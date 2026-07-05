# E1R v0.2 Stage 3.6 Dashboard Export Path Fix Report

Generated At: `2026-07-05T15:53:10.277600+00:00`

## Status

- Stage: `B_STAGE_3_6_DASHBOARD_E1R_EXPORT_PATH_FIX`
- Status: `PATCHED_E1R_DASHBOARD_EXPORT_PATHS`
- File: `dashboard/app.js`
- Replace count: `10`

## Root Cause

`dashboard/app.js` used `exports/...` from a page located under `/dashboard/`, so GitHub Pages resolved the requests to `/dashboard/exports/...`, causing 404.

## Fix

Changed E1R v0.2 module fetch paths to `../exports/...`.

## Boundary

- Only `dashboard/app.js` modified.
- No export JSON files modified.
- No research data modified.
- No engine/backtest/workflow files modified.

