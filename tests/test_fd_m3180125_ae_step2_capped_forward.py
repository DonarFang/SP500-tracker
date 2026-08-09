from __future__ import annotations

from e1r_engine.capped_atr_stop import (
    ENTRY_METADATA_KEY,
    POSITION_METADATA_KEY,
    VARIANT_ID,
    build_entry_metadata,
)
from e1r_engine.contracts import DailyBar, MarketSnapshot, RegimeRecord
from e1r_engine.forward_runtime import (
    CanonicalDailyDecisionRouter,
    PendingOrderRecord,
    T1ExecutionEngine,
)
from e1r_engine.state import AccountState, PositionState


def test_forward_buy_fill_freezes_capped_atr_state() -> None:
    account = AccountState.empty("2026-01-05", 100000.0)
    account.metadata["strategy_variant"] = VARIANT_ID
    order = PendingOrderRecord(
        order_id="order-1",
        signal_date="2026-01-05",
        symbol="TEST",
        intent_type="BUY",
        side="BUY",
        branch="UPTREND",
        sequence=1,
        reason="entry",
        target_quantity=None,
        quantity_delta=None,
        metadata={
            "target_fraction_of_equity": 0.10,
            ENTRY_METADATA_KEY: build_entry_metadata(
                atr20=5.0,
                atr_as_of="2026-01-05",
            ),
        },
    )
    result = T1ExecutionEngine().execute(
        execution_date="2026-01-06",
        account=account,
        pending_orders=[order],
        bars_by_symbol={
            "TEST": DailyBar(
                date="2026-01-06",
                open=100.0,
                high=101.0,
                low=99.0,
                close=100.0,
            )
        },
    )
    state = result.account_after.positions["TEST"].metadata[POSITION_METADATA_KEY]
    assert abs(state["a0"] - 101.101) < 1e-12
    assert state["atr20"] == 5.0
    assert state["atr_as_of"] == "2026-01-05"


def test_forward_non_uptrend_route_uses_canonical_hard_stop() -> None:
    position = PositionState.create(
        symbol="TEST",
        quantity=10.0,
        avg_cost=100.0,
        price=80.0,
        date="2026-02-01",
    )
    object.__setattr__(
        position,
        "metadata",
        {
            "origin_branch": "UPTREND",
            POSITION_METADATA_KEY: {
                "variant_id": VARIANT_ID,
                "hard_stop_model": "CAPPED_ATR_FROZEN_ENTRY_A0",
                "a0": 100.0,
                "atr20": 5.0,
                "atr_as_of": "2026-01-01",
                "distance": 15.0,
                "distance_fraction": 0.15,
                "trigger_price": 85.0,
                "atr_frozen_for_cycle": True,
                "add_updates_stop_anchor": False,
                "block_same_day_reentry_after_hard_stop": False,
            },
        },
    )
    account = AccountState(
        date="2026-02-01",
        cash=1000.0,
        positions={"TEST": position},
        total_equity=1800.0,
        positions_value=800.0,
        open_positions_count=1,
        metadata={"strategy_variant": VARIANT_ID},
    )
    snapshot = MarketSnapshot(
        date="2026-02-01",
        universe=["TEST"],
        prices_by_symbol={
            "TEST": DailyBar(
                date="2026-02-01", open=82.0, high=83.0, low=79.0, close=80.0
            )
        },
        indices={},
        regime=RegimeRecord(
            date="2026-02-01",
            spx_regime="DOWNTREND",
            subclass="NO_SUBCLASS",
        ),
    )
    result = CanonicalDailyDecisionRouter().decide(
        snapshot=snapshot,
        account=account,
    )
    assert len(result.order_intents) == 1
    assert result.order_intents[0].intent_type == "EXIT"
    assert result.order_intents[0].reason == "HARD_LOSS_STOP"
