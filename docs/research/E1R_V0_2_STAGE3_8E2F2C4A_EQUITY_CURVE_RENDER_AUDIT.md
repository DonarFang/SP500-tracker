# Stage 3.8E-2F-2C-4A Equity Curve Render Audit

Generated At: `2026-07-08T10:03:45.050820+00:00`

## Status

- Status: `AUDIT_COMPLETE_NO_SOURCE_CHANGES`
- Dashboard changed: `False`
- Exports changed: `False`
- State changed: `False`
- Workflow changed: `False`

## File Summaries

- `e1_backtest`
  - exists: `True`
  - json_valid: `True`
  - row_count: `0`
  - sample_keys: ``
- `e1_oos_equity`
  - exists: `True`
  - json_valid: `True`
  - row_count: `12`
  - sample_keys: `cash, date, equity, holdings_value, n_positions, source`
- `e1r_backtest_summary`
  - exists: `True`
  - json_valid: `True`
  - row_count: `0`
  - sample_keys: ``
- `e1r_backtest_equity`
  - exists: `True`
  - json_valid: `True`
  - row_count: `8819`
  - sample_keys: `close, date, diagnostic_only, e1r_entry_type, e1r_uptrend_confirmed_eligible, e1r_uptrend_emerging_eligible, equity, leader_rank, leader_score, ma20, ma20_slope, ma50, ma50_slope, momentum_acceleration, momentum_score, reasons, rs_20d_improvement, rs_prev20, rs_score, spx_regime, symbol, trend_health`
- `e1r_forward_equity`
  - exists: `True`
  - json_valid: `True`
  - row_count: `1`
  - sample_keys: `backfill_start_date, cash, core_exposure, date, drawdown_pct, equity, forward_return_pct, gross_exposure, market_state, market_value, official_kickoff_date, portfolio_value, regime, shadow_start_date, sidecar_exposure, strategy_id, strategy_indexed, subclass, tracking_status, version`
- `market_state`
  - exists: `True`
  - json_valid: `True`
  - row_count: `0`
  - sample_keys: ``
- `e1r_status`
  - exists: `True`
  - json_valid: `True`
  - row_count: `0`
  - sample_keys: ``

## Diagnosis

- E1R forward equity file exists with row_count=1.
- dashboard/app.js mentions oos_e1r_v0_2_equity_curve.
- dashboard has some E1R forward text references.
- main equity chart footnote still says E1-R OOS tracking is not yet completed.

## Next Patch Should

- Add E1R forward paper equity as a separate dataset only if oos_e1r_v0_2_equity_curve.json has usable rows.
- Rename legend labels to distinguish E1R backtest vs E1R forward paper.
- Update footnote so it no longer says E1-R OOS tracking is not yet completed when paper tracking data exists.
- Do not modify strategy/backtest/export files.

