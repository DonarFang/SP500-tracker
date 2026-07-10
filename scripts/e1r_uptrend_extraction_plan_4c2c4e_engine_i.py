#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
import inspect
import ast
import re
import sys
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_I_UPTREND_EXTRACTION_PLAN.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_I_UPTREND_EXTRACTION_PLAN.md"
ARCH_MD = ROOT / "docs/architecture/E1R_UPTREND_EXTRACTION_PLAN.md"
PLAN_JSON = ROOT / "exports/e1r_engine/audit/e1r_engine_i_uptrend_extraction_plan.json"

ENGINE_A_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_A_STANDALONE_ENGINE_ARCHITECTURE_CONTRACT.json"
ENGINE_B_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_B_R1_NORMALIZED_INPUT_DATA_ADAPTER_CONTRACT_AUDIT.json"
ENGINE_C_R1_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_C_R1_NO_STRATEGY_DATA_HARNESS_SMOKE.json"
ENGINE_D_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_D_HISTORICAL_DATA_ADAPTER_SKELETON_SMOKE.json"
ENGINE_E_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_E_STATE_CONTRACT_SMOKE.json"
ENGINE_F_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_F_CORE_ENGINE_SHELL_SMOKE.json"
ENGINE_G_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_G_GOLDEN_MASTER_HARNESS.json"
ENGINE_H_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_H_GOLDEN_MASTER_TRACE_SHAPE_AUDIT.json"
ASSERTIONS_JSON = ROOT / "exports/e1r_engine/audit/e1r_engine_h_equivalence_assertions.json"

BACKTEST_PATH = ROOT / "src/engine/backtest.py"
SIDECAR_PATH = ROOT / "src/engine/e1r_sidecar_sleeve.py"
COMPOSER_PATH = ROOT / "src/engine/e1r_composer.py"

FROZEN_STRATEGY_FILES = [
    BACKTEST_PATH,
    SIDECAR_PATH,
    COMPOSER_PATH,
]

TARGET_MODULES = [
    "src/e1r_engine/uptrend_core.py",
    "src/e1r_engine/equivalence.py",
]

KEYWORD_GROUPS = {
    "candidate_generation": [
        "leader_score",
        "leader_rank",
        "rank",
        "rs_score",
        "trend_health",
        "candidate",
        "top_n",
        "entry_top_n",
    ],
    "entry_buy": [
        "BUY",
        "buy_size",
        "target_size",
        "entry_signal",
        "entry_type",
        "pending_orders",
    ],
    "add_reduce_exit": [
        "ADD",
        "REDUCE",
        "EXIT",
        "leader_score_below",
        "broken_trend",
        "exit_signal",
        "exit_type",
    ],
    "market_gate": [
        "market_gate",
        "market_entry_gate",
        "SPX",
        "MA50",
        "shock",
        "risk_off",
    ],
    "account_state": [
        "cash",
        "positions",
        "total_equity",
        "positions_value",
        "open_positions_count",
        "n_holdings",
        "max_positions",
    ],
    "daily_trace": [
        "daily_equity_records",
        "daily_records",
        "trades",
        "actions_during_trade",
        "pending_orders_count",
    ],
}


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


def find_function_node(source: str, function_name: str) -> ast.FunctionDef | None:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return node
    return None


def line_window(lines: list[str], lineno: int, radius: int = 4) -> dict[str, Any]:
    start = max(1, lineno - radius)
    end = min(len(lines), lineno + radius)
    return {
        "start": start,
        "end": end,
        "text": [
            {"line": i, "text": lines[i - 1].rstrip()}
            for i in range(start, end + 1)
        ],
    }


def keyword_contexts(source: str, keywords: list[str], max_hits: int = 20) -> list[dict[str, Any]]:
    lines = source.splitlines()
    out: list[dict[str, Any]] = []

    for i, line in enumerate(lines, start=1):
        lowered = line.lower()
        matched = [kw for kw in keywords if kw.lower() in lowered]
        if matched:
            out.append({
                "line": i,
                "matched": matched,
                "context": line_window(lines, i, radius=3),
            })
            if len(out) >= max_hits:
                break

    return out


def extract_function_source(source: str, node: ast.FunctionDef) -> dict[str, Any]:
    lines = source.splitlines()
    start = node.lineno
    end = getattr(node, "end_lineno", start)
    return {
        "name": node.name,
        "start_line": start,
        "end_line": end,
        "line_count": end - start + 1,
        "source_sha256": hashlib.sha256("\n".join(lines[start - 1:end]).encode()).hexdigest(),
    }


def static_feature_scan(source: str) -> dict[str, Any]:
    features: dict[str, Any] = {}

    for group, keywords in KEYWORD_GROUPS.items():
        contexts = keyword_contexts(source, keywords, max_hits=25)
        features[group] = {
            "keyword_count": len(contexts),
            "keywords": keywords,
            "contexts": contexts,
            "present": len(contexts) > 0,
        }

    literal_counts = {}
    for literal in ["BUY", "ADD", "REDUCE", "EXIT", "HOLD", "TP_REDUCE", "SIM_END"]:
        literal_counts[literal] = len(re.findall(rf'["\\\']{re.escape(literal)}["\\\']', source))

    features["literal_action_counts"] = literal_counts
    features["has_daily_equity_records"] = "daily_equity_records" in source
    features["has_daily_records"] = "daily_records" in source
    features["has_trades"] = "trades" in source
    features["has_pending_orders"] = "pending_orders" in source
    features["has_max_positions"] = "max_positions" in source
    features["has_market_gate_state"] = "market_gate_state" in source

    return features


def import_backtest_signature() -> str:
    from src.engine.backtest import run_stateful_simulation
    return str(inspect.signature(run_stateful_simulation))


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    prereq_paths = [
        ENGINE_A_REPORT,
        ENGINE_B_REPORT,
        ENGINE_C_R1_REPORT,
        ENGINE_D_REPORT,
        ENGINE_E_REPORT,
        ENGINE_F_REPORT,
        ENGINE_G_REPORT,
        ENGINE_H_REPORT,
        ASSERTIONS_JSON,
    ]

    for p in prereq_paths:
        if not p.exists():
            raise FileNotFoundError(f"Missing prerequisite file: {rel(p)}")

    engine_g = read_json(ENGINE_G_REPORT)
    engine_h = read_json(ENGINE_H_REPORT)
    assertions = read_json(ASSERTIONS_JSON)

    if engine_g.get("decision", {}).get("golden_master_harness_passed") is not True:
        raise RuntimeError("ENGINE-G did not pass.")
    if engine_h.get("decision", {}).get("trace_shape_audit_passed") is not True:
        raise RuntimeError("ENGINE-H did not pass.")
    if engine_h.get("decision", {}).get("minimum_equivalence_available") is not True:
        raise RuntimeError("Minimum equivalence is not available.")

    source = BACKTEST_PATH.read_text()
    fn_node = find_function_node(source, "run_stateful_simulation")
    if fn_node is None:
        raise RuntimeError("run_stateful_simulation not found.")

    function_info = extract_function_source(source, fn_node)
    fn_source = "\n".join(source.splitlines()[function_info["start_line"] - 1:function_info["end_line"]])
    static_features = static_feature_scan(fn_source)
    signature = import_backtest_signature()

    hard_assertions = engine_h.get("decision", {}).get("hard_required_assertions", [])
    missing_or_partial = engine_h.get("decision", {}).get("missing_or_partial_assertions", [])
    extraction_minimum = engine_h.get("extraction_minimum", {})

    extraction_boundaries = {
        "source_of_truth": {
            "legacy_function": "src.engine.backtest.run_stateful_simulation",
            "function_info": function_info,
            "signature": signature,
            "strategy_file_hash_before": before_hashes.get(rel(BACKTEST_PATH)),
        },
        "target_modules": {
            "uptrend_core": "src/e1r_engine/uptrend_core.py",
            "equivalence": "src/e1r_engine/equivalence.py",
            "existing_core_shell": "src/e1r_engine/core.py",
            "existing_state_contract": "src/e1r_engine/state.py",
            "existing_data_adapter": "src/e1r_engine/adapters/historical_data.py",
        },
        "allowed_in_engine_j": [
            "Create UptrendCore class/function skeleton with copied-equivalent data contracts.",
            "Implement minimal UPTREND branch extraction only if it can be compared against ENGINE-H T0/T1 assertions.",
            "Create equivalence checker comparing new engine output to ENGINE-G golden master.",
            "Run only the same short-window golden-master window.",
            "Modify only new src/e1r_engine/* modules and new scripts/docs/exports artifacts.",
        ],
        "not_allowed_in_engine_j": [
            "Do not change src/engine/backtest.py strategy logic.",
            "Do not modify entry/exit/sizing/ranking/market gate rules by interpretation.",
            "Do not implement SIDEWAYS_MA_CONFLICT branch.",
            "Do not implement DOWNTREND / defensive branch beyond shell routing.",
            "Do not run full 5Y backtest.",
            "Do not generate official result/dashboard output.",
            "Do not use invalid artifacts as source.",
        ],
    }

    extraction_units = [
        {
            "unit": "market_gate_state",
            "legacy_evidence_group": "market_gate",
            "target": "uptrend_core should preserve legacy market gate state exactly",
            "equivalence_assertions": ["daily_market_gate_state"],
            "implementation_order": 1,
            "risk": "High — gate drift changes all downstream orders.",
        },
        {
            "unit": "daily_account_mark_to_market",
            "legacy_evidence_group": "account_state",
            "target": "account cash/equity/positions_value/open_positions_count must match golden master",
            "equivalence_assertions": [
                "daily_total_equity_cash_positions",
                "daily_open_positions_count",
                "daily_account_date_sequence",
            ],
            "implementation_order": 2,
            "risk": "High — accounting drift invalidates backtest equivalence.",
        },
        {
            "unit": "candidate_generation_and_rank",
            "legacy_evidence_group": "candidate_generation",
            "target": "candidate scoring/ranking must be extracted without interpretation",
            "equivalence_assertions": ["candidate_ranking_trace"],
            "implementation_order": 3,
            "risk": "Very high — current ENGINE-G short window lacks candidate trace, so first extraction can only be indirectly verified.",
        },
        {
            "unit": "entry_buy_logic",
            "legacy_evidence_group": "entry_buy",
            "target": "BUY symbol/date/entry price must match trade lifecycle where available",
            "equivalence_assertions": ["trade_lifecycle_symbol_dates", "trade_signals_and_reasons"],
            "implementation_order": 4,
            "risk": "High — depends on candidate generation, market gate, cash, capacity.",
        },
        {
            "unit": "hold_add_reduce_exit_logic",
            "legacy_evidence_group": "add_reduce_exit",
            "target": "ADD/REDUCE/EXIT transitions must match trade lifecycle and daily account state",
            "equivalence_assertions": ["trade_lifecycle_symbol_dates", "trade_signals_and_reasons"],
            "implementation_order": 5,
            "risk": "High — action trace is currently missing, so daily/trade lifecycle must be first control.",
        },
        {
            "unit": "trace_export",
            "legacy_evidence_group": "daily_trace",
            "target": "new engine must export daily equity records and trade lifecycle in a comparable schema",
            "equivalence_assertions": hard_assertions,
            "implementation_order": 6,
            "risk": "Medium — trace schema must be stable before tightening equivalence.",
        },
    ]

    equivalence_plan = {
        "locked_assertions_source": rel(ASSERTIONS_JSON),
        "t0_t1_hard_required_assertions": hard_assertions,
        "minimum_extraction_assertions": extraction_minimum.get("minimum_assertions", []),
        "known_trace_gaps": extraction_minimum.get("known_limits", []),
        "tolerances": {
            "date_sequence": "exact",
            "cash": "abs <= 0.01 or relative <= 1e-6",
            "positions_value": "abs <= 0.01 or relative <= 1e-6",
            "total_equity": "abs <= 0.01 or relative <= 1e-6",
            "open_positions_count": "exact integer and <= 3",
            "market_gate_state": "exact string",
            "spx_regime": "exact string",
            "trade_symbol_dates": "symbol/date exact",
            "trade_prices": "abs <= 0.01",
            "trade_return_pct": "abs <= 0.01 percentage points",
        },
        "engine_j_acceptance": {
            "must_pass": [
                "new engine runs same 2021-04-05..2021-06-30 window",
                "no frozen strategy files changed",
                "no full 5Y run",
                "no official result/dashboard",
                "T0 assertions pass",
                "T1 trade lifecycle assertions pass or report exact mismatch list",
                "max open positions <= 3 every day",
            ],
            "allowed_initial_mismatch": [
                "candidate_ranking_trace because source golden master has e1r_candidates=0",
                "standalone action_trace because source golden master lacks action_trace_candidates",
                "daily_position_snapshot because source golden master lacks per-day symbol snapshots",
            ],
            "hard_fail": [
                "date sequence mismatch",
                "cash/equity mismatch above tolerance",
                "open_positions_count > 3",
                "market_gate_state mismatch",
                "trade symbol/date mismatch without documented trace gap",
                "any change to src/engine/backtest.py strategy logic",
            ],
        },
    }

    implementation_sequence = [
        {
            "stage": "ENGINE-J",
            "name": "UPTREND extraction skeleton + equivalence checker",
            "scope": "Create uptrend_core.py and equivalence.py; run same short window; compare T0/T1; no full 5Y.",
            "strategy_logic_change": "New engine module only; frozen legacy files unchanged.",
        },
        {
            "stage": "ENGINE-K",
            "name": "UPTREND equivalence tightening",
            "scope": "Resolve mismatches against T0/T1 assertions; optionally add trace instrumentation only after approval.",
            "strategy_logic_change": "No rule interpretation changes without explicit approval.",
        },
        {
            "stage": "ENGINE-L",
            "name": "SIDEWAYS_MA_CONFLICT integration plan",
            "scope": "After UPTREND equivalence, integrate sidecar candidate branch under max3 account.",
            "strategy_logic_change": "Separate approval required.",
        },
    ]

    plan = {
        "schema": "E1RUptrendExtractionPlanV1",
        "generated_at": now(),
        "stage": "4C-2C-4E-ENGINE-I",
        "purpose": "Define UPTREND extraction plan against locked ENGINE-H equivalence assertions without implementing extracted strategy code.",
        "source": extraction_boundaries["source_of_truth"],
        "extraction_boundaries": extraction_boundaries,
        "static_feature_scan": static_features,
        "extraction_units": extraction_units,
        "equivalence_plan": equivalence_plan,
        "implementation_sequence": implementation_sequence,
        "missing_or_partial_assertions": missing_or_partial,
        "decision_gate": {
            "engine_j_allowed_next": True,
            "engine_j_must_not_modify_frozen_strategy_files": True,
            "engine_j_must_not_run_full_5y": True,
            "engine_j_must_compare_against_engine_g_golden_master": True,
            "engine_j_must_use_engine_h_assertions": True,
        },
    }
    write_json(PLAN_JSON, plan)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "uptrend_extraction_plan_defined": True,
        "plan_only": True,
        "strategy_logic_changed": False,
        "backtest_engine_run": False,
        "full_5y_backtest_run": False,
        "forward_runner_run": False,
        "provider_extraction_run": False,
        "strategy_core_implemented": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "invalid_artifacts_not_used_as_source": True,
        "composer_not_used": True,
        "return_curve_stitching_used": False,
        "engine_g_loaded": True,
        "engine_h_loaded": True,
        "equivalence_assertions_loaded": True,
        "run_stateful_simulation_located": function_info["line_count"] > 0,
        "static_feature_scan_completed": all(v["present"] for k, v in static_features.items() if isinstance(v, dict) and "present" in v),
        "extraction_boundaries_defined": True,
        "extraction_units_defined": len(extraction_units) >= 5,
        "equivalence_plan_defined": True,
        "engine_j_acceptance_defined": True,
        "plan_artifact_written": PLAN_JSON.exists(),
        "strategy_core_extraction_not_run": True,
    }

    decision = {
        "uptrend_extraction_plan_passed": all([
            validations["strategy_files_unchanged"],
            validations["run_stateful_simulation_located"],
            validations["extraction_boundaries_defined"],
            validations["extraction_units_defined"],
            validations["equivalence_plan_defined"],
            validations["engine_j_acceptance_defined"],
            validations["plan_artifact_written"],
        ]),
        "next_stage_allowed": "4C-2C-4E-ENGINE-J",
        "engine_j_scope": "UPTREND extraction skeleton + equivalence checker against ENGINE-G/H",
        "strategy_core_extraction_allowed_now": False,
        "uptrend_provider_extraction_allowed_after_user_approval": True,
        "sideways_branch_implementation_allowed_now": False,
        "full_5y_backtest_allowed_now": False,
        "forward_runner_allowed_now": False,
        "conclusion": (
            "UPTREND_EXTRACTION_PLAN_PASS_READY_FOR_ENGINE_J_IMPLEMENTATION"
            if all([
                validations["strategy_files_unchanged"],
                validations["run_stateful_simulation_located"],
                validations["equivalence_plan_defined"],
            ])
            else "UPTREND_EXTRACTION_PLAN_NEEDS_REVIEW"
        ),
        "recommended_next_action": (
            "Proceed to 4C-2C-4E-ENGINE-J: implement UPTREND extraction skeleton and equivalence checker. "
            "This next step may create new strategy-core code under src/e1r_engine, but must not modify legacy strategy files."
        ),
        "engineering_rule": (
            "ENGINE-J must be equivalence-first. Any mismatch must be reported before continuing. "
            "Do not tune, reinterpret, or improve trading rules during extraction."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-I",
        "status": "UPTREND_EXTRACTION_PLAN_COMPLETE",
        "purpose": plan["purpose"],
        "policy": {
            "strategy_logic_changed": False,
            "plan_only": True,
            "backtest_engine_run": False,
            "full_5y_backtest_run": False,
            "forward_runner_run": False,
            "provider_extraction_run": False,
            "strategy_core_implemented": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
            "invalid_artifacts_used_as_source": False,
            "composer_used": False,
            "return_curve_stitching_used": False,
        },
        "source_function": function_info,
        "signature": signature,
        "static_feature_scan_summary": {
            group: {
                "present": data.get("present"),
                "keyword_count": data.get("keyword_count"),
                "keywords": data.get("keywords"),
            }
            for group, data in static_features.items()
            if isinstance(data, dict) and "present" in data
        },
        "literal_action_counts": static_features["literal_action_counts"],
        "extraction_units": extraction_units,
        "equivalence_plan": equivalence_plan,
        "implementation_sequence": implementation_sequence,
        "plan_path": rel(PLAN_JSON),
        "plan_sha256": sha256(PLAN_JSON),
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-I — UPTREND Extraction Plan")
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
    md.append("## Source Function")
    md.append("```json")
    md.append(json.dumps(report["source_function"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Static Feature Scan Summary")
    md.append("```json")
    md.append(json.dumps(report["static_feature_scan_summary"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Literal Action Counts")
    md.append("```json")
    md.append(json.dumps(report["literal_action_counts"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Extraction Units")
    md.append("```json")
    md.append(json.dumps(extraction_units, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Equivalence Plan")
    md.append("```json")
    md.append(json.dumps(equivalence_plan, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Implementation Sequence")
    md.append("```json")
    md.append(json.dumps(implementation_sequence, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Plan Artifact")
    md.append(f"- Path: `{report['plan_path']}`")
    md.append(f"- SHA256: `{report['plan_sha256']}`")
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

    print("E1R_4C2C4E_ENGINE_I_UPTREND_EXTRACTION_PLAN_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("source_function:", json.dumps(function_info, ensure_ascii=False))
    print("signature:", signature)
    print("static_feature_scan_summary:", json.dumps(report["static_feature_scan_summary"], ensure_ascii=False))
    print("literal_action_counts:", json.dumps(report["literal_action_counts"], ensure_ascii=False))
    print("extraction_units:", json.dumps(extraction_units, ensure_ascii=False))
    print("equivalence_plan:", json.dumps(equivalence_plan, ensure_ascii=False))
    print("implementation_sequence:", json.dumps(implementation_sequence, ensure_ascii=False))
    print("plan:", json.dumps({
        "path": report["plan_path"],
        "sha256": report["plan_sha256"],
    }, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(PLAN_JSON))


if __name__ == "__main__":
    main()
