#!/usr/bin/env python3
"""Run the approved Parity-step-3 read-only replay and daily comparator."""

from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import tempfile

from e1r_engine.live_calendar import load_live_trading_calendar
from e1r_engine.live_composition import compose_active_live_production
from e1r_engine.parity_step3_replay import (
    FORBIDDEN_STOCK_SYMBOLS,
    build_causal_live_projection,
    compare_contract,
    load_json,
    normalize_forward,
    normalize_live,
    protected_hashes,
    validate_actions,
)

ENGINE_ROOT = Path("exports/official/FD-M3180125-SP500-TOP3-engine")
LIVE_ROOT = ENGINE_ROOT / "live"
FORWARD_DAILY = ENGINE_ROOT / "forward/runtime/daily"
ADJUSTED_ROOT = Path("data/live_prices_adjusted_v1/live_prices")
CALENDAR = Path("config/live_calendar/us_equity_calendar_v1.0.json")
OUTPUT = LIVE_ROOT / "automation/parity/step_3/current_replay.json"


def _dates(start: date, end: date) -> list[date]:
    available = []
    for path in sorted(FORWARD_DAILY.iterdir()):
        if path.is_dir():
            candidate = date.fromisoformat(path.name)
            if start <= candidate <= end and (LIVE_ROOT / "runtime/daily" / path.name).is_dir():
                available.append(candidate)
    return available


def _status(path: Path, market_date: date) -> None:
    path.write_text(json.dumps({"data_status": "CURRENT", "latest_market_date": market_date.isoformat(), "catalogue_changed": False, "unavailable_symbols": []}), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2026-08-13")
    parser.add_argument("--end")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if not ADJUSTED_ROOT.is_dir():
        raise RuntimeError("HOLD_PARITY_STEP_3: adjusted shadow price root missing")
    shadow = load_json(LIVE_ROOT / "automation/parity/current_adjusted_shadow.json")
    if shadow.get("auto_adjust") is not True or shadow.get("price_mode") != "ADJUSTED_SHADOW_NOT_ACTIVE":
        raise RuntimeError("HOLD_PARITY_STEP_3: adjusted source evidence invalid")
    end = date.fromisoformat(args.end or str(shadow["latest_market_date"]))
    days = _dates(date.fromisoformat(args.start), end)
    if not days:
        raise RuntimeError("HOLD_PARITY_STEP_3: no common replay dates")
    before = protected_hashes(LIVE_ROOT)
    calendar = load_live_trading_calendar(CALENDAR)
    rows = []
    for market_date in days:
        with tempfile.TemporaryDirectory(prefix="fd_m3180125_parity_step3_") as directory:
            temp_live = Path(directory) / "live"
            counts = build_causal_live_projection(LIVE_ROOT, temp_live, market_date)
            status_path = Path(directory) / "status.json"
            _status(status_path, market_date)
            composition = compose_active_live_production(
                price_root=ADJUSTED_ROOT,
                live_root=temp_live,
                data_status_path=status_path,
                market_date=market_date,
                expected_execution_date=calendar.next_session(market_date),
                expected_stock_count=491,
                min_bars=120,
            )
            if FORBIDDEN_STOCK_SYMBOLS.intersection(composition.catalogue_stock_symbols):
                raise RuntimeError("HOLD_PARITY_STEP_3: forbidden ETF leaked into stock universe")
            result = composition.runtime.dry_run(market_date=market_date, market_data=composition.market_data)
            adjusted = result.to_payload()
            forward = normalize_forward(load_json(FORWARD_DAILY / market_date.isoformat() / "decision_trace.json"))
            legacy = load_json(LIVE_ROOT / "runtime/daily" / market_date.isoformat() / "market_status.json")
            contract = compare_contract(normalize_live(adjusted), forward)
            action_errors = validate_actions(adjusted)
            rows.append({
                "market_date": market_date.isoformat(),
                "causal_ledger": counts,
                "adjusted_live": normalize_live(adjusted),
                "formal_forward": forward,
                "legacy_live": legacy,
                "contract_comparison": contract,
                "action_contract_errors": action_errors,
                "legacy_to_adjusted_changed": normalize_live(adjusted) != {"regime": legacy.get("regime"), "regime_subclass": legacy.get("subclass"), "market_state": legacy.get("market_state"), "market_gate": legacy.get("market_gate"), "entry_capacity": legacy.get("entry_capacity"), "strategy_branch": legacy.get("strategy_branch"), "reference_top3": [x.get("symbol") for x in load_json(LIVE_ROOT / "runtime/daily" / market_date.isoformat() / "reference_top3.json").get("top3", [])]},
            })
    after = protected_hashes(LIVE_ROOT)
    protected = before == after
    failures = sum(row["contract_comparison"]["decision"] != "PASS" or bool(row["action_contract_errors"]) for row in rows)
    payload = {
        "decision": "PASS_PARITY_STEP_3_READ_ONLY_REPLAY" if protected and failures == 0 else "HOLD_PARITY_STEP_3",
        "classification": "DIAGNOSTIC_ONLY_NOT_EXECUTION_APPROVED",
        "start_date": days[0].isoformat(), "end_date": days[-1].isoformat(), "date_count": len(days),
        "adjusted_price_mode": "YAHOO_AUTO_ADJUST_TRUE_SHADOW",
        "five_year_mutated": False, "forward_mutated": False, "live_history_mutated": False,
        "active_live_invoked": False, "broker_api_connected": False, "automatic_execution_enabled": False,
        "buy_add_manual_pause_remains": True, "reduce_manual_verification_remains": True,
        "protected_hashes_before": before, "protected_hashes_after": after, "protected_hashes_unchanged": protected,
        "contract_failure_count": failures, "activation_eligible": protected and failures == 0,
        "rows": rows,
    }
    payload["evidence_hash"] = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["decision"].startswith("PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
