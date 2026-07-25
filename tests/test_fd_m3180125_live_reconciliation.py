from datetime import date
from decimal import Decimal

from e1r_engine.live_ledger import TransactionEvent
from e1r_engine.live_recommendation import PositionRecommendation
from e1r_engine.live_reconciliation import (
    FROZEN_RECONCILIATION_STATUSES,
    reconcile_recommendations,
)


def test_frozen_status_set_is_exact() -> None:
    assert FROZEN_RECONCILIATION_STATUSES == {
        "PENDING",
        "EXECUTED_AS_RECOMMENDED",
        "PARTIALLY_EXECUTED",
        "NOT_EXECUTED",
        "EXECUTED_DIFFERENTLY",
        "EXPIRED",
        "INFORMATIONAL",
    }


def test_execution_as_recommended_uses_manual_action_value() -> None:
    rows = reconcile_recommendations(
        signal_date=date(2026, 7, 27),
        expected_execution_date=date(2026, 7, 28),
        as_of_date=date(2026, 7, 28),
        recommendations=(
            PositionRecommendation(
                "AAPL",
                "BUY",
                target_shares=Decimal("2"),
            ),
        ),
        transactions=(
            TransactionEvent(
                event_id="tx-1",
                trade_date=date(2026, 7, 28),
                symbol="AAPL",
                action="BUY",
                price="101",
                shares="2",
            ),
        ),
    )
    assert rows[0].actual_action == "BUY"
    assert rows[0].status == "EXECUTED_AS_RECOMMENDED"


def test_pending_not_executed_expired_and_hold() -> None:
    recommendation = PositionRecommendation(
        "AAPL",
        "BUY",
        target_shares=Decimal("2"),
    )

    pending = reconcile_recommendations(
        signal_date=date(2026, 7, 27),
        expected_execution_date=date(2026, 7, 28),
        as_of_date=date(2026, 7, 27),
        recommendations=(recommendation,),
        transactions=(),
    )
    assert pending[0].status == "PENDING"

    not_executed = reconcile_recommendations(
        signal_date=date(2026, 7, 27),
        expected_execution_date=date(2026, 7, 28),
        as_of_date=date(2026, 7, 28),
        recommendations=(recommendation,),
        transactions=(),
    )
    assert not_executed[0].status == "NOT_EXECUTED"

    expired = reconcile_recommendations(
        signal_date=date(2026, 7, 27),
        expected_execution_date=date(2026, 7, 28),
        as_of_date=date(2026, 7, 29),
        recommendations=(recommendation,),
        transactions=(),
    )
    assert expired[0].status == "EXPIRED"

    hold = reconcile_recommendations(
        signal_date=date(2026, 7, 27),
        expected_execution_date=date(2026, 7, 28),
        as_of_date=date(2026, 7, 27),
        recommendations=(PositionRecommendation("AAPL", "HOLD"),),
        transactions=(),
    )
    assert hold[0].status == "INFORMATIONAL"


def test_partial_and_different_execution() -> None:
    recommendation = PositionRecommendation(
        "AAPL",
        "BUY",
        target_shares=Decimal("2"),
    )

    partial = reconcile_recommendations(
        signal_date=date(2026, 7, 27),
        expected_execution_date=date(2026, 7, 28),
        as_of_date=date(2026, 7, 28),
        recommendations=(recommendation,),
        transactions=(
            TransactionEvent(
                event_id="tx-partial",
                trade_date=date(2026, 7, 28),
                symbol="AAPL",
                action="BUY",
                price="101",
                shares="1",
            ),
        ),
    )
    assert partial[0].status == "PARTIALLY_EXECUTED"

    different = reconcile_recommendations(
        signal_date=date(2026, 7, 27),
        expected_execution_date=date(2026, 7, 28),
        as_of_date=date(2026, 7, 28),
        recommendations=(recommendation,),
        transactions=(
            TransactionEvent(
                event_id="tx-different",
                trade_date=date(2026, 7, 28),
                symbol="AAPL",
                action="REDUCE",
                price="101",
                shares="1",
            ),
        ),
    )
    assert different[0].status == "EXECUTED_DIFFERENTLY"
