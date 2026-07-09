# E1R Unified 5Y Full Account V1 — 4C-2B-1 Smoke Retry

Generated At: `2026-07-09T11:20:49.729355+00:00`

## Status

- Status: `E1R_UNIFIED_ENGINE_SMOKE_RETRY_COMPLETE_NO_FULL_BACKTEST`
- Full backtest run: `False`
- Strategy logic changed: `False`

## Import Probe

```json
{
  "ok": true,
  "error": null,
  "signature": "(symbols: 'list[str]', prices_map: 'dict[str, list[float]]', dates_map: 'dict[str, list[str]]', spx_prices: 'list[float]', spx_dates: 'list[str]', ohlc_map: 'dict' = None, assumptions: 'dict' = None, step: 'int' = 1, min_history: 'int' = 120, market_score_default: 'float' = 60.0, sim_start_date: 'str' = None, sim_end_date: 'str' = None, ndx_prices: 'list' = None, ndx_dates: 'list' = None, sox_prices: 'list' = None, sox_dates: 'list' = None, vix_prices: 'list' = None, vix_dates: 'list' = None) -> 'dict'"
}
```

## Smoke

```json
{
  "attempted": true,
  "ok": false,
  "error": "TypeError: unsupported operand type(s) for /: 'NoneType' and 'int'",
  "traceback_tail": "Traceback (most recent call last):\n  File \"/Users/dongfang/Downloads/sp500-tracker-v13/scripts/smoke_invoke_unified_engine_4c2b1.py\", line 358, in main\n    result = fn(\n  File \"/Users/dongfang/Downloads/sp500-tracker-v13/src/engine/backtest.py\", line 799, in run_stateful_simulation\n    max_pct  = a[\"max_single_size\"] / max_pos # Top3: max 1/3 per position\nTypeError: unsupported operand type(s) for /: 'NoneType' and 'int'\n",
  "input_summary": {
    "symbol_count": 12,
    "symbols": [
      "A",
      "AAL",
      "AAPL",
      "ABBV",
      "ABNB",
      "ABT",
      "ACGL",
      "ACN",
      "ADBE",
      "ADI",
      "ADM",
      "ADP"
    ],
    "spx_count": 1562,
    "spx_start": "2020-04-01",
    "spx_end": "2026-06-18",
    "sim_start_date": "2021-04-14",
    "sim_end_date": "2021-07-09",
    "required_assumption_keys_count": 44,
    "required_assumption_keys": [
      "add_size",
      "block_add_after_take_profit",
      "buy_size",
      "candidate_top_n",
      "dynamic_exit_enabled",
      "e1r_regime_daily",
      "e1r_regime_source",
      "e1r_regime_wiring_enabled",
      "e1r_shell_mode",
      "e1r_uptrend_execution_enabled",
      "entry_rs_min",
      "entry_top_n",
      "execution_model",
      "fill_only_enabled",
      "gate_use_leadership",
      "gate_use_slope",
      "initial_capital",
      "ls60_exit_mode",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "max_positions",
      "max_single_size",
      "min_hold_allow_broken_exit",
      "min_holding_days",
      "partial_take_profit_enabled",
      "partial_take_profit_fraction",
      "partial_take_profit_threshold",
      "qualified_entry_enabled",
      "qualified_ma50_slope_min",
      "qualified_momentum_min",
      "qualified_price_above_ma50",
      "qualified_rs_min",
      "qualified_states",
      "qualified_th_min",
      "rank_based_exit",
      "relative_stop_action",
      "relative_stop_enabled",
      "relative_stop_once_per_position",
      "relative_stop_underperform_pct",
      "risk_off_below_spx_ma50",
      "strategy_variant",
      "total_one_way",
      "version"
    ],
    "missing_filled": {
      "block_add_after_take_profit": null,
      "dynamic_exit_enabled": false,
      "e1r_regime_daily": null,
      "e1r_regime_source": null,
      "e1r_regime_wiring_enabled": false,
      "e1r_shell_mode": "default",
      "e1r_uptrend_execution_enabled": false,
      "fill_only_enabled": false,
      "gate_use_leadership": null,
      "gate_use_slope": null,
      "ls60_exit_mode": "default",
      "market_shock_daily_return": null,
      "market_shock_gate_enabled": false,
      "max_single_size": null,
      "min_hold_allow_broken_exit": null,
      "partial_take_profit_enabled": false,
      "partial_take_profit_fraction": null,
      "partial_take_profit_threshold": 0.0,
      "qualified_ma50_slope_min": null,
      "qualified_momentum_min": null,
      "qualified_price_above_ma50": null,
      "qualified_rs_min": null,
      "qualified_th_min": null,
      "relative_stop_action": null,
      "relative_stop_once_per_position": null,
      "risk_off_below_spx_ma50": null,
      "strategy_variant": null,
      "total_one_way": null,
      "version": null
    },
    "final_assumption_keys": [
      "add_size",
      "block_add_after_take_profit",
      "buy_size",
      "candidate_top_n",
      "dynamic_exit_enabled",
      "e1r_regime_daily",
      "e1r_regime_source",
      "e1r_regime_wiring_enabled",
      "e1r_shell_mode",
      "e1r_unified_smoke",
      "e1r_uptrend_execution_enabled",
      "entry_rs_min",
      "entry_top_n",
      "execution_model",
      "fill_only_enabled",
      "gate_use_leadership",
      "gate_use_slope",
      "initial_capital",
      "leader_score_exit",
      "ls60_exit_mode",
      "market_entry_gate",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "max_positions",
      "max_single_size",
      "min_hold_allow_broken_exit",
      "min_holding_days",
      "partial_take_profit",
      "partial_take_profit_enabled",
      "partial_take_profit_fraction",
      "partial_take_profit_threshold",
      "position_size_pct",
      "qualified_entry_enabled",
      "qualified_ma50_slope_min",
      "qualified_momentum_min",
      "qualified_price_above_ma50",
      "qualified_rs_min",
      "qualified_states",
      "qualified_th_min",
      "rank_based_exit",
      "reduce_size",
      "relative_stop_action",
      "relative_stop_enabled",
      "relative_stop_once_per_position",
      "relative_stop_underperform_pct",
      "risk_off_below_spx_ma50",
      "sell_size",
      "strategy_variant",
      "total_one_way",
      "version"
    ]
  },
  "result_summary": {}
}
```

## Conclusion

- `PACKAGE_IMPORT_OK_SMOKE_RETRY_FAILED`
- Recommended: Use traceback to add remaining missing assumptions or adjust input contract, then retry.

