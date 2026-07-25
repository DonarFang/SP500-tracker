"""Independent Daily OHLCV updater for `data/live_prices`.

The updater owns only Live market data and freshness state. It does not
run the Engine, read Forward/5Y state, alter the catalogue, or activate
the Live opening date.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol, Sequence


class LiveDataUpdateError(ValueError):
    pass


REQUIRED_INDEX_PROVIDER_SYMBOLS = {
    "SPX": "^GSPC",
    "NDX": "^NDX",
    "SOX": "^SOX",
    "VIX": "^VIX",
}

FROZEN_DATA_STATUSES = frozenset(
    {"CURRENT", "STALE", "PARTIAL", "FAILED"}
)


def _decimal_text(value: object, field: str) -> str:
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise LiveDataUpdateError(
            f"{field} must be numeric"
        ) from exc
    if not parsed.is_finite():
        raise LiveDataUpdateError(
            f"{field} must be finite"
        )
    return format(parsed, "f")


def _normalize_row(row: Mapping[str, object]) -> dict[str, object]:
    try:
        market_date = date.fromisoformat(str(row["date"]))
    except (KeyError, ValueError) as exc:
        raise LiveDataUpdateError(
            "row date must be ISO YYYY-MM-DD"
        ) from exc

    normalized = {
        "date": market_date.isoformat(),
        "open": _decimal_text(row.get("open"), "open"),
        "high": _decimal_text(row.get("high"), "high"),
        "low": _decimal_text(row.get("low"), "low"),
        "close": _decimal_text(row.get("close"), "close"),
        "volume": _decimal_text(row.get("volume", 0), "volume"),
    }

    open_price = Decimal(str(normalized["open"]))
    high = Decimal(str(normalized["high"]))
    low = Decimal(str(normalized["low"]))
    close = Decimal(str(normalized["close"]))
    volume = Decimal(str(normalized["volume"]))

    if min(open_price, high, low, close) <= 0:
        raise LiveDataUpdateError(
            "OHLC values must be positive"
        )
    if volume < 0:
        raise LiveDataUpdateError(
            "volume must not be negative"
        )
    if high < max(open_price, low, close):
        raise LiveDataUpdateError(
            "high is below another OHLC value"
        )
    if low > min(open_price, high, close):
        raise LiveDataUpdateError(
            "low is above another OHLC value"
        )

    return normalized


class DailyPriceProvider(Protocol):
    def fetch(
        self,
        *,
        provider_symbol: str,
        start_date: date,
        end_date: date,
    ) -> Sequence[Mapping[str, object]]:
        """Return Daily bars in [start_date, end_date]."""


@dataclass(frozen=True)
class LiveDataUpdateResult:
    latest_market_date: str | None
    last_successful_update_at: str | None
    expected_latest_market_date: str
    missing_dates: tuple[str, ...]
    updated_symbol_count: int
    unchanged_symbol_count: int
    unavailable_symbols: tuple[str, ...]
    catalogue_changed: bool
    data_status: str
    symbol_count: int
    changed_files: tuple[str, ...]
    source_commit: str

    def to_payload(self) -> dict[str, object]:
        return {
            "latest_market_date": self.latest_market_date,
            "last_successful_update_at": (
                self.last_successful_update_at
            ),
            "expected_latest_market_date": (
                self.expected_latest_market_date
            ),
            "missing_dates": list(self.missing_dates),
            "updated_symbol_count": self.updated_symbol_count,
            "unchanged_symbol_count": self.unchanged_symbol_count,
            "unavailable_symbols": list(
                self.unavailable_symbols
            ),
            "catalogue_changed": self.catalogue_changed,
            "data_status": self.data_status,
            "symbol_count": self.symbol_count,
            "changed_files": list(self.changed_files),
            "source_commit": self.source_commit,
        }


class LiveDataUpdater:
    def __init__(
        self,
        *,
        price_root: Path,
        status_path: Path,
        provider: DailyPriceProvider,
        source_commit: str,
        lookback_days: int = 7,
    ) -> None:
        self.price_root = Path(price_root)
        self.status_path = Path(status_path)
        self.provider = provider
        self.source_commit = str(source_commit)
        self.lookback_days = int(lookback_days)

        if self.price_root.name != "live_prices":
            raise LiveDataUpdateError(
                "Live price root must be named live_prices"
            )
        if self.lookback_days < 1:
            raise LiveDataUpdateError(
                "lookback_days must be positive"
            )

    def _read_rows(self, symbol: str) -> list[dict[str, object]]:
        path = self.price_root / f"{symbol}.json"
        if not path.exists():
            return []
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise LiveDataUpdateError(
                f"{symbol} file must contain a list"
            )
        rows = [_normalize_row(row) for row in payload]
        dates = [str(row["date"]) for row in rows]
        if dates != sorted(dates):
            raise LiveDataUpdateError(
                f"{symbol} dates must be ascending"
            )
        if len(dates) != len(set(dates)):
            raise LiveDataUpdateError(
                f"{symbol} contains duplicate dates"
            )
        return rows

    def _write_rows(
        self,
        symbol: str,
        rows: Sequence[Mapping[str, object]],
    ) -> bool:
        path = self.price_root / f"{symbol}.json"
        normalized = [_normalize_row(row) for row in rows]
        normalized = sorted(
            normalized,
            key=lambda item: str(item["date"]),
        )
        body = (
            json.dumps(
                normalized,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")

        if path.exists() and path.read_bytes() == body:
            return False

        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(".json.tmp")
        temporary.write_bytes(body)
        os.replace(temporary, path)
        return True

    def _load_catalogue(self) -> tuple[str, ...]:
        files = sorted(self.price_root.glob("*.json"))
        symbols = tuple(path.stem.upper() for path in files)
        if not symbols:
            raise LiveDataUpdateError(
                "data/live_prices catalogue is empty"
            )
        required = set(REQUIRED_INDEX_PROVIDER_SYMBOLS)
        missing = sorted(required - set(symbols))
        if missing:
            raise LiveDataUpdateError(
                "required Live index files missing: "
                + ", ".join(missing)
            )
        return symbols

    def _provider_symbol(self, symbol: str) -> str:
        return REQUIRED_INDEX_PROVIDER_SYMBOLS.get(
            symbol,
            symbol,
        )

    def update(
        self,
        *,
        expected_latest_market_date: date,
        now: datetime | None = None,
    ) -> LiveDataUpdateResult:
        timestamp = now or datetime.now(timezone.utc)
        if timestamp.tzinfo is None:
            raise LiveDataUpdateError(
                "now must be timezone-aware"
            )

        catalogue_before = self._load_catalogue()
        unavailable = []
        changed_files = []
        unchanged_count = 0

        for symbol in catalogue_before:
            existing = self._read_rows(symbol)
            existing_by_date = {
                str(row["date"]): row
                for row in existing
            }

            if existing:
                latest_existing = date.fromisoformat(
                    str(existing[-1]["date"])
                )
                fetch_start = latest_existing - timedelta(
                    days=self.lookback_days
                )
            else:
                fetch_start = (
                    expected_latest_market_date
                    - timedelta(days=self.lookback_days)
                )

            try:
                fetched = self.provider.fetch(
                    provider_symbol=self._provider_symbol(symbol),
                    start_date=fetch_start,
                    end_date=expected_latest_market_date,
                )
            except Exception:
                unavailable.append(symbol)
                continue

            for row in fetched:
                normalized = _normalize_row(row)
                row_date = date.fromisoformat(
                    str(normalized["date"])
                )
                if fetch_start <= row_date <= expected_latest_market_date:
                    existing_by_date[
                        str(normalized["date"])
                    ] = normalized

            merged = [
                existing_by_date[item]
                for item in sorted(existing_by_date)
            ]
            if self._write_rows(symbol, merged):
                changed_files.append(
                    str(self.price_root / f"{symbol}.json")
                )
            else:
                unchanged_count += 1

        catalogue_after = self._load_catalogue()
        catalogue_changed = catalogue_after != catalogue_before

        latest_by_symbol: dict[str, str] = {}
        for symbol in catalogue_after:
            rows = self._read_rows(symbol)
            if rows:
                latest_by_symbol[symbol] = str(
                    rows[-1]["date"]
                )

        required_latest = [
            latest_by_symbol.get(symbol)
            for symbol in REQUIRED_INDEX_PROVIDER_SYMBOLS
        ]
        complete_required = all(required_latest)

        latest_market_date = (
            min(str(value) for value in required_latest)
            if complete_required
            else None
        )

        expected_text = expected_latest_market_date.isoformat()
        missing_dates = []
        if (
            latest_market_date is None
            or latest_market_date < expected_text
        ):
            missing_dates.append(expected_text)

        if catalogue_changed:
            data_status = "FAILED"
        elif not complete_required:
            data_status = "FAILED"
        elif unavailable:
            data_status = "PARTIAL"
        elif latest_market_date < expected_text:
            data_status = "STALE"
        else:
            data_status = "CURRENT"

        successful_at = (
            timestamp.isoformat()
            if data_status == "CURRENT"
            else None
        )

        result = LiveDataUpdateResult(
            latest_market_date=latest_market_date,
            last_successful_update_at=successful_at,
            expected_latest_market_date=expected_text,
            missing_dates=tuple(missing_dates),
            updated_symbol_count=len(changed_files),
            unchanged_symbol_count=unchanged_count,
            unavailable_symbols=tuple(sorted(unavailable)),
            catalogue_changed=catalogue_changed,
            data_status=data_status,
            symbol_count=len(catalogue_after),
            changed_files=tuple(sorted(changed_files)),
            source_commit=self.source_commit,
        )

        self.status_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        body = (
            json.dumps(
                result.to_payload(),
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
        temporary = self.status_path.with_suffix(
            self.status_path.suffix + ".tmp"
        )
        temporary.write_bytes(body)
        os.replace(temporary, self.status_path)

        return result
