# E1R 4C-2C-4E-D3 — UPTREND Runtime Equivalence Audit

Generated At: `2026-07-10T03:37:07.466070+00:00`

## Purpose

Audit whether `src/oos/tracking_engine.py::run_oos_day` is equivalent to `src/engine/backtest.py::run_stateful_simulation` for official UPTREND provider use.

## Policy
```json
{
  "strategy_logic_changed": false,
  "backtest_engine_full_run": false,
  "candidate_runtime_execution_run": false,
  "full_5y_backtest_run": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "frozen_strategy_files_changed": false,
  "invalid_artifacts_used_as_source": false,
  "composer_used": false,
  "return_curve_stitching_used": false
}
```

## Validations
```json
{
  "audit_only_no_full_5y": true,
  "backtest_engine_full_run": false,
  "candidate_runtime_execution_run": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "strategy_files_unchanged": true,
  "invalid_artifacts_not_used_as_source": true,
  "composer_not_used": true,
  "return_curve_stitching_not_used": true,
  "d2b_report_loaded": true,
  "baseline_function_loaded": true,
  "candidate_function_loaded": true,
  "equivalence_matrix_generated": true,
  "trade_decision_helpers_audited": true,
  "provider_not_locked_if_equivalence_failed": true,
  "implementation_not_allowed_yet": true,
  "decision_generated": true
}
```

## Baseline Summary
```json
{
  "path": "src/engine/backtest.py",
  "name": "run_stateful_simulation",
  "line_count": 1724,
  "features": {
    "exists": true,
    "path": "src/engine/backtest.py",
    "name": "run_stateful_simulation",
    "args": [
      "symbols",
      "prices_map",
      "dates_map",
      "spx_prices",
      "spx_dates",
      "ohlc_map",
      "assumptions",
      "step",
      "min_history",
      "market_score_default",
      "sim_start_date",
      "sim_end_date",
      "ndx_prices",
      "ndx_dates",
      "sox_prices",
      "sox_dates",
      "vix_prices",
      "vix_dates"
    ],
    "line_count": 1724,
    "has_candidate_terms": true,
    "takes_precomputed_leaders": false,
    "generates_leaders_from_prices_map": true,
    "has_buy_logic": true,
    "has_add_logic": true,
    "has_reduce_logic": true,
    "has_exit_logic": true,
    "has_hold_logic": true,
    "has_market_gate": true,
    "takes_market_state": false,
    "has_max_positions": true,
    "has_open_positions_count": true,
    "has_cash_state": true,
    "has_positions_state": true,
    "has_total_equity": true,
    "has_daily_mark_to_market": true,
    "has_signal_execute_dates": false,
    "references_invalid_artifacts": false,
    "calls_run_stateful_simulation": false,
    "writes_files_or_state": false,
    "imports_or_uses_oos_state": true,
    "contains_sidecar": false
  },
  "action_shapes": {
    "action_like_dict_count": 16,
    "literal_action_counts": {
      "BUY": 3,
      "ADD": 1,
      "TP_REDUCE": 1
    },
    "samples": [
      {
        "line": 2236,
        "keys": [
          "date",
          "cash",
          "positions_value",
          "total_equity",
          "open_positions_count",
          "sim_end_trades",
          "spx_regime",
          "e1r_active_mode",
          "risk_budget_mode",
          "event"
        ],
        "literal_action": null,
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 1515,
        "keys": [
          "date",
          "cash",
          "positions_value",
          "total_equity",
          "daily_return_pct",
          "drawdown_pct",
          "exposure_pct",
          "open_positions_count",
          "pending_orders_count",
          "market_gate_state",
          "spx_regime",
          "e1r_active_mode",
          "risk_budget_mode",
          "risk_budget",
          "spx_close",
          "spx_ma50",
          "spx_day_return_pct",
          "event"
        ],
        "literal_action": null,
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 1589,
        "keys": [
          "symbol",
          "action",
          "trend_state",
          "momentum_score",
          "rs_score",
          "leader_score",
          "trend_health",
          "close_t",
          "ma20",
          "ma20_slope",
          "ma50",
          "ma50_slope",
          "rs_prev20",
          "rs_20d_improvement",
          "momentum_acceleration",
          "e1r_entry_type",
          "e1r_uptrend_emerging_eligible",
          "e1r_uptrend_confirmed_eligible",
          "e1r_entry_reason"
        ],
        "literal_action": null,
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 2198,
        "keys": [
          "symbol",
          "entry_date",
          "exit_date",
          "entry_signal",
          "exit_signal",
          "entry_price",
          "avg_cost",
          "exit_price",
          "effective_exit",
          "return_pct",
          "max_gain_pct",
          "max_drawdown_in_trade",
          "holding_days",
          "size_units_at_exit",
          "leader_score_entry",
          "take_profit_triggered",
          "take_profit_exec_date",
          "realized_pnl_before_exit",
          "actions_during_trade",
          "action_count",
          "execution_model",
          "is_sim_end",
          "entry_regime",
          "exit_regime",
          "dominant_regime",
          "entry_type",
          "regime_day_weights",
          "exit_type",
          "exit_warning_log",
          "exit_warning_count"
        ],
        "literal_action": null,
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 2148,
        "keys": [
          "date",
          "cash",
          "position_value",
          "total_equity",
          "n_holdings",
          "pending_orders",
          "market_gate_state",
          "spx_close",
          "spx_ma50",
          "spx_day_return_pct"
        ],
        "literal_action": null,
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 1165,
        "keys": [
          "shares",
          "avg_cost",
          "size_units",
          "entry_close_ref",
          "entry_date",
          "entry_sig_date",
          "entry_signal",
          "e1r_entry_type",
          "highest_close",
          "min_close_since_entry",
          "current_close",
          "leader_score_entry",
          "entry_spx",
          "relative_stop_triggered",
          "relative_stop_signal_date",
          "relative_stop_exec_date",
          "take_profit_triggered",
          "take_profit_signal_date",
          "take_profit_exec_date",
          "realized_pnl",
          "realized_cost_basis",
          "action_history",
          "ls60_reduce_triggered",
          "entry_regime",
          "entry_type",
          "regime_day_weights"
        ],
        "literal_action": null,
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 1789,
        "keys": [
          "sym",
          "action",
          "signal_date",
          "ls",
          "close_t",
          "entry_rank",
          "strategy",
          "entry_mode",
          "primary_reason",
          "reasons",
          "e1r_entry_type",
          "target_size_units"
        ],
        "literal_action": "BUY",
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 2013,
        "keys": [
          "sym",
          "action",
          "signal_date",
          "ls",
          "close_t",
          "entry_rank",
          "strategy",
          "primary_reason",
          "reasons"
        ],
        "literal_action": null,
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 2048,
        "keys": [
          "sym",
          "action",
          "signal_date",
          "ls",
          "close_t",
          "entry_rank",
          "strategy",
          "primary_reason",
          "reasons",
          "e1r_entry_type",
          "add_size_units"
        ],
        "literal_action": "ADD",
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 1671,
        "keys": [
          "date",
          "symbol",
          "spx_regime",
          "e1r_entry_type",
          "e1r_uptrend_emerging_eligible",
          "e1r_uptrend_confirmed_eligible",
          "leader_rank",
          "leader_score",
          "rs_score",
          "rs_prev20",
          "rs_20d_improvement",
          "momentum_score",
          "momentum_acceleration",
          "trend_health",
          "close",
          "ma20",
          "ma50",
          "ma20_slope",
          "ma50_slope",
          "reasons",
          "diagnostic_only"
        ],
        "literal_action": null,
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 1879,
        "keys": [
          "sym",
          "action",
          "signal_date",
          "ls",
          "close_t",
          "entry_rank",
          "strategy",
          "entry_mode",
          "primary_reason",
          "reasons"
        ],
        "literal_action": "BUY",
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 2083,
        "keys": [
          "sym",
          "action",
          "signal_date",
          "ls",
          "close_t",
          "entry_rank",
          "strategy"
        ],
        "literal_action": null,
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 2114,
        "keys": [
          "sym",
          "action",
          "signal_date",
          "ls",
          "close_t",
          "entry_rank",
          "strategy"
        ],
        "literal_action": "TP_REDUCE",
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 1274,
        "keys": [
          "symbol",
          "entry_date",
          "exit_date",
          "entry_signal",
          "exit_signal",
          "entry_price",
          "avg_cost",
          "exit_price",
          "effective_exit",
          "return_pct",
          "max_gain_pct",
          "max_drawdown_in_trade",
          "holding_days",
          "size_units_at_exit",
          "leader_score_entry",
          "relative_stop_triggered",
          "relative_stop_exec_date",
          "take_profit_triggered",
          "take_profit_exec_date",
          "realized_pnl_before_exit",
          "actions_during_trade",
          "action_count",
          "execution_model",
          "entry_adverse_gap_pct",
          "exit_adverse_gap_pct",
          "total_execution_drag_pct",
          "is_sim_end",
          "entry_regime",
          "exit_regime",
          "dominant_regime",
          "entry_type",
          "regime_day_weights",
          "exit_reason",
          "exit_reasons",
          "exit_type",
          "exit_warning_log",
          "exit_warning_count"
        ],
        "literal_action": null,
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 1836,
        "keys": [
          "sym",
          "action",
          "signal_date",
          "ls",
          "close_t",
          "entry_rank",
          "strategy",
          "entry_mode",
          "primary_reason",
          "reasons",
          "candidate_top_n"
        ],
        "literal_action": "BUY",
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 1934,
        "keys": [
          "date",
          "ls",
          "price",
          "ma50",
          "price_vs_ma50_pct",
          "ma50_slope",
          "market_state",
          "warning_day"
        ],
        "literal_action": null,
        "literal_reason": null,
        "literal_order_type": null
      }
    ]
  }
}
```

## Candidate Summary
```json
{
  "path": "src/oos/tracking_engine.py",
  "name": "run_oos_day",
  "line_count": 241,
  "features": {
    "exists": true,
    "path": "src/oos/tracking_engine.py",
    "name": "run_oos_day",
    "args": [
      "signal_date",
      "leaders",
      "prices",
      "market_state",
      "source",
      "data_date"
    ],
    "line_count": 241,
    "has_candidate_terms": true,
    "takes_precomputed_leaders": true,
    "generates_leaders_from_prices_map": false,
    "has_buy_logic": true,
    "has_add_logic": true,
    "has_reduce_logic": false,
    "has_exit_logic": true,
    "has_hold_logic": false,
    "has_market_gate": false,
    "takes_market_state": true,
    "has_max_positions": false,
    "has_open_positions_count": false,
    "has_cash_state": true,
    "has_positions_state": true,
    "has_total_equity": true,
    "has_daily_mark_to_market": true,
    "has_signal_execute_dates": true,
    "references_invalid_artifacts": false,
    "calls_run_stateful_simulation": false,
    "writes_files_or_state": true,
    "imports_or_uses_oos_state": true,
    "contains_sidecar": false
  },
  "action_shapes": {
    "action_like_dict_count": 11,
    "literal_action_counts": {
      "EXIT": 4,
      "BUY": 2
    },
    "samples": [
      {
        "line": 253,
        "keys": [
          "date",
          "source",
          "gate_open",
          "equity",
          "executed",
          "new_orders",
          "n_positions",
          "status"
        ],
        "literal_action": null,
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 233,
        "keys": [
          "event_id",
          "event_type",
          "date",
          "equity",
          "cash",
          "holdings_value",
          "n_positions",
          "gate_open",
          "source"
        ],
        "literal_action": null,
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 51,
        "keys": [
          "event_id",
          "event_type",
          "date",
          "initial_capital",
          "source",
          "strategy_id"
        ],
        "literal_action": null,
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 77,
        "keys": [
          "event_id",
          "event_type",
          "date",
          "symbol",
          "action",
          "fill_price",
          "units",
          "cost_rate",
          "source",
          "signal_provenance",
          "order_ref"
        ],
        "literal_action": "EXIT",
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 91,
        "keys": [
          "symbol",
          "action",
          "fill_price",
          "signal_provenance",
          "execution_provenance"
        ],
        "literal_action": "EXIT",
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 129,
        "keys": [
          "event_id",
          "event_type",
          "date",
          "signal_date",
          "symbol",
          "action",
          "fill_price",
          "units",
          "total_cost",
          "cost_rate",
          "source",
          "signal_provenance",
          "order_ref"
        ],
        "literal_action": null,
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 145,
        "keys": [
          "symbol",
          "action",
          "fill_price",
          "units",
          "total_cost",
          "signal_provenance",
          "execution_provenance"
        ],
        "literal_action": null,
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 179,
        "keys": [
          "event_id",
          "event_type",
          "date",
          "symbol",
          "action",
          "signal_reason",
          "leader_score",
          "execute_date",
          "source"
        ],
        "literal_action": "EXIT",
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 206,
        "keys": [
          "event_id",
          "event_type",
          "date",
          "symbol",
          "action",
          "rank",
          "leader_score",
          "rs_score",
          "execute_date",
          "source"
        ],
        "literal_action": "BUY",
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 191,
        "keys": [
          "symbol",
          "action",
          "reason"
        ],
        "literal_action": "EXIT",
        "literal_reason": null,
        "literal_order_type": null
      },
      {
        "line": 219,
        "keys": [
          "symbol",
          "action"
        ],
        "literal_action": "BUY",
        "literal_reason": null,
        "literal_order_type": null
      }
    ]
  }
}
```

## Equivalence Matrix
```json
{
  "matrix": {
    "candidate_generation": {
      "baseline": {
        "has_candidate_terms": true,
        "generates_leaders_from_prices_map": true,
        "takes_precomputed_leaders": false
      },
      "candidate": {
        "has_candidate_terms": true,
        "generates_leaders_from_prices_map": false,
        "takes_precomputed_leaders": true
      },
      "equivalent": false,
      "risk": "Candidate takes precomputed leaders rather than generating the same historical candidate universe."
    },
    "buy_rule": {
      "baseline_has_buy": true,
      "candidate_has_buy": true,
      "baseline_literal_actions": {
        "BUY": 3,
        "ADD": 1,
        "TP_REDUCE": 1
      },
      "candidate_literal_actions": {
        "EXIT": 4,
        "BUY": 2
      },
      "equivalent": true
    },
    "exit_rule": {
      "baseline_has_exit": true,
      "candidate_has_exit": true,
      "equivalent": true
    },
    "add_rule": {
      "baseline_has_add": true,
      "candidate_has_add": true,
      "equivalent": true
    },
    "reduce_rule": {
      "baseline_has_reduce": true,
      "candidate_has_reduce": false,
      "equivalent": false
    },
    "hold_rule": {
      "baseline_has_hold": true,
      "candidate_has_hold": false,
      "equivalent": false
    },
    "market_gate": {
      "baseline_has_market_gate": true,
      "candidate_has_market_gate": false,
      "candidate_takes_market_state": true,
      "equivalent": false,
      "risk": "Candidate accepts market_state but does not show same market-gate implementation."
    },
    "max_positions": {
      "baseline_has_max_positions": true,
      "candidate_has_max_positions": false,
      "baseline_has_open_positions_count": true,
      "candidate_has_open_positions_count": false,
      "equivalent": false
    },
    "position_sizing": {
      "baseline_action_keys_sample": [
        {
          "line": 2236,
          "keys": [
            "date",
            "cash",
            "positions_value",
            "total_equity",
            "open_positions_count",
            "sim_end_trades",
            "spx_regime",
            "e1r_active_mode",
            "risk_budget_mode",
            "event"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 1515,
          "keys": [
            "date",
            "cash",
            "positions_value",
            "total_equity",
            "daily_return_pct",
            "drawdown_pct",
            "exposure_pct",
            "open_positions_count",
            "pending_orders_count",
            "market_gate_state",
            "spx_regime",
            "e1r_active_mode",
            "risk_budget_mode",
            "risk_budget",
            "spx_close",
            "spx_ma50",
            "spx_day_return_pct",
            "event"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 1589,
          "keys": [
            "symbol",
            "action",
            "trend_state",
            "momentum_score",
            "rs_score",
            "leader_score",
            "trend_health",
            "close_t",
            "ma20",
            "ma20_slope",
            "ma50",
            "ma50_slope",
            "rs_prev20",
            "rs_20d_improvement",
            "momentum_acceleration",
            "e1r_entry_type",
            "e1r_uptrend_emerging_eligible",
            "e1r_uptrend_confirmed_eligible",
            "e1r_entry_reason"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 2198,
          "keys": [
            "symbol",
            "entry_date",
            "exit_date",
            "entry_signal",
            "exit_signal",
            "entry_price",
            "avg_cost",
            "exit_price",
            "effective_exit",
            "return_pct",
            "max_gain_pct",
            "max_drawdown_in_trade",
            "holding_days",
            "size_units_at_exit",
            "leader_score_entry",
            "take_profit_triggered",
            "take_profit_exec_date",
            "realized_pnl_before_exit",
            "actions_during_trade",
            "action_count",
            "execution_model",
            "is_sim_end",
            "entry_regime",
            "exit_regime",
            "dominant_regime",
            "entry_type",
            "regime_day_weights",
            "exit_type",
            "exit_warning_log",
            "exit_warning_count"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 2148,
          "keys": [
            "date",
            "cash",
            "position_value",
            "total_equity",
            "n_holdings",
            "pending_orders",
            "market_gate_state",
            "spx_close",
            "spx_ma50",
            "spx_day_return_pct"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 1165,
          "keys": [
            "shares",
            "avg_cost",
            "size_units",
            "entry_close_ref",
            "entry_date",
            "entry_sig_date",
            "entry_signal",
            "e1r_entry_type",
            "highest_close",
            "min_close_since_entry",
            "current_close",
            "leader_score_entry",
            "entry_spx",
            "relative_stop_triggered",
            "relative_stop_signal_date",
            "relative_stop_exec_date",
            "take_profit_triggered",
            "take_profit_signal_date",
            "take_profit_exec_date",
            "realized_pnl",
            "realized_cost_basis",
            "action_history",
            "ls60_reduce_triggered",
            "entry_regime",
            "entry_type",
            "regime_day_weights"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 1789,
          "keys": [
            "sym",
            "action",
            "signal_date",
            "ls",
            "close_t",
            "entry_rank",
            "strategy",
            "entry_mode",
            "primary_reason",
            "reasons",
            "e1r_entry_type",
            "target_size_units"
          ],
          "literal_action": "BUY",
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 2013,
          "keys": [
            "sym",
            "action",
            "signal_date",
            "ls",
            "close_t",
            "entry_rank",
            "strategy",
            "primary_reason",
            "reasons"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        }
      ],
      "candidate_action_keys_sample": [
        {
          "line": 253,
          "keys": [
            "date",
            "source",
            "gate_open",
            "equity",
            "executed",
            "new_orders",
            "n_positions",
            "status"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 233,
          "keys": [
            "event_id",
            "event_type",
            "date",
            "equity",
            "cash",
            "holdings_value",
            "n_positions",
            "gate_open",
            "source"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 51,
          "keys": [
            "event_id",
            "event_type",
            "date",
            "initial_capital",
            "source",
            "strategy_id"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 77,
          "keys": [
            "event_id",
            "event_type",
            "date",
            "symbol",
            "action",
            "fill_price",
            "units",
            "cost_rate",
            "source",
            "signal_provenance",
            "order_ref"
          ],
          "literal_action": "EXIT",
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 91,
          "keys": [
            "symbol",
            "action",
            "fill_price",
            "signal_provenance",
            "execution_provenance"
          ],
          "literal_action": "EXIT",
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 129,
          "keys": [
            "event_id",
            "event_type",
            "date",
            "signal_date",
            "symbol",
            "action",
            "fill_price",
            "units",
            "total_cost",
            "cost_rate",
            "source",
            "signal_provenance",
            "order_ref"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 145,
          "keys": [
            "symbol",
            "action",
            "fill_price",
            "units",
            "total_cost",
            "signal_provenance",
            "execution_provenance"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 179,
          "keys": [
            "event_id",
            "event_type",
            "date",
            "symbol",
            "action",
            "signal_reason",
            "leader_score",
            "execute_date",
            "source"
          ],
          "literal_action": "EXIT",
          "literal_reason": null,
          "literal_order_type": null
        }
      ],
      "equivalent": false,
      "risk": "Position sizing cannot be assumed equivalent from static schema; requires explicit mapping or replay comparison."
    },
    "state_ownership": {
      "baseline_cash": true,
      "baseline_positions": true,
      "candidate_cash": true,
      "candidate_positions": true,
      "candidate_uses_oos_state": true,
      "equivalent": true
    },
    "historical_replay_compatibility": {
      "candidate_writes_files_or_state": true,
      "candidate_imports_or_uses_oos_state": true,
      "candidate_references_invalid_artifacts": false,
      "equivalent": false,
      "risk": "OOS candidate may depend on forward event/state model; adapter historical replay should own account state."
    }
  },
  "equivalent_count": 4,
  "total_count": 11,
  "failed_dimensions": {
    "candidate_generation": {
      "baseline": {
        "has_candidate_terms": true,
        "generates_leaders_from_prices_map": true,
        "takes_precomputed_leaders": false
      },
      "candidate": {
        "has_candidate_terms": true,
        "generates_leaders_from_prices_map": false,
        "takes_precomputed_leaders": true
      },
      "equivalent": false,
      "risk": "Candidate takes precomputed leaders rather than generating the same historical candidate universe."
    },
    "reduce_rule": {
      "baseline_has_reduce": true,
      "candidate_has_reduce": false,
      "equivalent": false
    },
    "hold_rule": {
      "baseline_has_hold": true,
      "candidate_has_hold": false,
      "equivalent": false
    },
    "market_gate": {
      "baseline_has_market_gate": true,
      "candidate_has_market_gate": false,
      "candidate_takes_market_state": true,
      "equivalent": false,
      "risk": "Candidate accepts market_state but does not show same market-gate implementation."
    },
    "max_positions": {
      "baseline_has_max_positions": true,
      "candidate_has_max_positions": false,
      "baseline_has_open_positions_count": true,
      "candidate_has_open_positions_count": false,
      "equivalent": false
    },
    "position_sizing": {
      "baseline_action_keys_sample": [
        {
          "line": 2236,
          "keys": [
            "date",
            "cash",
            "positions_value",
            "total_equity",
            "open_positions_count",
            "sim_end_trades",
            "spx_regime",
            "e1r_active_mode",
            "risk_budget_mode",
            "event"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 1515,
          "keys": [
            "date",
            "cash",
            "positions_value",
            "total_equity",
            "daily_return_pct",
            "drawdown_pct",
            "exposure_pct",
            "open_positions_count",
            "pending_orders_count",
            "market_gate_state",
            "spx_regime",
            "e1r_active_mode",
            "risk_budget_mode",
            "risk_budget",
            "spx_close",
            "spx_ma50",
            "spx_day_return_pct",
            "event"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 1589,
          "keys": [
            "symbol",
            "action",
            "trend_state",
            "momentum_score",
            "rs_score",
            "leader_score",
            "trend_health",
            "close_t",
            "ma20",
            "ma20_slope",
            "ma50",
            "ma50_slope",
            "rs_prev20",
            "rs_20d_improvement",
            "momentum_acceleration",
            "e1r_entry_type",
            "e1r_uptrend_emerging_eligible",
            "e1r_uptrend_confirmed_eligible",
            "e1r_entry_reason"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 2198,
          "keys": [
            "symbol",
            "entry_date",
            "exit_date",
            "entry_signal",
            "exit_signal",
            "entry_price",
            "avg_cost",
            "exit_price",
            "effective_exit",
            "return_pct",
            "max_gain_pct",
            "max_drawdown_in_trade",
            "holding_days",
            "size_units_at_exit",
            "leader_score_entry",
            "take_profit_triggered",
            "take_profit_exec_date",
            "realized_pnl_before_exit",
            "actions_during_trade",
            "action_count",
            "execution_model",
            "is_sim_end",
            "entry_regime",
            "exit_regime",
            "dominant_regime",
            "entry_type",
            "regime_day_weights",
            "exit_type",
            "exit_warning_log",
            "exit_warning_count"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 2148,
          "keys": [
            "date",
            "cash",
            "position_value",
            "total_equity",
            "n_holdings",
            "pending_orders",
            "market_gate_state",
            "spx_close",
            "spx_ma50",
            "spx_day_return_pct"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 1165,
          "keys": [
            "shares",
            "avg_cost",
            "size_units",
            "entry_close_ref",
            "entry_date",
            "entry_sig_date",
            "entry_signal",
            "e1r_entry_type",
            "highest_close",
            "min_close_since_entry",
            "current_close",
            "leader_score_entry",
            "entry_spx",
            "relative_stop_triggered",
            "relative_stop_signal_date",
            "relative_stop_exec_date",
            "take_profit_triggered",
            "take_profit_signal_date",
            "take_profit_exec_date",
            "realized_pnl",
            "realized_cost_basis",
            "action_history",
            "ls60_reduce_triggered",
            "entry_regime",
            "entry_type",
            "regime_day_weights"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 1789,
          "keys": [
            "sym",
            "action",
            "signal_date",
            "ls",
            "close_t",
            "entry_rank",
            "strategy",
            "entry_mode",
            "primary_reason",
            "reasons",
            "e1r_entry_type",
            "target_size_units"
          ],
          "literal_action": "BUY",
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 2013,
          "keys": [
            "sym",
            "action",
            "signal_date",
            "ls",
            "close_t",
            "entry_rank",
            "strategy",
            "primary_reason",
            "reasons"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        }
      ],
      "candidate_action_keys_sample": [
        {
          "line": 253,
          "keys": [
            "date",
            "source",
            "gate_open",
            "equity",
            "executed",
            "new_orders",
            "n_positions",
            "status"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 233,
          "keys": [
            "event_id",
            "event_type",
            "date",
            "equity",
            "cash",
            "holdings_value",
            "n_positions",
            "gate_open",
            "source"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 51,
          "keys": [
            "event_id",
            "event_type",
            "date",
            "initial_capital",
            "source",
            "strategy_id"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 77,
          "keys": [
            "event_id",
            "event_type",
            "date",
            "symbol",
            "action",
            "fill_price",
            "units",
            "cost_rate",
            "source",
            "signal_provenance",
            "order_ref"
          ],
          "literal_action": "EXIT",
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 91,
          "keys": [
            "symbol",
            "action",
            "fill_price",
            "signal_provenance",
            "execution_provenance"
          ],
          "literal_action": "EXIT",
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 129,
          "keys": [
            "event_id",
            "event_type",
            "date",
            "signal_date",
            "symbol",
            "action",
            "fill_price",
            "units",
            "total_cost",
            "cost_rate",
            "source",
            "signal_provenance",
            "order_ref"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 145,
          "keys": [
            "symbol",
            "action",
            "fill_price",
            "units",
            "total_cost",
            "signal_provenance",
            "execution_provenance"
          ],
          "literal_action": null,
          "literal_reason": null,
          "literal_order_type": null
        },
        {
          "line": 179,
          "keys": [
            "event_id",
            "event_type",
            "date",
            "symbol",
            "action",
            "signal_reason",
            "leader_score",
            "execute_date",
            "source"
          ],
          "literal_action": "EXIT",
          "literal_reason": null,
          "literal_order_type": null
        }
      ],
      "equivalent": false,
      "risk": "Position sizing cannot be assumed equivalent from static schema; requires explicit mapping or replay comparison."
    },
    "historical_replay_compatibility": {
      "candidate_writes_files_or_state": true,
      "candidate_imports_or_uses_oos_state": true,
      "candidate_references_invalid_artifacts": false,
      "equivalent": false,
      "risk": "OOS candidate may depend on forward event/state model; adapter historical replay should own account state."
    }
  },
  "all_equivalent": false
}
```

## Trade Decision Helpers
```json
{
  "path": "src/engine/trade_decision.py",
  "interpretation": "trade_decision helpers may be reusable as pure rule helpers, but they do not own candidate ranking, cash, positions, max_positions, or market gate. They are not a full UPTREND provider by themselves.",
  "helpers": [
    {
      "name": "trade_action",
      "exists": true,
      "features": {
        "exists": true,
        "path": "src/engine/trade_decision.py",
        "name": "trade_action",
        "args": [
          "trend_state",
          "mom_score",
          "rs_score",
          "price",
          "ma50",
          "ma50_slope",
          "leader_score",
          "trend_health",
          "market_score",
          "ls60_exit_mode"
        ],
        "line_count": 55,
        "has_candidate_terms": true,
        "takes_precomputed_leaders": false,
        "generates_leaders_from_prices_map": false,
        "has_buy_logic": true,
        "has_add_logic": true,
        "has_reduce_logic": true,
        "has_exit_logic": true,
        "has_hold_logic": true,
        "has_market_gate": false,
        "takes_market_state": false,
        "has_max_positions": false,
        "has_open_positions_count": false,
        "has_cash_state": false,
        "has_positions_state": false,
        "has_total_equity": false,
        "has_daily_mark_to_market": true,
        "has_signal_execute_dates": false,
        "references_invalid_artifacts": false,
        "calls_run_stateful_simulation": false,
        "writes_files_or_state": false,
        "imports_or_uses_oos_state": true,
        "contains_sidecar": false
      },
      "action_shapes": {
        "action_like_dict_count": 0,
        "literal_action_counts": {},
        "samples": []
      }
    },
    {
      "name": "trade_action_reason",
      "exists": true,
      "features": {
        "exists": true,
        "path": "src/engine/trade_decision.py",
        "name": "trade_action_reason",
        "args": [
          "trend_state",
          "mom_score",
          "rs_score",
          "price",
          "ma50",
          "ma50_slope",
          "leader_score",
          "trend_health",
          "market_score",
          "ls60_exit_mode"
        ],
        "line_count": 81,
        "has_candidate_terms": true,
        "takes_precomputed_leaders": false,
        "generates_leaders_from_prices_map": false,
        "has_buy_logic": true,
        "has_add_logic": true,
        "has_reduce_logic": true,
        "has_exit_logic": true,
        "has_hold_logic": true,
        "has_market_gate": false,
        "takes_market_state": false,
        "has_max_positions": false,
        "has_open_positions_count": false,
        "has_cash_state": false,
        "has_positions_state": false,
        "has_total_equity": false,
        "has_daily_mark_to_market": true,
        "has_signal_execute_dates": false,
        "references_invalid_artifacts": false,
        "calls_run_stateful_simulation": false,
        "writes_files_or_state": false,
        "imports_or_uses_oos_state": true,
        "contains_sidecar": false
      },
      "action_shapes": {
        "action_like_dict_count": 8,
        "literal_action_counts": {
          "REDUCE": 2,
          "EXIT": 2,
          "BUY": 1,
          "ADD": 1,
          "HOLD": 1
        },
        "samples": [
          {
            "line": 194,
            "keys": [
              "action",
              "primary_reason",
              "reasons"
            ],
            "literal_action": "REDUCE",
            "literal_reason": null,
            "literal_order_type": null
          },
          {
            "line": 157,
            "keys": [
              "action",
              "primary_reason",
              "reasons"
            ],
            "literal_action": "EXIT",
            "literal_reason": null,
            "literal_order_type": null
          },
          {
            "line": 161,
            "keys": [
              "action",
              "primary_reason",
              "reasons"
            ],
            "literal_action": "EXIT",
            "literal_reason": null,
            "literal_order_type": null
          },
          {
            "line": 167,
            "keys": [
              "action",
              "primary_reason",
              "reasons"
            ],
            "literal_action": null,
            "literal_reason": null,
            "literal_order_type": null
          },
          {
            "line": 173,
            "keys": [
              "action",
              "primary_reason",
              "reasons"
            ],
            "literal_action": "BUY",
            "literal_reason": null,
            "literal_order_type": null
          },
          {
            "line": 177,
            "keys": [
              "action",
              "primary_reason",
              "reasons"
            ],
            "literal_action": "ADD",
            "literal_reason": null,
            "literal_order_type": null
          },
          {
            "line": 187,
            "keys": [
              "action",
              "primary_reason",
              "reasons"
            ],
            "literal_action": "REDUCE",
            "literal_reason": null,
            "literal_order_type": null
          },
          {
            "line": 191,
            "keys": [
              "action",
              "primary_reason",
              "reasons"
            ],
            "literal_action": "HOLD",
            "literal_reason": null,
            "literal_order_type": null
          }
        ]
      }
    }
  ]
}
```

## Decision
```json
{
  "uptrend_provider_locked": false,
  "implementation_allowed_now": false,
  "run_oos_day_equivalence_passed": false,
  "hard_fail_reasons": [
    "candidate_generation",
    "candidate_lacks_hold_logic",
    "candidate_lacks_max_positions_guard",
    "candidate_lacks_reduce_logic",
    "candidate_lacks_same_market_gate",
    "candidate_requires_precomputed_leaders",
    "historical_replay_compatibility",
    "hold_rule",
    "market_gate",
    "max_positions",
    "position_sizing",
    "reduce_rule"
  ],
  "conclusion": "RUN_OOS_DAY_NOT_EQUIVALENT_USE_RUN_STATEFUL_EXTRACTION_PLAN",
  "recommended_next_action": "Proceed to 4C-2C-4E-D4: no-strategy-change UPTREND provider extraction design from src/engine/backtest.py::run_stateful_simulation. Do not use run_oos_day as adapter provider.",
  "engineering_rule": "Correct trading logic has priority over code reuse. A helper that lacks candidate generation, market gate, max-position guard, sizing equivalence, or historical replay compatibility cannot be used as the official UPTREND provider."
}
```

## Next Action

Proceed to 4C-2C-4E-D4: no-strategy-change UPTREND provider extraction design from src/engine/backtest.py::run_stateful_simulation. Do not use run_oos_day as adapter provider.
