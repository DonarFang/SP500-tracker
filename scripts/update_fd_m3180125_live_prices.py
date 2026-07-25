#!/usr/bin/env python3
"""Update independent `data/live_prices` Daily OHLCV via Yahoo Finance."""

from __future__ import annotations

import argparse
from datetime import date, timedelta
import json
from pathlib import Path
import subprocess
from typing import Mapping, Sequence


class YahooDailyProvider:
    def fetch(
        self,
        *,
        provider_symbol: str,
        start_date: date,
        end_date: date,
    ) -> Sequence[Mapping[str, object]]:
        import yfinance as yf

        # yfinance end is exclusive.
        frame = yf.download(
            provider_symbol,
            start=start_date.isoformat(),
            end=(end_date + timedelta(days=1)).isoformat(),
            interval="1d",
            auto_adjust=False,
            actions=False,
            progress=False,
            threads=False,
        )
        if frame is None or frame.empty:
            return []

        rows = []
        for index, row in frame.iterrows():
            def scalar(name: str) -> object:
                value = row[name]
                if hasattr(value, "iloc"):
                    value = value.iloc[0]
                return value

            rows.append(
                {
                    "date": index.date().isoformat(),
                    "open": scalar("Open"),
                    "high": scalar("High"),
                    "low": scalar("Low"),
                    "close": scalar("Close"),
                    "volume": scalar("Volume"),
                }
            )
        return rows


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        text=True,
    ).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--price-root",
        default="data/live_prices",
    )
    parser.add_argument(
        "--status-path",
        default=(
            "exports/official/"
            "FD-M3180125-SP500-TOP3-engine/"
            "live/automation/current_data_update.json"
        ),
    )
    parser.add_argument(
        "--expected-latest-market-date",
        required=True,
    )
    parser.add_argument(
        "--lookback-days",
        type=int,
        default=7,
    )
    args = parser.parse_args()

    from e1r_engine.live_data_update import LiveDataUpdater

    result = LiveDataUpdater(
        price_root=Path(args.price_root),
        status_path=Path(args.status_path),
        provider=YahooDailyProvider(),
        source_commit=git_head(),
        lookback_days=args.lookback_days,
    ).update(
        expected_latest_market_date=date.fromisoformat(
            args.expected_latest_market_date
        )
    )

    print(
        json.dumps(
            result.to_payload(),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if result.data_status == "CURRENT" else 2


if __name__ == "__main__":
    raise SystemExit(main())
