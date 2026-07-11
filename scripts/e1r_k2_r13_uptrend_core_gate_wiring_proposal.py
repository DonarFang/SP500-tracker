#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

R10 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R10_MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL.json"
R11 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R11_MARKET_GATE_STANDALONE_SKELETON.json"
R12C = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R12C_MARKET_GATE_GOLDEN_ROW_LOCATOR_AND_EQUIVALENCE_RETRY.json"
MARKET_GATE = ROOT / "src/e1r_engine/market_gate.py"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R13_UPTREND_CORE_GATE_WIRING_PROPOSAL.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R13_UPTREND_CORE_GATE_WIRING_PROPOSAL.md"
ARCH_MD = ROOT / "docs/architecture/E1R_UPTREND_CORE_GATE_WIRING_PROPOSAL.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_r13_uptrend_core_gate_wiring_proposal.json"
EVIDENCE_JSON = ROOT / "exports/e1r_engine/equivalence/e1r_k2_r13_uptrend_core_gate_wiring_proposal_evidence.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

PROHIBITED_CREATED_IN_R13 = [
    ROOT / "src/e1r_engine/uptrend_core.py",
    ROOT / "src/e1r_engine/regime_router.py",
    ROOT / "src/e1r_engine/core_engine.py",
    ROOT / "tests/e1r_engine/test_uptrend_core_gate_wiring.py",
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


def build_wiring_proposal(r12c: dict[str, Any]) -> dict[str, Any]:
    eq = r12c.get("equivalence", {})
    return {
        "proposal_id": "E1R_UPTREND_CORE_GATE_WIRING_PROPOSAL_V1",
        "proposal_scope": "Design only. No implementation in R13.",
        "prerequisite_evidence": {
            "market_gate_module": rel(MARKET_GATE),
            "r12c_selected_golden_path": r12c.get("golden_row_locator", {}).get("selected_path"),
            "r12c_row_count": eq.get("row_count"),
            "r12c_mismatch_count": eq.get("mismatch_count"),
            "r12c_equivalence_ok": eq.get("ok"),
        },
        "target_future_module_not_created_in_r13": {
            "file": "src/e1r_engine/uptrend_core.py",
            "purpose": "A future standalone UptrendCore that consumes MarketGateDecision while preserving legacy entry/exit/sizing behavior.",
            "status": "proposal_only_not_created",
        },
        "wiring_boundary": {
            "MarketGateEvaluator": {
                "responsibility": [
                    "Receive MarketGateInputs.",
                    "Return MarketGateDecision.",
                    "Expose gate_state, market_entry_allowed, market_shock, market_risk_off, entry_capacity.",
                ],
                "must_not_do": [
                    "No candidate ranking.",
                    "No BUY/ADD/REDUCE/EXIT generation.",
                    "No position sizing.",
                    "No account mutation.",
                    "No regime routing.",
                ],
            },
            "FutureUptrendCore": {
                "responsibility": [
                    "Consume MarketGateDecision.",
                    "Preserve existing legacy UPTREND candidate ranking and order semantics.",
                    "Block new entry actions when market_entry_allowed is false.",
                    "Respect entry_capacity as the max intended open-position capacity for new entries/adds.",
                    "Allow HOLD/REDUCE/EXIT logic to remain unaffected by gate blocks.",
                ],
                "must_not_do": [
                    "Must not recompute gate_state from SPX close < MA50.",
                    "Must not change existing rank/RS/exit/take-profit logic.",
                    "Must not increase max live holdings above 3.",
                    "Must not use SIDEWAYS sidecar Top10 as live holdings.",
                ],
            },
        },
        "action_contract": {
            "blocked_by_gate_when_market_entry_allowed_false": [
                "BUY",
                "ADD"
            ],
            "unaffected_by_gate": [
                "HOLD",
                "REDUCE",
                "EXIT"
            ],
            "entry_capacity_contract": {
                "FULL_ON": 3,
                "CAUTIOUS_ON": 2,
                "CASH_MODE": 0,
                "note": "Future UptrendCore consumes entry_capacity from MarketGateDecision. It does not compute this mapping internally unless that mapping is separately implemented and equivalence-tested."
            },
            "max_live_holdings": 3,
        },
        "future_interface_sketch": {
            "UptrendCoreInputs": {
                "date": "YYYY-MM-DD",
                "account_state": "positions/cash/equity snapshot",
                "candidate_snapshot": "pre-ranked candidate data from future candidate engine",
                "market_gate_decision": "MarketGateDecision",
                "legacy_config": "frozen legacy uptrend assumptions",
            },
            "UptrendCoreOutputs": {
                "orders": "list[OrderIntent]",
                "post_decision_trace": "dict with market_gate_state and gate block reason",
            },
            "proposed_pseudocode": [
                "gate = MarketGateEvaluator.evaluate(config, market_inputs)",
                "candidate_orders = legacy_uptrend_candidate_order_logic(inputs)",
                "if not gate.market_entry_allowed: remove BUY and ADD from candidate_orders",
                "enforce open_positions_after_orders <= min(3, gate.entry_capacity when adding new exposure)",
                "preserve HOLD/REDUCE/EXIT decisions",
                "record gate trace for audit",
            ],
        },
        "future_equivalence_test_plan": {
            "stage": "R14/R15 after user approval",
            "tests": [
                {
                    "name": "gate_decision_consumption_only",
                    "assertion": "Future UptrendCore receives MarketGateDecision; it does not call direct SPX/MA50 formula.",
                },
                {
                    "name": "buy_add_blocking",
                    "assertion": "When market_entry_allowed=false, BUY/ADD are removed or not produced.",
                },
                {
                    "name": "hold_reduce_exit_unaffected",
                    "assertion": "HOLD/REDUCE/EXIT paths are unchanged by market_entry_allowed=false.",
                },
                {
                    "name": "entry_capacity_guard",
                    "assertion": "Future UptrendCore never creates exposure above gate.entry_capacity and never above 3 live holdings.",
                },
                {
                    "name": "r7_guard_rows",
                    "assertion": "2021-06-18 remains ALLOW despite close < MA50; 2021-05-12 remains SHOCK.",
                },
            ],
            "required_pass_before_full_5y": [
                "Standalone unit smoke pass.",
                "R7 focused_rows equivalence pass.",
                "No strategy file changes.",
                "No candidate extraction unless separately approved.",
            ],
        },
        "implementation_sequence_after_approval": [
            {
                "stage": "4C-2C-4E-ENGINE-K2-R14-UPTREND_CORE_CONTRACT_SKELETON",
                "allowed": "Create standalone dataclasses/interfaces for UptrendCore. No legacy strategy integration.",
            },
            {
                "stage": "4C-2C-4E-ENGINE-K2-R15-UPTREND_CORE_GATE_CONSUMPTION_SMOKE",
                "allowed": "Pure Python tests for gate consumption only, with synthetic orders.",
            },
            {
                "stage": "4C-2C-4E-ENGINE-K2-R16-LEGACY_UPTREND_ORDER_LOGIC_EXTRACTION_PROPOSAL",
                "allowed": "Proposal only for extracting legacy UPTREND order logic.",
            }
        ],
        "explicit_non_goals": [
            "No direct patch to src/engine/backtest.py.",
            "No full 5Y run.",
            "No official result generation.",
            "No dashboard changes.",
            "No candidate extraction.",
            "No live-holding behavior change.",
            "No SIDEWAYS sidecar integration.",
        ],
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    required = [R10, R11, R12C, MARKET_GATE]
    missing = [rel(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError(f"Missing prerequisites: {missing}")

    r10 = read_json(R10)
    r11 = read_json(R11)
    r12c = read_json(R12C)

    if r10.get("decision", {}).get("k2_r10_market_gate_standalone_replication_proposal_passed") is not True:
        raise RuntimeError("R10 prerequisite not passed.")
    if r11.get("decision", {}).get("k2_r11_market_gate_standalone_skeleton_passed") is not True:
        raise RuntimeError("R11 prerequisite not passed.")
    if r12c.get("decision", {}).get("k2_r12c_market_gate_equivalence_retry_passed") is not True:
        raise RuntimeError("R12C prerequisite not passed.")
    if r12c.get("decision", {}).get("next_stage_after_user_approval") != "4C-2C-4E-ENGINE-K2-R13-UPTREND_CORE_GATE_WIRING_PROPOSAL":
        raise RuntimeError("R12C did not authorize R13 proposal.")

    proposal = build_wiring_proposal(r12c)
    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "r13_wiring_proposal_complete": True,
        "r10_loaded": True,
        "r11_loaded": True,
        "r12c_loaded": True,
        "r12c_authorized_r13": True,
        "market_gate_module_exists": MARKET_GATE.exists(),
        "r12c_equivalence_ready": r12c.get("decision", {}).get("market_gate_equivalence_ready") is True,
        "r12c_row_count_positive": (r12c.get("equivalence", {}).get("row_count") or 0) > 0,
        "r12c_mismatch_count_zero": r12c.get("equivalence", {}).get("mismatch_count") == 0,
        "proposal_only": True,
        "strategy_logic_changed": False,
        "standalone_module_only": True,
        "strategy_integration_changed": False,
        "legacy_backtest_called": False,
        "backtest_engine_run": False,
        "short_window_existing_engine_run": False,
        "full_5y_backtest_run": False,
        "forward_runner_run": False,
        "candidate_generation_extracted": False,
        "buy_add_reduce_exit_extracted": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "formula_not_patched_in_legacy": True,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "future_modules_not_created": all(not p.exists() for p in PROHIBITED_CREATED_IN_R13),
    }

    passed = all([
        validations["r13_wiring_proposal_complete"],
        validations["r12c_equivalence_ready"],
        validations["r12c_row_count_positive"],
        validations["r12c_mismatch_count_zero"],
        validations["strategy_files_unchanged"],
        validations["future_modules_not_created"],
    ])

    decision = {
        "k2_r13_uptrend_core_gate_wiring_proposal_passed": passed,
        "uptrend_core_gate_wiring_proposal_ready": passed,
        "uptrend_core_implementation_allowed_now": False,
        "market_gate_strategy_integration_allowed_now": False,
        "formula_patch_allowed_now": False,
        "candidate_extraction_allowed_now": False,
        "implementation_may_resume": False,
        "requires_user_approval_before_next_stage": True,
        "next_stage_after_user_approval": (
            "4C-2C-4E-ENGINE-K2-R14-UPTREND_CORE_CONTRACT_SKELETON"
            if passed
            else "4C-2C-4E-ENGINE-K2-R13B-UPTREND_CORE_WIRING_PROPOSAL_GAP_RCA"
        ),
        "conclusion": (
            "K2_R13_PASS_UPTREND_CORE_GATE_WIRING_PROPOSAL_READY_FOR_R14_CONTRACT_SKELETON"
            if passed
            else "K2_R13_WIRING_PROPOSAL_INCOMPLETE_DO_NOT_IMPLEMENT"
        ),
        "recommended_next_action": (
            "Review R13 proposal. If accepted, proceed to R14 contract skeleton only."
            if passed
            else "Stop and perform R13B RCA before any implementation."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R13-UPTREND_CORE_GATE_WIRING_PROPOSAL",
        "status": "UPTREND_CORE_GATE_WIRING_PROPOSAL_COMPLETE",
        "purpose": "Design how a future standalone UptrendCore should consume MarketGateDecision without changing strategy logic.",
        "source_reports": {
            "r10": {"path": rel(R10), "sha256": sha256(R10)},
            "r11": {"path": rel(R11), "sha256": sha256(R11)},
            "r12c": {"path": rel(R12C), "sha256": sha256(R12C)},
            "market_gate": {"path": rel(MARKET_GATE), "sha256": sha256(MARKET_GATE)},
        },
        "proposal": proposal,
        "policy": {
            "proposal_only": True,
            "strategy_logic_changed": False,
            "standalone_module_only": True,
            "strategy_integration_changed": False,
            "legacy_backtest_called": False,
            "backtest_engine_run": False,
            "short_window_existing_engine_run": False,
            "full_5y_backtest_run": False,
            "forward_runner_run": False,
            "candidate_generation_extracted": False,
            "buy_add_reduce_exit_extracted": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "formula_not_patched_in_legacy": True,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
        },
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)
    write_json(EVIDENCE_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R13 — Uptrend Core Gate Wiring Proposal")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
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

    print("E1R_4C2C4E_ENGINE_K2_R13_UPTREND_CORE_GATE_WIRING_PROPOSAL_COMPLETE")
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
