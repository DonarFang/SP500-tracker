# E1R v0.2 Stage 3.5 Main Smoke Test Report

Generated At: `2026-07-05T15:45:29.057461+00:00`

## Status

- Stage: `B_STAGE_3_5_MAIN_SMOKE_TEST_AND_DASHBOARD_JSON_VALIDATION`
- Status: `PASS_WITH_DISCOVERED_FROZEN_BACKTEST_ARTIFACTS`
- Main HEAD before test: `1638b6f`

## Validation Summary

- Python compile targets passed: `8`
- OOS export commands passed: `4`
- Frozen backtest artifacts validated: `2`
- Export JSON files validated: `10`
- Dashboard JSON references validated: `10`

## Explicit Skip

- `python3 scripts/export_e1r_v0_2_backtest_equity.py` was not used as a regeneration command because main `exports/backtest.json` does not contain E1R v0.1/v0.2 variants.
- Instead, feature artifacts were recursively discovered, normalized, validated, and committed as frozen E1R v0.2 5Y research artifacts.

## Selected Frozen Artifact Sources

- Equity source: `exports/e1r_candidates.json` at `$.candidates`
- Equity rows: `8819`
- Summary source: `exports/e1r_v0_2_backtest_summary.json` at `$.v0_2`

## Export Files

- `exports/e1r_v0_2_status.json`: valid_json=`True`, type=`dict`, size=`1580` bytes
- `exports/oos_e1r_v0_2_summary.json`: valid_json=`True`, type=`dict`, size=`873` bytes
- `exports/oos_e1r_v0_2_sidecar.json`: valid_json=`True`, type=`dict`, size=`507` bytes
- `exports/oos_e1r_v0_2_positions.json`: valid_json=`True`, type=`dict`, size=`446` bytes
- `exports/oos_e1r_v0_2_orders.json`: valid_json=`True`, type=`dict`, size=`255` bytes
- `exports/oos_e1r_v0_2_equity_curve.json`: valid_json=`True`, type=`dict`, size=`2632` bytes
- `exports/oos_e1r_v0_2_sidecar_lifecycle.json`: valid_json=`True`, type=`dict`, size=`2557` bytes
- `exports/oos_e1r_v0_2_sidecar_turnover.json`: valid_json=`True`, type=`dict`, size=`1924` bytes
- `exports/e1r_v0_2_backtest_summary.json`: valid_json=`True`, type=`dict`, size=`941` bytes
- `exports/e1r_v0_2_backtest_equity_curve.json`: valid_json=`True`, type=`dict`, size=`16004713` bytes

## Dashboard Checks

- App marker present: `True`
- Missing app JSON paths: `[]`
- Forbidden module hits: `[]`
- Missing CSS terms: `[]`

## Workflow Checks

- Contains E1R OOS script: `True`
- Contains continue-on-error: `True`

## Next

Manual browser review of GitHub Pages dashboard after deployment refresh.

