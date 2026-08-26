from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from e1r_engine.contracts import (
    DailyBar,
    MarketSnapshot,
    RegimeRecord,
)
from e1r_engine.forward_runtime import (
    ENGINE_ID,
    FIRST_FORWARD_MARKET_DATE,
    CanonicalDailyDecisionRouter,
    ForwardAccountRepository,
    ForwardDatePlanner,
    ForwardRuntimeState,
    OfficialForwardArtifactWriter,
    PendingOrderLedger,
    PendingOrderRecord,
    RUNTIME_SCHEMA_VERSION,
    T1ExecutionEngine,
    account_from_dict,
    deterministic_id,
)
from e1r_engine.state import (
    AccountState,
    OrderIntent,
    PositionState,
)


class FakeRouter:
    def route(
        self,
        *,
        date,
        spx_regime,
        subclass,
    ):
        class Route:
            branch = (
                "UPTREND"
                if spx_regime == "UPTREND"
                else "NO_TRADE"
            )

        return Route()


class FakeEngine:
    def __init__(self):
        self.router = FakeRouter()

    def step(
        self,
        snapshot,
        account,
        *,
        uptrend_inputs=None,
        entry_atr20_provider=None,
    ):
        class Result:
            order_intents = [
                OrderIntent(
                    date=snapshot.date,
                    symbol="TEST",
                    intent_type="BUY",
                    side="BUY",
                    target_quantity=None,
                    quantity_delta=None,
                    reason="synthetic_test",
                    branch="UPTREND",
                    metadata={
                        "target_fraction_of_equity": 0.10,
                        "target_size_units": 1.0,
                    },
                )
            ]
            decision_trace = {
                "source": "FakeEngine.step"
            }

        assert uptrend_inputs is not None
        assert entry_atr20_provider is None
        return Result()


class SharedRuntimeImplementationTests(
    unittest.TestCase
):
    def test_date_planner_is_open_ended_and_incremental(
        self,
    ) -> None:
        planner = ForwardDatePlanner(
            [
                "2026-06-16",
                "2026-06-17",
                "2026-06-18",
                "2026-06-19",
            ]
        )

        self.assertEqual(
            planner.plan(
                last_committed_date=None,
                latest_complete_common_data_date=(
                    "2026-06-18"
                ),
            ),
            [
                "2026-06-17",
                "2026-06-18",
            ],
        )

        self.assertEqual(
            planner.plan(
                last_committed_date="2026-06-18",
                latest_complete_common_data_date=(
                    "2026-06-19"
                ),
            ),
            ["2026-06-19"],
        )

    def test_order_and_fill_identity_are_deterministic(
        self,
    ) -> None:
        intent = OrderIntent(
            date="2026-06-19",
            symbol="TEST",
            intent_type="BUY",
            side="BUY",
            target_quantity=None,
            quantity_delta=None,
            reason="test",
            branch="UPTREND",
            metadata={},
        )

        first = PendingOrderRecord.from_intent(
            intent,
            sequence=1,
        )
        second = PendingOrderRecord.from_intent(
            intent,
            sequence=1,
        )

        self.assertEqual(
            first.order_id,
            second.order_id,
        )

        fill_id_1 = deterministic_id(
            ENGINE_ID,
            first.order_id,
            "2026-06-22",
            "BUY",
        )

        fill_id_2 = deterministic_id(
            ENGINE_ID,
            first.order_id,
            "2026-06-22",
            "BUY",
        )

        self.assertEqual(fill_id_1, fill_id_2)

    def test_t1_execution_uses_exit_before_buy(
        self,
    ) -> None:
        old_position = PositionState(
            symbol="OLD",
            quantity=10.0,
            avg_cost=100.0,
            last_price=100.0,
            market_value=1000.0,
            unrealized_pnl=0.0,
            entry_date="2026-06-01",
            last_update_date="2026-06-19",
            metadata={
                "origin_branch": "UPTREND",
                "size_units": 1.0,
                "remaining_cost_basis": 1000.0,
            },
        )

        account = AccountState(
            date="2026-06-19",
            cash=0.0,
            positions={"OLD": old_position},
            total_equity=1000.0,
            positions_value=1000.0,
            open_positions_count=1,
            metadata={},
        )

        exit_intent = OrderIntent(
            date="2026-06-19",
            symbol="OLD",
            intent_type="EXIT",
            side="SELL",
            target_quantity=0.0,
            quantity_delta=-10.0,
            reason="test_exit",
            branch="UPTREND",
            metadata={},
        )

        buy_intent = OrderIntent(
            date="2026-06-19",
            symbol="NEW",
            intent_type="BUY",
            side="BUY",
            target_quantity=None,
            quantity_delta=None,
            reason="test_buy",
            branch="UPTREND",
            metadata={
                "target_fraction_of_equity": 0.50,
                "target_size_units": 1.0,
                "origin_branch": "UPTREND",
            },
        )

        pending = PendingOrderLedger.create(
            [buy_intent, exit_intent]
        )

        result = T1ExecutionEngine().execute(
            execution_date="2026-06-22",
            account=account,
            pending_orders=pending,
            bars_by_symbol={
                "OLD": DailyBar(
                    date="2026-06-22",
                    open=101.0,
                    high=102.0,
                    low=99.0,
                    close=100.0,
                    volume=None,
                ),
                "NEW": DailyBar(
                    date="2026-06-22",
                    open=50.0,
                    high=51.0,
                    low=49.0,
                    close=50.0,
                    volume=None,
                ),
            },
        )

        self.assertNotIn(
            "OLD",
            result.account_after.positions,
        )
        self.assertIn(
            "NEW",
            result.account_after.positions,
        )
        self.assertEqual(
            len(result.fills),
            2,
        )
        self.assertFalse(
            result.account_after.metadata[
                "sim_end_performed"
            ]
        )

    def test_sideways_cash_contract_is_bounded(
        self,
    ) -> None:
        account = AccountState.empty(
            "2026-06-19",
            initial_cash=100000.0,
        )

        intents = [
            OrderIntent(
                date="2026-06-19",
                symbol=symbol,
                intent_type="BUY",
                side="BUY",
                target_quantity=None,
                quantity_delta=None,
                reason="sideways_test",
                branch="SIDEWAYS_MA_CONFLICT",
                metadata={
                    "origin_branch": (
                        "SIDEWAYS_MA_CONFLICT"
                    ),
                    "target_fraction_of_tradable_cash": (
                        0.10
                    ),
                    "capital_fraction_of_tradable_cash": (
                        0.30
                    ),
                },
            )
            for symbol in ("A", "B", "C")
        ]

        result = T1ExecutionEngine().execute(
            execution_date="2026-06-22",
            account=account,
            pending_orders=PendingOrderLedger.create(
                intents
            ),
            bars_by_symbol={
                symbol: DailyBar(
                    date="2026-06-22",
                    open=100.0,
                    high=100.0,
                    low=100.0,
                    close=100.0,
                    volume=None,
                )
                for symbol in ("A", "B", "C")
            },
        )

        spent = (
            100000.0
            - result.account_after.cash
        )

        self.assertLessEqual(
            spent,
            30000.0 + 1e-6,
        )
        self.assertEqual(
            result.account_after.open_positions_count,
            3,
        )

        for position in (
            result.account_after.positions.values()
        ):
            self.assertEqual(
                position.metadata["origin_branch"],
                "SIDEWAYS_MA_CONFLICT",
            )

    def test_repository_round_trip_preserves_origin(
        self,
    ) -> None:
        account = account_from_dict(
            {
                "date": "2026-06-16",
                "cash": 70000.0,
                "positions": {
                    "MRVL": {
                        "symbol": "MRVL",
                        "remaining_shares": 10.0,
                        "average_cost": 70.0,
                        "last_price": 72.0,
                        "remaining_cost_basis": 700.0,
                        "size_units": 1.0,
                        "origin_branch": "UPTREND",
                    }
                },
            }
        )

        state = ForwardRuntimeState(
            schema_version=RUNTIME_SCHEMA_VERSION,
            engine_id=ENGINE_ID,
            seed_date="2026-06-16",
            first_forward_market_date=(
                FIRST_FORWARD_MARKET_DATE
            ),
            last_committed_date=None,
            account=account,
            pending_orders=[],
            closed_trades=[],
            equity_history=[],
            metadata={
                "sim_end_performed": False,
            },
        )

        with tempfile.TemporaryDirectory() as temp:
            repository = ForwardAccountRepository(
                Path(temp)
            )
            repository.initialize(state)
            loaded = repository.load()

            self.assertEqual(
                loaded.account.positions[
                    "MRVL"
                ].metadata["origin_branch"],
                "UPTREND",
            )

    def test_decision_router_calls_engine_for_uptrend(
        self,
    ) -> None:
        router = CanonicalDailyDecisionRouter(
            engine=FakeEngine()
        )

        snapshot = MarketSnapshot(
            date="2026-06-19",
            universe=["TEST"],
            prices_by_symbol={
                "TEST": DailyBar(
                    date="2026-06-19",
                    open=100.0,
                    high=101.0,
                    low=99.0,
                    close=100.0,
                    volume=None,
                )
            },
            indices={},
            regime=RegimeRecord(
                date="2026-06-19",
                spx_regime="UPTREND",
                subclass="NO_SUBCLASS",
            ),
            metadata={},
        )

        result = router.decide(
            snapshot=snapshot,
            account=AccountState.empty(
                "2026-06-19"
            ),
            uptrend_inputs={
                "synthetic": True,
            },
        )

        self.assertEqual(
            result.metadata["decision_source"],
            "E1RCoreEngine.step",
        )

        self.assertEqual(
            result.order_intents[0].intent_type,
            "BUY",
        )

    def test_artifact_writer_never_writes_sim_end(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            writer = OfficialForwardArtifactWriter(
                root
            )

            account = AccountState.empty(
                "2026-06-19"
            )

            state = ForwardRuntimeState(
                schema_version=(
                    RUNTIME_SCHEMA_VERSION
                ),
                engine_id=ENGINE_ID,
                seed_date="2026-06-16",
                first_forward_market_date=(
                    "2026-06-17"
                ),
                last_committed_date=(
                    "2026-06-19"
                ),
                account=account,
                pending_orders=[],
                closed_trades=[],
                equity_history=[],
                metadata={
                    "sim_end_performed": False,
                },
            )

            class Result:
                resolved_orders = []
                skipped_orders = []
                closed_trades = []

            manifest = writer.write_daily(
                trading_date="2026-06-19",
                state=state,
                order_intents=[],
                fills=[],
                decision_trace={
                    "branch": "NO_TRADE"
                },
                execution_result=Result(),
                source_hashes={},
                runtime_commit="synthetic",
            )

            self.assertFalse(
                manifest["sim_end_performed"]
            )

            serialized = json.dumps(
                manifest
            )

            self.assertNotIn(
                "SIM_END_LIQUIDATION",
                serialized,
            )


def run_tests() -> None:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        SharedRuntimeImplementationTests
    )

    result = unittest.TextTestRunner(
        verbosity=2
    ).run(suite)

    if not result.wasSuccessful():
        raise SystemExit(1)


if __name__ == "__main__":
    run_tests()
