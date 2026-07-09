# E1R Unified 5Y Full Account V1 — 4C-2C-2 Row-Derived Metrics

Generated At: `2026-07-09T12:24:16.248508+00:00`

## Conclusion

- `ACCOUNT_LEVEL_ROW_DERIVED_CURVE_USABLE_FOR_RESEARCH_DISPLAY_ONLY`
- Recommended: Patch dashboard/research labels to use row-derived metrics only; separately fix engine SIM_END/effective_exit trade contract before any trade-level claims.

## Row-Derived Metrics

```json
{
  "metric_source": "daily_equity_records.total_equity",
  "reported_engine_metrics_status": "REJECTED_FOR_OFFICIAL_USE_METRIC_LAYER_USED_CASH_AS_FINAL_EQUITY",
  "trade_metrics_status": "NOT_VALIDATED_SIM_END_EFFECTIVE_EXIT_ZERO_RETURN_MINUS_100",
  "first_date": "2021-06-11",
  "last_date": "2026-06-16",
  "row_count": 1259,
  "unique_dates": 1259,
  "one_row_per_date": true,
  "first_equity": 100000.0,
  "last_equity": 165715.78,
  "total_return_pct": 65.71578,
  "spx_total_return_pct": 76.84,
  "alpha_pct": -11.124220000000008,
  "cagr_pct": 10.638841693504443,
  "max_drawdown_pct": 52.18893,
  "sharpe_ratio_row_derived": 0.5017379738002563,
  "annualized_vol_pct_row_derived": 28.012222610626974,
  "final_cash": 0.16,
  "final_positions_value": 165715.61,
  "final_cash_plus_positions": 165715.77,
  "final_exposure_pct": 100.0,
  "regime_counts": {
    "UPTREND": 860,
    "SIDEWAYS": 241,
    "DOWNTREND": 158
  },
  "active_mode_counts": {
    "UPTREND_EMERGING_CONFIRMED_ENABLED": 860,
    "SIDEWAYS_QUALITY_BREAKOUT_ONLY": 241,
    "DOWNTREND_EXCEPTION_ONLY": 158
  },
  "risk_budget_mode_counts": {
    "UPTREND_RISK_ON": 860,
    "SIDEWAYS_LIMITED": 241,
    "DOWNTREND_DEFENSIVE": 158
  },
  "cash_plus_positions_break_count": 0,
  "cash_plus_positions_break_samples": []
}
```

## Engine Metrics Rejected

```json
{
  "result_total_return_pct": -100.0,
  "result_final_equity": 0.16,
  "result_max_drawdown_pct": 100.0,
  "summary_total_return_pct": -100.0,
  "summary_final_equity": 0.16,
  "summary_max_drawdown_pct": 100.0
}
```

## Trade Layer Audit

```json
{
  "trade_count": 10,
  "exit_counter": {
    "SIM_END": 10
  },
  "return_counter": {
    "-100.0": 10
  },
  "effective_exit_counter": {
    "0.0": 10
  },
  "sim_end_effective_exit_zero_count": 10,
  "suspicious_samples": [
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
      "exit_type": "SIM_END"
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
      "exit_type": "SIM_END"
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
      "exit_type": "SIM_END"
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
      "exit_type": "SIM_END"
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
      "exit_type": "SIM_END"
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
      "exit_type": "SIM_END"
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
      "exit_type": "SIM_END"
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
      "exit_type": "SIM_END"
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
      "exit_type": "SIM_END"
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
      "exit_type": "SIM_END"
    }
  ]
}
```
