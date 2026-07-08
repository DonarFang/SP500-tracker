# Stage 3.8E-2F-0 E1R Forward Kickoff Readiness Audit

Generated At: `2026-07-08T06:24:55.288374+00:00`
HEAD: `9d3f522`

## Status

- Status: `AUDIT_COMPLETE_NO_SOURCE_CHANGES`
- Source changed: `False`
- Dashboard changed: `False`
- Exports changed: `False`
- Strategy logic changed: `False`

## Decision

- E1 forward test: `STARTED`
- E1 forward start date: `2026-06-18`
- E1R forward performance test: `NOT YET PROPERLY KICKED OFF`
- E1R current status: historical freeze + partial status scaffold.

## Readiness

- E1R status scaffold exists: `True`
- E1R equity curve scaffold exists: `True`
- E1R orders scaffold exists: `True`
- E1R positions scaffold exists: `True`
- E1R forward performance fields exist: `False`
- Assessment: `NOT_YET_KICKED_OFF_AS_FORWARD_PERFORMANCE_TEST`

## Recommended Forward Start Policy

- Official E1R forward tracking should start on the next available trading day after implementation.
- Any generated data before official kickoff should be labeled `BACKFILL` / `SHADOW`, not official OOS.

## Required Daily Exports

### Summary

- `generated_at`
- `generated_at_display`
- `status_date`
- `strategy_id`
- `version`
- `forward_start_date`
- `forward_day_count`
- `research_status`
- `tracking_status`
- `portfolio_value`
- `equity`
- `cash`
- `market_value`
- `forward_return_pct`
- `spx_forward_return_pct`
- `alpha_pct`
- `max_drawdown_pct`
- `sharpe_ratio`
- `profit_factor`
- `number_of_trades`
- `open_positions_count`
- `executed_orders_count`
- `gross_exposure`
- `net_exposure`
- `core_exposure`
- `sidecar_exposure`
- `market_state`
- `regime`
- `subclass`
- `core_active`
- `sidecar_active`
- `sidecar_selected_count`

## JSON Export Inspection

- `exports/oos_summary.json` exists=`True` type=`dict` top_keys=`['generated_at', 'generated_at_display', 'status', 'strategy_id', 'oos_start_date', 'run_date', 'last_successful_run', 'last_market_date', 'expected_market_date', 'initial_capital', 'final_equity', 'total_return_pct', 'max_drawdown_pct', 'profit_factor', 'win_rate_pct', 'total_trades', 'open_positions', 'live_event_count', 'backfill_event_count', 'first_review_criteria', 'provenance_note', 'mixed_provenance_positions']` date=`{'generated_at': '2026-07-07T22:52:43.361353+00:00', 'generated_at_display': '2026年7月7日 18:52 ET'}` performance=`{'total_return_pct': -24.74, 'profit_factor': None, 'max_drawdown_pct': 24.74}` regime=`{}`
- `exports/oos_equity_curve.json` exists=`True` type=`dict` top_keys=`['generated_at', 'generated_at_display', 'strategy_id', 'initial_capital', 'curve']` date=`{'generated_at': '2026-07-07T22:52:43.361353+00:00', 'generated_at_display': '2026年7月7日 18:52 ET'}` performance=`{}` regime=`{}`
- `exports/oos_orders.json` exists=`True` type=`dict` top_keys=`['generated_at', 'generated_at_display', 'strategy_id', 'orders']` date=`{'generated_at': '2026-07-07T22:52:43.361353+00:00', 'generated_at_display': '2026年7月7日 18:52 ET'}` performance=`{}` regime=`{}`
- `exports/oos_positions.json` exists=`True` type=`dict` top_keys=`['generated_at', 'generated_at_display', 'strategy_id', 'as_of', 'positions', 'pending_orders', 'cash']` date=`{'generated_at': '2026-07-07T22:52:43.361353+00:00', 'generated_at_display': '2026年7月7日 18:52 ET', 'as_of': '2026-07-07'}` performance=`{'cash': 0.02}` regime=`{}`
- `exports/oos_trades.json` exists=`True` type=`dict` top_keys=`['generated_at', 'generated_at_display', 'strategy_id', 'total_trades', 'trades']` date=`{'generated_at': '2026-07-07T22:52:43.361353+00:00', 'generated_at_display': '2026年7月7日 18:52 ET'}` performance=`{'trades': []}` regime=`{}`
- `exports/oos_e1r_v0_2_summary.json` exists=`True` type=`dict` top_keys=`['generated_at', 'phase', 'strategy_id', 'version', 'research_status', 'status_date', 'market_state', 'regime', 'subclass', 'mutually_exclusive_state_model', 'core_active', 'sidecar_active', 'sidecar_selected_count', 'gross_exposure', 'top_n', 'execution_status', 'equity_status', 'notes']` date=`{'status_date': '2026-06-18', 'generated_at': '2026-07-07T23:56:04.521255+00:00'}` performance=`{'gross_exposure': 0.25}` regime=`{'market_state': 'UPTREND', 'regime': 'UPTREND', 'subclass': None, 'core_active': True, 'sidecar_active': False, 'sidecar_selected_count': 0, 'execution_status': 'NO_REAL_EXECUTION', 'equity_status': 'NOT_YET_CONNECTED'}`
- `exports/oos_e1r_v0_2_equity_curve.json` exists=`True` type=`dict` top_keys=`['generated_at', 'strategy_id', 'phase', 'equity_status', 'execution_status', 'curve_type', 'start_date', 'end_date', 'row_count', 'latest', 'records', 'notes']` date=`{'generated_at': '2026-07-07T23:56:04.524822+00:00'}` performance=`{}` regime=`{'execution_status': 'PAPER_TRACKING_NO_REAL_EXECUTION', 'equity_status': 'OOS_EQUITY_MTM_TRACKING_SIDECAR_PAPER'}`
- `exports/oos_e1r_v0_2_orders.json` exists=`True` type=`dict` top_keys=`['generated_at', 'phase', 'strategy_id', 'status_date', 'market_state', 'execution_status', 'orders']` date=`{'status_date': '2026-06-18', 'generated_at': '2026-07-07T23:56:04.521255+00:00'}` performance=`{}` regime=`{'market_state': 'UPTREND', 'execution_status': 'NO_REAL_EXECUTION'}`
- `exports/oos_e1r_v0_2_positions.json` exists=`True` type=`dict` top_keys=`['generated_at', 'phase', 'strategy_id', 'status_date', 'market_state', 'core', 'sidecar']` date=`{'status_date': '2026-06-18', 'generated_at': '2026-07-07T23:56:04.521255+00:00'}` performance=`{}` regime=`{'market_state': 'UPTREND'}`
- `exports/oos_e1r_v0_2_sidecar.json` exists=`True` type=`dict` top_keys=`['generated_at', 'phase', 'strategy_id', 'status_date', 'market_state', 'regime', 'subclass', 'active', 'active_condition', 'gross_exposure', 'top_n', 'excluded_symbols', 'source_record_date', 'source_record_next_date', 'selected_count', 'selected']` date=`{'status_date': '2026-06-18', 'generated_at': '2026-07-07T23:56:04.521255+00:00'}` performance=`{'gross_exposure': 0.25}` regime=`{'market_state': 'UPTREND', 'regime': 'UPTREND', 'subclass': None}`
- `exports/e1r_v0_2_status.json` exists=`True` type=`dict` top_keys=`['generated_at', 'strategy_id', 'version', 'research_status', 'status_date', 'e1r_market_state', 'regime', 'subclass', 'mutually_exclusive_state_model', 'core', 'sidecar', 'legacy_market_state', 'source_files', 'notes']` date=`{'status_date': '2026-06-18', 'generated_at': '2026-07-07T23:56:04.506044+00:00'}` performance=`{}` regime=`{'regime': 'UPTREND', 'subclass': None}`
- `exports/e1r_v0_2_backtest_summary.json` exists=`True` type=`dict` top_keys=`['strategy_id', 'total_return_pct', 'spx_return_pct', 'alpha_pct', 'max_drawdown_pct', 'profit_factor', 'sharpe_ratio', 'research_status', 'regime_aware_logic', 'sidecar_active_days', 'sidecar_active_by_regime', 'sidecar_active_by_subclass', 'composition_exists', 'row_count', 'variant', 'artifact_type', 'source_file', 'source_json_path', 'frozen_artifact', 'regeneration_note']` date=`{}` performance=`{'total_return_pct': 116.7435999134756, 'profit_factor': 1.1919630955509348, 'max_drawdown_pct': 25.904809362815108}` regime=`{}`
- `exports/e1r_v0_2_backtest_equity_curve.json` exists=`True` type=`dict` top_keys=`['variant', 'artifact_type', 'source_file', 'source_json_path', 'frozen_artifact', 'regeneration_note', 'row_count', 'rows', 'equity_curve']` date=`{}` performance=`{}` regime=`{}`
- `data/oos/portfolio_state.json` exists=`True` type=`dict` top_keys=`['cash', 'holdings', 'holdings_value', 'equity', 'n_positions', 'pending_orders', 'closed_trades']` date=`{}` performance=`{'equity': 75255.2, 'cash': 0.02}` regime=`{}`

## Candidate Source / Pipeline Files

- `dashboard/app.js`
- `docs/research/stage3_2_backtest_snapshots/backtest_feature_source_stage3_2.py`
- `docs/research/stage3_2_backtest_snapshots/backtest_main_before_stage3_2.py`
- `docs/research/stage3_4_app_snapshots/app_feature_source_stage3_4.js`
- `docs/research/stage3_4_app_snapshots/app_generated_e1r_v0_2_module_stage3_4.js`
- `docs/research/stage3_4_app_snapshots/app_main_before_stage3_4.js`
- `docs/research/stage3_8b_dashboard_refactor_snapshots/app_before_stage3_8b.js`
- `docs/research/stage3_8b_dashboard_refactor_snapshots/app_stage3_8b_module.js`
- `run_oos.py`
- `scripts/export_e1r_v0_2_backtest_equity.py`
- `scripts/export_e1r_v0_2_status.py`
- `scripts/run_e1r_v0_2_oos.py`
- `scripts/run_e1r_v0_2_oos_equity.py`
- `scripts/run_e1r_v0_2_sidecar_lifecycle.py`
- `src/engine/backtest.py`
- `src/engine/e1r_composer.py`
- `src/engine/e1r_sidecar_sleeve.py`
- `src/oos/__init__.py`
- `src/oos/exporter.py`
- `src/oos/portfolio_state.py`
- `src/oos/tracking_engine.py`

## Watched File Hits

- `.github/workflows/update.yml` exists=`True` line_count=`51` hit_terms=`['OOS', 'paper']`
- `scripts/update_pipeline.py` exists=`False` line_count=`None` hit_terms=`[]`
- `scripts/init_data.py` exists=`False` line_count=`None` hit_terms=`[]`
- `scripts/backtest.py` exists=`False` line_count=`None` hit_terms=`[]`
- `src/engine/backtest.py` exists=`True` line_count=`2978` hit_terms=`['E1_AUDITED_G4_MINHOLD10', 'E1R_REGIME_AWARE_V0_2', 'forward', 'equity', 'positions', 'orders', 'gross_exposure', 'sidecar']`
- `src/engine/e1r_composer.py` exists=`True` line_count=`360` hit_terms=`['E1R_REGIME_AWARE_V0_2', 'equity', 'gross_exposure', 'sidecar', 'sidecar_active']`
- `src/engine/e1r_sidecar_sleeve.py` exists=`True` line_count=`594` hit_terms=`['E1_AUDITED_G4_MINHOLD10', 'E1R_REGIME_AWARE_V0_2', 'equity', 'gross_exposure', 'sidecar']`
- `dashboard/app.js` exists=`True` line_count=`1356` hit_terms=`['E1_AUDITED_G4_MINHOLD10', 'oos_summary', 'oos_equity_curve', 'oos_e1r_v0_2', 'forward', 'OOS', 'paper', 'equity', 'positions', 'orders', 'sidecar', 'core_active', 'sidecar_active', 'status_date']`
- `exports/oos_summary.json` exists=`True` line_count=`24` hit_terms=`['E1_AUDITED_G4_MINHOLD10', 'OOS', 'equity', 'positions']`
- `exports/oos_equity_curve.json` exists=`True` line_count=`104` hit_terms=`['E1_AUDITED_G4_MINHOLD10', 'equity', 'positions']`
- `exports/oos_orders.json` exists=`True` line_count=`94` hit_terms=`['E1_AUDITED_G4_MINHOLD10', 'orders']`
- `exports/oos_positions.json` exists=`True` line_count=`43` hit_terms=`['E1_AUDITED_G4_MINHOLD10', 'positions', 'orders']`
- `exports/oos_trades.json` exists=`True` line_count=`7` hit_terms=`['E1_AUDITED_G4_MINHOLD10']`
- `exports/oos_e1r_v0_2_summary.json` exists=`True` line_count=`25` hit_terms=`['E1R_REGIME_AWARE_V0_2', 'OOS', 'equity', 'orders', 'gross_exposure', 'sidecar', 'core_active', 'sidecar_active', 'status_date']`
- `exports/oos_e1r_v0_2_equity_curve.json` exists=`True` line_count=`66` hit_terms=`['E1R_REGIME_AWARE_V0_2', 'OOS', 'equity', 'positions', 'orders', 'sidecar', 'core_active', 'sidecar_active']`
- `exports/oos_e1r_v0_2_orders.json` exists=`True` line_count=`9` hit_terms=`['E1R_REGIME_AWARE_V0_2', 'OOS', 'orders', 'status_date']`
- `exports/oos_e1r_v0_2_positions.json` exists=`True` line_count=`17` hit_terms=`['E1R_REGIME_AWARE_V0_2', 'OOS', 'positions', 'sidecar', 'status_date']`
- `exports/oos_e1r_v0_2_sidecar.json` exists=`True` line_count=`20` hit_terms=`['E1R_REGIME_AWARE_V0_2', 'OOS', 'gross_exposure', 'status_date']`
- `exports/e1r_v0_2_status.json` exists=`True` line_count=`49` hit_terms=`['E1R_REGIME_AWARE_V0_2', 'OOS', 'gross_exposure', 'sidecar', 'status_date']`
- `exports/e1r_v0_2_backtest_summary.json` exists=`True` line_count=`26` hit_terms=`['E1R_REGIME_AWARE_V0_2', 'sidecar', 'sidecar_active']`
- `exports/e1r_v0_2_backtest_equity_curve.json` exists=`True` line_count=`573843` hit_terms=`['E1R_REGIME_AWARE_V0_2', 'equity']`
- `data/oos/portfolio_state.json` exists=`True` line_count=`37` hit_terms=`['equity', 'positions', 'orders']`
- `data/oos/events.jsonl` exists=`True` line_count=`19` hit_terms=`['E1_AUDITED_G4_MINHOLD10', 'equity', 'positions']`
- `data/oos/run_history.jsonl` exists=`True` line_count=`17` hit_terms=`['OOS', 'equity', 'positions', 'orders']`

## Minimum Kickoff Acceptance

- E1R summary export contains forward_start_date and status_date.
- E1R summary export contains portfolio_value/equity and forward_return_pct.
- E1R equity curve has at least one row for kickoff date.
- E1R positions export exists even if empty.
- E1R orders export exists even if empty.
- Daily update pipeline writes all E1R OOS exports deterministically.
- Dashboard does not infer E1R performance from historical backtest fields.

## Next

- Stage 3.8E-2F-1 should implement E1R forward test exports and daily pipeline integration.
- Dashboard mapping should wait until exports contain real forward performance fields.

