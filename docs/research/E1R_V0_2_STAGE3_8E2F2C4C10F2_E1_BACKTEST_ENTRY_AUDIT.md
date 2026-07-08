# Stage 3.8E-2F-2C-4C-10F-2 E1 Backtest Entry Audit

Generated At: `2026-07-08T12:22:51.393428+00:00`

## Status

- Status: `E1_BACKTEST_ENTRY_AUDIT_COMPLETE_NO_EXPORTS_WRITTEN`
- Direct backtest command ok: `False`
- Module import ok: `True`
- Strategy files unchanged: `True`
- Canonical existence unchanged: `True`

## Diagnosis

- Direct backtest command ok: False.
- Backtest module import ok: True.
- Frozen strategy files unchanged: True.
- Canonical export existence unchanged: True.
- E1 loop/export candidate functions found: 2.
- Direct command final error line: ImportError: attempted relative import with no known parent package
- Backtest date literals: 2021-06-11, 2023-11-06, 2024-12-03, 2024-12-31, 2026-06-11, 2026-06-18
- Top E1 loop/export candidate: run_stateful_simulation line 763 score=42.
- Next step should fix command/import/entry failure or call internal functions via an export-only wrapper.

## Direct Run

```json
{
  "cmd": [
    "/Library/Developer/CommandLineTools/usr/bin/python3",
    "src/engine/backtest.py"
  ],
  "returncode": 1,
  "ok": false,
  "stdout_tail": "",
  "stderr_tail": "Traceback (most recent call last):\n  File \"/Users/dongfang/Downloads/sp500-tracker-v13/src/engine/backtest.py\", line 19, in <module>\n    from ..features.rs import period_return, rs_percentile\nImportError: attempted relative import with no known parent package\n"
}
```

## Module Import

```json
{
  "import_ok": true,
  "public_names": [
    "LAYER_D_ASSUMPTIONS",
    "Path",
    "annotations",
    "calc_leader_score",
    "calc_momentum",
    "calc_trend_health",
    "forward_return",
    "is_broken_trend",
    "json",
    "linreg_slope",
    "logger",
    "math",
    "momentum_acceleration",
    "moving_average",
    "period_return",
    "rs_percentile",
    "run_action_forward_validation",
    "run_full_backtest",
    "run_leader_engine_validation",
    "run_promotion_engine_validation",
    "run_stateful_simulation",
    "run_strategy_variant_comparison",
    "run_trade_rule_validation",
    "trade_action",
    "trade_action_reason"
  ],
  "callables": {
    "Path": {
      "type": "type",
      "signature": "(*args, **kwargs)"
    },
    "calc_leader_score": {
      "type": "function",
      "signature": "(rs: 'float', mom: 'float', th: 'float') -> 'float'"
    },
    "calc_momentum": {
      "type": "function",
      "signature": "(prices: 'list[float]', all_ret20: 'list[float]' = None, all_ret60: 'list[float]' = None, all_ma50_slopes: 'list[float]' = None) -> 'dict'"
    },
    "calc_trend_health": {
      "type": "function",
      "signature": "(prices: 'list[float]') -> 'dict'"
    },
    "forward_return": {
      "type": "function",
      "signature": "(prices: 'list[float]', t: 'int', days: 'int') -> 'float | None'"
    },
    "is_broken_trend": {
      "type": "function",
      "signature": "(trend_state: 'str') -> 'bool'"
    },
    "linreg_slope": {
      "type": "function",
      "signature": "(values: 'list[float]') -> 'float'"
    },
    "momentum_acceleration": {
      "type": "function",
      "signature": "(prices: 'list[float]', lookback: 'int' = 5) -> 'float'"
    },
    "moving_average": {
      "type": "function",
      "signature": "(prices: 'list[float]', window: 'int') -> 'list[float]'"
    },
    "period_return": {
      "type": "function",
      "signature": "(prices: 'list[float]', window: 'int') -> 'float | None'"
    },
    "rs_percentile": {
      "type": "function",
      "signature": "(symbol_return: 'float', all_returns: 'list[float]') -> 'float'"
    },
    "run_action_forward_validation": {
      "type": "function",
      "signature": "(symbols: 'list[str]', prices_map: 'dict[str, list[float]]', spx_prices: 'list[float]', dates_map: 'dict[str, list[str]] | None' = None, spx_dates: 'list[str] | None' = None, forward_days: 'list[int]' = [5, 10, 20, 30], step: 'int' = 5, min_history: 'int' = 120, market_score_default: 'float' = 60.0) -> 'dict'"
    },
    "run_full_backtest": {
      "type": "function",
      "signature": "(symbols: 'list[str]', prices_map: 'dict[str, list[float]]', spx_prices: 'list[float]', dates_map: 'dict[str, list[str]]' = None, spx_dates: 'list[str]' = None, run_layer_b: 'bool' = False, run_layer_d: 'bool' = True, ndx_prices: 'list[float]' = None, ndx_dates: 'list[str]' = None, sox_prices: 'list[float]' = None, sox_dates: 'list[str]' = None, vix_prices: 'list[float]' = None, vix_dates: 'list[str]' = None) -> 'dict'"
    },
    "run_leader_engine_validation": {
      "type": "function",
      "signature": "(symbols: 'list[str]', prices_map: 'dict[str, list[float]]', spx_prices: 'list[float]', forward_days: 'list[int]' = [5, 10, 20, 30], step: 'int' = 5, min_history: 'int' = 120) -> 'dict'"
    },
    "run_promotion_engine_validation": {
      "type": "function",
      "signature": "(symbols: 'list[str]', prices_map: 'dict[str, list[float]]', spx_prices: 'list[float]', promotion_thresholds: 'list[int]' = [80, 85, 90], track_days: 'list[int]' = [5, 10, 20, 30], step: 'int' = 5, min_history: 'int' = 120) -> 'dict'"
    },
    "run_stateful_simulation": {
      "type": "function",
      "signature": "(symbols: 'list[str]', prices_map: 'dict[str, list[float]]', dates_map: 'dict[str, list[str]]', spx_prices: 'list[float]', spx_dates: 'list[str]', ohlc_map: 'dict' = None, assumptions: 'dict' = None, step: 'int' = 1, min_history: 'int' = 120, market_score_default: 'float' = 60.0, sim_start_date: 'str' = None, sim_end_date: 'str' = None, ndx_prices: 'list' = None, ndx_dates: 'list' = None, sox_prices: 'list' = None, sox_dates: 'list' = None, vix_prices: 'list' = None, vix_dates: 'list' = None) -> 'dict'"
    },
    "run_strategy_variant_comparison": {
      "type": "function",
      "signature": "(symbols: 'list[str]', prices_map: 'dict[str, list[float]]', dates_map: 'dict[str, list[str]]', spx_prices: 'list[float]', spx_dates: 'list[str]', ndx_prices: 'list[float]' = None, ndx_dates: 'list[str]' = None, sox_prices: 'list[float]' = None, sox_dates: 'list[str]' = None, vix_prices: 'list[float]' = None, vix_dates: 'list[str]' = None) -> 'dict'"
    },
    "run_trade_rule_validation": {
      "type": "function",
      "signature": "(symbols: 'list[str]', prices_map: 'dict[str, list[float]]', spx_prices: 'list[float]', forward_days: 'list[int]' = [5, 10, 20, 30], step: 'int' = 5, min_history: 'int' = 120, market_score_default: 'float' = 60.0) -> 'dict'"
    },
    "trade_action": {
      "type": "function",
      "signature": "(trend_state: 'str', mom_score: 'float', rs_score: 'float', price: 'float', ma50: 'float', ma50_slope: 'float', leader_score: 'float', trend_health: 'float', market_score: 'float' = 60.0, ls60_exit_mode: 'str' = 'reduce') -> 'str'"
    },
    "trade_action_reason": {
      "type": "function",
      "signature": "(trend_state: 'str', mom_score: 'float', rs_score: 'float', price: 'float', ma50: 'float', ma50_slope: 'float', leader_score: 'float', trend_health: 'float', market_score: 'float' = 60.0, ls60_exit_mode: 'str' = 'reduce') -> 'dict'"
    }
  }
}
```

## Top Loop Candidates

```json
[
  {
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
    "terms": [
      "daily_records",
      "total_equity",
      "cash",
      "positions",
      "portfolio",
      "initial_capital",
      "simulation_start_date",
      "sim_start_date",
      "market_entry_gate",
      "pending_orders"
    ],
    "score": 42
  },
  {
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
    "terms": [
      "portfolio",
      "initial_capital",
      "simulation_start_date",
      "sim_start_date",
      "2023-11-06",
      "2021-06-11",
      "data/research/e1_5y",
      "variant_results",
      "E1_AUDITED_G4_MINHOLD10",
      "MINHOLD10"
    ],
    "score": 30
  }
]
```

## Important Lines

```json
[
  {
    "line": 34,
    "terms": [
      "initial_capital"
    ],
    "text": "    \"initial_capital\":   100_000,"
  },
  {
    "line": 35,
    "terms": [
      "positions"
    ],
    "text": "    \"max_positions\":      3,"
  },
  {
    "line": 36,
    "terms": [
      "portfolio"
    ],
    "text": "    \"buy_size\":          1.0,    # Top3: 1/3 portfolio full position"
  },
  {
    "line": 37,
    "terms": [
      "portfolio"
    ],
    "text": "    \"add_size\":          0.5,    # Top3: +1/6 portfolio, used only after REDUCE if allowed"
  },
  {
    "line": 51,
    "terms": [
      "cash"
    ],
    "text": "    \"cash_yield\":        0.0,"
  },
  {
    "line": 83,
    "terms": [
      "positions"
    ],
    "text": "    # max_positions：组合最大持仓数"
  },
  {
    "line": 313,
    "terms": [
      "run_trade_rule_validation"
    ],
    "text": "def run_trade_rule_validation("
  },
  {
    "line": 595,
    "terms": [
      "run_action_forward_validation"
    ],
    "text": "def run_action_forward_validation("
  },
  {
    "line": 774,
    "terms": [
      "sim_start_date"
    ],
    "text": "    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）"
  },
  {
    "line": 796,
    "terms": [
      "positions"
    ],
    "text": "    max_pos  = a[\"max_positions\"]"
  },
  {
    "line": 801,
    "terms": [
      "initial_capital"
    ],
    "text": "    init_cap = float(a.get(\"initial_capital\", 100_000))"
  },
  {
    "line": 831,
    "terms": [
      "positions"
    ],
    "text": "            return {\"mode\": \"UPTREND_RISK_ON\", \"max_positions\": 3, \"max_total_exposure_pct\": 100.0}"
  },
  {
    "line": 833,
    "terms": [
      "positions"
    ],
    "text": "            return {\"mode\": \"SIDEWAYS_LIMITED\", \"max_positions\": 2, \"max_total_exposure_pct\": 33.3}"
  },
  {
    "line": 835,
    "terms": [
      "positions"
    ],
    "text": "            return {\"mode\": \"DOWNTREND_DEFENSIVE\", \"max_positions\": 1, \"max_total_exposure_pct\": 10.0}"
  },
  {
    "line": 837,
    "terms": [
      "positions"
    ],
    "text": "            return {\"mode\": \"N/A\", \"max_positions\": None, \"max_total_exposure_pct\": None}"
  },
  {
    "line": 838,
    "terms": [
      "positions"
    ],
    "text": "        return {\"mode\": \"UNCLASSIFIED_DEFENSIVE\", \"max_positions\": 0, \"max_total_exposure_pct\": 0.0}"
  },
  {
    "line": 951,
    "terms": [
      "sim_start_date"
    ],
    "text": "    _trade_start = sim_start_date  # None = 从 min_history 后第一天"
  },
  {
    "line": 1016,
    "terms": [
      "cash"
    ],
    "text": "    cash            = init_cap"
  },
  {
    "line": 1018,
    "terms": [
      "pending_orders"
    ],
    "text": "    pending_orders: list[dict] = []"
  },
  {
    "line": 1024,
    "terms": [
      "positions"
    ],
    "text": "        \"max_positions_reached\":    0,"
  },
  {
    "line": 1025,
    "terms": [
      "cash"
    ],
    "text": "        \"cash_insufficient\":        0,"
  },
  {
    "line": 1056,
    "terms": [
      "portfolio"
    ],
    "text": "    portfolio_action_dist = {\"HOLD\": 0, \"ADD\": 0, \"REDUCE\": 0, \"REL_REDUCE\": 0, \"EXIT\": 0, \"TP_REDUCE\": 0}"
  },
  {
    "line": 1081,
    "terms": [
      "daily_records"
    ],
    "text": "    daily_records: list[dict]  = []"
  },
  {
    "line": 1112,
    "terms": [
      "pending_orders"
    ],
    "text": "            pending_orders = []   # 不生成订单"
  },
  {
    "line": 1120,
    "terms": [
      "pending_orders"
    ],
    "text": "        for order in pending_orders:"
  },
  {
    "line": 1138,
    "terms": [
      "cash"
    ],
    "text": "                port_val = cash + sum("
  },
  {
    "line": 1148,
    "terms": [
      "positions"
    ],
    "text": "                        skip_reasons[\"max_positions_reached\"] += 1"
  },
  {
    "line": 1156,
    "terms": [
      "cash"
    ],
    "text": "                    if target > cash:"
  },
  {
    "line": 1157,
    "terms": [
      "cash"
    ],
    "text": "                        if cash * 0.99 < 10:"
  },
  {
    "line": 1158,
    "terms": [
      "cash"
    ],
    "text": "                            skip_reasons[\"cash_insufficient\"] += 1"
  },
  {
    "line": 1160,
    "terms": [
      "cash"
    ],
    "text": "                        target = cash * 0.99"
  },
  {
    "line": 1163,
    "terms": [
      "cash"
    ],
    "text": "                    cash  -= shares * exec_price"
  },
  {
    "line": 1213,
    "terms": [
      "cash"
    ],
    "text": "                    if target_add > cash:"
  },
  {
    "line": 1214,
    "terms": [
      "cash"
    ],
    "text": "                        if cash * 0.99 < 10:"
  },
  {
    "line": 1215,
    "terms": [
      "cash"
    ],
    "text": "                            skip_reasons[\"cash_insufficient\"] += 1"
  },
  {
    "line": 1217,
    "terms": [
      "cash"
    ],
    "text": "                        target_add = cash * 0.99"
  },
  {
    "line": 1228,
    "terms": [
      "cash"
    ],
    "text": "                    cash -= target_add"
  },
  {
    "line": 1264,
    "terms": [
      "cash"
    ],
    "text": "                    cash    += proceeds"
  },
  {
    "line": 1321,
    "terms": [
      "cash"
    ],
    "text": "                    cash            += sell_shares * exec_price"
  },
  {
    "line": 1356,
    "terms": [
      "positions"
    ],
    "text": "            _today_regime_for_positions = _e1r_regime_on(date_t)"
  },
  {
    "line": 1359,
    "terms": [
      "positions"
    ],
    "text": "                _weights[_today_regime_for_positions] = _weights.get(_today_regime_for_positions, 0) + 1"
  },
  {
    "line": 1361,
    "terms": [
      "total_equity",
      "cash"
    ],
    "text": "        total_equity = cash + position_value"
  },
  {
    "line": 1364,
    "terms": [
      "cash"
    ],
    "text": "        if cash < -1.0:"
  },
  {
    "line": 1365,
    "terms": [
      "cash"
    ],
    "text": "            logger.warn(f\"  {date_t}: negative cash={cash:.2f}\")"
  },
  {
    "line": 1366,
    "terms": [
      "cash"
    ],
    "text": "            cash = 0.0"
  },
  {
    "line": 1367,
    "terms": [
      "total_equity"
    ],
    "text": "        if position_value > total_equity * 1.02:"
  },
  {
    "line": 1370,
    "terms": [
      "total_equity"
    ],
    "text": "        equity_curve.append(total_equity)"
  },
  {
    "line": 1377,
    "terms": [
      "pending_orders"
    ],
    "text": "        # STEP 3: 生成 T 日信号 → pending_orders for T+1"
  },
  {
    "line": 1462,
    "terms": [
      "cash"
    ],
    "text": "            _cash_mode = ("
  },
  {
    "line": 1468,
    "terms": [
      "cash"
    ],
    "text": "            if _cash_mode:"
  },
  {
    "line": 1498,
    "terms": [
      "total_equity"
    ],
    "text": "            daily_equity_records[-1][\"total_equity\"]"
  },
  {
    "line": 1502,
    "terms": [
      "total_equity"
    ],
    "text": "            (total_equity / _prev_equity - 1) * 100"
  },
  {
    "line": 1505,
    "terms": [
      "total_equity"
    ],
    "text": "        daily_equity_peak = max(daily_equity_peak, total_equity)"
  },
  {
    "line": 1507,
    "terms": [
      "total_equity"
    ],
    "text": "            (daily_equity_peak - total_equity) / daily_equity_peak * 100"
  },
  {
    "line": 1517,
    "terms": [
      "cash"
    ],
    "text": "            \"cash\": round(cash, 2),"
  },
  {
    "line": 1518,
    "terms": [
      "positions"
    ],
    "text": "            \"positions_value\": round(position_value, 2),"
  },
  {
    "line": 1519,
    "terms": [
      "total_equity"
    ],
    "text": "            \"total_equity\": round(total_equity, 2),"
  },
  {
    "line": 1522,
    "terms": [
      "total_equity"
    ],
    "text": "            \"exposure_pct\": round(position_value / total_equity * 100, 2) if total_equity > 0 else 0.0,"
  },
  {
    "line": 1523,
    "terms": [
      "positions"
    ],
    "text": "            \"open_positions_count\": len(holdings),"
  },
  {
    "line": 1524,
    "terms": [
      "pending_orders"
    ],
    "text": "            \"pending_orders_count\": len(pending_orders),"
  },
  {
    "line": 1622,
    "terms": [
      "cash"
    ],
    "text": "        # This does not change buy_orders, management_orders, holdings, or cash."
  },
  {
    "line": 1775,
    "terms": [
      "portfolio"
    ],
    "text": "                if action in portfolio_action_dist:"
  },
  {
    "line": 1776,
    "terms": [
      "portfolio"
    ],
    "text": "                    portfolio_action_dist[action] += 1"
  },
  {
    "line": 1871,
    "terms": [
      "positions"
    ],
    "text": "                    # Gate OFF 时依赖 STEP 1 执行层的 max_positions_reached 检查"
  },
  {
    "line": 2134,
    "terms": [
      "pending_orders"
    ],
    "text": "        pending_orders = management_orders + buy_orders"
  },
  {
    "line": 2143,
    "terms": [
      "cash"
    ],
    "text": "                f\"day={spx_day_return*100:+.1f}% cash={cash:.0f} \""
  },
  {
    "line": 2148,
    "terms": [
      "daily_records"
    ],
    "text": "            daily_records.append({"
  },
  {
    "line": 2150,
    "terms": [
      "cash"
    ],
    "text": "                \"cash\":           round(cash, 2),"
  },
  {
    "line": 2152,
    "terms": [
      "total_equity"
    ],
    "text": "                \"total_equity\":   round(total_equity, 2),"
  },
  {
    "line": 2154,
    "terms": [
      "pending_orders"
    ],
    "text": "                \"pending_orders\": len(pending_orders),"
  },
  {
    "line": 2196,
    "terms": [
      "cash"
    ],
    "text": "        cash    += h[\"shares\"] * exec_price"
  },
  {
    "line": 2233,
    "terms": [
      "cash"
    ],
    "text": "    final_equity = cash"
  },
  {
    "line": 2238,
    "terms": [
      "cash"
    ],
    "text": "        \"cash\": round(cash, 2),"
  },
  {
    "line": 2239,
    "terms": [
      "positions"
    ],
    "text": "        \"positions_value\": 0.0,"
  },
  {
    "line": 2240,
    "terms": [
      "total_equity"
    ],
    "text": "        \"total_equity\": round(final_equity, 2),"
  },
  {
    "line": 2241,
    "terms": [
      "positions"
    ],
    "text": "        \"open_positions_count\": 0,"
  },
  {
    "line": 2402,
    "terms": [
      "cash"
    ],
    "text": "            \"note\": \"Partial reduction releases cash but does not free a Max3 symbol slot.\","
  },
  {
    "line": 2404,
    "terms": [
      "market_entry_gate"
    ],
    "text": "        \"market_entry_gate\": {"
  },
  {
    "line": 2420,
    "terms": [
      "simulation_start_date",
      "sim_start_date"
    ],
    "text": "            \"simulation_start_date\": sim_start_date,"
  },
  {
    "line": 2438,
    "terms": [
      "initial_capital"
    ],
    "text": "        \"initial_capital\":   init_cap,"
  },
  {
    "line": 2456,
    "terms": [
      "pending_orders"
    ],
    "text": "        \"pending_orders_executed\":  orders_executed,"
  },
  {
    "line": 2457,
    "terms": [
      "pending_orders"
    ],
    "text": "        \"pending_orders_skipped\":   sum(skip_reasons.values()),"
  },
  {
    "line": 2459,
    "terms": [
      "portfolio"
    ],
    "text": "        \"portfolio_action_distribution\":      portfolio_action_dist,"
  },
  {
    "line": 2476,
    "terms": [
      "daily_records"
    ],
    "text": "        \"daily_records\":     daily_records,"
  },
  {
    "line": 2503,
    "terms": [
      "portfolio"
    ],
    "text": "    Run four diagnostic portfolio variants using Strict Top3, no fixed TP."
  },
  {
    "line": 2552,
    "terms": [
      "data/research/e1_5y"
    ],
    "text": "        regime_path = Path(\"data/research/e1_5y/regimes/spx_regime_daily.json\")"
  },
  {
    "line": 2568,
    "terms": [
      "E1_AUDITED_G4_MINHOLD10",
      "MINHOLD10"
    ],
    "text": "        \"E1_AUDITED_G4_MINHOLD10\": {"
  },
  {
    "line": 2590,
    "terms": [
      "data/research/e1_5y"
    ],
    "text": "            \"e1r_regime_source\":     \"data/research/e1_5y/regimes/spx_regime_daily.json\","
  },
  {
    "line": 2606,
    "terms": [
      "sim_start_date"
    ],
    "text": "    # 只用 sim_start_date / sim_end_date 控制交易执行和统计区间。"
  },
  {
    "line": 2612,
    "terms": [
      "sim_start_date",
      "2021-06-11"
    ],
    "text": "                \"sim_start_date\": \"2021-06-11\","
  },
  {
    "line": 2620,
    "terms": [
      "sim_start_date",
      "2023-11-06"
    ],
    "text": "                \"sim_start_date\": \"2023-11-06\","
  },
  {
    "line": 2625,
    "terms": [
      "sim_start_date"
    ],
    "text": "                \"sim_start_date\": \"2024-12-03\","
  },
  {
    "line": 2630,
    "terms": [
      "sim_start_date",
      "2023-11-06"
    ],
    "text": "                \"sim_start_date\": \"2023-11-06\","
  },
  {
    "line": 2653,
    "terms": [
      "sim_start_date"
    ],
    "text": "                sim_start_date=period_cfg[\"sim_start_date\"],"
  },
  {
    "line": 2690,
    "terms": [
      "variant_results"
    ],
    "text": "    variant_results = period_results[_full_period_key][\"variants\"]"
  },
  {
    "line": 2710,
    "terms": [
      "variant_results"
    ],
    "text": "        _core_e1r = variant_results.get(\"E1R_REGIME_AWARE_V0_1\")"
  },
  {
    "line": 2713,
    "terms": [
      "data/research/e1_5y"
    ],
    "text": "        _stock_dir = Path(\"data/research/e1_5y/raw/stocks\")"
  },
  {
    "line": 2714,
    "terms": [
      "data/research/e1_5y"
    ],
    "text": "        _spx_path = Path(\"data/research/e1_5y/raw/indices/SPX.json\")"
  },
  {
    "line": 2715,
    "terms": [
      "data/research/e1_5y"
    ],
    "text": "        _regime_path = Path(\"data/research/e1_5y/regimes/spx_regime_daily.json\")"
  },
  {
    "line": 2726,
    "terms": [
      "initial_capital"
    ],
    "text": "                initial_equity=float(base.get(\"initial_capital\", 100000)),"
  },
  {
    "line": 2737,
    "terms": [
      "variant_results"
    ],
    "text": "            variant_results[\"E1R_REGIME_AWARE_V0_2\"] = compose_e1r_v0_2_variant("
  },
  {
    "line": 2740,
    "terms": [
      "initial_capital"
    ],
    "text": "                initial_equity=float(base.get(\"initial_capital\", 100000)),"
  },
  {
    "line": 2778,
    "terms": [
      "variant_results"
    ],
    "text": "    selected_id, selected_result = max(variant_results.items(), key=selection_key)"
  },
  {
    "line": 2780,
    "terms": [
      "variant_results"
    ],
    "text": "    for variant_id, result in variant_results.items():"
  },
  {
    "line": 2829,
    "terms": [
      "variant_results"
    ],
    "text": "    for vid, res in variant_results.items():"
  },
  {
    "line": 2870,
    "terms": [
      "variant_results"
    ],
    "text": "        \"variant_results\": variant_results,"
  },
  {
    "line": 2887,
    "terms": [
      "simulation_start_date",
      "sim_start_date"
    ],
    "text": "                        \"sim_start_date\":   r.get(\"sample_validity\", {}).get(\"simulation_start_date\"),"
  },
  {
    "line": 2934,
    "terms": [
      "run_trade_rule_validation"
    ],
    "text": "    results[\"layer_c\"] = run_trade_rule_validation("
  },
  {
    "line": 2939,
    "terms": [
      "run_action_forward_validation"
    ],
    "text": "    results[\"layer_c2\"] = run_action_forward_validation("
  }
]
```

## Source Heads for Top Candidates

### `run_stateful_simulation` line `763` score `42`

```python
def run_stateful_simulation(
    symbols:        list[str],
    prices_map:     dict[str, list[float]],
    dates_map:      dict[str, list[str]],
    spx_prices:     list[float],
    spx_dates:      list[str],
    ohlc_map:       dict = None,
    assumptions:    dict = None,
    step:           int  = 1,
    min_history:    int  = 120,
    market_score_default: float = 60.0,
    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）
    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）
    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）
    ndx_dates:      list = None,
    sox_prices:     list = None,  # SOX 收盘价
    sox_dates:      list = None,
    vix_prices:     list = None,  # VIX 收盘价
    vix_dates:      list = None,
) -> dict:
    """
    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop

    修正项（相比 v3）：
    1. SPX master calendar — 时间轴以 SPX dates 为准
    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐
    3. skipped_orders_by_reason — 跳过原因分类统计
    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE
    """
    logger.info("[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop Backtest...")

    # ── 冻结参数 ─────────────────────────────────────────
    a        = assumptions or LAYER_D_ASSUMPTIONS
    max_pos  = a["max_positions"]
    buy_pct  = a["buy_size"]  / max_pos       # Top3: 1/3 per full slot
    add_pct  = a["add_size"]  / max_pos       # Top3: +1/6, only useful after REDUCE
    max_pct  = a["max_single_size"] / max_pos # Top3: max 1/3 per position
    one_way  = a["total_one_way"]             # 0.001
    init_cap = float(a.get("initial_capital", 100_000))
    strategy_variant = a.get("strategy_variant", "top3_entry_rs_minhold_relstop")
    e1r_shell_mode = bool(a.get("e1r_shell_mode", False))
    e1r_regime_wiring_enabled = bool(a.get("e1r_regime_wiring_enabled", False))
    e1r_uptrend_execution_enabled = bool(a.get("e1r_uptrend_execution_enabled", False))
    e1r_regime_daily = a.get("e1r_regime_daily", {}) or {}

    def _e1r_regime_on(date: str) -> str:
        if not e1r_regime_wiring_enabled or not date:
            return "N/A"
        rec = e1r_regime_daily.get(date, {})
        if isinstance(rec, dict):
            return rec.get("regime") or rec.get("spx_regime") or rec.get("weekly_regime") or "UNCLASSIFIED"
        if isinstance(rec, str):
            return rec
        return "UNCLASSIFIED"

    def _e1r_mode_for_regime(regime: str) -> str:
        if regime == "UPTREND":
            return "UPTREND_EMERGING_CONFIRMED_ENABLED"
        if regime == "SIDEWAYS":
            return "SIDEWAYS_QUALITY_BREAKOUT_ONLY"
        if regime == "DOWNTREND":
            return "DOWNTREND_EXCEPTION_ONLY"
        if regime == "N/A":
            return "N/A"
        return "UNCLASSIFIED_NO_RISK_EXPANSION"

    def _e1r_risk_budget_for_regime(regime: str) -> dict:
        if regime == "UPTREND":
            return {"mode": "UPTREND_RISK_ON", "max_positions": 3, "max_total_exposure_pct": 100.0}
        if regime == "SIDEWAYS":
            return {"mode": "SIDEWAYS_LIMITED", "max_positions": 2, "max_total_exposure_pct": 33.3}
        if regime == "DOWNTREND":
            return {"mode": "DOWNTREND_DEFENSIVE", "max_positions": 1, "max_total_exposure_pct": 10.0}
        if regime == "N/A":
            return {"mode": "N/A", "max_positions": None, "max_total_exposure_pct": None}
        return {"mode": "UNCLASSIFIED_DEFENSIVE", "max_positions": 0, "max_total_exposure_pct": 0.0}

    def _e1r_dominant_regime(weights: dict) -> str:
        if not weights:
            return "UNCLASSIFIED" if e1r_regime_wiring_enabled else "N/A"
        return max(weights.items(), key=lambda kv: kv[1])[0]

    entry_top_n = int(a.get("entry_top_n", 3))
    rank_based_exit = bool(a.get("rank_based_exit", False))
    market_gate_enabled = bool(a.get("market_gate_enabled", True))
    risk_off_below_spx_ma50 = bool(a.get("risk_off_below_spx_ma50", True))
    ls60_exit_mode = a.get("ls60_exit_mode", "reduce")  # "exit"=旧规则 "reduce"=新规则

    # Qualified Candidate Pool 参数
    candidate_top_n           = a.get("candidate_top_n", None)   # None = 沿用旧 entry_top_n
    qualified_entry_enabled   = bool(a.get("qualified_entry_enabled", False))
    qualified_rs_min          = float(a.get("qualified_rs_min", 90.0))
    qualified_momentum_min    = float(a.get("qualified_momentum_min", 85.0))
    qualified_th_min          = float(a.get("qualified_th_min", 75.0))
    qualified_states          = set(a.get("qualified_states", ["Expansion"]))
    qualified_price_above_ma50 = bool(a.get("qualified_price_above_ma50", True))
    qualified_ma50_slope_min  = float(a.get("qualified_ma50_slope_min", 0.0))

    fill_only_enabled    = bool(a.get("fill_only_enabled", False))
    gate_use_slope       = bool(a.get("gate_use_slope", True))
    gate_use_leadership  = bool(a.get("gate_use_leadership", True))

    # ── 辅助指数 Lookup（日期 → 价格）─────────────────────────
    # 用于 Gate v2 市场状态判断；缺失日期使用最近一个有效值
    def _build_lookup(dates_list, prices_list):
        """建立 date_str → price 映射"""
        m = {}
        if dates_list and prices_list:
            for d, p in zip(dates_list, prices_list):
                m[d] = p
        return m

    ndx_lookup = _build_lookup(ndx_dates or [], ndx_prices or [])
    sox_lookup = _build_lookup(sox_dates or [], sox_prices or [])
    vix_lookup = _build_lookup(vix_dates or [], vix_prices or [])

    def _get_price_on(lookup, date, fallback=None):
        """获取 date 当天价格，缺失时返回 fallback"""
        return lookup.get(date, fallback)

    # SPX MA50 历史队列（用于 10日 slope 计算）
    from collections import deque
    spx_ma50_history = deque(maxlen=11)  # 存最近11个 MA50 值（今天+10天前）

    if qualified_entry_enabled:
        logger.info(f"  Qualified Pool: candidate_top_n={candidate_top_n} "
                    f"RS>={qualified_rs_min} Mom>={qualified_momentum_min} "
                    f"TH>={qualified_th_min} states={qualified_states} "
                    f"price>MA50={qualified_p
```

### `run_strategy_variant_comparison` line `2489` score `30`

```python
def run_strategy_variant_comparison(
    symbols: list[str],
    prices_map: dict[str, list[float]],
    dates_map: dict[str, list[str]],
    spx_prices: list[float],
    spx_dates: list[str],
    ndx_prices: list[float] = None,
    ndx_dates:  list[str]   = None,
    sox_prices: list[float] = None,
    sox_dates:  list[str]   = None,
    vix_prices: list[float] = None,
    vix_dates:  list[str]   = None,
) -> dict:
    """
    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.

    V0_BASE: current Strict Top3 baseline.
    V1_RS95: raise entry RS threshold from 90 to 95.
    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.
    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.

    Selection policy:
    1. Prefer PASS over PARTIAL over FAIL.
    2. Within the same status, prefer higher total return.
    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.
    """
    logger.info("[Backtest Layer D v1.6] Strategy Variant Comparison...")

    base = {
        **LAYER_D_ASSUMPTIONS,
        "market_gate_enabled": False,
        "market_shock_gate_enabled": False,
        "partial_take_profit_enabled": False,
        "block_add_after_take_profit": False,
    }
    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────
    _gate_v2_no_vix = {
        "market_gate_enabled":       True,
        "risk_off_below_spx_ma50":   True,
        "market_shock_gate_enabled": True,
        "market_shock_daily_return": -0.02,
        "candidate_top_n":           None,
        "qualified_entry_enabled":   False,
        "fill_only_enabled":         False,
    }

    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────
    _gate_g4 = {
        "market_gate_enabled":       True,
        "risk_off_below_spx_ma50":   False,
        "market_shock_gate_enabled": False,
        "market_shock_daily_return": -0.02,
        "gate_use_slope":            True,
        "gate_use_leadership":       True,
        "candidate_top_n":           None,
        "qualified_entry_enabled":   False,
        "fill_only_enabled":         False,
        "entry_top_n":               3,
        "entry_rs_min":              90.0,
        "ls60_exit_mode":            "exit",
    }

    def _load_e1r_regime_daily() -> dict:
        regime_path = Path("data/research/e1_5y/regimes/spx_regime_daily.json")
        if not regime_path.exists():
            logger.warn(f"  E1-R regime wiring: missing {regime_path}")
            return {}
        try:
            obj = json.loads(regime_path.read_text())
        except Exception as exc:
            logger.warn(f"  E1-R regime wiring: failed to load {regime_path}: {exc}")
            return {}
        daily = obj.get("daily_regime", obj) if isinstance(obj, dict) else {}
        return daily if isinstance(daily, dict) else {}

    _e1r_regime_daily = _load_e1r_regime_daily()

    variants = {
        # E1: Gate G4 + MinHold10（审计对照基准，不可修改）
        "E1_AUDITED_G4_MINHOLD10": {
            **base, **_gate_g4,
            "strategy_variant":      "E1_audited_g4_minhold10",
            "min_holding_days":      10,
            "dynamic_exit_enabled":  False,
            "relative_stop_enabled": False,
            "version":               "E1-audited-g4-minhold10",
        },
        # E1-R v0.1 shell: research candidate placeholder.
        # Shell intentionally mirrors E1 execution rules for Phase 1 so that
        # exports/backtest.json exposes the strategy ID without changing E1.
        "E1R_REGIME_AWARE_V0_1": {
            **base, **_gate_g4,
            "strategy_variant":      "E1R_regime_aware_v0_1_shell",
            "min_holding_days":      10,
            "dynamic_exit_enabled":  False,
            "relative_stop_enabled": False,
            "version":               "E1R-uptrend-execution-v0.1",
            "e1r_shell_mode":        True,
            "e1r_uptrend_execution_enabled": True,
            "e1r_regime_wiring_enabled": True,
            "e1r_regime_daily":      _e1r_regime_daily,
            "e1r_regime_source":     "data/research/e1_5y/regimes/spx_regime_daily.json",
            "e1r_spec_ref":          "docs/research/E1R_REGIME_AWARE_STRATEGY_SPEC_v0.1.md",
        },
        # E2v2: Gate G4 + Dynamic Exit v2（CAUTIOUS/CASH_MODE 下 LS<60 直接退出）
        "E2_DYNAMIC_EXIT_V2": {
            **base, **_gate_g4,
            "strategy_variant":      "E2_dynamic_exit_v2",
            "min_holding_days":      0,
            "dynamic_exit_enabled":  True,
            "relative_stop_enabled": False,
            "version":               "E2-dynamic-exit-v2",
        },
    }

    # ── 分期定义 ─────────────────────────────────────────────────
    # 时间轴保持完整（确保 warm-up / MA50 / RS 计算不失真）；
    # 只用 sim_start_date / sim_end_date 控制交易执行和统计区间。
    import os as _os
    if _os.environ.get("SP500_RESEARCH_5Y") == "1":
        periods = {
            "C_FULL_5Y_2021_06_TO_2026_06": {
                "label":          "Period C (Full 5Y): 2021-06 → 2026-06",
                "sim_start_date": "2021-06-11",
                "sim_end_date":   "2026-06-18",
            },
        }
    else:
        periods = {
            "A_2023_11_TO_2024_12": {
                "label":          "Period A: 2023-11 → 2024-12",
                "sim_start_date": "2023-11-06",
                "sim_end_date":   "2024-12-31",
            },
            "B_2024_12_TO_2026_06": {
                "label":          "Period B: 2024-12 → 2026-06",
                "sim_start_date": "2024-12-03",
                "sim_end_date":   "2026-06-11",
            },
            "C_FULL_2023_11_TO_2026_06": {
                "label":          "Period C (Full): 2023-11 → 2026-06",
                "sim_start_date": "2023-11-06",
                "sim_end_date":   "2026-06-11",
            },
        }

    # ── 逐 period × variant 跑回测 ──────────────────────────────
    period_results = {}
    for period_key, period_cfg in periods.items():
        logger.info(f"  ══ {peri
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-3`: Build export-only E1 5Y core wrapper
- Recommended action: Use the identified E1 loop/export candidate function(s). Do not modify frozen strategy logic. Create an export-only wrapper that runs E1 from 2021-06-11 to 2026-06-18 and emits one continuous portfolio daily/equity record per interval.

