# E1R 4C-2C-4E-ENGINE-A — Standalone E1R Engine Architecture Contract

Generated At: `2026-07-10T05:02:54.322235+00:00`

## Core Principle

Backtest, forward test / paper tracking, and future live trading must call the same E1R Core Engine. Mode-specific code may only adapt data, execution, persistence, and reporting; it must not fork trading logic.

## Policy
```json
{
  "strategy_logic_changed": false,
  "architecture_contract_only": true,
  "backtest_engine_run": false,
  "full_5y_backtest_run": false,
  "forward_runner_run": false,
  "provider_extraction_run": false,
  "adapter_implementation_run": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "frozen_strategy_files_changed": false,
  "invalid_artifacts_used_as_source": false,
  "composer_used": false,
  "return_curve_stitching_used": false
}
```

## Why This Architecture Shift Is Required
```json
[
  "D3 showed run_oos_day is not equivalent and cannot be the official UPTREND provider.",
  "D4A showed golden master fields are sufficient, but only as a baseline contract.",
  "D4B-R1 showed ad hoc data loaders are unsafe and the engine needs a normalized input contract.",
  "The final target requires one core engine callable by backtest, forward test, and future live trading."
]
```

## Target Module Layout
```json
{
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
    "live_future": "src/e1r_engine/adapters/live_data.py"
  },
  "execution_adapters": {
    "backtest": "src/e1r_engine/adapters/backtest_execution.py",
    "paper": "src/e1r_engine/adapters/paper_execution.py",
    "live_future": "src/e1r_engine/adapters/live_broker_execution.py"
  },
  "persistence": {
    "backtest_memory": "in-memory state for historical simulation",
    "paper_state": "persisted JSON state for forward tracking",
    "live_state_future": "broker/account synced state after explicit approval"
  },
  "exports": {
    "backtest": "exports/e1r_engine/backtest/",
    "forward": "exports/e1r_engine/forward/",
    "audit": "exports/e1r_engine/audit/"
  }
}
```

## Engine API Contract
```json
{
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
      "execution_adapter"
    ],
    "outputs": [
      "next_account_state",
      "decision_trace",
      "orders",
      "fills",
      "daily_account_record",
      "validation_flags"
    ],
    "must_not": [
      "read mode-specific files directly",
      "write dashboard outputs directly",
      "call invalid artifacts",
      "fork trading logic by mode"
    ]
  },
  "E1RBacktestRunner.run": {
    "purpose": "Loop over historical dates and call E1RCoreEngine.step for each date.",
    "allowed_responsibility": [
      "historical data loading",
      "date iteration",
      "in-memory account initialization",
      "backtest execution fills",
      "backtest report export"
    ],
    "not_allowed": [
      "own separate trading rules",
      "override core decisions",
      "stitch sidecar/composer curves"
    ]
  },
  "E1RForwardRunner.run_day": {
    "purpose": "Load latest data and persisted paper account state, then call E1RCoreEngine.step once.",
    "allowed_responsibility": [
      "latest data loading",
      "state persistence",
      "paper execution fills",
      "forward report export"
    ],
    "not_allowed": [
      "own separate trading rules",
      "use run_oos_day as a parallel decision engine",
      "override core decisions"
    ]
  },
  "E1RLiveRunner.future": {
    "purpose": "Future live wrapper; disabled until explicitly approved.",
    "allowed_responsibility": [
      "broker data adapter",
      "broker order adapter",
      "broker state reconciliation",
      "risk and safety checks"
    ],
    "not_allowed": [
      "bypass E1RCoreEngine",
      "introduce new trading rules outside core"
    ]
  }
}
```

## State Contract
```json
{
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
    "mode"
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
    "action_history"
  ],
  "hard_invariants": [
    "open_positions_count <= 3",
    "cash cannot silently diverge between modes",
    "position sizing must be decided by core logic and filled by execution adapter",
    "state transition timing must be identical between backtest and forward when input snapshots are identical"
  ]
}
```

## Strategy Core Contract
```json
{
  "RegimeRouter": {
    "UPTREND": "call UPTREND core extracted from existing validated run_stateful_simulation behavior",
    "SIDEWAYS_MA_CONFLICT": "call sidecar candidate provider as candidate/ranking input, then core max3 account execution",
    "DETERIORATION_TRANSITION": "cash defensive branch",
    "RECOVERY_TRANSITION": "cash defensive branch",
    "DOWNTREND": "cash defensive branch"
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
      "sizing/cash/equity match within explicit tolerance"
    ]
  },
  "SIDEWAYS_MA_CONFLICT": {
    "source_of_truth": "src/engine/e1r_sidecar_sleeve.py strict MA_CONFLICT Top10 candidate/ranking provider",
    "important_rule": "Top10 is not ten live holdings; final account holdings remain max3."
  },
  "CASH_DEFENSIVE": {
    "behavior": "No new risk entries; manage/exit existing positions according to approved defensive branch rules.",
    "must_be_explicit": true
  }
}
```

## Data Adapter Contract
```json
{
  "normalized_input_required": true,
  "reason": "D4B-R1 showed that ad hoc JSON parsing is unsafe; engine must rely on one normalized input contract.",
  "NormalizedMarketSnapshot": [
    "date",
    "prices_by_symbol",
    "ohlc_by_symbol_optional",
    "index_prices",
    "regime",
    "subclass",
    "leader_features",
    "universe_membership"
  ],
  "historical_adapter": {
    "must_use_existing_verified_loader_or_formalized_replacement": true,
    "purpose": "5Y backtest data normalization."
  },
  "forward_adapter": {
    "purpose": "Daily latest data normalization using same schema."
  },
  "live_adapter_future": {
    "purpose": "Broker/live market data normalization using same schema."
  }
}
```

## Execution Adapter Contract
```json
{
  "BacktestExecutionAdapter": [
    "simulate fills using approved historical execution convention",
    "return fills to core/account state"
  ],
  "PaperExecutionAdapter": [
    "simulate/record paper fills using latest close or approved paper convention",
    "persist paper state"
  ],
  "LiveBrokerExecutionAdapter_future": [
    "disabled until explicit approval",
    "must include broker reconciliation and risk controls"
  ],
  "core_rule": "Execution adapter may fill or reject orders; it must not decide trading signals."
}
```

## Migration Plan
```json
[
  {
    "stage": "ENGINE-A",
    "name": "Standalone engine architecture contract",
    "allowed": "architecture docs only",
    "status": "current"
  },
  {
    "stage": "ENGINE-B",
    "name": "Normalized input/data adapter contract audit",
    "purpose": "Find and formalize the existing verified data loader/input schema.",
    "allowed": "audit only"
  },
  {
    "stage": "ENGINE-C",
    "name": "Core state and execution adapter contract",
    "purpose": "Define AccountState, Order, Fill, DecisionTrace, BacktestExecution, PaperExecution.",
    "allowed": "contract only"
  },
  {
    "stage": "ENGINE-D",
    "name": "Golden master baseline export harness",
    "purpose": "Export baseline traces from current run_stateful_simulation using formalized input adapter.",
    "allowed": "short-window baseline only"
  },
  {
    "stage": "ENGINE-E",
    "name": "UPTREND no-strategy-change extraction",
    "purpose": "Extract UPTREND core from run_stateful_simulation behind golden master equivalence tests.",
    "allowed": "implementation only after contract approval"
  },
  {
    "stage": "ENGINE-F",
    "name": "SIDEWAYS MA_CONFLICT and cash defensive branch integration",
    "purpose": "Integrate sidecar candidate provider and defensive branch into same engine state.",
    "allowed": "smoke first, no official result"
  },
  {
    "stage": "ENGINE-G",
    "name": "5Y E1R backtest runner",
    "purpose": "Run formal 5Y backtest through E1RCoreEngine.",
    "allowed": "only after branch equivalence validations pass"
  },
  {
    "stage": "ENGINE-H",
    "name": "Forward paper runner",
    "purpose": "Daily forward tracking through same E1RCoreEngine.",
    "allowed": "only after backtest runner contract and state persistence pass"
  },
  {
    "stage": "ENGINE-I",
    "name": "Dashboard integration",
    "purpose": "Dashboard consumes engine exports only.",
    "allowed": "after backtest + forward outputs are stable"
  }
]
```

## Validations
```json
{
  "architecture_contract_only": true,
  "strategy_logic_changed": false,
  "backtest_engine_run": false,
  "full_5y_backtest_run": false,
  "forward_runner_run": false,
  "provider_extraction_run": false,
  "adapter_implementation_run": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "strategy_files_unchanged": true,
  "invalid_artifacts_not_used_as_source": true,
  "composer_not_used": true,
  "return_curve_stitching_not_used": true,
  "shared_core_engine_principle_defined": true,
  "backtest_forward_live_adapter_boundary_defined": true,
  "state_contract_defined": true,
  "strategy_core_contract_defined": true,
  "data_adapter_contract_defined": true,
  "execution_adapter_contract_defined": true,
  "migration_plan_defined": true,
  "provider_extraction_not_allowed_yet": true,
  "adapter_implementation_not_allowed_yet": true,
  "full_5y_backtest_not_allowed_yet": true,
  "decision_generated": true
}
```

## Decision
```json
{
  "standalone_engine_contract_defined": true,
  "replaces_old_next_step": "D4B-R2 ad hoc loader fix is replaced by ENGINE-B normalized input/data adapter contract audit.",
  "why": [
    "D3 showed run_oos_day is not equivalent and cannot be the official UPTREND provider.",
    "D4A showed golden master fields are sufficient, but only as a baseline contract.",
    "D4B-R1 showed ad hoc data loaders are unsafe and the engine needs a normalized input contract.",
    "The final target requires one core engine callable by backtest, forward test, and future live trading."
  ],
  "provider_extraction_allowed_now": false,
  "adapter_implementation_allowed_now": false,
  "full_5y_backtest_allowed_now": false,
  "forward_runner_allowed_now": false,
  "conclusion": "STANDALONE_E1R_ENGINE_ARCHITECTURE_CONTRACT_READY",
  "recommended_next_action": "Proceed to 4C-2C-4E-ENGINE-B: normalized input/data adapter contract audit. Do not patch D4B with another ad hoc loader; formalize the shared input contract first.",
  "engineering_rule": "Backtest, forward test / paper tracking, and future live trading must call the same E1R Core Engine. Mode-specific code may only adapt data, execution, persistence, and reporting; it must not fork trading logic.",
  "prior_status": {
    "D3": "UPTREND_RUNTIME_EQUIVALENCE_AUDIT_COMPLETE",
    "D4A": "UPTREND_GOLDEN_MASTER_TRACE_CONTRACT_COMPLETE",
    "D4B_R1": "UPTREND_GOLDEN_MASTER_FAILSAFE_DIAGNOSTIC_COMPLETE"
  }
}
```
