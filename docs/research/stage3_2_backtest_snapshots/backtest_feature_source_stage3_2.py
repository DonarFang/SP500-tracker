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
import json
from pathlib import Path
from ..features.rs import period_return, rs_percentile
from ..features.momentum import (
    momentum_score as calc_momentum, moving_average, linreg_slope, momentum_acceleration
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

    # Qualified Candidate Pool（v1.7+）
    # candidate_top_n：Qualified Pool 内最多取 N 个候选（None = 用旧 entry_top_n 逻辑）
    # max_positions：组合最大持仓数
    # qualified_entry_enabled：是否启用资格过滤
    # qualified_states：允许的 trend_state
    "candidate_top_n":          None,    # None = 沿用旧 entry_top_n=3 逻辑
    "qualified_entry_enabled":  False,
    "qualified_rs_min":         90.0,
    "qualified_momentum_min":   85.0,
    "qualified_th_min":         75.0,
    "qualified_states":         ["Expansion"],
    "qualified_price_above_ma50": True,
    "qualified_ma50_slope_min":   0.0,
    "fill_only_enabled":          False,  # True = Qualified Pool 只补空仓，不替换持仓
    "gate_use_slope":             True,   # Gate v2: 是否使用 SPX MA50 slope 条件
    "gate_use_leadership":        True,   # Gate v2: 是否使用 NDX/SOX Leadership 条件
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
    sim_start_date: str  = None,  # 交易执行起始日（None=从 min_history 后开始）
    sim_end_date:   str  = None,  # 交易执行截止日（None=到末尾）
    ndx_prices:     list = None,  # NDX 收盘价（Gate v2 Leadership 判断）
    ndx_dates:      list = None,
    sox_prices:     list = None,  # SOX 收盘价
    sox_dates:      list = None,
    vix_prices:     list = None,  # VIX 收盘价
    vix_dates:      list = None,
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
    e1r_shell_mode = bool(a.get("e1r_shell_mode", False))
    e1r_regime_wiring_enabled = bool(a.get("e1r_regime_wiring_enabled", False))
    e1r_uptrend_execution_enabled = bool(a.get("e1r_uptrend_execution_enabled", False))
    e1r_regime_daily = a.get("e1r_regime_daily", {}) or {}

    def _e1r_regime_on(date: str) -> str:
        if not e1r_regime_wiring_enabled or not date:
            return "N/A"
        rec = e1r_regime_daily.get(date, {})
        if isinstance(rec, dict):
            return rec.get("regime") or rec.get("spx_regime") or rec.get("weekly_regime") or "UNCLASSIFIED"
        if isinstance(rec, str):
            return rec
        return "UNCLASSIFIED"

    def _e1r_mode_for_regime(regime: str) -> str:
        if regime == "UPTREND":
            return "UPTREND_EMERGING_CONFIRMED_ENABLED"
        if regime == "SIDEWAYS":
            return "SIDEWAYS_QUALITY_BREAKOUT_ONLY"
        if regime == "DOWNTREND":
            return "DOWNTREND_EXCEPTION_ONLY"
        if regime == "N/A":
            return "N/A"
        return "UNCLASSIFIED_NO_RISK_EXPANSION"

    def _e1r_risk_budget_for_regime(regime: str) -> dict:
        if regime == "UPTREND":
            return {"mode": "UPTREND_RISK_ON", "max_positions": 3, "max_total_exposure_pct": 100.0}
        if regime == "SIDEWAYS":
            return {"mode": "SIDEWAYS_LIMITED", "max_positions": 2, "max_total_exposure_pct": 33.3}
        if regime == "DOWNTREND":
            return {"mode": "DOWNTREND_DEFENSIVE", "max_positions": 1, "max_total_exposure_pct": 10.0}
        if regime == "N/A":
            return {"mode": "N/A", "max_positions": None, "max_total_exposure_pct": None}
        return {"mode": "UNCLASSIFIED_DEFENSIVE", "max_positions": 0, "max_total_exposure_pct": 0.0}

    def _e1r_dominant_regime(weights: dict) -> str:
        if not weights:
            return "UNCLASSIFIED" if e1r_regime_wiring_enabled else "N/A"
        return max(weights.items(), key=lambda kv: kv[1])[0]

    entry_top_n = int(a.get("entry_top_n", 3))
    rank_based_exit = bool(a.get("rank_based_exit", False))
    market_gate_enabled = bool(a.get("market_gate_enabled", True))
    risk_off_below_spx_ma50 = bool(a.get("risk_off_below_spx_ma50", True))
    ls60_exit_mode = a.get("ls60_exit_mode", "reduce")  # "exit"=旧规则 "reduce"=新规则

    # Qualified Candidate Pool 参数
    candidate_top_n           = a.get("candidate_top_n", None)   # None = 沿用旧 entry_top_n
    qualified_entry_enabled   = bool(a.get("qualified_entry_enabled", False))
    qualified_rs_min          = float(a.get("qualified_rs_min", 90.0))
    qualified_momentum_min    = float(a.get("qualified_momentum_min", 85.0))
    qualified_th_min          = float(a.get("qualified_th_min", 75.0))
    qualified_states          = set(a.get("qualified_states", ["Expansion"]))
    qualified_price_above_ma50 = bool(a.get("qualified_price_above_ma50", True))
    qualified_ma50_slope_min  = float(a.get("qualified_ma50_slope_min", 0.0))

    fill_only_enabled    = bool(a.get("fill_only_enabled", False))
    gate_use_slope       = bool(a.get("gate_use_slope", True))
    gate_use_leadership  = bool(a.get("gate_use_leadership", True))

    # ── 辅助指数 Lookup（日期 → 价格）─────────────────────────
    # 用于 Gate v2 市场状态判断；缺失日期使用最近一个有效值
    def _build_lookup(dates_list, prices_list):
        """建立 date_str → price 映射"""
        m = {}
        if dates_list and prices_list:
            for d, p in zip(dates_list, prices_list):
                m[d] = p
        return m

    ndx_lookup = _build_lookup(ndx_dates or [], ndx_prices or [])
    sox_lookup = _build_lookup(sox_dates or [], sox_prices or [])
    vix_lookup = _build_lookup(vix_dates or [], vix_prices or [])

    def _get_price_on(lookup, date, fallback=None):
        """获取 date 当天价格，缺失时返回 fallback"""
        return lookup.get(date, fallback)

    # SPX MA50 历史队列（用于 10日 slope 计算）
    from collections import deque
    spx_ma50_history = deque(maxlen=11)  # 存最近11个 MA50 值（今天+10天前）

    if qualified_entry_enabled:
        logger.info(f"  Qualified Pool: candidate_top_n={candidate_top_n} "
                    f"RS>={qualified_rs_min} Mom>={qualified_momentum_min} "
                    f"TH>={qualified_th_min} states={qualified_states} "
                    f"price>MA50={qualified_price_above_ma50} slope>={qualified_ma50_slope_min}")
    else:
        logger.info(f"  Entry mode: Strict Top{entry_top_n} (legacy)")
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
    # E2 Dynamic Exit parameters
    dynamic_exit_enabled   = bool(a.get("dynamic_exit_enabled", False))
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

    if qualified_entry_enabled:
        logger.info(f"  v{a.get('version','?')} | Strategy={strategy_variant} "
                    f"| CandidateTopN={candidate_top_n} MaxPos={max_pos} EntryMode=QualifiedPool "
                    f"BuySlot={buy_pct*100:.1f}% MaxSingle={max_pct*100:.1f}% "
                    f"OneWay={one_way*100:.2f}%")
    else:
        logger.info(f"  v{a.get('version','?')} | Strategy={strategy_variant} "
                    f"| EntryTopN={entry_top_n} MaxPos={max_pos} EntryMode=StrictTop3 "
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
    if dynamic_exit_enabled:
        logger.info(f"  Dynamic Exit v2: ON | Hard=Close<MA50+slope<0 | FULL_ON=needs structure | CAUTIOUS/CASH=LS<60 exits")
    logger.info(f"  Fixed TP: enabled={take_profit_enabled} "
                f"(v1.6 default OFF; TP7-P rejected for this matrix)")

    # ── 修正1: SPX master calendar ────────────────────────
    # 时间轴以 SPX dates 为准，不受个股短数据影响
    master_dates = spx_dates
    n_days       = len(spx_prices)

    logger.info(f"  时间轴: {master_dates[0] if master_dates else '?'} → {master_dates[-1] if master_dates else '?'} ({n_days} bars)")
    # 交易执行区间（不影响 warm-up 和指标计算，只控制交易时段）
    _trade_start = sim_start_date  # None = 从 min_history 后第一天
    _trade_end   = sim_end_date    # None = 到末尾
    _default_start = master_dates[min_history] if len(master_dates) > min_history else (master_dates[0] if master_dates else "?")
    _default_end   = master_dates[-2] if len(master_dates) >= 2 else (master_dates[-1] if master_dates else "?")
    logger.info(f"  时间轴: {master_dates[0] if master_dates else '?'} → {master_dates[-1] if master_dates else '?'} ({n_days} bars)")
    logger.info(f"  回测区间: {_trade_start or _default_start} → {_trade_end or _default_end}")

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
        "not_in_entry_top_n":               0,   # legacy: 旧 Strict Top3 模式
        "not_in_qualified_candidate_pool":  0,   # qualified: 不在候选池
        "not_qualified_entry":              0,   # qualified: 未通过资格过滤
        "qualified_candidate_generated":    0,   # qualified: 候选池 BUY 已生成

        "market_risk_off_block":    0,
        "market_shock_block":       0,
        "add_blocked_after_tp":     0,
        "entry_rs_below_threshold":        0,
        "min_hold_block":                  0,
        "dynamic_exit_warning":            0,  # E2: LS<60 但动态确认为 HOLD
        "dynamic_hard_exit_triggered":     0,  # E2: 硬退出触发次数
        "dynamic_soft_exit_confirmed":     0,  # E2: 软退出确认次数
        "ls60_reduce_already_triggered":   0,
        "action_reason_buy_add_mismatch":  0,   # BUY/ADD 不一致（记录，不中断）
        "fill_only_no_empty_slot":         0,   # fill_only 模式：无空仓位，跳过 BUY
        "e1r_legacy_buy_blocked":          0,   # E1-R execution: legacy BUY suppressed
        "e1r_no_capacity":                 0,   # E1-R execution: no available slot
        "e1r_candidate_buy_generated":     0,   # E1-R execution: candidate BUY generated
        "e1r_emerging_to_confirmed_add":   0,   # E1-R execution: upgrade ADD generated
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
    # Continuous observer-only daily equity records.
    # Read-only telemetry for regime/equity attribution.
    daily_equity_records: list[dict] = []
    daily_equity_peak = init_cap
    sim_end_liquidation_record = None
    # E1-R Phase 3A candidate tagging only.
    # These records are diagnostics; they must not affect orders or execution.
    e1r_candidate_records: list[dict] = []
    spx_entry = 0.0  # 在日循环中遇到第一个 sim 日时设置，保证与 Period 区间一致

    # ── Qualified Pool 诊断计数器 ───────────────────────────────
    qp_diag = {
        "pool_size_sum":        0,   # 每天候选池大小之和
        "pool_days":            0,   # 有交易信号的天数
        "days_pool_lt_3":       0,   # 候选池 < 3 的天数
        "days_pool_ge_10":      0,   # 候选池 >= 10 的天数
        "buy_orders_generated": 0,   # qualified_pool BUY 生成数
    }

    # ── 日循环（以 SPX master calendar 为准）────────────
    for t in range(min_history, n_days - 2):
        date_t  = master_dates[t]   if t   < len(master_dates) else None
        date_t1 = master_dates[t+1] if t+1 < len(master_dates) else None
        if not date_t or not date_t1:
            continue

        # ── 交易执行区间过滤 ────────────────────────────
        # master_dates 保持完整（指标计算不受影响）；
        # 只有在 [_trade_start, _trade_end] 区间内才执行交易和统计
        if _trade_start and date_t < _trade_start:
            pending_orders = []   # 不生成订单
            continue
        if _trade_end and date_t > _trade_end:
            break

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
                    _order_size_units = float(order.get("target_size_units", 1.0))
                    _order_size_units = max(0.0, min(_order_size_units, 1.0))
                    target = port_val * buy_pct * _order_size_units
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
                        "size_units":            _order_size_units,
                        "entry_close_ref":       close_ref,
                        "entry_date":            exec_date,
                        "entry_sig_date":        sig_date,
                        "entry_signal":          "BUY",
                        "e1r_entry_type":       order.get("e1r_entry_type"),
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
                        # E1-R Phase 2 regime wiring telemetry. Observer-only.
                        "entry_regime": _e1r_regime_on(exec_date),
                        "entry_type": order.get("e1r_entry_type") or ("E1R_PLACEHOLDER_LEGACY_ENTRY" if e1r_regime_wiring_enabled else None),
                        "regime_day_weights": {},
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
                    _add_size_units = float(order.get("add_size_units", 0.5))
                    _add_size_units = max(0.0, min(_add_size_units, 0.5))
                    target_add  = port_val * buy_pct * _add_size_units
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
                    h["size_units"] = min(1.0 if e1r_uptrend_execution_enabled else 1.5, h["size_units"] + _add_size_units)
                    if order.get("e1r_entry_type"):
                        h["e1r_entry_type"] = order.get("e1r_entry_type")
                        h["entry_type"] = order.get("e1r_entry_type")
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
                    # 此处不再需要 warn+reclassify 防御，因为上游已有 raise 检查
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
                        "entry_regime":         h.get("entry_regime", _e1r_regime_on(entry_date)),
                        "exit_regime":          _e1r_regime_on(exec_date),
                        "dominant_regime":      _e1r_dominant_regime(h.get("regime_day_weights", {})),
                        "entry_type":           h.get("entry_type"),
                        "regime_day_weights":   h.get("regime_day_weights", {}),
                        "exit_reason":          exec_primary_reason,
                        "exit_reasons":         exec_reasons,
                        "exit_type":            h.get("exit_type", "NORMAL_EXIT"),
                        "exit_warning_log":     h.get("exit_warning_log", []),
                        "exit_warning_count":   len(h.get("exit_warning_log", [])),
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

        if e1r_regime_wiring_enabled:
            _today_regime_for_positions = _e1r_regime_on(date_t)
            for _h in holdings.values():
                _weights = _h.setdefault("regime_day_weights", {})
                _weights[_today_regime_for_positions] = _weights.get(_today_regime_for_positions, 0) + 1

        total_equity = cash + position_value

        # P0 guards
        if cash < -1.0:
            logger.warn(f"  {date_t}: negative cash={cash:.2f}")
            cash = 0.0
        if position_value > total_equity * 1.02:
            logger.warn(f"  {date_t}: leverage detected")

        equity_curve.append(total_equity)
        # 第一个 sim 日时锁定 SPX 起点（保证每个 Period 独立基准）
        if spx_entry <= 0:
            spx_entry = spx_prices[t] if spx_prices[t] > 0 else 1.0
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

        # ── Gate v2：三档市场状态 ────────────────────────────────
        if not market_gate_enabled:
            # Gate 关闭：完全跳过，不执行任何 Gate v2 计算
            market_state     = "FULL_ON"
            entry_capacity   = max_pos
            market_risk_off  = False
            market_shock     = False
            market_entry_allowed = True
            market_gate_days["entry_allowed"] += 1
        else:
            # ── MA50 slope（10日变化率，使用完整历史索引，无 warm-up 问题）
            if t >= 59:  # t>=49（MA50）+ 10（slope 回溯）
                spx_ma50_t10 = sum(spx_prices[t-59:t-9]) / 50
                spx_ma50_slope = (spx_ma50_t / spx_ma50_t10) - 1.0 if spx_ma50_t10 > 0 else 0.0
            else:
                spx_ma50_slope = 0.0

            # ── NDX/SOX/VIX 当日价格
            _ndx_last = None
            _sox_last = None
            _vix_last = None
            _ndx_ma50 = None
            _sox_ma50 = None

            if ndx_lookup:
                _ndx_last = _get_price_on(ndx_lookup, date_t)
                if ndx_prices and len(ndx_prices) >= 50:
                    _ndx_idx = next((i for i, d in enumerate(ndx_dates or []) if d == date_t), None)
                    if _ndx_idx is not None and _ndx_idx >= 49:
                        _ndx_ma50 = sum(ndx_prices[_ndx_idx-49:_ndx_idx+1]) / 50

            if sox_lookup:
                _sox_last = _get_price_on(sox_lookup, date_t)
                if sox_prices and len(sox_prices) >= 50:
                    _sox_idx = next((i for i, d in enumerate(sox_dates or []) if d == date_t), None)
                    if _sox_idx is not None and _sox_idx >= 49:
                        _sox_ma50 = sum(sox_prices[_sox_idx-49:_sox_idx+1]) / 50

            if vix_lookup:
                _vix_last = _get_price_on(vix_lookup, date_t)

            # ── Leadership 计算
            _spx_above = spx_close_t > spx_ma50_t
            _ndx_above = (_ndx_last is not None and _ndx_ma50 is not None
                          and _ndx_last > _ndx_ma50) if ndx_lookup else None
            _sox_above = (_sox_last is not None and _sox_ma50 is not None
                          and _sox_last > _sox_ma50) if sox_lookup else None

            _n_indices = 1 + (1 if ndx_lookup else 0) + (1 if sox_lookup else 0)
            _leadership_count = sum([
                1 if _spx_above else 0,
                1 if (_ndx_above is True) else 0,
                1 if (_sox_above is True) else 0,
            ])
            _leadership_ratio = _leadership_count / _n_indices if _n_indices > 0 else 1.0
            # shock/VIX 受开关控制，不泄漏到未启用的 variant
            _shock_active = (
                market_shock_gate_enabled
                and spx_day_return <= market_shock_daily_return
            )
            _vix_active = (
                vix_lookup is not None and len(vix_lookup) > 0
                and (_vix_last or 0) >= 30
                # VIX 当前冻结禁用（所有 Gate v2.1 variant 均不传 VIX 数据）
            )

            # ── 三档状态判定（条件受开关控制）
            _slope_ok          = (spx_ma50_slope >= 0) if gate_use_slope else True
            _leadership_strong = (_leadership_ratio >= 1.0) if gate_use_leadership else True

            _cash_mode = (
                _vix_active
                or _shock_active
                or (gate_use_leadership and _leadership_ratio < 2/3)
                or (gate_use_slope and spx_ma50_slope < 0)
            )
            if _cash_mode:
                market_state   = "CASH_MODE"
                entry_capacity = 0
            elif (
                _spx_above
                and _slope_ok
                and _leadership_strong
                and not _shock_active
            ):
                market_state   = "FULL_ON"
                entry_capacity = max_pos
            else:
                market_state   = "CAUTIOUS_ON"
                entry_capacity = min(max_pos, 2)

            market_risk_off  = (market_state == "CASH_MODE") and not _shock_active
            market_shock     = _shock_active
            market_entry_allowed = entry_capacity > 0

            if market_risk_off:
                market_gate_days["risk_off"] += 1
            if market_shock:
                market_gate_days["market_shock"] += 1
            if market_entry_allowed:
                market_gate_days["entry_allowed"] += 1
            else:
                market_gate_days["blocked_total"] += 1

        # ── Continuous daily equity observer record ─────────────────────
        _prev_equity = (
            daily_equity_records[-1]["total_equity"]
            if daily_equity_records else init_cap
        )
        _daily_return_pct = (
            (total_equity / _prev_equity - 1) * 100
            if _prev_equity and _prev_equity > 0 else 0.0
        )
        daily_equity_peak = max(daily_equity_peak, total_equity)
        _drawdown_pct = (
            (daily_equity_peak - total_equity) / daily_equity_peak * 100
            if daily_equity_peak and daily_equity_peak > 0 else 0.0
        )
        _gate_state = (
            "ALLOW" if market_entry_allowed else
            "SHOCK" if market_shock else "RISK_OFF"
        )

        daily_equity_records.append({
            "date": date_t,
            "cash": round(cash, 2),
            "positions_value": round(position_value, 2),
            "total_equity": round(total_equity, 2),
            "daily_return_pct": round(_daily_return_pct, 4),
            "drawdown_pct": round(_drawdown_pct, 4),
            "exposure_pct": round(position_value / total_equity * 100, 2) if total_equity > 0 else 0.0,
            "open_positions_count": len(holdings),
            "pending_orders_count": len(pending_orders),
            "market_gate_state": _gate_state,
            "spx_regime": _e1r_regime_on(date_t) if e1r_regime_wiring_enabled else None,
            "e1r_active_mode": _e1r_mode_for_regime(_e1r_regime_on(date_t)) if e1r_regime_wiring_enabled else None,
            "risk_budget_mode": _e1r_risk_budget_for_regime(_e1r_regime_on(date_t))["mode"] if e1r_regime_wiring_enabled else None,
            "risk_budget": _e1r_risk_budget_for_regime(_e1r_regime_on(date_t)) if e1r_regime_wiring_enabled else None,
            "spx_close": round(spx_close_t, 2),
            "spx_ma50": round(spx_ma50_t, 2),
            "spx_day_return_pct": round(spx_day_return * 100, 4),
            "event": "EOD_MARK_TO_MARKET",
        })

        all_ret60 = []
        all_ret60_prev20 = []
        for s in symbols:
            p_s = get_close_series_by_date(s, date_t)
            if len(p_s) > 60:
                r = period_return(p_s, 60)
                if r is not None:
                    all_ret60.append(r)
            # E1-R Phase 3A: previous RS reference for Emerging Leader acceleration.
            # Uses data up to T-20 only; diagnostic-only, no execution impact.
            if e1r_shell_mode and len(p_s) > 80:
                r_prev = period_return(p_s[:-20], 60)
                if r_prev is not None:
                    all_ret60_prev20.append(r_prev)

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
            ma20s   = moving_average(p, 20)
            ma20_v  = ma20s[-1] if ma20s else close_t
            ma20_sl = linreg_slope(ma20s[-10:]) if len(ma20s) >= 10 else 0
            ma50s   = moving_average(p, 50)
            ma50_v  = ma50s[-1] if ma50s else close_t
            ma50_sl = linreg_slope(ma50s[-10:]) if len(ma50s) >= 10 else 0
            rs_prev20 = 50.0
            rs_20d_improvement = 0.0
            if e1r_shell_mode and len(p) > 80 and all_ret60_prev20:
                ret60_prev20 = period_return(p[:-20], 60)
                rs_prev20 = rs_percentile(ret60_prev20, all_ret60_prev20)
                rs_20d_improvement = round(rs - rs_prev20, 2)
            mom_acc = momentum_acceleration(p) if e1r_shell_mode else 0.0

            action  = trade_action(
                state, mom, rs, close_t, ma50_v, ma50_sl,
                ls, th, market_score_default,
                ls60_exit_mode=ls60_exit_mode,
            )

            day_signals[sym] = {
                "symbol":         sym,
                "action":         action,
                # 完整保存所有 trade_action_reason 所需字段，避免第二轮作用域污染
                "trend_state":    state,
                "momentum_score": mom,
                "rs_score":       rs,
                "leader_score":   ls,
                "trend_health":   th,
                "close_t":        close_t,
                "ma20":           ma20_v,
                "ma20_slope":     ma20_sl,
                "ma50":           ma50_v,
                "ma50_slope":     ma50_sl,
                # E1-R Phase 3A diagnostic fields.
                "rs_prev20":      rs_prev20,
                "rs_20d_improvement": rs_20d_improvement,
                "momentum_acceleration": mom_acc,
                "e1r_entry_type": None,
                "e1r_uptrend_emerging_eligible": False,
                "e1r_uptrend_confirmed_eligible": False,
                "e1r_entry_reason": [],
            }

        # ── Entry Universe ────────────────────────────────────────────
        # 只限制新开仓 BUY；不限制已有持仓的 HOLD/ADD/REDUCE/EXIT
        top_ranked = sorted(
            ((s, v["leader_score"]) for s, v in day_signals.items()),
            key=lambda x: x[1],
            reverse=True
        )

        # E1-R Phase 3A: UPTREND candidate tagging only.
        # This does not change buy_orders, management_orders, holdings, or cash.
        if e1r_shell_mode and e1r_regime_wiring_enabled and _e1r_regime_on(date_t) == "UPTREND":
            leader_rank_all = {s: i + 1 for i, (s, _) in enumerate(top_ranked)}
            for sym, sig in day_signals.items():
                rank_all = leader_rank_all.get(sym, 9999)
                emerging_reasons = []
                if sig["rs_score"] >= 80: emerging_reasons.append("rs_above_80")
                if sig.get("rs_20d_improvement", 0) >= 10: emerging_reasons.append("rs_20d_improvement_above_10")
                if sig["momentum_score"] >= 70: emerging_reasons.append("momentum_above_70")
                if sig.get("momentum_acceleration", 0) > 0: emerging_reasons.append("momentum_acceleration_positive")
                if sig["trend_health"] >= 65: emerging_reasons.append("trend_health_above_65")
                if sig["close_t"] > sig.get("ma20", sig["close_t"]): emerging_reasons.append("close_above_ma20")
                if sig.get("ma20_slope", 0) > 0 or sig.get("ma20", 0) > sig.get("ma50", 0): emerging_reasons.append("ma20_structure_positive")
                if rank_all <= 20: emerging_reasons.append("leader_rank_top20")

                emerging = (
                    sig["rs_score"] >= 80
                    and sig.get("rs_20d_improvement", 0) >= 10
                    and sig["momentum_score"] >= 70
                    and sig.get("momentum_acceleration", 0) > 0
                    and sig["trend_health"] >= 65
                    and sig["close_t"] > sig.get("ma20", sig["close_t"])
                    and (sig.get("ma20_slope", 0) > 0 or sig.get("ma20", 0) > sig.get("ma50", 0))
                    and rank_all <= 20
                )
                confirmed_reasons = []
                if sig["rs_score"] >= 90: confirmed_reasons.append("rs_above_90")
                if rank_all <= 5: confirmed_reasons.append("leader_rank_top5")
                if sig["leader_score"] >= 75: confirmed_reasons.append("leader_score_above_75")
                if sig["momentum_score"] >= 75: confirmed_reasons.append("momentum_above_75")
                if sig["trend_health"] >= 70: confirmed_reasons.append("trend_health_above_70")
                if sig["close_t"] > sig.get("ma50", sig["close_t"]): confirmed_reasons.append("close_above_ma50")
                if sig.get("ma50_slope", 0) >= 0: confirmed_reasons.append("ma50_slope_non_negative")
                confirmed = (
                    sig["rs_score"] >= 90
                    and rank_all <= 5
                    and sig["leader_score"] >= 75
                    and sig["momentum_score"] >= 75
                    and sig["trend_health"] >= 70
                    and sig["close_t"] > sig.get("ma50", sig["close_t"])
                    and sig.get("ma50_slope", 0) >= 0
                )
                if emerging or confirmed:
                    entry_type = "E1R_UPTREND_CONFIRMED" if confirmed else "E1R_UPTREND_EMERGING"
                    reasons = confirmed_reasons if confirmed else emerging_reasons
                    sig["e1r_entry_type"] = entry_type
                    sig["e1r_uptrend_emerging_eligible"] = emerging
                    sig["e1r_uptrend_confirmed_eligible"] = confirmed
                    sig["e1r_entry_reason"] = reasons
                    e1r_candidate_records.append({
                        "date": date_t,
                        "symbol": sym,
                        "spx_regime": "UPTREND",
                        "e1r_entry_type": entry_type,
                        "e1r_uptrend_emerging_eligible": emerging,
                        "e1r_uptrend_confirmed_eligible": confirmed,
                        "leader_rank": rank_all,
                        "leader_score": round(sig["leader_score"], 2),
                        "rs_score": round(sig["rs_score"], 2),
                        "rs_prev20": round(sig.get("rs_prev20", 0), 2),
                        "rs_20d_improvement": round(sig.get("rs_20d_improvement", 0), 2),
                        "momentum_score": round(sig["momentum_score"], 2),
                        "momentum_acceleration": round(sig.get("momentum_acceleration", 0), 2),
                        "trend_health": round(sig["trend_health"], 2),
                        "close": round(sig["close_t"], 2),
                        "ma20": round(sig.get("ma20", 0), 2),
                        "ma50": round(sig.get("ma50", 0), 2),
                        "ma20_slope": round(sig.get("ma20_slope", 0), 6),
                        "ma50_slope": round(sig.get("ma50_slope", 0), 6),
                        "reasons": reasons,
                        "diagnostic_only": True,
                    })

        # E1-R Phase 3B: UPTREND Execution v0.1 candidate selection.
        # Only entry execution is changed; existing E1 reduce/exit logic remains intact.
        e1r_selected_buy: dict | None = None
        if e1r_uptrend_execution_enabled and _e1r_regime_on(date_t) == "UPTREND":
            e1r_buy_candidates = []
            for s, v in day_signals.items():
                if s in holdings:
                    continue
                if not v.get("e1r_entry_type"):
                    continue
                _etype = v.get("e1r_entry_type")
                _priority = 0 if _etype == "E1R_UPTREND_CONFIRMED" else 1
                e1r_buy_candidates.append((
                    _priority,
                    leader_rank_all.get(s, 9999),
                    -v.get("leader_score", 0),
                    -v.get("momentum_acceleration", 0),
                    -v.get("rs_20d_improvement", 0),
                    s,
                    v,
                ))
            e1r_buy_candidates.sort()
            if e1r_buy_candidates and market_entry_allowed:
                if len(holdings) < min(max_pos, entry_capacity):
                    _, _, _, _, _, _sym, _sig = e1r_buy_candidates[0]
                    _etype = _sig.get("e1r_entry_type")
                    e1r_selected_buy = {
                        "sym": _sym,
                        "sig": _sig,
                        "entry_type": _etype,
                        "target_size_units": 1.0 if _etype == "E1R_UPTREND_CONFIRMED" else 0.5,
                    }
                else:
                    skip_reasons["e1r_no_capacity"] += len(e1r_buy_candidates)

        if qualified_entry_enabled and candidate_top_n is not None:
            # Qualified Candidate Pool 逻辑：
            # Step 1: 过滤资格条件
            qualified = []
            for s, v in day_signals.items():
                if v["rs_score"]       < qualified_rs_min:          continue
                if v["momentum_score"] < qualified_momentum_min:    continue
                if v["trend_health"]   < qualified_th_min:          continue
                if v["trend_state"]    not in qualified_states:     continue
                if qualified_price_above_ma50 and v["close_t"] <= v["ma50"]: continue
                if v["ma50_slope"]     < qualified_ma50_slope_min:  continue
                qualified.append((s, v["leader_score"]))
            # Step 2: Qualified Pool 内按 LS 排名，取前 candidate_top_n
            qualified.sort(key=lambda x: x[1], reverse=True)
            top_entry_symbols = set(s for s, _ in qualified[:candidate_top_n])
            top_entry_rank    = {s: i + 1 for i, (s, _) in enumerate(qualified[:candidate_top_n])}
            # 诊断：记录每日候选池大小
            pool_size = len(top_entry_symbols)
            qp_diag["pool_size_sum"]  += pool_size
            qp_diag["pool_days"]      += 1
            if pool_size < 3:  qp_diag["days_pool_lt_3"]  += 1
            if pool_size >= 10: qp_diag["days_pool_ge_10"] += 1
        else:
            # 旧逻辑：全市场 LS 排名取前 entry_top_n（Strict Top3）
            top_entry_symbols = set(s for s, _ in top_ranked[:entry_top_n])
            top_entry_rank    = {s: i + 1 for i, (s, _) in enumerate(top_ranked[:entry_top_n])}

        management_orders = []
        buy_orders = []
        for sym, sig in day_signals.items():
            # 从 sig 完整读取所有字段，严格避免跨 sym 的变量作用域污染
            action  = sig["action"]
            state   = sig["trend_state"]
            mom     = sig["momentum_score"]
            rs      = sig["rs_score"]
            ls      = sig["leader_score"]
            th      = sig["trend_health"]
            close_t = sig["close_t"]
            ma50_v  = sig["ma50"]
            ma50_sl = sig["ma50_slope"]

            # 已持仓股票：记录每天动作；是否卖出/减仓只看 Trade Action，不看是否仍在 Top 3
            if sym in holdings:
                holdings[sym]["action_history"].append(action)
                # 持仓内 Action 分布统计
                if action in portfolio_action_dist:
                    portfolio_action_dist[action] += 1

            # ── 新开仓逻辑 ────────────────────────────────────────
            # 职责拆分：
            #   Entry Engine  → 由 Qualified Pool 或旧 trade_action BUY 决定
            #   Position Mgmt → 由 trade_action 决定（HOLD/ADD/REDUCE/EXIT）
            if (
                e1r_uptrend_execution_enabled
                and e1r_selected_buy
                and sym == e1r_selected_buy["sym"]
                and sym not in holdings
            ):
                _etype = e1r_selected_buy["entry_type"]
                buy_orders.append({
                    "sym":            sym,
                    "action":         "BUY",
                    "signal_date":    date_t,
                    "ls":             ls,
                    "close_t":        close_t,
                    "entry_rank":     top_entry_rank.get(sym) or leader_rank_all.get(sym),
                    "strategy":       "E1R_UPTREND_EXECUTION_V0_1",
                    "entry_mode":     "e1r_uptrend_execution_v0_1",
                    "primary_reason": _etype,
                    "reasons":        sig.get("e1r_entry_reason", []),
                    "e1r_entry_type": _etype,
                    "target_size_units": e1r_selected_buy["target_size_units"],
                })
                skip_reasons["e1r_candidate_buy_generated"] += 1
                continue

            if qualified_entry_enabled:
                # Qualified Pool 模式：接管新开仓权限
                # 不使用 trade_action()=="BUY"，由候选池资格决定是否可开仓
                if sym in holdings:
                    # 已持仓：BUY 信号在 Qualified 模式下转为 ADD，由下方 position mgmt 处理
                    if action == "BUY":
                        action = "ADD"
                elif sym in top_entry_symbols:
                    # sym 在 Qualified Pool 候选里
                    # Fill-Only 检查：如果开启，只在有空仓位时才允许买入
                    if fill_only_enabled and len(holdings) >= entry_capacity:
                        skip_reasons["fill_only_no_empty_slot"] += 1
                        continue
                    # → 允许开仓（Gate 启用时才在 STEP 3 检查容量）
                    if market_gate_enabled and len(holdings) >= entry_capacity:
                        skip_reasons["gate_capacity_block"] = skip_reasons.get("gate_capacity_block", 0) + 1
                        continue
                    if not market_entry_allowed:
                        reason = "market_shock_block" if market_shock else "market_risk_off_block"
                        skip_reasons[reason] += 1
                        continue
                    qual_reasons = [
                        "qualified_pool_entry",
                        f"rs_above_{qualified_rs_min}",
                        f"mom_above_{qualified_momentum_min}",
                        f"th_above_{qualified_th_min}",
                        "trend_state_expansion",
                        "price_above_ma50",
                        "ma50_slope_non_negative",
                    ]
                    buy_orders.append({
                        "sym":            sym,
                        "action":         "BUY",    # 强制 BUY，不依赖 trade_action()
                        "signal_date":    date_t,
                        "ls":             ls,
                        "close_t":        close_t,
                        "entry_rank":     top_entry_rank.get(sym),
                        "strategy":       strategy_variant,
                        "entry_mode":     "qualified_pool",
                        "primary_reason": "qualified_pool_entry",
                        "reasons":        qual_reasons,
                        "candidate_top_n": candidate_top_n,
                    })
                    qp_diag["buy_orders_generated"] += 1
                    skip_reasons["qualified_candidate_generated"] += 1
                    continue
                # 如果 sym 不在 Qualified Pool 里，不生成 BUY 订单（跳过）
                elif action == "BUY":
                    skip_reasons["not_in_qualified_candidate_pool"] += 1

            else:
                # 旧模式：trade_action()=="BUY" + Strict TopN
                if action == "BUY":
                    if e1r_uptrend_execution_enabled:
                        skip_reasons["e1r_legacy_buy_blocked"] += 1
                        continue
                    if sym in holdings:
                        continue
                    if sig.get("rs_score", 0.0) < entry_rs_min:
                        skip_reasons["entry_rs_below_threshold"] += 1
                        continue
                    if sym not in top_entry_symbols:
                        skip_reasons["not_in_entry_top_n"] += 1
                        continue
                    # STEP 3 容量检查：只在 Gate 启用时才在信号生成层拦截
                    # Gate OFF 时依赖 STEP 1 执行层的 max_positions_reached 检查
                    if market_gate_enabled and len(holdings) >= entry_capacity:
                        skip_reasons["gate_capacity_block"] = skip_reasons.get("gate_capacity_block", 0) + 1
                        continue
                    if not market_entry_allowed:
                        reason = "market_shock_block" if market_shock else "market_risk_off_block"
                        skip_reasons[reason] += 1
                        continue
                    buy_orders.append({
                        "sym":            sym,
                        "action":         "BUY",
                        "signal_date":    date_t,
                        "ls":             ls,
                        "close_t":        close_t,
                        "entry_rank":     top_entry_rank.get(sym),
                        "strategy":       strategy_variant,
                        "entry_mode":     "legacy_trade_action",
                        "primary_reason": "all_entry_conditions_met",
                        "reasons":        ["all_entry_conditions_met"],
                    })
                    continue

            # 已持仓股票的管理：ADD / REDUCE / EXIT 与 rank 无关
            if action in ("ADD", "REDUCE", "EXIT"):
                if sym not in holdings:
                    continue
                # ── 退出层：MinHold（E1）或 Dynamic Exit（E2）──────────
                if action in ("REDUCE", "EXIT"):
                    h = holdings[sym]
                    holding_days_so_far = sum(
                        1 for d in master_dates
                        if h.get("entry_date", date_t) <= d <= date_t
                    )
                    stock_ma50  = sig.get("ma50",       close_t)
                    stock_slope = sig.get("ma50_slope",  0.0)
                    price_below_ma50   = close_t < stock_ma50
                    slope_negative     = stock_slope < 0

                    if dynamic_exit_enabled:
                        # ── E2 Dynamic Exit Confirmation v2 ──────────────
                        # 硬退出：Close<MA50 AND slope<0，不受市场状态影响
                        hard_exit = price_below_ma50 and slope_negative
                        if hard_exit:
                            action = "EXIT"
                            h["exit_type"] = "HARD_EXIT"
                            skip_reasons["dynamic_hard_exit_triggered"] = (
                                skip_reasons.get("dynamic_hard_exit_triggered", 0) + 1)
                        else:
                            ls_below_60 = ls < 60
                            if market_state == "FULL_ON":
                                # FULL_ON：LS<60 还需一项价格结构证据才退出
                                if ls_below_60 and not (price_below_ma50 or slope_negative):
                                    # EXIT_WARNING：记录预警，继续持有
                                    skip_reasons["dynamic_exit_warning"] += 1
                                    if "exit_warning_log" not in h:
                                        h["exit_warning_log"] = []
                                    last_warn = (h["exit_warning_log"][-1]["date"]
                                                 if h["exit_warning_log"] else None)
                                    prev_date = (master_dates[master_dates.index(date_t)-1]
                                                 if date_t in master_dates and
                                                 master_dates.index(date_t) > 0 else None)
                                    is_consecutive = (last_warn and last_warn == prev_date)
                                    if not is_consecutive:
                                        h["exit_warning_log"].append({
                                            "date": date_t,
                                            "ls": round(ls, 2),
                                            "price": round(close_t, 2),
                                            "ma50": round(stock_ma50, 2),
                                            "price_vs_ma50_pct": round(
                                                (close_t/stock_ma50-1)*100, 2)
                                                if stock_ma50 > 0 else 0,
                                            "ma50_slope": round(stock_slope, 4),
                                            "market_state": market_state,
                                            "warning_day": True,
                                        })
                                    else:
                                        h["exit_warning_log"][-1][
                                            "last_consecutive_date"] = date_t
                                    h["exit_warning"] = date_t
                                    continue  # EXIT_WARNING → HOLD
                                else:
                                    h["exit_type"] = "SOFT_EXIT_CONFIRMED"
                                    skip_reasons["dynamic_soft_exit_confirmed"] = (
                                        skip_reasons.get("dynamic_soft_exit_confirmed", 0) + 1)
                            else:
                                # CAUTIOUS_ON / CASH_MODE：LS<60 本身足以退出
                                if ls_below_60:
                                    h["exit_type"] = "SOFT_EXIT_CONFIRMED"
                                    skip_reasons["dynamic_soft_exit_confirmed"] = (
                                        skip_reasons.get("dynamic_soft_exit_confirmed", 0) + 1)
                                # LS>=60 时继续持有，不生成 warning
                    else:
                        # ── E1 MinHold（原逻辑）────────────────────────────
                        is_broken = is_broken_trend(sig.get("trend_state", ""))
                        if min_holding_days > 0 and holding_days_so_far < min_holding_days and not (min_hold_allow_broken_exit and is_broken):
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
                # 一致性检查：
                # REDUCE / EXIT mismatch → raise（风险动作必须准确）
                # BUY / ADD mismatch     → 仅计数，不中断（进攻类语义相近）
                reason_action = reason_info.get("action", "")
                if action != reason_action:
                    risk_actions = {"REDUCE", "EXIT"}
                    if {action, reason_action} & risk_actions:
                        raise RuntimeError(
                            f"action_reason_mismatch: {sym} "
                            f"sig_action={action} reason_action={reason_action} "
                            f"ls60_exit_mode={ls60_exit_mode} "
                            f"ls={ls:.1f} state={state} price={close_t:.2f} ma50={ma50_v:.2f}"
                        )
                    else:
                        skip_reasons["action_reason_buy_add_mismatch"] += 1
                # CAUTIOUS_ON/CASH_MODE 禁止 ADD（生成层拦截）
                if action == "ADD" and market_gate_enabled and market_state in ("CAUTIOUS_ON", "CASH_MODE"):
                    skip_reasons["gate_add_blocked"] = skip_reasons.get("gate_add_blocked", 0) + 1
                    continue

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

        # E1-R Phase 3B: Emerging → Confirmed upgrade ADD.
        # This is the only ADD behavior introduced in Phase 3B and it never overrides
        # existing EXIT/REDUCE management orders generated above.
        if e1r_uptrend_execution_enabled and _e1r_regime_on(date_t) == "UPTREND":
            scheduled_management = {o["sym"]: o["action"] for o in management_orders}
            for sym, h in holdings.items():
                if scheduled_management.get(sym) in ("EXIT", "REDUCE", "REL_REDUCE", "TP_REDUCE", "ADD"):
                    continue
                sig = day_signals.get(sym)
                if not sig or not sig.get("e1r_uptrend_confirmed_eligible"):
                    continue
                if h.get("e1r_entry_type") != "E1R_UPTREND_EMERGING":
                    continue
                if h.get("size_units", 0.0) >= 1.0:
                    continue
                close_t_h = h.get("current_close", 0.0)
                pos_ret = (close_t_h / h["avg_cost"] - 1.0) if h.get("avg_cost", 0) > 0 and close_t_h > 0 else 0.0
                if pos_ret <= 0.03:
                    continue
                if close_t_h <= sig.get("ma20", close_t_h):
                    continue
                if sig.get("momentum_acceleration", 0) < 0:
                    continue
                management_orders.append({
                    "sym": sym,
                    "action": "ADD",
                    "signal_date": date_t,
                    "ls": sig.get("leader_score", h.get("leader_score_entry", 0)),
                    "close_t": close_t_h,
                    "entry_rank": top_entry_rank.get(sym) or leader_rank_all.get(sym),
                    "strategy": "E1R_UPTREND_EXECUTION_V0_1",
                    "primary_reason": "emerging_upgraded_to_confirmed",
                    "reasons": ["emerging_upgraded_to_confirmed", "position_return_above_3pct", "close_above_ma20", "momentum_acceleration_non_negative"],
                    "e1r_entry_type": "E1R_UPTREND_CONFIRMED",
                    "add_size_units": 0.5,
                })
                skip_reasons["e1r_emerging_to_confirmed_add"] += 1

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
        # P0 Fix: 最后一个 sim 日（T日）不生成新 BUY/ADD
        # 因为 T+1 执行时会等于或超过 sim_end_date，导致 entry==exit invalid
        _next_date = master_dates[t+1] if t+1 < len(master_dates) else None
        # 最后一个或倒数第二个 sim 日不生成新 BUY（T+1 执行时会撞上 sim_end_date）
        _is_last_sim_day = (_trade_end and _next_date and _next_date >= _trade_end)
        if _is_last_sim_day:
            buy_orders = []  # 不在最后一天生成新买入（防止 entry==exit invalid）
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
    # 强制平仓日期：用 sim_end_date（若有），否则用数据末日
    if sim_end_date and sim_end_date in master_dates:
        last_date = sim_end_date
    elif sim_end_date:
        # sim_end_date 不在 master_dates，找最近的前一个交易日
        last_date = max((d for d in master_dates if d <= sim_end_date), default=master_dates[-2])
    else:
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
            "entry_regime":         h.get("entry_regime", _e1r_regime_on(entry_date)),
            "exit_regime":          _e1r_regime_on(last_date),
            "dominant_regime":      _e1r_dominant_regime(h.get("regime_day_weights", {})),
            "entry_type":           h.get("entry_type"),
            "regime_day_weights":   h.get("regime_day_weights", {}),
            "exit_type":            h.get("exit_type", "SIM_END"),
            "exit_warning_log":     h.get("exit_warning_log", []),
            "exit_warning_count":   len(h.get("exit_warning_log", [])),
        })
        del holdings[sym]

    # 修正3: 强制平仓后更新 final_equity
    final_equity = cash
    equity_curve.append(final_equity)

    sim_end_liquidation_record = {
        "date": last_date,
        "cash": round(cash, 2),
        "positions_value": 0.0,
        "total_equity": round(final_equity, 2),
        "open_positions_count": 0,
        "sim_end_trades": sim_end_count,
        "spx_regime": _e1r_regime_on(last_date) if e1r_regime_wiring_enabled else None,
        "e1r_active_mode": _e1r_mode_for_regime(_e1r_regime_on(last_date)) if e1r_regime_wiring_enabled else None,
        "risk_budget_mode": _e1r_risk_budget_for_regime(_e1r_regime_on(last_date))["mode"] if e1r_regime_wiring_enabled else None,
        "event": "SIM_END_LIQUIDATION",
    }

    # ════════════════════════════════════════════════════
    # 修正4: sample_validity 检查
    # ════════════════════════════════════════════════════
    # 统计回测区间（仅计算实际执行交易的天数）
    trade_dates = [d for d in master_dates
                   if (not _trade_start or d >= _trade_start)
                   and (not _trade_end or d <= _trade_end)]
    simulation_days = len(trade_dates)
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
    if dynamic_exit_enabled:
        logger.info(
            f"  Dynamic Exit stats: "
            f"warning={skip_reasons.get('dynamic_exit_warning',0)} "
            f"soft_confirmed={skip_reasons.get('dynamic_soft_exit_confirmed',0)} "
            f"hard_exit={skip_reasons.get('dynamic_hard_exit_triggered',0)}"
        )
    if invalid_trades:
        for inv in invalid_trades:
            logger.warn(f"  ⚠️  INVALID TRADE: {inv}")
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
            "ls60_exit_mode":             ls60_exit_mode,
            "candidate_top_n":            candidate_top_n,
            "qualified_entry_enabled":    qualified_entry_enabled,
            "qualified_rs_min":           qualified_rs_min,
            "qualified_momentum_min":     qualified_momentum_min,
            "qualified_th_min":           qualified_th_min,
            "qualified_states":           list(qualified_states),
            "qualified_price_above_ma50": qualified_price_above_ma50,
            "qualified_ma50_slope_min":   qualified_ma50_slope_min,
            # Qualified Pool 诊断
            "qp_avg_pool_size":          round(qp_diag["pool_size_sum"] / max(qp_diag["pool_days"], 1), 1),
            "qp_pool_days":              qp_diag["pool_days"],
            "qp_days_pool_lt_3":         qp_diag["days_pool_lt_3"],
            "qp_days_pool_ge_10":        qp_diag["days_pool_ge_10"],
            "qp_buy_orders_generated":   qp_diag["buy_orders_generated"],
            "min_holding_days": min_holding_days,
            "min_hold_allow_broken_exit": min_hold_allow_broken_exit,
            "e1r_regime_wiring_enabled": e1r_regime_wiring_enabled,
            "e1r_regime_source": a.get("e1r_regime_source") if e1r_regime_wiring_enabled else None,
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
        "daily_equity_records": daily_equity_records,
        "daily_equity_record_count": len(daily_equity_records),
        "sim_end_liquidation_record": sim_end_liquidation_record,
        "e1r_candidates": e1r_candidate_records if e1r_shell_mode else [],
        "e1r_candidate_count": len(e1r_candidate_records) if e1r_shell_mode else 0,
        "e1r_uptrend_execution_enabled": e1r_uptrend_execution_enabled,
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
    ndx_prices: list[float] = None,
    ndx_dates:  list[str]   = None,
    sox_prices: list[float] = None,
    sox_dates:  list[str]   = None,
    vix_prices: list[float] = None,
    vix_dates:  list[str]   = None,
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
    logger.info("[Backtest Layer D v1.6] Strategy Variant Comparison...")

    base = {
        **LAYER_D_ASSUMPTIONS,
        "market_gate_enabled": False,
        "market_shock_gate_enabled": False,
        "partial_take_profit_enabled": False,
        "block_add_after_take_profit": False,
    }
    # ── Gate v2 No VIX（冻结市场层基准）─────────────────────────
    _gate_v2_no_vix = {
        "market_gate_enabled":       True,
        "risk_off_below_spx_ma50":   True,
        "market_shock_gate_enabled": True,
        "market_shock_daily_return": -0.02,
        "candidate_top_n":           None,
        "qualified_entry_enabled":   False,
        "fill_only_enabled":         False,
    }

    # ── E2 实验配置（Gate 固定 G4，只改退出层）────────────────
    _gate_g4 = {
        "market_gate_enabled":       True,
        "risk_off_below_spx_ma50":   False,
        "market_shock_gate_enabled": False,
        "market_shock_daily_return": -0.02,
        "gate_use_slope":            True,
        "gate_use_leadership":       True,
        "candidate_top_n":           None,
        "qualified_entry_enabled":   False,
        "fill_only_enabled":         False,
        "entry_top_n":               3,
        "entry_rs_min":              90.0,
        "ls60_exit_mode":            "exit",
    }

    def _load_e1r_regime_daily() -> dict:
        regime_path = Path("data/research/e1_5y/regimes/spx_regime_daily.json")
        if not regime_path.exists():
            logger.warn(f"  E1-R regime wiring: missing {regime_path}")
            return {}
        try:
            obj = json.loads(regime_path.read_text())
        except Exception as exc:
            logger.warn(f"  E1-R regime wiring: failed to load {regime_path}: {exc}")
            return {}
        daily = obj.get("daily_regime", obj) if isinstance(obj, dict) else {}
        return daily if isinstance(daily, dict) else {}

    _e1r_regime_daily = _load_e1r_regime_daily()

    variants = {
        # E1: Gate G4 + MinHold10（审计对照基准，不可修改）
        "E1_AUDITED_G4_MINHOLD10": {
            **base, **_gate_g4,
            "strategy_variant":      "E1_audited_g4_minhold10",
            "min_holding_days":      10,
            "dynamic_exit_enabled":  False,
            "relative_stop_enabled": False,
            "version":               "E1-audited-g4-minhold10",
        },
        # E1-R v0.1 shell: research candidate placeholder.
        # Shell intentionally mirrors E1 execution rules for Phase 1 so that
        # exports/backtest.json exposes the strategy ID without changing E1.
        "E1R_REGIME_AWARE_V0_1": {
            **base, **_gate_g4,
            "strategy_variant":      "E1R_regime_aware_v0_1_shell",
            "min_holding_days":      10,
            "dynamic_exit_enabled":  False,
            "relative_stop_enabled": False,
            "version":               "E1R-uptrend-execution-v0.1",
            "e1r_shell_mode":        True,
            "e1r_uptrend_execution_enabled": True,
            "e1r_regime_wiring_enabled": True,
            "e1r_regime_daily":      _e1r_regime_daily,
            "e1r_regime_source":     "data/research/e1_5y/regimes/spx_regime_daily.json",
            "e1r_spec_ref":          "docs/research/E1R_REGIME_AWARE_STRATEGY_SPEC_v0.1.md",
        },
        # E2v2: Gate G4 + Dynamic Exit v2（CAUTIOUS/CASH_MODE 下 LS<60 直接退出）
        "E2_DYNAMIC_EXIT_V2": {
            **base, **_gate_g4,
            "strategy_variant":      "E2_dynamic_exit_v2",
            "min_holding_days":      0,
            "dynamic_exit_enabled":  True,
            "relative_stop_enabled": False,
            "version":               "E2-dynamic-exit-v2",
        },
    }

    # ── 分期定义 ─────────────────────────────────────────────────
    # 时间轴保持完整（确保 warm-up / MA50 / RS 计算不失真）；
    # 只用 sim_start_date / sim_end_date 控制交易执行和统计区间。
    import os as _os
    if _os.environ.get("SP500_RESEARCH_5Y") == "1":
        periods = {
            "C_FULL_5Y_2021_06_TO_2026_06": {
                "label":          "Period C (Full 5Y): 2021-06 → 2026-06",
                "sim_start_date": "2021-06-11",
                "sim_end_date":   "2026-06-18",
            },
        }
    else:
        periods = {
            "A_2023_11_TO_2024_12": {
                "label":          "Period A: 2023-11 → 2024-12",
                "sim_start_date": "2023-11-06",
                "sim_end_date":   "2024-12-31",
            },
            "B_2024_12_TO_2026_06": {
                "label":          "Period B: 2024-12 → 2026-06",
                "sim_start_date": "2024-12-03",
                "sim_end_date":   "2026-06-11",
            },
            "C_FULL_2023_11_TO_2026_06": {
                "label":          "Period C (Full): 2023-11 → 2026-06",
                "sim_start_date": "2023-11-06",
                "sim_end_date":   "2026-06-11",
            },
        }

    # ── 逐 period × variant 跑回测 ──────────────────────────────
    period_results = {}
    for period_key, period_cfg in periods.items():
        logger.info(f"  ══ {period_cfg['label']} ══")
        period_results[period_key] = {"label": period_cfg["label"], "variants": {}}
        for variant_id, assumptions in variants.items():
            logger.info(f"    === {period_key}/{variant_id} ===")
            # E1/E2：Gate G4 固定使用 NDX/SOX（leadership），不传 VIX
            _use_ndx = ndx_prices or []
            _use_sox = sox_prices or []
            _use_vix = []  # Gate v2.1 不使用 VIX
            _result = run_stateful_simulation(
                symbols=symbols,
                prices_map=prices_map,
                dates_map=dates_map,
                spx_prices=spx_prices,
                spx_dates=spx_dates,
                assumptions=assumptions,
                sim_start_date=period_cfg["sim_start_date"],
                sim_end_date=period_cfg["sim_end_date"],
                ndx_prices=_use_ndx,
                ndx_dates=ndx_dates or [],
                sox_prices=_use_sox,
                sox_dates=sox_dates or [],
                vix_prices=_use_vix,
                vix_dates=vix_dates or [],
            )
            if assumptions.get("e1r_shell_mode"):
                _result["strategy_id"] = variant_id
                _result["research_status"] = "REGIME_WIRING_ONLY_NOT_IMPLEMENTED"
                _result["e1r_shell_mode"] = True
                _result["e1r_regime_wiring_enabled"] = True
                _result["e1r_spec_ref"] = assumptions.get("e1r_spec_ref")
                _result["e1r_regime_source"] = assumptions.get("e1r_regime_source")
                _result.setdefault("strategy_controls", {})["e1r_shell_mode"] = True
                _result["strategy_controls"]["e1r_regime_wiring_enabled"] = True
                _result["strategy_controls"]["e1r_spec_ref"] = assumptions.get("e1r_spec_ref")
                _result["strategy_controls"]["e1r_regime_source"] = assumptions.get("e1r_regime_source")
                if assumptions.get("e1r_uptrend_execution_enabled"):
                    _result["strategy_controls"]["regime_aware_logic"] = "UPTREND_EXECUTION_V0_1_ENTRY_ONLY"
                    _result["research_status"] = "UPTREND_EXECUTION_V0_1"
                    _result["e1r_candidate_tagging_enabled"] = True
                    _result["e1r_uptrend_execution_enabled"] = True
                    _result["strategy_controls"]["e1r_candidate_tagging_enabled"] = True
                    _result["strategy_controls"]["e1r_uptrend_execution_enabled"] = True
                    _result["strategy_controls"]["exit_reduce_logic"] = "LEGACY_E1_UNCHANGED"
                else:
                    _result["strategy_controls"]["regime_aware_logic"] = "NOT_IMPLEMENTED_PHASE_3A_CANDIDATE_TAGGING_ONLY"
                    _result["research_status"] = "UPTREND_CANDIDATE_TAGGING_ONLY_NOT_EXECUTED"
                    _result["e1r_candidate_tagging_enabled"] = True
                    _result["strategy_controls"]["e1r_candidate_tagging_enabled"] = True
            period_results[period_key]["variants"][variant_id] = _result

    # ── 为兼容现有输出格式，把 Period C（全区间）当作主结果 ────
    _full_period_key = "C_FULL_5Y_2021_06_TO_2026_06" if "C_FULL_5Y_2021_06_TO_2026_06" in period_results else "C_FULL_2023_11_TO_2026_06"
    variant_results = period_results[_full_period_key]["variants"]

    # ── E1-R v0.2 formal sidecar sleeve composition ────────────────
    #
    # Design principle:
    # - Do not modify run_stateful_simulation().
    # - Do not modify E1R_REGIME_AWARE_V0_1.
    # - Compose the validated SIDEWAYS:MA_CONFLICT Top10 25% sleeve
    #   with the existing E1R v0.1 core daily returns.
    #
    # This keeps the formal engine semantics aligned with the validated
    # research S4 sidecar instead of approximating it inside the Top3
    # stateful order loop.
    try:
        from src.engine.e1r_sidecar_sleeve import (
            E1RSidecarConfig,
            build_e1r_sidecar_sleeve,
        )
        from src.engine.e1r_composer import compose_e1r_v0_2_variant

        _core_e1r = variant_results.get("E1R_REGIME_AWARE_V0_1")
        _core_records = (_core_e1r or {}).get("daily_equity_records", []) if _core_e1r else []

        _stock_dir = Path("data/research/e1_5y/raw/stocks")
        _spx_path = Path("data/research/e1_5y/raw/indices/SPX.json")
        _regime_path = Path("data/research/e1_5y/regimes/spx_regime_daily.json")

        if _core_e1r and _core_records and _stock_dir.exists() and _spx_path.exists() and _regime_path.exists():
            _sidecar_cfg = E1RSidecarConfig(
                start_date=_core_records[0]["date"],
                end_date=_core_records[-1]["date"],
                allowed_subclasses=("MA_CONFLICT",),
                top_n=10,
                gross_exposure=0.25,
                min_history_days=200,
                min_price=5.0,
                initial_equity=float(base.get("initial_capital", 100000)),
                excluded_symbols=("VIXY",),
            )

            _sidecar_result = build_e1r_sidecar_sleeve(
                stock_dir=_stock_dir,
                spx_path=_spx_path,
                regime_path=_regime_path,
                config=_sidecar_cfg,
            )

            variant_results["E1R_REGIME_AWARE_V0_2"] = compose_e1r_v0_2_variant(
                core_variant_result=_core_e1r,
                sidecar_result=_sidecar_result,
                initial_equity=float(base.get("initial_capital", 100000)),
            )

            _sidecar_summary = _sidecar_result.get("summary", {}) or {}
            logger.info(
                "  E1-R v0.2 formal sidecar sleeve composed: "
                f"active_days={_sidecar_summary.get('active_days')} "
                f"return={_sidecar_summary.get('full_period_strategy_return_pct'):.2f}%"
            )
        else:
            logger.warn(
                "  E1-R v0.2 formal sidecar sleeve skipped: missing core records or research 5Y inputs"
            )

    except Exception as exc:
        logger.warn(f"  E1-R v0.2 formal sidecar sleeve failed: {exc}")

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
            "qualified_entry_enabled": controls.get("qualified_entry_enabled", False),
            "candidate_top_n": controls.get("candidate_top_n"),
            "qualified_states": controls.get("qualified_states", []),
            "relative_stop_stats": controls.get("relative_stop_stats", {}),
            "e1r_shell_mode": controls.get("e1r_shell_mode", False),
            "e1r_regime_wiring_enabled": controls.get("e1r_regime_wiring_enabled", False),
            "research_status": result.get("research_status"),
        })

    logger.info("  === 4-Variant Qualified Pool Comparison ===")
    for row in comparison_rows:
        marker = "SELECTED" if row["selected"] else ""
        qual = "QUAL" if row.get("qualified_entry_enabled") else "STRICT"
        cand = f"top{row.get('candidate_top_n','?')}" if row.get("qualified_entry_enabled") else f"top{row.get('entry_top_n','?')}"
        logger.info(
            f"  {row['variant']}: {row['status']} "
            f"{qual}({cand}) LS60={row.get('ls60_exit_mode','?')} "
            f"RS>={row.get('entry_rs_min','?')} "
            f"Return={row['total_return_pct']:+.2f}% "
            f"Alpha={row['alpha_pct']:+.2f}% "
            f"MaxDD={row['max_drawdown_pct']:.2f}% "
            f"PF={row.get('profit_factor','?')} Sharpe={row.get('sharpe_ratio','?')} {marker}"
        )
    logger.info(f"  Selected strategy variant: {selected_id}")

    # ── Qualified Pool 诊断摘要 ───────────────────────────────
    for vid, res in variant_results.items():
        ctrl = res.get("strategy_controls", {})
        if not ctrl.get("qualified_entry_enabled"):
            continue
        avg_pool  = ctrl.get("qp_avg_pool_size", 0)
        days_lt3  = ctrl.get("qp_days_pool_lt_3", 0)
        days_ge10 = ctrl.get("qp_days_pool_ge_10", 0)
        gen       = ctrl.get("qp_buy_orders_generated", 0)
        logger.info(
            f"  [QP Diag] {vid}: AvgPoolSize={avg_pool} "
            f"DaysLT3={days_lt3} DaysGE10={days_ge10} "
            f"BuyOrdersGenerated={gen}"
        )

    # ── 分期对比摘要 ──────────────────────────────────────────────
    logger.info("  ══ Period Comparison Summary ══")
    for period_key, pcfg in period_results.items():
        logger.info(f"  [{pcfg['label']}]")
        for vid, res in pcfg["variants"].items():
            r = res.get("total_return_pct", 0)
            a = res.get("alpha_pct", 0)
            dd = res.get("max_drawdown_pct", 0)
            pf = res.get("profit_factor", 0)
            n  = res.get("number_of_trades", 0)
            sd = res.get("sample_validity", {}).get("simulation_days", 0)
            logger.info(
                f"    {vid:<30} Return={r:+.1f}% Alpha={a:+.1f}% "
                f"MaxDD={dd:.1f}% PF={pf:.2f} Trades={n} Days={sd}"
            )

    # Preserve selected Layer D's top-level shape for current exporters/dashboard.
    return {
        **selected_result,
        "name": "Strategy Variant Comparison",
        "version": "v1.6-ls60-mode-comparison",
        "selected_variant": selected_id,
        "selection_policy": (
            "status(PASS>PARTIAL>FAIL), then total return, "
            "then profit factor, then Sharpe, then lower max drawdown"
        ),
        "comparison": comparison_rows,
        "variant_results": variant_results,
        "period_comparison": {
            pk: {
                "label":    pv["label"],
                "variants": {
                    vid: {
                        "status":           r.get("status"),
                        "total_return_pct": r.get("total_return_pct"),
                        "alpha_pct":        r.get("alpha_pct"),
                        "cagr_pct":         r.get("cagr_pct"),
                        "max_drawdown_pct": r.get("max_drawdown_pct"),
                        "profit_factor":    r.get("profit_factor"),
                        "sharpe_ratio":     r.get("sharpe_ratio"),
                        "number_of_trades": r.get("number_of_trades"),
                        "win_rate_pct":     r.get("win_rate_pct"),
                        "avg_holding_days": r.get("avg_holding_days"),
                        "simulation_days":  r.get("sample_validity", {}).get("simulation_days"),
                        "sim_start_date":   r.get("sample_validity", {}).get("simulation_start_date"),
                        "sim_end_date":     r.get("sample_validity", {}).get("simulation_end_date"),
                    }
                    for vid, r in pv["variants"].items()
                },
            }
            for pk, pv in period_results.items()
        },
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
    ndx_prices:   list[float] = None,
    ndx_dates:    list[str]   = None,
    sox_prices:   list[float] = None,
    sox_dates:    list[str]   = None,
    vix_prices:   list[float] = None,
    vix_dates:    list[str]   = None,
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
            symbols, prices_map, dates_map, spx_prices, spx_dates,
            ndx_prices=ndx_prices or [], ndx_dates=ndx_dates or [],
            sox_prices=sox_prices or [], sox_dates=sox_dates or [],
            vix_prices=vix_prices or [], vix_dates=vix_dates or [],
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
