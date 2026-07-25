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
