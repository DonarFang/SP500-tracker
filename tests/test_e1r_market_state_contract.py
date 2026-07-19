from __future__ import annotations
import unittest
from e1r_engine.market_state import MarketStateConfig, MarketStateEvaluator, MarketStateInputs

def make_inputs(**kwargs):
    base = dict(
        date="2026-07-17",
        spx_close=110.0,
        spx_ma50=100.0,
        spx_ma50_10d_ago=100.0,
        spx_day_return=0.0,
        ndx_close=110.0,
        ndx_ma50=100.0,
        sox_close=110.0,
        sox_ma50=100.0,
        max_positions=3,
    )
    base.update(kwargs)
    return MarketStateInputs(**base)

class MarketStateContractTests(unittest.TestCase):
    def setUp(self):
        self.cfg = MarketStateConfig()

    def test_full_on(self):
        r = MarketStateEvaluator.evaluate(self.cfg, make_inputs())
        self.assertEqual((r.market_state, r.entry_capacity), ("FULL_ON", 3))

    def test_cautious(self):
        r = MarketStateEvaluator.evaluate(self.cfg, make_inputs(sox_close=90.0))
        self.assertEqual(r.leadership_ratio, 2/3)
        self.assertEqual((r.market_state, r.entry_capacity), ("CAUTIOUS_ON", 2))

    def test_cash_leadership(self):
        r = MarketStateEvaluator.evaluate(
            self.cfg, make_inputs(ndx_close=90.0, sox_close=90.0)
        )
        self.assertEqual((r.market_state, r.entry_capacity), ("CASH_MODE", 0))

    def test_negative_slope(self):
        r = MarketStateEvaluator.evaluate(
            self.cfg, make_inputs(spx_ma50=99.0, spx_ma50_10d_ago=100.0)
        )
        self.assertEqual(r.market_state, "CASH_MODE")

    def test_shock_boundary(self):
        a = MarketStateEvaluator.evaluate(
            self.cfg, make_inputs(spx_day_return=-0.0199)
        )
        b = MarketStateEvaluator.evaluate(
            self.cfg, make_inputs(spx_day_return=-0.02)
        )
        self.assertFalse(a.shock_active)
        self.assertTrue(b.shock_active)
        self.assertEqual(b.market_state, "CASH_MODE")

    def test_gate_disabled(self):
        r = MarketStateEvaluator.evaluate(
            MarketStateConfig(market_gate_enabled=False),
            make_inputs(
                spx_day_return=-0.10,
                ndx_close=90.0,
                sox_close=90.0,
                spx_ma50=90.0,
                spx_ma50_10d_ago=100.0,
            ),
        )
        self.assertEqual((r.market_state, r.entry_capacity), ("FULL_ON", 3))

if __name__ == "__main__":
    unittest.main(verbosity=2)
