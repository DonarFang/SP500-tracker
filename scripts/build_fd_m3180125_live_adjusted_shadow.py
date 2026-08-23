#!/usr/bin/env python3
"""Build the versioned adjusted Live price store without activating it."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
import hashlib
import json
import os
from pathlib import Path
from typing import Mapping, Sequence

from update_fd_m3180125_live_prices import YahooDailyProvider


LEGACY_ROOT = Path("data/live_prices")
SHADOW_ROOT = Path("data/live_prices_adjusted_v1/live_prices")
EXCLUDED_STOCK_SYMBOLS = frozenset({"QQQ", "SOXX", "VIXY"})
INDEX_PROVIDER_SYMBOLS = {"SPX": "^GSPC", "NDX": "^NDX", "SOX": "^SOX", "VIX": "^VIX"}


def _atomic_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(body)
    os.replace(temporary, path)


def _catalogue(legacy_root: Path) -> tuple[str, ...]:
    symbols = tuple(
        sorted(
            path.stem.upper()
            for path in legacy_root.glob("*.json")
            if path.stem.upper() not in EXCLUDED_STOCK_SYMBOLS
        )
    )
    if not symbols:
        raise RuntimeError("legacy Live catalogue is empty")
    return symbols


def _first_date(path: Path) -> date:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not payload:
        raise RuntimeError(f"missing legacy history: {path}")
    return date.fromisoformat(str(payload[0]["date"]))


def build_adjusted_shadow(
    *, legacy_root: Path, shadow_root: Path, end_date: date, provider: object
) -> dict[str, object]:
    if shadow_root.name != "live_prices" or shadow_root.parent.name != "live_prices_adjusted_v1":
        raise RuntimeError("adjusted shadow root name mismatch")
    symbols = _catalogue(legacy_root)
    hashes: dict[str, str] = {}
    unavailable: list[str] = []
    for symbol in symbols:
        rows: Sequence[Mapping[str, object]] = provider.fetch(
            provider_symbol=INDEX_PROVIDER_SYMBOLS.get(symbol, symbol),
            start_date=_first_date(legacy_root / f"{symbol}.json"),
            end_date=end_date,
        )
        if not rows:
            unavailable.append(symbol)
            continue
        target = shadow_root / f"{symbol}.json"
        _atomic_json(target, list(rows))
        hashes[symbol] = hashlib.sha256(target.read_bytes()).hexdigest()
    if unavailable:
        raise RuntimeError("HOLD_ADJUSTED_SHADOW_UNAVAILABLE: " + ",".join(unavailable))
    return {
        "decision": "PASS_PARITY_STEP_2_ADJUSTED_SHADOW_BUILT",
        "price_mode": "ADJUSTED_SHADOW_NOT_ACTIVE",
        "auto_adjust": True,
        "symbol_count": len(symbols),
        "stock_symbol_count": len(set(symbols) - set(INDEX_PROVIDER_SYMBOLS)),
        "excluded_stock_symbols": sorted(EXCLUDED_STOCK_SYMBOLS),
        "latest_requested_date": end_date.isoformat(),
        "latest_market_date": end_date.isoformat(),
        "data_status": "CURRENT",
        "catalogue_changed": False,
        "unavailable_symbols": [],
        "built_at": datetime.now(timezone.utc).isoformat(),
        "file_hashes": hashes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--legacy-root", type=Path, default=LEGACY_ROOT)
    parser.add_argument("--shadow-root", type=Path, default=SHADOW_ROOT)
    parser.add_argument("--end-date", required=True)
    parser.add_argument(
        "--evidence-path",
        type=Path,
        default=Path(
            "exports/official/FD-M3180125-SP500-TOP3-engine/live/automation/"
            "parity/current_adjusted_shadow.json"
        ),
    )
    args = parser.parse_args()
    result = build_adjusted_shadow(
        legacy_root=args.legacy_root,
        shadow_root=args.shadow_root,
        end_date=date.fromisoformat(args.end_date),
        provider=YahooDailyProvider(auto_adjust=True),
    )
    _atomic_json(args.evidence_path, result)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
