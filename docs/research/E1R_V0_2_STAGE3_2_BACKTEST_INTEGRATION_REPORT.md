# E1R v0.2 Stage 3.2 Backtest Integration Report

Generated At: `2026-07-05T15:06:02.658504+00:00`

## Status

- Stage: `B_STAGE_3_2_BACKTEST_CONTROLLED_INTEGRATION`
- Status: `INTEGRATED_FEATURE_BACKTEST_WITH_GUARDS`
- Integrated file: `src/engine/backtest.py`
- Policy: `controlled_integration_with_snapshots_diff_compile_and_marker_checks`

## Validation

- `py_compile` passed.
- Legacy E1/E2 markers preserved.
- E1R v0.2 markers present.
- Concrete `e1r_composer` function usage detected dynamically.
- Snapshot and diff files created.

## Composer Function Detection

- Available composer functions: `['safe_float', 'pct_display', 'compound_return', 'max_drawdown', 'sharpe_ratio', 'profit_factor', 'extract_core_interval_returns', 'build_equity_records_from_returns', 'summarize_combined_variant', 'compose_e1r_v0_2_variant']`
- Used by feature backtest: `['max_drawdown', 'sharpe_ratio', 'profit_factor', 'compose_e1r_v0_2_variant']`
- Used after integration: `['max_drawdown', 'sharpe_ratio', 'profit_factor', 'compose_e1r_v0_2_variant']`

## Snapshots

- Main before: `docs/research/stage3_2_backtest_snapshots/backtest_main_before_stage3_2.py`
- Feature source: `docs/research/stage3_2_backtest_snapshots/backtest_feature_source_stage3_2.py`
- Diff: `docs/research/stage3_2_backtest_py_controlled.diff`

## Boundary

- No broker integration.
- No real order execution.
- This stage only integrates `src/engine/backtest.py`.
- Dashboard and CSS files are not changed in this stage.

## Next Stage

Stage 3.3: `dashboard/styles.css` scoped append.

