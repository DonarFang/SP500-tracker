# E1R 4C-2C-4E-B2 — Backtest Assumptions Contract Audit

Generated At: `2026-07-10T02:28:39.782670+00:00`

## Purpose

This audit fixes the B/B1 issue by locking the assumptions contract before another smoke run.

## Policy
```json
{
  "strategy_logic_changed": false,
  "backtest_engine_run": false,
  "full_5y_backtest_run": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "frozen_strategy_files_changed": false,
  "fix_reason": "B/B1 failed because assumptions contract was not locked before smoke."
}
```

## Validations
```json
{
  "audit_only_no_backtest_run": true,
  "official_result_generated": false,
  "dashboard_changed": false,
  "strategy_files_unchanged": true,
  "run_stateful_contract_extracted": true,
  "callers_found": true,
  "required_unresolved_zero": true
}
```

## Required Keys Without Default
```json
[
  "add_size",
  "buy_size",
  "max_positions",
  "max_single_size",
  "total_one_way"
]
```

## Unresolved Required Keys
```json
[]
```

## Typed Default Blueprint
```json
{
  "add_size": 0.5,
  "block_add_after_take_profit": false,
  "buy_size": 1.0,
  "candidate_top_n": 10,
  "dynamic_exit_enabled": false,
  "e1r_regime_daily": "<regime_daily_dict>",
  "e1r_regime_source": null,
  "e1r_regime_wiring_enabled": false,
  "e1r_shell_mode": false,
  "e1r_uptrend_execution_enabled": false,
  "entry_rs_min": 90.0,
  "entry_top_n": 3,
  "execution_model": "default",
  "fill_only_enabled": false,
  "gate_use_leadership": false,
  "gate_use_slope": false,
  "initial_capital": 100000,
  "ls60_exit_mode": "default",
  "market_gate_enabled": false,
  "market_shock_daily_return": -0.02,
  "market_shock_gate_enabled": false,
  "max_positions": 3,
  "max_single_size": 1.0,
  "min_hold_allow_broken_exit": false,
  "min_holding_days": 10,
  "partial_take_profit_enabled": false,
  "partial_take_profit_fraction": 0.5,
  "partial_take_profit_threshold": 0.07,
  "qualified_entry_enabled": false,
  "qualified_ma50_slope_min": 0.0,
  "qualified_momentum_min": 85.0,
  "qualified_price_above_ma50": false,
  "qualified_rs_min": 90.0,
  "qualified_states": [
    "Expansion"
  ],
  "qualified_th_min": 75.0,
  "rank_based_exit": false,
  "relative_stop_action": "REL_REDUCE",
  "relative_stop_enabled": false,
  "relative_stop_once_per_position": false,
  "relative_stop_underperform_pct": -0.08,
  "risk_off_below_spx_ma50": false,
  "strategy_variant": "default",
  "total_one_way": 1.0,
  "version": "default"
}
```

## Conclusion
- `READY_FOR_4C2C4E_B3_SMOKE_WITH_TYPED_ASSUMPTION_CONTRACT`
- Recommended: Proceed to 4C-2C-4E-B3: rerun continuous stateful smoke using typed assumption blueprint. Do not use heuristic key defaults.
