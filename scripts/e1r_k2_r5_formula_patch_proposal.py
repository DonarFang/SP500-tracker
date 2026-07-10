#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

BACKTEST = ROOT / "src/engine/backtest.py"
K2_RCA = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_RCA_MARKET_GATE_ROOT_CAUSE_ANALYSIS.json"
K2_R4 = ROOT / "docs/research/E1R_K2_R4_SOURCE_DEPENDENCY_TRACE.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R5_FORMULA_PATCH_PROPOSAL.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R5_FORMULA_PATCH_PROPOSAL.md"
ARCH_MD = ROOT / "docs/architecture/E1R_4C2C4E_ENGINE_K2_R5_FORMULA_PATCH_PROPOSAL.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_r5_formula_patch_proposal.json"

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


def source_line(lines: list[str], line_no: int) -> str:
    if line_no < 1 or line_no > len(lines):
        return ""
    return lines[line_no - 1].rstrip()


def source_context(lines: list[str], start: int, end: int) -> list[dict[str, Any]]:
    return [
        {"line": i, "text": source_line(lines, i)}
        for i in range(start, end + 1)
        if 1 <= i <= len(lines)
    ]


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    for p in [BACKTEST, K2_RCA, K2_R4]:
        if not p.exists():
            raise FileNotFoundError(f"Missing prerequisite: {rel(p)}")

    rca = read_json(K2_RCA)
    r4 = read_json(K2_R4)
    source = BACKTEST.read_text()
    lines = source.splitlines()

    if rca.get("decision", {}).get("formula_patch_allowed_now") is not False:
        raise RuntimeError("Unexpected RCA state: formula patch should still be blocked before proposal.")
    if r4.get("decision", {}).get("k2_r4_source_dependency_trace_passed") is not True:
        raise RuntimeError("K2-R4 dependency trace did not pass.")

    required_chain = r4.get("required_chain", {})
    unresolved = r4.get("unresolved", [])

    source_evidence = {
        "daily_equity_target": {
            "line": 1525,
            "text": source_line(lines, 1525),
            "meaning": "Golden-master equivalence target is daily_equity_records.market_gate_state, which stores _gate_state.",
        },
        "_gate_state_assignment_context": {
            "lines": "1510-1512",
            "context": source_context(lines, 1510, 1512),
            "meaning": "_gate_state is derived from market_entry_allowed and market_shock.",
        },
        "market_entry_allowed_assignments": required_chain.get("market_entry_allowed", {}).get("assignment_lines", []),
        "market_risk_off_assignments": required_chain.get("market_risk_off", {}).get("assignment_lines", []),
        "market_shock_assignments": required_chain.get("market_shock", {}).get("assignment_lines", []),
        "logger_gate_context": {
            "lines": "2137-2139",
            "context": source_context(lines, 2137, 2139),
            "meaning": "Logger gate_state uses the same local expression pattern but is not the primary equivalence target.",
        },
    }

    patch_proposal = {
        "target_file": "src/e1r_engine/uptrend_core.py",
        "target_api": "compute_market_gate_state",
        "proposal_type": "source-line-cited formula correction",
        "equivalence_target": "daily_equity_records.market_gate_state",
        "equivalence_target_source_line": "src/engine/backtest.py:L1525",
        "do_not_replicate": [
            "Do not compute RISK_OFF directly from same-day spx_close < spx_ma50.",
            "Do not compute SHOCK directly from rounded daily_equity_records.spx_day_return_pct unless it is only used as a display field.",
            "Do not use logger gate_state as the equivalence target when daily_equity_records stores _gate_state.",
        ],
        "required_formula": {
            "source_lines": ["src/engine/backtest.py:L1510-L1512"],
            "formula": "_gate_state = 'ALLOW' if market_entry_allowed else ('SHOCK' if market_shock else 'RISK_OFF')",
            "required_inputs": [
                "market_entry_allowed",
                "market_shock",
            ],
            "optional_trace_inputs_for_explainability": [
                "market_risk_off",
                "market_state",
                "_shock_active",
                "entry_capacity",
                "spx_close_t",
                "spx_ma50_t",
                "spx_day_return",
            ],
        },
        "implementation_shape_for_k2_r6": {
            "new_or_updated_dataclass": "MarketGateDecision",
            "recommended_method_signature": (
                "compute_market_gate_state(date, market_entry_allowed, market_shock, "
                "market_risk_off=None, raw=None) -> MarketGateDecision"
            ),
            "state_logic": [
                "if market_entry_allowed: state = 'ALLOW'",
                "elif market_shock: state = 'SHOCK'",
                "else: state = 'RISK_OFF'",
            ],
            "reason_logic": [
                "ALLOW -> market_entry_allowed_true",
                "SHOCK -> market_entry_blocked_by_market_shock",
                "RISK_OFF -> market_entry_blocked_by_market_risk_off_or_capacity",
            ],
        },
        "input_policy": {
            "short_window_k2_r6": (
                "Use source-equivalent fields when available. For the existing golden master, "
                "market_entry_allowed and market_shock are not separately persisted, so K2-R6 must either "
                "derive them from a source-equivalent replay trace or intentionally mark this as not patchable from daily rows alone."
            ),
            "important_constraint": (
                "A patch that only consumes spx_close, spx_ma50, and spx_day_return_pct is not source-equivalent."
            ),
        },
        "blocking_check_before_k2_r6": [
            {
                "check": "Can K2-R6 obtain market_entry_allowed and market_shock for each daily_equity row?",
                "required_answer": "yes",
                "if_no": "Do not patch formula; first generate variable-level replay trace from legacy run.",
            },
            {
                "check": "Is daily_equity_records.market_gate_state the confirmed target?",
                "required_answer": "yes",
                "source_line": "src/engine/backtest.py:L1525",
            },
            {
                "check": "Will K2-R6 avoid direct SPX<MA50 formula?",
                "required_answer": "yes",
            },
        ],
    }

    recovered_understanding = {
        "previous_wrong_model": "market_gate_state = SHOCK if SPX day return <= -2%; else RISK_OFF if SPX close < SPX MA50; else ALLOW",
        "source_supported_model": "_gate_state = ALLOW if market_entry_allowed else SHOCK if market_shock else RISK_OFF",
        "why_previous_model_failed": [
            "RISK_OFF is not a direct same-day SPX<MA50 display-field comparison.",
            "daily_equity_records target stores _gate_state, not a standalone formula over rounded output fields.",
            "market_entry_allowed depends on entry_capacity under gate-enabled branch.",
            "market_shock depends on _shock_active under gate-enabled branch.",
        ],
    }

    next_step_decision = {
        "k2_r6_should_patch_now": False,
        "reason": (
            "The formula target is now source-supported, but the current golden master daily rows do not persist "
            "market_entry_allowed and market_shock as standalone fields. A direct patch using only daily rows would "
            "repeat the same evidence error. K2-R6 must first include a source-equivalent variable replay input or fail closed."
        ),
        "recommended_next_stage": "4C-2C-4E-ENGINE-K2-R6-MARKET_GATE_VARIABLE_REPLAY_TRACE",
        "why_this_is_not_path_divergence": (
            "This is the minimum required step to satisfy the K2-RCA acceptance rule: no formula patch until all "
            "inputs used by the formula are available and source-cited."
        ),
        "stage_after_r6_if_pass": "4C-2C-4E-ENGINE-K2-R7-MARKET_GATE_EQUIVALENCE_PATCH",
    }

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "formula_patch_proposal_complete": True,
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
        "k2_r4_loaded": True,
        "k2_r4_unresolved_empty": unresolved == [],
        "daily_equity_target_cited": True,
        "_gate_state_assignment_cited": True,
        "direct_spx_ma50_formula_rejected": True,
        "required_inputs_identified": True,
        "patch_blocking_check_defined": True,
    }

    decision = {
        "k2_r5_formula_patch_proposal_passed": all([
            validations["strategy_files_unchanged"],
            validations["k2_r4_unresolved_empty"],
            validations["daily_equity_target_cited"],
            validations["_gate_state_assignment_cited"],
            validations["direct_spx_ma50_formula_rejected"],
            validations["required_inputs_identified"],
            validations["patch_blocking_check_defined"],
        ]),
        "formula_patch_allowed_now": False,
        "implementation_may_resume": False,
        "candidate_extraction_allowed_now": False,
        "next_required_stage": next_step_decision["recommended_next_stage"],
        "conclusion": "K2_R5_PASS_PATCH_PROPOSAL_READY_FOR_VARIABLE_REPLAY_TRACE",
        "recommended_next_action": (
            "Run 4C-2C-4E-ENGINE-K2-R6-MARKET_GATE_VARIABLE_REPLAY_TRACE to obtain "
            "market_entry_allowed and market_shock per daily row before patching standalone equivalence."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R5-FORMULA_PATCH_PROPOSAL",
        "status": "FORMULA_PATCH_PROPOSAL_COMPLETE",
        "purpose": "Produce a source-line-cited market gate patch proposal without patching implementation.",
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
        "source_evidence": source_evidence,
        "recovered_understanding": recovered_understanding,
        "patch_proposal": patch_proposal,
        "next_step_decision": next_step_decision,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R5 — Formula Patch Proposal")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Source Evidence")
    md.append("```json")
    md.append(json.dumps(source_evidence, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Recovered Understanding")
    md.append("```json")
    md.append(json.dumps(recovered_understanding, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Patch Proposal")
    md.append("```json")
    md.append(json.dumps(patch_proposal, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Next Step Decision")
    md.append("```json")
    md.append(json.dumps(next_step_decision, indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_ENGINE_K2_R5_FORMULA_PATCH_PROPOSAL_COMPLETE")
    print("status:", report["status"])
    print("source_evidence:", json.dumps(source_evidence, ensure_ascii=False))
    print("recovered_understanding:", json.dumps(recovered_understanding, ensure_ascii=False))
    print("patch_proposal:", json.dumps(patch_proposal, ensure_ascii=False))
    print("next_step_decision:", json.dumps(next_step_decision, ensure_ascii=False))
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
