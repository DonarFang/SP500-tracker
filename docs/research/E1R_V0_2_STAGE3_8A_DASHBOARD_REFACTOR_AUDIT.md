# E1R v0.2 Stage 3.8A Research & Backtest Dashboard Refactor Audit

Generated At: `2026-07-07T12:24:33.562128+00:00`

## Status

- Stage: `B_STAGE_3_8A_RESEARCH_BACKTEST_DASHBOARD_REFACTOR_AUDIT`
- Status: `AUDIT_COMPLETE_NO_SOURCE_CHANGES`
- Main HEAD: `855a443`

## Policy

- Strategy logic changes allowed: `False`
- Only dashboard/display/export-path/JSON-normalization work is allowed.
- E1 and E1R v0.2 remain frozen.

## Target Page Structure

1. Unified Equity Curve — E1 vs E1R v0.2 vs SPX, historical + forward.
2. Strategy Summary Comparison — E1 / E1R v0.2 / SPX in one comparison block.
3. Trade Log — keep trade log; remove Period comparison.
4. Market State — only market/regime context below Trade Log.

## Remove or Hide

- `E1-R Research Summary v0.1 top block` — Legacy research block duplicates/confuses the new E1/E1R comparison structure.
- `Period comparison` — User explicitly wants Trade Log and not Period comparison.
- `Separate E1R v0.2 Market/OOS, 5Y Backtest, Forward/OOS panels` — Standalone appended panels fragment the page.
- `Old text: Main engine migration / OOS tracking not yet completed` — Stale/confusing after Stage 3.5/3.6 integration.
- `E2 Dynamic Exit large note` — E2 is deprecated and should not occupy main Research & Backtest attention.

## Current Dashboard Findings

- Legacy E1-R research summary present: `True`
- Period comparison present: `True`
- Trade log present: `True`
- E1R v0.2 standalone module present: `True`
- Stale migration text present: `True`

## Data Source Map

- `e1_historical_backtest`: available=`True`; primary=`exports/backtest.json`
- `e1_trade_log`: available=`True`; primary=`exports/trade_log.json`
- `e1_forward_oos`: available=`True`; primary=`['exports/oos_summary.json', 'exports/oos_positions.json', 'exports/oos_trades.json', 'exports/oos_equity_curve.json', 'exports/oos_orders.json']`
- `e1r_historical_summary`: available=`True`; primary=`exports/e1r_v0_2_backtest_summary.json`
- `e1r_historical_equity`: available=`True`; primary=`exports/e1r_v0_2_backtest_equity_curve.json`
- `e1r_forward_oos`: available=`True`; primary=`['exports/oos_e1r_v0_2_summary.json', 'exports/oos_e1r_v0_2_positions.json', 'exports/oos_e1r_v0_2_orders.json', 'exports/oos_e1r_v0_2_equity_curve.json', 'exports/oos_e1r_v0_2_sidecar.json', 'exports/oos_e1r_v0_2_sidecar_lifecycle.json', 'exports/oos_e1r_v0_2_sidecar_turnover.json']`
- `market_state`: available=`True`; primary=`['exports/e1r_v0_2_status.json', 'exports/market_regime.json', 'exports/oos_e1r_v0_2_summary.json']`

## Refactor Risks

- Legacy E1-R v0.1 research block is still present and should be removed/hidden in the new layout.
- Period comparison is still present; user explicitly asked to remove it.
- E1R v0.2 panels are currently appended as standalone blocks; they should be merged into unified curve/summary/market-state sections.
- Stale text says main engine migration/OOS tracking not completed; replace with frozen artifact + paper tracking language.

## Stage 3.8B Acceptance Criteria

- Research & Backtest shows one unified E1/E1R/SPX curve block.
- Research & Backtest shows one combined E1 vs E1R vs SPX summary comparison.
- Period comparison is absent.
- Trade log is visible and not buried under period analysis.
- Only market state/context remains below Trade Log.
- E1R v0.2 historical numbers are labeled as frozen research artifacts.
- Forward metrics are labeled as paper tracking and update from OOS exports.
- No E1/E1R strategy logic files are modified.
- No exports/backtest.json mutation is required.

