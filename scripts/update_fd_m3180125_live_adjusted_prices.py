#!/usr/bin/env python3
"""Incrementally update the accepted, Live-owned adjusted price library.

This is the Live counterpart of update_engine_forward_prices.py.  It keeps
the existing Live catalogue and history, refreshes a bounded overlap with
Yahoo adjusted prices, and publishes only after all four required indices
reach the exact latest completed market session.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import tempfile
import time
from datetime import date, datetime, timedelta, timezone
from typing import Any, Optional

import pandas as pd
import yfinance as yf


ROOT = Path(__file__).resolve().parents[1]
PRICE_ROOT = ROOT / "data" / "live_prices_adjusted_v1" / "live_prices"
STATUS_PATH = (
    ROOT
    / "exports"
    / "official"
    / "FD-M3180125-SP500-TOP3-engine"
    / "live"
    / "automation"
    / "parity"
    / "current_adjusted_accepted.json"
)
INDEX_TICKERS = {
    "SPX": "^GSPC",
    "NDX": "^NDX",
    "SOX": "^SOX",
    "VIX": "^VIX",
}
REQUIRED_INDEX_FILES = tuple(sorted(f"{symbol}.json" for symbol in INDEX_TICKERS))
EXCLUDED_SYMBOLS = frozenset({"QQQ", "SOXX", "VIXY"})
EXPECTED_STOCK_COUNT = 491
EXPECTED_FILE_COUNT = EXPECTED_STOCK_COUNT + len(INDEX_TICKERS)
LOOKBACK_DAYS = 10
BATCH_SIZE = 40
DOWNLOAD_ATTEMPTS = 3
DOWNLOAD_RETRY_SECONDS = (20.0, 60.0)
BATCH_PAUSE_SECONDS = 2.0
DOWNLOAD_EXPECTED_DATE: Optional[str] = None
DOWNLOAD_FRESHNESS_SYMBOLS: frozenset[str] = frozenset()


def atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
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
        raise RuntimeError(f"Invalid or empty Live adjusted price file: {path}")
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
            raise RuntimeError(f"Invalid close in {path} at {trading_date}")
        previous_date = trading_date
    return payload


def yahoo_symbol(path: Path) -> str:
    return INDEX_TICKERS.get(path.stem, path.stem)


def normalize_frame(raw: pd.DataFrame, symbol: str) -> Optional[pd.DataFrame]:
    if raw is None or raw.empty:
        return None
    frame = raw
    if isinstance(raw.columns, pd.MultiIndex):
        level_zero = set(map(str, raw.columns.get_level_values(0)))
        level_one = set(map(str, raw.columns.get_level_values(1)))
        if symbol in level_one:
            frame = raw.xs(symbol, axis=1, level=1, drop_level=True)
        elif symbol in level_zero:
            frame = raw.xs(symbol, axis=1, level=0, drop_level=True)
        else:
            return None
    frame = frame.rename(columns={column: str(column).lower() for column in frame.columns})
    if "close" not in frame.columns:
        return None
    frame = frame.reset_index()
    frame = frame.rename(columns={frame.columns[0]: "date"})
    frame["date"] = frame["date"].astype(str).str[:10]
    frame = frame.dropna(subset=["close"])
    return frame if not frame.empty else None


def frame_contains_date(frame: Optional[pd.DataFrame], trading_date: str) -> bool:
    if frame is None:
        return False
    if not hasattr(frame, "columns"):
        return True
    if "date" not in frame.columns:
        return False
    return trading_date in set(frame["date"].astype(str).str[:10])


def download_bulk(
    symbols: list[str],
    start: str,
    end: str,
) -> dict[str, pd.DataFrame]:
    downloaded: dict[str, pd.DataFrame] = {}
    pending = list(symbols)
    for attempt in range(DOWNLOAD_ATTEMPTS):
        if attempt:
            time.sleep(DOWNLOAD_RETRY_SECONDS[attempt - 1])
        print(
            f"LIVE_PRICE_DOWNLOAD_ATTEMPT={attempt + 1}/"
            f"{DOWNLOAD_ATTEMPTS} SYMBOLS={len(pending)}"
        )
        for offset in range(0, len(pending), BATCH_SIZE):
            batch = pending[offset : offset + BATCH_SIZE]
            raw_index_retry = (
                attempt > 0
                and batch
                and all(symbol in DOWNLOAD_FRESHNESS_SYMBOLS for symbol in batch)
            )
            try:
                if raw_index_retry:
                    raw = yf.download(
                        batch, start=start, end=end, interval="1d",
                        auto_adjust=False, progress=False, threads=False,
                        group_by="column",
                    )
                else:
                    raw = yf.download(
                        batch, start=start, end=end, interval="1d",
                        auto_adjust=True, progress=False, threads=False,
                        group_by="column",
                    )
            except Exception:
                raw = pd.DataFrame()
            for symbol in batch:
                parsed = normalize_frame(raw, symbol)
                if parsed is not None:
                    downloaded[symbol] = parsed
            if offset + BATCH_SIZE < len(pending):
                time.sleep(BATCH_PAUSE_SECONDS)
        pending = [
            symbol
            for symbol in symbols
            if symbol not in downloaded
            or (
                DOWNLOAD_EXPECTED_DATE is not None
                and symbol in DOWNLOAD_FRESHNESS_SYMBOLS
                and not frame_contains_date(
                    downloaded.get(symbol),
                    DOWNLOAD_EXPECTED_DATE,
                )
            )
        ]
        if not pending:
            break
    return downloaded


def download_single(symbol: str, start: str, end: str) -> Optional[pd.DataFrame]:
    try:
        ticker = yf.Ticker(symbol)
        if symbol in INDEX_TICKERS.values():
            raw = ticker.history(
                start=start, end=end, interval="1d", auto_adjust=False
            )
        else:
            raw = ticker.history(
                start=start, end=end, interval="1d", auto_adjust=True
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
    frame: pd.DataFrame, expected_latest_market_date: str
) -> Optional[pd.DataFrame]:
    clipped = frame.loc[frame["date"] <= expected_latest_market_date].copy()
    return clipped if not clipped.empty else None


def merge_records(
    existing: list[dict[str, Any]], frame: pd.DataFrame
) -> list[dict[str, Any]]:
    rows = {str(row["date"]): dict(row) for row in existing}
    for item in frame.itertuples(index=False):
        record = downloaded_record(item)
        if record is None:
            continue
        rows[record["date"]] = record
    return [rows[key] for key in sorted(rows)]


def promote_complete_staging(staging_root: Path, price_root: Path) -> None:
    backup = price_root.parent / f".{price_root.name}.previous"
    if backup.exists():
        shutil.rmtree(backup)
    os.replace(price_root, backup)
    try:
        os.replace(staging_root, price_root)
    except Exception:
        if backup.exists() and not price_root.exists():
            os.replace(backup, price_root)
        raise
    shutil.rmtree(backup)


def main() -> int:
    global DOWNLOAD_EXPECTED_DATE, DOWNLOAD_FRESHNESS_SYMBOLS
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-latest-market-date", required=True)
    args = parser.parse_args()
    expected = date.fromisoformat(args.expected_latest_market_date).isoformat()
    if not PRICE_ROOT.is_dir():
        raise RuntimeError(f"Missing accepted Live adjusted price root: {PRICE_ROOT}")

    price_files = sorted(PRICE_ROOT.glob("*.json"))
    stems = {path.stem for path in price_files}
    stocks = stems - set(INDEX_TICKERS)
    if len(price_files) != EXPECTED_FILE_COUNT or len(stocks) != EXPECTED_STOCK_COUNT:
        raise RuntimeError(
            "Live adjusted catalogue count mismatch: "
            f"expected={EXPECTED_FILE_COUNT} actual={len(price_files)}"
        )
    if set(INDEX_TICKERS) - stems:
        raise RuntimeError("Live adjusted catalogue is missing required indices")
    if stems & EXCLUDED_SYMBOLS:
        raise RuntimeError("Live adjusted catalogue contains excluded ETF symbols")

    existing = {path.name: load_existing(path) for path in price_files}
    symbol_by_file = {path.name: yahoo_symbol(path) for path in price_files}
    file_by_symbol = {symbol: filename for filename, symbol in symbol_by_file.items()}
    if len(file_by_symbol) != len(price_files):
        raise RuntimeError("Duplicate Live Yahoo symbol mapping")

    oldest_latest = min(records[-1]["date"] for records in existing.values())
    start = (date.fromisoformat(oldest_latest) - timedelta(days=LOOKBACK_DAYS)).isoformat()
    end = (date.fromisoformat(expected) + timedelta(days=1)).isoformat()
    symbols = sorted(file_by_symbol)
    required_symbols = set(INDEX_TICKERS.values())
    DOWNLOAD_EXPECTED_DATE = expected
    DOWNLOAD_FRESHNESS_SYMBOLS = frozenset(required_symbols)
    downloaded = download_bulk(symbols, start, end)
    missing_symbols = [symbol for symbol in symbols if symbol not in downloaded]
    stale_required_symbols = [
        symbol
        for symbol in required_symbols
        if not frame_contains_date(downloaded.get(symbol), expected)
    ]
    fallback_symbols = (
        sorted(required_symbols)
        if not downloaded
        else sorted(
            set(missing_symbols) | set(stale_required_symbols),
            key=lambda item: (item not in required_symbols, item),
        )
    )
    if not downloaded:
        print("LIVE_PRICE_GLOBAL_FETCH_FAILURE_REQUIRED_INDEX_PROBE=true")
    for symbol in fallback_symbols:
        if symbol not in downloaded or symbol in stale_required_symbols:
            fallback = download_single(symbol, start, end)
            if fallback is not None and (
                symbol not in required_symbols
                or frame_contains_date(fallback, expected)
            ):
                downloaded[symbol] = fallback

    merged_by_file: dict[str, list[dict[str, Any]]] = {}
    fetch_unavailable: list[str] = []
    latest_dates: dict[str, str] = {}
    for symbol in symbols:
        filename = file_by_symbol[symbol]
        records = existing[filename]
        frame = downloaded.get(symbol)
        if frame is not None:
            frame = clip_frame_to_expected_session(frame, expected)
        if frame is None:
            fetch_unavailable.append(symbol)
            merged = records
        else:
            merged = merge_records(records, frame)
        merged_by_file[filename] = merged
        latest_dates[filename] = str(merged[-1]["date"])

    required_latest = {name: latest_dates[name] for name in REQUIRED_INDEX_FILES}
    stale_required = {
        name: actual for name, actual in required_latest.items() if actual != expected
    }
    ordinary_stale = sorted(
        Path(name).stem
        for name, actual in latest_dates.items()
        if name not in REQUIRED_INDEX_FILES and actual < expected
    )
    changed_files = sorted(
        name for name in merged_by_file if merged_by_file[name] != existing[name]
    )
    invalid_files = {
        filename: dates
        for filename, records in merged_by_file.items()
        if (dates := invalid_ohlc_dates(records))
    }
    if stale_required or invalid_files:
        decision = (
            "HOLD_LIVE_ADJUSTED_INVALID_OHLC"
            if invalid_files
            else "HOLD_LIVE_ADJUSTED_REQUIRED_INDEX_FRESHNESS"
        )
        status = {
            "schema_version": "2.0",
            "decision": decision,
            "data_status": "HOLD",
            "price_mode": "ADJUSTED_ACCEPTED",
            "auto_adjust": True,
            "production_activation": True,
            "catalogue_changed": False,
            "latest_requested_date": expected,
            "latest_market_date": max(latest_dates.values()),
            "required_index_latest_dates": required_latest,
            "stale_required_indices": stale_required,
            "invalid_ohlc_files": invalid_files,
            "fetch_unavailable_symbols": sorted(fetch_unavailable),
            "ordinary_stale_symbols": ordinary_stale,
            "unavailable_symbols": [],
        }
        print(json.dumps(status, ensure_ascii=False, indent=2, sort_keys=True))
        return 2

    staging_root: Optional[Path] = Path(
        tempfile.mkdtemp(prefix=".live-adjusted-incremental-", dir=str(PRICE_ROOT.parent))
    )
    try:
        assert staging_root is not None
        for filename, records in sorted(merged_by_file.items()):
            atomic_write_json(staging_root / filename, records)
        if sorted(path.name for path in staging_root.glob("*.json")) != sorted(existing):
            raise RuntimeError("Live adjusted staging catalogue mismatch")
        promote_complete_staging(staging_root, PRICE_ROOT)
        staging_root = None
    finally:
        if staging_root is not None and staging_root.exists():
            shutil.rmtree(staging_root)

    file_hashes = {
        path.stem: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(PRICE_ROOT.glob("*.json"))
    }
    status = {
        "schema_version": "2.0",
        "decision": "PASS_LIVE_ADJUSTED_DAILY_INCREMENTAL_PRICE_UPDATE",
        "data_status": "CURRENT",
        "price_mode": "ADJUSTED_ACCEPTED",
        "auto_adjust": True,
        "production_activation": True,
        "provider": "Yahoo Finance via yfinance",
        "price_root": "data/live_prices_adjusted_v1/live_prices",
        "catalogue_source": "existing accepted Live adjusted filenames",
        "catalogue_changed": False,
        "symbol_count": len(price_files),
        "stock_symbol_count": len(stocks),
        "index_symbol_count": len(INDEX_TICKERS),
        "excluded_stock_symbols": sorted(EXCLUDED_SYMBOLS),
        "lookback_days": LOOKBACK_DAYS,
        "download_start_date": start,
        "latest_requested_date": expected,
        "latest_market_date": expected,
        "required_index_latest_dates": required_latest,
        "stale_required_indices": {},
        "invalid_ohlc_files": {},
        "changed_file_count": len(changed_files),
        "changed_files": changed_files,
        "fetch_unavailable_symbols": sorted(fetch_unavailable),
        "ordinary_stale_symbols": ordinary_stale,
        "unavailable_symbols": [],
        "symbol_latest_dates": {Path(k).stem: v for k, v in sorted(latest_dates.items())},
        "file_hashes": file_hashes,
        "completed_at": datetime.now(timezone.utc).isoformat(),
    }
    atomic_write_json(STATUS_PATH, status)
    print(json.dumps(status, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
