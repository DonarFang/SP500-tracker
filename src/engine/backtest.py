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
    ohlc_map:       dict[str, dict[str, list[float]]] = None,  # {sym: {high:[], low:[]}}
    assumptions:    dict  = None,
    step:           int   = 1,
    min_history:    int   = 120,
    market_score_default: float = 60.0,
) -> dict:
    """
    Layer D: Stateful Portfolio Backtest (v2 - corrected)

    正确实现：
    1. 每日盯市（mark-to-market）维护组合净值
    2. 现金账户追踪，无隐含杠杆
    3. 入场/出场使用 T+1 adverse execution
    4. P0 校验：日期合法性、无杠杆、净值每日更新
    """
    logger.info("[Backtest Layer D] Stateful Portfolio Backtest (v2)...")

    # ── 冻结参数 ─────────────────────────────────────────
    a             = assumptions or LAYER_D_ASSUMPTIONS
    max_positions = a["max_positions"]           # 10
    buy_pct       = a["buy_size"] / max_positions  # 10% of portfolio
    add_pct       = a["add_size"] / max_positions  # 5% of portfolio
    max_pct       = a["max_single_size"] / max_positions  # 15% of portfolio
    one_way_cost  = a["total_one_way"]           # 0.001 (cost+slippage)

    logger.info(f"  Assumptions v{a.get('version','?')}: "
                f"MaxPos={max_positions} BuyPct={buy_pct*100:.0f}% "
                f"AdverseCost={one_way_cost*100:.2f}% one-way")

    # ── 数据准备 ─────────────────────────────────────────
    # 加载 high/low（Adverse Execution 用）
    highs: dict[str, list[float]] = {}
    lows:  dict[str, list[float]] = {}
    if ohlc_map:
        highs = {s: ohlc_map[s]["high"] for s in ohlc_map if "high" in ohlc_map[s]}
        lows  = {s: ohlc_map[s]["low"]  for s in ohlc_map if "low"  in ohlc_map[s]}
    else:
        from ..data_ingestion.fetch_yahoo import get_price_series as _gps
        for sym in symbols:
            _, h = _gps(sym, field="high")
            _, l = _gps(sym, field="low")
            if h: highs[sym] = h
            if l: lows[sym]  = l

    min_len = min(len(p) for p in prices_map.values()) if prices_map else 0
    n_days  = min(min_len, len(spx_prices))

    # ── 组合状态 ─────────────────────────────────────────
    initial_capital = float(a.get("initial_capital", 100_000))
    cash     = initial_capital   # 现金
    holdings: dict[str, dict] = {}
    # holdings[sym] = {
    #   shares, avg_cost, entry_date, entry_idx, entry_signal,
    #   highest_close, min_close_since_entry, action_history
    # }
    closed_trades: list[dict] = []
    invalid_trades: list[str] = []

    # 每日净值记录
    daily_records: list[dict] = []
    equity_curve:  list[float] = []
    spx_curve:     list[float] = []
    spx_entry = spx_prices[min_history] if len(spx_prices) > min_history else 1.0

    # ── 日循环 ────────────────────────────────────────────
    for t in range(min_history, n_days - 2):  # -2 保证 T+1 有数据
        date_t   = spx_dates[t]   if t   < len(spx_dates) else str(t)
        date_t1  = spx_dates[t+1] if t+1 < len(spx_dates) else str(t+1)

        # ── 1. 计算所有股票的信号（基于 t 日收盘数据）──────
        all_ret60 = [
            (period_return(prices_map[s][:t+1], 60) or 0.0)
            for s in symbols if s in prices_map and len(prices_map[s]) > t+1
        ]

        day_signals: dict[str, tuple] = {}   # {sym: (action, leader_score, close_t)}
        for sym in symbols:
            if sym not in prices_map or len(prices_map[sym]) <= t:
                continue
            p = prices_map[sym][:t+1]
            if len(p) < 60:
                continue
            close_t = p[-1]
            ret60   = period_return(p, 60) or 0.0
            rs      = rs_percentile(ret60, all_ret60)
            mom_d   = calc_momentum(p)
            mom     = mom_d["momentum_score"]
            th_d    = calc_trend_health(p)
            th      = th_d["trend_health"]
            ls      = calc_leader_score(rs, mom, th)
            from ..features.trend_health import trend_lifecycle
            state   = trend_lifecycle(th, mom, rs)
            ma50s   = moving_average(p, 50)
            ma50_v  = ma50s[-1] if ma50s else close_t
            ma50_sl = linreg_slope(ma50s[-10:]) if len(ma50s) >= 10 else 0
            action  = trade_action(state, mom, rs, close_t, ma50_v, ma50_sl, ls, th, market_score_default)
            day_signals[sym] = (action, ls, close_t)

        # ── 2. 更新持仓状态（mark-to-market at close_t）───
        for sym in list(holdings.keys()):
            h = holdings[sym]
            if t < len(prices_map.get(sym, [])):
                close_t = prices_map[sym][t]
                h["highest_close"] = max(h["highest_close"], close_t)
                h["min_close_since_entry"] = min(h.get("min_close_since_entry", close_t), close_t)
                h["current_close"] = close_t
            if sym in day_signals:
                h["action_history"].append(day_signals[sym][0])

        # ── 3. 处理 EXIT / REDUCE（T+1 日最低价执行）──────
        for sym in list(holdings.keys()):
            if sym not in day_signals:
                continue
            action, ls, close_t = day_signals[sym]
            h = holdings[sym]
            t1 = t + 1

            # 取 T+1 最低价（Adverse: 最差卖出价）
            if sym in lows and t1 < len(lows[sym]) and lows[sym][t1] > 0:
                exec_low = lows[sym][t1]
            else:
                exec_low = prices_map[sym][t1] if t1 < len(prices_map[sym]) else close_t
            sell_price = exec_low * (1 - one_way_cost)

            if action == "EXIT":
                # Guard: execution_price > 0
                if sell_price <= 0:
                    logger.warn(f"  SKIP EXIT {sym}: invalid sell price {sell_price}")
                    continue

                # P0 校验：exit_date > entry_date
                entry_date = h["entry_date"]
                if date_t1 <= entry_date:
                    invalid_trades.append(f"{sym}: exit {date_t1} <= entry {entry_date}")
                    continue

                # 计算收益
                proceeds     = h["shares"] * sell_price
                cost_basis   = h["shares"] * h["avg_cost"]
                ret          = (sell_price - h["avg_cost"]) / h["avg_cost"] if h["avg_cost"] > 0 else 0
                holding_days = (t1 - h["entry_idx"])

                # P0 校验：holding_days > 0
                if holding_days <= 0:
                    invalid_trades.append(f"{sym}: holding_days={holding_days}")
                    continue

                # 归还现金
                cash += proceeds

                # adverse gap 分析
                close_ref = h.get("entry_close_ref", h["avg_cost"])
                entry_gap = (h["avg_cost"] - close_ref) / close_ref if close_ref > 0 else 0
                exit_gap  = (close_t - sell_price) / close_t if close_t > 0 else 0

                closed_trades.append({
                    "symbol":               sym,
                    "entry_date":           entry_date,
                    "exit_date":            date_t1,
                    "entry_signal":         h["entry_signal"],
                    "exit_signal":          "EXIT",
                    "entry_price":          round(h.get("entry_close_ref", h["avg_cost"]), 2),
                    "avg_cost":             round(h["avg_cost"], 2),
                    "exit_price":           round(close_t, 2),
                    "effective_exit":       round(sell_price, 2),
                    "return_pct":           round(ret * 100, 2),
                    "max_gain_pct":         round((h["highest_close"]-h["avg_cost"])/h["avg_cost"]*100, 2) if h["avg_cost"] > 0 else 0,
                    "max_drawdown_in_trade": round((h["highest_close"]-h.get("min_close_since_entry",h["avg_cost"]))/h["highest_close"]*100, 2) if h["highest_close"] > 0 else 0,
                    "holding_days":         holding_days,
                    "size_at_exit":         round(h["shares"] * h["avg_cost"] / initial_capital, 3),
                    "leader_score_entry":   round(h.get("leader_score_entry", 0), 1),
                    "actions_during_trade": h["action_history"],
                    "action_count":         len(h["action_history"]),
                    "execution_model":      "adverse_intraday_v1.0",
                    "entry_adverse_gap_pct": round(entry_gap * 100, 3),
                    "exit_adverse_gap_pct":  round(exit_gap * 100, 3),
                    "total_execution_drag_pct": round((entry_gap + exit_gap) * 100, 3),
                })
                del holdings[sym]

            elif action == "REDUCE":
                # Guard: execution_price > 0
                if sell_price <= 0:
                    logger.warn(f"  SKIP REDUCE {sym}: invalid sell price {sell_price}")
                    continue
                # 减仓一半（只有持仓大于最小值才减）
                portfolio_val = cash + sum(h2["shares"] * h2.get("current_close", h2["avg_cost"]) for h2 in holdings.values())
                current_pct   = h["shares"] * sell_price / portfolio_val if portfolio_val > 0 else 0
                if current_pct > max_pct / 2:
                    sell_shares = h["shares"] / 2
                    proceeds    = sell_shares * sell_price
                    # Guard: cash >= 0 (selling increases cash, always fine)
                    cash       += proceeds
                    h["shares"] -= sell_shares

        # ── 4. 处理 BUY（T+1 日最高价执行）──────────────
        n_holdings = len(holdings)
        if n_holdings < max_positions:
            buy_cands = sorted(
                [(sym, ls, close_t) for sym, (action, ls, close_t) in day_signals.items()
                 if action == "BUY" and sym not in holdings],
                key=lambda x: x[1], reverse=True
            )
            for sym, ls, close_t in buy_cands:
                if len(holdings) >= max_positions:
                    break

                # P0 校验：现金是否充足（无隐含杠杆）
                portfolio_val = cash + sum(
                    h2["shares"] * h2.get("current_close", h2["avg_cost"])
                    for h2 in holdings.values()
                )
                target_value = portfolio_val * buy_pct
                if cash < target_value:
                    # 现金不足，用现有现金的一部分
                    target_value = cash * 0.9
                if target_value < 100:
                    continue  # 资金太少，跳过

                # Adverse: T+1 最高价
                t1 = t + 1
                if sym in highs and t1 < len(highs[sym]) and highs[sym][t1] > 0:
                    exec_high = highs[sym][t1]
                else:
                    exec_high = prices_map[sym][t1] if t1 < len(prices_map[sym]) else close_t
                buy_price = exec_high * (1 + one_way_cost)

                # Guard 1: execution_price > 0
                if buy_price <= 0:
                    logger.warn(f"  SKIP BUY {sym}: invalid exec price {buy_price}")
                    continue

                shares = target_value / buy_price
                if shares <= 0:
                    continue

                cost = shares * buy_price

                # Guard 2: cash >= 0 after trade
                if cash - cost < 0:
                    # 用现有现金最大化买入
                    cost   = cash * 0.99
                    shares = cost / buy_price if buy_price > 0 else 0
                    if shares <= 0:
                        continue

                # Guard 3: open_positions_count <= max_positions (已在外层检查)

                # Guard 4: position_size <= max_single_size
                portfolio_est = cash + sum(
                    h2["shares"] * h2.get("current_close", h2["avg_cost"])
                    for h2 in holdings.values()
                )
                if portfolio_est > 0 and cost / portfolio_est > max_pct:
                    cost   = portfolio_est * max_pct
                    shares = cost / buy_price if buy_price > 0 else 0
                    if shares <= 0:
                        continue

                cash -= cost
                sym_dates = dates_map.get(sym, [])
                entry_date = date_t1  # 入场日期 = T+1（执行日）

                holdings[sym] = {
                    "shares":            shares,
                    "avg_cost":          buy_price,
                    "entry_close_ref":   close_t,  # 信号日收盘（用于 adverse gap 计算）
                    "entry_date":        entry_date,
                    "entry_idx":         t + 1,    # 执行日 index
                    "entry_signal":      "BUY",
                    "highest_close":     close_t,
                    "min_close_since_entry": close_t,
                    "current_close":     close_t,
                    "leader_score_entry": ls,
                    "action_history":    ["BUY"],
                }

        # ── 5. 每日盯市：计算组合总价值 ──────────────────
        position_value = sum(
            h["shares"] * (prices_map[sym][t] if t < len(prices_map.get(sym, [])) else h["avg_cost"])
            for sym, h in holdings.items()
        )
        total_equity = cash + position_value

        # P0 校验：无杠杆
        if position_value > total_equity * 1.01:  # 1% 容差
            logger.warn(f"  Day {t}: leverage detected! pos={position_value:.0f} equity={total_equity:.0f}")

        # P0 校验：cash >= 0
        if cash < -1.0:  # 允许 $1 浮点误差
            logger.warn(f"  Day {t}: negative cash detected! cash={cash:.2f}")
            cash = 0.0  # 强制归零，防止进一步错误

        equity_curve.append(total_equity)
        spx_curve.append(spx_prices[t] / spx_entry if spx_entry > 0 else 1.0)

        # 每30天记录一次
        if t % 30 == 0:
            daily_records.append({
                "date":           date_t,
                "cash":           round(cash, 2),
                "position_value": round(position_value, 2),
                "total_equity":   round(total_equity, 2),
                "n_holdings":     len(holdings),
                "spx_ref":        round(spx_curve[-1], 4),
            })

    # ── 强制平仓剩余持仓（模拟结束）─────────────────────
    t_last = n_days - 2  # -2 保证有 T+1
    date_end = spx_dates[t_last] if t_last < len(spx_dates) else str(t_last)
    for sym, h in list(holdings.items()):
        t1 = t_last + 1
        if sym in lows and t1 < len(lows[sym]) and lows[sym][t1] > 0:
            sell_price = lows[sym][t1] * (1 - one_way_cost)
        else:
            sell_price = prices_map[sym][t_last] if t_last < len(prices_map[sym]) else h["avg_cost"]
            sell_price *= (1 - one_way_cost)

        # P0 校验：日期合法性
        if date_end <= h["entry_date"]:
            invalid_trades.append(f"{sym}: SIM_END {date_end} <= entry {h['entry_date']}")
            del holdings[sym]
            continue

        ret = (sell_price - h["avg_cost"]) / h["avg_cost"] if h["avg_cost"] > 0 else 0
        proceeds = h["shares"] * sell_price
        cash += proceeds

        closed_trades.append({
            "symbol":              sym,
            "entry_date":          h["entry_date"],
            "exit_date":           date_end,
            "entry_signal":        h["entry_signal"],
            "exit_signal":         "SIM_END",
            "entry_price":         round(h.get("entry_close_ref", h["avg_cost"]), 2),
            "avg_cost":            round(h["avg_cost"], 2),
            "exit_price":          round(prices_map[sym][t_last] if t_last < len(prices_map[sym]) else h["avg_cost"], 2),
            "effective_exit":      round(sell_price, 2),
            "return_pct":          round(ret * 100, 2),
            "max_gain_pct":        round((h["highest_close"]-h["avg_cost"])/h["avg_cost"]*100, 2) if h["avg_cost"] > 0 else 0,
            "max_drawdown_in_trade": round((h["highest_close"]-h.get("min_close_since_entry",h["avg_cost"]))/h["highest_close"]*100, 2) if h["highest_close"] > 0 else 0,
            "holding_days":        t1 - h["entry_idx"],
            "size_at_exit":        round(h["shares"] * h["avg_cost"] / initial_capital, 3),
            "leader_score_entry":  round(h.get("leader_score_entry", 0), 1),
            "actions_during_trade": h["action_history"],
            "action_count":        len(h["action_history"]),
            "execution_model":     "adverse_intraday_v1.0",
        })
        del holdings[sym]

    # ── P0 校验汇总 ────────────────────────────────────
    if invalid_trades:
        logger.warn(f"  ⚠️  P0 校验发现 {len(invalid_trades)} 条无效交易记录：")
        for msg in invalid_trades[:5]:
            logger.warn(f"    {msg}")
        if len(invalid_trades) > len(closed_trades) * 0.1:
            logger.error("  ❌ 无效交易超过10%，Layer D 结果不可信")
            return {
                "layer": "D", "name": "Stateful Portfolio Backtest",
                "status": "INVALID",
                "reason": f"P0 validation failed: {len(invalid_trades)} invalid trades",
                "invalid_trades": invalid_trades[:10],
                "trades": [],
            }

    if not closed_trades:
        return {"layer":"D","name":"Stateful Portfolio Backtest","status":"NO_TRADES","trades":[]}

    # ── 统计 ──────────────────────────────────────────
    final_equity = equity_curve[-1] if equity_curve else initial_capital
    total_return = (final_equity - initial_capital) / initial_capital * 100
    years = (n_days - min_history) / 252
    cagr  = ((final_equity / initial_capital) ** (1/years) - 1) * 100 if years > 0 else 0

    # Max Drawdown（基于每日盯市净值）
    peak = equity_curve[0] if equity_curve else initial_capital
    max_dd = 0.0
    for e in equity_curve:
        peak  = max(peak, e)
        dd    = (peak - e) / peak if peak > 0 else 0
        max_dd = max(max_dd, dd)

    rets   = [t["return_pct"] for t in closed_trades]
    wins   = [r for r in rets if r > 0]
    losses = [r for r in rets if r <= 0]
    holds  = [t["holding_days"] for t in closed_trades]
    pf     = round(abs(sum(wins)) / abs(sum(losses)), 2) if losses and sum(losses) != 0 else 0
    avg_h  = sum(holds) / len(holds) if holds else 1
    avg_r  = sum(rets) / len(rets)
    std_r  = math.sqrt(sum((r-avg_r)**2 for r in rets)/len(rets)) if len(rets)>1 else 0
    sharpe = round(avg_r / std_r * math.sqrt(252/max(avg_h,1)), 2) if std_r > 0 else 0

    spx_total = round((spx_curve[-1]-1)*100, 2) if spx_curve else 0
    spx_cagr  = round((spx_curve[-1]**(1/years)-1)*100, 2) if years > 0 and spx_curve else 0

    total_days = n_days - min_history
    exposure   = round(sum(holds) / (max_positions * max(total_days, 1)) * 100, 1)

    # P0 校验：收益是否在合理范围
    reasonable = abs(total_return) < 50000  # 超过50000%就有问题
    status = "INVALID" if not reasonable or len(invalid_trades) > 0 else \
             "PASS"    if total_return > spx_total and pf > 1.2 and len(closed_trades) >= 5 else \
             "PARTIAL" if total_return > 0 else "FAIL"

    logger.info(f"  Layer D v2: {status}")
    logger.info(f"  Capital: ${initial_capital:,.0f} → ${final_equity:,.0f}")
    logger.info(f"  Total Return: {total_return:+.2f}%  SPX: {spx_total:+.2f}%  Alpha: {total_return-spx_total:+.2f}%")
    logger.info(f"  CAGR: {cagr:+.2f}%  MaxDD: {max_dd*100:.2f}%  WinRate: {round(len(wins)/len(rets)*100,1) if rets else 0}%")
    logger.info(f"  Trades: {len(closed_trades)}  AvgHold: {avg_h:.1f}d  Invalid: {len(invalid_trades)}")

    return {
        "layer":             "D",
        "name":              "Stateful Portfolio Backtest",
        "status":            status,
        "execution_model":   a.get("execution_model", "adverse_intraday"),
        "version":           a.get("version", "1.0"),
        # 核心指标
        "initial_capital":   initial_capital,
        "final_equity":      round(final_equity, 2),
        "total_return_pct":  round(total_return, 2),
        "cagr_pct":          round(cagr, 2),
        "max_drawdown_pct":  round(max_dd * 100, 2),
        "win_rate_pct":      round(len(wins)/len(rets)*100, 1) if rets else 0,
        "profit_factor":     pf,
        "sharpe_ratio":      sharpe,
        "number_of_trades":  len(closed_trades),
        "avg_holding_days":  round(avg_h, 1),
        "avg_winner_pct":    round(sum(wins)/len(wins), 2)   if wins   else 0,
        "avg_loser_pct":     round(sum(losses)/len(losses),2) if losses else 0,
        "exposure_pct":      exposure,
        # SPX 基准
        "spx_total_return_pct": spx_total,
        "spx_cagr_pct":         spx_cagr,
        "alpha_pct":         round(total_return - spx_total, 2),
        # 执行损耗
        "avg_execution_drag_pct": round(
            sum(t.get("total_execution_drag_pct", 0) for t in closed_trades) / len(closed_trades), 3
        ) if closed_trades else 0,
        # P0 校验
        "invalid_trades_count": len(invalid_trades),
        "p0_passed":         len(invalid_trades) == 0 and reasonable,
        # 净值曲线
        "equity_curve":      [round(e, 2) for e in equity_curve[::5]],
        "spx_curve":         [round(e*initial_capital, 2) for e in spx_curve[::5]],
        "daily_records":     daily_records,
        # 交易记录
        "trades":            closed_trades,
        "total_trades_all":  len(closed_trades),
        "invalid_trades":    invalid_trades[:20],
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
