"""
trend_state.py — 整合所有 Phase 2 指标，计算每只股票完整状态。

关键变化：
1. RS 基准改为 SPX (^GSPC)
2. Momentum Score 改为百分位制 0-100
3. Trend Health 不含 RS/Momentum
4. 全部使用横截面百分位
"""
from __future__ import annotations
from ..features.rs import rs_score as calc_rs_score, raw_rs_vs_spx, period_return
from ..features.momentum import (
    momentum_score as calc_momentum_score,
    momentum_acceleration, volatility,
    moving_average, linreg_slope, pct_rank,
)
from ..features.trend_health import (
    trend_health_score as calc_trend_health,
    trend_lifecycle, drawdown_from_high,
    pullback_category,
)
from ..engine.leader_ranking import leader_score as calc_leader_score


def compute_stock_state(
    symbol:        str,
    prices:        list[float],
    dates:         list[str],
    spx_prices:    list[float],   # 必须是 ^GSPC，不能用 SPY
    # 横截面百分位基准（全市场）
    all_ret20:     list[float],
    all_ret60:     list[float],
    all_ma50_slopes: list[float],
    members_map:   dict,
) -> dict | None:
    """
    计算一只股票的完整 Phase 2 技术状态。
    """
    n = len(prices)
    if n < 20:
        return None

    last  = prices[-1]
    ma20  = moving_average(prices, 20)[-1]
    ma50  = moving_average(prices, 50)[-1]  if n >= 50  else last
    ma200 = moving_average(prices, 200)[-1] if n >= 200 else last
    ma20s = moving_average(prices, 20)
    ma50s = moving_average(prices, 50) if n >= 50 else []

    ma20_slope = linreg_slope(ma20s[-10:]) if len(ma20s) >= 10 else 0
    ma50_slope = linreg_slope(ma50s[-10:]) if len(ma50s) >= 10 else 0

    # ── RS Score（基准 SPX，非 SPY）─────────────────────
    ret60 = period_return(prices, 60) or 0.0
    rs_sc = calc_rs_score(ret60, all_ret60)         # 0-100
    rs_raw = raw_rs_vs_spx(prices, spx_prices, 60)  # 原始超额收益%

    # ── Momentum Score（横截面百分位制）─────────────────
    mom_dict = calc_momentum_score(prices, all_ret20, all_ret60, all_ma50_slopes)
    mom_sc   = mom_dict["momentum_score"]            # 0-100

    # ── Trend Health（纯趋势质量）───────────────────────
    th_dict = calc_trend_health(prices)
    th_sc   = th_dict["trend_health"]               # 0-100
    dd      = th_dict["drawdown_pct"]
    vol     = th_dict["volatility_pct"]

    # ── Leader Score（Phase 2 权重）──────────────────────
    ls = calc_leader_score(rs_sc, mom_sc, th_sc)    # 0-100

    # ── Trend Lifecycle State ────────────────────────────
    state = trend_lifecycle(th_sc, mom_sc, rs_sc)

    # ── 近126日图表数据 ────────────────────────────────────
    chart_dates  = dates[-126:]
    chart_prices = [round(p, 2) for p in prices[-126:]]
    chart_ma20   = [round(v, 2) for v in ma20s[-126:]]
    chart_ma50   = [round(v, 2) for v in ma50s[-126:]] if ma50s else []

    info = members_map.get(symbol, {})

    return {
        # 基础
        "symbol":          symbol,
        "name":            info.get("name", symbol),
        "sector":          info.get("sector", "Other"),
        "price":           round(last, 2),
        "ma20":            round(ma20, 2),
        "ma50":            round(ma50, 2),
        "ma200":           round(ma200, 2),
        "above_ma20":      last > ma20,
        "above_ma50":      last > ma50,
        "above_ma200":     last > ma200,
        "ma20_slope":      round(ma20_slope, 6),
        "ma50_slope":      round(ma50_slope, 6),
        # RS
        "rs_score":        rs_sc,
        "rs_raw":          rs_raw,
        "ret60":           round(ret60 * 100, 2),
        # Momentum
        "momentum_score":  mom_sc,
        "ret20":           mom_dict["ret20"],
        "ret60_pct":       mom_dict["ret60_pct"],
        "ret20_pct":       mom_dict["ret20_pct"],
        "ma50_slope_pct":  mom_dict["ma50_slope_pct"],
        # 兼容字段
        "slope5":          mom_dict["slope5"],
        "slope10":         mom_dict["slope10"],
        "slope20":         mom_dict["slope20"],
        # Trend Health
        "trend_health":    th_sc,
        "drawdown_pct":    dd,
        "volatility_pct":  vol,
        "price_structure_score": th_dict["price_structure_score"],
        "ma50_slope_score":      th_dict["ma50_slope_score"],
        "drawdown_score":        th_dict["drawdown_score"],
        "volatility_score":      th_dict["volatility_score"],
        # Scores
        "leader_score":    ls,
        "trend_state":     state,
        # Chart
        "chart_dates":     chart_dates,
        "chart_prices":    chart_prices,
        "chart_ma20":      chart_ma20,
        "chart_ma50":      chart_ma50,
    }
