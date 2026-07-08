# Stage 3.8E-2F-2C-4C-9 Controlled Long Export Audit

Generated At: `2026-07-08T11:50:00.237489+00:00`

## Status

- Status: `CONTROLLED_LONG_EXPORT_COMPLETE_CANONICAL_EXPORTS_NOT_READY`
- Frozen strategy files unchanged: `True`
- Canonical exports written: `None`

## Diagnosis

- Frozen strategy files unchanged: True.
- Commands run: 2.
- E1 candidate accepted: False.
- E1R candidate accepted: False.
- E1R metric validation passed: False.
- Canonical exports written: 0.
- Canonical comparison not ready. Existing frozen export path still does not produce one-row-per-date E1R portfolio equity.
- Next step should call the frozen E1R sidecar/composer generation path directly, rather than reusing diagnostic rows.

## Commands

- `['/Library/Developer/CommandLineTools/usr/bin/python3', 'src/engine/backtest.py']` returncode `1` ok `False`
- `['/Library/Developer/CommandLineTools/usr/bin/python3', 'scripts/export_e1r_v0_2_backtest_equity.py']` returncode `1` ok `False`

## E1 Candidate Eval

```json
{
  "reason": "no 5Y one-row-per-date E1 daily_records",
  "evaluated": [
    {
      "source": "daily_records",
      "rows": 22,
      "date_summary": {
        "start": "2023-11-06",
        "end": "2026-05-13",
        "unique_dates": 22,
        "max_rows_per_date": 1
      },
      "accepted": false
    },
    {
      "source": "variant_results.E1_AUDITED_G4_MINHOLD10.daily_records",
      "rows": 22,
      "date_summary": {
        "start": "2023-11-06",
        "end": "2026-05-13",
        "unique_dates": 22,
        "max_rows_per_date": 1
      },
      "accepted": false
    },
    {
      "source": "variant_results.E2_DYNAMIC_EXIT_V2.daily_records",
      "rows": 22,
      "date_summary": {
        "start": "2023-11-06",
        "end": "2026-05-13",
        "unique_dates": 22,
        "max_rows_per_date": 1
      },
      "accepted": false
    }
  ]
}
```

## E1R Candidate Eval

```json
{
  "reason": "E1R output is diagnostic/symbol-level, not portfolio-level",
  "source_key": "rows",
  "row_count": 8819,
  "date_summary": {
    "start": "2021-06-11",
    "end": "2026-06-16",
    "unique_dates": 859,
    "max_rows_per_date": 19
  },
  "sample_keys": [
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
```

## E1R Metric Validation

```json
{
  "ok": false,
  "reason": "missing E1R candidate"
}
```

## Canonical Skipped

```json
[
  {
    "path": "exports/e1_5y_backtest_equity_curve.json",
    "reason": {
      "reason": "no 5Y one-row-per-date E1 daily_records",
      "evaluated": [
        {
          "source": "daily_records",
          "rows": 22,
          "date_summary": {
            "start": "2023-11-06",
            "end": "2026-05-13",
            "unique_dates": 22,
            "max_rows_per_date": 1
          },
          "accepted": false
        },
        {
          "source": "variant_results.E1_AUDITED_G4_MINHOLD10.daily_records",
          "rows": 22,
          "date_summary": {
            "start": "2023-11-06",
            "end": "2026-05-13",
            "unique_dates": 22,
            "max_rows_per_date": 1
          },
          "accepted": false
        },
        {
          "source": "variant_results.E2_DYNAMIC_EXIT_V2.daily_records",
          "rows": 22,
          "date_summary": {
            "start": "2023-11-06",
            "end": "2026-05-13",
            "unique_dates": 22,
            "max_rows_per_date": 1
          },
          "accepted": false
        }
      ]
    }
  },
  {
    "path": "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
    "reason": {
      "reason": "E1R output is diagnostic/symbol-level, not portfolio-level",
      "source_key": "rows",
      "row_count": 8819,
      "date_summary": {
        "start": "2021-06-11",
        "end": "2026-06-16",
        "unique_dates": 859,
        "max_rows_per_date": 19
      },
      "sample_keys": [
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
    "metric_validation": {
      "ok": false,
      "reason": "missing E1R candidate"
    }
  },
  {
    "path": "exports/e1_e1r_5y_equity_comparison.json",
    "reason": "requires accepted E1 and validated E1R"
  }
]
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10`: Implement direct frozen E1R portfolio-equity generator
- Recommended action: Call e1r_sidecar_sleeve/e1r_composer generation directly to create 5Y sidecar_records and interval_records in memory, then export only after frozen metrics match.

