# E1R v0.2 Port Readiness Audit

Generated At: `2026-07-05T14:49:06.939592+00:00`

## 1. Worktree Status

| Worktree | Path | Branch | HEAD | Clean |
|---|---|---:|---:|---:|
| Feature | `/Users/dongfang/Downloads/sp500-tracker-5y` | `feature/e1-5y-data` | `b8787ad` | `False` |
| Main | `/Users/dongfang/Downloads/sp500-tracker-v13` | `main` | `5730bc6` | `True` |

## 2. Summary

- Recommendation: `NOT_READY_REVIEW_STATUS_OR_MISSING_FILES`
- Ready for controlled copy: `False`
- Missing required files in feature: `0`
- Required files missing in main: `11`
- Required files changed vs main: `4`
- Manual review files: `4`

## 3. Required Files

| Path | Feature | Main | Same | Recommendation |
|---|---:|---:|---:|---|
| `src/engine/e1r_sidecar_sleeve.py` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `src/engine/e1r_composer.py` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `src/engine/backtest.py` | `True` | `True` | `False` | `MANUAL_REVIEW_BEFORE_COPY` |
| `scripts/export_e1r_v0_2_status.py` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `scripts/run_e1r_v0_2_oos.py` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `scripts/run_e1r_v0_2_oos_equity.py` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `scripts/run_e1r_v0_2_sidecar_lifecycle.py` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `scripts/export_e1r_v0_2_backtest_equity.py` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `dashboard/app.js` | `True` | `True` | `False` | `MANUAL_REVIEW_BEFORE_COPY` |
| `dashboard/styles.css` | `True` | `True` | `False` | `MANUAL_REVIEW_BEFORE_COPY` |
| `.github/workflows/update.yml` | `True` | `True` | `False` | `MANUAL_REVIEW_BEFORE_COPY` |
| `docs/research/E1R_V0_2_IMPLEMENTATION_MANIFEST.md` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `docs/research/E1R_V0_2_OOS_2B_2_SIDECAR_MTM_SPEC.md` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `docs/research/E1R_V0_2_UI_OOS_INTEGRATION_AUDIT.md` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `docs/research/E1R_V0_2_PORT_TO_MAIN_PLAN.md` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |

## 4. Lightweight Exports

| Path | Feature | Main | Same | Recommendation |
|---|---:|---:|---:|---|
| `exports/e1r_v0_2_status.json` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `exports/oos_e1r_v0_2_summary.json` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `exports/oos_e1r_v0_2_sidecar.json` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `exports/oos_e1r_v0_2_positions.json` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `exports/oos_e1r_v0_2_orders.json` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `exports/oos_e1r_v0_2_equity_curve.json` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `exports/oos_e1r_v0_2_sidecar_lifecycle.json` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `exports/oos_e1r_v0_2_sidecar_turnover.json` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `exports/e1r_v0_2_backtest_summary.json` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |
| `exports/e1r_v0_2_backtest_equity_curve.json` | `True` | `False` | `False` | `COPY_NEW_TO_MAIN` |

## 5. Heavy / Legacy Exports — Do Not Blindly Copy

- `exports/backtest.json`: feature_exists=`True`, main_exists=`True`, same_content=`True`
- `exports/equity_curve.json`: feature_exists=`True`, main_exists=`True`, same_content=`True`
- `exports/trade_log.json`: feature_exists=`True`, main_exists=`True`, same_content=`True`
- `exports/portfolio_backtest.json`: feature_exists=`True`, main_exists=`True`, same_content=`True`
- `exports/action_forward_returns.json`: feature_exists=`True`, main_exists=`True`, same_content=`True`

## 6. Manual Review Required

- `src/engine/backtest.py`
- `dashboard/app.js`
- `dashboard/styles.css`
- `.github/workflows/update.yml`

## 7. Next Step

If both worktrees are clean and no required feature files are missing, proceed with a controlled copy into v13/main.
Do not blindly merge the full feature branch into main.

