from __future__ import annotations

import json
import runpy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    status_script = ROOT / "scripts/export_e1r_v0_2_status.py"
    status_path = ROOT / "exports/e1r_v0_2_status.json"

    if not status_script.exists():
        raise RuntimeError("Missing scripts/export_e1r_v0_2_status.py")

    # Refresh the lightweight v0.2 status first.
    runpy.run_path(str(status_script), run_name="__main__")

    if not status_path.exists():
        raise RuntimeError("exports/e1r_v0_2_status.json was not generated")

    status = read_json(status_path)

    generated_at = datetime.now(timezone.utc).isoformat()
    status_date = status.get("status_date")
    strategy_id = status.get("strategy_id", "E1R_REGIME_AWARE_V0_2")
    market_state = status.get("e1r_market_state", "UNKNOWN")
    regime = status.get("regime")
    subclass = status.get("subclass")

    core = status.get("core", {}) or {}
    sidecar = status.get("sidecar", {}) or {}
    selected = sidecar.get("selected", []) or []

    core_active = bool(core.get("active"))
    sidecar_active = bool(sidecar.get("active"))

    phase = "OOS_STATUS_SIGNAL_ONLY"

    summary = {
        "generated_at": generated_at,
        "phase": phase,
        "strategy_id": strategy_id,
        "version": status.get("version"),
        "research_status": status.get("research_status"),
        "status_date": status_date,
        "market_state": market_state,
        "regime": regime,
        "subclass": subclass,
        "mutually_exclusive_state_model": bool(status.get("mutually_exclusive_state_model")),
        "core_active": core_active,
        "sidecar_active": sidecar_active,
        "sidecar_selected_count": len(selected),
        "gross_exposure": sidecar.get("gross_exposure"),
        "top_n": sidecar.get("top_n"),
        "execution_status": "NO_REAL_EXECUTION",
        "equity_status": "NOT_YET_CONNECTED",
        "notes": [
            "OOS-1 exports daily E1R v0.2 state and sidecar target signals only.",
            "No real orders are executed by this script.",
            "No E1R v0.2 OOS equity curve is updated by this script.",
            "This is the bridge layer for Dashboard and future OOS equity integration.",
        ],
    }

    sidecar_export = {
        "generated_at": generated_at,
        "phase": phase,
        "strategy_id": strategy_id,
        "status_date": status_date,
        "market_state": market_state,
        "regime": regime,
        "subclass": subclass,
        "active": sidecar_active,
        "active_condition": sidecar.get("active_condition"),
        "gross_exposure": sidecar.get("gross_exposure"),
        "top_n": sidecar.get("top_n"),
        "excluded_symbols": sidecar.get("excluded_symbols", []),
        "source_record_date": sidecar.get("source_record_date"),
        "source_record_next_date": sidecar.get("source_record_next_date"),
        "selected_count": len(selected),
        "selected": selected,
    }

    target_positions = []
    if sidecar_active:
        for h in selected:
            symbol = h.get("symbol")
            if not symbol:
                continue
            target_positions.append({
                "symbol": symbol,
                "sleeve": "E1R_V0_2_SIDECAR",
                "target_weight": h.get("weight"),
                "score": h.get("score"),
                "source": "SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
                "execution_status": "TARGET_ONLY_NOT_EXECUTED",
            })

    positions = {
        "generated_at": generated_at,
        "phase": phase,
        "strategy_id": strategy_id,
        "status_date": status_date,
        "market_state": market_state,
        "core": {
            "active": core_active,
            "strategy_id": core.get("strategy_id", "E1R_REGIME_AWARE_V0_1"),
            "positions_status": "NOT_CONNECTED_IN_OOS_1",
        },
        "sidecar": {
            "active": sidecar_active,
            "positions_status": "TARGET_ONLY_NOT_EXECUTED",
            "target_positions": target_positions,
        },
    }

    orders = {
        "generated_at": generated_at,
        "phase": phase,
        "strategy_id": strategy_id,
        "status_date": status_date,
        "market_state": market_state,
        "execution_status": "NO_REAL_EXECUTION",
        "orders": [
            {
                "symbol": p["symbol"],
                "sleeve": p["sleeve"],
                "target_weight": p["target_weight"],
                "side": "TARGET_HOLD",
                "status": "SIGNAL_ONLY",
                "reason": "E1R_V0_2_OOS_1_SIGNAL_EXPORT_ONLY",
            }
            for p in target_positions
        ],
    }

    write_json(ROOT / "exports/oos_e1r_v0_2_summary.json", summary)
    write_json(ROOT / "exports/oos_e1r_v0_2_sidecar.json", sidecar_export)
    write_json(ROOT / "exports/oos_e1r_v0_2_positions.json", positions)
    write_json(ROOT / "exports/oos_e1r_v0_2_orders.json", orders)

    print("E1R v0.2 OOS-1 export complete")
    print("status_date:", status_date)
    print("market_state:", market_state)
    print("core_active:", core_active)
    print("sidecar_active:", sidecar_active)
    print("sidecar_selected_count:", len(selected))
    print("wrote:")
    print("  exports/e1r_v0_2_status.json")
    print("  exports/oos_e1r_v0_2_summary.json")
    print("  exports/oos_e1r_v0_2_sidecar.json")
    print("  exports/oos_e1r_v0_2_positions.json")
    print("  exports/oos_e1r_v0_2_orders.json")
    # Refresh forward/OOS equity curve after status and signal exports.
    equity_script = ROOT / "scripts/run_e1r_v0_2_oos_equity.py"
    if equity_script.exists():
        runpy.run_path(str(equity_script), run_name="__main__")
        print("  exports/oos_e1r_v0_2_equity_curve.json")
        lifecycle_script = ROOT / "scripts/run_e1r_v0_2_sidecar_lifecycle.py"
        if lifecycle_script.exists():
            runpy.run_path(str(lifecycle_script), run_name="__main__")
            print("  exports/oos_e1r_v0_2_sidecar_lifecycle.json")
            print("  exports/oos_e1r_v0_2_sidecar_turnover.json")


if __name__ == "__main__":
    main()
