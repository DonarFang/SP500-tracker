"""Independent Live data adapter for the shared FD-M3180125 Engine.

This adapter owns only Live-source normalization. It never reads 5Y or
Engine Forward paths and does not import either runtime. RegimeRecord and
formal branch inputs are standard Engine contracts supplied by the Engine
composition; this adapter does not reimplement strategy logic.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Sequence

from e1r_engine.contracts import (
    AssetSeries,
    DailyBar,
    HistoricalDataBundle,
    MarketSnapshot,
    RegimeRecord,
)


class LiveDataAdapterError(ValueError):
    """Raised when independent Live data cannot satisfy Engine contracts."""


def _float_value(value: object, field: str, *, optional: bool) -> Optional[float]:
    if value is None and optional:
        return None
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise LiveDataAdapterError(f"{field} is not numeric") from exc
    if not parsed.is_finite():
        raise LiveDataAdapterError(f"{field} must be finite")
    return float(parsed)


class LiveDataAdapter:
    """Normalize `data/live_prices` JSON into standard Engine contracts."""

    INDEX_SYMBOLS = ("SPX", "NDX", "SOX")
    VIX_SYMBOL = "VIX"

    def __init__(self, price_root: Path) -> None:
        self.price_root = Path(price_root)
        if self.price_root.name != "live_prices":
            raise LiveDataAdapterError(
                "Live data root must be named live_prices"
            )

    def _path(self, symbol: str) -> Path:
        normalized = str(symbol).strip().upper()
        if not normalized:
            raise LiveDataAdapterError("symbol is required")
        return self.price_root / f"{normalized}.json"

    def load_asset_series(self, symbol: str) -> AssetSeries:
        normalized = str(symbol).strip().upper()
        path = self._path(normalized)
        if not path.is_file():
            raise LiveDataAdapterError(
                f"missing independent Live price file: {normalized}"
            )

        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise LiveDataAdapterError(
                f"{normalized} payload must be a JSON list"
            )

        bars_by_date: dict[str, DailyBar] = {}
        for row in payload:
            if not isinstance(row, dict):
                raise LiveDataAdapterError(
                    f"{normalized} contains a non-object row"
                )

            raw_date = str(row.get("date", ""))
            try:
                date.fromisoformat(raw_date)
            except ValueError as exc:
                raise LiveDataAdapterError(
                    f"{normalized} has invalid ISO date: {raw_date}"
                ) from exc

            if raw_date in bars_by_date:
                raise LiveDataAdapterError(
                    f"{normalized} duplicate date: {raw_date}"
                )

            open_price = _float_value(row.get("open"), "open", optional=True)
            high = _float_value(row.get("high"), "high", optional=True)
            low = _float_value(row.get("low"), "low", optional=True)
            close = _float_value(row.get("close"), "close", optional=False)
            volume = _float_value(row.get("volume"), "volume", optional=True)

            if close is None or close <= 0:
                raise LiveDataAdapterError(
                    f"{normalized} close must be positive"
                )
            for field_name, value in (
                ("open", open_price),
                ("high", high),
                ("low", low),
            ):
                if value is not None and value <= 0:
                    raise LiveDataAdapterError(
                        f"{normalized} {field_name} must be positive"
                    )
            if volume is not None and volume < 0:
                raise LiveDataAdapterError(
                    f"{normalized} volume must not be negative"
                )
            if high is not None:
                observed = [
                    value for value in (open_price, low, close)
                    if value is not None
                ]
                if observed and high < max(observed):
                    raise LiveDataAdapterError(
                        f"{normalized} invalid high on {raw_date}"
                    )
            if low is not None:
                observed = [
                    value for value in (open_price, high, close)
                    if value is not None
                ]
                if observed and low > min(observed):
                    raise LiveDataAdapterError(
                        f"{normalized} invalid low on {raw_date}"
                    )

            bars_by_date[raw_date] = DailyBar(
                date=raw_date,
                open=open_price,
                high=high,
                low=low,
                close=close,
                volume=volume,
            )

        dates = sorted(bars_by_date)
        if not dates:
            raise LiveDataAdapterError(
                f"{normalized} contains no bars"
            )

        bars = [bars_by_date[item] for item in dates]
        series = AssetSeries(
            symbol=normalized,
            dates=dates,
            closes=[bar.close for bar in bars],
            bars=bars,
            source_path=str(path),
            meta={
                "source": "LIVE",
                "adapter": "LiveDataAdapter",
            },
        )
        errors = series.validate()
        if errors:
            raise LiveDataAdapterError(
                f"{normalized} invalid AssetSeries: {'; '.join(errors)}"
            )
        return series

    def load_bundle(
        self,
        *,
        stock_symbols: Sequence[str],
        regime_daily: Mapping[str, RegimeRecord],
        min_bars: int = 120,
        index_symbols: Sequence[str] = INDEX_SYMBOLS,
        vix_symbol: str = VIX_SYMBOL,
    ) -> HistoricalDataBundle:
        if min_bars <= 0:
            raise LiveDataAdapterError("min_bars must be positive")

        symbols: list[str] = []
        prices_map: dict[str, list[float]] = {}
        dates_map: dict[str, list[str]] = {}
        ohlc_map: dict[str, list[DailyBar]] = {}
        meta_by_symbol: dict[str, Any] = {}
        skipped: dict[str, str] = {}

        for raw_symbol in stock_symbols:
            symbol = str(raw_symbol).strip().upper()
            series = self.load_asset_series(symbol)
            if len(series.dates) < min_bars:
                skipped[symbol] = f"too_few_bars:{len(series.dates)}"
                continue
            symbols.append(symbol)
            prices_map[symbol] = list(series.closes)
            dates_map[symbol] = list(series.dates)
            ohlc_map[symbol] = list(series.bars)
            meta_by_symbol[symbol] = dict(series.meta)

        if not symbols:
            raise LiveDataAdapterError(
                "no Live stock series satisfy min_bars"
            )

        indices: dict[str, AssetSeries] = {}
        for raw_symbol in index_symbols:
            symbol = str(raw_symbol).strip().upper()
            path = self._path(symbol)
            if not path.is_file():
                raise LiveDataAdapterError(
                    f"missing required Live index file: {symbol}"
                )
            indices[symbol] = self.load_asset_series(symbol)

        normalized_vix = str(vix_symbol).strip().upper()
        vix_path = self._path(normalized_vix)
        if not vix_path.is_file():
            raise LiveDataAdapterError(
                f"missing required Live VIX file: {normalized_vix}"
            )
        vix = self.load_asset_series(normalized_vix)

        bundle = HistoricalDataBundle(
            symbols=symbols,
            prices_map=prices_map,
            dates_map=dates_map,
            ohlc_map=ohlc_map,
            indices=indices,
            regime_daily=dict(regime_daily),
            vix=vix,
            metadata={
                "mode": "LIVE",
                "source": "LiveDataAdapter",
                "price_root": str(self.price_root),
                "skipped": skipped,
                "meta_by_symbol": meta_by_symbol,
                "index_symbols": sorted(indices),
                "vix_symbol": normalized_vix,
            },
        )

        if hasattr(bundle, "validate_shape"):
            validation = bundle.validate_shape()
            if not isinstance(validation, dict):
                raise LiveDataAdapterError(
                    "HistoricalDataBundle.validate_shape "
                    "must return a report dict"
                )
            if not validation.get("ok", False):
                errors = validation.get("errors", [])
                raise LiveDataAdapterError(
                    "invalid Live HistoricalDataBundle: "
                    + "; ".join(str(item) for item in errors)
                )
        return bundle

    def build_snapshot(
        self,
        *,
        bundle: HistoricalDataBundle,
        market_date: str,
        universe: Optional[Sequence[str]] = None,
    ) -> MarketSnapshot:
        date.fromisoformat(market_date)

        selected = [
            str(symbol).strip().upper()
            for symbol in (
                universe if universe is not None else bundle.symbols
            )
        ]

        prices_by_symbol: dict[str, DailyBar] = {}
        for symbol in selected:
            dates = bundle.dates_map.get(symbol, [])
            if market_date not in dates:
                continue
            index = dates.index(market_date)
            prices_by_symbol[symbol] = bundle.ohlc_map[symbol][index]

        if not prices_by_symbol:
            raise LiveDataAdapterError(
                f"no Live stock bars for {market_date}"
            )

        indices: dict[str, DailyBar] = {}
        for symbol, series in bundle.indices.items():
            if market_date in series.dates:
                index = series.dates.index(market_date)
                indices[symbol] = series.bars[index]

        regime = bundle.regime_daily.get(market_date)
        if regime is None:
            raise LiveDataAdapterError(
                f"standard RegimeRecord missing for {market_date}"
            )

        return MarketSnapshot(
            date=market_date,
            universe=sorted(prices_by_symbol),
            prices_by_symbol=prices_by_symbol,
            indices=indices,
            regime=regime,
            metadata={
                "mode": "LIVE",
                "source": "LiveDataAdapter",
                "price_root": str(self.price_root),
            },
        )
