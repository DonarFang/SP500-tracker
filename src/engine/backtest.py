"""
backtest.py — 回测引擎  [Phase 2 Spec Section 17]

Entry:  BUY 信号
Exit:   EXIT 信号
统计：Total Return / Win Rate / Profit Factor /
       Avg Holding Days / Max Drawdown / Sharpe Ratio
"""
from __future__ import annotations
import math
from ..features.rs import period_return, rs_percentile
from ..features.momentum import (
    momentum_score, ma50_slope, pct_rank,
    moving_average, linreg_slope,
)
from ..features.trend_health import trend_health_score, trend_lifecycle
from ..engine.leader_ranking import leader_score
from ..engine.trade_decision import trade_action


def _compute_signal_series(
    prices: list[float],
    spx_prices: list[float],
    all_ret20: list[float],
    all_ret60: list[float],
    all_slopes: list[float],
) -> list[str]:
    """为每个交易日计算 BUY/ADD/HOLD/REDUCE/EXIT 信号序列。"""
    n = len(prices)
    signals = []
    for i in range(60, n):  # 至少需要60日数据
        p = prices[:i+1]
        s = spx_prices[:min(i+1, len(spx_prices))]

        # RS
        ret60 = period_return(p, 60) or 0.0
        rs_sc = rs_percentile(ret60, all_ret60)

        # Momentum
        mom_dict = momentum_score(p, all_ret20, all_ret60, all_slopes)
        mom_sc = mom_dict["momentum_score"]

        # Trend Health
        th_dict = trend_health_score(p)
        th_sc = th_dict["trend_health"]

        # State & Action
        state = trend_lifecycle(th_sc, mom_sc, rs_sc)
        ma50 = moving_average(p, 50)[-1] if len(p) >= 50 else p[-1]
        action = trade_action(state, mom_sc, rs_sc, p[-1], ma50)
        signals.append(action)

    return signals


def run_backtest(
    symbol: str,
    prices: list[float],
    dates: list[str],
    spx_prices: list[float],
    all_ret20: list[float],
    all_ret60: list[float],
    all_slopes: list[float],
) -> dict:
    """
    对单只股票运行2年回测。
    返回统计结果。
    """
    n = len(prices)
    if n < 120:
        return {"symbol": symbol, "status": "insufficient_data"}

    signals = _compute_signal_series(prices, spx_prices, all_ret20, all_ret60, all_slopes)
    # signals[i] 对应 prices[60+i]

    trades = []
    position = None  # {"entry_price": x, "entry_date": y, "entry_idx": z}

    for i, sig in enumerate(signals):
        price_idx = 60 + i
        price = prices[price_idx]
        date  = dates[price_idx] if price_idx < len(dates) else str(price_idx)

        if position is None:
            if sig == "BUY":
                position = {
                    "entry_price": price,
                    "entry_date":  date,
                    "entry_idx":   price_idx,
                }
        else:
            if sig == "EXIT" or price_idx == n - 1:
                ret = (price - position["entry_price"]) / position["entry_price"]
                holding = price_idx - position["entry_idx"]
                trades.append({
                    "symbol":       symbol,
                    "entry_date":   position["entry_date"],
                    "exit_date":    date,
                    "entry_price":  round(position["entry_price"], 2),
                    "exit_price":   round(price, 2),
                    "return_pct":   round(ret * 100, 2),
                    "holding_days": holding,
                    "exit_reason":  sig,
                })
                position = None

    # ── 统计 ──────────────────────────────────────────
    if not trades:
        return {"symbol": symbol, "status": "no_trades", "trades": []}

    returns = [t["return_pct"] / 100 for t in trades]
    wins    = [r for r in returns if r > 0]
    losses  = [r for r in returns if r <= 0]

    total_return  = round((math.prod(1 + r for r in returns) - 1) * 100, 2)
    win_rate      = round(len(wins) / len(returns) * 100, 1) if returns else 0
    avg_win       = round(sum(wins) / len(wins) * 100, 2) if wins else 0
    avg_loss      = round(sum(losses) / len(losses) * 100, 2) if losses else 0
    profit_factor = round(abs(sum(wins)) / abs(sum(losses)), 2) if losses and sum(losses) != 0 else 0
    avg_hold      = round(sum(t["holding_days"] for t in trades) / len(trades), 1)

    # Max Drawdown（基于权益曲线）
    equity = [1.0]
    for r in returns:
        equity.append(equity[-1] * (1 + r))
    peak = equity[0]
    max_dd = 0.0
    for e in equity:
        peak = max(peak, e)
        dd = (peak - e) / peak
        max_dd = max(max_dd, dd)

    # Sharpe Ratio（日收益率，年化）
    if len(returns) > 1:
        avg_r  = sum(returns) / len(returns)
        std_r  = math.sqrt(sum((r - avg_r)**2 for r in returns) / len(returns))
        sharpe = round(avg_r / std_r * math.sqrt(252 / max(avg_hold, 1)), 2) if std_r > 0 else 0
    else:
        sharpe = 0

    return {
        "symbol":           symbol,
        "status":           "ok",
        "total_trades":     len(trades),
        "total_return_pct": total_return,
        "win_rate_pct":     win_rate,
        "profit_factor":    profit_factor,
        "avg_win_pct":      avg_win,
        "avg_loss_pct":     avg_loss,
        "avg_holding_days": avg_hold,
        "max_drawdown_pct": round(max_dd * 100, 2),
        "sharpe_ratio":     sharpe,
        "trades":           trades[-20:],  # 只保留最近20笔
    }


def run_portfolio_backtest(
    symbols: list[str],
    prices_map: dict,
    dates_map:  dict,
    spx_prices: list[float],
    all_ret20:  list[float],
    all_ret60:  list[float],
    all_slopes: list[float],
    top_n: int = 10,
) -> dict:
    """
    对 Top N 股票运行组合回测，返回汇总统计。
    """
    from ..utils import logger
    results = []
    logger.info(f"  [Backtest] 回测 {len(symbols)} 只股票...")

    for sym in symbols[:top_n]:
        if sym not in prices_map:
            continue
        try:
            r = run_backtest(
                sym, prices_map[sym], dates_map.get(sym, []),
                spx_prices, all_ret20, all_ret60, all_slopes,
            )
            if r.get("status") == "ok":
                results.append(r)
        except Exception as e:
            logger.warn(f"    {sym}: {e}")

    if not results:
        return {"status": "no_results", "symbols": symbols[:top_n]}

    # 组合汇总
    avg_return   = round(sum(r["total_return_pct"] for r in results) / len(results), 2)
    avg_winrate  = round(sum(r["win_rate_pct"] for r in results) / len(results), 1)
    avg_pf       = round(sum(r["profit_factor"] for r in results) / len(results), 2)
    avg_hold     = round(sum(r["avg_holding_days"] for r in results) / len(results), 1)
    avg_dd       = round(sum(r["max_drawdown_pct"] for r in results) / len(results), 2)
    avg_sharpe   = round(sum(r["sharpe_ratio"] for r in results) / len(results), 2)

    logger.info(f"  [Backtest] 完成：{len(results)} 只 | 平均收益 {avg_return:+.1f}% | 胜率 {avg_winrate}%")

    return {
        "status":              "ok",
        "symbols_tested":      len(results),
        "avg_total_return_pct": avg_return,
        "avg_win_rate_pct":    avg_winrate,
        "avg_profit_factor":   avg_pf,
        "avg_holding_days":    avg_hold,
        "avg_max_drawdown_pct": avg_dd,
        "avg_sharpe_ratio":    avg_sharpe,
        "individual_results":  results,
    }
