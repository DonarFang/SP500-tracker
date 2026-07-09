# Stage 3.8E-2F-2C-4C-10F-4B-0N Research Curve Bundle

Generated At: `2026-07-09T11:02:16.774285+00:00`

## Status

- Status: `E1_E1R_RESEARCH_CURVE_BUNDLE_COMPLETE_NONCANONICAL`
- Dashboard changed: `False`
- E1R canonical written: `False`
- Research bundle written: `True`

## Bundle

- `exports/e1_e1r_research_curve_bundle_noncanonical.json`

## Summaries

```json
{
  "e1_5y_canonical": {
    "row_count": 1259,
    "date_start": "2021-06-11",
    "date_end": "2026-06-16",
    "first_equity": 100000.0,
    "last_equity": 189815.69,
    "total_return_pct": 89.81569
  },
  "e1r_5y_direct_composed_candidate": {
    "row_count": 1258,
    "date_start": "2021-06-14",
    "date_end": "2026-06-16",
    "first_equity": 99900.4,
    "last_equity": 189817.146545481,
    "total_return_pct": 90.00639291282218
  },
  "e1_forward_oos": {
    "row_count": 13,
    "date_start": "2026-06-18",
    "date_end": "2026-07-08",
    "first_equity": 100000.0,
    "last_equity": 75599.98,
    "total_return_pct": -24.40002
  },
  "e1r_forward_oos_kickoff_ready": {
    "row_count": 1,
    "date_start": "2026-06-18",
    "date_end": "2026-06-18",
    "first_equity": 100000.0,
    "last_equity": 100000.0,
    "total_return_pct": 0.0
  }
}
```

## Validations

```json
{
  "e1_5y_rows_ge_1000": true,
  "e1r_5y_candidate_rows_ge_1000": true,
  "e1_oos_exists": true,
  "e1r_oos_exists": true,
  "official_e1r_canonical_absent": true,
  "bundle_noncanonical": true
}
```

## Conclusion

- `RESEARCH_CURVE_BUNDLE_READY_FOR_DASHBOARD_CANDIDATE_WIRING`
- Recommended: Wire this bundle into dashboard under Research/Candidate labels only; do not label E1R as frozen official.

