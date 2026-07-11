#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

R7 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R7_MARKET_STATE_SOURCE_EQUIVALENCE_TRACE.json"
R8 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R8_MARKET_STATE_PARAMETER_AUDIT.json"
R9D = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9D_MARKET_PARAM_SOURCE_LINE_TRACE.json"
RCA2 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_RCA2_MARKET_PARAM_EVIDENCE_CHAIN_REVIEW.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R10_MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R10_MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL.md"
ARCH_MD = ROOT / "docs/architecture/E1R_MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_r10_market_gate_standalone_replication_proposal.json"
EVIDENCE_JSON = ROOT / "exports/e1r_engine/equivalence/e1r_k2_r10_market_gate_standalone_replication_proposal_evidence.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

PROPOSED_FILES_NOT_CREATED_IN_R10 = [
    "src/e1r_engine/market_gate.py",
    "tests/e1r_engine/test_market_gate_equivalence.py",
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


def compact(v: Any, max_len: int = 2200) -> Any:
    if isinstance(v, (str, int, float, bool)) or v is None:
        if isinstance(v, str) and len(v) > max_len:
            return v[:max_len] + "...<truncated>"
        return v
    try:
        s = json.dumps(v, ensure_ascii=False)
        if len(s) > max_len:
            return s[:max_len] + "...<truncated>"
        return json.loads(s)
    except Exception:
        s = repr(v)
        if len(s) > max_len:
            return s[:max_len] + "...<truncated>"
        return s


def load_required() -> dict[str, Any]:
    missing = [rel(p) for p in [R8, R9D, RCA2] if not p.exists()]
    if missing:
        raise FileNotFoundError(f"Missing required reports: {missing}")

    reports = {
        "r8": read_json(R8),
        "r9d": read_json(R9D),
        "rca2": read_json(RCA2),
    }
    if R7.exists():
        reports["r7"] = read_json(R7)
    return reports


def summarize_r9d_evidence(r9d: dict[str, Any]) -> dict[str, Any]:
    matrix = r9d.get("evidence_matrix", {})
    summary = {}
    for field, row in matrix.items():
        summary[field] = {
            "status": row.get("status"),
            "clean_evidence_count": row.get("clean_evidence_count"),
            "primary_source_count": row.get("primary_source_count"),
            "original_trace_or_source_head_count": row.get("original_trace_or_source_head_count"),
            "best_evidence": [compact(x) for x in row.get("best_evidence", [])[:4]],
        }
    return summary


def build_replication_proposal(reports: dict[str, Any]) -> dict[str, Any]:
    r8 = reports["r8"]
    r9d = reports["r9d"]

    r8_decision = r8.get("decision", {})
    r8_controls = (
        r8.get("golden_master_market_state_parameters", {})
        or r8.get("market_state_parameter_summary", {})
        or r8.get("parameter_summary", {})
    )

    evidence_summary = summarize_r9d_evidence(r9d)

    return {
        "proposal_id": "E1R_MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL_V1",
        "proposal_scope": "Design only. No implementation in R10.",
        "source_evidence_inputs": {
            "r7_short_window_source_equivalence": rel(R7) if R7.exists() else None,
            "r8_short_window_parameter_audit": rel(R8),
            "r9d_full_artifact_source_line_evidence": rel(R9D),
            "rca2_stop_review": rel(RCA2),
        },
        "r9d_evidence_summary": evidence_summary,
        "replication_target": {
            "target_component": "market gate / market state chain used by legacy E1R v0.2 core",
            "do_not_replicate_as": [
                "same-day SPX close < SPX MA50 direct formula",
                "rounded daily_equity_records display-only formula",
                "audit-report evidence-count formula",
            ],
            "replicate_as": [
                "legacy local-variable chain",
                "market_state + _shock_active + entry_capacity",
                "market_entry_allowed + market_shock + market_risk_off",
                "_gate_state export identity",
            ],
        },
        "proposed_module": {
            "file": "src/e1r_engine/market_gate.py",
            "classes": [
                {
                    "name": "MarketGateConfig",
                    "purpose": "Hold source-proven market gate settings.",
                    "fields": {
                        "variant": "D3_RISK_OFF_PLUS_SHOCK_GATE",
                        "market_gate_enabled": True,
                        "risk_off_below_spx_ma50": True,
                        "market_shock_gate_enabled": True,
                        "market_shock_daily_return": -0.02,
                    },
                    "source": "R8 + R9D",
                },
                {
                    "name": "MarketGateInputs",
                    "purpose": "Carry precomputed legacy-equivalent upstream values for one trading day.",
                    "fields": {
                        "date": "YYYY-MM-DD",
                        "spx_close": "float | None",
                        "spx_ma50": "float | None",
                        "spx_day_return": "float | None",
                        "market_state": "FULL_ON | CAUTIOUS_ON | CASH_MODE | UNKNOWN",
                        "entry_capacity": "int",
                        "existing_positions_count": "int",
                    },
                    "boundary": "Inputs are data/state facts; this object must not rank candidates or decide BUY/ADD/REDUCE/EXIT.",
                },
                {
                    "name": "MarketGateDecision",
                    "purpose": "Return the exact gate-related local outputs needed by later strategy branches.",
                    "fields": {
                        "market_shock": "bool",
                        "market_risk_off": "bool",
                        "market_entry_allowed": "bool",
                        "entry_capacity": "int",
                        "gate_state": "ALLOW | SHOCK | RISK_OFF",
                        "blocked_actions": ["BUY", "ADD"],
                        "unaffected_actions": ["HOLD", "REDUCE", "EXIT"],
                        "trace": "dict",
                    },
                },
                {
                    "name": "MarketGateEvaluator",
                    "purpose": "Pure deterministic evaluator for market gate state. No order generation.",
                    "methods": [
                        "evaluate(config: MarketGateConfig, inputs: MarketGateInputs) -> MarketGateDecision"
                    ],
                },
            ],
        },
        "source_equivalent_logic_contract": {
            "market_shock": "_shock_active = market_shock_gate_enabled and spx_day_return <= market_shock_daily_return",
            "market_risk_off": "market_risk_off = (market_state == 'CASH_MODE') and not market_shock",
            "market_entry_allowed": "market_entry_allowed = entry_capacity > 0",
            "gate_state": "_gate_state = 'ALLOW' if market_entry_allowed else 'SHOCK' if market_shock else 'RISK_OFF'",
            "blocked_actions_when_not_allow": ["BUY", "ADD"],
            "unaffected_actions": ["HOLD", "REDUCE", "EXIT"],
            "warning": "Do not recompute gate_state directly from SPX close < SPX MA50. R7 proved the direct formula mismatched legacy target.",
        },
        "entry_capacity_contract": {
            "mapping_observed_in_r8": {
                "FULL_ON": 3,
                "CAUTIOUS_ON": 2,
                "CASH_MODE": 0,
            },
            "responsibility_boundary": {
                "MarketStateEvaluator": "Computes or receives market_state and entry_capacity using legacy-equivalent upstream rules.",
                "MarketGateEvaluator": "Consumes market_state, entry_capacity, and shock inputs to derive gate decision.",
                "UptrendCore": "Consumes MarketGateDecision to block BUY/ADD only.",
            },
            "r10_design_choice": "Keep entry_capacity as an explicit input to MarketGateEvaluator, not an implicit recomputation inside _gate_state.",
        },
        "call_chain_integration_contract": {
            "legacy_full_artifact_chain": [
                "run_stateful_simulation",
                "_core_e1r / core_variant_result",
                "build_e1r_sidecar_sleeve",
                "_sidecar_result",
                "compose_e1r_v0_2_variant",
                "E1R_REGIME_AWARE_V0_2",
            ],
            "standalone_target_chain": [
                "HistoricalDataAdapter / ForwardDataAdapter",
                "MarketStateEvaluator",
                "MarketGateEvaluator",
                "UptrendCore",
                "SidewaysCore",
                "RegimeRouter",
                "E1RCoreEngine",
                "BacktestRunner / ForwardRunner",
            ],
            "do_not_mix": [
                "Do not let sidecar Top10 become live holdings > 3.",
                "Do not let SIDEWAYS sidecar change UPTREND gate behavior.",
                "Do not use invalid stitched curves as equivalence target.",
            ],
        },
        "equivalence_test_plan": {
            "stage": "future R11/R12, not R10",
            "golden_master_sources": [
                "R7 62-row short-window legacy locals trace",
                "R8 market state parameter audit",
                "R9D source-line matrix",
            ],
            "row_level_assertions": [
                "date exact match",
                "market_state exact match",
                "entry_capacity exact match",
                "market_shock exact match",
                "market_risk_off exact match",
                "market_entry_allowed exact match",
                "gate_state exact match",
                "blocked_actions exact match",
                "unaffected_actions exact match",
            ],
            "pass_threshold": {
                "mismatch_count": 0,
                "required_rows": "all rows in golden master trace",
            },
        },
        "implementation_sequence_after_approval": [
            {
                "stage": "4C-2C-4E-ENGINE-K2-R11-MARKET_GATE_STANDALONE_SKELETON",
                "allowed": "Add dataclasses and evaluator skeleton with no strategy integration.",
            },
            {
                "stage": "4C-2C-4E-ENGINE-K2-R12-MARKET_GATE_EQUIVALENCE_SMOKE",
                "allowed": "Compare evaluator output against R7/R8 golden rows.",
            },
            {
                "stage": "4C-2C-4E-ENGINE-K2-R13-UPTREND_CORE_GATE_WIRING_PROPOSAL",
                "allowed": "Proposal only for how UptrendCore should consume gate decision.",
            },
        ],
        "proposal_risk_controls": [
            "No patch in R10.",
            "No full 5Y run in R10.",
            "No formula simplification.",
            "No candidate/BUY/ADD/REDUCE/EXIT extraction in R10.",
            "No replication-ready implementation until row-level equivalence passes.",
        ],
    }


def build_validation_decision(reports: dict[str, Any], proposal: dict[str, Any], before_hashes: dict[str, str | None], after_hashes: dict[str, str | None]) -> tuple[dict[str, Any], dict[str, Any]]:
    r9d = reports["r9d"]
    rca2 = reports["rca2"]

    r9d_decision = r9d.get("decision", {})
    rca2_decision = rca2.get("decision", {})

    required_sections = [
        "proposed_module",
        "source_equivalent_logic_contract",
        "entry_capacity_contract",
        "call_chain_integration_contract",
        "equivalence_test_plan",
        "implementation_sequence_after_approval",
        "proposal_risk_controls",
    ]

    validations = {
        "proposal_complete": True,
        "rca2_loaded": True,
        "r9d_loaded": True,
        "r9d_source_line_evidence_ready": r9d_decision.get("market_state_115_replication_ready") is True,
        "r9d_blocking_fields_empty": r9d_decision.get("blocking_fields") == [],
        "all_required_sections_present": all(section in proposal for section in required_sections),
        "market_gate_module_design_present": "proposed_module" in proposal,
        "source_equivalent_logic_contract_present": "source_equivalent_logic_contract" in proposal,
        "entry_capacity_boundary_defined": "entry_capacity_contract" in proposal,
        "call_chain_integration_contract_present": "call_chain_integration_contract" in proposal,
        "equivalence_test_plan_present": "equivalence_test_plan" in proposal,
        "implementation_sequence_after_approval_defined": "implementation_sequence_after_approval" in proposal,
        "strategy_logic_changed": False,
        "audit_only": True,
        "proposal_only": True,
        "formula_not_patched": True,
        "backtest_engine_run": False,
        "short_window_existing_engine_run": False,
        "full_5y_backtest_run": False,
        "forward_runner_run": False,
        "candidate_generation_extracted": False,
        "buy_add_reduce_exit_extracted": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "proposed_files_not_created": all(not (ROOT / p).exists() for p in PROPOSED_FILES_NOT_CREATED_IN_R10),
    }

    proposal_passed = all([
        validations["proposal_complete"],
        validations["rca2_loaded"],
        validations["r9d_loaded"],
        validations["r9d_source_line_evidence_ready"],
        validations["r9d_blocking_fields_empty"],
        validations["all_required_sections_present"],
        validations["strategy_files_unchanged"],
        validations["proposed_files_not_created"],
    ])

    decision = {
        "k2_r10_market_gate_standalone_replication_proposal_passed": proposal_passed,
        "market_state_115_replication_proposal_ready": proposal_passed,
        "market_gate_implementation_allowed_now": False,
        "formula_patch_allowed_now": False,
        "candidate_extraction_allowed_now": False,
        "implementation_may_resume": False,
        "requires_user_approval_before_next_implementation_stage": True,
        "next_stage_after_user_approval": "4C-2C-4E-ENGINE-K2-R11-MARKET_GATE_STANDALONE_SKELETON",
        "conclusion": (
            "K2_R10_PASS_PROPOSAL_READY_FOR_USER_REVIEW_BEFORE_R11"
            if proposal_passed
            else "K2_R10_PROPOSAL_INCOMPLETE_DO_NOT_IMPLEMENT"
        ),
        "recommended_next_action": "Review proposal. If accepted, proceed to R11 skeleton only; still no full strategy extraction.",
    }

    return validations, decision


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    reports = load_required()
    proposal = build_replication_proposal(reports)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}
    validations, decision = build_validation_decision(reports, proposal, before_hashes, after_hashes)

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R10-MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL",
        "status": "MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL_COMPLETE",
        "purpose": "Convert R7/R8/R9D evidence into a standalone market gate replication design proposal without implementation.",
        "policy": {
            "strategy_logic_changed": False,
            "audit_only": True,
            "proposal_only": True,
            "formula_not_patched": True,
            "backtest_engine_run": False,
            "short_window_existing_engine_run": False,
            "full_5y_backtest_run": False,
            "forward_runner_run": False,
            "candidate_generation_extracted": False,
            "buy_add_reduce_exit_extracted": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
        },
        "source_reports": {
            "r7": {"path": rel(R7), "exists": R7.exists(), "sha256": sha256(R7)},
            "r8": {"path": rel(R8), "exists": R8.exists(), "sha256": sha256(R8)},
            "r9d": {"path": rel(R9D), "exists": R9D.exists(), "sha256": sha256(R9D)},
            "rca2": {"path": rel(RCA2), "exists": RCA2.exists(), "sha256": sha256(RCA2)},
        },
        "proposal": proposal,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)
    write_json(EVIDENCE_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R10 — Market Gate Standalone Replication Proposal")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Scope")
    md.append("R10 is proposal-only. It does not create `src/e1r_engine/market_gate.py`, does not patch strategy logic, and does not run any backtest.")
    md.append("")
    md.append("## Proposal")
    md.append("```json")
    md.append(json.dumps(proposal, indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_ENGINE_K2_R10_MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL_COMPLETE")
    print("status:", report["status"])
    print("proposal:", json.dumps(proposal, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(AUDIT_JSON))
    print("wrote:", rel(EVIDENCE_JSON))


if __name__ == "__main__":
    main()
