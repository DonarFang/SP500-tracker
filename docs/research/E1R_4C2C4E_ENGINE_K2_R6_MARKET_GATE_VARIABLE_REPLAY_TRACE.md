# E1R 4C-2C-4E-ENGINE-K2-R6 — Market Gate Variable Replay Trace

Generated At: `2026-07-10T12:26:00.748446+00:00`

## Purpose
Replay market gate variables required by the source-supported formula before patching standalone implementation.

## Source Evidence
```json
{
  "_gate_state_formula": [
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
  "daily_equity_target": [
    {
      "line": 1525,
      "text": "            \"market_gate_state\": _gate_state,"
    }
  ],
  "market_entry_allowed_no_gate": [
    {
      "line": 1399,
      "text": "            market_entry_allowed = True"
    }
  ],
  "market_entry_allowed_gate": [
    {
      "line": 1485,
      "text": "            market_entry_allowed = entry_capacity > 0"
    }
  ],
  "market_risk_off_gate": [
    {
      "line": 1483,
      "text": "            market_risk_off  = (market_state == \"CASH_MODE\") and not _shock_active"
    }
  ],
  "market_shock_gate": [
    {
      "line": 1484,
      "text": "            market_shock     = _shock_active"
    }
  ]
}
```

## Upstream Availability
```json
{
  "golden_master_has_market_entry_allowed": false,
  "golden_master_has_market_shock": false,
  "golden_master_has_market_risk_off": false,
  "golden_master_has_market_state": false,
  "golden_master_has__shock_active": false,
  "golden_master_has_entry_capacity": false
}
```

## Equivalence Report
```json
{
  "ok": true,
  "checked_assertions": [
    "daily_equity_market_gate_state_date_sequence",
    "formula_replayed_gate_state_matches_daily_equity_market_gate_state"
  ],
  "mismatch_count": 0,
  "mismatches": [],
  "summary": {
    "row_count": 62,
    "mismatch_count": 0,
    "expected_distribution": {
      "ALLOW": 53,
      "RISK_OFF": 8,
      "SHOCK": 1
    },
    "replayed_distribution": {
      "ALLOW": 53,
      "RISK_OFF": 8,
      "SHOCK": 1
    },
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  },
  "caveat": "This is formula-level replay from inverse target labels, not full upstream source-equivalent replay, because golden master rows do not persist market_entry_allowed and market_shock."
}
```

## Focused Rows
```json
[
  {
    "date": "2021-05-03",
    "daily_equity_market_gate_state": "ALLOW",
    "replayed_gate_state": "ALLOW",
    "market_entry_allowed": true,
    "market_shock": false,
    "market_risk_off": false,
    "market_state": null,
    "_shock_active": null,
    "entry_capacity": null,
    "spx_close": 4192.66,
    "spx_ma50": 4008.46,
    "spx_day_return_pct": 0.2748,
    "open_positions_count": 3,
    "pending_orders_count": 1,
    "exposure_pct": 15.09,
    "replay_mode": "minimal_inverse_from_target_allow",
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  },
  {
    "date": "2021-05-04",
    "daily_equity_market_gate_state": "ALLOW",
    "replayed_gate_state": "ALLOW",
    "market_entry_allowed": true,
    "market_shock": false,
    "market_risk_off": false,
    "market_state": null,
    "_shock_active": null,
    "entry_capacity": null,
    "spx_close": 4164.66,
    "spx_ma50": 4014.22,
    "spx_day_return_pct": -0.6678,
    "open_positions_count": 3,
    "pending_orders_count": 1,
    "exposure_pct": 15.01,
    "replay_mode": "minimal_inverse_from_target_allow",
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  },
  {
    "date": "2021-05-05",
    "daily_equity_market_gate_state": "ALLOW",
    "replayed_gate_state": "ALLOW",
    "market_entry_allowed": true,
    "market_shock": false,
    "market_risk_off": false,
    "market_state": null,
    "_shock_active": null,
    "entry_capacity": null,
    "spx_close": 4167.59,
    "spx_ma50": 4019.94,
    "spx_day_return_pct": 0.0703,
    "open_positions_count": 3,
    "pending_orders_count": 1,
    "exposure_pct": 15.15,
    "replay_mode": "minimal_inverse_from_target_allow",
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  },
  {
    "date": "2021-05-06",
    "daily_equity_market_gate_state": "ALLOW",
    "replayed_gate_state": "ALLOW",
    "market_entry_allowed": true,
    "market_shock": false,
    "market_risk_off": false,
    "market_state": null,
    "_shock_active": null,
    "entry_capacity": null,
    "spx_close": 4201.62,
    "spx_ma50": 4025.47,
    "spx_day_return_pct": 0.8165,
    "open_positions_count": 3,
    "pending_orders_count": 1,
    "exposure_pct": 15.18,
    "replay_mode": "minimal_inverse_from_target_allow",
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  },
  {
    "date": "2021-05-07",
    "daily_equity_market_gate_state": "ALLOW",
    "replayed_gate_state": "ALLOW",
    "market_entry_allowed": true,
    "market_shock": false,
    "market_risk_off": false,
    "market_state": null,
    "_shock_active": null,
    "entry_capacity": null,
    "spx_close": 4232.6,
    "spx_ma50": 4033.53,
    "spx_day_return_pct": 0.7373,
    "open_positions_count": 3,
    "pending_orders_count": 1,
    "exposure_pct": 15.44,
    "replay_mode": "minimal_inverse_from_target_allow",
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  },
  {
    "date": "2021-05-10",
    "daily_equity_market_gate_state": "RISK_OFF",
    "replayed_gate_state": "RISK_OFF",
    "market_entry_allowed": false,
    "market_shock": false,
    "market_risk_off": true,
    "market_state": null,
    "_shock_active": null,
    "entry_capacity": null,
    "spx_close": 4188.43,
    "spx_ma50": 4041.08,
    "spx_day_return_pct": -1.0436,
    "open_positions_count": 3,
    "pending_orders_count": 1,
    "exposure_pct": 15.2,
    "replay_mode": "minimal_inverse_from_target_risk_off",
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  },
  {
    "date": "2021-05-11",
    "daily_equity_market_gate_state": "RISK_OFF",
    "replayed_gate_state": "RISK_OFF",
    "market_entry_allowed": false,
    "market_shock": false,
    "market_risk_off": true,
    "market_state": null,
    "_shock_active": null,
    "entry_capacity": null,
    "spx_close": 4152.1,
    "spx_ma50": 4046.08,
    "spx_day_return_pct": -0.8674,
    "open_positions_count": 3,
    "pending_orders_count": 1,
    "exposure_pct": 14.79,
    "replay_mode": "minimal_inverse_from_target_risk_off",
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  },
  {
    "date": "2021-05-12",
    "daily_equity_market_gate_state": "SHOCK",
    "replayed_gate_state": "SHOCK",
    "market_entry_allowed": false,
    "market_shock": true,
    "market_risk_off": false,
    "market_state": null,
    "_shock_active": null,
    "entry_capacity": null,
    "spx_close": 4063.04,
    "spx_ma50": 4049.94,
    "spx_day_return_pct": -2.1449,
    "open_positions_count": 3,
    "pending_orders_count": 1,
    "exposure_pct": 14.01,
    "replay_mode": "minimal_inverse_from_target_shock",
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  },
  {
    "date": "2021-05-13",
    "daily_equity_market_gate_state": "RISK_OFF",
    "replayed_gate_state": "RISK_OFF",
    "market_entry_allowed": false,
    "market_shock": false,
    "market_risk_off": true,
    "market_state": null,
    "_shock_active": null,
    "entry_capacity": null,
    "spx_close": 4112.5,
    "spx_ma50": 4055.8,
    "spx_day_return_pct": 1.2173,
    "open_positions_count": 3,
    "pending_orders_count": 3,
    "exposure_pct": 14.47,
    "replay_mode": "minimal_inverse_from_target_risk_off",
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  },
  {
    "date": "2021-05-14",
    "daily_equity_market_gate_state": "RISK_OFF",
    "replayed_gate_state": "RISK_OFF",
    "market_entry_allowed": false,
    "market_shock": false,
    "market_risk_off": true,
    "market_state": null,
    "_shock_active": null,
    "entry_capacity": null,
    "spx_close": 4173.85,
    "spx_ma50": 4063.9,
    "spx_day_return_pct": 1.4918,
    "open_positions_count": 3,
    "pending_orders_count": 3,
    "exposure_pct": 14.66,
    "replay_mode": "minimal_inverse_from_target_risk_off",
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  },
  {
    "date": "2021-05-17",
    "daily_equity_market_gate_state": "RISK_OFF",
    "replayed_gate_state": "RISK_OFF",
    "market_entry_allowed": false,
    "market_shock": false,
    "market_risk_off": true,
    "market_state": null,
    "_shock_active": null,
    "entry_capacity": null,
    "spx_close": 4163.29,
    "spx_ma50": 4070.33,
    "spx_day_return_pct": -0.253,
    "open_positions_count": 3,
    "pending_orders_count": 3,
    "exposure_pct": 14.58,
    "replay_mode": "minimal_inverse_from_target_risk_off",
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  },
  {
    "date": "2021-05-18",
    "daily_equity_market_gate_state": "RISK_OFF",
    "replayed_gate_state": "RISK_OFF",
    "market_entry_allowed": false,
    "market_shock": false,
    "market_risk_off": true,
    "market_state": null,
    "_shock_active": null,
    "entry_capacity": null,
    "spx_close": 4127.83,
    "spx_ma50": 4076.46,
    "spx_day_return_pct": -0.8517,
    "open_positions_count": 3,
    "pending_orders_count": 2,
    "exposure_pct": 14.29,
    "replay_mode": "minimal_inverse_from_target_risk_off",
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  },
  {
    "date": "2021-05-19",
    "daily_equity_market_gate_state": "RISK_OFF",
    "replayed_gate_state": "RISK_OFF",
    "market_entry_allowed": false,
    "market_shock": false,
    "market_risk_off": true,
    "market_state": null,
    "_shock_active": null,
    "entry_capacity": null,
    "spx_close": 4115.68,
    "spx_ma50": 4081.26,
    "spx_day_return_pct": -0.2943,
    "open_positions_count": 3,
    "pending_orders_count": 2,
    "exposure_pct": 14.16,
    "replay_mode": "minimal_inverse_from_target_risk_off",
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  },
  {
    "date": "2021-05-20",
    "daily_equity_market_gate_state": "ALLOW",
    "replayed_gate_state": "ALLOW",
    "market_entry_allowed": true,
    "market_shock": false,
    "market_risk_off": false,
    "market_state": null,
    "_shock_active": null,
    "entry_capacity": null,
    "spx_close": 4159.12,
    "spx_ma50": 4086.47,
    "spx_day_return_pct": 1.0555,
    "open_positions_count": 3,
    "pending_orders_count": 3,
    "exposure_pct": 14.3,
    "replay_mode": "minimal_inverse_from_target_allow",
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  },
  {
    "date": "2021-05-21",
    "daily_equity_market_gate_state": "RISK_OFF",
    "replayed_gate_state": "RISK_OFF",
    "market_entry_allowed": false,
    "market_shock": false,
    "market_risk_off": true,
    "market_state": null,
    "_shock_active": null,
    "entry_capacity": null,
    "spx_close": 4155.86,
    "spx_ma50": 4090.8,
    "spx_day_return_pct": -0.0784,
    "open_positions_count": 3,
    "pending_orders_count": 3,
    "exposure_pct": 14.2,
    "replay_mode": "minimal_inverse_from_target_risk_off",
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  },
  {
    "date": "2021-05-24",
    "daily_equity_market_gate_state": "ALLOW",
    "replayed_gate_state": "ALLOW",
    "market_entry_allowed": true,
    "market_shock": false,
    "market_risk_off": false,
    "market_state": null,
    "_shock_active": null,
    "entry_capacity": null,
    "spx_close": 4197.05,
    "spx_ma50": 4095.88,
    "spx_day_return_pct": 0.9911,
    "open_positions_count": 3,
    "pending_orders_count": 3,
    "exposure_pct": 14.39,
    "replay_mode": "minimal_inverse_from_target_allow",
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  },
  {
    "date": "2021-06-18",
    "daily_equity_market_gate_state": "ALLOW",
    "replayed_gate_state": "ALLOW",
    "market_entry_allowed": true,
    "market_shock": false,
    "market_risk_off": false,
    "market_state": null,
    "_shock_active": null,
    "entry_capacity": null,
    "spx_close": 4166.45,
    "spx_ma50": 4181.59,
    "spx_day_return_pct": -1.3124,
    "open_positions_count": 3,
    "pending_orders_count": 3,
    "exposure_pct": 15.49,
    "replay_mode": "minimal_inverse_from_target_allow",
    "source_quality": "target_inverse_only_not_upstream_source_equivalent"
  }
]
```

## Validations
```json
{
  "market_gate_variable_replay_trace_complete": true,
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
  "k2_r5_loaded": true,
  "golden_master_loaded": true,
  "daily_equity_records_loaded": true,
  "source_evidence_cited": true,
  "source_chain_scanned": true,
  "upstream_source_equivalent_available": false,
  "target_inverse_replay_available": true,
  "target_inverse_replay_mismatch_count": 0,
  "target_inverse_replay_passed": true,
  "replay_artifact_written": true,
  "equivalence_report_written": true
}
```

## Decision
```json
{
  "k2_r6_variable_replay_trace_passed": true,
  "upstream_source_equivalent_available": false,
  "formula_patch_allowed_now": false,
  "candidate_extraction_allowed_now": false,
  "implementation_may_resume": false,
  "reason_patch_still_blocked": "K2-R6 obtained formula-level target replay but did not obtain true upstream market_entry_allowed/market_shock from legacy internals. A standalone patch can now be designed to require these inputs, but historical equivalence must be checked against target-inverse replay unless legacy instrumentation is added.",
  "acceptable_patch_shape_next": "K2-R7 may patch compute_market_gate_state only as a pure function requiring market_entry_allowed and market_shock inputs. It must not accept spx_close/spx_ma50/spx_day_return as sufficient source-equivalent inputs.",
  "next_required_stage": "4C-2C-4E-ENGINE-K2-R7-MARKET_GATE_EQUIVALENCE_PATCH",
  "conclusion": "K2_R6_PASS_TARGET_REPLAY_READY_FOR_INPUT_REQUIRED_EQUIVALENCE_PATCH",
  "recommended_next_action": "Run 4C-2C-4E-ENGINE-K2-R7-MARKET_GATE_EQUIVALENCE_PATCH: patch a pure input-required market gate function and validate against K2-R6 replay rows with mismatch_count=0."
}
```
