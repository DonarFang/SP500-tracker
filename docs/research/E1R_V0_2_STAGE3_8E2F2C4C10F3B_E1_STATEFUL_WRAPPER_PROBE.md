# Stage 3.8E-2F-2C-4C-10F-3B E1 Stateful Wrapper Probe

Generated At: `2026-07-08T12:28:44.723843+00:00`

## Status

- Status: `E1_STATEFUL_WRAPPER_PROBE_COMPLETE_NO_EXPORTS_WRITTEN`
- Import/signature probe ok: `True`
- Strategy files unchanged: `True`
- Canonical existence unchanged: `True`

## Diagnosis

- Backtest import/signature probe ok: True.
- Backtest import ok: True.
- run_stateful_simulation signature: (symbols: 'list[str]', prices_map: 'dict[str, list[float]]', dates_map: 'dict[str, list[str]]', spx_prices: 'list[float]', spx_dates: 'list[str]', ohlc_map: 'dict' = None, assumptions: 'dict' = None, step: 'int' = 1, min_history: 'int' = 120, market_score_default: 'float' = 60.0, sim_start_date: 'str' = None, sim_end_date: 'str' = None, ndx_prices: 'list' = None, ndx_dates: 'list' = None, sox_prices: 'list' = None, sox_dates: 'list' = None, vix_prices: 'list' = None, vix_dates: 'list' = None) -> 'dict'.
- run_strategy_variant_comparison signature: (symbols: 'list[str]', prices_map: 'dict[str, list[float]]', dates_map: 'dict[str, list[str]]', spx_prices: 'list[float]', spx_dates: 'list[str]', ndx_prices: 'list[float]' = None, ndx_dates: 'list[str]' = None, sox_prices: 'list[float]' = None, sox_dates: 'list[str]' = None, vix_prices: 'list[float]' = None, vix_dates: 'list[str]' = None) -> 'dict'.
- Frozen strategy files unchanged: True.
- Canonical export existence unchanged: True.
- run_stateful_simulation is the preferred export-only E1 core loop candidate because it directly exposes sim_start_date and sim_end_date.
- run_strategy_variant_comparison is useful for reproducing frozen E1 variant settings, but may still use internal hardcoded windows.

## Function Signatures

```json
{
  "run_stateful_simulation": {
    "exists": true,
    "callable": true,
    "signature": "(symbols: 'list[str]', prices_map: 'dict[str, list[float]]', dates_map: 'dict[str, list[str]]', spx_prices: 'list[float]', spx_dates: 'list[str]', ohlc_map: 'dict' = None, assumptions: 'dict' = None, step: 'int' = 1, min_history: 'int' = 120, market_score_default: 'float' = 60.0, sim_start_date: 'str' = None, sim_end_date: 'str' = None, ndx_prices: 'list' = None, ndx_dates: 'list' = None, sox_prices: 'list' = None, sox_dates: 'list' = None, vix_prices: 'list' = None, vix_dates: 'list' = None) -> 'dict'"
  },
  "run_strategy_variant_comparison": {
    "exists": true,
    "callable": true,
    "signature": "(symbols: 'list[str]', prices_map: 'dict[str, list[float]]', dates_map: 'dict[str, list[str]]', spx_prices: 'list[float]', spx_dates: 'list[str]', ndx_prices: 'list[float]' = None, ndx_dates: 'list[str]' = None, sox_prices: 'list[float]' = None, sox_dates: 'list[str]' = None, vix_prices: 'list[float]' = None, vix_dates: 'list[str]' = None) -> 'dict'"
  },
  "load_json": {
    "exists": false
  },
  "load_price_series": {
    "exists": false
  },
  "load_ohlc_series": {
    "exists": false
  },
  "load_symbol_universe": {
    "exists": false
  },
  "align_dates": {
    "exists": false
  },
  "compute_market_score": {
    "exists": false
  },
  "evaluate_leader": {
    "exists": false
  }
}
```

## Important Lines

```json
[
  {
    "line": 124,
    "terms": [
      "spx_prices"
    ],
    "text": "def _rebuild_leader_score(prices: list[float], spx_prices: list[float],"
  },
  {
    "line": 131,
    "terms": [
      "spx_prices"
    ],
    "text": "    spx = spx_prices[:t+1]"
  },
  {
    "line": 178,
    "terms": [
      "prices_map"
    ],
    "text": "    prices_map: dict[str, list[float]],"
  },
  {
    "line": 179,
    "terms": [
      "spx_prices"
    ],
    "text": "    spx_prices: list[float],"
  },
  {
    "line": 200,
    "terms": [
      "spx_prices"
    ],
    "text": "    n_days = len(spx_prices)"
  },
  {
    "line": 207,
    "terms": [
      "prices_map"
    ],
    "text": "            if sym not in prices_map:"
  },
  {
    "line": 210,
    "terms": [
      "prices_map",
      "spx_prices"
    ],
    "text": "                prices_map[sym], spx_prices,"
  },
  {
    "line": 211,
    "terms": [
      "prices_map"
    ],
    "text": "                prices_map,  # 全量横截面（正式回测）"
  },
  {
    "line": 223,
    "terms": [
      "prices_map"
    ],
    "text": "            p_series = prices_map[sym]"
  },
  {
    "line": 315,
    "terms": [
      "prices_map"
    ],
    "text": "    prices_map: dict[str, list[float]],"
  },
  {
    "line": 316,
    "terms": [
      "spx_prices"
    ],
    "text": "    spx_prices: list[float],"
  },
  {
    "line": 344,
    "terms": [
      "spx_prices"
    ],
    "text": "    n_days = len(spx_prices)"
  },
  {
    "line": 350,
    "terms": [
      "spx_prices"
    ],
    "text": "            spx_ret = forward_return(spx_prices, t, days)"
  },
  {
    "line": 357,
    "terms": [
      "prices_map"
    ],
    "text": "            if sym in prices_map:"
  },
  {
    "line": 358,
    "terms": [
      "prices_map"
    ],
    "text": "                r = period_return(prices_map[sym][:t+1], 60)"
  },
  {
    "line": 363,
    "terms": [
      "prices_map"
    ],
    "text": "            if sym not in prices_map:"
  },
  {
    "line": 365,
    "terms": [
      "prices_map"
    ],
    "text": "            p = prices_map[sym][:t+1]"
  },
  {
    "line": 401,
    "terms": [
      "prices_map"
    ],
    "text": "            p_full = prices_map[sym]"
  },
  {
    "line": 473,
    "terms": [
      "prices_map"
    ],
    "text": "    prices_map: dict[str, list[float]],"
  },
  {
    "line": 474,
    "terms": [
      "spx_prices"
    ],
    "text": "    spx_prices: list[float],"
  },
  {
    "line": 492,
    "terms": [
      "spx_prices"
    ],
    "text": "    n_days = len(spx_prices)"
  },
  {
    "line": 500,
    "terms": [
      "prices_map"
    ],
    "text": "            if sym not in prices_map:"
  },
  {
    "line": 502,
    "terms": [
      "prices_map"
    ],
    "text": "            p = prices_map[sym][:t+1]"
  },
  {
    "line": 510,
    "terms": [
      "prices_map"
    ],
    "text": "            if sym not in prices_map:"
  },
  {
    "line": 512,
    "terms": [
      "prices_map"
    ],
    "text": "            p = prices_map[sym][:t+1]"
  },
  {
    "line": 544,
    "terms": [
      "prices_map"
    ],
    "text": "                        if s not in prices_map:"
  },
  {
    "line": 546,
    "terms": [
      "prices_map"
    ],
    "text": "                        fp = prices_map[s][:future_t+1]"
  },
  {
    "line": 597,
    "terms": [
      "prices_map"
    ],
    "text": "    prices_map:    dict[str, list[float]],"
  },
  {
    "line": 598,
    "terms": [
      "spx_prices"
    ],
    "text": "    spx_prices:    list[float],"
  },
  {
    "line": 599,
    "terms": [
      "dates_map"
    ],
    "text": "    dates_map:     dict[str, list[str]] | None = None,"
  },
  {
    "line": 617,
    "terms": [
      "dates_map"
    ],
    "text": "    dates_map = dates_map or {}"
  },
  {
    "line": 627,
    "terms": [
      "spx_prices"
    ],
    "text": "    n_days = len(spx_prices)"
  },
  {
    "line": 638,
    "terms": [
      "spx_prices"
    ],
    "text": "            r = forward_return(spx_prices, t, d)"
  },
  {
    "line": 643,
    "terms": [
      "prices_map"
    ],
    "text": "            (period_return(prices_map[s][:t+1], 60) or 0.0)"
  },
  {
    "line": 644,
    "terms": [
      "prices_map"
    ],
    "text": "            for s in symbols if s in prices_map and len(prices_map[s]) > t+1"
  },
  {
    "line": 648,
    "terms": [
      "prices_map"
    ],
    "text": "            if sym not in prices_map:"
  },
  {
    "line": 650,
    "terms": [
      "prices_map"
    ],
    "text": "            p = prices_map[sym][:t+1]"
  },
  {
    "line": 681,
    "terms": [
      "prices_map"
    ],
    "text": "            p_full = prices_map[sym]"
  },
  {
    "line": 763,
    "terms": [
      "run_stateful_simulation("
    ],
    "text": "def run_stateful_simulation("
  },
  {
    "line": 765,
    "terms": [
      "prices_map"
    ],
    "text": "    prices_map:     dict[str, list[float]],"
  },
  {
    "line": 766,
    "terms": [
      "dates_map"
    ],
    "text": "    dates_map:      dict[str, list[str]],"
  },
  {
    "line": 767,
    "terms": [
      "spx_prices"
    ],
    "text": "    spx_prices:     list[float],"
  },
  {
    "line": 769,
    "terms": [
      "ohlc_map"
    ],
    "text": "    ohlc_map:       dict = None,"
  },
  {
    "line": 774,
    "terms": [
      "sim_start_date"
    ],
    "text": "    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）"
  },
  {
    "line": 775,
    "terms": [
      "sim_end_date"
    ],
    "text": "    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）"
  },
  {
    "line": 776,
    "terms": [
      "ndx_prices"
    ],
    "text": "    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）"
  },
  {
    "line": 778,
    "terms": [
      "sox_prices"
    ],
    "text": "    sox_prices:     list = None,  # SOX 收盘价"
  },
  {
    "line": 780,
    "terms": [
      "vix_prices"
    ],
    "text": "    vix_prices:     list = None,  # VIX 收盘价"
  },
  {
    "line": 875,
    "terms": [
      "ndx_prices"
    ],
    "text": "    ndx_lookup = _build_lookup(ndx_dates or [], ndx_prices or [])"
  },
  {
    "line": 876,
    "terms": [
      "sox_prices"
    ],
    "text": "    sox_lookup = _build_lookup(sox_dates or [], sox_prices or [])"
  },
  {
    "line": 877,
    "terms": [
      "vix_prices"
    ],
    "text": "    vix_lookup = _build_lookup(vix_dates or [], vix_prices or [])"
  },
  {
    "line": 947,
    "terms": [
      "spx_prices"
    ],
    "text": "    n_days       = len(spx_prices)"
  },
  {
    "line": 951,
    "terms": [
      "sim_start_date"
    ],
    "text": "    _trade_start = sim_start_date  # None = 从 min_history 后第一天"
  },
  {
    "line": 952,
    "terms": [
      "sim_end_date"
    ],
    "text": "    _trade_end   = sim_end_date    # None = 到末尾"
  },
  {
    "line": 962,
    "terms": [
      "dates_map"
    ],
    "text": "        sym_dates = dates_map.get(sym, [])"
  },
  {
    "line": 971,
    "terms": [
      "ohlc_map"
    ],
    "text": "    if ohlc_map:"
  },
  {
    "line": 972,
    "terms": [
      "ohlc_map"
    ],
    "text": "        highs = {s: ohlc_map[s].get(\"high\", []) for s in ohlc_map}"
  },
  {
    "line": 973,
    "terms": [
      "ohlc_map"
    ],
    "text": "        lows  = {s: ohlc_map[s].get(\"low\",  []) for s in ohlc_map}"
  },
  {
    "line": 996,
    "terms": [
      "prices_map"
    ],
    "text": "            data    = prices_map.get(sym, [])"
  },
  {
    "line": 1005,
    "terms": [
      "prices_map"
    ],
    "text": "        data     = prices_map.get(sym, [])"
  },
  {
    "line": 1081,
    "terms": [
      "daily_records"
    ],
    "text": "    daily_records: list[dict]  = []"
  },
  {
    "line": 1178,
    "terms": [
      "spx_prices"
    ],
    "text": "                        \"entry_spx\":             spx_prices[master_dates.index(exec_date)] if exec_date in master_dates else spx_close_t,"
  },
  {
    "line": 1361,
    "terms": [
      "total_equity"
    ],
    "text": "        total_equity = cash + position_value"
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
    "line": 1373,
    "terms": [
      "spx_prices"
    ],
    "text": "            spx_entry = spx_prices[t] if spx_prices[t] > 0 else 1.0"
  },
  {
    "line": 1374,
    "terms": [
      "spx_prices"
    ],
    "text": "        spx_curve.append(spx_prices[t] / spx_entry if spx_entry > 0 else 1.0)"
  },
  {
    "line": 1385,
    "terms": [
      "spx_prices"
    ],
    "text": "        spx_close_t = spx_prices[t]"
  },
  {
    "line": 1386,
    "terms": [
      "spx_prices"
    ],
    "text": "        spx_ma50_t = sum(spx_prices[t-49:t+1]) / 50 if t >= 49 else spx_close_t"
  },
  {
    "line": 1388,
    "terms": [
      "spx_prices"
    ],
    "text": "            (spx_prices[t] - spx_prices[t-1]) / spx_prices[t-1]"
  },
  {
    "line": 1389,
    "terms": [
      "spx_prices"
    ],
    "text": "            if t > 0 and spx_prices[t-1] > 0 else 0.0"
  },
  {
    "line": 1404,
    "terms": [
      "spx_prices"
    ],
    "text": "                spx_ma50_t10 = sum(spx_prices[t-59:t-9]) / 50"
  },
  {
    "line": 1418,
    "terms": [
      "ndx_prices"
    ],
    "text": "                if ndx_prices and len(ndx_prices) >= 50:"
  },
  {
    "line": 1421,
    "terms": [
      "ndx_prices"
    ],
    "text": "                        _ndx_ma50 = sum(ndx_prices[_ndx_idx-49:_ndx_idx+1]) / 50"
  },
  {
    "line": 1425,
    "terms": [
      "sox_prices"
    ],
    "text": "                if sox_prices and len(sox_prices) >= 50:"
  },
  {
    "line": 1428,
    "terms": [
      "sox_prices"
    ],
    "text": "                        _sox_ma50 = sum(sox_prices[_sox_idx-49:_sox_idx+1]) / 50"
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
    "line": 2128,
    "terms": [
      "sim_end_date"
    ],
    "text": "        # 因为 T+1 执行时会等于或超过 sim_end_date，导致 entry==exit invalid"
  },
  {
    "line": 2130,
    "terms": [
      "sim_end_date"
    ],
    "text": "        # 最后一个或倒数第二个 sim 日不生成新 BUY（T+1 执行时会撞上 sim_end_date）"
  },
  {
    "line": 2148,
    "terms": [
      "daily_records"
    ],
    "text": "            daily_records.append({"
  },
  {
    "line": 2152,
    "terms": [
      "total_equity"
    ],
    "text": "                \"total_equity\":   round(total_equity, 2),"
  },
  {
    "line": 2167,
    "terms": [
      "sim_end_date"
    ],
    "text": "    # 强制平仓日期：用 sim_end_date（若有），否则用数据末日"
  },
  {
    "line": 2168,
    "terms": [
      "sim_end_date"
    ],
    "text": "    if sim_end_date and sim_end_date in master_dates:"
  },
  {
    "line": 2169,
    "terms": [
      "sim_end_date"
    ],
    "text": "        last_date = sim_end_date"
  },
  {
    "line": 2170,
    "terms": [
      "sim_end_date"
    ],
    "text": "    elif sim_end_date:"
  },
  {
    "line": 2171,
    "terms": [
      "sim_end_date"
    ],
    "text": "        # sim_end_date 不在 master_dates，找最近的前一个交易日"
  },
  {
    "line": 2172,
    "terms": [
      "sim_end_date"
    ],
    "text": "        last_date = max((d for d in master_dates if d <= sim_end_date), default=master_dates[-2])"
  },
  {
    "line": 2240,
    "terms": [
      "total_equity"
    ],
    "text": "        \"total_equity\": round(final_equity, 2),"
  },
  {
    "line": 2420,
    "terms": [
      "sim_start_date"
    ],
    "text": "            \"simulation_start_date\": sim_start_date,"
  },
  {
    "line": 2421,
    "terms": [
      "sim_end_date"
    ],
    "text": "            \"simulation_end_date\":   sim_end_date,"
  },
  {
    "line": 2476,
    "terms": [
      "daily_records"
    ],
    "text": "        \"daily_records\":     daily_records,"
  },
  {
    "line": 2489,
    "terms": [
      "run_strategy_variant_comparison("
    ],
    "text": "def run_strategy_variant_comparison("
  },
  {
    "line": 2491,
    "terms": [
      "prices_map"
    ],
    "text": "    prices_map: dict[str, list[float]],"
  },
  {
    "line": 2492,
    "terms": [
      "dates_map"
    ],
    "text": "    dates_map: dict[str, list[str]],"
  },
  {
    "line": 2493,
    "terms": [
      "spx_prices"
    ],
    "text": "    spx_prices: list[float],"
  },
  {
    "line": 2495,
    "terms": [
      "ndx_prices"
    ],
    "text": "    ndx_prices: list[float] = None,"
  },
  {
    "line": 2497,
    "terms": [
      "sox_prices"
    ],
    "text": "    sox_prices: list[float] = None,"
  },
  {
    "line": 2499,
    "terms": [
      "vix_prices"
    ],
    "text": "    vix_prices: list[float] = None,"
  },
  {
    "line": 2552,
    "terms": [
      "data/research/e1_5y"
    ],
    "text": "        regime_path = Path(\"data/research/e1_5y/regimes/spx_regime_daily.json\")"
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
      "sim_start_date",
      "sim_end_date"
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
    "line": 2613,
    "terms": [
      "sim_end_date",
      "2026-06-18"
    ],
    "text": "                \"sim_end_date\":   \"2026-06-18\","
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
    "line": 2621,
    "terms": [
      "sim_end_date"
    ],
    "text": "                \"sim_end_date\":   \"2024-12-31\","
  },
  {
    "line": 2625,
    "terms": [
      "sim_start_date"
    ],
    "text": "                \"sim_start_date\": \"2024-12-03\","
  },
  {
    "line": 2626,
    "terms": [
      "sim_end_date"
    ],
    "text": "                \"sim_end_date\":   \"2026-06-11\","
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
    "line": 2631,
    "terms": [
      "sim_end_date"
    ],
    "text": "                \"sim_end_date\":   \"2026-06-11\","
  },
  {
    "line": 2643,
    "terms": [
      "ndx_prices"
    ],
    "text": "            _use_ndx = ndx_prices or []"
  },
  {
    "line": 2644,
    "terms": [
      "sox_prices"
    ],
    "text": "            _use_sox = sox_prices or []"
  },
  {
    "line": 2646,
    "terms": [
      "run_stateful_simulation("
    ],
    "text": "            _result = run_stateful_simulation("
  },
  {
    "line": 2648,
    "terms": [
      "prices_map"
    ],
    "text": "                prices_map=prices_map,"
  },
  {
    "line": 2649,
    "terms": [
      "dates_map"
    ],
    "text": "                dates_map=dates_map,"
  },
  {
    "line": 2650,
    "terms": [
      "spx_prices"
    ],
    "text": "                spx_prices=spx_prices,"
  },
  {
    "line": 2653,
    "terms": [
      "sim_start_date"
    ],
    "text": "                sim_start_date=period_cfg[\"sim_start_date\"],"
  },
  {
    "line": 2654,
    "terms": [
      "sim_end_date"
    ],
    "text": "                sim_end_date=period_cfg[\"sim_end_date\"],"
  },
  {
    "line": 2655,
    "terms": [
      "ndx_prices"
    ],
    "text": "                ndx_prices=_use_ndx,"
  },
  {
    "line": 2657,
    "terms": [
      "sox_prices"
    ],
    "text": "                sox_prices=_use_sox,"
  },
  {
    "line": 2659,
    "terms": [
      "vix_prices"
    ],
    "text": "                vix_prices=_use_vix,"
  },
  {
    "line": 2695,
    "terms": [
      "run_stateful_simulation("
    ],
    "text": "    # - Do not modify run_stateful_simulation()."
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
    "line": 2887,
    "terms": [
      "sim_start_date"
    ],
    "text": "                        \"sim_start_date\":   r.get(\"sample_validity\", {}).get(\"simulation_start_date\"),"
  },
  {
    "line": 2888,
    "terms": [
      "sim_end_date"
    ],
    "text": "                        \"sim_end_date\":     r.get(\"sample_validity\", {}).get(\"simulation_end_date\"),"
  },
  {
    "line": 2906,
    "terms": [
      "prices_map"
    ],
    "text": "    prices_map:   dict[str, list[float]],"
  },
  {
    "line": 2907,
    "terms": [
      "spx_prices"
    ],
    "text": "    spx_prices:   list[float],"
  },
  {
    "line": 2908,
    "terms": [
      "dates_map"
    ],
    "text": "    dates_map:    dict[str, list[str]] = None,"
  },
  {
    "line": 2912,
    "terms": [
      "ndx_prices"
    ],
    "text": "    ndx_prices:   list[float] = None,"
  },
  {
    "line": 2914,
    "terms": [
      "sox_prices"
    ],
    "text": "    sox_prices:   list[float] = None,"
  },
  {
    "line": 2916,
    "terms": [
      "vix_prices"
    ],
    "text": "    vix_prices:   list[float] = None,"
  },
  {
    "line": 2924,
    "terms": [
      "dates_map"
    ],
    "text": "    dates_map  = dates_map  or {}"
  },
  {
    "line": 2930,
    "terms": [
      "prices_map",
      "spx_prices"
    ],
    "text": "        symbols, prices_map, spx_prices"
  },
  {
    "line": 2935,
    "terms": [
      "prices_map",
      "spx_prices"
    ],
    "text": "        symbols, prices_map, spx_prices"
  },
  {
    "line": 2941,
    "terms": [
      "prices_map"
    ],
    "text": "        prices_map=prices_map,"
  },
  {
    "line": 2942,
    "terms": [
      "spx_prices"
    ],
    "text": "        spx_prices=spx_prices,"
  },
  {
    "line": 2943,
    "terms": [
      "dates_map"
    ],
    "text": "        dates_map=dates_map,"
  },
  {
    "line": 2949,
    "terms": [
      "run_strategy_variant_comparison("
    ],
    "text": "        results[\"layer_d\"] = run_strategy_variant_comparison("
  },
  {
    "line": 2950,
    "terms": [
      "prices_map",
      "dates_map",
      "spx_prices"
    ],
    "text": "            symbols, prices_map, dates_map, spx_prices, spx_dates,"
  },
  {
    "line": 2951,
    "terms": [
      "ndx_prices"
    ],
    "text": "            ndx_prices=ndx_prices or [], ndx_dates=ndx_dates or [],"
  },
  {
    "line": 2952,
    "terms": [
      "sox_prices"
    ],
    "text": "            sox_prices=sox_prices or [], sox_dates=sox_dates or [],"
  },
  {
    "line": 2953,
    "terms": [
      "vix_prices"
    ],
    "text": "            vix_prices=vix_prices or [], vix_dates=vix_dates or [],"
  },
  {
    "line": 2959,
    "terms": [
      "prices_map",
     
```

## Target Function Source Heads

### `run_stateful_simulation` line `763`

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
                    f"price>MA50={qualified_price_above_ma50} slope>={qualified_ma50_slope_min}")
    else:
        logger.info(f"  Entry mode: Strict Top{entry_top_n} (legacy)")
    if ls60_exit_mode not in {"exit", "reduce"}:
        raise ValueError(f"Invalid ls60_exit_mode={ls60_exit_mode!r}; expected 'exit' or 'reduce'")
    market_shock_gate_enabled = bool(a.get("market_shock_gate_enabled", True))
    market_shock_daily_return = float(a.get("market_shock_daily_return", -0.02))
    take_profit_enabled = bool(a.get("partial_take_profit_enabled", False))
    take_profit_threshold = float(a.get("partial_take_profit_threshold", 0.07))
    take_profit_fraction = float(a.get("partial_take_profit_fraction", 0.50))
    block_add_after_take_profit = bool(a.get("block_add_after_take_profit", False))
    entry_rs_min = float(a.get("entry_rs_min", 90.0))
    min_holding_days = int(a.get("min_holding_days", 0))
    # E2 Dynamic Exit parameters
    dynamic_exit_enabled   = bool(a.get("dynamic_exit_enabled", False))
    min_hold_allow_broken_exit = bool(a.get("min_hold_allow_broken_exit", True))
    relative_stop_enabled = bool(a.get("relative_stop_enabled", False))
    relative_stop_underperform = float(a.get("relative_stop_underperform_pct", -0.08))
    relative_stop_action = a.get("relative_stop_action", "REL_REDUCE")
    relative_stop_once = bool(a.get("relative_stop_once_per_position", True))
    market_gate_variant = (
        "D1_NO_MARKET_GATE" if not market_gate_enabled else
        "D2_RISK_OFF_GATE" if not market_shock_gate_enabled else
        "D3_RISK_OFF_PLUS_SHOCK_GATE"
    )

    if qualified_entry_enabled:
        logger.info(f"  v{a.get('version','?')} | Strategy={strategy_variant} "
                    f"| CandidateTopN={candidate_top_n} MaxPos={max_pos} EntryMode=QualifiedPool "
                    f"BuySlot={buy_pct*100:.1f}% MaxSingle={max_pct*100:.1f}% "
                    f"OneWay={one_way*100:.2f}%")
    else:
        logger.info(f"  v{a.get('version','?')} | Strategy={strategy_variant} "
                    f"| EntryTopN={entry_top_n} MaxPos={max_pos} EntryMode=StrictTop3 "
                    f"BuySlot={buy_pct*100:.1f}% MaxSingle={max_pct*100:.1f}% "
                    f"OneWay={one_way*100:.2f}%")
    logger.info(f"  Market Gate Variant: {market_gate_variant}")
    logger.info(f"  Market Gate: enabled={market_gate_enabled} "
                f"| RiskOff=SPX<MA50:{risk_off_below_spx_ma50} "
                f"| Shock<={market_shock_daily_return*100:.1f}%:{market_shock_gate_enabled}")
    logger.info(f"  Entry filter: RS >= {entry_rs_min:.1f}; MinHold={min_holding_days}d; "
                f"RelStop={'ON' if relative_stop_enabled else 'OFF'} "
                f"({relative_stop_underperform*100:.1f}% vs SPX)")
    logger.info(f"  LS60 mode: {ls60_exit_mode} "
                f"({'LS<60 → EXIT' if ls60_exit_mode == 'exit' else 'LS<60 → REDUCE'})")
    logger.info(f"  ── Param check: ls60={ls60_exit_mode} rs={entry_rs_min} "
                f"top_n={entry_top_n} minhold={min_holding_days} "
                f"relstop={relative_stop_enabled} gate={market_gate_enabled} ──")
    if dynamic_exit_enabled:
        logger.info(f"  Dynamic Exit v2: ON | Hard=Close<MA50+slope<0 | FULL_ON=needs structure | CAUTIOUS/CASH=LS<60 exits")
    logger.info(f"  Fixed TP: enabled={take_profit_enabled} "
                f"(v1.6 default OFF; TP7-P rejected for this matrix)")

    # ── 修正1: SPX master calendar ────────────────────────
    # 时间轴以 SPX dates 为准，不受个股短数据影响
    master_dates = spx_dates
    n_days       = len(spx_prices)

    logger.info(f"  时间轴: {master_dates[0] if master_dates else '?'} → {master_dates[-1] if master_dates else '?'} ({n_days} bars)")
    # 交易执行区间（不影响 warm-up 和指标计算，只控制交易时段）
    _trade_start = sim_start_date  # None = 从 min_history 后第一天
    _trade_end   = sim_end_date    # None = 到末尾
    _default_start = master_dates[min_history] if len(master_dates) > min_history else (master_dates[0] if master_dates else "?")
    _default_end   = master_dates[-2] if len(master_dates) >= 2 else (master_dates[-1] if master_dates else "?")
    logger.info(f"  时间轴: {master_dates[0] if master_dates else '?'} → {master_dates[-1] if master_dates else '?'} ({n_days} bars)")
    logger.info(f"  回测区间: {_trade_start or _default_start} → {_trade_end or _default_end}")

    # ── 修正2: Date-based lookup 索引 ─────────────────────
    # 为每只股票建立 date→index 映射，按日期对齐而非 array index
    date_idx: dict[str, dict[str, int]] = {}  # {sym: {date: idx}}
    for sym in symbols:
        sym_dates = dates_map.get(sym, [])
        date_idx[sym] = {d: i for i, d in enumerate(sym_dates)}

    # high/low 加载
    highs: dict[str, list[float]] = {}
    lows:  dict[str, list[float]] = {}
    highs_dates: dict[str, dict[str, int]] = {}
    lows_dates:  dict[str, dict[str, int]] = {}

    if ohlc_map:
        highs = {s: ohlc_map[s].get("high", []) for s in ohlc_map}
        lows  = {s: ohlc_map[s].get("low",  []) for s in ohlc_map}
    else:
        from ..data_ingestion.fetch_yahoo import get_price_series as _gps
        for sym in symbols:
            hd, h = _gps(sym, field="high")
            ld, l = _gps(sym, field="low")
            if h:
                highs[sym]       = h
                highs_dates[sym] = {d: i for i, d in enumerate(hd)}
            if l:
                lows[sym]        = l
                lows_dates[sym]  = {d: i for i, d in enumerate(ld)}

    def get_price_by_date(sym: str, date: str, field: str = "close") -> float:
        """按日期安全获取价格，不存在返回0。"""
        if field == "high":
            idx_map = highs_dates.get(sym, {})
            data    = highs.get(sym, [])
        elif field == "low":
            idx_map = lows_dates.get(sym, {})
            data    = lows.get(sym, [])
        else:
            idx_map = date_idx.get(sym, {})
            data    = prices_map.get(sym, [])
        i = idx_map.get(date, -1)
        if i < 0 or i >= len(data):
            return 0.0
        return data[i]

    def get_close_series_by_date(sym: str, up_to
```

### `run_strategy_variant_comparison` line `2489`

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
        logger.info(f"  ══ {period_cfg['label']} ══")
        period_results[period_key] = {"label": period_cfg["label"], "variants": {}}
        for variant_id, assumptions in variants.items():
            logger.info(f"    === {period_key}/{variant_id} ===")
            # E1/E2：Gate G4 固定使用 NDX/SOX（leadership），不传 VIX
            _use_ndx = ndx_prices or []
            _use_sox = sox_prices or []
            _use_vix = []  # Gate v2.1 不使用 VIX
            _result = run_stateful_simulation(
                symbols=symbols,
                prices_map=prices_map,
                dates_map=dates_map,
                spx_prices=spx_prices,
                spx_dates=spx_dates,
                assumptions=assumptions,
                sim_start_date=period_cfg["sim_start_date"],
                sim_end_date=period_cfg["sim_end_date"],
                ndx_prices=_use_ndx,
                ndx_dates=ndx_dates or [],
                sox_prices=_use_sox,
                sox_dates=sox_dates or [],
                vix_prices=_use_vix,
                vix_dates=vix_dates or [],
            )
            if assumptions.get("e1r_shell_mode"):
                _result["strategy_id"] = variant_id
                _result["research_status"] = "REGIME_WIRING_ONLY_NOT_IMPLEMENTED"
                _result["e1r_shell_mode"] = True
                _result["e1r_regime_wiring_enabled"] = True
                _result["e1r_spec_ref"] = assumptions.get("e1r_spec_ref")
                _result["e1r_regime_source"] = assumptions.get("e1r_regime_source")
                _result.setdefault("strategy_controls", {})["e1r_shell_mode"] = True
                _result["strategy_controls"]["e1r_regime_wiring_enabled"] = True
                _result["strategy_controls"]["e1r_spec_ref"] = assumptions.get("e1r_spec_ref")
                _result["strategy_controls"]["e1r_regime_source"] = assumptions.get("e1r_regime_source")
                if assumptions.get("e1r_uptrend_execution_enabled"):
                    _result["strategy_controls"]["regime_aware_logic"] = "UPTREND_EXECUTION_V0_1_ENTRY_ONLY"
                    _result["research_status"] = "UPTREND_EXECUTION_V0_1"
                    _result["e1r_candidate_tagging_enabled"] = True
                    _result["e1r_uptrend_execution_enabled"] = True
                    _result["strategy_controls"]["e1r_candidate_tagging_enabled"] = True
                    _result["strategy_controls"]["e1r_uptrend_execution_enabled"] = True
                    _result["strategy_controls"]["exit_reduce_logic"] = "LEGACY_E1_UNCHANGED"
                else:
                    _result["strategy_controls"]["regime_aware_logic"] = "NOT_IMPLEMENTED_PHASE_3A_CANDIDATE_TAGGING_ONLY"
                    _result["research_status"] = "UPTREND_CANDIDATE_TAGGING_ONLY_NOT_EXECUTED"
                    _result["e1r_candidate_tagging_enabled"] = True
                    _result["strategy_controls"]["e1r_candidate_tagging_enabled"] = True
            period_results[period_key]["variants"][variant_id] = _result

    # ── 为兼容现有输出格式，把 Period C（全区间）当作主结果 ────
    _full_period_key = "C_FULL_5Y_2021_06_TO_2026_06" if "C_FULL_5Y_2021_06_TO_2026_06" in period_results else "C_FULL_2023_11_TO_2026_06"
    variant_results = period_results[_full_period_key]["variants"]

    # ── E1-R v0.2 formal sidecar sleeve composition ────────────────
    #
    # Design principle:
    # - Do not modify run_stateful_simulation().
    # - Do not modify E1R_REGIME_AWARE_V0_1.
    # - Compose the validated SIDEWAYS:MA_CONFLICT Top10 25% sleeve
    #   with the existing E1R v0.1 core daily returns.
    #
    # This keeps the formal engine semantics aligned with the validated
    # research S4 sidecar instead of approximating it inside the Top3
    # stateful order loop.
    try:
        from src.engine.e1r_sidecar_sleeve import (
            E1RSidecarConfig,
            build_e1r_sidecar_sleeve,
        )
        from src.engine.e1r_composer import compose_e1r_v0_2_variant

        _core_e1r = variant_results.get("E1R_REGIME_AWARE_V0_1")
        _core_records = (_core_e1r or {}).get("daily_equity_records", []) if _core_e1r else []

        _stock_dir = Path("data/research/e1_5y/raw/stocks")
        _spx_path = Path("data/research/e1_5y/raw/indices/SPX.json")
        _regime_path = Path("data/research/e1_5y/regimes/spx_regime_daily.json")

        if _core_e1r and _core_records and _stock_dir.exists() and _spx_path.exists() and _regime_path.exists():
            _sidecar_cfg = E1RSidecarConfig(
                start_date=_core_records[0]["date"],
                end_date=_core_records[-1]["date"],
                allowed_subclasses=("MA_CONFLICT",),
                top_n=10,
                gross_exposure=0.25,
                min_history_days=200,
                min_price=5.0,
                initial_equity=float(base.get("initial_capital", 100000)),
                excluded_symbols=("VIXY",),
            )

            _sidecar_result = build_e1r_sidecar_sleeve(
                stock_dir=_stock_dir,
                spx_path=_spx_path,
                regime_path=_regime_path,
                config=_sidecar_cfg,
            )

            variant_results["E1R_REGIME_AWARE_V0_2"] = compose_e1r_v0_2_variant(
                core_variant_result=_core_e1r,
                sidecar_result=_sidecar_result,
                initial_equity=float(base.get("initial_capital", 100000)),
            )

            _sidecar_summary = _sidecar_result.get("summary", {}) or {}
            logger.info(
                "  E1-R v0.2 formal sidecar sleeve composed: "
                f"active_days={_sidecar_summary.get('active_days')} "
                f"return={_sidecar_summary.get('full_period_strategy_return_pct'):.2f}%"
            )
        else:
            logger.warn(
                "  E1-R v0.2 formal sidecar sleeve skipped: missing core records or research 5Y inputs"
            )

    except Exception as exc:
        logger.warn(f"  E1-R v0.2 formal sidecar sleeve failed: {exc}")

 
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-3C`: Build minimal export-only E1 5Y core generator
- Recommended action: Create a new script under scripts/ that imports src.engine.backtest, loads 5Y data, calls run_stateful_simulation with sim_start_date=2021-06-11 and sim_end_date=2026-06-18, then writes exports/e1_5y_backtest_equity_curve.json only if one-row-per-date continuous-capital validation passes.

