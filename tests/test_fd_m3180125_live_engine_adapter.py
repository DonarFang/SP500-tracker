from dataclasses import dataclass
from datetime import date
from pathlib import Path
import json

from e1r_engine.adapters.live_data import LiveDataAdapter
from e1r_engine.contracts import RegimeRecord
from e1r_engine.live_account import LiveOpeningState, rebuild_live_account
from e1r_engine.live_data import LiveBar, LiveMarketData
from e1r_engine.live_engine_adapter import (
    LiveEngineAdapter,
    LivePreparedEngineInputs,
)
from e1r_engine.live_ledger import LiveLedger


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


class Provider:
    def prepare(
        self,
        *,
        market_date,
        market_data,
        live_account,
        data_adapter,
    ):
        regime = RegimeRecord(
            date=market_date,
            spx_regime="DOWNTREND",
            subclass=None,
        )
        bundle = data_adapter.load_bundle(
            stock_symbols=["AAPL"],
            index_symbols=["SPX", "NDX", "SOX"],
            regime_daily={market_date: regime},
            min_bars=3,
        )
        return LivePreparedEngineInputs(
            bundle=bundle,
            stock_symbols=("AAPL",),
            reference_symbols=(),
        )


def test_live_engine_adapter_calls_real_engine_step(tmp_path: Path) -> None:
    root = tmp_path / "live_prices"
    root.mkdir()
    write_series(root, "AAPL")
    write_series(root, "SPX")
    write_series(root, "NDX")
    write_series(root, "SOX")
    write_series(root, "VIX")

    day = date(2026, 7, 3)
    market_data = LiveMarketData(
        market_date=day,
        bars={
            "AAPL": LiveBar.from_mapping(
                "AAPL",
                {
                    "date": day.isoformat(),
                    "open": 103,
                    "high": 105,
                    "low": 102,
                    "close": 104,
                    "volume": 1000,
                },
            )
        },
    )
    account = rebuild_live_account(
        opening=LiveOpeningState(),
        ledger=LiveLedger(),
    )

    decision = LiveEngineAdapter(
        data_adapter=LiveDataAdapter(root),
        input_provider=Provider(),
    ).decide(
        market_date=day,
        market_data=market_data,
        account=account,
    )

    assert decision.market_date == day
    assert decision.regime == "DOWNTREND"
    assert decision.strategy_branch == "DOWNTREND"
    assert decision.reference_candidates == ()
    assert (
        decision.evidence["engine_entry"]
        == "E1RCoreEngine.step"
    )
    assert (
        decision.evidence["strategy_logic_reimplemented"]
        is False
    )
