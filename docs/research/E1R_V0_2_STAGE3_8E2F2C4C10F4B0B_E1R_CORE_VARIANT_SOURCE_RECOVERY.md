# Stage 3.8E-2F-2C-4C-10F-4B-0B E1R Core Variant Source Recovery

Generated At: `2026-07-09T08:50:48.105771+00:00`

## Status

- Status: `E1R_CORE_VARIANT_SOURCE_RECOVERY_COMPLETE_NO_EXPORTS_WRITTEN`
- Strategy files unchanged: `True`
- Canonical existence unchanged: `True`
- Full backtest rerun: `False`

## Recovery Summary

```json
{
  "recovered_node_count": 282,
  "top_node_count": 80,
  "exact_metric_candidate_count": 17,
  "core_variant_candidate_count": 2,
  "daily_equity_candidate_count": 8,
  "conclusion": "E1R_FROZEN_METRIC_ARTIFACT_FOUND_CORE_SOURCE_CANDIDATES_PRESENT",
  "recommended_next_action": "Use the highest-scoring exact metric artifact to extract the nested core_variant_result / daily equity source in the next step."
}
```

## Top Recovered Nodes

```json
[
  {
    "score": 65,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "strategy_id",
        "total_return_pct",
        "variant"
      ],
      "metric_like_values": {
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json"
  },
  {
    "score": 65,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$",
      "type": "dict",
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
      ],
      "metric_like_values": {
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "exports/e1r_v0_2_backtest_summary.json"
  },
  {
    "score": 60,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.export_reports.e1r_backtest_summary.e1r_objects[0].summary_fields",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json"
  },
  {
    "score": 60,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.dry_run_generate_intervals.result.frozen_metric_targets",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C5_EXPORT_WRAPPER_SMOKE_REPORT.json"
  },
  {
    "score": 60,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.json_file_reports.docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json.lists[11].first_sample.summary_fields",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json"
  },
  {
    "score": 60,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.json_file_reports.docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json.lists[11].last_sample.summary_fields",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json"
  },
  {
    "score": 60,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.summary.frozen_metric_targets",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json"
  },
  {
    "score": 60,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.wrapper_output.dry_run_generate_intervals.result.frozen_metric_targets",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json"
  },
  {
    "score": 59,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      }
    },
    "summary": {
      "path": "$.specific_files.exports/e1r_v0_2_backtest_summary.json.top_level_metrics",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "spx_return_pct",
        "strategy_id",
        "total_return_pct",
        "variant"
      ],
      "metric_like_values": {
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json"
  },
  {
    "score": 59,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      }
    },
    "summary": {
      "path": "$.json_summaries.exports/e1r_v0_2_backtest_summary.json",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "exists",
        "json_valid",
        "max_drawdown_pct",
        "profit_factor",
        "spx_return_pct",
        "strategy_id",
        "top_keys",
        "total_return_pct",
        "type",
        "variant"
      ],
      "metric_like_values": {
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json"
  },
  {
    "score": 40,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.target_reports.backtest_summary.candidate_records[0].forward_fields",
      "type": "dict",
      "keys": [
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json"
  },
  {
    "score": 40,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.target_reports.backtest_summary.candidate_records[0].numeric_forward_fields",
      "type": "dict",
      "keys": [
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json"
  },
  {
    "score": 40,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.json_file_reports.docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json.lists[18].first_sample.forward_fields",
      "type": "dict",
      "keys": [
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json"
  },
  {
    "score": 40,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.json_file_reports.docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json.lists[18].first_sample.numeric_forward_fields",
      "type": "dict",
      "keys": [
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json"
  },
  {
    "score": 40,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.json_file_reports.docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json.lists[18].last_sample.forward_fields",
      "type": "dict",
      "keys": [
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json"
  },
  {
    "score": 40,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.json_file_reports.docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json.lists[18].last_sample.numeric_forward_fields",
      "type": "dict",
      "keys": [
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json"
  },
  {
    "score": 34,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      }
    },
    "summary": {
      "path": "$.json_reports.exports/e1r_v0_2_backtest_summary.json.field_presence.performance_like",
      "type": "dict",
      "keys": [
        "max_drawdown_pct",
        "profit_factor",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json"
  },
  {
    "score": 12,
    "target_diffs_abs": {
      "total_return_pct": 109.22359991347561,
      "alpha_pct": 101.73942548515961,
      "max_drawdown_pct": 12.195190637184893,
      "profit_factor": 0.058036904449065174,
      "sharpe_ratio": 0.6157270568329265
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 7.52,
        "target": 116.7435999134756
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": -61.84,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 38.1,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.25,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.18,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.backtest.results.layer_d",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "avg_execution_drag_pct",
        "avg_holding_days",
        "avg_loser_pct",
        "avg_winner_pct",
        "cagr_pct",
        "comparison",
        "daily_records",
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
        "spx_curve",
        "spx_total_return_pct",
        "status",
        "strategy_controls",
        "strategy_variant",
        "total_return_pct",
        "total_trades_all",
        "trades",
        "variant_results",
        "version",
        "win_rate_pct"
      ],
      "metric_like_values": {
        "name": "3-Variant LS60 Mode Compari
```

## Exact Metric Candidates

```json
[
  {
    "score": 65,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "strategy_id",
        "total_return_pct",
        "variant"
      ],
      "metric_like_values": {
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json"
  },
  {
    "score": 65,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$",
      "type": "dict",
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
      ],
      "metric_like_values": {
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "exports/e1r_v0_2_backtest_summary.json"
  },
  {
    "score": 60,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.export_reports.e1r_backtest_summary.e1r_objects[0].summary_fields",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json"
  },
  {
    "score": 60,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.dry_run_generate_intervals.result.frozen_metric_targets",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C5_EXPORT_WRAPPER_SMOKE_REPORT.json"
  },
  {
    "score": 60,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.json_file_reports.docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json.lists[11].first_sample.summary_fields",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json"
  },
  {
    "score": 60,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.json_file_reports.docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json.lists[11].last_sample.summary_fields",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json"
  },
  {
    "score": 60,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.summary.frozen_metric_targets",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json"
  },
  {
    "score": 60,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.wrapper_output.dry_run_generate_intervals.result.frozen_metric_targets",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json"
  },
  {
    "score": 59,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      }
    },
    "summary": {
      "path": "$.specific_files.exports/e1r_v0_2_backtest_summary.json.top_level_metrics",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "spx_return_pct",
        "strategy_id",
        "total_return_pct",
        "variant"
      ],
      "metric_like_values": {
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json"
  },
  {
    "score": 59,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "spx_return_pct": 0.0,
      "alpha_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "spx_return_pct": {
        "key": "spx_return_pct",
        "value": 76.844174428316,
        "target": 76.844174428316
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": 39.89942548515961,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      }
    },
    "summary": {
      "path": "$.json_summaries.exports/e1r_v0_2_backtest_summary.json",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "exists",
        "json_valid",
        "max_drawdown_pct",
        "profit_factor",
        "spx_return_pct",
        "strategy_id",
        "top_keys",
        "total_return_pct",
        "type",
        "variant"
      ],
      "metric_like_values": {
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json"
  },
  {
    "score": 40,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.target_reports.backtest_summary.candidate_records[0].forward_fields",
      "type": "dict",
      "keys": [
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json"
  },
  {
    "score": 40,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.target_reports.backtest_summary.candidate_records[0].numeric_forward_fields",
      "type": "dict",
      "keys": [
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json"
  },
  {
    "score": 40,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.json_file_reports.docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json.lists[18].first_sample.forward_fields",
      "type": "dict",
      "keys": [
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json"
  },
  {
    "score": 40,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 25.904809362815108,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.1919630955509348,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.7957270568329264,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.json_file_reports.docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json.lists[18].first_sample.numeric_forward_fields",
      "type": "dict",
      "keys": [
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      }
    },
    "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json"
  },
  {
    "score": 40,
    "target_diffs_abs": {
      "total_return_pct": 0.0,
      "max_drawdown_pct": 0.0,
      "profit_factor": 0.0,
      "sharpe_ratio": 0.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "target": 116.7435999134756
      },
      "max_drawdown_p
```

## Core Variant Candidates

```json
[
  {
    "score": 12,
    "target_diffs_abs": {
      "total_return_pct": 109.22359991347561,
      "alpha_pct": 101.73942548515961,
      "max_drawdown_pct": 12.195190637184893,
      "profit_factor": 0.058036904449065174,
      "sharpe_ratio": 0.6157270568329265
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 7.52,
        "target": 116.7435999134756
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": -61.84,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 38.1,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.25,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.18,
        "target": 0.7957270568329264
      }
    },
    "summary": {
      "path": "$.backtest.results.layer_d",
      "type": "dict",
      "keys": [
        "alpha_pct",
        "avg_execution_drag_pct",
        "avg_holding_days",
        "avg_loser_pct",
        "avg_winner_pct",
        "cagr_pct",
        "comparison",
        "daily_records",
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
        "spx_curve",
        "spx_total_return_pct",
        "status",
        "strategy_controls",
        "strategy_variant",
        "total_return_pct",
        "total_trades_all",
        "trades",
        "variant_results",
        "version",
        "win_rate_pct"
      ],
      "metric_like_values": {
        "name": "3-Variant LS60 Mode Comparison",
        "strategy_variant": "E1_audited_g4_minhold10",
        "version": "v1.6-ls60-mode-comparison",
        "status": "PARTIAL",
        "total_return_pct": 7.52,
        "spx_total_return_pct": 69.36,
        "alpha_pct": -61.84,
        "cagr_pct": 2.85,
        "max_drawdown_pct": 38.1,
        "profit_factor": 1.25,
        "sharpe_ratio": 0.18,
        "win_rate_pct": 36.2,
        "number_of_trades": 47,
        "total_trades_all": 47
      },
      "daily_records_len": 22,
      "daily_records_first_keys": [
        "cash",
        "date",
        "market_gate_state",
        "n_holdings",
        "pending_orders",
        "position_value",
        "spx_close",
        "spx_day_return_pct",
        "spx_ma50",
        "total_equity"
      ],
      "daily_records_first": {
        "date": "2023-11-06",
        "cash": 100000.0,
        "position_value": 0.0,
        "total_equity": 100000.0,
        "n_holdings": 0,
        "pending_orders": 0,
        "market_gate_state": "RISK_OFF",
        "spx_close": 4365.98,
        "spx_ma50": 4346.84,
        "spx_day_return_pct": 0.18
      },
      "daily_records_last": {
        "date": "2026-05-13",
        "cash": 37067.35,
        "position_value": 55620.57,
        "total_equity": 92687.92,
        "n_holdings": 3,
        "pending_orders": 2,
        "market_gate_state": "ALLOW",
        "spx_close": 7444.25,
        "spx_ma50": 6896.91,
        "spx_day_return_pct": 0.58
      },
      "equity_curve_len": 131,
      "spx_curve_len": 131,
      "trades_len": 47,
      "trades_first_keys": [
        "action_count",
        "actions_during_trade",
        "avg_cost",
        "effective_exit",
        "entry_adverse_gap_pct",
        "entry_date",
        "entry_price",
        "entry_signal",
        "execution_model",
        "exit_adverse_gap_pct",
        "exit_date",
        "exit_price",
        "exit_reason",
        "exit_reasons",
        "exit_signal",
        "exit_type",
        "exit_warning_count",
        "exit_warning_log",
        "holding_days",
        "is_sim_end",
        "leader_score_entry",
        "max_drawdown_in_trade",
        "max_gain_pct",
        "realized_pnl_before_exit",
        "relative_stop_exec_date",
        "relative_stop_triggered",
        "return_pct",
        "size_units_at_exit",
        "symbol",
        "take_profit_exec_date",
        "take_profit_triggered",
        "total_execution_drag_pct"
      ],
      "trades_first": {
        "symbol": "COIN",
        "entry_date": "2023-11-24",
        "exit_date": "2024-01-05",
        "entry_signal": "BUY",
        "exit_signal": "EXIT",
        "entry_price": 109.25,
        "avg_cost": 117.06,
        "exit_price": 155.6,
        "effective_exit": 150.94,
        "return_pct": 25.97,
        "max_gain_pct": 59.2,
        "max_drawdown_in_trade": 41.38,
        "holding_days": 29,
        "size_units_at_exit": 0.5,
        "leader_score_entry": 95.7,
        "relative_stop_triggered": false,
        "relative_stop_exec_date": null,
        "take_profit_triggered": false,
        "take_profit_exec_date": null,
        "realized_pnl_before_exit": 3831.32,
        "actions_during_trade": [
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "HOLD",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
          "REDUCE",
          "REDUCE",
          "REDUCE",
          "EXIT"
        ],
        "action_count": 30,
        "execution_model": "adverse_intraday_v1.0",
        "entry_adverse_gap_pct": 7.146,
        "exit_adverse_gap_pct": 2.996,
        "total_execution_drag_pct": 10.141,
        "is_sim_end": false,
        "exit_reason": "leader_score_below_60",
        "exit_reasons": [
          "leader_score_below_60"
        ],
        "exit_type": "NORMAL_EXIT",
        "exit_warning_log": [],
        "exit_warning_count": 0
      },
      "trades_last": {
        "symbol": "ODFL",
        "entry_date": "2026-06-10",
        "exit_date": "2026-06-11",
        "entry_signal": "BUY",
        "exit_signal": "SIM_END",
        "entry_price": 248.73,
        "avg_cost": 239.81,
        "exit_price": 247.76,
        "effective_exit": 236.92,
        "return_pct": -1.2,
        "max_gain_pct": 3.72,
        "max_drawdown_in_trade": 0,
        "holding_days": 2,
        "size_units_at_exit": 1.0,
        "leader_score_entry": 95.5,
        "take_profit_triggered": false,
        "take_profit_exec_date": null,
        "realized_pnl_before_exit": 0.0,
        "actions_during_trade": [
          "BUY",
          "HOLD",
          "HOLD"
        ],
        "action_count": 3,
        "execution_model": "adverse_intraday_v1.0",
        "is_sim_end": true,
        "exit_type": "SIM_END",
        "exit_warning_log": [],
        "exit_warning_count": 0
      }
    },
    "file": "exports/backtest.json"
  },
  {
    "score": 6,
    "target_diffs_abs": {
      "total_return_pct": 109.22359991347561,
      "alpha_pct": 101.73942548515961,
      "max_drawdown_pct": 12.195190637184893,
      "profit_factor": 0.058036904449065174,
      "sharpe_ratio": 0.6157270568329265,
      "trades": 13.0
    },
    "matched_metrics": {
      "total_return_pct": {
        "key": "total_return_pct",
        "value": 7.52,
        "target": 116.7435999134756
      },
      "alpha_pct": {
        "key": "alpha_pct",
        "value": -61.84,
        "target": 39.89942548515961
      },
      "max_drawdown_pct": {
        "key": "max_drawdown_pct",
        "value": 38.1,
        "target": 25.904809362815108
      },
      "profit_factor": {
        "key": "profit_factor",
        "value": 1.25,
        "target": 1.1919630955509348
      },
      "sharpe_ratio": {
        "key": "sharpe_ratio",
        "value": 0.18,
        "target": 0.7957270568329264
      },
      "trades": {
        "key": "number_of_trades",
        "value": 47.0,
        "target": 60
      }
    },
    "summary": {
      "path": "$",
      "type": "dict",
      "keys": [
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
      "metric_like_values": {
        "name": "3-Variant LS60 Mode Comparison",
        "strategy_variant": "E1_audited_g4_minhold10",
        "version": "v1.6-ls60-mode-comparison",
        "status": "PARTIAL",
        "total_return_pct": 7.52,
        "spx_total_return_pct": 69.36,
        "alpha_pct": -61.84,
        "cagr_pct": 2.85,
        "max_drawdown_pct": 38.1,
        "profit_factor": 1.25,
        "sharpe_ratio": 0.18,
        "win_rate_pct": 36.2,
        "number_of_trades": 47,
        "total_trades_all": 47
      },
      "daily_records_len": 22,
      "daily_records_first_keys": [
        "cash",
        "date",
        "market_gate_state",
        "n_holdings",
        "pending_orders",
        "position_value",
        "spx_close",
        "spx_day_return_pct",
        "spx_ma50",
        "total_equity"
      ],
      "daily_records_first": {
        "date": "2023-11-06",
        "cash": 100000.0,
        "position_value": 0.0,
        "total_equity": 100000.0,
        "n_holdings": 0,
        "pending_orders": 0,
        "market_gate_state": "RISK_OFF",
        "spx_close": 4365.98,
        "spx_ma50": 4346.84,
        "spx_day_return_pct": 0.18
      },
      "daily_records_last": {
        "date": "2026-05-13",
        "cash": 37067.35,
        "position_value": 55620.57,
        "total_equity": 92687.92,
        "n_holdings": 3,
        "pending_orders": 2,
        "market_gate_state": "ALLOW",
        "spx_close": 7444.25,
        "spx_ma50": 6896.91,
        "spx_day_return_pct": 0.58
      }
    },
    "file": "exports/portfolio_backtest.json"
  }
]
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-4B-0C`: Targeted extract of exact E1R core variant / daily equity
- Recommended action: Use the highest-scoring exact metric artifact to extract the nested core_variant_result / daily equity source in the next step.

