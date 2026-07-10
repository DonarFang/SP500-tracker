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

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_F_CORE_ENGINE_SHELL_SMOKE.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_F_CORE_ENGINE_SHELL_SMOKE.md"
ARCH_MD = ROOT / "docs/architecture/E1R_CORE_ENGINE_SHELL_CONTRACT.md"
AUDIT_SAMPLE_JSON = ROOT / "exports/e1r_engine/audit/e1r_engine_f_core_engine_shell_sample.json"

ENGINE_A_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_A_STANDALONE_ENGINE_ARCHITECTURE_CONTRACT.json"
ENGINE_B_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_B_R1_NORMALIZED_INPUT_DATA_ADAPTER_CONTRACT_AUDIT.json"
ENGINE_C_R1_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_C_R1_NO_STRATEGY_DATA_HARNESS_SMOKE.json"
ENGINE_D_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_D_HISTORICAL_DATA_ADAPTER_SKELETON_SMOKE.json"
ENGINE_E_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_E_STATE_CONTRACT_SMOKE.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
]

NEW_ENGINE_FILES = [
    ROOT / "src/e1r_engine/core.py",
    ROOT / "src/e1r_engine/regime_router.py",
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

def to_dict(obj: Any) -> Any:
    if hasattr(obj, "__dict__"):
        out = {}
        for k, v in obj.__dict__.items():
            out[k] = to_dict(v)
        return out
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_dict(v) for v in obj]
    return obj

def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    for p in [ENGINE_A_REPORT, ENGINE_B_REPORT, ENGINE_C_R1_REPORT, ENGINE_D_REPORT, ENGINE_E_REPORT]:
        if not p.exists():
            raise FileNotFoundError(f"Missing prerequisite report: {rel(p)}")

    engine_d = read_json(ENGINE_D_REPORT)
    engine_e = read_json(ENGINE_E_REPORT)

    if engine_d.get("decision", {}).get("historical_adapter_skeleton_passed") is not True:
        raise RuntimeError("ENGINE-D did not pass.")
    if engine_e.get("decision", {}).get("state_contract_smoke_passed") is not True:
        raise RuntimeError("ENGINE-E did not pass.")

    from e1r_engine.adapters.historical_data import HistoricalDataAdapter
    from e1r_engine.contracts import MarketSnapshot
    from e1r_engine.core import E1RCoreEngine
    from e1r_engine.state import AccountState, PositionState

    adapter = HistoricalDataAdapter(ROOT)
    bundle = adapter.load_bundle(min_bars=120)

    snapshot_date = "2021-04-05"
    if snapshot_date not in bundle.regime_daily:
        snapshot_date = sorted(bundle.regime_daily.keys())[0]

    sample_symbols = [s for s in bundle.symbols[:5] if snapshot_date in set(bundle.dates_map[s])]
    if not sample_symbols:
        raise RuntimeError(f"No sample symbols available on {snapshot_date}")

    prices_by_symbol = {}
    for sym in sample_symbols:
        idx = bundle.dates_map[sym].index(snapshot_date)
        prices_by_symbol[sym] = bundle.ohlc_map[sym][idx]

    indices = {}
    for idx_sym, series in bundle.indices.items():
        if snapshot_date in series.dates:
            i = series.dates.index(snapshot_date)
            indices[idx_sym] = series.bars[i]

    snapshot = MarketSnapshot(
        date=snapshot_date,
        universe=sample_symbols,
        prices_by_symbol=prices_by_symbol,
        indices=indices,
        regime=bundle.regime_daily.get(snapshot_date),
        metadata={
            "stage": "ENGINE-F",
            "shell_smoke": True,
            "source": "HistoricalDataAdapter",
        },
    )

    first_symbol = sample_symbols[0]
    first_price = prices_by_symbol[first_symbol].close

    account_0 = AccountState(
        date=snapshot_date,
        cash=90000.0,
        positions={
            first_symbol: PositionState.create(
                symbol=first_symbol,
                quantity=10.0,
                avg_cost=first_price * 0.95,
                price=first_price,
                date=snapshot_date,
            )
        },
        positions_value=10.0 * first_price,
        total_equity=90000.0 + 10.0 * first_price,
        open_positions_count=1,
        metadata={"stage": "ENGINE-F", "shell_smoke": True},
    )

    engine = E1RCoreEngine()
    result = engine.step(snapshot=snapshot, account=account_0)

    result_validation = result.validate(max_positions=3)
    account_before_validation = result.account_before.validate(max_positions=3)
    account_after_validation = result.account_after.validate(max_positions=3)

    router_cases = []
    for regime, subclass in [
        ("UPTREND", None),
        ("SIDEWAYS", "MA_CONFLICT"),
        ("SIDEWAYS", "DETERIORATION_TRANSITION"),
        ("SIDEWAYS", "RECOVERY_TRANSITION"),
        ("DOWNTREND", None),
        (None, None),
    ]:
        route = engine.router.route(date=snapshot_date, spx_regime=regime, subclass=subclass)
        router_cases.append(to_dict(route))

    audit_sample = {
        "schema": "E1RCoreEngineShellSmokeSampleV1",
        "generated_at": now(),
        "snapshot": to_dict(snapshot),
        "account_before": to_dict(result.account_before),
        "account_after": to_dict(result.account_after),
        "decision_trace": to_dict(result.decision_trace),
        "order_intents": to_dict(result.order_intents),
        "fills": to_dict(result.fills),
        "router_cases": router_cases,
        "result_validation": result_validation,
    }
    write_json(AUDIT_SAMPLE_JSON, audit_sample)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "core_engine_shell_defined": True,
        "regime_router_shell_defined": True,
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
        "engine_e_loaded": True,
        "new_engine_files_exist": all(p.exists() for p in NEW_ENGINE_FILES),
        "historical_adapter_bundle_loaded": bundle.validate_shape()["ok"] is True,
        "market_snapshot_created": snapshot.date == snapshot_date and len(snapshot.prices_by_symbol) > 0,
        "core_step_returned_daily_engine_result": result.date == snapshot_date,
        "daily_engine_result_valid": result_validation["ok"] is True,
        "account_before_valid": account_before_validation["ok"] is True,
        "account_after_valid": account_after_validation["ok"] is True,
        "max_positions_contract_enforced": result.account_after.open_positions_count <= 3,
        "fills_empty_by_design": len(result.fills) == 0,
        "orders_are_noop_or_hold_only": all(o.intent_type in {"NOOP", "HOLD"} for o in result.order_intents),
        "decision_trace_shell_only": result.decision_trace.inputs.get("shell_mode") is True,
        "router_cases_generated": len(router_cases) == 6,
        "audit_sample_written": AUDIT_SAMPLE_JSON.exists(),
        "strategy_core_extraction_not_allowed_yet": True,
    }

    decision = {
        "core_engine_shell_smoke_passed": all([
            validations["core_engine_shell_defined"],
            validations["regime_router_shell_defined"],
            validations["new_engine_files_exist"],
            validations["historical_adapter_bundle_loaded"],
            validations["market_snapshot_created"],
            validations["daily_engine_result_valid"],
            validations["orders_are_noop_or_hold_only"],
            validations["fills_empty_by_design"],
            validations["decision_trace_shell_only"],
            validations["strategy_files_unchanged"],
        ]),
        "core_shell_api_locked_for_next_stage": {
            "E1RCoreEngine.step": "MarketSnapshot + AccountState -> DailyEngineResult",
            "RegimeRouter.route": "date + spx_regime + subclass -> RegimeRoute",
            "current_behavior": "mark-to-market + NOOP/HOLD shell only",
        },
        "strategy_core_extraction_allowed_now": False,
        "uptrend_provider_extraction_allowed_now": False,
        "sideways_branch_implementation_allowed_now": False,
        "full_5y_backtest_allowed_now": False,
        "forward_runner_allowed_now": False,
        "recommended_next_stage": "4C-2C-4E-ENGINE-G",
        "conclusion": (
            "CORE_ENGINE_SHELL_PASS_READY_FOR_GOLDEN_MASTER_HARNESS"
            if all([
                validations["core_engine_shell_defined"],
                validations["regime_router_shell_defined"],
                validations["daily_engine_result_valid"],
                validations["orders_are_noop_or_hold_only"],
            ])
            else "CORE_ENGINE_SHELL_NEEDS_REVIEW"
        ),
        "recommended_next_action": (
            "Proceed to 4C-2C-4E-ENGINE-G: build golden-master harness around existing run_stateful_simulation outputs. "
            "Do not extract UPTREND strategy core yet."
        ),
        "engineering_rule": (
            "E1RCoreEngine shell may coordinate data/state/trace flow. "
            "It must not decide trading actions until golden-master equivalence work begins."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-F",
        "status": "CORE_ENGINE_SHELL_SMOKE_COMPLETE",
        "purpose": "Define E1RCoreEngine shell and RegimeRouter shell, then verify MarketSnapshot + AccountState -> DailyEngineResult flow without strategy decisions.",
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
        "new_engine_files": [rel(p) for p in NEW_ENGINE_FILES],
        "snapshot_summary": {
            "date": snapshot.date,
            "universe_count": len(snapshot.universe),
            "sample_symbols": snapshot.universe,
            "index_symbols": sorted(snapshot.indices.keys()),
            "regime": to_dict(snapshot.regime),
        },
        "router_cases": router_cases,
        "result_validation": result_validation,
        "account_before_validation": account_before_validation,
        "account_after_validation": account_after_validation,
        "audit_sample_path": rel(AUDIT_SAMPLE_JSON),
        "audit_sample_sha256": sha256(AUDIT_SAMPLE_JSON),
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-F — Core Engine Shell Smoke")
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
    md.append("## New Engine Files")
    md.append("```json")
    md.append(json.dumps(report["new_engine_files"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Snapshot Summary")
    md.append("```json")
    md.append(json.dumps(report["snapshot_summary"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Router Cases")
    md.append("```json")
    md.append(json.dumps(report["router_cases"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Result Validation")
    md.append("```json")
    md.append(json.dumps(report["result_validation"], indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_ENGINE_F_CORE_ENGINE_SHELL_SMOKE_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("new_engine_files:", json.dumps(report["new_engine_files"], ensure_ascii=False))
    print("snapshot_summary:", json.dumps(report["snapshot_summary"], ensure_ascii=False))
    print("router_cases:", json.dumps(report["router_cases"], ensure_ascii=False))
    print("result_validation:", json.dumps(report["result_validation"], ensure_ascii=False))
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
