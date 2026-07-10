# E1R 4C-2C-4E-ENGINE-E — State Contract Smoke

Generated At: `2026-07-10T05:57:12.656378+00:00`

## Purpose
Define AccountState / PositionState / OrderIntent / Fill / DecisionTrace / DailyEngineResult contracts and validate contract-only accounting identity.

## Policy
```json
{
  "strategy_logic_changed": false,
  "unit_smoke_only": true,
  "backtest_engine_run": false,
  "full_5y_backtest_run": false,
  "forward_runner_run": false,
  "provider_extraction_run": false,
  "strategy_core_implemented": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "frozen_strategy_files_changed": false,
  "invalid_artifacts_used_as_source": false,
  "composer_used": false,
  "return_curve_stitching_used": false
}
```

## State Files
```json
[
  "src/e1r_engine/state.py",
  "src/e1r_engine/contracts.py",
  "src/e1r_engine/adapters/historical_data.py"
]
```

## State Contract Validation
```json
{
  "account_0": {
    "ok": true,
    "errors": [],
    "error_count": 0,
    "date": "2026-06-15",
    "cash": 100000.0,
    "positions_value": 0.0,
    "total_equity": 100000.0,
    "open_positions_count": 0,
    "max_positions": 3
  },
  "account_1": {
    "ok": true,
    "errors": [],
    "error_count": 0,
    "date": "2026-06-16",
    "cash": 98000.0,
    "positions_value": 2000.0,
    "total_equity": 100000.0,
    "open_positions_count": 1,
    "max_positions": 3
  },
  "account_1_mtm": {
    "ok": true,
    "errors": [],
    "error_count": 0,
    "date": "2026-06-17",
    "cash": 98000.0,
    "positions_value": 2050.0,
    "total_equity": 100050.0,
    "open_positions_count": 1,
    "max_positions": 3
  },
  "order_1_errors": [],
  "fill_1_errors": [],
  "daily_engine_result": {
    "ok": true,
    "errors": [],
    "error_count": 0,
    "date": "2026-06-17",
    "max_positions": 3,
    "account_before": {
      "ok": true,
      "errors": [],
      "error_count": 0,
      "date": "2026-06-16",
      "cash": 98000.0,
      "positions_value": 2000.0,
      "total_equity": 100000.0,
      "open_positions_count": 1,
      "max_positions": 3
    },
    "account_after": {
      "ok": true,
      "errors": [],
      "error_count": 0,
      "date": "2026-06-17",
      "cash": 98000.0,
      "positions_value": 2050.0,
      "total_equity": 100050.0,
      "open_positions_count": 1,
      "max_positions": 3
    },
    "order_count": 1,
    "fill_count": 0
  }
}
```

## Validations
```json
{
  "state_contracts_defined": true,
  "unit_smoke_only": true,
  "strategy_logic_changed": false,
  "backtest_engine_run": false,
  "full_5y_backtest_run": false,
  "forward_runner_run": false,
  "provider_extraction_run": false,
  "strategy_core_implemented": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "strategy_files_unchanged": true,
  "invalid_artifacts_not_used_as_source": true,
  "composer_not_used": true,
  "return_curve_stitching_used": false,
  "engine_a_loaded": true,
  "engine_b_loaded": true,
  "engine_c_r1_loaded": true,
  "engine_d_loaded": true,
  "state_file_created": true,
  "account_state_valid": true,
  "order_intent_valid": true,
  "fill_valid": true,
  "decision_trace_valid": true,
  "daily_engine_result_valid": true,
  "max_positions_contract_enforced": true,
  "equity_identity_valid": true,
  "audit_sample_written": true,
  "strategy_core_extraction_not_allowed_yet": true
}
```

## Decision
```json
{
  "state_contract_smoke_passed": true,
  "state_api_locked_for_next_stage": {
    "PositionState": "symbol, quantity, avg_cost, last_price, market_value, unrealized_pnl, entry_date, last_update_date",
    "AccountState": "date, cash, positions, total_equity, positions_value, open_positions_count",
    "OrderIntent": "date, symbol, intent_type, side, target_quantity, quantity_delta, reason, branch",
    "Fill": "date, symbol, side, quantity, price, gross_amount, status, reason",
    "DecisionTrace": "date, branch, market_regime, regime_subclass, inputs, candidate_count, selected_symbols, order_intents, reasons",
    "DailyEngineResult": "date, account_before, account_after, decision_trace, order_intents, fills"
  },
  "strategy_core_extraction_allowed_now": false,
  "full_5y_backtest_allowed_now": false,
  "forward_runner_allowed_now": false,
  "recommended_next_stage": "4C-2C-4E-ENGINE-F",
  "conclusion": "STATE_CONTRACT_SMOKE_PASS_READY_FOR_ENGINE_CORE_SHELL",
  "recommended_next_action": "Proceed to 4C-2C-4E-ENGINE-F: define E1RCoreEngine shell and RegimeRouter shell with no strategy decisions. Do not extract UPTREND strategy core yet.",
  "engineering_rule": "State contracts may represent account/order/fill/trace data. They must not decide trading actions, sizing, market gate, or regime branch execution."
}
```
