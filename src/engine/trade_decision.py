"""
trade_decision.py — Trade Decision Engine
Quantitative Model Specification v1.0 (Frozen)
"""
from __future__ import annotations

ACTION_META = {
    "BUY":   {"label":"买入", "color":"#1D9E75", "desc":"强势领导股，建仓信号"},
    "ADD":   {"label":"加仓", "color":"#378ADD", "desc":"趋势扩张，加仓信号"},
    "HOLD":  {"label":"持有", "color":"#BA7517", "desc":"趋势健康，维持仓位"},
    "REDUCE":{"label":"减仓", "color":"#D85A30", "desc":"趋势减弱，降低风险"},
    "EXIT":  {"label":"退出", "color":"#993C1D", "desc":"趋势破坏，止损离场"},
}

TREND_STATE_ZH = {
    "Expansion":      "强势扩张",
    "Healthy Trend":  "健康趋势",
    "Mature Trend":   "趋势成熟",
    "Weakening Trend":"趋势减弱",
    "Broken Trend":   "趋势破坏",
}


def trade_action(
    trend_state:   str,
    mom_score:     float,   # 0-100
    rs_score:      float,   # 0-100
    price:         float,
    ma50:          float,
    ma50_slope:    float,   # 新增：MA50斜率（用于EXIT条件）
    leader_score:  float,   # 0-100
    trend_health:  float,   # 0-100
    market_score:  float = 60.0,  # 0-100，默认中性
) -> str:
    """
    Quantitative Model Specification v1.0 Trade Rules (Frozen)

    BUY:    LeaderScore≥90 AND RS≥90 AND Mom≥85 AND TH≥80 AND MarketScore≥50
    ADD:    LeaderScore≥85 AND Expansion
    HOLD:   LeaderScore≥75 AND TH≥70
    REDUCE: LeaderScore<75 OR TH<60
    EXIT:   LeaderScore<60 OR (Price<MA50 AND MA50Slope<0) OR Broken
    """
    # EXIT — 最优先检查
    if trend_state == "Broken Trend":
        return "EXIT"
    if leader_score < 60:
        return "EXIT"
    if ma50 > 0 and price < ma50 and ma50_slope < 0:
        return "EXIT"

    # BUY
    if (leader_score >= 90 and rs_score >= 90 and
            mom_score >= 85 and trend_health >= 80 and market_score >= 50):
        return "BUY"

    # ADD
    if leader_score >= 85 and trend_state == "Expansion":
        return "ADD"

    # REDUCE
    if leader_score < 75 or trend_health < 60:
        return "REDUCE"

    # HOLD
    if leader_score >= 75 and trend_health >= 70:
        return "HOLD"

    # 默认 REDUCE（不满足 HOLD 条件）
    return "REDUCE"


def enrich_action(s: dict) -> dict:
    action = trade_action(
        s.get("trend_state", "Broken Trend"),
        s.get("momentum_score", 0),
        s.get("rs_score", 0),
        s.get("price", 0),
        s.get("ma50", 0),
        s.get("ma50_slope", 0),
        s.get("leader_score", 0),
        s.get("trend_health", 0),
        s.get("market_score", 60),
    )
    meta = ACTION_META.get(action, {})
    return {
        **s,
        "trade_action":       action,
        "action_label":       meta.get("label", action),
        "action_color":       meta.get("color", "#888"),
        "action_description": meta.get("desc", ""),
    }


# ── Reason constants ────────────────────────────────────────
EXIT_REASON_BROKEN_TREND              = "broken_trend"
EXIT_REASON_LEADER_SCORE_BELOW_60     = "leader_score_below_60"
EXIT_REASON_PRICE_BELOW_MA50          = "price_below_ma50_and_ma50_slope_down"
REDUCE_REASON_LEADER_SCORE_BELOW_75   = "leader_score_below_75"
REDUCE_REASON_TREND_HEALTH_BELOW_60   = "trend_health_below_60"
BUY_REASON_ALL_CONDITIONS_MET         = "all_entry_conditions_met"
HOLD_REASON_TREND_HEALTHY             = "trend_healthy"
NO_REASON                             = "no_exit_reason"


def trade_action_reason(
    trend_state:   str,
    mom_score:     float,
    rs_score:      float,
    price:         float,
    ma50:          float,
    ma50_slope:    float,
    leader_score:  float,
    trend_health:  float,
    market_score:  float = 60.0,
) -> dict:
    """
    同 trade_action() 相同的决策逻辑，但返回带原因的结构。

    返回：
    {
        "action": "EXIT" / "BUY" / ...,
        "primary_reason": "leader_score_below_60",
        "reasons": ["leader_score_below_60", ...]
    }

    原则：
    - 不改变 trade_action() 的返回逻辑
    - 记录所有满足的条件（reasons 可以有多个）
    - primary_reason = 最高优先级触发条件
    """
    reasons = []

    # EXIT 条件检查（按优先级）
    broken = is_broken_trend(trend_state)
    ls_below_60 = leader_score < 60
    price_broken = ma50 > 0 and price < ma50 and ma50_slope < 0

    if broken:
        reasons.append(EXIT_REASON_BROKEN_TREND)
    if ls_below_60:
        reasons.append(EXIT_REASON_LEADER_SCORE_BELOW_60)
    if price_broken:
        reasons.append(EXIT_REASON_PRICE_BELOW_MA50)

    if broken or ls_below_60 or price_broken:
        primary = (
            EXIT_REASON_BROKEN_TREND if broken else
            EXIT_REASON_LEADER_SCORE_BELOW_60 if ls_below_60 else
            EXIT_REASON_PRICE_BELOW_MA50
        )
        return {"action": "EXIT", "primary_reason": primary, "reasons": reasons}

    # BUY
    if (leader_score >= 90 and rs_score >= 90 and
            mom_score >= 85 and trend_health >= 80 and market_score >= 50):
        return {"action": "BUY", "primary_reason": BUY_REASON_ALL_CONDITIONS_MET, "reasons": [BUY_REASON_ALL_CONDITIONS_MET]}

    # ADD
    if leader_score >= 85 and trend_state == "Expansion":
        return {"action": "ADD", "primary_reason": "leader_score_above_85_expansion", "reasons": ["leader_score_above_85_expansion"]}

    # REDUCE
    reduce_reasons = []
    if leader_score < 75:
        reduce_reasons.append(REDUCE_REASON_LEADER_SCORE_BELOW_75)
    if trend_health < 60:
        reduce_reasons.append(REDUCE_REASON_TREND_HEALTH_BELOW_60)

    if reduce_reasons:
        return {"action": "REDUCE", "primary_reason": reduce_reasons[0], "reasons": reduce_reasons}

    # HOLD
    if leader_score >= 75 and trend_health >= 70:
        return {"action": "HOLD", "primary_reason": HOLD_REASON_TREND_HEALTHY, "reasons": [HOLD_REASON_TREND_HEALTHY]}

    # 默认 REDUCE
    return {"action": "REDUCE", "primary_reason": REDUCE_REASON_LEADER_SCORE_BELOW_75, "reasons": [REDUCE_REASON_LEADER_SCORE_BELOW_75]}


def is_broken_trend(trend_state: str) -> bool:
    """已在 backtest.py 定义，此处重复以保持 trade_decision.py 独立可用。"""
    return str(trend_state).strip().lower() in {"broken", "broken trend", "breakdown"}
