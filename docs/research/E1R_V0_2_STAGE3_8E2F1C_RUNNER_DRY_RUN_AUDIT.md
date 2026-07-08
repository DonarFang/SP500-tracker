# Stage 3.8E-2F-1C E1R Runner Dry-run Audit

Generated At: `2026-07-08T06:44:53.415831+00:00`
HEAD: `fd19a9e`

## Status

- Status: `AUDIT_COMPLETE_EXPORT_CHANGES_REVERTED`
- Source changed: `False`
- Dashboard changed: `False`
- Strategy logic changed: `False`
- Export changes committed: `False`
- Runtime export changes reverted: `True`

## Classification

- All scripts succeeded: `True`
- Changed watch files: `6`
- Touches E1 state: `False`
- Touches E1 exports: `False`
- Implementation readiness: `CAN_EXTEND_EXISTING_RUNNER_WITH_GUARDS`

## Script Results

- `scripts/run_e1r_v0_2_oos.py` returncode=`0`
  - stdout tail: `exports/oos_e1r_v0_2_equity_curve.json E1R v0.2 OOS-2B.3 sidecar lifecycle/turnover export complete date: 2026-06-18 previous_date: None market_state: UPTREND sidecar_active: False lifecycle_status: NO_PREVIOUS_RECORD previous_count: 0 current_count: 0 entered_count: 0 exited_count: 0 one_way_turnover: 0.0 wrote: exports/oos_e1r_v0_2_sidecar_lifecycle.json wrote: exports/oos_e1r_v0_2_sidecar_turnover.json   exports/oos_e1r_v0_2_sidecar_lifecycle.json   exports/oos_e1r_v0_2_sidecar_turnover.json `
  - stderr tail: ``
- `scripts/run_e1r_v0_2_oos_equity.py` returncode=`0`
  - stdout tail: `E1R v0.2 OOS-2B equity export complete status_date: 2026-06-18 market_state: UPTREND core_active: True sidecar_active: False sidecar_selected_count: 0 core_equity: 100000.0 sidecar_equity: 100000.0 combined_equity: 100000.0 row_count: 1 update_mode: UPDATED_EXISTING_DATE wrote: exports/oos_e1r_v0_2_equity_curve.json `
  - stderr tail: ``
- `scripts/export_e1r_v0_2_status.py` returncode=`0`
  - stdout tail: `Wrote /Users/dongfang/Downloads/sp500-tracker-v13/exports/e1r_v0_2_status.json status_date: 2026-06-18 e1r_market_state: UPTREND regime: UPTREND subclass: None core.active: True sidecar.active: False sidecar.selected_count: 0 `
  - stderr tail: ``

## Changed Watch Files

- `exports/oos_e1r_v0_2_summary.json` before_exists=`True` after_exists=`True` before_size=`873` after_size=`873`
- `exports/oos_e1r_v0_2_equity_curve.json` before_exists=`True` after_exists=`True` before_size=`2632` after_size=`2632`
- `exports/oos_e1r_v0_2_orders.json` before_exists=`True` after_exists=`True` before_size=`255` after_size=`255`
- `exports/oos_e1r_v0_2_positions.json` before_exists=`True` after_exists=`True` before_size=`446` after_size=`446`
- `exports/oos_e1r_v0_2_sidecar.json` before_exists=`True` after_exists=`True` before_size=`507` after_size=`507`
- `exports/e1r_v0_2_status.json` before_exists=`True` after_exists=`True` before_size=`1580` after_size=`1580`

## Git Status After Script Run

- ` M exports/e1r_v0_2_status.json`
- ` M exports/oos_e1r_v0_2_equity_curve.json`
- ` M exports/oos_e1r_v0_2_orders.json`
- ` M exports/oos_e1r_v0_2_positions.json`
- ` M exports/oos_e1r_v0_2_sidecar.json`
- ` M exports/oos_e1r_v0_2_sidecar_lifecycle.json`
- ` M exports/oos_e1r_v0_2_sidecar_turnover.json`
- ` M exports/oos_e1r_v0_2_summary.json`

## Decision Rules

- `CAN_EXTEND_EXISTING_RUNNER_WITH_GUARDS`: Existing E1R scripts run and stay isolated from E1 state/exports; implementation can extend them.
- `NEEDS_CLEAN_RUNNER_OR_ISOLATION_BEFORE_IMPLEMENTATION`: Existing scripts fail or touch E1 files; implement isolation first or create a clean E1R runner.

