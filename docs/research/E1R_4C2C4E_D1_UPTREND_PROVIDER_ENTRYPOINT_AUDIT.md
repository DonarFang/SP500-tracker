# E1R 4C-2C-4E-D1 — UPTREND Provider Entrypoint Audit

Generated At: `2026-07-10T02:56:36.235859+00:00`

## Purpose

Locate and lock the validated UPTREND candidate/order source before implementing the continuous-stateful E1R adapter.

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
  "prior_d_loaded": true,
  "run_stateful_audited": true,
  "internal_uptrend_logic_located": true,
  "action_shapes_audited": true,
  "decision_generated": true,
  "implementation_not_allowed_yet": true
}
```

## Prior D Evidence
```json
{
  "exists": true,
  "status": "CONTINUOUS_STATEFUL_ADAPTER_DESIGN_COMPLETE",
  "decision": {
    "c_audit_supports_adapter_need": true,
    "sidecar_provider_locked": true,
    "cash_defensive_provider_locked": true,
    "uptrend_provider_locked": false,
    "adapter_design_complete": true,
    "implementation_allowed_now": false,
    "conclusion": "ADAPTER_DESIGN_READY_BUT_UPTREND_PROVIDER_ENTRYPOINT_MUST_BE_LOCKED_BEFORE_IMPLEMENTATION",
    "recommended_next_action": "Proceed to 4C-2C-4E-D1: UPTREND provider entrypoint audit. Do not implement adapter trading logic until the validated UPTREND candidate/order source is locked."
  },
  "branch_provider_status": {
    "uptrend": "NEEDS_ENTRYPOINT_AUDIT_BEFORE_IMPLEMENTATION",
    "sideways": "AVAILABLE_AS_CANDIDATE_PROVIDER",
    "cash_defensive": "DESIGN_DEFINED"
  },
  "entrypoint_status": {
    "uptrend_provider_entrypoint_locked": false,
    "sidecar_provider_entrypoint_locked": true,
    "cash_defensive_provider_entrypoint_locked": true
  }
}
```

## Run Stateful UPTREND Audit Summary
```json
{
  "path": "src/engine/backtest.py",
  "function": "run_stateful_simulation",
  "start_line": 763,
  "end_line": 2486,
  "line_count": 1724,
  "static_evidence": {
    "contains_UPTREND": true,
    "contains_e1r_uptrend_execution_enabled": true,
    "contains_candidate_terms": true,
    "contains_buy_logic": true,
    "contains_add_logic": true,
    "contains_reduce_logic": true,
    "contains_exit_logic": true,
    "contains_position_state": true,
    "contains_market_gate": true,
    "contains_max_positions": true
  },
  "internal_uptrend_source_logic_located": true,
  "keyword_hits_count": 267
}
```

## External Provider Candidate Summary
```json
{
  "direct_standalone_uptrend_provider_count": 6,
  "likely_candidate_provider_count": 80,
  "likely_order_provider_count": 26,
  "likely_stateful_provider_count": 45
}
```

## Decision
```json
{
  "prior_d_requires_uptrend_provider_lock": true,
  "internal_run_stateful_uptrend_logic_located": true,
  "direct_standalone_provider_candidate_count": 6,
  "directly_callable_provider_locked": true,
  "provider_lock_status": "DIRECT_CANDIDATE_FOUND_NOT_VERIFIED",
  "action_dict_shapes_found": true,
  "implementation_allowed_now": false,
  "conclusion": "UPTREND_PROVIDER_DIRECT_ENTRYPOINT_CANDIDATE_FOUND_REVIEW_REQUIRED",
  "recommended_next_action": "Proceed to 4C-2C-4E-D2: verify the direct provider candidate against existing run_stateful_simulation behavior before adapter implementation.",
  "engineering_rule": "Do not re-invent UPTREND ranking/order logic. Adapter implementation must either call a verified provider or extract the existing run_stateful_simulation logic under a no-strategy-change equivalence test."
}
```

## Next Action

Proceed to 4C-2C-4E-D2: verify the direct provider candidate against existing run_stateful_simulation behavior before adapter implementation.
