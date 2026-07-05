from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text())


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def pick(obj: Any, keys: list[str], default: Any = None) -> Any:
    if not isinstance(obj, dict):
        return default
    for k in keys:
        v = obj.get(k)
        if v not in (None, ""):
            return v
    return default


def safe_float(v: Any, default: float | None = None) -> float | None:
    try:
        if v is None:
            return default
        return float(v)
    except Exception:
        return default


def extract_existing_oos_core_equity() -> dict[str, Any]:
    """
    Best-effort bridge to existing legacy OOS equity if present.

    This function does not assume a fixed old schema.
    It tries to find the latest equity value from:
      - exports/oos_summary.json
      - exports/oos_equity_curve.json

    If nothing usable exists, it initializes at 100000.
    """
    summary = read_json(ROOT / "exports/oos_summary.json", {}) or {}
    curve = read_json(ROOT / "exports/oos_equity_curve.json", {}) or {}

    equity = safe_float(
        pick(summary, ["equity", "current_equity", "portfolio_value", "final_equity", "total_equity"]),
        None,
    )

    date = pick(summary, ["date", "status_date", "as_of", "data_date"], None)

    records = None
    if isinstance(curve, list):
        records = curve
    elif isinstance(curve, dict):
        records = (
            curve.get("records")
            or curve.get("equity_curve")
            or curve.get("series")
            or curve.get("data")
        )

    if isinstance(records, list) and records:
        rows = [r for r in records if isinstance(r, dict)]
        if rows:
            rows = sorted(rows, key=lambda r: str(pick(r, ["date", "status_date", "as_of"], "")))
            last = rows[-1]
            equity = safe_float(
                pick(last, ["equity", "total_equity", "portfolio_value", "value"]),
                equity,
            )
            date = pick(last, ["date", "status_date", "as_of"], date)

    if equity is None:
        equity = 100000.0

    return {
        "date": date,
        "equity": equity,
        "source": "legacy_oos_if_available_else_initial_capital",
    }


def compute_return(prev_equity: float, new_equity: float) -> float:
    if prev_equity == 0:
        return 0.0
    return (new_equity / prev_equity) - 1.0


def main() -> None:
    status = read_json(ROOT / "exports/e1r_v0_2_status.json", {}) or {}
    summary = read_json(ROOT / "exports/oos_e1r_v0_2_summary.json", {}) or {}
    sidecar = read_json(ROOT / "exports/oos_e1r_v0_2_sidecar.json", {}) or {}

    out_path = ROOT / "exports/oos_e1r_v0_2_equity_curve.json"
    existing = read_json(out_path, {}) or {}

    generated_at = datetime.now(timezone.utc).isoformat()

    status_date = (
        summary.get("status_date")
        or status.get("status_date")
        or sidecar.get("status_date")
    )

    if not status_date:
        raise RuntimeError("Missing status_date from E1R v0.2 OOS status files")

    market_state = (
        summary.get("market_state")
        or status.get("e1r_market_state")
        or "UNKNOWN"
    )

    core_active = bool(summary.get("core_active", status.get("core", {}).get("active", False)))
    sidecar_active = bool(summary.get("sidecar_active", sidecar.get("active", False)))
    selected_count = int(summary.get("sidecar_selected_count", sidecar.get("selected_count", 0)) or 0)

    initial_capital = 100000.0
    legacy_core = extract_existing_oos_core_equity()

    records = existing.get("records", []) if isinstance(existing, dict) else []
    if not isinstance(records, list):
        records = []

    records = [r for r in records if isinstance(r, dict)]
    records = sorted(records, key=lambda r: str(r.get("date", "")))

    previous = records[-1] if records else None

    if previous and previous.get("date") == status_date:
        # Idempotent update for the same date.
        core_equity = safe_float(previous.get("core_equity"), legacy_core["equity"]) or initial_capital
        sidecar_equity = safe_float(previous.get("sidecar_equity"), initial_capital) or initial_capital
        combined_equity = safe_float(previous.get("combined_equity"), core_equity) or core_equity
        prev_core_equity = core_equity
        prev_sidecar_equity = sidecar_equity
        prev_combined_equity = combined_equity
        daily_core_return = safe_float(previous.get("core_daily_return"), 0.0) or 0.0
        daily_sidecar_return = safe_float(previous.get("sidecar_daily_return"), 0.0) or 0.0
        daily_combined_return = safe_float(previous.get("combined_daily_return"), 0.0) or 0.0
        update_mode = "UPDATED_EXISTING_DATE"
    else:
        prev_core_equity = safe_float(previous.get("core_equity"), None) if previous else None
        prev_sidecar_equity = safe_float(previous.get("sidecar_equity"), None) if previous else None
        prev_combined_equity = safe_float(previous.get("combined_equity"), None) if previous else None

        if prev_core_equity is None:
            prev_core_equity = initial_capital
        if prev_sidecar_equity is None:
            prev_sidecar_equity = initial_capital
        if prev_combined_equity is None:
            prev_combined_equity = initial_capital

        # OOS-2B.1:
        # Core equity bridges to legacy OOS equity if available.
        # Sidecar is target-only/paper initialized; no MTM return is applied yet.
        core_equity = legacy_core["equity"] if core_active else prev_core_equity
        sidecar_equity = prev_sidecar_equity

        daily_core_return = compute_return(prev_core_equity, core_equity)
        daily_sidecar_return = 0.0

        combined_daily_return = (1.0 + daily_core_return) * (1.0 + daily_sidecar_return) - 1.0
        combined_equity = prev_combined_equity * (1.0 + combined_daily_return)

        daily_combined_return = combined_daily_return
        update_mode = "APPENDED_NEW_DATE"

    record = {
        "date": status_date,
        "generated_at": generated_at,
        "market_state": market_state,
        "core_active": core_active,
        "sidecar_active": sidecar_active,
        "sidecar_selected_count": selected_count,
        "core_equity": core_equity,
        "sidecar_equity": sidecar_equity,
        "combined_equity": combined_equity,
        "core_daily_return": daily_core_return,
        "sidecar_daily_return": daily_sidecar_return,
        "combined_daily_return": daily_combined_return,
        "core_source": legacy_core["source"],
        "sidecar_source": "target_only_no_mtm_in_oos_2b_1",
        "combined_source": "core_bridge_plus_sidecar_target_only",
        "execution_status": "PAPER_TRACKING_NO_REAL_EXECUTION",
        "equity_status": "OOS_EQUITY_INITIALIZED_TARGET_ONLY",
        "update_mode": update_mode,
    }

    if previous and previous.get("date") == status_date:
        records[-1] = record
    else:
        records.append(record)

    records = sorted(records, key=lambda r: str(r.get("date", "")))

    latest = records[-1]

    output = {
        "generated_at": generated_at,
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "phase": "OOS_2B_FORWARD_EQUITY_CURVE",
        "equity_status": "OOS_EQUITY_INITIALIZED_TARGET_ONLY",
        "execution_status": "PAPER_TRACKING_NO_REAL_EXECUTION",
        "curve_type": "FORWARD_OOS_EQUITY",
        "start_date": records[0]["date"] if records else status_date,
        "end_date": latest["date"],
        "row_count": len(records),
        "latest": latest,
        "records": records,
        "notes": [
            "OOS-2B.1 initializes E1R v0.2 forward/OOS equity curve schema.",
            "Core equity bridges to existing legacy OOS equity when available.",
            "Sidecar equity is target-only and does not apply MTM return yet.",
            "No real orders are executed by this script.",
            "OOS-2B.2 should add sidecar daily MTM and simulated/real position lifecycle.",
        ],
    }

    write_json(out_path, output)

    print("E1R v0.2 OOS-2B equity export complete")
    print("status_date:", status_date)
    print("market_state:", market_state)
    print("core_active:", core_active)
    print("sidecar_active:", sidecar_active)
    print("sidecar_selected_count:", selected_count)
    print("core_equity:", core_equity)
    print("sidecar_equity:", sidecar_equity)
    print("combined_equity:", combined_equity)
    print("row_count:", len(records))
    print("update_mode:", update_mode)
    print("wrote:", out_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
