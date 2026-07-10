#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

K2_R1 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R1_MARKET_GATE_FORMULA_AUDIT.json"
K2_R2 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R2_MARKET_GATE_SOURCE_TRACE.json"
K2_R3 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R3_MARKET_GATE_SOURCE_LINE_DRILLDOWN.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_RCA_MARKET_GATE_ROOT_CAUSE_ANALYSIS.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_RCA_MARKET_GATE_ROOT_CAUSE_ANALYSIS.md"
ARCH_MD = ROOT / "docs/architecture/E1R_MARKET_GATE_RCA_AND_RECOVERY_PLAN.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_engine_k2_rca_market_gate_root_cause_analysis.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
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


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    for p in [K2_R1, K2_R2, K2_R3]:
        if not p.exists():
            raise FileNotFoundError(f"Missing prerequisite: {rel(p)}")

    r1 = read_json(K2_R1)
    r2 = read_json(K2_R2)
    r3 = read_json(K2_R3)

    evidence = {
        "k2_r1_formula_audit": {
            "status": r1.get("status"),
            "expected_summary": r1.get("expected_summary"),
            "basic_formula_mismatch_count": r1.get("decision", {}).get("basic_formula_mismatch_count"),
            "exact_formula_candidates": r1.get("decision", {}).get("exact_formula_candidates"),
            "requires_source_formula_patch": r1.get("decision", {}).get("requires_source_formula_patch"),
            "source": rel(K2_R1),
        },
        "k2_r2_source_trace": {
            "status": r2.get("status"),
            "source": r2.get("source"),
            "hit_summary": r2.get("hit_summary"),
            "critical_cluster_count": r2.get("decision", {}).get("critical_cluster_count"),
            "best_diagnostic_hypotheses": r2.get("decision", {}).get("best_diagnostic_hypotheses"),
            "source_file": rel(K2_R2),
        },
        "k2_r3_source_line_drilldown": {
            "status": r3.get("status"),
            "important_line_numbers": r3.get("trace_graph", {}).get("important_line_numbers"),
            "assignment_lines": r3.get("trace_graph", {}).get("assignment_lines"),
            "control_lines": r3.get("trace_graph", {}).get("control_lines"),
            "source_file": rel(K2_R3),
        },
    }

    confirmed_findings = [
        {
            "id": "F1",
            "finding": "The simplified K2 market gate formula is not equivalent to legacy output.",
            "evidence": {
                "expected_distribution": r1.get("expected_summary", {}).get("distribution"),
                "basic_formula_mismatch_count": r1.get("decision", {}).get("basic_formula_mismatch_count"),
                "exact_formula_candidates": r1.get("decision", {}).get("exact_formula_candidates"),
            },
            "impact": "Standalone market gate cannot proceed to candidate extraction until fixed.",
        },
        {
            "id": "F2",
            "finding": "The legacy RISK_OFF days in the golden master are not explained by same-day SPX close < same-day SPX MA50.",
            "evidence": r1.get("expected_summary", {}).get("examples", {}).get("RISK_OFF"),
            "impact": "Formula must be traced from source variables, not inferred from rounded daily output fields.",
        },
        {
            "id": "F3",
            "finding": "daily_equity_records.market_gate_state stores `_gate_state`; logging/daily_records use a separate local expression based on market_entry_allowed / market_shock.",
            "evidence": {
                "daily_equity_record_line": "L1525: \"market_gate_state\": _gate_state",
                "logging_gate_lines": [
                    "L2137: gate_state = \"ALLOW\" if market_entry_allowed else (",
                    "L2138:     \"SHOCK\" if market_shock else \"RISK_OFF\"",
                    "L2155-L2158: daily_records market_gate_state uses market_entry_allowed / market_shock",
                ],
                "source": rel(K2_R3),
            },
            "impact": "The extraction target must be explicitly chosen: daily_equity_records._gate_state, not logger gate_state unless proven identical.",
        },
    ]

    unknowns = [
        {
            "id": "U1",
            "unknown": "Exact assignment location and computation chain for `_gate_state` before line 1525.",
            "required_evidence": "Source lines showing `_gate_state = ...` and all variables feeding that assignment.",
            "blocking": True,
        },
        {
            "id": "U2",
            "unknown": "Exact computation chain for `market_entry_allowed`, `market_risk_off`, and `market_shock` on every day.",
            "required_evidence": "Source lines for assignments and updates, plus row-level replay trace.",
            "blocking": True,
        },
        {
            "id": "U3",
            "unknown": "Whether `_gate_state` is based on current-day values, previous-day values, execution-day alignment, or rounded/unrounded source arrays.",
            "required_evidence": "Variable-level trace for dates 2021-05-03 through 2021-05-24 and 2021-06-18.",
            "blocking": True,
        },
    ]

    root_causes = [
        {
            "id": "RC1",
            "category": "Evidence discipline",
            "root_cause": "Implementation was attempted from an inferred formula before the exact source assignment chain was located.",
            "corrective_action": "No extraction implementation until source assignment line and dependencies are identified.",
        },
        {
            "id": "RC2",
            "category": "Field identity",
            "root_cause": "Different gate-related fields were treated as equivalent: `_gate_state`, `gate_state`, and market_entry_allowed-derived state.",
            "corrective_action": "Define a field identity table before patching: source field, assignment line, consumer, and equivalence target.",
        },
        {
            "id": "RC3",
            "category": "Process control",
            "root_cause": "After the first mismatch, the process continued into multiple audit stages without an explicit RCA gate.",
            "corrective_action": "Introduce a three-strike stop rule and RCA requirement for repeated failures around the same issue.",
        },
        {
            "id": "RC4",
            "category": "Trace quality",
            "root_cause": "Existing golden master trace lacks variable-level market gate internals, so formula reconstruction from output rows alone is underdetermined.",
            "corrective_action": "Add an audit-only variable trace script that reads source/output and reports exact dependencies before any patch.",
        },
    ]

    recovery_plan = {
        "stage": "4C-2C-4E-ENGINE-K2-RCA",
        "status": "STOP_IMPLEMENTATION_UNTIL_RCA_ACCEPTED",
        "do_not_do_next": [
            "Do not patch compute_market_gate_state yet.",
            "Do not proceed to candidate/ranking extraction.",
            "Do not run full 5Y.",
            "Do not generate official/dashboard result.",
            "Do not infer a formula from output rows alone.",
        ],
        "required_next_stage": "4C-2C-4E-ENGINE-K2-R4-SOURCE_DEPENDENCY_TRACE",
        "required_next_stage_scope": [
            "Search explicitly for `_gate_state` assignment in src/engine/backtest.py.",
            "Search explicitly for `market_entry_allowed`, `market_risk_off`, and `market_shock` assignments.",
            "Build a variable dependency table with line numbers.",
            "Generate focused source snippets around each assignment.",
            "Extract row-level values for the mismatch window from the legacy run if available.",
            "Only after this dependency trace passes, write K2-R5 formula patch.",
        ],
        "acceptance_criteria_before_formula_patch": [
            "`_gate_state` assignment line is found.",
            "Every variable used by `_gate_state` is traced to a source line.",
            "Extraction target is explicitly confirmed as `daily_equity_records.market_gate_state`.",
            "No unresolved unknowns U1-U3 remain.",
            "Patch proposal cites exact source lines.",
        ],
        "process_rule_added": {
            "three_strike_rule": (
                "If the same issue fails or is corrected incorrectly around three times, "
                "stop implementation and perform RCA before continuing."
            ),
            "evidence_rule": (
                "No source-code extraction patch may be implemented from assumption. "
                "The patch must cite source lines, logs, or test evidence."
            ),
        },
    }

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "rca_complete": True,
        "implementation_paused": True,
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
        "k2_r1_loaded": True,
        "k2_r2_loaded": True,
        "k2_r3_loaded": True,
        "confirmed_findings_documented": len(confirmed_findings) >= 3,
        "unknowns_documented": len(unknowns) >= 3,
        "root_causes_documented": len(root_causes) >= 4,
        "recovery_plan_defined": True,
        "three_strike_rule_added": True,
        "evidence_rule_added": True,
    }

    decision = {
        "k2_rca_passed": all([
            validations["rca_complete"],
            validations["implementation_paused"],
            validations["strategy_files_unchanged"],
            validations["confirmed_findings_documented"],
            validations["unknowns_documented"],
            validations["root_causes_documented"],
            validations["recovery_plan_defined"],
        ]),
        "implementation_may_resume": False,
        "formula_patch_allowed_now": False,
        "candidate_extraction_allowed_now": False,
        "required_next_stage": recovery_plan["required_next_stage"],
        "conclusion": "K2_RCA_PASS_IMPLEMENTATION_PAUSED_READY_FOR_SOURCE_DEPENDENCY_TRACE",
        "recommended_next_action": (
            "Run K2-R4 source dependency trace to find `_gate_state` and all upstream variables before any formula patch."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-RCA",
        "status": "MARKET_GATE_ROOT_CAUSE_ANALYSIS_COMPLETE",
        "purpose": "Stop implementation and document root cause analysis after repeated market gate extraction failures.",
        "policy": {
            "strategy_logic_changed": False,
            "audit_only": True,
            "implementation_paused": True,
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
        "evidence": evidence,
        "confirmed_findings": confirmed_findings,
        "unknowns": unknowns,
        "root_causes": root_causes,
        "recovery_plan": recovery_plan,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-RCA — Market Gate Root Cause Analysis & Recovery Plan")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Policy")
    md.append("```json")
    md.append(json.dumps(report["policy"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Confirmed Findings")
    md.append("```json")
    md.append(json.dumps(confirmed_findings, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Unknowns")
    md.append("```json")
    md.append(json.dumps(unknowns, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Root Causes")
    md.append("```json")
    md.append(json.dumps(root_causes, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Recovery Plan")
    md.append("```json")
    md.append(json.dumps(recovery_plan, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Decision")
    md.append("```json")
    md.append(json.dumps(decision, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")

    REPORT_MD.write_text("\n".join(md))
    ARCH_MD.write_text("\n".join(md))

    print("E1R_4C2C4E_ENGINE_K2_RCA_MARKET_GATE_ROOT_CAUSE_ANALYSIS_COMPLETE")
    print("status:", report["status"])
    print("confirmed_findings:", json.dumps(confirmed_findings, ensure_ascii=False))
    print("unknowns:", json.dumps(unknowns, ensure_ascii=False))
    print("root_causes:", json.dumps(root_causes, ensure_ascii=False))
    print("recovery_plan:", json.dumps(recovery_plan, ensure_ascii=False))
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
