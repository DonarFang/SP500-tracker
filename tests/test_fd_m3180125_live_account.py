from datetime import date
from decimal import Decimal
from typing import Optional

import pytest

from e1r_engine.live_account import (
    CashRuleViolation,
    LiveOpeningState,
    PositionRuleViolation,
    rebuild_live_account,
)
from e1r_engine.live_ledger import CashControlEvent, LiveLedger, TransactionEvent


D = Decimal


def tx(
    event_id: str,
    symbol: str,
    action: str,
    price: str,
    shares: Optional[str] = None,
) -> TransactionEvent:
    return TransactionEvent(
        event_id=event_id,
        trade_date=date(2026, 7, 27),
        symbol=symbol,
        action=action,
        price=price,
        shares=shares,
    )


def test_empty_account_initializes_at_frozen_opening_cash() -> None:
    state = rebuild_live_account(
        opening=LiveOpeningState(),
        ledger=LiveLedger(),
    )

    assert state.opening_cash == D("100000.00")
    assert state.actual_cash == D("100000.00")
    assert state.calculated_cash == D("100000.00")
    assert state.cash_difference == D("0")
    assert state.positions == {}
    assert state.trading_pnl == D("0")
    assert state.net_cash_adjustment == D("0")
    assert state.total_equity == D("100000.00")


def test_buy_add_reduce_exit_accounting() -> None:
    ledger = LiveLedger()
    ledger.append_transaction(tx("1", "AAPL", "BUY", "100", "10"))
    ledger.append_transaction(tx("2", "AAPL", "ADD", "120", "10"))
    ledger.append_transaction(tx("3", "AAPL", "REDUCE", "130", "5"))
    ledger.append_transaction(tx("4", "AAPL", "EXIT", "140"))

    state = rebuild_live_account(
        opening=LiveOpeningState(),
        ledger=ledger,
    )

    # Reconciliation:
    # BUY 10@100 + ADD 10@120 => 20 shares at average cost 110.
    # REDUCE 5@130 => realized P&L 100, 15 shares remain.
    # EXIT 15@140 => realized P&L 450.
    # Total realized P&L and final cash increase are therefore 550.
    assert state.positions == {}
    assert state.realized_pnl == D("550")
    assert state.unrealized_pnl == D("0")
    assert state.trading_pnl == D("550")
    assert state.actual_cash == D("100550.00")
    assert state.calculated_cash == D("100550.00")
    assert state.total_equity == D("100550.00")
    assert state.applied_transactions[2].realized_pnl == D("100")
    assert state.applied_transactions[3].realized_pnl == D("450")
    assert state.applied_transactions[-1].effective_shares == D("15")


def test_cash_control_is_authoritative_and_excluded_from_trading_pnl() -> None:
    ledger = LiveLedger()
    ledger.append_transaction(tx("1", "AAPL", "BUY", "100", "10"))
    ledger.append_cash_control(
        CashControlEvent(
            event_id="cash-1",
            effective_date=date(2026, 7, 27),
            actual_cash="95000",
            notes="user confirmed actual cash",
        )
    )

    state = rebuild_live_account(
        opening=LiveOpeningState(),
        ledger=ledger,
        marks={"AAPL": "110"},
    )

    assert state.calculated_cash == D("99000.00")
    assert state.actual_cash == D("95000")
    assert state.cash_difference == D("-4000.00")
    assert state.net_cash_adjustment == D("-4000.00")
    assert state.unrealized_pnl == D("100")
    assert state.trading_pnl == D("100")
    assert state.positions_value == D("1100")
    assert state.total_equity == D("96100")


def test_cash_difference_survives_later_transactions() -> None:
    ledger = LiveLedger()
    ledger.append_cash_control(
        CashControlEvent(
            event_id="cash-1",
            effective_date=date(2026, 7, 27),
            actual_cash="120000",
        )
    )
    ledger.append_transaction(tx("1", "AAPL", "BUY", "100", "10"))

    state = rebuild_live_account(
        opening=LiveOpeningState(),
        ledger=ledger,
    )

    assert state.actual_cash == D("119000")
    assert state.calculated_cash == D("99000.00")
    assert state.cash_difference == D("20000.00")
    assert state.net_cash_adjustment == D("20000.00")


def test_max_three_positions_is_enforced() -> None:
    ledger = LiveLedger()
    for index, symbol in enumerate(("AAPL", "MSFT", "NVDA", "AMZN"), start=1):
        ledger.append_transaction(
            tx(str(index), symbol, "BUY", "10", "1")
        )

    with pytest.raises(PositionRuleViolation, match="max_positions=3"):
        rebuild_live_account(
            opening=LiveOpeningState(),
            ledger=ledger,
        )


def test_add_requires_existing_position() -> None:
    ledger = LiveLedger()
    ledger.append_transaction(tx("1", "AAPL", "ADD", "100", "10"))

    with pytest.raises(PositionRuleViolation, match="ADD requires"):
        rebuild_live_account(
            opening=LiveOpeningState(),
            ledger=ledger,
        )


def test_reduce_cannot_close_position() -> None:
    ledger = LiveLedger()
    ledger.append_transaction(tx("1", "AAPL", "BUY", "100", "10"))
    ledger.append_transaction(tx("2", "AAPL", "REDUCE", "110", "10"))

    with pytest.raises(PositionRuleViolation, match="use EXIT"):
        rebuild_live_account(
            opening=LiveOpeningState(),
            ledger=ledger,
        )


def test_transaction_cannot_create_negative_actual_cash() -> None:
    ledger = LiveLedger()
    ledger.append_transaction(tx("1", "AAPL", "BUY", "100001", "1"))

    with pytest.raises(CashRuleViolation):
        rebuild_live_account(
            opening=LiveOpeningState(),
            ledger=ledger,
        )


def test_rebuild_is_deterministic() -> None:
    ledger = LiveLedger()
    ledger.append_transaction(tx("1", "AAPL", "BUY", "100", "10"))
    ledger.append_cash_control(
        CashControlEvent(
            event_id="cash-1",
            effective_date=date(2026, 7, 27),
            actual_cash="101000",
        )
    )
    ledger.append_transaction(tx("2", "AAPL", "EXIT", "110"))

    first = rebuild_live_account(
        opening=LiveOpeningState(),
        ledger=ledger,
    )
    second = rebuild_live_account(
        opening=LiveOpeningState(),
        ledger=ledger,
    )

    assert first.actual_cash == second.actual_cash
    assert first.calculated_cash == second.calculated_cash
    assert first.cash_difference == second.cash_difference
    assert first.realized_pnl == second.realized_pnl
    assert first.positions == second.positions
