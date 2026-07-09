# Stage 3.8E-2F-2C-4C-10F-4B-0I Composer Input Candidates

Generated At: `2026-07-09T10:38:38.099355+00:00`

## Status

- Status: `E1R_COMPOSER_INPUT_CANDIDATES_AUDIT_COMPLETE_NO_INVOCATION`
- Composer invoked: `False`
- Candidate extracted: `False`
- E1R canonical written: `False`
- Strategy files unchanged: `True`
- Canonical existence unchanged: `True`

## Summary

```json
{
  "json_files_scanned": 692,
  "node_candidates_found": 1044,
  "file_error_count": 0,
  "core_candidate_count": 60,
  "sidecar_candidate_count": 60,
  "named_core_candidate_count": 0,
  "named_sidecar_candidate_count": 0,
  "exact_metric_node_count": 30
}
```

## Conclusion

- `CORE_VARIANT_RESULT_INPUT_NOT_PERSISTED_BY_NAME`
- Recommended: Instrument the call site that originally builds core_variant_result, because no persisted named core_variant_result was found.

## Top Core Candidates

```json
[
  {
    "source_file": "exports/backtest.json",
    "json_path": "$.backtest.results.layer_d",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 210,
    "sidecar_score": 0,
    "metric_match": {
      "matched": {
        "total_return_pct": 7.52,
        "alpha_pct": -61.84,
        "max_drawdown_pct": 38.1,
        "profit_factor": 1.25,
        "sharpe_ratio": 0.18
      },
      "diffs": {
        "total_return_pct": 109.22359991347561,
        "alpha_pct": 101.73942548515961,
        "max_drawdown_pct": 12.195190637184893,
        "profit_factor": 0.058036904449065174,
        "sharpe_ratio": 0.6157270568329265
      },
      "exact_metric_match": false
    },
    "summary": {
      "type": "dict",
      "len": 49,
      "keys": [
        "alpha_pct",
        "avg_execution_drag_pct",
        "avg_holding_days",
        "avg_loser_pct",
        "avg_winner_pct",
        "cagr_pct",
        "comparison",
        "daily_records",
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
        "period_comparison",
        "portfolio_action_distribution",
        "profit_factor",
        "rank_based_exit",
        "sample_validity",
        "selected_variant",
        "selection_policy",
        "sharpe_ratio",
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
        "variant_results",
        "version",
        "win_rate_pct"
      ],
      "metric_like_values": {
        "name": "3-Variant LS60 Mode Comparison",
        "version": "v1.6-ls60-mode-comparison",
        "status": "PARTIAL",
        "total_return_pct": 7.52,
        "spx_total_return_pct": 69.36,
        "alpha_pct": -61.84,
        "max_drawdown_pct": 38.1,
        "profit_factor": 1.25,
        "sharpe_ratio": 0.18,
        "number_of_trades": 47,
        "total_trades_all": 47
      },
      "children": {
        "strategy_controls": {
          "type": "dict",
          "keys": [
            "candidate_top_n",
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
          "len": 23
        },
        "partial_take_profit": {
          "type": "dict",
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
          "type": "dict",
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
          "type": "dict",
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
          "type": "dict",
          "keys": [
            "action_reason_buy_add_mismatch",
            "add_blocked_after_tp",
            "already_holding",
            "cash_insufficient",
            "dynamic_exit_warning",
            "dynamic_hard_exit_triggered",
            "dynamic_soft_exit_confirmed",
            "entry_rs_below_threshold",
            "fill_only_no_empty_slot",
            "gate_add_blocked",
            "gate_capacity_block",
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
          "len": 25
        },
        "portfolio_action_distribution": {
          "type": "dict",
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
          "type": "dict",
          "keys": [
            "leader_score_below_60"
          ],
          "len": 1
        },
        "executed_reduce_reason_distribution": {
          "type": "dict",
          "keys": [
            "leader_score_below_75",
            "trend_health_below_60"
          ],
          "len": 2
        },
        "pending_signal_reason_distribution": {
          "type": "dict",
          "keys": [
            "leader_score_below_60",
            "leader_score_below_75",
            "trend_health_below_60"
          ],
          "len": 3
        },
        "invalid_trades": {
          "len": 0,
          "first_type": null
        },
        "equity_curve": {
          "len": 131,
          "first_type": "float"
        },
        "spx_curve": {
          "len": 131,
          "first_type": "float"
        },
        "daily_records": {
          "len": 22,
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
          "first_sample": {
            "date": "2023-11-06",
            "cash": 100000.0,
            "position_value": 0.0,
            "total_equity": 100000.0,
            "n_holdings": 0,
            "pending_orders": 0,
            "market_gate_state": "RISK_OFF",
            "spx_close": 4365.98,
            "spx_ma50": 4346.84,
            "spx_day_return_pct": 0.18
          },
          "last_sample": {
            "date": "2026-05-13",
            "cash": 37067.35,
            "position_value": 55620.57,
            "total_equity": 92687.92,
            "n_holdings": 3,
            "pending_orders": 2,
            "market_gate_state": "ALLOW",
            "spx_close": 7444.25,
            "spx_ma50": 6896.91,
            "spx_day_return_pct": 0.58
          },
          "unique_dates": 22,
          "date_start": "2023-11-06",
          "date_end": "2026-05-13",
          "max_rows_per_date": 1,
          "one_row_per_date_candidate": true
        },
        "trades": {
          "len": 47,
          "first_type": "dict",
          "first_keys": [
            "action_count",
            "actions_during_trade",
            "avg_cost",
            "effective_exit",
            "entry_adverse_gap_pct",
            "entry_date",
            "entry_price",
            "entry_signal",
            "execution_model",
            "exit_adverse_gap_pct",
            "exit_date",
            "exit_price",
            "exit_reason",
            "exit_reasons",
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
            "relative_stop_exec_date",
            "relative_stop_triggered",
            "return_pct",
            "size_units_at_exit",
            "symbol",
            "take_profit_exec_date",
            "take_profit_triggered",
            "total_execution_drag_pct"
          ],
          "first_sample": {
            "symbol": "COIN",
            "entry_date": "2023-11-24",
            "exit_date": "2024-01-05",
            "entry_signal": "BUY",
            "exit_signal": "EXIT",
            "entry_price": 109.25,
            "avg_cost": 117.06,
            "exit_price": 155.6,
            "effective_exit": 150.94,
            "return_pct": 25.97,
            "max_gain_pct": 59.2,
            "max_drawdown_in_trade": 41.38,
            "holding_days": 29,
            "size_units_at_exit": 0.5,
            "leader_score_entry": 95.7,
            "relative_stop_triggered": false,
            "relative_stop_exec_date": null,
            "take_profit_triggered": false,
            "take_profit_exec_date": null,
            "realized_pnl_before_exit": 3831.32,
            "actions_during_trade": [
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "HOLD",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "BUY",
              "REDUCE",
              "REDUCE",
              "REDUCE",
              "EXIT"
            ],
            "action_count": 30,
            "execution_model": "adverse_intraday_v1.0",
            "entry_adverse_gap_pct": 7.146,
            "exit_adverse_gap_pct": 2.996,
            "total_execution_drag_pct": 10.141,
            "is_sim_end": false,
            "exit_reason": "leader_score_below_60",
            "exit_reasons": [
              "leader_score_below_60"
            ],
            "exit_type": "NORMAL_EXIT",
            "exit_warning_log": [],
            "exit_warning_count": 0
          },
          "last_sample": {
            "symbol": "ODFL",
            "entry_date": "2026-06-10",
            "exit_date": "2026-06-11",
            "entry_signal": "BUY",
            "exit_signal": "SIM_END",
            "entry_price": 248.73,
            "avg_cost": 239.81,
            "exit_price": 247.76,
            "effective_exit": 236.92,
            "return_pct": -1.2,
            "max_gain_pct": 3.72,
            "max_drawdown_in_trade": 0,
            "holding_days": 2,
            "size_units_at_exit": 1.0,
            "leader_score_entry": 95.5,
            "take_profit_triggered": false,
            "take_profit_exec_date": null,
            "realized_pnl_before_exit": 0.0,
            "actions_during_trade": [
              "BUY",
              "HOLD",
              "HOLD"
            ],
            "action_count": 3,
            "execution_model": "adverse_intraday_v1.0",
            "is_sim_end": true,
            "exit_type": "SIM_END",
            "exit_warning_log": [],
            "exit_warning_count": 0
          }
        },
        "comparison": {
          "len": 2,
          "first_type": "dict",
          "first_keys": [
            "alpha_pct",
            "avg_loser_pct",
            "avg_winner_pct",
            "cagr_pct",
            "candidate_top_n",
            "entry_rs_min",
            "exposure_pct",
            "ls60_exit_mode",
            "max_drawdown_pct",
            "min_holding_days",
            "number_of_trades",
            "profit_factor",
            "qualified_entry_enabled",
            "qualified_states",
            "relative_stop_enabled",
            "relative_stop_stats",
            "relative_stop_underperform_pct",
            "selected",
            "sharpe_ratio",
            "skip_reasons",
            "status",
            "total_return_pct",
            "variant",
            "win_rate_pct"
          ],
          "first_sample": {
            "variant": "E1_AUDITED_G4_MINHOLD10",
            "selected": true,
            "status": "PARTIAL",
            "entry_rs_min": 90.0,
            "ls60_exit_mode": "exit",
            "min_holding_days": 10,
            "relative_stop_enabled": false,
            "relative_stop_underperform_pct": -8.0,
            "total_return_pct": 7.52,
            "alpha_pct": -61.84,
            "cagr_pct": 2.85,
            "max_drawdown_pct": 38.1,
            "win_rate_pct": 36.2,
            "profit_factor": 1.25,
            "sharpe_ratio": 0.18,
            "number_of_trades": 47,
            "avg_winner_pct": 14.42,
            "avg_loser_pct": -6.56,
            "exposure_pct": 80.1,
            "skip_reasons": {
              "max_positions_reached": 32,
              "cash_insufficient": 0,
              "already_holding": 0,
              "max_single_size_reached": 40,
              "no_t1_price": 0,
              "invalid_execution_price": 0,
              "size_at_minimum": 231,
              "not_holding": 0,
              "not_in_entry_top_n": 4957,
              "not_in_qualified_candidate_pool": 0,
              "not_qualified_entry": 0,
              "qualified_candidate_generated": 0,
              "market_risk_off_block": 13,
              "market_shock_block": 0,
              "add_blocked_after_tp": 0,
              "entry_rs_below_threshold": 0,
              "min_hold_block": 60,
              "dynamic_exit_warning": 0,
              "dynamic_hard_exit_triggered": 0,
              "dynamic_soft_exit_confirmed": 0,
              "ls60_reduce_already_triggered": 0,
              "action_reason_buy_add_mismatch": 0,
              "fill_only_no_empty_slot": 0,
              "gate_capacity_block": 1519,
              "gate_add_blocked": 12
            },
            "qualified_entry_enabled": false,
            "candidate_top_n": null,
            "qualified_states": [
              "Expansion"
            ],
            "relative_stop_stats": {
              "signals": 0,
              "executed": 0
            }
          },
          "last_sample": {
            "variant": "E2_DYNAMIC_EXIT_V2",
            "selected": false,
            "status": "FAIL",
            "entry_rs_min": 90.0,
            "ls60_exit_mode": "exit",
            "min_holding_days": 0,
            "relative_stop_enabled": false,
            "relative_stop_underperform_pct": -8.0,
            "total_return_pct": -21.95,
            "alpha_pct": -91.31,
            "cagr_pct": -9.15,
            "max_drawdown_pct": 51.1,
            "win_rate_pct": 29.3,
            "profit_factor": 0.83,
            "sharpe_ratio": -0.15,
            "number_of_trades": 41,
            "avg_winner_pct": 15.82,
            "avg_loser_pct": -7.88,
            "exposure_pct": 79.8,
            "skip_reasons": {
              "max_positions_reached": 28,
              "cash_insufficient": 0,
              "already_holding": 0,
              "max_single_size_reached": 31,
              "no_t1_price": 0,
              "invalid_execution_price": 0,
              "size_at_minimum": 313,
              "not_holding": 0,
              "not_in_entry_top_n": 4946,
              "not_in_qualified_candidate_pool": 0,
              "not_qualified_entry": 0,
              "qualified_candidate_generated": 0,
              "market_risk_off_block": 6,
              "market_shock_block": 0,
              "add_blocked_after_tp": 0,
              "entry_rs_below_threshold": 0,
              "min_hold_block": 0,
              "dynamic_exit_warning": 27,
              "dynamic_hard_exit_triggered": 0,
              "dynamic_soft_exit_confirmed": 339,
              "ls60_reduce_already_triggered": 0,
              "action_reason_buy_add_mismatch": 0,
              "fill_only_no_empty_slot": 0,
              "gate_capacity_block": 1541,
              "gate_add_blocked": 14
            },
            "qualified_entry_enabled": false,
            "candidate_top_n": null,
            "qualified_states": [
              "Expansion"
            ],
            "relative_stop_stats": {
              "signals": 0,
              "executed": 0
            }
          }
        },
        "variant_results": {
          "type": "dict",
          "keys": [
            "E1_AUDITED_G4_MINHOLD10",
            "E2_DYNAMIC_EXIT_V2"
          ],
          "len": 2
        },
        "period_comparison": {
          "type": "dict",
          "keys": [
            "A_2023_11_TO_2024_12",
            "B_2024_12_TO_2026_06",
            "C_FULL_2023_11_TO_2026_06"
          ],
          "len": 3
        }
      }
    }
  },
  {
    "source_file": "exports/backtest.json",
    "json_path": "$.backtest.results.layer_d.variant_results.E1_AUDITED_G4_MINHOLD10",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 210,
    "sidecar_score": 0,
    "metric_match": {
      "matched": {
        "total_return_pct": 7.52,
        "alpha_pct": -61.84,
        "max_drawdown_pct": 38.1,
        "profit_factor": 1.25,
        "sharpe_ratio": 0.18
      },
      "diffs": {
        "total_return_pct": 109.22359991347561,
        "alpha_pct": 101.73942548515961,
        "max_drawdown_pct": 12.195190637184893,
        "profit_factor": 0.058036904449065174,
        "sharpe_ratio": 0.6157270568329265
      },
      "exact_metric_match": false
    },
    "summary": {
      "type": "dict",
      "len": 44,
      "keys": [
        "alpha_pct",
        "avg_execution_drag_pct",
        "avg_holding_days",
        "avg_loser_pct",
        "avg_winner_pct",
        "cagr_pct",
        "daily_records",
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
        "name": "Stateful Portfolio Backtest",
        "version": "v1.6-top3-rs-minhold-relstop",
        "status": "PARTIAL",
        "total_return_pct": 7.52,
        "spx_total_return_pct": 69.36,
        "alpha_pct": -61.84,
        "max_drawdown_pct": 38.1,
        "profit_factor": 1.25,
        "sharpe_ratio": 0.18,
        "number_of_trades": 47,
        "total_trades_all": 47
      },
      "children": {
        "strategy_controls": {
          "type": "dict",
          "keys": [
            "candidate_top_n",
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
          "len": 23
        },
        "partial_take_profit": {
          "type": "dict",
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
          "type": "dict",
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
          "type": "dict",
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
          "type": "dict",
          "keys": [
            "action_reason_buy_add_mismatch",
            "add_blocked_after_tp",
            "already_holding",
            "cash_insufficient",
            "dynamic_exit_warning",
            "dynamic_hard_exit_triggered",
            "dynamic_soft_exit_confirmed",
            "entry_rs_below_threshold",
            "fill_only_no_empty_slot",
            "gate_add_blocked",
            "gate_capacity_block",
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
          "len": 25
        },
        "portfolio_action_distribution": {
          "type": "dict",
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
          "type": "dict",
          "keys": [
            "leade
```

## Top Sidecar Candidates

```json
[
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4A1_SIDECAR_ACTIVATION_AUDIT.json",
    "json_path": "$.last_4a_summary.sidecar_stats",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 0,
    "sidecar_score": 230,
    "metric_match": {
      "matched": {},
      "diffs": {},
      "exact_metric_match": false
    },
    "summary": {
      "type": "dict",
      "len": 16,
      "keys": [
        "active_count",
        "date_end",
        "date_start",
        "gross_exposure_max",
        "gross_exposure_min",
        "max_rows_per_date",
        "nonzero_sidecar_return_count",
        "one_row_per_date",
        "regime_counts",
        "row_count",
        "selected_count_max",
        "selected_count_min",
        "sidecar_active_by_regime",
        "sidecar_active_by_subclass",
        "subclass_counts",
        "unique_dates"
      ],
      "metric_like_values": {
        "active_count": 0,
        "row_count": 1260
      },
      "children": {
        "regime_counts": {
          "type": "dict",
          "keys": [
            "DOWNTREND",
            "SIDEWAYS",
            "UPTREND"
          ],
          "len": 3
        },
        "subclass_counts": {
          "type": "dict",
          "keys": [
            "DETERIORATION_TRANSITION",
            "MA_CONFLICT",
            "NO_SUBCLASS",
            "RECOVERY_TRANSITION"
          ],
          "len": 4
        },
        "sidecar_active_by_regime": {
          "type": "dict",
          "keys": [],
          "len": 0
        },
        "sidecar_active_by_subclass": {
          "type": "dict",
          "keys": [],
          "len": 0
        }
      }
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4A_SIDECAR_RECORDS_EXPORT_REPORT.json",
    "json_path": "$.sidecar_stats",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 0,
    "sidecar_score": 230,
    "metric_match": {
      "matched": {},
      "diffs": {},
      "exact_metric_match": false
    },
    "summary": {
      "type": "dict",
      "len": 16,
      "keys": [
        "active_count",
        "date_end",
        "date_start",
        "gross_exposure_max",
        "gross_exposure_min",
        "max_rows_per_date",
        "nonzero_sidecar_return_count",
        "one_row_per_date",
        "regime_counts",
        "row_count",
        "selected_count_max",
        "selected_count_min",
        "sidecar_active_by_regime",
        "sidecar_active_by_subclass",
        "subclass_counts",
        "unique_dates"
      ],
      "metric_like_values": {
        "active_count": 135,
        "row_count": 1260
      },
      "children": {
        "regime_counts": {
          "type": "dict",
          "keys": [
            "DOWNTREND",
            "SIDEWAYS",
            "UPTREND"
          ],
          "len": 3
        },
        "subclass_counts": {
          "type": "dict",
          "keys": [
            "DETERIORATION_TRANSITION",
            "MA_CONFLICT",
            "NO_SUBCLASS",
            "RECOVERY_TRANSITION"
          ],
          "len": 4
        },
        "sidecar_active_by_regime": {
          "type": "dict",
          "keys": [
            "SIDEWAYS"
          ],
          "len": 1
        },
        "sidecar_active_by_subclass": {
          "type": "dict",
          "keys": [
            "MA_CONFLICT"
          ],
          "len": 1
        }
      }
    }
  },
  {
    "source_file": "exports/e1r_v0_2_sidecar_records_5y.json",
    "json_path": "$.sidecar_stats",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 0,
    "sidecar_score": 230,
    "metric_match": {
      "matched": {},
      "diffs": {},
      "exact_metric_match": false
    },
    "summary": {
      "type": "dict",
      "len": 16,
      "keys": [
        "active_count",
        "date_end",
        "date_start",
        "gross_exposure_max",
        "gross_exposure_min",
        "max_rows_per_date",
        "nonzero_sidecar_return_count",
        "one_row_per_date",
        "regime_counts",
        "row_count",
        "selected_count_max",
        "selected_count_min",
        "sidecar_active_by_regime",
        "sidecar_active_by_subclass",
        "subclass_counts",
        "unique_dates"
      ],
      "metric_like_values": {
        "active_count": 135,
        "row_count": 1260
      },
      "children": {
        "regime_counts": {
          "type": "dict",
          "keys": [
            "DOWNTREND",
            "SIDEWAYS",
            "UPTREND"
          ],
          "len": 3
        },
        "subclass_counts": {
          "type": "dict",
          "keys": [
            "DETERIORATION_TRANSITION",
            "MA_CONFLICT",
            "NO_SUBCLASS",
            "RECOVERY_TRANSITION"
          ],
          "len": 4
        },
        "sidecar_active_by_regime": {
          "type": "dict",
          "keys": [
            "SIDEWAYS"
          ],
          "len": 1
        },
        "sidecar_active_by_subclass": {
          "type": "dict",
          "keys": [
            "MA_CONFLICT"
          ],
          "len": 1
        }
      }
    }
  },
  {
    "source_file": "exports/e1r_v0_2_backtest_summary.json",
    "json_path": "$",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 100,
    "sidecar_score": 160,
    "metric_match": {
      "matched": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "diffs": {
        "total_return_pct": 0.0,
        "spx_return_pct": 0.0,
        "alpha_pct": 0.0,
        "max_drawdown_pct": 0.0,
        "profit_factor": 0.0,
        "sharpe_ratio": 0.0
      },
      "exact_metric_match": true
    },
    "summary": {
      "type": "dict",
      "len": 20,
      "keys": [
        "alpha_pct",
        "artifact_type",
        "composition_exists",
        "frozen_artifact",
        "max_drawdown_pct",
        "profit_factor",
        "regeneration_note",
        "regime_aware_logic",
        "research_status",
        "row_count",
        "sharpe_ratio",
        "sidecar_active_by_regime",
        "sidecar_active_by_subclass",
        "sidecar_active_days",
        "source_file",
        "source_json_path",
        "spx_return_pct",
        "strategy_id",
        "total_return_pct",
        "variant"
      ],
      "metric_like_values": {
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264,
        "row_count": 1258
      },
      "children": {
        "sidecar_active_by_regime": {
          "type": "dict",
          "keys": [
            "SIDEWAYS"
          ],
          "len": 1
        },
        "sidecar_active_by_subclass": {
          "type": "dict",
          "keys": [
            "MA_CONFLICT"
          ],
          "len": 1
        }
      }
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0_E1_E1R_CORE_CONTRACT_AUDIT.json",
    "json_path": "$.sidecar_saved_summary",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 0,
    "sidecar_score": 130,
    "metric_match": {
      "matched": {},
      "diffs": {},
      "exact_metric_match": false
    },
    "summary": {
      "type": "dict",
      "len": 11,
      "keys": [
        "active_by_regime",
        "active_by_subclass",
        "active_count",
        "artifact_type",
        "exists",
        "gross_exposure_max",
        "gross_exposure_min",
        "path",
        "return_max",
        "return_min",
        "row_count"
      ],
      "metric_like_values": {
        "active_count": 135,
        "row_count": 1260
      },
      "children": {
        "active_by_regime": {
          "type": "dict",
          "keys": [
            "SIDEWAYS"
          ],
          "len": 1
        },
        "active_by_subclass": {
          "type": "dict",
          "keys": [
            "MA_CONFLICT"
          ],
          "len": 1
        }
      }
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json",
    "json_path": "$.source_reports.scripts/export_e1r_v0_2_status.py.term_hits",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 0,
    "sidecar_score": 80,
    "metric_match": {
      "matched": {},
      "diffs": {},
      "exact_metric_match": false
    },
    "summary": {
      "type": "dict",
      "len": 16,
      "keys": [
        "DOWNTREND",
        "E1R_REGIME_AWARE_V0_2",
        "MA_CONFLICT",
        "SIDEWAYS",
        "UPTREND",
        "core",
        "gross_exposure",
        "leader",
        "selected",
        "selected_count",
        "sidecar",
        "sleeve",
        "symbols",
        "top",
        "top_n",
        "weight"
      ],
      "children": {
        "weight": {
          "len": 2,
          "first_type": "int"
        },
        "selected": {
          "len": 5,
          "first_type": "int"
        },
        "selected_count": {
          "len": 2,
          "first_type": "int"
        },
        "symbols": {
          "len": 2,
          "first_type": "int"
        },
        "top": {
          "len": 2,
          "first_type": "int"
        },
        "top_n": {
          "len": 2,
          "first_type": "int"
        },
        "leader": {
          "len": 2,
          "first_type": "int"
        },
        "core": {
          "len": 6,
          "first_type": "int"
        },
        "sidecar": {
          "len": 9,
          "first_type": "int"
        },
        "sleeve": {
          "len": 3,
          "first_type": "int"
        },
        "gross_exposure": {
          "len": 2,
          "first_type": "int"
        },
        "E1R_REGIME_AWARE_V0_2": {
          "len": 1,
          "first_type": "int"
        },
        "UPTREND": {
          "len": 4,
          "first_type": "int"
        },
        "SIDEWAYS": {
          "len": 7,
          "first_type": "int"
        },
        "DOWNTREND": {
          "len": 1,
          "first_type": "int"
        },
        "MA_CONFLICT": {
          "len": 6,
          "first_type": "int"
        }
      }
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json",
    "json_path": "$.source_reports.scripts/run_e1r_v0_2_oos.py.term_hits",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 20,
    "sidecar_score": 80,
    "metric_match": {
      "matched": {},
      "diffs": {},
      "exact_metric_match": false
    },
    "summary": {
      "type": "dict",
      "len": 20,
      "keys": [
        "E1R_REGIME_AWARE_V0_2",
        "HOLD",
        "MA_CONFLICT",
        "SIDEWAYS",
        "core",
        "gross_exposure",
        "order",
        "orders",
        "position",
        "positions",
        "selected",
        "selected_count",
        "sidecar",
        "sleeve",
        "symbols",
        "target",
        "target_weight",
        "top",
        "top_n",
        "weight"
      ],
      "children": {
        "target": {
          "len": 7,
          "first_type": "int"
        },
        "target_weight": {
          "len": 2,
          "first_type": "int"
        },
        "weight": {
          "len": 3,
          "first_type": "int"
        },
        "selected": {
          "len": 6,
          "first_type": "int"
        },
        "selected_count": {
          "len": 3,
          "first_type": "int"
        },
        "symbols": {
          "len": 1,
          "first_type": "int"
        },
        "top": {
          "len": 2,
          "first_type": "int"
        },
        "top_n": {
          "len": 2,
          "first_type": "int"
        },
        "core": {
          "len": 8,
          "first_type": "int"
        },
        "sidecar": {
          "len": 26,
          "first_type": "int"
        },
        "sleeve": {
          "len": 2,
          "first_type": "int"
        },
        "gross_exposure": {
          "len": 2,
          "first_type": "int"
        },
        "position": {
          "len": 9,
          "first_type": "int"
        },
        "positions": {
          "len": 9,
          "first_type": "int"
        },
        "order": {
          "len": 5,
          "first_type": "int"
        },
        "orders": {
          "len": 5,
          "first_type": "int"
        },
        "HOLD": {
          "len": 1,
          "first_type": "int"
        },
        "E1R_REGIME_AWARE_V0_2": {
          "len": 1,
          "first_type": "int"
        },
        "SIDEWAYS": {
          "len": 1,
          "first_type": "int"
        },
        "MA_CONFLICT": {
          "len": 1,
          "first_type": "int"
        }
      }
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json",
    "json_path": "$.source_reports.src/engine/e1r_composer.py.term_hits",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 0,
    "sidecar_score": 80,
    "metric_match": {
      "matched": {},
      "diffs": {},
      "exact_metric_match": false
    },
    "summary": {
      "type": "dict",
      "len": 14,
      "keys": [
        "E1R_REGIME_AWARE_V0_2",
        "MA_CONFLICT",
        "SIDEWAYS",
        "UPTREND",
        "core",
        "gross_exposure",
        "position",
        "selected",
        "selected_count",
        "sidecar",
        "sleeve",
        "symbols",
        "top",
        "top_n"
      ],
      "children": {
        "selected": {
          "len": 2,
          "first_type": "int"
        },
        "selected_count": {
          "len": 2,
          "first_type": "int"
        },
        "symbols": {
          "len": 1,
          "first_type": "int"
        },
        "top": {
          "len": 1,
          "first_type": "int"
        },
        "top_n": {
          "len": 1,
          "first_type": "int"
        },
        "core": {
          "len": 31,
          "first_type": "int"
        },
        "sidecar": {
          "len": 50,
          "first_type": "int"
        },
        "sleeve": {
          "len": 5,
          "first_type": "int"
        },
        "gross_exposure": {
          "len": 3,
          "first_type": "int"
        },
        "position": {
          "len": 2,
          "first_type": "int"
        },
        "E1R_REGIME_AWARE_V0_2": {
          "len": 2,
          "first_type": "int"
        },
        "UPTREND": {
          "len": 1,
          "first_type": "int"
        },
        "SIDEWAYS": {
          "len": 1,
          "first_type": "int"
        },
        "MA_CONFLICT": {
          "len": 1,
          "first_type": "int"
        }
      }
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json",
    "json_path": "$.source_reports.src/engine/e1r_sidecar_sleeve.py.term_hits",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 0,
    "sidecar_score": 80,
    "metric_match": {
      "matched": {},
      "diffs": {},
      "exact_metric_match": false
    },
    "summary": {
      "type": "dict",
      "len": 18,
      "keys": [
        "DOWNTREND",
        "E1R_REGIME_AWARE_V0_2",
        "EXIT",
        "HOLD",
        "MA_CONFLICT",
        "SIDEWAYS",
        "candidate",
        "candidates",
        "core",
        "gross_exposure",
        "selected",
        "selected_count",
        "sidecar",
        "sleeve",
        "symbols",
        "top",
        "top_n",
        "weight"
      ],
      "children": {
        "weight": {
          "len": 5,
          "first_type": "int"
        },
        "selected": {
          "len": 4,
          "first_type": "int"
        },
        "selected_count": {
          "len": 1,
          "first_type": "int"
        },
        "symbols": {
          "len": 5,
          "first_type": "int"
        },
        "candidates": {
          "len": 9,
          "first_type": "int"
        },
        "candidate": {
          "len": 17,
          "first_type": "int"
        },
        "top": {
          "len": 6,
          "first_type": "int"
        },
        "top_n": {
          "len": 6,
          "first_type": "int"
        },
        "core": {
          "len": 16,
          "first_type": "int"
        },
        "sidecar": {
          "len": 9,
          "first_type": "int"
        },
        "sleeve": {
          "len": 8,
          "first_type": "int"
        },
        "gross_exposure": {
          "len": 7,
          "first_type": "int"
        },
        "HOLD": {
          "len": 1,
          "first_type": "int"
        },
        "EXIT": {
          "len": 1,
          "first_type": "int"
        },
        "E1R_REGIME_AWARE_V0_2": {
          "len": 1,
          "first_type": "int"
        },
        "SIDEWAYS": {
          "len": 6,
          "first_type": "int"
        },
        "DOWNTREND": {
          "len": 1,
          "first_type": "int"
        },
        "MA_CONFLICT": {
          "len": 3,
          "first_type": "int"
        }
      }
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4A_SIDECAR_RECORDS_EXPORT_REPORT.json",
    "json_path": "$.sidecar_summary",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 20,
    "sidecar_score": 80,
    "metric_match": {
      "matched": {
        "max_drawdown_pct": -4.30474425235311,
        "profit_factor": 1.324066375239395
      },
      "diffs": {
        "max_drawdown_pct": 30.20955361516822,
        "profit_factor": 0.13210327968846025
      },
      "exact_metric_match": false
    },
    "summary": {
      "type": "dict",
      "len": 25,
      "keys": [
        "active_day_win_rate_pct",
        "active_days",
        "active_window_excess_vs_spx_pct",
        "active_window_spx_return_pct",
        "active_window_strategy_return_pct",
        "allowed_subclasses",
        "avg_active_day_return_pct",
        "equity_end",
        "equity_start",
        "excluded_symbols",
        "exposure_pct_full_period",
        "full_period_excess_vs_spx_pct",
        "full_period_spx_return_pct",
        "full_period_strategy_return_pct",
        "gross_exposure",
        "losing_active_days",
        "max_drawdown_pct",
        "median_active_day_return_pct",
        "name",
        "profit_factor",
        "sharpe",
        "top_n",
        "total_days",
        "trade_count_approx",
        "winning_active_days"
      ],
      "metric_like_values": {
        "name": "E1R_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
        "max_drawdown_pct": -4.30474425235311,
        "profit_factor": 1.324066375239395
      },
      "children": {
        "allowed_subclasses": {
          "len": 1,
          "first_type": "str"
        },
        "excluded_symbols": {
          "len": 1,
          "first_type": "str"
        }
      }
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C6_INTERVAL_SCHEMA_SOURCE_AUDIT.json",
    "json_path": "$.exact_schema_probe.json.equity_records[1]",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 0,
    "sidecar_score": 80,
    "metric_match": {
      "matched": {
        "spx_return_pct": -0.2
      },
      "diffs": {
        "spx_return_pct": 77.044174428316
      },
      "exact_metric_match": false
    },
    "summary": {
      "type": "dict",
      "len": 20,
      "keys": [
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
      "metric_like_values": {
        "spx_return_pct": -0.2
      },
      "children": {}
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C6_INTERVAL_SCHEMA_SOURCE_AUDIT.json",
    "json_path": "$.exact_schema_probe.json.interval_records[1]",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 0,
    "sidecar_score": 80,
    "metric_match": {
      "matched": {
        "spx_return_pct": -0.2
      },
      "diffs": {
        "spx_return_pct": 77.044174428316
      },
      "exact_metric_match": false
    },
    "summary": {
      "type": "dict",
      "len": 17,
      "keys": [
        "combined_return",
        "combined_return_pct",
        "core_end_date",
        "core_return",
        "core_return_pct",
        "date",
        "next_date",
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
      "metric_like_values": {
        "spx_return_pct": -0.2
      },
      "children": {
        "sidecar_holdings": {
          "len": 0,
          "first_type": null
        }
      }
    }
  }
]
```

## Named Core Candidates

```json
[]
```

## Named Sidecar Candidates

```json
[]
```

## Exact Metric Nodes

```json
[
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json",
    "json_path": "$.export_reports.e1r_backtest_summary.e1r_objects[0].summary_fields",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 90,
    "sidecar_score": 0,
    "metric_match": {
      "matched": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "diffs": {
        "total_return_pct": 0.0,
        "spx_return_pct": 0.0,
        "alpha_pct": 0.0,
        "max_drawdown_pct": 0.0,
        "profit_factor": 0.0,
        "sharpe_ratio": 0.0
      },
      "exact_metric_match": true
    },
    "summary": {
      "type": "dict",
      "len": 6,
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "children": {}
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
    "json_path": "$.targets",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 110,
    "sidecar_score": 0,
    "metric_match": {
      "matched": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "diffs": {
        "total_return_pct": 0.0,
        "spx_return_pct": 0.0,
        "alpha_pct": 0.0,
        "max_drawdown_pct": 0.0,
        "profit_factor": 0.0,
        "sharpe_ratio": 0.0
      },
      "exact_metric_match": true
    },
    "summary": {
      "type": "dict",
      "len": 7,
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct",
        "trades"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "children": {}
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
    "json_path": "$.top_recovered_nodes[0].summary.metric_like_values",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 90,
    "sidecar_score": 0,
    "metric_match": {
      "matched": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "diffs": {
        "total_return_pct": 0.0,
        "spx_return_pct": 0.0,
        "alpha_pct": 0.0,
        "max_drawdown_pct": 0.0,
        "profit_factor": 0.0,
        "sharpe_ratio": 0.0
      },
      "exact_metric_match": true
    },
    "summary": {
      "type": "dict",
      "len": 7,
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "strategy_id",
        "total_return_pct"
      ],
      "metric_like_values": {
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "children": {}
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
    "json_path": "$.top_recovered_nodes[1].summary.metric_like_values",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 90,
    "sidecar_score": 0,
    "metric_match": {
      "matched": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "diffs": {
        "total_return_pct": 0.0,
        "spx_return_pct": 0.0,
        "alpha_pct": 0.0,
        "max_drawdown_pct": 0.0,
        "profit_factor": 0.0,
        "sharpe_ratio": 0.0
      },
      "exact_metric_match": true
    },
    "summary": {
      "type": "dict",
      "len": 7,
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "strategy_id",
        "total_return_pct"
      ],
      "metric_like_values": {
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "children": {}
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
    "json_path": "$.top_recovered_nodes[2].summary.metric_like_values",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 90,
    "sidecar_score": 0,
    "metric_match": {
      "matched": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "diffs": {
        "total_return_pct": 0.0,
        "spx_return_pct": 0.0,
        "alpha_pct": 0.0,
        "max_drawdown_pct": 0.0,
        "profit_factor": 0.0,
        "sharpe_ratio": 0.0
      },
      "exact_metric_match": true
    },
    "summary": {
      "type": "dict",
      "len": 6,
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "children": {}
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
    "json_path": "$.top_recovered_nodes[3].summary.metric_like_values",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 90,
    "sidecar_score": 0,
    "metric_match": {
      "matched": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "diffs": {
        "total_return_pct": 0.0,
        "spx_return_pct": 0.0,
        "alpha_pct": 0.0,
        "max_drawdown_pct": 0.0,
        "profit_factor": 0.0,
        "sharpe_ratio": 0.0
      },
      "exact_metric_match": true
    },
    "summary": {
      "type": "dict",
      "len": 6,
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "children": {}
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
    "json_path": "$.top_recovered_nodes[4].summary.metric_like_values",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 90,
    "sidecar_score": 0,
    "metric_match": {
      "matched": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "diffs": {
        "total_return_pct": 0.0,
        "spx_return_pct": 0.0,
        "alpha_pct": 0.0,
        "max_drawdown_pct": 0.0,
        "profit_factor": 0.0,
        "sharpe_ratio": 0.0
      },
      "exact_metric_match": true
    },
    "summary": {
      "type": "dict",
      "len": 6,
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "children": {}
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
    "json_path": "$.top_recovered_nodes[5].summary.metric_like_values",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 90,
    "sidecar_score": 0,
    "metric_match": {
      "matched": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "diffs": {
        "total_return_pct": 0.0,
        "spx_return_pct": 0.0,
        "alpha_pct": 0.0,
        "max_drawdown_pct": 0.0,
        "profit_factor": 0.0,
        "sharpe_ratio": 0.0
      },
      "exact_metric_match": true
    },
    "summary": {
      "type": "dict",
      "len": 6,
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "children": {}
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
    "json_path": "$.top_recovered_nodes[6].summary.metric_like_values",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 90,
    "sidecar_score": 0,
    "metric_match": {
      "matched": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "diffs": {
        "total_return_pct": 0.0,
        "spx_return_pct": 0.0,
        "alpha_pct": 0.0,
        "max_drawdown_pct": 0.0,
        "profit_factor": 0.0,
        "sharpe_ratio": 0.0
      },
      "exact_metric_match": true
    },
    "summary": {
      "type": "dict",
      "len": 6,
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "children": {}
    }
  },
  {
    "source_file": "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0B_E1R_CORE_VARIANT_SOURCE_RECOVERY.json",
    "json_path": "$.top_recovered_nodes[7].summary.metric_like_values",
    "is_named_core_variant_result": false,
    "is_named_sidecar_result": false,
    "core_score": 90,
    "sidecar_score": 0,
    "metric_match": {
      "matched": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "diffs": {
        "total_return_pct": 0.0,
        "spx_return_pct": 0.0,
        "alpha_pct": 0.0,
        "max_drawdown_pct": 0.0,
        "profit_factor": 0.0,
        "sharpe_ratio": 0.0
      },
      "exact_metric_match": true
    },
    "summary": {
      "type": "dict",
      "len": 6,
      "keys": [
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "spx_return_pct",
        "total_return_pct"
      ],
      "metric_like_values": {
        "total_return_pct": 116.7435999134756,
        "spx_return_pct": 76.844174428316,
        "alpha_pct": 39.89942548515961,
        "max_drawdown_pct": 25.904809362815108,
        "profit_factor": 1.1919630955509348,
        "sharpe_ratio": 0.7957270568329264
      },
      "children": {}
    }
  }
]
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-4B-0J`: Direct no-write compose invocation or call-site instrumentation
- Recommended action: Instrument the call site that originally builds core_variant_result, because no persisted named core_variant_result was found.

