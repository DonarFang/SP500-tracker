# Stage 3.8E-2F-1F-1A E1R Daily Sequence Dry-run Audit

Generated At: `2026-07-08T07:34:57.829478+00:00`
HEAD: `d8b7375`

## Status

- Status: `AUDIT_COMPLETE_RUNTIME_CHANGES_REVERTED`
- Source changed: `False`
- Workflow changed: `False`
- Dashboard changed: `False`
- Runtime changes committed: `False`

## Classification

- all_scripts_succeeded: `True`
- touches_e1_files: `[]`
- official_orders_preserved: `False`
- official_positions_preserved: `False`
- safe_to_integrate_workflow_as_is: `False`
- needs_forward_performance_preservation_fix: `True`

## Before Snapshot

- orders_count: `10`
- positions_count: `10`
- buy_orders: `10`
- position_weight_sum: `0.24999999999999997`
- summary_tracking_status: `KICKOFF_READY`
- summary_official_kickoff_date: `None`
- summary_execution_status: `PAPER_POSITIONS_READY_KICKOFF_PENDING`
- summary_open_positions_count: `10`
- state_positions_count: `10`

## After Snapshot

- orders_count: `0`
- positions_count: `0`
- buy_orders: `0`
- position_weight_sum: `0`
- summary_tracking_status: `KICKOFF_READY`
- summary_official_kickoff_date: `2026-06-18`
- summary_execution_status: `NO_ORDER_ENGINE_WIRED_YET`
- summary_open_positions_count: `0`
- state_positions_count: `0`

## Sequence

1. `scripts/export_e1r_v0_2_status.py`
2. `scripts/run_e1r_v0_2_oos.py`
3. `scripts/run_e1r_v0_2_oos_equity.py`
4. `scripts/export_e1r_v0_2_targets_preview.py`
5. `scripts/export_e1r_v0_2_orders_positions_preview.py`
6. `scripts/run_e1r_v0_2_forward_performance.py`

## Script Results

- `scripts/export_e1r_v0_2_status.py` returncode=`0` stdout_tail=`Wrote /Users/dongfang/Downloads/sp500-tracker-v13/exports/e1r_v0_2_status.json status_date: 2026-06-18 e1r_market_state: UPTREND regime: UPTREND subclass: None core.active: True sidecar.active: False sidecar.selected_count: 0 ` stderr_tail=``
- `scripts/run_e1r_v0_2_oos.py` returncode=`0` stdout_tail=`date: 2026-06-18 previous_date: None market_state: UPTREND sidecar_active: False lifecycle_status: NO_PREVIOUS_RECORD previous_count: 0 current_count: 0 entered_count: 0 exited_count: 0 one_way_turnover: 0.0 wrote: exports/oos_e1r_v0_2_sidecar_lifecycle.json wrote: exports/oos_e1r_v0_2_sidecar_turnover.json   exports/oos_e1r_v0_2_sidecar_lifecycle.json   exports/oos_e1r_v0_2_sidecar_turnover.json ` stderr_tail=``
- `scripts/run_e1r_v0_2_oos_equity.py` returncode=`0` stdout_tail=`E1R v0.2 OOS-2B equity export complete status_date: 2026-06-18 market_state: UPTREND core_active: True sidecar_active: False sidecar_selected_count: 0 core_equity: 75255.2 sidecar_equity: 100000.0 combined_equity: 75255.2 row_count: 1 update_mode: UPDATED_EXISTING_DATE wrote: exports/oos_e1r_v0_2_equity_curve.json ` stderr_tail=``
- `scripts/export_e1r_v0_2_targets_preview.py` returncode=`0` stdout_tail=`E1R target extraction preview complete status_date: 2026-06-18 tracking_status: KICKOFF_READY official_kickoff_date: None core_targets: 10 sidecar_targets: 0 all_targets: 10 core_weight_sum: 0.24999999999999997 sidecar_weight_sum: 0 total_weight_sum: 0.24999999999999997 wrote: exports/oos_e1r_v0_2_targets.json ` stderr_tail=``
- `scripts/export_e1r_v0_2_orders_positions_preview.py` returncode=`0` stdout_tail=`rs/positions preview complete status_date: 2026-06-18 tracking_status: KICKOFF_READY official_kickoff_date: None targets: 10 orders: 10 positions: 10 buy_orders: 0 add_orders: 0 hold_orders: 10 reduce_orders: 0 exit_orders: 0 positions_weight_sum: 0.24999999999999997 orders_abs_delta_weight_sum: 0.0 wrote: exports/oos_e1r_v0_2_orders_preview.json wrote: exports/oos_e1r_v0_2_positions_preview.json ` stderr_tail=``
- `scripts/run_e1r_v0_2_forward_performance.py` returncode=`0` stdout_tail=`-06-18 official_kickoff_date: 2026-06-18 tracking_status: KICKOFF_READY portfolio_value: 100000.0 forward_return_pct: 0.0 max_drawdown_pct: 0.0 sharpe_ratio: None gross_exposure: 0.25 wrote: data/oos/e1r_v0_2_portfolio_state.json wrote: exports/oos_e1r_v0_2_summary.json wrote: exports/oos_e1r_v0_2_equity_curve.json wrote: exports/oos_e1r_v0_2_positions.json wrote: exports/oos_e1r_v0_2_orders.json ` stderr_tail=``

## Changed Watch Files

- `data/oos/e1r_v0_2_portfolio_state.json`
- `data/oos/e1r_v0_2_events.jsonl`
- `data/oos/e1r_v0_2_run_history.jsonl`
- `exports/e1r_v0_2_status.json`
- `exports/oos_e1r_v0_2_summary.json`
- `exports/oos_e1r_v0_2_equity_curve.json`
- `exports/oos_e1r_v0_2_orders.json`
- `exports/oos_e1r_v0_2_positions.json`
- `exports/oos_e1r_v0_2_targets.json`
- `exports/oos_e1r_v0_2_orders_preview.json`
- `exports/oos_e1r_v0_2_positions_preview.json`
- `exports/oos_e1r_v0_2_sidecar.json`
- `exports/oos_e1r_v0_2_sidecar_lifecycle.json`
- `exports/oos_e1r_v0_2_sidecar_turnover.json`

## Next Decision

Proceed to workflow integration if safe_to_integrate_workflow_as_is is true; otherwise patch the forward performance layer before touching GitHub Actions.

