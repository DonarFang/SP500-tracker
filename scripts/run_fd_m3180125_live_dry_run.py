#!/usr/bin/env python3
"""Run the formal unactivated FD-M3180125 Live production composition."""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path

from e1r_engine.live_composition import (
    run_unactivated_live_acceptance,
)


DEFAULT_LIVE_ROOT = Path(
    "exports/official/"
    "FD-M3180125-SP500-TOP3-engine/"
    "live"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--price-root",
        default="data/live_prices",
    )
    parser.add_argument(
        "--live-root",
        default=str(DEFAULT_LIVE_ROOT),
    )
    parser.add_argument(
        "--data-status-path",
        default=str(
            DEFAULT_LIVE_ROOT
            / "automation"
            / "current_data_update.json"
        ),
    )
    parser.add_argument(
        "--market-date",
        required=True,
    )
    parser.add_argument(
        "--expected-execution-date",
        required=True,
    )
    parser.add_argument(
        "--expected-stock-count",
        type=int,
        default=498,
    )
    parser.add_argument(
        "--min-bars",
        type=int,
        default=120,
    )
    args = parser.parse_args()

    acceptance = run_unactivated_live_acceptance(
        price_root=Path(args.price_root),
        live_root=Path(args.live_root),
        data_status_path=Path(
            args.data_status_path
        ),
        market_date=date.fromisoformat(
            args.market_date
        ),
        expected_execution_date=date.fromisoformat(
            args.expected_execution_date
        ),
        expected_stock_count=(
            args.expected_stock_count
        ),
        min_bars=args.min_bars,
    )

    print(
        json.dumps(
            acceptance,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
