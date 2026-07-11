from __future__ import annotations

import copy
import unittest
from types import SimpleNamespace

from e1r_engine.core import E1RCoreEngine
from e1r_engine.market_gate import MarketGateDecision
from e1r_engine.state import AccountState
from e1r_engine.uptrend_consumer import (
    UptrendConsumerInputs,
    UptrendDecisionConsumer,
)
from e1r_engine.uptrend_core import UptrendCore

TEST_DATE = "2026-07-10"


def make_snapshot(*, regime: str = "UPTREND"):
    return SimpleNamespace(
        date=TEST_DATE,
        universe=["AVGO", "EMG"],
        prices_by_symbol={
            "AVGO": SimpleNamespace(close=100.0),
            "EMG": SimpleNamespace(close=50.0),
        },
        indices={},
        regime=SimpleNamespace(
            spx_regime=regime,
            subclass=None,
        ),
        metadata={},
    )


def make_gate(
    *,
    allowed: bool = True,
    capacity: int = 3,
    date: str = TEST_DATE,
) -> MarketGateDecision:
    return MarketGateDecision(
        date=date,
        market_state="RISK_ON" if allowed else "CASH_MODE",
        entry_capacity=capacity,
        market_shock=False,
        market_risk_off=not allowed,
        market_entry_allowed=allowed,
        gate_state="ALLOW" if allowed else "RISK_OFF",
    )


def confirmed_signal() -> dict:
    return {
        "e1r_entry_type": "E1R_UPTREND_CONFIRMED",
        "leader_score": 96.0,
        "momentum_acceleration": 4.0,
        "rs_20d_improvement": 12.0,
        "close_t": 100.0,
        "e1r_entry_reason": [
            "rs_above_90",
            "leader_rank_top5",
        ],
    }


def emerging_signal() -> dict:
    return {
        "e1r_entry_type": "E1R_UPTREND_EMERGING",
        "leader_score": 98.0,
        "momentum_acceleration": 8.0,
        "rs_20d_improvement": 15.0,
        "close_t": 50.0,
        "e1r_entry_reason": ["rs_improving"],
    }


class TestUptrendConsumerIntegration(unittest.TestCase):
    def test_consumer_matches_direct_core_decision(self) -> None:
        account = AccountState.empty(date=TEST_DATE)
        signals = {
            "EMG": emerging_signal(),
            "AVGO": confirmed_signal(),
        }
        ranks = {
            "EMG": 1,
            "AVGO": 5,
        }

        direct = UptrendCore.decide_uptrend_buy(
            day_signals=signals,
            holdings_symbols=set(),
            leader_rank_all=ranks,
            market_entry_allowed=True,
            entry_capacity=3,
            max_positions=3,
        )

        consumed = UptrendDecisionConsumer.consume(
            inputs=UptrendConsumerInputs(
                date=TEST_DATE,
                day_signals=signals,
                leader_rank_all=ranks,
                market_gate_decision=make_gate(),
            ),
            account_state=account,
            max_positions=3,
        )

        self.assertEqual(
            consumed.decision.pre_rank_candidates,
            direct.pre_rank_candidates,
        )
        self.assertEqual(
            consumed.decision.ranked_candidates,
            direct.ranked_candidates,
        )
        self.assertEqual(
            consumed.decision.selected_buy["sym"],
            direct.selected_buy["sym"],
        )
        self.assertEqual(
            consumed.decision.selected_buy["target_size_units"],
            direct.selected_buy["target_size_units"],
        )

    def test_standard_buy_intent_has_no_legacy_payload(self) -> None:
        account = AccountState.empty(date=TEST_DATE)

        result = UptrendDecisionConsumer.consume(
            inputs=UptrendConsumerInputs(
                date=TEST_DATE,
                day_signals={"AVGO": confirmed_signal()},
                leader_rank_all={"AVGO": 1},
                market_gate_decision=make_gate(),
            ),
            account_state=account,
            max_positions=3,
        )

        self.assertEqual(len(result.order_intents), 1)
        order = result.order_intents[0]
        self.assertEqual(order.symbol, "AVGO")
        self.assertEqual(order.intent_type, "BUY")
        self.assertEqual(order.side, "BUY")
        self.assertNotIn("legacy_order_payload", order.metadata)
        self.assertFalse(
            result.metadata["legacy_order_payload_constructed"]
        )

    def test_consumer_does_not_mutate_inputs_or_account(self) -> None:
        account = AccountState.empty(date=TEST_DATE)
        signals = {"AVGO": confirmed_signal()}
        ranks = {"AVGO": 1}

        signals_before = copy.deepcopy(signals)
        ranks_before = copy.deepcopy(ranks)
        account_before = copy.deepcopy(account)

        result = UptrendDecisionConsumer.consume(
            inputs=UptrendConsumerInputs(
                date=TEST_DATE,
                day_signals=signals,
                leader_rank_all=ranks,
                market_gate_decision=make_gate(),
            ),
            account_state=account,
            max_positions=3,
        )

        self.assertEqual(signals, signals_before)
        self.assertEqual(ranks, ranks_before)
        self.assertEqual(account, account_before)
        self.assertIs(result.account_state_reference, account)

    def test_gate_blocks_buy(self) -> None:
        account = AccountState.empty(date=TEST_DATE)

        result = UptrendDecisionConsumer.consume(
            inputs=UptrendConsumerInputs(
                date=TEST_DATE,
                day_signals={"AVGO": confirmed_signal()},
                leader_rank_all={"AVGO": 1},
                market_gate_decision=make_gate(
                    allowed=False,
                    capacity=0,
                ),
            ),
            account_state=account,
            max_positions=3,
        )

        self.assertEqual(result.order_intents, ())
        self.assertIsNone(result.decision.selected_buy)
        self.assertFalse(result.metadata["market_gate_recomputed"])

    def test_core_step_uses_consumer_for_uptrend(self) -> None:
        account = AccountState.empty(date=TEST_DATE)

        result = E1RCoreEngine().step(
            make_snapshot(),
            account,
            uptrend_inputs=UptrendConsumerInputs(
                date=TEST_DATE,
                day_signals={"AVGO": confirmed_signal()},
                leader_rank_all={"AVGO": 1},
                market_gate_decision=make_gate(),
            ),
        )

        self.assertEqual(result.decision_trace.branch, "UPTREND")
        self.assertEqual(
            result.decision_trace.selected_symbols,
            ["AVGO"],
        )
        self.assertEqual(result.decision_trace.candidate_count, 1)
        self.assertEqual(len(result.order_intents), 1)
        self.assertEqual(
            result.order_intents[0].intent_type,
            "BUY",
        )
        self.assertEqual(result.fills, [])
        self.assertEqual(result.account_after.cash, account.cash)
        self.assertEqual(
            result.account_after.positions,
            account.positions,
        )

    def test_non_uptrend_input_is_rejected(self) -> None:
        account = AccountState.empty(date=TEST_DATE)
        inputs = UptrendConsumerInputs(
            date=TEST_DATE,
            day_signals={},
            leader_rank_all={},
            market_gate_decision=make_gate(),
        )

        with self.assertRaisesRegex(ValueError, "non-UPTREND"):
            E1RCoreEngine().step(
                make_snapshot(regime="DOWNTREND"),
                account,
                uptrend_inputs=inputs,
            )

    def test_snapshot_date_mismatch_is_rejected(self) -> None:
        account = AccountState.empty(date=TEST_DATE)
        inputs = UptrendConsumerInputs(
            date="2026-07-09",
            day_signals={},
            leader_rank_all={},
            market_gate_decision=make_gate(
                date="2026-07-09"
            ),
        )

        with self.assertRaisesRegex(
            ValueError,
            "date does not match",
        ):
            E1RCoreEngine().step(
                make_snapshot(),
                account,
                uptrend_inputs=inputs,
            )

    def test_gate_date_mismatch_is_rejected(self) -> None:
        account = AccountState.empty(date=TEST_DATE)
        inputs = UptrendConsumerInputs(
            date=TEST_DATE,
            day_signals={},
            leader_rank_all={},
            market_gate_decision=make_gate(
                date="2026-07-09"
            ),
        )

        with self.assertRaisesRegex(
            ValueError,
            "market_gate_decision_date_mismatch",
        ):
            UptrendDecisionConsumer.consume(
                inputs=inputs,
                account_state=account,
                max_positions=3,
            )


if __name__ == "__main__":
    unittest.main()
