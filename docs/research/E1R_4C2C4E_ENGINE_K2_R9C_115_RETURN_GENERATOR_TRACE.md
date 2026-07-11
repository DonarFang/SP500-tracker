# E1R 4C-2C-4E-ENGINE-K2-R9C — 115 Return Generator Trace

Generated At: `2026-07-11T02:19:30.999814+00:00`

## Purpose
Trace the real generator/call-chain evidence for the E1R v0.2 116.74% artifact, excluding self-reference audit pollution.

## Target Artifact
```json
{
  "exists": true,
  "path": "exports/e1r_v0_2_backtest_summary.json",
  "sha256": "449a8ace55ce2335d174e17e2532d8793a3a9b99c021a935f8d7f2e531092114",
  "selected_fields": {
    "strategy_id": "E1R_REGIME_AWARE_V0_2",
    "total_return_pct": 116.7435999134756,
    "spx_return_pct": 76.844174428316,
    "alpha_pct": 39.89942548515961,
    "max_drawdown_pct": 25.904809362815108,
    "profit_factor": 1.1919630955509348,
    "sharpe_ratio": 0.7957270568329264,
    "regime_aware_logic": "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
    "sidecar_active_by_regime": {
      "SIDEWAYS": 135
    },
    "sidecar_active_by_subclass": {
      "MA_CONFLICT": 135
    },
    "variant": "E1R_REGIME_AWARE_V0_2",
    "source_file": "exports/e1r_v0_2_backtest_summary.json"
  }
}
```

## Generator Trace JSON Relevant Rows
```json
{
  "relevant_row_count": 8747,
  "rows": [
    {
      "path": "generator_candidates",
      "key": "generator_candidates",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json",
        "run_stateful_simulation",
        "build_e1r_sidecar_sleeve",
        "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
        "sidecar_active_by_regime",
        "sidecar_active_by_subclass"
      ],
      "value": "[{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json\", \"generator_score\": 166, \"base_score\": 108, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"extract_core_interval_returns\", \"run_stateful_simulation\", \"run_strategy_variant_comparison\", \"sidecar_result\", \"variant_results\", \"write_json\"], \"hits\": [{\"line\": 7, \"matched\": [\"export\"], \"context\": [{\"line\": 5, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 6, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 7, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 8, \"text\": \"    \\\"workflow_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"strategy_logic_changed\\\": false,\"}]}, {\"line\": 79, \"matched\": [\"extract_core_interval_returns\"], \"context\": [{\"line\": 77, \"text\": \"        },\"}, {\"line\": 78, \"text\": \"        {\"}, {\"line\": 79, \"text\": \"          \\\"name\\\": \\\"extract_core_interval_returns\\\",\"}, {\"line\": 80, \"text\": \"          \\\"line\\\": 94,\"}, {\"line\": 81, \"text\": \"          \\\"args\\\": [\"}]}, {\"line\": 82, \"matched\": [\"daily_equity_records\"], \"context\": [{\"line\": 80, \"text\": \"          \\\"line\\\": 94,\"}, {\"line\": 81, \"text\": \"          \\\"args\\\": [\"}, {\"line\": 82, \"text\": \"            \\\"core_daily_equity_records\\\",\"}, {\"line\": 83, \"text\": \"            \\\"sidecar_records\\\"\"}, {\"line\": 84, \"text\": \"          ],\"}]}, {\"line\": 90, \"matched\": [\"build_equity_records_from_returns\"], \"context\": [{\"line\": 88, \"text\"...<truncated>"
    },
    {
      "path": "generator_candidates[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json",
        "run_stateful_simulation",
        "build_e1r_sidecar_sleeve"
      ],
      "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json\", \"generator_score\": 166, \"base_score\": 108, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"extract_core_interval_returns\", \"run_stateful_simulation\", \"run_strategy_variant_comparison\", \"sidecar_result\", \"variant_results\", \"write_json\"], \"hits\": [{\"line\": 7, \"matched\": [\"export\"], \"context\": [{\"line\": 5, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 6, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 7, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 8, \"text\": \"    \\\"workflow_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"strategy_logic_changed\\\": false,\"}]}, {\"line\": 79, \"matched\": [\"extract_core_interval_returns\"], \"context\": [{\"line\": 77, \"text\": \"        },\"}, {\"line\": 78, \"text\": \"        {\"}, {\"line\": 79, \"text\": \"          \\\"name\\\": \\\"extract_core_interval_returns\\\",\"}, {\"line\": 80, \"text\": \"          \\\"line\\\": 94,\"}, {\"line\": 81, \"text\": \"          \\\"args\\\": [\"}]}, {\"line\": 82, \"matched\": [\"daily_equity_records\"], \"context\": [{\"line\": 80, \"text\": \"          \\\"line\\\": 94,\"}, {\"line\": 81, \"text\": \"          \\\"args\\\": [\"}, {\"line\": 82, \"text\": \"            \\\"core_daily_equity_records\\\",\"}, {\"line\": 83, \"text\": \"            \\\"sidecar_records\\\"\"}, {\"line\": 84, \"text\": \"          ],\"}]}, {\"line\": 90, \"matched\": [\"build_equity_records_from_returns\"], \"context\": [{\"line\": 88, \"text\":...<truncated>"
    },
    {
      "path": "generator_candidates[0].matched_terms",
      "key": "matched_terms",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json",
        "run_stateful_simulation",
        "build_e1r_sidecar_sleeve"
      ],
      "value": [
        "0.7957270568329264",
        "1.1919630955509348",
        "116.7435999134756",
        "25.904809362815108",
        "39.89942548515961",
        "76.844174428316",
        "E1R_REGIME_AWARE_V0_2",
        "build_e1r_sidecar_sleeve",
        "build_equity_records_from_returns",
        "compose_e1r_v0_2_variant",
        "core_variant_result",
        "daily_equity_records",
        "daily_records",
        "e1r_v0_2",
        "e1r_v0_2_backtest_equity_curve.json",
        "e1r_v0_2_backtest_summary.json",
        "equity_curve",
        "export",
        "extract_core_interval_returns",
        "run_stateful_simulation",
        "run_strategy_variant_comparison",
        "sidecar_result",
        "variant_results",
        "write_json"
      ]
    },
    {
      "path": "generator_candidates[0].matched_terms[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[0].matched_terms[6]",
      "key": "[6]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[0].matched_terms[7]",
      "key": "[7]",
      "matched": [
        "build_e1r_sidecar_sleeve"
      ],
      "value": "build_e1r_sidecar_sleeve"
    },
    {
      "path": "generator_candidates[0].matched_terms[15]",
      "key": "[15]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "e1r_v0_2_backtest_summary.json"
    },
    {
      "path": "generator_candidates[0].matched_terms[19]",
      "key": "[19]",
      "matched": [
        "run_stateful_simulation"
      ],
      "value": "run_stateful_simulation"
    },
    {
      "path": "generator_candidates[0].hits",
      "key": "hits",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "[{\"line\": 7, \"matched\": [\"export\"], \"context\": [{\"line\": 5, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 6, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 7, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 8, \"text\": \"    \\\"workflow_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"strategy_logic_changed\\\": false,\"}]}, {\"line\": 79, \"matched\": [\"extract_core_interval_returns\"], \"context\": [{\"line\": 77, \"text\": \"        },\"}, {\"line\": 78, \"text\": \"        {\"}, {\"line\": 79, \"text\": \"          \\\"name\\\": \\\"extract_core_interval_returns\\\",\"}, {\"line\": 80, \"text\": \"          \\\"line\\\": 94,\"}, {\"line\": 81, \"text\": \"          \\\"args\\\": [\"}]}, {\"line\": 82, \"matched\": [\"daily_equity_records\"], \"context\": [{\"line\": 80, \"text\": \"          \\\"line\\\": 94,\"}, {\"line\": 81, \"text\": \"          \\\"args\\\": [\"}, {\"line\": 82, \"text\": \"            \\\"core_daily_equity_records\\\",\"}, {\"line\": 83, \"text\": \"            \\\"sidecar_records\\\"\"}, {\"line\": 84, \"text\": \"          ],\"}]}, {\"line\": 90, \"matched\": [\"build_equity_records_from_returns\"], \"context\": [{\"line\": 88, \"text\": \"        },\"}, {\"line\": 89, \"text\": \"        {\"}, {\"line\": 90, \"text\": \"          \\\"name\\\": \\\"build_equity_records_from_returns\\\",\"}, {\"line\": 91, \"text\": \"          \\\"line\\\": 171,\"}, {\"line\": 92, \"text\": \"          \\\"args\\\": [\"}]}, {\"line\": 113, \"matched\": [\"e1r_v0_2\", \"compose_e1r_v0_2_variant\"], \"context\": [{\"line\": 111, \"text\": \"        },\"}, {\"line\": 112, \"text\": \"        {\"}, {\"line\": 113, \"text\": \"          \\\"name\\\": \\\"compose_e1r_v0_2_variant\\\",\"}, {\"line\": 114, \"text\": \"          \\\"line\\\": 283,\"}, {\"line\": 115, \"text\": \"          \\\"args\\\": [\"}]}, {\"line\": 116, \"matched\": [\"core_variant_result\"], \"context\": [{\"line\": 114, \"text\": \"          \\\"line\\\": 283,\"}, {\"line\": 115, \"text\": \"          \\\"args\\\": [\"}, {\"line\": 116, ...<truncated>"
    },
    {
      "path": "generator_candidates[0].hits[10]",
      "key": "[10]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 206,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 204,
            "text": "          \"line\": 9,"
          },
          {
            "line": 205,
            "text": "          \"terms\": ["
          },
          {
            "line": 206,
            "text": "            \"E1R_REGIME_AWARE_V0_2\""
          },
          {
            "line": 207,
            "text": "          ],"
          },
          {
            "line": 208,
            "text": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
          }
        ]
      }
    },
    {
      "path": "generator_candidates[0].hits[10].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[0].hits[10].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[0].hits[10].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 204,
          "text": "          \"line\": 9,"
        },
        {
          "line": 205,
          "text": "          \"terms\": ["
        },
        {
          "line": 206,
          "text": "            \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "line": 207,
          "text": "          ],"
        },
        {
          "line": 208,
          "text": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
        }
      ]
    },
    {
      "path": "generator_candidates[0].hits[10].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 206,
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      }
    },
    {
      "path": "generator_candidates[0].hits[10].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "            \"E1R_REGIME_AWARE_V0_2\""
    },
    {
      "path": "generator_candidates[0].hits[10].context[4]",
      "key": "[4]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 208,
        "text": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
      }
    },
    {
      "path": "generator_candidates[0].hits[10].context[4].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
    },
    {
      "path": "generator_candidates[0].hits[11]",
      "key": "[11]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 208,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 206,
            "text": "            \"E1R_REGIME_AWARE_V0_2\""
          },
          {
            "line": 207,
            "text": "          ],"
          },
          {
            "line": 208,
            "text": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
          },
          {
            "line": 209,
            "text": "        },"
          },
          {
            "line": 210,
            "text": "        {"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[0].hits[11].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[0].hits[11].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[0].hits[11].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 206,
          "text": "            \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "line": 207,
          "text": "          ],"
        },
        {
          "line": 208,
          "text": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
        },
        {
          "line": 209,
          "text": "        },"
        },
        {
          "line": 210,
          "text": "        {"
        }
      ]
    },
    {
      "path": "generator_candidates[0].hits[11].context[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 206,
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      }
    },
    {
      "path": "generator_candidates[0].hits[11].context[0].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "            \"E1R_REGIME_AWARE_V0_2\""
    },
    {
      "path": "generator_candidates[0].hits[11].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 208,
        "text": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
      }
    },
    {
      "path": "generator_candidates[0].hits[11].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
    },
    {
      "path": "generator_candidates[0].hits[27]",
      "key": "[27]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 297,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 295,
            "text": "          \"line\": 300,"
          },
          {
            "line": 296,
            "text": "          \"terms\": ["
          },
          {
            "line": 297,
            "text": "            \"E1R_REGIME_AWARE_V0_2\""
          },
          {
            "line": 298,
            "text": "          ],"
          },
          {
            "line": 299,
            "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
          }
        ]
      }
    },
    {
      "path": "generator_candidates[0].hits[27].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[0].hits[27].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[0].hits[27].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 295,
          "text": "          \"line\": 300,"
        },
        {
          "line": 296,
          "text": "          \"terms\": ["
        },
        {
          "line": 297,
          "text": "            \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "line": 298,
          "text": "          ],"
        },
        {
          "line": 299,
          "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
        }
      ]
    },
    {
      "path": "generator_candidates[0].hits[27].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 297,
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      }
    },
    {
      "path": "generator_candidates[0].hits[27].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "            \"E1R_REGIME_AWARE_V0_2\""
    },
    {
      "path": "generator_candidates[0].hits[27].context[4]",
      "key": "[4]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 299,
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      }
    },
    {
      "path": "generator_candidates[0].hits[27].context[4].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
    },
    {
      "path": "generator_candidates[0].hits[28]",
      "key": "[28]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 299,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 297,
            "text": "            \"E1R_REGIME_AWARE_V0_2\""
          },
          {
            "line": 298,
            "text": "          ],"
          },
          {
            "line": 299,
            "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
          },
          {
            "line": 300,
            "text": "        },"
          },
          {
            "line": 301,
            "text": "        {"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[0].hits[28].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[0].hits[28].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[0].hits[28].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 297,
          "text": "            \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "line": 298,
          "text": "          ],"
        },
        {
          "line": 299,
          "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
        },
        {
          "line": 300,
          "text": "        },"
        },
        {
          "line": 301,
          "text": "        {"
        }
      ]
    },
    {
      "path": "generator_candidates[0].hits[28].context[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 297,
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      }
    },
    {
      "path": "generator_candidates[0].hits[28].context[0].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "            \"E1R_REGIME_AWARE_V0_2\""
    },
    {
      "path": "generator_candidates[0].hits[28].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 299,
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      }
    },
    {
      "path": "generator_candidates[0].hits[28].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
    },
    {
      "path": "generator_candidates[1]",
      "key": "[1]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json",
        "run_stateful_simulation",
        "build_e1r_sidecar_sleeve"
      ],
      "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\", \"generator_score\": 166, \"base_score\": 108, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"extract_core_interval_returns\", \"run_stateful_simulation\", \"run_strategy_variant_comparison\", \"sidecar_result\", \"variant_results\", \"write_json\"], \"hits\": [{\"line\": 7, \"matched\": [\"export\"], \"context\": [{\"line\": 5, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 6, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 7, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 8, \"text\": \"    \\\"workflow_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"strategy_logic_changed\\\": false,\"}]}, {\"line\": 10, \"matched\": [\"export\"], \"context\": [{\"line\": 8, \"text\": \"    \\\"workflow_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"strategy_logic_changed\\\": false,\"}, {\"line\": 10, \"text\": \"    \\\"canonical_exports_written\\\": false,\"}, {\"line\": 11, \"text\": \"    \\\"long_backtest_run\\\": false\"}, {\"line\": 12, \"text\": \"  },\"}]}, {\"line\": 27, \"matched\": [\"E1R_REGIME_AWARE_V0_2\"], \"context\": [{\"line\": 25, \"text\": \"          \\\"line\\\": 9,\"}, {\"line\": 26, \"text\": \"          \\\"terms\\\": [\"}, {\"line\": 27, \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\"}, {\"line\": 28, \"text\": \"          ],\"}, {\"line\": 29, \"text\": \"          \\\"text\\\": \\\"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\\\"\"}]}, {\"line\": 29, \"matched\": [\"E1R_REGIME_AWARE_V0_2\"], \"co...<truncated>"
    },
    {
      "path": "generator_candidates[1].matched_terms",
      "key": "matched_terms",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json",
        "run_stateful_simulation",
        "build_e1r_sidecar_sleeve"
      ],
      "value": [
        "0.7957270568329264",
        "1.1919630955509348",
        "116.7435999134756",
        "25.904809362815108",
        "39.89942548515961",
        "76.844174428316",
        "E1R_REGIME_AWARE_V0_2",
        "build_e1r_sidecar_sleeve",
        "build_equity_records_from_returns",
        "compose_e1r_v0_2_variant",
        "core_variant_result",
        "daily_equity_records",
        "daily_records",
        "e1r_v0_2",
        "e1r_v0_2_backtest_equity_curve.json",
        "e1r_v0_2_backtest_summary.json",
        "equity_curve",
        "export",
        "extract_core_interval_returns",
        "run_stateful_simulation",
        "run_strategy_variant_comparison",
        "sidecar_result",
        "variant_results",
        "write_json"
      ]
    },
    {
      "path": "generator_candidates[1].matched_terms[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[1].matched_terms[6]",
      "key": "[6]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[1].matched_terms[7]",
      "key": "[7]",
      "matched": [
        "build_e1r_sidecar_sleeve"
      ],
      "value": "build_e1r_sidecar_sleeve"
    },
    {
      "path": "generator_candidates[1].matched_terms[15]",
      "key": "[15]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "e1r_v0_2_backtest_summary.json"
    },
    {
      "path": "generator_candidates[1].matched_terms[19]",
      "key": "[19]",
      "matched": [
        "run_stateful_simulation"
      ],
      "value": "run_stateful_simulation"
    },
    {
      "path": "generator_candidates[1].hits",
      "key": "hits",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "[{\"line\": 7, \"matched\": [\"export\"], \"context\": [{\"line\": 5, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 6, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 7, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 8, \"text\": \"    \\\"workflow_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"strategy_logic_changed\\\": false,\"}]}, {\"line\": 10, \"matched\": [\"export\"], \"context\": [{\"line\": 8, \"text\": \"    \\\"workflow_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"strategy_logic_changed\\\": false,\"}, {\"line\": 10, \"text\": \"    \\\"canonical_exports_written\\\": false,\"}, {\"line\": 11, \"text\": \"    \\\"long_backtest_run\\\": false\"}, {\"line\": 12, \"text\": \"  },\"}]}, {\"line\": 27, \"matched\": [\"E1R_REGIME_AWARE_V0_2\"], \"context\": [{\"line\": 25, \"text\": \"          \\\"line\\\": 9,\"}, {\"line\": 26, \"text\": \"          \\\"terms\\\": [\"}, {\"line\": 27, \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\"}, {\"line\": 28, \"text\": \"          ],\"}, {\"line\": 29, \"text\": \"          \\\"text\\\": \\\"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\\\"\"}]}, {\"line\": 29, \"matched\": [\"E1R_REGIME_AWARE_V0_2\"], \"context\": [{\"line\": 27, \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\"}, {\"line\": 28, \"text\": \"          ],\"}, {\"line\": 29, \"text\": \"          \\\"text\\\": \\\"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\\\"\"}, {\"line\": 30, \"text\": \"        },\"}, {\"line\": 31, \"text\": \"        {\"}]}, {\"line\": 62, \"matched\": [\"extract_core_interval_returns\"], \"context\": [{\"line\": 60, \"text\": \"          \\\"line\\\": 94,\"}, {\"line\": 61, \"text\": \"          \\\"terms\\\": [\"}, {\"line\": 62, \"text\": \"            \\\"extract_core_interval_returns\\\"\"}, {\"line\": 63, \"text\": \"          ],\"}, {\"line\": 64, \"text\": \"          \\\"text\\\": \\\"def extract_core_interval_returns(\\\"\"}]}, {\"line\": 64, \"matched\": [\"extract_core_interval_returns\"], \"context\":...<truncated>"
    },
    {
      "path": "generator_candidates[1].hits[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 27,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 25,
            "text": "          \"line\": 9,"
          },
          {
            "line": 26,
            "text": "          \"terms\": ["
          },
          {
            "line": 27,
            "text": "            \"E1R_REGIME_AWARE_V0_2\""
          },
          {
            "line": 28,
            "text": "          ],"
          },
          {
            "line": 29,
            "text": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
          }
        ]
      }
    },
    {
      "path": "generator_candidates[1].hits[2].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[1].hits[2].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[1].hits[2].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 25,
          "text": "          \"line\": 9,"
        },
        {
          "line": 26,
          "text": "          \"terms\": ["
        },
        {
          "line": 27,
          "text": "            \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "line": 28,
          "text": "          ],"
        },
        {
          "line": 29,
          "text": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
        }
      ]
    },
    {
      "path": "generator_candidates[1].hits[2].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 27,
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      }
    },
    {
      "path": "generator_candidates[1].hits[2].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "            \"E1R_REGIME_AWARE_V0_2\""
    },
    {
      "path": "generator_candidates[1].hits[2].context[4]",
      "key": "[4]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 29,
        "text": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
      }
    },
    {
      "path": "generator_candidates[1].hits[2].context[4].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
    },
    {
      "path": "generator_candidates[1].hits[3]",
      "key": "[3]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 29,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 27,
            "text": "            \"E1R_REGIME_AWARE_V0_2\""
          },
          {
            "line": 28,
            "text": "          ],"
          },
          {
            "line": 29,
            "text": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
          },
          {
            "line": 30,
            "text": "        },"
          },
          {
            "line": 31,
            "text": "        {"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[1].hits[3].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[1].hits[3].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[1].hits[3].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 27,
          "text": "            \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "line": 28,
          "text": "          ],"
        },
        {
          "line": 29,
          "text": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
        },
        {
          "line": 30,
          "text": "        },"
        },
        {
          "line": 31,
          "text": "        {"
        }
      ]
    },
    {
      "path": "generator_candidates[1].hits[3].context[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 27,
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      }
    },
    {
      "path": "generator_candidates[1].hits[3].context[0].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "            \"E1R_REGIME_AWARE_V0_2\""
    },
    {
      "path": "generator_candidates[1].hits[3].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 29,
        "text": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
      }
    },
    {
      "path": "generator_candidates[1].hits[3].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
    },
    {
      "path": "generator_candidates[1].hits[18]",
      "key": "[18]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 594,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 592,
            "text": "          \"line\": 300,"
          },
          {
            "line": 593,
            "text": "          \"terms\": ["
          },
          {
            "line": 594,
            "text": "            \"E1R_REGIME_AWARE_V0_2\""
          },
          {
            "line": 595,
            "text": "          ],"
          },
          {
            "line": 596,
            "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
          }
        ]
      }
    },
    {
      "path": "generator_candidates[1].hits[18].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[1].hits[18].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[1].hits[18].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 592,
          "text": "          \"line\": 300,"
        },
        {
          "line": 593,
          "text": "          \"terms\": ["
        },
        {
          "line": 594,
          "text": "            \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "line": 595,
          "text": "          ],"
        },
        {
          "line": 596,
          "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
        }
      ]
    },
    {
      "path": "generator_candidates[1].hits[18].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 594,
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      }
    },
    {
      "path": "generator_candidates[1].hits[18].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "            \"E1R_REGIME_AWARE_V0_2\""
    },
    {
      "path": "generator_candidates[1].hits[18].context[4]",
      "key": "[4]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 596,
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      }
    },
    {
      "path": "generator_candidates[1].hits[18].context[4].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
    },
    {
      "path": "generator_candidates[1].hits[19]",
      "key": "[19]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 596,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 594,
            "text": "            \"E1R_REGIME_AWARE_V0_2\""
          },
          {
            "line": 595,
            "text": "          ],"
          },
          {
            "line": 596,
            "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
          },
          {
            "line": 597,
            "text": "        },"
          },
          {
            "line": 598,
            "text": "        {"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[1].hits[19].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[1].hits[19].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[1].hits[19].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 594,
          "text": "            \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "line": 595,
          "text": "          ],"
        },
        {
          "line": 596,
          "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
        },
        {
          "line": 597,
          "text": "        },"
        },
        {
          "line": 598,
          "text": "        {"
        }
      ]
    },
    {
      "path": "generator_candidates[1].hits[19].context[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 594,
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      }
    },
    {
      "path": "generator_candidates[1].hits[19].context[0].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "            \"E1R_REGIME_AWARE_V0_2\""
    },
    {
      "path": "generator_candidates[1].hits[19].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 596,
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      }
    },
    {
      "path": "generator_candidates[1].hits[19].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
    },
    {
      "path": "generator_candidates[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json",
        "run_stateful_simulation",
        "build_e1r_sidecar_sleeve"
      ],
      "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json\", \"generator_score\": 161, \"base_score\": 103, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"extract_core_interval_returns\", \"run_stateful_simulation\", \"run_strategy_variant_comparison\", \"sidecar_result\", \"variant_results\", \"write_json\"], \"hits\": [{\"line\": 14, \"matched\": [\"116.7435999134756\"], \"context\": [{\"line\": 12, \"text\": \"  },\"}, {\"line\": 13, \"text\": \"  \\\"e1r_frozen_targets\\\": {\"}, {\"line\": 14, \"text\": \"    \\\"total_return_pct\\\": 116.7435999134756,\"}, {\"line\": 15, \"text\": \"    \\\"spx_return_pct\\\": 76.844174428316,\"}, {\"line\": 16, \"text\": \"    \\\"alpha_pct\\\": 39.89942548515961,\"}]}, {\"line\": 15, \"matched\": [\"76.844174428316\"], \"context\": [{\"line\": 13, \"text\": \"  \\\"e1r_frozen_targets\\\": {\"}, {\"line\": 14, \"text\": \"    \\\"total_return_pct\\\": 116.7435999134756,\"}, {\"line\": 15, \"text\": \"    \\\"spx_return_pct\\\": 76.844174428316,\"}, {\"line\": 16, \"text\": \"    \\\"alpha_pct\\\": 39.89942548515961,\"}, {\"line\": 17, \"text\": \"    \\\"max_drawdown_pct\\\": 25.904809362815108,\"}]}, {\"line\": 16, \"matched\": [\"39.89942548515961\"], \"context\": [{\"line\": 14, \"text\": \"    \\\"total_return_pct\\\": 116.7435999134756,\"}, {\"line\": 15, \"text\": \"    \\\"spx_return_pct\\\": 76.844174428316,\"}, {\"line\": 16, \"text\": \"    \\\"alpha_pct\\\": 39.89942548515961,\"}, {\"line\": 17, \"text\": \"    \\\"max_drawdown_pct\\\": 25.904809362815108,\"}, {\"line\": 18, \"text\": \"    \\\"profit_factor\\\": 1.191963095550...<truncated>"
    },
    {
      "path": "generator_candidates[2].matched_terms",
      "key": "matched_terms",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json",
        "run_stateful_simulation",
        "build_e1r_sidecar_sleeve"
      ],
      "value": [
        "0.7957270568329264",
        "1.1919630955509348",
        "116.7435999134756",
        "25.904809362815108",
        "39.89942548515961",
        "76.844174428316",
        "E1R_REGIME_AWARE_V0_2",
        "build_e1r_sidecar_sleeve",
        "build_equity_records_from_returns",
        "compose_e1r_v0_2_variant",
        "core_variant_result",
        "daily_equity_records",
        "daily_records",
        "e1r_v0_2",
        "e1r_v0_2_backtest_summary.json",
        "equity_curve",
        "export",
        "extract_core_interval_returns",
        "run_stateful_simulation",
        "run_strategy_variant_comparison",
        "sidecar_result",
        "variant_results",
        "write_json"
      ]
    },
    {
      "path": "generator_candidates[2].matched_terms[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[2].matched_terms[6]",
      "key": "[6]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[2].matched_terms[7]",
      "key": "[7]",
      "matched": [
        "build_e1r_sidecar_sleeve"
      ],
      "value": "build_e1r_sidecar_sleeve"
    },
    {
      "path": "generator_candidates[2].matched_terms[14]",
      "key": "[14]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "e1r_v0_2_backtest_summary.json"
    },
    {
      "path": "generator_candidates[2].matched_terms[18]",
      "key": "[18]",
      "matched": [
        "run_stateful_simulation"
      ],
      "value": "run_stateful_simulation"
    },
    {
      "path": "generator_candidates[2].hits",
      "key": "hits",
      "matched": [
        "116.7435999134756"
      ],
      "value": "[{\"line\": 14, \"matched\": [\"116.7435999134756\"], \"context\": [{\"line\": 12, \"text\": \"  },\"}, {\"line\": 13, \"text\": \"  \\\"e1r_frozen_targets\\\": {\"}, {\"line\": 14, \"text\": \"    \\\"total_return_pct\\\": 116.7435999134756,\"}, {\"line\": 15, \"text\": \"    \\\"spx_return_pct\\\": 76.844174428316,\"}, {\"line\": 16, \"text\": \"    \\\"alpha_pct\\\": 39.89942548515961,\"}]}, {\"line\": 15, \"matched\": [\"76.844174428316\"], \"context\": [{\"line\": 13, \"text\": \"  \\\"e1r_frozen_targets\\\": {\"}, {\"line\": 14, \"text\": \"    \\\"total_return_pct\\\": 116.7435999134756,\"}, {\"line\": 15, \"text\": \"    \\\"spx_return_pct\\\": 76.844174428316,\"}, {\"line\": 16, \"text\": \"    \\\"alpha_pct\\\": 39.89942548515961,\"}, {\"line\": 17, \"text\": \"    \\\"max_drawdown_pct\\\": 25.904809362815108,\"}]}, {\"line\": 16, \"matched\": [\"39.89942548515961\"], \"context\": [{\"line\": 14, \"text\": \"    \\\"total_return_pct\\\": 116.7435999134756,\"}, {\"line\": 15, \"text\": \"    \\\"spx_return_pct\\\": 76.844174428316,\"}, {\"line\": 16, \"text\": \"    \\\"alpha_pct\\\": 39.89942548515961,\"}, {\"line\": 17, \"text\": \"    \\\"max_drawdown_pct\\\": 25.904809362815108,\"}, {\"line\": 18, \"text\": \"    \\\"profit_factor\\\": 1.1919630955509348,\"}]}, {\"line\": 17, \"matched\": [\"25.904809362815108\"], \"context\": [{\"line\": 15, \"text\": \"    \\\"spx_return_pct\\\": 76.844174428316,\"}, {\"line\": 16, \"text\": \"    \\\"alpha_pct\\\": 39.89942548515961,\"}, {\"line\": 17, \"text\": \"    \\\"max_drawdown_pct\\\": 25.904809362815108,\"}, {\"line\": 18, \"text\": \"    \\\"profit_factor\\\": 1.1919630955509348,\"}, {\"line\": 19, \"text\": \"    \\\"sharpe_ratio\\\": 0.7957270568329264,\"}]}, {\"line\": 18, \"matched\": [\"1.1919630955509348\"], \"context\": [{\"line\": 16, \"text\": \"    \\\"alpha_pct\\\": 39.89942548515961,\"}, {\"line\": 17, \"text\": \"    \\\"max_drawdown_pct\\\": 25.904809362815108,\"}, {\"line\": 18, \"text\": \"    \\\"profit_factor\\\": 1.1919630955509348,\"}, {\"line\": 19, \"te...<truncated>"
    },
    {
      "path": "generator_candidates[2].hits[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 14,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 12,
            "text": "  },"
          },
          {
            "line": 13,
            "text": "  \"e1r_frozen_targets\": {"
          },
          {
            "line": 14,
            "text": "    \"total_return_pct\": 116.7435999134756,"
          },
          {
            "line": 15,
            "text": "    \"spx_return_pct\": 76.844174428316,"
          },
          {
            "line": 16,
            "text": "    \"alpha_pct\": 39.89942548515961,"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[2].hits[0].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[2].hits[0].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[2].hits[0].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 12,
          "text": "  },"
        },
        {
          "line": 13,
          "text": "  \"e1r_frozen_targets\": {"
        },
        {
          "line": 14,
          "text": "    \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 15,
          "text": "    \"spx_return_pct\": 76.844174428316,"
        },
        {
          "line": 16,
          "text": "    \"alpha_pct\": 39.89942548515961,"
        }
      ]
    },
    {
      "path": "generator_candidates[2].hits[0].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 14,
        "text": "    \"total_return_pct\": 116.7435999134756,"
      }
    },
    {
      "path": "generator_candidates[2].hits[0].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "    \"total_return_pct\": 116.7435999134756,"
    },
    {
      "path": "generator_candidates[2].hits[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 15,
        "matched": [
          "76.844174428316"
        ],
        "context": [
          {
            "line": 13,
            "text": "  \"e1r_frozen_targets\": {"
          },
          {
            "line": 14,
            "text": "    \"total_return_pct\": 116.7435999134756,"
          },
          {
            "line": 15,
            "text": "    \"spx_return_pct\": 76.844174428316,"
          },
          {
            "line": 16,
            "text": "    \"alpha_pct\": 39.89942548515961,"
          },
          {
            "line": 17,
            "text": "    \"max_drawdown_pct\": 25.904809362815108,"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[2].hits[1].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 13,
          "text": "  \"e1r_frozen_targets\": {"
        },
        {
          "line": 14,
          "text": "    \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 15,
          "text": "    \"spx_return_pct\": 76.844174428316,"
        },
        {
          "line": 16,
          "text": "    \"alpha_pct\": 39.89942548515961,"
        },
        {
          "line": 17,
          "text": "    \"max_drawdown_pct\": 25.904809362815108,"
        }
      ]
    },
    {
      "path": "generator_candidates[2].hits[1].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 14,
        "text": "    \"total_return_pct\": 116.7435999134756,"
      }
    },
    {
      "path": "generator_candidates[2].hits[1].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "    \"total_return_pct\": 116.7435999134756,"
    },
    {
      "path": "generator_candidates[2].hits[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 16,
        "matched": [
          "39.89942548515961"
        ],
        "context": [
          {
            "line": 14,
            "text": "    \"total_return_pct\": 116.7435999134756,"
          },
          {
            "line": 15,
            "text": "    \"spx_return_pct\": 76.844174428316,"
          },
          {
            "line": 16,
            "text": "    \"alpha_pct\": 39.89942548515961,"
          },
          {
            "line": 17,
            "text": "    \"max_drawdown_pct\": 25.904809362815108,"
          },
          {
            "line": 18,
            "text": "    \"profit_factor\": 1.1919630955509348,"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[2].hits[2].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 14,
          "text": "    \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 15,
          "text": "    \"spx_return_pct\": 76.844174428316,"
        },
        {
          "line": 16,
          "text": "    \"alpha_pct\": 39.89942548515961,"
        },
        {
          "line": 17,
          "text": "    \"max_drawdown_pct\": 25.904809362815108,"
        },
        {
          "line": 18,
          "text": "    \"profit_factor\": 1.1919630955509348,"
        }
      ]
    },
    {
      "path": "generator_candidates[2].hits[2].context[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 14,
        "text": "    \"total_return_pct\": 116.7435999134756,"
      }
    },
    {
      "path": "generator_candidates[2].hits[2].context[0].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "    \"total_return_pct\": 116.7435999134756,"
    },
    {
      "path": "generator_candidates[2].hits[10]",
      "key": "[10]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 85,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 83,
            "text": "      \"score\": 9,"
          },
          {
            "line": 84,
            "text": "      \"matched_terms\": ["
          },
          {
            "line": 85,
            "text": "        \"116.7435999134756\","
          },
          {
            "line": 86,
            "text": "        \"39.89942548515961\","
          },
          {
            "line": 87,
            "text": "        \"E1R\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[2].hits[10].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[2].hits[10].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[2].hits[10].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 83,
          "text": "      \"score\": 9,"
        },
        {
          "line": 84,
          "text": "      \"matched_terms\": ["
        },
        {
          "line": 85,
          "text": "        \"116.7435999134756\","
        },
        {
          "line": 86,
          "text": "        \"39.89942548515961\","
        },
        {
          "line": 87,
          "text": "        \"E1R\","
        }
      ]
    },
    {
      "path": "generator_candidates[2].hits[10].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 85,
        "text": "        \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[2].hits[10].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[2].hits[11]",
      "key": "[11]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 86,
        "matched": [
          "39.89942548515961"
        ],
        "context": [
          {
            "line": 84,
            "text": "      \"matched_terms\": ["
          },
          {
            "line": 85,
            "text": "        \"116.7435999134756\","
          },
          {
            "line": 86,
            "text": "        \"39.89942548515961\","
          },
          {
            "line": 87,
            "text": "        \"E1R\","
          },
          {
            "line": 88,
            "text": "        \"v0.2\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[2].hits[11].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 84,
          "text": "      \"matched_terms\": ["
        },
        {
          "line": 85,
          "text": "        \"116.7435999134756\","
        },
        {
          "line": 86,
          "text": "        \"39.89942548515961\","
        },
        {
          "line": 87,
          "text": "        \"E1R\","
        },
        {
          "line": 88,
          "text": "        \"v0.2\","
        }
      ]
    },
    {
      "path": "generator_candidates[2].hits[11].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 85,
        "text": "        \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[2].hits[11].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[2].hits[13]",
      "key": "[13]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 119,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 117,
            "text": "      \"score\": 9,"
          },
          {
            "line": 118,
            "text": "      \"matched_terms\": ["
          },
          {
            "line": 119,
            "text": "        \"116.7435999134756\","
          },
          {
            "line": 120,
            "text": "        \"39.89942548515961\","
          },
          {
            "line": 121,
            "text": "        \"E1R\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[2].hits[13].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[2].hits[13].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[2].hits[13].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 117,
          "text": "      \"score\": 9,"
        },
        {
          "line": 118,
          "text": "      \"matched_terms\": ["
        },
        {
          "line": 119,
          "text": "        \"116.7435999134756\","
        },
        {
          "line": 120,
          "text": "        \"39.89942548515961\","
        },
        {
          "line": 121,
          "text": "        \"E1R\","
        }
      ]
    },
    {
      "path": "generator_candidates[2].hits[13].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 119,
        "text": "        \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[2].hits[13].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[2].hits[14]",
      "key": "[14]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 120,
        "matched": [
          "39.89942548515961"
        ],
        "context": [
          {
            "line": 118,
            "text": "      \"matched_terms\": ["
          },
          {
            "line": 119,
            "text": "        \"116.7435999134756\","
          },
          {
            "line": 120,
            "text": "        \"39.89942548515961\","
          },
          {
            "line": 121,
            "text": "        \"E1R\","
          },
          {
            "line": 122,
            "text": "        \"v0.2\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[2].hits[14].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 118,
          "text": "      \"matched_terms\": ["
        },
        {
          "line": 119,
          "text": "        \"116.7435999134756\","
        },
        {
          "line": 120,
          "text": "        \"39.89942548515961\","
        },
        {
          "line": 121,
          "text": "        \"E1R\","
        },
        {
          "line": 122,
          "text": "        \"v0.2\","
        }
      ]
    },
    {
      "path": "generator_candidates[2].hits[14].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 119,
        "text": "        \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[2].hits[14].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[2].hits[17]",
      "key": "[17]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 154,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 152,
            "text": "      \"score\": 9,"
          },
          {
            "line": 153,
            "text": "      \"matched_terms\": ["
          },
          {
            "line": 154,
            "text": "        \"116.7435999134756\","
          },
          {
            "line": 155,
            "text": "        \"39.89942548515961\","
          },
          {
            "line": 156,
            "text": "        \"E1R\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[2].hits[17].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[2].hits[17].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[2].hits[17].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 152,
          "text": "      \"score\": 9,"
        },
        {
          "line": 153,
          "text": "      \"matched_terms\": ["
        },
        {
          "line": 154,
          "text": "        \"116.7435999134756\","
        },
        {
          "line": 155,
          "text": "        \"39.89942548515961\","
        },
        {
          "line": 156,
          "text": "        \"E1R\","
        }
      ]
    },
    {
      "path": "generator_candidates[2].hits[17].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 154,
        "text": "        \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[2].hits[17].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[2].hits[18]",
      "key": "[18]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 155,
        "matched": [
          "39.89942548515961"
        ],
        "context": [
          {
            "line": 153,
            "text": "      \"matched_terms\": ["
          },
          {
            "line": 154,
            "text": "        \"116.7435999134756\","
          },
          {
            "line": 155,
            "text": "        \"39.89942548515961\","
          },
          {
            "line": 156,
            "text": "        \"E1R\","
          },
          {
            "line": 157,
            "text": "        \"v0.2\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[2].hits[18].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 153,
          "text": "      \"matched_terms\": ["
        },
        {
          "line": 154,
          "text": "        \"116.7435999134756\","
        },
        {
          "line": 155,
          "text": "        \"39.89942548515961\","
        },
        {
          "line": 156,
          "text": "        \"E1R\","
        },
        {
          "line": 157,
          "text": "        \"v0.2\","
        }
      ]
    },
    {
      "path": "generator_candidates[2].hits[18].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 154,
        "text": "        \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[2].hits[18].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[2].hits[21]",
      "key": "[21]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 185,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 183,
            "text": "      \"score\": 9,"
          },
          {
            "line": 184,
            "text": "      \"matched_terms\": ["
          },
          {
            "line": 185,
            "text": "        \"116.7435999134756\","
          },
          {
            "line": 186,
            "text": "        \"39.89942548515961\","
          },
          {
            "line": 187,
            "text": "        \"E1R\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[2].hits[21].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[2].hits[21].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[2].hits[21].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 183,
          "text": "      \"score\": 9,"
        },
        {
          "line": 184,
          "text": "      \"matched_terms\": ["
        },
        {
          "line": 185,
          "text": "        \"116.7435999134756\","
        },
        {
          "line": 186,
          "text": "        \"39.89942548515961\","
        },
        {
          "line": 187,
          "text": "        \"E1R\","
        }
      ]
    },
    {
      "path": "generator_candidates[2].hits[21].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 185,
        "text": "        \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[2].hits[21].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[2].hits[22]",
      "key": "[22]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 186,
        "matched": [
          "39.89942548515961"
        ],
        "context": [
          {
            "line": 184,
            "text": "      \"matched_terms\": ["
          },
          {
            "line": 185,
            "text": "        \"116.7435999134756\","
          },
          {
            "line": 186,
            "text": "        \"39.89942548515961\","
          },
          {
            "line": 187,
            "text": "        \"E1R\","
          },
          {
            "line": 188,
            "text": "        \"v0.2\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[2].hits[22].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 184,
          "text": "      \"matched_terms\": ["
        },
        {
          "line": 185,
          "text": "        \"116.7435999134756\","
        },
        {
          "line": 186,
          "text": "        \"39.89942548515961\","
        },
        {
          "line": 187,
          "text": "        \"E1R\","
        },
        {
          "line": 188,
          "text": "        \"v0.2\","
        }
      ]
    },
    {
      "path": "generator_candidates[2].hits[22].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 185,
        "text": "        \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[2].hits[22].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[2].hits[24]",
      "key": "[24]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 219,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 217,
            "text": "      \"score\": 8,"
          },
          {
            "line": 218,
            "text": "      \"matched_terms\": ["
          },
          {
            "line": 219,
            "text": "        \"116.7435999134756\","
          },
          {
            "line": 220,
            "text": "        \"39.89942548515961\","
          },
          {
            "line": 221,
            "text": "        \"E1R\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[2].hits[24].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[2].hits[24].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[2].hits[24].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 217,
          "text": "      \"score\": 8,"
        },
        {
          "line": 218,
          "text": "      \"matched_terms\": ["
        },
        {
          "line": 219,
          "text": "        \"116.7435999134756\","
        },
        {
          "line": 220,
          "text": "        \"39.89942548515961\","
        },
        {
          "line": 221,
          "text": "        \"E1R\","
        }
      ]
    },
    {
      "path": "generator_candidates[2].hits[24].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 219,
        "text": "        \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[2].hits[24].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[2].hits[25]",
      "key": "[25]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 220,
        "matched": [
          "39.89942548515961"
        ],
        "context": [
          {
            "line": 218,
            "text": "      \"matched_terms\": ["
          },
          {
            "line": 219,
            "text": "        \"116.7435999134756\","
          },
          {
            "line": 220,
            "text": "        \"39.89942548515961\","
          },
          {
            "line": 221,
            "text": "        \"E1R\","
          },
          {
            "line": 222,
            "text": "        \"v0.2\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[2].hits[25].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 218,
          "text": "      \"matched_terms\": ["
        },
        {
          "line": 219,
          "text": "        \"116.7435999134756\","
        },
        {
          "line": 220,
          "text": "        \"39.89942548515961\","
        },
        {
          "line": 221,
          "text": "        \"E1R\","
        },
        {
          "line": 222,
          "text": "        \"v0.2\","
        }
      ]
    },
    {
      "path": "generator_candidates[2].hits[25].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 219,
        "text": "        \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[2].hits[25].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[2].hits[26]",
      "key": "[26]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 251,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 249,
            "text": "      \"score\": 8,"
          },
          {
            "line": 250,
            "text": "      \"matched_terms\": ["
          },
          {
            "line": 251,
            "text": "        \"116.7435999134756\","
          },
          {
            "line": 252,
            "text": "        \"39.89942548515961\","
          },
          {
            "line": 253,
            "text": "        \"E1R\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[2].hits[26].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[2].hits[26].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[2].hits[26].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 249,
          "text": "      \"score\": 8,"
        },
        {
          "line": 250,
          "text": "      \"matched_terms\": ["
        },
        {
          "line": 251,
          "text": "        \"116.7435999134756\","
        },
        {
          "line": 252,
          "text": "        \"39.89942548515961\","
        },
        {
          "line": 253,
          "text": "        \"E1R\","
        }
      ]
    },
    {
      "path": "generator_candidates[2].hits[26].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 251,
        "text": "        \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[2].hits[26].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[2].hits[27]",
      "key": "[27]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 252,
        "matched": [
          "39.89942548515961"
        ],
        "context": [
          {
            "line": 250,
            "text": "      \"matched_terms\": ["
          },
          {
            "line": 251,
            "text": "        \"116.7435999134756\","
          },
          {
            "line": 252,
            "text": "        \"39.89942548515961\","
          },
          {
            "line": 253,
            "text": "        \"E1R\","
          },
          {
            "line": 254,
            "text": "        \"compose_e1r\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[2].hits[27].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 250,
          "text": "      \"matched_terms\": ["
        },
        {
          "line": 251,
          "text": "        \"116.7435999134756\","
        },
        {
          "line": 252,
          "text": "        \"39.89942548515961\","
        },
        {
          "line": 253,
          "text": "        \"E1R\","
        },
        {
          "line": 254,
          "text": "        \"compose_e1r\","
        }
      ]
    },
    {
      "path": "generator_candidates[2].hits[27].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 251,
        "text": "        \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[2].hits[27].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[2].hits[29]",
      "key": "[29]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 279,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 277,
            "text": "      \"score\": 7,"
          },
          {
            "line": 278,
            "text": "      \"matched_terms\": ["
          },
          {
            "line": 279,
            "text": "        \"116.7435999134756\","
          },
          {
            "line": 280,
            "text": "        \"39.89942548515961\","
          },
          {
            "line": 281,
            "text": "        \"E1R\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[2].hits[29].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[2].hits[29].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[2].hits[29].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 277,
          "text": "      \"score\": 7,"
        },
        {
          "line": 278,
          "text": "      \"matched_terms\": ["
        },
        {
          "line": 279,
          "text": "        \"116.7435999134756\","
        },
        {
          "line": 280,
          "text": "        \"39.89942548515961\","
        },
        {
          "line": 281,
          "text": "        \"E1R\","
        }
      ]
    },
    {
      "path": "generator_candidates[2].hits[29].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 279,
        "text": "        \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[2].hits[29].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[3]",
      "key": "[3]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json\", \"generator_score\": 154, \"base_score\": 96, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"variant_results\", \"write_json\"], \"hits\": [{\"line\": 7, \"matched\": [\"export\"], \"context\": [{\"line\": 5, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 6, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 7, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 8, \"text\": \"    \\\"state_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"workflow_changed\\\": false,\"}]}, {\"line\": 20, \"matched\": [\"E1R_REGIME_AWARE_V0_2\"], \"context\": [{\"line\": 18, \"text\": \"      \\\"signature_hits\\\": [\"}, {\"line\": 19, \"text\": \"        \\\"E1_AUDITED_G4_MINHOLD10\\\",\"}, {\"line\": 20, \"text\": \"        \\\"E1R_REGIME_AWARE_V0_2\\\",\"}, {\"line\": 21, \"text\": \"        \\\"E1R v0.2\\\",\"}, {\"line\": 22, \"text\": \"        \\\"116.74\\\",\"}]}, {\"line\": 33, \"matched\": [\"equity_curve\"], \"context\": [{\"line\": 31, \"text\": \"        \\\"portfolio_value\\\",\"}, {\"line\": 32, \"text\": \"        \\\"daily_equity\\\",\"}, {\"line\": 33, \"text\": \"        \\\"equity_curve\\\",\"}, {\"line\": 34, \"text\": \"        \\\"strategy_indexed\\\",\"}, {\"line\": 35, \"text\": \"        \\\"spx_return\\\",\"}]}, {\"line\": 79, \"matched\": [\"e1r_v0_2\"], \"context\": [{\"line\": 77, \"text\": \"        {\"}, {\"line\": 78, \"text\": \"          \\\"path\\\": \\\"docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json\\\",\"}, {\"line\": 79, \"text\": \"          \\\"list_path\\\": \\\"source_reports.scripts/run_e1r_...<truncated>"
    },
    {
      "path": "generator_candidates[3].matched_terms",
      "key": "matched_terms",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": [
        "0.7957270568329264",
        "1.1919630955509348",
        "116.7435999134756",
        "25.904809362815108",
        "39.89942548515961",
        "76.844174428316",
        "E1R_REGIME_AWARE_V0_2",
        "compose_e1r_v0_2_variant",
        "core_variant_result",
        "daily_equity_records",
        "daily_records",
        "e1r_v0_2",
        "e1r_v0_2_backtest_equity_curve.json",
        "e1r_v0_2_backtest_summary.json",
        "equity_curve",
        "export",
        "variant_results",
        "write_json"
      ]
    },
    {
      "path": "generator_candidates[3].matched_terms[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[3].matched_terms[6]",
      "key": "[6]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[3].matched_terms[13]",
      "key": "[13]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "e1r_v0_2_backtest_summary.json"
    },
    {
      "path": "generator_candidates[3].hits",
      "key": "hits",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "[{\"line\": 7, \"matched\": [\"export\"], \"context\": [{\"line\": 5, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 6, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 7, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 8, \"text\": \"    \\\"state_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"workflow_changed\\\": false,\"}]}, {\"line\": 20, \"matched\": [\"E1R_REGIME_AWARE_V0_2\"], \"context\": [{\"line\": 18, \"text\": \"      \\\"signature_hits\\\": [\"}, {\"line\": 19, \"text\": \"        \\\"E1_AUDITED_G4_MINHOLD10\\\",\"}, {\"line\": 20, \"text\": \"        \\\"E1R_REGIME_AWARE_V0_2\\\",\"}, {\"line\": 21, \"text\": \"        \\\"E1R v0.2\\\",\"}, {\"line\": 22, \"text\": \"        \\\"116.74\\\",\"}]}, {\"line\": 33, \"matched\": [\"equity_curve\"], \"context\": [{\"line\": 31, \"text\": \"        \\\"portfolio_value\\\",\"}, {\"line\": 32, \"text\": \"        \\\"daily_equity\\\",\"}, {\"line\": 33, \"text\": \"        \\\"equity_curve\\\",\"}, {\"line\": 34, \"text\": \"        \\\"strategy_indexed\\\",\"}, {\"line\": 35, \"text\": \"        \\\"spx_return\\\",\"}]}, {\"line\": 79, \"matched\": [\"e1r_v0_2\"], \"context\": [{\"line\": 77, \"text\": \"        {\"}, {\"line\": 78, \"text\": \"          \\\"path\\\": \\\"docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json\\\",\"}, {\"line\": 79, \"text\": \"          \\\"list_path\\\": \\\"source_reports.scripts/run_e1r_v0_2_oos.py.defs\\\",\"}, {\"line\": 80, \"text\": \"          \\\"row_count\\\": 3,\"}, {\"line\": 81, \"text\": \"          \\\"kind\\\": \\\"unknown\\\",\"}]}, {\"line\": 101, \"matched\": [\"e1r_v0_2\"], \"context\": [{\"line\": 99, \"text\": \"        {\"}, {\"line\": 100, \"text\": \"          \\\"path\\\": \\\"docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json\\\",\"}, {\"line\": 101, \"text\": \"          \\\"list_path\\\": \\\"source_reports.scripts/run_e1r_v0_2_oos.py.term_hits.target\\\",\"}, {\"line\": 102, \"text\": \"          \\\"row_count\\\": 7,\"}, {\"line\": 103, \"text\": \"          \\\"kind\\\"...<truncated>"
    },
    {
      "path": "generator_candidates[3].hits[1]",
      "key": "[1]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 20,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 18,
            "text": "      \"signature_hits\": ["
          },
          {
            "line": 19,
            "text": "        \"E1_AUDITED_G4_MINHOLD10\","
          },
          {
            "line": 20,
            "text": "        \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 21,
            "text": "        \"E1R v0.2\","
          },
          {
            "line": 22,
            "text": "        \"116.74\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[3].hits[1].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[3].hits[1].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[3].hits[1].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 18,
          "text": "      \"signature_hits\": ["
        },
        {
          "line": 19,
          "text": "        \"E1_AUDITED_G4_MINHOLD10\","
        },
        {
          "line": 20,
          "text": "        \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 21,
          "text": "        \"E1R v0.2\","
        },
        {
          "line": 22,
          "text": "        \"116.74\","
        }
      ]
    },
    {
      "path": "generator_candidates[3].hits[1].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 20,
        "text": "        \"E1R_REGIME_AWARE_V0_2\","
      }
    },
    {
      "path": "generator_candidates[3].hits[1].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "        \"E1R_REGIME_AWARE_V0_2\","
    },
    {
      "path": "generator_candidates[3].hits[21]",
      "key": "[21]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 550,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 548,
            "text": "      \"signature_hits\": ["
          },
          {
            "line": 549,
            "text": "        \"E1_AUDITED_G4_MINHOLD10\","
          },
          {
            "line": 550,
            "text": "        \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 551,
            "text": "        \"E1R v0.2\","
          },
          {
            "line": 552,
            "text": "        \"2026-06-18\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[3].hits[21].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[3].hits[21].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[3].hits[21].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 548,
          "text": "      \"signature_hits\": ["
        },
        {
          "line": 549,
          "text": "        \"E1_AUDITED_G4_MINHOLD10\","
        },
        {
          "line": 550,
          "text": "        \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 551,
          "text": "        \"E1R v0.2\","
        },
        {
          "line": 552,
          "text": "        \"2026-06-18\","
        }
      ]
    },
    {
      "path": "generator_candidates[3].hits[21].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 550,
        "text": "        \"E1R_REGIME_AWARE_V0_2\","
      }
    },
    {
      "path": "generator_candidates[3].hits[21].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "        \"E1R_REGIME_AWARE_V0_2\","
    },
    {
      "path": "generator_candidates[3].hits[27]",
      "key": "[27]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 1028,
        "matched": [
          "e1r_v0_2",
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 1026,
            "text": "        {"
          },
          {
            "line": 1027,
            "text": "          \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json\","
          },
          {
            "line": 1028,
            "text": "          \"list_path\": \"source_reports.scripts/run_e1r_v0_2_oos.py.term_hits.E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 1029,
            "text": "          \"row_count\": 1,"
          },
          {
            "line": 1030,
            "text": "          \"kind\": \"numeric_array_candidate\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[3].hits[27].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "e1r_v0_2",
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[3].hits[27].matched[1]",
      "key": "[1]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[3].hits[27].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 1026,
          "text": "        {"
        },
        {
          "line": 1027,
          "text": "          \"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json\","
        },
        {
          "line": 1028,
          "text": "          \"list_path\": \"source_reports.scripts/run_e1r_v0_2_oos.py.term_hits.E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 1029,
          "text": "          \"row_count\": 1,"
        },
        {
          "line": 1030,
          "text": "          \"kind\": \"numeric_array_candidate\","
        }
      ]
    },
    {
      "path": "generator_candidates[3].hits[27].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 1028,
        "text": "          \"list_path\": \"source_reports.scripts/run_e1r_v0_2_oos.py.term_hits.E1R_REGIME_AWARE_V0_2\","
      }
    },
    {
      "path": "generator_candidates[3].hits[27].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "          \"list_path\": \"source_reports.scripts/run_e1r_v0_2_oos.py.term_hits.E1R_REGIME_AWARE_V0_2\","
    },
    {
      "path": "generator_candidates[3].hits[28]",
      "key": "[28]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 1061,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 1059,
            "text": "      \"signature_hits\": ["
          },
          {
            "line": 1060,
            "text": "        \"E1_AUDITED_G4_MINHOLD10\","
          },
          {
            "line": 1061,
            "text": "        \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 1062,
            "text": "        \"E1R v0.2\","
          },
          {
            "line": 1063,
            "text": "        \"E1-R v0.2\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[3].hits[28].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[3].hits[28].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[3].hits[28].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 1059,
          "text": "      \"signature_hits\": ["
        },
        {
          "line": 1060,
          "text": "        \"E1_AUDITED_G4_MINHOLD10\","
        },
        {
          "line": 1061,
          "text": "        \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 1062,
          "text": "        \"E1R v0.2\","
        },
        {
          "line": 1063,
          "text": "        \"E1-R v0.2\","
        }
      ]
    },
    {
      "path": "generator_candidates[3].hits[28].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 1061,
        "text": "        \"E1R_REGIME_AWARE_V0_2\","
      }
    },
    {
      "path": "generator_candidates[3].hits[28].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "        \"E1R_REGIME_AWARE_V0_2\","
    },
    {
      "path": "generator_candidates[4]",
      "key": "[4]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json",
        "run_stateful_simulation",
        "build_e1r_sidecar_sleeve"
      ],
      "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json\", \"generator_score\": 154, \"base_score\": 96, \"matched_terms\": [\"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"extract_core_interval_returns\", \"run_stateful_simulation\", \"run_strategy_variant_comparison\", \"variant_results\", \"write_json\"], \"hits\": [{\"line\": 7, \"matched\": [\"export\"], \"context\": [{\"line\": 5, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 6, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 7, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 8, \"text\": \"    \\\"state_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"workflow_changed\\\": false,\"}]}, {\"line\": 19, \"matched\": [\"export\"], \"context\": [{\"line\": 17, \"text\": \"    \\\"preliminary_decision\\\": {\"}, {\"line\": 18, \"text\": \"      \\\"dashboard_chart_should_not_use_current_e1r_backtest_equity_directly\\\": true,\"}, {\"line\": 19, \"text\": \"      \\\"reason\\\": \\\"E1R 5Y backtest equity artifact in exports is symbol-level/diagnostic rows, not one row per date.\\\",\"}, {\"line\": 20, \"text\": \"      \\\"need_next_step\\\": \\\"Either locate true portfolio-level 5Y equity outputs or generate/export canonical portfolio-level curves from existing backtest engine outputs.\\\",\"}, {\"line\": 21, \"text\": \"      \\\"proposed_canonical_export_names\\\": [\"}]}, {\"line\": 20, \"matched\": [\"export\"], \"context\": [{\"line\": 18, \"text\": \"      \\\"dashboard_chart_should_not_use_current_e1r_backtest_equity_directly\\\": true,\"}, {...<truncated>"
    },
    {
      "path": "generator_candidates[4].matched_terms",
      "key": "matched_terms",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json",
        "run_stateful_simulation",
        "build_e1r_sidecar_sleeve"
      ],
      "value": [
        "1.1919630955509348",
        "116.7435999134756",
        "25.904809362815108",
        "39.89942548515961",
        "76.844174428316",
        "E1R_REGIME_AWARE_V0_2",
        "build_e1r_sidecar_sleeve",
        "build_equity_records_from_returns",
        "compose_e1r_v0_2_variant",
        "core_variant_result",
        "daily_equity_records",
        "daily_records",
        "e1r_v0_2",
        "e1r_v0_2_backtest_equity_curve.json",
        "e1r_v0_2_backtest_summary.json",
        "equity_curve",
        "export",
        "extract_core_interval_returns",
        "run_stateful_simulation",
        "run_strategy_variant_comparison",
        "variant_results",
        "write_json"
      ]
    },
    {
      "path": "generator_candidates[4].matched_terms[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[4].matched_terms[5]",
      "key": "[5]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[4].matched_terms[6]",
      "key": "[6]",
      "matched": [
        "build_e1r_sidecar_sleeve"
      ],
      "value": "build_e1r_sidecar_sleeve"
    },
    {
      "path": "generator_candidates[4].matched_terms[14]",
      "key": "[14]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "e1r_v0_2_backtest_summary.json"
    },
    {
      "path": "generator_candidates[4].matched_terms[18]",
      "key": "[18]",
      "matched": [
        "run_stateful_simulation"
      ],
      "value": "run_stateful_simulation"
    },
    {
      "path": "generator_candidates[4].hits",
      "key": "hits",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "[{\"line\": 7, \"matched\": [\"export\"], \"context\": [{\"line\": 5, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 6, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 7, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 8, \"text\": \"    \\\"state_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"workflow_changed\\\": false,\"}]}, {\"line\": 19, \"matched\": [\"export\"], \"context\": [{\"line\": 17, \"text\": \"    \\\"preliminary_decision\\\": {\"}, {\"line\": 18, \"text\": \"      \\\"dashboard_chart_should_not_use_current_e1r_backtest_equity_directly\\\": true,\"}, {\"line\": 19, \"text\": \"      \\\"reason\\\": \\\"E1R 5Y backtest equity artifact in exports is symbol-level/diagnostic rows, not one row per date.\\\",\"}, {\"line\": 20, \"text\": \"      \\\"need_next_step\\\": \\\"Either locate true portfolio-level 5Y equity outputs or generate/export canonical portfolio-level curves from existing backtest engine outputs.\\\",\"}, {\"line\": 21, \"text\": \"      \\\"proposed_canonical_export_names\\\": [\"}]}, {\"line\": 20, \"matched\": [\"export\"], \"context\": [{\"line\": 18, \"text\": \"      \\\"dashboard_chart_should_not_use_current_e1r_backtest_equity_directly\\\": true,\"}, {\"line\": 19, \"text\": \"      \\\"reason\\\": \\\"E1R 5Y backtest equity artifact in exports is symbol-level/diagnostic rows, not one row per date.\\\",\"}, {\"line\": 20, \"text\": \"      \\\"need_next_step\\\": \\\"Either locate true portfolio-level 5Y equity outputs or generate/export canonical portfolio-level curves from existing backtest engine outputs.\\\",\"}, {\"line\": 21, \"text\": \"      \\\"proposed_canonical_export_names\\\": [\"}, {\"line\": 22, \"text\": \"        \\\"exports/e1_5y_backtest_equity_curve.json\\\",\"}]}, {\"line\": 21, \"matched\": [\"export\"], \"context\": [{\"line\": 19, \"text\": \"      \\\"reason\\\": \\\"E1R 5Y backtest equity artifact in exports is symbol-level/diagnostic rows, not one row per date.\\\",\"}, {\"l...<truncated>"
    },
    {
      "path": "generator_candidates[4].hits[15]",
      "key": "[15]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": {
        "line": 225,
        "matched": [
          "e1r_v0_2_backtest_summary.json",
          "e1r_v0_2",
          "export"
        ],
        "context": [
          {
            "line": 223,
            "text": "      ]"
          },
          {
            "line": 224,
            "text": "    },"
          },
          {
            "line": 225,
            "text": "    \"exports/e1r_v0_2_backtest_summary.json\": {"
          },
          {
            "line": 226,
            "text": "      \"exists\": true,"
          },
          {
            "line": 227,
            "text": "      \"json_valid\": true,"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[4].hits[15].matched",
      "key": "matched",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": [
        "e1r_v0_2_backtest_summary.json",
        "e1r_v0_2",
        "export"
      ]
    },
    {
      "path": "generator_candidates[4].hits[15].matched[0]",
      "key": "[0]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "e1r_v0_2_backtest_summary.json"
    },
    {
      "path": "generator_candidates[4].hits[15].context",
      "key": "context",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": [
        {
          "line": 223,
          "text": "      ]"
        },
        {
          "line": 224,
          "text": "    },"
        },
        {
          "line": 225,
          "text": "    \"exports/e1r_v0_2_backtest_summary.json\": {"
        },
        {
          "line": 226,
          "text": "      \"exists\": true,"
        },
        {
          "line": 227,
          "text": "      \"json_valid\": true,"
        }
      ]
    },
    {
      "path": "generator_candidates[4].hits[15].context[2]",
      "key": "[2]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": {
        "line": 225,
        "text": "    \"exports/e1r_v0_2_backtest_summary.json\": {"
      }
    },
    {
      "path": "generator_candidates[4].hits[15].context[2].text",
      "key": "text",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "    \"exports/e1r_v0_2_backtest_summary.json\": {"
    },
    {
      "path": "generator_candidates[4].hits[16]",
      "key": "[16]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 251,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 249,
            "text": "        \"variant\""
          },
          {
            "line": 250,
            "text": "      ],"
          },
          {
            "line": 251,
            "text": "      \"total_return_pct\": 116.7435999134756,"
          },
          {
            "line": 252,
            "text": "      \"spx_return_pct\": 76.844174428316,"
          },
          {
            "line": 253,
            "text": "      \"alpha_pct\": 39.89942548515961,"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[4].hits[16].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[4].hits[16].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[4].hits[16].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 249,
          "text": "        \"variant\""
        },
        {
          "line": 250,
          "text": "      ],"
        },
        {
          "line": 251,
          "text": "      \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 252,
          "text": "      \"spx_return_pct\": 76.844174428316,"
        },
        {
          "line": 253,
          "text": "      \"alpha_pct\": 39.89942548515961,"
        }
      ]
    },
    {
      "path": "generator_candidates[4].hits[16].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 251,
        "text": "      \"total_return_pct\": 116.7435999134756,"
      }
    },
    {
      "path": "generator_candidates[4].hits[16].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "      \"total_return_pct\": 116.7435999134756,"
    },
    {
      "path": "generator_candidates[4].hits[17]",
      "key": "[17]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 252,
        "matched": [
          "76.844174428316"
        ],
        "context": [
          {
            "line": 250,
            "text": "      ],"
          },
          {
            "line": 251,
            "text": "      \"total_return_pct\": 116.7435999134756,"
          },
          {
            "line": 252,
            "text": "      \"spx_return_pct\": 76.844174428316,"
          },
          {
            "line": 253,
            "text": "      \"alpha_pct\": 39.89942548515961,"
          },
          {
            "line": 254,
            "text": "      \"max_drawdown_pct\": 25.904809362815108,"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[4].hits[17].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 250,
          "text": "      ],"
        },
        {
          "line": 251,
          "text": "      \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 252,
          "text": "      \"spx_return_pct\": 76.844174428316,"
        },
        {
          "line": 253,
          "text": "      \"alpha_pct\": 39.89942548515961,"
        },
        {
          "line": 254,
          "text": "      \"max_drawdown_pct\": 25.904809362815108,"
        }
      ]
    },
    {
      "path": "generator_candidates[4].hits[17].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 251,
        "text": "      \"total_return_pct\": 116.7435999134756,"
      }
    },
    {
      "path": "generator_candidates[4].hits[17].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "      \"total_return_pct\": 116.7435999134756,"
    },
    {
      "path": "generator_candidates[4].hits[18]",
      "key": "[18]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 253,
        "matched": [
          "39.89942548515961"
        ],
        "context": [
          {
            "line": 251,
            "text": "      \"total_return_pct\": 116.7435999134756,"
          },
          {
            "line": 252,
            "text": "      \"spx_return_pct\": 76.844174428316,"
          },
          {
            "line": 253,
            "text": "      \"alpha_pct\": 39.89942548515961,"
          },
          {
            "line": 254,
            "text": "      \"max_drawdown_pct\": 25.904809362815108,"
          },
          {
            "line": 255,
            "text": "      \"profit_factor\": 1.1919630955509348,"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[4].hits[18].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 251,
          "text": "      \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 252,
          "text": "      \"spx_return_pct\": 76.844174428316,"
        },
        {
          "line": 253,
          "text": "      \"alpha_pct\": 39.89942548515961,"
        },
        {
          "line": 254,
          "text": "      \"max_drawdown_pct\": 25.904809362815108,"
        },
        {
          "line": 255,
          "text": "      \"profit_factor\": 1.1919630955509348,"
        }
      ]
    },
    {
      "path": "generator_candidates[4].hits[18].context[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 251,
        "text": "      \"total_return_pct\": 116.7435999134756,"
      }
    },
    {
      "path": "generator_candidates[4].hits[18].context[0].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "      \"total_return_pct\": 116.7435999134756,"
    },
    {
      "path": "generator_candidates[4].hits[19]",
      "key": "[19]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 254,
        "matched": [
          "25.904809362815108"
        ],
        "context": [
          {
            "line": 252,
            "text": "      \"spx_return_pct\": 76.844174428316,"
          },
          {
            "line": 253,
            "text": "      \"alpha_pct\": 39.89942548515961,"
          },
          {
            "line": 254,
            "text": "      \"max_drawdown_pct\": 25.904809362815108,"
          },
          {
            "line": 255,
            "text": "      \"profit_factor\": 1.1919630955509348,"
          },
          {
            "line": 256,
            "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[4].hits[19].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 252,
          "text": "      \"spx_return_pct\": 76.844174428316,"
        },
        {
          "line": 253,
          "text": "      \"alpha_pct\": 39.89942548515961,"
        },
        {
          "line": 254,
          "text": "      \"max_drawdown_pct\": 25.904809362815108,"
        },
        {
          "line": 255,
          "text": "      \"profit_factor\": 1.1919630955509348,"
        },
        {
          "line": 256,
          "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
        }
      ]
    },
    {
      "path": "generator_candidates[4].hits[19].context[4]",
      "key": "[4]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 256,
        "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      }
    },
    {
      "path": "generator_candidates[4].hits[19].context[4].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
    },
    {
      "path": "generator_candidates[4].hits[20]",
      "key": "[20]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 255,
        "matched": [
          "1.1919630955509348"
        ],
        "context": [
          {
            "line": 253,
            "text": "      \"alpha_pct\": 39.89942548515961,"
          },
          {
            "line": 254,
            "text": "      \"max_drawdown_pct\": 25.904809362815108,"
          },
          {
            "line": 255,
            "text": "      \"profit_factor\": 1.1919630955509348,"
          },
          {
            "line": 256,
            "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 257,
            "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
          }
        ]
      }
    },
    {
      "path": "generator_candidates[4].hits[20].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 253,
          "text": "      \"alpha_pct\": 39.89942548515961,"
        },
        {
          "line": 254,
          "text": "      \"max_drawdown_pct\": 25.904809362815108,"
        },
        {
          "line": 255,
          "text": "      \"profit_factor\": 1.1919630955509348,"
        },
        {
          "line": 256,
          "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 257,
          "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
        }
      ]
    },
    {
      "path": "generator_candidates[4].hits[20].context[3]",
      "key": "[3]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 256,
        "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      }
    },
    {
      "path": "generator_candidates[4].hits[20].context[3].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
    },
    {
      "path": "generator_candidates[4].hits[20].context[4]",
      "key": "[4]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 257,
        "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
      }
    },
    {
      "path": "generator_candidates[4].hits[20].context[4].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
    },
    {
      "path": "generator_candidates[4].hits[21]",
      "key": "[21]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 256,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 254,
            "text": "      \"max_drawdown_pct\": 25.904809362815108,"
          },
          {
            "line": 255,
            "text": "      \"profit_factor\": 1.1919630955509348,"
          },
          {
            "line": 256,
            "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 257,
            "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
          },
          {
            "line": 258,
            "text": "    },"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[4].hits[21].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[4].hits[21].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[4].hits[21].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 254,
          "text": "      \"max_drawdown_pct\": 25.904809362815108,"
        },
        {
          "line": 255,
          "text": "      \"profit_factor\": 1.1919630955509348,"
        },
        {
          "line": 256,
          "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 257,
          "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "line": 258,
          "text": "    },"
        }
      ]
    },
    {
      "path": "generator_candidates[4].hits[21].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 256,
        "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      }
    },
    {
      "path": "generator_candidates[4].hits[21].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
    },
    {
      "path": "generator_candidates[4].hits[21].context[3]",
      "key": "[3]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 257,
        "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
      }
    },
    {
      "path": "generator_candidates[4].hits[21].context[3].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
    },
    {
      "path": "generator_candidates[4].hits[22]",
      "key": "[22]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 257,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 255,
            "text": "      \"profit_factor\": 1.1919630955509348,"
          },
          {
            "line": 256,
            "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 257,
            "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
          },
          {
            "line": 258,
            "text": "    },"
          },
          {
            "line": 259,
            "text": "    \"exports/e1r_v0_2_backtest_equity_curve.json\": {"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[4].hits[22].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[4].hits[22].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[4].hits[22].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 255,
          "text": "      \"profit_factor\": 1.1919630955509348,"
        },
        {
          "line": 256,
          "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 257,
          "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "line": 258,
          "text": "    },"
        },
        {
          "line": 259,
          "text": "    \"exports/e1r_v0_2_backtest_equity_curve.json\": {"
        }
      ]
    },
    {
      "path": "generator_candidates[4].hits[22].context[1]",
      "key": "[1]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 256,
        "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      }
    },
    {
      "path": "generator_candidates[4].hits[22].context[1].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
    },
    {
      "path": "generator_candidates[4].hits[22].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 257,
        "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
      }
    },
    {
      "path": "generator_candidates[4].hits[22].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
    },
    {
      "path": "generator_candidates[4].hits[23]",
      "key": "[23]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 259,
        "matched": [
          "e1r_v0_2_backtest_equity_curve.json",
          "e1r_v0_2",
          "equity_curve",
          "export"
        ],
        "context": [
          {
            "line": 257,
            "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
          },
          {
            "line": 258,
            "text": "    },"
          },
          {
            "line": 259,
            "text": "    \"exports/e1r_v0_2_backtest_equity_curve.json\": {"
          },
          {
            "line": 260,
            "text": "      \"exists\": true,"
          },
          {
            "line": 261,
            "text": "      \"json_valid\": true,"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[4].hits[23].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 257,
          "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "line": 258,
          "text": "    },"
        },
        {
          "line": 259,
          "text": "    \"exports/e1r_v0_2_backtest_equity_curve.json\": {"
        },
        {
          "line": 260,
          "text": "      \"exists\": true,"
        },
        {
          "line": 261,
          "text": "      \"json_valid\": true,"
        }
      ]
    },
    {
      "path": "generator_candidates[4].hits[23].context[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 257,
        "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
      }
    },
    {
      "path": "generator_candidates[4].hits[23].context[0].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
    },
    {
      "path": "generator_candidates[4].hits[26]",
      "key": "[26]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 348,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 346,
            "text": "        }"
          },
          {
            "line": 347,
            "text": "      },"
          },
          {
            "line": 348,
            "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
          },
          {
            "line": 349,
            "text": "    },"
          },
          {
            "line": 350,
            "text": "    \"exports/oos_e1r_v0_2_equity_curve.json\": {"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[4].hits[26].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[4].hits[26].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[4].hits[26].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 346,
          "text": "        }"
        },
        {
          "line": 347,
          "text": "      },"
        },
        {
          "line": 348,
          "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "line": 349,
          "text": "    },"
        },
        {
          "line": 350,
          "text": "    \"exports/oos_e1r_v0_2_equity_curve.json\": {"
        }
      ]
    },
    {
      "path": "generator_candidates[4].hits[26].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 348,
        "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
      }
    },
    {
      "path": "generator_candidates[4].hits[26].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
    },
    {
      "path": "generator_candidates[4].hits[27]",
      "key": "[27]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 350,
        "matched": [
          "e1r_v0_2",
          "equity_curve",
          "export"
        ],
        "context": [
          {
            "line": 348,
            "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
          },
          {
            "line": 349,
            "text": "    },"
          },
          {
            "line": 350,
            "text": "    \"exports/oos_e1r_v0_2_equity_curve.json\": {"
          },
          {
            "line": 351,
            "text": "      \"exists\": true,"
          },
          {
            "line": 352,
            "text": "      \"json_valid\": true,"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[4].hits[27].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 348,
          "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
        },
        {
          "line": 349,
          "text": "    },"
        },
        {
          "line": 350,
          "text": "    \"exports/oos_e1r_v0_2_equity_curve.json\": {"
        },
        {
          "line": 351,
          "text": "      \"exists\": true,"
        },
        {
          "line": 352,
          "text": "      \"json_valid\": true,"
        }
      ]
    },
    {
      "path": "generator_candidates[4].hits[27].context[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 348,
        "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
      }
    },
    {
      "path": "generator_candidates[4].hits[27].context[0].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
    },
    {
      "path": "generator_candidates[4].hits[28]",
      "key": "[28]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 360,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 358,
            "text": "        \"portfolio_value\": 100000.0,"
          },
          {
            "line": 359,
            "text": "        \"equity\": 100000.0,"
          },
          {
            "line": 360,
            "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 361,
            "text": "        \"version\": \"v0.2\","
          },
          {
            "line": 362,
            "text": "        \"cash\": 100000.0,"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[4].hits[28].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[4].hits[28].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[4].hits[28].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 358,
          "text": "        \"portfolio_value\": 100000.0,"
        },
        {
          "line": 359,
          "text": "        \"equity\": 100000.0,"
        },
        {
          "line": 360,
          "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 361,
          "text": "        \"version\": \"v0.2\","
        },
        {
          "line": 362,
          "text": "        \"cash\": 100000.0,"
        }
      ]
    },
    {
      "path": "generator_candidates[4].hits[28].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 360,
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      }
    },
    {
      "path": "generator_candidates[4].hits[28].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
    },
    {
      "path": "generator_candidates[5]",
      "key": "[5]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json",
        "build_e1r_sidecar_sleeve"
      ],
      "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json\", \"generator_score\": 150, \"base_score\": 100, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"extract_core_interval_returns\", \"sidecar_result\", \"write_json\"], \"hits\": [{\"line\": 11, \"matched\": [\"export\"], \"context\": [{\"line\": 9, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 10, \"text\": \"    \\\"source_changed\\\": false,\"}, {\"line\": 11, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 12, \"text\": \"    \\\"state_changed\\\": false,\"}, {\"line\": 13, \"text\": \"    \\\"dashboard_changed\\\": false,\"}]}, {\"line\": 18, \"matched\": [\"e1r_v0_2\"], \"context\": [{\"line\": 16, \"text\": \"  \\\"question\\\": \\\"What exact symbol-level target/action inputs are available for E1R forward positions/orders?\\\",\"}, {\"line\": 17, \"text\": \"  \\\"source_files\\\": [\"}, {\"line\": 18, \"text\": \"    \\\"scripts/run_e1r_v0_2_oos.py\\\",\"}, {\"line\": 19, \"text\": \"    \\\"scripts/run_e1r_v0_2_oos_equity.py\\\",\"}, {\"line\": 20, \"text\": \"    \\\"scripts/run_e1r_v0_2_forward_performance.py\\\",\"}]}, {\"line\": 19, \"matched\": [\"e1r_v0_2\"], \"context\": [{\"line\": 17, \"text\": \"  \\\"source_files\\\": [\"}, {\"line\": 18, \"text\": \"    \\\"scripts/run_e1r_v0_2_oos.py\\\",\"}, {\"line\": 19, \"text\": \"    \\\"scripts/run_e1r_v0_2_oos_equity.py\\\",\"}, {\"line\": 20, \"text\": \"    \\\"scripts/run_e1r_v0_2_forward_performance.py\\\",\"}, {\"line\": 21, \"text\": \"    \\\"scripts/export_e1r_v0_2_status.py\\\",\"}]}, {\"line\": 20, \"matched\": [\"e1r_v0_2\"], \"c...<truncated>"
    },
    {
      "path": "generator_candidates[5].matched_terms",
      "key": "matched_terms",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json",
        "build_e1r_sidecar_sleeve"
      ],
      "value": [
        "0.7957270568329264",
        "1.1919630955509348",
        "116.7435999134756",
        "25.904809362815108",
        "39.89942548515961",
        "76.844174428316",
        "E1R_REGIME_AWARE_V0_2",
        "build_e1r_sidecar_sleeve",
        "build_equity_records_from_returns",
        "compose_e1r_v0_2_variant",
        "core_variant_result",
        "daily_equity_records",
        "e1r_v0_2",
        "e1r_v0_2_backtest_equity_curve.json",
        "e1r_v0_2_backtest_summary.json",
        "equity_curve",
        "export",
        "extract_core_interval_returns",
        "sidecar_result",
        "write_json"
      ]
    },
    {
      "path": "generator_candidates[5].matched_terms[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[5].matched_terms[6]",
      "key": "[6]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[5].matched_terms[7]",
      "key": "[7]",
      "matched": [
        "build_e1r_sidecar_sleeve"
      ],
      "value": "build_e1r_sidecar_sleeve"
    },
    {
      "path": "generator_candidates[5].matched_terms[14]",
      "key": "[14]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "e1r_v0_2_backtest_summary.json"
    },
    {
      "path": "generator_candidates[5].hits",
      "key": "hits",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "[{\"line\": 11, \"matched\": [\"export\"], \"context\": [{\"line\": 9, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 10, \"text\": \"    \\\"source_changed\\\": false,\"}, {\"line\": 11, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 12, \"text\": \"    \\\"state_changed\\\": false,\"}, {\"line\": 13, \"text\": \"    \\\"dashboard_changed\\\": false,\"}]}, {\"line\": 18, \"matched\": [\"e1r_v0_2\"], \"context\": [{\"line\": 16, \"text\": \"  \\\"question\\\": \\\"What exact symbol-level target/action inputs are available for E1R forward positions/orders?\\\",\"}, {\"line\": 17, \"text\": \"  \\\"source_files\\\": [\"}, {\"line\": 18, \"text\": \"    \\\"scripts/run_e1r_v0_2_oos.py\\\",\"}, {\"line\": 19, \"text\": \"    \\\"scripts/run_e1r_v0_2_oos_equity.py\\\",\"}, {\"line\": 20, \"text\": \"    \\\"scripts/run_e1r_v0_2_forward_performance.py\\\",\"}]}, {\"line\": 19, \"matched\": [\"e1r_v0_2\"], \"context\": [{\"line\": 17, \"text\": \"  \\\"source_files\\\": [\"}, {\"line\": 18, \"text\": \"    \\\"scripts/run_e1r_v0_2_oos.py\\\",\"}, {\"line\": 19, \"text\": \"    \\\"scripts/run_e1r_v0_2_oos_equity.py\\\",\"}, {\"line\": 20, \"text\": \"    \\\"scripts/run_e1r_v0_2_forward_performance.py\\\",\"}, {\"line\": 21, \"text\": \"    \\\"scripts/export_e1r_v0_2_status.py\\\",\"}]}, {\"line\": 20, \"matched\": [\"e1r_v0_2\"], \"context\": [{\"line\": 18, \"text\": \"    \\\"scripts/run_e1r_v0_2_oos.py\\\",\"}, {\"line\": 19, \"text\": \"    \\\"scripts/run_e1r_v0_2_oos_equity.py\\\",\"}, {\"line\": 20, \"text\": \"    \\\"scripts/run_e1r_v0_2_forward_performance.py\\\",\"}, {\"line\": 21, \"text\": \"    \\\"scripts/export_e1r_v0_2_status.py\\\",\"}, {\"line\": 22, \"text\": \"    \\\"scripts/run_e1r_v0_2_sidecar_lifecycle.py\\\",\"}]}, {\"line\": 21, \"matched\": [\"e1r_v0_2\", \"export\"], \"context\": [{\"line\": 19, \"text\": \"    \\\"scripts/run_e1r_v0_2_oos_equity.py\\\",\"}, {\"line\": 20, \"text\": \"    \\\"scripts/run_e1r_v0_2_forward_performance.py\\\",\"}, {\"line\": 21, \"text\": \"    \\\"scripts/export_e1r_...<truncated>"
    },
    {
      "path": "generator_candidates[5].hits[13]",
      "key": "[13]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": {
        "line": 36,
        "matched": [
          "e1r_v0_2",
          "export"
        ],
        "context": [
          {
            "line": 34,
            "text": "    \"exports/oos_e1r_v0_2_orders.json\","
          },
          {
            "line": 35,
            "text": "    \"exports/oos_e1r_v0_2_sidecar.json\","
          },
          {
            "line": 36,
            "text": "    \"exports/oos_e1r_v0_2_sidecar_lifecycle.json\","
          },
          {
            "line": 37,
            "text": "    \"exports/oos_e1r_v0_2_sidecar_turnover.json\","
          },
          {
            "line": 38,
            "text": "    \"exports/e1r_v0_2_backtest_summary.json\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[5].hits[13].context",
      "key": "context",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": [
        {
          "line": 34,
          "text": "    \"exports/oos_e1r_v0_2_orders.json\","
        },
        {
          "line": 35,
          "text": "    \"exports/oos_e1r_v0_2_sidecar.json\","
        },
        {
          "line": 36,
          "text": "    \"exports/oos_e1r_v0_2_sidecar_lifecycle.json\","
        },
        {
          "line": 37,
          "text": "    \"exports/oos_e1r_v0_2_sidecar_turnover.json\","
        },
        {
          "line": 38,
          "text": "    \"exports/e1r_v0_2_backtest_summary.json\","
        }
      ]
    },
    {
      "path": "generator_candidates[5].hits[13].context[4]",
      "key": "[4]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": {
        "line": 38,
        "text": "    \"exports/e1r_v0_2_backtest_summary.json\","
      }
    },
    {
      "path": "generator_candidates[5].hits[13].context[4].text",
      "key": "text",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "    \"exports/e1r_v0_2_backtest_summary.json\","
    },
    {
      "path": "generator_candidates[5].hits[14]",
      "key": "[14]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": {
        "line": 37,
        "matched": [
          "e1r_v0_2",
          "export"
        ],
        "context": [
          {
            "line": 35,
            "text": "    \"exports/oos_e1r_v0_2_sidecar.json\","
          },
          {
            "line": 36,
            "text": "    \"exports/oos_e1r_v0_2_sidecar_lifecycle.json\","
          },
          {
            "line": 37,
            "text": "    \"exports/oos_e1r_v0_2_sidecar_turnover.json\","
          },
          {
            "line": 38,
            "text": "    \"exports/e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 39,
            "text": "    \"exports/e1r_v0_2_backtest_equity_curve.json\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[5].hits[14].context",
      "key": "context",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": [
        {
          "line": 35,
          "text": "    \"exports/oos_e1r_v0_2_sidecar.json\","
        },
        {
          "line": 36,
          "text": "    \"exports/oos_e1r_v0_2_sidecar_lifecycle.json\","
        },
        {
          "line": 37,
          "text": "    \"exports/oos_e1r_v0_2_sidecar_turnover.json\","
        },
        {
          "line": 38,
          "text": "    \"exports/e1r_v0_2_backtest_summary.json\","
        },
        {
          "line": 39,
          "text": "    \"exports/e1r_v0_2_backtest_equity_curve.json\","
        }
      ]
    },
    {
      "path": "generator_candidates[5].hits[14].context[3]",
      "key": "[3]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": {
        "line": 38,
        "text": "    \"exports/e1r_v0_2_backtest_summary.json\","
      }
    },
    {
      "path": "generator_candidates[5].hits[14].context[3].text",
      "key": "text",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "    \"exports/e1r_v0_2_backtest_summary.json\","
    },
    {
      "path": "generator_candidates[5].hits[15]",
      "key": "[15]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": {
        "line": 38,
        "matched": [
          "e1r_v0_2_backtest_summary.json",
          "e1r_v0_2",
          "export"
        ],
        "context": [
          {
            "line": 36,
            "text": "    \"exports/oos_e1r_v0_2_sidecar_lifecycle.json\","
          },
          {
            "line": 37,
            "text": "    \"exports/oos_e1r_v0_2_sidecar_turnover.json\","
          },
          {
            "line": 38,
            "text": "    \"exports/e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 39,
            "text": "    \"exports/e1r_v0_2_backtest_equity_curve.json\","
          },
          {
            "line": 40,
            "text": "    \"exports/leaderboard.json\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[5].hits[15].matched",
      "key": "matched",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": [
        "e1r_v0_2_backtest_summary.json",
        "e1r_v0_2",
        "export"
      ]
    },
    {
      "path": "generator_candidates[5].hits[15].matched[0]",
      "key": "[0]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "e1r_v0_2_backtest_summary.json"
    },
    {
      "path": "generator_candidates[5].hits[15].context",
      "key": "context",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": [
        {
          "line": 36,
          "text": "    \"exports/oos_e1r_v0_2_sidecar_lifecycle.json\","
        },
        {
          "line": 37,
          "text": "    \"exports/oos_e1r_v0_2_sidecar_turnover.json\","
        },
        {
          "line": 38,
          "text": "    \"exports/e1r_v0_2_backtest_summary.json\","
        },
        {
          "line": 39,
          "text": "    \"exports/e1r_v0_2_backtest_equity_curve.json\","
        },
        {
          "line": 40,
          "text": "    \"exports/leaderboard.json\","
        }
      ]
    },
    {
      "path": "generator_candidates[5].hits[15].context[2]",
      "key": "[2]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": {
        "line": 38,
        "text": "    \"exports/e1r_v0_2_backtest_summary.json\","
      }
    },
    {
      "path": "generator_candidates[5].hits[15].context[2].text",
      "key": "text",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "    \"exports/e1r_v0_2_backtest_summary.json\","
    },
    {
      "path": "generator_candidates[5].hits[16]",
      "key": "[16]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": {
        "line": 39,
        "matched": [
          "e1r_v0_2_backtest_equity_curve.json",
          "e1r_v0_2",
          "equity_curve",
          "export"
        ],
        "context": [
          {
            "line": 37,
            "text": "    \"exports/oos_e1r_v0_2_sidecar_turnover.json\","
          },
          {
            "line": 38,
            "text": "    \"exports/e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 39,
            "text": "    \"exports/e1r_v0_2_backtest_equity_curve.json\","
          },
          {
            "line": 40,
            "text": "    \"exports/leaderboard.json\","
          },
          {
            "line": 41,
            "text": "    \"exports/market_state.json\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[5].hits[16].context",
      "key": "context",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": [
        {
          "line": 37,
          "text": "    \"exports/oos_e1r_v0_2_sidecar_turnover.json\","
        },
        {
          "line": 38,
          "text": "    \"exports/e1r_v0_2_backtest_summary.json\","
        },
        {
          "line": 39,
          "text": "    \"exports/e1r_v0_2_backtest_equity_curve.json\","
        },
        {
          "line": 40,
          "text": "    \"exports/leaderboard.json\","
        },
        {
          "line": 41,
          "text": "    \"exports/market_state.json\","
        }
      ]
    },
    {
      "path": "generator_candidates[5].hits[16].context[1]",
      "key": "[1]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": {
        "line": 38,
        "text": "    \"exports/e1r_v0_2_backtest_summary.json\","
      }
    },
    {
      "path": "generator_candidates[5].hits[16].context[1].text",
      "key": "text",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "    \"exports/e1r_v0_2_backtest_summary.json\","
    },
    {
      "path": "generator_candidates[5].hits[17]",
      "key": "[17]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": {
        "line": 40,
        "matched": [
          "export"
        ],
        "context": [
          {
            "line": 38,
            "text": "    \"exports/e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 39,
            "text": "    \"exports/e1r_v0_2_backtest_equity_curve.json\","
          },
          {
            "line": 40,
            "text": "    \"exports/leaderboard.json\","
          },
          {
            "line": 41,
            "text": "    \"exports/market_state.json\","
          },
          {
            "line": 42,
            "text": "    \"data/oos/e1r_v0_2_portfolio_state.json\""
          }
        ]
      }
    },
    {
      "path": "generator_candidates[5].hits[17].context",
      "key": "context",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": [
        {
          "line": 38,
          "text": "    \"exports/e1r_v0_2_backtest_summary.json\","
        },
        {
          "line": 39,
          "text": "    \"exports/e1r_v0_2_backtest_equity_curve.json\","
        },
        {
          "line": 40,
          "text": "    \"exports/leaderboard.json\","
        },
        {
          "line": 41,
          "text": "    \"exports/market_state.json\","
        },
        {
          "line": 42,
          "text": "    \"data/oos/e1r_v0_2_portfolio_state.json\""
        }
      ]
    },
    {
      "path": "generator_candidates[5].hits[17].context[0]",
      "key": "[0]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": {
        "line": 38,
        "text": "    \"exports/e1r_v0_2_backtest_summary.json\","
      }
    },
    {
      "path": "generator_candidates[5].hits[17].context[0].text",
      "key": "text",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "    \"exports/e1r_v0_2_backtest_summary.json\","
    },
    {
      "path": "generator_candidates[5].hits[24]",
      "key": "[24]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 197,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 195,
            "text": "          142"
          },
          {
            "line": 196,
            "text": "        ],"
          },
          {
            "line": 197,
            "text": "        \"E1R_REGIME_AWARE_V0_2\": ["
          },
          {
            "line": 198,
            "text": "          38"
          },
          {
            "line": 199,
            "text": "        ],"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[5].hits[24].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[5].hits[24].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[5].hits[24].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 195,
          "text": "          142"
        },
        {
          "line": 196,
          "text": "        ],"
        },
        {
          "line": 197,
          "text": "        \"E1R_REGIME_AWARE_V0_2\": ["
        },
        {
          "line": 198,
          "text": "          38"
        },
        {
          "line": 199,
          "text": "        ],"
        }
      ]
    },
    {
      "path": "generator_candidates[5].hits[24].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 197,
        "text": "        \"E1R_REGIME_AWARE_V0_2\": ["
      }
    },
    {
      "path": "generator_candidates[5].hits[24].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "        \"E1R_REGIME_AWARE_V0_2\": ["
    },
    {
      "path": "generator_candidates[6]",
      "key": "[6]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json",
        "build_e1r_sidecar_sleeve"
      ],
      "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json\", \"generator_score\": 139, \"base_score\": 96, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"daily_equity_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"sidecar_result\", \"variant_results\"], \"hits\": [{\"line\": 12, \"matched\": [\"export\"], \"context\": [{\"line\": 10, \"text\": \"    \\\"source_changed\\\": false,\"}, {\"line\": 11, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 12, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 13, \"text\": \"    \\\"strategy_logic_changed\\\": false\"}, {\"line\": 14, \"text\": \"  },\"}]}, {\"line\": 18, \"matched\": [\"export\"], \"context\": [{\"line\": 16, \"text\": \"  \\\"readiness\\\": {\"}, {\"line\": 17, \"text\": \"    \\\"e1_forward_start\\\": {\"}, {\"line\": 18, \"text\": \"      \\\"source\\\": \\\"exports/oos_summary.json\\\",\"}, {\"line\": 19, \"text\": \"      \\\"key\\\": \\\"oos_start_date\\\",\"}, {\"line\": 20, \"text\": \"      \\\"value\\\": \\\"2026-06-16\\\"\"}]}, {\"line\": 23, \"matched\": [\"equity_curve\"], \"context\": [{\"line\": 21, \"text\": \"    },\"}, {\"line\": 22, \"text\": \"    \\\"e1r_status_scaffold_exists\\\": true,\"}, {\"line\": 23, \"text\": \"    \\\"e1r_equity_curve_scaffold_exists\\\": true,\"}, {\"line\": 24, \"text\": \"    \\\"e1r_orders_scaffold_exists\\\": true,\"}, {\"line\": 25, \"text\": \"    \\\"e1r_positions_scaffold_exists\\\": true,\"}]}, {\"line\": 28, \"matched\": [\"export\"], \"context\": [{\"line\": 26, \"text\": \"    \\\"e1r_forward_performance_fields_exist\\\": false,\"}, {\"line\": 27, \"text\": \"    \\\"current_assessment\\\": \\\"NOT_YET_KICKED_OFF_AS_FORWARD_PERFORMANCE_T...<truncated>"
    },
    {
      "path": "generator_candidates[6].matched_terms",
      "key": "matched_terms",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json",
        "build_e1r_sidecar_sleeve"
      ],
      "value": [
        "0.7957270568329264",
        "1.1919630955509348",
        "116.7435999134756",
        "25.904809362815108",
        "39.89942548515961",
        "76.844174428316",
        "E1R_REGIME_AWARE_V0_2",
        "build_e1r_sidecar_sleeve",
        "build_equity_records_from_returns",
        "compose_e1r_v0_2_variant",
        "daily_equity_records",
        "e1r_v0_2",
        "e1r_v0_2_backtest_equity_curve.json",
        "e1r_v0_2_backtest_summary.json",
        "equity_curve",
        "export",
        "sidecar_result",
        "variant_results"
      ]
    },
    {
      "path": "generator_candidates[6].matched_terms[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[6].matched_terms[6]",
      "key": "[6]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[6].matched_terms[7]",
      "key": "[7]",
      "matched": [
        "build_e1r_sidecar_sleeve"
      ],
      "value": "build_e1r_sidecar_sleeve"
    },
    {
      "path": "generator_candidates[6].matched_terms[13]",
      "key": "[13]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "e1r_v0_2_backtest_summary.json"
    },
    {
      "path": "generator_candidates[6].hits",
      "key": "hits",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "[{\"line\": 12, \"matched\": [\"export\"], \"context\": [{\"line\": 10, \"text\": \"    \\\"source_changed\\\": false,\"}, {\"line\": 11, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 12, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 13, \"text\": \"    \\\"strategy_logic_changed\\\": false\"}, {\"line\": 14, \"text\": \"  },\"}]}, {\"line\": 18, \"matched\": [\"export\"], \"context\": [{\"line\": 16, \"text\": \"  \\\"readiness\\\": {\"}, {\"line\": 17, \"text\": \"    \\\"e1_forward_start\\\": {\"}, {\"line\": 18, \"text\": \"      \\\"source\\\": \\\"exports/oos_summary.json\\\",\"}, {\"line\": 19, \"text\": \"      \\\"key\\\": \\\"oos_start_date\\\",\"}, {\"line\": 20, \"text\": \"      \\\"value\\\": \\\"2026-06-16\\\"\"}]}, {\"line\": 23, \"matched\": [\"equity_curve\"], \"context\": [{\"line\": 21, \"text\": \"    },\"}, {\"line\": 22, \"text\": \"    \\\"e1r_status_scaffold_exists\\\": true,\"}, {\"line\": 23, \"text\": \"    \\\"e1r_equity_curve_scaffold_exists\\\": true,\"}, {\"line\": 24, \"text\": \"    \\\"e1r_orders_scaffold_exists\\\": true,\"}, {\"line\": 25, \"text\": \"    \\\"e1r_positions_scaffold_exists\\\": true,\"}]}, {\"line\": 28, \"matched\": [\"export\"], \"context\": [{\"line\": 26, \"text\": \"    \\\"e1r_forward_performance_fields_exist\\\": false,\"}, {\"line\": 27, \"text\": \"    \\\"current_assessment\\\": \\\"NOT_YET_KICKED_OFF_AS_FORWARD_PERFORMANCE_TEST\\\",\"}, {\"line\": 28, \"text\": \"    \\\"recommended_next_step\\\": \\\"Implement E1R forward engine/export kickoff, not just dashboard mapping.\\\"\"}, {\"line\": 29, \"text\": \"  },\"}, {\"line\": 30, \"text\": \"  \\\"kickoff_schema\\\": {\"}]}, {\"line\": 31, \"matched\": [\"E1R_REGIME_AWARE_V0_2\"], \"context\": [{\"line\": 29, \"text\": \"  },\"}, {\"line\": 30, \"text\": \"  \\\"kickoff_schema\\\": {\"}, {\"line\": 31, \"text\": \"    \\\"official_strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\"}, {\"line\": 32, \"text\": \"    \\\"recommended_forward_start_policy\\\": {\"}, {\"line\": 33, \"text\": \"      \\\"principle\\\": \\...<truncated>"
    },
    {
      "path": "generator_candidates[6].hits[4]",
      "key": "[4]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 31,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 29,
            "text": "  },"
          },
          {
            "line": 30,
            "text": "  \"kickoff_schema\": {"
          },
          {
            "line": 31,
            "text": "    \"official_strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 32,
            "text": "    \"recommended_forward_start_policy\": {"
          },
          {
            "line": 33,
            "text": "      \"principle\": \"Do not retroactively count pre-kickoff dates as true OOS performance.\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[6].hits[4].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[6].hits[4].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[6].hits[4].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 29,
          "text": "  },"
        },
        {
          "line": 30,
          "text": "  \"kickoff_schema\": {"
        },
        {
          "line": 31,
          "text": "    \"official_strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 32,
          "text": "    \"recommended_forward_start_policy\": {"
        },
        {
          "line": 33,
          "text": "      \"principle\": \"Do not retroactively count pre-kickoff dates as true OOS performance.\","
        }
      ]
    },
    {
      "path": "generator_candidates[6].hits[4].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 31,
        "text": "    \"official_strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      }
    },
    {
      "path": "generator_candidates[6].hits[4].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "    \"official_strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
    },
    {
      "path": "generator_candidates[6].hits[23]",
      "key": "[23]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 243,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 241,
            "text": "          2568"
          },
          {
            "line": 242,
            "text": "        ],"
          },
          {
            "line": 243,
            "text": "        \"E1R_REGIME_AWARE_V0_2\": ["
          },
          {
            "line": 244,
            "text": "          2737"
          },
          {
            "line": 245,
            "text": "        ],"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[6].hits[23].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[6].hits[23].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[6].hits[23].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 241,
          "text": "          2568"
        },
        {
          "line": 242,
          "text": "        ],"
        },
        {
          "line": 243,
          "text": "        \"E1R_REGIME_AWARE_V0_2\": ["
        },
        {
          "line": 244,
          "text": "          2737"
        },
        {
          "line": 245,
          "text": "        ],"
        }
      ]
    },
    {
      "path": "generator_candidates[6].hits[23].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 243,
        "text": "        \"E1R_REGIME_AWARE_V0_2\": ["
      }
    },
    {
      "path": "generator_candidates[6].hits[23].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "        \"E1R_REGIME_AWARE_V0_2\": ["
    },
    {
      "path": "generator_candidates[6].hits[24]",
      "key": "[24]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 414,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 412,
            "text": "        },"
          },
          {
            "line": 413,
            "text": "        {"
          },
          {
            "line": 414,
            "text": "          \"term\": \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 415,
            "text": "          \"line\": 2737,"
          },
          {
            "line": 416,
            "text": "          \"text\": \"            variant_results[\\\"E1R_REGIME_AWARE_V0_2\\\"] = compose_e1r_v0_2_variant(\""
          }
        ]
      }
    },
    {
      "path": "generator_candidates[6].hits[24].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[6].hits[24].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[6].hits[24].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 412,
          "text": "        },"
        },
        {
          "line": 413,
          "text": "        {"
        },
        {
          "line": 414,
          "text": "          \"term\": \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 415,
          "text": "          \"line\": 2737,"
        },
        {
          "line": 416,
          "text": "          \"text\": \"            variant_results[\\\"E1R_REGIME_AWARE_V0_2\\\"] = compose_e1r_v0_2_variant(\""
        }
      ]
    },
    {
      "path": "generator_candidates[6].hits[24].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 414,
        "text": "          \"term\": \"E1R_REGIME_AWARE_V0_2\","
      }
    },
    {
      "path": "generator_candidates[6].hits[24].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "          \"term\": \"E1R_REGIME_AWARE_V0_2\","
    },
    {
      "path": "generator_candidates[6].hits[24].context[4]",
      "key": "[4]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 416,
        "text": "          \"text\": \"            variant_results[\\\"E1R_REGIME_AWARE_V0_2\\\"] = compose_e1r_v0_2_variant(\""
      }
    },
    {
      "path": "generator_candidates[6].hits[24].context[4].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "          \"text\": \"            variant_results[\\\"E1R_REGIME_AWARE_V0_2\\\"] = compose_e1r_v0_2_variant(\""
    },
    {
      "path": "generator_candidates[6].hits[25]",
      "key": "[25]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 416,
        "matched": [
          "e1r_v0_2",
          "E1R_REGIME_AWARE_V0_2",
          "compose_e1r_v0_2_variant",
          "variant_results"
        ],
        "context": [
          {
            "line": 414,
            "text": "          \"term\": \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 415,
            "text": "          \"line\": 2737,"
          },
          {
            "line": 416,
            "text": "          \"text\": \"            variant_results[\\\"E1R_REGIME_AWARE_V0_2\\\"] = compose_e1r_v0_2_variant(\""
          },
          {
            "line": 417,
            "text": "        },"
          },
          {
            "line": 418,
            "text": "        {"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[6].hits[25].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "e1r_v0_2",
        "E1R_REGIME_AWARE_V0_2",
        "compose_e1r_v0_2_variant",
        "variant_results"
      ]
    },
    {
      "path": "generator_candidates[6].hits[25].matched[1]",
      "key": "[1]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[6].hits[25].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        {
          "line": 414,
          "text": "          \"term\": \"E1R_REGIME_AWARE_V0_2\","
        },
        {
          "line": 415,
          "text": "          \"line\": 2737,"
        },
        {
          "line": 416,
          "text": "          \"text\": \"            variant_results[\\\"E1R_REGIME_AWARE_V0_2\\\"] = compose_e1r_v0_2_variant(\""
        },
        {
          "line": 417,
          "text": "        },"
        },
        {
          "line": 418,
          "text": "        {"
        }
      ]
    },
    {
      "path": "generator_candidates[6].hits[25].context[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 414,
        "text": "          \"term\": \"E1R_REGIME_AWARE_V0_2\","
      }
    },
    {
      "path": "generator_candidates[6].hits[25].context[0].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "          \"term\": \"E1R_REGIME_AWARE_V0_2\","
    },
    {
      "path": "generator_candidates[6].hits[25].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 416,
        "text": "          \"text\": \"            variant_results[\\\"E1R_REGIME_AWARE_V0_2\\\"] = compose_e1r_v0_2_variant(\""
      }
    },
    {
      "path": "generator_candidates[6].hits[25].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "          \"text\": \"            variant_results[\\\"E1R_REGIME_AWARE_V0_2\\\"] = compose_e1r_v0_2_variant(\""
    },
    {
      "path": "generator_candidates[7]",
      "key": "[7]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json",
        "run_stateful_simulation"
      ],
      "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.md\", \"generator_score\": 130, \"base_score\": 85, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"e1r_v0_2\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"run_stateful_simulation\"], \"hits\": [{\"line\": 20, \"matched\": [\"e1r_v0_2\", \"compose_e1r_v0_2_variant\", \"core_variant_result\"], \"context\": [{\"line\": 18, \"text\": \"    \\\"E1 saved core row-derived total_return_pct is 89.8157%, while frozen E1R target total_return_pct is 116.7436%; delta=26.9279pp.\\\",\"}, {\"line\": 19, \"text\": \"    \\\"Saved sidecar is active exactly 135 rows, all expected MA_CONFLICT/SIDEWAYS intervals.\\\",\"}, {\"line\": 20, \"text\": \"    \\\"Source references core_variant_result / compose_e1r_v0_2_variant, so E1R appears to be composed from an explicit core result plus sidecar result.\\\",\"}, {\"line\": 21, \"text\": \"    \\\"Source/result terms include e1r_uptrend_execution_enabled / e1r_candidates; this suggests E1R may have distinct execution instrumentation beyond plain E1.\\\",\"}, {\"line\": 22, \"text\": \"    \\\"Found 18 metric/source candidate files that may contain frozen E1R/core contract evidence.\\\"\"}]}, {\"line\": 26, \"matched\": [\"core_variant_result\", \"export\"], \"context\": [{\"line\": 24, \"text\": \"  \\\"risk_flags\\\": [\"}, {\"line\": 25, \"text\": \"    \\\"E1 core return differs materially from frozen E1R total return; sidecar alone must explain a large gap if E1 core is reused.\\\",\"}, {\"line\": 26, \"text\": \"    \\\"E1R UPTREND core may not be identical to current exported E1 core unless the specific core_variant_result is recovered.\\\"\"}, {\"line\": 27, \"text\": \"  ],\"}, {\"li...<truncated>"
    },
    {
      "path": "generator_candidates[7].matched_terms",
      "key": "matched_terms",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json",
        "run_stateful_simulation"
      ],
      "value": [
        "0.7957270568329264",
        "1.1919630955509348",
        "116.7435999134756",
        "25.904809362815108",
        "39.89942548515961",
        "76.844174428316",
        "E1R_REGIME_AWARE_V0_2",
        "compose_e1r_v0_2_variant",
        "core_variant_result",
        "e1r_v0_2",
        "e1r_v0_2_backtest_summary.json",
        "equity_curve",
        "export",
        "run_stateful_simulation"
      ]
    },
    {
      "path": "generator_candidates[7].matched_terms[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[7].matched_terms[6]",
      "key": "[6]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[7].matched_terms[10]",
      "key": "[10]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "e1r_v0_2_backtest_summary.json"
    },
    {
      "path": "generator_candidates[7].matched_terms[13]",
      "key": "[13]",
      "matched": [
        "run_stateful_simulation"
      ],
      "value": "run_stateful_simulation"
    },
    {
      "path": "generator_candidates[7].hits",
      "key": "hits",
      "matched": [
        "116.7435999134756"
      ],
      "value": "[{\"line\": 20, \"matched\": [\"e1r_v0_2\", \"compose_e1r_v0_2_variant\", \"core_variant_result\"], \"context\": [{\"line\": 18, \"text\": \"    \\\"E1 saved core row-derived total_return_pct is 89.8157%, while frozen E1R target total_return_pct is 116.7436%; delta=26.9279pp.\\\",\"}, {\"line\": 19, \"text\": \"    \\\"Saved sidecar is active exactly 135 rows, all expected MA_CONFLICT/SIDEWAYS intervals.\\\",\"}, {\"line\": 20, \"text\": \"    \\\"Source references core_variant_result / compose_e1r_v0_2_variant, so E1R appears to be composed from an explicit core result plus sidecar result.\\\",\"}, {\"line\": 21, \"text\": \"    \\\"Source/result terms include e1r_uptrend_execution_enabled / e1r_candidates; this suggests E1R may have distinct execution instrumentation beyond plain E1.\\\",\"}, {\"line\": 22, \"text\": \"    \\\"Found 18 metric/source candidate files that may contain frozen E1R/core contract evidence.\\\"\"}]}, {\"line\": 26, \"matched\": [\"core_variant_result\", \"export\"], \"context\": [{\"line\": 24, \"text\": \"  \\\"risk_flags\\\": [\"}, {\"line\": 25, \"text\": \"    \\\"E1 core return differs materially from frozen E1R total return; sidecar alone must explain a large gap if E1 core is reused.\\\",\"}, {\"line\": 26, \"text\": \"    \\\"E1R UPTREND core may not be identical to current exported E1 core unless the specific core_variant_result is recovered.\\\"\"}, {\"line\": 27, \"text\": \"  ],\"}, {\"line\": 28, \"text\": \"  \\\"recommended_next_action\\\": \\\"Recover or regenerate the exact E1R core_variant_result / continuous core daily equity used by frozen E1R v0.2, then compare it against exports/e1_5y_backtest_equity_curve.json before any canonical E1R composition.\\\"\"}]}, {\"line\": 28, \"matched\": [\"core_variant_result\", \"equity_curve\", \"export\"], \"context\": [{\"line\": 26, \"text\": \"    \\\"E1R UPTREND core may not be identical to current exported E1 core unle...<truncated>"
    },
    {
      "path": "generator_candidates[7].hits[7]",
      "key": "[7]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 108,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 106,
            "text": "    \"score\": 9,"
          },
          {
            "line": 107,
            "text": "    \"matched_terms\": ["
          },
          {
            "line": 108,
            "text": "      \"116.7435999134756\","
          },
          {
            "line": 109,
            "text": "      \"39.89942548515961\","
          },
          {
            "line": 110,
            "text": "      \"E1R\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[7].hits[7].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[7].hits[7].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[7].hits[7].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 106,
          "text": "    \"score\": 9,"
        },
        {
          "line": 107,
          "text": "    \"matched_terms\": ["
        },
        {
          "line": 108,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 109,
          "text": "      \"39.89942548515961\","
        },
        {
          "line": 110,
          "text": "      \"E1R\","
        }
      ]
    },
    {
      "path": "generator_candidates[7].hits[7].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 108,
        "text": "      \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[7].hits[7].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "      \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[7].hits[8]",
      "key": "[8]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 109,
        "matched": [
          "39.89942548515961"
        ],
        "context": [
          {
            "line": 107,
            "text": "    \"matched_terms\": ["
          },
          {
            "line": 108,
            "text": "      \"116.7435999134756\","
          },
          {
            "line": 109,
            "text": "      \"39.89942548515961\","
          },
          {
            "line": 110,
            "text": "      \"E1R\","
          },
          {
            "line": 111,
            "text": "      \"v0.2\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[7].hits[8].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 107,
          "text": "    \"matched_terms\": ["
        },
        {
          "line": 108,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 109,
          "text": "      \"39.89942548515961\","
        },
        {
          "line": 110,
          "text": "      \"E1R\","
        },
        {
          "line": 111,
          "text": "      \"v0.2\","
        }
      ]
    },
    {
      "path": "generator_candidates[7].hits[8].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 108,
        "text": "      \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[7].hits[8].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "      \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[7].hits[10]",
      "key": "[10]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 142,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 140,
            "text": "    \"score\": 9,"
          },
          {
            "line": 141,
            "text": "    \"matched_terms\": ["
          },
          {
            "line": 142,
            "text": "      \"116.7435999134756\","
          },
          {
            "line": 143,
            "text": "      \"39.89942548515961\","
          },
          {
            "line": 144,
            "text": "      \"E1R\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[7].hits[10].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[7].hits[10].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[7].hits[10].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 140,
          "text": "    \"score\": 9,"
        },
        {
          "line": 141,
          "text": "    \"matched_terms\": ["
        },
        {
          "line": 142,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 143,
          "text": "      \"39.89942548515961\","
        },
        {
          "line": 144,
          "text": "      \"E1R\","
        }
      ]
    },
    {
      "path": "generator_candidates[7].hits[10].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 142,
        "text": "      \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[7].hits[10].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "      \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[7].hits[11]",
      "key": "[11]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 143,
        "matched": [
          "39.89942548515961"
        ],
        "context": [
          {
            "line": 141,
            "text": "    \"matched_terms\": ["
          },
          {
            "line": 142,
            "text": "      \"116.7435999134756\","
          },
          {
            "line": 143,
            "text": "      \"39.89942548515961\","
          },
          {
            "line": 144,
            "text": "      \"E1R\","
          },
          {
            "line": 145,
            "text": "      \"v0.2\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[7].hits[11].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 141,
          "text": "    \"matched_terms\": ["
        },
        {
          "line": 142,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 143,
          "text": "      \"39.89942548515961\","
        },
        {
          "line": 144,
          "text": "      \"E1R\","
        },
        {
          "line": 145,
          "text": "      \"v0.2\","
        }
      ]
    },
    {
      "path": "generator_candidates[7].hits[11].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 142,
        "text": "      \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[7].hits[11].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "      \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[7].hits[14]",
      "key": "[14]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 177,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 175,
            "text": "    \"score\": 9,"
          },
          {
            "line": 176,
            "text": "    \"matched_terms\": ["
          },
          {
            "line": 177,
            "text": "      \"116.7435999134756\","
          },
          {
            "line": 178,
            "text": "      \"39.89942548515961\","
          },
          {
            "line": 179,
            "text": "      \"E1R\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[7].hits[14].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[7].hits[14].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[7].hits[14].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 175,
          "text": "    \"score\": 9,"
        },
        {
          "line": 176,
          "text": "    \"matched_terms\": ["
        },
        {
          "line": 177,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 178,
          "text": "      \"39.89942548515961\","
        },
        {
          "line": 179,
          "text": "      \"E1R\","
        }
      ]
    },
    {
      "path": "generator_candidates[7].hits[14].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 177,
        "text": "      \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[7].hits[14].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "      \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[7].hits[15]",
      "key": "[15]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 178,
        "matched": [
          "39.89942548515961"
        ],
        "context": [
          {
            "line": 176,
            "text": "    \"matched_terms\": ["
          },
          {
            "line": 177,
            "text": "      \"116.7435999134756\","
          },
          {
            "line": 178,
            "text": "      \"39.89942548515961\","
          },
          {
            "line": 179,
            "text": "      \"E1R\","
          },
          {
            "line": 180,
            "text": "      \"v0.2\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[7].hits[15].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 176,
          "text": "    \"matched_terms\": ["
        },
        {
          "line": 177,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 178,
          "text": "      \"39.89942548515961\","
        },
        {
          "line": 179,
          "text": "      \"E1R\","
        },
        {
          "line": 180,
          "text": "      \"v0.2\","
        }
      ]
    },
    {
      "path": "generator_candidates[7].hits[15].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 177,
        "text": "      \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[7].hits[15].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "      \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[7].hits[18]",
      "key": "[18]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 208,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 206,
            "text": "    \"score\": 9,"
          },
          {
            "line": 207,
            "text": "    \"matched_terms\": ["
          },
          {
            "line": 208,
            "text": "      \"116.7435999134756\","
          },
          {
            "line": 209,
            "text": "      \"39.89942548515961\","
          },
          {
            "line": 210,
            "text": "      \"E1R\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[7].hits[18].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[7].hits[18].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[7].hits[18].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 206,
          "text": "    \"score\": 9,"
        },
        {
          "line": 207,
          "text": "    \"matched_terms\": ["
        },
        {
          "line": 208,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 209,
          "text": "      \"39.89942548515961\","
        },
        {
          "line": 210,
          "text": "      \"E1R\","
        }
      ]
    },
    {
      "path": "generator_candidates[7].hits[18].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 208,
        "text": "      \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[7].hits[18].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "      \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[7].hits[19]",
      "key": "[19]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 209,
        "matched": [
          "39.89942548515961"
        ],
        "context": [
          {
            "line": 207,
            "text": "    \"matched_terms\": ["
          },
          {
            "line": 208,
            "text": "      \"116.7435999134756\","
          },
          {
            "line": 209,
            "text": "      \"39.89942548515961\","
          },
          {
            "line": 210,
            "text": "      \"E1R\","
          },
          {
            "line": 211,
            "text": "      \"v0.2\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[7].hits[19].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 207,
          "text": "    \"matched_terms\": ["
        },
        {
          "line": 208,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 209,
          "text": "      \"39.89942548515961\","
        },
        {
          "line": 210,
          "text": "      \"E1R\","
        },
        {
          "line": 211,
          "text": "      \"v0.2\","
        }
      ]
    },
    {
      "path": "generator_candidates[7].hits[19].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 208,
        "text": "      \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[7].hits[19].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "      \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[7].hits[21]",
      "key": "[21]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 242,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 240,
            "text": "    \"score\": 8,"
          },
          {
            "line": 241,
            "text": "    \"matched_terms\": ["
          },
          {
            "line": 242,
            "text": "      \"116.7435999134756\","
          },
          {
            "line": 243,
            "text": "      \"39.89942548515961\","
          },
          {
            "line": 244,
            "text": "      \"E1R\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[7].hits[21].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[7].hits[21].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[7].hits[21].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 240,
          "text": "    \"score\": 8,"
        },
        {
          "line": 241,
          "text": "    \"matched_terms\": ["
        },
        {
          "line": 242,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 243,
          "text": "      \"39.89942548515961\","
        },
        {
          "line": 244,
          "text": "      \"E1R\","
        }
      ]
    },
    {
      "path": "generator_candidates[7].hits[21].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 242,
        "text": "      \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[7].hits[21].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "      \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[7].hits[22]",
      "key": "[22]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 243,
        "matched": [
          "39.89942548515961"
        ],
        "context": [
          {
            "line": 241,
            "text": "    \"matched_terms\": ["
          },
          {
            "line": 242,
            "text": "      \"116.7435999134756\","
          },
          {
            "line": 243,
            "text": "      \"39.89942548515961\","
          },
          {
            "line": 244,
            "text": "      \"E1R\","
          },
          {
            "line": 245,
            "text": "      \"v0.2\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[7].hits[22].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 241,
          "text": "    \"matched_terms\": ["
        },
        {
          "line": 242,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 243,
          "text": "      \"39.89942548515961\","
        },
        {
          "line": 244,
          "text": "      \"E1R\","
        },
        {
          "line": 245,
          "text": "      \"v0.2\","
        }
      ]
    },
    {
      "path": "generator_candidates[7].hits[22].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 242,
        "text": "      \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[7].hits[22].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "      \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[7].hits[23]",
      "key": "[23]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 274,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 272,
            "text": "    \"score\": 8,"
          },
          {
            "line": 273,
            "text": "    \"matched_terms\": ["
          },
          {
            "line": 274,
            "text": "      \"116.7435999134756\","
          },
          {
            "line": 275,
            "text": "      \"39.89942548515961\","
          },
          {
            "line": 276,
            "text": "      \"E1R\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[7].hits[23].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[7].hits[23].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[7].hits[23].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 272,
          "text": "    \"score\": 8,"
        },
        {
          "line": 273,
          "text": "    \"matched_terms\": ["
        },
        {
          "line": 274,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 275,
          "text": "      \"39.89942548515961\","
        },
        {
          "line": 276,
          "text": "      \"E1R\","
        }
      ]
    },
    {
      "path": "generator_candidates[7].hits[23].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 274,
        "text": "      \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[7].hits[23].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "      \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[7].hits[24]",
      "key": "[24]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 275,
        "matched": [
          "39.89942548515961"
        ],
        "context": [
          {
            "line": 273,
            "text": "    \"matched_terms\": ["
          },
          {
            "line": 274,
            "text": "      \"116.7435999134756\","
          },
          {
            "line": 275,
            "text": "      \"39.89942548515961\","
          },
          {
            "line": 276,
            "text": "      \"E1R\","
          },
          {
            "line": 277,
            "text": "      \"compose_e1r\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[7].hits[24].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 273,
          "text": "    \"matched_terms\": ["
        },
        {
          "line": 274,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 275,
          "text": "      \"39.89942548515961\","
        },
        {
          "line": 276,
          "text": "      \"E1R\","
        },
        {
          "line": 277,
          "text": "      \"compose_e1r\","
        }
      ]
    },
    {
      "path": "generator_candidates[7].hits[24].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 274,
        "text": "      \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[7].hits[24].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "      \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[7].hits[26]",
      "key": "[26]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 302,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 300,
            "text": "    \"score\": 7,"
          },
          {
            "line": 301,
            "text": "    \"matched_terms\": ["
          },
          {
            "line": 302,
            "text": "      \"116.7435999134756\","
          },
          {
            "line": 303,
            "text": "      \"39.89942548515961\","
          },
          {
            "line": 304,
            "text": "      \"E1R\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[7].hits[26].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[7].hits[26].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[7].hits[26].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 300,
          "text": "    \"score\": 7,"
        },
        {
          "line": 301,
          "text": "    \"matched_terms\": ["
        },
        {
          "line": 302,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 303,
          "text": "      \"39.89942548515961\","
        },
        {
          "line": 304,
          "text": "      \"E1R\","
        }
      ]
    },
    {
      "path": "generator_candidates[7].hits[26].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 302,
        "text": "      \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[7].hits[26].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "      \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[7].hits[27]",
      "key": "[27]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 303,
        "matched": [
          "39.89942548515961"
        ],
        "context": [
          {
            "line": 301,
            "text": "    \"matched_terms\": ["
          },
          {
            "line": 302,
            "text": "      \"116.7435999134756\","
          },
          {
            "line": 303,
            "text": "      \"39.89942548515961\","
          },
          {
            "line": 304,
            "text": "      \"E1R\","
          },
          {
            "line": 305,
            "text": "      \"v0.2\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[7].hits[27].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 301,
          "text": "    \"matched_terms\": ["
        },
        {
          "line": 302,
          "text": "      \"116.7435999134756\","
        },
        {
          "line": 303,
          "text": "      \"39.89942548515961\","
        },
        {
          "line": 304,
          "text": "      \"E1R\","
        },
        {
          "line": 305,
          "text": "      \"v0.2\","
        }
      ]
    },
    {
      "path": "generator_candidates[7].hits[27].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 302,
        "text": "      \"116.7435999134756\","
      }
    },
    {
      "path": "generator_candidates[7].hits[27].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "      \"116.7435999134756\","
    },
    {
      "path": "generator_candidates[8]",
      "key": "[8]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json\", \"generator_score\": 128, \"base_score\": 90, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"core_variant_result\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"variant_results\"], \"hits\": [{\"line\": 36, \"matched\": [\"e1r_v0_2_backtest_summary.json\", \"e1r_v0_2\", \"export\"], \"context\": [{\"line\": 34, \"text\": \"      \\\"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3D_E1_CANONICAL_INTEGRITY_AUDIT.json\\\",\"}, {\"line\": 35, \"text\": \"      \\\"docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json\\\",\"}, {\"line\": 36, \"text\": \"      \\\"exports/e1r_v0_2_backtest_summary.json\\\",\"}, {\"line\": 37, \"text\": \"      \\\"data/research/e1r/e1r_formal_backtest_v0_1.json\\\",\"}, {\"line\": 38, \"text\": \"      \\\"data/research/e1r/e1r_phase3e_confirmed_quality_diagnostic.json\\\",\"}]}, {\"line\": 56, \"matched\": [\"e1r_v0_2\", \"export\"], \"context\": [{\"line\": 54, \"text\": \"      \\\"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3C_E1_CORE_EXPORT_REPORT.json\\\",\"}, {\"line\": 55, \"text\": \"      \\\"docs/research/E1R_V0_2_STAGE3_8E2F2C4C5_EXPORT_WRAPPER_SMOKE_REPORT.json\\\",\"}, {\"line\": 56, \"text\": \"      \\\"exports/oos_e1r_v0_2_summary.json\\\",\"}, {\"line\": 57, \"text\": \"      \\\"docs/research/E1R_V0_2_STAGE3_5_ARTIFACT_DISCOVERY_REPORT.json\\\",\"}, {\"line\": 58, \"text\": \"      \\\"docs/research/E1R_V0_2_STAGE3_8E2F2C4A1_SIDECAR_ACTIVATION_AUDIT.json\\\",\"}]}, {\"line\": 61, \"matched\": [\"export\"], \"context\": [{\"line\": 59, \"text\": \"      \\\"docs/research/E1R_V0_2_STAGE3_8E2F2C4A2_SIDECAR_RANKINGS_ACTIVATION_PROBE.json\\\",\"}, {\"line\": 60, \"te...<truncated>"
    },
    {
      "path": "generator_candidates[8].matched_terms",
      "key": "matched_terms",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": [
        "0.7957270568329264",
        "1.1919630955509348",
        "116.7435999134756",
        "25.904809362815108",
        "39.89942548515961",
        "76.844174428316",
        "E1R_REGIME_AWARE_V0_2",
        "core_variant_result",
        "daily_records",
        "e1r_v0_2",
        "e1r_v0_2_backtest_equity_curve.json",
        "e1r_v0_2_backtest_summary.json",
        "equity_curve",
        "export",
        "variant_results"
      ]
    },
    {
      "path": "generator_candidates[8].matched_terms[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[8].matched_terms[6]",
      "key": "[6]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[8].matched_terms[11]",
      "key": "[11]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "e1r_v0_2_backtest_summary.json"
    },
    {
      "path": "generator_candidates[8].hits",
      "key": "hits",
      "matched": [
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "[{\"line\": 36, \"matched\": [\"e1r_v0_2_backtest_summary.json\", \"e1r_v0_2\", \"export\"], \"context\": [{\"line\": 34, \"text\": \"      \\\"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3D_E1_CANONICAL_INTEGRITY_AUDIT.json\\\",\"}, {\"line\": 35, \"text\": \"      \\\"docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json\\\",\"}, {\"line\": 36, \"text\": \"      \\\"exports/e1r_v0_2_backtest_summary.json\\\",\"}, {\"line\": 37, \"text\": \"      \\\"data/research/e1r/e1r_formal_backtest_v0_1.json\\\",\"}, {\"line\": 38, \"text\": \"      \\\"data/research/e1r/e1r_phase3e_confirmed_quality_diagnostic.json\\\",\"}]}, {\"line\": 56, \"matched\": [\"e1r_v0_2\", \"export\"], \"context\": [{\"line\": 54, \"text\": \"      \\\"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3C_E1_CORE_EXPORT_REPORT.json\\\",\"}, {\"line\": 55, \"text\": \"      \\\"docs/research/E1R_V0_2_STAGE3_8E2F2C4C5_EXPORT_WRAPPER_SMOKE_REPORT.json\\\",\"}, {\"line\": 56, \"text\": \"      \\\"exports/oos_e1r_v0_2_summary.json\\\",\"}, {\"line\": 57, \"text\": \"      \\\"docs/research/E1R_V0_2_STAGE3_5_ARTIFACT_DISCOVERY_REPORT.json\\\",\"}, {\"line\": 58, \"text\": \"      \\\"docs/research/E1R_V0_2_STAGE3_8E2F2C4A1_SIDECAR_ACTIVATION_AUDIT.json\\\",\"}]}, {\"line\": 61, \"matched\": [\"export\"], \"context\": [{\"line\": 59, \"text\": \"      \\\"docs/research/E1R_V0_2_STAGE3_8E2F2C4A2_SIDECAR_RANKINGS_ACTIVATION_PROBE.json\\\",\"}, {\"line\": 60, \"text\": \"      \\\"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F2_E1_BACKTEST_ENTRY_AUDIT.json\\\",\"}, {\"line\": 61, \"text\": \"      \\\"exports/backtest.json\\\",\"}, {\"line\": 62, \"text\": \"      \\\"exports/portfolio_backtest.json\\\",\"}, {\"line\": 63, \"text\": \"      \\\"data/research/e1_5y/e1_baseline_parity_check.json\\\",\"}]}, {\"line\": 62, \"matched\": [\"export\"], \"context\": [{\"line\": 60, \"text\": \"      \\\"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F2_E1_BACKTEST_ENTRY_AUDIT.json\\\",\"}, {\"line\": 61, \"text\": \"   ...<truncated>"
    },
    {
      "path": "generator_candidates[8].hits[0]",
      "key": "[0]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": {
        "line": 36,
        "matched": [
          "e1r_v0_2_backtest_summary.json",
          "e1r_v0_2",
          "export"
        ],
        "context": [
          {
            "line": 34,
            "text": "      \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3D_E1_CANONICAL_INTEGRITY_AUDIT.json\","
          },
          {
            "line": 35,
            "text": "      \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json\","
          },
          {
            "line": 36,
            "text": "      \"exports/e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 37,
            "text": "      \"data/research/e1r/e1r_formal_backtest_v0_1.json\","
          },
          {
            "line": 38,
            "text": "      \"data/research/e1r/e1r_phase3e_confirmed_quality_diagnostic.json\","
          }
        ]
      }
    },
    {
      "path": "generator_candidates[8].hits[0].matched",
      "key": "matched",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": [
        "e1r_v0_2_backtest_summary.json",
        "e1r_v0_2",
        "export"
      ]
    },
    {
      "path": "generator_candidates[8].hits[0].matched[0]",
      "key": "[0]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "e1r_v0_2_backtest_summary.json"
    },
    {
      "path": "generator_candidates[8].hits[0].context",
      "key": "context",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": [
        {
          "line": 34,
          "text": "      \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3D_E1_CANONICAL_INTEGRITY_AUDIT.json\","
        },
        {
          "line": 35,
          "text": "      \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C8_DRY_RUN_GENERATION_PATH_AUDIT.json\","
        },
        {
          "line": 36,
          "text": "      \"exports/e1r_v0_2_backtest_summary.json\","
        },
        {
          "line": 37,
          "text": "      \"data/research/e1r/e1r_formal_backtest_v0_1.json\","
        },
        {
          "line": 38,
          "text": "      \"data/research/e1r/e1r_phase3e_confirmed_quality_diagnostic.json\","
        }
      ]
    },
    {
      "path": "generator_candidates[8].hits[0].context[2]",
      "key": "[2]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": {
        "line": 36,
        "text": "      \"exports/e1r_v0_2_backtest_summary.json\","
      }
    },
    {
      "path": "generator_candidates[8].hits[0].context[2].text",
      "key": "text",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "      \"exports/e1r_v0_2_backtest_summary.json\","
    },
    {
      "path": "generator_candidates[8].hits[13]",
      "key": "[13]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 96,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 94,
            "text": "  },"
          },
          {
            "line": 95,
            "text": "  \"targets\": {"
          },
          {
            "line": 96,
            "text": "    \"total_return_pct\": 116.7435999134756,"
          },
          {
            "line": 97,
            "text": "    \"spx_return_pct\": 76.844174428316,"
          },
          {
            "line": 98,
            "text": "    \"alpha_pct\": 39.89942548515961,"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[8].hits[13].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[8].hits[13].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[8].hits[13].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 94,
          "text": "  },"
        },
        {
          "line": 95,
          "text": "  \"targets\": {"
        },
        {
          "line": 96,
          "text": "    \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 97,
          "text": "    \"spx_return_pct\": 76.844174428316,"
        },
        {
          "line": 98,
          "text": "    \"alpha_pct\": 39.89942548515961,"
        }
      ]
    },
    {
      "path": "generator_candidates[8].hits[13].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 96,
        "text": "    \"total_return_pct\": 116.7435999134756,"
      }
    },
    {
      "path": "generator_candidates[8].hits[13].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "    \"total_return_pct\": 116.7435999134756,"
    },
    {
      "path": "generator_candidates[8].hits[14]",
      "key": "[14]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 97,
        "matched": [
          "76.844174428316"
        ],
        "context": [
          {
            "line": 95,
            "text": "  \"targets\": {"
          },
          {
            "line": 96,
            "text": "    \"total_return_pct\": 116.7435999134756,"
          },
          {
            "line": 97,
            "text": "    \"spx_return_pct\": 76.844174428316,"
          },
          {
            "line": 98,
            "text": "    \"alpha_pct\": 39.89942548515961,"
          },
          {
            "line": 99,
            "text": "    \"max_drawdown_pct\": 25.904809362815108,"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[8].hits[14].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 95,
          "text": "  \"targets\": {"
        },
        {
          "line": 96,
          "text": "    \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 97,
          "text": "    \"spx_return_pct\": 76.844174428316,"
        },
        {
          "line": 98,
          "text": "    \"alpha_pct\": 39.89942548515961,"
        },
        {
          "line": 99,
          "text": "    \"max_drawdown_pct\": 25.904809362815108,"
        }
      ]
    },
    {
      "path": "generator_candidates[8].hits[14].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 96,
        "text": "    \"total_return_pct\": 116.7435999134756,"
      }
    },
    {
      "path": "generator_candidates[8].hits[14].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "    \"total_return_pct\": 116.7435999134756,"
    },
    {
      "path": "generator_candidates[8].hits[15]",
      "key": "[15]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 98,
        "matched": [
          "39.89942548515961"
        ],
        "context": [
          {
            "line": 96,
            "text": "    \"total_return_pct\": 116.7435999134756,"
          },
          {
            "line": 97,
            "text": "    \"spx_return_pct\": 76.844174428316,"
          },
          {
            "line": 98,
            "text": "    \"alpha_pct\": 39.89942548515961,"
          },
          {
            "line": 99,
            "text": "    \"max_drawdown_pct\": 25.904809362815108,"
          },
          {
            "line": 100,
            "text": "    \"profit_factor\": 1.1919630955509348,"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[8].hits[15].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 96,
          "text": "    \"total_return_pct\": 116.7435999134756,"
        },
        {
          "line": 97,
          "text": "    \"spx_return_pct\": 76.844174428316,"
        },
        {
          "line": 98,
          "text": "    \"alpha_pct\": 39.89942548515961,"
        },
        {
          "line": 99,
          "text": "    \"max_drawdown_pct\": 25.904809362815108,"
        },
        {
          "line": 100,
          "text": "    \"profit_factor\": 1.1919630955509348,"
        }
      ]
    },
    {
      "path": "generator_candidates[8].hits[15].context[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 96,
        "text": "    \"total_return_pct\": 116.7435999134756,"
      }
    },
    {
      "path": "generator_candidates[8].hits[15].context[0].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "    \"total_return_pct\": 116.7435999134756,"
    },
    {
      "path": "generator_candidates[8].hits[20]",
      "key": "[20]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 127,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 125,
            "text": "        \"total_return_pct\": {"
          },
          {
            "line": 126,
            "text": "          \"key\": \"total_return_pct\","
          },
          {
            "line": 127,
            "text": "          \"value\": 116.7435999134756,"
          },
          {
            "line": 128,
            "text": "          \"target\": 116.7435999134756"
          },
          {
            "line": 129,
            "text": "        },"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[8].hits[20].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[8].hits[20].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[8].hits[20].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 125,
          "text": "        \"total_return_pct\": {"
        },
        {
          "line": 126,
          "text": "          \"key\": \"total_return_pct\","
        },
        {
          "line": 127,
          "text": "          \"value\": 116.7435999134756,"
        },
        {
          "line": 128,
          "text": "          \"target\": 116.7435999134756"
        },
        {
          "line": 129,
          "text": "        },"
        }
      ]
    },
    {
      "path": "generator_candidates[8].hits[20].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 127,
        "text": "          \"value\": 116.7435999134756,"
      }
    },
    {
      "path": "generator_candidates[8].hits[20].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "          \"value\": 116.7435999134756,"
    },
    {
      "path": "generator_candidates[8].hits[20].context[3]",
      "key": "[3]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 128,
        "text": "          \"target\": 116.7435999134756"
      }
    },
    {
      "path": "generator_candidates[8].hits[20].context[3].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "          \"target\": 116.7435999134756"
    },
    {
      "path": "generator_candidates[8].hits[21]",
      "key": "[21]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 128,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 126,
            "text": "          \"key\": \"total_return_pct\","
          },
          {
            "line": 127,
            "text": "          \"value\": 116.7435999134756,"
          },
          {
            "line": 128,
            "text": "          \"target\": 116.7435999134756"
          },
          {
            "line": 129,
            "text": "        },"
          },
          {
            "line": 130,
            "text": "        \"spx_return_pct\": {"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[8].hits[21].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[8].hits[21].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[8].hits[21].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 126,
          "text": "          \"key\": \"total_return_pct\","
        },
        {
          "line": 127,
          "text": "          \"value\": 116.7435999134756,"
        },
        {
          "line": 128,
          "text": "          \"target\": 116.7435999134756"
        },
        {
          "line": 129,
          "text": "        },"
        },
        {
          "line": 130,
          "text": "        \"spx_return_pct\": {"
        }
      ]
    },
    {
      "path": "generator_candidates[8].hits[21].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 127,
        "text": "          \"value\": 116.7435999134756,"
      }
    },
    {
      "path": "generator_candidates[8].hits[21].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "          \"value\": 116.7435999134756,"
    },
    {
      "path": "generator_candidates[8].hits[21].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 128,
        "text": "          \"target\": 116.7435999134756"
      }
    },
    {
      "path": "generator_candidates[8].hits[21].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "          \"target\": 116.7435999134756"
    },
    {
      "path": "generator_candidates[9]",
      "key": "[9]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.md\", \"generator_score\": 123, \"base_score\": 85, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"core_variant_result\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"variant_results\"], \"hits\": [{\"line\": 22, \"matched\": [\"core_variant_result\"], \"context\": [{\"line\": 20, \"text\": \"  \\\"daily_equity_candidate_count\\\": 8,\"}, {\"line\": 21, \"text\": \"  \\\"conclusion\\\": \\\"E1R_FROZEN_METRIC_ARTIFACT_FOUND_CORE_SOURCE_CANDIDATES_PRESENT\\\",\"}, {\"line\": 22, \"text\": \"  \\\"recommended_next_action\\\": \\\"Use the highest-scoring exact metric artifact to extract the nested core_variant_result / daily equity source in the next step.\\\"\"}, {\"line\": 23, \"text\": \"}\"}, {\"line\": 24, \"text\": \"```\"}]}, {\"line\": 43, \"matched\": [\"116.7435999134756\"], \"context\": [{\"line\": 41, \"text\": \"      \\\"total_return_pct\\\": {\"}, {\"line\": 42, \"text\": \"        \\\"key\\\": \\\"total_return_pct\\\",\"}, {\"line\": 43, \"text\": \"        \\\"value\\\": 116.7435999134756,\"}, {\"line\": 44, \"text\": \"        \\\"target\\\": 116.7435999134756\"}, {\"line\": 45, \"text\": \"      },\"}]}, {\"line\": 44, \"matched\": [\"116.7435999134756\"], \"context\": [{\"line\": 42, \"text\": \"        \\\"key\\\": \\\"total_return_pct\\\",\"}, {\"line\": 43, \"text\": \"        \\\"value\\\": 116.7435999134756,\"}, {\"line\": 44, \"text\": \"        \\\"target\\\": 116.7435999134756\"}, {\"line\": 45, \"text\": \"      },\"}, {\"line\": 46, \"text\": \"      \\\"spx_return_pct\\\": {\"}]}, {\"line\": 48, \"matched\": [\"76.844174428316\"], \"context\": [{\"line\": 46, \"text\": \"      \\\"spx_return_pct\\\": {\"}, {\"line\": 47, \"text\": \"        \\\"key\\\": \\\"spx_return_pct\\\",\"}, {\"line\": 48, \"text\":...<truncated>"
    },
    {
      "path": "generator_candidates[9].matched_terms",
      "key": "matched_terms",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": [
        "0.7957270568329264",
        "1.1919630955509348",
        "116.7435999134756",
        "25.904809362815108",
        "39.89942548515961",
        "76.844174428316",
        "E1R_REGIME_AWARE_V0_2",
        "core_variant_result",
        "daily_records",
        "e1r_v0_2",
        "e1r_v0_2_backtest_summary.json",
        "equity_curve",
        "export",
        "variant_results"
      ]
    },
    {
      "path": "generator_candidates[9].matched_terms[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[9].matched_terms[6]",
      "key": "[6]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[9].matched_terms[10]",
      "key": "[10]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "e1r_v0_2_backtest_summary.json"
    },
    {
      "path": "generator_candidates[9].hits",
      "key": "hits",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756",
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "[{\"line\": 22, \"matched\": [\"core_variant_result\"], \"context\": [{\"line\": 20, \"text\": \"  \\\"daily_equity_candidate_count\\\": 8,\"}, {\"line\": 21, \"text\": \"  \\\"conclusion\\\": \\\"E1R_FROZEN_METRIC_ARTIFACT_FOUND_CORE_SOURCE_CANDIDATES_PRESENT\\\",\"}, {\"line\": 22, \"text\": \"  \\\"recommended_next_action\\\": \\\"Use the highest-scoring exact metric artifact to extract the nested core_variant_result / daily equity source in the next step.\\\"\"}, {\"line\": 23, \"text\": \"}\"}, {\"line\": 24, \"text\": \"```\"}]}, {\"line\": 43, \"matched\": [\"116.7435999134756\"], \"context\": [{\"line\": 41, \"text\": \"      \\\"total_return_pct\\\": {\"}, {\"line\": 42, \"text\": \"        \\\"key\\\": \\\"total_return_pct\\\",\"}, {\"line\": 43, \"text\": \"        \\\"value\\\": 116.7435999134756,\"}, {\"line\": 44, \"text\": \"        \\\"target\\\": 116.7435999134756\"}, {\"line\": 45, \"text\": \"      },\"}]}, {\"line\": 44, \"matched\": [\"116.7435999134756\"], \"context\": [{\"line\": 42, \"text\": \"        \\\"key\\\": \\\"total_return_pct\\\",\"}, {\"line\": 43, \"text\": \"        \\\"value\\\": 116.7435999134756,\"}, {\"line\": 44, \"text\": \"        \\\"target\\\": 116.7435999134756\"}, {\"line\": 45, \"text\": \"      },\"}, {\"line\": 46, \"text\": \"      \\\"spx_return_pct\\\": {\"}]}, {\"line\": 48, \"matched\": [\"76.844174428316\"], \"context\": [{\"line\": 46, \"text\": \"      \\\"spx_return_pct\\\": {\"}, {\"line\": 47, \"text\": \"        \\\"key\\\": \\\"spx_return_pct\\\",\"}, {\"line\": 48, \"text\": \"        \\\"value\\\": 76.844174428316,\"}, {\"line\": 49, \"text\": \"        \\\"target\\\": 76.844174428316\"}, {\"line\": 50, \"text\": \"      },\"}]}, {\"line\": 49, \"matched\": [\"76.844174428316\"], \"context\": [{\"line\": 47, \"text\": \"        \\\"key\\\": \\\"spx_return_pct\\\",\"}, {\"line\": 48, \"text\": \"        \\\"value\\\": 76.844174428316,\"}, {\"line\": 49, \"text\": \"        \\\"target\\\": 76.844174428316\"}, {\"line\": 50, \"text\": \"      },\"}, {\"line\": 51, \"text\": \"      \\\"alp...<truncated>"
    },
    {
      "path": "generator_candidates[9].hits[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 43,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
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
            "line": 45,
            "text": "      },"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[9].hits[1].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[9].hits[1].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[9].hits[1].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
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
          "line": 45,
          "text": "      },"
        }
      ]
    },
    {
      "path": "generator_candidates[9].hits[1].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 43,
        "text": "        \"value\": 116.7435999134756,"
      }
    },
    {
      "path": "generator_candidates[9].hits[1].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"value\": 116.7435999134756,"
    },
    {
      "path": "generator_candidates[9].hits[1].context[3]",
      "key": "[3]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 44,
        "text": "        \"target\": 116.7435999134756"
      }
    },
    {
      "path": "generator_candidates[9].hits[1].context[3].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"target\": 116.7435999134756"
    },
    {
      "path": "generator_candidates[9].hits[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 44,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
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
            "line": 45,
            "text": "      },"
          },
          {
            "line": 46,
            "text": "      \"spx_return_pct\": {"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[9].hits[2].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    },
    {
      "path": "generator_candidates[9].hits[2].matched[0]",
      "key": "[0]",
      "matched": [
        "116.7435999134756"
      ],
      "value": "116.7435999134756"
    },
    {
      "path": "generator_candidates[9].hits[2].context",
      "key": "context",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
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
          "line": 45,
          "text": "      },"
        },
        {
          "line": 46,
          "text": "      \"spx_return_pct\": {"
        }
      ]
    },
    {
      "path": "generator_candidates[9].hits[2].context[1]",
      "key": "[1]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 43,
        "text": "        \"value\": 116.7435999134756,"
      }
    },
    {
      "path": "generator_candidates[9].hits[2].context[1].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"value\": 116.7435999134756,"
    },
    {
      "path": "generator_candidates[9].hits[2].context[2]",
      "key": "[2]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 44,
        "text": "        \"target\": 116.7435999134756"
      }
    },
    {
      "path": "generator_candidates[9].hits[2].context[2].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"target\": 116.7435999134756"
    },
    {
      "path": "generator_candidates[9].hits[13]",
      "key": "[13]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": {
        "line": 73,
        "matched": [
          "e1r_v0_2_backtest_summary.json",
          "e1r_v0_2",
          "export"
        ],
        "context": [
          {
            "line": 71,
            "text": "    },"
          },
          {
            "line": 72,
            "text": "    \"summary\": {"
          },
          {
            "line": 73,
            "text": "      \"path\": \"$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics\","
          },
          {
            "line": 74,
            "text": "      \"type\": \"dict\","
          },
          {
            "line": 75,
            "text": "      \"keys\": ["
          }
        ]
      }
    },
    {
      "path": "generator_candidates[9].hits[13].matched",
      "key": "matched",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": [
        "e1r_v0_2_backtest_summary.json",
        "e1r_v0_2",
        "export"
      ]
    },
    {
      "path": "generator_candidates[9].hits[13].matched[0]",
      "key": "[0]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "e1r_v0_2_backtest_summary.json"
    },
    {
      "path": "generator_candidates[9].hits[13].context",
      "key": "context",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": [
        {
          "line": 71,
          "text": "    },"
        },
        {
          "line": 72,
          "text": "    \"summary\": {"
        },
        {
          "line": 73,
          "text": "      \"path\": \"$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics\","
        },
        {
          "line": 74,
          "text": "      \"type\": \"dict\","
        },
        {
          "line": 75,
          "text": "      \"keys\": ["
        }
      ]
    },
    {
      "path": "generator_candidates[9].hits[13].context[2]",
      "key": "[2]",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": {
        "line": 73,
        "text": "      \"path\": \"$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics\","
      }
    },
    {
      "path": "generator_candidates[9].hits[13].context[2].text",
      "key": "text",
      "matched": [
        "e1r_v0_2_backtest_summary.json"
      ],
      "value": "      \"path\": \"$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics\","
    },
    {
      "path": "generator_candidates[9].hits[14]",
      "key": "[14]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756"
      ],
      "value": {
        "line": 86,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 84,
            "text": "      ],"
          },
          {
            "line": 85,
            "text": "      \"metric_like_values\": {"
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
            "line": 88,
            "text": "        \"spx_return_pct\": 76.844174428316,"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[9].hits[14].matched",
      "key": "matched",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": [
        "E1R_REGIME_AWARE_V0_2"
      ]
    },
    {
      "path": "generator_candidates[9].hits[14].matched[0]",
      "key": "[0]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "E1R_REGIME_AWARE_V0_2"
    },
    {
      "path": "generator_candidates[9].hits[14].context",
      "key": "context",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756"
      ],
      "value": [
        {
          "line": 84,
          "text": "      ],"
        },
        {
          "line": 85,
          "text": "      \"metric_like_values\": {"
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
          "line": 88,
          "text": "        \"spx_return_pct\": 76.844174428316,"
        }
      ]
    },
    {
      "path": "generator_candidates[9].hits[14].context[2]",
      "key": "[2]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": {
        "line": 86,
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      }
    },
    {
      "path": "generator_candidates[9].hits[14].context[2].text",
      "key": "text",
      "matched": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "value": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
    },
    {
      "path": "generator_candidates[9].hits[14].context[3]",
      "key": "[3]",
      "matched": [
        "116.7435999134756"
      ],
      "value": {
        "line": 87,
        "text": "        \"total_return_pct\": 116.7435999134756,"
      }
    },
    {
      "path": "generator_candidates[9].hits[14].context[3].text",
      "key": "text",
      "matched": [
        "116.7435999134756"
      ],
      "value": "        \"total_return_pct\": 116.7435999134756,"
    },
    {
      "path": "generator_candidates[9].hits[15]",
      "key": "[15]",
      "matched": [
        "E1R_REGIME_AWARE_V0_2",
        "116.7435999134756"
      ],
      "value": {
        "line": 87,
        "matched": [
          "116.7435999134756"
        ],
        "context": [
          {
            "line": 85,
            "text": "      \"metric_like_values\": {"
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
            "line": 88,
            "text": "        \"spx_return_pct\": 76.844174428316,"
          },
          {
            "line": 89,
            "text": "        \"alpha_pct\": 39.89942548515961,"
          }
        ]
      }
    },
    {
      "path": "generator_candidates[9].hits[15].matched",
      "key": "matched",
      "matched": [
        "116.7435999134756"
      ],
      "value": [
        "116.7435999134756"
      ]
    }
  ],
  "matched_terms": [
    "116.7435999134756",
    "D3_RISK_OFF_PLUS_SHOCK_GATE",
    "E1R_REGIME_AWARE_V0_2",
    "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
    "build_e1r_sidecar_sleeve",
    "e1r_v0_2_backtest_summary.json",
    "market_gate_enabled",
    "market_shock_daily_return",
    "market_shock_gate_enabled",
    "risk_off_below_spx_ma50",
    "run_stateful_simulation",
    "sidecar_active_by_regime",
    "sidecar_active_by_subclass"
  ]
}
```

## Market Parameter Evidence
```json
{
  "by_term": {
    "D3_RISK_OFF_PLUS_SHOCK_GATE": {
      "evidence_count": 37,
      "sample": [
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 67,
          "text": "          \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 162,
          "text": "              \"D3_RISK_OFF_PLUS_SHOCK_GATE\""
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 164,
          "text": "            \"text\": \"    \\\"D3_RISK_OFF_PLUS_SHOCK_GATE\\\",\""
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 183,
          "text": "          \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 67,
          "text": "          \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 162,
          "text": "              \"D3_RISK_OFF_PLUS_SHOCK_GATE\""
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 164,
          "text": "            \"text\": \"    \\\"D3_RISK_OFF_PLUS_SHOCK_GATE\\\",\""
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 183,
          "text": "          \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 67,
          "text": "          \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 162,
          "text": "              \"D3_RISK_OFF_PLUS_SHOCK_GATE\""
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 164,
          "text": "            \"text\": \"    \\\"D3_RISK_OFF_PLUS_SHOCK_GATE\\\",\""
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 183,
          "text": "          \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 48,
          "text": "        \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 143,
          "text": "            \"D3_RISK_OFF_PLUS_SHOCK_GATE\""
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 145,
          "text": "          \"text\": \"    \\\"D3_RISK_OFF_PLUS_SHOCK_GATE\\\",\""
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 166,
          "text": "      \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 48,
          "text": "        \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 143,
          "text": "            \"D3_RISK_OFF_PLUS_SHOCK_GATE\""
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 145,
          "text": "          \"text\": \"    \\\"D3_RISK_OFF_PLUS_SHOCK_GATE\\\",\""
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 166,
          "text": "      \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
        }
      ]
    },
    "market_gate_enabled": {
      "evidence_count": 95,
      "sample": [
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 76,
          "text": "          \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 192,
          "text": "          \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 76,
          "text": "          \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 192,
          "text": "          \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 76,
          "text": "          \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 192,
          "text": "          \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 57,
          "text": "        \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 175,
          "text": "      \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 57,
          "text": "        \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 175,
          "text": "      \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 122,
          "text": "    \"market_gate_enabled\": true,"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 201,
          "text": "    \"market_gate_enabled\": [],"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 220,
          "text": "      \"id\": \"full_115_artifact_missing_market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 221,
          "text": "      \"field\": \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 122,
          "text": "    \"market_gate_enabled\": true,"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 201,
          "text": "    \"market_gate_enabled\": [],"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 220,
          "text": "      \"id\": \"full_115_artifact_missing_market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 221,
          "text": "      \"field\": \"market_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
          "line": 229,
          "text": "      \"source_head\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_m"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
          "line": 1951,
          "text": "              \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
        }
      ]
    },
    "risk_off_below_spx_ma50": {
      "evidence_count": 65,
      "sample": [
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 79,
          "text": "          \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 195,
          "text": "          \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 79,
          "text": "          \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 195,
          "text": "          \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 79,
          "text": "          \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 195,
          "text": "          \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 60,
          "text": "        \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 178,
          "text": "      \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 60,
          "text": "        \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 178,
          "text": "      \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 123,
          "text": "    \"risk_off_below_spx_ma50\": true,"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 202,
          "text": "    \"risk_off_below_spx_ma50\": [],"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 225,
          "text": "      \"id\": \"full_115_artifact_missing_risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 226,
          "text": "      \"field\": \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 123,
          "text": "    \"risk_off_below_spx_ma50\": true,"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 202,
          "text": "    \"risk_off_below_spx_ma50\": [],"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 225,
          "text": "      \"id\": \"full_115_artifact_missing_risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 226,
          "text": "      \"field\": \"risk_off_below_spx_ma50\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
          "line": 229,
          "text": "      \"source_head\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_m"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
          "line": 1955,
          "text": "              \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
        }
      ]
    },
    "market_shock_gate_enabled": {
      "evidence_count": 84,
      "sample": [
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 78,
          "text": "          \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 194,
          "text": "          \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 78,
          "text": "          \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 194,
          "text": "          \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 78,
          "text": "          \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 194,
          "text": "          \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 59,
          "text": "        \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 177,
          "text": "      \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 59,
          "text": "        \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 177,
          "text": "      \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 124,
          "text": "    \"market_shock_gate_enabled\": true,"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 203,
          "text": "    \"market_shock_gate_enabled\": [],"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 230,
          "text": "      \"id\": \"full_115_artifact_missing_market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 231,
          "text": "      \"field\": \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 124,
          "text": "    \"market_shock_gate_enabled\": true,"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 203,
          "text": "    \"market_shock_gate_enabled\": [],"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 230,
          "text": "      \"id\": \"full_115_artifact_missing_market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 231,
          "text": "      \"field\": \"market_shock_gate_enabled\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
          "line": 229,
          "text": "      \"source_head\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_m"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
          "line": 2095,
          "text": "              \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
        }
      ]
    },
    "market_shock_daily_return": {
      "evidence_count": 81,
      "sample": [
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 77,
          "text": "          \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 193,
          "text": "          \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 77,
          "text": "          \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
          "line": 193,
          "text": "          \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 77,
          "text": "          \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
          "line": 193,
          "text": "          \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 58,
          "text": "        \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 176,
          "text": "      \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 58,
          "text": "        \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
          "line": 176,
          "text": "      \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 125,
          "text": "    \"market_shock_daily_return\": -0.02,"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 204,
          "text": "    \"market_shock_daily_return\": [],"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 235,
          "text": "      \"id\": \"full_115_artifact_missing_market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 236,
          "text": "      \"field\": \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 125,
          "text": "    \"market_shock_daily_return\": -0.02,"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 204,
          "text": "    \"market_shock_daily_return\": [],"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 235,
          "text": "      \"id\": \"full_115_artifact_missing_market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
          "line": 236,
          "text": "      \"field\": \"market_shock_daily_return\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
          "line": 229,
          "text": "      \"source_head\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_m"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
          "line": 3024,
          "text": "              \"text\": \"        \\\"market_shock_daily_return\\\": -0.02,\""
        }
      ]
    },
    "market_entry_gate": {
      "evidence_count": 0,
      "sample": []
    },
    "run_stateful_simulation": {
      "evidence_count": 168,
      "sample": [
        {
          "source": "generator_trace_json",
          "path": "generator_candidates",
          "value": "[{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json\", \"generator_score\": 166, \"base_score\": 108, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"extract_core_interval_returns\", \"run_stateful_simulation\", \"run_strategy_variant_comparison\", \"sidecar_result\", \"variant_results\", \"write_json\"], \"hits\": [{\"line\": 7, \"matched\": [\"export\"], \"context\": [{\"line\": 5, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 6, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 7, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 8, \"text\": \"    \\\"workflow_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"strategy_logic_changed\\\": false,\"}]}, {\"line\": 79, \"matched\": [\"extract_core_interval_returns\"], \"context\": [{\"line\": 77, \"text\": \"        },\"}, {\"line\": 78, \"text\": \"        {\"}, {\"line\": 79, \"text\": \"          \\\"name\\\": \\\"extract_core_interval_returns\\\",\"}, {\"line\": 80, \"text\": \"          \\\"line\\\": 94,\"}, {\"line\": 81, \"text\": \"          \\\"args\\\": [\"}]}, {\"line\": 82, \"matched\": [\"daily_equity_records\"], \"context\": [{\"line\": 80, \"text\": \"          \\\"line\\\": 94,\"}, {\"line\": 81, \"text\": \"          \\\"args\\\": [\"}, {\"line\": 82, \"text\": \"            \\\"core_daily_equity_records\\\",\"}, {\"line\": 83, \"text\": \"            \\\"sidecar_records\\\"\"}, {\"line\": 84, \"text\": \"          ],\"}]}, {\"line\": 90, \"matched\": [\"build_equity_records_from_returns\"], \"context\": [{\"line\": 88, \"text\"...<truncated>"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[0]",
          "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json\", \"generator_score\": 166, \"base_score\": 108, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"extract_core_interval_returns\", \"run_stateful_simulation\", \"run_strategy_variant_comparison\", \"sidecar_result\", \"variant_results\", \"write_json\"], \"hits\": [{\"line\": 7, \"matched\": [\"export\"], \"context\": [{\"line\": 5, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 6, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 7, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 8, \"text\": \"    \\\"workflow_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"strategy_logic_changed\\\": false,\"}]}, {\"line\": 79, \"matched\": [\"extract_core_interval_returns\"], \"context\": [{\"line\": 77, \"text\": \"        },\"}, {\"line\": 78, \"text\": \"        {\"}, {\"line\": 79, \"text\": \"          \\\"name\\\": \\\"extract_core_interval_returns\\\",\"}, {\"line\": 80, \"text\": \"          \\\"line\\\": 94,\"}, {\"line\": 81, \"text\": \"          \\\"args\\\": [\"}]}, {\"line\": 82, \"matched\": [\"daily_equity_records\"], \"context\": [{\"line\": 80, \"text\": \"          \\\"line\\\": 94,\"}, {\"line\": 81, \"text\": \"          \\\"args\\\": [\"}, {\"line\": 82, \"text\": \"            \\\"core_daily_equity_records\\\",\"}, {\"line\": 83, \"text\": \"            \\\"sidecar_records\\\"\"}, {\"line\": 84, \"text\": \"          ],\"}]}, {\"line\": 90, \"matched\": [\"build_equity_records_from_returns\"], \"context\": [{\"line\": 88, \"text\":...<truncated>"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[0].matched_terms",
          "value": [
            "0.7957270568329264",
            "1.1919630955509348",
            "116.7435999134756",
            "25.904809362815108",
            "39.89942548515961",
            "76.844174428316",
            "E1R_REGIME_AWARE_V0_2",
            "build_e1r_sidecar_sleeve",
            "build_equity_records_from_returns",
            "compose_e1r_v0_2_variant",
            "core_variant_result",
            "daily_equity_records",
            "daily_records",
            "e1r_v0_2",
            "e1r_v0_2_backtest_equity_curve.json",
            "e1r_v0_2_backtest_summary.json",
            "equity_curve",
            "export",
            "extract_core_interval_returns",
            "run_stateful_simulation",
            "run_strategy_variant_comparison",
            "sidecar_result",
            "variant_results",
            "write_json"
          ]
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[0].matched_terms[19]",
          "value": "run_stateful_simulation"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[1]",
          "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\", \"generator_score\": 166, \"base_score\": 108, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"extract_core_interval_returns\", \"run_stateful_simulation\", \"run_strategy_variant_comparison\", \"sidecar_result\", \"variant_results\", \"write_json\"], \"hits\": [{\"line\": 7, \"matched\": [\"export\"], \"context\": [{\"line\": 5, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 6, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 7, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 8, \"text\": \"    \\\"workflow_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"strategy_logic_changed\\\": false,\"}]}, {\"line\": 10, \"matched\": [\"export\"], \"context\": [{\"line\": 8, \"text\": \"    \\\"workflow_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"strategy_logic_changed\\\": false,\"}, {\"line\": 10, \"text\": \"    \\\"canonical_exports_written\\\": false,\"}, {\"line\": 11, \"text\": \"    \\\"long_backtest_run\\\": false\"}, {\"line\": 12, \"text\": \"  },\"}]}, {\"line\": 27, \"matched\": [\"E1R_REGIME_AWARE_V0_2\"], \"context\": [{\"line\": 25, \"text\": \"          \\\"line\\\": 9,\"}, {\"line\": 26, \"text\": \"          \\\"terms\\\": [\"}, {\"line\": 27, \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\"}, {\"line\": 28, \"text\": \"          ],\"}, {\"line\": 29, \"text\": \"          \\\"text\\\": \\\"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\\\"\"}]}, {\"line\": 29, \"matched\": [\"E1R_REGIME_AWARE_V0_2\"], \"co...<truncated>"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[1].matched_terms",
          "value": [
            "0.7957270568329264",
            "1.1919630955509348",
            "116.7435999134756",
            "25.904809362815108",
            "39.89942548515961",
            "76.844174428316",
            "E1R_REGIME_AWARE_V0_2",
            "build_e1r_sidecar_sleeve",
            "build_equity_records_from_returns",
            "compose_e1r_v0_2_variant",
            "core_variant_result",
            "daily_equity_records",
            "daily_records",
            "e1r_v0_2",
            "e1r_v0_2_backtest_equity_curve.json",
            "e1r_v0_2_backtest_summary.json",
            "equity_curve",
            "export",
            "extract_core_interval_returns",
            "run_stateful_simulation",
            "run_strategy_variant_comparison",
            "sidecar_result",
            "variant_results",
            "write_json"
          ]
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[1].matched_terms[19]",
          "value": "run_stateful_simulation"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[2]",
          "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json\", \"generator_score\": 161, \"base_score\": 103, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"extract_core_interval_returns\", \"run_stateful_simulation\", \"run_strategy_variant_comparison\", \"sidecar_result\", \"variant_results\", \"write_json\"], \"hits\": [{\"line\": 14, \"matched\": [\"116.7435999134756\"], \"context\": [{\"line\": 12, \"text\": \"  },\"}, {\"line\": 13, \"text\": \"  \\\"e1r_frozen_targets\\\": {\"}, {\"line\": 14, \"text\": \"    \\\"total_return_pct\\\": 116.7435999134756,\"}, {\"line\": 15, \"text\": \"    \\\"spx_return_pct\\\": 76.844174428316,\"}, {\"line\": 16, \"text\": \"    \\\"alpha_pct\\\": 39.89942548515961,\"}]}, {\"line\": 15, \"matched\": [\"76.844174428316\"], \"context\": [{\"line\": 13, \"text\": \"  \\\"e1r_frozen_targets\\\": {\"}, {\"line\": 14, \"text\": \"    \\\"total_return_pct\\\": 116.7435999134756,\"}, {\"line\": 15, \"text\": \"    \\\"spx_return_pct\\\": 76.844174428316,\"}, {\"line\": 16, \"text\": \"    \\\"alpha_pct\\\": 39.89942548515961,\"}, {\"line\": 17, \"text\": \"    \\\"max_drawdown_pct\\\": 25.904809362815108,\"}]}, {\"line\": 16, \"matched\": [\"39.89942548515961\"], \"context\": [{\"line\": 14, \"text\": \"    \\\"total_return_pct\\\": 116.7435999134756,\"}, {\"line\": 15, \"text\": \"    \\\"spx_return_pct\\\": 76.844174428316,\"}, {\"line\": 16, \"text\": \"    \\\"alpha_pct\\\": 39.89942548515961,\"}, {\"line\": 17, \"text\": \"    \\\"max_drawdown_pct\\\": 25.904809362815108,\"}, {\"line\": 18, \"text\": \"    \\\"profit_factor\\\": 1.191963095550...<truncated>"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[2].matched_terms",
          "value": [
            "0.7957270568329264",
            "1.1919630955509348",
            "116.7435999134756",
            "25.904809362815108",
            "39.89942548515961",
            "76.844174428316",
            "E1R_REGIME_AWARE_V0_2",
            "build_e1r_sidecar_sleeve",
            "build_equity_records_from_returns",
            "compose_e1r_v0_2_variant",
            "core_variant_result",
            "daily_equity_records",
            "daily_records",
            "e1r_v0_2",
            "e1r_v0_2_backtest_summary.json",
            "equity_curve",
            "export",
            "extract_core_interval_returns",
            "run_stateful_simulation",
            "run_strategy_variant_comparison",
            "sidecar_result",
            "variant_results",
            "write_json"
          ]
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[2].matched_terms[18]",
          "value": "run_stateful_simulation"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[4]",
          "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json\", \"generator_score\": 154, \"base_score\": 96, \"matched_terms\": [\"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"extract_core_interval_returns\", \"run_stateful_simulation\", \"run_strategy_variant_comparison\", \"variant_results\", \"write_json\"], \"hits\": [{\"line\": 7, \"matched\": [\"export\"], \"context\": [{\"line\": 5, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 6, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 7, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 8, \"text\": \"    \\\"state_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"workflow_changed\\\": false,\"}]}, {\"line\": 19, \"matched\": [\"export\"], \"context\": [{\"line\": 17, \"text\": \"    \\\"preliminary_decision\\\": {\"}, {\"line\": 18, \"text\": \"      \\\"dashboard_chart_should_not_use_current_e1r_backtest_equity_directly\\\": true,\"}, {\"line\": 19, \"text\": \"      \\\"reason\\\": \\\"E1R 5Y backtest equity artifact in exports is symbol-level/diagnostic rows, not one row per date.\\\",\"}, {\"line\": 20, \"text\": \"      \\\"need_next_step\\\": \\\"Either locate true portfolio-level 5Y equity outputs or generate/export canonical portfolio-level curves from existing backtest engine outputs.\\\",\"}, {\"line\": 21, \"text\": \"      \\\"proposed_canonical_export_names\\\": [\"}]}, {\"line\": 20, \"matched\": [\"export\"], \"context\": [{\"line\": 18, \"text\": \"      \\\"dashboard_chart_should_not_use_current_e1r_backtest_equity_directly\\\": true,\"}, {...<truncated>"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[4].matched_terms",
          "value": [
            "1.1919630955509348",
            "116.7435999134756",
            "25.904809362815108",
            "39.89942548515961",
            "76.844174428316",
            "E1R_REGIME_AWARE_V0_2",
            "build_e1r_sidecar_sleeve",
            "build_equity_records_from_returns",
            "compose_e1r_v0_2_variant",
            "core_variant_result",
            "daily_equity_records",
            "daily_records",
            "e1r_v0_2",
            "e1r_v0_2_backtest_equity_curve.json",
            "e1r_v0_2_backtest_summary.json",
            "equity_curve",
            "export",
            "extract_core_interval_returns",
            "run_stateful_simulation",
            "run_strategy_variant_comparison",
            "variant_results",
            "write_json"
          ]
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[4].matched_terms[18]",
          "value": "run_stateful_simulation"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[7]",
          "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.md\", \"generator_score\": 130, \"base_score\": 85, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"e1r_v0_2\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"run_stateful_simulation\"], \"hits\": [{\"line\": 20, \"matched\": [\"e1r_v0_2\", \"compose_e1r_v0_2_variant\", \"core_variant_result\"], \"context\": [{\"line\": 18, \"text\": \"    \\\"E1 saved core row-derived total_return_pct is 89.8157%, while frozen E1R target total_return_pct is 116.7436%; delta=26.9279pp.\\\",\"}, {\"line\": 19, \"text\": \"    \\\"Saved sidecar is active exactly 135 rows, all expected MA_CONFLICT/SIDEWAYS intervals.\\\",\"}, {\"line\": 20, \"text\": \"    \\\"Source references core_variant_result / compose_e1r_v0_2_variant, so E1R appears to be composed from an explicit core result plus sidecar result.\\\",\"}, {\"line\": 21, \"text\": \"    \\\"Source/result terms include e1r_uptrend_execution_enabled / e1r_candidates; this suggests E1R may have distinct execution instrumentation beyond plain E1.\\\",\"}, {\"line\": 22, \"text\": \"    \\\"Found 18 metric/source candidate files that may contain frozen E1R/core contract evidence.\\\"\"}]}, {\"line\": 26, \"matched\": [\"core_variant_result\", \"export\"], \"context\": [{\"line\": 24, \"text\": \"  \\\"risk_flags\\\": [\"}, {\"line\": 25, \"text\": \"    \\\"E1 core return differs materially from frozen E1R total return; sidecar alone must explain a large gap if E1 core is reused.\\\",\"}, {\"line\": 26, \"text\": \"    \\\"E1R UPTREND core may not be identical to current exported E1 core unless the specific core_variant_result is recovered.\\\"\"}, {\"line\": 27, \"text\": \"  ],\"}, {\"li...<truncated>"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[7].matched_terms",
          "value": [
            "0.7957270568329264",
            "1.1919630955509348",
            "116.7435999134756",
            "25.904809362815108",
            "39.89942548515961",
            "76.844174428316",
            "E1R_REGIME_AWARE_V0_2",
            "compose_e1r_v0_2_variant",
            "core_variant_result",
            "e1r_v0_2",
            "e1r_v0_2_backtest_summary.json",
            "equity_curve",
            "export",
            "run_stateful_simulation"
          ]
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[7].matched_terms[13]",
          "value": "run_stateful_simulation"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
          "line": 47,
          "text": "        \"run_stateful_simulation\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
          "line": 923,
          "text": "        \"run_stateful_simulation\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
          "line": 1798,
          "text": "        \"run_stateful_simulation\","
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
          "line": 80,
          "text": "          \"run_stateful_simulation\","
        }
      ]
    },
    "build_e1r_sidecar_sleeve": {
      "evidence_count": 99,
      "sample": [
        {
          "source": "generator_trace_json",
          "path": "generator_candidates",
          "value": "[{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json\", \"generator_score\": 166, \"base_score\": 108, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"extract_core_interval_returns\", \"run_stateful_simulation\", \"run_strategy_variant_comparison\", \"sidecar_result\", \"variant_results\", \"write_json\"], \"hits\": [{\"line\": 7, \"matched\": [\"export\"], \"context\": [{\"line\": 5, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 6, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 7, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 8, \"text\": \"    \\\"workflow_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"strategy_logic_changed\\\": false,\"}]}, {\"line\": 79, \"matched\": [\"extract_core_interval_returns\"], \"context\": [{\"line\": 77, \"text\": \"        },\"}, {\"line\": 78, \"text\": \"        {\"}, {\"line\": 79, \"text\": \"          \\\"name\\\": \\\"extract_core_interval_returns\\\",\"}, {\"line\": 80, \"text\": \"          \\\"line\\\": 94,\"}, {\"line\": 81, \"text\": \"          \\\"args\\\": [\"}]}, {\"line\": 82, \"matched\": [\"daily_equity_records\"], \"context\": [{\"line\": 80, \"text\": \"          \\\"line\\\": 94,\"}, {\"line\": 81, \"text\": \"          \\\"args\\\": [\"}, {\"line\": 82, \"text\": \"            \\\"core_daily_equity_records\\\",\"}, {\"line\": 83, \"text\": \"            \\\"sidecar_records\\\"\"}, {\"line\": 84, \"text\": \"          ],\"}]}, {\"line\": 90, \"matched\": [\"build_equity_records_from_returns\"], \"context\": [{\"line\": 88, \"text\"...<truncated>"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[0]",
          "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json\", \"generator_score\": 166, \"base_score\": 108, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"extract_core_interval_returns\", \"run_stateful_simulation\", \"run_strategy_variant_comparison\", \"sidecar_result\", \"variant_results\", \"write_json\"], \"hits\": [{\"line\": 7, \"matched\": [\"export\"], \"context\": [{\"line\": 5, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 6, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 7, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 8, \"text\": \"    \\\"workflow_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"strategy_logic_changed\\\": false,\"}]}, {\"line\": 79, \"matched\": [\"extract_core_interval_returns\"], \"context\": [{\"line\": 77, \"text\": \"        },\"}, {\"line\": 78, \"text\": \"        {\"}, {\"line\": 79, \"text\": \"          \\\"name\\\": \\\"extract_core_interval_returns\\\",\"}, {\"line\": 80, \"text\": \"          \\\"line\\\": 94,\"}, {\"line\": 81, \"text\": \"          \\\"args\\\": [\"}]}, {\"line\": 82, \"matched\": [\"daily_equity_records\"], \"context\": [{\"line\": 80, \"text\": \"          \\\"line\\\": 94,\"}, {\"line\": 81, \"text\": \"          \\\"args\\\": [\"}, {\"line\": 82, \"text\": \"            \\\"core_daily_equity_records\\\",\"}, {\"line\": 83, \"text\": \"            \\\"sidecar_records\\\"\"}, {\"line\": 84, \"text\": \"          ],\"}]}, {\"line\": 90, \"matched\": [\"build_equity_records_from_returns\"], \"context\": [{\"line\": 88, \"text\":...<truncated>"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[0].matched_terms",
          "value": [
            "0.7957270568329264",
            "1.1919630955509348",
            "116.7435999134756",
            "25.904809362815108",
            "39.89942548515961",
            "76.844174428316",
            "E1R_REGIME_AWARE_V0_2",
            "build_e1r_sidecar_sleeve",
            "build_equity_records_from_returns",
            "compose_e1r_v0_2_variant",
            "core_variant_result",
            "daily_equity_records",
            "daily_records",
            "e1r_v0_2",
            "e1r_v0_2_backtest_equity_curve.json",
            "e1r_v0_2_backtest_summary.json",
            "equity_curve",
            "export",
            "extract_core_interval_returns",
            "run_stateful_simulation",
            "run_strategy_variant_comparison",
            "sidecar_result",
            "variant_results",
            "write_json"
          ]
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[0].matched_terms[7]",
          "value": "build_e1r_sidecar_sleeve"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[1]",
          "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json\", \"generator_score\": 166, \"base_score\": 108, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"extract_core_interval_returns\", \"run_stateful_simulation\", \"run_strategy_variant_comparison\", \"sidecar_result\", \"variant_results\", \"write_json\"], \"hits\": [{\"line\": 7, \"matched\": [\"export\"], \"context\": [{\"line\": 5, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 6, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 7, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 8, \"text\": \"    \\\"workflow_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"strategy_logic_changed\\\": false,\"}]}, {\"line\": 10, \"matched\": [\"export\"], \"context\": [{\"line\": 8, \"text\": \"    \\\"workflow_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"strategy_logic_changed\\\": false,\"}, {\"line\": 10, \"text\": \"    \\\"canonical_exports_written\\\": false,\"}, {\"line\": 11, \"text\": \"    \\\"long_backtest_run\\\": false\"}, {\"line\": 12, \"text\": \"  },\"}]}, {\"line\": 27, \"matched\": [\"E1R_REGIME_AWARE_V0_2\"], \"context\": [{\"line\": 25, \"text\": \"          \\\"line\\\": 9,\"}, {\"line\": 26, \"text\": \"          \\\"terms\\\": [\"}, {\"line\": 27, \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\"}, {\"line\": 28, \"text\": \"          ],\"}, {\"line\": 29, \"text\": \"          \\\"text\\\": \\\"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\\\"\"}]}, {\"line\": 29, \"matched\": [\"E1R_REGIME_AWARE_V0_2\"], \"co...<truncated>"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[1].matched_terms",
          "value": [
            "0.7957270568329264",
            "1.1919630955509348",
            "116.7435999134756",
            "25.904809362815108",
            "39.89942548515961",
            "76.844174428316",
            "E1R_REGIME_AWARE_V0_2",
            "build_e1r_sidecar_sleeve",
            "build_equity_records_from_returns",
            "compose_e1r_v0_2_variant",
            "core_variant_result",
            "daily_equity_records",
            "daily_records",
            "e1r_v0_2",
            "e1r_v0_2_backtest_equity_curve.json",
            "e1r_v0_2_backtest_summary.json",
            "equity_curve",
            "export",
            "extract_core_interval_returns",
            "run_stateful_simulation",
            "run_strategy_variant_comparison",
            "sidecar_result",
            "variant_results",
            "write_json"
          ]
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[1].matched_terms[7]",
          "value": "build_e1r_sidecar_sleeve"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[2]",
          "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json\", \"generator_score\": 161, \"base_score\": 103, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"extract_core_interval_returns\", \"run_stateful_simulation\", \"run_strategy_variant_comparison\", \"sidecar_result\", \"variant_results\", \"write_json\"], \"hits\": [{\"line\": 14, \"matched\": [\"116.7435999134756\"], \"context\": [{\"line\": 12, \"text\": \"  },\"}, {\"line\": 13, \"text\": \"  \\\"e1r_frozen_targets\\\": {\"}, {\"line\": 14, \"text\": \"    \\\"total_return_pct\\\": 116.7435999134756,\"}, {\"line\": 15, \"text\": \"    \\\"spx_return_pct\\\": 76.844174428316,\"}, {\"line\": 16, \"text\": \"    \\\"alpha_pct\\\": 39.89942548515961,\"}]}, {\"line\": 15, \"matched\": [\"76.844174428316\"], \"context\": [{\"line\": 13, \"text\": \"  \\\"e1r_frozen_targets\\\": {\"}, {\"line\": 14, \"text\": \"    \\\"total_return_pct\\\": 116.7435999134756,\"}, {\"line\": 15, \"text\": \"    \\\"spx_return_pct\\\": 76.844174428316,\"}, {\"line\": 16, \"text\": \"    \\\"alpha_pct\\\": 39.89942548515961,\"}, {\"line\": 17, \"text\": \"    \\\"max_drawdown_pct\\\": 25.904809362815108,\"}]}, {\"line\": 16, \"matched\": [\"39.89942548515961\"], \"context\": [{\"line\": 14, \"text\": \"    \\\"total_return_pct\\\": 116.7435999134756,\"}, {\"line\": 15, \"text\": \"    \\\"spx_return_pct\\\": 76.844174428316,\"}, {\"line\": 16, \"text\": \"    \\\"alpha_pct\\\": 39.89942548515961,\"}, {\"line\": 17, \"text\": \"    \\\"max_drawdown_pct\\\": 25.904809362815108,\"}, {\"line\": 18, \"text\": \"    \\\"profit_factor\\\": 1.191963095550...<truncated>"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[2].matched_terms",
          "value": [
            "0.7957270568329264",
            "1.1919630955509348",
            "116.7435999134756",
            "25.904809362815108",
            "39.89942548515961",
            "76.844174428316",
            "E1R_REGIME_AWARE_V0_2",
            "build_e1r_sidecar_sleeve",
            "build_equity_records_from_returns",
            "compose_e1r_v0_2_variant",
            "core_variant_result",
            "daily_equity_records",
            "daily_records",
            "e1r_v0_2",
            "e1r_v0_2_backtest_summary.json",
            "equity_curve",
            "export",
            "extract_core_interval_returns",
            "run_stateful_simulation",
            "run_strategy_variant_comparison",
            "sidecar_result",
            "variant_results",
            "write_json"
          ]
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[2].matched_terms[7]",
          "value": "build_e1r_sidecar_sleeve"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[4]",
          "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json\", \"generator_score\": 154, \"base_score\": 96, \"matched_terms\": [\"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"daily_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"extract_core_interval_returns\", \"run_stateful_simulation\", \"run_strategy_variant_comparison\", \"variant_results\", \"write_json\"], \"hits\": [{\"line\": 7, \"matched\": [\"export\"], \"context\": [{\"line\": 5, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 6, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 7, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 8, \"text\": \"    \\\"state_changed\\\": false,\"}, {\"line\": 9, \"text\": \"    \\\"workflow_changed\\\": false,\"}]}, {\"line\": 19, \"matched\": [\"export\"], \"context\": [{\"line\": 17, \"text\": \"    \\\"preliminary_decision\\\": {\"}, {\"line\": 18, \"text\": \"      \\\"dashboard_chart_should_not_use_current_e1r_backtest_equity_directly\\\": true,\"}, {\"line\": 19, \"text\": \"      \\\"reason\\\": \\\"E1R 5Y backtest equity artifact in exports is symbol-level/diagnostic rows, not one row per date.\\\",\"}, {\"line\": 20, \"text\": \"      \\\"need_next_step\\\": \\\"Either locate true portfolio-level 5Y equity outputs or generate/export canonical portfolio-level curves from existing backtest engine outputs.\\\",\"}, {\"line\": 21, \"text\": \"      \\\"proposed_canonical_export_names\\\": [\"}]}, {\"line\": 20, \"matched\": [\"export\"], \"context\": [{\"line\": 18, \"text\": \"      \\\"dashboard_chart_should_not_use_current_e1r_backtest_equity_directly\\\": true,\"}, {...<truncated>"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[4].matched_terms",
          "value": [
            "1.1919630955509348",
            "116.7435999134756",
            "25.904809362815108",
            "39.89942548515961",
            "76.844174428316",
            "E1R_REGIME_AWARE_V0_2",
            "build_e1r_sidecar_sleeve",
            "build_equity_records_from_returns",
            "compose_e1r_v0_2_variant",
            "core_variant_result",
            "daily_equity_records",
            "daily_records",
            "e1r_v0_2",
            "e1r_v0_2_backtest_equity_curve.json",
            "e1r_v0_2_backtest_summary.json",
            "equity_curve",
            "export",
            "extract_core_interval_returns",
            "run_stateful_simulation",
            "run_strategy_variant_comparison",
            "variant_results",
            "write_json"
          ]
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[4].matched_terms[6]",
          "value": "build_e1r_sidecar_sleeve"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[5]",
          "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json\", \"generator_score\": 150, \"base_score\": 100, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"core_variant_result\", \"daily_equity_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"extract_core_interval_returns\", \"sidecar_result\", \"write_json\"], \"hits\": [{\"line\": 11, \"matched\": [\"export\"], \"context\": [{\"line\": 9, \"text\": \"  \\\"policy\\\": {\"}, {\"line\": 10, \"text\": \"    \\\"source_changed\\\": false,\"}, {\"line\": 11, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 12, \"text\": \"    \\\"state_changed\\\": false,\"}, {\"line\": 13, \"text\": \"    \\\"dashboard_changed\\\": false,\"}]}, {\"line\": 18, \"matched\": [\"e1r_v0_2\"], \"context\": [{\"line\": 16, \"text\": \"  \\\"question\\\": \\\"What exact symbol-level target/action inputs are available for E1R forward positions/orders?\\\",\"}, {\"line\": 17, \"text\": \"  \\\"source_files\\\": [\"}, {\"line\": 18, \"text\": \"    \\\"scripts/run_e1r_v0_2_oos.py\\\",\"}, {\"line\": 19, \"text\": \"    \\\"scripts/run_e1r_v0_2_oos_equity.py\\\",\"}, {\"line\": 20, \"text\": \"    \\\"scripts/run_e1r_v0_2_forward_performance.py\\\",\"}]}, {\"line\": 19, \"matched\": [\"e1r_v0_2\"], \"context\": [{\"line\": 17, \"text\": \"  \\\"source_files\\\": [\"}, {\"line\": 18, \"text\": \"    \\\"scripts/run_e1r_v0_2_oos.py\\\",\"}, {\"line\": 19, \"text\": \"    \\\"scripts/run_e1r_v0_2_oos_equity.py\\\",\"}, {\"line\": 20, \"text\": \"    \\\"scripts/run_e1r_v0_2_forward_performance.py\\\",\"}, {\"line\": 21, \"text\": \"    \\\"scripts/export_e1r_v0_2_status.py\\\",\"}]}, {\"line\": 20, \"matched\": [\"e1r_v0_2\"], \"c...<truncated>"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[5].matched_terms",
          "value": [
            "0.7957270568329264",
            "1.1919630955509348",
            "116.7435999134756",
            "25.904809362815108",
            "39.89942548515961",
            "76.844174428316",
            "E1R_REGIME_AWARE_V0_2",
            "build_e1r_sidecar_sleeve",
            "build_equity_records_from_returns",
            "compose_e1r_v0_2_variant",
            "core_variant_result",
            "daily_equity_records",
            "e1r_v0_2",
            "e1r_v0_2_backtest_equity_curve.json",
            "e1r_v0_2_backtest_summary.json",
            "equity_curve",
            "export",
            "extract_core_interval_returns",
            "sidecar_result",
            "write_json"
          ]
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[5].matched_terms[7]",
          "value": "build_e1r_sidecar_sleeve"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[6]",
          "value": "{\"path\": \"docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json\", \"generator_score\": 139, \"base_score\": 96, \"matched_terms\": [\"0.7957270568329264\", \"1.1919630955509348\", \"116.7435999134756\", \"25.904809362815108\", \"39.89942548515961\", \"76.844174428316\", \"E1R_REGIME_AWARE_V0_2\", \"build_e1r_sidecar_sleeve\", \"build_equity_records_from_returns\", \"compose_e1r_v0_2_variant\", \"daily_equity_records\", \"e1r_v0_2\", \"e1r_v0_2_backtest_equity_curve.json\", \"e1r_v0_2_backtest_summary.json\", \"equity_curve\", \"export\", \"sidecar_result\", \"variant_results\"], \"hits\": [{\"line\": 12, \"matched\": [\"export\"], \"context\": [{\"line\": 10, \"text\": \"    \\\"source_changed\\\": false,\"}, {\"line\": 11, \"text\": \"    \\\"dashboard_changed\\\": false,\"}, {\"line\": 12, \"text\": \"    \\\"exports_changed\\\": false,\"}, {\"line\": 13, \"text\": \"    \\\"strategy_logic_changed\\\": false\"}, {\"line\": 14, \"text\": \"  },\"}]}, {\"line\": 18, \"matched\": [\"export\"], \"context\": [{\"line\": 16, \"text\": \"  \\\"readiness\\\": {\"}, {\"line\": 17, \"text\": \"    \\\"e1_forward_start\\\": {\"}, {\"line\": 18, \"text\": \"      \\\"source\\\": \\\"exports/oos_summary.json\\\",\"}, {\"line\": 19, \"text\": \"      \\\"key\\\": \\\"oos_start_date\\\",\"}, {\"line\": 20, \"text\": \"      \\\"value\\\": \\\"2026-06-16\\\"\"}]}, {\"line\": 23, \"matched\": [\"equity_curve\"], \"context\": [{\"line\": 21, \"text\": \"    },\"}, {\"line\": 22, \"text\": \"    \\\"e1r_status_scaffold_exists\\\": true,\"}, {\"line\": 23, \"text\": \"    \\\"e1r_equity_curve_scaffold_exists\\\": true,\"}, {\"line\": 24, \"text\": \"    \\\"e1r_orders_scaffold_exists\\\": true,\"}, {\"line\": 25, \"text\": \"    \\\"e1r_positions_scaffold_exists\\\": true,\"}]}, {\"line\": 28, \"matched\": [\"export\"], \"context\": [{\"line\": 26, \"text\": \"    \\\"e1r_forward_performance_fields_exist\\\": false,\"}, {\"line\": 27, \"text\": \"    \\\"current_assessment\\\": \\\"NOT_YET_KICKED_OFF_AS_FORWARD_PERFORMANCE_T...<truncated>"
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[6].matched_terms",
          "value": [
            "0.7957270568329264",
            "1.1919630955509348",
            "116.7435999134756",
            "25.904809362815108",
            "39.89942548515961",
            "76.844174428316",
            "E1R_REGIME_AWARE_V0_2",
            "build_e1r_sidecar_sleeve",
            "build_equity_records_from_returns",
            "compose_e1r_v0_2_variant",
            "daily_equity_records",
            "e1r_v0_2",
            "e1r_v0_2_backtest_equity_curve.json",
            "e1r_v0_2_backtest_summary.json",
            "equity_curve",
            "export",
            "sidecar_result",
            "variant_results"
          ]
        },
        {
          "source": "generator_trace_json",
          "path": "generator_candidates[6].matched_terms[7]",
          "value": "build_e1r_sidecar_sleeve"
        },
        {
          "source": "clean_repo_grep",
          "file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
          "line": 35,
          "text": "        \"build_e1r_sidecar_sleeve\","
        }
      ]
    }
  },
  "blocking_missing_terms": [],
  "has_required_market_param_evidence": true,
  "has_generator_call_evidence": true
}
```

## Clean Grep Top Paths
```json
[
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
    "score": 3442,
    "hit_count": 3002,
    "matched_terms": [
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 30,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 34,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 35,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "        \"build_e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 43,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "        \"e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 47,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "        \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 339,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 352,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 360,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"          \\\"text\\\": \\\"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 367,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 372,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 380,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"          \\\"text\\\": \\\"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 816,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 829,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 837,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"          \\\"text\\\": \\\"        \\\\\\\"strategy_id\\\\\\\": \\\\\\\"E1R_REGIME_AWARE_V0_2\\\\\\\",\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 844,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 849,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 857,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"          \\\"text\\\": \\\"        \\\\\\\"strategy_id\\\\\\\": \\\\\\\"E1R_REGIME_AWARE_V0_2\\\\\\\",\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 906,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 910,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 911,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "        \"build_e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 919,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "        \"e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 923,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "        \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 989,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1002,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1010,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"          \\\"text\\\": \\\"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1017,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1022,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1030,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"          \\\"text\\\": \\\"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1438,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1451,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1459,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"          \\\"text\\\": \\\"        \\\\\\\"strategy_id\\\\\\\": \\\\\\\"E1R_REGIME_AWARE_V0_2\\\\\\\",\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1466,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1471,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1479,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"          \\\"text\\\": \\\"        \\\\\\\"strategy_id\\\\\\\": \\\\\\\"E1R_REGIME_AWARE_V0_2\\\\\\\",\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1782,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1786,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1787,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "        \"build_e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1794,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "        \"e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1798,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "        \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json",
        "line": 1808,
        "matched": [
          "116.7435999134756"
        ],
        "text": "            \"116.7435999134756\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
    "score": 1675,
    "hit_count": 1235,
    "matched_terms": [
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 6,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "  \"purpose\": \"Recover the generation chain and parameter evidence for exports/e1r_v0_2_backtest_summary.json without changing strategy logic.\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 24,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "    \"target_artifact\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 35,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "    \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 38,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 39,
        "matched": [
          "116.7435999134756"
        ],
        "text": "      \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 45,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "      \"regime_aware_logic\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 46,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"sidecar_active_by_regime\": {"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 49,
        "matched": [
          "sidecar_active_by_subclass"
        ],
        "text": "      \"sidecar_active_by_subclass\": {"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 52,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 53,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "      \"source_file\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 66,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 67,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "          \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 69,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 70,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 76,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "          \"market_gate_enabled\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 77,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "          \"market_shock_daily_return\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 78,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "          \"market_shock_gate_enabled\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 79,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "          \"risk_off_below_spx_ma50\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 80,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 81,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"sidecar_active_by_regime\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 90,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "            \"text\": \"TARGET_ARTIFACT = ROOT / \\\"exports/e1r_v0_2_backtest_summary.json\\\"\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 113,
        "matched": [
          "116.7435999134756"
        ],
        "text": "              \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 116,
        "matched": [
          "116.7435999134756"
        ],
        "text": "            \"text\": \"TARGET_RETURN = 116.7435999134756\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 130,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 132,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"text\": \"    \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 146,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "              \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 148,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "            \"text\": \"    \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 154,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "              \"sidecar_active_by_regime\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 156,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "            \"text\": \"    \\\"sidecar_active_by_regime\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 162,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "              \"D3_RISK_OFF_PLUS_SHOCK_GATE\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 164,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "            \"text\": \"    \\\"D3_RISK_OFF_PLUS_SHOCK_GATE\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 182,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 183,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "          \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 185,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 186,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 192,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "          \"market_gate_enabled\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 193,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "          \"market_shock_daily_return\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 194,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "          \"market_shock_gate_enabled\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 195,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "          \"risk_off_below_spx_ma50\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json",
        "line": 196,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"run_stateful_simulation\","
      }
    ]
  },
  {
    "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
    "score": 1675,
    "hit_count": 1235,
    "matched_terms": [
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass"
    ],
    "sample_hits": [
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 6,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "  \"purpose\": \"Recover the generation chain and parameter evidence for exports/e1r_v0_2_backtest_summary.json without changing strategy logic.\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 24,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "    \"target_artifact\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 35,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "    \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 38,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 39,
        "matched": [
          "116.7435999134756"
        ],
        "text": "      \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 45,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "      \"regime_aware_logic\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 46,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"sidecar_active_by_regime\": {"
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 49,
        "matched": [
          "sidecar_active_by_subclass"
        ],
        "text": "      \"sidecar_active_by_subclass\": {"
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 52,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 53,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "      \"source_file\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 66,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"116.7435999134756\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 67,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "          \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 69,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 70,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 76,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "          \"market_gate_enabled\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 77,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "          \"market_shock_daily_return\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 78,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "          \"market_shock_gate_enabled\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 79,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "          \"risk_off_below_spx_ma50\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 80,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"run_stateful_simulation\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 81,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"sidecar_active_by_regime\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 90,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "            \"text\": \"TARGET_ARTIFACT = ROOT / \\\"exports/e1r_v0_2_backtest_summary.json\\\"\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 113,
        "matched": [
          "116.7435999134756"
        ],
        "text": "              \"116.7435999134756\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 116,
        "matched": [
          "116.7435999134756"
        ],
        "text": "            \"text\": \"TARGET_RETURN = 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 130,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 132,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"text\": \"    \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 146,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "              \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 148,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "            \"text\": \"    \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 154,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "              \"sidecar_active_by_regime\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 156,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "            \"text\": \"    \\\"sidecar_active_by_regime\\\",\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 162,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "              \"D3_RISK_OFF_PLUS_SHOCK_GATE\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 164,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "            \"text\": \"    \\\"D3_RISK_OFF_PLUS_SHOCK_GATE\\\",\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 182,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"116.7435999134756\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 183,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "          \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 185,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 186,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 192,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "          \"market_gate_enabled\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 193,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "          \"market_shock_daily_return\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 194,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "          \"market_shock_gate_enabled\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 195,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "          \"risk_off_below_spx_ma50\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json",
        "line": 196,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"run_stateful_simulation\","
      }
    ]
  },
  {
    "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
    "score": 1675,
    "hit_count": 1235,
    "matched_terms": [
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass"
    ],
    "sample_hits": [
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 6,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "  \"purpose\": \"Recover the generation chain and parameter evidence for exports/e1r_v0_2_backtest_summary.json without changing strategy logic.\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 24,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "    \"target_artifact\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 35,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "    \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 38,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 39,
        "matched": [
          "116.7435999134756"
        ],
        "text": "      \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 45,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "      \"regime_aware_logic\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 46,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"sidecar_active_by_regime\": {"
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 49,
        "matched": [
          "sidecar_active_by_subclass"
        ],
        "text": "      \"sidecar_active_by_subclass\": {"
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 52,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 53,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "      \"source_file\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 66,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"116.7435999134756\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 67,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "          \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 69,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 70,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 76,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "          \"market_gate_enabled\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 77,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "          \"market_shock_daily_return\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 78,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "          \"market_shock_gate_enabled\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 79,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "          \"risk_off_below_spx_ma50\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 80,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"run_stateful_simulation\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 81,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"sidecar_active_by_regime\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 90,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "            \"text\": \"TARGET_ARTIFACT = ROOT / \\\"exports/e1r_v0_2_backtest_summary.json\\\"\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 113,
        "matched": [
          "116.7435999134756"
        ],
        "text": "              \"116.7435999134756\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 116,
        "matched": [
          "116.7435999134756"
        ],
        "text": "            \"text\": \"TARGET_RETURN = 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 130,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 132,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"text\": \"    \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 146,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "              \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 148,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "            \"text\": \"    \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 154,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "              \"sidecar_active_by_regime\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 156,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "            \"text\": \"    \\\"sidecar_active_by_regime\\\",\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 162,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "              \"D3_RISK_OFF_PLUS_SHOCK_GATE\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 164,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "            \"text\": \"    \\\"D3_RISK_OFF_PLUS_SHOCK_GATE\\\",\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 182,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"116.7435999134756\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 183,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "          \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 185,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 186,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 192,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "          \"market_gate_enabled\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 193,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "          \"market_shock_daily_return\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 194,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "          \"market_shock_gate_enabled\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 195,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "          \"risk_off_below_spx_ma50\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json",
        "line": 196,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"run_stateful_simulation\","
      }
    ]
  },
  {
    "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
    "score": 1674,
    "hit_count": 1234,
    "matched_terms": [
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass"
    ],
    "sample_hits": [
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 6,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "Recover the generation chain and parameter evidence for exports/e1r_v0_2_backtest_summary.json without changing strategy logic."
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 12,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "  \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 15,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "    \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 16,
        "matched": [
          "116.7435999134756"
        ],
        "text": "    \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 22,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "    \"regime_aware_logic\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 23,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "    \"sidecar_active_by_regime\": {"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 26,
        "matched": [
          "sidecar_active_by_subclass"
        ],
        "text": "    \"sidecar_active_by_subclass\": {"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 29,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "    \"variant\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 30,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "    \"source_file\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 47,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 48,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "        \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 50,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 51,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "        \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 57,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "        \"market_gate_enabled\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 58,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "        \"market_shock_daily_return\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 59,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "        \"market_shock_gate_enabled\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 60,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "        \"risk_off_below_spx_ma50\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 61,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "        \"run_stateful_simulation\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 62,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "        \"sidecar_active_by_regime\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 71,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "          \"text\": \"TARGET_ARTIFACT = ROOT / \\\"exports/e1r_v0_2_backtest_summary.json\\\"\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 94,
        "matched": [
          "116.7435999134756"
        ],
        "text": "            \"116.7435999134756\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 97,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"TARGET_RETURN = 116.7435999134756\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 111,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 113,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"    \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 127,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "            \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 129,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"text\": \"    \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 135,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "            \"sidecar_active_by_regime\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 137,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"text\": \"    \\\"sidecar_active_by_regime\\\",\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 143,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "            \"D3_RISK_OFF_PLUS_SHOCK_GATE\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 145,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "          \"text\": \"    \\\"D3_RISK_OFF_PLUS_SHOCK_GATE\\\",\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 165,
        "matched": [
          "116.7435999134756"
        ],
        "text": "      \"116.7435999134756\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 166,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "      \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 168,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 169,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "      \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 175,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "      \"market_gate_enabled\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 176,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "      \"market_shock_daily_return\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 177,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "      \"market_shock_gate_enabled\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 178,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "      \"risk_off_below_spx_ma50\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 179,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "      \"run_stateful_simulation\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 180,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"sidecar_active_by_regime\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
    "score": 1674,
    "hit_count": 1234,
    "matched_terms": [
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 6,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "Recover the generation chain and parameter evidence for exports/e1r_v0_2_backtest_summary.json without changing strategy logic."
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 12,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "  \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 15,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "    \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 16,
        "matched": [
          "116.7435999134756"
        ],
        "text": "    \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 22,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "    \"regime_aware_logic\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 23,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "    \"sidecar_active_by_regime\": {"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 26,
        "matched": [
          "sidecar_active_by_subclass"
        ],
        "text": "    \"sidecar_active_by_subclass\": {"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 29,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "    \"variant\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 30,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "    \"source_file\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 47,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 48,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "        \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 50,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 51,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "        \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 57,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "        \"market_gate_enabled\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 58,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "        \"market_shock_daily_return\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 59,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "        \"market_shock_gate_enabled\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 60,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "        \"risk_off_below_spx_ma50\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 61,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "        \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 62,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "        \"sidecar_active_by_regime\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 71,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "          \"text\": \"TARGET_ARTIFACT = ROOT / \\\"exports/e1r_v0_2_backtest_summary.json\\\"\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 94,
        "matched": [
          "116.7435999134756"
        ],
        "text": "            \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 97,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"TARGET_RETURN = 116.7435999134756\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 111,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 113,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"    \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 127,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "            \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 129,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"text\": \"    \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 135,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "            \"sidecar_active_by_regime\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 137,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"text\": \"    \\\"sidecar_active_by_regime\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 143,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "            \"D3_RISK_OFF_PLUS_SHOCK_GATE\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 145,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "          \"text\": \"    \\\"D3_RISK_OFF_PLUS_SHOCK_GATE\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 165,
        "matched": [
          "116.7435999134756"
        ],
        "text": "      \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 166,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "      \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 168,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 169,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "      \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 175,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "      \"market_gate_enabled\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 176,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "      \"market_shock_daily_return\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 177,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "      \"market_shock_gate_enabled\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 178,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "      \"risk_off_below_spx_ma50\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 179,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "      \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md",
        "line": 180,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"sidecar_active_by_regime\""
      }
    ]
  },
  {
    "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
    "score": 1421,
    "hit_count": 1261,
    "matched_terms": [
      "116.7435999134756",
      "E1R_REGIME_AWARE_V0_2"
    ],
    "sample_hits": [
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 19,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "    \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 20,
        "matched": [
          "116.7435999134756"
        ],
        "text": "    \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10105,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10114,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10123,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10132,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10141,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10150,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10159,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10168,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10177,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10186,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10195,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10204,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10213,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10222,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10231,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10240,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10249,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10258,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10267,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10276,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10285,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10294,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10303,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10312,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10321,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10330,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10339,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10348,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10357,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10366,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10375,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10384,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10393,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10402,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10411,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10420,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10429,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      },
      {
        "path": "exports/e1_e1r_research_curve_bundle_noncanonical.json",
        "line": 10438,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2_DIRECT_COMPOSED_CANDIDATE\","
      }
    ]
  },
  {
    "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
    "score": 1021,
    "hit_count": 641,
    "matched_terms": [
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass"
    ],
    "sample_hits": [
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 11,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "  \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 14,
        "matched": [
          "116.7435999134756"
        ],
        "text": "    \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 24,
        "matched": [
          "116.7435999134756"
        ],
        "text": "      \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 32,
        "matched": [
          "116.7435999134756"
        ],
        "text": "      \"value\": 116.7435999134756"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 64,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "      \"value\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 67,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"path\": \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 68,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"key\": \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 74,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"path\": \"sidecar_active_by_regime.SIDEWAYS\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 83,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 88,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 93,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "      \"value\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 109,
        "matched": [
          "116.7435999134756"
        ],
        "text": "  \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 121,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "    \"market_gate_variant\": \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 122,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "    \"market_gate_enabled\": true,"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 123,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "    \"risk_off_below_spx_ma50\": true,"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 124,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "    \"market_shock_gate_enabled\": true,"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 125,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "    \"market_shock_daily_return\": -0.02,"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 129,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "        \"text\": \"Market Gate Variant: D3_RISK_OFF_PLUS_SHOCK_GATE\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 171,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "      \"variant\": \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 201,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "    \"market_gate_enabled\": [],"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 202,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "    \"risk_off_below_spx_ma50\": [],"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 203,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "    \"market_shock_gate_enabled\": [],"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 204,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "    \"market_shock_daily_return\": [],"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 220,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "      \"id\": \"full_115_artifact_missing_market_gate_enabled\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 221,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "      \"field\": \"market_gate_enabled\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 225,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "      \"id\": \"full_115_artifact_missing_risk_off_below_spx_ma50\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 226,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "      \"field\": \"risk_off_below_spx_ma50\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 230,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "      \"id\": \"full_115_artifact_missing_market_shock_gate_enabled\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 231,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "      \"field\": \"market_shock_gate_enabled\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 235,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "      \"id\": \"full_115_artifact_missing_market_shock_daily_return\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 236,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "      \"field\": \"market_shock_daily_return\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 257,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "    \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 260,
        "matched": [
          "116.7435999134756"
        ],
        "text": "      \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 270,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 278,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"value\": 116.7435999134756"
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 310,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "        \"value\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\""
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 313,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "        \"path\": \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 314,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "        \"key\": \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 320,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "        \"path\": \"sidecar_active_by_regime.SIDEWAYS\","
      },
      {
        "path": "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 329,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"value\": \"E1R_REGIME_AWARE_V0_2\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
    "score": 1021,
    "hit_count": 641,
    "matched_terms": [
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 32,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "      \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 35,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 45,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 53,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"value\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 85,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"value\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 88,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"path\": \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 89,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"key\": \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 95,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"path\": \"sidecar_active_by_regime.SIDEWAYS\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 104,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 109,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 114,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "          \"value\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 156,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 160,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 164,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "          \"text\": \"      \\\"path\\\": \\\"$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 172,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 176,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 196,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 200,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 208,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 212,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 216,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "          \"text\": \"    \\\"file\\\": \\\"exports/e1r_v0_2_backtest_summary.json\\\"\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 232,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 236,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 248,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 268,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 272,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 280,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 300,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 304,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 316,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 336,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 340,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 352,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 372,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 376,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 384,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 404,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 408,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 416,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json",
        "line": 436,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
    "score": 1021,
    "hit_count": 641,
    "matched_terms": [
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 11,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "  \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 14,
        "matched": [
          "116.7435999134756"
        ],
        "text": "    \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 24,
        "matched": [
          "116.7435999134756"
        ],
        "text": "      \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 32,
        "matched": [
          "116.7435999134756"
        ],
        "text": "      \"value\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 64,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "      \"value\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 67,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"path\": \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 68,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"key\": \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 74,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "      \"path\": \"sidecar_active_by_regime.SIDEWAYS\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 83,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 88,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 93,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "      \"value\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 109,
        "matched": [
          "116.7435999134756"
        ],
        "text": "  \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 121,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "    \"market_gate_variant\": \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 122,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "    \"market_gate_enabled\": true,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 123,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "    \"risk_off_below_spx_ma50\": true,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 124,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "    \"market_shock_gate_enabled\": true,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 125,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "    \"market_shock_daily_return\": -0.02,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 129,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "        \"text\": \"Market Gate Variant: D3_RISK_OFF_PLUS_SHOCK_GATE\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 171,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "      \"variant\": \"D3_RISK_OFF_PLUS_SHOCK_GATE\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 201,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "    \"market_gate_enabled\": [],"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 202,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "    \"risk_off_below_spx_ma50\": [],"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 203,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "    \"market_shock_gate_enabled\": [],"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 204,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "    \"market_shock_daily_return\": [],"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 220,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "      \"id\": \"full_115_artifact_missing_market_gate_enabled\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 221,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "      \"field\": \"market_gate_enabled\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 225,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "      \"id\": \"full_115_artifact_missing_risk_off_below_spx_ma50\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 226,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "      \"field\": \"risk_off_below_spx_ma50\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 230,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "      \"id\": \"full_115_artifact_missing_market_shock_gate_enabled\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 231,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "      \"field\": \"market_shock_gate_enabled\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 235,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "      \"id\": \"full_115_artifact_missing_market_shock_daily_return\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 236,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "      \"field\": \"market_shock_daily_return\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 257,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "    \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 260,
        "matched": [
          "116.7435999134756"
        ],
        "text": "      \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 270,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"value\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 278,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"value\": 116.7435999134756"
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 310,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "        \"value\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 313,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "        \"path\": \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 314,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "        \"key\": \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 320,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "        \"path\": \"sidecar_active_by_regime.SIDEWAYS\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md",
        "line": 329,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"value\": \"E1R_REGIME_AWARE_V0_2\""
      }
    ]
  },
  {
    "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
    "score": 1021,
    "hit_count": 641,
    "matched_terms": [
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass"
    ],
    "sample_hits": [
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 32,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "      \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 35,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 45,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"value\": 116.7435999134756,"
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 53,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"value\": 116.7435999134756"
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 85,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"value\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 88,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"path\": \"sidecar_active_by_regime\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 89,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"key\": \"sidecar_active_by_regime\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 95,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"path\": \"sidecar_active_by_regime.SIDEWAYS\","
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 104,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 109,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 114,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "          \"value\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 156,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 160,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 164,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "          \"text\": \"      \\\"path\\\": \\\"$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics\\\",\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 172,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 176,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 196,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 200,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 208,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 212,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 216,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "          \"text\": \"    \\\"file\\\": \\\"exports/e1r_v0_2_backtest_summary.json\\\"\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 232,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 236,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 248,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 268,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 272,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 280,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 300,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 304,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 316,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 336,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 340,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 352,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 372,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 376,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 384,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 404,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 408,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 416,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json",
        "line": 436,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      }
    ]
  },
  {
    "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
    "score": 1021,
    "hit_count": 641,
    "matched_terms": [
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass"
    ],
    "sample_hits": [
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 32,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "      \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 35,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 45,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"value\": 116.7435999134756,"
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 53,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"value\": 116.7435999134756"
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 85,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"value\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 88,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"path\": \"sidecar_active_by_regime\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 89,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"key\": \"sidecar_active_by_regime\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 95,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"path\": \"sidecar_active_by_regime.SIDEWAYS\","
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 104,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 109,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"value\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 114,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "          \"value\": \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 156,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 160,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 164,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "          \"text\": \"      \\\"path\\\": \\\"$.inspection.exports/e1r_v0_2_backtest_summary.json.metrics\\\",\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 172,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 176,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 196,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 200,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 208,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 212,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 216,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "          \"text\": \"    \\\"file\\\": \\\"exports/e1r_v0_2_backtest_summary.json\\\"\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 232,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 236,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 248,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 268,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 272,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 280,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 300,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 304,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 316,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 336,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 340,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 352,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 372,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 376,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 384,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 404,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 408,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"target\\\": 116.7435999134756\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 416,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"total_return_pct\\\": 116.7435999134756,\""
      },
      {
        "path": "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json",
        "line": 436,
        "matched": [
          "116.7435999134756"
        ],
        "text": "          \"text\": \"        \\\"value\\\": 116.7435999134756,\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
    "score": 934,
    "hit_count": 554,
    "matched_terms": [
      "116.7435999134756",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 38,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "          \"name\": \"build_e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 49,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"name\": \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 98,
        "matched": [
          "E1R_REGIME_AWARE_V0_2",
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
          "sidecar_active_by_regime",
          "sidecar_active_by_subclass"
        ],
        "text": "      \"source_head\": \"def compose_e1r_v0_2_variant(\\n    core_variant_result: dict[str, Any],\\n    sidecar_result: dict[str, Any],\\n    initial_equity: float = 100000.0,\\n) -> dict[str, Any]:\\n    core_records = core_variant_result.get(\\\"daily_equity_records\\\", [])\\n    sidecar_records = sidecar_result.get(\\\"records\\\", [])\\n\\n    interval_records = extract_core_interval_returns(core_records, sidecar_records)\\n    equity_records = build_equity_records_from_returns(interval_records, initial_equity)\\n    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)\\n\\n    result = copy.deepcopy(core_variant_result)\\n\\n    sidecar_summary = sidecar_result.get(\\\"summary\\\", {}) or {}\\n\\n    result.update({\\n        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\\n        \\\"strategy_variant\\\": \\\"E1R_regime_aware_v0_2_formal_sidecar_sleeve\\\",\\n        \\\"version\\\": \\\"E1R-v0.2-formal-sidecar-sleeve\\\",\\n        \\\"research_status\\\": \\\"FORMAL_SIDECAR_SLEEVE_ENGINE\\\",\\n        \\\"core_total_trades\\\": core_variant_result.get(\\\"total_trades\\\"),\\n        \\\"sidecar_trade_count_approx\\\": sidecar_summary.get(\\\"trade_count_approx\\\"),\\n        \\\"combined_trade_count_note\\\": (\\n            \\\"total_trades remains inherited from E1R v0.1 core; \\\"\\n            \\\"sidecar_trade_count_approx counts daily basket holdings and is not \\\"\\n            \\\"stateful round-trip trade count.\\\"\\n        ),\\n        \\\"e1r_v0_2_composition\\\": {\\n            \\\"core_variant\\\": \\\"E1R_REGIME_AWARE_V0_1"
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 150,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "      \"function\": \"build_e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 153,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "        \"build_e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 163,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "      \"source_head\": \"def build_e1r_sidecar_sleeve(\\n    stock_dir: Path,\\n    spx_path: Path,\\n    regime_path: Path,\\n    config: E1RSidecarConfig,\\n) -> dict[str, Any]:\\n    spx = load_asset(spx_path)\\n    regimes = load_regimes(regime_path)\\n    stocks, excluded_found = load_stock_universe(stock_dir, config)\\n\\n    intervals = build_backtest_intervals(spx, regimes, config)\\n    rankings = build_daily_rankings(stocks, spx, regimes, intervals, config)\\n    records = run_daily_rebalanced_sidecar(rankings, spx, regimes, intervals, config)\\n    summary = summarize_sidecar(records, config)\\n\\n    regime_counts: dict[str, int] = {}\\n    subclass_counts: dict[str, int] = {}\\n\\n    for record in records:\\n        regime = record[\\\"regime\\\"]\\n        subclass = record[\\\"subclass\\\"]\\n        regime_counts[regime] = regime_counts.get(regime, 0) + 1\\n        if regime == \\\"SIDEWAYS\\\":\\n            subclass_counts[subclass] = subclass_counts.get(subclass, 0) + 1\\n\\n    return {\\n        \\\"engine\\\": \\\"e1r_sidecar_sleeve\\\",\\n        \\\"version\\\": \\\"v0.2_formal_sleeve_engine\\\",\\n        \\\"config\\\": {\\n            \\\"start_date\\\": config.start_date,\\n            \\\"end_date\\\": config.end_date,\\n            \\\"allowed_subclasses\\\": list(config.allowed_subclasses),\\n            \\\"top_n\\\": config.top_n,\\n            \\\"gross_exposure\\\": config.gross_exposure,\\n            \\\"min_history_days\\\": config.min_history_days,\\n            \\\"min_price\\\": config.min_price,\\n            \\\"initial_equity\\\": c"
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 167,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "      \"function\": \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 170,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "        \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 200,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "      \"source_head\": \"def run_stateful_simulation(\\n    symbols:        list[str],\\n    prices_map:     dict[str, list[float]],\\n    dates_map:      dict[str, list[str]],\\n    spx_prices:     list[float],\\n    spx_dates:      list[str],\\n    ohlc_map:       dict = None,\\n    assumptions:    dict = None,\\n    step:           int  = 1,\\n    min_history:    int  = 120,\\n    market_score_default: float = 60.0,\\n    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）\\n    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）\\n    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）\\n    ndx_dates:      list = None,\\n    sox_prices:     list = None,  # SOX 收盘价\\n    sox_dates:      list = None,\\n    vix_prices:     list = None,  # VIX 收盘价\\n    vix_dates:      list = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop\\n\\n    修正项（相比 v3）：\\n    1. SPX master calendar — 时间轴以 SPX dates 为准\\n    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐\\n    3. skipped_orders_by_reason — 跳过原因分类统计\\n    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop Backtest...\\\")\\n\\n    # ── 冻结参数 ─────────────────────────────────────────\\n    a        = assumptions or LAYER_D_ASSUMPTIONS\\n    max_pos  = a[\\\"max_positions\\\"]\\n    buy_pct  = a[\\\"buy_size\\\"]  / max_pos       # Top3: 1/3 per full slot\\n    add_pct  = a[\\\"add_size\\\"]  / max_pos       # Top3: +"
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 208,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "        \"build_e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 209,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "        \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 229,
        "matched": [
          "market_gate_enabled",
          "risk_off_below_spx_ma50",
          "market_shock_gate_enabled",
          "market_shock_daily_return"
        ],
        "text": "      \"source_head\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_spx_m"
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 373,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"text\": \"\\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 389,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "              \"text\": \"        \\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 408,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"text\": \"\\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 424,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "              \"text\": \"        \\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 589,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"keyword\": \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 590,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"This is intentionally separate from run_stateful_simulation().\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 606,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "              \"text\": \"This is intentionally separate from run_stateful_simulation().\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 1044,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "          \"keyword\": \"build_e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 1045,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "          \"text\": \"def build_e1r_sidecar_sleeve(\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 1061,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "              \"text\": \"def build_e1r_sidecar_sleeve(\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 1401,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"keyword\": \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 1402,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"def run_stateful_simulation(\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 1418,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "              \"text\": \"def run_stateful_simulation(\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 1951,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "              \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 1955,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "              \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 2095,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "              \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 2192,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "              \"text\": \"                f\\\"relstop={relative_stop_enabled} gate={market_gate_enabled} ──\\\")\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 2822,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "              \"text\": \"                    if market_gate_enabled and len(holdings) >= entry_capacity:\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 3016,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "              \"text\": \"        \\\"risk_off_below_spx_ma50\\\":   True,\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 3020,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "              \"text\": \"        \\\"market_shock_gate_enabled\\\": True,\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 3024,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "              \"text\": \"        \\\"market_shock_daily_return\\\": -0.02,\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 3051,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "              \"text\": \"        \\\"market_shock_daily_return\\\": -0.02,\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 3116,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"keyword\": \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 3117,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"_result = run_stateful_simulation(\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 3133,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "              \"text\": \"            _result = run_stateful_simulation(\""
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 3151,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"keyword\": \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 3152,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"# - Do not modify run_stateful_simulation().\","
      },
      {
        "path": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4B_ORIGINAL_ENTRYPOINT_LOCK_REPORT.json",
        "line": 3168,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "              \"text\": \"    # - Do not modify run_stateful_simulation().\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
    "score": 646,
    "hit_count": 266,
    "matched_terms": [
      "116.7435999134756",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "run_stateful_simulation",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 231,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "                \"text\": \"    \\\"build_e1r_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 239,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "                \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 271,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "                \"text\": \"    \\\"build_e1r_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 279,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "                \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 283,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "                \"text\": \"    \\\"e1r_v0_2_backtest_summary.json\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 307,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "                \"text\": \"    \\\"build_e1r_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 315,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "                \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 319,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "                \"text\": \"    \\\"e1r_v0_2_backtest_summary.json\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 327,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "                \"text\": \"    \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 334,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "              \"run_stateful_simulation\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 347,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "                \"text\": \"    \\\"build_e1r_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 355,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "                \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 359,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "                \"text\": \"    \\\"e1r_v0_2_backtest_summary.json\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 367,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "                \"text\": \"    \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 378,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "              \"e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 387,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "                \"text\": \"    \\\"build_e1r_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 395,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "                \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 399,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "                \"text\": \"    \\\"e1r_v0_2_backtest_summary.json\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 407,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "                \"text\": \"    \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 427,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "                \"text\": \"    \\\"build_e1r_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 435,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "                \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 439,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "                \"text\": \"    \\\"e1r_v0_2_backtest_summary.json\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 447,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "                \"text\": \"    \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 466,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 475,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "                \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 479,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "                \"text\": \"    \\\"e1r_v0_2_backtest_summary.json\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 487,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "                \"text\": \"    \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 1214,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "              \"e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 1236,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "                \"text\": \"    if \\\"e1r_v0_2_backtest_equity_curve.json\\\" in generator_text and \\\"e1r_v0_2_backtest_summary.json\\\" in generator_text:\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 1284,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "                \"text\": \"    next_actions.append(\\\"If composer returns only metrics plus diagnostic rows, inspect upstream run_stateful_simulation / run_strategy_variant_comparison return object.\\\")\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 1304,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "              \"run_stateful_simulation\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 1325,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "                \"text\": \"    next_actions.append(\\\"If composer returns only metrics plus diagnostic rows, inspect upstream run_stateful_simulation / run_strategy_variant_comparison return object.\\\")\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 1365,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "                \"text\": \"    next_actions.append(\\\"If composer returns only metrics plus diagnostic rows, inspect upstream run_stateful_simulation / run_strategy_variant_comparison return object.\\\")\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 1912,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "                \"text\": \"        \\\"mentions_build_e1r_sidecar_sleeve\\\": \\\"build_e1r_sidecar_sleeve\\\" in src,\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 1952,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "                \"text\": \"        \\\"mentions_build_e1r_sidecar_sleeve\\\": \\\"build_e1r_sidecar_sleeve\\\" in src,\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 2595,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 2616,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "                \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 3201,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "                \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 3205,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "                \"text\": \"        \\\"strategy_variant\\\": \\\"E1R_regime_aware_v0_2_formal_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0J_COMPOSER_CALLSITE_INSTRUMENTATION.json",
        "line": 3212,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"E1R_REGIME_AWARE_V0_2\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
    "score": 560,
    "hit_count": 260,
    "matched_terms": [
      "E1R_REGIME_AWARE_V0_2",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 17,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "    \"function\": \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 376,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "      \"market_gate_enabled\": {"
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 392,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 397,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "      \"market_shock_daily_return\": {"
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 413,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "            \"text\": \"market_shock_daily_return = float(a.get(\\\"market_shock_daily_return\\\", -0.02))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 418,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "      \"market_shock_gate_enabled\": {"
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 434,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 828,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "      \"risk_off_below_spx_ma50\": {"
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 844,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 942,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "          \"text\": \"    \\\"build_e1r_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 950,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 954,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "          \"text\": \"    \\\"e1r_v0_2_backtest_summary.json\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 962,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"    \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1048,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "          \"text\": \"    if \\\"e1r_v0_2_backtest_equity_curve.json\\\" in generator_text and \\\"e1r_v0_2_backtest_summary.json\\\" in generator_text:\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1072,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"    next_actions.append(\\\"If composer returns only metrics plus diagnostic rows, inspect upstream run_stateful_simulation / run_strategy_variant_comparison return object.\\\")\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1194,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"    \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1218,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "          \"text\": \"    \\\"market_shock_daily_return\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1226,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "          \"text\": \"    \\\"market_shock_gate_enabled\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1316,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        if isinstance(node, ast.FunctionDef) and node.name == \\\"run_stateful_simulation\\\":\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1336,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        return {\\\"error\\\": \\\"run_stateful_simulation not found\\\"}\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1418,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        if isinstance(node, ast.FunctionDef) and node.name == \\\"run_stateful_simulation\\\":\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1438,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        return {\\\"error\\\": \\\"run_stateful_simulation not found\\\"}\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1560,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        \\\"function\\\": \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1596,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        if \\\"run_stateful_simulation\\\" not in text:\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1612,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"            if \\\"run_stateful_simulation\\\" in line:\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1682,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        if \\\"run_stateful_simulation\\\" not in text:\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1698,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"            if \\\"run_stateful_simulation\\\" in line:\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1788,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        if \\\"run_stateful_simulation\\\" not in text:\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1804,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"            if \\\"run_stateful_simulation\\\" in line:\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1926,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"    run_info = funcs.get(\\\"run_stateful_simulation\\\", {})\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 1938,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 2036,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"    run_info = funcs.get(\\\"run_stateful_simulation\\\", {})\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 2048,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        \\\"run_stateful_simulation\\\",\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 2170,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        \\\"has_run_stateful_simulation\\\": \\\"run_stateful_simulation\\\" in funcs,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 2230,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        \\\"signature\\\": import_signature(\\\"src.engine.backtest\\\", \\\"run_stateful_simulation\\\"),\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 2234,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        \\\"run_stateful_simulation_summary\\\": run_info,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 2292,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        \\\"signature\\\": import_signature(\\\"src.engine.backtest\\\", \\\"run_stateful_simulation\\\"),\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 2296,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"        \\\"run_stateful_simulation_summary\\\": run_info,\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 2328,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "          \"text\": \"    build_info = funcs.get(\\\"build_e1r_sidecar_sleeve\\\", {})\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json",
        "line": 2344,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "          \"text\": \"        \\\"build_e1r_sidecar_sleeve\\\",\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
    "score": 557,
    "hit_count": 117,
    "matched_terms": [
      "116.7435999134756",
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 14,
        "matched": [
          "116.7435999134756"
        ],
        "text": "    \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 85,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 119,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 154,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 185,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 219,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 251,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 279,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 342,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 641,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 673,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "      \"path\": \"exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 676,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 695,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "        \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 696,
        "matched": [
          "sidecar_active_by_subclass"
        ],
        "text": "        \"sidecar_active_by_subclass\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 706,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 707,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 1285,
        "matched": [
          "116.7435999134756"
        ],
        "text": "        \"116.7435999134756\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 1357,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 2158,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 2193,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 2215,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 2241,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 2264,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 2293,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 2332,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"run_stateful_simulation\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 2345,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "            \"text\": \"def run_stateful_simulation(\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 2627,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 2631,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 2672,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 2697,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 2701,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "            \"text\": \"    market_shock_daily_return = float(a.get(\\\"market_shock_daily_return\\\", -0.02))\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 2789,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"                f\\\"relstop={relative_stop_enabled} gate={market_gate_enabled} ──\\\")\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 3639,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"            \\\"enabled\\\": market_gate_enabled,\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 3966,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"run_stateful_simulation\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 3979,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "            \"text\": \"            _result = run_stateful_simulation(\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 4198,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"run_stateful_simulation\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 4211,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "            \"text\": \"    # - Do not modify run_stateful_simulation().\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 4236,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "            \"text\": \"    # - Do not modify run_stateful_simulation().\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 4261,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "            \"text\": \"    # - Do not modify run_stateful_simulation().\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
        "line": 4364,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "            \"text\": \"            build_e1r_sidecar_sleeve,\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
    "score": 539,
    "hit_count": 159,
    "matched_terms": [
      "116.7435999134756",
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 27,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 29,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 553,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"text\": \"        \\\"sidecar_active_by_regime\\\": active_by_regime,\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 560,
        "matched": [
          "sidecar_active_by_subclass"
        ],
        "text": "          \"text\": \"        \\\"sidecar_active_by_subclass\\\": active_by_subclass,\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 594,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 596,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 654,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"text\": \"    result[\\\"sidecar_active_by_regime\\\"] = summary[\\\"sidecar_active_by_regime\\\"]\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 661,
        "matched": [
          "sidecar_active_by_subclass"
        ],
        "text": "          \"text\": \"    result[\\\"sidecar_active_by_subclass\\\"] = summary[\\\"sidecar_active_by_subclass\\\"]\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 668,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "          \"text\": \"        \\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 783,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 786,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"source_head\": \"def compose_e1r_v0_2_variant(\\n    core_variant_result: dict[str, Any],\\n    sidecar_result: dict[str, Any],\\n    initial_equity: float = 100000.0,\\n) -> dict[str, Any]:\\n    core_records = core_variant_result.get(\\\"daily_equity_records\\\", [])\\n    sidecar_records = sidecar_result.get(\\\"records\\\", [])\\n\\n    interval_records = extract_core_interval_returns(core_records, sidecar_records)\\n    equity_records = build_equity_records_from_returns(interval_records, initial_equity)\\n    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)\\n\\n    result = copy.deepcopy(core_variant_result)\\n\\n    sidecar_summary = sidecar_result.get(\\\"summary\\\", {}) or {}\\n\\n    result.update({\\n        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\\n        \\\"strategy_variant\\\": \\\"E1R_regime_aware_v0_2_formal_sidecar_sleeve\\\",\\n        \\\"version\\\": \\\"E1R-v0.2-formal-sidecar-sleeve\\\",\\n        \\\"research_status\\\": \\\"FORMAL_SIDECAR_SLEEVE_ENGINE\\\",\\n        \\\"core_total_trades\\\": core_variant_result.get(\\\"total_trades\\\"),\\n        \\\"sidecar_trade_count_approx\\\": sidecar_summary.get(\\\"trade_count_approx\\\"),\\n        \\\"combined_trade_count_note\\\": (\\n            \\\"total_trades remains inherited from E1R v0.1 core; \\\"\\n            \\\"sidecar_trade_count_approx counts daily basket holdings and is not \\\"\\n            \\\"stateful round-trip trade count.\\\"\\n        ),\\n        \\\"e1r_v0_2_composition\\\": {\\n            \\\"core_variant\\\": \\\"E1R_REGIME_AWARE_"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 796,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 798,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"Formal engine module for E1R_REGIME_AWARE_V0_2 sidecar sleeve.\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1038,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "          \"name\": \"build_e1r_sidecar_sleeve\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1050,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "          \"source_head\": \"def build_e1r_sidecar_sleeve(\\n    stock_dir: Path,\\n    spx_path: Path,\\n    regime_path: Path,\\n    config: E1RSidecarConfig,\\n) -> dict[str, Any]:\\n    spx = load_asset(spx_path)\\n    regimes = load_regimes(regime_path)\\n    stocks, excluded_found = load_stock_universe(stock_dir, config)\\n\\n    intervals = build_backtest_intervals(spx, regimes, config)\\n    rankings = build_daily_rankings(stocks, spx, regimes, intervals, config)\\n    records = run_daily_rebalanced_sidecar(rankings, spx, regimes, intervals, config)\\n    summary = summarize_sidecar(records, config)\\n\\n    regime_counts: dict[str, int] = {}\\n    subclass_counts: dict[str, int] = {}\\n\\n    for record in records:\\n        regime = record[\\\"regime\\\"]\\n        subclass = record[\\\"subclass\\\"]\\n        regime_counts[regime] = regime_counts.get(regime, 0) + 1\\n        if regime == \\\"SIDEWAYS\\\":\\n            subclass_counts[subclass] = subclass_counts.get(subclass, 0) + 1\\n\\n    return {\\n        \\\"engine\\\": \\\"e1r_sidecar_sleeve\\\",\\n        \\\"version\\\": \\\"v0.2_formal_sleeve_engine\\\",\\n        \\\"config\\\": {\\n            \\\"start_date\\\": config.start_date,\\n            \\\"end_date\\\": config.end_date,\\n            \\\"allowed_subclasses\\\": list(config.allowed_subclasses),\\n            \\\"top_n\\\": config.top_n,\\n            \\\"gross_exposure\\\": config.gross_exposure,\\n            \\\"min_history_days\\\": config.min_history_days,\\n            \\\"min_price\\\": config.min_price,\\n            \\\"initial_equity\\"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1308,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1310,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"            variant_results[\\\"E1R_REGIME_AWARE_V0_2\\\"] = compose_e1r_v0_2_variant(\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1353,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"name\": \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1382,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"source_head\": \"def run_stateful_simulation(\\n    symbols:        list[str],\\n    prices_map:     dict[str, list[float]],\\n    dates_map:      dict[str, list[str]],\\n    spx_prices:     list[float],\\n    spx_dates:      list[str],\\n    ohlc_map:       dict = None,\\n    assumptions:    dict = None,\\n    step:           int  = 1,\\n    min_history:    int  = 120,\\n    market_score_default: float = 60.0,\\n    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）\\n    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）\\n    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）\\n    ndx_dates:      list = None,\\n    sox_prices:     list = None,  # SOX 收盘价\\n    sox_dates:      list = None,\\n    vix_prices:     list = None,  # VIX 收盘价\\n    vix_dates:      list = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop\\n\\n    修正项（相比 v3）：\\n    1. SPX master calendar — 时间轴以 SPX dates 为准\\n    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐\\n    3. skipped_orders_by_reason — 跳过原因分类统计\\n    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop Backtest...\\\")\\n\\n    # ── 冻结参数 ─────────────────────────────────────────\\n    a        = assumptions or LAYER_D_ASSUMPTIONS\\n    max_pos  = a[\\\"max_positions\\\"]\\n    buy_pct  = a[\\\"buy_size\\\"]  / max_pos       # Top3: 1/3 per full slot\\n    add_pct  = a[\\\"add_size\\\"]  / max_pos       # Top"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1404,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1407,
        "matched": [
          "market_gate_enabled",
          "risk_off_below_spx_ma50",
          "market_shock_gate_enabled",
          "market_shock_daily_return"
        ],
        "text": "          \"source_head\": \"def run_strategy_variant_comparison(\\n    symbols: list[str],\\n    prices_map: dict[str, list[float]],\\n    dates_map: dict[str, list[str]],\\n    spx_prices: list[float],\\n    spx_dates: list[str],\\n    ndx_prices: list[float] = None,\\n    ndx_dates:  list[str]   = None,\\n    sox_prices: list[float] = None,\\n    sox_dates:  list[str]   = None,\\n    vix_prices: list[float] = None,\\n    vix_dates:  list[str]   = None,\\n) -> dict:\\n    \\\"\\\"\\\"\\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\\n\\n    V0_BASE: current Strict Top3 baseline.\\n    V1_RS95: raise entry RS threshold from 90 to 95.\\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\\n\\n    Selection policy:\\n    1. Prefer PASS over PARTIAL over FAIL.\\n    2. Within the same status, prefer higher total return.\\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\\n    \\\"\\\"\\\"\\n    logger.info(\\\"[Backtest Layer D v1.6] Strategy Variant Comparison...\\\")\\n\\n    base = {\\n        **LAYER_D_ASSUMPTIONS,\\n        \\\"market_gate_enabled\\\": False,\\n        \\\"market_shock_gate_enabled\\\": False,\\n        \\\"partial_take_profit_enabled\\\": False,\\n        \\\"block_add_after_take_profit\\\": False,\\n    }\\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\\n    _gate_v2_no_vix = {\\n        \\\"market_gate_enabled\\\":       True,\\n        \\\"risk_off_below_s"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1614,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1616,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"    v2 = extract_variant(variants, \\\"E1R_REGIME_AWARE_V0_2\\\")\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1635,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1637,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1657,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1659,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"            \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1681,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "          \"text\": \"            \\\"sidecar_active_by_regime\\\": v2.get(\\\"sidecar_active_by_regime\\\"),\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1688,
        "matched": [
          "sidecar_active_by_subclass"
        ],
        "text": "          \"text\": \"            \\\"sidecar_active_by_subclass\\\": v2.get(\\\"sidecar_active_by_subclass\\\"),\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1700,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1702,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\": v2_curve,\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1738,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1741,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"source_head\": \"def main() -> None:\\n    bt_path = ROOT / \\\"exports/backtest.json\\\"\\n    if not bt_path.exists():\\n        raise RuntimeError(\\\"Missing exports/backtest.json\\\")\\n\\n    bt = read_json(bt_path)\\n    layer_d = bt.get(\\\"backtest\\\", {}).get(\\\"results\\\", {}).get(\\\"layer_d\\\", {})\\n    variants = layer_d.get(\\\"variant_results\\\", {})\\n\\n    comparison_name = layer_d.get(\\\"name\\\")\\n\\n    v1 = extract_variant(variants, \\\"E1R_REGIME_AWARE_V0_1\\\")\\n    v2 = extract_variant(variants, \\\"E1R_REGIME_AWARE_V0_2\\\")\\n\\n    v1_records = v1.get(\\\"daily_equity_records\\\") or v1.get(\\\"equity_curve\\\") or []\\n    v2_records = v2.get(\\\"daily_equity_records\\\") or v2.get(\\\"equity_curve\\\") or []\\n\\n    v1_curve = normalize_curve(v1_records)\\n    v2_curve = normalize_curve(v2_records)\\n\\n    if len(v1_curve) < 1000:\\n        raise RuntimeError(f\\\"E1R v0.1 curve too short: {len(v1_curve)} rows. Expected 5Y-like curve.\\\")\\n\\n    if len(v2_curve) < 1000:\\n        raise RuntimeError(f\\\"E1R v0.2 curve too short: {len(v2_curve)} rows. Expected 5Y-like curve.\\\")\\n\\n    start_date = v2_curve[0][\\\"date\\\"]\\n    end_date = v2_curve[-1][\\\"date\\\"]\\n\\n    if start_date > \\\"2021-06-15\\\":\\n        raise RuntimeError(f\\\"Start date looks too recent for 5Y export: {start_date}\\\")\\n\\n    if end_date < \\\"2026-06-15\\\":\\n        raise RuntimeError(f\\\"End date looks too old for current 5Y export: {end_date}\\\")\\n\\n    summary = {\\n        \\\"generated_at\\\": datetime.now(timezone.utc).isoformat(),\\n        \\"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1885,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1887,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1940,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1952,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 1954,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"    strategy_id = status.get(\\\"strategy_id\\\", \\\"E1R_REGIME_AWARE_V0_2\\\")\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 2045,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
        "line": 2048,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"source_head\": \"def main() -> None:\\n    status_script = ROOT / \\\"scripts/export_e1r_v0_2_status.py\\\"\\n    status_path = ROOT / \\\"exports/e1r_v0_2_status.json\\\"\\n\\n    if not status_script.exists():\\n        raise RuntimeError(\\\"Missing scripts/export_e1r_v0_2_status.py\\\")\\n\\n    # Refresh the lightweight v0.2 status first.\\n    runpy.run_path(str(status_script), run_name=\\\"__main__\\\")\\n\\n    if not status_path.exists():\\n        raise RuntimeError(\\\"exports/e1r_v0_2_status.json was not generated\\\")\\n\\n    status = read_json(status_path)\\n\\n    generated_at = datetime.now(timezone.utc).isoformat()\\n    status_date = status.get(\\\"status_date\\\")\\n    strategy_id = status.get(\\\"strategy_id\\\", \\\"E1R_REGIME_AWARE_V0_2\\\")\\n    market_state = status.get(\\\"e1r_market_state\\\", \\\"UNKNOWN\\\")\\n    regime = status.get(\\\"regime\\\")\\n    subclass = status.get(\\\"subclass\\\")\\n\\n    core = status.get(\\\"core\\\", {}) or {}\\n    sidecar = status.get(\\\"sidecar\\\", {}) or {}\\n    selected = sidecar.get(\\\"selected\\\", []) or []\\n\\n    core_active = bool(core.get(\\\"active\\\"))\\n    sidecar_active = bool(sidecar.get(\\\"active\\\"))\\n\\n    phase = \\\"OOS_STATUS_SIGNAL_ONLY\\\"\\n\\n    summary = {\\n        \\\"generated_at\\\": generated_at,\\n        \\\"phase\\\": phase,\\n        \\\"strategy_id\\\": strategy_id,\\n        \\\"version\\\": status.get(\\\"version\\\"),\\n        \\\"research_status\\\": status.get(\\\"research_status\\\"),\\n        \\\"status_date\\\": status_date,\\n        \\\"market_state\\\": market_state,\\n        \\\"regim"
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
    "score": 512,
    "hit_count": 132,
    "matched_terms": [
      "116.7435999134756",
      "E1R_REGIME_AWARE_V0_2",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "run_stateful_simulation",
      "sidecar_active_by_regime",
      "sidecar_active_by_subclass"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 225,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "    \"exports/e1r_v0_2_backtest_summary.json\": {"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 241,
        "matched": [
          "sidecar_active_by_regime"
        ],
        "text": "        \"sidecar_active_by_regime\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 242,
        "matched": [
          "sidecar_active_by_subclass"
        ],
        "text": "        \"sidecar_active_by_subclass\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 251,
        "matched": [
          "116.7435999134756"
        ],
        "text": "      \"total_return_pct\": 116.7435999134756,"
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 256,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 257,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 348,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "      \"variant\": \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 360,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 464,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 466,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"    strategy_id = status.get(\\\"strategy_id\\\", \\\"E1R_REGIME_AWARE_V0_2\\\")\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 793,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 795,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"STRATEGY_ID = \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 1277,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 1279,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 1436,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 1438,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"STRATEGY_ID = \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 1814,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 1816,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"STRATEGY_ID = \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2176,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2178,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"    v2 = extract_variant(variants, \\\"E1R_REGIME_AWARE_V0_2\\\")\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2221,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2223,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2235,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2237,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"            \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2279,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2281,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"            \\\"E1R_REGIME_AWARE_V0_2\\\": v2_curve,\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2290,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "          \"text\": \"    write_json(ROOT / \\\"exports/e1r_v0_2_backtest_summary.json\\\", summary)\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2309,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "          \"text\": \"    print(\\\"Wrote exports/e1r_v0_2_backtest_summary.json\\\")\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2332,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "        \"Wrote exports/e1r_v0_2_backtest_summary.json\","
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2335,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "text": "        \"exports/e1r_v0_2_backtest_summary.json\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2501,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2503,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2649,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2651,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"STRATEGY_ID = \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2810,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 2812,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "          \"text\": \"STRATEGY_ID = \\\"E1R_REGIME_AWARE_V0_2\\\"\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 3389,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "          \"text\": \"def run_stateful_simulation(\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 3474,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "          \"text\": \"    \\\"market_gate_enabled\\\": False,\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 3481,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "          \"text\": \"    \\\"market_shock_gate_enabled\\\": False,\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json",
        "line": 3488,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "          \"text\": \"    \\\"market_shock_daily_return\\\": -0.02,\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
    "score": 507,
    "hit_count": 327,
    "matched_terms": [
      "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "build_e1r_sidecar_sleeve",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "risk_off_below_spx_ma50",
      "run_stateful_simulation"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 44,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "    \"function\": \"run_stateful_simulation\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 917,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 987,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 991,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1061,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1065,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1111,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1115,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1185,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1189,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1235,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "        \"text\": \"market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\","
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1259,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1263,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1329,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1333,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1395,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1399,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1473,
        "matched": [
          "risk_off_below_spx_ma50"
        ],
        "text": "            \"text\": \"    risk_off_below_spx_ma50 = bool(a.get(\\\"risk_off_below_spx_ma50\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1685,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1689,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "            \"text\": \"    market_shock_daily_return = float(a.get(\\\"market_shock_daily_return\\\", -0.02))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1759,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1763,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "            \"text\": \"    market_shock_daily_return = float(a.get(\\\"market_shock_daily_return\\\", -0.02))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1817,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1821,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "            \"text\": \"    market_shock_daily_return = float(a.get(\\\"market_shock_daily_return\\\", -0.02))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1891,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1895,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "            \"text\": \"    market_shock_daily_return = float(a.get(\\\"market_shock_daily_return\\\", -0.02))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1965,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"    market_shock_gate_enabled = bool(a.get(\\\"market_shock_gate_enabled\\\", True))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 1969,
        "matched": [
          "market_shock_daily_return"
        ],
        "text": "            \"text\": \"    market_shock_daily_return = float(a.get(\\\"market_shock_daily_return\\\", -0.02))\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 2075,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"        \\\"D1_NO_MARKET_GATE\\\" if not market_gate_enabled else\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 2079,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"        \\\"D2_RISK_OFF_GATE\\\" if not market_shock_gate_enabled else\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 2083,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "            \"text\": \"        \\\"D3_RISK_OFF_PLUS_SHOCK_GATE\\\"\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 2137,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"        \\\"D1_NO_MARKET_GATE\\\" if not market_gate_enabled else\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 2141,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"        \\\"D2_RISK_OFF_GATE\\\" if not market_shock_gate_enabled else\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 2145,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "            \"text\": \"        \\\"D3_RISK_OFF_PLUS_SHOCK_GATE\\\"\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 2211,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"        \\\"D1_NO_MARKET_GATE\\\" if not market_gate_enabled else\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 2215,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"        \\\"D2_RISK_OFF_GATE\\\" if not market_shock_gate_enabled else\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 2219,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "            \"text\": \"        \\\"D3_RISK_OFF_PLUS_SHOCK_GATE\\\"\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 2285,
        "matched": [
          "market_gate_enabled"
        ],
        "text": "            \"text\": \"        \\\"D1_NO_MARKET_GATE\\\" if not market_gate_enabled else\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 2289,
        "matched": [
          "market_shock_gate_enabled"
        ],
        "text": "            \"text\": \"        \\\"D2_RISK_OFF_GATE\\\" if not market_shock_gate_enabled else\""
      },
      {
        "path": "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json",
        "line": 2293,
        "matched": [
          "D3_RISK_OFF_PLUS_SHOCK_GATE"
        ],
        "text": "            \"text\": \"        \\\"D3_RISK_OFF_PLUS_SHOCK_GATE\\\"\""
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
    "score": 469,
    "hit_count": 169,
    "matched_terms": [
      "E1R_REGIME_AWARE_V0_2",
      "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
      "build_e1r_sidecar_sleeve",
      "e1r_v0_2_backtest_summary.json",
      "run_stateful_simulation"
    ],
    "sample_hits": [
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 31,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 56,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 596,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 640,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 644,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_variant\\\": \\\"E1R_regime_aware_v0_2_formal_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 655,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 680,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 684,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_variant\\\": \\\"E1R_regime_aware_v0_2_formal_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 716,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 720,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_variant\\\": \\\"E1R_regime_aware_v0_2_formal_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1032,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "              \"text\": \"        \\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1080,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "              \"text\": \"        \\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1128,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "              \"text\": \"        \\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1222,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "            \"run_stateful_simulation\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1247,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "              \"text\": \"def run_stateful_simulation(\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1326,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "            \"run_stateful_simulation\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1351,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "              \"text\": \"            _result = run_stateful_simulation(\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1378,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "            \"run_stateful_simulation\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1403,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "              \"text\": \"    # - Do not modify run_stateful_simulation().\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1447,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "              \"text\": \"            build_e1r_sidecar_sleeve,\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1507,
        "matched": [
          "build_e1r_sidecar_sleeve"
        ],
        "text": "              \"text\": \"            _sidecar_result = build_e1r_sidecar_sleeve(\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1535,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1560,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            variant_results[\\\"E1R_REGIME_AWARE_V0_2\\\"] = compose_e1r_v0_2_variant(\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1608,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            variant_results[\\\"E1R_REGIME_AWARE_V0_2\\\"] = compose_e1r_v0_2_variant(\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1656,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"            variant_results[\\\"E1R_REGIME_AWARE_V0_2\\\"] = compose_e1r_v0_2_variant(\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1804,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 1829,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"- E1R_REGIME_AWARE_V0_2 formal combined daily equity records\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 2369,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 2413,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 2417,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_variant\\\": \\\"E1R_regime_aware_v0_2_formal_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 2428,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "            \"E1R_REGIME_AWARE_V0_2\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 2453,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 2457,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_variant\\\": \\\"E1R_regime_aware_v0_2_formal_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 2489,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_id\\\": \\\"E1R_REGIME_AWARE_V0_2\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 2493,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "text": "              \"text\": \"        \\\"strategy_variant\\\": \\\"E1R_regime_aware_v0_2_formal_sidecar_sleeve\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 2805,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "              \"text\": \"        \\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 2853,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "              \"text\": \"        \\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 2901,
        "matched": [
          "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE"
        ],
        "text": "              \"text\": \"        \\\"regime_aware_logic\\\": \\\"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\\\",\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 2995,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "            \"run_stateful_simulation\""
      },
      {
        "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json",
        "line": 3020,
        "matched": [
          "run_stateful_simulation"
        ],
        "text": "              \"text\": \"def run_stateful_simulation(\""
      }
    ]
  }
]
```

## Inspected Candidate Scripts
```json
[
  {
    "path": "source_reports.scripts/run_e1r_v0_2_oos.py",
    "parse_ok": false,
    "reason": "not_python_or_missing"
  },
  {
    "path": "scripts/run_e1r_v0_2_oos.py",
    "parse_ok": true,
    "imports": [
      {
        "line": 18,
        "text": "from __future__ import annotations"
      },
      {
        "line": 20,
        "text": "import json"
      },
      {
        "line": 21,
        "text": "import runpy"
      },
      {
        "line": 22,
        "text": "from datetime import datetime, timezone"
      },
      {
        "line": 23,
        "text": "from pathlib import Path"
      },
      {
        "line": 24,
        "text": "from typing import Any, Dict, List"
      }
    ],
    "functions": [
      {
        "name": "now_iso",
        "line": 38,
        "end_line": 39
      },
      {
        "name": "read_json",
        "line": 42,
        "end_line": 48
      },
      {
        "name": "write_json",
        "line": 51,
        "end_line": 53
      },
      {
        "name": "to_float",
        "line": 56,
        "end_line": 62
      },
      {
        "name": "get_orders",
        "line": 65,
        "end_line": 70
      },
      {
        "name": "get_positions",
        "line": 73,
        "end_line": 78
      },
      {
        "name": "snapshot",
        "line": 81,
        "end_line": 87
      },
      {
        "name": "should_preserve",
        "line": 90,
        "end_line": 106
      },
      {
        "name": "restore_paper_state",
        "line": 109,
        "end_line": 203
      },
      {
        "name": "main",
        "line": 206,
        "end_line": 233
      }
    ],
    "calls": [
      {
        "line": 53,
        "text": "path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + \"\\n\")"
      },
      {
        "line": 53,
        "text": "json.dumps(obj, indent=2, ensure_ascii=False)"
      }
    ],
    "writes": [],
    "constants": [
      {
        "line": 35,
        "text": "STRATEGY_ID = \"E1R_REGIME_AWARE_V0_2\""
      }
    ]
  },
  {
    "path": "scripts/run_e1r_v0_2_oos_equity.py",
    "parse_ok": true,
    "imports": [
      {
        "line": 1,
        "text": "from __future__ import annotations"
      },
      {
        "line": 3,
        "text": "import json"
      },
      {
        "line": 4,
        "text": "from datetime import datetime, timezone"
      },
      {
        "line": 5,
        "text": "from pathlib import Path"
      },
      {
        "line": 6,
        "text": "from typing import Any"
      }
    ],
    "functions": [
      {
        "name": "read_json",
        "line": 11,
        "end_line": 14
      },
      {
        "name": "write_json",
        "line": 17,
        "end_line": 19
      },
      {
        "name": "pick",
        "line": 22,
        "end_line": 29
      },
      {
        "name": "safe_float",
        "line": 32,
        "end_line": 38
      },
      {
        "name": "extract_existing_oos_core_equity",
        "line": 41,
        "end_line": 91
      },
      {
        "name": "compute_return",
        "line": 94,
        "end_line": 97
      },
      {
        "name": "load_stock_price_map",
        "line": 101,
        "end_line": 149
      },
      {
        "name": "compute_sidecar_mtm_return",
        "line": 152,
        "end_line": 222
      },
      {
        "name": "normalize_current_sidecar_positions",
        "line": 225,
        "end_line": 245
      },
      {
        "name": "main",
        "line": 248,
        "end_line": 404
      }
    ],
    "calls": [
      {
        "line": 19,
        "text": "path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + \"\\n\")"
      },
      {
        "line": 19,
        "text": "json.dumps(obj, indent=2, ensure_ascii=False)"
      }
    ],
    "writes": [],
    "constants": [
      {
        "line": 370,
        "text": "output = {\n        \"generated_at\": generated_at,\n        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\",\n        \"phase\": \"OOS_2B_FORWARD_EQUITY_CURVE\",\n        \"equity_status\": \"OOS_EQUITY_MTM_TRACKING_SIDECAR_PAPER\",\n        \"execution_status\": \"PAPER_TRACKING_NO_REAL_EXECUTION\",\n        \"curve_type\": \"FORWARD_OOS_EQUITY\",\n        \"start_date\": records[0][\"date\"] if records else status_date,\n        \"end_date\": latest[\"date\"],\n        \"row_count\": len(records),\n        \"latest\": latest,\n        \"records\": records,\n        \"notes\": [\n            \"OOS-2B.2 adds sidecar close-to-close MTM tracking when previous positions are available.\",\n            \"Core equity bridges to existing legacy OOS equity when available.\",\n            \"Sidecar equity uses previous sidecar positions for close-to-close MTM to avoid lookahead.\",\n            \"No real orders are executed by this script.\",\n            \"OOS-2B.2 should add sidecar daily MTM and simulated/real position lifecycle.\",\n        ],\n    }"
      }
    ]
  },
  {
    "path": "scripts/run_e1r_v0_2_forward_performance.py",
    "parse_ok": true,
    "imports": [
      {
        "line": 19,
        "text": "from __future__ import annotations"
      },
      {
        "line": 21,
        "text": "import json"
      },
      {
        "line": 22,
        "text": "import runpy"
      },
      {
        "line": 23,
        "text": "from datetime import datetime, timezone"
      },
      {
        "line": 24,
        "text": "from pathlib import Path"
      },
      {
        "line": 25,
        "text": "from typing import Any, Dict"
      }
    ],
    "functions": [
      {
        "name": "now_iso",
        "line": 39,
        "end_line": 40
      },
      {
        "name": "read_json",
        "line": 43,
        "end_line": 49
      },
      {
        "name": "write_json",
        "line": 52,
        "end_line": 54
      },
      {
        "name": "to_float",
        "line": 57,
        "end_line": 63
      },
      {
        "name": "count_orders",
        "line": 66,
        "end_line": 71
      },
      {
        "name": "count_positions",
        "line": 74,
        "end_line": 79
      },
      {
        "name": "get_positions",
        "line": 82,
        "end_line": 87
      },
      {
        "name": "should_preserve",
        "line": 90,
        "end_line": 107
      },
      {
        "name": "snapshot",
        "line": 110,
        "end_line": 116
      },
      {
        "name": "restore_kickoff_ready_paper_state",
        "line": 119,
        "end_line": 215
      },
      {
        "name": "main",
        "line": 218,
        "end_line": 244
      }
    ],
    "calls": [
      {
        "line": 54,
        "text": "path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + \"\\n\")"
      },
      {
        "line": 54,
        "text": "json.dumps(obj, indent=2, ensure_ascii=False)"
      }
    ],
    "writes": [],
    "constants": [
      {
        "line": 36,
        "text": "STRATEGY_ID = \"E1R_REGIME_AWARE_V0_2\""
      }
    ]
  },
  {
    "path": "scripts/export_e1r_v0_2_status.py",
    "parse_ok": true,
    "imports": [
      {
        "line": 1,
        "text": "from __future__ import annotations"
      },
      {
        "line": 3,
        "text": "import json"
      },
      {
        "line": 4,
        "text": "import sys"
      },
      {
        "line": 5,
        "text": "from datetime import datetime, timezone"
      },
      {
        "line": 6,
        "text": "from pathlib import Path"
      },
      {
        "line": 7,
        "text": "from typing import Any"
      },
      {
        "line": 12,
        "text": "from src.engine.e1r_sidecar_sleeve import E1RSidecarConfig, build_e1r_sidecar_sleeve"
      }
    ],
    "functions": [
      {
        "name": "read_json",
        "line": 15,
        "end_line": 16
      },
      {
        "name": "write_json",
        "line": 19,
        "end_line": 21
      },
      {
        "name": "pick",
        "line": 24,
        "end_line": 31
      },
      {
        "name": "normalize_e1r_state",
        "line": 34,
        "end_line": 50
      },
      {
        "name": "extract_latest_regime",
        "line": 53,
        "end_line": 75
      },
      {
        "name": "extract_legacy_market_state",
        "line": 78,
        "end_line": 92
      },
      {
        "name": "simplify_holding",
        "line": 95,
        "end_line": 102
      },
      {
        "name": "main",
        "line": 105,
        "end_line": 213
      }
    ],
    "calls": [
      {
        "line": 21,
        "text": "path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + \"\\n\")"
      },
      {
        "line": 132,
        "text": "build_e1r_sidecar_sleeve(\n        stock_dir=stock_dir,\n        spx_path=spx_path,\n        regime_path=regime_path,\n        config=config,\n    )"
      },
      {
        "line": 21,
        "text": "json.dumps(obj, indent=2, ensure_ascii=False)"
      }
    ],
    "writes": [],
    "constants": [
      {
        "line": 132,
        "text": "sidecar_result = build_e1r_sidecar_sleeve(\n        stock_dir=stock_dir,\n        spx_path=spx_path,\n        regime_path=regime_path,\n        config=config,\n    )"
      },
      {
        "line": 163,
        "text": "status = {\n        \"generated_at\": datetime.now(timezone.utc).isoformat(),\n        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\",\n        \"version\": \"E1R-v0.2-formal-sidecar-sleeve\",\n        \"research_status\": \"FORMAL_SIDECAR_SLEEVE_ENGINE\",\n        \"status_date\": date,\n        \"e1r_market_state\": e1r_market_state,\n        \"regime\": regime,\n        \"subclass\": subclass or None,\n        \"mutually_exclusive_state_model\": True,\n        \"core\": {\n            \"strategy_id\": \"E1R_REGIME_AWARE_V0_1\",\n            \"active\": core_active,\n            \"active_condition\": \"UPTREND\",\n        },\n        \"sidecar\": {\n            \"active\": sidecar_active,\n            \"active_condition\": \"SIDEWAYS_MA_CONFLICT\",\n            \"gross_exposure\": 0.25,\n            \"top_n\": 10,\n            \"excluded_symbols\": [\"VIXY\"],\n            \"selected_count\": len(holdings),\n            \"selected\": holdings,\n            \"source_record_date\": last_record.get(\"date\") if isinstance(last_record, dict) else None,\n            \"source_record_next_date\": last_record.get(\"next_date\") if isinstance(last_record, dict) else None,\n        },\n        \"legacy_market_state\": extract_legacy_market_state(legacy_market_path),\n        \"source_files\": {\n            \"regime\": str(regime_path.relative_to(ROOT)),\n            \"stocks\": str(stock_dir.relative_to(ROOT)),\n            \"spx\": str(spx_path.relative_to(ROOT)),\n            \"legacy_market_state\": str(legacy_market_path.relative_to(ROOT)),\n        },\n        \"notes\": [\n            \"E1R v0.2 uses mutually exclusive daily market states.\",\n            \"Core is active only in UPTREND under the current v0.2 state model.\",\n            \"Sidecar is active only in SIDEWAYS_MA_CONFLICT when holdings are available.\",\n            \"This status export is a lightweight bridge for Dashboard and future OOS integration.\",\n        ],\n    }"
      }
    ]
  },
  {
    "path": "scripts/run_e1r_v0_2_sidecar_lifecycle.py",
    "parse_ok": true,
    "imports": [
      {
        "line": 1,
        "text": "from __future__ import annotations"
      },
      {
        "line": 3,
        "text": "import json"
      },
      {
        "line": 4,
        "text": "from datetime import datetime, timezone"
      },
      {
        "line": 5,
        "text": "from pathlib import Path"
      },
      {
        "line": 6,
        "text": "from typing import Any"
      }
    ],
    "functions": [
      {
        "name": "read_json",
        "line": 11,
        "end_line": 14
      },
      {
        "name": "write_json",
        "line": 17,
        "end_line": 19
      },
      {
        "name": "safe_float",
        "line": 22,
        "end_line": 28
      },
      {
        "name": "normalize_positions",
        "line": 31,
        "end_line": 61
      },
      {
        "name": "compute_lifecycle",
        "line": 64,
        "end_line": 142
      },
      {
        "name": "main",
        "line": 145,
        "end_line": 292
      }
    ],
    "calls": [
      {
        "line": 19,
        "text": "path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + \"\\n\")"
      },
      {
        "line": 19,
        "text": "json.dumps(obj, indent=2, ensure_ascii=False)"
      }
    ],
    "writes": [],
    "constants": [
      {
        "line": 178,
        "text": "latest_record = {\n        \"date\": date,\n        \"previous_date\": previous_date,\n        \"generated_at\": generated_at,\n        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\",\n        \"phase\": \"OOS_2B_3_SIDECAR_LIFECYCLE_TURNOVER\",\n        \"execution_status\": \"PAPER_TRACKING_NO_REAL_EXECUTION\",\n        \"lifecycle_status\": lifecycle_status,\n        \"market_state\": latest.get(\"market_state\"),\n        \"sidecar_active\": latest.get(\"sidecar_active\"),\n        \"sidecar_mtm_status\": latest.get(\"sidecar_mtm_status\"),\n        \"sidecar_daily_return\": latest.get(\"sidecar_daily_return\"),\n        \"sidecar_equity\": latest.get(\"sidecar_equity\"),\n        **lifecycle,\n    }"
      },
      {
        "line": 203,
        "text": "lifecycle_output = {\n        \"generated_at\": generated_at,\n        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\",\n        \"phase\": \"OOS_2B_3_SIDECAR_LIFECYCLE_TURNOVER\",\n        \"execution_status\": \"PAPER_TRACKING_NO_REAL_EXECUTION\",\n        \"source\": \"exports/oos_e1r_v0_2_equity_curve.json\",\n        \"start_date\": history[0][\"date\"] if history else date,\n        \"end_date\": history[-1][\"date\"] if history else date,\n        \"row_count\": len(history),\n        \"latest\": latest_record,\n        \"records\": history,\n        \"notes\": [\n            \"Tracks sidecar target position changes day by day.\",\n            \"Calculates entered/exited/stayed symbols and target-weight turnover.\",\n            \"Still paper tracking only; no real orders, no fills, no broker execution.\",\n            \"One-way turnover uses 0.5 * sum(abs(weight_delta)).\",\n        ],\n    }"
      },
      {
        "line": 222,
        "text": "turnover_latest = {\n        \"date\": date,\n        \"previous_date\": previous_date,\n        \"generated_at\": generated_at,\n        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\",\n        \"phase\": \"OOS_2B_3_SIDECAR_TURNOVER\",\n        \"execution_status\": \"PAPER_TRACKING_NO_REAL_EXECUTION\",\n        \"market_state\": latest.get(\"market_state\"),\n        \"sidecar_active\": latest.get(\"sidecar_active\"),\n        \"lifecycle_status\": lifecycle_status,\n        \"previous_count\": lifecycle[\"previous_count\"],\n        \"current_count\": lifecycle[\"current_count\"],\n        \"entered_count\": lifecycle[\"entered_count\"],\n        \"exited_count\": lifecycle[\"exited_count\"],\n        \"stayed_count\": lifecycle[\"stayed_count\"],\n        \"gross_added_weight\": lifecycle[\"gross_added_weight\"],\n        \"gross_removed_weight\": lifecycle[\"gross_removed_weight\"],\n        \"two_way_turnover\": lifecycle[\"two_way_turnover\"],\n        \"one_way_turnover\": lifecycle[\"one_way_turnover\"],\n        \"entered_symbols\": lifecycle[\"entered_symbols\"],\n        \"exited_symbols\": lifecycle[\"exited_symbols\"],\n    }"
      },
      {
        "line": 259,
        "text": "turnover_output = {\n        \"generated_at\": generated_at,\n        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\",\n        \"phase\": \"OOS_2B_3_SIDECAR_TURNOVER\",\n        \"execution_status\": \"PAPER_TRACKING_NO_REAL_EXECUTION\",\n        \"source\": \"exports/oos_e1r_v0_2_equity_curve.json\",\n        \"start_date\": turnover_history[0][\"date\"] if turnover_history else date,\n        \"end_date\": turnover_history[-1][\"date\"] if turnover_history else date,\n        \"row_count\": len(turnover_history),\n        \"average_one_way_turnover\": avg_one_way_turnover,\n        \"latest\": turnover_latest,\n        \"records\": turnover_history,\n        \"notes\": [\n            \"Turnover is based on target position changes, not real fills.\",\n            \"This prepares transaction-cost analysis but does not apply costs yet.\",\n        ],\n    }"
      }
    ]
  },
  {
    "path": "scripts/audit_e1r_generator_composer_contract_4b0g.py",
    "parse_ok": true,
    "imports": [
      {
        "line": 2,
        "text": "from __future__ import annotations"
      },
      {
        "line": 4,
        "text": "from pathlib import Path"
      },
      {
        "line": 5,
        "text": "import ast"
      },
      {
        "line": 6,
        "text": "import json"
      },
      {
        "line": 7,
        "text": "import hashlib"
      },
      {
        "line": 8,
        "text": "import inspect"
      },
      {
        "line": 9,
        "text": "import importlib.util"
      },
      {
        "line": 10,
        "text": "import os"
      },
      {
        "line": 11,
        "text": "import re"
      },
      {
        "line": 12,
        "text": "import sys"
      },
      {
        "line": 13,
        "text": "from datetime import datetime, timezone"
      },
      {
        "line": 14,
        "text": "from typing import Any"
      }
    ],
    "functions": [
      {
        "name": "now",
        "line": 58,
        "end_line": 59
      },
      {
        "name": "rel",
        "line": 61,
        "end_line": 62
      },
      {
        "name": "sha256",
        "line": 64,
        "end_line": 69
      },
      {
        "name": "read_text",
        "line": 71,
        "end_line": 72
      },
      {
        "name": "write_json",
        "line": 74,
        "end_line": 76
      },
      {
        "name": "safe_segment",
        "line": 78,
        "end_line": 83
      },
      {
        "name": "parse_ast",
        "line": 85,
        "end_line": 89
      },
      {
        "name": "collect_defs",
        "line": 91,
        "end_line": 160
      },
      {
        "name": "grep_context",
        "line": 162,
        "end_line": 185
      },
      {
        "name": "module_import_probe",
        "line": 187,
        "end_line": 257
      },
      {
        "name": "infer_contract",
        "line": 259,
        "end_line": 328
      },
      {
        "name": "main",
        "line": 330,
        "end_line": 497
      }
    ],
    "calls": [
      {
        "line": 76,
        "text": "p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + \"\\n\")"
      },
      {
        "line": 311,
        "text": "next_actions.append(\"If composer returns only metrics plus diagnostic rows, inspect upstream run_stateful_simulation / run_strategy_variant_comparison return object.\")"
      },
      {
        "line": 424,
        "text": "md.append(json.dumps(inference[\"source_flags\"], indent=2, ensure_ascii=False))"
      },
      {
        "line": 440,
        "text": "md.append(json.dumps(import_probe, indent=2, ensure_ascii=False)[:18000])"
      },
      {
        "line": 459,
        "text": "md.append(json.dumps(compact_defs, indent=2, ensure_ascii=False)[:30000])"
      },
      {
        "line": 471,
        "text": "md.append(json.dumps(compact_grep, indent=2, ensure_ascii=False)[:26000])"
      },
      {
        "line": 480,
        "text": "REPORT_MD.write_text(\"\\n\".join(md) + \"\\n\")"
      },
      {
        "line": 488,
        "text": "print(\"source_flags:\", json.dumps(inference[\"source_flags\"], ensure_ascii=False))"
      },
      {
        "line": 492,
        "text": "print(\"import_probe_errors:\", json.dumps(import_probe.get(\"errors\"), ensure_ascii=False))"
      },
      {
        "line": 424,
        "text": "json.dumps(inference[\"source_flags\"], indent=2, ensure_ascii=False)"
      },
      {
        "line": 488,
        "text": "json.dumps(inference[\"source_flags\"], ensure_ascii=False)"
      },
      {
        "line": 492,
        "text": "json.dumps(import_probe.get(\"errors\"), ensure_ascii=False)"
      },
      {
        "line": 76,
        "text": "json.dumps(obj, indent=2, ensure_ascii=False)"
      },
      {
        "line": 440,
        "text": "json.dumps(import_probe, indent=2, ensure_ascii=False)"
      },
      {
        "line": 459,
        "text": "json.dumps(compact_defs, indent=2, ensure_ascii=False)"
      },
      {
        "line": 471,
        "text": "json.dumps(compact_grep, indent=2, ensure_ascii=False)"
      }
    ],
    "writes": [
      {
        "line": 40,
        "text": "TARGET_NAMES = [\n    \"compose_e1r_v0_2_variant\",\n    \"core_variant_result\",\n    \"sidecar_result\",\n    \"daily_equity_records\",\n    \"daily_records\",\n    \"equity_curve\",\n    \"variant_results\",\n    \"build_equity_records_from_returns\",\n    \"extract_core_interval_returns\",\n    \"build_e1r_sidecar_sleeve\",\n    \"run_strategy_variant_comparison\",\n    \"run_stateful_simulation\",\n    \"e1r_v0_2_backtest_summary.json\",\n    \"e1r_v0_2_backtest_equity_curve.json\",\n    \"E1R_REGIME_AWARE_V0_2\",\n]"
      }
    ],
    "constants": [
      {
        "line": 40,
        "text": "TARGET_NAMES = [\n    \"compose_e1r_v0_2_variant\",\n    \"core_variant_result\",\n    \"sidecar_result\",\n    \"daily_equity_records\",\n    \"daily_records\",\n    \"equity_curve\",\n    \"variant_results\",\n    \"build_equity_records_from_returns\",\n    \"extract_core_interval_returns\",\n    \"build_e1r_sidecar_sleeve\",\n    \"run_strategy_variant_comparison\",\n    \"run_stateful_simulation\",\n    \"e1r_v0_2_backtest_summary.json\",\n    \"e1r_v0_2_backtest_equity_curve.json\",\n    \"E1R_REGIME_AWARE_V0_2\",\n]"
      }
    ]
  },
  {
    "path": "docs/research/stage3_2_backtest_snapshots/backtest_feature_source_stage3_2.py",
    "parse_ok": true,
    "imports": [
      {
        "line": 15,
        "text": "from __future__ import annotations"
      },
      {
        "line": 16,
        "text": "import math"
      },
      {
        "line": 17,
        "text": "import json"
      },
      {
        "line": 18,
        "text": "from pathlib import Path"
      },
      {
        "line": 19,
        "text": "from ..features.rs import period_return, rs_percentile"
      },
      {
        "line": 20,
        "text": "from ..features.momentum import (\n    momentum_score as calc_momentum, moving_average, linreg_slope, momentum_acceleration\n)"
      },
      {
        "line": 23,
        "text": "from ..features.trend_health import trend_health_score as calc_trend_health"
      },
      {
        "line": 24,
        "text": "from ..engine.leader_ranking import leader_score as calc_leader_score"
      },
      {
        "line": 25,
        "text": "from ..engine.trade_decision import trade_action, trade_action_reason"
      },
      {
        "line": 26,
        "text": "from ..utils import logger"
      },
      {
        "line": 884,
        "text": "from collections import deque"
      },
      {
        "line": 2607,
        "text": "import os as _os"
      },
      {
        "line": 975,
        "text": "from ..data_ingestion.fetch_yahoo import get_price_series as _gps"
      },
      {
        "line": 2704,
        "text": "from src.engine.e1r_sidecar_sleeve import (\n            E1RSidecarConfig,\n            build_e1r_sidecar_sleeve,\n        )"
      },
      {
        "line": 2708,
        "text": "from src.engine.e1r_composer import compose_e1r_v0_2_variant"
      },
      {
        "line": 378,
        "text": "from ..features.trend_health import trend_lifecycle"
      },
      {
        "line": 662,
        "text": "from ..features.trend_health import trend_lifecycle"
      },
      {
        "line": 1567,
        "text": "from ..features.trend_health import trend_lifecycle"
      }
    ],
    "functions": [
      {
        "name": "is_broken_trend",
        "line": 104,
        "end_line": 113
      },
      {
        "name": "forward_return",
        "line": 115,
        "end_line": 121
      },
      {
        "name": "_rebuild_leader_score",
        "line": 124,
        "end_line": 169
      },
      {
        "name": "run_leader_engine_validation",
        "line": 176,
        "end_line": 306
      },
      {
        "name": "run_trade_rule_validation",
        "line": 313,
        "end_line": 464
      },
      {
        "name": "run_promotion_engine_validation",
        "line": 471,
        "end_line": 588
      },
      {
        "name": "run_action_forward_validation",
        "line": 595,
        "end_line": 756
      },
      {
        "name": "run_stateful_simulation",
        "line": 763,
        "end_line": 2486
      },
      {
        "name": "run_strategy_variant_comparison",
        "line": 2489,
        "end_line": 2895
      },
      {
        "name": "run_full_backtest",
        "line": 2904,
        "end_line": 2978
      },
      {
        "name": "stats",
        "line": 412,
        "end_line": 430
      },
      {
        "name": "stats",
        "line": 688,
        "end_line": 700
      },
      {
        "name": "_e1r_regime_on",
        "line": 808,
        "end_line": 816
      },
      {
        "name": "_e1r_mode_for_regime",
        "line": 818,
        "end_line": 827
      },
      {
        "name": "_e1r_risk_budget_for_regime",
        "line": 829,
        "end_line": 838
      },
      {
        "name": "_e1r_dominant_regime",
        "line": 840,
        "end_line": 843
      },
      {
        "name": "_build_lookup",
        "line": 867,
        "end_line": 873
      },
      {
        "name": "_get_price_on",
        "line": 879,
        "end_line": 881
      },
      {
        "name": "get_price_by_date",
        "line": 986,
        "end_line": 1000
      },
      {
        "name": "get_close_series_by_date",
        "line": 1002,
        "end_line": 1013
      },
      {
        "name": "_load_e1r_regime_daily",
        "line": 2551,
        "end_line": 2562
      },
      {
        "name": "selection_key",
        "line": 2767,
        "end_line": 2776
      }
    ],
    "calls": [
      {
        "line": 2646,
        "text": "run_stateful_simulation(\n                symbols=symbols,\n                prices_map=prices_map,\n                dates_map=dates_map,\n                spx_prices=spx_prices,\n                spx_dates=spx_dates,\n                assumptions=assumptions,\n                sim_start_date=period_cfg[\"sim_start_date\"],\n                sim_end_date=period_cfg[\"sim_end_date\"],\n                ndx_prices=_use_ndx,\n                ndx_dates=ndx_dates or [],\n                sox_prices=_use_sox,\n                sox_dates=sox_dates or [],\n                vix_prices=_use_vix,\n                vix_dates=vix_dates or [],\n            )"
      },
      {
        "line": 2730,
        "text": "build_e1r_sidecar_sleeve(\n                stock_dir=_stock_dir,\n                spx_path=_spx_path,\n                regime_path=_regime_path,\n                config=_sidecar_cfg,\n            )"
      }
    ],
    "writes": [],
    "constants": [
      {
        "line": 33,
        "text": "LAYER_D_ASSUMPTIONS = {\n    \"initial_capital\":   100_000,\n    \"max_positions\":      3,\n    \"buy_size\":          1.0,    # Top3: 1/3 portfolio full position\n    \"add_size\":          0.5,    # Top3: +1/6 portfolio, used only after REDUCE if allowed\n    \"max_single_size\":   1.0,    # Top3 strategy: 1/3 max per position\n    \"transaction_cost\":  0.0005, # 0.05% one-way\n    \"slippage\":          0.0005, # 0.05% one-way\n    \"total_one_way\":     0.0010, # cost + slippage per direction\n    \"total_round_trip\":  0.0020, # buy + sell total\n    # Primary Execution Model: Adverse Intraday Execution v1.0\n    # Signal Day T → Execute Day T+1\n    # BUY/ADD:     next_day_high  × (1 + cost + slippage)  ← worst buy\n    # REDUCE/EXIT: next_day_low   × (1 - cost - slippage)  ← worst sell\n    # HOLD:        mark-to-market at close, no transaction\n    \"execution_model\":   \"adverse_intraday\",\n    \"buy_price_field\":   \"high\",   # T+1 high\n    \"sell_price_field\":  \"low\",    # T+1 low\n    \"cash_yield\":        0.0,\n    \"leverage\":          False,\n    \"short_selling\":     False,\n    \"strategy_variant\":  \"top3_entry_rs_minhold_relstop\",\n    \"entry_top_n\":       3,\n    \"rank_based_exit\":   False,\n    # Market Gate is disabled in this v1.6 diagnostic matrix so we can isolate\n    # the impact of RS threshold, minimum holding period, and relative SPX stop.\n    \"market_gate_enabled\": False,\n    \"risk_off_below_spx_ma50\": False,\n    \"market_shock_gate_enabled\": False,\n    \"market_shock_daily_return\": -0.02,\n\n    # Entry / holding / relative-risk controls tested by v1.6 variants.\n    \"entry_rs_min\": 90.0,\n    \"min_holding_days\": 0,\n    \"min_hold_allow_broken_exit\": True,\n    \"relative_stop_enabled\": False,\n    \"relative_stop_underperform_pct\": -0.08,  # stock return - SPX return <= -8%\n    \"relative_stop_action\": \"REL_REDUCE\",   # reduce 50%, once per position\n    \"relative_stop_once_per_position\": True,\n\n    # No fixed take-profit in v1.6. TP7-P is intentionally disabled/rejected.\n    \"partial_take_profit_enabled\": False,\n    \"partial_take_profit_threshold\": 0.07,\n    \"partial_take_profit_fraction\": 0.50,\n    \"block_add_after_take_profit\": False,\n    \"version\":           \"1.6-top3-rs95-minhold-relstop-comparison\",\n    \"ls60_exit_mode\":    \"reduce\",   # \"exit\"=旧规则 \"reduce\"=新规则（默认）\n\n    # Qualified Candidate Pool（v1.7+）\n    # candidate_top_n：Qualified Pool 内最多取 N 个候选（None = 用旧 entry_top_n 逻辑）\n    # max_positions：组合最大持仓数\n    # qualified_entry_enabled：是否启用资格过滤\n    # qualified_states：允许的 trend_stat"
      },
      {
        "line": 847,
        "text": "market_gate_enabled = bool(a.get(\"market_gate_enabled\", True))"
      },
      {
        "line": 848,
        "text": "risk_off_below_spx_ma50 = bool(a.get(\"risk_off_below_spx_ma50\", True))"
      },
      {
        "line": 896,
        "text": "market_shock_gate_enabled = bool(a.get(\"market_shock_gate_enabled\", True))"
      },
      {
        "line": 897,
        "text": "market_shock_daily_return = float(a.get(\"market_shock_daily_return\", -0.02))"
      },
      {
        "line": 911,
        "text": "market_gate_variant = (\n        \"D1_NO_MARKET_GATE\" if not market_gate_enabled else\n        \"D2_RISK_OFF_GATE\" if not market_shock_gate_enabled else\n        \"D3_RISK_OFF_PLUS_SHOCK_GATE\"\n    )"
      },
      {
        "line": 2517,
        "text": "base = {\n        **LAYER_D_ASSUMPTIONS,\n        \"market_gate_enabled\": False,\n        \"market_shock_gate_enabled\": False,\n        \"partial_take_profit_enabled\": False,\n        \"block_add_after_take_profit\": False,\n    }"
      },
      {
        "line": 2525,
        "text": "_gate_v2_no_vix = {\n        \"market_gate_enabled\":       True,\n        \"risk_off_below_spx_ma50\":   True,\n        \"market_shock_gate_enabled\": True,\n        \"market_shock_daily_return\": -0.02,\n        \"candidate_top_n\":           None,\n        \"qualified_entry_enabled\":   False,\n        \"fill_only_enabled\":         False,\n    }"
      },
      {
        "line": 2536,
        "text": "_gate_g4 = {\n        \"market_gate_enabled\":       True,\n        \"risk_off_below_spx_ma50\":   False,\n        \"market_shock_gate_enabled\": False,\n        \"market_shock_daily_return\": -0.02,\n        \"gate_use_slope\":            True,\n        \"gate_use_leadership\":       True,\n        \"candidate_top_n\":           None,\n        \"qualified_entry_enabled\":   False,\n        \"fill_only_enabled\":         False,\n        \"entry_top_n\":               3,\n        \"entry_rs_min\":              90.0,\n        \"ls60_exit_mode\":            \"exit\",\n    }"
      },
      {
        "line": 1448,
        "text": "_shock_active = (\n                market_shock_gate_enabled\n                and spx_day_return <= market_shock_daily_return\n            )"
      },
      {
        "line": 2646,
        "text": "_result = run_stateful_simulation(\n                symbols=symbols,\n                prices_map=prices_map,\n                dates_map=dates_map,\n                spx_prices=spx_prices,\n                spx_dates=spx_dates,\n                assumptions=assumptions,\n                sim_start_date=period_cfg[\"sim_start_date\"],\n                sim_end_date=period_cfg[\"sim_end_date\"],\n                ndx_prices=_use_ndx,\n                ndx_dates=ndx_dates or [],\n                sox_prices=_use_sox,\n                sox_dates=sox_dates or [],\n                vix_prices=_use_vix,\n                vix_dates=vix_dates or [],\n            )"
      },
      {
        "line": 2730,
        "text": "_sidecar_result = build_e1r_sidecar_sleeve(\n                stock_dir=_stock_dir,\n                spx_path=_spx_path,\n                regime_path=_regime_path,\n                config=_sidecar_cfg,\n            )"
      },
      {
        "line": 2737,
        "text": "variant_results[\"E1R_REGIME_AWARE_V0_2\"] = compose_e1r_v0_2_variant(\n                core_variant_result=_core_e1r,\n                sidecar_result=_sidecar_result,\n                initial_equity=float(base.get(\"initial_capital\", 100000)),\n            )"
      }
    ]
  },
  {
    "path": "src/engine/backtest.py",
    "parse_ok": true,
    "imports": [
      {
        "line": 15,
        "text": "from __future__ import annotations"
      },
      {
        "line": 16,
        "text": "import math"
      },
      {
        "line": 17,
        "text": "import json"
      },
      {
        "line": 18,
        "text": "from pathlib import Path"
      },
      {
        "line": 19,
        "text": "from ..features.rs import period_return, rs_percentile"
      },
      {
        "line": 20,
        "text": "from ..features.momentum import (\n    momentum_score as calc_momentum, moving_average, linreg_slope, momentum_acceleration\n)"
      },
      {
        "line": 23,
        "text": "from ..features.trend_health import trend_health_score as calc_trend_health"
      },
      {
        "line": 24,
        "text": "from ..engine.leader_ranking import leader_score as calc_leader_score"
      },
      {
        "line": 25,
        "text": "from ..engine.trade_decision import trade_action, trade_action_reason"
      },
      {
        "line": 26,
        "text": "from ..utils import logger"
      },
      {
        "line": 884,
        "text": "from collections import deque"
      },
      {
        "line": 2607,
        "text": "import os as _os"
      },
      {
        "line": 975,
        "text": "from ..data_ingestion.fetch_yahoo import get_price_series as _gps"
      },
      {
        "line": 2704,
        "text": "from src.engine.e1r_sidecar_sleeve import (\n            E1RSidecarConfig,\n            build_e1r_sidecar_sleeve,\n        )"
      },
      {
        "line": 2708,
        "text": "from src.engine.e1r_composer import compose_e1r_v0_2_variant"
      },
      {
        "line": 378,
        "text": "from ..features.trend_health import trend_lifecycle"
      },
      {
        "line": 662,
        "text": "from ..features.trend_health import trend_lifecycle"
      },
      {
        "line": 1567,
        "text": "from ..features.trend_health import trend_lifecycle"
      }
    ],
    "functions": [
      {
        "name": "is_broken_trend",
        "line": 104,
        "end_line": 113
      },
      {
        "name": "forward_return",
        "line": 115,
        "end_line": 121
      },
      {
        "name": "_rebuild_leader_score",
        "line": 124,
        "end_line": 169
      },
      {
        "name": "run_leader_engine_validation",
        "line": 176,
        "end_line": 306
      },
      {
        "name": "run_trade_rule_validation",
        "line": 313,
        "end_line": 464
      },
      {
        "name": "run_promotion_engine_validation",
        "line": 471,
        "end_line": 588
      },
      {
        "name": "run_action_forward_validation",
        "line": 595,
        "end_line": 756
      },
      {
        "name": "run_stateful_simulation",
        "line": 763,
        "end_line": 2486
      },
      {
        "name": "run_strategy_variant_comparison",
        "line": 2489,
        "end_line": 2895
      },
      {
        "name": "run_full_backtest",
        "line": 2904,
        "end_line": 2978
      },
      {
        "name": "stats",
        "line": 412,
        "end_line": 430
      },
      {
        "name": "stats",
        "line": 688,
        "end_line": 700
      },
      {
        "name": "_e1r_regime_on",
        "line": 808,
        "end_line": 816
      },
      {
        "name": "_e1r_mode_for_regime",
        "line": 818,
        "end_line": 827
      },
      {
        "name": "_e1r_risk_budget_for_regime",
        "line": 829,
        "end_line": 838
      },
      {
        "name": "_e1r_dominant_regime",
        "line": 840,
        "end_line": 843
      },
      {
        "name": "_build_lookup",
        "line": 867,
        "end_line": 873
      },
      {
        "name": "_get_price_on",
        "line": 879,
        "end_line": 881
      },
      {
        "name": "get_price_by_date",
        "line": 986,
        "end_line": 1000
      },
      {
        "name": "get_close_series_by_date",
        "line": 1002,
        "end_line": 1013
      },
      {
        "name": "_load_e1r_regime_daily",
        "line": 2551,
        "end_line": 2562
      },
      {
        "name": "selection_key",
        "line": 2767,
        "end_line": 2776
      }
    ],
    "calls": [
      {
        "line": 2646,
        "text": "run_stateful_simulation(\n                symbols=symbols,\n                prices_map=prices_map,\n                dates_map=dates_map,\n                spx_prices=spx_prices,\n                spx_dates=spx_dates,\n                assumptions=assumptions,\n                sim_start_date=period_cfg[\"sim_start_date\"],\n                sim_end_date=period_cfg[\"sim_end_date\"],\n                ndx_prices=_use_ndx,\n                ndx_dates=ndx_dates or [],\n                sox_prices=_use_sox,\n                sox_dates=sox_dates or [],\n                vix_prices=_use_vix,\n                vix_dates=vix_dates or [],\n            )"
      },
      {
        "line": 2730,
        "text": "build_e1r_sidecar_sleeve(\n                stock_dir=_stock_dir,\n                spx_path=_spx_path,\n                regime_path=_regime_path,\n                config=_sidecar_cfg,\n            )"
      }
    ],
    "writes": [],
    "constants": [
      {
        "line": 33,
        "text": "LAYER_D_ASSUMPTIONS = {\n    \"initial_capital\":   100_000,\n    \"max_positions\":      3,\n    \"buy_size\":          1.0,    # Top3: 1/3 portfolio full position\n    \"add_size\":          0.5,    # Top3: +1/6 portfolio, used only after REDUCE if allowed\n    \"max_single_size\":   1.0,    # Top3 strategy: 1/3 max per position\n    \"transaction_cost\":  0.0005, # 0.05% one-way\n    \"slippage\":          0.0005, # 0.05% one-way\n    \"total_one_way\":     0.0010, # cost + slippage per direction\n    \"total_round_trip\":  0.0020, # buy + sell total\n    # Primary Execution Model: Adverse Intraday Execution v1.0\n    # Signal Day T → Execute Day T+1\n    # BUY/ADD:     next_day_high  × (1 + cost + slippage)  ← worst buy\n    # REDUCE/EXIT: next_day_low   × (1 - cost - slippage)  ← worst sell\n    # HOLD:        mark-to-market at close, no transaction\n    \"execution_model\":   \"adverse_intraday\",\n    \"buy_price_field\":   \"high\",   # T+1 high\n    \"sell_price_field\":  \"low\",    # T+1 low\n    \"cash_yield\":        0.0,\n    \"leverage\":          False,\n    \"short_selling\":     False,\n    \"strategy_variant\":  \"top3_entry_rs_minhold_relstop\",\n    \"entry_top_n\":       3,\n    \"rank_based_exit\":   False,\n    # Market Gate is disabled in this v1.6 diagnostic matrix so we can isolate\n    # the impact of RS threshold, minimum holding period, and relative SPX stop.\n    \"market_gate_enabled\": False,\n    \"risk_off_below_spx_ma50\": False,\n    \"market_shock_gate_enabled\": False,\n    \"market_shock_daily_return\": -0.02,\n\n    # Entry / holding / relative-risk controls tested by v1.6 variants.\n    \"entry_rs_min\": 90.0,\n    \"min_holding_days\": 0,\n    \"min_hold_allow_broken_exit\": True,\n    \"relative_stop_enabled\": False,\n    \"relative_stop_underperform_pct\": -0.08,  # stock return - SPX return <= -8%\n    \"relative_stop_action\": \"REL_REDUCE\",   # reduce 50%, once per position\n    \"relative_stop_once_per_position\": True,\n\n    # No fixed take-profit in v1.6. TP7-P is intentionally disabled/rejected.\n    \"partial_take_profit_enabled\": False,\n    \"partial_take_profit_threshold\": 0.07,\n    \"partial_take_profit_fraction\": 0.50,\n    \"block_add_after_take_profit\": False,\n    \"version\":           \"1.6-top3-rs95-minhold-relstop-comparison\",\n    \"ls60_exit_mode\":    \"reduce\",   # \"exit\"=旧规则 \"reduce\"=新规则（默认）\n\n    # Qualified Candidate Pool（v1.7+）\n    # candidate_top_n：Qualified Pool 内最多取 N 个候选（None = 用旧 entry_top_n 逻辑）\n    # max_positions：组合最大持仓数\n    # qualified_entry_enabled：是否启用资格过滤\n    # qualified_states：允许的 trend_stat"
      },
      {
        "line": 847,
        "text": "market_gate_enabled = bool(a.get(\"market_gate_enabled\", True))"
      },
      {
        "line": 848,
        "text": "risk_off_below_spx_ma50 = bool(a.get(\"risk_off_below_spx_ma50\", True))"
      },
      {
        "line": 896,
        "text": "market_shock_gate_enabled = bool(a.get(\"market_shock_gate_enabled\", True))"
      },
      {
        "line": 897,
        "text": "market_shock_daily_return = float(a.get(\"market_shock_daily_return\", -0.02))"
      },
      {
        "line": 911,
        "text": "market_gate_variant = (\n        \"D1_NO_MARKET_GATE\" if not market_gate_enabled else\n        \"D2_RISK_OFF_GATE\" if not market_shock_gate_enabled else\n        \"D3_RISK_OFF_PLUS_SHOCK_GATE\"\n    )"
      },
      {
        "line": 2517,
        "text": "base = {\n        **LAYER_D_ASSUMPTIONS,\n        \"market_gate_enabled\": False,\n        \"market_shock_gate_enabled\": False,\n        \"partial_take_profit_enabled\": False,\n        \"block_add_after_take_profit\": False,\n    }"
      },
      {
        "line": 2525,
        "text": "_gate_v2_no_vix = {\n        \"market_gate_enabled\":       True,\n        \"risk_off_below_spx_ma50\":   True,\n        \"market_shock_gate_enabled\": True,\n        \"market_shock_daily_return\": -0.02,\n        \"candidate_top_n\":           None,\n        \"qualified_entry_enabled\":   False,\n        \"fill_only_enabled\":         False,\n    }"
      },
      {
        "line": 2536,
        "text": "_gate_g4 = {\n        \"market_gate_enabled\":       True,\n        \"risk_off_below_spx_ma50\":   False,\n        \"market_shock_gate_enabled\": False,\n        \"market_shock_daily_return\": -0.02,\n        \"gate_use_slope\":            True,\n        \"gate_use_leadership\":       True,\n        \"candidate_top_n\":           None,\n        \"qualified_entry_enabled\":   False,\n        \"fill_only_enabled\":         False,\n        \"entry_top_n\":               3,\n        \"entry_rs_min\":              90.0,\n        \"ls60_exit_mode\":            \"exit\",\n    }"
      },
      {
        "line": 1448,
        "text": "_shock_active = (\n                market_shock_gate_enabled\n                and spx_day_return <= market_shock_daily_return\n            )"
      },
      {
        "line": 2646,
        "text": "_result = run_stateful_simulation(\n                symbols=symbols,\n                prices_map=prices_map,\n                dates_map=dates_map,\n                spx_prices=spx_prices,\n                spx_dates=spx_dates,\n                assumptions=assumptions,\n                sim_start_date=period_cfg[\"sim_start_date\"],\n                sim_end_date=period_cfg[\"sim_end_date\"],\n                ndx_prices=_use_ndx,\n                ndx_dates=ndx_dates or [],\n                sox_prices=_use_sox,\n                sox_dates=sox_dates or [],\n                vix_prices=_use_vix,\n                vix_dates=vix_dates or [],\n            )"
      },
      {
        "line": 2730,
        "text": "_sidecar_result = build_e1r_sidecar_sleeve(\n                stock_dir=_stock_dir,\n                spx_path=_spx_path,\n                regime_path=_regime_path,\n                config=_sidecar_cfg,\n            )"
      },
      {
        "line": 2737,
        "text": "variant_results[\"E1R_REGIME_AWARE_V0_2\"] = compose_e1r_v0_2_variant(\n                core_variant_result=_core_e1r,\n                sidecar_result=_sidecar_result,\n                initial_equity=float(base.get(\"initial_capital\", 100000)),\n            )"
      }
    ]
  }
]
```

## Unresolved
```json
[]
```

## Validations
```json
{
  "generator_trace_complete": true,
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
  "r9b_loaded": true,
  "target_artifact_exists": true,
  "generator_path_trace_exists": true,
  "generator_path_trace_relevant_rows_found": true,
  "self_reference_pollution_removed": true,
  "clean_repo_grep_completed": true,
  "candidate_scripts_inspected": true,
  "required_market_param_evidence_found": true,
  "generator_call_chain_evidence_found": true,
  "blocking_unresolved_count": 0
}
```

## Decision
```json
{
  "k2_r9c_115_return_generator_trace_passed": true,
  "market_state_115_replication_ready": true,
  "formula_patch_allowed_now": false,
  "candidate_extraction_allowed_now": false,
  "implementation_may_resume": false,
  "unresolved": [],
  "next_required_stage_if_ready": "4C-2C-4E-ENGINE-K2-R10-MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL",
  "next_required_stage_if_not_ready": "4C-2C-4E-ENGINE-K2-R9D-MARKET_PARAM_SOURCE_LINE_TRACE",
  "conclusion": "K2_R9C_PASS_GENERATOR_TRACE_READY_FOR_REPLICATION_PROPOSAL",
  "recommended_next_action": "If market param evidence is present, prepare standalone replication proposal. If evidence is still indirect, perform source-line trace for each missing market parameter."
}
```
