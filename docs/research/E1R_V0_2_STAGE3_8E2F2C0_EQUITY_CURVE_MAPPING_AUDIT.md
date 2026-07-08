# Stage 3.8E-2F-2C-0 E1R Forward Equity Curve Mapping Audit

Generated At: `2026-07-08T08:30:57.833791+00:00`
HEAD: `2e1be15`

## Status

- Status: `AUDIT_COMPLETE_NO_SOURCE_CHANGES`
- Source changed: `False`
- Dashboard changed: `False`
- Exports changed: `False`
- State changed: `False`
- Workflow changed: `False`

## Readiness

- e1r_curve_exists: `True`
- e1r_curve_json_valid: `True`
- e1r_curve_row_count: `1`
- e1r_curve_has_date: `True`
- e1r_curve_has_equity: `True`
- dashboard_fetches_e1r_forward_curve: `True`
- dashboard_mentions_e1r_curve_var: `True`
- ready_for_equity_curve_mapping_patch: `True`

## E1R Curve

- exists: `True`
- json_valid: `True`
- type: `list`
- row_count: `1`
- sample_keys: `['backfill_start_date', 'cash', 'core_exposure', 'date', 'drawdown_pct', 'equity', 'forward_return_pct', 'gross_exposure', 'market_state', 'market_value', 'official_kickoff_date', 'portfolio_value', 'regime', 'shadow_start_date', 'sidecar_exposure', 'strategy_id', 'strategy_indexed', 'subclass', 'tracking_status', 'version']`
- has_date: `True`
- has_equity: `True`

## E1R Summary Snapshot

- tracking_status: `KICKOFF_READY`
- execution_status: `PAPER_POSITIONS_READY_KICKOFF_PENDING`
- portfolio_value: `100000.0`
- forward_return_pct: `0.0`
- gross_exposure: `0.24999999999999997`
- open_positions_count: `10`

## Next

- 3.8E-2F-2C-1: patch dashboard equity curve mapping.

