"""
E1-R sidecar sleeve engine.

Purpose
-------
Formal engine module for E1R_REGIME_AWARE_V0_2 sidecar sleeve.

This module implements the same rule semantics that passed research validation:

- Active only in SIDEWAYS:MA_CONFLICT.
- Top-N basket selection.
- Gross exposure sleeve, default 25%.
- Daily close-to-close rebalance.
- VIXY excluded by default.
- DOWNTREND / RECOVERY / DETERIORATION have zero sleeve exposure.

Important
---------
This is intentionally separate from run_stateful_simulation().

The existing stateful Top3 engine remains responsible for:
- E1_AUDITED_G4_MINHOLD10
- E1R_REGIME_AWARE_V0_1 core
- E2_DYNAMIC_EXIT_V2

The sidecar sleeve is later composed with the E1R v0.1 core daily returns by
e1r_composer.py.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, median, pstdev
from typing import Any, Iterable, Optional, Sequence


@dataclass(frozen=True)
class E1RSidecarConfig:
    start_date: str
    end_date: str
    allowed_subclasses: tuple[str, ...] = ("MA_CONFLICT",)
    top_n: int = 10
    gross_exposure: float = 0.25
    min_history_days: int = 200
    min_price: float = 5.0
    initial_equity: float = 100000.0
    excluded_symbols: tuple[str, ...] = ("VIXY",)


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


def pct_display(decimal_return: Optional[float]) -> Optional[float]:
    return None if decimal_return is None else decimal_return * 100.0


def compound_return(returns: Iterable[Optional[float]]) -> float:
    value = 1.0
    for r in returns:
        if r is not None:
            value *= 1.0 + r
    return value - 1.0


def mean_or_none(values: Iterable[Optional[float]]) -> Optional[float]:
    xs = [x for x in values if x is not None]
    return mean(xs) if xs else None


def median_or_none(values: Iterable[Optional[float]]) -> Optional[float]:
    xs = [x for x in values if x is not None]
    return median(xs) if xs else None


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


def load_asset(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text())
    bars: list[dict[str, Any]] = []

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
    config: E1RSidecarConfig,
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    assets: dict[str, dict[str, Any]] = {}
    excluded_found: list[str] = []
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


def load_regimes(path: Path) -> dict[str, dict[str, Any]]:
    raw = json.loads(path.read_text())
    daily = raw.get("daily_regime", raw)
    return {
        date: value
        for date, value in daily.items()
        if isinstance(value, dict)
    }


def history_closes(asset: dict[str, Any], date: str, length: int) -> Optional[list[float]]:
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
    asset: dict[str, Any],
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
    asset: dict[str, Any],
    spx: dict[str, Any],
    date: str,
    config: E1RSidecarConfig,
) -> Optional[dict[str, Any]]:
    """
    Formal copy of the validated research S4 opportunity score.

    Score:
      2.0 * RS20 vs SPX
    + 1.0 * RS60 vs SPX
    + 0.5 * 20d momentum
    + 0.25 * 60d momentum
    + 3.0 * trend_points
    + 0.2 * 60d drawdown from high
    """
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
    spx: dict[str, Any],
    regimes: dict[str, dict[str, Any]],
    config: E1RSidecarConfig,
) -> list[tuple[str, str]]:
    dates = [
        d for d in spx["dates"]
        if config.start_date <= d <= config.end_date
        and d in regimes
    ]
    dates = sorted(dates)
    return list(zip(dates[:-1], dates[1:]))


def build_daily_rankings(
    stocks: dict[str, dict[str, Any]],
    spx: dict[str, Any],
    regimes: dict[str, dict[str, Any]],
    intervals: Sequence[tuple[str, str]],
    config: E1RSidecarConfig,
) -> dict[str, dict[str, Any]]:
    rankings: dict[str, dict[str, Any]] = {}

    for date, next_date in intervals:
        regime_info = regimes.get(date, {})
        if regime_info.get("regime") != "SIDEWAYS":
            continue

        candidates: list[dict[str, Any]] = []

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


def run_daily_rebalanced_sidecar(
    rankings: dict[str, dict[str, Any]],
    spx: dict[str, Any],
    regimes: dict[str, dict[str, Any]],
    intervals: Sequence[tuple[str, str]],
    config: E1RSidecarConfig,
) -> list[dict[str, Any]]:
    allowed_subclasses = set(config.allowed_subclasses)
    top_n = int(config.top_n)
    gross_exposure = float(config.gross_exposure)

    records: list[dict[str, Any]] = []

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

        holdings: list[dict[str, Any]] = []
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
    records: Sequence[dict[str, Any]],
    config: E1RSidecarConfig,
) -> dict[str, Any]:
    equity = config.initial_equity
    equity_curve = [equity]

    daily_returns = [r["portfolio_return"] for r in records]
    active_records = [r for r in records if r["is_active"]]
    active_returns = [r["portfolio_return"] for r in active_records]
    active_spx_returns = [r["spx_return"] for r in active_records]

    for record in records:
        equity *= 1.0 + record["portfolio_return"]
        equity_curve.append(equity)

    full_strategy_return = equity_curve[-1] / config.initial_equity - 1.0
    full_spx_return = compound_return(r["spx_return"] for r in records)
    active_strategy_return = compound_return(active_returns)
    active_spx_return = compound_return(active_spx_returns)

    wins = [r for r in active_records if r["portfolio_return"] > 0]
    losses = [r for r in active_records if r["portfolio_return"] < 0]

    return {
        "name": "E1R_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
        "allowed_subclasses": list(config.allowed_subclasses),
        "top_n": config.top_n,
        "gross_exposure": config.gross_exposure,
        "excluded_symbols": list(config.excluded_symbols),

        "total_days": len(records),
        "active_days": len(active_records),
        "exposure_pct_full_period": (
            100.0 * len(active_records) / len(records)
            if records else None
        ),

        "full_period_strategy_return_pct": pct_display(full_strategy_return),
        "full_period_spx_return_pct": pct_display(full_spx_return),
        "full_period_excess_vs_spx_pct": pct_display(full_strategy_return - full_spx_return),

        "active_window_strategy_return_pct": pct_display(active_strategy_return),
        "active_window_spx_return_pct": pct_display(active_spx_return),
        "active_window_excess_vs_spx_pct": pct_display(active_strategy_return - active_spx_return),

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
        "equity_start": config.initial_equity,
        "equity_end": equity_curve[-1],
    }


def build_e1r_sidecar_sleeve(
    stock_dir: Path,
    spx_path: Path,
    regime_path: Path,
    config: E1RSidecarConfig,
) -> dict[str, Any]:
    spx = load_asset(spx_path)
    regimes = load_regimes(regime_path)
    stocks, excluded_found = load_stock_universe(stock_dir, config)

    intervals = build_backtest_intervals(spx, regimes, config)
    rankings = build_daily_rankings(stocks, spx, regimes, intervals, config)
    records = run_daily_rebalanced_sidecar(rankings, spx, regimes, intervals, config)
    summary = summarize_sidecar(records, config)

    regime_counts: dict[str, int] = {}
    subclass_counts: dict[str, int] = {}

    for record in records:
        regime = record["regime"]
        subclass = record["subclass"]
        regime_counts[regime] = regime_counts.get(regime, 0) + 1
        if regime == "SIDEWAYS":
            subclass_counts[subclass] = subclass_counts.get(subclass, 0) + 1

    return {
        "engine": "e1r_sidecar_sleeve",
        "version": "v0.2_formal_sleeve_engine",
        "config": {
            "start_date": config.start_date,
            "end_date": config.end_date,
            "allowed_subclasses": list(config.allowed_subclasses),
            "top_n": config.top_n,
            "gross_exposure": config.gross_exposure,
            "min_history_days": config.min_history_days,
            "min_price": config.min_price,
            "initial_equity": config.initial_equity,
            "excluded_symbols": list(config.excluded_symbols),
        },
        "sample": {
            "intervals": len(intervals),
            "first_interval": {
                "date": intervals[0][0],
                "next_date": intervals[0][1],
            } if intervals else None,
            "last_interval": {
                "date": intervals[-1][0],
                "next_date": intervals[-1][1],
            } if intervals else None,
            "stock_universe_after_exclusions": len(stocks),
            "excluded_symbols_found_in_raw_data": excluded_found,
            "regime_counts": regime_counts,
            "sideways_subclass_counts": subclass_counts,
        },
        "summary": summary,
        "records": records,
    }
