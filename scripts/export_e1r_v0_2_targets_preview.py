#!/usr/bin/env python3
"""
Stage 3.8E-2F-1E-2
E1R v0.2 target extraction preview.

Purpose:
- Extract symbol-level E1R target candidates.
- Do not create orders.
- Do not update positions.
- Do not modify E1 state/export.
- Do not change LIVE_FORWARD status.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = ROOT / "exports"

STATUS_PATH = EXPORT_DIR / "e1r_v0_2_status.json"
SIDECAR_PATH = EXPORT_DIR / "oos_e1r_v0_2_sidecar.json"
LEADERBOARD_PATH = EXPORT_DIR / "leaderboard.json"
SUMMARY_PATH = EXPORT_DIR / "oos_e1r_v0_2_summary.json"

TARGETS_PATH = EXPORT_DIR / "oos_e1r_v0_2_targets.json"

STRATEGY_ID = "E1R_REGIME_AWARE_V0_2"
VERSION = "v0.2"


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


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(v: Any, default: bool = False) -> bool:
    if isinstance(v, bool):
        return v
    if v is None:
        return default
    if isinstance(v, str):
        return v.strip().lower() in {"1", "true", "yes", "y", "active"}
    return bool(v)


def as_float(v: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        if v is None or v == "":
            return default
        return float(v)
    except Exception:
        return default


def pick_first(obj: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    if not isinstance(obj, dict):
        return default
    for k in keys:
        if k in obj and obj[k] not in (None, ""):
            return obj[k]
    return default


def normalize_symbol(v: Any) -> Optional[str]:
    if not isinstance(v, str):
        return None
    s = v.strip().upper()
    if not s:
        return None
    return s


def extract_leader_rows(raw: Any) -> List[Dict[str, Any]]:
    if isinstance(raw, dict):
        for key in ["leaders", "rows", "data", "leaderboard"]:
            rows = raw.get(key)
            if isinstance(rows, list):
                return [r for r in rows if isinstance(r, dict)]
    if isinstance(raw, list):
        return [r for r in raw if isinstance(r, dict)]
    return []


def extract_selected_list(raw: Any) -> List[Any]:
    if isinstance(raw, dict):
        for key in ["selected", "selected_symbols", "symbols", "candidates", "positions"]:
            v = raw.get(key)
            if isinstance(v, list):
                return v
        # common nested sidecar structure
        sidecar = raw.get("sidecar")
        if isinstance(sidecar, dict):
            for key in ["selected", "selected_symbols", "symbols", "candidates", "positions"]:
                v = sidecar.get(key)
                if isinstance(v, list):
                    return v
    return []


def extract_symbol_from_row(row: Any) -> Optional[str]:
    if isinstance(row, str):
        return normalize_symbol(row)
    if not isinstance(row, dict):
        return None
    return normalize_symbol(pick_first(row, ["symbol", "ticker", "name"]))


def extract_core_targets(leaderboard: Any, status: Dict[str, Any], summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = extract_leader_rows(leaderboard)

    core_active = as_bool(
        pick_first(status, ["core_active"], None),
        default=as_bool(pick_first(summary, ["core_active"], True), True),
    )

    if not core_active:
        return []

    top_n = int(as_float(
        pick_first(status, ["top_n"], pick_first(summary, ["top_n"], 10)),
        10,
    ) or 10)

    # Conservative preview rule:
    # Use top N current leaderboard symbols as core target candidates.
    # Weighting is only preview-level until execution accounting is approved.
    core_exposure = as_float(
        pick_first(summary, ["core_exposure"], None),
        None,
    )

    gross_exposure = as_float(
        pick_first(status, ["gross_exposure"], pick_first(summary, ["gross_exposure"], 0.0)),
        0.0,
    ) or 0.0

    if core_exposure is None:
        # If current status only has gross_exposure, use it as preview sleeve exposure.
        # This does not imply execution approval.
        core_exposure = gross_exposure

    selected = []
    seen = set()
    for rank, row in enumerate(rows, start=1):
        sym = extract_symbol_from_row(row)
        if not sym or sym in seen:
            continue
        seen.add(sym)

        score = pick_first(row, ["leader_score", "score", "ls", "rank_score"], None)
        price = pick_first(row, ["price", "last_price", "close"], None)

        selected.append({
            "date_rank": rank,
            "symbol": sym,
            "core_or_sidecar": "core",
            "source": "exports/leaderboard.json",
            "target_weight": None,
            "preview_weight": None,
            "leader_score": score,
            "price": price,
            "raw": row,
        })

        if len(selected) >= top_n:
            break

    if selected:
        equal_weight = core_exposure / len(selected) if len(selected) else 0.0
        for row in selected:
            row["preview_weight"] = equal_weight
            row["target_weight"] = equal_weight

    return selected


def extract_sidecar_targets(sidecar: Any, status: Dict[str, Any], summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    sidecar_obj = sidecar if isinstance(sidecar, dict) else {}
    selected_raw = extract_selected_list(sidecar_obj)

    status_sidecar = status.get("sidecar") if isinstance(status.get("sidecar"), dict) else {}

    sidecar_active = as_bool(
        pick_first(status, ["sidecar_active"], None),
        default=as_bool(pick_first(summary, ["sidecar_active"], False), False),
    )
    if not sidecar_active:
        # Still extract visible candidates, but mark inactive.
        pass

    sidecar_exposure = as_float(
        pick_first(summary, ["sidecar_exposure"], None),
        None,
    )

    gross_exposure = as_float(
        pick_first(sidecar_obj, ["gross_exposure"], pick_first(status_sidecar, ["gross_exposure"], pick_first(summary, ["gross_exposure"], 0.0))),
        0.0,
    ) or 0.0

    if sidecar_exposure is None:
        sidecar_exposure = gross_exposure if sidecar_active else 0.0

    targets = []
    seen = set()

    for idx, item in enumerate(selected_raw, start=1):
        sym = extract_symbol_from_row(item)
        if not sym or sym in seen:
            continue
        seen.add(sym)

        raw_weight = None
        raw_price = None
        raw_score = None
        if isinstance(item, dict):
            raw_weight = pick_first(item, ["target_weight", "weight", "allocation"], None)
            raw_price = pick_first(item, ["price", "last_price", "close"], None)
            raw_score = pick_first(item, ["score", "leader_score", "rank_score"], None)

        targets.append({
            "date_rank": idx,
            "symbol": sym,
            "core_or_sidecar": "sidecar",
            "source": "exports/oos_e1r_v0_2_sidecar.json",
            "target_weight": as_float(raw_weight, None),
            "preview_weight": None,
            "sidecar_active": sidecar_active,
            "score": raw_score,
            "price": raw_price,
            "raw": item,
        })

    unresolved_weight_count = sum(1 for x in targets if x["target_weight"] is None)

    if targets and unresolved_weight_count:
        equal_weight = sidecar_exposure / len(targets) if sidecar_active and len(targets) else 0.0
        for row in targets:
            if row["target_weight"] is None:
                row["target_weight"] = equal_weight
            row["preview_weight"] = row["target_weight"]
    else:
        for row in targets:
            row["preview_weight"] = row["target_weight"]

    return targets


def merge_targets(core_targets: List[Dict[str, Any]], sidecar_targets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Keep core and sidecar rows separate in preview.
    # If same symbol appears in both, include both rows with sleeve labels;
    # later orders layer can aggregate by symbol after approval.
    return core_targets + sidecar_targets


def main() -> int:
    status = read_json(STATUS_PATH, {})
    sidecar = read_json(SIDECAR_PATH, {})
    leaderboard = read_json(LEADERBOARD_PATH, {})
    summary = read_json(SUMMARY_PATH, {})

    status_date = (
        status.get("status_date")
        or summary.get("status_date")
        or datetime.now().strftime("%Y-%m-%d")
    )

    core_targets = extract_core_targets(leaderboard, status, summary)
    sidecar_targets = extract_sidecar_targets(sidecar, status, summary)
    all_targets = merge_targets(core_targets, sidecar_targets)

    output = {
        "generated_at": now_iso(),
        "status_date": status_date,
        "strategy_id": STRATEGY_ID,
        "version": VERSION,
        "stage": "Stage 3.8E-2F-1E-2",
        "tracking_status": summary.get("tracking_status", "KICKOFF_READY"),
        "official_kickoff_date": summary.get("official_kickoff_date"),
        "shadow_start_date": summary.get("shadow_start_date"),
        "contract": {
            "core_target_source": "exports/leaderboard.json",
            "sidecar_target_source": "exports/oos_e1r_v0_2_sidecar.json",
            "orders_rule": "orders = diff(previous E1R positions, new symbol-level target weights)",
            "execution_status": "TARGET_PREVIEW_ONLY_NO_ORDERS",
            "guardrail": "Do not infer executable orders from gross_exposure alone without symbol-level targets.",
        },
        "counts": {
            "core_targets": len(core_targets),
            "sidecar_targets": len(sidecar_targets),
            "all_targets": len(all_targets),
        },
        "exposure_preview": {
            "core_weight_sum": sum((x.get("target_weight") or 0.0) for x in core_targets),
            "sidecar_weight_sum": sum((x.get("target_weight") or 0.0) for x in sidecar_targets),
            "total_weight_sum": sum((x.get("target_weight") or 0.0) for x in all_targets),
        },
        "core_targets": core_targets,
        "sidecar_targets": sidecar_targets,
        "targets": all_targets,
        "notes": [
            "This file is a target extraction preview only.",
            "It does not update E1R positions or orders.",
            "It does not change tracking_status to LIVE_FORWARD.",
            "Orders require explicit approval in the next implementation stage.",
        ],
    }

    write_json(TARGETS_PATH, output)

    print("E1R target extraction preview complete")
    print("status_date:", status_date)
    print("tracking_status:", output["tracking_status"])
    print("official_kickoff_date:", output["official_kickoff_date"])
    print("core_targets:", len(core_targets))
    print("sidecar_targets:", len(sidecar_targets))
    print("all_targets:", len(all_targets))
    print("core_weight_sum:", output["exposure_preview"]["core_weight_sum"])
    print("sidecar_weight_sum:", output["exposure_preview"]["sidecar_weight_sum"])
    print("total_weight_sum:", output["exposure_preview"]["total_weight_sum"])
    print("wrote:", TARGETS_PATH.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
