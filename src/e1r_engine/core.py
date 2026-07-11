from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from e1r_engine.contracts import MarketSnapshot
from e1r_engine.regime_router import RegimeRouter, RegimeRoute
from e1r_engine.state import (
    AccountState,
    DailyEngineResult,
    DecisionTrace,
    OrderIntent,
)
from e1r_engine.uptrend_consumer import (
    UptrendConsumerInputs,
    UptrendConsumerResult,
    UptrendDecisionConsumer,
)


@dataclass(frozen=True)
class E1RCoreEngineConfig:
    max_positions: int = 3
    shell_mode: bool = True


class E1RCoreEngine:
    """
    E1R Core Engine shell.

    Current ENGINE-F scope:
    - Accept MarketSnapshot + AccountState.
    - Route regime through RegimeRouter shell.
    - Mark current positions to market.
    - Return DailyEngineResult with explicit NOOP/HOLD trace.

    Must not yet:
    - Extract UPTREND logic.
    - Implement SIDEWAYS logic.
    - Generate BUY/SELL decisions.
    - Apply sizing / market gate / candidate ranking.
    - Call run_stateful_simulation.
    - Run 5Y backtest.
    """

    def __init__(self, config: E1RCoreEngineConfig | None = None, router: RegimeRouter | None = None) -> None:
        self.config = config or E1RCoreEngineConfig()
        self.router = router or RegimeRouter()

    def step(
        self,
        snapshot: MarketSnapshot,
        account: AccountState,
        *,
        uptrend_inputs: UptrendConsumerInputs | None = None,
    ) -> DailyEngineResult:
        route = self._route(snapshot)
        account_before = account

        if (
            uptrend_inputs is not None
            and route.branch != "UPTREND"
        ):
            raise ValueError(
                "uptrend_inputs supplied for non-UPTREND route: "
                + route.branch
            )

        if (
            uptrend_inputs is not None
            and uptrend_inputs.date != snapshot.date
        ):
            raise ValueError(
                "uptrend_inputs date does not match snapshot date"
            )

        prices = {
            symbol: bar.close
            for symbol, bar in snapshot.prices_by_symbol.items()
            if bar is not None
        }

        account_after = account.mark_to_market(prices=prices, date=snapshot.date)

        if uptrend_inputs is not None:
            return self._step_uptrend(
                snapshot=snapshot,
                route=route,
                account_before=account_before,
                account_after=account_after,
                uptrend_inputs=uptrend_inputs,
            )

        order_intents = self._noop_or_hold_orders(snapshot=snapshot, route=route, account_after=account_after)

        trace = DecisionTrace(
            date=snapshot.date,
            branch=route.branch,
            market_regime=route.spx_regime,
            regime_subclass=route.subclass,
            inputs={
                "shell_mode": True,
                "no_strategy_logic": True,
                "no_candidate_ranking": True,
                "no_sizing": True,
                "no_market_gate": True,
                "route_reason": route.reason,
            },
            candidate_count=0,
            selected_symbols=[],
            order_intents=order_intents,
            reasons=[
                "engine_f_core_shell_only",
                route.reason,
                "mark_to_market_only",
            ],
            metadata={
                "route": route.__dict__,
                "max_positions": self.config.max_positions,
            },
        )

        return DailyEngineResult(
            date=snapshot.date,
            account_before=account_before,
            account_after=account_after,
            decision_trace=trace,
            order_intents=order_intents,
            fills=[],
            metadata={
                "engine": "E1RCoreEngine",
                "stage": "ENGINE-F",
                "shell_mode": True,
            },
        )

    def _step_uptrend(
        self,
        *,
        snapshot: MarketSnapshot,
        route: RegimeRoute,
        account_before: AccountState,
        account_after: AccountState,
        uptrend_inputs: UptrendConsumerInputs,
    ) -> DailyEngineResult:
        uptrend_result: UptrendConsumerResult = (
            UptrendDecisionConsumer.consume(
                inputs=uptrend_inputs,
                account_state=account_after,
                max_positions=self.config.max_positions,
            )
        )

        base_orders = self._noop_or_hold_orders(
            snapshot=snapshot,
            route=route,
            account_after=account_after,
        )

        if uptrend_result.order_intents:
            order_intents = [
                order
                for order in base_orders
                if order.intent_type != "NOOP"
            ]
            order_intents.extend(
                uptrend_result.order_intents
            )
        else:
            order_intents = base_orders

        trace = DecisionTrace(
            date=snapshot.date,
            branch=route.branch,
            market_regime=route.spx_regime,
            regime_subclass=route.subclass,
            inputs={
                "shell_mode": False,
                "no_strategy_logic": False,
                "no_candidate_ranking": False,
                "no_sizing": True,
                "no_market_gate_recomputation": True,
                "route_reason": route.reason,
                "uptrend_consumer_active": True,
            },
            candidate_count=(
                uptrend_result.decision.candidate_count
            ),
            selected_symbols=list(
                uptrend_result.metadata["selected_symbols"]
            ),
            order_intents=order_intents,
            reasons=[
                "uptrend_core_consumer",
                route.reason,
                "mark_to_market_only",
                "standard_order_intent_only",
                "no_order_execution",
            ],
            metadata={
                "route": route.__dict__,
                "max_positions": self.config.max_positions,
                "uptrend_consumer": uptrend_result.metadata,
            },
        )

        return DailyEngineResult(
            date=snapshot.date,
            account_before=account_before,
            account_after=account_after,
            decision_trace=trace,
            order_intents=order_intents,
            fills=[],
            metadata={
                "engine": "E1RCoreEngine",
                "stage": "K2-R21",
                "shell_mode": False,
                "uptrend_consumer_active": True,
                "legacy_order_payload_constructed": False,
                "order_execution_performed": False,
                "account_trade_mutation_performed": False,
            },
        )

    def _route(self, snapshot: MarketSnapshot) -> RegimeRoute:
        if snapshot.regime is None:
            return self.router.route(
                date=snapshot.date,
                spx_regime=None,
                subclass=None,
            )

        return self.router.route(
            date=snapshot.date,
            spx_regime=snapshot.regime.spx_regime,
            subclass=snapshot.regime.subclass,
        )

    def _noop_or_hold_orders(
        self,
        snapshot: MarketSnapshot,
        route: RegimeRoute,
        account_after: AccountState,
    ) -> list[OrderIntent]:
        if not account_after.positions:
            return [
                OrderIntent(
                    date=snapshot.date,
                    symbol="",
                    intent_type="NOOP",
                    side=None,
                    target_quantity=None,
                    quantity_delta=None,
                    reason="engine_f_shell_no_positions_noop",
                    branch=route.branch,
                    metadata={
                        "shell_mode": True,
                        "no_strategy_decision": True,
                    },
                )
            ]

        orders: list[OrderIntent] = []
        for symbol, position in sorted(account_after.positions.items()):
            orders.append(
                OrderIntent(
                    date=snapshot.date,
                    symbol=symbol,
                    intent_type="HOLD",
                    side=None,
                    target_quantity=position.quantity,
                    quantity_delta=0.0,
                    reason="engine_f_shell_existing_position_hold",
                    branch=route.branch,
                    metadata={
                        "shell_mode": True,
                        "no_strategy_decision": True,
                    },
                )
            )
        return orders
