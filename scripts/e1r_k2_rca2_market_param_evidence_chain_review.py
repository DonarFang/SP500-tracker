#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

R9 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json"
R9B = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json"
R9C = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9C_115_RETURN_GENERATOR_TRACE.json"
R8 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R8_MARKET_STATE_PARAMETER_AUDIT.json"
TARGET_ARTIFACT = ROOT / "exports/e1r_v0_2_backtest_summary.json"
GENERATOR_TRACE = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_RCA2_MARKET_PARAM_EVIDENCE_CHAIN_REVIEW.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_RCA2_MARKET_PARAM_EVIDENCE_CHAIN_REVIEW.md"
ARCH_MD = ROOT / "docs/architecture/E1R_4C2C4E_ENGINE_K2_RCA2_MARKET_PARAM_EVIDENCE_CHAIN_REVIEW.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_rca2_market_param_evidence_chain_review.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
]

BLOCKING_FIELDS = [
    "market_entry_gate",
    "market_gate_enabled",
    "risk_off_below_spx_ma50",
    "market_shock_gate_enabled",
    "market_shock_daily_return",
]

AUDIT_POLLUTION_PREFIXES = [
    "docs/research/E1R_4C2C4E_ENGINE_K2_",
    "docs/architecture/E1R_4C2C4E_ENGINE_K2_",
    "exports/e1r_engine/audit/",
    "exports/e1r_engine/equivalence/",
    "scripts/e1r_k2_r9",
    "scripts/e1r_k2_rca",
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


def compact(v: Any, max_len: int = 2000) -> Any:
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


def path_is_polluted(path_s: str | None) -> bool:
    if not path_s:
        return False
    return any(path_s.startswith(prefix) for prefix in AUDIT_POLLUTION_PREFIXES)


def load_required_reports() -> dict[str, Any]:
    missing = [rel(p) for p in [R9, R9B, R9C, R8] if not p.exists()]
    if missing:
        raise FileNotFoundError(f"Missing required reports: {missing}")

    return {
        "r8": read_json(R8),
        "r9": read_json(R9),
        "r9b": read_json(R9B),
        "r9c": read_json(R9C),
    }


def extract_attempt_summary(reports: dict[str, Any]) -> list[dict[str, Any]]:
    r9 = reports["r9"]
    r9b = reports["r9b"]
    r9c = reports["r9c"]

    attempts = []

    attempts.append({
        "attempt": "K2-R9-MARKET_STATE_115_RETURN_ARTIFACT_AUDIT",
        "objective": "Find the exact 115% E1R artifact and compare whether it contains market gate parameters.",
        "achieved": {
            "target_artifact_found": r9.get("decision", {}).get("full_115_artifact_verified"),
            "target_return_verified": r9.get("validations", {}).get("target_return_116_74_verified"),
        },
        "not_achieved": {
            "market_state_115_replication_ready": r9.get("decision", {}).get("market_state_115_replication_ready"),
            "blocking_unresolved": [
                x for x in r9.get("unresolved", [])
                if x.get("blocking_for_replication")
            ],
        },
        "failure_mode": "Target artifact was found, but the summary artifact did not persist the required market gate parameter fields.",
        "evidence_boundary": "Artifact-level summary only; insufficient for parameter identity.",
    })

    attempts.append({
        "attempt": "K2-R9B-115_RETURN_ARTIFACT_RECOVERY",
        "objective": "Recover generator/call-chain candidates and parameter evidence for the 115% artifact.",
        "achieved": {
            "target_artifact_exists": r9b.get("validations", {}).get("target_artifact_exists"),
            "target_return_verified": r9b.get("validations", {}).get("target_return_verified"),
            "repository_grep_completed": r9b.get("validations", {}).get("repository_grep_completed"),
            "candidate_script_analysis_completed": r9b.get("validations", {}).get("candidate_script_analysis_completed"),
        },
        "not_achieved": {
            "market_state_115_replication_ready": r9b.get("decision", {}).get("market_state_115_replication_ready"),
            "blocking_unresolved": [
                x for x in r9b.get("unresolved", [])
                if x.get("blocking_for_replication")
            ],
        },
        "failure_mode": "Generator candidates were found, but the highest-ranked candidate set included self/audit-script pollution and did not isolate original source-line evidence.",
        "evidence_boundary": "Repository grep and candidate grouping; insufficient pollution controls.",
    })

    attempts.append({
        "attempt": "K2-R9C-115_RETURN_GENERATOR_TRACE",
        "objective": "Parse generator trace and recover clean source/call-chain evidence for market gate parameters.",
        "achieved": {
            "generator_path_trace_exists": r9c.get("validations", {}).get("generator_path_trace_exists"),
            "generator_path_trace_relevant_rows_found": r9c.get("validations", {}).get("generator_path_trace_relevant_rows_found"),
            "target_artifact_exists": r9c.get("validations", {}).get("target_artifact_exists"),
            "clean_repo_grep_completed": r9c.get("validations", {}).get("clean_repo_grep_completed"),
        },
        "not_achieved": {
            "market_state_115_replication_ready_claimed": r9c.get("decision", {}).get("market_state_115_replication_ready"),
            "market_entry_gate_evidence_count": (
                r9c.get("market_param_evidence", {})
                   .get("by_term", {})
                   .get("market_entry_gate", {})
                   .get("evidence_count")
            ),
            "source_quality_problem": "Evidence samples still include R9/R9B/R9C audit artifacts and generated reports.",
        },
        "failure_mode": "R9C validation accepted evidence counts without distinguishing original source-line evidence from generated audit/report evidence; market_entry_gate was not required.",
        "evidence_boundary": "Term-level evidence count is not equivalent to clean source-line provenance.",
    })

    return attempts


def extract_current_evidence_status(reports: dict[str, Any]) -> dict[str, Any]:
    r9c = reports["r9c"]
    mpe = r9c.get("market_param_evidence", {}).get("by_term", {})

    field_status = {}
    for field in BLOCKING_FIELDS:
        evidence = mpe.get(field, {})
        samples = evidence.get("sample", [])
        clean_samples = []
        polluted_samples = []
        for s in samples:
            file_s = s.get("file") or s.get("path") or ""
            if path_is_polluted(str(file_s)):
                polluted_samples.append(compact(s))
            else:
                clean_samples.append(compact(s))
        field_status[field] = {
            "reported_evidence_count": evidence.get("evidence_count", 0),
            "sample_count": len(samples),
            "clean_sample_count_after_pollution_filter": len(clean_samples),
            "polluted_sample_count_after_filter": len(polluted_samples),
            "clean_sample_examples": clean_samples[:10],
            "polluted_sample_examples": polluted_samples[:10],
            "requires_source_line_trace": True,
        }

    return {
        "blocking_fields": BLOCKING_FIELDS,
        "field_status": field_status,
        "generator_trace_file": {
            "exists": GENERATOR_TRACE.exists(),
            "path": rel(GENERATOR_TRACE),
            "sha256": sha256(GENERATOR_TRACE),
        },
        "target_artifact": {
            "exists": TARGET_ARTIFACT.exists(),
            "path": rel(TARGET_ARTIFACT),
            "sha256": sha256(TARGET_ARTIFACT),
        },
    }


def build_root_cause_analysis(attempts: list[dict[str, Any]], current_status: dict[str, Any]) -> dict[str, Any]:
    return {
        "three_attempt_stop_rule_triggered": True,
        "repeated_objective": "Recover source-quality evidence proving the 115% E1R v0.2 market gate / market state parameter chain before standalone replication.",
        "attempts_counted": [
            "K2-R9",
            "K2-R9B",
            "K2-R9C",
        ],
        "what_is_known": [
            "The 115% / 116.7435999134756 E1R artifact exists at exports/e1r_v0_2_backtest_summary.json.",
            "The target artifact identifies strategy_id E1R_REGIME_AWARE_V0_2.",
            "The target artifact identifies regime_aware_logic as UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE.",
            "The sidecar was active in SIDEWAYS / MA_CONFLICT for 135 rows in the target artifact.",
            "Short-window R8 parameter audit found D3_RISK_OFF_PLUS_SHOCK_GATE, market_gate_enabled=True, risk_off_below_spx_ma50=True, market_shock_gate_enabled=True, market_shock_daily_return=-0.02.",
            "R7/R8 short-window evidence is source-equivalent for the short-window golden master, but does not by itself prove the full 115% artifact parameter identity.",
        ],
        "what_is_not_yet_proven": [
            "The full 115% E1R v0.2 artifact itself does not persist market_entry_gate or the required market gate parameter fields.",
            "The original generator source-line chain for each market gate parameter has not been cleanly isolated.",
            "Evidence counts in R9C include generated audit/report artifacts and therefore cannot be accepted as source-line proof.",
            "market_entry_gate had zero evidence in R9C and was not included as a required blocking condition.",
        ],
        "root_causes": [
            {
                "id": "RC1_EVIDENCE_COUNT_OVER_SOURCE_PROVENANCE",
                "description": "R9C treated term evidence count as sufficient, but did not require original source-line provenance.",
                "impact": "Generated audit/report files could satisfy evidence_count without proving the real generator code path.",
            },
            {
                "id": "RC2_INCOMPLETE_POLLUTION_FILTER",
                "description": "R9B/R9C excluded some self-reference scripts but did not exclude all generated audit/research/equivalence artifacts.",
                "impact": "Evidence samples were contaminated by prior audit outputs.",
            },
            {
                "id": "RC3_REQUIRED_FIELD_SET_INCOMPLETE",
                "description": "R9C did not require market_entry_gate or an explicitly equivalent output structure as a blocking field.",
                "impact": "market_state_115_replication_ready could become true despite market_entry_gate evidence_count=0.",
            },
            {
                "id": "RC4_SHORT_WINDOW_AND_FULL_ARTIFACT_BOUNDARY",
                "description": "R8 short-window parameters are strong but cannot be automatically promoted to full 115% artifact identity.",
                "impact": "A separate full artifact generator/source-line trace is still required.",
            },
            {
                "id": "RC5_GENERATOR_TRACE_JSON_IS_A_TRACE_INDEX_NOT_DIRECT_PROOF",
                "description": "The generator trace JSON points to candidate files and source fragments, but it is not itself the original generator implementation.",
                "impact": "The next step must inspect original source files / source_head / source lines, not accept the trace index as final proof.",
            },
        ],
        "corrective_principles": [
            "Do not proceed to implementation or replication proposal until each blocking field has clean source-line evidence.",
            "Evidence must be classified by quality: original source code > original generator artifact with source_head/source_line > runtime trace > generated audit report.",
            "Generated docs/research/E1R_4C2C4E_ENGINE_K2_* and exports/e1r_engine/* must be excluded from source proof.",
            "market_entry_gate must be either found directly or explicitly mapped to an equivalent source structure.",
            "A PASS can mean RCA complete; it must not imply replication_ready unless all blocking evidence gates are satisfied.",
        ],
    }


def build_corrective_plan() -> dict[str, Any]:
    return {
        "next_stage": "4C-2C-4E-ENGINE-K2-R9D-MARKET_PARAM_SOURCE_LINE_TRACE",
        "stage_type": "source-line audit only",
        "allowed": [
            "Read existing source files and existing generator trace artifacts.",
            "Extract source-line snippets for market gate parameters.",
            "Classify evidence quality.",
            "Produce a field-by-field evidence matrix.",
            "Commit only audit/report/script files.",
        ],
        "not_allowed": [
            "No strategy logic patch.",
            "No full 5Y backtest.",
            "No short-window rerun unless explicitly approved.",
            "No candidate/BUY/ADD/REDUCE/EXIT extraction.",
            "No official result or dashboard change.",
            "No replication proposal until R9D passes source-line evidence gates.",
        ],
        "mandatory_source_filter": {
            "include_preferred": [
                "src/engine/backtest.py",
                "src/engine/e1r_composer.py",
                "src/engine/e1r_sidecar_sleeve.py",
                "original generator candidate source files referenced by E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
            ],
            "exclude_as_primary_proof": [
                "docs/research/E1R_4C2C4E_ENGINE_K2_*.json",
                "docs/research/E1R_4C2C4E_ENGINE_K2_*.md",
                "docs/architecture/E1R_4C2C4E_ENGINE_K2_*.md",
                "exports/e1r_engine/audit/*.json",
                "exports/e1r_engine/equivalence/*.json",
                "scripts/e1r_k2_r9*.py",
                "scripts/e1r_k2_rca*.py",
            ],
        },
        "required_evidence_matrix_fields": [
            {
                "field": "market_gate_enabled",
                "required": "source line or source_head showing assignment/default and call-path into run_stateful_simulation assumptions for E1R v0.2 core",
            },
            {
                "field": "risk_off_below_spx_ma50",
                "required": "source line or source_head showing assignment/default and usage in market_state / entry_capacity / risk-off logic",
            },
            {
                "field": "market_shock_gate_enabled",
                "required": "source line or source_head showing assignment/default and usage in _shock_active",
            },
            {
                "field": "market_shock_daily_return",
                "required": "source line or source_head showing assignment/default value -0.02 and usage in _shock_active",
            },
            {
                "field": "market_entry_gate_or_equivalent",
                "required": "source evidence showing output structure or explicit equivalent: blocked BUY/ADD, unaffected HOLD/REDUCE/EXIT, entry_capacity mapping, or generated market gate report",
            },
            {
                "field": "e1r_v0_2_core_call_chain",
                "required": "source evidence showing run_stateful_simulation -> core_variant_result/_core_e1r -> compose_e1r_v0_2_variant",
            },
            {
                "field": "e1r_v0_2_sidecar_call_chain",
                "required": "source evidence showing build_e1r_sidecar_sleeve -> sidecar_result -> compose_e1r_v0_2_variant, MA_CONFLICT 135-row sleeve",
            },
        ],
        "pass_conditions_for_r9d": [
            "Every required evidence matrix field is PASS or explicitly documented as equivalent with source-line proof.",
            "No blocking field relies only on generated audit/report/equivalence files.",
            "R8 short-window parameters are treated as supporting evidence, not sole proof for full 115% artifact.",
            "market_state_115_replication_ready remains false unless all source-line evidence gates pass.",
            "formula_patch_allowed_now remains false.",
        ],
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    reports = load_required_reports()
    attempts = extract_attempt_summary(reports)
    current_status = extract_current_evidence_status(reports)
    rca = build_root_cause_analysis(attempts, current_status)
    corrective_plan = build_corrective_plan()

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "rca2_review_complete": True,
        "three_attempt_stop_rule_triggered": True,
        "repeated_objective_identified": True,
        "attempts_reviewed_count": len(attempts),
        "r9_loaded": True,
        "r9b_loaded": True,
        "r9c_loaded": True,
        "r8_loaded": True,
        "evidence_vs_assumption_separated": True,
        "root_causes_identified": len(rca["root_causes"]) >= 3,
        "corrective_plan_defined": True,
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
    }

    decision = {
        "k2_rca2_market_param_evidence_chain_review_passed": all([
            validations["rca2_review_complete"],
            validations["three_attempt_stop_rule_triggered"],
            validations["repeated_objective_identified"],
            validations["evidence_vs_assumption_separated"],
            validations["root_causes_identified"],
            validations["corrective_plan_defined"],
            validations["strategy_files_unchanged"],
        ]),
        "implementation_may_resume": False,
        "market_state_115_replication_ready": False,
        "formula_patch_allowed_now": False,
        "candidate_extraction_allowed_now": False,
        "next_required_stage": corrective_plan["next_stage"],
        "conclusion": "K2_RCA2_PASS_STOP_CONFIRMED_READY_FOR_R9D_SOURCE_LINE_TRACE_ONLY",
        "recommended_next_action": "Proceed only to R9D source-line trace with strict pollution filters and field-by-field evidence gates. Do not implement or patch.",
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-RCA2-MARKET_PARAM_EVIDENCE_CHAIN_REVIEW",
        "status": "MARKET_PARAM_EVIDENCE_CHAIN_RCA2_COMPLETE",
        "purpose": "Stop after three attempts toward the same objective and perform review/root cause analysis before next market-param evidence step.",
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
        "source_reports": {
            "r8": {"path": rel(R8), "sha256": sha256(R8)},
            "r9": {"path": rel(R9), "sha256": sha256(R9)},
            "r9b": {"path": rel(R9B), "sha256": sha256(R9B)},
            "r9c": {"path": rel(R9C), "sha256": sha256(R9C)},
            "target_artifact": {"path": rel(TARGET_ARTIFACT), "sha256": sha256(TARGET_ARTIFACT)},
            "generator_trace": {"path": rel(GENERATOR_TRACE), "sha256": sha256(GENERATOR_TRACE)},
        },
        "attempt_review": attempts,
        "current_evidence_status": current_status,
        "root_cause_analysis": rca,
        "corrective_plan": corrective_plan,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-RCA2 — Market Parameter Evidence Chain Review")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Stop Rule")
    md.append("Three attempts toward the same objective have not reached the final replication evidence standard. Implementation is stopped before the next step.")
    md.append("")
    md.append("## Attempt Review")
    md.append("```json")
    md.append(json.dumps(attempts, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Current Evidence Status")
    md.append("```json")
    md.append(json.dumps(current_status, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Root Cause Analysis")
    md.append("```json")
    md.append(json.dumps(rca, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Corrective Plan")
    md.append("```json")
    md.append(json.dumps(corrective_plan, indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_ENGINE_K2_RCA2_MARKET_PARAM_EVIDENCE_CHAIN_REVIEW_COMPLETE")
    print("status:", report["status"])
    print("attempt_review:", json.dumps(attempts, ensure_ascii=False))
    print("current_evidence_status:", json.dumps(current_status, ensure_ascii=False))
    print("root_cause_analysis:", json.dumps(rca, ensure_ascii=False))
    print("corrective_plan:", json.dumps(corrective_plan, ensure_ascii=False))
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
