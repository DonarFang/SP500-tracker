from datetime import date
from decimal import Decimal

import pytest

from e1r_engine.live_ledger import (
    CashControlEvent,
    DuplicateEventConflict,
    LiveLedger,
    LiveLedgerError,
    ManualAction,
    TransactionEvent,
)


def test_two_ledgers_preserve_one_global_sequence() -> None:
    ledger = LiveLedger()

    buy = TransactionEvent(
        event_id="tx-1",
        trade_date=date(2026, 7, 27),
        symbol="aapl",
        action="BUY",
        price="100",
        shares="10",
    )
    cash = CashControlEvent(
        event_id="cash-1",
        effective_date=date(2026, 7, 27),
        actual_cash="99000",
        notes="user confirmed cash",
    )

    assert ledger.append_transaction(buy) is True
    assert ledger.append_cash_control(cash) is True

    journal = list(ledger.iter_journal())
    assert [item.sequence for item in journal] == [1, 2]
    assert [item.ledger for item in journal] == [
        "TRANSACTION",
        "CASH_CONTROL",
    ]
    assert ledger.transactions == (buy,)
    assert ledger.cash_controls == (cash,)


def test_same_event_id_same_payload_is_idempotent() -> None:
    ledger = LiveLedger()
    event = TransactionEvent(
        event_id="tx-1",
        trade_date=date(2026, 7, 27),
        symbol="AAPL",
        action=ManualAction.BUY,
        price=Decimal("100"),
        shares=Decimal("10"),
    )

    assert ledger.append_transaction(event) is True
    assert ledger.append_transaction(event) is False
    assert len(ledger) == 1


def test_same_event_id_different_payload_is_conflict() -> None:
    ledger = LiveLedger()
    ledger.append_transaction(
        TransactionEvent(
            event_id="tx-1",
            trade_date=date(2026, 7, 27),
            symbol="AAPL",
            action="BUY",
            price="100",
            shares="10",
        )
    )

    with pytest.raises(DuplicateEventConflict):
        ledger.append_transaction(
            TransactionEvent(
                event_id="tx-1",
                trade_date=date(2026, 7, 27),
                symbol="AAPL",
                action="BUY",
                price="101",
                shares="10",
            )
        )


def test_exit_must_not_accept_shares() -> None:
    with pytest.raises(LiveLedgerError, match="EXIT must not provide shares"):
        TransactionEvent(
            event_id="tx-exit",
            trade_date=date(2026, 7, 27),
            symbol="AAPL",
            action="EXIT",
            price="110",
            shares="10",
        )


@pytest.mark.parametrize("action", ["BUY", "ADD", "REDUCE"])
def test_non_exit_actions_require_positive_shares(action: str) -> None:
    with pytest.raises(LiveLedgerError):
        TransactionEvent(
            event_id=f"tx-{action.lower()}",
            trade_date=date(2026, 7, 27),
            symbol="AAPL",
            action=action,
            price="100",
            shares=None,
        )
