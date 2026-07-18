from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from e1r_engine.contracts import DailyBar
from e1r_engine.forward_composition import (
    ProductionForwardComposition,
    build_production_forward_composition,
)
from e1r_engine.forward_providers import (
    ExplicitMarketStateProvider,
    FormalManagementActionProvider,
    FormalMarketGateProvider,
    MarketStateRecord,
)


def dates(count: int = 90) -> list[str]:
    result = []
    year = 2025
    month = 1
    day = 1

    while len(result) < count:
        result.append(
            f"{year:04d}-{month:02d}-{day:02d}"
        )
        day += 1

        if day > 28:
            day = 1
            month += 1

        if month > 12:
            month = 1
            year += 1

    return result


def series(
    values: list[str],
    start: float,
    step: float,
):
    result = {}

    for index, date in enumerate(values):
        close = start + step * index

        result[date] = DailyBar(
            date=date,
            open=close,
            high=close,
            low=close,
            close=close,
            volume=None,
        )

    return result


class Step2CompositionTests(
    unittest.TestCase
):
    def setUp(self) -> None:
        self.dates = dates()
        self.date = self.dates[-1]

        self.series_by_symbol = {
            "SPX": series(
                self.dates,
                100.0,
                1.0,
            ),
            "NDX": series(
                self.dates,
                200.0,
                1.0,
            ),
            "SOX": series(
                self.dates,
                300.0,
                1.0,
            ),
            "AAA": series(
                self.dates,
                50.0,
                0.5,
            ),
        }

    def test_explicit_market_state_is_not_recomputed(
        self,
    ) -> None:
        record = MarketStateRecord(
            date=self.date,
            market_state="CAUTIOUS_ON",
            entry_capacity=2,
            spx_close=100.0,
            spx_ma50=200.0,
            spx_day_return=-0.01,
        )

        provider = FormalMarketGateProvider(
            market_state_provider=(
                ExplicitMarketStateProvider(
                    records_by_date={
                        self.date: record
                    }
                )
            )
        )

        decision = provider(
            date=self.date,
            index_series={
                "SPX":
                    self.series_by_symbol["SPX"],
                "NDX":
                    self.series_by_symbol["NDX"],
                "SOX":
                    self.series_by_symbol["SOX"],
            },
        )

        self.assertEqual(
            decision.market_state,
            "CAUTIOUS_ON",
        )
        self.assertEqual(
            decision.entry_capacity,
            2,
        )
        self.assertEqual(
            decision.gate_state,
            "ALLOW",
        )
        self.assertTrue(
            decision.market_entry_allowed
        )

    def test_shock_precedence(
        self,
    ) -> None:
        record = MarketStateRecord(
            date=self.date,
            market_state="CASH_MODE",
            entry_capacity=0,
            spx_day_return=-0.021,
        )

        provider = FormalMarketGateProvider(
            market_state_provider=(
                ExplicitMarketStateProvider(
                    records_by_date={
                        self.date: record
                    }
                )
            )
        )

        decision = provider(
            date=self.date,
            index_series={},
        )

        self.assertEqual(
            decision.gate_state,
            "SHOCK",
        )
        self.assertTrue(
            decision.market_shock
        )
        self.assertFalse(
            decision.market_entry_allowed
        )

    def test_management_provider_empty_account(
        self,
    ) -> None:
        account = Mock()
        account.positions = {}

        actions = (
            FormalManagementActionProvider()(
                date=self.date,
                account=account,
                stock_series={},
            )
        )

        self.assertEqual(actions, {})

    def test_composition_root_instantiates_without_run(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            runtime_root = root / "runtime"

            market_states = {
                date: MarketStateRecord(
                    date=date,
                    market_state="FULL_ON",
                    entry_capacity=3,
                    spx_close=(
                        self.series_by_symbol[
                            "SPX"
                        ][date].close
                    ),
                    spx_ma50=None,
                    spx_day_return=0.0,
                )
                for date in self.dates
            }

            composition = (
                build_production_forward_composition(
                    seed_root=root / "seed",
                    runtime_root=runtime_root,
                    trading_dates=self.dates,
                    universe=("AAA",),
                    series_by_symbol=(
                        self.series_by_symbol
                    ),
                    market_state_by_date=(
                        market_states
                    ),
                    runtime_commit_provider=(
                        lambda: "test-commit"
                    ),
                )
            )

            self.assertIsInstance(
                composition,
                ProductionForwardComposition,
            )

            self.assertFalse(
                runtime_root.exists()
            )

            self.assertFalse(
                composition.repository.exists()
            )

            self.assertIs(
                composition.runner.committer,
                composition.committer,
            )


if __name__ == "__main__":
    unittest.main()
