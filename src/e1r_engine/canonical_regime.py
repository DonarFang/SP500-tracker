from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
import math
from typing import Any, Iterable

from e1r_engine.contracts import (
    AssetSeries,
    CanonicalRegime,
    CanonicalSubclass,
    DailyBar,
    RegimeRecord,
)


_EXECUTABLE_REGIMES = {
    "UPTREND",
    "SIDEWAYS",
    "DOWNTREND",
}

_VALID_COMBINATIONS = {
    ("UNCLASSIFIED", None),
    ("UPTREND", None),
    ("DOWNTREND", None),
    ("SIDEWAYS", "MA_CONFLICT"),
    ("SIDEWAYS", "DETERIORATION_TRANSITION"),
    ("SIDEWAYS", "RECOVERY_TRANSITION"),
}


@dataclass(frozen=True)
class RegimeDecision:
    """
    Canonical engine-owned Regime fact.

    `date` is the date on which the decision is represented.
    For a daily decision, `source_week_end_date` identifies the completed
    weekly close whose state is effective on that date.
    """

    date: str
    ready: bool
    regime: CanonicalRegime
    subclass: CanonicalSubclass = None
    source_week_end_date: str | None = None
    close_w: float | None = None
    ma10w: float | None = None
    ma40w: float | None = None
    ma40w_slope_13w: float | None = None
    reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        combination = (self.regime, self.subclass)

        if combination not in _VALID_COMBINATIONS:
            raise ValueError(
                "invalid canonical regime/subclass combination: "
                f"{combination}"
            )

        if self.ready != (self.regime in _EXECUTABLE_REGIMES):
            raise ValueError(
                "ready must be true exactly for executable Regime states"
            )

        if self.regime == "SIDEWAYS" and self.subclass is None:
            raise ValueError(
                "SIDEWAYS requires a canonical subclass"
            )

        if self.regime != "SIDEWAYS" and self.subclass is not None:
            raise ValueError(
                "non-SIDEWAYS Regime must not have a subclass"
            )

    def to_record(self) -> RegimeRecord:
        return RegimeRecord(
            date=self.date,
            spx_regime=self.regime,
            subclass=self.subclass or "NO_SUBCLASS",
            raw={
                "schema": "CanonicalRegimeDecisionV1",
                "ready": self.ready,
                "source_week_end_date": self.source_week_end_date,
                "close_w": self.close_w,
                "ma10w": self.ma10w,
                "ma40w": self.ma40w,
                "ma40w_slope_13w": self.ma40w_slope_13w,
                "reason": self.reason,
                "metadata": dict(self.metadata),
            },
            source_path="engine://canonical_regime",
        )


@dataclass(frozen=True)
class CanonicalRegimeTimeline:
    weekly_decisions: tuple[RegimeDecision, ...]
    daily_decisions: dict[str, RegimeDecision]
    metadata: dict[str, Any] = field(default_factory=dict)

    def decision_for_date(
        self,
        date_value: str,
    ) -> RegimeDecision:
        try:
            return self.daily_decisions[date_value]
        except KeyError as exc:
            raise KeyError(
                f"no canonical Regime decision for date: {date_value}"
            ) from exc

    def record_for_date(
        self,
        date_value: str,
    ) -> RegimeRecord:
        return self.decision_for_date(date_value).to_record()

    @property
    def daily_records(self) -> dict[str, RegimeRecord]:
        return {
            date_value: decision.to_record()
            for date_value, decision
            in self.daily_decisions.items()
        }


class CanonicalRegimeGenerator:
    """
    Single canonical Regime-generation module owned by E1R Engine.

    Frozen mechanism:
    SPX daily closes
    -> ISO weekly final close
    -> MA10W / MA40W / MA40W 13-week relative slope
    -> weekly state
    -> mandatory one-week lag
    -> daily Regime decisions.

    This module does not route strategies, rank candidates, apply market
    gates, size positions, mutate accounts, or execute orders.
    """

    @classmethod
    def generate(
        cls,
        source: AssetSeries | Iterable[DailyBar],
    ) -> CanonicalRegimeTimeline:
        bars, metadata = cls._normalize_input(source)
        weekly_rows = cls._build_weekly_rows(bars)
        weekly_decisions = cls._classify_weekly(weekly_rows)
        daily_decisions = cls._expand_daily(
            bars=bars,
            weekly_decisions=weekly_decisions,
        )

        return CanonicalRegimeTimeline(
            weekly_decisions=tuple(weekly_decisions),
            daily_decisions=daily_decisions,
            metadata={
                **metadata,
                "generator": "CanonicalRegimeGenerator",
                "schema": "CanonicalRegimeTimelineV1",
                "weekly_count": len(weekly_decisions),
                "daily_count": len(daily_decisions),
                "one_week_lag": True,
                "runtime_source": "GENERATED_CANONICAL",
            },
        )

    @staticmethod
    def _normalize_input(
        source: AssetSeries | Iterable[DailyBar],
    ) -> tuple[list[DailyBar], dict[str, Any]]:
        if isinstance(source, AssetSeries):
            if source.symbol.upper() != "SPX":
                raise ValueError(
                    "CanonicalRegimeGenerator requires SPX AssetSeries"
                )
            input_bars = list(source.bars)
            source_kind = "AssetSeries"
            source_path = source.source_path
        else:
            input_bars = list(source)
            source_kind = "DailyBarIterable"
            source_path = None

        if not input_bars:
            raise ValueError(
                "CanonicalRegimeGenerator requires non-empty SPX bars"
            )

        normalized: list[DailyBar] = []
        seen_dates: set[str] = set()
        original_dates: list[str] = []

        for index, bar in enumerate(input_bars):
            if not isinstance(bar, DailyBar):
                raise TypeError(
                    "CanonicalRegimeGenerator accepts DailyBar records; "
                    f"index={index}, type={type(bar).__name__}"
                )

            try:
                parsed_date = date.fromisoformat(bar.date)
            except Exception as exc:
                raise ValueError(
                    f"invalid SPX bar date at index {index}: {bar.date!r}"
                ) from exc

            normalized_date = parsed_date.isoformat()

            if normalized_date != bar.date:
                raise ValueError(
                    "SPX bar date must use canonical YYYY-MM-DD format: "
                    f"{bar.date!r}"
                )

            if normalized_date in seen_dates:
                raise ValueError(
                    f"duplicate SPX bar date: {normalized_date}"
                )

            close = float(bar.close)

            if not math.isfinite(close):
                raise ValueError(
                    f"non-finite SPX close on {normalized_date}"
                )

            if close <= 0:
                raise ValueError(
                    f"non-positive SPX close on {normalized_date}"
                )

            seen_dates.add(normalized_date)
            original_dates.append(normalized_date)

            normalized.append(
                DailyBar(
                    date=normalized_date,
                    open=bar.open,
                    high=bar.high,
                    low=bar.low,
                    close=close,
                    volume=bar.volume,
                )
            )

        sorted_bars = sorted(
            normalized,
            key=lambda row: row.date,
        )
        sorted_dates = [bar.date for bar in sorted_bars]

        return sorted_bars, {
            "source_kind": source_kind,
            "source_path": source_path,
            "input_bar_count": len(sorted_bars),
            "first_date": sorted_dates[0],
            "last_date": sorted_dates[-1],
            "input_reordered": original_dates != sorted_dates,
            "duplicate_dates_rejected": True,
            "invalid_close_rejected": True,
        }

    @staticmethod
    def _build_weekly_rows(
        bars: list[DailyBar],
    ) -> list[dict[str, Any]]:
        by_week: dict[
            tuple[int, int],
            DailyBar,
        ] = {}

        for bar in bars:
            parsed = date.fromisoformat(bar.date)
            iso_year, iso_week, _ = parsed.isocalendar()
            key = (int(iso_year), int(iso_week))

            current = by_week.get(key)

            if current is None or bar.date > current.date:
                by_week[key] = bar

        return [
            {
                "week_end_date": bar.date,
                "iso_year": iso_year,
                "iso_week": iso_week,
                "close": bar.close,
            }
            for (iso_year, iso_week), bar
            in sorted(by_week.items())
        ]

    @staticmethod
    def _sma(
        values: list[float],
        length: int,
    ) -> float | None:
        if len(values) < length:
            return None
        return sum(values[-length:]) / length

    @classmethod
    def _classify_weekly(
        cls,
        weekly_rows: list[dict[str, Any]],
    ) -> list[RegimeDecision]:
        closes = [
            float(row["close"])
            for row in weekly_rows
        ]
        decisions: list[RegimeDecision] = []

        for index, row in enumerate(weekly_rows):
            closes_so_far = closes[: index + 1]

            ma10w = cls._sma(closes_so_far, 10)
            ma40w = cls._sma(closes_so_far, 40)
            slope13w = None

            if ma40w is not None and index >= 13:
                ma40w_13_weeks_ago = cls._sma(
                    closes[: index + 1 - 13],
                    40,
                )

                if (
                    ma40w_13_weeks_ago is not None
                    and ma40w_13_weeks_ago > 0
                ):
                    slope13w = (
                        ma40w / ma40w_13_weeks_ago - 1
                    )

            close_w = float(row["close"])

            if (
                ma10w is None
                or ma40w is None
                or slope13w is None
            ):
                regime: CanonicalRegime = "UNCLASSIFIED"
                subclass: CanonicalSubclass = None
                reason = "insufficient_history"

            elif (
                close_w > ma40w
                and ma10w > ma40w
                and slope13w > 0
            ):
                regime = "UPTREND"
                subclass = None
                reason = "canonical_uptrend"

            elif (
                close_w < ma40w
                and ma10w < ma40w
                and slope13w < 0
            ):
                regime = "DOWNTREND"
                subclass = None
                reason = "canonical_downtrend"

            elif (
                close_w > ma40w
                and ma10w > ma40w
                and slope13w <= 0
            ):
                regime = "SIDEWAYS"
                subclass = "RECOVERY_TRANSITION"
                reason = "canonical_recovery_transition"

            elif (
                close_w < ma40w
                and ma10w < ma40w
                and slope13w >= 0
            ):
                regime = "SIDEWAYS"
                subclass = "DETERIORATION_TRANSITION"
                reason = "canonical_deterioration_transition"

            else:
                regime = "SIDEWAYS"
                subclass = "MA_CONFLICT"
                reason = "canonical_ma_conflict"

            decisions.append(
                RegimeDecision(
                    date=str(row["week_end_date"]),
                    ready=regime in _EXECUTABLE_REGIMES,
                    regime=regime,
                    subclass=subclass,
                    source_week_end_date=str(
                        row["week_end_date"]
                    ),
                    close_w=close_w,
                    ma10w=(
                        round(ma10w, 4)
                        if ma10w is not None
                        else None
                    ),
                    ma40w=(
                        round(ma40w, 4)
                        if ma40w is not None
                        else None
                    ),
                    ma40w_slope_13w=(
                        round(slope13w, 6)
                        if slope13w is not None
                        else None
                    ),
                    reason=reason,
                    metadata={
                        "iso_year": row["iso_year"],
                        "iso_week": row["iso_week"],
                        "decision_scope": "WEEKLY",
                    },
                )
            )

        return decisions

    @staticmethod
    def _expand_daily(
        *,
        bars: list[DailyBar],
        weekly_decisions: list[RegimeDecision],
    ) -> dict[str, RegimeDecision]:
        ordered_weekly = sorted(
            weekly_decisions,
            key=lambda decision: decision.date,
        )

        daily: dict[str, RegimeDecision] = {}
        weekly_index = 0
        applicable: RegimeDecision | None = None

        for bar in bars:
            parsed = date.fromisoformat(bar.date)
            monday = parsed - timedelta(
                days=parsed.weekday()
            )

            while weekly_index < len(ordered_weekly):
                candidate = ordered_weekly[weekly_index]
                candidate_date = date.fromisoformat(
                    candidate.date
                )

                if candidate_date < monday:
                    applicable = candidate
                    weekly_index += 1
                else:
                    break

            if applicable is None:
                daily[bar.date] = RegimeDecision(
                    date=bar.date,
                    ready=False,
                    regime="UNCLASSIFIED",
                    subclass=None,
                    source_week_end_date=None,
                    reason="no_prior_completed_week",
                    metadata={
                        "decision_scope": "DAILY",
                        "effective_week_monday": (
                            monday.isoformat()
                        ),
                        "one_week_lag": True,
                    },
                )
                continue

            source_week = date.fromisoformat(
                applicable.date
            )

            if not source_week < monday:
                raise RuntimeError(
                    "one-week lag invariant violated"
                )

            daily[bar.date] = RegimeDecision(
                date=bar.date,
                ready=applicable.ready,
                regime=applicable.regime,
                subclass=applicable.subclass,
                source_week_end_date=applicable.date,
                close_w=applicable.close_w,
                ma10w=applicable.ma10w,
                ma40w=applicable.ma40w,
                ma40w_slope_13w=(
                    applicable.ma40w_slope_13w
                ),
                reason=applicable.reason,
                metadata={
                    **dict(applicable.metadata),
                    "decision_scope": "DAILY",
                    "effective_week_monday": (
                        monday.isoformat()
                    ),
                    "one_week_lag": True,
                },
            )

        return daily
