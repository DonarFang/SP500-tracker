from __future__ import annotations
import unittest
from e1r_engine.core import E1RCoreEngine
from e1r_engine.market_state import MarketStateInputs

class EngineMarketStateGateIntegrationTests(unittest.TestCase):
    def test_full_on_allow(self):
        state, gate = E1RCoreEngine().evaluate_market_state_and_gate(
            inputs=MarketStateInputs(
                date="2026-07-17", spx_close=110.0, spx_ma50=100.0,
                spx_ma50_10d_ago=100.0, spx_day_return=0.0,
                ndx_close=110.0, ndx_ma50=100.0,
                sox_close=110.0, sox_ma50=100.0, max_positions=3,
            ),
            existing_positions_count=0,
        )
        self.assertEqual((state.market_state, state.entry_capacity, gate.gate_state), ("FULL_ON", 3, "ALLOW"))

    def test_shock(self):
        state, gate = E1RCoreEngine().evaluate_market_state_and_gate(
            inputs=MarketStateInputs(
                date="2026-07-17", spx_close=98.0, spx_ma50=100.0,
                spx_ma50_10d_ago=100.0, spx_day_return=-0.02,
                ndx_close=110.0, ndx_ma50=100.0,
                sox_close=110.0, sox_ma50=100.0, max_positions=3,
            ),
            existing_positions_count=3,
        )
        self.assertEqual((state.market_state, state.entry_capacity, gate.gate_state), ("CASH_MODE", 0, "SHOCK"))

if __name__ == "__main__":
    unittest.main(verbosity=2)
