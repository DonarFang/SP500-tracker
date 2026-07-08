#!/usr/bin/env python3
"""
Stage 3.8E-2F-1D
E1R v0.2 independent forward performance layer.

Purpose:
- Do not touch E1 OOS state.
- Do not modify frozen E1R backtest artifacts.
- Consume existing E1R status/equity scaffolding.
- Write E1R-only state and forward performance exports.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]

STATE_DIR = ROOT / "data" / "oos"
EXPORT_DIR = ROOT / "exports"

STATE_PATH = STATE_DIR / "e1r_v0_2_portfolio_state.json"
EVENTS_PATH = STATE_DIR / "e1r_v0_2_events.jsonl"
RUN_HISTORY_PATH = STATE_DIR / "e1r_v0_2_run_history.jsonl"

SUMMARY_PATH = EXPORT_DIR / "oos_e1r_v0_2_summary.json"
EQUITY_PATH = EXPORT_DIR / "oos_e1r_v0_2_equity_curve.json"
POSITIONS_PATH = EXPORT_DIR / "oos_e1r_v0_2_positions.json"
ORDERS_PATH = EXPORT_DIR / "oos_e1r_v0_2_orders.json"

STATUS_PATH = EXPORT_DIR / "e1r_v0_2_status.json"
SCAFFOLD_SUMMARY_PATH = EXPORT_DIR / "oos_e1r_v0_2_summary.json"
SCAFFOLD_EQUITY_PATH = EXPORT_DIR / "oos_e1r_v0_2_equity_curve.json"

STRATEGY_ID = "E1R_REGIME_AWARE_V0_2"
VERSION = "v0.2"
INITIAL_CAPITAL = 100000.0


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def generated_at_display() -> str:
    # Keep display simple and deterministic enough for dashboard.
    return datetime.now().strftime("%Y-%m-%d %H:%M local")


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


def append_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def to_float(v: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        if v is None or v == "":
            return default
        n = float(v)
        if math.isfinite(n):
            return n
    except Exception:
        pass
    return default


def pct_return(current: float, base: float) -> float:
    if not base:
        return 0.0
    return (current / base - 1.0) * 100.0


def max_drawdown_pct(values: List[float]) -> float:
    if not values:
        return 0.0
    peak = values[0]
    max_dd = 0.0
    for v in values:
        peak = max(peak, v)
        if peak:
            dd = (v / peak - 1.0) * 100.0
            max_dd = min(max_dd, dd)
    return max_dd


def daily_returns(values: List[float]) -> List[float]:
    out = []
    for a, b in zip(values, values[1:]):
        if a:
            out.append(b / a - 1.0)
    return out


def sharpe_ratio(values: List[float]) -> Optional[float]:
    rets = daily_returns(values)
    if len(rets) < 2:
        return None
    avg = sum(rets) / len(rets)
    var = sum((x - avg) ** 2 for x in rets) / (len(rets) - 1)
    sd = math.sqrt(var)
    if sd == 0:
        return None
    return (avg / sd) * math.sqrt(252)


def first_existing(*vals: Any, default: Any = None) -> Any:
    for v in vals:
        if v is not None and v != "":
            return v
    return default


def normalize_status_date(status: Dict[str, Any], scaffold_summary: Dict[str, Any], equity_rows: List[Dict[str, Any]]) -> str:
    latest_equity_date = equity_rows[-1].get("date") if equity_rows else None
    return str(first_existing(
        status.get("status_date"),
        scaffold_summary.get("status_date"),
        scaffold_summary.get("date"),
        latest_equity_date,
        default=datetime.now().strftime("%Y-%m-%d"),
    ))


def normalize_equity_rows(raw: Any) -> List[Dict[str, Any]]:
    if isinstance(raw, list):
        rows = raw
    elif isinstance(raw, dict):
        if isinstance(raw.get("curve"), list):
            rows = raw["curve"]
        elif isinstance(raw.get("rows"), list):
            rows = raw["rows"]
        elif isinstance(raw.get("equity_curve"), list):
            rows = raw["equity_curve"]
        else:
            rows = []
    else:
        rows = []

    cleaned = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        date = row.get("date") or row.get("status_date")
        if not date:
            continue

        combined = to_float(
            first_existing(
                row.get("combined_equity"),
                row.get("portfolio_value"),
                row.get("equity"),
                row.get("nav"),
            ),
            None,
        )

        core = to_float(row.get("core_equity"), None)
        sidecar = to_float(row.get("sidecar_equity"), None)

        if combined is None:
            if core is not None and sidecar is not None:
                # Existing scaffold appears to record sleeve equity values.
                # Avoid double-counting by keeping the combined value if present;
                # otherwise use the average as neutral 100000 baseline proxy.
                combined = (core + sidecar) / 2.0
            elif core is not None:
                combined = core
            elif sidecar is not None:
                combined = sidecar
            else:
                combined = INITIAL_CAPITAL

        cleaned.append({
            **row,
            "date": str(date),
            "portfolio_value": float(combined),
            "equity": float(combined),
        })

    # de-duplicate by date, keep latest occurrence
    by_date = {}
    for row in cleaned:
        by_date[row["date"]] = row
    return [by_date[d] for d in sorted(by_date.keys())]


def infer_spx_forward_return_pct() -> Optional[float]:
    # Optional benchmark cross-check from E1 OOS summary when available.
    e1 = read_json(EXPORT_DIR / "oos_summary.json", {})
    for key in ("spx_forward_return_pct", "spx_return_pct", "benchmark_return_pct"):
        v = to_float(e1.get(key), None) if isinstance(e1, dict) else None
        if v is not None:
            return v
    return None


def build_forward_outputs() -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    status = read_json(STATUS_PATH, {})
    scaffold_summary = read_json(SCAFFOLD_SUMMARY_PATH, {})
    raw_equity = read_json(SCAFFOLD_EQUITY_PATH, [])

    equity_rows = normalize_equity_rows(raw_equity)
    status_date = normalize_status_date(status, scaffold_summary, equity_rows)

    if not equity_rows:
        equity_rows = [{
            "date": status_date,
            "portfolio_value": INITIAL_CAPITAL,
            "equity": INITIAL_CAPITAL,
        }]

    if all(row["date"] != status_date for row in equity_rows):
        last_value = equity_rows[-1]["portfolio_value"] if equity_rows else INITIAL_CAPITAL
        equity_rows.append({
            "date": status_date,
            "portfolio_value": last_value,
            "equity": last_value,
        })

    equity_rows = sorted(equity_rows, key=lambda r: r["date"])
    first_date = equity_rows[0]["date"]
    official_kickoff_date = first_existing(
        scaffold_summary.get("official_kickoff_date") if isinstance(scaffold_summary, dict) else None,
        scaffold_summary.get("forward_start_date") if isinstance(scaffold_summary, dict) else None,
        first_date,
    )

    base_value = to_float(equity_rows[0].get("portfolio_value"), INITIAL_CAPITAL) or INITIAL_CAPITAL
    values = [to_float(r.get("portfolio_value"), base_value) or base_value for r in equity_rows]
    current_value = values[-1]
    dd = max_drawdown_pct(values)
    sr = sharpe_ratio(values)

    gross_exposure = to_float(first_existing(
        status.get("gross_exposure") if isinstance(status, dict) else None,
        scaffold_summary.get("gross_exposure") if isinstance(scaffold_summary, dict) else None,
        default=0.0,
    ), 0.0) or 0.0

    core_active = bool(first_existing(
        status.get("core", {}).get("active") if isinstance(status.get("core"), dict) else None,
        status.get("core_active") if isinstance(status, dict) else None,
        scaffold_summary.get("core_active") if isinstance(scaffold_summary, dict) else None,
        default=False,
    ))

    sidecar_active = bool(first_existing(
        status.get("sidecar", {}).get("active") if isinstance(status.get("sidecar"), dict) else None,
        status.get("sidecar_active") if isinstance(status, dict) else None,
        scaffold_summary.get("sidecar_active") if isinstance(scaffold_summary, dict) else None,
        default=False,
    ))

    sidecar_selected_count = int(to_float(first_existing(
        status.get("sidecar", {}).get("selected_count") if isinstance(status.get("sidecar"), dict) else None,
        status.get("sidecar_selected_count") if isinstance(status, dict) else None,
        scaffold_summary.get("sidecar_selected_count") if isinstance(scaffold_summary, dict) else None,
        default=0,
    ), 0) or 0)

    regime = first_existing(status.get("regime"), scaffold_summary.get("regime"), status.get("market_state"), default="UNKNOWN")
    subclass = first_existing(status.get("subclass"), scaffold_summary.get("subclass"), default=None)
    market_state = first_existing(status.get("market_state"), scaffold_summary.get("market_state"), regime, default="UNKNOWN")

    spx_forward = infer_spx_forward_return_pct()
    strategy_forward = pct_return(current_value, base_value)
    alpha = strategy_forward - spx_forward if spx_forward is not None else None

    enhanced_equity = []
    peak = values[0]
    for row, value in zip(equity_rows, values):
        peak = max(peak, value)
        row_return = pct_return(value, base_value)
        row_dd = pct_return(value, peak) if peak else 0.0
        enhanced_equity.append({
            **row,
            "strategy_id": STRATEGY_ID,
            "version": VERSION,
            "portfolio_value": value,
            "equity": value,
            "cash": to_float(row.get("cash"), value) if row.get("cash") is not None else value,
            "market_value": to_float(row.get("market_value"), 0.0) if row.get("market_value") is not None else 0.0,
            "strategy_indexed": 100.0 * value / base_value if base_value else 100.0,
            "forward_return_pct": row_return,
            "drawdown_pct": row_dd,
            "gross_exposure": gross_exposure,
            "core_exposure": gross_exposure if core_active else 0.0,
            "sidecar_exposure": gross_exposure if sidecar_active else 0.0,
            "market_state": market_state,
            "regime": regime,
            "subclass": subclass,
            "official_kickoff_date": official_kickoff_date,
        })

    # We do not invent holdings or trades. These remain empty until E1R target/action logic is wired.
    positions: List[Dict[str, Any]] = []
    orders: List[Dict[str, Any]] = []

    summary = {
        "generated_at": utc_now_iso(),
        "generated_at_display": generated_at_display(),
        "status_date": status_date,
        "strategy_id": STRATEGY_ID,
        "version": VERSION,
        "phase": "Stage 3.8E-2F-1D",
        "research_status": "FROZEN_RESEARCH_CANDIDATE",
        "tracking_status": "KICKOFF_READY",
        "forward_start_date": official_kickoff_date,
        "official_kickoff_date": official_kickoff_date,
        "forward_day_count": len(enhanced_equity),
        "portfolio_value": current_value,
        "equity": current_value,
        "cash": current_value,
        "market_value": 0.0,
        "forward_return_pct": strategy_forward,
        "spx_forward_return_pct": spx_forward,
        "alpha_pct": alpha,
        "max_drawdown_pct": dd,
        "sharpe_ratio": sr,
        "profit_factor": None,
        "number_of_trades": 0,
        "executed_orders_count": 0,
        "open_positions_count": 0,
        "gross_exposure": gross_exposure,
        "net_exposure": gross_exposure,
        "core_exposure": gross_exposure if core_active else 0.0,
        "sidecar_exposure": gross_exposure if sidecar_active else 0.0,
        "market_state": market_state,
        "regime": regime,
        "subclass": subclass,
        "core_active": core_active,
        "sidecar_active": sidecar_active,
        "sidecar_selected_count": sidecar_selected_count,
        "equity_status": "FORWARD_PERFORMANCE_LAYER_ACTIVE",
        "execution_status": "NO_ORDER_ENGINE_WIRED_YET",
        "notes": [
            "Stage 3.8E-2F-1D creates E1R-only forward performance fields.",
            "No E1 state/export is touched.",
            "Positions/orders remain empty until E1R target/action engine is wired.",
            "Historical E1R backtest artifacts are not modified.",
        ],
    }

    state = {
        "strategy_id": STRATEGY_ID,
        "version": VERSION,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
        "official_kickoff_date": official_kickoff_date,
        "status_date": status_date,
        "portfolio_value": current_value,
        "equity": current_value,
        "cash": current_value,
        "market_value": 0.0,
        "positions": positions,
        "last_summary": summary,
    }

    return summary, enhanced_equity, positions, orders, state


def main() -> int:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    summary, equity, positions, orders, state = build_forward_outputs()

    write_json(STATE_PATH, state)
    write_json(SUMMARY_PATH, summary)
    write_json(EQUITY_PATH, equity)
    write_json(POSITIONS_PATH, positions)
    write_json(ORDERS_PATH, orders)

    event = {
        "ts": utc_now_iso(),
        "event": "E1R_FORWARD_PERFORMANCE_LAYER_RUN",
        "status_date": summary["status_date"],
        "tracking_status": summary["tracking_status"],
        "portfolio_value": summary["portfolio_value"],
        "forward_return_pct": summary["forward_return_pct"],
    }
    append_jsonl(EVENTS_PATH, event)
    append_jsonl(RUN_HISTORY_PATH, event)

    print("E1R v0.2 forward performance layer complete")
    print("status_date:", summary["status_date"])
    print("official_kickoff_date:", summary["official_kickoff_date"])
    print("tracking_status:", summary["tracking_status"])
    print("portfolio_value:", summary["portfolio_value"])
    print("forward_return_pct:", summary["forward_return_pct"])
    print("max_drawdown_pct:", summary["max_drawdown_pct"])
    print("sharpe_ratio:", summary["sharpe_ratio"])
    print("gross_exposure:", summary["gross_exposure"])
    print("wrote:", STATE_PATH.relative_to(ROOT))
    print("wrote:", SUMMARY_PATH.relative_to(ROOT))
    print("wrote:", EQUITY_PATH.relative_to(ROOT))
    print("wrote:", POSITIONS_PATH.relative_to(ROOT))
    print("wrote:", ORDERS_PATH.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
