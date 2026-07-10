#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import hashlib
import re
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

BACKTEST = ROOT / "src/engine/backtest.py"
K2_RCA = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_RCA_MARKET_GATE_ROOT_CAUSE_ANALYSIS.json"

REPORT_JSON = ROOT / "docs/research/E1R_K2_R4_SOURCE_DEPENDENCY_TRACE.json"
REPORT_MD = ROOT / "docs/research/E1R_K2_R4_SOURCE_DEPENDENCY_TRACE.md"
ARCH_MD = ROOT / "docs/architecture/E1R_K2_R4_SOURCE_DEPENDENCY_TRACE.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_r4_source_dependency_trace.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
]

TARGET_NAMES = [
    "_gate_state",
    "market_entry_allowed",
    "market_risk_off",
    "market_shock",
    "spx_close_t",
    "spx_ma50_t",
    "spx_day_return",
    "risk_off_below_spx_ma50",
    "market_shock_daily_return",
    "market_gate_enabled",
    "market_shock_gate_enabled",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except Exception:
        return str(path)


def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def find_function_bounds(source: str, fn_name: str) -> dict[str, Any]:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == fn_name:
            return {
                "name": node.name,
                "start_line": node.lineno,
                "end_line": getattr(node, "end_lineno", node.lineno),
                "line_count": getattr(node, "end_lineno", node.lineno) - node.lineno + 1,
            }
    raise RuntimeError(f"function not found: {fn_name}")


def context(lines: list[str], line_no: int, radius: int = 8) -> dict[str, Any]:
    start = max(1, line_no - radius)
    end = min(len(lines), line_no + radius)
    return {
        "start": start,
        "end": end,
        "rows": [
            {"line": i, "text": lines[i - 1].rstrip()}
            for i in range(start, end + 1)
        ],
    }


def scan_name_occurrences(lines: list[str], bounds: dict[str, Any], name: str) -> list[dict[str, Any]]:
    pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])")
    out = []
    for i in range(bounds["start_line"], bounds["end_line"] + 1):
        text = lines[i - 1]
        if pattern.search(text):
            stripped = text.strip()
            kind = "reference"
            if re.search(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])\s*=", text):
                kind = "assignment"
            elif stripped.startswith("if ") or stripped.startswith("elif "):
                kind = "control"
            elif "append({" in text or f'"{name}"' in text or f"'{name}'" in text:
                kind = "output"
            out.append({
                "line": i,
                "kind": kind,
                "indent": len(text) - len(text.lstrip(" ")),
                "text": text.rstrip(),
                "context": context(lines, i, radius=6),
            })
    return out


def extract_assigned_names_from_expr(expr: str) -> list[str]:
    try:
        tree = ast.parse(expr, mode="eval")
    except Exception:
        try:
            tree = ast.parse(expr)
        except Exception:
            return []
    names = sorted({node.id for node in ast.walk(tree) if isinstance(node, ast.Name)})
    return names


def assignment_rhs(text: str, name: str) -> str | None:
    m = re.search(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])\s*=\s*(.*)$", text)
    if not m:
        return None
    return m.group(1).strip()


def build_dependency_table(lines: list[str], bounds: dict[str, Any]) -> dict[str, Any]:
    table = {}

    for name in TARGET_NAMES:
        occurrences = scan_name_occurrences(lines, bounds, name)
        assignments = [x for x in occurrences if x["kind"] == "assignment"]
        controls = [x for x in occurrences if x["kind"] == "control"]
        outputs = [x for x in occurrences if x["kind"] == "output"]

        deps = []
        for a in assignments:
            rhs = assignment_rhs(a["text"], name)
            deps.append({
                "assignment_line": a["line"],
                "rhs": rhs,
                "rhs_names": extract_assigned_names_from_expr(rhs or ""),
                "text": a["text"],
            })

        table[name] = {
            "occurrence_count": len(occurrences),
            "assignment_count": len(assignments),
            "control_count": len(controls),
            "output_count": len(outputs),
            "assignments": assignments,
            "controls": controls,
            "outputs": outputs,
            "dependency_candidates": deps,
            "all_occurrences": occurrences,
        }

    return table


def build_required_chain(table: dict[str, Any]) -> dict[str, Any]:
    chain = {}

    for name in ["_gate_state", "market_entry_allowed", "market_risk_off", "market_shock"]:
        item = table.get(name, {})
        chain[name] = {
            "assignment_lines": [
                {
                    "line": x["line"],
                    "text": x["text"],
                    "rhs_names": d.get("rhs_names", []),
                }
                for x, d in zip(item.get("assignments", []), item.get("dependency_candidates", []))
            ],
            "reference_lines": [
                {"line": x["line"], "kind": x["kind"], "text": x["text"]}
                for x in item.get("all_occurrences", [])
            ],
        }

    return chain


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    if not BACKTEST.exists():
        raise FileNotFoundError(BACKTEST)
    if not K2_RCA.exists():
        raise FileNotFoundError(K2_RCA)

    rca = read_json(K2_RCA)
    if rca.get("decision", {}).get("formula_patch_allowed_now") is not False:
        raise RuntimeError("RCA state unexpected: formula patch should still be blocked.")

    source = BACKTEST.read_text()
    lines = source.splitlines()
    bounds = find_function_bounds(source, "run_stateful_simulation")

    dependency_table = build_dependency_table(lines, bounds)
    required_chain = build_required_chain(dependency_table)

    # `_gate_state` may be assigned in multiline if/else form; also search broadly for exact token.
    gate_state_occurrences = dependency_table["_gate_state"]["all_occurrences"]

    unresolved = []

    if dependency_table["_gate_state"]["assignment_count"] == 0:
        unresolved.append({
            "id": "U1",
            "reason": "_gate_state assignment line not found by exact assignment scanner.",
            "blocking": True,
        })

    for name in ["market_entry_allowed", "market_risk_off", "market_shock"]:
        if dependency_table[name]["assignment_count"] == 0:
            unresolved.append({
                "id": f"{name}_assignment_missing",
                "reason": f"{name} assignment line not found.",
                "blocking": True,
            })

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "source_dependency_trace_complete": True,
        "strategy_logic_changed": False,
        "audit_only": True,
        "formula_not_patched": True,
        "backtest_engine_run": False,
        "full_5y_backtest_run": False,
        "forward_runner_run": False,
        "candidate_generation_extracted": False,
        "buy_add_reduce_exit_extracted": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "k2_rca_loaded": True,
        "run_stateful_simulation_bounds_found": bounds["line_count"] > 0,
        "dependency_table_built": True,
        "_gate_state_occurrences_found": len(gate_state_occurrences) > 0,
        "_gate_state_assignment_found": dependency_table["_gate_state"]["assignment_count"] > 0,
        "market_entry_allowed_assignment_found": dependency_table["market_entry_allowed"]["assignment_count"] > 0,
        "market_risk_off_assignment_found": dependency_table["market_risk_off"]["assignment_count"] > 0,
        "market_shock_assignment_found": dependency_table["market_shock"]["assignment_count"] > 0,
        "unresolved_blocking_count": len([x for x in unresolved if x.get("blocking")]),
    }

    decision = {
        "k2_r4_source_dependency_trace_passed": all([
            validations["strategy_files_unchanged"],
            validations["dependency_table_built"],
            validations["_gate_state_assignment_found"],
            validations["market_entry_allowed_assignment_found"],
            validations["market_risk_off_assignment_found"],
            validations["market_shock_assignment_found"],
            validations["unresolved_blocking_count"] == 0,
        ]),
        "implementation_may_resume": False,
        "formula_patch_allowed_now": False,
        "candidate_extraction_allowed_now": False,
        "unresolved": unresolved,
        "next_stage_if_pass": "K2-R5: formula patch proposal with source-line citations",
        "next_stage_if_fail": "K2-R4B: targeted multiline/source parser for unresolved variables",
        "conclusion": (
            "K2_R4_PASS_READY_FOR_PATCH_PROPOSAL"
            if len(unresolved) == 0
            else "K2_R4_NEEDS_TARGETED_DEPENDENCY_TRACE"
        ),
        "recommended_next_action": (
            "If unresolved is empty, prepare K2-R5 patch proposal citing exact source lines. "
            "If unresolved exists, run targeted trace only for missing variables."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "K2-R4",
        "full_stage_name": "4C-2C-4E-ENGINE-K2-R4-SOURCE_DEPENDENCY_TRACE",
        "status": "SOURCE_DEPENDENCY_TRACE_COMPLETE",
        "purpose": "Trace `_gate_state` and upstream market gate variables to source assignment lines before any formula patch.",
        "policy": {
            "strategy_logic_changed": False,
            "audit_only": True,
            "formula_not_patched": True,
            "backtest_engine_run": False,
            "full_5y_backtest_run": False,
            "forward_runner_run": False,
            "candidate_generation_extracted": False,
            "buy_add_reduce_exit_extracted": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
        },
        "source": {
            "backtest_path": rel(BACKTEST),
            "backtest_sha256": sha256(BACKTEST),
            "function_bounds": bounds,
            "k2_rca": rel(K2_RCA),
        },
        "required_chain": required_chain,
        "dependency_table": dependency_table,
        "unresolved": unresolved,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)

    md = []
    md.append("# E1R K2-R4 — Source Dependency Trace")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("Full stage name: `4C-2C-4E-ENGINE-K2-R4-SOURCE_DEPENDENCY_TRACE`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Required Chain")
    md.append("```json")
    md.append(json.dumps(required_chain, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Unresolved")
    md.append("```json")
    md.append(json.dumps(unresolved, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Validations")
    md.append("```json")
    md.append(json.dumps(validations, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Decision")
    md.append("```json")
    md.append(json.dumps(decision, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")

    REPORT_MD.write_text("\n".join(md))
    ARCH_MD.write_text("\n".join(md))

    print("E1R_K2_R4_SOURCE_DEPENDENCY_TRACE_COMPLETE")
    print("status:", report["status"])
    print("source:", json.dumps(report["source"], ensure_ascii=False))
    print("")
    print("=== REQUIRED CHAIN ===")
    print(json.dumps(required_chain, indent=2, ensure_ascii=False))
    print("")
    print("=== UNRESOLVED ===")
    print(json.dumps(unresolved, indent=2, ensure_ascii=False))
    print("")
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(AUDIT_JSON))


if __name__ == "__main__":
    main()
