# Stage 3.8E-2F-2C-4C-10F-4B-0D E1R Generator Path Trace

Generated At: `2026-07-09T09:31:36.292651+00:00`

## Status

- Status: `E1R_GENERATOR_PATH_TRACE_COMPLETE_NO_EXPORTS_WRITTEN`
- Strategy files unchanged: `True`
- Canonical existence unchanged: `True`
- Full backtest rerun: `False`

## Conclusion

- `COMPOSER_GENERATOR_PATH_CANDIDATES_FOUND`
- Recommended: Trace the generator candidate that calls compose_e1r_v0_2_variant and rerun it in dry-run/no-write mode to recover core_variant_result and daily equity.

## Search Summary

```json
{
  "files_scanned": 832,
  "grep_result_count": 160,
  "function_index_file_count": 11,
  "json_probe_count": 22,
  "generator_candidate_count": 80
}
```

## Generator Candidates

```json
[
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json",
    "generator_score": 166,
    "base_score": 108,
    "matched_terms": [
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
    ],
    "hits": [
      {
        "line": 7,
        "matched": [
          "export"
        ],
        "context": [
          {
            "line": 5,
            "text": "  \"policy\": {"
          },
          {
            "line": 6,
            "text": "    \"dashboard_changed\": false,"
          },
          {
            "line": 7,
            "text": "    \"exports_changed\": false,"
          },
          {
            "line": 8,
            "text": "    \"workflow_changed\": false,"
          },
          {
            "line": 9,
            "text": "    \"strategy_logic_changed\": false,"
          }
        ]
      },
      {
        "line": 79,
        "matched": [
          "extract_core_interval_returns"
        ],
        "context": [
          {
            "line": 77,
            "text": "        },"
          },
          {
            "line": 78,
            "text": "        {"
          },
          {
            "line": 79,
            "text": "          \"name\": \"extract_core_interval_returns\","
          },
          {
            "line": 80,
            "text": "          \"line\": 94,"
          },
          {
            "line": 81,
            "text": "          \"args\": ["
          }
        ]
      },
      {
        "line": 82,
        "matched": [
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 80,
            "text": "          \"line\": 94,"
          },
          {
            "line": 81,
            "text": "          \"args\": ["
          },
          {
            "line": 82,
            "text": "            \"core_daily_equity_records\","
          },
          {
            "line": 83,
            "text": "            \"sidecar_records\""
          },
          {
            "line": 84,
            "text": "          ],"
          }
        ]
      },
      {
        "line": 90,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 88,
            "text": "        },"
          },
          {
            "line": 89,
            "text": "        {"
          },
          {
            "line": 90,
            "text": "          \"name\": \"build_equity_records_from_returns\","
          },
          {
            "line": 91,
            "text": "          \"line\": 171,"
          },
          {
            "line": 92,
            "text": "          \"args\": ["
          }
        ]
      },
      {
        "line": 113,
        "matched": [
          "e1r_v0_2",
          "compose_e1r_v0_2_variant"
        ],
        "context": [
          {
            "line": 111,
            "text": "        },"
          },
          {
            "line": 112,
            "text": "        {"
          },
          {
            "line": 113,
            "text": "          \"name\": \"compose_e1r_v0_2_variant\","
          },
          {
            "line": 114,
            "text": "          \"line\": 283,"
          },
          {
            "line": 115,
            "text": "          \"args\": ["
          }
        ]
      },
      {
        "line": 116,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 114,
            "text": "          \"line\": 283,"
          },
          {
            "line": 115,
            "text": "          \"args\": ["
          },
          {
            "line": 116,
            "text": "            \"core_variant_result\","
          },
          {
            "line": 117,
            "text": "            \"sidecar_result\","
          },
          {
            "line": 118,
            "text": "            \"initial_equity\""
          }
        ]
      },
      {
        "line": 117,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 115,
            "text": "          \"args\": ["
          },
          {
            "line": 116,
            "text": "            \"core_variant_result\","
          },
          {
            "line": 117,
            "text": "            \"sidecar_result\","
          },
          {
            "line": 118,
            "text": "            \"initial_equity\""
          },
          {
            "line": 119,
            "text": "          ],"
          }
        ]
      },
      {
        "line": 166,
        "matched": [
          "equity_curve"
        ],
        "context": [
          {
            "line": 164,
            "text": "        {"
          },
          {
            "line": 165,
            "text": "          \"line\": 224,"
          },
          {
            "line": 166,
            "text": "          \"target\": \"equity_curve\","
          },
          {
            "line": 167,
            "text": "          \"value\": \"[initial_equity] + [safe_float(r.get('equity')) or initial_equity for r in equity_records]\""
          },
          {
            "line": 168,
            "text": "        },"
          }
        ]
      },
      {
        "line": 172,
        "matched": [
          "core_variant_result",
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 170,
            "text": "          \"line\": 288,"
          },
          {
            "line": 171,
            "text": "          \"target\": \"core_records\","
          },
          {
            "line": 172,
            "text": "          \"value\": \"core_variant_result.get('daily_equity_records', [])\""
          },
          {
            "line": 173,
            "text": "        },"
          },
          {
            "line": 174,
            "text": "        {"
          }
        ]
      },
      {
        "line": 177,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 175,
            "text": "          \"line\": 292,"
          },
          {
            "line": 176,
            "text": "          \"target\": \"equity_records\","
          },
          {
            "line": 177,
            "text": "          \"value\": \"build_equity_records_from_returns(interval_records, initial_equity)\""
          },
          {
            "line": 178,
            "text": "        },"
          },
          {
            "line": 179,
            "text": "        {"
          }
        ]
      },
      {
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
      },
      {
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
      },
      {
        "line": 213,
        "matched": [
          "extract_core_interval_returns"
        ],
        "context": [
          {
            "line": 211,
            "text": "          \"line\": 94,"
          },
          {
            "line": 212,
            "text": "          \"terms\": ["
          },
          {
            "line": 213,
            "text": "            \"extract_core_interval_returns\""
          },
          {
            "line": 214,
            "text": "          ],"
          },
          {
            "line": 215,
            "text": "          \"text\": \"def extract_core_interval_returns(\""
          }
        ]
      },
      {
        "line": 215,
        "matched": [
          "extract_core_interval_returns"
        ],
        "context": [
          {
            "line": 213,
            "text": "            \"extract_core_interval_returns\""
          },
          {
            "line": 214,
            "text": "          ],"
          },
          {
            "line": 215,
            "text": "          \"text\": \"def extract_core_interval_returns(\""
          },
          {
            "line": 216,
            "text": "        },"
          },
          {
            "line": 217,
            "text": "        {"
          }
        ]
      },
      {
        "line": 222,
        "matched": [
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 220,
            "text": "            \"daily_equity\""
          },
          {
            "line": 221,
            "text": "          ],"
          },
          {
            "line": 222,
            "text": "          \"text\": \"    core_daily_equity_records: Sequence[dict[str, Any]],\""
          },
          {
            "line": 223,
            "text": "        },"
          },
          {
            "line": 224,
            "text": "        {"
          }
        ]
      },
      {
        "line": 229,
        "matched": [
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 227,
            "text": "            \"daily_equity\""
          },
          {
            "line": 228,
            "text": "          ],"
          },
          {
            "line": 229,
            "text": "          \"text\": \"    for row in core_daily_equity_records:\""
          },
          {
            "line": 230,
            "text": "        },"
          },
          {
            "line": 231,
            "text": "        {"
          }
        ]
      },
      {
        "line": 241,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 239,
            "text": "          \"line\": 171,"
          },
          {
            "line": 240,
            "text": "          \"terms\": ["
          },
          {
            "line": 241,
            "text": "            \"build_equity_records_from_returns\""
          },
          {
            "line": 242,
            "text": "          ],"
          },
          {
            "line": 243,
            "text": "          \"text\": \"def build_equity_records_from_returns(\""
          }
        ]
      },
      {
        "line": 243,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 241,
            "text": "            \"build_equity_records_from_returns\""
          },
          {
            "line": 242,
            "text": "          ],"
          },
          {
            "line": 243,
            "text": "          \"text\": \"def build_equity_records_from_returns(\""
          },
          {
            "line": 244,
            "text": "        },"
          },
          {
            "line": 245,
            "text": "        {"
          }
        ]
      },
      {
        "line": 255,
        "matched": [
          "equity_curve"
        ],
        "context": [
          {
            "line": 253,
            "text": "          \"line\": 224,"
          },
          {
            "line": 254,
            "text": "          \"terms\": ["
          },
          {
            "line": 255,
            "text": "            \"equity_curve\""
          },
          {
            "line": 256,
            "text": "          ],"
          },
          {
            "line": 257,
            "text": "          \"text\": \"    equity_curve = [initial_equity] + [\""
          }
        ]
      },
      {
        "line": 257,
        "matched": [
          "equity_curve"
        ],
        "context": [
          {
            "line": 255,
            "text": "            \"equity_curve\""
          },
          {
            "line": 256,
            "text": "          ],"
          },
          {
            "line": 257,
            "text": "          \"text\": \"    equity_curve = [initial_equity] + [\""
          },
          {
            "line": 258,
            "text": "        },"
          },
          {
            "line": 259,
            "text": "        {"
          }
        ]
      },
      {
        "line": 262,
        "matched": [
          "equity_curve"
        ],
        "context": [
          {
            "line": 260,
            "text": "          \"line\": 260,"
          },
          {
            "line": 261,
            "text": "          \"terms\": ["
          },
          {
            "line": 262,
            "text": "            \"equity_curve\""
          },
          {
            "line": 263,
            "text": "          ],"
          },
          {
            "line": 264,
            "text": "          \"text\": \"        \\\"max_drawdown_pct\\\": abs(pct_display(max_drawdown(equity_curve)) or 0.0),\""
          }
        ]
      },
      {
        "line": 264,
        "matched": [
          "equity_curve"
        ],
        "context": [
          {
            "line": 262,
            "text": "            \"equity_curve\""
          },
          {
            "line": 263,
            "text": "          ],"
          },
          {
            "line": 264,
            "text": "          \"text\": \"        \\\"max_drawdown_pct\\\": abs(pct_display(max_drawdown(equity_curve)) or 0.0),\""
          },
          {
            "line": 265,
            "text": "        },"
          },
          {
            "line": 266,
            "text": "        {"
          }
        ]
      },
      {
        "line": 278,
        "matched": [
          "core_variant_result",
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 276,
            "text": "            \"daily_equity\""
          },
          {
            "line": 277,
            "text": "          ],"
          },
          {
            "line": 278,
            "text": "          \"text\": \"    core_records = core_variant_result.get(\\\"daily_equity_records\\\", [])\""
          },
          {
            "line": 279,
            "text": "        },"
          },
          {
            "line": 280,
            "text": "        {"
          }
        ]
      },
      {
        "line": 283,
        "matched": [
          "extract_core_interval_returns"
        ],
        "context": [
          {
            "line": 281,
            "text": "          \"line\": 291,"
          },
          {
            "line": 282,
            "text": "          \"terms\": ["
          },
          {
            "line": 283,
            "text": "            \"extract_core_interval_returns\""
          },
          {
            "line": 284,
            "text": "          ],"
          },
          {
            "line": 285,
            "text": "          \"text\": \"    interval_records = extract_core_interval_returns(core_records, sidecar_records)\""
          }
        ]
      },
      {
        "line": 285,
        "matched": [
          "extract_core_interval_returns"
        ],
        "context": [
          {
            "line": 283,
            "text": "            \"extract_core_interval_returns\""
          },
          {
            "line": 284,
            "text": "          ],"
          },
          {
            "line": 285,
            "text": "          \"text\": \"    interval_records = extract_core_interval_returns(core_records, sidecar_records)\""
          },
          {
            "line": 286,
            "text": "        },"
          },
          {
            "line": 287,
            "text": "        {"
          }
        ]
      },
      {
        "line": 290,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 288,
            "text": "          \"line\": 292,"
          },
          {
            "line": 289,
            "text": "          \"terms\": ["
          },
          {
            "line": 290,
            "text": "            \"build_equity_records_from_returns\""
          },
          {
            "line": 291,
            "text": "          ],"
          },
          {
            "line": 292,
            "text": "          \"text\": \"    equity_records = build_equity_records_from_returns(interval_records, initial_equity)\""
          }
        ]
      },
      {
        "line": 292,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 290,
            "text": "            \"build_equity_records_from_returns\""
          },
          {
            "line": 291,
            "text": "          ],"
          },
          {
            "line": 292,
            "text": "          \"text\": \"    equity_records = build_equity_records_from_returns(interval_records, initial_equity)\""
          },
          {
            "line": 293,
            "text": "        },"
          },
          {
            "line": 294,
            "text": "        {"
          }
        ]
      },
      {
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
      },
      {
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
      },
      {
        "line": 313,
        "matched": [
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 311,
            "text": "            \"daily_equity\""
          },
          {
            "line": 312,
            "text": "          ],"
          },
          {
            "line": 313,
            "text": "          \"text\": \"        \\\"daily_equity_records\\\": equity_records,\""
          },
          {
            "line": 314,
            "text": "        },"
          },
          {
            "line": 315,
            "text": "        {"
          }
        ]
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C7_REAL_CORE_SIDECAR_RECORDS_AUDIT.json",
    "generator_score": 166,
    "base_score": 108,
    "matched_terms": [
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
    ],
    "hits": [
      {
        "line": 7,
        "matched": [
          "export"
        ],
        "context": [
          {
            "line": 5,
            "text": "  \"policy\": {"
          },
          {
            "line": 6,
            "text": "    \"dashboard_changed\": false,"
          },
          {
            "line": 7,
            "text": "    \"exports_changed\": false,"
          },
          {
            "line": 8,
            "text": "    \"workflow_changed\": false,"
          },
          {
            "line": 9,
            "text": "    \"strategy_logic_changed\": false,"
          }
        ]
      },
      {
        "line": 10,
        "matched": [
          "export"
        ],
        "context": [
          {
            "line": 8,
            "text": "    \"workflow_changed\": false,"
          },
          {
            "line": 9,
            "text": "    \"strategy_logic_changed\": false,"
          },
          {
            "line": 10,
            "text": "    \"canonical_exports_written\": false,"
          },
          {
            "line": 11,
            "text": "    \"long_backtest_run\": false"
          },
          {
            "line": 12,
            "text": "  },"
          }
        ]
      },
      {
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
      },
      {
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
      },
      {
        "line": 62,
        "matched": [
          "extract_core_interval_returns"
        ],
        "context": [
          {
            "line": 60,
            "text": "          \"line\": 94,"
          },
          {
            "line": 61,
            "text": "          \"terms\": ["
          },
          {
            "line": 62,
            "text": "            \"extract_core_interval_returns\""
          },
          {
            "line": 63,
            "text": "          ],"
          },
          {
            "line": 64,
            "text": "          \"text\": \"def extract_core_interval_returns(\""
          }
        ]
      },
      {
        "line": 64,
        "matched": [
          "extract_core_interval_returns"
        ],
        "context": [
          {
            "line": 62,
            "text": "            \"extract_core_interval_returns\""
          },
          {
            "line": 63,
            "text": "          ],"
          },
          {
            "line": 64,
            "text": "          \"text\": \"def extract_core_interval_returns(\""
          },
          {
            "line": 65,
            "text": "        },"
          },
          {
            "line": 66,
            "text": "        {"
          }
        ]
      },
      {
        "line": 69,
        "matched": [
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 67,
            "text": "          \"line\": 95,"
          },
          {
            "line": 68,
            "text": "          \"terms\": ["
          },
          {
            "line": 69,
            "text": "            \"core_daily_equity_records\","
          },
          {
            "line": 70,
            "text": "            \"daily_equity\""
          },
          {
            "line": 71,
            "text": "          ],"
          }
        ]
      },
      {
        "line": 72,
        "matched": [
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 70,
            "text": "            \"daily_equity\""
          },
          {
            "line": 71,
            "text": "          ],"
          },
          {
            "line": 72,
            "text": "          \"text\": \"    core_daily_equity_records: Sequence[dict[str, Any]],\""
          },
          {
            "line": 73,
            "text": "        },"
          },
          {
            "line": 74,
            "text": "        {"
          }
        ]
      },
      {
        "line": 119,
        "matched": [
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 117,
            "text": "          \"line\": 113,"
          },
          {
            "line": 118,
            "text": "          \"terms\": ["
          },
          {
            "line": 119,
            "text": "            \"core_daily_equity_records\","
          },
          {
            "line": 120,
            "text": "            \"daily_equity\""
          },
          {
            "line": 121,
            "text": "          ],"
          }
        ]
      },
      {
        "line": 122,
        "matched": [
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 120,
            "text": "            \"daily_equity\""
          },
          {
            "line": 121,
            "text": "          ],"
          },
          {
            "line": 122,
            "text": "          \"text\": \"    for row in core_daily_equity_records:\""
          },
          {
            "line": 123,
            "text": "        },"
          },
          {
            "line": 124,
            "text": "        {"
          }
        ]
      },
      {
        "line": 286,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 284,
            "text": "          \"line\": 171,"
          },
          {
            "line": 285,
            "text": "          \"terms\": ["
          },
          {
            "line": 286,
            "text": "            \"build_equity_records_from_returns\""
          },
          {
            "line": 287,
            "text": "          ],"
          },
          {
            "line": 288,
            "text": "          \"text\": \"def build_equity_records_from_returns(\""
          }
        ]
      },
      {
        "line": 288,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 286,
            "text": "            \"build_equity_records_from_returns\""
          },
          {
            "line": 287,
            "text": "          ],"
          },
          {
            "line": 288,
            "text": "          \"text\": \"def build_equity_records_from_returns(\""
          },
          {
            "line": 289,
            "text": "        },"
          },
          {
            "line": 290,
            "text": "        {"
          }
        ]
      },
      {
        "line": 567,
        "matched": [
          "core_variant_result",
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 565,
            "text": "            \"daily_equity\""
          },
          {
            "line": 566,
            "text": "          ],"
          },
          {
            "line": 567,
            "text": "          \"text\": \"    core_records = core_variant_result.get(\\\"daily_equity_records\\\", [])\""
          },
          {
            "line": 568,
            "text": "        },"
          },
          {
            "line": 569,
            "text": "        {"
          }
        ]
      },
      {
        "line": 574,
        
```

## Function Indexes

```json
{
  "scripts/export_e1_5y_core_equity.py": {
    "main": {
      "line": 295,
      "end_line": 514,
      "matched_terms": [
        "run_stateful_simulation"
      ],
      "source": "def main() -> int:\n    sys.path.insert(0, str(ROOT))\n    sys.path.insert(0, str(ROOT / \"src\"))\n\n    from src.engine import backtest\n\n    symbols, prices_map, dates_map, ohlc_map, rejected = load_stocks()\n    spx_dates, spx_prices = load_index(\"SPX\")\n\n    ndx_dates = ndx_prices = sox_dates = sox_prices = vix_dates = vix_prices = None\n\n    try:\n        ndx_dates, ndx_prices = load_index(\"NDX\")\n    except Exception:\n        pass\n    try:\n        sox_dates, sox_prices = load_index(\"SOX\")\n    except Exception:\n        pass\n    try:\n        vix_dates, vix_prices = load_index(\"VIX\")\n    except Exception:\n        pass\n\n    assumptions = None\n    for name in [\"ASSUMPTIONS\", \"DEFAULT_ASSUMPTIONS\"]:\n        value = getattr(backtest, name, None)\n        if isinstance(value, dict):\n            assumptions = dict(value)\n            break\n\n    try:\n        result = backtest.run_stateful_simulation(\n            symbols=symbols,\n            prices_map=prices_map,\n            dates_map=dates_map,\n            spx_prices=spx_prices,\n            spx_dates=spx_dates,\n            ohlc_map=ohlc_map,\n            assumptions=assumptions,\n            step=1,\n            min_history=120,\n            market_score_default=60.0,\n            sim_start_date=START_DATE,\n            sim_end_date=END_DATE,\n            ndx_prices=ndx_prices,\n            ndx_dates=ndx_dates,\n            sox_prices=sox_prices,\n            sox_dates=sox_dates,\n            vix_prices=vix_prices,\n            vix_dates=vix_dates,\n        )\n    except Exception as exc:\n        report = {\n            \"generated_at\": now(),\n            \"stage\": \"B_STAGE_3_8E2F2C4C10F3C_E1_CORE_EXPORT\",\n            \"status\": \"E1_5Y_CORE_CANONICAL_NOT_READY\",\n            \"policy\": {\n                \"dashboard_changed\": False,\n                \"workflow_changed\": False,\n                \"strategy_logic_changed\": False,\n                \"frozen_strategy_imported_only\": True,\n                \"canonical_e1_written\": False,\n            },\n            \"input_summary\": {\n                \"symbols_loaded\": len(symbols),\n                \"symbols_rejected\": len(rejected),\n                \"rejected_sample\": rejected[:20],\n                \"spx_dates\": len(spx_dates),\n                \"spx_start\": spx_dates[0] if spx_dates else None,\n                \"spx_end\": spx_dates[-1] if spx_dates else None,\n                \"ndx_loaded\": bool(ndx_dates),\n                \"sox_loaded\": bool(sox_dates),\n                \"vix_loaded\": bool(vix_dates),\n                \"assumptions_source\": \"ASSUMPTIONS/DEFAULT_ASSUMPTIONS\" if assumptions else \"run_stateful_default\",\n                \"ohlc_contract\": \"dict[symbol] -> dict[open/high/low/close/volume] -> list\",\n            },\n            \"error\": type(exc).__name__ + \": \" + str(exc),\n            \"diagnosis\": [\n                \"Export-only wrapper called frozen run_stateful_simulation but it raised before producing candidate equity rows.\",\n                \"No canonical E1 export was written.\",\n            ],\n            \"canonical_written\": False,\n        }\n        write_json(REPORT_JSON, report)\n        REPORT_MD.write_text(\"# Stage 3.8E-2F-2C-4C-10F-3C E1 Core Export Report\\n\\nStatus: `E1_5Y_CORE_CANONICAL_NOT_READY`\\n\\nError: `\" + report[\"error\"] + \"`\\n\")\n        print(\"E1 5Y core export wrapper failed before candidate extraction\")\n        print(\"status:\", report[\"status\"])\n        print(\"error:\", report[\"error\"])\n        print(\"symbols_loaded:\", len(symbols))\n        print(\"report_json:\", rel(REPORT_JSON))\n        print(\"report_md:\", rel(REPORT_MD))\n        return 2\n\n    rows, chosen_shape, candidate_shapes = normalize_equity_rows(result)\n\n    validation = {\n        \"row_count\": len(rows),\n        \"unique_dates\": len({r[\"date\"] for r in rows}),\n        \"date_start\": rows[0][\"date\"] if rows else None,\n        \"date_end\": rows[-1][\"date\"] if rows else None,\n        \"one_row_per_date\": len(rows) == len({r[\"date\"] for r in rows}) if rows else False,\n        \"full_window\": bool(rows) and rows[0][\"date\"] <= \"2021-07-15\" and rows[-1][\"date\"] >= \"2026-06-01\",\n        \"capital_continuity_candidate\": bool(rows) and len(rows) == len({r[\"date\"] for r in rows}),\n        \"chosen_shape\": chosen_shape,\n    }\n\n    write_canonical = (\n        validation[\"row_count\"] >= 1000\n        and validation[\"one_row_per_date\"]\n        and validation[\"full_window\"]\n        and validation[\"capital_continuity_candidate\"]\n    )\n\n    canonical = None\n    if write_canonical:\n        canonical = {\n            \"strategy_id\": \"E1_AUDITED_G4_MINHOLD10\",\n            \"artifact_type\": \"canonical_continuous_capital_e1_5y_core_equity_curve\",\n            \"generated_at\": now(),\n            \"capital_model\": \"continuous_single_account\",\n            \"initial_capital\": INITIAL_CAPITAL,\n            \"simulation_start_date\": rows[0][\"date\"],\n            \"simulation_end_date\": rows[-1][\"date\"],\n            \"row_count\": len(rows),\n            \"unique_dates\": len({r[\"date\"] for r in rows}),\n            \"source\": \"src.engine.backtest.run_stateful_simulation\",\n            \"parameters\": {\n                \"sim_start_date\": START_DATE,\n                \"sim_end_date\": END_DATE,\n                \"step\": 1,\n                \"min_history\": 120,\n                \"market_score_default\": 60.0,\n                \"symbols\": len(symbols),\n                \"stock_dir\": rel(STOCK_DIR),\n                \"index_dir\": rel(INDEX_DIR),\n            },\n            \"rows\": rows,\n        }\n        write_json(OUT_JSON, canonical)\n\n    report = {\n        \"generated_at\": now(),\n        \"stage\": \"B_STAGE_3_8E2F2C4C10F3C_E1_CORE_EXPORT\",\n        \"status\": \"E1_5Y_CORE_CANONICAL_WRITTEN\" if write_canonical else \"E1_5Y_CORE_CANONICAL_NOT_READY\",\n        \"policy\": {\n            \"dashboard_changed\": False,\n            \"workflow_changed\": False,\n            \"strategy_logic_changed\": False,\n            \"frozen_strategy_imported_only\": True,\n            \"canonical_e1_written\": write_canonical,\n        },\n        \"input_summary\": {\n            \"symbols_loaded\": len(symbols),\n            \"symbols_rejected\": len(rejected),\n            \"rejected_sample\": rejected[:20],\n            \"spx_dates\": len(spx_dates),\n            \"spx_start\": spx_dates[0] if spx_dates else None,\n            \"spx_end\": spx_dates[-1] if spx_dates else None,\n            \"ndx_loaded\": bool(ndx_dates),\n            \"sox_loaded\": bool(sox_dates),\n            \"vix_loaded\": bool(vix_dates),\n            \"assumptions_source\": \"ASSUMPTIONS/DEFAULT_ASSUMPTIONS\" if assumptions else \"run_stateful_default\",\n        },\n        \"result_top_keys\": sorted(result.keys()) if isinstance(result, dict) else None,\n        \"candidate_shapes\": candidate_shapes[:80],\n        \"validation\": validation,\n        \"canonical_path\": rel(OUT_JSON),\n        \"canonical_written\": write_canonical,\n        \"diagnosis\": [\n            \"Called frozen run_stateful_simulation through an export-only wrapper.\",\n            \"Used explicit 5Y window and one continuous capital account validation.\",\n            \"Wrote E1 canonical only if row-count, one-row-per-date, full-window and continuity-candidate checks passed.\",\n        ],\n    }\n\n    write_json(REPORT_JSON, report)\n\n    md = []\n    md.append(\"# Stage 3.8E-2F-2C-4C-10F-3C E1 Core Export Report\")\n    md.append(\"\")\n    md.append(f\"Generated At: `{report['generated_at']}`\")\n    md.append(\"\")\n    md.append(\"## Status\")\n    md.append(\"\")\n    md.append(f\"- Status: `{report['status']}`\")\n    md.append(f\"- Canonical E1 written: `{write_canonical}`\")\n    md.append(f\"- Symbols loaded: `{len(symbols)}`\")\n    md.append(\"\")\n    md.append(\"## Validation\")\n    md.append(\"\")\n    md.append(\"```json\")\n    md.append(json.dumps(validation, indent=2, ensure_ascii=False))\n    md.append(\"```\")\n    md.append(\"\")\n    md.append(\"## Input Summary\")\n    md.append(\"\")\n    md.append(\"```json\")\n    md.append(json.dumps(report[\"input_summary\"], indent=2, ensure_ascii=False))\n    md.append(\"```\")\n    md.append(\"\")\n    md.append(\"## Candidate Shapes\")\n    md.append(\"\")\n    md.append(\"```json\")\n    md.append(json.dumps(candidate_shapes[:60], indent=2, ensure_ascii=False)[:18000])\n    md.append(\"```\")\n    REPORT_MD.write_text(\"\\n\".join(md) + \"\\n\")\n\n    print(\"E1 5Y core export wrapper complete\")\n    print(\"status:\", report[\"status\"])\n    print(\"symbols_loaded:\", len(symbols))\n    print(\"symbols_rejected:\", len(rejected))\n    print(\"result_top_keys:\", report[\"result_top_keys\"])\n    print(\"validation:\", json.dumps(validation, ensure_ascii=False))\n    print(\"canonical_written:\", write_canonical)\n    print(\"canonical_path:\", rel(OUT_JSON))\n    print(\"report_json:\", rel(REPORT_JSON))\n    print(\"report_md:\", rel(REPORT_MD))\n\n    return 0 if write_canonical else 2"
    }
  },
  "scripts/run_e1r_v0_2_oos_equity.py": {
    "main": {
      "line": 248,
      "end_line": 404,
      "matched_terms": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "source": "def main() -> None:\n    status = read_json(ROOT / \"exports/e1r_v0_2_status.json\", {}) or {}\n    summary = read_json(ROOT / \"exports/oos_e1r_v0_2_summary.json\", {}) or {}\n    sidecar = read_json(ROOT / \"exports/oos_e1r_v0_2_sidecar.json\", {}) or {}\n\n    out_path = ROOT / \"exports/oos_e1r_v0_2_equity_curve.json\"\n    existing = read_json(out_path, {}) or {}\n\n    generated_at = datetime.now(timezone.utc).isoformat()\n\n    status_date = (\n        summary.get(\"status_date\")\n        or status.get(\"status_date\")\n        or sidecar.get(\"status_date\")\n    )\n\n    if not status_date:\n        raise RuntimeError(\"Missing status_date from E1R v0.2 OOS status files\")\n\n    market_state = (\n        summary.get(\"market_state\")\n        or status.get(\"e1r_market_state\")\n        or \"UNKNOWN\"\n    )\n\n    core_active = bool(summary.get(\"core_active\", status.get(\"core\", {}).get(\"active\", False)))\n    sidecar_active = bool(summary.get(\"sidecar_active\", sidecar.get(\"active\", False)))\n    selected_count = int(summary.get(\"sidecar_selected_count\", sidecar.get(\"selected_count\", 0)) or 0)\n    current_sidecar_positions = normalize_current_sidecar_positions(sidecar)\n    price_map = load_stock_price_map()\n\n    initial_capital = 100000.0\n    legacy_core = extract_existing_oos_core_equity()\n\n    records = existing.get(\"records\", []) if isinstance(existing, dict) else []\n    if not isinstance(records, list):\n        records = []\n\n    records = [r for r in records if isinstance(r, dict)]\n    records = sorted(records, key=lambda r: str(r.get(\"date\", \"\")))\n\n    previous = records[-1] if records else None\n\n    if previous and previous.get(\"date\") == status_date:\n        # Idempotent update for the same date.\n        core_equity = safe_float(previous.get(\"core_equity\"), legacy_core[\"equity\"]) or initial_capital\n        sidecar_equity = safe_float(previous.get(\"sidecar_equity\"), initial_capital) or initial_capital\n        combined_equity = safe_float(previous.get(\"combined_equity\"), core_equity) or core_equity\n        prev_core_equity = core_equity\n        prev_sidecar_equity = sidecar_equity\n        prev_combined_equity = combined_equity\n        daily_core_return = safe_float(previous.get(\"core_daily_return\"), 0.0) or 0.0\n        daily_sidecar_return = safe_float(previous.get(\"sidecar_daily_return\"), 0.0) or 0.0\n        daily_combined_return = safe_float(previous.get(\"combined_daily_return\"), 0.0) or 0.0\n        sidecar_mtm_status = \"SAME_DATE_NO_NEW_MTM\"\n        sidecar_mtm_details = previous.get(\"sidecar_mtm_details\", [])\n        update_mode = \"UPDATED_EXISTING_DATE\"\n    else:\n        prev_core_equity = safe_float(previous.get(\"core_equity\"), None) if previous else None\n        prev_sidecar_equity = safe_float(previous.get(\"sidecar_equity\"), None) if previous else None\n        prev_combined_equity = safe_float(previous.get(\"combined_equity\"), None) if previous else None\n\n        if prev_core_equity is None:\n            prev_core_equity = initial_capital\n        if prev_sidecar_equity is None:\n            prev_sidecar_equity = initial_capital\n        if prev_combined_equity is None:\n            prev_combined_equity = initial_capital\n\n        # OOS-2B.2:\n        # Core equity bridges to legacy OOS equity if available.\n        # Sidecar MTM uses previous record's sidecar_positions to avoid lookahead.\n        core_equity = legacy_core[\"equity\"] if core_active else prev_core_equity\n\n        daily_core_return = compute_return(prev_core_equity, core_equity)\n\n        daily_sidecar_return, sidecar_mtm_status, sidecar_mtm_details = compute_sidecar_mtm_return(\n            previous_record=previous,\n            current_date=status_date,\n            price_map=price_map,\n        )\n        sidecar_equity = prev_sidecar_equity * (1.0 + daily_sidecar_return)\n\n        combined_daily_return = (1.0 + daily_core_return) * (1.0 + daily_sidecar_return) - 1.0\n        combined_equity = prev_combined_equity * (1.0 + combined_daily_return)\n\n        daily_combined_return = combined_daily_return\n        update_mode = \"APPENDED_NEW_DATE\"\n\n    record = {\n        \"date\": status_date,\n        \"generated_at\": generated_at,\n        \"market_state\": market_state,\n        \"core_active\": core_active,\n        \"sidecar_active\": sidecar_active,\n        \"sidecar_selected_count\": selected_count,\n        \"sidecar_positions\": current_sidecar_positions if sidecar_active else [],\n        \"sidecar_mtm_status\": sidecar_mtm_status,\n        \"sidecar_mtm_details\": sidecar_mtm_details,\n        \"core_equity\": core_equity,\n        \"sidecar_equity\": sidecar_equity,\n        \"combined_equity\": combined_equity,\n        \"core_daily_return\": daily_core_return,\n        \"sidecar_daily_return\": daily_sidecar_return,\n        \"combined_daily_return\": daily_combined_return,\n        \"core_source\": legacy_core[\"source\"],\n        \"sidecar_source\": \"previous_positions_close_to_close_mtm_when_available\",\n        \"combined_source\": \"core_bridge_plus_sidecar_target_only\",\n        \"execution_status\": \"PAPER_TRACKING_NO_REAL_EXECUTION\",\n        \"equity_status\": \"OOS_EQUITY_MTM_TRACKING_SIDECAR_PAPER\",\n        \"update_mode\": update_mode,\n    }\n\n    if previous and previous.get(\"date\") == status_date:\n        records[-1] = record\n    else:\n        records.append(record)\n\n    records = sorted(records, key=lambda r: str(r.get(\"date\", \"\")))\n\n    latest = records[-1]\n\n    output = {\n        \"generated_at\": generated_at,\n        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\",\n        \"phase\": \"OOS_2B_FORWARD_EQUITY_CURVE\",\n        \"equity_status\": \"OOS_EQUITY_MTM_TRACKING_SIDECAR_PAPER\",\n        \"execution_status\": \"PAPER_TRACKING_NO_REAL_EXECUTION\",\n        \"curve_type\": \"FORWARD_OOS_EQUITY\",\n        \"start_date\": records[0][\"date\"] if records else status_date,\n        \"end_date\": latest[\"date\"],\n        \"row_count\": len(records),\n        \"latest\": latest,\n        \"records\": records,\n        \"notes\": [\n            \"OOS-2B.2 adds sidecar close-to-close MTM tracking when previous positions are available.\",\n            \"Core equity bridges to existing legacy OOS equity when available.\",\n            \"Sidecar equity uses previous sidecar positions for close-to-close MTM to avoid lookahead.\",\n            \"No real orders are executed by this script.\",\n            \"OOS-2B.2 should add sidecar daily MTM and simulated/real position lifecycle.\",\n        ],\n    }\n\n    write_json(out_path, output)\n\n    print(\"E1R v0.2 OOS-2B equity export complete\")\n    print(\"status_date:\", status_date)\n    print(\"market_state:\", market_state)\n    print(\"core_active:\", core_active)\n    print(\"sidecar_active:\", sidecar_active)\n    print(\"sidecar_selected_count:\", selected_count)\n    print(\"core_equity:\", core_equity)\n    print(\"sidecar_equity:\", sidecar_equity)\n    print(\"combined_equity:\", combined_equity)\n    print(\"row_count:\", len(records))\n    print(\"update_mode:\", update_mode)\n    print(\"wrote:\", out_path.relative_to(ROOT))"
    }
  },
  "scripts/export_e1r_v0_2_status.py": {
    "main": {
      "line": 105,
      "end_line": 213,
      "matched_terms": [
        "E1R_REGIME_AWARE_V0_2",
        "sidecar_result"
      ],
      "source": "def main() -> None:\n    regime_path = ROOT / \"data/research/e1_5y/regimes/spx_regime_daily.json\"\n    stock_dir = ROOT / \"data/research/e1_5y/raw/stocks\"\n    spx_path = ROOT / \"data/research/e1_5y/raw/indices/SPX.json\"\n    legacy_market_path = ROOT / \"exports/market_state.json\"\n    out_path = ROOT / \"exports/e1r_v0_2_status.json\"\n\n    regime_json = read_json(regime_path)\n    latest = extract_latest_regime(regime_json)\n\n    date = str(pick(latest, [\"date\", \"as_of\", \"data_date\"], \"UNKNOWN\"))\n    regime = str(pick(latest, [\"regime\", \"market_regime\", \"state\"], \"UNKNOWN\")).upper()\n    subclass = str(pick(latest, [\"subclass\", \"regime_subclass\", \"market_subclass\", \"sideways_subclass\"], \"\") or \"\").upper()\n    e1r_market_state = normalize_e1r_state(regime, subclass)\n\n    config = E1RSidecarConfig(\n        start_date=\"2021-06-11\",\n        end_date=date,\n        allowed_subclasses=(\"MA_CONFLICT\",),\n        top_n=10,\n        gross_exposure=0.25,\n        min_history_days=200,\n        min_price=5.0,\n        initial_equity=100000.0,\n        excluded_symbols=(\"VIXY\",),\n    )\n\n    sidecar_result = build_e1r_sidecar_sleeve(\n        stock_dir=stock_dir,\n        spx_path=spx_path,\n        regime_path=regime_path,\n        config=config,\n    )\n\n    records = sidecar_result.get(\"records\", []) or []\n    last_record = None\n\n    for r in records:\n        if r.get(\"date\") == date or r.get(\"next_date\") == date:\n            last_record = r\n\n    if last_record is None and records:\n        last_record = records[-1]\n\n    holdings = []\n    if isinstance(last_record, dict):\n        raw_holdings = (\n            last_record.get(\"holdings\")\n            or last_record.get(\"selected\")\n            or last_record.get(\"selected_holdings\")\n            or []\n        )\n        if isinstance(raw_holdings, list):\n            holdings = [simplify_holding(h) for h in raw_holdings if isinstance(h, dict)]\n\n    sidecar_active = e1r_market_state == \"SIDEWAYS_MA_CONFLICT\" and len(holdings) > 0\n    core_active = e1r_market_state == \"UPTREND\"\n\n    status = {\n        \"generated_at\": datetime.now(timezone.utc).isoformat(),\n        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\",\n        \"version\": \"E1R-v0.2-formal-sidecar-sleeve\",\n        \"research_status\": \"FORMAL_SIDECAR_SLEEVE_ENGINE\",\n        \"status_date\": date,\n        \"e1r_market_state\": e1r_market_state,\n        \"regime\": regime,\n        \"subclass\": subclass or None,\n        \"mutually_exclusive_state_model\": True,\n        \"core\": {\n            \"strategy_id\": \"E1R_REGIME_AWARE_V0_1\",\n            \"active\": core_active,\n            \"active_condition\": \"UPTREND\",\n        },\n        \"sidecar\": {\n            \"active\": sidecar_active,\n            \"active_condition\": \"SIDEWAYS_MA_CONFLICT\",\n            \"gross_exposure\": 0.25,\n            \"top_n\": 10,\n            \"excluded_symbols\": [\"VIXY\"],\n            \"selected_count\": len(holdings),\n            \"selected\": holdings,\n            \"source_record_date\": last_record.get(\"date\") if isinstance(last_record, dict) else None,\n            \"source_record_next_date\": last_record.get(\"next_date\") if isinstance(last_record, dict) else None,\n        },\n        \"legacy_market_state\": extract_legacy_market_state(legacy_market_path),\n        \"source_files\": {\n            \"regime\": str(regime_path.relative_to(ROOT)),\n            \"stocks\": str(stock_dir.relative_to(ROOT)),\n            \"spx\": str(spx_path.relative_to(ROOT)),\n            \"legacy_market_state\": str(legacy_market_path.relative_to(ROOT)),\n        },\n        \"notes\": [\n            \"E1R v0.2 uses mutually exclusive daily market states.\",\n            \"Core is active only in UPTREND under the current v0.2 state model.\",\n            \"Sidecar is active only in SIDEWAYS_MA_CONFLICT when holdings are available.\",\n            \"This status export is a lightweight bridge for Dashboard and future OOS integration.\",\n        ],\n    }\n\n    write_json(out_path, status)\n\n    print(\"Wrote\", out_path)\n    print(\"status_date:\", status[\"status_date\"])\n    print(\"e1r_market_state:\", status[\"e1r_market_state\"])\n    print(\"regime:\", status[\"regime\"])\n    print(\"subclass:\", status[\"subclass\"])\n    print(\"core.active:\", status[\"core\"][\"active\"])\n    print(\"sidecar.active:\", status[\"sidecar\"][\"active\"])\n    print(\"sidecar.selected_count:\", status[\"sidecar\"][\"selected_count\"])"
    }
  },
  "scripts/export_e1r_v0_2_backtest_equity.py": {
    "main": {
      "line": 77,
      "end_line": 185,
      "matched_terms": [
        "e1r_v0_2_backtest_summary",
        "E1R_REGIME_AWARE_V0_2",
        "daily_equity_records",
        "variant_results"
      ],
      "source": "def main() -> None:\n    bt_path = ROOT / \"exports/backtest.json\"\n    if not bt_path.exists():\n        raise RuntimeError(\"Missing exports/backtest.json\")\n\n    bt = read_json(bt_path)\n    layer_d = bt.get(\"backtest\", {}).get(\"results\", {}).get(\"layer_d\", {})\n    variants = layer_d.get(\"variant_results\", {})\n\n    comparison_name = layer_d.get(\"name\")\n\n    v1 = extract_variant(variants, \"E1R_REGIME_AWARE_V0_1\")\n    v2 = extract_variant(variants, \"E1R_REGIME_AWARE_V0_2\")\n\n    v1_records = v1.get(\"daily_equity_records\") or v1.get(\"equity_curve\") or []\n    v2_records = v2.get(\"daily_equity_records\") or v2.get(\"equity_curve\") or []\n\n    v1_curve = normalize_curve(v1_records)\n    v2_curve = normalize_curve(v2_records)\n\n    if len(v1_curve) < 1000:\n        raise RuntimeError(f\"E1R v0.1 curve too short: {len(v1_curve)} rows. Expected 5Y-like curve.\")\n\n    if len(v2_curve) < 1000:\n        raise RuntimeError(f\"E1R v0.2 curve too short: {len(v2_curve)} rows. Expected 5Y-like curve.\")\n\n    start_date = v2_curve[0][\"date\"]\n    end_date = v2_curve[-1][\"date\"]\n\n    if start_date > \"2021-06-15\":\n        raise RuntimeError(f\"Start date looks too recent for 5Y export: {start_date}\")\n\n    if end_date < \"2026-06-15\":\n        raise RuntimeError(f\"End date looks too old for current 5Y export: {end_date}\")\n\n    summary = {\n        \"generated_at\": datetime.now(timezone.utc).isoformat(),\n        \"source\": \"exports/backtest.json\",\n        \"comparison_name\": comparison_name,\n        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\",\n        \"version\": v2.get(\"version\"),\n        \"research_status\": v2.get(\"research_status\"),\n        \"curve_type\": \"FULL_5Y_BACKTEST_EQUITY\",\n        \"start_date\": start_date,\n        \"end_date\": end_date,\n        \"row_count\": len(v2_curve),\n        \"v0_1\": {\n            \"strategy_id\": \"E1R_REGIME_AWARE_V0_1\",\n            \"total_return_pct\": v1.get(\"total_return_pct\"),\n            \"spx_return_pct\": v1.get(\"spx_return_pct\"),\n            \"alpha_pct\": v1.get(\"alpha_pct\"),\n            \"max_drawdown_pct\": v1.get(\"max_drawdown_pct\"),\n            \"profit_factor\": v1.get(\"profit_factor\"),\n            \"sharpe_ratio\": v1.get(\"sharpe_ratio\"),\n            \"research_status\": v1.get(\"research_status\"),\n            \"regime_aware_logic\": (v1.get(\"strategy_controls\") or {}).get(\"regime_aware_logic\"),\n            \"row_count\": len(v1_curve),\n        },\n        \"v0_2\": {\n            \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\",\n            \"total_return_pct\": v2.get(\"total_return_pct\"),\n            \"spx_return_pct\": v2.get(\"spx_return_pct\"),\n            \"alpha_pct\": v2.get(\"alpha_pct\"),\n            \"max_drawdown_pct\": v2.get(\"max_drawdown_pct\"),\n            \"profit_factor\": v2.get(\"profit_factor\"),\n            \"sharpe_ratio\": v2.get(\"sharpe_ratio\"),\n            \"research_status\": v2.get(\"research_status\"),\n            \"regime_aware_logic\": (v2.get(\"strategy_controls\") or {}).get(\"regime_aware_logic\"),\n            \"sidecar_active_days\": v2.get(\"sidecar_active_days\"),\n            \"sidecar_active_by_regime\": v2.get(\"sidecar_active_by_regime\"),\n            \"sidecar_active_by_subclass\": v2.get(\"sidecar_active_by_subclass\"),\n            \"composition_exists\": bool(v2.get(\"e1r_v0_2_composition\")),\n            \"row_count\": len(v2_curve),\n        },\n        \"notes\": [\n            \"This is the full 5Y E1R v0.2 backtest equity export for Dashboard display.\",\n            \"It is not the live OOS / forward equity curve.\",\n            \"OOS / forward equity will be exported separately in OOS-2B.\",\n            \"Large legacy backtest exports should not be committed with this lightweight export.\",\n        ],\n    }\n\n    equity_export = {\n        \"generated_at\": datetime.now(timezone.utc).isoformat(),\n        \"curve_type\": \"FULL_5Y_BACKTEST_EQUITY\",\n        \"start_date\": start_date,\n        \"end_date\": end_date,\n        \"row_count\": len(v2_curve),\n        \"series\": {\n            \"E1R_REGIME_AWARE_V0_1\": v1_curve,\n            \"E1R_REGIME_AWARE_V0_2\": v2_curve,\n        },\n        \"summary\": summary,\n    }\n\n    write_json(ROOT / \"exports/e1r_v0_2_backtest_summary.json\", summary)\n    write_json(ROOT / \"exports/e1r_v0_2_backtest_equity_curve.json\", equity_export)\n\n    print(\"Wrote exports/e1r_v0_2_backtest_summary.json\")\n    print(\"Wrote exports/e1r_v0_2_backtest_equity_curve.json\")\n    print(\"comparison_name:\", comparison_name)\n    print(\"curve_type:\", equity_export[\"curve_type\"])\n    print(\"start_date:\", start_date)\n    print(\"end_date:\", end_date)\n    print(\"row_count:\", len(v2_curve))\n    print(\"v0_1 return:\", summary[\"v0_1\"][\"total_return_pct\"])\n    print(\"v0_2 return:\", summary[\"v0_2\"][\"total_return_pct\"])\n    print(\"v0_2 maxDD:\", summary[\"v0_2\"][\"max_drawdown_pct\"])\n    print(\"sidecar_active_days:\", summary[\"v0_2\"][\"sidecar_active_days\"])"
    }
  },
  "scripts/run_e1r_v0_2_oos_core.py": {
    "main": {
      "line": 21,
      "end_line": 176,
      "matched_terms": [
        "E1R_REGIME_AWARE_V0_2"
      ],
      "source": "def main() -> None:\n    status_script = ROOT / \"scripts/export_e1r_v0_2_status.py\"\n    status_path = ROOT / \"exports/e1r_v0_2_status.json\"\n\n    if not status_script.exists():\n        raise RuntimeError(\"Missing scripts/export_e1r_v0_2_status.py\")\n\n    # Refresh the lightweight v0.2 status first.\n    runpy.run_path(str(status_script), run_name=\"__main__\")\n\n    if not status_path.exists():\n        raise RuntimeError(\"exports/e1r_v0_2_status.json was not generated\")\n\n    status = read_json(status_path)\n\n    generated_at = datetime.now(timezone.utc).isoformat()\n    status_date = status.get(\"status_date\")\n    strategy_id = status.get(\"strategy_id\", \"E1R_REGIME_AWARE_V0_2\")\n    market_state = status.get(\"e1r_market_state\", \"UNKNOWN\")\n    regime = status.get(\"regime\")\n    subclass = status.get(\"subclass\")\n\n    core = status.get(\"core\", {}) or {}\n    sidecar = status.get(\"sidecar\", {}) or {}\n    selected = sidecar.get(\"selected\", []) or []\n\n    core_active = bool(core.get(\"active\"))\n    sidecar_active = bool(sidecar.get(\"active\"))\n\n    phase = \"OOS_STATUS_SIGNAL_ONLY\"\n\n    summary = {\n        \"generated_at\": generated_at,\n        \"phase\": phase,\n        \"strategy_id\": strategy_id,\n        \"version\": status.get(\"version\"),\n        \"research_status\": status.get(\"research_status\"),\n        \"status_date\": status_date,\n        \"market_state\": market_state,\n        \"regime\": regime,\n        \"subclass\": subclass,\n        \"mutually_exclusive_state_model\": bool(status.get(\"mutually_exclusive_state_model\")),\n        \"core_active\": core_active,\n        \"sidecar_active\": sidecar_active,\n        \"sidecar_selected_count\": len(selected),\n        \"gross_exposure\": sidecar.get(\"gross_exposure\"),\n        \"top_n\": sidecar.get(\"top_n\"),\n        \"execution_status\": \"NO_REAL_EXECUTION\",\n        \"equity_status\": \"NOT_YET_CONNECTED\",\n        \"notes\": [\n            \"OOS-1 exports daily E1R v0.2 state and sidecar target signals only.\",\n            \"No real orders are executed by this script.\",\n            \"No E1R v0.2 OOS equity curve is updated by this script.\",\n            \"This is the bridge layer for Dashboard and future OOS equity integration.\",\n        ],\n    }\n\n    sidecar_export = {\n        \"generated_at\": generated_at,\n        \"phase\": phase,\n        \"strategy_id\": strategy_id,\n        \"status_date\": status_date,\n        \"market_state\": market_state,\n        \"regime\": regime,\n        \"subclass\": subclass,\n        \"active\": sidecar_active,\n        \"active_condition\": sidec
```

## JSON Probes

```json
[
  {
    "path": "data/research/e1r/e1r_formal_backtest_v0_1.json",
    "nodes": [
      {
        "path": "$",
        "matched_keys": [
          "equity_curve",
          "metrics"
        ],
        "summary": {
          "type": "dict",
          "keys": [
            "comparison_base",
            "e1_metrics",
            "equity_curve",
            "metrics",
            "source",
            "spx_curve",
            "status",
            "trades",
            "variant_id"
          ],
          "metric_like_values": {
            "status": "FORMAL_BACKTEST_AVAILABLE_RESEARCH_EXPORT"
          },
          "metrics_dict_keys": [
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
          ],
          "e1_metrics_dict_keys": [
            "max_drawdown_pct",
            "number_of_trades",
            "profit_factor",
            "sharpe_ratio",
            "total_return_pct"
          ],
          "equity_curve_len": 131,
          "spx_curve_len": 131,
          "trades_len": 39,
          "trades_first_keys": [
            "action_count",
            "actions_during_trade",
            "avg_cost",
            "dominant_regime",
            "effective_exit",
            "entry_adverse_gap_pct",
            "entry_date",
            "entry_price",
            "entry_regime",
            "entry_signal",
            "entry_type",
            "execution_model",
            "exit_adverse_gap_pct",
            "exit_date",
            "exit_price",
            "exit_reason",
            "exit_reasons",
            "exit_regime",
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
            "regime_day_weights",
            "relative_stop_exec_date",
            "relative_stop_triggered",
            "return_pct",
            "size_units_at_exit",
            "symbol",
            "take_profit_exec_date",
            "take_profit_triggered",
            "total_execution_drag_pct"
          ]
        }
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8D_NATIVE_RENDER_AUDIT.json",
    "nodes": [
      {
        "path": "$.key_neighborhoods",
        "matched_keys": [
          "equity_curve"
        ],
        "summary": {
          "type": "dict",
          "keys": [
            "e1_frozen_summary",
            "e1r_v02",
            "equity_curve",
            "market_state",
            "period_comparison",
            "research_backtest_title",
            "trade_log"
          ],
          "research_backtest_title_len": 1,
          "research_backtest_title_first_keys": [
            "context",
            "line",
            "needle"
          ],
          "period_comparison_len": 1,
          "period_comparison_first_keys": [
            "context",
            "line",
            "needle"
          ],
          "trade_log_len": 1,
          "trade_log_first_keys": [
            "context",
            "line",
            "needle"
          ],
          "equity_curve_len": 1,
          "equity_curve_first_keys": [
            "context",
            "line",
            "needle"
          ],
          "e1_frozen_summary_len": 1,
          "e1_frozen_summary_first_keys": [
            "context",
            "line",
            "needle"
          ],
          "e1r_v02_len": 1,
          "e1r_v02_first_keys": [
            "context",
            "line",
            "needle"
          ],
          "market_state_len": 0
        }
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2B_SUMMARY_INTEGRATION_REPORT.json",
    "nodes": [
      {
        "path": "$.untouched_blocks_validated",
        "matched_keys": [
          "equity_curve"
        ],
        "summary": {
          "type": "dict",
          "keys": [
            "equity_curve",
            "market_state",
            "trade_log"
          ]
        }
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json",
    "nodes": [
      {
        "path": "$.watched_file_reports",
        "matched_keys": [
          "exports/e1r_v0_2_backtest_summary.json"
        ],
        "summary": {
          "type": "dict",
          "keys": [
            ".github/workflows/update.yml",
            "dashboard/app.js",
            "data/oos/events.jsonl",
            "data/oos/portfolio_state.json",
            "data/oos/run_history.jsonl",
            "exports/e1r_v0_2_backtest_equity_curve.json",
            "exports/e1r_v0_2_backtest_summary.json",
            "exports/e1r_v0_2_status.json",
            "exports/oos_e1r_v0_2_equity_curve.json",
            "exports/oos_e1r_v0_2_orders.json",
            "exports/oos_e1r_v0_2_positions.json",
            "exports/oos_e1r_v0_2_sidecar.json",
            "exports/oos_e1r_v0_2_summary.json",
            "exports/oos_equity_curve.json",
            "exports/oos_orders.json",
            "exports/oos_positions.json",
            "exports/oos_summary.json",
            "exports/oos_trades.json",
            "scripts/backtest.py",
            "scripts/init_data.py",
            "scripts/update_pipeline.py",
            "src/engine/backtest.py",
            "src/engine/e1r_composer.py",
            "src/engine/e1r_sidecar_sleeve.py"
          ],
          ".github/workflows/update.yml_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "scripts/update_pipeline.py_dict_keys": [
            "exists",
            "hits",
            "line_hits",
            "path"
          ],
          "scripts/init_data.py_dict_keys": [
            "exists",
            "hits",
            "line_hits",
            "path"
          ],
          "scripts/backtest.py_dict_keys": [
            "exists",
            "hits",
            "line_hits",
            "path"
          ],
          "src/engine/backtest.py_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "src/engine/e1r_composer.py_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "src/engine/e1r_sidecar_sleeve.py_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "dashboard/app.js_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "exports/oos_summary.json_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "exports/oos_equity_curve.json_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "exports/oos_orders.json_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "exports/oos_positions.json_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "exports/oos_trades.json_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "exports/oos_e1r_v0_2_summary.json_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "exports/oos_e1r_v0_2_equity_curve.json_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "exports/oos_e1r_v0_2_orders.json_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "exports/oos_e1r_v0_2_positions.json_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "exports/oos_e1r_v0_2_sidecar.json_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "exports/e1r_v0_2_status.json_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "exports/e1r_v0_2_backtest_summary.json_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "exports/e1r_v0_2_backtest_equity_curve.json_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "data/oos/portfolio_state.json_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "data/oos/events.jsonl_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ],
          "data/oos/run_history.jsonl_dict_keys": [
            "exists",
            "hits",
            "line_count",
            "line_hits",
            "path"
          ]
        }
      },
      {
        "path": "$.json_reports",
        "matched_keys": [
          "exports/e1r_v0_2_backtest_summary.json"
        ],
        "summary": {
          "type": "dict",
          "keys": [
            "data/oos/portfolio_state.json",
            "exports/e1r_v0_2_backtest_equity_curve.json",
            "exports/e1r_v0_2_backtest_summary.json",
            "exports/e1r_v0_2_status.json",
            "exports/oos_e1r_v0_2_equity_curve.json",
            "exports/oos_e1r_v0_2_orders.json",
            "exports/oos_e1r_v0_2_positions.json",
            "exports/oos_e1r_v0_2_sidecar.json",
            "exports/oos_e1r_v0_2_summary.json",
            "exports/oos_equity_curve.json",
            "exports/oos_orders.json",
            "exports/oos_positions.json",
            "exports/oos_summary.json",
            "exports/oos_trades.json"
          ],
          "exports/oos_summary.json_dict_keys": [
            "field_presence",
            "meta",
            "preview"
          ],
          "exports/oos_equity_curve.json_dict_keys": [
            "field_presence",
            "meta",
            "preview"
          ],
          "exports/oos_orders.json_dict_keys": [
            "field_presence",
            "meta",
            "preview"
          ],
          "exports/oos_positions.json_dict_keys": [
            "field_presence",
            "meta",
            "preview"
          ],
          "exports/oos_trades.json_dict_keys": [
            "field_presence",
            "meta",
            "preview"
          ],
          "exports/oos_e1r_v0_2_summary.json_dict_keys": [
            "field_presence",
            "meta",
            "preview"
          ],
          "exports/oos_e1r_v0_2_equity_curve.json_dict_keys": [
            "field_presence",
            "meta",
            "preview"
          ],
          "exports/oos_e1r_v0_2_orders.json_dict_keys": [
            "field_presence",
            "meta",
            "preview"
          ],
          "exports/oos_e1r_v0_2_positions.json_dict_keys": [
            "field_presence",
            "meta",
            "preview"
          ],
          "exports/oos_e1r_v0_2_sidecar.json_dict_keys": [
            "field_presence",
            "meta",
            "preview"
          ],
          "exports/e1r_v0_2_status.json_dict_keys": [
            "field_presence",
            "meta",
            "preview"
          ],
          "exports/e1r_v0_2_backtest_summary.json_dict_keys": [
            "field_presence",
            "meta",
            "preview"
          ],
          "exports/e1r_v0_2_backtest_equity_curve.json_dict_keys": [
            "field_presence",
            "meta",
            "preview"
          ],
          "data/oos/portfolio_state.json_dict_keys": [
            "field_presence",
            "meta",
            "preview"
          ]
        }
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F1B_FORWARD_IMPLEMENTATION_PLAN.json",
    "nodes": [
      {
        "path": "$.current_exports.e1",
        "matched_keys": [
          "equity_curve"
        ],
        "summary": {
          "type": "dict",
          "keys": [
            "equity_curve",
            "orders",
            "positions",
            "state",
            "summary",
            "trades"
          ]
        }
      },
      {
        "path": "$.current_exports.e1r_existing_scaffold",
        "matched_keys": [
          "equity_curve"
        ],
        "summary": {
          "type": "dict",
          "keys": [
            "equity_curve",
            "orders",
            "positions",
            "sidecar",
            "status",
            "summary"
          ],
          "metric_like_values": {
            "status": "exports/e1r_v0_2_status.json"
          }
        }
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F1D_FORWARD_PERFORMANCE_IMPLEMENTATION.json",
    "nodes": [
      {
        "path": "$.outputs",
        "matched_keys": [
          "equity_curve"
        ],
        "summary": {
          "type": "dict",
          "keys": [
            "equity_curve",
            "events",
            "orders",
            "positions",
            "run_history",
            "state",
            "summary"
          ]
        }
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json",
    "nodes": [
      {
        "path": "$.data_reports",
        "matched_keys": [
          "exports/e1r_v0_2_backtest_summary.json"
        ],
        "summary": {
          "type": "dict",
          "keys": [
            "data/oos/e1r_v0_2_portfolio_state.json",
            "exports/e1r_v0_2_backtest_equity_curve.json",
            "exports/e1r_v0_2_backtest_summary.json",
            "exports/e1r_v0_2_status.json",
            "exports/leaderboard.json",
            "exports/market_state.json",
            "exports/oos_e1r_v0_2_equity_curve.json",
            "exports/oos_e1r_v0_2_orders.json",
            "exports/oos_e1r_v0_2_positions.json",
            "exports/oos_e1r_v0_2_sidecar.json",
            "exports/oos_e1r_v0_2_sidecar_lifecycle.json",
            "exports/oos_e1r_v0_2_sidecar_turnover.json",
            "exports/oos_e1r_v0_2_summary.json"
          ],
          "exports/e1r_v0_2_status.json_dict_keys": [
            "candidate_arrays",
            "candidate_objects",
            "meta",
            "preview"
          ],
          "exports/oos_e1r_v0_2_summary.json_dict_keys": [
            "candidate_arrays",
            "candidate_objects",
            "meta",
            "preview"
          ],
          "exports/oos_e1r_v0_2_equity_curve.json_dict_keys": [
            "candidate_arrays",
            "candidate_objects",
            "meta",
            "preview"
          ],
          "exports/oos_e1r_v0_2_positions.json_dict_keys": [
            "candidate_arrays",
            "candidate_objects",
            "meta",
            "preview"
          ],
          "exports/oos_e1r_v0_2_orders.json_dict_keys": [
            "candidate_arrays",
            "candidate_objects",
            "meta",
            "preview"
          ],
          "exports/oos_e1r_v0_2_sidecar.json_dict_keys": [
            "candidate_arrays",
            "candidate_objects",
            "meta",
            "preview"
          ],
          "exports/oos_e1r_v0_2_sidecar_lifecycle.json_dict_keys": [
            "candidate_arrays",
            "candidate_objects",
            "meta",
            "preview"
          ],
          "exports/oos_e1r_v0_2_sidecar_turnover.json_dict_keys": [
            "candidate_arrays",
            "candidate_objects",
            "meta",
            "preview"
          ],
          "exports/e1r_v0_2_backtest_summary.json_dict_keys": [
            "candidate_arrays",
            "candidate_objects",
            "meta",
            "preview"
          ],
          "exports/e1r_v0_2_backtest_equity_curve.json_dict_keys": [
            "candidate_arrays",
            "candidate_objects",
            "meta",
            "preview"
          ],
          "exports/leaderboard.json_dict_keys": [
            "candidate_arrays",
            "candidate_objects",
            "meta",
            "preview"
          ],
          "exports/market_state.json_dict_keys": [
            "candidate_arrays",
            "candidate_objects",
            "meta",
            "preview"
          ],
          "data/oos/e1r_v0_2_portfolio_state.json_dict_keys": [
            "candidate_arrays",
            "candidate_objects",
            "meta",
            "preview"
          ]
        }
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json",
    "nodes": [
      {
        "path": "$.export_summaries",
        "matched_keys": [
          "exports/e1r_v0_2_backtest_summary.json"
        ],
        "summary": {
          "type": "dict",
          "keys": [
            "exports/e1r_v0_2_backtest_equity_curve.json",
            "exports/e1r_v0_2_backtest_summary.json",
            "exports/e1r_v0_2_status.json",
            "exports/equity_curve.json",
            "exports/market_state.json",
            "exports/oos_e1r_v0_2_equity_curve.json",
            "exports/oos_e1r_v0_2_orders.json",
            "exports/oos_e1r_v0_2_orders_preview.json",
            "exports/oos_e1r_v0_2_positions.json",
            "exports/oos_e1r_v0_2_positions_preview.json",
            "exports/oos_e1r_v0_2_sidecar.json",
            "exports/oos_e1r_v0_2_sidecar_lifecycle.json",
            "exports/oos_e1r_v0_2_sidecar_turnover.json",
            "exports/oos_e1r_v0_2_summary.json",
            "exports/oos_e1r_v0_2_targets.json",
            "exports/oos_equity_curve.json",
            "exports/oos_summary.json"
          ],
          "exports/e1r_v0_2_backtest_equity_curve.json_dict_keys": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ],
          "exports/e1r_v0_2_backtest_summary.json_dict_keys": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ],
          "exports/e1r_v0_2_status.json_dict_keys": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ],
          "exports/equity_curve.json_dict_keys": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ],
          "exports/market_state.json_dict_keys": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ],
          "exports/oos_e1r_v0_2_equity_curve.json_dict_keys": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ],
          "exports/oos_e1r_v0_2_orders.json_dict_keys": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ],
          "exports/oos_e1r_v0_2_orders_preview.json_dict_keys": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ],
          "exports/oos_e1r_v0_2_positions.json_dict_keys": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ],
          "exports/oos_e1r_v0_2_positions_preview.json_dict_keys": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ],
          "exports/oos_e1r_v0_2_sidecar.json_dict_keys": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ],
          "exports/oos_e1r_v0_2_sidecar_lifecycle.json_dict_keys": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ],
          "exports/oos_e1r_v0_2_sidecar_turnover.json_dict_keys": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ],
          "exports/oos_e1r_v0_2_summary.json_dict_keys": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ],
          "exports/oos_e1r_v0_2_targets.json_dict_keys": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ],
          "exports/oos_equity_curve.json_dict_keys": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ],
          "exports/oos_summary.json_dict_keys": [
            "json_valid",
            "regime_like_keys",
            "regime_like_samples",
            "row_count",
            "top_level_keys",
            "top_level_type"
          ]
        }
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10E_R_CONTINUOUS_CAPITAL_CONTRACT.json",
    "nodes": [
      {
        "path": "$.json_reports",
        "matched_keys": [
          "exports/e1r_v0_2_backtest_summary.json"
        ],
        "summary": {
          "type": "dict",
          "keys": [
            "data/research/e1_5y/regimes/spx_regime_daily.json",
            "exports/backtest.json",
            "exports/e1r_v0_2_backtest_equity_curve.json",
            "exports/e1r_v0_2_backtest_summary.json",
            "exports/oos_e1r_v0_2_equity_curve.json",
            "exports/oos_equity_curve.json",
            "exports/portfolio_backtest.json"
          ],
          "exports/portfolio_backtest.json_dict_keys": [
            "exists",
            "json_valid",
            "lists",
            "path",
            "top_keys",
            "type"
          ],
          "exports/backtest.json_dict_keys": [
            "exists",
            "json_valid",
            "lists",
            "path",
            "top_keys",
            "type"
          ],
          "exports/e1r_v0_2_backtest_summary.json_dict_keys": [
            "exists",
            "json_valid",
            "lists",
            "path",
            "top_keys",
            "type"
          ],
          "exports/e1r_v0_2_backtest_equity_curve.json_dict_keys": [
            "exists",
            "json_valid",
            "lists",
            "path",
            "top_keys",
            "type"
          ],
          "exports/oos_equity_curve.json_dict_keys": [
            "exists",
            "json_valid",
            "lists",
            "path",
            "top_keys",
            "type"
          ],
          "exports/oos_e1r_v0_2_equity_curve.json_dict_keys": [
            "exists",
            "json_valid",
            "lists",
            "path",
            "type"
          ],
          "data/research/e1_5y/regimes/spx_regime_daily.json_dict_keys": [
            "exists",
            "json_valid",
            "lists",
            "path",
            "top_keys",
            "type"
          ]
        }
      }
    ]
  },
  {
    "path": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F1_E1_CONTINUOUS_CORE_RECOVERY.json",
    "nodes": [
      {
        "path": "$.json_reports_after_run.exports/backtest.json",
        "matched_keys": [
          "metrics"
        ],
        "summary": {
          "type": "dict",
          "keys": [
            "exists",
            "json_valid",
            "lists",
            "metrics",
            "path",
            "top_keys",
            "type"
          ],
          "top_keys_len": 3,
          "metrics_dict_keys": [
            "alpha_pct",
            "initial_capital",
            "max_drawdown_pct",
            "name",
            "profit_factor",
            "sample_validity",
            "selected_variant",
            "sharpe_ratio",
            "spx_total_return_pct",
            
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-4B-0E`: Dry-run exact E1R frozen generator candidate
- Recommended action: Trace the generator candidate that calls compose_e1r_v0_2_variant and rerun it in dry-run/no-write mode to recover core_variant_result and daily equity.

