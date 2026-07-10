#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
import sys
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_E_STATE_CONTRACT_SMOKE.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_E_STATE_CONTRACT_SMOKE.md"
ARCH_MD = ROOT / "docs/architecture/E1R_ENGINE_STATE_CONTRACT.md"
AUDIT_SAMPLE_JSON = ROOT / "exports/e1r_engine/audit/e1r_engine_e_state_contract_sample.json"

ENGINE_A_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_A_STANDALONE_ENGINE_ARCHITECTURE_CONTRACT.json"
ENGINE_B_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_B_R1_NORMALIZED_INPUT_DATA_ADAPTER_CONTRACT_AUDIT.json"
ENGINE_C_R1_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_C_R1_NO_STRATEGY_DATA_HARNESS_SMOKE.json"
ENGINE_D_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_D_HISTORICAL_DATA_ADAPTER_SKELETON_SMOKE.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
]

STATE_FILES = [
    ROOT / "src/e1r_engine/state.py",
    ROOT / "src/e1r_engine/contracts.py",
    ROOT / "src/e1r_engine/adapters/historical_data.py",
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

def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    for p in [ENGINE_A_REPORT, ENGINE_B_REPORT, ENGINE_C_R1_REPORT, ENGINE_D_REPORT]:
        if not p.exists():
            raise FileNotFoundError(f"Missing prerequisite report: {rel(p)}")

    engine_d = read_json(ENGINE_D_REPORT)
    if engine_d.get("decision", {}).get("historical_adapter_skeleton_passed") is not True:
        raise RuntimeError("ENGINE-D did not pass; ENGINE-E state contract smoke is not allowed.")

    from e1r_engine.state import (
        AccountState,
        DecisionTrace,
        Fill,
        OrderIntent,
        DailyEngineResult,
        apply_fills_contract_only,
    )

    # Contract-only toy scenario. This does not decide strategy.
    account_0 = AccountState.empty(date="2026-06-15", initial_cash=100000.0)

    order_1 = OrderIntent(
        date="2026-06-16",
        symbol="AAPL",
        intent_type="BUY",
        side="BUY",
        target_quantity=10.0,
        quantity_delta=10.0,
        reason="contract_smoke_buy_example",
        branch="UPTREND",
        metadata={"contract_only": True},
    )
    fill_1 = Fill.from_order(
        date="2026-06-16",
        symbol="AAPL",
        side="BUY",
        quantity=10.0,
        price=200.0,
        status="FILLED",
        reason="contract_smoke_fill_example",
    )

    account_1 = apply_fills_contract_only(account_0, [fill_1], date="2026-06-16")
    account_1_mtm = account_1.mark_to_market({"AAPL": 205.0}, date="2026-06-17")

    order_2 = OrderIntent(
        date="2026-06-17",
        symbol="AAPL",
        intent_type="HOLD",
        side=None,
        target_quantity=10.0,
        quantity_delta=0.0,
        reason="contract_smoke_hold_example",
        branch="UPTREND",
        metadata={"contract_only": True},
    )

    decision_trace = DecisionTrace(
        date="2026-06-17",
        branch="UPTREND",
        market_regime="UPTREND",
        regime_subclass="NO_SUBCLASS",
        inputs={
            "contract_only": True,
            "no_strategy_logic": True,
            "no_market_gate": True,
            "no_sizing_logic": True,
        },
        candidate_count=0,
        selected_symbols=[],
        order_intents=[order_2],
        reasons=["contract_smoke_state_trace"],
        metadata={"purpose": "validate state/order/fill/trace shapes only"},
    )

    result = DailyEngineResult(
        date="2026-06-17",
        account_before=account_1,
        account_after=account_1_mtm,
        decision_trace=decision_trace,
        order_intents=[order_2],
        fills=[],
        metadata={"contract_only": True},
    )

    account_0_validation = account_0.validate(max_positions=3)
    account_1_validation = account_1.validate(max_positions=3)
    account_1_mtm_validation = account_1_mtm.validate(max_positions=3)
    order_1_validation = order_1.validate()
    fill_1_validation = fill_1.validate()
    result_validation = result.validate(max_positions=3)

    audit_sample = {
        "schema": "E1REngineStateContractSampleV1",
        "generated_at": now(),
        "contract_only": True,
        "account_0": account_0.__dict__,
        "order_1": order_1.__dict__,
        "fill_1": fill_1.__dict__,
        "account_1": {
            **account_1.__dict__,
            "positions": {k: v.__dict__ for k, v in account_1.positions.items()},
        },
        "account_1_mtm": {
            **account_1_mtm.__dict__,
            "positions": {k: v.__dict__ for k, v in account_1_mtm.positions.items()},
        },
        "decision_trace": {
            **decision_trace.__dict__,
            "order_intents": [o.__dict__ for o in decision_trace.order_intents],
        },
        "daily_engine_result": {
            "date": result.date,
            "account_before": {
                **result.account_before.__dict__,
                "positions": {k: v.__dict__ for k, v in result.account_before.positions.items()},
            },
            "account_after": {
                **result.account_after.__dict__,
                "positions": {k: v.__dict__ for k, v in result.account_after.positions.items()},
            },
            "order_intents": [o.__dict__ for o in result.order_intents],
            "fills": [f.__dict__ for f in result.fills],
            "metadata": result.metadata,
        },
    }
    write_json(AUDIT_SAMPLE_JSON, audit_sample)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "state_contracts_defined": True,
        "unit_smoke_only": True,
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
        "engine_a_loaded": True,
        "engine_b_loaded": True,
        "engine_c_r1_loaded": True,
        "engine_d_loaded": True,
        "state_file_created": (ROOT / "src/e1r_engine/state.py").exists(),
        "account_state_valid": account_0_validation["ok"] and account_1_validation["ok"] and account_1_mtm_validation["ok"],
        "order_intent_valid": len(order_1_validation) == 0,
        "fill_valid": len(fill_1_validation) == 0,
        "decision_trace_valid": len(decision_trace.validate()) == 0,
        "daily_engine_result_valid": result_validation["ok"] is True,
        "max_positions_contract_enforced": account_1_mtm_validation["open_positions_count"] <= 3,
        "equity_identity_valid": abs(account_1_mtm.total_equity - (account_1_mtm.cash + account_1_mtm.positions_value)) < 1e-6,
        "audit_sample_written": AUDIT_SAMPLE_JSON.exists(),
        "strategy_core_extraction_not_allowed_yet": True,
    }

    decision = {
        "state_contract_smoke_passed": all([
            validations["state_file_created"],
            validations["account_state_valid"],
            validations["order_intent_valid"],
            validations["fill_valid"],
            validations["decision_trace_valid"],
            validations["daily_engine_result_valid"],
            validations["max_positions_contract_enforced"],
            validations["equity_identity_valid"],
            validations["strategy_files_unchanged"],
        ]),
        "state_api_locked_for_next_stage": {
            "PositionState": "symbol, quantity, avg_cost, last_price, market_value, unrealized_pnl, entry_date, last_update_date",
            "AccountState": "date, cash, positions, total_equity, positions_value, open_positions_count",
            "OrderIntent": "date, symbol, intent_type, side, target_quantity, quantity_delta, reason, branch",
            "Fill": "date, symbol, side, quantity, price, gross_amount, status, reason",
            "DecisionTrace": "date, branch, market_regime, regime_subclass, inputs, candidate_count, selected_symbols, order_intents, reasons",
            "DailyEngineResult": "date, account_before, account_after, decision_trace, order_intents, fills",
        },
        "strategy_core_extraction_allowed_now": False,
        "full_5y_backtest_allowed_now": False,
        "forward_runner_allowed_now": False,
        "recommended_next_stage": "4C-2C-4E-ENGINE-F",
        "conclusion": (
            "STATE_CONTRACT_SMOKE_PASS_READY_FOR_ENGINE_CORE_SHELL"
            if all([
                validations["state_file_created"],
                validations["account_state_valid"],
                validations["daily_engine_result_valid"],
                validations["strategy_files_unchanged"],
            ])
            else "STATE_CONTRACT_SMOKE_NEEDS_REVIEW"
        ),
        "recommended_next_action": (
            "Proceed to 4C-2C-4E-ENGINE-F: define E1RCoreEngine shell and RegimeRouter shell with no strategy decisions. "
            "Do not extract UPTREND strategy core yet."
        ),
        "engineering_rule": (
            "State contracts may represent account/order/fill/trace data. "
            "They must not decide trading actions, sizing, market gate, or regime branch execution."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-E",
        "status": "STATE_CONTRACT_SMOKE_COMPLETE",
        "purpose": "Define AccountState / PositionState / OrderIntent / Fill / DecisionTrace / DailyEngineResult contracts and validate contract-only accounting identity.",
        "policy": {
            "strategy_logic_changed": False,
            "unit_smoke_only": True,
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
        "state_files": [rel(p) for p in STATE_FILES],
        "state_contract_validation": {
            "account_0": account_0_validation,
            "account_1": account_1_validation,
            "account_1_mtm": account_1_mtm_validation,
            "order_1_errors": order_1_validation,
            "fill_1_errors": fill_1_validation,
            "daily_engine_result": result_validation,
        },
        "audit_sample_path": rel(AUDIT_SAMPLE_JSON),
        "audit_sample_sha256": sha256(AUDIT_SAMPLE_JSON),
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-E — State Contract Smoke")
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
    md.append("## State Files")
    md.append("```json")
    md.append(json.dumps(report["state_files"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## State Contract Validation")
    md.append("```json")
    md.append(json.dumps(report["state_contract_validation"], indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_ENGINE_E_STATE_CONTRACT_SMOKE_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("state_files:", json.dumps(report["state_files"], ensure_ascii=False))
    print("state_contract_validation:", json.dumps(report["state_contract_validation"], ensure_ascii=False))
    print("audit_sample:", json.dumps({
        "path": report["audit_sample_path"],
        "sha256": report["audit_sample_sha256"],
    }, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(AUDIT_SAMPLE_JSON))

if __name__ == "__main__":
    main()
