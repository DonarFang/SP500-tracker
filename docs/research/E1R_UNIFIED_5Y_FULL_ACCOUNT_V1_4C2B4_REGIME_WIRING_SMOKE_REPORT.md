# E1R Unified 5Y Full Account V1 — 4C-2B-4 Regime Wiring Smoke

Generated At: `2026-07-09T11:45:20.179838+00:00`

## Status

- Status: `E1R_UNIFIED_ENGINE_REGIME_WIRING_SMOKE_COMPLETE_NO_FULL_BACKTEST`
- Full backtest run: `False`
- Strategy logic changed: `False`

## Key Checks

```json
{
  "package_import_ok": true,
  "smoke_ok": true,
  "has_daily_records_like_output": false,
  "regime_wired_observed": false,
  "critical_assumptions": {
    "e1r_regime_wiring_enabled": true,
    "e1r_uptrend_execution_enabled": true,
    "e1r_regime_source": "data/research/e1_5y/regimes/spx_regime_daily.json",
    "e1r_shell_mode": "regime_wiring_smoke",
    "strategy_variant": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_REGIME_WIRING_SMOKE",
    "version": "4C-2B-4-regime-wiring-smoke"
  },
  "daily_regime_output_summary": {
    "daily_equity_records_length": null,
    "first_spx_regime": null,
    "first_e1r_active_mode": null,
    "last_spx_regime": null,
    "last_e1r_active_mode": null,
    "first": null,
    "last": null
  }
}
```

## Smoke Summary

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
    "sim_start_date": "2022-01-03",
    "sim_end_date": "2022-04-29",
    "required_assumption_keys_count": 44,
    "assumption_provenance_counts": {
      "recovered_artifact": 37,
      "stage_override_loaded_regime_file": 2,
      "stage_override": 5,
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
    "regime_daily_summary": {
      "path": "data/research/e1_5y/regimes/spx_regime_daily.json",
      "exists": true,
      "count": 1562,
      "date_start": "2020-04-01",
      "date_end": "2026-06-18",
      "regime_counts": {
        "UNCLASSIFIED": 253,
        "UPTREND": 910,
        "SIDEWAYS": 241,
        "DOWNTREND": 158
      },
      "subclass_counts": {
        "NO_SUBCLASS": 1321,
        "MA_CONFLICT": 135,
        "DETERIORATION_TRANSITION": 63,
        "RECOVERY_TRANSITION": 43
      },
      "sample_first": {
        "regime": "UNCLASSIFIED",
        "subclass": "NO_SUBCLASS",
        "spx_regime": "UNCLASSIFIED",
        "sideways_subclass": "NO_SUBCLASS"
      },
      "sample_last": {
        "regime": "UPTREND",
        "subclass": "NO_SUBCLASS",
        "spx_regime": "UPTREND",
        "sideways_subclass": "NO_SUBCLASS"
      }
    },
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
    "critical_assumptions": {
      "e1r_regime_wiring_enabled": true,
      "e1r_uptrend_execution_enabled": true,
      "e1r_regime_source": "data/research/e1_5y/regimes/spx_regime_daily.json",
      "e1r_shell_mode": "regime_wiring_smoke",
      "strategy_variant": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_REGIME_WIRING_SMOKE",
      "version": "4C-2B-4-regime-wiring-smoke"
    }
  },
  "result_summary": {
    "type": "dict",
    "keys": [
      "layer",
      "name",
      "skipped_orders_by_reason",
      "status"
    ],
    "metric_like_values": {
      "status": "NO_TRADES"
    },
    "lists": {},
    "dicts": {
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
        "len": 27
      }
    }
  },
  "daily_regime_output_summary": {
    "daily_equity_records_length": null,
    "first_spx_regime": null,
    "first_e1r_active_mode": null,
    "last_spx_regime": null,
    "last_e1r_active_mode": null,
    "first": null,
    "last": null
  }
}
```

## Conclusion

- `STATEFUL_ENGINE_REGIME_SMOKE_OK_BUT_OUTPUT_CONTRACT_NEEDS_MAPPING`
- Recommended: Map returned object fields to daily equity contract before full 5Y.

