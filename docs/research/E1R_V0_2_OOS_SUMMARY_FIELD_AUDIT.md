# E1R v0.2 OOS Summary Field Audit

Generated At: `2026-07-08T06:14:00.632858+00:00`
HEAD: `0ed55b2`

## Status

- Status: `AUDIT_COMPLETE_NO_SOURCE_CHANGES`
- Source changed: `False`
- Dashboard changed: `False`
- Exports changed: `False`
- Strategy logic changed: `False`

## Question

Does exports/oos_e1r_v0_2_summary.json contain daily forward fields for E1R v0.2?

## Readiness

- Readiness: `HAS_DAILY_FORWARD_FIELDS`
- Reason: Found date fields and numeric forward metrics in candidate summary records.
- Candidate paths: `['$']`

## Target File

- Path: `exports/oos_e1r_v0_2_summary.json`
- Exists: `True`
- Valid JSON: `True`
- Type: `dict`
- Top-level keys: `['generated_at', 'phase', 'strategy_id', 'version', 'research_status', 'status_date', 'market_state', 'regime', 'subclass', 'mutually_exclusive_state_model', 'core_active', 'sidecar_active', 'sidecar_selected_count', 'gross_exposure', 'top_n', 'execution_status', 'equity_status', 'notes']`
- Size bytes: `873`

## Candidate Records in E1R OOS Summary

- path `$` date=True metric=True numeric=True date_fields=`{'status_date': '2026-06-18', 'generated_at': '2026-07-07T23:56:04.521255+00:00'}` forward_fields=`{'gross_exposure': 0.25}`

## Candidate Arrays in E1R OOS Summary


## Cross-check Files

- `e1r_oos_summary` `exports/oos_e1r_v0_2_summary.json` exists=`True` type=`dict` top_keys=`['generated_at', 'phase', 'strategy_id', 'version', 'research_status', 'status_date', 'market_state', 'regime', 'subclass', 'mutually_exclusive_state_model', 'core_active', 'sidecar_active', 'sidecar_selected_count', 'gross_exposure', 'top_n', 'execution_status', 'equity_status', 'notes']`
- `e1r_oos_equity_curve` `exports/oos_e1r_v0_2_equity_curve.json` exists=`True` type=`dict` top_keys=`['generated_at', 'strategy_id', 'phase', 'equity_status', 'execution_status', 'curve_type', 'start_date', 'end_date', 'row_count', 'latest', 'records', 'notes']`
- `e1r_oos_positions` `exports/oos_e1r_v0_2_positions.json` exists=`True` type=`dict` top_keys=`['generated_at', 'phase', 'strategy_id', 'status_date', 'market_state', 'core', 'sidecar']`
- `e1r_oos_orders` `exports/oos_e1r_v0_2_orders.json` exists=`True` type=`dict` top_keys=`['generated_at', 'phase', 'strategy_id', 'status_date', 'market_state', 'execution_status', 'orders']`
- `e1r_status` `exports/e1r_v0_2_status.json` exists=`True` type=`dict` top_keys=`['generated_at', 'strategy_id', 'version', 'research_status', 'status_date', 'e1r_market_state', 'regime', 'subclass', 'mutually_exclusive_state_model', 'core', 'sidecar', 'legacy_market_state', 'source_files', 'notes']`
- `e1_oos_summary` `exports/oos_summary.json` exists=`True` type=`dict` top_keys=`['generated_at', 'generated_at_display', 'status', 'strategy_id', 'oos_start_date', 'run_date', 'last_successful_run', 'last_market_date', 'expected_market_date', 'initial_capital', 'final_equity', 'total_return_pct', 'max_drawdown_pct', 'profit_factor', 'win_rate_pct', 'total_trades', 'open_positions', 'live_event_count', 'backfill_event_count', 'first_review_criteria', 'provenance_note', 'mixed_provenance_positions']`
- `e1_oos_equity_curve` `exports/oos_equity_curve.json` exists=`True` type=`dict` top_keys=`['generated_at', 'generated_at_display', 'strategy_id', 'initial_capital', 'curve']`
- `backtest_summary` `exports/e1r_v0_2_backtest_summary.json` exists=`True` type=`dict` top_keys=`['strategy_id', 'total_return_pct', 'spx_return_pct', 'alpha_pct', 'max_drawdown_pct', 'profit_factor', 'sharpe_ratio', 'research_status', 'regime_aware_logic', 'sidecar_active_days', 'sidecar_active_by_regime', 'sidecar_active_by_subclass', 'composition_exists', 'row_count', 'variant', 'artifact_type', 'source_file', 'source_json_path', 'frozen_artifact', 'regeneration_note']`

## Decision Rules

- `HAS_DAILY_FORWARD_FIELDS`: Dashboard mapping likely needs improvement.
- `HAS_FORWARD_METRICS_BUT_DATE_MAPPING_UNCLEAR`: Dashboard mapping and export schema need alignment.
- `HAS_DAILY_FORWARD_ARRAY_BUT_NOT_SUMMARY_OBJECT`: Dashboard may need to derive latest summary from an array or export should publish a latest object.
- `HAS_DATE_OR_METADATA_ONLY`: Export exists but daily forward metrics are not generated yet.
- `NO_FORWARD_FIELDS_FOUND`: Export does not contain daily forward summary fields.
- `MISSING_EXPORT`: OOS E1R summary export is not generated.

## Top-level Preview

```json
{
  "generated_at": "2026-07-07T23:56:04.521255+00:00",
  "phase": "OOS_STATUS_SIGNAL_ONLY",
  "strategy_id": "E1R_REGIME_AWARE_V0_2",
  "version": "E1R-v0.2-formal-sidecar-sleeve",
  "research_status": "FORMAL_SIDECAR_SLEEVE_ENGINE",
  "status_date": "2026-06-18",
  "market_state": "UPTREND",
  "regime": "UPTREND",
  "subclass": null,
  "mutually_exclusive_state_model": true,
  "core_active": true,
  "sidecar_active": false,
  "sidecar_selected_count": 0,
  "gross_exposure": 0.25,
  "top_n": 10,
  "execution_status": "NO_REAL_EXECUTION",
  "equity_status": "NOT_YET_CONNECTED",
  "notes": [
    "OOS-1 exports daily E1R v0.2 state and sidecar target signals only.",
    "No real orders are executed by this script.",
    "No E1R v0.2 OOS equity curve is updated by this script.",
    "This is the bridge layer for Dashboard and future OOS equity integration."
  ]
}
```

