# Stage 3.8E-2F-1F-1F Full E1R Daily Sequence After OOS Patch

Generated At: `2026-07-08T08:04:39.208653+00:00`
HEAD: `39da375`

## Status

- Status: `AUDIT_COMPLETE_RUNTIME_CHANGES_REVERTED`
- Source changed: `False`
- Workflow changed: `False`
- Dashboard changed: `False`
- Runtime changes committed: `False`

## Classification

- all_scripts_succeeded: `True`
- touches_e1_files: `[]`
- official_orders_preserved: `True`
- official_positions_preserved: `True`
- kickoff_semantics_preserved: `True`
- paper_accounting_preserved: `True`
- safe_to_integrate_workflow_as_is: `True`

## Before Snapshot

- orders_count: `10`
- positions_count: `10`
- buy_orders: `10`
- position_weight_sum: `0.24999999999999997`
- summary_tracking_status: `KICKOFF_READY`
- summary_official_kickoff_date: `None`
- summary_forward_start_date: `None`
- summary_execution_status: `PAPER_POSITIONS_READY_KICKOFF_PENDING`
- summary_open_positions_count: `10`
- summary_paper_orders_count: `10`
- summary_gross_exposure: `0.24999999999999997`
- summary_cash: `75000.0`
- summary_market_value: `24999.999999999996`
- summary_portfolio_value: `100000.0`
- state_positions_count: `10`
- state_official_kickoff_date: `None`

## After Snapshot

- orders_count: `10`
- positions_count: `10`
- buy_orders: `10`
- position_weight_sum: `0.24999999999999997`
- summary_tracking_status: `KICKOFF_READY`
- summary_official_kickoff_date: `None`
- summary_forward_start_date: `None`
- summary_execution_status: `PAPER_POSITIONS_READY_KICKOFF_PENDING`
- summary_open_positions_count: `10`
- summary_paper_orders_count: `10`
- summary_gross_exposure: `0.24999999999999997`
- summary_cash: `75000.0`
- summary_market_value: `24999.999999999996`
- summary_portfolio_value: `100000.0`
- state_positions_count: `10`
- state_official_kickoff_date: `None`

## Sequence

1. `scripts/export_e1r_v0_2_status.py`
2. `scripts/run_e1r_v0_2_oos.py`
3. `scripts/run_e1r_v0_2_oos_equity.py`
4. `scripts/export_e1r_v0_2_targets_preview.py`
5. `scripts/export_e1r_v0_2_orders_positions_preview.py`
6. `scripts/run_e1r_v0_2_forward_performance.py`

## Changed Watch Files

- `data/oos/e1r_v0_2_portfolio_state.json`
- `data/oos/e1r_v0_2_events.jsonl`
- `data/oos/e1r_v0_2_run_history.jsonl`
- `exports/e1r_v0_2_status.json`
- `exports/oos_e1r_v0_2_summary.json`
- `exports/oos_e1r_v0_2_equity_curve.json`
- `exports/oos_e1r_v0_2_targets.json`
- `exports/oos_e1r_v0_2_orders_preview.json`
- `exports/oos_e1r_v0_2_positions_preview.json`
- `exports/oos_e1r_v0_2_sidecar.json`
- `exports/oos_e1r_v0_2_sidecar_lifecycle.json`
- `exports/oos_e1r_v0_2_sidecar_turnover.json`

## Next

- 1F-1G: integrate E1R runner sequence into daily workflow if safe.
- 1G: map E1R forward fields into Summary.
- 2C: map E1R forward equity curve.

