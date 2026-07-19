from __future__ import annotations
import unittest
from e1r_engine.core import (
    E1RCoreEngine,
    E1RCoreEngineConfig,
)
from e1r_engine.market_gate import MarketGateConfig
from e1r_engine.market_state import MarketStateConfig
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

    def test_engine_owns_canonical_evaluator_configs(self):
        state_config = MarketStateConfig()
        gate_config = MarketGateConfig()
        engine = E1RCoreEngine(
            config=E1RCoreEngineConfig(
                max_positions=3,
                market_state_config=state_config,
                market_gate_config=gate_config,
            )
        )

        self.assertIs(
            engine.config.market_state_config,
            state_config,
        )
        self.assertIs(
            engine.config.market_gate_config,
            gate_config,
        )

        state, gate = engine.evaluate_market_state_and_gate(
            inputs=MarketStateInputs(
                date="2026-07-17",
                spx_close=98.0,
                spx_ma50=100.0,
                spx_ma50_10d_ago=100.0,
                spx_day_return=-0.02,
                ndx_close=110.0,
                ndx_ma50=100.0,
                sox_close=110.0,
                sox_ma50=100.0,
                max_positions=3,
            ),
            existing_positions_count=3,
        )

        self.assertEqual(state.market_state, "CASH_MODE")
        self.assertEqual(state.entry_capacity, 0)
        self.assertEqual(gate.gate_state, "SHOCK")
        self.assertTrue(gate.market_shock)

    def test_engine_default_contract_is_canonical_max3_d3(self):
        engine = E1RCoreEngine()

        self.assertEqual(engine.config.max_positions, 3)
        self.assertEqual(
            engine.config.market_gate_config.variant,
            "D3_RISK_OFF_PLUS_SHOCK_GATE",
        )
        self.assertTrue(
            engine.config.market_state_config.market_shock_gate_enabled
        )
        self.assertTrue(
            engine.config.market_gate_config.market_shock_gate_enabled
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
