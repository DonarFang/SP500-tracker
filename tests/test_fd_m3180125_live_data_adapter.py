from pathlib import Path
import json

import pytest

from e1r_engine.adapters.live_data import (
    LiveDataAdapter,
    LiveDataAdapterError,
)
from e1r_engine.contracts import RegimeRecord


def write_series(root: Path, symbol: str) -> None:
    rows = []
    for day in range(1, 4):
        rows.append(
            {
                "date": f"2026-07-0{day}",
                "open": 100 + day,
                "high": 102 + day,
                "low": 99 + day,
                "close": 101 + day,
                "volume": 1000,
            }
        )
    (root / f"{symbol}.json").write_text(
        json.dumps(rows),
        encoding="utf-8",
    )


def test_live_data_adapter_requires_live_prices_root(tmp_path: Path) -> None:
    with pytest.raises(LiveDataAdapterError):
        LiveDataAdapter(tmp_path / "fw_prices")


def test_live_data_adapter_builds_standard_snapshot(tmp_path: Path) -> None:
    root = tmp_path / "live_prices"
    root.mkdir()
    write_series(root, "AAPL")
    write_series(root, "SPX")
    write_series(root, "NDX")
    write_series(root, "SOX")
    write_series(root, "VIX")

    regime = RegimeRecord(
        date="2026-07-03",
        spx_regime="UPTREND",
        subclass=None,
    )
    adapter = LiveDataAdapter(root)
    bundle = adapter.load_bundle(
        stock_symbols=["AAPL"],
        index_symbols=["SPX", "NDX", "SOX"],
        regime_daily={"2026-07-03": regime},
        min_bars=3,
    )
    snapshot = adapter.build_snapshot(
        bundle=bundle,
        market_date="2026-07-03",
    )

    assert snapshot.date == "2026-07-03"
    assert list(snapshot.universe) == ["AAPL"]
    assert snapshot.prices_by_symbol["AAPL"].close == 104.0
    assert snapshot.indices["SPX"].close == 104.0
    assert snapshot.indices["NDX"].close == 104.0
    assert snapshot.indices["SOX"].close == 104.0
    assert bundle.vix.symbol == "VIX"
    assert bundle.vix.closes[-1] == 104.0
    assert sorted(bundle.indices) == ["NDX", "SOX", "SPX"]
    assert snapshot.regime.spx_regime == "UPTREND"
    assert snapshot.metadata["source"] == "LiveDataAdapter"
