# E1R 4C-2C-4E-ENGINE-K2-R12B — Market Gate Equivalence Gap RCA

Generated At: `2026-07-11T05:47:27.539984+00:00`

## Purpose
Explain R12 failure, inspect R7/R8 structure, preserve failed evidence, and define a minimal retry path.

## R12 Failure Summary
```json
{
  "r12_report_exists": true,
  "status": "MARKET_GATE_EQUIVALENCE_SMOKE_COMPLETE",
  "golden_row_extraction": {
    "sources": [
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R7_MARKET_STATE_SOURCE_EQUIVALENCE_TRACE.json",
        "exists": true,
        "sha256": "593161d81dd3a9951b7039505e6ea041a3653e2c44dcfa05c2b933796991a468",
        "candidate_lists": [],
        "best": null
      },
      {
        "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R8_MARKET_STATE_PARAMETER_AUDIT.json",
        "exists": true,
        "sha256": "aaf28cdf0b60a29480f4a8c3936dd8b2fe8d31b17a50e4578df1566903670063",
        "candidate_lists": [],
        "best": null
      }
    ],
    "selected_source": null,
    "error": "No usable golden row list found in R7/R8.",
    "row_count": 0,
    "sample_rows": []
  },
  "equivalence": {
    "row_count": 0,
    "mismatch_count": 0,
    "ok": false,
    "distribution": {
      "expected_gate_state": {},
      "actual_gate_state": {},
      "expected_market_state": {}
    },
    "sample_comparisons": [],
    "mismatches": []
  },
  "pytest_smoke": {
    "cmd": [
      "/Library/Developer/CommandLineTools/usr/bin/python3",
      "-m",
      "pytest",
      "-q",
      "/Users/dongfang/Downloads/sp500-tracker-v13/tests/e1r_engine/test_market_gate_equivalence.py"
    ],
    "returncode": 1,
    "stdout": "",
    "stderr": "/Library/Developer/CommandLineTools/usr/bin/python3: No module named pytest\n",
    "ok": false
  },
  "validations": {
    "market_gate_equivalence_smoke_complete": true,
    "r7_loaded": true,
    "r8_loaded": true,
    "r9d_loaded": true,
    "r10_loaded": true,
    "r11_loaded": true,
    "r11_authorized_r12": true,
    "golden_rows_found": false,
    "golden_rows_count": 0,
    "equivalence_run": true,
    "equivalence_passed": false,
    "mismatch_count_zero": true,
    "pytest_file_created": true,
    "pytest_smoke_run": true,
    "pytest_smoke_passed": false,
    "strategy_logic_changed": false,
    "standalone_module_only": true,
    "strategy_integration_changed": false,
    "legacy_backtest_called": false,
    "backtest_engine_run": false,
    "short_window_existing_engine_run": false,
    "full_5y_backtest_run": false,
    "forward_runner_run": false,
    "candidate_generation_extracted": false,
    "buy_add_reduce_exit_extracted": false,
    "official_result_generated": false,
    "dashboard_changed": false,
    "formula_not_patched_in_legacy": true,
    "strategy_files_unchanged": true
  },
  "decision": {
    "k2_r12_market_gate_equivalence_smoke_passed": false,
    "market_gate_equivalence_ready": false,
    "market_gate_strategy_integration_allowed_now": false,
    "formula_patch_allowed_now": false,
    "candidate_extraction_allowed_now": false,
    "implementation_may_resume": false,
    "requires_user_approval_before_next_stage": true,
    "next_stage_after_user_approval": "4C-2C-4E-ENGINE-K2-R12B-MARKET_GATE_EQUIVALENCE_GAP_RCA",
    "conclusion": "K2_R12_EQUIVALENCE_GAPS_REMAIN_DO_NOT_INTEGRATE",
    "recommended_next_action": "Stop and perform R12B RCA/gap closure before any wiring proposal."
  }
}
```

## R7 Structure Inspection
```json
{
  "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R7_MARKET_STATE_SOURCE_EQUIVALENCE_TRACE.json",
  "exists": true,
  "sha256": "593161d81dd3a9951b7039505e6ea041a3653e2c44dcfa05c2b933796991a468",
  "top_key_frequency": [
    [
      "line",
      67
    ],
    [
      "text",
      67
    ],
    [
      "kind",
      64
    ],
    [
      "market_state",
      35
    ],
    [
      "_shock_active",
      35
    ],
    [
      "entry_capacity",
      35
    ],
    [
      "market_entry_allowed",
      35
    ],
    [
      "market_risk_off",
      35
    ],
    [
      "market_shock",
      35
    ],
    [
      "source_quality",
      35
    ],
    [
      "captured__gate_state",
      35
    ],
    [
      "date",
      34
    ],
    [
      "expected_market_gate_state",
      34
    ],
    [
      "computed_gate_state_from_captured_inputs",
      34
    ],
    [
      "spx_close_t",
      34
    ],
    [
      "spx_ma50_t",
      34
    ],
    [
      "spx_day_return",
      34
    ],
    [
      "holdings_count",
      34
    ],
    [
      "pending_orders_count",
      34
    ],
    [
      "occurrence_count",
      7
    ],
    [
      "assignment_count",
      7
    ],
    [
      "rows",
      7
    ],
    [
      "ALLOW",
      3
    ],
    [
      "RISK_OFF",
      3
    ],
    [
      "SHOCK",
      3
    ],
    [
      "focused_rows",
      2
    ],
    [
      "strategy_logic_changed",
      2
    ],
    [
      "audit_only",
      2
    ],
    [
      "formula_not_patched",
      2
    ],
    [
      "short_window_existing_engine_run",
      2
    ],
    [
      "legacy_run_under_sys_trace",
      2
    ],
    [
      "full_5y_backtest_run",
      2
    ],
    [
      "forward_runner_run",
      2
    ],
    [
      "candidate_generation_extracted",
      2
    ],
    [
      "buy_add_reduce_exit_extracted",
      2
    ],
    [
      "official_result_generated",
      2
    ],
    [
      "dashboard_changed",
      2
    ],
    [
      "capture_line",
      2
    ],
    [
      "mismatch_count",
      2
    ],
    [
      "upstream_values_available",
      2
    ],
    [
      "generated_at",
      1
    ],
    [
      "elapsed_seconds",
      1
    ],
    [
      "stage",
      1
    ],
    [
      "status",
      1
    ],
    [
      "purpose",
      1
    ],
    [
      "policy",
      1
    ],
    [
      "source",
      1
    ],
    [
      "source_evidence",
      1
    ],
    [
      "trace_artifact_path",
      1
    ],
    [
      "trace_artifact_sha256",
      1
    ],
    [
      "equivalence_report_path",
      1
    ],
    [
      "equivalence_report_sha256",
      1
    ],
    [
      "equivalence_report",
      1
    ],
    [
      "validations",
      1
    ],
    [
      "decision",
      1
    ],
    [
      "frozen_strategy_files_changed",
      1
    ],
    [
      "backtest_path",
      1
    ],
    [
      "backtest_sha256",
      1
    ],
    [
      "golden_master_harness",
      1
    ],
    [
      "golden_master",
      1
    ],
    [
      "function_bounds",
      1
    ],
    [
      "capture_line_text",
      1
    ],
    [
      "_gate_state_formula_context",
      1
    ],
    [
      "market_state_chain_static_scan",
      1
    ],
    [
      "name",
      1
    ],
    [
      "start_line",
      1
    ],
    [
      "end_line",
      1
    ],
    [
      "line_count",
      1
    ],
    [
      "_gate_state",
      1
    ],
    [
      "ok",
      1
    ],
    [
      "checked_assertions",
      1
    ],
    [
      "row_count",
      1
    ],
    [
      "expected_row_count",
      1
    ],
    [
      "trace_row_count",
      1
    ],
    [
      "mismatches",
      1
    ],
    [
      "distribution",
      1
    ],
    [
      "expected",
      1
    ],
    [
      "computed_from_captured_inputs",
      1
    ],
    [
      "market_state_source_equivalence_trace_complete",
      1
    ],
    [
      "strategy_files_unchanged",
      1
    ]
  ],
  "term_hit_count": 40,
  "term_hits_sample": [
    {
      "path": "policy",
      "matched_keys": [
        "candidate_generation_extracted"
      ],
      "key_count": 12,
      "sample": {
        "strategy_logic_changed": false,
        "audit_only": true,
        "formula_not_patched": true,
        "short_window_existing_engine_run": true,
        "legacy_run_under_sys_trace": true,
        "full_5y_backtest_run": false,
        "forward_runner_run": false,
        "candidate_generation_extracted": false,
        "buy_add_reduce_exit_extracted": false,
        "official_result_generated": false,
        "dashboard_changed": false,
        "frozen_strategy_files_changed": false
      }
    },
    {
      "path": "source_evidence",
      "matched_keys": [
        "_gate_state_formula_context",
        "market_state_chain_static_scan"
      ],
      "key_count": 5,
      "sample": "{\"function_bounds\": {\"name\": \"run_stateful_simulation\", \"start_line\": 763, \"end_line\": 2486, \"line_count\": 1724}, \"capture_line\": 1525, \"capture_line_text\": \"            \\\"market_gate_state\\\": _gate_state,\", \"_gate_state_formula_context\": [{\"line\": 1510, \"text\": \"        _gate_state = (\"}, {\"line\": 1511, \"text\": \"            \\\"ALLOW\\\" if market_entry_allowed else\"}, {\"line\": 1512, \"text\": \"            \\\"SHOCK\\\" if market_shock else \\\"RISK_OFF\\\"\"}], \"market_state_chain_static_scan\": {\"market_state\": {\"occurrence_count\": 8, \"assignment_count\": 3, \"rows\": [{\"line\": 1395, \"kind\": \"assignment\", \"text\": \"            market_state     = \\\"FULL_ON\\\"\"}, {\"line\": 1469, \"kind\": \"reference\", \"text\": \"                market_state   = \\\"CASH_MODE\\\"\"}, {\"line\": 1477, \"kind\": \"reference\", \"text\": \"                market_state   = \\\"FULL_ON\\\"\"}, {\"line\": 1480, \"kind\": \"reference\", \"text\": \"                market_state   = \\\"CAUTIOUS_ON\\\"\"}, {\"line\": 1483, \"kind\": \"assignment\", \"text\": \"            market_risk_off  = (market_state == \\\"CASH_MODE\\\") and not _shock_active\"}, {\"line\": 1920, \"kind\": \"assignment\", \"text\": \"                            if market_state == \\\"FULL_ON\\\":\"}, {\"line\": 1943, \"kind...<truncated>"
    },
    {
      "path": "source_evidence.market_state_chain_static_scan",
      "matched_keys": [
        "market_state",
        "_shock_active",
        "entry_capacity",
        "market_entry_allowed",
        "market_risk_off",
        "market_shock",
        "_gate_state"
      ],
      "key_count": 7,
      "sample": "{\"market_state\": {\"occurrence_count\": 8, \"assignment_count\": 3, \"rows\": [{\"line\": 1395, \"kind\": \"assignment\", \"text\": \"            market_state     = \\\"FULL_ON\\\"\"}, {\"line\": 1469, \"kind\": \"reference\", \"text\": \"                market_state   = \\\"CASH_MODE\\\"\"}, {\"line\": 1477, \"kind\": \"reference\", \"text\": \"                market_state   = \\\"FULL_ON\\\"\"}, {\"line\": 1480, \"kind\": \"reference\", \"text\": \"                market_state   = \\\"CAUTIOUS_ON\\\"\"}, {\"line\": 1483, \"kind\": \"assignment\", \"text\": \"            market_risk_off  = (market_state == \\\"CASH_MODE\\\") and not _shock_active\"}, {\"line\": 1920, \"kind\": \"assignment\", \"text\": \"                            if market_state == \\\"FULL_ON\\\":\"}, {\"line\": 1943, \"kind\": \"reference\", \"text\": \"                                            \\\"market_state\\\": market_state,\"}, {\"line\": 1997, \"kind\": \"control\", \"text\": \"                if action == \\\"ADD\\\" and market_gate_enabled and market_state in (\\\"CAUTIOUS_ON\\\", \\\"CASH_MODE\\\"):\"}]}, \"_shock_active\": {\"occurrence_count\": 5, \"assignment_count\": 1, \"rows\": [{\"line\": 1448, \"kind\": \"assignment\", \"text\": \"            _shock_active = (\"}, {\"line\": 1464, \"kind\": \"reference\", \"text\": \"                or _sho...<truncated>"
    },
    {
      "path": "equivalence_report.distribution",
      "matched_keys": [
        "captured__gate_state"
      ],
      "key_count": 3,
      "sample": {
        "expected": {
          "ALLOW": 53,
          "RISK_OFF": 8,
          "SHOCK": 1
        },
        "captured__gate_state": {
          "ALLOW": 53,
          "RISK_OFF": 8,
          "SHOCK": 1
        },
        "computed_from_captured_inputs": {
          "ALLOW": 53,
          "RISK_OFF": 8,
          "SHOCK": 1
        }
      }
    },
    {
      "path": "equivalence_report.focused_rows[0]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-03",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4192.660156,
        "spx_ma50_t": 4008.45681644,
        "spx_day_return": 0.0027480906574836577,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[1]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-04",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4164.660156,
        "spx_ma50_t": 4014.2200195600003,
        "spx_day_return": -0.006678337608625392,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[2]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-05",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4167.589844,
        "spx_ma50_t": 4019.9444141,
        "spx_day_return": 0.0007034638818678605,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[3]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-06",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4201.620117,
        "spx_ma50_t": 4025.4682178000007,
        "spx_day_return": 0.008165456360585254,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[4]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-07",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "FULL_ON",
        "_shock_active": false,
        "entry_capacity": 3,
        "spx_close_t": 4232.600098,
        "spx_ma50_t": 4033.5334180000004,
        "spx_day_return": 0.007373341743736585,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[5]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-10",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4188.430176,
        "spx_ma50_t": 4041.07902348,
        "spx_day_return": -0.010435647350873364,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[6]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-11",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4152.100098,
        "spx_ma50_t": 4046.08462408,
        "spx_day_return": -0.008673912772421005,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[7]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-12",
        "expected_market_gate_state": "SHOCK",
        "captured__gate_state": "SHOCK",
        "computed_gate_state_from_captured_inputs": "SHOCK",
        "market_entry_allowed": false,
        "market_shock": true,
        "market_risk_off": false,
        "market_state": "CASH_MODE",
        "_shock_active": true,
        "entry_capacity": 0,
        "spx_close_t": 4063.040039,
        "spx_ma50_t": 4049.93962408,
        "spx_day_return": -0.02144940076056902,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[8]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-13",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4112.5,
        "spx_ma50_t": 4055.7952246600007,
        "spx_day_return": 0.01217314142249338,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[9]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-14",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4173.850098,
        "spx_ma50_t": 4063.902827200001,
        "spx_day_return": 0.014917956960486296,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[10]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-17",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4163.290039,
        "spx_ma50_t": 4070.329829160001,
        "spx_day_return": -0.0025300522903444855,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[11]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-18",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4127.830078,
        "spx_ma50_t": 4076.4594287600007,
        "spx_day_return": -0.00851729297450479,
        "holdings_count": 3,
        "pending_orders_count": 2,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[12]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-19",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4115.680176,
        "spx_ma50_t": 4081.264233460001,
        "spx_day_return": -0.0029434113736307027,
        "holdings_count": 3,
        "pending_orders_count": 2,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[13]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-20",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4159.120117,
        "spx_ma50_t": 4086.470434620001,
        "spx_day_return": 0.010554741656874688,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[14]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-21",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4155.859863,
        "spx_ma50_t": 4090.8008301200007,
        "spx_day_return": -0.0007838807027175632,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[15]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-24",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "FULL_ON",
        "_shock_active": false,
        "entry_capacity": 3,
        "spx_close_t": 4197.049805,
        "spx_ma50_t": 4095.87502446,
        "spx_day_return": 0.009911292333679919,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[16]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-06-18",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4166.450195,
        "spx_ma50_t": 4181.589023459999,
        "spx_day_return": -0.01312446878817667,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[0]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-03",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4192.660156,
        "spx_ma50_t": 4008.45681644,
        "spx_day_return": 0.0027480906574836577,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[1]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-04",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4164.660156,
        "spx_ma50_t": 4014.2200195600003,
        "spx_day_return": -0.006678337608625392,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[2]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-05",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4167.589844,
        "spx_ma50_t": 4019.9444141,
        "spx_day_return": 0.0007034638818678605,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[3]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-06",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4201.620117,
        "spx_ma50_t": 4025.4682178000007,
        "spx_day_return": 0.008165456360585254,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[4]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-07",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "FULL_ON",
        "_shock_active": false,
        "entry_capacity": 3,
        "spx_close_t": 4232.600098,
        "spx_ma50_t": 4033.5334180000004,
        "spx_day_return": 0.007373341743736585,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[5]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-10",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4188.430176,
        "spx_ma50_t": 4041.07902348,
        "spx_day_return": -0.010435647350873364,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[6]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-11",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4152.100098,
        "spx_ma50_t": 4046.08462408,
        "spx_day_return": -0.008673912772421005,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[7]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-12",
        "expected_market_gate_state": "SHOCK",
        "captured__gate_state": "SHOCK",
        "computed_gate_state_from_captured_inputs": "SHOCK",
        "market_entry_allowed": false,
        "market_shock": true,
        "market_risk_off": false,
        "market_state": "CASH_MODE",
        "_shock_active": true,
        "entry_capacity": 0,
        "spx_close_t": 4063.040039,
        "spx_ma50_t": 4049.93962408,
        "spx_day_return": -0.02144940076056902,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[8]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-13",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4112.5,
        "spx_ma50_t": 4055.7952246600007,
        "spx_day_return": 0.01217314142249338,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    }
  ],
  "row_like_dict_count": 36,
  "row_like_dicts_sample": [
    {
      "path": "source_evidence.market_state_chain_static_scan",
      "matched_keys": [
        "market_state",
        "_shock_active",
        "entry_capacity",
        "market_entry_allowed",
        "market_risk_off",
        "market_shock",
        "_gate_state"
      ],
      "sample": "{\"market_state\": {\"occurrence_count\": 8, \"assignment_count\": 3, \"rows\": [{\"line\": 1395, \"kind\": \"assignment\", \"text\": \"            market_state     = \\\"FULL_ON\\\"\"}, {\"line\": 1469, \"kind\": \"reference\", \"text\": \"                market_state   = \\\"CASH_MODE\\\"\"}, {\"line\": 1477, \"kind\": \"reference\", \"text\": \"                market_state   = \\\"FULL_ON\\\"\"}, {\"line\": 1480, \"kind\": \"reference\", \"text\": \"                market_state   = \\\"CAUTIOUS_ON\\\"\"}, {\"line\": 1483, \"kind\": \"assignment\", \"text\": \"            market_risk_off  = (market_state == \\\"CASH_MODE\\\") and not _shock_active\"}, {\"line\": 1920, \"kind\": \"assignment\", \"text\": \"                            if market_state == \\\"FULL_ON\\\":\"}, {\"line\": 1943, \"kind\": \"reference\", \"text\": \"                                            \\\"market_state\\\": market_state,\"}, {\"line\": 1997, \"kind\": \"control\", \"text\": \"                if action == \\\"ADD\\\" and market_gate_enabled and market_state in (\\\"CAUTIOUS_ON\\\", \\\"CASH_MODE\\\"):\"}]}, \"_shock_active\": {\"occurrence_count\": 5, \"assignment_count\": 1, \"rows\": [{\"line\": 1448, \"kind\": \"assignment\", \"text\": \"            _shock_active = (\"}, {\"line\": 1464, \"kind\": \"reference\", \"text\": \"                or _sho...<truncated>"
    },
    {
      "path": "equivalence_report.focused_rows[0]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-03",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4192.660156,
        "spx_ma50_t": 4008.45681644,
        "spx_day_return": 0.0027480906574836577,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[1]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-04",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4164.660156,
        "spx_ma50_t": 4014.2200195600003,
        "spx_day_return": -0.006678337608625392,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[2]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-05",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4167.589844,
        "spx_ma50_t": 4019.9444141,
        "spx_day_return": 0.0007034638818678605,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[3]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-06",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4201.620117,
        "spx_ma50_t": 4025.4682178000007,
        "spx_day_return": 0.008165456360585254,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[4]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-07",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "FULL_ON",
        "_shock_active": false,
        "entry_capacity": 3,
        "spx_close_t": 4232.600098,
        "spx_ma50_t": 4033.5334180000004,
        "spx_day_return": 0.007373341743736585,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[5]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-10",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4188.430176,
        "spx_ma50_t": 4041.07902348,
        "spx_day_return": -0.010435647350873364,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[6]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-11",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4152.100098,
        "spx_ma50_t": 4046.08462408,
        "spx_day_return": -0.008673912772421005,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[7]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-12",
        "expected_market_gate_state": "SHOCK",
        "captured__gate_state": "SHOCK",
        "computed_gate_state_from_captured_inputs": "SHOCK",
        "market_entry_allowed": false,
        "market_shock": true,
        "market_risk_off": false,
        "market_state": "CASH_MODE",
        "_shock_active": true,
        "entry_capacity": 0,
        "spx_close_t": 4063.040039,
        "spx_ma50_t": 4049.93962408,
        "spx_day_return": -0.02144940076056902,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[8]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-13",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4112.5,
        "spx_ma50_t": 4055.7952246600007,
        "spx_day_return": 0.01217314142249338,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[9]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-14",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4173.850098,
        "spx_ma50_t": 4063.902827200001,
        "spx_day_return": 0.014917956960486296,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[10]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-17",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4163.290039,
        "spx_ma50_t": 4070.329829160001,
        "spx_day_return": -0.0025300522903444855,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[11]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-18",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4127.830078,
        "spx_ma50_t": 4076.4594287600007,
        "spx_day_return": -0.00851729297450479,
        "holdings_count": 3,
        "pending_orders_count": 2,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[12]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-19",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4115.680176,
        "spx_ma50_t": 4081.264233460001,
        "spx_day_return": -0.0029434113736307027,
        "holdings_count": 3,
        "pending_orders_count": 2,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[13]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-20",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4159.120117,
        "spx_ma50_t": 4086.470434620001,
        "spx_day_return": 0.010554741656874688,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[14]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-21",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4155.859863,
        "spx_ma50_t": 4090.8008301200007,
        "spx_day_return": -0.0007838807027175632,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[15]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-24",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "FULL_ON",
        "_shock_active": false,
        "entry_capacity": 3,
        "spx_close_t": 4197.049805,
        "spx_ma50_t": 4095.87502446,
        "spx_day_return": 0.009911292333679919,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "equivalence_report.focused_rows[16]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-06-18",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4166.450195,
        "spx_ma50_t": 4181.589023459999,
        "spx_day_return": -0.01312446878817667,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[0]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-03",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4192.660156,
        "spx_ma50_t": 4008.45681644,
        "spx_day_return": 0.0027480906574836577,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[1]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-04",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4164.660156,
        "spx_ma50_t": 4014.2200195600003,
        "spx_day_return": -0.006678337608625392,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[2]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-05",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4167.589844,
        "spx_ma50_t": 4019.9444141,
        "spx_day_return": 0.0007034638818678605,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[3]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-06",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4201.620117,
        "spx_ma50_t": 4025.4682178000007,
        "spx_day_return": 0.008165456360585254,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[4]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-07",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "FULL_ON",
        "_shock_active": false,
        "entry_capacity": 3,
        "spx_close_t": 4232.600098,
        "spx_ma50_t": 4033.5334180000004,
        "spx_day_return": 0.007373341743736585,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[5]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-10",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4188.430176,
        "spx_ma50_t": 4041.07902348,
        "spx_day_return": -0.010435647350873364,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[6]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-11",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4152.100098,
        "spx_ma50_t": 4046.08462408,
        "spx_day_return": -0.008673912772421005,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[7]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-12",
        "expected_market_gate_state": "SHOCK",
        "captured__gate_state": "SHOCK",
        "computed_gate_state_from_captured_inputs": "SHOCK",
        "market_entry_allowed": false,
        "market_shock": true,
        "market_risk_off": false,
        "market_state": "CASH_MODE",
        "_shock_active": true,
        "entry_capacity": 0,
        "spx_close_t": 4063.040039,
        "spx_ma50_t": 4049.93962408,
        "spx_day_return": -0.02144940076056902,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[8]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-13",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4112.5,
        "spx_ma50_t": 4055.7952246600007,
        "spx_day_return": 0.01217314142249338,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[9]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-14",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4173.850098,
        "spx_ma50_t": 4063.902827200001,
        "spx_day_return": 0.014917956960486296,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[10]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-17",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4163.290039,
        "spx_ma50_t": 4070.329829160001,
        "spx_day_return": -0.0025300522903444855,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows[11]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-18",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4127.830078,
        "spx_ma50_t": 4076.4594287600007,
        "spx_day_return": -0.00851729297450479,
        "holdings_count": 3,
        "pending_orders_count": 2,
        "source_quality": "legacy_sys_trace_locals"
      }
    }
  ],
  "list_candidate_count": 2,
  "list_candidates_sample": [
    {
      "path": "equivalence_report.focused_rows",
      "length": 17,
      "dict_sample_count": 17,
      "sample_keys": [
        "_shock_active",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "date",
        "entry_capacity",
        "expected_market_gate_state",
        "holdings_count",
        "market_entry_allowed",
        "market_risk_off",
        "market_shock",
        "market_state",
        "pending_orders_count",
        "source_quality",
        "spx_close_t",
        "spx_day_return",
        "spx_ma50_t"
      ],
      "matched_keys": [
        "_shock_active",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "date",
        "entry_capacity",
        "expected_market_gate_state",
        "market_entry_allowed",
        "market_risk_off",
        "market_shock",
        "market_state",
        "spx_close_t",
        "spx_day_return",
        "spx_ma50_t"
      ],
      "sample_first": {
        "date": "2021-05-03",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4192.660156,
        "spx_ma50_t": 4008.45681644,
        "spx_day_return": 0.0027480906574836577,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "focused_rows",
      "length": 17,
      "dict_sample_count": 17,
      "sample_keys": [
        "_shock_active",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "date",
        "entry_capacity",
        "expected_market_gate_state",
        "holdings_count",
        "market_entry_allowed",
        "market_risk_off",
        "market_shock",
        "market_state",
        "pending_orders_count",
        "source_quality",
        "spx_close_t",
        "spx_day_return",
        "spx_ma50_t"
      ],
      "matched_keys": [
        "_shock_active",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "date",
        "entry_capacity",
        "expected_market_gate_state",
        "market_entry_allowed",
        "market_risk_off",
        "market_shock",
        "market_state",
        "spx_close_t",
        "spx_day_return",
        "spx_ma50_t"
      ],
      "sample_first": {
        "date": "2021-05-03",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4192.660156,
        "spx_ma50_t": 4008.45681644,
        "spx_day_return": 0.0027480906574836577,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    }
  ]
}
```

## R8 Structure Inspection
```json
{
  "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R8_MARKET_STATE_PARAMETER_AUDIT.json",
  "exists": true,
  "sha256": "aaf28cdf0b60a29480f4a8c3936dd8b2fe8d31b17a50e4578df1566903670063",
  "top_key_frequency": [
    [
      "text",
      557
    ],
    [
      "line",
      555
    ],
    [
      "kind",
      95
    ],
    [
      "indent",
      95
    ],
    [
      "rows",
      61
    ],
    [
      "key",
      46
    ],
    [
      "default_expr",
      46
    ],
    [
      "context",
      46
    ],
    [
      "start",
      46
    ],
    [
      "end",
      46
    ],
    [
      "from",
      40
    ],
    [
      "to",
      40
    ],
    [
      "date",
      29
    ],
    [
      "market_state",
      28
    ],
    [
      "entry_capacity",
      28
    ],
    [
      "market_risk_off",
      24
    ],
    [
      "market_entry_allowed",
      22
    ],
    [
      "market_shock",
      21
    ],
    [
      "_shock_active",
      20
    ],
    [
      "expected_market_gate_state",
      17
    ],
    [
      "captured__gate_state",
      17
    ],
    [
      "computed_gate_state_from_captured_inputs",
      17
    ],
    [
      "spx_close_t",
      17
    ],
    [
      "spx_ma50_t",
      17
    ],
    [
      "spx_day_return",
      17
    ],
    [
      "holdings_count",
      17
    ],
    [
      "pending_orders_count",
      17
    ],
    [
      "source_quality",
      17
    ],
    [
      "occurrence_count",
      15
    ],
    [
      "assignment_count",
      15
    ],
    [
      "control_count",
      15
    ],
    [
      "changed",
      12
    ],
    [
      "prev_date",
      12
    ],
    [
      "_gate_state",
      7
    ],
    [
      "FULL_ON",
      3
    ],
    [
      "CAUTIOUS_ON",
      3
    ],
    [
      "CASH_MODE",
      3
    ],
    [
      "status",
      2
    ],
    [
      "unresolved",
      2
    ],
    [
      "strategy_logic_changed",
      2
    ],
    [
      "audit_only",
      2
    ],
    [
      "formula_not_patched",
      2
    ],
    [
      "backtest_engine_run",
      2
    ],
    [
      "short_window_existing_engine_run",
      2
    ],
    [
      "full_5y_backtest_run",
      2
    ],
    [
      "forward_runner_run",
      2
    ],
    [
      "candidate_generation_extracted",
      2
    ],
    [
      "buy_add_reduce_exit_extracted",
      2
    ],
    [
      "official_result_generated",
      2
    ],
    [
      "dashboard_changed",
      2
    ],
    [
      "market_gate_enabled",
      2
    ],
    [
      "risk_off_below_spx_ma50",
      2
    ],
    [
      "market_shock_gate_enabled",
      2
    ],
    [
      "market_shock_daily_return",
      2
    ],
    [
      "type",
      2
    ],
    [
      "generated_at",
      1
    ],
    [
      "elapsed_seconds",
      1
    ],
    [
      "stage",
      1
    ],
    [
      "purpose",
      1
    ],
    [
      "policy",
      1
    ],
    [
      "source",
      1
    ],
    [
      "source_scan",
      1
    ],
    [
      "assumption_gets",
      1
    ],
    [
      "parameter_audit",
      1
    ],
    [
      "validations",
      1
    ],
    [
      "decision",
      1
    ],
    [
      "frozen_strategy_files_changed",
      1
    ],
    [
      "backtest_path",
      1
    ],
    [
      "backtest_sha256",
      1
    ],
    [
      "function_bounds",
      1
    ],
    [
      "k2_r7_report",
      1
    ],
    [
      "r7_trace",
      1
    ],
    [
      "r7_equivalence",
      1
    ],
    [
      "golden_master",
      1
    ],
    [
      "name",
      1
    ],
    [
      "start_line",
      1
    ],
    [
      "end_line",
      1
    ],
    [
      "line_count",
      1
    ],
    [
      "market_gate_days",
      1
    ],
    [
      "market_gate_parameters",
      1
    ]
  ],
  "term_hit_count": 50,
  "term_hits_sample": [
    {
      "path": "policy",
      "matched_keys": [
        "candidate_generation_extracted"
      ],
      "key_count": 12,
      "sample": {
        "strategy_logic_changed": false,
        "audit_only": true,
        "formula_not_patched": true,
        "backtest_engine_run": false,
        "short_window_existing_engine_run": false,
        "full_5y_backtest_run": false,
        "forward_runner_run": false,
        "candidate_generation_extracted": false,
        "buy_add_reduce_exit_extracted": false,
        "official_result_generated": false,
        "dashboard_changed": false,
        "frozen_strategy_files_changed": false
      }
    },
    {
      "path": "source_scan",
      "matched_keys": [
        "risk_off_below_spx_ma50",
        "market_shock_gate_enabled",
        "market_shock_daily_return",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "market_entry_allowed",
        "market_risk_off",
        "market_shock",
        "_gate_state"
      ],
      "key_count": 15,
      "sample": "{\"market_gate_enabled\": {\"occurrence_count\": 9, \"assignment_count\": 1, \"control_count\": 4, \"rows\": [{\"line\": 847, \"kind\": \"assignment\", \"indent\": 4, \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\"}, {\"line\": 912, \"kind\": \"reference\", \"indent\": 8, \"text\": \"        \\\"D1_NO_MARKET_GATE\\\" if not market_gate_enabled else\"}, {\"line\": 928, \"kind\": \"log\", \"indent\": 4, \"text\": \"    logger.info(f\\\"  Market Gate: enabled={market_gate_enabled} \\\"\"}, {\"line\": 938, \"kind\": \"reference\", \"indent\": 16, \"text\": \"                f\\\"relstop={relative_stop_enabled} gate={market_gate_enabled} ──\\\")\"}, {\"line\": 1393, \"kind\": \"control\", \"indent\": 8, \"text\": \"        if not market_gate_enabled:\"}, {\"line\": 1820, \"kind\": \"control\", \"indent\": 20, \"text\": \"                    if market_gate_enabled and len(holdings) >= entry_capacity:\"}, {\"line\": 1872, \"kind\": \"control\", \"indent\": 20, \"text\": \"                    if market_gate_enabled and len(holdings) >= entry_capacity:\"}, {\"line\": 1997, \"kind\": \"control\", \"indent\": 16, \"text\": \"                if action == \\\"ADD\\\" and market_gate_enabled and market_state in (\\\"CAUTIOUS_ON\\\", \\\"CASH_MODE\\\"):\"}, {\"line\": 2406, \"kind\": \"referenc...<truncated>"
    },
    {
      "path": "parameter_audit",
      "matched_keys": [
        "observed_market_state_distribution",
        "observed_entry_capacity_distribution",
        "observed_gate_state_distribution",
        "entry_capacity_mapping_by_market_state"
      ],
      "key_count": 10,
      "sample": "{\"market_gate_parameters\": {\"market_gate_variant\": \"D3_RISK_OFF_PLUS_SHOCK_GATE\", \"market_gate_enabled\": true, \"risk_off_below_spx_ma50\": true, \"market_shock_gate_enabled\": true, \"market_shock_daily_return\": -0.02, \"evidence\": [{\"type\": \"runtime_log_from_R7\", \"text\": \"Market Gate Variant: D3_RISK_OFF_PLUS_SHOCK_GATE\"}, {\"type\": \"runtime_log_from_R7\", \"text\": \"Market Gate: enabled=True | RiskOff=SPX<MA50:True | Shock<=-2.0%:True\"}]}, \"observed_market_state_distribution\": {\"FULL_ON\": 46, \"CAUTIOUS_ON\": 7, \"CASH_MODE\": 9}, \"observed_shock_distribution\": {\"False\": 61, \"True\": 1}, \"observed_entry_capacity_distribution\": {\"3\": 46, \"2\": 7, \"0\": 9}, \"observed_gate_state_distribution\": {\"None\": 62}, \"entry_capacity_mapping_by_market_state\": {\"mapping\": {\"FULL_ON\": [3], \"CAUTIOUS_ON\": [2], \"CASH_MODE\": [0]}, \"conflicts\": [], \"stable_mapping\": true}, \"focused_rows\": [{\"date\": \"2021-05-03\", \"expected_market_gate_state\": \"ALLOW\", \"captured__gate_state\": \"ALLOW\", \"computed_gate_state_from_captured_inputs\": \"ALLOW\", \"market_entry_allowed\": true, \"market_shock\": false, \"market_risk_off\": false, \"market_state\": \"CAUTIOUS_ON\", \"_shock_active\": false, \"entry_capacity\": 2, \"spx_close_t\": 4192.660156, ...<truncated>"
    },
    {
      "path": "parameter_audit.market_gate_parameters",
      "matched_keys": [
        "risk_off_below_spx_ma50",
        "market_shock_gate_enabled",
        "market_shock_daily_return"
      ],
      "key_count": 6,
      "sample": {
        "market_gate_variant": "D3_RISK_OFF_PLUS_SHOCK_GATE",
        "market_gate_enabled": true,
        "risk_off_below_spx_ma50": true,
        "market_shock_gate_enabled": true,
        "market_shock_daily_return": -0.02,
        "evidence": [
          {
            "type": "runtime_log_from_R7",
            "text": "Market Gate Variant: D3_RISK_OFF_PLUS_SHOCK_GATE"
          },
          {
            "type": "runtime_log_from_R7",
            "text": "Market Gate: enabled=True | RiskOff=SPX<MA50:True | Shock<=-2.0%:True"
          }
        ]
      }
    },
    {
      "path": "parameter_audit.focused_rows[0]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-03",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4192.660156,
        "spx_ma50_t": 4008.45681644,
        "spx_day_return": 0.0027480906574836577,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[1]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-04",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4164.660156,
        "spx_ma50_t": 4014.2200195600003,
        "spx_day_return": -0.006678337608625392,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[2]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-05",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4167.589844,
        "spx_ma50_t": 4019.9444141,
        "spx_day_return": 0.0007034638818678605,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[3]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-06",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4201.620117,
        "spx_ma50_t": 4025.4682178000007,
        "spx_day_return": 0.008165456360585254,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[4]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-07",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "FULL_ON",
        "_shock_active": false,
        "entry_capacity": 3,
        "spx_close_t": 4232.600098,
        "spx_ma50_t": 4033.5334180000004,
        "spx_day_return": 0.007373341743736585,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[5]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-10",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4188.430176,
        "spx_ma50_t": 4041.07902348,
        "spx_day_return": -0.010435647350873364,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[6]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-11",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4152.100098,
        "spx_ma50_t": 4046.08462408,
        "spx_day_return": -0.008673912772421005,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[7]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-12",
        "expected_market_gate_state": "SHOCK",
        "captured__gate_state": "SHOCK",
        "computed_gate_state_from_captured_inputs": "SHOCK",
        "market_entry_allowed": false,
        "market_shock": true,
        "market_risk_off": false,
        "market_state": "CASH_MODE",
        "_shock_active": true,
        "entry_capacity": 0,
        "spx_close_t": 4063.040039,
        "spx_ma50_t": 4049.93962408,
        "spx_day_return": -0.02144940076056902,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[8]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-13",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4112.5,
        "spx_ma50_t": 4055.7952246600007,
        "spx_day_return": 0.01217314142249338,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[9]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-14",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4173.850098,
        "spx_ma50_t": 4063.902827200001,
        "spx_day_return": 0.014917956960486296,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[10]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-17",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4163.290039,
        "spx_ma50_t": 4070.329829160001,
        "spx_day_return": -0.0025300522903444855,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[11]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-18",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4127.830078,
        "spx_ma50_t": 4076.4594287600007,
        "spx_day_return": -0.00851729297450479,
        "holdings_count": 3,
        "pending_orders_count": 2,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[12]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-19",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4115.680176,
        "spx_ma50_t": 4081.264233460001,
        "spx_day_return": -0.0029434113736307027,
        "holdings_count": 3,
        "pending_orders_count": 2,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[13]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-20",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4159.120117,
        "spx_ma50_t": 4086.470434620001,
        "spx_day_return": 0.010554741656874688,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[14]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-21",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4155.859863,
        "spx_ma50_t": 4090.8008301200007,
        "spx_day_return": -0.0007838807027175632,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[15]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-05-24",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "FULL_ON",
        "_shock_active": false,
        "entry_capacity": 3,
        "spx_close_t": 4197.049805,
        "spx_ma50_t": 4095.87502446,
        "spx_day_return": 0.009911292333679919,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[16]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "key_count": 16,
      "sample": {
        "date": "2021-06-18",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4166.450195,
        "spx_ma50_t": 4181.589023459999,
        "spx_day_return": -0.01312446878817667,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.transitions[0]",
      "matched_keys": [
        "date",
        "prev_date"
      ],
      "key_count": 3,
      "sample": {
        "date": "2021-05-03",
        "changed": {
          "market_state": {
            "from": "FULL_ON",
            "to": "CAUTIOUS_ON"
          },
          "entry_capacity": {
            "from": 3,
            "to": 2
          }
        },
        "prev_date": "2021-04-30"
      }
    },
    {
      "path": "parameter_audit.transitions[0].changed",
      "matched_keys": [
        "market_state",
        "entry_capacity"
      ],
      "key_count": 2,
      "sample": {
        "market_state": {
          "from": "FULL_ON",
          "to": "CAUTIOUS_ON"
        },
        "entry_capacity": {
          "from": 3,
          "to": 2
        }
      }
    },
    {
      "path": "parameter_audit.transitions[1]",
      "matched_keys": [
        "date",
        "prev_date"
      ],
      "key_count": 3,
      "sample": {
        "date": "2021-05-07",
        "changed": {
          "market_state": {
            "from": "CAUTIOUS_ON",
            "to": "FULL_ON"
          },
          "entry_capacity": {
            "from": 2,
            "to": 3
          }
        },
        "prev_date": "2021-05-06"
      }
    },
    {
      "path": "parameter_audit.transitions[1].changed",
      "matched_keys": [
        "market_state",
        "entry_capacity"
      ],
      "key_count": 2,
      "sample": {
        "market_state": {
          "from": "CAUTIOUS_ON",
          "to": "FULL_ON"
        },
        "entry_capacity": {
          "from": 2,
          "to": 3
        }
      }
    },
    {
      "path": "parameter_audit.transitions[2]",
      "matched_keys": [
        "date",
        "prev_date"
      ],
      "key_count": 3,
      "sample": {
        "date": "2021-05-10",
        "changed": {
          "market_state": {
            "from": "FULL_ON",
            "to": "CASH_MODE"
          },
          "entry_capacity": {
            "from": 3,
            "to": 0
          },
          "market_entry_allowed": {
            "from": true,
            "to": false
          },
          "market_risk_off": {
            "from": false,
            "to": true
          },
          "_gate_state": {
            "from": "ALLOW",
            "to": "RISK_OFF"
          }
        },
        "prev_date": "2021-05-07"
      }
    },
    {
      "path": "parameter_audit.transitions[2].changed",
      "matched_keys": [
        "market_state",
        "entry_capacity",
        "market_entry_allowed",
        "market_risk_off",
        "_gate_state"
      ],
      "key_count": 5,
      "sample": {
        "market_state": {
          "from": "FULL_ON",
          "to": "CASH_MODE"
        },
        "entry_capacity": {
          "from": 3,
          "to": 0
        },
        "market_entry_allowed": {
          "from": true,
          "to": false
        },
        "market_risk_off": {
          "from": false,
          "to": true
        },
        "_gate_state": {
          "from": "ALLOW",
          "to": "RISK_OFF"
        }
      }
    },
    {
      "path": "parameter_audit.transitions[3]",
      "matched_keys": [
        "date",
        "prev_date"
      ],
      "key_count": 3,
      "sample": {
        "date": "2021-05-12",
        "changed": {
          "_shock_active": {
            "from": false,
            "to": true
          },
          "market_shock": {
            "from": false,
            "to": true
          },
          "market_risk_off": {
            "from": true,
            "to": false
          },
          "_gate_state": {
            "from": "RISK_OFF",
            "to": "SHOCK"
          }
        },
        "prev_date": "2021-05-11"
      }
    },
    {
      "path": "parameter_audit.transitions[3].changed",
      "matched_keys": [
        "_shock_active",
        "market_shock",
        "market_risk_off",
        "_gate_state"
      ],
      "key_count": 4,
      "sample": {
        "_shock_active": {
          "from": false,
          "to": true
        },
        "market_shock": {
          "from": false,
          "to": true
        },
        "market_risk_off": {
          "from": true,
          "to": false
        },
        "_gate_state": {
          "from": "RISK_OFF",
          "to": "SHOCK"
        }
      }
    },
    {
      "path": "parameter_audit.transitions[4]",
      "matched_keys": [
        "date",
        "prev_date"
      ],
      "key_count": 3,
      "sample": {
        "date": "2021-05-13",
        "changed": {
          "_shock_active": {
            "from": true,
            "to": false
          },
          "market_shock": {
            "from": true,
            "to": false
          },
          "market_risk_off": {
            "from": false,
            "to": true
          },
          "_gate_state": {
            "from": "SHOCK",
            "to": "RISK_OFF"
          }
        },
        "prev_date": "2021-05-12"
      }
    }
  ],
  "row_like_dict_count": 28,
  "row_like_dicts_sample": [
    {
      "path": "source_scan",
      "matched_keys": [
        "risk_off_below_spx_ma50",
        "market_shock_gate_enabled",
        "market_shock_daily_return",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "market_entry_allowed",
        "market_risk_off",
        "market_shock",
        "_gate_state"
      ],
      "sample": "{\"market_gate_enabled\": {\"occurrence_count\": 9, \"assignment_count\": 1, \"control_count\": 4, \"rows\": [{\"line\": 847, \"kind\": \"assignment\", \"indent\": 4, \"text\": \"    market_gate_enabled = bool(a.get(\\\"market_gate_enabled\\\", True))\"}, {\"line\": 912, \"kind\": \"reference\", \"indent\": 8, \"text\": \"        \\\"D1_NO_MARKET_GATE\\\" if not market_gate_enabled else\"}, {\"line\": 928, \"kind\": \"log\", \"indent\": 4, \"text\": \"    logger.info(f\\\"  Market Gate: enabled={market_gate_enabled} \\\"\"}, {\"line\": 938, \"kind\": \"reference\", \"indent\": 16, \"text\": \"                f\\\"relstop={relative_stop_enabled} gate={market_gate_enabled} ──\\\")\"}, {\"line\": 1393, \"kind\": \"control\", \"indent\": 8, \"text\": \"        if not market_gate_enabled:\"}, {\"line\": 1820, \"kind\": \"control\", \"indent\": 20, \"text\": \"                    if market_gate_enabled and len(holdings) >= entry_capacity:\"}, {\"line\": 1872, \"kind\": \"control\", \"indent\": 20, \"text\": \"                    if market_gate_enabled and len(holdings) >= entry_capacity:\"}, {\"line\": 1997, \"kind\": \"control\", \"indent\": 16, \"text\": \"                if action == \\\"ADD\\\" and market_gate_enabled and market_state in (\\\"CAUTIOUS_ON\\\", \\\"CASH_MODE\\\"):\"}, {\"line\": 2406, \"kind\": \"referenc...<truncated>"
    },
    {
      "path": "parameter_audit",
      "matched_keys": [
        "observed_market_state_distribution",
        "observed_entry_capacity_distribution",
        "observed_gate_state_distribution",
        "entry_capacity_mapping_by_market_state"
      ],
      "sample": "{\"market_gate_parameters\": {\"market_gate_variant\": \"D3_RISK_OFF_PLUS_SHOCK_GATE\", \"market_gate_enabled\": true, \"risk_off_below_spx_ma50\": true, \"market_shock_gate_enabled\": true, \"market_shock_daily_return\": -0.02, \"evidence\": [{\"type\": \"runtime_log_from_R7\", \"text\": \"Market Gate Variant: D3_RISK_OFF_PLUS_SHOCK_GATE\"}, {\"type\": \"runtime_log_from_R7\", \"text\": \"Market Gate: enabled=True | RiskOff=SPX<MA50:True | Shock<=-2.0%:True\"}]}, \"observed_market_state_distribution\": {\"FULL_ON\": 46, \"CAUTIOUS_ON\": 7, \"CASH_MODE\": 9}, \"observed_shock_distribution\": {\"False\": 61, \"True\": 1}, \"observed_entry_capacity_distribution\": {\"3\": 46, \"2\": 7, \"0\": 9}, \"observed_gate_state_distribution\": {\"None\": 62}, \"entry_capacity_mapping_by_market_state\": {\"mapping\": {\"FULL_ON\": [3], \"CAUTIOUS_ON\": [2], \"CASH_MODE\": [0]}, \"conflicts\": [], \"stable_mapping\": true}, \"focused_rows\": [{\"date\": \"2021-05-03\", \"expected_market_gate_state\": \"ALLOW\", \"captured__gate_state\": \"ALLOW\", \"computed_gate_state_from_captured_inputs\": \"ALLOW\", \"market_entry_allowed\": true, \"market_shock\": false, \"market_risk_off\": false, \"market_state\": \"CAUTIOUS_ON\", \"_shock_active\": false, \"entry_capacity\": 2, \"spx_close_t\": 4192.660156, ...<truncated>"
    },
    {
      "path": "parameter_audit.market_gate_parameters",
      "matched_keys": [
        "risk_off_below_spx_ma50",
        "market_shock_gate_enabled",
        "market_shock_daily_return"
      ],
      "sample": {
        "market_gate_variant": "D3_RISK_OFF_PLUS_SHOCK_GATE",
        "market_gate_enabled": true,
        "risk_off_below_spx_ma50": true,
        "market_shock_gate_enabled": true,
        "market_shock_daily_return": -0.02,
        "evidence": [
          {
            "type": "runtime_log_from_R7",
            "text": "Market Gate Variant: D3_RISK_OFF_PLUS_SHOCK_GATE"
          },
          {
            "type": "runtime_log_from_R7",
            "text": "Market Gate: enabled=True | RiskOff=SPX<MA50:True | Shock<=-2.0%:True"
          }
        ]
      }
    },
    {
      "path": "parameter_audit.focused_rows[0]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-03",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4192.660156,
        "spx_ma50_t": 4008.45681644,
        "spx_day_return": 0.0027480906574836577,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[1]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-04",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4164.660156,
        "spx_ma50_t": 4014.2200195600003,
        "spx_day_return": -0.006678337608625392,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[2]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-05",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4167.589844,
        "spx_ma50_t": 4019.9444141,
        "spx_day_return": 0.0007034638818678605,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[3]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-06",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4201.620117,
        "spx_ma50_t": 4025.4682178000007,
        "spx_day_return": 0.008165456360585254,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[4]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-07",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "FULL_ON",
        "_shock_active": false,
        "entry_capacity": 3,
        "spx_close_t": 4232.600098,
        "spx_ma50_t": 4033.5334180000004,
        "spx_day_return": 0.007373341743736585,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[5]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-10",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4188.430176,
        "spx_ma50_t": 4041.07902348,
        "spx_day_return": -0.010435647350873364,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[6]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-11",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4152.100098,
        "spx_ma50_t": 4046.08462408,
        "spx_day_return": -0.008673912772421005,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[7]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-12",
        "expected_market_gate_state": "SHOCK",
        "captured__gate_state": "SHOCK",
        "computed_gate_state_from_captured_inputs": "SHOCK",
        "market_entry_allowed": false,
        "market_shock": true,
        "market_risk_off": false,
        "market_state": "CASH_MODE",
        "_shock_active": true,
        "entry_capacity": 0,
        "spx_close_t": 4063.040039,
        "spx_ma50_t": 4049.93962408,
        "spx_day_return": -0.02144940076056902,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[8]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-13",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4112.5,
        "spx_ma50_t": 4055.7952246600007,
        "spx_day_return": 0.01217314142249338,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[9]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-14",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4173.850098,
        "spx_ma50_t": 4063.902827200001,
        "spx_day_return": 0.014917956960486296,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[10]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-17",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4163.290039,
        "spx_ma50_t": 4070.329829160001,
        "spx_day_return": -0.0025300522903444855,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[11]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-18",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4127.830078,
        "spx_ma50_t": 4076.4594287600007,
        "spx_day_return": -0.00851729297450479,
        "holdings_count": 3,
        "pending_orders_count": 2,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[12]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-19",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4115.680176,
        "spx_ma50_t": 4081.264233460001,
        "spx_day_return": -0.0029434113736307027,
        "holdings_count": 3,
        "pending_orders_count": 2,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[13]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-20",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4159.120117,
        "spx_ma50_t": 4086.470434620001,
        "spx_day_return": 0.010554741656874688,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[14]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-21",
        "expected_market_gate_state": "RISK_OFF",
        "captured__gate_state": "RISK_OFF",
        "computed_gate_state_from_captured_inputs": "RISK_OFF",
        "market_entry_allowed": false,
        "market_shock": false,
        "market_risk_off": true,
        "market_state": "CASH_MODE",
        "_shock_active": false,
        "entry_capacity": 0,
        "spx_close_t": 4155.859863,
        "spx_ma50_t": 4090.8008301200007,
        "spx_day_return": -0.0007838807027175632,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[15]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-05-24",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "FULL_ON",
        "_shock_active": false,
        "entry_capacity": 3,
        "spx_close_t": 4197.049805,
        "spx_ma50_t": 4095.87502446,
        "spx_day_return": 0.009911292333679919,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.focused_rows[16]",
      "matched_keys": [
        "date",
        "expected_market_gate_state",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "market_entry_allowed",
        "market_shock",
        "market_risk_off",
        "market_state",
        "_shock_active",
        "entry_capacity",
        "spx_close_t",
        "spx_ma50_t",
        "spx_day_return"
      ],
      "sample": {
        "date": "2021-06-18",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4166.450195,
        "spx_ma50_t": 4181.589023459999,
        "spx_day_return": -0.01312446878817667,
        "holdings_count": 3,
        "pending_orders_count": 3,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.transitions[2].changed",
      "matched_keys": [
        "market_state",
        "entry_capacity",
        "market_entry_allowed",
        "market_risk_off",
        "_gate_state"
      ],
      "sample": {
        "market_state": {
          "from": "FULL_ON",
          "to": "CASH_MODE"
        },
        "entry_capacity": {
          "from": 3,
          "to": 0
        },
        "market_entry_allowed": {
          "from": true,
          "to": false
        },
        "market_risk_off": {
          "from": false,
          "to": true
        },
        "_gate_state": {
          "from": "ALLOW",
          "to": "RISK_OFF"
        }
      }
    },
    {
      "path": "parameter_audit.transitions[3].changed",
      "matched_keys": [
        "_shock_active",
        "market_shock",
        "market_risk_off",
        "_gate_state"
      ],
      "sample": {
        "_shock_active": {
          "from": false,
          "to": true
        },
        "market_shock": {
          "from": false,
          "to": true
        },
        "market_risk_off": {
          "from": true,
          "to": false
        },
        "_gate_state": {
          "from": "RISK_OFF",
          "to": "SHOCK"
        }
      }
    },
    {
      "path": "parameter_audit.transitions[4].changed",
      "matched_keys": [
        "_shock_active",
        "market_shock",
        "market_risk_off",
        "_gate_state"
      ],
      "sample": {
        "_shock_active": {
          "from": true,
          "to": false
        },
        "market_shock": {
          "from": true,
          "to": false
        },
        "market_risk_off": {
          "from": false,
          "to": true
        },
        "_gate_state": {
          "from": "SHOCK",
          "to": "RISK_OFF"
        }
      }
    },
    {
      "path": "parameter_audit.transitions[5].changed",
      "matched_keys": [
        "market_state",
        "entry_capacity",
        "market_entry_allowed",
        "market_risk_off",
        "_gate_state"
      ],
      "sample": {
        "market_state": {
          "from": "CASH_MODE",
          "to": "CAUTIOUS_ON"
        },
        "entry_capacity": {
          "from": 0,
          "to": 2
        },
        "market_entry_allowed": {
          "from": false,
          "to": true
        },
        "market_risk_off": {
          "from": true,
          "to": false
        },
        "_gate_state": {
          "from": "RISK_OFF",
          "to": "ALLOW"
        }
      }
    },
    {
      "path": "parameter_audit.transitions[6].changed",
      "matched_keys": [
        "market_state",
        "entry_capacity",
        "market_entry_allowed",
        "market_risk_off",
        "_gate_state"
      ],
      "sample": {
        "market_state": {
          "from": "CAUTIOUS_ON",
          "to": "CASH_MODE"
        },
        "entry_capacity": {
          "from": 2,
          "to": 0
        },
        "market_entry_allowed": {
          "from": true,
          "to": false
        },
        "market_risk_off": {
          "from": false,
          "to": true
        },
        "_gate_state": {
          "from": "ALLOW",
          "to": "RISK_OFF"
        }
      }
    },
    {
      "path": "parameter_audit.transitions[7].changed",
      "matched_keys": [
        "market_state",
        "entry_capacity",
        "market_entry_allowed",
        "market_risk_off",
        "_gate_state"
      ],
      "sample": {
        "market_state": {
          "from": "CASH_MODE",
          "to": "FULL_ON"
        },
        "entry_capacity": {
          "from": 0,
          "to": 3
        },
        "market_entry_allowed": {
          "from": false,
          "to": true
        },
        "market_risk_off": {
          "from": true,
          "to": false
        },
        "_gate_state": {
          "from": "RISK_OFF",
          "to": "ALLOW"
        }
      }
    },
    {
      "path": "validations",
      "matched_keys": [
        "market_state_parameter_audit_complete",
        "candidate_generation_extracted",
        "market_state_distribution_documented",
        "entry_capacity_mapping_documented",
        "entry_capacity_mapping_stable"
      ],
      "sample": {
        "market_state_parameter_audit_complete": true,
        "strategy_logic_changed": false,
        "audit_only": true,
        "formula_not_patched": true,
        "backtest_engine_run": false,
        "short_window_existing_engine_run": false,
        "full_5y_backtest_run": false,
        "forward_runner_run": false,
        "candidate_generation_extracted": false,
        "buy_add_reduce_exit_extracted": false,
        "official_result_generated": false,
        "dashboard_changed": false,
        "strategy_files_unchanged": true,
        "k2_r7_loaded": true,
        "r7_trace_loaded": true,
        "r7_equivalence_ok": true,
        "trace_rows_loaded": true,
        "source_scan_complete": true,
        "assumption_gets_extracted": true,
        "market_gate_parameters_documented": true,
        "market_state_distribution_documented": true,
        "entry_capacity_mapping_documented": true,
        "entry_capacity_mapping_stable": true,
        "focused_rows_documented": true,
        "unresolved_count": 0
      }
    },
    {
      "path": "decision",
      "matched_keys": [
        "k2_r8_market_state_parameter_audit_passed",
        "candidate_extraction_allowed_now",
        "short_window_market_state_replication_ready"
      ],
      "sample": {
        "k2_r8_market_state_parameter_audit_passed": true,
        "formula_patch_allowed_now": false,
        "candidate_extraction_allowed_now": false,
        "implementation_may_resume": false,
        "unresolved": [],
        "short_window_market_state_replication_ready": true,
        "full_115_replication_ready": true,
        "next_required_stage": "4C-2C-4E-ENGINE-K2-R9-MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL",
        "conclusion": "K2_R8_PASS_MARKET_STATE_PARAMETERS_READY_FOR_REPLICATION_PROPOSAL",
        "recommended_next_action": "Audit the exact full E1R 115% run artifact and assumptions before standalone replication, because short-window source equivalence is not enough to prove full 115% parameter identity."
      }
    }
  ],
  "list_candidate_count": 2,
  "list_candidates_sample": [
    {
      "path": "parameter_audit.focused_rows",
      "length": 17,
      "dict_sample_count": 17,
      "sample_keys": [
        "_shock_active",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "date",
        "entry_capacity",
        "expected_market_gate_state",
        "holdings_count",
        "market_entry_allowed",
        "market_risk_off",
        "market_shock",
        "market_state",
        "pending_orders_count",
        "source_quality",
        "spx_close_t",
        "spx_day_return",
        "spx_ma50_t"
      ],
      "matched_keys": [
        "_shock_active",
        "captured__gate_state",
        "computed_gate_state_from_captured_inputs",
        "date",
        "entry_capacity",
        "expected_market_gate_state",
        "market_entry_allowed",
        "market_risk_off",
        "market_shock",
        "market_state",
        "spx_close_t",
        "spx_day_return",
        "spx_ma50_t"
      ],
      "sample_first": {
        "date": "2021-05-03",
        "expected_market_gate_state": "ALLOW",
        "captured__gate_state": "ALLOW",
        "computed_gate_state_from_captured_inputs": "ALLOW",
        "market_entry_allowed": true,
        "market_shock": false,
        "market_risk_off": false,
        "market_state": "CAUTIOUS_ON",
        "_shock_active": false,
        "entry_capacity": 2,
        "spx_close_t": 4192.660156,
        "spx_ma50_t": 4008.45681644,
        "spx_day_return": 0.0027480906574836577,
        "holdings_count": 3,
        "pending_orders_count": 1,
        "source_quality": "legacy_sys_trace_locals"
      }
    },
    {
      "path": "parameter_audit.transitions",
      "length": 12,
      "dict_sample_count": 12,
      "sample_keys": [
        "changed",
        "date",
        "prev_date"
      ],
      "matched_keys": [
        "date",
        "prev_date"
      ],
      "sample_first": {
        "date": "2021-05-03",
        "changed": {
          "market_state": {
            "from": "FULL_ON",
            "to": "CAUTIOUS_ON"
          },
          "entry_capacity": {
            "from": 3,
            "to": 2
          }
        },
        "prev_date": "2021-04-30"
      }
    }
  ]
}
```

## Corrected Review
```json
{
  "generated_at": "2026-07-11T05:47:27.539979+00:00",
  "title": "E1R K2 R12B Review And Simplified Next Steps",
  "current_truth": [
    "R12 did not pass.",
    "No strategy integration is allowed.",
    "No R13 wiring proposal is allowed until R12C passes or a better golden-row source is explicitly approved.",
    "The standalone MarketGateEvaluator skeleton from R11 remains intact, but equivalence is not proven."
  ],
  "r12_failure_causes": [
    {
      "id": "R12B_RC1_GOLDEN_ROW_EXTRACTION_FAILED",
      "evidence": "R12 golden_row_extraction selected_source=null and row_count=0.",
      "meaning": "The extractor assumed the wrong R7/R8 JSON structure."
    },
    {
      "id": "R12B_RC2_PYTEST_DEPENDENCY_ASSUMED",
      "evidence": "R12 pytest_smoke stderr says No module named pytest.",
      "meaning": "R12 should not require pytest in this local workflow; use pure-Python smoke fallback."
    },
    {
      "id": "R12B_RC3_REVIEW_NEXT_STEP_CONFLICT",
      "evidence": "R12 decision says R12B, while review still listed R13 as recommended.",
      "meaning": "Review generation must branch on failure and recommend R12C/RCA, not R13."
    }
  ],
  "simplified_next_step": {
    "stage": "4C-2C-4E-ENGINE-K2-R12C-MARKET_GATE_GOLDEN_ROW_LOCATOR_AND_EQUIVALENCE_RETRY",
    "purpose": "One compact retry: locate real golden rows first, then run pure-Python equivalence only if rows are found.",
    "rules": [
      "Do not use pytest.",
      "Do not integrate strategy.",
      "Do not run full 5Y.",
      "If row_count remains 0, stop and inspect R7/R8 manually instead of adding complexity."
    ]
  },
  "do_not_do_next": [
    "Do not proceed to R13.",
    "Do not patch market_gate.py based on zero-row equivalence.",
    "Do not install dependencies just to make R12 pass.",
    "Do not treat mismatch_count=0 as success when row_count=0."
  ],
  "r12_failure_summary": {
    "r12_report_exists": true,
    "status": "MARKET_GATE_EQUIVALENCE_SMOKE_COMPLETE",
    "golden_row_extraction": {
      "sources": [
        {
          "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R7_MARKET_STATE_SOURCE_EQUIVALENCE_TRACE.json",
          "exists": true,
          "sha256": "593161d81dd3a9951b7039505e6ea041a3653e2c44dcfa05c2b933796991a468",
          "candidate_lists": [],
          "best": null
        },
        {
          "path": "docs/research/E1R_4C2C4E_ENGINE_K2_R8_MARKET_STATE_PARAMETER_AUDIT.json",
          "exists": true,
          "sha256": "aaf28cdf0b60a29480f4a8c3936dd8b2fe8d31b17a50e4578df1566903670063",
          "candidate_lists": [],
          "best": null
        }
      ],
      "selected_source": null,
      "error": "No usable golden row list found in R7/R8.",
      "row_count": 0,
      "sample_rows": []
    },
    "equivalence": {
      "row_count": 0,
      "mismatch_count": 0,
      "ok": false,
      "distribution": {
        "expected_gate_state": {},
        "actual_gate_state": {},
        "expected_market_state": {}
      },
      "sample_comparisons": [],
      "mismatches": []
    },
    "pytest_smoke": {
      "cmd": [
        "/Library/Developer/CommandLineTools/usr/bin/python3",
        "-m",
        "pytest",
        "-q",
        "/Users/dongfang/Downloads/sp500-tracker-v13/tests/e1r_engine/test_market_gate_equivalence.py"
      ],
      "returncode": 1,
      "stdout": "",
      "stderr": "/Library/Developer/CommandLineTools/usr/bin/python3: No module named pytest\n",
      "ok": false
    },
    "validations": {
      "market_gate_equivalence_smoke_complete": true,
      "r7_loaded": true,
      "r8_loaded": true,
      "r9d_loaded": true,
      "r10_loaded": true,
      "r11_loaded": true,
      "r11_authorized_r12": true,
      "golden_rows_found": false,
      "golden_rows_count": 0,
      "equivalence_run": true,
      "equivalence_passed": false,
      "mismatch_count_zero": true,
      "pytest_file_created": true,
      "pytest_smoke_run": true,
      "pytest_smoke_passed": false,
      "strategy_logic_changed": false,
      "standalone_module_only": true,
      "strategy_integration_changed": false,
      "legacy_backtest_called": false,
      "backtest_engine_run": false,
      "short_window_existing_engine_run": false,
      "full_5y_backtest_run": false,
      "forward_runner_run": false,
      "candidate_generation_extracted": false,
      "buy_add_reduce_exit_extracted": false,
      "official_result_generated": false,
      "dashboard_changed": false,
      "formula_not_patched_in_legacy": true,
      "strategy_files_unchanged": true
    },
    "decision": {
      "k2_r12_market_gate_equivalence_smoke_passed": false,
      "market_gate_equivalence_ready": false,
      "market_gate_strategy_integration_allowed_now": false,
      "formula_patch_allowed_now": false,
      "candidate_extraction_allowed_now": false,
      "implementation_may_resume": false,
      "requires_user_approval_before_next_stage": true,
      "next_stage_after_user_approval": "4C-2C-4E-ENGINE-K2-R12B-MARKET_GATE_EQUIVALENCE_GAP_RCA",
      "conclusion": "K2_R12_EQUIVALENCE_GAPS_REMAIN_DO_NOT_INTEGRATE",
      "recommended_next_action": "Stop and perform R12B RCA/gap closure before any wiring proposal."
    }
  }
}
```

## Validations
```json
{
  "r12b_gap_rca_complete": true,
  "r7_loaded": true,
  "r8_loaded": true,
  "r11_loaded": true,
  "r12_failed_report_loaded": true,
  "r7_structure_inspected": true,
  "r8_structure_inspected": true,
  "pytest_availability_checked": true,
  "pytest_available": false,
  "r12_failure_preserved": true,
  "strategy_logic_changed": false,
  "strategy_integration_changed": false,
  "legacy_backtest_called": false,
  "backtest_engine_run": false,
  "full_5y_backtest_run": false,
  "candidate_generation_extracted": false,
  "buy_add_reduce_exit_extracted": false,
  "dashboard_changed": false,
  "strategy_files_unchanged": true
}
```

## Decision
```json
{
  "k2_r12b_market_gate_equivalence_gap_rca_passed": true,
  "r12_failure_confirmed": true,
  "market_gate_equivalence_ready": false,
  "market_gate_strategy_integration_allowed_now": false,
  "formula_patch_allowed_now": false,
  "candidate_extraction_allowed_now": false,
  "implementation_may_resume": false,
  "candidate_golden_paths_found_for_next_retry": true,
  "next_stage_after_user_approval": "4C-2C-4E-ENGINE-K2-R12C-MARKET_GATE_GOLDEN_ROW_LOCATOR_AND_EQUIVALENCE_RETRY",
  "conclusion": "K2_R12B_PASS_GAP_RCA_DONE_DO_NOT_INTEGRATE_READY_FOR_R12C_MINIMAL_RETRY",
  "recommended_next_action": "Run one minimal R12C retry that first locates golden rows and uses pure-Python assertions. Do not proceed to R13."
}
```
