"""
momentum.py — Momentum Score
Quantitative Model Specification v1.0 (Frozen)

Formula:
  Momentum Score = 50%×Slope5 + 30%×Slope10 + 20%×Slope20
  Normalized to 0-100

Weight in Leader Score: 35%
"""
from __future__ import annotations
import math


def period_return(prices: list[float], window: int) -> float:
    """计算 window 日收益率（小数）。"""
    if len(prices) < window + 1:
        return 0.0
    base = prices[-(window + 1)]
    return (prices[-1] - base) / base if base > 0 else 0.0


def moving_average(prices: list[float], window: int) -> list[float]:
    return [sum(prices[max(0, i-window+1):i+1]) / min(i+1, window)
            for i in range(len(prices))]


def linreg_slope(values: list[float]) -> float:
    """线性回归斜率（归一化为每日百分比变化）。"""
    n = len(values)
    if n < 2:
        return 0.0
    xm = (n - 1) / 2
    ym = sum(values) / n
    num = sum((i - xm) * (v - ym) for i, v in enumerate(values))
    den = sum((i - xm) ** 2 for i in range(n))
    if den == 0 or abs(ym) < 1e-10:
        return 0.0
    return num / den / abs(ym)


def ma50_slope(prices: list[float]) -> float:
    """计算 MA50 的斜率。"""
    if len(prices) < 50:
        return 0.0
    ma = moving_average(prices, 50)
    return linreg_slope(ma[-10:])


def _slope_n(prices: list[float], n: int) -> float:
    """N日价格斜率（线性回归）。"""
    if len(prices) < n:
        return 0.0
    return linreg_slope(prices[-n:])


def _normalize_slope(slope: float,
                     lo: float = -0.01,
                     hi: float = 0.01) -> float:
    """
    把斜率归一化到 0-100。
    lo=-0.01（最差），hi=+0.01（最强），0.0→50
    """
    if hi == lo:
        return 50.0
    normalized = (slope - lo) / (hi - lo) * 100
    return max(0.0, min(100.0, normalized))


def momentum_score(
    prices: list[float],
    # 以下参数保留兼容性，v1.0 不使用
    all_ret20: list[float] = None,
    all_ret60: list[float] = None,
    all_ma50_slopes: list[float] = None,
) -> dict:
    """
    Momentum Score v1.0 (Frozen):
      = 50%×Slope5 + 30%×Slope10 + 20%×Slope20
      归一化到 0-100

    使用全市场横截面动态归一化范围：
    若提供 all_ret20/all_ret60，用百分位法；
    否则用固定区间归一化（-0.01 到 +0.01）。
    """
    s5  = _slope_n(prices, 5)
    s10 = _slope_n(prices, 10)
    s20 = _slope_n(prices, 20)

    # 归一化各斜率到 0-100
    if all_ret20 is not None and len(all_ret20) > 10:
        # 用全市场百分位
        from .rs import rs_percentile
        # 收集全市场5日/10日/20日斜率
        # 简化：用 all_ret20 作为5日斜率的参考分布
        n5  = rs_percentile(s5,  all_ret20)
        n10 = rs_percentile(s10, all_ret20)
        n20 = rs_percentile(s20, all_ret20)
    else:
        # 固定区间归一化
        n5  = _normalize_slope(s5)
        n10 = _normalize_slope(s10)
        n20 = _normalize_slope(s20)

    score = round(0.50 * n5 + 0.30 * n10 + 0.20 * n20, 1)

    return {
        "momentum_score": score,      # 0-100
        "slope5":  round(s5,  6),
        "slope10": round(s10, 6),
        "slope20": round(s20, 6),
        "n5":  round(n5,  1),
        "n10": round(n10, 1),
        "n20": round(n20, 1),
        # 兼容字段
        "ret20": round(period_return(prices, 20) * 100, 2),
        "ret60": round(period_return(prices, 60) * 100, 2),
        "ret20_pct": n5,
        "ret60_pct": n20,
        "ma50_slope_pct": n10,
        "ma50_slope": round(ma50_slope(prices), 6),
    }


def momentum_acceleration(prices: list[float], lookback: int = 5) -> float:
    """
    Momentum Acceleration = Momentum(t) - Momentum(t-5)
    返回原始差值（供 rank_history 使用）。
    """
    if len(prices) < lookback + 20:
        return 0.0
    now_mom  = momentum_score(prices)["momentum_score"]
    prev_mom = momentum_score(prices[:-lookback])["momentum_score"]
    return round(now_mom - prev_mom, 2)


def volatility(prices: list[float], window: int = 20) -> float:
    """20日滚动波动率（年化标准差，%）。"""
    if len(prices) < window + 1:
        return 0.0
    w = prices[-window:]
    rets = [(w[i] - w[i-1]) / w[i-1] for i in range(1, len(w)) if w[i-1] > 0]
    if not rets:
        return 0.0
    mu  = sum(rets) / len(rets)
    std = math.sqrt(sum((r - mu) ** 2 for r in rets) / len(rets))
    return round(std * math.sqrt(252) * 100, 2)


def pct_rank(value: float, all_values: list[float]) -> float:
    if not all_values:
        return 50.0
    below = sum(1 for v in all_values if v < value)
    return round(below / len(all_values) * 100, 1)
