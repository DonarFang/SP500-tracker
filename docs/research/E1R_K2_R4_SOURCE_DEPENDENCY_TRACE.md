# E1R K2-R4 — Source Dependency Trace

Generated At: `2026-07-10T12:11:36.139872+00:00`

Full stage name: `4C-2C-4E-ENGINE-K2-R4-SOURCE_DEPENDENCY_TRACE`

## Purpose
Trace `_gate_state` and upstream market gate variables to source assignment lines before any formula patch.

## Required Chain
```json
{
  "_gate_state": {
    "assignment_lines": [
      {
        "line": 1510,
        "text": "        _gate_state = (",
        "rhs_names": []
      }
    ],
    "reference_lines": [
      {
        "line": 1510,
        "kind": "assignment",
        "text": "        _gate_state = ("
      },
      {
        "line": 1525,
        "kind": "reference",
        "text": "            \"market_gate_state\": _gate_state,"
      }
    ]
  },
  "market_entry_allowed": {
    "assignment_lines": [
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
    "reference_lines": [
      {
        "line": 1399,
        "kind": "assignment",
        "text": "            market_entry_allowed = True"
      },
      {
        "line": 1485,
        "kind": "assignment",
        "text": "            market_entry_allowed = entry_capacity > 0"
      },
      {
        "line": 1491,
        "kind": "control",
        "text": "            if market_entry_allowed:"
      },
      {
        "line": 1511,
        "kind": "reference",
        "text": "            \"ALLOW\" if market_entry_allowed else"
      },
      {
        "line": 1717,
        "kind": "control",
        "text": "            if e1r_buy_candidates and market_entry_allowed:"
      },
      {
        "line": 1823,
        "kind": "control",
        "text": "                    if not market_entry_allowed:"
      },
      {
        "line": 1875,
        "kind": "control",
        "text": "                    if not market_entry_allowed:"
      },
      {
        "line": 1971,
        "kind": "control",
        "text": "                if action == \"ADD\" and not market_entry_allowed:"
      },
      {
        "line": 2137,
        "kind": "reference",
        "text": "            gate_state = \"ALLOW\" if market_entry_allowed else ("
      },
      {
        "line": 2156,
        "kind": "reference",
        "text": "                    \"ALLOW\" if market_entry_allowed else"
      }
    ]
  },
  "market_risk_off": {
    "assignment_lines": [
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
    "reference_lines": [
      {
        "line": 1397,
        "kind": "assignment",
        "text": "            market_risk_off  = False"
      },
      {
        "line": 1483,
        "kind": "assignment",
        "text": "            market_risk_off  = (market_state == \"CASH_MODE\") and not _shock_active"
      },
      {
        "line": 1487,
        "kind": "control",
        "text": "            if market_risk_off:"
      }
    ]
  },
  "market_shock": {
    "assignment_lines": [
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
    "reference_lines": [
      {
        "line": 1075,
        "kind": "output",
        "text": "        \"market_shock\": 0,"
      },
      {
        "line": 1398,
        "kind": "assignment",
        "text": "            market_shock     = False"
      },
      {
        "line": 1484,
        "kind": "assignment",
        "text": "            market_shock     = _shock_active"
      },
      {
        "line": 1489,
        "kind": "control",
        "text": "            if market_shock:"
      },
      {
        "line": 1490,
        "kind": "output",
        "text": "                market_gate_days[\"market_shock\"] += 1"
      },
      {
        "line": 1512,
        "kind": "reference",
        "text": "            \"SHOCK\" if market_shock else \"RISK_OFF\""
      },
      {
        "line": 1824,
        "kind": "reference",
        "text": "                        reason = \"market_shock_block\" if market_shock else \"market_risk_off_block\""
      },
      {
        "line": 1876,
        "kind": "reference",
        "text": "                        reason = \"market_shock_block\" if market_shock else \"market_risk_off_block\""
      },
      {
        "line": 1972,
        "kind": "reference",
        "text": "                    reason = \"market_shock_block\" if market_shock else \"market_risk_off_block\""
      },
      {
        "line": 2138,
        "kind": "reference",
        "text": "                \"SHOCK\" if market_shock else \"RISK_OFF\""
      },
      {
        "line": 2157,
        "kind": "reference",
        "text": "                    \"SHOCK\" if market_shock else \"RISK_OFF\""
      },
      {
        "line": 2333,
        "kind": "output",
        "text": "                f\"shock={market_gate_days['market_shock']}\")"
      }
    ]
  }
}
```

## Unresolved
```json
[]
```

## Validations
```json
{
  "source_dependency_trace_complete": true,
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
  "run_stateful_simulation_bounds_found": true,
  "dependency_table_built": true,
  "_gate_state_occurrences_found": true,
  "_gate_state_assignment_found": true,
  "market_entry_allowed_assignment_found": true,
  "market_risk_off_assignment_found": true,
  "market_shock_assignment_found": true,
  "unresolved_blocking_count": 0
}
```

## Decision
```json
{
  "k2_r4_source_dependency_trace_passed": true,
  "implementation_may_resume": false,
  "formula_patch_allowed_now": false,
  "candidate_extraction_allowed_now": false,
  "unresolved": [],
  "next_stage_if_pass": "K2-R5: formula patch proposal with source-line citations",
  "next_stage_if_fail": "K2-R4B: targeted multiline/source parser for unresolved variables",
  "conclusion": "K2_R4_PASS_READY_FOR_PATCH_PROPOSAL",
  "recommended_next_action": "If unresolved is empty, prepare K2-R5 patch proposal citing exact source lines. If unresolved exists, run targeted trace only for missing variables."
}
```
