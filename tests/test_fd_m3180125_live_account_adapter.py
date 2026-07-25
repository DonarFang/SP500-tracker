from datetime import date
from decimal import Decimal

from e1r_engine.live_account import (
    LiveOpeningState,
    rebuild_live_account,
)
from e1r_engine.live_account_adapter import LiveAccountAdapter
from e1r_engine.live_ledger import LiveLedger, TransactionEvent


def test_live_account_adapter_uses_actual_cash_authority() -> None:
    ledger = LiveLedger()
    ledger.append_transaction(
        TransactionEvent(
            event_id="buy-1",
            trade_date=date(2026, 7, 1),
            symbol="AAPL",
            action="BUY",
            price="100",
            shares="10",
        )
    )
    live = rebuild_live_account(
        opening=LiveOpeningState(),
        ledger=ledger,
        marks={"AAPL": Decimal("110")},
    )

    engine = LiveAccountAdapter().to_engine_account(
        live_account=live,
        market_date="2026-07-02",
    )

    assert engine.cash == float(live.actual_cash)
    assert engine.positions["AAPL"].quantity == 10.0
    assert engine.positions["AAPL"].avg_cost == 100.0
    assert engine.open_positions_count == 1
    assert engine.metadata["cash_authority"] == "actual_cash"
