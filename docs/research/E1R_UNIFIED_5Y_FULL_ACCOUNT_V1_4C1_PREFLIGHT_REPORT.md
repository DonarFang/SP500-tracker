# E1R Unified 5Y Full Account V1 — 4C-1 Preflight

Generated At: `2026-07-09T11:11:34.812663+00:00`

## Status

- Status: `E1R_UNIFIED_5Y_FULL_ACCOUNT_PREFLIGHT_COMPLETE`
- Full backtest run: `False`
- Strategy logic changed: `False`
- Canonical backtest written: `False`
- Spec written: `True`

## Preflight Checks

```json
{
  "required_data_exists": true,
  "spx_regime_available": true,
  "sidecar_records_available": true,
  "backtest_import_ok": false,
  "composer_import_ok": true,
  "sidecar_import_ok": true,
  "stateful_simulation_function_found": false,
  "variant_comparison_function_found": false,
  "composer_function_found": true
}
```

## Available Functions

```json
{
  "e1r_composer.compose_e1r_v0_2_variant": "(core_variant_result: 'dict[str, Any]', sidecar_result: 'dict[str, Any]', initial_equity: 'float' = 100000.0) -> 'dict[str, Any]'",
  "e1r_composer.extract_core_interval_returns": "(core_daily_equity_records: 'Sequence[dict[str, Any]]', sidecar_records: 'Sequence[dict[str, Any]]') -> 'list[dict[str, Any]]'",
  "e1r_composer.build_equity_records_from_returns": "(interval_records: 'Sequence[dict[str, Any]]', initial_equity: 'float') -> 'list[dict[str, Any]]'",
  "e1r_sidecar_sleeve.build_e1r_sidecar_sleeve": "(stock_dir: 'Path', spx_path: 'Path', regime_path: 'Path', config: 'E1RSidecarConfig') -> 'dict[str, Any]'"
}
```

## Data Summary

```json
{
  "spx_regime_daily": {
    "exists": true,
    "path": "data/research/e1_5y/regimes/spx_regime_daily.json",
    "size": 125589,
    "sha256": "3ad4f9308b0b6b77476e4a7d204d3fab71882a5cd6234d872aa5299bf356afc8",
    "json_valid": true,
    "type": "dict",
    "top_keys": [
      "daily_regime",
      "generated_at",
      "validation_window"
    ],
    "daily_regime_count": 1562,
    "daily_regime_start": "2020-04-01",
    "daily_regime_end": "2026-06-18"
  },
  "spx_raw": {
    "exists": true,
    "path": "data/research/e1_5y/raw/indices/SPX.json",
    "size": 201484,
    "sha256": "04e09605b1bee9a900a0f3db4c1926e6bd48f8f4dceebf711b2c9511bd98633e",
    "json_valid": true,
    "type": "dict",
    "top_keys": [
      "bars",
      "data_end",
      "data_start",
      "dataset_mode",
      "downloaded_at",
      "requested_end",
      "requested_start",
      "schema_version",
      "source",
      "symbol",
      "yahoo_ticker"
    ],
    "bars_len": 1562,
    "bars_first_keys": [
      "close",
      "date",
      "high",
      "low",
      "open",
      "volume"
    ],
    "bars_first": {
      "date": "2020-04-01",
      "open": 2498.080078,
      "high": 2522.75,
      "low": 2447.48999,
      "close": 2470.5,
      "volume": 5964000000
    },
    "bars_last": {
      "date": "2026-06-18",
      "open": 7487.359863,
      "high": 7511.069824,
      "low": 7468.319824,
      "close": 7500.580078,
      "volume": 9061110000
    }
  },
  "e1r_sidecar_records": {
    "exists": true,
    "path": "exports/e1r_v0_2_sidecar_records_5y.json",
    "size": 1125719,
    "sha256": "2113cbaeb47e2905b45ffd7a41dc2806789aba280a016aebadca12e58a8439e9",
    "json_valid": true,
    "type": "dict",
    "top_keys": [
      "artifact_type",
      "config",
      "generated_at",
      "input_summary",
      "interval_stats",
      "policy",
      "records",
      "sidecar_stats",
      "sidecar_summary",
      "source",
      "validation",
      "window"
    ],
    "records_len": 1260,
    "records_first_keys": [
      "candidate_count",
      "date",
      "next_date",
      "raw_contract",
      "regime",
      "sidecar_active",
      "sidecar_gross_exposure",
      "sidecar_holdings",
      "sidecar_return",
      "sidecar_return_pct",
      "sidecar_selected_count",
      "spx_return",
      "spx_return_pct",
      "subclass"
    ],
    "records_first": {
      "date": "2021-06-11",
      "next_date": "2021-06-14",
      "regime": "UPTREND",
      "subclass": "NO_SUBCLASS",
      "sidecar_active": false,
      "sidecar_return": 0.0,
      "sidecar_return_pct": 0.0,
      "spx_return": 0.0018152018879837861,
      "spx_return_pct": 0.1815201887983786,
      "sidecar_gross_exposure": 0.0,
      "sidecar_selected_count": 0,
      "sidecar_holdings": [],
      "candidate_count": 0,
      "raw_contract": "is_active/portfolio_return/gross_exposure/selected_count/holdings"
    },
    "records_last": {
      "date": "2026-06-17",
      "next_date": "2026-06-18",
      "regime": "UPTREND",
      "subclass": "NO_SUBCLASS",
      "sidecar_active": false,
      "sidecar_return": 0.0,
      "sidecar_return_pct": 0.0,
      "spx_return": 0.010846212171947922,
      "spx_return_pct": 1.0846212171947922,
      "sidecar_gross_exposure": 0.0,
      "sidecar_selected_count": 0,
      "sidecar_holdings": [],
      "candidate_count": 0,
      "raw_contract": "is_active/portfolio_return/gross_exposure/selected_count/holdings"
    }
  }
}
```

## Conclusion

- `UNIFIED_5Y_BACKTEST_ENGINE_ENTRYPOINT_NOT_YET_RESOLVED`
- Recommended: Before full run, add a thin adapter around the existing portfolio/stateful engine entrypoint; do not reconstruct from summary artifacts.

## Spec Path

- `docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_SPEC.json`

