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
