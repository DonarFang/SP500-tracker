#!/usr/bin/env python3
"""
E1R v0.2 OOS runner with KICKOFF_READY paper-state preservation guard.

This wrapper protects accepted E1R paper orders / positions created by
Stage 3.8E-2F-1E-4.

The previous implementation is kept in:
scripts/run_e1r_v0_2_oos_core.py

Guard behavior:
- Let the core script run so it can refresh status/sidecar/lifecycle outputs.
- If accepted paper orders/positions existed before the run and E1R is still
  KICKOFF_READY with no official_kickoff_date, restore official paper
  orders/positions and summary/state kickoff semantics afterward.
"""

from __future__ import annotations

import json
import runpy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
CORE_SCRIPT = ROOT / "scripts" / "run_e1r_v0_2_oos_core.py"

ORDERS = ROOT / "exports" / "oos_e1r_v0_2_orders.json"
POSITIONS = ROOT / "exports" / "oos_e1r_v0_2_positions.json"
SUMMARY = ROOT / "exports" / "oos_e1r_v0_2_summary.json"
STATE = ROOT / "data" / "oos" / "e1r_v0_2_portfolio_state.json"

STRATEGY_ID = "E1R_REGIME_AWARE_V0_2"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def to_float(v: Any, default: float = 0.0) -> float:
    try:
        if v is None or v == "":
            return default
        return float(v)
    except Exception:
        return default


def get_orders(doc: Any) -> List[Dict[str, Any]]:
    if isinstance(doc, dict) and isinstance(doc.get("orders"), list):
        return [x for x in doc["orders"] if isinstance(x, dict)]
    if isinstance(doc, list):
        return [x for x in doc if isinstance(x, dict)]
    return []


def get_positions(doc: Any) -> List[Dict[str, Any]]:
    if isinstance(doc, dict) and isinstance(doc.get("positions"), list):
        return [x for x in doc["positions"] if isinstance(x, dict)]
    if isinstance(doc, list):
        return [x for x in doc if isinstance(x, dict)]
    return []


def snapshot() -> Dict[str, Any]:
    return {
        "orders_doc": read_json(ORDERS, {}),
        "positions_doc": read_json(POSITIONS, {}),
        "summary": read_json(SUMMARY, {}),
        "state": read_json(STATE, {}),
    }


def should_preserve(before: Dict[str, Any]) -> bool:
    summary = before["summary"]
    state = before["state"]
    orders = get_orders(before["orders_doc"])
    positions = get_positions(before["positions_doc"])

    if not isinstance(summary, dict) or not isinstance(state, dict):
        return False

    return (
        summary.get("strategy_id") == STRATEGY_ID
        and summary.get("tracking_status") == "KICKOFF_READY"
        and summary.get("official_kickoff_date") is None
        and state.get("official_kickoff_date") is None
        and len(orders) > 0
        and len(positions) > 0
    )


def restore_paper_state(before: Dict[str, Any]) -> Dict[str, Any]:
    before_orders_doc = before["orders_doc"]
    before_positions_doc = before["positions_doc"]
    before_summary = before["summary"] if isinstance(before["summary"], dict) else {}
    before_state = before["state"] if isinstance(before["state"], dict) else {}

    after_summary = read_json(SUMMARY, {})
    after_state = read_json(STATE, {})

    if not isinstance(after_summary, dict):
        after_summary = {}
    if not isinstance(after_state, dict):
        after_state = {}

    orders = get_orders(before_orders_doc)
    positions = get_positions(before_positions_doc)

    position_weight_sum = sum(to_float(p.get("weight")) for p in positions)
    portfolio_value = to_float(
        before_summary.get("portfolio_value")
        or before_state.get("portfolio_value")
        or after_summary.get("portfolio_value"),
        100000.0,
    )
    market_value = portfolio_value * position_weight_sum
    cash = portfolio_value - market_value

    # Restore official paper exports exactly.
    write_json(ORDERS, before_orders_doc)
    write_json(POSITIONS, before_positions_doc)

    # Merge non-paper fields from the core output, but preserve paper-state semantics.
    preserved_summary = {
        **after_summary,
        "strategy_id": STRATEGY_ID,
        "tracking_status": "KICKOFF_READY",
        "official_kickoff_date": None,
        "forward_start_date": None,
        "execution_status": before_summary.get("execution_status", "PAPER_POSITIONS_READY_KICKOFF_PENDING"),
        "open_positions_count": len(positions),
        "paper_orders_count": len(orders),
        "executed_orders_count": before_summary.get("executed_orders_count", 0),
        "number_of_trades": before_summary.get("number_of_trades", 0),
        "gross_exposure": position_weight_sum,
        "net_exposure": position_weight_sum,
        "core_exposure": before_summary.get("core_exposure", position_weight_sum),
        "sidecar_exposure": before_summary.get("sidecar_exposure", 0.0),
        "cash": cash,
        "market_value": market_value,
        "portfolio_value": portfolio_value,
        "equity": portfolio_value,
        "preservation_guard": {
            "active": True,
            "guarded_script": "scripts/run_e1r_v0_2_oos.py",
            "core_script": str(CORE_SCRIPT.relative_to(ROOT)),
            "reason": "Preserve accepted paper orders/positions before LIVE_FORWARD.",
            "preserved_at": now_iso(),
        },
    }

    notes = preserved_summary.get("notes")
    if not isinstance(notes, list):
        notes = []
    notes.append("Stage 3.8E-2F-1F-1E preservation guard restored accepted paper orders/positions after E1R OOS runner.")
    preserved_summary["notes"] = notes

    preserved_state = {
        **after_state,
        "strategy_id": STRATEGY_ID,
        "tracking_status": "KICKOFF_READY",
        "official_kickoff_date": None,
        "forward_start_date": None,
        "execution_status": preserved_summary["execution_status"],
        "positions": positions,
        "cash": cash,
        "market_value": market_value,
        "portfolio_value": portfolio_value,
        "equity": portfolio_value,
        "last_summary": preserved_summary,
        "updated_at": now_iso(),
        "preservation_guard": preserved_summary["preservation_guard"],
    }

    write_json(SUMMARY, preserved_summary)
    write_json(STATE, preserved_state)

    return {
        "orders_count": len(orders),
        "positions_count": len(positions),
        "buy_orders": sum(1 for o in orders if o.get("action") == "BUY"),
        "position_weight_sum": position_weight_sum,
        "tracking_status": preserved_summary.get("tracking_status"),
        "official_kickoff_date": preserved_summary.get("official_kickoff_date"),
        "execution_status": preserved_summary.get("execution_status"),
    }


def main() -> int:
    if not CORE_SCRIPT.exists():
        raise SystemExit(f"missing core script: {CORE_SCRIPT}")

    before = snapshot()
    preserve = should_preserve(before)

    try:
        runpy.run_path(str(CORE_SCRIPT), run_name="__main__")
    except SystemExit as exc:
        code = exc.code
        if code not in (0, None):
            raise

    if preserve:
        result = restore_paper_state(before)
        print("E1R OOS runner preservation guard applied")
        print("orders_count:", result["orders_count"])
        print("positions_count:", result["positions_count"])
        print("buy_orders:", result["buy_orders"])
        print("position_weight_sum:", result["position_weight_sum"])
        print("tracking_status:", result["tracking_status"])
        print("official_kickoff_date:", result["official_kickoff_date"])
        print("execution_status:", result["execution_status"])
    else:
        print("E1R OOS runner preservation guard not active")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
