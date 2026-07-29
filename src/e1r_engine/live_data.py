"""Independent Live market-data contract.

The repository root is explicitly supplied by the Live composition. This
module never discovers or falls back to 5Y or Engine Forward data.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
from typing import Iterable, Mapping


class LiveDataError(ValueError):
    """Raised when independent Live market data is invalid or incomplete."""


def _decimal(value: object, field: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise LiveDataError(f"{field} must be a valid decimal") from exc
    if not result.is_finite():
        raise LiveDataError(f"{field} must be finite")
    return result


@dataclass(frozen=True)
class LiveBar:
    symbol: str
    market_date: date
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal

    @classmethod
    def from_mapping(cls, symbol: str, row: Mapping[str, object]) -> "LiveBar":
        try:
            market_date = date.fromisoformat(str(row["date"]))
        except (KeyError, ValueError) as exc:
            raise LiveDataError("bar date must be ISO YYYY-MM-DD") from exc

        normalized = str(symbol).strip().upper()
        if not normalized:
            raise LiveDataError("symbol is required")

        open_price = _decimal(row.get("open"), "open")
        high = _decimal(row.get("high"), "high")
        low = _decimal(row.get("low"), "low")
        close = _decimal(row.get("close"), "close")
        volume = _decimal(row.get("volume"), "volume")

        if min(open_price, high, low, close) <= 0:
            raise LiveDataError("OHLC prices must be greater than zero")
        if volume < 0:
            raise LiveDataError("volume must not be negative")

        return cls(
            symbol=normalized,
            market_date=market_date,
            open=open_price,
            high=high,
            low=low,
            close=close,
            volume=volume,
        )


@dataclass(frozen=True)
class LiveMarketData:
    market_date: date
    bars: Mapping[str, LiveBar]

    def __post_init__(self) -> None:
        normalized = {str(k).upper(): v for k, v in self.bars.items()}
        if not normalized:
            raise LiveDataError("at least one Live bar is required")
        for symbol, bar in normalized.items():
            if symbol != bar.symbol:
                raise LiveDataError(f"bar key mismatch for {symbol}")
            if bar.market_date != self.market_date:
                raise LiveDataError(f"bar date mismatch for {symbol}")
        object.__setattr__(self, "bars", normalized)

    @property
    def close_marks(self) -> dict[str, Decimal]:
        return {symbol: bar.close for symbol, bar in self.bars.items()}

    def require_symbols(self, symbols: Iterable[str]) -> None:
        missing = sorted(
            {str(symbol).strip().upper() for symbol in symbols}
            - set(self.bars)
        )
        if missing:
            raise LiveDataError(
                "missing required Live symbols: " + ",".join(missing)
            )


class LivePriceRepository:
    """Reads only the explicitly supplied independent Live price root."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        if self.root.name != "live_prices":
            raise LiveDataError(
                "Live price repository root must be named live_prices"
            )

    def load_date(
        self,
        market_date: date,
        symbols: Iterable[str],
    ) -> LiveMarketData:
        bars: dict[str, LiveBar] = {}

        for raw_symbol in symbols:
            symbol = str(raw_symbol).strip().upper()
            path = self.root / f"{symbol}.json"
            if not path.is_file():
                raise LiveDataError(f"missing Live price file: {symbol}")

            payload = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(payload, list):
                raise LiveDataError(f"{symbol} price payload must be a list")

            matches = [
                row
                for row in payload
                if isinstance(row, dict)
                and str(row.get("date")) == market_date.isoformat()
            ]

            if len(matches) != 1:
                raise LiveDataError(
                    f"{symbol} requires exactly one row for {market_date}"
                )
            bars[symbol] = LiveBar.from_mapping(symbol, matches[0])

        return LiveMarketData(market_date=market_date, bars=bars)
