#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
import importlib.util
import sys
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

E1_CORE = ROOT / "exports/e1_5y_backtest_equity_curve.json"
SIDECAR = ROOT / "exports/e1r_v0_2_sidecar_records_5y.json"

REPORT_JSON = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0L_DIRECT_COMPOSE_CANDIDATE_REPORT.json"
REPORT_MD = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0L_DIRECT_COMPOSE_CANDIDATE_REPORT.md"

OUT_NONCANONICAL = ROOT / "exports/e1r_v0_2_direct_composed_candidate_5y_noncanonical.json"

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
        for k in ["rows", "records", "daily_equity_records", "daily_records", "equity_curve", "curve"]:
            v = obj.get(k)
            if isinstance(v, list):
                return [x for x in v if isinstance(x, dict)]
    return []

def summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    dates = []
    for r in rows:
        d = r.get("date") or r.get("next_date") or r.get("interval_end_date")
        if isinstance(d, str) and len(d) >= 10:
            dates.append(d[:10])

    return {
        "row_count": len(rows),
        "unique_dates": len(set(dates)),
        "date_start": min(dates) if dates else None,
        "date_end": max(dates) if dates else None,
        "first_keys": sorted(rows[0].keys()) if rows else None,
        "first_row": rows[0] if rows else None,
        "last_row": rows[-1] if rows else None,
    }

def find_metric(obj: dict[str, Any], names: list[str]):
    for n in names:
        if n in obj:
            return obj[n]
    return None

def metric_values(obj: dict[str, Any]) -> dict[str, Any]:
    return {
        "total_return_pct": find_metric(obj, ["total_return_pct", "return_pct"]),
        "spx_return_pct": find_metric(obj, ["spx_return_pct", "spx_total_return_pct"]),
        "alpha_pct": find_metric(obj, ["alpha_pct"]),
        "max_drawdown_pct": find_metric(obj, ["max_drawdown_pct", "maxdd_pct"]),
        "profit_factor": find_metric(obj, ["profit_factor"]),
        "sharpe_ratio": find_metric(obj, ["sharpe_ratio", "sharpe"]),
    }

def metric_diffs(metrics: dict[str, Any]) -> dict[str, Any]:
    out = {}
    for k, target in TARGETS.items():
        v = as_float(metrics.get(k))
        out[k] = None if v is None else abs(v - target)
    return out

def import_composer():
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "src"))
    p = ROOT / "src/engine/e1r_composer.py"
    spec = importlib.util.spec_from_file_location("e1r_composer_4b0l", p)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import e1r_composer")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod

def build_core_variant_result(e1_obj: Any) -> dict[str, Any]:
    rows = extract_rows(e1_obj)
    metrics = metric_values(e1_obj if isinstance(e1_obj, dict) else {})
    return {
        "source": "exports/e1_5y_backtest_equity_curve.json",
        "candidate_input_type": "current_e1_5y_core_not_frozen_e1r_core",
        "daily_equity_records": rows,
        "daily_records": rows,
        "metrics": metrics,
        **{k: v for k, v in metrics.items() if v is not None},
    }

def build_sidecar_result(sidecar_obj: Any) -> dict[str, Any]:
    rows = extract_rows(sidecar_obj)
    return {
        "source": "exports/e1r_v0_2_sidecar_records_5y.json",
        "candidate_input_type": "validated_sidecar_records_5y",
        "sidecar_records": rows,
        "records": rows,
        "rows": rows,
    }

def main() -> int:
    baseline_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_before = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    e1_obj = read_json(E1_CORE)
    sidecar_obj = read_json(SIDECAR)

    core_input = build_core_variant_result(e1_obj)
    sidecar_input = build_sidecar_result(sidecar_obj)

    composer = import_composer()
    compose = getattr(composer, "compose_e1r_v0_2_variant")

    invocation = {
        "attempted": True,
        "ok": False,
        "error": None,
    }

    result = None
    try:
        result = compose(core_input, sidecar_input, 100000.0)
        invocation["ok"] = True
        invocation["result_type"] = type(result).__name__
        invocation["result_keys"] = sorted(result.keys()) if isinstance(result, dict) else None
    except Exception as exc:
        invocation["ok"] = False
        invocation["error"] = type(exc).__name__ + ": " + str(exc)

    output_written = False
    result_metrics = {}
    result_diffs = {}
    result_rows = []

    if isinstance(result, dict):
        result_metrics = metric_values(result)
        result_diffs = metric_diffs(result_metrics)
        result_rows = extract_rows(result)

        candidate_artifact = {
            "artifact_type": "e1r_v0_2_direct_composed_candidate_5y_noncanonical",
            "generated_at": now(),
            "canonical": False,
            "source_warning": "Composed from current E1 5Y core artifact + validated sidecar records; this is not yet proven to be frozen E1R core.",
            "inputs": {
                "core": {
                    "path": rel(E1_CORE),
                    "summary": summarize_rows(core_input["daily_equity_records"]),
                    "input_type": core_input["candidate_input_type"],
                    "metrics": core_input.get("metrics"),
                },
                "sidecar": {
                    "path": rel(SIDECAR),
                    "summary": summarize_rows(sidecar_input["records"]),
                    "input_type": sidecar_input["candidate_input_type"],
                },
            },
            "targets": TARGETS,
            "result_metrics": result_metrics,
            "result_metric_diffs_abs": result_diffs,
            "result_summary": {
                "keys": sorted(result.keys()),
                "rows_summary": summarize_rows(result_rows),
            },
            "result": result,
        }
        write_json(OUT_NONCANONICAL, candidate_artifact)
        output_written = True

    post_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_after = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    frozen_match = bool(result_diffs) and all(
        v is not None and v <= 0.001
        for v in result_diffs.values()
    )

    if invocation["ok"] and frozen_match:
        conclusion = "DIRECT_COMPOSE_MATCHED_FROZEN_E1R_METRICS_NONCANONICAL_READY_FOR_VALIDATION"
        recommended = "Validate row contract and then promote to canonical in a separate guarded step."
    elif invocation["ok"]:
        conclusion = "DIRECT_COMPOSE_SUCCEEDED_BUT_DID_NOT_MATCH_FROZEN_E1R_METRICS"
        recommended = "Use this result to quantify gap; frozen E1R core input is still not equal to current E1 5Y core."
    else:
        conclusion = "DIRECT_COMPOSE_INVOCATION_FAILED"
        recommended = "Inspect composer expected input schema and patch candidate input wrapper."

    report = {
        "generated_at": now(),
        "stage": "B_STAGE_3_8E2F2C4C10F4B0L_DIRECT_COMPOSE_CANDIDATE",
        "status": "E1R_DIRECT_COMPOSE_CANDIDATE_COMPLETE_NONCANONICAL",
        "policy": {
            "dashboard_changed": False,
            "workflow_changed": False,
            "strategy_logic_changed": False,
            "e1r_canonical_written": False,
            "portfolio_equity_composed": True,
            "full_backtest_rerun": False,
            "noncanonical_candidate_written": output_written,
        },
        "input_summaries": {
            "core": summarize_rows(core_input["daily_equity_records"]),
            "sidecar": summarize_rows(sidecar_input["records"]),
        },
        "invocation": invocation,
        "result_metrics": result_metrics,
        "result_metric_diffs_abs": result_diffs,
        "frozen_metric_exact_match": frozen_match,
        "candidate_output_path": rel(OUT_NONCANONICAL),
        "candidate_output_exists": OUT_NONCANONICAL.exists(),
        "conclusion": conclusion,
        "recommended_next_action": recommended,
        "strategy_files_unchanged": baseline_hashes == post_hashes,
        "canonical_existence_unchanged": canonical_before == canonical_after,
        "canonical_after": canonical_after,
        "next_stage": {
            "name": "Stage 3.8E-2F-2C-4C-10F-4B-0M",
            "title": "Validate direct composed noncanonical candidate or recover frozen core input",
            "recommended_action": recommended,
        },
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# Stage 3.8E-2F-2C-4C-10F-4B-0L Direct Compose Candidate")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append("- Status: `E1R_DIRECT_COMPOSE_CANDIDATE_COMPLETE_NONCANONICAL`")
    md.append("- E1R canonical written: `False`")
    md.append(f"- Noncanonical candidate written: `{output_written}`")
    md.append(f"- Strategy files unchanged: `{report['strategy_files_unchanged']}`")
    md.append(f"- Canonical existence unchanged: `{report['canonical_existence_unchanged']}`")
    md.append("")
    md.append("## Metrics")
    md.append("")
    md.append("```json")
    md.append(json.dumps({
        "result_metrics": result_metrics,
        "target_metrics": TARGETS,
        "diffs_abs": result_diffs,
        "frozen_metric_exact_match": frozen_match,
    }, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Input Summaries")
    md.append("")
    md.append("```json")
    md.append(json.dumps(report["input_summaries"], indent=2, ensure_ascii=False)[:12000])
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

    print("Stage 3.8E-2F-2C-4C-10F-4B-0L direct compose complete")
    print("status:", report["status"])
    print("strategy_files_unchanged:", report["strategy_files_unchanged"])
    print("canonical_existence_unchanged:", report["canonical_existence_unchanged"])
    print("invocation_ok:", invocation["ok"])
    print("invocation_error:", invocation.get("error"))
    print("candidate_output_exists:", report["candidate_output_exists"])
    print("candidate_output_path:", report["candidate_output_path"])
    print("input_summaries:", json.dumps(report["input_summaries"], ensure_ascii=False))
    print("result_metrics:", json.dumps(result_metrics, ensure_ascii=False))
    print("result_metric_diffs_abs:", json.dumps(result_diffs, ensure_ascii=False))
    print("frozen_metric_exact_match:", frozen_match)
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)
    print("next_stage:", report["next_stage"]["name"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
