"""
trend_health.py — Trend Health Score  [Phase 2 Spec Section 6]

定义：纯趋势质量，禁止包含 RS 或 Momentum。

组成：
  Price Structure    30%   (Close>MA20/50/200)
  MA50 Slope Quality 25%   (斜率强度)
  Drawdown Stability 25%   (60日高点回撤)
  Volatility Quality 20%   (20日年化波动率)

输出：0~100
"""
from __future__ import annotations
import math
from .momentum import moving_average, linreg_slope, volatility


# ── Price Structure（满分30）────────────────────────────

def price_structure_score(prices: list[float]) -> float:
    """Close > MA20(10) + MA50(10) + MA200(10) = 30"""
    n = len(prices)
    last = prices[-1]
    score = 0.0
    if n >= 20  and last > sum(prices[-20:])/20:   score += 10
    if n >= 50  and last > sum(prices[-50:])/50:   score += 10
    if n >= 200 and last > sum(prices[-200:])/200: score += 10
    elif n >= 100:
        ma200_approx = sum(prices[-n:]) / n
        if last > ma200_approx: score += 10
    return score


# ── MA50 Slope Quality（满分25）────────────────────────

def ma50_slope_score(prices: list[float]) -> float:
    """MA50 斜率强度，归一化到 0-25"""
    if len(prices) < 50:
        return 12.5  # 数据不足给中间分
    ma = moving_average(prices, 50)
    slope = linreg_slope(ma[-10:])
    # slope 典型范围约 -0.005 ~ +0.005
    # 映射：slope >= +0.003 → 25分，slope <= -0.003 → 0分
    normalized = max(0.0, min(1.0, (slope + 0.003) / 0.006))
    return round(normalized * 25, 2)


# ── Drawdown Stability（满分25）────────────────────────

def drawdown_from_high(prices: list[float], window: int = 60) -> float:
    """从近 window 日高点计算当前回撤百分比（正值）。"""
    if not prices:
        return 0.0
    recent = prices[-window:] if len(prices) >= window else prices
    peak = max(recent)
    return round((peak - prices[-1]) / peak * 100, 2) if peak > 0 else 0.0


def drawdown_stability_score(dd_pct: float) -> float:
    """
    规格书定义（满分25）：
    DD < 5%  → 100 → 25分
    5~8%     → 80  → 20分
    8~12%    → 50  → 12.5分
    12~15%   → 25  → 6.25分
    > 15%    → 0   → 0分
    """
    if dd_pct < 5:   raw = 100
    elif dd_pct < 8:  raw = 80
    elif dd_pct < 12: raw = 50
    elif dd_pct < 15: raw = 25
    else:             raw = 0
    return raw * 25 / 100


# ── Volatility Quality（满分20）────────────────────────

def volatility_quality_score(vol_pct: float) -> float:
    """
    规格书定义（满分20）：
    Vol < 20%  → 100 → 20分
    20~35%     → 75  → 15分
    35~50%     → 50  → 10分
    50~70%     → 25  → 5分
    > 70%      → 0   → 0分
    """
    if vol_pct < 20:   raw = 100
    elif vol_pct < 35:  raw = 75
    elif vol_pct < 50:  raw = 50
    elif vol_pct < 70:  raw = 25
    else:               raw = 0
    return raw * 20 / 100


# ── Trend Health Score（总分0-100）─────────────────────

def trend_health_score(prices: list[float]) -> dict:
    """
    Trend Health Score（纯趋势质量，不含RS/Momentum）
    = Price Structure(30%) + MA50 Slope(25%) + Drawdown(25%) + Volatility(20%)
    """
    dd  = drawdown_from_high(prices)
    vol = volatility(prices)

    ps  = price_structure_score(prices)         # 0-30
    ms  = ma50_slope_score(prices)              # 0-25
    ds  = drawdown_stability_score(dd)          # 0-25
    vs  = volatility_quality_score(vol)         # 0-20

    total = round(ps + ms + ds + vs, 1)

    return {
        "trend_health":          total,          # 0-100
        "price_structure_score": ps,
        "ma50_slope_score":      ms,
        "drawdown_score":        ds,
        "volatility_score":      vs,
        "drawdown_pct":          dd,
        "volatility_pct":        vol,
    }


# ── Trend Lifecycle State  [Spec Section 13] ──────────

def trend_lifecycle(th: float, mom: float, rs: float) -> str:
    """
    Expansion:  TH>=80 AND Mom>=80 AND RS>=80
    Healthy:    TH>=65 AND Mom>=65
    Mature:     TH>=50
    Weakening:  TH>=30
    Broken:     TH<30
    """
    if th >= 80 and mom >= 80 and rs >= 80:
        return "Expansion"
    if th >= 65 and mom >= 65:
        return "Healthy Trend"
    if th >= 50:
        return "Mature Trend"
    if th >= 30:
        return "Weakening Trend"
    return "Broken Trend"


# ── Pullback category（供 UI 展示用）──────────────────

def pullback_category(dd_pct: float) -> str:
    if dd_pct < 5:   return "healthy"
    if dd_pct < 8:   return "normal"
    if dd_pct < 12:  return "deep"
    if dd_pct < 15:  return "warning"
    return "breakdown"
