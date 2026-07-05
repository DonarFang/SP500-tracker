#!/usr/bin/env python3
"""
Reusable research utilities for E1-R SIDEWAYS sidecar studies.

This module is intentionally independent from the official E1-R engine.
It provides:
- 5Y research data loading
- regime loading
- transparent candidate scoring
- daily rebalanced sidecar backtest
- benchmark-aware portfolio summary

No official strategy logic is modified here.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, median, pstdev
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class ResearchConfig:
    start_date: str
    end_date: str
    min_history_days: int = 200
    min_price: float = 5.0
    initial_equity: float = 100000.0
    excluded_symbols: Tuple[str, ...] = ("VIXY",)


def safe_float(value: Any) -> Optional[float]:
    try:
        if value is None:
            return None
        x = float(value)
        if math.isnan(x) or math.isinf(x):
            return None
        return x
    except Exception:
        return None


def mean_or_none(values: Iterable[Optional[float]]) -> Optional[float]:
    xs = [x for x in values if x is not None]
    return mean(xs) if xs else None


def median_or_none(values: Iterable[Optional[float]]) -> Optional[float]:
    xs = [x for x in values if x is not None]
    return median(xs) if xs else None


def pct_display(decimal_return: Optional[float]) -> Optional[float]:
    return None if decimal_return is None else decimal_return * 100.0


def compound_return(returns: Iterable[Optional[float]]) -> float:
    value = 1.0
    for r in returns:
        if r is not None:
            value *= 1.0 + r
    return value - 1.0


def load_asset(path: Path) -> Dict[str, Any]:
    raw = json.loads(path.read_text())
    bars: List[Dict[str, Any]] = []

    for row in raw.get("bars", []):
        date = row.get("date")
        close = safe_float(row.get("close"))
        if not date or close is None:
            continue

        bars.append({
            "date": date,
            "open": safe_float(row.get("open")),
            "high": safe_float(row.get("high")),
            "low": safe_float(row.get("low")),
            "close": close,
            "volume": safe_float(row.get("volume")),
        })

    bars.sort(key=lambda x: x["date"])

    return {
        "symbol": raw.get("symbol") or path.stem,
        "data_start": raw.get("data_start"),
        "data_end": raw.get("data_end"),
        "bars": bars,
        "dates": [x["date"] for x in bars],
        "by_date": {x["date"]: x for x in bars},
        "date_to_idx": {x["date"]: i for i, x in enumerate(bars)},
    }


def load_stock_universe(
    stock_dir: Path,
    config: ResearchConfig,
) -> Tuple[Dict[str, Dict[str, Any]], List[str]]:
    assets: Dict[str, Dict[str, Any]] = {}
    excluded_found: List[str] = []
    excluded = set(config.excluded_symbols)

    for path in sorted(stock_dir.glob("*.json")):
        asset = load_asset(path)
        symbol = asset["symbol"]

        if symbol in excluded:
            excluded_found.append(symbol)
            continue

        if len(asset["bars"]) < config.min_history_days:
            continue

        assets[symbol] = asset

    return assets, sorted(excluded_found)


def load_regimes(path: Path) -> Dict[str, Dict[str, Any]]:
    raw = json.loads(path.read_text())
    daily = raw.get("daily_regime", {})
    return {
        date: value
        for date, value in daily.items()
        if isinstance(value, dict)
    }


def history_closes(asset: Dict[str, Any], date: str, length: int) -> Optional[List[float]]:
    idx = asset["date_to_idx"].get(date)
    if idx is None or idx + 1 < length:
        return None
    return [asset["bars"][i]["close"] for i in range(idx - length + 1, idx + 1)]


def moving_average(values: Optional[Sequence[float]], length: int) -> Optional[float]:
    if values is None or len(values) < length:
        return None
    window = values[-length:]
    if any(x is None for x in window):
        return None
    return sum(window) / length


def slope_pct(values: Optional[Sequence[float]], periods: int) -> Optional[float]:
    if values is None or len(values) < periods + 1:
        return None
    first = values[-periods - 1]
    last = values[-1]
    if first is None or first == 0 or last is None:
        return None
    return (last / first - 1.0) * 100.0


def drawdown_from_high_pct(values: Optional[Sequence[float]]) -> Optional[float]:
    if not values:
        return None
    high = max(values)
    last = values[-1]
    if high <= 0:
        return None
    return (last / high - 1.0) * 100.0


def close_to_close_return(
    asset: Dict[str, Any],
    date: str,
    next_date: str,
) -> Optional[float]:
    left = asset["by_date"].get(date)
    right = asset["by_date"].get(next_date)

    if not left or not right:
        return None

    c0 = safe_float(left.get("close"))
    c1 = safe_float(right.get("close"))

    if c0 is None or c1 is None or c0 == 0:
        return None

    return c1 / c0 - 1.0


def score_candidate(
    asset: Dict[str, Any],
    spx: Dict[str, Any],
    date: str,
    config: ResearchConfig,
) -> Optional[Dict[str, Any]]:
    if date not in asset["by_date"]:
        return None

    close = safe_float(asset["by_date"][date].get("close"))
    if close is None or close < config.min_price:
        return None

    hist20 = history_closes(asset, date, 20)
    hist50 = history_closes(asset, date, 50)
    hist60 = history_closes(asset, date, 60)
    hist150 = history_closes(asset, date, 150)
    hist200 = history_closes(asset, date, 200)

    spx20 = history_closes(spx, date, 20)
    spx60 = history_closes(spx, date, 60)

    if not all([hist20, hist50, hist60, hist150, hist200, spx20, spx60]):
        return None

    ma20 = moving_average(hist20, 20)
    ma50 = moving_average(hist50, 50)
    ma150 = moving_average(hist150, 150)
    ma200 = moving_average(hist200, 200)

    mom20 = slope_pct(hist20, 19)
    mom60 = slope_pct(hist60, 59)
    spx_mom20 = slope_pct(spx20, 19)
    spx_mom60 = slope_pct(spx60, 59)

    rs20 = None if mom20 is None or spx_mom20 is None else mom20 - spx_mom20
    rs60 = None if mom60 is None or spx_mom60 is None else mom60 - spx_mom60

    dd60 = drawdown_from_high_pct(hist60)

    trend_points = 0
    trend_points += int(ma20 is not None and close > ma20)
    trend_points += int(ma50 is not None and close > ma50)
    trend_points += int(ma150 is not None and close > ma150)
    trend_points += int(ma200 is not None and close > ma200)
    trend_points += int(ma50 is not None and ma150 is not None and ma50 > ma150)
    trend_points += int(ma150 is not None and ma200 is not None and ma150 > ma200)

    score = 0.0
    if rs20 is not None:
        score += 2.0 * rs20
    if rs60 is not None:
        score += 1.0 * rs60
    if mom20 is not None:
        score += 0.5 * mom20
    if mom60 is not None:
        score += 0.25 * mom60

    score += 3.0 * trend_points

    if dd60 is not None:
        score += 0.2 * dd60

    return {
        "symbol": asset["symbol"],
        "score": score,
        "close": close,
        "mom20_pct": mom20,
        "mom60_pct": mom60,
        "rs20_vs_spx_pct": rs20,
        "rs60_vs_spx_pct": rs60,
        "trend_points_0_to_6": trend_points,
        "drawdown_60d_pct": dd60,
    }


def build_backtest_intervals(
    spx: Dict[str, Any],
    regimes: Dict[str, Dict[str, Any]],
    config: ResearchConfig,
) -> List[Tuple[str, str]]:
    dates = [
        d for d in spx["dates"]
        if config.start_date <= d <= config.end_date
        and d in regimes
    ]
    dates = sorted(dates)
    return list(zip(dates[:-1], dates[1:]))


def build_daily_rankings(
    stocks: Dict[str, Dict[str, Any]],
    spx: Dict[str, Any],
    regimes: Dict[str, Dict[str, Any]],
    intervals: Sequence[Tuple[str, str]],
    config: ResearchConfig,
) -> Dict[str, Dict[str, Any]]:
    rankings: Dict[str, Dict[str, Any]] = {}

    for date, next_date in intervals:
        regime_info = regimes.get(date, {})
        if regime_info.get("regime") != "SIDEWAYS":
            continue

        candidates: List[Dict[str, Any]] = []

        for asset in stocks.values():
            if date not in asset["by_date"] or next_date not in asset["by_date"]:
                continue

            candidate = score_candidate(asset, spx, date, config)
            if candidate is None:
                continue

            one_day_return = close_to_close_return(asset, date, next_date)
            if one_day_return is None:
                continue

            candidate["one_day_return"] = one_day_return
            candidates.append(candidate)

        candidates.sort(key=lambda x: x["score"], reverse=True)

        rankings[date] = {
            "date": date,
            "next_date": next_date,
            "regime": "SIDEWAYS",
            "subclass": regime_info.get("subclass") or "NO_SUBCLASS",
            "candidate_count": len(candidates),
            "candidates": candidates,
        }

    return rankings


def max_drawdown(equity_values: Sequence[float]) -> Optional[float]:
    if not equity_values:
        return None

    peak = equity_values[0]
    worst = 0.0

    for value in equity_values:
        peak = max(peak, value)
        if peak > 0:
            worst = min(worst, value / peak - 1.0)

    return worst


def sharpe_ratio(daily_returns: Sequence[float]) -> Optional[float]:
    values = [x for x in daily_returns if x is not None]
    if len(values) < 2:
        return None

    sigma = pstdev(values)
    if sigma == 0:
        return None

    return mean(values) / sigma * math.sqrt(252)


def profit_factor(daily_returns: Sequence[float]) -> Optional[float]:
    gains = sum(x for x in daily_returns if x is not None and x > 0)
    losses = -sum(x for x in daily_returns if x is not None and x < 0)

    if losses == 0:
        if gains == 0:
            return None
        return float("inf")

    return gains / losses


def run_daily_rebalanced_sidecar(
    variant: Dict[str, Any],
    rankings: Dict[str, Dict[str, Any]],
    spx: Dict[str, Any],
    regimes: Dict[str, Dict[str, Any]],
    intervals: Sequence[Tuple[str, str]],
) -> List[Dict[str, Any]]:
    allowed_subclasses = set(variant["allowed_subclasses"])
    top_n = int(variant["top_n"])
    gross_exposure = float(variant["gross_exposure"])

    records: List[Dict[str, Any]] = []

    for date, next_date in intervals:
        regime_info = regimes.get(date, {})
        regime = regime_info.get("regime") or "NO_REGIME"
        subclass = regime_info.get("subclass") or "NO_SUBCLASS"

        spx_return = close_to_close_return(spx, date, next_date) or 0.0

        ranked = rankings.get(date, {})
        candidates = ranked.get("candidates", [])

        is_active = (
            regime == "SIDEWAYS"
            and subclass in allowed_subclasses
            and top_n > 0
            and gross_exposure > 0
            and bool(candidates)
        )

        holdings: List[Dict[str, Any]] = []
        portfolio_return = 0.0

        if is_active:
            selected = candidates[:top_n]
            weight = gross_exposure / len(selected)

            for candidate in selected:
                raw_return = candidate["one_day_return"]
                contribution = weight * raw_return
                portfolio_return += contribution

                holdings.append({
                    "symbol": candidate["symbol"],
                    "score": candidate["score"],
                    "weight": weight,
                    "raw_return": raw_return,
                    "raw_return_pct": pct_display(raw_return),
                    "weighted_contribution": contribution,
                    "weighted_contribution_pct": pct_display(contribution),
                })

        records.append({
            "date": date,
            "next_date": next_date,
            "regime": regime,
            "subclass": subclass,
            "is_active": is_active,
            "candidate_count": len(candidates),
            "selected_count": len(holdings),
            "gross_exposure": gross_exposure if is_active else 0.0,
            "portfolio_return": portfolio_return,
            "portfolio_return_pct": pct_display(portfolio_return),
            "spx_return": spx_return,
            "spx_return_pct": pct_display(spx_return),
            "holdings": holdings,
        })

    return records


def summarize_sidecar(
    name: str,
    variant: Dict[str, Any],
    records: Sequence[Dict[str, Any]],
    initial_equity: float,
) -> Dict[str, Any]:
    equity = initial_equity
    equity_curve = [equity]

    daily_returns = [r["portfolio_return"] for r in records]
    active_records = [r for r in records if r["is_active"]]
    active_returns = [r["portfolio_return"] for r in active_records]
    active_spx_returns = [r["spx_return"] for r in active_records]

    sideways_records = [r for r in records if r["regime"] == "SIDEWAYS"]
    sideways_spx_returns = [r["spx_return"] for r in sideways_records]

    allowed = set(variant["allowed_subclasses"])
    allowed_sideways_records = [
        r for r in sideways_records
        if r["subclass"] in allowed
    ]
    allowed_sideways_spx_returns = [r["spx_return"] for r in allowed_sideways_records]

    trade_contrib = Counter()
    symbol_contrib = Counter()
    symbol_days = Counter()

    for record in records:
        equity *= 1.0 + record["portfolio_return"]
        equity_curve.append(equity)

        for holding in record["holdings"]:
            symbol = holding["symbol"]
            contribution = holding["weighted_contribution"]
            trade_key = f"{record['date']}->{record['next_date']}:{symbol}"

            trade_contrib[trade_key] += contribution
            symbol_contrib[symbol] += contribution
            symbol_days[symbol] += 1

    full_strategy_return = equity_curve[-1] / initial_equity - 1.0
    full_spx_return = compound_return(r["spx_return"] for r in records)
    active_spx_return = compound_return(active_spx_returns)
    sideways_spx_return = compound_return(sideways_spx_returns)
    allowed_sideways_spx_return = compound_return(allowed_sideways_spx_returns)

    active_strategy_return = compound_return(active_returns)

    wins = [r for r in active_records if r["portfolio_return"] > 0]
    losses = [r for r in active_records if r["portfolio_return"] < 0]

    total_abs_contribution = sum(abs(x) for x in trade_contrib.values())

    top_3_trades = trade_contrib.most_common(3)
    top_3_symbols = symbol_contrib.most_common(3)

    return {
        "name": name,
        "description": variant["description"],
        "allowed_subclasses": variant["allowed_subclasses"],
        "top_n": variant["top_n"],
        "gross_exposure": variant["gross_exposure"],

        "total_days": len(records),
        "active_days": len(active_records),
        "sideways_days": len(sideways_records),
        "allowed_sideways_days": len(allowed_sideways_records),
        "exposure_pct_full_period": (
            100.0 * len(active_records) / len(records)
            if records else None
        ),
        "exposure_pct_sideways_only": (
            100.0 * len(active_records) / len(sideways_records)
            if sideways_records else None
        ),

        "full_period_strategy_return_pct": pct_display(full_strategy_return),
        "full_period_spx_return_pct": pct_display(full_spx_return),
        "full_period_excess_vs_spx_pct": pct_display(full_strategy_return - full_spx_return),

        "active_window_strategy_return_pct": pct_display(active_strategy_return),
        "active_window_spx_return_pct": pct_display(active_spx_return),
        "active_window_excess_vs_spx_pct": pct_display(active_strategy_return - active_spx_return),

        "sideways_all_days_spx_return_pct": pct_display(sideways_spx_return),
        "allowed_sideways_spx_return_pct": pct_display(allowed_sideways_spx_return),

        "max_drawdown_pct": pct_display(max_drawdown(equity_curve)),
        "profit_factor": profit_factor(daily_returns),
        "sharpe": sharpe_ratio(daily_returns),

        "active_day_win_rate_pct": (
            100.0 * len(wins) / len(active_records)
            if active_records else None
        ),
        "winning_active_days": len(wins),
        "losing_active_days": len(losses),
        "avg_active_day_return_pct": pct_display(mean_or_none(active_returns)),
        "median_active_day_return_pct": pct_display(median_or_none(active_returns)),

        "trade_count_approx": sum(len(r["holdings"]) for r in active_records),
        "unique_symbols": len(symbol_days),
        "top_3_symbols_by_contribution": top_3_symbols,
        "top_3_trades_by_contribution": top_3_trades,
        "top_20_symbols_by_active_days": symbol_days.most_common(20),
        "top_3_symbols_contribution_pct_of_total_abs": (
            100.0 * sum(abs(v) for _, v in top_3_symbols) / total_abs_contribution
            if total_abs_contribution else None
        ),
        "top_3_trades_contribution_pct_of_total_abs": (
            100.0 * sum(abs(v) for _, v in top_3_trades) / total_abs_contribution
            if total_abs_contribution else None
        ),

        "equity_start": initial_equity,
        "equity_end": equity_curve[-1],
    }


def summarize_sample_counts(
    records: Sequence[Dict[str, Any]],
    stock_count: int,
    excluded_found: Sequence[str],
) -> Dict[str, Any]:
    regime_counts = Counter(r["regime"] for r in records)
    sideways_subclass_counts = Counter(
        r["subclass"] for r in records if r["regime"] == "SIDEWAYS"
    )

    return {
        "backtest_intervals": len(records),
        "regime_counts": dict(regime_counts),
        "sideways_subclass_counts": dict(sideways_subclass_counts),
        "stock_universe_after_exclusions": stock_count,
        "excluded_symbols_found_in_raw_data": list(excluded_found),
    }
