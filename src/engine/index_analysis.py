"""
index_analysis.py — 四大指数分析 Phase 2
策略：用稳定的 ETF 替代不稳定的 ^ 指数代码
  SPY  → 代表 SPX（价格显示时 ×10 近似还原）
  QQQ  → 代表 NDX
  ^VIX → VIX（保留，fallback 到 UVXY）
  SOXX → 代表 SOX
"""
from __future__ import annotations
from ..features.momentum import linreg_slope, moving_average

# Yahoo Finance 稳定代码映射
# key=显示代码, value=实际下载代码
INDEX_DOWNLOAD_MAP = {
    "SPX": ["^GSPC", "SPY"],   # 先试^GSPC，失败用SPY
    "NDX": ["^NDX",  "QQQ"],   # 先试^NDX，失败用QQQ
    "VIX": ["^VIX",  "VIXY", "UVXY"],  # 先试^VIX，失败用VIXY或UVXY
    "SOX": ["^SOX",  "SOXX"],  # 先试^SOX，失败用SOXX
}

# ETF 价格倍数（ETF价格 × 倍数 ≈ 指数真实值，仅用于显示）
ETF_MULTIPLIER = {
    "SPY": 10.0,   # SPY ~750 × 10 ≈ SPX ~7500
    "QQQ": 50.0,   # QQQ ~440 × 50 ≈ NDX ~22000（近似）
    "VIXY": 1.0,
    "UVXY": 1.0,
    "SOXX": 20.0,  # SOXX ~230 × 20 ≈ SOX ~4600（近似）
}

INDEX_META = {
    "SPX": {"name": "标普500",     "desc": "大盘趋势基准"},
    "NDX": {"name": "纳斯达克100", "desc": "科技/成长股风向标"},
    "VIX": {"name": "波动率指数",  "desc": "市场恐惧/情绪指标"},
    "SOX": {"name": "费城半导体",  "desc": "半导体/科技先行指标"},
}


def _find_prices(code: str, prices_map: dict) -> tuple[list[float], list[str], str]:
    """
    按优先级查找指数价格：先试原始代码，再试ETF替代。
    返回 (prices, dates, actual_key_used)
    """
    from ..data_ingestion.fetch_yahoo import get_price_series

    candidates = INDEX_DOWNLOAD_MAP.get(code, [code])
    for sym in candidates:
        # 尝试多种key格式
        for key in [sym, sym.replace("^", "_"), sym.lstrip("^")]:
            p = prices_map.get(key, [])
            if len(p) >= 5:
                from ..utils.helpers import price_file
                from ..utils.config import PRICES_DIR
                # 也从文件读取
                d, pp = get_price_series(key)
                if len(pp) >= 5:
                    return pp, d, key
                if len(p) >= 5:
                    return p, [], key
    return [], [], ""


def analyze_index(code: str, prices: list[float], dates: list[str],
                  actual_key: str = "") -> dict:
    n = len(prices)
    if n < 5:
        return {"code": code, "available": False,
                "name": INDEX_META.get(code, {}).get("name", code)}

    # 如果用的是ETF，价格还原到指数量级（仅用于显示）
    mult = ETF_MULTIPLIER.get(actual_key, 1.0)
    display_prices = [p * mult for p in prices]

    last = display_prices[-1] if mult != 1.0 else prices[-1]
    raw_last = prices[-1]
    raw_prev = prices[-2] if n >= 2 else raw_last
    chg_pct  = (raw_last - raw_prev) / raw_prev * 100 if raw_prev > 0 else 0

    # 技术指标用原始价格计算（避免倍数干扰斜率）
    ma20  = sum(prices[-20:]) / min(n, 20)
    ma50  = sum(prices[-50:]) / min(n, 50)  if n >= 20 else prices[-1]
    ma200 = sum(prices[-200:]) / min(n, 200) if n >= 100 else prices[-1]
    sl20  = linreg_slope(prices[-20:]) if n >= 20 else 0
    w52   = prices[-252:] if n >= 252 else prices
    high52, low52 = max(w52), min(w52)

    # 显示值（ETF还原后）
    disp_ma20  = ma20  * mult
    disp_ma50  = ma50  * mult
    disp_ma200 = ma200 * mult

    chart_ma20 = [round(v * mult, 2) for v in moving_average(prices, 20)[-60:]]
    chart_ma50 = [round(v * mult, 2) for v in moving_average(prices, 50)[-60:]] if n >= 50 else []
    chart_prices = [round(p * mult, 2) for p in prices[-60:]]

    r = {
        "code":          code,
        "actual_key":    actual_key,
        "name":          INDEX_META[code]["name"],
        "desc":          INDEX_META[code]["desc"],
        "available":     True,
        "price":         round(last, 2),
        "change_pct":    round(chg_pct, 2),
        "change":        round((raw_last - raw_prev) * mult, 2),
        "ma20":          round(disp_ma20, 2),
        "ma50":          round(disp_ma50, 2),
        "ma200":         round(disp_ma200, 2),
        "above_ma20":    raw_last > ma20,
        "above_ma50":    raw_last > ma50,
        "above_ma200":   raw_last > ma200,
        "slope20":       round(sl20, 6),
        "high52w":       round(high52 * mult, 2),
        "low52w":        round(low52 * mult, 2),
        "pct_from_high": round((high52 - raw_last) / high52 * 100, 2) if high52 > 0 else 0,
        "chart_dates":   dates[-60:],
        "chart_prices":  chart_prices,
        "chart_ma20":    chart_ma20,
        "chart_ma50":    chart_ma50,
    }

    if code == "VIX":
        v = prices[-1]  # VIX 用原始值
        if v < 15:   st, col = "低恐惧",   "#1D9E75"
        elif v < 20: st, col = "正常",     "#378ADD"
        elif v < 25: st, col = "偏高",     "#BA7517"
        elif v < 35: st, col = "高恐惧",   "#D85A30"
        else:        st, col = "极度恐惧", "#993C1D"
        trend = "上升" if sl20 > 0.001 else "下降" if sl20 < -0.001 else "横盘"
        r.update({"vix_state": st, "vix_color": col, "vix_trend": trend,
                  "price": round(v, 2)})  # VIX显示原始值
    else:
        if raw_last > ma50 > ma200 and sl20 > 0:   tr, col = "强势上涨", "#1D9E75"
        elif raw_last > ma50 and sl20 > 0:          tr, col = "趋势向上", "#378ADD"
        elif raw_last > ma50:                        tr, col = "震荡偏多", "#BA7517"
        elif raw_last > ma200:                       tr, col = "弱势整理", "#D85A30"
        else:                                        tr, col = "趋势向下", "#993C1D"
        r.update({"trend": tr, "trend_color": col})

    return r


def analyze_all_indices(prices_map: dict, dates_map: dict) -> dict:
    results = {}
    for code in ["SPX", "NDX", "VIX", "SOX"]:
        prices, dates, actual_key = _find_prices(code, prices_map)
        if len(prices) >= 5:
            results[code] = analyze_index(code, prices, dates, actual_key)
        else:
            results[code] = {"code": code, "name": INDEX_META[code]["name"],
                             "available": False}

    # 相对强弱（用原始价格，不乘倍数）
    spx_prices, _, _ = _find_prices("SPX", prices_map)
    ndx_prices, _, _ = _find_prices("NDX", prices_map)
    sox_prices, _, _ = _find_prices("SOX", prices_map)

    if len(ndx_prices) >= 20 and len(spx_prices) >= 20:
        nr = (ndx_prices[-1] - ndx_prices[-20]) / ndx_prices[-20] * 100
        sr = (spx_prices[-1] - spx_prices[-20]) / spx_prices[-20] * 100
        tp = round(nr - sr, 2)
        results["tech_premium"] = tp
        results["tech_premium_signal"] = "科技领涨" if tp > 2 else "科技同步" if tp > -2 else "科技落后"

    if len(sox_prices) >= 20 and len(spx_prices) >= 20:
        xr  = (sox_prices[-1] - sox_prices[-20]) / sox_prices[-20] * 100
        sr2 = (spx_prices[-1] - spx_prices[-20]) / spx_prices[-20] * 100
        sp  = round(xr - sr2, 2)
        results["sox_premium"] = sp
        results["sox_premium_signal"] = "半导体领涨" if sp > 3 else "半导体同步" if sp > -3 else "半导体落后"

    return results
