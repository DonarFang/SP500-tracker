"""
market_score.py — Market Score  [v1.0 Frozen]

Market Score = SPX(35%) + NDX(25%) + SOX(25%) + VIX(15%)
输出：0~100

5档区间（v1.0规格）：
  80-100 = Strong Risk-On
  60-80  = Risk-On
  40-60  = Neutral
  20-40  = Risk-Off
  0-20   = Defensive

Leadership Confirmed: SPX>70 AND NDX>70 AND SOX>70
"""
from __future__ import annotations
from ..features.momentum import linreg_slope


def _index_score(prices: list[float]) -> float:
    if len(prices) < 20: return 30.0
    n = len(prices); last = prices[-1]
    ma20 = sum(prices[-20:]) / 20
    ma50 = sum(prices[-50:]) / 50  if n >= 50  else ma20
    ma200= sum(prices[-200:]) / 200 if n >= 200 else ma50
    score = 0.0
    if last > ma20:  score += 20
    if last > ma50:  score += 20
    if last > ma200: score += 20
    sl20 = linreg_slope(prices[-20:])
    score += 25 if sl20 > 0.002 else 15 if sl20 > 0 else 5 if sl20 > -0.002 else 0
    if n >= 6:
        m5 = (prices[-1] - prices[-6]) / prices[-6] if prices[-6] > 0 else 0
        score += 15 if m5 > 0.02 else 8 if m5 > 0 else 3 if m5 > -0.02 else 0
    return min(score, 100.0)


def _vix_score(vix: list[float]) -> tuple[float, str, str]:
    if not vix: return 50.0, "未知", "#888"
    v = vix[-1]
    sl = linreg_slope(vix[-10:]) if len(vix) >= 10 else 0
    tb = 10 if sl < -0.005 else 0 if sl < 0.005 else -10
    if v < 15:   raw, st, col = 100, "低恐惧",   "#1D9E75"
    elif v < 20: raw, st, col = 80,  "正常",     "#378ADD"
    elif v < 25: raw, st, col = 55,  "偏高",     "#BA7517"
    elif v < 35: raw, st, col = 30,  "高恐惧",   "#D85A30"
    else:        raw, st, col = 10,  "极度恐惧", "#993C1D"
    return max(0.0, min(100.0, raw + tb)), st, col


def compute_market_score(spx, ndx, sox, vix) -> dict:
    spx_sc = _index_score(spx)
    ndx_sc = _index_score(ndx)
    sox_sc = _index_score(sox)
    vix_sc, vix_st, vix_col = _vix_score(vix)
    total = round(0.35*spx_sc + 0.25*ndx_sc + 0.25*sox_sc + 0.15*vix_sc, 1)

    # v1.0 规格：5档区间
    if total >= 80:
        state, zh, icon, col = "Strong Risk-On", "强势偏好", "🟢", "#0F6E56"
    elif total >= 60:
        state, zh, icon, col = "Risk-On",        "风险偏好", "🟢", "#1D9E75"
    elif total >= 40:
        state, zh, icon, col = "Neutral",         "中性观望", "🟡", "#BA7517"
    elif total >= 20:
        state, zh, icon, col = "Risk-Off",        "风险规避", "🔴", "#D85A30"
    else:
        state, zh, icon, col = "Defensive",       "防御模式", "⛔", "#993C1D"

    # Leadership: SPX>70 AND NDX>70 AND SOX>70
    leadership = spx_sc > 70 and ndx_sc > 70 and sox_sc > 70

    def am50(p): return len(p) >= 50 and p[-1] > sum(p[-50:]) / 50

    breakdown = {
        "SPX": {"score": round(spx_sc, 1), "weight": "35%", "above_ma50": am50(spx)},
        "NDX": {"score": round(ndx_sc, 1), "weight": "25%", "above_ma50": am50(ndx)},
        "SOX": {"score": round(sox_sc, 1), "weight": "25%", "above_ma50": am50(sox)},
        "VIX": {"score": round(vix_sc, 1), "weight": "15%", "vix_state": vix_st, "vix_color": vix_col},
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
        "spx_score":             round(spx_sc, 1),
        "ndx_score":             round(ndx_sc, 1),
        "sox_score":             round(sox_sc, 1),
        "vix_score":             round(vix_sc, 1),
    }
