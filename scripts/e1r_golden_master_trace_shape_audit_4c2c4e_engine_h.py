#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_H_GOLDEN_MASTER_TRACE_SHAPE_AUDIT.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_H_GOLDEN_MASTER_TRACE_SHAPE_AUDIT.md"
ARCH_MD = ROOT / "docs/architecture/E1R_GOLDEN_MASTER_EQUIVALENCE_ASSERTIONS_CONTRACT.md"
ASSERTIONS_JSON = ROOT / "exports/e1r_engine/audit/e1r_engine_h_equivalence_assertions.json"

ENGINE_A_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_A_STANDALONE_ENGINE_ARCHITECTURE_CONTRACT.json"
ENGINE_B_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_B_R1_NORMALIZED_INPUT_DATA_ADAPTER_CONTRACT_AUDIT.json"
ENGINE_C_R1_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_C_R1_NO_STRATEGY_DATA_HARNESS_SMOKE.json"
ENGINE_D_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_D_HISTORICAL_DATA_ADAPTER_SKELETON_SMOKE.json"
ENGINE_E_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_E_STATE_CONTRACT_SMOKE.json"
ENGINE_F_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_F_CORE_ENGINE_SHELL_SMOKE.json"
ENGINE_G_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_G_GOLDEN_MASTER_HARNESS.json"
GOLDEN_MASTER_JSON = ROOT / "exports/e1r_engine/golden_master/e1r_engine_g_short_window_golden_master.json"

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


def list_fields(rows: Any) -> list[str]:
    if isinstance(rows, list) and rows and isinstance(rows[0], dict):
        return sorted(rows[0].keys())
    return []


def sample_rows(rows: Any, n: int = 3) -> list[Any]:
    if isinstance(rows, list):
        return rows[:n]
    return []


def has_fields(rows: Any, required: list[str]) -> dict[str, Any]:
    fields = set(list_fields(rows))
    missing = [f for f in required if f not in fields]
    return {
        "ok": len(missing) == 0,
        "required": required,
        "available": sorted(fields),
        "missing": missing,
        "coverage": (len(required) - len(missing)) / len(required) if required else 1.0,
    }


def inspect_actions_during_trade(trades: list[dict[str, Any]]) -> dict[str, Any]:
    action_rows = []
    action_shapes = {}

    for trade in trades:
        actions = trade.get("actions_during_trade")
        if isinstance(actions, list):
            for action in actions:
                if isinstance(action, dict):
                    action_rows.append(action)
                    key = tuple(sorted(action.keys()))
                    action_shapes[str(key)] = action_shapes.get(str(key), 0) + 1

    return {
        "actions_during_trade_available": len(action_rows) > 0,
        "action_row_count": len(action_rows),
        "action_shape_count": len(action_shapes),
        "action_shapes": action_shapes,
        "action_sample": action_rows[:10],
        "action_fields": sorted(set().union(*[set(a.keys()) for a in action_rows])) if action_rows else [],
    }


def assertion_item(
    name: str,
    tier: str,
    status: str,
    fields: list[str],
    source_section: str,
    tolerance: str,
    hard_fail: bool,
    notes: str,
) -> dict[str, Any]:
    return {
        "name": name,
        "tier": tier,
        "status": status,
        "fields": fields,
        "source_section": source_section,
        "tolerance": tolerance,
        "hard_fail": hard_fail,
        "notes": notes,
    }


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
        GOLDEN_MASTER_JSON,
    ]

    for p in prereq_paths:
        if not p.exists():
            raise FileNotFoundError(f"Missing prerequisite file: {rel(p)}")

    engine_g = read_json(ENGINE_G_REPORT)
    if engine_g.get("decision", {}).get("golden_master_harness_passed") is not True:
        raise RuntimeError("ENGINE-G did not pass. ENGINE-H trace audit is not allowed.")

    gm = read_json(GOLDEN_MASTER_JSON)
    raw = gm.get("raw_result", {})
    if not isinstance(raw, dict):
        raise RuntimeError("Golden master raw_result is not a dict.")

    daily_equity_records = raw.get("daily_equity_records", [])
    daily_records = raw.get("daily_records", [])
    trades = raw.get("trades", [])
    equity_curve = raw.get("equity_curve", [])
    e1r_candidates = raw.get("e1r_candidates", [])
    invalid_trades = raw.get("invalid_trades", [])

    daily_equity_required = [
        "date",
        "cash",
        "total_equity",
        "positions_value",
        "open_positions_count",
        "market_gate_state",
        "spx_regime",
    ]

    daily_extended = [
        "daily_return_pct",
        "drawdown_pct",
        "exposure_pct",
        "pending_orders_count",
        "risk_budget",
        "risk_budget_mode",
        "spx_close",
        "spx_day_return_pct",
        "spx_ma50",
    ]

    trade_required = [
        "symbol",
        "entry_date",
        "entry_price",
        "exit_date",
        "exit_price",
        "entry_regime",
        "exit_regime",
        "entry_signal",
        "exit_signal",
        "return_pct",
        "holding_days",
        "actions_during_trade",
    ]

    candidate_required = [
        "date",
        "symbol",
        "leader_score",
        "leader_rank",
        "rs_score",
        "trend_health",
    ]

    daily_equity_audit = has_fields(daily_equity_records, daily_equity_required)
    daily_extended_audit = has_fields(daily_equity_records, daily_extended)
    trade_audit = has_fields(trades, trade_required)
    candidate_audit = has_fields(e1r_candidates, candidate_required)
    action_during_trade_audit = inspect_actions_during_trade(trades if isinstance(trades, list) else [])

    row_counts = {
        "daily_equity_records": len(daily_equity_records) if isinstance(daily_equity_records, list) else 0,
        "daily_records": len(daily_records) if isinstance(daily_records, list) else 0,
        "trades": len(trades) if isinstance(trades, list) else 0,
        "equity_curve": len(equity_curve) if isinstance(equity_curve, list) else 0,
        "e1r_candidates": len(e1r_candidates) if isinstance(e1r_candidates, list) else 0,
        "invalid_trades": len(invalid_trades) if isinstance(invalid_trades, list) else 0,
    }

    trace_shape = {
        "raw_result_keys": sorted(raw.keys()),
        "row_counts": row_counts,
        "daily_equity_records": {
            "fields": list_fields(daily_equity_records),
            "sample": sample_rows(daily_equity_records, 3),
            "required_audit": daily_equity_audit,
            "extended_audit": daily_extended_audit,
        },
        "daily_records": {
            "fields": list_fields(daily_records),
            "sample": sample_rows(daily_records, 3),
        },
        "trades": {
            "fields": list_fields(trades),
            "sample": sample_rows(trades, 3),
            "required_audit": trade_audit,
            "actions_during_trade_audit": action_during_trade_audit,
        },
        "equity_curve": {
            "type": type(equity_curve).__name__,
            "sample": sample_rows(equity_curve, 5),
        },
        "e1r_candidates": {
            "fields": list_fields(e1r_candidates),
            "sample": sample_rows(e1r_candidates, 3),
            "required_audit": candidate_audit,
        },
    }

    equivalence_assertions = [
        assertion_item(
            name="daily_account_date_sequence",
            tier="T0_REQUIRED",
            status="ASSERTABLE",
            fields=["daily_equity_records.date"],
            source_section="raw_result.daily_equity_records",
            tolerance="exact sequence match",
            hard_fail=True,
            notes="New engine must generate the same daily dates for the same short-window baseline.",
        ),
        assertion_item(
            name="daily_total_equity_cash_positions",
            tier="T0_REQUIRED",
            status="ASSERTABLE",
            fields=[
                "daily_equity_records.cash",
                "daily_equity_records.positions_value",
                "daily_equity_records.total_equity",
            ],
            source_section="raw_result.daily_equity_records",
            tolerance="absolute <= 0.01 or relative <= 1e-6",
            hard_fail=True,
            notes="Accounting identity and daily equity must match after extraction.",
        ),
        assertion_item(
            name="daily_open_positions_count",
            tier="T0_REQUIRED",
            status="ASSERTABLE",
            fields=["daily_equity_records.open_positions_count"],
            source_section="raw_result.daily_equity_records",
            tolerance="exact integer match; always <= 3",
            hard_fail=True,
            notes="Max3 account contract must be preserved.",
        ),
        assertion_item(
            name="daily_market_gate_state",
            tier="T0_REQUIRED",
            status="ASSERTABLE",
            fields=["daily_equity_records.market_gate_state"],
            source_section="raw_result.daily_equity_records",
            tolerance="exact string match",
            hard_fail=True,
            notes="Market gate behavior must not drift during extraction.",
        ),
        assertion_item(
            name="daily_spx_regime",
            tier="T0_REQUIRED",
            status="ASSERTABLE",
            fields=["daily_equity_records.spx_regime"],
            source_section="raw_result.daily_equity_records",
            tolerance="exact string match",
            hard_fail=True,
            notes="Regime attribution must remain aligned.",
        ),
        assertion_item(
            name="trade_lifecycle_symbol_dates",
            tier="T1_REQUIRED",
            status="ASSERTABLE" if trade_audit["ok"] else "PARTIAL",
            fields=[
                "trades.symbol",
                "trades.entry_date",
                "trades.exit_date",
                "trades.entry_price",
                "trades.exit_price",
            ],
            source_section="raw_result.trades",
            tolerance="symbol/date exact; price absolute <= 0.01",
            hard_fail=True,
            notes="Trade lifecycle must match after extraction.",
        ),
        assertion_item(
            name="trade_signals_and_reasons",
            tier="T1_REQUIRED",
            status="ASSERTABLE" if trade_audit["ok"] else "PARTIAL",
            fields=[
                "trades.entry_signal",
                "trades.exit_signal",
                "trades.entry_regime",
                "trades.exit_regime",
            ],
            source_section="raw_result.trades",
            tolerance="exact match where available",
            hard_fail=True,
            notes="Entry/exit reasons are available at trade level.",
        ),
        assertion_item(
            name="actions_during_trade",
            tier="T2_PARTIAL",
            status="PARTIAL" if action_during_trade_audit["actions_during_trade_available"] else "MISSING",
            fields=["trades.actions_during_trade"],
            source_section="raw_result.trades[].actions_during_trade",
            tolerance="exact if action rows are sufficiently structured",
            hard_fail=False,
            notes="Current golden master has no standalone action_trace section; only nested actions_during_trade may be available.",
        ),
        assertion_item(
            name="daily_position_snapshot",
            tier="T2_PARTIAL",
            status="MISSING",
            fields=["per_day.positions_by_symbol"],
            source_section="not available",
            tolerance="not assertable until trace instrumentation exists",
            hard_fail=False,
            notes="Need trace instrumentation for strict per-symbol daily position equivalence.",
        ),
        assertion_item(
            name="candidate_ranking_trace",
            tier="T3_OPTIONAL_FOR_EXTRACTION_BUT_REQUIRED_FOR_DEEP_AUDIT",
            status="ASSERTABLE" if candidate_audit["ok"] and row_counts["e1r_candidates"] > 0 else "MISSING",
            fields=candidate_required,
            source_section="raw_result.e1r_candidates",
            tolerance="exact rank/date/symbol match if available",
            hard_fail=False,
            notes="Current short window has e1r_candidate_count=0, so candidate/rank equivalence is not assertable from this golden master.",
        ),
        assertion_item(
            name="pending_order_trace",
            tier="T3_OPTIONAL_FOR_EXTRACTION_BUT_REQUIRED_FOR_DEEP_AUDIT",
            status="MISSING",
            fields=["pending_order.date", "symbol", "action", "reason", "target_size"],
            source_section="not available as standalone section",
            tolerance="not assertable until trace instrumentation exists",
            hard_fail=False,
            notes="pending_orders_count exists, but standalone pending order rows are absent.",
        ),
    ]

    required_assertable = [
        item for item in equivalence_assertions
        if item["tier"] in {"T0_REQUIRED", "T1_REQUIRED"}
    ]
    required_assertable_ok = all(item["status"] in {"ASSERTABLE", "PARTIAL"} for item in required_assertable)

    instrumentation_gaps = [
        item for item in equivalence_assertions
        if item["status"] == "MISSING"
    ]

    extraction_minimum = {
        "can_start_uptrend_extraction_with_minimum_equivalence": required_assertable_ok
        and daily_equity_audit["ok"]
        and row_counts["daily_equity_records"] > 0
        and row_counts["trades"] > 0,
        "minimum_assertions": [
            "daily_account_date_sequence",
            "daily_total_equity_cash_positions",
            "daily_open_positions_count",
            "daily_market_gate_state",
            "daily_spx_regime",
            "trade_lifecycle_symbol_dates",
            "trade_signals_and_reasons",
        ],
        "known_limits": [
            "No standalone action_trace section.",
            "No daily per-symbol position snapshot section.",
            "No candidate ranking trace in this short window.",
            "No standalone pending order trace.",
        ],
    }

    assertion_contract = {
        "schema": "E1RGoldenMasterEquivalenceAssertionsV1",
        "generated_at": now(),
        "source_golden_master": rel(GOLDEN_MASTER_JSON),
        "window": gm.get("window"),
        "trace_shape": trace_shape,
        "equivalence_assertions": equivalence_assertions,
        "instrumentation_gaps": instrumentation_gaps,
        "extraction_minimum": extraction_minimum,
    }
    write_json(ASSERTIONS_JSON, assertion_contract)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "trace_shape_audit_defined": True,
        "golden_master_loaded": True,
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
        "daily_equity_records_available": row_counts["daily_equity_records"] > 0,
        "daily_equity_required_fields_available": daily_equity_audit["ok"],
        "trades_available": row_counts["trades"] > 0,
        "trade_required_fields_available": trade_audit["ok"],
        "action_trace_standalone_missing_identified": True,
        "position_snapshot_missing_identified": True,
        "candidate_trace_gap_identified": row_counts["e1r_candidates"] == 0,
        "equivalence_assertions_written": ASSERTIONS_JSON.exists(),
        "minimum_extraction_assertions_defined": extraction_minimum["can_start_uptrend_extraction_with_minimum_equivalence"],
        "strategy_core_extraction_not_run": True,
    }

    decision = {
        "trace_shape_audit_passed": all([
            validations["golden_master_loaded"],
            validations["daily_equity_records_available"],
            validations["daily_equity_required_fields_available"],
            validations["trades_available"],
            validations["trade_required_fields_available"],
            validations["equivalence_assertions_written"],
            validations["strategy_files_unchanged"],
        ]),
        "minimum_equivalence_available": extraction_minimum["can_start_uptrend_extraction_with_minimum_equivalence"],
        "instrumentation_gap_count": len(instrumentation_gaps),
        "hard_required_assertions": [
            item["name"]
            for item in equivalence_assertions
            if item["hard_fail"]
        ],
        "missing_or_partial_assertions": [
            {
                "name": item["name"],
                "tier": item["tier"],
                "status": item["status"],
                "notes": item["notes"],
            }
            for item in equivalence_assertions
            if item["status"] != "ASSERTABLE"
        ],
        "strategy_core_extraction_allowed_now": False,
        "uptrend_provider_extraction_allowed_now": False,
        "sideways_branch_implementation_allowed_now": False,
        "full_5y_backtest_allowed_now": False,
        "forward_runner_allowed_now": False,
        "recommended_next_stage": "4C-2C-4E-ENGINE-I",
        "conclusion": (
            "TRACE_SHAPE_AUDIT_PASS_READY_FOR_UPTREND_EXTRACTION_PLAN"
            if extraction_minimum["can_start_uptrend_extraction_with_minimum_equivalence"]
            else "TRACE_SHAPE_AUDIT_REQUIRES_TRACE_INSTRUMENTATION_BEFORE_EXTRACTION_PLAN"
        ),
        "recommended_next_action": (
            "Proceed to 4C-2C-4E-ENGINE-I: create UPTREND extraction plan against the locked equivalence assertions. "
            "Do not implement extracted strategy code yet."
        ),
        "engineering_rule": (
            "UPTREND extraction must be judged first by T0/T1 assertions. "
            "T2/T3 gaps are known and must not be hidden; add instrumentation later if strict candidate/order trace is required."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-H",
        "status": "GOLDEN_MASTER_TRACE_SHAPE_AUDIT_COMPLETE",
        "purpose": "Audit golden-master trace shape and define exact equivalence assertions for future UPTREND extraction.",
        "policy": {
            "strategy_logic_changed": False,
            "trace_audit_only": True,
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
        "source": {
            "engine_g_report": rel(ENGINE_G_REPORT),
            "golden_master": rel(GOLDEN_MASTER_JSON),
            "golden_master_sha256": sha256(GOLDEN_MASTER_JSON),
        },
        "row_counts": row_counts,
        "trace_shape": trace_shape,
        "equivalence_assertions": equivalence_assertions,
        "instrumentation_gaps": instrumentation_gaps,
        "extraction_minimum": extraction_minimum,
        "assertions_path": rel(ASSERTIONS_JSON),
        "assertions_sha256": sha256(ASSERTIONS_JSON),
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-H — Golden Master Trace Shape Audit")
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
    md.append("## Row Counts")
    md.append("```json")
    md.append(json.dumps(row_counts, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Trace Shape")
    md.append("```json")
    md.append(json.dumps(trace_shape, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Equivalence Assertions")
    md.append("```json")
    md.append(json.dumps(equivalence_assertions, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Instrumentation Gaps")
    md.append("```json")
    md.append(json.dumps(instrumentation_gaps, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Extraction Minimum")
    md.append("```json")
    md.append(json.dumps(extraction_minimum, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Assertions Artifact")
    md.append(f"- Path: `{report['assertions_path']}`")
    md.append(f"- SHA256: `{report['assertions_sha256']}`")
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

    print("E1R_4C2C4E_ENGINE_H_GOLDEN_MASTER_TRACE_SHAPE_AUDIT_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("row_counts:", json.dumps(row_counts, ensure_ascii=False))
    print("daily_equity_required_audit:", json.dumps(daily_equity_audit, ensure_ascii=False))
    print("trade_required_audit:", json.dumps(trade_audit, ensure_ascii=False))
    print("action_during_trade_audit:", json.dumps(action_during_trade_audit, ensure_ascii=False))
    print("candidate_audit:", json.dumps(candidate_audit, ensure_ascii=False))
    print("instrumentation_gaps:", json.dumps(instrumentation_gaps, ensure_ascii=False))
    print("extraction_minimum:", json.dumps(extraction_minimum, ensure_ascii=False))
    print("assertions:", json.dumps({
        "path": report["assertions_path"],
        "sha256": report["assertions_sha256"],
    }, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(ASSERTIONS_JSON))


if __name__ == "__main__":
    main()
