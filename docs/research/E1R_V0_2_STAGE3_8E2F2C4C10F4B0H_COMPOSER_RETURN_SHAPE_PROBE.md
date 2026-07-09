# Stage 3.8E-2F-2C-4C-10F-4B-0H Composer Return Shape Probe

Generated At: `2026-07-09T10:35:11.914002+00:00`

## Status

- Status: `E1R_COMPOSER_RETURN_SHAPE_PROBE_COMPLETE_NO_RUNTIME_EXECUTION`
- Composer function invoked: `False`
- Generator executed: `False`
- E1R canonical written: `False`
- Strategy files unchanged: `True`
- Canonical existence unchanged: `True`

## Conclusion

- `COMPOSER_RETURN_CONTRACT_HAS_CORE_AND_SIDECAR_SOURCE_FIELDS`
- Recommended: Use the inspected signature/source to design the next wrapper: either direct invoke compose_e1r_v0_2_variant if inputs are available, or instrument the existing call site that builds those inputs.

## Inference

```json
{
  "source_flags": {
    "mentions_core_variant_result": true,
    "mentions_sidecar_result": true,
    "mentions_daily_equity_records": true,
    "mentions_daily_records": false,
    "mentions_equity_curve": false,
    "mentions_variant_results": false,
    "mentions_metrics": false,
    "mentions_total_return_pct": true,
    "mentions_profit_factor": true,
    "mentions_sharpe_ratio": true,
    "mentions_build_equity_records_from_returns": true,
    "mentions_extract_core_interval_returns": true,
    "mentions_build_e1r_sidecar_sleeve": false,
    "return_mentions_dict": false,
    "return_mentions_result": true,
    "return_mentions_metrics": false,
    "return_mentions_daily": false
  },
  "findings": [
    "compose_e1r_v0_2_variant definition found in composer source.",
    "compose_e1r_v0_2_variant can be imported and its signature can be inspected.",
    "Function source mentions core_variant_result.",
    "Function source mentions sidecar_result.",
    "Function source mentions daily/equity output fields."
  ],
  "risks": [
    "Return expression may not directly expose a dict; runtime probe may need wrapper instrumentation."
  ],
  "recommended_next_actions": [
    "Run a narrow runtime invocation probe only if required arguments can be resolved from signature and existing generator code.",
    "If direct invocation requires full data objects, build an instrumentation wrapper around existing generator/composer call site instead of guessing arguments.",
    "Do not use persisted exports/e1r_v0_2_backtest_equity_curve.json as portfolio equity; 4B-0F-v2 already rejected it."
  ]
}
```

## Import Probe

```json
{
  "attempted": true,
  "ok": true,
  "module": "e1r_composer",
  "errors": [],
  "target_function": {
    "exists": true,
    "type": "function",
    "signature": "(core_variant_result: 'dict[str, Any]', sidecar_result: 'dict[str, Any]', initial_equity: 'float' = 100000.0) -> 'dict[str, Any]'",
    "source_line": 283,
    "source_excerpt": "def compose_e1r_v0_2_variant(\n    core_variant_result: dict[str, Any],\n    sidecar_result: dict[str, Any],\n    initial_equity: float = 100000.0,\n) -> dict[str, Any]:\n    core_records = core_variant_result.get(\"daily_equity_records\", [])\n    sidecar_records = sidecar_result.get(\"records\", [])\n\n    interval_records = extract_core_interval_returns(core_records, sidecar_records)\n    equity_records = build_equity_records_from_returns(interval_records, initial_equity)\n    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)\n\n    result = copy.deepcopy(core_variant_result)\n\n    sidecar_summary = sidecar_result.get(\"summary\", {}) or {}\n\n    result.update({\n        \"strategy_id\": \"E1R_REGIME_AWARE_V0_2\",\n        \"strategy_variant\": \"E1R_regime_aware_v0_2_formal_sidecar_sleeve\",\n        \"version\": \"E1R-v0.2-formal-sidecar-sleeve\",\n        \"research_status\": \"FORMAL_SIDECAR_SLEEVE_ENGINE\",\n        \"core_total_trades\": core_variant_result.get(\"total_trades\"),\n        \"sidecar_trade_count_approx\": sidecar_summary.get(\"trade_count_approx\"),\n        \"combined_trade_count_note\": (\n            \"total_trades remains inherited from E1R v0.1 core; \"\n            \"sidecar_trade_count_approx counts daily basket holdings and is not \"\n            \"stateful round-trip trade count.\"\n        ),\n        \"e1r_v0_2_composition\": {\n            \"core_variant\": \"E1R_REGIME_AWARE_V0_1\",\n            \"sidecar_engine\": sidecar_result.get(\"engine\"),\n            \"sidecar_version\": sidecar_result.get(\"version\"),\n            \"alignment\": \"core daily return ending at next_date aligned to sidecar date->next_date interval\",\n            \"composition_formula\": \"(1 + core_return) * (1 + sidecar_return) - 1\",\n            \"sidecar_config\": sidecar_result.get(\"config\", {}),\n            \"sidecar_sample\": sidecar_result.get(\"sample\", {}),\n            \"sidecar_summary\": sidecar_result.get(\"summary\", {}),\n            \"combined_summary\": summary,\n        },\n        \"daily_equity_records\": equity_records,\n        \"daily_equity_record_count\": len(equity_records),\n        \"e1r_v0_2_interval_records_sample\": {\n            \"first_5\": interval_records[:5],\n            \"last_5\": interval_records[-5:],\n        },\n    })\n\n    # Override summary-level fields with formal combined values.\n    for key in (\n        \"total_return_pct\",\n        \"spx_return_pct\",\n        \"alpha_pct\",\n        \"max_drawdown_pct\",\n        \"profit_factor\",\n        \"sharpe_ratio\",\n    ):\n        if key in summary:\n            result[key] = summary[key]\n\n    result[\"total_days\"] = summary[\"total_days\"]\n    result[\"sidecar_active_days\"] = summary[\"sidecar_active_days\"]\n    result[\"sidecar_active_by_regime\"] = summary[\"sidecar_active_by_regime\"]\n    result[\"sidecar_active_by_subclass\"] = summary[\"sidecar_active_by_subclass\"]\n    result[\"sidecar_simple_contribution_by_regime_pct\"] = summary[\"sidecar_simple_contribution_by_regime_pct\"]\n    result[\"sidecar_simple_contribution_by_subclass_pct\"] = summary[\"sidecar_simple_contribution_by_subclass_pct\"]\n\n    result.setdefault(\"strategy_controls\", {})\n    result[\"strategy_controls\"].update({\n        \"regime_aware_logic\": \"UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\",\n        \"e1r_v0_2_formal_sidecar_sleeve\": True,\n        \"e1r_v0_2_core_variant\": \"E1R_REGIME_AWARE_V0_1\",\n        \"e1r_v0_2_sidecar_allowed_subclasses\": sidecar_result.get(\"config\", {}).get(\"allowed_subclasses\"),\n        \"e1r_v0_2_sidecar_top_n\": sidecar_result.get(\"config\", {}).get(\"top_n\"),\n        \"e1r_v0_2_sidecar_gross_exposure\": sidecar_result.get(\"config\", {}).get(\"gross_exposure\"),\n        \"e1r_v0_2_excluded_symbols\": sidecar_result.get(\"config\", {}).get(\"excluded_symbols\"),\n    })\n\n    return result\n"
  },
  "public_relevant_objects": {
    "build_equity_records_from_returns": {
      "type": "function",
      "signature": "(interval_records: 'Sequence[dict[str, Any]]', initial_equity: 'float') -> 'list[dict[str, Any]]'"
    },
    "compose_e1r_v0_2_variant": {
      "type": "function",
      "signature": "(core_variant_result: 'dict[str, Any]', sidecar_result: 'dict[str, Any]', initial_equity: 'float' = 100000.0) -> 'dict[str, Any]'"
    },
    "compound_return": {
      "type": "function",
      "signature": "(returns: 'Sequence[Optional[float]]') -> 'float'"
    },
    "extract_core_interval_returns": {
      "type": "function",
      "signature": "(core_daily_equity_records: 'Sequence[dict[str, Any]]', sidecar_records: 'Sequence[dict[str, Any]]') -> 'list[dict[str, Any]]'"
    },
    "summarize_combined_variant": {
      "type": "function",
      "signature": "(interval_records: 'Sequence[dict[str, Any]]', equity_records: 'Sequence[dict[str, Any]]', initial_equity: 'float') -> 'dict[str, Any]'"
    }
  }
}
```

## Function Signature / Return Contract

```json
{
  "exists": true,
  "name": "compose_e1r_v0_2_variant",
  "line": 283,
  "end_line": 360,
  "signature_ast": {
    "args": [
      {
        "name": "core_variant_result",
        "annotation": "dict[str, Any]"
      },
      {
        "name": "sidecar_result",
        "annotation": "dict[str, Any]"
      },
      {
        "name": "initial_equity",
        "annotation": "float"
      }
    ],
    "defaults": [
      "100000.0"
    ],
    "returns_annotation": "dict[str, Any]"
  },
  "returns": [
    "result"
  ],
  "return_nodes": [
    {
      "line": 360,
      "value": "result"
    }
  ],
  "assignments_of_interest": [
    {
      "line": 288,
      "target": "core_records",
      "value": "core_variant_result.get('daily_equity_records', [])"
    },
    {
      "line": 289,
      "target": "sidecar_records",
      "value": "sidecar_result.get('records', [])"
    },
    {
      "line": 291,
      "target": "interval_records",
      "value": "extract_core_interval_returns(core_records, sidecar_records)"
    },
    {
      "line": 292,
      "target": "equity_records",
      "value": "build_equity_records_from_returns(interval_records, initial_equity)"
    },
    {
      "line": 293,
      "target": "summary",
      "value": "summarize_combined_variant(interval_records, equity_records, initial_equity)"
    },
    {
      "line": 295,
      "target": "result",
      "value": "copy.deepcopy(core_variant_result)"
    },
    {
      "line": 297,
      "target": "sidecar_summary",
      "value": "sidecar_result.get('summary', {}) or {}"
    },
    {
      "line": 342,
      "target": "result['total_days']",
      "value": "summary['total_days']"
    },
    {
      "line": 343,
      "target": "result['sidecar_active_days']",
      "value": "summary['sidecar_active_days']"
    },
    {
      "line": 344,
      "target": "result['sidecar_active_by_regime']",
      "value": "summary['sidecar_active_by_regime']"
    },
    {
      "line": 345,
      "target": "result['sidecar_active_by_subclass']",
      "value": "summary['sidecar_active_by_subclass']"
    },
    {
      "line": 346,
      "target": "result['sidecar_simple_contribution_by_regime_pct']",
      "value": "summary['sidecar_simple_contribution_by_regime_pct']"
    },
    {
      "line": 347,
      "target": "result['sidecar_simple_contribution_by_subclass_pct']",
      "value": "summary['sidecar_simple_contribution_by_subclass_pct']"
    },
    {
      "line": 340,
      "target": "result[key]",
      "value": "summary[key]"
    }
  ],
  "dict_literals": [],
  "calls_unique": [
    "build_equity_records_from_returns",
    "deepcopy",
    "extract_core_interval_returns",
    "get",
    "len",
    "setdefault",
    "summarize_combined_variant",
    "update"
  ]
}
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-4B-0I`: Resolve composer invocation inputs or instrument existing call site
- Recommended action: Use the inspected signature/source to design the next wrapper: either direct invoke compose_e1r_v0_2_variant if inputs are available, or instrument the existing call site that builds those inputs.

