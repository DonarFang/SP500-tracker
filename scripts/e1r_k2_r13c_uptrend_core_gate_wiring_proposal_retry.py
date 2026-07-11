#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
import subprocess
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

R12C = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R12C_MARKET_GATE_GOLDEN_ROW_LOCATOR_AND_EQUIVALENCE_RETRY.json"
R13B = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R13B_UPTREND_CORE_WIRING_PROPOSAL_GAP_RCA.json"
MARKET_GATE = ROOT / "src/e1r_engine/market_gate.py"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R13C_UPTREND_CORE_GATE_WIRING_PROPOSAL_RETRY.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R13C_UPTREND_CORE_GATE_WIRING_PROPOSAL_RETRY.md"
ARCH_MD = ROOT / "docs/architecture/E1R_UPTREND_CORE_GATE_WIRING_PROPOSAL_RETRY.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_r13c_uptrend_core_gate_wiring_proposal_retry.json"
EVIDENCE_JSON = ROOT / "exports/e1r_engine/equivalence/e1r_k2_r13c_uptrend_core_gate_wiring_proposal_retry_evidence.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

FUTURE_SHELL_AUDIT_PATHS = [
    "src/e1r_engine/uptrend_core.py",
    "src/e1r_engine/regime_router.py",
    "src/e1r_engine/core_engine.py",
    "tests/e1r_engine/test_uptrend_core_gate_wiring.py",
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


def run_git(args: list[str]) -> dict[str, Any]:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
    )
    return {
        "cmd": ["git", *args],
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "ok": proc.returncode == 0,
    }


def git_stdout(args: list[str]) -> str:
    return run_git(args)["stdout"].strip()


def classify_future_shell_path(path: str) -> dict[str, Any]:
    full = ROOT / path
    exists = full.exists()
    tracked = bool(git_stdout(["ls-files", "--", path]))
    status = git_stdout(["status", "--porcelain", "--", path])
    diff_name = git_stdout(["diff", "--name-only", "--", path])
    cached_diff_name = git_stdout(["diff", "--cached", "--name-only", "--", path])
    creation_log = git_stdout([
        "log",
        "--diff-filter=A",
        "--follow",
        "--format=%H %ad %s",
        "--date=iso-strict",
        "--",
        path,
    ])
    recent_log = git_stdout([
        "log",
        "-5",
        "--follow",
        "--format=%H %ad %s",
        "--date=iso-strict",
        "--",
        path,
    ])

    if not exists:
        classification = "ABSENT_OK"
    elif tracked and not status:
        classification = "HISTORICAL_TRACKED_UNCHANGED"
    elif tracked and status:
        classification = "TRACKED_BUT_MODIFIED_BLOCKING"
    elif exists and not tracked:
        classification = "UNTRACKED_NEW_BLOCKING"
    else:
        classification = "UNKNOWN_BLOCKING"

    return {
        "path": path,
        "exists": exists,
        "tracked": tracked,
        "sha256": sha256(full),
        "git_status_porcelain": status,
        "git_diff_name": diff_name,
        "git_cached_diff_name": cached_diff_name,
        "creation_log": creation_log.splitlines()[:5],
        "recent_log": recent_log.splitlines()[:5],
        "classification": classification,
    }


def build_retry_proposal(r12c: dict[str, Any], r13b: dict[str, Any], shell_audit: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "proposal_id": "E1R_UPTREND_CORE_GATE_WIRING_PROPOSAL_V2_HISTORICAL_SHELL_AWARE",
        "proposal_scope": "Design only. No implementation in R13C.",
        "why_retry": {
            "r13_failure": "Original R13 used future_modules_not_created=all(not exists(path)), which conflicted with historical standalone shell files.",
            "r13b_root_cause": r13b.get("decision", {}).get("root_cause"),
            "corrected_rule": "Historical tracked unchanged shell files may exist; new or modified implementation paths remain blocking.",
        },
        "prerequisite_evidence": {
            "market_gate_module": rel(MARKET_GATE),
            "r12c_selected_golden_path": r12c.get("golden_row_locator", {}).get("selected_path"),
            "r12c_row_count": r12c.get("equivalence", {}).get("row_count"),
            "r12c_mismatch_count": r12c.get("equivalence", {}).get("mismatch_count"),
            "r12c_equivalence_ok": r12c.get("equivalence", {}).get("ok"),
            "r13b_gap_rca_passed": r13b.get("decision", {}).get("k2_r13b_uptrend_core_wiring_proposal_gap_rca_passed"),
        },
        "historical_shell_aware_audit": shell_audit,
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
                    "Block new entry actions only when market_entry_allowed is false.",
                    "Respect entry_capacity as the future max intended new-exposure capacity.",
                    "Keep HOLD/REDUCE/EXIT unaffected by market_entry_allowed=false.",
                ],
                "must_not_do": [
                    "Must not recompute gate_state from SPX close < MA50.",
                    "Must not change legacy rank/RS/exit/take-profit logic.",
                    "Must not increase live holdings above 3.",
                    "Must not use SIDEWAYS Top10 sidecar as live holdings.",
                ],
            },
        },
        "action_contract": {
            "blocked_by_gate_when_market_entry_allowed_false": ["BUY", "ADD"],
            "unaffected_by_gate": ["HOLD", "REDUCE", "EXIT"],
            "max_live_holdings": 3,
            "entry_capacity_contract": {
                "FULL_ON": 3,
                "CAUTIOUS_ON": 2,
                "CASH_MODE": 0,
                "note": "Future UptrendCore consumes entry_capacity from MarketGateDecision. It does not recalculate direct gate_state from SPX/MA50.",
            },
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
            "pseudocode": [
                "gate = MarketGateEvaluator.evaluate(config, market_inputs)",
                "candidate_orders = legacy_uptrend_candidate_order_logic(inputs)",
                "if not gate.market_entry_allowed: remove BUY and ADD from candidate_orders",
                "preserve HOLD/REDUCE/EXIT candidate decisions",
                "enforce open_positions_after_orders <= 3",
                "record gate trace for audit",
            ],
        },
        "future_test_plan": {
            "before_any_full_5y": [
                "R14 standalone contract skeleton only.",
                "R15 gate consumption smoke with synthetic orders.",
                "No legacy strategy file diffs.",
                "No direct SPX/MA50 gate formula.",
                "No candidate extraction unless approved.",
            ],
            "guard_rows": [
                "2021-06-18 remains ALLOW despite close < MA50.",
                "2021-05-12 remains SHOCK.",
            ],
        },
        "explicit_non_goals": [
            "No direct patch to src/engine/backtest.py.",
            "No modifications to historical shell files in R13C.",
            "No full 5Y run.",
            "No official result generation.",
            "No dashboard changes.",
            "No candidate extraction.",
            "No live-holding behavior change.",
            "No SIDEWAYS sidecar integration.",
        ],
        "implementation_sequence_after_approval": [
            {
                "stage": "4C-2C-4E-ENGINE-K2-R14-UPTREND_CORE_CONTRACT_SKELETON",
                "allowed": "Create or update standalone UptrendCore contract skeleton only if required; no legacy strategy integration.",
            },
            {
                "stage": "4C-2C-4E-ENGINE-K2-R15-UPTREND_CORE_GATE_CONSUMPTION_SMOKE",
                "allowed": "Pure Python smoke for gate consumption only, with synthetic order intents.",
            },
            {
                "stage": "4C-2C-4E-ENGINE-K2-R16-LEGACY_UPTREND_ORDER_LOGIC_EXTRACTION_PROPOSAL",
                "allowed": "Proposal only for extracting legacy UPTREND order logic.",
            },
        ],
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    required = [R12C, R13B, MARKET_GATE]
    missing = [rel(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError(f"Missing prerequisites: {missing}")

    r12c = read_json(R12C)
    r13b = read_json(R13B)

    if r12c.get("decision", {}).get("k2_r12c_market_gate_equivalence_retry_passed") is not True:
        raise RuntimeError("R12C prerequisite not passed.")
    if r13b.get("decision", {}).get("k2_r13b_uptrend_core_wiring_proposal_gap_rca_passed") is not True:
        raise RuntimeError("R13B prerequisite not passed.")
    if r13b.get("decision", {}).get("next_stage_after_user_approval") != "4C-2C-4E-ENGINE-K2-R13C-UPTREND_CORE_GATE_WIRING_PROPOSAL_RETRY_WITH_HISTORICAL_SHELL_AWARE_VALIDATION":
        raise RuntimeError("R13B did not authorize R13C retry.")

    shell_audit = [classify_future_shell_path(path) for path in FUTURE_SHELL_AUDIT_PATHS]
    allowed_classifications = {"ABSENT_OK", "HISTORICAL_TRACKED_UNCHANGED"}
    blocking_shell_paths = [
        row for row in shell_audit
        if row["classification"] not in allowed_classifications
    ]

    proposal = build_retry_proposal(r12c, r13b, shell_audit)
    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "r13c_wiring_proposal_retry_complete": True,
        "r12c_loaded": True,
        "r13b_loaded": True,
        "r13b_authorized_r13c": True,
        "market_gate_module_exists": MARKET_GATE.exists(),
        "r12c_equivalence_ready": r12c.get("decision", {}).get("market_gate_equivalence_ready") is True,
        "r12c_row_count_positive": (r12c.get("equivalence", {}).get("row_count") or 0) > 0,
        "r12c_mismatch_count_zero": r12c.get("equivalence", {}).get("mismatch_count") == 0,
        "historical_shell_aware_validation_used": True,
        "shell_audit_path_count": len(shell_audit),
        "blocking_shell_path_count": len(blocking_shell_paths),
        "future_shell_paths_historical_or_absent": len(blocking_shell_paths) == 0,
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
    }

    passed = all([
        validations["r13c_wiring_proposal_retry_complete"],
        validations["r12c_equivalence_ready"],
        validations["r12c_row_count_positive"],
        validations["r12c_mismatch_count_zero"],
        validations["historical_shell_aware_validation_used"],
        validations["future_shell_paths_historical_or_absent"],
        validations["strategy_files_unchanged"],
    ])

    decision = {
        "k2_r13c_uptrend_core_gate_wiring_proposal_retry_passed": passed,
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
            else "4C-2C-4E-ENGINE-K2-R13D-UPTREND_CORE_WIRING_PROPOSAL_RETRY_GAP_RCA"
        ),
        "conclusion": (
            "K2_R13C_PASS_UPTREND_CORE_GATE_WIRING_PROPOSAL_READY_FOR_R14_CONTRACT_SKELETON"
            if passed
            else "K2_R13C_WIRING_PROPOSAL_RETRY_INCOMPLETE_DO_NOT_IMPLEMENT"
        ),
        "recommended_next_action": (
            "Review R13C proposal. If accepted, proceed to R14 contract skeleton only."
            if passed
            else "Stop and perform R13D RCA before any implementation."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R13C-UPTREND_CORE_GATE_WIRING_PROPOSAL_RETRY_WITH_HISTORICAL_SHELL_AWARE_VALIDATION",
        "status": "UPTREND_CORE_GATE_WIRING_PROPOSAL_RETRY_COMPLETE",
        "purpose": "Retry R13 proposal with historical-shell-aware validation. Proposal only; no implementation.",
        "source_reports": {
            "r12c": {"path": rel(R12C), "sha256": sha256(R12C)},
            "r13b": {"path": rel(R13B), "sha256": sha256(R13B)},
            "market_gate": {"path": rel(MARKET_GATE), "sha256": sha256(MARKET_GATE)},
        },
        "historical_shell_audit": shell_audit,
        "blocking_shell_paths": blocking_shell_paths,
        "proposal": proposal,
        "policy": {
            "proposal_only": True,
            "historical_shell_aware_validation": True,
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
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R13C — Uptrend Core Gate Wiring Proposal Retry")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Historical Shell Audit")
    md.append("```json")
    md.append(json.dumps(shell_audit, indent=2, ensure_ascii=False))
    md.append("```")
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

    print("E1R_4C2C4E_ENGINE_K2_R13C_UPTREND_CORE_GATE_WIRING_PROPOSAL_RETRY_COMPLETE")
    print("status:", report["status"])
    print("historical_shell_audit:", json.dumps(shell_audit, ensure_ascii=False))
    print("blocking_shell_paths:", json.dumps(blocking_shell_paths, ensure_ascii=False))
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
