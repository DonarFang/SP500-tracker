# Stage 3.8E-2F-2C-4C-10F-4B-0F-v2 E1R Daily-like Candidate Rejection Audit

Generated At: `2026-07-09T10:26:03.196664+00:00`

## Status

- Status: `E1R_DAILY_LIKE_CANDIDATE_REJECTION_AUDIT_COMPLETE_NO_CANDIDATE_EXTRACTED`
- Candidate extracted: `False`
- E1R canonical written: `False`
- Strategy files unchanged: `True`
- Canonical existence unchanged after restore: `True`
- Invalid 4B-0F files absent after: `True`

## Summary

```json
{
  "daily_like_candidate_count": 4,
  "accepted_candidate_count": 0,
  "rejected_candidate_count": 4,
  "metric_node_count": 3,
  "exact_metric_node_count": 1
}
```

## Conclusion

- `NO_ACCEPTABLE_PORTFOLIO_DAILY_EQUITY_CANDIDATE_FOUND`
- Recommended: Do not promote any daily-like output. Next step should inspect source code around export_canonical_5y_equity_curves.py and composer return values, not persisted diagnostic rows.

## Hard Filters

- reject if diagnostic_only == true
- reject if row contains symbol/ticker
- reject if max_rows_per_date > 1
- reject if one_row_per_date != true
- reject if total_return diff from frozen > 1.0 pct
- reject if maxDD diff from frozen > 1.5 pct

## Rejected Candidates

```json
[
  {
    "source_file": "exports/e1r_v0_2_backtest_equity_curve.json",
    "json_path": "$.rows",
    "list_key": "rows",
    "stats": {
      "row_count": 8819,
      "parseable_equity_rows": 8819,
      "unique_dates": 859,
      "date_start": "2021-06-11",
      "date_end": "2026-06-16",
      "max_rows_per_date": 19,
      "one_row_per_date": false,
      "symbol_row_count": 8819,
      "diagnostic_only_row_count": 8819,
      "symbol_row_pct": 1.0,
      "diagnostic_only_row_pct": 1.0,
      "equity_key_counter": {
        "equity": 8819
      },
      "first_equity": 541.26,
      "last_equity": 227.18,
      "total_return_pct_from_rows": -58.027565310571624,
      "total_return_abs_diff_vs_frozen": 174.77116522404722,
      "max_drawdown_pct_from_rows": 99.94945853241056,
      "maxdd_abs_diff_vs_frozen": 74.04464916959546,
      "first_row_keys": [
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
      ],
      "first_row_sample": {
        "date": "2021-06-11",
        "symbol": "ADBE",
        "spx_regime": "UPTREND",
        "e1r_entry_type": "E1R_UPTREND_EMERGING",
        "e1r_uptrend_emerging_eligible": true,
        "e1r_uptrend_confirmed_eligible": false,
        "leader_rank": 14,
        "leader_score": 90.88,
        "rs_score": 89.0,
        "rs_prev20": 18.6,
        "rs_20d_improvement": 70.4,
        "momentum_score": 93.0,
        "momentum_acceleration": 41.0,
        "trend_health": 90.9,
        "close": 541.26,
        "ma20": 501.12,
        "ma50": 501.37,
        "ma20_slope": 0.002536,
        "ma50_slope": 0.002011,
        "reasons": [
          "rs_above_80",
          "rs_20d_improvement_above_10",
          "momentum_above_70",
          "momentum_acceleration_positive",
          "trend_health_above_65",
          "close_above_ma20",
          "ma20_structure_positive",
          "leader_rank_top20"
        ],
        "diagnostic_only": true,
        "equity": 541.26
      },
      "last_row_sample": {
        "date": "2026-06-16",
        "symbol": "WSM",
        "spx_regime": "UPTREND",
        "e1r_entry_type": "E1R_UPTREND_EMERGING",
        "e1r_uptrend_emerging_eligible": true,
        "e1r_uptrend_confirmed_eligible": false,
        "leader_rank": 19,
        "leader_score": 91.06,
        "rs_score": 83.9,
        "rs_prev20": 10.8,
        "rs_20d_improvement": 73.1,
        "momentum_score": 100.0,
        "momentum_acceleration": 27.9,
        "trend_health": 90.0,
        "close": 227.18,
        "ma20": 204.43,
        "ma50": 193.01,
        "ma20_slope": 0.009685,
        "ma50_slope": 0.00366,
        "reasons": [
          "rs_above_80",
          "rs_20d_improvement_above_10",
          "momentum_above_70",
          "momentum_acceleration_positive",
          "trend_health_above_65",
          "close_above_ma20",
          "ma20_structure_positive",
          "leader_rank_top20"
        ],
        "diagnostic_only": true,
        "equity": 227.18
      }
    },
    "validation": {
      "checks": {
        "row_count_ge_1000": true,
        "one_row_per_date": false,
        "not_symbol_level": false,
        "not_diagnostic_only": false,
        "max_rows_per_date_eq_1": false,
        "total_return_close_to_frozen_1pct": false,
        "maxdd_close_to_frozen_1_5pct": false
      },
      "accepted_as_portfolio_daily_equity": false,
      "rejection_reasons": [
        "one_row_per_date",
        "not_symbol_level",
        "not_diagnostic_only",
        "max_rows_per_date_eq_1",
        "total_return_close_to_frozen_1pct",
        "maxdd_close_to_frozen_1_5pct"
      ]
    }
  },
  {
    "source_file": "exports/e1r_v0_2_backtest_equity_curve.json",
    "json_path": "$.equity_curve",
    "list_key": "equity_curve",
    "stats": {
      "row_count": 8819,
      "parseable_equity_rows": 8819,
      "unique_dates": 859,
      "date_start": "2021-06-11",
      "date_end": "2026-06-16",
      "max_rows_per_date": 19,
      "one_row_per_date": false,
      "symbol_row_count": 8819,
      "diagnostic_only_row_count": 8819,
      "symbol_row_pct": 1.0,
      "diagnostic_only_row_pct": 1.0,
      "equity_key_counter": {
        "equity": 8819
      },
      "first_equity": 541.26,
      "last_equity": 227.18,
      "total_return_pct_from_rows": -58.027565310571624,
      "total_return_abs_diff_vs_frozen": 174.77116522404722,
      "max_drawdown_pct_from_rows": 99.94945853241056,
      "maxdd_abs_diff_vs_frozen": 74.04464916959546,
      "first_row_keys": [
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
      ],
      "first_row_sample": {
        "date": "2021-06-11",
        "symbol": "ADBE",
        "spx_regime": "UPTREND",
        "e1r_entry_type": "E1R_UPTREND_EMERGING",
        "e1r_uptrend_emerging_eligible": true,
        "e1r_uptrend_confirmed_eligible": false,
        "leader_rank": 14,
        "leader_score": 90.88,
        "rs_score": 89.0,
        "rs_prev20": 18.6,
        "rs_20d_improvement": 70.4,
        "momentum_score": 93.0,
        "momentum_acceleration": 41.0,
        "trend_health": 90.9,
        "close": 541.26,
        "ma20": 501.12,
        "ma50": 501.37,
        "ma20_slope": 0.002536,
        "ma50_slope": 0.002011,
        "reasons": [
          "rs_above_80",
          "rs_20d_improvement_above_10",
          "momentum_above_70",
          "momentum_acceleration_positive",
          "trend_health_above_65",
          "close_above_ma20",
          "ma20_structure_positive",
          "leader_rank_top20"
        ],
        "diagnostic_only": true,
        "equity": 541.26
      },
      "last_row_sample": {
        "date": "2026-06-16",
        "symbol": "WSM",
        "spx_regime": "UPTREND",
        "e1r_entry_type": "E1R_UPTREND_EMERGING",
        "e1r_uptrend_emerging_eligible": true,
        "e1r_uptrend_confirmed_eligible": false,
        "leader_rank": 19,
        "leader_score": 91.06,
        "rs_score": 83.9,
        "rs_prev20": 10.8,
        "rs_20d_improvement": 73.1,
        "momentum_score": 100.0,
        "momentum_acceleration": 27.9,
        "trend_health": 90.0,
        "close": 227.18,
        "ma20": 204.43,
        "ma50": 193.01,
        "ma20_slope": 0.009685,
        "ma50_slope": 0.00366,
        "reasons": [
          "rs_above_80",
          "rs_20d_improvement_above_10",
          "momentum_above_70",
          "momentum_acceleration_positive",
          "trend_health_above_65",
          "close_above_ma20",
          "ma20_structure_positive",
          "leader_rank_top20"
        ],
        "diagnostic_only": true,
        "equity": 227.18
      }
    },
    "validation": {
      "checks": {
        "row_count_ge_1000": true,
        "one_row_per_date": false,
        "not_symbol_level": false,
        "not_diagnostic_only": false,
        "max_rows_per_date_eq_1": false,
        "total_return_close_to_frozen_1pct": false,
        "maxdd_close_to_frozen_1_5pct": false
      },
      "accepted_as_portfolio_daily_equity": false,
      "rejection_reasons": [
        "one_row_per_date",
        "not_symbol_level",
        "not_diagnostic_only",
        "max_rows_per_date_eq_1",
        "total_return_close_to_frozen_1pct",
        "maxdd_close_to_frozen_1_5pct"
      ]
    }
  },
  {
    "source_file": "exports/e1r_v0_2_backtest_equity_curve.json",
    "json_path": "$.rows",
    "list_key": null,
    "stats": {
      "row_count": 8819,
      "parseable_equity_rows": 8819,
      "unique_dates": 859,
      "date_start": "2021-06-11",
      "date_end": "2026-06-16",
      "max_rows_per_date": 19,
      "one_row_per_date": false,
      "symbol_row_count": 8819,
      "diagnostic_only_row_count": 8819,
      "symbol_row_pct": 1.0,
      "diagnostic_only_row_pct": 1.0,
      "equity_key_counter": {
        "equity": 8819
      },
      "first_equity": 541.26,
      "last_equity": 227.18,
      "total_return_pct_from_rows": -58.027565310571624,
      "total_return_abs_diff_vs_frozen": 174.77116522404722,
      "max_drawdown_pct_from_rows": 99.94945853241056,
      "maxdd_abs_diff_vs_frozen": 74.04464916959546,
      "first_row_keys": [
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
      ],
      "first_row_sample": {
        "date": "2021-06-11",
        "symbol": "ADBE",
        "spx_regime": "UPTREND",
        "e1r_entry_type": "E1R_UPTREND_EMERGING",
        "e1r_uptrend_emerging_eligible": true,
        "e1r_uptrend_confirmed_eligible": false,
        "leader_rank": 14,
        "leader_score": 90.88,
        "rs_score": 89.0,
        "rs_prev20": 18.6,
        "rs_20d_improvement": 70.4,
        "momentum_score": 93.0,
        "momentum_acceleration": 41.0,
        "trend_health": 90.9,
        "close": 541.26,
        "ma20": 501.12,
        "ma50": 501.37,
        "ma20_slope": 0.002536,
        "ma50_slope": 0.002011,
        "reasons": [
          "rs_above_80",
          "rs_20d_improvement_above_10",
          "momentum_above_70",
          "momentum_acceleration_positive",
          "trend_health_above_65",
          "close_above_ma20",
          "ma20_structure_positive",
          "leader_rank_top20"
        ],
        "diagnostic_only": true,
        "equity": 541.26
      },
      "last_row_sample": {
        "date": "2026-06-16",
        "symbol": "WSM",
        "spx_regime": "UPTREND",
        "e1r_entry_type": "E1R_UPTREND_EMERGING",
        "e1r_uptrend_emerging_eligible": true,
        "e1r_uptrend_confirmed_eligible": false,
        "leader_rank": 19,
        "leader_score": 91.06,
        "rs_score": 83.9,
        "rs_prev20": 10.8,
        "rs_20d_improvement": 73.1,
        "momentum_score": 100.0,
        "momentum_acceleration": 27.9,
        "trend_health": 90.0,
        "close": 227.18,
        "ma20": 204.43,
        "ma50": 193.01,
        "ma20_slope": 0.009685,
        "ma50_slope": 0.00366,
        "reasons": [
          "rs_above_80",
          "rs_20d_improvement_above_10",
          "momentum_above_70",
          "momentum_acceleration_positive",
          "trend_health_above_65",
          "close_above_ma20",
          "ma20_structure_positive",
          "leader_rank_top20"
        ],
        "diagnostic_only": true,
        "equity": 227.18
      }
    },
    "validation": {
      "checks": {
        "row_count_ge_1000": true,
        "one_row_per_date": false,
        "not_symbol_level": false,
        "not_diagnostic_only": false,
        "max_rows_per_date_eq_1": false,
        "total_return_close_to_frozen_1pct": false,
        "maxdd_close_to_frozen_1_5pct": false
      },
      "accepted_as_portfolio_daily_equity": false,
      "rejection_reasons": [
        "one_row_per_date",
        "not_symbol_level",
        "not_diagnostic_only",
        "max_rows_per_date_eq_1",
        "total_return_close_to_frozen_1pct",
        "maxdd_close_to_frozen_1_5pct"
      ]
    }
  },
  {
    "source_file": "exports/e1r_v0_2_backtest_equity_curve.json",
    "json_path": "$.equity_curve",
    "list_key": null,
    "stats": {
      "row_count": 8819,
      "parseable_equity_rows": 8819,
      "unique_dates": 859,
      "date_start": "2021-06-11",
      "date_end": "2026-06-16",
      "max_rows_per_date": 19,
      "one_row_per_date": false,
      "symbol_row_count": 8819,
      "diagnostic_only_row_count": 8819,
      "symbol_row_pct": 1.0,
      "diagnostic_only_row_pct": 1.0,
      "equity_key_counter": {
        "equity": 8819
      },
      "first_equity": 541.26,
      "last_equity": 227.18,
      "total_return_pct_from_rows": -58.027565310571624,
      "total_return_abs_diff_vs_frozen": 174.77116522404722,
      "max_drawdown_pct_from_rows": 99.94945853241056,
      "maxdd_abs_diff_vs_frozen": 74.04464916959546,
      "first_row_keys": [
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
      ],
      "first_row_sample": {
        "date": "2021-06-11",
        "symbol": "ADBE",
        "spx_regime": "UPTREND",
        "e1r_entry_type": "E1R_UPTREND_EMERGING",
        "e1r_uptrend_emerging_eligible": true,
        "e1r_uptrend_confirmed_eligible": false,
        "leader_rank": 14,
        "leader_score": 90.88,
        "rs_score": 89.0,
        "rs_prev20": 18.6,
        "rs_20d_improvement": 70.4,
        "momentum_score": 93.0,
        "momentum_acceleration": 41.0,
        "trend_health": 90.9,
        "close": 541.26,
        "ma20": 501.12,
        "ma50": 501.37,
        "ma20_slope": 0.002536,
        "ma50_slope": 0.002011,
        "reasons": [
          "rs_above_80",
          "rs_20d_improvement_above_10",
          "momentum_above_70",
          "momentum_acceleration_positive",
          "trend_health_above_65",
          "close_above_ma20",
          "ma20_structure_positive",
          "leader_rank_top20"
        ],
        "diagnostic_only": true,
        "equity": 541.26
      },
      "last_row_sample": {
        "date": "2026-06-16",
        "symbol": "WSM",
        "spx_regime": "UPTREND",
        "e1r_entry_type": "E1R_UPTREND_EMERGING",
        "e1r_uptrend_emerging_eligible": true,
        "e1r_uptrend_confirmed_eligible": false,
        "leader_rank": 19,
        "leader_score": 91.06,
        "rs_score": 83.9,
        "rs_prev20": 10.8,
        "rs_20d_improvement": 73.1,
        "momentum_score": 100.0,
        "momentum_acceleration": 27.9,
        "trend_health": 90.0,
        "close": 227.18,
        "ma20": 204.43,
        "ma50": 193.01,
        "ma20_slope": 0.009685,
        "ma50_slope": 0.00366,
        "reasons": [
          "rs_above_80",
          "rs_20d_improvement_above_10",
          "momentum_above_70",
          "momentum_acceleration_positive",
          "trend_health_above_65",
          "close_above_ma20",
          "ma20_structure_positive",
          "leader_rank_top20"
        ],
        "diagnostic_only": true,
        "equity": 227.18
      }
    },
    "validation": {
      "checks": {
        "row_count_ge_1000": true,
        "one_row_per_date": false,
        "not_symbol_level": false,
        "not_diagnostic_only": false,
        "max_rows_per_date_eq_1": false,
        "total_return_close_to_frozen_1pct": false,
        "maxdd_close_to_frozen_1_5pct": false
      },
      "accepted_as_portfolio_daily_equity": false,
      "rejection_reasons": [
        "one_row_per_date",
        "not_symbol_level",
        "not_diagnostic_only",
        "max_rows_per_date_eq_1",
        "total_return_close_to_frozen_1pct",
        "maxdd_close_to_frozen_1_5pct"
      ]
    }
  }
]
```

## Accepted Candidates

```json
[]
```

## Exact Metric Nodes

```json
[
  {
    "source_file": "exports/e1r_v0_2_backtest_summary.json",
    "json_path": "$",
    "matched": {
      "total_return_pct": 116.7435999134756,
      "spx_return_pct": 76.844174428316,
      "alpha_pct": 39.89942548515961,
      "max_drawdown_pct": 25.904809362815108,
      "profit_factor": 1.1919630955509348,
      "sharpe_ratio": 0.7957270568329264
    },
    "diffs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "exact_all_present": true,
    "keys": [
      "alpha_pct",
      "artifact_type",
      "composition_exists",
      "frozen_artifact",
      "max_drawdown_pct",
      "profit_factor",
      "regeneration_note",
      "regime_aware_logic",
      "research_status",
      "row_count",
      "sharpe_ratio",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass",
      "sidecar_active_days",
      "source_file",
      "source_json_path",
      "spx_return_pct",
      "strategy_id",
      "total_return_pct",
      "variant"
    ]
  }
]
```

## Output Items

```json
[
  {
    "path": "exports/e1r_v0_2_backtest_summary.json",
    "exists_after_run": true,
    "size_after_run": 941,
    "hash_after_run": "449a8ace55ce2335d174e17e2532d8793a3a9b99c021a935f8d7f2e531092114",
    "daily_like_count": 0,
    "metric_node_count": 1
  },
  {
    "path": "exports/e1r_v0_2_backtest_equity_curve.json",
    "exists_after_run": true,
    "size_after_run": 16004713,
    "hash_after_run": "d43ac75bc56340079b98958d73a0b2c3acb8c7154c04f8a0c394e5e969246926",
    "daily_like_count": 4,
    "metric_node_count": 0
  },
  {
    "path": "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
    "exists_after_run": false,
    "size_after_run": 0,
    "hash_after_run": null
  },
  {
    "path": "exports/e1_e1r_5y_equity_comparison.json",
    "exists_after_run": false,
    "size_after_run": 0,
    "hash_after_run": null
  },
  {
    "path": "data/research/e1r/e1r_formal_backtest_v0_1.json",
    "exists_after_run": true,
    "size_after_run": 81365,
    "hash_after_run": "a42c6496d407f833ab117307a7677d7c4d251482ae02495271eea0e060202dad",
    "daily_like_count": 0,
    "metric_node_count": 2
  }
]
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-4B-0G`: Inspect generator source and composer return contract
- Recommended action: Do not promote any daily-like output. Next step should inspect source code around export_canonical_5y_equity_curves.py and composer return values, not persisted diagnostic rows.

