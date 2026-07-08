# Stage 3.8E-2F-1E-0 E1R Target/Action Input Contract Audit

Generated At: `2026-07-08T06:56:23.186135+00:00`
HEAD: `613e7ee`

## Status

- Status: `AUDIT_COMPLETE_NO_SOURCE_CHANGES`
- Source changed: `False`
- Exports changed: `False`
- State changed: `False`
- Dashboard changed: `False`
- Strategy logic changed: `False`

## Question

What exact symbol-level target/action inputs are available for E1R forward positions/orders?

## Implementation Decision

- Can generate real orders now: `False`
- Reason: Need exact target symbol/weight source before generating orders/positions. This audit maps available candidates only.
- Likely core input: `exports/leaderboard.json or E1R composer output, pending exact field confirmation.`
- Likely sidecar input: `exports/oos_e1r_v0_2_sidecar.json if it contains selected symbols/weights; otherwise e1r_sidecar_sleeve output must be called directly.`
- Official runner to extend: `scripts/run_e1r_v0_2_oos.py`

## Target-ready Candidate Files

- `exports/e1r_v0_2_status.json`
- `exports/oos_e1r_v0_2_summary.json`
- `exports/oos_e1r_v0_2_equity_curve.json`
- `exports/oos_e1r_v0_2_sidecar.json`
- `exports/e1r_v0_2_backtest_equity_curve.json`
- `exports/leaderboard.json`
- `exports/market_state.json`
- `data/oos/e1r_v0_2_portfolio_state.json`

## Source Summary

- `scripts/run_e1r_v0_2_oos.py` lines=`180` defs=`['read_json', 'write_json', 'main']` hit_terms=`['target', 'target_weight', 'weight', 'selected', 'selected_count', 'symbols', 'top', 'top_n', 'core', 'sidecar', 'sleeve', 'gross_exposure', 'position', 'positions', 'order', 'orders', 'HOLD', 'E1R_REGIME_AWARE_V0_2', 'SIDEWAYS', 'MA_CONFLICT']` write_hits=`10`
- `scripts/run_e1r_v0_2_oos_equity.py` lines=`408` defs=`['read_json', 'write_json', 'pick', 'safe_float', 'extract_existing_oos_core_equity', 'compute_return', 'load_stock_price_map', 'compute_sidecar_mtm_return', 'normalize_current_sidecar_positions', 'main']` hit_terms=`['target', 'target_weight', 'weight', 'selected', 'selected_count', 'core', 'sidecar', 'position', 'positions', 'order', 'orders', 'E1R_REGIME_AWARE_V0_2']` write_hits=`5`
- `scripts/run_e1r_v0_2_forward_performance.py` lines=`423` defs=`['utc_now_iso', 'generated_at_display', 'read_json', 'write_json', 'append_jsonl', 'to_float', 'pct_return', 'max_drawdown_pct', 'daily_returns', 'sharpe_ratio', 'first_existing', 'normalize_status_date', 'normalize_equity_rows', 'infer_spx_forward_return_pct']` hit_terms=`['target', 'selected', 'selected_count', 'core', 'sidecar', 'sleeve', 'gross_exposure', 'core_exposure', 'sidecar_exposure', 'position', 'positions', 'order', 'orders', 'E1R_REGIME_AWARE_V0_2']` write_hits=`14`
- `scripts/export_e1r_v0_2_status.py` lines=`217` defs=`['read_json', 'write_json', 'pick', 'normalize_e1r_state', 'extract_latest_regime', 'extract_legacy_market_state', 'simplify_holding', 'main']` hit_terms=`['weight', 'selected', 'selected_count', 'symbols', 'top', 'top_n', 'leader', 'core', 'sidecar', 'sleeve', 'gross_exposure', 'E1R_REGIME_AWARE_V0_2', 'UPTREND', 'SIDEWAYS', 'DOWNTREND', 'MA_CONFLICT']` write_hits=`3`
- `scripts/run_e1r_v0_2_sidecar_lifecycle.py` lines=`296` defs=`['read_json', 'write_json', 'safe_float', 'normalize_positions', 'compute_lifecycle', 'main']` hit_terms=`['target', 'target_weight', 'weight', 'symbols', 'core', 'sidecar', 'sleeve', 'position', 'positions', 'order', 'orders', 'EXIT', 'E1R_REGIME_AWARE_V0_2']` write_hits=`8`
- `src/engine/e1r_composer.py` lines=`360` defs=`['safe_float', 'pct_display', 'compound_return', 'max_drawdown', 'sharpe_ratio', 'profit_factor', 'extract_core_interval_returns', 'build_equity_records_from_returns', 'summarize_combined_variant', 'compose_e1r_v0_2_variant']` hit_terms=`['selected', 'selected_count', 'symbols', 'top', 'top_n', 'core', 'sidecar', 'sleeve', 'gross_exposure', 'position', 'E1R_REGIME_AWARE_V0_2', 'UPTREND', 'SIDEWAYS', 'MA_CONFLICT']` write_hits=`0`
- `src/engine/e1r_sidecar_sleeve.py` lines=`594` defs=`['E1RSidecarConfig', 'safe_float', 'pct_display', 'compound_return', 'mean_or_none', 'median_or_none', 'max_drawdown', 'sharpe_ratio', 'profit_factor', 'load_asset', 'load_stock_universe', 'load_regimes', 'history_closes', 'moving_average']` hit_terms=`['weight', 'selected', 'selected_count', 'symbols', 'candidates', 'candidate', 'top', 'top_n', 'core', 'sidecar', 'sleeve', 'gross_exposure', 'HOLD', 'EXIT', 'E1R_REGIME_AWARE_V0_2', 'SIDEWAYS', 'DOWNTREND', 'MA_CONFLICT']` write_hits=`0`
- `src/oos/tracking_engine.py` lines=`265` defs=`['run_oos_day']` hit_terms=`['candidates', 'candidate', 'leader', 'core', 'position', 'positions', 'order', 'orders', 'BUY', 'HOLD', 'ADD', 'EXIT']` write_hits=`0`
- `src/oos/portfolio_state.py` lines=`140` defs=`['PortfolioState', '__init__', 'rebuild_from_events', 'total_equity', 'save_snapshot']` hit_terms=`['position', 'positions', 'order', 'orders', 'BUY', 'ADD', 'EXIT']` write_hits=`1`
- `src/oos/exporter.py` lines=`207` defs=`['_now_iso', '_now_display', 'write_json', 'export_no_op', 'export_stale', 'export_failed', 'export_all']` hit_terms=`['position', 'positions', 'order', 'orders', 'BUY', 'EXIT']` write_hits=`10`

## Data Summary

- `exports/e1r_v0_2_status.json` exists=`True` type=`dict` top_keys=`['generated_at', 'strategy_id', 'version', 'research_status', 'status_date', 'e1r_market_state', 'regime', 'subclass', 'mutually_exclusive_state_model', 'core', 'sidecar', 'legacy_market_state', 'source_files', 'notes']` candidate_objects=`3` candidate_arrays=`0`
- `exports/oos_e1r_v0_2_summary.json` exists=`True` type=`dict` top_keys=`['generated_at', 'generated_at_display', 'status_date', 'strategy_id', 'version', 'phase', 'research_status', 'tracking_status', 'forward_start_date', 'official_kickoff_date', 'forward_day_count', 'portfolio_value', 'equity', 'cash', 'market_value', 'forward_return_pct', 'spx_forward_return_pct', 'alpha_pct', 'max_drawdown_pct', 'sharpe_ratio', 'profit_factor', 'number_of_trades', 'executed_orders_count', 'open_positions_count', 'gross_exposure', 'net_exposure', 'core_exposure', 'sidecar_exposure', 'market_state', 'regime', 'subclass', 'core_active', 'sidecar_active', 'sidecar_selected_count', 'equity_status', 'execution_status', 'notes', 'shadow_start_date', 'backfill_start_date', 'kickoff_semantics']` candidate_objects=`1` candidate_arrays=`0`
- `exports/oos_e1r_v0_2_equity_curve.json` exists=`True` type=`list` top_keys=`[]` candidate_objects=`1` candidate_arrays=`1`
- `exports/oos_e1r_v0_2_positions.json` exists=`True` type=`list` top_keys=`[]` candidate_objects=`0` candidate_arrays=`0`
- `exports/oos_e1r_v0_2_orders.json` exists=`True` type=`list` top_keys=`[]` candidate_objects=`0` candidate_arrays=`0`
- `exports/oos_e1r_v0_2_sidecar.json` exists=`True` type=`dict` top_keys=`['generated_at', 'phase', 'strategy_id', 'status_date', 'market_state', 'regime', 'subclass', 'active', 'active_condition', 'gross_exposure', 'top_n', 'excluded_symbols', 'source_record_date', 'source_record_next_date', 'selected_count', 'selected']` candidate_objects=`1` candidate_arrays=`0`
- `exports/oos_e1r_v0_2_sidecar_lifecycle.json` exists=`True` type=`dict` top_keys=`['generated_at', 'strategy_id', 'phase', 'execution_status', 'source', 'start_date', 'end_date', 'row_count', 'latest', 'records', 'notes']` candidate_objects=`2` candidate_arrays=`0`
- `exports/oos_e1r_v0_2_sidecar_turnover.json` exists=`True` type=`dict` top_keys=`['generated_at', 'strategy_id', 'phase', 'execution_status', 'source', 'start_date', 'end_date', 'row_count', 'average_one_way_turnover', 'latest', 'records', 'notes']` candidate_objects=`2` candidate_arrays=`0`
- `exports/e1r_v0_2_backtest_summary.json` exists=`True` type=`dict` top_keys=`['strategy_id', 'total_return_pct', 'spx_return_pct', 'alpha_pct', 'max_drawdown_pct', 'profit_factor', 'sharpe_ratio', 'research_status', 'regime_aware_logic', 'sidecar_active_days', 'sidecar_active_by_regime', 'sidecar_active_by_subclass', 'composition_exists', 'row_count', 'variant', 'artifact_type', 'source_file', 'source_json_path', 'frozen_artifact', 'regeneration_note']` candidate_objects=`1` candidate_arrays=`0`
- `exports/e1r_v0_2_backtest_equity_curve.json` exists=`True` type=`dict` top_keys=`['variant', 'artifact_type', 'source_file', 'source_json_path', 'frozen_artifact', 'regeneration_note', 'row_count', 'rows', 'equity_curve']` candidate_objects=`80` candidate_arrays=`2`
- `exports/leaderboard.json` exists=`True` type=`dict` top_keys=`['generated_at', 'generated_at_display', 'data_source', 'phase', 'leaders']` candidate_objects=`10` candidate_arrays=`1`
- `exports/market_state.json` exists=`True` type=`dict` top_keys=`['generated_at', 'generated_at_display', 'data_source', 'phase', 'market']` candidate_objects=`8` candidate_arrays=`0`
- `data/oos/e1r_v0_2_portfolio_state.json` exists=`True` type=`dict` top_keys=`['strategy_id', 'version', 'created_at', 'updated_at', 'official_kickoff_date', 'status_date', 'portfolio_value', 'equity', 'cash', 'market_value', 'positions', 'last_summary', 'shadow_start_date', 'backfill_start_date', 'tracking_status']` candidate_objects=`2` candidate_arrays=`0`

## Key Candidate Objects

### E1R status
- `$` symbol_keys=`[]` weight_keys=`[]` target_like_keys=`[]`
- `$.core` symbol_keys=`[]` weight_keys=`[]` target_like_keys=`[]`
- `$.sidecar` symbol_keys=`['selected']` weight_keys=`['gross_exposure']` target_like_keys=`['excluded_symbols', 'selected_count', 'selected']`

### E1R sidecar
- `$` symbol_keys=`['selected']` weight_keys=`['gross_exposure']` target_like_keys=`['excluded_symbols', 'selected_count', 'selected']`

### Leaderboard arrays
- `$.leaders` rows=`10` sample_keys=`['symbol', 'name', 'sector', 'price', 'ma20', 'ma50', 'ma200', 'above_ma20', 'above_ma50', 'above_ma200', 'ma20_slope', 'ma50_slope', 'rs_score', 'rs_raw', 'ret60', 'momentum_score', 'ret20', 'ret60_pct', 'ret20_pct', 'ma50_slope_pct', 'slope5', 'slope10', 'slope20', 'trend_health', 'drawdown_pct', 'volatility_pct', 'price_structure_score', 'ma50_slope_score', 'drawdown_score', 'volatility_score']`

## Guardrails

- Do not generate synthetic orders from gross_exposure alone. Orders require symbol-level targets.
- Do not touch E1 state.
- Do not alter frozen E1R strategy logic.

## Next

- Stage 3.8E-2F-1E-1 should implement symbol-level target extraction after this contract is reviewed.

