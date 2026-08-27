#!/usr/bin/env python3
# Incrementally update the existing Engine Forward price library.
# Discovers symbols only from the Engine-owned price directory,
# updates only matching files, and never changes the symbol catalogue.

from __future__ import annotations

import argparse
import json
import math
import os
import tempfile
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
PRICE_ROOT = ROOT / "data" / "fw_prices"
STATUS_PATH = (
    ROOT
    / "exports"
    / "official"
    / "FD-M3180125-SP500-TOP3-engine"
    / "forward"
    / "automation"
    / "current_data_update.json"
)

INDEX_TICKERS = {
    "_GSPC": "^GSPC",
    "_NDX": "^NDX",
    "_SOX": "^SOX",
    "_VIX": "^VIX",
}
REQUIRED_INDEX_FILES = tuple(sorted(f"{symbol}.json" for symbol in INDEX_TICKERS))
LOOKBACK_DAYS = 10
BATCH_SIZE = 60


def atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def load_existing(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not payload:
        raise RuntimeError(f"Invalid or empty Engine price file: {path}")

    previous_date = ""
    for row in payload:
        trading_date = row.get("date")
        close = row.get("close")
        if (
            not isinstance(trading_date, str)
            or len(trading_date) != 10
            or trading_date <= previous_date
        ):
            raise RuntimeError(f"Invalid date sequence in {path}")
        if (
            not isinstance(close, (int, float))
            or not math.isfinite(float(close))
            or float(close) <= 0
        ):
            raise RuntimeError(
                f"Invalid close in {path} at {trading_date}"
            )
        previous_date = trading_date
    return payload


def yahoo_symbol(path: Path) -> str:
    return INDEX_TICKERS.get(path.stem, path.stem)


def normalize_frame(
    raw: pd.DataFrame,
    symbol: str,
) -> Optional[pd.DataFrame]:
    if raw is None or raw.empty:
        return None

    frame = raw
    if isinstance(raw.columns, pd.MultiIndex):
        level_zero = set(map(str, raw.columns.get_level_values(0)))
        level_one = set(map(str, raw.columns.get_level_values(1)))

        if symbol in level_one:
            frame = raw.xs(
                symbol,
                axis=1,
                level=1,
                drop_level=True,
            )
        elif symbol in level_zero:
            frame = raw.xs(
                symbol,
                axis=1,
                level=0,
                drop_level=True,
            )
        else:
            return None

    frame = frame.rename(
        columns={
            column: str(column).lower()
            for column in frame.columns
        }
    )
    if "close" not in frame.columns:
        return None

    frame = frame.reset_index()
    frame = frame.rename(columns={frame.columns[0]: "date"})
    frame["date"] = frame["date"].astype(str).str[:10]
    frame = frame.dropna(subset=["close"])
    return frame if not frame.empty else None


def download_bulk(
    symbols: list[str],
    start: str,
    end: str,
) -> dict[str, pd.DataFrame]:
    downloaded: dict[str, pd.DataFrame] = {}

    for offset in range(0, len(symbols), BATCH_SIZE):
        batch = symbols[offset : offset + BATCH_SIZE]
        try:
            raw = yf.download(
                batch,
                start=start,
                end=end,
                interval="1d",
                auto_adjust=True,
                progress=False,
                threads=True,
                group_by="column",
            )
        except Exception:
            raw = pd.DataFrame()

        for symbol in batch:
            parsed = normalize_frame(raw, symbol)
            if parsed is not None:
                downloaded[symbol] = parsed

        if offset + BATCH_SIZE < len(symbols):
            time.sleep(1.0)

    return downloaded


def download_single(
    symbol: str,
    start: str,
    end: str,
) -> Optional[pd.DataFrame]:
    try:
        raw = yf.Ticker(symbol).history(
            start=start,
            end=end,
            interval="1d",
            auto_adjust=True,
        )
    except Exception:
        return None
    return normalize_frame(raw, symbol)


def numeric(row: Any, field: str, default: float = 0.0) -> float:
    value = getattr(row, field, default)
    if value is None or pd.isna(value):
        value = default
    return round(float(value), 6)


def valid_ohlc_record(row: dict[str, Any]) -> bool:
    values: dict[str, float] = {}
    for field in ("open", "high", "low", "close"):
        value = row.get(field)
        if (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not math.isfinite(float(value))
            or float(value) <= 0
        ):
            return False
        values[field] = float(value)

    tolerance = max(values.values()) * 1e-12
    return (
        values["low"] <= min(values["open"], values["close"]) + tolerance
        and values["high"] + tolerance
        >= max(values["open"], values["close"])
        and values["low"] <= values["high"] + tolerance
    )


def downloaded_record(item: Any) -> Optional[dict[str, Any]]:
    trading_date = str(item.date)[:10]
    record = {
        "date": trading_date,
        "open": numeric(item, "open"),
        "high": numeric(item, "high"),
        "low": numeric(item, "low"),
        "close": numeric(item, "close"),
        "volume": round(numeric(item, "volume"), 0),
    }
    return record if valid_ohlc_record(record) else None


def invalid_ohlc_dates(records: list[dict[str, Any]]) -> list[str]:
    return [
        str(row.get("date", "UNKNOWN"))
        for row in records
        if not valid_ohlc_record(row)
    ]


def clip_frame_to_expected_session(
    frame: pd.DataFrame,
    expected_latest_market_date: str,
) -> Optional[pd.DataFrame]:
    """Exclude provider rows for an incomplete or future market session."""
    clipped = frame.loc[
        frame["date"] <= expected_latest_market_date
    ].copy()
    return clipped if not clipped.empty else None


def merge_records(
    existing: list[dict[str, Any]],
    frame: pd.DataFrame,
) -> list[dict[str, Any]]:
    rows = {
        str(row["date"]): dict(row)
        for row in existing
    }

    for item in frame.itertuples(index=False):
        record = downloaded_record(item)
        if record is None:
            continue
        rows[record["date"]] = record

    return [rows[key] for key in sorted(rows)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--expected-latest-market-date",
        required=True,
        help="Latest completed US equity session; required fail-closed freshness gate.",
    )
    args = parser.parse_args()
    expected_latest_market_date = date.fromisoformat(
        args.expected_latest_market_date
    ).isoformat()
    if not PRICE_ROOT.is_dir():
        raise RuntimeError(f"Missing Engine price root: {PRICE_ROOT}")

    price_files = sorted(PRICE_ROOT.glob("*.json"))
    if not price_files:
        raise RuntimeError("No existing Engine Forward price files")

    existing = {
        path.name: load_existing(path)
        for path in price_files
    }
    symbol_by_file = {
        path.name: yahoo_symbol(path)
        for path in price_files
    }
    file_by_symbol = {
        symbol: filename
        for filename, symbol in symbol_by_file.items()
    }

    if len(file_by_symbol) != len(price_files):
        raise RuntimeError("Duplicate Yahoo symbol mapping")

    oldest_latest = min(
        records[-1]["date"]
        for records in existing.values()
    )
    start = (
        date.fromisoformat(oldest_latest)
        - timedelta(days=LOOKBACK_DAYS)
    ).isoformat()
    end = (
        datetime.now(timezone.utc).date()
        + timedelta(days=1)
    ).isoformat()

    symbols = sorted(file_by_symbol)
    downloaded = download_bulk(symbols, start, end)

    for symbol in symbols:
        if symbol in downloaded:
            continue
        fallback = download_single(symbol, start, end)
        if fallback is not None:
            downloaded[symbol] = fallback

    merged_by_file: dict[str, list[dict[str, Any]]] = {}
    unavailable_symbols: list[str] = []
    latest_dates: dict[str, str] = {}

    for symbol in symbols:
        filename = file_by_symbol[symbol]
        old_records = existing[filename]
        frame = downloaded.get(symbol)

        if frame is not None:
            frame = clip_frame_to_expected_session(
                frame,
                expected_latest_market_date,
            )

        if frame is None:
            unavailable_symbols.append(symbol)
            merged = old_records
        else:
            merged = merge_records(old_records, frame)
        merged_by_file[filename] = merged
        latest_dates[filename] = merged[-1]["date"]

    invalid_files = {
        filename: dates
        for filename, records in merged_by_file.items()
        if (dates := invalid_ohlc_dates(records))
    }

    required_index_latest_dates = {
        filename: latest_dates.get(filename)
        for filename in REQUIRED_INDEX_FILES
    }
    stale_required_indices = {
        filename: actual
        for filename, actual in required_index_latest_dates.items()
        if actual != expected_latest_market_date
    }
    if invalid_files:
        decision = "HOLD_ENGINE_FORWARD_INVALID_OHLC"
    elif stale_required_indices:
        decision = "HOLD_ENGINE_FORWARD_REQUIRED_INDEX_FRESHNESS"
    else:
        decision = "PASS_ENGINE_FORWARD_DAILY_INCREMENTAL_PRICE_UPDATE"

    changed_files = sorted(
        filename
        for filename, records in merged_by_file.items()
        if records != existing[filename]
    )
    unchanged_files = sorted(set(existing) - set(changed_files))
    status = {
        "schema_version": "1.0",
        "engine_id": "FD-M3180125-SP500-TOP3-engine",
        "decision": decision,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "provider": "Yahoo Finance via yfinance",
        "price_root": "data/fw_prices",
        "catalogue_source": "existing data/fw_prices filenames",
        "catalogue_changed": False,
        "legacy_price_root_read": False,
        "legacy_price_root_written": False,
        "existing_file_count": len(price_files),
        "downloaded_symbol_count": len(downloaded),
        "changed_file_count": len(changed_files),
        "unchanged_file_count": len(unchanged_files),
        "unavailable_symbol_count": len(unavailable_symbols),
        "unavailable_symbols": unavailable_symbols,
        "changed_files": changed_files,
        "expected_latest_market_date": expected_latest_market_date,
        "required_index_latest_dates": required_index_latest_dates,
        "stale_required_indices": stale_required_indices,
        "invalid_ohlc_files": invalid_files,
        "latest_date_min": min(latest_dates.values()),
        "latest_date_max": max(latest_dates.values()),
    }
    if invalid_files or stale_required_indices:
        atomic_write_json(STATUS_PATH, status)
        print(json.dumps(status, ensure_ascii=False, indent=2))
        return 2

    for filename in changed_files:
        atomic_write_json(PRICE_ROOT / filename, merged_by_file[filename])
    atomic_write_json(STATUS_PATH, status)
    print(json.dumps(status, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
