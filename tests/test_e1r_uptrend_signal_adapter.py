from __future__ import annotations

import copy
import unittest

from e1r_engine.market_gate import MarketGateDecision
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


def base_signal(
    *,
    leader_score: float,
    rs_score: float = 50.0,
    rs_improvement: float = 0.0,
    momentum_score: float = 50.0,
    momentum_acceleration: float = 0.0,
    trend_health: float = 50.0,
    close_t: float = 100.0,
    ma20: float = 100.0,
    ma20_slope: float = 0.0,
    ma50: float = 100.0,
    ma50_slope: float = 0.0,
) -> dict:
    return {
        "symbol": "",
        "action": "HOLD",
        "trend_state": "Expansion",
        "momentum_score": momentum_score,
        "rs_score": rs_score,
        "leader_score": leader_score,
        "trend_health": trend_health,
        "close_t": close_t,
        "ma20": ma20,
        "ma20_slope": ma20_slope,
        "ma50": ma50,
        "ma50_slope": ma50_slope,
        "rs_prev20": 50.0,
        "rs_20d_improvement": rs_improvement,
        "momentum_acceleration": momentum_acceleration,
        "e1r_entry_type": None,
        "e1r_uptrend_emerging_eligible": False,
        "e1r_uptrend_confirmed_eligible": False,
        "e1r_entry_reason": [],
    }


def gate() -> MarketGateDecision:
    return MarketGateDecision(
        date=DATE,
        market_state="RISK_ON",
        entry_capacity=3,
        market_shock=False,
        market_risk_off=False,
        market_entry_allowed=True,
        gate_state="ALLOW",
    )


class TestUptrendSignalAdapter(unittest.TestCase):
    def test_build_produces_required_signal_fields(self) -> None:
        symbols = ["AAA", "BBB", "CCC"]
        prices = {
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

        result = UptrendSignalAdapter.build(
            date=DATE,
            symbols=symbols,
            prices_by_symbol=prices,
        )

        required = {
            "symbol",
            "action",
            "trend_state",
            "momentum_score",
            "rs_score",
            "leader_score",
            "trend_health",
            "close_t",
            "ma20",
            "ma20_slope",
            "ma50",
            "ma50_slope",
            "rs_prev20",
            "rs_20d_improvement",
            "momentum_acceleration",
            "e1r_entry_type",
            "e1r_uptrend_emerging_eligible",
            "e1r_uptrend_confirmed_eligible",
            "e1r_entry_reason",
        }

        self.assertEqual(
            set(result.day_signals),
            set(symbols),
        )

        for signal in result.day_signals.values():
            self.assertEqual(
                set(signal),
                required,
            )

    def test_short_history_is_excluded(self) -> None:
        result = UptrendSignalAdapter.build(
            date=DATE,
            symbols=["SHORT", "LONG"],
            prices_by_symbol={
                "SHORT": [100.0] * 59,
                "LONG": [100.0] * 61,
            },
        )

        self.assertNotIn(
            "SHORT",
            result.day_signals,
        )
        self.assertIn(
            "LONG",
            result.day_signals,
        )

    def test_input_prices_are_not_mutated(self) -> None:
        prices = {
            "AAA": increasing_series(
                start=50.0,
                daily_step=1.0,
            ),
            "BBB": increasing_series(
                start=80.0,
                daily_step=0.4,
            ),
        }
        before = copy.deepcopy(prices)

        UptrendSignalAdapter.build(
            date=DATE,
            symbols=["AAA", "BBB"],
            prices_by_symbol=prices,
        )

        self.assertEqual(prices, before)

    def test_rank_tie_preserves_symbol_order(self) -> None:
        source = {
            "BBB": base_signal(
                leader_score=80.0
            ),
            "AAA": base_signal(
                leader_score=80.0
            ),
        }

        _, ranks = (
            UptrendSignalAdapter
            .tag_uptrend_candidates(
                day_signals=source,
                symbol_order=["BBB", "AAA"],
            )
        )

        self.assertEqual(
            ranks,
            {
                "BBB": 1,
                "AAA": 2,
            },
        )

    def test_confirmed_threshold_contract(self) -> None:
        signal = base_signal(
            leader_score=75.0,
            rs_score=90.0,
            momentum_score=75.0,
            trend_health=70.0,
            close_t=101.0,
            ma50=100.0,
            ma50_slope=0.0,
        )

        tagged, ranks = (
            UptrendSignalAdapter
            .tag_uptrend_candidates(
                day_signals={"AAA": signal},
                symbol_order=["AAA"],
            )
        )

        self.assertEqual(ranks["AAA"], 1)
        self.assertEqual(
            tagged["AAA"]["e1r_entry_type"],
            "E1R_UPTREND_CONFIRMED",
        )
        self.assertTrue(
            tagged["AAA"][
                "e1r_uptrend_confirmed_eligible"
            ]
        )

    def test_emerging_threshold_contract(self) -> None:
        signal = base_signal(
            leader_score=74.0,
            rs_score=80.0,
            rs_improvement=10.0,
            momentum_score=70.0,
            momentum_acceleration=0.1,
            trend_health=65.0,
            close_t=101.0,
            ma20=100.0,
            ma20_slope=0.001,
            ma50=100.0,
            ma50_slope=-0.001,
        )

        tagged, _ = (
            UptrendSignalAdapter
            .tag_uptrend_candidates(
                day_signals={"AAA": signal},
                symbol_order=["AAA"],
            )
        )

        self.assertEqual(
            tagged["AAA"]["e1r_entry_type"],
            "E1R_UPTREND_EMERGING",
        )
        self.assertTrue(
            tagged["AAA"][
                "e1r_uptrend_emerging_eligible"
            ]
        )
        self.assertFalse(
            tagged["AAA"][
                "e1r_uptrend_confirmed_eligible"
            ]
        )

    def test_tagging_does_not_mutate_source(self) -> None:
        source = {
            "AAA": base_signal(
                leader_score=80.0,
                rs_score=90.0,
                momentum_score=80.0,
                trend_health=80.0,
                close_t=110.0,
                ma50=100.0,
            )
        }
        before = copy.deepcopy(source)

        UptrendSignalAdapter.tag_uptrend_candidates(
            day_signals=source,
            symbol_order=["AAA"],
        )

        self.assertEqual(source, before)

    def test_result_converts_to_consumer_inputs(self) -> None:
        result = UptrendSignalAdapter.build(
            date=DATE,
            symbols=["AAA"],
            prices_by_symbol={
                "AAA": increasing_series(
                    start=50.0,
                    daily_step=1.0,
                ),
            },
        )

        consumer_inputs = result.to_consumer_inputs(
            market_gate_decision=gate(),
        )

        self.assertEqual(
            consumer_inputs.date,
            DATE,
        )
        self.assertEqual(
            consumer_inputs.day_signals,
            result.day_signals,
        )
        self.assertEqual(
            consumer_inputs.leader_rank_all,
            result.leader_rank_all,
        )
        self.assertIsNot(
            consumer_inputs.day_signals,
            result.day_signals,
        )


if __name__ == "__main__":
    unittest.main()
