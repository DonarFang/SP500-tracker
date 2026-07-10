# E1R 4C-2C-4E-ENGINE-K2-R3 — Market Gate Source Line Drilldown

Generated At: `2026-07-10T11:58:14.647026+00:00`

## Purpose
Extract exact source lines around market gate assignments and controls.

## Policy
```json
{
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
  "frozen_strategy_files_changed": false
}
```

## Trace Graph
```json
{
  "assignment_lines": [
    {
      "line": 2137,
      "indent": 12,
      "text": "            gate_state = \"ALLOW\" if market_entry_allowed else (",
      "matched_any": [
        "\\bgate_state\\b"
      ],
      "matched_assign": [
        "\\bgate_state\\s*="
      ],
      "matched_control": []
    },
    {
      "line": 2332,
      "indent": 16,
      "text": "                f\"risk_off={market_gate_days['risk_off']} \"",
      "matched_any": [
        "\\brisk_off\\b"
      ],
      "matched_assign": [
        "\\brisk_off\\s*="
      ],
      "matched_control": []
    },
    {
      "line": 2333,
      "indent": 16,
      "text": "                f\"shock={market_gate_days['market_shock']}\")",
      "matched_any": [
        "\\bshock\\b"
      ],
      "matched_assign": [
        "\\bshock\\s*="
      ],
      "matched_control": []
    }
  ],
  "control_lines": [
    {
      "line": 912,
      "indent": 8,
      "text": "        \"D1_NO_MARKET_GATE\" if not market_gate_enabled else",
      "matched_any": [],
      "matched_assign": [],
      "matched_control": [
        "\\bif\\b.*market_gate"
      ]
    },
    {
      "line": 913,
      "indent": 8,
      "text": "        \"D2_RISK_OFF_GATE\" if not market_shock_gate_enabled else",
      "matched_any": [],
      "matched_assign": [],
      "matched_control": [
        "\\bif\\b.*shock"
      ]
    },
    {
      "line": 1393,
      "indent": 8,
      "text": "        if not market_gate_enabled:",
      "matched_any": [],
      "matched_assign": [],
      "matched_control": [
        "\\bif\\b.*market_gate"
      ]
    },
    {
      "line": 1487,
      "indent": 12,
      "text": "            if market_risk_off:",
      "matched_any": [],
      "matched_assign": [],
      "matched_control": [
        "\\bif\\b.*risk_off"
      ]
    },
    {
      "line": 1489,
      "indent": 12,
      "text": "            if market_shock:",
      "matched_any": [],
      "matched_assign": [],
      "matched_control": [
        "\\bif\\b.*shock"
      ]
    },
    {
      "line": 1512,
      "indent": 12,
      "text": "            \"SHOCK\" if market_shock else \"RISK_OFF\"",
      "matched_any": [],
      "matched_assign": [],
      "matched_control": [
        "\\bif\\b.*shock"
      ]
    },
    {
      "line": 1820,
      "indent": 20,
      "text": "                    if market_gate_enabled and len(holdings) >= entry_capacity:",
      "matched_any": [],
      "matched_assign": [],
      "matched_control": [
        "\\bif\\b.*market_gate"
      ]
    },
    {
      "line": 1824,
      "indent": 24,
      "text": "                        reason = \"market_shock_block\" if market_shock else \"market_risk_off_block\"",
      "matched_any": [],
      "matched_assign": [],
      "matched_control": [
        "\\bif\\b.*risk_off",
        "\\bif\\b.*shock"
      ]
    },
    {
      "line": 1872,
      "indent": 20,
      "text": "                    if market_gate_enabled and len(holdings) >= entry_capacity:",
      "matched_any": [],
      "matched_assign": [],
      "matched_control": [
        "\\bif\\b.*market_gate"
      ]
    },
    {
      "line": 1876,
      "indent": 24,
      "text": "                        reason = \"market_shock_block\" if market_shock else \"market_risk_off_block\"",
      "matched_any": [],
      "matched_assign": [],
      "matched_control": [
        "\\bif\\b.*risk_off",
        "\\bif\\b.*shock"
      ]
    },
    {
      "line": 1972,
      "indent": 20,
      "text": "                    reason = \"market_shock_block\" if market_shock else \"market_risk_off_block\"",
      "matched_any": [],
      "matched_assign": [],
      "matched_control": [
        "\\bif\\b.*risk_off",
        "\\bif\\b.*shock"
      ]
    },
    {
      "line": 1997,
      "indent": 16,
      "text": "                if action == \"ADD\" and market_gate_enabled and market_state in (\"CAUTIOUS_ON\", \"CASH_MODE\"):",
      "matched_any": [],
      "matched_assign": [],
      "matched_control": [
        "\\bif\\b.*market_gate"
      ]
    },
    {
      "line": 2138,
      "indent": 16,
      "text": "                \"SHOCK\" if market_shock else \"RISK_OFF\"",
      "matched_any": [],
      "matched_assign": [],
      "matched_control": [
        "\\bif\\b.*shock"
      ]
    },
    {
      "line": 2157,
      "indent": 20,
      "text": "                    \"SHOCK\" if market_shock else \"RISK_OFF\"",
      "matched_any": [],
      "matched_assign": [],
      "matched_control": [
        "\\bif\\b.*shock"
      ]
    },
    {
      "line": 2407,
      "indent": 12,
      "text": "            \"risk_off_rule\": \"SPX close < SPX MA50\" if risk_off_below_spx_ma50 else \"disabled\",",
      "matched_any": [],
      "matched_assign": [],
      "matched_control": [
        "\\bif\\b.*risk_off"
      ]
    },
    {
      "line": 2410,
      "indent": 16,
      "text": "                if market_shock_gate_enabled else \"disabled\"",
      "matched_any": [],
      "matched_assign": [],
      "matched_control": [
        "\\bif\\b.*shock"
      ]
    }
  ],
  "important_line_numbers": [
    914,
    929,
    1525,
    2137,
    2142,
    2155
  ],
  "contexts": [
    {
      "start": 904,
      "end": 924,
      "rows": [
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
        }
      ]
    },
    {
      "start": 919,
      "end": 939,
      "rows": [
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
        }
      ]
    },
    {
      "start": 1515,
      "end": 1535,
      "rows": [
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
        }
      ]
    },
    {
      "start": 2127,
      "end": 2147,
      "rows": [
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
        }
      ]
    },
    {
      "start": 2132,
      "end": 2152,
      "rows": [
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
        }
      ]
    },
    {
      "start": 2145,
      "end": 2165,
      "rows": [
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
        }
      ]
    }
  ]
}
```

## Range Results
```json
[
  {
    "start": 831,
    "end": 954,
    "line_count": 124,
    "matched_row_count": 4,
    "rows": [
      {
        "line": 912,
        "indent": 8,
        "text": "        \"D1_NO_MARKET_GATE\" if not market_gate_enabled else",
        "matched_any": [],
        "matched_assign": [],
        "matched_control": [
          "\\bif\\b.*market_gate"
        ]
      },
      {
        "line": 913,
        "indent": 8,
        "text": "        \"D2_RISK_OFF_GATE\" if not market_shock_gate_enabled else",
        "matched_any": [],
        "matched_assign": [],
        "matched_control": [
          "\\bif\\b.*shock"
        ]
      },
      {
        "line": 914,
        "indent": 8,
        "text": "        \"D3_RISK_OFF_PLUS_SHOCK_GATE\"",
        "matched_any": [
          "\\bD3_RISK_OFF_PLUS_SHOCK_GATE\\b"
        ],
        "matched_assign": [],
        "matched_control": []
      },
      {
        "line": 929,
        "indent": 16,
        "text": "                f\"| RiskOff=SPX<MA50:{risk_off_below_spx_ma50} \"",
        "matched_any": [
          "\\bSPX<MA50\\b"
        ],
        "matched_assign": [],
        "matched_control": []
      }
    ]
  },
  {
    "start": 1021,
    "end": 1054,
    "line_count": 34,
    "matched_row_count": 0,
    "rows": []
  },
  {
    "start": 1056,
    "end": 1091,
    "line_count": 36,
    "matched_row_count": 1,
    "rows": [
      {
        "line": 1074,
        "indent": 8,
        "text": "        \"risk_off\": 0,",
        "matched_any": [
          "\\brisk_off\\b"
        ],
        "matched_assign": [],
        "matched_control": []
      }
    ]
  },
  {
    "start": 1370,
    "end": 1547,
    "line_count": 178,
    "matched_row_count": 8,
    "rows": [
      {
        "line": 1393,
        "indent": 8,
        "text": "        if not market_gate_enabled:",
        "matched_any": [],
        "matched_assign": [],
        "matched_control": [
          "\\bif\\b.*market_gate"
        ]
      },
      {
        "line": 1447,
        "indent": 12,
        "text": "            # shock/VIX 受开关控制，不泄漏到未启用的 variant",
        "matched_any": [
          "\\bshock\\b"
        ],
        "matched_assign": [],
        "matched_control": []
      },
      {
        "line": 1487,
        "indent": 12,
        "text": "            if market_risk_off:",
        "matched_any": [],
        "matched_assign": [],
        "matched_control": [
          "\\bif\\b.*risk_off"
        ]
      },
      {
        "line": 1488,
        "indent": 16,
        "text": "                market_gate_days[\"risk_off\"] += 1",
        "matched_any": [
          "\\brisk_off\\b"
        ],
        "matched_assign": [],
        "matched_control": []
      },
      {
        "line": 1489,
        "indent": 12,
        "text": "            if market_shock:",
        "matched_any": [],
        "matched_assign": [],
        "matched_control": [
          "\\bif\\b.*shock"
        ]
      },
      {
        "line": 1512,
        "indent": 12,
        "text": "            \"SHOCK\" if market_shock else \"RISK_OFF\"",
        "matched_any": [],
        "matched_assign": [],
        "matched_control": [
          "\\bif\\b.*shock"
        ]
      },
      {
        "line": 1525,
        "indent": 12,
        "text": "            \"market_gate_state\": _gate_state,",
        "matched_any": [
          "\\bmarket_gate_state\\b"
        ],
        "matched_assign": [],
        "matched_control": []
      },
      {
        "line": 1531,
        "indent": 12,
        "text": "            \"spx_ma50\": round(spx_ma50_t, 2),",
        "matched_any": [
          "\\bspx_ma50\\b"
        ],
        "matched_assign": [],
        "matched_control": []
      }
    ]
  },
  {
    "start": 1804,
    "end": 1850,
    "line_count": 47,
    "matched_row_count": 2,
    "rows": [
      {
        "line": 1820,
        "indent": 20,
        "text": "                    if market_gate_enabled and len(holdings) >= entry_capacity:",
        "matched_any": [],
        "matched_assign": [],
        "matched_control": [
          "\\bif\\b.*market_gate"
        ]
      },
      {
        "line": 1824,
        "indent": 24,
        "text": "                        reason = \"market_shock_block\" if market_shock else \"market_risk_off_block\"",
        "matched_any": [],
        "matched_assign": [],
        "matched_control": [
          "\\bif\\b.*risk_off",
          "\\bif\\b.*shock"
        ]
      }
    ]
  },
  {
    "start": 1856,
    "end": 2013,
    "line_count": 158,
    "matched_row_count": 4,
    "rows": [
      {
        "line": 1872,
        "indent": 20,
        "text": "                    if market_gate_enabled and len(holdings) >= entry_capacity:",
        "matched_any": [],
        "matched_assign": [],
        "matched_control": [
          "\\bif\\b.*market_gate"
        ]
      },
      {
        "line": 1876,
        "indent": 24,
        "text": "                        reason = \"market_shock_block\" if market_shock else \"market_risk_off_block\"",
        "matched_any": [],
        "matched_assign": [],
        "matched_control": [
          "\\bif\\b.*risk_off",
          "\\bif\\b.*shock"
        ]
      },
      {
        "line": 1972,
        "indent": 20,
        "text": "                    reason = \"market_shock_block\" if market_shock else \"market_risk_off_block\"",
        "matched_any": [],
        "matched_assign": [],
        "matched_control": [
          "\\bif\\b.*risk_off",
          "\\bif\\b.*shock"
        ]
      },
      {
        "line": 1997,
        "indent": 16,
        "text": "                if action == \"ADD\" and market_gate_enabled and market_state in (\"CAUTIOUS_ON\", \"CASH_MODE\"):",
        "matched_any": [],
        "matched_assign": [],
        "matched_control": [
          "\\bif\\b.*market_gate"
        ]
      }
    ]
  },
  {
    "start": 2121,
    "end": 2176,
    "line_count": 56,
    "matched_row_count": 6,
    "rows": [
      {
        "line": 2137,
        "indent": 12,
        "text": "            gate_state = \"ALLOW\" if market_entry_allowed else (",
        "matched_any": [
          "\\bgate_state\\b"
        ],
        "matched_assign": [
          "\\bgate_state\\s*="
        ],
        "matched_control": []
      },
      {
        "line": 2138,
        "indent": 16,
        "text": "                \"SHOCK\" if market_shock else \"RISK_OFF\"",
        "matched_any": [],
        "matched_assign": [],
        "matched_control": [
          "\\bif\\b.*shock"
        ]
      },
      {
        "line": 2142,
        "indent": 16,
        "text": "                f\"gate={gate_state} SPXvsMA50={(spx_close_t/spx_ma50_t-1)*100:+.1f}% \"",
        "matched_any": [
          "\\bgate_state\\b"
        ],
        "matched_assign": [],
        "matched_control": []
      },
      {
        "line": 2155,
        "indent": 16,
        "text": "                \"market_gate_state\": (",
        "matched_any": [
          "\\bmarket_gate_state\\b"
        ],
        "matched_assign": [],
        "matched_control": []
      },
      {
        "line": 2157,
        "indent": 20,
        "text": "                    \"SHOCK\" if market_shock else \"RISK_OFF\"",
        "matched_any": [],
        "matched_assign": [],
        "matched_control": [
          "\\bif\\b.*shock"
        ]
      },
      {
        "line": 2160,
        "indent": 16,
        "text": "                \"spx_ma50\":       round(spx_ma50_t, 2),",
        "matched_any": [
          "\\bspx_ma50\\b"
        ],
        "matched_assign": [],
        "matched_control": []
      }
    ]
  },
  {
    "start": 2314,
    "end": 2349,
    "line_count": 36,
    "matched_row_count": 2,
    "rows": [
      {
        "line": 2332,
        "indent": 16,
        "text": "                f\"risk_off={market_gate_days['risk_off']} \"",
        "matched_any": [
          "\\brisk_off\\b"
        ],
        "matched_assign": [
          "\\brisk_off\\s*="
        ],
        "matched_control": []
      },
      {
        "line": 2333,
        "indent": 16,
        "text": "                f\"shock={market_gate_days['market_shock']}\")",
        "matched_any": [
          "\\bshock\\b"
        ],
        "matched_assign": [
          "\\bshock\\s*="
        ],
        "matched_control": []
      }
    ]
  },
  {
    "start": 2357,
    "end": 2430,
    "line_count": 74,
    "matched_row_count": 3,
    "rows": [
      {
        "line": 2404,
        "indent": 8,
        "text": "        \"market_entry_gate\": {",
        "matched_any": [
          "\\bmarket_entry_gate\\b"
        ],
        "matched_assign": [],
        "matched_control": []
      },
      {
        "line": 2407,
        "indent": 12,
        "text": "            \"risk_off_rule\": \"SPX close < SPX MA50\" if risk_off_below_spx_ma50 else \"disabled\",",
        "matched_any": [],
        "matched_assign": [],
        "matched_control": [
          "\\bif\\b.*risk_off"
        ]
      },
      {
        "line": 2410,
        "indent": 16,
        "text": "                if market_shock_gate_enabled else \"disabled\"",
        "matched_any": [],
        "matched_assign": [],
        "matched_control": [
          "\\bif\\b.*shock"
        ]
      }
    ]
  }
]
```

## Decision
```json
{
  "source_line_drilldown_passed": true,
  "matched_row_count": 30,
  "assignment_line_count": 3,
  "important_line_numbers": [
    914,
    929,
    1525,
    2137,
    2142,
    2155
  ],
  "recommended_next_stage": "4C-2C-4E-ENGINE-K2-R4",
  "conclusion": "MARKET_GATE_SOURCE_LINE_DRILLDOWN_PASS_READY_FOR_FORMULA_RECONSTRUCTION",
  "recommended_next_action": "Use the printed assignment/control contexts to reconstruct the exact legacy market gate formula, then patch the standalone market gate unit and require daily_market_gate_state mismatch_count=0.",
  "engineering_rule": "Do not use a data-fitted formula. The K2-R4 formula must cite exact assignment/control source lines."
}
```
