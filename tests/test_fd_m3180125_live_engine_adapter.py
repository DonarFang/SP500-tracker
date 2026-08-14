from datetime import date, timedelta
import inspect
import json
from pathlib import Path

from e1r_engine.adapters.live_data import (
    LiveDataAdapter,
)
from e1r_engine.live_account import (
    LiveOpeningState,
    rebuild_live_account,
)
from e1r_engine.live_data import (
    LiveBar,
    LiveMarketData,
)
from e1r_engine.live_engine_adapter import (
    LiveEngineAdapter,
)
from e1r_engine.live_ledger import (
    LiveLedger,
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


def test_live_data_enters_existing_engine_without_provider(
    tmp_path: Path,
) -> None:
    root = tmp_path / "live_prices"
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

    day = date.fromisoformat(
        market_date
    )

    market_data = LiveMarketData(
        market_date=day,
        bars={
            "AAPL": LiveBar.from_mapping(
                "AAPL",
                {
                    "date": market_date,
                    "open": 174.85,
                    "high": 175.85,
                    "low": 173.85,
                    "close": 174.85,
                    "volume": 1000,
                },
            )
        },
    )

    account = rebuild_live_account(
        opening=LiveOpeningState(),
        ledger=LiveLedger(),
    )

    signature = inspect.signature(
        LiveEngineAdapter
    )

    assert "input_provider" not in (
        signature.parameters
    )

    decision = LiveEngineAdapter(
        data_adapter=LiveDataAdapter(root),
        stock_symbols=("AAPL",),
        min_bars=120,
    ).decide(
        market_date=day,
        market_data=market_data,
        account=account,
    )

    assert decision.market_date == day
    assert decision.regime in {
        "UPTREND",
        "SIDEWAYS",
        "DOWNTREND",
        "UNCLASSIFIED",
    }
    assert (
        decision.evidence[
            "engine_entry"
        ]
        == "E1RCoreEngine.step"
    )
    assert (
        decision.evidence[
            "regime_source"
        ]
        == "engine://canonical_regime"
    )
    assert (
        decision.evidence[
            "external_regime_injected"
        ]
        is False
    )
    assert (
        decision.evidence[
            "provider_abstraction_used"
        ]
        is False
    )
    assert (
        decision.evidence[
            "strategy_logic_reimplemented"
        ]
        is False
    )
    assert decision.regime == "UPTREND"
    assert [
        (item.rank, item.symbol)
        for item in decision.reference_candidates
    ] == [(1, "AAPL")]
    assert [
        (item.symbol, item.action)
        for item in decision.position_recommendations
    ] == [("AAPL", "BUY")]
    assert (
        decision.evidence[
            "reference_ranking_source"
        ]
        == "UptrendSignalAdapter.leader_rank_all"
    )
    assert (
        decision.evidence[
            "reference_ranking_account_independent"
        ]
        is True
    )
    assert (
        decision.evidence[
            "reference_ranking_buy_independent"
        ]
        is True
    )


def test_unsupported_live_provider_types_are_absent() -> None:
    import e1r_engine.live_engine_adapter as module

    assert not hasattr(
        module,
        "LiveFormalInputProvider",
    )
    assert not hasattr(
        module,
        "LivePreparedEngineInputs",
    )
