from __future__ import annotations

from e1r_engine.core import E1RCoreEngine

import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import Mock

from e1r_engine.forward_orchestrator import (
    ForwardStrategyInputBuilder,
)
from e1r_engine.forward_production_composition import (
    ForwardProductionData,
    ProductionForwardComposition,
    ProductionForwardDataAdapter,
    build_production_forward_composition,
)


def business_dates(count: int) -> list[str]:
    result: list[str] = []
    current = date(2023, 1, 2)

    while len(result) < count:
        if current.weekday() < 5:
            result.append(current.isoformat())

        current += timedelta(days=1)

    return result


def write_price_file(
    path: Path,
    *,
    dates: list[str],
    start: float,
    step: float,
) -> None:
    rows = []

    for index, trading_date in enumerate(dates):
        close = start + step * index

        rows.append({
            "date": trading_date,
            "open": close - 0.25,
            "high": close + 0.50,
            "low": close - 0.50,
            "close": close,
            "volume": 1_000_000 + index,
        })

    path.write_text(
        json.dumps(rows, indent=2) + "\n",
        encoding="utf-8",
    )


class ForwardProductionCompositionTests(
    unittest.TestCase
):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.dates = business_dates(520)

        self.files: dict[str, Path] = {}

        for symbol, start, step in (
            ("SPX", 4000.0, 1.0),
            ("NDX", 12000.0, 2.0),
            ("SOX", 3000.0, 1.5),
            ("AAA", 50.0, 0.10),
            ("BBB", 80.0, 0.20),
            ("CCC", 110.0, 0.15),
        ):
            path = self.root / f"{symbol}.json"

            write_price_file(
                path,
                dates=self.dates,
                start=start,
                step=step,
            )

            self.files[symbol] = path

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_real_files_are_normalized(
        self,
    ) -> None:
        data = (
            ProductionForwardDataAdapter()
            .load(
                price_files_by_symbol=self.files,
                universe=(
                    "AAA",
                    "BBB",
                    "CCC",
                ),
            )
        )

        self.assertIsInstance(
            data,
            ForwardProductionData,
        )

        self.assertEqual(
            data.universe,
            (
                "AAA",
                "BBB",
                "CCC",
            ),
        )

        self.assertEqual(
            data.required_symbols,
            (
                "SPX",
                "NDX",
                "SOX",
                "AAA",
                "BBB",
                "CCC",
            ),
        )

        self.assertEqual(
            data.latest_complete_common_date,
            self.dates[-1],
        )

        self.assertEqual(
            data.trading_dates,
            tuple(self.dates),
        )

        self.assertEqual(
            set(data.source_hashes),
            set(data.required_symbols),
        )

    def test_missing_required_file_is_rejected(
        self,
    ) -> None:
        incomplete = dict(self.files)
        incomplete.pop("CCC")

        with self.assertRaisesRegex(
            ValueError,
            "Missing production price files",
        ):
            (
                ProductionForwardDataAdapter()
                .load(
                    price_files_by_symbol=incomplete,
                    universe=(
                        "AAA",
                        "BBB",
                        "CCC",
                    ),
                )
            )

    def test_composition_wires_existing_runtime(
        self,
    ) -> None:
        runtime_root = self.root / "runtime"

        strategy_input_builder = (
            Mock(
                spec=ForwardStrategyInputBuilder
            )
        )

        strategy_input_builder.__class__ = (
            ForwardStrategyInputBuilder
        )

        composition = (
            build_production_forward_composition(
                seed_root=self.root / "seed",
                runtime_root=runtime_root,
                price_files_by_symbol=self.files,
                universe=(
                    "AAA",
                    "BBB",
                    "CCC",
                ),
                strategy_input_builder=(
                    strategy_input_builder
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

        self.assertIs(
            composition.strategy_input_builder,
            strategy_input_builder,
        )

        self.assertIs(
            composition.runner.committer,
            composition.committer,
        )

        self.assertIs(
            composition.runner.snapshot_builder,
            composition.snapshot_builder,
        )

        self.assertIs(
            composition.runner.strategy_input_builder,
            strategy_input_builder,
        )

        self.assertEqual(
            composition.execution_engine.max_positions,
            3,
        )

        self.assertFalse(runtime_root.exists())
        self.assertFalse(
            composition.repository.exists()
        )


if __name__ == "__main__":
    unittest.main()
