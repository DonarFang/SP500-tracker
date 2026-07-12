"""Standalone SIDEWAYS decision/allocation core.

This module intentionally has no dependency on ``src.engine`` or legacy
backtest/account execution code.  It reproduces the frozen historical S4
SIDEWAYS allocation decision at the decision/configuration abstraction only.

It does not create OrderIntent objects, mutate cash, manage positions, or apply
the future max-three execution contract.  Those belong to later project steps.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence


@dataclass(frozen=True)
class SidewaysConfig:
    allowed_subclasses: tuple[str, ...] = ("MA_CONFLICT",)
    top_n: int = 10
    gross_exposure: float = 0.25
    min_history_days: int = 200
    min_price: float = 5.0
    excluded_symbols: tuple[str, ...] = ("VIXY",)


@dataclass(frozen=True)
class SidewaysCandidate:
    symbol: str
    score: float
    close: float
    mom20_pct: Optional[float]
    mom60_pct: Optional[float]
    rs20_vs_spx_pct: Optional[float]
    rs60_vs_spx_pct: Optional[float]
    trend_points_0_to_6: int
    drawdown_60d_pct: Optional[float]
    one_day_return: float


@dataclass(frozen=True)
class SidewaysAllocationHolding:
    symbol: str
    score: float
    weight: float
    raw_return: float
    weighted_contribution: float


@dataclass(frozen=True)
class SidewaysDecisionTrace:
    activation_checks: Mapping[str, bool]
    selected_symbols: tuple[str, ...]
    score_order: tuple[tuple[str, float], ...]
    tie_rule: str


@dataclass(frozen=True)
class SidewaysAllocationPlan:
    date: str
    next_date: str
    regime: str
    subclass: str
    is_active: bool
    candidate_count: int
    ranked_candidates: tuple[SidewaysCandidate, ...]
    selected_count: int
    holdings: tuple[SidewaysAllocationHolding, ...]
    gross_exposure: float
    portfolio_return: float
    spx_return: float
    trace: SidewaysDecisionTrace


def _safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    if result != result:  # NaN
        return None
    return result


def history_closes(
    asset: Mapping[str, Any],
    date: str,
    length: int,
) -> Optional[list[float]]:
    idx = asset["date_to_idx"].get(date)
    if idx is None or idx + 1 < length:
        return None
    return [
        asset["bars"][i]["close"]
        for i in range(idx - length + 1, idx + 1)
    ]


def moving_average(
    values: Optional[Sequence[float]],
    length: int,
) -> Optional[float]:
    if values is None or len(values) < length:
        return None
    window = values[-length:]
    if any(x is None for x in window):
        return None
    return sum(window) / length


def slope_pct(
    values: Optional[Sequence[float]],
    periods: int,
) -> Optional[float]:
    if values is None or len(values) < periods + 1:
        return None
    first = values[-periods - 1]
    last = values[-1]
    if first is None or first == 0 or last is None:
        return None
    return (last / first - 1.0) * 100.0


def drawdown_from_high_pct(
    values: Optional[Sequence[float]],
) -> Optional[float]:
    if not values:
        return None
    high = max(values)
    last = values[-1]
    if high <= 0:
        return None
    return (last / high - 1.0) * 100.0


def close_to_close_return(
    asset: Mapping[str, Any],
    date: str,
    next_date: str,
) -> Optional[float]:
    left = asset["by_date"].get(date)
    right = asset["by_date"].get(next_date)
    if not left or not right:
        return None
    c0 = _safe_float(left.get("close"))
    c1 = _safe_float(right.get("close"))
    if c0 is None or c1 is None or c0 == 0:
        return None
    return c1 / c0 - 1.0


def score_candidate(
    asset: Mapping[str, Any],
    spx: Mapping[str, Any],
    date: str,
    config: SidewaysConfig,
) -> Optional[dict[str, Any]]:
    """Return the frozen S4 opportunity-score components for one asset."""

    if date not in asset["by_date"]:
        return None

    close = _safe_float(asset["by_date"][date].get("close"))
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

    rs20 = (
        None
        if mom20 is None or spx_mom20 is None
        else mom20 - spx_mom20
    )
    rs60 = (
        None
        if mom60 is None or spx_mom60 is None
        else mom60 - spx_mom60
    )
    dd60 = drawdown_from_high_pct(hist60)

    trend_points = 0
    trend_points += int(ma20 is not None and close > ma20)
    trend_points += int(ma50 is not None and close > ma50)
    trend_points += int(ma150 is not None and close > ma150)
    trend_points += int(ma200 is not None and close > ma200)
    trend_points += int(
        ma50 is not None and ma150 is not None and ma50 > ma150
    )
    trend_points += int(
        ma150 is not None and ma200 is not None and ma150 > ma200
    )

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


def build_intervals(
    spx: Mapping[str, Any],
    regimes: Mapping[str, Mapping[str, Any]],
    start_date: str,
    end_date: str,
) -> list[tuple[str, str]]:
    dates = [
        date
        for date in spx["dates"]
        if start_date <= date <= end_date and date in regimes
    ]
    dates = sorted(dates)
    return list(zip(dates[:-1], dates[1:]))


class SidewaysCore:
    """Stateless SIDEWAYS ranking and allocation decision component."""

    _TIE_RULE = (
        "stable score-descending sort; ties preserve stock dictionary "
        "insertion order"
    )

    def __init__(self, config: SidewaysConfig | None = None) -> None:
        self.config = config or SidewaysConfig()

    def rank_interval(
        self,
        *,
        stocks: Mapping[str, Mapping[str, Any]],
        spx: Mapping[str, Any],
        date: str,
        next_date: str,
        regime: str,
        subclass: str,
    ) -> tuple[SidewaysCandidate, ...]:
        if regime != "SIDEWAYS":
            return ()

        candidates: list[SidewaysCandidate] = []
        excluded = set(self.config.excluded_symbols)

        for asset in stocks.values():
            symbol = str(asset.get("symbol", ""))
            if symbol in excluded:
                continue
            if len(asset.get("bars", ())) < self.config.min_history_days:
                continue
            if (
                date not in asset["by_date"]
                or next_date not in asset["by_date"]
            ):
                continue

            scored = score_candidate(asset, spx, date, self.config)
            if scored is None:
                continue

            one_day_return = close_to_close_return(asset, date, next_date)
            if one_day_return is None:
                continue

            candidates.append(
                SidewaysCandidate(
                    symbol=scored["symbol"],
                    score=scored["score"],
                    close=scored["close"],
                    mom20_pct=scored["mom20_pct"],
                    mom60_pct=scored["mom60_pct"],
                    rs20_vs_spx_pct=scored["rs20_vs_spx_pct"],
                    rs60_vs_spx_pct=scored["rs60_vs_spx_pct"],
                    trend_points_0_to_6=scored["trend_points_0_to_6"],
                    drawdown_60d_pct=scored["drawdown_60d_pct"],
                    one_day_return=one_day_return,
                )
            )

        candidates.sort(key=lambda candidate: candidate.score, reverse=True)
        return tuple(candidates)

    def decide_interval(
        self,
        *,
        stocks: Mapping[str, Mapping[str, Any]],
        spx: Mapping[str, Any],
        date: str,
        next_date: str,
        regime: str,
        subclass: str,
    ) -> SidewaysAllocationPlan:
        ranked = self.rank_interval(
            stocks=stocks,
            spx=spx,
            date=date,
            next_date=next_date,
            regime=regime,
            subclass=subclass,
        )

        top_n = int(self.config.top_n)
        gross = float(self.config.gross_exposure)
        checks = {
            "regime_is_sideways": regime == "SIDEWAYS",
            "subclass_allowed": subclass in set(
                self.config.allowed_subclasses
            ),
            "top_n_positive": top_n > 0,
            "gross_exposure_positive": gross > 0,
            "has_candidates": bool(ranked),
        }
        is_active = all(checks.values())

        holdings: list[SidewaysAllocationHolding] = []
        portfolio_return = 0.0

        if is_active:
            selected = ranked[:top_n]
            weight = gross / len(selected)
            for candidate in selected:
                contribution = weight * candidate.one_day_return
                portfolio_return += contribution
                holdings.append(
                    SidewaysAllocationHolding(
                        symbol=candidate.symbol,
                        score=candidate.score,
                        weight=weight,
                        raw_return=candidate.one_day_return,
                        weighted_contribution=contribution,
                    )
                )

        spx_return = close_to_close_return(spx, date, next_date) or 0.0

        return SidewaysAllocationPlan(
            date=date,
            next_date=next_date,
            regime=regime or "NO_REGIME",
            subclass=subclass or "NO_SUBCLASS",
            is_active=is_active,
            candidate_count=len(ranked),
            ranked_candidates=ranked,
            selected_count=len(holdings),
            holdings=tuple(holdings),
            gross_exposure=gross if is_active else 0.0,
            portfolio_return=portfolio_return,
            spx_return=spx_return,
            trace=SidewaysDecisionTrace(
                activation_checks=checks,
                selected_symbols=tuple(h.symbol for h in holdings),
                score_order=tuple(
                    (candidate.symbol, candidate.score)
                    for candidate in ranked
                ),
                tie_rule=self._TIE_RULE,
            ),
        )

    def decide_many(
        self,
        *,
        stocks: Mapping[str, Mapping[str, Any]],
        spx: Mapping[str, Any],
        regimes: Mapping[str, Mapping[str, Any]],
        intervals: Sequence[tuple[str, str]],
    ) -> list[SidewaysAllocationPlan]:
        plans = []
        for date, next_date in intervals:
            info = regimes.get(date, {})
            plans.append(
                self.decide_interval(
                    stocks=stocks,
                    spx=spx,
                    date=date,
                    next_date=next_date,
                    regime=info.get("regime") or "NO_REGIME",
                    subclass=info.get("subclass") or "NO_SUBCLASS",
                )
            )
        return plans
