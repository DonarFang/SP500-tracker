# Stage 3.8E-2F-2C-4C-4 Generator Internals / Export Wrapper Prototype

Generated At: `2026-07-08T10:33:11.881327+00:00`

## Status

- Status: `INSPECTION_COMPLETE_PROTOTYPE_PLAN_DEFINED_NO_SOURCE_CHANGES`
- Dashboard changed: `False`
- Exports changed: `False`
- Workflow changed: `False`
- Strategy logic changed: `False`
- Long backtest run: `False`

## Diagnosis

- e1r_composer.py contains build_equity_records_from_returns; this is the best first candidate for E1R portfolio-level equity construction.
- e1r_composer.py contains extract_core_interval_returns; likely can rebuild core interval portfolio returns before composing equity.
- export_e1r_v0_2_backtest_equity.py has normalize/extract functions but current output is diagnostic rows; likely needs replacement/export-only wrapper, not minor patch.
- e1r_formal_backtest_v0_1.json has numeric equity_curve length=131; useful as reference, but too short for full 5Y daily canonical chart.
- exports/portfolio_backtest.json sample window remains 2023-11-06 to 2026-06-11; not full 5Y.
- Toy import probe for e1r_composer.py ran successfully; wrapper can likely import composer functions safely.

## Key Target Inspection

### `src/engine/e1r_composer.py`

- exists: `True`
- ast_valid: `True`
- key functions:
  - `compound_return(returns)` line `47` returns `float`
  - `max_drawdown(equity_values)` line `55` returns `Optional[float]`
  - `sharpe_ratio(daily_returns)` line `70` returns `Optional[float]`
  - `profit_factor(daily_returns)` line `82` returns `Optional[float]`
  - `extract_core_interval_returns(core_daily_equity_records, sidecar_records)` line `94` returns `list[dict[str, Any]]`
  - `build_equity_records_from_returns(interval_records, initial_equity)` line `171` returns `list[dict[str, Any]]`

### `src/engine/e1r_sidecar_sleeve.py`

- exists: `True`
- ast_valid: `True`
- key functions:
  - `compound_return(returns)` line `69` returns `float`
  - `max_drawdown(equity_values)` line `87` returns `Optional[float]`
  - `sharpe_ratio(daily_returns)` line `102` returns `Optional[float]`
  - `profit_factor(daily_returns)` line `114` returns `Optional[float]`
- path literals: `*.json`

### `src/engine/backtest.py`

- exists: `True`
- ast_valid: `True`
- key functions:
  - `run_trade_rule_validation(symbols, prices_map, spx_prices, forward_days, step, min_history, market_score_default)` line `313` returns `dict`
  - `run_action_forward_validation(symbols, prices_map, spx_prices, dates_map, spx_dates, forward_days, step, min_history, market_score_default)` line `595` returns `dict`
- path literals: `data/research/e1_5y/raw/indices/SPX.json, data/research/e1_5y/regimes/spx_regime_daily.json`

### `scripts/export_e1r_v0_2_backtest_equity.py`

- exists: `True`
- ast_valid: `True`
- key functions:
  - `normalize_curve(records)` line `27` returns `list[dict[str, Any]]`
  - `extract_variant(variants, strategy_id)` line `66` returns `dict[str, Any]`
  - `main()` line `77` returns `None`
- path literals: `Missing exports/backtest.json, Wrote exports/e1r_v0_2_backtest_equity_curve.json, Wrote exports/e1r_v0_2_backtest_summary.json, exports/backtest.json, exports/e1r_v0_2_backtest_equity_curve.json, exports/e1r_v0_2_backtest_summary.json`

### `scripts/run_e1r_v0_2_oos_equity.py`

- exists: `True`
- ast_valid: `True`
- key functions:
  - `main()` line `248` returns `None`
- path literals: `*.json, exports/e1r_v0_2_status.json, exports/oos_e1r_v0_2_equity_curve.json, exports/oos_e1r_v0_2_sidecar.json, exports/oos_e1r_v0_2_summary.json, exports/oos_equity_curve.json, exports/oos_summary.json`

### `scripts/run_e1r_v0_2_forward_performance_core.py`

- exists: `True`
- ast_valid: `True`
- key functions:
  - `sharpe_ratio(values)` line `114` returns `Optional[float]`
  - `main()` line `382` returns `int`
- path literals: `e1r_v0_2_portfolio_state.json, e1r_v0_2_status.json, oos_e1r_v0_2_equity_curve.json, oos_e1r_v0_2_orders.json, oos_e1r_v0_2_positions.json, oos_e1r_v0_2_summary.json, oos_summary.json`

### `data/research/e1r/e1r_formal_backtest_v0_1.json`

- exists: `True`
- top_keys: `comparison_base, e1_metrics, equity_curve, metrics, source, spx_curve, status, trades, variant_id`
- metrics: `{"variant_id": "E1R_REGIME_AWARE_V0_1"}`
- lists:
  - `equity_curve` length `131` last_type `float` keys ``
  - `spx_curve` length `131` last_type `float` keys ``
  - `trades` length `39` last_type `dict` keys `action_count, actions_during_trade, avg_cost, dominant_regime, effective_exit, entry_date, entry_price, entry_regime, entry_signal, entry_type, execution_model, exit_date, exit_price, exit_regime, exit_signal, exit_type, exit_warning_count,`

### `exports/portfolio_backtest.json`

- exists: `True`
- top_keys: `alpha_pct, avg_execution_drag_pct, avg_holding_days, avg_loser_pct, avg_winner_pct, cagr_pct, comparison, daily_records, entry_top_n, executed_exit_reason_distribution, executed_reduce_reason_distribution, execution_model, exposure_pct, final_equity, generated_at, generated_at_display, initial_capital, invalid_trades, invalid_trades_count, layer, market_entry_gate, max_drawdown_pct, name, number_of_trades, p0_passed, partial_take_profit, pending_orders_executed, pending_orders_skipped, pending_signal_reason_distribution, period_comparison, portfolio_action_distribution, profit_factor, rank_based_exit, sample_validity, selected_variant, selection_policy, sharpe_ratio, skipped_orders_by_reason, spx_cagr_pct, spx_total_return_pct, status, strategy_controls, strategy_variant, total_return_pct, total_trades_all, variant_results, version, win_rate_pct`
- metrics: `{"version": "v1.6-ls60-mode-comparison", "total_return_pct": 7.52, "alpha_pct": -61.84, "max_drawdown_pct": 38.1, "profit_factor": 1.25, "sharpe_ratio": 0.18, "final_equity": 107519.31, "initial_capital": 100000.0, "sample_validity": {"is_valid": true, "sample_status": "VALID", "simulation_start_date": "2023-11-06", "simulation_end_date": "2026-06-11", "simulation_days": 651, "total_trades": 47, "completed_trades": 44, "sim_end_trades": 3, "sim_end_ratio_pct": 6.4, "invalid_trades": 0, "minimum_required": {"sim_days": 252, "trades": 20, "sim_end_ratio_pct": 50, "invalid": 0}}}`
- lists:
  - `invalid_trades` length `0` last_type `None` keys ``
  - `daily_records` length `22` last_type `dict` keys `cash, date, market_gate_state, n_holdings, pending_orders, position_value, spx_close, spx_day_return_pct, spx_ma50, total_equity`
  - `comparison` length `2` last_type `dict` keys `alpha_pct, avg_loser_pct, avg_winner_pct, cagr_pct, candidate_top_n, entry_rs_min, exposure_pct, ls60_exit_mode, max_drawdown_pct, min_holding_days, number_of_trades, profit_factor, qualified_entry_enabled, qualified_states, relative_stop_e`

### `exports/e1r_v0_2_backtest_summary.json`

- exists: `True`
- top_keys: `alpha_pct, artifact_type, composition_exists, frozen_artifact, max_drawdown_pct, profit_factor, regeneration_note, regime_aware_logic, research_status, row_count, sharpe_ratio, sidecar_active_by_regime, sidecar_active_by_subclass, sidecar_active_days, source_file, source_json_path, spx_return_pct, strategy_id, total_return_pct, variant`
- metrics: `{"strategy_id": "E1R_REGIME_AWARE_V0_2", "variant": "E1R_REGIME_AWARE_V0_2", "total_return_pct": 116.7435999134756, "spx_return_pct": 76.844174428316, "alpha_pct": 39.89942548515961, "max_drawdown_pct": 25.904809362815108, "profit_factor": 1.1919630955509348, "sharpe_ratio": 0.7957270568329264}`

### `exports/e1r_v0_2_backtest_equity_curve.json`

- exists: `True`
- top_keys: `artifact_type, equity_curve, frozen_artifact, regeneration_note, row_count, rows, source_file, source_json_path, variant`
- metrics: `{"variant": "E1R_REGIME_AWARE_V0_2"}`
- lists:
  - `rows` length `8819` last_type `dict` keys `close, date, diagnostic_only, e1r_entry_type, e1r_uptrend_confirmed_eligible, e1r_uptrend_emerging_eligible, equity, leader_rank, leader_score, ma20, ma20_slope, ma50, ma50_slope, momentum_acceleration, momentum_score, reasons, rs_20d_impro`
  - `equity_curve` length `8819` last_type `dict` keys `close, date, diagnostic_only, e1r_entry_type, e1r_uptrend_confirmed_eligible, e1r_uptrend_emerging_eligible, equity, leader_rank, leader_score, ma20, ma20_slope, ma50, ma50_slope, momentum_acceleration, momentum_score, reasons, rs_20d_impro`

## Toy Import Probe

- status: `RUN`
- returncode: `0`

```text
{
  "has_build_equity_records_from_returns": true,
  "has_extract_core_interval_returns": true,
  "has_compound_return": true,
  "has_max_drawdown": true,
  "has_sharpe_ratio": true,
  "has_profit_factor": true,
  "build_equity_records_from_returns_signature": "(interval_records: 'Sequence[dict[str, Any]]', initial_equity: 'float') -> 'list[dict[str, Any]]'",
  "toy_call_attempts": [
    {
      "name": "returns_only",
      "ok": false,
      "error": "TypeError: build_equity_records_from_returns() missing 1 required positional argument: 'initial_equity'"
    },
    {
      "name": "dates_returns",
      "ok": false,
      "error": "AttributeError: 'str' object has no attribute 'get'"
    },
    {
      "name": "keyword_returns_dates",
      "ok": false,
      "error": "TypeError: build_equity_records_from_returns() got an unexpected keyword argument 'returns'"
    },
    {
      "name": "keyword_interval_returns",
      "ok": false,
      "error": "TypeError: build_equity_records_from_returns() got an unexpected keyword argument 'interval_returns'"
    }
  ]
}

```

## Prototype Wrapper Plan

- recommended_path: `scripts/export_canonical_5y_equity_curves.py`
- next_stage: `Stage 3.8E-2F-2C-4C-5 — Build export-only canonical 5Y equity wrapper smoke test`

## Preferred Implementation Path

1. Use e1r_composer.extract_core_interval_returns and build_equity_records_from_returns if their signatures support existing E1R records.
   - Reason: Composer already contains portfolio-return-to-equity utilities.
2. If E1 5Y daily returns are not exported, call frozen backtest engine in a wrapper and capture daily_equity/portfolio records without changing strategy logic.
   - Reason: Current exports/portfolio_backtest.json is only 2023-11 to 2026-06.
3. Validate final E1R metrics against frozen values: total_return_pct≈116.74, spx_return_pct≈76.84, alpha_pct≈39.90, max_drawdown_pct≈25.9.
   - Reason: Prevents accidental schema-only exports with wrong accounting.
4. Only after validation, patch dashboard main equity chart to use exports/e1_e1r_5y_equity_comparison.json.
   - Reason: Avoids another timeline-anchor bug.

## Long Backtest Policy

- allowed: `True`
- when_reasonable: Only if no existing portfolio daily curve can be recovered from composer/export artifacts.
- Run as export-only wrapper.
- Do not edit frozen strategy files.
- Write canonical exports under new filenames.
- Run smoke/import/signature checks before long run.
- Compare final metrics to frozen references before dashboard consumption.
