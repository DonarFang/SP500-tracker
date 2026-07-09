# Stage 3.8E-2F-2C-4C-10F-4B-0J Composer Callsite Instrumentation

Generated At: `2026-07-09T10:43:46.871371+00:00`

## Status

- Status: `E1R_COMPOSER_CALLSITE_INSTRUMENTATION_COMPLETE_OUTPUTS_RESTORED`
- E1R canonical written: `False`
- Candidate extracted: `False`
- Strategy files unchanged: `True`
- Canonical existence unchanged after restore: `True`

## Summary

```json
{
  "wrapped_call_count": 0,
  "direct_callsite_candidate_count": 7,
  "generator_run_ok": true,
  "generator_elapsed_seconds": 0.06775188446044922,
  "patched_modules": [
    "engine.e1r_composer",
    "src.engine.e1r_composer"
  ],
  "patch_errors": []
}
```

## Conclusion

- `COMPOSER_CALLSITE_FOUND_IN_SOURCE_BUT_NOT_TRIGGERED_BY_GENERATOR`
- Recommended: Instrument the highest source callsite directly instead of export_canonical_5y_equity_curves.py.

## Wrapped Calls

```json
[]
```

## Direct Callsite Candidates

```json
[
  {
    "path": "scripts/audit_e1r_generator_composer_contract_4b0g.py",
    "score": 379,
    "hit_count": 37,
    "hits": [
      {
        "line": 41,
        "matched": [
          "compose_e1r_v0_2_variant"
        ],
        "context": [
          {
            "line": 37,
            "text": "    BACKTEST,"
          },
          {
            "line": 38,
            "text": "]"
          },
          {
            "line": 39,
            "text": ""
          },
          {
            "line": 40,
            "text": "TARGET_NAMES = ["
          },
          {
            "line": 41,
            "text": "    \"compose_e1r_v0_2_variant\","
          },
          {
            "line": 42,
            "text": "    \"core_variant_result\","
          },
          {
            "line": 43,
            "text": "    \"sidecar_result\","
          },
          {
            "line": 44,
            "text": "    \"daily_equity_records\","
          },
          {
            "line": 45,
            "text": "    \"daily_records\","
          }
        ]
      },
      {
        "line": 42,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 38,
            "text": "]"
          },
          {
            "line": 39,
            "text": ""
          },
          {
            "line": 40,
            "text": "TARGET_NAMES = ["
          },
          {
            "line": 41,
            "text": "    \"compose_e1r_v0_2_variant\","
          },
          {
            "line": 42,
            "text": "    \"core_variant_result\","
          },
          {
            "line": 43,
            "text": "    \"sidecar_result\","
          },
          {
            "line": 44,
            "text": "    \"daily_equity_records\","
          },
          {
            "line": 45,
            "text": "    \"daily_records\","
          },
          {
            "line": 46,
            "text": "    \"equity_curve\","
          }
        ]
      },
      {
        "line": 43,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 39,
            "text": ""
          },
          {
            "line": 40,
            "text": "TARGET_NAMES = ["
          },
          {
            "line": 41,
            "text": "    \"compose_e1r_v0_2_variant\","
          },
          {
            "line": 42,
            "text": "    \"core_variant_result\","
          },
          {
            "line": 43,
            "text": "    \"sidecar_result\","
          },
          {
            "line": 44,
            "text": "    \"daily_equity_records\","
          },
          {
            "line": 45,
            "text": "    \"daily_records\","
          },
          {
            "line": 46,
            "text": "    \"equity_curve\","
          },
          {
            "line": 47,
            "text": "    \"variant_results\","
          }
        ]
      },
      {
        "line": 44,
        "matched": [
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 40,
            "text": "TARGET_NAMES = ["
          },
          {
            "line": 41,
            "text": "    \"compose_e1r_v0_2_variant\","
          },
          {
            "line": 42,
            "text": "    \"core_variant_result\","
          },
          {
            "line": 43,
            "text": "    \"sidecar_result\","
          },
          {
            "line": 44,
            "text": "    \"daily_equity_records\","
          },
          {
            "line": 45,
            "text": "    \"daily_records\","
          },
          {
            "line": 46,
            "text": "    \"equity_curve\","
          },
          {
            "line": 47,
            "text": "    \"variant_results\","
          },
          {
            "line": 48,
            "text": "    \"build_equity_records_from_returns\","
          }
        ]
      },
      {
        "line": 48,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 44,
            "text": "    \"daily_equity_records\","
          },
          {
            "line": 45,
            "text": "    \"daily_records\","
          },
          {
            "line": 46,
            "text": "    \"equity_curve\","
          },
          {
            "line": 47,
            "text": "    \"variant_results\","
          },
          {
            "line": 48,
            "text": "    \"build_equity_records_from_returns\","
          },
          {
            "line": 49,
            "text": "    \"extract_core_interval_returns\","
          },
          {
            "line": 50,
            "text": "    \"build_e1r_sidecar_sleeve\","
          },
          {
            "line": 51,
            "text": "    \"run_strategy_variant_comparison\","
          },
          {
            "line": 52,
            "text": "    \"run_stateful_simulation\","
          }
        ]
      },
      {
        "line": 49,
        "matched": [
          "extract_core_interval_returns"
        ],
        "context": [
          {
            "line": 45,
            "text": "    \"daily_records\","
          },
          {
            "line": 46,
            "text": "    \"equity_curve\","
          },
          {
            "line": 47,
            "text": "    \"variant_results\","
          },
          {
            "line": 48,
            "text": "    \"build_equity_records_from_returns\","
          },
          {
            "line": 49,
            "text": "    \"extract_core_interval_returns\","
          },
          {
            "line": 50,
            "text": "    \"build_e1r_sidecar_sleeve\","
          },
          {
            "line": 51,
            "text": "    \"run_strategy_variant_comparison\","
          },
          {
            "line": 52,
            "text": "    \"run_stateful_simulation\","
          },
          {
            "line": 53,
            "text": "    \"e1r_v0_2_backtest_summary.json\","
          }
        ]
      },
      {
        "line": 51,
        "matched": [
          "run_strategy_variant_comparison"
        ],
        "context": [
          {
            "line": 47,
            "text": "    \"variant_results\","
          },
          {
            "line": 48,
            "text": "    \"build_equity_records_from_returns\","
          },
          {
            "line": 49,
            "text": "    \"extract_core_interval_returns\","
          },
          {
            "line": 50,
            "text": "    \"build_e1r_sidecar_sleeve\","
          },
          {
            "line": 51,
            "text": "    \"run_strategy_variant_comparison\","
          },
          {
            "line": 52,
            "text": "    \"run_stateful_simulation\","
          },
          {
            "line": 53,
            "text": "    \"e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 54,
            "text": "    \"e1r_v0_2_backtest_equity_curve.json\","
          },
          {
            "line": 55,
            "text": "    \"E1R_REGIME_AWARE_V0_2\","
          }
        ]
      },
      {
        "line": 52,
        "matched": [
          "run_stateful_simulation"
        ],
        "context": [
          {
            "line": 48,
            "text": "    \"build_equity_records_from_returns\","
          },
          {
            "line": 49,
            "text": "    \"extract_core_interval_returns\","
          },
          {
            "line": 50,
            "text": "    \"build_e1r_sidecar_sleeve\","
          },
          {
            "line": 51,
            "text": "    \"run_strategy_variant_comparison\","
          },
          {
            "line": 52,
            "text": "    \"run_stateful_simulation\","
          },
          {
            "line": 53,
            "text": "    \"e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 54,
            "text": "    \"e1r_v0_2_backtest_equity_curve.json\","
          },
          {
            "line": 55,
            "text": "    \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 56,
            "text": "]"
          }
        ]
      },
      {
        "line": 53,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "context": [
          {
            "line": 49,
            "text": "    \"extract_core_interval_returns\","
          },
          {
            "line": 50,
            "text": "    \"build_e1r_sidecar_sleeve\","
          },
          {
            "line": 51,
            "text": "    \"run_strategy_variant_comparison\","
          },
          {
            "line": 52,
            "text": "    \"run_stateful_simulation\","
          },
          {
            "line": 53,
            "text": "    \"e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 54,
            "text": "    \"e1r_v0_2_backtest_equity_curve.json\","
          },
          {
            "line": 55,
            "text": "    \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 56,
            "text": "]"
          },
          {
            "line": 57,
            "text": ""
          }
        ]
      },
      {
        "line": 54,
        "matched": [
          "e1r_v0_2_backtest_equity_curve.json"
        ],
        "context": [
          {
            "line": 50,
            "text": "    \"build_e1r_sidecar_sleeve\","
          },
          {
            "line": 51,
            "text": "    \"run_strategy_variant_comparison\","
          },
          {
            "line": 52,
            "text": "    \"run_stateful_simulation\","
          },
          {
            "line": 53,
            "text": "    \"e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 54,
            "text": "    \"e1r_v0_2_backtest_equity_curve.json\","
          },
          {
            "line": 55,
            "text": "    \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 56,
            "text": "]"
          },
          {
            "line": 57,
            "text": ""
          },
          {
            "line": 58,
            "text": "def now() -> str:"
          }
        ]
      },
      {
        "line": 55,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 51,
            "text": "    \"run_strategy_variant_comparison\","
          },
          {
            "line": 52,
            "text": "    \"run_stateful_simulation\","
          },
          {
            "line": 53,
            "text": "    \"e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 54,
            "text": "    \"e1r_v0_2_backtest_equity_curve.json\","
          },
          {
            "line": 55,
            "text": "    \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 56,
            "text": "]"
          },
          {
            "line": 57,
            "text": ""
          },
          {
            "line": 58,
            "text": "def now() -> str:"
          },
          {
            "line": 59,
            "text": "    return datetime.now(timezone.utc).isoformat()"
          }
        ]
      },
      {
        "line": 267,
        "matched": [
          "compose_e1r_v0_2_variant"
        ],
        "context": [
          {
            "line": 263,
            "text": ""
          },
          {
            "line": 264,
            "text": "    generator_text = read_text(GENERATOR) if GENERATOR.exists() else \"\""
          },
          {
            "line": 265,
            "text": "    composer_text = read_text(COMPOSER) if COMPOSER.exists() else \"\""
          },
          {
            "line": 266,
            "text": ""
          },
          {
            "line": 267,
            "text": "    has_compose_call_in_generator = \"compose_e1r_v0_2_variant\" in generator_text"
          },
          {
            "line": 268,
            "text": "    has_core_var_in_generator = \"core_variant_result\" in generator_text"
          },
          {
            "line": 269,
            "text": "    has_sidecar_var_in_generator = \"sidecar_result\" in generator_text"
          },
          {
            "line": 270,
            "text": "    has_daily_in_generator = (\"daily_equity_records\" in generator_text) or (\"daily_records\" in generator_text) or (\"equity_curve\" in generator_text)"
          },
          {
            "line": 271,
            "text": ""
          }
        ]
      },
      {
        "line": 268,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 264,
            "text": "    generator_text = read_text(GENERATOR) if GENERATOR.exists() else \"\""
          },
          {
            "line": 265,
            "text": "    composer_text = read_text(COMPOSER) if COMPOSER.exists() else \"\""
          },
          {
            "line": 266,
            "text": ""
          },
          {
            "line": 267,
            "text": "    has_compose_call_in_generator = \"compose_e1r_v0_2_variant\" in generator_text"
          },
          {
            "line": 268,
            "text": "    has_core_var_in_generator = \"core_variant_result\" in generator_text"
          },
          {
            "line": 269,
            "text": "    has_sidecar_var_in_generator = \"sidecar_result\" in generator_text"
          },
          {
            "line": 270,
            "text": "    has_daily_in_generator = (\"daily_equity_records\" in generator_text) or (\"daily_records\" in generator_text) or (\"equity_curve\" in generator_text)"
          },
          {
            "line": 271,
            "text": ""
          },
          {
            "line": 272,
            "text": "    has_compose_def = \"def compose_e1r_v0_2_variant\" in composer_text"
          }
        ]
      },
      {
        "line": 269,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 265,
            "text": "    composer_text = read_text(COMPOSER) if COMPOSER.exists() else \"\""
          },
          {
            "line": 266,
            "text": ""
          },
          {
            "line": 267,
            "text": "    has_compose_call_in_generator = \"compose_e1r_v0_2_variant\" in generator_text"
          },
          {
            "line": 268,
            "text": "    has_core_var_in_generator = \"core_variant_result\" in generator_text"
          },
          {
            "line": 269,
            "text": "    has_sidecar_var_in_generator = \"sidecar_result\" in generator_text"
          },
          {
            "line": 270,
            "text": "    has_daily_in_generator = (\"daily_equity_records\" in generator_text) or (\"daily_records\" in generator_text) or (\"equity_curve\" in generator_text)"
          },
          {
            "line": 271,
            "text": ""
          },
          {
            "line": 272,
            "text": "    has_compose_def = \"def compose_e1r_v0_2_variant\" in composer_text"
          },
          {
            "line": 273,
            "text": "    compose_mentions_core = \"core_variant_result\" in composer_text"
          }
        ]
      },
      {
        "line": 270,
        "matched": [
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 266,
            "text": ""
          },
          {
            "line": 267,
            "text": "    has_compose_call_in_generator = \"compose_e1r_v0_2_variant\" in generator_text"
          },
          {
            "line": 268,
            "text": "    has_core_var_in_generator = \"core_variant_result\" in generator_text"
          },
          {
            "line": 269,
            "text": "    has_sidecar_var_in_generator = \"sidecar_result\" in generator_text"
          },
          {
            "line": 270,
            "text": "    has_daily_in_generator = (\"daily_equity_records\" in generator_text) or (\"daily_records\" in generator_text) or (\"equity_curve\" in generator_text)"
          },
          {
            "line": 271,
            "text": ""
          },
          {
            "line": 272,
            "text": "    has_compose_def = \"def compose_e1r_v0_2_variant\" in composer_text"
          },
          {
            "line": 273,
            "text": "    compose_mentions_core = \"core_variant_result\" in composer_text"
          },
          {
            "line": 274,
            "text": "    compose_mentions_sidecar = \"sidecar_result\" in composer_text"
          }
        ]
      },
      {
        "line": 272,
        "matched": [
          "compose_e1r_v0_2_variant"
        ],
        "context": [
          {
            "line": 268,
            "text": "    has_core_var_in_generator = \"core_variant_result\" in generator_text"
          },
          {
            "line": 269,
            "text": "    has_sidecar_var_in_generator = \"sidecar_result\" in generator_text"
          },
          {
            "line": 270,
            "text": "    has_daily_in_generator = (\"daily_equity_records\" in generator_text) or (\"daily_records\" in generator_text) or (\"equity_curve\" in generator_text)"
          },
          {
            "line": 271,
            "text": ""
          },
          {
            "line": 272,
            "text": "    has_compose_def = \"def compose_e1r_v0_2_variant\" in composer_text"
          },
          {
            "line": 273,
            "text": "    compose_mentions_core = \"core_variant_result\" in composer_text"
          },
          {
            "line": 274,
            "text": "    compose_mentions_sidecar = \"sidecar_result\" in composer_text"
          },
          {
            "line": 275,
            "text": "    compose_mentions_daily = (\"daily_equity_records\" in composer_text) or (\"daily_records\" in composer_text) or (\"equity_curve\" in composer_text)"
          },
          {
            "line": 276,
            "text": ""
          }
        ]
      },
      {
        "line": 273,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 269,
            "text": "    has_sidecar_var_in_generator = \"sidecar_result\" in generator_text"
          },
          {
            "line": 270,
            "text": "    has_daily_in_generator = (\"daily_equity_records\" in generator_text) or (\"daily_records\" in generator_text) or (\"equity_curve\" in generator_text)"
          },
          {
            "line": 271,
            "text": ""
          },
          {
            "line": 272,
            "text": "    has_compose_def = \"def compose_e1r_v0_2_variant\" in composer_text"
          },
          {
            "line": 273,
            "text": "    compose_mentions_core = \"core_variant_result\" in composer_text"
          },
          {
            "line": 274,
            "text": "    compose_mentions_sidecar = \"sidecar_result\" in composer_text"
          },
          {
            "line": 275,
            "text": "    compose_mentions_daily = (\"daily_equity_records\" in composer_text) or (\"daily_records\" in composer_text) or (\"equity_curve\" in composer_text)"
          },
          {
            "line": 276,
            "text": ""
          },
          {
            "line": 277,
            "text": "    if has_compose_call_in_generator:"
          }
        ]
      },
      {
        "line": 274,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 270,
            "text": "    has_daily_in_generator = (\"daily_equity_records\" in generator_text) or (\"daily_records\" in generator_text) or (\"equity_curve\" in generator_text)"
          },
          {
            "line": 271,
            "text": ""
          },
          {
            "line": 272,
            "text": "    has_compose_def = \"def compose_e1r_v0_2_variant\" in composer_text"
          },
          {
            "line": 273,
            "text": "    compose_mentions_core = \"core_variant_result\" in composer_text"
          },
          {
            "line": 274,
            "text": "    compose_mentions_sidecar = \"sidecar_result\" in composer_text"
          },
          {
            "line": 275,
            "text": "    compose_mentions_daily = (\"daily_equity_records\" in composer_text) or (\"daily_records\" in composer_text) or (\"equity_curve\" in composer_text)"
          },
          {
            "line": 276,
            "text": ""
          },
          {
            "line": 277,
            "text": "    if has_compose_call_in_generator:"
          },
          {
            "line": 278,
            "text": "        findings.append(\"Generator references compose_e1r_v0_2_variant.\")"
          }
        ]
      },
      {
        "line": 275,
        "matched": [
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 271,
            "text": ""
          },
          {
            "line": 272,
            "text": "    has_compose_def = \"def compose_e1r_v0_2_variant\" in composer_text"
          },
          {
            "line": 273,
            "text": "    compose_mentions_core = \"core_variant_result\" in composer_text"
          },
          {
            "line": 274,
            "text": "    compose_mentions_sidecar = \"sidecar_result\" in composer_text"
          },
          {
            "line": 275,
            "text": "    compose_mentions_daily = (\"daily_equity_records\" in composer_text) or (\"daily_records\" in composer_text) or (\"equity_curve\" in composer_text)"
          },
          {
            "line": 276,
            "text": ""
          },
          {
            "line": 277,
            "text": "    if has_compose_call_in_generator:"
          },
          {
            "line": 278,
            "text": "        findings.append(\"Generator references compose_e1r_v0_2_variant.\")"
          },
          {
            "line": 279,
            "text": "    else:"
          }
        ]
      },
      {
        "line": 278,
        "matched": [
          "compose_e1r_v0_2_variant"
        ],
        "context": [
          {
            "line": 274,
            "text": "    compose_mentions_sidecar = \"sidecar_result\" in composer_text"
          },
          {
            "line": 275,
            "text": "    compose_mentions_daily = (\"daily_equity_records\" in composer_text) or (\"daily_records\" in composer_text) or (\"equity_curve\" in composer_text)"
          },
          {
            "line": 276,
            "text": ""
          },
          {
            "line": 277,
            "text": "    if has_compose_call_in_generator:"
          },
          {
            "line": 278,
            "text": "        findings.append(\"Generator references compose_e1r_v0_2_variant.\")"
          },
          {
            "line": 279,
            "text": "    else:"
          },
          {
            "line": 280,
            "text": "        risks.append(\"Generator does not directly reference compose_e1r_v0_2_variant; dry-run candidate may be wrapper-only or summary replay.\")"
          },
          {
            "line": 281,
            "text": ""
          },
          {
            "line": 282,
            "text": "    if has_compose_def:"
          }
        ]
      },
      {
        "line": 280,
        "matched": [
          "compose_e1r_v0_2_variant"
        ],
        "context": [
          {
            "line": 276,
            "text": ""
          },
          {
            "line": 277,
            "text
```

## Top Source Candidates

```json
[
  {
    "path": "scripts/audit_e1r_generator_composer_contract_4b0g.py",
    "score": 379,
    "hit_count": 37,
    "hits": [
      {
        "line": 41,
        "matched": [
          "compose_e1r_v0_2_variant"
        ],
        "context": [
          {
            "line": 37,
            "text": "    BACKTEST,"
          },
          {
            "line": 38,
            "text": "]"
          },
          {
            "line": 39,
            "text": ""
          },
          {
            "line": 40,
            "text": "TARGET_NAMES = ["
          },
          {
            "line": 41,
            "text": "    \"compose_e1r_v0_2_variant\","
          },
          {
            "line": 42,
            "text": "    \"core_variant_result\","
          },
          {
            "line": 43,
            "text": "    \"sidecar_result\","
          },
          {
            "line": 44,
            "text": "    \"daily_equity_records\","
          },
          {
            "line": 45,
            "text": "    \"daily_records\","
          }
        ]
      },
      {
        "line": 42,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 38,
            "text": "]"
          },
          {
            "line": 39,
            "text": ""
          },
          {
            "line": 40,
            "text": "TARGET_NAMES = ["
          },
          {
            "line": 41,
            "text": "    \"compose_e1r_v0_2_variant\","
          },
          {
            "line": 42,
            "text": "    \"core_variant_result\","
          },
          {
            "line": 43,
            "text": "    \"sidecar_result\","
          },
          {
            "line": 44,
            "text": "    \"daily_equity_records\","
          },
          {
            "line": 45,
            "text": "    \"daily_records\","
          },
          {
            "line": 46,
            "text": "    \"equity_curve\","
          }
        ]
      },
      {
        "line": 43,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 39,
            "text": ""
          },
          {
            "line": 40,
            "text": "TARGET_NAMES = ["
          },
          {
            "line": 41,
            "text": "    \"compose_e1r_v0_2_variant\","
          },
          {
            "line": 42,
            "text": "    \"core_variant_result\","
          },
          {
            "line": 43,
            "text": "    \"sidecar_result\","
          },
          {
            "line": 44,
            "text": "    \"daily_equity_records\","
          },
          {
            "line": 45,
            "text": "    \"daily_records\","
          },
          {
            "line": 46,
            "text": "    \"equity_curve\","
          },
          {
            "line": 47,
            "text": "    \"variant_results\","
          }
        ]
      },
      {
        "line": 44,
        "matched": [
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 40,
            "text": "TARGET_NAMES = ["
          },
          {
            "line": 41,
            "text": "    \"compose_e1r_v0_2_variant\","
          },
          {
            "line": 42,
            "text": "    \"core_variant_result\","
          },
          {
            "line": 43,
            "text": "    \"sidecar_result\","
          },
          {
            "line": 44,
            "text": "    \"daily_equity_records\","
          },
          {
            "line": 45,
            "text": "    \"daily_records\","
          },
          {
            "line": 46,
            "text": "    \"equity_curve\","
          },
          {
            "line": 47,
            "text": "    \"variant_results\","
          },
          {
            "line": 48,
            "text": "    \"build_equity_records_from_returns\","
          }
        ]
      },
      {
        "line": 48,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 44,
            "text": "    \"daily_equity_records\","
          },
          {
            "line": 45,
            "text": "    \"daily_records\","
          },
          {
            "line": 46,
            "text": "    \"equity_curve\","
          },
          {
            "line": 47,
            "text": "    \"variant_results\","
          },
          {
            "line": 48,
            "text": "    \"build_equity_records_from_returns\","
          },
          {
            "line": 49,
            "text": "    \"extract_core_interval_returns\","
          },
          {
            "line": 50,
            "text": "    \"build_e1r_sidecar_sleeve\","
          },
          {
            "line": 51,
            "text": "    \"run_strategy_variant_comparison\","
          },
          {
            "line": 52,
            "text": "    \"run_stateful_simulation\","
          }
        ]
      },
      {
        "line": 49,
        "matched": [
          "extract_core_interval_returns"
        ],
        "context": [
          {
            "line": 45,
            "text": "    \"daily_records\","
          },
          {
            "line": 46,
            "text": "    \"equity_curve\","
          },
          {
            "line": 47,
            "text": "    \"variant_results\","
          },
          {
            "line": 48,
            "text": "    \"build_equity_records_from_returns\","
          },
          {
            "line": 49,
            "text": "    \"extract_core_interval_returns\","
          },
          {
            "line": 50,
            "text": "    \"build_e1r_sidecar_sleeve\","
          },
          {
            "line": 51,
            "text": "    \"run_strategy_variant_comparison\","
          },
          {
            "line": 52,
            "text": "    \"run_stateful_simulation\","
          },
          {
            "line": 53,
            "text": "    \"e1r_v0_2_backtest_summary.json\","
          }
        ]
      },
      {
        "line": 51,
        "matched": [
          "run_strategy_variant_comparison"
        ],
        "context": [
          {
            "line": 47,
            "text": "    \"variant_results\","
          },
          {
            "line": 48,
            "text": "    \"build_equity_records_from_returns\","
          },
          {
            "line": 49,
            "text": "    \"extract_core_interval_returns\","
          },
          {
            "line": 50,
            "text": "    \"build_e1r_sidecar_sleeve\","
          },
          {
            "line": 51,
            "text": "    \"run_strategy_variant_comparison\","
          },
          {
            "line": 52,
            "text": "    \"run_stateful_simulation\","
          },
          {
            "line": 53,
            "text": "    \"e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 54,
            "text": "    \"e1r_v0_2_backtest_equity_curve.json\","
          },
          {
            "line": 55,
            "text": "    \"E1R_REGIME_AWARE_V0_2\","
          }
        ]
      },
      {
        "line": 52,
        "matched": [
          "run_stateful_simulation"
        ],
        "context": [
          {
            "line": 48,
            "text": "    \"build_equity_records_from_returns\","
          },
          {
            "line": 49,
            "text": "    \"extract_core_interval_returns\","
          },
          {
            "line": 50,
            "text": "    \"build_e1r_sidecar_sleeve\","
          },
          {
            "line": 51,
            "text": "    \"run_strategy_variant_comparison\","
          },
          {
            "line": 52,
            "text": "    \"run_stateful_simulation\","
          },
          {
            "line": 53,
            "text": "    \"e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 54,
            "text": "    \"e1r_v0_2_backtest_equity_curve.json\","
          },
          {
            "line": 55,
            "text": "    \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 56,
            "text": "]"
          }
        ]
      },
      {
        "line": 53,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "context": [
          {
            "line": 49,
            "text": "    \"extract_core_interval_returns\","
          },
          {
            "line": 50,
            "text": "    \"build_e1r_sidecar_sleeve\","
          },
          {
            "line": 51,
            "text": "    \"run_strategy_variant_comparison\","
          },
          {
            "line": 52,
            "text": "    \"run_stateful_simulation\","
          },
          {
            "line": 53,
            "text": "    \"e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 54,
            "text": "    \"e1r_v0_2_backtest_equity_curve.json\","
          },
          {
            "line": 55,
            "text": "    \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 56,
            "text": "]"
          },
          {
            "line": 57,
            "text": ""
          }
        ]
      },
      {
        "line": 54,
        "matched": [
          "e1r_v0_2_backtest_equity_curve.json"
        ],
        "context": [
          {
            "line": 50,
            "text": "    \"build_e1r_sidecar_sleeve\","
          },
          {
            "line": 51,
            "text": "    \"run_strategy_variant_comparison\","
          },
          {
            "line": 52,
            "text": "    \"run_stateful_simulation\","
          },
          {
            "line": 53,
            "text": "    \"e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 54,
            "text": "    \"e1r_v0_2_backtest_equity_curve.json\","
          },
          {
            "line": 55,
            "text": "    \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 56,
            "text": "]"
          },
          {
            "line": 57,
            "text": ""
          },
          {
            "line": 58,
            "text": "def now() -> str:"
          }
        ]
      },
      {
        "line": 55,
        "matched": [
          "E1R_REGIME_AWARE_V0_2"
        ],
        "context": [
          {
            "line": 51,
            "text": "    \"run_strategy_variant_comparison\","
          },
          {
            "line": 52,
            "text": "    \"run_stateful_simulation\","
          },
          {
            "line": 53,
            "text": "    \"e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 54,
            "text": "    \"e1r_v0_2_backtest_equity_curve.json\","
          },
          {
            "line": 55,
            "text": "    \"E1R_REGIME_AWARE_V0_2\","
          },
          {
            "line": 56,
            "text": "]"
          },
          {
            "line": 57,
            "text": ""
          },
          {
            "line": 58,
            "text": "def now() -> str:"
          },
          {
            "line": 59,
            "text": "    return datetime.now(timezone.utc).isoformat()"
          }
        ]
      },
      {
        "line": 267,
        "matched": [
          "compose_e1r_v0_2_variant"
        ],
        "context": [
          {
            "line": 263,
            "text": ""
          },
          {
            "line": 264,
            "text": "    generator_text = read_text(GENERATOR) if GENERATOR.exists() else \"\""
          },
          {
            "line": 265,
            "text": "    composer_text = read_text(COMPOSER) if COMPOSER.exists() else \"\""
          },
          {
            "line": 266,
            "text": ""
          },
          {
            "line": 267,
            "text": "    has_compose_call_in_generator = \"compose_e1r_v0_2_variant\" in generator_text"
          },
          {
            "line": 268,
            "text": "    has_core_var_in_generator = \"core_variant_result\" in generator_text"
          },
          {
            "line": 269,
            "text": "    has_sidecar_var_in_generator = \"sidecar_result\" in generator_text"
          },
          {
            "line": 270,
            "text": "    has_daily_in_generator = (\"daily_equity_records\" in generator_text) or (\"daily_records\" in generator_text) or (\"equity_curve\" in generator_text)"
          },
          {
            "line": 271,
            "text": ""
          }
        ]
      },
      {
        "line": 268,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 264,
            "text": "    generator_text = read_text(GENERATOR) if GENERATOR.exists() else \"\""
          },
          {
            "line": 265,
            "text": "    composer_text = read_text(COMPOSER) if COMPOSER.exists() else \"\""
          },
          {
            "line": 266,
            "text": ""
          },
          {
            "line": 267,
            "text": "    has_compose_call_in_generator = \"compose_e1r_v0_2_variant\" in generator_text"
          },
          {
            "line": 268,
            "text": "    has_core_var_in_generator = \"core_variant_result\" in generator_text"
          },
          {
            "line": 269,
            "text": "    has_sidecar_var_in_generator = \"sidecar_result\" in generator_text"
          },
          {
            "line": 270,
            "text": "    has_daily_in_generator = (\"daily_equity_records\" in generator_text) or (\"daily_records\" in generator_text) or (\"equity_curve\" in generator_text)"
          },
          {
            "line": 271,
            "text": ""
          },
          {
            "line": 272,
            "text": "    has_compose_def = \"def compose_e1r_v0_2_variant\" in composer_text"
          }
        ]
      },
      {
        "line": 269,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 265,
            "text": "    composer_text = read_text(COMPOSER) if COMPOSER.exists() else \"\""
          },
          {
            "line": 266,
            "text": ""
          },
          {
            "line": 267,
            "text": "    has_compose_call_in_generator = \"compose_e1r_v0_2_variant\" in generator_text"
          },
          {
            "line": 268,
            "text": "    has_core_var_in_generator = \"core_variant_result\" in generator_text"
          },
          {
            "line": 269,
            "text": "    has_sidecar_var_in_generator = \"sidecar_result\" in generator_text"
          },
          {
            "line": 270,
            "text": "    has_daily_in_generator = (\"daily_equity_records\" in generator_text) or (\"daily_records\" in generator_text) or (\"equity_curve\" in generator_text)"
          },
          {
            "line": 271,
            "text": ""
          },
          {
            "line": 272,
            "text": "    has_compose_def = \"def compose_e1r_v0_2_variant\" in composer_text"
          },
          {
            "line": 273,
            "text": "    compose_mentions_core = \"core_variant_result\" in composer_text"
          }
        ]
      },
      {
        "line": 270,
        "matched": [
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 266,
            "text": ""
          },
          {
            "line": 267,
            "text": "    has_compose_call_in_generator = \"compose_e1r_v0_2_variant\" in generator_text"
          },
          {
            "line": 268,
            "text": "    has_core_var_in_generator = \"core_variant_result\" in generator_text"
          },
          {
            "line": 269,
            "text": "    has_sidecar_var_in_generator = \"sidecar_result\" in generator_text"
          },
          {
            "line": 270,
            "text": "    has_daily_in_generator = (\"daily_equity_records\" in generator_text) or (\"daily_records\" in generator_text) or (\"equity_curve\" in generator_text)"
          },
          {
            "line": 271,
            "text": ""
          },
          {
            "line": 272,
            "text": "    has_compose_def = \"def compose_e1r_v0_2_variant\" in composer_text"
          },
          {
            "line": 273,
            "text": "    compose_mentions_core = \"core_variant_result\" in composer_text"
          },
          {
            "line": 274,
            "text": "    compose_mentions_sidecar = \"sidecar_result\" in composer_text"
          }
        ]
      },
      {
        "line": 272,
        "matched": [
          "compose_e1r_v0_2_variant"
        ],
        "context": [
          {
            "line": 268,
            "text": "    has_core_var_in_generator = \"core_variant_result\" in generator_text"
          },
          {
            "line": 269,
            "text": "    has_sidecar_var_in_generator = \"sidecar_result\" in generator_text"
          },
          {
            "line": 270,
            "text": "    has_daily_in_generator = (\"daily_equity_records\" in generator_text) or (\"daily_records\" in generator_text) or (\"equity_curve\" in generator_text)"
          },
          {
            "line": 271,
            "text": ""
          },
          {
            "line": 272,
            "text": "    has_compose_def = \"def compose_e1r_v0_2_variant\" in composer_text"
          },
          {
            "line": 273,
            "text": "    compose_mentions_core = \"core_variant_result\" in composer_text"
          },
          {
            "line": 274,
            "text": "    compose_mentions_sidecar = \"sidecar_result\" in composer_text"
          },
          {
            "line": 275,
            "text": "    compose_mentions_daily = (\"daily_equity_records\" in composer_text) or (\"daily_records\" in composer_text) or (\"equity_curve\" in composer_text)"
          },
          {
            "line": 276,
            "text": ""
          }
        ]
      },
      {
        "line": 273,
        "matched": [
          "core_variant_result"
        ],
        "context": [
          {
            "line": 269,
            "text": "    has_sidecar_var_in_generator = \"sidecar_result\" in generator_text"
          },
          {
            "line": 270,
            "text": "    has_daily_in_generator = (\"daily_equity_records\" in generator_text) or (\"daily_records\" in generator_text) or (\"equity_curve\" in generator_text)"
          },
          {
            "line": 271,
            "text": ""
          },
          {
            "line": 272,
            "text": "    has_compose_def = \"def compose_e1r_v0_2_variant\" in composer_text"
          },
          {
            "line": 273,
            "text": "    compose_mentions_core = \"core_variant_result\" in composer_text"
          },
          {
            "line": 274,
            "text": "    compose_mentions_sidecar = \"sidecar_result\" in composer_text"
          },
          {
            "line": 275,
            "text": "    compose_mentions_daily = (\"daily_equity_records\" in composer_text) or (\"daily_records\" in composer_text) or (\"equity_curve\" in composer_text)"
          },
          {
            "line": 276,
            "text": ""
          },
          {
            "line": 277,
            "text": "    if has_compose_call_in_generator:"
          }
        ]
      },
      {
        "line": 274,
        "matched": [
          "sidecar_result"
        ],
        "context": [
          {
            "line": 270,
            "text": "    has_daily_in_generator = (\"daily_equity_records\" in generator_text) or (\"daily_records\" in generator_text) or (\"equity_curve\" in generator_text)"
          },
          {
            "line": 271,
            "text": ""
          },
          {
            "line": 272,
            "text": "    has_compose_def = \"def compose_e1r_v0_2_variant\" in composer_text"
          },
          {
            "line": 273,
            "text": "    compose_mentions_core = \"core_variant_result\" in composer_text"
          },
          {
            "line": 274,
            "text": "    compose_mentions_sidecar = \"sidecar_result\" in composer_text"
          },
          {
            "line": 275,
            "text": "    compose_mentions_daily = (\"daily_equity_records\" in composer_text) or (\"daily_records\" in composer_text) or (\"equity_curve\" in composer_text)"
          },
          {
            "line": 276,
            "text": ""
          },
          {
            "line": 277,
            "text": "    if has_compose_call_in_generator:"
          },
          {
            "line": 278,
            "text": "        findings.append(\"Generator references compose_e1r_v0_2_variant.\")"
          }
        ]
      },
      {
        "line": 275,
        "matched": [
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 271,
            "text": ""
          },
          {
            "line": 272,
            "text": "    has_compose_def = \"def compose_e1r_v0_2_variant\" in composer_text"
          },
          {
            "line": 273,
            "text": "    compose_mentions_core = \"core_variant_result\" in composer_text"
          },
          {
            "line": 274,
            "text": "    compose_mentions_sidecar = \"sidecar_result\" in composer_text"
          },
          {
            "line": 275,
            "text": "    compose_mentions_daily = (\"daily_equity_records\" in composer_text) or (\"daily_records\" in composer_text) or (\"equity_curve\" in composer_text)"
          },
          {
            "line": 276,
            "text": ""
          },
          {
            "line": 277,
            "text": "    if has_compose_call_in_generator:"
          },
          {
            "line": 278,
            "text": "        findings.append(\"Generator references compose_e1r_v0_2_variant.\")"
          },
          {
            "line": 279,
            "text": "    else:"
          }
        ]
      },
      {
        "line": 278,
        "matched": [
          "compose_e1r_v0_2_variant"
        ],
        "context": [
          {
            "line": 274,
            "text": "    compose_mentions_sidecar = \"sidecar_result\" in composer_text"
          },
          {
            "line": 275,
            "text": "    compose_mentions_daily = (\"daily_equity_records\" in composer_text) or (\"daily_records\" in composer_text) or (\"equity_curve\" in composer_text)"
          },
          {
            "line": 276,
            "text": ""
          },
          {
            "line": 277,
            "text": "    if has_compose_call_in_generator:"
          },
          {
            "line": 278,
            "text": "        findings.append(\"Generator references compose_e1r_v0_2_variant.\")"
          },
          {
            "line": 279,
            "text": "    else:"
          },
          {
            "line": 280,
            "text": "        risks.append(\"Generator does not directly reference compose_e1r_v0_2_variant; dry-run candidate may be wrapper-only or summary replay.\")"
          },
          {
            "line": 281,
            "text": ""
          },
          {
            "line": 282,
            "text": "    if has_compose_def:"
          }
        ]
      },
      {
        "line": 280,
        "matched": [
          "compose_e1r_v0_2_variant"
        ],
        "context": [
          {
            "line": 276,
            "text": ""
          },
          {
            "line": 277,
            "text": "    if has_compose_call_in_generator:"
          },
          {
            "line": 278,
            "text": "        findings.append(\"Generator references compose_e1r_v0_2_variant.\")"
          },
          {
            "line": 279,
            "text": "    else:"
          },
          {
            "line": 280,
            "text": "        risks.append(\"Generator does not directly reference compose_e1r_v0_2_variant; dry-run candidate may be wrapper-only or summary replay.\")"
          },
          {
            "line": 281,
            "text": ""
          },
          {
            "line": 282,
            "text": "    if has_compose_def:"
          },
          {
            "line": 283,
            "text": "        findings.append(\"Composer defines compose_e1r_v0_2_variant.\")"
          },
          {
            "line": 284,
            "text": "    else:"
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
            "line": 279,
            "text": "    else:"
          },
          {
            "line": 280,
            "text": "        risks.append(\"Generator does not directly reference compose_e1r_v0_2_variant; dry-run candidate may be wrapper-only or summary replay.\")"
          },
          {
            "line": 281,
            "text": ""
          },
          {
            "line": 282,
            "text": "    if has_compose_def:"
          },
          {
            "line": 283,
            "text": "        findings.append(\"Composer defines compose_e1r_v0_2_variant.\")"
          },
          {
            "line": 284,
            "text": "    else:"
          },
          {
            "line": 285,
            "text": "        risks.append(\"Composer definition compose_e1r_v0_2_variant not found by text scan.\")"
          },
          {
            "line": 286,
            "text": ""
          },
          {
            "li
```

## Output Inspection

```json
{
  "exports/e1r_v0_2_backtest_summary.json": {
    "path": "exports/e1r_v0_2_backtest_summary.json",
    "exists_after_run": true,
    "size_after_run": 941,
    "hash_after_run": "449a8ace55ce2335d174e17e2532d8793a3a9b99c021a935f8d7f2e531092114",
    "top_summary": {
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
        "sharpe_ratio": 0.7957270568329264,
        "row_count": 1258
      },
      "children": {
        "sidecar_active_by_regime": {
          "type": "dict",
          "len": 1,
          "keys": [
            "SIDEWAYS"
          ]
        },
        "sidecar_active_by_subclass": {
          "type": "dict",
          "len": 1,
          "keys": [
            "MA_CONFLICT"
          ]
        }
      }
    }
  },
  "exports/e1r_v0_2_backtest_equity_curve.json": {
    "path": "exports/e1r_v0_2_backtest_equity_curve.json",
    "exists_after_run": true,
    "size_after_run": 16004713,
    "hash_after_run": "d43ac75bc56340079b98958d73a0b2c3acb8c7154c04f8a0c394e5e969246926"
  },
  "exports/e1r_v0_2_portfolio_backtest_equity_curve.json": {
    "path": "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
    "exists_after_run": false,
    "size_after_run": 0,
    "hash_after_run": null
  },
  "exports/e1_e1r_5y_equity_comparison.json": {
    "path": "exports/e1_e1r_5y_equity_comparison.json",
    "exists_after_run": false,
    "size_after_run": 0,
    "hash_after_run": null
  },
  "data/research/e1r/e1r_formal_backtest_v0_1.json": {
    "path": "data/research/e1r/e1r_formal_backtest_v0_1.json",
    "exists_after_run": true,
    "size_after_run": 81365,
    "hash_after_run": "a42c6496d407f833ab117307a7677d7c4d251482ae02495271eea0e060202dad",
    "top_summary": {
      "type": "dict",
      "len": 9,
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
      "children": {
        "metrics": {
          "type": "dict",
          "len": 10,
          "keys": [
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
        "e1_metrics": {
          "type": "dict",
          "len": 5,
          "keys": [
            "max_drawdown_pct",
            "number_of_trades",
            "profit_factor",
            "sharpe_ratio",
            "total_return_pct"
          ]
        },
        "equity_curve": {
          "type": "list",
          "len": 131,
          "first_type": "float"
        },
        "spx_curve": {
          "type": "list",
          "len": 131,
          "first_type": "float"
        },
        "trades": {
          "type": "list",
          "len": 39,
          "first_type": "dict",
          "first_keys": [
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
          ],
          "first_sample": {
            "symbol": "MELI",
            "entry_date": "2023-11-28",
            "exit_date": "2024-01-04",
            "entry_signal": "BUY",
            "exit_signal": "EXIT",
            "entry_price": 1599.21,
            "avg_cost": 1607.2,
            "exit_price": 1500.0,
            "effective_exit": 1482.16,
            "return_pct": -4.73,
            "max_gain_pct": 2.79,
            "max_drawdown_in_trade": 9.2,
            "holding_days": 26,
            "size_units_at_exit": 0.5,
            "leader_score_entry": 94.4,
            "relative_stop_triggered": false,
            "relative_stop_exec_date": null,
            "take_profit_triggered": false,
            "take_profit_exec_date": null,
            "realized_pnl_before_exit": -282.58,
            "actions_during_trade": [
              "BUY",
              "ADD",
              "ADD",
              "BUY",
              "ADD",
              "ADD",
              "BUY",
              "ADD",
              "HOLD",
              "REDUCE",
              "REDUCE",
              "REDUCE",
              "HOLD",
              "HOLD",
              "HOLD",
              "HOLD",
              "HOLD",
              "HOLD",
              "HOLD",
              "REDUCE",
              "REDUCE",
              "REDUCE",
              "REDUCE",
              "REDUCE",
              "REDUCE",
              "REDUCE",
              "REDUCE",
              "REDUCE",
              "EXIT"
            ],
            "action_count": 29,
            "execution_model": "adverse_intraday_v1.0",
            "entry_adverse_gap_pct": 0.5,
            "exit_adverse_gap_pct": 1.19,
            "total_execution_drag_pct": 1.689,
            "is_sim_end": false,
            "entry_regime": "UPTREND",
            "exit_regime": "UPTREND",
            "dominant_regime": "UPTREND",
            "entry_type": "E1R_UPTREND_CONFIRMED",
            "regime_day_weights": {
              "UPTREND": 25
            },
            "exit_reason": "leader_score_below_60",
            "exit_reasons": [
              "leader_score_below_60"
            ],
            "exit_type": "NORMAL_EXIT",
            "exit_warning_log": [],
            "exit_warning_count": 0
          },
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
      }
    }
  }
}
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-4B-0K`: Instrument highest direct source callsite or recover core builder
- Recommended action: Instrument the highest source callsite directly instead of export_canonical_5y_equity_curves.py.

