#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import hashlib
import re
from datetime import datetime, timezone
from typing import Any
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

C_REPORT = ROOT / "docs/research/E1R_4C2C4E_C_BRANCH_EXECUTION_TRANSITION_AUDIT.json"
B2_REPORT = ROOT / "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json"
B3_REPORT = ROOT / "docs/research/E1R_4C2C4E_B3_CONTINUOUS_STATEFUL_SMOKE_TYPED_CONTRACT.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_D_CONTINUOUS_STATEFUL_ADAPTER_DESIGN.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_D_CONTINUOUS_STATEFUL_ADAPTER_DESIGN.md"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

SEARCH_PATHS = [
    ROOT / "src",
    ROOT / "scripts",
]

INVALID_ARTIFACTS = [
    "exports/e1r_unified_5y_full_account_v1_result.json",
    "exports/e1r_unified_5y_dashboard_research_bundle.json",
    "exports/e1r_combined_5y_original_max3_result.json",
    "exports/e1r_combined_5y_original_max3_equity_curve.json",
    "exports/e1r_combined_5y_original_max3_summary.json",
]

PROPOSED_NEW_FILES = [
    "src/engine/e1r_continuous_stateful_adapter.py",
    "scripts/run_e1r_continuous_stateful_smoke_4c2c4e_e.py",
    "docs/research/E1R_4C2C4E_E_CONTINUOUS_STATEFUL_ADAPTER_SMOKE.json",
    "docs/research/E1R_4C2C4E_E_CONTINUOUS_STATEFUL_ADAPTER_SMOKE.md",
]

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))

def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def read_json(path: Path) -> Any:
    return json.loads(path.read_text())

def read_text(path: Path) -> str:
    return path.read_text(errors="replace")

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def py_files() -> list[Path]:
    out = []
    for root in SEARCH_PATHS:
        if root.exists():
            out.extend(sorted(root.rglob("*.py")))
    return out

def symbol_hits(patterns: list[str], max_hits_each: int = 60) -> dict[str, list[dict[str, Any]]]:
    results = {p: [] for p in patterns}

    for path in py_files():
        text = read_text(path)
        lines = text.splitlines()

        for pat in patterns:
            if pat not in text:
                continue
            for i, line in enumerate(lines, start=1):
                if pat in line and len(results[pat]) < max_hits_each:
                    results[pat].append({
                        "path": rel(path),
                        "line": i,
                        "text": line.strip()[:260],
                    })

    return results

def ast_function_index() -> list[dict[str, Any]]:
    functions = []
    interesting_terms = [
        "leader", "score", "rank", "candidate", "signal", "stateful",
        "market", "gate", "regime", "sidecar", "buy", "exit", "reduce",
    ]

    for path in py_files():
        try:
            text = read_text(path)
            tree = ast.parse(text)
        except Exception:
            continue

        lines = text.splitlines()

        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue

            name_lower = node.name.lower()
            if not any(term in name_lower for term in interesting_terms):
                continue

            start = getattr(node, "lineno", None)
            end = getattr(node, "end_lineno", None)
            source = "\n".join(lines[start - 1:end]) if start and end else ""

            functions.append({
                "path": rel(path),
                "name": node.name,
                "start_line": start,
                "end_line": end,
                "line_count": end - start + 1 if start and end else None,
                "args": [a.arg for a in node.args.args],
                "contains_buy": "BUY" in source or "buy" in source,
                "contains_exit": "EXIT" in source or "exit" in source,
                "contains_reduce": "REDUCE" in source or "reduce" in source,
                "contains_leader_score": "leader_score" in source,
                "contains_regime": "regime" in source,
                "contains_sidecar": "sidecar" in source.lower(),
                "contains_positions": "positions" in source,
                "contains_cash": "cash" in source,
            })

    return functions

def load_prior_evidence() -> dict[str, Any]:
    evidence = {
        "c_report_exists": C_REPORT.exists(),
        "b2_report_exists": B2_REPORT.exists(),
        "b3_report_exists": B3_REPORT.exists(),
        "c_decision": None,
        "b2_assumption_contract": None,
        "b3_smoke_summary": None,
    }

    if C_REPORT.exists():
        c = read_json(C_REPORT)
        evidence["c_decision"] = c.get("decision")
        evidence["c_key_facts"] = {
            "status": c.get("status"),
            "engine_reads_e1r_regime": c.get("decision", {}).get("engine_reads_e1r_regime"),
            "engine_calls_sidecar_inside_run_stateful": c.get("decision", {}).get("engine_calls_sidecar_inside_run_stateful"),
            "engine_has_sideways_branch_order_generation_evidence": c.get("decision", {}).get("engine_has_sideways_branch_order_generation_evidence"),
            "b3_proves_sidecar_execution": c.get("decision", {}).get("b3_proves_sidecar_execution"),
            "existing_engine_sufficient_for_official_4e": c.get("decision", {}).get("existing_engine_sufficient_for_official_4e"),
            "conclusion": c.get("decision", {}).get("conclusion"),
        }

    if B2_REPORT.exists():
        b2 = read_json(B2_REPORT)
        evidence["b2_assumption_contract"] = {
            "status": b2.get("status"),
            "assumption_key_count": b2.get("contract", {}).get("assumption_key_count"),
            "required_without_default_keys": b2.get("safe_assumption_blueprint", {}).get("required_without_default_keys"),
            "unresolved_required_keys": b2.get("safe_assumption_blueprint", {}).get("unresolved_required_keys"),
        }

    if B3_REPORT.exists():
        b3 = read_json(B3_REPORT)
        evidence["b3_smoke_summary"] = {
            "status": b3.get("status"),
            "conclusion": b3.get("conclusion"),
            "known_conclusion_bug": b3.get("conclusion") == "4C2C4E_B3_SMOKE_FAILED_REVIEW_BEFORE_CONTINUING",
            "engine_summary": {
                "record_count": b3.get("engine_summary", {}).get("record_count"),
                "regime_counts": b3.get("engine_summary", {}).get("regime_counts"),
                "branch_plan_counts": b3.get("engine_summary", {}).get("branch_plan_counts"),
                "max_open_positions": b3.get("engine_summary", {}).get("max_open_positions"),
                "open_position_violations_count": b3.get("engine_summary", {}).get("open_position_violations_count"),
            },
            "sidecar_summary": b3.get("sidecar_summary"),
        }

    return evidence

def design_adapter_contract() -> dict[str, Any]:
    return {
        "adapter_name": "E1RContinuousStatefulAdapter",
        "proposed_module": "src/engine/e1r_continuous_stateful_adapter.py",
        "purpose": "Official E1R 5Y continuous-stateful account orchestrator.",
        "core_principle": "One account, one timeline, continuous cash/positions, daily mark-to-market, explicit regime branch execution.",
        "non_goals": [
            "Do not compose or stitch return curves.",
            "Do not read invalid historical result artifacts.",
            "Do not treat sidecar Top10 as live account holdings.",
            "Do not modify frozen strategy files in adapter design stage.",
            "Do not hide transition behavior inside undocumented assumptions.",
        ],
        "account_state_schema": {
            "cash": "float",
            "positions": {
                "symbol": "str",
                "shares": "float",
                "cost_basis": "float",
                "entry_date": "YYYY-MM-DD",
                "branch_origin": "UPTREND | SIDEWAYS_MA_CONFLICT",
                "last_action": "BUY | ADD | REDUCE | HOLD | EXIT",
                "holding_days": "int",
                "metadata": "dict",
            },
            "total_equity": "cash + market_value(positions)",
            "open_positions_count": "len(positions)",
            "max_open_positions": 3,
        },
        "daily_record_schema": {
            "date": "YYYY-MM-DD",
            "regime": "UPTREND | SIDEWAYS | DOWNTREND",
            "subclass": "NO_SUBCLASS | MA_CONFLICT | DETERIORATION_TRANSITION | RECOVERY_TRANSITION",
            "active_branch": "UPTREND | SIDEWAYS_MA_CONFLICT | CASH_DEFENSIVE",
            "cash": "float",
            "positions_value": "float",
            "total_equity": "float",
            "open_positions_count": "int <= 3",
            "orders": "list[Order]",
            "candidate_source": "UPTREND_SIGNAL_PROVIDER | SIDECAR_TOP10 | NONE",
            "guard_flags": "dict",
        },
        "order_schema": {
            "date": "YYYY-MM-DD",
            "symbol": "str",
            "action": "BUY | ADD | REDUCE | EXIT | HOLD",
            "quantity_or_weight": "float",
            "price": "float",
            "branch": "UPTREND | SIDEWAYS_MA_CONFLICT | CASH_DEFENSIVE",
            "reason": "str",
        },
    }

def design_daily_loop() -> dict[str, Any]:
    return {
        "pseudocode": [
            "initialize cash = 100000, positions = {}",
            "for each trading day in aligned 5Y timeline:",
            "    mark_to_market existing positions using close price",
            "    read regime and subclass for date",
            "    if regime == UPTREND:",
            "        branch = UPTREND",
            "        candidates/orders = uptrend_signal_provider(date, current_state)",
            "        execute orders with account-level max_positions <= 3",
            "    elif regime == SIDEWAYS and subclass == MA_CONFLICT:",
            "        branch = SIDEWAYS_MA_CONFLICT",
            "        candidates = sidecar_top10_provider(date)",
            "        convert sidecar Top10 into live account target <= 3 positions",
            "        execute transition orders explicitly",
            "    else:",
            "        branch = CASH_DEFENSIVE",
            "        execute defensive transition orders explicitly",
            "    enforce open_positions_count <= 3",
            "    record daily account state",
        ],
        "hard_guards": [
            "Fail if open_positions_count > 3 on any date.",
            "Fail if any invalid artifact path is read.",
            "Fail if composer is imported or called for official result.",
            "Fail if sidecar holdings_len > 3 is interpreted as live holdings.",
            "Fail if DETERIORATION/RECOVERY/DOWNTREND branch leaves positions open without explicit approved rule.",
            "Fail if daily record lacks cash, positions_value, total_equity, active_branch.",
        ],
    }

def design_transition_policy() -> dict[str, Any]:
    return {
        "status": "DESIGN_REQUIRES_USER_CONFIRMATION_BEFORE_IMPLEMENTATION",
        "policy_options": {
            "UPTREND_to_SIDEWAYS_MA_CONFLICT": {
                "recommended": "transition_to_sidecar_targets",
                "meaning": "Existing UPTREND positions are not automatically assumed valid. Adapter compares current holdings with sidecar Top10 candidate pool and moves toward <=3 sidecar live targets.",
                "why": "C audit showed current engine kept UPTREND positions during SIDEWAYS while sidecar was only data-available; formal E1R requires branch execution.",
                "implementation_guard": "Every kept position must be explicitly tagged as also passing the SIDEWAYS sidecar candidate/target rule; otherwise exit or reduce by approved transition rule.",
            },
            "SIDEWAYS_MA_CONFLICT_to_UPTREND": {
                "recommended": "transition_to_uptrend_targets",
                "meaning": "Sidecar-origin positions are re-evaluated by UPTREND branch. They can be kept only if current UPTREND branch would hold them.",
                "implementation_guard": "No position silently changes branch_origin without a logged transition decision.",
            },
            "ANY_to_DETERIORATION_OR_RECOVERY": {
                "recommended": "cash_defensive_exit",
                "meaning": "Exit live equity positions and hold cash unless a defensive holding rule is explicitly approved later.",
                "implementation_guard": "open_positions_count should become 0 after transition execution window.",
            },
            "ANY_to_DOWNTREND": {
                "recommended": "cash_defensive_exit",
                "meaning": "Exit live equity positions and hold cash.",
                "implementation_guard": "open_positions_count should become 0 after transition execution window.",
            },
        },
        "unresolved_decision": "Whether transition exits occur same close, next close, or existing engine's execution convention. This must be confirmed before official full 5Y.",
    }

def design_branch_providers() -> dict[str, Any]:
    return {
        "UPTREND_signal_provider": {
            "status": "NEEDS_ENTRYPOINT_AUDIT_BEFORE_IMPLEMENTATION",
            "goal": "Reuse existing validated UPTREND candidate/order logic without modifying frozen strategy files.",
            "allowed_sources": [
                "Existing leader score / rank / buy candidate functions if callable independently.",
                "Existing run_stateful_simulation internals only if extracted into a non-strategy-changing provider after approval.",
            ],
            "not_allowed": [
                "Use old invalid result artifacts as UPTREND source.",
                "Approximate UPTREND rules by a new ranking formula without explicit approval.",
            ],
            "next_audit_needed": "Locate exact existing UPTREND candidate/order generation logic and define a read-only provider API.",
        },
        "SIDEWAYS_MA_CONFLICT_provider": {
            "status": "AVAILABLE_AS_CANDIDATE_PROVIDER",
            "source": "src.engine.e1r_sidecar_sleeve.build_e1r_sidecar_sleeve",
            "confirmed_behavior": [
                "active only in SIDEWAYS / MA_CONFLICT in strict sidecar audit",
                "Top10 selected_count is candidate/basket pool",
                "gross_exposure = 0.25 in original sidecar model",
            ],
            "adapter_responsibility": [
                "Convert Top10 candidate pool into <=3 live account targets.",
                "Generate real account orders.",
                "Record branch_origin = SIDEWAYS_MA_CONFLICT.",
            ],
        },
        "CASH_DEFENSIVE_provider": {
            "status": "DESIGN_DEFINED",
            "source": "adapter-owned transition logic",
            "adapter_responsibility": [
                "Generate EXIT orders for live equity positions.",
                "Hold cash after transition.",
                "Record active_branch = CASH_DEFENSIVE.",
            ],
        },
    }

def design_validation_matrix() -> dict[str, Any]:
    return {
        "adapter_smoke_validations_for_next_stage": {
            "strategy_files_unchanged": True,
            "invalid_artifacts_not_used": True,
            "composer_not_used": True,
            "return_curve_stitching_not_used": True,
            "single_account_state_owned_by_adapter": True,
            "cash_positions_continuous": True,
            "daily_mark_to_market_present": True,
            "active_branch_recorded_daily": True,
            "uptrend_branch_orders_observed": True,
            "sideways_ma_conflict_branch_orders_observed": True,
            "cash_defensive_exit_orders_observed": True,
            "sidecar_top10_never_live_holdings_10": True,
            "max_open_positions_le_3": True,
            "position_violations_zero": True,
            "transition_logs_present": True,
            "official_result_generated": False,
            "full_5y_backtest_run": False,
        },
        "official_5y_validations_later": {
            "full_timeline_covered": "2021-06-11 to 2026-06-18 or current aligned window",
            "daily_record_count_matches_trading_days": True,
            "open_positions_count_max_le_3": True,
            "cash_defensive_regimes_open_positions_zero_or_explicitly_approved": True,
            "orders_have_branch_and_reason": True,
            "equity_curve_derived_from_account_state": True,
            "no_result_stitching": True,
            "no_invalid_artifact_dependency": True,
        },
    }

def inspect_candidate_entrypoints() -> dict[str, Any]:
    patterns = [
        "leader_score",
        "Leader",
        "leader",
        "candidate",
        "BUY",
        "run_stateful_simulation",
        "calculate",
        "rank",
        "relative_strength",
        "trend_health",
        "market_gate",
        "build_e1r_sidecar_sleeve",
        "E1RSidecarConfig",
    ]

    hits = symbol_hits(patterns)
    functions = ast_function_index()

    uptrend_related = [
        f for f in functions
        if (
            f["contains_buy"]
            or f["contains_leader_score"]
            or "leader" in f["name"].lower()
            or "rank" in f["name"].lower()
            or "candidate" in f["name"].lower()
        )
        and "e1r_sidecar_sleeve.py" not in f["path"]
    ]

    sidecar_related = [
        f for f in functions
        if f["contains_sidecar"] or "sidecar" in f["name"].lower()
    ]

    return {
        "keyword_hits": hits,
        "candidate_function_index_count": len(functions),
        "uptrend_related_functions_sample": uptrend_related[:80],
        "sidecar_related_functions_sample": sidecar_related[:40],
        "entrypoint_status": {
            "uptrend_provider_entrypoint_locked": False,
            "sidecar_provider_entrypoint_locked": True,
            "cash_defensive_provider_entrypoint_locked": True,
        },
        "reason": "SIDEWAYS sidecar provider is known. UPTREND order/candidate provider still needs a focused entrypoint audit before adapter implementation.",
    }

def derive_decision(prior: dict[str, Any], entrypoints: dict[str, Any]) -> dict[str, Any]:
    c_ok = prior.get("c_key_facts", {}).get("existing_engine_sufficient_for_official_4e") is False
    sidecar_locked = entrypoints["entrypoint_status"]["sidecar_provider_entrypoint_locked"] is True
    cash_locked = entrypoints["entrypoint_status"]["cash_defensive_provider_entrypoint_locked"] is True
    uptrend_locked = entrypoints["entrypoint_status"]["uptrend_provider_entrypoint_locked"] is True

    if c_ok and sidecar_locked and cash_locked and not uptrend_locked:
        conclusion = "ADAPTER_DESIGN_READY_BUT_UPTREND_PROVIDER_ENTRYPOINT_MUST_BE_LOCKED_BEFORE_IMPLEMENTATION"
        next_action = (
            "Proceed to 4C-2C-4E-D1: UPTREND provider entrypoint audit. "
            "Do not implement adapter trading logic until the validated UPTREND candidate/order source is locked."
        )
    elif c_ok and sidecar_locked and cash_locked and uptrend_locked:
        conclusion = "READY_FOR_4C2C4E_E_ADAPTER_SMOKE_IMPLEMENTATION"
        next_action = (
            "Proceed to 4C-2C-4E-E: implement adapter smoke with explicit branch execution."
        )
    else:
        conclusion = "ADAPTER_DESIGN_NEEDS_REVIEW"
        next_action = (
            "Review missing evidence before adapter implementation."
        )

    return {
        "c_audit_supports_adapter_need": c_ok,
        "sidecar_provider_locked": sidecar_locked,
        "cash_defensive_provider_locked": cash_locked,
        "uptrend_provider_locked": uptrend_locked,
        "adapter_design_complete": True,
        "implementation_allowed_now": False if not uptrend_locked else True,
        "conclusion": conclusion,
        "recommended_next_action": next_action,
    }

def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    prior = load_prior_evidence()
    adapter_contract = design_adapter_contract()
    daily_loop = design_daily_loop()
    transition_policy = design_transition_policy()
    branch_providers = design_branch_providers()
    validation_matrix = design_validation_matrix()
    entrypoints = inspect_candidate_entrypoints()
    decision = derive_decision(prior, entrypoints)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "design_only_no_backtest_run": True,
        "full_5y_backtest_run": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "invalid_artifacts_not_used_as_source": True,
        "composer_not_used": True,
        "return_curve_stitching_not_used": True,
        "c_report_loaded": prior["c_report_exists"],
        "c_conclusion_requires_adapter": prior.get("c_key_facts", {}).get("existing_engine_sufficient_for_official_4e") is False,
        "adapter_contract_defined": bool(adapter_contract),
        "daily_loop_defined": bool(daily_loop),
        "transition_policy_defined": bool(transition_policy),
        "branch_provider_contracts_defined": bool(branch_providers),
        "validation_matrix_defined": bool(validation_matrix),
        "sidecar_provider_locked": decision["sidecar_provider_locked"],
        "cash_defensive_provider_locked": decision["cash_defensive_provider_locked"],
        "uptrend_provider_not_yet_locked": decision["uptrend_provider_locked"] is False,
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-D",
        "status": "CONTINUOUS_STATEFUL_ADAPTER_DESIGN_COMPLETE",
        "purpose": "Design a formal E1R continuous-stateful adapter/orchestrator after C audit proved existing engine does not execute full E1R branches.",
        "policy": {
            "strategy_logic_changed": False,
            "backtest_engine_run": False,
            "full_5y_backtest_run": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
            "invalid_artifacts_used_as_source": False,
            "composer_used": False,
            "return_curve_stitching_used": False,
        },
        "prior_evidence": prior,
        "proposed_new_files": PROPOSED_NEW_FILES,
        "invalid_artifacts_banned": INVALID_ARTIFACTS,
        "adapter_contract": adapter_contract,
        "daily_loop_design": daily_loop,
        "transition_policy": transition_policy,
        "branch_providers": branch_providers,
        "validation_matrix": validation_matrix,
        "entrypoint_inspection": entrypoints,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-D — Continuous-Stateful Adapter / Orchestrator Design")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("Design a formal E1R adapter/orchestrator after 4E-C confirmed that the existing `run_stateful_simulation` reads regime data but does not prove full SIDEWAYS sidecar branch execution inside the account engine.")
    md.append("")
    md.append("## Policy")
    md.append("```json")
    md.append(json.dumps(report["policy"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Prior Evidence")
    md.append("```json")
    md.append(json.dumps(prior, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Adapter Contract")
    md.append("```json")
    md.append(json.dumps(adapter_contract, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Daily Loop Design")
    md.append("```json")
    md.append(json.dumps(daily_loop, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Transition Policy")
    md.append("```json")
    md.append(json.dumps(transition_policy, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Branch Providers")
    md.append("```json")
    md.append(json.dumps(branch_providers, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Validation Matrix")
    md.append("```json")
    md.append(json.dumps(validation_matrix, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Decision")
    md.append("```json")
    md.append(json.dumps(decision, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Next Action")
    md.append("")
    md.append(decision["recommended_next_action"])
    md.append("")

    REPORT_MD.write_text("\n".join(md))

    print("E1R_4C2C4E_D_CONTINUOUS_STATEFUL_ADAPTER_DESIGN_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("prior_key_facts:", json.dumps(prior.get("c_key_facts"), ensure_ascii=False))
    print("adapter_contract_summary:", json.dumps({
        "adapter_name": adapter_contract["adapter_name"],
        "proposed_module": adapter_contract["proposed_module"],
        "core_principle": adapter_contract["core_principle"],
        "max_open_positions": adapter_contract["account_state_schema"]["max_open_positions"],
    }, ensure_ascii=False))
    print("transition_policy_summary:", json.dumps(transition_policy["policy_options"], ensure_ascii=False))
    print("branch_provider_status:", json.dumps({
        "uptrend": branch_providers["UPTREND_signal_provider"]["status"],
        "sideways": branch_providers["SIDEWAYS_MA_CONFLICT_provider"]["status"],
        "cash_defensive": branch_providers["CASH_DEFENSIVE_provider"]["status"],
    }, ensure_ascii=False))
    print("entrypoint_status:", json.dumps(entrypoints["entrypoint_status"], ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
