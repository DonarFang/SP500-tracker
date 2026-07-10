#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import hashlib
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_A_STANDALONE_ENGINE_ARCHITECTURE_CONTRACT.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_A_STANDALONE_ENGINE_ARCHITECTURE_CONTRACT.md"
ARCH_MD = ROOT / "docs/architecture/E1R_STANDALONE_ENGINE_ARCHITECTURE_CONTRACT.md"

BACKTEST_PATH = ROOT / "src/engine/backtest.py"
TRACKING_ENGINE_PATH = ROOT / "src/oos/tracking_engine.py"
TRADE_DECISION_PATH = ROOT / "src/engine/trade_decision.py"
SIDECAR_PATH = ROOT / "src/engine/e1r_sidecar_sleeve.py"
COMPOSER_PATH = ROOT / "src/engine/e1r_composer.py"

D3_REPORT = ROOT / "docs/research/E1R_4C2C4E_D3_UPTREND_RUNTIME_EQUIVALENCE_AUDIT.json"
D4A_REPORT = ROOT / "docs/research/E1R_4C2C4E_D4A_UPTREND_GOLDEN_MASTER_TRACE_CONTRACT.json"
D4B_R1_REPORT = ROOT / "docs/research/E1R_4C2C4E_D4B_R1_UPTREND_GOLDEN_MASTER_DIAGNOSTIC.json"

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

def function_summary(path: Path, name: str) -> dict[str, Any]:
    if not path.exists():
        return {
            "exists": False,
            "path": rel(path),
            "name": name,
        }

    text = read_text(path)
    lines = text.splitlines()

    try:
        tree = ast.parse(text)
    except Exception as e:
        return {
            "exists": False,
            "path": rel(path),
            "name": name,
            "parse_error": f"{type(e).__name__}: {e}",
        }

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            src = "\n".join(lines[node.lineno - 1:getattr(node, "end_lineno", node.lineno)])
            lower = src.lower()
            return {
                "exists": True,
                "path": rel(path),
                "name": name,
                "start_line": node.lineno,
                "end_line": getattr(node, "end_lineno", node.lineno),
                "line_count": getattr(node, "end_lineno", node.lineno) - node.lineno + 1,
                "args": [a.arg for a in node.args.args],
                "features": {
                    "has_candidate_logic": any(x in lower for x in ["candidate", "leader_score", "rank", "qualified"]),
                    "has_buy": "BUY" in src,
                    "has_add": "ADD" in src,
                    "has_reduce": "REDUCE" in src or "TP_REDUCE" in src,
                    "has_exit": "EXIT" in src,
                    "has_hold": "HOLD" in src,
                    "has_cash": "cash" in src,
                    "has_positions": "positions" in src,
                    "has_total_equity": "total_equity" in src or "equity" in src,
                    "has_market_gate": "market_gate" in src or "gate_" in lower,
                    "has_max_positions": "max_positions" in src or "open_positions_count" in src,
                    "has_regime": "regime" in lower,
                    "has_sidecar": "sidecar" in lower,
                    "references_invalid_artifacts": any(x in src for x in INVALID_ARTIFACTS),
                },
            }

    return {
        "exists": False,
        "path": rel(path),
        "name": name,
        "reason": "function_not_found",
    }

def prior_report_summary() -> dict[str, Any]:
    out = {}

    for label, path in {
        "D3": D3_REPORT,
        "D4A": D4A_REPORT,
        "D4B_R1": D4B_R1_REPORT,
    }.items():
        if not path.exists():
            out[label] = {"exists": False, "path": rel(path)}
            continue

        data = read_json(path)
        out[label] = {
            "exists": True,
            "path": rel(path),
            "status": data.get("status"),
            "decision": data.get("decision"),
            "policy": data.get("policy"),
        }

    return out

def build_engine_contract() -> dict[str, Any]:
    return {
        "contract_name": "E1R_STANDALONE_ENGINE_ARCHITECTURE_CONTRACT_V1",
        "core_principle": (
            "Backtest, forward test / paper tracking, and future live trading must call the same E1R Core Engine. "
            "Mode-specific code may only adapt data, execution, persistence, and reporting; it must not fork trading logic."
        ),
        "engine_goal": {
            "historical_backtest": "Run formal 5Y E1R historical simulation using the same core decision engine.",
            "forward_test": "Run daily paper tracking using the same core decision engine and persisted account state.",
            "future_live": "Use the same core decision engine with a live broker execution adapter after explicit approval.",
        },
        "non_negotiable_rules": [
            "Do not maintain separate backtest-only, forward-only, or live-only trading logic.",
            "Do not use stitched return curves.",
            "Do not use invalid artifacts as formal sources.",
            "Do not silently modify entry, exit, add, reduce, hold, sizing, market gate, regime routing, or account-state rules.",
            "Do not use src/oos/tracking_engine.py::run_oos_day as the official historical UPTREND provider.",
            "Do not treat sidecar Top10 as ten live holdings; it is candidate/ranking input only.",
            "Live holdings must never exceed max_open_positions = 3.",
            "Cash, positions, pending orders, realized/unrealized PnL, and equity must be owned by one continuous account state.",
            "Golden master / equivalence checks must precede any strategy-core extraction.",
        ],
        "target_module_layout": {
            "core_engine": "src/e1r_engine/core.py",
            "contracts": "src/e1r_engine/contracts.py",
            "state": "src/e1r_engine/state.py",
            "strategy_core": "src/e1r_engine/strategy_core.py",
            "regime_router": "src/e1r_engine/regime_router.py",
            "uptrend_core": "src/e1r_engine/uptrend_core.py",
            "sideways_core": "src/e1r_engine/sideways_core.py",
            "cash_defensive_core": "src/e1r_engine/cash_defensive_core.py",
            "data_adapters": {
                "historical": "src/e1r_engine/adapters/historical_data.py",
                "forward": "src/e1r_engine/adapters/forward_data.py",
                "live_future": "src/e1r_engine/adapters/live_data.py",
            },
            "execution_adapters": {
                "backtest": "src/e1r_engine/adapters/backtest_execution.py",
                "paper": "src/e1r_engine/adapters/paper_execution.py",
                "live_future": "src/e1r_engine/adapters/live_broker_execution.py",
            },
            "persistence": {
                "backtest_memory": "in-memory state for historical simulation",
                "paper_state": "persisted JSON state for forward tracking",
                "live_state_future": "broker/account synced state after explicit approval",
            },
            "exports": {
                "backtest": "exports/e1r_engine/backtest/",
                "forward": "exports/e1r_engine/forward/",
                "audit": "exports/e1r_engine/audit/",
            },
        },
        "engine_api_contract": {
            "E1RCoreEngine.step": {
                "purpose": "Process one trading date with current account state and normalized market snapshot.",
                "inputs": [
                    "as_of_date",
                    "mode: BACKTEST | PAPER | LIVE",
                    "account_state",
                    "market_snapshot",
                    "regime_snapshot",
                    "universe_snapshot",
                    "config",
                    "execution_adapter",
                ],
                "outputs": [
                    "next_account_state",
                    "decision_trace",
                    "orders",
                    "fills",
                    "daily_account_record",
                    "validation_flags",
                ],
                "must_not": [
                    "read mode-specific files directly",
                    "write dashboard outputs directly",
                    "call invalid artifacts",
                    "fork trading logic by mode",
                ],
            },
            "E1RBacktestRunner.run": {
                "purpose": "Loop over historical dates and call E1RCoreEngine.step for each date.",
                "allowed_responsibility": [
                    "historical data loading",
                    "date iteration",
                    "in-memory account initialization",
                    "backtest execution fills",
                    "backtest report export",
                ],
                "not_allowed": [
                    "own separate trading rules",
                    "override core decisions",
                    "stitch sidecar/composer curves",
                ],
            },
            "E1RForwardRunner.run_day": {
                "purpose": "Load latest data and persisted paper account state, then call E1RCoreEngine.step once.",
                "allowed_responsibility": [
                    "latest data loading",
                    "state persistence",
                    "paper execution fills",
                    "forward report export",
                ],
                "not_allowed": [
                    "own separate trading rules",
                    "use run_oos_day as a parallel decision engine",
                    "override core decisions",
                ],
            },
            "E1RLiveRunner.future": {
                "purpose": "Future live wrapper; disabled until explicitly approved.",
                "allowed_responsibility": [
                    "broker data adapter",
                    "broker order adapter",
                    "broker state reconciliation",
                    "risk and safety checks",
                ],
                "not_allowed": [
                    "bypass E1RCoreEngine",
                    "introduce new trading rules outside core",
                ],
            },
        },
        "state_contract": {
            "AccountState": [
                "cash",
                "positions",
                "pending_orders",
                "realized_pnl",
                "unrealized_pnl",
                "total_equity",
                "open_positions_count",
                "max_open_positions",
                "last_processed_date",
                "mode",
            ],
            "PositionState": [
                "symbol",
                "shares",
                "avg_cost",
                "size_units",
                "entry_date",
                "entry_signal",
                "entry_price",
                "leader_score_entry",
                "entry_regime",
                "entry_type",
                "highest_close",
                "min_close_since_entry",
                "action_history",
            ],
            "hard_invariants": [
                "open_positions_count <= 3",
                "cash cannot silently diverge between modes",
                "position sizing must be decided by core logic and filled by execution adapter",
                "state transition timing must be identical between backtest and forward when input snapshots are identical",
            ],
        },
        "strategy_core_contract": {
            "RegimeRouter": {
                "UPTREND": "call UPTREND core extracted from existing validated run_stateful_simulation behavior",
                "SIDEWAYS_MA_CONFLICT": "call sidecar candidate provider as candidate/ranking input, then core max3 account execution",
                "DETERIORATION_TRANSITION": "cash defensive branch",
                "RECOVERY_TRANSITION": "cash defensive branch",
                "DOWNTREND": "cash defensive branch",
            },
            "UPTREND": {
                "source_of_truth": "src/engine/backtest.py::run_stateful_simulation current validated behavior",
                "migration_method": "golden-master-first no-strategy-change extraction",
                "required_equivalence": [
                    "BUY symbol/date/reason match",
                    "EXIT symbol/date/reason match",
                    "ADD/REDUCE/HOLD behavior match",
                    "candidate ranking match",
                    "market gate match",
                    "max_positions behavior match",
                    "sizing/cash/equity match within explicit tolerance",
                ],
            },
            "SIDEWAYS_MA_CONFLICT": {
                "source_of_truth": "src/engine/e1r_sidecar_sleeve.py strict MA_CONFLICT Top10 candidate/ranking provider",
                "important_rule": "Top10 is not ten live holdings; final account holdings remain max3.",
            },
            "CASH_DEFENSIVE": {
                "behavior": "No new risk entries; manage/exit existing positions according to approved defensive branch rules.",
                "must_be_explicit": True,
            },
        },
        "data_adapter_contract": {
            "normalized_input_required": True,
            "reason": "D4B-R1 showed that ad hoc JSON parsing is unsafe; engine must rely on one normalized input contract.",
            "NormalizedMarketSnapshot": [
                "date",
                "prices_by_symbol",
                "ohlc_by_symbol_optional",
                "index_prices",
                "regime",
                "subclass",
                "leader_features",
                "universe_membership",
            ],
            "historical_adapter": {
                "must_use_existing_verified_loader_or_formalized_replacement": True,
                "purpose": "5Y backtest data normalization.",
            },
            "forward_adapter": {
                "purpose": "Daily latest data normalization using same schema.",
            },
            "live_adapter_future": {
                "purpose": "Broker/live market data normalization using same schema.",
            },
        },
        "execution_adapter_contract": {
            "BacktestExecutionAdapter": [
                "simulate fills using approved historical execution convention",
                "return fills to core/account state",
            ],
            "PaperExecutionAdapter": [
                "simulate/record paper fills using latest close or approved paper convention",
                "persist paper state",
            ],
            "LiveBrokerExecutionAdapter_future": [
                "disabled until explicit approval",
                "must include broker reconciliation and risk controls",
            ],
            "core_rule": "Execution adapter may fill or reject orders; it must not decide trading signals.",
        },
        "audit_and_output_contract": {
            "decision_trace_required": True,
            "trace_fields": [
                "date",
                "mode",
                "regime",
                "subclass",
                "active_branch",
                "candidate_snapshot",
                "action_decisions",
                "orders",
                "fills",
                "cash",
                "positions",
                "total_equity",
                "open_positions_count",
                "validation_flags",
            ],
            "outputs_by_mode": {
                "backtest": [
                    "daily_equity",
                    "trades",
                    "orders",
                    "fills",
                    "decision_trace",
                    "metrics",
                    "validation_report",
                ],
                "forward": [
                    "daily_forward_state",
                    "paper_orders",
                    "paper_fills",
                    "decision_trace",
                    "dashboard_export",
                ],
                "live_future": [
                    "broker_orders",
                    "broker_fills",
                    "reconciliation_report",
                    "risk_log",
                ],
            },
        },
        "migration_plan": [
            {
                "stage": "ENGINE-A",
                "name": "Standalone engine architecture contract",
                "allowed": "architecture docs only",
                "status": "current",
            },
            {
                "stage": "ENGINE-B",
                "name": "Normalized input/data adapter contract audit",
                "purpose": "Find and formalize the existing verified data loader/input schema.",
                "allowed": "audit only",
            },
            {
                "stage": "ENGINE-C",
                "name": "Core state and execution adapter contract",
                "purpose": "Define AccountState, Order, Fill, DecisionTrace, BacktestExecution, PaperExecution.",
                "allowed": "contract only",
            },
            {
                "stage": "ENGINE-D",
                "name": "Golden master baseline export harness",
                "purpose": "Export baseline traces from current run_stateful_simulation using formalized input adapter.",
                "allowed": "short-window baseline only",
            },
            {
                "stage": "ENGINE-E",
                "name": "UPTREND no-strategy-change extraction",
                "purpose": "Extract UPTREND core from run_stateful_simulation behind golden master equivalence tests.",
                "allowed": "implementation only after contract approval",
            },
            {
                "stage": "ENGINE-F",
                "name": "SIDEWAYS MA_CONFLICT and cash defensive branch integration",
                "purpose": "Integrate sidecar candidate provider and defensive branch into same engine state.",
                "allowed": "smoke first, no official result",
            },
            {
                "stage": "ENGINE-G",
                "name": "5Y E1R backtest runner",
                "purpose": "Run formal 5Y backtest through E1RCoreEngine.",
                "allowed": "only after branch equivalence validations pass",
            },
            {
                "stage": "ENGINE-H",
                "name": "Forward paper runner",
                "purpose": "Daily forward tracking through same E1RCoreEngine.",
                "allowed": "only after backtest runner contract and state persistence pass",
            },
            {
                "stage": "ENGINE-I",
                "name": "Dashboard integration",
                "purpose": "Dashboard consumes engine exports only.",
                "allowed": "after backtest + forward outputs are stable",
            },
        ],
        "success_definition": {
            "architecture_success": [
                "One shared E1R Core Engine defined.",
                "Backtest/forward/live responsibilities separated by adapters.",
                "Trading logic belongs only to strategy core.",
                "Data input contract normalized.",
                "Account state ownership explicit.",
                "Migration path preserves no-strategy-change rule.",
            ],
            "future_engine_success": [
                "5Y backtest can run through E1RCoreEngine.",
                "Forward test can run through E1RCoreEngine with persisted state.",
                "Given same input snapshot and state, backtest and forward mode produce same decisions before execution fill differences.",
                "Dashboard uses engine exports, not stitched research artifacts.",
            ],
        },
    }

def derive_decision(prior: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    d3 = prior.get("D3", {})
    d4a = prior.get("D4A", {})
    d4b = prior.get("D4B_R1", {})

    return {
        "standalone_engine_contract_defined": True,
        "replaces_old_next_step": "D4B-R2 ad hoc loader fix is replaced by ENGINE-B normalized input/data adapter contract audit.",
        "why": [
            "D3 showed run_oos_day is not equivalent and cannot be the official UPTREND provider.",
            "D4A showed golden master fields are sufficient, but only as a baseline contract.",
            "D4B-R1 showed ad hoc data loaders are unsafe and the engine needs a normalized input contract.",
            "The final target requires one core engine callable by backtest, forward test, and future live trading.",
        ],
        "provider_extraction_allowed_now": False,
        "adapter_implementation_allowed_now": False,
        "full_5y_backtest_allowed_now": False,
        "forward_runner_allowed_now": False,
        "conclusion": "STANDALONE_E1R_ENGINE_ARCHITECTURE_CONTRACT_READY",
        "recommended_next_action": (
            "Proceed to 4C-2C-4E-ENGINE-B: normalized input/data adapter contract audit. "
            "Do not patch D4B with another ad hoc loader; formalize the shared input contract first."
        ),
        "engineering_rule": contract["core_principle"],
        "prior_status": {
            "D3": d3.get("status"),
            "D4A": d4a.get("status"),
            "D4B_R1": d4b.get("status"),
        },
    }

def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    prior = prior_report_summary()

    source_inventory = {
        "run_stateful_simulation": function_summary(BACKTEST_PATH, "run_stateful_simulation"),
        "run_oos_day": function_summary(TRACKING_ENGINE_PATH, "run_oos_day"),
        "trade_action": function_summary(TRADE_DECISION_PATH, "trade_action"),
        "trade_action_reason": function_summary(TRADE_DECISION_PATH, "trade_action_reason"),
        "run_daily_rebalanced_sidecar": function_summary(SIDECAR_PATH, "run_daily_rebalanced_sidecar"),
        "build_e1r_sidecar_sleeve": function_summary(SIDECAR_PATH, "build_e1r_sidecar_sleeve"),
    }

    contract = build_engine_contract()
    decision = derive_decision(prior, contract)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "architecture_contract_only": True,
        "strategy_logic_changed": False,
        "backtest_engine_run": False,
        "full_5y_backtest_run": False,
        "forward_runner_run": False,
        "provider_extraction_run": False,
        "adapter_implementation_run": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "invalid_artifacts_not_used_as_source": True,
        "composer_not_used": True,
        "return_curve_stitching_not_used": True,
        "shared_core_engine_principle_defined": True,
        "backtest_forward_live_adapter_boundary_defined": True,
        "state_contract_defined": True,
        "strategy_core_contract_defined": True,
        "data_adapter_contract_defined": True,
        "execution_adapter_contract_defined": True,
        "migration_plan_defined": True,
        "provider_extraction_not_allowed_yet": decision["provider_extraction_allowed_now"] is False,
        "adapter_implementation_not_allowed_yet": decision["adapter_implementation_allowed_now"] is False,
        "full_5y_backtest_not_allowed_yet": decision["full_5y_backtest_allowed_now"] is False,
        "decision_generated": bool(decision["conclusion"]),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-A",
        "status": "STANDALONE_E1R_ENGINE_ARCHITECTURE_CONTRACT_COMPLETE",
        "purpose": "Define a standalone E1R engine architecture callable by 5Y backtest, forward test, and future live trading.",
        "policy": {
            "strategy_logic_changed": False,
            "architecture_contract_only": True,
            "backtest_engine_run": False,
            "full_5y_backtest_run": False,
            "forward_runner_run": False,
            "provider_extraction_run": False,
            "adapter_implementation_run": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
            "invalid_artifacts_used_as_source": False,
            "composer_used": False,
            "return_curve_stitching_used": False,
        },
        "prior_reports": prior,
        "source_inventory": source_inventory,
        "engine_architecture_contract": contract,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-A — Standalone E1R Engine Architecture Contract")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Core Principle")
    md.append("")
    md.append(contract["core_principle"])
    md.append("")
    md.append("## Policy")
    md.append("```json")
    md.append(json.dumps(report["policy"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Why This Architecture Shift Is Required")
    md.append("```json")
    md.append(json.dumps(decision["why"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Target Module Layout")
    md.append("```json")
    md.append(json.dumps(contract["target_module_layout"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Engine API Contract")
    md.append("```json")
    md.append(json.dumps(contract["engine_api_contract"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## State Contract")
    md.append("```json")
    md.append(json.dumps(contract["state_contract"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Strategy Core Contract")
    md.append("```json")
    md.append(json.dumps(contract["strategy_core_contract"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Data Adapter Contract")
    md.append("```json")
    md.append(json.dumps(contract["data_adapter_contract"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Execution Adapter Contract")
    md.append("```json")
    md.append(json.dumps(contract["execution_adapter_contract"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Migration Plan")
    md.append("```json")
    md.append(json.dumps(contract["migration_plan"], indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_ENGINE_A_STANDALONE_ENGINE_ARCHITECTURE_CONTRACT_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("source_inventory_summary:", json.dumps({
        k: {
            "exists": v.get("exists"),
            "path": v.get("path"),
            "name": v.get("name"),
            "line_count": v.get("line_count"),
            "features": v.get("features"),
        }
        for k, v in source_inventory.items()
    }, ensure_ascii=False))
    print("engine_contract_summary:", json.dumps({
        "contract_name": contract["contract_name"],
        "core_principle": contract["core_principle"],
        "target_modules": contract["target_module_layout"],
        "migration_stages": [x["stage"] for x in contract["migration_plan"]],
    }, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))

if __name__ == "__main__":
    main()
