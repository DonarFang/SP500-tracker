from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


EngineMode = Literal["BACKTEST", "PAPER", "LIVE"]

CanonicalRegime = Literal[
    "UNCLASSIFIED",
    "UPTREND",
    "SIDEWAYS",
    "DOWNTREND",
]

CanonicalSubclass = Literal[
    "MA_CONFLICT",
    "DETERIORATION_TRANSITION",
    "RECOVERY_TRANSITION",
    None,
]


@dataclass(frozen=True)
class DailyBar:
    date: str
    open: float | None
    high: float | None
    low: float | None
    close: float
    volume: float | None = None


@dataclass(frozen=True)
class AssetSeries:
    symbol: str
    dates: list[str]
    closes: list[float]
    bars: list[DailyBar]
    source_path: str
    meta: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.symbol:
            errors.append("missing_symbol")
        if not self.dates:
            errors.append(f"{self.symbol}:empty_dates")
        if len(self.dates) != len(self.closes):
            errors.append(f"{self.symbol}:dates_closes_len_mismatch")
        if len(self.dates) != len(self.bars):
            errors.append(f"{self.symbol}:dates_bars_len_mismatch")
        if self.dates != sorted(self.dates):
            errors.append(f"{self.symbol}:dates_not_sorted")
        return errors


@dataclass(frozen=True)
class RegimeRecord:
    date: str
    spx_regime: CanonicalRegime
    subclass: str = "NO_SUBCLASS"
    raw: Any = None
    source_path: str | None = None


@dataclass(frozen=True)
class HistoricalDataBundle:
    symbols: list[str]
    prices_map: dict[str, list[float]]
    dates_map: dict[str, list[str]]
    ohlc_map: dict[str, list[DailyBar]]
    indices: dict[str, AssetSeries]
    regime_daily: dict[str, RegimeRecord]
    vix: AssetSeries | None
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate_shape(self) -> dict[str, Any]:
        errors: list[str] = []

        if not self.symbols:
            errors.append("empty_symbols")

        for sym in self.symbols:
            if sym not in self.prices_map:
                errors.append(f"{sym}:missing_prices_map")
            if sym not in self.dates_map:
                errors.append(f"{sym}:missing_dates_map")
            if sym not in self.ohlc_map:
                errors.append(f"{sym}:missing_ohlc_map")

            prices = self.prices_map.get(sym, [])
            dates = self.dates_map.get(sym, [])
            bars = self.ohlc_map.get(sym, [])

            if len(prices) != len(dates):
                errors.append(f"{sym}:prices_dates_len_mismatch")
            if len(bars) != len(dates):
                errors.append(f"{sym}:bars_dates_len_mismatch")
            if dates and dates != sorted(dates):
                errors.append(f"{sym}:dates_not_sorted")

        for required_index in ["SPX", "NDX", "SOX"]:
            if required_index not in self.indices:
                errors.append(f"missing_index:{required_index}")
            else:
                errors.extend(self.indices[required_index].validate())

        if not self.regime_daily:
            errors.append("empty_regime_daily")

        return {
            "ok": len(errors) == 0,
            "errors": errors[:100],
            "error_count": len(errors),
            "symbols_count": len(self.symbols),
            "indices": sorted(self.indices.keys()),
            "regime_count": len(self.regime_daily),
            "vix_available": self.vix is not None,
        }


@dataclass(frozen=True)
class MarketSnapshot:
    date: str
    universe: list[str]
    prices_by_symbol: dict[str, DailyBar]
    indices: dict[str, DailyBar]
    regime: RegimeRecord | None
    metadata: dict[str, Any] = field(default_factory=dict)
    # Canonical formal-entry input.  When present, Engine.step owns Regime,
    # Market State/Gate, branch routing, ranking and position decisions.
    # Legacy callers (including the frozen 5Y path) remain valid because the
    # field is optional and the old precomputed-input path is preserved.
    history_by_symbol: dict[str, dict[str, DailyBar]] = field(
        default_factory=dict
    )


def strict_common_dates(named_date_lists: dict[str, list[str]]) -> dict[str, Any]:
    missing_or_empty = [name for name, dates in named_date_lists.items() if not dates]

    if missing_or_empty:
        return {
            "count": 0,
            "first": None,
            "last": None,
            "sample": [],
            "strict_ok": False,
            "missing_or_empty": missing_or_empty,
            "input_counts": {name: len(dates or []) for name, dates in named_date_lists.items()},
        }

    sets = [set(dates) for dates in named_date_lists.values()]
    common = sorted(set.intersection(*sets))

    return {
        "count": len(common),
        "first": common[0] if common else None,
        "last": common[-1] if common else None,
        "sample": common[:5],
        "strict_ok": len(common) > 0,
        "missing_or_empty": [],
        "input_counts": {name: len(dates or []) for name, dates in named_date_lists.items()},
    }
