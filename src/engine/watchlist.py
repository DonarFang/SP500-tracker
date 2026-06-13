"""
watchlist.py — Watchlist & Promotion Score  [Phase 2 Rev. Watchlist Review]

核心修复：
1. 候选池改为 Rank 11-100（排除 Top10 Leaders）
2. Rank Velocity 用真实历史快照计算
3. Momentum Acceleration 用真实5日前数据计算
4. Promotion Score 权重调整：更强调"正在变强"

Promotion Score = 0.40×Momentum + 0.30×TrendHealth
                + 0.20×RankVelocity + 0.10×MomAcceleration
"""
from __future__ import annotations
from .rank_history import (
    compute_rank_velocity,
    compute_momentum_acceleration,
    get_rank_delta,
)
from ..utils import logger


def promotion_score(
    mom_score:    float,   # 0-100
    trend_health: float,   # 0-100
    rank_vel:     float,   # 0-100
    mom_accel:    float,   # 0-100
) -> float:
    """
    Promotion Score = 0.40×Mom + 0.30×TH + 0.20×RankVel + 0.10×MomAccel
    输出：0~100
    """
    return round(
        0.40 * max(0, min(100, mom_score))    +
        0.30 * max(0, min(100, trend_health)) +
        0.20 * max(0, min(100, rank_vel))     +
        0.10 * max(0, min(100, mom_accel)),
        2
    )


def build_watchlist(ranked_stocks: list[dict]) -> list[dict]:
    """
    Phase 2 Watchlist Review 修复版：

    候选池：Rank 11-100（排除 Top10 Leaders）
    排序：Promotion Score 降序
    输出：Top 20
    """
    # 候选池：Rank 11-100，排除已是 Leader Board 的股票
    candidates_raw = [s for s in ranked_stocks if 10 < s.get("rank", 999) <= 100]

    if not candidates_raw:
        # 兜底：如果不足，扩展到 Rank 11-50
        candidates_raw = [s for s in ranked_stocks if s.get("rank", 999) > 10]

    candidates = []
    for s in candidates_raw:
        sym   = s["symbol"]
        rank  = s["rank"]
        mom   = s.get("momentum_score", 50)
        th    = s.get("trend_health", 50)

        # 真实 Rank Velocity（从历史快照计算）
        rv = compute_rank_velocity(sym, rank, lookback_days=20)

        # 真实 Momentum Acceleration（从历史快照计算）
        ma_score = compute_momentum_acceleration(sym, mom, lookback_days=5)

        # Rank Delta（5日前排名变化，用于显示）
        rank_delta_5d  = get_rank_delta(sym, rank, days_ago=5)
        rank_delta_20d = get_rank_delta(sym, rank, days_ago=20)

        ps = promotion_score(mom, th, rv, ma_score)

        candidates.append({
            "symbol":           sym,
            "name":             s.get("name", sym),
            "sector":           s.get("sector", "Other"),
            "rank":             rank,
            "price":            s.get("price", 0),
            "leader_score":     s.get("leader_score", 0),
            "rs_score":         s.get("rs_score", 0),
            "momentum_score":   mom,
            "trend_health":     th,
            "trend_state":      s.get("trend_state", ""),
            "trade_action":     s.get("trade_action", "HOLD"),
            "action_label":     s.get("action_label", "持有"),
            "action_color":     s.get("action_color", "#888"),
            "drawdown_pct":     s.get("drawdown_pct", 0),
            "rank_velocity":    rv,
            "mom_acceleration": ma_score,
            "rank_delta_5d":    rank_delta_5d,
            "rank_delta_20d":   rank_delta_20d,
            "promotion_score":  ps,
        })

    # 按 Promotion Score 降序，取 Top 20
    candidates.sort(key=lambda x: x["promotion_score"], reverse=True)
    result = candidates[:20]

    # 统计并记录重叠率
    leader_syms = {s["symbol"] for s in ranked_stocks[:10]}
    overlap = sum(1 for s in result if s["symbol"] in leader_syms)
    if result:
        overlap_pct = overlap / len(result) * 100
        if overlap_pct > 30:
            logger.warn(f"  Watchlist与Leader Board重叠率 {overlap_pct:.0f}% > 30%，检查候选池")
        else:
            logger.info(f"  Watchlist重叠率: {overlap_pct:.0f}% (目标<30%)")

    return result
