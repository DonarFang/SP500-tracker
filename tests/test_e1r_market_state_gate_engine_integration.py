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
        from e1r_engine.market_state import (
            MarketStateConfig,
            MarketStateEvaluator,
            MarketStateInputs,
        )
        from e1r_engine.market_gate import (
            MarketGateConfig,
            MarketGateEvaluator,
            MarketGateInputs,
        )
        state = MarketStateEvaluator.evaluate(
            MarketStateConfig(
                market_shock_gate_enabled=True,
                market_shock_daily_return=-0.02,
            ),
            MarketStateInputs(
                date="2021-05-12",
                spx_close=110.0,
                spx_ma50=100.0,
                spx_ma50_10d_ago=99.0,
                spx_day_return=-0.02,
                ndx_close=110.0,
                ndx_ma50=100.0,
                sox_close=110.0,
                sox_ma50=100.0,
                max_positions=3,
            ),
        )
        gate = MarketGateEvaluator.evaluate(
            MarketGateConfig(
                variant="D3_RISK_OFF_PLUS_SHOCK_GATE",
                market_gate_enabled=True,
                risk_off_below_spx_ma50=True,
                market_shock_gate_enabled=True,
                market_shock_daily_return=-0.02,
            ),
            MarketGateInputs(
                date=state.date,
                spx_close=state.spx_close,
                spx_ma50=state.spx_ma50,
                spx_day_return=state.spx_day_return,
                market_state=state.market_state,
                entry_capacity=state.entry_capacity,
                existing_positions_count=0,
            ),
        )
        assert state.shock_active is True
        assert state.market_state == "CASH_MODE"
        assert state.entry_capacity == 0
        assert gate.market_shock is True
        assert gate.gate_state == "SHOCK"

    def test_engine_owns_canonical_evaluator_configs(self):
        from e1r_engine.core import E1RCoreEngine
        engine = E1RCoreEngine()
        state = engine.config.market_state_config
        gate = engine.config.market_gate_config
        self.assertTrue(state.market_gate_enabled)
        self.assertFalse(state.market_shock_gate_enabled)
        self.assertTrue(state.use_ma50_slope)
        self.assertTrue(state.use_index_leadership)
        self.assertEqual(gate.variant, "D2_RISK_OFF_GATE")
        self.assertTrue(gate.market_gate_enabled)
        self.assertFalse(gate.risk_off_below_spx_ma50)
        self.assertFalse(gate.market_shock_gate_enabled)

    def test_engine_default_contract_matches_formal_5y_d2(self):
        from e1r_engine.core import E1RCoreEngine
        engine = E1RCoreEngine()
        self.assertEqual(
            engine.config.market_gate_config.variant,
            "D2_RISK_OFF_GATE",
        )
        self.assertFalse(
            engine.config.market_gate_config.risk_off_below_spx_ma50
        )
        self.assertFalse(
            engine.config.market_gate_config.market_shock_gate_enabled
        )
        self.assertFalse(
            engine.config.market_state_config.market_shock_gate_enabled
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
