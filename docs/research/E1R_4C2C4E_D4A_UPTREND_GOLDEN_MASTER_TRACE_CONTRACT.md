# E1R 4C-2C-4E-D4A — UPTREND Golden Master Trace Contract

Generated At: `2026-07-10T03:47:20.362530+00:00`

## Purpose

Define the UPTREND golden master trace contract before any no-strategy-change provider extraction.

## Policy
```json
{
  "strategy_logic_changed": false,
  "backtest_engine_run": false,
  "full_5y_backtest_run": false,
  "provider_extraction_run": false,
  "adapter_implementation_run": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "frozen_strategy_files_changed": false,
  "invalid_artifacts_used_as_source": false,
  "composer_used": false,
  "return_curve_stitching_used": false
}
```

## Trace Capability Summary
```json
{
  "function": {
    "path": "src/engine/backtest.py",
    "name": "run_stateful_simulation",
    "start_line": 763,
    "end_line": 2486,
    "line_count": 1724
  },
  "classified_counts": {
    "other": 21,
    "daily_account_state": 2,
    "generic_action_record": 1,
    "position_lifecycle": 2,
    "legacy_or_summary_account_state": 1,
    "position_state_internal": 1,
    "action_trace": 7,
    "candidate_trace": 1
  },
  "coverage": {
    "daily_account_state": {
      "source_group": "daily_account_state",
      "required_count": 8,
      "available_required_count": 8,
      "coverage_pct": 1.0,
      "available_required_fields": [
        "cash",
        "date",
        "e1r_active_mode",
        "market_gate_state",
        "open_positions_count",
        "positions_value",
        "spx_regime",
        "total_equity"
      ],
      "missing_fields": []
    },
    "candidate_trace": {
      "source_group": "candidate_trace",
      "required_count": 11,
      "available_required_count": 11,
      "coverage_pct": 1.0,
      "available_required_fields": [
        "close",
        "date",
        "leader_rank",
        "leader_score",
        "ma50",
        "ma50_slope",
        "momentum_score",
        "reasons",
        "rs_score",
        "symbol",
        "trend_health"
      ],
      "missing_fields": []
    },
    "action_trace": {
      "source_group": "action_trace",
      "required_count": 9,
      "available_required_count": 9,
      "coverage_pct": 1.0,
      "available_required_fields": [
        "action",
        "close_t",
        "entry_rank",
        "ls",
        "primary_reason",
        "reasons",
        "signal_date",
        "strategy",
        "sym"
      ],
      "missing_fields": []
    },
    "position_lifecycle": {
      "source_group": "position_lifecycle",
      "required_count": 16,
      "available_required_count": 16,
      "coverage_pct": 1.0,
      "available_required_fields": [
        "actions_during_trade",
        "avg_cost",
        "entry_date",
        "entry_price",
        "entry_regime",
        "entry_signal",
        "entry_type",
        "exit_date",
        "exit_price",
        "exit_regime",
        "exit_signal",
        "exit_type",
        "holding_days",
        "leader_score_entry",
        "return_pct",
        "symbol"
      ],
      "missing_fields": []
    },
    "pending_order_trace": {
      "source_group": "action_trace",
      "required_count": 6,
      "available_required_count": 6,
      "coverage_pct": 1.0,
      "available_required_fields": [
        "action",
        "add_size_units",
        "entry_rank",
        "signal_date",
        "sym",
        "target_size_units"
      ],
      "missing_fields": []
    }
  },
  "enough_for_minimal_golden_master": true
}
```

## Golden Master Contract
```json
{
  "contract_name": "UPTREND_GOLDEN_MASTER_TRACE_V1",
  "baseline_source": "src/engine/backtest.py::run_stateful_simulation",
  "purpose": "Freeze current validated UPTREND behavior before any provider extraction.",
  "scope": {
    "full_5y": false,
    "short_window_only": true,
    "recommended_windows": [
      {
        "name": "UPTREND_WITH_BUY_ADD_HOLD_EXIT",
        "criteria": "A short historical window containing at least one BUY and one EXIT, preferably also ADD/TP_REDUCE if naturally present."
      },
      {
        "name": "UPTREND_GATE_TRANSITION",
        "criteria": "A short window around market gate opening/closing or regime/mode transition."
      }
    ]
  },
  "trace_units": {
    "daily": [
      "date",
      "cash",
      "positions_value",
      "total_equity",
      "open_positions_count",
      "market_gate_state",
      "spx_regime",
      "e1r_active_mode"
    ],
    "candidate": [
      "date",
      "symbol",
      "leader_rank",
      "leader_score",
      "rs_score",
      "trend_health",
      "momentum_score",
      "close",
      "ma50",
      "ma50_slope",
      "reasons"
    ],
    "action": [
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
    "position_lifecycle": [
      "symbol",
      "entry_date",
      "exit_date",
      "entry_signal",
      "exit_signal",
      "entry_price",
      "avg_cost",
      "exit_price",
      "return_pct",
      "holding_days",
      "leader_score_entry",
      "actions_during_trade",
      "entry_regime",
      "exit_regime",
      "entry_type",
      "exit_type"
    ],
    "pending_order": [
      "sym",
      "action",
      "signal_date",
      "entry_rank",
      "target_size_units",
      "add_size_units"
    ]
  },
  "acceptance_rules": {
    "buy_actions": "100% match on symbol, signal_date, action, entry_rank, e1r_entry_type, primary_reason.",
    "exit_actions": "100% match on symbol, signal_date or exit_signal convention, action, exit_type/reasons.",
    "add_reduce_hold_actions": "100% match where the baseline emits explicit action records.",
    "candidate_ranking": "Top-N candidate ordering must match exactly for date/symbol/rank; score values must match within float tolerance.",
    "market_gate": "market_gate_state and risk/e1r active mode must match exactly by date.",
    "account_state": "cash, positions_value, total_equity must match within tolerance; open_positions_count must match exactly and stay <= 3.",
    "position_lifecycle": "entry/exit symbol/date/price/holding_days/action history must match exactly or within explicit execution-price tolerance."
  },
  "float_tolerance": 1e-09,
  "hard_fail_conditions": [
    "Any BUY/EXIT symbol-date mismatch.",
    "Any action missing from extracted provider trace.",
    "Any open_positions_count > 3.",
    "Any candidate ranking mismatch not explained by identical score tie handling.",
    "Any sizing/cash mismatch above tolerance.",
    "Any market_gate_state mismatch by date.",
    "Any use of invalid artifacts or stitched result curves."
  ],
  "current_output_sufficiency": true
}
```

## Minimal Non-Strategy Instrumentation Proposal
```json
{
  "status": "NO_INSTRUMENTATION_REQUIRED_FOR_MINIMAL_CONTRACT",
  "strategy_logic_change_allowed": false,
  "allowed_change_type": "trace/output instrumentation only",
  "not_allowed": [
    "Do not change ranking formula.",
    "Do not change entry/exit/add/reduce/hold decision logic.",
    "Do not change sizing.",
    "Do not change market gate.",
    "Do not change state transition timing.",
    "Do not change execution convention."
  ],
  "required_additions": []
}
```

## Validations
```json
{
  "audit_only_no_full_5y": true,
  "backtest_engine_run": false,
  "provider_extraction_run": false,
  "adapter_implementation_run": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "strategy_files_unchanged": true,
  "invalid_artifacts_not_used_as_source": true,
  "composer_not_used": true,
  "return_curve_stitching_not_used": true,
  "run_stateful_source_audited": true,
  "golden_master_contract_defined": true,
  "acceptance_rules_defined": true,
  "instrumentation_proposal_generated": true,
  "strategy_logic_change_required_false": true,
  "provider_extraction_not_allowed_yet": true,
  "adapter_implementation_not_allowed_yet": true,
  "decision_generated": true
}
```

## Decision
```json
{
  "golden_master_contract_defined": true,
  "current_outputs_sufficient_for_minimal_golden_master": true,
  "instrumentation_required": false,
  "strategy_logic_change_required": false,
  "provider_extraction_allowed_now": false,
  "adapter_implementation_allowed_now": false,
  "conclusion": "GOLDEN_MASTER_TRACE_CONTRACT_READY_FOR_SHORT_WINDOW_BASELINE_EXPORT",
  "recommended_next_action": "Proceed to 4C-2C-4E-D4B: export a short-window UPTREND golden master trace from current run_stateful_simulation outputs. No provider extraction yet.",
  "engineering_rule": "Golden master must be established before provider extraction. Any missing trace fields may only be added as output instrumentation after approval and must not affect ranking, orders, sizing, market gate, or account state."
}
```

## Next Action

Proceed to 4C-2C-4E-D4B: export a short-window UPTREND golden master trace from current run_stateful_simulation outputs. No provider extraction yet.
