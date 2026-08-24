#!/usr/bin/env python3
"""Atomically rebuild the Forward-owned adjusted price library.

The rebuild downloads an independent Yahoo-adjusted snapshot.  It never reads
the Live adjusted store and it retains outgoing securities only when they are
needed by the canonical Forward membership timeline.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import tempfile

from build_fd_m3180125_live_adjusted_shadow import (
    FetchRequest,
    YahooAdjustedBatchProvider,
    build_adjusted_shadow,
    latest_completed_session,
)
from e1r_engine.live_calendar import load_live_trading_calendar


ROOT = Path(__file__).resolve().parents[1]
PRICE_ROOT = ROOT / "data/fw_prices"
BUILD_ROOT = ROOT / "data/forward_prices_adjusted_v1/fw_prices"
CALENDAR_PATH = ROOT / "config/live_calendar/us_equity_calendar_v1.0.json"
EVIDENCE_PATH = (
    ROOT
    / "exports/official/FD-M3180125-SP500-TOP3-engine/forward/automation"
    / "current_adjusted_rebuild.json"
)
EXCLUDED = {"QQQ", "SOXX", "VIXY", "_GSPC", "_NDX", "_SOX", "_VIX"}
INDEX_ALIASES = {
    "SPX": "_GSPC",
    "NDX": "_NDX",
    "SOX": "_SOX",
    "VIX": "_VIX",
}
PRE_FORWARD_REMOVALS = {"CTRA"}
TIMELINE_ADDITIONS = {"VEEV", "FERG"}
EXPECTED_DAILY_MEMBERSHIP = 491
EXPECTED_TIMELINE_STOCKS = 493
FROZEN_HISTORICAL_END_DATES = {"EA": "2026-08-04"}


def atomic_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def parse_utc(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("--as-of-utc must include a timezone")
    return result.astimezone(timezone.utc)


def source_symbols() -> tuple[str, ...]:
    existing = {
        path.stem.upper()
        for path in PRICE_ROOT.glob("*.json")
        if path.stem.upper() not in EXCLUDED
    }
    stocks = (existing - PRE_FORWARD_REMOVALS) | TIMELINE_ADDITIONS
    stocks -= set(INDEX_ALIASES)
    if len(stocks) != EXPECTED_TIMELINE_STOCKS:
        raise RuntimeError(
            "Forward timeline stock count mismatch: expected=%d actual=%d"
            % (EXPECTED_TIMELINE_STOCKS, len(stocks))
        )
    return tuple(sorted(stocks | set(INDEX_ALIASES)))


def prepare_legacy_aliases(root: Path) -> None:
    root.mkdir(parents=True)
    for path in PRICE_ROOT.glob("*.json"):
        if path.stem.upper() in EXCLUDED:
            continue
        target = root / path.name
        shutil.copy2(path, target)
    for canonical, stored in INDEX_ALIASES.items():
        source = PRICE_ROOT / (stored + ".json")
        if not source.is_file():
            source = PRICE_ROOT / (canonical + ".json")
        if not source.is_file():
            raise RuntimeError("Forward index history missing: " + canonical)
        shutil.copy2(source, root / (canonical + ".json"))


def frozen_historical_rows(path: Path, end_date: str) -> list[dict[str, object]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise RuntimeError("Frozen Forward history is not a list: " + str(path))
    rows = [row for row in payload if str(row.get("date", "")) <= end_date]
    dates = [str(row.get("date", "")) for row in rows]
    if len(rows) < 252 or dates != sorted(set(dates)) or dates[-1] != end_date:
        raise RuntimeError("Frozen Forward history boundary invalid: " + str(path))
    for row in rows:
        try:
            prices = [float(row[name]) for name in ("open", "high", "low", "close")]
            volume = float(row.get("volume", 0.0))
        except (KeyError, TypeError, ValueError) as exc:
            raise RuntimeError("Frozen Forward history row invalid: " + str(path)) from exc
        if any(not math.isfinite(value) or value <= 0 for value in prices):
            raise RuntimeError("Frozen Forward history price invalid: " + str(path))
        if not math.isfinite(volume) or volume < 0:
            raise RuntimeError("Frozen Forward history volume invalid: " + str(path))
    return rows


class ForwardAdjustedProvider:
    """Yahoo provider plus bounded history for delisted outgoing members."""

    def __init__(self, upstream: object, price_root: Path) -> None:
        self.upstream = upstream
        self.price_root = price_root
        self.fallback_evidence: list[dict[str, object]] = []

    def fetch_many(self, requests: list[FetchRequest], *, attempt: int):
        frozen = [
            request for request in requests
            if request.symbol in FROZEN_HISTORICAL_END_DATES
        ]
        regular = [request for request in requests if request not in frozen]
        fetch_many = getattr(self.upstream, "fetch_many")
        results, errors = fetch_many(regular, attempt=attempt)
        for request in frozen:
            path = self.price_root / (request.symbol + ".json")
            end_date = FROZEN_HISTORICAL_END_DATES[request.symbol]
            rows = frozen_historical_rows(path, end_date)
            results[request.symbol] = rows
            errors.pop(request.symbol, None)
            evidence = {
                "symbol": request.symbol,
                "reason": "DELISTED_OUTGOING_MEMBER_PROVIDER_UNAVAILABLE",
                "membership_effective_through": end_date,
                "source": "data/fw_prices/" + request.symbol + ".json",
                "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "row_count": len(rows),
                "first_date": str(rows[0]["date"]),
                "last_date": str(rows[-1]["date"]),
            }
            if evidence not in self.fallback_evidence:
                self.fallback_evidence.append(evidence)
        return results, errors


def promote() -> None:
    backup = PRICE_ROOT.parent / ".fw_prices.previous"
    if backup.exists():
        shutil.rmtree(backup)
    os.replace(PRICE_ROOT, backup)
    try:
        os.replace(BUILD_ROOT, PRICE_ROOT)
    except Exception:
        if not PRICE_ROOT.exists():
            os.replace(backup, PRICE_ROOT)
        raise
    shutil.rmtree(backup)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of-utc", default=datetime.now(timezone.utc).isoformat())
    parser.add_argument("--max-attempts", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=20)
    args = parser.parse_args()
    as_of = parse_utc(args.as_of_utc)
    calendar = load_live_trading_calendar(CALENDAR_PATH)
    target = latest_completed_session(as_of_utc=as_of, calendar=calendar)
    symbols = source_symbols()

    with tempfile.TemporaryDirectory(prefix="fd-forward-adjusted-") as directory:
        legacy = Path(directory) / "legacy"
        prepare_legacy_aliases(legacy)
        provider = ForwardAdjustedProvider(
            YahooAdjustedBatchProvider(batch_size=args.batch_size),
            PRICE_ROOT,
        )
        evidence = build_adjusted_shadow(
            legacy_root=legacy,
            shadow_root=BUILD_ROOT,
            end_date=target,
            provider=provider,
            symbols=symbols,
            max_attempts=args.max_attempts,
            as_of_utc=as_of,
        )

    for canonical, stored in INDEX_ALIASES.items():
        source = BUILD_ROOT / (canonical + ".json")
        os.replace(source, BUILD_ROOT / (stored + ".json"))
    files = sorted(BUILD_ROOT.glob("*.json"))
    if len(files) != EXPECTED_TIMELINE_STOCKS + len(INDEX_ALIASES):
        raise RuntimeError("Forward adjusted staging catalogue mismatch")
    promote()
    result = {
        **evidence,
        "decision": "PASS_FORWARD_ADJUSTED_PRICE_LIBRARY_REBUILT",
        "price_mode": "ADJUSTED_FORWARD_ACTIVE",
        "price_root": "data/fw_prices",
        "live_price_root_read": False,
        "daily_membership_count": EXPECTED_DAILY_MEMBERSHIP,
        "timeline_stock_count": EXPECTED_TIMELINE_STOCKS,
        "total_file_count": len(files),
        "historical_fallbacks": provider.fallback_evidence,
    }
    atomic_json(EVIDENCE_PATH, result)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
