# Stage 3.8E-2F-2C-4C-10F-3A E1 Module Entry Recovery

Generated At: `2026-07-08T12:26:40.394418+00:00`

## Status

- Status: `E1_MODULE_ENTRY_RECOVERY_COMPLETE_CANONICAL_NOT_READY`
- Module entry command ok: `True`
- Frozen strategy files unchanged: `True`
- Old mutable exports restored: `True`
- E1 canonical written: `False`

## Diagnosis

- Module entry command ok: True.
- Frozen strategy files unchanged: True.
- Old mutable exports restored: True.
- Candidate lists scanned: 46.
- Accepted full-window continuous E1 candidates: 0.
- E1 canonical written: False.
- Module entry did not produce a full 5Y one-row-per-date continuous E1 portfolio curve.
- Next step should call run_strategy_variant_comparison / run_stateful_simulation through an explicit export-only wrapper with 2021-06-11→2026-06-18 parameters.

## Chosen Candidate

```json
null
```

## Module Run

```json
{
  "cmd": [
    "/Library/Developer/CommandLineTools/usr/bin/python3",
    "-m",
    "src.engine.backtest"
  ],
  "returncode": 0,
  "ok": true,
  "stdout_tail": "",
  "stderr_tail": ""
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

- `Stage 3.8E-2F-2C-4C-10F-3B`: Call E1 stateful simulation through explicit export-only wrapper
- Recommended action: Use module import and the identified run_strategy_variant_comparison / run_stateful_simulation functions. Pass explicit 5Y window and export one continuous daily E1 equity curve only after validation.

