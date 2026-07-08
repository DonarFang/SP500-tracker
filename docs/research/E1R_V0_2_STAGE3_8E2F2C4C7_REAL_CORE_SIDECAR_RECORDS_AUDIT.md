# Stage 3.8E-2F-2C-4C-7 Real Core / Sidecar Records Audit

Generated At: `2026-07-08T11:41:21.133414+00:00`

## Status

- Status: `REAL_CORE_SIDECAR_RECORDS_AUDIT_COMPLETE_NO_EXPORTS_WRITTEN`
- Dashboard changed: `False`
- Exports changed: `False`
- Workflow changed: `False`
- Strategy logic changed: `False`
- Canonical exports written: `False`
- Long backtest run: `False`

## Diagnosis

- No strong persisted 5Y sidecar_records candidate found with required minimum fields.
- Found persisted core-daily-like candidate: exports/e1r_v0_2_backtest_equity_curve.json::rows rows=8819.
- No persisted combined interval_records candidate found.
- Real source probe did not produce non-empty intervals from currently persisted OOS sidecar + E1 daily_records.
- If 5Y sidecar/core records are not persisted, 4C-8 should implement inspect/dry-run generation through frozen sidecar/composer path before any long backtest export.

## Persisted Sidecar Candidates


## Persisted Core Candidates

- `exports/oos_e1r_v0_2_equity_curve.json::root` rows `1` dates `2026-06-18→2026-06-18` unique `1`
- `exports/e1r_v0_2_backtest_equity_curve.json::rows` rows `8819` dates `2021-06-11→2023-05-22` unique `187`
- `exports/e1r_v0_2_backtest_equity_curve.json::equity_curve` rows `8819` dates `2021-06-11→2023-05-22` unique `187`
- `exports/portfolio_backtest.json::daily_records` rows `22` dates `2023-11-06→2026-05-13` unique `22`
- `exports/portfolio_backtest.json::variant_results.E1_AUDITED_G4_MINHOLD10.daily_records` rows `22` dates `2023-11-06→2026-05-13` unique `22`
- `exports/portfolio_backtest.json::variant_results.E2_DYNAMIC_EXIT_V2.daily_records` rows `22` dates `2023-11-06→2026-05-13` unique `22`
- `exports/oos_equity_curve.json::curve` rows `12` dates `2026-06-18→2026-07-07` unique `12`

## Persisted Interval Candidates


## Real Source Probe

```json
{
  "candidate_lists": {
    "exports/oos_e1r_v0_2_sidecar.json": [
      {
        "list_path": "excluded_symbols",
        "length": 1,
        "keys": []
      },
      {
        "list_path": "selected",
        "length": 0,
        "keys": []
      }
    ],
    "exports/portfolio_backtest.json": [
      {
        "list_path": "strategy_controls.qualified_states",
        "length": 1,
        "keys": []
      },
      {
        "list_path": "market_entry_gate.blocked_actions",
        "length": 2,
        "keys": []
      },
      {
        "list_path": "market_entry_gate.unaffected_actions",
        "length": 3,
        "keys": []
      },
      {
        "list_path": "invalid_trades",
        "length": 0,
        "keys": []
      },
      {
        "list_path": "daily_records",
        "length": 22,
        "keys": [
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
        "list_path": "comparison",
        "length": 2,
        "keys": [
          "alpha_pct",
          "avg_loser_pct",
          "avg_winner_pct",
          "cagr_pct",
          "candidate_top_n",
          "entry_rs_min",
          "exposure_pct",
          "ls60_exit_mode",
          "max_drawdown_pct",
          "min_holding_days",
          "number_of_trades",
          "profit_factor",
          "qualified_entry_enabled",
          "qualified_states",
          "relative_stop_enabled",
          "relative_stop_stats",
          "relative_stop_underperform_pct",
          "selected",
          "sharpe_ratio",
          "skip_reasons",
          "status",
          "total_return_pct",
          "variant",
          "win_rate_pct"
        ]
      },
      {
        "list_path": "variant_results.E1_AUDITED_G4_MINHOLD10.strategy_controls.qualified_states",
        "length": 1,
        "keys": []
      },
      {
        "list_path": "variant_results.E1_AUDITED_G4_MINHOLD10.market_entry_gate.blocked_actions",
        "length": 2,
        "keys": []
      },
      {
        "list_path": "variant_results.E1_AUDITED_G4_MINHOLD10.market_entry_gate.unaffected_actions",
        "length": 3,
        "keys": []
      },
      {
        "list_path": "variant_results.E1_AUDITED_G4_MINHOLD10.invalid_trades",
        "length": 0,
        "keys": []
      },
      {
        "list_path": "variant_results.E1_AUDITED_G4_MINHOLD10.equity_curve",
        "length": 131,
        "keys": []
      },
      {
        "list_path": "variant_results.E1_AUDITED_G4_MINHOLD10.spx_curve",
        "length": 131,
        "keys": []
      },
      {
        "list_path": "variant_results.E1_AUDITED_G4_MINHOLD10.daily_records",
        "length": 22,
        "keys": [
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
        "list_path": "variant_results.E1_AUDITED_G4_MINHOLD10.trades",
        "length": 47,
        "keys": [
          "action_count",
          "actions_during_trade",
          "avg_cost",
          "effective_exit",
          "entry_adverse_gap_pct",
          "entry_date",
          "entry_price",
          "entry_signal",
          "execution_model",
          "exit_adverse_gap_pct",
          "exit_date",
          "exit_price",
          "exit_reason",
          "exit_reasons",
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
          "relative_stop_exec_date",
          "relative_stop_triggered",
          "return_pct",
          "size_units_at_exit",
          "symbol",
          "take_profit_exec_date",
          "take_profit_triggered",
          "total_execution_drag_pct"
        ]
      },
      {
        "list_path": "variant_results.E2_DYNAMIC_EXIT_V2.strategy_controls.qualified_states",
        "length": 1,
        "keys": []
      },
      {
        "list_path": "variant_results.E2_DYNAMIC_EXIT_V2.market_entry_gate.blocked_actions",
        "length": 2,
        "keys": []
      },
      {
        "list_path": "variant_results.E2_DYNAMIC_EXIT_V2.market_entry_gate.unaffected_actions",
        "length": 3,
        "keys": []
      },
      {
        "list_path": "variant_results.E2_DYNAMIC_EXIT_V2.invalid_trades",
        "length": 0,
        "keys": []
      },
      {
        "list_path": "variant_results.E2_DYNAMIC_EXIT_V2.equity_curve",
        "length": 131,
        "keys": []
      },
      {
        "list_path": "variant_results.E2_DYNAMIC_EXIT_V2.spx_curve",
        "length": 131,
        "keys": []
      },
      {
        "list_path": "variant_results.E2_DYNAMIC_EXIT_V2.daily_records",
        "length": 22,
        "keys": [
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
        "list_path": "variant_results.E2_DYNAMIC_EXIT_V2.trades",
        "length": 41,
        "keys": [
          "action_count",
          "actions_during_trade",
          "avg_cost",
          "effective_exit",
          "entry_adverse_gap_pct",
          "entry_date",
          "entry_price",
          "entry_signal",
          "execution_model",
          "exit_adverse_gap_pct",
          "exit_date",
          "exit_price",
          "exit_reason",
          "exit_reasons",
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
          "relative_stop_exec_date",
          "relative_stop_triggered",
          "return_pct",
          "size_units_at_exit",
          "symbol",
          "take_profit_exec_date",
          "take_profit_triggered",
          "total_execution_drag_pct"
        ]
      }
    ],
    "exports/e1r_v0_2_backtest_equity_curve.json": [
      {
        "list_path": "rows",
        "length": 8819,
        "keys": [
          "close",
          "date",
          "diagnostic_only",
          "e1r_entry_type",
          "e1r_uptrend_confirmed_eligible",
          "e1r_uptrend_emerging_eligible",
          "equity",
          "leader_rank",
          "leader_score",
          "ma20",
          "ma20_slope",
          "ma50",
          "ma50_slope",
          "momentum_acceleration",
          "momentum_score",
          "reasons",
          "rs_20d_improvement",
          "rs_prev20",
          "rs_score",
          "spx_regime",
          "symbol",
          "trend_health"
        ]
      },
      {
        "list_path": "equity_curve",
        "length": 8819,
        "keys": [
          "close",
          "date",
          "diagnostic_only",
          "e1r_entry_type",
          "e1r_uptrend_confirmed_eligible",
          "e1r_uptrend_emerging_eligible",
          "equity",
          "leader_rank",
          "leader_score",
          "ma20",
          "ma20_slope",
          "ma50",
          "ma50_slope",
          "momentum_acceleration",
          "momentum_score",
          "reasons",
          "rs_20d_improvement",
          "rs_prev20",
          "rs_score",
          "spx_regime",
          "symbol",
          "trend_health"
        ]
      }
    ],
    "data/research/e1r/e1r_formal_backtest_v0_1.json": [
      {
        "list_path": "equi
```

## Top JSON Candidates

- score `68` · `docs/research/E1R_V0_2_STAGE3_8E2F2C4C6_INTERVAL_SCHEMA_SOURCE_AUDIT.json` · hits `core_daily_equity_records, sidecar_records, extract_core_interval_returns, build_equity_records_from_returns, combined_return, sidecar_return, sidecar_return_pct, core_return, core_return_pct, spx_return, spx_return_pct, next_date, daily_records, daily_equity, total_equity, sidecar_active, sidecar_selected_count, sidecar_gross_exposure, sidecar_holdings, MA_CONFLICT, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1`
- score `66` · `docs/research/E1R_V0_2_STAGE3_8E2F2C4C5_EXPORT_WRAPPER_SMOKE_REPORT.json` · hits `core_daily_equity_records, sidecar_records, extract_core_interval_returns, build_equity_records_from_returns, combined_return, sidecar_return, sidecar_return_pct, core_return, core_return_pct, spx_return, spx_return_pct, next_date, daily_records, daily_equity, total_equity, sidecar_active, sidecar_selected_count, sidecar_gross_exposure, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1`
- score `64` · `docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json` · hits `core_daily_equity_records, sidecar_records, extract_core_interval_returns, build_equity_records_from_returns, combined_return, sidecar_return, sidecar_return_pct, core_return, core_return_pct, spx_return, spx_return_pct, next_date, daily_equity, total_equity, sidecar_active, sidecar_selected_count, sidecar_gross_exposure, sidecar_holdings, MA_CONFLICT, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1`
- score `64` · `docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json` · hits `core_daily_equity_records, sidecar_records, extract_core_interval_returns, build_equity_records_from_returns, combined_return, sidecar_return, sidecar_return_pct, core_return, core_return_pct, spx_return, spx_return_pct, next_date, daily_equity, total_equity, sidecar_active, sidecar_selected_count, sidecar_gross_exposure, sidecar_holdings, MA_CONFLICT, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1`
- score `60` · `docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json` · hits `core_daily_equity_records, sidecar_records, build_equity_records_from_returns, combined_return, sidecar_return, core_return, spx_return, spx_return_pct, next_date, daily_equity, total_equity, sidecar_active, sidecar_selected_count, sidecar_gross_exposure, MA_CONFLICT, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1`
- score `56` · `docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json` · hits `core_daily_equity_records, sidecar_records, extract_core_interval_returns, build_equity_records_from_returns, sidecar_return, core_return, spx_return, spx_return_pct, next_date, daily_records, daily_equity, total_equity, sidecar_active, sidecar_selected_count, sidecar_gross_exposure, MA_CONFLICT, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1`
- score `43` · `docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json` · hits `core_daily_equity_records, combined_return, spx_return, spx_return_pct, next_date, daily_records, daily_equity, total_equity, sidecar_active, sidecar_selected_count, MA_CONFLICT, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1`
- score `27` · `docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json` · hits `extract_core_interval_returns, build_equity_records_from_returns, sidecar_return, spx_return, spx_return_pct, next_date, sidecar_active, sidecar_selected_count, MA_CONFLICT, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1`
- score `26` · `docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json` · hits `core_daily_equity_records, extract_core_interval_returns, build_equity_records_from_returns, spx_return, spx_return_pct, daily_records, daily_equity, total_equity, sidecar_active, MA_CONFLICT, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1`
- score `24` · `docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json` · hits `spx_return, spx_return_pct, next_date, daily_records, total_equity, sidecar_active, sidecar_selected_count, MA_CONFLICT, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1`
- score `23` · `docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json` · hits `combined_return, next_date, sidecar_active, sidecar_selected_count, MA_CONFLICT, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1`
- score `20` · `docs/research/E1R_V0_2_STAGE3_8E2F1F0_DAILY_PIPELINE_AUDIT.json` · hits `spx_return, spx_return_pct, next_date, total_equity, sidecar_active, sidecar_selected_count, MA_CONFLICT, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1`
- score `16` · `docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json` · hits `spx_return, spx_return_pct, next_date, sidecar_active, sidecar_selected_count, MA_CONFLICT, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1`
- score `16` · `docs/research/E1R_V0_2_STAGE3_8E2F1E1_TARGET_SOURCE_CONTRACT.json` · hits `spx_return, spx_return_pct, next_date, sidecar_active, sidecar_selected_count, MA_CONFLICT, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1`
- score `14` · `docs/research/E1R_V0_2_STAGE3_8A_DASHBOARD_REFACTOR_AUDIT.json` · hits `spx_return, spx_return_pct, next_date, sidecar_active, sidecar_selected_count, E1R_REGIME_AWARE_V0_1`
- score `14` · `docs/research/E1R_V0_2_STAGE3_8E2F1C_RUNNER_DRY_RUN_AUDIT.json` · hits `next_date, sidecar_active, sidecar_selected_count, MA_CONFLICT, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1`
- score `13` · `docs/research/E1R_V0_2_STAGE3_5_MAIN_SMOKE_TEST_REPORT.json` · hits `spx_return, spx_return_pct, next_date, sidecar_active, sidecar_selected_count`
- score `13` · `docs/research/E1R_V0_2_STAGE3_8E2F2C3FC_E1R_STATUS_TREND_FIELD_AUDIT.json` · hits `next_date, sidecar_active, MA_CONFLICT, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1`
- score `12` · `exports/e1r_v0_2_status.json` · hits `next_date, MA_CONFLICT, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1`
- score `11` · `exports/oos_e1r_v0_2_sidecar.json` · hits `next_date, MA_CONFLICT, E1R_REGIME_AWARE_V0_2`
- score `10` · `docs/research/E1R_V0_2_STAGE3_8E2F2C4C1_5Y_EQUITY_ARTIFACT_AUDIT.json` · hits `spx_return, spx_return_pct, daily_equity, total_equity, sidecar_active, sidecar_selected_count, E1R_REGIME_AWARE_V0_2`

## Next Stage

- `Stage 3.8E-2F-2C-4C-8`: Implement dry-run generation path for 5Y core and sidecar interval records
- Recommended action: Extend scripts/export_canonical_5y_equity_curves.py with --dry-run-generate-intervals. It should call frozen composer/sidecar generation paths, summarize interval counts and final metrics, but still avoid writing canonical exports until validation matches frozen E1R metrics.

