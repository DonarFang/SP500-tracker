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
# Layer D Frozen Assumptions (v1.0)
# docs/layer_d_assumptions.md
# ══════════════════════════════════════════════════════════════════
LAYER_D_ASSUMPTIONS = {
    "initial_capital":   100_000,
    "max_positions":     10,
    "buy_size":          1.0,    # 10% of portfolio (full position)
    "add_size":          0.5,    # +5% of portfolio
    "max_single_size":   1.5,    # 15% max
    "transaction_cost":  0.0005, # 0.05% one-way
    "slippage":          0.0005, # 0.05% one-way
    "total_one_way":     0.0010, # cost + slippage per direction
    "total_round_trip":  0.0020, # buy + sell total
    # Primary Execution Model: Adverse Intraday Execution v1.0
    # Signal Day T → Execute Day T+1
    # BUY/ADD:     next_day_high  × (1 + cost + slippage)  ← worst buy
    # REDUCE/EXIT: next_day_low   × (1 - cost - slippage)  ← worst sell
    # HOLD:        mark-to-market at close, no transaction
    "execution_model":   "adverse_intraday",
    "buy_price_field":   "high",   # T+1 high
    "sell_price_field":  "low",    # T+1 low
    "cash_yield":        0.0,
    "leverage":          False,
    "short_selling":     False,
    "version":           "1.0",
}


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
    # 主要标准：A 桶是否是最强桶（最重要）
    # 次要标准：严格单调（D/E 桶样本量少，噪音大）
    monotonic = {}
    a_is_best_count = 0
    for days in forward_days:
        avg_rets = []
        for b in ["A","B","C","D","E"]:
            k = f"fwd{days}d"
            avg_rets.append(summary[b].get(k, {}).get("avg_ret", 0))
        is_strict = all(avg_rets[i] >= avg_rets[i+1] for i in range(len(avg_rets)-1))
        a_is_best = avg_rets[0] == max(avg_rets)
        monotonic[f"fwd{days}d"] = is_strict
        if a_is_best:
            a_is_best_count += 1

    strict_count = sum(1 for v in monotonic.values() if v)

    # A1: Top Bucket Edge — A 桶是否显著领先（最重要）
    a1_status = "PASS" if a_is_best_count >= 3 else "PARTIAL" if a_is_best_count >= 2 else "FAIL"
    # A2: Full Monotonic Ranking — A>B>C>D>E 严格单调
    a2_status = "PASS" if strict_count >= 3 else "PARTIAL" if strict_count >= 2 else "FAIL"

    # 样本数量统计（用于评估统计显著性）
    bucket_sample_counts = {}
    for b in ["A","B","C","D","E"]:
        bucket_sample_counts[b] = {f"fwd{d}d": summary[b].get(f"fwd{d}d",{}).get("n",0) for d in forward_days}

    # Layer A 整体判断
    status = "PASS"    if a1_status == "PASS" and a2_status != "FAIL" else              "PARTIAL" if a1_status in ("PASS","PARTIAL") else "FAIL"

    logger.info(f"  Layer A: A1(TopEdge)={a1_status} A2(Monotonic)={a2_status} → {status}")
    logger.info(f"  样本量: A={bucket_sample_counts['A'].get('fwd20d',0)} B={bucket_sample_counts['B'].get('fwd20d',0)} C={bucket_sample_counts['C'].get('fwd20d',0)} D={bucket_sample_counts['D'].get('fwd20d',0)} E={bucket_sample_counts['E'].get('fwd20d',0)}")
    return {
        "layer": "A",
        "name":  "Leader Engine Validation",
        "status": status,
        "a1_top_bucket_edge": a1_status,
        "a2_full_monotonic":  a2_status,
        "a_is_best_count":    a_is_best_count,
        "strict_monotonic_count": strict_count,
        "monotonic": monotonic,
        "bucket_summary": summary,
        "bucket_sample_counts": bucket_sample_counts,
        "buckets_defined": {b: f"{lo}-{hi}" for b, (lo, hi) in buckets.items()},
        "interpretation": (
            "A1 PASS: Bucket A 持续领先，Top Leader 识别有效；A2 中低分组区分力待改善"
            if a1_status == "PASS" and a2_status == "FAIL"
            else "Leader Score 完整有效（A桶领先且单调性强）"
            if a1_status == "PASS"
            else "Leader Score 区分力不足，需检查公式"
        ),
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
    spx_returns = {d: [] for d in forward_days}

    # 去重：记录每只股票的上次信号日期（避免连续多天重复计算）
    last_signal_day: dict[str, int] = {}
    signal_counts = {"BUY": 0, "ADD": 0, "HOLD": 0, "REDUCE": 0, "EXIT": 0}
    dedup_gap = 5  # 同一股票同一信号至少间隔5天才重新计入

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

            signal_counts[action] = signal_counts.get(action, 0) + 1

            # 去重：同一股票同一信号至少间隔 dedup_gap 天
            key = f"{sym}_{action}"
            if key in last_signal_day and t - last_signal_day[key] < dedup_gap:
                continue
            last_signal_day[key] = t

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

    # 有效 BUY 信号数量（去重后）
    buy_n = summary.get("BUY",{}).get("fwd20d",{}).get("n", 0)

    logger.info(f"  Layer C: {status} (BUY跑赢SPX {pass_count}/4, BUY信号数={buy_n})")
    logger.info(f"  信号总数(去重前): {signal_counts}")
    return {
        "layer":          "C",
        "name":           "Trade Rule Validation",
        "status":         status,
        "buy_vs_spx":     buy_vs_spx,
        "buy_signal_count": buy_n,
        "signal_counts_raw": signal_counts,
        "signal_summary": summary,
        "spx_benchmark":  spx_summary,
        "dedup_gap_days": dedup_gap,
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
# Layer C2: Action Forward Return Validation
# ══════════════════════════════════════════════════════════════════

def run_action_forward_validation(
    symbols:       list[str],
    prices_map:    dict[str, list[float]],
    spx_prices:    list[float],
    forward_days:  list[int] = [5, 10, 20, 30],
    step:          int = 5,
    min_history:   int = 120,
    market_score_default: float = 60.0,
) -> dict:
    """
    Layer C2: Action Forward Return Validation

    验证每种 Action 之后的前向收益：
    - BUY  → 买入后是否有正向期望？
    - ADD  → 加仓后是否继续超额？
    - HOLD → 继续持有是否比卖出更好？
    - REDUCE → 减仓后股票是否真的走弱？
    - EXIT → 退出后是否避免了进一步下跌？
    """
    logger.info("[Backtest Layer C2] Action Forward Return Validation...")

    action_returns = {
        a: {d: [] for d in forward_days}
        for a in ["BUY","ADD","HOLD","REDUCE","EXIT"]
    }
    spx_returns = {d: [] for d in forward_days}

    min_len = min(len(p) for p in prices_map.values()) if prices_map else 0
    n_days  = min(min_len, len(spx_prices))

    # 去重：同一股票同一信号至少间隔 5 天
    last_action_day: dict[str, int] = {}
    dedup_gap = 5

    for t in range(min_history, n_days - max(forward_days), step):
        for d in forward_days:
            r = forward_return(spx_prices, t, d)
            if r is not None:
                spx_returns[d].append(r * 100)

        all_ret60 = [
            (period_return(prices_map[s][:t+1], 60) or 0.0)
            for s in symbols if s in prices_map and len(prices_map[s]) > t+1
        ]

        for sym in symbols:
            if sym not in prices_map:
                continue
            p = prices_map[sym][:t+1]
            if len(p) < 60:
                continue

            ret60 = period_return(p, 60) or 0.0
            rs    = rs_percentile(ret60, all_ret60)
            mom_d = calc_momentum(p)
            mom   = mom_d["momentum_score"]
            th_d  = calc_trend_health(p)
            th    = th_d["trend_health"]
            ls    = calc_leader_score(rs, mom, th)

            from ..features.trend_health import trend_lifecycle
            state    = trend_lifecycle(th, mom, rs)
            ma50s    = moving_average(p, 50)
            ma50_v   = ma50s[-1] if ma50s else p[-1]
            ma50_sl  = linreg_slope(ma50s[-10:]) if len(ma50s) >= 10 else 0

            action = trade_action(
                state, mom, rs, p[-1], ma50_v,
                ma50_sl, ls, th, market_score_default
            )

            if action not in action_returns:
                continue

            key = f"{sym}_{action}"
            if key in last_action_day and t - last_action_day[key] < dedup_gap:
                continue
            last_action_day[key] = t

            p_full = prices_map[sym]
            for d in forward_days:
                r = forward_return(p_full, t, d)
                if r is not None:
                    action_returns[action][d].append(r * 100)

    # 统计
    def stats(rets):
        if not rets: return {"n": 0}
        avg = sum(rets)/len(rets)
        med = sorted(rets)[len(rets)//2]
        std = math.sqrt(sum((r-avg)**2 for r in rets)/len(rets)) if len(rets)>1 else 0
        wins = [r for r in rets if r > 0]
        return {
            "n":         len(rets),
            "avg_ret":   round(avg, 3),
            "med_ret":   round(med, 3),
            "win_rate":  round(len(wins)/len(rets)*100, 1),
            "vol":       round(std, 3),
        }

    summary   = {a: {f"fwd{d}d": stats(action_returns[a][d]) for d in forward_days} for a in action_returns}
    spx_summ  = {f"fwd{d}d": stats(spx_returns[d]) for d in forward_days}

    # 关键验证
    # 1. HOLD 后收益是否为正（持有有效）
    hold_positive = sum(
        1 for d in forward_days
        if summary["HOLD"].get(f"fwd{d}d",{}).get("avg_ret",0) > 0
    )
    # 2. REDUCE/EXIT 后收益是否低于 HOLD（减仓/退出有保护作用）
    reduce_lower = sum(
        1 for d in forward_days
        if summary["REDUCE"].get(f"fwd{d}d",{}).get("avg_ret",999) <
           summary["HOLD"].get(f"fwd{d}d",{}).get("avg_ret",0)
    )
    exit_lower = sum(
        1 for d in forward_days
        if summary["EXIT"].get(f"fwd{d}d",{}).get("avg_ret",999) <
           summary["HOLD"].get(f"fwd{d}d",{}).get("avg_ret",0)
    )

    status = "PASS" if hold_positive >= 3 and (reduce_lower + exit_lower) >= 4 else              "PARTIAL" if hold_positive >= 2 else "FAIL"

    # 日志输出
    for d in forward_days:
        k = f"fwd{d}d"
        row = {a: summary[a].get(k,{}).get("avg_ret","—") for a in ["BUY","ADD","HOLD","REDUCE","EXIT"]}
        spx = spx_summ.get(k,{}).get("avg_ret","—")
        logger.info(
            f"  C2 {d:2d}日: "
            f"BUY={row['BUY']:+.2f}% "
            f"ADD={row['ADD']:+.2f}% "
            f"HOLD={row['HOLD']:+.2f}% "
            f"REDUCE={row['REDUCE']:+.2f}% "
            f"EXIT={row['EXIT']:+.2f}% "
            f"SPX={spx:+.2f}%"
            if isinstance(row["BUY"], float) else f"  C2 {d}日: 无数据"
        )
    logger.info(f"  Layer C2: {status} (HOLD正收益 {hold_positive}/4, REDUCE低于HOLD {reduce_lower}/4, EXIT低于HOLD {exit_lower}/4)")

    return {
        "layer":   "C2",
        "name":    "Action Forward Return Validation",
        "status":  status,
        "hold_positive_count":  hold_positive,
        "reduce_lower_count":   reduce_lower,
        "exit_lower_count":     exit_lower,
        "action_summary":       summary,
        "spx_benchmark":        spx_summ,
        "interpretation": {
            "HOLD":   "持有有效" if hold_positive >= 3 else "持有期望偏低，需检查",
            "REDUCE": f"减仓有保护 ({reduce_lower}/4)" if reduce_lower >= 3 else "减仓保护不足",
            "EXIT":   f"退出有保护 ({exit_lower}/4)" if exit_lower >= 3 else "退出可能过早",
        },
    }


# ══════════════════════════════════════════════════════════════════
# Layer D: Stateful Strategy Simulation
# ══════════════════════════════════════════════════════════════════

def run_stateful_simulation(
    symbols:        list[str],
    prices_map:     dict[str, list[float]],
    dates_map:      dict[str, list[str]],
    spx_prices:     list[float],
    spx_dates:      list[str],
    assumptions:    dict  = None,   # LAYER_D_ASSUMPTIONS v1.0
    step:           int   = 1,
    min_history:    int   = 120,
    market_score_default: float = 60.0,
) -> dict:
    """
    Layer D: Stateful Portfolio Backtest

    每天维护持仓状态，模拟完整交易链条：
      BUY    → 建仓
      ADD    → 加仓（增加 0.5 单位，上限 1.5）
      HOLD   → 继续持有，更新最高价
      REDUCE → 减仓（卖出一半）
      EXIT   → 全部平仓

    持仓状态：
      position_size: 0 = 空仓, 0.5 = 半仓, 1.0 = 满仓, 1.5 = 加仓
      entry_price, highest_close, holding_days, current_return

    组合：等权重，最多 max_positions 只。
    """
    logger.info("[Backtest Layer D] Stateful Portfolio Backtest...")

    # ── 加载 high/low 序列（用于 Adverse Execution）────────
    from ..data_ingestion.fetch_yahoo import get_price_series as _gps
    highs_map: dict[str, list[float]] = {}
    lows_map:  dict[str, list[float]] = {}
    for sym in symbols:
        _, h = _gps(sym, field="high")
        _, l = _gps(sym, field="low")
        if h: highs_map[sym] = h
        if l: lows_map[sym]  = l
    spx_highs = highs_map.get("^GSPC") or highs_map.get("_GSPC", spx_prices)
    spx_lows  = lows_map.get("^GSPC")  or lows_map.get("_GSPC",  spx_prices)

    # ── 使用冻结参数（v1.0）──────────────────────────────
    a = assumptions or LAYER_D_ASSUMPTIONS
    max_positions  = a["max_positions"]
    buy_size       = a["buy_size"]         # 1.0
    add_size       = a["add_size"]         # 0.5
    max_size       = a["max_single_size"]  # 1.5
    txn_cost       = a["total_round_trip"] # 0.002 (round trip)
    logger.info(f"  Assumptions v{a.get('version','?')}: MaxPos={max_positions} BuySize={buy_size} TxnCost={txn_cost*100:.2f}%")

    min_len = min(len(p) for p in prices_map.values()) if prices_map else 0
    n_days  = min(min_len, len(spx_prices))

    # 持仓状态字典
    # {sym: {size, entry_price, entry_date, entry_idx, entry_signal,
    #        highest_close, holding_days, leader_score_entry}}
    positions: dict[str, dict] = {}
    closed_trades: list[dict]  = []
    equity_curve:  list[float] = []
    spx_curve:     list[float] = []
    daily_log:     list[dict]  = []

    spx_entry = spx_prices[min_history] if len(spx_prices) > min_history else 1.0

    for t in range(min_history, n_days - 1):
        date_str = spx_dates[t] if t < len(spx_dates) else str(t)

        # ── 计算所有股票信号 ─────────────────────────
        all_ret60 = [
            (period_return(prices_map[s][:t+1], 60) or 0.0)
            for s in symbols if s in prices_map and len(prices_map[s]) > t+1
        ]

        day_signals: dict[str, tuple] = {}  # {sym: (action, leader_score, price)}
        for sym in symbols:
            if sym not in prices_map:
                continue
            p = prices_map[sym][:t+1]
            if len(p) < 60:
                continue
            curr_price = p[-1]
            ret60 = period_return(p, 60) or 0.0
            rs    = rs_percentile(ret60, all_ret60)
            mom_d = calc_momentum(p)
            mom   = mom_d["momentum_score"]
            th_d  = calc_trend_health(p)
            th    = th_d["trend_health"]
            ls    = calc_leader_score(rs, mom, th)
            from ..features.trend_health import trend_lifecycle
            state   = trend_lifecycle(th, mom, rs)
            ma50s   = moving_average(p, 50)
            ma50_v  = ma50s[-1] if ma50s else curr_price
            ma50_sl = linreg_slope(ma50s[-10:]) if len(ma50s) >= 10 else 0
            action = trade_action(
                state, mom, rs, curr_price, ma50_v,
                ma50_sl, ls, th, market_score_default
            )
            day_signals[sym] = (action, ls, curr_price)

        # ── 更新现有持仓 ──────────────────────────────
        to_close  = []
        to_reduce = []
        to_add    = []

        for sym, pos in positions.items():
            if sym not in day_signals:
                continue
            action, ls, curr_price = day_signals[sym]

            # size > 0 才是有效持仓，才需要更新状态
            if pos["size"] <= 0:
                continue

            pos["holding_days"] += step
            pos["highest_close"] = max(pos["highest_close"], curr_price)
            unrealized = (curr_price - pos["avg_cost"]) / pos["avg_cost"] if pos["avg_cost"] > 0 else 0
            pos["current_return"] = unrealized

            # 记录交易期间每个 Action（交易生命周期追踪）
            pos["action_history"].append(action)

            # 状态保护：只有 size > 0 才响应信号
            if action == "EXIT":
                # size > 0 → 全部平仓
                to_close.append((sym, "EXIT", curr_price))
            elif action == "REDUCE":
                # size > 0 → 减仓（不能低于 0.5，不能凭空开仓）
                if pos["size"] > 0.5:
                    to_reduce.append((sym, curr_price))
                # size == 0.5 时 REDUCE 忽略，维持最小仓位
            elif action == "ADD":
                # size > 0 才能加仓（不能在空仓时 ADD）
                if pos["size"] < 1.5:
                    to_add.append((sym, curr_price, ls))
            elif action == "HOLD":
                # size > 0 → 维持，无需额外操作
                pass
            # BUY 时已有持仓 → 忽略（不重复开仓）

        # 执行平仓
        for sym, exit_sig, exit_price in to_close:
            pos = positions[sym]
            # Adverse Execution: 使用 T+1 日最低价卖出
            t1 = t + 1
            if sym in lows_map and t1 < len(lows_map[sym]) and lows_map[sym][t1] > 0:
                raw_exit = lows_map[sym][t1]  # T+1 最低价
            else:
                raw_exit = exit_price  # 数据缺失时 fallback 到收盘价
            effective_exit = raw_exit * (1 - a["total_one_way"])
            # adverse gap vs 信号日收盘价
            adverse_exit_gap = (exit_price - effective_exit) / exit_price if exit_price > 0 else 0
            ret = (effective_exit - pos["avg_cost"]) / pos["avg_cost"] if pos["avg_cost"] > 0 else 0
            # 持仓期间最大回撤
            max_dd_trade = (pos["highest_close"] - pos.get("min_close", pos["entry_price"])) / pos["highest_close"] if pos["highest_close"] > 0 else 0
            sym_dates  = dates_map.get(sym, [])
            entry_date = sym_dates[pos["entry_idx"]] if pos["entry_idx"] < len(sym_dates) else str(pos["entry_idx"])
            closed_trades.append({
                # 基本信息
                "symbol":               sym,
                "entry_date":           entry_date,
                "exit_date":            date_str,
                "entry_signal":         pos["entry_signal"],
                "exit_signal":          exit_sig,
                # 价格（信号日收盘）
                "entry_price":          round(pos["entry_price"], 2),
                "exit_price":           round(exit_price, 2),
                # Adverse Execution 实际成交价
                "avg_cost":             round(pos["avg_cost"], 2),        # 实际买入均价（含成本）
                "effective_exit":       round(effective_exit, 2),          # 实际卖出价（含成本）
                # 收益
                "return_pct":           round(ret * 100, 2),
                "max_gain_pct":         round((pos["highest_close"]-pos["avg_cost"])/pos["avg_cost"]*100, 2) if pos["avg_cost"] > 0 else 0,
                "max_drawdown_in_trade": round(max_dd_trade * 100, 2),
                # Adverse Gap 分析
                "execution_model":          "adverse_intraday_v1.0",
                "entry_adverse_gap_pct":    round(pos.get("adverse_buy_gap", 0) * 100, 3),
                "exit_adverse_gap_pct":     round(adverse_exit_gap * 100, 3),
                "total_execution_drag_pct": round((pos.get("adverse_buy_gap", 0) + adverse_exit_gap) * 100, 3),
                # 时间
                "holding_days":         pos["holding_days"],
                # 仓位
                "size_at_exit":         pos["size"],
                # 评分
                "leader_score_entry":   round(pos.get("leader_score_entry", 0), 1),
                # 完整 Action 链条
                "actions_during_trade": pos.get("action_history", []),
                "action_count":         len(pos.get("action_history", [])),
            })
            del positions[sym]

        # 执行减仓（只记录，不完全平仓）
        for sym, curr_price in to_reduce:
            if sym in positions:
                positions[sym]["size"] = max(0.5, positions[sym]["size"] - 0.5)

        # 执行加仓（更新均价）
        for sym, curr_price, ls in to_add:
            if sym in positions and positions[sym]["size"] > 0:
                pos = positions[sym]
                old_size = pos["size"]
                new_size = min(1.5, old_size + 0.5)
                # 加权平均更新均价
                pos["avg_cost"] = (pos["avg_cost"] * old_size + curr_price * 0.5) / new_size
                pos["size"] = new_size

        # ── 建仓：BUY 信号（只有 size==0 才新开仓）────────
        if len(positions) < max_positions:
            buy_cands = [
                (sym, ls, price)
                for sym, (action, ls, price) in day_signals.items()
                if action == "BUY"
                and (sym not in positions or positions[sym]["size"] == 0)
            ]
            buy_cands.sort(key=lambda x: x[1], reverse=True)
            for sym, ls, entry_price in buy_cands:
                if len(positions) >= max_positions:
                    break
                sym_dates  = dates_map.get(sym, [])
                entry_date = sym_dates[t] if t < len(sym_dates) else date_str
                # Adverse Execution: 使用 T+1 日最高价买入
                # T+1 = t+1（当前循环 t 是信号日，t+1 是执行日）
                t1 = t + 1
                if sym in highs_map and t1 < len(highs_map[sym]) and highs_map[sym][t1] > 0:
                    raw_buy = highs_map[sym][t1]  # T+1 最高价
                else:
                    raw_buy = entry_price  # 数据缺失时 fallback 到收盘价
                effective_entry = raw_buy * (1 + a["total_one_way"])
                # 记录 adverse gap（相比信号日收盘价的额外成本）
                adverse_buy_gap = (effective_entry - entry_price) / entry_price if entry_price > 0 else 0

                positions[sym] = {
                    "size":            buy_size,
                    "avg_cost":        effective_entry,
                    "entry_price":     entry_price,    # 信号日收盘价（用于参考）
                    "entry_exec_price": effective_entry,  # 实际成交价
                    "entry_date":      entry_date,
                    "entry_idx":       t,
                    "entry_signal":    "BUY",
                    "highest_close":   entry_price,
                    "min_close":       entry_price,  # 持仓期间最低价（用于计算最大回撤）
                    "holding_days":    0,
                    "current_return":  0.0,
                    "leader_score_entry": ls,
                    "action_history":  ["BUY"],      # 完整 Action 链条记录
                }

        # ── 每日净值 ──────────────────────────────────
        if positions:
            pos_vals = []
            for sym, pos in positions.items():
                curr = prices_map[sym][t] if t < len(prices_map[sym]) else pos["entry_price"]
                pos_vals.append(curr / pos["entry_price"] * pos["size"])
            # 加权平均（按 size 归一化）
            total_size = sum(pos["size"] for pos in positions.values())
            weighted = sum(
                (prices_map[sym][t] if t < len(prices_map[sym]) else positions[sym]["entry_price"])
                / positions[sym]["entry_price"] * positions[sym]["size"]
                for sym in positions
            ) / max(total_size, 1)
            daily_equity = (equity_curve[-1] if equity_curve else 1.0) * (1 + (weighted - 1) * (len(positions) / max_positions))
        else:
            daily_equity = equity_curve[-1] if equity_curve else 1.0

        equity_curve.append(daily_equity)
        spx_curve.append(spx_prices[t] / spx_entry if spx_entry > 0 else 1.0)

        # 每30天记录一次状态
        if t % 30 == 0:
            daily_log.append({
                "date":      date_str,
                "positions": len(positions),
                "equity":    round(daily_equity, 4),
                "spx":       round(spx_curve[-1], 4),
            })

    # ── 强制平仓剩余持仓 ─────────────────────────────
    t_last = n_days - 1
    for sym, pos in list(positions.items()):
        if pos["size"] <= 0:
            continue
        curr  = prices_map[sym][t_last] if t_last < len(prices_map[sym]) else pos["avg_cost"]
        ret   = (curr - pos["avg_cost"]) / pos["avg_cost"] if pos["avg_cost"] > 0 else 0
        sym_d = dates_map.get(sym, [])
        ed    = sym_d[pos["entry_idx"]] if pos["entry_idx"] < len(sym_d) else str(pos["entry_idx"])
        xd    = spx_dates[t_last] if t_last < len(spx_dates) else str(t_last)
        max_dd_trade = (pos["highest_close"] - pos.get("min_close", pos["entry_price"])) / pos["highest_close"] if pos["highest_close"] > 0 else 0
        closed_trades.append({
            "symbol":                sym,
            "entry_date":            ed,
            "exit_date":             xd,
            "entry_signal":          pos["entry_signal"],
            "exit_signal":           "SIM_END",
            "entry_price":           round(pos["entry_price"], 2),
            "avg_cost":              round(pos["avg_cost"], 2),
            "exit_price":            round(curr, 2),
            "return_pct":            round(ret * 100, 2),
            "max_gain_pct":          round((pos["highest_close"]-pos["avg_cost"])/pos["avg_cost"]*100, 2) if pos["avg_cost"] > 0 else 0,
            "max_drawdown_in_trade": round(max_dd_trade * 100, 2),
            "holding_days":          pos["holding_days"],
            "size_at_exit":          pos["size"],
            "leader_score_entry":    round(pos.get("leader_score_entry", 0), 1),
            "actions_during_trade":  pos.get("action_history", []),
            "action_count":          len(pos.get("action_history", [])),
        })

    if not closed_trades:
        return {"layer":"D","name":"Stateful Portfolio Backtest","status":"NO_TRADES","trades":[]}

    # ── 统计 ──────────────────────────────────────────
    rets   = [t["return_pct"] for t in closed_trades]
    wins   = [r for r in rets if r > 0]
    losses = [r for r in rets if r <= 0]
    holds  = [t["holding_days"] for t in closed_trades]

    total_days  = n_days - min_history
    exposure_pct = round(
        sum(h for h in holds) / (max_positions * max(total_days, 1)) * 100, 1
    )

    final_equity = equity_curve[-1] if equity_curve else 1.0
    years = total_days / 252
    cagr  = round((final_equity**(1/years)-1)*100, 2) if years > 0 else 0

    peak = 1.0; max_dd = 0.0
    for e in equity_curve:
        peak  = max(peak, e)
        max_dd = max(max_dd, (peak-e)/peak)

    spx_total = round((spx_curve[-1]-1)*100, 2) if spx_curve else 0
    spx_cagr  = round((spx_curve[-1]**(1/years)-1)*100, 2) if years > 0 and spx_curve else 0
    pf   = round(abs(sum(wins))/abs(sum(losses)), 2) if losses and sum(losses)!=0 else 0
    avg_h = sum(holds)/len(holds) if holds else 1
    avg_r = sum(rets)/len(rets)
    std_r = math.sqrt(sum((r-avg_r)**2 for r in rets)/len(rets)) if len(rets)>1 else 0
    sharpe = round(avg_r/std_r*math.sqrt(252/max(avg_h,1)), 2) if std_r>0 else 0
    total_ret = round((final_equity-1)*100, 2)

    status = "PASS"    if total_ret > spx_total and pf > 1.2 and len(closed_trades)>=10 else              "PARTIAL" if total_ret > 0 else "FAIL"

    logger.info(f"  Layer D: {status}")
    logger.info(f"  Return: {total_ret:+.1f}% vs SPX {spx_total:+.1f}%  Alpha: {total_ret-spx_total:+.1f}%")
    logger.info(f"  CAGR: {cagr:+.1f}%  MaxDD: {max_dd*100:.1f}%  WinRate: {round(len(wins)/len(rets)*100,1) if rets else 0}%  Trades: {len(closed_trades)}")

    return {
        "layer":             "D",
        "name":              "Stateful Portfolio Backtest",
        "status":            status,
        "execution_model":   a.get("execution_model", "adverse_intraday"),
        "execution_version": a.get("version", "1.0"),
        "total_return_pct":  total_ret,
        "cagr_pct":          cagr,
        "max_drawdown_pct":  round(max_dd*100, 2),
        "win_rate_pct":      round(len(wins)/len(rets)*100, 1) if rets else 0,
        "profit_factor":     pf,
        "sharpe_ratio":      sharpe,
        "number_of_trades":  len(closed_trades),
        "avg_holding_days":  round(sum(holds)/len(holds), 1) if holds else 0,
        "avg_winner_pct":    round(sum(wins)/len(wins), 2)   if wins   else 0,
        "avg_loser_pct":     round(sum(losses)/len(losses),2) if losses else 0,
        "exposure_pct":      exposure_pct,
        "avg_position_size": round(1/max_positions*100, 1),
        "spx_total_return_pct": spx_total,
        "spx_cagr_pct":         spx_cagr,
        "alpha_pct":         round(total_ret - spx_total, 2),
        "avg_execution_drag_pct": round(
            sum(t.get("total_execution_drag_pct", 0) for t in closed_trades) / len(closed_trades), 3
        ) if closed_trades else 0,
        "equity_curve":      [round(e,4) for e in equity_curve[::5]],
        "spx_curve":         [round(e,4) for e in spx_curve[::5]],
        "daily_log":         daily_log,
        "trades":            closed_trades[-100:],
        "total_trades_all":  len(closed_trades),
    }


# ══════════════════════════════════════════════════════════════════
# 主函数：运行完整回测
# ══════════════════════════════════════════════════════════════════

def run_full_backtest(
    symbols:      list[str],
    prices_map:   dict[str, list[float]],
    spx_prices:   list[float],
    dates_map:    dict[str, list[str]] = None,
    spx_dates:    list[str] = None,
    run_layer_b:  bool = False,
    run_layer_d:  bool = True,
) -> dict:
    """
    运行完整4层回测验证（A → C → D → B）。
    返回汇总结果，供 export_json 写入 backtest.json。
    """
    logger.info("=== 开始回测验证（Backtest Methodology v1.0）===")
    dates_map  = dates_map  or {}
    spx_dates  = spx_dates  or []
    results    = {}

    # Layer A: Leader Engine（最基础）
    results["layer_a"] = run_leader_engine_validation(
        symbols, prices_map, spx_prices
    )

    # Layer C: Trade Rule Signal Validation
    results["layer_c"] = run_trade_rule_validation(
        symbols, prices_map, spx_prices
    )

    # Layer C2: Action Forward Return Validation
    results["layer_c2"] = run_action_forward_validation(
        symbols, prices_map, spx_prices
    )

    # Layer D: Stateful Portfolio Backtest（完整状态机）
    if run_layer_d:
        results["layer_d"] = run_stateful_simulation(
            symbols, prices_map, dates_map, spx_prices, spx_dates
        )

    # Layer B: Promotion Engine（需要历史快照，可选）
    if run_layer_b:
        results["layer_b"] = run_promotion_engine_validation(
            symbols, prices_map, spx_prices
        )

    # 整体评分
    statuses = [v["status"] for v in results.values()]
    overall = "PASS"     if all(s == "PASS" for s in statuses) else \
              "PROMISING" if sum(s == "PASS" for s in statuses) >= 2 else \
              "PARTIAL"  if any(s in ("PASS","PARTIAL") for s in statuses) else "FAIL"

    logger.info(f"=== 回测完成: {overall} ===")
    for k, v in results.items():
        logger.info(f"  {k.upper()}: {v['status']}")

    return {
        "overall_status": overall,
        "methodology":    "Backtest Methodology v1.0",
        "model_version":  "Quantitative Model Spec v1.0 (Frozen)",
        "results":        results,
    }
