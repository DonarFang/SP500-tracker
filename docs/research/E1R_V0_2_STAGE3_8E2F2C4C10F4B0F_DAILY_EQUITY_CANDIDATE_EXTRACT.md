# Stage 3.8E-2F-2C-4C-10F-4B-0F E1R Daily Equity Candidate Extract

Generated At: `2026-07-09T10:06:46.209159+00:00`

## Status

- Status: `E1R_DAILY_EQUITY_CANDIDATE_EXTRACT_COMPLETE_NONCANONICAL`
- Noncanonical candidate written: `True`
- Strategy files unchanged: `True`
- Canonical existence unchanged after restore: `True`
- E1R canonical written: `False`

## Conclusion

- `DAILY_EQUITY_CANDIDATE_EXTRACTED_NONCANONICAL`
- Recommended: Validate the noncanonical candidate against frozen metrics and portfolio-level contract; if it passes, promote via a separate canonical-writing step.

## Best Candidate

```json
{
  "source_file": "exports/e1r_v0_2_backtest_equity_curve.json",
  "json_path": "$.rows",
  "list_key": "rows",
  "kind": "daily_like_list",
  "stats": {
    "row_count": 8819,
    "parseable_equity_rows": 8819,
    "unique_dates": 859,
    "date_start": "2021-06-11",
    "date_end": "2026-06-16",
    "max_rows_per_date": 19,
    "one_row_per_date": false,
    "first_equity": 541.26,
    "last_equity": 227.18,
    "total_return_pct_from_rows": -58.027565310571624,
    "max_drawdown_pct_from_rows": 99.94945853241056,
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
    "first_row": {
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
    "last_row": {
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
  "parent_metric_match": {
    "matched": {},
    "diffs": {},
    "exact": false
  }
}
```

## All Candidate Summaries

```json
[
  {
    "score": -100.0,
    "source_file": "exports/e1r_v0_2_backtest_equity_curve.json",
    "json_path": "$.rows",
    "list_key": "rows",
    "kind": "daily_like_list",
    "stats": {
      "row_count": 8819,
      "parseable_equity_rows": 8819,
      "unique_dates": 859,
      "date_start": "2021-06-11",
      "date_end": "2026-06-16",
      "max_rows_per_date": 19,
      "one_row_per_date": false,
      "first_equity": 541.26,
      "last_equity": 227.18,
      "total_return_pct_from_rows": -58.027565310571624,
      "max_drawdown_pct_from_rows": 99.94945853241056,
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
      "first_row": {
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
      "last_row": {
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
    "parent_metric_match": {
      "matched": {},
      "diffs": {},
      "exact": false
    }
  },
  {
    "score": -100.0,
    "source_file": "exports/e1r_v0_2_backtest_equity_curve.json",
    "json_path": "$.equity_curve",
    "list_key": "equity_curve",
    "kind": "daily_like_list",
    "stats": {
      "row_count": 8819,
      "parseable_equity_rows": 8819,
      "unique_dates": 859,
      "date_start": "2021-06-11",
      "date_end": "2026-06-16",
      "max_rows_per_date": 19,
      "one_row_per_date": false,
      "first_equity": 541.26,
      "last_equity": 227.18,
      "total_return_pct_from_rows": -58.027565310571624,
      "max_drawdown_pct_from_rows": 99.94945853241056,
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
      "first_row": {
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
      "last_row": {
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
    "parent_metric_match": {
      "matched": {},
      "diffs": {},
      "exact": false
    }
  },
  {
    "score": -100.0,
    "source_file": "exports/e1r_v0_2_backtest_equity_curve.json",
    "json_path": "$.rows",
    "list_key": null,
    "kind": "daily_like_list",
    "stats": {
      "row_count": 8819,
      "parseable_equity_rows": 8819,
      "unique_dates": 859,
      "date_start": "2021-06-11",
      "date_end": "2026-06-16",
      "max_rows_per_date": 19,
      "one_row_per_date": false,
      "first_equity": 541.26,
      "last_equity": 227.18,
      "total_return_pct_from_rows": -58.027565310571624,
      "max_drawdown_pct_from_rows": 99.94945853241056,
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
      "first_row": {
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
      "last_row": {
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
    "parent_metric_match": {
      "matched": {},
      "diffs": {},
      "exact": false
    }
  },
  {
    "score": -100.0,
    "source_file": "exports/e1r_v0_2_backtest_equity_curve.json",
    "json_path": "$.equity_curve",
    "list_key": null,
    "kind": "daily_like_list",
    "stats": {
      "row_count": 8819,
      "parseable_equity_rows": 8819,
      "unique_dates": 859,
      "date_start": "2021-06-11",
      "date_end": "2026-06-16",
      "max_rows_per_date": 19,
      "one_row_per_date": false,
      "first_equity": 541.26,
      "last_equity": 227.18,
      "total_return_pct_from_rows": -58.027565310571624,
      "max_drawdown_pct_from_rows": 99.94945853241056,
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
      "first_row": {
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
      "last_row": {
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
    "parent_metric_match": {
      "matched": {},
      "diffs": {},
      "exact": false
    }
  }
]
```

## Generated Output Items

```json
[
  {
    "path": "exports/e1r_v0_2_backtest_summary.json",
    "exists": true,
    "size": 941,
    "hash": "449a8ace55ce2335d174e17e2532d8793a3a9b99c021a935f8d7f2e531092114",
    "candidate_count": 1,
    "candidate_summaries": [
      {
        "source_file": "exports/e1r_v0_2_backtest_summary.json",
        "json_path": "$",
        "kind": "metric_node",
        "metric_match": {
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
          "exact": true
        },
        "summary_keys": [
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
  },
  {
    "path": "exports/e1r_v0_2_backtest_equity_curve.json",
    "exists": true,
    "size": 16004713,
    "hash": "d43ac75bc56340079b98958d73a0b2c3acb8c7154c04f8a0c394e5e969246926",
    "candidate_count": 4,
    "candidate_summaries": [
      {
        "source_file": "exports/e1r_v0_2_backtest_equity_curve.json",
        "json_path": "$.rows",
        "list_key": "rows",
        "kind": "daily_like_list",
        "stats": {
          "row_count": 8819,
          "parseable_equity_rows": 8819,
          "unique_dates": 859,
          "date_start": "2021-06-11",
          "date_end": "2026-06-16",
          "max_rows_per_date": 19,
          "one_row_per_date": false,
          "first_equity": 541.26,
          "last_equity": 227.18,
          "total_return_pct_from_rows": -58.027565310571624,
          "max_drawdown_pct_from_rows": 99.94945853241056,
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
          "first_row": {
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
          "last_row": {
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
        "parent_metric_match": {
          "matched": {},
          "diffs": {},
          "exact": false
        }
      },
      {
        "source_file": "exports/e1r_v0_2_backtest_equity_curve.json",
        "json_path": "$.equity_curve",
        "list_key": "equity_curve",
        "kind": "daily_like_list",
        "stats": {
          "row_count": 8819,
          "parseable_equity_rows": 8819,
          "unique_dates": 859,
          "date_start": "2021-06-11",
          "date_end": "2026-06-16",
          "max_rows_per_date": 19,
          "one_row_per_date": false,
          "first_equity": 541.26,
          "last_equity": 227.18,
          "total_return_pct_from_rows": -58.027565310571624,
          "max_drawdown_pct_from_rows": 99.94945853241056,
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
          "first_row": {
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
          "last_row": {
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
        "parent_metric_match": {
          "matched": {},
          "diffs": {},
          "exact": false
        }
      },
      {
        "source_file": "exports/e1r_v0_2_backtest_equity_curve.json",
        "json_path": "$.rows",
        "list_key": null,
        "kind": "daily_like_list",
        "stats": {
          "row_count": 8819,
          "parseable_equity_rows": 8819,
          "unique_dates": 859,
          "date_start": "2021-06-11",
          "date_end": "2026-06-16",
          "max_rows_per_date": 19,
          "one_row_per_date": false,
          "first_equity": 541.26,
          "last_equity": 227.18,
          "total_return_pct_from_rows": -58.027565310571624,
          "max_drawdown_pct_from_rows": 99.94945853241056,
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
          "first_row": {
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
          "last_row": {
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
        "parent_metric_match": {
          "matched": {},
          "diffs": {},
          "exact": false
        }
      },
      {
        "source_file": "exports/e1r_v0_2_backtest_equity_curve.json",
        "json_path": "$.equity_curve",
        "list_key": null,
        "kind": "daily_like_list",
        "stats": {
          "row_count": 8819,
          "parseable_equity_rows": 8819,
          "unique_dates": 859,
          "date_start": "2021-06-11",
          "date_end": "2026-06-16",
          "max_rows_per_date": 19,
          "one_row_per_date": false,
          "first_equity": 541.26,
          "last_equity": 227.18,
          "total_return_pct_from_rows": -58.027565310571624,
          "max_drawdown_pct_from_rows": 99.94945853241056,
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
          "first_row": {
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
          "last_row": {
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
        "parent_metric_match": {
          "matched": {},
          "diffs": {},
          "exact": false
        }
      }
    ]
  },
  {
    "path": "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
    "exists": false,
    "size": 0,
    "hash": null
  },
  {
    "path": "exports/e1_e1r_5y_equity_comparison.json",
    "exists": false,
    "size": 0,
    "hash": null
  },
  {
    "path": "data/research/e1r/e1r_formal_backtest_v0_1.json",
    "exists": true,
    "size": 81365,
    "hash": "a42c6496d407f833ab117307a7677d7c4d251482ae02495271eea0e060202dad",
    "candidate_count": 2,
    "candidate_summaries": [
      {
        "source_file": "data/research/e1r/e1r_formal_backtest_v0_1.json",
        "json_path": "$.metrics",
        "kind": "metric_node",
        "metric_match": {
          "matched": {
            "total_return_pct": 65.71,
            "alpha_pct": -3.65,
            "max_drawdown_pct": 32.35,
            "profit_factor": 1.97,
            "sharpe_ratio": 0.58
          },
          "diffs": {
            "total_return_pct": 51.03359991347561,
            "alpha_pct": 43.54942548515961,
            "max_drawdown_pct": 6.4451906371848935,
            "profit_factor": 0.7780369044490651,
            "sharpe_ratio": 0.21572705683292648
          },
          "exact": false
        },
        "summary_keys": [
          "alpha_pct",
          "avg_holding_days",
          "exposure_pct",
          "max_drawdown_pct",
          "number_of_trades",
          "profit_factor",
          "sharpe_ratio",
          "spx_total_return_pct",
          "total_return_pct",
          "win_rate_pct"
        ]
      },
      {
        "source_file": "data/research/e1r/e1r_formal_backtest_v0_1.json",
        "json_path": "$.e1_metrics",
        "kind": "metric_node",
        "metric_match": {
          "matched": {
            "total_return_pct": 7.52,
            "max_drawdown_pct": 38.1,
            "profit_factor": 1.25,
            "sharpe_ratio": 0.18
          },
          "diffs": {
            "total_return_pct": 109.22359991347561,
            "max_drawdown_pct": 12.195190637184893,
            "profit_factor": 0.058036904449065174,
            "sharpe_ratio": 0.6157270568329265
          },
          "exact": false
        },
        "summary_keys": [
          "max_drawdown_pct",
          "number_of_trades",
          "profit_factor",
          "sharpe_ratio",
          "total_return_pct"
        ]
      }
    ]
  }
]
```

## Restore Report

```json
{
  "exports/e1r_v0_2_backtest_summary.json": {
    "action": "restored",
    "hash_after_restore": "449a8ace55ce2335d174e17e2532d8793a3a9b99c021a935f8d7f2e531092114",
    "matches_before": true
  },
  "exports/e1r_v0_2_backtest_equity_curve.json": {
    "action": "restored",
    "hash_after_restore": "d43ac75bc56340079b98958d73a0b2c3acb8c7154c04f8a0c394e5e969246926",
    "matches_before": true
  },
  "exports/e1r_v0_2_portfolio_backtest_equity_curve.json": {
    "action": "no_action_absent",
    "hash_after_restore": null,
    "matches_before": true
  },
  "exports/e1_e1r_5y_equity_comparison.json": {
    "action": "no_action_absent",
    "hash_after_restore": null,
    "matches_before": true
  },
  "data/research/e1r/e1r_formal_backtest_v0_1.json": {
    "action": "restored",
    "hash_after_restore": "a42c6496d407f833ab117307a7677d7c4d251482ae02495271eea0e060202dad",
    "matches_before": true
  }
}
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-4B-0G`: Validate E1R noncanonical daily equity candidate
- Recommended action: Validate the noncanonical candidate against frozen metrics and portfolio-level contract; if it passes, promote via a separate canonical-writing step.

