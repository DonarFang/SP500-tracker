#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

E1_5Y = ROOT / "exports/e1_5y_backtest_equity_curve.json"
E1R_COMPARISON = ROOT / "exports/e1_vs_e1r_direct_composed_5y_comparison_noncanonical.json"
E1_OOS = ROOT / "exports/oos_equity_curve.json"
E1R_OOS = ROOT / "exports/oos_e1r_v0_2_equity_curve.json"

OUT_BUNDLE = ROOT / "exports/e1_e1r_research_curve_bundle_noncanonical.json"

REPORT_JSON = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0N_RESEARCH_CURVE_BUNDLE_REPORT.json"
REPORT_MD = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0N_RESEARCH_CURVE_BUNDLE_REPORT.md"

FROZEN_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

CANONICAL_E1R_FILES = [
    ROOT / "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
    ROOT / "exports/e1_e1r_5y_equity_comparison.json",
]

FROZEN_TARGET = {
    "strategy_id": "E1R_REGIME_AWARE_V0_2",
    "total_return_pct": 116.7435999134756,
    "spx_return_pct": 76.844174428316,
    "alpha_pct": 39.89942548515961,
    "max_drawdown_pct": 25.904809362815108,
    "profit_factor": 1.1919630955509348,
    "sharpe_ratio": 0.7957270568329264,
}

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))

def sha256(p: Path) -> str | None:
    if not p.exists():
        return None
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def read_json_if_exists(p: Path) -> Any:
    if not p.exists():
        return None
    return json.loads(p.read_text())

def write_json(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def as_float(x: Any, default=None):
    try:
        if x is None:
            return default
        return float(x)
    except Exception:
        return default

def extract_rows(obj: Any) -> list[dict[str, Any]]:
    if obj is None:
        return []
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]
    if isinstance(obj, dict):
        for k in ["rows", "curve", "daily_equity_records", "daily_records", "records", "equity_curve"]:
            v = obj.get(k)
            if isinstance(v, list):
                return [x for x in v if isinstance(x, dict)]
        if isinstance(obj.get("result"), dict):
            return extract_rows(obj["result"])
    return []

def get_date(row: dict[str, Any]) -> str | None:
    for k in ["date", "interval_end_date", "next_date"]:
        v = row.get(k)
        if isinstance(v, str) and len(v) >= 10:
            return v[:10]
    return None

def get_equity(row: dict[str, Any]) -> float | None:
    for k in [
        "equity", "total_equity", "portfolio_value",
        "e1_equity", "e1r_direct_composed_equity",
    ]:
        v = as_float(row.get(k))
        if v is not None:
            return v
    return None

def normalize_backtest_e1(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    first = None
    for r in rows:
        d = get_date(r)
        e = as_float(r.get("equity") or r.get("portfolio_value") or r.get("total_equity"))
        if not d or e is None:
            continue
        if first is None:
            first = e
        out.append({
            "date": d,
            "strategy_id": "E1_AUDITED_G4_MINHOLD10",
            "curve_type": "backtest_5y",
            "canonical": True,
            "equity": e,
            "indexed": e / first * 100.0 if first else None,
        })
    return out

def normalize_backtest_e1r_from_comparison(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for r in rows:
        d = get_date(r)
        e = as_float(r.get("e1r_direct_composed_equity"))
        idx = as_float(r.get("e1r_direct_composed_indexed"))
        if not d or e is None:
            continue
        out.append({
            "date": d,
            "strategy_id": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE",
            "curve_type": "backtest_5y_candidate",
            "canonical": False,
            "warning": "NOT_FROZEN_E1R_V0_2",
            "equity": e,
            "indexed": idx,
        })
    return out

def normalize_e1_oos(obj: Any) -> list[dict[str, Any]]:
    rows = extract_rows(obj)
    out = []
    first = None
    for r in rows:
        d = get_date(r)
        e = as_float(r.get("equity") or r.get("portfolio_value") or r.get("total_equity"))
        if not d or e is None:
            continue
        if first is None:
            first = e
        out.append({
            "date": d,
            "strategy_id": "E1_AUDITED_G4_MINHOLD10",
            "curve_type": "forward_oos",
            "canonical": True,
            "equity": e,
            "indexed": e / first * 100.0 if first else None,
            "source": r.get("source"),
            "n_positions": r.get("n_positions"),
        })
    return out

def normalize_e1r_oos(obj: Any) -> list[dict[str, Any]]:
    rows = extract_rows(obj)
    out = []
    first = None
    for r in rows:
        d = get_date(r)
        e = as_float(r.get("portfolio_value") or r.get("equity") or r.get("total_equity"))
        if not d or e is None:
            continue
        if first is None:
            first = e
        out.append({
            "date": d,
            "strategy_id": r.get("strategy_id") or "E1R_REGIME_AWARE_V0_2",
            "curve_type": "forward_oos_kickoff_ready",
            "canonical": False,
            "warning": "E1R_FORWARD_KICKOFF_READY_NOT_OFFICIAL_LIVE",
            "equity": e,
            "indexed": as_float(r.get("strategy_indexed")) or (e / first * 100.0 if first else None),
            "official_kickoff_date": r.get("official_kickoff_date"),
            "market_state": r.get("market_state"),
            "regime": r.get("regime"),
            "subclass": r.get("subclass"),
            "gross_exposure": r.get("gross_exposure"),
            "core_exposure": r.get("core_exposure"),
            "sidecar_exposure": r.get("sidecar_exposure"),
        })
    return out

def curve_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    dates = [r["date"] for r in rows if r.get("date")]
    equities = [as_float(r.get("equity")) for r in rows if as_float(r.get("equity")) is not None]
    first = equities[0] if equities else None
    last = equities[-1] if equities else None
    return {
        "row_count": len(rows),
        "date_start": min(dates) if dates else None,
        "date_end": max(dates) if dates else None,
        "first_equity": first,
        "last_equity": last,
        "total_return_pct": (last / first - 1.0) * 100.0 if first and last else None,
    }

def main() -> int:
    baseline_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_before = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    e1_5y_obj = read_json_if_exists(E1_5Y)
    e1r_cmp_obj = read_json_if_exists(E1R_COMPARISON)
    e1_oos_obj = read_json_if_exists(E1_OOS)
    e1r_oos_obj = read_json_if_exists(E1R_OOS)

    e1_5y_rows = normalize_backtest_e1(extract_rows(e1_5y_obj))
    e1r_cmp_rows = extract_rows(e1r_cmp_obj)
    e1r_5y_rows = normalize_backtest_e1r_from_comparison(e1r_cmp_rows)
    e1_oos_rows = normalize_e1_oos(e1_oos_obj)
    e1r_oos_rows = normalize_e1r_oos(e1r_oos_obj)

    bundle = {
        "artifact_type": "e1_e1r_research_curve_bundle_noncanonical",
        "generated_at": now(),
        "canonical": False,
        "dashboard_ready": True,
        "official_e1r_canonical_ready": False,
        "warning": {
            "status": "RESEARCH_BUNDLE_NONCANONICAL",
            "e1r_backtest_warning": "E1R 5Y curve is direct-composed candidate and NOT frozen E1R v0.2.",
            "e1r_forward_warning": "E1R forward/OOS is KICKOFF_READY and not official live until daily pipeline succeeds.",
        },
        "sources": {
            "e1_5y": rel(E1_5Y),
            "e1r_5y_candidate_comparison": rel(E1R_COMPARISON),
            "e1_oos": rel(E1_OOS),
            "e1r_oos": rel(E1R_OOS),
        },
        "frozen_e1r_v0_2_target_metrics": FROZEN_TARGET,
        "curves": {
            "e1_5y_canonical": e1_5y_rows,
            "e1r_5y_direct_composed_candidate": e1r_5y_rows,
            "e1_forward_oos": e1_oos_rows,
            "e1r_forward_oos_kickoff_ready": e1r_oos_rows,
        },
        "summaries": {
            "e1_5y_canonical": curve_summary(e1_5y_rows),
            "e1r_5y_direct_composed_candidate": curve_summary(e1r_5y_rows),
            "e1_forward_oos": curve_summary(e1_oos_rows),
            "e1r_forward_oos_kickoff_ready": curve_summary(e1r_oos_rows),
        },
        "validations": {
            "e1_5y_rows_ge_1000": len(e1_5y_rows) >= 1000,
            "e1r_5y_candidate_rows_ge_1000": len(e1r_5y_rows) >= 1000,
            "e1_oos_exists": E1_OOS.exists(),
            "e1r_oos_exists": E1R_OOS.exists(),
            "official_e1r_canonical_absent": all(not p.exists() for p in CANONICAL_E1R_FILES),
            "bundle_noncanonical": True,
        },
    }

    write_json(OUT_BUNDLE, bundle)

    post_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_after = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    validations = bundle["validations"]
    if validations["e1_5y_rows_ge_1000"] and validations["e1r_5y_candidate_rows_ge_1000"]:
        conclusion = "RESEARCH_CURVE_BUNDLE_READY_FOR_DASHBOARD_CANDIDATE_WIRING"
        recommended = "Wire this bundle into dashboard under Research/Candidate labels only; do not label E1R as frozen official."
    else:
        conclusion = "RESEARCH_CURVE_BUNDLE_INCOMPLETE"
        recommended = "Do not wire dashboard until missing curve rows are fixed."

    report = {
        "generated_at": now(),
        "stage": "B_STAGE_3_8E2F2C4C10F4B0N_RESEARCH_CURVE_BUNDLE",
        "status": "E1_E1R_RESEARCH_CURVE_BUNDLE_COMPLETE_NONCANONICAL",
        "policy": {
            "dashboard_changed": False,
            "workflow_changed": False,
            "strategy_logic_changed": False,
            "e1r_canonical_written": False,
            "official_comparison_canonical_written": False,
            "full_backtest_rerun": False,
            "research_bundle_written": True,
        },
        "bundle_output_path": rel(OUT_BUNDLE),
        "bundle_output_exists": OUT_BUNDLE.exists(),
        "summaries": bundle["summaries"],
        "validations": validations,
        "conclusion": conclusion,
        "recommended_next_action": recommended,
        "strategy_files_unchanged": baseline_hashes == post_hashes,
        "canonical_existence_unchanged": canonical_before == canonical_after,
        "canonical_after": canonical_after,
        "next_stage": {
            "name": "Stage 3.8E-2F-2C-4C-10F-4B-0O",
            "title": "Wire research bundle into dashboard candidate panel",
            "recommended_action": recommended,
        },
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# Stage 3.8E-2F-2C-4C-10F-4B-0N Research Curve Bundle")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append("- Status: `E1_E1R_RESEARCH_CURVE_BUNDLE_COMPLETE_NONCANONICAL`")
    md.append("- Dashboard changed: `False`")
    md.append("- E1R canonical written: `False`")
    md.append("- Research bundle written: `True`")
    md.append("")
    md.append("## Bundle")
    md.append("")
    md.append(f"- `{rel(OUT_BUNDLE)}`")
    md.append("")
    md.append("## Summaries")
    md.append("")
    md.append("```json")
    md.append(json.dumps(bundle["summaries"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Validations")
    md.append("")
    md.append("```json")
    md.append(json.dumps(validations, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {recommended}")
    md.append("")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("Stage 3.8E-2F-2C-4C-10F-4B-0N research curve bundle complete")
    print("status:", report["status"])
    print("strategy_files_unchanged:", report["strategy_files_unchanged"])
    print("canonical_existence_unchanged:", report["canonical_existence_unchanged"])
    print("bundle_output_exists:", report["bundle_output_exists"])
    print("bundle_output_path:", report["bundle_output_path"])
    print("summaries:", json.dumps(bundle["summaries"], ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)
    print("next_stage:", report["next_stage"]["name"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
