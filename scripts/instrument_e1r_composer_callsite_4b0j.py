#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
import importlib
import os
import runpy
import shutil
import sys
import tempfile
import time
import traceback
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts/export_canonical_5y_equity_curves.py"

REPORT_JSON = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json"
REPORT_MD = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.md"

FROZEN_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

CANONICAL_E1R_FILES = [
    ROOT / "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
    ROOT / "exports/e1_e1r_5y_equity_comparison.json",
]

MUTABLE_OUTPUTS = [
    ROOT / "exports/e1r_v0_2_backtest_summary.json",
    ROOT / "exports/e1r_v0_2_backtest_equity_curve.json",
    ROOT / "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
    ROOT / "exports/e1_e1r_5y_equity_comparison.json",
    ROOT / "data/research/e1r/e1r_formal_backtest_v0_1.json",
]

TARGET_FUNC = "compose_e1r_v0_2_variant"

TARGET_TERMS = [
    "compose_e1r_v0_2_variant",
    "core_variant_result",
    "sidecar_result",
    "daily_equity_records",
    "build_equity_records_from_returns",
    "extract_core_interval_returns",
    "run_strategy_variant_comparison",
    "run_stateful_simulation",
    "e1r_v0_2_backtest_summary.json",
    "e1r_v0_2_backtest_equity_curve.json",
    "E1R_REGIME_AWARE_V0_2",
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

def write_json(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def summarize_value(x: Any, depth: int = 0) -> Any:
    if depth > 2:
        return {"type": type(x).__name__, "repr": repr(x)[:300]}

    if isinstance(x, dict):
        out = {
            "type": "dict",
            "len": len(x),
            "keys": sorted(str(k) for k in x.keys())[:120],
        }
        metrics = {}
        for k in [
            "strategy_id", "name", "version", "status",
            "total_return_pct", "spx_return_pct", "spx_total_return_pct",
            "alpha_pct", "max_drawdown_pct", "profit_factor", "sharpe_ratio",
            "number_of_trades", "total_trades_all", "simulation_start_date",
            "simulation_end_date", "simulation_days", "daily_equity_record_count",
            "records_count", "active_count", "row_count",
        ]:
            if k in x:
                metrics[k] = x.get(k)
        if metrics:
            out["metric_like_values"] = metrics

        child = {}
        for k, v in x.items():
            if isinstance(v, list):
                child[str(k)] = summarize_value(v, depth + 1)
            elif isinstance(v, dict):
                child[str(k)] = {
                    "type": "dict",
                    "len": len(v),
                    "keys": sorted(str(kk) for kk in v.keys())[:80],
                }
        if child:
            out["children"] = child
        return out

    if isinstance(x, list):
        out = {
            "type": "list",
            "len": len(x),
            "first_type": type(x[0]).__name__ if x else None,
        }
        if x and isinstance(x[0], dict):
            out["first_keys"] = sorted(str(k) for k in x[0].keys())[:100]
            out["first_sample"] = x[0]
            out["last_sample"] = x[-1]
        return out

    return {"type": type(x).__name__, "repr": repr(x)[:500]}

def backup_outputs(tmpdir: Path) -> dict[str, Any]:
    backup = {}
    for p in MUTABLE_OUTPUTS:
        item = {
            "path": rel(p),
            "existed_before": p.exists(),
            "hash_before": sha256(p),
            "backup_path": None,
        }
        if p.exists():
            bp = tmpdir / rel(p)
            bp.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, bp)
            item["backup_path"] = str(bp)
        backup[rel(p)] = item
    return backup

def restore_outputs(backup: dict[str, Any]) -> dict[str, Any]:
    out = {}
    for relpath, item in backup.items():
        p = ROOT / relpath
        if item["existed_before"]:
            bp = item.get("backup_path")
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

        out[relpath] = {
            "action": action,
            "hash_after_restore": sha256(p),
            "matches_before": sha256(p) == item["hash_before"],
        }
    return out

def source_callsite_scan() -> dict[str, Any]:
    results = []

    for base in [ROOT / "scripts", ROOT / "src"]:
        if not base.exists():
            continue
        for p in sorted(base.rglob("*.py")):
            if not p.is_file():
                continue
            text = p.read_text(errors="replace")
            if not any(t in text for t in TARGET_TERMS):
                continue

            lines = text.splitlines()
            hits = []
            score = 0

            for i, line in enumerate(lines, start=1):
                matched = [t for t in TARGET_TERMS if t in line]
                if not matched:
                    continue
                score += len(matched)
                if TARGET_FUNC in matched:
                    score += 20
                if "core_variant_result" in matched:
                    score += 10
                if "sidecar_result" in matched:
                    score += 10

                lo = max(1, i - 4)
                hi = min(len(lines), i + 4)
                hits.append({
                    "line": i,
                    "matched": matched,
                    "context": [
                        {"line": j, "text": lines[j - 1][:1000]}
                        for j in range(lo, hi + 1)
                    ],
                })

            results.append({
                "path": rel(p),
                "score": score,
                "hit_count": len(hits),
                "hits": hits[:80],
            })

    return {
        "candidate_file_count": len(results),
        "candidates": sorted(results, key=lambda x: (-x["score"], x["path"]))[:80],
    }

def patch_composer_modules() -> dict[str, Any]:
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "src"))

    module_names = [
        "engine.e1r_composer",
        "src.engine.e1r_composer",
    ]

    patch_report = {
        "attempted_modules": module_names,
        "patched_modules": [],
        "errors": [],
        "wrapped_calls": [],
    }

    def make_wrapper(original, module_name: str):
        def wrapper(*args, **kwargs):
            call = {
                "module_name": module_name,
                "arg_count": len(args),
                "kwarg_keys": sorted(kwargs.keys()),
                "args": [summarize_value(a) for a in args],
                "kwargs": {k: summarize_value(v) for k, v in kwargs.items()},
            }

            try:
                result = original(*args, **kwargs)
                call["ok"] = True
                call["result_summary"] = summarize_value(result)
                patch_report["wrapped_calls"].append(call)
                return result
            except Exception as exc:
                call["ok"] = False
                call["error"] = type(exc).__name__ + ": " + str(exc)
                call["traceback_tail"] = traceback.format_exc()[-5000:]
                patch_report["wrapped_calls"].append(call)
                raise

        return wrapper

    for name in module_names:
        try:
            mod = importlib.import_module(name)
            if hasattr(mod, TARGET_FUNC):
                original = getattr(mod, TARGET_FUNC)
                setattr(mod, TARGET_FUNC, make_wrapper(original, name))
                patch_report["patched_modules"].append(name)
            else:
                patch_report["errors"].append(f"{name}: {TARGET_FUNC} not found")
        except Exception as exc:
            patch_report["errors"].append(f"{name}: {type(exc).__name__}: {exc}")

    return patch_report

def run_generator_with_instrumentation() -> dict[str, Any]:
    env_before = dict(os.environ)
    os.environ["E1R_DRY_RUN"] = "1"
    os.environ["E1R_NO_WRITE"] = "1"

    started = time.time()
    run_report = {
        "attempted": True,
        "ok": False,
        "elapsed_seconds": None,
        "error": None,
        "traceback_tail": None,
    }

    try:
        runpy.run_path(str(GENERATOR), run_name="__main__")
        run_report["ok"] = True
    except SystemExit as exc:
        code = exc.code
        run_report["system_exit_code"] = code
        run_report["ok"] = code in (0, None)
        if not run_report["ok"]:
            run_report["error"] = f"SystemExit: {code}"
    except Exception as exc:
        run_report["error"] = type(exc).__name__ + ": " + str(exc)
        run_report["traceback_tail"] = traceback.format_exc()[-8000:]
    finally:
        run_report["elapsed_seconds"] = time.time() - started
        os.environ.clear()
        os.environ.update(env_before)

    return run_report

def inspect_outputs_after_run() -> dict[str, Any]:
    out = {}
    for p in MUTABLE_OUTPUTS:
        item = {
            "path": rel(p),
            "exists_after_run": p.exists(),
            "size_after_run": p.stat().st_size if p.exists() else 0,
            "hash_after_run": sha256(p),
        }
        if p.exists() and p.suffix == ".json" and p.stat().st_size <= 8_000_000:
            try:
                obj = json.loads(p.read_text())
                item["top_summary"] = summarize_value(obj)
            except Exception as exc:
                item["inspect_error"] = type(exc).__name__ + ": " + str(exc)
        out[rel(p)] = item
    return out

def main() -> int:
    baseline_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_before = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    callsite_scan = source_callsite_scan()

    with tempfile.TemporaryDirectory(prefix="e1r_4b0j_backup_") as td:
        backup = backup_outputs(Path(td))
        patch_report = patch_composer_modules()
        run_report = run_generator_with_instrumentation()
        output_inspection = inspect_outputs_after_run()
        restore_report = restore_outputs(backup)

    post_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_after = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    wrapped_call_count = len(patch_report.get("wrapped_calls") or [])
    direct_callsite_candidates = [
        c for c in callsite_scan["candidates"]
        if any(TARGET_FUNC in h["matched"] for h in c.get("hits", []))
    ]

    if wrapped_call_count > 0:
        conclusion = "COMPOSER_CALLSITE_EXECUTED_AND_INPUT_SHAPES_CAPTURED"
        recommended = "Use captured core_variant_result and sidecar_result shapes to build a noncanonical compose output extraction probe."
    elif direct_callsite_candidates:
        conclusion = "COMPOSER_CALLSITE_FOUND_IN_SOURCE_BUT_NOT_TRIGGERED_BY_GENERATOR"
        recommended = "Instrument the highest source callsite directly instead of export_canonical_5y_equity_curves.py."
    else:
        conclusion = "NO_DIRECT_COMPOSER_CALLSITE_FOUND_OR_TRIGGERED"
        recommended = "Trace upstream generator/source that builds core_variant_result; current generator appears to replay summary/diagnostic exports."

    report = {
        "generated_at": now(),
        "stage": "B_STAGE_3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION",
        "status": "E1R_COMPOSER_CALLSITE_INSTRUMENTATION_COMPLETE_OUTPUTS_RESTORED",
        "policy": {
            "dashboard_changed": False,
            "workflow_changed": False,
            "strategy_logic_changed": False,
            "e1r_canonical_written": False,
            "portfolio_equity_composed": False,
            "full_backtest_rerun": False,
            "candidate_extracted": False,
            "mutable_outputs_restored": True,
        },
        "callsite_scan": callsite_scan,
        "direct_callsite_candidate_count": len(direct_callsite_candidates),
        "direct_callsite_candidates": direct_callsite_candidates[:20],
        "patch_report": patch_report,
        "run_report": run_report,
        "output_inspection": output_inspection,
        "restore_report": restore_report,
        "wrapped_call_count": wrapped_call_count,
        "conclusion": conclusion,
        "recommended_next_action": recommended,
        "strategy_files_unchanged": baseline_hashes == post_hashes,
        "canonical_existence_unchanged_after_restore": canonical_before == canonical_after,
        "canonical_after_restore": canonical_after,
        "next_stage": {
            "name": "Stage 3.8E-2F-2C-4C-10F-4B-0K",
            "title": "Instrument highest direct source callsite or recover core builder",
            "recommended_action": recommended,
        },
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# Stage 3.8E-2F-2C-4C-10F-4B-0J Composer Callsite Instrumentation")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append("- Status: `E1R_COMPOSER_CALLSITE_INSTRUMENTATION_COMPLETE_OUTPUTS_RESTORED`")
    md.append("- E1R canonical written: `False`")
    md.append("- Candidate extracted: `False`")
    md.append(f"- Strategy files unchanged: `{report['strategy_files_unchanged']}`")
    md.append(f"- Canonical existence unchanged after restore: `{report['canonical_existence_unchanged_after_restore']}`")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append("```json")
    md.append(json.dumps({
        "wrapped_call_count": wrapped_call_count,
        "direct_callsite_candidate_count": len(direct_callsite_candidates),
        "generator_run_ok": run_report.get("ok"),
        "generator_elapsed_seconds": run_report.get("elapsed_seconds"),
        "patched_modules": patch_report.get("patched_modules"),
        "patch_errors": patch_report.get("errors"),
    }, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {recommended}")
    md.append("")
    md.append("## Wrapped Calls")
    md.append("")
    md.append("```json")
    md.append(json.dumps(patch_report.get("wrapped_calls", []), indent=2, ensure_ascii=False)[:22000])
    md.append("```")
    md.append("")
    md.append("## Direct Callsite Candidates")
    md.append("")
    md.append("```json")
    md.append(json.dumps(direct_callsite_candidates[:12], indent=2, ensure_ascii=False)[:24000])
    md.append("```")
    md.append("")
    md.append("## Top Source Candidates")
    md.append("")
    md.append("```json")
    md.append(json.dumps(callsite_scan["candidates"][:20], indent=2, ensure_ascii=False)[:26000])
    md.append("```")
    md.append("")
    md.append("## Output Inspection")
    md.append("")
    md.append("```json")
    md.append(json.dumps(output_inspection, indent=2, ensure_ascii=False)[:16000])
    md.append("```")
    md.append("")
    md.append("## Next Stage")
    md.append("")
    md.append(f"- `{report['next_stage']['name']}`: {report['next_stage']['title']}")
    md.append(f"- Recommended action: {report['next_stage']['recommended_action']}")
    md.append("")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("Stage 3.8E-2F-2C-4C-10F-4B-0J callsite instrumentation complete")
    print("status:", report["status"])
    print("strategy_files_unchanged:", report["strategy_files_unchanged"])
    print("canonical_existence_unchanged_after_restore:", report["canonical_existence_unchanged_after_restore"])
    print("generator_run_ok:", run_report.get("ok"))
    print("generator_elapsed_seconds:", run_report.get("elapsed_seconds"))
    print("patched_modules:", json.dumps(patch_report.get("patched_modules"), ensure_ascii=False))
    print("patch_errors:", json.dumps(patch_report.get("errors"), ensure_ascii=False))
    print("wrapped_call_count:", wrapped_call_count)
    print("direct_callsite_candidate_count:", len(direct_callsite_candidates))
    if direct_callsite_candidates:
        top = direct_callsite_candidates[0]
        print("top_direct_callsite_source:", top["path"])
        print("top_direct_callsite_score:", top["score"])
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)
    print("next_stage:", report["next_stage"]["name"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
