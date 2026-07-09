# Stage 3.8E-2F-2C-4C-10F-4B-0L Direct Compose Candidate

Generated At: `2026-07-09T10:49:33.423605+00:00`

## Status

- Status: `E1R_DIRECT_COMPOSE_CANDIDATE_COMPLETE_NONCANONICAL`
- E1R canonical written: `False`
- Noncanonical candidate written: `True`
- Strategy files unchanged: `True`
- Canonical existence unchanged: `True`

## Metrics

```json
{
  "result_metrics": {
    "total_return_pct": 89.81714654548038,
    "spx_return_pct": 76.844174428316,
    "alpha_pct": 12.972972117164394,
    "max_drawdown_pct": 26.586544760596375,
    "profit_factor": 1.1518254290657277,
    "sharpe_ratio": 0.7399161307043354
  },
  "target_metrics": {
    "total_return_pct": 116.7435999134756,
    "spx_return_pct": 76.844174428316,
    "alpha_pct": 39.89942548515961,
    "max_drawdown_pct": 25.904809362815108,
    "profit_factor": 1.1919630955509348,
    "sharpe_ratio": 0.7957270568329264
  },
  "diffs_abs": {
    "total_return_pct": 26.926453367995222,
    "spx_return_pct": 0.0,
    "alpha_pct": 26.926453367995215,
    "max_drawdown_pct": 0.6817353977812672,
    "profit_factor": 0.04013766648520711,
    "sharpe_ratio": 0.055810926128591065
  },
  "frozen_metric_exact_match": false
}
```

## Input Summaries

```json
{
  "core": {
    "row_count": 1259,
    "unique_dates": 1259,
    "date_start": "2021-06-11",
    "date_end": "2026-06-16",
    "first_keys": [
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
  "sidecar": {
    "row_count": 1260,
    "unique_dates": 1260,
    "date_start": "2021-06-11",
    "date_end": "2026-06-17",
    "first_keys": [
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
    "first_row": {
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
    "last_row": {
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

- `DIRECT_COMPOSE_SUCCEEDED_BUT_DID_NOT_MATCH_FROZEN_E1R_METRICS`
- Recommended: Use this result to quantify gap; frozen E1R core input is still not equal to current E1 5Y core.

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-4B-0M`: Validate direct composed noncanonical candidate or recover frozen core input
- Recommended action: Use this result to quantify gap; frozen E1R core input is still not equal to current E1 5Y core.

