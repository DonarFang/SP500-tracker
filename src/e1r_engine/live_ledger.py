"""Append-only Live transaction and cash-control ledgers.

This module owns only user-confirmed Live account facts. It does not own
strategy ranking, Regime, Market State, Market Gate, recommendations, or
model execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from enum import Enum
import hashlib
import json
from typing import Iterator, Literal, Union


class LiveLedgerError(ValueError):
    """Base exception for invalid Live ledger operations."""


class DuplicateEventConflict(LiveLedgerError):
    """Raised when an event_id is reused with different content."""


class ManualAction(str, Enum):
    BUY = "BUY"
    ADD = "ADD"
    REDUCE = "REDUCE"
    EXIT = "EXIT"


def _decimal(value: Decimal | int | float | str, *, field: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise LiveLedgerError(f"{field} must be a valid decimal") from exc
    if not result.is_finite():
        raise LiveLedgerError(f"{field} must be finite")
    return result


def _event_id(value: str) -> str:
    normalized = str(value).strip()
    if not normalized:
        raise LiveLedgerError("event_id is required")
    return normalized


def _notes(value: str) -> str:
    return str(value).strip()


def _symbol(value: str) -> str:
    normalized = str(value).strip().upper()
    if not normalized:
        raise LiveLedgerError("symbol is required")
    return normalized


@dataclass(frozen=True)
class TransactionEvent:
    event_id: str
    trade_date: date
    symbol: str
    action: ManualAction | str
    price: Decimal | int | float | str
    shares: Decimal | int | float | str | None = None
    notes: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "event_id", _event_id(self.event_id))
        if not isinstance(self.trade_date, date):
            raise LiveLedgerError("trade_date must be datetime.date")
        object.__setattr__(self, "symbol", _symbol(self.symbol))
        try:
            action = (
                self.action
                if isinstance(self.action, ManualAction)
                else ManualAction(str(self.action).strip().upper())
            )
        except ValueError as exc:
            raise LiveLedgerError(
                "action must be BUY, ADD, REDUCE, or EXIT"
            ) from exc
        object.__setattr__(self, "action", action)

        price = _decimal(self.price, field="price")
        if price <= 0:
            raise LiveLedgerError("price must be greater than zero")
        object.__setattr__(self, "price", price)

        if action is ManualAction.EXIT:
            if self.shares is not None:
                raise LiveLedgerError("EXIT must not provide shares")
        else:
            if self.shares is None:
                raise LiveLedgerError(f"{action.value} requires shares")
            shares = _decimal(self.shares, field="shares")
            if shares <= 0:
                raise LiveLedgerError("shares must be greater than zero")
            object.__setattr__(self, "shares", shares)

        object.__setattr__(self, "notes", _notes(self.notes))

    def canonical_payload(self) -> dict[str, object]:
        return {
            "event_type": "TRANSACTION",
            "event_id": self.event_id,
            "trade_date": self.trade_date.isoformat(),
            "symbol": self.symbol,
            "action": self.action.value,
            "price": str(self.price),
            "shares": None if self.shares is None else str(self.shares),
            "notes": self.notes,
        }

    def fingerprint(self) -> str:
        raw = json.dumps(
            self.canonical_payload(),
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class CashControlEvent:
    event_id: str
    effective_date: date
    actual_cash: Decimal | int | float | str
    notes: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "event_id", _event_id(self.event_id))
        if not isinstance(self.effective_date, date):
            raise LiveLedgerError("effective_date must be datetime.date")
        actual_cash = _decimal(self.actual_cash, field="actual_cash")
        if actual_cash < 0:
            raise LiveLedgerError("actual_cash must not be negative")
        object.__setattr__(self, "actual_cash", actual_cash)
        object.__setattr__(self, "notes", _notes(self.notes))

    def canonical_payload(self) -> dict[str, object]:
        return {
            "event_type": "CASH_CONTROL",
            "event_id": self.event_id,
            "effective_date": self.effective_date.isoformat(),
            "actual_cash": str(self.actual_cash),
            "notes": self.notes,
        }

    def fingerprint(self) -> str:
        raw = json.dumps(
            self.canonical_payload(),
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


LedgerEvent = Union[TransactionEvent, CashControlEvent]
LedgerName = Literal["TRANSACTION", "CASH_CONTROL"]


@dataclass(frozen=True)
class LedgerEnvelope:
    sequence: int
    ledger: LedgerName
    event_id: str
    event: LedgerEvent


class LiveLedger:
    """Two append-only ledgers with one deterministic global event journal."""

    def __init__(self) -> None:
        self._transactions: list[TransactionEvent] = []
        self._cash_controls: list[CashControlEvent] = []
        self._journal: list[LedgerEnvelope] = []
        self._fingerprints: dict[str, str] = {}

    @property
    def transactions(self) -> tuple[TransactionEvent, ...]:
        return tuple(self._transactions)

    @property
    def cash_controls(self) -> tuple[CashControlEvent, ...]:
        return tuple(self._cash_controls)

    def _append(self, event: LedgerEvent, ledger: LedgerName) -> bool:
        fingerprint = event.fingerprint()
        previous = self._fingerprints.get(event.event_id)
        if previous is not None:
            if previous == fingerprint:
                return False
            raise DuplicateEventConflict(
                f"event_id {event.event_id!r} already exists with different content"
            )

        self._fingerprints[event.event_id] = fingerprint
        if ledger == "TRANSACTION":
            if not isinstance(event, TransactionEvent):
                raise TypeError("TRANSACTION ledger requires TransactionEvent")
            self._transactions.append(event)
        else:
            if not isinstance(event, CashControlEvent):
                raise TypeError("CASH_CONTROL ledger requires CashControlEvent")
            self._cash_controls.append(event)

        self._journal.append(
            LedgerEnvelope(
                sequence=len(self._journal) + 1,
                ledger=ledger,
                event_id=event.event_id,
                event=event,
            )
        )
        return True

    def append_transaction(self, event: TransactionEvent) -> bool:
        return self._append(event, "TRANSACTION")

    def append_cash_control(self, event: CashControlEvent) -> bool:
        return self._append(event, "CASH_CONTROL")

    def iter_journal(self) -> Iterator[LedgerEnvelope]:
        yield from tuple(self._journal)

    def __len__(self) -> int:
        return len(self._journal)
