# E1R v0.2 Stage 2 High-Risk File Review

Generated At: `2026-07-05T14:56:15.386938+00:00`

## 1. Summary

- Stage: `B_STAGE_2_HIGH_RISK_REVIEW_AUDIT`
- Feature: `/Users/dongfang/Downloads/sp500-tracker-5y` / `feature/e1-5y-data` / `5f6063e`
- Main: `/Users/dongfang/Downloads/sp500-tracker-v13` / `main` / `2c884bf`
- Changed high-risk files: `4`
- Manual integration required: `3`

## 2. File Review Table

| Path | Risk | Recommendation | Same | Diff Lines | Diff File |
|---|---|---|---:|---:|---|
| `src/engine/backtest.py` | `HIGH` | `MANUAL_INTEGRATION_REQUIRED` | `False` | `766` | `docs/research/stage2_high_risk_diffs/src__engine__backtest_py.diff` |
| `dashboard/app.js` | `HIGH` | `CLEAN_INTEGRATION_RECOMMENDED` | `False` | `1328` | `docs/research/stage2_high_risk_diffs/dashboard__app_js.diff` |
| `dashboard/styles.css` | `MEDIUM` | `SELECTIVE_COPY_OR_APPEND_AFTER_REVIEW` | `False` | `403` | `docs/research/stage2_high_risk_diffs/dashboard__styles_css.diff` |
| `.github/workflows/update.yml` | `HIGH` | `MANUAL_WORKFLOW_PATCH_REQUIRED` | `False` | `10` | `docs/research/stage2_high_risk_diffs/_github__workflows__update_yml.diff` |

## 3. Recommended Stage 2 Order

1. `.github/workflows/update.yml` — controlled patch only.
2. `src/engine/backtest.py` — extract E1R v0.2 integration only; preserve frozen E1/E2.
3. `dashboard/styles.css` — append scoped E1R v0.2 CSS blocks only.
4. `dashboard/app.js` — clean first-class integration preferred; avoid wrapper-on-wrapper debt.

## 4. Do Not Do

- Do not blindly overwrite `dashboard/app.js`.
- Do not blindly overwrite `src/engine/backtest.py`.
- Do not blindly overwrite `.github/workflows/update.yml`.
- Do not merge the full feature branch into main.

## 5. Detailed Notes

### `src/engine/backtest.py`

- Risk: `HIGH`
- Recommendation: `MANUAL_INTEGRATION_REQUIRED`
- Reason: Core backtest file exists in main and feature; replacing it blindly may affect frozen E1/E2 results.
- Expected action: Extract only E1R v0.2 variant integration after confirming E1 frozen results are unchanged.
- Diff file: `docs/research/stage2_high_risk_diffs/src__engine__backtest_py.diff`

### `dashboard/app.js`

- Risk: `HIGH`
- Recommendation: `CLEAN_INTEGRATION_RECOMMENDED`
- Reason: Feature dashboard/app.js contains accumulated safe-wrapper UI patches. Main should ideally receive a clean first-class integration.
- Expected action: Review feature diff and port E1R v0.2 UI into explicit render/load functions rather than blindly replacing main app.js.
- Diff file: `docs/research/stage2_high_risk_diffs/dashboard__app_js.diff`

### `dashboard/styles.css`

- Risk: `MEDIUM`
- Recommendation: `SELECTIVE_COPY_OR_APPEND_AFTER_REVIEW`
- Reason: CSS additions are lower risk than app.js but can still affect layout globally.
- Expected action: Append only E1R v0.2 scoped CSS blocks after confirming selectors are scoped and do not override global layout.
- Diff file: `docs/research/stage2_high_risk_diffs/dashboard__styles_css.diff`

### `.github/workflows/update.yml`

- Risk: `HIGH`
- Recommendation: `MANUAL_WORKFLOW_PATCH_REQUIRED`
- Reason: Workflow controls daily production update. Blind overwrite can break existing deployment cadence.
- Expected action: Patch only E1R v0.2 OOS runner step after existing update/export steps; ensure failures are controlled.
- Diff file: `docs/research/stage2_high_risk_diffs/_github__workflows__update_yml.diff`

