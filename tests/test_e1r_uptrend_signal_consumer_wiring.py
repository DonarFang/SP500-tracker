from __future__ import annotations

import copy
import unittest

from e1r_engine.market_gate import MarketGateDecision
from e1r_engine.state import AccountState
from e1r_engine.uptrend_consumer import (
    UptrendDecisionConsumer,
)
from e1r_engine.uptrend_pipeline import (
    UptrendSignalConsumerPipeline,
)
from e1r_engine.uptrend_signal_adapter import (
    UptrendSignalAdapter,
)


DATE = "2026-07-10"


def increasing_series(
    *,
    start: float,
    daily_step: float,
    length: int = 100,
) -> list[float]:
    return [
        start + daily_step * index
        for index in range(length)
    ]


def prices() -> dict[str, list[float]]:
    return {
        "AAA": increasing_series(
            start=50.0,
            daily_step=1.0,
        ),
        "BBB": increasing_series(
            start=80.0,
            daily_step=0.4,
        ),
        "CCC": increasing_series(
            start=120.0,
            daily_step=-0.1,
        ),
    }


def gate(
    *,
    allowed: bool = True,
    capacity: int = 3,
    date: str = DATE,
) -> MarketGateDecision:
    return MarketGateDecision(
        date=date,
        market_state=(
            "RISK_ON"
            if allowed
            else "CASH_MODE"
        ),
        entry_capacity=capacity,
        market_shock=False,
        market_risk_off=not allowed,
        market_entry_allowed=allowed,
        gate_state=(
            "ALLOW"
            if allowed
            else "RISK_OFF"
        ),
    )


class TestUptrendSignalConsumerWiring(
    unittest.TestCase
):
    def test_pipeline_matches_manual_chain(self) -> None:
        symbols = ["AAA", "BBB", "CCC"]
        price_map = prices()
        account = AccountState.empty(date=DATE)
        gate_decision = gate()

        adapter_result = UptrendSignalAdapter.build(
            date=DATE,
            symbols=symbols,
            prices_by_symbol=price_map,
        )
        consumer_inputs = (
            adapter_result.to_consumer_inputs(
                market_gate_decision=gate_decision,
            )
        )
        manual_result = (
            UptrendDecisionConsumer.consume(
                inputs=consumer_inputs,
                account_state=account,
                max_positions=3,
            )
        )

        pipeline_result = (
            UptrendSignalConsumerPipeline.run(
                date=DATE,
                symbols=symbols,
                prices_by_symbol=price_map,
                market_gate_decision=gate_decision,
                account_state=account,
                max_positions=3,
            )
        )

        self.assertEqual(
            pipeline_result.adapter_result.day_signals,
            adapter_result.day_signals,
        )
        self.assertEqual(
            pipeline_result.adapter_result.leader_rank_all,
            adapter_result.leader_rank_all,
        )
        self.assertEqual(
            pipeline_result.consumer_result.decision,
            manual_result.decision,
        )
        self.assertEqual(
            pipeline_result.consumer_result.order_intents,
            manual_result.order_intents,
        )

    def test_pipeline_does_not_mutate_inputs(self) -> None:
        symbols = ["AAA", "BBB", "CCC"]
        price_map = prices()
        account = AccountState.empty(date=DATE)
        gate_decision = gate()

        symbols_before = copy.deepcopy(symbols)
        prices_before = copy.deepcopy(price_map)
        account_before = copy.deepcopy(account)
        gate_before = copy.deepcopy(gate_decision)

        UptrendSignalConsumerPipeline.run(
            date=DATE,
            symbols=symbols,
            prices_by_symbol=price_map,
            market_gate_decision=gate_decision,
            account_state=account,
            max_positions=3,
        )

        self.assertEqual(symbols, symbols_before)
        self.assertEqual(price_map, prices_before)
        self.assertEqual(account, account_before)
        self.assertEqual(gate_decision, gate_before)

    def test_gate_block_reaches_consumer(self) -> None:
        result = UptrendSignalConsumerPipeline.run(
            date=DATE,
            symbols=["AAA", "BBB", "CCC"],
            prices_by_symbol=prices(),
            market_gate_decision=gate(
                allowed=False,
                capacity=0,
            ),
            account_state=AccountState.empty(
                date=DATE
            ),
            max_positions=3,
        )

        self.assertIsNone(
            result.consumer_result.decision.selected_buy
        )
        self.assertEqual(
            result.consumer_result.order_intents,
            (),
        )
        self.assertFalse(
            result.metadata["market_gate_recomputed"]
        )

    def test_account_date_mismatch_rejected(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "account state date",
        ):
            UptrendSignalConsumerPipeline.run(
                date=DATE,
                symbols=["AAA"],
                prices_by_symbol={
                    "AAA": increasing_series(
                        start=50.0,
                        daily_step=1.0,
                    ),
                },
                market_gate_decision=gate(),
                account_state=AccountState.empty(
                    date="2026-07-09"
                ),
                max_positions=3,
            )

    def test_gate_date_mismatch_rejected(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "market gate date",
        ):
            UptrendSignalConsumerPipeline.run(
                date=DATE,
                symbols=["AAA"],
                prices_by_symbol={
                    "AAA": increasing_series(
                        start=50.0,
                        daily_step=1.0,
                    ),
                },
                market_gate_decision=gate(
                    date="2026-07-09"
                ),
                account_state=AccountState.empty(
                    date=DATE
                ),
                max_positions=3,
            )

    def test_negative_max_positions_rejected(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "max_positions",
        ):
            UptrendSignalConsumerPipeline.run(
                date=DATE,
                symbols=["AAA"],
                prices_by_symbol={
                    "AAA": increasing_series(
                        start=50.0,
                        daily_step=1.0,
                    ),
                },
                market_gate_decision=gate(),
                account_state=AccountState.empty(
                    date=DATE
                ),
                max_positions=-1,
            )

    def test_pipeline_metadata_tracks_chain(self) -> None:
        result = UptrendSignalConsumerPipeline.run(
            date=DATE,
            symbols=["AAA", "BBB", "CCC"],
            prices_by_symbol=prices(),
            market_gate_decision=gate(),
            account_state=AccountState.empty(
                date=DATE
            ),
            max_positions=3,
            metadata={
                "test_marker": "R23",
            },
        )

        self.assertEqual(
            result.metadata["pipeline"],
            "UptrendSignalConsumerPipeline",
        )
        self.assertEqual(
            result.metadata["adapter"],
            "UptrendSignalAdapter",
        )
        self.assertEqual(
            result.metadata["consumer"],
            "UptrendDecisionConsumer",
        )
        self.assertEqual(
            result.metadata["strategy_core"],
            "UptrendCore",
        )
        self.assertEqual(
            result.metadata["test_marker"],
            "R23",
        )
        self.assertFalse(
            result.metadata["account_mutated"]
        )
        self.assertFalse(
            result.metadata["order_execution_performed"]
        )


if __name__ == "__main__":
    unittest.main()
