"""C01-C10: frozen shared REDUCE contract."""

from e1r_engine.canonical_runtime import CanonicalRuntime
from e1r_engine.state import AccountState, PositionState


def _orders(action: str, units: float, *, origin: str = "UPTREND"):
    position = PositionState.create("AAA", 10, 100, 90, "2026-01-01")
    position = position.__class__(**{**position.__dict__, "metadata": {
        "size_units": units, "origin_branch": origin, "e1r_entry_type": "CONFIRMED"
    }})
    account = AccountState(
        date="2026-02-01", cash=1000, positions={"AAA": position},
        total_equity=1900, positions_value=900, open_positions_count=1,
    )
    return CanonicalRuntime._management_orders(
        date="2026-02-01", branch="UPTREND", account=account,
        day_signals={"AAA": {"action": action, "trend_state": "BROKEN"}},
        market_entry_allowed=True,
        trading_dates=["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04", "2026-01-05", "2026-02-01"],
    )


def test_c01_half_unit_reduce_becomes_hold():
    assert _orders("REDUCE", 0.5)[0].intent_type == "HOLD"


def test_c02_half_unit_exit_remains_exit():
    assert _orders("EXIT", 0.5)[0].intent_type == "EXIT"


def test_c03_full_unit_reduce_remains_reduce():
    assert _orders("REDUCE", 1.0)[0].intent_type == "REDUCE"


def test_c04_minimum_reason_is_explicit():
    assert _orders("REDUCE", 0.5)[0].reason == "reduce_skipped_size_at_minimum"


def test_c05_minimum_hold_has_no_sell_side():
    assert _orders("REDUCE", 0.5)[0].side is None


def test_c06_minimum_hold_has_zero_delta():
    assert _orders("REDUCE", 0.5)[0].quantity_delta == 0.0


def test_c07_regular_reduce_is_half_quantity():
    assert _orders("REDUCE", 1.0)[0].quantity_delta == -5.0


def test_c08_regular_reduce_keeps_fraction_contract():
    assert _orders("REDUCE", 1.0)[0].metadata["reduce_fraction"] == 0.5


def test_c09_sideways_origin_is_not_managed_by_uptrend():
    assert _orders("REDUCE", 1.0, origin="SIDEWAYS_MA_CONFLICT") == []


def test_c10_existing_position_buy_signal_is_hold():
    assert _orders("BUY", 1.0)[0].intent_type == "HOLD"
