#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

TRACE_REPORT = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json"

REPORT_JSON = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0E_LITE_GENERATOR_DRY_RUN_REPORT.json"
REPORT_MD = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0E_LITE_GENERATOR_DRY_RUN_REPORT.md"

FROZEN_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

# Files that the historical generator may write.
# They are backed up, inspected after the run, then restored/deleted.
MUTABLE_OUTPUTS = [
    ROOT / "exports/e1r_v0_2_backtest_summary.json",
    ROOT / "exports/e1r_v0_2_backtest_equity_curve.json",
    ROOT / "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
    ROOT / "exports/e1_e1r_5y_equity_comparison.json",
    ROOT / "data/research/e1r/e1r_formal_backtest_v0_1.json",
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

TIMEOUT_SECONDS = 2400

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))

def read_json(p: Path) -> Any:
    return json.loads(p.read_text())

def write_json(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def sha256(p: Path) -> str | None:
    if not p.exists():
        return None
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def as_float(x: Any, default=None):
    try:
        if x is None:
            return default
        return float(x)
    except Exception:
        return default

def summarize_json_node(node: Any, max_depth: int = 3) -> dict[str, Any]:
    if isinstance(node, dict):
        out = {
            "type": "dict",
            "len": len(node),
            "keys": sorted(node.keys())[:160],
        }
        metric_like = {
            k: node.get(k)
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
                "daily_equity_record_count",
                "simulation_start_date",
                "simulation_end_date",
                "simulation_days",
                "e1r_candidate_count",
                "e1r_uptrend_execution_enabled",
            ]
            if k in node
        }
        if metric_like:
            out["metric_like_values"] = metric_like

        for k, v in node.items():
            if isinstance(v, list):
                out[f"{k}_len"] = len(v)
                if v and isinstance(v[0], dict):
                    out[f"{k}_first_keys"] = sorted(v[0].keys())[:120]
                    out[f"{k}_first"] = v[0]
                    out[f"{k}_last"] = v[-1]
            elif isinstance(v, dict) and max_depth > 0:
                child_metric = {
                    kk: v.get(kk)
                    for kk in [
                        "strategy_id",
                        "name",
                        "total_return_pct",
                        "spx_return_pct",
                        "alpha_pct",
                        "max_drawdown_pct",
                        "profit_factor",
                        "sharpe_ratio",
                        "number_of_trades",
                        "daily_equity_record_count",
                        "e1r_candidate_count",
                        "e1r_uptrend_execution_enabled",
                    ]
                    if kk in v
                }
                out[f"{k}_dict_keys"] = sorted(v.keys())[:120]
                if child_metric:
                    out[f"{k}_dict_metric_like_values"] = child_metric
        return out

    if isinstance(node, list):
        out = {
            "type": "list",
            "len": len(node),
            "first_type": type(node[0]).__name__ if node else None,
        }
        if node and isinstance(node[0], dict):
            out["first_keys"] = sorted(node[0].keys())[:120]
            out["first"] = node[0]
            out["last"] = node[-1]
        return out

    return {"type": type(node).__name__, "repr": repr(node)[:1000]}

def walk_for_nodes(node: Any, path: str = "$", depth: int = 0, max_depth: int = 8) -> list[dict[str, Any]]:
    if depth > max_depth:
        return []

    results = []

    if isinstance(node, dict):
        keys = set(node.keys())

        wanted = {
            "metrics",
            "core_variant_result",
            "sidecar_result",
            "daily_equity_records",
            "daily_records",
            "equity_curve",
            "variant_results",
            "records",
            "rows",
            "trades",
            "orders",
        }

        metric_hit = any(k in node for k in TARGETS)
        key_hit = bool(keys.intersection(wanted))

        if metric_hit or key_hit:
            diffs = {}
            matched = {}
            for k, target in TARGETS.items():
                if k in node:
                    val = as_float(node.get(k))
                    if val is not None:
                        matched[k] = val
                        diffs[k] = abs(val - target)

            results.append({
                "path": path,
                "matched_keys": sorted(keys.intersection(wanted)),
                "matched_metrics": matched,
                "target_diffs_abs": diffs,
                "summary": summarize_json_node(node),
            })

        for k, v in node.items():
            if isinstance(v, (dict, list)):
                results.extend(walk_for_nodes(v, f"{path}.{k}", depth + 1, max_depth))

    elif isinstance(node, list):
        for i, v in enumerate(node[:100]):
            if isinstance(v, (dict, list)):
                results.extend(walk_for_nodes(v, f"{path}[{i}]", depth + 1, max_depth))

    return results

def select_generator_candidate() -> dict[str, Any]:
    if not TRACE_REPORT.exists():
        fallback = ROOT / "scripts/export_e1r_v0_2_backtest_equity.py"
        return {
            "path": rel(fallback),
            "source": "fallback",
            "reason": "trace report missing",
        }

    trace = read_json(TRACE_REPORT)
    candidates = trace.get("generator_candidates") or []

    py_candidates = [
        c for c in candidates
        if str(c.get("path", "")).endswith(".py")
        and Path(ROOT / c["path"]).exists()
    ]

    # Prefer scripts over docs-generated probes, and prefer candidates mentioning composer.
    def score(c):
        p = c.get("path", "")
        terms = set(c.get("matched_terms") or [])
        s = int(c.get("generator_score") or 0)
        if p.startswith("scripts/"):
            s += 1000
        if "compose_e1r_v0_2_variant" in terms:
            s += 200
        if "core_variant_result" in terms:
            s += 100
        if "sidecar_result" in terms:
            s += 100
        if "e1r_v0_2_backtest_summary.json" in terms:
            s += 100
        return s

    if py_candidates:
        chosen = sorted(py_candidates, key=lambda c: (-score(c), c.get("path", "")))[0]
        chosen = dict(chosen)
        chosen["source"] = "4B-0D generator_candidates"
        chosen["selection_score"] = score(chosen)
        return chosen

    fallback = ROOT / "scripts/export_e1r_v0_2_backtest_equity.py"
    return {
        "path": rel(fallback),
        "source": "fallback",
        "reason": "no python candidate found in trace report",
    }

def backup_outputs(tmpdir: Path) -> dict[str, Any]:
    backup = {}

    for p in MUTABLE_OUTPUTS:
        entry = {
            "path": rel(p),
            "existed_before": p.exists(),
            "hash_before": sha256(p),
            "backup_path": None,
        }

        if p.exists():
            bp = tmpdir / rel(p)
            bp.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, bp)
            entry["backup_path"] = str(bp)

        backup[rel(p)] = entry

    return backup

def restore_outputs(backup: dict[str, Any]) -> dict[str, Any]:
    restore_report = {}

    for relpath, entry in backup.items():
        p = ROOT / relpath
        existed = entry["existed_before"]
        bp = entry.get("backup_path")

        if existed:
            if bp and Path(bp).exists():
                p.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(bp, p)
                action = "restored"
            else:
                action = "missing_backup"
        else:
            if p.exists():
                p.unlink()
                action = "deleted_new_file"
            else:
                action = "no_action_absent"

        restore_report[relpath] = {
            "action": action,
            "hash_after_restore": sha256(p),
            "matches_before": sha256(p) == entry["hash_before"],
        }

    return restore_report

def inspect_generated_outputs() -> dict[str, Any]:
    out = {}

    for p in MUTABLE_OUTPUTS:
        item = {
            "path": rel(p),
            "exists_after_run": p.exists(),
            "size_after_run": p.stat().st_size if p.exists() else 0,
            "hash_after_run": sha256(p),
        }

        if p.exists() and p.suffix == ".json" and p.stat().st_size <= 15_000_000:
            try:
                obj = read_json(p)
                nodes = walk_for_nodes(obj)
                exact_metric_nodes = []
                daily_like_nodes = []
                core_nodes = []
                sidecar_nodes = []

                for n in nodes:
                    diffs = n.get("target_diffs_abs") or {}
                    if diffs and all(d <= 0.001 for d in diffs.values()):
                        exact_metric_nodes.append(n)

                    matched_keys = set(n.get("matched_keys") or [])
                    if matched_keys.intersection({"daily_equity_records", "daily_records", "equity_curve", "rows", "records"}):
                        daily_like_nodes.append(n)
                    if "core_variant_result" in matched_keys:
                        core_nodes.append(n)
                    if "sidecar_result" in matched_keys:
                        sidecar_nodes.append(n)

                item["top_summary"] = summarize_json_node(obj)
                item["node_count"] = len(nodes)
                item["exact_metric_node_count"] = len(exact_metric_nodes)
                item["daily_like_node_count"] = len(daily_like_nodes)
                item["core_variant_node_count"] = len(core_nodes)
                item["sidecar_node_count"] = len(sidecar_nodes)
                item["nodes_sample"] = nodes[:30]
                item["exact_metric_nodes"] = exact_metric_nodes[:10]
                item["daily_like_nodes"] = daily_like_nodes[:10]
                item["core_variant_nodes"] = core_nodes[:10]
                item["sidecar_nodes"] = sidecar_nodes[:10]
            except Exception as exc:
                item["inspect_error"] = type(exc).__name__ + ": " + str(exc)

        out[rel(p)] = item

    return out

def run_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    candidate_path = ROOT / candidate["path"]

    if not candidate_path.exists():
        return {
            "attempted": False,
            "ok": False,
            "error": f"candidate path missing: {candidate['path']}",
        }

    env = os.environ.copy()
    env["E1R_DRY_RUN"] = "1"
    env["E1R_NO_WRITE"] = "1"
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")

    cmd = [sys.executable, str(candidate_path)]

    started = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(ROOT),
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIMEOUT_SECONDS,
        )
        elapsed = time.time() - started
        return {
            "attempted": True,
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "elapsed_seconds": elapsed,
            "cmd": cmd,
            "stdout_tail": proc.stdout[-12000:],
            "stderr_tail": proc.stderr[-12000:],
        }
    except subprocess.TimeoutExpired as exc:
        elapsed = time.time() - started
        return {
            "attempted": True,
            "ok": False,
            "timeout": True,
            "elapsed_seconds": elapsed,
            "cmd": cmd,
            "stdout_tail": (exc.stdout or "")[-12000:] if isinstance(exc.stdout, str) else "",
            "stderr_tail": (exc.stderr or "")[-12000:] if isinstance(exc.stderr, str) else "",
            "error": f"TimeoutExpired after {TIMEOUT_SECONDS}s",
        }
    except Exception as exc:
        elapsed = time.time() - started
        return {
            "attempted": True,
            "ok": False,
            "elapsed_seconds": elapsed,
            "cmd": cmd,
            "error": type(exc).__name__ + ": " + str(exc),
        }

def main() -> int:
    baseline_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_before = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    candidate = select_generator_candidate()

    with tempfile.TemporaryDirectory(prefix="e1r_dry_run_backup_") as td:
        tmpdir = Path(td)
        backup = backup_outputs(tmpdir)

        run_report = run_candidate(candidate)
        generated_inspection = inspect_generated_outputs()
        restore_report = restore_outputs(backup)

    post_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_after = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    exact_metric_total = sum(
        item.get("exact_metric_node_count", 0)
        for item in generated_inspection.values()
    )
    daily_like_total = sum(
        item.get("daily_like_node_count", 0)
        for item in generated_inspection.values()
    )
    core_total = sum(
        item.get("core_variant_node_count", 0)
        for item in generated_inspection.values()
    )
    sidecar_total = sum(
        item.get("sidecar_node_count", 0)
        for item in generated_inspection.values()
    )

    conclusion = "DRY_RUN_DID_NOT_RECOVER_DAILY_EQUITY"
    recommended = "Inspect selected candidate output and source; if metrics are reproduced but daily equity is missing, patch a temporary dry-run wrapper around composer inputs."

    if exact_metric_total > 0 and daily_like_total > 0:
        conclusion = "DRY_RUN_RECOVERED_METRICS_AND_DAILY_LIKE_OUTPUT"
        recommended = "Next step can extract candidate daily equity into a non-canonical artifact and validate full-window portfolio-level contract."
    elif exact_metric_total > 0:
        conclusion = "DRY_RUN_REPRODUCED_FROZEN_METRICS_BUT_DAILY_EQUITY_STILL_MISSING"
        recommended = "Patch dry-run wrapper to expose in-memory core_variant_result / composed equity before summary-only export."
    elif run_report.get("ok"):
        conclusion = "DRY_RUN_COMPLETED_BUT_FROZEN_METRIC_MATCH_NOT_FOUND"
        recommended = "Inspect generated outputs and candidate source; selected script may not be the exact frozen generator path."
    elif run_report.get("attempted"):
        conclusion = "DRY_RUN_ATTEMPT_FAILED_OR_TIMED_OUT"
        recommended = "Use stdout/stderr tail to fix invocation or select the next generator candidate."

    report = {
        "generated_at": now(),
        "stage": "B_STAGE_3_8E2F2C4C10F4B0E_LITE_GENERATOR_DRY_RUN",
        "status": "E1R_GENERATOR_DRY_RUN_LITE_COMPLETE_OUTPUTS_RESTORED",
        "policy": {
            "dashboard_changed": False,
            "workflow_changed": False,
            "strategy_logic_changed": False,
            "e1r_canonical_written": False,
            "portfolio_equity_composed": False,
            "full_backtest_rerun": False,
            "mutable_outputs_restored": True,
        },
        "selected_candidate": candidate,
        "run_report": run_report,
        "generated_inspection": generated_inspection,
        "restore_report": restore_report,
        "recovery_counts": {
            "exact_metric_node_count": exact_metric_total,
            "daily_like_node_count": daily_like_total,
            "core_variant_node_count": core_total,
            "sidecar_node_count": sidecar_total,
        },
        "conclusion": conclusion,
        "recommended_next_action": recommended,
        "strategy_files_unchanged": baseline_hashes == post_hashes,
        "canonical_existence_unchanged_after_restore": canonical_before == canonical_after,
        "canonical_after_restore": canonical_after,
        "next_stage": {
            "name": "Stage 3.8E-2F-2C-4C-10F-4B-0F",
            "title": "Expose exact in-memory E1R composition result or select next generator",
            "recommended_action": recommended,
        },
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# Stage 3.8E-2F-2C-4C-10F-4B-0E-lite E1R Generator Dry-run Report")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append("- Status: `E1R_GENERATOR_DRY_RUN_LITE_COMPLETE_OUTPUTS_RESTORED`")
    md.append(f"- Strategy files unchanged: `{report['strategy_files_unchanged']}`")
    md.append(f"- Canonical existence unchanged after restore: `{report['canonical_existence_unchanged_after_restore']}`")
    md.append("- E1R canonical written: `False`")
    md.append("")
    md.append("## Selected Candidate")
    md.append("")
    md.append("```json")
    md.append(json.dumps(candidate, indent=2, ensure_ascii=False)[:12000])
    md.append("```")
    md.append("")
    md.append("## Run Report")
    md.append("")
    md.append("```json")
    md.append(json.dumps(run_report, indent=2, ensure_ascii=False)[:18000])
    md.append("```")
    md.append("")
    md.append("## Recovery Counts")
    md.append("")
    md.append("```json")
    md.append(json.dumps(report["recovery_counts"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {recommended}")
    md.append("")
    md.append("## Generated Inspection Compact")
    md.append("")
    compact = {}
    for k, v in generated_inspection.items():
        compact[k] = {
            "exists_after_run": v.get("exists_after_run"),
            "size_after_run": v.get("size_after_run"),
            "node_count": v.get("node_count"),
            "exact_metric_node_count": v.get("exact_metric_node_count"),
            "daily_like_node_count": v.get("daily_like_node_count"),
            "core_variant_node_count": v.get("core_variant_node_count"),
            "sidecar_node_count": v.get("sidecar_node_count"),
            "top_summary": v.get("top_summary"),
            "exact_metric_nodes": v.get("exact_metric_nodes"),
            "daily_like_nodes": v.get("daily_like_nodes"),
        }
    md.append("```json")
    md.append(json.dumps(compact, indent=2, ensure_ascii=False)[:30000])
    md.append("```")
    md.append("")
    md.append("## Restore Report")
    md.append("")
    md.append("```json")
    md.append(json.dumps(restore_report, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Next Stage")
    md.append("")
    md.append(f"- `{report['next_stage']['name']}`: {report['next_stage']['title']}")
    md.append(f"- Recommended action: {report['next_stage']['recommended_action']}")
    md.append("")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("Stage 3.8E-2F-2C-4C-10F-4B-0E-lite dry-run complete")
    print("status:", report["status"])
    print("strategy_files_unchanged:", report["strategy_files_unchanged"])
    print("canonical_existence_unchanged_after_restore:", report["canonical_existence_unchanged_after_restore"])
    print("selected_candidate_path:", candidate.get("path"))
    print("selected_candidate_source:", candidate.get("source"))
    print("run_attempted:", run_report.get("attempted"))
    print("run_ok:", run_report.get("ok"))
    print("run_returncode:", run_report.get("returncode"))
    print("elapsed_seconds:", run_report.get("elapsed_seconds"))
    print("recovery_counts:", json.dumps(report["recovery_counts"], ensure_ascii=False))
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)
    print("canonical_after_restore:", json.dumps(canonical_after, ensure_ascii=False))
    print("next_stage:", report["next_stage"]["name"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
