#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import hashlib
from datetime import datetime, timezone
from typing import Any
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

D3_REPORT = ROOT / "docs/research/E1R_4C2C4E_D3_UPTREND_RUNTIME_EQUIVALENCE_AUDIT.json"
D2B_REPORT = ROOT / "docs/research/E1R_4C2C4E_D2B_REAL_UPTREND_PROVIDER_FILTER_AUDIT.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_D4A_UPTREND_GOLDEN_MASTER_TRACE_CONTRACT.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_D4A_UPTREND_GOLDEN_MASTER_TRACE_CONTRACT.md"

BACKTEST_PATH = ROOT / "src/engine/backtest.py"
SIDECAR_PATH = ROOT / "src/engine/e1r_sidecar_sleeve.py"
COMPOSER_PATH = ROOT / "src/engine/e1r_composer.py"

FROZEN_STRATEGY_FILES = [
    BACKTEST_PATH,
    SIDECAR_PATH,
    COMPOSER_PATH,
]

INVALID_ARTIFACTS = [
    "exports/e1r_unified_5y_full_account_v1_result.json",
    "exports/e1r_unified_5y_dashboard_research_bundle.json",
    "exports/e1r_combined_5y_original_max3_result.json",
    "exports/e1r_combined_5y_original_max3_equity_curve.json",
    "exports/e1r_combined_5y_original_max3_summary.json",
]

REQUIRED_GOLDEN_MASTER_FIELDS = {
    "daily_account_state": [
        "date",
        "cash",
        "positions_value",
        "total_equity",
        "open_positions_count",
        "market_gate_state",
        "spx_regime",
        "e1r_active_mode",
    ],
    "candidate_trace": [
        "date",
        "symbol",
        "leader_rank",
        "leader_score",
        "rs_score",
        "trend_health",
        "momentum_score",
        "close",
        "ma50",
        "ma50_slope",
        "reasons",
    ],
    "action_trace": [
        "sym",
        "action",
        "signal_date",
        "ls",
        "close_t",
        "entry_rank",
        "strategy",
        "primary_reason",
        "reasons",
    ],
    "position_lifecycle": [
        "symbol",
        "entry_date",
        "exit_date",
        "entry_signal",
        "exit_signal",
        "entry_price",
        "avg_cost",
        "exit_price",
        "return_pct",
        "holding_days",
        "leader_score_entry",
        "actions_during_trade",
        "entry_regime",
        "exit_regime",
        "entry_type",
        "exit_type",
    ],
    "pending_order_trace": [
        "sym",
        "action",
        "signal_date",
        "entry_rank",
        "target_size_units",
        "add_size_units",
    ],
}

EQUIVALENCE_ACCEPTANCE_RULES = {
    "buy_actions": "100% match on symbol, signal_date, action, entry_rank, e1r_entry_type, primary_reason.",
    "exit_actions": "100% match on symbol, signal_date or exit_signal convention, action, exit_type/reasons.",
    "add_reduce_hold_actions": "100% match where the baseline emits explicit action records.",
    "candidate_ranking": "Top-N candidate ordering must match exactly for date/symbol/rank; score values must match within float tolerance.",
    "market_gate": "market_gate_state and risk/e1r active mode must match exactly by date.",
    "account_state": "cash, positions_value, total_equity must match within tolerance; open_positions_count must match exactly and stay <= 3.",
    "position_lifecycle": "entry/exit symbol/date/price/holding_days/action history must match exactly or within explicit execution-price tolerance.",
}

FLOAT_TOLERANCE = 1e-9

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

def read_text(path: Path) -> str:
    return path.read_text(errors="replace")

def read_json(path: Path) -> Any:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def get_function(path: Path, name: str) -> dict[str, Any] | None:
    if not path.exists():
        return None

    text = read_text(path)
    lines = text.splitlines()

    try:
        tree = ast.parse(text)
    except Exception:
        return None

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            start = node.lineno
            end = getattr(node, "end_lineno", start)
            source = "\n".join(lines[start - 1:end])
            return {
                "path": rel(path),
                "name": name,
                "start_line": start,
                "end_line": end,
                "line_count": end - start + 1,
                "args": [a.arg for a in node.args.args],
                "source": source,
                "lines": lines,
            }

    return None

def extract_dict_literals(fn: dict[str, Any] | None) -> list[dict[str, Any]]:
    if fn is None:
        return []

    try:
        tree = ast.parse(fn["source"])
    except Exception:
        return []

    out = []
    start_line = fn["start_line"]

    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue

        keys = []
        literal_values = {}

        for k, v in zip(node.keys, node.values):
            if isinstance(k, ast.Constant) and isinstance(k.value, str):
                key = k.value
                keys.append(key)
                try:
                    literal_values[key] = ast.literal_eval(v)
                except Exception:
                    literal_values[key] = None

        if not keys:
            continue

        out.append({
            "line": start_line + getattr(node, "lineno", 1) - 1,
            "keys": keys,
            "literal_action": literal_values.get("action"),
            "literal_event": literal_values.get("event"),
            "literal_event_type": literal_values.get("event_type"),
        })

    return out

def classify_dict_literal(d: dict[str, Any]) -> str:
    keys = set(d["keys"])

    if {"date", "cash", "positions_value", "total_equity", "open_positions_count"}.issubset(keys):
        return "daily_account_state"

    if {"date", "symbol", "leader_rank", "leader_score", "rs_score", "trend_health"}.issubset(keys):
        return "candidate_trace"

    if {"sym", "action", "signal_date", "ls", "close_t", "entry_rank", "strategy"}.issubset(keys):
        return "action_trace"

    if {"symbol", "entry_date", "exit_date", "entry_signal", "exit_signal", "entry_price", "exit_price"}.issubset(keys):
        return "position_lifecycle"

    if {"shares", "avg_cost", "size_units", "entry_date", "entry_signal", "leader_score_entry"}.issubset(keys):
        return "position_state_internal"

    if "action" in keys and ("sym" in keys or "symbol" in keys):
        return "generic_action_record"

    if {"date", "cash", "position_value", "total_equity", "n_holdings"}.issubset(keys):
        return "legacy_or_summary_account_state"

    return "other"

def audit_current_trace_capability() -> dict[str, Any]:
    fn = get_function(BACKTEST_PATH, "run_stateful_simulation")
    dicts = extract_dict_literals(fn)

    classified = []
    counts = Counter()

    for d in dicts:
        cls = classify_dict_literal(d)
        counts[cls] += 1
        classified.append({
            **d,
            "classification": cls,
        })

    available_keys_by_group: dict[str, set[str]] = {}
    sample_by_group: dict[str, list[dict[str, Any]]] = {}

    for item in classified:
        cls = item["classification"]
        available_keys_by_group.setdefault(cls, set()).update(item["keys"])
        sample_by_group.setdefault(cls, []).append(item)

    available_keys_by_group_json = {
        k: sorted(v)
        for k, v in available_keys_by_group.items()
    }

    sample_by_group_json = {
        k: v[:20]
        for k, v in sample_by_group.items()
    }

    coverage = {}
    missing = {}

    mapping = {
        "daily_account_state": "daily_account_state",
        "candidate_trace": "candidate_trace",
        "action_trace": "action_trace",
        "position_lifecycle": "position_lifecycle",
        "pending_order_trace": "action_trace",
    }

    for req_group, req_fields in REQUIRED_GOLDEN_MASTER_FIELDS.items():
        source_group = mapping.get(req_group, req_group)
        available = set(available_keys_by_group_json.get(source_group, []))
        req_set = set(req_fields)
        coverage[req_group] = {
            "source_group": source_group,
            "required_count": len(req_fields),
            "available_required_count": len(req_set.intersection(available)),
            "coverage_pct": round(len(req_set.intersection(available)) / len(req_fields), 4) if req_fields else 1.0,
            "available_required_fields": sorted(req_set.intersection(available)),
            "missing_fields": sorted(req_set - available),
        }
        missing[req_group] = sorted(req_set - available)

    enough_for_minimal_golden_master = (
        coverage["daily_account_state"]["coverage_pct"] >= 0.875
        and coverage["candidate_trace"]["coverage_pct"] >= 0.8
        and coverage["action_trace"]["coverage_pct"] >= 0.8
        and coverage["position_lifecycle"]["coverage_pct"] >= 0.75
    )

    return {
        "function": {
            "path": fn["path"] if fn else None,
            "name": fn["name"] if fn else None,
            "start_line": fn["start_line"] if fn else None,
            "end_line": fn["end_line"] if fn else None,
            "line_count": fn["line_count"] if fn else None,
        },
        "dict_literal_count": len(dicts),
        "classified_counts": dict(counts),
        "available_keys_by_group": available_keys_by_group_json,
        "samples_by_group": sample_by_group_json,
        "required_fields": REQUIRED_GOLDEN_MASTER_FIELDS,
        "coverage": coverage,
        "missing": missing,
        "enough_for_minimal_golden_master": enough_for_minimal_golden_master,
    }

def audit_existing_report_outputs() -> dict[str, Any]:
    outputs = {}

    for label, path in {
        "D3": D3_REPORT,
        "D2B": D2B_REPORT,
    }.items():
        if not path.exists():
            outputs[label] = {"exists": False}
            continue

        data = read_json(path)
        outputs[label] = {
            "exists": True,
            "path": rel(path),
            "top_level_keys": sorted(data.keys()),
            "has_baseline": "baseline" in data,
            "has_candidate": "candidate" in data,
            "has_equivalence": "equivalence" in data,
            "has_decision": "decision" in data,
            "decision": data.get("decision"),
        }

    return outputs

def build_golden_master_contract(trace_capability: dict[str, Any]) -> dict[str, Any]:
    return {
        "contract_name": "UPTREND_GOLDEN_MASTER_TRACE_V1",
        "baseline_source": "src/engine/backtest.py::run_stateful_simulation",
        "purpose": "Freeze current validated UPTREND behavior before any provider extraction.",
        "scope": {
            "full_5y": False,
            "short_window_only": True,
            "recommended_windows": [
                {
                    "name": "UPTREND_WITH_BUY_ADD_HOLD_EXIT",
                    "criteria": "A short historical window containing at least one BUY and one EXIT, preferably also ADD/TP_REDUCE if naturally present.",
                },
                {
                    "name": "UPTREND_GATE_TRANSITION",
                    "criteria": "A short window around market gate opening/closing or regime/mode transition.",
                },
            ],
        },
        "trace_units": {
            "daily": REQUIRED_GOLDEN_MASTER_FIELDS["daily_account_state"],
            "candidate": REQUIRED_GOLDEN_MASTER_FIELDS["candidate_trace"],
            "action": REQUIRED_GOLDEN_MASTER_FIELDS["action_trace"],
            "position_lifecycle": REQUIRED_GOLDEN_MASTER_FIELDS["position_lifecycle"],
            "pending_order": REQUIRED_GOLDEN_MASTER_FIELDS["pending_order_trace"],
        },
        "acceptance_rules": EQUIVALENCE_ACCEPTANCE_RULES,
        "float_tolerance": FLOAT_TOLERANCE,
        "hard_fail_conditions": [
            "Any BUY/EXIT symbol-date mismatch.",
            "Any action missing from extracted provider trace.",
            "Any open_positions_count > 3.",
            "Any candidate ranking mismatch not explained by identical score tie handling.",
            "Any sizing/cash mismatch above tolerance.",
            "Any market_gate_state mismatch by date.",
            "Any use of invalid artifacts or stitched result curves.",
        ],
        "current_output_sufficiency": trace_capability["enough_for_minimal_golden_master"],
    }

def build_instrumentation_proposal(trace_capability: dict[str, Any]) -> dict[str, Any]:
    missing = trace_capability["missing"]

    required_additions = []

    for group, fields in missing.items():
        if not fields:
            continue

        required_additions.append({
            "trace_group": group,
            "missing_fields": fields,
            "proposal": "Add these fields to trace/report output only; do not alter signal, order, sizing, or account-state calculations.",
        })

    if not required_additions:
        status = "NO_INSTRUMENTATION_REQUIRED_FOR_MINIMAL_CONTRACT"
    else:
        status = "MINIMAL_NON_STRATEGY_INSTRUMENTATION_PROPOSAL_REQUIRED"

    return {
        "status": status,
        "strategy_logic_change_allowed": False,
        "allowed_change_type": "trace/output instrumentation only",
        "not_allowed": [
            "Do not change ranking formula.",
            "Do not change entry/exit/add/reduce/hold decision logic.",
            "Do not change sizing.",
            "Do not change market gate.",
            "Do not change state transition timing.",
            "Do not change execution convention.",
        ],
        "required_additions": required_additions,
    }

def derive_decision(trace_capability: dict[str, Any], instrumentation: dict[str, Any]) -> dict[str, Any]:
    if trace_capability["enough_for_minimal_golden_master"]:
        conclusion = "GOLDEN_MASTER_TRACE_CONTRACT_READY_FOR_SHORT_WINDOW_BASELINE_EXPORT"
        next_action = (
            "Proceed to 4C-2C-4E-D4B: export a short-window UPTREND golden master trace from current "
            "run_stateful_simulation outputs. No provider extraction yet."
        )
    else:
        conclusion = "GOLDEN_MASTER_TRACE_REQUIRES_MINIMAL_NON_STRATEGY_INSTRUMENTATION_PROPOSAL"
        next_action = (
            "Proceed to 4C-2C-4E-D4B: review and approve minimal trace-only instrumentation before exporting "
            "the golden master. No strategy logic change."
        )

    return {
        "golden_master_contract_defined": True,
        "current_outputs_sufficient_for_minimal_golden_master": trace_capability["enough_for_minimal_golden_master"],
        "instrumentation_required": instrumentation["status"] != "NO_INSTRUMENTATION_REQUIRED_FOR_MINIMAL_CONTRACT",
        "strategy_logic_change_required": False,
        "provider_extraction_allowed_now": False,
        "adapter_implementation_allowed_now": False,
        "conclusion": conclusion,
        "recommended_next_action": next_action,
        "engineering_rule": (
            "Golden master must be established before provider extraction. Any missing trace fields may only be added "
            "as output instrumentation after approval and must not affect ranking, orders, sizing, market gate, or account state."
        ),
    }

def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    trace_capability = audit_current_trace_capability()
    existing_reports = audit_existing_report_outputs()
    contract = build_golden_master_contract(trace_capability)
    instrumentation = build_instrumentation_proposal(trace_capability)
    decision = derive_decision(trace_capability, instrumentation)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "audit_only_no_full_5y": True,
        "backtest_engine_run": False,
        "provider_extraction_run": False,
        "adapter_implementation_run": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "invalid_artifacts_not_used_as_source": True,
        "composer_not_used": True,
        "return_curve_stitching_not_used": True,
        "run_stateful_source_audited": trace_capability["function"]["name"] == "run_stateful_simulation",
        "golden_master_contract_defined": contract["contract_name"] == "UPTREND_GOLDEN_MASTER_TRACE_V1",
        "acceptance_rules_defined": bool(contract["acceptance_rules"]),
        "instrumentation_proposal_generated": bool(instrumentation),
        "strategy_logic_change_required_false": decision["strategy_logic_change_required"] is False,
        "provider_extraction_not_allowed_yet": decision["provider_extraction_allowed_now"] is False,
        "adapter_implementation_not_allowed_yet": decision["adapter_implementation_allowed_now"] is False,
        "decision_generated": bool(decision["conclusion"]),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-D4A",
        "status": "UPTREND_GOLDEN_MASTER_TRACE_CONTRACT_COMPLETE",
        "purpose": "Define the UPTREND golden master trace contract before any no-strategy-change provider extraction.",
        "policy": {
            "strategy_logic_changed": False,
            "backtest_engine_run": False,
            "full_5y_backtest_run": False,
            "provider_extraction_run": False,
            "adapter_implementation_run": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
            "invalid_artifacts_used_as_source": False,
            "composer_used": False,
            "return_curve_stitching_used": False,
        },
        "trace_capability": trace_capability,
        "existing_reports": existing_reports,
        "golden_master_contract": contract,
        "minimal_non_strategy_instrumentation_proposal": instrumentation,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-D4A — UPTREND Golden Master Trace Contract")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("Define the UPTREND golden master trace contract before any no-strategy-change provider extraction.")
    md.append("")
    md.append("## Policy")
    md.append("```json")
    md.append(json.dumps(report["policy"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Trace Capability Summary")
    md.append("```json")
    md.append(json.dumps({
        "function": trace_capability["function"],
        "classified_counts": trace_capability["classified_counts"],
        "coverage": trace_capability["coverage"],
        "enough_for_minimal_golden_master": trace_capability["enough_for_minimal_golden_master"],
    }, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Golden Master Contract")
    md.append("```json")
    md.append(json.dumps(contract, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Minimal Non-Strategy Instrumentation Proposal")
    md.append("```json")
    md.append(json.dumps(instrumentation, indent=2, ensure_ascii=False))
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
    md.append("## Next Action")
    md.append("")
    md.append(decision["recommended_next_action"])
    md.append("")

    REPORT_MD.write_text("\n".join(md))

    print("E1R_4C2C4E_D4A_UPTREND_GOLDEN_MASTER_TRACE_CONTRACT_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("trace_capability_summary:", json.dumps({
        "function": trace_capability["function"],
        "classified_counts": trace_capability["classified_counts"],
        "coverage": trace_capability["coverage"],
        "enough_for_minimal_golden_master": trace_capability["enough_for_minimal_golden_master"],
    }, ensure_ascii=False))
    print("golden_master_contract_summary:", json.dumps({
        "contract_name": contract["contract_name"],
        "baseline_source": contract["baseline_source"],
        "current_output_sufficiency": contract["current_output_sufficiency"],
        "hard_fail_conditions": contract["hard_fail_conditions"],
    }, ensure_ascii=False))
    print("instrumentation_proposal:", json.dumps(instrumentation, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
