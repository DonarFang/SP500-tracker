from datetime import date, timedelta
import inspect
import json
from pathlib import Path

import pytest

from e1r_engine.adapters.live_data import (
    LiveDataAdapter,
    LiveDataAdapterError,
)


def write_series(
    root: Path,
    symbol: str,
    *,
    days: int = 500,
    slope: float = 0.1,
) -> str:
    start = date(2025, 1, 1)
    rows = []

    for index in range(days):
        day = start + timedelta(
            days=index
        )
        base = 100.0 + slope * index

        rows.append(
            {
                "date": day.isoformat(),
                "open": base,
                "high": base + 1.0,
                "low": base - 1.0,
                "close": base,
                "volume": 1000,
            }
        )

    (root / f"{symbol}.json").write_text(
        json.dumps(rows),
        encoding="utf-8",
    )

    return rows[-1]["date"]


def seed_live_prices(
    root: Path,
) -> str:
    root.mkdir()

    market_date = write_series(
        root,
        "SPX",
        slope=0.2,
    )
    write_series(
        root,
        "NDX",
        slope=0.22,
    )
    write_series(
        root,
        "SOX",
        slope=0.25,
    )
    write_series(
        root,
        "VIX",
        slope=0.01,
    )
    write_series(
        root,
        "AAPL",
        slope=0.15,
    )

    return market_date


def test_live_data_adapter_requires_live_prices_root(
    tmp_path: Path,
) -> None:
    with pytest.raises(
        LiveDataAdapterError
    ):
        LiveDataAdapter(
            tmp_path / "fw_prices"
        )


def test_live_data_adapter_accepts_no_regime_input(
    tmp_path: Path,
) -> None:
    root = tmp_path / "live_prices"
    seed_live_prices(root)

    adapter = LiveDataAdapter(root)
    signature = inspect.signature(
        adapter.load_bundle
    )

    assert "regime_daily" not in (
        signature.parameters
    )

    bundle = adapter.load_bundle(
        stock_symbols=("AAPL",),
        min_bars=120,
    )

    assert bundle.symbols == ["AAPL"]
    assert sorted(bundle.indices) == [
        "NDX",
        "SOX",
        "SPX",
    ]
    assert bundle.vix.symbol == "VIX"
    assert bundle.regime_daily == {}
    assert (
        bundle.metadata[
            "regime_logic_performed"
        ]
        is False
    )
    assert (
        bundle.metadata[
            "strategy_logic_performed"
        ]
        is False
    )
