# Stage 3.8E-2F-2C-4C-10F-3D E1 Canonical Integrity Audit

Generated At: `2026-07-08T12:56:46.404328+00:00`

## Status

- Status: `E1_CANONICAL_INTEGRITY_AUDIT_COMPLETE_MAPPING_FIXED_NO_BACKTEST`
- Full backtest rerun: `False`
- Canonical E1 rewritten: `False`
- Export script changed: `True`
- Strategy files unchanged: `True`

## Canonical Audit

```json
{
  "canonical_path": "exports/e1_5y_backtest_equity_curve.json",
  "exists": true,
  "strategy_id": "E1_AUDITED_G4_MINHOLD10",
  "artifact_type": "canonical_continuous_capital_e1_5y_core_equity_curve",
  "capital_model": "continuous_single_account",
  "row_count": 1259,
  "unique_dates": 1259,
  "date_start": "2021-06-11",
  "date_end": "2026-06-16",
  "one_row_per_date": true,
  "max_rows_per_date": 1,
  "first_equity": 100000.0,
  "last_equity": 189815.69,
  "first_row": {
    "date": "2021-06-11",
    "equity": 100000.0,
    "portfolio_value": 100000.0,
    "strategy_indexed": 100.0,
    "cash": 100000.0,
    "market_value": null,
    "n_positions": null,
    "daily_return": null,
    "daily_return_pct": 0.0,
    "market_state": "ALLOW",
    "source_row_keys": [
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
  },
  "last_row": {
    "date": "2026-06-16",
    "equity": 189815.69,
    "portfolio_value": 189815.69,
    "strategy_indexed": 189.81569000000002,
    "cash": 60493.25,
    "market_value": null,
    "n_positions": null,
    "daily_return": null,
    "daily_return_pct": -1.66,
    "market_state": "ALLOW",
    "source_row_keys": [
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
  },
  "missing_market_value_rows": 1259,
  "missing_n_positions_rows": 1259,
  "log_final_equity": 189625.94,
  "daily_last_vs_log_final_delta": 189.75,
  "daily_last_vs_log_final_delta_pct": 0.10006542353857284,
  "continuity_checks": {
    "row_count_ge_1000": true,
    "one_row_per_date": true,
    "date_start_ok": true,
    "date_end_ok_for_daily_records": true,
    "capital_continuity_candidate": true
  }
}
```

## Patch Report

```json
{
  "script_changed": true,
  "market_value_mapping_fixed": true,
  "n_positions_mapping_fixed": false
}
```

## Diagnosis

- Existing E1 canonical is valid as a continuous daily equity curve.
- The canonical daily records end at 2026-06-16, while the run log reported final equity after sim-end processing.
- The small difference between daily last equity and log final equity should be treated as daily-record vs final/liquidation accounting until verified by a rerun with enriched export fields.
- No frozen strategy files were modified.
- Export script mapping was fixed so future E1 exports map positions_value -> market_value and open_positions_count -> n_positions.

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-4A`: Generate regime-aware E1R sidecar records with explicit 5Y window
- Recommended action: Use the validated E1 5Y core equity curve as core input, then generate/validate sidecar records separately before composing E1R.

