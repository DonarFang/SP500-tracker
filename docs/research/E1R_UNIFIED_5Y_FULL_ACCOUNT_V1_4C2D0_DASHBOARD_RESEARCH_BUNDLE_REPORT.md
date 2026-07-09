# E1R Unified 5Y — 4C-2D-0 Dashboard Research Bundle

Generated At: `2026-07-09T12:28:51.249392+00:00`

## Conclusion

- `E1R_ROW_DERIVED_ACCOUNT_CURVE_READY_FOR_RESEARCH_DASHBOARD_WIRING`
- Recommended: Proceed to 4C-2D-1: wire this bundle into Research & Backtest tab with explicit Account-level only / Trade metrics not validated labels.

## Metrics

```json
{
  "first_date": "2021-06-11",
  "last_date": "2026-06-16",
  "row_count": 1259,
  "total_return_pct": 65.71578,
  "spx_total_return_pct": 76.84,
  "alpha_pct": -11.124220000000008,
  "cagr_pct": 10.638841693504443,
  "max_drawdown_pct": 52.18893,
  "sharpe_ratio": 0.5017379738002563,
  "annualized_vol_pct": 28.012222610626974,
  "final_equity": 165715.78,
  "initial_equity": 100000.0,
  "final_exposure_pct": 100.0
}
```

## Validation

```json
{
  "bundle_status_ready": true,
  "row_count_ge_1000": true,
  "has_curve_rows": true,
  "uses_row_derived_metrics": true,
  "engine_metrics_rejected": true,
  "trade_metrics_rejected": true,
  "covers_uptrend": true,
  "covers_sideways": true,
  "covers_downtrend": true
}
```

## Warnings

```json
[
  "Account-level row-derived equity curve is usable for research display.",
  "Trade metrics are not validated and must not be shown as official performance.",
  "Engine-reported result/summary metrics are rejected for official use.",
  "This bundle should not overwrite frozen E1 metrics."
]
```
