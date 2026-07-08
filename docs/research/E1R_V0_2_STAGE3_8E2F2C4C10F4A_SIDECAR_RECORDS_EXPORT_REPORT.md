# Stage 3.8E-2F-2C-4C-10F-4A Sidecar Records Export Report

Generated At: `2026-07-08T13:03:38.170893+00:00`

## Status

- Status: `E1R_SIDECAR_RECORDS_5Y_NOT_READY`
- Sidecar records written: `False`
- E1R canonical written: `False`

## Interval Stats

```json
{
  "row_count": 1260,
  "date_start": "2021-06-11",
  "date_end": "2026-06-17",
  "unique_dates": 1260,
  "max_rows_per_date": 1,
  "one_row_per_date": true,
  "sample_first": [
    {
      "date": "2021-06-11",
      "next_date": "2021-06-14"
    },
    {
      "date": "2021-06-14",
      "next_date": "2021-06-15"
    },
    {
      "date": "2021-06-15",
      "next_date": "2021-06-16"
    }
  ],
  "sample_last": [
    {
      "date": "2026-06-15",
      "next_date": "2026-06-16"
    },
    {
      "date": "2026-06-16",
      "next_date": "2026-06-17"
    },
    {
      "date": "2026-06-17",
      "next_date": "2026-06-18"
    }
  ]
}
```

## Sidecar Stats

```json
{
  "row_count": 1260,
  "date_start": "2021-06-11",
  "date_end": "2026-06-17",
  "unique_dates": 1260,
  "max_rows_per_date": 1,
  "one_row_per_date": true,
  "regime_counts": {
    "UPTREND": 861,
    "SIDEWAYS": 241,
    "DOWNTREND": 158
  },
  "subclass_counts": {
    "NO_SUBCLASS": 1019,
    "MA_CONFLICT": 135,
    "DETERIORATION_TRANSITION": 63,
    "RECOVERY_TRANSITION": 43
  },
  "active_count": 0,
  "nonzero_sidecar_return_count": 0,
  "sidecar_active_by_regime": {},
  "sidecar_active_by_subclass": {},
  "gross_exposure_min": null,
  "gross_exposure_max": null,
  "selected_count_min": null,
  "selected_count_max": null
}
```

## Validation

```json
{
  "full_intervals_ge_1000": true,
  "sidecar_records_nonempty": true,
  "sidecar_one_row_per_date": true,
  "sidecar_active_count_positive": false,
  "sidecar_active_count_reasonable": false,
  "ma_conflict_active_present": false,
  "canonical_e1r_files_unchanged": true
}
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-4B`: Compose continuous E1R portfolio equity from E1 core + sidecar records
- Recommended action: Use exports/e1_5y_backtest_equity_curve.json and exports/e1r_v0_2_sidecar_records_5y.json to compose full-window E1R equity, then validate frozen metrics before writing canonical E1R export.

