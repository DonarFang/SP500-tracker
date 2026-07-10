# E1R 4C-2C-4E-ENGINE-K2-R9 — Market State 115 Return Artifact Audit

Generated At: `2026-07-10T13:25:20.337555+00:00`

## Purpose
Find and audit the exact E1R ~116.74% full-run artifact and its market-state/gate assumptions before standalone replication.

## Selected Artifact
```json
{
  "path": "exports/e1r_v0_2_backtest_summary.json",
  "sha256": "449a8ace55ce2335d174e17e2532d8793a3a9b99c021a935f8d7f2e531092114",
  "top_level": {
    "total_return_pct": 116.7435999134756,
    "alpha_pct": 39.89942548515961,
    "max_drawdown_pct": 25.904809362815108,
    "sharpe_ratio": 0.7957270568329264,
    "profit_factor": 1.1919630955509348
  },
  "return_hits": [
    {
      "path": "total_return_pct",
      "key": "total_return_pct",
      "value": 116.7435999134756,
      "distance_to_target_116_74": 0.0035999134756110607
    }
  ],
  "metric_hits": [
    {
      "path": "total_return_pct",
      "key": "total_return_pct",
      "value": 116.7435999134756
    },
    {
      "path": "spx_return_pct",
      "key": "spx_return_pct",
      "value": 76.844174428316
    },
    {
      "path": "alpha_pct",
      "key": "alpha_pct",
      "value": 39.89942548515961
    },
    {
      "path": "max_drawdown_pct",
      "key": "max_drawdown_pct",
      "value": 25.904809362815108
    },
    {
      "path": "profit_factor",
      "key": "profit_factor",
      "value": 1.1919630955509348
    },
    {
      "path": "sharpe_ratio",
      "key": "sharpe_ratio",
      "value": 0.7957270568329264
    }
  ],
  "market_hits": [
    {
      "path": "regime_aware_logic",
      "key": "regime_aware_logic",
      "value": "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
    },
    {
      "path": "sidecar_active_by_regime",
      "key": "sidecar_active_by_regime",
      "value": {
        "SIDEWAYS": 135
      }
    },
    {
      "path": "sidecar_active_by_regime.SIDEWAYS",
      "key": "SIDEWAYS",
      "value": 135
    }
  ],
  "e1r_hits": [
    {
      "path": "strategy_id",
      "key": "strategy_id",
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "variant",
      "key": "variant",
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "source_file",
      "key": "source_file",
      "value": "exports/e1r_v0_2_backtest_summary.json"
    }
  ],
  "counts": {
    "return_hits": 1,
    "metric_hits": 6,
    "market_hits": 3,
    "e1r_hits": 3
  },
  "score": 280
}
```

## Metric Snapshot
```json
{
  "total_return_pct": 116.7435999134756,
  "alpha_pct": 39.89942548515961,
  "max_drawdown_pct": 25.904809362815108,
  "profit_factor": 1.1919630955509348,
  "sharpe_ratio": 0.7957270568329264
}
```

## Market Parameter Compare
```json
{
  "r8_short_window_market_gate_parameters": {
    "market_gate_variant": "D3_RISK_OFF_PLUS_SHOCK_GATE",
    "market_gate_enabled": true,
    "risk_off_below_spx_ma50": true,
    "market_shock_gate_enabled": true,
    "market_shock_daily_return": -0.02,
    "evidence": [
      {
        "type": "runtime_log_from_R7",
        "text": "Market Gate Variant: D3_RISK_OFF_PLUS_SHOCK_GATE"
      },
      {
        "type": "runtime_log_from_R7",
        "text": "Market Gate: enabled=True | RiskOff=SPX<MA50:True | Shock<=-2.0%:True"
      }
    ]
  },
  "r8_short_window_golden_master_controls": {
    "strategy_controls": {
      "entry_rs_min": 90.0,
      "ls60_exit_mode": "reduce",
      "candidate_top_n": null,
      "qualified_entry_enabled": false,
      "qualified_rs_min": 90.0,
      "qualified_momentum_min": 85.0,
      "qualified_th_min": 75.0,
      "qualified_states": [
        "Expansion"
      ],
      "qualified_price_above_ma50": true,
      "qualified_ma50_slope_min": 0.0,
      "qp_avg_pool_size": 0.0,
      "qp_pool_days": 0,
      "qp_days_pool_lt_3": 0,
      "qp_days_pool_ge_10": 0,
      "qp_buy_orders_generated": 0,
      "min_holding_days": 0,
      "min_hold_allow_broken_exit": true,
      "e1r_regime_wiring_enabled": false,
      "e1r_regime_source": null,
      "relative_stop_enabled": false,
      "relative_stop_underperform_pct": -8.0,
      "relative_stop_action": "REL_REDUCE",
      "relative_stop_once_per_position": true,
      "relative_stop_stats": {
        "signals": 0,
        "executed": 0
      },
      "fixed_take_profit_enabled": false
    },
    "market_entry_gate": {
      "variant": "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "enabled": true,
      "risk_off_rule": "SPX close < SPX MA50",
      "market_shock_rule": "SPX daily return <= -2.0%",
      "blocked_actions": [
        "BUY",
        "ADD"
      ],
      "unaffected_actions": [
        "HOLD",
        "REDUCE",
        "EXIT"
      ],
      "days": {
        "entry_allowed": 53,
        "risk_off": 8,
        "market_shock": 1,
        "blocked_total": 9
      }
    },
    "version": "v1.6-top3-rs-minhold-relstop",
    "strategy_variant": "top3_entry_rs_minhold_relstop",
    "entry_top_n": 3,
    "rank_based_exit": false,
    "e1r_uptrend_execution_enabled": false,
    "status": "INSUFFICIENT_SAMPLE"
  },
  "full_115_artifact_values": {
    "market_entry_gate": [],
    "strategy_controls": [],
    "market_gate_enabled": [],
    "risk_off_below_spx_ma50": [],
    "market_shock_gate_enabled": [],
    "market_shock_daily_return": [],
    "e1r_regime_wiring_enabled": [],
    "e1r_uptrend_execution_enabled": []
  },
  "unresolved": [
    {
      "id": "full_115_artifact_missing_market_entry_gate",
      "field": "market_entry_gate",
      "blocking_for_replication": true
    },
    {
      "id": "full_115_artifact_missing_strategy_controls",
      "field": "strategy_controls",
      "blocking_for_replication": false
    },
    {
      "id": "full_115_artifact_missing_market_gate_enabled",
      "field": "market_gate_enabled",
      "blocking_for_replication": true
    },
    {
      "id": "full_115_artifact_missing_risk_off_below_spx_ma50",
      "field": "risk_off_below_spx_ma50",
      "blocking_for_replication": true
    },
    {
      "id": "full_115_artifact_missing_market_shock_gate_enabled",
      "field": "market_shock_gate_enabled",
      "blocking_for_replication": true
    },
    {
      "id": "full_115_artifact_missing_market_shock_daily_return",
      "field": "market_shock_daily_return",
      "blocking_for_replication": true
    },
    {
      "id": "full_115_artifact_missing_e1r_regime_wiring_enabled",
      "field": "e1r_regime_wiring_enabled",
      "blocking_for_replication": false
    },
    {
      "id": "full_115_artifact_missing_e1r_uptrend_execution_enabled",
      "field": "e1r_uptrend_execution_enabled",
      "blocking_for_replication": false
    }
  ]
}
```

## Top Artifact Candidates
```json
{
  "best_json": {
    "path": "exports/e1r_v0_2_backtest_summary.json",
    "sha256": "449a8ace55ce2335d174e17e2532d8793a3a9b99c021a935f8d7f2e531092114",
    "top_level": {
      "total_return_pct": 116.7435999134756,
      "alpha_pct": 39.89942548515961,
      "max_drawdown_pct": 25.904809362815108,
      "sharpe_ratio": 0.7957270568329264,
      "profit_factor": 1.1919630955509348
    },
    "return_hits": [
      {
        "path": "total_return_pct",
        "key": "total_return_pct",
        "value": 116.7435999134756,
        "distance_to_target_116_74": 0.0035999134756110607
      }
    ],
    "metric_hits": [
      {
        "path": "total_return_pct",
        "key": "total_return_pct",
        "value": 116.7435999134756
      },
      {
        "path": "spx_return_pct",
        "key": "spx_return_pct",
        "value": 76.844174428316
      },
      {
        "path": "alpha_pct",
        "key": "alpha_pct",
        "value": 39.89942548515961
      },
      {
        "path": "max_drawdown_pct",
        "key": "max_drawdown_pct",
        "value": 25.904809362815108
      },
      {
        "path": "profit_factor",
        "key": "profit_factor",
        "value": 1.1919630955509348
      },
      {
        "path": "sharpe_ratio",
        "key": "sharpe_ratio",
        "value": 0.7957270568329264
      }
    ],
    "market_hits": [
      {
        "path": "regime_aware_logic",
        "key": "regime_aware_logic",
        "value": "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
      },
      {
        "path": "sidecar_active_by_regime",
        "key": "sidecar_active_by_regime",
        "value": {
          "SIDEWAYS": 135
        }
      },
      {
        "path": "sidecar_active_by_regime.SIDEWAYS",
        "key": "SIDEWAYS",
        "value": 135
      }
    ],
    "e1r_hits": [
      {
        "path": "strategy_id",
        "key": "strategy_id",
        "value": "E1R_REGIME_AWARE_V0_2"
      },
      {
        "path": "variant",
        "key": "variant",
        "value": "E1R_REGIME_AWARE_V0_2"
      },
      {
        "path": "source_file",
        "key": "source_file",
        "value": "exports/e1r_v0_2_backtest_summary.json"
      }
    ],
    "counts": {
      "return_hits": 1,
      "metric_hits": 6,
      "market_hits": 3,
      "e1r_hits": 3
    },
    "score": 280
  },
  "best_text": {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
    "sha256": "13f9dffb0e11fb9247084b14e7c6da290e3c735d211f527bea51fe8311bf61e4",
    "score": 120,
    "hits": [
      {
        "line": 1,
        "text": "# Stage 3.8E-2F-2C-4C-10F-4B-0B E1R Core Variant Source Recovery"
      },
      {
        "line": 7,
        "text": "- Status: `E1R_CORE_VARIANT_SOURCE_RECOVERY_COMPLETE_NO_EXPORTS_WRITTEN`"
      },
      {
        "line": 21,
        "text": "  \"conclusion\": \"E1R_FROZEN_METRIC_ARTIFACT_FOUND_CORE_SOURCE_CANDIDATES_PRESENT\","
      },
      {
        "line": 33,
        "text": "      \"total_return_pct\": 0.0,"
      },
      {
        "line": 41,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 42,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 43,
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "line": 44,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 73,
        "text": "      \"path\": \"$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics\","
      },
      {
        "line": 82,
        "text": "        \"total_return_pct\","
      },
      {
        "line": 86,
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "line": 87,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "line": 95,
        "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json\""
      },
      {
        "line": 100,
        "text": "      \"total_return_pct\": 0.0,"
      },
      {
        "line": 108,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 109,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 110,
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "line": 111,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 161,
        "text": "        \"total_return_pct\","
      },
      {
        "line": 165,
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "line": 166,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "line": 174,
        "text": "    \"file\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "line": 179,
        "text": "      \"total_return_pct\": 0.0,"
      },
      {
        "line": 187,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 188,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 189,
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "line": 190,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 219,
        "text": "      \"path\": \"$.export_reports.e1r_backtest_summary.e1r_objects[0].summary_fields\","
      },
      {
        "line": 227,
        "text": "        \"total_return_pct\""
      },
      {
        "line": 230,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "line": 238,
        "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json\""
      },
      {
        "line": 243,
        "text": "      \"total_return_pct\": 0.0,"
      },
      {
        "line": 251,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 252,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 253,
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "line": 254,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 291,
        "text": "        \"total_return_pct\""
      },
      {
        "line": 294,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "line": 302,
        "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C5_EXPORT_WRAPPER_SMOKE_REPORT.json\""
      },
      {
        "line": 307,
        "text": "      \"total_return_pct\": 0.0,"
      },
      {
        "line": 315,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 316,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 317,
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "line": 318,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 347,
        "text": "      \"path\": \"$.json_file_reports.docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json.lists[11].first_sample.summary_fields\","
      },
      {
        "line": 355,
        "text": "        \"total_return_pct\""
      },
      {
        "line": 358,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "line": 366,
        "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\""
      },
      {
        "line": 371,
        "text": "      \"total_return_pct\": 0.0,"
      },
      {
        "line": 379,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 380,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 381,
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "line": 382,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 411,
        "text": "      \"path\": \"$.json_file_reports.docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json.lists[11].last_sample.summary_fields\","
      },
      {
        "line": 419,
        "text": "        \"total_return_pct\""
      },
      {
        "line": 422,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "line": 430,
        "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\""
      },
      {
        "line": 435,
        "text": "      \"total_return_pct\": 0.0,"
      },
      {
        "line": 443,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 444,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 445,
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "line": 446,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 483,
        "text": "        \"total_return_pct\""
      },
      {
        "line": 486,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "line": 494,
        "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json\""
      },
      {
        "line": 499,
        "text": "      \"total_return_pct\": 0.0,"
      },
      {
        "line": 507,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 508,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 509,
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "line": 510,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 547,
        "text": "        \"total_return_pct\""
      },
      {
        "line": 550,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "line": 558,
        "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json\""
      },
      {
        "line": 563,
        "text": "      \"total_return_pct\": 0.0,"
      },
      {
        "line": 570,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 571,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 572,
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "line": 573,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 597,
        "text": "      \"path\": \"$.specific_files.exports/e1r_v0_2_backtest_summary.json.top_level_metrics\","
      },
      {
        "line": 605,
        "text": "        \"total_return_pct\","
      },
      {
        "line": 609,
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "line": 610,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "line": 617,
        "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json\""
      },
      {
        "line": 622,
        "text": "      \"total_return_pct\": 0.0,"
      },
      {
        "line": 629,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 630,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 631,
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "line": 632,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 656,
        "text": "      \"path\": \"$.json_summaries.exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "line": 667,
        "text": "        \"total_return_pct\","
      },
      {
        "line": 672,
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "line": 673,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "line": 680,
        "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json\""
      },
      {
        "line": 685,
        "text": "      \"total_return_pct\": 0.0,"
      },
      {
        "line": 691,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 692,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 693,
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "line": 694,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 719,
        "text": "        \"total_return_pct\""
      },
      {
        "line": 722,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "line": 728,
        "text": "    \"file\": \"docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json\""
      },
      {
        "line": 733,
        "text": "      \"total_return_pct\": 0.0,"
      },
      {
        "line": 739,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 740,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 741,
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "line": 742,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 767,
        "text": "        \"total_return_pct\""
      },
      {
        "line": 770,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "line": 776,
        "text": "    \"file\": \"docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json\""
      },
      {
        "line": 781,
        "text": "      \"total_return_pct\": 0.0,"
      },
      {
        "line": 787,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 788,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 789,
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "line": 790,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 809,
        "text": "      \"path\": \"$.json_file_reports.docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json.lists[18].first_sample.forward_fields\","
      },
      {
        "line": 815,
        "text": "        \"total_return_pct\""
      },
      {
        "line": 818,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "line": 824,
        "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\""
      },
      {
        "line": 829,
        "text": "      \"total_return_pct\": 0.0,"
      },
      {
        "line": 835,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 836,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 837,
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "line": 838,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 857,
        "text": "      \"path\": \"$.json_file_reports.docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json.lists[18].first_sample.numeric_forward_fields\","
      },
      {
        "line": 863,
        "text": "        \"total_return_pct\""
      },
      {
        "line": 866,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "line": 872,
        "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\""
      },
      {
        "line": 877,
        "text": "      \"total_return_pct\": 0.0,"
      },
      {
        "line": 883,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 884,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 885,
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "line": 886,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 905,
        "text": "      \"path\": \"$.json_file_reports.docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json.lists[18].last_sample.forward_fields\","
      },
      {
        "line": 911,
        "text": "        \"total_return_pct\""
      },
      {
        "line": 914,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "line": 920,
        "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\""
      },
      {
        "line": 925,
        "text": "      \"total_return_pct\": 0.0,"
      },
      {
        "line": 931,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 932,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 933,
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "line": 934,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 953,
        "text": "      \"path\": \"$.json_file_reports.docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json.lists[18].last_sample.numeric_forward_fields\","
      },
      {
        "line": 959,
        "text": "        \"total_return_pct\""
      },
      {
        "line": 962,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "line": 968,
        "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\""
      },
      {
        "line": 973,
        "text": "      \"total_return_pct\": 0.0,"
      },
      {
        "line": 978,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 979,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 980,
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "line": 981,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 995,
        "text": "      \"path\": \"$.json_reports.exports/e1r_v0_2_backtest_summary.json.field_presence.performance_like\","
      },
      {
        "line": 1000,
        "text": "        \"total_return_pct\""
      },
      {
        "line": 1003,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "line": 1008,
        "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json\""
      },
      {
        "line": 1013,
        "text": "      \"total_return_pct\": 109.22359991347561,"
      },
      {
        "line": 1020,
        "text": "      \"total_return_pct\": {"
      },
      {
        "line": 1021,
        "text": "        \"key\": \"total_return_pct\","
      },
      {
        "line": 1023,
        "text": "        \"target\": 116.7435999134756"
      },
      {
        "line": 1089,
        "text": "        \"spx_total_return_pct\","
      },
      {
        "line": 1093,
        "text": "        \"total_return_pct\","
      }
    ],
    "counts": {
      "hits": 160
    }
  },
  "top_json": [
    {
      "path": "exports/e1r_v0_2_backtest_summary.json",
      "sha256": "449a8ace55ce2335d174e17e2532d8793a3a9b99c021a935f8d7f2e531092114",
      "top_level": {
        "total_return_pct": 116.7435999134756,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "sharpe_ratio": 0.7957270568329264,
        "profit_factor": 1.1919630955509348
      },
      "return_hits": [
        {
          "path": "total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        }
      ],
      "metric_hits": [
        {
          "path": "total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "spx_return_pct",
          "key": "spx_return_pct",
          "value": 76.844174428316
        },
        {
          "path": "alpha_pct",
          "key": "alpha_pct",
          "value": 39.89942548515961
        },
        {
          "path": "max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        },
        {
          "path": "profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.7957270568329264
        }
      ],
      "market_hits": [
        {
          "path": "regime_aware_logic",
          "key": "regime_aware_logic",
          "value": "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        },
        {
          "path": "sidecar_active_by_regime",
          "key": "sidecar_active_by_regime",
          "value": {
            "SIDEWAYS": 135
          }
        },
        {
          "path": "sidecar_active_by_regime.SIDEWAYS",
          "key": "SIDEWAYS",
          "value": 135
        }
      ],
      "e1r_hits": [
        {
          "path": "strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "variant",
          "key": "variant",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "source_file",
          "key": "source_file",
          "value": "exports/e1r_v0_2_backtest_summary.json"
        }
      ],
      "counts": {
        "return_hits": 1,
        "metric_hits": 6,
        "market_hits": 3,
        "e1r_hits": 3
      },
      "score": 280
    },
    {
      "path": "docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json",
      "sha256": "1fdaa9fd1eee845d06111b087250d727a3d1d4aa24171e0f7a87648d31668508",
      "top_level": {
        "status": "AUDIT_COMPLETE_NO_SOURCE_CHANGES"
      },
      "return_hits": [
        {
          "path": "target_reports.backtest_summary.candidate_records[0].forward_fields.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "target_reports.backtest_summary.candidate_records[0].numeric_forward_fields.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        }
      ],
      "metric_hits": [
        {
          "path": "target_reports.e1_oos_summary.candidate_records[0].forward_fields.total_return_pct",
          "key": "total_return_pct",
          "value": -24.74
        },
        {
          "path": "target_reports.e1_oos_summary.candidate_records[0].forward_fields.win_rate_pct",
          "key": "win_rate_pct",
          "value": null
        },
        {
          "path": "target_reports.e1_oos_summary.candidate_records[0].forward_fields.profit_factor",
          "key": "profit_factor",
          "value": null
        },
        {
          "path": "target_reports.e1_oos_summary.candidate_records[0].forward_fields.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 24.74
        },
        {
          "path": "target_reports.e1_oos_summary.candidate_records[0].numeric_forward_fields.total_return_pct",
          "key": "total_return_pct",
          "value": -24.74
        },
        {
          "path": "target_reports.e1_oos_summary.candidate_records[0].numeric_forward_fields.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 24.74
        },
        {
          "path": "target_reports.backtest_summary.candidate_records[0].forward_fields.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "target_reports.backtest_summary.candidate_records[0].forward_fields.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "target_reports.backtest_summary.candidate_records[0].forward_fields.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.7957270568329264
        },
        {
          "path": "target_reports.backtest_summary.candidate_records[0].forward_fields.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        },
        {
          "path": "target_reports.backtest_summary.candidate_records[0].numeric_forward_fields.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "target_reports.backtest_summary.candidate_records[0].numeric_forward_fields.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "target_reports.backtest_summary.candidate_records[0].numeric_forward_fields.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.7957270568329264
        },
        {
          "path": "target_reports.backtest_summary.candidate_records[0].numeric_forward_fields.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        }
      ],
      "market_hits": [
        {
          "path": "target_reports.e1r_oos_summary.term_presence.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_summary.term_presence.regime",
          "key": "regime",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.term_presence.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.term_presence.regime",
          "key": "regime",
          "value": false
        },
        {
          "path": "target_reports.e1r_oos_positions.term_presence.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_positions.term_presence.regime",
          "key": "regime",
          "value": false
        },
        {
          "path": "target_reports.e1r_oos_orders.term_presence.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_orders.term_presence.regime",
          "key": "regime",
          "value": false
        },
        {
          "path": "target_reports.e1r_status.term_presence.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": true
        },
        {
          "path": "target_reports.e1r_status.term_presence.regime",
          "key": "regime",
          "value": true
        },
        {
          "path": "target_reports.e1_oos_summary.term_presence.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": false
        },
        {
          "path": "target_reports.e1_oos_summary.term_presence.regime",
          "key": "regime",
          "value": false
        },
        {
          "path": "target_reports.e1_oos_equity_curve.term_presence.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": false
        },
        {
          "path": "target_reports.e1_oos_equity_curve.term_presence.regime",
          "key": "regime",
          "value": false
        },
        {
          "path": "target_reports.backtest_summary.term_presence.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": true
        },
        {
          "path": "target_reports.backtest_summary.term_presence.regime",
          "key": "regime",
          "value": true
        }
      ],
      "e1r_hits": [
        {
          "path": "stage",
          "key": "stage",
          "value": "B_STAGE_3_8E2B_E1R_OOS_SUMMARY_FIELD_AUDIT"
        },
        {
          "path": "question",
          "key": "question",
          "value": "Does exports/oos_e1r_v0_2_summary.json contain daily forward fields for E1R v0.2?"
        },
        {
          "path": "targets.e1r_oos_summary",
          "key": "e1r_oos_summary",
          "value": "exports/oos_e1r_v0_2_summary.json"
        },
        {
          "path": "targets.e1r_oos_equity_curve",
          "key": "e1r_oos_equity_curve",
          "value": "exports/oos_e1r_v0_2_equity_curve.json"
        },
        {
          "path": "targets.e1r_oos_positions",
          "key": "e1r_oos_positions",
          "value": "exports/oos_e1r_v0_2_positions.json"
        },
        {
          "path": "targets.e1r_oos_orders",
          "key": "e1r_oos_orders",
          "value": "exports/oos_e1r_v0_2_orders.json"
        },
        {
          "path": "targets.e1r_status",
          "key": "e1r_status",
          "value": "exports/e1r_v0_2_status.json"
        },
        {
          "path": "targets.backtest_summary",
          "key": "backtest_summary",
          "value": "exports/e1r_v0_2_backtest_summary.json"
        },
        {
          "path": "target_reports.e1r_oos_summary",
          "key": "e1r_oos_summary",
          "value": "{\"name\": \"e1r_oos_summary\", \"meta\": {\"exists\": true, \"valid_json\": true, \"path\": \"exports/oos_e1r_v0_2_summary.json\", \"size_bytes\": 873, \"type\": \"dict\", \"top_level_keys\": [\"generated_at\", \"phase\", \"strategy_id\", \"version\", \"research_status\", \"status_date\", \"market_state\", \"regime\", \"subclass\", \"mutually_exclusive_state_model\", \"core_active\", \"sidecar_active\", \"sidecar_selected_count\", \"gross_exposure\", \"top_n\", \"execution_status\", \"equity_status\", \"notes\"], \"array_length\": null}, \"term_presence\": {\"E1R_REGIME_AWARE_V0_2\": true, \"E1R\": true, \"v0.2\": true, \"sidecar\": true, \"regime\": true, \"UPTREND\": true, \"SIDEWAYS\": false, \"DOWNTREND\": false, \"MA_CONFLICT\": false}, \"candidate_records\": [{\"path\": \"$\", \"keys\": [\"generated_at\", \"phase\", \"strategy_id\", \"version\", \"research_status\", \"status_date\", \"market_state\", \"regime\", \"subclass\", \"mutually_exclusive_state_model\", \"core_active\", \"sidecar_active\", \"sidecar_selected_count\", \"gross_exposure\", \"top_n\", \"execution_status\", \"equity_status\", \"notes\"], \"has_date\": true, \"has_forward_metric\": true, \"has_numeric_forward_metric\": true, \"date_fields\": {\"status_date\": \"2026-06-18\", \"generated_at\": \"2026-07-07T23:56:04.521255+00:00\"}, \"forward_fie...<truncated>"
        },
        {
          "path": "target_reports.e1r_oos_summary.name",
          "key": "name",
          "value": "e1r_oos_summary"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta",
          "key": "meta",
          "value": {
            "exists": true,
            "valid_json": true,
            "path": "exports/oos_e1r_v0_2_summary.json",
            "size_bytes": 873,
            "type": "dict",
            "top_level_keys": [
              "generated_at",
              "phase",
              "strategy_id",
              "version",
              "research_status",
              "status_date",
              "market_state",
              "regime",
              "subclass",
              "mutually_exclusive_state_model",
              "core_active",
              "sidecar_active",
              "sidecar_selected_count",
              "gross_exposure",
              "top_n",
              "execution_status",
              "equity_status",
              "notes"
            ],
            "array_length": null
          }
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.exists",
          "key": "exists",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.valid_json",
          "key": "valid_json",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.path",
          "key": "path",
          "value": "exports/oos_e1r_v0_2_summary.json"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.size_bytes",
          "key": "size_bytes",
          "value": 873
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.type",
          "key": "type",
          "value": "dict"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys",
          "key": "top_level_keys",
          "value": [
            "generated_at",
            "phase",
            "strategy_id",
            "version",
            "research_status",
            "status_date",
            "market_state",
            "regime",
            "subclass",
            "mutually_exclusive_state_model",
            "core_active",
            "sidecar_active",
            "sidecar_selected_count",
            "gross_exposure",
            "top_n",
            "execution_status",
            "equity_status",
            "notes"
          ]
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[0]",
          "key": "[0]",
          "value": "generated_at"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[1]",
          "key": "[1]",
          "value": "phase"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[2]",
          "key": "[2]",
          "value": "strategy_id"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[3]",
          "key": "[3]",
          "value": "version"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[4]",
          "key": "[4]",
          "value": "research_status"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[5]",
          "key": "[5]",
          "value": "status_date"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[6]",
          "key": "[6]",
          "value": "market_state"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[7]",
          "key": "[7]",
          "value": "regime"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[8]",
          "key": "[8]",
          "value": "subclass"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[9]",
          "key": "[9]",
          "value": "mutually_exclusive_state_model"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[10]",
          "key": "[10]",
          "value": "core_active"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[11]",
          "key": "[11]",
          "value": "sidecar_active"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[12]",
          "key": "[12]",
          "value": "sidecar_selected_count"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[13]",
          "key": "[13]",
          "value": "gross_exposure"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[14]",
          "key": "[14]",
          "value": "top_n"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[15]",
          "key": "[15]",
          "value": "execution_status"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[16]",
          "key": "[16]",
          "value": "equity_status"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.top_level_keys[17]",
          "key": "[17]",
          "value": "notes"
        },
        {
          "path": "target_reports.e1r_oos_summary.meta.array_length",
          "key": "array_length",
          "value": null
        },
        {
          "path": "target_reports.e1r_oos_summary.term_presence",
          "key": "term_presence",
          "value": {
            "E1R_REGIME_AWARE_V0_2": true,
            "E1R": true,
            "v0.2": true,
            "sidecar": true,
            "regime": true,
            "UPTREND": true,
            "SIDEWAYS": false,
            "DOWNTREND": false,
            "MA_CONFLICT": false
          }
        },
        {
          "path": "target_reports.e1r_oos_summary.term_presence.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_summary.term_presence.E1R",
          "key": "E1R",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_summary.term_presence.v0.2",
          "key": "v0.2",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_summary.term_presence.sidecar",
          "key": "sidecar",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_summary.term_presence.regime",
          "key": "regime",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_summary.term_presence.UPTREND",
          "key": "UPTREND",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_summary.term_presence.SIDEWAYS",
          "key": "SIDEWAYS",
          "value": false
        },
        {
          "path": "target_reports.e1r_oos_summary.term_presence.DOWNTREND",
          "key": "DOWNTREND",
          "value": false
        },
        {
          "path": "target_reports.e1r_oos_summary.term_presence.MA_CONFLICT",
          "key": "MA_CONFLICT",
          "value": false
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records",
          "key": "candidate_records",
          "value": "[{\"path\": \"$\", \"keys\": [\"generated_at\", \"phase\", \"strategy_id\", \"version\", \"research_status\", \"status_date\", \"market_state\", \"regime\", \"subclass\", \"mutually_exclusive_state_model\", \"core_active\", \"sidecar_active\", \"sidecar_selected_count\", \"gross_exposure\", \"top_n\", \"execution_status\", \"equity_status\", \"notes\"], \"has_date\": true, \"has_forward_metric\": true, \"has_numeric_forward_metric\": true, \"date_fields\": {\"status_date\": \"2026-06-18\", \"generated_at\": \"2026-07-07T23:56:04.521255+00:00\"}, \"forward_fields\": {\"gross_exposure\": 0.25}, \"numeric_forward_fields\": {\"gross_exposure\": 0.25}, \"preview\": \"{\\n  \\\"generated_at\\\": \\\"2026-07-07T23:56:04.521255+00:00\\\",\\n  \\\"phase\\\": \\\"OOS_STATUS_SIGNAL_ONLY\\\",\\n  \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\\n  \\\"version\\\": \\\"E1R-v0.2-formal-sidecar-sleeve\\\",\\n  \\\"research_status\\\": \\\"FORMAL_SIDECAR_SLEEVE_ENGINE\\\",\\n  \\\"status_date\\\": \\\"2026-06-18\\\",\\n  \\\"market_state\\\": \\\"UPTREND\\\",\\n  \\\"regime\\\": \\\"UPTREND\\\",\\n  \\\"subclass\\\": null,\\n  \\\"mutually_exclusive_state_model\\\": true,\\n  \\\"core_active\\\": true,\\n  \\\"sidecar_active\\\": false,\\n  \\\"sidecar_selected_count\\\": 0,\\n  \\\"gross_exposure\\\": 0.25,\\n  \\\"top_n\\\": 10,\\n  \\\"execution_status\\\": \\\"NO_REAL_...<truncated>"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0]",
          "key": "[0]",
          "value": "{\"path\": \"$\", \"keys\": [\"generated_at\", \"phase\", \"strategy_id\", \"version\", \"research_status\", \"status_date\", \"market_state\", \"regime\", \"subclass\", \"mutually_exclusive_state_model\", \"core_active\", \"sidecar_active\", \"sidecar_selected_count\", \"gross_exposure\", \"top_n\", \"execution_status\", \"equity_status\", \"notes\"], \"has_date\": true, \"has_forward_metric\": true, \"has_numeric_forward_metric\": true, \"date_fields\": {\"status_date\": \"2026-06-18\", \"generated_at\": \"2026-07-07T23:56:04.521255+00:00\"}, \"forward_fields\": {\"gross_exposure\": 0.25}, \"numeric_forward_fields\": {\"gross_exposure\": 0.25}, \"preview\": \"{\\n  \\\"generated_at\\\": \\\"2026-07-07T23:56:04.521255+00:00\\\",\\n  \\\"phase\\\": \\\"OOS_STATUS_SIGNAL_ONLY\\\",\\n  \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\\n  \\\"version\\\": \\\"E1R-v0.2-formal-sidecar-sleeve\\\",\\n  \\\"research_status\\\": \\\"FORMAL_SIDECAR_SLEEVE_ENGINE\\\",\\n  \\\"status_date\\\": \\\"2026-06-18\\\",\\n  \\\"market_state\\\": \\\"UPTREND\\\",\\n  \\\"regime\\\": \\\"UPTREND\\\",\\n  \\\"subclass\\\": null,\\n  \\\"mutually_exclusive_state_model\\\": true,\\n  \\\"core_active\\\": true,\\n  \\\"sidecar_active\\\": false,\\n  \\\"sidecar_selected_count\\\": 0,\\n  \\\"gross_exposure\\\": 0.25,\\n  \\\"top_n\\\": 10,\\n  \\\"execution_status\\\": \\\"NO_REAL_E...<truncated>"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].path",
          "key": "path",
          "value": "$"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys",
          "key": "keys",
          "value": [
            "generated_at",
            "phase",
            "strategy_id",
            "version",
            "research_status",
            "status_date",
            "market_state",
            "regime",
            "subclass",
            "mutually_exclusive_state_model",
            "core_active",
            "sidecar_active",
            "sidecar_selected_count",
            "gross_exposure",
            "top_n",
            "execution_status",
            "equity_status",
            "notes"
          ]
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[0]",
          "key": "[0]",
          "value": "generated_at"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[1]",
          "key": "[1]",
          "value": "phase"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[2]",
          "key": "[2]",
          "value": "strategy_id"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[3]",
          "key": "[3]",
          "value": "version"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[4]",
          "key": "[4]",
          "value": "research_status"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[5]",
          "key": "[5]",
          "value": "status_date"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[6]",
          "key": "[6]",
          "value": "market_state"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[7]",
          "key": "[7]",
          "value": "regime"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[8]",
          "key": "[8]",
          "value": "subclass"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[9]",
          "key": "[9]",
          "value": "mutually_exclusive_state_model"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[10]",
          "key": "[10]",
          "value": "core_active"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[11]",
          "key": "[11]",
          "value": "sidecar_active"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[12]",
          "key": "[12]",
          "value": "sidecar_selected_count"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[13]",
          "key": "[13]",
          "value": "gross_exposure"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[14]",
          "key": "[14]",
          "value": "top_n"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[15]",
          "key": "[15]",
          "value": "execution_status"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[16]",
          "key": "[16]",
          "value": "equity_status"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].keys[17]",
          "key": "[17]",
          "value": "notes"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].has_date",
          "key": "has_date",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].has_forward_metric",
          "key": "has_forward_metric",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].has_numeric_forward_metric",
          "key": "has_numeric_forward_metric",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].date_fields",
          "key": "date_fields",
          "value": {
            "status_date": "2026-06-18",
            "generated_at": "2026-07-07T23:56:04.521255+00:00"
          }
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].date_fields.status_date",
          "key": "status_date",
          "value": "2026-06-18"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].date_fields.generated_at",
          "key": "generated_at",
          "value": "2026-07-07T23:56:04.521255+00:00"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].forward_fields",
          "key": "forward_fields",
          "value": {
            "gross_exposure": 0.25
          }
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].forward_fields.gross_exposure",
          "key": "gross_exposure",
          "value": 0.25
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].numeric_forward_fields",
          "key": "numeric_forward_fields",
          "value": {
            "gross_exposure": 0.25
          }
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].numeric_forward_fields.gross_exposure",
          "key": "gross_exposure",
          "value": 0.25
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_records[0].preview",
          "key": "preview",
          "value": "{\n  \"generated_at\": \"2026-07-07T23:56:04.521255+00:00\",\n  \"phase\": \"OOS_STATUS_SIGNAL_ONLY\",\n  \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\",\n  \"version\": \"E1R-v0.2-formal-sidecar-sleeve\",\n  \"research_status\": \"FORMAL_SIDECAR_SLEEVE_ENGINE\",\n  \"status_date\": \"2026-06-18\",\n  \"market_state\": \"UPTREND\",\n  \"regime\": \"UPTREND\",\n  \"subclass\": null,\n  \"mutually_exclusive_state_model\": true,\n  \"core_active\": true,\n  \"sidecar_active\": false,\n  \"sidecar_selected_count\": 0,\n  \"gross_exposure\": 0.25,\n  \"top_n\": 10,\n  \"execution_status\": \"NO_REAL_EXECUTION\",\n  \"equity_status\": \"NOT_YET_CONNECTED\",\n  \"notes\": [\n    \"OOS-1 exports daily E1R v0.2 state and sidecar target signals only.\",\n    \"No real orders are executed by this script.\",\n    \"No E1R v0.2 OOS equity curve is updated by this script.\",\n    \"This is the bridge layer for Dashboard and future OOS equity integration.\"\n  ]\n}"
        },
        {
          "path": "target_reports.e1r_oos_summary.candidate_arrays",
          "key": "candidate_arrays",
          "value": []
        },
        {
          "path": "target_reports.e1r_oos_summary.top_level_preview",
          "key": "top_level_preview",
          "value": "{\n  \"generated_at\": \"2026-07-07T23:56:04.521255+00:00\",\n  \"phase\": \"OOS_STATUS_SIGNAL_ONLY\",\n  \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\",\n  \"version\": \"E1R-v0.2-formal-sidecar-sleeve\",\n  \"research_status\": \"FORMAL_SIDECAR_SLEEVE_ENGINE\",\n  \"status_date\": \"2026-06-18\",\n  \"market_state\": \"UPTREND\",\n  \"regime\": \"UPTREND\",\n  \"subclass\": null,\n  \"mutually_exclusive_state_model\": true,\n  \"core_active\": true,\n  \"sidecar_active\": false,\n  \"sidecar_selected_count\": 0,\n  \"gross_exposure\": 0.25,\n  \"top_n\": 10,\n  \"execution_status\": \"NO_REAL_EXECUTION\",\n  \"equity_status\": \"NOT_YET_CONNECTED\",\n  \"notes\": [\n    \"OOS-1 exports daily E1R v0.2 state and sidecar target signals only.\",\n    \"No real orders are executed by this script.\",\n    \"No E1R v0.2 OOS equity curve is updated by this script.\",\n    \"This is the bridge layer for Dashboard and future OOS equity integration.\"\n  ]\n}"
        },
        {
          "path": "target_reports.e1r_oos_equity_curve",
          "key": "e1r_oos_equity_curve",
          "value": "{\"name\": \"e1r_oos_equity_curve\", \"meta\": {\"exists\": true, \"valid_json\": true, \"path\": \"exports/oos_e1r_v0_2_equity_curve.json\", \"size_bytes\": 2632, \"type\": \"dict\", \"top_level_keys\": [\"generated_at\", \"strategy_id\", \"phase\", \"equity_status\", \"execution_status\", \"curve_type\", \"start_date\", \"end_date\", \"row_count\", \"latest\", \"records\", \"notes\"], \"array_length\": null}, \"term_presence\": {\"E1R_REGIME_AWARE_V0_2\": true, \"E1R\": true, \"v0.2\": false, \"sidecar\": true, \"regime\": false, \"UPTREND\": true, \"SIDEWAYS\": false, \"DOWNTREND\": false, \"MA_CONFLICT\": false}, \"candidate_records\": [{\"path\": \"$\", \"keys\": [\"generated_at\", \"strategy_id\", \"phase\", \"equity_status\", \"execution_status\", \"curve_type\", \"start_date\", \"end_date\", \"row_count\", \"latest\", \"records\", \"notes\"], \"has_date\": true, \"has_forward_metric\": false, \"has_numeric_forward_metric\": false, \"date_fields\": {\"generated_at\": \"2026-07-07T23:56:04.524822+00:00\"}, \"forward_fields\": {}, \"numeric_forward_fields\": {}, \"preview\": \"{\\n  \\\"generated_at\\\": \\\"2026-07-07T23:56:04.524822+00:00\\\",\\n  \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\\n  \\\"phase\\\": \\\"OOS_2B_FORWARD_EQUITY_CURVE\\\",\\n  \\\"equity_status\\\": \\\"OOS_EQUITY_MTM_TRACKING_SIDECAR_PAPER\\\",\\...<truncated>"
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.name",
          "key": "name",
          "value": "e1r_oos_equity_curve"
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.meta",
          "key": "meta",
          "value": {
            "exists": true,
            "valid_json": true,
            "path": "exports/oos_e1r_v0_2_equity_curve.json",
            "size_bytes": 2632,
            "type": "dict",
            "top_level_keys": [
              "generated_at",
              "strategy_id",
              "phase",
              "equity_status",
              "execution_status",
              "curve_type",
              "start_date",
              "end_date",
              "row_count",
              "latest",
              "records",
              "notes"
            ],
            "array_length": null
          }
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.meta.exists",
          "key": "exists",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.meta.valid_json",
          "key": "valid_json",
          "value": true
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.meta.path",
          "key": "path",
          "value": "exports/oos_e1r_v0_2_equity_curve.json"
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.meta.size_bytes",
          "key": "size_bytes",
          "value": 2632
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.meta.type",
          "key": "type",
          "value": "dict"
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.meta.top_level_keys",
          "key": "top_level_keys",
          "value": [
            "generated_at",
            "strategy_id",
            "phase",
            "equity_status",
            "execution_status",
            "curve_type",
            "start_date",
            "end_date",
            "row_count",
            "latest",
            "records",
            "notes"
          ]
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.meta.top_level_keys[0]",
          "key": "[0]",
          "value": "generated_at"
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.meta.top_level_keys[1]",
          "key": "[1]",
          "value": "strategy_id"
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.meta.top_level_keys[2]",
          "key": "[2]",
          "value": "phase"
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.meta.top_level_keys[3]",
          "key": "[3]",
          "value": "equity_status"
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.meta.top_level_keys[4]",
          "key": "[4]",
          "value": "execution_status"
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.meta.top_level_keys[5]",
          "key": "[5]",
          "value": "curve_type"
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.meta.top_level_keys[6]",
          "key": "[6]",
          "value": "start_date"
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.meta.top_level_keys[7]",
          "key": "[7]",
          "value": "end_date"
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.meta.top_level_keys[8]",
          "key": "[8]",
          "value": "row_count"
        },
        {
          "path": "target_reports.e1r_oos_equity_curve.meta.top_level_keys[9]",
          "key": "[9]",
          "value": "latest"
        }
      ],
      "counts": {
        "return_hits": 2,
        "metric_hits": 14,
        "market_hits": 16,
        "e1r_hits": 488
      },
      "score": 190
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
      "sha256": "12b57e8d324e2676f0984392098ffa5b625f8f636b90f081d1930460213bbf7f",
      "top_level": {
        "status": "AUDIT_COMPLETE_PLAN_DEFINED_NO_SOURCE_CHANGES"
      },
      "return_hits": [
        {
          "path": "json_summaries.exports/e1r_v0_2_backtest_summary.json.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "important_files.scripts/run_e1r_v0_2_oos_core.py.hits[14].line",
          "key": "line",
          "value": 117.0,
          "distance_to_target_116_74": 0.2600000000000051
        },
        {
          "path": "important_files.scripts/export_e1r_v0_2_status.py.hits[12].line",
          "key": "line",
          "value": 117.0,
          "distance_to_target_116_74": 0.2600000000000051
        },
        {
          "path": "important_files.scripts/export_e1r_v0_2_backtest_equity.py.hits[14].line",
          "key": "line",
          "value": 116.0,
          "distance_to_target_116_74": 0.7399999999999949
        },
        {
          "path": "important_files.scripts/export_e1r_v0_2_status.py.hits[11].line",
          "key": "line",
          "value": 116.0,
          "distance_to_target_116_74": 0.7399999999999949
        },
        {
          "path": "important_files.scripts/export_e1r_v0_2_status.py.hits[13].line",
          "key": "line",
          "value": 118.0,
          "distance_to_target_116_74": 1.2600000000000051
        },
        {
          "path": "important_files.scripts/export_e1r_v0_2_targets_preview.py.defs[9].line",
          "key": "line",
          "value": 118.0,
          "distance_to_target_116_74": 1.2600000000000051
        },
        {
          "path": "top_generator_candidates[32].defs[9].line",
          "key": "line",
          "value": 118.0,
          "distance_to_target_116_74": 1.2600000000000051
        },
        {
          "path": "important_files.src/engine/backtest.py.defs[1].line",
          "key": "line",
          "value": 115.0,
          "distance_to_target_116_74": 1.7399999999999949
        },
        {
          "path": "top_generator_candidates[8].defs[1].line",
          "key": "line",
          "value": 115.0,
          "distance_to_target_116_74": 1.7399999999999949
        },
        {
          "path": "top_generator_candidates[10].defs[1].line",
          "key": "line",
          "value": 115.0,
          "distance_to_target_116_74": 1.7399999999999949
        },
        {
          "path": "important_files.scripts/run_e1r_v0_2_forward_performance.py.defs[9].line",
          "key": "line",
          "value": 119.0,
          "distance_to_target_116_74": 2.260000000000005
        },
        {
          "path": "top_generator_candidates[21].defs[9].line",
          "key": "line",
          "value": 119.0,
          "distance_to_target_116_74": 2.260000000000005
        },
        {
          "path": "important_files.scripts/run_e1r_v0_2_forward_performance_core.py.defs[9].line",
          "key": "line",
          "value": 114.0,
          "distance_to_target_116_74": 2.739999999999995
        },
        {
          "path": "important_files.scripts/export_e1r_v0_2_backtest_equity.py.hits[13].line",
          "key": "line",
          "value": 114.0,
          "distance_to_target_116_74": 2.739999999999995
        },
        {
          "path": "important_files.src/engine/e1r_sidecar_sleeve.py.defs[8].line",
          "key": "line",
          "value": 114.0,
          "distance_to_target_116_74": 2.739999999999995
        },
        {
          "path": "top_generator_candidates[9].defs[9].line",
          "key": "line",
          "value": 114.0,
          "distance_to_target_116_74": 2.739999999999995
        },
        {
          "path": "top_generator_candidates[34].defs[8].line",
          "key": "line",
          "value": 114.0,
          "distance_to_target_116_74": 2.739999999999995
        },
        {
          "path": "important_files.scripts/run_e1r_v0_2_oos_core.py.hits[15].line",
          "key": "line",
          "value": 120.0,
          "distance_to_target_116_74": 3.260000000000005
        },
        {
          "path": "important_files.run_oos.py.hits[15].line",
          "key": "line",
          "value": 120.0,
          "distance_to_target_116_74": 3.260000000000005
        }
      ],
      "metric_hits": [
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.return_pct",
          "key": "return_pct",
          "value": 37.57
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 0
        },
        {
          "path": "json_summaries.exports/portfolio_backtest.json.total_return_pct",
          "key": "total_return_pct",
          "value": 7.52
        },
        {
          "path": "json_summaries.exports/portfolio_backtest.json.alpha_pct",
          "key": "alpha_pct",
          "value": -61.84
        },
        {
          "path": "json_summaries.exports/portfolio_backtest.json.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 38.1
        },
        {
          "path": "json_summaries.exports/portfolio_backtest.json.profit_factor",
          "key": "profit_factor",
          "value": 1.25
        },
        {
          "path": "json_summaries.exports/e1r_v0_2_backtest_summary.json.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "json_summaries.exports/e1r_v0_2_backtest_summary.json.spx_return_pct",
          "key": "spx_return_pct",
          "value": 76.844174428316
        },
        {
          "path": "json_summaries.exports/e1r_v0_2_backtest_summary.json.alpha_pct",
          "key": "alpha_pct",
          "value": 39.89942548515961
        },
        {
          "path": "json_summaries.exports/e1r_v0_2_backtest_summary.json.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        },
        {
          "path": "json_summaries.exports/e1r_v0_2_backtest_summary.json.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "json_summaries.exports/oos_e1r_v0_2_equity_curve.json.last_sample.forward_return_pct",
          "key": "forward_return_pct",
          "value": 0.0
        },
        {
          "path": "json_summaries.exports/oos_e1r_v0_2_equity_curve.json.last_sample.drawdown_pct",
          "key": "drawdown_pct",
          "value": 0.0
        },
        {
          "path": "canonical_export_plan.required_outputs[0].schema.metrics.total_return_pct",
          "key": "total_return_pct",
          "value": "number"
        },
        {
          "path": "canonical_export_plan.required_outputs[0].schema.metrics.spx_return_pct",
          "key": "spx_return_pct",
          "value": "number"
        },
        {
          "path": "canonical_export_plan.required_outputs[0].schema.metrics.alpha_pct",
          "key": "alpha_pct",
          "value": "number"
        },
        {
          "path": "canonical_export_plan.required_outputs[0].schema.metrics.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": "number"
        },
        {
          "path": "canonical_export_plan.required_outputs[0].schema.metrics.sharpe",
          "key": "sharpe",
          "value": "number | null"
        },
        {
          "path": "canonical_export_plan.required_outputs[0].schema.metrics.profit_factor",
          "key": "profit_factor",
          "value": "number | null"
        }
      ],
      "market_hits": [
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.entry_regime",
          "key": "entry_regime",
          "value": "UPTREND"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.exit_regime",
          "key": "exit_regime",
          "value": "UPTREND"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.dominant_regime",
          "key": "dominant_regime",
          "value": "UPTREND"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.regime_day_weights",
          "key": "regime_day_weights",
          "value": {
            "UPTREND": 34
          }
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.regime_day_weights.UPTREND",
          "key": "UPTREND",
          "value": 34
        },
        {
          "path": "json_summaries.exports/e1r_v0_2_backtest_equity_curve.json.equity_curve.last_sample.spx_regime",
          "key": "spx_regime",
          "value": "UPTREND"
        },
        {
          "path": "json_summaries.exports/e1r_v0_2_backtest_equity_curve.json.rows.last_sample.spx_regime",
          "key": "spx_regime",
          "value": "UPTREND"
        },
        {
          "path": "json_summaries.exports/oos_e1r_v0_2_equity_curve.json.last_sample.market_state",
          "key": "market_state",
          "value": "UPTREND"
        },
        {
          "path": "json_summaries.exports/oos_e1r_v0_2_equity_curve.json.last_sample.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "canonical_export_plan.validation_gates",
          "key": "validation_gates",
          "value": [
            "Each canonical backtest curve must have one row per date.",
            "Date range should start near 2021-06-11 and end near 2026-06-16/2026-06-18.",
            "E1 and E1R curves must use the same SPX date calendar or explicit null padding.",
            "E1R symbol-level diagnostic rows must not be used directly as portfolio equity.",
            "Dashboard should use exports/e1_e1r_5y_equity_comparison.json for historical chart once generated."
          ]
        },
        {
          "path": "canonical_export_plan.validation_gates[0]",
          "key": "[0]",
          "value": "Each canonical backtest curve must have one row per date."
        },
        {
          "path": "canonical_export_plan.validation_gates[1]",
          "key": "[1]",
          "value": "Date range should start near 2021-06-11 and end near 2026-06-16/2026-06-18."
        },
        {
          "path": "canonical_export_plan.validation_gates[2]",
          "key": "[2]",
          "value": "E1 and E1R curves must use the same SPX date calendar or explicit null padding."
        },
        {
          "path": "canonical_export_plan.validation_gates[3]",
          "key": "[3]",
          "value": "E1R symbol-level diagnostic rows must not be used directly as portfolio equity."
        },
        {
          "path": "canonical_export_plan.validation_gates[4]",
          "key": "[4]",
          "value": "Dashboard should use exports/e1_e1r_5y_equity_comparison.json for historical chart once generated."
        }
      ],
      "e1r_hits": [
        {
          "path": "prior_4c2_summary.top_e1",
          "key": "top_e1",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json"
        },
        {
          "path": "prior_4c2_summary.top_e1r",
          "key": "top_e1r",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json"
        },
        {
          "path": "prior_4c2_summary.preliminary_decision.dashboard_chart_should_not_use_current_e1r_backtest_equity_directly",
          "key": "dashboard_chart_should_not_use_current_e1r_backtest_equity_directly",
          "value": true
        },
        {
          "path": "prior_4c2_summary.preliminary_decision.reason",
          "key": "reason",
          "value": "E1R 5Y backtest equity artifact in exports is symbol-level/diagnostic rows, not one row per date."
        },
        {
          "path": "prior_4c2_summary.preliminary_decision.proposed_canonical_export_names[1]",
          "key": "[1]",
          "value": "exports/e1r_v0_2_portfolio_backtest_equity_curve.json"
        },
        {
          "path": "prior_4c2_summary.preliminary_decision.proposed_canonical_export_names[2]",
          "key": "[2]",
          "value": "exports/e1_e1r_5y_equity_comparison.json"
        },
        {
          "path": "prior_4c2_summary.diagnosis[1]",
          "key": "[1]",
          "value": "No strong E1R 5Y portfolio-level equity candidate found in v13/main JSON artifacts."
        },
        {
          "path": "prior_4c2_summary.diagnosis[2]",
          "key": "[2]",
          "value": "E1R 5Y symbol/diagnostic candidate exists: exports/e1r_v0_2_backtest_equity_curve.json list=rows rows=8819 unique_dates=859 max_rows_per_date=19."
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json",
          "key": "data/research/e1r/e1r_formal_backtest_v0_1.json",
          "value": "{\"exists\": true, \"json_valid\": true, \"type\": \"dict\", \"top_keys\": [\"comparison_base\", \"e1_metrics\", \"equity_curve\", \"metrics\", \"source\", \"spx_curve\", \"status\", \"trades\", \"variant_id\"], \"equity_curve\": {\"length\": 131, \"last_type\": \"float\", \"last_sample\": 170918.25}, \"spx_curve\": {\"length\": 131, \"last_type\": \"float\", \"last_sample\": 169361.75}, \"trades\": {\"length\": 39, \"last_type\": \"dict\", \"last_sample\": {\"symbol\": \"DELL\", \"entry_date\": \"2026-04-24\", \"exit_date\": \"2026-06-11\", \"entry_signal\": \"BUY\", \"exit_signal\": \"SIM_END\", \"entry_price\": 212.14, \"avg_cost\": 219.22, \"exit_price\": 391.45, \"effective_exit\": 366.59, \"return_pct\": 37.57, \"max_gain_pct\": 112.55, \"max_drawdown_in_trade\": 0, \"holding_days\": 34, \"size_units_at_exit\": 0.5, \"leader_score_entry\": 96.0, \"take_profit_triggered\": false, \"take_profit_exec_date\": null, \"realized_pnl_before_exit\": 1665.07, \"actions_during_trade\": [\"BUY\", \"BUY\", \"BUY\", \"HOLD\", \"HOLD\", \"REDUCE\", \"HOLD\", \"HOLD\", \"ADD\", \"ADD\", \"BUY\", \"BUY\", \"BUY\", \"HOLD\", \"REDUCE\", \"REDUCE\", \"HOLD\", \"HOLD\", \"HOLD\", \"REDUCE\", \"REDUCE\", \"REDUCE\", \"HOLD\", \"BUY\", \"BUY\", \"BUY\", \"BUY\", \"BUY\", \"BUY\", \"HOLD\", \"REDUCE\", \"REDUCE\", \"REDUCE\", \"REDUCE\", \"REDUCE\", \"REDUCE\", \"REDUCE\"], ...<truncated>"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.exists",
          "key": "exists",
          "value": true
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.json_valid",
          "key": "json_valid",
          "value": true
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.type",
          "key": "type",
          "value": "dict"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.top_keys",
          "key": "top_keys",
          "value": [
            "comparison_base",
            "e1_metrics",
            "equity_curve",
            "metrics",
            "source",
            "spx_curve",
            "status",
            "trades",
            "variant_id"
          ]
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.top_keys[0]",
          "key": "[0]",
          "value": "comparison_base"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.top_keys[1]",
          "key": "[1]",
          "value": "e1_metrics"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.top_keys[2]",
          "key": "[2]",
          "value": "equity_curve"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.top_keys[3]",
          "key": "[3]",
          "value": "metrics"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.top_keys[4]",
          "key": "[4]",
          "value": "source"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.top_keys[5]",
          "key": "[5]",
          "value": "spx_curve"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.top_keys[6]",
          "key": "[6]",
          "value": "status"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.top_keys[7]",
          "key": "[7]",
          "value": "trades"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.top_keys[8]",
          "key": "[8]",
          "value": "variant_id"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.equity_curve",
          "key": "equity_curve",
          "value": {
            "length": 131,
            "last_type": "float",
            "last_sample": 170918.25
          }
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.equity_curve.length",
          "key": "length",
          "value": 131
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.equity_curve.last_type",
          "key": "last_type",
          "value": "float"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.equity_curve.last_sample",
          "key": "last_sample",
          "value": 170918.25
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.spx_curve",
          "key": "spx_curve",
          "value": {
            "length": 131,
            "last_type": "float",
            "last_sample": 169361.75
          }
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.spx_curve.length",
          "key": "length",
          "value": 131
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.spx_curve.last_type",
          "key": "last_type",
          "value": "float"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.spx_curve.last_sample",
          "key": "last_sample",
          "value": 169361.75
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades",
          "key": "trades",
          "value": {
            "length": 39,
            "last_type": "dict",
            "last_sample": {
              "symbol": "DELL",
              "entry_date": "2026-04-24",
              "exit_date": "2026-06-11",
              "entry_signal": "BUY",
              "exit_signal": "SIM_END",
              "entry_price": 212.14,
              "avg_cost": 219.22,
              "exit_price": 391.45,
              "effective_exit": 366.59,
              "return_pct": 37.57,
              "max_gain_pct": 112.55,
              "max_drawdown_in_trade": 0,
              "holding_days": 34,
              "size_units_at_exit": 0.5,
              "leader_score_entry": 96.0,
              "take_profit_triggered": false,
              "take_profit_exec_date": null,
              "realized_pnl_before_exit": 1665.07,
              "actions_during_trade": [
                "BUY",
                "BUY",
                "BUY",
                "HOLD",
                "HOLD",
                "REDUCE",
                "HOLD",
                "HOLD",
                "ADD",
                "ADD",
                "BUY",
                "BUY",
                "BUY",
                "HOLD",
                "REDUCE",
                "REDUCE",
                "HOLD",
                "HOLD",
                "HOLD",
                "REDUCE",
                "REDUCE",
                "REDUCE",
                "HOLD",
                "BUY",
                "BUY",
                "BUY",
                "BUY",
                "BUY",
                "BUY",
                "HOLD",
                "REDUCE",
                "REDUCE",
                "REDUCE",
                "REDUCE",
                "REDUCE",
                "REDUCE",
                "REDUCE"
              ],
              "action_count": 37,
              "execution_model": "adverse_intraday_v1.0",
              "is_sim_end": true,
              "entry_regime": "UPTREND",
              "exit_regime": "UPTREND",
              "dominant_regime": "UPTREND",
              "entry_type": "E1R_UPTREND_CONFIRMED",
              "regime_day_weights": {
                "UPTREND": 34
              },
              "exit_type": "SIM_END",
              "exit_warning_log": [],
              "exit_warning_count": 0
            }
          }
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.length",
          "key": "length",
          "value": 39
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_type",
          "key": "last_type",
          "value": "dict"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample",
          "key": "last_sample",
          "value": {
            "symbol": "DELL",
            "entry_date": "2026-04-24",
            "exit_date": "2026-06-11",
            "entry_signal": "BUY",
            "exit_signal": "SIM_END",
            "entry_price": 212.14,
            "avg_cost": 219.22,
            "exit_price": 391.45,
            "effective_exit": 366.59,
            "return_pct": 37.57,
            "max_gain_pct": 112.55,
            "max_drawdown_in_trade": 0,
            "holding_days": 34,
            "size_units_at_exit": 0.5,
            "leader_score_entry": 96.0,
            "take_profit_triggered": false,
            "take_profit_exec_date": null,
            "realized_pnl_before_exit": 1665.07,
            "actions_during_trade": [
              "BUY",
              "BUY",
              "BUY",
              "HOLD",
              "HOLD",
              "REDUCE",
              "HOLD",
              "HOLD",
              "ADD",
              "ADD",
              "BUY",
              "BUY",
              "BUY",
              "HOLD",
              "REDUCE",
              "REDUCE",
              "HOLD",
              "HOLD",
              "HOLD",
              "REDUCE",
              "REDUCE",
              "REDUCE",
              "HOLD",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "HOLD",
              "REDUCE",
              "REDUCE",
              "REDUCE",
              "REDUCE",
              "REDUCE",
              "REDUCE",
              "REDUCE"
            ],
            "action_count": 37,
            "execution_model": "adverse_intraday_v1.0",
            "is_sim_end": true,
            "entry_regime": "UPTREND",
            "exit_regime": "UPTREND",
            "dominant_regime": "UPTREND",
            "entry_type": "E1R_UPTREND_CONFIRMED",
            "regime_day_weights": {
              "UPTREND": 34
            },
            "exit_type": "SIM_END",
            "exit_warning_log": [],
            "exit_warning_count": 0
          }
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.symbol",
          "key": "symbol",
          "value": "DELL"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.entry_date",
          "key": "entry_date",
          "value": "2026-04-24"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.exit_date",
          "key": "exit_date",
          "value": "2026-06-11"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.entry_signal",
          "key": "entry_signal",
          "value": "BUY"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.exit_signal",
          "key": "exit_signal",
          "value": "SIM_END"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.entry_price",
          "key": "entry_price",
          "value": 212.14
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.avg_cost",
          "key": "avg_cost",
          "value": 219.22
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.exit_price",
          "key": "exit_price",
          "value": 391.45
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.effective_exit",
          "key": "effective_exit",
          "value": 366.59
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.return_pct",
          "key": "return_pct",
          "value": 37.57
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.max_gain_pct",
          "key": "max_gain_pct",
          "value": 112.55
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 0
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.holding_days",
          "key": "holding_days",
          "value": 34
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.size_units_at_exit",
          "key": "size_units_at_exit",
          "value": 0.5
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.leader_score_entry",
          "key": "leader_score_entry",
          "value": 96.0
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.take_profit_triggered",
          "key": "take_profit_triggered",
          "value": false
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.take_profit_exec_date",
          "key": "take_profit_exec_date",
          "value": null
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.realized_pnl_before_exit",
          "key": "realized_pnl_before_exit",
          "value": 1665.07
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade",
          "key": "actions_during_trade",
          "value": [
            "BUY",
            "BUY",
            "BUY",
            "HOLD",
            "HOLD",
            "REDUCE",
            "HOLD",
            "HOLD",
            "ADD",
            "ADD",
            "BUY",
            "BUY",
            "BUY",
            "HOLD",
            "REDUCE",
            "REDUCE",
            "HOLD",
            "HOLD",
            "HOLD",
            "REDUCE",
            "REDUCE",
            "REDUCE",
            "HOLD",
            "BUY",
            "BUY",
            "BUY",
            "BUY",
            "BUY",
            "BUY",
            "HOLD",
            "REDUCE",
            "REDUCE",
            "REDUCE",
            "REDUCE",
            "REDUCE",
            "REDUCE",
            "REDUCE"
          ]
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[0]",
          "key": "[0]",
          "value": "BUY"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[1]",
          "key": "[1]",
          "value": "BUY"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[2]",
          "key": "[2]",
          "value": "BUY"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[3]",
          "key": "[3]",
          "value": "HOLD"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[4]",
          "key": "[4]",
          "value": "HOLD"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[5]",
          "key": "[5]",
          "value": "REDUCE"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[6]",
          "key": "[6]",
          "value": "HOLD"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[7]",
          "key": "[7]",
          "value": "HOLD"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[8]",
          "key": "[8]",
          "value": "ADD"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[9]",
          "key": "[9]",
          "value": "ADD"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[10]",
          "key": "[10]",
          "value": "BUY"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[11]",
          "key": "[11]",
          "value": "BUY"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[12]",
          "key": "[12]",
          "value": "BUY"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[13]",
          "key": "[13]",
          "value": "HOLD"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[14]",
          "key": "[14]",
          "value": "REDUCE"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[15]",
          "key": "[15]",
          "value": "REDUCE"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[16]",
          "key": "[16]",
          "value": "HOLD"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[17]",
          "key": "[17]",
          "value": "HOLD"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[18]",
          "key": "[18]",
          "value": "HOLD"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[19]",
          "key": "[19]",
          "value": "REDUCE"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[20]",
          "key": "[20]",
          "value": "REDUCE"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[21]",
          "key": "[21]",
          "value": "REDUCE"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[22]",
          "key": "[22]",
          "value": "HOLD"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[23]",
          "key": "[23]",
          "value": "BUY"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[24]",
          "key": "[24]",
          "value": "BUY"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[25]",
          "key": "[25]",
          "value": "BUY"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[26]",
          "key": "[26]",
          "value": "BUY"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[27]",
          "key": "[27]",
          "value": "BUY"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[28]",
          "key": "[28]",
          "value": "BUY"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[29]",
          "key": "[29]",
          "value": "HOLD"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[30]",
          "key": "[30]",
          "value": "REDUCE"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[31]",
          "key": "[31]",
          "value": "REDUCE"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[32]",
          "key": "[32]",
          "value": "REDUCE"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[33]",
          "key": "[33]",
          "value": "REDUCE"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[34]",
          "key": "[34]",
          "value": "REDUCE"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[35]",
          "key": "[35]",
          "value": "REDUCE"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.actions_during_trade[36]",
          "key": "[36]",
          "value": "REDUCE"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.action_count",
          "key": "action_count",
          "value": 37
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.execution_model",
          "key": "execution_model",
          "value": "adverse_intraday_v1.0"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.is_sim_end",
          "key": "is_sim_end",
          "value": true
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.entry_regime",
          "key": "entry_regime",
          "value": "UPTREND"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.exit_regime",
          "key": "exit_regime",
          "value": "UPTREND"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.dominant_regime",
          "key": "dominant_regime",
          "value": "UPTREND"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.entry_type",
          "key": "entry_type",
          "value": "E1R_UPTREND_CONFIRMED"
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.regime_day_weights",
          "key": "regime_day_weights",
          "value": {
            "UPTREND": 34
          }
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.regime_day_weights.UPTREND",
          "key": "UPTREND",
          "value": 34
        },
        {
          "path": "json_summaries.data/research/e1r/e1r_formal_backtest_v0_1.json.trades.last_sample.exit_type",
          "key": "exit_type",
          "value": "SIM_END"
        }
      ],
      "counts": {
        "return_hits": 31,
        "metric_hits": 19,
        "market_hits": 15,
        "e1r_hits": 2818
      },
      "score": 190
    },
    {
      "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
      "sha256": "7cc740f91ad676449ec2c4ce845287b3347d5b9de66091c1073c1a4f766da07e",
      "top_level": {},
      "return_hits": [
        {
          "path": "frozen_e1r_v0_2_target_metrics.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "curves.e1_5y_canonical[466].indexed",
          "key": "indexed",
          "value": 116.73020000000001,
          "distance_to_target_116_74": 0.009799999999984266
        },
        {
          "path": "curves.e1_5y_canonical[209].indexed",
          "key": "indexed",
          "value": 116.75012,
          "distance_to_target_116_74": 0.010120000000000573
        },
        {
          "path": "curves.e1_5y_canonical[751].indexed",
          "key": "indexed",
          "value": 116.75551,
          "distance_to_target_116_74": 0.01551000000000613
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[124].indexed",
          "key": "indexed",
          "value": 116.75857188084828,
          "distance_to_target_116_74": 0.01857188084828465
        },
        {
          "path": "curves.e1_5y_canonical[216].indexed",
          "key": "indexed",
          "value": 116.76597,
          "distance_to_target_116_74": 0.025970000000000937
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[504].indexed",
          "key": "indexed",
          "value": 116.76611332322804,
          "distance_to_target_116_74": 0.026113323228045715
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[538].indexed",
          "key": "indexed",
          "value": 116.70225808008736,
          "distance_to_target_116_74": 0.03774191991263365
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[533].indexed",
          "key": "indexed",
          "value": 116.70087040883652,
          "distance_to_target_116_74": 0.03912959116347281
        },
        {
          "path": "curves.e1_5y_canonical[777].indexed",
          "key": "indexed",
          "value": 116.69803,
          "distance_to_target_116_74": 0.04196999999999207
        },
        {
          "path": "curves.e1_5y_canonical[510].indexed",
          "key": "indexed",
          "value": 116.78489,
          "distance_to_target_116_74": 0.04489000000000942
        },
        {
          "path": "curves.e1_5y_canonical[742].indexed",
          "key": "indexed",
          "value": 116.79238999999998,
          "distance_to_target_116_74": 0.05238999999998839
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[776].indexed",
          "key": "indexed",
          "value": 116.81573788784623,
          "distance_to_target_116_74": 0.07573788784623048
        },
        {
          "path": "curves.e1_5y_canonical[505].indexed",
          "key": "indexed",
          "value": 116.64817000000001,
          "distance_to_target_116_74": 0.09182999999998742
        },
        {
          "path": "curves.e1_5y_canonical[124].indexed",
          "key": "indexed",
          "value": 116.83424,
          "distance_to_target_116_74": 0.09423999999999921
        },
        {
          "path": "curves.e1_5y_canonical[125].indexed",
          "key": "indexed",
          "value": 116.64197999999999,
          "distance_to_target_116_74": 0.09802000000000533
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[465].indexed",
          "key": "indexed",
          "value": 116.84783475298974,
          "distance_to_target_116_74": 0.10783475298974565
        },
        {
          "path": "curves.e1_5y_canonical[741].indexed",
          "key": "indexed",
          "value": 116.85233,
          "distance_to_target_116_74": 0.11233000000000004
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[121].indexed",
          "key": "indexed",
          "value": 116.6259598384868,
          "distance_to_target_116_74": 0.11404016151318785
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[208].indexed",
          "key": "indexed",
          "value": 116.86725919581747,
          "distance_to_target_116_74": 0.12725919581747291
        }
      ],
      "metric_hits": [
        {
          "path": "frozen_e1r_v0_2_target_metrics.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "frozen_e1r_v0_2_target_metrics.spx_return_pct",
          "key": "spx_return_pct",
          "value": 76.844174428316
        },
        {
          "path": "frozen_e1r_v0_2_target_metrics.alpha_pct",
          "key": "alpha_pct",
          "value": 39.89942548515961
        },
        {
          "path": "frozen_e1r_v0_2_target_metrics.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        },
        {
          "path": "frozen_e1r_v0_2_target_metrics.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "frozen_e1r_v0_2_target_metrics.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.7957270568329264
        },
        {
          "path": "summaries.e1_5y_canonical.total_return_pct",
          "key": "total_return_pct",
          "value": 89.81569
        },
        {
          "path": "summaries.e1r_5y_direct_composed_candidate.total_return_pct",
          "key": "total_return_pct",
          "value": 90.00639291282218
        },
        {
          "path": "summaries.e1_forward_oos.total_return_pct",
          "key": "total_return_pct",
          "value": -24.40002
        },
        {
          "path": "summaries.e1r_forward_oos_kickoff_ready.total_return_pct",
          "key": "total_return_pct",
          "value": 0.0
        }
      ],
      "market_hits": [
        {
          "path": "curves.e1r_forward_oos_kickoff_ready[0].market_state",
          "key": "market_state",
          "value": "UPTREND"
        },
        {
          "path": "curves.e1r_forward_oos_kickoff_ready[0].regime",
          "key": "regime",
          "value": "UPTREND"
        }
      ],
      "e1r_hits": [
        {
          "path": "artifact_type",
          "key": "artifact_type",
          "value": "e1_e1r_research_curve_bundle_noncanonical"
        },
        {
          "path": "official_e1r_canonical_ready",
          "key": "official_e1r_canonical_ready",
          "value": false
        },
        {
          "path": "warning.e1r_backtest_warning",
          "key": "e1r_backtest_warning",
          "value": "E1R 5Y curve is direct-composed candidate and NOT frozen E1R v0.2."
        },
        {
          "path": "warning.e1r_forward_warning",
          "key": "e1r_forward_warning",
          "value": "E1R forward/OOS is KICKOFF_READY and not official live until daily pipeline succeeds."
        },
        {
          "path": "sources.e1r_5y_candidate_comparison",
          "key": "e1r_5y_candidate_comparison",
          "value": "exports/e1_vs_e1r_direct_composed_5y_comparison_noncanonical.json"
        },
        {
          "path": "sources.e1r_oos",
          "key": "e1r_oos",
          "value": "exports/oos_e1r_v0_2_equity_curve.json"
        },
        {
          "path": "frozen_e1r_v0_2_target_metrics",
          "key": "frozen_e1r_v0_2_target_metrics",
          "value": {
            "strategy_id": "E1R_REGIME_AWARE_V0_2",
            "total_return_pct": 116.7435999134756,
            "spx_return_pct": 76.844174428316,
            "alpha_pct": 39.89942548515961,
            "max_drawdown_pct": 25.904809362815108,
            "profit_factor": 1.1919630955509348,
            "sharpe_ratio": 0.7957270568329264
          }
        },
        {
          "path": "frozen_e1r_v0_2_target_metrics.strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "frozen_e1r_v0_2_target_metrics.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "frozen_e1r_v0_2_target_metrics.spx_return_pct",
          "key": "spx_return_pct",
          "value": 76.844174428316
        },
        {
          "path": "frozen_e1r_v0_2_target_metrics.alpha_pct",
          "key": "alpha_pct",
          "value": 39.89942548515961
        },
        {
          "path": "frozen_e1r_v0_2_target_metrics.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        },
        {
          "path": "frozen_e1r_v0_2_target_metrics.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "frozen_e1r_v0_2_target_metrics.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.7957270568329264
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate",
          "key": "e1r_5y_direct_composed_candidate",
          "value": "[{\"date\": \"2021-06-14\", \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\", \"curve_type\": \"backtest_5y_candidate\", \"canonical\": false, \"warning\": \"NOT_FROZEN_E1R_V0_2\", \"equity\": 99900.4, \"indexed\": 100.0}, {\"date\": \"2021-06-15\", \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\", \"curve_type\": \"backtest_5y_candidate\", \"canonical\": false, \"warning\": \"NOT_FROZEN_E1R_V0_2\", \"equity\": 98350.944796, \"indexed\": 98.449}, {\"date\": \"2021-06-16\", \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\", \"curve_type\": \"backtest_5y_candidate\", \"canonical\": false, \"warning\": \"NOT_FROZEN_E1R_V0_2\", \"equity\": 99582.10192295632, \"indexed\": 99.68138458199999}, {\"date\": \"2021-06-17\", \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\", \"curve_type\": \"backtest_5y_candidate\", \"canonical\": false, \"warning\": \"NOT_FROZEN_E1R_V0_2\", \"equity\": 102541.38324580081, \"indexed\": 102.64361628762329}, {\"date\": \"2021-06-18\", \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\", \"curve_type\": \"backtest_5y_candidate\", \"canonical\": false, \"warning\": \"NOT_FROZEN_E1R_V0_2\", \"equity\": 101969.61249282223, \"indexed\": 102.0712754832035}, {\"date\": \"2021-06-21\", \"...<truncated>"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[0]",
          "key": "[0]",
          "value": {
            "date": "2021-06-14",
            "strategy_id": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE",
            "curve_type": "backtest_5y_candidate",
            "canonical": false,
            "warning": "NOT_FROZEN_E1R_V0_2",
            "equity": 99900.4,
            "indexed": 100.0
          }
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[0].date",
          "key": "date",
          "value": "2021-06-14"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[0].strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[0].curve_type",
          "key": "curve_type",
          "value": "backtest_5y_candidate"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[0].canonical",
          "key": "canonical",
          "value": false
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[0].warning",
          "key": "warning",
          "value": "NOT_FROZEN_E1R_V0_2"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[0].equity",
          "key": "equity",
          "value": 99900.4
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[0].indexed",
          "key": "indexed",
          "value": 100.0
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[1]",
          "key": "[1]",
          "value": {
            "date": "2021-06-15",
            "strategy_id": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE",
            "curve_type": "backtest_5y_candidate",
            "canonical": false,
            "warning": "NOT_FROZEN_E1R_V0_2",
            "equity": 98350.944796,
            "indexed": 98.449
          }
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[1].date",
          "key": "date",
          "value": "2021-06-15"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[1].strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[1].curve_type",
          "key": "curve_type",
          "value": "backtest_5y_candidate"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[1].canonical",
          "key": "canonical",
          "value": false
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[1].warning",
          "key": "warning",
          "value": "NOT_FROZEN_E1R_V0_2"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[1].equity",
          "key": "equity",
          "value": 98350.944796
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[1].indexed",
          "key": "indexed",
          "value": 98.449
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[2]",
          "key": "[2]",
          "value": {
            "date": "2021-06-16",
            "strategy_id": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE",
            "curve_type": "backtest_5y_candidate",
            "canonical": false,
            "warning": "NOT_FROZEN_E1R_V0_2",
            "equity": 99582.10192295632,
            "indexed": 99.68138458199999
          }
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[2].date",
          "key": "date",
          "value": "2021-06-16"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[2].strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[2].curve_type",
          "key": "curve_type",
          "value": "backtest_5y_candidate"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[2].canonical",
          "key": "canonical",
          "value": false
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[2].warning",
          "key": "warning",
          "value": "NOT_FROZEN_E1R_V0_2"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[2].equity",
          "key": "equity",
          "value": 99582.10192295632
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[2].indexed",
          "key": "indexed",
          "value": 99.68138458199999
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[3]",
          "key": "[3]",
          "value": {
            "date": "2021-06-17",
            "strategy_id": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE",
            "curve_type": "backtest_5y_candidate",
            "canonical": false,
            "warning": "NOT_FROZEN_E1R_V0_2",
            "equity": 102541.38324580081,
            "indexed": 102.64361628762329
          }
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[3].date",
          "key": "date",
          "value": "2021-06-17"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[3].strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[3].curve_type",
          "key": "curve_type",
          "value": "backtest_5y_candidate"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[3].canonical",
          "key": "canonical",
          "value": false
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[3].warning",
          "key": "warning",
          "value": "NOT_FROZEN_E1R_V0_2"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[3].equity",
          "key": "equity",
          "value": 102541.38324580081
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[3].indexed",
          "key": "indexed",
          "value": 102.64361628762329
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[4]",
          "key": "[4]",
          "value": {
            "date": "2021-06-18",
            "strategy_id": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE",
            "curve_type": "backtest_5y_candidate",
            "canonical": false,
            "warning": "NOT_FROZEN_E1R_V0_2",
            "equity": 101969.61249282223,
            "indexed": 102.0712754832035
          }
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[4].date",
          "key": "date",
          "value": "2021-06-18"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[4].strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[4].curve_type",
          "key": "curve_type",
          "value": "backtest_5y_candidate"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[4].canonical",
          "key": "canonical",
          "value": false
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[4].warning",
          "key": "warning",
          "value": "NOT_FROZEN_E1R_V0_2"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[4].equity",
          "key": "equity",
          "value": 101969.61249282223
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[4].indexed",
          "key": "indexed",
          "value": 102.0712754832035
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[5]",
          "key": "[5]",
          "value": {
            "date": "2021-06-21",
            "strategy_id": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE",
            "curve_type": "backtest_5y_candidate",
            "canonical": false,
            "warning": "NOT_FROZEN_E1R_V0_2",
            "equity": 102884.07597765786,
            "indexed": 102.98665068173688
          }
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[5].date",
          "key": "date",
          "value": "2021-06-21"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[5].strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[5].curve_type",
          "key": "curve_type",
          "value": "backtest_5y_candidate"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[5].canonical",
          "key": "canonical",
          "value": false
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[5].warning",
          "key": "warning",
          "value": "NOT_FROZEN_E1R_V0_2"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[5].equity",
          "key": "equity",
          "value": 102884.07597765786
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[5].indexed",
          "key": "indexed",
          "value": 102.98665068173688
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[6]",
          "key": "[6]",
          "value": {
            "date": "2021-06-22",
            "strategy_id": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE",
            "curve_type": "backtest_5y_candidate",
            "canonical": false,
            "warning": "NOT_FROZEN_E1R_V0_2",
            "equity": 102972.3505148467,
            "indexed": 103.07501322802182
          }
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[6].date",
          "key": "date",
          "value": "2021-06-22"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[6].strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[6].curve_type",
          "key": "curve_type",
          "value": "backtest_5y_candidate"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[6].canonical",
          "key": "canonical",
          "value": false
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[6].warning",
          "key": "warning",
          "value": "NOT_FROZEN_E1R_V0_2"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[6].equity",
          "key": "equity",
          "value": 102972.3505148467
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[6].indexed",
          "key": "indexed",
          "value": 103.07501322802182
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[7]",
          "key": "[7]",
          "value": {
            "date": "2021-06-23",
            "strategy_id": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE",
            "curve_type": "backtest_5y_candidate",
            "canonical": false,
            "warning": "NOT_FROZEN_E1R_V0_2",
            "equity": 103187.87164447426,
            "indexed": 103.29074923070804
          }
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[7].date",
          "key": "date",
          "value": "2021-06-23"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[7].strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[7].curve_type",
          "key": "curve_type",
          "value": "backtest_5y_candidate"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[7].canonical",
          "key": "canonical",
          "value": false
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[7].warning",
          "key": "warning",
          "value": "NOT_FROZEN_E1R_V0_2"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[7].equity",
          "key": "equity",
          "value": 103187.87164447426
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[7].indexed",
          "key": "indexed",
          "value": 103.29074923070804
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[8]",
          "key": "[8]",
          "value": {
            "date": "2021-06-24",
            "strategy_id": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE",
            "curve_type": "backtest_5y_candidate",
            "canonical": false,
            "warning": "NOT_FROZEN_E1R_V0_2",
            "equity": 103549.02919522993,
            "indexed": 103.65226685301553
          }
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[8].date",
          "key": "date",
          "value": "2021-06-24"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[8].strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[8].curve_type",
          "key": "curve_type",
          "value": "backtest_5y_candidate"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[8].canonical",
          "key": "canonical",
          "value": false
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[8].warning",
          "key": "warning",
          "value": "NOT_FROZEN_E1R_V0_2"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[8].equity",
          "key": "equity",
          "value": 103549.02919522993
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[8].indexed",
          "key": "indexed",
          "value": 103.65226685301553
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[9]",
          "key": "[9]",
          "value": {
            "date": "2021-06-25",
            "strategy_id": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE",
            "curve_type": "backtest_5y_candidate",
            "canonical": false,
            "warning": "NOT_FROZEN_E1R_V0_2",
            "equity": 103829.12931920303,
            "indexed": 103.93264623485294
          }
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[9].date",
          "key": "date",
          "value": "2021-06-25"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[9].strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[9].curve_type",
          "key": "curve_type",
          "value": "backtest_5y_candidate"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[9].canonical",
          "key": "canonical",
          "value": false
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[9].warning",
          "key": "warning",
          "value": "NOT_FROZEN_E1R_V0_2"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[9].equity",
          "key": "equity",
          "value": 103829.12931920303
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[9].indexed",
          "key": "indexed",
          "value": 103.93264623485294
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[10]",
          "key": "[10]",
          "value": {
            "date": "2021-06-28",
            "strategy_id": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE",
            "curve_type": "backtest_5y_candidate",
            "canonical": false,
            "warning": "NOT_FROZEN_E1R_V0_2",
            "equity": 104147.57325882501,
            "indexed": 104.25140766085524
          }
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[10].date",
          "key": "date",
          "value": "2021-06-28"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[10].strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[10].curve_type",
          "key": "curve_type",
          "value": "backtest_5y_candidate"
        },
        {
          "path": "curves.e1r_5y_direct_composed_candidate[10].canonical",
          "key": "canonical",
          "value": false
        }
      ],
      "counts": {
        "return_hits": 958,
        "metric_hits": 10,
        "market_hits": 2,
        "e1r_hits": 10112
      },
      "score": 190
    },
    {
      "path": "exports/e1r_combined_5y_original_max3_result.json",
      "sha256": "6bbae48535fdd2cff7b2a6c2ecc063b6984b08254bcf622dfc44efca9d18fe6f",
      "top_level": {},
      "return_hits": [
        {
          "path": "rows[664].spx_equity_index",
          "key": "spx_equity_index",
          "value": 116.7434956557047,
          "distance_to_target_116_74": 0.003495655704710998
        },
        {
          "path": "rows[859].indexed_100",
          "key": "indexed_100",
          "value": 116.70017521903482,
          "distance_to_target_116_74": 0.03982478096517639
        },
        {
          "path": "rows[1157].indexed_100",
          "key": "indexed_100",
          "value": 116.79258460871738,
          "distance_to_target_116_74": 0.0525846087173818
        },
        {
          "path": "rows[666].spx_equity_index",
          "key": "spx_equity_index",
          "value": 116.6403774701426,
          "distance_to_target_116_74": 0.09962252985739894
        },
        {
          "path": "rows[671].spx_equity_index",
          "key": "spx_equity_index",
          "value": 116.61541989535108,
          "distance_to_target_116_74": 0.12458010464891345
        },
        {
          "path": "rows[1055].indexed_100",
          "key": "indexed_100",
          "value": 116.60526986318258,
          "distance_to_target_116_74": 0.13473013681741008
        },
        {
          "path": "rows[1150].indexed_100",
          "key": "indexed_100",
          "value": 116.89436353722895,
          "distance_to_target_116_74": 0.15436353722896
        },
        {
          "path": "rows[717].spx_equity_index",
          "key": "spx_equity_index",
          "value": 116.94644418752014,
          "distance_to_target_116_74": 0.20644418752014815
        },
        {
          "path": "rows[1054].indexed_100",
          "key": "indexed_100",
          "value": 116.94788330326331,
          "distance_to_target_116_74": 0.2078833032633156
        },
        {
          "path": "rows[860].indexed_100",
          "key": "indexed_100",
          "value": 116.97582685996124,
          "distance_to_target_116_74": 0.23582685996125008
        },
        {
          "path": "rows[894].indexed_100",
          "key": "indexed_100",
          "value": 116.48871555059262,
          "distance_to_target_116_74": 0.25128444940737893
        },
        {
          "path": "rows[931].indexed_100",
          "key": "indexed_100",
          "value": 117.06777464467271,
          "distance_to_target_116_74": 0.327774644672715
        },
        {
          "path": "rows[665].spx_equity_index",
          "key": "spx_equity_index",
          "value": 116.37151149066717,
          "distance_to_target_116_74": 0.3684885093328205
        },
        {
          "path": "rows[675].spx_equity_index",
          "key": "spx_equity_index",
          "value": 117.14138010456689,
          "distance_to_target_116_74": 0.401380104566897
        },
        {
          "path": "rows[1115].indexed_100",
          "key": "indexed_100",
          "value": 117.1618292998564,
          "distance_to_target_116_74": 0.42182929985639817
        },
        {
          "path": "rows[376].sidecar_live_positions[2].score",
          "key": "score",
          "value": 116.28806430047702,
          "distance_to_target_116_74": 0.4519356995229771
        },
        {
          "path": "rows[1119].indexed_100",
          "key": "indexed_100",
          "value": 117.19938983182871,
          "distance_to_target_116_74": 0.45938983182871596
        },
        {
          "path": "rows[863].indexed_100",
          "key": "indexed_100",
          "value": 117.19976918839208,
          "distance_to_target_116_74": 0.45976918839208736
        },
        {
          "path": "rows[1056].indexed_100",
          "key": "indexed_100",
          "value": 117.26404291567718,
          "distance_to_target_116_74": 0.5240429156771853
        },
        {
          "path": "rows[929].indexed_100",
          "key": "indexed_100",
          "value": 116.20842018973867,
          "distance_to_target_116_74": 0.5315798102613201
        }
      ],
      "metric_hits": [
        {
          "path": "metrics.total_return_pct",
          "key": "total_return_pct",
          "value": 48.901700114733984
        },
        {
          "path": "metrics.cagr_pct",
          "key": "cagr_pct",
          "value": 8.294748607300061
        },
        {
          "path": "metrics.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 41.06978999999992
        },
        {
          "path": "metrics.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.47338246180914334
        },
        {
          "path": "metrics.spx_total_return_pct",
          "key": "spx_total_return_pct",
          "value": 74.37928789564872
        },
        {
          "path": "metrics.alpha_pct",
          "key": "alpha_pct",
          "value": -25.47758778091473
        },
        {
          "path": "rows[0].daily_return",
          "key": "daily_return",
          "value": 0.0
        },
        {
          "path": "rows[0].daily_return_pct",
          "key": "daily_return_pct",
          "value": 0.0
        },
        {
          "path": "rows[0].spx_return",
          "key": "spx_return",
          "value": 0.0018152018879837861
        },
        {
          "path": "rows[0].spx_return_pct",
          "key": "spx_return_pct",
          "value": 0.1815201887983786
        },
        {
          "path": "rows[0].core_daily_return",
          "key": "core_daily_return",
          "value": 0.0
        },
        {
          "path": "rows[0].sidecar_adapter_return",
          "key": "sidecar_adapter_return",
          "value": 0.0
        },
        {
          "path": "rows[1].daily_return",
          "key": "daily_return",
          "value": -0.050000000000000044
        },
        {
          "path": "rows[1].daily_return_pct",
          "key": "daily_return_pct",
          "value": -5.000000000000004
        },
        {
          "path": "rows[1].spx_return",
          "key": "spx_return",
          "value": -0.002011693641151502
        },
        {
          "path": "rows[1].spx_return_pct",
          "key": "spx_return_pct",
          "value": -0.20116936411515018
        },
        {
          "path": "rows[1].core_daily_return",
          "key": "core_daily_return",
          "value": -0.050000000000000044
        },
        {
          "path": "rows[1].sidecar_adapter_return",
          "key": "sidecar_adapter_return",
          "value": 0.0
        },
        {
          "path": "rows[2].daily_return",
          "key": "daily_return",
          "value": -0.05045578947368423
        },
        {
          "path": "rows[2].daily_return_pct",
          "key": "daily_return_pct",
          "value": -5.045578947368423
        },
        {
          "path": "rows[2].spx_return",
          "key": "spx_return",
          "value": -0.00539012474499756
        },
        {
          "path": "rows[2].spx_return_pct",
          "key": "spx_return_pct",
          "value": -0.539012474499756
        },
        {
          "path": "rows[2].core_daily_return",
          "key": "core_daily_return",
          "value": -0.05045578947368423
        },
        {
          "path": "rows[2].sidecar_adapter_return",
          "key": "sidecar_adapter_return",
          "value": 0.0
        },
        {
          "path": "rows[3].daily_return",
          "key": "daily_return",
          "value": -0.048303618245651325
        },
        {
          "path": "rows[3].daily_return_pct",
          "key": "daily_return_pct",
          "value": -4.8303618245651325
        },
        {
          "path": "rows[3].spx_return",
          "key": "spx_return",
          "value": -0.0004357155846854699
        },
        {
          "path": "rows[3].spx_return_pct",
          "key": "spx_return_pct",
          "value": -0.04357155846854699
        },
        {
          "path": "rows[3].core_daily_return",
          "key": "core_daily_return",
          "value": -0.048303618245651325
        },
        {
          "path": "rows[3].sidecar_adapter_return",
          "key": "sidecar_adapter_return",
          "value": 0.0
        },
        {
          "path": "rows[4].daily_return",
          "key": "daily_return",
          "value": -0.05000221900237156
        },
        {
          "path": "rows[4].daily_return_pct",
          "key": "daily_return_pct",
          "value": -5.000221900237156
        },
        {
          "path": "rows[4].spx_return",
          "key": "spx_return",
          "value": -0.013124468788176635
        },
        {
          "path": "rows[4].spx_return_pct",
          "key": "spx_return_pct",
          "value": -1.3124468788176635
        },
        {
          "path": "rows[4].core_daily_return",
          "key": "core_daily_return",
          "value": -0.05000221900237156
        },
        {
          "path": "rows[4].sidecar_adapter_return",
          "key": "sidecar_adapter_return",
          "value": 0.0
        },
        {
          "path": "rows[5].daily_return",
          "key": "daily_return",
          "value": -0.05257444725898164
        },
        {
          "path": "rows[5].daily_return_pct",
          "key": "daily_return_pct",
          "value": -5.257444725898164
        },
        {
          "path": "rows[5].spx_return",
          "key": "spx_return",
          "value": 0.014002290023774178
        },
        {
          "path": "rows[5].spx_return_pct",
          "key": "spx_return_pct",
          "value": 1.4002290023774178
        },
        {
          "path": "rows[5].core_daily_return",
          "key": "core_daily_return",
          "value": -0.05257444725898164
        },
        {
          "path": "rows[5].sidecar_adapter_return",
          "key": "sidecar_adapter_return",
          "value": 0.0
        },
        {
          "path": "rows[6].daily_return",
          "key": "daily_return",
          "value": 0.0034620642475573504
        },
        {
          "path": "rows[6].daily_return_pct",
          "key": "daily_return_pct",
          "value": 0.34620642475573504
        },
        {
          "path": "rows[6].spx_return",
          "key": "spx_return",
          "value": 0.005124491820929222
        },
        {
          "path": "rows[6].spx_return_pct",
          "key": "spx_return_pct",
          "value": 0.5124491820929222
        },
        {
          "path": "rows[6].core_daily_return",
          "key": "core_daily_return",
          "value": 0.0034620642475573504
        },
        {
          "path": "rows[6].sidecar_adapter_return",
          "key": "sidecar_adapter_return",
          "value": 0.0
        },
        {
          "path": "rows[7].daily_return",
          "key": "daily_return",
          "value": -0.048922545321915756
        },
        {
          "path": "rows[7].daily_return_pct",
          "key": "daily_return_pct",
          "value": -4.892254532191576
        },
        {
          "path": "rows[7].spx_return",
          "key": "spx_return",
          "value": -0.0010832831887211958
        },
        {
          "path": "rows[7].spx_return_pct",
          "key": "spx_return_pct",
          "value": -0.10832831887211958
        },
        {
          "path": "rows[7].core_daily_return",
          "key": "core_daily_return",
          "value": -0.048922545321915756
        },
        {
          "path": "rows[7].sidecar_adapter_return",
          "key": "sidecar_adapter_return",
          "value": 0.0
        },
        {
          "path": "rows[8].daily_return",
          "key": "daily_return",
          "value": -0.04769811871365426
        },
        {
          "path": "rows[8].daily_return_pct",
          "key": "daily_return_pct",
          "value": -4.769811871365426
        },
        {
          "path": "rows[8].spx_return",
          "key": "spx_return",
          "value": 0.0058112495772011385
        },
        {
          "path": "rows[8].spx_return_pct",
          "key": "spx_return_pct",
          "value": 0.5811249577201139
        },
        {
          "path": "rows[8].core_daily_return",
          "key": "core_daily_return",
          "value": -0.04769811871365426
        },
        {
          "path": "rows[8].sidecar_adapter_return",
          "key": "sidecar_adapter_return",
          "value": 0.0
        },
        {
          "path": "rows[9].daily_return",
          "key": "daily_return",
          "value": -0.05092476762441123
        },
        {
          "path": "rows[9].daily_return_pct",
          "key": "daily_return_pct",
          "value": -5.092476762441123
        },
        {
          "path": "rows[9].spx_return",
          "key": "spx_return",
          "value": 0.003330597334258556
        },
        {
          "path": "rows[9].spx_return_pct",
          "key": "spx_return_pct",
          "value": 0.3330597334258556
        },
        {
          "path": "rows[9].core_daily_return",
          "key": "core_daily_return",
          "value": -0.05092476762441123
        },
        {
          "path": "rows[9].sidecar_adapter_return",
          "key": "sidecar_adapter_return",
          "value": 0.0
        },
        {
          "path": "rows[10].daily_return",
          "key": "daily_return",
          "value": -0.051199618541889036
        },
        {
          "path": "rows[10].daily_return_pct",
          "key": "daily_return_pct",
          "value": -5.119961854188904
        },
        {
          "path": "rows[10].spx_return",
          "key": "spx_return",
          "value": 0.002314964269531039
        },
        {
          "path": "rows[10].spx_return_pct",
          "key": "spx_return_pct",
          "value": 0.2314964269531039
        },
        {
          "path": "rows[10].core_daily_return",
          "key": "core_daily_return",
          "value": -0.051199618541889036
        },
        {
          "path": "rows[10].sidecar_adapter_return",
          "key": "sidecar_adapter_return",
          "value": 0.0
        },
        {
          "path": "rows[11].daily_return",
          "key": "daily_return",
          "value": -0.043557981557974856
        },
        {
          "path": "rows[11].daily_return_pct",
          "key": "daily_return_pct",
          "value": -4.355798155797485
        },
        {
          "path": "rows[11].spx_return",
          "key": "spx_return",
          "value": 0.0002773363316626032
        },
        {
          "path": "rows[11].spx_return_pct",
          "key": "spx_return_pct",
          "value": 0.02773363316626032
        },
        {
          "path": "rows[11].core_daily_return",
          "key": "core_daily_return",
          "value": -0.043557981557974856
        },
        {
          "path": "rows[11].sidecar_adapter_return",
          "key": "sidecar_adapter_return",
          "value": 0.0
        },
        {
          "path": "rows[12].daily_return",
          "key": "daily_return",
          "value": 0.0025266766761553594
        },
        {
          "path": "rows[12].daily_return_pct",
          "key": "daily_return_pct",
          "value": 0.25266766761553594
        },
        {
          "path": "rows[12].spx_return",
          "key": "spx_return",
          "value": 0.0013281595738365848
        },
        {
          "path": "rows[12].spx_return_pct",
          "key": "spx_return_pct",
          "value": 0.13281595738365848
        },
        {
          "path": "rows[12].core_daily_return",
          "key": "core_daily_return",
          "value": 0.0025266766761553594
        },
        {
          "path": "rows[12].sidecar_adapter_return",
          "key": "sidecar_adapter_return",
          "value": 0.0
        },
        {
          "path": "rows[13].daily_return",
          "key": "daily_return",
          "value": -0.004912144599287904
        },
        {
          "path": "rows[13].daily_return_pct",
          "key": "daily_return_pct",
          "value": -0.4912144599287904
        },
        {
          "path": "rows[13].spx_return",
          "key": "spx_return",
          "value": 0.005221626759744025
        },
        {
          "path": "rows[13].spx_return_pct",
          "key": "spx_return_pct",
          "value": 0.5221626759744025
        },
        {
          "path": "rows[13].core_daily_return",
          "key": "core_daily_return",
          "value": -0.004912144599287904
        },
        {
          "path": "rows[13].sidecar_adapter_return",
          "key": "sidecar_adapter_return",
          "value": 0.0
        },
        {
          "path": "rows[14].daily_return",
          "key": "daily_return",
          "value": 0.0005054892821356738
        },
        {
          "path": "rows[14].daily_return_pct",
          "key": "daily_return_pct",
          "value": 0.05054892821356738
        },
        {
          "path": "rows[14].spx_return",
          "key": "spx_return",
          "value": 0.007500081816531168
        },
        {
          "path": "rows[14].spx_return_pct",
          "key": "spx_return_pct",
          "value": 0.7500081816531168
        },
        {
          "path": "rows[14].core_daily_return",
          "key": "core_daily_return",
          "value": 0.0005054892821356738
        },
        {
          "path": "rows[14].sidecar_adapter_return",
          "key": "sidecar_adapter_return",
          "value": 0.0
        },
        {
          "path": "rows[15].daily_return",
          "key": "daily_return",
          "value": 0.006318239705486617
        },
        {
          "path": "rows[15].daily_return_pct",
          "key": "daily_return_pct",
          "value": 0.6318239705486617
        },
        {
          "path": "rows[15].spx_return",
          "key": "spx_return",
          "value": -0.002021856131508404
        },
        {
          "path": "rows[15].spx_return_pct",
          "key": "spx_return_pct",
          "value": -0.20218561315084038
        }
      ],
      "market_hits": [
        {
          "path": "regime_counts",
          "key": "regime_counts",
          "value": {
            "UPTREND": 860,
            "SIDEWAYS": 241,
            "DOWNTREND": 158
          }
        },
        {
          "path": "regime_counts.UPTREND",
          "key": "UPTREND",
          "value": 860
        },
        {
          "path": "regime_counts.SIDEWAYS",
          "key": "SIDEWAYS",
          "value": 241
        },
        {
          "path": "regime_counts.DOWNTREND",
          "key": "DOWNTREND",
          "value": 158
        },
        {
          "path": "rows[0].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[0].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[1].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[1].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[2].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[2].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[3].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[3].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[4].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[4].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[5].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[5].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[6].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[6].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[7].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[7].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[8].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[8].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[9].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[9].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[10].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[10].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[11].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[11].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[12].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[12].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[13].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[13].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[14].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[14].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[15].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[15].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[16].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[16].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[17].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[17].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[18].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[18].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[19].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[19].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[20].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[20].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[21].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[21].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[22].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[22].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[23].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[23].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[24].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[24].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[25].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[25].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[26].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[26].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[27].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[27].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[28].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[28].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[29].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[29].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[30].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[30].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[31].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[31].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[32].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[32].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[33].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[33].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[34].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[34].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[35].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[35].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[36].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[36].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[37].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[37].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[38].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[38].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[39].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[39].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[40].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[40].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[41].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[41].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[42].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[42].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[43].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[43].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[44].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[44].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[45].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[45].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[46].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[46].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[47].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[47].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[48].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[48].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[49].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[49].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[50].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[50].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[51].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[51].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[52].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[52].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[53].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[53].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[54].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[54].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[55].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[55].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[56].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[56].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[57].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[57].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[58].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[58].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[59].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[59].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[60].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[60].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[61].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[61].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[62].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[62].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[63].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[63].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[64].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[64].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[65].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[65].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[66].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[66].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[67].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[67].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[68].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[68].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[69].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[69].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[70].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[70].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[71].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[71].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[72].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[72].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[73].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[73].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[74].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[74].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[75].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[75].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[76].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[76].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[77].regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "rows[77].sidecar_meta.regime",
          "key": "regime",
          "value": "UPTREND"
        }
      ],
      "e1r_hits": [
        {
          "path": "artifact_type",
          "key": "artifact_type",
          "value": "e1r_combined_5y_original_max3_result"
        },
        {
          "path": "contract.strategy_id",
          "key": "strategy_id",
          "value": "E1R_COMBINED_5Y_ORIGINAL_MAX3"
        },
        {
          "path": "contract.sideways_ma_conflict",
          "key": "sideways_ma_conflict",
          "value": "Call original build_e1r_sidecar_sleeve with original defaults: allowed_subclasses=('MA_CONFLICT',), top_n=10, gross_exposure=0.25."
        },
        {
          "path": "source_core_result",
          "key": "source_core_result",
          "value": "exports/e1r_unified_5y_full_account_v1_result.json"
        },
        {
          "path": "sidecar_source.module",
          "key": "module",
          "value": "src.engine.e1r_sidecar_sleeve"
        },
        {
          "path": "sidecar_source.function",
          "key": "function",
          "value": "build_e1r_sidecar_sleeve"
        },
        {
          "path": "conclusion",
          "key": "conclusion",
          "value": "E1R_COMBINED_5Y_ORIGINAL_MAX3_FULL_RUN_VALIDATED"
        }
      ],
      "counts": {
        "return_hits": 247,
        "metric_hits": 8640,
        "market_hits": 2522,
        "e1r_hits": 7
      },
      "score": 190
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json",
      "sha256": "3a8c69a37b1557d53d6863db0ee7f1ed24e84c763be7d369fffa2c25c616af87",
      "top_level": {
        "status": "AUDIT_COMPLETE_NO_DASHBOARD_SOURCE_CHANGES"
      },
      "return_hits": [
        {
          "path": "export_reports.e1r_backtest_summary.e1r_objects[0].summary_fields.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[35].entry_price",
          "key": "entry_price",
          "value": 116.58,
          "distance_to_target_116_74": 0.1599999999999966
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[0].avg_cost",
          "key": "avg_cost",
          "value": 117.06,
          "distance_to_target_116_74": 0.3200000000000074
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[27].exit_price",
          "key": "exit_price",
          "value": 117.34,
          "distance_to_target_116_74": 0.6000000000000085
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[39].exit_price",
          "key": "exit_price",
          "value": 115.82,
          "distance_to_target_116_74": 0.9200000000000017
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[42].entry_price",
          "key": "entry_price",
          "value": 117.83,
          "distance_to_target_116_74": 1.0900000000000034
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[32].effective_exit",
          "key": "effective_exit",
          "value": 113.22,
          "distance_to_target_116_74": 3.519999999999996
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[32].exit_price",
          "key": "exit_price",
          "value": 112.96,
          "distance_to_target_116_74": 3.780000000000001
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[39].effective_exit",
          "key": "effective_exit",
          "value": 112.75,
          "distance_to_target_116_74": 3.989999999999995
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[27].effective_exit",
          "key": "effective_exit",
          "value": 112.01,
          "distance_to_target_116_74": 4.72999999999999
        }
      ],
      "metric_hits": [
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.total_return_pct",
          "key": "total_return_pct",
          "value": 7.52
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.alpha_pct",
          "key": "alpha_pct",
          "value": -61.84
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 38.1
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.profit_factor",
          "key": "profit_factor",
          "value": 1.25
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.18
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.win_rate_pct",
          "key": "win_rate_pct",
          "value": 36.2
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[0].return_pct",
          "key": "return_pct",
          "value": 25.97
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[0].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 41.38
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[1].return_pct",
          "key": "return_pct",
          "value": 6.94
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[1].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 15.28
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[2].return_pct",
          "key": "return_pct",
          "value": 1.67
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[2].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 19.54
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[3].return_pct",
          "key": "return_pct",
          "value": 2.51
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[3].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 7.73
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[4].return_pct",
          "key": "return_pct",
          "value": -0.11
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[4].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 20.23
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[5].return_pct",
          "key": "return_pct",
          "value": -2.65
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[5].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 8.76
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[6].return_pct",
          "key": "return_pct",
          "value": 4.7
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[6].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 25.52
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[7].return_pct",
          "key": "return_pct",
          "value": -4.51
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[7].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 8.52
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[8].return_pct",
          "key": "return_pct",
          "value": -3.95
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[8].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 11.42
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[9].return_pct",
          "key": "return_pct",
          "value": -2.42
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[9].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 11.46
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[10].return_pct",
          "key": "return_pct",
          "value": -0.87
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[10].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 11.64
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[11].return_pct",
          "key": "return_pct",
          "value": -6.24
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[11].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 6.05
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[12].return_pct",
          "key": "return_pct",
          "value": -2.53
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[12].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 4.22
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[13].return_pct",
          "key": "return_pct",
          "value": -3.23
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[13].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 11.7
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[14].return_pct",
          "key": "return_pct",
          "value": 6.64
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[14].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 21.84
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[15].return_pct",
          "key": "return_pct",
          "value": 44.8
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[15].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 38.4
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[16].return_pct",
          "key": "return_pct",
          "value": -16.45
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[16].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 15.84
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[17].return_pct",
          "key": "return_pct",
          "value": -13.74
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[17].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 12.77
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[18].return_pct",
          "key": "return_pct",
          "value": -18.5
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[18].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 28.56
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[19].return_pct",
          "key": "return_pct",
          "value": -12.3
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[19].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 20.51
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[20].return_pct",
          "key": "return_pct",
          "value": -19.1
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[20].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 16.76
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[21].return_pct",
          "key": "return_pct",
          "value": -9.35
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[21].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 9.07
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[22].return_pct",
          "key": "return_pct",
          "value": -9.6
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[22].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 14.75
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[23].return_pct",
          "key": "return_pct",
          "value": -10.07
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[23].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 9.37
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[24].return_pct",
          "key": "return_pct",
          "value": -3.16
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[24].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 9.19
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[25].return_pct",
          "key": "return_pct",
          "value": -0.33
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[25].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 9.92
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[26].return_pct",
          "key": "return_pct",
          "value": -4.16
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[26].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 9.85
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[27].return_pct",
          "key": "return_pct",
          "value": 16.42
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[27].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 26.95
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[28].return_pct",
          "key": "return_pct",
          "value": 16.01
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[28].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 32.31
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[29].return_pct",
          "key": "return_pct",
          "value": -2.06
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[29].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 8.81
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[30].return_pct",
          "key": "return_pct",
          "value": 1.37
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[30].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 6.93
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[31].return_pct",
          "key": "return_pct",
          "value": 0.54
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[31].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 19.05
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[32].return_pct",
          "key": "return_pct",
          "value": 21.96
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[32].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 29.91
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[33].return_pct",
          "key": "return_pct",
          "value": -3.46
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[33].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 13.34
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[34].return_pct",
          "key": "return_pct",
          "value": -16.03
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[34].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 14.34
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[35].return_pct",
          "key": "return_pct",
          "value": -2.74
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[35].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 33.71
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[36].return_pct",
          "key": "return_pct",
          "value": -4.73
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[36].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 12.23
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[37].return_pct",
          "key": "return_pct",
          "value": 3.79
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[37].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 16.84
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[38].return_pct",
          "key": "return_pct",
          "value": 21.41
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[38].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 26.15
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[39].return_pct",
          "key": "return_pct",
          "value": -4.01
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[39].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 16.52
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[40].return_pct",
          "key": "return_pct",
          "value": 0.14
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[40].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 14.69
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[41].return_pct",
          "key": "return_pct",
          "value": -13.13
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[41].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 14.69
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[42].return_pct",
          "key": "return_pct",
          "value": 2.8
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[42].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 14.72
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[43].return_pct",
          "key": "return_pct",
          "value": -4.54
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[43].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 5.99
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[44].return_pct",
          "key": "return_pct",
          "value": 67.47
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[44].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 0
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[45].return_pct",
          "key": "return_pct",
          "value": -1.55
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[45].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 0
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[46].return_pct",
          "key": "return_pct",
          "value": -1.2
        },
        {
          "path": "export_reports.backtest.e1_objects[3].summary_fields.trades[46].max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 0
        }
      ],
      "market_hits": [
        {
          "path": "exports_inspected.market_state",
          "key": "market_state",
          "value": "exports/market_state.json"
        },
        {
          "path": "export_reports.backtest.contains.market_state_like",
          "key": "market_state_like",
          "value": true
        },
        {
          "path": "export_reports.backtest.market_state_objects",
          "key": "market_state_objects",
          "value": "[{\"path\": \"$.backtest.results.layer_d.daily_records[0]\", \"keys\": [\"date\", \"cash\", \"position_value\", \"total_equity\", \"n_holdings\", \"pending_orders\", \"market_gate_state\", \"spx_close\", \"spx_ma50\", \"spx_day_return_pct\"], \"market_state_fields\": {\"date\": \"2023-11-06\"}, \"preview\": \"{\\n  \\\"date\\\": \\\"2023-11-06\\\",\\n  \\\"cash\\\": 100000.0,\\n  \\\"position_value\\\": 0.0,\\n  \\\"total_equity\\\": 100000.0,\\n  \\\"n_holdings\\\": 0,\\n  \\\"pending_orders\\\": 0,\\n  \\\"market_gate_state\\\": \\\"RISK_OFF\\\",\\n  \\\"spx_close\\\": 4365.98,\\n  \\\"spx_ma50\\\": 4346.84,\\n  \\\"spx_day_return_pct\\\": 0.18\\n}\"}, {\"path\": \"$.backtest.results.layer_d.daily_records[1]\", \"keys\": [\"date\", \"cash\", \"position_value\", \"total_equity\", \"n_holdings\", \"pending_orders\", \"market_gate_state\", \"spx_close\", \"spx_ma50\", \"spx_day_return_pct\"], \"market_state_fields\": {\"date\": \"2023-12-19\"}, \"preview\": \"{\\n  \\\"date\\\": \\\"2023-12-19\\\",\\n  \\\"cash\\\": 743.12,\\n  \\\"position_value\\\": 119246.73,\\n  \\\"total_equity\\\": 119989.85,\\n  \\\"n_holdings\\\": 3,\\n  \\\"pending_orders\\\": 0,\\n  \\\"market_gate_state\\\": \\\"ALLOW\\\",\\n  \\\"spx_close\\\": 4768.37,\\n  \\\"spx_ma50\\\": 4445.92,\\n  \\\"spx_day_return_pct\\\": 0.59\\n}\"}, {\"path\": \"$.backtest.results.layer_d.daily_records[2]\", \"keys\":...<truncated>"
        },
        {
          "path": "export_reports.backtest.market_state_objects[0]",
          "key": "[0]",
          "value": {
            "path": "$.backtest.results.layer_d.daily_records[0]",
            "keys": [
              "date",
              "cash",
              "position_value",
              "total_equity",
              "n_holdings",
              "pending_orders",
              "market_gate_state",
              "spx_close",
              "spx_ma50",
              "spx_day_return_pct"
            ],
            "market_state_fields": {
              "date": "2023-11-06"
            },
            "preview": "{\n  \"date\": \"2023-11-06\",\n  \"cash\": 100000.0,\n  \"position_value\": 0.0,\n  \"total_equity\": 100000.0,\n  \"n_holdings\": 0,\n  \"pending_orders\": 0,\n  \"market_gate_state\": \"RISK_OFF\",\n  \"spx_close\": 4365.98,\n  \"spx_ma50\": 4346.84,\n  \"spx_day_return_pct\": 0.18\n}"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[0].path",
          "key": "path",
          "value": "$.backtest.results.layer_d.daily_records[0]"
        },
        {
          "path": "export_reports.backtest.market_state_objects[0].keys",
          "key": "keys",
          "value": [
            "date",
            "cash",
            "position_value",
            "total_equity",
            "n_holdings",
            "pending_orders",
            "market_gate_state",
            "spx_close",
            "spx_ma50",
            "spx_day_return_pct"
          ]
        },
        {
          "path": "export_reports.backtest.market_state_objects[0].keys[0]",
          "key": "[0]",
          "value": "date"
        },
        {
          "path": "export_reports.backtest.market_state_objects[0].keys[1]",
          "key": "[1]",
          "value": "cash"
        },
        {
          "path": "export_reports.backtest.market_state_objects[0].keys[2]",
          "key": "[2]",
          "value": "position_value"
        },
        {
          "path": "export_reports.backtest.market_state_objects[0].keys[3]",
          "key": "[3]",
          "value": "total_equity"
        },
        {
          "path": "export_reports.backtest.market_state_objects[0].keys[4]",
          "key": "[4]",
          "value": "n_holdings"
        },
        {
          "path": "export_reports.backtest.market_state_objects[0].keys[5]",
          "key": "[5]",
          "value": "pending_orders"
        },
        {
          "path": "export_reports.backtest.market_state_objects[0].keys[6]",
          "key": "[6]",
          "value": "market_gate_state"
        },
        {
          "path": "export_reports.backtest.market_state_objects[0].keys[7]",
          "key": "[7]",
          "value": "spx_close"
        },
        {
          "path": "export_reports.backtest.market_state_objects[0].keys[8]",
          "key": "[8]",
          "value": "spx_ma50"
        },
        {
          "path": "export_reports.backtest.market_state_objects[0].keys[9]",
          "key": "[9]",
          "value": "spx_day_return_pct"
        },
        {
          "path": "export_reports.backtest.market_state_objects[0].market_state_fields",
          "key": "market_state_fields",
          "value": {
            "date": "2023-11-06"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[0].market_state_fields.date",
          "key": "date",
          "value": "2023-11-06"
        },
        {
          "path": "export_reports.backtest.market_state_objects[0].preview",
          "key": "preview",
          "value": "{\n  \"date\": \"2023-11-06\",\n  \"cash\": 100000.0,\n  \"position_value\": 0.0,\n  \"total_equity\": 100000.0,\n  \"n_holdings\": 0,\n  \"pending_orders\": 0,\n  \"market_gate_state\": \"RISK_OFF\",\n  \"spx_close\": 4365.98,\n  \"spx_ma50\": 4346.84,\n  \"spx_day_return_pct\": 0.18\n}"
        },
        {
          "path": "export_reports.backtest.market_state_objects[1]",
          "key": "[1]",
          "value": {
            "path": "$.backtest.results.layer_d.daily_records[1]",
            "keys": [
              "date",
              "cash",
              "position_value",
              "total_equity",
              "n_holdings",
              "pending_orders",
              "market_gate_state",
              "spx_close",
              "spx_ma50",
              "spx_day_return_pct"
            ],
            "market_state_fields": {
              "date": "2023-12-19"
            },
            "preview": "{\n  \"date\": \"2023-12-19\",\n  \"cash\": 743.12,\n  \"position_value\": 119246.73,\n  \"total_equity\": 119989.85,\n  \"n_holdings\": 3,\n  \"pending_orders\": 0,\n  \"market_gate_state\": \"ALLOW\",\n  \"spx_close\": 4768.37,\n  \"spx_ma50\": 4445.92,\n  \"spx_day_return_pct\": 0.59\n}"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[1].path",
          "key": "path",
          "value": "$.backtest.results.layer_d.daily_records[1]"
        },
        {
          "path": "export_reports.backtest.market_state_objects[1].keys",
          "key": "keys",
          "value": [
            "date",
            "cash",
            "position_value",
            "total_equity",
            "n_holdings",
            "pending_orders",
            "market_gate_state",
            "spx_close",
            "spx_ma50",
            "spx_day_return_pct"
          ]
        },
        {
          "path": "export_reports.backtest.market_state_objects[1].keys[0]",
          "key": "[0]",
          "value": "date"
        },
        {
          "path": "export_reports.backtest.market_state_objects[1].keys[1]",
          "key": "[1]",
          "value": "cash"
        },
        {
          "path": "export_reports.backtest.market_state_objects[1].keys[2]",
          "key": "[2]",
          "value": "position_value"
        },
        {
          "path": "export_reports.backtest.market_state_objects[1].keys[3]",
          "key": "[3]",
          "value": "total_equity"
        },
        {
          "path": "export_reports.backtest.market_state_objects[1].keys[4]",
          "key": "[4]",
          "value": "n_holdings"
        },
        {
          "path": "export_reports.backtest.market_state_objects[1].keys[5]",
          "key": "[5]",
          "value": "pending_orders"
        },
        {
          "path": "export_reports.backtest.market_state_objects[1].keys[6]",
          "key": "[6]",
          "value": "market_gate_state"
        },
        {
          "path": "export_reports.backtest.market_state_objects[1].keys[7]",
          "key": "[7]",
          "value": "spx_close"
        },
        {
          "path": "export_reports.backtest.market_state_objects[1].keys[8]",
          "key": "[8]",
          "value": "spx_ma50"
        },
        {
          "path": "export_reports.backtest.market_state_objects[1].keys[9]",
          "key": "[9]",
          "value": "spx_day_return_pct"
        },
        {
          "path": "export_reports.backtest.market_state_objects[1].market_state_fields",
          "key": "market_state_fields",
          "value": {
            "date": "2023-12-19"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[1].market_state_fields.date",
          "key": "date",
          "value": "2023-12-19"
        },
        {
          "path": "export_reports.backtest.market_state_objects[1].preview",
          "key": "preview",
          "value": "{\n  \"date\": \"2023-12-19\",\n  \"cash\": 743.12,\n  \"position_value\": 119246.73,\n  \"total_equity\": 119989.85,\n  \"n_holdings\": 3,\n  \"pending_orders\": 0,\n  \"market_gate_state\": \"ALLOW\",\n  \"spx_close\": 4768.37,\n  \"spx_ma50\": 4445.92,\n  \"spx_day_return_pct\": 0.59\n}"
        },
        {
          "path": "export_reports.backtest.market_state_objects[2]",
          "key": "[2]",
          "value": {
            "path": "$.backtest.results.layer_d.daily_records[2]",
            "keys": [
              "date",
              "cash",
              "position_value",
              "total_equity",
              "n_holdings",
              "pending_orders",
              "market_gate_state",
              "spx_close",
              "spx_ma50",
              "spx_day_return_pct"
            ],
            "market_state_fields": {
              "date": "2024-02-02"
            },
            "preview": "{\n  \"date\": \"2024-02-02\",\n  \"cash\": 47367.59,\n  \"position_value\": 67654.8,\n  \"total_equity\": 115022.39,\n  \"n_holdings\": 3,\n  \"pending_orders\": 1,\n  \"market_gate_state\": \"ALLOW\",\n  \"spx_close\": 4958.61,\n  \"spx_ma50\": 4726.76,\n  \"spx_day_return_pct\": 1.07\n}"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[2].path",
          "key": "path",
          "value": "$.backtest.results.layer_d.daily_records[2]"
        },
        {
          "path": "export_reports.backtest.market_state_objects[2].keys",
          "key": "keys",
          "value": [
            "date",
            "cash",
            "position_value",
            "total_equity",
            "n_holdings",
            "pending_orders",
            "market_gate_state",
            "spx_close",
            "spx_ma50",
            "spx_day_return_pct"
          ]
        },
        {
          "path": "export_reports.backtest.market_state_objects[2].keys[0]",
          "key": "[0]",
          "value": "date"
        },
        {
          "path": "export_reports.backtest.market_state_objects[2].keys[1]",
          "key": "[1]",
          "value": "cash"
        },
        {
          "path": "export_reports.backtest.market_state_objects[2].keys[2]",
          "key": "[2]",
          "value": "position_value"
        },
        {
          "path": "export_reports.backtest.market_state_objects[2].keys[3]",
          "key": "[3]",
          "value": "total_equity"
        },
        {
          "path": "export_reports.backtest.market_state_objects[2].keys[4]",
          "key": "[4]",
          "value": "n_holdings"
        },
        {
          "path": "export_reports.backtest.market_state_objects[2].keys[5]",
          "key": "[5]",
          "value": "pending_orders"
        },
        {
          "path": "export_reports.backtest.market_state_objects[2].keys[6]",
          "key": "[6]",
          "value": "market_gate_state"
        },
        {
          "path": "export_reports.backtest.market_state_objects[2].keys[7]",
          "key": "[7]",
          "value": "spx_close"
        },
        {
          "path": "export_reports.backtest.market_state_objects[2].keys[8]",
          "key": "[8]",
          "value": "spx_ma50"
        },
        {
          "path": "export_reports.backtest.market_state_objects[2].keys[9]",
          "key": "[9]",
          "value": "spx_day_return_pct"
        },
        {
          "path": "export_reports.backtest.market_state_objects[2].market_state_fields",
          "key": "market_state_fields",
          "value": {
            "date": "2024-02-02"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[2].market_state_fields.date",
          "key": "date",
          "value": "2024-02-02"
        },
        {
          "path": "export_reports.backtest.market_state_objects[2].preview",
          "key": "preview",
          "value": "{\n  \"date\": \"2024-02-02\",\n  \"cash\": 47367.59,\n  \"position_value\": 67654.8,\n  \"total_equity\": 115022.39,\n  \"n_holdings\": 3,\n  \"pending_orders\": 1,\n  \"market_gate_state\": \"ALLOW\",\n  \"spx_close\": 4958.61,\n  \"spx_ma50\": 4726.76,\n  \"spx_day_return_pct\": 1.07\n}"
        },
        {
          "path": "export_reports.backtest.market_state_objects[3]",
          "key": "[3]",
          "value": {
            "path": "$.backtest.results.layer_d.daily_records[3]",
            "keys": [
              "date",
              "cash",
              "position_value",
              "total_equity",
              "n_holdings",
              "pending_orders",
              "market_gate_state",
              "spx_close",
              "spx_ma50",
              "spx_day_return_pct"
            ],
            "market_state_fields": {
              "date": "2024-03-18"
            },
            "preview": "{\n  \"date\": \"2024-03-18\",\n  \"cash\": 55529.84,\n  \"position_value\": 59845.54,\n  \"total_equity\": 115375.38,\n  \"n_holdings\": 3,\n  \"pending_orders\": 1,\n  \"market_gate_state\": \"ALLOW\",\n  \"spx_close\": 5149.42,\n  \"spx_ma50\": 4972.1,\n  \"spx_day_return_pct\": 0.63\n}"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[3].path",
          "key": "path",
          "value": "$.backtest.results.layer_d.daily_records[3]"
        },
        {
          "path": "export_reports.backtest.market_state_objects[3].keys",
          "key": "keys",
          "value": [
            "date",
            "cash",
            "position_value",
            "total_equity",
            "n_holdings",
            "pending_orders",
            "market_gate_state",
            "spx_close",
            "spx_ma50",
            "spx_day_return_pct"
          ]
        },
        {
          "path": "export_reports.backtest.market_state_objects[3].keys[0]",
          "key": "[0]",
          "value": "date"
        },
        {
          "path": "export_reports.backtest.market_state_objects[3].keys[1]",
          "key": "[1]",
          "value": "cash"
        },
        {
          "path": "export_reports.backtest.market_state_objects[3].keys[2]",
          "key": "[2]",
          "value": "position_value"
        },
        {
          "path": "export_reports.backtest.market_state_objects[3].keys[3]",
          "key": "[3]",
          "value": "total_equity"
        },
        {
          "path": "export_reports.backtest.market_state_objects[3].keys[4]",
          "key": "[4]",
          "value": "n_holdings"
        },
        {
          "path": "export_reports.backtest.market_state_objects[3].keys[5]",
          "key": "[5]",
          "value": "pending_orders"
        },
        {
          "path": "export_reports.backtest.market_state_objects[3].keys[6]",
          "key": "[6]",
          "value": "market_gate_state"
        },
        {
          "path": "export_reports.backtest.market_state_objects[3].keys[7]",
          "key": "[7]",
          "value": "spx_close"
        },
        {
          "path": "export_reports.backtest.market_state_objects[3].keys[8]",
          "key": "[8]",
          "value": "spx_ma50"
        },
        {
          "path": "export_reports.backtest.market_state_objects[3].keys[9]",
          "key": "[9]",
          "value": "spx_day_return_pct"
        },
        {
          "path": "export_reports.backtest.market_state_objects[3].market_state_fields",
          "key": "market_state_fields",
          "value": {
            "date": "2024-03-18"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[3].market_state_fields.date",
          "key": "date",
          "value": "2024-03-18"
        },
        {
          "path": "export_reports.backtest.market_state_objects[3].preview",
          "key": "preview",
          "value": "{\n  \"date\": \"2024-03-18\",\n  \"cash\": 55529.84,\n  \"position_value\": 59845.54,\n  \"total_equity\": 115375.38,\n  \"n_holdings\": 3,\n  \"pending_orders\": 1,\n  \"market_gate_state\": \"ALLOW\",\n  \"spx_close\": 5149.42,\n  \"spx_ma50\": 4972.1,\n  \"spx_day_return_pct\": 0.63\n}"
        },
        {
          "path": "export_reports.backtest.market_state_objects[4]",
          "key": "[4]",
          "value": {
            "path": "$.backtest.results.layer_d.daily_records[4]",
            "keys": [
              "date",
              "cash",
              "position_value",
              "total_equity",
              "n_holdings",
              "pending_orders",
              "market_gate_state",
              "spx_close",
              "spx_ma50",
              "spx_day_return_pct"
            ],
            "market_state_fields": {
              "date": "2024-04-30"
            },
            "preview": "{\n  \"date\": \"2024-04-30\",\n  \"cash\": 106450.37,\n  \"position_value\": 11991.96,\n  \"total_equity\": 118442.33,\n  \"n_holdings\": 1,\n  \"pending_orders\": 0,\n  \"market_gate_state\": \"RISK_OFF\",\n  \"spx_close\": 5035.69,\n  \"spx_ma50\": 5126.66,\n  \"spx_day_return_pct\": -1.57\n}"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[4].path",
          "key": "path",
          "value": "$.backtest.results.layer_d.daily_records[4]"
        },
        {
          "path": "export_reports.backtest.market_state_objects[4].keys",
          "key": "keys",
          "value": [
            "date",
            "cash",
            "position_value",
            "total_equity",
            "n_holdings",
            "pending_orders",
            "market_gate_state",
            "spx_close",
            "spx_ma50",
            "spx_day_return_pct"
          ]
        },
        {
          "path": "export_reports.backtest.market_state_objects[4].keys[0]",
          "key": "[0]",
          "value": "date"
        },
        {
          "path": "export_reports.backtest.market_state_objects[4].keys[1]",
          "key": "[1]",
          "value": "cash"
        },
        {
          "path": "export_reports.backtest.market_state_objects[4].keys[2]",
          "key": "[2]",
          "value": "position_value"
        },
        {
          "path": "export_reports.backtest.market_state_objects[4].keys[3]",
          "key": "[3]",
          "value": "total_equity"
        },
        {
          "path": "export_reports.backtest.market_state_objects[4].keys[4]",
          "key": "[4]",
          "value": "n_holdings"
        },
        {
          "path": "export_reports.backtest.market_state_objects[4].keys[5]",
          "key": "[5]",
          "value": "pending_orders"
        },
        {
          "path": "export_reports.backtest.market_state_objects[4].keys[6]",
          "key": "[6]",
          "value": "market_gate_state"
        },
        {
          "path": "export_reports.backtest.market_state_objects[4].keys[7]",
          "key": "[7]",
          "value": "spx_close"
        },
        {
          "path": "export_reports.backtest.market_state_objects[4].keys[8]",
          "key": "[8]",
          "value": "spx_ma50"
        },
        {
          "path": "export_reports.backtest.market_state_objects[4].keys[9]",
          "key": "[9]",
          "value": "spx_day_return_pct"
        },
        {
          "path": "export_reports.backtest.market_state_objects[4].market_state_fields",
          "key": "market_state_fields",
          "value": {
            "date": "2024-04-30"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[4].market_state_fields.date",
          "key": "date",
          "value": "2024-04-30"
        },
        {
          "path": "export_reports.backtest.market_state_objects[4].preview",
          "key": "preview",
          "value": "{\n  \"date\": \"2024-04-30\",\n  \"cash\": 106450.37,\n  \"position_value\": 11991.96,\n  \"total_equity\": 118442.33,\n  \"n_holdings\": 1,\n  \"pending_orders\": 0,\n  \"market_gate_state\": \"RISK_OFF\",\n  \"spx_close\": 5035.69,\n  \"spx_ma50\": 5126.66,\n  \"spx_day_return_pct\": -1.57\n}"
        },
        {
          "path": "export_reports.backtest.market_state_objects[5]",
          "key": "[5]",
          "value": {
            "path": "$.backtest.results.layer_d.daily_records[5]",
            "keys": [
              "date",
              "cash",
              "position_value",
              "total_equity",
              "n_holdings",
              "pending_orders",
              "market_gate_state",
              "spx_close",
              "spx_ma50",
              "spx_day_return_pct"
            ],
            "market_state_fields": {
              "date": "2024-06-12"
            },
            "preview": "{\n  \"date\": \"2024-06-12\",\n  \"cash\": 67317.32,\n  \"position_value\": 45217.62,\n  \"total_equity\": 112534.94,\n  \"n_holdings\": 3,\n  \"pending_orders\": 3,\n  \"market_gate_state\": \"ALLOW\",\n  \"spx_close\": 5421.03,\n  \"spx_ma50\": 5199.72,\n  \"spx_day_return_pct\": 0.85\n}"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[5].path",
          "key": "path",
          "value": "$.backtest.results.layer_d.daily_records[5]"
        },
        {
          "path": "export_reports.backtest.market_state_objects[5].keys",
          "key": "keys",
          "value": [
            "date",
            "cash",
            "position_value",
            "total_equity",
            "n_holdings",
            "pending_orders",
            "market_gate_state",
            "spx_close",
            "spx_ma50",
            "spx_day_return_pct"
          ]
        },
        {
          "path": "export_reports.backtest.market_state_objects[5].keys[0]",
          "key": "[0]",
          "value": "date"
        },
        {
          "path": "export_reports.backtest.market_state_objects[5].keys[1]",
          "key": "[1]",
          "value": "cash"
        },
        {
          "path": "export_reports.backtest.market_state_objects[5].keys[2]",
          "key": "[2]",
          "value": "position_value"
        },
        {
          "path": "export_reports.backtest.market_state_objects[5].keys[3]",
          "key": "[3]",
          "value": "total_equity"
        },
        {
          "path": "export_reports.backtest.market_state_objects[5].keys[4]",
          "key": "[4]",
          "value": "n_holdings"
        },
        {
          "path": "export_reports.backtest.market_state_objects[5].keys[5]",
          "key": "[5]",
          "value": "pending_orders"
        },
        {
          "path": "export_reports.backtest.market_state_objects[5].keys[6]",
          "key": "[6]",
          "value": "market_gate_state"
        },
        {
          "path": "export_reports.backtest.market_state_objects[5].keys[7]",
          "key": "[7]",
          "value": "spx_close"
        },
        {
          "path": "export_reports.backtest.market_state_objects[5].keys[8]",
          "key": "[8]",
          "value": "spx_ma50"
        },
        {
          "path": "export_reports.backtest.market_state_objects[5].keys[9]",
          "key": "[9]",
          "value": "spx_day_return_pct"
        },
        {
          "path": "export_reports.backtest.market_state_objects[5].market_state_fields",
          "key": "market_state_fields",
          "value": {
            "date": "2024-06-12"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[5].market_state_fields.date",
          "key": "date",
          "value": "2024-06-12"
        },
        {
          "path": "export_reports.backtest.market_state_objects[5].preview",
          "key": "preview",
          "value": "{\n  \"date\": \"2024-06-12\",\n  \"cash\": 67317.32,\n  \"position_value\": 45217.62,\n  \"total_equity\": 112534.94,\n  \"n_holdings\": 3,\n  \"pending_orders\": 3,\n  \"market_gate_state\": \"ALLOW\",\n  \"spx_close\": 5421.03,\n  \"spx_ma50\": 5199.72,\n  \"spx_day_return_pct\": 0.85\n}"
        },
        {
          "path": "export_reports.backtest.market_state_objects[6]",
          "key": "[6]",
          "value": {
            "path": "$.backtest.results.layer_d.daily_records[6]",
            "keys": [
              "date",
              "cash",
              "position_value",
              "total_equity",
              "n_holdings",
              "pending_orders",
              "market_gate_state",
              "spx_close",
              "spx_ma50",
              "spx_day_return_pct"
            ],
            "market_state_fields": {
              "date": "2024-07-26"
            },
            "preview": "{\n  \"date\": \"2024-07-26\",\n  \"cash\": 63630.57,\n  \"position_value\": 49055.03,\n  \"total_equity\": 112685.6,\n  \"n_holdings\": 2,\n  \"pending_orders\": 1,\n  \"market_gate_state\": \"RISK_OFF\",\n  \"spx_close\": 5459.1,\n  \"spx_ma50\": 5436.1,\n  \"spx_day_return_pct\": 1.11\n}"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[6].path",
          "key": "path",
          "value": "$.backtest.results.layer_d.daily_records[6]"
        },
        {
          "path": "export_reports.backtest.market_state_objects[6].keys",
          "key": "keys",
          "value": [
            "date",
            "cash",
            "position_value",
            "total_equity",
            "n_holdings",
            "pending_orders",
            "market_gate_state",
            "spx_close",
            "spx_ma50",
            "spx_day_return_pct"
          ]
        },
        {
          "path": "export_reports.backtest.market_state_objects[6].keys[0]",
          "key": "[0]",
          "value": "date"
        },
        {
          "path": "export_reports.backtest.market_state_objects[6].keys[1]",
          "key": "[1]",
          "value": "cash"
        },
        {
          "path": "export_reports.backtest.market_state_objects[6].keys[2]",
          "key": "[2]",
          "value": "position_value"
        },
        {
          "path": "export_reports.backtest.market_state_objects[6].keys[3]",
          "key": "[3]",
          "value": "total_equity"
        },
        {
          "path": "export_reports.backtest.market_state_objects[6].keys[4]",
          "key": "[4]",
          "value": "n_holdings"
        },
        {
          "path": "export_reports.backtest.market_state_objects[6].keys[5]",
          "key": "[5]",
          "value": "pending_orders"
        },
        {
          "path": "export_reports.backtest.market_state_objects[6].keys[6]",
          "key": "[6]",
          "value": "market_gate_state"
        },
        {
          "path": "export_reports.backtest.market_state_objects[6].keys[7]",
          "key": "[7]",
          "value": "spx_close"
        },
        {
          "path": "export_reports.backtest.market_state_objects[6].keys[8]",
          "key": "[8]",
          "value": "spx_ma50"
        },
        {
          "path": "export_reports.backtest.market_state_objects[6].keys[9]",
          "key": "[9]",
          "value": "spx_day_return_pct"
        },
        {
          "path": "export_reports.backtest.market_state_objects[6].market_state_fields",
          "key": "market_state_fields",
          "value": {
            "date": "2024-07-26"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[6].market_state_fields.date",
          "key": "date",
          "value": "2024-07-26"
        },
        {
          "path": "export_reports.backtest.market_state_objects[6].preview",
          "key": "preview",
          "value": "{\n  \"date\": \"2024-07-26\",\n  \"cash\": 63630.57,\n  \"position_value\": 49055.03,\n  \"total_equity\": 112685.6,\n  \"n_holdings\": 2,\n  \"pending_orders\": 1,\n  \"market_gate_state\": \"RISK_OFF\",\n  \"spx_close\": 5459.1,\n  \"spx_ma50\": 5436.1,\n  \"spx_day_return_pct\": 1.11\n}"
        },
        {
          "path": "export_reports.backtest.market_state_objects[7]",
          "key": "[7]",
          "value": {
            "path": "$.backtest.results.layer_d.daily_records[7]",
            "keys": [
              "date",
              "cash",
              "position_value",
              "total_equity",
              "n_holdings",
              "pending_orders",
              "market_gate_state",
              "spx_close",
              "spx_ma50",
              "spx_day_return_pct"
            ],
            "market_state_fields": {
              "date": "2024-09-09"
            },
            "preview": "{\n  \"date\": \"2024-09-09\",\n  \"cash\": 106901.86,\n  \"position_value\": 0.0,\n  \"total_equity\": 106901.86,\n  \"n_holdings\": 0,\n  \"pending_orders\": 0,\n  \"market_gate_state\": \"RISK_OFF\",\n  \"spx_close\": 5471.05,\n  \"spx_ma50\": 5504.98,\n  \"spx_day_return_pct\": 1.16\n}"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[7].path",
          "key": "path",
          "value": "$.backtest.results.layer_d.daily_records[7]"
        },
        {
          "path": "export_reports.backtest.market_state_objects[7].keys",
          "key": "keys",
          "value": [
            "date",
            "cash",
            "position_value",
            "total_equity",
            "n_holdings",
            "pending_orders",
            "market_gate_state",
            "spx_close",
            "spx_ma50",
            "spx_day_return_pct"
          ]
        },
        {
          "path": "export_reports.backtest.market_state_objects[7].keys[0]",
          "key": "[0]",
          "value": "date"
        },
        {
          "path": "export_reports.backtest.market_state_objects[7].keys[1]",
          "key": "[1]",
          "value": "cash"
        },
        {
          "path": "export_reports.backtest.market_state_objects[7].keys[2]",
          "key": "[2]",
          "value": "position_value"
        },
        {
          "path": "export_reports.backtest.market_state_objects[7].keys[3]",
          "key": "[3]",
          "value": "total_equity"
        },
        {
          "path": "export_reports.backtest.market_state_objects[7].keys[4]",
          "key": "[4]",
          "value": "n_holdings"
        },
        {
          "path": "export_reports.backtest.market_state_objects[7].keys[5]",
          "key": "[5]",
          "value": "pending_orders"
        },
        {
          "path": "export_reports.backtest.market_state_objects[7].keys[6]",
          "key": "[6]",
          "value": "market_gate_state"
        },
        {
          "path": "export_reports.backtest.market_state_objects[7].keys[7]",
          "key": "[7]",
          "value": "spx_close"
        },
        {
          "path": "export_reports.backtest.market_state_objects[7].keys[8]",
          "key": "[8]",
          "value": "spx_ma50"
        },
        {
          "path": "export_reports.backtest.market_state_objects[7].keys[9]",
          "key": "[9]",
          "value": "spx_day_return_pct"
        },
        {
          "path": "export_reports.backtest.market_state_objects[7].market_state_fields",
          "key": "market_state_fields",
          "value": {
            "date": "2024-09-09"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[7].market_state_fields.date",
          "key": "date",
          "value": "2024-09-09"
        },
        {
          "path": "export_reports.backtest.market_state_objects[7].preview",
          "key": "preview",
          "value": "{\n  \"date\": \"2024-09-09\",\n  \"cash\": 106901.86,\n  \"position_value\": 0.0,\n  \"total_equity\": 106901.86,\n  \"n_holdings\": 0,\n  \"pending_orders\": 0,\n  \"market_gate_state\": \"RISK_OFF\",\n  \"spx_close\": 5471.05,\n  \"spx_ma50\": 5504.98,\n  \"spx_day_return_pct\": 1.16\n}"
        },
        {
          "path": "export_reports.backtest.market_state_objects[8]",
          "key": "[8]",
          "value": {
            "path": "$.backtest.results.layer_d.daily_records[8]",
            "keys": [
              "date",
              "cash",
              "position_value",
              "total_equity",
              "n_holdings",
              "pending_orders",
              "market_gate_state",
              "spx_close",
              "spx_ma50",
              "spx_day_return_pct"
            ],
            "market_state_fields": {
              "date": "2024-10-21"
            },
            "preview": "{\n  \"date\": \"2024-10-21\",\n  \"cash\": 18534.64,\n  \"position_value\": 97319.45,\n  \"total_equity\": 115854.09,\n  \"n_holdings\": 3,\n  \"pending_orders\": 1,\n  \"market_gate_state\": \"ALLOW\",\n  \"spx_close\": 5853.98,\n  \"spx_ma50\": 5652.89,\n  \"spx_day_return_pct\": -0.18\n}"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[8].path",
          "key": "path",
          "value": "$.backtest.results.layer_d.daily_records[8]"
        },
        {
          "path": "export_reports.backtest.market_state_objects[8].keys",
          "key": "keys",
          "value": [
            "date",
            "cash",
            "position_value",
            "total_equity",
            "n_holdings",
            "pending_orders",
            "market_gate_state",
            "spx_close",
            "spx_ma50",
            "spx_day_return_pct"
          ]
        },
        {
          "path": "export_reports.backtest.market_state_objects[8].keys[0]",
          "key": "[0]",
          "value": "date"
        },
        {
          "path": "export_reports.backtest.market_state_objects[8].keys[1]",
          "key": "[1]",
          "value": "cash"
        },
        {
          "path": "export_reports.backtest.market_state_objects[8].keys[2]",
          "key": "[2]",
          "value": "position_value"
        },
        {
          "path": "export_reports.backtest.market_state_objects[8].keys[3]",
          "key": "[3]",
          "value": "total_equity"
        },
        {
          "path": "export_reports.backtest.market_state_objects[8].keys[4]",
          "key": "[4]",
          "value": "n_holdings"
        },
        {
          "path": "export_reports.backtest.market_state_objects[8].keys[5]",
          "key": "[5]",
          "value": "pending_orders"
        },
        {
          "path": "export_reports.backtest.market_state_objects[8].keys[6]",
          "key": "[6]",
          "value": "market_gate_state"
        },
        {
          "path": "export_reports.backtest.market_state_objects[8].keys[7]",
          "key": "[7]",
          "value": "spx_close"
        },
        {
          "path": "export_reports.backtest.market_state_objects[8].keys[8]",
          "key": "[8]",
          "value": "spx_ma50"
        },
        {
          "path": "export_reports.backtest.market_state_objects[8].keys[9]",
          "key": "[9]",
          "value": "spx_day_return_pct"
        },
        {
          "path": "export_reports.backtest.market_state_objects[8].market_state_fields",
          "key": "market_state_fields",
          "value": {
            "date": "2024-10-21"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[8].market_state_fields.date",
          "key": "date",
          "value": "2024-10-21"
        },
        {
          "path": "export_reports.backtest.market_state_objects[8].preview",
          "key": "preview",
          "value": "{\n  \"date\": \"2024-10-21\",\n  \"cash\": 18534.64,\n  \"position_value\": 97319.45,\n  \"total_equity\": 115854.09,\n  \"n_holdings\": 3,\n  \"pending_orders\": 1,\n  \"market_gate_state\": \"ALLOW\",\n  \"spx_close\": 5853.98,\n  \"spx_ma50\": 5652.89,\n  \"spx_day_return_pct\": -0.18\n}"
        },
        {
          "path": "export_reports.backtest.market_state_objects[9]",
          "key": "[9]",
          "value": {
            "path": "$.backtest.results.layer_d.daily_records[9]",
            "keys": [
              "date",
              "cash",
              "position_value",
              "total_equity",
              "n_holdings",
              "pending_orders",
              "market_gate_state",
              "spx_close",
              "spx_ma50",
              "spx_day_return_pct"
            ],
            "market_state_fields": {
              "date": "2024-12-03"
            },
            "preview": "{\n  \"date\": \"2024-12-03\",\n  \"cash\": 87863.97,\n  \"position_value\": 36809.93,\n  \"total_equity\": 124673.9,\n  \"n_holdings\": 2,\n  \"pending_orders\": 1,\n  \"market_gate_state\": \"ALLOW\",\n  \"spx_close\": 6049.88,\n  \"spx_ma50\": 5852.4,\n  \"spx_day_return_pct\": 0.05\n}"
          }
        },
        {
          "path": "export_reports.backtest.market_state_objects[9].path",
          "key": "path",
          "value": "$.backtest.results.layer_d.daily_records[9]"
        },
        {
          "path": "export_reports.backtest.market_state_objects[9].keys",
          "key": "keys",
          "value": [
            "date",
            "cash",
            "position_value",
            "total_equity",
            "n_holdings",
            "pending_orders",
            "market_gate_state",
            "spx_close",
            "spx_ma50",
            "spx_day_return_pct"
          ]
        },
        {
          "path": "export_reports.backtest.market_state_objects[9].keys[0]",
          "key": "[0]",
          "value": "date"
        },
        {
          "path": "export_reports.backtest.market_state_objects[9].keys[1]",
          "key": "[1]",
          "value": "cash"
        },
        {
          "path": "export_reports.backtest.market_state_objects[9].keys[2]",
          "key": "[2]",
          "value": "position_value"
        },
        {
          "path": "export_reports.backtest.market_state_objects[9].keys[3]",
          "key": "[3]",
          "value": "total_equity"
        },
        {
          "path": "export_reports.backtest.market_state_objects[9].keys[4]",
          "key": "[4]",
          "value": "n_holdings"
        },
        {
          "path": "export_reports.backtest.market_state_objects[9].keys[5]",
          "key": "[5]",
          "value": "pending_orders"
        },
        {
          "path": "export_reports.backtest.market_state_objects[9].keys[6]",
          "key": "[6]",
          "value": "market_gate_state"
        },
        {
          "path": "export_reports.backtest.market_state_objects[9].keys[7]",
          "key": "[7]",
          "value": "spx_close"
        },
        {
          "path": "export_reports.backtest.market_state_objects[9].keys[8]",
          "key": "[8]",
          "value": "spx_ma50"
        },
        {
          "path": "export_reports.backtest.market_state_objects[9].keys[9]",
          "key": "[9]",
          "value": "spx_day_return_pct"
        }
      ],
      "e1r_hits": [
        {
          "path": "stage",
          "key": "stage",
          "value": "B_STAGE_3_8E2A_E1_E1R_SPX_DATA_SHAPE_AUDIT"
        },
        {
          "path": "policy.purpose",
          "key": "purpose",
          "value": "Audit E1/E1R/SPX summary, equity curve, trade log, and market-state export shapes before native Research & Backtest integration."
        },
        {
          "path": "exports_inspected.e1r_status",
          "key": "e1r_status",
          "value": "exports/e1r_v0_2_status.json"
        },
        {
          "path": "exports_inspected.e1r_backtest_summary",
          "key": "e1r_backtest_summary",
          "value": "exports/e1r_v0_2_backtest_summary.json"
        },
        {
          "path": "exports_inspected.e1r_backtest_equity_curve",
          "key": "e1r_backtest_equity_curve",
          "value": "exports/e1r_v0_2_backtest_equity_curve.json"
        },
        {
          "path": "exports_inspected.oos_e1r_summary",
          "key": "oos_e1r_summary",
          "value": "exports/oos_e1r_v0_2_summary.json"
        },
        {
          "path": "exports_inspected.oos_e1r_equity_curve",
          "key": "oos_e1r_equity_curve",
          "value": "exports/oos_e1r_v0_2_equity_curve.json"
        },
        {
          "path": "exports_inspected.oos_e1r_orders",
          "key": "oos_e1r_orders",
          "value": "exports/oos_e1r_v0_2_orders.json"
        },
        {
          "path": "exports_inspected.oos_e1r_positions",
          "key": "oos_e1r_positions",
          "value": "exports/oos_e1r_v0_2_positions.json"
        },
        {
          "path": "exports_inspected.oos_e1r_sidecar",
          "key": "oos_e1r_sidecar",
          "value": "exports/oos_e1r_v0_2_sidecar.json"
        },
        {
          "path": "export_reports.backtest.contains.E1R_v0_2",
          "key": "E1R_v0_2",
          "value": false
        },
        {
          "path": "export_reports.backtest.e1r_objects",
          "key": "e1r_objects",
          "value": []
        },
        {
          "path": "export_reports.trade_log.contains.E1R_v0_2",
          "key": "E1R_v0_2",
          "value": false
        },
        {
          "path": "export_reports.trade_log.e1r_objects",
          "key": "e1r_objects",
          "value": []
        },
        {
          "path": "export_reports.e1r_status",
          "key": "e1r_status",
          "value": "{\"exists\": true, \"valid_json\": true, \"path\": \"exports/e1r_v0_2_status.json\", \"size_bytes\": 1587, \"type\": \"dict\", \"top_level_keys\": [\"generated_at\", \"strategy_id\", \"version\", \"research_status\", \"status_date\", \"e1r_market_state\", \"regime\", \"subclass\", \"mutually_exclusive_state_model\", \"core\", \"sidecar\", \"legacy_market_state\", \"source_files\", \"notes\"], \"array_length\": null, \"contains\": {\"E1\": false, \"E1R_v0_2\": true, \"SPX\": true, \"trade_like\": true, \"equity_like\": false, \"market_state_like\": true}, \"equity_arrays\": [], \"trade_arrays\": [], \"market_state_objects\": [{\"path\": \"$\", \"keys\": [\"generated_at\", \"strategy_id\", \"version\", \"research_status\", \"status_date\", \"e1r_market_state\", \"regime\", \"subclass\", \"mutually_exclusive_state_model\", \"core\", \"sidecar\", \"legacy_market_state\", \"source_files\", \"notes\"], \"market_state_fields\": {\"regime\": \"UPTREND\", \"e1r_market_state\": \"UPTREND\", \"status_date\": \"2026-06-18\"}, \"preview\": \"{\\n  \\\"generated_at\\\": \\\"2026-07-07T00:04:55.962648+00:00\\\",\\n  \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\\n  \\\"version\\\": \\\"E1R-v0.2-formal-sidecar-sleeve\\\",\\n  \\\"research_status\\\": \\\"FORMAL_SIDECAR_SLEEVE_ENGINE\\\",\\n  \\\"status_date\\\": \\\"2026-06-18\\\",\\n  \\\"e1r_market_st...<truncated>"
        },
        {
          "path": "export_reports.e1r_status.exists",
          "key": "exists",
          "value": true
        },
        {
          "path": "export_reports.e1r_status.valid_json",
          "key": "valid_json",
          "value": true
        },
        {
          "path": "export_reports.e1r_status.path",
          "key": "path",
          "value": "exports/e1r_v0_2_status.json"
        },
        {
          "path": "export_reports.e1r_status.size_bytes",
          "key": "size_bytes",
          "value": 1587
        },
        {
          "path": "export_reports.e1r_status.type",
          "key": "type",
          "value": "dict"
        },
        {
          "path": "export_reports.e1r_status.top_level_keys",
          "key": "top_level_keys",
          "value": [
            "generated_at",
            "strategy_id",
            "version",
            "research_status",
            "status_date",
            "e1r_market_state",
            "regime",
            "subclass",
            "mutually_exclusive_state_model",
            "core",
            "sidecar",
            "legacy_market_state",
            "source_files",
            "notes"
          ]
        },
        {
          "path": "export_reports.e1r_status.top_level_keys[0]",
          "key": "[0]",
          "value": "generated_at"
        },
        {
          "path": "export_reports.e1r_status.top_level_keys[1]",
          "key": "[1]",
          "value": "strategy_id"
        },
        {
          "path": "export_reports.e1r_status.top_level_keys[2]",
          "key": "[2]",
          "value": "version"
        },
        {
          "path": "export_reports.e1r_status.top_level_keys[3]",
          "key": "[3]",
          "value": "research_status"
        },
        {
          "path": "export_reports.e1r_status.top_level_keys[4]",
          "key": "[4]",
          "value": "status_date"
        },
        {
          "path": "export_reports.e1r_status.top_level_keys[5]",
          "key": "[5]",
          "value": "e1r_market_state"
        },
        {
          "path": "export_reports.e1r_status.top_level_keys[6]",
          "key": "[6]",
          "value": "regime"
        },
        {
          "path": "export_reports.e1r_status.top_level_keys[7]",
          "key": "[7]",
          "value": "subclass"
        },
        {
          "path": "export_reports.e1r_status.top_level_keys[8]",
          "key": "[8]",
          "value": "mutually_exclusive_state_model"
        },
        {
          "path": "export_reports.e1r_status.top_level_keys[9]",
          "key": "[9]",
          "value": "core"
        },
        {
          "path": "export_reports.e1r_status.top_level_keys[10]",
          "key": "[10]",
          "value": "sidecar"
        },
        {
          "path": "export_reports.e1r_status.top_level_keys[11]",
          "key": "[11]",
          "value": "legacy_market_state"
        },
        {
          "path": "export_reports.e1r_status.top_level_keys[12]",
          "key": "[12]",
          "value": "source_files"
        },
        {
          "path": "export_reports.e1r_status.top_level_keys[13]",
          "key": "[13]",
          "value": "notes"
        },
        {
          "path": "export_reports.e1r_status.array_length",
          "key": "array_length",
          "value": null
        },
        {
          "path": "export_reports.e1r_status.contains",
          "key": "contains",
          "value": {
            "E1": false,
            "E1R_v0_2": true,
            "SPX": true,
            "trade_like": true,
            "equity_like": false,
            "market_state_like": true
          }
        },
        {
          "path": "export_reports.e1r_status.contains.E1",
          "key": "E1",
          "value": false
        },
        {
          "path": "export_reports.e1r_status.contains.E1R_v0_2",
          "key": "E1R_v0_2",
          "value": true
        },
        {
          "path": "export_reports.e1r_status.contains.SPX",
          "key": "SPX",
          "value": true
        },
        {
          "path": "export_reports.e1r_status.contains.trade_like",
          "key": "trade_like",
          "value": true
        },
        {
          "path": "export_reports.e1r_status.contains.equity_like",
          "key": "equity_like",
          "value": false
        },
        {
          "path": "export_reports.e1r_status.contains.market_state_like",
          "key": "market_state_like",
          "value": true
        },
        {
          "path": "export_reports.e1r_status.equity_arrays",
          "key": "equity_arrays",
          "value": []
        },
        {
          "path": "export_reports.e1r_status.trade_arrays",
          "key": "trade_arrays",
          "value": []
        },
        {
          "path": "export_reports.e1r_status.market_state_objects",
          "key": "market_state_objects",
          "value": "[{\"path\": \"$\", \"keys\": [\"generated_at\", \"strategy_id\", \"version\", \"research_status\", \"status_date\", \"e1r_market_state\", \"regime\", \"subclass\", \"mutually_exclusive_state_model\", \"core\", \"sidecar\", \"legacy_market_state\", \"source_files\", \"notes\"], \"market_state_fields\": {\"regime\": \"UPTREND\", \"e1r_market_state\": \"UPTREND\", \"status_date\": \"2026-06-18\"}, \"preview\": \"{\\n  \\\"generated_at\\\": \\\"2026-07-07T00:04:55.962648+00:00\\\",\\n  \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\\n  \\\"version\\\": \\\"E1R-v0.2-formal-sidecar-sleeve\\\",\\n  \\\"research_status\\\": \\\"FORMAL_SIDECAR_SLEEVE_ENGINE\\\",\\n  \\\"status_date\\\": \\\"2026-06-18\\\",\\n  \\\"e1r_market_state\\\": \\\"UPTREND\\\",\\n  \\\"regime\\\": \\\"UPTREND\\\",\\n  \\\"subclass\\\": null,\\n  \\\"mutually_exclusive_state_model\\\": true,\\n  \\\"core\\\": {\\n    \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\\n    \\\"active\\\": true,\\n    \\\"active_condition\\\": \\\"UPTREND\\\"\\n  },\\n  \\\"sidecar\\\": {\\n    \\\"active\\\": false,\\n    \\\"active_condition\\\": \\\"SIDEWAYS_MA_CONFLICT\\\",\\n    \\\"gross_exposure\\\": 0.25,\\n    \\\"top_n\\\": 10,\\n    \\\"excluded_symbols\\\": [\\n      \\\"VIXY\\\"\\n    ],\\n    \\\"selected_count\\\": 0,\\n    \\\"selected\\\": [],\\n    \\\"source_record_date\\\": \\\"2026-06-17\\\",\\n    \\\"source_record_ne...<truncated>"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0]",
          "key": "[0]",
          "value": "{\"path\": \"$\", \"keys\": [\"generated_at\", \"strategy_id\", \"version\", \"research_status\", \"status_date\", \"e1r_market_state\", \"regime\", \"subclass\", \"mutually_exclusive_state_model\", \"core\", \"sidecar\", \"legacy_market_state\", \"source_files\", \"notes\"], \"market_state_fields\": {\"regime\": \"UPTREND\", \"e1r_market_state\": \"UPTREND\", \"status_date\": \"2026-06-18\"}, \"preview\": \"{\\n  \\\"generated_at\\\": \\\"2026-07-07T00:04:55.962648+00:00\\\",\\n  \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\\n  \\\"version\\\": \\\"E1R-v0.2-formal-sidecar-sleeve\\\",\\n  \\\"research_status\\\": \\\"FORMAL_SIDECAR_SLEEVE_ENGINE\\\",\\n  \\\"status_date\\\": \\\"2026-06-18\\\",\\n  \\\"e1r_market_state\\\": \\\"UPTREND\\\",\\n  \\\"regime\\\": \\\"UPTREND\\\",\\n  \\\"subclass\\\": null,\\n  \\\"mutually_exclusive_state_model\\\": true,\\n  \\\"core\\\": {\\n    \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\\n    \\\"active\\\": true,\\n    \\\"active_condition\\\": \\\"UPTREND\\\"\\n  },\\n  \\\"sidecar\\\": {\\n    \\\"active\\\": false,\\n    \\\"active_condition\\\": \\\"SIDEWAYS_MA_CONFLICT\\\",\\n    \\\"gross_exposure\\\": 0.25,\\n    \\\"top_n\\\": 10,\\n    \\\"excluded_symbols\\\": [\\n      \\\"VIXY\\\"\\n    ],\\n    \\\"selected_count\\\": 0,\\n    \\\"selected\\\": [],\\n    \\\"source_record_date\\\": \\\"2026-06-17\\\",\\n    \\\"source_record_nex...<truncated>"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].path",
          "key": "path",
          "value": "$"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].keys",
          "key": "keys",
          "value": [
            "generated_at",
            "strategy_id",
            "version",
            "research_status",
            "status_date",
            "e1r_market_state",
            "regime",
            "subclass",
            "mutually_exclusive_state_model",
            "core",
            "sidecar",
            "legacy_market_state",
            "source_files",
            "notes"
          ]
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].keys[0]",
          "key": "[0]",
          "value": "generated_at"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].keys[1]",
          "key": "[1]",
          "value": "strategy_id"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].keys[2]",
          "key": "[2]",
          "value": "version"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].keys[3]",
          "key": "[3]",
          "value": "research_status"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].keys[4]",
          "key": "[4]",
          "value": "status_date"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].keys[5]",
          "key": "[5]",
          "value": "e1r_market_state"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].keys[6]",
          "key": "[6]",
          "value": "regime"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].keys[7]",
          "key": "[7]",
          "value": "subclass"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].keys[8]",
          "key": "[8]",
          "value": "mutually_exclusive_state_model"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].keys[9]",
          "key": "[9]",
          "value": "core"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].keys[10]",
          "key": "[10]",
          "value": "sidecar"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].keys[11]",
          "key": "[11]",
          "value": "legacy_market_state"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].keys[12]",
          "key": "[12]",
          "value": "source_files"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].keys[13]",
          "key": "[13]",
          "value": "notes"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].market_state_fields",
          "key": "market_state_fields",
          "value": {
            "regime": "UPTREND",
            "e1r_market_state": "UPTREND",
            "status_date": "2026-06-18"
          }
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].market_state_fields.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].market_state_fields.e1r_market_state",
          "key": "e1r_market_state",
          "value": "UPTREND"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].market_state_fields.status_date",
          "key": "status_date",
          "value": "2026-06-18"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[0].preview",
          "key": "preview",
          "value": "{\n  \"generated_at\": \"2026-07-07T00:04:55.962648+00:00\",\n  \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\",\n  \"version\": \"E1R-v0.2-formal-sidecar-sleeve\",\n  \"research_status\": \"FORMAL_SIDECAR_SLEEVE_ENGINE\",\n  \"status_date\": \"2026-06-18\",\n  \"e1r_market_state\": \"UPTREND\",\n  \"regime\": \"UPTREND\",\n  \"subclass\": null,\n  \"mutually_exclusive_state_model\": true,\n  \"core\": {\n    \"strategy_id\": \"E1R_REGIME_AWARE_V0_1\",\n    \"active\": true,\n    \"active_condition\": \"UPTREND\"\n  },\n  \"sidecar\": {\n    \"active\": false,\n    \"active_condition\": \"SIDEWAYS_MA_CONFLICT\",\n    \"gross_exposure\": 0.25,\n    \"top_n\": 10,\n    \"excluded_symbols\": [\n      \"VIXY\"\n    ],\n    \"selected_count\": 0,\n    \"selected\": [],\n    \"source_record_date\": \"2026-06-17\",\n    \"source_record_next_date\": \"2026-06-18\"\n  },\n  \"legacy_market_state\": {\n    \"date\": \"2026-07-06\",\n    \"state\": \"Strong Risk-On\",\n    \"state_zh\": \"强势偏好\",\n    \"market_score\": 82.0,\n    \"leadership_confirmed\": false,\n    \"leadership_label\": \"Leadership Unconfirmed ⚠️\"\n  },\n  \"source_files\": {\n    \"regime\": \"data/research/e1_5y/regimes/spx_regime_daily.json\",\n    \"stocks\": \"data/research/e1_5y/raw/stocks\",\n    \"spx\": \"data/research/e1_5y/raw/indices/SPX.json\",\n    \"legacy_m...<truncated>"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[1]",
          "key": "[1]",
          "value": {
            "path": "$.legacy_market_state",
            "keys": [
              "date",
              "state",
              "state_zh",
              "market_score",
              "leadership_confirmed",
              "leadership_label"
            ],
            "market_state_fields": {
              "state": "Strong Risk-On",
              "date": "2026-07-06"
            },
            "preview": "{\n  \"date\": \"2026-07-06\",\n  \"state\": \"Strong Risk-On\",\n  \"state_zh\": \"强势偏好\",\n  \"market_score\": 82.0,\n  \"leadership_confirmed\": false,\n  \"leadership_label\": \"Leadership Unconfirmed ⚠️\"\n}"
          }
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[1].path",
          "key": "path",
          "value": "$.legacy_market_state"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[1].keys",
          "key": "keys",
          "value": [
            "date",
            "state",
            "state_zh",
            "market_score",
            "leadership_confirmed",
            "leadership_label"
          ]
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[1].keys[0]",
          "key": "[0]",
          "value": "date"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[1].keys[1]",
          "key": "[1]",
          "value": "state"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[1].keys[2]",
          "key": "[2]",
          "value": "state_zh"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[1].keys[3]",
          "key": "[3]",
          "value": "market_score"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[1].keys[4]",
          "key": "[4]",
          "value": "leadership_confirmed"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[1].keys[5]",
          "key": "[5]",
          "value": "leadership_label"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[1].market_state_fields",
          "key": "market_state_fields",
          "value": {
            "state": "Strong Risk-On",
            "date": "2026-07-06"
          }
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[1].market_state_fields.state",
          "key": "state",
          "value": "Strong Risk-On"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[1].market_state_fields.date",
          "key": "date",
          "value": "2026-07-06"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[1].preview",
          "key": "preview",
          "value": "{\n  \"date\": \"2026-07-06\",\n  \"state\": \"Strong Risk-On\",\n  \"state_zh\": \"强势偏好\",\n  \"market_score\": 82.0,\n  \"leadership_confirmed\": false,\n  \"leadership_label\": \"Leadership Unconfirmed ⚠️\"\n}"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[2]",
          "key": "[2]",
          "value": {
            "path": "$.source_files",
            "keys": [
              "regime",
              "stocks",
              "spx",
              "legacy_market_state"
            ],
            "market_state_fields": {
              "regime": "data/research/e1_5y/regimes/spx_regime_daily.json"
            },
            "preview": "{\n  \"regime\": \"data/research/e1_5y/regimes/spx_regime_daily.json\",\n  \"stocks\": \"data/research/e1_5y/raw/stocks\",\n  \"spx\": \"data/research/e1_5y/raw/indices/SPX.json\",\n  \"legacy_market_state\": \"exports/market_state.json\"\n}"
          }
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[2].path",
          "key": "path",
          "value": "$.source_files"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[2].keys",
          "key": "keys",
          "value": [
            "regime",
            "stocks",
            "spx",
            "legacy_market_state"
          ]
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[2].keys[0]",
          "key": "[0]",
          "value": "regime"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[2].keys[1]",
          "key": "[1]",
          "value": "stocks"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[2].keys[2]",
          "key": "[2]",
          "value": "spx"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[2].keys[3]",
          "key": "[3]",
          "value": "legacy_market_state"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[2].market_state_fields",
          "key": "market_state_fields",
          "value": {
            "regime": "data/research/e1_5y/regimes/spx_regime_daily.json"
          }
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[2].market_state_fields.regime",
          "key": "regime",
          "value": "data/research/e1_5y/regimes/spx_regime_daily.json"
        },
        {
          "path": "export_reports.e1r_status.market_state_objects[2].preview",
          "key": "preview",
          "value": "{\n  \"regime\": \"data/research/e1_5y/regimes/spx_regime_daily.json\",\n  \"stocks\": \"data/research/e1_5y/raw/stocks\",\n  \"spx\": \"data/research/e1_5y/raw/indices/SPX.json\",\n  \"legacy_market_state\": \"exports/market_state.json\"\n}"
        },
        {
          "path": "export_reports.e1r_status.e1_objects",
          "key": "e1_objects",
          "value": []
        },
        {
          "path": "export_reports.e1r_status.e1r_objects",
          "key": "e1r_objects",
          "value": "[{\"path\": \"$\", \"keys\": [\"generated_at\", \"strategy_id\", \"version\", \"research_status\", \"status_date\", \"e1r_market_state\", \"regime\", \"subclass\", \"mutually_exclusive_state_model\", \"core\", \"sidecar\", \"legacy_market_state\", \"source_files\", \"notes\"], \"summary_fields\": {}, \"preview\": \"{\\n  \\\"generated_at\\\": \\\"2026-07-07T00:04:55.962648+00:00\\\",\\n  \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\\n  \\\"version\\\": \\\"E1R-v0.2-formal-sidecar-sleeve\\\",\\n  \\\"research_status\\\": \\\"FORMAL_SIDECAR_SLEEVE_ENGINE\\\",\\n  \\\"status_date\\\": \\\"2026-06-18\\\",\\n  \\\"e1r_market_state\\\": \\\"UPTREND\\\",\\n  \\\"regime\\\": \\\"UPTREND\\\",\\n  \\\"subclass\\\": null,\\n  \\\"mutually_exclusive_state_model\\\": true,\\n  \\\"core\\\": {\\n    \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\\n    \\\"active\\\": true,\\n    \\\"active_condition\\\": \\\"UPTREND\\\"\\n  },\\n  \\\"sidecar\\\": {\\n    \\\"active\\\": false,\\n    \\\"active_condition\\\": \\\"SIDEWAYS_MA_CONFLICT\\\",\\n    \\\"gross_exposure\\\": 0.25,\\n    \\\"top_n\\\": 10,\\n    \\\"excluded_symbols\\\": [\\n      \\\"VIXY\\\"\\n    ],\\n    \\\"selected_count\\\": 0,\\n    \\\"selected\\\": [],\\n    \\\"source_record_date\\\": \\\"2026-06-17\\\",\\n    \\\"source_record_next_date\\\": \\\"2026-06-18\\\"\\n  },\\n  \\\"legacy_market_state\\\": {\\n    \\\"date\\\": \\\"2026-...<truncated>"
        },
        {
          "path": "export_reports.e1r_status.e1r_objects[0]",
          "key": "[0]",
          "value": "{\"path\": \"$\", \"keys\": [\"generated_at\", \"strategy_id\", \"version\", \"research_status\", \"status_date\", \"e1r_market_state\", \"regime\", \"subclass\", \"mutually_exclusive_state_model\", \"core\", \"sidecar\", \"legacy_market_state\", \"source_files\", \"notes\"], \"summary_fields\": {}, \"preview\": \"{\\n  \\\"generated_at\\\": \\\"2026-07-07T00:04:55.962648+00:00\\\",\\n  \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\\n  \\\"version\\\": \\\"E1R-v0.2-formal-sidecar-sleeve\\\",\\n  \\\"research_status\\\": \\\"FORMAL_SIDECAR_SLEEVE_ENGINE\\\",\\n  \\\"status_date\\\": \\\"2026-06-18\\\",\\n  \\\"e1r_market_state\\\": \\\"UPTREND\\\",\\n  \\\"regime\\\": \\\"UPTREND\\\",\\n  \\\"subclass\\\": null,\\n  \\\"mutually_exclusive_state_model\\\": true,\\n  \\\"core\\\": {\\n    \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\\n    \\\"active\\\": true,\\n    \\\"active_condition\\\": \\\"UPTREND\\\"\\n  },\\n  \\\"sidecar\\\": {\\n    \\\"active\\\": false,\\n    \\\"active_condition\\\": \\\"SIDEWAYS_MA_CONFLICT\\\",\\n    \\\"gross_exposure\\\": 0.25,\\n    \\\"top_n\\\": 10,\\n    \\\"excluded_symbols\\\": [\\n      \\\"VIXY\\\"\\n    ],\\n    \\\"selected_count\\\": 0,\\n    \\\"selected\\\": [],\\n    \\\"source_record_date\\\": \\\"2026-06-17\\\",\\n    \\\"source_record_next_date\\\": \\\"2026-06-18\\\"\\n  },\\n  \\\"legacy_market_state\\\": {\\n    \\\"date\\\": \\\"2026-0...<truncated>"
        },
        {
          "path": "export_reports.e1r_status.e1r_objects[0].path",
          "key": "path",
          "value": "$"
        },
        {
          "path": "export_reports.e1r_status.e1r_objects[0].keys",
          "key": "keys",
          "value": [
            "generated_at",
            "strategy_id",
            "version",
            "research_status",
            "status_date",
            "e1r_market_state",
            "regime",
            "subclass",
            "mutually_exclusive_state_model",
            "core",
            "sidecar",
            "legacy_market_state",
            "source_files",
            "notes"
          ]
        },
        {
          "path": "export_reports.e1r_status.e1r_objects[0].keys[0]",
          "key": "[0]",
          "value": "generated_at"
        },
        {
          "path": "export_reports.e1r_status.e1r_objects[0].keys[1]",
          "key": "[1]",
          "value": "strategy_id"
        },
        {
          "path": "export_reports.e1r_status.e1r_objects[0].keys[2]",
          "key": "[2]",
          "value": "version"
        },
        {
          "path": "export_reports.e1r_status.e1r_objects[0].keys[3]",
          "key": "[3]",
          "value": "research_status"
        }
      ],
      "counts": {
        "return_hits": 10,
        "metric_hits": 112,
        "market_hits": 2410,
        "e1r_hits": 2210
      },
      "score": 180
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json",
      "sha256": "f1df5a4054cc029259e2a7f57fda48deee38f13407945b6caefe38284bf9f19d",
      "top_level": {
        "status": "AUDIT_COMPLETE_NO_SOURCE_CHANGES"
      },
      "return_hits": [
        {
          "path": "json_reports.exports/e1r_v0_2_backtest_summary.json.field_presence.performance_like.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "watched_file_reports.src/engine/backtest.py.hits.forward[0]",
          "key": "[0]",
          "value": 115.0,
          "distance_to_target_116_74": 1.7399999999999949
        },
        {
          "path": "watched_file_reports.src/engine/backtest.py.line_hits[2].line",
          "key": "line",
          "value": 115.0,
          "distance_to_target_116_74": 1.7399999999999949
        },
        {
          "path": "watched_file_reports.src/engine/e1r_composer.py.hits.equity[8]",
          "key": "[8]",
          "value": 113.0,
          "distance_to_target_116_74": 3.739999999999995
        },
        {
          "path": "watched_file_reports.src/engine/e1r_composer.py.line_hits[10].line",
          "key": "line",
          "value": 113.0,
          "distance_to_target_116_74": 3.739999999999995
        }
      ],
      "metric_hits": [
        {
          "path": "json_reports.exports/oos_summary.json.field_presence.performance_like.total_return_pct",
          "key": "total_return_pct",
          "value": -24.74
        },
        {
          "path": "json_reports.exports/oos_summary.json.field_presence.performance_like.profit_factor",
          "key": "profit_factor",
          "value": null
        },
        {
          "path": "json_reports.exports/oos_summary.json.field_presence.performance_like.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 24.74
        },
        {
          "path": "json_reports.exports/e1r_v0_2_backtest_summary.json.field_presence.performance_like.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "json_reports.exports/e1r_v0_2_backtest_summary.json.field_presence.performance_like.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "json_reports.exports/e1r_v0_2_backtest_summary.json.field_presence.performance_like.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        }
      ],
      "market_hits": [
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.regime_fields",
          "key": "regime_fields",
          "value": [
            "market_state",
            "regime",
            "subclass",
            "core_active",
            "sidecar_active",
            "sidecar_selected_count"
          ]
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.regime_fields[0]",
          "key": "[0]",
          "value": "market_state"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.regime_fields[1]",
          "key": "[1]",
          "value": "regime"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.regime_fields[2]",
          "key": "[2]",
          "value": "subclass"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.regime_fields[3]",
          "key": "[3]",
          "value": "core_active"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.regime_fields[4]",
          "key": "[4]",
          "value": "sidecar_active"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.regime_fields[5]",
          "key": "[5]",
          "value": "sidecar_selected_count"
        },
        {
          "path": "watched_file_reports.src/engine/backtest.py.hits.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": [
            2737
          ]
        },
        {
          "path": "watched_file_reports.src/engine/backtest.py.hits.E1R_REGIME_AWARE_V0_2[0]",
          "key": "[0]",
          "value": 2737
        },
        {
          "path": "watched_file_reports.src/engine/e1r_composer.py.hits.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": [
            9,
            300
          ]
        },
        {
          "path": "watched_file_reports.src/engine/e1r_composer.py.hits.E1R_REGIME_AWARE_V0_2[0]",
          "key": "[0]",
          "value": 9
        },
        {
          "path": "watched_file_reports.src/engine/e1r_composer.py.hits.E1R_REGIME_AWARE_V0_2[1]",
          "key": "[1]",
          "value": 300
        },
        {
          "path": "watched_file_reports.src/engine/e1r_sidecar_sleeve.py.hits.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": [
            6
          ]
        },
        {
          "path": "watched_file_reports.src/engine/e1r_sidecar_sleeve.py.hits.E1R_REGIME_AWARE_V0_2[0]",
          "key": "[0]",
          "value": 6
        },
        {
          "path": "watched_file_reports.exports/oos_e1r_v0_2_summary.json.hits.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": [
            4
          ]
        },
        {
          "path": "watched_file_reports.exports/oos_e1r_v0_2_summary.json.hits.E1R_REGIME_AWARE_V0_2[0]",
          "key": "[0]",
          "value": 4
        },
        {
          "path": "watched_file_reports.exports/oos_e1r_v0_2_equity_curve.json.hits.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": [
            3
          ]
        },
        {
          "path": "watched_file_reports.exports/oos_e1r_v0_2_equity_curve.json.hits.E1R_REGIME_AWARE_V0_2[0]",
          "key": "[0]",
          "value": 3
        },
        {
          "path": "watched_file_reports.exports/oos_e1r_v0_2_orders.json.hits.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": [
            4
          ]
        },
        {
          "path": "watched_file_reports.exports/oos_e1r_v0_2_orders.json.hits.E1R_REGIME_AWARE_V0_2[0]",
          "key": "[0]",
          "value": 4
        },
        {
          "path": "watched_file_reports.exports/oos_e1r_v0_2_positions.json.hits.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": [
            4
          ]
        },
        {
          "path": "watched_file_reports.exports/oos_e1r_v0_2_positions.json.hits.E1R_REGIME_AWARE_V0_2[0]",
          "key": "[0]",
          "value": 4
        },
        {
          "path": "watched_file_reports.exports/oos_e1r_v0_2_sidecar.json.hits.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": [
            4
          ]
        },
        {
          "path": "watched_file_reports.exports/oos_e1r_v0_2_sidecar.json.hits.E1R_REGIME_AWARE_V0_2[0]",
          "key": "[0]",
          "value": 4
        },
        {
          "path": "watched_file_reports.exports/e1r_v0_2_status.json.hits.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": [
            3
          ]
        },
        {
          "path": "watched_file_reports.exports/e1r_v0_2_status.json.hits.E1R_REGIME_AWARE_V0_2[0]",
          "key": "[0]",
          "value": 3
        },
        {
          "path": "watched_file_reports.exports/e1r_v0_2_backtest_summary.json.hits.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": [
            2,
            20
          ]
        },
        {
          "path": "watched_file_reports.exports/e1r_v0_2_backtest_summary.json.hits.E1R_REGIME_AWARE_V0_2[0]",
          "key": "[0]",
          "value": 2
        },
        {
          "path": "watched_file_reports.exports/e1r_v0_2_backtest_summary.json.hits.E1R_REGIME_AWARE_V0_2[1]",
          "key": "[1]",
          "value": 20
        },
        {
          "path": "watched_file_reports.exports/e1r_v0_2_backtest_equity_curve.json.hits.E1R_REGIME_AWARE_V0_2",
          "key": "E1R_REGIME_AWARE_V0_2",
          "value": [
            2
          ]
        },
        {
          "path": "watched_file_reports.exports/e1r_v0_2_backtest_equity_curve.json.hits.E1R_REGIME_AWARE_V0_2[0]",
          "key": "[0]",
          "value": 2
        },
        {
          "path": "json_reports.exports/oos_summary.json.field_presence.regime_like",
          "key": "regime_like",
          "value": {}
        },
        {
          "path": "json_reports.exports/oos_equity_curve.json.field_presence.regime_like",
          "key": "regime_like",
          "value": {}
        },
        {
          "path": "json_reports.exports/oos_orders.json.field_presence.regime_like",
          "key": "regime_like",
          "value": {}
        },
        {
          "path": "json_reports.exports/oos_positions.json.field_presence.regime_like",
          "key": "regime_like",
          "value": {}
        },
        {
          "path": "json_reports.exports/oos_trades.json.field_presence.regime_like",
          "key": "regime_like",
          "value": {}
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_summary.json.field_presence.regime_like",
          "key": "regime_like",
          "value": {
            "market_state": "UPTREND",
            "regime": "UPTREND",
            "subclass": null,
            "core_active": true,
            "sidecar_active": false,
            "sidecar_selected_count": 0,
            "execution_status": "NO_REAL_EXECUTION",
            "equity_status": "NOT_YET_CONNECTED"
          }
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_summary.json.field_presence.regime_like.market_state",
          "key": "market_state",
          "value": "UPTREND"
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_summary.json.field_presence.regime_like.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_summary.json.field_presence.regime_like.subclass",
          "key": "subclass",
          "value": null
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_summary.json.field_presence.regime_like.core_active",
          "key": "core_active",
          "value": true
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_summary.json.field_presence.regime_like.sidecar_active",
          "key": "sidecar_active",
          "value": false
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_summary.json.field_presence.regime_like.sidecar_selected_count",
          "key": "sidecar_selected_count",
          "value": 0
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_summary.json.field_presence.regime_like.execution_status",
          "key": "execution_status",
          "value": "NO_REAL_EXECUTION"
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_summary.json.field_presence.regime_like.equity_status",
          "key": "equity_status",
          "value": "NOT_YET_CONNECTED"
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_equity_curve.json.field_presence.regime_like",
          "key": "regime_like",
          "value": {
            "execution_status": "PAPER_TRACKING_NO_REAL_EXECUTION",
            "equity_status": "OOS_EQUITY_MTM_TRACKING_SIDECAR_PAPER"
          }
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_equity_curve.json.field_presence.regime_like.execution_status",
          "key": "execution_status",
          "value": "PAPER_TRACKING_NO_REAL_EXECUTION"
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_equity_curve.json.field_presence.regime_like.equity_status",
          "key": "equity_status",
          "value": "OOS_EQUITY_MTM_TRACKING_SIDECAR_PAPER"
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_orders.json.field_presence.regime_like",
          "key": "regime_like",
          "value": {
            "market_state": "UPTREND",
            "execution_status": "NO_REAL_EXECUTION"
          }
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_orders.json.field_presence.regime_like.market_state",
          "key": "market_state",
          "value": "UPTREND"
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_orders.json.field_presence.regime_like.execution_status",
          "key": "execution_status",
          "value": "NO_REAL_EXECUTION"
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_positions.json.field_presence.regime_like",
          "key": "regime_like",
          "value": {
            "market_state": "UPTREND"
          }
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_positions.json.field_presence.regime_like.market_state",
          "key": "market_state",
          "value": "UPTREND"
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_sidecar.json.field_presence.regime_like",
          "key": "regime_like",
          "value": {
            "market_state": "UPTREND",
            "regime": "UPTREND",
            "subclass": null
          }
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_sidecar.json.field_presence.regime_like.market_state",
          "key": "market_state",
          "value": "UPTREND"
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_sidecar.json.field_presence.regime_like.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "json_reports.exports/oos_e1r_v0_2_sidecar.json.field_presence.regime_like.subclass",
          "key": "subclass",
          "value": null
        },
        {
          "path": "json_reports.exports/e1r_v0_2_status.json.field_presence.regime_like",
          "key": "regime_like",
          "value": {
            "regime": "UPTREND",
            "subclass": null
          }
        },
        {
          "path": "json_reports.exports/e1r_v0_2_status.json.field_presence.regime_like.regime",
          "key": "regime",
          "value": "UPTREND"
        },
        {
          "path": "json_reports.exports/e1r_v0_2_status.json.field_presence.regime_like.subclass",
          "key": "subclass",
          "value": null
        },
        {
          "path": "json_reports.exports/e1r_v0_2_backtest_summary.json.field_presence.regime_like",
          "key": "regime_like",
          "value": {}
        },
        {
          "path": "json_reports.exports/e1r_v0_2_backtest_equity_curve.json.field_presence.regime_like",
          "key": "regime_like",
          "value": {}
        },
        {
          "path": "json_reports.data/oos/portfolio_state.json.field_presence.regime_like",
          "key": "regime_like",
          "value": {}
        }
      ],
      "e1r_hits": [
        {
          "path": "stage",
          "key": "stage",
          "value": "B_STAGE_3_8E2F0_E1R_FORWARD_KICKOFF_READINESS_AUDIT"
        },
        {
          "path": "question",
          "key": "question",
          "value": "How should E1R v0.2 forward test be properly kicked off?"
        },
        {
          "path": "readiness.e1r_status_scaffold_exists",
          "key": "e1r_status_scaffold_exists",
          "value": true
        },
        {
          "path": "readiness.e1r_equity_curve_scaffold_exists",
          "key": "e1r_equity_curve_scaffold_exists",
          "value": true
        },
        {
          "path": "readiness.e1r_orders_scaffold_exists",
          "key": "e1r_orders_scaffold_exists",
          "value": true
        },
        {
          "path": "readiness.e1r_positions_scaffold_exists",
          "key": "e1r_positions_scaffold_exists",
          "value": true
        },
        {
          "path": "readiness.e1r_forward_performance_fields_exist",
          "key": "e1r_forward_performance_fields_exist",
          "value": false
        },
        {
          "path": "readiness.recommended_next_step",
          "key": "recommended_next_step",
          "value": "Implement E1R forward engine/export kickoff, not just dashboard mapping."
        },
        {
          "path": "kickoff_schema.official_strategy_id",
          "key": "official_strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "kickoff_schema.recommended_forward_start_policy.start_date_options[0].meaning",
          "key": "meaning",
          "value": "Official E1R forward tracking begins after the engine is implemented and committed."
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json",
          "key": "exports/oos_e1r_v0_2_summary.json",
          "value": {
            "status_fields": [
              "generated_at",
              "generated_at_display",
              "status_date",
              "strategy_id",
              "version",
              "forward_start_date",
              "forward_day_count",
              "research_status",
              "tracking_status"
            ],
            "performance_fields": [
              "portfolio_value",
              "equity",
              "cash",
              "market_value",
              "forward_return_pct",
              "spx_forward_return_pct",
              "alpha_pct",
              "max_drawdown_pct",
              "sharpe_ratio",
              "profit_factor",
              "number_of_trades",
              "open_positions_count",
              "executed_orders_count"
            ],
            "exposure_fields": [
              "gross_exposure",
              "net_exposure",
              "core_exposure",
              "sidecar_exposure"
            ],
            "regime_fields": [
              "market_state",
              "regime",
              "subclass",
              "core_active",
              "sidecar_active",
              "sidecar_selected_count"
            ]
          }
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.status_fields",
          "key": "status_fields",
          "value": [
            "generated_at",
            "generated_at_display",
            "status_date",
            "strategy_id",
            "version",
            "forward_start_date",
            "forward_day_count",
            "research_status",
            "tracking_status"
          ]
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.status_fields[0]",
          "key": "[0]",
          "value": "generated_at"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.status_fields[1]",
          "key": "[1]",
          "value": "generated_at_display"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.status_fields[2]",
          "key": "[2]",
          "value": "status_date"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.status_fields[3]",
          "key": "[3]",
          "value": "strategy_id"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.status_fields[4]",
          "key": "[4]",
          "value": "version"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.status_fields[5]",
          "key": "[5]",
          "value": "forward_start_date"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.status_fields[6]",
          "key": "[6]",
          "value": "forward_day_count"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.status_fields[7]",
          "key": "[7]",
          "value": "research_status"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.status_fields[8]",
          "key": "[8]",
          "value": "tracking_status"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.performance_fields",
          "key": "performance_fields",
          "value": [
            "portfolio_value",
            "equity",
            "cash",
            "market_value",
            "forward_return_pct",
            "spx_forward_return_pct",
            "alpha_pct",
            "max_drawdown_pct",
            "sharpe_ratio",
            "profit_factor",
            "number_of_trades",
            "open_positions_count",
            "executed_orders_count"
          ]
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.performance_fields[0]",
          "key": "[0]",
          "value": "portfolio_value"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.performance_fields[1]",
          "key": "[1]",
          "value": "equity"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.performance_fields[2]",
          "key": "[2]",
          "value": "cash"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.performance_fields[3]",
          "key": "[3]",
          "value": "market_value"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.performance_fields[4]",
          "key": "[4]",
          "value": "forward_return_pct"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.performance_fields[5]",
          "key": "[5]",
          "value": "spx_forward_return_pct"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.performance_fields[6]",
          "key": "[6]",
          "value": "alpha_pct"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.performance_fields[7]",
          "key": "[7]",
          "value": "max_drawdown_pct"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.performance_fields[8]",
          "key": "[8]",
          "value": "sharpe_ratio"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.performance_fields[9]",
          "key": "[9]",
          "value": "profit_factor"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.performance_fields[10]",
          "key": "[10]",
          "value": "number_of_trades"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.performance_fields[11]",
          "key": "[11]",
          "value": "open_positions_count"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.performance_fields[12]",
          "key": "[12]",
          "value": "executed_orders_count"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.exposure_fields",
          "key": "exposure_fields",
          "value": [
            "gross_exposure",
            "net_exposure",
            "core_exposure",
            "sidecar_exposure"
          ]
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.exposure_fields[0]",
          "key": "[0]",
          "value": "gross_exposure"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.exposure_fields[1]",
          "key": "[1]",
          "value": "net_exposure"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.exposure_fields[2]",
          "key": "[2]",
          "value": "core_exposure"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.exposure_fields[3]",
          "key": "[3]",
          "value": "sidecar_exposure"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.regime_fields",
          "key": "regime_fields",
          "value": [
            "market_state",
            "regime",
            "subclass",
            "core_active",
            "sidecar_active",
            "sidecar_selected_count"
          ]
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.regime_fields[0]",
          "key": "[0]",
          "value": "market_state"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.regime_fields[1]",
          "key": "[1]",
          "value": "regime"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.regime_fields[2]",
          "key": "[2]",
          "value": "subclass"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.regime_fields[3]",
          "key": "[3]",
          "value": "core_active"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.regime_fields[4]",
          "key": "[4]",
          "value": "sidecar_active"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.regime_fields[5]",
          "key": "[5]",
          "value": "sidecar_selected_count"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_equity_curve.json",
          "key": "exports/oos_e1r_v0_2_equity_curve.json",
          "value": {
            "row_fields": [
              "date",
              "equity",
              "portfolio_value",
              "cash",
              "market_value",
              "spx_value",
              "spx_indexed",
              "strategy_indexed",
              "drawdown_pct",
              "gross_exposure"
            ]
          }
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_equity_curve.json.row_fields",
          "key": "row_fields",
          "value": [
            "date",
            "equity",
            "portfolio_value",
            "cash",
            "market_value",
            "spx_value",
            "spx_indexed",
            "strategy_indexed",
            "drawdown_pct",
            "gross_exposure"
          ]
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_equity_curve.json.row_fields[0]",
          "key": "[0]",
          "value": "date"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_equity_curve.json.row_fields[1]",
          "key": "[1]",
          "value": "equity"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_equity_curve.json.row_fields[2]",
          "key": "[2]",
          "value": "portfolio_value"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_equity_curve.json.row_fields[3]",
          "key": "[3]",
          "value": "cash"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_equity_curve.json.row_fields[4]",
          "key": "[4]",
          "value": "market_value"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_equity_curve.json.row_fields[5]",
          "key": "[5]",
          "value": "spx_value"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_equity_curve.json.row_fields[6]",
          "key": "[6]",
          "value": "spx_indexed"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_equity_curve.json.row_fields[7]",
          "key": "[7]",
          "value": "strategy_indexed"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_equity_curve.json.row_fields[8]",
          "key": "[8]",
          "value": "drawdown_pct"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_equity_curve.json.row_fields[9]",
          "key": "[9]",
          "value": "gross_exposure"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_orders.json",
          "key": "exports/oos_e1r_v0_2_orders.json",
          "value": {
            "row_fields": [
              "date",
              "symbol",
              "action",
              "reason",
              "target_weight",
              "fill_policy",
              "paper_price",
              "shares",
              "notional",
              "status"
            ]
          }
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_orders.json.row_fields",
          "key": "row_fields",
          "value": [
            "date",
            "symbol",
            "action",
            "reason",
            "target_weight",
            "fill_policy",
            "paper_price",
            "shares",
            "notional",
            "status"
          ]
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_orders.json.row_fields[0]",
          "key": "[0]",
          "value": "date"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_orders.json.row_fields[1]",
          "key": "[1]",
          "value": "symbol"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_orders.json.row_fields[2]",
          "key": "[2]",
          "value": "action"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_orders.json.row_fields[3]",
          "key": "[3]",
          "value": "reason"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_orders.json.row_fields[4]",
          "key": "[4]",
          "value": "target_weight"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_orders.json.row_fields[5]",
          "key": "[5]",
          "value": "fill_policy"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_orders.json.row_fields[6]",
          "key": "[6]",
          "value": "paper_price"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_orders.json.row_fields[7]",
          "key": "[7]",
          "value": "shares"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_orders.json.row_fields[8]",
          "key": "[8]",
          "value": "notional"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_orders.json.row_fields[9]",
          "key": "[9]",
          "value": "status"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_positions.json",
          "key": "exports/oos_e1r_v0_2_positions.json",
          "value": {
            "row_fields": [
              "date",
              "symbol",
              "weight",
              "shares",
              "entry_date",
              "entry_price",
              "last_price",
              "market_value",
              "unrealized_return_pct",
              "source",
              "core_or_sidecar"
            ]
          }
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_positions.json.row_fields",
          "key": "row_fields",
          "value": [
            "date",
            "symbol",
            "weight",
            "shares",
            "entry_date",
            "entry_price",
            "last_price",
            "market_value",
            "unrealized_return_pct",
            "source",
            "core_or_sidecar"
          ]
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_positions.json.row_fields[0]",
          "key": "[0]",
          "value": "date"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_positions.json.row_fields[1]",
          "key": "[1]",
          "value": "symbol"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_positions.json.row_fields[2]",
          "key": "[2]",
          "value": "weight"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_positions.json.row_fields[3]",
          "key": "[3]",
          "value": "shares"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_positions.json.row_fields[4]",
          "key": "[4]",
          "value": "entry_date"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_positions.json.row_fields[5]",
          "key": "[5]",
          "value": "entry_price"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_positions.json.row_fields[6]",
          "key": "[6]",
          "value": "last_price"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_positions.json.row_fields[7]",
          "key": "[7]",
          "value": "market_value"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_positions.json.row_fields[8]",
          "key": "[8]",
          "value": "unrealized_return_pct"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_positions.json.row_fields[9]",
          "key": "[9]",
          "value": "source"
        },
        {
          "path": "kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_positions.json.row_fields[10]",
          "key": "[10]",
          "value": "core_or_sidecar"
        },
        {
          "path": "kickoff_schema.minimum_kickoff_acceptance[0]",
          "key": "[0]",
          "value": "E1R summary export contains forward_start_date and status_date."
        },
        {
          "path": "kickoff_schema.minimum_kickoff_acceptance[1]",
          "key": "[1]",
          "value": "E1R summary export contains portfolio_value/equity and forward_return_pct."
        },
        {
          "path": "kickoff_schema.minimum_kickoff_acceptance[2]",
          "key": "[2]",
          "value": "E1R equity curve has at least one row for kickoff date."
        },
        {
          "path": "kickoff_schema.minimum_kickoff_acceptance[3]",
          "key": "[3]",
          "value": "E1R positions export exists even if empty."
        },
        {
          "path": "kickoff_schema.minimum_kickoff_acceptance[4]",
          "key": "[4]",
          "value": "E1R orders export exists even if empty."
        },
        {
          "path": "kickoff_schema.minimum_kickoff_acceptance[5]",
          "key": "[5]",
          "value": "Daily update pipeline writes all E1R OOS exports deterministically."
        },
        {
          "path": "kickoff_schema.minimum_kickoff_acceptance[6]",
          "key": "[6]",
          "value": "Dashboard does not infer E1R performance from historical backtest fields."
        },
        {
          "path": "repo_candidate_files[4]",
          "key": "[4]",
          "value": "docs/research/stage3_4_app_snapshots/app_generated_e1r_v0_2_module_stage3_4.js"
        },
        {
          "path": "repo_candidate_files[9]",
          "key": "[9]",
          "value": "scripts/export_e1r_v0_2_backtest_equity.py"
        },
        {
          "path": "repo_candidate_files[10]",
          "key": "[10]",
          "value": "scripts/export_e1r_v0_2_status.py"
        },
        {
          "path": "repo_candidate_files[11]",
          "key": "[11]",
          "value": "scripts/run_e1r_v0_2_oos.py"
        },
        {
          "path": "repo_candidate_files[12]",
          "key": "[12]",
          "value": "scripts/run_e1r_v0_2_oos_equity.py"
        },
        {
          "path": "repo_candidate_files[13]",
          "key": "[13]",
          "value": "scripts/run_e1r_v0_2_sidecar_lifecycle.py"
        },
        {
          "path": "repo_candidate_files[15]",
          "key": "[15]",
          "value": "src/engine/e1r_composer.py"
        },
        {
          "path": "repo_candidate_files[16]",
          "key": "[16]",
          "value": "src/engine/e1r_sidecar_sleeve.py"
        },
        {
          "path": "watched_file_reports..github/workflows/update.yml.line_hits[3].text",
          "key": "text",
          "value": "      - name: E1R v0.2 OOS exports"
        }
      ],
      "counts": {
        "return_hits": 5,
        "metric_hits": 6,
        "market_hits": 63,
        "e1r_hits": 1475
      },
      "score": 180
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
      "sha256": "eebe78c3db00d193416e40b5a750127aa64a7f4f62016be7b703bf6370d4b18f",
      "top_level": {
        "status": "E1R_CORE_VARIANT_SOURCE_RECOVERY_COMPLETE_NO_EXPORTS_WRITTEN"
      },
      "return_hits": [
        {
          "path": "targets.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[0].matched_metrics.total_return_pct.value",
          "key": "value",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[0].matched_metrics.total_return_pct.target",
          "key": "target",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[0].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[1].matched_metrics.total_return_pct.value",
          "key": "value",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[1].matched_metrics.total_return_pct.target",
          "key": "target",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[1].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[2].matched_metrics.total_return_pct.value",
          "key": "value",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[2].matched_metrics.total_return_pct.target",
          "key": "target",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[2].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[3].matched_metrics.total_return_pct.value",
          "key": "value",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[3].matched_metrics.total_return_pct.target",
          "key": "target",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[3].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[4].matched_metrics.total_return_pct.value",
          "key": "value",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[4].matched_metrics.total_return_pct.target",
          "key": "target",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[4].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[5].matched_metrics.total_return_pct.value",
          "key": "value",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[5].matched_metrics.total_return_pct.target",
          "key": "target",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[5].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "top_recovered_nodes[6].matched_metrics.total_return_pct.value",
          "key": "value",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        }
      ],
      "metric_hits": [
        {
          "path": "targets.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "targets.spx_return_pct",
          "key": "spx_return_pct",
          "value": 76.844174428316
        },
        {
          "path": "targets.alpha_pct",
          "key": "alpha_pct",
          "value": 39.89942548515961
        },
        {
          "path": "targets.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        },
        {
          "path": "targets.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "targets.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.7957270568329264
        },
        {
          "path": "top_recovered_nodes[0].target_diffs_abs.total_return_pct",
          "key": "total_return_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[0].target_diffs_abs.spx_return_pct",
          "key": "spx_return_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[0].target_diffs_abs.alpha_pct",
          "key": "alpha_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[0].target_diffs_abs.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[0].target_diffs_abs.profit_factor",
          "key": "profit_factor",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[0].target_diffs_abs.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[0].matched_metrics.total_return_pct",
          "key": "total_return_pct",
          "value": {
            "key": "total_return_pct",
            "value": 116.7435999134756,
            "target": 116.7435999134756
          }
        },
        {
          "path": "top_recovered_nodes[0].matched_metrics.spx_return_pct",
          "key": "spx_return_pct",
          "value": {
            "key": "spx_return_pct",
            "value": 76.844174428316,
            "target": 76.844174428316
          }
        },
        {
          "path": "top_recovered_nodes[0].matched_metrics.alpha_pct",
          "key": "alpha_pct",
          "value": {
            "key": "alpha_pct",
            "value": 39.89942548515961,
            "target": 39.89942548515961
          }
        },
        {
          "path": "top_recovered_nodes[0].matched_metrics.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": {
            "key": "max_drawdown_pct",
            "value": 25.904809362815108,
            "target": 25.904809362815108
          }
        },
        {
          "path": "top_recovered_nodes[0].matched_metrics.profit_factor",
          "key": "profit_factor",
          "value": {
            "key": "profit_factor",
            "value": 1.1919630955509348,
            "target": 1.1919630955509348
          }
        },
        {
          "path": "top_recovered_nodes[0].matched_metrics.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": {
            "key": "sharpe_ratio",
            "value": 0.7957270568329264,
            "target": 0.7957270568329264
          }
        },
        {
          "path": "top_recovered_nodes[0].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "top_recovered_nodes[0].summary.metric_like_values.spx_return_pct",
          "key": "spx_return_pct",
          "value": 76.844174428316
        },
        {
          "path": "top_recovered_nodes[0].summary.metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": 39.89942548515961
        },
        {
          "path": "top_recovered_nodes[0].summary.metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        },
        {
          "path": "top_recovered_nodes[0].summary.metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "top_recovered_nodes[0].summary.metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.7957270568329264
        },
        {
          "path": "top_recovered_nodes[1].target_diffs_abs.total_return_pct",
          "key": "total_return_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[1].target_diffs_abs.spx_return_pct",
          "key": "spx_return_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[1].target_diffs_abs.alpha_pct",
          "key": "alpha_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[1].target_diffs_abs.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[1].target_diffs_abs.profit_factor",
          "key": "profit_factor",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[1].target_diffs_abs.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[1].matched_metrics.total_return_pct",
          "key": "total_return_pct",
          "value": {
            "key": "total_return_pct",
            "value": 116.7435999134756,
            "target": 116.7435999134756
          }
        },
        {
          "path": "top_recovered_nodes[1].matched_metrics.spx_return_pct",
          "key": "spx_return_pct",
          "value": {
            "key": "spx_return_pct",
            "value": 76.844174428316,
            "target": 76.844174428316
          }
        },
        {
          "path": "top_recovered_nodes[1].matched_metrics.alpha_pct",
          "key": "alpha_pct",
          "value": {
            "key": "alpha_pct",
            "value": 39.89942548515961,
            "target": 39.89942548515961
          }
        },
        {
          "path": "top_recovered_nodes[1].matched_metrics.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": {
            "key": "max_drawdown_pct",
            "value": 25.904809362815108,
            "target": 25.904809362815108
          }
        },
        {
          "path": "top_recovered_nodes[1].matched_metrics.profit_factor",
          "key": "profit_factor",
          "value": {
            "key": "profit_factor",
            "value": 1.1919630955509348,
            "target": 1.1919630955509348
          }
        },
        {
          "path": "top_recovered_nodes[1].matched_metrics.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": {
            "key": "sharpe_ratio",
            "value": 0.7957270568329264,
            "target": 0.7957270568329264
          }
        },
        {
          "path": "top_recovered_nodes[1].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "top_recovered_nodes[1].summary.metric_like_values.spx_return_pct",
          "key": "spx_return_pct",
          "value": 76.844174428316
        },
        {
          "path": "top_recovered_nodes[1].summary.metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": 39.89942548515961
        },
        {
          "path": "top_recovered_nodes[1].summary.metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        },
        {
          "path": "top_recovered_nodes[1].summary.metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "top_recovered_nodes[1].summary.metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.7957270568329264
        },
        {
          "path": "top_recovered_nodes[2].target_diffs_abs.total_return_pct",
          "key": "total_return_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[2].target_diffs_abs.spx_return_pct",
          "key": "spx_return_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[2].target_diffs_abs.alpha_pct",
          "key": "alpha_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[2].target_diffs_abs.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[2].target_diffs_abs.profit_factor",
          "key": "profit_factor",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[2].target_diffs_abs.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[2].matched_metrics.total_return_pct",
          "key": "total_return_pct",
          "value": {
            "key": "total_return_pct",
            "value": 116.7435999134756,
            "target": 116.7435999134756
          }
        },
        {
          "path": "top_recovered_nodes[2].matched_metrics.spx_return_pct",
          "key": "spx_return_pct",
          "value": {
            "key": "spx_return_pct",
            "value": 76.844174428316,
            "target": 76.844174428316
          }
        },
        {
          "path": "top_recovered_nodes[2].matched_metrics.alpha_pct",
          "key": "alpha_pct",
          "value": {
            "key": "alpha_pct",
            "value": 39.89942548515961,
            "target": 39.89942548515961
          }
        },
        {
          "path": "top_recovered_nodes[2].matched_metrics.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": {
            "key": "max_drawdown_pct",
            "value": 25.904809362815108,
            "target": 25.904809362815108
          }
        },
        {
          "path": "top_recovered_nodes[2].matched_metrics.profit_factor",
          "key": "profit_factor",
          "value": {
            "key": "profit_factor",
            "value": 1.1919630955509348,
            "target": 1.1919630955509348
          }
        },
        {
          "path": "top_recovered_nodes[2].matched_metrics.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": {
            "key": "sharpe_ratio",
            "value": 0.7957270568329264,
            "target": 0.7957270568329264
          }
        },
        {
          "path": "top_recovered_nodes[2].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "top_recovered_nodes[2].summary.metric_like_values.spx_return_pct",
          "key": "spx_return_pct",
          "value": 76.844174428316
        },
        {
          "path": "top_recovered_nodes[2].summary.metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": 39.89942548515961
        },
        {
          "path": "top_recovered_nodes[2].summary.metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        },
        {
          "path": "top_recovered_nodes[2].summary.metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "top_recovered_nodes[2].summary.metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.7957270568329264
        },
        {
          "path": "top_recovered_nodes[3].target_diffs_abs.total_return_pct",
          "key": "total_return_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[3].target_diffs_abs.spx_return_pct",
          "key": "spx_return_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[3].target_diffs_abs.alpha_pct",
          "key": "alpha_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[3].target_diffs_abs.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[3].target_diffs_abs.profit_factor",
          "key": "profit_factor",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[3].target_diffs_abs.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[3].matched_metrics.total_return_pct",
          "key": "total_return_pct",
          "value": {
            "key": "total_return_pct",
            "value": 116.7435999134756,
            "target": 116.7435999134756
          }
        },
        {
          "path": "top_recovered_nodes[3].matched_metrics.spx_return_pct",
          "key": "spx_return_pct",
          "value": {
            "key": "spx_return_pct",
            "value": 76.844174428316,
            "target": 76.844174428316
          }
        },
        {
          "path": "top_recovered_nodes[3].matched_metrics.alpha_pct",
          "key": "alpha_pct",
          "value": {
            "key": "alpha_pct",
            "value": 39.89942548515961,
            "target": 39.89942548515961
          }
        },
        {
          "path": "top_recovered_nodes[3].matched_metrics.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": {
            "key": "max_drawdown_pct",
            "value": 25.904809362815108,
            "target": 25.904809362815108
          }
        },
        {
          "path": "top_recovered_nodes[3].matched_metrics.profit_factor",
          "key": "profit_factor",
          "value": {
            "key": "profit_factor",
            "value": 1.1919630955509348,
            "target": 1.1919630955509348
          }
        },
        {
          "path": "top_recovered_nodes[3].matched_metrics.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": {
            "key": "sharpe_ratio",
            "value": 0.7957270568329264,
            "target": 0.7957270568329264
          }
        },
        {
          "path": "top_recovered_nodes[3].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "top_recovered_nodes[3].summary.metric_like_values.spx_return_pct",
          "key": "spx_return_pct",
          "value": 76.844174428316
        },
        {
          "path": "top_recovered_nodes[3].summary.metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": 39.89942548515961
        },
        {
          "path": "top_recovered_nodes[3].summary.metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        },
        {
          "path": "top_recovered_nodes[3].summary.metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "top_recovered_nodes[3].summary.metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.7957270568329264
        },
        {
          "path": "top_recovered_nodes[4].target_diffs_abs.total_return_pct",
          "key": "total_return_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[4].target_diffs_abs.spx_return_pct",
          "key": "spx_return_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[4].target_diffs_abs.alpha_pct",
          "key": "alpha_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[4].target_diffs_abs.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[4].target_diffs_abs.profit_factor",
          "key": "profit_factor",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[4].target_diffs_abs.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[4].matched_metrics.total_return_pct",
          "key": "total_return_pct",
          "value": {
            "key": "total_return_pct",
            "value": 116.7435999134756,
            "target": 116.7435999134756
          }
        },
        {
          "path": "top_recovered_nodes[4].matched_metrics.spx_return_pct",
          "key": "spx_return_pct",
          "value": {
            "key": "spx_return_pct",
            "value": 76.844174428316,
            "target": 76.844174428316
          }
        },
        {
          "path": "top_recovered_nodes[4].matched_metrics.alpha_pct",
          "key": "alpha_pct",
          "value": {
            "key": "alpha_pct",
            "value": 39.89942548515961,
            "target": 39.89942548515961
          }
        },
        {
          "path": "top_recovered_nodes[4].matched_metrics.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": {
            "key": "max_drawdown_pct",
            "value": 25.904809362815108,
            "target": 25.904809362815108
          }
        },
        {
          "path": "top_recovered_nodes[4].matched_metrics.profit_factor",
          "key": "profit_factor",
          "value": {
            "key": "profit_factor",
            "value": 1.1919630955509348,
            "target": 1.1919630955509348
          }
        },
        {
          "path": "top_recovered_nodes[4].matched_metrics.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": {
            "key": "sharpe_ratio",
            "value": 0.7957270568329264,
            "target": 0.7957270568329264
          }
        },
        {
          "path": "top_recovered_nodes[4].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "top_recovered_nodes[4].summary.metric_like_values.spx_return_pct",
          "key": "spx_return_pct",
          "value": 76.844174428316
        },
        {
          "path": "top_recovered_nodes[4].summary.metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": 39.89942548515961
        },
        {
          "path": "top_recovered_nodes[4].summary.metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        },
        {
          "path": "top_recovered_nodes[4].summary.metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "top_recovered_nodes[4].summary.metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.7957270568329264
        },
        {
          "path": "top_recovered_nodes[5].target_diffs_abs.total_return_pct",
          "key": "total_return_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[5].target_diffs_abs.spx_return_pct",
          "key": "spx_return_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[5].target_diffs_abs.alpha_pct",
          "key": "alpha_pct",
          "value": 0.0
        },
        {
          "path": "top_recovered_nodes[5].target_diffs_abs.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 0.0
        }
      ],
      "market_hits": [
        {
          "path": "top_recovered_nodes[17].summary.daily_records_first.market_gate_state",
          "key": "market_gate_state",
          "value": "RISK_OFF"
        },
        {
          "path": "top_recovered_nodes[17].summary.daily_records_last.market_gate_state",
          "key": "market_gate_state",
          "value": "ALLOW"
        },
        {
          "path": "top_recovered_nodes[18].summary.daily_records_first.market_gate_state",
          "key": "market_gate_state",
          "value": "RISK_OFF"
        },
        {
          "path": "top_recovered_nodes[18].summary.daily_records_last.market_gate_state",
          "key": "market_gate_state",
          "value": "ALLOW"
        },
        {
          "path": "top_recovered_nodes[19].summary.daily_records_first.market_gate_state",
          "key": "market_gate_state",
          "value": "RISK_OFF"
        },
        {
          "path": "top_recovered_nodes[19].summary.daily_records_last.market_gate_state",
          "key": "market_gate_state",
          "value": "ALLOW"
        },
        {
          "path": "top_recovered_nodes[19].summary.trades_first.exit_warning_log[0].market_state",
          "key": "market_state",
          "value": "FULL_ON"
        },
        {
          "path": "top_recovered_nodes[19].summary.trades_first.exit_warning_log[1].market_state",
          "key": "market_state",
          "value": "FULL_ON"
        },
        {
          "path": "top_recovered_nodes[19].summary.trades_last.exit_warning_log[0].market_state",
          "key": "market_state",
          "value": "FULL_ON"
        },
        {
          "path": "top_recovered_nodes[19].summary.trades_last.exit_warning_log[1].market_state",
          "key": "market_state",
          "value": "FULL_ON"
        },
        {
          "path": "top_recovered_nodes[20].summary.daily_records_first.market_gate_state",
          "key": "market_gate_state",
          "value": "RISK_OFF"
        },
        {
          "path": "top_recovered_nodes[20].summary.daily_records_last.market_gate_state",
          "key": "market_gate_state",
          "value": "ALLOW"
        },
        {
          "path": "top_recovered_nodes[21].summary.daily_records_first.market_gate_state",
          "key": "market_gate_state",
          "value": "RISK_OFF"
        },
        {
          "path": "top_recovered_nodes[21].summary.daily_records_last.market_gate_state",
          "key": "market_gate_state",
          "value": "ALLOW"
        },
        {
          "path": "top_recovered_nodes[21].summary.trades_first.exit_warning_log[0].market_state",
          "key": "market_state",
          "value": "FULL_ON"
        },
        {
          "path": "top_recovered_nodes[21].summary.trades_first.exit_warning_log[1].market_state",
          "key": "market_state",
          "value": "FULL_ON"
        },
        {
          "path": "top_recovered_nodes[21].summary.trades_last.exit_warning_log[0].market_state",
          "key": "market_state",
          "value": "FULL_ON"
        },
        {
          "path": "top_recovered_nodes[21].summary.trades_last.exit_warning_log[1].market_state",
          "key": "market_state",
          "value": "FULL_ON"
        },
        {
          "path": "top_recovered_nodes[34].summary.trades_first.entry_regime",
          "key": "entry_regime",
          "value": "UPTREND"
        },
        {
          "path": "top_recovered_nodes[34].summary.trades_first.exit_regime",
          "key": "exit_regime",
          "value": "UPTREND"
        },
        {
          "path": "top_recovered_nodes[34].summary.trades_first.dominant_regime",
          "key": "dominant_regime",
          "value": "UPTREND"
        },
        {
          "path": "top_recovered_nodes[34].summary.trades_first.regime_day_weights",
          "key": "regime_day_weights",
          "value": {
            "UPTREND": 25
          }
        },
        {
          "path": "top_recovered_nodes[34].summary.trades_first.regime_day_weights.UPTREND",
          "key": "UPTREND",
          "value": 25
        },
        {
          "path": "top_recovered_nodes[34].summary.trades_last.entry_regime",
          "key": "entry_regime",
          "value": "UPTREND"
        },
        {
          "path": "top_recovered_nodes[34].summary.trades_last.exit_regime",
          "key": "exit_regime",
          "value": "UPTREND"
        },
        {
          "path": "top_recovered_nodes[34].summary.trades_last.dominant_regime",
          "key": "dominant_regime",
          "value": "UPTREND"
        },
        {
          "path": "top_recovered_nodes[34].summary.trades_last.regime_day_weights",
          "key": "regime_day_weights",
          "value": {
            "UPTREND": 34
          }
        },
        {
          "path": "top_recovered_nodes[34].summary.trades_last.regime_day_weights.UPTREND",
          "key": "UPTREND",
          "value": 34
        },
        {
          "path": "top_recovered_nodes[48].summary.daily_records_first.market_gate_state",
          "key": "market_gate_state",
          "value": "RISK_OFF"
        },
        {
          "path": "top_recovered_nodes[48].summary.daily_records_last.market_gate_state",
          "key": "market_gate_state",
          "value": "ALLOW"
        },
        {
          "path": "core_variant_candidates[0].summary.daily_records_first.market_gate_state",
          "key": "market_gate_state",
          "value": "RISK_OFF"
        },
        {
          "path": "core_variant_candidates[0].summary.daily_records_last.market_gate_state",
          "key": "market_gate_state",
          "value": "ALLOW"
        },
        {
          "path": "core_variant_candidates[1].summary.daily_records_first.market_gate_state",
          "key": "market_gate_state",
          "value": "RISK_OFF"
        },
        {
          "path": "core_variant_candidates[1].summary.daily_records_last.market_gate_state",
          "key": "market_gate_state",
          "value": "ALLOW"
        },
        {
          "path": "daily_equity_candidates[0].summary.daily_records_first.market_gate_state",
          "key": "market_gate_state",
          "value": "RISK_OFF"
        },
        {
          "path": "daily_equity_candidates[0].summary.daily_records_last.market_gate_state",
          "key": "market_gate_state",
          "value": "ALLOW"
        },
        {
          "path": "daily_equity_candidates[1].summary.daily_records_first.market_gate_state",
          "key": "market_gate_state",
          "value": "RISK_OFF"
        },
        {
          "path": "daily_equity_candidates[1].summary.daily_records_last.market_gate_state",
          "key": "market_gate_state",
          "value": "ALLOW"
        },
        {
          "path": "daily_equity_candidates[2].summary.daily_records_first.market_gate_state",
          "key": "market_gate_state",
          "value": "RISK_OFF"
        },
        {
          "path": "daily_equity_candidates[2].summary.daily_records_last.market_gate_state",
          "key": "market_gate_state",
          "value": "ALLOW"
        },
        {
          "path": "daily_equity_candidates[2].summary.trades_first.exit_warning_log[0].market_state",
          "key": "market_state",
          "value": "FULL_ON"
        },
        {
          "path": "daily_equity_candidates[2].summary.trades_first.exit_warning_log[1].market_state",
          "key": "market_state",
          "value": "FULL_ON"
        },
        {
          "path": "daily_equity_candidates[2].summary.trades_last.exit_warning_log[0].market_state",
          "key": "market_state",
          "value": "FULL_ON"
        },
        {
          "path": "daily_equity_candidates[2].summary.trades_last.exit_warning_log[1].market_state",
          "key": "market_state",
          "value": "FULL_ON"
        },
        {
          "path": "daily_equity_candidates[3].summary.daily_records_first.market_gate_state",
          "key": "market_gate_state",
          "value": "RISK_OFF"
        },
        {
          "path": "daily_equity_candidates[3].summary.daily_records_last.market_gate_state",
          "key": "market_gate_state",
          "value": "ALLOW"
        },
        {
          "path": "daily_equity_candidates[4].summary.daily_records_first.market_gate_state",
          "key": "market_gate_state",
          "value": "RISK_OFF"
        },
        {
          "path": "daily_equity_candidates[4].summary.daily_records_last.market_gate_state",
          "key": "market_gate_state",
          "value": "ALLOW"
        },
        {
          "path": "daily_equity_candidates[4].summary.trades_first.exit_warning_log[0].market_state",
          "key": "market_state",
          "value": "FULL_ON"
        },
        {
          "path": "daily_equity_candidates[4].summary.trades_first.exit_warning_log[1].market_state",
          "key": "market_state",
          "value": "FULL_ON"
        },
        {
          "path": "daily_equity_candidates[4].summary.trades_last.exit_warning_log[0].market_state",
          "key": "market_state",
          "value": "FULL_ON"
        },
        {
          "path": "daily_equity_candidates[4].summary.trades_last.exit_warning_log[1].market_state",
          "key": "market_state",
          "value": "FULL_ON"
        },
        {
          "path": "daily_equity_candidates[5].summary.trades_first.entry_regime",
          "key": "entry_regime",
          "value": "UPTREND"
        },
        {
          "path": "daily_equity_candidates[5].summary.trades_first.exit_regime",
          "key": "exit_regime",
          "value": "UPTREND"
        },
        {
          "path": "daily_equity_candidates[5].summary.trades_first.dominant_regime",
          "key": "dominant_regime",
          "value": "UPTREND"
        },
        {
          "path": "daily_equity_candidates[5].summary.trades_first.regime_day_weights",
          "key": "regime_day_weights",
          "value": {
            "UPTREND": 25
          }
        },
        {
          "path": "daily_equity_candidates[5].summary.trades_first.regime_day_weights.UPTREND",
          "key": "UPTREND",
          "value": 25
        },
        {
          "path": "daily_equity_candidates[5].summary.trades_last.entry_regime",
          "key": "entry_regime",
          "value": "UPTREND"
        },
        {
          "path": "daily_equity_candidates[5].summary.trades_last.exit_regime",
          "key": "exit_regime",
          "value": "UPTREND"
        },
        {
          "path": "daily_equity_candidates[5].summary.trades_last.dominant_regime",
          "key": "dominant_regime",
          "value": "UPTREND"
        },
        {
          "path": "daily_equity_candidates[5].summary.trades_last.regime_day_weights",
          "key": "regime_day_weights",
          "value": {
            "UPTREND": 34
          }
        },
        {
          "path": "daily_equity_candidates[5].summary.trades_last.regime_day_weights.UPTREND",
          "key": "UPTREND",
          "value": 34
        },
        {
          "path": "daily_equity_candidates[6].summary.daily_records_first.market_gate_state",
          "key": "market_gate_state",
          "value": "RISK_OFF"
        },
        {
          "path": "daily_equity_candidates[6].summary.daily_records_last.market_gate_state",
          "key": "market_gate_state",
          "value": "ALLOW"
        }
      ],
      "e1r_hits": [
        {
          "path": "stage",
          "key": "stage",
          "value": "B_STAGE_3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY"
        },
        {
          "path": "status",
          "key": "status",
          "value": "E1R_CORE_VARIANT_SOURCE_RECOVERY_COMPLETE_NO_EXPORTS_WRITTEN"
        },
        {
          "path": "policy.e1r_canonical_written",
          "key": "e1r_canonical_written",
          "value": false
        },
        {
          "path": "input.previous_report",
          "key": "previous_report",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json"
        },
        {
          "path": "input.candidate_files[0]",
          "key": "[0]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json"
        },
        {
          "path": "input.candidate_files[1]",
          "key": "[1]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json"
        },
        {
          "path": "input.candidate_files[2]",
          "key": "[2]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json"
        },
        {
          "path": "input.candidate_files[3]",
          "key": "[3]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json"
        },
        {
          "path": "input.candidate_files[4]",
          "key": "[4]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json"
        },
        {
          "path": "input.candidate_files[5]",
          "key": "[5]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json"
        },
        {
          "path": "input.candidate_files[6]",
          "key": "[6]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json"
        },
        {
          "path": "input.candidate_files[7]",
          "key": "[7]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10E_R_CONTINUOUS_CAPITAL_CONTRACT.json"
        },
        {
          "path": "input.candidate_files[8]",
          "key": "[8]",
          "value": "docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json"
        },
        {
          "path": "input.candidate_files[9]",
          "key": "[9]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json"
        },
        {
          "path": "input.candidate_files[10]",
          "key": "[10]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json"
        },
        {
          "path": "input.candidate_files[11]",
          "key": "[11]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10A_DIRECT_GENERATOR_FUNCTION_AUDIT.json"
        },
        {
          "path": "input.candidate_files[12]",
          "key": "[12]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C1_5Y_EQUITY_ARTIFACT_AUDIT.json"
        },
        {
          "path": "input.candidate_files[13]",
          "key": "[13]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C6_INTERVAL_SCHEMA_SOURCE_AUDIT.json"
        },
        {
          "path": "input.candidate_files[14]",
          "key": "[14]",
          "value": "docs/research/E1R_V0_2_STAGE3_8A_DASHBOARD_REFACTOR_AUDIT.json"
        },
        {
          "path": "input.candidate_files[15]",
          "key": "[15]",
          "value": "docs/research/E1R_V0_2_STAGE3_8D_NATIVE_RENDER_AUDIT.json"
        },
        {
          "path": "input.candidate_files[16]",
          "key": "[16]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F1G0_SUMMARY_MAPPING_AUDIT.json"
        },
        {
          "path": "input.candidate_files[17]",
          "key": "[17]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3D_E1_CANONICAL_INTEGRITY_AUDIT.json"
        },
        {
          "path": "input.candidate_files[18]",
          "key": "[18]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json"
        },
        {
          "path": "input.candidate_files[19]",
          "key": "[19]",
          "value": "exports/e1r_v0_2_backtest_summary.json"
        },
        {
          "path": "input.candidate_files[20]",
          "key": "[20]",
          "value": "data/research/e1r/e1r_formal_backtest_v0_1.json"
        },
        {
          "path": "input.candidate_files[21]",
          "key": "[21]",
          "value": "data/research/e1r/e1r_phase3e_confirmed_quality_diagnostic.json"
        },
        {
          "path": "input.candidate_files[22]",
          "key": "[22]",
          "value": "data/research/e1r/e1r_regime_attribution_review.json"
        },
        {
          "path": "input.candidate_files[23]",
          "key": "[23]",
          "value": "docs/research/E1R_V0_2_STAGE3_2_BACKTEST_INTEGRATION_REPORT.json"
        },
        {
          "path": "input.candidate_files[24]",
          "key": "[24]",
          "value": "docs/research/E1R_V0_2_STAGE3_5_DEPENDENCY_FIX_REPORT.json"
        },
        {
          "path": "input.candidate_files[25]",
          "key": "[25]",
          "value": "docs/research/E1R_V0_2_STAGE3_5_MAIN_SMOKE_TEST_REPORT.json"
        },
        {
          "path": "input.candidate_files[26]",
          "key": "[26]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2B_STRUCTURAL_DIFF_AUDIT.json"
        },
        {
          "path": "input.candidate_files[27]",
          "key": "[27]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2B_V3_PREPATCH_AUDIT.json"
        },
        {
          "path": "input.candidate_files[28]",
          "key": "[28]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2B_V4_SURGICAL_MAP.json"
        },
        {
          "path": "input.candidate_files[29]",
          "key": "[29]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F1B_FORWARD_IMPLEMENTATION_PLAN.json"
        },
        {
          "path": "input.candidate_files[30]",
          "key": "[30]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F1C_RUNNER_DRY_RUN_AUDIT.json"
        },
        {
          "path": "input.candidate_files[31]",
          "key": "[31]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C3A_TRADE_LOG_RENDER_PATH_AUDIT.json"
        },
        {
          "path": "input.candidate_files[32]",
          "key": "[32]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json"
        },
        {
          "path": "input.candidate_files[33]",
          "key": "[33]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4A_EQUITY_CURVE_RENDER_AUDIT.json"
        },
        {
          "path": "input.candidate_files[34]",
          "key": "[34]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F1_E1_CONTINUOUS_CORE_RECOVERY.json"
        },
        {
          "path": "input.candidate_files[35]",
          "key": "[35]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3A_E1_MODULE_ENTRY_RECOVERY.json"
        },
        {
          "path": "input.candidate_files[36]",
          "key": "[36]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3B_E1_STATEFUL_WRAPPER_PROBE.json"
        },
        {
          "path": "input.candidate_files[37]",
          "key": "[37]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3C_E1_CORE_EXPORT_REPORT.json"
        },
        {
          "path": "input.candidate_files[38]",
          "key": "[38]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C5_EXPORT_WRAPPER_SMOKE_REPORT.json"
        },
        {
          "path": "input.candidate_files[39]",
          "key": "[39]",
          "value": "exports/oos_e1r_v0_2_summary.json"
        },
        {
          "path": "input.candidate_files[40]",
          "key": "[40]",
          "value": "docs/research/E1R_V0_2_STAGE3_5_ARTIFACT_DISCOVERY_REPORT.json"
        },
        {
          "path": "input.candidate_files[41]",
          "key": "[41]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4A1_SIDECAR_ACTIVATION_AUDIT.json"
        },
        {
          "path": "input.candidate_files[42]",
          "key": "[42]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4A2_SIDECAR_RANKINGS_ACTIVATION_PROBE.json"
        },
        {
          "path": "input.candidate_files[43]",
          "key": "[43]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F2_E1_BACKTEST_ENTRY_AUDIT.json"
        },
        {
          "path": "input.candidate_files[47]",
          "key": "[47]",
          "value": "docs/research/E1R_V0_2_STAGE2_HIGH_RISK_REVIEW.json"
        },
        {
          "path": "input.candidate_files[48]",
          "key": "[48]",
          "value": "docs/research/E1R_V0_2_STAGE3_1_WORKFLOW_FIX_REPORT.json"
        },
        {
          "path": "input.candidate_files[49]",
          "key": "[49]",
          "value": "docs/research/E1R_V0_2_STAGE3_1_WORKFLOW_PATCH_REPORT.json"
        },
        {
          "path": "input.candidate_files[50]",
          "key": "[50]",
          "value": "docs/research/E1R_V0_2_STAGE3_6_DASHBOARD_PATH_FIX_REPORT.json"
        },
        {
          "path": "input.candidate_files[51]",
          "key": "[51]",
          "value": "docs/research/E1R_V0_2_STAGE3_8B_DASHBOARD_REFACTOR_REPORT.json"
        },
        {
          "path": "input.candidate_files[52]",
          "key": "[52]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E1_NATIVE_RESEARCH_CLEANUP_REPORT.json"
        },
        {
          "path": "input.candidate_files[53]",
          "key": "[53]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F1E1_TARGET_SOURCE_CONTRACT.json"
        },
        {
          "path": "input.candidate_files[54]",
          "key": "[54]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F1F0_DAILY_PIPELINE_AUDIT.json"
        },
        {
          "path": "input.candidate_files[55]",
          "key": "[55]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F1F1A_DAILY_SEQUENCE_DRY_RUN_AUDIT.json"
        },
        {
          "path": "input.candidate_files[56]",
          "key": "[56]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F1F1C_DAILY_SEQUENCE_DRY_RUN_AFTER_FIX.json"
        },
        {
          "path": "input.candidate_files[57]",
          "key": "[57]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F1F1D_PINPOINT_RESET_SCRIPT.json"
        },
        {
          "path": "input.candidate_files[58]",
          "key": "[58]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F1F1F_FULL_DAILY_SEQUENCE_AFTER_OOS_PATCH.json"
        },
        {
          "path": "input.candidate_files[59]",
          "key": "[59]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C0_EQUITY_CURVE_MAPPING_AUDIT.json"
        },
        {
          "path": "input.candidate_files[60]",
          "key": "[60]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C3FA_MARKET_STATE_FIELD_AUDIT.json"
        },
        {
          "path": "input.candidate_files[61]",
          "key": "[61]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C3FC_E1R_STATUS_TREND_FIELD_AUDIT.json"
        },
        {
          "path": "input.candidate_files[62]",
          "key": "[62]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10B_DIRECT_GENERATOR_DRY_RUN_AUDIT.json"
        },
        {
          "path": "input.candidate_files[63]",
          "key": "[63]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10C_SIDECAR_BUILD_FAILURE_AUDIT.json"
        },
        {
          "path": "input.candidate_files[64]",
          "key": "[64]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10D_REGIME_AWARE_SIDECAR_PROBE.json"
        },
        {
          "path": "input.candidate_files[65]",
          "key": "[65]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4A_SIDECAR_RECORDS_EXPORT_REPORT.json"
        },
        {
          "path": "input.candidate_files[66]",
          "key": "[66]",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C9_CONTROLLED_LONG_EXPORT_AUDIT.json"
        },
        {
          "path": "input.candidate_files[67]",
          "key": "[67]",
          "value": "exports/e1r_v0_2_sidecar_records_5y.json"
        },
        {
          "path": "input.candidate_files[68]",
          "key": "[68]",
          "value": "exports/e1r_v0_2_status.json"
        },
        {
          "path": "input.candidate_files[69]",
          "key": "[69]",
          "value": "exports/oos_e1r_v0_2_equity_curve.json"
        },
        {
          "path": "input.candidate_files[70]",
          "key": "[70]",
          "value": "exports/oos_e1r_v0_2_orders.json"
        },
        {
          "path": "input.candidate_files[71]",
          "key": "[71]",
          "value": "exports/oos_e1r_v0_2_orders_preview.json"
        },
        {
          "path": "input.candidate_files[72]",
          "key": "[72]",
          "value": "exports/oos_e1r_v0_2_positions.json"
        },
        {
          "path": "input.candidate_files[73]",
          "key": "[73]",
          "value": "exports/oos_e1r_v0_2_positions_preview.json"
        },
        {
          "path": "input.candidate_files[74]",
          "key": "[74]",
          "value": "exports/oos_e1r_v0_2_targets.json"
        },
        {
          "path": "input.candidate_files[75]",
          "key": "[75]",
          "value": "exports/e1r_v0_2_backtest_equity_curve.json"
        },
        {
          "path": "recovery_summary.conclusion",
          "key": "conclusion",
          "value": "E1R_FROZEN_METRIC_ARTIFACT_FOUND_CORE_SOURCE_CANDIDATES_PRESENT"
        },
        {
          "path": "top_recovered_nodes[0].summary.path",
          "key": "path",
          "value": "$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics"
        },
        {
          "path": "top_recovered_nodes[0].summary.metric_like_values.strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "top_recovered_nodes[0].file",
          "key": "file",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json"
        },
        {
          "path": "top_recovered_nodes[1].summary.metric_like_values.strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "top_recovered_nodes[1].file",
          "key": "file",
          "value": "exports/e1r_v0_2_backtest_summary.json"
        },
        {
          "path": "top_recovered_nodes[2].summary.path",
          "key": "path",
          "value": "$.export_reports.e1r_backtest_summary.e1r_objects[0].summary_fields"
        },
        {
          "path": "top_recovered_nodes[2].file",
          "key": "file",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json"
        },
        {
          "path": "top_recovered_nodes[3].file",
          "key": "file",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C5_EXPORT_WRAPPER_SMOKE_REPORT.json"
        },
        {
          "path": "top_recovered_nodes[4].summary.path",
          "key": "path",
          "value": "$.json_file_reports.docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json.lists[11].first_sample.summary_fields"
        },
        {
          "path": "top_recovered_nodes[4].file",
          "key": "file",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json"
        },
        {
          "path": "top_recovered_nodes[5].summary.path",
          "key": "path",
          "value": "$.json_file_reports.docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json.lists[11].last_sample.summary_fields"
        },
        {
          "path": "top_recovered_nodes[5].file",
          "key": "file",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json"
        },
        {
          "path": "top_recovered_nodes[6].file",
          "key": "file",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json"
        },
        {
          "path": "top_recovered_nodes[7].file",
          "key": "file",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json"
        },
        {
          "path": "top_recovered_nodes[8].summary.path",
          "key": "path",
          "value": "$.specific_files.exports/e1r_v0_2_backtest_summary.json.top_level_metrics"
        },
        {
          "path": "top_recovered_nodes[8].summary.metric_like_values.strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "top_recovered_nodes[8].file",
          "key": "file",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json"
        },
        {
          "path": "top_recovered_nodes[9].summary.path",
          "key": "path",
          "value": "$.json_summaries.exports/e1r_v0_2_backtest_summary.json"
        },
        {
          "path": "top_recovered_nodes[9].summary.metric_like_values.strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "top_recovered_nodes[9].file",
          "key": "file",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json"
        },
        {
          "path": "top_recovered_nodes[10].file",
          "key": "file",
          "value": "docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json"
        },
        {
          "path": "top_recovered_nodes[11].file",
          "key": "file",
          "value": "docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json"
        }
      ],
      "counts": {
        "return_hits": 142,
        "metric_hits": 891,
        "market_hits": 64,
        "e1r_hits": 246
      },
      "score": 180
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
      "sha256": "5944e610222879e27dd99515fad747febfcdb2da12a0abc89d6ff861e55d41cd",
      "top_level": {
        "status": "E1R_GENERATOR_PATH_TRACE_COMPLETE_NO_EXPORTS_WRITTEN"
      },
      "return_hits": [
        {
          "path": "generator_candidates[0].matched_terms[2]",
          "key": "[2]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[1].matched_terms[2]",
          "key": "[2]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[2].matched_terms[2]",
          "key": "[2]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[2].hits[0].matched[0]",
          "key": "[0]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[2].hits[10].matched[0]",
          "key": "[0]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[2].hits[13].matched[0]",
          "key": "[0]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[2].hits[17].matched[0]",
          "key": "[0]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[2].hits[21].matched[0]",
          "key": "[0]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[2].hits[24].matched[0]",
          "key": "[0]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[2].hits[26].matched[0]",
          "key": "[0]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[2].hits[29].matched[0]",
          "key": "[0]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[3].matched_terms[2]",
          "key": "[2]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[4].matched_terms[1]",
          "key": "[1]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[4].hits[16].matched[0]",
          "key": "[0]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[5].matched_terms[2]",
          "key": "[2]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[6].matched_terms[2]",
          "key": "[2]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[7].matched_terms[2]",
          "key": "[2]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[7].hits[7].matched[0]",
          "key": "[0]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[7].hits[10].matched[0]",
          "key": "[0]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generator_candidates[7].hits[14].matched[0]",
          "key": "[0]",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        }
      ],
      "metric_hits": [
        {
          "path": "function_indexes.src/engine/e1r_composer.py.extract_core_interval_returns",
          "key": "extract_core_interval_returns",
          "value": "{\"line\": 94, \"end_line\": 168, \"matched_terms\": [\"daily_equity_records\", \"extract_core_interval_returns\"], \"source\": \"def extract_core_interval_returns(\\n    core_daily_equity_records: Sequence[dict[str, Any]],\\n    sidecar_records: Sequence[dict[str, Any]],\\n) -> list[dict[str, Any]]:\\n    \\\"\\\"\\\"\\n    Align core daily returns to sidecar intervals by next_date.\\n\\n    Returns one record per shared interval:\\n    {\\n      date,\\n      next_date,\\n      core_return,\\n      sidecar_return,\\n      spx_return,\\n      ...\\n    }\\n    \\\"\\\"\\\"\\n    core_by_end_date = {}\\n\\n    for row in core_daily_equity_records:\\n        date = row.get(\\\"date\\\")\\n        if not date:\\n            continue\\n\\n        r = safe_float(row.get(\\\"daily_return\\\"))\\n        if r is None:\\n            # Some historical outputs may store pct instead of decimal.\\n            rp = safe_float(row.get(\\\"daily_return_pct\\\"))\\n            r = None if rp is None else rp / 100.0\\n\\n        if r is None:\\n            continue\\n\\n        core_by_end_date[date] = row | {\\\"_normalized_daily_return\\\": r}\\n\\n    aligned: list[dict[str, Any]] = []\\n\\n    for sidecar in sidecar_records:\\n        date = sidecar.get(\\\"date\\\")\\n      ...<truncated>"
        },
        {
          "path": "function_indexes.src/engine/e1r_composer.py.build_equity_records_from_returns",
          "key": "build_equity_records_from_returns",
          "value": "{\"line\": 171, \"end_line\": 211, \"matched_terms\": [\"build_equity_records_from_returns\"], \"source\": \"def build_equity_records_from_returns(\\n    interval_records: Sequence[dict[str, Any]],\\n    initial_equity: float,\\n) -> list[dict[str, Any]]:\\n    equity = initial_equity\\n    peak = initial_equity\\n    records: list[dict[str, Any]] = []\\n\\n    for row in interval_records:\\n        r = safe_float(row.get(\\\"combined_return\\\")) or 0.0\\n        equity *= 1.0 + r\\n        peak = max(peak, equity)\\n\\n        drawdown = equity / peak - 1.0 if peak > 0 else 0.0\\n\\n        records.append({\\n            \\\"date\\\": row[\\\"next_date\\\"],\\n            \\\"interval_start_date\\\": row[\\\"date\\\"],\\n            \\\"interval_end_date\\\": row[\\\"next_date\\\"],\\n            \\\"total_equity\\\": equity,\\n            \\\"equity\\\": equity,\\n            \\\"daily_return\\\": r,\\n            \\\"daily_return_pct\\\": pct_display(r),\\n            \\\"drawdown\\\": drawdown,\\n            \\\"drawdown_pct\\\": pct_display(drawdown),\\n\\n            \\\"core_return\\\": row[\\\"core_return\\\"],\\n            \\\"core_return_pct\\\": row[\\\"core_return_pct\\\"],\\n            \\\"sidecar_return\\\": row[\\\"sidecar_return\\\"],\\n            \\\"sidecar_return_pct\\\": row[...<truncated>"
        },
        {
          "path": "json_probes[19].nodes[0].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 7.52
        },
        {
          "path": "json_probes[19].nodes[0].summary.metric_like_values.spx_total_return_pct",
          "key": "spx_total_return_pct",
          "value": 69.36
        },
        {
          "path": "json_probes[19].nodes[0].summary.metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": -61.84
        },
        {
          "path": "json_probes[19].nodes[0].summary.metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 38.1
        },
        {
          "path": "json_probes[19].nodes[0].summary.metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.25
        },
        {
          "path": "json_probes[19].nodes[0].summary.metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.18
        },
        {
          "path": "json_probes[19].nodes[1].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 7.52
        },
        {
          "path": "json_probes[19].nodes[1].summary.metric_like_values.spx_total_return_pct",
          "key": "spx_total_return_pct",
          "value": 69.36
        },
        {
          "path": "json_probes[19].nodes[1].summary.metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": -61.84
        },
        {
          "path": "json_probes[19].nodes[1].summary.metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 38.1
        },
        {
          "path": "json_probes[19].nodes[1].summary.metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.25
        },
        {
          "path": "json_probes[19].nodes[1].summary.metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.18
        },
        {
          "path": "json_probes[19].nodes[2].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": -21.95
        },
        {
          "path": "json_probes[19].nodes[2].summary.metric_like_values.spx_total_return_pct",
          "key": "spx_total_return_pct",
          "value": 69.36
        },
        {
          "path": "json_probes[19].nodes[2].summary.metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": -91.31
        },
        {
          "path": "json_probes[19].nodes[2].summary.metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 51.1
        },
        {
          "path": "json_probes[19].nodes[2].summary.metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 0.83
        },
        {
          "path": "json_probes[19].nodes[2].summary.metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": -0.15
        },
        {
          "path": "json_probes[21].nodes[0].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 7.52
        },
        {
          "path": "json_probes[21].nodes[0].summary.metric_like_values.spx_total_return_pct",
          "key": "spx_total_return_pct",
          "value": 69.36
        },
        {
          "path": "json_probes[21].nodes[0].summary.metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": -61.84
        },
        {
          "path": "json_probes[21].nodes[0].summary.metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 38.1
        },
        {
          "path": "json_probes[21].nodes[0].summary.metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.25
        },
        {
          "path": "json_probes[21].nodes[0].summary.metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.18
        },
        {
          "path": "json_probes[21].nodes[1].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 7.52
        },
        {
          "path": "json_probes[21].nodes[1].summary.metric_like_values.spx_total_return_pct",
          "key": "spx_total_return_pct",
          "value": 69.36
        },
        {
          "path": "json_probes[21].nodes[1].summary.metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": -61.84
        },
        {
          "path": "json_probes[21].nodes[1].summary.metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 38.1
        },
        {
          "path": "json_probes[21].nodes[1].summary.metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.25
        },
        {
          "path": "json_probes[21].nodes[1].summary.metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.18
        },
        {
          "path": "json_probes[21].nodes[2].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": -21.95
        },
        {
          "path": "json_probes[21].nodes[2].summary.metric_like_values.spx_total_return_pct",
          "key": "spx_total_return_pct",
          "value": 69.36
        },
        {
          "path": "json_probes[21].nodes[2].summary.metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": -91.31
        },
        {
          "path": "json_probes[21].nodes[2].summary.metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 51.1
        },
        {
          "path": "json_probes[21].nodes[2].summary.metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 0.83
        },
        {
          "path": "json_probes[21].nodes[2].summary.metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": -0.15
        }
      ],
      "market_hits": [
        {
          "path": "json_probes[1].nodes[0].summary.market_state_len",
          "key": "market_state_len",
          "value": 0
        },
        {
          "path": "json_probes[6].nodes[0].summary.exports/market_state.json_dict_keys",
          "key": "exports/market_state.json_dict_keys",
          "value": [
            "candidate_arrays",
            "candidate_objects",
            "meta",
            "preview"
          ]
        },
        {
          "path": "json_probes[6].nodes[0].summary.exports/market_state.json_dict_keys[0]",
          "key": "[0]",
          "value": "candidate_arrays"
        },
        {
          "path": "json_probes[6].nodes[0].summary.exports/market_state.json_dict_keys[1]",
          "key": "[1]",
          "value": "candidate_objects"
        },
        {
          "path": "json_probes[6].nodes[0].summary.exports/market_state.json_dict_keys[2]",
          "key": "[2]",
          "value": "meta"
        },
        {
          "path": "json_probes[6].nodes[0].summary.exports/market_state.json_dict_keys[3]",
          "key": "[3]",
          "value": "preview"
        },
        {
          "path": "json_probes[7].nodes[0].summary.exports/market_state.json_dict_keys",
          "key": "exports/market_state.json_dict_keys",
          "value": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ]
        },
        {
          "path": "json_probes[7].nodes[0].summary.exports/market_state.json_dict_keys[0]",
          "key": "[0]",
          "value": "json_valid"
        },
        {
          "path": "json_probes[7].nodes[0].summary.exports/market_state.json_dict_keys[1]",
          "key": "[1]",
          "value": "regime_like_keys"
        },
        {
          "path": "json_probes[7].nodes[0].summary.exports/market_state.json_dict_keys[2]",
          "key": "[2]",
          "value": "regime_like_samples"
        },
        {
          "path": "json_probes[7].nodes[0].summary.exports/market_state.json_dict_keys[3]",
          "key": "[3]",
          "value": "row_count"
        },
        {
          "path": "json_probes[7].nodes[0].summary.exports/market_state.json_dict_keys[4]",
          "key": "[4]",
          "value": "top_level_keys"
        },
        {
          "path": "json_probes[7].nodes[0].summary.exports/market_state.json_dict_keys[5]",
          "key": "[5]",
          "value": "top_level_type"
        },
        {
          "path": "json_probes[8].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys",
          "key": "data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys",
          "value": [
            "exists",
            "json_valid",
            "lists",
            "path",
            "top_keys",
            "type"
          ]
        },
        {
          "path": "json_probes[8].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[0]",
          "key": "[0]",
          "value": "exists"
        },
        {
          "path": "json_probes[8].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[1]",
          "key": "[1]",
          "value": "json_valid"
        },
        {
          "path": "json_probes[8].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[2]",
          "key": "[2]",
          "value": "lists"
        },
        {
          "path": "json_probes[8].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[3]",
          "key": "[3]",
          "value": "path"
        },
        {
          "path": "json_probes[8].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[4]",
          "key": "[4]",
          "value": "top_keys"
        },
        {
          "path": "json_probes[8].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[5]",
          "key": "[5]",
          "value": "type"
        },
        {
          "path": "json_probes[12].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys",
          "key": "data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys",
          "value": [
            "date_examples",
            "date_keys",
            "date_summary",
            "exists",
            "inferred",
            "json_valid",
            "numeric_examples",
            "numeric_keys",
            "path",
            "primary_list_key",
            "row_count",
            "sample_last",
            "top_keys",
            "top_level_arrays",
            "type"
          ]
        },
        {
          "path": "json_probes[12].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[0]",
          "key": "[0]",
          "value": "date_examples"
        },
        {
          "path": "json_probes[12].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[1]",
          "key": "[1]",
          "value": "date_keys"
        },
        {
          "path": "json_probes[12].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[2]",
          "key": "[2]",
          "value": "date_summary"
        },
        {
          "path": "json_probes[12].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[3]",
          "key": "[3]",
          "value": "exists"
        },
        {
          "path": "json_probes[12].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[4]",
          "key": "[4]",
          "value": "inferred"
        },
        {
          "path": "json_probes[12].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[5]",
          "key": "[5]",
          "value": "json_valid"
        },
        {
          "path": "json_probes[12].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[6]",
          "key": "[6]",
          "value": "numeric_examples"
        },
        {
          "path": "json_probes[12].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[7]",
          "key": "[7]",
          "value": "numeric_keys"
        },
        {
          "path": "json_probes[12].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[8]",
          "key": "[8]",
          "value": "path"
        },
        {
          "path": "json_probes[12].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[9]",
          "key": "[9]",
          "value": "primary_list_key"
        },
        {
          "path": "json_probes[12].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[10]",
          "key": "[10]",
          "value": "row_count"
        },
        {
          "path": "json_probes[12].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[11]",
          "key": "[11]",
          "value": "sample_last"
        },
        {
          "path": "json_probes[12].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[12]",
          "key": "[12]",
          "value": "top_keys"
        },
        {
          "path": "json_probes[12].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[13]",
          "key": "[13]",
          "value": "top_level_arrays"
        },
        {
          "path": "json_probes[12].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[14]",
          "key": "[14]",
          "value": "type"
        },
        {
          "path": "json_probes[16].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys",
          "key": "data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys",
          "value": [
            "exists",
            "json_valid",
            "lists",
            "path",
            "top_keys",
            "type"
          ]
        },
        {
          "path": "json_probes[16].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[0]",
          "key": "[0]",
          "value": "exists"
        },
        {
          "path": "json_probes[16].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[1]",
          "key": "[1]",
          "value": "json_valid"
        },
        {
          "path": "json_probes[16].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[2]",
          "key": "[2]",
          "value": "lists"
        },
        {
          "path": "json_probes[16].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[3]",
          "key": "[3]",
          "value": "path"
        },
        {
          "path": "json_probes[16].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[4]",
          "key": "[4]",
          "value": "top_keys"
        },
        {
          "path": "json_probes[16].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[5]",
          "key": "[5]",
          "value": "type"
        },
        {
          "path": "json_probes[16].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json_dict_keys",
          "key": "docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json_dict_keys",
          "value": [
            "exists",
            "json_valid",
            "lists",
            "path",
            "top_keys",
            "type"
          ]
        },
        {
          "path": "json_probes[16].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json_dict_keys[0]",
          "key": "[0]",
          "value": "exists"
        },
        {
          "path": "json_probes[16].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json_dict_keys[1]",
          "key": "[1]",
          "value": "json_valid"
        },
        {
          "path": "json_probes[16].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json_dict_keys[2]",
          "key": "[2]",
          "value": "lists"
        },
        {
          "path": "json_probes[16].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json_dict_keys[3]",
          "key": "[3]",
          "value": "path"
        },
        {
          "path": "json_probes[16].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json_dict_keys[4]",
          "key": "[4]",
          "value": "top_keys"
        },
        {
          "path": "json_probes[16].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json_dict_keys[5]",
          "key": "[5]",
          "value": "type"
        },
        {
          "path": "json_probes[16].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json_dict_keys",
          "key": "docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json_dict_keys",
          "value": [
            "exists",
            "json_valid",
            "lists",
            "path",
            "top_keys",
            "type"
          ]
        },
        {
          "path": "json_probes[16].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json_dict_keys[0]",
          "key": "[0]",
          "value": "exists"
        },
        {
          "path": "json_probes[16].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json_dict_keys[1]",
          "key": "[1]",
          "value": "json_valid"
        },
        {
          "path": "json_probes[16].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json_dict_keys[2]",
          "key": "[2]",
          "value": "lists"
        },
        {
          "path": "json_probes[16].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json_dict_keys[3]",
          "key": "[3]",
          "value": "path"
        },
        {
          "path": "json_probes[16].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json_dict_keys[4]",
          "key": "[4]",
          "value": "top_keys"
        },
        {
          "path": "json_probes[16].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json_dict_keys[5]",
          "key": "[5]",
          "value": "type"
        },
        {
          "path": "json_probes[17].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys",
          "key": "data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys",
          "value": [
            "exists",
            "json_valid",
            "lists",
            "path",
            "top_keys",
            "type"
          ]
        },
        {
          "path": "json_probes[17].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[0]",
          "key": "[0]",
          "value": "exists"
        },
        {
          "path": "json_probes[17].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[1]",
          "key": "[1]",
          "value": "json_valid"
        },
        {
          "path": "json_probes[17].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[2]",
          "key": "[2]",
          "value": "lists"
        },
        {
          "path": "json_probes[17].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[3]",
          "key": "[3]",
          "value": "path"
        },
        {
          "path": "json_probes[17].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[4]",
          "key": "[4]",
          "value": "top_keys"
        },
        {
          "path": "json_probes[17].nodes[0].summary.data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys[5]",
          "key": "[5]",
          "value": "type"
        },
        {
          "path": "json_probes[17].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json_dict_keys",
          "key": "docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json_dict_keys",
          "value": [
            "exists",
            "json_valid",
            "lists",
            "path",
            "top_keys",
            "type"
          ]
        },
        {
          "path": "json_probes[17].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json_dict_keys[0]",
          "key": "[0]",
          "value": "exists"
        },
        {
          "path": "json_probes[17].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json_dict_keys[1]",
          "key": "[1]",
          "value": "json_valid"
        },
        {
          "path": "json_probes[17].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json_dict_keys[2]",
          "key": "[2]",
          "value": "lists"
        },
        {
          "path": "json_probes[17].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json_dict_keys[3]",
          "key": "[3]",
          "value": "path"
        },
        {
          "path": "json_probes[17].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json_dict_keys[4]",
          "key": "[4]",
          "value": "top_keys"
        },
        {
          "path": "json_probes[17].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json_dict_keys[5]",
          "key": "[5]",
          "value": "type"
        },
        {
          "path": "json_probes[17].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json_dict_keys",
          "key": "docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json_dict_keys",
          "value": [
            "exists",
            "json_valid",
            "lists",
            "path",
            "top_keys",
            "type"
          ]
        },
        {
          "path": "json_probes[17].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json_dict_keys[0]",
          "key": "[0]",
          "value": "exists"
        },
        {
          "path": "json_probes[17].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json_dict_keys[1]",
          "key": "[1]",
          "value": "json_valid"
        },
        {
          "path": "json_probes[17].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json_dict_keys[2]",
          "key": "[2]",
          "value": "lists"
        },
        {
          "path": "json_probes[17].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json_dict_keys[3]",
          "key": "[3]",
          "value": "path"
        },
        {
          "path": "json_probes[17].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json_dict_keys[4]",
          "key": "[4]",
          "value": "top_keys"
        },
        {
          "path": "json_probes[17].nodes[0].summary.docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json_dict_keys[5]",
          "key": "[5]",
          "value": "type"
        },
        {
          "path": "json_probes[19].nodes[0].summary.market_entry_gate_dict_keys",
          "key": "market_entry_gate_dict_keys",
          "value": [
            "blocked_actions",
            "days",
            "enabled",
            "market_shock_rule",
            "risk_off_rule",
            "unaffected_actions",
            "variant"
          ]
        },
        {
          "path": "json_probes[19].nodes[0].summary.market_entry_gate_dict_keys[0]",
          "key": "[0]",
          "value": "blocked_actions"
        },
        {
          "path": "json_probes[19].nodes[0].summary.market_entry_gate_dict_keys[1]",
          "key": "[1]",
          "value": "days"
        },
        {
          "path": "json_probes[19].nodes[0].summary.market_entry_gate_dict_keys[2]",
          "key": "[2]",
          "value": "enabled"
        },
        {
          "path": "json_probes[19].nodes[0].summary.market_entry_gate_dict_keys[3]",
          "key": "[3]",
          "value": "market_shock_rule"
        },
        {
          "path": "json_probes[19].nodes[0].summary.market_entry_gate_dict_keys[4]",
          "key": "[4]",
          "value": "risk_off_rule"
        },
        {
          "path": "json_probes[19].nodes[0].summary.market_entry_gate_dict_keys[5]",
          "key": "[5]",
          "value": "unaffected_actions"
        },
        {
          "path": "json_probes[19].nodes[0].summary.market_entry_gate_dict_keys[6]",
          "key": "[6]",
          "value": "variant"
        },
        {
          "path": "json_probes[19].nodes[1].summary.market_entry_gate_dict_keys",
          "key": "market_entry_gate_dict_keys",
          "value": [
            "blocked_actions",
            "days",
            "enabled",
            "market_shock_rule",
            "risk_off_rule",
            "unaffected_actions",
            "variant"
          ]
        },
        {
          "path": "json_probes[19].nodes[1].summary.market_entry_gate_dict_keys[0]",
          "key": "[0]",
          "value": "blocked_actions"
        },
        {
          "path": "json_probes[19].nodes[1].summary.market_entry_gate_dict_keys[1]",
          "key": "[1]",
          "value": "days"
        },
        {
          "path": "json_probes[19].nodes[1].summary.market_entry_gate_dict_keys[2]",
          "key": "[2]",
          "value": "enabled"
        },
        {
          "path": "json_probes[19].nodes[1].summary.market_entry_gate_dict_keys[3]",
          "key": "[3]",
          "value": "market_shock_rule"
        },
        {
          "path": "json_probes[19].nodes[1].summary.market_entry_gate_dict_keys[4]",
          "key": "[4]",
          "value": "risk_off_rule"
        },
        {
          "path": "json_probes[19].nodes[1].summary.market_entry_gate_dict_keys[5]",
          "key": "[5]",
          "value": "unaffected_actions"
        },
        {
          "path": "json_probes[19].nodes[1].summary.market_entry_gate_dict_keys[6]",
          "key": "[6]",
          "value": "variant"
        },
        {
          "path": "json_probes[19].nodes[2].summary.market_entry_gate_dict_keys",
          "key": "market_entry_gate_dict_keys",
          "value": [
            "blocked_actions",
            "days",
            "enabled",
            "market_shock_rule",
            "risk_off_rule",
            "unaffected_actions",
            "variant"
          ]
        },
        {
          "path": "json_probes[19].nodes[2].summary.market_entry_gate_dict_keys[0]",
          "key": "[0]",
          "value": "blocked_actions"
        },
        {
          "path": "json_probes[19].nodes[2].summary.market_entry_gate_dict_keys[1]",
          "key": "[1]",
          "value": "days"
        },
        {
          "path": "json_probes[19].nodes[2].summary.market_entry_gate_dict_keys[2]",
          "key": "[2]",
          "value": "enabled"
        },
        {
          "path": "json_probes[19].nodes[2].summary.market_entry_gate_dict_keys[3]",
          "key": "[3]",
          "value": "market_shock_rule"
        },
        {
          "path": "json_probes[19].nodes[2].summary.market_entry_gate_dict_keys[4]",
          "key": "[4]",
          "value": "risk_off_rule"
        },
        {
          "path": "json_probes[19].nodes[2].summary.market_entry_gate_dict_keys[5]",
          "key": "[5]",
          "value": "unaffected_actions"
        },
        {
          "path": "json_probes[19].nodes[2].summary.market_entry_gate_dict_keys[6]",
          "key": "[6]",
          "value": "variant"
        },
        {
          "path": "json_probes[21].nodes[0].summary.market_entry_gate_dict_keys",
          "key": "market_entry_gate_dict_keys",
          "value": [
            "blocked_actions",
            "days",
            "enabled",
            "market_shock_rule",
            "risk_off_rule",
            "unaffected_actions",
            "variant"
          ]
        },
        {
          "path": "json_probes[21].nodes[0].summary.market_entry_gate_dict_keys[0]",
          "key": "[0]",
          "value": "blocked_actions"
        },
        {
          "path": "json_probes[21].nodes[0].summary.market_entry_gate_dict_keys[1]",
          "key": "[1]",
          "value": "days"
        },
        {
          "path": "json_probes[21].nodes[0].summary.market_entry_gate_dict_keys[2]",
          "key": "[2]",
          "value": "enabled"
        },
        {
          "path": "json_probes[21].nodes[0].summary.market_entry_gate_dict_keys[3]",
          "key": "[3]",
          "value": "market_shock_rule"
        },
        {
          "path": "json_probes[21].nodes[0].summary.market_entry_gate_dict_keys[4]",
          "key": "[4]",
          "value": "risk_off_rule"
        },
        {
          "path": "json_probes[21].nodes[0].summary.market_entry_gate_dict_keys[5]",
          "key": "[5]",
          "value": "unaffected_actions"
        },
        {
          "path": "json_probes[21].nodes[0].summary.market_entry_gate_dict_keys[6]",
          "key": "[6]",
          "value": "variant"
        },
        {
          "path": "json_probes[21].nodes[1].summary.market_entry_gate_dict_keys",
          "key": "market_entry_gate_dict_keys",
          "value": [
            "blocked_actions",
            "days",
            "enabled",
            "market_shock_rule",
            "risk_off_rule",
            "unaffected_actions",
            "variant"
          ]
        },
        {
          "path": "json_probes[21].nodes[1].summary.market_entry_gate_dict_keys[0]",
          "key": "[0]",
          "value": "blocked_actions"
        },
        {
          "path": "json_probes[21].nodes[1].summary.market_entry_gate_dict_keys[1]",
          "key": "[1]",
          "value": "days"
        },
        {
          "path": "json_probes[21].nodes[1].summary.market_entry_gate_dict_keys[2]",
          "key": "[2]",
          "value": "enabled"
        },
        {
          "path": "json_probes[21].nodes[1].summary.market_entry_gate_dict_keys[3]",
          "key": "[3]",
          "value": "market_shock_rule"
        },
        {
          "path": "json_probes[21].nodes[1].summary.market_entry_gate_dict_keys[4]",
          "key": "[4]",
          "value": "risk_off_rule"
        },
        {
          "path": "json_probes[21].nodes[1].summary.market_entry_gate_dict_keys[5]",
          "key": "[5]",
          "value": "unaffected_actions"
        },
        {
          "path": "json_probes[21].nodes[1].summary.market_entry_gate_dict_keys[6]",
          "key": "[6]",
          "value": "variant"
        },
        {
          "path": "json_probes[21].nodes[2].summary.market_entry_gate_dict_keys",
          "key": "market_entry_gate_dict_keys",
          "value": [
            "blocked_actions",
            "days",
            "enabled",
            "market_shock_rule",
            "risk_off_rule",
            "unaffected_actions",
            "variant"
          ]
        },
        {
          "path": "json_probes[21].nodes[2].summary.market_entry_gate_dict_keys[0]",
          "key": "[0]",
          "value": "blocked_actions"
        },
        {
          "path": "json_probes[21].nodes[2].summary.market_entry_gate_dict_keys[1]",
          "key": "[1]",
          "value": "days"
        },
        {
          "path": "json_probes[21].nodes[2].summary.market_entry_gate_dict_keys[2]",
          "key": "[2]",
          "value": "enabled"
        },
        {
          "path": "json_probes[21].nodes[2].summary.market_entry_gate_dict_keys[3]",
          "key": "[3]",
          "value": "market_shock_rule"
        },
        {
          "path": "json_probes[21].nodes[2].summary.market_entry_gate_dict_keys[4]",
          "key": "[4]",
          "value": "risk_off_rule"
        },
        {
          "path": "json_probes[21].nodes[2].summary.market_entry_gate_dict_keys[5]",
          "key": "[5]",
          "value": "unaffected_actions"
        },
        {
          "path": "json_probes[21].nodes[2].summary.market_entry_gate_dict_keys[6]",
          "key": "[6]",
          "value": "variant"
        }
      ],
      "e1r_hits": [
        {
          "path": "status",
          "key": "status",
          "value": "E1R_GENERATOR_PATH_TRACE_COMPLETE_NO_EXPORTS_WRITTEN"
        },
        {
          "path": "policy.e1r_canonical_written",
          "key": "e1r_canonical_written",
          "value": false
        },
        {
          "path": "recommended_next_action",
          "key": "recommended_next_action",
          "value": "Trace the generator candidate that calls compose_e1r_v0_2_variant and rerun it in dry-run/no-write mode to recover core_variant_result and daily equity."
        },
        {
          "path": "generator_candidates[0].path",
          "key": "path",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json"
        },
        {
          "path": "generator_candidates[0].matched_terms[6]",
          "key": "[6]",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "generator_candidates[0].matched_terms[7]",
          "key": "[7]",
          "value": "build_e1r_sidecar_sleeve"
        },
        {
          "path": "generator_candidates[0].matched_terms[9]",
          "key": "[9]",
          "value": "compose_e1r_v0_2_variant"
        },
        {
          "path": "generator_candidates[0].matched_terms[13]",
          "key": "[13]",
          "value": "e1r_v0_2"
        },
        {
          "path": "generator_candidates[0].matched_terms[14]",
          "key": "[14]",
          "value": "e1r_v0_2_backtest_equity_curve.json"
        },
        {
          "path": "generator_candidates[0].matched_terms[15]",
          "key": "[15]",
          "value": "e1r_v0_2_backtest_summary.json"
        },
        {
          "path": "generator_candidates[0].hits[4].matched[0]",
          "key": "[0]",
          "value": "e1r_v0_2"
        },
        {
          "path": "generator_candidates[0].hits[4].matched[1]",
          "key": "[1]",
          "value": "compose_e1r_v0_2_variant"
        },
        {
          "path": "generator_candidates[0].hits[4].context[2].text",
          "key": "text",
          "value": "          \"name\": \"compose_e1r_v0_2_variant\","
        },
        {
          "path": "generator_candidates[0].hits[10].matched[0]",
          "key": "[0]",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "generator_candidates[0].hits[10].context[2].text",
          "key": "text",
          "value": "            \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "path": "generator_candidates[0].hits[10].context[4].text",
          "key": "text",
          "value": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
        },
        {
          "path": "generator_candidates[0].hits[11].matched[0]",
          "key": "[0]",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "generator_candidates[0].hits[11].context[0].text",
          "key": "text",
          "value": "            \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "path": "generator_candidates[0].hits[11].context[2].text",
          "key": "text",
          "value": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
        },
        {
          "path": "generator_candidates[0].hits[27].matched[0]",
          "key": "[0]",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "generator_candidates[0].hits[27].context[2].text",
          "key": "text",
          "value": "            \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "path": "generator_candidates[0].hits[27].context[4].text",
          "key": "text",
          "value": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
        },
        {
          "path": "generator_candidates[0].hits[28].matched[0]",
          "key": "[0]",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "generator_candidates[0].hits[28].context[0].text",
          "key": "text",
          "value": "            \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "path": "generator_candidates[0].hits[28].context[2].text",
          "key": "text",
          "value": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
        },
        {
          "path": "generator_candidates[1].path",
          "key": "path",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json"
        },
        {
          "path": "generator_candidates[1].matched_terms[6]",
          "key": "[6]",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "generator_candidates[1].matched_terms[7]",
          "key": "[7]",
          "value": "build_e1r_sidecar_sleeve"
        },
        {
          "path": "generator_candidates[1].matched_terms[9]",
          "key": "[9]",
          "value": "compose_e1r_v0_2_variant"
        },
        {
          "path": "generator_candidates[1].matched_terms[13]",
          "key": "[13]",
          "value": "e1r_v0_2"
        },
        {
          "path": "generator_candidates[1].matched_terms[14]",
          "key": "[14]",
          "value": "e1r_v0_2_backtest_equity_curve.json"
        },
        {
          "path": "generator_candidates[1].matched_terms[15]",
          "key": "[15]",
          "value": "e1r_v0_2_backtest_summary.json"
        },
        {
          "path": "generator_candidates[1].hits[2].matched[0]",
          "key": "[0]",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "generator_candidates[1].hits[2].context[2].text",
          "key": "text",
          "value": "            \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "path": "generator_candidates[1].hits[2].context[4].text",
          "key": "text",
          "value": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
        },
        {
          "path": "generator_candidates[1].hits[3].matched[0]",
          "key": "[0]",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "generator_candidates[1].hits[3].context[0].text",
          "key": "text",
          "value": "            \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "path": "generator_candidates[1].hits[3].context[2].text",
          "key": "text",
          "value": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
        },
        {
          "path": "generator_candidates[1].hits[18].matched[0]",
          "key": "[0]",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "generator_candidates[1].hits[18].context[2].text",
          "key": "text",
          "value": "            \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "path": "generator_candidates[1].hits[18].context[4].text",
          "key": "text",
          "value": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
        },
        {
          "path": "generator_candidates[1].hits[19].matched[0]",
          "key": "[0]",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "generator_candidates[1].hits[19].context[0].text",
          "key": "text",
          "value": "            \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "path": "generator_candidates[1].hits[19].context[2].text",
          "key": "text",
          "value": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
        },
        {
          "path": "generator_candidates[1].hits[21].matched[0]",
          "key": "[0]",
          "value": "e1r_v0_2"
        },
        {
          "path": "generator_candidates[1].hits[21].context[0].text",
          "key": "text",
          "value": "            \"E1R_REGIME_AWARE_V0_1\""
        },
        {
          "path": "generator_candidates[1].hits[21].context[2].text",
          "key": "text",
          "value": "          \"text\": \"        \\\"e1r_v0_2_core_variant\\\": \\\"E1R_REGIME_AWARE_V0_1\\\",\""
        },
        {
          "path": "generator_candidates[1].hits[22].matched[0]",
          "key": "[0]",
          "value": "e1r_v0_2"
        },
        {
          "path": "generator_candidates[1].hits[22].context[2].text",
          "key": "text",
          "value": "          \"text\": \"        \\\"e1r_v0_2_sidecar_gross_exposure\\\": sidecar_result.get(\\\"config\\\", {}).get(\\\"gross_exposure\\\"),\""
        },
        {
          "path": "generator_candidates[2].path",
          "key": "path",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json"
        },
        {
          "path": "generator_candidates[2].matched_terms[6]",
          "key": "[6]",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "generator_candidates[2].matched_terms[7]",
          "key": "[7]",
          "value": "build_e1r_sidecar_sleeve"
        },
        {
          "path": "generator_candidates[2].matched_terms[9]",
          "key": "[9]",
          "value": "compose_e1r_v0_2_variant"
        },
        {
          "path": "generator_candidates[2].matched_terms[13]",
          "key": "[13]",
          "value": "e1r_v0_2"
        },
        {
          "path": "generator_candidates[2].matched_terms[14]",
          "key": "[14]",
          "value": "e1r_v0_2_backtest_summary.json"
        },
        {
          "path": "generator_candidates[2].hits[0].context[1].text",
          "key": "text",
          "value": "  \"e1r_frozen_targets\": {"
        },
        {
          "path": "generator_candidates[2].hits[1].context[0].text",
          "key": "text",
          "value": "  \"e1r_frozen_targets\": {"
        },
        {
          "path": "generator_candidates[2].hits[8].matched[0]",
          "key": "[0]",
          "value": "e1r_v0_2"
        },
        {
          "path": "generator_candidates[2].hits[8].context[2].text",
          "key": "text",
          "value": "    \"path\": \"exports/e1r_v0_2_sidecar_records_5y.json\","
        },
        {
          "path": "generator_candidates[2].hits[8].context[3].text",
          "key": "text",
          "value": "    \"artifact_type\": \"e1r_v0_2_regime_aware_sidecar_records_5y\","
        },
        {
          "path": "generator_candidates[2].hits[9].matched[0]",
          "key": "[0]",
          "value": "e1r_v0_2"
        },
        {
          "path": "generator_candidates[2].hits[9].context[1].text",
          "key": "text",
          "value": "    \"path\": \"exports/e1r_v0_2_sidecar_records_5y.json\","
        },
        {
          "path": "generator_candidates[2].hits[9].context[2].text",
          "key": "text",
          "value": "    \"artifact_type\": \"e1r_v0_2_regime_aware_sidecar_records_5y\","
        },
        {
          "path": "generator_candidates[2].hits[10].context[4].text",
          "key": "text",
          "value": "        \"E1R\","
        },
        {
          "path": "generator_candidates[2].hits[11].context[3].text",
          "key": "text",
          "value": "        \"E1R\","
        },
        {
          "path": "generator_candidates[2].hits[12].context[1].text",
          "key": "text",
          "value": "        \"compose_e1r\","
        },
        {
          "path": "generator_candidates[2].hits[13].context[4].text",
          "key": "text",
          "value": "        \"E1R\","
        },
        {
          "path": "generator_candidates[2].hits[14].context[3].text",
          "key": "text",
          "value": "        \"E1R\","
        },
        {
          "path": "generator_candidates[2].hits[15].context[1].text",
          "key": "text",
          "value": "        \"compose_e1r\","
        },
        {
          "path": "generator_candidates[2].hits[17].context[4].text",
          "key": "text",
          "value": "        \"E1R\","
        },
        {
          "path": "generator_candidates[2].hits[18].context[3].text",
          "key": "text",
          "value": "        \"E1R\","
        },
        {
          "path": "generator_candidates[2].hits[19].context[1].text",
          "key": "text",
          "value": "        \"compose_e1r\","
        },
        {
          "path": "generator_candidates[2].hits[21].context[4].text",
          "key": "text",
          "value": "        \"E1R\","
        },
        {
          "path": "generator_candidates[2].hits[22].context[3].text",
          "key": "text",
          "value": "        \"E1R\","
        },
        {
          "path": "generator_candidates[2].hits[23].context[1].text",
          "key": "text",
          "value": "        \"compose_e1r\","
        },
        {
          "path": "generator_candidates[2].hits[24].context[4].text",
          "key": "text",
          "value": "        \"E1R\","
        },
        {
          "path": "generator_candidates[2].hits[25].context[3].text",
          "key": "text",
          "value": "        \"E1R\","
        },
        {
          "path": "generator_candidates[2].hits[26].context[4].text",
          "key": "text",
          "value": "        \"E1R\","
        },
        {
          "path": "generator_candidates[2].hits[27].context[3].text",
          "key": "text",
          "value": "        \"E1R\","
        },
        {
          "path": "generator_candidates[2].hits[27].context[4].text",
          "key": "text",
          "value": "        \"compose_e1r\","
        },
        {
          "path": "generator_candidates[2].hits[28].context[0].text",
          "key": "text",
          "value": "        \"E1R\","
        },
        {
          "path": "generator_candidates[2].hits[28].context[1].text",
          "key": "text",
          "value": "        \"compose_e1r\","
        },
        {
          "path": "generator_candidates[2].hits[29].context[4].text",
          "key": "text",
          "value": "        \"E1R\","
        },
        {
          "path": "generator_candidates[3].path",
          "key": "path",
          "value": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json"
        },
        {
          "path": "generator_candidates[3].matched_terms[6]",
          "key": "[6]",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "generator_candidates[3].matched_terms[7]",
          "key": "[7]",
          "value": "compose_e1r_v0_2_variant"
        },
        {
          "path": "generator_candidates[3].matched_terms[11]",
          "key": "[11]",
          "value": "e1r_v0_2"
        },
        {
          "path": "generator_candidates[3].matched_terms[12]",
          "key": "[12]",
          "value": "e1r_v0_2_backtest_equity_curve.json"
        },
        {
          "path": "generator_candidates[3].matched_terms[13]",
          "key": "[13]",
          "value": "e1r_v0_2_backtest_summary.json"
        },
        {
          "path": "generator_candidates[3].hits[1].matched[0]",
          "key": "[0]",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "generator_candidates[3].hits[1].context[2].text",
          "key": "text",
          "value": "        \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "path": "generator_candidates[3].hits[1].context[3].text",
          "key": "text",
          "value": "        \"E1R v0.2\","
        },
        {
          "path": "generator_candidates[3].hits[3].matched[0]",
          "key": "[0]",
          "value": "e1r_v0_2"
        },
        {
          "path": "generator_candidates[3].hits[3].context[1].text",
          "key": "text",
          "value": "          \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json\","
        },
        {
          "path": "generator_candidates[3].hits[3].context[2].text",
          "key": "text",
          "value": "          \"list_path\": \"source_reports.scripts/run_e1r_v0_2_oos.py.defs\","
        },
        {
          "path": "generator_candidates[3].hits[4].matched[0]",
          "key": "[0]",
          "value": "e1r_v0_2"
        },
        {
          "path": "generator_candidates[3].hits[4].context[1].text",
          "key": "text",
          "value": "          \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json\","
        },
        {
          "path": "generator_candidates[3].hits[4].context[2].text",
          "key": "text",
          "value": "          \"list_path\": \"source_reports.scripts/run_e1r_v0_2_oos.py.term_hits.target\","
        },
        {
          "path": "generator_candidates[3].hits[5].matched[0]",
          "key": "[0]",
          "value": "e1r_v0_2"
        },
        {
          "path": "generator_candidates[3].hits[5].context[1].text",
          "key": "text",
          "value": "          \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json\","
        }
      ],
      "counts": {
        "return_hits": 886,
        "metric_hits": 38,
        "market_hits": 126,
        "e1r_hits": 10910
      },
      "score": 180
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0E_LITE_GENERATOR_DRY_RUN_REPORT.json",
      "sha256": "f9635400f1f948e8fa881626b41bac9dcb4304de4bcf14dbccdfc395bb5ed37f",
      "top_level": {
        "status": "E1R_GENERATOR_DRY_RUN_LITE_COMPLETE_OUTPUTS_RESTORED"
      },
      "return_hits": [
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].matched_metrics.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].matched_metrics.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756,
          "distance_to_target_116_74": 0.0035999134756110607
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.trades_last.max_gain_pct",
          "key": "max_gain_pct",
          "value": 112.55,
          "distance_to_target_116_74": 4.189999999999998
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.trades_last.max_gain_pct",
          "key": "max_gain_pct",
          "value": 112.55,
          "distance_to_target_116_74": 4.189999999999998
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.daily_like_nodes[0].summary.trades_last.max_gain_pct",
          "key": "max_gain_pct",
          "value": 112.55,
          "distance_to_target_116_74": 4.189999999999998
        }
      ],
      "metric_hits": [
        {
          "path": "run_report.returncode",
          "key": "returncode",
          "value": 0
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.metric_like_values.spx_return_pct",
          "key": "spx_return_pct",
          "value": 76.844174428316
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": 39.89942548515961
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.7957270568329264
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].matched_metrics.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].matched_metrics.spx_return_pct",
          "key": "spx_return_pct",
          "value": 76.844174428316
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].matched_metrics.alpha_pct",
          "key": "alpha_pct",
          "value": 39.89942548515961
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].matched_metrics.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].matched_metrics.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].matched_metrics.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.7957270568329264
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].target_diffs_abs.total_return_pct",
          "key": "total_return_pct",
          "value": 0.0
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].target_diffs_abs.spx_return_pct",
          "key": "spx_return_pct",
          "value": 0.0
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].target_diffs_abs.alpha_pct",
          "key": "alpha_pct",
          "value": 0.0
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].target_diffs_abs.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 0.0
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].target_diffs_abs.profit_factor",
          "key": "profit_factor",
          "value": 0.0
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].target_diffs_abs.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.0
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].summary.metric_like_values.spx_return_pct",
          "key": "spx_return_pct",
          "value": 76.844174428316
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].summary.metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": 39.89942548515961
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].summary.metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].summary.metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].summary.metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.7957270568329264
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].matched_metrics.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].matched_metrics.spx_return_pct",
          "key": "spx_return_pct",
          "value": 76.844174428316
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].matched_metrics.alpha_pct",
          "key": "alpha_pct",
          "value": 39.89942548515961
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].matched_metrics.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].matched_metrics.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].matched_metrics.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.7957270568329264
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].target_diffs_abs.total_return_pct",
          "key": "total_return_pct",
          "value": 0.0
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].target_diffs_abs.spx_return_pct",
          "key": "spx_return_pct",
          "value": 0.0
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].target_diffs_abs.alpha_pct",
          "key": "alpha_pct",
          "value": 0.0
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].target_diffs_abs.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 0.0
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].target_diffs_abs.profit_factor",
          "key": "profit_factor",
          "value": 0.0
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].target_diffs_abs.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.0
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].summary.metric_like_values.spx_return_pct",
          "key": "spx_return_pct",
          "value": 76.844174428316
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].summary.metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": 39.89942548515961
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].summary.metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].summary.metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].summary.metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.7957270568329264
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.metrics_dict_metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 65.71
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.metrics_dict_metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": -3.65
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.metrics_dict_metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 32.35
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.metrics_dict_metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.97
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.metrics_dict_metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.58
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.e1_metrics_dict_metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 7.52
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.e1_metrics_dict_metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 38.1
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.e1_metrics_dict_metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.25
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.e1_metrics_dict_metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.18
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.trades_first.return_pct",
          "key": "return_pct",
          "value": -4.73
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.trades_first.max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 9.2
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.trades_last.return_pct",
          "key": "return_pct",
          "value": 37.57
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.trades_last.max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 0
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.metrics_dict_metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 65.71
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.metrics_dict_metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": -3.65
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.metrics_dict_metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 32.35
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.metrics_dict_metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.97
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.metrics_dict_metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.58
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.e1_metrics_dict_metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 7.52
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.e1_metrics_dict_metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 38.1
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.e1_metrics_dict_metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.25
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.e1_metrics_dict_metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.18
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.trades_first.return_pct",
          "key": "return_pct",
          "value": -4.73
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.trades_first.max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 9.2
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.trades_last.return_pct",
          "key": "return_pct",
          "value": 37.57
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.trades_last.max_drawdown_in_trade",
          "key": "max_drawdown_in_trade",
          "value": 0
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[1].matched_metrics.total_return_pct",
          "key": "total_return_pct",
          "value": 65.71
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[1].matched_metrics.alpha_pct",
          "key": "alpha_pct",
          "value": -3.65
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[1].matched_metrics.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 32.35
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[1].matched_metrics.profit_factor",
          "key": "profit_factor",
          "value": 1.97
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[1].matched_metrics.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.58
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[1].target_diffs_abs.total_return_pct",
          "key": "total_return_pct",
          "value": 51.03359991347561
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[1].target_diffs_abs.alpha_pct",
          "key": "alpha_pct",
          "value": 43.54942548515961
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[1].target_diffs_abs.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 6.4451906371848935
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[1].target_diffs_abs.profit_factor",
          "key": "profit_factor",
          "value": 0.7780369044490651
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[1].target_diffs_abs.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.21572705683292648
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[1].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 65.71
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[1].summary.metric_like_values.spx_total_return_pct",
          "key": "spx_total_return_pct",
          "value": 69.36
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[1].summary.metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": -3.65
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[1].summary.metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 32.35
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[1].summary.metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.97
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[1].summary.metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.58
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[2].matched_metrics.total_return_pct",
          "key": "total_return_pct",
          "value": 7.52
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[2].matched_metrics.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 38.1
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[2].matched_metrics.profit_factor",
          "key": "profit_factor",
          "value": 1.25
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[2].matched_metrics.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.18
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[2].target_diffs_abs.total_return_pct",
          "key": "total_return_pct",
          "value": 109.22359991347561
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[2].target_diffs_abs.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 12.195190637184893
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[2].target_diffs_abs.profit_factor",
          "key": "profit_factor",
          "value": 0.058036904449065174
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[2].target_diffs_abs.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.6157270568329265
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[2].summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 7.52
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[2].summary.metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 38.1
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[2].summary.metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.25
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[2].summary.metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.18
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.daily_like_nodes[0].summary.metrics_dict_metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 65.71
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.daily_like_nodes[0].summary.metrics_dict_metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": -3.65
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.daily_like_nodes[0].summary.metrics_dict_metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 32.35
        }
      ],
      "market_hits": [
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.sidecar_active_by_regime_dict_keys",
          "key": "sidecar_active_by_regime_dict_keys",
          "value": [
            "SIDEWAYS"
          ]
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.sidecar_active_by_regime_dict_keys[0]",
          "key": "[0]",
          "value": "SIDEWAYS"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].summary.sidecar_active_by_regime_dict_keys",
          "key": "sidecar_active_by_regime_dict_keys",
          "value": [
            "SIDEWAYS"
          ]
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.nodes_sample[0].summary.sidecar_active_by_regime_dict_keys[0]",
          "key": "[0]",
          "value": "SIDEWAYS"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].summary.sidecar_active_by_regime_dict_keys",
          "key": "sidecar_active_by_regime_dict_keys",
          "value": [
            "SIDEWAYS"
          ]
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_nodes[0].summary.sidecar_active_by_regime_dict_keys[0]",
          "key": "[0]",
          "value": "SIDEWAYS"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.trades_first.entry_regime",
          "key": "entry_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.trades_first.exit_regime",
          "key": "exit_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.trades_first.dominant_regime",
          "key": "dominant_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.trades_first.regime_day_weights",
          "key": "regime_day_weights",
          "value": {
            "UPTREND": 25
          }
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.trades_first.regime_day_weights.UPTREND",
          "key": "UPTREND",
          "value": 25
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.trades_last.entry_regime",
          "key": "entry_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.trades_last.exit_regime",
          "key": "exit_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.trades_last.dominant_regime",
          "key": "dominant_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.trades_last.regime_day_weights",
          "key": "regime_day_weights",
          "value": {
            "UPTREND": 34
          }
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.top_summary.trades_last.regime_day_weights.UPTREND",
          "key": "UPTREND",
          "value": 34
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.trades_first.entry_regime",
          "key": "entry_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.trades_first.exit_regime",
          "key": "exit_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.trades_first.dominant_regime",
          "key": "dominant_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.trades_first.regime_day_weights",
          "key": "regime_day_weights",
          "value": {
            "UPTREND": 25
          }
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.trades_first.regime_day_weights.UPTREND",
          "key": "UPTREND",
          "value": 25
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.trades_last.entry_regime",
          "key": "entry_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.trades_last.exit_regime",
          "key": "exit_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.trades_last.dominant_regime",
          "key": "dominant_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.trades_last.regime_day_weights",
          "key": "regime_day_weights",
          "value": {
            "UPTREND": 34
          }
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.nodes_sample[0].summary.trades_last.regime_day_weights.UPTREND",
          "key": "UPTREND",
          "value": 34
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.daily_like_nodes[0].summary.trades_first.entry_regime",
          "key": "entry_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.daily_like_nodes[0].summary.trades_first.exit_regime",
          "key": "exit_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.daily_like_nodes[0].summary.trades_first.dominant_regime",
          "key": "dominant_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.daily_like_nodes[0].summary.trades_first.regime_day_weights",
          "key": "regime_day_weights",
          "value": {
            "UPTREND": 25
          }
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.daily_like_nodes[0].summary.trades_first.regime_day_weights.UPTREND",
          "key": "UPTREND",
          "value": 25
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.daily_like_nodes[0].summary.trades_last.entry_regime",
          "key": "entry_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.daily_like_nodes[0].summary.trades_last.exit_regime",
          "key": "exit_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.daily_like_nodes[0].summary.trades_last.dominant_regime",
          "key": "dominant_regime",
          "value": "UPTREND"
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.daily_like_nodes[0].summary.trades_last.regime_day_weights",
          "key": "regime_day_weights",
          "value": {
            "UPTREND": 34
          }
        },
        {
          "path": "generated_inspection.data/research/e1r/e1r_formal_backtest_v0_1.json.daily_like_nodes[0].summary.trades_last.regime_day_weights.UPTREND",
          "key": "UPTREND",
          "value": 34
        }
      ],
      "e1r_hits": [
        {
          "path": "status",
          "key": "status",
          "value": "E1R_GENERATOR_DRY_RUN_LITE_COMPLETE_OUTPUTS_RESTORED"
        },
        {
          "path": "policy.e1r_canonical_written",
          "key": "e1r_canonical_written",
          "value": false
        },
        {
          "path": "selected_candidate.matched_terms[3]",
          "key": "[3]",
          "value": "e1r_v0_2"
        },
        {
          "path": "selected_candidate.matched_terms[4]",
          "key": "[4]",
          "value": "e1r_v0_2_backtest_equity_curve.json"
        },
        {
          "path": "selected_candidate.matched_terms[5]",
          "key": "[5]",
          "value": "e1r_v0_2_backtest_summary.json"
        },
        {
          "path": "selected_candidate.hits[6].context[1].text",
          "key": "text",
          "value": "        ROOT / \"data/research/e1r/e1r_formal_backtest_v0_1.json\","
        },
        {
          "path": "selected_candidate.hits[6].context[3].text",
          "key": "text",
          "value": "        ROOT / \"exports/e1r_v0_2_backtest_summary.json\","
        },
        {
          "path": "selected_candidate.hits[6].context[4].text",
          "key": "text",
          "value": "        ROOT / \"exports/e1r_v0_2_backtest_equity_curve.json\","
        },
        {
          "path": "selected_candidate.hits[7].matched[0]",
          "key": "[0]",
          "value": "e1r_v0_2_backtest_summary.json"
        },
        {
          "path": "selected_candidate.hits[7].matched[1]",
          "key": "[1]",
          "value": "e1r_v0_2"
        },
        {
          "path": "selected_candidate.hits[7].context[0].text",
          "key": "text",
          "value": "        ROOT / \"data/research/e1r/e1r_formal_backtest_v0_1.json\","
        },
        {
          "path": "selected_candidate.hits[7].context[2].text",
          "key": "text",
          "value": "        ROOT / \"exports/e1r_v0_2_backtest_summary.json\","
        },
        {
          "path": "selected_candidate.hits[7].context[3].text",
          "key": "text",
          "value": "        ROOT / \"exports/e1r_v0_2_backtest_equity_curve.json\","
        },
        {
          "path": "selected_candidate.hits[7].context[4].text",
          "key": "text",
          "value": "        ROOT / \"exports/oos_e1r_v0_2_equity_curve.json\","
        },
        {
          "path": "selected_candidate.hits[8].matched[0]",
          "key": "[0]",
          "value": "e1r_v0_2_backtest_equity_curve.json"
        },
        {
          "path": "selected_candidate.hits[8].matched[1]",
          "key": "[1]",
          "value": "e1r_v0_2"
        },
        {
          "path": "selected_candidate.hits[8].context[1].text",
          "key": "text",
          "value": "        ROOT / \"exports/e1r_v0_2_backtest_summary.json\","
        },
        {
          "path": "selected_candidate.hits[8].context[2].text",
          "key": "text",
          "value": "        ROOT / \"exports/e1r_v0_2_backtest_equity_curve.json\","
        },
        {
          "path": "selected_candidate.hits[8].context[3].text",
          "key": "text",
          "value": "        ROOT / \"exports/oos_e1r_v0_2_equity_curve.json\","
        },
        {
          "path": "selected_candidate.hits[9].matched[0]",
          "key": "[0]",
          "value": "e1r_v0_2"
        },
        {
          "path": "selected_candidate.hits[9].context[0].text",
          "key": "text",
          "value": "        ROOT / \"exports/e1r_v0_2_backtest_summary.json\","
        },
        {
          "path": "selected_candidate.hits[9].context[1].text",
          "key": "text",
          "value": "        ROOT / \"exports/e1r_v0_2_backtest_equity_curve.json\","
        },
        {
          "path": "selected_candidate.hits[9].context[2].text",
          "key": "text",
          "value": "        ROOT / \"exports/oos_e1r_v0_2_equity_curve.json\","
        },
        {
          "path": "selected_candidate.hits[10].context[0].text",
          "key": "text",
          "value": "        ROOT / \"exports/e1r_v0_2_backtest_equity_curve.json\","
        },
        {
          "path": "selected_candidate.hits[10].context[1].text",
          "key": "text",
          "value": "        ROOT / \"exports/oos_e1r_v0_2_equity_curve.json\","
        },
        {
          "path": "selected_candidate.hits[12].context[4].text",
          "key": "text",
          "value": "    to generate E1R 5Y interval records:"
        },
        {
          "path": "selected_candidate.hits[13].context[1].text",
          "key": "text",
          "value": "    to generate E1R 5Y interval records:"
        },
        {
          "path": "selected_candidate.hits[14].context[0].text",
          "key": "text",
          "value": "    to generate E1R 5Y interval records:"
        },
        {
          "path": "selected_candidate.hits[15].context[4].text",
          "key": "text",
          "value": "    from src.engine import e1r_composer as composer  # type: ignore"
        },
        {
          "path": "selected_candidate.hits[23].context[4].text",
          "key": "text",
          "value": "    e1r_diag = read_json(ROOT / \"exports/e1r_v0_2_backtest_equity_curve.json\", default={})"
        },
        {
          "path": "selected_candidate.hits[24].matched[0]",
          "key": "[0]",
          "value": "e1r_v0_2_backtest_equity_curve.json"
        },
        {
          "path": "selected_candidate.hits[24].matched[1]",
          "key": "[1]",
          "value": "e1r_v0_2"
        },
        {
          "path": "selected_candidate.hits[24].context[2].text",
          "key": "text",
          "value": "    e1r_diag = read_json(ROOT / \"exports/e1r_v0_2_backtest_equity_curve.json\", default={})"
        },
        {
          "path": "selected_candidate.hits[24].context[3].text",
          "key": "text",
          "value": "    if isinstance(e1r_diag, dict):"
        },
        {
          "path": "selected_candidate.hits[24].context[4].text",
          "key": "text",
          "value": "        append_if_list(\"core_sources\", \"exports/e1r_v0_2_backtest_equity_curve.json.rows\", e1r_diag.get(\"rows\"))"
        },
        {
          "path": "selected_candidate.hits[25].matched[0]",
          "key": "[0]",
          "value": "e1r_v0_2_backtest_equity_curve.json"
        },
        {
          "path": "selected_candidate.hits[25].matched[1]",
          "key": "[1]",
          "value": "e1r_v0_2"
        },
        {
          "path": "selected_candidate.hits[25].context[0].text",
          "key": "text",
          "value": "    e1r_diag = read_json(ROOT / \"exports/e1r_v0_2_backtest_equity_curve.json\", default={})"
        },
        {
          "path": "selected_candidate.hits[25].context[1].text",
          "key": "text",
          "value": "    if isinstance(e1r_diag, dict):"
        },
        {
          "path": "selected_candidate.hits[25].context[2].text",
          "key": "text",
          "value": "        append_if_list(\"core_sources\", \"exports/e1r_v0_2_backtest_equity_curve.json.rows\", e1r_diag.get(\"rows\"))"
        },
        {
          "path": "selected_candidate.hits[25].context[3].text",
          "key": "text",
          "value": "        append_if_list(\"core_sources\", \"exports/e1r_v0_2_backtest_equity_curve.json.equity_curve\", e1r_diag.get(\"equity_curve\"))"
        },
        {
          "path": "selected_candidate.hits[26].matched[0]",
          "key": "[0]",
          "value": "e1r_v0_2_backtest_equity_curve.json"
        },
        {
          "path": "selected_candidate.hits[26].matched[1]",
          "key": "[1]",
          "value": "e1r_v0_2"
        },
        {
          "path": "selected_candidate.hits[26].context[0].text",
          "key": "text",
          "value": "    if isinstance(e1r_diag, dict):"
        },
        {
          "path": "selected_candidate.hits[26].context[1].text",
          "key": "text",
          "value": "        append_if_list(\"core_sources\", \"exports/e1r_v0_2_backtest_equity_curve.json.rows\", e1r_diag.get(\"rows\"))"
        },
        {
          "path": "selected_candidate.hits[26].context[2].text",
          "key": "text",
          "value": "        append_if_list(\"core_sources\", \"exports/e1r_v0_2_backtest_equity_curve.json.equity_curve\", e1r_diag.get(\"equity_curve\"))"
        },
        {
          "path": "selected_candidate.hits[26].context[4].text",
          "key": "text",
          "value": "    sidecar = read_json(ROOT / \"exports/oos_e1r_v0_2_sidecar.json\", default={})"
        },
        {
          "path": "selected_candidate.hits[27].matched[0]",
          "key": "[0]",
          "value": "e1r_v0_2"
        },
        {
          "path": "selected_candidate.hits[27].context[0].text",
          "key": "text",
          "value": "        append_if_list(\"core_sources\", \"exports/e1r_v0_2_backtest_equity_curve.json.equity_curve\", e1r_diag.get(\"equity_curve\"))"
        },
        {
          "path": "selected_candidate.hits[27].context[2].text",
          "key": "text",
          "value": "    sidecar = read_json(ROOT / \"exports/oos_e1r_v0_2_sidecar.json\", default={})"
        },
        {
          "path": "selected_candidate.hits[28].matched[0]",
          "key": "[0]",
          "value": "e1r_v0_2"
        },
        {
          "path": "selected_candidate.hits[28].context[2].text",
          "key": "text",
          "value": "            append_if_list(\"sidecar_sources\", f\"exports/oos_e1r_v0_2_sidecar.json.{k}\", v)"
        },
        {
          "path": "selected_candidate.hits[28].context[4].text",
          "key": "text",
          "value": "        append_if_list(\"sidecar_sources\", \"exports/oos_e1r_v0_2_sidecar.json.root\", sidecar)"
        },
        {
          "path": "selected_candidate.hits[29].matched[0]",
          "key": "[0]",
          "value": "e1r_v0_2"
        },
        {
          "path": "selected_candidate.hits[29].context[0].text",
          "key": "text",
          "value": "            append_if_list(\"sidecar_sources\", f\"exports/oos_e1r_v0_2_sidecar.json.{k}\", v)"
        },
        {
          "path": "selected_candidate.hits[29].context[2].text",
          "key": "text",
          "value": "        append_if_list(\"sidecar_sources\", \"exports/oos_e1r_v0_2_sidecar.json.root\", sidecar)"
        },
        {
          "path": "run_report.stdout_tail",
          "key": "stdout_tail",
          "value": "       \"regime_day_weights\",\n              \"return_pct\",\n              \"size_units_at_exit\",\n              \"symbol\",\n              \"take_profit_exec_date\",\n              \"take_profit_triggered\"\n            ]\n          }\n        },\n        \"metrics\": {\n          \"variant_id\": \"E1R_REGIME_AWARE_V0_1\"\n        }\n      },\n      {\n        \"path\": \"exports/portfolio_backtest.json\",\n        \"exists\": true,\n        \"json_valid\": true,\n        \"type\": \"dict\",\n        \"top_keys\": [\n          \"alpha_pct\",\n          \"avg_execution_drag_pct\",\n          \"avg_holding_days\",\n          \"avg_loser_pct\",\n          \"avg_winner_pct\",\n          \"cagr_pct\",\n          \"comparison\",\n          \"daily_records\",\n          \"entry_top_n\",\n          \"executed_exit_reason_distribution\",\n          \"executed_reduce_reason_distribution\",\n          \"execution_model\",\n          \"exposure_pct\",\n          \"final_equity\",\n          \"generated_at\",\n          \"generated_at_display\",\n          \"initial_capital\",\n          \"invalid_trades\",\n          \"invalid_trades_count\",\n          \"layer\",\n          \"market_entry_gate\",\n          \"max_drawdown_pct\",\n          \"name\",\n          \"number_of_trades\",\n          \"p0_passed\",\n   ...<truncated>"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json",
          "key": "exports/e1r_v0_2_backtest_summary.json",
          "value": "{\"path\": \"exports/e1r_v0_2_backtest_summary.json\", \"exists_after_run\": true, \"size_after_run\": 941, \"hash_after_run\": \"449a8ace55ce2335d174e17e2532d8793a3a9b99c021a935f8d7f2e531092114\", \"top_summary\": {\"type\": \"dict\", \"len\": 20, \"keys\": [\"alpha_pct\", \"artifact_type\", \"composition_exists\", \"frozen_artifact\", \"max_drawdown_pct\", \"profit_factor\", \"regeneration_note\", \"regime_aware_logic\", \"research_status\", \"row_count\", \"sharpe_ratio\", \"sidecar_active_by_regime\", \"sidecar_active_by_subclass\", \"sidecar_active_days\", \"source_file\", \"source_json_path\", \"spx_return_pct\", \"strategy_id\", \"total_return_pct\", \"variant\"], \"metric_like_values\": {\"strategy_id\": \"E1R_REGIME_AWARE_V0_2\", \"total_return_pct\": 116.7435999134756, \"spx_return_pct\": 76.844174428316, \"alpha_pct\": 39.89942548515961, \"max_drawdown_pct\": 25.904809362815108, \"profit_factor\": 1.1919630955509348, \"sharpe_ratio\": 0.7957270568329264}, \"sidecar_active_by_regime_dict_keys\": [\"SIDEWAYS\"], \"sidecar_active_by_subclass_dict_keys\": [\"MA_CONFLICT\"]}, \"node_count\": 1, \"exact_metric_node_count\": 1, \"daily_like_node_count\": 0, \"core_variant_node_count\": 0, \"sidecar_node_count\": 0, \"nodes_sample\": [{\"path\": \"$\", \"matched_keys\": [], \"matched...<truncated>"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.path",
          "key": "path",
          "value": "exports/e1r_v0_2_backtest_summary.json"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exists_after_run",
          "key": "exists_after_run",
          "value": true
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.size_after_run",
          "key": "size_after_run",
          "value": 941
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.hash_after_run",
          "key": "hash_after_run",
          "value": "449a8ace55ce2335d174e17e2532d8793a3a9b99c021a935f8d7f2e531092114"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary",
          "key": "top_summary",
          "value": {
            "type": "dict",
            "len": 20,
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
            },
            "sidecar_active_by_regime_dict_keys": [
              "SIDEWAYS"
            ],
            "sidecar_active_by_subclass_dict_keys": [
              "MA_CONFLICT"
            ]
          }
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.type",
          "key": "type",
          "value": "dict"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.len",
          "key": "len",
          "value": 20
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys",
          "key": "keys",
          "value": [
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
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[0]",
          "key": "[0]",
          "value": "alpha_pct"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[1]",
          "key": "[1]",
          "value": "artifact_type"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[2]",
          "key": "[2]",
          "value": "composition_exists"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[3]",
          "key": "[3]",
          "value": "frozen_artifact"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[4]",
          "key": "[4]",
          "value": "max_drawdown_pct"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[5]",
          "key": "[5]",
          "value": "profit_factor"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[6]",
          "key": "[6]",
          "value": "regeneration_note"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[7]",
          "key": "[7]",
          "value": "regime_aware_logic"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[8]",
          "key": "[8]",
          "value": "research_status"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[9]",
          "key": "[9]",
          "value": "row_count"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[10]",
          "key": "[10]",
          "value": "sharpe_ratio"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[11]",
          "key": "[11]",
          "value": "sidecar_active_by_regime"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[12]",
          "key": "[12]",
          "value": "sidecar_active_by_subclass"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[13]",
          "key": "[13]",
          "value": "sidecar_active_days"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[14]",
          "key": "[14]",
          "value": "source_file"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[15]",
          "key": "[15]",
          "value": "source_json_path"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[16]",
          "key": "[16]",
          "value": "spx_return_pct"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[17]",
          "key": "[17]",
          "value": "strategy_id"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[18]",
          "key": "[18]",
          "value": "total_return_pct"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.keys[19]",
          "key": "[19]",
          "value": "variant"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.metric_like_values",
          "key": "metric_like_values",
          "value": {
            "strategy_id": "E1R_REGIME_AWARE_V0_2",
            "total_return_pct": 116.7435999134756,
            "spx_return_pct": 76.844174428316,
            "alpha_pct": 39.89942548515961,
            "max_drawdown_pct": 25.904809362815108,
            "profit_factor": 1.1919630955509348,
            "sharpe_ratio": 0.7957270568329264
          }
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.metric_like_values.strategy_id",
          "key": "strategy_id",
          "value": "E1R_REGIME_AWARE_V0_2"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.metric_like_values.total_return_pct",
          "key": "total_return_pct",
          "value": 116.7435999134756
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.metric_like_values.spx_return_pct",
          "key": "spx_return_pct",
          "value": 76.844174428316
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.metric_like_values.alpha_pct",
          "key": "alpha_pct",
          "value": 39.89942548515961
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.metric_like_values.max_drawdown_pct",
          "key": "max_drawdown_pct",
          "value": 25.904809362815108
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.metric_like_values.profit_factor",
          "key": "profit_factor",
          "value": 1.1919630955509348
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.metric_like_values.sharpe_ratio",
          "key": "sharpe_ratio",
          "value": 0.7957270568329264
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.sidecar_active_by_regime_dict_keys",
          "key": "sidecar_active_by_regime_dict_keys",
          "value": [
            "SIDEWAYS"
          ]
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.sidecar_active_by_regime_dict_keys[0]",
          "key": "[0]",
          "value": "SIDEWAYS"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.sidecar_active_by_subclass_dict_keys",
          "key": "sidecar_active_by_subclass_dict_keys",
          "value": [
            "MA_CONFLICT"
          ]
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.top_summary.sidecar_active_by_subclass_dict_keys[0]",
          "key": "[0]",
          "value": "MA_CONFLICT"
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.node_count",
          "key": "node_count",
          "value": 1
        },
        {
          "path": "generated_inspection.exports/e1r_v0_2_backtest_summary.json.exact_metric_node_count",
          "key": "exact_metric_node_count",
          "value": 1
        }
      ],
      "counts": {
        "return_hits": 8,
        "metric_hits": 110,
        "market_hits": 36,
        "e1r_hits": 1020
      },
      "score": 180
    }
  ],
  "top_text": [
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md",
      "sha256": "13f9dffb0e11fb9247084b14e7c6da290e3c735d211f527bea51fe8311bf61e4",
      "score": 120,
      "hits": [
        {
          "line": 1,
          "text": "# Stage 3.8E-2F-2C-4C-10F-4B-0B E1R Core Variant Source Recovery"
        },
        {
          "line": 7,
          "text": "- Status: `E1R_CORE_VARIANT_SOURCE_RECOVERY_COMPLETE_NO_EXPORTS_WRITTEN`"
        },
        {
          "line": 21,
          "text": "  \"conclusion\": \"E1R_FROZEN_METRIC_ARTIFACT_FOUND_CORE_SOURCE_CANDIDATES_PRESENT\","
        },
        {
          "line": 33,
          "text": "      \"total_return_pct\": 0.0,"
        },
        {
          "line": 41,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 42,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 43,
          "text": "        \"value\": 116.7435999134756,"
        },
        {
          "line": 44,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 73,
          "text": "      \"path\": \"$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics\","
        },
        {
          "line": 82,
          "text": "        \"total_return_pct\","
        },
        {
          "line": 86,
          "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 87,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 95,
          "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json\""
        },
        {
          "line": 100,
          "text": "      \"total_return_pct\": 0.0,"
        },
        {
          "line": 108,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 109,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 110,
          "text": "        \"value\": 116.7435999134756,"
        },
        {
          "line": 111,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 161,
          "text": "        \"total_return_pct\","
        },
        {
          "line": 165,
          "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 166,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 174,
          "text": "    \"file\": \"exports/e1r_v0_2_backtest_summary.json\""
        },
        {
          "line": 179,
          "text": "      \"total_return_pct\": 0.0,"
        },
        {
          "line": 187,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 188,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 189,
          "text": "        \"value\": 116.7435999134756,"
        },
        {
          "line": 190,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 219,
          "text": "      \"path\": \"$.export_reports.e1r_backtest_summary.e1r_objects[0].summary_fields\","
        },
        {
          "line": 227,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 230,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 238,
          "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json\""
        },
        {
          "line": 243,
          "text": "      \"total_return_pct\": 0.0,"
        },
        {
          "line": 251,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 252,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 253,
          "text": "        \"value\": 116.7435999134756,"
        },
        {
          "line": 254,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 291,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 294,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 302,
          "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C5_EXPORT_WRAPPER_SMOKE_REPORT.json\""
        },
        {
          "line": 307,
          "text": "      \"total_return_pct\": 0.0,"
        },
        {
          "line": 315,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 316,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 317,
          "text": "        \"value\": 116.7435999134756,"
        },
        {
          "line": 318,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 347,
          "text": "      \"path\": \"$.json_file_reports.docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json.lists[11].first_sample.summary_fields\","
        },
        {
          "line": 355,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 358,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 366,
          "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\""
        },
        {
          "line": 371,
          "text": "      \"total_return_pct\": 0.0,"
        },
        {
          "line": 379,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 380,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 381,
          "text": "        \"value\": 116.7435999134756,"
        },
        {
          "line": 382,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 411,
          "text": "      \"path\": \"$.json_file_reports.docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json.lists[11].last_sample.summary_fields\","
        },
        {
          "line": 419,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 422,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 430,
          "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\""
        },
        {
          "line": 435,
          "text": "      \"total_return_pct\": 0.0,"
        },
        {
          "line": 443,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 444,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 445,
          "text": "        \"value\": 116.7435999134756,"
        },
        {
          "line": 446,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 483,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 486,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 494,
          "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json\""
        },
        {
          "line": 499,
          "text": "      \"total_return_pct\": 0.0,"
        },
        {
          "line": 507,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 508,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 509,
          "text": "        \"value\": 116.7435999134756,"
        },
        {
          "line": 510,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 547,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 550,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 558,
          "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json\""
        },
        {
          "line": 563,
          "text": "      \"total_return_pct\": 0.0,"
        },
        {
          "line": 570,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 571,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 572,
          "text": "        \"value\": 116.7435999134756,"
        },
        {
          "line": 573,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 597,
          "text": "      \"path\": \"$.specific_files.exports/e1r_v0_2_backtest_summary.json.top_level_metrics\","
        },
        {
          "line": 605,
          "text": "        \"total_return_pct\","
        },
        {
          "line": 609,
          "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 610,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 617,
          "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json\""
        },
        {
          "line": 622,
          "text": "      \"total_return_pct\": 0.0,"
        },
        {
          "line": 629,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 630,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 631,
          "text": "        \"value\": 116.7435999134756,"
        },
        {
          "line": 632,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 656,
          "text": "      \"path\": \"$.json_summaries.exports/e1r_v0_2_backtest_summary.json\","
        },
        {
          "line": 667,
          "text": "        \"total_return_pct\","
        },
        {
          "line": 672,
          "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 673,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 680,
          "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json\""
        },
        {
          "line": 685,
          "text": "      \"total_return_pct\": 0.0,"
        },
        {
          "line": 691,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 692,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 693,
          "text": "        \"value\": 116.7435999134756,"
        },
        {
          "line": 694,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 719,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 722,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 728,
          "text": "    \"file\": \"docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json\""
        },
        {
          "line": 733,
          "text": "      \"total_return_pct\": 0.0,"
        },
        {
          "line": 739,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 740,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 741,
          "text": "        \"value\": 116.7435999134756,"
        },
        {
          "line": 742,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 767,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 770,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 776,
          "text": "    \"file\": \"docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json\""
        },
        {
          "line": 781,
          "text": "      \"total_return_pct\": 0.0,"
        },
        {
          "line": 787,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 788,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 789,
          "text": "        \"value\": 116.7435999134756,"
        },
        {
          "line": 790,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 809,
          "text": "      \"path\": \"$.json_file_reports.docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json.lists[18].first_sample.forward_fields\","
        },
        {
          "line": 815,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 818,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 824,
          "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\""
        },
        {
          "line": 829,
          "text": "      \"total_return_pct\": 0.0,"
        },
        {
          "line": 835,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 836,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 837,
          "text": "        \"value\": 116.7435999134756,"
        },
        {
          "line": 838,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 857,
          "text": "      \"path\": \"$.json_file_reports.docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json.lists[18].first_sample.numeric_forward_fields\","
        },
        {
          "line": 863,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 866,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 872,
          "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\""
        },
        {
          "line": 877,
          "text": "      \"total_return_pct\": 0.0,"
        },
        {
          "line": 883,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 884,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 885,
          "text": "        \"value\": 116.7435999134756,"
        },
        {
          "line": 886,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 905,
          "text": "      \"path\": \"$.json_file_reports.docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json.lists[18].last_sample.forward_fields\","
        },
        {
          "line": 911,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 914,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 920,
          "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\""
        },
        {
          "line": 925,
          "text": "      \"total_return_pct\": 0.0,"
        },
        {
          "line": 931,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 932,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 933,
          "text": "        \"value\": 116.7435999134756,"
        },
        {
          "line": 934,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 953,
          "text": "      \"path\": \"$.json_file_reports.docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json.lists[18].last_sample.numeric_forward_fields\","
        },
        {
          "line": 959,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 962,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 968,
          "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\""
        },
        {
          "line": 973,
          "text": "      \"total_return_pct\": 0.0,"
        },
        {
          "line": 978,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 979,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 980,
          "text": "        \"value\": 116.7435999134756,"
        },
        {
          "line": 981,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 995,
          "text": "      \"path\": \"$.json_reports.exports/e1r_v0_2_backtest_summary.json.field_presence.performance_like\","
        },
        {
          "line": 1000,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 1003,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 1008,
          "text": "    \"file\": \"docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json\""
        },
        {
          "line": 1013,
          "text": "      \"total_return_pct\": 109.22359991347561,"
        },
        {
          "line": 1020,
          "text": "      \"total_return_pct\": {"
        },
        {
          "line": 1021,
          "text": "        \"key\": \"total_return_pct\","
        },
        {
          "line": 1023,
          "text": "        \"target\": 116.7435999134756"
        },
        {
          "line": 1089,
          "text": "        \"spx_total_return_pct\","
        },
        {
          "line": 1093,
          "text": "        \"total_return_pct\","
        }
      ],
      "counts": {
        "hits": 160
      }
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0E_LITE_GENERATOR_DRY_RUN_REPORT.md",
      "sha256": "ab937a62a7d810f6230c5d9fe9f56558343891e25b26e753eaa7d5489352a6fa",
      "score": 120,
      "hits": [
        {
          "line": 1,
          "text": "# Stage 3.8E-2F-2C-4C-10F-4B-0E-lite E1R Generator Dry-run Report"
        },
        {
          "line": 7,
          "text": "- Status: `E1R_GENERATOR_DRY_RUN_LITE_COMPLETE_OUTPUTS_RESTORED`"
        },
        {
          "line": 10,
          "text": "- E1R canonical written: `False`"
        },
        {
          "line": 23,
          "text": "    \"e1r_v0_2\","
        },
        {
          "line": 24,
          "text": "    \"e1r_v0_2_backtest_equity_curve.json\","
        },
        {
          "line": 25,
          "text": "    \"e1r_v0_2_backtest_summary.json\","
        },
        {
          "line": 213,
          "text": "          \"text\": \"        ROOT / \\\"data/research/e1r/e1r_formal_backtest_v0_1.json\\\",\""
        },
        {
          "line": 221,
          "text": "          \"text\": \"        ROOT / \\\"exports/e1r_v0_2_backtest_summary.json\\\",\""
        },
        {
          "line": 225,
          "text": "          \"text\": \"        ROOT / \\\"exports/e1r_v0_2_backtest_equity_curve.json\\\",\""
        },
        {
          "line": 232,
          "text": "        \"e1r_v0_2_backtest_summary.json\","
        },
        {
          "line": 233,
          "text": "        \"e1r_v0_2\","
        },
        {
          "line": 239,
          "text": "          \"text\": \"        ROOT / \\\"data/research/e1r/e1r_formal_backtest_v0_1.json\\\",\""
        },
        {
          "line": 247,
          "text": "          \"text\": \"        ROOT / \\\"exports/e1r_v0_2_backtest_summary.json\\\",\""
        },
        {
          "line": 251,
          "text": "          \"text\": \"        ROOT / \\\"exports/e1r_v0_2_backtest_equity_curve.json\\\",\""
        },
        {
          "line": 255,
          "text": "          \"text\": \"        ROOT / \\\"exports/oos_e1r_v0_2_equity_curve.json\\\",\""
        },
        {
          "line": 262,
          "text": "        \"e1r_v0_2_backtest_equity_curve.json\","
        },
        {
          "line": 263,
          "text": "        \"e1r_v0_2\","
        },
        {
          "line": 274,
          "text": "          \"text\": \"        ROOT / \\\"exports/e1r_v0_2_backtest_summary.json\\\",\""
        },
        {
          "line": 278,
          "text": "          \"text\": \"        ROOT / \\\"exports/e1r_v0_2_backtest_equity_curve.json\\\",\""
        },
        {
          "line": 282,
          "text": "          \"text\": \"        ROOT / \\\"exports/oos_e1r_v0_2_equity_curve.json\\\",\""
        },
        {
          "line": 293,
          "text": "        \"e1r_v0_2\","
        },
        {
          "line": 300,
          "text": "          \"text\": \"        ROOT / \\\"exports/e1r_v0_2_backtest_summary.json\\\",\""
        },
        {
          "line": 304,
          "text": "          \"text\": \"        ROOT / \\\"exports/e1r_v0_2_backtest_equity_curve.json\\\",\""
        },
        {
          "line": 308,
          "text": "          \"text\": \"        ROOT / \\\"exports/oos_e1r_v0_2_equity_curve.json\\\",\""
        },
        {
          "line": 329,
          "text": "          \"text\": \"        ROOT / \\\"exports/e1r_v0_2_backtest_equity_curve.json\\\",\""
        },
        {
          "line": 333,
          "text": "          \"text\": \"        ROOT / \\\"exports/oos_e1r_v0_2_equity_curve.json\\\",\""
        },
        {
          "line": 401,
          "text": "          \"text\": \"    to generate E1R 5Y interval records:\""
        },
        {
          "line": 417,
          "text": "          \"text\": \"    to generate E1R 5Y interval records:\""
        },
        {
          "line": 441,
          "text": "          \"text\": \"    to generate E1R 5Y interval records:\""
        },
        {
          "line": 485,
          "text": "          \"text\": \"    from src.engine import e1r_composer as composer  # type: ignore\""
        },
        {
          "line": 528,
          "text": "  \"stdout_tail\": \"       \\\"regime_day_weights\\\",\\n              \\\"return_pct\\\",\\n              \\\"size_units_at_exit\\\",\\n              \\\"symbol\\\",\\n              \\\"take_profit_exec_date\\\",\\n              \\\"take_profit_triggered\\\"\\n            ]\\n          }\\n        },\\n        \\\"metrics\\\": {\\n          \\\"variant_id\\\": \\\"E1R_REGIME_AWARE_V0_1\\\"\\n        }\\n      },\\n      {\\n        \\\"path\\\": \\\"exports/portfolio_backtest.json\\\",\\n        \\\"exists\\\": true,\\n        \\\"json_valid\\\": true,\\n        \\\"type\\\": \\\"dict\\\",\\n        \\\"top_keys\\\": [\\n          \\\"alpha_pct\\\",\\n          \\\"avg_execution_drag_pct\\\",\\n          \\\"avg_holding_days\\\",\\n          \\\"avg_loser_pct\\\",\\n          \\\"avg_winner_pct\\\",\\n          \\\"cagr_pct\\\",\\n          \\\"comparison\\\",\\n          \\\"daily_records\\\",\\n          \\\"entry_top_n\\\",\\n          \\\"executed_exit_reason_distribution\\\",\\n          \\\"executed_reduce_reason_distribution\\\",\\n          \\\"execution_model\\\",\\n          \\\"exposure_pct\\\",\\n          \\\"final_equit"
        },
        {
          "line": 553,
          "text": "  \"exports/e1r_v0_2_backtest_summary.json\": {"
        },
        {
          "line": 583,
          "text": "        \"total_return_pct\","
        },
        {
          "line": 587,
          "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 588,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 607,
          "text": "          \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 615,
          "text": "          \"total_return_pct\": 0.0,"
        },
        {
          "line": 644,
          "text": "            \"total_return_pct\","
        },
        {
          "line": 648,
          "text": "            \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 649,
          "text": "            \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 667,
          "text": "  \"exports/e1r_v0_2_backtest_equity_curve.json\": {"
        },
        {
          "line": 679,
          "text": "  \"exports/e1r_v0_2_portfolio_backtest_equity_curve.json\": {"
        },
        {
          "line": 691,
          "text": "  \"exports/e1_e1r_5y_equity_comparison.json\": {"
        },
        {
          "line": 703,
          "text": "  \"data/research/e1r/e1r_formal_backtest_v0_1.json\": {"
        },
        {
          "line": 736,
          "text": "        \"spx_total_return_pct\","
        },
        {
          "line": 737,
          "text": "        \"total_return_pct\","
        },
        {
          "line": 741,
          "text": "        \"total_return_pct\": 65.71,"
        },
        {
          "line": 753,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 756,
          "text": "        \"total_return_pct\": 7.52,"
        },
        {
          "line": 865,
          "text": "        \"entry_type\": \"E1R_UPTREND_CONFIRMED\","
        },
        {
          "line": 941,
          "text": "        \"entry_type\": \"E1R_UPTREND_CONFIRMED\","
        },
        {
          "line": 986,
          "text": "            \"spx_total_return_pct\","
        },
        {
          "line": 987,
          "text": "            \"total_return_pct\","
        },
        {
          "line": 991,
          "text": "            \"total_return_pct\": 65.71,"
        },
        {
          "line": 1003,
          "text": "            \"total_return_pct\""
        },
        {
          "line": 1006,
          "text": "            \"total_return_pct\": 7.52,"
        },
        {
          "line": 1115,
          "text": "            \"entry_type\": \"E1R_UPTREND_CONFIRMED\","
        },
        {
          "line": 1191,
          "text": "            \"entry_type\": \"E1R_UPTREND_CONFIRMED\","
        },
        {
          "line": 1210,
          "text": "  \"exports/e1r_v0_2_backtest_summary.json\": {"
        },
        {
          "line": 1215,
          "text": "  \"exports/e1r_v0_2_backtest_equity_curve.json\": {"
        },
        {
          "line": 1220,
          "text": "  \"exports/e1r_v0_2_portfolio_backtest_equity_curve.json\": {"
        },
        {
          "line": 1225,
          "text": "  \"exports/e1_e1r_5y_equity_comparison.json\": {"
        },
        {
          "line": 1230,
          "text": "  \"data/research/e1r/e1r_formal_backtest_v0_1.json\": {"
        },
        {
          "line": 1240,
          "text": "- `Stage 3.8E-2F-2C-4C-10F-4B-0F`: Expose exact in-memory E1R composition result or select next generator"
        }
      ],
      "counts": {
        "hits": 64
      }
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0I_COMPOSER_INPUT_CANDIDATES.md",
      "sha256": "6bd5dd6c6d05fc50d03cc8dd208f9eba37fe8122059f440b84aa7c125ae5ffe0",
      "score": 120,
      "hits": [
        {
          "line": 7,
          "text": "- Status: `E1R_COMPOSER_INPUT_CANDIDATES_AUDIT_COMPLETE_NO_INVOCATION`"
        },
        {
          "line": 10,
          "text": "- E1R canonical written: `False`"
        },
        {
          "line": 47,
          "text": "        \"total_return_pct\": 7.52,"
        },
        {
          "line": 54,
          "text": "        \"total_return_pct\": 109.22359991347561,"
        },
        {
          "line": 105,
          "text": "        \"spx_total_return_pct\","
        },
        {
          "line": 109,
          "text": "        \"total_return_pct\","
        },
        {
          "line": 120,
          "text": "        \"total_return_pct\": 7.52,"
        },
        {
          "line": 121,
          "text": "        \"spx_total_return_pct\": 69.36,"
        },
        {
          "line": 181,
          "text": "            \"market_shock_rule\","
        },
        {
          "line": 182,
          "text": "            \"risk_off_rule\","
        },
        {
          "line": 221,
          "text": "            \"market_risk_off_block\","
        },
        {
          "line": 222,
          "text": "            \"market_shock_block\","
        },
        {
          "line": 290,
          "text": "            \"market_gate_state\","
        },
        {
          "line": 306,
          "text": "            \"market_gate_state\": \"RISK_OFF\","
        },
        {
          "line": 318,
          "text": "            \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 490,
          "text": "            \"total_return_pct\","
        },
        {
          "line": 503,
          "text": "            \"total_return_pct\": 7.52,"
        },
        {
          "line": 527,
          "text": "              \"market_risk_off_block\": 13,"
        },
        {
          "line": 528,
          "text": "              \"market_shock_block\": 0,"
        },
        {
          "line": 560,
          "text": "            \"total_return_pct\": -21.95,"
        },
        {
          "line": 584,
          "text": "              \"market_risk_off_block\": 6,"
        },
        {
          "line": 585,
          "text": "              \"market_shock_block\": 0,"
        },
        {
          "line": 638,
          "text": "        \"total_return_pct\": 7.52,"
        },
        {
          "line": 645,
          "text": "        \"total_return_pct\": 109.22359991347561,"
        },
        {
          "line": 692,
          "text": "        \"spx_total_return_pct\","
        },
        {
          "line": 696,
          "text": "        \"total_return_pct\","
        },
        {
          "line": 706,
          "text": "        \"total_return_pct\": 7.52,"
        },
        {
          "line": 707,
          "text": "        \"spx_total_return_pct\": 69.36,"
        },
        {
          "line": 767,
          "text": "            \"market_shock_rule\","
        },
        {
          "line": 768,
          "text": "            \"risk_off_rule\","
        },
        {
          "line": 807,
          "text": "            \"market_risk_off_block\","
        },
        {
          "line": 808,
          "text": "            \"market_shock_block\","
        },
        {
          "line": 845,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4A1_SIDECAR_ACTIVATION_AUDIT.json\","
        },
        {
          "line": 915,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4A_SIDECAR_RECORDS_EXPORT_REPORT.json\","
        },
        {
          "line": 989,
          "text": "    \"source_file\": \"exports/e1r_v0_2_sidecar_records_5y.json\","
        },
        {
          "line": 1063,
          "text": "    \"source_file\": \"exports/e1r_v0_2_backtest_summary.json\","
        },
        {
          "line": 1071,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 1079,
          "text": "        \"total_return_pct\": 0.0,"
        },
        {
          "line": 1110,
          "text": "        \"total_return_pct\","
        },
        {
          "line": 1114,
          "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 1115,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 1142,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json\","
        },
        {
          "line": 1192,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json\","
        },
        {
          "line": 1193,
          "text": "    \"json_path\": \"$.source_reports.scripts/export_e1r_v0_2_status.py.term_hits\","
        },
        {
          "line": 1208,
          "text": "        \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 1269,
          "text": "        \"E1R_REGIME_AWARE_V0_2\": {"
        },
        {
          "line": 1293,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json\","
        },
        {
          "line": 1294,
          "text": "    \"json_path\": \"$.source_reports.scripts/run_e1r_v0_2_oos.py.term_hits\","
        },
        {
          "line": 1308,
          "text": "        \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 1398,
          "text": "        \"E1R_REGIME_AWARE_V0_2\": {"
        },
        {
          "line": 1414,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json\","
        },
        {
          "line": 1415,
          "text": "    \"json_path\": \"$.source_reports.src/engine/e1r_composer.py.term_hits\","
        },
        {
          "line": 1429,
          "text": "        \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 1485,
          "text": "        \"E1R_REGIME_AWARE_V0_2\": {"
        },
        {
          "line": 1505,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json\","
        },
        {
          "line": 1506,
          "text": "    \"json_path\": \"$.source_reports.src/engine/e1r_sidecar_sleeve.py.term_hits\","
        },
        {
          "line": 1521,
          "text": "        \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 1596,
          "text": "        \"E1R_REGIME_AWARE_V0_2\": {"
        },
        {
          "line": 1616,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4A_SIDECAR_RECORDS_EXPORT_REPORT.json\","
        },
        {
          "line": 1664,
          "text": "        \"name\": \"E1R_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
        },
        {
          "line": 1681,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C6_INTERVAL_SCHEMA_SOURCE_AUDIT.json\","
        },
        {
          "line": 1728,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C6_INTERVAL_SCHEMA_SOURCE_AUDIT.json\","
        },
        {
          "line": 1796,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json\","
        },
        {
          "line": 1797,
          "text": "    \"json_path\": \"$.export_reports.e1r_backtest_summary.e1r_objects[0].summary_fields\","
        },
        {
          "line": 1804,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 1812,
          "text": "        \"total_return_pct\": 0.0,"
        },
        {
          "line": 1830,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 1833,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 1844,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json\","
        },
        {
          "line": 1852,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 1860,
          "text": "        \"total_return_pct\": 0.0,"
        },
        {
          "line": 1878,
          "text": "        \"total_return_pct\","
        },
        {
          "line": 1882,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 1893,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json\","
        },
        {
          "line": 1901,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 1909,
          "text": "        \"total_return_pct\": 0.0,"
        },
        {
          "line": 1928,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 1931,
          "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 1932,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 1943,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json\","
        },
        {
          "line": 1951,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 1959,
          "text": "        \"total_return_pct\": 0.0,"
        },
        {
          "line": 1978,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 1981,
          "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 1982,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 1993,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json\","
        },
        {
          "line": 2001,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 2009,
          "text": "        \"total_return_pct\": 0.0,"
        },
        {
          "line": 2027,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 2030,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 2041,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json\","
        },
        {
          "line": 2049,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 2057,
          "text": "        \"total_return_pct\": 0.0,"
        },
        {
          "line": 2075,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 2078,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 2089,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json\","
        },
        {
          "line": 2097,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 2105,
          "text": "        \"total_return_pct\": 0.0,"
        },
        {
          "line": 2123,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 2126,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 2137,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json\","
        },
        {
          "line": 2145,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 2153,
          "text": "        \"total_return_pct\": 0.0,"
        },
        {
          "line": 2171,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 2174,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 2185,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json\","
        },
        {
          "line": 2193,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 2201,
          "text": "        \"total_return_pct\": 0.0,"
        },
        {
          "line": 2219,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 2222,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 2233,
          "text": "    \"source_file\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json\","
        },
        {
          "line": 2241,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 2249,
          "text": "        \"total_return_pct\": 0.0,"
        },
        {
          "line": 2267,
          "text": "        \"total_return_pct\""
        },
        {
          "line": 2270,
          "text": "        \"total_return_pct\": 116.7435999134756,"
        }
      ],
      "counts": {
        "hits": 115
      }
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0L_DIRECT_COMPOSE_CANDIDATE_REPORT.md",
      "sha256": "7cb2de2db878748ff6fa9a3bab7dff3e09ed80f90cd01ed3ba9123c25907fd74",
      "score": 120,
      "hits": [
        {
          "line": 7,
          "text": "- Status: `E1R_DIRECT_COMPOSE_CANDIDATE_COMPLETE_NONCANONICAL`"
        },
        {
          "line": 8,
          "text": "- E1R canonical written: `False`"
        },
        {
          "line": 18,
          "text": "    \"total_return_pct\": 89.81714654548038,"
        },
        {
          "line": 26,
          "text": "    \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 34,
          "text": "    \"total_return_pct\": 26.926453367995222,"
        },
        {
          "line": 83,
          "text": "        \"e1r_active_mode\","
        },
        {
          "line": 86,
          "text": "        \"market_gate_state\","
        },
        {
          "line": 115,
          "text": "        \"e1r_active_mode\","
        },
        {
          "line": 118,
          "text": "        \"market_gate_state\","
        },
        {
          "line": 191,
          "text": "- `DIRECT_COMPOSE_SUCCEEDED_BUT_DID_NOT_MATCH_FROZEN_E1R_METRICS`"
        },
        {
          "line": 192,
          "text": "- Recommended: Use this result to quantify gap; frozen E1R core input is still not equal to current E1 5Y core."
        },
        {
          "line": 197,
          "text": "- Recommended action: Use this result to quantify gap; frozen E1R core input is still not equal to current E1 5Y core."
        }
      ],
      "counts": {
        "hits": 12
      }
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0M_DIRECT_COMPOSED_CANDIDATE_VALIDATION.md",
      "sha256": "ff2b678198d9aa193bb95d9ef6368e9c3dee69c5c9040c8ae87b18700edd9d3e",
      "score": 120,
      "hits": [
        {
          "line": 7,
          "text": "- Status: `E1R_DIRECT_COMPOSED_CANDIDATE_VALIDATION_COMPLETE_NONCANONICAL`"
        },
        {
          "line": 8,
          "text": "- E1R canonical written: `False`"
        },
        {
          "line": 16,
          "text": "- `NOT_FROZEN_E1R_V0_2`"
        },
        {
          "line": 17,
          "text": "- Candidate total return: `89.81714654548038`"
        },
        {
          "line": 18,
          "text": "- Frozen total return: `116.7435999134756`"
        },
        {
          "line": 26,
          "text": "  \"e1r_one_row_per_date\": true,"
        },
        {
          "line": 27,
          "text": "  \"e1r_not_symbol_level\": true,"
        },
        {
          "line": 28,
          "text": "  \"e1r_not_diagnostic_only\": true,"
        },
        {
          "line": 29,
          "text": "  \"e1r_row_count_ge_1000\": true,"
        },
        {
          "line": 54,
          "text": "    \"total_return_pct_from_rows\": 89.81569,"
        },
        {
          "line": 85,
          "text": "        \"e1r_active_mode\","
        },
        {
          "line": 88,
          "text": "        \"market_gate_state\","
        },
        {
          "line": 117,
          "text": "        \"e1r_active_mode\","
        },
        {
          "line": 120,
          "text": "        \"market_gate_state\","
        },
        {
          "line": 134,
          "text": "  \"e1r_direct_composed\": {"
        },
        {
          "line": 148,
          "text": "    \"total_return_pct_from_rows\": 90.00639291282218,"
        },
        {
          "line": 230,
          "text": "    \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 238,
          "text": "    \"total_return_pct\": 89.81714654548038,"
        },
        {
          "line": 246,
          "text": "    \"total_return_pct\": 26.926453367995222,"
        },
        {
          "line": 258,
          "text": "- `DIRECT_COMPOSED_CANDIDATE_CURVE_VALID_BUT_NOT_FROZEN_E1R`"
        }
      ],
      "counts": {
        "hits": 20
      }
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.md",
      "sha256": "df886dfff7dd0a44610b6911dee2623b58634e4eb72949c8294723fbfac4960c",
      "score": 120,
      "hits": [
        {
          "line": 1,
          "text": "# Stage 3.8E-2F-2C-4C-10F-4B-0 E1 vs E1R UPTREND Core Contract Audit"
        },
        {
          "line": 7,
          "text": "- Status: `E1_E1R_UPTREND_CORE_CONTRACT_AUDIT_COMPLETE_NO_EXPORTS_WRITTEN`"
        },
        {
          "line": 16,
          "text": "  \"contract_conclusion\": \"UNCONFIRMED_DO_NOT_USE_E1_CORE_AS_E1R_CORE_CANONICAL_YET\","
        },
        {
          "line": 18,
          "text": "    \"E1 saved core row-derived total_return_pct is 89.8157%, while frozen E1R target total_return_pct is 116.7436%; delta=26.9279pp.\","
        },
        {
          "line": 20,
          "text": "    \"Source references core_variant_result / compose_e1r_v0_2_variant, so E1R appears to be composed from an explicit core result plus sidecar result.\","
        },
        {
          "line": 21,
          "text": "    \"Source/result terms include e1r_uptrend_execution_enabled / e1r_candidates; this suggests E1R may have distinct execution instrumentation beyond plain E1.\","
        },
        {
          "line": 22,
          "text": "    \"Found 18 metric/source candidate files that may contain frozen E1R/core contract evidence.\""
        },
        {
          "line": 25,
          "text": "    \"E1 core return differs materially from frozen E1R total return; sidecar alone must explain a large gap if E1 core is reused.\","
        },
        {
          "line": 26,
          "text": "    \"E1R UPTREND core may not be identical to current exported E1 core unless the specific core_variant_result is recovered.\""
        },
        {
          "line": 28,
          "text": "  \"recommended_next_action\": \"Recover or regenerate the exact E1R core_variant_result / continuous core daily equity used by frozen E1R v0.2, then compare it against exports/e1_5y_backtest_equity_curve.json before any canonical E1R composition.\""
        },
        {
          "line": 47,
          "text": "  \"total_return_pct_from_rows\": 89.81569,"
        },
        {
          "line": 83,
          "text": "  \"path\": \"exports/e1r_v0_2_sidecar_records_5y.json\","
        },
        {
          "line": 84,
          "text": "  \"artifact_type\": \"e1r_v0_2_regime_aware_sidecar_records_5y\","
        },
        {
          "line": 105,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json\","
        },
        {
          "line": 108,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 110,
          "text": "      \"E1R\","
        },
        {
          "line": 112,
          "text": "      \"compose_e1r\","
        },
        {
          "line": 114,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 139,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json\","
        },
        {
          "line": 142,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 144,
          "text": "      \"E1R\","
        },
        {
          "line": 146,
          "text": "      \"compose_e1r\","
        },
        {
          "line": 148,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 167,
          "text": "      \"top_e1r_candidates\""
        },
        {
          "line": 174,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json\","
        },
        {
          "line": 177,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 179,
          "text": "      \"E1R\","
        },
        {
          "line": 181,
          "text": "      \"compose_e1r\","
        },
        {
          "line": 183,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 205,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\","
        },
        {
          "line": 208,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 210,
          "text": "      \"E1R\","
        },
        {
          "line": 212,
          "text": "      \"compose_e1r\","
        },
        {
          "line": 214,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 239,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json\","
        },
        {
          "line": 242,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 244,
          "text": "      \"E1R\","
        },
        {
          "line": 246,
          "text": "      \"compose_e1r\","
        },
        {
          "line": 247,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 271,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json\","
        },
        {
          "line": 274,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 276,
          "text": "      \"E1R\","
        },
        {
          "line": 277,
          "text": "      \"compose_e1r\","
        },
        {
          "line": 279,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 299,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json\","
        },
        {
          "line": 302,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 304,
          "text": "      \"E1R\","
        },
        {
          "line": 306,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 328,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10E_R_CONTINUOUS_CAPITAL_CONTRACT.json\","
        },
        {
          "line": 331,
          "text": "      \"E1R\","
        },
        {
          "line": 333,
          "text": "      \"compose_e1r\","
        },
        {
          "line": 335,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 362,
          "text": "    \"path\": \"docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json\","
        },
        {
          "line": 365,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 367,
          "text": "      \"E1R\","
        },
        {
          "line": 369,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 390,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json\","
        },
        {
          "line": 393,
          "text": "      \"E1R\","
        },
        {
          "line": 395,
          "text": "      \"compose_e1r\","
        },
        {
          "line": 397,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 421,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json\","
        },
        {
          "line": 424,
          "text": "      \"E1R\","
        },
        {
          "line": 426,
          "text": "      \"compose_e1r\","
        },
        {
          "line": 427,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 449,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10A_DIRECT_GENERATOR_FUNCTION_AUDIT.json\","
        },
        {
          "line": 452,
          "text": "      \"E1R\","
        },
        {
          "line": 454,
          "text": "      \"compose_e1r\","
        },
        {
          "line": 456,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 477,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C1_5Y_EQUITY_ARTIFACT_AUDIT.json\","
        },
        {
          "line": 480,
          "text": "      \"E1R\","
        },
        {
          "line": 482,
          "text": "      \"compose_e1r\","
        },
        {
          "line": 483,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 500,
          "text": "      \"top_e1r_candidates\""
        },
        {
          "line": 507,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C6_INTERVAL_SCHEMA_SOURCE_AUDIT.json\","
        },
        {
          "line": 510,
          "text": "      \"E1R\","
        },
        {
          "line": 513,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 536,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8A_DASHBOARD_REFACTOR_AUDIT.json\","
        },
        {
          "line": 539,
          "text": "      \"E1R\","
        },
        {
          "line": 541,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 568,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8D_NATIVE_RENDER_AUDIT.json\","
        },
        {
          "line": 571,
          "text": "      \"E1R\","
        },
        {
          "line": 573,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 605,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F1G0_SUMMARY_MAPPING_AUDIT.json\","
        },
        {
          "line": 608,
          "text": "      \"E1R\","
        },
        {
          "line": 610,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 634,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3D_E1_CANONICAL_INTEGRITY_AUDIT.json\","
        },
        {
          "line": 637,
          "text": "      \"E1R\","
        },
        {
          "line": 638,
          "text": "      \"e1r_candidate_count\","
        },
        {
          "line": 639,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 661,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json\","
        },
        {
          "line": 664,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 666,
          "text": "      \"E1R\","
        },
        {
          "line": 667,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 696,
          "text": "    \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
        },
        {
          "line": 699,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 701,
          "text": "      \"E1R\","
        },
        {
          "line": 702,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 725,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 729,
          "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 730,
          "text": "      \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 739,
          "text": "    \"path\": \"data/research/e1r/e1r_formal_backtest_v0_1.json\","
        },
        {
          "line": 742,
          "text": "      \"E1R\","
        },
        {
          "line": 743,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 770,
          "text": "      \"spx_total_return_pct\","
        },
        {
          "line": 771,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 775,
          "text": "      \"total_return_pct\": 65.71,"
        },
        {
          "line": 784,
          "text": "    \"path\": \"data/research/e1r/e1r_phase3e_confirmed_quality_diagnostic.json\","
        },
        {
          "line": 787,
          "text": "      \"E1R\","
        },
        {
          "line": 788,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 819,
          "text": "    \"path\": \"data/research/e1r/e1r_regime_attribution_review.json\","
        },
        {
          "line": 822,
          "text": "      \"E1R\","
        },
        {
          "line": 823,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 848,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_2_BACKTEST_INTEGRATION_REPORT.json\","
        },
        {
          "line": 851,
          "text": "      \"E1R\","
        },
        {
          "line": 853,
          "text": "      \"compose_e1r\","
        },
        {
          "line": 864,
          "text": "      \"feature_e1r_hits\","
        },
        {
          "line": 867,
          "text": "      \"integrated_e1r_hits\","
        },
        {
          "line": 875,
          "text": "      \"required_e1r_markers\","
        },
        {
          "line": 886,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_5_DEPENDENCY_FIX_REPORT.json\","
        },
        {
          "line": 889,
          "text": "      \"E1R\","
        },
        {
          "line": 891,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 917,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_5_MAIN_SMOKE_TEST_REPORT.json\","
        },
        {
          "line": 920,
          "text": "      \"E1R\","
        },
        {
          "line": 922,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 954,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2B_STRUCTURAL_DIFF_AUDIT.json\","
        },
        {
          "line": 957,
          "text": "      \"E1R\","
        },
        {
          "line": 958,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 975,
          "text": "      \"removed_non_ui_candidates_in_renderE1RResearchPanel\","
        },
        {
          "line": 988,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2B_V3_PREPATCH_AUDIT.json\","
        },
        {
          "line": 991,
          "text": "      \"E1R\","
        },
        {
          "line": 992,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 1012,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2B_V4_SURGICAL_MAP.json\","
        },
        {
          "line": 1015,
          "text": "      \"E1R\","
        },
        {
          "line": 1016,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 1046,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F1B_FORWARD_IMPLEMENTATION_PLAN.json\","
        },
        {
          "line": 1049,
          "text": "      \"E1R\","
        },
        {
          "line": 1078,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F1C_RUNNER_DRY_RUN_AUDIT.json\","
        },
        {
          "line": 1081,
          "text": "      \"E1R\","
        },
        {
          "line": 1083,
          "text": "      \"total_return_pct\","
        },
        {
          "line": 1109,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C3A_TRADE_LOG_RENDER_PATH_AUDIT.json\","
        },
        {
          "line": 1112,
          "text": "      \"E1R\","
        },
        {
          "line": 1135,
          "text": "    \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json\","
        },
        {
          "line": 1138,
          "text": "      \"E1R\","
        },
        {
          "line": 1214,
          "text": "        \"e1r_uptrend_execution_enabled\""
        },
        {
          "line": 1219,
          "text": "          \"text\": \"    e1r_shell_mode = bool(a.get(\\\"e1r_shell_mode\\\", False))\""
        },
        {
          "line": 1223,
          "text": "          \"text\": \"    e1r_regime_wiring_enabled = bool(a.get(\\\"e1r_regime_wiring_enabled\\\", False))\""
        },
        {
          "line": 1227,
          "text": "          \"text\": \"    e1r_uptrend_execution_enabled = bool(a.get(\\\"e1r_uptrend_execution_enabled\\\", False))\""
        },
        {
          "line": 1231,
          "text": "          \"text\": \"    e1r_regime_daily = a.get(\\\"e1r_regime_daily\\\", {}) or {}\""
        },
        {
          "line": 1252,
          "text": "          \"text\": \"    def _e1r_mode_for_regime(regime: str) -> str:\""
        },
        {
          "line": 1277,
          "text": "          \"text\": \"    def _e1r_mode_for_regime(regime: str) -> str:\""
        },
        {
          "line": 1368,
          "text": "          \"text\": \"    def _e1r_risk_budget_for_regime(regime: str) -> dict:\""
        },
        {
          "line": 1393,
          "text": "          \"text\": \"    def _e1r_risk_budget_for_regime(regime: str) -> dict:\""
        },
        {
          "line": 1480,
          "text": "          \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
        },
        {
          "line": 1484,
          "text": "          \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
        },
        {
          "line": 1525,
          "text": "          \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
        },
        {
          "line": 1550,
          "text": "          \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
        },
        {
          "line": 1554,
          "text": "          \"text\": \"    market_shock_daily_return = float(a.get(\\\"market_shock_daily_return\\\", -0.02))\""
        },
        {
          "line": 1642,
          "text": "          \"text\": \"                f\\\"relstop={relative_stop_enabled} gate={market_gate_enabled} ──\\\")\""
        },
        {
          "line": 1700,
          "text": "          \"text\": \"                        \\\"entry_regime\\\": _e1r_regime_on(exec_date),\""
        },
        {
          "line": 1708,
          "text": "        \"E1R\""
        }
      ],
      "counts": {
        "hits": 160
      }
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.md",
      "sha256": "92204fbd0ac4d95d8c8f4eef579b26b15fd3f70628e1668174dca3ef3c7d84d5",
      "score": 120,
      "hits": [
        {
          "line": 17,
          "text": "- No strong E1R 5Y portfolio-level equity candidate found in v13/main JSON artifacts."
        },
        {
          "line": 18,
          "text": "- E1R 5Y symbol/diagnostic candidate exists: exports/e1r_v0_2_backtest_equity_curve.json list=rows rows=8819 unique_dates=859 max_rows_per_date=19."
        },
        {
          "line": 23,
          "text": "- score `127` · `docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json`"
        },
        {
          "line": 24,
          "text": "  - signature_hits: `E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, E1R v0.2, 116.74, 76.84, 2021-06-11, 2026-06-18, 2026-06-16, 1258, UPTREND, SIDEWAYS, DOWNTREND, portfolio_value, daily_equity, equity_curve, strategy_indexed, spx_return, total_return, max_drawdown, sharpe, profit_factor`"
        },
        {
          "line": 27,
          "text": "  - list `source_reports.scripts/run_e1r_v0_2_oos.py.defs` kind `unknown` rows `3` dates `None→None` unique `0` max_rows_per_date `None` keys `kind, line, name, text`"
        },
        {
          "line": 28,
          "text": "  - list `source_reports.scripts/run_e1r_v0_2_oos.py.term_hits.target` kind `numeric_array_candidate` rows `7` dates `None→None` unique `0` max_rows_per_date `None` keys ``"
        },
        {
          "line": 29,
          "text": "  - list `source_reports.scripts/run_e1r_v0_2_oos.py.term_hits.target_weight` kind `numeric_array_candidate` rows `2` dates `None→None` unique `0` max_rows_per_date `None` keys ``"
        },
        {
          "line": 30,
          "text": "- score `99` · `docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json`"
        },
        {
          "line": 31,
          "text": "  - signature_hits: `E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, E1R v0.2, 2026-06-18, 2026-06-16, UPTREND, SIDEWAYS, DOWNTREND, portfolio_value, daily_equity, equity_curve, spx_return, total_return, max_drawdown, sharpe, profit_factor`"
        },
        {
          "line": 37,
          "text": "- score `82` · `docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json`"
        },
        {
          "line": 38,
          "text": "  - signature_hits: `E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, E1R v0.2, E1-R v0.2, 116.74, 76.84, 2021-06-11, 2026-06-18, 2026-06-16, 1258, 1261, UPTREND, SIDEWAYS, DOWNTREND, portfolio_value, daily_equity, equity_curve, strategy_indexed, spx_curve, spx_return, total_return, max_drawdown, sharpe, profit_factor`"
        },
        {
          "line": 40,
          "text": "  - list `kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.status_fields` kind `unknown` rows `9` dates `None→None` unique `0` max_rows_per_date `None` keys ``"
        },
        {
          "line": 41,
          "text": "  - list `kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.performance_fields` kind `unknown` rows `13` dates `None→None` unique `0` max_rows_per_date `None` keys ``"
        },
        {
          "line": 42,
          "text": "  - list `kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.exposure_fields` kind `unknown` rows `4` dates `None→None` unique `0` max_rows_per_date `None` keys ``"
        },
        {
          "line": 43,
          "text": "  - list `kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.regime_fields` kind `unknown` rows `6` dates `None→None` unique `0` max_rows_per_date `None` keys ``"
        },
        {
          "line": 44,
          "text": "- score `76` · `docs/research/E1R_V0_2_STAGE3_8E2F2C3FA_MARKET_STATE_FIELD_AUDIT.json`"
        },
        {
          "line": 52,
          "text": "  - signature_hits: `E1_AUDITED_G4_MINHOLD10, equity_curve, spx_curve, total_return, max_drawdown, sharpe, profit_factor`"
        },
        {
          "line": 53,
          "text": "  - metrics: `{\"name\": \"3-Variant LS60 Mode Comparison\", \"version\": \"v1.6-ls60-mode-comparison\", \"total_return_pct\": 7.52, \"alpha_pct\": -61.84, \"max_drawdown_pct\": 38.1, \"profit_factor\": 1.25, \"sample_validity.simulation_start_date\": \"2023-11-06\", \"sample_validity.simulation_end_date\": \"2026-06-11\", \"sample_validity.simulation_days\": 651}`"
        },
        {
          "line": 57,
          "text": "  - list `daily_records` kind `portfolio_daily_equity_candidate` rows `22` dates `2023-11-06→2026-05-13` unique `22` max_rows_per_date `1` keys `cash, date, market_gate_state, n_holdings, pending_orders, position_value, spx_close, spx_day_return_pct, spx_ma50, total_equity`"
        },
        {
          "line": 60,
          "text": "  - signature_hits: `E1_AUDITED_G4_MINHOLD10, equity_curve, spx_curve, total_return, max_drawdown, sharpe, profit_factor`"
        },
        {
          "line": 67,
          "text": "  - signature_hits: `116.74, 103.85, 76.84, 39.90, 2021-06-11, 2026-06-18, 2026-06-16, 1258, 1261`"
        },
        {
          "line": 70,
          "text": "  - signature_hits: `116.74, 103.85, 76.84, 39.90, 2021-06-11, 2026-06-18, 2026-06-16, 1258, 1261`"
        },
        {
          "line": 73,
          "text": "  - signature_hits: `116.74, 103.85, 39.90, 2021-06-11, 2026-06-18, 2026-06-16, 1258, 1261`"
        },
        {
          "line": 76,
          "text": "  - signature_hits: `116.74, 103.85, 76.84, 2021-06-11, 2026-06-18, 2026-06-16, 1258, 1261`"
        },
        {
          "line": 79,
          "text": "## Top E1R Candidates"
        },
        {
          "line": 81,
          "text": "- score `139` · `docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json`"
        },
        {
          "line": 82,
          "text": "  - signature_hits: `E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, E1R v0.2, 116.74, 76.84, 2021-06-11, 2026-06-18, 2026-06-16, 1258, UPTREND, SIDEWAYS, DOWNTREND, portfolio_value, daily_equity, equity_curve, strategy_indexed, spx_return, total_return, max_drawdown, sharpe, profit_factor`"
        },
        {
          "line": 85,
          "text": "  - list `source_reports.scripts/run_e1r_v0_2_oos.py.defs` kind `unknown` rows `3` dates `None→None` unique `0` max_rows_per_date `None` keys `kind, line, name, text`"
        },
        {
          "line": 86,
          "text": "  - list `source_reports.scripts/run_e1r_v0_2_oos.py.term_hits.target` kind `numeric_array_candidate` rows `7` dates `None→None` unique `0` max_rows_per_date `None` keys ``"
        },
        {
          "line": 87,
          "text": "  - list `source_reports.scripts/run_e1r_v0_2_oos.py.term_hits.target_weight` kind `numeric_array_candidate` rows `2` dates `None→None` unique `0` max_rows_per_date `None` keys ``"
        },
        {
          "line": 88,
          "text": "- score `111` · `docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json`"
        },
        {
          "line": 89,
          "text": "  - signature_hits: `E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, E1R v0.2, 2026-06-18, 2026-06-16, UPTREND, SIDEWAYS, DOWNTREND, portfolio_value, daily_equity, equity_curve, spx_return, total_return, max_drawdown, sharpe, profit_factor`"
        },
        {
          "line": 95,
          "text": "- score `94` · `docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json`"
        },
        {
          "line": 96,
          "text": "  - signature_hits: `E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, E1R v0.2, E1-R v0.2, 116.74, 76.84, 2021-06-11, 2026-06-18, 2026-06-16, 1258, 1261, UPTREND, SIDEWAYS, DOWNTREND, portfolio_value, daily_equity, equity_curve, strategy_indexed, spx_curve, spx_return, total_return, max_drawdown, sharpe, profit_factor`"
        },
        {
          "line": 98,
          "text": "  - list `kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.status_fields` kind `unknown` rows `9` dates `None→None` unique `0` max_rows_per_date `None` keys ``"
        },
        {
          "line": 99,
          "text": "  - list `kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.performance_fields` kind `unknown` rows `13` dates `None→None` unique `0` max_rows_per_date `None` keys ``"
        },
        {
          "line": 100,
          "text": "  - list `kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.exposure_fields` kind `unknown` rows `4` dates `None→None` unique `0` max_rows_per_date `None` keys ``"
        },
        {
          "line": 101,
          "text": "  - list `kickoff_schema.required_daily_exports.exports/oos_e1r_v0_2_summary.json.regime_fields` kind `unknown` rows `6` dates `None→None` unique `0` max_rows_per_date `None` keys ``"
        },
        {
          "line": 102,
          "text": "- score `88` · `docs/research/E1R_V0_2_STAGE3_8E2F2C3FA_MARKET_STATE_FIELD_AUDIT.json`"
        },
        {
          "line": 110,
          "text": "  - signature_hits: `E1_AUDITED_G4_MINHOLD10, equity_curve, spx_curve, total_return, max_drawdown, sharpe, profit_factor`"
        },
        {
          "line": 111,
          "text": "  - metrics: `{\"name\": \"3-Variant LS60 Mode Comparison\", \"version\": \"v1.6-ls60-mode-comparison\", \"total_return_pct\": 7.52, \"alpha_pct\": -61.84, \"max_drawdown_pct\": 38.1, \"profit_factor\": 1.25, \"sample_validity.simulation_start_date\": \"2023-11-06\", \"sample_validity.simulation_end_date\": \"2026-06-11\", \"sample_validity.simulation_days\": 651}`"
        },
        {
          "line": 115,
          "text": "  - list `daily_records` kind `portfolio_daily_equity_candidate` rows `22` dates `2023-11-06→2026-05-13` unique `22` max_rows_per_date `1` keys `cash, date, market_gate_state, n_holdings, pending_orders, position_value, spx_close, spx_day_return_pct, spx_ma50, total_equity`"
        },
        {
          "line": 118,
          "text": "  - signature_hits: `E1_AUDITED_G4_MINHOLD10, equity_curve, spx_curve, total_return, max_drawdown, sharpe, profit_factor`"
        },
        {
          "line": 124,
          "text": "- score `46` · `data/research/e1r/e1r_phase3i_sideways_quality_decomposition_diagnostic.json`"
        },
        {
          "line": 126,
          "text": "  - metrics: `{\"strategy_id\": \"E1R_REGIME_AWARE_V0_1\"}`"
        },
        {
          "line": 132,
          "text": "- score `45` · `exports/e1r_v0_2_backtest_equity_curve.json`"
        },
        {
          "line": 133,
          "text": "  - signature_hits: `E1R_REGIME_AWARE_V0_2, 116.74, 103.85, 76.84, 2021-06-11, 2026-06-16, 1258, 1261, UPTREND, equity_curve`"
        },
        {
          "line": 134,
          "text": "  - metrics: `{\"variant\": \"E1R_REGIME_AWARE_V0_2\"}`"
        },
        {
          "line": 135,
          "text": "  - list `rows` kind `symbol_level_or_diagnostic_rows` rows `8819` dates `2021-06-11→2026-06-16` unique `859` max_rows_per_date `19` keys `close, date, diagnostic_only, e1r_entry_type, e1r_uptrend_confirmed_eligible, e1r_uptrend_emerging_eligible, equity, leader_rank, leader_score, ma20, ma20_slope, ma50, ma50_slope, momentum_acceleration, momentum_score, reasons, rs_20d_improvement, rs_prev20, rs_score, spx_regime`"
        },
        {
          "line": 136,
          "text": "  - list `equity_curve` kind `symbol_level_or_diagnostic_rows` rows `8819` dates `2021-06-11→2026-06-16` unique `859` max_rows_per_date `19` keys `close, date, diagnostic_only, e1r_entry_type, e1r_uptrend_confirmed_eligible, e1r_uptrend_emerging_eligible, equity, leader_rank, leader_score, ma20, ma20_slope, ma50, ma50_slope, momentum_acceleration, momentum_score, reasons, rs_20d_improvement, rs_prev20, rs_score, spx_regime`"
        },
        {
          "line": 137,
          "text": "- score `42` · `data/research/e1r/e1r_regime_attribution_review.json`"
        },
        {
          "line": 138,
          "text": "  - signature_hits: `E1_AUDITED_G4_MINHOLD10, UPTREND, SIDEWAYS, DOWNTREND, total_return, max_drawdown, sharpe, profit_factor`"
        },
        {
          "line": 141,
          "text": "  - list `strategies.E1R_REGIME_AWARE_V0_1.daily_sample` kind `portfolio_daily_equity_candidate` rows `7` dates `2023-11-06→2026-06-11` unique `6` max_rows_per_date `1` keys `daily_return_pct, date, ellipsis, equity, exposure_pct, regime, spx_day_return_pct`"
        },
        {
          "line": 142,
          "text": "- score `38` · `docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json`"
        },
        {
          "line": 143,
          "text": "  - signature_hits: `E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, E1R v0.2, 116.74, 76.84, 2021-06-11, 2026-06-18, 2026-06-16, 1258, UPTREND, SIDEWAYS, equity_curve, spx_curve, spx_return, total_return, max_drawdown, sharpe, profit_factor`"
        },
        {
          "line": 152,
          "text": "### `data/research/e1r/e1r_formal_backtest_v0_1.json`"
        },
        {
          "line": 156,
          "text": "- metrics: `{\"trades\": [{\"symbol\": \"MELI\", \"entry_date\": \"2023-11-28\", \"exit_date\": \"2024-01-04\", \"entry_signal\": \"BUY\", \"exit_signal\": \"EXIT\", \"entry_price\": 1599.21, \"avg_cost\": 1607.2, \"exit_price\": 1500.0, \"effective_exit\": 1482.16, \"return_pct\": -4.73, \"max_gain_pct\": 2.79, \"max_drawdown_in_trade\": 9.2, \"holding_days\": 26, \"size_units_at_exit\": 0.5, \"leader_score_entry\": 94.4, \"relative_stop_triggered\": false, \"relative_stop_exec_date\": null, \"take_profit_triggered\": false, \"take_profit_exec_date\": null, \"realized_pnl_before_exit\": -282.58, \"actions_during_trade\": [\"BUY\", \"ADD\", \"ADD\", \"BUY\", \"ADD\", \"ADD\", \"BUY\", \"ADD\", \"HOLD\", \"REDUCE\", \"REDUCE\", \"REDUCE\", \"HOLD\", \"HOLD\", \"HOLD\", \"HOLD\", \"HOLD\", \"HOLD\", \"HOLD\", \"REDUCE\", \"REDUCE\", \"REDUCE\", \"REDUCE\", \"REDUCE\", \"REDUCE\", \"REDUCE\", \"REDUCE\", \"REDUCE\", \"EXIT\"], \"action_count\": 29, \"execution_model\": \"adverse_intraday_v1.0\", \"entry_adverse_gap_pct\": 0.5, \"exit_adverse_gap_pct\": 1.19, \"total_execution_drag_pct\": 1.689, \"is_sim_end\": f"
        },
        {
          "line": 173,
          "text": "- list `backtest.results.layer_d.daily_records` kind `portfolio_daily_equity_candidate` rows `22` dates `2023-11-06→2026-05-13` unique `22` max_rows_per_date `1` keys `cash, date, market_gate_state, n_holdings, pending_orders, position_value, spx_close, spx_day_return_pct, spx_ma50, total_equity`"
        },
        {
          "line": 175,
          "text": "### `exports/e1r_v0_2_backtest_summary.json`"
        },
        {
          "line": 178,
          "text": "- top_keys: `alpha_pct, artifact_type, composition_exists, frozen_artifact, max_drawdown_pct, profit_factor, regeneration_note, regime_aware_logic, research_status, row_count, sharpe_ratio, sidecar_active_by_regime, sidecar_active_by_subclass, sidecar_active_days, source_file, source_json_path, spx_return_pct, strategy_id, total_return_pct, variant`"
        },
        {
          "line": 179,
          "text": "- metrics: `{\"strategy_id\": \"E1R_REGIME_AWARE_V0_2\", \"variant\": \"E1R_REGIME_AWARE_V0_2\", \"total_return_pct\": 116.7435999134756, \"spx_return_pct\": 76.844174428316, \"alpha_pct\": 39.89942548515961, \"max_drawdown_pct\": 25.904809362815108, \"profit_factor\": 1.1919630955509348}`"
        },
        {
          "line": 181,
          "text": "### `exports/e1r_v0_2_backtest_equity_curve.json`"
        },
        {
          "line": 185,
          "text": "- metrics: `{\"variant\": \"E1R_REGIME_AWARE_V0_2\"}`"
        },
        {
          "line": 186,
          "text": "- list `rows` kind `symbol_level_or_diagnostic_rows` rows `8819` dates `2021-06-11→2026-06-16` unique `859` max_rows_per_date `19` keys `close, date, diagnostic_only, e1r_entry_type, e1r_uptrend_confirmed_eligible, e1r_uptrend_emerging_eligible, equity, leader_rank, leader_score, ma20, ma20_slope, ma50, ma50_slope, momentum_acceleration, momentum_score, reasons, rs_20d_improvement, rs_prev20, rs_score, spx_regime, symbol, trend_health`"
        },
        {
          "line": 187,
          "text": "- list `equity_curve` kind `symbol_level_or_diagnostic_rows` rows `8819` dates `2021-06-11→2026-06-16` unique `859` max_rows_per_date `19` keys `close, date, diagnostic_only, e1r_entry_type, e1r_uptrend_confirmed_eligible, e1r_uptrend_emerging_eligible, equity, leader_rank, leader_score, ma20, ma20_slope, ma50, ma50_slope, momentum_acceleration, momentum_score, reasons, rs_20d_improvement, rs_prev20, rs_score, spx_regime, symbol, trend_health`"
        },
        {
          "line": 189,
          "text": "### `exports/oos_e1r_v0_2_equity_curve.json`"
        },
        {
          "line": 198,
          "text": "- dashboard_chart_should_not_use_current_e1r_backtest_equity_directly: `True`"
        },
        {
          "line": 199,
          "text": "- reason: E1R 5Y backtest equity artifact in exports is symbol-level/diagnostic rows, not one row per date."
        },
        {
          "line": 204,
          "text": "- If top candidates do not contain one-row-per-date 5Y E1/E1R portfolio curves, do not patch the chart again."
        }
      ],
      "counts": {
        "hits": 69
      }
    },
    {
      "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.md",
      "sha256": "af5a3de2472b81f26e15ca184c90a05cbef22b625f27805a5fe83bb36a8a7218",
      "score": 120,
      "hits": [
        {
          "line": 16,
          "text": "- e1r_composer.py contains build_equity_records_from_returns; this is the best first candidate for E1R portfolio-level equity construction."
        },
        {
          "line": 17,
          "text": "- e1r_composer.py contains extract_core_interval_returns; likely can rebuild core interval portfolio returns before composing equity."
        },
        {
          "line": 18,
          "text": "- export_e1r_v0_2_backtest_equity.py has normalize/extract functions but current output is diagnostic rows; likely needs replacement/export-only wrapper, not minor patch."
        },
        {
          "line": 19,
          "text": "- e1r_formal_backtest_v0_1.json has numeric equity_curve length=131; useful as reference, but too short for full 5Y daily canonical chart."
        },
        {
          "line": 21,
          "text": "- Toy import probe for e1r_composer.py ran successfully; wrapper can likely import composer functions safely."
        },
        {
          "line": 25,
          "text": "### `src/engine/e1r_composer.py`"
        },
        {
          "line": 37,
          "text": "### `src/engine/e1r_sidecar_sleeve.py`"
        },
        {
          "line": 57,
          "text": "### `scripts/export_e1r_v0_2_backtest_equity.py`"
        },
        {
          "line": 65,
          "text": "- path literals: `Missing exports/backtest.json, Wrote exports/e1r_v0_2_backtest_equity_curve.json, Wrote exports/e1r_v0_2_backtest_summary.json, exports/backtest.json, exports/e1r_v0_2_backtest_equity_curve.json, exports/e1r_v0_2_backtest_summary.json`"
        },
        {
          "line": 67,
          "text": "### `scripts/run_e1r_v0_2_oos_equity.py`"
        },
        {
          "line": 73,
          "text": "- path literals: `*.json, exports/e1r_v0_2_status.json, exports/oos_e1r_v0_2_equity_curve.json, exports/oos_e1r_v0_2_sidecar.json, exports/oos_e1r_v0_2_summary.json, exports/oos_equity_curve.json, exports/oos_summary.json`"
        },
        {
          "line": 75,
          "text": "### `scripts/run_e1r_v0_2_forward_performance_core.py`"
        },
        {
          "line": 82,
          "text": "- path literals: `e1r_v0_2_portfolio_state.json, e1r_v0_2_status.json, oos_e1r_v0_2_equity_curve.json, oos_e1r_v0_2_orders.json, oos_e1r_v0_2_positions.json, oos_e1r_v0_2_summary.json, oos_summary.json`"
        },
        {
          "line": 84,
          "text": "### `data/research/e1r/e1r_formal_backtest_v0_1.json`"
        },
        {
          "line": 88,
          "text": "- metrics: `{\"variant_id\": \"E1R_REGIME_AWARE_V0_1\"}`"
        },
        {
          "line": 97,
          "text": "- top_keys: `alpha_pct, avg_execution_drag_pct, avg_holding_days, avg_loser_pct, avg_winner_pct, cagr_pct, comparison, daily_records, entry_top_n, executed_exit_reason_distribution, executed_reduce_reason_distribution, execution_model, exposure_pct, final_equity, generated_at, generated_at_display, initial_capital, invalid_trades, invalid_trades_count, layer, market_entry_gate, max_drawdown_pct, name, number_of_trades, p0_passed, partial_take_profit, pending_orders_executed, pending_orders_skipped, pending_signal_reason_distribution, period_comparison, portfolio_action_distribution, profit_factor, rank_based_exit, sample_validity, selected_variant, selection_policy, sharpe_ratio, skipped_orders_by_reason, spx_cagr_pct, spx_total_return_pct, status, strategy_controls, strategy_variant, total_return_pct, total_trades_all, variant_results, version, win_rate_pct`"
        },
        {
          "line": 98,
          "text": "- metrics: `{\"version\": \"v1.6-ls60-mode-comparison\", \"total_return_pct\": 7.52, \"alpha_pct\": -61.84, \"max_drawdown_pct\": 38.1, \"profit_factor\": 1.25, \"sharpe_ratio\": 0.18, \"final_equity\": 107519.31, \"initial_capital\": 100000.0, \"sample_validity\": {\"is_valid\": true, \"sample_status\": \"VALID\", \"simulation_start_date\": \"2023-11-06\", \"simulation_end_date\": \"2026-06-11\", \"simulation_days\": 651, \"total_trades\": 47, \"completed_trades\": 44, \"sim_end_trades\": 3, \"sim_end_ratio_pct\": 6.4, \"invalid_trades\": 0, \"minimum_required\": {\"sim_days\": 252, \"trades\": 20, \"sim_end_ratio_pct\": 50, \"invalid\": 0}}}`"
        },
        {
          "line": 101,
          "text": "  - `daily_records` length `22` last_type `dict` keys `cash, date, market_gate_state, n_holdings, pending_orders, position_value, spx_close, spx_day_return_pct, spx_ma50, total_equity`"
        },
        {
          "line": 104,
          "text": "### `exports/e1r_v0_2_backtest_summary.json`"
        },
        {
          "line": 107,
          "text": "- top_keys: `alpha_pct, artifact_type, composition_exists, frozen_artifact, max_drawdown_pct, profit_factor, regeneration_note, regime_aware_logic, research_status, row_count, sharpe_ratio, sidecar_active_by_regime, sidecar_active_by_subclass, sidecar_active_days, source_file, source_json_path, spx_return_pct, strategy_id, total_return_pct, variant`"
        },
        {
          "line": 108,
          "text": "- metrics: `{\"strategy_id\": \"E1R_REGIME_AWARE_V0_2\", \"variant\": \"E1R_REGIME_AWARE_V0_2\", \"total_return_pct\": 116.7435999134756, \"spx_return_pct\": 76.844174428316, \"alpha_pct\": 39.89942548515961, \"max_drawdown_pct\": 25.904809362815108, \"profit_factor\": 1.1919630955509348, \"sharpe_ratio\": 0.7957270568329264}`"
        },
        {
          "line": 110,
          "text": "### `exports/e1r_v0_2_backtest_equity_curve.json`"
        },
        {
          "line": 114,
          "text": "- metrics: `{\"variant\": \"E1R_REGIME_AWARE_V0_2\"}`"
        },
        {
          "line": 116,
          "text": "  - `rows` length `8819` last_type `dict` keys `close, date, diagnostic_only, e1r_entry_type, e1r_uptrend_confirmed_eligible, e1r_uptrend_emerging_eligible, equity, leader_rank, leader_score, ma20, ma20_slope, ma50, ma50_slope, momentum_acceleration, momentum_score, reasons, rs_20d_impro`"
        },
        {
          "line": 117,
          "text": "  - `equity_curve` length `8819` last_type `dict` keys `close, date, diagnostic_only, e1r_entry_type, e1r_uptrend_confirmed_eligible, e1r_uptrend_emerging_eligible, equity, leader_rank, leader_score, ma20, ma20_slope, ma50, ma50_slope, momentum_acceleration, momentum_score, reasons, rs_20d_impro`"
        },
        {
          "line": 166,
          "text": "1. Use e1r_composer.extract_core_interval_returns and build_equity_records_from_returns if their signatures support existing E1R records."
        },
        {
          "line": 170,
          "text": "3. Validate final E1R metrics against frozen values: total_return_pct≈116.74, spx_return_pct≈76.84, alpha_pct≈39.90, max_drawdown_pct≈25.9."
        },
        {
          "line": 172,
          "text": "4. Only after validation, patch dashboard main equity chart to use exports/e1_e1r_5y_equity_comparison.json."
        }
      ],
      "counts": {
        "hits": 28
      }
    },
    {
      "path": "exports/e1r_unified_5y_full_account_v1_result.json",
      "sha256": "d62917d5591b511391d73ff532acffcb8aacca6daff6323030943c1c9ed04a44",
      "score": 120,
      "hits": [
        {
          "line": 7,
          "text": "  \"strategy_variant\": \"E1R_UNIFIED_5Y_FULL_ACCOUNT_V1\","
        },
        {
          "line": 30,
          "text": "    \"e1r_regime_wiring_enabled\": true,"
        },
        {
          "line": 31,
          "text": "    \"e1r_regime_source\": \"data/research/e1_5y/regimes/spx_regime_daily.json\","
        },
        {
          "line": 58,
          "text": "    \"variant\": \"D2_RISK_OFF_GATE\","
        },
        {
          "line": 60,
          "text": "    \"risk_off_rule\": \"disabled\","
        },
        {
          "line": 61,
          "text": "    \"market_shock_rule\": \"disabled\","
        },
        {
          "line": 73,
          "text": "      \"risk_off\": 465,"
        },
        {
          "line": 74,
          "text": "      \"market_shock\": 0,"
        },
        {
          "line": 109,
          "text": "    \"market_risk_off_block\": 49,"
        },
        {
          "line": 110,
          "text": "    \"market_shock_block\": 0,"
        },
        {
          "line": 120,
          "text": "    \"e1r_legacy_buy_blocked\": 14577,"
        },
        {
          "line": 121,
          "text": "    \"e1r_no_capacity\": 6319,"
        },
        {
          "line": 122,
          "text": "    \"e1r_candidate_buy_generated\": 10,"
        },
        {
          "line": 123,
          "text": "    \"e1r_emerging_to_confirmed_add\": 0,"
        },
        {
          "line": 128,
          "text": "  \"total_return_pct\": -100.0,"
        },
        {
          "line": 139,
          "text": "  \"spx_total_return_pct\": 76.84,"
        },
        {
          "line": 552,
          "text": "    115151.02,"
        },
        {
          "line": 615,
          "text": "    131115.69,"
        },
        {
          "line": 681,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 693,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 705,
          "text": "      \"market_gate_state\": \"RISK_OFF\","
        },
        {
          "line": 717,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 729,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 741,
          "text": "      \"market_gate_state\": \"RISK_OFF\","
        },
        {
          "line": 753,
          "text": "      \"market_gate_state\": \"RISK_OFF\","
        },
        {
          "line": 765,
          "text": "      \"market_gate_state\": \"RISK_OFF\","
        },
        {
          "line": 777,
          "text": "      \"market_gate_state\": \"RISK_OFF\","
        },
        {
          "line": 789,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 801,
          "text": "      \"market_gate_state\": \"RISK_OFF\","
        },
        {
          "line": 813,
          "text": "      \"market_gate_state\": \"RISK_OFF\","
        },
        {
          "line": 825,
          "text": "      \"market_gate_state\": \"RISK_OFF\","
        },
        {
          "line": 837,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 849,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 861,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 873,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 885,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 897,
          "text": "      \"market_gate_state\": \"RISK_OFF\","
        },
        {
          "line": 909,
          "text": "      \"market_gate_state\": \"RISK_OFF\","
        },
        {
          "line": 921,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 933,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 945,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 957,
          "text": "      \"market_gate_state\": \"RISK_OFF\","
        },
        {
          "line": 969,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 981,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 993,
          "text": "      \"market_gate_state\": \"RISK_OFF\","
        },
        {
          "line": 1005,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1017,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1029,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1041,
          "text": "      \"market_gate_state\": \"RISK_OFF\","
        },
        {
          "line": 1053,
          "text": "      \"market_gate_state\": \"RISK_OFF\","
        },
        {
          "line": 1065,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1077,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1089,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1101,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1113,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1125,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1137,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1149,
          "text": "      \"market_gate_state\": \"RISK_OFF\","
        },
        {
          "line": 1161,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1178,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1180,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1202,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1204,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1226,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1228,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1250,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1252,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1274,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1276,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1298,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1300,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1322,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1324,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1346,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1348,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1370,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1372,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1394,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1396,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1418,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1420,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1442,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1444,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1466,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1468,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1490,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1492,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1514,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1516,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1538,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1540,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1562,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1564,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1586,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1588,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1610,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1612,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1634,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1636,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1658,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1660,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1682,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1684,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1706,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1708,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1730,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1732,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1754,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1756,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1778,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1780,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1802,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1804,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1826,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1828,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1850,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1852,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1874,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1876,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1898,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1900,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1922,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1924,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1946,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1948,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1970,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1972,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 1994,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 1996,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 2018,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 2020,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 2042,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 2044,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 2066,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 2068,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 2090,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 2092,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 2114,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 2116,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 2138,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 2140,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 2162,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 2164,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 2186,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 2188,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 2210,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 2212,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 2234,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 2236,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 2258,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 2260,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 2282,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 2284,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 2306,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 2308,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 2330,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 2332,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 2354,
          "text": "      \"market_gate_state\": \"ALLOW\","
        },
        {
          "line": 2356,
          "text": "      \"e1r_active_mode\": \"UPTREND_EMERGING_CONFIRMED_ENABLED\","
        },
        {
          "line": 2378,
          "text": "      \"market_gate_state\": \"ALLOW\","
        }
      ],
      "counts": {
        "hits": 160
      }
    },
    {
      "path": "docs/research/E1R_V0_2_IMPLEMENTATION_MANIFEST.md",
      "sha256": "374817ced312943ec1db141d4831e4ed65c99fa4fc8157c9c9064e16030737eb",
      "score": 105,
      "hits": [
        {
          "line": 1,
          "text": "# E1R_REGIME_AWARE_V0_2 Implementation Manifest"
        },
        {
          "line": 5,
          "text": "Strategy ID: E1R_REGIME_AWARE_V0_2  "
        },
        {
          "line": 13,
          "text": "E1R_REGIME_AWARE_V0_2 is:"
        },
        {
          "line": 15,
          "text": "E1R_REGIME_AWARE_V0_1 core  "
        },
        {
          "line": 21,
          "text": "- UPTREND: use unchanged E1R_REGIME_AWARE_V0_1 logic."
        },
        {
          "line": 56,
          "text": "- src/engine/e1r_sidecar_sleeve.py"
        },
        {
          "line": 57,
          "text": "- src/engine/e1r_composer.py"
        },
        {
          "line": 62,
          "text": "- E1R_REGIME_AWARE_V0_1 is not modified."
        },
        {
          "line": 83,
          "text": "E1R_REGIME_AWARE_V0_1:"
        },
        {
          "line": 85,
          "text": "- Total Return: +105.61%"
        },
        {
          "line": 91,
          "text": "E1R_REGIME_AWARE_V0_2:"
        },
        {
          "line": 93,
          "text": "- Total Return: +116.7435999134756%"
        },
        {
          "line": 122,
          "text": "1. Do not modify E1R_REGIME_AWARE_V0_1 behavior."
        },
        {
          "line": 166,
          "text": "   - show E1R_REGIME_AWARE_V0_2"
        },
        {
          "line": 184,
          "text": "E1R_REGIME_AWARE_V0_2 is formally implemented as:"
        },
        {
          "line": 186,
          "text": "E1R_REGIME_AWARE_V0_1 core  "
        }
      ],
      "counts": {
        "hits": 16
      }
    }
  ]
}
```

## Unresolved
```json
[
  {
    "id": "full_115_artifact_missing_market_entry_gate",
    "field": "market_entry_gate",
    "blocking_for_replication": true
  },
  {
    "id": "full_115_artifact_missing_strategy_controls",
    "field": "strategy_controls",
    "blocking_for_replication": false
  },
  {
    "id": "full_115_artifact_missing_market_gate_enabled",
    "field": "market_gate_enabled",
    "blocking_for_replication": true
  },
  {
    "id": "full_115_artifact_missing_risk_off_below_spx_ma50",
    "field": "risk_off_below_spx_ma50",
    "blocking_for_replication": true
  },
  {
    "id": "full_115_artifact_missing_market_shock_gate_enabled",
    "field": "market_shock_gate_enabled",
    "blocking_for_replication": true
  },
  {
    "id": "full_115_artifact_missing_market_shock_daily_return",
    "field": "market_shock_daily_return",
    "blocking_for_replication": true
  },
  {
    "id": "full_115_artifact_missing_e1r_regime_wiring_enabled",
    "field": "e1r_regime_wiring_enabled",
    "blocking_for_replication": false
  },
  {
    "id": "full_115_artifact_missing_e1r_uptrend_execution_enabled",
    "field": "e1r_uptrend_execution_enabled",
    "blocking_for_replication": false
  }
]
```

## Validations
```json
{
  "market_state_115_return_artifact_audit_complete": true,
  "strategy_logic_changed": false,
  "audit_only": true,
  "formula_not_patched": true,
  "backtest_engine_run": false,
  "short_window_existing_engine_run": false,
  "full_5y_backtest_run": false,
  "forward_runner_run": false,
  "candidate_generation_extracted": false,
  "buy_add_reduce_exit_extracted": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "strategy_files_unchanged": true,
  "k2_r8_loaded": true,
  "repo_artifacts_searched": true,
  "json_artifact_found": true,
  "text_artifact_found": true,
  "target_return_116_74_verified": true,
  "metric_snapshot_extracted": true,
  "market_param_compare_complete": true,
  "unresolved_count": 8
}
```

## Decision
```json
{
  "k2_r9_market_state_115_return_artifact_audit_passed": true,
  "full_115_artifact_verified": true,
  "market_state_115_replication_ready": false,
  "formula_patch_allowed_now": false,
  "candidate_extraction_allowed_now": false,
  "implementation_may_resume": false,
  "unresolved": [
    {
      "id": "full_115_artifact_missing_market_entry_gate",
      "field": "market_entry_gate",
      "blocking_for_replication": true
    },
    {
      "id": "full_115_artifact_missing_strategy_controls",
      "field": "strategy_controls",
      "blocking_for_replication": false
    },
    {
      "id": "full_115_artifact_missing_market_gate_enabled",
      "field": "market_gate_enabled",
      "blocking_for_replication": true
    },
    {
      "id": "full_115_artifact_missing_risk_off_below_spx_ma50",
      "field": "risk_off_below_spx_ma50",
      "blocking_for_replication": true
    },
    {
      "id": "full_115_artifact_missing_market_shock_gate_enabled",
      "field": "market_shock_gate_enabled",
      "blocking_for_replication": true
    },
    {
      "id": "full_115_artifact_missing_market_shock_daily_return",
      "field": "market_shock_daily_return",
      "blocking_for_replication": true
    },
    {
      "id": "full_115_artifact_missing_e1r_regime_wiring_enabled",
      "field": "e1r_regime_wiring_enabled",
      "blocking_for_replication": false
    },
    {
      "id": "full_115_artifact_missing_e1r_uptrend_execution_enabled",
      "field": "e1r_uptrend_execution_enabled",
      "blocking_for_replication": false
    }
  ],
  "next_required_stage_if_ready": "4C-2C-4E-ENGINE-K2-R10-MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL",
  "next_required_stage_if_not_ready": "4C-2C-4E-ENGINE-K2-R9B-115_RETURN_ARTIFACT_RECOVERY",
  "conclusion": "K2_R9_AUDIT_COMPLETE_NEEDS_115_ARTIFACT_RECOVERY_OR_PARAM_EVIDENCE",
  "recommended_next_action": "If the 116.74% JSON artifact and market parameters are verified, proceed to replication proposal. If not, recover the exact E1R 115% artifact or run only an artifact-producing audit, not optimization."
}
```
