from __future__ import annotations

import ast
import json
from pathlib import Path
import unittest

from e1r_engine.adapters.historical_data import (
    HistoricalDataAdapter,
)


ROOT = Path(__file__).resolve().parents[1]

RUN_BACKTEST = ROOT / "run_backtest.py"

BACKTEST = ROOT / "src/engine/backtest.py"

SPX_PATH = (
    ROOT
    / "data/research/e1_5y/raw/indices/SPX.json"
)

STOCK_DIR = (
    ROOT
    / "data/research/e1_5y/raw/stocks"
)


class FiveYearRCARevalidationContractTests(
    unittest.TestCase
):
    def test_run_backtest_parses_research_flag(
        self,
    ) -> None:
        source = RUN_BACKTEST.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            '"--research-5y" in sys.argv',
            source,
        )

        self.assertIn(
            'os.environ["SP500_RESEARCH_5Y"] = "1"',
            source,
        )

        self.assertIn(
            "data/research/e1_5y/raw",
            source,
        )

        self.assertIn(
            "_series_from_research_5y_file",
            source,
        )

    def test_frozen_research_dataset_contract(
        self,
    ) -> None:
        adapter = HistoricalDataAdapter(ROOT)

        spx = adapter.load_asset_series(
            SPX_PATH,
            symbol="SPX",
        )

        dates = [
            bar.date
            for bar in spx.bars
            if (
                "2021-06-11"
                <= bar.date
                <= "2026-06-18"
            )
        ]

        self.assertEqual(len(dates), 1261)
        self.assertEqual(
            dates[0],
            "2021-06-11",
        )
        self.assertEqual(
            dates[-1],
            "2026-06-18",
        )

        self.assertEqual(
            len(list(STOCK_DIR.glob("*.json"))),
            542,
        )

    def test_runtime_regime_objects_are_not_exported(
        self,
    ) -> None:
        source = BACKTEST.read_text(
            encoding="utf-8"
        )

        self.assertNotIn(
            '_result["resolved_assumptions"] = assumptions',
            source,
        )

        self.assertIn(
            'if key != "e1r_regime_daily"',
            source,
        )

        self.assertIn(
            '"e1r_regime_daily_runtime_object_exported"',
            source,
        )

        self.assertIn(
            '"e1r_regime_daily_record_count"',
            source,
        )

    def test_sources_compile(self) -> None:
        for path in (
            RUN_BACKTEST,
            BACKTEST,
        ):
            ast.parse(
                path.read_text(
                    encoding="utf-8"
                )
            )

    def test_safe_assumption_shape_is_json_serializable(
        self,
    ) -> None:
        safe = {
            "e1r_regime_source":
                "engine://canonical_regime",
            "e1r_regime_daily_runtime_object_exported":
                False,
            "e1r_regime_daily_record_count":
                1562,
        }

        encoded = json.dumps(safe)

        self.assertIn(
            "engine://canonical_regime",
            encoded,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
