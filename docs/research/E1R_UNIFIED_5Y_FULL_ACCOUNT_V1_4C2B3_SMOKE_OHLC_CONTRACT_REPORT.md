# E1R Unified 5Y Full Account V1 — 4C-2B-3 Smoke OHLC Contract

Generated At: `2026-07-09T11:42:01.184113+00:00`

## Status

- Status: `E1R_UNIFIED_ENGINE_SMOKE_OHLC_CONTRACT_COMPLETE_NO_FULL_BACKTEST`
- Full backtest run: `False`
- Strategy logic changed: `False`

## Import Probe

```json
{
  "ok": true,
  "error": null,
  "signature": "(symbols: 'list[str]', prices_map: 'dict[str, list[float]]', dates_map: 'dict[str, list[str]]', spx_prices: 'list[float]', spx_dates: 'list[str]', ohlc_map: 'dict' = None, assumptions: 'dict' = None, step: 'int' = 1, min_history: 'int' = 120, market_score_default: 'float' = 60.0, sim_start_date: 'str' = None, sim_end_date: 'str' = None, ndx_prices: 'list' = None, ndx_dates: 'list' = None, sox_prices: 'list' = None, sox_dates: 'list' = None, vix_prices: 'list' = None, vix_dates: 'list' = None) -> 'dict'"
}
```

## Smoke

```json
{
  "attempted": true,
  "ok": true,
  "error": null,
  "traceback_tail": null,
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
    "required_assumption_keys_count": 44,
    "required_assumption_keys": [
      "add_size",
      "block_add_after_take_profit",
      "buy_size",
      "candidate_top_n",
      "dynamic_exit_enabled",
      "e1r_regime_daily",
      "e1r_regime_source",
      "e1r_regime_wiring_enabled",
      "e1r_shell_mode",
      "e1r_uptrend_execution_enabled",
      "entry_rs_min",
      "entry_top_n",
      "execution_model",
      "fill_only_enabled",
      "gate_use_leadership",
      "gate_use_slope",
      "initial_capital",
      "ls60_exit_mode",
      "market_gate_enabled",
      "market_shock_daily_return",
      "market_shock_gate_enabled",
      "max_positions",
      "max_single_size",
      "min_hold_allow_broken_exit",
      "min_holding_days",
      "partial_take_profit_enabled",
      "partial_take_profit_fraction",
      "partial_take_profit_threshold",
      "qualified_entry_enabled",
      "qualified_ma50_slope_min",
      "qualified_momentum_min",
      "qualified_price_above_ma50",
      "qualified_rs_min",
      "qualified_states",
      "qualified_th_min",
      "rank_based_exit",
      "relative_stop_action",
      "relative_stop_enabled",
      "relative_stop_once_per_position",
      "relative_stop_underperform_pct",
      "risk_off_below_spx_ma50",
      "strategy_variant",
      "total_one_way",
      "version"
    ],
    "assumption_provenance_counts": {
      "recovered_artifact": 44,
      "hard_default_extra": 12
    },
    "assumption_recovery_sources": [
      {
        "source": "exports/portfolio_backtest.json",
        "json_path": "$",
        "overlap_count": 6,
        "overlap_keys": [
          "entry_top_n",
          "execution_model",
          "initial_capital",
          "rank_based_exit",
          "strategy_variant",
          "version"
        ]
      },
      {
        "source": "exports/portfolio_backtest.json",
        "json_path": "$.strategy_controls",
        "overlap_count": 16,
        "overlap_keys": [
          "candidate_top_n",
          "entry_rs_min",
          "ls60_exit_mode",
          "min_hold_allow_broken_exit",
          "min_holding_days",
          "qualified_entry_enabled",
          "qualified_ma50_slope_min",
          "qualified_momentum_min",
          "qualified_price_above_ma50",
          "qualified_rs_min",
          "qualified_states",
          "qualified_th_min",
          "relative_stop_action",
          "relative_stop_enabled",
          "relative_stop_once_per_position",
          "relative_stop_underperform_pct"
        ]
      },
      {
        "source": "exports/portfolio_backtest.json",
        "json_path": "$.comparison[0]",
        "overlap_count": 8,
        "overlap_keys": [
          "candidate_top_n",
          "entry_rs_min",
          "ls60_exit_mode",
          "min_holding_days",
          "qualified_entry_enabled",
          "qualified_states",
          "relative_stop_enabled",
          "relative_stop_underperform_pct"
        ]
      },
      {
        "source": "exports/portfolio_backtest.json",
        "json_path": "$.comparison[1]",
        "overlap_count": 8,
        "overlap_keys": [
          "candidate_top_n",
          "entry_rs_min",
          "ls60_exit_mode",
          "min_holding_days",
          "qualified_entry_enabled",
          "qualified_states",
          "relative_stop_enabled",
          "relative_stop_underperform_pct"
        ]
      },
      {
        "source": "exports/portfolio_backtest.json",
        "json_path": "$.variant_results.E1_AUDITED_G4_MINHOLD10",
        "overlap_count": 6,
        "overlap_keys": [
          "entry_top_n",
          "execution_model",
          "initial_capital",
          "rank_based_exit",
          "strategy_variant",
          "version"
        ]
      },
      {
        "source": "exports/portfolio_backtest.json",
        "json_path": "$.variant_results.E1_AUDITED_G4_MINHOLD10.strategy_controls",
        "overlap_count": 16,
        "overlap_keys": [
          "candidate_top_n",
          "entry_rs_min",
          "ls60_exit_mode",
          "min_hold_allow_broken_exit",
          "min_holding_days",
          "qualified_entry_enabled",
          "qualified_ma50_slope_min",
          "qualified_momentum_min",
          "qualified_price_above_ma50",
          "qualified_rs_min",
          "qualified_states",
          "qualified_th_min",
          "relative_stop_action",
          "relative_stop_enabled",
          "relative_stop_once_per_position",
          "relative_stop_underperform_pct"
        ]
      },
      {
        "source": "exports/portfolio_backtest.json",
        "json_path": "$.variant_results.E2_DYNAMIC_EXIT_V2",
        "overlap_count": 6,
        "overlap_keys": [
          "entry_top_n",
          "execution_model",
          "initial_capital",
          "rank_based_exit",
          "strategy_variant",
          "version"
        ]
      },
      {
        "source": "exports/portfolio_backtest.json",
        "json_path": "$.variant_results.E2_DYNAMIC_EXIT_V2.strategy_controls",
        "overlap_count": 16,
        "overlap_keys": [
          "candidate_top_n",
          "entry_rs_min",
          "ls60_exit_mode",
          "min_hold_allow_broken_exit",
          "min_holding_days",
          "qualified_entry_enabled",
          "qualified_ma50_slope_min",
          "qualified_momentum_min",
          "qualified_price_above_ma50",
          "qualified_rs_min",
          "qualified_states",
          "qualified_th_min",
          "relative_stop_action",
          "relative_stop_enabled",
          "relative_stop_once_per_position",
          "relative_stop_underperform_pct"
        ]
      },
      {
        "source": "exports/backtest.json",
        "json_path": "$.backtest.results.layer_d",
        "overlap_count": 6,
        "overlap_keys": [
          "entry_top_n",
          "execution_model",
          "initial_capital",
          "rank_based_exit",
          "strategy_variant",
          "version"
        ]
      },
      {
        "source": "exports/backtest.json",
        "json_path": "$.backtest.results.layer_d.strategy_controls",
        "overlap_count": 16,
        "overlap_keys": [
          "candidate_top_n",
          "entry_rs_min",
          "ls60_exit_mode",
          "min_hold_allow_broken_exit",
          "min_holding_days",
          "qualified_entry_enabled",
          "qualified_ma50_slope_min",
          "qualified_momentum_min",
          "qualified_price_above_ma50",
          "qualified_rs_min",
          "qualified_states",
          "qualified_th_min",
          "relative_stop_action",
          "relative_stop_enabled",
          "relative_stop_once_per_position",
          "relative_stop_underperform_pct"
        ]
      }
    ],
    "ohlc_contract_sample": {
      "A": {
        "type": "dict",
        "keys": [
          "close",
          "high",
          "low",
          "open",
          "volume"
        ],
        "lengths": {
          "open": 1562,
          "high": 1562,
          "low": 1562,
          "close": 1562,
          "volume": 1562
        }
      },
      "AAL": {
        "type": "dict",
        "keys": [
          "close",
          "high",
          "low",
          "open",
          "volume"
        ],
        "lengths": {
          "open": 1562,
          "high": 1562,
          "low": 1562,
          "close": 1562,
          "volume": 1562
        }
      },
      "AAPL": {
        "type": "dict",
        "keys": [
          "close",
          "high",
          "low",
          "open",
          "volume"
        ],
        "lengths": {
          "open": 1562,
          "high": 1562,
          "low": 1562,
          "close": 1562,
          "volume": 1562
        }
      }
    },
    "final_assumptions": {
      "add_size": 0.5,
      "block_add_after_take_profit": true,
      "buy_size": 1.0,
      "candidate_top_n": 10,
      "dynamic_exit_enabled": false,
      "e1r_regime_daily": {},
      "e1r_regime_source": "disabled_smoke",
      "e1r_regime_wiring_enabled": false,
      "e1r_shell_mode": "default",
      "e1r_uptrend_execution_enabled": false,
      "entry_rs_min": 90.0,
      "entry_top_n": 3,
      "execution_model": "adverse_intraday",
      "fill_only_enabled": false,
      "gate_use_leadership": true,
      "gate_use_slope": true,
      "initial_capital": 100000.0,
      "ls60_exit_mode": "exit",
      "market_gate_enabled": true,
      "market_shock_daily_return": -0.02,
      "market_shock_gate_enabled": false,
      "max_positions": 10,
      "max_single_size": 1.0,
      "min_hold_allow_broken_exit": true,
      "min_holding_days": 10,
      "partial_take_profit_enabled": false,
      "partial_take_profit_fraction": 0.5,
      "partial_take_profit_threshold": 0.0,
      "qualified_entry_enabled": false,
      "qualified_ma50_slope_min": 0.0,
      "qualified_momentum_min": 85.0,
      "qualified_price_above_ma50": true,
      "qualified_rs_min": 90.0,
      "qualified_states": [
        "Expansion"
      ],
      "qualified_th_min": 75.0,
      "rank_based_exit": false,
      "relative_stop_action": "REL_REDUCE",
      "relative_stop_enabled": false,
      "relative_stop_once_per_position": true,
      "relative_stop_underperform_pct": -8.0,
      "risk_off_below_spx_ma50": false,
      "strategy_variant": "E1_audited_g4_minhold10",
      "total_one_way": 1.0,
      "version": "v1.6-ls60-mode-comparison",
      "sell_size": 1.0,
      "reduce_size": 0.5,
      "position_size_pct": 0.1,
      "min_hold": 10,
      "leader_score_exit": 60,
      "exit_score": 60,
      "market_entry_gate": "slope_leadership",
      "partial_take_profit": false,
      "commission_pct": 0.0,
      "slippage_pct": 0.0,
      "risk_budget": 1.0,
      "risk_budget_mode": "full"
    }
  },
  "result_summary": {
    "type": "dict",
    "keys": [
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
    "metric_like_values": {
      "total_return_pct": -19.52,
      "spx_total_return_pct": 5.94,
      "alpha_pct": -25.46,
      "max_drawdown_pct": 19.52,
      "profit_factor": 0.0,
      "sharpe_ratio": 0,
      "number_of_trades": 2,
      "total_trades_all": 2,
      "final_equity": 80477.02,
      "initial_capital": 100000.0,
      "exposure_pct": 11.1,
      "status": "INSUFFICIENT_SAMPLE",
      "sample_validity": {
        "is_valid": false,
        "sample_status": "INSUFFICIENT_SAMPLE",
        "simulation_start_date": "2021-04-14",
        "simulation_end_date": "2021-07-09",
        "simulation_days": 61,
        "total_trades": 2,
        "completed_trades": 0,
        "sim_end_trades": 2,
        "sim_end_ratio_pct": 100.0,
        "invalid_trades": 0,
        "minimum_required": {
          "sim_days": 252,
          "trades": 20,
          "sim_end_ratio_pct": 50,
          "invalid": 0
        }
      }
    },
    "lists": {
      "invalid_trades": {
        "length": 0,
        "first_type": null
      },
      "equity_curve": {
        "length": 13,
        "first_type": "float"
      },
      "spx_curve": {
        "length": 13,
        "first_type": "float"
      },
      "daily_records": {
        "length": 2,
        "first_type": "dict",
        "first_keys": [
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
        "first": {
          "date": "2021-04-28",
          "cash": 100000.0,
          "position_value": 0.0,
          "total_equity": 100000.0,
          "n_holdings": 0,
          "pending_orders": 0,
          "market_gate_state": "ALLOW",
          "spx_close": 4183.18,
          "spx_ma50": 3991.79,
          "spx_day_return_pct": -0.08
        },
        "last": {
          "date": "2021-06-10",
          "cash": 90000.0,
          "position_value": 5229.75,
          "total_equity": 95229.75,
          "n_holdings": 1,
          "pending_orders": 2,
          "market_gate_state": "ALLOW",
          "spx_close": 4239.18,
          "spx_ma50": 4160.8,
          "spx_day_return_pct": 0.47
        }
      },
      "daily_equity_records": {
        "length": 61,
        "first_type": "dict",
        "first_keys": [
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
        "first": {
          "date": "2021-04-14",
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
          "spx_close": 4124.66,
          "spx_ma50": 3936.5,
          "spx_day_return_pct": -0.4088,
          "event": "EOD_MARK_TO_MARKET"
        },
        "last": {
          "date": "2021-07-09",
          "cash": 80477.02,
          "positions_value": 10010.04,
          "total_equity": 90487.07,
          "daily_return_pct": 0.0883,
          "drawdown_pct": 9.5129,
          "exposure_pct": 11.06,
          "open_positions_count": 2,
          "pending_orders_count": 1,
          "market_gate_state": "ALLOW",
          "spx_regime": null,
          "e1r_active_mode": null,
          "risk_budget_mode": null,
          "risk_budget": null,
          "spx_close": 4369.55,
          "spx_ma50": 4221.21,
          "spx_day_return_pct": 1.1278,
          "event": "EOD_MARK_TO_MARKET"
        }
      },
      "e1r_candidates": {
        "length": 0,
        "first_type": null
      },
      "trades": {
        "length": 2,
        "first_type": "dict",
        "first_keys": [
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
        "first": {
          "symbol": "ADM",
          "entry_date": "2021-05-03",
          "exit_date": "2021-07-09",
          "entry_signal": "BUY",
          "exit_signal": "SIM_END",
          "entry_price": 54.53,
          "avg_cost": 111.65,
          "exit_price": 52.39,
          "effective_exit": 0.0,
          "return_pct": -100.0,
          "max_gain_pct": -46.5,
          "max_drawdown_in_trade": 0,
          "holding_days": 48,
          "size_units_at_exit": 1.5,
          "leader_score_entry": 93.5,
          "take_profit_triggered": false,
          "take_profit_exec_date": null,
          "realized_pnl_before_exit": 0.0,
          "actions_during_trade": [
            "BUY",
            "ADD",
            "ADD",
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
            "HOLD",
            "HOLD",
            "HOLD",
            "HOLD",
            "HOLD",
            "HOLD",
            "HOLD",
            "HOLD",
            "HOLD",
            "HOLD",
            "HOLD",
            "HOLD",
            "HOLD",
            "HOLD",
            "HOLD",
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
          "action_count": 50,
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
        "last": {
          "symbol": "ADBE",
          "entry_date": "2021-06-11",
          "exit_date": "2021-07-09",
          "entry_signal": "BUY",
          "exit_signal": "SIM_END",
          "entry_price": 535.52,
          "avg_cost": 1082.52,
          "exit_price": 604.5,
          "effective_exit": 0.0,
          "return_pct": -100.0,
          "max_gain_pct": -44.02,
          "max_drawdown_in_trade": 0,
          "holding_days": 20,
          "size_units_at_exit": 1.5,
          "leader_score_entry": 90.3,
          "take_profit_triggered": false,
          "take_profit_exec_date": null,
          "realized_pnl_before_exit": 0.0,
          "actions_during_trade": [
            "BUY",
            "BUY",
            "BUY",
            "BUY",
            "ADD",
            "ADD",
            "HOLD",
            "ADD",
            "BUY",
            "BUY",
            "BUY",
            "ADD",
            "ADD",
            "ADD",
            "BUY",
            "HOLD",
            "HOLD",
            "HOLD",
            "HOLD",
            "BUY",
            "BUY",
            "HOLD"
          ],
          "action_count": 22,
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
      }
    },
    "dicts": {
      "strategy_controls": {
        "keys": [
          "candidate_top_n",
          "e1r_regime_source",
          "e1r_regime_wiring_enabled",
          "entry_rs_min",
          "fixed_take_profit_enabled",
          "ls60_exit_mode",
          "min_hold_allow_broken_exit",
          "min_holding_days",
          "qp_avg_pool_size",
          "qp_buy_orders_generated",
          "qp_days_pool_ge_10",
          "qp_days_pool_lt_3",
          "qp_pool_days",
          "qualified_entry_enabled",
          "qualified_ma50_slope_min",
          "qualified_momentum_min",
          "qualified_price_above_ma50",
          "qualified_rs_min",
          "qualified_states",
          "qualified_th_min",
          "relative_stop_action",
          "relative_stop_enabled",
          "relative_stop_once_per_position",
          "relative_stop_stats",
          "relative_stop_underperform_pct"
        ],
        "len": 25
      },
      "partial_take_profit": {
        "keys": [
          "block_add_after_trigger",
          "enabled",
          "execution",
          "name",
          "note",
          "once_per_position",
          "sell_fraction_pct",
          "stats",
          "trigger_gain_pct",
          "trigger_price"
        ],
        "len": 10
      },
      "market_entry_gate": {
        "keys": [
          "blocked_actions",
          "days",
          "enabled",
          "market_shock_rule",
          "risk_off_rule",
          "unaffected_actions",
          "variant"
        ],
        "len": 7
      },
      "sample_validity": {
        "keys": [
          "completed_trades",
          "invalid_trades",
          "is_valid",
          "minimum_required",
          "sample_status",
          "sim_end_ratio_pct",
          "sim_end_trades",
          "simulation_days",
          "simulation_end_date",
          "simulation_start_date",
          "total_trades"
        ],
        "len": 11
      },
      "skipped_orders_by_reason": {
        "keys": [
          "action_reason_buy_add_mismatch",
          "add_blocked_after_tp",
          "already_holding",
          "cash_insufficient",
          "dynamic_exit_warning",
          "dynamic_hard_exit_triggered",
          "dynamic_soft_exit_confirmed",
          "e1r_candidate_buy_generated",
          "e1r_emerging_to_confirmed_add",
          "e1r_legacy_buy_blocked",
          "e1r_no_capacity",
          "entry_rs_below_threshold",
          "fill_only_no_empty_slot",
          "gate_add_blocked",
          "invalid_execution_price",
          "ls60_reduce_already_triggered",
          "market_risk_off_block",
          "market_shock_block",
          "max_positions_reached",
          "max_single_size_reached",
          "min_hold_block",
          "no_t1_price",
          "not_holding",
          "not_in_entry_top_n",
          "not_in_qualified_candidate_pool",
          "not_qualified_entry",
          "qualified_candidate_generated",
          "size_at_minimum"
        ],
        "len": 28
      },
      "portfolio_action_distribution": {
        "keys": [
          "ADD",
          "EXIT",
          "HOLD",
          "REDUCE",
          "REL_REDUCE",
          "TP_REDUCE"
        ],
        "len": 6
      },
      "executed_exit_reason_distribution": {
        "keys": [],
        "len": 0
      },
      "executed_reduce_reason_distribution": {
        "keys": [],
        "len": 0
      },
      "pending_signal_reason_distribution": {
        "keys": [
          "leader_score_below_60",
          "leader_score_below_75"
        ],
        "len": 2
      },
      "sim_end_liquidation_record": {
        "keys": [
          "cash",
          "date",
          "e1r_active_mode",
          "event",
          "open_positions_count",
          "positions_value",
          "risk_budget_mode",
          "sim_end_trades",
          "spx_regime",
          "total_equity"
        ],
        "len": 10
      }
    }
  }
}
```

## Conclusion

- `STATEFUL_ENGINE_SMOKE_OK_READY_FOR_FULL_5Y_RUN`
- Recommended: Proceed to 4C-2C: run full 5Y unified account backtest with all symbols and full aligned 5Y date window.

