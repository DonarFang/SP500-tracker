# E1R Unified 5Y Full Account V1 — 4C-2B Smoke Invoke

Generated At: `2026-07-09T11:16:36.062544+00:00`

## Status

- Status: `E1R_UNIFIED_ENGINE_SMOKE_INVOKE_COMPLETE_NO_FULL_BACKTEST`
- Full backtest run: `False`
- Strategy logic changed: `False`
- Canonical backtest written: `False`

## Import Probe

```json
{
  "attempted": true,
  "ok": true,
  "error": null,
  "signature": "(symbols: 'list[str]', prices_map: 'dict[str, list[float]]', dates_map: 'dict[str, list[str]]', spx_prices: 'list[float]', spx_dates: 'list[str]', ohlc_map: 'dict' = None, assumptions: 'dict' = None, step: 'int' = 1, min_history: 'int' = 120, market_score_default: 'float' = 60.0, sim_start_date: 'str' = None, sim_end_date: 'str' = None, ndx_prices: 'list' = None, ndx_dates: 'list' = None, sox_prices: 'list' = None, sox_dates: 'list' = None, vix_prices: 'list' = None, vix_dates: 'list' = None) -> 'dict'",
  "module_file": "/Users/dongfang/Downloads/sp500-tracker-v13/src/engine/backtest.py"
}
```

## Smoke

```json
{
  "attempted": true,
  "ok": false,
  "error": "KeyError: 'buy_size'",
  "traceback_tail": "Traceback (most recent call last):\n  File \"/Users/dongfang/Downloads/sp500-tracker-v13/scripts/smoke_invoke_unified_engine_4c2b.py\", line 261, in main\n    result = fn(\n  File \"/Users/dongfang/Downloads/sp500-tracker-v13/src/engine/backtest.py\", line 797, in run_stateful_simulation\n    buy_pct  = a[\"buy_size\"]  / max_pos       # Top3: 1/3 per full slot\nKeyError: 'buy_size'\n",
  "input_summary": {
    "symbol_count": 12,
    "symbols": [
      "A",
      "AAL",
      "AAPL",
      "ABBV",
      "ABNB",
      "ABT",
      "ACGL",
      "ACN",
      "ADBE",
      "ADI",
      "ADM",
      "ADP"
    ],
    "spx_count": 1562,
    "spx_start": "2020-04-01",
    "spx_end": "2026-06-18",
    "sim_start_date": "2021-04-14",
    "sim_end_date": "2021-07-09",
    "assumption_keys": [
      "candidate_top_n",
      "e1r_unified_smoke",
      "entry_rs_min",
      "entry_top_n",
      "execution_model",
      "initial_capital",
      "leader_score_exit",
      "market_entry_gate",
      "market_gate_enabled",
      "max_positions",
      "min_holding_days",
      "position_size_pct",
      "qualified_entry_enabled",
      "qualified_states"
    ]
  },
  "result_summary": {}
}
```

## Conclusion

- `PACKAGE_IMPORT_OK_SMOKE_INVOKE_FAILED`
- Recommended: Use traceback to adjust assumptions/input contract, then retry smoke.

