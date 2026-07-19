from __future__ import annotations

import unittest

from e1r_engine.core import E1RCoreEngine
from e1r_engine.market_gate import MarketGateConfig
from e1r_engine.market_state import MarketStateConfig


class FormalFiveYearMarketConfigTests(unittest.TestCase):
    def test_market_state_defaults(self) -> None:
        config = MarketStateConfig()
        self.assertTrue(config.market_gate_enabled)
        self.assertFalse(config.market_shock_gate_enabled)
        self.assertEqual(config.market_shock_daily_return, -0.02)
        self.assertTrue(config.use_ma50_slope)
        self.assertTrue(config.use_index_leadership)
        self.assertEqual(config.cash_leadership_threshold, 2.0 / 3.0)
        self.assertEqual(config.full_on_leadership_threshold, 1.0)

    def test_market_gate_defaults(self) -> None:
        config = MarketGateConfig()
        self.assertEqual(config.variant, "D2_RISK_OFF_GATE")
        self.assertTrue(config.market_gate_enabled)
        self.assertFalse(config.risk_off_below_spx_ma50)
        self.assertFalse(config.market_shock_gate_enabled)
        self.assertEqual(config.market_shock_daily_return, -0.02)

    def test_engine_consumes_formal_defaults(self) -> None:
        engine = E1RCoreEngine()
        state = engine.config.market_state_config
        gate = engine.config.market_gate_config

        self.assertFalse(state.market_shock_gate_enabled)
        self.assertEqual(gate.variant, "D2_RISK_OFF_GATE")
        self.assertFalse(gate.risk_off_below_spx_ma50)
        self.assertFalse(gate.market_shock_gate_enabled)


if __name__ == "__main__":
    unittest.main(verbosity=2)
