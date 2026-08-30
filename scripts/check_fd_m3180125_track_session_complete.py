#!/usr/bin/env python3
"""Read-only idempotency gate for Forward and Live scheduled retries."""

from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
from typing import Any, Optional


ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = (
    ROOT
    / "exports"
    / "official"
    / "FD-M3180125-SP500-TOP3-engine"
)


def load_object(path: Path) -> Optional[dict[str, Any]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def artifacts_match(manifest_path: Path, files: Any, nested_hash: bool) -> bool:
    if not isinstance(files, dict) or not files:
        return False
    for filename, recorded in files.items():
        if not isinstance(filename, str) or not filename or "/" in filename:
            return False
        expected = recorded.get("sha256") if nested_hash and isinstance(recorded, dict) else recorded
        if not isinstance(expected, str) or len(expected) != 64:
            return False
        artifact = manifest_path.parent / filename
        if not artifact.is_file():
            return False
        if hashlib.sha256(artifact.read_bytes()).hexdigest() != expected:
            return False
    return True


def forward_complete(market_date: str) -> bool:
    manifest_path = (
        ENGINE_ROOT
        / "forward"
        / "runtime"
        / "daily"
        / market_date
        / "manifest.json"
    )
    manifest = load_object(manifest_path)
    return bool(
        manifest
        and manifest.get("artifact_type") == "OFFICIAL_FORWARD_DAILY_COMMIT"
        and manifest.get("date") == market_date
        and manifest.get("last_committed_date") == market_date
        and artifacts_match(manifest_path, manifest.get("artifacts"), True)
    )


def live_complete(market_date: str) -> bool:
    live_root = ENGINE_ROOT / "live"
    manifest_path = live_root / "runtime" / "daily" / market_date / "manifest.json"
    manifest = load_object(manifest_path)
    state = load_object(live_root / "runtime" / "current" / "runtime_state.json")
    status = load_object(
        live_root
        / "automation"
        / "parity"
        / "current_adjusted_accepted.json"
    )
    required_latest = status.get("required_index_latest_dates") if status else None
    indices_current = bool(
        isinstance(required_latest, dict)
        and len(required_latest) == 4
        and all(value == market_date for value in required_latest.values())
    )
    return bool(
        manifest
        and manifest.get("market_date") == market_date
        and manifest.get("validation_status") == "PASS"
        and artifacts_match(manifest_path, manifest.get("files"), False)
        and state
        and state.get("last_committed_market_date") == market_date
        and status
        and status.get("data_status") == "CURRENT"
        and status.get("latest_market_date") == market_date
        and status.get("stale_required_indices") == {}
        and status.get("invalid_ohlc_files") == {}
        and indices_current
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--track", required=True, choices=("forward", "live"))
    parser.add_argument("--market-date", required=True)
    args = parser.parse_args()
    market_date = date.fromisoformat(args.market_date).isoformat()
    complete = (
        forward_complete(market_date)
        if args.track == "forward"
        else live_complete(market_date)
    )
    print("true" if complete else "false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
