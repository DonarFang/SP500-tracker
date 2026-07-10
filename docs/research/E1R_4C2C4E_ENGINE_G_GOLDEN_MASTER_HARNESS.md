# E1R 4C-2C-4E-ENGINE-G — Golden Master Harness

Generated At: `2026-07-10T06:30:24.113971+00:00`

## Purpose
Run a short-window existing-engine baseline via run_stateful_simulation and export golden-master trace-shaped output for future equivalence comparison.

## Policy
```json
{
  "strategy_logic_changed": false,
  "short_window_existing_engine_run": true,
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

## Baseline Function
```json
{
  "name": "run_stateful_simulation",
  "module": "src.engine.backtest",
  "signature": "(symbols: 'list[str]', prices_map: 'dict[str, list[float]]', dates_map: 'dict[str, list[str]]', spx_prices: 'list[float]', spx_dates: 'list[str]', ohlc_map: 'dict' = None, assumptions: 'dict' = None, step: 'int' = 1, min_history: 'int' = 120, market_score_default: 'float' = 60.0, sim_start_date: 'str' = None, sim_end_date: 'str' = None, ndx_prices: 'list' = None, ndx_dates: 'list' = None, sox_prices: 'list' = None, sox_dates: 'list' = None, vix_prices: 'list' = None, vix_dates: 'list' = None) -> 'dict'"
}
```

## Window
```json
{
  "start": "2021-04-05",
  "end": "2021-06-30",
  "spx_trading_days": 62,
  "max_window_days_allowed": 90
}
```

## Input Summary
```json
{
  "symbols_count": 540,
  "indices": [
    "NDX",
    "SOX",
    "SPX"
  ],
  "regime_count": 1309,
  "vix_available": true,
  "bundle_validation": {
    "ok": true,
    "errors": [],
    "error_count": 0,
    "symbols_count": 540,
    "indices": [
      "NDX",
      "SOX",
      "SPX"
    ],
    "regime_count": 1309,
    "vix_available": true
  },
  "date_alignment": {
    "spx_vs_indices": {
      "count": 1562,
      "first": "2020-04-01",
      "last": "2026-06-18",
      "sample": [
        "2020-04-01",
        "2020-04-02",
        "2020-04-03",
        "2020-04-06",
        "2020-04-07"
      ],
      "strict_ok": true,
      "missing_or_empty": [],
      "input_counts": {
        "SPX": 1562,
        "NDX": 1562,
        "SOX": 1562
      }
    },
    "sample_stocks_vs_spx": {
      "count": 1386,
      "first": "2020-12-10",
      "last": "2026-06-18",
      "sample": [
        "2020-12-10",
        "2020-12-11",
        "2020-12-14",
        "2020-12-15",
        "2020-12-16"
      ],
      "strict_ok": true,
      "missing_or_empty": [],
      "input_counts": {
        "SPX": 1562,
        "A": 1562,
        "AAL": 1562,
        "AAPL": 1562,
        "ABBV": 1562,
        "ABNB": 1386,
        "ABT": 1562,
        "ACGL": 1562,
        "ACN": 1562,
        "ADBE": 1562,
        "ADI": 1562,
        "ADM": 1562,
        "ADP": 1562,
        "ADSK": 1562,
        "AEE": 1562,
        "AEP": 1562,
        "AES": 1562,
        "AFL": 1562,
        "AIG": 1562,
        "AIZ": 1562,
        "AJG": 1562
      }
    },
    "spx_vs_regime": {
      "count": 1309,
      "first": "2021-04-05",
      "last": "2026-06-18",
      "sample": [
        "2021-04-05",
        "2021-04-06",
        "2021-04-07",
        "2021-04-08",
        "2021-04-09"
      ],
      "strict_ok": true,
      "missing_or_empty": [],
      "input_counts": {
        "SPX": 1562,
        "regime": 1309
      }
    }
  }
}
```

## Result Summary
```json
{
  "type": "dict",
  "key_count": 50,
  "keys": [
    "alpha_pct",
    "avg_execution_drag_pct",
    "avg_holding_days",
    "avg_loser_pct",
    "avg_winner_pct",
    "cagr_pct",
    "daily_equity_record_count",
    "daily_equity_records",
    "daily_records",
    "e1r_candidate_count",
    "e1r_candidates",
    "e1r_uptrend_execution_enabled",
    "entry_top_n",
    "equity_curve",
    "executed_exit_reason_distribution",
    "executed_reduce_reason_distribution",
    "execution_model",
    "exposure_pct",
    "final_equity",
    "initial_capital",
    "invalid_trades",
    "invalid_trades_count",
    "layer",
    "market_entry_gate",
    "max_drawdown_pct",
    "name",
    "number_of_trades",
    "p0_passed",
    "partial_take_profit",
    "pending_orders_executed",
    "pending_orders_skipped",
    "pending_signal_reason_distribution",
    "portfolio_action_distribution",
    "profit_factor",
    "rank_based_exit",
    "sample_validity",
    "sharpe_ratio",
    "sim_end_liquidation_record",
    "skipped_orders_by_reason",
    "spx_cagr_pct",
    "spx_curve",
    "spx_total_return_pct",
    "status",
    "strategy_controls",
    "strategy_variant",
    "total_return_pct",
    "total_trades_all",
    "trades",
    "version",
    "win_rate_pct"
  ],
  "preview": {
    "layer": "D",
    "name": "Stateful Portfolio Backtest",
    "status": "INSUFFICIENT_SAMPLE"
  }
}
```

## Candidate Trace Sections
```json
{
  "daily_account_candidates": [
    {
      "key": "equity_curve",
      "length": 13,
      "first_row_keys": []
    },
    {
      "key": "daily_records",
      "length": 2,
      "first_row_keys": [
        "cash",
        "date",
        "market_gate_state",
        "n_holdings",
        "pending_orders",
        "position_value",
        "spx_close",
        "spx_day_return_pct",
        "spx_ma50",
        "total_equity"
      ]
    },
    {
      "key": "daily_equity_records",
      "length": 62,
      "first_row_keys": [
        "cash",
        "daily_return_pct",
        "date",
        "drawdown_pct",
        "e1r_active_mode",
        "event",
        "exposure_pct",
        "market_gate_state",
        "open_positions_count",
        "pending_orders_count",
        "positions_value",
        "risk_budget",
        "risk_budget_mode",
        "spx_close",
        "spx_day_return_pct",
        "spx_ma50",
        "spx_regime",
        "total_equity"
      ]
    }
  ],
  "action_trace_candidates": [],
  "trade_candidates": [
    {
      "key": "invalid_trades",
      "length": 0,
      "first_row_keys": []
    },
    {
      "key": "trades",
      "length": 3,
      "first_row_keys": [
        "action_count",
        "actions_during_trade",
        "avg_cost",
        "dominant_regime",
        "effective_exit",
        "entry_date",
        "entry_price",
        "entry_regime",
        "entry_signal",
        "entry_type",
        "execution_model",
        "exit_date",
        "exit_price",
        "exit_regime",
        "exit_signal",
        "exit_type",
        "exit_warning_count",
        "exit_warning_log",
        "holding_days",
        "is_sim_end",
        "leader_score_entry",
        "max_drawdown_in_trade",
        "max_gain_pct",
        "realized_pnl_before_exit",
        "regime_day_weights",
        "return_pct",
        "size_units_at_exit",
        "symbol",
        "take_profit_exec_date",
        "take_profit_triggered"
      ]
    }
  ],
  "equity_curve_candidates": [
    {
      "key": "equity_curve",
      "length": 13,
      "first_row_keys": []
    },
    {
      "key": "daily_equity_records",
      "length": 62,
      "first_row_keys": [
        "cash",
        "daily_return_pct",
        "date",
        "drawdown_pct",
        "e1r_active_mode",
        "event",
        "exposure_pct",
        "market_gate_state",
        "open_positions_count",
        "pending_orders_count",
        "positions_value",
        "risk_budget",
        "risk_budget_mode",
        "spx_close",
        "spx_day_return_pct",
        "spx_ma50",
        "spx_regime",
        "total_equity"
      ]
    }
  ],
  "position_candidates": []
}
```

## Scalar Metrics
```json
{
  "layer": "D",
  "name": "Stateful Portfolio Backtest",
  "status": "INSUFFICIENT_SAMPLE",
  "version": "v1.6-top3-rs-minhold-relstop",
  "execution_model": "adverse_intraday",
  "strategy_variant": "top3_entry_rs_minhold_relstop",
  "entry_top_n": 3,
  "rank_based_exit": false,
  "initial_capital": 100000.0,
  "final_equity": 71746.21,
  "total_return_pct": -28.25,
  "cagr_pct": -74.06,
  "max_drawdown_pct": 28.25,
  "win_rate_pct": 0.0,
  "profit_factor": 0.0,
  "sharpe_ratio": 0,
  "number_of_trades": 3,
  "avg_holding_days": 61.0,
  "avg_winner_pct": 0,
  "avg_loser_pct": -100.0,
  "exposure_pct": 98.4,
  "spx_total_return_pct": 5.38,
  "spx_cagr_pct": 23.76,
  "alpha_pct": -33.63,
  "pending_orders_executed": 6,
  "pending_orders_skipped": 758,
  "avg_execution_drag_pct": 0.0,
  "p0_passed": true,
  "invalid_trades_count": 0,
  "daily_equity_record_count": 62,
  "e1r_candidate_count": 0,
  "e1r_uptrend_execution_enabled": false,
  "total_trades_all": 3
}
```

## Golden Master
- Path: `exports/e1r_engine/golden_master/e1r_engine_g_short_window_golden_master.json`
- SHA256: `89ef22f4b8f98c2fa120f28143c8b7019f10363b405806b6bd8f4f68edb51e8d`

## Validations
```json
{
  "golden_master_harness_defined": true,
  "short_window_existing_engine_run": true,
  "strategy_logic_changed": false,
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
  "engine_f_loaded": true,
  "historical_adapter_bundle_loaded": true,
  "short_window_days_le_90": true,
  "run_stateful_simulation_called_once": true,
  "baseline_result_is_dict": true,
  "baseline_result_has_keys": true,
  "golden_master_file_written": true,
  "trace_sections_detected": true,
  "strategy_core_extraction_not_allowed_yet": true,
  "uptrend_provider_extraction_not_allowed_yet": true
}
```

## Decision
```json
{
  "golden_master_harness_passed": true,
  "trace_sections_detected": 7,
  "golden_master_api_locked_for_next_stage": {
    "baseline_source": "src.engine.backtest.run_stateful_simulation",
    "golden_master_path": "exports/e1r_engine/golden_master/e1r_engine_g_short_window_golden_master.json",
    "window": "2021-04-05..2021-06-30",
    "purpose": "future extraction equivalence comparison, not official performance result"
  },
  "strategy_core_extraction_allowed_now": false,
  "uptrend_provider_extraction_allowed_now": false,
  "sideways_branch_implementation_allowed_now": false,
  "full_5y_backtest_allowed_now": false,
  "forward_runner_allowed_now": false,
  "recommended_next_stage": "4C-2C-4E-ENGINE-H",
  "conclusion": "GOLDEN_MASTER_HARNESS_PASS_READY_FOR_TRACE_SHAPE_AUDIT",
  "recommended_next_action": "Proceed to 4C-2C-4E-ENGINE-H: audit golden-master trace shape and define exact equivalence assertions. Do not extract UPTREND strategy core yet.",
  "engineering_rule": "Golden master is a comparison baseline only. It must not be treated as official result, and it must not modify strategy behavior."
}
```
