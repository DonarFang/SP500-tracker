"""L01-L14: confirmed-transaction Live Cycle contract."""

from datetime import date
from decimal import Decimal
import json

from e1r_engine.live_cycle_state import (
    LiveCycleStateError, load_transaction_events, replay_live_cycles,
    stable_recommendation_id,
)
from e1r_engine.live_ledger import TransactionEvent


def _event(event_id, action, shares="10", **extra):
    return TransactionEvent(
        event_id=event_id, trade_date=date(2026, 8, 18), symbol="AAA",
        action=action, price="100", shares=None if action == "EXIT" else shares,
        **extra,
    )


def test_l01_buy_opens_confirmed_unit_cycle():
    assert replay_live_cycles([_event("BUY-0001", "BUY")])["AAA"].size_units == 1.0


def test_l02_emerging_buy_opens_half_unit_cycle():
    state = replay_live_cycles([_event("BUY-0002", "BUY", target_size_units="0.5")])["AAA"]
    assert state.size_units == 0.5


def test_l03_add_advances_half_to_one():
    state = replay_live_cycles([_event("BUY-0003", "BUY", target_size_units="0.5"), _event("ADD-0003", "ADD")])["AAA"]
    assert state.size_units == 1.0


def test_l04_add_caps_at_one():
    state = replay_live_cycles([_event("BUY-0004", "BUY"), _event("ADD-0004", "ADD")])["AAA"]
    assert state.size_units == 1.0


def test_l05_reduce_moves_one_to_half():
    state = replay_live_cycles([_event("BUY-0005", "BUY"), _event("RED-0005", "REDUCE")])["AAA"]
    assert state.size_units == 0.5


def test_l06_reduce_never_moves_below_half():
    state = replay_live_cycles([_event("BUY-0006", "BUY", target_size_units="0.5"), _event("RED-0006", "REDUCE")])["AAA"]
    assert state.size_units == 0.5


def test_l07_exit_closes_cycle():
    assert replay_live_cycles([_event("BUY-0007", "BUY"), _event("EXIT-007", "EXIT")]) == {}


def test_l08_duplicate_event_id_is_exactly_once():
    buy = _event("BUY-0008", "BUY")
    assert replay_live_cycles([buy, buy])["AAA"].add_count == 0


def test_l09_add_without_buy_holds_as_error():
    try:
        replay_live_cycles([_event("ADD-0009", "ADD")])
    except LiveCycleStateError:
        return
    raise AssertionError("ADD without BUY must fail closed")


def test_l10_linkage_is_preserved():
    buy = _event("BUY-0010", "BUY", recommendation_id="REC-1", signal_date=date(2026, 8, 17), expected_execution_date=date(2026, 8, 18), origin_branch="UPTREND")
    state = replay_live_cycles([buy])["AAA"]
    assert state.entry_recommendation_id == "REC-1" and state.entry_signal_date == "2026-08-17"


def test_l11_stable_recommendation_id_is_deterministic():
    kwargs = dict(signal_date="2026-08-17", expected_execution_date="2026-08-18", symbol="AAA", action="BUY")
    assert stable_recommendation_id(**kwargs) == stable_recommendation_id(**kwargs)


def test_l12_legacy_payload_fingerprint_shape_is_unchanged():
    event = _event("BUY-0012", "BUY")
    assert "recommendation_id" not in event.canonical_payload()


def test_l13_optional_linkage_round_trips_from_journal(tmp_path):
    root = tmp_path / "live"
    path = root / "runtime/history/ledger_journal.jsonl"
    path.parent.mkdir(parents=True)
    event = _event("BUY-0013", "BUY", recommendation_id="REC-13")
    path.write_text(json.dumps({"ledger": "TRANSACTION", "event": event.canonical_payload()}) + "\n")
    assert load_transaction_events(root)[0].recommendation_id == "REC-13"


def test_l14_counts_confirmed_add_and_reduce_only():
    state = replay_live_cycles([_event("BUY-0014", "BUY"), _event("ADD-0014", "ADD"), _event("RED-0014", "REDUCE")])["AAA"]
    assert (state.add_count, state.reduce_count) == (1, 1)
