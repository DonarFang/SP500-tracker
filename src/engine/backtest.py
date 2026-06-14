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
from ..engine.trade_decision import trade_action, trade_action_reason
from ..utils import logger


# ══════════════════════════════════════════════════════════════════
# Layer D Frozen Assumptions (v1.6 RS95 / MinHold / Relative Stop comparison)
# docs/layer_d_assumptions.md
# ══════════════════════════════════════════════════════════════════
LAYER_D_ASSUMPTIONS = {
    "initial_capital":   100_000,
    "max_positions":      3,
    "buy_size":          1.0,    # Top3: 1/3 portfolio full position
    "add_size":          0.5,    # Top3: +1/6 portfolio, used only after REDUCE if allowed
    "max_single_size":   1.0,    # Top3 strategy: 1/3 max per position
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
    "strategy_variant":  "top3_entry_rs_minhold_relstop",
    "entry_top_n":       3,
    "rank_based_exit":   False,
    # Market Gate is disabled in this v1.6 diagnostic matrix so we can isolate
    # the impact of RS threshold, minimum holding period, and relative SPX stop.
    "market_gate_enabled": False,
    "risk_off_below_spx_ma50": False,
    "market_shock_gate_enabled": False,
    "market_shock_daily_return": -0.02,

    # Entry / holding / relative-risk controls tested by v1.6 variants.
    "entry_rs_min": 90.0,
    "min_holding_days": 0,
    "min_hold_allow_broken_exit": True,
    "relative_stop_enabled": False,
    "relative_stop_underperform_pct": -0.08,  # stock return - SPX return <= -8%
    "relative_stop_action": "REL_REDUCE",   # reduce 50%, once per position
    "relative_stop_once_per_position": True,

    # No fixed take-profit in v1.6. TP7-P is intentionally disabled/rejected.
    "partial_take_profit_enabled": False,
    "partial_take_profit_threshold": 0.07,
    "partial_take_profit_fraction": 0.50,
    "block_add_after_take_profit": False,
    "version":           "1.6-top3-rs95-minhold-relstop-comparison",
    "ls60_exit_mode":    "reduce",   # "exit"=旧规则 "reduce"=新规则（默认）
}


# ══════════════════════════════════════════════════════════════════
# 工具函数
# ══════════════════════════════════════════════════════════════════

def is_broken_trend(trend_state: str) -> bool:
    """
    判断趋势状态是否为 Broken。
    防御性实现：兼容 trend_lifecycle() 返回值的细微变化。
    """
    return str(trend_state).strip().lower() in {
        "broken",
        "broken trend",
        "breakdown",
    }

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
    # 用 SPX 长度作为时间轴，避免被个股短数据截断
    n_days = len(spx_prices)

    processed = 0
    for t in range(min_history, n_days - max(forward_days), step):
        # 计算该时间点所有股票的 Leader Score
        day_scores = {}
        for sym in symbols:
            if sym not in prices_map:
                continue
            info = _rebuild_leader_score(
                prices_map[sym], spx_prices,
                prices_map,  # 全量横截面（正式回测）
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

    # 用 SPX 长度作为时间轴，避免被个股短数据截断
    n_days = len(spx_prices)
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
    logger.info(f"  全市场 Action 分布(market_wide, 去重前): {signal_counts}")
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

    # 用 SPX 长度作为时间轴，避免被个股短数据截断
    n_days = len(spx_prices)
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
    dates_map:     dict[str, list[str]] | None = None,
    spx_dates:     list[str] | None = None,
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
    dates_map = dates_map or {}
    spx_dates = spx_dates or []
    action_returns = {
        a: {d: [] for d in forward_days}
        for a in ["BUY","ADD","HOLD","REDUCE","EXIT"]
    }
    spx_returns = {d: [] for d in forward_days}

    # 用 SPX 长度作为时间轴基准（不被个股短数据截断）
    # 个股在信号计算时独立检查是否有足够历史
    n_days = len(spx_prices)
    logger.info(f"  回测时间轴：{n_days} bars（基于 SPX）")
    if spx_dates:
        logger.info(f"  回测期间：{spx_dates[min_history] if len(spx_dates)>min_history else '?'} → {spx_dates[-1]}")

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
    ohlc_map:       dict = None,
    assumptions:    dict = None,
    step:           int  = 1,
    min_history:    int  = 120,
    market_score_default: float = 60.0,
) -> dict:
    """
    Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop

    修正项（相比 v3）：
    1. SPX master calendar — 时间轴以 SPX dates 为准
    2. Date-based alignment — 所有股票按日期查找，不用 index 直接对齐
    3. skipped_orders_by_reason — 跳过原因分类统计
    4. sample_validity 检查 — 样本不足时返回 INSUFFICIENT_SAMPLE
    """
    logger.info("[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop Backtest...")

    # ── 冻结参数 ─────────────────────────────────────────
    a        = assumptions or LAYER_D_ASSUMPTIONS
    max_pos  = a["max_positions"]
    buy_pct  = a["buy_size"]  / max_pos       # Top3: 1/3 per full slot
    add_pct  = a["add_size"]  / max_pos       # Top3: +1/6, only useful after REDUCE
    max_pct  = a["max_single_size"] / max_pos # Top3: max 1/3 per position
    one_way  = a["total_one_way"]             # 0.001
    init_cap = float(a.get("initial_capital", 100_000))
    strategy_variant = a.get("strategy_variant", "top3_entry_rs_minhold_relstop")
    entry_top_n = int(a.get("entry_top_n", 3))
    rank_based_exit = bool(a.get("rank_based_exit", False))
    market_gate_enabled = bool(a.get("market_gate_enabled", True))
    risk_off_below_spx_ma50 = bool(a.get("risk_off_below_spx_ma50", True))
    ls60_exit_mode = a.get("ls60_exit_mode", "reduce")  # "exit"=旧规则 "reduce"=新规则
    if ls60_exit_mode not in {"exit", "reduce"}:
        raise ValueError(f"Invalid ls60_exit_mode={ls60_exit_mode!r}; expected 'exit' or 'reduce'")
    market_shock_gate_enabled = bool(a.get("market_shock_gate_enabled", True))
    market_shock_daily_return = float(a.get("market_shock_daily_return", -0.02))
    take_profit_enabled = bool(a.get("partial_take_profit_enabled", False))
    take_profit_threshold = float(a.get("partial_take_profit_threshold", 0.07))
    take_profit_fraction = float(a.get("partial_take_profit_fraction", 0.50))
    block_add_after_take_profit = bool(a.get("block_add_after_take_profit", False))
    entry_rs_min = float(a.get("entry_rs_min", 90.0))
    min_holding_days = int(a.get("min_holding_days", 0))
    min_hold_allow_broken_exit = bool(a.get("min_hold_allow_broken_exit", True))
    relative_stop_enabled = bool(a.get("relative_stop_enabled", False))
    relative_stop_underperform = float(a.get("relative_stop_underperform_pct", -0.08))
    relative_stop_action = a.get("relative_stop_action", "REL_REDUCE")
    relative_stop_once = bool(a.get("relative_stop_once_per_position", True))
    market_gate_variant = (
        "D1_NO_MARKET_GATE" if not market_gate_enabled else
        "D2_RISK_OFF_GATE" if not market_shock_gate_enabled else
        "D3_RISK_OFF_PLUS_SHOCK_GATE"
    )

    logger.info(f"  v{a.get('version','?')} | Strategy={strategy_variant} "
                f"| EntryTopN={entry_top_n} | MaxPos={max_pos} "
                f"BuySlot={buy_pct*100:.1f}% MaxSingle={max_pct*100:.1f}% "
                f"OneWay={one_way*100:.2f}%")
    logger.info(f"  Market Gate Variant: {market_gate_variant}")
    logger.info(f"  Market Gate: enabled={market_gate_enabled} "
                f"| RiskOff=SPX<MA50:{risk_off_below_spx_ma50} "
                f"| Shock<={market_shock_daily_return*100:.1f}%:{market_shock_gate_enabled}")
    logger.info(f"  Entry filter: RS >= {entry_rs_min:.1f}; MinHold={min_holding_days}d; "
                f"RelStop={'ON' if relative_stop_enabled else 'OFF'} "
                f"({relative_stop_underperform*100:.1f}% vs SPX)")
    logger.info(f"  LS60 mode: {ls60_exit_mode} "
                f"({'LS<60 → EXIT' if ls60_exit_mode == 'exit' else 'LS<60 → REDUCE'})")
    logger.info(f"  ── Param check: ls60={ls60_exit_mode} rs={entry_rs_min} "
                f"top_n={entry_top_n} minhold={min_holding_days} "
                f"relstop={relative_stop_enabled} gate={market_gate_enabled} ──")
    logger.info(f"  Fixed TP: enabled={take_profit_enabled} "
                f"(v1.6 default OFF; TP7-P rejected for this matrix)")

    # ── 修正1: SPX master calendar ────────────────────────
    # 时间轴以 SPX dates 为准，不受个股短数据影响
    master_dates = spx_dates
    n_days       = len(spx_prices)
    sim_start_date = master_dates[min_history] if len(master_dates) > min_history else (master_dates[0] if master_dates else "?")
    sim_end_date   = master_dates[-2] if len(master_dates) >= 2 else (master_dates[-1] if master_dates else "?")
    logger.info(f"  时间轴: {master_dates[0] if master_dates else '?'} → {master_dates[-1] if master_dates else '?'} ({n_days} bars)")
    logger.info(f"  回测区间: {sim_start_date} → {sim_end_date}")

    # ── 修正2: Date-based lookup 索引 ─────────────────────
    # 为每只股票建立 date→index 映射，按日期对齐而非 array index
    date_idx: dict[str, dict[str, int]] = {}  # {sym: {date: idx}}
    for sym in symbols:
        sym_dates = dates_map.get(sym, [])
        date_idx[sym] = {d: i for i, d in enumerate(sym_dates)}

    # high/low 加载
    highs: dict[str, list[float]] = {}
    lows:  dict[str, list[float]] = {}
    highs_dates: dict[str, dict[str, int]] = {}
    lows_dates:  dict[str, dict[str, int]] = {}

    if ohlc_map:
        highs = {s: ohlc_map[s].get("high", []) for s in ohlc_map}
        lows  = {s: ohlc_map[s].get("low",  []) for s in ohlc_map}
    else:
        from ..data_ingestion.fetch_yahoo import get_price_series as _gps
        for sym in symbols:
            hd, h = _gps(sym, field="high")
            ld, l = _gps(sym, field="low")
            if h:
                highs[sym]       = h
                highs_dates[sym] = {d: i for i, d in enumerate(hd)}
            if l:
                lows[sym]        = l
                lows_dates[sym]  = {d: i for i, d in enumerate(ld)}

    def get_price_by_date(sym: str, date: str, field: str = "close") -> float:
        """按日期安全获取价格，不存在返回0。"""
        if field == "high":
            idx_map = highs_dates.get(sym, {})
            data    = highs.get(sym, [])
        elif field == "low":
            idx_map = lows_dates.get(sym, {})
            data    = lows.get(sym, [])
        else:
            idx_map = date_idx.get(sym, {})
            data    = prices_map.get(sym, [])
        i = idx_map.get(date, -1)
        if i < 0 or i >= len(data):
            return 0.0
        return data[i]

    def get_close_series_by_date(sym: str, up_to_date: str) -> list[float]:
        """获取某只股票截止 up_to_date 的历史收盘价序列（无前视）。"""
        idx_map  = date_idx.get(sym, {})
        data     = prices_map.get(sym, [])
        end_idx  = idx_map.get(up_to_date, -1)
        if end_idx < 0:
            # 找最近的日期
            dates_sorted = sorted(d for d in idx_map if d <= up_to_date)
            if not dates_sorted:
                return []
            end_idx = idx_map[dates_sorted[-1]]
        return data[:end_idx+1]

    # ── 组合状态 ─────────────────────────────────────────
    cash            = init_cap
    holdings: dict[str, dict] = {}
    pending_orders: list[dict] = []
    closed_trades:  list[dict] = []
    invalid_trades: list[str]  = []

    # 修正3: skipped_orders_by_reason
    skip_reasons = {
        "max_positions_reached":    0,
        "cash_insufficient":        0,
        "already_holding":          0,
        "max_single_size_reached":  0,
        "no_t1_price":              0,
        "invalid_execution_price":  0,
        "size_at_minimum":          0,
        "not_holding":              0,
        "not_in_entry_top_n":       0,
        "market_risk_off_block":    0,
        "market_shock_block":       0,
        "add_blocked_after_tp":     0,
        "entry_rs_below_threshold":        0,
        "min_hold_block":                  0,
        "ls60_reduce_already_triggered":   0,
    }
    orders_executed = 0

    # 持仓内 Action 分布（只统计实际持仓股的信号）
    portfolio_action_dist = {"HOLD": 0, "ADD": 0, "REDUCE": 0, "REL_REDUCE": 0, "EXIT": 0, "TP_REDUCE": 0}
    # 真实成交退出的原因分布
    executed_exit_reason_dist: dict[str, int] = {}
    # 真实成交减仓的原因分布
    executed_reduce_reason_dist: dict[str, int] = {}
    # 生成过的 EXIT/REDUCE pending signal 原因（含未成交）
    pending_signal_reason_dist: dict[str, int] = {}

    take_profit_stats = {
        "signals": 0,
        "executed": 0,
    }
    relative_stop_stats = {
        "signals": 0,
        "executed": 0,
    }
    market_gate_days = {
        "entry_allowed": 0,
        "risk_off": 0,
        "market_shock": 0,
        "blocked_total": 0,
    }

    equity_curve:  list[float] = []
    spx_curve:     list[float] = []
    daily_records: list[dict]  = []
    spx_entry = spx_prices[min_history] if len(spx_prices) > min_history else 1.0

    # ── 日循环（以 SPX master calendar 为准）────────────
    for t in range(min_history, n_days - 2):
        date_t  = master_dates[t]   if t   < len(master_dates) else None
        date_t1 = master_dates[t+1] if t+1 < len(master_dates) else None
        if not date_t or not date_t1:
            continue

        # ════════════════════════════════════════════════
        # STEP 1: 执行前一日 pending orders（T-1信号 → T日执行）
        # ════════════════════════════════════════════════
        for order in pending_orders:
            sym       = order["sym"]
            action    = order["action"]
            sig_date  = order["signal_date"]   # 信号日期
            exec_date = date_t                 # 执行日期 = 今天
            ls        = order["ls"]
            close_ref = order["close_t"]       # 信号日收盘（参考价）

            if action in ("BUY", "ADD"):
                # Adverse: 执行日最高价买入
                raw = get_price_by_date(sym, exec_date, "high")
                if raw <= 0:
                    raw = get_price_by_date(sym, exec_date, "close")
                if raw <= 0:
                    skip_reasons["no_t1_price"] += 1
                    continue
                exec_price = raw * (1 + one_way)

                port_val = cash + sum(
                    h["shares"] * h.get("current_close", h["avg_cost"])
                    for h in holdings.values()
                )

                if action == "BUY":
                    if sym in holdings:
                        skip_reasons["already_holding"] += 1
                        continue
                    if len(holdings) >= max_pos:
                        skip_reasons["max_positions_reached"] += 1
                        continue
                    target = port_val * buy_pct
                    if port_val > 0 and target / port_val > max_pct:
                        target = port_val * max_pct
                        skip_reasons["max_single_size_reached"] += 1
                    if target > cash:
                        if cash * 0.99 < 10:
                            skip_reasons["cash_insufficient"] += 1
                            continue
                        target = cash * 0.99

                    shares = target / exec_price
                    cash  -= shares * exec_price
                    orders_executed += 1
                    holdings[sym] = {
                        "shares":                shares,
                        "avg_cost":              exec_price,
                        "size_units":            1.0,
                        "entry_close_ref":       close_ref,
                        "entry_date":            exec_date,
                        "entry_sig_date":        sig_date,
                        "entry_signal":          "BUY",
                        "highest_close":         close_ref,
                        "min_close_since_entry": close_ref,
                        "current_close":         close_ref,
                        "leader_score_entry":    ls,
                        "entry_spx":             spx_prices[master_dates.index(exec_date)] if exec_date in master_dates else spx_close_t,
                        "relative_stop_triggered": False,
                        "relative_stop_signal_date": None,
                        "relative_stop_exec_date": None,
                        "take_profit_triggered": False,
                        "take_profit_signal_date": None,
                        "take_profit_exec_date": None,
                        "realized_pnl":          0.0,
                        "realized_cost_basis":   0.0,
                        "action_history":        ["BUY"],
                        "ls60_reduce_triggered": False,  # 方案A：LS<60 REDUCE 一次性保护
                    }

                elif action == "ADD":
                    if sym not in holdings:
                        skip_reasons["not_holding"] += 1
                        continue
                    h = holdings[sym]
                    if block_add_after_take_profit and h.get("take_profit_triggered"):
                        skip_reasons["add_blocked_after_tp"] += 1
                        continue
                    if h["size_units"] >= 1.5:
                        skip_reasons["max_single_size_reached"] += 1
                        continue
                    current_val = h["shares"] * exec_price
                    target_add  = port_val * add_pct
                    new_total   = current_val + target_add
                    if port_val > 0 and new_total / port_val > max_pct:
                        target_add = max(0, port_val * max_pct - current_val)
                    if target_add > cash:
                        if cash * 0.99 < 10:
                            skip_reasons["cash_insufficient"] += 1
                            continue
                        target_add = cash * 0.99
                    add_shares   = target_add / exec_price
                    old_c, old_s = h["avg_cost"], h["shares"]
                    h["avg_cost"]   = (old_s * old_c + add_shares * exec_price) / (old_s + add_shares)
                    h["shares"]    += add_shares
                    h["size_units"] = min(1.5, h["size_units"] + 0.5)
                    h["action_history"].append("ADD")
                    h["ls60_reduce_triggered"] = False  # ADD 后清零 ls60 保护
                    cash -= target_add
                    orders_executed += 1

            elif action in ("REDUCE", "REL_REDUCE", "TP_REDUCE", "EXIT"):
                if sym not in holdings:
                    skip_reasons["not_holding"] += 1
                    continue
                h = holdings[sym]
                raw = get_price_by_date(sym, exec_date, "low")
                if raw <= 0:
                    raw = get_price_by_date(sym, exec_date, "close")
                if raw <= 0:
                    skip_reasons["no_t1_price"] += 1
                    continue
                exec_price = raw * (1 - one_way)
                if exec_price <= 0:
                    skip_reasons["invalid_execution_price"] += 1
                    continue

                entry_date   = h["entry_date"]
                holding_days = sum(
                    1 for d in master_dates
                    if entry_date <= d <= exec_date
                )

                # P0: exit_date > entry_date
                if exec_date <= entry_date or holding_days <= 0:
                    invalid_trades.append(f"{sym}: exec {exec_date} <= entry {entry_date}")
                    continue

                if action == "EXIT":
                    proceeds = h["shares"] * exec_price
                    remaining_pnl = h["shares"] * (exec_price - h["avg_cost"])
                    total_pnl = h.get("realized_pnl", 0.0) + remaining_pnl
                    total_cost = h.get("realized_cost_basis", 0.0) + h["shares"] * h["avg_cost"]
                    ret = total_pnl / total_cost if total_cost > 0 else 0
                    cash    += proceeds
                    entry_gap = (h["avg_cost"] - h["entry_close_ref"]) / h["entry_close_ref"] if h["entry_close_ref"] > 0 else 0
                    exit_gap  = (h.get("current_close", exec_price) - exec_price) / max(h.get("current_close", exec_price), 0.01)
                    max_dd_t  = (h["highest_close"] - h.get("min_close_since_entry", h["avg_cost"])) / h["highest_close"] if h["highest_close"] > 0 else 0
                    orders_executed += 1
                    # 记录真实成交退出的原因（from pending order reason，T日冻结）
                    exec_primary_reason = order.get("primary_reason", "")
                    exec_reasons        = order.get("reasons", [])
                    executed_exit_reason_dist[exec_primary_reason] =                         executed_exit_reason_dist.get(exec_primary_reason, 0) + 1
                    closed_trades.append({
                        "symbol":               sym,
                        "entry_date":           entry_date,
                        "exit_date":            exec_date,
                        "entry_signal":         h["entry_signal"],
                        "exit_signal":          "EXIT",
                        "entry_price":          round(h["entry_close_ref"], 2),
                        "avg_cost":             round(h["avg_cost"], 2),
                        "exit_price":           round(h.get("current_close", exec_price), 2),
                        "effective_exit":       round(exec_price, 2),
                        "return_pct":           round(ret * 100, 2),
                        "max_gain_pct":         round((h["highest_close"]-h["avg_cost"])/h["avg_cost"]*100, 2) if h["avg_cost"] > 0 else 0,
                        "max_drawdown_in_trade": round(max_dd_t * 100, 2),
                        "holding_days":         holding_days,
                        "size_units_at_exit":   h["size_units"],
                        "leader_score_entry":   round(h.get("leader_score_entry", 0), 1),
                        "relative_stop_triggered": h.get("relative_stop_triggered", False),
                        "relative_stop_exec_date": h.get("relative_stop_exec_date"),
                        "take_profit_triggered": h.get("take_profit_triggered", False),
                        "take_profit_exec_date": h.get("take_profit_exec_date"),
                        "realized_pnl_before_exit": round(h.get("realized_pnl", 0.0), 2),
                        "actions_during_trade": h["action_history"],
                        "action_count":         len(h["action_history"]),
                        "execution_model":      "adverse_intraday_v1.0",
                        "entry_adverse_gap_pct": round(entry_gap * 100, 3),
                        "exit_adverse_gap_pct":  round(exit_gap * 100, 3),
                        "total_execution_drag_pct": round((entry_gap + exit_gap) * 100, 3),
                        "is_sim_end":           False,
                        "exit_reason":          exec_primary_reason,
                        "exit_reasons":         exec_reasons,
                    })
                    del holdings[sym]

                elif action in ("REDUCE", "REL_REDUCE", "TP_REDUCE"):
                    if h["size_units"] <= 0.5:
                        skip_reasons["size_at_minimum"] += 1
                        continue
                    sell_fraction = take_profit_fraction if action == "TP_REDUCE" else 0.50
                    sell_shares      = h["shares"] * sell_fraction
                    cash            += sell_shares * exec_price
                    h["shares"]     -= sell_shares
                    h["size_units"]  = max(0.5, h["size_units"] - 0.5)
                    h["realized_pnl"] = h.get("realized_pnl", 0.0) + sell_shares * (exec_price - h["avg_cost"])
                    h["realized_cost_basis"] = h.get("realized_cost_basis", 0.0) + sell_shares * h["avg_cost"]
                    h["action_history"].append(action)
                    if action == "TP_REDUCE":
                        h["take_profit_exec_date"] = exec_date
                        take_profit_stats["executed"] += 1
                    if action == "REL_REDUCE":
                        h["relative_stop_exec_date"] = exec_date
                        relative_stop_stats["executed"] += 1
                    # 记录 REDUCE 原因，并设置 ls60 一次性保护
                    reduce_primary = order.get("primary_reason", "")
                    if reduce_primary:
                        executed_reduce_reason_dist[reduce_primary] =                             executed_reduce_reason_dist.get(reduce_primary, 0) + 1
                    if reduce_primary == "leader_score_below_60":
                        h["ls60_reduce_triggered"] = True
                    orders_executed += 1

        # ════════════════════════════════════════════════
        # STEP 2: T 日盯市（mark-to-market at T close）
        # ════════════════════════════════════════════════
        position_value = 0.0
        for sym, h in holdings.items():
            close_t = get_price_by_date(sym, date_t, "close")
            if close_t > 0:
                h["current_close"]         = close_t
                h["highest_close"]         = max(h["highest_close"], close_t)
                h["min_close_since_entry"] = min(h.get("min_close_since_entry", close_t), close_t)
                position_value            += h["shares"] * close_t
            else:
                position_value += h["shares"] * h["avg_cost"]

        total_equity = cash + position_value

        # P0 guards
        if cash < -1.0:
            logger.warn(f"  {date_t}: negative cash={cash:.2f}")
            cash = 0.0
        if position_value > total_equity * 1.02:
            logger.warn(f"  {date_t}: leverage detected")

        equity_curve.append(total_equity)
        spx_curve.append(spx_prices[t] / spx_entry if spx_entry > 0 else 1.0)

        # ════════════════════════════════════════════════
        # STEP 3: 生成 T 日信号 → pending_orders for T+1
        # Strategy v1.6:
        #   Top 3 只限制“新 BUY 候选池”
        #   可选：提高入场 RS 阈值到 95
        #   可选：普通 REDUCE/EXIT 最短持仓 5 天
        #   可选：相对 SPX 跑输 8% 时减仓 50%
        #   不使用固定止盈；不因跌出 Top3 卖出
        # ════════════════════════════════════════════════
        spx_close_t = spx_prices[t]
        spx_ma50_t = sum(spx_prices[t-49:t+1]) / 50 if t >= 49 else spx_close_t
        spx_day_return = (
            (spx_prices[t] - spx_prices[t-1]) / spx_prices[t-1]
            if t > 0 and spx_prices[t-1] > 0 else 0.0
        )
        market_risk_off = (
            market_gate_enabled
            and risk_off_below_spx_ma50
            and spx_close_t < spx_ma50_t
        )
        market_shock = (
            market_gate_enabled
            and market_shock_gate_enabled
            and spx_day_return <= market_shock_daily_return
        )
        market_entry_allowed = not (market_risk_off or market_shock)

        if market_risk_off:
            market_gate_days["risk_off"] += 1
        if market_shock:
            market_gate_days["market_shock"] += 1
        if market_entry_allowed:
            market_gate_days["entry_allowed"] += 1
        else:
            market_gate_days["blocked_total"] += 1

        all_ret60 = []
        for s in symbols:
            p_s = get_close_series_by_date(s, date_t)
            if len(p_s) > 60:
                r = period_return(p_s, 60)
                if r is not None:
                    all_ret60.append(r)

        # 先重建全市场当日信号与 Leader Score，用于确定 Top 3 Entry Universe
        day_signals: dict[str, dict] = {}
        for sym in symbols:
            p = get_close_series_by_date(sym, date_t)
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

            action  = trade_action(
                state, mom, rs, close_t, ma50_v, ma50_sl,
                ls, th, market_score_default,
                ls60_exit_mode=ls60_exit_mode,
            )

            day_signals[sym] = {
                "action": action,
                "leader_score": ls,
                "close_t": close_t,
                "rs_score": rs,
                "momentum_score": mom,
                "trend_health": th,
                "trend_state": state,
            }

        # Top 3 Entry Universe:
        # 只限制新开仓 BUY；不限制已有持仓的 HOLD/ADD/REDUCE/EXIT
        top_ranked = sorted(
            ((s, v["leader_score"]) for s, v in day_signals.items()),
            key=lambda x: x[1],
            reverse=True
        )
        top_entry_symbols = set(s for s, _ in top_ranked[:entry_top_n])
        top_entry_rank = {s: i + 1 for i, (s, _) in enumerate(top_ranked[:entry_top_n])}

        management_orders = []
        buy_orders = []
        for sym, sig in day_signals.items():
            action  = sig["action"]
            ls      = sig["leader_score"]
            close_t = sig["close_t"]

            # 已持仓股票：记录每天动作；是否卖出/减仓只看 Trade Action，不看是否仍在 Top 3
            if sym in holdings:
                holdings[sym]["action_history"].append(action)
                # 持仓内 Action 分布统计
                if action in portfolio_action_dist:
                    portfolio_action_dist[action] += 1

            # 新 BUY：只有当日 Top 3 才允许进入
            if action == "BUY":
                if sym in holdings:
                    # 已持仓时 BUY 不重复开仓，不算错误
                    continue
                if sig.get("rs_score", 0.0) < entry_rs_min:
                    skip_reasons["entry_rs_below_threshold"] += 1
                    continue
                if sym not in top_entry_symbols:
                    skip_reasons["not_in_entry_top_n"] += 1
                    continue
                if not market_entry_allowed:
                    reason = "market_shock_block" if market_shock else "market_risk_off_block"
                    skip_reasons[reason] += 1
                    continue
                buy_orders.append({
                    "sym":         sym,
                    "action":      "BUY",
                    "signal_date": date_t,
                    "ls":          ls,
                    "close_t":     close_t,
                    "entry_rank":  top_entry_rank.get(sym),
                    "strategy":    strategy_variant,
                })
                continue

            # 已持仓股票的管理：ADD / REDUCE / EXIT 与 rank 无关
            if action in ("ADD", "REDUCE", "EXIT"):
                if sym not in holdings:
                    continue
                # Minimum holding period only blocks ordinary REDUCE/EXIT.
                # Broken trend can bypass if configured.
                if action in ("REDUCE", "EXIT") and min_holding_days > 0:
                    h = holdings[sym]
                    holding_days_so_far = sum(
                        1 for d in master_dates
                        if h.get("entry_date", date_t) <= d <= date_t
                    )
                    is_broken = is_broken_trend(sig.get("trend_state", ""))
                    if holding_days_so_far < min_holding_days and not (min_hold_allow_broken_exit and is_broken):
                        skip_reasons["min_hold_block"] += 1
                        continue
                if action == "ADD" and block_add_after_take_profit and holdings[sym].get("take_profit_triggered"):
                    skip_reasons["add_blocked_after_tp"] += 1
                    continue
                if action == "ADD" and not market_entry_allowed:
                    reason = "market_shock_block" if market_shock else "market_risk_off_block"
                    skip_reasons[reason] += 1
                    continue
                # 记录 reason（在 T 日信号生成时调用，不在 T+1 执行时重算）
                reason_info = trade_action_reason(
                    state, mom, rs, close_t, ma50_v, ma50_sl,
                    ls, th, market_score_default,
                    ls60_exit_mode=ls60_exit_mode,
                )
                if action in ("EXIT", "REDUCE"):
                    pr = reason_info.get("primary_reason", "")
                    pending_signal_reason_dist[pr] = pending_signal_reason_dist.get(pr, 0) + 1

                # 方案A：LS<60 REDUCE 一次性保护（STEP 3 过滤，避免每天重复减仓）
                if (action == "REDUCE"
                        and reason_info.get("primary_reason") == "leader_score_below_60"
                        and sym in holdings
                        and holdings[sym].get("ls60_reduce_triggered")):
                    skip_reasons["ls60_reduce_already_triggered"] += 1
                    continue

                management_orders.append({
                    "sym":           sym,
                    "action":        action,
                    "signal_date":   date_t,
                    "ls":            ls,
                    "close_t":       close_t,
                    "entry_rank":    top_entry_rank.get(sym),
                    "strategy":      strategy_variant,
                    "primary_reason": reason_info.get("primary_reason", ""),
                    "reasons":       reason_info.get("reasons", []),
                })

        # Relative SPX stop: if the holding underperforms SPX since entry
        # by more than the configured threshold, reduce 50% once per position.
        if relative_stop_enabled:
            scheduled_management = {o["sym"]: o["action"] for o in management_orders}
            for sym, h in holdings.items():
                if relative_stop_once and h.get("relative_stop_triggered"):
                    continue
                if h.get("size_units", 0.0) <= 0.5:
                    continue
                if scheduled_management.get(sym) in ("EXIT", "REDUCE", "REL_REDUCE"):
                    continue
                close_t = h.get("current_close", 0.0)
                stock_ret = (close_t - h["avg_cost"]) / h["avg_cost"] if h.get("avg_cost", 0) > 0 else 0.0
                spx_entry_h = h.get("entry_spx", spx_close_t)
                spx_ret = (spx_close_t - spx_entry_h) / spx_entry_h if spx_entry_h > 0 else 0.0
                relative_perf = stock_ret - spx_ret
                if relative_perf <= relative_stop_underperform:
                    h["relative_stop_triggered"] = True
                    h["relative_stop_signal_date"] = date_t
                    relative_stop_stats["signals"] += 1
                    management_orders.append({
                        "sym": sym,
                        "action": relative_stop_action,
                        "signal_date": date_t,
                        "ls": day_signals.get(sym, {}).get("leader_score", h.get("leader_score_entry", 0)),
                        "close_t": close_t,
                        "entry_rank": top_entry_rank.get(sym),
                        "strategy": strategy_variant,
                    })

        # TP7-P only applies when the stock-level rule did not already request
        # EXIT or REDUCE. It is independent of rank and market entry gates.
        if take_profit_enabled:
            scheduled_management = {o["sym"]: o["action"] for o in management_orders}
            for sym, h in holdings.items():
                if h.get("take_profit_triggered"):
                    continue
                if h.get("size_units", 0.0) <= 0.5:
                    continue
                if scheduled_management.get(sym) in ("EXIT", "REDUCE"):
                    continue
                close_t = h.get("current_close", 0.0)
                gain = (close_t - h["avg_cost"]) / h["avg_cost"] if h["avg_cost"] > 0 else 0.0
                if gain >= take_profit_threshold:
                    h["take_profit_triggered"] = True
                    h["take_profit_signal_date"] = date_t
                    take_profit_stats["signals"] += 1
                    management_orders = [
                        o for o in management_orders
                        if not (o["sym"] == sym and o["action"] == "ADD")
                    ]
                    management_orders.append({
                        "sym": sym,
                        "action": "TP_REDUCE",
                        "signal_date": date_t,
                        "ls": day_signals.get(sym, {}).get("leader_score", h.get("leader_score_entry", 0)),
                        "close_t": close_t,
                        "entry_rank": top_entry_rank.get(sym),
                        "strategy": strategy_variant,
                    })

        action_priority = {"EXIT": 0, "REDUCE": 1, "REL_REDUCE": 2, "TP_REDUCE": 3, "ADD": 4}
        management_orders.sort(key=lambda o: action_priority.get(o["action"], 9))
        buy_orders.sort(key=lambda o: o.get("entry_rank") or 999)
        pending_orders = management_orders + buy_orders

        if (t - min_history) % 20 == 0:
            gate_state = "ALLOW" if market_entry_allowed else (
                "SHOCK" if market_shock else "RISK_OFF"
            )
            logger.info(
                f"  Layer D market-gate: {t}/{n_days} {date_t} "
                f"gate={gate_state} SPXvsMA50={(spx_close_t/spx_ma50_t-1)*100:+.1f}% "
                f"day={spx_day_return*100:+.1f}% cash={cash:.0f} "
                f"holdings={len(holdings)} trades={len(closed_trades)}"
            )

        if t % 30 == 0:
            daily_records.append({
                "date":           date_t,
                "cash":           round(cash, 2),
                "position_value": round(position_value, 2),
                "total_equity":   round(total_equity, 2),
                "n_holdings":     len(holdings),
                "pending_orders": len(pending_orders),
                "market_gate_state": (
                    "ALLOW" if market_entry_allowed else
                    "SHOCK" if market_shock else "RISK_OFF"
                ),
                "spx_close":      round(spx_close_t, 2),
                "spx_ma50":       round(spx_ma50_t, 2),
                "spx_day_return_pct": round(spx_day_return * 100, 2),
            })

    # ════════════════════════════════════════════════════
    # 强制平仓剩余持仓
    # ════════════════════════════════════════════════════
    last_date = master_dates[-2] if len(master_dates) >= 2 else master_dates[-1]
    sim_end_count = 0
    for sym, h in list(holdings.items()):
        exec_price_raw = get_price_by_date(sym, last_date, "low")
        if exec_price_raw <= 0:
            exec_price_raw = get_price_by_date(sym, last_date, "close")
        if exec_price_raw <= 0:
            exec_price_raw = h["avg_cost"]
        exec_price = exec_price_raw * (1 - one_way)

        entry_date   = h["entry_date"]
        holding_days = sum(1 for d in master_dates if entry_date <= d <= last_date)

        if last_date <= entry_date or holding_days <= 0:
            invalid_trades.append(f"{sym}: SIM_END {last_date} <= entry {entry_date}")
            del holdings[sym]
            continue

        remaining_pnl = h["shares"] * (exec_price - h["avg_cost"])
        total_pnl = h.get("realized_pnl", 0.0) + remaining_pnl
        total_cost = h.get("realized_cost_basis", 0.0) + h["shares"] * h["avg_cost"]
        ret = total_pnl / total_cost if total_cost > 0 else 0
        cash    += h["shares"] * exec_price
        sim_end_count += 1
        closed_trades.append({
            "symbol":               sym,
            "entry_date":           entry_date,
            "exit_date":            last_date,
            "entry_signal":         h["entry_signal"],
            "exit_signal":          "SIM_END",
            "entry_price":          round(h["entry_close_ref"], 2),
            "avg_cost":             round(h["avg_cost"], 2),
            "exit_price":           round(h.get("current_close", exec_price), 2),
            "effective_exit":       round(exec_price, 2),
            "return_pct":           round(ret * 100, 2),
            "max_gain_pct":         round((h["highest_close"]-h["avg_cost"])/h["avg_cost"]*100, 2) if h["avg_cost"] > 0 else 0,
            "max_drawdown_in_trade": 0,
            "holding_days":         holding_days,
            "size_units_at_exit":   h["size_units"],
            "leader_score_entry":   round(h.get("leader_score_entry", 0), 1),
            "take_profit_triggered": h.get("take_profit_triggered", False),
            "take_profit_exec_date": h.get("take_profit_exec_date"),
            "realized_pnl_before_exit": round(h.get("realized_pnl", 0.0), 2),
            "actions_during_trade": h["action_history"],
            "action_count":         len(h["action_history"]),
            "execution_model":      "adverse_intraday_v1.0",
            "is_sim_end":           True,
        })
        del holdings[sym]

    # 修正3: 强制平仓后更新 final_equity
    final_equity = cash
    equity_curve.append(final_equity)

    # ════════════════════════════════════════════════════
    # 修正4: sample_validity 检查
    # ════════════════════════════════════════════════════
    simulation_days      = n_days - min_history
    completed_trades     = len([t for t in closed_trades if not t.get("is_sim_end")])
    total_trades         = len(closed_trades)
    sim_end_ratio        = sim_end_count / max(total_trades, 1)
    skip_total           = sum(skip_reasons.values())

    sample_valid = (
        simulation_days    >= 252 and
        total_trades       >= 20  and
        sim_end_ratio      <= 0.50 and
        len(invalid_trades) == 0
    )

    logger.info(f"  sim_days={simulation_days} trades={total_trades} "
                f"sim_end={sim_end_count}({sim_end_ratio*100:.0f}%) "
                f"exec={orders_executed} skip={skip_total}")

    if not sample_valid:
        reasons = []
        if simulation_days < 252:    reasons.append(f"sim_days={simulation_days}<252")
        if total_trades < 20:        reasons.append(f"trades={total_trades}<20")
        if sim_end_ratio > 0.50:     reasons.append(f"sim_end={sim_end_ratio*100:.0f}%>50%")
        if invalid_trades:           reasons.append(f"invalid={len(invalid_trades)}")
        logger.warn(f"  ⚠️  INSUFFICIENT_SAMPLE: {', '.join(reasons)}")

    if not closed_trades:
        return {
            "layer": "D", "name": "Stateful Portfolio Backtest",
            "status": "NO_TRADES", "skipped_orders_by_reason": skip_reasons,
        }

    # ════════════════════════════════════════════════════
    # 统计
    # ════════════════════════════════════════════════════
    total_return = (final_equity - init_cap) / init_cap * 100
    years        = simulation_days / 252
    cagr = ((final_equity / init_cap) ** (1/years) - 1) * 100 if years > 0 and final_equity > 0 else 0

    peak = equity_curve[0]; max_dd = 0.0
    for e in equity_curve:
        peak   = max(peak, e)
        max_dd = max(max_dd, (peak - e) / peak if peak > 0 else 0)

    rets   = [t["return_pct"] for t in closed_trades]
    wins   = [r for r in rets if r > 0]
    losses = [r for r in rets if r <= 0]
    holds  = [t["holding_days"] for t in closed_trades]
    pf     = round(abs(sum(wins)) / abs(sum(losses)), 2) if losses and sum(losses) != 0 else 0
    avg_h  = sum(holds) / len(holds) if holds else 1
    avg_r  = sum(rets)  / len(rets)
    std_r  = math.sqrt(sum((r-avg_r)**2 for r in rets)/len(rets)) if len(rets)>1 else 0
    sharpe = round(avg_r / std_r * math.sqrt(252/max(avg_h,1)), 2) if std_r > 0 else 0

    spx_total = round((spx_curve[-1]-1)*100, 2) if spx_curve else 0
    spx_cagr  = round((spx_curve[-1]**(1/years)-1)*100, 2) if years>0 and spx_curve else 0
    exposure  = round(sum(holds) / (max_pos * max(simulation_days, 1)) * 100, 1)

    reasonable = -99 < total_return < 10_000

    if not reasonable:
        status = "INVALID"
    elif not sample_valid:
        # 区分：不足样本但数字好 vs 不足样本且数字差
        if total_return > spx_total and pf >= 1.0 and max_dd * 100 <= 35:
            status = "PROMISING_INSUFFICIENT_SAMPLE"
        else:
            status = "INSUFFICIENT_SAMPLE"
    elif total_return > spx_total and pf > 1.2 and completed_trades >= 10:
        status = "PASS"
    elif total_return > 0:
        status = "PARTIAL"
    else:
        status = "FAIL"

    logger.info(f"  Market gate days: allowed={market_gate_days['entry_allowed']} "
                f"blocked={market_gate_days['blocked_total']} "
                f"risk_off={market_gate_days['risk_off']} "
                f"shock={market_gate_days['market_shock']}")
    logger.info(f"  Relative stop: signals={relative_stop_stats['signals']} "
                f"executed={relative_stop_stats['executed']}")
    logger.info(f"  Fixed TP: signals={take_profit_stats['signals']} "
                f"executed={take_profit_stats['executed']}")
    logger.info(f"  Layer D v1.6-top3-rs-minhold-relstop: {status}")
    logger.info(f"  ${init_cap:,.0f}→${final_equity:,.2f} ({total_return:+.2f}%) "
                f"SPX:{spx_total:+.2f}% Alpha:{total_return-spx_total:+.2f}%")
    logger.info(f"  CAGR:{cagr:+.2f}% MaxDD:{max_dd*100:.2f}% "
                f"WR:{round(len(wins)/len(rets)*100,1) if rets else 0}% "
                f"Trades:{total_trades}(SIM_END:{sim_end_count})")

    return {
        "layer":   "D",
        "name":    "Stateful Portfolio Backtest",
        "status":  status,
        "version": "v1.6-top3-rs-minhold-relstop",
        "execution_model": a.get("execution_model", "adverse_intraday"),
        "strategy_variant": strategy_variant,
        "entry_top_n": entry_top_n,
        "rank_based_exit": rank_based_exit,
        "strategy_controls": {
            "entry_rs_min": entry_rs_min,
            "ls60_exit_mode": ls60_exit_mode,
            "min_holding_days": min_holding_days,
            "min_hold_allow_broken_exit": min_hold_allow_broken_exit,
            "relative_stop_enabled": relative_stop_enabled,
            "relative_stop_underperform_pct": round(relative_stop_underperform * 100, 2),
            "relative_stop_action": relative_stop_action,
            "relative_stop_once_per_position": relative_stop_once,
            "relative_stop_stats": relative_stop_stats,
            "fixed_take_profit_enabled": take_profit_enabled,
        },
        "partial_take_profit": {
            "name": "TP7-P",
            "enabled": take_profit_enabled,
            "trigger_gain_pct": round(take_profit_threshold * 100, 2),
            "sell_fraction_pct": round(take_profit_fraction * 100, 1),
            "trigger_price": "signal-day close vs actual average cost",
            "execution": "T+1 adverse low minus one-way costs",
            "once_per_position": True,
            "block_add_after_trigger": block_add_after_take_profit,
            "stats": take_profit_stats,
            "note": "Partial reduction releases cash but does not free a Max3 symbol slot.",
        },
        "market_entry_gate": {
            "variant": market_gate_variant,
            "enabled": market_gate_enabled,
            "risk_off_rule": "SPX close < SPX MA50" if risk_off_below_spx_ma50 else "disabled",
            "market_shock_rule": (
                f"SPX daily return <= {market_shock_daily_return*100:.1f}%"
                if market_shock_gate_enabled else "disabled"
            ),
            "blocked_actions": ["BUY", "ADD"],
            "unaffected_actions": ["HOLD", "REDUCE", "EXIT"],
            "days": market_gate_days,
        },
        # 样本有效性（完整字段）
        "sample_validity": {
            "is_valid":            sample_valid,
            "sample_status":       status if status == "INSUFFICIENT_SAMPLE" else ("VALID" if sample_valid else "INSUFFICIENT"),
            "simulation_start_date": sim_start_date,
            "simulation_end_date":   sim_end_date,
            "simulation_days":     simulation_days,
            "total_trades":        total_trades,
            "completed_trades":    completed_trades,
            "sim_end_trades":      sim_end_count,
            "sim_end_ratio_pct":   round(sim_end_ratio * 100, 1),
            "invalid_trades":      len(invalid_trades),
            "minimum_required": {
                "sim_days":            252,
                "trades":              20,
                "sim_end_ratio_pct":   50,
                "invalid":             0,
            },
        },
        # skip 原因（直接在顶层也输出，方便快速查看）
        "skipped_orders_by_reason": skip_reasons,
        # 核心指标
        "initial_capital":   init_cap,
        "final_equity":      round(final_equity, 2),
        "total_return_pct":  round(total_return, 2),
        "cagr_pct":          round(cagr, 2),
        "max_drawdown_pct":  round(max_dd * 100, 2),
        "win_rate_pct":      round(len(wins)/len(rets)*100, 1) if rets else 0,
        "profit_factor":     pf,
        "sharpe_ratio":      sharpe,
        "number_of_trades":  total_trades,
        "avg_holding_days":  round(avg_h, 1),
        "avg_winner_pct":    round(sum(wins)/len(wins), 2)   if wins   else 0,
        "avg_loser_pct":     round(sum(losses)/len(losses),2) if losses else 0,
        "exposure_pct":      exposure,
        # SPX 基准
        "spx_total_return_pct": spx_total,
        "spx_cagr_pct":         spx_cagr,
        "alpha_pct":         round(total_return - spx_total, 2),
        # 订单统计
        "pending_orders_executed":  orders_executed,
        "pending_orders_skipped":   sum(skip_reasons.values()),
        # 持仓内 Action 分布（真实持仓股在持仓期间收到的信号）
        "portfolio_action_distribution":      portfolio_action_dist,
        # 真实成交退出的原因分布
        "executed_exit_reason_distribution":   executed_exit_reason_dist,
        "executed_reduce_reason_distribution": executed_reduce_reason_dist,
        # 所有生成过的 EXIT/REDUCE pending 信号原因（含未成交）
        "pending_signal_reason_distribution": pending_signal_reason_dist,
        # 执行损耗
        "avg_execution_drag_pct": round(
            sum(t.get("total_execution_drag_pct", 0) for t in closed_trades) / len(closed_trades), 3
        ) if closed_trades else 0,
        # P0
        "p0_passed":         len(invalid_trades) == 0 and reasonable,
        "invalid_trades_count": len(invalid_trades),
        "invalid_trades":    invalid_trades[:10],
        # 净值曲线
        "equity_curve":      [round(e, 2) for e in equity_curve[::5]],
        "spx_curve":         [round(e * init_cap, 2) for e in spx_curve[::5]],
        "daily_records":     daily_records,
        # 交易记录
        "trades":            closed_trades,
        "total_trades_all":  total_trades,
    }


def run_strategy_variant_comparison(
    symbols: list[str],
    prices_map: dict[str, list[float]],
    dates_map: dict[str, list[str]],
    spx_prices: list[float],
    spx_dates: list[str],
) -> dict:
    """
    Run four diagnostic portfolio variants using Strict Top3, no fixed TP.

    V0_BASE: current Strict Top3 baseline.
    V1_RS95: raise entry RS threshold from 90 to 95.
    V2_RS95_MINHOLD5: add minimum 5 trading-day hold for ordinary REDUCE/EXIT.
    V3_RS95_MINHOLD5_RELSTOP8: add relative SPX underperformance stop.

    Selection policy:
    1. Prefer PASS over PARTIAL over FAIL.
    2. Within the same status, prefer higher total return.
    3. Break ties with higher Profit Factor, higher Sharpe, then lower max drawdown.
    """
    logger.info("[Backtest Layer D v1.6] 3-Variant LS60 Mode Comparison...")

    base = {
        **LAYER_D_ASSUMPTIONS,
        "market_gate_enabled": False,
        "market_shock_gate_enabled": False,
        "partial_take_profit_enabled": False,
        "block_add_after_take_profit": False,
    }
    variants = {
        # V0: 旧规则基准 — LS<60 → EXIT
        "V0_OLD_LS60_EXIT": {
            **base,
            "strategy_variant": "V0_old_ls60_exit_rs90",
            "entry_rs_min":      90.0,
            "min_holding_days":  0,
            "relative_stop_enabled": False,
            "ls60_exit_mode":    "exit",    # ← 旧规则
            "version":           "V0-old-ls60-exit-rs90",
        },
        # V1: 新规则 — LS<60 → REDUCE
        "V1_NEW_LS60_REDUCE": {
            **base,
            "strategy_variant": "V1_new_ls60_reduce_rs90",
            "entry_rs_min":      90.0,
            "min_holding_days":  0,
            "relative_stop_enabled": False,
            "ls60_exit_mode":    "reduce",  # ← 新规则
            "version":           "V1-new-ls60-reduce-rs90",
        },
        # V2: 新规则 + RS95
        "V2_NEW_LS60_REDUCE_RS95": {
            **base,
            "strategy_variant": "V2_new_ls60_reduce_rs95",
            "entry_rs_min":      95.0,
            "min_holding_days":  0,
            "relative_stop_enabled": False,
            "ls60_exit_mode":    "reduce",  # ← 新规则
            "version":           "V2-new-ls60-reduce-rs95",
        },
    }

    variant_results = {}
    for variant_id, assumptions in variants.items():
        logger.info(f"  === Running {variant_id} ===")
        variant_results[variant_id] = run_stateful_simulation(
            symbols=symbols,
            prices_map=prices_map,
            dates_map=dates_map,
            spx_prices=spx_prices,
            spx_dates=spx_dates,
            assumptions=assumptions,
        )

    status_rank = {
        "PASS":                          5,
        "PARTIAL":                       4,
        "PROMISING_INSUFFICIENT_SAMPLE": 3,  # 数字好但样本不足 > 明确失败
        "FAIL":                          2,
        "INSUFFICIENT_SAMPLE":           1,
        "INVALID":                       0,
        "NO_TRADES":                     0,
    }

    def selection_key(item):
        _, result = item
        return (
            status_rank.get(result.get("status"), 0),
            result.get("alpha_pct", -10_000),          # 优先看 Alpha
            result.get("profit_factor", -10_000),
            result.get("total_return_pct", -10_000),
            result.get("sharpe_ratio", -10_000),
            -result.get("max_drawdown_pct", 10_000),
        )

    selected_id, selected_result = max(variant_results.items(), key=selection_key)
    comparison_rows = []
    for variant_id, result in variant_results.items():
        controls = result.get("strategy_controls", {})
        comparison_rows.append({
            "variant": variant_id,
            "selected": variant_id == selected_id,
            "status": result.get("status"),
            "entry_rs_min": controls.get("entry_rs_min"),
            "ls60_exit_mode": controls.get("ls60_exit_mode", "reduce"),
            "min_holding_days": controls.get("min_holding_days"),
            "relative_stop_enabled": controls.get("relative_stop_enabled"),
            "relative_stop_underperform_pct": controls.get("relative_stop_underperform_pct"),
            "total_return_pct": result.get("total_return_pct"),
            "alpha_pct": result.get("alpha_pct"),
            "cagr_pct": result.get("cagr_pct"),
            "max_drawdown_pct": result.get("max_drawdown_pct"),
            "win_rate_pct": result.get("win_rate_pct"),
            "profit_factor": result.get("profit_factor"),
            "sharpe_ratio": result.get("sharpe_ratio"),
            "number_of_trades": result.get("number_of_trades"),
            "avg_winner_pct": result.get("avg_winner_pct"),
            "avg_loser_pct": result.get("avg_loser_pct"),
            "exposure_pct": result.get("exposure_pct"),
            "skip_reasons": result.get("skipped_orders_by_reason", {}),
            "relative_stop_stats": controls.get("relative_stop_stats", {}),
        })

    logger.info("  === 3-Variant LS60 Mode Comparison ===")
    for row in comparison_rows:
        marker = "SELECTED" if row["selected"] else ""
        logger.info(
            f"  {row['variant']}: {row['status']} "
            f"LS60={row.get('ls60_exit_mode','?')} "
            f"RS>={row['entry_rs_min']} MinHold={row['min_holding_days']} "
            f"Return={row['total_return_pct']:+.2f}% "
            f"Alpha={row['alpha_pct']:+.2f}% "
            f"MaxDD={row['max_drawdown_pct']:.2f}% "
            f"PF={row['profit_factor']} Sharpe={row['sharpe_ratio']} {marker}"
        )
    logger.info(f"  Selected strategy variant: {selected_id}")

    # Preserve selected Layer D's top-level shape for current exporters/dashboard.
    return {
        **selected_result,
        "name": "3-Variant LS60 Mode Comparison",
        "version": "v1.6-ls60-mode-comparison",
        "selected_variant": selected_id,
        "selection_policy": (
            "status(PASS>PARTIAL>FAIL), then total return, "
            "then profit factor, then Sharpe, then lower max drawdown"
        ),
        "comparison": comparison_rows,
        "variant_results": variant_results,
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
        symbols=symbols,
        prices_map=prices_map,
        spx_prices=spx_prices,
        dates_map=dates_map,
        spx_dates=spx_dates,
    )

    # Layer D: 4-variant strategy comparison; selected result remains top-level compatible
    if run_layer_d:
        results["layer_d"] = run_strategy_variant_comparison(
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
              "PROMISING" if (sum(s == "PASS" for s in statuses) >= 2 or
                               sum(s == "PROMISING_INSUFFICIENT_SAMPLE" for s in statuses) >= 1) else \
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
