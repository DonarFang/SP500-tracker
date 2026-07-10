# E1R 4C-2C-4E-ENGINE-K2-R5 — Formula Patch Proposal

Generated At: `2026-07-10T12:17:44.385213+00:00`

## Purpose
Produce a source-line-cited market gate patch proposal without patching implementation.

## Source Evidence
```json
{
  "daily_equity_target": {
    "line": 1525,
    "text": "            \"market_gate_state\": _gate_state,",
    "meaning": "Golden-master equivalence target is daily_equity_records.market_gate_state, which stores _gate_state."
  },
  "_gate_state_assignment_context": {
    "lines": "1510-1512",
    "context": [
      {
        "line": 1510,
        "text": "        _gate_state = ("
      },
      {
        "line": 1511,
        "text": "            \"ALLOW\" if market_entry_allowed else"
      },
      {
        "line": 1512,
        "text": "            \"SHOCK\" if market_shock else \"RISK_OFF\""
      }
    ],
    "meaning": "_gate_state is derived from market_entry_allowed and market_shock."
  },
  "market_entry_allowed_assignments": [
    {
      "line": 1399,
      "text": "            market_entry_allowed = True",
      "rhs_names": []
    },
    {
      "line": 1485,
      "text": "            market_entry_allowed = entry_capacity > 0",
      "rhs_names": [
        "entry_capacity"
      ]
    }
  ],
  "market_risk_off_assignments": [
    {
      "line": 1397,
      "text": "            market_risk_off  = False",
      "rhs_names": []
    },
    {
      "line": 1483,
      "text": "            market_risk_off  = (market_state == \"CASH_MODE\") and not _shock_active",
      "rhs_names": [
        "_shock_active",
        "market_state"
      ]
    }
  ],
  "market_shock_assignments": [
    {
      "line": 1398,
      "text": "            market_shock     = False",
      "rhs_names": []
    },
    {
      "line": 1484,
      "text": "            market_shock     = _shock_active",
      "rhs_names": [
        "_shock_active"
      ]
    }
  ],
  "logger_gate_context": {
    "lines": "2137-2139",
    "context": [
      {
        "line": 2137,
        "text": "            gate_state = \"ALLOW\" if market_entry_allowed else ("
      },
      {
        "line": 2138,
        "text": "                \"SHOCK\" if market_shock else \"RISK_OFF\""
      },
      {
        "line": 2139,
        "text": "            )"
      }
    ],
    "meaning": "Logger gate_state uses the same local expression pattern but is not the primary equivalence target."
  }
}
```

## Recovered Understanding
```json
{
  "previous_wrong_model": "market_gate_state = SHOCK if SPX day return <= -2%; else RISK_OFF if SPX close < SPX MA50; else ALLOW",
  "source_supported_model": "_gate_state = ALLOW if market_entry_allowed else SHOCK if market_shock else RISK_OFF",
  "why_previous_model_failed": [
    "RISK_OFF is not a direct same-day SPX<MA50 display-field comparison.",
    "daily_equity_records target stores _gate_state, not a standalone formula over rounded output fields.",
    "market_entry_allowed depends on entry_capacity under gate-enabled branch.",
    "market_shock depends on _shock_active under gate-enabled branch."
  ]
}
```

## Patch Proposal
```json
{
  "target_file": "src/e1r_engine/uptrend_core.py",
  "target_api": "compute_market_gate_state",
  "proposal_type": "source-line-cited formula correction",
  "equivalence_target": "daily_equity_records.market_gate_state",
  "equivalence_target_source_line": "src/engine/backtest.py:L1525",
  "do_not_replicate": [
    "Do not compute RISK_OFF directly from same-day spx_close < spx_ma50.",
    "Do not compute SHOCK directly from rounded daily_equity_records.spx_day_return_pct unless it is only used as a display field.",
    "Do not use logger gate_state as the equivalence target when daily_equity_records stores _gate_state."
  ],
  "required_formula": {
    "source_lines": [
      "src/engine/backtest.py:L1510-L1512"
    ],
    "formula": "_gate_state = 'ALLOW' if market_entry_allowed else ('SHOCK' if market_shock else 'RISK_OFF')",
    "required_inputs": [
      "market_entry_allowed",
      "market_shock"
    ],
    "optional_trace_inputs_for_explainability": [
      "market_risk_off",
      "market_state",
      "_shock_active",
      "entry_capacity",
      "spx_close_t",
      "spx_ma50_t",
      "spx_day_return"
    ]
  },
  "implementation_shape_for_k2_r6": {
    "new_or_updated_dataclass": "MarketGateDecision",
    "recommended_method_signature": "compute_market_gate_state(date, market_entry_allowed, market_shock, market_risk_off=None, raw=None) -> MarketGateDecision",
    "state_logic": [
      "if market_entry_allowed: state = 'ALLOW'",
      "elif market_shock: state = 'SHOCK'",
      "else: state = 'RISK_OFF'"
    ],
    "reason_logic": [
      "ALLOW -> market_entry_allowed_true",
      "SHOCK -> market_entry_blocked_by_market_shock",
      "RISK_OFF -> market_entry_blocked_by_market_risk_off_or_capacity"
    ]
  },
  "input_policy": {
    "short_window_k2_r6": "Use source-equivalent fields when available. For the existing golden master, market_entry_allowed and market_shock are not separately persisted, so K2-R6 must either derive them from a source-equivalent replay trace or intentionally mark this as not patchable from daily rows alone.",
    "important_constraint": "A patch that only consumes spx_close, spx_ma50, and spx_day_return_pct is not source-equivalent."
  },
  "blocking_check_before_k2_r6": [
    {
      "check": "Can K2-R6 obtain market_entry_allowed and market_shock for each daily_equity row?",
      "required_answer": "yes",
      "if_no": "Do not patch formula; first generate variable-level replay trace from legacy run."
    },
    {
      "check": "Is daily_equity_records.market_gate_state the confirmed target?",
      "required_answer": "yes",
      "source_line": "src/engine/backtest.py:L1525"
    },
    {
      "check": "Will K2-R6 avoid direct SPX<MA50 formula?",
      "required_answer": "yes"
    }
  ]
}
```

## Next Step Decision
```json
{
  "k2_r6_should_patch_now": false,
  "reason": "The formula target is now source-supported, but the current golden master daily rows do not persist market_entry_allowed and market_shock as standalone fields. A direct patch using only daily rows would repeat the same evidence error. K2-R6 must first include a source-equivalent variable replay input or fail closed.",
  "recommended_next_stage": "4C-2C-4E-ENGINE-K2-R6-MARKET_GATE_VARIABLE_REPLAY_TRACE",
  "why_this_is_not_path_divergence": "This is the minimum required step to satisfy the K2-RCA acceptance rule: no formula patch until all inputs used by the formula are available and source-cited.",
  "stage_after_r6_if_pass": "4C-2C-4E-ENGINE-K2-R7-MARKET_GATE_EQUIVALENCE_PATCH"
}
```

## Validations
```json
{
  "formula_patch_proposal_complete": true,
  "strategy_logic_changed": false,
  "audit_only": true,
  "formula_not_patched": true,
  "backtest_engine_run": false,
  "full_5y_backtest_run": false,
  "forward_runner_run": false,
  "candidate_generation_extracted": false,
  "buy_add_reduce_exit_extracted": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "strategy_files_unchanged": true,
  "k2_rca_loaded": true,
  "k2_r4_loaded": true,
  "k2_r4_unresolved_empty": true,
  "daily_equity_target_cited": true,
  "_gate_state_assignment_cited": true,
  "direct_spx_ma50_formula_rejected": true,
  "required_inputs_identified": true,
  "patch_blocking_check_defined": true
}
```

## Decision
```json
{
  "k2_r5_formula_patch_proposal_passed": true,
  "formula_patch_allowed_now": false,
  "implementation_may_resume": false,
  "candidate_extraction_allowed_now": false,
  "next_required_stage": "4C-2C-4E-ENGINE-K2-R6-MARKET_GATE_VARIABLE_REPLAY_TRACE",
  "conclusion": "K2_R5_PASS_PATCH_PROPOSAL_READY_FOR_VARIABLE_REPLAY_TRACE",
  "recommended_next_action": "Run 4C-2C-4E-ENGINE-K2-R6-MARKET_GATE_VARIABLE_REPLAY_TRACE to obtain market_entry_allowed and market_shock per daily row before patching standalone equivalence."
}
```
