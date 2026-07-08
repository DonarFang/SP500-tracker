#!/usr/bin/env python3
"""
Stage 3.8E-2F-1E-3
E1R v0.2 orders / positions preview from target weights.

Preview only:
- Does not change LIVE_FORWARD status.
- Does not set official_kickoff_date.
- Does not touch E1 state/export.
- Does not overwrite official E1R orders/positions exports.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = ROOT / "exports"
STATE_DIR = ROOT / "data" / "oos"

TARGETS_PATH = EXPORT_DIR / "oos_e1r_v0_2_targets.json"
SUMMARY_PATH = EXPORT_DIR / "oos_e1r_v0_2_summary.json"
STATE_PATH = STATE_DIR / "e1r_v0_2_portfolio_state.json"

ORDERS_PREVIEW_PATH = EXPORT_DIR / "oos_e1r_v0_2_orders_preview.json"
POSITIONS_PREVIEW_PATH = EXPORT_DIR / "oos_e1r_v0_2_positions_preview.json"

STRATEGY_ID = "E1R_REGIME_AWARE_V0_2"
VERSION = "v0.2"


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


def normalize_positions(raw_positions: Any) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    if not isinstance(raw_positions, list):
        return out

    for row in raw_positions:
        if not isinstance(row, dict):
            continue
        sym = str(row.get("symbol") or "").strip().upper()
        if not sym:
            continue
        out[sym] = {
            **row,
            "symbol": sym,
            "weight": to_float(row.get("weight") or row.get("target_weight"), 0.0),
        }
    return out


def build_preview() -> Dict[str, Any]:
    targets_doc = read_json(TARGETS_PATH, {})
    summary = read_json(SUMMARY_PATH, {})
    state = read_json(STATE_PATH, {})

    if targets_doc.get("strategy_id") != STRATEGY_ID:
        raise SystemExit("targets strategy_id mismatch or missing")

    status_date = targets_doc.get("status_date") or summary.get("status_date")
    tracking_status = summary.get("tracking_status") or targets_doc.get("tracking_status")

    if tracking_status != "KICKOFF_READY":
        raise SystemExit(f"expected KICKOFF_READY preview status, got {tracking_status}")

    if summary.get("official_kickoff_date") is not None:
        raise SystemExit("official_kickoff_date must remain null during preview")

    targets = targets_doc.get("targets") or []
    if not isinstance(targets, list) or not targets:
        raise SystemExit("targets list missing or empty")

    previous_positions = normalize_positions(state.get("positions") or [])
    portfolio_value = to_float(summary.get("portfolio_value") or state.get("portfolio_value"), 100000.0)

    orders: List[Dict[str, Any]] = []
    positions: List[Dict[str, Any]] = []

    target_symbols = set()

    for rank, target in enumerate(targets, start=1):
        if not isinstance(target, dict):
            continue

        symbol = str(target.get("symbol") or "").strip().upper()
        if not symbol:
            continue

        target_symbols.add(symbol)

        target_weight = to_float(target.get("target_weight"), 0.0)
        previous = previous_positions.get(symbol, {})
        previous_weight = to_float(previous.get("weight"), 0.0)

        delta_weight = target_weight - previous_weight

        if abs(delta_weight) < 1e-12:
            action = "HOLD"
        elif previous_weight == 0 and target_weight > 0:
            action = "BUY"
        elif target_weight == 0 and previous_weight > 0:
            action = "EXIT"
        elif delta_weight > 0:
            action = "ADD"
        else:
            action = "REDUCE"

        notional = portfolio_value * abs(delta_weight)

        order = {
            "date": status_date,
            "strategy_id": STRATEGY_ID,
            "version": VERSION,
            "preview": True,
            "symbol": symbol,
            "action": action,
            "reason": "TARGET_DIFF_PREVIEW",
            "target_weight": target_weight,
            "previous_weight": previous_weight,
            "delta_weight": delta_weight,
            "paper_price": target.get("price"),
            "shares": None,
            "notional": notional,
            "status": "PREVIEW_NOT_EXECUTED",
            "core_or_sidecar": target.get("core_or_sidecar"),
            "source": target.get("source"),
            "date_rank": target.get("date_rank", rank),
        }
        orders.append(order)

        if target_weight > 0:
            positions.append({
                "date": status_date,
                "strategy_id": STRATEGY_ID,
                "version": VERSION,
                "preview": True,
                "symbol": symbol,
                "weight": target_weight,
                "shares": None,
                "entry_date": None,
                "entry_price": None,
                "last_price": target.get("price"),
                "market_value": portfolio_value * target_weight,
                "unrealized_return_pct": 0.0,
                "core_or_sidecar": target.get("core_or_sidecar"),
                "source": target.get("source"),
                "date_rank": target.get("date_rank", rank),
            })

    # Exits for previous positions not in targets.
    for symbol, previous in previous_positions.items():
        if symbol in target_symbols:
            continue
        previous_weight = to_float(previous.get("weight"), 0.0)
        if previous_weight <= 0:
            continue
        orders.append({
            "date": status_date,
            "strategy_id": STRATEGY_ID,
            "version": VERSION,
            "preview": True,
            "symbol": symbol,
            "action": "EXIT",
            "reason": "REMOVED_FROM_TARGETS_PREVIEW",
            "target_weight": 0.0,
            "previous_weight": previous_weight,
            "delta_weight": -previous_weight,
            "paper_price": previous.get("last_price"),
            "shares": None,
            "notional": portfolio_value * previous_weight,
            "status": "PREVIEW_NOT_EXECUTED",
            "core_or_sidecar": previous.get("core_or_sidecar"),
            "source": "data/oos/e1r_v0_2_portfolio_state.json",
            "date_rank": None,
        })

    action_counts: Dict[str, int] = {}
    for order in orders:
        action_counts[order["action"]] = action_counts.get(order["action"], 0) + 1

    return {
        "generated_at": now_iso(),
        "status_date": status_date,
        "strategy_id": STRATEGY_ID,
        "version": VERSION,
        "stage": "Stage 3.8E-2F-1E-3",
        "tracking_status": tracking_status,
        "official_kickoff_date": summary.get("official_kickoff_date"),
        "shadow_start_date": summary.get("shadow_start_date"),
        "execution_status": "ORDERS_POSITIONS_PREVIEW_ONLY",
        "portfolio_value": portfolio_value,
        "counts": {
            "targets": len(targets),
            "orders": len(orders),
            "positions": len(positions),
            "buy_orders": action_counts.get("BUY", 0),
            "add_orders": action_counts.get("ADD", 0),
            "hold_orders": action_counts.get("HOLD", 0),
            "reduce_orders": action_counts.get("REDUCE", 0),
            "exit_orders": action_counts.get("EXIT", 0),
        },
        "exposure_preview": {
            "positions_weight_sum": sum(to_float(p.get("weight"), 0.0) for p in positions),
            "orders_abs_delta_weight_sum": sum(abs(to_float(o.get("delta_weight"), 0.0)) for o in orders),
        },
        "orders": orders,
        "positions": positions,
        "notes": [
            "Preview only. Official E1R orders/positions exports are not overwritten.",
            "tracking_status remains KICKOFF_READY.",
            "official_kickoff_date remains null.",
            "Next stage may promote this preview into official E1R paper orders/positions after acceptance.",
        ],
    }


def main() -> int:
    preview = build_preview()

    write_json(ORDERS_PREVIEW_PATH, {
        "generated_at": preview["generated_at"],
        "status_date": preview["status_date"],
        "strategy_id": preview["strategy_id"],
        "version": preview["version"],
        "preview": True,
        "execution_status": preview["execution_status"],
        "counts": preview["counts"],
        "orders": preview["orders"],
    })

    write_json(POSITIONS_PREVIEW_PATH, {
        "generated_at": preview["generated_at"],
        "status_date": preview["status_date"],
        "strategy_id": preview["strategy_id"],
        "version": preview["version"],
        "preview": True,
        "execution_status": preview["execution_status"],
        "counts": preview["counts"],
        "exposure_preview": preview["exposure_preview"],
        "positions": preview["positions"],
    })

    print("E1R orders/positions preview complete")
    print("status_date:", preview["status_date"])
    print("tracking_status:", preview["tracking_status"])
    print("official_kickoff_date:", preview["official_kickoff_date"])
    print("targets:", preview["counts"]["targets"])
    print("orders:", preview["counts"]["orders"])
    print("positions:", preview["counts"]["positions"])
    print("buy_orders:", preview["counts"]["buy_orders"])
    print("add_orders:", preview["counts"]["add_orders"])
    print("hold_orders:", preview["counts"]["hold_orders"])
    print("reduce_orders:", preview["counts"]["reduce_orders"])
    print("exit_orders:", preview["counts"]["exit_orders"])
    print("positions_weight_sum:", preview["exposure_preview"]["positions_weight_sum"])
    print("orders_abs_delta_weight_sum:", preview["exposure_preview"]["orders_abs_delta_weight_sum"])
    print("wrote:", ORDERS_PREVIEW_PATH.relative_to(ROOT))
    print("wrote:", POSITIONS_PREVIEW_PATH.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
