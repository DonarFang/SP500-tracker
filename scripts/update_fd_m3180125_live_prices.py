#!/usr/bin/env python3
"""Best-effort update of independent `data/live_prices` via Yahoo.

This is the Personal Live implementation of the already-proven per-symbol
update boundary:

* the catalogue is owned by existing `data/live_prices` filenames;
* an unavailable ordinary symbol preserves its existing file;
* malformed Yahoo rows are discarded rather than written;
* required Live indices determine whether the requested market date is current;
* no Forward data, account, runtime, status, or equity is read or written.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
import json
import math
import os
from pathlib import Path
import subprocess
from typing import Mapping, Sequence


def _finite_number(value: object) -> float | None:
    """Return a finite float or None."""
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def _valid_provider_row(
    *,
    market_date: object,
    open_value: object,
    high_value: object,
    low_value: object,
    close_value: object,
    volume_value: object,
) -> dict[str, object] | None:
    """Normalize one Yahoo row; invalid rows become unavailable input."""
    try:
        day = date.fromisoformat(str(market_date)[:10]).isoformat()
    except ValueError:
        return None

    open_price = _finite_number(open_value)
    high = _finite_number(high_value)
    low = _finite_number(low_value)
    close = _finite_number(close_value)
    volume = _finite_number(volume_value)

    if None in (open_price, high, low, close, volume):
        return None
    assert open_price is not None
    assert high is not None
    assert low is not None
    assert close is not None
    assert volume is not None

    if min(open_price, high, low, close) <= 0:
        return None
    if volume < 0:
        return None

    return {
        "date": day,
        "open": open_price,
        "high": high,
        "low": low,
        "close": close,
        "volume": volume,
    }


class YahooDailyProvider:
    """Yahoo adapter that returns only valid finite positive OHLC rows."""

    def fetch(
        self,
        *,
        provider_symbol: str,
        start_date: date,
        end_date: date,
    ) -> Sequence[Mapping[str, object]]:
        import yfinance as yf

        try:
            frame = yf.download(
                provider_symbol,
                start=start_date.isoformat(),
                # yfinance end is exclusive.
                end=(end_date + timedelta(days=1)).isoformat(),
                interval="1d",
                auto_adjust=False,
                actions=False,
                progress=False,
                threads=False,
            )
        except Exception:
            return []

        if frame is None or frame.empty:
            return []

        rows: list[dict[str, object]] = []
        for index, source_row in frame.iterrows():

            def scalar(name: str) -> object:
                try:
                    value = source_row[name]
                except (KeyError, TypeError):
                    return None
                if hasattr(value, "iloc"):
                    try:
                        value = value.iloc[0]
                    except (IndexError, TypeError):
                        return None
                return value

            normalized = _valid_provider_row(
                market_date=index,
                open_value=scalar("Open"),
                high_value=scalar("High"),
                low_value=scalar("Low"),
                close_value=scalar("Close"),
                volume_value=scalar("Volume"),
            )
            if normalized is not None:
                rows.append(normalized)

        return rows


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        text=True,
    ).strip()


def _promote_ordinary_unavailable_to_current(
    payload: dict[str, object],
    *,
    expected_latest_market_date: date,
    now: datetime,
) -> dict[str, object]:
    """Use the latest complete required-index date as the Live data date.

    This follows the proven Engine Forward responsibility split:
    the updater preserves and records the data actually available, while the
    daily runner decides whether that date is new and runnable. A wall-clock
    date does not fabricate an unavailable EOD session.

    Ordinary unavailable symbols remain recorded and preserve their files.
    Required Live indices still determine latest_market_date inside
    LiveDataUpdater. No Forward data or runtime state is consulted.
    """
    if payload.get("catalogue_changed") is not False:
        return payload

    latest_raw = payload.get("latest_market_date")
    if latest_raw is None:
        return payload

    try:
        latest = date.fromisoformat(str(latest_raw))
    except ValueError:
        return payload

    if payload.get("data_status") not in {"PARTIAL", "STALE"}:
        return payload

    payload["requested_latest_market_date"] = (
        expected_latest_market_date.isoformat()
    )
    payload["expected_latest_market_date"] = latest.isoformat()
    payload["data_status"] = "CURRENT"
    payload["missing_dates"] = []
    payload["last_successful_update_at"] = now.isoformat()
    return payload


def _atomic_write_payload(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = (
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(body)
    os.replace(temporary, path)


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

    price_root = Path(args.price_root)
    status_path = Path(args.status_path)

    if price_root.as_posix() != "data/live_prices":
        raise RuntimeError(
            "Personal Live updater must use data/live_prices"
        )
    if "/live/automation/" not in f"/{status_path.as_posix()}":
        raise RuntimeError(
            "Personal Live updater status must remain in Live automation"
        )

    from e1r_engine.live_data_update import LiveDataUpdater

    expected_date = date.fromisoformat(
        args.expected_latest_market_date
    )
    now = datetime.now(timezone.utc)

    result = LiveDataUpdater(
        price_root=price_root,
        status_path=status_path,
        provider=YahooDailyProvider(),
        source_commit=git_head(),
        lookback_days=args.lookback_days,
    ).update(
        expected_latest_market_date=expected_date
    )

    payload = _promote_ordinary_unavailable_to_current(
        result.to_payload(),
        expected_latest_market_date=expected_date,
        now=now,
    )
    _atomic_write_payload(status_path, payload)

    print(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if payload.get("data_status") == "CURRENT" else 2


if __name__ == "__main__":
    raise SystemExit(main())
