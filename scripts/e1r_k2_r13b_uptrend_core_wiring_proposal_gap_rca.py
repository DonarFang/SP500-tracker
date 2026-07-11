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
R13 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R13_UPTREND_CORE_GATE_WIRING_PROPOSAL.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R13B_UPTREND_CORE_WIRING_PROPOSAL_GAP_RCA.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R13B_UPTREND_CORE_WIRING_PROPOSAL_GAP_RCA.md"
ARCH_MD = ROOT / "docs/architecture/E1R_UPTREND_CORE_WIRING_PROPOSAL_GAP_RCA.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_r13b_uptrend_core_wiring_proposal_gap_rca.json"
EVIDENCE_JSON = ROOT / "exports/e1r_engine/equivalence/e1r_k2_r13b_uptrend_core_wiring_proposal_gap_rca_evidence.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

R13_PROHIBITED_PATHS = [
    "src/e1r_engine/uptrend_core.py",
    "src/e1r_engine/regime_router.py",
    "src/e1r_engine/core_engine.py",
    "tests/e1r_engine/test_uptrend_core_gate_wiring.py",
]

R13_FAILED_ARTIFACTS = [
    "scripts/e1r_k2_r13_uptrend_core_gate_wiring_proposal.py",
    "docs/research/E1R_4C2C4E_ENGINE_K2_R13_UPTREND_CORE_GATE_WIRING_PROPOSAL.json",
    "docs/research/E1R_4C2C4E_ENGINE_K2_R13_UPTREND_CORE_GATE_WIRING_PROPOSAL.md",
    "docs/architecture/E1R_UPTREND_CORE_GATE_WIRING_PROPOSAL.md",
    "exports/e1r_engine/audit/e1r_k2_r13_uptrend_core_gate_wiring_proposal.json",
    "exports/e1r_engine/equivalence/e1r_k2_r13_uptrend_core_gate_wiring_proposal_evidence.json",
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
    r = run_git(args)
    return r["stdout"].strip()


def file_status(path: str) -> dict[str, Any]:
    full = ROOT / path

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

    exists = full.exists()
    untracked = bool(status.startswith("??"))
    modified_or_staged = bool(status and not status.startswith("??"))

    if not exists:
        classification = "ABSENT_OK"
    elif tracked and not status:
        classification = "HISTORICAL_TRACKED_UNCHANGED"
    elif tracked and modified_or_staged:
        classification = "TRACKED_BUT_MODIFIED_REQUIRES_REVIEW"
    elif untracked:
        classification = "UNTRACKED_NEW_REQUIRES_REVIEW"
    else:
        classification = "EXISTS_UNCLASSIFIED_REQUIRES_REVIEW"

    return {
        "path": path,
        "exists": exists,
        "sha256": sha256(full),
        "tracked": tracked,
        "git_status_porcelain": status,
        "git_diff_name": diff_name,
        "git_cached_diff_name": cached_diff_name,
        "creation_log": creation_log.splitlines()[:5],
        "recent_log": recent_log.splitlines()[:5],
        "classification": classification,
    }


def summarize_r13_failure() -> dict[str, Any]:
    if not R13.exists():
        return {
            "r13_report_exists": False,
            "failure_confirmed": False,
            "summary": "R13 report not found.",
        }

    r13 = read_json(R13)
    return {
        "r13_report_exists": True,
        "status": r13.get("status"),
        "validations": r13.get("validations"),
        "decision": r13.get("decision"),
        "failure_confirmed": (
            r13.get("decision", {}).get("k2_r13_uptrend_core_gate_wiring_proposal_passed") is False
            and r13.get("validations", {}).get("future_modules_not_created") is False
        ),
        "failed_condition": "future_modules_not_created=false",
    }


def build_corrected_validation_policy(path_audit: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "old_policy": {
            "future_modules_not_created": "all(not exists(path) for prohibited_future_paths)",
            "problem": "This blocks historically created standalone engine shell files, even if R13 did not modify or create them.",
        },
        "corrected_policy": {
            "future_modules_not_newly_created_or_modified_by_R13": [
                "Historical tracked files may exist.",
                "Historical tracked files must have clean git status.",
                "Untracked future implementation files remain blocking.",
                "Tracked but modified future implementation files remain blocking.",
                "Frozen legacy strategy files must remain unchanged.",
            ],
            "allowed_existing_classifications": [
                "ABSENT_OK",
                "HISTORICAL_TRACKED_UNCHANGED",
            ],
            "blocking_classifications": [
                "TRACKED_BUT_MODIFIED_REQUIRES_REVIEW",
                "UNTRACKED_NEW_REQUIRES_REVIEW",
                "EXISTS_UNCLASSIFIED_REQUIRES_REVIEW",
            ],
        },
        "path_audit_summary": [
            {
                "path": row["path"],
                "exists": row["exists"],
                "tracked": row["tracked"],
                "git_status_porcelain": row["git_status_porcelain"],
                "classification": row["classification"],
            }
            for row in path_audit
        ],
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    if not R12C.exists():
        raise FileNotFoundError(f"Missing prerequisite: {rel(R12C)}")
    if not R13.exists():
        raise FileNotFoundError(f"Missing failed R13 report: {rel(R13)}")

    r12c = read_json(R12C)
    if r12c.get("decision", {}).get("k2_r12c_market_gate_equivalence_retry_passed") is not True:
        raise RuntimeError("R12C prerequisite not passed.")

    r13_failure = summarize_r13_failure()
    path_audit = [file_status(path) for path in R13_PROHIBITED_PATHS]

    blocking_paths = [
        row for row in path_audit
        if row["classification"] not in {"ABSENT_OK", "HISTORICAL_TRACKED_UNCHANGED"}
    ]
    historical_existing_paths = [
        row for row in path_audit
        if row["classification"] == "HISTORICAL_TRACKED_UNCHANGED"
    ]

    failed_artifact_status = [
        file_status(path)
        for path in R13_FAILED_ARTIFACTS
        if (ROOT / path).exists()
    ]

    corrected_policy = build_corrected_validation_policy(path_audit)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "r13b_gap_rca_complete": True,
        "r12c_loaded": True,
        "r12c_equivalence_ready": r12c.get("decision", {}).get("market_gate_equivalence_ready") is True,
        "r13_failed_report_loaded": R13.exists(),
        "r13_failure_confirmed": r13_failure["failure_confirmed"],
        "prohibited_paths_audited": True,
        "prohibited_path_count": len(path_audit),
        "historical_existing_path_count": len(historical_existing_paths),
        "blocking_path_count": len(blocking_paths),
        "all_existing_future_paths_historical_or_absent": len(blocking_paths) == 0,
        "corrected_validation_policy_defined": True,
        "failed_r13_artifacts_preserved": len(failed_artifact_status) > 0,
        "proposal_only": True,
        "strategy_logic_changed": False,
        "strategy_integration_changed": False,
        "legacy_backtest_called": False,
        "backtest_engine_run": False,
        "full_5y_backtest_run": False,
        "candidate_generation_extracted": False,
        "buy_add_reduce_exit_extracted": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
    }

    ready_for_r13c = all([
        validations["r13b_gap_rca_complete"],
        validations["r13_failure_confirmed"],
        validations["all_existing_future_paths_historical_or_absent"],
        validations["corrected_validation_policy_defined"],
        validations["strategy_files_unchanged"],
    ])

    decision = {
        "k2_r13b_uptrend_core_wiring_proposal_gap_rca_passed": ready_for_r13c,
        "root_cause": (
            "R13 validation rule was too strict: it treated historical standalone engine shell files as forbidden new future implementation files."
            if ready_for_r13c
            else "R13 found one or more future implementation paths that are new or modified and require manual review."
        ),
        "r13_original_proposal_can_be_retried_with_corrected_validation": ready_for_r13c,
        "market_gate_equivalence_ready": r12c.get("decision", {}).get("market_gate_equivalence_ready") is True,
        "uptrend_core_implementation_allowed_now": False,
        "market_gate_strategy_integration_allowed_now": False,
        "formula_patch_allowed_now": False,
        "candidate_extraction_allowed_now": False,
        "implementation_may_resume": False,
        "requires_user_approval_before_next_stage": True,
        "next_stage_after_user_approval": (
            "4C-2C-4E-ENGINE-K2-R13C-UPTREND_CORE_GATE_WIRING_PROPOSAL_RETRY_WITH_HISTORICAL_SHELL_AWARE_VALIDATION"
            if ready_for_r13c
            else "4C-2C-4E-ENGINE-K2-R13C-MANUAL_REVIEW_OF_NEW_OR_MODIFIED_FUTURE_PATHS"
        ),
        "conclusion": (
            "K2_R13B_PASS_VALIDATION_RULE_TOO_STRICT_READY_FOR_R13C_RETRY"
            if ready_for_r13c
            else "K2_R13B_BLOCKED_NEW_OR_MODIFIED_FUTURE_PATHS_REQUIRE_MANUAL_REVIEW"
        ),
        "recommended_next_action": (
            "Retry R13 with corrected validation: historical tracked unchanged shell files are allowed; new/modified implementation files remain blocking."
            if ready_for_r13c
            else "Inspect blocking paths before retrying R13."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R13B-UPTREND_CORE_WIRING_PROPOSAL_GAP_RCA",
        "status": "UPTREND_CORE_WIRING_PROPOSAL_GAP_RCA_COMPLETE",
        "purpose": "Determine why R13 proposal validation failed on future_modules_not_created and define corrected validation policy.",
        "r12c_summary": {
            "path": rel(R12C),
            "market_gate_equivalence_ready": r12c.get("decision", {}).get("market_gate_equivalence_ready"),
            "row_count": r12c.get("equivalence", {}).get("row_count"),
            "mismatch_count": r12c.get("equivalence", {}).get("mismatch_count"),
        },
        "r13_failure_summary": r13_failure,
        "prohibited_path_audit": path_audit,
        "historical_existing_paths": historical_existing_paths,
        "blocking_paths": blocking_paths,
        "failed_r13_artifacts_preserved": failed_artifact_status,
        "corrected_validation_policy": corrected_policy,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)
    write_json(EVIDENCE_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R13B — Uptrend Core Wiring Proposal Gap RCA")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## R13 Failure Summary")
    md.append("```json")
    md.append(json.dumps(r13_failure, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Prohibited Path Audit")
    md.append("```json")
    md.append(json.dumps(path_audit, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Corrected Validation Policy")
    md.append("```json")
    md.append(json.dumps(corrected_policy, indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_ENGINE_K2_R13B_UPTREND_CORE_WIRING_PROPOSAL_GAP_RCA_COMPLETE")
    print("status:", report["status"])
    print("r12c_summary:", json.dumps(report["r12c_summary"], ensure_ascii=False))
    print("r13_failure_summary:", json.dumps(r13_failure, ensure_ascii=False))
    print("prohibited_path_audit:", json.dumps(path_audit, ensure_ascii=False))
    print("historical_existing_paths:", json.dumps(historical_existing_paths, ensure_ascii=False))
    print("blocking_paths:", json.dumps(blocking_paths, ensure_ascii=False))
    print("corrected_validation_policy:", json.dumps(corrected_policy, ensure_ascii=False))
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
