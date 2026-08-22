#!/usr/bin/env python3
"""Controlled UV-step-4 activation/deactivation; no strategy or market run."""

from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
ENGINE_ID = "FD-M3180125-SP500-TOP3-engine"
CONTRACT = ROOT / "docs/canonical/FD-M3180125_SP500_UNIVERSE_VERSIONING_UV_STEP_4_CONTRACT_v1.0_FROZEN_2026-08-22.md"
EXCLUDED = {
    "SPX", "NDX", "SOX", "VIX", "_GSPC", "_NDX", "_SOX", "_VIX",
    "GSPC", "^GSPC", "^NDX", "^SOX", "^VIX", "QQQ", "SOXX", "VIXY",
}


def load_json(path: Path):
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError("expected JSON object: " + str(path))
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--track", choices=("forward", "live", "both"), default="both")
    parser.add_argument("--mode", choices=("enforce", "off"), default="enforce")
    args = parser.parse_args()
    sys.path.insert(0, str(ROOT / "src"))
    from e1r_engine.live_calendar import load_live_trading_calendar
    from e1r_engine.live_composition import (
        discover_live_eligible_stock_symbols,
        discover_live_stock_symbols,
    )
    from e1r_engine.universe_versioning.production_integration import ProductionUniverseGate

    authority = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    contract_hash = hashlib.sha256(CONTRACT.read_bytes()).hexdigest()
    tracks = ("forward", "live") if args.track == "both" else (args.track,)
    results = []
    for track in tracks:
        gate = ProductionUniverseGate(ROOT, track)
        if args.mode == "off":
            gate.deactivate(authority_head=authority, contract_hash=contract_hash)
            results.append({"track": track, "mode": "OFF", "decision": "PASS_UV_STEP_4_TRACK_DEACTIVATED"})
            continue
        if track == "forward":
            price_paths = {
                path.stem.upper(): path
                for path in (ROOT / "data/fw_prices").glob("*.json")
                if path.stem.upper() not in EXCLUDED
            }
            catalogue = tuple(sorted(price_paths))
            runtime = load_json(ROOT / "exports/official" / ENGINE_ID / "forward/runtime/current/runtime_state.json")
            execution_date = str(runtime["last_committed_date"])
            positions = runtime.get("account", {}).get("positions", {})
            if not isinstance(positions, dict):
                raise RuntimeError("HOLD_UV_STEP_4_FORWARD_PRODUCTION: positions must be an object")
            from e1r_engine.forward_runtime import ForwardMarketDataAdapter
            ready = tuple(
                symbol for symbol in catalogue
                if execution_date in ForwardMarketDataAdapter.parse_price_file(
                    price_paths[symbol]
                )
            )
            indices = ("SPX", "NDX", "SOX")
        else:
            catalogue = discover_live_stock_symbols(
                price_root=ROOT / "data/live_prices", expected_stock_count=494,
            )
            status = load_json(ROOT / "exports/official" / ENGINE_ID / "live/automation/current_data_update.json")
            market_date = date.fromisoformat(str(status["latest_market_date"]))
            execution_date = load_live_trading_calendar(
                ROOT / "config/live_calendar/us_equity_calendar_v1.0.json"
            ).next_session(market_date).isoformat()
            eligible, _ = discover_live_eligible_stock_symbols(
                price_root=ROOT / "data/live_prices",
                market_date=market_date,
                catalogue_stock_symbols=catalogue,
            )
            account_path = ROOT / "exports/official" / ENGINE_ID / "live/runtime/current/account_state.json"
            account = load_json(account_path) if account_path.is_file() else {"positions": {}}
            positions = account.get("positions", {})
            if not isinstance(positions, dict):
                raise RuntimeError("HOLD_UV_STEP_4_LIVE_PRODUCTION: positions must be an object")
            ready = eligible
            indices = ("SPX", "NDX", "SOX", "VIX")
        gate.activate(
            expected_execution_date=execution_date,
            baseline_membership=catalogue,
            authority_head=authority,
            contract_hash=contract_hash,
        )
        decision = gate.resolve(
            expected_execution_date=execution_date,
            production_catalogue=catalogue,
            production_eligible=ready,
            holdings_symbols=positions.keys(),
            data_ready_symbols=ready,
            required_indices=indices,
        )
        results.append({
            "track": track, "mode": "ENFORCE", "decision": "PASS_UV_STEP_4_TRACK_ACTIVATED",
            "expected_execution_date": execution_date, "snapshot_id": decision.snapshot_id,
            "snapshot_hash": decision.snapshot_hash, "eligible_count": len(decision.eligible_buy_universe),
            "evidence_hash": decision.evidence_hash,
        })
    print(json.dumps({
        "decision": "PASS_UV_STEP_4_PRODUCTION_MODE_UPDATED",
        "authority_head": authority, "contract_hash": contract_hash,
        "results": results, "strategy_modified": False, "production_run_performed": False,
        "price_update_performed": False, "commit_or_push_performed": False,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
