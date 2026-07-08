# Stage 3.8E-2F-2C-4C-10F-3D-S E1 Export Field Mapping Fix

Generated At: `2026-07-08T12:59:19.002257+00:00`

## Status

- Status: `E1_EXPORT_FIELD_MAPPING_FIX_COMPLETE_NO_BACKTEST`
- Full backtest rerun: `False`
- Canonical E1 rewritten: `False`
- Export script changed: `True`
- Strategy files unchanged: `True`

## Patch Report

```json
{
  "script_changed": true,
  "market_value_mapping_fixed": true,
  "n_positions_mapping_fixed": true
}
```

## Canonical Audit

```json
{
  "canonical_path": "exports/e1_5y_backtest_equity_curve.json",
  "exists": true,
  "row_count": 1259,
  "unique_dates": 1259,
  "date_start": "2021-06-11",
  "date_end": "2026-06-16",
  "one_row_per_date": true,
  "max_rows_per_date": 1,
  "missing_market_value_rows_existing_canonical": 1259,
  "missing_n_positions_rows_existing_canonical": 1259,
  "note": "Existing canonical was not rewritten in this step; missing field counts reflect the already-saved file from 10F-3C."
}
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-4A`: Generate regime-aware E1R sidecar records with explicit 5Y window
- Recommended action: Use saved E1 5Y core equity as input and generate/validate sidecar records before composing E1R.

