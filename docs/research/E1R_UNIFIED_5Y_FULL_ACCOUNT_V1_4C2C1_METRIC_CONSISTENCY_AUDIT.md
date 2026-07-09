# E1R Unified 5Y Full Account V1 — 4C-2C-1 Metric Consistency Audit

Generated At: `2026-07-09T12:19:59.020772+00:00`

## Diagnosis

- `METRIC_LAYER_APPEARS_TO_USE_CASH_AS_FINAL_EQUITY`
- Recommended: Do not use reported result metrics. Recompute official metrics from daily_equity_records total_equity, then patch exporter/report labels.

## Reported vs Row-Derived Metrics

```json
{
  "reported_metrics": {
    "result_total_return_pct": -100.0,
    "result_final_equity": 0.16,
    "result_max_drawdown_pct": 100.0,
    "summary_total_return_pct": -100.0,
    "summary_final_equity": 0.16,
    "summary_max_drawdown_pct": 100.0
  },
  "row_derived_metrics": {
    "first_equity": 100000.0,
    "last_equity": 165715.78,
    "total_return_pct": 65.71578,
    "max_drawdown_pct": 52.18893
  },
  "consistency_checks": {
    "result_exists": true,
    "curve_exists": true,
    "summary_exists": true,
    "daily_records_count": 1259,
    "curve_rows_count": 1259,
    "first_daily_equity": 100000.0,
    "last_daily_equity": 165715.78,
    "last_daily_cash": 0.16,
    "last_daily_positions_value": 165715.61,
    "last_cash_plus_positions": 165715.77,
    "row_derived_total_return_pct": 65.71578,
    "row_derived_max_drawdown_pct": 52.18893,
    "reported_result_final_equity_equals_last_total_equity": false,
    "reported_result_final_equity_equals_last_cash": true,
    "reported_return_matches_row_return": false,
    "reported_maxdd_matches_row_maxdd": false
  }
}
```

## Trade Audit

```json
{
  "trade_count": 10,
  "exit_counter": {
    "SIM_END": 10
  },
  "return_counter": {
    "-100.0": 10
  },
  "dominant_regime_counter": {
    "UPTREND": 10
  },
  "suspicious_trade_count": 10,
  "suspicious_trade_samples": [
    {
      "symbol": "ANET",
      "entry_date": "2021-06-14",
      "exit_date": "2026-06-18",
      "entry_price": 22.75,
      "avg_cost": 45.61,
      "exit_price": 168.01,
      "effective_exit": 0.0,
      "return_pct": -100.0,
      "is_sim_end": true,
      "exit_signal": "SIM_END",
      "exit_type": "SIM_END",
      "dominant_regime": "UPTREND",
      "size_units_at_exit": 1.0
    },
    {
      "symbol": "NET",
      "entry_date": "2021-06-15",
      "exit_date": "2026-06-18",
      "entry_price": 95.64,
      "avg_cost": 186.88,
      "exit_price": 230.97,
      "effective_exit": 0.0,
      "return_pct": -100.0,
      "is_sim_end": true,
      "exit_signal": "SIM_END",
      "exit_type": "SIM_END",
      "dominant_regime": "UPTREND",
      "size_units_at_exit": 1.0
    },
    {
      "symbol": "TRGP",
      "entry_date": "2021-06-16",
      "exit_date": "2026-06-18",
      "entry_price": 43.02,
      "avg_cost": 88.32,
      "exit_price": 259.68,
      "effective_exit": 0.0,
      "return_pct": -100.0,
      "is_sim_end": true,
      "exit_signal": "SIM_END",
      "exit_type": "SIM_END",
      "dominant_regime": "UPTREND",
      "size_units_at_exit": 1.0
    },
    {
      "symbol": "RMD",
      "entry_date": "2021-06-17",
      "exit_date": "2026-06-18",
      "entry_price": 226.6,
      "avg_cost": 449.35,
      "exit_price": 193.94,
      "effective_exit": 0.0,
      "return_pct": -100.0,
      "is_sim_end": true,
      "exit_signal": "SIM_END",
      "exit_type": "SIM_END",
      "dominant_regime": "UPTREND",
      "size_units_at_exit": 1.0
    },
    {
      "symbol": "GNRC",
      "entry_date": "2021-06-18",
      "exit_date": "2026-06-18",
      "entry_price": 378.94,
      "avg_cost": 437.61,
      "exit_price": 265.66,
      "effective_exit": 0.0,
      "return_pct": -100.0,
      "is_sim_end": true,
      "exit_signal": "SIM_END",
      "exit_type": "SIM_END",
      "dominant_regime": "UPTREND",
      "size_units_at_exit": 1.0
    },
    {
      "symbol": "SHOP",
      "entry_date": "2021-06-22",
      "exit_date": "2026-06-18",
      "entry_price": 148.02,
      "avg_cost": 207.57,
      "exit_price": 113.23,
      "effective_exit": 0.0,
      "return_pct": -100.0,
      "is_sim_end": true,
      "exit_signal": "SIM_END",
      "exit_type": "SIM_END",
      "dominant_regime": "UPTREND",
      "size_units_at_exit": 1.0
    },
    {
      "symbol": "NVDA",
      "entry_date": "2021-06-23",
      "exit_date": "2026-06-18",
      "entry_price": 18.82,
      "avg_cost": 37.98,
      "exit_price": 207.41,
      "effective_exit": 0.0,
      "return_pct": -100.0,
      "is_sim_end": true,
      "exit_signal": "SIM_END",
      "exit_type": "SIM_END",
      "dominant_regime": "UPTREND",
      "size_units_at_exit": 1.0
    },
    {
      "symbol": "DDOG",
      "entry_date": "2021-06-24",
      "exit_date": "2026-06-18",
      "entry_price": 106.53,
      "avg_cost": 218.1,
      "exit_price": 231.11,
      "effective_exit": 0.0,
      "return_pct": -100.0,
      "is_sim_end": true,
      "exit_signal": "SIM_END",
      "exit_type": "SIM_END",
      "dominant_regime": "UPTREND",
      "size_units_at_exit": 1.0
    },
    {
      "symbol": "MSCI",
      "entry_date": "2021-06-25",
      "exit_date": "2026-06-18",
      "entry_price": 504.38,
      "avg_cost": 1015.47,
      "exit_price": 608.16,
      "effective_exit": 0.0,
      "return_pct": -100.0,
      "is_sim_end": true,
      "exit_signal": "SIM_END",
      "exit_type": "SIM_END",
      "dominant_regime": "UPTREND",
      "size_units_at_exit": 1.0
    },
    {
      "symbol": "CRWD",
      "entry_date": "2021-06-28",
      "exit_date": "2026-06-18",
      "entry_price": 253.24,
      "avg_cost": 417.34,
      "exit_price": 679.49,
      "effective_exit": 0.0,
      "return_pct": -100.0,
      "is_sim_end": true,
      "exit_signal": "SIM_END",
      "exit_type": "SIM_END",
      "dominant_regime": "UPTREND",
      "size_units_at_exit": 1.0
    }
  ]
}
```
