"""
watchlist.py — Watchlist & Promotion Score  [Phase 2 Spec Section 8, 9, 10, 15]

Watchlist：Promotion Score Top20（不再是 Rank 11-30）

Promotion Score = 0.40×Momentum_Score + 0.30×Trend_Health
                + 0.20×Rank_Velocity   + 0.10×Momentum_Acceleration
输出：0~100
"""
from __future__ import annotations
from ..utils.helpers import read_json
from ..utils.config import LEADERBOARD_HIST_FILE


def rank_velocity(symbol: str, current_rank: int, lookback_days: int = 20) -> float:
    """
    Rank Velocity：过去20个交易日排名改善速度。
    输出：0~100
    50 = 排名不变，>50 = 上升，<50 = 下降
    """
    history = read_json(LEADERBOARD_HIST_FILE)
    if not history or not isinstance(history, list):
        return 50.0  # 无历史数据时返回中间值

    recent = history[-lookback_days:] if len(history) >= lookback_days else history
    past_ranks = []
    for day in recent:
        for stock in day.get("leaders", []) + day.get("watchlist", []):
            if stock.get("symbol") == symbol:
                past_ranks.append(stock.get("rank", current_rank))
                break

    if not past_ranks:
        return 50.0

    avg_past = sum(past_ranks) / len(past_ranks)
    # 排名改善 = 数字变小（从30→10 = 改善很大）
    # 归一化：改善20名 → +100点，恶化20名 → -100点，映射到 0-100
    raw_velocity = avg_past - current_rank  # 正=改善
    normalized = max(0.0, min(100.0, 50.0 + raw_velocity * 2.5))
    return round(normalized, 1)


def momentum_acceleration_score(
    mom_now: float, mom_5d_ago: float
) -> float:
    """
    Momentum Acceleration = Mom(t) / Mom(t-5)
    规格书：输出 0-100
    >1.0（加速）→ >50，<1.0（减速）→ <50
    """
    if mom_5d_ago <= 0:
        return 50.0
    ratio = mom_now / mom_5d_ago
    # ratio=2.0 → 100，ratio=0.5 → 0，ratio=1.0 → 50
    normalized = max(0.0, min(100.0, (ratio - 0.5) / 1.5 * 100))
    return round(normalized, 1)


def promotion_score(
    mom_score:   float,  # 0-100
    trend_health: float,  # 0-100
    rank_vel:    float,  # 0-100
    mom_accel:   float,  # 0-100
) -> float:
    """
    Promotion Score = 0.40×Mom + 0.30×TH + 0.20×RankVel + 0.10×MomAccel
    输出：0~100
    """
    return round(
        0.40 * max(0, min(100, mom_score))   +
        0.30 * max(0, min(100, trend_health)) +
        0.20 * max(0, min(100, rank_vel))    +
        0.10 * max(0, min(100, mom_accel)),
        2
    )


def build_watchlist(ranked_stocks: list[dict]) -> list[dict]:
    """
    Phase 2: Watchlist = Promotion Score Top20（从全部排名股票中选）
    不再限制 Rank 11-30。
    """
    candidates = []
    for s in ranked_stocks:
        sym   = s["symbol"]
        rank  = s["rank"]
        rv    = rank_velocity(sym, rank)
        mom   = s.get("momentum_score", 50)
        th    = s.get("trend_health", 50)

        # Momentum Acceleration：用动量得分与5日前的对比
        # 这里用斜率变化作为近似（精确值需历史数据）
        mom_prev = s.get("momentum_score_5d", mom)  # 如有历史则用，否则用当前
        ma_score = momentum_acceleration_score(mom, mom_prev)

        ps = promotion_score(mom, th, rv, ma_score)

        candidates.append({
            "symbol":          sym,
            "name":            s.get("name", sym),
            "sector":          s.get("sector", "Other"),
            "rank":            rank,
            "price":           s.get("price", 0),
            "leader_score":    s.get("leader_score", 0),
            "rs_score":        s.get("rs_score", 0),
            "momentum_score":  mom,
            "trend_health":    th,
            "trend_state":     s.get("trend_state", ""),
            "trade_action":    s.get("trade_action", "HOLD"),
            "action_label":    s.get("action_label", "持有"),
            "action_color":    s.get("action_color", "#888"),
            "drawdown_pct":    s.get("drawdown_pct", 0),
            "rank_velocity":   rv,
            "mom_acceleration":ma_score,
            "promotion_score": ps,
        })

    # 按 Promotion Score 降序，取 Top20
    candidates.sort(key=lambda x: x["promotion_score"], reverse=True)
    return candidates[:20]
