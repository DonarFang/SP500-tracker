"""Deterministic Live account reconstruction from two append-only ledgers."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Mapping

from .live_ledger import (
    CashControlEvent,
    LiveLedger,
    LiveLedgerError,
    ManualAction,
    TransactionEvent,
)


class LiveAccountError(ValueError):
    """Base exception for invalid Live account state transitions."""


class PositionRuleViolation(LiveAccountError):
    """Raised when a transaction violates position-state rules."""


class CashRuleViolation(LiveAccountError):
    """Raised when a transaction would create unsupported negative cash."""


def _decimal(
    value: Decimal | int | float | str,
    *,
    field_name: str,
) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise LiveAccountError(f"{field_name} must be a valid decimal") from exc
    if not result.is_finite():
        raise LiveAccountError(f"{field_name} must be finite")
    return result


@dataclass(frozen=True)
class LiveOpeningState:
    opening_date: date | None = None
    opening_cash: Decimal | int | float | str = Decimal("100000.00")
    positions: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.opening_date is not None and not isinstance(self.opening_date, date):
            raise LiveAccountError("opening_date must be datetime.date or None")
        cash = _decimal(self.opening_cash, field_name="opening_cash")
        if cash < 0:
            raise LiveAccountError("opening_cash must not be negative")
        object.__setattr__(self, "opening_cash", cash)
        if dict(self.positions):
            raise LiveAccountError(
                "M_step 2-L2 opening contract supports an empty account only"
            )
        object.__setattr__(self, "positions", {})


@dataclass
class PositionState:
    symbol: str
    shares: Decimal
    average_cost: Decimal
    realized_pnl: Decimal = Decimal("0")

    @property
    def cost_basis(self) -> Decimal:
        return self.shares * self.average_cost


@dataclass(frozen=True)
class AppliedTransaction:
    event_id: str
    trade_date: date
    symbol: str
    action: str
    price: Decimal
    effective_shares: Decimal
    gross_cash_effect: Decimal
    realized_pnl: Decimal


@dataclass(frozen=True)
class AppliedCashControl:
    event_id: str
    effective_date: date
    cash_before: Decimal
    cash_after: Decimal
    cash_delta: Decimal


@dataclass
class LiveAccountState:
    opening_cash: Decimal
    actual_cash: Decimal
    calculated_cash: Decimal
    cash_difference: Decimal
    positions: dict[str, PositionState]
    realized_pnl: Decimal
    unrealized_pnl: Decimal
    trading_pnl: Decimal
    net_cash_adjustment: Decimal
    positions_value: Decimal
    total_equity: Decimal
    applied_transactions: tuple[AppliedTransaction, ...]
    applied_cash_controls: tuple[AppliedCashControl, ...]

    @property
    def active_position_count(self) -> int:
        return len(self.positions)


def _clone_positions(
    positions: dict[str, PositionState],
) -> dict[str, PositionState]:
    return {
        symbol: PositionState(
            symbol=position.symbol,
            shares=position.shares,
            average_cost=position.average_cost,
            realized_pnl=position.realized_pnl,
        )
        for symbol, position in positions.items()
    }


def rebuild_live_account(
    *,
    opening: LiveOpeningState,
    ledger: LiveLedger,
    marks: Mapping[str, Decimal | int | float | str] | None = None,
    max_positions: int = 3,
) -> LiveAccountState:
    """Replay the global ledger journal into one deterministic account state."""

    if max_positions <= 0:
        raise LiveAccountError("max_positions must be greater than zero")

    actual_cash = opening.opening_cash
    calculated_cash = opening.opening_cash
    positions: dict[str, PositionState] = {}
    realized_pnl = Decimal("0")
    net_cash_adjustment = Decimal("0")
    applied_transactions: list[AppliedTransaction] = []
    applied_cash_controls: list[AppliedCashControl] = []

    for envelope in ledger.iter_journal():
        event = envelope.event

        if isinstance(event, CashControlEvent):
            cash_before = actual_cash
            cash_after = event.actual_cash
            cash_delta = cash_after - cash_before
            actual_cash = cash_after
            net_cash_adjustment += cash_delta
            applied_cash_controls.append(
                AppliedCashControl(
                    event_id=event.event_id,
                    effective_date=event.effective_date,
                    cash_before=cash_before,
                    cash_after=cash_after,
                    cash_delta=cash_delta,
                )
            )
            continue

        if not isinstance(event, TransactionEvent):
            raise LiveAccountError(
                f"unsupported ledger event type: {type(event).__name__}"
            )

        symbol = event.symbol
        position = positions.get(symbol)

        if event.action is ManualAction.BUY:
            if position is not None:
                raise PositionRuleViolation(
                    f"BUY requires no active position for {symbol}; use ADD"
                )
            if len(positions) >= max_positions:
                raise PositionRuleViolation(
                    f"BUY would exceed max_positions={max_positions}"
                )
            assert event.shares is not None
            effective_shares = event.shares
            gross = event.price * effective_shares
            if actual_cash < gross:
                raise CashRuleViolation(
                    f"BUY {symbol} requires {gross} but actual_cash is {actual_cash}"
                )
            actual_cash -= gross
            calculated_cash -= gross
            positions[symbol] = PositionState(
                symbol=symbol,
                shares=effective_shares,
                average_cost=event.price,
            )
            event_realized = Decimal("0")
            gross_effect = -gross

        elif event.action is ManualAction.ADD:
            if position is None:
                raise PositionRuleViolation(
                    f"ADD requires an active position for {symbol}"
                )
            assert event.shares is not None
            effective_shares = event.shares
            gross = event.price * effective_shares
            if actual_cash < gross:
                raise CashRuleViolation(
                    f"ADD {symbol} requires {gross} but actual_cash is {actual_cash}"
                )
            new_shares = position.shares + effective_shares
            new_cost = (
                position.shares * position.average_cost
                + effective_shares * event.price
            ) / new_shares
            actual_cash -= gross
            calculated_cash -= gross
            position.shares = new_shares
            position.average_cost = new_cost
            event_realized = Decimal("0")
            gross_effect = -gross

        elif event.action is ManualAction.REDUCE:
            if position is None:
                raise PositionRuleViolation(
                    f"REDUCE requires an active position for {symbol}"
                )
            assert event.shares is not None
            effective_shares = event.shares
            if effective_shares >= position.shares:
                raise PositionRuleViolation(
                    "REDUCE must be less than current shares; use EXIT for full exit"
                )
            gross = event.price * effective_shares
            event_realized = (
                event.price - position.average_cost
            ) * effective_shares
            actual_cash += gross
            calculated_cash += gross
            position.shares -= effective_shares
            position.realized_pnl += event_realized
            realized_pnl += event_realized
            gross_effect = gross

        elif event.action is ManualAction.EXIT:
            if position is None:
                raise PositionRuleViolation(
                    f"EXIT requires an active position for {symbol}"
                )
            effective_shares = position.shares
            gross = event.price * effective_shares
            event_realized = (
                event.price - position.average_cost
            ) * effective_shares
            actual_cash += gross
            calculated_cash += gross
            position.realized_pnl += event_realized
            realized_pnl += event_realized
            del positions[symbol]
            gross_effect = gross

        else:
            raise LiveLedgerError(f"unsupported action: {event.action}")

        applied_transactions.append(
            AppliedTransaction(
                event_id=event.event_id,
                trade_date=event.trade_date,
                symbol=symbol,
                action=event.action.value,
                price=event.price,
                effective_shares=effective_shares,
                gross_cash_effect=gross_effect,
                realized_pnl=event_realized,
            )
        )

    normalized_marks: dict[str, Decimal] = {}
    if marks:
        for symbol, value in marks.items():
            mark = _decimal(value, field_name=f"mark[{symbol}]")
            if mark < 0:
                raise LiveAccountError(f"mark[{symbol}] must not be negative")
            normalized_marks[str(symbol).strip().upper()] = mark

    positions_value = Decimal("0")
    unrealized_pnl = Decimal("0")
    for symbol, position in positions.items():
        mark = normalized_marks.get(symbol, position.average_cost)
        positions_value += position.shares * mark
        unrealized_pnl += position.shares * (mark - position.average_cost)

    cash_difference = actual_cash - calculated_cash
    trading_pnl = realized_pnl + unrealized_pnl
    total_equity = actual_cash + positions_value

    return LiveAccountState(
        opening_cash=opening.opening_cash,
        actual_cash=actual_cash,
        calculated_cash=calculated_cash,
        cash_difference=cash_difference,
        positions=_clone_positions(positions),
        realized_pnl=realized_pnl,
        unrealized_pnl=unrealized_pnl,
        trading_pnl=trading_pnl,
        net_cash_adjustment=net_cash_adjustment,
        positions_value=positions_value,
        total_equity=total_equity,
        applied_transactions=tuple(applied_transactions),
        applied_cash_controls=tuple(applied_cash_controls),
    )
