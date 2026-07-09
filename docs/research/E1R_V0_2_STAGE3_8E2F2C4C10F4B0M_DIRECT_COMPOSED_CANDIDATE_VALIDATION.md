# Stage 3.8E-2F-2C-4C-10F-4B-0M Direct-Composed Candidate Validation

Generated At: `2026-07-09T10:56:18.259928+00:00`

## Status

- Status: `E1R_DIRECT_COMPOSED_CANDIDATE_VALIDATION_COMPLETE_NONCANONICAL`
- E1R canonical written: `False`
- Dashboard changed: `False`
- Noncanonical comparison written: `True`
- Strategy files unchanged: `True`
- Canonical existence unchanged: `True`

## Warning

- `NOT_FROZEN_E1R_V0_2`
- Candidate total return: `89.81714654548038`
- Frozen total return: `116.7435999134756`
- Gap: `26.926453367995222` pct

## Validations

```json
{
  "noncanonical_only": true,
  "e1r_one_row_per_date": true,
  "e1r_not_symbol_level": true,
  "e1r_not_diagnostic_only": true,
  "e1r_row_count_ge_1000": true,
  "shared_dates_ge_1000": true,
  "frozen_metric_exact_match": false,
  "explicit_not_frozen_warning_required": true
}
```

## Summaries

```json
{
  "e1": {
    "row_count": 1259,
    "parseable_rows": 1259,
    "unique_dates": 1259,
    "date_start": "2021-06-11",
    "date_end": "2026-06-16",
    "max_rows_per_date": 1,
    "one_row_per_date": true,
    "symbol_row_count": 0,
    "diagnostic_only_row_count": 0,
    "not_symbol_level": true,
    "not_diagnostic_only": true,
    "first_equity": 100000.0,
    "last_equity": 189815.69,
    "total_return_pct_from_rows": 89.81569,
    "max_drawdown_pct_from_rows": 26.58666092538411,
    "first_row_keys": [
      "cash",
      "daily_return",
      "daily_return_pct",
      "date",
      "equity",
      "market_state",
      "market_value",
      "n_positions",
      "portfolio_value",
      "source_row_keys",
      "strategy_indexed"
    ],
    "first_row": {
      "date": "2021-06-11",
      "equity": 100000.0,
      "portfolio_value": 100000.0,
      "strategy_indexed": 100.0,
      "cash": 100000.0,
      "market_value": null,
      "n_positions": null,
      "daily_return": null,
      "daily_return_pct": 0.0,
      "market_state": "ALLOW",
      "source_row_keys": [
        "cash",
        "daily_return_pct",
        "date",
        "drawdown_pct",
        "e1r_active_mode",
        "event",
        "exposure_pct",
        "market_gate_state",
        "open_positions_count",
        "pending_orders_count",
        "positions_value",
        "risk_budget",
        "risk_budget_mode",
        "spx_close",
        "spx_day_return_pct",
        "spx_ma50",
        "spx_regime",
        "total_equity"
      ]
    },
    "last_row": {
      "date": "2026-06-16",
      "equity": 189815.69,
      "portfolio_value": 189815.69,
      "strategy_indexed": 189.81569000000002,
      "cash": 60493.25,
      "market_value": null,
      "n_positions": null,
      "daily_return": null,
      "daily_return_pct": -1.66,
      "market_state": "ALLOW",
      "source_row_keys": [
        "cash",
        "daily_return_pct",
        "date",
        "drawdown_pct",
        "e1r_active_mode",
        "event",
        "exposure_pct",
        "market_gate_state",
        "open_positions_count",
        "pending_orders_count",
        "positions_value",
        "risk_budget",
        "risk_budget_mode",
        "spx_close",
        "spx_day_return_pct",
        "spx_ma50",
        "spx_regime",
        "total_equity"
      ]
    }
  },
  "e1r_direct_composed": {
    "row_count": 1258,
    "parseable_rows": 1258,
    "unique_dates": 1258,
    "date_start": "2021-06-14",
    "date_end": "2026-06-16",
    "max_rows_per_date": 1,
    "one_row_per_date": true,
    "symbol_row_count": 0,
    "diagnostic_only_row_count": 0,
    "not_symbol_level": true,
    "not_diagnostic_only": true,
    "first_equity": 99900.4,
    "last_equity": 189817.146545481,
    "total_return_pct_from_rows": 90.00639291282218,
    "max_drawdown_pct_from_rows": 26.586544760596375,
    "first_row_keys": [
      "core_return",
      "core_return_pct",
      "daily_return",
      "daily_return_pct",
      "date",
      "drawdown",
      "drawdown_pct",
      "equity",
      "interval_end_date",
      "interval_start_date",
      "sidecar_active",
      "sidecar_gross_exposure",
      "sidecar_return",
      "sidecar_return_pct",
      "sidecar_selected_count",
      "sideways_subclass",
      "spx_regime",
      "spx_return",
      "spx_return_pct",
      "total_equity"
    ],
    "first_row": {
      "date": "2021-06-14",
      "interval_start_date": "2021-06-11",
      "interval_end_date": "2021-06-14",
      "total_equity": 99900.4,
      "equity": 99900.4,
      "daily_return": -0.0009959999999999969,
      "daily_return_pct": -0.09959999999999969,
      "drawdown": -0.000996000000000108,
      "drawdown_pct": -0.09960000000001079,
      "core_return": -0.000996,
      "core_return_pct": -0.0996,
      "sidecar_return": 0.0,
      "sidecar_return_pct": 0.0,
      "spx_return": 0.0018152018879837861,
      "spx_return_pct": 0.1815201887983786,
      "spx_regime": "UPTREND",
      "sideways_subclass": "NO_SUBCLASS",
      "sidecar_active": false,
      "sidecar_selected_count": null,
      "sidecar_gross_exposure": null
    },
    "last_row": {
      "date": "2026-06-16",
      "interval_start_date": "2026-06-15",
      "interval_end_date": "2026-06-16",
      "total_equity": 189817.146545481,
      "equity": 189817.146545481,
      "daily_return": -0.016599999999999948,
      "daily_return_pct": -1.6599999999999948,
      "drawdown": -0.027172796902710572,
      "drawdown_pct": -2.717279690271057,
      "core_return": -0.0166,
      "core_return_pct": -1.66,
      "sidecar_return": 0.0,
      "sidecar_return_pct": 0.0,
      "spx_return": -0.005684179556029401,
      "spx_return_pct": -0.5684179556029401,
      "spx_regime": "UPTREND",
      "sideways_subclass": "NO_SUBCLASS",
      "sidecar_active": false,
      "sidecar_selected_count": null,
      "sidecar_gross_exposure": null
    }
  },
  "shared_dates": {
    "count": 1258,
    "date_start": "2021-06-14",
    "date_end": "2026-06-16"
  }
}
```

## Metrics

```json
{
  "frozen_target": {
    "total_return_pct": 116.7435999134756,
    "spx_return_pct": 76.844174428316,
    "alpha_pct": 39.89942548515961,
    "max_drawdown_pct": 25.904809362815108,
    "profit_factor": 1.1919630955509348,
    "sharpe_ratio": 0.7957270568329264
  },
  "candidate": {
    "total_return_pct": 89.81714654548038,
    "spx_return_pct": 76.844174428316,
    "alpha_pct": 12.972972117164394,
    "max_drawdown_pct": 26.586544760596375,
    "profit_factor": 1.1518254290657277,
    "sharpe_ratio": 0.7399161307043354
  },
  "diffs_abs": {
    "total_return_pct": 26.926453367995222,
    "spx_return_pct": 0.0,
    "alpha_pct": 26.926453367995215,
    "max_drawdown_pct": 0.6817353977812672,
    "profit_factor": 0.04013766648520711,
    "sharpe_ratio": 0.055810926128591065
  }
}
```

## Conclusion

- `DIRECT_COMPOSED_CANDIDATE_CURVE_VALID_BUT_NOT_FROZEN_E1R`
- Recommended: Use this noncanonical curve for engineering validation only; continue frozen core recovery separately.

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-4B-0N`: Prepare dashboard research candidate curve or continue frozen core recovery
- Recommended action: Use this noncanonical curve for engineering validation only; continue frozen core recovery separately.

