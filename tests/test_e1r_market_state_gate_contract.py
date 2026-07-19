from __future__ import annotations
import unittest
from e1r_engine.market_gate import MarketGateConfig, MarketGateEvaluator, MarketGateInputs
from e1r_engine.market_state import MarketStateConfig, MarketStateEvaluator, MarketStateInputs

def evaluate_chain(spx_day_return=0.0, sox_close=110.0, spx_ma50=100.0, spx_ma50_10d_ago=100.0):
    state = MarketStateEvaluator.evaluate(
        MarketStateConfig(),
        MarketStateInputs(
            date="2026-07-17",
            spx_close=110.0,
            spx_ma50=spx_ma50,
            spx_ma50_10d_ago=spx_ma50_10d_ago,
            spx_day_return=spx_day_return,
            ndx_close=110.0,
            ndx_ma50=100.0,
            sox_close=sox_close,
            sox_ma50=100.0,
            max_positions=3,
        ),
    )
    gate = MarketGateEvaluator.evaluate(
        MarketGateConfig(),
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
    return state, gate

class MarketStateGateContractTests(unittest.TestCase):
    def test_full_on_allow(self):
        s, g = evaluate_chain()
        self.assertEqual((s.market_state, g.gate_state), ("FULL_ON", "ALLOW"))

    def test_cautious_allow(self):
        s, g = evaluate_chain(sox_close=90.0)
        self.assertEqual((s.market_state, s.entry_capacity, g.gate_state), ("CAUTIOUS_ON", 2, "ALLOW"))

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

    def test_risk_off(self):
        s, g = evaluate_chain(spx_ma50=99.0, spx_ma50_10d_ago=100.0)
        self.assertEqual((s.market_state, g.gate_state), ("CASH_MODE", "RISK_OFF"))

    def test_action_contract(self):
        _, g = evaluate_chain(spx_day_return=-0.02)
        self.assertEqual(g.blocked_actions, ("BUY", "ADD"))
        self.assertEqual(g.unaffected_actions, ("HOLD", "REDUCE", "EXIT"))

if __name__ == "__main__":
    unittest.main(verbosity=2)
