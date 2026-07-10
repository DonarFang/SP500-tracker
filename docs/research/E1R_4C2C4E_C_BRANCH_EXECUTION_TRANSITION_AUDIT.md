# E1R 4C-2C-4E-C — Branch Execution / Transition Audit

Generated At: `2026-07-10T02:41:45.303213+00:00`

## Purpose

This audit checks whether the existing backtest engine truly executes E1R regime branches inside one continuous account, or only records/aligns regime and sidecar information.

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

## Safety Validations
```json
{
  "audit_only_no_backtest_run": true,
  "full_5y_backtest_run": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "strategy_files_unchanged": true,
  "invalid_artifacts_used_as_source": false,
  "composer_used_for_result": false,
  "return_curve_stitching_used": false
}
```

## Evidence Validations
```json
{
  "b3_report_exists": true,
  "engine_regime_usage_audited": true,
  "sidecar_data_available_on_ma_conflict": true,
  "b3_sidecar_execution_not_proven": true,
  "decision_generated": true
}
```

## Engine Regime Usage Summary
```json
{
  "run_stateful_path": "src/engine/backtest.py",
  "run_stateful_start_line": 763,
  "run_stateful_end_line": 2486,
  "e1r_regime_daily_present": true,
  "e1r_wiring_present": true,
  "sidecar_call_present_inside_engine": false,
  "explicit_sideways_condition_present": true,
  "explicit_downtrend_condition_present": true,
  "explicit_cash_defensive_transition_present": true,
  "branch_specific_order_generation_present": false,
  "interpretation": [
    "Engine reads E1R regime wiring fields.",
    "Engine does not call sidecar builder inside run_stateful_simulation.",
    "Engine mentions SIDEWAYS/MA_CONFLICT, but branch-specific order execution is not proven.",
    "Engine may contain cash/defensive transition logic; inspect contexts."
  ]
}
```

## B3 Transition Behavior Summary
```json
{
  "b3_report_exists": true,
  "b3_status": "CONTINUOUS_STATEFUL_SMOKE_COMPLETE",
  "b3_conclusion": "4C2C4E_B3_SMOKE_FAILED_REVIEW_BEFORE_CONTINUING",
  "b3_conclusion_known_bug": true,
  "b3_validation_all_expected_true": true,
  "regime_counts": {
    "UPTREND": 19,
    "SIDEWAYS": 78,
    "DOWNTREND": 27
  },
  "subclass_counts": {
    "NO_SUBCLASS": 46,
    "MA_CONFLICT": 39,
    "DETERIORATION_TRANSITION": 39
  },
  "branch_plan_counts": {
    "UPTREND_ENGINE_BRANCH": 19,
    "SIDEWAYS_MA_CONFLICT_SIDECAR_AVAILABLE": 39,
    "CASH_DEFENSIVE_EXPECTED": 66
  },
  "sideways_ma_conflict_rows_sample_count": 11,
  "cash_defensive_rows_sample_count": 0,
  "sidecar_data_available_on_ma_conflict": true,
  "sidecar_execution_proven_by_b3_rows": false,
  "sidecar_execution_not_proven_reason": "B3 rows show sidecar data availability on MA_CONFLICT dates, but they do not show account positions being replaced by or opened from sidecar holdings. The sample retains existing open positions through UPTREND → SIDEWAYS transition."
}
```

## Decision
```json
{
  "engine_reads_e1r_regime": true,
  "engine_calls_sidecar_inside_run_stateful": false,
  "engine_has_sideways_branch_order_generation_evidence": false,
  "b3_proves_sidecar_execution": false,
  "existing_engine_sufficient_for_official_4e": false,
  "conclusion": "EXISTING_ENGINE_BRANCH_EXECUTION_NOT_PROVEN_NEED_CONTINUOUS_STATEFUL_ADAPTER_DESIGN",
  "recommended_next_action": "Proceed to 4C-2C-4E-D: design a new continuous-stateful E1R adapter/orchestrator that owns cash/positions and explicitly executes regime transitions. Do not use composer or stitched results.",
  "reason": "Official E1R requires actual branch execution in one continuous account. Sidecar data availability is not enough; account orders/positions must be produced by the SIDEWAYS/MA_CONFLICT branch."
}
```

## Next Action

Proceed to 4C-2C-4E-D: design a new continuous-stateful E1R adapter/orchestrator that owns cash/positions and explicitly executes regime transitions. Do not use composer or stitched results.
