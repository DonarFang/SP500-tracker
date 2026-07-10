# E1R 4C-2C-4E-ENGINE-F — Core Engine Shell Smoke

Generated At: `2026-07-10T06:05:14.273521+00:00`

## Purpose
Define E1RCoreEngine shell and RegimeRouter shell, then verify MarketSnapshot + AccountState -> DailyEngineResult flow without strategy decisions.

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

## New Engine Files
```json
[
  "src/e1r_engine/core.py",
  "src/e1r_engine/regime_router.py",
  "src/e1r_engine/state.py",
  "src/e1r_engine/contracts.py",
  "src/e1r_engine/adapters/historical_data.py"
]
```

## Snapshot Summary
```json
{
  "date": "2021-04-05",
  "universe_count": 5,
  "sample_symbols": [
    "A",
    "AAL",
    "AAPL",
    "ABBV",
    "ABNB"
  ],
  "index_symbols": [
    "NDX",
    "SOX",
    "SPX"
  ],
  "regime": {
    "date": "2021-04-05",
    "spx_regime": "UPTREND",
    "subclass": "NO_SUBCLASS",
    "raw": {
      "regime": "UPTREND",
      "subclass": null
    },
    "source_path": "$.daily_regime.2021-04-05"
  }
}
```

## Router Cases
```json
[
  {
    "date": "2021-04-05",
    "branch": "UPTREND",
    "spx_regime": "UPTREND",
    "subclass": "NO_SUBCLASS",
    "reason": "route_uptrend",
    "metadata": {
      "router_shell_only": true,
      "no_strategy_decision": true
    }
  },
  {
    "date": "2021-04-05",
    "branch": "SIDEWAYS_MA_CONFLICT",
    "spx_regime": "SIDEWAYS",
    "subclass": "MA_CONFLICT",
    "reason": "route_sideways_ma_conflict",
    "metadata": {
      "router_shell_only": true,
      "no_strategy_decision": true
    }
  },
  {
    "date": "2021-04-05",
    "branch": "DETERIORATION_TRANSITION",
    "spx_regime": "SIDEWAYS",
    "subclass": "DETERIORATION_TRANSITION",
    "reason": "route_deterioration_transition",
    "metadata": {
      "router_shell_only": true,
      "no_strategy_decision": true
    }
  },
  {
    "date": "2021-04-05",
    "branch": "RECOVERY_TRANSITION",
    "spx_regime": "SIDEWAYS",
    "subclass": "RECOVERY_TRANSITION",
    "reason": "route_recovery_transition",
    "metadata": {
      "router_shell_only": true,
      "no_strategy_decision": true
    }
  },
  {
    "date": "2021-04-05",
    "branch": "DOWNTREND",
    "spx_regime": "DOWNTREND",
    "subclass": "NO_SUBCLASS",
    "reason": "route_downtrend",
    "metadata": {
      "router_shell_only": true,
      "no_strategy_decision": true
    }
  },
  {
    "date": "2021-04-05",
    "branch": "CASH_DEFENSIVE",
    "spx_regime": "UNKNOWN",
    "subclass": "NO_SUBCLASS",
    "reason": "route_default_cash_defensive",
    "metadata": {
      "router_shell_only": true,
      "no_strategy_decision": true
    }
  }
]
```

## Result Validation
```json
{
  "ok": true,
  "errors": [],
  "error_count": 0,
  "date": "2021-04-05",
  "max_positions": 3,
  "account_before": {
    "ok": true,
    "errors": [],
    "error_count": 0,
    "date": "2021-04-05",
    "cash": 90000.0,
    "positions_value": 1255.4335,
    "total_equity": 91255.4335,
    "open_positions_count": 1,
    "max_positions": 3
  },
  "account_after": {
    "ok": true,
    "errors": [],
    "error_count": 0,
    "date": "2021-04-05",
    "cash": 90000.0,
    "positions_value": 1255.4335,
    "total_equity": 91255.4335,
    "open_positions_count": 1,
    "max_positions": 3
  },
  "order_count": 1,
  "fill_count": 0
}
```

## Validations
```json
{
  "core_engine_shell_defined": true,
  "regime_router_shell_defined": true,
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
  "engine_e_loaded": true,
  "new_engine_files_exist": true,
  "historical_adapter_bundle_loaded": true,
  "market_snapshot_created": true,
  "core_step_returned_daily_engine_result": true,
  "daily_engine_result_valid": true,
  "account_before_valid": true,
  "account_after_valid": true,
  "max_positions_contract_enforced": true,
  "fills_empty_by_design": true,
  "orders_are_noop_or_hold_only": true,
  "decision_trace_shell_only": true,
  "router_cases_generated": true,
  "audit_sample_written": true,
  "strategy_core_extraction_not_allowed_yet": true
}
```

## Decision
```json
{
  "core_engine_shell_smoke_passed": true,
  "core_shell_api_locked_for_next_stage": {
    "E1RCoreEngine.step": "MarketSnapshot + AccountState -> DailyEngineResult",
    "RegimeRouter.route": "date + spx_regime + subclass -> RegimeRoute",
    "current_behavior": "mark-to-market + NOOP/HOLD shell only"
  },
  "strategy_core_extraction_allowed_now": false,
  "uptrend_provider_extraction_allowed_now": false,
  "sideways_branch_implementation_allowed_now": false,
  "full_5y_backtest_allowed_now": false,
  "forward_runner_allowed_now": false,
  "recommended_next_stage": "4C-2C-4E-ENGINE-G",
  "conclusion": "CORE_ENGINE_SHELL_PASS_READY_FOR_GOLDEN_MASTER_HARNESS",
  "recommended_next_action": "Proceed to 4C-2C-4E-ENGINE-G: build golden-master harness around existing run_stateful_simulation outputs. Do not extract UPTREND strategy core yet.",
  "engineering_rule": "E1RCoreEngine shell may coordinate data/state/trace flow. It must not decide trading actions until golden-master equivalence work begins."
}
```
