# Stage 3.8E-2F-1A E1R Forward Implementation Source Audit

Generated At: `2026-07-08T06:28:19.076897+00:00`
HEAD: `c16b2d6`

## Status

- Status: `AUDIT_COMPLETE_NO_SOURCE_CHANGES`
- Source changed: `False`
- Dashboard changed: `False`
- Exports changed: `False`
- Strategy logic changed: `False`

## Core Decision

- E1 forward entry likely: `run_oos.py`
- E1 OOS engine likely: `src/oos/tracking_engine.py + src/oos/portfolio_state.py + src/oos/exporter.py`
- E1R forward performance fields exist: `False`

## Implementation Hypothesis

E1 has a real OOS tracking engine. E1R currently has separate scaffolding scripts for status/equity artifacts but does not yet produce a full forward performance summary. Stage 3.8E-2F-1 likely needs either a dedicated E1R OOS engine that mirrors E1 tracking or a wrapper that reuses src/oos tracking primitives with E1R target positions/actions.

## Roles

- E1 forward entry candidates: `['scripts/run_e1r_v0_2_oos_equity.py', 'src/oos/tracking_engine.py', 'src/oos/exporter.py', 'src/oos/__init__.py', 'src/engine/backtest.py', 'src/engine/e1r_sidecar_sleeve.py']`
- E1R forward entry candidates: `['scripts/run_e1r_v0_2_oos.py', 'scripts/run_e1r_v0_2_oos_equity.py', 'scripts/export_e1r_v0_2_status.py', 'scripts/export_e1r_v0_2_backtest_equity.py', 'scripts/run_e1r_v0_2_sidecar_lifecycle.py', 'src/engine/backtest.py', 'src/engine/e1r_composer.py', 'src/engine/e1r_sidecar_sleeve.py']`
- Portfolio state candidates: `['run_oos.py', 'src/oos/tracking_engine.py', 'src/oos/exporter.py', 'src/oos/portfolio_state.py']`
- Export writer candidates: `['run_oos.py', 'scripts/run_e1r_v0_2_oos.py', 'scripts/run_e1r_v0_2_oos_equity.py', 'scripts/export_e1r_v0_2_status.py', 'scripts/export_e1r_v0_2_backtest_equity.py', 'scripts/run_e1r_v0_2_sidecar_lifecycle.py', 'src/oos/tracking_engine.py', 'src/oos/exporter.py', 'src/oos/portfolio_state.py', 'src/engine/backtest.py', '.github/workflows/update.yml']`
- Daily pipeline candidates: `['run_oos.py', 'src/oos/tracking_engine.py', '.github/workflows/update.yml']`
- Strategy logic candidates: `['src/engine/backtest.py', 'src/engine/e1r_composer.py', 'src/engine/e1r_sidecar_sleeve.py']`

## Source File Summary

- `run_oos.py` lines=`352` defs=`['_load_price_from_history', '_current_oos_holding_symbols', 'load_market_data', 'cmd_status', 'cmd_replay_invalidated', 'main']` hit_terms=`['run_oos', 'PortfolioState', 'export', 'portfolio_state', 'mark', 'equity', 'cash', 'position', 'trade', 'return', 'generated_at', 'main(', 'if __name__']` write_exports=`['events.jsonl', 'portfolio_state.json']`
- `scripts/run_e1r_v0_2_oos.py` lines=`180` defs=`['read_json', 'write_json', 'main']` hit_terms=`['E1R_REGIME_AWARE_V0_2', 'export', 'oos_e1r_v0_2_summary', 'oos_e1r_v0_2_equity_curve', 'oos_e1r_v0_2_orders', 'oos_e1r_v0_2_positions', 'mark', 'equity', 'position', 'order', 'return', 'gross_exposure', 'sidecar', 'core_active', 'sidecar_active', 'status_date', 'generated_at', 'main(', 'if __name__']` write_exports=`['oos_e1r_v0_2_equity_curve.json', 'oos_e1r_v0_2_orders.json', 'oos_e1r_v0_2_positions.json', 'oos_e1r_v0_2_sidecar.json', 'oos_e1r_v0_2_summary.json']`
- `scripts/run_e1r_v0_2_oos_equity.py` lines=`408` defs=`['read_json', 'write_json', 'pick', 'safe_float', 'extract_existing_oos_core_equity', 'compute_return', 'load_stock_price_map', 'compute_sidecar_mtm_return', 'normalize_current_sidecar_positions', 'main']` hit_terms=`['E1R_REGIME_AWARE_V0_2', 'export', 'oos_summary', 'oos_equity_curve', 'oos_e1r_v0_2_summary', 'oos_e1r_v0_2_equity_curve', 'mark', 'equity', 'position', 'order', 'return', 'sidecar', 'core_active', 'sidecar_active', 'status_date', 'generated_at', 'main(', 'if __name__']` write_exports=`['oos_e1r_v0_2_equity_curve.json', 'oos_e1r_v0_2_sidecar.json', 'oos_e1r_v0_2_summary.json', 'oos_equity_curve.json', 'oos_summary.json']`
- `scripts/export_e1r_v0_2_status.py` lines=`217` defs=`['read_json', 'write_json', 'pick', 'normalize_e1r_state', 'extract_latest_regime', 'extract_legacy_market_state', 'simplify_holding', 'main']` hit_terms=`['E1R_REGIME_AWARE_V0_2', 'export', 'mark', 'equity', 'return', 'gross_exposure', 'sidecar', 'core_active', 'sidecar_active', 'status_date', 'generated_at', 'main(', 'if __name__']` write_exports=`[]`
- `scripts/export_e1r_v0_2_backtest_equity.py` lines=`189` defs=`['read_json', 'write_json', 'first_present', 'normalize_curve', 'extract_variant', 'main']` hit_terms=`['E1R_REGIME_AWARE_V0_2', 'export', 'mark', 'equity', 'position', 'return', 'drawdown', 'sharpe', 'profit_factor', 'sidecar', 'sidecar_active', 'generated_at', 'main(', 'if __name__']` write_exports=`[]`
- `scripts/run_e1r_v0_2_sidecar_lifecycle.py` lines=`296` defs=`['read_json', 'write_json', 'safe_float', 'normalize_positions', 'compute_lifecycle', 'main']` hit_terms=`['E1R_REGIME_AWARE_V0_2', 'export', 'oos_e1r_v0_2_equity_curve', 'mark', 'equity', 'position', 'order', 'return', 'sidecar', 'sidecar_active', 'generated_at', 'main(', 'if __name__']` write_exports=`['oos_e1r_v0_2_equity_curve.json']`
- `src/oos/tracking_engine.py` lines=`265` defs=`['run_oos_day']` hit_terms=`['E1_AUDITED_G4_MINHOLD10', 'run_oos', 'PortfolioState', 'export', 'portfolio_state', 'mark', 'equity', 'cash', 'position', 'order', 'return']` write_exports=`[]`
- `src/oos/exporter.py` lines=`207` defs=`['_now_iso', '_now_display', 'write_json', 'export_no_op', 'export_stale', 'export_failed', 'export_all']` hit_terms=`['export', 'oos_summary', 'oos_equity_curve', 'oos_orders', 'oos_positions', 'oos_trades', 'portfolio_state', 'mark', 'equity', 'cash', 'position', 'order', 'trade', 'return', 'drawdown', 'profit_factor', 'generated_at']` write_exports=`['events.jsonl', 'oos_equity_curve.json', 'oos_orders.json', 'oos_positions.json', 'oos_summary.json', 'oos_trades.json', 'portfolio_state.json']`
- `src/oos/portfolio_state.py` lines=`140` defs=`['PortfolioState', '__init__', 'rebuild_from_events', 'total_equity', 'save_snapshot']` hit_terms=`['PortfolioState', 'portfolio_state', 'equity', 'cash', 'position', 'order', 'trade', 'return']` write_exports=`['events.jsonl', 'portfolio_state.json']`
- `src/oos/__init__.py` lines=`5` defs=`[]` hit_terms=`['E1_AUDITED_G4_MINHOLD10']` write_exports=`[]`
- `src/engine/backtest.py` lines=`2978` defs=`['is_broken_trend', 'forward_return', '_rebuild_leader_score', 'run_leader_engine_validation', 'run_trade_rule_validation', 'stats', 'run_promotion_engine_validation', 'run_action_forward_validation', 'stats', 'run_stateful_simulation', '_e1r_regime_on', '_e1r_mode_for_regime']` hit_terms=`['E1_AUDITED_G4_MINHOLD10', 'E1R_REGIME_AWARE_V0_2', 'export', 'mark', 'equity', 'cash', 'position', 'order', 'trade', 'return', 'drawdown', 'sharpe', 'profit_factor', 'gross_exposure', 'sidecar']` write_exports=`[]`
- `src/engine/e1r_composer.py` lines=`360` defs=`['safe_float', 'pct_display', 'compound_return', 'max_drawdown', 'sharpe_ratio', 'profit_factor', 'extract_core_interval_returns', 'build_equity_records_from_returns', 'summarize_combined_variant', 'compose_e1r_v0_2_variant']` hit_terms=`['E1R_REGIME_AWARE_V0_2', 'equity', 'position', 'trade', 'return', 'drawdown', 'sharpe', 'profit_factor', 'gross_exposure', 'sidecar', 'sidecar_active']` write_exports=`[]`
- `src/engine/e1r_sidecar_sleeve.py` lines=`594` defs=`['E1RSidecarConfig', 'safe_float', 'pct_display', 'compound_return', 'mean_or_none', 'median_or_none', 'max_drawdown', 'sharpe_ratio', 'profit_factor', 'load_asset', 'load_stock_universe', 'load_regimes']` hit_terms=`['E1_AUDITED_G4_MINHOLD10', 'E1R_REGIME_AWARE_V0_2', 'equity', 'trade', 'return', 'drawdown', 'sharpe', 'profit_factor', 'gross_exposure', 'sidecar']` write_exports=`[]`
- `.github/workflows/update.yml` lines=`51` defs=`[]` hit_terms=`['run_oos', 'export']` write_exports=`[]`

## Export File Summary

- `exports/oos_summary.json` exists=`True` type=`dict` top_keys=`['generated_at', 'generated_at_display', 'status', 'strategy_id', 'oos_start_date', 'run_date', 'last_successful_run', 'last_market_date', 'expected_market_date', 'initial_capital', 'final_equity', 'total_return_pct', 'max_drawdown_pct', 'profit_factor', 'win_rate_pct', 'total_trades', 'open_positions', 'live_event_count', 'backfill_event_count', 'first_review_criteria', 'provenance_note', 'mixed_provenance_positions']` performance=`{'total_return_pct': -24.74, 'max_drawdown_pct': 24.74, 'profit_factor': None}` status=`{'strategy_id': 'E1_AUDITED_G4_MINHOLD10'}`
- `exports/oos_equity_curve.json` exists=`True` type=`dict` top_keys=`['generated_at', 'generated_at_display', 'strategy_id', 'initial_capital', 'curve']` performance=`{}` status=`{'strategy_id': 'E1_AUDITED_G4_MINHOLD10'}`
- `exports/oos_orders.json` exists=`True` type=`dict` top_keys=`['generated_at', 'generated_at_display', 'strategy_id', 'orders']` performance=`{}` status=`{'strategy_id': 'E1_AUDITED_G4_MINHOLD10'}`
- `exports/oos_positions.json` exists=`True` type=`dict` top_keys=`['generated_at', 'generated_at_display', 'strategy_id', 'as_of', 'positions', 'pending_orders', 'cash']` performance=`{'cash': 0.02}` status=`{'strategy_id': 'E1_AUDITED_G4_MINHOLD10'}`
- `exports/oos_trades.json` exists=`True` type=`dict` top_keys=`['generated_at', 'generated_at_display', 'strategy_id', 'total_trades', 'trades']` performance=`{}` status=`{'strategy_id': 'E1_AUDITED_G4_MINHOLD10'}`
- `exports/oos_e1r_v0_2_summary.json` exists=`True` type=`dict` top_keys=`['generated_at', 'phase', 'strategy_id', 'version', 'research_status', 'status_date', 'market_state', 'regime', 'subclass', 'mutually_exclusive_state_model', 'core_active', 'sidecar_active', 'sidecar_selected_count', 'gross_exposure', 'top_n', 'execution_status', 'equity_status', 'notes']` performance=`{}` status=`{'phase': 'OOS_STATUS_SIGNAL_ONLY', 'strategy_id': 'E1R_REGIME_AWARE_V0_2', 'version': 'E1R-v0.2-formal-sidecar-sleeve', 'research_status': 'FORMAL_SIDECAR_SLEEVE_ENGINE', 'execution_status': 'NO_REAL_EXECUTION', 'equity_status': 'NOT_YET_CONNECTED', 'market_state': 'UPTREND', 'regime': 'UPTREND', 'subclass': None, 'core_active': True, 'sidecar_active': False, 'sidecar_selected_count': 0, 'gross_exposure': 0.25}`
- `exports/oos_e1r_v0_2_equity_curve.json` exists=`True` type=`dict` top_keys=`['generated_at', 'strategy_id', 'phase', 'equity_status', 'execution_status', 'curve_type', 'start_date', 'end_date', 'row_count', 'latest', 'records', 'notes']` performance=`{}` status=`{'phase': 'OOS_2B_FORWARD_EQUITY_CURVE', 'strategy_id': 'E1R_REGIME_AWARE_V0_2', 'execution_status': 'PAPER_TRACKING_NO_REAL_EXECUTION', 'equity_status': 'OOS_EQUITY_MTM_TRACKING_SIDECAR_PAPER'}`
- `exports/oos_e1r_v0_2_orders.json` exists=`True` type=`dict` top_keys=`['generated_at', 'phase', 'strategy_id', 'status_date', 'market_state', 'execution_status', 'orders']` performance=`{}` status=`{'phase': 'OOS_STATUS_SIGNAL_ONLY', 'strategy_id': 'E1R_REGIME_AWARE_V0_2', 'execution_status': 'NO_REAL_EXECUTION', 'market_state': 'UPTREND'}`
- `exports/oos_e1r_v0_2_positions.json` exists=`True` type=`dict` top_keys=`['generated_at', 'phase', 'strategy_id', 'status_date', 'market_state', 'core', 'sidecar']` performance=`{}` status=`{'phase': 'OOS_STATUS_SIGNAL_ONLY', 'strategy_id': 'E1R_REGIME_AWARE_V0_2', 'market_state': 'UPTREND'}`
- `exports/oos_e1r_v0_2_sidecar.json` exists=`True` type=`dict` top_keys=`['generated_at', 'phase', 'strategy_id', 'status_date', 'market_state', 'regime', 'subclass', 'active', 'active_condition', 'gross_exposure', 'top_n', 'excluded_symbols', 'source_record_date', 'source_record_next_date', 'selected_count', 'selected']` performance=`{}` status=`{'phase': 'OOS_STATUS_SIGNAL_ONLY', 'strategy_id': 'E1R_REGIME_AWARE_V0_2', 'market_state': 'UPTREND', 'regime': 'UPTREND', 'subclass': None, 'gross_exposure': 0.25}`
- `exports/e1r_v0_2_status.json` exists=`True` type=`dict` top_keys=`['generated_at', 'strategy_id', 'version', 'research_status', 'status_date', 'e1r_market_state', 'regime', 'subclass', 'mutually_exclusive_state_model', 'core', 'sidecar', 'legacy_market_state', 'source_files', 'notes']` performance=`{}` status=`{'strategy_id': 'E1R_REGIME_AWARE_V0_2', 'version': 'E1R-v0.2-formal-sidecar-sleeve', 'research_status': 'FORMAL_SIDECAR_SLEEVE_ENGINE', 'regime': 'UPTREND', 'subclass': None}`
- `data/oos/portfolio_state.json` exists=`True` type=`dict` top_keys=`['cash', 'holdings', 'holdings_value', 'equity', 'n_positions', 'pending_orders', 'closed_trades']` performance=`{'equity': 75255.2, 'cash': 0.02}` status=`{}`
- `data/oos/events.jsonl` exists=`True` type=`None` top_keys=`None` performance=`{}` status=`{}`
- `data/oos/run_history.jsonl` exists=`True` type=`None` top_keys=`None` performance=`{}` status=`{}`

## Recommended Implementation Path

- Do not modify frozen historical E1R rules.
- Reuse E1 OOS accounting primitives where possible: portfolio state, equity mark-to-market, exporter.
- Use E1R composer/sidecar outputs only to generate daily target actions/weights.
- Create or extend an E1R OOS runner to write summary/equity_curve/orders/positions with performance fields.
- Add kickoff date explicitly to summary.
- Integrate runner into daily pipeline after smoke validation.

## Official Kickoff Policy

- Official E1R forward test starts on first trading day after implementation is merged and daily pipeline runs.
- If backfilled rows are generated for diagnostics, label them BACKFILL/SHADOW and do not count as official OOS.

## Next

- `Stage 3.8E-2F-1B`: Design implementation plan with exact files/functions to modify before coding.

