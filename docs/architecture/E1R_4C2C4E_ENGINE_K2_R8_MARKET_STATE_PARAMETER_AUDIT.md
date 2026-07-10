# E1R 4C-2C-4E-ENGINE-K2-R8 — Market State Parameter Audit

Generated At: `2026-07-10T13:03:59.470621+00:00`

## Purpose
Audit exact market-state and market-gate parameters before copying the E1R 115% market-state behavior.

## Parameter Audit
```json
{
  "market_gate_parameters": {
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
  },
  "observed_market_state_distribution": {
    "FULL_ON": 46,
    "CAUTIOUS_ON": 7,
    "CASH_MODE": 9
  },
  "observed_shock_distribution": {
    "False": 61,
    "True": 1
  },
  "observed_entry_capacity_distribution": {
    "3": 46,
    "2": 7,
    "0": 9
  },
  "observed_gate_state_distribution": {
    "None": 62
  },
  "entry_capacity_mapping_by_market_state": {
    "mapping": {
      "FULL_ON": [
        3
      ],
      "CAUTIOUS_ON": [
        2
      ],
      "CASH_MODE": [
        0
      ]
    },
    "conflicts": [],
    "stable_mapping": true
  },
  "focused_rows": [
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
  ],
  "transitions": [
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
      "date": "2021-05-20",
      "changed": {
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
      },
      "prev_date": "2021-05-19"
    },
    {
      "date": "2021-05-21",
      "changed": {
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
      },
      "prev_date": "2021-05-20"
    },
    {
      "date": "2021-05-24",
      "changed": {
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
      },
      "prev_date": "2021-05-21"
    },
    {
      "date": "2021-06-03",
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
      "prev_date": "2021-06-02"
    },
    {
      "date": "2021-06-04",
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
      "prev_date": "2021-06-03"
    },
    {
      "date": "2021-06-18",
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
      "prev_date": "2021-06-17"
    },
    {
      "date": "2021-06-21",
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
      "prev_date": "2021-06-18"
    }
  ],
  "golden_master_controls": {
    "strategy_controls": {
      "entry_rs_min": 90.0,
      "ls60_exit_mode": "reduce",
      "candidate_top_n": null,
      "qualified_entry_enabled": false,
      "qualified_rs_min": 90.0,
      "qualified_momentum_min": 85.0,
      "qualified_th_min": 75.0,
      "qualified_states": [
        "Expansion"
      ],
      "qualified_price_above_ma50": true,
      "qualified_ma50_slope_min": 0.0,
      "qp_avg_pool_size": 0.0,
      "qp_pool_days": 0,
      "qp_days_pool_lt_3": 0,
      "qp_days_pool_ge_10": 0,
      "qp_buy_orders_generated": 0,
      "min_holding_days": 0,
      "min_hold_allow_broken_exit": true,
      "e1r_regime_wiring_enabled": false,
      "e1r_regime_source": null,
      "relative_stop_enabled": false,
      "relative_stop_underperform_pct": -8.0,
      "relative_stop_action": "REL_REDUCE",
      "relative_stop_once_per_position": true,
      "relative_stop_stats": {
        "signals": 0,
        "executed": 0
      },
      "fixed_take_profit_enabled": false
    },
    "market_entry_gate": {
      "variant": "D3_RISK_OFF_PLUS_SHOCK_GATE",
      "enabled": true,
      "risk_off_rule": "SPX close < SPX MA50",
      "market_shock_rule": "SPX daily return <= -2.0%",
      "blocked_actions": [
        "BUY",
        "ADD"
      ],
      "unaffected_actions": [
        "HOLD",
        "REDUCE",
        "EXIT"
      ],
      "days": {
        "entry_allowed": 53,
        "risk_off": 8,
        "market_shock": 1,
        "blocked_total": 9
      }
    },
    "version": "v1.6-top3-rs-minhold-relstop",
    "strategy_variant": "top3_entry_rs_minhold_relstop",
    "entry_top_n": 3,
    "rank_based_exit": false,
    "e1r_uptrend_execution_enabled": false,
    "status": "INSUFFICIENT_SAMPLE"
  },
  "source_assumption_gets_relevant": [
    {
      "line": 845,
      "key": "entry_top_n",
      "default_expr": "3",
      "text": "    entry_top_n = int(a.get(\"entry_top_n\", 3))",
      "context": {
        "start": 841,
        "end": 849,
        "rows": [
          {
            "line": 841,
            "text": "        if not weights:"
          },
          {
            "line": 842,
            "text": "            return \"UNCLASSIFIED\" if e1r_regime_wiring_enabled else \"N/A\""
          },
          {
            "line": 843,
            "text": "        return max(weights.items(), key=lambda kv: kv[1])[0]"
          },
          {
            "line": 844,
            "text": ""
          },
          {
            "line": 845,
            "text": "    entry_top_n = int(a.get(\"entry_top_n\", 3))"
          },
          {
            "line": 846,
            "text": "    rank_based_exit = bool(a.get(\"rank_based_exit\", False))"
          },
          {
            "line": 847,
            "text": "    market_gate_enabled = bool(a.get(\"market_gate_enabled\", True))"
          },
          {
            "line": 848,
            "text": "    risk_off_below_spx_ma50 = bool(a.get(\"risk_off_below_spx_ma50\", True))"
          },
          {
            "line": 849,
            "text": "    ls60_exit_mode = a.get(\"ls60_exit_mode\", \"reduce\")  # \"exit\"=旧规则 \"reduce\"=新规则"
          }
        ]
      }
    },
    {
      "line": 847,
      "key": "market_gate_enabled",
      "default_expr": "True",
      "text": "    market_gate_enabled = bool(a.get(\"market_gate_enabled\", True))",
      "context": {
        "start": 843,
        "end": 851,
        "rows": [
          {
            "line": 843,
            "text": "        return max(weights.items(), key=lambda kv: kv[1])[0]"
          },
          {
            "line": 844,
            "text": ""
          },
          {
            "line": 845,
            "text": "    entry_top_n = int(a.get(\"entry_top_n\", 3))"
          },
          {
            "line": 846,
            "text": "    rank_based_exit = bool(a.get(\"rank_based_exit\", False))"
          },
          {
            "line": 847,
            "text": "    market_gate_enabled = bool(a.get(\"market_gate_enabled\", True))"
          },
          {
            "line": 848,
            "text": "    risk_off_below_spx_ma50 = bool(a.get(\"risk_off_below_spx_ma50\", True))"
          },
          {
            "line": 849,
            "text": "    ls60_exit_mode = a.get(\"ls60_exit_mode\", \"reduce\")  # \"exit\"=旧规则 \"reduce\"=新规则"
          },
          {
            "line": 850,
            "text": ""
          },
          {
            "line": 851,
            "text": "    # Qualified Candidate Pool 参数"
          }
        ]
      }
    },
    {
      "line": 848,
      "key": "risk_off_below_spx_ma50",
      "default_expr": "True",
      "text": "    risk_off_below_spx_ma50 = bool(a.get(\"risk_off_below_spx_ma50\", True))",
      "context": {
        "start": 844,
        "end": 852,
        "rows": [
          {
            "line": 844,
            "text": ""
          },
          {
            "line": 845,
            "text": "    entry_top_n = int(a.get(\"entry_top_n\", 3))"
          },
          {
            "line": 846,
            "text": "    rank_based_exit = bool(a.get(\"rank_based_exit\", False))"
          },
          {
            "line": 847,
            "text": "    market_gate_enabled = bool(a.get(\"market_gate_enabled\", True))"
          },
          {
            "line": 848,
            "text": "    risk_off_below_spx_ma50 = bool(a.get(\"risk_off_below_spx_ma50\", True))"
          },
          {
            "line": 849,
            "text": "    ls60_exit_mode = a.get(\"ls60_exit_mode\", \"reduce\")  # \"exit\"=旧规则 \"reduce\"=新规则"
          },
          {
            "line": 850,
            "text": ""
          },
          {
            "line": 851,
            "text": "    # Qualified Candidate Pool 参数"
          },
          {
            "line": 852,
            "text": "    candidate_top_n           = a.get(\"candidate_top_n\", None)   # None = 沿用旧 entry_top_n"
          }
        ]
      }
    },
    {
      "line": 853,
      "key": "qualified_entry_enabled",
      "default_expr": "False",
      "text": "    qualified_entry_enabled   = bool(a.get(\"qualified_entry_enabled\", False))",
      "context": {
        "start": 849,
        "end": 857,
        "rows": [
          {
            "line": 849,
            "text": "    ls60_exit_mode = a.get(\"ls60_exit_mode\", \"reduce\")  # \"exit\"=旧规则 \"reduce\"=新规则"
          },
          {
            "line": 850,
            "text": ""
          },
          {
            "line": 851,
            "text": "    # Qualified Candidate Pool 参数"
          },
          {
            "line": 852,
            "text": "    candidate_top_n           = a.get(\"candidate_top_n\", None)   # None = 沿用旧 entry_top_n"
          },
          {
            "line": 853,
            "text": "    qualified_entry_enabled   = bool(a.get(\"qualified_entry_enabled\", False))"
          },
          {
            "line": 854,
            "text": "    qualified_rs_min          = float(a.get(\"qualified_rs_min\", 90.0))"
          },
          {
            "line": 855,
            "text": "    qualified_momentum_min    = float(a.get(\"qualified_momentum_min\", 85.0))"
          },
          {
            "line": 856,
            "text": "    qualified_th_min          = float(a.get(\"qualified_th_min\", 75.0))"
          },
          {
            "line": 857,
            "text": "    qualified_states          = set(a.get(\"qualified_states\", [\"Expansion\"]))"
          }
        ]
      }
    },
    {
      "line": 896,
      "key": "market_shock_gate_enabled",
      "default_expr": "True",
      "text": "    market_shock_gate_enabled = bool(a.get(\"market_shock_gate_enabled\", True))",
      "context": {
        "start": 892,
        "end": 900,
        "rows": [
          {
            "line": 892,
            "text": "    else:"
          },
          {
            "line": 893,
            "text": "        logger.info(f\"  Entry mode: Strict Top{entry_top_n} (legacy)\")"
          },
          {
            "line": 894,
            "text": "    if ls60_exit_mode not in {\"exit\", \"reduce\"}:"
          },
          {
            "line": 895,
            "text": "        raise ValueError(f\"Invalid ls60_exit_mode={ls60_exit_mode!r}; expected 'exit' or 'reduce'\")"
          },
          {
            "line": 896,
            "text": "    market_shock_gate_enabled = bool(a.get(\"market_shock_gate_enabled\", True))"
          },
          {
            "line": 897,
            "text": "    market_shock_daily_return = float(a.get(\"market_shock_daily_return\", -0.02))"
          },
          {
            "line": 898,
            "text": "    take_profit_enabled = bool(a.get(\"partial_take_profit_enabled\", False))"
          },
          {
            "line": 899,
            "text": "    take_profit_threshold = float(a.get(\"partial_take_profit_threshold\", 0.07))"
          },
          {
            "line": 900,
            "text": "    take_profit_fraction = float(a.get(\"partial_take_profit_fraction\", 0.50))"
          }
        ]
      }
    },
    {
      "line": 897,
      "key": "market_shock_daily_return",
      "default_expr": "-0.02",
      "text": "    market_shock_daily_return = float(a.get(\"market_shock_daily_return\", -0.02))",
      "context": {
        "start": 893,
        "end": 901,
        "rows": [
          {
            "line": 893,
            "text": "        logger.info(f\"  Entry mode: Strict Top{entry_top_n} (legacy)\")"
          },
          {
            "line": 894,
            "text": "    if ls60_exit_mode not in {\"exit\", \"reduce\"}:"
          },
          {
            "line": 895,
            "text": "        raise ValueError(f\"Invalid ls60_exit_mode={ls60_exit_mode!r}; expected 'exit' or 'reduce'\")"
          },
          {
            "line": 896,
            "text": "    market_shock_gate_enabled = bool(a.get(\"market_shock_gate_enabled\", True))"
          },
          {
            "line": 897,
            "text": "    market_shock_daily_return = float(a.get(\"market_shock_daily_return\", -0.02))"
          },
          {
            "line": 898,
            "text": "    take_profit_enabled = bool(a.get(\"partial_take_profit_enabled\", False))"
          },
          {
            "line": 899,
            "text": "    take_profit_threshold = float(a.get(\"partial_take_profit_threshold\", 0.07))"
          },
          {
            "line": 900,
            "text": "    take_profit_fraction = float(a.get(\"partial_take_profit_fraction\", 0.50))"
          },
          {
            "line": 901,
            "text": "    block_add_after_take_profit = bool(a.get(\"block_add_after_take_profit\", False))"
          }
        ]
      }
    },
    {
      "line": 902,
      "key": "entry_rs_min",
      "default_expr": "90.0",
      "text": "    entry_rs_min = float(a.get(\"entry_rs_min\", 90.0))",
      "context": {
        "start": 898,
        "end": 906,
        "rows": [
          {
            "line": 898,
            "text": "    take_profit_enabled = bool(a.get(\"partial_take_profit_enabled\", False))"
          },
          {
            "line": 899,
            "text": "    take_profit_threshold = float(a.get(\"partial_take_profit_threshold\", 0.07))"
          },
          {
            "line": 900,
            "text": "    take_profit_fraction = float(a.get(\"partial_take_profit_fraction\", 0.50))"
          },
          {
            "line": 901,
            "text": "    block_add_after_take_profit = bool(a.get(\"block_add_after_take_profit\", False))"
          },
          {
            "line": 902,
            "text": "    entry_rs_min = float(a.get(\"entry_rs_min\", 90.0))"
          },
          {
            "line": 903,
            "text": "    min_holding_days = int(a.get(\"min_holding_days\", 0))"
          },
          {
            "line": 904,
            "text": "    # E2 Dynamic Exit parameters"
          },
          {
            "line": 905,
            "text": "    dynamic_exit_enabled   = bool(a.get(\"dynamic_exit_enabled\", False))"
          },
          {
            "line": 906,
            "text": "    min_hold_allow_broken_exit = bool(a.get(\"min_hold_allow_broken_exit\", True))"
          }
        ]
      }
    }
  ]
}
```

## Unresolved
```json
[]
```

## Validations
```json
{
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
```

## Decision
```json
{
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
```
