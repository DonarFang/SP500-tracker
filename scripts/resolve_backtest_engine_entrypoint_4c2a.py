#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import hashlib
import importlib.util
import inspect
import runpy
import sys
import traceback
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

BACKTEST = ROOT / "src/engine/backtest.py"
REPORT_JSON = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.json"
REPORT_MD = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT_REPORT.md"

FROZEN_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

SEARCH_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

for base in [ROOT / "scripts", ROOT / "src"]:
    if base.exists():
        for p in base.rglob("*.py"):
            if p not in SEARCH_FILES:
                SEARCH_FILES.append(p)

TARGET_TERMS = [
    "run_stateful_simulation",
    "run_strategy_variant_comparison",
    "portfolio_backtest",
    "daily_records",
    "total_equity",
    "portfolio_value",
    "positions_value",
    "open_positions_count",
    "market_gate_state",
    "spx_regime",
    "e1r_active_mode",
    "selected_variant",
    "variant_results",
    "cash",
    "pending_orders",
    "risk_budget",
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

def try_import_backtest() -> dict[str, Any]:
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "src"))

    out = {
        "attempted": True,
        "ok": False,
        "error": None,
        "traceback_tail": None,
        "objects": {},
    }

    try:
        spec = importlib.util.spec_from_file_location("backtest_4c2a", BACKTEST)
        if spec is None or spec.loader is None:
            raise RuntimeError("cannot create import spec")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)

        out["ok"] = True

        for name in dir(mod):
            if name.startswith("_"):
                continue
            lower = name.lower()
            if any(k in lower for k in ["backtest", "simulation", "portfolio", "variant", "stateful", "run"]):
                obj = getattr(mod, name)
                item = {"type": type(obj).__name__}
                if callable(obj):
                    try:
                        item["signature"] = str(inspect.signature(obj))
                    except Exception as exc:
                        item["signature_error"] = type(exc).__name__ + ": " + str(exc)
                out["objects"][name] = item

    except Exception as exc:
        out["error"] = type(exc).__name__ + ": " + str(exc)
        out["traceback_tail"] = traceback.format_exc()[-12000:]

    return out

def ast_scan(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": rel(path), "exists": False}

    text = path.read_text(errors="replace")
    result = {
        "path": rel(path),
        "exists": True,
        "function_defs": [],
        "class_defs": [],
        "imports": [],
        "calls": [],
        "grep_hits": [],
        "if_main_blocks": [],
    }

    lines = text.splitlines()

    for i, line in enumerate(lines, start=1):
        matched = [t for t in TARGET_TERMS if t in line]
        if matched:
            lo = max(1, i - 4)
            hi = min(len(lines), i + 4)
            result["grep_hits"].append({
                "line": i,
                "matched": matched,
                "context": [
                    {"line": j, "text": lines[j - 1][:1000]}
                    for j in range(lo, hi + 1)
                ],
            })

    try:
        tree = ast.parse(text)
    except Exception as exc:
        result["parse_error"] = type(exc).__name__ + ": " + str(exc)
        return result

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            result["imports"].append({
                "line": node.lineno,
                "names": [a.name for a in node.names],
            })

        if isinstance(node, ast.ImportFrom):
            result["imports"].append({
                "line": node.lineno,
                "module": node.module,
                "names": [a.name for a in node.names],
            })

        if isinstance(node, ast.FunctionDef):
            name = node.name
            score = 0
            lower = name.lower()

            if any(k in lower for k in ["backtest", "simulation", "portfolio", "variant", "stateful", "run"]):
                score += 30
            body_text = ast.get_source_segment(text, node) or ""
            for t in TARGET_TERMS:
                if t in body_text:
                    score += 5

            if score > 0:
                result["function_defs"].append({
                    "name": name,
                    "line": node.lineno,
                    "end_line": getattr(node, "end_lineno", node.lineno),
                    "args": [a.arg for a in node.args.args],
                    "score": score,
                    "returns_annotation": ast.unparse(node.returns) if node.returns else None,
                    "body_head": "\n".join(body_text.splitlines()[:80]),
                })

        if isinstance(node, ast.ClassDef):
            lower = node.name.lower()
            if any(k in lower for k in ["backtest", "portfolio", "simulation", "strategy", "engine"]):
                result["class_defs"].append({
                    "name": node.name,
                    "line": node.lineno,
                    "end_line": getattr(node, "end_lineno", node.lineno),
                })

        if isinstance(node, ast.Call):
            call_name = None
            if isinstance(node.func, ast.Name):
                call_name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                call_name = node.func.attr

            if call_name and any(k in call_name.lower() for k in ["backtest", "simulation", "portfolio", "variant", "stateful", "run"]):
                result["calls"].append({
                    "line": getattr(node, "lineno", None),
                    "call": call_name,
                })

        if isinstance(node, ast.If):
            test_src = ast.unparse(node.test)
            if "__name__" in test_src and "__main__" in test_src:
                result["if_main_blocks"].append({
                    "line": node.lineno,
                    "test": test_src,
                    "body_calls": [
                        ast.unparse(x)[:500]
                        for x in node.body
                    ],
                })

    result["function_defs"] = sorted(result["function_defs"], key=lambda x: (-x["score"], x["line"]))[:80]
    result["calls"] = result["calls"][:120]
    result["grep_hits"] = result["grep_hits"][:120]

    return result

def rank_entrypoint_candidates(scans: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = []

    for path, scan in scans.items():
        for f in scan.get("function_defs", []):
            name = f["name"]
            lower = name.lower()
            score = f.get("score", 0)

            if "stateful" in lower:
                score += 80
            if "simulation" in lower:
                score += 60
            if "portfolio" in lower:
                score += 50
            if "backtest" in lower:
                score += 40
            if "variant" in lower:
                score += 30
            if name.startswith("run_"):
                score += 20

            body = f.get("body_head", "")
            if "daily_records" in body:
                score += 30
            if "total_equity" in body or "portfolio_value" in body:
                score += 30
            if "cash" in body:
                score += 20
            if "positions_value" in body or "market_value" in body:
                score += 20
            if "spx_regime" in body or "market_gate_state" in body:
                score += 20

            candidates.append({
                "source": path,
                "name": name,
                "line": f.get("line"),
                "end_line": f.get("end_line"),
                "args": f.get("args"),
                "score": score,
                "body_head": body,
            })

    return sorted(candidates, key=lambda x: (-x["score"], x["source"], x["line"]))[:40]

def main() -> int:
    baseline_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}

    import_probe = try_import_backtest()
    scans = {}

    for p in SEARCH_FILES:
        if p.exists() and p.suffix == ".py":
            scans[rel(p)] = ast_scan(p)

    entrypoint_candidates = rank_entrypoint_candidates(scans)

    top = entrypoint_candidates[0] if entrypoint_candidates else None

    if import_probe["ok"] and top:
        conclusion = "BACKTEST_IMPORT_OK_AND_ENTRYPOINT_CANDIDATE_FOUND"
        recommended = "Proceed to 4C-2B: smoke invoke the top entrypoint with no-write / limited window."
    elif top:
        conclusion = "BACKTEST_IMPORT_FAILED_BUT_STATIC_ENTRYPOINT_CANDIDATE_FOUND"
        recommended = "Patch import path/environment in a thin adapter, then smoke invoke top static entrypoint."
    else:
        conclusion = "NO_STATEFUL_ENTRYPOINT_CANDIDATE_FOUND"
        recommended = "Create a new full-account engine adapter explicitly from existing data contracts before running full 5Y."

    post_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}

    report = {
        "generated_at": now(),
        "stage": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2A_ENGINE_ENTRYPOINT",
        "status": "E1R_UNIFIED_ENGINE_ENTRYPOINT_RESOLUTION_COMPLETE_NO_BACKTEST",
        "policy": {
            "dashboard_changed": False,
            "strategy_logic_changed": False,
            "full_backtest_run": False,
            "canonical_backtest_written": False,
            "source_only_plus_import_probe": True,
        },
        "import_probe": import_probe,
        "entrypoint_candidates": entrypoint_candidates,
        "top_entrypoint_candidate": top,
        "source_scans": scans,
        "conclusion": conclusion,
        "recommended_next_action": recommended,
        "strategy_files_unchanged": baseline_hashes == post_hashes,
        "next_stage": {
            "name": "4C-2B",
            "title": "Smoke invoke unified backtest entrypoint or build thin adapter",
            "recommended_action": recommended,
        },
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R Unified 5Y Full Account V1 — 4C-2A Engine Entrypoint Resolution")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append("- Status: `E1R_UNIFIED_ENGINE_ENTRYPOINT_RESOLUTION_COMPLETE_NO_BACKTEST`")
    md.append("- Full backtest run: `False`")
    md.append("- Strategy logic changed: `False`")
    md.append("- Canonical backtest written: `False`")
    md.append("")
    md.append("## Import Probe")
    md.append("")
    md.append("```json")
    md.append(json.dumps({
        "ok": import_probe.get("ok"),
        "error": import_probe.get("error"),
        "traceback_tail": import_probe.get("traceback_tail"),
        "objects": import_probe.get("objects"),
    }, indent=2, ensure_ascii=False)[:20000])
    md.append("```")
    md.append("")
    md.append("## Top Entrypoint Candidates")
    md.append("")
    md.append("```json")
    md.append(json.dumps(entrypoint_candidates[:12], indent=2, ensure_ascii=False)[:26000])
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {recommended}")
    md.append("")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("Stage 4C-2A engine entrypoint resolution complete")
    print("status:", report["status"])
    print("strategy_files_unchanged:", report["strategy_files_unchanged"])
    print("backtest_import_ok:", import_probe.get("ok"))
    print("backtest_import_error:", import_probe.get("error"))
    if import_probe.get("traceback_tail"):
        print("backtest_import_traceback_tail:", import_probe.get("traceback_tail")[-2000:])
    print("entrypoint_candidate_count:", len(entrypoint_candidates))
    if top:
        print("top_entrypoint_source:", top["source"])
        print("top_entrypoint_name:", top["name"])
        print("top_entrypoint_line:", top["line"])
        print("top_entrypoint_args:", top["args"])
        print("top_entrypoint_score:", top["score"])
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)
    print("next_stage:", report["next_stage"]["name"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
