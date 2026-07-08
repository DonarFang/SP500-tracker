# Stage 3.8E-2F-1F-1D Pinpoint E1R Reset Script

Generated At: `2026-07-08T07:52:38.470658+00:00`
HEAD: `1897746`

## Status

- Status: `AUDIT_COMPLETE_RUNTIME_RESTORED`

## Baseline

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
- state_positions_count: `10`
- state_official_kickoff_date: `None`

## Dangerous Scripts

- `scripts/run_e1r_v0_2_oos.py`

## Reset Scripts

- `scripts/run_e1r_v0_2_oos.py`

## Step Summary

- `scripts/export_e1r_v0_2_status.py` dangerous=`[]` clears_orders=`False` clears_positions=`False` sets_kickoff=`False`
- `scripts/run_e1r_v0_2_oos.py` dangerous=`True` clears_orders=`True` clears_positions=`True` sets_kickoff=`False`
- `scripts/run_e1r_v0_2_oos_equity.py` dangerous=`[]` clears_orders=`False` clears_positions=`False` sets_kickoff=`False`
- `scripts/export_e1r_v0_2_targets_preview.py` dangerous=`[]` clears_orders=`False` clears_positions=`False` sets_kickoff=`False`
- `scripts/export_e1r_v0_2_orders_positions_preview.py` dangerous=`[]` clears_orders=`False` clears_positions=`False` sets_kickoff=`False`
- `scripts/run_e1r_v0_2_forward_performance.py` dangerous=`[]` clears_orders=`False` clears_positions=`False` sets_kickoff=`False`

## Next

- Patch the exact reset script(s).
- Rerun full daily sequence dry-run.
- Only then integrate workflow.

