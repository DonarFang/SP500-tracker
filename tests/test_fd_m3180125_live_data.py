from datetime import date
import json
from pathlib import Path

import pytest

from e1r_engine.live_data import (
    LiveBar,
    LiveDataError,
    LivePriceRepository,
)


def test_live_bar_validates_ohlcv() -> None:
    bar = LiveBar.from_mapping(
        "aapl",
        {
            "date": "2026-07-27",
            "open": 100,
            "high": 110,
            "low": 95,
            "close": 105,
            "volume": 1000,
        },
    )
    assert bar.symbol == "AAPL"
    assert str(bar.close) == "105"


def test_live_price_repository_requires_live_prices_root(tmp_path: Path) -> None:
    with pytest.raises(LiveDataError):
        LivePriceRepository(tmp_path / "fw_prices")


def test_live_price_repository_loads_exact_date(tmp_path: Path) -> None:
    root = tmp_path / "live_prices"
    root.mkdir()
    (root / "AAPL.json").write_text(
        json.dumps(
            [
                {
                    "date": "2026-07-27",
                    "open": 100,
                    "high": 110,
                    "low": 95,
                    "close": 105,
                    "volume": 1000,
                }
            ]
        ),
        encoding="utf-8",
    )
    data = LivePriceRepository(root).load_date(
        date(2026, 7, 27),
        ["AAPL"],
    )
    assert str(data.close_marks["AAPL"]) == "105"



def test_live_bar_accepts_source_equivalent_ohlc_rounding_crosses() -> None:
    low_cross = LiveBar.from_mapping(
        "LOWX",
        {
            "date": "2026-07-28",
            "open": "100.00",
            "high": "100.02",
            "low": "100.01",
            "close": "100.00",
            "volume": "1000",
        },
    )
    high_cross = LiveBar.from_mapping(
        "HIGHX",
        {
            "date": "2026-07-28",
            "open": "100.01",
            "high": "100.00",
            "low": "99.99",
            "close": "100.01",
            "volume": "1000",
        },
    )

    assert str(low_cross.low) == "100.01"
    assert str(high_cross.high) == "100.00"
