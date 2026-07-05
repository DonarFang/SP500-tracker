# E1R v0.2 Stage 3.4 App.js Integration Report

Generated At: `2026-07-05T15:25:01.098415+00:00`

## Status

- Stage: `B_STAGE_3_4_APP_JS_CLEAN_INTEGRATION`
- Status: `APPENDED_CLEAN_E1R_V0_2_DASHBOARD_MODULE`
- Integrated file: `dashboard/app.js`
- Policy: `do_not_copy_feature_app_js_wholesale_append_isolated_idempotent_e1r_module`

## Evidence

- `feature/dashboard/app.js` was parsed for E1R/OOS evidence.
- `main/dashboard/app.js` was patched without wholesale replacement.
- `main/dashboard/styles.css` was used to select existing scoped class names.

## Feature Evidence Summary

- E1R occurrences: `198`
- OOS occurrences: `78`
- Feature JSON paths: `['exports/e1r_v0_2_backtest_equity_curve.json', 'exports/oos_e1r_v0_2_equity_curve.json']`
- Feature E1R/OOS function names: `['e1rPerfSource', 'fmtOosEquity', 'fmtOosPct', 'getE1RV02BacktestEquity', 'getE1RV02OOSEquity', 'getE1RV02OOSSummary', 'injectE1RV02BacktestEquityUI', 'injectE1RV02BacktestSummaryCard', 'injectE1RV02OOSCard', 'injectE1RV02OOSEquityUI', 'installE1RV02BacktestEquityPatch', 'installE1RV02OOSEquityPatch', 'installE1RV02OOSPatch', 'normalizeE1REquitySeries', 'normalizeOOSEquityRecords', 'oosCard', 'patchRenderForOOS', 'patchRenderForOOSEquity', 'renderE1RResearchPanel', 'renderE1RV02BacktestEquityChart', 'renderE1RV02BacktestSummaryCard', 'renderE1RV02OOSCard', 'renderE1RV02OOSEquityCard', 'renderE1RV02OOSEquityChart', 'sidecarActive']`
- Feature E1R/OOS class tokens: `['e1r-backtest-card', 'e1r-backtest-date', 'e1r-backtest-grid', 'e1r-backtest-label', 'e1r-backtest-main', 'e1r-backtest-note', 'e1r-backtest-value', 'e1r-card', 'e1r-oos-card', 'e1r-oos-date', 'e1r-oos-equity-card', 'e1r-oos-equity-chart-wrap', 'e1r-oos-equity-date', 'e1r-oos-equity-grid', 'e1r-oos-equity-label', 'e1r-oos-equity-main', 'e1r-oos-equity-note', 'e1r-oos-equity-value', 'e1r-oos-grid', 'e1r-oos-label', 'e1r-oos-main', 'e1r-oos-note', 'e1r-oos-value', 'oos-banner']`
- Feature E1R/OOS id tokens: `['cw-e1r-v02-oos-equity', 'e1r-v02-backtest-card', 'e1r-v02-oos-card', 'e1r-v02-oos-equity-card']`

## Runtime Guards

- Idempotent init guard: `window.__E1R_V02_DASHBOARD_INITIALIZED__`.
- Isolated IIFE module: no override of existing dashboard functions.
- Paper tracking only.
- Missing JSON exports render as unavailable instead of crashing.
- No broker/order execution markers are present.

## Boundary

- No dashboard/styles.css changes.
- No backtest.py changes.
- No workflow changes.

## Next Stage

Stage 3.5: main smoke test + dashboard JSON validation.

