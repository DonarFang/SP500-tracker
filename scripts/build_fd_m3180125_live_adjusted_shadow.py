#!/usr/bin/env python3
"""Build the versioned adjusted Live price store without activating it."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import time
from typing import Mapping, Optional, Sequence

from update_fd_m3180125_live_prices import YahooDailyProvider


LEGACY_ROOT = Path("data/live_prices")
SHADOW_ROOT = Path("data/live_prices_adjusted_v1/live_prices")
EXCLUDED_STOCK_SYMBOLS = frozenset({"QQQ", "SOXX", "VIXY"})
INDEX_PROVIDER_SYMBOLS = {"SPX": "^GSPC", "NDX": "^NDX", "SOX": "^SOX", "VIX": "^VIX"}
LIVE_UNIVERSE_STATE = Path("data/live_universe/state/current.json")
LIVE_UNIVERSE_SNAPSHOTS = Path("data/live_universe/snapshots")
EXPECTED_STOCK_COUNT = 491


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


def _production_catalogue(
    *, legacy_root: Path, state_path: Path, snapshot_root: Path
) -> tuple[str, ...]:
    state = json.loads(state_path.read_text(encoding="utf-8"))
    snapshot_id = str(state.get("snapshot_id", ""))
    if not snapshot_id:
        raise RuntimeError("Live Universe current snapshot_id missing")
    snapshot = json.loads(
        (snapshot_root / f"{snapshot_id}.json").read_text(encoding="utf-8")
    )
    if snapshot.get("snapshot_id") != snapshot_id:
        raise RuntimeError("Live Universe snapshot identity mismatch")
    if snapshot.get("track") != "live" or snapshot.get("status") != "EFFECTIVE":
        raise RuntimeError("Live Universe snapshot is not effective")
    membership = snapshot.get("effective_membership")
    if not isinstance(membership, list) or not all(
        isinstance(symbol, str) and symbol for symbol in membership
    ):
        raise RuntimeError("Live Universe effective_membership invalid")
    stocks = sorted(set(membership) - set(EXCLUDED_STOCK_SYMBOLS))
    if len(stocks) != EXPECTED_STOCK_COUNT:
        raise RuntimeError(
            "Live adjusted shadow stock count mismatch: "
            f"expected={EXPECTED_STOCK_COUNT}, actual={len(stocks)}"
        )
    required = tuple(sorted(set(stocks) | set(INDEX_PROVIDER_SYMBOLS)))
    missing = [
        symbol for symbol in required if not (legacy_root / f"{symbol}.json").is_file()
    ]
    if missing:
        raise RuntimeError("Live adjusted shadow legacy inputs missing: " + ",".join(missing))
    return required


def _first_date(path: Path) -> date:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not payload:
        raise RuntimeError(f"missing legacy history: {path}")
    return date.fromisoformat(str(payload[0]["date"]))


def build_adjusted_shadow(
    *,
    legacy_root: Path,
    shadow_root: Path,
    end_date: date,
    provider: object,
    symbols: Optional[Sequence[str]] = None,
    max_attempts: int = 5,
    retry_delay_seconds: float = 15.0,
) -> dict[str, object]:
    if shadow_root.name != "live_prices" or shadow_root.parent.name != "live_prices_adjusted_v1":
        raise RuntimeError("adjusted shadow root name mismatch")
    catalogue = tuple(symbols) if symbols is not None else _catalogue(legacy_root)
    if max_attempts < 1:
        raise ValueError("max_attempts must be positive")
    hashes: dict[str, str] = {}
    pending = list(catalogue)
    for attempt in range(1, max_attempts + 1):
        unavailable: list[str] = []
        for symbol in pending:
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
        pending = unavailable
        if not pending:
            break
        if attempt < max_attempts and retry_delay_seconds > 0:
            time.sleep(retry_delay_seconds * attempt)
    if pending:
        raise RuntimeError("HOLD_ADJUSTED_SHADOW_UNAVAILABLE: " + ",".join(pending))
    return {
        "decision": "PASS_PARITY_STEP_2_ADJUSTED_SHADOW_BUILT",
        "price_mode": "ADJUSTED_SHADOW_NOT_ACTIVE",
        "auto_adjust": True,
        "symbol_count": len(catalogue),
        "stock_symbol_count": len(set(catalogue) - set(INDEX_PROVIDER_SYMBOLS)),
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
    symbols = _production_catalogue(
        legacy_root=args.legacy_root,
        state_path=LIVE_UNIVERSE_STATE,
        snapshot_root=LIVE_UNIVERSE_SNAPSHOTS,
    )
    result = build_adjusted_shadow(
        legacy_root=args.legacy_root,
        shadow_root=args.shadow_root,
        end_date=date.fromisoformat(args.end_date),
        provider=YahooDailyProvider(auto_adjust=True),
        symbols=symbols,
    )
    _atomic_json(args.evidence_path, result)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
