# Stage 3.8E-2F-2C-4C-10E-R Continuous-Capital Contract

Generated At: `2026-07-08T12:15:23.961229+00:00`

## Core Principle

E1 and E1R 5Y backtests must each be one continuous portfolio-value curve. Market regimes select behavior, but capital does not reset between regimes.

## Status

- Status: `CONTINUOUS_CAPITAL_CONTRACT_AUDIT_COMPLETE_NO_EXPORTS_WRITTEN`
- Strategy files unchanged: `True`
- Canonical existence unchanged: `True`

## Contract

```json
{
  "capital_model": "continuous_single_account",
  "start_date": "2021-06-11",
  "end_date": "2026-06-18",
  "initial_capital": 100000.0,
  "principles": [
    "E1 5Y backtest must be one continuous portfolio-value curve across the full 5Y window.",
    "E1R 5Y backtest must also be one continuous portfolio-value curve across the full 5Y window.",
    "Market regime changes select strategy behavior; they do not create separate independent capital accounts.",
    "Each interval starts from the prior interval's ending portfolio_value/equity.",
    "Each interval has exactly one total portfolio_value/equity.",
    "E1R combines core sleeve + conditional sidecar sleeve + cash into one total portfolio return.",
    "Sidecar is regime-aware and should only be active in eligible regime/subclass intervals.",
    "Sidecar inactive intervals must not create equity gaps; sidecar_return must be 0 or be filled as 0 by composer.",
    "Final total_return, max_drawdown, Sharpe, and PF must be computed from the same continuous equity curve.",
    "No dashboard integration is allowed until continuous-capital canonical exports pass metric validation."
  ],
  "expected_shapes": {
    "e1_canonical": {
      "artifact": "exports/e1_5y_backtest_equity_curve.json",
      "required": true,
      "one_row_per_interval": true,
      "full_window": true,
      "capital_continuity": true,
      "required_fields": [
        "date",
        "equity",
        "portfolio_value",
        "strategy_indexed",
        "cash",
        "market_value"
      ]
    },
    "e1r_canonical": {
      "artifact": "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
      "required": true,
      "one_row_per_interval": true,
      "full_window": true,
      "capital_continuity": true,
      "required_fields": [
        "date",
        "equity",
        "portfolio_value",
        "strategy_indexed",
        "daily_return",
        "core_return",
        "sidecar_return",
        "spx_return",
        "spx_regime",
        "sideways_subclass"
      ]
    },
    "comparison": {
      "artifact": "exports/e1_e1r_5y_equity_comparison.json",
      "required_after_e1_and_e1r": true,
      "must_not_mix_windows": true
    }
  },
  "validation_thresholds": {
    "full_interval_rows_approx": "about 1258-1261",
    "sideways_days_approx": 241,
    "ma_conflict_days_approx": 135,
    "sidecar_active_days_approx": 135,
    "one_row_per_date": true,
    "no_symbol_level_rows_in_portfolio_equity": true
  }
}
```

## Diagnosis

- Continuous-capital contract defined for both E1 and E1R.
- E1 and E1R must each be one continuous full-window portfolio curve; regimes select behavior but do not reset capital.
- Sidecar active count must be validated separately from full interval/equity count.
- Current continuous portfolio candidates found: 8.
- Current full-window portfolio candidates found: 0.
- Symbol-level / non-portfolio rows rejected: 7.
- No existing full-window continuous-capital portfolio curve is currently ready for canonical export.
- Next stage should generate/recover continuous 5Y E1 core daily equity first, then compose E1R using regime-aware sidecar records.

## Portfolio Curve Candidates

```json
[
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.daily_records",
    "length": 22,
    "date_start": "2023-11-06",
    "date_end": "2026-05-13",
    "unique_dates": 22,
    "keys": [
      "cash",
      "date",
      "market_gate_state",
      "n_holdings",
      "pending_orders",
      "position_value",
      "spx_close",
      "spx_day_return_pct",
      "spx_ma50",
      "total_equity"
    ]
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E1_AUDITED_G4_MINHOLD10.daily_records",
    "length": 22,
    "date_start": "2023-11-06",
    "date_end": "2026-05-13",
    "unique_dates": 22,
    "keys": [
      "cash",
      "date",
      "market_gate_state",
      "n_holdings",
      "pending_orders",
      "position_value",
      "spx_close",
      "spx_day_return_pct",
      "spx_ma50",
      "total_equity"
    ]
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E2_DYNAMIC_EXIT_V2.daily_records",
    "length": 22,
    "date_start": "2023-11-06",
    "date_end": "2026-05-13",
    "unique_dates": 22,
    "keys": [
      "cash",
      "date",
      "market_gate_state",
      "n_holdings",
      "pending_orders",
      "position_value",
      "spx_close",
      "spx_day_return_pct",
      "spx_ma50",
      "total_equity"
    ]
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.daily_records",
    "length": 22,
    "date_start": "2023-11-06",
    "date_end": "2026-05-13",
    "unique_dates": 22,
    "keys": [
      "cash",
      "date",
      "market_gate_state",
      "n_holdings",
      "pending_orders",
      "position_value",
      "spx_close",
      "spx_day_return_pct",
      "spx_ma50",
      "total_equity"
    ]
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E1_AUDITED_G4_MINHOLD10.daily_records",
    "length": 22,
    "date_start": "2023-11-06",
    "date_end": "2026-05-13",
    "unique_dates": 22,
    "keys": [
      "cash",
      "date",
      "market_gate_state",
      "n_holdings",
      "pending_orders",
      "position_value",
      "spx_close",
      "spx_day_return_pct",
      "spx_ma50",
      "total_equity"
    ]
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E2_DYNAMIC_EXIT_V2.daily_records",
    "length": 22,
    "date_start": "2023-11-06",
    "date_end": "2026-05-13",
    "unique_dates": 22,
    "keys": [
      "cash",
      "date",
      "market_gate_state",
      "n_holdings",
      "pending_orders",
      "position_value",
      "spx_close",
      "spx_day_return_pct",
      "spx_ma50",
      "total_equity"
    ]
  },
  {
    "path": "exports/oos_equity_curve.json",
    "list": "root.curve",
    "length": 12,
    "date_start": "2026-06-18",
    "date_end": "2026-07-07",
    "unique_dates": 12,
    "keys": [
      "cash",
      "date",
      "equity",
      "holdings_value",
      "n_positions",
      "source"
    ]
  },
  {
    "path": "exports/oos_e1r_v0_2_equity_curve.json",
    "list": "root",
    "length": 1,
    "date_start": "2026-06-18",
    "date_end": "2026-06-18",
    "unique_dates": 1,
    "keys": [
      "backfill_start_date",
      "cash",
      "core_exposure",
      "date",
      "drawdown_pct",
      "equity",
      "forward_return_pct",
      "gross_exposure",
      "market_state",
      "market_value",
      "official_kickoff_date",
      "portfolio_value",
      "regime",
      "shadow_start_date",
      "sidecar_exposure",
      "strategy_id",
      "strategy_indexed",
      "subclass",
      "tracking_status",
      "version"
    ]
  }
]
```

## Full 5Y Portfolio Candidates

```json
[]
```

## Symbol-Level Rejections

```json
[
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E1_AUDITED_G4_MINHOLD10.trades",
    "length": 47,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "reason": "symbol-level rows cannot be used as portfolio equity"
  },
  {
    "path": "exports/portfolio_backtest.json",
    "list": "root.variant_results.E2_DYNAMIC_EXIT_V2.trades",
    "length": 41,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "reason": "symbol-level rows cannot be used as portfolio equity"
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.trades",
    "length": 47,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "reason": "symbol-level rows cannot be used as portfolio equity"
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E1_AUDITED_G4_MINHOLD10.trades",
    "length": 47,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "reason": "symbol-level rows cannot be used as portfolio equity"
  },
  {
    "path": "exports/backtest.json",
    "list": "root.backtest.results.layer_d.variant_results.E2_DYNAMIC_EXIT_V2.trades",
    "length": 41,
    "date_start": null,
    "date_end": null,
    "unique_dates": 0,
    "reason": "symbol-level rows cannot be used as portfolio equity"
  },
  {
    "path": "exports/e1r_v0_2_backtest_equity_curve.json",
    "list": "root.rows",
    "length": 8819,
    "date_start": "2021-06-11",
    "date_end": "2026-06-16",
    "unique_dates": 859,
    "reason": "symbol-level rows cannot be used as portfolio equity"
  },
  {
    "path": "exports/e1r_v0_2_backtest_equity_curve.json",
    "list": "root.equity_curve",
    "length": 8819,
    "date_start": "2021-06-11",
    "date_end": "2026-06-16",
    "unique_dates": 859,
    "reason": "symbol-level rows cannot be used as portfolio equity"
  }
]
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F`: Generate continuous 5Y E1 core equity and compose continuous E1R equity
- Recommended action: Run/extend export-only wrapper to create continuous E1 5Y core_daily_equity_records. Then compose E1R through e1r_composer with regime-aware sidecar records. Only write canonical exports after continuity and frozen metric validation pass.

