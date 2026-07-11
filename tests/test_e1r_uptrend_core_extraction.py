from __future__ import annotations

import copy
import unittest

from e1r_engine.uptrend_core import (
    UptrendBuyDecision,
    UptrendCore,
)


class TestUptrendCoreExtraction(unittest.TestCase):
    def setUp(self) -> None:
        self.confirmed = {
            "e1r_entry_type": "E1R_UPTREND_CONFIRMED",
            "leader_score": 96.03,
            "momentum_acceleration": 4.0,
            "rs_20d_improvement": 12.0,
            "close_t": 60.565498,
            "e1r_entry_reason": [
                "rs_above_90",
                "leader_rank_top5",
            ],
        }

        self.emerging = {
            "e1r_entry_type": "E1R_UPTREND_EMERGING",
            "leader_score": 93.0,
            "momentum_acceleration": 6.0,
            "rs_20d_improvement": 15.0,
            "close_t": 50.0,
            "e1r_entry_reason": [
                "rs_above_80",
            ],
        }

    def test_confirmed_has_priority_over_emerging(self) -> None:
        signals = {
            "EMG": self.emerging,
            "CFM": self.confirmed,
        }

        before = copy.deepcopy(signals)

        result = UptrendCore.decide_uptrend_buy(
            day_signals=signals,
            holdings_symbols=set(),
            leader_rank_all={
                "EMG": 1,
                "CFM": 5,
            },
            market_entry_allowed=True,
            entry_capacity=3,
            max_positions=3,
        )

        self.assertEqual(
            result.selected_buy["sym"],
            "CFM",
        )
        self.assertEqual(
            result.selected_buy[
                "target_size_units"
            ],
            1.0,
        )
        self.assertEqual(signals, before)

    def test_emerging_target_is_half_unit(self) -> None:
        result = UptrendCore.decide_uptrend_buy(
            day_signals={
                "EMG": self.emerging,
            },
            holdings_symbols=set(),
            leader_rank_all={
                "EMG": 2,
            },
            market_entry_allowed=True,
            entry_capacity=3,
            max_positions=3,
        )

        self.assertEqual(
            result.selected_buy["sym"],
            "EMG",
        )
        self.assertEqual(
            result.selected_buy[
                "target_size_units"
            ],
            0.5,
        )

    def test_gate_blocks_selection(self) -> None:
        result = UptrendCore.decide_uptrend_buy(
            day_signals={
                "CFM": self.confirmed,
            },
            holdings_symbols=set(),
            leader_rank_all={
                "CFM": 1,
            },
            market_entry_allowed=False,
            entry_capacity=3,
            max_positions=3,
        )

        self.assertIsNone(
            result.selected_buy
        )
        self.assertEqual(
            result.no_capacity_count,
            0,
        )

    def test_capacity_block_count_matches_candidates(self) -> None:
        result = UptrendCore.decide_uptrend_buy(
            day_signals={
                "CFM": self.confirmed,
                "EMG": self.emerging,
            },
            holdings_symbols={
                "A",
                "B",
                "C",
            },
            leader_rank_all={
                "CFM": 1,
                "EMG": 2,
            },
            market_entry_allowed=True,
            entry_capacity=3,
            max_positions=3,
        )

        self.assertIsNone(
            result.selected_buy
        )
        self.assertEqual(
            result.no_capacity_count,
            2,
        )

    def test_existing_holding_is_excluded(self) -> None:
        result = UptrendCore.decide_uptrend_buy(
            day_signals={
                "CFM": self.confirmed,
                "EMG": self.emerging,
            },
            holdings_symbols={
                "CFM",
            },
            leader_rank_all={
                "CFM": 1,
                "EMG": 2,
            },
            market_entry_allowed=True,
            entry_capacity=3,
            max_positions=3,
        )

        self.assertEqual(
            result.selected_buy["sym"],
            "EMG",
        )

    def test_trace_rows_preserve_tuple_fields(self) -> None:
        result = UptrendCore.decide_uptrend_buy(
            day_signals={
                "CFM": self.confirmed,
            },
            holdings_symbols=set(),
            leader_rank_all={
                "CFM": 4,
            },
            market_entry_allowed=True,
            entry_capacity=3,
            max_positions=3,
        )

        rows = UptrendBuyDecision.trace_rows(
            result.ranked_candidates
        )

        self.assertEqual(
            rows,
            [
                {
                    "entry_priority": 0,
                    "leader_rank_all": 4,
                    "negative_leader_score": -96.03,
                    "negative_momentum_acceleration": -4.0,
                    "negative_rs_20d_improvement": -12.0,
                    "symbol": "CFM",
                    "entry_type": "E1R_UPTREND_CONFIRMED",
                }
            ],
        )

    def test_order_payload_is_legacy_equivalent(self) -> None:
        selected = {
            "sym": "AVGO",
            "sig": self.confirmed,
            "entry_type": "E1R_UPTREND_CONFIRMED",
            "target_size_units": 1.0,
        }

        order = UptrendCore.build_uptrend_buy_order(
            date="2021-12-22",
            symbol="AVGO",
            signal=self.confirmed,
            selected_buy=selected,
            top_entry_rank={},
            leader_rank_all={
                "AVGO": 1,
            },
        )

        self.assertEqual(
            order,
            {
                "sym": "AVGO",
                "action": "BUY",
                "signal_date": "2021-12-22",
                "ls": 96.03,
                "close_t": 60.565498,
                "entry_rank": 1,
                "strategy": "E1R_UPTREND_EXECUTION_V0_1",
                "entry_mode": "e1r_uptrend_execution_v0_1",
                "primary_reason": "E1R_UPTREND_CONFIRMED",
                "reasons": [
                    "rs_above_90",
                    "leader_rank_top5",
                ],
                "e1r_entry_type": "E1R_UPTREND_CONFIRMED",
                "target_size_units": 1.0,
            },
        )


if __name__ == "__main__":
    unittest.main()
