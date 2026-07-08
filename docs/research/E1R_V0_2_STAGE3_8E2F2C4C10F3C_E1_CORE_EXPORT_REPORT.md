# Stage 3.8E-2F-2C-4C-10F-3C E1 Core Export Report

Generated At: `2026-07-08T12:49:02.440325+00:00`

## Status

- Status: `E1_5Y_CORE_CANONICAL_WRITTEN`
- Canonical E1 written: `True`
- Symbols loaded: `539`

## Validation

```json
{
  "row_count": 1259,
  "unique_dates": 1259,
  "date_start": "2021-06-11",
  "date_end": "2026-06-16",
  "one_row_per_date": true,
  "full_window": true,
  "capital_continuity_candidate": true,
  "chosen_shape": {
    "label": "root.daily_equity_records",
    "length": 1259,
    "keys": [
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
    ],
    "date_start": "2021-06-11",
    "date_end": "2026-06-16",
    "unique_dates": 1259,
    "max_rows_per_date": 1,
    "has_symbol_level_rows": false,
    "has_equity_or_portfolio_value": true,
    "one_row_per_date": true,
    "equity_count": 1259,
    "first_equity": 100000.0,
    "last_equity": 189815.69,
    "continuity_candidate": true
  }
}
```

## Input Summary

```json
{
  "symbols_loaded": 539,
  "symbols_rejected": 3,
  "rejected_sample": [
    {
      "symbol": "FDXF",
      "reason": "too_few_rows:17"
    },
    {
      "symbol": "Q",
      "reason": "too_few_rows:162"
    },
    {
      "symbol": "VIXY",
      "reason": "excluded_known_non_sp500_proxy"
    }
  ],
  "spx_dates": 1562,
  "spx_start": "2020-04-01",
  "spx_end": "2026-06-18",
  "ndx_loaded": true,
  "sox_loaded": true,
  "vix_loaded": false,
  "assumptions_source": "run_stateful_default"
}
```

## Candidate Shapes

```json
[
  {
    "label": "root.daily_records",
    "length": 41,
    "keys": [
      "cash",
      "date",
      "market_gate_state",
      "n_holdings",
      "pending_orders",
      "position_value",
      "spx_close",
      "spx_day_return_pct",
      "spx_ma50",
      "total_equity"
    ],
    "date_start": "2021-07-23",
    "date_end": "2026-05-05",
    "unique_dates": 41,
    "max_rows_per_date": 1,
    "has_symbol_level_rows": false,
    "has_equity_or_portfolio_value": true,
    "one_row_per_date": true,
    "equity_count": 41,
    "first_equity": 107406.23,
    "last_equity": 192510.02,
    "continuity_candidate": false
  },
  {
    "label": "root.daily_equity_records",
    "length": 1259,
    "keys": [
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
    ],
    "date_start": "2021-06-11",
    "date_end": "2026-06-16",
    "unique_dates": 1259,
    "max_rows_per_date": 1,
    "has_symbol_level_rows": false,
    "has_equity_or_portfolio_value": true,
    "one_row_per_date": true,
    "equity_count": 1259,
    "first_equity": 100000.0,
    "last_equity": 189815.69,
    "continuity_candidate": true
  },
  {
    "label": "root.trades",
    "length": 45,
    "keys": [
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
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "max_rows_per_date": null,
    "has_symbol_level_rows": true,
    "has_equity_or_portfolio_value": false,
    "one_row_per_date": false,
    "equity_count": 0,
    "first_equity": null,
    "last_equity": null,
    "continuity_candidate": false
  }
]
```
