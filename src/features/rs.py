"""
rs.py — Relative Strength Score  [Phase 2 Spec Section 4]

定义：
  RS Percentile = 股票60日收益率在全部SP500中的横截面百分位
  基准：SPX (^GSPC)，禁止使用 SPY

输出：0~100
  RS=95 表示跑赢95%的SP500股票
"""
from __future__ import annotations


def period_return(prices: list[float], window: int) -> float | None:
    """计算最近 window 日的收益率。"""
    if len(prices) < window + 1:
        return None
    base = prices[-(window + 1)]
    return (prices[-1] - base) / base if base > 0 else None


def rs_percentile(symbol_return: float, all_returns: list[float]) -> float:
    """
    RS 百分位（0-100）。
    symbol_return: 该股票的60日收益率（小数，如0.15表示+15%）
    all_returns:   全市场所有成分股的60日收益率列表
    """
    if not all_returns:
        return 50.0
    below = sum(1 for r in all_returns if r < symbol_return)
    return round(below / len(all_returns) * 100, 1)


def rs_score(symbol_return: float, all_returns: list[float]) -> float:
    """
    RS Score = RS Percentile，直接作为 0-100 分值。
    """
    return rs_percentile(symbol_return, all_returns)


def raw_rs_vs_spx(stock_prices: list[float], spx_prices: list[float],
                   window: int = 60) -> float:
    """
    原始 RS = 股票N日收益率 - SPX同期收益率。
    基准必须是 SPX (^GSPC)，不能用 SPY。
    """
    n = min(len(stock_prices), len(spx_prices))
    if n < window + 1:
        return 0.0
    sp = stock_prices[-n:]
    sx = spx_prices[-n:]
    sr = (sp[-1] - sp[-window-1]) / sp[-window-1] * 100 if sp[-window-1] > 0 else 0
    mr = (sx[-1] - sx[-window-1]) / sx[-window-1] * 100 if sx[-window-1] > 0 else 0
    return round(sr - mr, 2)
