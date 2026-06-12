"""
momentum.py — Momentum Score  [Phase 2 Spec Section 5]

定义：
  Momentum Score = 0.30×Return20Pct + 0.40×Return60Pct + 0.30×MA50SlopePct
  输出：0~100（百分位制）

Return20Pct:    该股票20日收益率在全市场的百分位
Return60Pct:    该股票60日收益率在全市场的百分位
MA50SlopePct:   该股票MA50斜率在全市场的百分位
"""
from __future__ import annotations
import math


# ── 基础工具 ──────────────────────────────────────────

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
    """计算 MA50 的斜率（每日变化率）。"""
    if len(prices) < 50:
        return 0.0
    ma = moving_average(prices, 50)
    return linreg_slope(ma[-10:])  # 用最近10日MA50斜率


def pct_rank(value: float, all_values: list[float]) -> float:
    """计算 value 在 all_values 中的百分位（0-100）。"""
    if not all_values:
        return 50.0
    below = sum(1 for v in all_values if v < value)
    return round(below / len(all_values) * 100, 1)


# ── Phase 2 Momentum Score ────────────────────────────

def momentum_score(
    prices: list[float],
    all_ret20: list[float],   # 全市场所有股票的20日收益率列表
    all_ret60: list[float],   # 全市场所有股票的60日收益率列表
    all_ma50_slopes: list[float],  # 全市场所有股票的MA50斜率列表
) -> dict:
    """
    Momentum Score = 0.30×Return20Pct + 0.40×Return60Pct + 0.30×MA50SlopePct
    输出：0-100
    """
    ret20 = period_return(prices, 20)
    ret60 = period_return(prices, 60)
    slope = ma50_slope(prices)

    ret20_pct     = pct_rank(ret20,  all_ret20)
    ret60_pct     = pct_rank(ret60,  all_ret60)
    ma50slope_pct = pct_rank(slope,  all_ma50_slopes)

    score = round(0.30 * ret20_pct + 0.40 * ret60_pct + 0.30 * ma50slope_pct, 1)

    return {
        "momentum_score":   score,         # 0-100
        "ret20":            round(ret20 * 100, 2),
        "ret60":            round(ret60 * 100, 2),
        "ret20_pct":        ret20_pct,
        "ret60_pct":        ret60_pct,
        "ma50_slope":       round(slope, 6),
        "ma50_slope_pct":   ma50slope_pct,
        # 兼容旧字段名（供 trade_decision 使用）
        "slope5":           round(period_return(prices, 5),  6),
        "slope10":          round(period_return(prices, 10), 6),
        "slope20":          round(period_return(prices, 20), 6),
    }


def momentum_acceleration(
    prices: list[float],
    all_ret20_now:  list[float],
    all_ret60_now:  list[float],
    all_slopes_now: list[float],
    lookback: int = 5,
) -> float:
    """
    Momentum Acceleration = Momentum(t) - Momentum(t-5)
    输出：-100 ~ +100（正=加速，负=减速）
    冻结为 0-100 百分位：50=持平，>50=加速，<50=减速
    """
    if len(prices) < lookback + 60:
        return 50.0
    now_mom  = momentum_score(prices, all_ret20_now, all_ret60_now, all_slopes_now)["momentum_score"]
    prev_mom = momentum_score(prices[:-lookback], all_ret20_now, all_ret60_now, all_slopes_now)["momentum_score"]
    raw_accel = now_mom - prev_mom
    # 归一化到 0-100：raw_accel 范围约 -50~+50，映射到 0-100
    normalized = max(0.0, min(100.0, 50.0 + raw_accel))
    return round(normalized, 1)


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
