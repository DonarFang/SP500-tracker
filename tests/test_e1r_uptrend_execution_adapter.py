from __future__ import annotations

import copy
import unittest

from e1r_engine.state import OrderIntent
from e1r_engine.uptrend_execution_adapter import (
    UptrendExecutionAdapter,
)


class TestUptrendExecutionAdapter(unittest.TestCase):
    def test_legacy_buy_roundtrip_is_exact(self) -> None:
        payload = {
            "sym": "NVDA",
            "action": "BUY",
            "signal_date": "2021-06-01",
            "entry_type": "E1R_UPTREND_CONFIRMED",
            "target_size_units": 1.0,
            "entry_rank": 1,
            "close_t": 16.25,
            "strategy": "E1R_regime_aware_v0_1_shell",
        }
        before = copy.deepcopy(payload)
        intent = UptrendExecutionAdapter.from_legacy_pending_order(
            payload
        )
        restored = UptrendExecutionAdapter.to_legacy_pending_order(
            intent
        )
        self.assertEqual(restored, before)
        self.assertEqual(payload, before)

    def test_legacy_reduce_roundtrip_is_exact(self) -> None:
        payload = {
            "sym": "MAA",
            "action": "REDUCE",
            "signal_date": "2021-08-18",
            "close_t": 156.520508,
            "ls": 74.77,
            "primary_reason": "leader_score_below_75",
            "reasons": ["leader_score_below_75"],
            "strategy": "E1R_regime_aware_v0_1_shell",
        }
        restored = UptrendExecutionAdapter.to_legacy_pending_order(
            UptrendExecutionAdapter.from_legacy_pending_order(
                payload
            )
        )
        self.assertEqual(restored, payload)

    def test_legacy_exit_roundtrip_is_exact(self) -> None:
        payload = {
            "sym": "NVDA",
            "action": "EXIT",
            "signal_date": "2021-07-16",
            "close_t": 18.0984,
            "ls": 56.69,
            "primary_reason": "leader_score_below_60",
            "reasons": ["leader_score_below_60"],
            "strategy": "E1R_regime_aware_v0_1_shell",
        }
        restored = UptrendExecutionAdapter.to_legacy_pending_order(
            UptrendExecutionAdapter.from_legacy_pending_order(
                payload
            )
        )
        self.assertEqual(restored, payload)

    def test_engine_buy_maps_to_execution_payload(self) -> None:
        intent = OrderIntent(
            date="2021-12-22",
            symbol="AVGO",
            intent_type="BUY",
            side="BUY",
            target_quantity=None,
            quantity_delta=None,
            reason="E1R_UPTREND_CONFIRMED",
            branch="UPTREND",
            metadata={
                "source": "UptrendDecisionConsumer",
                "e1r_entry_type": "E1R_UPTREND_CONFIRMED",
                "target_size_units": 1.0,
                "leader_rank_all": 1,
                "leader_score": 95.0,
                "close_t": 100.0,
                "entry_reasons": ["confirmed"],
            },
        )
        payload = UptrendExecutionAdapter.to_legacy_pending_order(
            intent
        )
        self.assertEqual(payload["sym"], "AVGO")
        self.assertEqual(payload["action"], "BUY")
        self.assertEqual(payload["signal_date"], "2021-12-22")
        self.assertEqual(
            payload["e1r_entry_type"],
            "E1R_UPTREND_CONFIRMED",
        )
        self.assertEqual(payload["target_size_units"], 1.0)
        self.assertEqual(payload["entry_rank"], 1)

    def test_engine_reduce_without_payload_rejected(self) -> None:
        intent = OrderIntent(
            date="2021-08-18",
            symbol="MAA",
            intent_type="REDUCE",
            side="SELL",
            target_quantity=None,
            quantity_delta=None,
            reason="leader_score_below_75",
            branch="UPTREND",
            metadata={},
        )
        with self.assertRaisesRegex(
            ValueError,
            "require preserved legacy payload",
        ):
            UptrendExecutionAdapter.to_legacy_pending_order(
                intent
            )

    def test_unsupported_action_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported"):
            UptrendExecutionAdapter.from_legacy_pending_order(
                {
                    "sym": "AAA",
                    "action": "ADD",
                    "signal_date": "2021-01-01",
                }
            )

    def test_add_is_bypassed_without_mutation(self) -> None:
        payloads = [
            {
                "sym": "AAA",
                "action": "ADD",
                "signal_date": "2021-01-01",
                "close_t": 100.0,
                "strategy": "E1R_regime_aware_v0_1_shell",
            }
        ]
        before = copy.deepcopy(payloads)

        normalized = (
            UptrendExecutionAdapter
            .normalize_legacy_pending_orders(payloads)
        )

        self.assertEqual(normalized, before)
        self.assertEqual(payloads, before)
        self.assertIsNot(normalized[0], payloads[0])

    def test_normalization_does_not_mutate_input(self) -> None:
        payloads = [
            {
                "sym": "AAA",
                "action": "BUY",
                "signal_date": "2021-01-01",
                "entry_type": "E1R_UPTREND_CONFIRMED",
                "target_size_units": 1.0,
            }
        ]
        before = copy.deepcopy(payloads)
        normalized = (
            UptrendExecutionAdapter
            .normalize_legacy_pending_orders(payloads)
        )
        self.assertEqual(payloads, before)
        self.assertEqual(normalized, before)


if __name__ == "__main__":
    unittest.main()
