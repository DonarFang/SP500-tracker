# E1R Combined 5Y — 4C-2C-4C No-Strategy-Change Adapter Smoke

Generated At: `2026-07-09T13:02:52.879275+00:00`
Elapsed Seconds: `0.039062`

## Policy
```json
{
  "strategy_logic_changed": false,
  "backtest_engine_run": false,
  "dashboard_changed": false,
  "official_result_generated": false,
  "purpose": "Smoke original sidecar entrypoint and validate adapter guards before full 5Y rerun."
}
```

## Contract
```json
{
  "UPTREND": "Use previously validated UPTREND strategy. Do not replace logic.",
  "SIDEWAYS_MA_CONFLICT": "Use previously validated sidecar strategy.",
  "DETERIORATION_RECOVERY": "Participate only if original sidecar proves participation; otherwise cash/defensive.",
  "DOWNTREND": "Cash/defensive.",
  "GLOBAL_POSITION_CAP": "Actual account live holdings must always be <= 3 stocks.",
  "SIDEWAYS_TOP10": "Candidate pool only, not live 10-stock account holdings.",
  "NO_STRATEGY_CHANGE": true
}
```

## Sidecar Summary
```json
null
```

## Core Candidates
```json
[
  {
    "path": "exports/portfolio_backtest.json",
    "exists": true,
    "json_ok": true,
    "top_keys": [
      "alpha_pct",
      "avg_execution_drag_pct",
      "avg_holding_days",
      "avg_loser_pct",
      "avg_winner_pct",
      "cagr_pct",
      "comparison",
      "daily_records",
      "entry_top_n",
      "executed_exit_reason_distribution",
      "executed_reduce_reason_distribution",
      "execution_model",
      "exposure_pct",
      "final_equity",
      "generated_at",
      "generated_at_display",
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
      "period_comparison",
      "portfolio_action_distribution",
      "profit_factor",
      "rank_based_exit",
      "sample_validity",
      "selected_variant",
      "selection_policy",
      "sharpe_ratio",
      "skipped_orders_by_reason",
      "spx_cagr_pct",
      "spx_total_return_pct",
      "status",
      "strategy_controls",
      "strategy_variant",
      "total_return_pct",
      "total_trades_all",
      "variant_results",
      "version",
      "win_rate_pct"
    ],
    "strategy_variant": "E1_audited_g4_minhold10",
    "status": "PARTIAL",
    "version": "v1.6-ls60-mode-comparison",
    "total_return_pct": 7.52,
    "spx_total_return_pct": 69.36,
    "daily_records_count": 22,
    "daily_equity_records_count": null
  },
  {
    "path": "exports/e1r_unified_5y_full_account_v1_result.json",
    "exists": true,
    "json_ok": true,
    "top_keys": [
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
    "strategy_variant": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1",
    "status": "INVALID",
    "version": "v1.6-top3-rs-minhold-relstop",
    "total_return_pct": -100.0,
    "spx_total_return_pct": 76.84,
    "daily_records_count": 41,
    "daily_equity_records_count": 1259
  },
  {
    "path": "exports/e1r_unified_5y_dashboard_research_bundle.json",
    "exists": true,
    "json_ok": true,
    "top_keys": [
      "artifact_type",
      "curve",
      "display_scope",
      "do_not_use",
      "generated_at",
      "metric_source",
      "metrics",
      "regime_summary",
      "source_files",
      "status",
      "strategy_id",
      "validation",
      "warnings"
    ],
    "strategy_variant": null,
    "status": "DASHBOARD_RESEARCH_BUNDLE_READY_ACCOUNT_LEVEL_ONLY",
    "version": null,
    "total_return_pct": null,
    "spx_total_return_pct": null,
    "daily_records_count": null,
    "daily_equity_records_count": null,
    "curve_rows_count": 1259
  },
  {
    "path": "exports/e1r_unified_5y_full_account_v1_row_derived_summary.json",
    "exists": true,
    "json_ok": true,
    "top_keys": [
      "artifact_type",
      "engine_reported_metrics_rejected",
      "generated_at",
      "metric_consistency_diagnosis",
      "next_action",
      "row_derived_metrics",
      "sample_validity_from_engine",
      "source_metric_audit",
      "source_raw_summary",
      "source_result",
      "status",
      "strategy_id",
      "trade_layer_audit",
      "validation"
    ],
    "strategy_variant": null,
    "status": "ROW_DERIVED_ACCOUNT_METRICS_VALIDATED_TRADE_METRICS_NOT_VALIDATED",
    "version": null,
    "total_return_pct": null,
    "spx_total_return_pct": null,
    "daily_records_count": null,
    "daily_equity_records_count": null
  }
]
```

## Validations
```json
{
  "strategy_files_unchanged": true,
  "no_backtest_engine_run": true,
  "sidecar_function_called": false,
  "sidecar_function_ok": false,
  "sidecar_has_records": false,
  "sidecar_active_only_sideways": false,
  "sidecar_active_only_ma_conflict": false,
  "deterioration_recovery_not_active": false,
  "top10_candidate_pool_observed": false,
  "global_live_position_cap_guard_required": true
}
```

## Conclusion
- `SIDECAR_ENTRYPOINT_SMOKE_NEEDS_REVIEW_BEFORE_FULL_RUN`
- Recommended: Do not run full 5Y yet. Review failed validations and source report.

