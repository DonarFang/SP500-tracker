# E1R 4C-2C-4E-D2 — UPTREND Provider Candidate Verification Audit

Generated At: `2026-07-10T03:05:41.387092+00:00`

## Purpose

Classify and verify direct UPTREND provider candidates found by D1 before adapter implementation.

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
  "d1_report_loaded": true,
  "d_report_loaded": true,
  "direct_candidates_from_d1_loaded": true,
  "direct_candidates_inspected": true,
  "best_candidate_selected_or_reviewed": true,
  "run_stateful_baseline_audited": true,
  "provider_not_locked_yet": true,
  "implementation_not_allowed_yet": true,
  "decision_generated": true
}
```

## Candidate Counts
```json
{
  "d1_direct_candidates_count": 6,
  "additional_direct_candidates_count": 5
}
```

## Ranked Candidates Summary
```json
[
  {
    "rank": 1,
    "path": "scripts/e1r_uptrend_provider_entrypoint_audit_4c2c4e_d1.py",
    "name": "audit_run_stateful_uptrend_logic",
    "start_line": 178,
    "classification": "STATEFUL_UPTREND_SIMULATOR_OR_PROVIDER_CANDIDATE",
    "score": 11,
    "risks": [
      "Wrapper around run_stateful_simulation, not independent provider."
    ],
    "action_like_dict_count": 0,
    "literal_action_counts": {}
  },
  {
    "rank": 2,
    "path": "scripts/e1r_uptrend_provider_entrypoint_audit_4c2c4e_d1.py",
    "name": "function_index",
    "start_line": 262,
    "classification": "STATEFUL_UPTREND_SIMULATOR_OR_PROVIDER_CANDIDATE",
    "score": 11,
    "risks": [],
    "action_like_dict_count": 0,
    "literal_action_counts": {}
  },
  {
    "rank": 3,
    "path": "src/oos/tracking_engine.py",
    "name": "run_oos_day",
    "start_line": 25,
    "classification": "STATEFUL_UPTREND_SIMULATOR_OR_PROVIDER_CANDIDATE",
    "score": 10,
    "risks": [],
    "action_like_dict_count": 11,
    "literal_action_counts": {
      "EXIT": 4,
      "BUY": 2
    }
  },
  {
    "rank": 4,
    "path": "scripts/e1r_continuous_stateful_adapter_design_4c2c4e_d.py",
    "name": "design_adapter_contract",
    "start_line": 195,
    "classification": "STATEFUL_UPTREND_SIMULATOR_OR_PROVIDER_CANDIDATE",
    "score": 10,
    "risks": [
      "Contains sidecar terms; may be mixed-regime helper rather than pure UPTREND provider."
    ],
    "action_like_dict_count": 3,
    "literal_action_counts": {
      "BUY | ADD | REDUCE | EXIT | HOLD": 1
    }
  },
  {
    "rank": 5,
    "path": "scripts/e1r_continuous_stateful_adapter_design_4c2c4e_d.py",
    "name": "ast_function_index",
    "start_line": 98,
    "classification": "STATEFUL_UPTREND_SIMULATOR_OR_PROVIDER_CANDIDATE",
    "score": 10,
    "risks": [
      "Contains sidecar terms; may be mixed-regime helper rather than pure UPTREND provider."
    ],
    "action_like_dict_count": 0,
    "literal_action_counts": {}
  },
  {
    "rank": 6,
    "path": "scripts/e1r_branch_execution_transition_audit_4c2c4e_c.py",
    "name": "find_e1r_regime_usage_in_engine",
    "start_line": 116,
    "classification": "STATEFUL_UPTREND_SIMULATOR_OR_PROVIDER_CANDIDATE",
    "score": 8,
    "risks": [
      "Wrapper around run_stateful_simulation, not independent provider.",
      "Contains sidecar terms; may be mixed-regime helper rather than pure UPTREND provider."
    ],
    "action_like_dict_count": 0,
    "literal_action_counts": {}
  }
]
```

## Selected Candidate
```json
{
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
}
```

## Baseline
```json
{
  "path": "src/engine/backtest.py",
  "name": "run_stateful_simulation",
  "action_like_dict_count": 16,
  "literal_action_counts": {
    "BUY": 3,
    "ADD": 1,
    "TP_REDUCE": 1
  }
}
```

## Decision
```json
{
  "uptrend_provider_locked": false,
  "implementation_allowed_now": false,
  "selected_candidate": {
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
  "baseline": {
    "path": "src/engine/backtest.py",
    "name": "run_stateful_simulation",
    "action_like_dict_count": 16,
    "literal_action_counts": {
      "BUY": 3,
      "ADD": 1,
      "TP_REDUCE": 1
    }
  },
  "conclusion": "UPTREND_PROVIDER_CANDIDATE_SELECTED_FOR_EQUIVALENCE_SMOKE",
  "recommended_next_action": "Proceed to 4C-2C-4E-D3: run a short-window UPTREND-only equivalence smoke comparing the selected candidate against run_stateful_simulation action/order behavior. Do not implement adapter yet.",
  "engineering_rule": "The selected UPTREND provider candidate is not allowed in adapter trading logic until equivalence against the existing run_stateful_simulation UPTREND behavior is demonstrated."
}
```

## Next Action

Proceed to 4C-2C-4E-D3: run a short-window UPTREND-only equivalence smoke comparing the selected candidate against run_stateful_simulation action/order behavior. Do not implement adapter yet.
