#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import hashlib
import inspect
import importlib.util
import os
import re
import sys
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

GENERATOR = ROOT / "scripts/export_canonical_5y_equity_curves.py"
COMPOSER = ROOT / "src/engine/e1r_composer.py"
SIDECAR = ROOT / "src/engine/e1r_sidecar_sleeve.py"
BACKTEST = ROOT / "src/engine/backtest.py"

REPORT_JSON = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0G_GENERATOR_COMPOSER_CONTRACT_AUDIT.json"
REPORT_MD = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0G_GENERATOR_COMPOSER_CONTRACT_AUDIT.md"

FROZEN_FILES = [BACKTEST, COMPOSER, SIDECAR]

CANONICAL_E1R_FILES = [
    ROOT / "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
    ROOT / "exports/e1_e1r_5y_equity_comparison.json",
]

WATCH_FILES = [
    GENERATOR,
    COMPOSER,
    SIDECAR,
    BACKTEST,
]

TARGET_NAMES = [
    "compose_e1r_v0_2_variant",
    "core_variant_result",
    "sidecar_result",
    "daily_equity_records",
    "daily_records",
    "equity_curve",
    "variant_results",
    "build_equity_records_from_returns",
    "extract_core_interval_returns",
    "build_e1r_sidecar_sleeve",
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

def read_text(p: Path) -> str:
    return p.read_text(errors="replace")

def write_json(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def safe_segment(text: str, start: int, end: int, max_chars: int = 30000) -> str:
    lines = text.splitlines()
    seg = "\n".join(lines[max(0, start - 1): min(len(lines), end)])
    if len(seg) > max_chars:
        return seg[:max_chars] + "\n...TRUNCATED..."
    return seg

def parse_ast(p: Path):
    try:
        return ast.parse(read_text(p)), None
    except Exception as exc:
        return None, type(exc).__name__ + ": " + str(exc)

def collect_defs(p: Path) -> dict[str, Any]:
    text = read_text(p)
    tree, err = parse_ast(p)
    if tree is None:
        return {"path": rel(p), "parse_error": err, "defs": []}

    defs = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start = getattr(node, "lineno", None)
            end = getattr(node, "end_lineno", start)
            src = safe_segment(text, start, end, max_chars=22000) if start and end else ""

            matched_terms = [t for t in TARGET_NAMES if t in src or t == getattr(node, "name", "")]
            if matched_terms:
                returns = []
                calls = []
                assigns = []

                for child in ast.walk(node):
                    if isinstance(child, ast.Return):
                        try:
                            returns.append(ast.unparse(child.value) if child.value is not None else "None")
                        except Exception:
                            returns.append("<unparse_failed>")

                    if isinstance(child, ast.Call):
                        fn = child.func
                        name = None
                        if isinstance(fn, ast.Name):
                            name = fn.id
                        elif isinstance(fn, ast.Attribute):
                            name = fn.attr
                        if name:
                            calls.append(name)

                    if isinstance(child, (ast.Assign, ast.AnnAssign)):
                        targets = []
                        if isinstance(child, ast.Assign):
                            for t in child.targets:
                                try:
                                    targets.append(ast.unparse(t))
                                except Exception:
                                    pass
                        elif isinstance(child, ast.AnnAssign):
                            try:
                                targets.append(ast.unparse(child.target))
                            except Exception:
                                pass
                        for t in targets:
                            if any(x in t for x in ["core", "sidecar", "daily", "equity", "variant", "summary", "metrics", "records", "rows"]):
                                try:
                                    value = ast.unparse(child.value) if getattr(child, "value", None) is not None else None
                                except Exception:
                                    value = "<unparse_failed>"
                                assigns.append({"target": t, "value": value})

                defs.append({
                    "name": getattr(node, "name", None),
                    "type": type(node).__name__,
                    "line": start,
                    "end_line": end,
                    "matched_terms": sorted(set(matched_terms)),
                    "calls_counter_top": sorted(set(calls))[:200],
                    "assignments_of_interest": assigns[:120],
                    "returns": returns[:40],
                    "source_excerpt": src,
                })

    return {"path": rel(p), "defs": defs}

def grep_context(p: Path) -> dict[str, Any]:
    text = read_text(p)
    lines = text.splitlines()
    hits = []

    for i, line in enumerate(lines, start=1):
        matched = [t for t in TARGET_NAMES if t in line]
        if matched:
            lo = max(1, i - 3)
            hi = min(len(lines), i + 3)
            hits.append({
                "line": i,
                "matched": matched,
                "context": [
                    {"line": j, "text": lines[j - 1][:900]}
                    for j in range(lo, hi + 1)
                ],
            })

    return {
        "path": rel(p),
        "hit_count": len(hits),
        "hits": hits[:120],
    }

def module_import_probe() -> dict[str, Any]:
    """
    Import modules only. Do not invoke heavy functions.
    This helps inspect signatures and object availability.
    """
    out = {
        "attempted": True,
        "ok": False,
        "objects": {},
        "errors": [],
    }

    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "src"))

    targets = [
        ("e1r_composer", COMPOSER),
        ("e1r_sidecar_sleeve", SIDECAR),
    ]

    for name, path in targets:
        try:
            spec = importlib.util.spec_from_file_location(name, path)
            if spec is None or spec.loader is None:
                out["errors"].append(f"cannot create spec for {path}")
                continue
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            obj_info = {}
            for attr in TARGET_NAMES:
                if hasattr(mod, attr):
                    obj = getattr(mod, attr)
                    info = {"type": type(obj).__name__}
                    try:
                        info["signature"] = str(inspect.signature(obj))
                    except Exception:
                        pass
                    try:
                        info["source_file"] = inspect.getsourcefile(obj)
                        info["source_line"] = inspect.getsourcelines(obj)[1]
                    except Exception:
                        pass
                    obj_info[attr] = info

            # Also list public functions/classes with e1r/equity/variant/core/sidecar names.
            public = {}
            for attr in dir(mod):
                if attr.startswith("_"):
                    continue
                if any(x in attr.lower() for x in ["e1r", "equity", "variant", "core", "sidecar", "return", "record"]):
                    obj = getattr(mod, attr)
                    info = {"type": type(obj).__name__}
                    if callable(obj):
                        try:
                            info["signature"] = str(inspect.signature(obj))
                        except Exception:
                            pass
                    public[attr] = info

            out["objects"][name] = {
                "path": rel(path),
                "target_objects": obj_info,
                "public_relevant_objects": public,
            }

        except Exception as exc:
            out["errors"].append(f"{name}: {type(exc).__name__}: {exc}")

    out["ok"] = len(out["errors"]) == 0
    return out

def infer_contract(defs_by_file: dict[str, Any], grep_by_file: dict[str, Any], import_probe: dict[str, Any]) -> dict[str, Any]:
    findings = []
    risks = []
    next_actions = []

    generator_text = read_text(GENERATOR) if GENERATOR.exists() else ""
    composer_text = read_text(COMPOSER) if COMPOSER.exists() else ""

    has_compose_call_in_generator = "compose_e1r_v0_2_variant" in generator_text
    has_core_var_in_generator = "core_variant_result" in generator_text
    has_sidecar_var_in_generator = "sidecar_result" in generator_text
    has_daily_in_generator = ("daily_equity_records" in generator_text) or ("daily_records" in generator_text) or ("equity_curve" in generator_text)

    has_compose_def = "def compose_e1r_v0_2_variant" in composer_text
    compose_mentions_core = "core_variant_result" in composer_text
    compose_mentions_sidecar = "sidecar_result" in composer_text
    compose_mentions_daily = ("daily_equity_records" in composer_text) or ("daily_records" in composer_text) or ("equity_curve" in composer_text)

    if has_compose_call_in_generator:
        findings.append("Generator references compose_e1r_v0_2_variant.")
    else:
        risks.append("Generator does not directly reference compose_e1r_v0_2_variant; dry-run candidate may be wrapper-only or summary replay.")

    if has_compose_def:
        findings.append("Composer defines compose_e1r_v0_2_variant.")
    else:
        risks.append("Composer definition compose_e1r_v0_2_variant not found by text scan.")

    if has_core_var_in_generator or compose_mentions_core:
        findings.append("core_variant_result is referenced in generator/composer source.")
    else:
        risks.append("core_variant_result not visible in generator/composer source.")

    if has_sidecar_var_in_generator or compose_mentions_sidecar:
        findings.append("sidecar_result is referenced in generator/composer source.")
    else:
        risks.append("sidecar_result not visible in generator/composer source.")

    if has_daily_in_generator or compose_mentions_daily:
        findings.append("daily/equity record names are referenced in generator/composer source.")
    else:
        risks.append("No obvious daily-equity return field in generator/composer text.")

    # Detect whether generator likely writes diagnostic rows.
    if "diagnostic_only" in generator_text:
        findings.append("Generator source references diagnostic_only; persisted equity_curve may be diagnostic, not portfolio-level.")
    if "e1r_v0_2_backtest_equity_curve.json" in generator_text and "e1r_v0_2_backtest_summary.json" in generator_text:
        findings.append("Generator writes both summary and equity_curve export names.")
    if "e1r_v0_2_portfolio_backtest_equity_curve.json" not in generator_text:
        risks.append("Generator does not visibly write portfolio-level E1R canonical filename.")

    next_actions.append("Create a no-write introspection wrapper around compose_e1r_v0_2_variant that captures its actual return object keys and list lengths.")
    next_actions.append("If composer returns only metrics plus diagnostic rows, inspect upstream run_stateful_simulation / run_strategy_variant_comparison return object.")
    next_actions.append("Do not promote exports/e1r_v0_2_backtest_equity_curve.json because 4B-0F-v2 rejected it as symbol/diagnostic rows.")

    return {
        "findings": findings,
        "risks": risks,
        "recommended_next_actions": next_actions,
        "source_flags": {
            "generator_has_compose_call": has_compose_call_in_generator,
            "generator_has_core_variant_result": has_core_var_in_generator,
            "generator_has_sidecar_result": has_sidecar_var_in_generator,
            "generator_has_daily_or_equity_records": has_daily_in_generator,
            "composer_has_compose_def": has_compose_def,
            "composer_mentions_core_variant_result": compose_mentions_core,
            "composer_mentions_sidecar_result": compose_mentions_sidecar,
            "composer_mentions_daily_or_equity_records": compose_mentions_daily,
        },
    }

def main() -> int:
    baseline_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_before = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    defs_by_file = {}
    grep_by_file = {}

    for p in WATCH_FILES:
        if p.exists():
            defs_by_file[rel(p)] = collect_defs(p)
            grep_by_file[rel(p)] = grep_context(p)
        else:
            defs_by_file[rel(p)] = {"path": rel(p), "exists": False}
            grep_by_file[rel(p)] = {"path": rel(p), "exists": False}

    import_probe = module_import_probe()

    post_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_after = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    inference = infer_contract(defs_by_file, grep_by_file, import_probe)

    status = "E1R_GENERATOR_COMPOSER_CONTRACT_AUDIT_COMPLETE_NO_EXECUTION"
    conclusion = "GENERATOR_COMPOSER_CONTRACT_NEEDS_RUNTIME_RETURN_PROBE"
    recommended = "Next run a narrow runtime-return probe around compose_e1r_v0_2_variant to print actual return keys/list lengths without writing canonical exports."

    if inference["source_flags"]["generator_has_compose_call"] and inference["source_flags"]["composer_has_compose_def"]:
        conclusion = "COMPOSER_PATH_CONFIRMED_SOURCE_CONTRACT_STILL_NEEDS_RUNTIME_PROBE"

    report = {
        "generated_at": now(),
        "stage": "B_STAGE_3_8E2F2C4C10F4B0G_GENERATOR_COMPOSER_CONTRACT_AUDIT",
        "status": status,
        "policy": {
            "dashboard_changed": False,
            "workflow_changed": False,
            "strategy_logic_changed": False,
            "e1r_canonical_written": False,
            "portfolio_equity_composed": False,
            "full_backtest_rerun": False,
            "generator_executed": False,
            "composer_executed": False,
            "source_only_audit": True,
        },
        "watched_files": {
            rel(p): {
                "exists": p.exists(),
                "sha256": sha256(p),
                "size": p.stat().st_size if p.exists() else None,
            }
            for p in WATCH_FILES
        },
        "defs_by_file": defs_by_file,
        "grep_by_file": grep_by_file,
        "import_probe": import_probe,
        "inference": inference,
        "conclusion": conclusion,
        "recommended_next_action": recommended,
        "strategy_files_unchanged": baseline_hashes == post_hashes,
        "canonical_existence_unchanged": canonical_before == canonical_after,
        "canonical_after": canonical_after,
        "next_stage": {
            "name": "Stage 3.8E-2F-2C-4C-10F-4B-0H",
            "title": "Runtime return-shape probe for compose_e1r_v0_2_variant",
            "recommended_action": recommended,
        },
    }

    write_json(REPORT_JSON, report)

    # Compact MD
    md = []
    md.append("# Stage 3.8E-2F-2C-4C-10F-4B-0G Generator / Composer Contract Audit")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append(f"- Status: `{status}`")
    md.append("- Source-only audit: `True`")
    md.append("- Generator executed: `False`")
    md.append("- Composer executed: `False`")
    md.append("- E1R canonical written: `False`")
    md.append(f"- Strategy files unchanged: `{report['strategy_files_unchanged']}`")
    md.append(f"- Canonical existence unchanged: `{report['canonical_existence_unchanged']}`")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {recommended}")
    md.append("")
    md.append("## Source Flags")
    md.append("")
    md.append("```json")
    md.append(json.dumps(inference["source_flags"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Findings")
    md.append("")
    for x in inference["findings"]:
        md.append(f"- {x}")
    md.append("")
    md.append("## Risks")
    md.append("")
    for x in inference["risks"]:
        md.append(f"- {x}")
    md.append("")
    md.append("## Import Probe")
    md.append("")
    md.append("```json")
    md.append(json.dumps(import_probe, indent=2, ensure_ascii=False)[:18000])
    md.append("```")
    md.append("")
    md.append("## Relevant Definitions")
    md.append("")
    compact_defs = {}
    for file, obj in defs_by_file.items():
        compact_defs[file] = []
        for d in obj.get("defs", []):
            compact_defs[file].append({
                "name": d.get("name"),
                "type": d.get("type"),
                "line": d.get("line"),
                "end_line": d.get("end_line"),
                "matched_terms": d.get("matched_terms"),
                "assignments_of_interest": d.get("assignments_of_interest", [])[:30],
                "returns": d.get("returns", [])[:20],
            })
    md.append("```json")
    md.append(json.dumps(compact_defs, indent=2, ensure_ascii=False)[:30000])
    md.append("```")
    md.append("")
    md.append("## Grep Context")
    md.append("")
    compact_grep = {}
    for file, obj in grep_by_file.items():
        compact_grep[file] = {
            "hit_count": obj.get("hit_count"),
            "hits": obj.get("hits", [])[:30],
        }
    md.append("```json")
    md.append(json.dumps(compact_grep, indent=2, ensure_ascii=False)[:26000])
    md.append("```")
    md.append("")
    md.append("## Next Stage")
    md.append("")
    md.append(f"- `{report['next_stage']['name']}`: {report['next_stage']['title']}")
    md.append(f"- Recommended action: {report['next_stage']['recommended_action']}")
    md.append("")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("Stage 3.8E-2F-2C-4C-10F-4B-0G source contract audit complete")
    print("status:", status)
    print("strategy_files_unchanged:", report["strategy_files_unchanged"])
    print("canonical_existence_unchanged:", report["canonical_existence_unchanged"])
    print("generator_executed:", report["policy"]["generator_executed"])
    print("composer_executed:", report["policy"]["composer_executed"])
    print("source_flags:", json.dumps(inference["source_flags"], ensure_ascii=False))
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)
    print("import_probe_ok:", import_probe.get("ok"))
    print("import_probe_errors:", json.dumps(import_probe.get("errors"), ensure_ascii=False))
    print("next_stage:", report["next_stage"]["name"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
