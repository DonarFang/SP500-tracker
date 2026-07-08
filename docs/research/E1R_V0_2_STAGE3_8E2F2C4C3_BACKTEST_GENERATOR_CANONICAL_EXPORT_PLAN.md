# Stage 3.8E-2F-2C-4C-3 Backtest Generator / Canonical Export Plan

Generated At: `2026-07-08T10:29:14.284139+00:00`

## Status

- Status: `AUDIT_COMPLETE_PLAN_DEFINED_NO_SOURCE_CHANGES`
- Dashboard changed: `False`
- Exports changed: `False`
- State changed: `False`
- Workflow changed: `False`
- Strategy logic changed: `False`

## Diagnosis

- Prior 4C-2 report confirms no direct 5Y portfolio-level E1/E1R equity artifact was selected in v13/main.
- exports/portfolio_backtest.json is E1-like but window is 2023-11-06 to 2026-06-11; not 5Y.
- exports/e1r_v0_2_backtest_equity_curve.json exists but previous audit classifies it as symbol-level/diagnostic, not canonical portfolio equity.
- Top Python generator candidate: scripts/export_e1r_v0_2_backtest_equity.py score=73 roles=portfolio_equity_logic_candidate,export_writer_candidate,e1r_v0_2_candidate,backtest_logic_candidate.

## Top Generator Candidates

- score `89` · `docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json` · roles `portfolio_equity_logic_candidate, e1r_v0_2_candidate, e1_candidate`
  - matched_terms: `portfolio_value, daily_equity, equity_curve, spx_curve, strategy_indexed, cash, market_value, positions, mark, backtest, E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1, run_oos, export, portfolio_backtest, e1r_v0_2_backtest, formal_backtest, simulation_start_date, simulation_end_date, 2021-06-11, 2026-06-18, 1261, 1258`
  - path_literals: `      - exports/oos_equity_curve.json,       latest record in exports/oos_e1r_v0_2_equity_curve.json, data/research/e1_5y/constituents/current_constituents.json, data/research/e1_5y/constituents/snapshot_2026-06-11.json, data/research/e1_5y/data_audit.json, data/research/e1_5y/download_manifest.json, data/research/e1_5y/e1_baseline_parity_check.json, data/research/e1_5y/raw/indices/NDX.json, data/research/e1_5y/raw/indices/SOX.json, data/research/e1_5y/raw/indices/SPX.json, data/research/e1_5y/raw/stocks/A.json, data/research/e1_5y/raw/stocks/AAL.json, data/research/e1_5y/raw/stocks/AAPL.json, data/research/e1_5y/raw/stocks/ABBV.json, data/research/e1_5y/raw/stocks/ABNB.json, data/research/e1_5y/raw/stocks/ABT.json, data/research/e1_5y/raw/stocks/ACGL.json, data/research/e1_5y/raw/stocks/ACN.json, data/research/e1_5y/raw/stocks/ADBE.json, data/research/e1_5y/raw/stocks/ADI.json`
- score `87` · `docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.md` · roles `portfolio_equity_logic_candidate, e1r_v0_2_candidate, e1_candidate`
  - matched_terms: `portfolio_value, daily_equity, equity_curve, spx_curve, strategy_indexed, cash, market_value, mark, backtest, E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1, run_oos, export, portfolio_backtest, e1r_v0_2_backtest, formal_backtest, simulation_start_date, simulation_end_date, 2021-06-11, 2026-06-18, 1261, 1258`
- score `83` · `docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json` · roles `portfolio_equity_logic_candidate, export_writer_candidate, e1r_v0_2_candidate, e1_candidate`
  - matched_terms: `portfolio_value, daily_equity, equity_curve, strategy_indexed, cash, market_value, positions, mark, backtest, E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1, run_oos, export, json.dump, json.dumps, write_text, e1r_v0_2_backtest, 2021-06-11, 2026-06-18, 1258`
  - path_literals: `      latest record in exports/oos_e1r_v0_2_equity_curve.json, data/oos/e1r_v0_2_portfolio_state.json, exports/e1r_v0_2_backtest_equity_curve.json, exports/e1r_v0_2_backtest_summary.json, exports/e1r_v0_2_status.json, exports/leaderboard.json, exports/market_state.json, exports/oos_e1r_v0_2_equity_curve.json, exports/oos_e1r_v0_2_orders.json, exports/oos_e1r_v0_2_positions.json, exports/oos_e1r_v0_2_sidecar.json, exports/oos_e1r_v0_2_sidecar_lifecycle.json, exports/oos_e1r_v0_2_sidecar_turnover.json, exports/oos_e1r_v0_2_summary.json`
- score `79` · `docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json` · roles `portfolio_equity_logic_candidate, e1r_v0_2_candidate, e1_candidate`
  - matched_terms: `portfolio_value, daily_equity, equity_curve, spx_curve, strategy_indexed, cash, market_value, positions, mark, marked, backtest, E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1, run_oos, export, e1r_v0_2_backtest, simulation_end_date, 2021-06-11, 2026-06-18, 1261, 1258`
  - path_literals: `data/oos/portfolio_state.json, exports/e1r_v0_2_backtest_equity_curve.json, exports/e1r_v0_2_backtest_summary.json, exports/e1r_v0_2_status.json, exports/oos_e1r_v0_2_equity_curve.json, exports/oos_e1r_v0_2_orders.json, exports/oos_e1r_v0_2_positions.json, exports/oos_e1r_v0_2_sidecar.json, exports/oos_e1r_v0_2_summary.json, exports/oos_equity_curve.json, exports/oos_orders.json, exports/oos_positions.json, exports/oos_summary.json, exports/oos_trades.json`
- score `76` · `docs/research/E1R_V0_2_STAGE3_8E2F2C4C1_5Y_EQUITY_ARTIFACT_AUDIT.json` · roles `portfolio_equity_logic_candidate, e1r_v0_2_candidate, e1_candidate`
  - matched_terms: `portfolio_value, daily_equity, equity_curve, spx_curve, strategy_indexed, cash, market_value, positions, mark, backtest, E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, export, portfolio_backtest, e1r_v0_2_backtest, formal_backtest, simulation_start_date, 2021-06-11, 2026-06-18`
  - path_literals: `          git add -f exports/backtest.json exports/action_forward_returns.json exports/portfolio_backtest.json exports/trade_log.json exports/equity_curve.json,       - exports/oos_equity_curve.json,       latest record in exports/oos_e1r_v0_2_equity_curve.json, backtest.json, data/research/e1_5y/regimes/spx_regime_daily.json, data/research/e1r/e1r_formal_backtest_v0_1.json, exports/backtest.json, exports/e1r_v0_2_backtest_equity_curve.json, exports/e1r_v0_2_backtest_summary.json, exports/oos_e1r_v0_2_equity_curve.json, exports/oos_e1r_v0_2_summary.json, exports/oos_equity_curve.json`
- score `75` · `docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json` · roles `portfolio_equity_logic_candidate, export_writer_candidate, e1r_v0_2_candidate, e1_candidate`
  - matched_terms: `portfolio_value, daily_equity, equity_curve, cash, positions, mark, backtest, E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1, run_oos, export, json.dump, json.dumps, write_text, e1r_v0_2_backtest, 2026-06-18`
  - path_literals: `      - exports/oos_equity_curve.json,       - exports/oos_summary.json,       latest record in exports/oos_e1r_v0_2_equity_curve.json, data/oos/portfolio_state.json, exports/e1r_v0_2_status.json, exports/oos_e1r_v0_2_equity_curve.json, exports/oos_e1r_v0_2_orders.json, exports/oos_e1r_v0_2_positions.json, exports/oos_e1r_v0_2_sidecar.json, exports/oos_e1r_v0_2_summary.json, exports/oos_equity_curve.json, exports/oos_orders.json, exports/oos_positions.json, exports/oos_summary.json, exports/oos_trades.json, oos_e1r_v0_2_equity_curve.json, oos_e1r_v0_2_orders.json, oos_e1r_v0_2_positions.json, oos_e1r_v0_2_sidecar.json, oos_e1r_v0_2_summary.json`
- score `73` · `scripts/export_e1r_v0_2_backtest_equity.py` · roles `portfolio_equity_logic_candidate, export_writer_candidate, e1r_v0_2_candidate, backtest_logic_candidate`
  - matched_terms: `portfolio_value, daily_equity, equity_curve, mark, backtest, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1, export, json.dump, json.dumps, write_text, e1r_v0_2_backtest`
  - defs: `def read_json(path: Path) -> Any:; def write_json(path: Path, obj: Any) -> None:; def first_present(d: dict[str, Any], keys: list[str], default=None):; def normalize_curve(records: list[dict[str, Any]]) -> list[dict[str, Any]]:; def extract_variant(variants: dict[str, Any], strategy_id: str) -> dict[str, Any]:; def main() -> None:`
  - path_literals: `Missing exports/backtest.json, Wrote exports/e1r_v0_2_backtest_equity_curve.json, Wrote exports/e1r_v0_2_backtest_summary.json, exports/backtest.json, exports/e1r_v0_2_backtest_equity_curve.json, exports/e1r_v0_2_backtest_summary.json`
- score `66` · `docs/research/E1R_V0_2_STAGE3_8E2F2C4A_EQUITY_CURVE_RENDER_AUDIT.json` · roles `portfolio_equity_logic_candidate, e1r_v0_2_candidate, e1_candidate`
  - matched_terms: `portfolio_value, equity_curve, spx_curve, strategy_indexed, cash, market_value, positions, mark, marked, backtest, E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, export, e1r_v0_2_backtest, simulation_end_date, 2021-06-11, 2026-06-18, 1258`
- score `63` · `src/engine/backtest.py` · roles `portfolio_equity_logic_candidate, e1r_v0_2_candidate, e1_candidate, backtest_logic_candidate`
  - matched_terms: `daily_equity, equity_curve, spx_curve, cash, positions, mark, backtest, E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1, export, simulation_start_date, simulation_end_date, 2021-06-11, 2026-06-18`
  - defs: `def is_broken_trend(trend_state: str) -> bool:; def forward_return(prices: list[float], t: int, days: int) -> float | None:; def _rebuild_leader_score(prices: list[float], spx_prices: list[float],; def run_leader_engine_validation(; def run_trade_rule_validation(;     def stats(rets):; def run_promotion_engine_validation(; def run_action_forward_validation(`
  - path_literals: `data/research/e1_5y/raw/indices/SPX.json, data/research/e1_5y/raw/stocks, data/research/e1_5y/regimes/spx_regime_daily.json`
- score `61` · `scripts/run_e1r_v0_2_forward_performance_core.py` · roles `portfolio_equity_logic_candidate, export_writer_candidate, e1r_v0_2_candidate, forward_oos_logic_candidate`
  - matched_terms: `portfolio_value, equity_curve, strategy_indexed, cash, market_value, positions, mark, backtest, E1R_REGIME_AWARE_V0_2, export, json.dump, json.dumps, write_text`
  - defs: `def utc_now_iso() -> str:; def generated_at_display() -> str:; def read_json(path: Path, default: Any) -> Any:; def write_json(path: Path, obj: Any) -> None:; def append_jsonl(path: Path, obj: Dict[str, Any]) -> None:; def to_float(v: Any, default: Optional[float] = None) -> Optional[float]:; def pct_return(current: float, base: float) -> float:; def max_drawdown_pct(values: List[float]) -> float:`
  - path_literals: `data, e1r_v0_2_portfolio_state.json, e1r_v0_2_status.json, exports, oos_e1r_v0_2_equity_curve.json, oos_e1r_v0_2_orders.json, oos_e1r_v0_2_positions.json, oos_e1r_v0_2_summary.json, oos_summary.json`
- score `60` · `docs/research/stage3_2_backtest_snapshots/backtest_feature_source_stage3_2.py` · roles `portfolio_equity_logic_candidate, e1r_v0_2_candidate, e1_candidate, backtest_logic_candidate`
  - matched_terms: `daily_equity, equity_curve, spx_curve, cash, positions, mark, backtest, E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1, export, simulation_start_date, simulation_end_date, 2021-06-11, 2026-06-18`
  - defs: `def is_broken_trend(trend_state: str) -> bool:; def forward_return(prices: list[float], t: int, days: int) -> float | None:; def _rebuild_leader_score(prices: list[float], spx_prices: list[float],; def run_leader_engine_validation(; def run_trade_rule_validation(;     def stats(rets):; def run_promotion_engine_validation(; def run_action_forward_validation(`
  - path_literals: `data/research/e1_5y/raw/indices/SPX.json, data/research/e1_5y/raw/stocks, data/research/e1_5y/regimes/spx_regime_daily.json`
- score `59` · `docs/research/E1R_V0_2_STAGE3_8E2F1F0_DAILY_PIPELINE_AUDIT.json` · roles `portfolio_equity_logic_candidate, export_writer_candidate, e1r_v0_2_candidate`
  - matched_terms: `portfolio_value, equity_curve, cash, market_value, positions, mark, backtest, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1, run_oos, export, json.dump, json.dumps, write_text, 2021-06-11, 2026-06-18`
  - path_literals: `      - exports/oos_equity_curve.json,       - exports/oos_summary.json`
- score `59` · `scripts/run_e1r_v0_2_oos_equity.py` · roles `portfolio_equity_logic_candidate, export_writer_candidate, e1r_v0_2_candidate`
  - matched_terms: `portfolio_value, equity_curve, positions, mark, E1R_REGIME_AWARE_V0_2, export, json.dump, json.dumps, write_text`
  - defs: `def read_json(path: Path, default: Any = None) -> Any:; def write_json(path: Path, obj: Any) -> None:; def pick(obj: Any, keys: list[str], default: Any = None) -> Any:; def safe_float(v: Any, default: float | None = None) -> float | None:; def extract_existing_oos_core_equity() -> dict[str, Any]:; def compute_return(prev_equity: float, new_equity: float) -> float:; def load_stock_price_map() -> dict[str, dict[str, float]]:; def compute_sidecar_mtm_return(`
  - path_literals: `*.json, data/research/e1_5y/raw/stocks, exports/e1r_v0_2_status.json, exports/oos_e1r_v0_2_equity_curve.json, exports/oos_e1r_v0_2_sidecar.json, exports/oos_e1r_v0_2_summary.json, exports/oos_equity_curve.json, exports/oos_summary.json`
- score `56` · `docs/research/E1R_V0_2_STAGE3_8E2F2C0_EQUITY_CURVE_MAPPING_AUDIT.json` · roles `portfolio_equity_logic_candidate, e1r_v0_2_candidate`
  - matched_terms: `portfolio_value, equity_curve, spx_curve, strategy_indexed, cash, market_value, positions, mark, marked, backtest, E1R_REGIME_AWARE_V0_2, export, e1r_v0_2_backtest, formal_backtest, simulation_end_date, 2026-06-18`
- score `53` · `docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.md` · roles `portfolio_equity_logic_candidate, e1r_v0_2_candidate, e1_candidate`
  - matched_terms: `portfolio_value, equity_curve, cash, market_value, positions, mark, backtest, E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, run_oos, export, e1r_v0_2_backtest, 2026-06-18`
- score `51` · `docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json` · roles `portfolio_equity_logic_candidate, e1r_v0_2_candidate`
  - matched_terms: `portfolio_value, equity_curve, spx_curve, cash, market_value, positions, mark, backtest, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1, run_oos, export, e1r_v0_2_backtest, formal_backtest, 2026-06-18`
  - path_literals: `- fallback: exports/market_state.json, data/research/e1_5y/regimes/spx_regime_daily.json, docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json, docs/research/E1R_V0_2_STAGE3_5_MAIN_SMOKE_TEST_REPORT.json, docs/research/E1R_V0_2_STAGE3_8A_DASHBOARD_REFACTOR_AUDIT.json, docs/research/E1R_V0_2_STAGE3_8D_NATIVE_RENDER_AUDIT.json, docs/research/E1R_V0_2_STAGE3_8E2B_V3_PREPATCH_AUDIT.json, docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json, docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json, docs/research/E1R_V0_2_STAGE3_8E2F1C_RUNNER_DRY_RUN_AUDIT.json, docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json, docs/research/E1R_V0_2_STAGE3_8E2F1E1_TARGET_SOURCE_CONTRACT.json, docs/research/E1R_V0_2_STAGE3_8E2F1F0_DAILY_PIPELINE_AUDIT.json, docs/research/E1R_V0_2_STAGE3_8E2F2C3FA_MARKET_STATE_FIELD_AUDIT.json, exports/e1r_v0_2_backtest_equity_curve.json, exports/e1r_v0_2_backtest_summary.json, exports/e1r_v0_2_status.json, exports/equity_curve.json, exports/market_state.json, exports/oos_e1r_v0_2_equity_curve.json`
- score `51` · `docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json` · roles `portfolio_equity_logic_candidate, export_writer_candidate, e1r_v0_2_candidate`
  - matched_terms: `equity_curve, strategy_indexed, cash, market_value, positions, mark, backtest, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1, run_oos, export, json.dump, json.dumps, write_text, e1r_v0_2_backtest, 2021-06-11, 2026-06-18`
  - path_literals: `      - exports/oos_equity_curve.json,       - exports/oos_summary.json,       latest record in exports/oos_e1r_v0_2_equity_curve.json,     # market_state.json,     # watchlist.json, market_state.json, spx_regime_daily.json`
- score `49` · `docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json` · roles `e1r_v0_2_candidate, e1_candidate`
  - matched_terms: `equity_curve, spx_curve, cash, positions, mark, backtest, E1_AUDITED_G4_MINHOLD10, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1, export, e1r_v0_2_backtest, simulation_start_date, simulation_end_date, 2021-06-11, 2026-06-18, 1258`
  - path_literals: `data/research/e1_5y/regimes/spx_regime_daily.json, exports/backtest.json, exports/e1r_v0_2_backtest_equity_curve.json, exports/e1r_v0_2_backtest_summary.json, exports/e1r_v0_2_status.json, exports/leaderboard.json, exports/market_state.json, exports/oos_e1r_v0_2_equity_curve.json, exports/oos_e1r_v0_2_orders.json, exports/oos_e1r_v0_2_positions.json, exports/oos_e1r_v0_2_sidecar.json, exports/oos_e1r_v0_2_summary.json, exports/oos_equity_curve.json, exports/oos_orders.json, exports/oos_positions.json, exports/oos_summary.json, exports/oos_trades.json, exports/oos_trades.json / exports/oos_orders.json, exports/trade_log.json, exports/trade_log.json or embedded backtest.json`
- score `48` · `scripts/run_e1r_v0_2_oos.py` · roles `portfolio_equity_logic_candidate, export_writer_candidate, e1r_v0_2_candidate`
  - matched_terms: `portfolio_value, cash, market_value, positions, mark, E1R_REGIME_AWARE_V0_2, export, json.dump, json.dumps, write_text`
  - defs: `def now_iso() -> str:; def read_json(path: Path, default: Any) -> Any:; def write_json(path: Path, obj: Any) -> None:; def to_float(v: Any, default: float = 0.0) -> float:; def get_orders(doc: Any) -> List[Dict[str, Any]]:; def get_positions(doc: Any) -> List[Dict[str, Any]]:; def snapshot() -> Dict[str, Any]:; def should_preserve(before: Dict[str, Any]) -> bool:`
  - path_literals: `data, e1r_v0_2_portfolio_state.json, exports, oos_e1r_v0_2_orders.json, oos_e1r_v0_2_positions.json, oos_e1r_v0_2_summary.json, scripts`
- score `46` · `scripts/run_e1r_v0_2_oos_core.py` · roles `export_writer_candidate, e1r_v0_2_candidate`
  - matched_terms: `equity_curve, positions, mark, E1R_REGIME_AWARE_V0_2, E1R_REGIME_AWARE_V0_1, export, json.dump, json.dumps, write_text`
  - defs: `def read_json(path: Path) -> Any:; def write_json(path: Path, obj: Any) -> None:; def main() -> None:`
  - path_literals: `  exports/e1r_v0_2_status.json,   exports/oos_e1r_v0_2_equity_curve.json,   exports/oos_e1r_v0_2_orders.json,   exports/oos_e1r_v0_2_positions.json,   exports/oos_e1r_v0_2_sidecar.json,   exports/oos_e1r_v0_2_sidecar_lifecycle.json,   exports/oos_e1r_v0_2_sidecar_turnover.json,   exports/oos_e1r_v0_2_summary.json, exports/e1r_v0_2_status.json, exports/oos_e1r_v0_2_orders.json, exports/oos_e1r_v0_2_positions.json, exports/oos_e1r_v0_2_sidecar.json, exports/oos_e1r_v0_2_summary.json, scripts/export_e1r_v0_2_status.py, scripts/run_e1r_v0_2_oos_equity.py, scripts/run_e1r_v0_2_sidecar_lifecycle.py`

## Required Canonical Outputs

- `exports/e1_5y_backtest_equity_curve.json`
  - strategy_id: `E1_AUDITED_G4_MINHOLD10`
  - purpose: `portfolio-level canonical equity curve`
- `exports/e1r_v0_2_portfolio_backtest_equity_curve.json`
  - strategy_id: `E1R_REGIME_AWARE_V0_2`
  - purpose: `portfolio-level canonical equity curve`
- `exports/e1_e1r_5y_equity_comparison.json`
  - strategy_id: `N/A`
  - purpose: `dashboard canonical source for historical comparison`

## Continuity Rule

- `E1_forward`: Scale E1 OOS equity by E1 5Y backtest ending strategy_indexed / 100.
- `E1R_forward`: Scale E1R forward strategy_indexed by E1R 5Y backtest ending strategy_indexed / 100.
- `do_not`: Do not plot forward strategy_indexed=100 directly on historical comparison chart when a backtest continuation is intended.

## Validation Gates

- Each canonical backtest curve must have one row per date.
- Date range should start near 2021-06-11 and end near 2026-06-16/2026-06-18.
- E1 and E1R curves must use the same SPX date calendar or explicit null padding.
- E1R symbol-level diagnostic rows must not be used directly as portfolio equity.
- Dashboard should use exports/e1_e1r_5y_equity_comparison.json for historical chart once generated.

## Implementation Options

### Option A: Find existing backtest engine portfolio curve output

- Risk: `lowest if present`
- Inspect top generator candidates for internal portfolio daily equity variables.
- Export already-computed daily portfolio values without changing strategy logic.
- Validate against frozen metrics: E1R v0.2 total return +116.74%, SPX +76.84%, Alpha +39.90%.

### Option B: Re-run frozen backtest engines and export canonical daily curves

- Risk: `medium, runtime may be longer`
- Create export-only wrapper scripts around frozen backtest code.
- Do not change strategy files.
- Emit canonical JSONs under exports/.
- Compare final metrics with frozen audit numbers before dashboard patch.

### Option C: Aggregate existing E1R symbol-level diagnostic rows

- Risk: `high unless diagnostic rows include exact daily portfolio weights/cash`
- Only use this if rows contain enough portfolio accounting fields.
- Reject if only symbol-level score/price diagnostics are available.
- Prefer A or B.

## Recommended Next Stage

`Stage 3.8E-2F-2C-4C-4: Inspect selected generator candidate internals and prototype export-only wrappers.`

