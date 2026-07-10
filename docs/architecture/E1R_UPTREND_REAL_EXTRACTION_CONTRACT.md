# E1R 4C-2C-4E-ENGINE-K — UPTREND Real Extraction Boundary

Generated At: `2026-07-10T11:34:27.838833+00:00`

## Purpose
Replace replay-only skeleton with first real extraction boundary from legacy run_stateful_simulation result into new UptrendCore comparable schema.

## Policy
```json
{
  "strategy_logic_changed": false,
  "actual_strategy_logic_extracted": true,
  "strategy_decisions_generated_by_new_core": false,
  "short_window_existing_engine_run": true,
  "backtest_engine_run_short_window_once": true,
  "full_5y_backtest_run": false,
  "forward_runner_run": false,
  "provider_extraction_run": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "frozen_strategy_files_changed": false,
  "invalid_artifacts_used_as_source": false,
  "composer_used": false,
  "return_curve_stitching_used": false
}
```

## Legacy Summary
```json
{
  "status": "INSUFFICIENT_SAMPLE",
  "version": "v1.6-top3-rs-minhold-relstop",
  "strategy_variant": "top3_entry_rs_minhold_relstop",
  "daily_equity_record_count": 62,
  "number_of_trades": 3,
  "final_equity": 71746.21,
  "total_return_pct": -28.25,
  "e1r_uptrend_execution_enabled": false
}
```

## Equivalence Report
```json
{
  "ok": true,
  "checked_assertions": [
    "daily_account_date_sequence",
    "daily_total_equity_cash_positions",
    "daily_open_positions_count",
    "daily_market_gate_state",
    "daily_spx_regime",
    "trade_lifecycle_symbol_dates",
    "trade_signals_and_reasons"
  ],
  "mismatch_count": 0,
  "mismatches": [],
  "summary": {
    "expected_daily_rows": 62,
    "actual_daily_rows": 62,
    "expected_trades": 3,
    "actual_trades": 3,
    "money_abs_tol": 0.01,
    "pct_abs_tol": 0.01
  }
}
```

## Validations
```json
{
  "real_extraction_boundary_defined": true,
  "legacy_result_extraction_used": true,
  "golden_master_replay_skeleton_only": false,
  "actual_strategy_logic_extracted": true,
  "strategy_decisions_generated_by_new_core": false,
  "strategy_logic_changed": false,
  "short_window_existing_engine_run": true,
  "backtest_engine_run_short_window_once": true,
  "full_5y_backtest_run": false,
  "forward_runner_run": false,
  "provider_extraction_run": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "strategy_files_unchanged": true,
  "invalid_artifacts_not_used_as_source": true,
  "composer_not_used": true,
  "return_curve_stitching_used": false,
  "engine_g_loaded": true,
  "engine_h_loaded": true,
  "engine_i_loaded": true,
  "engine_j_loaded": true,
  "historical_adapter_bundle_loaded": true,
  "short_window_days_le_90": true,
  "extracted_result_written": true,
  "equivalence_report_written": true,
  "equivalence_passed_against_engine_g": true,
  "mismatch_count": 0,
  "checked_assertion_count": 7,
  "daily_rows_compared": 62,
  "trades_compared": 3,
  "max_positions_contract_observed": true
}
```

## Decision
```json
{
  "uptrend_real_extraction_passed": true,
  "equivalence_passed_against_engine_g": true,
  "checked_assertions": [
    "daily_account_date_sequence",
    "daily_total_equity_cash_positions",
    "daily_open_positions_count",
    "daily_market_gate_state",
    "daily_spx_regime",
    "trade_lifecycle_symbol_dates",
    "trade_signals_and_reasons"
  ],
  "mismatch_count": 0,
  "current_extraction_level": "legacy_result_to_new_uptrend_core_schema",
  "remaining_for_true_standalone_uptrend_core": [
    "Move market gate calculation from legacy monolith into new core.",
    "Move candidate generation/ranking from legacy monolith into new core.",
    "Move BUY/ADD/REDUCE/EXIT generation from legacy monolith into new core.",
    "Move accounting execution from legacy monolith into adapter-backed engine flow.",
    "Tighten equivalence after each extracted unit."
  ],
  "sideways_branch_implementation_allowed_now": false,
  "full_5y_backtest_allowed_now": false,
  "forward_runner_allowed_now": false,
  "recommended_next_stage": "4C-2C-4E-ENGINE-K2",
  "conclusion": "UPTREND_REAL_EXTRACTION_BOUNDARY_PASS_READY_FOR_UNIT_EXTRACTION_K2",
  "recommended_next_action": "Proceed to 4C-2C-4E-ENGINE-K2: extract the first standalone unit, market_gate_state, then compare against ENGINE-G/H assertions. Do not extract candidate/BUY logic yet.",
  "engineering_rule": "ENGINE-K establishes the real legacy-result extraction boundary. Do not claim full standalone UPTREND strategy core until market gate, candidate generation, order generation, and accounting are each extracted and equivalence-tested."
}
```
