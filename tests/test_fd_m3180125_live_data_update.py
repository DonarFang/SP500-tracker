from datetime import date, datetime, timezone
import json
from pathlib import Path

from e1r_engine.live_data_update import (
    LiveDataUpdater,
    REQUIRED_INDEX_PROVIDER_SYMBOLS,
)


def row(day: str, close: str = "100"):
    return {
        "date": day,
        "open": close,
        "high": str(float(close) + 1),
        "low": str(float(close) - 1),
        "close": close,
        "volume": "1000",
    }


class Provider:
    def __init__(self, payloads):
        self.payloads = payloads
        self.calls = []

    def fetch(
        self,
        *,
        provider_symbol,
        start_date,
        end_date,
    ):
        self.calls.append(
            (provider_symbol, start_date, end_date)
        )
        return self.payloads.get(provider_symbol, [])


def seed_catalogue(root: Path) -> None:
    root.mkdir()
    symbols = [
        "AAPL",
        "SPX",
        "NDX",
        "SOX",
        "VIX",
    ]
    for symbol in symbols:
        (root / f"{symbol}.json").write_text(
            json.dumps([row("2026-07-23")]),
            encoding="utf-8",
        )


def test_updater_uses_independent_catalogue_and_canonical_indices(
    tmp_path: Path,
) -> None:
    root = tmp_path / "live_prices"
    seed_catalogue(root)

    payloads = {
        "AAPL": [row("2026-07-24", "101")],
        "^GSPC": [row("2026-07-24", "201")],
        "^NDX": [row("2026-07-24", "301")],
        "^SOX": [row("2026-07-24", "401")],
        "^VIX": [row("2026-07-24", "21")],
    }
    provider = Provider(payloads)
    status = tmp_path / "live" / "automation" / "current_data_update.json"

    result = LiveDataUpdater(
        price_root=root,
        status_path=status,
        provider=provider,
        source_commit="abc123",
    ).update(
        expected_latest_market_date=date(2026, 7, 24),
        now=datetime(
            2026, 7, 25, 1, 0, tzinfo=timezone.utc
        ),
    )

    assert result.data_status == "CURRENT"
    assert result.catalogue_changed is False
    assert result.latest_market_date == "2026-07-24"
    assert result.updated_symbol_count == 5
    assert result.unavailable_symbols == ()
    assert {
        call[0] for call in provider.calls
    } == {
        "AAPL",
        "^GSPC",
        "^NDX",
        "^SOX",
        "^VIX",
    }
    assert sorted(path.stem for path in root.glob("*.json")) == [
        "AAPL",
        "NDX",
        "SOX",
        "SPX",
        "VIX",
    ]


def test_updater_is_idempotent_by_symbol_and_date(
    tmp_path: Path,
) -> None:
    root = tmp_path / "live_prices"
    seed_catalogue(root)

    payloads = {
        "AAPL": [row("2026-07-24", "101")],
        "^GSPC": [row("2026-07-24", "201")],
        "^NDX": [row("2026-07-24", "301")],
        "^SOX": [row("2026-07-24", "401")],
        "^VIX": [row("2026-07-24", "21")],
    }
    provider = Provider(payloads)
    updater = LiveDataUpdater(
        price_root=root,
        status_path=tmp_path / "live" / "automation" / "current_data_update.json",
        provider=provider,
        source_commit="abc123",
    )

    first = updater.update(
        expected_latest_market_date=date(2026, 7, 24),
        now=datetime(
            2026, 7, 25, 1, 0, tzinfo=timezone.utc
        ),
    )
    second = updater.update(
        expected_latest_market_date=date(2026, 7, 24),
        now=datetime(
            2026, 7, 25, 1, 1, tzinfo=timezone.utc
        ),
    )

    assert first.updated_symbol_count == 5
    assert second.updated_symbol_count == 0
    assert second.unchanged_symbol_count == 5
    for path in root.glob("*.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        dates = [item["date"] for item in payload]
        assert dates == sorted(set(dates))


def test_required_index_unavailable_blocks_current_status(
    tmp_path: Path,
) -> None:
    root = tmp_path / "live_prices"
    seed_catalogue(root)

    payloads = {
        "AAPL": [row("2026-07-24", "101")],
        "^GSPC": [row("2026-07-24", "201")],
        "^NDX": [row("2026-07-24", "301")],
        "^SOX": [row("2026-07-24", "401")],
    }
    provider = Provider(payloads)

    result = LiveDataUpdater(
        price_root=root,
        status_path=tmp_path / "live" / "automation" / "current_data_update.json",
        provider=provider,
        source_commit="abc123",
    ).update(
        expected_latest_market_date=date(2026, 7, 24),
        now=datetime(
            2026, 7, 25, 1, 0, tzinfo=timezone.utc
        ),
    )

    assert result.data_status in {"PARTIAL", "STALE"}
    assert result.latest_market_date == "2026-07-23"
    assert "2026-07-24" in result.missing_dates


def test_live_updater_accepts_source_equivalent_ohlc_rounding_crosses() -> None:
    from e1r_engine.live_data_update import _normalize_row

    low_cross = _normalize_row(
        {
            "date": "2026-07-24",
            "open": "100.00",
            "high": "101.00",
            "low": "100.01",
            "close": "100.00",
            "volume": "1000",
        }
    )
    high_cross = _normalize_row(
        {
            "date": "2026-07-25",
            "open": "100.01",
            "high": "100.00",
            "low": "99.00",
            "close": "100.01",
            "volume": "1000",
        }
    )

    assert low_cross["low"] == "100.01"
    assert high_cross["high"] == "100.00"
