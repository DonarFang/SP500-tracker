from __future__ import annotations

from collections import Counter
from datetime import date
import json
import math
from pathlib import Path
import unittest

from e1r_engine.adapters.historical_data import (
    HistoricalDataAdapter,
)
from e1r_engine.canonical_regime import (
    CanonicalRegimeGenerator,
    RegimeDecision,
)
from e1r_engine.contracts import (
    AssetSeries,
    DailyBar,
    MarketSnapshot,
)
from e1r_engine.core import E1RCoreEngine
from e1r_engine.regime_router import RegimeRouter
from e1r_engine.state import AccountState


ROOT = Path(__file__).resolve().parents[1]
SPX_PATH = (
    ROOT
    / "data/research/e1_5y/raw/indices/SPX.json"
)
REGIME_PATH = (
    ROOT
    / "data/research/e1_5y/regimes/spx_regime_daily.json"
)


def load_spx_series() -> AssetSeries:
    adapter = HistoricalDataAdapter(ROOT)
    return adapter.load_asset_series(
        SPX_PATH,
        symbol="SPX",
    )


class CanonicalRegimeIntegrationTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spx = load_spx_series()
        cls.timeline = (
            CanonicalRegimeGenerator.generate(cls.spx)
        )
        cls.reference_daily = json.loads(
            REGIME_PATH.read_text()
        )["daily_regime"]

    def test_rejects_duplicate_dates(self) -> None:
        bar = DailyBar(
            date="2026-01-02",
            open=None,
            high=None,
            low=None,
            close=100.0,
        )

        with self.assertRaisesRegex(
            ValueError,
            "duplicate SPX bar date",
        ):
            CanonicalRegimeGenerator.generate(
                [bar, bar]
            )

    def test_rejects_invalid_closes(self) -> None:
        invalid_values = [
            0.0,
            -1.0,
            math.nan,
            math.inf,
        ]

        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    CanonicalRegimeGenerator.generate([
                        DailyBar(
                            date="2026-01-02",
                            open=None,
                            high=None,
                            low=None,
                            close=value,
                        )
                    ])

    def test_reorders_without_mutating_input(
        self,
    ) -> None:
        bars = [
            DailyBar(
                date="2026-01-09",
                open=None,
                high=None,
                low=None,
                close=101.0,
            ),
            DailyBar(
                date="2026-01-02",
                open=None,
                high=None,
                low=None,
                close=100.0,
            ),
        ]
        original = list(bars)

        timeline = CanonicalRegimeGenerator.generate(
            bars
        )

        self.assertEqual(bars, original)
        self.assertTrue(
            timeline.metadata["input_reordered"]
        )
        self.assertEqual(
            list(timeline.daily_decisions),
            ["2026-01-02", "2026-01-09"],
        )

    def test_engine_generated_timeline_shape(
        self,
    ) -> None:
        self.assertEqual(
            len(self.timeline.weekly_decisions),
            325,
        )
        self.assertEqual(
            len(self.timeline.daily_decisions),
            1562,
        )
        self.assertEqual(
            list(self.timeline.daily_decisions)[0],
            "2020-04-01",
        )
        self.assertEqual(
            list(self.timeline.daily_decisions)[-1],
            "2026-06-18",
        )

    def test_selected_reference_states_match(
        self,
    ) -> None:
        selected_dates = {
            "2020-04-01",
            "2020-04-02",
            "2020-04-03",
        }

        first_by_state: dict[
            tuple[str, str],
            str,
        ] = {}

        for date_value, row in (
            self.reference_daily.items()
        ):
            key = (
                row["regime"],
                row.get("subclass")
                or "NO_SUBCLASS",
            )
            first_by_state.setdefault(
                key,
                date_value,
            )

        selected_dates.update(
            first_by_state.values()
        )

        for date_value in sorted(selected_dates):
            with self.subTest(date=date_value):
                generated = (
                    self.timeline.decision_for_date(
                        date_value
                    )
                )
                reference = self.reference_daily[
                    date_value
                ]

                self.assertEqual(
                    generated.regime,
                    reference["regime"],
                )
                self.assertEqual(
                    generated.subclass,
                    reference.get("subclass"),
                )

    def test_one_week_lag_invariant(self) -> None:
        for decision in (
            self.timeline.daily_decisions.values()
        ):
            if (
                decision.source_week_end_date
                is None
            ):
                self.assertEqual(
                    decision.regime,
                    "UNCLASSIFIED",
                )
                continue

            effective_date = date.fromisoformat(
                decision.date
            )
            monday = effective_date.fromordinal(
                effective_date.toordinal()
                - effective_date.weekday()
            )
            source_week_end = date.fromisoformat(
                decision.source_week_end_date
            )

            self.assertLess(
                source_week_end,
                monday,
            )

    def test_decision_record_contract(self) -> None:
        decision = RegimeDecision(
            date="2026-01-05",
            ready=False,
            regime="UNCLASSIFIED",
            reason="insufficient_history",
        )
        record = decision.to_record()

        self.assertEqual(
            record.spx_regime,
            "UNCLASSIFIED",
        )
        self.assertEqual(
            record.subclass,
            "NO_SUBCLASS",
        )
        self.assertFalse(record.raw["ready"])
        self.assertEqual(
            record.source_path,
            "engine://canonical_regime",
        )

    def test_artifact_adapter_preserves_warmup(
        self,
    ) -> None:
        adapter = HistoricalDataAdapter(ROOT)
        records = adapter.load_regime_daily()

        self.assertEqual(len(records), 1562)

        counts = Counter(
            record.spx_regime
            for record in records.values()
        )

        self.assertEqual(
            counts["UNCLASSIFIED"],
            253,
        )

    def test_generated_adapter_path(self) -> None:
        adapter = HistoricalDataAdapter(ROOT)
        records = adapter.generate_regime_daily(
            self.spx
        )

        self.assertEqual(len(records), 1562)
        self.assertEqual(
            records["2020-04-01"].spx_regime,
            "UNCLASSIFIED",
        )

    def test_router_valid_and_defensive_paths(
        self,
    ) -> None:
        router = RegimeRouter()

        cases = [
            (
                "UPTREND",
                "NO_SUBCLASS",
                "UPTREND",
                "route_uptrend",
            ),
            (
                "SIDEWAYS",
                "MA_CONFLICT",
                "SIDEWAYS_MA_CONFLICT",
                "route_sideways_ma_conflict",
            ),
            (
                "SIDEWAYS",
                "DETERIORATION_TRANSITION",
                "DETERIORATION_TRANSITION",
                "route_deterioration_transition",
            ),
            (
                "SIDEWAYS",
                "RECOVERY_TRANSITION",
                "RECOVERY_TRANSITION",
                "route_recovery_transition",
            ),
            (
                "DOWNTREND",
                "NO_SUBCLASS",
                "DOWNTREND",
                "route_downtrend",
            ),
            (
                "UNCLASSIFIED",
                "NO_SUBCLASS",
                "CASH_DEFENSIVE",
                "route_unclassified_cash_defensive",
            ),
            (
                "DOWNTREND",
                "RECOVERY_TRANSITION",
                "CASH_DEFENSIVE",
                "route_invalid_regime_subclass_combination",
            ),
            (
                "MYSTERY",
                "NO_SUBCLASS",
                "CASH_DEFENSIVE",
                "route_unknown_cash_defensive",
            ),
        ]

        for (
            regime,
            subclass,
            expected_branch,
            expected_reason,
        ) in cases:
            with self.subTest(
                regime=regime,
                subclass=subclass,
            ):
                route = router.route(
                    "2026-01-05",
                    regime,
                    subclass,
                )
                self.assertEqual(
                    route.branch,
                    expected_branch,
                )
                self.assertEqual(
                    route.reason,
                    expected_reason,
                )

    def test_generated_path_reaches_core_engine(
        self,
    ) -> None:
        uptrend_date = next(
            date_value
            for date_value, decision
            in self.timeline.daily_decisions.items()
            if decision.regime == "UPTREND"
        )

        spx_bar = next(
            bar
            for bar in self.spx.bars
            if bar.date == uptrend_date
        )

        snapshot = MarketSnapshot(
            date=uptrend_date,
            universe=[],
            prices_by_symbol={},
            indices={"SPX": spx_bar},
            regime=self.timeline.record_for_date(
                uptrend_date
            ),
            metadata={
                "regime_source":
                    "GENERATED_CANONICAL",
            },
        )

        result = E1RCoreEngine().step(
            snapshot,
            AccountState.empty(
                date=uptrend_date
            ),
        )

        self.assertEqual(
            result.decision_trace.branch,
            "UPTREND",
        )
        self.assertEqual(
            result.decision_trace.market_regime,
            "UPTREND",
        )

    def test_unclassified_reaches_defensive_core(
        self,
    ) -> None:
        date_value = "2020-04-01"
        spx_bar = self.spx.bars[0]

        snapshot = MarketSnapshot(
            date=date_value,
            universe=[],
            prices_by_symbol={},
            indices={"SPX": spx_bar},
            regime=self.timeline.record_for_date(
                date_value
            ),
            metadata={
                "regime_source":
                    "GENERATED_CANONICAL",
            },
        )

        result = E1RCoreEngine().step(
            snapshot,
            AccountState.empty(
                date=date_value
            ),
        )

        self.assertEqual(
            result.decision_trace.branch,
            "CASH_DEFENSIVE",
        )
        self.assertIn(
            "route_unclassified_cash_defensive",
            result.decision_trace.reasons,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
