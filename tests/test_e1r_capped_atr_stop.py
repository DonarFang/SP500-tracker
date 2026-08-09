from __future__ import annotations

import math
import unittest

from e1r_engine.capped_atr_stop import (
    CappedAtrStopConfig,
    CappedAtrStopPolicy,
    ENTRY_METADATA_KEY,
    HARD_STOP_REASON,
    POSITION_METADATA_KEY,
    VARIANT_ID,
    annotate_legacy_buy_order,
    build_frozen_state,
    compute_entry_atr20,
    triggered_at_close,
)
from e1r_engine.contracts import DailyBar, MarketSnapshot, RegimeRecord
from e1r_engine.core import E1RCoreEngine
from e1r_engine.state import AccountState, OrderIntent, PositionState


class CappedAtrStopTests(unittest.TestCase):
    def test_atr20_is_simple_complete_tr_and_has_no_lookahead(self):
        dates = [f"2026-01-{index:02d}" for index in range(1, 23)]
        closes = [100.0 + index for index in range(22)]
        highs = [close + 2.0 for close in closes]
        lows = [close - 1.0 for close in closes]

        atr = compute_entry_atr20(
            symbol="TEST",
            dates=dates,
            closes=closes,
            ohlc={"high": highs, "low": lows},
            as_of_date=dates[20],
        )
        self.assertAlmostEqual(atr, 3.0)

        highs[21] = 10000.0
        lows[21] = 1.0
        atr_after_future_mutation = compute_entry_atr20(
            symbol="TEST",
            dates=dates,
            closes=closes,
            ohlc={"high": highs, "low": lows},
            as_of_date=dates[20],
        )
        self.assertEqual(atr, atr_after_future_mutation)

    def test_distance_floor_middle_and_cap(self):
        floor = build_frozen_state(
            adjusted_first_buy_price=100.0,
            entry_metadata={"atr20": 1.0, "atr_as_of": "2026-01-01"},
        )
        middle = build_frozen_state(
            adjusted_first_buy_price=100.0,
            entry_metadata={"atr20": 5.0, "atr_as_of": "2026-01-01"},
        )
        cap = build_frozen_state(
            adjusted_first_buy_price=100.0,
            entry_metadata={"atr20": 10.0, "atr_as_of": "2026-01-01"},
        )
        self.assertEqual(floor.distance, 12.0)
        self.assertEqual(middle.distance, 15.0)
        self.assertEqual(cap.distance, 20.0)
        self.assertTrue(triggered_at_close(close=floor.trigger_price, state=floor))

    def test_legacy_overlay_preserves_original_exit_precedence(self):
        state = build_frozen_state(
            adjusted_first_buy_price=100.0,
            entry_metadata={"atr20": 5.0, "atr_as_of": "2026-01-01"},
        )
        holding = {
            "avg_cost": 110.0,
            "current_close": 84.0,
            "leader_score_entry": 90.0,
            POSITION_METADATA_KEY: state.to_dict(),
        }
        original = {
            "sym": "TEST",
            "action": "EXIT",
            "signal_date": "2026-02-01",
            "ls": 50.0,
            "close_t": 84.0,
            "primary_reason": "broken_trend",
            "reasons": ["broken_trend"],
        }
        orders, trace = CappedAtrStopPolicy.apply_legacy_management_orders(
            date="2026-02-01",
            holdings={"TEST": holding},
            canonical_orders=[original],
        )
        self.assertEqual(orders, [original])
        self.assertEqual(trace[0]["primary_reason"], "ORIGINAL_ENGINE_EXIT")
        self.assertEqual(
            trace[0]["triggered_reasons"],
            ["ORIGINAL_ENGINE_EXIT", HARD_STOP_REASON],
        )

    def test_hard_stop_replaces_add_without_mutating_frozen_state(self):
        state = build_frozen_state(
            adjusted_first_buy_price=100.0,
            entry_metadata={"atr20": 5.0, "atr_as_of": "2026-01-01"},
        )
        frozen_before = state.to_dict()
        holding = {
            "avg_cost": 120.0,
            "current_close": 84.0,
            "origin_branch": "UPTREND",
            POSITION_METADATA_KEY: frozen_before,
        }
        add = {
            "sym": "TEST",
            "action": "ADD",
            "signal_date": "2026-02-01",
            "ls": 80.0,
            "close_t": 84.0,
        }
        orders, _ = CappedAtrStopPolicy.apply_legacy_management_orders(
            date="2026-02-01",
            holdings={"TEST": holding},
            canonical_orders=[add],
        )
        self.assertEqual(orders[0]["action"], "EXIT")
        self.assertEqual(orders[0]["primary_reason"], HARD_STOP_REASON)
        self.assertEqual(holding[POSITION_METADATA_KEY], frozen_before)

    def test_buy_annotation_and_reentry_policy_are_frozen(self):
        order = annotate_legacy_buy_order(
            {"sym": "TEST", "action": "BUY", "signal_date": "2026-01-01"},
            atr20=4.0,
            atr_as_of="2026-01-01",
        )
        self.assertEqual(order[ENTRY_METADATA_KEY]["atr20"], 4.0)
        self.assertFalse(CappedAtrStopConfig().block_same_day_reentry_after_hard_stop)

    def test_core_applies_stop_in_non_uptrend_route(self):
        state = build_frozen_state(
            adjusted_first_buy_price=100.0,
            entry_metadata={"atr20": 5.0, "atr_as_of": "2026-01-01"},
        )
        position = PositionState.create(
            symbol="TEST",
            quantity=10.0,
            avg_cost=120.0,
            price=84.0,
            date="2026-01-02",
        )
        object.__setattr__(
            position,
            "metadata",
            {POSITION_METADATA_KEY: state.to_dict()},
        )
        account = AccountState(
            date="2026-02-01",
            cash=1000.0,
            positions={"TEST": position},
            total_equity=1840.0,
            positions_value=840.0,
            open_positions_count=1,
            metadata={"strategy_variant": VARIANT_ID},
        )
        snapshot = MarketSnapshot(
            date="2026-02-01",
            universe=["TEST"],
            prices_by_symbol={
                "TEST": DailyBar(
                    date="2026-02-01",
                    open=86.0,
                    high=87.0,
                    low=83.0,
                    close=84.0,
                )
            },
            indices={},
            regime=RegimeRecord(
                date="2026-02-01",
                spx_regime="SIDEWAYS",
                subclass="MA_CONFLICT",
            ),
        )
        result = E1RCoreEngine().step(snapshot, account)
        exits = [order for order in result.order_intents if order.intent_type == "EXIT"]
        self.assertEqual(len(exits), 1)
        self.assertEqual(exits[0].reason, HARD_STOP_REASON)

    def test_strict_core_fails_closed_when_cycle_state_is_missing(self):
        position = PositionState.create(
            symbol="TEST",
            quantity=10.0,
            avg_cost=100.0,
            price=90.0,
            date="2026-01-02",
        )
        account = AccountState(
            date="2026-02-01",
            cash=1000.0,
            positions={"TEST": position},
            total_equity=1900.0,
            positions_value=900.0,
            open_positions_count=1,
            metadata={"strategy_variant": VARIANT_ID},
        )
        snapshot = MarketSnapshot(
            date="2026-02-01",
            universe=["TEST"],
            prices_by_symbol={
                "TEST": DailyBar(
                    date="2026-02-01",
                    open=None,
                    high=None,
                    low=None,
                    close=90.0,
                )
            },
            indices={},
            regime=None,
        )
        with self.assertRaisesRegex(RuntimeError, "missing frozen A0/ATR"):
            E1RCoreEngine().step(snapshot, account)


if __name__ == "__main__":
    unittest.main(verbosity=2)
