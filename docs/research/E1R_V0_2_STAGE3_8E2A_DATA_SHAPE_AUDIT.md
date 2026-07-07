# Stage 3.8E-2A E1 / E1R / SPX Data-Shape Audit

Generated At: `2026-07-07T13:11:58.529585+00:00`
Main HEAD: `f1cff91`

## Status

- Status: `AUDIT_COMPLETE_NO_DASHBOARD_SOURCE_CHANGES`
- Strategy logic changed: `False`
- Dashboard source changed: `False`
- Exports changed: `False`

## Summary Candidates

- `e1_historical` source `exports/backtest.json`
  - objects_found: `10`
  - top_paths: `['$', '$.backtest', '$.backtest.results', '$.backtest.results.layer_d', '$.backtest.results.layer_d.comparison[0]']`
- `e1r_v0_2_historical` source `exports/e1r_v0_2_backtest_summary.json`
  - objects_found: `1`
  - top_paths: `['$']`
- `e1_forward` source `exports/oos_summary.json`
  - objects_found: `N/A`
  - top_paths: `['generated_at', 'generated_at_display', 'status', 'stale_reason', 'run_date', 'last_successful_run', 'last_market_date', 'expected_market_date']`
- `e1r_forward` source `exports/oos_e1r_v0_2_summary.json`
  - objects_found: `N/A`
  - top_paths: `['generated_at', 'phase', 'strategy_id', 'version', 'research_status', 'status_date', 'market_state', 'regime', 'subclass', 'mutually_exclusive_state_model', 'core_active', 'sidecar_active', 'sidecar_selected_count', 'gross_exposure', 'top_n', 'execution_status', 'equity_status', 'notes']`

## Equity Curve Candidates

- `e1_historical` from `exports/backtest.json`:
  - path `$.backtest.results.layer_d.daily_records`, rows `22`, date keys `['date']`, equity keys `['total_equity']`, first `2023-11-06`, last `2026-05-13`
  - path `$.backtest.results.layer_d.variant_results.E1_AUDITED_G4_MINHOLD10.daily_records`, rows `22`, date keys `['date']`, equity keys `['total_equity']`, first `2023-11-06`, last `2026-05-13`
  - path `$.backtest.results.layer_d.variant_results.E2_DYNAMIC_EXIT_V2.daily_records`, rows `22`, date keys `['date']`, equity keys `['total_equity']`, first `2023-11-06`, last `2026-05-13`
- `e1_forward` from `exports/oos_equity_curve.json`:
  - path `$.curve`, rows `11`, date keys `['date']`, equity keys `['equity']`, first `2026-06-18`, last `2026-07-06`
- `e1r_v0_2_historical` from `exports/e1r_v0_2_backtest_equity_curve.json`:
  - path `$.equity_curve`, rows `8819`, date keys `['date']`, equity keys `['close', 'equity']`, first `2021-06-11`, last `2026-06-16`
  - path `$.rows`, rows `8819`, date keys `['date']`, equity keys `['close', 'equity']`, first `2021-06-11`, last `2026-06-16`
- `e1r_v0_2_forward` from `exports/oos_e1r_v0_2_equity_curve.json`:
  - path `$.records`, rows `1`, date keys `['date']`, equity keys `['combined_equity', 'core_equity', 'equity_status', 'sidecar_equity']`, first `2026-06-18`, last `2026-06-18`
- `spx_benchmark` from `likely exports/backtest.json, may be embedded as spx/benchmark fields or separate array`:
  - path `$.backtest.results.layer_d.daily_records`, rows `22`, date keys `['date']`, equity keys `['total_equity']`, first `2023-11-06`, last `2026-05-13`
  - path `$.backtest.results.layer_d.variant_results.E1_AUDITED_G4_MINHOLD10.daily_records`, rows `22`, date keys `['date']`, equity keys `['total_equity']`, first `2023-11-06`, last `2026-05-13`
  - path `$.backtest.results.layer_d.variant_results.E2_DYNAMIC_EXIT_V2.daily_records`, rows `22`, date keys `['date']`, equity keys `['total_equity']`, first `2023-11-06`, last `2026-05-13`

## Market State / Regime Candidates

- `primary_e1r_status` source `exports/e1r_v0_2_status.json` objects `3`
  - path `$` fields `{'regime': 'UPTREND', 'e1r_market_state': 'UPTREND', 'status_date': '2026-06-18'}`
  - path `$.legacy_market_state` fields `{'state': 'Strong Risk-On', 'date': '2026-07-06'}`
  - path `$.source_files` fields `{'regime': 'data/research/e1_5y/regimes/spx_regime_daily.json'}`
- `e1r_oos_summary` source `exports/oos_e1r_v0_2_summary.json` objects `1`
  - path `$` fields `{'market_state': 'UPTREND', 'regime': 'UPTREND', 'core_active': True, 'sidecar_active': False, 'sidecar_selected_count': 0, 'status_date': '2026-06-18'}`
- `general_market_state` source `exports/market_state.json` objects `1`
  - path `$.market` fields `{'state': 'Strong Risk-On', 'date': '2026-07-06'}`

## Recommendations

- Do not modify dashboard in Stage 3.8E-2A; use this report to design a minimal native render patch.
- Build summary comparison from E1 historical object in backtest.json and E1R v0.2 historical summary export first; only add forward summary fields if shapes are confirmed.
- For equity curve, normalize each candidate array by explicit date key and equity key; do not infer from unrelated numeric fields.
- SPX should only be plotted if a confirmed SPX/benchmark equity series is found; otherwise keep the current SPX line until a reliable mapping is available.
- Market State in Research & Backtest should prefer E1R status export, then E1R OOS summary, then general market_state.json as fallback.
- Stage 3.8E-2B should only integrate Summary Comparison first, not curve and market state together.
- Stage 3.8E-2C should fix equity curve after date/equity keys are confirmed.
- Stage 3.8E-2D should fix Market State regime mapping after confirming field names.

## Next

- Stage 3.8E-2B should integrate Summary Comparison only, after reviewing this audit.
- Do not combine summary, curve, and market-state fixes in one patch.

