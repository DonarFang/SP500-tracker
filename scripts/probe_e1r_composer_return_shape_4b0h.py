#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import hashlib
import importlib.util
import inspect
import os
import re
import sys
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

COMPOSER = ROOT / "src/engine/e1r_composer.py"
SIDECAR = ROOT / "src/engine/e1r_sidecar_sleeve.py"
BACKTEST = ROOT / "src/engine/backtest.py"
GENERATOR = ROOT / "scripts/export_canonical_5y_equity_curves.py"

REPORT_JSON = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0H_COMPOSER_RETURN_SHAPE_PROBE.json"
REPORT_MD = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0H_COMPOSER_RETURN_SHAPE_PROBE.md"

FROZEN_FILES = [BACKTEST, COMPOSER, SIDECAR]

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

TARGET_FUNC = "compose_e1r_v0_2_variant"

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

def read_text(p: Path) -> str:
    return p.read_text(errors="replace")

def as_float(x: Any, default=None):
    try:
        if x is None:
            return default
        return float(x)
    except Exception:
        return default

def safe_unparse(node: ast.AST | None) -> str | None:
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:
        return "<unparse_failed>"

def source_segment(path: Path, start: int, end: int, max_chars: int = 40000) -> str:
    lines = read_text(path).splitlines()
    s = "\n".join(lines[max(0, start - 1): min(len(lines), end)])
    return s[:max_chars] + ("\n...TRUNCATED..." if len(s) > max_chars else "")

def find_function_ast(path: Path, func_name: str) -> dict[str, Any]:
    text = read_text(path)
    tree = ast.parse(text)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            args = []
            for a in node.args.args:
                args.append({
                    "name": a.arg,
                    "annotation": safe_unparse(a.annotation),
                })

            defaults = [safe_unparse(d) for d in node.args.defaults]

            returns = []
            return_nodes = []
            assignments = []
            calls = []
            dict_literals = []

            for child in ast.walk(node):
                if isinstance(child, ast.Return):
                    returns.append(safe_unparse(child.value))
                    return_nodes.append({
                        "line": getattr(child, "lineno", None),
                        "value": safe_unparse(child.value),
                    })

                if isinstance(child, (ast.Assign, ast.AnnAssign)):
                    targets = []
                    if isinstance(child, ast.Assign):
                        targets = [safe_unparse(t) for t in child.targets]
                    else:
                        targets = [safe_unparse(child.target)]

                    value_src = safe_unparse(child.value)
                    for t in targets:
                        if t and any(k in t for k in [
                            "result", "metrics", "core", "sidecar", "daily", "equity",
                            "records", "summary", "variant", "portfolio", "curve"
                        ]):
                            assignments.append({
                                "line": getattr(child, "lineno", None),
                                "target": t,
                                "value": value_src,
                            })

                    if isinstance(getattr(child, "value", None), ast.Dict):
                        keys = []
                        for k in child.value.keys:
                            if isinstance(k, ast.Constant):
                                keys.append(k.value)
                            else:
                                keys.append(safe_unparse(k))
                        dict_literals.append({
                            "line": getattr(child, "lineno", None),
                            "target": targets,
                            "keys": keys,
                        })

                if isinstance(child, ast.Call):
                    fn = child.func
                    if isinstance(fn, ast.Name):
                        calls.append(fn.id)
                    elif isinstance(fn, ast.Attribute):
                        calls.append(fn.attr)

            return {
                "exists": True,
                "name": func_name,
                "line": node.lineno,
                "end_line": getattr(node, "end_lineno", node.lineno),
                "signature_ast": {
                    "args": args,
                    "defaults": defaults,
                    "returns_annotation": safe_unparse(node.returns),
                },
                "returns": returns[:60],
                "return_nodes": return_nodes[:60],
                "assignments_of_interest": assignments[:160],
                "dict_literals": dict_literals[:80],
                "calls_unique": sorted(set(calls)),
                "source_excerpt": source_segment(path, node.lineno, getattr(node, "end_lineno", node.lineno)),
            }

    return {"exists": False, "name": func_name}

def import_composer_module() -> dict[str, Any]:
    """
    Import composer only. We do not execute compose_e1r_v0_2_variant.
    The prior 4B-0G sidecar import failed, so this probe isolates composer import first.
    """
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "src"))

    out = {
        "attempted": True,
        "ok": False,
        "module": "e1r_composer",
        "errors": [],
        "target_function": None,
        "public_relevant_objects": {},
    }

    try:
        spec = importlib.util.spec_from_file_location("e1r_composer_4b0h_probe", COMPOSER)
        if spec is None or spec.loader is None:
            raise RuntimeError("cannot create import spec for composer")

        mod = importlib.util.module_from_spec(spec)
        # Important for dataclasses / forward references in some modules.
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)

        if hasattr(mod, TARGET_FUNC):
            fn = getattr(mod, TARGET_FUNC)
            info = {
                "exists": True,
                "type": type(fn).__name__,
            }
            try:
                info["signature"] = str(inspect.signature(fn))
            except Exception as exc:
                info["signature_error"] = type(exc).__name__ + ": " + str(exc)
            try:
                src_lines, line_no = inspect.getsourcelines(fn)
                info["source_line"] = line_no
                info["source_excerpt"] = "".join(src_lines)[:40000]
            except Exception as exc:
                info["source_error"] = type(exc).__name__ + ": " + str(exc)

            out["target_function"] = info
        else:
            out["target_function"] = {"exists": False}

        for name in dir(mod):
            if name.startswith("_"):
                continue
            if any(k in name.lower() for k in [
                "e1r", "compose", "variant", "core", "sidecar", "equity", "record", "return", "metric"
            ]):
                obj = getattr(mod, name)
                item = {"type": type(obj).__name__}
                if callable(obj):
                    try:
                        item["signature"] = str(inspect.signature(obj))
                    except Exception:
                        pass
                out["public_relevant_objects"][name] = item

        out["ok"] = True
    except Exception as exc:
        out["errors"].append(type(exc).__name__ + ": " + str(exc))

    return out

def infer_return_contract(func_ast: dict[str, Any], import_probe: dict[str, Any]) -> dict[str, Any]:
    findings = []
    risks = []
    source_flags = {}

    src = func_ast.get("source_excerpt") or ""

    patterns = {
        "mentions_core_variant_result": "core_variant_result" in src,
        "mentions_sidecar_result": "sidecar_result" in src,
        "mentions_daily_equity_records": "daily_equity_records" in src,
        "mentions_daily_records": "daily_records" in src,
        "mentions_equity_curve": "equity_curve" in src,
        "mentions_variant_results": "variant_results" in src,
        "mentions_metrics": "metrics" in src,
        "mentions_total_return_pct": "total_return_pct" in src,
        "mentions_profit_factor": "profit_factor" in src,
        "mentions_sharpe_ratio": "sharpe_ratio" in src,
        "mentions_build_equity_records_from_returns": "build_equity_records_from_returns" in src,
        "mentions_extract_core_interval_returns": "extract_core_interval_returns" in src,
        "mentions_build_e1r_sidecar_sleeve": "build_e1r_sidecar_sleeve" in src,
    }
    source_flags.update(patterns)

    if func_ast.get("exists"):
        findings.append("compose_e1r_v0_2_variant definition found in composer source.")
    else:
        risks.append("compose_e1r_v0_2_variant definition not found.")

    if import_probe.get("ok") and (import_probe.get("target_function") or {}).get("exists"):
        findings.append("compose_e1r_v0_2_variant can be imported and its signature can be inspected.")
    else:
        risks.append("compose_e1r_v0_2_variant import/signature inspection did not fully succeed.")

    if patterns["mentions_core_variant_result"]:
        findings.append("Function source mentions core_variant_result.")
    else:
        risks.append("Function source does not visibly mention core_variant_result.")

    if patterns["mentions_sidecar_result"]:
        findings.append("Function source mentions sidecar_result.")
    else:
        risks.append("Function source does not visibly mention sidecar_result.")

    if patterns["mentions_daily_equity_records"] or patterns["mentions_daily_records"] or patterns["mentions_equity_curve"]:
        findings.append("Function source mentions daily/equity output fields.")
    else:
        risks.append("Function source does not visibly mention daily/equity output fields.")

    returns = func_ast.get("returns") or []
    return_text = "\n".join(str(x) for x in returns)
    source_flags["return_mentions_dict"] = "{" in return_text or "dict(" in return_text
    source_flags["return_mentions_result"] = "result" in return_text
    source_flags["return_mentions_metrics"] = "metrics" in return_text
    source_flags["return_mentions_daily"] = "daily" in return_text or "equity" in return_text

    if source_flags["return_mentions_dict"]:
        findings.append("Return expression appears to include a dict-like object.")
    else:
        risks.append("Return expression may not directly expose a dict; runtime probe may need wrapper instrumentation.")

    return {
        "findings": findings,
        "risks": risks,
        "source_flags": source_flags,
        "recommended_next_actions": [
            "Run a narrow runtime invocation probe only if required arguments can be resolved from signature and existing generator code.",
            "If direct invocation requires full data objects, build an instrumentation wrapper around existing generator/composer call site instead of guessing arguments.",
            "Do not use persisted exports/e1r_v0_2_backtest_equity_curve.json as portfolio equity; 4B-0F-v2 already rejected it.",
        ],
    }

def main() -> int:
    baseline_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_before = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    func_ast = find_function_ast(COMPOSER, TARGET_FUNC)
    import_probe = import_composer_module()
    inference = infer_return_contract(func_ast, import_probe)

    post_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_after = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    conclusion = "COMPOSER_RETURN_CONTRACT_SOURCE_PROBED_RUNTIME_INVOCATION_NOT_EXECUTED"
    recommended = "Use the inspected signature/source to design the next wrapper: either direct invoke compose_e1r_v0_2_variant if inputs are available, or instrument the existing call site that builds those inputs."

    if inference["source_flags"].get("mentions_core_variant_result") and inference["source_flags"].get("mentions_sidecar_result"):
        conclusion = "COMPOSER_RETURN_CONTRACT_HAS_CORE_AND_SIDECAR_SOURCE_FIELDS"

    report = {
        "generated_at": now(),
        "stage": "B_STAGE_3_8E2F2C4C10F4B0H_COMPOSER_RETURN_SHAPE_PROBE",
        "status": "E1R_COMPOSER_RETURN_SHAPE_PROBE_COMPLETE_NO_RUNTIME_EXECUTION",
        "policy": {
            "dashboard_changed": False,
            "workflow_changed": False,
            "strategy_logic_changed": False,
            "e1r_canonical_written": False,
            "portfolio_equity_composed": False,
            "full_backtest_rerun": False,
            "composer_function_invoked": False,
            "generator_executed": False,
            "source_and_signature_probe_only": True,
        },
        "watched_files": {
            rel(p): {
                "exists": p.exists(),
                "sha256": sha256(p),
                "size": p.stat().st_size if p.exists() else None,
            }
            for p in [COMPOSER, SIDECAR, BACKTEST, GENERATOR]
        },
        "target_function_ast": func_ast,
        "import_probe": import_probe,
        "inference": inference,
        "conclusion": conclusion,
        "recommended_next_action": recommended,
        "strategy_files_unchanged": baseline_hashes == post_hashes,
        "canonical_existence_unchanged": canonical_before == canonical_after,
        "canonical_after": canonical_after,
        "next_stage": {
            "name": "Stage 3.8E-2F-2C-4C-10F-4B-0I",
            "title": "Resolve composer invocation inputs or instrument existing call site",
            "recommended_action": recommended,
        },
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# Stage 3.8E-2F-2C-4C-10F-4B-0H Composer Return Shape Probe")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append("- Status: `E1R_COMPOSER_RETURN_SHAPE_PROBE_COMPLETE_NO_RUNTIME_EXECUTION`")
    md.append("- Composer function invoked: `False`")
    md.append("- Generator executed: `False`")
    md.append("- E1R canonical written: `False`")
    md.append(f"- Strategy files unchanged: `{report['strategy_files_unchanged']}`")
    md.append(f"- Canonical existence unchanged: `{report['canonical_existence_unchanged']}`")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {recommended}")
    md.append("")
    md.append("## Inference")
    md.append("")
    md.append("```json")
    md.append(json.dumps({
        "source_flags": inference["source_flags"],
        "findings": inference["findings"],
        "risks": inference["risks"],
        "recommended_next_actions": inference["recommended_next_actions"],
    }, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Import Probe")
    md.append("")
    md.append("```json")
    md.append(json.dumps(import_probe, indent=2, ensure_ascii=False)[:20000])
    md.append("```")
    md.append("")
    md.append("## Function Signature / Return Contract")
    md.append("")
    compact_func = {
        "exists": func_ast.get("exists"),
        "name": func_ast.get("name"),
        "line": func_ast.get("line"),
        "end_line": func_ast.get("end_line"),
        "signature_ast": func_ast.get("signature_ast"),
        "returns": func_ast.get("returns"),
        "return_nodes": func_ast.get("return_nodes"),
        "assignments_of_interest": func_ast.get("assignments_of_interest", [])[:80],
        "dict_literals": func_ast.get("dict_literals", [])[:60],
        "calls_unique": func_ast.get("calls_unique", [])[:200],
    }
    md.append("```json")
    md.append(json.dumps(compact_func, indent=2, ensure_ascii=False)[:30000])
    md.append("```")
    md.append("")
    md.append("## Next Stage")
    md.append("")
    md.append(f"- `{report['next_stage']['name']}`: {report['next_stage']['title']}")
    md.append(f"- Recommended action: {report['next_stage']['recommended_action']}")
    md.append("")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("Stage 3.8E-2F-2C-4C-10F-4B-0H composer return-shape probe complete")
    print("status:", report["status"])
    print("strategy_files_unchanged:", report["strategy_files_unchanged"])
    print("canonical_existence_unchanged:", report["canonical_existence_unchanged"])
    print("composer_function_invoked:", report["policy"]["composer_function_invoked"])
    print("generator_executed:", report["policy"]["generator_executed"])
    print("target_function_exists:", func_ast.get("exists"))
    print("import_probe_ok:", import_probe.get("ok"))
    print("target_function_signature:", (import_probe.get("target_function") or {}).get("signature"))
    print("source_flags:", json.dumps(inference["source_flags"], ensure_ascii=False))
    print("findings:", json.dumps(inference["findings"], ensure_ascii=False))
    print("risks:", json.dumps(inference["risks"], ensure_ascii=False))
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)
    print("next_stage:", report["next_stage"]["name"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
