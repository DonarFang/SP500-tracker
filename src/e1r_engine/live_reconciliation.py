"""Recommendation versus actual-execution reconciliation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional, Sequence

from .live_ledger import ManualAction, TransactionEvent
from .live_recommendation import PositionRecommendation


class LiveReconciliationError(ValueError):
    pass


FROZEN_RECONCILIATION_STATUSES = frozenset(
    {
        "PENDING",
        "EXECUTED_AS_RECOMMENDED",
        "PARTIALLY_EXECUTED",
        "NOT_EXECUTED",
        "EXECUTED_DIFFERENTLY",
        "EXPIRED",
        "INFORMATIONAL",
    }
)


@dataclass(frozen=True)
class LiveReconciliationRecord:
    reconciliation_id: str
    signal_date: date
    expected_execution_date: date
    symbol: str
    recommended_action: str
    actual_action: Optional[str]
    recommended_shares: Optional[Decimal]
    actual_shares: Optional[Decimal]
    actual_price: Optional[Decimal]
    status: str
    notes: str = ""

    def __post_init__(self) -> None:
        if self.status not in FROZEN_RECONCILIATION_STATUSES:
            raise LiveReconciliationError(
                f"unsupported reconciliation status: {self.status}"
            )


def _actual_action(event: TransactionEvent) -> str:
    if not isinstance(event.action, ManualAction):
        raise LiveReconciliationError(
            "TransactionEvent.action must be ManualAction"
        )
    return event.action.value


def reconcile_recommendations(
    *,
    signal_date: date,
    expected_execution_date: date,
    as_of_date: date,
    recommendations: Sequence[PositionRecommendation],
    transactions: Sequence[TransactionEvent],
) -> tuple[LiveReconciliationRecord, ...]:
    if expected_execution_date <= signal_date:
        raise LiveReconciliationError(
            "expected_execution_date must be after signal_date"
        )
    if as_of_date < signal_date:
        raise LiveReconciliationError(
            "as_of_date must not precede signal_date"
        )

    actual_by_symbol: dict[str, list[TransactionEvent]] = {}
    for event in transactions:
        if event.trade_date == expected_execution_date:
            actual_by_symbol.setdefault(event.symbol, []).append(event)

    records = []
    for recommendation in recommendations:
        symbol = recommendation.symbol
        recommended_action = recommendation.action

        if recommended_action == "HOLD":
            records.append(
                LiveReconciliationRecord(
                    reconciliation_id=(
                        f"{signal_date.isoformat()}::"
                        f"{expected_execution_date.isoformat()}::"
                        f"{symbol}::HOLD"
                    ),
                    signal_date=signal_date,
                    expected_execution_date=expected_execution_date,
                    symbol=symbol,
                    recommended_action="HOLD",
                    actual_action=None,
                    recommended_shares=None,
                    actual_shares=None,
                    actual_price=None,
                    status="INFORMATIONAL",
                )
            )
            continue

        candidates = actual_by_symbol.get(symbol, [])
        actual = candidates[0] if candidates else None

        if actual is None:
            if as_of_date < expected_execution_date:
                status = "PENDING"
            elif as_of_date == expected_execution_date:
                status = "NOT_EXECUTED"
            else:
                status = "EXPIRED"

            records.append(
                LiveReconciliationRecord(
                    reconciliation_id=(
                        f"{signal_date.isoformat()}::"
                        f"{expected_execution_date.isoformat()}::"
                        f"{symbol}::{recommended_action}"
                    ),
                    signal_date=signal_date,
                    expected_execution_date=expected_execution_date,
                    symbol=symbol,
                    recommended_action=recommended_action,
                    actual_action=None,
                    recommended_shares=recommendation.target_shares,
                    actual_shares=None,
                    actual_price=None,
                    status=status,
                )
            )
            continue

        actual_action = _actual_action(actual)
        actual_shares = (
            Decimal(str(actual.shares))
            if actual.shares is not None
            else None
        )

        if actual_action != recommended_action:
            status = "EXECUTED_DIFFERENTLY"
        elif (
            recommendation.target_shares is not None
            and actual_shares != recommendation.target_shares
        ):
            status = "PARTIALLY_EXECUTED"
        else:
            status = "EXECUTED_AS_RECOMMENDED"

        records.append(
            LiveReconciliationRecord(
                reconciliation_id=(
                    f"{signal_date.isoformat()}::"
                    f"{expected_execution_date.isoformat()}::"
                    f"{symbol}::{recommended_action}"
                ),
                signal_date=signal_date,
                expected_execution_date=expected_execution_date,
                symbol=symbol,
                recommended_action=recommended_action,
                actual_action=actual_action,
                recommended_shares=recommendation.target_shares,
                actual_shares=actual_shares,
                actual_price=Decimal(str(actual.price)),
                status=status,
            )
        )

    recommended_symbols = {
        item.symbol
        for item in recommendations
        if item.action != "HOLD"
    }
    for symbol, events in sorted(actual_by_symbol.items()):
        if symbol in recommended_symbols:
            continue
        for event in events:
            records.append(
                LiveReconciliationRecord(
                    reconciliation_id=(
                        f"{signal_date.isoformat()}::"
                        f"{expected_execution_date.isoformat()}::"
                        f"{symbol}::NO_RECOMMENDATION::"
                        f"{_actual_action(event)}"
                    ),
                    signal_date=signal_date,
                    expected_execution_date=expected_execution_date,
                    symbol=symbol,
                    recommended_action="NO_RECOMMENDATION",
                    actual_action=_actual_action(event),
                    recommended_shares=None,
                    actual_shares=(
                        Decimal(str(event.shares))
                        if event.shares is not None
                        else None
                    ),
                    actual_price=Decimal(str(event.price)),
                    status="EXECUTED_DIFFERENTLY",
                    notes="actual execution had no matching recommendation",
                )
            )

    return tuple(records)
