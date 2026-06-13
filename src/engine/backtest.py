"""
backtest.py — Backtest Engine
Backtest Methodology v1.0 (Frozen)

3个验证层：
  Layer A: Leader Engine Validation (Leader Score 桶分析)
  Layer B: Promotion Engine Validation (晋升率分析)
  Layer C: Trade Rule Validation (信号收益分析)

原则：
  - 无前视偏差：每个时间点只用该点之前的数据
  - 所有指标历史重建
  - 对比 SPX 基准
"""
from __future__ import annotations
import math
from ..features.rs import period_return, rs_percentile
from ..features.momentum import (
    momentum_score as calc_momentum, moving_average, linreg_slope
)
from ..features.trend_health import trend_health_score as calc_trend_health
from ..engine.leader_ranking import leader_score as calc_leader_score
from ..engine.trade_decision import trade_action
from ..utils import logger


# ══════════════════════════════════════════════════════════════════
# 工具函数
# ══════════════════════════════════════════════════════════════════

def forward_return(prices: list[float], t: int, days: int) -> float | None:
    """计算 t 日后 days 天的收益率。"""
    if t + days >= len(prices) or t < 0:
        return None
    if prices[t] <= 0:
        return None
    return (prices[t + days] - prices[t]) / prices[t]


def _rebuild_leader_score(prices: list[float], spx_prices: list[float],
                           all_stocks_prices: dict[str, list[float]],
                           t: int) -> dict | None:
    """
    在时间点 t 重建该股票的所有指标（无前视偏差）。
    """
    p = prices[:t+1]
    spx = spx_prices[:t+1]
    if len(p) < 60:
        return None

    # RS Score（全市场横截面）
    all_ret60 = []
    for sym_p in all_stocks_prices.values():
        r = period_return(sym_p[:t+1], 60)
        if r is not None:
            all_ret60.append(r)
    ret60 = period_return(p, 60) or 0.0
    rs = rs_percentile(ret60, all_ret60)

    # Momentum Score（v1.0: 50%S5 + 30%S10 + 20%S20）
    mom_dict = calc_momentum(p)
    mom = mom_dict["momentum_score"]

    # Trend Health
    th_dict = calc_trend_health(p)
    th = th_dict["trend_health"]

    # Leader Score
    ls = calc_leader_score(rs, mom, th)

    # MA50 slope（用于 trade_decision）
    ma50s = moving_average(p, 50)
    ma50_sl = linreg_slope(ma50s[-10:]) if len(ma50s) >= 10 else 0
    ma50_val = ma50s[-1] if ma50s else p[-1]

    return {
        "rs_score":     rs,
        "momentum_score": mom,
        "trend_health": th,
        "leader_score": ls,
        "price":        p[-1],
        "ma50":         ma50_val,
        "ma50_slope":   ma50_sl,
        "drawdown_pct": th_dict["drawdown_pct"],
    }


# ══════════════════════════════════════════════════════════════════
# Layer A: Leader Engine Validation
# ══════════════════════════════════════════════════════════════════

def run_leader_engine_validation(
    symbols: list[str],
    prices_map: dict[str, list[float]],
    spx_prices: list[float],
    forward_days: list[int] = [5, 10, 20, 30],
    step: int = 5,           # 每隔 step 天计算一次（节省时间）
    min_history: int = 120,  # 最少需要多少天历史
) -> dict:
    """
    Layer A: Leader Score Bucket Analysis

    对每个时间点 t，计算所有股票的 Leader Score，
    分5个桶，测量前向收益。
    """
    logger.info("[Backtest Layer A] Leader Engine Validation...")

    buckets = {"A": (90, 100), "B": (80, 90), "C": (70, 80),
               "D": (60, 70), "E": (0, 60)}

    # 结果结构：{bucket: {days: [returns]}}
    results = {b: {d: [] for d in forward_days} for b in buckets}

    # 获取最短价格序列长度
    min_len = min(len(p) for p in prices_map.values()) if prices_map else 0
    n_days = min(min_len, len(spx_prices))

    processed = 0
    for t in range(min_history, n_days - max(forward_days), step):
        # 计算该时间点所有股票的 Leader Score
        day_scores = {}
        for sym in symbols:
            if sym not in prices_map:
                continue
            info = _rebuild_leader_score(
                prices_map[sym], spx_prices,
                {s: prices_map[s] for s in symbols[:50]},  # 用前50只作为横截面样本
                t
            )
            if info:
                day_scores[sym] = info

        if len(day_scores) < 20:
            continue

        # 分桶并记录前向收益
        for sym, info in day_scores.items():
            ls = info["leader_score"]
            p_series = prices_map[sym]

            for bucket, (lo, hi) in buckets.items():
                if lo <= ls < hi:
                    for days in forward_days:
                        ret = forward_return(p_series, t, days)
                        if ret is not None:
                            results[bucket][days].append(ret * 100)
                    break

        processed += 1
        if processed % 20 == 0:
            logger.info(f"  Layer A: {t}/{n_days} 天已处理...")

    # 汇总统计
    summary = {}
    for bucket in buckets:
        summary[bucket] = {}
        for days in forward_days:
            rets = results[bucket][days]
            if not rets:
                summary[bucket][f"fwd{days}d"] = {"n": 0}
                continue
            summary[bucket][f"fwd{days}d"] = {
                "n":        len(rets),
                "avg_ret":  round(sum(rets) / len(rets), 3),
                "med_ret":  round(sorted(rets)[len(rets)//2], 3),
                "win_rate": round(sum(1 for r in rets if r > 0) / len(rets) * 100, 1),
                "vol":      round(math.sqrt(sum((r - sum(rets)/len(rets))**2 for r in rets)/len(rets)), 3),
            }

    # 单调性检验
    monotonic = {}
    for days in forward_days:
        avg_rets = []
        for b in ["A","B","C","D","E"]:
            k = f"fwd{days}d"
            avg_rets.append(summary[b].get(k, {}).get("avg_ret", 0))
        # 检查是否 A > B > C > D > E
        is_monotonic = all(avg_rets[i] >= avg_rets[i+1] for i in range(len(avg_rets)-1))
        monotonic[f"fwd{days}d"] = is_monotonic

    pass_count = sum(1 for v in monotonic.values() if v)
    status = "PASS" if pass_count >= 3 else "PARTIAL" if pass_count >= 2 else "FAIL"

    logger.info(f"  Layer A 完成: {status} ({pass_count}/4 时间窗口单调)")
    return {
        "layer": "A",
        "name":  "Leader Engine Validation",
        "status": status,
        "monotonic": monotonic,
        "bucket_summary": summary,
        "buckets_defined": {b: f"{lo}-{hi}" for b, (lo, hi) in buckets.items()},
    }


# ══════════════════════════════════════════════════════════════════
# Layer C: Trade Rule Validation（最重要，先实现）
# ══════════════════════════════════════════════════════════════════

def run_trade_rule_validation(
    symbols: list[str],
    prices_map: dict[str, list[float]],
    spx_prices: list[float],
    forward_days: list[int] = [5, 10, 20, 30],
    step: int = 5,
    min_history: int = 120,
    market_score_default: float = 60.0,
) -> dict:
    """
    Layer C: Trade Rule Validation

    对每个 BUY/EXIT 信号，测量信号后的前向收益，
    并与 SPX 同期收益对比。
    """
    logger.info("[Backtest Layer C] Trade Rule Validation...")

    signal_returns = {
        "BUY":  {d: [] for d in forward_days},
        "ADD":  {d: [] for d in forward_days},
        "EXIT": {d: [] for d in forward_days},
        "HOLD": {d: [] for d in forward_days},
    }
    spx_returns = {d: [] for d in forward_days}  # SPX 同期对比

    min_len = min(len(p) for p in prices_map.values()) if prices_map else 0
    n_days = min(min_len, len(spx_prices))
    processed = 0

    for t in range(min_history, n_days - max(forward_days), step):
        # SPX 前向收益（用于基准比较）
        for days in forward_days:
            spx_ret = forward_return(spx_prices, t, days)
            if spx_ret is not None:
                spx_returns[days].append(spx_ret * 100)

        # 每只股票生成信号
        all_ret60 = []
        for sym in symbols:
            if sym in prices_map:
                r = period_return(prices_map[sym][:t+1], 60)
                if r is not None:
                    all_ret60.append(r)

        for sym in symbols:
            if sym not in prices_map:
                continue
            p = prices_map[sym][:t+1]
            if len(p) < 60:
                continue

            ret60 = period_return(p, 60) or 0.0
            rs = rs_percentile(ret60, all_ret60)
            mom_dict = calc_momentum(p)
            mom = mom_dict["momentum_score"]
            th_dict = calc_trend_health(p)
            th = th_dict["trend_health"]
            ls = calc_leader_score(rs, mom, th)

            # Trend State
            from ..features.trend_health import trend_lifecycle
            state = trend_lifecycle(th, mom, rs)

            ma50s = moving_average(p, 50)
            ma50_val = ma50s[-1] if ma50s else p[-1]
            ma50_sl  = linreg_slope(ma50s[-10:]) if len(ma50s) >= 10 else 0

            action = trade_action(
                state, mom, rs, p[-1], ma50_val,
                ma50_sl, ls, th, market_score_default
            )

            if action not in signal_returns:
                continue

            p_full = prices_map[sym]
            for days in forward_days:
                ret = forward_return(p_full, t, days)
                if ret is not None:
                    signal_returns[action][days].append(ret * 100)

        processed += 1
        if processed % 20 == 0:
            logger.info(f"  Layer C: {t}/{n_days} 天已处理...")

    # 汇总
    def stats(rets):
        if not rets:
            return {"n": 0}
        avg = sum(rets) / len(rets)
        med = sorted(rets)[len(rets)//2]
        std = math.sqrt(sum((r-avg)**2 for r in rets)/len(rets)) if len(rets)>1 else 0
        wins = [r for r in rets if r > 0]
        losses = [r for r in rets if r <= 0]
        pf = abs(sum(wins)/sum(losses)) if losses and sum(losses) != 0 else 0
        sh = avg/std * math.sqrt(252/20) if std > 0 else 0
        return {
            "n":          len(rets),
            "avg_ret":    round(avg, 3),
            "med_ret":    round(med, 3),
            "win_rate":   round(len(wins)/len(rets)*100, 1),
            "vol":        round(std, 3),
            "profit_factor": round(pf, 2),
            "sharpe":     round(sh, 2),
        }

    summary = {}
    for sig in signal_returns:
        summary[sig] = {f"fwd{d}d": stats(signal_returns[sig][d]) for d in forward_days}

    spx_summary = {f"fwd{d}d": stats(spx_returns[d]) for d in forward_days}

    # 判断 PASS/FAIL
    buy_vs_spx = []
    for days in forward_days:
        k = f"fwd{days}d"
        buy_avg = summary["BUY"].get(k, {}).get("avg_ret", 0)
        spx_avg = spx_summary.get(k, {}).get("avg_ret", 0)
        buy_vs_spx.append(buy_avg > spx_avg)

    pass_count = sum(buy_vs_spx)
    status = "PASS" if pass_count >= 3 else "PARTIAL" if pass_count >= 2 else "FAIL"

    logger.info(f"  Layer C 完成: {status} (BUY跑赢SPX {pass_count}/4 时间窗口)")
    return {
        "layer":        "C",
        "name":         "Trade Rule Validation",
        "status":       status,
        "buy_vs_spx":   buy_vs_spx,
        "signal_summary": summary,
        "spx_benchmark":  spx_summary,
    }


# ══════════════════════════════════════════════════════════════════
# Layer B: Promotion Engine Validation（需要历史数据积累）
# ══════════════════════════════════════════════════════════════════

def run_promotion_engine_validation(
    symbols: list[str],
    prices_map: dict[str, list[float]],
    spx_prices: list[float],
    promotion_thresholds: list[int] = [80, 85, 90],
    track_days: list[int] = [5, 10, 20, 30],
    step: int = 5,
    min_history: int = 120,
) -> dict:
    """
    Layer B: Promotion Engine Validation

    验证 Promotion Score 能否预测未来晋升 Top30。
    注意：需要历史排名数据，首次运行用 Leader Score 近似。
    """
    logger.info("[Backtest Layer B] Promotion Engine Validation...")

    threshold_results = {t: {"promoted": 0, "total": 0} for t in promotion_thresholds}
    all_ret60 = []

    min_len = min(len(p) for p in prices_map.values()) if prices_map else 0
    n_days = min(min_len, len(spx_prices))
    processed = 0

    for t in range(min_history, n_days - max(track_days), step):
        # 计算全市场横截面
        day_scores = {}
        all_ret60 = []
        for sym in symbols:
            if sym not in prices_map:
                continue
            p = prices_map[sym][:t+1]
            if len(p) < 60:
                continue
            r = period_return(p, 60)
            if r is not None:
                all_ret60.append(r)

        for sym in symbols:
            if sym not in prices_map:
                continue
            p = prices_map[sym][:t+1]
            if len(p) < 60:
                continue
            ret60 = period_return(p, 60) or 0.0
            rs = rs_percentile(ret60, all_ret60)
            mom = calc_momentum(p)["momentum_score"]
            th = calc_trend_health(p)["trend_health"]
            ls = calc_leader_score(rs, mom, th)
            # 用 Leader Score 近似 Promotion Score（历史 RankVelocity 不可用）
            promo_approx = ls
            day_scores[sym] = {"leader_score": ls, "promotion_score": promo_approx}

        if not day_scores:
            continue

        # 当前 Top30
        top30_now = set(sorted(day_scores, key=lambda s: day_scores[s]["leader_score"], reverse=True)[:30])

        # 检查各阈值
        for thresh in promotion_thresholds:
            candidates = [s for s, v in day_scores.items()
                         if v["promotion_score"] >= thresh and s not in top30_now]
            for sym in candidates:
                threshold_results[thresh]["total"] += 1
                # 未来某天进入 Top30？
                for days in track_days:
                    future_t = t + days
                    if future_t >= n_days:
                        continue
                    # 重算未来 Top30
                    future_scores = {}
                    for s in symbols:
                        if s not in prices_map:
                            continue
                        fp = prices_map[s][:future_t+1]
                        if len(fp) < 60:
                            continue
                        fret60 = period_return(fp, 60) or 0.0
                        frs = rs_percentile(fret60, all_ret60)
                        fmom = calc_momentum(fp)["momentum_score"]
                        fth = calc_trend_health(fp)["trend_health"]
                        future_scores[s] = calc_leader_score(frs, fmom, fth)
                    future_top30 = set(sorted(future_scores, key=lambda s: future_scores[s], reverse=True)[:30])
                    if sym in future_top30:
                        threshold_results[thresh]["promoted"] += 1
                        break  # 只计一次

        processed += 1
        if processed % 20 == 0:
            logger.info(f"  Layer B: {t}/{n_days} 天已处理...")

    # 汇总
    summary = {}
    for thresh in promotion_thresholds:
        total = threshold_results[thresh]["total"]
        promoted = threshold_results[thresh]["promoted"]
        rate = round(promoted / total * 100, 1) if total > 0 else 0
        summary[f"score_{thresh}+"] = {
            "total_candidates": total,
            "promoted":         promoted,
            "promotion_rate":   rate,
        }

    # PASS: 更高分对应更高晋升率
    rates = [summary[f"score_{t}+"]["promotion_rate"] for t in sorted(promotion_thresholds)]
    is_monotonic = all(rates[i] <= rates[i+1] for i in range(len(rates)-1))
    status = "PASS" if is_monotonic and any(r > 20 for r in rates) else "PARTIAL" if any(r > 10 for r in rates) else "FAIL"

    logger.info(f"  Layer B 完成: {status}")
    return {
        "layer":   "B",
        "name":    "Promotion Engine Validation",
        "status":  status,
        "monotonic": is_monotonic,
        "threshold_summary": summary,
        "note":    "Layer B 使用 Leader Score 近似 Promotion Score（需历史RankVelocity数据后重跑）",
    }


# ══════════════════════════════════════════════════════════════════
# 主函数：运行完整回测
# ══════════════════════════════════════════════════════════════════

def run_full_backtest(
    symbols: list[str],
    prices_map: dict[str, list[float]],
    spx_prices: list[float],
    run_layer_b: bool = False,  # Layer B 较慢，默认跳过
) -> dict:
    """
    运行完整3层回测验证。
    返回汇总结果，供 export_json 写入 backtest.json。
    """
    logger.info("=== 开始回测验证（Backtest Methodology v1.0）===")

    results = {}

    # Layer A: Leader Engine
    results["layer_a"] = run_leader_engine_validation(
        symbols, prices_map, spx_prices
    )

    # Layer C: Trade Rules
    results["layer_c"] = run_trade_rule_validation(
        symbols, prices_map, spx_prices
    )

    # Layer B: Promotion（可选，较慢）
    if run_layer_b:
        results["layer_b"] = run_promotion_engine_validation(
            symbols, prices_map, spx_prices
        )

    # 整体评分
    statuses = [v["status"] for v in results.values()]
    overall = "PASS" if all(s == "PASS" for s in statuses) else \
              "PARTIAL" if any(s in ("PASS","PARTIAL") for s in statuses) else "FAIL"

    logger.info(f"=== 回测完成: {overall} ===")
    logger.info(f"  Layer A: {results['layer_a']['status']}")
    logger.info(f"  Layer C: {results['layer_c']['status']}")

    return {
        "overall_status": overall,
        "methodology":    "Backtest Methodology v1.0",
        "model_version":  "Quantitative Model Spec v1.0 (Frozen)",
        "results":        results,
    }
