"""
market_score.py — Market Score  [Phase 2 Spec Section 11, 12]

Market Score = SPX(35%) + NDX(25%) + SOX(25%) + VIX(15%)
输出：0~100

Leadership Confirmed：
  SPX Score > 70 AND NDX Score > 70 AND SOX Score > 70

Market Regime：
  >= 80 → Risk-On
  60~79 → Neutral
  < 60  → Risk-Off
"""
from __future__ import annotations
from ..features.momentum import moving_average, linreg_slope


def _index_score(prices: list[float]) -> float:
    """
    计算单个价格指数的趋势得分（0-100）。
    综合：价格位置(60分) + MA斜率(25分) + 近期动量(15分)
    """
    if len(prices) < 20:
        return 30.0  # 数据不足给保守分

    n    = len(prices)
    last = prices[-1]
    ma20 = sum(prices[-20:]) / 20
    ma50 = sum(prices[-50:]) / 50  if n >= 50  else ma20
    ma200= sum(prices[-200:]) / 200 if n >= 200 else ma50

    score = 0.0

    # 价格结构（60分）
    if last > ma20:  score += 20
    if last > ma50:  score += 20
    if last > ma200: score += 20

    # MA20 斜率（25分）
    sl20 = linreg_slope(prices[-20:])
    if sl20 > 0.002:    score += 25
    elif sl20 > 0:      score += 15
    elif sl20 > -0.002: score += 5

    # 近5日动量（15分）
    if n >= 6:
        m5 = (prices[-1] - prices[-6]) / prices[-6] if prices[-6] > 0 else 0
        if m5 > 0.02:    score += 15
        elif m5 > 0:     score += 8
        elif m5 > -0.02: score += 3

    return min(score, 100.0)


def _vix_score(vix_prices: list[float]) -> tuple[float, str, str]:
    """
    VIX 得分（0-100），VIX 越低得分越高。
    返回 (score, state, color)
    """
    if not vix_prices:
        return 50.0, "未知", "#888"

    vix = vix_prices[-1]
    sl  = linreg_slope(vix_prices[-10:]) if len(vix_prices) >= 10 else 0
    trend_bonus = 10 if sl < -0.005 else 0 if sl < 0.005 else -10

    if vix < 15:    raw, st, col = 100, "低恐惧",   "#1D9E75"
    elif vix < 20:  raw, st, col = 80,  "正常",     "#378ADD"
    elif vix < 25:  raw, st, col = 55,  "偏高",     "#BA7517"
    elif vix < 35:  raw, st, col = 30,  "高恐惧",   "#D85A30"
    else:           raw, st, col = 10,  "极度恐惧", "#993C1D"

    return max(0.0, min(100.0, raw + trend_bonus)), st, col


def compute_market_score(
    spx_prices: list[float],
    ndx_prices: list[float],
    sox_prices: list[float],
    vix_prices: list[float],
) -> dict:
    """
    Market Score = SPX(35%) + NDX(25%) + SOX(25%) + VIX(15%)
    Leadership Confirmed: 三个指数 Score 均 > 70
    """
    spx_sc = _index_score(spx_prices)
    ndx_sc = _index_score(ndx_prices)
    sox_sc = _index_score(sox_prices)
    vix_sc, vix_st, vix_col = _vix_score(vix_prices)

    total = round(0.35*spx_sc + 0.25*ndx_sc + 0.25*sox_sc + 0.15*vix_sc, 1)

    # Market Regime
    if total >= 80:   state, zh, icon, col = "Risk-On",  "风险偏好", "🟢", "#1D9E75"
    elif total >= 60: state, zh, icon, col = "Neutral",  "中性观望", "🟡", "#BA7517"
    else:             state, zh, icon, col = "Risk-Off", "风险规避", "🔴", "#D85A30"

    # Leadership Confirmed: SPX>70 AND NDX>70 AND SOX>70
    leadership = spx_sc > 70 and ndx_sc > 70 and sox_sc > 70

    breakdown = {
        "SPX": {"score": round(spx_sc, 1), "weight": "35%",
                "above_ma50": len(spx_prices)>=50 and spx_prices[-1]>sum(spx_prices[-50:])/50},
        "NDX": {"score": round(ndx_sc, 1), "weight": "25%",
                "above_ma50": len(ndx_prices)>=50 and ndx_prices[-1]>sum(ndx_prices[-50:])/50},
        "SOX": {"score": round(sox_sc, 1), "weight": "25%",
                "above_ma50": len(sox_prices)>=50 and sox_prices[-1]>sum(sox_prices[-50:])/50},
        "VIX": {"score": round(vix_sc, 1), "weight": "15%",
                "vix_state": vix_st, "vix_color": vix_col},
    }

    return {
        "market_score":          total,
        "state":                 state,
        "state_zh":              zh,
        "state_icon":            icon,
        "state_color":           col,
        "leadership_confirmed":  leadership,
        "leadership_label":      "Leadership Confirmed ✅" if leadership else "Leadership Unconfirmed ⚠️",
        "vix_state":             vix_st,
        "vix_color":             vix_col,
        "breakdown":             breakdown,
        # 各指数原始得分（供 UI 展示）
        "spx_score":             round(spx_sc, 1),
        "ndx_score":             round(ndx_sc, 1),
        "sox_score":             round(sox_sc, 1),
        "vix_score":             round(vix_sc, 1),
    }
