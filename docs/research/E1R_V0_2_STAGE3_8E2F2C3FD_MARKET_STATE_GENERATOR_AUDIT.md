# Stage 3.8E-2F-2C-3F-D Market State Generator Audit

Generated At: `2026-07-08T09:57:32.431740+00:00`

## Status

- Status: `AUDIT_COMPLETE_NO_SOURCE_CHANGES`
- Dashboard changed: `False`
- Exports changed: `False`
- State changed: `False`
- Workflow changed: `False`

## Current market_state Schema

- state: `Risk-On`
- market_score: `60.0`
- date: `2026-07-07`
- has_trend_state: `False`

## Top Candidate Generators

- `scripts/export_e1r_v0_2_status.py` score `21` terms `exports, json.dump, json.dumps, leadership_confirmed, market_score, market_state, market_state.json, state_zh, write_text`
  - L21: `    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")`
  - L78: `def extract_legacy_market_state(path: Path) -> dict[str, Any]:`
  - L87: `        "state": pick(market, ["state", "market_state", "trend_state", "regime"], None),`
  - L88: `        "state_zh": pick(market, ["state_zh"], None),`
  - L89: `        "market_score": pick(market, ["market_score"], None),`
- `src/export/export_json.py` score `15` terms `EXPORTS, market_state, market_state.json`
  - L15: `    EXPORT_TRADES, EXPORT_LIFECYCLE, EXPORTS_DIR,`
  - L21: `EXPORT_BACKTEST = EXPORTS_DIR / "backtest.json"`
  - L22: `EXPORT_STOCK_CHARTS = EXPORTS_DIR / "stock_charts.json"`
  - L75: `    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)`
  - L79: `    # market_state.json`
- `src/utils/config.py` score `15` terms `EXPORTS, exports, market_state, market_state.json`
  - L8: `EXPORTS_DIR = ROOT_DIR / "exports"`
  - L31: `EXPORT_MARKET     = EXPORTS_DIR / "market_state.json"`
  - L32: `EXPORT_LEADERBOARD= EXPORTS_DIR / "leaderboard.json"`
  - L33: `EXPORT_WATCHLIST  = EXPORTS_DIR / "watchlist.json"`
  - L34: `EXPORT_TRADES     = EXPORTS_DIR / "trade_actions.json"`
- `scripts/run_e1r_v0_2_forward_performance_core.py` score `11` terms `exports, json.dump, json.dumps, market_state, write_text`
  - L10: `- Write E1R-only state and forward performance exports.`
  - L26: `EXPORT_DIR = ROOT / "exports"`
  - L66: `    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")`
  - L72: `        f.write(json.dumps(obj, ensure_ascii=False) + "\n")`
  - L281: `    regime = first_existing(status.get("regime"), scaffold_summary.get("regime"), status.get("market_state"), default="UNKNOWN")`
- `scripts/run_e1r_v0_2_oos_core.py` score `11` terms `exports, json.dump, json.dumps, market_state, write_text`
  - L18: `    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")`
  - L23: `    status_path = ROOT / "exports/e1r_v0_2_status.json"`
  - L32: `        raise RuntimeError("exports/e1r_v0_2_status.json was not generated")`
  - L39: `    market_state = status.get("e1r_market_state", "UNKNOWN")`
  - L59: `        "market_state": market_state,`
- `scripts/run_e1r_v0_2_oos_equity.py` score `11` terms `exports, json.dump, json.dumps, market_state, write_text`
  - L19: `    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")`
  - L47: `      - exports/oos_summary.json`
  - L48: `      - exports/oos_equity_curve.json`
  - L52: `    summary = read_json(ROOT / "exports/oos_summary.json", {}) or {}`
  - L53: `    curve = read_json(ROOT / "exports/oos_equity_curve.json", {}) or {}`
- `scripts/run_e1r_v0_2_sidecar_lifecycle.py` score `11` terms `exports, json.dump, json.dumps, market_state, write_text`
  - L19: `    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")`
  - L37: `      latest record in exports/oos_e1r_v0_2_equity_curve.json`
  - L148: `    equity_path = ROOT / "exports/oos_e1r_v0_2_equity_curve.json"`
  - L149: `    lifecycle_path = ROOT / "exports/oos_e1r_v0_2_sidecar_lifecycle.json"`
  - L150: `    turnover_path = ROOT / "exports/oos_e1r_v0_2_sidecar_turnover.json"`
- `src/engine/backtest.py` score `9` terms `exports, market_score, market_state`
  - L320: `    market_score_default: float = 60.0,`
  - L387: `                ma50_sl, ls, th, market_score_default`
  - L604: `    market_score_default: float = 60.0,`
  - L670: `                ma50_sl, ls, th, market_score_default`
  - L773: `    market_score_default: float = 60.0,`

## Workflow Hits

- L18: `      - uses: actions/setup-python@v5`
- L20: `          python-version: '3.11'`
- L24: `        run: python fetch_data.py`
- L29: `          python run_oos.py --check`
- L35: `        run: python run_oos.py`
- L41: `          python3 scripts/export_e1r_v0_2_status.py`
- L42: `          python3 scripts/run_e1r_v0_2_oos.py`
- L43: `          python3 scripts/run_e1r_v0_2_oos_equity.py`
- L44: `          python3 scripts/export_e1r_v0_2_targets_preview.py`
- L45: `          python3 scripts/export_e1r_v0_2_orders_positions_preview.py`
- L46: `          python3 scripts/run_e1r_v0_2_forward_performance.py`

## Regime Mentions In Candidates

- `scripts/export_e1r_v0_2_status.py` L34: `def normalize_e1r_state(regime: str, subclass: str) -> str:`
- `scripts/export_e1r_v0_2_status.py` L35: `    r = (regime or "UNKNOWN").upper()`
- `scripts/export_e1r_v0_2_status.py` L39: `        return "UPTREND"`
- `scripts/export_e1r_v0_2_status.py` L41: `        return "DOWNTREND"`
- `scripts/export_e1r_v0_2_status.py` L44: `            return "SIDEWAYS_MA_CONFLICT"`
- `scripts/export_e1r_v0_2_status.py` L46: `            return "SIDEWAYS_DETERIORATION"`
- `scripts/export_e1r_v0_2_status.py` L48: `            return "SIDEWAYS_RECOVERY"`
- `scripts/export_e1r_v0_2_status.py` L49: `        return "SIDEWAYS"`
- `scripts/export_e1r_v0_2_status.py` L53: `def extract_latest_regime(regime_json: Any) -> dict[str, Any]:`
- `scripts/export_e1r_v0_2_status.py` L54: `    daily = regime_json.get("daily_regime") if isinstance(regime_json, dict) else regime_json`
- `scripts/export_e1r_v0_2_status.py` L59: `            raise RuntimeError("daily_regime list is empty")`
- `scripts/export_e1r_v0_2_status.py` L66: `            raise RuntimeError("daily_regime dict is empty")`
- `scripts/export_e1r_v0_2_status.py` L75: `    raise RuntimeError("Unsupported spx_regime_daily.json structure")`
- `scripts/export_e1r_v0_2_status.py` L87: `        "state": pick(market, ["state", "market_state", "trend_state", "regime"], None),`
- `scripts/export_e1r_v0_2_status.py` L106: `    regime_path = ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json"`
- `scripts/export_e1r_v0_2_status.py` L112: `    regime_json = read_json(regime_path)`
- `scripts/export_e1r_v0_2_status.py` L113: `    latest = extract_latest_regime(regime_json)`
- `scripts/export_e1r_v0_2_status.py` L116: `    regime = str(pick(latest, ["regime", "market_regime", "state"], "UNKNOWN")).upper()`
- `scripts/export_e1r_v0_2_status.py` L117: `    subclass = str(pick(latest, ["subclass", "regime_subclass", "market_subclass", "sideways_subclass"], "") or "").upper()`
- `scripts/export_e1r_v0_2_status.py` L118: `    e1r_market_state = normalize_e1r_state(regime, subclass)`
- `scripts/export_e1r_v0_2_status.py` L135: `        regime_path=regime_path,`
- `scripts/export_e1r_v0_2_status.py` L160: `    sidecar_active = e1r_market_state == "SIDEWAYS_MA_CONFLICT" and len(holdings) > 0`
- `scripts/export_e1r_v0_2_status.py` L161: `    core_active = e1r_market_state == "UPTREND"`
- `scripts/export_e1r_v0_2_status.py` L170: `        "regime": regime,`
- `scripts/export_e1r_v0_2_status.py` L176: `            "active_condition": "UPTREND",`
- `scripts/export_e1r_v0_2_status.py` L180: `            "active_condition": "SIDEWAYS_MA_CONFLICT",`
- `scripts/export_e1r_v0_2_status.py` L191: `            "regime": str(regime_path.relative_to(ROOT)),`
- `scripts/export_e1r_v0_2_status.py` L198: `            "Core is active only in UPTREND under the current v0.2 state model.",`
- `scripts/export_e1r_v0_2_status.py` L199: `            "Sidecar is active only in SIDEWAYS_MA_CONFLICT when holdings are available.",`
- `scripts/export_e1r_v0_2_status.py` L209: `    print("regime:", status["regime"])`
- `src/export/export_json.py` L38: `    字段名匹配 trend_state.py 实际输出。"""`
- `src/export/export_json.py` L59: `            "trend_state":    s.get("trend_state"),`
- `src/export/export_json.py` L110: `        state = s.get("trend_state", "Broken Trend")`
- `src/export/export_json.py` L120: `                "trend_state":    state,`
- `src/export/export_json.py` L127: `    write_json(EXPORT_LIFECYCLE, {**meta, "regimes": groups})`
- `scripts/run_e1r_v0_2_forward_performance_core.py` L281: `    regime = first_existing(status.get("regime"), scaffold_summary.get("regime"), status.get("market_state"), default="UNKNOWN")`
- `scripts/run_e1r_v0_2_forward_performance_core.py` L283: `    market_state = first_existing(status.get("market_state"), scaffold_summary.get("market_state"), regime, default="UNKNOWN")`
- `scripts/run_e1r_v0_2_forward_performance_core.py` L310: `            "regime": regime,`
- `scripts/run_e1r_v0_2_forward_performance_core.py` L349: `        "regime": regime,`
- `scripts/run_e1r_v0_2_oos_core.py` L40: `    regime = status.get("regime")`
- `scripts/run_e1r_v0_2_oos_core.py` L60: `        "regime": regime,`
- `scripts/run_e1r_v0_2_oos_core.py` L84: `        "regime": regime,`
- `scripts/run_e1r_v0_2_oos_core.py` L108: `                "source": "SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",`
- `src/engine/backtest.py` L85: `    # qualified_states：允许的 trend_state`
- `src/engine/backtest.py` L104: `def is_broken_trend(trend_state: str) -> bool:`
- `src/engine/backtest.py` L109: `    return str(trend_state).strip().lower() in {`
- `src/engine/backtest.py` L804: `    e1r_regime_wiring_enabled = bool(a.get("e1r_regime_wiring_enabled", False))`
- `src/engine/backtest.py` L806: `    e1r_regime_daily = a.get("e1r_regime_daily", {}) or {}`
- `src/engine/backtest.py` L808: `    def _e1r_regime_on(date: str) -> str:`
- `src/engine/backtest.py` L809: `        if not e1r_regime_wiring_enabled or not date:`
- `src/engine/backtest.py` L811: `        rec = e1r_regime_daily.get(date, {})`
- `src/engine/backtest.py` L813: `            return rec.get("regime") or rec.get("spx_regime") or rec.get("weekly_regime") or "UNCLASSIFIED"`
- `src/engine/backtest.py` L818: `    def _e1r_mode_for_regime(regime: str) -> str:`
- `src/engine/backtest.py` L819: `        if regime == "UPTREND":`
- `src/engine/backtest.py` L820: `            return "UPTREND_EMERGING_CONFIRMED_ENABLED"`
- `src/engine/backtest.py` L821: `        if regime == "SIDEWAYS":`
- `src/engine/backtest.py` L822: `            return "SIDEWAYS_QUALITY_BREAKOUT_ONLY"`
- `src/engine/backtest.py` L823: `        if regime == "DOWNTREND":`
- `src/engine/backtest.py` L824: `            return "DOWNTREND_EXCEPTION_ONLY"`
- `src/engine/backtest.py` L825: `        if regime == "N/A":`

## Diagnosis

- Top candidate generator: scripts/export_e1r_v0_2_status.py score=21.
- At least one candidate generator mentions regime/trend source terms.
- Current market_state schema exposes risk/state but not trend_state/regime.

## Open Questions

- Which candidate actually writes exports/market_state.json in the daily pipeline?
- Does that candidate have safe access to data/research/e1_5y/regimes/spx_regime_daily.json?
- Would adding trend_state to market_state.json be lower risk than sourcing dashboard Trend State directly from e1r_v0_2_status.json?

