# E1R 4C-2C-4E-ENGINE-K2-RCA — Market Gate Root Cause Analysis & Recovery Plan

Generated At: `2026-07-10T12:05:43.181844+00:00`

## Purpose
Stop implementation and document root cause analysis after repeated market gate extraction failures.

## Policy
```json
{
  "strategy_logic_changed": false,
  "audit_only": true,
  "implementation_paused": true,
  "formula_not_patched": true,
  "backtest_engine_run": false,
  "full_5y_backtest_run": false,
  "forward_runner_run": false,
  "candidate_generation_extracted": false,
  "buy_add_reduce_exit_extracted": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "frozen_strategy_files_changed": false
}
```

## Confirmed Findings
```json
[
  {
    "id": "F1",
    "finding": "The simplified K2 market gate formula is not equivalent to legacy output.",
    "evidence": {
      "expected_distribution": {
        "ALLOW": 53,
        "RISK_OFF": 8,
        "SHOCK": 1
      },
      "basic_formula_mismatch_count": 9,
      "exact_formula_candidates": []
    },
    "impact": "Standalone market gate cannot proceed to candidate extraction until fixed."
  },
  {
    "id": "F2",
    "finding": "The legacy RISK_OFF days in the golden master are not explained by same-day SPX close < same-day SPX MA50.",
    "evidence": [
      {
        "date": "2021-05-10",
        "spx_close": 4188.43,
        "spx_ma50": 4041.08,
        "spx_day_return_pct": -1.0436,
        "market_gate_state": "RISK_OFF"
      },
      {
        "date": "2021-05-11",
        "spx_close": 4152.1,
        "spx_ma50": 4046.08,
        "spx_day_return_pct": -0.8674,
        "market_gate_state": "RISK_OFF"
      },
      {
        "date": "2021-05-13",
        "spx_close": 4112.5,
        "spx_ma50": 4055.8,
        "spx_day_return_pct": 1.2173,
        "market_gate_state": "RISK_OFF"
      },
      {
        "date": "2021-05-14",
        "spx_close": 4173.85,
        "spx_ma50": 4063.9,
        "spx_day_return_pct": 1.4918,
        "market_gate_state": "RISK_OFF"
      },
      {
        "date": "2021-05-17",
        "spx_close": 4163.29,
        "spx_ma50": 4070.33,
        "spx_day_return_pct": -0.253,
        "market_gate_state": "RISK_OFF"
      },
      {
        "date": "2021-05-18",
        "spx_close": 4127.83,
        "spx_ma50": 4076.46,
        "spx_day_return_pct": -0.8517,
        "market_gate_state": "RISK_OFF"
      },
      {
        "date": "2021-05-19",
        "spx_close": 4115.68,
        "spx_ma50": 4081.26,
        "spx_day_return_pct": -0.2943,
        "market_gate_state": "RISK_OFF"
      },
      {
        "date": "2021-05-21",
        "spx_close": 4155.86,
        "spx_ma50": 4090.8,
        "spx_day_return_pct": -0.0784,
        "market_gate_state": "RISK_OFF"
      }
    ],
    "impact": "Formula must be traced from source variables, not inferred from rounded daily output fields."
  },
  {
    "id": "F3",
    "finding": "daily_equity_records.market_gate_state stores `_gate_state`; logging/daily_records use a separate local expression based on market_entry_allowed / market_shock.",
    "evidence": {
      "daily_equity_record_line": "L1525: \"market_gate_state\": _gate_state",
      "logging_gate_lines": [
        "L2137: gate_state = \"ALLOW\" if market_entry_allowed else (",
        "L2138:     \"SHOCK\" if market_shock else \"RISK_OFF\"",
        "L2155-L2158: daily_records market_gate_state uses market_entry_allowed / market_shock"
      ],
      "source": "docs/research/E1R_4C2C4E_ENGINE_K2_R3_MARKET_GATE_SOURCE_LINE_DRILLDOWN.json"
    },
    "impact": "The extraction target must be explicitly chosen: daily_equity_records._gate_state, not logger gate_state unless proven identical."
  }
]
```

## Unknowns
```json
[
  {
    "id": "U1",
    "unknown": "Exact assignment location and computation chain for `_gate_state` before line 1525.",
    "required_evidence": "Source lines showing `_gate_state = ...` and all variables feeding that assignment.",
    "blocking": true
  },
  {
    "id": "U2",
    "unknown": "Exact computation chain for `market_entry_allowed`, `market_risk_off`, and `market_shock` on every day.",
    "required_evidence": "Source lines for assignments and updates, plus row-level replay trace.",
    "blocking": true
  },
  {
    "id": "U3",
    "unknown": "Whether `_gate_state` is based on current-day values, previous-day values, execution-day alignment, or rounded/unrounded source arrays.",
    "required_evidence": "Variable-level trace for dates 2021-05-03 through 2021-05-24 and 2021-06-18.",
    "blocking": true
  }
]
```

## Root Causes
```json
[
  {
    "id": "RC1",
    "category": "Evidence discipline",
    "root_cause": "Implementation was attempted from an inferred formula before the exact source assignment chain was located.",
    "corrective_action": "No extraction implementation until source assignment line and dependencies are identified."
  },
  {
    "id": "RC2",
    "category": "Field identity",
    "root_cause": "Different gate-related fields were treated as equivalent: `_gate_state`, `gate_state`, and market_entry_allowed-derived state.",
    "corrective_action": "Define a field identity table before patching: source field, assignment line, consumer, and equivalence target."
  },
  {
    "id": "RC3",
    "category": "Process control",
    "root_cause": "After the first mismatch, the process continued into multiple audit stages without an explicit RCA gate.",
    "corrective_action": "Introduce a three-strike stop rule and RCA requirement for repeated failures around the same issue."
  },
  {
    "id": "RC4",
    "category": "Trace quality",
    "root_cause": "Existing golden master trace lacks variable-level market gate internals, so formula reconstruction from output rows alone is underdetermined.",
    "corrective_action": "Add an audit-only variable trace script that reads source/output and reports exact dependencies before any patch."
  }
]
```

## Recovery Plan
```json
{
  "stage": "4C-2C-4E-ENGINE-K2-RCA",
  "status": "STOP_IMPLEMENTATION_UNTIL_RCA_ACCEPTED",
  "do_not_do_next": [
    "Do not patch compute_market_gate_state yet.",
    "Do not proceed to candidate/ranking extraction.",
    "Do not run full 5Y.",
    "Do not generate official/dashboard result.",
    "Do not infer a formula from output rows alone."
  ],
  "required_next_stage": "4C-2C-4E-ENGINE-K2-R4-SOURCE_DEPENDENCY_TRACE",
  "required_next_stage_scope": [
    "Search explicitly for `_gate_state` assignment in src/engine/backtest.py.",
    "Search explicitly for `market_entry_allowed`, `market_risk_off`, and `market_shock` assignments.",
    "Build a variable dependency table with line numbers.",
    "Generate focused source snippets around each assignment.",
    "Extract row-level values for the mismatch window from the legacy run if available.",
    "Only after this dependency trace passes, write K2-R5 formula patch."
  ],
  "acceptance_criteria_before_formula_patch": [
    "`_gate_state` assignment line is found.",
    "Every variable used by `_gate_state` is traced to a source line.",
    "Extraction target is explicitly confirmed as `daily_equity_records.market_gate_state`.",
    "No unresolved unknowns U1-U3 remain.",
    "Patch proposal cites exact source lines."
  ],
  "process_rule_added": {
    "three_strike_rule": "If the same issue fails or is corrected incorrectly around three times, stop implementation and perform RCA before continuing.",
    "evidence_rule": "No source-code extraction patch may be implemented from assumption. The patch must cite source lines, logs, or test evidence."
  }
}
```

## Decision
```json
{
  "k2_rca_passed": true,
  "implementation_may_resume": false,
  "formula_patch_allowed_now": false,
  "candidate_extraction_allowed_now": false,
  "required_next_stage": "4C-2C-4E-ENGINE-K2-R4-SOURCE_DEPENDENCY_TRACE",
  "conclusion": "K2_RCA_PASS_IMPLEMENTATION_PAUSED_READY_FOR_SOURCE_DEPENDENCY_TRACE",
  "recommended_next_action": "Run K2-R4 source dependency trace to find `_gate_state` and all upstream variables before any formula patch."
}
```
