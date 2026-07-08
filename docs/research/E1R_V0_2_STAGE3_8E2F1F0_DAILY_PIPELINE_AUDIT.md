# Stage 3.8E-2F-1F-0 Daily Pipeline Integration Audit

Generated At: `2026-07-08T07:13:45.797502+00:00`
HEAD: `5af4432`

## Status

- Status: `AUDIT_COMPLETE_NO_SOURCE_CHANGES`
- Source changed: `False`
- Workflow changed: `False`
- Exports changed: `False`
- State changed: `False`
- Dashboard changed: `False`

## E1R Scripts Present In Workflow

- `run_e1r_v0_2_oos.py`: `True`
- `run_e1r_v0_2_oos_equity.py`: `False`
- `export_e1r_v0_2_targets_preview.py`: `False`
- `export_e1r_v0_2_orders_positions_preview.py`: `False`
- `run_e1r_v0_2_forward_performance.py`: `False`
- `export_e1r_v0_2_status.py`: `False`

## Recommended E1R Daily Sequence

1. `python3 scripts/export_e1r_v0_2_status.py`
2. `python3 scripts/run_e1r_v0_2_oos.py`
3. `python3 scripts/run_e1r_v0_2_oos_equity.py`
4. `python3 scripts/export_e1r_v0_2_targets_preview.py`
5. `python3 scripts/export_e1r_v0_2_orders_positions_preview.py`
6. `python3 scripts/run_e1r_v0_2_forward_performance.py`

## Next Sequence

- 1F-1: integrate E1R daily runner sequence.
- 1G: map E1R forward fields into Summary.
- 2C: map E1R forward equity curve.

## File Hit Summary

- `.github/workflows/update.yml` exists=`True` hits=`4`
- `run_oos.py` exists=`True` hits=`6`
- `scripts/run_e1r_v0_2_oos.py` exists=`True` hits=`17`
- `scripts/run_e1r_v0_2_oos_equity.py` exists=`True` hits=`8`
- `scripts/export_e1r_v0_2_targets_preview.py` exists=`True` hits=`4`
- `scripts/export_e1r_v0_2_orders_positions_preview.py` exists=`True` hits=`1`
- `scripts/run_e1r_v0_2_forward_performance.py` exists=`True` hits=`1`
- `scripts/export_e1r_v0_2_status.py` exists=`True` hits=`2`

