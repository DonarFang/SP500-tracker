# AE-step 1 — E1R CAPPED-ATR Formal 5Y Rebuild

Generated At: `2026-08-09T08:50:01.781443+00:00`
Elapsed Seconds: `1334.056214`

## Outputs

```json
{
  "result": "exports/e1r_unified_5y_full_account_v1_result.json",
  "curve": "exports/e1r_unified_5y_full_account_v1_equity_curve.json",
  "summary": "exports/e1r_unified_5y_full_account_v1_summary.json"
}
```

## Metrics

```json
{
  "total_return_pct": 212.69,
  "spx_total_return_pct": 76.84,
  "alpha_pct": 135.85,
  "cagr_pct": 25.59,
  "spx_cagr_pct": 12.07,
  "max_drawdown_pct": 25.66,
  "profit_factor": 2.36,
  "sharpe_ratio": 0.76,
  "win_rate_pct": 52.2,
  "number_of_trades": 92,
  "total_trades_all": 92,
  "avg_holding_days": 28.5,
  "avg_winner_pct": 14.32,
  "avg_loser_pct": -6.63,
  "exposure_pct": 69.2,
  "final_equity": 312687.26,
  "initial_capital": 100000.0,
  "status": "PASS",
  "sample_validity": {
    "is_valid": true,
    "sample_status": "VALID",
    "simulation_start_date": "2021-06-11",
    "simulation_end_date": "2026-06-18",
    "simulation_days": 1261,
    "total_trades": 92,
    "completed_trades": 89,
    "sim_end_trades": 3,
    "sim_end_ratio_pct": 3.3,
    "invalid_trades": 0,
    "minimum_required": {
      "sim_days": 252,
      "trades": 20,
      "sim_end_ratio_pct": 50,
      "invalid": 0
    }
  },
  "e1r_candidate_count": 8830,
  "e1r_uptrend_execution_enabled": true
}
```

## Validations

```json
{
  "full_run_completed": true,
  "has_daily_equity_records": true,
  "row_count_ge_1000": true,
  "one_row_per_date": true,
  "regime_wired_observed": true,
  "active_mode_observed": true,
  "covers_uptrend": true,
  "covers_sideways": true,
  "covers_downtrend": true,
  "cash_plus_positions_continuity_ok": true,
  "sample_validity": {
    "is_valid": true,
    "sample_status": "VALID",
    "simulation_start_date": "2021-06-11",
    "simulation_end_date": "2026-06-18",
    "simulation_days": 1261,
    "total_trades": 92,
    "completed_trades": 89,
    "sim_end_trades": 3,
    "sim_end_ratio_pct": 3.3,
    "invalid_trades": 0,
    "minimum_required": {
      "sim_days": 252,
      "trades": 20,
      "sim_end_ratio_pct": 50,
      "invalid": 0
    }
  }
}
```

## Record Summary

```json
{
  "row_count": 1259,
  "unique_dates": 1259,
  "date_start": "2021-06-11",
  "date_end": "2026-06-16",
  "max_rows_per_date": 1,
  "one_row_per_date": true,
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
  "subclass_counts": {
    "None": 1259
  },
  "non_null_regime_count": 1259,
  "non_null_active_mode_count": 1259,
  "cash_value_break_count": 0,
  "cash_value_break_samples": [],
  "first": {
    "date": "2021-06-11",
    "cash": 100000.0,
    "positions_value": 0.0,
    "total_equity": 100000.0,
    "daily_return_pct": 0.0,
    "drawdown_pct": 0.0,
    "exposure_pct": 0.0,
    "open_positions_count": 0,
    "uptrend_positions_count": 0,
    "sideways_positions_count": 0,
    "position_origin_counts": {
      "UPTREND": 0,
      "SIDEWAYS_MA_CONFLICT": 0
    },
    "sideways_positions_value": 0,
    "pending_orders_count": 0,
    "market_gate_state": "ALLOW",
    "spx_regime": "UPTREND",
    "e1r_active_mode": "UPTREND_EMERGING_CONFIRMED_ENABLED",
    "risk_budget_mode": "UPTREND_RISK_ON",
    "risk_budget": {
      "mode": "UPTREND_RISK_ON",
      "max_positions": 3,
      "max_total_exposure_pct": 100.0
    },
    "spx_close": 4247.44,
    "spx_ma50": 4166.29,
    "spx_day_return_pct": 0.1948,
    "event": "EOD_MARK_TO_MARKET"
  },
  "last": {
    "date": "2026-06-16",
    "cash": 77867.71,
    "positions_value": 232132.29,
    "total_equity": 310000.01,
    "daily_return_pct": -3.3054,
    "drawdown_pct": 6.8091,
    "exposure_pct": 74.88,
    "open_positions_count": 3,
    "uptrend_positions_count": 3,
    "sideways_positions_count": 0,
    "position_origin_counts": {
      "UPTREND": 3,
      "SIDEWAYS_MA_CONFLICT": 0
    },
    "sideways_positions_value": 0,
    "pending_orders_count": 1,
    "market_gate_state": "ALLOW",
    "spx_regime": "UPTREND",
    "e1r_active_mode": "UPTREND_EMERGING_CONFIRMED_ENABLED",
    "risk_budget_mode": "UPTREND_RISK_ON",
    "risk_budget": {
      "mode": "UPTREND_RISK_ON",
      "max_positions": 3,
      "max_total_exposure_pct": 100.0
    },
    "spx_close": 7511.35,
    "spx_ma50": 7285.21,
    "spx_day_return_pct": -0.5684,
    "event": "EOD_MARK_TO_MARKET"
  }
}
```

## Trade Summary

```json
{
  "trade_count": 92,
  "dominant_regime_counts": {
    "UPTREND": 59,
    "SIDEWAYS": 33
  },
  "first_trade": {
    "symbol": "TRGP",
    "entry_date": "2021-06-16",
    "exit_date": "2021-07-15",
    "entry_signal": "BUY",
    "exit_signal": "EXIT",
    "entry_price": 43.02,
    "avg_cost": 44.21,
    "exit_price": 38.81,
    "effective_exit": 37.83,
    "return_pct": -11.91,
    "max_gain_pct": -0.1,
    "max_drawdown_in_trade": 12.11,
    "holding_days": 21,
    "size_units_at_exit": 0.5,
    "leader_score_entry": 96.1,
    "relative_stop_triggered": false,
    "relative_stop_exec_date": null,
    "take_profit_triggered": false,
    "take_profit_exec_date": null,
    "realized_pnl_before_exit": -1559.94,
    "actions_during_trade": [
      "BUY",
      "BUY",
      "HOLD",
      "REDUCE",
      "REDUCE",
      "REDUCE",
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
      "REDUCE",
      "REDUCE",
      "REDUCE",
      "REDUCE",
      "REDUCE"
    ],
    "action_count": 22,
    "execution_model": "adverse_intraday_v1.0",
    "entry_adverse_gap_pct": 2.744,
    "exit_adverse_gap_pct": 2.538,
    "total_execution_drag_pct": 5.282,
    "is_sim_end": false,
    "entry_regime": "UPTREND",
    "entry_subclass": "NO_SUBCLASS",
    "entry_signal_date": "2021-06-15",
    "entry_signal_regime": null,
    "entry_signal_subclass": null,
    "entry_execution_date": "2021-06-16",
    "exit_regime": "UPTREND",
    "exit_subclass": "NO_SUBCLASS",
    "dominant_regime": "UPTREND",
    "entry_type": "E1R_UPTREND_CONFIRMED",
    "origin_branch": "UPTREND",
    "sideways_entry_rank": null,
    "sideways_entry_score": null,
    "entry_tradable_cash_base": null,
    "entry_sideways_total_budget": null,
    "entry_target_cash": null,
    "entry_shares": 751.3816321874776,
    "entry_execution_price": 44.205248086999994,
    "total_cost_basis": 33215.01145886243,
    "total_realized_pnl": -3956.048924884043,
    "regime_day_weights": {
      "UPTREND": 20
    },
    "exit_reason": "HARD_LOSS_STOP",
    "exit_reasons": [
      "HARD_LOSS_STOP"
    ],
    "exit_type": "NORMAL_EXIT",
    "exit_warning_log": [],
    "exit_warning_count": 0
  },
  "last_trade": {
    "symbol": "HUM",
    "entry_date": "2026-06-11",
    "exit_date": "2026-06-18",
    "entry_signal": "BUY",
    "exit_signal": "SIM_END",
    "entry_price": 364.46,
    "avg_cost": 373.07,
    "exit_price": 369.49,
    "effective_exit": 357.15,
    "return_pct": -4.27,
    "max_gain_pct": 1.93,
    "max_drawdown_in_trade": 0,
    "holding_days": 6,
    "size_units_at_exit": 1.0,
    "leader_score_entry": 97.0,
    "take_profit_triggered": false,
    "take_profit_exec_date": null,
    "realized_pnl_before_exit": 0.0,
    "actions_during_trade": [
      "BUY",
      "BUY",
      "BUY",
      "BUY",
      "BUY"
    ],
    "action_count": 5,
    "execution_model": "adverse_intraday_v1.0",
    "is_sim_end": true,
    "entry_regime": "UPTREND",
    "entry_subclass": "NO_SUBCLASS",
    "entry_signal_date": "2026-06-10",
    "entry_signal_regime": null,
    "entry_signal_subclass": null,
    "entry_execution_date": "2026-06-11",
    "exit_regime": "UPTREND",
    "exit_subclass": "NO_SUBCLASS",
    "dominant_regime": "UPTREND",
    "entry_type": "E1R_UPTREND_CONFIRMED",
    "origin_branch": "UPTREND",
    "sideways_entry_rank": null,
    "sideways_entry_score": null,
    "entry_tradable_cash_base": null,
    "entry_sideways_total_budget": null,
    "entry_target_cash": null,
    "entry_shares": 267.2339875982243,
    "entry_execution_price": 373.07269999999994,
    "total_cost_basis": 99697.70528503603,
    "total_realized_pnl": -4254.4212017011105,
    "regime_day_weights": {
      "UPTREND": 4
    },
    "exit_type": "SIM_END",
    "exit_warning_log": [],
    "exit_warning_count": 0
  }
}
```

## Conclusion

- `PASS_AE_STEP_1_CAPPED_ATR_FORMAL_5Y_REBUILD`
- Recommended: AE-step 1 complete; proceed only to AE-step 2 when authorized.
