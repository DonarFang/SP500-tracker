from __future__ import annotations

import unittest

from e1r_engine.contracts import (
    DailyBar,
    MarketSnapshot,
    RegimeRecord,
)
from e1r_engine.core import E1RCoreEngine
from e1r_engine.market_gate import MarketGateDecision
from e1r_engine.state import AccountState
from e1r_engine.uptrend_consumer import UptrendConsumerInputs
from e1r_engine.uptrend_execution_adapter import (
    UptrendExecutionAdapter,
)


class TestUptrendFormalReplacement(unittest.TestCase):
    def test_engine_buy_maps_to_exact_legacy_payload(self) -> None:
        date = "2026-01-02"
        signal = {
            "e1r_entry_type": "E1R_UPTREND_CONFIRMED",
            "e1r_entry_reason": ["confirmed"],
            "leader_score": 95.0,
            "momentum_acceleration": 2.0,
            "rs_20d_improvement": 3.0,
            "close_t": 100.0,
        }
        snapshot = MarketSnapshot(
            date=date,
            universe=["AAA"],
            prices_by_symbol={
                "AAA": DailyBar(
                    date=date,
                    open=None,
                    high=None,
                    low=None,
                    close=100.0,
                    volume=None,
                )
            },
            indices={},
            regime=RegimeRecord(
                date=date,
                spx_regime="UPTREND",
            ),
        )
        gate = MarketGateDecision(
            date=date,
            market_state="FULL_ON",
            entry_capacity=3,
            market_shock=False,
            market_risk_off=False,
            market_entry_allowed=True,
            gate_state="ALLOW",
        )
        result = E1RCoreEngine().step(
            snapshot,
            AccountState.empty(date=date),
            uptrend_inputs=UptrendConsumerInputs(
                date=date,
                day_signals={"AAA": signal},
                leader_rank_all={"AAA": 1},
                market_gate_decision=gate,
            ),
        )
        buy = [
            order
            for order in result.order_intents
            if order.intent_type == "BUY"
        ]
        self.assertEqual(len(buy), 1)
        payload = (
            UptrendExecutionAdapter
            .to_legacy_pending_order(buy[0])
        )
        self.assertEqual(
            payload,
            {
                "sym": "AAA",
                "action": "BUY",
                "signal_date": date,
                "ls": 95.0,
                "close_t": 100.0,
                "entry_rank": 1,
                "strategy": "E1R_UPTREND_EXECUTION_V0_1",
                "entry_mode": "e1r_uptrend_execution_v0_1",
                "primary_reason": "E1R_UPTREND_CONFIRMED",
                "reasons": ["confirmed"],
                "e1r_entry_type": "E1R_UPTREND_CONFIRMED",
                "target_size_units": 1.0,
            },
        )


if __name__ == "__main__":
    unittest.main()
