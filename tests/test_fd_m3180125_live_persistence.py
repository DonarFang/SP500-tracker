from datetime import date, datetime, timezone
from decimal import Decimal
import json
from pathlib import Path

import pytest

from e1r_engine.live_ledger import (
    CashControlEvent,
    ManualAction,
    TransactionEvent,
)
from e1r_engine.live_persistence import (
    LivePersistenceError,
    LiveRuntimeRepository,
)


def test_runtime_initializes_unactivated(tmp_path: Path) -> None:
    repo = LiveRuntimeRepository(tmp_path / "live")
    repo.initialize_unactivated()
    state = (
        repo.paths.current / "runtime_state.json"
    ).read_text(encoding="utf-8")
    assert '"status": "UNACTIVATED"' in state
    assert '"opening_date": null' in state


def test_two_ledgers_round_trip_preserves_global_sequence(
    tmp_path: Path,
) -> None:
    repo = LiveRuntimeRepository(tmp_path / "live")
    repo.append_transaction(
        TransactionEvent(
            event_id="tx-1",
            trade_date=date(2026, 7, 27),
            symbol="AAPL",
            action="BUY",
            price="100",
            shares="2",
        )
    )
    repo.append_cash_control(
        CashControlEvent(
            event_id="cash-1",
            effective_date=date(2026, 7, 27),
            actual_cash="99850",
            notes="user confirmed",
        ),
        cash_before="99800",
        created_at=datetime(
            2026, 7, 27, 20, 0, tzinfo=timezone.utc
        ),
    )
    repo.append_transaction(
        TransactionEvent(
            event_id="tx-2",
            trade_date=date(2026, 7, 28),
            symbol="AAPL",
            action="ADD",
            price="110",
            shares="1",
            recommendation_id="REC-20260727-AAPL-ADD",
            signal_date=date(2026, 7, 27),
            expected_execution_date=date(2026, 7, 28),
            origin_branch="UPTREND",
            strategy_variant="E1R-CAPPED-ATR",
            target_size_units="1.0",
        )
    )

    restored = repo.load_ledger()
    journal = list(restored.iter_journal())
    assert [item.sequence for item in journal] == [1, 2, 3]
    assert [item.ledger for item in journal] == [
        "TRANSACTION",
        "CASH_CONTROL",
        "TRANSACTION",
    ]
    assert restored.transactions[0].trade_date == date(2026, 7, 27)
    assert restored.transactions[0].action is ManualAction.BUY
    assert restored.transactions[0].price == Decimal("100")
    assert restored.transactions[1].signal_date == date(2026, 7, 27)
    assert restored.transactions[1].expected_execution_date == date(2026, 7, 28)
    assert restored.cash_controls[0].actual_cash == Decimal("99850")


def test_cash_control_projection_has_frozen_audit_fields(
    tmp_path: Path,
) -> None:
    repo = LiveRuntimeRepository(tmp_path / "live")
    repo.append_cash_control(
        CashControlEvent(
            event_id="cash-1",
            effective_date=date(2026, 7, 27),
            actual_cash="100250",
            notes="confirmed",
        ),
        cash_before="100000",
        created_at=datetime(
            2026, 7, 27, 20, 0, tzinfo=timezone.utc
        ),
    )
    row = json.loads(
        repo.cash_control_path.read_text(encoding="utf-8").strip()
    )
    assert row["cash_adjustment_id"] == "cash-1"
    assert row["cash_before"] == "100000"
    assert row["cash_after"] == "100250"
    assert row["cash_delta"] == "250"
    assert row["source"] == "USER_CONFIRMED_CASH"
    assert row["created_at"] == "2026-07-27T20:00:00+00:00"
    assert len(row["record_hash"]) == 64


def test_transaction_is_idempotent_and_conflict_safe(
    tmp_path: Path,
) -> None:
    repo = LiveRuntimeRepository(tmp_path / "live")
    event = TransactionEvent(
        event_id="tx-1",
        trade_date=date(2026, 7, 27),
        symbol="AAPL",
        action="BUY",
        price="100",
        shares="2",
    )
    assert repo.append_transaction(event) == repo.append_transaction(event)
    assert len(
        repo.journal_path.read_text(encoding="utf-8").splitlines()
    ) == 1

    with pytest.raises(LivePersistenceError):
        repo.append_transaction(
            TransactionEvent(
                event_id="tx-1",
                trade_date=date(2026, 7, 27),
                symbol="AAPL",
                action="BUY",
                price="101",
                shares="2",
            )
        )


def test_daily_commit_rejects_conflict(tmp_path: Path) -> None:
    repo = LiveRuntimeRepository(tmp_path / "live")
    repo.commit_daily(
        market_date="2026-07-27",
        artifacts={"equity": {"value": 1}},
    )
    repo.commit_daily(
        market_date="2026-07-27",
        artifacts={"equity": {"value": 1}},
    )
    with pytest.raises(LivePersistenceError):
        repo.commit_daily(
            market_date="2026-07-27",
            artifacts={"equity": {"value": 2}},
        )
