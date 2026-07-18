from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from e1r_engine.contracts import DailyBar
from e1r_engine.forward_orchestrator import (
    ForwardMarketSnapshotBuilder,
    ForwardRegimeProvider,
    ForwardStrategyInputBuilder,
    OfficialForwardCatchupRunner,
)
from e1r_engine.forward_runtime import (
    ForwardAccountRepository,
    ForwardContractError,
    ForwardDatePlanner,
    ForwardMarketDataAdapter,
    ForwardSeedLoader,
)
from e1r_engine.market_gate import MarketGateDecision
from e1r_engine.state import AccountState


def bar(
    date: str,
    close: float,
) -> DailyBar:
    return DailyBar(
        date=date,
        open=close,
        high=close + 1.0,
        low=close - 1.0,
        close=close,
        volume=None,
    )


def series(
    *,
    dates: list[str],
    start: float,
    step: float,
) -> dict[str, DailyBar]:
    return {
        date: bar(
            date,
            start + index * step,
        )
        for index, date in enumerate(dates)
    }


class GateProvider:
    def __call__(
        self,
        *,
        date: str,
        index_series,
    ) -> MarketGateDecision:
        self.last_date = date
        self.index_series = index_series

        return MarketGateDecision(
            date=date,
            market_state="FULL_ON",
            entry_capacity=3,
            market_shock=False,
            market_risk_off=False,
            market_entry_allowed=True,
            gate_state="ALLOW",
            trace={
                "source": "test_formal_gate",
            },
        )


class ManagementProvider:
    def __call__(
        self,
        *,
        date: str,
        account: AccountState,
        stock_series,
    ):
        self.last_date = date
        self.account = account
        self.stock_series = stock_series

        return {
            symbol: "HOLD"
            for symbol in account.positions
        }


class FakeSeedLoader:
    def __init__(self, state):
        self.state = state

    def load(self):
        return self.state


class TestForwardOrchestrator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.history_dates = [
            f"2026-01-{day:02d}"
            for day in range(1, 32)
        ] + [
            f"2026-02-{day:02d}"
            for day in range(1, 29)
        ] + [
            "2026-03-01",
            "2026-03-02",
            "2026-03-03",
            "2026-03-04",
            "2026-03-05",
            "2026-03-06",
            "2026-03-09",
            "2026-03-10",
        ]

        cls.forward_date = "2026-03-10"

        cls.series_by_symbol = {
            "SPX": series(
                dates=cls.history_dates,
                start=100.0,
                step=1.0,
            ),
            "NDX": series(
                dates=cls.history_dates,
                start=200.0,
                step=1.5,
            ),
            "SOX": series(
                dates=cls.history_dates,
                start=300.0,
                step=2.0,
            ),
            "AAA": series(
                dates=cls.history_dates,
                start=50.0,
                step=1.0,
            ),
            "BBB": series(
                dates=cls.history_dates,
                start=80.0,
                step=0.7,
            ),
            "CCC": series(
                dates=cls.history_dates,
                start=120.0,
                step=0.4,
            ),
        }

    def test_regime_provider_uses_canonical_generator(
        self,
    ) -> None:
        provider = (
            ForwardRegimeProvider
            .from_spx_series(
                spx_series=(
                    self.series_by_symbol["SPX"]
                )
            )
        )

        record = provider.record_for_date(
            self.forward_date
        )

        self.assertEqual(
            record.source_path,
            "engine://canonical_regime",
        )

    def test_snapshot_builder_uses_exact_daily_bars(
        self,
    ) -> None:
        provider = (
            ForwardRegimeProvider
            .from_spx_series(
                spx_series=(
                    self.series_by_symbol["SPX"]
                )
            )
        )

        builder = ForwardMarketSnapshotBuilder(
            regime_provider=provider
        )

        snapshot = builder.build(
            date=self.forward_date,
            universe=("AAA", "BBB", "CCC"),
            series_by_symbol=(
                self.series_by_symbol
            ),
        )

        self.assertEqual(
            snapshot.date,
            self.forward_date,
        )
        self.assertEqual(
            snapshot.universe,
            ["AAA", "BBB", "CCC"],
        )
        self.assertEqual(
            set(snapshot.indices),
            {"SPX", "NDX", "SOX"},
        )
        self.assertEqual(
            snapshot.metadata["regime_source"],
            "engine://canonical_regime",
        )

    def test_uptrend_inputs_reuse_signal_adapter(
        self,
    ) -> None:
        provider = (
            ForwardRegimeProvider
            .from_spx_series(
                spx_series=(
                    self.series_by_symbol["SPX"]
                )
            )
        )

        snapshot = ForwardMarketSnapshotBuilder(
            regime_provider=provider
        ).build(
            date=self.forward_date,
            universe=("AAA", "BBB", "CCC"),
            series_by_symbol=(
                self.series_by_symbol
            ),
        )

        object.__setattr__(
            snapshot.regime,
            "spx_regime",
            "UPTREND",
        )

        gate = GateProvider()
        management = ManagementProvider()

        result = ForwardStrategyInputBuilder(
            market_gate_provider=gate,
            management_action_provider=management,
            min_uptrend_history=61,
        ).build(
            snapshot=snapshot,
            account=AccountState.empty(
                date=self.forward_date,
                initial_cash=100000.0,
            ),
            universe=("AAA", "BBB", "CCC"),
            series_by_symbol=(
                self.series_by_symbol
            ),
        )

        self.assertIsNotNone(
            result.uptrend_inputs
        )
        self.assertIsNone(
            result.sideways_context
        )
        self.assertEqual(
            result.uptrend_inputs.date,
            self.forward_date,
        )
        self.assertEqual(
            result.metadata["uptrend_adapter"],
            "UptrendSignalAdapter",
        )

    def test_sideways_context_builder_constructs_assets(
        self,
    ) -> None:
        provider = (
            ForwardRegimeProvider
            .from_spx_series(
                spx_series=(
                    self.series_by_symbol["SPX"]
                )
            )
        )

        snapshot = ForwardMarketSnapshotBuilder(
            regime_provider=provider
        ).build(
            date=self.forward_date,
            universe=("AAA", "BBB", "CCC"),
            series_by_symbol=(
                self.series_by_symbol
            ),
        )

        object.__setattr__(
            snapshot.regime,
            "spx_regime",
            "SIDEWAYS",
        )
        object.__setattr__(
            snapshot.regime,
            "subclass",
            "MA_CONFLICT",
        )

        result = ForwardStrategyInputBuilder(
            market_gate_provider=GateProvider(),
            management_action_provider=(
                ManagementProvider()
            ),
        ).build(
            snapshot=snapshot,
            account=AccountState.empty(
                date=self.forward_date,
                initial_cash=100000.0,
            ),
            universe=("AAA", "BBB", "CCC"),
            series_by_symbol=(
                self.series_by_symbol
            ),
        )

        self.assertIsNone(
            result.uptrend_inputs
        )
        self.assertIsNotNone(
            result.sideways_context
        )
        self.assertEqual(
            set(result.sideways_context.stocks),
            {"AAA", "BBB", "CCC"},
        )
        self.assertEqual(
            result.sideways_context.spx[
                "symbol"
            ],
            "SPX",
        )

    def test_runner_refuses_write_without_authorization(
        self,
    ) -> None:
        runner = object.__new__(
            OfficialForwardCatchupRunner
        )

        with self.assertRaisesRegex(
            ForwardContractError,
            "not authorized",
        ):
            runner.run(
                allow_official_write=False
            )

    def test_dry_run_never_calls_committer(
        self,
    ) -> None:
        provider = (
            ForwardRegimeProvider
            .from_spx_series(
                spx_series=(
                    self.series_by_symbol["SPX"]
                )
            )
        )

        snapshot_builder = (
            ForwardMarketSnapshotBuilder(
                regime_provider=provider
            )
        )

        state = AccountState.empty(
            date=self.forward_date,
            initial_cash=100000.0,
        )

        runtime_state = Mock()
        runtime_state.account = state
        runtime_state.last_committed_date = None
        runtime_state.validate = Mock()

        repository = Mock()
        repository.exists.return_value = False

        committer = Mock()

        runner = OfficialForwardCatchupRunner(
            seed_loader=FakeSeedLoader(
                runtime_state
            ),
            repository=repository,
            date_planner=ForwardDatePlanner(
                [self.forward_date]
            ),
            market_data_adapter=(
                ForwardMarketDataAdapter()
            ),
            snapshot_builder=snapshot_builder,
            strategy_input_builder=(
                ForwardStrategyInputBuilder(
                    market_gate_provider=(
                        GateProvider()
                    ),
                    management_action_provider=(
                        ManagementProvider()
                    ),
                    min_uptrend_history=61,
                )
            ),
            committer=committer,
            universe=("AAA", "BBB", "CCC"),
            series_by_symbol=(
                self.series_by_symbol
            ),
            required_execution_symbols=(
                "SPX",
                "NDX",
                "SOX",
                "AAA",
                "BBB",
                "CCC",
            ),
        )

        result = runner.dry_run()

        self.assertEqual(
            result.status,
            "PASS_FORWARD_ORCHESTRATOR_DRY_RUN",
        )
        self.assertFalse(
            result.repository_initialized
        )
        self.assertFalse(
            result.commit_day_called
        )
        repository.initialize.assert_not_called()
        committer.commit_day.assert_not_called()


if __name__ == "__main__":
    unittest.main()
