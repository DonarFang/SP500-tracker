# Stage 3.8E-2F-2C-4C-10F-1 E1 Continuous Core Recovery

Generated At: `2026-07-08T12:19:28.156969+00:00`

## Status

- Status: `E1_CONTINUOUS_CORE_RECOVERY_COMPLETE_CANONICAL_NOT_READY`
- Frozen strategy files unchanged: `True`
- Old mutable exports restored: `True`
- E1 canonical written: `False`

## Diagnosis

- Controlled E1 backtest command ok: False.
- Frozen strategy files unchanged: True.
- Old mutable exports restored: True.
- Full-window accepted E1 candidates: 0.
- E1 canonical written: False.
- No existing E1 output produced a full 5Y one-row-per-date continuous portfolio curve.
- Next step should implement an export-only E1 5Y core backtest wrapper or parameterize frozen backtest logic without changing strategy rules.

## Chosen Candidate

```json
null
```

## Backtest Source Date / Path Audit

```json
{
  "date_literals": [
    "2021-06-11",
    "2023-11-06",
    "2024-12-03",
    "2024-12-31",
    "2026-06-11",
    "2026-06-18"
  ],
  "path_literals": [
    "data/research/e1_5y/raw/indices/SPX.json",
    "data/research/e1_5y/raw/stocks",
    "data/research/e1_5y/regimes/spx_regime_daily.json",
    "docs/layer_d_assumptions.md",
    "docs/research/E1R_REGIME_AWARE_STRATEGY_SPEC_v0.1.md",
    "exports/backtest.json"
  ],
  "important_lines": [
    {
      "line": 774,
      "text": "    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）"
    },
    {
      "line": 951,
      "text": "    _trade_start = sim_start_date  # None = 从 min_history 后第一天"
    },
    {
      "line": 1081,
      "text": "    daily_records: list[dict]  = []"
    },
    {
      "line": 1361,
      "text": "        total_equity = cash + position_value"
    },
    {
      "line": 1367,
      "text": "        if position_value > total_equity * 1.02:"
    },
    {
      "line": 1370,
      "text": "        equity_curve.append(total_equity)"
    },
    {
      "line": 1498,
      "text": "            daily_equity_records[-1][\"total_equity\"]"
    },
    {
      "line": 1502,
      "text": "            (total_equity / _prev_equity - 1) * 100"
    },
    {
      "line": 1505,
      "text": "        daily_equity_peak = max(daily_equity_peak, total_equity)"
    },
    {
      "line": 1507,
      "text": "            (daily_equity_peak - total_equity) / daily_equity_peak * 100"
    },
    {
      "line": 1519,
      "text": "            \"total_equity\": round(total_equity, 2),"
    },
    {
      "line": 1522,
      "text": "            \"exposure_pct\": round(position_value / total_equity * 100, 2) if total_equity > 0 else 0.0,"
    },
    {
      "line": 2148,
      "text": "            daily_records.append({"
    },
    {
      "line": 2152,
      "text": "                \"total_equity\":   round(total_equity, 2),"
    },
    {
      "line": 2240,
      "text": "        \"total_equity\": round(final_equity, 2),"
    },
    {
      "line": 2420,
      "text": "            \"simulation_start_date\": sim_start_date,"
    },
    {
      "line": 2476,
      "text": "        \"daily_records\":     daily_records,"
    },
    {
      "line": 2552,
      "text": "        regime_path = Path(\"data/research/e1_5y/regimes/spx_regime_daily.json\")"
    },
    {
      "line": 2590,
      "text": "            \"e1r_regime_source\":     \"data/research/e1_5y/regimes/spx_regime_daily.json\","
    },
    {
      "line": 2606,
      "text": "    # 只用 sim_start_date / sim_end_date 控制交易执行和统计区间。"
    },
    {
      "line": 2612,
      "text": "                \"sim_start_date\": \"2021-06-11\","
    },
    {
      "line": 2620,
      "text": "                \"sim_start_date\": \"2023-11-06\","
    },
    {
      "line": 2625,
      "text": "                \"sim_start_date\": \"2024-12-03\","
    },
    {
      "line": 2630,
      "text": "                \"sim_start_date\": \"2023-11-06\","
    },
    {
      "line": 2653,
      "text": "                sim_start_date=period_cfg[\"sim_start_date\"],"
    },
    {
      "line": 2713,
      "text": "        _stock_dir = Path(\"data/research/e1_5y/raw/stocks\")"
    },
    {
      "line": 2714,
      "text": "        _spx_path = Path(\"data/research/e1_5y/raw/indices/SPX.json\")"
    },
    {
      "line": 2715,
      "text": "        _regime_path = Path(\"data/research/e1_5y/regimes/spx_regime_daily.json\")"
    },
    {
      "line": 2887,
      "text": "                        \"sim_start_date\":   r.get(\"sample_validity\", {}).get(\"simulation_start_date\"),"
    }
  ]
}
```

## Command

```json
{
  "cmd": [
    "/Library/Developer/CommandLineTools/usr/bin/python3",
    "src/engine/backtest.py"
  ],
  "started_at": "2026-07-08T12:19:28.126515+00:00",
  "ended_at": "2026-07-08T12:19:28.153050+00:00",
  "returncode": 1,
  "ok": false,
  "stdout_tail": "",
  "stderr_tail": "Traceback (most recent call last):\n  File \"/Users/dongfang/Downloads/sp500-tracker-v13/src/engine/backtest.py\", line 19, in <module>\n    from ..features.rs import period_return, rs_percentile\nImportError: attempted relative import with no known parent package\n"
}
```

## Candidate Summary

```json
[
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_c.buy_vs_spx",
    "length": 4,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.strategy_controls.qualified_states",
    "length": 1,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.market_entry_gate.blocked_actions",
    "length": 2,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.market_entry_gate.unaffected_actions",
    "length": 3,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.equity_curve",
    "length": 131,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.spx_curve",
    "length": 131,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.daily_records",
    "length": 22,
    "date_start": "2023-11-06",
    "date_end": "2026-05-13",
    "unique_dates": 22,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": 1
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.trades",
    "length": 47,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": true,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.comparison",
    "length": 2,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E1_AUDITED_G4_MINHOLD10.strategy_controls.qualified_states",
    "length": 1,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E1_AUDITED_G4_MINHOLD10.market_entry_gate.blocked_actions",
    "length": 2,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E1_AUDITED_G4_MINHOLD10.market_entry_gate.unaffected_actions",
    "length": 3,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E1_AUDITED_G4_MINHOLD10.equity_curve",
    "length": 131,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E1_AUDITED_G4_MINHOLD10.spx_curve",
    "length": 131,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E1_AUDITED_G4_MINHOLD10.daily_records",
    "length": 22,
    "date_start": "2023-11-06",
    "date_end": "2026-05-13",
    "unique_dates": 22,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": 1
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E1_AUDITED_G4_MINHOLD10.trades",
    "length": 47,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": true,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E2_DYNAMIC_EXIT_V2.strategy_controls.qualified_states",
    "length": 1,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E2_DYNAMIC_EXIT_V2.market_entry_gate.blocked_actions",
    "length": 2,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E2_DYNAMIC_EXIT_V2.market_entry_gate.unaffected_actions",
    "length": 3,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E2_DYNAMIC_EXIT_V2.equity_curve",
    "length": 131,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E2_DYNAMIC_EXIT_V2.spx_curve",
    "length": 131,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E2_DYNAMIC_EXIT_V2.daily_records",
    "length": 22,
    "date_start": "2023-11-06",
    "date_end": "2026-05-13",
    "unique_dates": 22,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": 1
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E2_DYNAMIC_EXIT_V2.trades",
    "length": 41,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": true,
    "max_rows_per_date": null
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.strategy_controls.qualified_states",
    "length": 1,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.market_entry_gate.blocked_actions",
    "length": 2,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.market_entry_gate.unaffected_actions",
    "length": 3,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.daily_records",
    "length": 22,
    "date_start": "2023-11-06",
    "date_end": "2026-05-13",
    "unique_dates": 22,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": 1
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.comparison",
    "length": 2,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E1_AUDITED_G4_MINHOLD10.strategy_controls.qualified_states",
    "length": 1,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E1_AUDITED_G4_MINHOLD10.market_entry_gate.blocked_actions",
    "length": 2,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E1_AUDITED_G4_MINHOLD10.market_entry_gate.unaffected_actions",
    "length": 3,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E1_AUDITED_G4_MINHOLD10.equity_curve",
    "length": 131,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E1_AUDITED_G4_MINHOLD10.spx_curve",
    "length": 131,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E1_AUDITED_G4_MINHOLD10.daily_records",
    "length": 22,
    "date_start": "2023-11-06",
    "date_end": "2026-05-13",
    "unique_dates": 22,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": 1
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E1_AUDITED_G4_MINHOLD10.trades",
    "length": 47,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": true,
    "max_rows_per_date": null
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E2_DYNAMIC_EXIT_V2.strategy_controls.qualified_states",
    "length": 1,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E2_DYNAMIC_EXIT_V2.market_entry_gate.blocked_actions",
    "length": 2,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E2_DYNAMIC_EXIT_V2.market_entry_gate.unaffected_actions",
    "length": 3,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E2_DYNAMIC_EXIT_V2.equity_curve",
    "length": 131,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E2_DYNAMIC_EXIT_V2.spx_curve",
    "length": 131,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E2_DYNAMIC_EXIT_V2.daily_records",
    "length": 22,
    "date_start": "2023-11-06",
    "date_end": "2026-05-13",
    "unique_dates": 22,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": 1
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E2_DYNAMIC_EXIT_V2.trades",
    "length": 41,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": true,
    "max_rows_per_date": null
  },
  {
    "path": "exports/oos_equity_curve.json",
    "list": "root.curve",
    "length": 12,
    "date_start": "2026-06-18",
    "date_end": "2026-07-07",
    "unique_dates": 12,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": 1
  },
  {
    "path": "data/research/e1r/e1r_formal_backtest_v0_1.json",
    "list": "root.equity_curve",
    "length": 131,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "data/research/e1r/e1r_formal_backtest_v0_1.json",
    "list": "root.spx_curve",
    "length": 131,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": false,
    "max_rows_per_date": null
  },
  {
    "path": "data/research/e1r/e1r_formal_backtest_v0_1.json",
    "list": "root.trades",
    "length": 39,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "full_5y": false,
    "has_symbol_level_rows": true,
    "max_rows_per_date": null
  }
]
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-2`: Generate export-only continuous E1 5Y core backtest if 10F-1 did not recover it
- Recommended action: If no E1 canonical was written, inspect backtest.py's portfolio loop and create an export-only wrapper that runs the same E1 rules from 2021-06-11 to 2026-06-18, producing one continuous daily equity record per interval.

