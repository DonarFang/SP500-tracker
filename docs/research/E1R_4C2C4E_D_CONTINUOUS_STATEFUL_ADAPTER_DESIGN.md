# E1R 4C-2C-4E-D — Continuous-Stateful Adapter / Orchestrator Design

Generated At: `2026-07-10T02:48:19.575303+00:00`

## Purpose

Design a formal E1R adapter/orchestrator after 4E-C confirmed that the existing `run_stateful_simulation` reads regime data but does not prove full SIDEWAYS sidecar branch execution inside the account engine.

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

## Prior Evidence
```json
{
  "c_report_exists": true,
  "b2_report_exists": true,
  "b3_report_exists": true,
  "c_decision": {
    "engine_reads_e1r_regime": true,
    "engine_calls_sidecar_inside_run_stateful": false,
    "engine_has_sideways_branch_order_generation_evidence": false,
    "b3_proves_sidecar_execution": false,
    "existing_engine_sufficient_for_official_4e": false,
    "conclusion": "EXISTING_ENGINE_BRANCH_EXECUTION_NOT_PROVEN_NEED_CONTINUOUS_STATEFUL_ADAPTER_DESIGN",
    "recommended_next_action": "Proceed to 4C-2C-4E-D: design a new continuous-stateful E1R adapter/orchestrator that owns cash/positions and explicitly executes regime transitions. Do not use composer or stitched results.",
    "reason": "Official E1R requires actual branch execution in one continuous account. Sidecar data availability is not enough; account orders/positions must be produced by the SIDEWAYS/MA_CONFLICT branch."
  },
  "b2_assumption_contract": {
    "status": "BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT_COMPLETE",
    "assumption_key_count": 44,
    "required_without_default_keys": [
      "add_size",
      "buy_size",
      "max_positions",
      "max_single_size",
      "total_one_way"
    ],
    "unresolved_required_keys": []
  },
  "b3_smoke_summary": {
    "status": "CONTINUOUS_STATEFUL_SMOKE_COMPLETE",
    "conclusion": "4C2C4E_B3_SMOKE_FAILED_REVIEW_BEFORE_CONTINUING",
    "known_conclusion_bug": true,
    "engine_summary": {
      "record_count": 124,
      "regime_counts": {
        "UPTREND": 19,
        "SIDEWAYS": 78,
        "DOWNTREND": 27
      },
      "branch_plan_counts": {
        "UPTREND_ENGINE_BRANCH": 19,
        "SIDEWAYS_MA_CONFLICT_SIDECAR_AVAILABLE": 39,
        "CASH_DEFENSIVE_EXPECTED": 66
      },
      "max_open_positions": 2,
      "open_position_violations_count": 0
    },
    "sidecar_summary": {
      "ok": true,
      "record_count": 123,
      "active_count": 39,
      "active_regime_counts": {
        "SIDEWAYS": 39
      },
      "active_subclass_counts": {
        "MA_CONFLICT": 39
      },
      "selected_count_max": 10,
      "holdings_len_max": 10,
      "gross_exposure_max": 0.25,
      "strict_active_ma_conflict_count": 39
    }
  },
  "c_key_facts": {
    "status": "BRANCH_EXECUTION_TRANSITION_AUDIT_COMPLETE",
    "engine_reads_e1r_regime": true,
    "engine_calls_sidecar_inside_run_stateful": false,
    "engine_has_sideways_branch_order_generation_evidence": false,
    "b3_proves_sidecar_execution": false,
    "existing_engine_sufficient_for_official_4e": false,
    "conclusion": "EXISTING_ENGINE_BRANCH_EXECUTION_NOT_PROVEN_NEED_CONTINUOUS_STATEFUL_ADAPTER_DESIGN"
  }
}
```

## Adapter Contract
```json
{
  "adapter_name": "E1RContinuousStatefulAdapter",
  "proposed_module": "src/engine/e1r_continuous_stateful_adapter.py",
  "purpose": "Official E1R 5Y continuous-stateful account orchestrator.",
  "core_principle": "One account, one timeline, continuous cash/positions, daily mark-to-market, explicit regime branch execution.",
  "non_goals": [
    "Do not compose or stitch return curves.",
    "Do not read invalid historical result artifacts.",
    "Do not treat sidecar Top10 as live account holdings.",
    "Do not modify frozen strategy files in adapter design stage.",
    "Do not hide transition behavior inside undocumented assumptions."
  ],
  "account_state_schema": {
    "cash": "float",
    "positions": {
      "symbol": "str",
      "shares": "float",
      "cost_basis": "float",
      "entry_date": "YYYY-MM-DD",
      "branch_origin": "UPTREND | SIDEWAYS_MA_CONFLICT",
      "last_action": "BUY | ADD | REDUCE | HOLD | EXIT",
      "holding_days": "int",
      "metadata": "dict"
    },
    "total_equity": "cash + market_value(positions)",
    "open_positions_count": "len(positions)",
    "max_open_positions": 3
  },
  "daily_record_schema": {
    "date": "YYYY-MM-DD",
    "regime": "UPTREND | SIDEWAYS | DOWNTREND",
    "subclass": "NO_SUBCLASS | MA_CONFLICT | DETERIORATION_TRANSITION | RECOVERY_TRANSITION",
    "active_branch": "UPTREND | SIDEWAYS_MA_CONFLICT | CASH_DEFENSIVE",
    "cash": "float",
    "positions_value": "float",
    "total_equity": "float",
    "open_positions_count": "int <= 3",
    "orders": "list[Order]",
    "candidate_source": "UPTREND_SIGNAL_PROVIDER | SIDECAR_TOP10 | NONE",
    "guard_flags": "dict"
  },
  "order_schema": {
    "date": "YYYY-MM-DD",
    "symbol": "str",
    "action": "BUY | ADD | REDUCE | EXIT | HOLD",
    "quantity_or_weight": "float",
    "price": "float",
    "branch": "UPTREND | SIDEWAYS_MA_CONFLICT | CASH_DEFENSIVE",
    "reason": "str"
  }
}
```

## Daily Loop Design
```json
{
  "pseudocode": [
    "initialize cash = 100000, positions = {}",
    "for each trading day in aligned 5Y timeline:",
    "    mark_to_market existing positions using close price",
    "    read regime and subclass for date",
    "    if regime == UPTREND:",
    "        branch = UPTREND",
    "        candidates/orders = uptrend_signal_provider(date, current_state)",
    "        execute orders with account-level max_positions <= 3",
    "    elif regime == SIDEWAYS and subclass == MA_CONFLICT:",
    "        branch = SIDEWAYS_MA_CONFLICT",
    "        candidates = sidecar_top10_provider(date)",
    "        convert sidecar Top10 into live account target <= 3 positions",
    "        execute transition orders explicitly",
    "    else:",
    "        branch = CASH_DEFENSIVE",
    "        execute defensive transition orders explicitly",
    "    enforce open_positions_count <= 3",
    "    record daily account state"
  ],
  "hard_guards": [
    "Fail if open_positions_count > 3 on any date.",
    "Fail if any invalid artifact path is read.",
    "Fail if composer is imported or called for official result.",
    "Fail if sidecar holdings_len > 3 is interpreted as live holdings.",
    "Fail if DETERIORATION/RECOVERY/DOWNTREND branch leaves positions open without explicit approved rule.",
    "Fail if daily record lacks cash, positions_value, total_equity, active_branch."
  ]
}
```

## Transition Policy
```json
{
  "status": "DESIGN_REQUIRES_USER_CONFIRMATION_BEFORE_IMPLEMENTATION",
  "policy_options": {
    "UPTREND_to_SIDEWAYS_MA_CONFLICT": {
      "recommended": "transition_to_sidecar_targets",
      "meaning": "Existing UPTREND positions are not automatically assumed valid. Adapter compares current holdings with sidecar Top10 candidate pool and moves toward <=3 sidecar live targets.",
      "why": "C audit showed current engine kept UPTREND positions during SIDEWAYS while sidecar was only data-available; formal E1R requires branch execution.",
      "implementation_guard": "Every kept position must be explicitly tagged as also passing the SIDEWAYS sidecar candidate/target rule; otherwise exit or reduce by approved transition rule."
    },
    "SIDEWAYS_MA_CONFLICT_to_UPTREND": {
      "recommended": "transition_to_uptrend_targets",
      "meaning": "Sidecar-origin positions are re-evaluated by UPTREND branch. They can be kept only if current UPTREND branch would hold them.",
      "implementation_guard": "No position silently changes branch_origin without a logged transition decision."
    },
    "ANY_to_DETERIORATION_OR_RECOVERY": {
      "recommended": "cash_defensive_exit",
      "meaning": "Exit live equity positions and hold cash unless a defensive holding rule is explicitly approved later.",
      "implementation_guard": "open_positions_count should become 0 after transition execution window."
    },
    "ANY_to_DOWNTREND": {
      "recommended": "cash_defensive_exit",
      "meaning": "Exit live equity positions and hold cash.",
      "implementation_guard": "open_positions_count should become 0 after transition execution window."
    }
  },
  "unresolved_decision": "Whether transition exits occur same close, next close, or existing engine's execution convention. This must be confirmed before official full 5Y."
}
```

## Branch Providers
```json
{
  "UPTREND_signal_provider": {
    "status": "NEEDS_ENTRYPOINT_AUDIT_BEFORE_IMPLEMENTATION",
    "goal": "Reuse existing validated UPTREND candidate/order logic without modifying frozen strategy files.",
    "allowed_sources": [
      "Existing leader score / rank / buy candidate functions if callable independently.",
      "Existing run_stateful_simulation internals only if extracted into a non-strategy-changing provider after approval."
    ],
    "not_allowed": [
      "Use old invalid result artifacts as UPTREND source.",
      "Approximate UPTREND rules by a new ranking formula without explicit approval."
    ],
    "next_audit_needed": "Locate exact existing UPTREND candidate/order generation logic and define a read-only provider API."
  },
  "SIDEWAYS_MA_CONFLICT_provider": {
    "status": "AVAILABLE_AS_CANDIDATE_PROVIDER",
    "source": "src.engine.e1r_sidecar_sleeve.build_e1r_sidecar_sleeve",
    "confirmed_behavior": [
      "active only in SIDEWAYS / MA_CONFLICT in strict sidecar audit",
      "Top10 selected_count is candidate/basket pool",
      "gross_exposure = 0.25 in original sidecar model"
    ],
    "adapter_responsibility": [
      "Convert Top10 candidate pool into <=3 live account targets.",
      "Generate real account orders.",
      "Record branch_origin = SIDEWAYS_MA_CONFLICT."
    ]
  },
  "CASH_DEFENSIVE_provider": {
    "status": "DESIGN_DEFINED",
    "source": "adapter-owned transition logic",
    "adapter_responsibility": [
      "Generate EXIT orders for live equity positions.",
      "Hold cash after transition.",
      "Record active_branch = CASH_DEFENSIVE."
    ]
  }
}
```

## Validation Matrix
```json
{
  "adapter_smoke_validations_for_next_stage": {
    "strategy_files_unchanged": true,
    "invalid_artifacts_not_used": true,
    "composer_not_used": true,
    "return_curve_stitching_not_used": true,
    "single_account_state_owned_by_adapter": true,
    "cash_positions_continuous": true,
    "daily_mark_to_market_present": true,
    "active_branch_recorded_daily": true,
    "uptrend_branch_orders_observed": true,
    "sideways_ma_conflict_branch_orders_observed": true,
    "cash_defensive_exit_orders_observed": true,
    "sidecar_top10_never_live_holdings_10": true,
    "max_open_positions_le_3": true,
    "position_violations_zero": true,
    "transition_logs_present": true,
    "official_result_generated": false,
    "full_5y_backtest_run": false
  },
  "official_5y_validations_later": {
    "full_timeline_covered": "2021-06-11 to 2026-06-18 or current aligned window",
    "daily_record_count_matches_trading_days": true,
    "open_positions_count_max_le_3": true,
    "cash_defensive_regimes_open_positions_zero_or_explicitly_approved": true,
    "orders_have_branch_and_reason": true,
    "equity_curve_derived_from_account_state": true,
    "no_result_stitching": true,
    "no_invalid_artifact_dependency": true
  }
}
```

## Decision
```json
{
  "c_audit_supports_adapter_need": true,
  "sidecar_provider_locked": true,
  "cash_defensive_provider_locked": true,
  "uptrend_provider_locked": false,
  "adapter_design_complete": true,
  "implementation_allowed_now": false,
  "conclusion": "ADAPTER_DESIGN_READY_BUT_UPTREND_PROVIDER_ENTRYPOINT_MUST_BE_LOCKED_BEFORE_IMPLEMENTATION",
  "recommended_next_action": "Proceed to 4C-2C-4E-D1: UPTREND provider entrypoint audit. Do not implement adapter trading logic until the validated UPTREND candidate/order source is locked."
}
```

## Next Action

Proceed to 4C-2C-4E-D1: UPTREND provider entrypoint audit. Do not implement adapter trading logic until the validated UPTREND candidate/order source is locked.
