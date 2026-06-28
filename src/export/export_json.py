"""export_json.py — 输出层 Phase 2"""
from __future__ import annotations
from datetime import datetime
from pathlib import Path

try:
    import pytz
    ET = pytz.timezone("America/New_York")
except:
    from datetime import timezone, timedelta
    ET = timezone(timedelta(hours=-4))

from ..utils.config import (
    EXPORT_MARKET, EXPORT_LEADERBOARD, EXPORT_WATCHLIST,
    EXPORT_TRADES, EXPORT_LIFECYCLE, EXPORTS_DIR,
    LEADERBOARD_HIST_FILE, WATCHLIST_HIST_FILE,
)
from ..utils.helpers import read_json, write_json
from ..utils import logger

EXPORT_BACKTEST = EXPORTS_DIR / "backtest.json"
EXPORT_STOCK_CHARTS = EXPORTS_DIR / "stock_charts.json"


def _meta():
    now = datetime.now(ET)
    return {
        "generated_at":         now.isoformat(),
        "generated_at_display": now.strftime("%Y年%-m月%-d日 %H:%M ET"),
        "data_source":          "Yahoo Finance",
        "phase":                "2",
    }


def export_stock_charts(chart_source):
    """通用单股图表数据，供 UI hover preview 使用。
    独立 chart_source，不污染 leaderboard/watchlist/lifecycle 业务范围。
    字段名匹配 trend_state.py 实际输出。"""
    symbols = {}
    for s in chart_source or []:
        sym = s.get("symbol")
        if not sym:
            continue
        dates  = s.get("chart_dates") or []
        prices = s.get("chart_prices") or []
        ma20   = s.get("chart_ma20") or []
        ma50   = s.get("chart_ma50") or []
        if not dates or not prices:
            continue
        symbols[sym] = {
            "dates":          dates,
            "close":          prices,
            "ma20":           ma20,
            "ma50":           ma50,
            "leader_score":   s.get("leader_score"),
            "rs_score":       s.get("rs_score"),
            "momentum_score": s.get("momentum_score"),
            "trend_health":   s.get("trend_health"),
            "trend_state":    s.get("trend_state"),
            "trade_action":   s.get("trade_action"),
            "action_label":   s.get("action_label"),
            "price":          s.get("price"),
            "name":           s.get("name", sym),
            "sector":         s.get("sector", "Other"),
        }
    write_json(EXPORT_STOCK_CHARTS, {
        **_meta(),
        "lookback_days": 126,
        "symbols":       symbols,
    })
    logger.ok(f"stock_charts.json ({len(symbols)} 只)")


def export_all(market, leaders, watchlist, all_signals, backtest=None, chart_source=None):
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    meta = _meta()
    now  = datetime.now(ET).strftime("%Y-%m-%d")

    # market_state.json
    write_json(EXPORT_MARKET, {**meta, "market": market})
    logger.ok("market_state.json")

    # leaderboard.json（不含图表数据）
    clean = [{k: v for k, v in s.items()
              if k not in ("chart_dates","chart_prices","chart_ma20","chart_ma50")}
             for s in leaders]
    write_json(EXPORT_LEADERBOARD, {**meta, "leaders": clean})
    logger.ok(f"leaderboard.json ({len(leaders)} 只)")

    # trade_actions.json（含图表数据）
    write_json(EXPORT_TRADES, {**meta, "stocks": leaders})
    logger.ok("trade_actions.json")

    # stock_charts.json — UI hover preview（独立 chart_source，不污染业务范围）
    export_stock_charts(chart_source or all_signals)

    # watchlist.json
    write_json(EXPORT_WATCHLIST, {**meta, "watchlist": watchlist})
    logger.ok(f"watchlist.json ({len(watchlist)} 只)")

    # lifecycle.json — 按 Trend State 分组
    groups = {
        "Expansion":    [],
        "Healthy Trend":[],
        "Mature Trend": [],
        "Weakening Trend":[],
        "Broken Trend": [],
    }
    for s in all_signals:
        state = s.get("trend_state", "Broken Trend")
        if state in groups:
            groups[state].append({
                "symbol":         s["symbol"],
                "name":           s.get("name", s["symbol"]),
                "sector":         s.get("sector", "Other"),
                "rank":           s.get("rank", 0),
                "trend_health":   s.get("trend_health", 0),
                "momentum_score": s.get("momentum_score", 0),
                "rs_score":       s.get("rs_score", 0),
                "trend_state":    state,
                "trade_action":   s.get("trade_action", "HOLD"),
                "action_label":   s.get("action_label", "持有"),
                "action_color":   s.get("action_color", "#888"),
                "rs_raw":         s.get("rs_raw", 0),
                "drawdown_pct":   s.get("drawdown_pct", 0),
            })
    write_json(EXPORT_LIFECYCLE, {**meta, "regimes": groups})
    logger.ok("lifecycle.json")

    # backtest.json（可选）
    if backtest:
        write_json(EXPORT_BACKTEST, {**meta, "backtest": backtest})
        logger.ok("backtest.json")

    # 历史记录追加
    _append_history(LEADERBOARD_HIST_FILE, {
        "date":    now,
        "leaders": [{"symbol": s["symbol"], "rank": s.get("rank", 0),
                     "leader_score": s.get("leader_score", 0),
                     "momentum_score": s.get("momentum_score", 0)}
                    for s in leaders],
        "watchlist": [{"symbol": s["symbol"], "rank": s.get("rank", 0),
                       "promotion_score": s.get("promotion_score", 0)}
                      for s in watchlist[:5]],
    })
    logger.ok("历史记录已追加")


def _append_history(path, record, max_days=90):
    history = read_json(path) or []
    if not isinstance(history, list):
        history = []
    history = [h for h in history if h.get("date") != record.get("date")]
    history.append(record)
    if len(history) > max_days:
        history = history[-max_days:]
    write_json(path, history)
