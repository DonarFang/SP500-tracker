# E1R v0.2 Stage 3.3 Styles Integration Report

Generated At: `2026-07-05T15:20:35.550841+00:00`

## Status

- Stage: `B_STAGE_3_3_STYLES_EVIDENCE_BASED_SCOPED_APPEND`
- Status: `APPENDED_EVIDENCE_BASED_SCOPED_CSS`
- Integrated file: `dashboard/styles.css`
- Policy: `derive_selectors_from_feature_app_js_then_append_matching_non_global_css_rules`

## Evidence Sources

- `feature/dashboard/app.js`
- `feature/dashboard/styles.css`
- `main/dashboard/styles.css`

## Selector Extraction

- Extracted classes: `['e1r-backtest-card', 'e1r-backtest-date', 'e1r-backtest-grid', 'e1r-backtest-label', 'e1r-backtest-main', 'e1r-backtest-note', 'e1r-backtest-value', 'e1r-card', 'e1r-oos-card', 'e1r-oos-date', 'e1r-oos-equity-card', 'e1r-oos-equity-chart-wrap', 'e1r-oos-equity-date', 'e1r-oos-equity-grid', 'e1r-oos-equity-label', 'e1r-oos-equity-main', 'e1r-oos-equity-note', 'e1r-oos-equity-value', 'e1r-oos-grid', 'e1r-oos-label', 'e1r-oos-main', 'e1r-oos-note', 'e1r-oos-value', 'oos-banner']`
- Extracted ids: `['cw-e1r-v02-oos-equity', 'e1r-v02-backtest-card', 'e1r-v02-oos-card', 'e1r-v02-oos-equity-card']`
- Covered selectors after integration: `['.e1r-backtest-card', '.e1r-backtest-date', '.e1r-backtest-grid', '.e1r-backtest-label', '.e1r-backtest-main', '.e1r-backtest-note', '.e1r-backtest-value', '.e1r-card', '.e1r-oos-card', '.e1r-oos-date', '.e1r-oos-equity-card', '.e1r-oos-equity-chart-wrap', '.e1r-oos-equity-date', '.e1r-oos-equity-grid', '.e1r-oos-equity-label', '.e1r-oos-equity-main', '.e1r-oos-equity-note', '.e1r-oos-equity-value', '.e1r-oos-grid', '.e1r-oos-label', '.e1r-oos-main', '.e1r-oos-note', '.e1r-oos-value']`
- Uncovered selectors after integration: `['#cw-e1r-v02-oos-equity', '#e1r-v02-backtest-card', '#e1r-v02-oos-card', '#e1r-v02-oos-equity-card', '.oos-banner']`

## CSS Rule Extraction

- Feature CSS rules parsed: `133`
- Matched E1R/OOS CSS rules: `38`
- Appended CSS rules: `38`
- Already-present CSS rules: `0`

## Boundary

- No dashboard/app.js changes.
- No backtest.py changes.
- No workflow changes.
- No global CSS overwrite.

## Next Stage

Stage 3.4: `dashboard/app.js` clean integration.

