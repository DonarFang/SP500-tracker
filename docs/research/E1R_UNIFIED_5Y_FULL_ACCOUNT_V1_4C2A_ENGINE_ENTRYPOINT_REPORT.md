# E1R Unified 5Y Full Account V1 — 4C-2A Engine Entrypoint Resolution

Generated At: `2026-07-09T11:14:16.999784+00:00`

## Status

- Status: `E1R_UNIFIED_ENGINE_ENTRYPOINT_RESOLUTION_COMPLETE_NO_BACKTEST`
- Full backtest run: `False`
- Strategy logic changed: `False`
- Canonical backtest written: `False`

## Import Probe

```json
{
  "ok": false,
  "error": "ImportError: attempted relative import with no known parent package",
  "traceback_tail": "Traceback (most recent call last):\n  File \"/Users/dongfang/Downloads/sp500-tracker-v13/scripts/resolve_backtest_engine_entrypoint_4c2a.py\", line 94, in try_import_backtest\n    spec.loader.exec_module(mod)\n  File \"<frozen importlib._bootstrap_external>\", line 850, in exec_module\n  File \"<frozen importlib._bootstrap>\", line 228, in _call_with_frames_removed\n  File \"/Users/dongfang/Downloads/sp500-tracker-v13/src/engine/backtest.py\", line 19, in <module>\n    from ..features.rs import period_return, rs_percentile\nImportError: attempted relative import with no known parent package\n",
  "objects": {}
}
```

## Top Entrypoint Candidates

```json
[
  {
    "source": "src/engine/backtest.py",
    "name": "run_stateful_simulation",
    "line": 763,
    "end_line": 2486,
    "args": [
      "symbols",
      "prices_map",
      "dates_map",
      "spx_prices",
      "spx_dates",
      "ohlc_map",
      "assumptions",
      "step",
      "min_history",
      "market_score_default",
      "sim_start_date",
      "sim_end_date",
      "ndx_prices",
      "ndx_dates",
      "sox_prices",
      "sox_dates",
      "vix_prices",
      "vix_dates"
    ],
    "score": 265,
    "body_head": "def run_stateful_simulation(\n    symbols:        list[str],\n    prices_map:     dict[str, list[float]],\n    dates_map:      dict[str, list[str]],\n    spx_prices:     list[float],\n    spx_dates:      list[str],\n    ohlc_map:       dict = None,\n    assumptions:    dict = None,\n    step:           int  = 1,\n    min_history:    int  = 120,\n    market_score_default: float = 60.0,\n    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）\n    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）\n    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）\n    ndx_dates:      list = None,\n    sox_prices:     list = None,  # SOX 收盘价\n    sox_dates:      list = None,\n    vix_prices:     list = None,  # VIX 收盘价\n    vix_dates:      list = None,\n) -> dict:\n    \"\"\"\n    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop\n\n    修正项（相比 v3）：\n    1. SPX master calendar — 时间轴以 SPX dates 为准\n    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐\n    3. skipped_orders_by_reason — 跳过原因分类统计\n    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE\n    \"\"\"\n    logger.info(\"[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop Backtest...\")\n\n    # ── 冻结参数 ─────────────────────────────────────────\n    a        = assumptions or LAYER_D_ASSUMPTIONS\n    max_pos  = a[\"max_positions\"]\n    buy_pct  = a[\"buy_size\"]  / max_pos       # Top3: 1/3 per full slot\n    add_pct  = a[\"add_size\"]  / max_pos       # Top3: +1/6, only useful after REDUCE\n    max_pct  = a[\"max_single_size\"] / max_pos # Top3: max 1/3 per position\n    one_way  = a[\"total_one_way\"]             # 0.001\n    init_cap = float(a.get(\"initial_capital\", 100_000))\n    strategy_variant = a.get(\"strategy_variant\", \"top3_entry_rs_minhold_relstop\")\n    e1r_shell_mode = bool(a.get(\"e1r_shell_mode\", False))\n    e1r_regime_wiring_enabled = bool(a.get(\"e1r_regime_wiring_enabled\", False))\n    e1r_uptrend_execution_enabled = bool(a.get(\"e1r_uptrend_execution_enabled\", False))\n    e1r_regime_daily = a.get(\"e1r_regime_daily\", {}) or {}\n\n    def _e1r_regime_on(date: str) -> str:\n        if not e1r_regime_wiring_enabled or not date:\n            return \"N/A\"\n        rec = e1r_regime_daily.get(date, {})\n        if isinstance(rec, dict):\n            return rec.get(\"regime\") or rec.get(\"spx_regime\") or rec.get(\"weekly_regime\") or \"UNCLASSIFIED\"\n        if isinstance(rec, str):\n            return rec\n        return \"UNCLASSIFIED\"\n\n    def _e1r_mode_for_regime(regime: str) -> str:\n        if regime == \"UPTREND\":\n            return \"UPTREND_EMERGING_CONFIRMED_ENABLED\"\n        if regime == \"SIDEWAYS\":\n            return \"SIDEWAYS_QUALITY_BREAKOUT_ONLY\"\n        if regime == \"DOWNTREND\":\n            return \"DOWNTREND_EXCEPTION_ONLY\"\n        if regime == \"N/A\":\n            return \"N/A\"\n        return \"UNCLASSIFIED_NO_RISK_EXPANSION\"\n\n    def _e1r_risk_budget_for_regime(regime: str) -> dict:\n        if regime == \"UPTREND\":\n            return {\"mode\": \"UPTREND_RISK_ON\", \"max_positions\": 3, \"max_total_exposure_pct\": 100.0}\n        if regime == \"SIDEWAYS\":\n            return {\"mode\": \"SIDEWAYS_LIMITED\", \"max_positions\": 2, \"max_total_exposure_pct\": 33.3}\n        if regime == \"DOWNTREND\":\n            return {\"mode\": \"DOWNTREND_DEFENSIVE\", \"max_positions\": 1, \"max_total_exposure_pct\": 10.0}\n        if regime == \"N/A\":\n            return {\"mode\": \"N/A\", \"max_positions\": None, \"max_total_exposure_pct\": None}\n        return {\"mode\": \"UNCLASSIFIED_DEFENSIVE\", \"max_positions\": 0, \"max_total_exposure_pct\": 0.0}\n\n    def _e1r_dominant_regime(weights: dict) -> str:\n        if not weights:\n            return \"UNCLASSIFIED\" if e1r_regime_wiring_enabled else \"N/A\""
  },
  {
    "source": "scripts/resolve_backtest_engine_entrypoint_4c2a.py",
    "name": "rank_entrypoint_candidates",
    "line": 233,
    "end_line": 277,
    "args": [
      "scans"
    ],
    "score": 155,
    "body_head": "def rank_entrypoint_candidates(scans: dict[str, Any]) -> list[dict[str, Any]]:\n    candidates = []\n\n    for path, scan in scans.items():\n        for f in scan.get(\"function_defs\", []):\n            name = f[\"name\"]\n            lower = name.lower()\n            score = f.get(\"score\", 0)\n\n            if \"stateful\" in lower:\n                score += 80\n            if \"simulation\" in lower:\n                score += 60\n            if \"portfolio\" in lower:\n                score += 50\n            if \"backtest\" in lower:\n                score += 40\n            if \"variant\" in lower:\n                score += 30\n            if name.startswith(\"run_\"):\n                score += 20\n\n            body = f.get(\"body_head\", \"\")\n            if \"daily_records\" in body:\n                score += 30\n            if \"total_equity\" in body or \"portfolio_value\" in body:\n                score += 30\n            if \"cash\" in body:\n                score += 20\n            if \"positions_value\" in body or \"market_value\" in body:\n                score += 20\n            if \"spx_regime\" in body or \"market_gate_state\" in body:\n                score += 20\n\n            candidates.append({\n                \"source\": path,\n                \"name\": name,\n                \"line\": f.get(\"line\"),\n                \"end_line\": f.get(\"end_line\"),\n                \"args\": f.get(\"args\"),\n                \"score\": score,\n                \"body_head\": body,\n            })\n\n    return sorted(candidates, key=lambda x: (-x[\"score\"], x[\"source\"], x[\"line\"]))[:40]"
  },
  {
    "source": "src/engine/backtest.py",
    "name": "run_strategy_variant_comparison",
    "line": 2489,
    "end_line": 2895,
    "args": [
      "symbols",
      "prices_map",
      "dates_map",
      "spx_prices",
      "spx_dates",
      "ndx_prices",
      "ndx_dates",
      "sox_prices",
      "sox_dates",
      "vix_prices",
      "vix_dates"
    ],
    "score": 125,
    "body_head": "def run_strategy_variant_comparison(\n    symbols: list[str],\n    prices_map: dict[str, list[float]],\n    dates_map: dict[str, list[str]],\n    spx_prices: list[float],\n    spx_dates: list[str],\n    ndx_prices: list[float] = None,\n    ndx_dates:  list[str]   = None,\n    sox_prices: list[float] = None,\n    sox_dates:  list[str]   = None,\n    vix_prices: list[float] = None,\n    vix_dates:  list[str]   = None,\n) -> dict:\n    \"\"\"\n    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.\n\n    V0_BASE: current Strict Top3 baseline.\n    V1_RS95: raise entry RS threshold from 90 to 95.\n    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.\n    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.\n\n    Selection policy:\n    1. Prefer PASS over PARTIAL over FAIL.\n    2. Within the same status, prefer higher total return.\n    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.\n    \"\"\"\n    logger.info(\"[Backtest Layer D v1.6] Strategy Variant Comparison...\")\n\n    base = {\n        **LAYER_D_ASSUMPTIONS,\n        \"market_gate_enabled\": False,\n        \"market_shock_gate_enabled\": False,\n        \"partial_take_profit_enabled\": False,\n        \"block_add_after_take_profit\": False,\n    }\n    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────\n    _gate_v2_no_vix = {\n        \"market_gate_enabled\":       True,\n        \"risk_off_below_spx_ma50\":   True,\n        \"market_shock_gate_enabled\": True,\n        \"market_shock_daily_return\": -0.02,\n        \"candidate_top_n\":           None,\n        \"qualified_entry_enabled\":   False,\n        \"fill_only_enabled\":         False,\n    }\n\n    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────\n    _gate_g4 = {\n        \"market_gate_enabled\":       True,\n        \"risk_off_below_spx_ma50\":   False,\n        \"market_shock_gate_enabled\": False,\n        \"market_shock_daily_return\": -0.02,\n        \"gate_use_slope\":            True,\n        \"gate_use_leadership\":       True,\n        \"candidate_top_n\":           None,\n        \"qualified_entry_enabled\":   False,\n        \"fill_only_enabled\":         False,\n        \"entry_top_n\":               3,\n        \"entry_rs_min\":              90.0,\n        \"ls60_exit_mode\":            \"exit\",\n    }\n\n    def _load_e1r_regime_daily() -> dict:\n        regime_path = Path(\"data/research/e1_5y/regimes/spx_regime_daily.json\")\n        if not regime_path.exists():\n            logger.warn(f\"  E1-R regime wiring: missing {regime_path}\")\n            return {}\n        try:\n            obj = json.loads(regime_path.read_text())\n        except Exception as exc:\n            logger.warn(f\"  E1-R regime wiring: failed to load {regime_path}: {exc}\")\n            return {}\n        daily = obj.get(\"daily_regime\", obj) if isinstance(obj, dict) else {}\n        return daily if isinstance(daily, dict) else {}\n\n    _e1r_regime_daily = _load_e1r_regime_daily()\n\n    variants = {\n        # E1: Gate G4 + MinHold10（审计对照基准，不可修改）\n        \"E1_AUDITED_G4_MINHOLD10\": {"
  },
  {
    "source": "scripts/export_e1_5y_core_equity.py",
    "name": "normalize_equity_rows",
    "line": 252,
    "end_line": 293,
    "args": [
      "result"
    ],
    "score": 120,
    "body_head": "def normalize_equity_rows(result: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any] | None, list[dict[str, Any]]]:\n    candidates = []\n\n    for path, rows in find_lists(result):\n        if rows and isinstance(rows[0], dict):\n            shape = shape_rows(rows, path)\n            candidates.append({\"path\": path, \"rows\": rows, \"shape\": shape})\n\n    accepted = [c for c in candidates if c[\"shape\"][\"continuity_candidate\"]]\n    if not accepted:\n        return [], None, [c[\"shape\"] for c in candidates]\n\n    best = sorted(\n        accepted,\n        key=lambda c: (c[\"shape\"][\"unique_dates\"], c[\"shape\"][\"length\"]),\n        reverse=True,\n    )[0]\n\n    clean = []\n    rows = sorted(best[\"rows\"], key=lambda r: normalize_date(r.get(\"date\") or r.get(\"interval_end_date\") or r.get(\"next_date\")) or \"\")\n\n    for r in rows:\n        d = normalize_date(r.get(\"date\") or r.get(\"interval_end_date\") or r.get(\"next_date\"))\n        eq = as_float(r.get(\"total_equity\", r.get(\"equity\", r.get(\"portfolio_value\"))))\n        if not d or eq is None:\n            continue\n\n        clean.append({\n            \"date\": d,\n            \"equity\": eq,\n            \"portfolio_value\": eq,\n            \"strategy_indexed\": eq / INITIAL_CAPITAL * 100.0,\n            \"cash\": r.get(\"cash\"),\n            \"market_value\": r.get(\"market_value\", r.get(\"positions_value\", r.get(\"position_value\", r.get(\"holdings_value\")))),\n            \"n_positions\": r.get(\"n_positions\", r.get(\"open_positions_count\", r.get(\"n_holdings\"))),\n            \"daily_return\": r.get(\"daily_return\"),\n            \"daily_return_pct\": r.get(\"daily_return_pct\"),\n            \"market_state\": r.get(\"market_state\", r.get(\"market_gate_state\", r.get(\"regime\"))),\n            \"source_row_keys\": sorted(r.keys()),\n        })\n\n    return clean, best[\"shape\"], [c[\"shape\"] for c in candidates]"
  },
  {
    "source": "scripts/build_e1_e1r_research_curve_bundle_4b0n.py",
    "name": "normalize_backtest_e1",
    "line": 104,
    "end_line": 122,
    "args": [
      "rows"
    ],
    "score": 110,
    "body_head": "def normalize_backtest_e1(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:\n    out = []\n    first = None\n    for r in rows:\n        d = get_date(r)\n        e = as_float(r.get(\"equity\") or r.get(\"portfolio_value\") or r.get(\"total_equity\"))\n        if not d or e is None:\n            continue\n        if first is None:\n            first = e\n        out.append({\n            \"date\": d,\n            \"strategy_id\": \"E1_AUDITED_G4_MINHOLD10\",\n            \"curve_type\": \"backtest_5y\",\n            \"canonical\": True,\n            \"equity\": e,\n            \"indexed\": e / first * 100.0 if first else None,\n        })\n    return out"
  },
  {
    "source": "scripts/direct_compose_e1r_candidate_4b0l.py",
    "name": "build_core_variant_result",
    "line": 132,
    "end_line": 142,
    "args": [
      "e1_obj"
    ],
    "score": 95,
    "body_head": "def build_core_variant_result(e1_obj: Any) -> dict[str, Any]:\n    rows = extract_rows(e1_obj)\n    metrics = metric_values(e1_obj if isinstance(e1_obj, dict) else {})\n    return {\n        \"source\": \"exports/e1_5y_backtest_equity_curve.json\",\n        \"candidate_input_type\": \"current_e1_5y_core_not_frozen_e1r_core\",\n        \"daily_equity_records\": rows,\n        \"daily_records\": rows,\n        \"metrics\": metrics,\n        **{k: v for k, v in metrics.items() if v is not None},\n    }"
  },
  {
    "source": "src/engine/backtest.py",
    "name": "run_full_backtest",
    "line": 2904,
    "end_line": 2978,
    "args": [
      "symbols",
      "prices_map",
      "spx_prices",
      "dates_map",
      "spx_dates",
      "run_layer_b",
      "run_layer_d",
      "ndx_prices",
      "ndx_dates",
      "sox_prices",
      "sox_dates",
      "vix_prices",
      "vix_dates"
    ],
    "score": 95,
    "body_head": "def run_full_backtest(\n    symbols:      list[str],\n    prices_map:   dict[str, list[float]],\n    spx_prices:   list[float],\n    dates_map:    dict[str, list[str]] = None,\n    spx_dates:    list[str] = None,\n    run_layer_b:  bool = False,\n    run_layer_d:  bool = True,\n    ndx_prices:   list[float] = None,\n    ndx_dates:    list[str]   = None,\n    sox_prices:   list[float] = None,\n    sox_dates:    list[str]   = None,\n    vix_prices:   list[float] = None,\n    vix_dates:    list[str]   = None,\n) -> dict:\n    \"\"\"\n    运行完整4层回测验证（A → C → D → B）。\n    返回汇总结果，供 export_json 写入 backtest.json。\n    \"\"\"\n    logger.info(\"=== 开始回测验证（Backtest Methodology v1.0）===\")\n    dates_map  = dates_map  or {}\n    spx_dates  = spx_dates  or []\n    results    = {}\n\n    # Layer A: Leader Engine（最基础）\n    results[\"layer_a\"] = run_leader_engine_validation(\n        symbols, prices_map, spx_prices\n    )\n\n    # Layer C: Trade Rule Signal Validation\n    results[\"layer_c\"] = run_trade_rule_validation(\n        symbols, prices_map, spx_prices\n    )\n\n    # Layer C2: Action Forward Return Validation\n    results[\"layer_c2\"] = run_action_forward_validation(\n        symbols=symbols,\n        prices_map=prices_map,\n        spx_prices=spx_prices,\n        dates_map=dates_map,\n        spx_dates=spx_dates,\n    )\n\n    # Layer D: 4-variant strategy comparison; selected result remains top-level compatible\n    if run_layer_d:\n        results[\"layer_d\"] = run_strategy_variant_comparison(\n            symbols, prices_map, dates_map, spx_prices, spx_dates,\n            ndx_prices=ndx_prices or [], ndx_dates=ndx_dates or [],\n            sox_prices=sox_prices or [], sox_dates=sox_dates or [],\n            vix_prices=vix_prices or [], vix_dates=vix_dates or [],\n        )\n\n    # Layer B: Promotion Engine（需要历史快照，可选）\n    if run_layer_b:\n        results[\"layer_b\"] = run_promotion_engine_validation(\n            symbols, prices_map, spx_prices\n        )\n\n    # 整体评分\n    statuses = [v[\"status\"] for v in results.values()]\n    overall = \"PASS\"     if all(s == \"PASS\" for s in statuses) else \\\n              \"PROMISING\" if (sum(s == \"PASS\" for s in statuses) >= 2 or\n                               sum(s == \"PROMISING_INSUFFICIENT_SAMPLE\" for s in statuses) >= 1) else \\\n              \"PARTIAL\"  if any(s in (\"PASS\",\"PARTIAL\") for s in statuses) else \"FAIL\"\n\n    logger.info(f\"=== 回测完成: {overall} ===\")\n    for k, v in results.items():\n        logger.info(f\"  {k.upper()}: {v['status']}\")\n\n    return {\n        \"overall_status\": overall,\n        \"methodology\":    \"Backtest Methodology v1.0\",\n        \"model_version\":  \"Quantitative Model Spec v1.0 (Frozen)\",\n        \"results\":        results,\n    }"
  },
  {
    "source": "scripts/run_e1r_v0_2_forward_performance.py",
    "name": "restore_kickoff_ready_paper_state",
    "line": 119,
    "end_line": 215,
    "args": [
      "before"
    ],
    "score": 85,
    "body_head": "def restore_kickoff_ready_paper_state(before: Dict[str, Any]) -> Dict[str, Any]:\n    before_orders = before[\"orders_doc\"]\n    before_positions = before[\"positions_doc\"]\n    before_summary = before[\"summary\"]\n    before_state = before[\"state\"]\n\n    after_summary = read_json(SUMMARY, {})\n    after_state = read_json(STATE, {})\n\n    if not isinstance(before_summary, dict):\n        before_summary = {}\n    if not isinstance(after_summary, dict):\n        after_summary = {}\n    if not isinstance(before_state, dict):\n        before_state = {}\n    if not isinstance(after_state, dict):\n        after_state = {}\n\n    before_positions_list = get_positions(before_positions)\n\n    position_weight_sum = sum(to_float(p.get(\"weight\")) for p in before_positions_list if isinstance(p, dict))\n    portfolio_value = to_float(\n        before_summary.get(\"portfolio_value\")\n        or before_state.get(\"portfolio_value\")\n        or after_summary.get(\"portfolio_value\"),\n        100000.0,\n    )\n    market_value = portfolio_value * position_weight_sum\n    cash = portfolio_value - market_value\n\n    # Preserve official paper orders/positions exactly as accepted in 1E-4.\n    write_json(ORDERS, before_orders)\n    write_json(POSITIONS, before_positions)\n\n    # Preserve kickoff semantics and accepted paper-position fields.\n    preserved_summary = {\n        **after_summary,\n        \"strategy_id\": STRATEGY_ID,\n        \"tracking_status\": \"KICKOFF_READY\",\n        \"official_kickoff_date\": None,\n        \"forward_start_date\": None,\n        \"execution_status\": before_summary.get(\"execution_status\", \"PAPER_POSITIONS_READY_KICKOFF_PENDING\"),\n        \"open_positions_count\": count_positions(before_positions),\n        \"paper_orders_count\": count_orders(before_orders),\n        \"executed_orders_count\": before_summary.get(\"executed_orders_count\", 0),\n        \"number_of_trades\": before_summary.get(\"number_of_trades\", 0),\n        \"gross_exposure\": position_weight_sum,\n        \"net_exposure\": position_weight_sum,\n        \"core_exposure\": before_summary.get(\"core_exposure\", position_weight_sum),\n        \"sidecar_exposure\": before_summary.get(\"sidecar_exposure\", 0.0),\n        \"cash\": cash,\n        \"market_value\": market_value,\n        \"portfolio_value\": portfolio_value,\n        \"equity\": portfolio_value,\n        \"preservation_guard\": {\n            \"active\": True,\n            \"reason\": \"KICKOFF_READY paper orders/positions must not be erased before LIVE_FORWARD.\",\n            \"preserved_at\": now_iso(),\n            \"core_script\": str(CORE_SCRIPT.relative_to(ROOT)),\n        },\n    }\n\n    notes = preserved_summary.get(\"notes\")\n    if not isinstance(notes, list):\n        notes = []\n    notes.append(\"Stage 3.8E-2F-1F-1B preservation guard restored accepted paper orders/positions after forward performance run.\")\n    preserved_summary[\"notes\"] = notes\n\n    preserved_state = {\n        **after_state,\n        \"strategy_id\": STRATEGY_ID,\n        \"tracking_status\": \"KICKOFF_READY\",\n        \"official_kickoff_date\": None,\n        \"forward_start_date\": None,\n        \"execution_status\": preserved_summary[\"execution_status\"],\n        \"positions\": before_positions_list,\n        \"cash\": cash,\n        \"market_value\": market_value,\n        \"portfolio_value\": portfolio_value,\n        \"equity\": portfolio_value,"
  },
  {
    "source": "scripts/run_e1r_v0_2_oos.py",
    "name": "restore_paper_state",
    "line": 109,
    "end_line": 203,
    "args": [
      "before"
    ],
    "score": 85,
    "body_head": "def restore_paper_state(before: Dict[str, Any]) -> Dict[str, Any]:\n    before_orders_doc = before[\"orders_doc\"]\n    before_positions_doc = before[\"positions_doc\"]\n    before_summary = before[\"summary\"] if isinstance(before[\"summary\"], dict) else {}\n    before_state = before[\"state\"] if isinstance(before[\"state\"], dict) else {}\n\n    after_summary = read_json(SUMMARY, {})\n    after_state = read_json(STATE, {})\n\n    if not isinstance(after_summary, dict):\n        after_summary = {}\n    if not isinstance(after_state, dict):\n        after_state = {}\n\n    orders = get_orders(before_orders_doc)\n    positions = get_positions(before_positions_doc)\n\n    position_weight_sum = sum(to_float(p.get(\"weight\")) for p in positions)\n    portfolio_value = to_float(\n        before_summary.get(\"portfolio_value\")\n        or before_state.get(\"portfolio_value\")\n        or after_summary.get(\"portfolio_value\"),\n        100000.0,\n    )\n    market_value = portfolio_value * position_weight_sum\n    cash = portfolio_value - market_value\n\n    # Restore official paper exports exactly.\n    write_json(ORDERS, before_orders_doc)\n    write_json(POSITIONS, before_positions_doc)\n\n    # Merge non-paper fields from the core output, but preserve paper-state semantics.\n    preserved_summary = {\n        **after_summary,\n        \"strategy_id\": STRATEGY_ID,\n        \"tracking_status\": \"KICKOFF_READY\",\n        \"official_kickoff_date\": None,\n        \"forward_start_date\": None,\n        \"execution_status\": before_summary.get(\"execution_status\", \"PAPER_POSITIONS_READY_KICKOFF_PENDING\"),\n        \"open_positions_count\": len(positions),\n        \"paper_orders_count\": len(orders),\n        \"executed_orders_count\": before_summary.get(\"executed_orders_count\", 0),\n        \"number_of_trades\": before_summary.get(\"number_of_trades\", 0),\n        \"gross_exposure\": position_weight_sum,\n        \"net_exposure\": position_weight_sum,\n        \"core_exposure\": before_summary.get(\"core_exposure\", position_weight_sum),\n        \"sidecar_exposure\": before_summary.get(\"sidecar_exposure\", 0.0),\n        \"cash\": cash,\n        \"market_value\": market_value,\n        \"portfolio_value\": portfolio_value,\n        \"equity\": portfolio_value,\n        \"preservation_guard\": {\n            \"active\": True,\n            \"guarded_script\": \"scripts/run_e1r_v0_2_oos.py\",\n            \"core_script\": str(CORE_SCRIPT.relative_to(ROOT)),\n            \"reason\": \"Preserve accepted paper orders/positions before LIVE_FORWARD.\",\n            \"preserved_at\": now_iso(),\n        },\n    }\n\n    notes = preserved_summary.get(\"notes\")\n    if not isinstance(notes, list):\n        notes = []\n    notes.append(\"Stage 3.8E-2F-1F-1E preservation guard restored accepted paper orders/positions after E1R OOS runner.\")\n    preserved_summary[\"notes\"] = notes\n\n    preserved_state = {\n        **after_state,\n        \"strategy_id\": STRATEGY_ID,\n        \"tracking_status\": \"KICKOFF_READY\",\n        \"official_kickoff_date\": None,\n        \"forward_start_date\": None,\n        \"execution_status\": preserved_summary[\"execution_status\"],\n        \"positions\": positions,\n        \"cash\": cash,\n        \"market_value\": market_value,\n        \"portfolio_value\": portfolio_value,\n        \"equity\": portfolio_value,\n        \"last_summary\": preserved_summary,\n        \"updated_at\": now_iso(),"
  },
  {
    "source": "scripts/audit_e1r_v0_2_daily_like_candidates_v2.py",
    "name": "validate_portfolio_candidate",
    "line": 259,
    "end_line": 286,
    "args": [
      "stats"
    ],
    "score": 80,
    "body_head": "def validate_portfolio_candidate(stats: dict[str, Any]) -> dict[str, Any]:\n    reasons = []\n\n    checks = {\n        \"row_count_ge_1000\": (stats.get(\"parseable_equity_rows\") or 0) >= 1000,\n        \"one_row_per_date\": stats.get(\"one_row_per_date\") is True,\n        \"not_symbol_level\": (stats.get(\"symbol_row_count\") or 0) == 0,\n        \"not_diagnostic_only\": (stats.get(\"diagnostic_only_row_count\") or 0) == 0,\n        \"max_rows_per_date_eq_1\": stats.get(\"max_rows_per_date\") == 1,\n        \"total_return_close_to_frozen_1pct\": (\n            stats.get(\"total_return_abs_diff_vs_frozen\") is not None\n            and stats[\"total_return_abs_diff_vs_frozen\"] <= 1.0\n        ),\n        \"maxdd_close_to_frozen_1_5pct\": (\n            stats.get(\"maxdd_abs_diff_vs_frozen\") is not None\n            and stats[\"maxdd_abs_diff_vs_frozen\"] <= 1.5\n        ),\n    }\n\n    for k, ok in checks.items():\n        if not ok:\n            reasons.append(k)\n\n    return {\n        \"checks\": checks,\n        \"accepted_as_portfolio_daily_equity\": all(checks.values()),\n        \"rejection_reasons\": reasons,\n    }"
  },
  {
    "source": "scripts/e1r_unified_5y_full_account_preflight_4c1.py",
    "name": "build_spec",
    "line": 258,
    "end_line": 328,
    "args": [],
    "score": 80,
    "body_head": "def build_spec() -> dict[str, Any]:\n    return {\n        \"strategy_id\": \"E1R_UNIFIED_5Y_FULL_ACCOUNT_V1\",\n        \"purpose\": \"Run a single continuous 5Y full-account backtest that organically connects UPTREND, SIDEWAY
```

## Conclusion

- `BACKTEST_IMPORT_FAILED_BUT_STATIC_ENTRYPOINT_CANDIDATE_FOUND`
- Recommended: Patch import path/environment in a thin adapter, then smoke invoke top static entrypoint.

