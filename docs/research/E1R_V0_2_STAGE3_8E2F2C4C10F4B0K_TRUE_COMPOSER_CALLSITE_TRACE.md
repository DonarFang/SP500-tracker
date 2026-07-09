# Stage 3.8E-2F-2C-4C-10F-4B-0K True Composer Callsite Trace

Generated At: `2026-07-09T10:46:03.972169+00:00`

## Status

- Status: `E1R_TRUE_COMPOSER_CALLSITE_TRACE_COMPLETE_NO_EXECUTION`
- Source only: `True`
- E1R canonical written: `False`
- Strategy files unchanged: `True`
- Canonical existence unchanged: `True`

## Summary

```json
{
  "source_files_scanned": 50,
  "grep_hit_file_count": 15,
  "ast_call_hit_file_count": 4,
  "direct_compose_file_count": 2,
  "core_builder_file_count": 4,
  "composer_related_file_count": 2
}
```

## Conclusion

- `TRUE_DIRECT_COMPOSER_CALLSITE_FOUND`
- Recommended: Instrument the top true direct composer callsite in no-write mode.

## Direct Compose Files

```json
[
  {
    "path": "src/engine/e1r_composer.py",
    "score": 803,
    "hit_count": 23,
    "hits": [
      {
        "line": 9,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 4,
            "text": "Composes:"
          },
          {
            "line": 5,
            "text": "- E1R_REGIME_AWARE_V0_1 core daily equity records"
          },
          {
            "line": 6,
            "text": "- E1R sidecar sleeve daily return records"
          },
          {
            "line": 7,
            "text": ""
          },
          {
            "line": 8,
            "text": "into:"
          },
          {
            "line": 9,
            "text": "- E1R_REGIME_AWARE_V0_2 formal combined daily equity records"
          },
          {
            "line": 10,
            "text": ""
          },
          {
            "line": 11,
            "text": "Alignment rule"
          },
          {
            "line": 12,
            "text": "--------------"
          },
          {
            "line": 13,
            "text": "Core daily equity record date means:"
          },
          {
            "line": 14,
            "text": "    previous trading day close -> date close"
          }
        ]
      },
      {
        "line": 94,
        "matched": [
          "extract_core_interval_returns"
        ],
        "context": [
          {
            "line": 89,
            "text": "        return float(\"inf\")"
          },
          {
            "line": 90,
            "text": ""
          },
          {
            "line": 91,
            "text": "    return gains / losses"
          },
          {
            "line": 92,
            "text": ""
          },
          {
            "line": 93,
            "text": ""
          },
          {
            "line": 94,
            "text": "def extract_core_interval_returns("
          },
          {
            "line": 95,
            "text": "    core_daily_equity_records: Sequence[dict[str, Any]],"
          },
          {
            "line": 96,
            "text": "    sidecar_records: Sequence[dict[str, Any]],"
          },
          {
            "line": 97,
            "text": ") -> list[dict[str, Any]]:"
          },
          {
            "line": 98,
            "text": "    \"\"\""
          },
          {
            "line": 99,
            "text": "    Align core daily returns to sidecar intervals by next_date."
          }
        ]
      },
      {
        "line": 171,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 166,
            "text": "        })"
          },
          {
            "line": 167,
            "text": ""
          },
          {
            "line": 168,
            "text": "    return aligned"
          },
          {
            "line": 169,
            "text": ""
          },
          {
            "line": 170,
            "text": ""
          },
          {
            "line": 171,
            "text": "def build_equity_records_from_returns("
          },
          {
            "line": 172,
            "text": "    interval_records: Sequence[dict[str, Any]],"
          },
          {
            "line": 173,
            "text": "    initial_equity: float,"
          },
          {
            "line": 174,
            "text": ") -> list[dict[str, Any]]:"
          },
          {
            "line": 175,
            "text": "    equity = initial_equity"
          },
          {
            "line": 176,
            "text": "    peak = initial_equity"
          }
        ]
      },
      {
        "line": 283,
        "matched": [
          "compose_e1r_v0_2_variant"
        ],
        "context": [
          {
            "line": 278,
            "text": "            for k, v in contribution_by_subclass.items()"
          },
          {
            "line": 279,
            "text": "        },"
          },
          {
            "line": 280,
            "text": "    }"
          },
          {
            "line": 281,
            "text": ""
          },
          {
            "line": 282,
            "text": ""
          },
          {
            "line": 283,
            "text": "def compose_e1r_v0_2_variant("
          },
          {
            "line": 284,
            "text": "    core_variant_result: dict[str, Any],"
          },
          {
            "line": 285,
            "text": "    sidecar_result: dict[str, Any],"
          },
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          }
        ]
      },
      {
        "line": 284,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 279,
            "text": "        },"
          },
          {
            "line": 280,
            "text": "    }"
          },
          {
            "line": 281,
            "text": ""
          },
          {
            "line": 282,
            "text": ""
          },
          {
            "line": 283,
            "text": "def compose_e1r_v0_2_variant("
          },
          {
            "line": 284,
            "text": "    core_variant_result: dict[str, Any],"
          },
          {
            "line": 285,
            "text": "    sidecar_result: dict[str, Any],"
          },
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          }
        ]
      },
      {
        "line": 285,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 280,
            "text": "    }"
          },
          {
            "line": 281,
            "text": ""
          },
          {
            "line": 282,
            "text": ""
          },
          {
            "line": 283,
            "text": "def compose_e1r_v0_2_variant("
          },
          {
            "line": 284,
            "text": "    core_variant_result: dict[str, Any],"
          },
          {
            "line": 285,
            "text": "    sidecar_result: dict[str, Any],"
          },
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          },
          {
            "line": 290,
            "text": ""
          }
        ]
      },
      {
        "line": 288,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 283,
            "text": "def compose_e1r_v0_2_variant("
          },
          {
            "line": 284,
            "text": "    core_variant_result: dict[str, Any],"
          },
          {
            "line": 285,
            "text": "    sidecar_result: dict[str, Any],"
          },
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          },
          {
            "line": 290,
            "text": ""
          },
          {
            "line": 291,
            "text": "    interval_records = extract_core_interval_returns(core_records, sidecar_records)"
          },
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          }
        ]
      },
      {
        "line": 289,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 284,
            "text": "    core_variant_result: dict[str, Any],"
          },
          {
            "line": 285,
            "text": "    sidecar_result: dict[str, Any],"
          },
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          },
          {
            "line": 290,
            "text": ""
          },
          {
            "line": 291,
            "text": "    interval_records = extract_core_interval_returns(core_records, sidecar_records)"
          },
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          },
          {
            "line": 294,
            "text": ""
          }
        ]
      },
      {
        "line": 291,
        "matched": [
          "extract_core_interval_returns"
        ],
        "context": [
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          },
          {
            "line": 290,
            "text": ""
          },
          {
            "line": 291,
            "text": "    interval_records = extract_core_interval_returns(core_records, sidecar_records)"
          },
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          },
          {
            "line": 294,
            "text": ""
          },
          {
            "line": 295,
            "text": "    result = copy.deepcopy(core_variant_result)"
          },
          {
            "line": 296,
            "text": ""
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
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          },
          {
            "line": 290,
            "text": ""
          },
          {
            "line": 291,
            "text": "    interval_records = extract_core_interval_returns(core_records, sidecar_records)"
          },
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          },
          {
            "line": 294,
            "text": ""
          },
          {
            "line": 295,
            "text": "    result = copy.deepcopy(core_variant_result)"
          },
          {
            "line": 296,
            "text": ""
          },
          {
            "line": 297,
            "text": "    sidecar_summary = sidecar_result.get(\"summary\", {}) or {}"
          }
        ]
      },
      {
        "line": 295,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 290,
            "text": ""
          },
          {
            "line": 291,
            "text": "    interval_records = extract_core_interval_returns(core_records, sidecar_records)"
          },
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          },
          {
            "line": 294,
            "text": ""
          },
          {
            "line": 295,
            "text": "    result = copy.deepcopy(core_variant_result)"
          },
          {
            "line": 296,
            "text": ""
          },
          {
            "line": 297,
            "text": "    sidecar_summary = sidecar_result.get(\"summary\", {}) or {}"
          },
          {
            "line": 298,
            "text": ""
          },
          {
            "line": 299,
            "text": "    result.update({"
          },
          {
            "line": 300,
            "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          }
        ]
      },
      {
        "line": 297,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          },
          {
            "line": 294,
            "text": ""
          },
          {
            "line": 295,
            "text": "    result = copy.deepcopy(core_variant_result)"
          },
          {
            "line": 296,
            "text": ""
          },
          {
            "line": 297,
            "text": "    sidecar_summary = sidecar_result.get(\"summary\", {}) or {}"
          },
          {
            "line": 298,
            "text": ""
          },
          {
            "line": 299,
            "text": "    result.update({"
          },
          {
            "line": 300,
            "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 301,
            "text": "        \"strategy_variant\": \"E1R_regime_aware_v0_2_formal_sidecar_sleeve\","
          },
          {
            "line": 302,
            "text": "        \"version\": \"E1R-v0.2-formal-sidecar-sleeve\","
          }
        ]
      },
      {
        "line": 300,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 295,
            "text": "    result = copy.deepcopy(core_variant_result)"
          },
          {
            "line": 296,
            "text": ""
          },
          {
            "line": 297,
            "text": "    sidecar_summary = sidecar_result.get(\"summary\", {}) or {}"
          },
          {
            "line": 298,
            "text": ""
          },
          {
            "line": 299,
            "text": "    result.update({"
          },
          {
            "line": 300,
            "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 301,
            "text": "        \"strategy_variant\": \"E1R_regime_aware_v0_2_formal_sidecar_sleeve\","
          },
          {
            "line": 302,
            "text": "        \"version\": \"E1R-v0.2-formal-sidecar-sleeve\","
          },
          {
            "line": 303,
            "text": "        \"research_status\": \"FORMAL_SIDECAR_SLEEVE_ENGINE\","
          },
          {
            "line": 304,
            "text": "        \"core_total_trades\": core_variant_result.get(\"total_trades\"),"
          },
          {
            "line": 305,
            "text": "        \"sidecar_trade_count_approx\": sidecar_summary.get(\"trade_count_approx\"),"
          }
        ]
      },
      {
        "line": 304,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 299,
            "text": "    result.update({"
          },
          {
            "line": 300,
            "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 301,
            "text": "        \"strategy_variant\": \"E1R_regime_aware_v0_2_formal_sidecar_sleeve\","
          },
          {
            "line": 302,
            "text": "        \"version\": \"E1R-v0.2-formal-sidecar-sleeve\","
          },
          {
            "line": 303,
            "text": "        \"research_status\": \"FORMAL_SIDECAR_SLEEVE_ENGINE\","
          },
          {
            "line": 304,
            "text": "        \"core_total_trades\": core_variant_result.get(\"total_trades\"),"
          },
          {
            "line": 305,
            "text": "        \"sidecar_trade_count_approx\": sidecar_summary.get(\"trade_count_approx\"),"
          },
          {
            "line": 306,
            "text": "        \"combined_trade_count_note\": ("
          },
          {
            "line": 307,
            "text": "            \"total_trades remains inherited from E1R v0.1 core; \""
          },
          {
            "line": 308,
            "text": "            \"sidecar_trade_count_approx counts daily basket holdings and is not \""
          },
          {
            "line": 309,
            "text": "            \"stateful round-trip trade count.\""
          }
        ]
      },
      {
        "line": 313,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 308,
            "text": "            \"sidecar_trade_count_approx counts daily basket holdings and is not \""
          },
          {
            "line": 309,
            "text": "            \"stateful round-trip trade count.\""
          },
          {
            "line": 310,
            "text": "        ),"
          },
          {
            "line": 311,
            "text": "        \"e1r_v0_2_composition\": {"
          },
          {
            "line": 312,
            "text": "            \"core_variant\": \"E1R_REGIME_AWARE_V0_1\","
          },
          {
            "line": 313,
            "text": "            \"sidecar_engine\": sidecar_result.get(\"engine\"),"
          },
          {
            "line": 314,
            "text": "            \"sidecar_version\": sidecar_result.get(\"version\"),"
          },
          {
            "line": 315,
            "text": "            \"alignment\": \"core daily return ending at next_date aligned to sidecar date->next_date interval\","
          },
          {
            "line": 316,
            "text": "            \"composition_formula\": \"(1 + core_return) * (1 + sidecar_return) - 1\","
          },
          {
            "line": 317,
            "text": "            \"sidecar_config\": sidecar_result.get(\"config\", {}),"
          },
          {
            "line": 318,
            "text": "            \"sidecar_sample\": sidecar_result.get(\"sample\", {}),"
          }
        ]
      },
      {
        "line": 314,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 309,
            "text": "            \"stateful round-trip trade count.\""
          },
          {
            "line": 310,
            "text": "        ),"
          },
          {
            "line": 311,
            "text": "        \"e1r_v0_2_composition\": {"
          },
          {
            "line": 312,
            "text": "            \"core_variant\": \"E1R_REGIME_AWARE_V0_1\","
          },
          {
            "line": 313,
            "text": "            \"sidecar_engine\": sidecar_result.get(\"engine\"),"
          },
          {
            "line": 314,
            "text": "            \"sidecar_version\": sidecar_result.get(\"version\"),"
          },
          {
            "line": 315,
            "text": "            \"alignment\": \"core daily return ending at next_date aligned to sidecar date->next_date interval\","
          },
          {
            "line": 316,
            "text": "            \"composition_formula\": \"(1 + core_return) * (1 + sidecar_return) - 1\","
          },
          {
            "line": 317,
            "text": "            \"sidecar_config\": sidecar_result.get(\"config\", {}),"
          },
          {
            "line": 318,
            "text": "            \"sidecar_sample\": sidecar_result.get(\"sample\", {}),"
          },
          {
            "line": 319,
            "text": "            \"sidecar_summary\": sidecar_result.get(\"summary\", {}),"
          }
        ]
      },
      {
        "line": 317,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 312,
            "text": "            \"core_variant\": \"E1R_REGIME_AWARE_V0_1\","
          },
          {
            "line": 313,
            "text": "            \"sidecar_engine\": sidecar_result.get(\"engine\"),"
          },
          {
            "line": 314,
            "text": "            \"sidecar_version\": sidecar_result.get(\"version\"),"
          },
          {
            "line": 315,
            "text": "            \"alignment\": \"core daily return ending at next_date aligned to sidecar date->next_date interval\","
          },
          {
            "line": 316,
            "text": "            \"composition_formula\": \"(1 + core_return) * (1 + sidecar_return) - 1\","
          },
          {
            "line": 317,
            "text": "            \"sidecar_config\": sidecar_result.get(\"config\", {}),"
          },
          {
            "line": 318,
            "text": "            \"sidecar_sample\": sidecar_result.get(\"sample\", {}),"
          },
          {
            "line": 319,
            "text": "            \"sidecar_summary\": sidecar_result.get(\"summary\", {}),"
          },
          {
            "line": 320,
            "text": "            \"combined_summary\": summary,"
          },
          {
            "line": 321,
            "text": "        },"
          },
          {
            "line": 322,
            "text": "        \"daily_equity_records\": equity_records,"
          }
        ]
      },
      {
        "line": 318,
        "matched": [
   
```

## Core Builder Files

```json
[
  {
    "path": "src/engine/e1r_composer.py",
    "score": 803,
    "hit_count": 23,
    "hits": [
      {
        "line": 9,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 4,
            "text": "Composes:"
          },
          {
            "line": 5,
            "text": "- E1R_REGIME_AWARE_V0_1 core daily equity records"
          },
          {
            "line": 6,
            "text": "- E1R sidecar sleeve daily return records"
          },
          {
            "line": 7,
            "text": ""
          },
          {
            "line": 8,
            "text": "into:"
          },
          {
            "line": 9,
            "text": "- E1R_REGIME_AWARE_V0_2 formal combined daily equity records"
          },
          {
            "line": 10,
            "text": ""
          },
          {
            "line": 11,
            "text": "Alignment rule"
          },
          {
            "line": 12,
            "text": "--------------"
          },
          {
            "line": 13,
            "text": "Core daily equity record date means:"
          },
          {
            "line": 14,
            "text": "    previous trading day close -> date close"
          }
        ]
      },
      {
        "line": 94,
        "matched": [
          "extract_core_interval_returns"
        ],
        "context": [
          {
            "line": 89,
            "text": "        return float(\"inf\")"
          },
          {
            "line": 90,
            "text": ""
          },
          {
            "line": 91,
            "text": "    return gains / losses"
          },
          {
            "line": 92,
            "text": ""
          },
          {
            "line": 93,
            "text": ""
          },
          {
            "line": 94,
            "text": "def extract_core_interval_returns("
          },
          {
            "line": 95,
            "text": "    core_daily_equity_records: Sequence[dict[str, Any]],"
          },
          {
            "line": 96,
            "text": "    sidecar_records: Sequence[dict[str, Any]],"
          },
          {
            "line": 97,
            "text": ") -> list[dict[str, Any]]:"
          },
          {
            "line": 98,
            "text": "    \"\"\""
          },
          {
            "line": 99,
            "text": "    Align core daily returns to sidecar intervals by next_date."
          }
        ]
      },
      {
        "line": 171,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 166,
            "text": "        })"
          },
          {
            "line": 167,
            "text": ""
          },
          {
            "line": 168,
            "text": "    return aligned"
          },
          {
            "line": 169,
            "text": ""
          },
          {
            "line": 170,
            "text": ""
          },
          {
            "line": 171,
            "text": "def build_equity_records_from_returns("
          },
          {
            "line": 172,
            "text": "    interval_records: Sequence[dict[str, Any]],"
          },
          {
            "line": 173,
            "text": "    initial_equity: float,"
          },
          {
            "line": 174,
            "text": ") -> list[dict[str, Any]]:"
          },
          {
            "line": 175,
            "text": "    equity = initial_equity"
          },
          {
            "line": 176,
            "text": "    peak = initial_equity"
          }
        ]
      },
      {
        "line": 283,
        "matched": [
          "compose_e1r_v0_2_variant"
        ],
        "context": [
          {
            "line": 278,
            "text": "            for k, v in contribution_by_subclass.items()"
          },
          {
            "line": 279,
            "text": "        },"
          },
          {
            "line": 280,
            "text": "    }"
          },
          {
            "line": 281,
            "text": ""
          },
          {
            "line": 282,
            "text": ""
          },
          {
            "line": 283,
            "text": "def compose_e1r_v0_2_variant("
          },
          {
            "line": 284,
            "text": "    core_variant_result: dict[str, Any],"
          },
          {
            "line": 285,
            "text": "    sidecar_result: dict[str, Any],"
          },
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          }
        ]
      },
      {
        "line": 284,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 279,
            "text": "        },"
          },
          {
            "line": 280,
            "text": "    }"
          },
          {
            "line": 281,
            "text": ""
          },
          {
            "line": 282,
            "text": ""
          },
          {
            "line": 283,
            "text": "def compose_e1r_v0_2_variant("
          },
          {
            "line": 284,
            "text": "    core_variant_result: dict[str, Any],"
          },
          {
            "line": 285,
            "text": "    sidecar_result: dict[str, Any],"
          },
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          }
        ]
      },
      {
        "line": 285,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 280,
            "text": "    }"
          },
          {
            "line": 281,
            "text": ""
          },
          {
            "line": 282,
            "text": ""
          },
          {
            "line": 283,
            "text": "def compose_e1r_v0_2_variant("
          },
          {
            "line": 284,
            "text": "    core_variant_result: dict[str, Any],"
          },
          {
            "line": 285,
            "text": "    sidecar_result: dict[str, Any],"
          },
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          },
          {
            "line": 290,
            "text": ""
          }
        ]
      },
      {
        "line": 288,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 283,
            "text": "def compose_e1r_v0_2_variant("
          },
          {
            "line": 284,
            "text": "    core_variant_result: dict[str, Any],"
          },
          {
            "line": 285,
            "text": "    sidecar_result: dict[str, Any],"
          },
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          },
          {
            "line": 290,
            "text": ""
          },
          {
            "line": 291,
            "text": "    interval_records = extract_core_interval_returns(core_records, sidecar_records)"
          },
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          }
        ]
      },
      {
        "line": 289,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 284,
            "text": "    core_variant_result: dict[str, Any],"
          },
          {
            "line": 285,
            "text": "    sidecar_result: dict[str, Any],"
          },
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          },
          {
            "line": 290,
            "text": ""
          },
          {
            "line": 291,
            "text": "    interval_records = extract_core_interval_returns(core_records, sidecar_records)"
          },
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          },
          {
            "line": 294,
            "text": ""
          }
        ]
      },
      {
        "line": 291,
        "matched": [
          "extract_core_interval_returns"
        ],
        "context": [
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          },
          {
            "line": 290,
            "text": ""
          },
          {
            "line": 291,
            "text": "    interval_records = extract_core_interval_returns(core_records, sidecar_records)"
          },
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          },
          {
            "line": 294,
            "text": ""
          },
          {
            "line": 295,
            "text": "    result = copy.deepcopy(core_variant_result)"
          },
          {
            "line": 296,
            "text": ""
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
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          },
          {
            "line": 290,
            "text": ""
          },
          {
            "line": 291,
            "text": "    interval_records = extract_core_interval_returns(core_records, sidecar_records)"
          },
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          },
          {
            "line": 294,
            "text": ""
          },
          {
            "line": 295,
            "text": "    result = copy.deepcopy(core_variant_result)"
          },
          {
            "line": 296,
            "text": ""
          },
          {
            "line": 297,
            "text": "    sidecar_summary = sidecar_result.get(\"summary\", {}) or {}"
          }
        ]
      },
      {
        "line": 295,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 290,
            "text": ""
          },
          {
            "line": 291,
            "text": "    interval_records = extract_core_interval_returns(core_records, sidecar_records)"
          },
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          },
          {
            "line": 294,
            "text": ""
          },
          {
            "line": 295,
            "text": "    result = copy.deepcopy(core_variant_result)"
          },
          {
            "line": 296,
            "text": ""
          },
          {
            "line": 297,
            "text": "    sidecar_summary = sidecar_result.get(\"summary\", {}) or {}"
          },
          {
            "line": 298,
            "text": ""
          },
          {
            "line": 299,
            "text": "    result.update({"
          },
          {
            "line": 300,
            "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          }
        ]
      },
      {
        "line": 297,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          },
          {
            "line": 294,
            "text": ""
          },
          {
            "line": 295,
            "text": "    result = copy.deepcopy(core_variant_result)"
          },
          {
            "line": 296,
            "text": ""
          },
          {
            "line": 297,
            "text": "    sidecar_summary = sidecar_result.get(\"summary\", {}) or {}"
          },
          {
            "line": 298,
            "text": ""
          },
          {
            "line": 299,
            "text": "    result.update({"
          },
          {
            "line": 300,
            "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 301,
            "text": "        \"strategy_variant\": \"E1R_regime_aware_v0_2_formal_sidecar_sleeve\","
          },
          {
            "line": 302,
            "text": "        \"version\": \"E1R-v0.2-formal-sidecar-sleeve\","
          }
        ]
      },
      {
        "line": 300,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 295,
            "text": "    result = copy.deepcopy(core_variant_result)"
          },
          {
            "line": 296,
            "text": ""
          },
          {
            "line": 297,
            "text": "    sidecar_summary = sidecar_result.get(\"summary\", {}) or {}"
          },
          {
            "line": 298,
            "text": ""
          },
          {
            "line": 299,
            "text": "    result.update({"
          },
          {
            "line": 300,
            "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 301,
            "text": "        \"strategy_variant\": \"E1R_regime_aware_v0_2_formal_sidecar_sleeve\","
          },
          {
            "line": 302,
            "text": "        \"version\": \"E1R-v0.2-formal-sidecar-sleeve\","
          },
          {
            "line": 303,
            "text": "        \"research_status\": \"FORMAL_SIDECAR_SLEEVE_ENGINE\","
          },
          {
            "line": 304,
            "text": "        \"core_total_trades\": core_variant_result.get(\"total_trades\"),"
          },
          {
            "line": 305,
            "text": "        \"sidecar_trade_count_approx\": sidecar_summary.get(\"trade_count_approx\"),"
          }
        ]
      },
      {
        "line": 304,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 299,
            "text": "    result.update({"
          },
          {
            "line": 300,
            "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 301,
            "text": "        \"strategy_variant\": \"E1R_regime_aware_v0_2_formal_sidecar_sleeve\","
          },
          {
            "line": 302,
            "text": "        \"version\": \"E1R-v0.2-formal-sidecar-sleeve\","
          },
          {
            "line": 303,
            "text": "        \"research_status\": \"FORMAL_SIDECAR_SLEEVE_ENGINE\","
          },
          {
            "line": 304,
            "text": "        \"core_total_trades\": core_variant_result.get(\"total_trades\"),"
          },
          {
            "line": 305,
            "text": "        \"sidecar_trade_count_approx\": sidecar_summary.get(\"trade_count_approx\"),"
          },
          {
            "line": 306,
            "text": "        \"combined_trade_count_note\": ("
          },
          {
            "line": 307,
            "text": "            \"total_trades remains inherited from E1R v0.1 core; \""
          },
          {
            "line": 308,
            "text": "            \"sidecar_trade_count_approx counts daily basket holdings and is not \""
          },
          {
            "line": 309,
            "text": "            \"stateful round-trip trade count.\""
          }
        ]
      },
      {
        "line": 313,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 308,
            "text": "            \"sidecar_trade_count_approx counts daily basket holdings and is not \""
          },
          {
            "line": 309,
            "text": "            \"stateful round-trip trade count.\""
          },
          {
            "line": 310,
            "text": "        ),"
          },
          {
            "line": 311,
            "text": "        \"e1r_v0_2_composition\": {"
          },
          {
            "line": 312,
            "text": "            \"core_variant\": \"E1R_REGIME_AWARE_V0_1\","
          },
          {
            "line": 313,
            "text": "            \"sidecar_engine\": sidecar_result.get(\"engine\"),"
          },
          {
            "line": 314,
            "text": "            \"sidecar_version\": sidecar_result.get(\"version\"),"
          },
          {
            "line": 315,
            "text": "            \"alignment\": \"core daily return ending at next_date aligned to sidecar date->next_date interval\","
          },
          {
            "line": 316,
            "text": "            \"composition_formula\": \"(1 + core_return) * (1 + sidecar_return) - 1\","
          },
          {
            "line": 317,
            "text": "            \"sidecar_config\": sidecar_result.get(\"config\", {}),"
          },
          {
            "line": 318,
            "text": "            \"sidecar_sample\": sidecar_result.get(\"sample\", {}),"
          }
        ]
      },
      {
        "line": 314,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 309,
            "text": "            \"stateful round-trip trade count.\""
          },
          {
            "line": 310,
            "text": "        ),"
          },
          {
            "line": 311,
            "text": "        \"e1r_v0_2_composition\": {"
          },
          {
            "line": 312,
            "text": "            \"core_variant\": \"E1R_REGIME_AWARE_V0_1\","
          },
          {
            "line": 313,
            "text": "            \"sidecar_engine\": sidecar_result.get(\"engine\"),"
          },
          {
            "line": 314,
            "text": "            \"sidecar_version\": sidecar_result.get(\"version\"),"
          },
          {
            "line": 315,
            "text": "            \"alignment\": \"core daily return ending at next_date aligned to sidecar date->next_date interval\","
          },
          {
            "line": 316,
            "text": "            \"composition_formula\": \"(1 + core_return) * (1 + sidecar_return) - 1\","
          },
          {
            "line": 317,
            "text": "            \"sidecar_config\": sidecar_result.get(\"config\", {}),"
          },
          {
            "line": 318,
            "text": "            \"sidecar_sample\": sidecar_result.get(\"sample\", {}),"
          },
          {
            "line": 319,
            "text": "            \"sidecar_summary\": sidecar_result.get(\"summary\", {}),"
          }
        ]
      },
      {
        "line": 317,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 312,
            "text": "            \"core_variant\": \"E1R_REGIME_AWARE_V0_1\","
          },
          {
            "line": 313,
            "text": "            \"sidecar_engine\": sidecar_result.get(\"engine\"),"
          },
          {
            "line": 314,
            "text": "            \"sidecar_version\": sidecar_result.get(\"version\"),"
          },
          {
            "line": 315,
            "text": "            \"alignment\": \"core daily return ending at next_date aligned to sidecar date->next_date interval\","
          },
          {
            "line": 316,
            "text": "            \"composition_formula\": \"(1 + core_return) * (1 + sidecar_return) - 1\","
          },
          {
            "line": 317,
            "text": "            \"sidecar_config\": sidecar_result.get(\"config\", {}),"
          },
          {
            "line": 318,
            "text": "            \"sidecar_sample\": sidecar_result.get(\"sample\", {}),"
          },
          {
            "line": 319,
            "text": "            \"sidecar_summary\": sidecar_result.get(\"summary\", {}),"
          },
          {
            "line": 320,
            "text": "            \"combined_summary\": summary,"
          },
          {
            "line": 321,
            "text": "        },"
          },
          {
            "line": 322,
            "text": "        \"daily_equity_records\": equity_records,"
          }
        ]
      },
      {
        "line": 318,
        "matched": [
   
```

## Top Grep Hits

```json
[
  {
    "path": "src/engine/e1r_composer.py",
    "score": 803,
    "hit_count": 23,
    "hits": [
      {
        "line": 9,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 4,
            "text": "Composes:"
          },
          {
            "line": 5,
            "text": "- E1R_REGIME_AWARE_V0_1 core daily equity records"
          },
          {
            "line": 6,
            "text": "- E1R sidecar sleeve daily return records"
          },
          {
            "line": 7,
            "text": ""
          },
          {
            "line": 8,
            "text": "into:"
          },
          {
            "line": 9,
            "text": "- E1R_REGIME_AWARE_V0_2 formal combined daily equity records"
          },
          {
            "line": 10,
            "text": ""
          },
          {
            "line": 11,
            "text": "Alignment rule"
          },
          {
            "line": 12,
            "text": "--------------"
          },
          {
            "line": 13,
            "text": "Core daily equity record date means:"
          },
          {
            "line": 14,
            "text": "    previous trading day close -> date close"
          }
        ]
      },
      {
        "line": 94,
        "matched": [
          "extract_core_interval_returns"
        ],
        "context": [
          {
            "line": 89,
            "text": "        return float(\"inf\")"
          },
          {
            "line": 90,
            "text": ""
          },
          {
            "line": 91,
            "text": "    return gains / losses"
          },
          {
            "line": 92,
            "text": ""
          },
          {
            "line": 93,
            "text": ""
          },
          {
            "line": 94,
            "text": "def extract_core_interval_returns("
          },
          {
            "line": 95,
            "text": "    core_daily_equity_records: Sequence[dict[str, Any]],"
          },
          {
            "line": 96,
            "text": "    sidecar_records: Sequence[dict[str, Any]],"
          },
          {
            "line": 97,
            "text": ") -> list[dict[str, Any]]:"
          },
          {
            "line": 98,
            "text": "    \"\"\""
          },
          {
            "line": 99,
            "text": "    Align core daily returns to sidecar intervals by next_date."
          }
        ]
      },
      {
        "line": 171,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 166,
            "text": "        })"
          },
          {
            "line": 167,
            "text": ""
          },
          {
            "line": 168,
            "text": "    return aligned"
          },
          {
            "line": 169,
            "text": ""
          },
          {
            "line": 170,
            "text": ""
          },
          {
            "line": 171,
            "text": "def build_equity_records_from_returns("
          },
          {
            "line": 172,
            "text": "    interval_records: Sequence[dict[str, Any]],"
          },
          {
            "line": 173,
            "text": "    initial_equity: float,"
          },
          {
            "line": 174,
            "text": ") -> list[dict[str, Any]]:"
          },
          {
            "line": 175,
            "text": "    equity = initial_equity"
          },
          {
            "line": 176,
            "text": "    peak = initial_equity"
          }
        ]
      },
      {
        "line": 283,
        "matched": [
          "compose_e1r_v0_2_variant"
        ],
        "context": [
          {
            "line": 278,
            "text": "            for k, v in contribution_by_subclass.items()"
          },
          {
            "line": 279,
            "text": "        },"
          },
          {
            "line": 280,
            "text": "    }"
          },
          {
            "line": 281,
            "text": ""
          },
          {
            "line": 282,
            "text": ""
          },
          {
            "line": 283,
            "text": "def compose_e1r_v0_2_variant("
          },
          {
            "line": 284,
            "text": "    core_variant_result: dict[str, Any],"
          },
          {
            "line": 285,
            "text": "    sidecar_result: dict[str, Any],"
          },
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          }
        ]
      },
      {
        "line": 284,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 279,
            "text": "        },"
          },
          {
            "line": 280,
            "text": "    }"
          },
          {
            "line": 281,
            "text": ""
          },
          {
            "line": 282,
            "text": ""
          },
          {
            "line": 283,
            "text": "def compose_e1r_v0_2_variant("
          },
          {
            "line": 284,
            "text": "    core_variant_result: dict[str, Any],"
          },
          {
            "line": 285,
            "text": "    sidecar_result: dict[str, Any],"
          },
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          }
        ]
      },
      {
        "line": 285,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 280,
            "text": "    }"
          },
          {
            "line": 281,
            "text": ""
          },
          {
            "line": 282,
            "text": ""
          },
          {
            "line": 283,
            "text": "def compose_e1r_v0_2_variant("
          },
          {
            "line": 284,
            "text": "    core_variant_result: dict[str, Any],"
          },
          {
            "line": 285,
            "text": "    sidecar_result: dict[str, Any],"
          },
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          },
          {
            "line": 290,
            "text": ""
          }
        ]
      },
      {
        "line": 288,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 283,
            "text": "def compose_e1r_v0_2_variant("
          },
          {
            "line": 284,
            "text": "    core_variant_result: dict[str, Any],"
          },
          {
            "line": 285,
            "text": "    sidecar_result: dict[str, Any],"
          },
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          },
          {
            "line": 290,
            "text": ""
          },
          {
            "line": 291,
            "text": "    interval_records = extract_core_interval_returns(core_records, sidecar_records)"
          },
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          }
        ]
      },
      {
        "line": 289,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 284,
            "text": "    core_variant_result: dict[str, Any],"
          },
          {
            "line": 285,
            "text": "    sidecar_result: dict[str, Any],"
          },
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          },
          {
            "line": 290,
            "text": ""
          },
          {
            "line": 291,
            "text": "    interval_records = extract_core_interval_returns(core_records, sidecar_records)"
          },
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          },
          {
            "line": 294,
            "text": ""
          }
        ]
      },
      {
        "line": 291,
        "matched": [
          "extract_core_interval_returns"
        ],
        "context": [
          {
            "line": 286,
            "text": "    initial_equity: float = 100000.0,"
          },
          {
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          },
          {
            "line": 290,
            "text": ""
          },
          {
            "line": 291,
            "text": "    interval_records = extract_core_interval_returns(core_records, sidecar_records)"
          },
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          },
          {
            "line": 294,
            "text": ""
          },
          {
            "line": 295,
            "text": "    result = copy.deepcopy(core_variant_result)"
          },
          {
            "line": 296,
            "text": ""
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
            "line": 287,
            "text": ") -> dict[str, Any]:"
          },
          {
            "line": 288,
            "text": "    core_records = core_variant_result.get(\"daily_equity_records\", [])"
          },
          {
            "line": 289,
            "text": "    sidecar_records = sidecar_result.get(\"records\", [])"
          },
          {
            "line": 290,
            "text": ""
          },
          {
            "line": 291,
            "text": "    interval_records = extract_core_interval_returns(core_records, sidecar_records)"
          },
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          },
          {
            "line": 294,
            "text": ""
          },
          {
            "line": 295,
            "text": "    result = copy.deepcopy(core_variant_result)"
          },
          {
            "line": 296,
            "text": ""
          },
          {
            "line": 297,
            "text": "    sidecar_summary = sidecar_result.get(\"summary\", {}) or {}"
          }
        ]
      },
      {
        "line": 295,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 290,
            "text": ""
          },
          {
            "line": 291,
            "text": "    interval_records = extract_core_interval_returns(core_records, sidecar_records)"
          },
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          },
          {
            "line": 294,
            "text": ""
          },
          {
            "line": 295,
            "text": "    result = copy.deepcopy(core_variant_result)"
          },
          {
            "line": 296,
            "text": ""
          },
          {
            "line": 297,
            "text": "    sidecar_summary = sidecar_result.get(\"summary\", {}) or {}"
          },
          {
            "line": 298,
            "text": ""
          },
          {
            "line": 299,
            "text": "    result.update({"
          },
          {
            "line": 300,
            "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          }
        ]
      },
      {
        "line": 297,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 292,
            "text": "    equity_records = build_equity_records_from_returns(interval_records, initial_equity)"
          },
          {
            "line": 293,
            "text": "    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)"
          },
          {
            "line": 294,
            "text": ""
          },
          {
            "line": 295,
            "text": "    result = copy.deepcopy(core_variant_result)"
          },
          {
            "line": 296,
            "text": ""
          },
          {
            "line": 297,
            "text": "    sidecar_summary = sidecar_result.get(\"summary\", {}) or {}"
          },
          {
            "line": 298,
            "text": ""
          },
          {
            "line": 299,
            "text": "    result.update({"
          },
          {
            "line": 300,
            "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 301,
            "text": "        \"strategy_variant\": \"E1R_regime_aware_v0_2_formal_sidecar_sleeve\","
          },
          {
            "line": 302,
            "text": "        \"version\": \"E1R-v0.2-formal-sidecar-sleeve\","
          }
        ]
      },
      {
        "line": 300,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 295,
            "text": "    result = copy.deepcopy(core_variant_result)"
          },
          {
            "line": 296,
            "text": ""
          },
          {
            "line": 297,
            "text": "    sidecar_summary = sidecar_result.get(\"summary\", {}) or {}"
          },
          {
            "line": 298,
            "text": ""
          },
          {
            "line": 299,
            "text": "    result.update({"
          },
          {
            "line": 300,
            "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 301,
            "text": "        \"strategy_variant\": \"E1R_regime_aware_v0_2_formal_sidecar_sleeve\","
          },
          {
            "line": 302,
            "text": "        \"version\": \"E1R-v0.2-formal-sidecar-sleeve\","
          },
          {
            "line": 303,
            "text": "        \"research_status\": \"FORMAL_SIDECAR_SLEEVE_ENGINE\","
          },
          {
            "line": 304,
            "text": "        \"core_total_trades\": core_variant_result.get(\"total_trades\"),"
          },
          {
            "line": 305,
            "text": "        \"sidecar_trade_count_approx\": sidecar_summary.get(\"trade_count_approx\"),"
          }
        ]
      },
      {
        "line": 304,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 299,
            "text": "    result.update({"
          },
          {
            "line": 300,
            "text": "        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 301,
            "text": "        \"strategy_variant\": \"E1R_regime_aware_v0_2_formal_sidecar_sleeve\","
          },
          {
            "line": 302,
            "text": "        \"version\": \"E1R-v0.2-formal-sidecar-sleeve\","
          },
          {
            "line": 303,
            "text": "        \"research_status\": \"FORMAL_SIDECAR_SLEEVE_ENGINE\","
          },
          {
            "line": 304,
            "text": "        \"core_total_trades\": core_variant_result.get(\"total_trades\"),"
          },
          {
            "line": 305,
            "text": "        \"sidecar_trade_count_approx\": sidecar_summary.get(\"trade_count_approx\"),"
          },
          {
            "line": 306,
            "text": "        \"combined_trade_count_note\": ("
          },
          {
            "line": 307,
            "text": "            \"total_trades remains inherited from E1R v0.1 core; \""
          },
          {
            "line": 308,
            "text": "            \"sidecar_trade_count_approx counts daily basket holdings and is not \""
          },
          {
            "line": 309,
            "text": "            \"stateful round-trip trade count.\""
          }
        ]
      },
      {
        "line": 313,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 308,
            "text": "            \"sidecar_trade_count_approx counts daily basket holdings and is not \""
          },
          {
            "line": 309,
            "text": "            \"stateful round-trip trade count.\""
          },
          {
            "line": 310,
            "text": "        ),"
          },
          {
            "line": 311,
            "text": "        \"e1r_v0_2_composition\": {"
          },
          {
            "line": 312,
            "text": "            \"core_variant\": \"E1R_REGIME_AWARE_V0_1\","
          },
          {
            "line": 313,
            "text": "            \"sidecar_engine\": sidecar_result.get(\"engine\"),"
          },
          {
            "line": 314,
            "text": "            \"sidecar_version\": sidecar_result.get(\"version\"),"
          },
          {
            "line": 315,
            "text": "            \"alignment\": \"core daily return ending at next_date aligned to sidecar date->next_date interval\","
          },
          {
            "line": 316,
            "text": "            \"composition_formula\": \"(1 + core_return) * (1 + sidecar_return) - 1\","
          },
          {
            "line": 317,
            "text": "            \"sidecar_config\": sidecar_result.get(\"config\", {}),"
          },
          {
            "line": 318,
            "text": "            \"sidecar_sample\": sidecar_result.get(\"sample\", {}),"
          }
        ]
      },
      {
        "line": 314,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 309,
            "text": "            \"stateful round-trip trade count.\""
          },
          {
            "line": 310,
            "text": "        ),"
          },
          {
            "line": 311,
            "text": "        \"e1r_v0_2_composition\": {"
          },
          {
            "line": 312,
            "text": "            \"core_variant\": \"E1R_REGIME_AWARE_V0_1\","
          },
          {
            "line": 313,
            "text": "            \"sidecar_engine\": sidecar_result.get(\"engine\"),"
          },
          {
            "line": 314,
            "text": "            \"sidecar_version\": sidecar_result.get(\"version\"),"
          },
          {
            "line": 315,
            "text": "            \"alignment\": \"core daily return ending at next_date aligned to sidecar date->next_date interval\","
          },
          {
            "line": 316,
            "text": "            \"composition_formula\": \"(1 + core_return) * (1 + sidecar_return) - 1\","
          },
          {
            "line": 317,
            "text": "            \"sidecar_config\": sidecar_result.get(\"config\", {}),"
          },
          {
            "line": 318,
            "text": "            \"sidecar_sample\": sidecar_result.get(\"sample\", {}),"
          },
          {
            "line": 319,
            "text": "            \"sidecar_summary\": sidecar_result.get(\"summary\", {}),"
          }
        ]
      },
      {
        "line": 317,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 312,
            "text": "            \"core_variant\": \"E1R_REGIME_AWARE_V0_1\","
          },
          {
            "line": 313,
            "text": "            \"sidecar_engine\": sidecar_result.get(\"engine\"),"
          },
          {
            "line": 314,
            "text": "            \"sidecar_version\": sidecar_result.get(\"version\"),"
          },
          {
            "line": 315,
            "text": "            \"alignment\": \"core daily return ending at next_date aligned to sidecar date->next_date interval\","
          },
          {
            "line": 316,
            "text": "            \"composition_formula\": \"(1 + core_return) * (1 + sidecar_return) - 1\","
          },
          {
            "line": 317,
            "text": "            \"sidecar_config\": sidecar_result.get(\"config\", {}),"
          },
          {
            "line": 318,
            "text": "            \"sidecar_sample\": sidecar_result.get(\"sample\", {}),"
          },
          {
            "line": 319,
            "text": "            \"sidecar_summary\": sidecar_result.get(\"summary\", {}),"
          },
          {
            "line": 320,
            "text": "            \"combined_summary\": summary,"
          },
          {
            "line": 321,
            "text": "        },"
          },
          {
            "line": 322,
            "text": "        \"daily_equity_records\": equity_records,"
          }
        ]
      },
      {
        "line": 318,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 313,
            "text": "            \"sidecar_engine\": sidecar_result.get(\"engine\"),"
          },
          {
            "line": 314,
            "text": "            \"sidecar_version\": sidecar_result.get(\"version\"),"
          },
          {
            "line": 315,
            "text": "            \"alignment\": \"core daily return ending at next_date aligned to sidecar date->next_date interval\","
          },
          {
            "line": 316,
            "text": "            \"composition_formula\": \"(1 + core_return) * (1 + sidecar_return) - 1\","
          },
          {
            "line": 317,
            "text": "            \"sidecar_config\": sidecar_result.get(\"config\", {}),"
          },
          {
            "line": 318,
            "text": "            \"sidecar_sample\": sidecar_result.get(\"sample\", {}),"
          },
          {
            "line": 319,
            "text": "            \"sidecar_summary\": sidecar_result.get(\"summary\", {}),"
          },
          {
            "line": 320,
            "text": "            \"combined_summary\": summary,"
          },
          {
            "line": 321,
            "text": "        },"
          },
          {
            "line": 322,
            "text": "        \"daily_equity_records\": equity_records,"
          },
          {
            "line": 323,
            "text": "        \"daily_equity_record_count\": len(equity_records),"
          }
        ]
      },
      {
        "line": 319,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 314,
            "text": "            \"sidecar_version\": sidecar_result.get(\"version\"),"
          },
          {
            "line": 315,
            "text": "            \"alignment\": \"core daily return ending at next_date aligned to sidecar date->next_date interval\","
          },
          {
            "line": 316,
            "text": "            \"composition_formula\": \"(1 + core_return) * (1 + sidecar_return) - 1\","
          },
          {
            "line": 317,
            "text": "            \"sidecar_config\": sidecar_result.get(\"config\", {}),"
          },
          {
            "line": 318,
            "text": "            \"sidecar_sample\": sidecar_result.get(\"sample\", {}),"
          },
          {
            "line": 319,
            "text": "            \"sidecar_summary\": sidecar_result.get(\"summary\", {}),"
          },
          {
            "line": 320,
            "text": "            \"combined_summary\": summary,"
          },
          {
            "line": 321,
            "text": "        },"
          },
          {
            "line": 322,
            "text": "        \"daily_equity_records\": equity_records,"
          },
          {
            "line": 323,
            "text": "        \"daily_equity_record_count\": len(equity_records),"
          },
          {
            "line": 324,
            "text": "        \"e1r_v0_2_interval_records_sample\": {"
          }
        ]
      },
      {
        "line": 354,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 349,
            "text": "    result.setdefault(\"strategy_controls\", {})"
          },
          {
            "line": 350,
            "text": "    result[\"strategy_controls\"].update({"
          },
          {
            "line": 351,
            "text": "        \"regime_aware_logic\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
          },
          {
            "line": 352,
            "text": "        \"e1r_v0_2_formal_sidecar_sleeve\": True,"
          },
          {
            "line": 353,
            "text": "        \"e1r_v0_2_core_variant\": \"E1R_REGIME_AWARE_V0_1\","
          },
          {
            "line": 354,
            "text":
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-4B-0L`: Instrument true source path or reconstruct noncanonical E1R composition
- Recommended action: Instrument the top true direct composer callsite in no-write mode.

