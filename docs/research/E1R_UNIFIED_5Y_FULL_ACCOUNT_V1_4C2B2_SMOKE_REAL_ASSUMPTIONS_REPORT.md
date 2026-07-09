# E1R Unified 5Y Full Account V1 — 4C-2B-2 Smoke Real Assumptions

Generated At: `2026-07-09T11:30:51.268574+00:00`

## Status

- Status: `E1R_UNIFIED_ENGINE_SMOKE_REAL_ASSUMPTIONS_COMPLETE_NO_FULL_BACKTEST`
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
  "error": "AttributeError: 'list' object has no attribute 'get'",
  "traceback_tail": "Traceback (most recent call last):\n  File \"/Users/dongfang/Downloads/sp500-tracker-v13/scripts/smoke_invoke_unified_engine_4c2b2.py\", line 419, in main\n    result = fn(\n  File \"/Users/dongfang/Downloads/sp500-tracker-v13/src/engine/backtest.py\", line 972, in run_stateful_simulation\n    highs = {s: ohlc_map[s].get(\"high\", []) for s in ohlc_map}\n  File \"/Users/dongfang/Downloads/sp500-tracker-v13/src/engine/backtest.py\", line 972, in <dictcomp>\n    highs = {s: ohlc_map[s].get(\"high\", []) for s in ohlc_map}\nAttributeError: 'list' object has no attribute 'get'\n",
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
    "assumption_provenance_counts": {
      "hard_default": 15,
      "recovered_artifact": 29,
      "hard_default_extra": 12
    },
    "assumption_recovery_sources": [
      {
        "source": "exports/portfolio_backtest.json",
        "json_path": "$",
        "overlap_count": 6,
        "overlap_keys": [
          "entry_top_n",
          "execution_model",
          "initial_capital",
          "rank_based_exit",
          "strategy_variant",
          "version"
        ]
      },
      {
        "source": "exports/portfolio_backtest.json",
        "json_path": "$.strategy_controls",
        "overlap_count": 16,
        "overlap_keys": [
          "candidate_top_n",
          "entry_rs_min",
          "ls60_exit_mode",
          "min_hold_allow_broken_exit",
          "min_holding_days",
          "qualified_entry_enabled",
          "qualified_ma50_slope_min",
          "qualified_momentum_min",
          "qualified_price_above_ma50",
          "qualified_rs_min",
          "qualified_states",
          "qualified_th_min",
          "relative_stop_action",
          "relative_stop_enabled",
          "relative_stop_once_per_position",
          "relative_stop_underperform_pct"
        ]
      },
      {
        "source": "exports/portfolio_backtest.json",
        "json_path": "$.comparison[0]",
        "overlap_count": 8,
        "overlap_keys": [
          "candidate_top_n",
          "entry_rs_min",
          "ls60_exit_mode",
          "min_holding_days",
          "qualified_entry_enabled",
          "qualified_states",
          "relative_stop_enabled",
          "relative_stop_underperform_pct"
        ]
      },
      {
        "source": "exports/portfolio_backtest.json",
        "json_path": "$.comparison[1]",
        "overlap_count": 8,
        "overlap_keys": [
          "candidate_top_n",
          "entry_rs_min",
          "ls60_exit_mode",
          "min_holding_days",
          "qualified_entry_enabled",
          "qualified_states",
          "relative_stop_enabled",
          "relative_stop_underperform_pct"
        ]
      },
      {
        "source": "exports/portfolio_backtest.json",
        "json_path": "$.variant_results.E1_AUDITED_G4_MINHOLD10",
        "overlap_count": 6,
        "overlap_keys": [
          "entry_top_n",
          "execution_model",
          "initial_capital",
          "rank_based_exit",
          "strategy_variant",
          "version"
        ]
      },
      {
        "source": "exports/portfolio_backtest.json",
        "json_path": "$.variant_results.E1_AUDITED_G4_MINHOLD10.strategy_controls",
        "overlap_count": 16,
        "overlap_keys": [
          "candidate_top_n",
          "entry_rs_min",
          "ls60_exit_mode",
          "min_hold_allow_broken_exit",
          "min_holding_days",
          "qualified_entry_enabled",
          "qualified_ma50_slope_min",
          "qualified_momentum_min",
          "qualified_price_above_ma50",
          "qualified_rs_min",
          "qualified_states",
          "qualified_th_min",
          "relative_stop_action",
          "relative_stop_enabled",
          "relative_stop_once_per_position",
          "relative_stop_underperform_pct"
        ]
      },
      {
        "source": "exports/portfolio_backtest.json",
        "json_path": "$.variant_results.E2_DYNAMIC_EXIT_V2",
        "overlap_count": 6,
        "overlap_keys": [
          "entry_top_n",
          "execution_model",
          "initial_capital",
          "rank_based_exit",
          "strategy_variant",
          "version"
        ]
      },
      {
        "source": "exports/portfolio_backtest.json",
        "json_path": "$.variant_results.E2_DYNAMIC_EXIT_V2.strategy_controls",
        "overlap_count": 16,
        "overlap_keys": [
          "candidate_top_n",
          "entry_rs_min",
          "ls60_exit_mode",
          "min_hold_allow_broken_exit",
          "min_holding_days",
          "qualified_entry_enabled",
          "qualified_ma50_slope_min",
          "qualified_momentum_min",
          "qualified_price_above_ma50",
          "qualified_rs_min",
          "qualified_states",
          "qualified_th_min",
          "relative_stop_action",
          "relative_stop_enabled",
          "relative_stop_once_per_position",
          "relative_stop_underperform_pct"
        ]
      },
      {
        "source": "exports/backtest.json",
        "json_path": "$.backtest.results.layer_d",
        "overlap_count": 6,
        "overlap_keys": [
          "entry_top_n",
          "execution_model",
          "initial_capital",
          "rank_based_exit",
          "strategy_variant",
          "version"
        ]
      },
      {
        "source": "exports/backtest.json",
        "json_path": "$.backtest.results.layer_d.strategy_controls",
        "overlap_count": 16,
        "overlap_keys": [
          "candidate_top_n",
          "entry_rs_min",
          "ls60_exit_mode",
          "min_hold_allow_broken_exit",
          "min_holding_days",
          "qualified_entry_enabled",
          "qualified_ma50_slope_min",
          "qualified_momentum_min",
          "qualified_price_above_ma50",
          "qualified_rs_min",
          "qualified_states",
          "qualified_th_min",
          "relative_stop_action",
          "relative_stop_enabled",
          "relative_stop_once_per_position",
          "relative_stop_underperform_pct"
        ]
      }
    ],
    "final_assumptions": {
      "add_size": 0.5,
      "block_add_after_take_profit": true,
      "buy_size": 1.0,
      "candidate_top_n": 10,
      "dynamic_exit_enabled": false,
      "e1r_regime_daily": {},
      "e1r_regime_source": "disabled_smoke",
      "e1r_regime_wiring_enabled": false,
      "e1r_shell_mode": "default",
      "e1r_uptrend_execution_enabled": false,
      "entry_rs_min": 90.0,
      "entry_top_n": 3,
      "execution_model": "adverse_intraday",
      "fill_only_enabled": false,
      "gate_use_leadership": true,
      "gate_use_slope": true,
      "initial_capital": 100000.0,
      "ls60_exit_mode": "exit",
      "market_gate_enabled": true,
      "market_shock_daily_return": -0.02,
      "market_shock_gate_enabled": false,
      "max_positions": 10,
      "max_single_size": 1.0,
      "min_hold_allow_broken_exit": true,
      "min_holding_days": 10,
      "partial_take_profit_enabled": false,
      "partial_take_profit_fraction": 0.5,
      "partial_take_profit_threshold": 0.0,
      "qualified_entry_enabled": false,
      "qualified_ma50_slope_min": 0.0,
      "qualified_momentum_min": 85.0,
      "qualified_price_above_ma50": true,
      "qualified_rs_min": 90.0,
      "qualified_states": [
        "Expansion"
      ],
      "qualified_th_min": 75.0,
      "rank_based_exit": false,
      "relative_stop_action": "REL_REDUCE",
      "relative_stop_enabled": false,
      "relative_stop_once_per_position": true,
      "relative_stop_underperform_pct": -8.0,
      "risk_off_below_spx_ma50": false,
      "strategy_variant": "E1_audited_g4_minhold10",
      "total_one_way": 1.0,
      "version": "v1.6-ls60-mode-comparison",
      "sell_size": 1.0,
      "reduce_size": 0.5,
      "position_size_pct": 0.1,
      "min_hold": 10,
      "leader_score_exit": 60,
      "exit_score": 60,
      "market_entry_gate": "slope_leadership",
      "partial_take_profit": false,
      "commission_pct": 0.0,
      "slippage_pct": 0.0,
      "risk_budget": 1.0,
      "risk_budget_mode": "full"
    }
  },
  "result_summary": {}
}
```

## Conclusion

- `PACKAGE_IMPORT_OK_SMOKE_RETRY_FAILED`
- Recommended: Use traceback to add remaining missing assumptions or adjust input contract, then retry.

