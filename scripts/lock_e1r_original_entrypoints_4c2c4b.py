#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import inspect
import importlib
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]

REPORT_JSON = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json"
REPORT_MD = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.md"

SOURCE_FILES = [
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/backtest.py",
    ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0G_GENERATOR_COMPOSER_CONTRACT_AUDIT.json",
    ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
    ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
    ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10E_R_CONTINUOUS_CAPITAL_CONTRACT.json",
    ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
]

KEYWORDS = [
    "compose_e1r_v0_2_variant",
    "build_e1r_sidecar_sleeve",
    "run_stateful_simulation",
    "E1R_UPTREND_CONFIRMED",
    "E1R_UPTREND_EMERGING",
    "SIDEWAYS",
    "MA_CONFLICT",
    "DETERIORATION_TRANSITION",
    "RECOVERY_TRANSITION",
    "DOWNTREND",
    "selected_count_max",
    "gross_exposure",
    "max_positions",
    "candidate_top_n",
    "entry_top_n",
    "open_positions_count",
]

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))

def write_json(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def read_text(p: Path) -> str:
    return p.read_text(errors="replace")

def extract_keyword_context(path: Path):
    if not path.exists():
        return {"path": rel(path), "exists": False, "hits": []}

    text = read_text(path)
    lines = text.splitlines()
    hits = []

    for i, line in enumerate(lines, start=1):
        for kw in KEYWORDS:
            if kw in line:
                start = max(1, i - 3)
                end = min(len(lines), i + 3)
                context = [
                    {"line": j, "text": lines[j - 1][:260]}
                    for j in range(start, end + 1)
                ]
                hits.append({
                    "line": i,
                    "keyword": kw,
                    "text": line.strip()[:300],
                    "context": context,
                })

    return {
        "path": rel(path),
        "exists": True,
        "hit_count": len(hits),
        "hits": hits[:120],
    }

def ast_functions(path: Path):
    if not path.exists() or path.suffix != ".py":
        return []

    text = read_text(path)
    tree = ast.parse(text)
    funcs = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            name = node.name
            src = ast.get_source_segment(text, node) or ""
            matched = [kw for kw in KEYWORDS if kw in src or kw in name]
            if matched:
                funcs.append({
                    "path": rel(path),
                    "function": name,
                    "line": node.lineno,
                    "matched_keywords": matched,
                    "args": [a.arg for a in node.args.args],
                    "source_head": "\n".join(src.splitlines()[:80]),
                })

    return funcs

def import_function_signatures():
    sys.path.insert(0, str(ROOT))
    targets = [
        ("src.engine.e1r_composer", ["compose_e1r_v0_2_variant", "extract_core_interval_returns", "build_equity_records_from_returns"]),
        ("src.engine.e1r_sidecar_sleeve", ["build_e1r_sidecar_sleeve"]),
        ("src.engine.backtest", ["run_stateful_simulation"]),
    ]

    out = []
    for mod_name, names in targets:
        item = {"module": mod_name, "import_ok": False, "functions": []}
        try:
            mod = importlib.import_module(mod_name)
            item["import_ok"] = True
            for name in names:
                fn = getattr(mod, name, None)
                item["functions"].append({
                    "name": name,
                    "exists": fn is not None,
                    "signature": str(inspect.signature(fn)) if fn else None,
                })
        except Exception as exc:
            item["error"] = type(exc).__name__ + ": " + str(exc)
        out.append(item)

    return out

def parse_json_extracts(path: Path):
    if not path.exists() or path.suffix != ".json":
        return None

    try:
        obj = json.loads(path.read_text())
    except Exception as exc:
        return {"path": rel(path), "json_ok": False, "error": str(exc)}

    text = json.dumps(obj, ensure_ascii=False)

    extracts = {}
    for kw in KEYWORDS:
        if kw in text:
            idx = text.find(kw)
            extracts[kw] = text[max(0, idx - 500): idx + 1200]

    return {
        "path": rel(path),
        "json_ok": True,
        "top_keys": sorted(obj.keys())[:80] if isinstance(obj, dict) else None,
        "keyword_extracts": extracts,
    }

def main():
    contexts = [extract_keyword_context(p) for p in SOURCE_FILES]
    funcs = []
    for p in SOURCE_FILES:
        funcs.extend(ast_functions(p))

    signatures = import_function_signatures()
    json_extracts = [parse_json_extracts(p) for p in SOURCE_FILES if p.suffix == ".json"]

    # Conservative lock result: only lock what source files prove exists.
    locked = {
        "uptrend_candidate_entrypoint": {
            "status": "LOCKED_IF_COMPOSER_CONTRACT_CONFIRMS",
            "module": "src.engine.e1r_composer",
            "function": "compose_e1r_v0_2_variant",
            "reason": "This is the recovered E1R composer entrypoint; must be verified to preserve original UPTREND branch, not replaced.",
        },
        "sideways_sidecar_entrypoint": {
            "status": "LOCKED_IF_SIDECAR_CONTRACT_CONFIRMS",
            "module": "src.engine.e1r_sidecar_sleeve",
            "function": "build_e1r_sidecar_sleeve",
            "reason": "This is the recovered sidecar sleeve builder; must be used as original SIDEWAYS/MA_CONFLICT source, with Top10 as candidate pool only.",
        },
        "full_account_engine": {
            "status": "AVAILABLE_BUT_REQUIRES_ADAPTER_GUARD",
            "module": "src.engine.backtest",
            "function": "run_stateful_simulation",
            "reason": "Prior 4C-2C full run used this engine but violated max holdings. Any adapter must enforce account holdings <=3 and must not alter strategy rules.",
        },
    }

    validation_questions = [
        {
            "topic": "UPTREND",
            "must_confirm": "compose_e1r_v0_2_variant contains original UPTREND branch, especially E1R_UPTREND_CONFIRMED, without newly invented entry/exit logic.",
        },
        {
            "topic": "SIDEWAYS / MA_CONFLICT",
            "must_confirm": "build_e1r_sidecar_sleeve is the original validated sidecar source; selected_count_max/Top10 remains candidate pool, not live holdings.",
        },
        {
            "topic": "DETERIORATION / RECOVERY",
            "must_confirm": "Whether original sidecar included only MA_CONFLICT or also DETERIORATION/RECOVERY. If not proven, keep DETERIORATION/RECOVERY cash/defensive.",
        },
        {
            "topic": "DOWNTREND",
            "must_confirm": "No normal buy execution. Cash/defensive only.",
        },
        {
            "topic": "Global account cap",
            "must_confirm": "Adapter/engine output open_positions_count never exceeds 3.",
        },
    ]

    report = {
        "generated_at": now(),
        "stage": "E1R_COMBINED_5Y_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK",
        "status": "ORIGINAL_ENTRYPOINT_LOCK_AUDIT_COMPLETE_NO_STRATEGY_CHANGE_NO_BACKTEST",
        "policy": {
            "strategy_logic_changed": False,
            "backtest_run": False,
            "dashboard_changed": False,
            "purpose": "Lock original executable entrypoints before 5Y combined rerun.",
        },
        "function_signatures": signatures,
        "ast_functions": funcs,
        "keyword_contexts": contexts,
        "json_extracts": json_extracts,
        "locked_entrypoints": locked,
        "validation_questions_before_rerun": validation_questions,
        "conclusion": "ENTRYPOINTS_IDENTIFIED_BUT_COMBINED_ADAPTER_STILL_NEEDS_EXPLICIT_NO_STRATEGY_CHANGE_GUARDS",
        "recommended_next_action": "Create 4C-2C-4C adapter dry-run/smoke that calls these original entrypoints only, enforces global holdings <=3, and reports branch usage before full 5Y run.",
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R Combined 5Y — 4C-2C-4B Original Entrypoint Lock")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Policy")
    md.append("```json")
    md.append(json.dumps(report["policy"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Function Signatures")
    md.append("```json")
    md.append(json.dumps(signatures, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Locked Entrypoints")
    md.append("```json")
    md.append(json.dumps(locked, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Validation Questions Before Rerun")
    md.append("```json")
    md.append(json.dumps(validation_questions, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## AST Functions")
    md.append("```json")
    md.append(json.dumps(funcs, indent=2, ensure_ascii=False)[:30000])
    md.append("```")
    md.append("")
    md.append("## Keyword Contexts")
    md.append("```json")
    md.append(json.dumps(contexts, indent=2, ensure_ascii=False)[:50000])
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append(f"- `{report['conclusion']}`")
    md.append(f"- Recommended: {report['recommended_next_action']}")
    md.append("")
    REPORT_MD.write_text("\n".join(md) + "\n")

    print("E1R_COMBINED_5Y_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("function_signatures:", json.dumps(signatures, ensure_ascii=False))
    print("locked_entrypoints:", json.dumps(locked, ensure_ascii=False))
    print("validation_questions_before_rerun:", json.dumps(validation_questions, ensure_ascii=False))
    print("conclusion:", report["conclusion"])
    print("recommended_next_action:", report["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
