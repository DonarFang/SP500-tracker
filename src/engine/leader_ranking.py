"""
leader_ranking.py — Leader Score  [Phase 2 Spec Section 7]

公式：
  Leader Score = 0.40×RS_Score + 0.35×Momentum_Score + 0.25×Trend_Health
  输出：0~100
"""
from __future__ import annotations


def leader_score(rs: float, mom: float, th: float) -> float:
    """
    rs:  RS Score (0-100)
    mom: Momentum Score (0-100)
    th:  Trend Health Score (0-100)
    """
    rs  = max(0.0, min(100.0, rs))
    mom = max(0.0, min(100.0, mom))
    th  = max(0.0, min(100.0, th))
    return round(0.40 * rs + 0.35 * mom + 0.25 * th, 2)


def rank_stocks(stocks: list[dict]) -> list[dict]:
    """按 leader_score 降序排列，写入 rank 字段。"""
    s = sorted(stocks, key=lambda x: x.get("leader_score", 0), reverse=True)
    for i, x in enumerate(s):
        x["rank"] = i + 1
    return s
