from datetime import date
from decimal import Decimal
from pathlib import Path

from e1r_engine.live_account import LiveOpeningState
from e1r_engine.live_daily import LiveDailyProcessor
from e1r_engine.live_data import LiveBar, LiveMarketData
from e1r_engine.live_ledger import LiveLedger, TransactionEvent
from e1r_engine.live_recommendation import (
    LiveEngineDecision,
    PositionRecommendation,
    ReferenceCandidate,
)
from e1r_engine.live_repository import LiveDailyRepository


class FakeSharedEngine:
    def __init__(self) -> None:
        self.calls = []

    def decide(self, *, market_date, market_data, account):
        self.calls.append((market_date, account.actual_cash))
        return LiveEngineDecision(
            market_date=market_date,
            regime="UPTREND",
            regime_subclass=None,
            market_state="RISK_ON",
            market_gate="ALLOW",
            entry_capacity=0,
            strategy_branch="UPTREND",
            reference_candidates=(
                ReferenceCandidate(1, "MSFT"),
                ReferenceCandidate(2, "NVDA"),
                ReferenceCandidate(3, "AAPL"),
            ),
            position_recommendations=(
                PositionRecommendation("AAPL", "HOLD", "test"),
            ),
            engine_version="test",
        )


def market_data(close: str = "110") -> LiveMarketData:
    day = date(2026, 7, 27)
    return LiveMarketData(
        market_date=day,
        bars={
            "AAPL": LiveBar.from_mapping(
                "AAPL",
                {
                    "date": day.isoformat(),
                    "open": "105",
                    "high": "112",
                    "low": "103",
                    "close": close,
                    "volume": "1000",
                },
            )
        },
    )


def test_empty_account_daily_processing_is_deterministic() -> None:
    engine = FakeSharedEngine()
    processor = LiveDailyProcessor(engine=engine)
    opening = LiveOpeningState()
    ledger = LiveLedger()

    first = processor.process(
        market_date=date(2026, 7, 27),
        market_data=market_data(),
        opening=opening,
        ledger=ledger,
    )
    second = processor.process(
        market_date=date(2026, 7, 27),
        market_data=market_data(),
        opening=opening,
        ledger=ledger,
    )

    assert first.input_hash == second.input_hash
    assert first.result_hash == second.result_hash
    assert first.account.total_equity == Decimal("100000.00")
    assert len(first.decision.reference_candidates) == 3


def test_mark_to_market_does_not_mutate_account_facts(tmp_path: Path) -> None:
    ledger = LiveLedger()
    ledger.append_transaction(
        TransactionEvent(
            event_id="buy-1",
            trade_date=date(2026, 7, 26),
            symbol="AAPL",
            action="BUY",
            price="100",
            shares="10",
        )
    )

    engine = FakeSharedEngine()
    repo = LiveDailyRepository(tmp_path / "live")
    processor = LiveDailyProcessor(engine=engine, repository=repo)

    result = processor.process(
        market_date=date(2026, 7, 27),
        market_data=market_data("110"),
        opening=LiveOpeningState(),
        ledger=ledger,
    )

    position = result.account.positions["AAPL"]
    assert position.shares == Decimal("10")
    assert position.average_cost == Decimal("100")
    assert result.account.actual_cash == Decimal("99000.00")
    assert result.account.calculated_cash == Decimal("99000.00")
    assert result.account.unrealized_pnl == Decimal("100")
    assert result.account.positions_value == Decimal("1100")
    assert result.account.total_equity == Decimal("100100.00")

    payload = result.to_payload()
    assert payload["reference_top3"] == [
        {"rank": 1, "symbol": "MSFT"},
        {"rank": 2, "symbol": "NVDA"},
        {"rank": 3, "symbol": "AAPL"},
    ]
    assert payload["position_recommendations"][0]["action"] == "HOLD"
