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


def safe_float(v: Any, default: float = 0.0) -> float:
    try:
        if v is None:
            return default
        return float(v)
    except Exception:
        return default


def normalize_positions(positions: Any) -> dict[str, dict[str, Any]]:
    """
    Normalize sidecar_positions into:
      symbol -> {symbol, target_weight, score, source}

    Expected source:
      latest record in exports/oos_e1r_v0_2_equity_curve.json
    """
    out: dict[str, dict[str, Any]] = {}

    if not isinstance(positions, list):
        return out

    for p in positions:
        if not isinstance(p, dict):
            continue

        symbol = str(p.get("symbol") or "").upper().strip()
        if not symbol:
            continue

        weight = safe_float(p.get("target_weight", p.get("weight", 0.0)), 0.0)

        out[symbol] = {
            "symbol": symbol,
            "target_weight": weight,
            "score": p.get("score"),
            "source": p.get("source", "E1R_V0_2_SIDECAR_TARGET"),
        }

    return out


def compute_lifecycle(prev_positions: dict[str, dict[str, Any]], curr_positions: dict[str, dict[str, Any]]) -> dict[str, Any]:
    prev_symbols = set(prev_positions.keys())
    curr_symbols = set(curr_positions.keys())

    entered = sorted(curr_symbols - prev_symbols)
    exited = sorted(prev_symbols - curr_symbols)
    stayed = sorted(prev_symbols & curr_symbols)

    increased = []
    decreased = []
    unchanged = []

    turnover = 0.0
    gross_added = 0.0
    gross_removed = 0.0

    all_symbols = sorted(prev_symbols | curr_symbols)

    changes = []

    for symbol in all_symbols:
        prev_w = safe_float(prev_positions.get(symbol, {}).get("target_weight"), 0.0)
        curr_w = safe_float(curr_positions.get(symbol, {}).get("target_weight"), 0.0)
        delta = curr_w - prev_w
        abs_delta = abs(delta)

        turnover += abs_delta

        if delta > 0:
            gross_added += delta
        elif delta < 0:
            gross_removed += abs(delta)

        if symbol in stayed:
            if delta > 0:
                increased.append(symbol)
            elif delta < 0:
                decreased.append(symbol)
            else:
                unchanged.append(symbol)

        changes.append({
            "symbol": symbol,
            "previous_weight": prev_w,
            "current_weight": curr_w,
            "delta_weight": delta,
            "abs_delta_weight": abs_delta,
            "change_type": (
                "ENTER" if symbol in entered else
                "EXIT" if symbol in exited else
                "INCREASE" if delta > 0 else
                "DECREASE" if delta < 0 else
                "UNCHANGED"
            ),
        })

    # Portfolio turnover convention:
    # half-turnover = 0.5 * sum(abs(weight change))
    # This estimates one-way turnover for a fully funded sleeve.
    one_way_turnover = 0.5 * turnover

    return {
        "entered_symbols": entered,
        "exited_symbols": exited,
        "stayed_symbols": stayed,
        "increased_symbols": increased,
        "decreased_symbols": decreased,
        "unchanged_symbols": unchanged,
        "entered_count": len(entered),
        "exited_count": len(exited),
        "stayed_count": len(stayed),
        "current_count": len(curr_symbols),
        "previous_count": len(prev_symbols),
        "gross_added_weight": gross_added,
        "gross_removed_weight": gross_removed,
        "two_way_turnover": turnover,
        "one_way_turnover": one_way_turnover,
        "changes": changes,
    }


def main() -> None:
    generated_at = datetime.now(timezone.utc).isoformat()

    equity_path = ROOT / "exports/oos_e1r_v0_2_equity_curve.json"
    lifecycle_path = ROOT / "exports/oos_e1r_v0_2_sidecar_lifecycle.json"
    turnover_path = ROOT / "exports/oos_e1r_v0_2_sidecar_turnover.json"

    equity = read_json(equity_path, {}) or {}
    records = equity.get("records", [])

    if not isinstance(records, list) or not records:
        raise RuntimeError("Missing OOS equity records. Run scripts/run_e1r_v0_2_oos_equity.py first.")

    records = [r for r in records if isinstance(r, dict) and r.get("date")]
    records = sorted(records, key=lambda r: str(r.get("date")))

    latest = records[-1]
    previous = records[-2] if len(records) >= 2 else None

    date = str(latest.get("date"))
    previous_date = str(previous.get("date")) if previous else None

    curr_positions = normalize_positions(latest.get("sidecar_positions", []))
    prev_positions = normalize_positions(previous.get("sidecar_positions", [])) if previous else {}

    lifecycle = compute_lifecycle(prev_positions, curr_positions)

    lifecycle_status = (
        "NO_PREVIOUS_RECORD" if previous is None else
        "SIDECAR_INACTIVE_NO_POSITIONS" if not curr_positions and not prev_positions else
        "CALCULATED"
    )

    latest_record = {
        "date": date,
        "previous_date": previous_date,
        "generated_at": generated_at,
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "phase": "OOS_2B_3_SIDECAR_LIFECYCLE_TURNOVER",
        "execution_status": "PAPER_TRACKING_NO_REAL_EXECUTION",
        "lifecycle_status": lifecycle_status,
        "market_state": latest.get("market_state"),
        "sidecar_active": latest.get("sidecar_active"),
        "sidecar_mtm_status": latest.get("sidecar_mtm_status"),
        "sidecar_daily_return": latest.get("sidecar_daily_return"),
        "sidecar_equity": latest.get("sidecar_equity"),
        **lifecycle,
    }

    existing_lifecycle = read_json(lifecycle_path, {}) or {}
    history = existing_lifecycle.get("records", [])
    if not isinstance(history, list):
        history = []

    history = [r for r in history if isinstance(r, dict) and r.get("date") != date]
    history.append(latest_record)
    history = sorted(history, key=lambda r: str(r.get("date")))

    lifecycle_output = {
        "generated_at": generated_at,
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "phase": "OOS_2B_3_SIDECAR_LIFECYCLE_TURNOVER",
        "execution_status": "PAPER_TRACKING_NO_REAL_EXECUTION",
        "source": "exports/oos_e1r_v0_2_equity_curve.json",
        "start_date": history[0]["date"] if history else date,
        "end_date": history[-1]["date"] if history else date,
        "row_count": len(history),
        "latest": latest_record,
        "records": history,
        "notes": [
            "Tracks sidecar target position changes day by day.",
            "Calculates entered/exited/stayed symbols and target-weight turnover.",
            "Still paper tracking only; no real orders, no fills, no broker execution.",
            "One-way turnover uses 0.5 * sum(abs(weight_delta)).",
        ],
    }

    turnover_latest = {
        "date": date,
        "previous_date": previous_date,
        "generated_at": generated_at,
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "phase": "OOS_2B_3_SIDECAR_TURNOVER",
        "execution_status": "PAPER_TRACKING_NO_REAL_EXECUTION",
        "market_state": latest.get("market_state"),
        "sidecar_active": latest.get("sidecar_active"),
        "lifecycle_status": lifecycle_status,
        "previous_count": lifecycle["previous_count"],
        "current_count": lifecycle["current_count"],
        "entered_count": lifecycle["entered_count"],
        "exited_count": lifecycle["exited_count"],
        "stayed_count": lifecycle["stayed_count"],
        "gross_added_weight": lifecycle["gross_added_weight"],
        "gross_removed_weight": lifecycle["gross_removed_weight"],
        "two_way_turnover": lifecycle["two_way_turnover"],
        "one_way_turnover": lifecycle["one_way_turnover"],
        "entered_symbols": lifecycle["entered_symbols"],
        "exited_symbols": lifecycle["exited_symbols"],
    }

    existing_turnover = read_json(turnover_path, {}) or {}
    turnover_history = existing_turnover.get("records", [])
    if not isinstance(turnover_history, list):
        turnover_history = []

    turnover_history = [r for r in turnover_history if isinstance(r, dict) and r.get("date") != date]
    turnover_history.append(turnover_latest)
    turnover_history = sorted(turnover_history, key=lambda r: str(r.get("date")))

    avg_one_way_turnover = (
        sum(safe_float(r.get("one_way_turnover"), 0.0) for r in turnover_history) / len(turnover_history)
        if turnover_history else 0.0
    )

    turnover_output = {
        "generated_at": generated_at,
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "phase": "OOS_2B_3_SIDECAR_TURNOVER",
        "execution_status": "PAPER_TRACKING_NO_REAL_EXECUTION",
        "source": "exports/oos_e1r_v0_2_equity_curve.json",
        "start_date": turnover_history[0]["date"] if turnover_history else date,
        "end_date": turnover_history[-1]["date"] if turnover_history else date,
        "row_count": len(turnover_history),
        "average_one_way_turnover": avg_one_way_turnover,
        "latest": turnover_latest,
        "records": turnover_history,
        "notes": [
            "Turnover is based on target position changes, not real fills.",
            "This prepares transaction-cost analysis but does not apply costs yet.",
        ],
    }

    write_json(lifecycle_path, lifecycle_output)
    write_json(turnover_path, turnover_output)

    print("E1R v0.2 OOS-2B.3 sidecar lifecycle/turnover export complete")
    print("date:", date)
    print("previous_date:", previous_date)
    print("market_state:", latest_record["market_state"])
    print("sidecar_active:", latest_record["sidecar_active"])
    print("lifecycle_status:", lifecycle_status)
    print("previous_count:", latest_record["previous_count"])
    print("current_count:", latest_record["current_count"])
    print("entered_count:", latest_record["entered_count"])
    print("exited_count:", latest_record["exited_count"])
    print("one_way_turnover:", latest_record["one_way_turnover"])
    print("wrote:", lifecycle_path.relative_to(ROOT))
    print("wrote:", turnover_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
