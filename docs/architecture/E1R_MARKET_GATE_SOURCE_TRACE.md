# E1R 4C-2C-4E-ENGINE-K2-R2 — Market Gate Source Trace

Generated At: `2026-07-10T11:55:31.551949+00:00`

## Purpose
Inspect exact source contexts for legacy market gate after K2 mismatch.

## Policy
```json
{
  "strategy_logic_changed": false,
  "audit_only": true,
  "formula_not_patched": true,
  "backtest_engine_run": false,
  "full_5y_backtest_run": false,
  "forward_runner_run": false,
  "provider_extraction_run": false,
  "candidate_generation_extracted": false,
  "buy_add_reduce_exit_extracted": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "frozen_strategy_files_changed": false
}
```

## Source
```json
{
  "backtest_path": "src/engine/backtest.py",
  "backtest_sha256": "906605eacae917f8288a3cf5d76bea5596b01f774d810ae24c3df9ef46230aea",
  "function_bounds": {
    "name": "run_stateful_simulation",
    "start_line": 763,
    "end_line": 2486,
    "line_count": 1724
  }
}
```

## Hit Summary
```json
{
  "hit_count": 117,
  "by_keyword": {
    "D3_RISK_OFF_PLUS_SHOCK_GATE": 1,
    "RiskOff": 1,
    "SPX<MA50": 1,
    "Shock": 1,
    "gate=": 2,
    "gate_state": 5,
    "ma50": 59,
    "market_entry_gate": 1,
    "market_gate": 25,
    "market_gate_state": 2,
    "risk_off": 13,
    "shock": 27,
    "spx_ma50": 14
  },
  "by_regex": {
    "D3_RISK_OFF_PLUS_SHOCK_GATE": 1,
    "SPX<MA50": 1,
    "gate_state\\s*=": 2,
    "market_gate": 25,
    "risk_off\\s*=": 3,
    "shock\\s*=": 3,
    "spx_ma50\\s*=": 1
  },
  "hit_lines": [
    847,
    848,
    858,
    859,
    885,
    891,
    896,
    897,
    911,
    912,
    913,
    914,
    927,
    928,
    929,
    930,
    938,
    1037,
    1038,
    1072,
    1074,
    1075,
    1386,
    1393,
    1397,
    1398,
    1400,
    1404,
    1405,
    1407,
    1413,
    1414,
    1421,
    1428,
    1434,
    1435,
    1436,
    1437,
    1438,
    1447,
    1448,
    1449,
    1450,
    1459,
    1464,
    1466,
    1475,
    1483,
    1484,
    1487,
    1488,
    1489,
    1490,
    1492,
    1494,
    1510,
    1512,
    1525,
    1531,
    1572,
    1573,
    1574,
    1584,
    1601,
    1602,
    1634,
    1644,
    1653,
    1654,
    1661,
    1662,
    1688,
    1690,
    1739,
    1740,
    1768,
    1769,
    1820,
    1824,
    1833,
    1834,
    1872,
    1876,
    1904,
    1905,
    1906,
    1912,
    1922,
    1938,
    1939,
    1940,
    1941,
    1942,
    1972,
    1977,
    1992,
    1997,
    2137,
    2138,
    2142,
    2155,
    2157,
    2160,
    2330,
    2331,
    2332,
    2333,
    2373,
    2374,
    2404,
    2405,
    2406,
    2407,
    2408,
    2409,
    2410,
    2414
  ]
}
```

## Focused Mismatch Window Rows
```json
{
  "rows": [
    {
      "date": "2021-05-03",
      "market_gate_state": "ALLOW",
      "spx_close": 4192.66,
      "spx_ma50": 4008.46,
      "spx_day_return_pct": 0.2748,
      "spx_regime": null,
      "risk_budget": null,
      "risk_budget_mode": null,
      "event": "EOD_MARK_TO_MARKET",
      "open_positions_count": 3,
      "pending_orders_count": 1,
      "exposure_pct": 15.09
    },
    {
      "date": "2021-05-04",
      "market_gate_state": "ALLOW",
      "spx_close": 4164.66,
      "spx_ma50": 4014.22,
      "spx_day_return_pct": -0.6678,
      "spx_regime": null,
      "risk_budget": null,
      "risk_budget_mode": null,
      "event": "EOD_MARK_TO_MARKET",
      "open_positions_count": 3,
      "pending_orders_count": 1,
      "exposure_pct": 15.01
    },
    {
      "date": "2021-05-05",
      "market_gate_state": "ALLOW",
      "spx_close": 4167.59,
      "spx_ma50": 4019.94,
      "spx_day_return_pct": 0.0703,
      "spx_regime": null,
      "risk_budget": null,
      "risk_budget_mode": null,
      "event": "EOD_MARK_TO_MARKET",
      "open_positions_count": 3,
      "pending_orders_count": 1,
      "exposure_pct": 15.15
    },
    {
      "date": "2021-05-06",
      "market_gate_state": "ALLOW",
      "spx_close": 4201.62,
      "spx_ma50": 4025.47,
      "spx_day_return_pct": 0.8165,
      "spx_regime": null,
      "risk_budget": null,
      "risk_budget_mode": null,
      "event": "EOD_MARK_TO_MARKET",
      "open_positions_count": 3,
      "pending_orders_count": 1,
      "exposure_pct": 15.18
    },
    {
      "date": "2021-05-07",
      "market_gate_state": "ALLOW",
      "spx_close": 4232.6,
      "spx_ma50": 4033.53,
      "spx_day_return_pct": 0.7373,
      "spx_regime": null,
      "risk_budget": null,
      "risk_budget_mode": null,
      "event": "EOD_MARK_TO_MARKET",
      "open_positions_count": 3,
      "pending_orders_count": 1,
      "exposure_pct": 15.44
    },
    {
      "date": "2021-05-10",
      "market_gate_state": "RISK_OFF",
      "spx_close": 4188.43,
      "spx_ma50": 4041.08,
      "spx_day_return_pct": -1.0436,
      "spx_regime": null,
      "risk_budget": null,
      "risk_budget_mode": null,
      "event": "EOD_MARK_TO_MARKET",
      "open_positions_count": 3,
      "pending_orders_count": 1,
      "exposure_pct": 15.2
    },
    {
      "date": "2021-05-11",
      "market_gate_state": "RISK_OFF",
      "spx_close": 4152.1,
      "spx_ma50": 4046.08,
      "spx_day_return_pct": -0.8674,
      "spx_regime": null,
      "risk_budget": null,
      "risk_budget_mode": null,
      "event": "EOD_MARK_TO_MARKET",
      "open_positions_count": 3,
      "pending_orders_count": 1,
      "exposure_pct": 14.79
    },
    {
      "date": "2021-05-12",
      "market_gate_state": "SHOCK",
      "spx_close": 4063.04,
      "spx_ma50": 4049.94,
      "spx_day_return_pct": -2.1449,
      "spx_regime": null,
      "risk_budget": null,
      "risk_budget_mode": null,
      "event": "EOD_MARK_TO_MARKET",
      "open_positions_count": 3,
      "pending_orders_count": 1,
      "exposure_pct": 14.01
    },
    {
      "date": "2021-05-13",
      "market_gate_state": "RISK_OFF",
      "spx_close": 4112.5,
      "spx_ma50": 4055.8,
      "spx_day_return_pct": 1.2173,
      "spx_regime": null,
      "risk_budget": null,
      "risk_budget_mode": null,
      "event": "EOD_MARK_TO_MARKET",
      "open_positions_count": 3,
      "pending_orders_count": 3,
      "exposure_pct": 14.47
    },
    {
      "date": "2021-05-14",
      "market_gate_state": "RISK_OFF",
      "spx_close": 4173.85,
      "spx_ma50": 4063.9,
      "spx_day_return_pct": 1.4918,
      "spx_regime": null,
      "risk_budget": null,
      "risk_budget_mode": null,
      "event": "EOD_MARK_TO_MARKET",
      "open_positions_count": 3,
      "pending_orders_count": 3,
      "exposure_pct": 14.66
    },
    {
      "date": "2021-05-17",
      "market_gate_state": "RISK_OFF",
      "spx_close": 4163.29,
      "spx_ma50": 4070.33,
      "spx_day_return_pct": -0.253,
      "spx_regime": null,
      "risk_budget": null,
      "risk_budget_mode": null,
      "event": "EOD_MARK_TO_MARKET",
      "open_positions_count": 3,
      "pending_orders_count": 3,
      "exposure_pct": 14.58
    },
    {
      "date": "2021-05-18",
      "market_gate_state": "RISK_OFF",
      "spx_close": 4127.83,
      "spx_ma50": 4076.46,
      "spx_day_return_pct": -0.8517,
      "spx_regime": null,
      "risk_budget": null,
      "risk_budget_mode": null,
      "event": "EOD_MARK_TO_MARKET",
      "open_positions_count": 3,
      "pending_orders_count": 2,
      "exposure_pct": 14.29
    },
    {
      "date": "2021-05-19",
      "market_gate_state": "RISK_OFF",
      "spx_close": 4115.68,
      "spx_ma50": 4081.26,
      "spx_day_return_pct": -0.2943,
      "spx_regime": null,
      "risk_budget": null,
      "risk_budget_mode": null,
      "event": "EOD_MARK_TO_MARKET",
      "open_positions_count": 3,
      "pending_orders_count": 2,
      "exposure_pct": 14.16
    },
    {
      "date": "2021-05-20",
      "market_gate_state": "ALLOW",
      "spx_close": 4159.12,
      "spx_ma50": 4086.47,
      "spx_day_return_pct": 1.0555,
      "spx_regime": null,
      "risk_budget": null,
      "risk_budget_mode": null,
      "event": "EOD_MARK_TO_MARKET",
      "open_positions_count": 3,
      "pending_orders_count": 3,
      "exposure_pct": 14.3
    },
    {
      "date": "2021-05-21",
      "market_gate_state": "RISK_OFF",
      "spx_close": 4155.86,
      "spx_ma50": 4090.8,
      "spx_day_return_pct": -0.0784,
      "spx_regime": null,
      "risk_budget": null,
      "risk_budget_mode": null,
      "event": "EOD_MARK_TO_MARKET",
      "open_positions_count": 3,
      "pending_orders_count": 3,
      "exposure_pct": 14.2
    },
    {
      "date": "2021-05-24",
      "market_gate_state": "ALLOW",
      "spx_close": 4197.05,
      "spx_ma50": 4095.88,
      "spx_day_return_pct": 0.9911,
      "spx_regime": null,
      "risk_budget": null,
      "risk_budget_mode": null,
      "event": "EOD_MARK_TO_MARKET",
      "open_positions_count": 3,
      "pending_orders_count": 3,
      "exposure_pct": 14.39
    },
    {
      "date": "2021-06-18",
      "market_gate_state": "ALLOW",
      "spx_close": 4166.45,
      "spx_ma50": 4181.59,
      "spx_day_return_pct": -1.3124,
      "spx_regime": null,
      "risk_budget": null,
      "risk_budget_mode": null,
      "event": "EOD_MARK_TO_MARKET",
      "open_positions_count": 3,
      "pending_orders_count": 3,
      "exposure_pct": 15.49
    }
  ],
  "row_count": 17
}
```

## Diagnostic Hypotheses
```json
{
  "diagnostic_only": true,
  "best_hypotheses": [
    {
      "name": "trigger_dayret_None_cooldown_5_include_ma50_False",
      "ok": false,
      "mismatch_count": 3,
      "distribution": {
        "ALLOW": 56,
        "SHOCK": 1,
        "RISK_OFF": 5
      },
      "mismatches": [
        {
          "date": "2021-05-10",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -1.0436,
          "close": 4188.43,
          "ma50": 4041.08
        },
        {
          "date": "2021-05-11",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.8674,
          "close": 4152.1,
          "ma50": 4046.08
        },
        {
          "date": "2021-05-21",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.0784,
          "close": 4155.86,
          "ma50": 4090.8
        }
      ]
    },
    {
      "name": "trigger_dayret_None_cooldown_7_include_ma50_False",
      "ok": false,
      "mismatch_count": 3,
      "distribution": {
        "ALLOW": 54,
        "SHOCK": 1,
        "RISK_OFF": 7
      },
      "mismatches": [
        {
          "date": "2021-05-10",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -1.0436,
          "close": 4188.43,
          "ma50": 4041.08
        },
        {
          "date": "2021-05-11",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.8674,
          "close": 4152.1,
          "ma50": 4046.08
        },
        {
          "date": "2021-05-20",
          "expected": "ALLOW",
          "actual": "RISK_OFF",
          "day_ret": 1.0555,
          "close": 4159.12,
          "ma50": 4086.47
        }
      ]
    },
    {
      "name": "trigger_dayret_-1.5_cooldown_5_include_ma50_False",
      "ok": false,
      "mismatch_count": 3,
      "distribution": {
        "ALLOW": 56,
        "SHOCK": 1,
        "RISK_OFF": 5
      },
      "mismatches": [
        {
          "date": "2021-05-10",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -1.0436,
          "close": 4188.43,
          "ma50": 4041.08
        },
        {
          "date": "2021-05-11",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.8674,
          "close": 4152.1,
          "ma50": 4046.08
        },
        {
          "date": "2021-05-21",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.0784,
          "close": 4155.86,
          "ma50": 4090.8
        }
      ]
    },
    {
      "name": "trigger_dayret_-1.5_cooldown_7_include_ma50_False",
      "ok": false,
      "mismatch_count": 3,
      "distribution": {
        "ALLOW": 54,
        "SHOCK": 1,
        "RISK_OFF": 7
      },
      "mismatches": [
        {
          "date": "2021-05-10",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -1.0436,
          "close": 4188.43,
          "ma50": 4041.08
        },
        {
          "date": "2021-05-11",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.8674,
          "close": 4152.1,
          "ma50": 4046.08
        },
        {
          "date": "2021-05-20",
          "expected": "ALLOW",
          "actual": "RISK_OFF",
          "day_ret": 1.0555,
          "close": 4159.12,
          "ma50": 4086.47
        }
      ]
    },
    {
      "name": "trigger_dayret_None_cooldown_4_include_ma50_False",
      "ok": false,
      "mismatch_count": 4,
      "distribution": {
        "ALLOW": 57,
        "SHOCK": 1,
        "RISK_OFF": 4
      },
      "mismatches": [
        {
          "date": "2021-05-10",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -1.0436,
          "close": 4188.43,
          "ma50": 4041.08
        },
        {
          "date": "2021-05-11",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.8674,
          "close": 4152.1,
          "ma50": 4046.08
        },
        {
          "date": "2021-05-19",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.2943,
          "close": 4115.68,
          "ma50": 4081.26
        },
        {
          "date": "2021-05-21",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.0784,
          "close": 4155.86,
          "ma50": 4090.8
        }
      ]
    },
    {
      "name": "trigger_dayret_None_cooldown_6_include_ma50_False",
      "ok": false,
      "mismatch_count": 4,
      "distribution": {
        "ALLOW": 55,
        "SHOCK": 1,
        "RISK_OFF": 6
      },
      "mismatches": [
        {
          "date": "2021-05-10",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -1.0436,
          "close": 4188.43,
          "ma50": 4041.08
        },
        {
          "date": "2021-05-11",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.8674,
          "close": 4152.1,
          "ma50": 4046.08
        },
        {
          "date": "2021-05-20",
          "expected": "ALLOW",
          "actual": "RISK_OFF",
          "day_ret": 1.0555,
          "close": 4159.12,
          "ma50": 4086.47
        },
        {
          "date": "2021-05-21",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.0784,
          "close": 4155.86,
          "ma50": 4090.8
        }
      ]
    },
    {
      "name": "trigger_dayret_None_cooldown_8_include_ma50_False",
      "ok": false,
      "mismatch_count": 4,
      "distribution": {
        "ALLOW": 53,
        "SHOCK": 1,
        "RISK_OFF": 8
      },
      "mismatches": [
        {
          "date": "2021-05-10",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -1.0436,
          "close": 4188.43,
          "ma50": 4041.08
        },
        {
          "date": "2021-05-11",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.8674,
          "close": 4152.1,
          "ma50": 4046.08
        },
        {
          "date": "2021-05-20",
          "expected": "ALLOW",
          "actual": "RISK_OFF",
          "day_ret": 1.0555,
          "close": 4159.12,
          "ma50": 4086.47
        },
        {
          "date": "2021-05-24",
          "expected": "ALLOW",
          "actual": "RISK_OFF",
          "day_ret": 0.9911,
          "close": 4197.05,
          "ma50": 4095.88
        }
      ]
    },
    {
      "name": "trigger_dayret_-1.5_cooldown_4_include_ma50_False",
      "ok": false,
      "mismatch_count": 4,
      "distribution": {
        "ALLOW": 57,
        "SHOCK": 1,
        "RISK_OFF": 4
      },
      "mismatches": [
        {
          "date": "2021-05-10",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -1.0436,
          "close": 4188.43,
          "ma50": 4041.08
        },
        {
          "date": "2021-05-11",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.8674,
          "close": 4152.1,
          "ma50": 4046.08
        },
        {
          "date": "2021-05-19",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.2943,
          "close": 4115.68,
          "ma50": 4081.26
        },
        {
          "date": "2021-05-21",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.0784,
          "close": 4155.86,
          "ma50": 4090.8
        }
      ]
    },
    {
      "name": "trigger_dayret_-1.5_cooldown_6_include_ma50_False",
      "ok": false,
      "mismatch_count": 4,
      "distribution": {
        "ALLOW": 55,
        "SHOCK": 1,
        "RISK_OFF": 6
      },
      "mismatches": [
        {
          "date": "2021-05-10",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -1.0436,
          "close": 4188.43,
          "ma50": 4041.08
        },
        {
          "date": "2021-05-11",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.8674,
          "close": 4152.1,
          "ma50": 4046.08
        },
        {
          "date": "2021-05-20",
          "expected": "ALLOW",
          "actual": "RISK_OFF",
          "day_ret": 1.0555,
          "close": 4159.12,
          "ma50": 4086.47
        },
        {
          "date": "2021-05-21",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.0784,
          "close": 4155.86,
          "ma50": 4090.8
        }
      ]
    },
    {
      "name": "trigger_dayret_-1.5_cooldown_8_include_ma50_False",
      "ok": false,
      "mismatch_count": 4,
      "distribution": {
        "ALLOW": 53,
        "SHOCK": 1,
        "RISK_OFF": 8
      },
      "mismatches": [
        {
          "date": "2021-05-10",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -1.0436,
          "close": 4188.43,
          "ma50": 4041.08
        },
        {
          "date": "2021-05-11",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.8674,
          "close": 4152.1,
          "ma50": 4046.08
        },
        {
          "date": "2021-05-20",
          "expected": "ALLOW",
          "actual": "RISK_OFF",
          "day_ret": 1.0555,
          "close": 4159.12,
          "ma50": 4086.47
        },
        {
          "date": "2021-05-24",
          "expected": "ALLOW",
          "actual": "RISK_OFF",
          "day_ret": 0.9911,
          "close": 4197.05,
          "ma50": 4095.88
        }
      ]
    }
  ],
  "note": "These hypotheses are not accepted as source-of-truth. They only guide source inspection."
}
```

## Critical Source Clusters
```json
[
  {
    "start": 831,
    "end": 954,
    "line_count": 124,
    "rows": [
      {
        "line": 831,
        "text": "            return {\"mode\": \"UPTREND_RISK_ON\", \"max_positions\": 3, \"max_total_exposure_pct\": 100.0}"
      },
      {
        "line": 832,
        "text": "        if regime == \"SIDEWAYS\":"
      },
      {
        "line": 833,
        "text": "            return {\"mode\": \"SIDEWAYS_LIMITED\", \"max_positions\": 2, \"max_total_exposure_pct\": 33.3}"
      },
      {
        "line": 834,
        "text": "        if regime == \"DOWNTREND\":"
      },
      {
        "line": 835,
        "text": "            return {\"mode\": \"DOWNTREND_DEFENSIVE\", \"max_positions\": 1, \"max_total_exposure_pct\": 10.0}"
      },
      {
        "line": 836,
        "text": "        if regime == \"N/A\":"
      },
      {
        "line": 837,
        "text": "            return {\"mode\": \"N/A\", \"max_positions\": None, \"max_total_exposure_pct\": None}"
      },
      {
        "line": 838,
        "text": "        return {\"mode\": \"UNCLASSIFIED_DEFENSIVE\", \"max_positions\": 0, \"max_total_exposure_pct\": 0.0}"
      },
      {
        "line": 839,
        "text": ""
      },
      {
        "line": 840,
        "text": "    def _e1r_dominant_regime(weights: dict) -> str:"
      },
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
      },
      {
        "line": 858,
        "text": "    qualified_price_above_ma50 = bool(a.get(\"qualified_price_above_ma50\", True))"
      },
      {
        "line": 859,
        "text": "    qualified_ma50_slope_min  = float(a.get(\"qualified_ma50_slope_min\", 0.0))"
      },
      {
        "line": 860,
        "text": ""
      },
      {
        "line": 861,
        "text": "    fill_only_enabled    = bool(a.get(\"fill_only_enabled\", False))"
      },
      {
        "line": 862,
        "text": "    gate_use_slope       = bool(a.get(\"gate_use_slope\", True))"
      },
      {
        "line": 863,
        "text": "    gate_use_leadership  = bool(a.get(\"gate_use_leadership\", True))"
      },
      {
        "line": 864,
        "text": ""
      },
      {
        "line": 865,
        "text": "    # ── 辅助指数 Lookup（日期 → 价格）─────────────────────────"
      },
      {
        "line": 866,
        "text": "    # 用于 Gate v2 市场状态判断；缺失日期使用最近一个有效值"
      },
      {
        "line": 867,
        "text": "    def _build_lookup(dates_list, prices_list):"
      },
      {
        "line": 868,
        "text": "        \"\"\"建立 date_str → price 映射\"\"\""
      },
      {
        "line": 869,
        "text": "        m = {}"
      },
      {
        "line": 870,
        "text": "        if dates_list and prices_list:"
      },
      {
        "line": 871,
        "text": "            for d, p in zip(dates_list, prices_list):"
      },
      {
        "line": 872,
        "text": "                m[d] = p"
      },
      {
        "line": 873,
        "text": "        return m"
      },
      {
        "line": 874,
        "text": ""
      },
      {
        "line": 875,
        "text": "    ndx_lookup = _build_lookup(ndx_dates or [], ndx_prices or [])"
      },
      {
        "line": 876,
        "text": "    sox_lookup = _build_lookup(sox_dates or [], sox_prices or [])"
      },
      {
        "line": 877,
        "text": "    vix_lookup = _build_lookup(vix_dates or [], vix_prices or [])"
      },
      {
        "line": 878,
        "text": ""
      },
      {
        "line": 879,
        "text": "    def _get_price_on(lookup, date, fallback=None):"
      },
      {
        "line": 880,
        "text": "        \"\"\"获取 date 当天价格，缺失时返回 fallback\"\"\""
      },
      {
        "line": 881,
        "text": "        return lookup.get(date, fallback)"
      },
      {
        "line": 882,
        "text": ""
      },
      {
        "line": 883,
        "text": "    # SPX MA50 历史队列（用于 10日 slope 计算）"
      },
      {
        "line": 884,
        "text": "    from collections import deque"
      },
      {
        "line": 885,
        "text": "    spx_ma50_history = deque(maxlen=11)  # 存最近11个 MA50 值（今天+10天前）"
      },
      {
        "line": 886,
        "text": ""
      },
      {
        "line": 887,
        "text": "    if qualified_entry_enabled:"
      },
      {
        "line": 888,
        "text": "        logger.info(f\"  Qualified Pool: candidate_top_n={candidate_top_n} \""
      },
      {
        "line": 889,
        "text": "                    f\"RS>={qualified_rs_min} Mom>={qualified_momentum_min} \""
      },
      {
        "line": 890,
        "text": "                    f\"TH>={qualified_th_min} states={qualified_states} \""
      },
      {
        "line": 891,
        "text": "                    f\"price>MA50={qualified_price_above_ma50} slope>={qualified_ma50_slope_min}\")"
      },
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
      },
      {
        "line": 907,
        "text": "    relative_stop_enabled = bool(a.get(\"relative_stop_enabled\", False))"
      },
      {
        "line": 908,
        "text": "    relative_stop_underperform = float(a.get(\"relative_stop_underperform_pct\", -0.08))"
      },
      {
        "line": 909,
        "text": "    relative_stop_action = a.get(\"relative_stop_action\", \"REL_REDUCE\")"
      },
      {
        "line": 910,
        "text": "    relative_stop_once = bool(a.get(\"relative_stop_once_per_position\", True))"
      },
      {
        "line": 911,
        "text": "    market_gate_variant = ("
      },
      {
        "line": 912,
        "text": "        \"D1_NO_MARKET_GATE\" if not market_gate_enabled else"
      },
      {
        "line": 913,
        "text": "        \"D2_RISK_OFF_GATE\" if not market_shock_gate_enabled else"
      },
      {
        "line": 914,
        "text": "        \"D3_RISK_OFF_PLUS_SHOCK_GATE\""
      },
      {
        "line": 915,
        "text": "    )"
      },
      {
        "line": 916,
        "text": ""
      },
      {
        "line": 917,
        "text": "    if qualified_entry_enabled:"
      },
      {
        "line": 918,
        "text": "        logger.info(f\"  v{a.get('version','?')} | Strategy={strategy_variant} \""
      },
      {
        "line": 919,
        "text": "                    f\"| CandidateTopN={candidate_top_n} MaxPos={max_pos} EntryMode=QualifiedPool \""
      },
      {
        "line": 920,
        "text": "                    f\"BuySlot={buy_pct*100:.1f}% MaxSingle={max_pct*100:.1f}% \""
      },
      {
        "line": 921,
        "text": "                    f\"OneWay={one_way*100:.2f}%\")"
      },
      {
        "line": 922,
        "text": "    else:"
      },
      {
        "line": 923,
        "text": "        logger.info(f\"  v{a.get('version','?')} | Strategy={strategy_variant} \""
      },
      {
        "line": 924,
        "text": "                    f\"| EntryTopN={entry_top_n} MaxPos={max_pos} EntryMode=StrictTop3 \""
      },
      {
        "line": 925,
        "text": "                    f\"BuySlot={buy_pct*100:.1f}% MaxSingle={max_pct*100:.1f}% \""
      },
      {
        "line": 926,
        "text": "                    f\"OneWay={one_way*100:.2f}%\")"
      },
      {
        "line": 927,
        "text": "    logger.info(f\"  Market Gate Variant: {market_gate_variant}\")"
      },
      {
        "line": 928,
        "text": "    logger.info(f\"  Market Gate: enabled={market_gate_enabled} \""
      },
      {
        "line": 929,
        "text": "                f\"| RiskOff=SPX<MA50:{risk_off_below_spx_ma50} \""
      },
      {
        "line": 930,
        "text": "                f\"| Shock<={market_shock_daily_return*100:.1f}%:{market_shock_gate_enabled}\")"
      },
      {
        "line": 931,
        "text": "    logger.info(f\"  Entry filter: RS >= {entry_rs_min:.1f}; MinHold={min_holding_days}d; \""
      },
      {
        "line": 932,
        "text": "                f\"RelStop={'ON' if relative_stop_enabled else 'OFF'} \""
      },
      {
        "line": 933,
        "text": "                f\"({relative_stop_underperform*100:.1f}% vs SPX)\")"
      },
      {
        "line": 934,
        "text": "    logger.info(f\"  LS60 mode: {ls60_exit_mode} \""
      },
      {
        "line": 935,
        "text": "                f\"({'LS<60 → EXIT' if ls60_exit_mode == 'exit' else 'LS<60 → REDUCE'})\")"
      },
      {
        "line": 936,
        "text": "    logger.info(f\"  ── Param check: ls60={ls60_exit_mode} rs={entry_rs_min} \""
      },
      {
        "line": 937,
        "text": "                f\"top_n={entry_top_n} minhold={min_holding_days} \""
      },
      {
        "line": 938,
        "text": "                f\"relstop={relative_stop_enabled} gate={market_gate_enabled} ──\")"
      },
      {
        "line": 939,
        "text": "    if dynamic_exit_enabled:"
      },
      {
        "line": 940,
        "text": "        logger.info(f\"  Dynamic Exit v2: ON | Hard=Close<MA50+slope<0 | FULL_ON=needs structure | CAUTIOUS/CASH=LS<60 exits\")"
      },
      {
        "line": 941,
        "text": "    logger.info(f\"  Fixed TP: enabled={take_profit_enabled} \""
      },
      {
        "line": 942,
        "text": "                f\"(v1.6 default OFF; TP7-P rejected for this matrix)\")"
      },
      {
        "line": 943,
        "text": ""
      },
      {
        "line": 944,
        "text": "    # ── 修正1: SPX master calendar ────────────────────────"
      },
      {
        "line": 945,
        "text": "    # 时间轴以 SPX dates 为准，不受个股短数据影响"
      },
      {
        "line": 946,
        "text": "    master_dates = spx_dates"
      },
      {
        "line": 947,
        "text": "    n_days       = len(spx_prices)"
      },
      {
        "line": 948,
        "text": ""
      },
      {
        "line": 949,
        "text": "    logger.info(f\"  时间轴: {master_dates[0] if master_dates else '?'} → {master_dates[-1] if master_dates else '?'} ({n_days} bars)\")"
      },
      {
        "line": 950,
        "text": "    # 交易执行区间（不影响 warm-up 和指标计算，只控制交易时段）"
      },
      {
        "line": 951,
        "text": "    _trade_start = sim_start_date  # None = 从 min_history 后第一天"
      },
      {
        "line": 952,
        "text": "    _trade_end   = sim_end_date    # None = 到末尾"
      },
      {
        "line": 953,
        "text": "    _default_start = master_dates[min_history] if len(master_dates) > min_history else (master_dates[0] if master_dates else \"?\")"
      },
      {
        "line": 954,
        "text": "    _default_end   = master_dates[-2] if len(master_dates) >= 2 else (master_dates[-1] if master_dates else \"?\")"
      }
    ]
  },
  {
    "start": 1021,
    "end": 1054,
    "line_count": 34,
    "rows": [
      {
        "line": 1021,
        "text": ""
      },
      {
        "line": 1022,
        "text": "    # 修正3: skipped_orders_by_reason"
      },
      {
        "line": 1023,
        "text": "    skip_reasons = {"
      },
      {
        "line": 1024,
        "text": "        \"max_positions_reached\":    0,"
      },
      {
        "line": 1025,
        "text": "        \"cash_insufficient\":        0,"
      },
      {
        "line": 1026,
        "text": "        \"already_holding\":          0,"
      },
      {
        "line": 1027,
        "text": "        \"max_single_size_reached\":  0,"
      },
      {
        "line": 1028,
        "text": "        \"no_t1_price\":              0,"
      },
      {
        "line": 1029,
        "text": "        \"invalid_execution_price\":  0,"
      },
      {
        "line": 1030,
        "text": "        \"size_at_minimum\":          0,"
      },
      {
        "line": 1031,
        "text": "        \"not_holding\":              0,"
      },
      {
        "line": 1032,
        "text": "        \"not_in_entry_top_n\":               0,   # legacy: 旧 Strict Top3 模式"
      },
      {
        "line": 1033,
        "text": "        \"not_in_qualified_candidate_pool\":  0,   # qualified: 不在候选池"
      },
      {
        "line": 1034,
        "text": "        \"not_qualified_entry\":              0,   # qualified: 未通过资格过滤"
      },
      {
        "line": 1035,
        "text": "        \"qualified_candidate_generated\":    0,   # qualified: 候选池 BUY 已生成"
      },
      {
        "line": 1036,
        "text": ""
      },
      {
        "line": 1037,
        "text": "        \"market_risk_off_block\":    0,"
      },
      {
        "line": 1038,
        "text": "        \"market_shock_block\":       0,"
      },
      {
        "line": 1039,
        "text": "        \"add_blocked_after_tp\":     0,"
      },
      {
        "line": 1040,
        "text": "        \"entry_rs_below_threshold\":        0,"
      },
      {
        "line": 1041,
        "text": "        \"min_hold_block\":                  0,"
      },
      {
        "line": 1042,
        "text": "        \"dynamic_exit_warning\":            0,  # E2: LS<60 但动态确认为 HOLD"
      },
      {
        "line": 1043,
        "text": "        \"dynamic_hard_exit_triggered\":     0,  # E2: 硬退出触发次数"
      },
      {
        "line": 1044,
        "text": "        \"dynamic_soft_exit_confirmed\":     0,  # E2: 软退出确认次数"
      },
      {
        "line": 1045,
        "text": "        \"ls60_reduce_already_triggered\":   0,"
      },
      {
        "line": 1046,
        "text": "        \"action_reason_buy_add_mismatch\":  0,   # BUY/ADD 不一致（记录，不中断）"
      },
      {
        "line": 1047,
        "text": "        \"fill_only_no_empty_slot\":         0,   # fill_only 模式：无空仓位，跳过 BUY"
      },
      {
        "line": 1048,
        "text": "        \"e1r_legacy_buy_blocked\":          0,   # E1-R execution: legacy BUY suppressed"
      },
      {
        "line": 1049,
        "text": "        \"e1r_no_capacity\":                 0,   # E1-R execution: no available slot"
      },
      {
        "line": 1050,
        "text": "        \"e1r_candidate_buy_generated\":     0,   # E1-R execution: candidate BUY generated"
      },
      {
        "line": 1051,
        "text": "        \"e1r_emerging_to_confirmed_add\":   0,   # E1-R execution: upgrade ADD generated"
      },
      {
        "line": 1052,
        "text": "    }"
      },
      {
        "line": 1053,
        "text": "    orders_executed = 0"
      },
      {
        "line": 1054,
        "text": ""
      }
    ]
  },
  {
    "start": 1056,
    "end": 1091,
    "line_count": 36,
    "rows": [
      {
        "line": 1056,
        "text": "    portfolio_action_dist = {\"HOLD\": 0, \"ADD\": 0, \"REDUCE\": 0, \"REL_REDUCE\": 0, \"EXIT\": 0, \"TP_REDUCE\": 0}"
      },
      {
        "line": 1057,
        "text": "    # 真实成交退出的原因分布"
      },
      {
        "line": 1058,
        "text": "    executed_exit_reason_dist: dict[str, int] = {}"
      },
      {
        "line": 1059,
        "text": "    # 真实成交减仓的原因分布"
      },
      {
        "line": 1060,
        "text": "    executed_reduce_reason_dist: dict[str, int] = {}"
      },
      {
        "line": 1061,
        "text": "    # 生成过的 EXIT/REDUCE pending signal 原因（含未成交）"
      },
      {
        "line": 1062,
        "text": "    pending_signal_reason_dist: dict[str, int] = {}"
      },
      {
        "line": 1063,
        "text": ""
      },
      {
        "line": 1064,
        "text": "    take_profit_stats = {"
      },
      {
        "line": 1065,
        "text": "        \"signals\": 0,"
      },
      {
        "line": 1066,
        "text": "        \"executed\": 0,"
      },
      {
        "line": 1067,
        "text": "    }"
      },
      {
        "line": 1068,
        "text": "    relative_stop_stats = {"
      },
      {
        "line": 1069,
        "text": "        \"signals\": 0,"
      },
      {
        "line": 1070,
        "text": "        \"executed\": 0,"
      },
      {
        "line": 1071,
        "text": "    }"
      },
      {
        "line": 1072,
        "text": "    market_gate_days = {"
      },
      {
        "line": 1073,
        "text": "        \"entry_allowed\": 0,"
      },
      {
        "line": 1074,
        "text": "        \"risk_off\": 0,"
      },
      {
        "line": 1075,
        "text": "        \"market_shock\": 0,"
      },
      {
        "line": 1076,
        "text": "        \"blocked_total\": 0,"
      },
      {
        "line": 1077,
        "text": "    }"
      },
      {
        "line": 1078,
        "text": ""
      },
      {
        "line": 1079,
        "text": "    equity_curve:  list[float] = []"
      },
      {
        "line": 1080,
        "text": "    spx_curve:     list[float] = []"
      },
      {
        "line": 1081,
        "text": "    daily_records: list[dict]  = []"
      },
      {
        "line": 1082,
        "text": "    # Continuous observer-only daily equity records."
      },
      {
        "line": 1083,
        "text": "    # Read-only telemetry for regime/equity attribution."
      },
      {
        "line": 1084,
        "text": "    daily_equity_records: list[dict] = []"
      },
      {
        "line": 1085,
        "text": "    daily_equity_peak = init_cap"
      },
      {
        "line": 1086,
        "text": "    sim_end_liquidation_record = None"
      },
      {
        "line": 1087,
        "text": "    # E1-R Phase 3A candidate tagging only."
      },
      {
        "line": 1088,
        "text": "    # These records are diagnostics; they must not affect orders or execution."
      },
      {
        "line": 1089,
        "text": "    e1r_candidate_records: list[dict] = []"
      },
      {
        "line": 1090,
        "text": "    spx_entry = 0.0  # 在日循环中遇到第一个 sim 日时设置，保证与 Period 区间一致"
      },
      {
        "line": 1091,
        "text": ""
      }
    ]
  },
  {
    "start": 1370,
    "end": 1547,
    "line_count": 178,
    "rows": [
      {
        "line": 1370,
        "text": "        equity_curve.append(total_equity)"
      },
      {
        "line": 1371,
        "text": "        # 第一个 sim 日时锁定 SPX 起点（保证每个 Period 独立基准）"
      },
      {
        "line": 1372,
        "text": "        if spx_entry <= 0:"
      },
      {
        "line": 1373,
        "text": "            spx_entry = spx_prices[t] if spx_prices[t] > 0 else 1.0"
      },
      {
        "line": 1374,
        "text": "        spx_curve.append(spx_prices[t] / spx_entry if spx_entry > 0 else 1.0)"
      },
      {
        "line": 1375,
        "text": ""
      },
      {
        "line": 1376,
        "text": "        # ════════════════════════════════════════════════"
      },
      {
        "line": 1377,
        "text": "        # STEP 3: 生成 T 日信号 → pending_orders for T+1"
      },
      {
        "line": 1378,
        "text": "        # Strategy v1.6:"
      },
      {
        "line": 1379,
        "text": "        #   Top 3 只限制“新 BUY 候选池”"
      },
      {
        "line": 1380,
        "text": "        #   可选：提高入场 RS 阈值到 95"
      },
      {
        "line": 1381,
        "text": "        #   可选：普通 REDUCE/EXIT 最短持仓 5 天"
      },
      {
        "line": 1382,
        "text": "        #   可选：相对 SPX 跑输 8% 时减仓 50%"
      },
      {
        "line": 1383,
        "text": "        #   不使用固定止盈；不因跌出 Top3 卖出"
      },
      {
        "line": 1384,
        "text": "        # ════════════════════════════════════════════════"
      },
      {
        "line": 1385,
        "text": "        spx_close_t = spx_prices[t]"
      },
      {
        "line": 1386,
        "text": "        spx_ma50_t = sum(spx_prices[t-49:t+1]) / 50 if t >= 49 else spx_close_t"
      },
      {
        "line": 1387,
        "text": "        spx_day_return = ("
      },
      {
        "line": 1388,
        "text": "            (spx_prices[t] - spx_prices[t-1]) / spx_prices[t-1]"
      },
      {
        "line": 1389,
        "text": "            if t > 0 and spx_prices[t-1] > 0 else 0.0"
      },
      {
        "line": 1390,
        "text": "        )"
      },
      {
        "line": 1391,
        "text": ""
      },
      {
        "line": 1392,
        "text": "        # ── Gate v2：三档市场状态 ────────────────────────────────"
      },
      {
        "line": 1393,
        "text": "        if not market_gate_enabled:"
      },
      {
        "line": 1394,
        "text": "            # Gate 关闭：完全跳过，不执行任何 Gate v2 计算"
      },
      {
        "line": 1395,
        "text": "            market_state     = \"FULL_ON\""
      },
      {
        "line": 1396,
        "text": "            entry_capacity   = max_pos"
      },
      {
        "line": 1397,
        "text": "            market_risk_off  = False"
      },
      {
        "line": 1398,
        "text": "            market_shock     = False"
      },
      {
        "line": 1399,
        "text": "            market_entry_allowed = True"
      },
      {
        "line": 1400,
        "text": "            market_gate_days[\"entry_allowed\"] += 1"
      },
      {
        "line": 1401,
        "text": "        else:"
      },
      {
        "line": 1402,
        "text": "            # ── MA50 slope（10日变化率，使用完整历史索引，无 warm-up 问题）"
      },
      {
        "line": 1403,
        "text": "            if t >= 59:  # t>=49（MA50）+ 10（slope 回溯）"
      },
      {
        "line": 1404,
        "text": "                spx_ma50_t10 = sum(spx_prices[t-59:t-9]) / 50"
      },
      {
        "line": 1405,
        "text": "                spx_ma50_slope = (spx_ma50_t / spx_ma50_t10) - 1.0 if spx_ma50_t10 > 0 else 0.0"
      },
      {
        "line": 1406,
        "text": "            else:"
      },
      {
        "line": 1407,
        "text": "                spx_ma50_slope = 0.0"
      },
      {
        "line": 1408,
        "text": ""
      },
      {
        "line": 1409,
        "text": "            # ── NDX/SOX/VIX 当日价格"
      },
      {
        "line": 1410,
        "text": "            _ndx_last = None"
      },
      {
        "line": 1411,
        "text": "            _sox_last = None"
      },
      {
        "line": 1412,
        "text": "            _vix_last = None"
      },
      {
        "line": 1413,
        "text": "            _ndx_ma50 = None"
      },
      {
        "line": 1414,
        "text": "            _sox_ma50 = None"
      },
      {
        "line": 1415,
        "text": ""
      },
      {
        "line": 1416,
        "text": "            if ndx_lookup:"
      },
      {
        "line": 1417,
        "text": "                _ndx_last = _get_price_on(ndx_lookup, date_t)"
      },
      {
        "line": 1418,
        "text": "                if ndx_prices and len(ndx_prices) >= 50:"
      },
      {
        "line": 1419,
        "text": "                    _ndx_idx = next((i for i, d in enumerate(ndx_dates or []) if d == date_t), None)"
      },
      {
        "line": 1420,
        "text": "                    if _ndx_idx is not None and _ndx_idx >= 49:"
      },
      {
        "line": 1421,
        "text": "                        _ndx_ma50 = sum(ndx_prices[_ndx_idx-49:_ndx_idx+1]) / 50"
      },
      {
        "line": 1422,
        "text": ""
      },
      {
        "line": 1423,
        "text": "            if sox_lookup:"
      },
      {
        "line": 1424,
        "text": "                _sox_last = _get_price_on(sox_lookup, date_t)"
      },
      {
        "line": 1425,
        "text": "                if sox_prices and len(sox_prices) >= 50:"
      },
      {
        "line": 1426,
        "text": "                    _sox_idx = next((i for i, d in enumerate(sox_dates or []) if d == date_t), None)"
      },
      {
        "line": 1427,
        "text": "                    if _sox_idx is not None and _sox_idx >= 49:"
      },
      {
        "line": 1428,
        "text": "                        _sox_ma50 = sum(sox_prices[_sox_idx-49:_sox_idx+1]) / 50"
      },
      {
        "line": 1429,
        "text": ""
      },
      {
        "line": 1430,
        "text": "            if vix_lookup:"
      },
      {
        "line": 1431,
        "text": "                _vix_last = _get_price_on(vix_lookup, date_t)"
      },
      {
        "line": 1432,
        "text": ""
      },
      {
        "line": 1433,
        "text": "            # ── Leadership 计算"
      },
      {
        "line": 1434,
        "text": "            _spx_above = spx_close_t > spx_ma50_t"
      },
      {
        "line": 1435,
        "text": "            _ndx_above = (_ndx_last is not None and _ndx_ma50 is not None"
      },
      {
        "line": 1436,
        "text": "                          and _ndx_last > _ndx_ma50) if ndx_lookup else None"
      },
      {
        "line": 1437,
        "text": "            _sox_above = (_sox_last is not None and _sox_ma50 is not None"
      },
      {
        "line": 1438,
        "text": "                          and _sox_last > _sox_ma50) if sox_lookup else None"
      },
      {
        "line": 1439,
        "text": ""
      },
      {
        "line": 1440,
        "text": "            _n_indices = 1 + (1 if ndx_lookup else 0) + (1 if sox_lookup else 0)"
      },
      {
        "line": 1441,
        "text": "            _leadership_count = sum(["
      },
      {
        "line": 1442,
        "text": "                1 if _spx_above else 0,"
      },
      {
        "line": 1443,
        "text": "                1 if (_ndx_above is True) else 0,"
      },
      {
        "line": 1444,
        "text": "                1 if (_sox_above is True) else 0,"
      },
      {
        "line": 1445,
        "text": "            ])"
      },
      {
        "line": 1446,
        "text": "            _leadership_ratio = _leadership_count / _n_indices if _n_indices > 0 else 1.0"
      },
      {
        "line": 1447,
        "text": "            # shock/VIX 受开关控制，不泄漏到未启用的 variant"
      },
      {
        "line": 1448,
        "text": "            _shock_active = ("
      },
      {
        "line": 1449,
        "text": "                market_shock_gate_enabled"
      },
      {
        "line": 1450,
        "text": "                and spx_day_return <= market_shock_daily_return"
      },
      {
        "line": 1451,
        "text": "            )"
      },
      {
        "line": 1452,
        "text": "            _vix_active = ("
      },
      {
        "line": 1453,
        "text": "                vix_lookup is not None and len(vix_lookup) > 0"
      },
      {
        "line": 1454,
        "text": "                and (_vix_last or 0) >= 30"
      },
      {
        "line": 1455,
        "text": "                # VIX 当前冻结禁用（所有 Gate v2.1 variant 均不传 VIX 数据）"
      },
      {
        "line": 1456,
        "text": "            )"
      },
      {
        "line": 1457,
        "text": ""
      },
      {
        "line": 1458,
        "text": "            # ── 三档状态判定（条件受开关控制）"
      },
      {
        "line": 1459,
        "text": "            _slope_ok          = (spx_ma50_slope >= 0) if gate_use_slope else True"
      },
      {
        "line": 1460,
        "text": "            _leadership_strong = (_leadership_ratio >= 1.0) if gate_use_leadership else True"
      },
      {
        "line": 1461,
        "text": ""
      },
      {
        "line": 1462,
        "text": "            _cash_mode = ("
      },
      {
        "line": 1463,
        "text": "                _vix_active"
      },
      {
        "line": 1464,
        "text": "                or _shock_active"
      },
      {
        "line": 1465,
        "text": "                or (gate_use_leadership and _leadership_ratio < 2/3)"
      },
      {
        "line": 1466,
        "text": "                or (gate_use_slope and spx_ma50_slope < 0)"
      },
      {
        "line": 1467,
        "text": "            )"
      },
      {
        "line": 1468,
        "text": "            if _cash_mode:"
      },
      {
        "line": 1469,
        "text": "                market_state   = \"CASH_MODE\""
      },
      {
        "line": 1470,
        "text": "                entry_capacity = 0"
      },
      {
        "line": 1471,
        "text": "            elif ("
      },
      {
        "line": 1472,
        "text": "                _spx_above"
      },
      {
        "line": 1473,
        "text": "                and _slope_ok"
      },
      {
        "line": 1474,
        "text": "                and _leadership_strong"
      },
      {
        "line": 1475,
        "text": "                and not _shock_active"
      },
      {
        "line": 1476,
        "text": "            ):"
      },
      {
        "line": 1477,
        "text": "                market_state   = \"FULL_ON\""
      },
      {
        "line": 1478,
        "text": "                entry_capacity = max_pos"
      },
      {
        "line": 1479,
        "text": "            else:"
      },
      {
        "line": 1480,
        "text": "                market_state   = \"CAUTIOUS_ON\""
      },
      {
        "line": 1481,
        "text": "                entry_capacity = min(max_pos, 2)"
      },
      {
        "line": 1482,
        "text": ""
      },
      {
        "line": 1483,
        "text": "            market_risk_off  = (market_state == \"CASH_MODE\") and not _shock_active"
      },
      {
        "line": 1484,
        "text": "            market_shock     = _shock_active"
      },
      {
        "line": 1485,
        "text": "            market_entry_allowed = entry_capacity > 0"
      },
      {
        "line": 1486,
        "text": ""
      },
      {
        "line": 1487,
        "text": "            if market_risk_off:"
      },
      {
        "line": 1488,
        "text": "                market_gate_days[\"risk_off\"] += 1"
      },
      {
        "line": 1489,
        "text": "            if market_shock:"
      },
      {
        "line": 1490,
        "text": "                market_gate_days[\"market_shock\"] += 1"
      },
      {
        "line": 1491,
        "text": "            if market_entry_allowed:"
      },
      {
        "line": 1492,
        "text": "                market_gate_days[\"entry_allowed\"] += 1"
      },
      {
        "line": 1493,
        "text": "            else:"
      },
      {
        "line": 1494,
        "text": "                market_gate_days[\"blocked_total\"] += 1"
      },
      {
        "line": 1495,
        "text": ""
      },
      {
        "line": 1496,
        "text": "        # ── Continuous daily equity observer record ─────────────────────"
      },
      {
        "line": 1497,
        "text": "        _prev_equity = ("
      },
      {
        "line": 1498,
        "text": "            daily_equity_records[-1][\"total_equity\"]"
      },
      {
        "line": 1499,
        "text": "            if daily_equity_records else init_cap"
      },
      {
        "line": 1500,
        "text": "        )"
      },
      {
        "line": 1501,
        "text": "        _daily_return_pct = ("
      },
      {
        "line": 1502,
        "text": "            (total_equity / _prev_equity - 1) * 100"
      },
      {
        "line": 1503,
        "text": "            if _prev_equity and _prev_equity > 0 else 0.0"
      },
      {
        "line": 1504,
        "text": "        )"
      },
      {
        "line": 1505,
        "text": "        daily_equity_peak = max(daily_equity_peak, total_equity)"
      },
      {
        "line": 1506,
        "text": "        _drawdown_pct = ("
      },
      {
        "line": 1507,
        "text": "            (daily_equity_peak - total_equity) / daily_equity_peak * 100"
      },
      {
        "line": 1508,
        "text": "            if daily_equity_peak and daily_equity_peak > 0 else 0.0"
      },
      {
        "line": 1509,
        "text": "        )"
      },
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
      },
      {
        "line": 1513,
        "text": "        )"
      },
      {
        "line": 1514,
        "text": ""
      },
      {
        "line": 1515,
        "text": "        daily_equity_records.append({"
      },
      {
        "line": 1516,
        "text": "            \"date\": date_t,"
      },
      {
        "line": 1517,
        "text": "            \"cash\": round(cash, 2),"
      },
      {
        "line": 1518,
        "text": "            \"positions_value\": round(position_value, 2),"
      },
      {
        "line": 1519,
        "text": "            \"total_equity\": round(total_equity, 2),"
      },
      {
        "line": 1520,
        "text": "            \"daily_return_pct\": round(_daily_return_pct, 4),"
      },
      {
        "line": 1521,
        "text": "            \"drawdown_pct\": round(_drawdown_pct, 4),"
      },
      {
        "line": 1522,
        "text": "            \"exposure_pct\": round(position_value / total_equity * 100, 2) if total_equity > 0 else 0.0,"
      },
      {
        "line": 1523,
        "text": "            \"open_positions_count\": len(holdings),"
      },
      {
        "line": 1524,
        "text": "            \"pending_orders_count\": len(pending_orders),"
      },
      {
        "line": 1525,
        "text": "            \"market_gate_state\": _gate_state,"
      },
      {
        "line": 1526,
        "text": "            \"spx_regime\": _e1r_regime_on(date_t) if e1r_regime_wiring_enabled else None,"
      },
      {
        "line": 1527,
        "text": "            \"e1r_active_mode\": _e1r_mode_for_regime(_e1r_regime_on(date_t)) if e1r_regime_wiring_enabled else None,"
      },
      {
        "line": 1528,
        "text": "            \"risk_budget_mode\": _e1r_risk_budget_for_regime(_e1r_regime_on(date_t))[\"mode\"] if e1r_regime_wiring_enabled else None,"
      },
      {
        "line": 1529,
        "text": "            \"risk_budget\": _e1r_risk_budget_for_regime(_e1r_regime_on(date_t)) if e1r_regime_wiring_enabled else None,"
      },
      {
        "line": 1530,
        "text": "            \"spx_close\": round(spx_close_t, 2),"
      },
      {
        "line": 1531,
        "text": "            \"spx_ma50\": round(spx_ma50_t, 2),"
      },
      {
        "line": 1532,
        "text": "            \"spx_day_return_pct\": round(spx_day_return * 100, 4),"
      },
      {
        "line": 1533,
        "text": "            \"event\": \"EOD_MARK_TO_MARKET\","
      },
      {
        "line": 1534,
        "text": "        })"
      },
      {
        "line": 1535,
        "text": ""
      },
      {
        "line": 1536,
        "text": "        all_ret60 = []"
      },
      {
        "line": 1537,
        "text": "        all_ret60_prev20 = []"
      },
      {
        "line": 1538,
        "text": "        for s in symbols:"
      },
      {
        "line": 1539,
        "text": "            p_s = get_close_series_by_date(s, date_t)"
      },
      {
        "line": 1540,
        "text": "            if len(p_s) > 60:"
      },
      {
        "line": 1541,
        "text": "                r = period_return(p_s, 60)"
      },
      {
        "line": 1542,
        "text": "                if r is not None:"
      },
      {
        "line": 1543,
        "text": "                    all_ret60.append(r)"
      },
      {
        "line": 1544,
        "text": "            # E1-R Phase 3A: previous RS reference for Emerging Leader acceleration."
      },
      {
        "line": 1545,
        "text": "            # Uses data up to T-20 only; diagnostic-only, no execution impact."
      },
      {
        "line": 1546,
        "text": "            if e1r_shell_mode and len(p_s) > 80:"
      },
      {
        "line": 1547,
        "text": "                r_prev = period_return(p_s[:-20], 60)"
      }
    ]
  },
  {
    "start": 1804,
    "end": 1850,
    "line_count": 47,
    "rows": [
      {
        "line": 1804,
        "text": "                continue"
      },
      {
        "line": 1805,
        "text": ""
      },
      {
        "line": 1806,
        "text": "            if qualified_entry_enabled:"
      },
      {
        "line": 1807,
        "text": "                # Qualified Pool 模式：接管新开仓权限"
      },
      {
        "line": 1808,
        "text": "                # 不使用 trade_action()==\"BUY\"，由候选池资格决定是否可开仓"
      },
      {
        "line": 1809,
        "text": "                if sym in holdings:"
      },
      {
        "line": 1810,
        "text": "                    # 已持仓：BUY 信号在 Qualified 模式下转为 ADD，由下方 position mgmt 处理"
      },
      {
        "line": 1811,
        "text": "                    if action == \"BUY\":"
      },
      {
        "line": 1812,
        "text": "                        action = \"ADD\""
      },
      {
        "line": 1813,
        "text": "                elif sym in top_entry_symbols:"
      },
      {
        "line": 1814,
        "text": "                    # sym 在 Qualified Pool 候选里"
      },
      {
        "line": 1815,
        "text": "                    # Fill-Only 检查：如果开启，只在有空仓位时才允许买入"
      },
      {
        "line": 1816,
        "text": "                    if fill_only_enabled and len(holdings) >= entry_capacity:"
      },
      {
        "line": 1817,
        "text": "                        skip_reasons[\"fill_only_no_empty_slot\"] += 1"
      },
      {
        "line": 1818,
        "text": "                        continue"
      },
      {
        "line": 1819,
        "text": "                    # → 允许开仓（Gate 启用时才在 STEP 3 检查容量）"
      },
      {
        "line": 1820,
        "text": "                    if market_gate_enabled and len(holdings) >= entry_capacity:"
      },
      {
        "line": 1821,
        "text": "                        skip_reasons[\"gate_capacity_block\"] = skip_reasons.get(\"gate_capacity_block\", 0) + 1"
      },
      {
        "line": 1822,
        "text": "                        continue"
      },
      {
        "line": 1823,
        "text": "                    if not market_entry_allowed:"
      },
      {
        "line": 1824,
        "text": "                        reason = \"market_shock_block\" if market_shock else \"market_risk_off_block\""
      },
      {
        "line": 1825,
        "text": "                        skip_reasons[reason] += 1"
      },
      {
        "line": 1826,
        "text": "                        continue"
      },
      {
        "line": 1827,
        "text": "                    qual_reasons = ["
      },
      {
        "line": 1828,
        "text": "                        \"qualified_pool_entry\","
      },
      {
        "line": 1829,
        "text": "                        f\"rs_above_{qualified_rs_min}\","
      },
      {
        "line": 1830,
        "text": "                        f\"mom_above_{qualified_momentum_min}\","
      },
      {
        "line": 1831,
        "text": "                        f\"th_above_{qualified_th_min}\","
      },
      {
        "line": 1832,
        "text": "                        \"trend_state_expansion\","
      },
      {
        "line": 1833,
        "text": "                        \"price_above_ma50\","
      },
      {
        "line": 1834,
        "text": "                        \"ma50_slope_non_negative\","
      },
      {
        "line": 1835,
        "text": "                    ]"
      },
      {
        "line": 1836,
        "text": "                    buy_orders.append({"
      },
      {
        "line": 1837,
        "text": "                        \"sym\":            sym,"
      },
      {
        "line": 1838,
        "text": "                        \"action\":         \"BUY\",    # 强制 BUY，不依赖 trade_action()"
      },
      {
        "line": 1839,
        "text": "                        \"signal_date\":    date_t,"
      },
      {
        "line": 1840,
        "text": "                        \"ls\":             ls,"
      },
      {
        "line": 1841,
        "text": "                        \"close_t\":        close_t,"
      },
      {
        "line": 1842,
        "text": "                        \"entry_rank\":     top_entry_rank.get(sym),"
      },
      {
        "line": 1843,
        "text": "                        \"strategy\":       strategy_variant,"
      },
      {
        "line": 1844,
        "text": "                        \"entry_mode\":     \"qualified_pool\","
      },
      {
        "line": 1845,
        "text": "                        \"primary_reason\": \"qualified_pool_entry\","
      },
      {
        "line": 1846,
        "text": "                        \"reasons\":        qual_reasons,"
      },
      {
        "line": 1847,
        "text": "                        \"candidate_top_n\": candidate_top_n,"
      },
      {
        "line": 1848,
        "text": "                    })"
      },
      {
        "line": 1849,
        "text": "                    qp_diag[\"buy_orders_generated\"] += 1"
      },
      {
        "line": 1850,
        "text": "                    skip_reasons[\"qualified_candidate_generated\"] += 1"
      }
    ]
  },
  {
    "start": 1856,
    "end": 2013,
    "line_count": 158,
    "rows": [
      {
        "line": 1856,
        "text": "            else:"
      },
      {
        "line": 1857,
        "text": "                # 旧模式：trade_action()==\"BUY\" + Strict TopN"
      },
      {
        "line": 1858,
        "text": "                if action == \"BUY\":"
      },
      {
        "line": 1859,
        "text": "                    if e1r_uptrend_execution_enabled:"
      },
      {
        "line": 1860,
        "text": "                        skip_reasons[\"e1r_legacy_buy_blocked\"] += 1"
      },
      {
        "line": 1861,
        "text": "                        continue"
      },
      {
        "line": 1862,
        "text": "                    if sym in holdings:"
      },
      {
        "line": 1863,
        "text": "                        continue"
      },
      {
        "line": 1864,
        "text": "                    if sig.get(\"rs_score\", 0.0) < entry_rs_min:"
      },
      {
        "line": 1865,
        "text": "                        skip_reasons[\"entry_rs_below_threshold\"] += 1"
      },
      {
        "line": 1866,
        "text": "                        continue"
      },
      {
        "line": 1867,
        "text": "                    if sym not in top_entry_symbols:"
      },
      {
        "line": 1868,
        "text": "                        skip_reasons[\"not_in_entry_top_n\"] += 1"
      },
      {
        "line": 1869,
        "text": "                        continue"
      },
      {
        "line": 1870,
        "text": "                    # STEP 3 容量检查：只在 Gate 启用时才在信号生成层拦截"
      },
      {
        "line": 1871,
        "text": "                    # Gate OFF 时依赖 STEP 1 执行层的 max_positions_reached 检查"
      },
      {
        "line": 1872,
        "text": "                    if market_gate_enabled and len(holdings) >= entry_capacity:"
      },
      {
        "line": 1873,
        "text": "                        skip_reasons[\"gate_capacity_block\"] = skip_reasons.get(\"gate_capacity_block\", 0) + 1"
      },
      {
        "line": 1874,
        "text": "                        continue"
      },
      {
        "line": 1875,
        "text": "                    if not market_entry_allowed:"
      },
      {
        "line": 1876,
        "text": "                        reason = \"market_shock_block\" if market_shock else \"market_risk_off_block\""
      },
      {
        "line": 1877,
        "text": "                        skip_reasons[reason] += 1"
      },
      {
        "line": 1878,
        "text": "                        continue"
      },
      {
        "line": 1879,
        "text": "                    buy_orders.append({"
      },
      {
        "line": 1880,
        "text": "                        \"sym\":            sym,"
      },
      {
        "line": 1881,
        "text": "                        \"action\":         \"BUY\","
      },
      {
        "line": 1882,
        "text": "                        \"signal_date\":    date_t,"
      },
      {
        "line": 1883,
        "text": "                        \"ls\":             ls,"
      },
      {
        "line": 1884,
        "text": "                        \"close_t\":        close_t,"
      },
      {
        "line": 1885,
        "text": "                        \"entry_rank\":     top_entry_rank.get(sym),"
      },
      {
        "line": 1886,
        "text": "                        \"strategy\":       strategy_variant,"
      },
      {
        "line": 1887,
        "text": "                        \"entry_mode\":     \"legacy_trade_action\","
      },
      {
        "line": 1888,
        "text": "                        \"primary_reason\": \"all_entry_conditions_met\","
      },
      {
        "line": 1889,
        "text": "                        \"reasons\":        [\"all_entry_conditions_met\"],"
      },
      {
        "line": 1890,
        "text": "                    })"
      },
      {
        "line": 1891,
        "text": "                    continue"
      },
      {
        "line": 1892,
        "text": ""
      },
      {
        "line": 1893,
        "text": "            # 已持仓股票的管理：ADD / REDUCE / EXIT 与 rank 无关"
      },
      {
        "line": 1894,
        "text": "            if action in (\"ADD\", \"REDUCE\", \"EXIT\"):"
      },
      {
        "line": 1895,
        "text": "                if sym not in holdings:"
      },
      {
        "line": 1896,
        "text": "                    continue"
      },
      {
        "line": 1897,
        "text": "                # ── 退出层：MinHold（E1）或 Dynamic Exit（E2）──────────"
      },
      {
        "line": 1898,
        "text": "                if action in (\"REDUCE\", \"EXIT\"):"
      },
      {
        "line": 1899,
        "text": "                    h = holdings[sym]"
      },
      {
        "line": 1900,
        "text": "                    holding_days_so_far = sum("
      },
      {
        "line": 1901,
        "text": "                        1 for d in master_dates"
      },
      {
        "line": 1902,
        "text": "                        if h.get(\"entry_date\", date_t) <= d <= date_t"
      },
      {
        "line": 1903,
        "text": "                    )"
      },
      {
        "line": 1904,
        "text": "                    stock_ma50  = sig.get(\"ma50\",       close_t)"
      },
      {
        "line": 1905,
        "text": "                    stock_slope = sig.get(\"ma50_slope\",  0.0)"
      },
      {
        "line": 1906,
        "text": "                    price_below_ma50   = close_t < stock_ma50"
      },
      {
        "line": 1907,
        "text": "                    slope_negative     = stock_slope < 0"
      },
      {
        "line": 1908,
        "text": ""
      },
      {
        "line": 1909,
        "text": "                    if dynamic_exit_enabled:"
      },
      {
        "line": 1910,
        "text": "                        # ── E2 Dynamic Exit Confirmation v2 ──────────────"
      },
      {
        "line": 1911,
        "text": "                        # 硬退出：Close<MA50 AND slope<0，不受市场状态影响"
      },
      {
        "line": 1912,
        "text": "                        hard_exit = price_below_ma50 and slope_negative"
      },
      {
        "line": 1913,
        "text": "                        if hard_exit:"
      },
      {
        "line": 1914,
        "text": "                            action = \"EXIT\""
      },
      {
        "line": 1915,
        "text": "                            h[\"exit_type\"] = \"HARD_EXIT\""
      },
      {
        "line": 1916,
        "text": "                            skip_reasons[\"dynamic_hard_exit_triggered\"] = ("
      },
      {
        "line": 1917,
        "text": "                                skip_reasons.get(\"dynamic_hard_exit_triggered\", 0) + 1)"
      },
      {
        "line": 1918,
        "text": "                        else:"
      },
      {
        "line": 1919,
        "text": "                            ls_below_60 = ls < 60"
      },
      {
        "line": 1920,
        "text": "                            if market_state == \"FULL_ON\":"
      },
      {
        "line": 1921,
        "text": "                                # FULL_ON：LS<60 还需一项价格结构证据才退出"
      },
      {
        "line": 1922,
        "text": "                                if ls_below_60 and not (price_below_ma50 or slope_negative):"
      },
      {
        "line": 1923,
        "text": "                                    # EXIT_WARNING：记录预警，继续持有"
      },
      {
        "line": 1924,
        "text": "                                    skip_reasons[\"dynamic_exit_warning\"] += 1"
      },
      {
        "line": 1925,
        "text": "                                    if \"exit_warning_log\" not in h:"
      },
      {
        "line": 1926,
        "text": "                                        h[\"exit_warning_log\"] = []"
      },
      {
        "line": 1927,
        "text": "                                    last_warn = (h[\"exit_warning_log\"][-1][\"date\"]"
      },
      {
        "line": 1928,
        "text": "                                                 if h[\"exit_warning_log\"] else None)"
      },
      {
        "line": 1929,
        "text": "                                    prev_date = (master_dates[master_dates.index(date_t)-1]"
      },
      {
        "line": 1930,
        "text": "                                                 if date_t in master_dates and"
      },
      {
        "line": 1931,
        "text": "                                                 master_dates.index(date_t) > 0 else None)"
      },
      {
        "line": 1932,
        "text": "                                    is_consecutive = (last_warn and last_warn == prev_date)"
      },
      {
        "line": 1933,
        "text": "                                    if not is_consecutive:"
      },
      {
        "line": 1934,
        "text": "                                        h[\"exit_warning_log\"].append({"
      },
      {
        "line": 1935,
        "text": "                                            \"date\": date_t,"
      },
      {
        "line": 1936,
        "text": "                                            \"ls\": round(ls, 2),"
      },
      {
        "line": 1937,
        "text": "                                            \"price\": round(close_t, 2),"
      },
      {
        "line": 1938,
        "text": "                                            \"ma50\": round(stock_ma50, 2),"
      },
      {
        "line": 1939,
        "text": "                                            \"price_vs_ma50_pct\": round("
      },
      {
        "line": 1940,
        "text": "                                                (close_t/stock_ma50-1)*100, 2)"
      },
      {
        "line": 1941,
        "text": "                                                if stock_ma50 > 0 else 0,"
      },
      {
        "line": 1942,
        "text": "                                            \"ma50_slope\": round(stock_slope, 4),"
      },
      {
        "line": 1943,
        "text": "                                            \"market_state\": market_state,"
      },
      {
        "line": 1944,
        "text": "                                            \"warning_day\": True,"
      },
      {
        "line": 1945,
        "text": "                                        })"
      },
      {
        "line": 1946,
        "text": "                                    else:"
      },
      {
        "line": 1947,
        "text": "                                        h[\"exit_warning_log\"][-1]["
      },
      {
        "line": 1948,
        "text": "                                            \"last_consecutive_date\"] = date_t"
      },
      {
        "line": 1949,
        "text": "                                    h[\"exit_warning\"] = date_t"
      },
      {
        "line": 1950,
        "text": "                                    continue  # EXIT_WARNING → HOLD"
      },
      {
        "line": 1951,
        "text": "                                else:"
      },
      {
        "line": 1952,
        "text": "                                    h[\"exit_type\"] = \"SOFT_EXIT_CONFIRMED\""
      },
      {
        "line": 1953,
        "text": "                                    skip_reasons[\"dynamic_soft_exit_confirmed\"] = ("
      },
      {
        "line": 1954,
        "text": "                                        skip_reasons.get(\"dynamic_soft_exit_confirmed\", 0) + 1)"
      },
      {
        "line": 1955,
        "text": "                            else:"
      },
      {
        "line": 1956,
        "text": "                                # CAUTIOUS_ON / CASH_MODE：LS<60 本身足以退出"
      },
      {
        "line": 1957,
        "text": "                                if ls_below_60:"
      },
      {
        "line": 1958,
        "text": "                                    h[\"exit_type\"] = \"SOFT_EXIT_CONFIRMED\""
      },
      {
        "line": 1959,
        "text": "                                    skip_reasons[\"dynamic_soft_exit_confirmed\"] = ("
      },
      {
        "line": 1960,
        "text": "                                        skip_reasons.get(\"dynamic_soft_exit_confirmed\", 0) + 1)"
      },
      {
        "line": 1961,
        "text": "                                # LS>=60 时继续持有，不生成 warning"
      },
      {
        "line": 1962,
        "text": "                    else:"
      },
      {
        "line": 1963,
        "text": "                        # ── E1 MinHold（原逻辑）────────────────────────────"
      },
      {
        "line": 1964,
        "text": "                        is_broken = is_broken_trend(sig.get(\"trend_state\", \"\"))"
      },
      {
        "line": 1965,
        "text": "                        if min_holding_days > 0 and holding_days_so_far < min_holding_days and not (min_hold_allow_broken_exit and is_broken):"
      },
      {
        "line": 1966,
        "text": "                            skip_reasons[\"min_hold_block\"] += 1"
      },
      {
        "line": 1967,
        "text": "                            continue"
      },
      {
        "line": 1968,
        "text": "                if action == \"ADD\" and block_add_after_take_profit and holdings[sym].get(\"take_profit_triggered\"):"
      },
      {
        "line": 1969,
        "text": "                    skip_reasons[\"add_blocked_after_tp\"] += 1"
      },
      {
        "line": 1970,
        "text": "                    continue"
      },
      {
        "line": 1971,
        "text": "                if action == \"ADD\" and not market_entry_allowed:"
      },
      {
        "line": 1972,
        "text": "                    reason = \"market_shock_block\" if market_shock else \"market_risk_off_block\""
      },
      {
        "line": 1973,
        "text": "                    skip_reasons[reason] += 1"
      },
      {
        "line": 1974,
        "text": "                    continue"
      },
      {
        "line": 1975,
        "text": "                # 记录 reason（在 T 日信号生成时调用，不在 T+1 执行时重算）"
      },
      {
        "line": 1976,
        "text": "                reason_info = trade_action_reason("
      },
      {
        "line": 1977,
        "text": "                    state, mom, rs, close_t, ma50_v, ma50_sl,"
      },
      {
        "line": 1978,
        "text": "                    ls, th, market_score_default,"
      },
      {
        "line": 1979,
        "text": "                    ls60_exit_mode=ls60_exit_mode,"
      },
      {
        "line": 1980,
        "text": "                )"
      },
      {
        "line": 1981,
        "text": "                # 一致性检查："
      },
      {
        "line": 1982,
        "text": "                # REDUCE / EXIT mismatch → raise（风险动作必须准确）"
      },
      {
        "line": 1983,
        "text": "                # BUY / ADD mismatch     → 仅计数，不中断（进攻类语义相近）"
      },
      {
        "line": 1984,
        "text": "                reason_action = reason_info.get(\"action\", \"\")"
      },
      {
        "line": 1985,
        "text": "                if action != reason_action:"
      },
      {
        "line": 1986,
        "text": "                    risk_actions = {\"REDUCE\", \"EXIT\"}"
      },
      {
        "line": 1987,
        "text": "                    if {action, reason_action} & risk_actions:"
      },
      {
        "line": 1988,
        "text": "                        raise RuntimeError("
      },
      {
        "line": 1989,
        "text": "                            f\"action_reason_mismatch: {sym} \""
      },
      {
        "line": 1990,
        "text": "                            f\"sig_action={action} reason_action={reason_action} \""
      },
      {
        "line": 1991,
        "text": "                            f\"ls60_exit_mode={ls60_exit_mode} \""
      },
      {
        "line": 1992,
        "text": "                            f\"ls={ls:.1f} state={state} price={close_t:.2f} ma50={ma50_v:.2f}\""
      },
      {
        "line": 1993,
        "text": "                        )"
      },
      {
        "line": 1994,
        "text": "                    else:"
      },
      {
        "line": 1995,
        "text": "                        skip_reasons[\"action_reason_buy_add_mismatch\"] += 1"
      },
      {
        "line": 1996,
        "text": "                # CAUTIOUS_ON/CASH_MODE 禁止 ADD（生成层拦截）"
      },
      {
        "line": 1997,
        "text": "                if action == \"ADD\" and market_gate_enabled and market_state in (\"CAUTIOUS_ON\", \"CASH_MODE\"):"
      },
      {
        "line": 1998,
        "text": "                    skip_reasons[\"gate_add_blocked\"] = skip_reasons.get(\"gate_add_blocked\", 0) + 1"
      },
      {
        "line": 1999,
        "text": "                    continue"
      },
      {
        "line": 2000,
        "text": ""
      },
      {
        "line": 2001,
        "text": "                if action in (\"EXIT\", \"REDUCE\"):"
      },
      {
        "line": 2002,
        "text": "                    pr = reason_info.get(\"primary_reason\", \"\")"
      },
      {
        "line": 2003,
        "text": "                    pending_signal_reason_dist[pr] = pending_signal_reason_dist.get(pr, 0) + 1"
      },
      {
        "line": 2004,
        "text": ""
      },
      {
        "line": 2005,
        "text": "                # 方案A：LS<60 REDUCE 一次性保护（STEP 3 过滤，避免每天重复减仓）"
      },
      {
        "line": 2006,
        "text": "                if (action == \"REDUCE\""
      },
      {
        "line": 2007,
        "text": "                        and reason_info.get(\"primary_reason\") == \"leader_score_below_60\""
      },
      {
        "line": 2008,
        "text": "                        and sym in holdings"
      },
      {
        "line": 2009,
        "text": "                        and holdings[sym].get(\"ls60_reduce_triggered\")):"
      },
      {
        "line": 2010,
        "text": "                    skip_reasons[\"ls60_reduce_already_triggered\"] += 1"
      },
      {
        "line": 2011,
        "text": "                    continue"
      },
      {
        "line": 2012,
        "text": ""
      },
      {
        "line": 2013,
        "text": "                management_orders.append({"
      }
    ]
  },
  {
    "start": 2121,
    "end": 2176,
    "line_count": 56,
    "rows": [
      {
        "line": 2121,
        "text": "                        \"strategy\": strategy_variant,"
      },
      {
        "line": 2122,
        "text": "                    })"
      },
      {
        "line": 2123,
        "text": ""
      },
      {
        "line": 2124,
        "text": "        action_priority = {\"EXIT\": 0, \"REDUCE\": 1, \"REL_REDUCE\": 2, \"TP_REDUCE\": 3, \"ADD\": 4}"
      },
      {
        "line": 2125,
        "text": "        management_orders.sort(key=lambda o: action_priority.get(o[\"action\"], 9))"
      },
      {
        "line": 2126,
        "text": "        buy_orders.sort(key=lambda o: o.get(\"entry_rank\") or 999)"
      },
      {
        "line": 2127,
        "text": "        # P0 Fix: 最后一个 sim 日（T日）不生成新 BUY/ADD"
      },
      {
        "line": 2128,
        "text": "        # 因为 T+1 执行时会等于或超过 sim_end_date，导致 entry==exit invalid"
      },
      {
        "line": 2129,
        "text": "        _next_date = master_dates[t+1] if t+1 < len(master_dates) else None"
      },
      {
        "line": 2130,
        "text": "        # 最后一个或倒数第二个 sim 日不生成新 BUY（T+1 执行时会撞上 sim_end_date）"
      },
      {
        "line": 2131,
        "text": "        _is_last_sim_day = (_trade_end and _next_date and _next_date >= _trade_end)"
      },
      {
        "line": 2132,
        "text": "        if _is_last_sim_day:"
      },
      {
        "line": 2133,
        "text": "            buy_orders = []  # 不在最后一天生成新买入（防止 entry==exit invalid）"
      },
      {
        "line": 2134,
        "text": "        pending_orders = management_orders + buy_orders"
      },
      {
        "line": 2135,
        "text": ""
      },
      {
        "line": 2136,
        "text": "        if (t - min_history) % 20 == 0:"
      },
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
      },
      {
        "line": 2140,
        "text": "            logger.info("
      },
      {
        "line": 2141,
        "text": "                f\"  Layer D market-gate: {t}/{n_days} {date_t} \""
      },
      {
        "line": 2142,
        "text": "                f\"gate={gate_state} SPXvsMA50={(spx_close_t/spx_ma50_t-1)*100:+.1f}% \""
      },
      {
        "line": 2143,
        "text": "                f\"day={spx_day_return*100:+.1f}% cash={cash:.0f} \""
      },
      {
        "line": 2144,
        "text": "                f\"holdings={len(holdings)} trades={len(closed_trades)}\""
      },
      {
        "line": 2145,
        "text": "            )"
      },
      {
        "line": 2146,
        "text": ""
      },
      {
        "line": 2147,
        "text": "        if t % 30 == 0:"
      },
      {
        "line": 2148,
        "text": "            daily_records.append({"
      },
      {
        "line": 2149,
        "text": "                \"date\":           date_t,"
      },
      {
        "line": 2150,
        "text": "                \"cash\":           round(cash, 2),"
      },
      {
        "line": 2151,
        "text": "                \"position_value\": round(position_value, 2),"
      },
      {
        "line": 2152,
        "text": "                \"total_equity\":   round(total_equity, 2),"
      },
      {
        "line": 2153,
        "text": "                \"n_holdings\":     len(holdings),"
      },
      {
        "line": 2154,
        "text": "                \"pending_orders\": len(pending_orders),"
      },
      {
        "line": 2155,
        "text": "                \"market_gate_state\": ("
      },
      {
        "line": 2156,
        "text": "                    \"ALLOW\" if market_entry_allowed else"
      },
      {
        "line": 2157,
        "text": "                    \"SHOCK\" if market_shock else \"RISK_OFF\""
      },
      {
        "line": 2158,
        "text": "                ),"
      },
      {
        "line": 2159,
        "text": "                \"spx_close\":      round(spx_close_t, 2),"
      },
      {
        "line": 2160,
        "text": "                \"spx_ma50\":       round(spx_ma50_t, 2),"
      },
      {
        "line": 2161,
        "text": "                \"spx_day_return_pct\": round(spx_day_return * 100, 2),"
      },
      {
        "line": 2162,
        "text": "            })"
      },
      {
        "line": 2163,
        "text": ""
      },
      {
        "line": 2164,
        "text": "    # ════════════════════════════════════════════════════"
      },
      {
        "line": 2165,
        "text": "    # 强制平仓剩余持仓"
      },
      {
        "line": 2166,
        "text": "    # ════════════════════════════════════════════════════"
      },
      {
        "line": 2167,
        "text": "    # 强制平仓日期：用 sim_end_date（若有），否则用数据末日"
      },
      {
        "line": 2168,
        "text": "    if sim_end_date and sim_end_date in master_dates:"
      },
      {
        "line": 2169,
        "text": "        last_date = sim_end_date"
      },
      {
        "line": 2170,
        "text": "    elif sim_end_date:"
      },
      {
        "line": 2171,
        "text": "        # sim_end_date 不在 master_dates，找最近的前一个交易日"
      },
      {
        "line": 2172,
        "text": "        last_date = max((d for d in master_dates if d <= sim_end_date), default=master_dates[-2])"
      },
      {
        "line": 2173,
        "text": "    else:"
      },
      {
        "line": 2174,
        "text": "        last_date = master_dates[-2] if len(master_dates) >= 2 else master_dates[-1]"
      },
      {
        "line": 2175,
        "text": "    sim_end_count = 0"
      },
      {
        "line": 2176,
        "text": "    for sym, h in list(holdings.items()):"
      }
    ]
  },
  {
    "start": 2314,
    "end": 2349,
    "line_count": 36,
    "rows": [
      {
        "line": 2314,
        "text": ""
      },
      {
        "line": 2315,
        "text": "    if not reasonable:"
      },
      {
        "line": 2316,
        "text": "        status = \"INVALID\""
      },
      {
        "line": 2317,
        "text": "    elif not sample_valid:"
      },
      {
        "line": 2318,
        "text": "        # 区分：不足样本但数字好 vs 不足样本且数字差"
      },
      {
        "line": 2319,
        "text": "        if total_return > spx_total and pf >= 1.0 and max_dd * 100 <= 35:"
      },
      {
        "line": 2320,
        "text": "            status = \"PROMISING_INSUFFICIENT_SAMPLE\""
      },
      {
        "line": 2321,
        "text": "        else:"
      },
      {
        "line": 2322,
        "text": "            status = \"INSUFFICIENT_SAMPLE\""
      },
      {
        "line": 2323,
        "text": "    elif total_return > spx_total and pf > 1.2 and completed_trades >= 10:"
      },
      {
        "line": 2324,
        "text": "        status = \"PASS\""
      },
      {
        "line": 2325,
        "text": "    elif total_return > 0:"
      },
      {
        "line": 2326,
        "text": "        status = \"PARTIAL\""
      },
      {
        "line": 2327,
        "text": "    else:"
      },
      {
        "line": 2328,
        "text": "        status = \"FAIL\""
      },
      {
        "line": 2329,
        "text": ""
      },
      {
        "line": 2330,
        "text": "    logger.info(f\"  Market gate days: allowed={market_gate_days['entry_allowed']} \""
      },
      {
        "line": 2331,
        "text": "                f\"blocked={market_gate_days['blocked_total']} \""
      },
      {
        "line": 2332,
        "text": "                f\"risk_off={market_gate_days['risk_off']} \""
      },
      {
        "line": 2333,
        "text": "                f\"shock={market_gate_days['market_shock']}\")"
      },
      {
        "line": 2334,
        "text": "    logger.info(f\"  Relative stop: signals={relative_stop_stats['signals']} \""
      },
      {
        "line": 2335,
        "text": "                f\"executed={relative_stop_stats['executed']}\")"
      },
      {
        "line": 2336,
        "text": "    logger.info(f\"  Fixed TP: signals={take_profit_stats['signals']} \""
      },
      {
        "line": 2337,
        "text": "                f\"executed={take_profit_stats['executed']}\")"
      },
      {
        "line": 2338,
        "text": "    if dynamic_exit_enabled:"
      },
      {
        "line": 2339,
        "text": "        logger.info("
      },
      {
        "line": 2340,
        "text": "            f\"  Dynamic Exit stats: \""
      },
      {
        "line": 2341,
        "text": "            f\"warning={skip_reasons.get('dynamic_exit_warning',0)} \""
      },
      {
        "line": 2342,
        "text": "            f\"soft_confirmed={skip_reasons.get('dynamic_soft_exit_confirmed',0)} \""
      },
      {
        "line": 2343,
        "text": "            f\"hard_exit={skip_reasons.get('dynamic_hard_exit_triggered',0)}\""
      },
      {
        "line": 2344,
        "text": "        )"
      },
      {
        "line": 2345,
        "text": "    if invalid_trades:"
      },
      {
        "line": 2346,
        "text": "        for inv in invalid_trades:"
      },
      {
        "line": 2347,
        "text": "            logger.warn(f\"  ⚠️  INVALID TRADE: {inv}\")"
      },
      {
        "line": 2348,
        "text": "    logger.info(f\"  Layer D v1.6-top3-rs-minhold-relstop: {status}\")"
      },
      {
        "line": 2349,
        "text": "    logger.info(f\"  ${init_cap:,.0f}→${final_equity:,.2f} ({total_return:+.2f}%) \""
      }
    ]
  },
  {
    "start": 2357,
    "end": 2430,
    "line_count": 74,
    "rows": [
      {
        "line": 2357,
        "text": "        \"name\":    \"Stateful Portfolio Backtest\","
      },
      {
        "line": 2358,
        "text": "        \"status\":  status,"
      },
      {
        "line": 2359,
        "text": "        \"version\": \"v1.6-top3-rs-minhold-relstop\","
      },
      {
        "line": 2360,
        "text": "        \"execution_model\": a.get(\"execution_model\", \"adverse_intraday\"),"
      },
      {
        "line": 2361,
        "text": "        \"strategy_variant\": strategy_variant,"
      },
      {
        "line": 2362,
        "text": "        \"entry_top_n\": entry_top_n,"
      },
      {
        "line": 2363,
        "text": "        \"rank_based_exit\": rank_based_exit,"
      },
      {
        "line": 2364,
        "text": "        \"strategy_controls\": {"
      },
      {
        "line": 2365,
        "text": "            \"entry_rs_min\": entry_rs_min,"
      },
      {
        "line": 2366,
        "text": "            \"ls60_exit_mode\":             ls60_exit_mode,"
      },
      {
        "line": 2367,
        "text": "            \"candidate_top_n\":            candidate_top_n,"
      },
      {
        "line": 2368,
        "text": "            \"qualified_entry_enabled\":    qualified_entry_enabled,"
      },
      {
        "line": 2369,
        "text": "            \"qualified_rs_min\":           qualified_rs_min,"
      },
      {
        "line": 2370,
        "text": "            \"qualified_momentum_min\":     qualified_momentum_min,"
      },
      {
        "line": 2371,
        "text": "            \"qualified_th_min\":           qualified_th_min,"
      },
      {
        "line": 2372,
        "text": "            \"qualified_states\":           list(qualified_states),"
      },
      {
        "line": 2373,
        "text": "            \"qualified_price_above_ma50\": qualified_price_above_ma50,"
      },
      {
        "line": 2374,
        "text": "            \"qualified_ma50_slope_min\":   qualified_ma50_slope_min,"
      },
      {
        "line": 2375,
        "text": "            # Qualified Pool 诊断"
      },
      {
        "line": 2376,
        "text": "            \"qp_avg_pool_size\":          round(qp_diag[\"pool_size_sum\"] / max(qp_diag[\"pool_days\"], 1), 1),"
      },
      {
        "line": 2377,
        "text": "            \"qp_pool_days\":              qp_diag[\"pool_days\"],"
      },
      {
        "line": 2378,
        "text": "            \"qp_days_pool_lt_3\":         qp_diag[\"days_pool_lt_3\"],"
      },
      {
        "line": 2379,
        "text": "            \"qp_days_pool_ge_10\":        qp_diag[\"days_pool_ge_10\"],"
      },
      {
        "line": 2380,
        "text": "            \"qp_buy_orders_generated\":   qp_diag[\"buy_orders_generated\"],"
      },
      {
        "line": 2381,
        "text": "            \"min_holding_days\": min_holding_days,"
      },
      {
        "line": 2382,
        "text": "            \"min_hold_allow_broken_exit\": min_hold_allow_broken_exit,"
      },
      {
        "line": 2383,
        "text": "            \"e1r_regime_wiring_enabled\": e1r_regime_wiring_enabled,"
      },
      {
        "line": 2384,
        "text": "            \"e1r_regime_source\": a.get(\"e1r_regime_source\") if e1r_regime_wiring_enabled else None,"
      },
      {
        "line": 2385,
        "text": "            \"relative_stop_enabled\": relative_stop_enabled,"
      },
      {
        "line": 2386,
        "text": "            \"relative_stop_underperform_pct\": round(relative_stop_underperform * 100, 2),"
      },
      {
        "line": 2387,
        "text": "            \"relative_stop_action\": relative_stop_action,"
      },
      {
        "line": 2388,
        "text": "            \"relative_stop_once_per_position\": relative_stop_once,"
      },
      {
        "line": 2389,
        "text": "            \"relative_stop_stats\": relative_stop_stats,"
      },
      {
        "line": 2390,
        "text": "            \"fixed_take_profit_enabled\": take_profit_enabled,"
      },
      {
        "line": 2391,
        "text": "        },"
      },
      {
        "line": 2392,
        "text": "        \"partial_take_profit\": {"
      },
      {
        "line": 2393,
        "text": "            \"name\": \"TP7-P\","
      },
      {
        "line": 2394,
        "text": "            \"enabled\": take_profit_enabled,"
      },
      {
        "line": 2395,
        "text": "            \"trigger_gain_pct\": round(take_profit_threshold * 100, 2),"
      },
      {
        "line": 2396,
        "text": "            \"sell_fraction_pct\": round(take_profit_fraction * 100, 1),"
      },
      {
        "line": 2397,
        "text": "            \"trigger_price\": \"signal-day close vs actual average cost\","
      },
      {
        "line": 2398,
        "text": "            \"execution\": \"T+1 adverse low minus one-way costs\","
      },
      {
        "line": 2399,
        "text": "            \"once_per_position\": True,"
      },
      {
        "line": 2400,
        "text": "            \"block_add_after_trigger\": block_add_after_take_profit,"
      },
      {
        "line": 2401,
        "text": "            \"stats\": take_profit_stats,"
      },
      {
        "line": 2402,
        "text": "            \"note\": \"Partial reduction releases cash but does not free a Max3 symbol slot.\","
      },
      {
        "line": 2403,
        "text": "        },"
      },
      {
        "line": 2404,
        "text": "        \"market_entry_gate\": {"
      },
      {
        "line": 2405,
        "text": "            \"variant\": market_gate_variant,"
      },
      {
        "line": 2406,
        "text": "            \"enabled\": market_gate_enabled,"
      },
      {
        "line": 2407,
        "text": "            \"risk_off_rule\": \"SPX close < SPX MA50\" if risk_off_below_spx_ma50 else \"disabled\","
      },
      {
        "line": 2408,
        "text": "            \"market_shock_rule\": ("
      },
      {
        "line": 2409,
        "text": "                f\"SPX daily return <= {market_shock_daily_return*100:.1f}%\""
      },
      {
        "line": 2410,
        "text": "                if market_shock_gate_enabled else \"disabled\""
      },
      {
        "line": 2411,
        "text": "            ),"
      },
      {
        "line": 2412,
        "text": "            \"blocked_actions\": [\"BUY\", \"ADD\"],"
      },
      {
        "line": 2413,
        "text": "            \"unaffected_actions\": [\"HOLD\", \"REDUCE\", \"EXIT\"],"
      },
      {
        "line": 2414,
        "text": "            \"days\": market_gate_days,"
      },
      {
        "line": 2415,
        "text": "        },"
      },
      {
        "line": 2416,
        "text": "        # 样本有效性（完整字段）"
      },
      {
        "line": 2417,
        "text": "        \"sample_validity\": {"
      },
      {
        "line": 2418,
        "text": "            \"is_valid\":            sample_valid,"
      },
      {
        "line": 2419,
        "text": "            \"sample_status\":       status if status == \"INSUFFICIENT_SAMPLE\" else (\"VALID\" if sample_valid else \"INSUFFICIENT\"),"
      },
      {
        "line": 2420,
        "text": "            \"simulation_start_date\": sim_start_date,"
      },
      {
        "line": 2421,
        "text": "            \"simulation_end_date\":   sim_end_date,"
      },
      {
        "line": 2422,
        "text": "            \"simulation_days\":     simulation_days,"
      },
      {
        "line": 2423,
        "text": "            \"total_trades\":        total_trades,"
      },
      {
        "line": 2424,
        "text": "            \"completed_trades\":    completed_trades,"
      },
      {
        "line": 2425,
        "text": "            \"sim_end_trades\":      sim_end_count,"
      },
      {
        "line": 2426,
        "text": "            \"sim_end_ratio_pct\":   round(sim_end_ratio * 100, 1),"
      },
      {
        "line": 2427,
        "text": "            \"invalid_trades\":      len(invalid_trades),"
      },
      {
        "line": 2428,
        "text": "            \"minimum_required\": {"
      },
      {
        "line": 2429,
        "text": "                \"sim_days\":            252,"
      },
      {
        "line": 2430,
        "text": "                \"trades\":              20,"
      }
    ]
  }
]
```

## Decision
```json
{
  "market_gate_source_trace_passed": true,
  "basic_formula_from_k2_r1_mismatch_count": 9,
  "critical_cluster_count": 9,
  "source_hit_summary": {
    "hit_count": 117,
    "by_keyword": {
      "D3_RISK_OFF_PLUS_SHOCK_GATE": 1,
      "RiskOff": 1,
      "SPX<MA50": 1,
      "Shock": 1,
      "gate=": 2,
      "gate_state": 5,
      "ma50": 59,
      "market_entry_gate": 1,
      "market_gate": 25,
      "market_gate_state": 2,
      "risk_off": 13,
      "shock": 27,
      "spx_ma50": 14
    },
    "by_regex": {
      "D3_RISK_OFF_PLUS_SHOCK_GATE": 1,
      "SPX<MA50": 1,
      "gate_state\\s*=": 2,
      "market_gate": 25,
      "risk_off\\s*=": 3,
      "shock\\s*=": 3,
      "spx_ma50\\s*=": 1
    },
    "hit_lines": [
      847,
      848,
      858,
      859,
      885,
      891,
      896,
      897,
      911,
      912,
      913,
      914,
      927,
      928,
      929,
      930,
      938,
      1037,
      1038,
      1072,
      1074,
      1075,
      1386,
      1393,
      1397,
      1398,
      1400,
      1404,
      1405,
      1407,
      1413,
      1414,
      1421,
      1428,
      1434,
      1435,
      1436,
      1437,
      1438,
      1447,
      1448,
      1449,
      1450,
      1459,
      1464,
      1466,
      1475,
      1483,
      1484,
      1487,
      1488,
      1489,
      1490,
      1492,
      1494,
      1510,
      1512,
      1525,
      1531,
      1572,
      1573,
      1574,
      1584,
      1601,
      1602,
      1634,
      1644,
      1653,
      1654,
      1661,
      1662,
      1688,
      1690,
      1739,
      1740,
      1768,
      1769,
      1820,
      1824,
      1833,
      1834,
      1872,
      1876,
      1904,
      1905,
      1906,
      1912,
      1922,
      1938,
      1939,
      1940,
      1941,
      1942,
      1972,
      1977,
      1992,
      1997,
      2137,
      2138,
      2142,
      2155,
      2157,
      2160,
      2330,
      2331,
      2332,
      2333,
      2373,
      2374,
      2404,
      2405,
      2406,
      2407,
      2408,
      2409,
      2410,
      2414
    ]
  },
  "best_diagnostic_hypotheses": [
    {
      "name": "trigger_dayret_None_cooldown_5_include_ma50_False",
      "ok": false,
      "mismatch_count": 3,
      "distribution": {
        "ALLOW": 56,
        "SHOCK": 1,
        "RISK_OFF": 5
      },
      "mismatches": [
        {
          "date": "2021-05-10",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -1.0436,
          "close": 4188.43,
          "ma50": 4041.08
        },
        {
          "date": "2021-05-11",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.8674,
          "close": 4152.1,
          "ma50": 4046.08
        },
        {
          "date": "2021-05-21",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.0784,
          "close": 4155.86,
          "ma50": 4090.8
        }
      ]
    },
    {
      "name": "trigger_dayret_None_cooldown_7_include_ma50_False",
      "ok": false,
      "mismatch_count": 3,
      "distribution": {
        "ALLOW": 54,
        "SHOCK": 1,
        "RISK_OFF": 7
      },
      "mismatches": [
        {
          "date": "2021-05-10",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -1.0436,
          "close": 4188.43,
          "ma50": 4041.08
        },
        {
          "date": "2021-05-11",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.8674,
          "close": 4152.1,
          "ma50": 4046.08
        },
        {
          "date": "2021-05-20",
          "expected": "ALLOW",
          "actual": "RISK_OFF",
          "day_ret": 1.0555,
          "close": 4159.12,
          "ma50": 4086.47
        }
      ]
    },
    {
      "name": "trigger_dayret_-1.5_cooldown_5_include_ma50_False",
      "ok": false,
      "mismatch_count": 3,
      "distribution": {
        "ALLOW": 56,
        "SHOCK": 1,
        "RISK_OFF": 5
      },
      "mismatches": [
        {
          "date": "2021-05-10",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -1.0436,
          "close": 4188.43,
          "ma50": 4041.08
        },
        {
          "date": "2021-05-11",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.8674,
          "close": 4152.1,
          "ma50": 4046.08
        },
        {
          "date": "2021-05-21",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.0784,
          "close": 4155.86,
          "ma50": 4090.8
        }
      ]
    },
    {
      "name": "trigger_dayret_-1.5_cooldown_7_include_ma50_False",
      "ok": false,
      "mismatch_count": 3,
      "distribution": {
        "ALLOW": 54,
        "SHOCK": 1,
        "RISK_OFF": 7
      },
      "mismatches": [
        {
          "date": "2021-05-10",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -1.0436,
          "close": 4188.43,
          "ma50": 4041.08
        },
        {
          "date": "2021-05-11",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.8674,
          "close": 4152.1,
          "ma50": 4046.08
        },
        {
          "date": "2021-05-20",
          "expected": "ALLOW",
          "actual": "RISK_OFF",
          "day_ret": 1.0555,
          "close": 4159.12,
          "ma50": 4086.47
        }
      ]
    },
    {
      "name": "trigger_dayret_None_cooldown_4_include_ma50_False",
      "ok": false,
      "mismatch_count": 4,
      "distribution": {
        "ALLOW": 57,
        "SHOCK": 1,
        "RISK_OFF": 4
      },
      "mismatches": [
        {
          "date": "2021-05-10",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -1.0436,
          "close": 4188.43,
          "ma50": 4041.08
        },
        {
          "date": "2021-05-11",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.8674,
          "close": 4152.1,
          "ma50": 4046.08
        },
        {
          "date": "2021-05-19",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.2943,
          "close": 4115.68,
          "ma50": 4081.26
        },
        {
          "date": "2021-05-21",
          "expected": "RISK_OFF",
          "actual": "ALLOW",
          "day_ret": -0.0784,
          "close": 4155.86,
          "ma50": 4090.8
        }
      ]
    }
  ],
  "recommended_next_stage": "4C-2C-4E-ENGINE-K2-R3",
  "conclusion": "MARKET_GATE_SOURCE_TRACE_PASS_READY_FOR_EXACT_FORMULA_PATCH",
  "recommended_next_action": "Review critical source clusters and patch market_gate_state using the exact legacy formula. Do not proceed to candidate extraction until market gate equivalence passes.",
  "engineering_rule": "A data-fitted hypothesis is not enough. K2-R3 must be tied to source lines from backtest.py."
}
```
