"""
rank_history.py — 每日排名快照系统

每天保存：data/rank_history/YYYY-MM-DD.json
用于计算：
  Rank Velocity        = 过去20日排名改善速度
  Momentum Acceleration = Momentum(today) / Momentum(5日前)
"""
from __future__ import annotations
from datetime import datetime, timedelta
from pathlib import Path
from ..utils.helpers import read_json, write_json
from ..utils.config import DATA_DIR
from ..utils import logger

RANK_HISTORY_DIR = DATA_DIR / "rank_history"


def save_daily_snapshot(date: str, ranked_stocks: list[dict]) -> None:
    """保存当日排名快照。"""
    RANK_HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    snapshot = [
        {
            "symbol":         s["symbol"],
            "rank":           s["rank"],
            "leader_score":   round(s.get("leader_score", 0), 2),
            "momentum_score": round(s.get("momentum_score", 0), 2),
            "trend_health":   round(s.get("trend_health", 0), 2),
            "rs_score":       round(s.get("rs_score", 0), 2),
        }
        for s in ranked_stocks
    ]
    path = RANK_HISTORY_DIR / f"{date}.json"
    write_json(path, snapshot)
    logger.ok(f"rank_history/{date}.json ({len(snapshot)} 只)")


def load_snapshot(date: str) -> list[dict]:
    """读取某日快照。"""
    path = RANK_HISTORY_DIR / f"{date}.json"
    data = read_json(path)
    return data if isinstance(data, list) else []


def get_recent_snapshots(lookback_days: int = 20) -> dict[str, list[dict]]:
    """
    读取最近 lookback_days 个交易日的快照。
    返回 {date_str: [snapshot]}
    """
    RANK_HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    snapshots = {}
    # 读取所有已存在的快照文件，取最近的
    files = sorted(RANK_HISTORY_DIR.glob("*.json"), reverse=True)
    for f in files[:lookback_days]:
        date_str = f.stem
        data = read_json(f)
        if isinstance(data, list) and data:
            snapshots[date_str] = data
    return snapshots


def compute_rank_velocity(symbol: str, current_rank: int,
                           lookback_days: int = 20) -> float:
    """
    Rank Velocity：过去20个交易日排名改善速度。
    输出：0~100
      50 = 排名不变
      >50 = 排名上升（变小）
      <50 = 排名下降（变大）

    例：Rank 96→42（改善54名）→ 高 Velocity
    """
    snapshots = get_recent_snapshots(lookback_days)
    if not snapshots:
        return 50.0  # 无历史数据

    past_ranks = []
    for date_str, snapshot in snapshots.items():
        for s in snapshot:
            if s.get("symbol") == symbol:
                past_ranks.append(s["rank"])
                break

    if not past_ranks:
        return 50.0

    # 取最早的排名（20日前）和最新的（今天）
    oldest_rank = past_ranks[-1]  # 最早的
    # 改善量：正值=排名上升（数字变小）
    rank_delta = oldest_rank - current_rank
    # 归一化：改善50名 → 100分，恶化50名 → 0分
    normalized = max(0.0, min(100.0, 50.0 + rank_delta))
    return round(normalized, 1)


def compute_momentum_acceleration(symbol: str, mom_today: float,
                                   lookback_days: int = 5) -> float:
    """
    Momentum Acceleration = Momentum(today) / Momentum(5日前)
    输出：0~100
      50 = 动量不变（ratio=1.0）
      >50 = 动量加速
      <50 = 动量减速

    规格书：Acceleration = Momentum(t) / Momentum(t-5)
    """
    snapshots = get_recent_snapshots(lookback_days + 2)
    if not snapshots:
        return 50.0

    # 找5日前的 momentum
    dates_sorted = sorted(snapshots.keys())
    mom_5d_ago = None

    if len(dates_sorted) >= lookback_days:
        past_date = dates_sorted[-(lookback_days)]
        for s in snapshots.get(past_date, []):
            if s.get("symbol") == symbol:
                mom_5d_ago = s.get("momentum_score", None)
                break

    if mom_5d_ago is None or mom_5d_ago <= 0:
        return 50.0

    if mom_today <= 0:
        return 25.0  # 动量为零或负，偏低

    ratio = mom_today / mom_5d_ago
    # ratio=2.0 → 100，ratio=0.5 → 0，ratio=1.0 → 50
    normalized = max(0.0, min(100.0, (ratio - 0.5) / 1.5 * 100))
    return round(normalized, 1)


def get_rank_delta(symbol: str, current_rank: int, days_ago: int = 5) -> int:
    """
    返回 days_ago 天前的排名 - 今天排名。
    正值=上升，负值=下降，0=无数据。
    """
    snapshots = get_recent_snapshots(days_ago + 2)
    if not snapshots:
        return 0
    dates_sorted = sorted(snapshots.keys())
    if len(dates_sorted) < days_ago:
        return 0
    past_date = dates_sorted[-(days_ago)]
    for s in snapshots.get(past_date, []):
        if s.get("symbol") == symbol:
            return s["rank"] - current_rank  # 正=上升
    return 0
