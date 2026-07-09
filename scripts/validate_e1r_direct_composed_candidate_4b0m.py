#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone
from collections import Counter
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

E1_CORE = ROOT / "exports/e1_5y_backtest_equity_curve.json"
E1R_CANDIDATE = ROOT / "exports/e1r_v0_2_direct_composed_candidate_5y_noncanonical.json"

OUT_COMPARISON = ROOT / "exports/e1_vs_e1r_direct_composed_5y_comparison_noncanonical.json"

REPORT_JSON = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0M_DIRECT_COMPOSED_CANDIDATE_VALIDATION.json"
REPORT_MD = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0M_DIRECT_COMPOSED_CANDIDATE_VALIDATION.md"

FROZEN_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

CANONICAL_E1R_FILES = [
    ROOT / "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
    ROOT / "exports/e1_e1r_5y_equity_comparison.json",
]

TARGETS = {
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

def read_json(p: Path) -> Any:
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
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]

    if isinstance(obj, dict):
        # Direct-composed candidate stores composer result under result.
        if isinstance(obj.get("result"), dict):
            r = obj["result"]
            for k in ["daily_equity_records", "daily_records", "rows", "records", "equity_curve", "curve"]:
                v = r.get(k)
                if isinstance(v, list):
                    return [x for x in v if isinstance(x, dict)]

        for k in ["daily_equity_records", "daily_records", "rows", "records", "equity_curve", "curve"]:
            v = obj.get(k)
            if isinstance(v, list):
                return [x for x in v if isinstance(x, dict)]

    return []

def get_date(row: dict[str, Any]) -> str | None:
    for k in ["date", "interval_end_date", "next_date"]:
        v = row.get(k)
        if isinstance(v, str) and len(v) >= 10:
            return v[:10]
    return None

def get_equity(row: dict[str, Any]) -> float | None:
    for k in ["total_equity", "portfolio_value", "equity", "strategy_equity"]:
        v = as_float(row.get(k))
        if v is not None:
            return v
    return None

def get_return(row: dict[str, Any]) -> float | None:
    for k in ["daily_return", "combined_return"]:
        v = as_float(row.get(k))
        if v is not None:
            return v
    for k in ["daily_return_pct", "combined_return_pct"]:
        v = as_float(row.get(k))
        if v is not None:
            return v / 100.0
    return None

def max_drawdown_pct(equities: list[float]) -> float | None:
    if not equities:
        return None
    peak = equities[0]
    worst = 0.0
    for v in equities:
        peak = max(peak, v)
        if peak > 0:
            worst = min(worst, v / peak - 1.0)
    return abs(worst * 100.0)

def summarize_curve(rows: list[dict[str, Any]]) -> dict[str, Any]:
    parsed = []
    for row in rows:
        d = get_date(row)
        e = get_equity(row)
        if d and e is not None:
            parsed.append((d, e, row))

    dates = [x[0] for x in parsed]
    dc = Counter(dates)
    equities = [x[1] for x in parsed]

    first_eq = equities[0] if equities else None
    last_eq = equities[-1] if equities else None
    total_return = (last_eq / first_eq - 1.0) * 100.0 if first_eq and last_eq else None

    symbol_count = sum(1 for _, _, r in parsed if "symbol" in r or "ticker" in r)
    diagnostic_count = sum(1 for _, _, r in parsed if r.get("diagnostic_only") is True)

    return {
        "row_count": len(rows),
        "parseable_rows": len(parsed),
        "unique_dates": len(set(dates)),
        "date_start": min(dates) if dates else None,
        "date_end": max(dates) if dates else None,
        "max_rows_per_date": max(dc.values()) if dc else None,
        "one_row_per_date": bool(dc) and max(dc.values()) == 1 and len(parsed) == len(set(dates)),
        "symbol_row_count": symbol_count,
        "diagnostic_only_row_count": diagnostic_count,
        "not_symbol_level": symbol_count == 0,
        "not_diagnostic_only": diagnostic_count == 0,
        "first_equity": first_eq,
        "last_equity": last_eq,
        "total_return_pct_from_rows": total_return,
        "max_drawdown_pct_from_rows": max_drawdown_pct(equities),
        "first_row_keys": sorted(rows[0].keys()) if rows else None,
        "first_row": rows[0] if rows else None,
        "last_row": rows[-1] if rows else None,
    }

def normalize_curve(rows: list[dict[str, Any]], label: str) -> list[dict[str, Any]]:
    out = []
    first_equity = None
    for row in rows:
        d = get_date(row)
        e = get_equity(row)
        r = get_return(row)
        if not d or e is None:
            continue
        if first_equity is None:
            first_equity = e
        out.append({
            "date": d,
            f"{label}_equity": e,
            f"{label}_indexed": e / first_equity * 100.0 if first_equity else None,
            f"{label}_daily_return": r,
        })
    return out

def metrics_from_candidate(obj: dict[str, Any]) -> dict[str, Any]:
    if isinstance(obj.get("result_metrics"), dict):
        return obj["result_metrics"]
    if isinstance(obj.get("result"), dict):
        r = obj["result"]
        return {
            "total_return_pct": r.get("total_return_pct"),
            "spx_return_pct": r.get("spx_return_pct"),
            "alpha_pct": r.get("alpha_pct"),
            "max_drawdown_pct": r.get("max_drawdown_pct"),
            "profit_factor": r.get("profit_factor"),
            "sharpe_ratio": r.get("sharpe_ratio"),
        }
    return {}

def diff_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    out = {}
    for k, target in TARGETS.items():
        v = as_float(metrics.get(k))
        out[k] = None if v is None else abs(v - target)
    return out

def main() -> int:
    baseline_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_before = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    e1_obj = read_json(E1_CORE)
    e1r_obj = read_json(E1R_CANDIDATE)

    e1_rows = extract_rows(e1_obj)
    e1r_rows = extract_rows(e1r_obj)

    e1_summary = summarize_curve(e1_rows)
    e1r_summary = summarize_curve(e1r_rows)

    e1_norm = normalize_curve(e1_rows, "e1")
    e1r_norm = normalize_curve(e1r_rows, "e1r_direct_composed")

    e1_by_date = {r["date"]: r for r in e1_norm}
    e1r_by_date = {r["date"]: r for r in e1r_norm}
    shared_dates = sorted(set(e1_by_date) & set(e1r_by_date))

    comparison_rows = []
    for d in shared_dates:
        comparison_rows.append({
            "date": d,
            **e1_by_date[d],
            **e1r_by_date[d],
            "e1r_minus_e1_indexed": (
                e1r_by_date[d]["e1r_direct_composed_indexed"] - e1_by_date[d]["e1_indexed"]
                if e1r_by_date[d].get("e1r_direct_composed_indexed") is not None and e1_by_date[d].get("e1_indexed") is not None
                else None
            ),
        })

    result_metrics = metrics_from_candidate(e1r_obj)
    diffs = diff_metrics(result_metrics)

    validations = {
        "noncanonical_only": True,
        "e1r_one_row_per_date": e1r_summary["one_row_per_date"],
        "e1r_not_symbol_level": e1r_summary["not_symbol_level"],
        "e1r_not_diagnostic_only": e1r_summary["not_diagnostic_only"],
        "e1r_row_count_ge_1000": e1r_summary["parseable_rows"] >= 1000,
        "shared_dates_ge_1000": len(shared_dates) >= 1000,
        "frozen_metric_exact_match": bool(diffs) and all(v is not None and v <= 0.001 for v in diffs.values()),
        "explicit_not_frozen_warning_required": True,
    }

    artifact = {
        "artifact_type": "e1_vs_e1r_direct_composed_5y_comparison_noncanonical",
        "generated_at": now(),
        "canonical": False,
        "dashboard_ready": False,
        "warning": {
            "status": "NOT_FROZEN_E1R_V0_2",
            "reason": "Direct-composed candidate uses current E1 5Y core + validated sidecar records. It does not match frozen E1R v0.2 metrics.",
            "frozen_total_return_pct": TARGETS["total_return_pct"],
            "candidate_total_return_pct": result_metrics.get("total_return_pct"),
            "total_return_gap_pct": diffs.get("total_return_pct"),
        },
        "inputs": {
            "e1_core": rel(E1_CORE),
            "e1r_direct_composed_candidate": rel(E1R_CANDIDATE),
        },
        "summaries": {
            "e1": e1_summary,
            "e1r_direct_composed": e1r_summary,
            "shared_dates": {
                "count": len(shared_dates),
                "date_start": shared_dates[0] if shared_dates else None,
                "date_end": shared_dates[-1] if shared_dates else None,
            },
        },
        "target_metrics_frozen_e1r_v0_2": TARGETS,
        "candidate_metrics": result_metrics,
        "candidate_metric_diffs_abs": diffs,
        "validations": validations,
        "rows": comparison_rows,
    }

    write_json(OUT_COMPARISON, artifact)

    post_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_after = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    if all([
        validations["e1r_one_row_per_date"],
        validations["e1r_not_symbol_level"],
        validations["e1r_not_diagnostic_only"],
        validations["e1r_row_count_ge_1000"],
        validations["shared_dates_ge_1000"],
    ]) and not validations["frozen_metric_exact_match"]:
        conclusion = "DIRECT_COMPOSED_CANDIDATE_CURVE_VALID_BUT_NOT_FROZEN_E1R"
        recommended = "Use this noncanonical curve for engineering validation only; continue frozen core recovery separately."
    elif validations["frozen_metric_exact_match"]:
        conclusion = "DIRECT_COMPOSED_CANDIDATE_MATCHES_FROZEN_E1R_READY_FOR_CANONICAL_REVIEW"
        recommended = "Promote only after separate canonical review."
    else:
        conclusion = "DIRECT_COMPOSED_CANDIDATE_FAILED_CURVE_CONTRACT"
        recommended = "Do not use candidate curve; inspect composer output row schema."

    report = {
        "generated_at": now(),
        "stage": "B_STAGE_3_8E2F2C4C10F4B0M_DIRECT_COMPOSED_CANDIDATE_VALIDATION",
        "status": "E1R_DIRECT_COMPOSED_CANDIDATE_VALIDATION_COMPLETE_NONCANONICAL",
        "policy": {
            "dashboard_changed": False,
            "workflow_changed": False,
            "strategy_logic_changed": False,
            "e1r_canonical_written": False,
            "comparison_canonical_written": False,
            "full_backtest_rerun": False,
            "noncanonical_comparison_written": True,
        },
        "comparison_output_path": rel(OUT_COMPARISON),
        "comparison_output_exists": OUT_COMPARISON.exists(),
        "summaries": artifact["summaries"],
        "target_metrics_frozen_e1r_v0_2": TARGETS,
        "candidate_metrics": result_metrics,
        "candidate_metric_diffs_abs": diffs,
        "validations": validations,
        "conclusion": conclusion,
        "recommended_next_action": recommended,
        "strategy_files_unchanged": baseline_hashes == post_hashes,
        "canonical_existence_unchanged": canonical_before == canonical_after,
        "canonical_after": canonical_after,
        "next_stage": {
            "name": "Stage 3.8E-2F-2C-4C-10F-4B-0N",
            "title": "Prepare dashboard research candidate curve or continue frozen core recovery",
            "recommended_action": recommended,
        },
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# Stage 3.8E-2F-2C-4C-10F-4B-0M Direct-Composed Candidate Validation")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append("- Status: `E1R_DIRECT_COMPOSED_CANDIDATE_VALIDATION_COMPLETE_NONCANONICAL`")
    md.append("- E1R canonical written: `False`")
    md.append("- Dashboard changed: `False`")
    md.append("- Noncanonical comparison written: `True`")
    md.append(f"- Strategy files unchanged: `{report['strategy_files_unchanged']}`")
    md.append(f"- Canonical existence unchanged: `{report['canonical_existence_unchanged']}`")
    md.append("")
    md.append("## Warning")
    md.append("")
    md.append("- `NOT_FROZEN_E1R_V0_2`")
    md.append(f"- Candidate total return: `{result_metrics.get('total_return_pct')}`")
    md.append(f"- Frozen total return: `{TARGETS['total_return_pct']}`")
    md.append(f"- Gap: `{diffs.get('total_return_pct')}` pct")
    md.append("")
    md.append("## Validations")
    md.append("")
    md.append("```json")
    md.append(json.dumps(validations, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Summaries")
    md.append("")
    md.append("```json")
    md.append(json.dumps(artifact["summaries"], indent=2, ensure_ascii=False)[:16000])
    md.append("```")
    md.append("")
    md.append("## Metrics")
    md.append("")
    md.append("```json")
    md.append(json.dumps({
        "frozen_target": TARGETS,
        "candidate": result_metrics,
        "diffs_abs": diffs,
    }, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {recommended}")
    md.append("")
    md.append("## Next Stage")
    md.append("")
    md.append(f"- `{report['next_stage']['name']}`: {report['next_stage']['title']}")
    md.append(f"- Recommended action: {report['next_stage']['recommended_action']}")
    md.append("")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("Stage 3.8E-2F-2C-4C-10F-4B-0M validation complete")
    print("status:", report["status"])
    print("strategy_files_unchanged:", report["strategy_files_unchanged"])
    print("canonical_existence_unchanged:", report["canonical_existence_unchanged"])
    print("comparison_output_exists:", report["comparison_output_exists"])
    print("comparison_output_path:", report["comparison_output_path"])
    print("summaries:", json.dumps(report["summaries"], ensure_ascii=False))
    print("candidate_metrics:", json.dumps(result_metrics, ensure_ascii=False))
    print("candidate_metric_diffs_abs:", json.dumps(diffs, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)
    print("next_stage:", report["next_stage"]["name"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
