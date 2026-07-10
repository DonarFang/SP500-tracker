# E1R 4C-2C-4E-ENGINE-H — Golden Master Trace Shape Audit

Generated At: `2026-07-10T10:46:58.422953+00:00`

## Purpose
Audit golden-master trace shape and define exact equivalence assertions for future UPTREND extraction.

## Policy
```json
{
  "strategy_logic_changed": false,
  "trace_audit_only": true,
  "backtest_engine_run": false,
  "full_5y_backtest_run": false,
  "forward_runner_run": false,
  "provider_extraction_run": false,
  "strategy_core_implemented": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "frozen_strategy_files_changed": false,
  "invalid_artifacts_used_as_source": false,
  "composer_used": false,
  "return_curve_stitching_used": false
}
```

## Row Counts
```json
{
  "daily_equity_records": 62,
  "daily_records": 2,
  "trades": 3,
  "equity_curve": 13,
  "e1r_candidates": 0,
  "invalid_trades": 0
}
```

## Trace Shape
```json
{
  "raw_result_keys": [
    "alpha_pct",
    "avg_execution_drag_pct",
    "avg_holding_days",
    "avg_loser_pct",
    "avg_winner_pct",
    "cagr_pct",
    "daily_equity_record_count",
    "daily_equity_records",
    "daily_records",
    "e1r_candidate_count",
    "e1r_candidates",
    "e1r_uptrend_execution_enabled",
    "entry_top_n",
    "equity_curve",
    "executed_exit_reason_distribution",
    "executed_reduce_reason_distribution",
    "execution_model",
    "exposure_pct",
    "final_equity",
    "initial_capital",
    "invalid_trades",
    "invalid_trades_count",
    "layer",
    "market_entry_gate",
    "max_drawdown_pct",
    "name",
    "number_of_trades",
    "p0_passed",
    "partial_take_profit",
    "pending_orders_executed",
    "pending_orders_skipped",
    "pending_signal_reason_distribution",
    "portfolio_action_distribution",
    "profit_factor",
    "rank_based_exit",
    "sample_validity",
    "sharpe_ratio",
    "sim_end_liquidation_record",
    "skipped_orders_by_reason",
    "spx_cagr_pct",
    "spx_curve",
    "spx_total_return_pct",
    "status",
    "strategy_controls",
    "strategy_variant",
    "total_return_pct",
    "total_trades_all",
    "trades",
    "version",
    "win_rate_pct"
  ],
  "row_counts": {
    "daily_equity_records": 62,
    "daily_records": 2,
    "trades": 3,
    "equity_curve": 13,
    "e1r_candidates": 0,
    "invalid_trades": 0
  },
  "daily_equity_records": {
    "fields": [
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
    "sample": [
      {
        "date": "2021-04-05",
        "cash": 100000.0,
        "positions_value": 0.0,
        "total_equity": 100000.0,
        "daily_return_pct": 0.0,
        "drawdown_pct": 0.0,
        "exposure_pct": 0.0,
        "open_positions_count": 0,
        "pending_orders_count": 0,
        "market_gate_state": "ALLOW",
        "spx_regime": null,
        "e1r_active_mode": null,
        "risk_budget_mode": null,
        "risk_budget": null,
        "spx_close": 4077.91,
        "spx_ma50": 3892.47,
        "spx_day_return_pct": 1.4438,
        "event": "EOD_MARK_TO_MARKET"
      },
      {
        "date": "2021-04-06",
        "cash": 80647.72,
        "positions_value": 9676.14,
        "total_equity": 90323.86,
        "daily_return_pct": -9.6761,
        "drawdown_pct": 9.6761,
        "exposure_pct": 10.71,
        "open_positions_count": 3,
        "pending_orders_count": 3,
        "market_gate_state": "ALLOW",
        "spx_regime": null,
        "e1r_active_mode": null,
        "risk_budget_mode": null,
        "risk_budget": null,
        "spx_close": 4073.94,
        "spx_ma50": 3897.12,
        "spx_day_return_pct": -0.0974,
        "event": "EOD_MARK_TO_MARKET"
      },
      {
        "date": "2021-04-07",
        "cash": 80647.72,
        "positions_value": 9578.94,
        "total_equity": 90226.66,
        "daily_return_pct": -0.1076,
        "drawdown_pct": 9.7733,
        "exposure_pct": 10.62,
        "open_positions_count": 3,
        "pending_orders_count": 0,
        "market_gate_state": "ALLOW",
        "spx_regime": null,
        "e1r_active_mode": null,
        "risk_budget_mode": null,
        "risk_budget": null,
        "spx_close": 4079.95,
        "spx_ma50": 3901.61,
        "spx_day_return_pct": 0.1475,
        "event": "EOD_MARK_TO_MARKET"
      }
    ],
    "required_audit": {
      "ok": true,
      "required": [
        "date",
        "cash",
        "total_equity",
        "positions_value",
        "open_positions_count",
        "market_gate_state",
        "spx_regime"
      ],
      "available": [
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
      "missing": [],
      "coverage": 1.0
    },
    "extended_audit": {
      "ok": true,
      "required": [
        "daily_return_pct",
        "drawdown_pct",
        "exposure_pct",
        "pending_orders_count",
        "risk_budget",
        "risk_budget_mode",
        "spx_close",
        "spx_day_return_pct",
        "spx_ma50"
      ],
      "available": [
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
      "missing": [],
      "coverage": 1.0
    }
  },
  "daily_records": {
    "fields": [
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
    "sample": [
      {
        "date": "2021-04-28",
        "cash": 74667.06,
        "position_value": 12972.09,
        "total_equity": 87639.15,
        "n_holdings": 3,
        "pending_orders": 2,
        "market_gate_state": "ALLOW",
        "spx_close": 4183.18,
        "spx_ma50": 3991.79,
        "spx_day_return_pct": -0.08
      },
      {
        "date": "2021-06-10",
        "cash": 71746.21,
        "position_value": 13497.2,
        "total_equity": 85243.42,
        "n_holdings": 3,
        "pending_orders": 3,
        "market_gate_state": "ALLOW",
        "spx_close": 4239.18,
        "spx_ma50": 4160.8,
        "spx_day_return_pct": 0.47
      }
    ]
  },
  "trades": {
    "fields": [
      "action_count",
      "actions_during_trade",
      "avg_cost",
      "dominant_regime",
      "effective_exit",
      "entry_date",
      "entry_price",
      "entry_regime",
      "entry_signal",
      "entry_type",
      "execution_model",
      "exit_date",
      "exit_price",
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
      "return_pct",
      "size_units_at_exit",
      "symbol",
      "take_profit_exec_date",
      "take_profit_triggered"
    ],
    "sample": [
      {
        "symbol": "AMAT",
        "entry_date": "2021-04-06",
        "exit_date": "2021-06-30",
        "entry_signal": "BUY",
        "exit_signal": "SIM_END",
        "entry_price": 136.91,
        "avg_cost": 266.42,
        "exit_price": 136.53,
        "effective_exit": 0.0,
        "return_pct": -100.0,
        "max_gain_pct": -48.61,
        "max_drawdown_in_trade": 0,
        "holding_days": 61,
        "size_units_at_exit": 1.5,
        "leader_score_entry": 96.0,
        "take_profit_triggered": false,
        "take_profit_exec_date": null,
        "realized_pnl_before_exit": 0.0,
        "actions_during_trade": [
          "BUY",
          "BUY",
          "BUY",
          "HOLD",
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
          "HOLD",
          "HOLD",
          "HOLD",
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
          "REDUCE",
          "REDUCE",
          "REDUCE",
          "REDUCE",
          "HOLD",
          "HOLD",
          "ADD",
          "ADD",
          "ADD",
          "HOLD",
          "HOLD",
          "HOLD",
          "HOLD",
          "HOLD",
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
          "REDUCE"
        ],
        "action_count": 63,
        "execution_model": "adverse_intraday_v1.0",
        "is_sim_end": true,
        "entry_regime": "N/A",
        "exit_regime": "N/A",
        "dominant_regime": "N/A",
        "entry_type": null,
        "regime_day_weights": {},
        "exit_type": "SIM_END",
        "exit_warning_log": [],
        "exit_warning_count": 0
      },
      {
        "symbol": "MHK",
        "entry_date": "2021-04-06",
        "exit_date": "2021-06-30",
        "entry_signal": "BUY",
        "exit_signal": "SIM_END",
        "entry_price": 201.19,
        "avg_cost": 399.93,
        "exit_price": 192.19,
        "effective_exit": 0.0,
        "return_pct": -100.0,
        "max_gain_pct": -42.56,
        "max_drawdown_in_trade": 0,
        "holding_days": 61,
        "size_units_at_exit": 1.5,
        "leader_score_entry": 95.7,
        "take_profit_triggered": false,
        "take_profit_exec_date": null,
        "realized_pnl_before_exit": 0.0,
        "actions_during_trade": [
          "BUY",
          "BUY",
          "ADD",
          "ADD",
          "HOLD",
          "HOLD",
          "ADD",
          "ADD",
          "HOLD",
          "HOLD",
          "HOLD",
          "HOLD",
          "REDUCE",
          "HOLD",
          "REDUCE",
          "HOLD",
          "HOLD",
          "ADD",
          "ADD",
          "BUY",
          "HOLD",
          "BUY",
          "BUY",
          "BUY",
          "BUY",
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
          "REDUCE",
          "REDUCE",
          "REDUCE",
          "REDUCE",
          "REDUCE",
          "REDUCE",
          "REDUCE",
          "EXIT",
          "EXIT",
          "EXIT",
          "EXIT",
          "EXIT",
          "EXIT",
          "EXIT",
          "EXIT",
          "EXIT",
          "EXIT"
        ],
        "action_count": 63,
        "execution_model": "adverse_intraday_v1.0",
        "is_sim_end": true,
        "entry_regime": "N/A",
        "exit_regime": "N/A",
        "dominant_regime": "N/A",
        "entry_type": null,
        "regime_day_weights": {},
        "exit_type": "SIM_END",
        "exit_warning_log": [],
        "exit_warning_count": 0
      },
      {
        "symbol": "DHI",
        "entry_date": "2021-04-06",
        "exit_date": "2021-06-30",
        "entry_signal": "BUY",
        "exit_signal": "SIM_END",
        "entry_price": 87.84,
        "avg_cost": 180.85,
        "exit_price": 85.86,
        "effective_exit": 0.0,
        "return_pct": -100.0,
        "max_gain_pct": -45.13,
        "max_drawdown_in_trade": 0,
        "holding_days": 61,
        "size_units_at_exit": 1.5,
        "leader_score_entry": 95.5,
        "take_profit_triggered": false,
        "take_profit_exec_date": null,
        "realized_pnl_before_exit": 0.0,
        "actions_during_trade": [
          "BUY",
          "BUY",
          "BUY",
          "HOLD",
          "HOLD",
          "HOLD",
          "HOLD",
          "HOLD",
          "HOLD",
          "HOLD",
          "BUY",
          "HOLD",
          "REDUCE",
          "REDUCE",
          "HOLD",
          "BUY",
          "ADD",
          "ADD",
          "ADD",
          "ADD",
          "HOLD",
          "HOLD",
          "HOLD",
          "HOLD",
          "HOLD",
          "HOLD",
          "ADD",
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
          "EXIT",
          "EXIT",
          "EXIT",
          "EXIT",
          "EXIT",
          "EXIT",
          "EXIT",
          "EXIT",
          "EXIT",
          "EXIT"
        ],
        "action_count": 63,
        "execution_model": "adverse_intraday_v1.0",
        "is_sim_end": true,
        "entry_regime": "N/A",
        "exit_regime": "N/A",
        "dominant_regime": "N/A",
        "entry_type": null,
        "regime_day_weights": {},
        "exit_type": "SIM_END",
        "exit_warning_log": [],
        "exit_warning_count": 0
      }
    ],
    "required_audit": {
      "ok": true,
      "required": [
        "symbol",
        "entry_date",
        "entry_price",
        "exit_date",
        "exit_price",
        "entry_regime",
        "exit_regime",
        "entry_signal",
        "exit_signal",
        "return_pct",
        "holding_days",
        "actions_during_trade"
      ],
      "available": [
        "action_count",
        "actions_during_trade",
        "avg_cost",
        "dominant_regime",
        "effective_exit",
        "entry_date",
        "entry_price",
        "entry_regime",
        "entry_signal",
        "entry_type",
        "execution_model",
        "exit_date",
        "exit_price",
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
        "return_pct",
        "size_units_at_exit",
        "symbol",
        "take_profit_exec_date",
        "take_profit_triggered"
      ],
      "missing": [],
      "coverage": 1.0
    },
    "actions_during_trade_audit": {
      "actions_during_trade_available": false,
      "action_row_count": 0,
      "action_shape_count": 0,
      "action_shapes": {},
      "action_sample": [],
      "action_fields": []
    }
  },
  "equity_curve": {
    "type": "list",
    "sample": [
      100000.0,
      88822.0,
      88690.27,
      89160.79,
      87936.05
    ]
  },
  "e1r_candidates": {
    "fields": [],
    "sample": [],
    "required_audit": {
      "ok": false,
      "required": [
        "date",
        "symbol",
        "leader_score",
        "leader_rank",
        "rs_score",
        "trend_health"
      ],
      "available": [],
      "missing": [
        "date",
        "symbol",
        "leader_score",
        "leader_rank",
        "rs_score",
        "trend_health"
      ],
      "coverage": 0.0
    }
  }
}
```

## Equivalence Assertions
```json
[
  {
    "name": "daily_account_date_sequence",
    "tier": "T0_REQUIRED",
    "status": "ASSERTABLE",
    "fields": [
      "daily_equity_records.date"
    ],
    "source_section": "raw_result.daily_equity_records",
    "tolerance": "exact sequence match",
    "hard_fail": true,
    "notes": "New engine must generate the same daily dates for the same short-window baseline."
  },
  {
    "name": "daily_total_equity_cash_positions",
    "tier": "T0_REQUIRED",
    "status": "ASSERTABLE",
    "fields": [
      "daily_equity_records.cash",
      "daily_equity_records.positions_value",
      "daily_equity_records.total_equity"
    ],
    "source_section": "raw_result.daily_equity_records",
    "tolerance": "absolute <= 0.01 or relative <= 1e-6",
    "hard_fail": true,
    "notes": "Accounting identity and daily equity must match after extraction."
  },
  {
    "name": "daily_open_positions_count",
    "tier": "T0_REQUIRED",
    "status": "ASSERTABLE",
    "fields": [
      "daily_equity_records.open_positions_count"
    ],
    "source_section": "raw_result.daily_equity_records",
    "tolerance": "exact integer match; always <= 3",
    "hard_fail": true,
    "notes": "Max3 account contract must be preserved."
  },
  {
    "name": "daily_market_gate_state",
    "tier": "T0_REQUIRED",
    "status": "ASSERTABLE",
    "fields": [
      "daily_equity_records.market_gate_state"
    ],
    "source_section": "raw_result.daily_equity_records",
    "tolerance": "exact string match",
    "hard_fail": true,
    "notes": "Market gate behavior must not drift during extraction."
  },
  {
    "name": "daily_spx_regime",
    "tier": "T0_REQUIRED",
    "status": "ASSERTABLE",
    "fields": [
      "daily_equity_records.spx_regime"
    ],
    "source_section": "raw_result.daily_equity_records",
    "tolerance": "exact string match",
    "hard_fail": true,
    "notes": "Regime attribution must remain aligned."
  },
  {
    "name": "trade_lifecycle_symbol_dates",
    "tier": "T1_REQUIRED",
    "status": "ASSERTABLE",
    "fields": [
      "trades.symbol",
      "trades.entry_date",
      "trades.exit_date",
      "trades.entry_price",
      "trades.exit_price"
    ],
    "source_section": "raw_result.trades",
    "tolerance": "symbol/date exact; price absolute <= 0.01",
    "hard_fail": true,
    "notes": "Trade lifecycle must match after extraction."
  },
  {
    "name": "trade_signals_and_reasons",
    "tier": "T1_REQUIRED",
    "status": "ASSERTABLE",
    "fields": [
      "trades.entry_signal",
      "trades.exit_signal",
      "trades.entry_regime",
      "trades.exit_regime"
    ],
    "source_section": "raw_result.trades",
    "tolerance": "exact match where available",
    "hard_fail": true,
    "notes": "Entry/exit reasons are available at trade level."
  },
  {
    "name": "actions_during_trade",
    "tier": "T2_PARTIAL",
    "status": "MISSING",
    "fields": [
      "trades.actions_during_trade"
    ],
    "source_section": "raw_result.trades[].actions_during_trade",
    "tolerance": "exact if action rows are sufficiently structured",
    "hard_fail": false,
    "notes": "Current golden master has no standalone action_trace section; only nested actions_during_trade may be available."
  },
  {
    "name": "daily_position_snapshot",
    "tier": "T2_PARTIAL",
    "status": "MISSING",
    "fields": [
      "per_day.positions_by_symbol"
    ],
    "source_section": "not available",
    "tolerance": "not assertable until trace instrumentation exists",
    "hard_fail": false,
    "notes": "Need trace instrumentation for strict per-symbol daily position equivalence."
  },
  {
    "name": "candidate_ranking_trace",
    "tier": "T3_OPTIONAL_FOR_EXTRACTION_BUT_REQUIRED_FOR_DEEP_AUDIT",
    "status": "MISSING",
    "fields": [
      "date",
      "symbol",
      "leader_score",
      "leader_rank",
      "rs_score",
      "trend_health"
    ],
    "source_section": "raw_result.e1r_candidates",
    "tolerance": "exact rank/date/symbol match if available",
    "hard_fail": false,
    "notes": "Current short window has e1r_candidate_count=0, so candidate/rank equivalence is not assertable from this golden master."
  },
  {
    "name": "pending_order_trace",
    "tier": "T3_OPTIONAL_FOR_EXTRACTION_BUT_REQUIRED_FOR_DEEP_AUDIT",
    "status": "MISSING",
    "fields": [
      "pending_order.date",
      "symbol",
      "action",
      "reason",
      "target_size"
    ],
    "source_section": "not available as standalone section",
    "tolerance": "not assertable until trace instrumentation exists",
    "hard_fail": false,
    "notes": "pending_orders_count exists, but standalone pending order rows are absent."
  }
]
```

## Instrumentation Gaps
```json
[
  {
    "name": "actions_during_trade",
    "tier": "T2_PARTIAL",
    "status": "MISSING",
    "fields": [
      "trades.actions_during_trade"
    ],
    "source_section": "raw_result.trades[].actions_during_trade",
    "tolerance": "exact if action rows are sufficiently structured",
    "hard_fail": false,
    "notes": "Current golden master has no standalone action_trace section; only nested actions_during_trade may be available."
  },
  {
    "name": "daily_position_snapshot",
    "tier": "T2_PARTIAL",
    "status": "MISSING",
    "fields": [
      "per_day.positions_by_symbol"
    ],
    "source_section": "not available",
    "tolerance": "not assertable until trace instrumentation exists",
    "hard_fail": false,
    "notes": "Need trace instrumentation for strict per-symbol daily position equivalence."
  },
  {
    "name": "candidate_ranking_trace",
    "tier": "T3_OPTIONAL_FOR_EXTRACTION_BUT_REQUIRED_FOR_DEEP_AUDIT",
    "status": "MISSING",
    "fields": [
      "date",
      "symbol",
      "leader_score",
      "leader_rank",
      "rs_score",
      "trend_health"
    ],
    "source_section": "raw_result.e1r_candidates",
    "tolerance": "exact rank/date/symbol match if available",
    "hard_fail": false,
    "notes": "Current short window has e1r_candidate_count=0, so candidate/rank equivalence is not assertable from this golden master."
  },
  {
    "name": "pending_order_trace",
    "tier": "T3_OPTIONAL_FOR_EXTRACTION_BUT_REQUIRED_FOR_DEEP_AUDIT",
    "status": "MISSING",
    "fields": [
      "pending_order.date",
      "symbol",
      "action",
      "reason",
      "target_size"
    ],
    "source_section": "not available as standalone section",
    "tolerance": "not assertable until trace instrumentation exists",
    "hard_fail": false,
    "notes": "pending_orders_count exists, but standalone pending order rows are absent."
  }
]
```

## Extraction Minimum
```json
{
  "can_start_uptrend_extraction_with_minimum_equivalence": true,
  "minimum_assertions": [
    "daily_account_date_sequence",
    "daily_total_equity_cash_positions",
    "daily_open_positions_count",
    "daily_market_gate_state",
    "daily_spx_regime",
    "trade_lifecycle_symbol_dates",
    "trade_signals_and_reasons"
  ],
  "known_limits": [
    "No standalone action_trace section.",
    "No daily per-symbol position snapshot section.",
    "No candidate ranking trace in this short window.",
    "No standalone pending order trace."
  ]
}
```

## Assertions Artifact
- Path: `exports/e1r_engine/audit/e1r_engine_h_equivalence_assertions.json`
- SHA256: `1e1655617afdb4b46b6cb2b50918083f5a4c070a4f76fdeaf6981e5fc9a19812`

## Validations
```json
{
  "trace_shape_audit_defined": true,
  "golden_master_loaded": true,
  "strategy_logic_changed": false,
  "backtest_engine_run": false,
  "full_5y_backtest_run": false,
  "forward_runner_run": false,
  "provider_extraction_run": false,
  "strategy_core_implemented": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "strategy_files_unchanged": true,
  "invalid_artifacts_not_used_as_source": true,
  "composer_not_used": true,
  "return_curve_stitching_used": false,
  "engine_g_loaded": true,
  "daily_equity_records_available": true,
  "daily_equity_required_fields_available": true,
  "trades_available": true,
  "trade_required_fields_available": true,
  "action_trace_standalone_missing_identified": true,
  "position_snapshot_missing_identified": true,
  "candidate_trace_gap_identified": true,
  "equivalence_assertions_written": true,
  "minimum_extraction_assertions_defined": true,
  "strategy_core_extraction_not_run": true
}
```

## Decision
```json
{
  "trace_shape_audit_passed": true,
  "minimum_equivalence_available": true,
  "instrumentation_gap_count": 4,
  "hard_required_assertions": [
    "daily_account_date_sequence",
    "daily_total_equity_cash_positions",
    "daily_open_positions_count",
    "daily_market_gate_state",
    "daily_spx_regime",
    "trade_lifecycle_symbol_dates",
    "trade_signals_and_reasons"
  ],
  "missing_or_partial_assertions": [
    {
      "name": "actions_during_trade",
      "tier": "T2_PARTIAL",
      "status": "MISSING",
      "notes": "Current golden master has no standalone action_trace section; only nested actions_during_trade may be available."
    },
    {
      "name": "daily_position_snapshot",
      "tier": "T2_PARTIAL",
      "status": "MISSING",
      "notes": "Need trace instrumentation for strict per-symbol daily position equivalence."
    },
    {
      "name": "candidate_ranking_trace",
      "tier": "T3_OPTIONAL_FOR_EXTRACTION_BUT_REQUIRED_FOR_DEEP_AUDIT",
      "status": "MISSING",
      "notes": "Current short window has e1r_candidate_count=0, so candidate/rank equivalence is not assertable from this golden master."
    },
    {
      "name": "pending_order_trace",
      "tier": "T3_OPTIONAL_FOR_EXTRACTION_BUT_REQUIRED_FOR_DEEP_AUDIT",
      "status": "MISSING",
      "notes": "pending_orders_count exists, but standalone pending order rows are absent."
    }
  ],
  "strategy_core_extraction_allowed_now": false,
  "uptrend_provider_extraction_allowed_now": false,
  "sideways_branch_implementation_allowed_now": false,
  "full_5y_backtest_allowed_now": false,
  "forward_runner_allowed_now": false,
  "recommended_next_stage": "4C-2C-4E-ENGINE-I",
  "conclusion": "TRACE_SHAPE_AUDIT_PASS_READY_FOR_UPTREND_EXTRACTION_PLAN",
  "recommended_next_action": "Proceed to 4C-2C-4E-ENGINE-I: create UPTREND extraction plan against the locked equivalence assertions. Do not implement extracted strategy code yet.",
  "engineering_rule": "UPTREND extraction must be judged first by T0/T1 assertions. T2/T3 gaps are known and must not be hidden; add instrumentation later if strict candidate/order trace is required."
}
```
