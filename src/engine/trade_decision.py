"""
trade_decision.py — Trade Decision Engine  [Phase 2 Spec Section 14]

规则（量化阈值，不再基于文字状态）：
  BUY:    Expansion AND Mom>=80 AND RS>=80
  ADD:    Healthy   AND Mom>=70
  HOLD:   Mature
  REDUCE: Weakening
  EXIT:   Broken OR Price < MA50
"""
from __future__ import annotations

ACTION_META = {
    "BUY":   {"label":"买入", "color":"#1D9E75", "desc":"强势扩张+动量加速，考虑建仓"},
    "ADD":   {"label":"加仓", "color":"#378ADD", "desc":"趋势健康+动量向上，可加仓"},
    "HOLD":  {"label":"持有", "color":"#BA7517", "desc":"趋势成熟，维持仓位"},
    "REDUCE":{"label":"减仓", "color":"#D85A30", "desc":"趋势减弱，考虑部分止盈"},
    "EXIT":  {"label":"退出", "color":"#993C1D", "desc":"趋势破坏，及时止损"},
}

# Trend State 中文映射
TREND_STATE_ZH = {
    "Expansion":      "强势扩张",
    "Healthy Trend":  "健康趋势",
    "Mature Trend":   "趋势成熟",
    "Weakening Trend":"趋势减弱",
    "Broken Trend":   "趋势破坏",
}


def trade_action(
    trend_state:  str,
    mom_score:    float,   # 0-100
    rs_score:     float,   # 0-100
    price:        float,
    ma50:         float,
) -> str:
    """
    Phase 2 量化规则：
    BUY:    Expansion + Mom>=80 + RS>=80
    ADD:    Healthy   + Mom>=70
    HOLD:   Mature
    REDUCE: Weakening
    EXIT:   Broken OR Price < MA50
    """
    # EXIT 优先检查
    if trend_state == "Broken Trend" or (ma50 > 0 and price < ma50):
        return "EXIT"
    if trend_state == "Expansion" and mom_score >= 80 and rs_score >= 80:
        return "BUY"
    if trend_state == "Healthy Trend" and mom_score >= 70:
        return "ADD"
    if trend_state in ("Expansion", "Healthy Trend"):
        return "HOLD"  # 达不到阈值则观望
    if trend_state == "Mature Trend":
        return "HOLD"
    if trend_state == "Weakening Trend":
        return "REDUCE"
    return "EXIT"


def enrich_action(s: dict) -> dict:
    """在 stock dict 上追加 trade_action 及其元数据。"""
    action = trade_action(
        s.get("trend_state", "Broken Trend"),
        s.get("momentum_score", 0),
        s.get("rs_score", 0),
        s.get("price", 0),
        s.get("ma50", 0),
    )
    meta = ACTION_META.get(action, {})
    return {
        **s,
        "trade_action":       action,
        "action_label":       meta.get("label", action),
        "action_color":       meta.get("color", "#888"),
        "action_description": meta.get("desc", ""),
    }
