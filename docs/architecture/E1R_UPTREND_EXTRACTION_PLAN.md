# E1R 4C-2C-4E-ENGINE-I — UPTREND Extraction Plan

Generated At: `2026-07-10T10:56:35.378449+00:00`

## Purpose
Define UPTREND extraction plan against locked ENGINE-H equivalence assertions without implementing extracted strategy code.

## Policy
```json
{
  "strategy_logic_changed": false,
  "plan_only": true,
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

## Source Function
```json
{
  "name": "run_stateful_simulation",
  "start_line": 763,
  "end_line": 2486,
  "line_count": 1724,
  "source_sha256": "4b14466bbe7c170dc2c212ecec0fb7c02baf79e70f0002163f3287dcecc14d4f"
}
```

## Static Feature Scan Summary
```json
{
  "candidate_generation": {
    "present": true,
    "keyword_count": 25,
    "keywords": [
      "leader_score",
      "leader_rank",
      "rank",
      "rs_score",
      "trend_health",
      "candidate",
      "top_n",
      "entry_top_n"
    ]
  },
  "entry_buy": {
    "present": true,
    "keyword_count": 25,
    "keywords": [
      "BUY",
      "buy_size",
      "target_size",
      "entry_signal",
      "entry_type",
      "pending_orders"
    ]
  },
  "add_reduce_exit": {
    "present": true,
    "keyword_count": 25,
    "keywords": [
      "ADD",
      "REDUCE",
      "EXIT",
      "leader_score_below",
      "broken_trend",
      "exit_signal",
      "exit_type"
    ]
  },
  "market_gate": {
    "present": true,
    "keyword_count": 25,
    "keywords": [
      "market_gate",
      "market_entry_gate",
      "SPX",
      "MA50",
      "shock",
      "risk_off"
    ]
  },
  "account_state": {
    "present": true,
    "keyword_count": 25,
    "keywords": [
      "cash",
      "positions",
      "total_equity",
      "positions_value",
      "open_positions_count",
      "n_holdings",
      "max_positions"
    ]
  },
  "daily_trace": {
    "present": true,
    "keyword_count": 25,
    "keywords": [
      "daily_equity_records",
      "daily_records",
      "trades",
      "actions_during_trade",
      "pending_orders_count"
    ]
  }
}
```

## Literal Action Counts
```json
{
  "BUY": 13,
  "ADD": 14,
  "REDUCE": 13,
  "EXIT": 14,
  "HOLD": 2,
  "TP_REDUCE": 8,
  "SIM_END": 2
}
```

## Extraction Units
```json
[
  {
    "unit": "market_gate_state",
    "legacy_evidence_group": "market_gate",
    "target": "uptrend_core should preserve legacy market gate state exactly",
    "equivalence_assertions": [
      "daily_market_gate_state"
    ],
    "implementation_order": 1,
    "risk": "High — gate drift changes all downstream orders."
  },
  {
    "unit": "daily_account_mark_to_market",
    "legacy_evidence_group": "account_state",
    "target": "account cash/equity/positions_value/open_positions_count must match golden master",
    "equivalence_assertions": [
      "daily_total_equity_cash_positions",
      "daily_open_positions_count",
      "daily_account_date_sequence"
    ],
    "implementation_order": 2,
    "risk": "High — accounting drift invalidates backtest equivalence."
  },
  {
    "unit": "candidate_generation_and_rank",
    "legacy_evidence_group": "candidate_generation",
    "target": "candidate scoring/ranking must be extracted without interpretation",
    "equivalence_assertions": [
      "candidate_ranking_trace"
    ],
    "implementation_order": 3,
    "risk": "Very high — current ENGINE-G short window lacks candidate trace, so first extraction can only be indirectly verified."
  },
  {
    "unit": "entry_buy_logic",
    "legacy_evidence_group": "entry_buy",
    "target": "BUY symbol/date/entry price must match trade lifecycle where available",
    "equivalence_assertions": [
      "trade_lifecycle_symbol_dates",
      "trade_signals_and_reasons"
    ],
    "implementation_order": 4,
    "risk": "High — depends on candidate generation, market gate, cash, capacity."
  },
  {
    "unit": "hold_add_reduce_exit_logic",
    "legacy_evidence_group": "add_reduce_exit",
    "target": "ADD/REDUCE/EXIT transitions must match trade lifecycle and daily account state",
    "equivalence_assertions": [
      "trade_lifecycle_symbol_dates",
      "trade_signals_and_reasons"
    ],
    "implementation_order": 5,
    "risk": "High — action trace is currently missing, so daily/trade lifecycle must be first control."
  },
  {
    "unit": "trace_export",
    "legacy_evidence_group": "daily_trace",
    "target": "new engine must export daily equity records and trade lifecycle in a comparable schema",
    "equivalence_assertions": [
      "daily_account_date_sequence",
      "daily_total_equity_cash_positions",
      "daily_open_positions_count",
      "daily_market_gate_state",
      "daily_spx_regime",
      "trade_lifecycle_symbol_dates",
      "trade_signals_and_reasons"
    ],
    "implementation_order": 6,
    "risk": "Medium — trace schema must be stable before tightening equivalence."
  }
]
```

## Equivalence Plan
```json
{
  "locked_assertions_source": "exports/e1r_engine/audit/e1r_engine_h_equivalence_assertions.json",
  "t0_t1_hard_required_assertions": [
    "daily_account_date_sequence",
    "daily_total_equity_cash_positions",
    "daily_open_positions_count",
    "daily_market_gate_state",
    "daily_spx_regime",
    "trade_lifecycle_symbol_dates",
    "trade_signals_and_reasons"
  ],
  "minimum_extraction_assertions": [
    "daily_account_date_sequence",
    "daily_total_equity_cash_positions",
    "daily_open_positions_count",
    "daily_market_gate_state",
    "daily_spx_regime",
    "trade_lifecycle_symbol_dates",
    "trade_signals_and_reasons"
  ],
  "known_trace_gaps": [
    "No standalone action_trace section.",
    "No daily per-symbol position snapshot section.",
    "No candidate ranking trace in this short window.",
    "No standalone pending order trace."
  ],
  "tolerances": {
    "date_sequence": "exact",
    "cash": "abs <= 0.01 or relative <= 1e-6",
    "positions_value": "abs <= 0.01 or relative <= 1e-6",
    "total_equity": "abs <= 0.01 or relative <= 1e-6",
    "open_positions_count": "exact integer and <= 3",
    "market_gate_state": "exact string",
    "spx_regime": "exact string",
    "trade_symbol_dates": "symbol/date exact",
    "trade_prices": "abs <= 0.01",
    "trade_return_pct": "abs <= 0.01 percentage points"
  },
  "engine_j_acceptance": {
    "must_pass": [
      "new engine runs same 2021-04-05..2021-06-30 window",
      "no frozen strategy files changed",
      "no full 5Y run",
      "no official result/dashboard",
      "T0 assertions pass",
      "T1 trade lifecycle assertions pass or report exact mismatch list",
      "max open positions <= 3 every day"
    ],
    "allowed_initial_mismatch": [
      "candidate_ranking_trace because source golden master has e1r_candidates=0",
      "standalone action_trace because source golden master lacks action_trace_candidates",
      "daily_position_snapshot because source golden master lacks per-day symbol snapshots"
    ],
    "hard_fail": [
      "date sequence mismatch",
      "cash/equity mismatch above tolerance",
      "open_positions_count > 3",
      "market_gate_state mismatch",
      "trade symbol/date mismatch without documented trace gap",
      "any change to src/engine/backtest.py strategy logic"
    ]
  }
}
```

## Implementation Sequence
```json
[
  {
    "stage": "ENGINE-J",
    "name": "UPTREND extraction skeleton + equivalence checker",
    "scope": "Create uptrend_core.py and equivalence.py; run same short window; compare T0/T1; no full 5Y.",
    "strategy_logic_change": "New engine module only; frozen legacy files unchanged."
  },
  {
    "stage": "ENGINE-K",
    "name": "UPTREND equivalence tightening",
    "scope": "Resolve mismatches against T0/T1 assertions; optionally add trace instrumentation only after approval.",
    "strategy_logic_change": "No rule interpretation changes without explicit approval."
  },
  {
    "stage": "ENGINE-L",
    "name": "SIDEWAYS_MA_CONFLICT integration plan",
    "scope": "After UPTREND equivalence, integrate sidecar candidate branch under max3 account.",
    "strategy_logic_change": "Separate approval required."
  }
]
```

## Plan Artifact
- Path: `exports/e1r_engine/audit/e1r_engine_i_uptrend_extraction_plan.json`
- SHA256: `179df39beb1ba4dc1974742327eba5cef8e34456c3646069e5a1cc3f22b8bdf0`

## Validations
```json
{
  "uptrend_extraction_plan_defined": true,
  "plan_only": true,
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
  "engine_h_loaded": true,
  "equivalence_assertions_loaded": true,
  "run_stateful_simulation_located": true,
  "static_feature_scan_completed": true,
  "extraction_boundaries_defined": true,
  "extraction_units_defined": true,
  "equivalence_plan_defined": true,
  "engine_j_acceptance_defined": true,
  "plan_artifact_written": true,
  "strategy_core_extraction_not_run": true
}
```

## Decision
```json
{
  "uptrend_extraction_plan_passed": true,
  "next_stage_allowed": "4C-2C-4E-ENGINE-J",
  "engine_j_scope": "UPTREND extraction skeleton + equivalence checker against ENGINE-G/H",
  "strategy_core_extraction_allowed_now": false,
  "uptrend_provider_extraction_allowed_after_user_approval": true,
  "sideways_branch_implementation_allowed_now": false,
  "full_5y_backtest_allowed_now": false,
  "forward_runner_allowed_now": false,
  "conclusion": "UPTREND_EXTRACTION_PLAN_PASS_READY_FOR_ENGINE_J_IMPLEMENTATION",
  "recommended_next_action": "Proceed to 4C-2C-4E-ENGINE-J: implement UPTREND extraction skeleton and equivalence checker. This next step may create new strategy-core code under src/e1r_engine, but must not modify legacy strategy files.",
  "engineering_rule": "ENGINE-J must be equivalence-first. Any mismatch must be reported before continuing. Do not tune, reinterpret, or improve trading rules during extraction."
}
```
