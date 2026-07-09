#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone
from collections import Counter
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REPORT_JSON = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.json"
REPORT_MD = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.md"

FROZEN_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

CANONICAL_E1R_FILES = [
    ROOT / "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
    ROOT / "exports/e1_e1r_5y_equity_comparison.json",
]

SEARCH_ROOTS = [
    ROOT / "docs/research",
    ROOT / "exports",
    ROOT / "data/research",
]

TARGETS = {
    "total_return_pct": 116.7435999134756,
    "spx_return_pct": 76.844174428316,
    "alpha_pct": 39.89942548515961,
    "max_drawdown_pct": 25.904809362815108,
    "profit_factor": 1.1919630955509348,
    "sharpe_ratio": 0.7957270568329264,
}

CORE_HINTS = [
    "core_variant_result",
    "run_strategy_variant_comparison",
    "run_stateful_simulation",
    "daily_equity_records",
    "trades",
    "orders",
    "positions",
    "total_return_pct",
    "profit_factor",
    "sharpe_ratio",
]

SIDECAR_HINTS = [
    "sidecar_result",
    "sidecar_records",
    "sidecar_active",
    "sidecar_return",
    "sidecar_holdings",
    "MA_CONFLICT",
    "gross_exposure",
    "portfolio_return",
]

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

def norm_date(x: Any) -> str | None:
    if x is None:
        return None
    s = str(x)
    if len(s) >= 10 and s[4:5] == "-" and s[7:8] == "-":
        return s[:10]
    return None

def summarize_list(rows: list[Any]) -> dict[str, Any]:
    out = {
        "len": len(rows),
        "first_type": type(rows[0]).__name__ if rows else None,
    }
    if rows and isinstance(rows[0], dict):
        out["first_keys"] = sorted(rows[0].keys())[:120]
        out["first_sample"] = rows[0]
        out["last_sample"] = rows[-1]

        dates = []
        for r in rows:
            if not isinstance(r, dict):
                continue
            for k in ["date", "next_date", "interval_end_date", "core_end_date"]:
                d = norm_date(r.get(k))
                if d:
                    dates.append(d)
                    break
        if dates:
            dc = Counter(dates)
            out["unique_dates"] = len(set(dates))
            out["date_start"] = min(dates)
            out["date_end"] = max(dates)
            out["max_rows_per_date"] = max(dc.values())
            out["one_row_per_date_candidate"] = max(dc.values()) == 1 and len(dates) == len(set(dates))
    return out

def summarize_node(node: Any) -> dict[str, Any]:
    if isinstance(node, dict):
        out = {
            "type": "dict",
            "len": len(node),
            "keys": sorted(node.keys())[:180],
        }

        metric_like = {}
        for k in [
            "strategy_id",
            "name",
            "version",
            "status",
            "total_return_pct",
            "spx_return_pct",
            "spx_total_return_pct",
            "alpha_pct",
            "max_drawdown_pct",
            "profit_factor",
            "sharpe_ratio",
            "number_of_trades",
            "total_trades_all",
            "simulation_start_date",
            "simulation_end_date",
            "simulation_days",
            "daily_equity_record_count",
            "e1r_candidate_count",
            "e1r_uptrend_execution_enabled",
            "active_count",
            "records_count",
            "row_count",
            "sidecar_active_count",
        ]:
            if k in node:
                metric_like[k] = node.get(k)
        if metric_like:
            out["metric_like_values"] = metric_like

        child_summaries = {}
        for k, v in node.items():
            if isinstance(v, list):
                child_summaries[k] = summarize_list(v)
            elif isinstance(v, dict):
                child_summaries[k] = {
                    "type": "dict",
                    "keys": sorted(v.keys())[:120],
                    "len": len(v),
                }
                child_metric = {
                    kk: v.get(kk)
                    for kk in [
                        "total_return_pct",
                        "spx_return_pct",
                        "alpha_pct",
                        "max_drawdown_pct",
                        "profit_factor",
                        "sharpe_ratio",
                        "daily_equity_record_count",
                        "active_count",
                        "records_count",
                    ]
                    if kk in v
                }
                if child_metric:
                    child_summaries[k]["metric_like_values"] = child_metric
        out["children"] = child_summaries
        return out

    if isinstance(node, list):
        return {"type": "list", **summarize_list(node)}

    return {"type": type(node).__name__, "repr": repr(node)[:1000]}

def metric_diffs(node: Any) -> dict[str, Any]:
    if not isinstance(node, dict):
        return {"matched": {}, "diffs": {}, "exact_metric_match": False}

    matched = {}
    diffs = {}
    for k, target in TARGETS.items():
        if k in node:
            v = as_float(node.get(k))
            if v is not None:
                matched[k] = v
                diffs[k] = abs(v - target)

    exact = len(matched) == len(TARGETS) and all(v <= 0.001 for v in diffs.values())
    return {"matched": matched, "diffs": diffs, "exact_metric_match": exact}

def score_core_candidate(node: Any, path: str) -> int:
    if not isinstance(node, dict):
        return -9999

    keys = set(node.keys())
    text_keys = " ".join(keys).lower()
    score = 0

    if "core_variant_result" in path:
        score += 200
    if "metrics" in keys:
        score += 30
    if "daily_equity_records" in keys:
        score += 80
    if "daily_records" in keys:
        score += 60
    if "equity_curve" in keys:
        score += 50
    if "trades" in keys:
        score += 20
    if "orders" in keys:
        score += 20
    if "total_return_pct" in keys:
        score += 30
    if "profit_factor" in keys:
        score += 20
    if "sharpe_ratio" in keys:
        score += 20
    if "run_strategy_variant_comparison" in path:
        score += 30
    if "variant" in text_keys:
        score += 10

    # Frozen metric exact match is likely full E1R summary, not core input; keep but don't overrate.
    md = metric_diffs(node)
    if md["exact_metric_match"]:
        score += 20

    return score

def score_sidecar_candidate(node: Any, path: str) -> int:
    if not isinstance(node, dict):
        return -9999

    keys = set(node.keys())
    text_keys = " ".join(keys).lower()
    score = 0

    if "sidecar_result" in path:
        score += 200
    if "sidecar_records" in keys or "records" in keys or "rows" in keys:
        score += 80
    if "active_count" in keys or "sidecar_active_count" in keys:
        score += 50
    if "sidecar_active_by_regime" in keys:
        score += 50
    if "sidecar_active_by_subclass" in keys:
        score += 50
    if "gross_exposure" in text_keys:
        score += 20
    if "ma_conflict" in str(node).lower()[:20000]:
        score += 30
    if "sidecar" in text_keys or "sidecar" in path:
        score += 30

    return score

def collect_json_files() -> list[Path]:
    files = []
    for root in SEARCH_ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*.json"):
            if not p.is_file():
                continue
            if p.stat().st_size > 25_000_000:
                continue
            files.append(p)
    return sorted(files)

def walk_json(node: Any, source_file: str, path: str = "$", depth: int = 0, max_depth: int = 10) -> list[dict[str, Any]]:
    if depth > max_depth:
        return []

    out = []

    if isinstance(node, dict):
        keys = set(node.keys())
        path_l = path.lower()
        keys_l = " ".join(keys).lower()

        is_named_core = "core_variant_result" in path_l
        is_named_sidecar = "sidecar_result" in path_l

        core_hint_hit = is_named_core or any(h.lower() in keys_l for h in CORE_HINTS)
        sidecar_hint_hit = is_named_sidecar or any(h.lower() in keys_l for h in SIDECAR_HINTS)

        if core_hint_hit or sidecar_hint_hit:
            summary = summarize_node(node)
            md = metric_diffs(node)
            out.append({
                "source_file": source_file,
                "json_path": path,
                "is_named_core_variant_result": is_named_core,
                "is_named_sidecar_result": is_named_sidecar,
                "core_score": score_core_candidate(node, path),
                "sidecar_score": score_sidecar_candidate(node, path),
                "metric_match": md,
                "summary": summary,
            })

        for k, v in node.items():
            if isinstance(v, (dict, list)):
                out.extend(walk_json(v, source_file, f"{path}.{k}", depth + 1, max_depth))

    elif isinstance(node, list):
        # Only sample first 30 items to control size.
        for i, v in enumerate(node[:30]):
            if isinstance(v, (dict, list)):
                out.extend(walk_json(v, source_file, f"{path}[{i}]", depth + 1, max_depth))

    return out

def main() -> int:
    baseline_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_before = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    files = collect_json_files()
    all_nodes = []
    file_errors = []

    for p in files:
        try:
            obj = read_json(p)
            all_nodes.extend(walk_json(obj, rel(p)))
        except Exception as exc:
            file_errors.append({
                "path": rel(p),
                "error": type(exc).__name__ + ": " + str(exc),
            })

    core_candidates = sorted(
        [n for n in all_nodes if n["core_score"] > 0],
        key=lambda x: (-x["core_score"], x["source_file"], x["json_path"]),
    )[:60]

    sidecar_candidates = sorted(
        [n for n in all_nodes if n["sidecar_score"] > 0],
        key=lambda x: (-x["sidecar_score"], x["source_file"], x["json_path"]),
    )[:60]

    exact_metric_nodes = [
        n for n in all_nodes
        if n.get("metric_match", {}).get("exact_metric_match")
    ][:30]

    named_core = [
        n for n in all_nodes
        if n["is_named_core_variant_result"]
    ][:30]

    named_sidecar = [
        n for n in all_nodes
        if n["is_named_sidecar_result"]
    ][:30]

    post_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_after = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    conclusion = "COMPOSER_INPUT_CANDIDATES_AUDITED"
    recommended = "If a high-confidence core and sidecar input pair is found, run a no-write direct invocation probe of compose_e1r_v0_2_variant in the next step."

    if not named_core:
        conclusion = "CORE_VARIANT_RESULT_INPUT_NOT_PERSISTED_BY_NAME"
        recommended = "Instrument the call site that originally builds core_variant_result, because no persisted named core_variant_result was found."
    elif not named_sidecar:
        conclusion = "SIDECAR_RESULT_INPUT_NOT_PERSISTED_BY_NAME"
        recommended = "Build sidecar_result from the validated sidecar records artifact or instrument the composer call site."
    elif named_core and named_sidecar:
        conclusion = "NAMED_CORE_AND_SIDECAR_INPUT_CANDIDATES_FOUND"
        recommended = "Next step can attempt direct no-write compose_e1r_v0_2_variant invocation with the highest-confidence named candidates."

    report = {
        "generated_at": now(),
        "stage": "B_STAGE_3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES",
        "status": "E1R_COMPOSER_INPUT_CANDIDATES_AUDIT_COMPLETE_NO_INVOCATION",
        "policy": {
            "dashboard_changed": False,
            "workflow_changed": False,
            "strategy_logic_changed": False,
            "e1r_canonical_written": False,
            "portfolio_equity_composed": False,
            "full_backtest_rerun": False,
            "composer_invoked": False,
            "candidate_extracted": False,
        },
        "search_summary": {
            "json_files_scanned": len(files),
            "node_candidates_found": len(all_nodes),
            "file_error_count": len(file_errors),
            "core_candidate_count": len(core_candidates),
            "sidecar_candidate_count": len(sidecar_candidates),
            "named_core_candidate_count": len(named_core),
            "named_sidecar_candidate_count": len(named_sidecar),
            "exact_metric_node_count": len(exact_metric_nodes),
        },
        "top_core_candidates": core_candidates[:25],
        "top_sidecar_candidates": sidecar_candidates[:25],
        "named_core_candidates": named_core[:20],
        "named_sidecar_candidates": named_sidecar[:20],
        "exact_metric_nodes": exact_metric_nodes[:20],
        "file_errors": file_errors[:20],
        "conclusion": conclusion,
        "recommended_next_action": recommended,
        "strategy_files_unchanged": baseline_hashes == post_hashes,
        "canonical_existence_unchanged": canonical_before == canonical_after,
        "canonical_after": canonical_after,
        "next_stage": {
            "name": "Stage 3.8E-2F-2C-4C-10F-4B-0J",
            "title": "Direct no-write compose invocation or call-site instrumentation",
            "recommended_action": recommended,
        },
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# Stage 3.8E-2F-2C-4C-10F-4B-0I Composer Input Candidates")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append("- Status: `E1R_COMPOSER_INPUT_CANDIDATES_AUDIT_COMPLETE_NO_INVOCATION`")
    md.append("- Composer invoked: `False`")
    md.append("- Candidate extracted: `False`")
    md.append("- E1R canonical written: `False`")
    md.append(f"- Strategy files unchanged: `{report['strategy_files_unchanged']}`")
    md.append(f"- Canonical existence unchanged: `{report['canonical_existence_unchanged']}`")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append("```json")
    md.append(json.dumps(report["search_summary"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {recommended}")
    md.append("")
    md.append("## Top Core Candidates")
    md.append("")
    md.append("```json")
    md.append(json.dumps(core_candidates[:12], indent=2, ensure_ascii=False)[:24000])
    md.append("```")
    md.append("")
    md.append("## Top Sidecar Candidates")
    md.append("")
    md.append("```json")
    md.append(json.dumps(sidecar_candidates[:12], indent=2, ensure_ascii=False)[:24000])
    md.append("```")
    md.append("")
    md.append("## Named Core Candidates")
    md.append("")
    md.append("```json")
    md.append(json.dumps(named_core[:10], indent=2, ensure_ascii=False)[:16000])
    md.append("```")
    md.append("")
    md.append("## Named Sidecar Candidates")
    md.append("")
    md.append("```json")
    md.append(json.dumps(named_sidecar[:10], indent=2, ensure_ascii=False)[:16000])
    md.append("```")
    md.append("")
    md.append("## Exact Metric Nodes")
    md.append("")
    md.append("```json")
    md.append(json.dumps(exact_metric_nodes[:10], indent=2, ensure_ascii=False)[:16000])
    md.append("```")
    md.append("")
    md.append("## Next Stage")
    md.append("")
    md.append(f"- `{report['next_stage']['name']}`: {report['next_stage']['title']}")
    md.append(f"- Recommended action: {report['next_stage']['recommended_action']}")
    md.append("")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("Stage 3.8E-2F-2C-4C-10F-4B-0I composer input candidate audit complete")
    print("status:", report["status"])
    print("strategy_files_unchanged:", report["strategy_files_unchanged"])
    print("canonical_existence_unchanged:", report["canonical_existence_unchanged"])
    print("summary:", json.dumps(report["search_summary"], ensure_ascii=False))
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)

    if core_candidates:
        c = core_candidates[0]
        print("top_core_source:", c["source_file"])
        print("top_core_path:", c["json_path"])
        print("top_core_score:", c["core_score"])
        print("top_core_summary:", json.dumps(c["summary"].get("metric_like_values", {}), ensure_ascii=False))

    if sidecar_candidates:
        s = sidecar_candidates[0]
        print("top_sidecar_source:", s["source_file"])
        print("top_sidecar_path:", s["json_path"])
        print("top_sidecar_score:", s["sidecar_score"])
        print("top_sidecar_summary:", json.dumps(s["summary"].get("metric_like_values", {}), ensure_ascii=False))

    print("next_stage:", report["next_stage"]["name"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
