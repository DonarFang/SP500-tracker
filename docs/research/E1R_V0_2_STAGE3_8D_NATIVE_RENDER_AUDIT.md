# Stage 3.8D Native Research & Backtest Render Audit

Generated At: `2026-07-07T12:53:14.952142+00:00`
Main HEAD: `fb7cbf4`

## Status

- Status: `AUDIT_COMPLETE_NO_DASHBOARD_SOURCE_CHANGES`
- Strategy logic changed: `False`
- Dashboard source changed: `False`
- Exports changed: `False`
- Stage 3.8B markers present: `False`

## Goal

Locate the native Research & Backtest render path before doing any tab-scoped refactor.

## Likely Render Functions

- `e1rRenderOosEquity` (function) line `1201`, score `20`
- `e1rRenderBacktest` (function) line `1161`, score `17`
- `renderE1RResearchPanel` (function) line `194`, score `15`
- `e1rRenderStatus` (function) line `1123`, score `13`
- `e1rRenderUnavailable` (function) line `1114`, score `11`
- `e1rRenderAll` (function) line `1240`, score `11`
- `e1rRenderAll` (async_function) line `1240`, score `11`
- `renderStockPreviewChart` (function) line `47`, score `6`
- `buildEquityDateLabels` (const_arrow) line `825`, score `6`
- `fetchResearchJ` (function) line `134`, score `4`
- `fetchResearchJ` (async_function) line `134`, score `4`
- `render` (function) line `267`, score `3`

## Key Code Neighborhoods

- `research_backtest_title`: line(s) 3
- `period_comparison`: line(s) 755
- `trade_log`: line(s) 794
- `equity_curve`: line(s) 749
- `e1_frozen_summary`: line(s) 565
- `e1r_v02`: line(s) 1126
- `market_state`: not found

## Export Summaries

- `exports/backtest.json`: exists=`True`, valid=`True`, contains={'E1': True, 'E1R_v0_2': False, 'SPX': True, 'trade_like': True, 'equity_like': True, 'market_state_like': True}
- `exports/trade_log.json`: exists=`True`, valid=`True`, contains={'E1': False, 'E1R_v0_2': False, 'SPX': False, 'trade_like': True, 'equity_like': False, 'market_state_like': False}
- `exports/e1r_v0_2_status.json`: exists=`True`, valid=`True`, contains={'E1': False, 'E1R_v0_2': True, 'SPX': True, 'trade_like': True, 'equity_like': False, 'market_state_like': True}
- `exports/e1r_v0_2_backtest_summary.json`: exists=`True`, valid=`True`, contains={'E1': False, 'E1R_v0_2': True, 'SPX': True, 'trade_like': False, 'equity_like': False, 'market_state_like': True}
- `exports/e1r_v0_2_backtest_equity_curve.json`: exists=`True`, valid=`True`, contains={'E1': False, 'E1R_v0_2': True, 'SPX': True, 'trade_like': True, 'equity_like': True, 'market_state_like': True}
- `exports/oos_summary.json`: exists=`True`, valid=`True`, contains={'E1': False, 'E1R_v0_2': False, 'SPX': False, 'trade_like': False, 'equity_like': False, 'market_state_like': False}
- `exports/oos_equity_curve.json`: exists=`True`, valid=`True`, contains={'E1': True, 'E1R_v0_2': False, 'SPX': False, 'trade_like': False, 'equity_like': True, 'market_state_like': False}
- `exports/oos_trades.json`: exists=`True`, valid=`True`, contains={'E1': True, 'E1R_v0_2': False, 'SPX': False, 'trade_like': False, 'equity_like': False, 'market_state_like': False}
- `exports/oos_orders.json`: exists=`True`, valid=`True`, contains={'E1': True, 'E1R_v0_2': False, 'SPX': False, 'trade_like': True, 'equity_like': False, 'market_state_like': False}
- `exports/oos_e1r_v0_2_summary.json`: exists=`True`, valid=`True`, contains={'E1': False, 'E1R_v0_2': True, 'SPX': False, 'trade_like': False, 'equity_like': True, 'market_state_like': True}
- `exports/oos_e1r_v0_2_equity_curve.json`: exists=`True`, valid=`True`, contains={'E1': False, 'E1R_v0_2': True, 'SPX': False, 'trade_like': False, 'equity_like': True, 'market_state_like': True}
- `exports/oos_e1r_v0_2_orders.json`: exists=`True`, valid=`True`, contains={'E1': False, 'E1R_v0_2': True, 'SPX': False, 'trade_like': False, 'equity_like': False, 'market_state_like': True}
- `exports/oos_e1r_v0_2_positions.json`: exists=`True`, valid=`True`, contains={'E1': False, 'E1R_v0_2': True, 'SPX': False, 'trade_like': False, 'equity_like': False, 'market_state_like': True}
- `exports/market_state.json`: exists=`True`, valid=`True`, contains={'E1': False, 'E1R_v0_2': False, 'SPX': True, 'trade_like': False, 'equity_like': False, 'market_state_like': False}

## Stage 3.8E Rules

- Do not append another global runtime module.
- Do not use global auto-init, global click listeners, MutationObserver, or hideLegacyBlocks.
- Patch the native Research & Backtest render path only after confirming the exact render function and tab container from this audit.
- Keep existing 5-tab framework intact.
- Remove Period comparison only inside the Research & Backtest render output.
- Reuse existing chart/render utilities if present; do not introduce a competing global rendering system.
- In Stage 3.8E, change should be small and line-targeted, ideally one render function plus minimal CSS.
- After Stage 3.8E, add cache-busting version if app.js/styles.css changes.

## Stage 3.8E Acceptance Criteria

- The original 5 tabs remain visible.
- Only Research & Backtest tab content changes.
- Unified E1/E1R/SPX curve appears inside Research & Backtest.
- E1 vs E1R summary comparison appears inside Research & Backtest.
- Period comparison is absent from Research & Backtest.
- Trade Log remains visible.
- Market State appears below Trade Log.
- No E1/E1R strategy logic files are modified.
- No exports/backtest.json mutation is required.

## Next

`Stage 3.8E tab-scoped Research & Backtest render refactor`, only after reviewing this audit.

