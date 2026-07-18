from __future__ import annotations

from collections import Counter
from datetime import date, timedelta
import json
from pathlib import Path
import unittest

from e1r_engine.adapters.historical_data import (
    HistoricalDataAdapter,
)
from e1r_engine.canonical_regime import (
    CanonicalRegimeGenerator,
)
from e1r_engine.contracts import MarketSnapshot
from e1r_engine.forward_runtime import (
    CanonicalDailyDecisionRouter,
)
from e1r_engine.state import AccountState


ROOT = Path(__file__).resolve().parents[1]

BACKTEST_PATH = ROOT / "src/engine/backtest.py"

ADAPTER_PATH = (
    ROOT
    / "src/e1r_engine/adapters/historical_data.py"
)

FORWARD_RUNTIME_PATH = (
    ROOT
    / "src/e1r_engine/forward_runtime.py"
)

SPX_PATH = (
    ROOT
    / "data/research/e1_5y/raw/indices/SPX.json"
)

DAILY_PATH = (
    ROOT
    / "data/research/e1_5y/regimes/"
    "spx_regime_daily.json"
)


class CanonicalRegimeRuntimeTakeoverTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.adapter = HistoricalDataAdapter(ROOT)

        cls.spx = cls.adapter.load_asset_series(
            SPX_PATH,
            symbol="SPX",
        )

        cls.timeline = (
            CanonicalRegimeGenerator.generate(
                cls.spx
            )
        )

        cls.daily_reference = json.loads(
            DAILY_PATH.read_text()
        )["daily_regime"]

    def test_full_daily_reproduction(self) -> None:
        generated = self.timeline.daily_decisions
        reference = self.daily_reference

        self.assertEqual(
            set(generated),
            set(reference),
        )

        mismatches = []

        for date_value in sorted(reference):
            decision = generated[date_value]
            expected = reference[date_value]

            if (
                decision.regime
                != expected["regime"]
                or decision.subclass
                != expected.get("subclass")
            ):
                mismatches.append(date_value)

        self.assertEqual(mismatches, [])

        self.assertEqual(
            Counter(
                (
                    decision.regime,
                    decision.subclass,
                )
                for decision
                in generated.values()
            ),
            Counter(
                (
                    row["regime"],
                    row.get("subclass"),
                )
                for row
                in reference.values()
            ),
        )

    def test_source_week_and_lag(self) -> None:
        weekly_dates = [
            date.fromisoformat(
                decision.date
            )
            for decision
            in self.timeline.weekly_decisions
        ]

        mismatches = []
        violations = []

        for (
            trading_date,
            decision,
        ) in self.timeline.daily_decisions.items():
            parsed = date.fromisoformat(
                trading_date
            )
            monday = parsed - timedelta(
                days=parsed.weekday()
            )

            eligible = [
                week_end
                for week_end in weekly_dates
                if week_end < monday
            ]

            expected = (
                eligible[-1].isoformat()
                if eligible
                else None
            )

            if (
                decision.source_week_end_date
                != expected
            ):
                mismatches.append(trading_date)

            if (
                decision.source_week_end_date
                is not None
                and not (
                    date.fromisoformat(
                        decision.source_week_end_date
                    )
                    < monday
                )
            ):
                violations.append(trading_date)

        self.assertEqual(mismatches, [])
        self.assertEqual(violations, [])

    def test_adapter_bundle_default_is_generated(
        self,
    ) -> None:
        source = ADAPTER_PATH.read_text()

        self.assertIn(
            "regime_daily = self.generate_regime_daily(",
            source,
        )

        self.assertIn(
            '"regime_runtime_source":',
            source,
        )

        self.assertIn(
            '"GENERATED_CANONICAL"',
            source,
        )

        self.assertNotIn(
            "regime_daily = self.load_regime_daily()",
            source,
        )

    def test_backtest_formal_runtime_has_no_artifact_loader(
        self,
    ) -> None:
        source = BACKTEST_PATH.read_text()

        self.assertNotIn(
            "def _load_e1r_regime_daily",
            source,
        )

        self.assertIn(
            "def _generate_e1r_regime_daily",
            source,
        )

        self.assertIn(
            "adapter.generate_regime_daily(",
            source,
        )

        self.assertNotIn(
            'spx_regime="UPTREND"',
            source,
        )

        self.assertIn(
            "regime=_e1r_record_on(date_t)",
            source,
        )

        self.assertGreaterEqual(
            source.count(
                '"e1r_regime_source":     '
                '"engine://canonical_regime"'
            ),
            2,
        )

    def test_legacy_reference_is_not_formal_source(
        self,
    ) -> None:
        source = BACKTEST_PATH.read_text()

        self.assertIn(
            "E1R_REGIME_AWARE_V0_2_"
            "LEGACY_SIDECAR_REFERENCE",
            source,
        )

        self.assertIn(
            "LEGACY_VIRTUAL_SIDECAR_"
            "REFERENCE_NOT_FORMAL",
            source,
        )

        self.assertIn(
            '"formal_selection_eligible"] = False',
            source,
        )

    def test_generated_record_reaches_forward_boundary(
        self,
    ) -> None:
        date_value = "2020-04-01"

        snapshot = MarketSnapshot(
            date=date_value,
            universe=[],
            prices_by_symbol={},
            indices={
                "SPX": self.spx.bars[0],
            },
            regime=(
                self.timeline.record_for_date(
                    date_value
                )
            ),
            metadata={
                "regime_source":
                    "engine://canonical_regime",
            },
        )

        result = CanonicalDailyDecisionRouter().decide(
            snapshot=snapshot,
            account=AccountState.empty(
                date=date_value
            ),
        )

        self.assertEqual(
            result.metadata["branch"],
            "CASH_DEFENSIVE",
        )

        self.assertFalse(
            result.metadata["new_risk_expansion"]
        )

        self.assertEqual(
            [
                intent.intent_type
                for intent
                in result.order_intents
            ],
            ["NOOP"],
        )

    def test_forward_runtime_has_no_regime_artifact_read(
        self,
    ) -> None:
        source = FORWARD_RUNTIME_PATH.read_text()

        self.assertNotIn(
            "spx_regime_daily.json",
            source,
        )

        self.assertNotIn(
            "spx_weekly_regimes.json",
            source,
        )

        self.assertIn(
            "snapshot.regime",
            source,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
