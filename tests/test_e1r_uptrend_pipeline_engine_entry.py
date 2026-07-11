from __future__ import annotations

import copy
import unittest
from types import SimpleNamespace

from e1r_engine.core import E1RCoreEngine
from e1r_engine.market_gate import MarketGateDecision
from e1r_engine.state import AccountState
from e1r_engine.uptrend_pipeline import (
    UptrendPipelineInputs,
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


def histories() -> dict[str, list[float]]:
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


def snapshot(
    *,
    regime: str = "UPTREND",
):
    price_histories = histories()

    return SimpleNamespace(
        date=DATE,
        universe=["AAA", "BBB", "CCC"],
        prices_by_symbol={
            symbol: SimpleNamespace(
                close=values[-1]
            )
            for symbol, values
            in price_histories.items()
        },
        indices={},
        regime=SimpleNamespace(
            spx_regime=regime,
            subclass=None,
        ),
        metadata={},
    )


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


def pipeline_inputs(
    *,
    date: str = DATE,
    gate_date: str = DATE,
) -> UptrendPipelineInputs:
    return UptrendPipelineInputs(
        date=date,
        symbols=["AAA", "BBB", "CCC"],
        prices_by_symbol=histories(),
        market_gate_decision=gate(
            date=gate_date
        ),
        metadata={"test_marker": "R24"},
    )


class TestUptrendPipelineEngineEntry(
    unittest.TestCase
):
    def test_engine_entry_matches_direct_pipeline(self) -> None:
        account = AccountState.empty(date=DATE)
        inputs = pipeline_inputs()

        direct = UptrendSignalConsumerPipeline.run(
            date=inputs.date,
            symbols=inputs.symbols,
            prices_by_symbol=inputs.prices_by_symbol,
            market_gate_decision=(
                inputs.market_gate_decision
            ),
            account_state=account,
            max_positions=3,
            market_score_default=(
                inputs.market_score_default
            ),
            ls60_exit_mode=inputs.ls60_exit_mode,
            metadata=inputs.metadata,
        )

        engine_result = E1RCoreEngine().step(
            snapshot(),
            account,
            uptrend_pipeline_inputs=inputs,
        )

        self.assertEqual(
            engine_result.decision_trace.branch,
            "UPTREND",
        )
        self.assertEqual(
            engine_result.decision_trace.candidate_count,
            direct.consumer_result.decision.candidate_count,
        )
        self.assertEqual(
            engine_result.decision_trace.selected_symbols,
            list(
                direct.consumer_result.metadata[
                    "selected_symbols"
                ]
            ),
        )
        engine_strategy_orders = [
            order
            for order in engine_result.order_intents
            if order.intent_type != "NOOP"
        ]

        self.assertEqual(
            engine_strategy_orders,
            list(
                direct.consumer_result.order_intents
            ),
        )

        if direct.consumer_result.order_intents:
            self.assertNotIn(
                "NOOP",
                {
                    order.intent_type
                    for order in engine_result.order_intents
                },
            )
        else:
            self.assertEqual(
                [
                    order.intent_type
                    for order in engine_result.order_intents
                ],
                ["NOOP"],
            )

    def test_engine_pipeline_matches_manual_input_path(self) -> None:
        account = AccountState.empty(date=DATE)
        inputs = pipeline_inputs()

        adapter_result = UptrendSignalAdapter.build(
            date=inputs.date,
            symbols=inputs.symbols,
            prices_by_symbol=inputs.prices_by_symbol,
            market_score_default=(
                inputs.market_score_default
            ),
            ls60_exit_mode=inputs.ls60_exit_mode,
        )

        manual_inputs = (
            adapter_result.to_consumer_inputs(
                market_gate_decision=(
                    inputs.market_gate_decision
                ),
            )
        )

        pipeline_result = E1RCoreEngine().step(
            snapshot(),
            account,
            uptrend_pipeline_inputs=inputs,
        )

        manual_result = E1RCoreEngine().step(
            snapshot(),
            account,
            uptrend_inputs=manual_inputs,
        )

        self.assertEqual(
            pipeline_result.decision_trace.candidate_count,
            manual_result.decision_trace.candidate_count,
        )
        self.assertEqual(
            pipeline_result.decision_trace.selected_symbols,
            manual_result.decision_trace.selected_symbols,
        )
        self.assertEqual(
            pipeline_result.order_intents,
            manual_result.order_intents,
        )
        self.assertEqual(
            pipeline_result.account_after,
            manual_result.account_after,
        )

    def test_pipeline_entry_does_not_mutate_inputs(self) -> None:
        account = AccountState.empty(date=DATE)
        inputs = pipeline_inputs()

        account_before = copy.deepcopy(account)
        histories_before = copy.deepcopy(
            inputs.prices_by_symbol
        )
        gate_before = copy.deepcopy(
            inputs.market_gate_decision
        )

        result = E1RCoreEngine().step(
            snapshot(),
            account,
            uptrend_pipeline_inputs=inputs,
        )

        self.assertEqual(account, account_before)
        self.assertEqual(
            inputs.prices_by_symbol,
            histories_before,
        )
        self.assertEqual(
            inputs.market_gate_decision,
            gate_before,
        )
        self.assertEqual(result.fills, [])
        self.assertEqual(
            result.account_after.cash,
            account.cash,
        )
        self.assertEqual(
            result.account_after.positions,
            account.positions,
        )

    def test_gate_block_reaches_engine_result(self) -> None:
        inputs = UptrendPipelineInputs(
            date=DATE,
            symbols=["AAA", "BBB", "CCC"],
            prices_by_symbol=histories(),
            market_gate_decision=gate(
                allowed=False,
                capacity=0,
            ),
        )

        result = E1RCoreEngine().step(
            snapshot(),
            AccountState.empty(date=DATE),
            uptrend_pipeline_inputs=inputs,
        )

        self.assertEqual(
            [
                order.intent_type
                for order in result.order_intents
            ],
            ["NOOP"],
        )
        self.assertEqual(
            result.order_intents[0].reason,
            "engine_f_shell_no_positions_noop",
        )
        self.assertEqual(
            result.decision_trace.selected_symbols,
            [],
        )
        self.assertTrue(
            result.metadata[
                "uptrend_pipeline_active"
            ]
        )

    def test_non_uptrend_route_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "non-UPTREND",
        ):
            E1RCoreEngine().step(
                snapshot(regime="DOWNTREND"),
                AccountState.empty(date=DATE),
                uptrend_pipeline_inputs=(
                    pipeline_inputs()
                ),
            )

    def test_mutually_exclusive_inputs_rejected(self) -> None:
        inputs = pipeline_inputs()
        adapter_result = UptrendSignalAdapter.build(
            date=inputs.date,
            symbols=inputs.symbols,
            prices_by_symbol=inputs.prices_by_symbol,
        )

        manual_inputs = (
            adapter_result.to_consumer_inputs(
                market_gate_decision=(
                    inputs.market_gate_decision
                ),
            )
        )

        with self.assertRaisesRegex(
            ValueError,
            "mutually exclusive",
        ):
            E1RCoreEngine().step(
                snapshot(),
                AccountState.empty(date=DATE),
                uptrend_inputs=manual_inputs,
                uptrend_pipeline_inputs=inputs,
            )

    def test_pipeline_date_mismatch_rejected(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "date does not match",
        ):
            E1RCoreEngine().step(
                snapshot(),
                AccountState.empty(date=DATE),
                uptrend_pipeline_inputs=(
                    pipeline_inputs(
                        date="2026-07-09",
                        gate_date="2026-07-09",
                    )
                ),
            )


if __name__ == "__main__":
    unittest.main()
