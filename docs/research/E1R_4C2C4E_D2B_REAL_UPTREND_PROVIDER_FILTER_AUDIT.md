# E1R 4C-2C-4E-D2B — Real UPTREND Provider Filter Audit

Generated At: `2026-07-10T03:27:14.220905+00:00`

## Purpose

Filter false-positive provider candidates and inspect the real runtime candidate `src/oos/tracking_engine.py::run_oos_day`.

## Policy
```json
{
  "strategy_logic_changed": false,
  "backtest_engine_run": false,
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
  "audit_only_no_backtest_run": true,
  "full_5y_backtest_run": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "strategy_files_unchanged": true,
  "invalid_artifacts_not_used_as_source": true,
  "composer_not_used": true,
  "return_curve_stitching_not_used": true,
  "d2_report_loaded": true,
  "d2_false_positive_confirmed": true,
  "scripts_docs_filtered_from_provider_candidates": true,
  "run_oos_day_audited": true,
  "runtime_candidates_ranked": true,
  "baseline_run_stateful_audited": true,
  "provider_not_locked_yet": true,
  "implementation_not_allowed_yet": true,
  "decision_generated": true
}
```

## False Positive Audit
```json
{
  "d2_selected_exists": true,
  "d2_selected_candidate": {
    "path": "scripts/e1r_uptrend_provider_entrypoint_audit_4c2c4e_d1.py",
    "name": "audit_run_stateful_uptrend_logic",
    "start_line": 178,
    "end_line": 260,
    "line_count": 83,
    "args": [],
    "classification": "STATEFUL_UPTREND_SIMULATOR_OR_PROVIDER_CANDIDATE",
    "score": 11,
    "reasons": [
      "has_candidate_logic",
      "has_buy_logic",
      "has_exit_logic",
      "has_positions_state",
      "has_cash_state",
      "has_market_gate",
      "has_max_positions"
    ],
    "risks": [
      "Wrapper around run_stateful_simulation, not independent provider."
    ],
    "action_like_dict_count": 0,
    "literal_action_counts": {},
    "return_shape": {
      "return_statements": [
        {
          "line": 244,
          "shape": {
            "type": "dict",
            "keys": [
              "path",
              "function",
              "start_line",
              "end_line",
              "line_count",
              "static_evidence",
              "internal_uptrend_source_logic_located",
              "keyword_hits_count",
              "keyword_hits_sample",
              "candidate_contexts_sample",
              "buy_contexts_sample",
              "add_contexts_sample",
              "reduce_contexts_sample",
              "exit_contexts_sample",
              "action_contexts_sample"
            ]
          }
        }
      ]
    }
  },
  "false_positive_confirmed": true,
  "false_positive_reasons": [
    "path_is_script_or_docs_not_runtime_provider",
    "name_contains_audit",
    "path_is_stage_audit_script",
    "no_action_like_dicts",
    "wrapper_or_static_audit_risk"
  ],
  "corrective_rule": "Exclude scripts/docs/audit/design functions from provider candidate set."
}
```

## run_oos_day Summary
```json
{
  "exists": true,
  "path": "src/oos/tracking_engine.py",
  "name": "run_oos_day",
  "start_line": 25,
  "end_line": 265,
  "line_count": 241,
  "args": [
    "signal_date",
    "leaders",
    "prices",
    "market_state",
    "source",
    "data_date"
  ],
  "classification": {
    "path": "src/oos/tracking_engine.py",
    "name": "run_oos_day",
    "start_line": 25,
    "end_line": 265,
    "line_count": 241,
    "args": [
      "signal_date",
      "leaders",
      "prices",
      "market_state",
      "source",
      "data_date"
    ],
    "classification": "REAL_RUNTIME_PROVIDER_CANDIDATE",
    "score": 16,
    "features": {
      "runtime_src_path": true,
      "oos_path": true,
      "engine_path": false,
      "has_candidate_logic": true,
      "has_buy_logic": true,
      "has_add_logic": true,
      "has_reduce_logic": false,
      "has_exit_logic": true,
      "has_hold_logic": false,
      "has_positions_state": true,
      "has_cash_state": true,
      "has_total_equity": true,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": true,
      "has_daily_loop": true,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": false
    },
    "risks": []
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
  },
  "direct_adapter_provider_assessment": {
    "can_be_direct_adapter_provider_without_equivalence": false,
    "can_be_direct_adapter_provider_after_equivalence": true,
    "blockers_or_required_checks": [
      "must_verify_same_UPTREND_rules_as_run_stateful_simulation",
      "must_verify_same_BUY_EXIT_dates_and_symbols_in_short_window",
      "must_verify_same_position_sizing_or explicitly map to adapter sizing",
      "must verify OOS assumptions do not depend on forward-only state unavailable in historical adapter"
    ]
  }
}
```

## Runtime Candidate Ranking
```json
[
  {
    "path": "src/engine/backtest.py",
    "name": "run_stateful_simulation",
    "start_line": 763,
    "end_line": 2486,
    "line_count": 1724,
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
    "classification": "REAL_RUNTIME_PROVIDER_CANDIDATE",
    "score": 19,
    "features": {
      "runtime_src_path": true,
      "oos_path": false,
      "engine_path": true,
      "has_candidate_logic": true,
      "has_buy_logic": true,
      "has_add_logic": true,
      "has_reduce_logic": true,
      "has_exit_logic": true,
      "has_hold_logic": true,
      "has_positions_state": true,
      "has_cash_state": true,
      "has_total_equity": true,
      "has_open_positions_count": true,
      "has_market_gate": true,
      "has_max_positions": true,
      "has_orders_or_trades": true,
      "has_daily_loop": true,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": false
    },
    "risks": [],
    "action_like_dict_count": 16,
    "literal_action_counts": {
      "BUY": 3,
      "ADD": 1,
      "TP_REDUCE": 1
    }
  },
  {
    "path": "src/oos/tracking_engine.py",
    "name": "run_oos_day",
    "start_line": 25,
    "end_line": 265,
    "line_count": 241,
    "args": [
      "signal_date",
      "leaders",
      "prices",
      "market_state",
      "source",
      "data_date"
    ],
    "classification": "REAL_RUNTIME_PROVIDER_CANDIDATE",
    "score": 16,
    "features": {
      "runtime_src_path": true,
      "oos_path": true,
      "engine_path": false,
      "has_candidate_logic": true,
      "has_buy_logic": true,
      "has_add_logic": true,
      "has_reduce_logic": false,
      "has_exit_logic": true,
      "has_hold_logic": false,
      "has_positions_state": true,
      "has_cash_state": true,
      "has_total_equity": true,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": true,
      "has_daily_loop": true,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": false
    },
    "risks": [],
    "action_like_dict_count": 11,
    "literal_action_counts": {
      "EXIT": 4,
      "BUY": 2
    }
  },
  {
    "path": "src/oos/exporter.py",
    "name": "export_all",
    "start_line": 82,
    "end_line": 207,
    "line_count": 126,
    "args": [
      "state",
      "events",
      "manifest",
      "run_date",
      "data_date"
    ],
    "classification": "RUNTIME_ORDER_OR_TRACKING_HELPER",
    "score": 14,
    "features": {
      "runtime_src_path": true,
      "oos_path": true,
      "engine_path": false,
      "has_candidate_logic": false,
      "has_buy_logic": true,
      "has_add_logic": false,
      "has_reduce_logic": false,
      "has_exit_logic": true,
      "has_hold_logic": false,
      "has_positions_state": true,
      "has_cash_state": true,
      "has_total_equity": true,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": true,
      "has_daily_loop": true,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": false
    },
    "risks": [],
    "action_like_dict_count": 1,
    "literal_action_counts": {}
  },
  {
    "path": "src/oos/portfolio_state.py",
    "name": "rebuild_from_events",
    "start_line": 26,
    "end_line": 112,
    "line_count": 87,
    "args": [
      "cls",
      "events"
    ],
    "classification": "RUNTIME_ORDER_OR_TRACKING_HELPER",
    "score": 14,
    "features": {
      "runtime_src_path": true,
      "oos_path": true,
      "engine_path": false,
      "has_candidate_logic": false,
      "has_buy_logic": true,
      "has_add_logic": true,
      "has_reduce_logic": false,
      "has_exit_logic": true,
      "has_hold_logic": false,
      "has_positions_state": true,
      "has_cash_state": true,
      "has_total_equity": true,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": true,
      "has_daily_loop": true,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": false
    },
    "risks": [],
    "action_like_dict_count": 0,
    "literal_action_counts": {}
  },
  {
    "path": "src/engine/trade_decision.py",
    "name": "trade_action_reason",
    "start_line": 114,
    "end_line": 194,
    "line_count": 81,
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
    "classification": "RUNTIME_ORDER_OR_TRACKING_HELPER",
    "score": 11,
    "features": {
      "runtime_src_path": true,
      "oos_path": false,
      "engine_path": true,
      "has_candidate_logic": true,
      "has_buy_logic": true,
      "has_add_logic": true,
      "has_reduce_logic": true,
      "has_exit_logic": true,
      "has_hold_logic": true,
      "has_positions_state": false,
      "has_cash_state": false,
      "has_total_equity": false,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": false,
      "has_daily_loop": false,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": false
    },
    "risks": [],
    "action_like_dict_count": 8,
    "literal_action_counts": {
      "REDUCE": 2,
      "EXIT": 2,
      "BUY": 1,
      "ADD": 1,
      "HOLD": 1
    }
  },
  {
    "path": "src/engine/trade_decision.py",
    "name": "trade_action",
    "start_line": 24,
    "end_line": 78,
    "line_count": 55,
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
    "classification": "RUNTIME_ORDER_OR_TRACKING_HELPER",
    "score": 11,
    "features": {
      "runtime_src_path": true,
      "oos_path": false,
      "engine_path": true,
      "has_candidate_logic": true,
      "has_buy_logic": true,
      "has_add_logic": true,
      "has_reduce_logic": true,
      "has_exit_logic": true,
      "has_hold_logic": true,
      "has_positions_state": false,
      "has_cash_state": false,
      "has_total_equity": false,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": false,
      "has_daily_loop": false,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": false
    },
    "risks": [],
    "action_like_dict_count": 0,
    "literal_action_counts": {}
  },
  {
    "path": "src/engine/backtest.py",
    "name": "run_strategy_variant_comparison",
    "start_line": 2489,
    "end_line": 2895,
    "line_count": 407,
    "args": [
      "symbols",
      "prices_map",
      "dates_map",
      "spx_prices",
      "spx_dates",
      "ndx_prices",
      "ndx_dates",
      "sox_prices",
      "sox_dates",
      "vix_prices",
      "vix_dates"
    ],
    "classification": "RUNTIME_ORDER_OR_TRACKING_HELPER",
    "score": 10,
    "features": {
      "runtime_src_path": true,
      "oos_path": false,
      "engine_path": true,
      "has_candidate_logic": true,
      "has_buy_logic": false,
      "has_add_logic": false,
      "has_reduce_logic": true,
      "has_exit_logic": true,
      "has_hold_logic": true,
      "has_positions_state": false,
      "has_cash_state": false,
      "has_total_equity": true,
      "has_open_positions_count": false,
      "has_market_gate": true,
      "has_max_positions": true,
      "has_orders_or_trades": true,
      "has_daily_loop": true,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": true,
      "contains_sidecar": true
    },
    "risks": [
      "wrapper_around_run_stateful_simulation",
      "contains_sidecar_terms_may_not_be_pure_uptrend"
    ],
    "action_like_dict_count": 0,
    "literal_action_counts": {}
  },
  {
    "path": "src/export/export_json.py",
    "name": "export_all",
    "start_line": 74,
    "end_line": 146,
    "line_count": 73,
    "args": [
      "market",
      "leaders",
      "watchlist",
      "all_signals",
      "backtest",
      "chart_source"
    ],
    "classification": "RUNTIME_CANDIDATE_GENERATOR_ONLY",
    "score": 8,
    "features": {
      "runtime_src_path": true,
      "oos_path": false,
      "engine_path": false,
      "has_candidate_logic": true,
      "has_buy_logic": false,
      "has_add_logic": false,
      "has_reduce_logic": false,
      "has_exit_logic": false,
      "has_hold_logic": true,
      "has_positions_state": false,
      "has_cash_state": false,
      "has_total_equity": false,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": true,
      "has_daily_loop": true,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": false
    },
    "risks": [],
    "action_like_dict_count": 4,
    "literal_action_counts": {}
  },
  {
    "path": "src/engine/e1r_sidecar_sleeve.py",
    "name": "run_daily_rebalanced_sidecar",
    "start_line": 401,
    "end_line": 470,
    "line_count": 70,
    "args": [
      "rankings",
      "spx",
      "regimes",
      "intervals",
      "config"
    ],
    "classification": "RUNTIME_CANDIDATE_GENERATOR_ONLY",
    "score": 7,
    "features": {
      "runtime_src_path": true,
      "oos_path": false,
      "engine_path": true,
      "has_candidate_logic": true,
      "has_buy_logic": false,
      "has_add_logic": false,
      "has_reduce_logic": false,
      "has_exit_logic": false,
      "has_hold_logic": false,
      "has_positions_state": false,
      "has_cash_state": false,
      "has_total_equity": false,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": false,
      "has_daily_loop": true,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": true
    },
    "risks": [
      "contains_sidecar_terms_may_not_be_pure_uptrend"
    ],
    "action_like_dict_count": 2,
    "literal_action_counts": {}
  },
  {
    "path": "src/engine/e1r_sidecar_sleeve.py",
    "name": "build_e1r_sidecar_sleeve",
    "start_line": 538,
    "end_line": 594,
    "line_count": 57,
    "args": [
      "stock_dir",
      "spx_path",
      "regime_path",
      "config"
    ],
    "classification": "RUNTIME_CANDIDATE_GENERATOR_ONLY",
    "score": 7,
    "features": {
      "runtime_src_path": true,
      "oos_path": false,
      "engine_path": true,
      "has_candidate_logic": true,
      "has_buy_logic": false,
      "has_add_logic": false,
      "has_reduce_logic": false,
      "has_exit_logic": false,
      "has_hold_logic": false,
      "has_positions_state": false,
      "has_cash_state": false,
      "has_total_equity": true,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": false,
      "has_daily_loop": true,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": true
    },
    "risks": [
      "contains_sidecar_terms_may_not_be_pure_uptrend"
    ],
    "action_like_dict_count": 2,
    "literal_action_counts": {}
  },
  {
    "path": "src/engine/e1r_sidecar_sleeve.py",
    "name": "score_candidate",
    "start_line": 254,
    "end_line": 339,
    "line_count": 86,
    "args": [
      "asset",
      "spx",
      "date",
      "config"
    ],
    "classification": "RUNTIME_CANDIDATE_GENERATOR_ONLY",
    "score": 7,
    "features": {
      "runtime_src_path": true,
      "oos_path": false,
      "engine_path": true,
      "has_candidate_logic": true,
      "has_buy_logic": false,
      "has_add_logic": false,
      "has_reduce_logic": false,
      "has_exit_logic": false,
      "has_hold_logic": false,
      "has_positions_state": false,
      "has_cash_state": false,
      "has_total_equity": false,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": false,
      "has_daily_loop": false,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": true
    },
    "risks": [
      "contains_sidecar_terms_may_not_be_pure_uptrend"
    ],
    "action_like_dict_count": 1,
    "literal_action_counts": {}
  },
  {
    "path": "src/engine/e1r_sidecar_sleeve.py",
    "name": "build_daily_rankings",
    "start_line": 356,
    "end_line": 398,
    "line_count": 43,
    "args": [
      "stocks",
      "spx",
      "regimes",
      "intervals",
      "config"
    ],
    "classification": "RUNTIME_CANDIDATE_GENERATOR_ONLY",
    "score": 7,
    "features": {
      "runtime_src_path": true,
      "oos_path": false,
      "engine_path": true,
      "has_candidate_logic": true,
      "has_buy_logic": false,
      "has_add_logic": false,
      "has_reduce_logic": false,
      "has_exit_logic": false,
      "has_hold_logic": false,
      "has_positions_state": false,
      "has_cash_state": false,
      "has_total_equity": false,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": false,
      "has_daily_loop": true,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": true
    },
    "risks": [
      "contains_sidecar_terms_may_not_be_pure_uptrend"
    ],
    "action_like_dict_count": 1,
    "literal_action_counts": {}
  },
  {
    "path": "src/engine/rank_history.py",
    "name": "save_daily_snapshot",
    "start_line": 19,
    "end_line": 35,
    "line_count": 17,
    "args": [
      "date",
      "ranked_stocks"
    ],
    "classification": "RUNTIME_CANDIDATE_GENERATOR_ONLY",
    "score": 7,
    "features": {
      "runtime_src_path": true,
      "oos_path": false,
      "engine_path": true,
      "has_candidate_logic": true,
      "has_buy_logic": false,
      "has_add_logic": false,
      "has_reduce_logic": false,
      "has_exit_logic": false,
      "has_hold_logic": false,
      "has_positions_state": false,
      "has_cash_state": false,
      "has_total_equity": false,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": false,
      "has_daily_loop": true,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": false
    },
    "risks": [],
    "action_like_dict_count": 1,
    "literal_action_counts": {}
  },
  {
    "path": "src/engine/trend_state.py",
    "name": "compute_stock_state",
    "start_line": 25,
    "end_line": 126,
    "line_count": 102,
    "args": [
      "symbol",
      "prices",
      "dates",
      "spx_prices",
      "all_ret20",
      "all_ret60",
      "all_ma50_slopes",
      "members_map"
    ],
    "classification": "RUNTIME_CANDIDATE_GENERATOR_ONLY",
    "score": 7,
    "features": {
      "runtime_src_path": true,
      "oos_path": false,
      "engine_path": true,
      "has_candidate_logic": true,
      "has_buy_logic": false,
      "has_add_logic": false,
      "has_reduce_logic": false,
      "has_exit_logic": false,
      "has_hold_logic": false,
      "has_positions_state": false,
      "has_cash_state": false,
      "has_total_equity": false,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": false,
      "has_daily_loop": true,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": false
    },
    "risks": [],
    "action_like_dict_count": 1,
    "literal_action_counts": {}
  },
  {
    "path": "src/engine/watchlist.py",
    "name": "build_watchlist",
    "start_line": 44,
    "end_line": 119,
    "line_count": 76,
    "args": [
      "ranked_stocks"
    ],
    "classification": "RUNTIME_CANDIDATE_GENERATOR_ONLY",
    "score": 7,
    "features": {
      "runtime_src_path": true,
      "oos_path": false,
      "engine_path": true,
      "has_candidate_logic": true,
      "has_buy_logic": false,
      "has_add_logic": false,
      "has_reduce_logic": false,
      "has_exit_logic": false,
      "has_hold_logic": true,
      "has_positions_state": false,
      "has_cash_state": false,
      "has_total_equity": false,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": false,
      "has_daily_loop": true,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": false
    },
    "risks": [],
    "action_like_dict_count": 1,
    "literal_action_counts": {}
  },
  {
    "path": "src/pipeline/update_pipeline.py",
    "name": "run_daily_update",
    "start_line": 114,
    "end_line": 304,
    "line_count": 191,
    "args": [
      "force_full"
    ],
    "classification": "RUNTIME_CANDIDATE_GENERATOR_ONLY",
    "score": 7,
    "features": {
      "runtime_src_path": true,
      "oos_path": false,
      "engine_path": false,
      "has_candidate_logic": true,
      "has_buy_logic": false,
      "has_add_logic": false,
      "has_reduce_logic": false,
      "has_exit_logic": false,
      "has_hold_logic": false,
      "has_positions_state": false,
      "has_cash_state": false,
      "has_total_equity": false,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": false,
      "has_daily_loop": true,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": false
    },
    "risks": [],
    "action_like_dict_count": 1,
    "literal_action_counts": {}
  },
  {
    "path": "src/engine/backtest.py",
    "name": "_rebuild_leader_score",
    "start_line": 124,
    "end_line": 169,
    "line_count": 46,
    "args": [
      "prices",
      "spx_prices",
      "all_stocks_prices",
      "t"
    ],
    "classification": "RUNTIME_CANDIDATE_GENERATOR_ONLY",
    "score": 7,
    "features": {
      "runtime_src_path": true,
      "oos_path": false,
      "engine_path": true,
      "has_candidate_logic": true,
      "has_buy_logic": false,
      "has_add_logic": false,
      "has_reduce_logic": false,
      "has_exit_logic": false,
      "has_hold_logic": false,
      "has_positions_state": false,
      "has_cash_state": false,
      "has_total_equity": false,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": false,
      "has_daily_loop": false,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": false
    },
    "risks": [],
    "action_like_dict_count": 0,
    "literal_action_counts": {}
  },
  {
    "path": "src/engine/backtest.py",
    "name": "selection_key",
    "start_line": 2767,
    "end_line": 2776,
    "line_count": 10,
    "args": [
      "item"
    ],
    "classification": "RUNTIME_CANDIDATE_GENERATOR_ONLY",
    "score": 7,
    "features": {
      "runtime_src_path": true,
      "oos_path": false,
      "engine_path": true,
      "has_candidate_logic": true,
      "has_buy_logic": false,
      "has_add_logic": false,
      "has_reduce_logic": false,
      "has_exit_logic": false,
      "has_hold_logic": false,
      "has_positions_state": false,
      "has_cash_state": false,
      "has_total_equity": false,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": false,
      "has_daily_loop": false,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": false
    },
    "risks": [],
    "action_like_dict_count": 0,
    "literal_action_counts": {}
  },
  {
    "path": "src/engine/index_analysis.py",
    "name": "_find_prices",
    "start_line": 38,
    "end_line": 59,
    "line_count": 22,
    "args": [
      "code",
      "prices_map"
    ],
    "classification": "RUNTIME_CANDIDATE_GENERATOR_ONLY",
    "score": 7,
    "features": {
      "runtime_src_path": true,
      "oos_path": false,
      "engine_path": true,
      "has_candidate_logic": true,
      "has_buy_logic": false,
      "has_add_logic": false,
      "has_reduce_logic": false,
      "has_exit_logic": false,
      "has_hold_logic": false,
      "has_positions_state": false,
      "has_cash_state": false,
      "has_total_equity": false,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": false,
      "has_daily_loop": true,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": false
    },
    "risks": [],
    "action_like_dict_count": 0,
    "literal_action_counts": {}
  },
  {
    "path": "src/engine/leader_ranking.py",
    "name": "leader_score",
    "start_line": 11,
    "end_line": 20,
    "line_count": 10,
    "args": [
      "rs",
      "mom",
      "th"
    ],
    "classification": "RUNTIME_CANDIDATE_GENERATOR_ONLY",
    "score": 7,
    "features": {
      "runtime_src_path": true,
      "oos_path": false,
      "engine_path": true,
      "has_candidate_logic": true,
      "has_buy_logic": false,
      "has_add_logic": false,
      "has_reduce_logic": false,
      "has_exit_logic": false,
      "has_hold_logic": false,
      "has_positions_state": false,
      "has_cash_state": false,
      "has_total_equity": false,
      "has_open_positions_count": false,
      "has_market_gate": false,
      "has_max_positions": false,
      "has_orders_or_trades": false,
      "has_daily_loop": false,
      "references_invalid_artifacts": false,
      "calls_run_stateful_simulation": false,
      "contains_sidecar": false
    },
    "risks": [],
    "action_like_dict_count": 0,
    "literal_action_counts": {}
  }
]
```

## Decision
```json
{
  "d2_false_positive_confirmed": true,
  "run_oos_day_is_runtime_candidate": true,
  "run_oos_day_allowed_directly_without_equivalence": false,
  "uptrend_provider_locked": false,
  "implementation_allowed_now": false,
  "baseline_reference": {
    "path": "src/engine/backtest.py",
    "name": "run_stateful_simulation",
    "action_like_dict_count": 16,
    "literal_action_counts": {
      "BUY": 3,
      "ADD": 1,
      "TP_REDUCE": 1
    }
  },
  "candidate_for_next_equivalence_audit": {
    "path": "src/oos/tracking_engine.py",
    "name": "run_oos_day",
    "reason": "Best real runtime candidate after filtering out scripts/docs/audit/design false positives."
  },
  "conclusion": "D2_FALSE_POSITIVE_FILTERED_RUN_OOS_DAY_REQUIRES_EQUIVALENCE_AUDIT",
  "recommended_next_action": "Proceed to 4C-2C-4E-D3: UPTREND runtime equivalence audit focused on src/oos/tracking_engine.py::run_oos_day versus src/engine/backtest.py::run_stateful_simulation. Do not implement adapter trading logic yet.",
  "engineering_rule": "Trading logic is not correct until proven equivalent or explicitly approved. Do not use audit scripts as providers. Do not use run_oos_day in adapter until equivalence with run_stateful_simulation UPTREND behavior is verified."
}
```

## Next Action

Proceed to 4C-2C-4E-D3: UPTREND runtime equivalence audit focused on src/oos/tracking_engine.py::run_oos_day versus src/engine/backtest.py::run_stateful_simulation. Do not implement adapter trading logic yet.
