from __future__ import annotations

from collections.abc import Mapping

from e1r_engine.market_gate import (
    MarketGateConfig,
    MarketGateDecision,
    MarketGateEvaluator,
    MarketGateInputs,
)
from e1r_engine.market_state import (
    MarketStateDecision,
    MarketStateEvaluator,
    MarketStateInputs,
)

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
from e1r_engine.uptrend_pipeline import (
    UptrendPipelineInputs,
    UptrendSignalConsumerPipeline,
    UptrendSignalConsumerPipelineResult,
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

    def __init__(
        self,
        config: E1RCoreEngineConfig | None = None,
        router: RegimeRouter | None = None,
        market_state_evaluator: type[MarketStateEvaluator] | None = None,
        market_gate_evaluator: type[MarketGateEvaluator] | None = None,
    ) -> None:
        self.config = config or E1RCoreEngineConfig()
        self.router = router or RegimeRouter()
        self.market_state_evaluator = market_state_evaluator or MarketStateEvaluator
        self.market_gate_evaluator = market_gate_evaluator or MarketGateEvaluator

    @staticmethod
    def _close_values_through_date(*, date: str, series: Mapping[str, object], symbol: str) -> list[float]:
        values = []
        for row_date in sorted(series):
            if row_date > date:
                break
            close = getattr(series[row_date], "close", None)
            if close is not None:
                values.append(float(close))
        if len(values) < 50:
            raise ValueError(f"{symbol}: Market State requires at least 50 closes through {date}; got {len(values)}")
        return values

    def build_market_state_inputs(self, *, date: str, index_series: Mapping[str, Mapping[str, object]], max_positions: int | None = None) -> MarketStateInputs:
        missing = [symbol for symbol in ("SPX", "NDX", "SOX") if symbol not in index_series]
        if missing:
            raise ValueError("Market State missing required index series: " + ",".join(missing))
        values = {
            symbol: self._close_values_through_date(date=date, series=index_series[symbol], symbol=symbol)
            for symbol in ("SPX", "NDX", "SOX")
        }
        spx, ndx, sox = values["SPX"], values["NDX"], values["SOX"]
        spx_ma50 = sum(spx[-50:]) / 50.0
        spx_ma50_10d_ago = sum(spx[-60:-10]) / 50.0 if len(spx) >= 60 else spx_ma50
        return MarketStateInputs(
            date=date,
            spx_close=spx[-1],
            spx_ma50=spx_ma50,
            spx_ma50_10d_ago=spx_ma50_10d_ago,
            spx_day_return=(spx[-1] / spx[-2] - 1.0 if len(spx) >= 2 and spx[-2] > 0 else 0.0),
            ndx_close=ndx[-1],
            ndx_ma50=sum(ndx[-50:]) / 50.0,
            sox_close=sox[-1],
            sox_ma50=sum(sox[-50:]) / 50.0,
            max_positions=self.config.max_positions if max_positions is None else int(max_positions),
        )

    def evaluate_market_state_and_gate(self, *, inputs: MarketStateInputs, existing_positions_count: int) -> tuple[MarketStateDecision, MarketGateDecision]:
        state = self.market_state_evaluator.evaluate(__import__("e1r_engine.market_state", fromlist=["MarketStateConfig"]).MarketStateConfig(), inputs)
        gate = self.market_gate_evaluator.evaluate(
            MarketGateConfig(),
            MarketGateInputs(
                date=state.date,
                spx_close=state.spx_close,
                spx_ma50=state.spx_ma50,
                spx_day_return=state.spx_day_return,
                market_state=state.market_state,
                entry_capacity=state.entry_capacity,
                existing_positions_count=int(existing_positions_count),
            ),
        )
        return state, gate

    def evaluate_market_state_and_gate_from_series(self, *, date: str, index_series: Mapping[str, Mapping[str, object]], existing_positions_count: int, max_positions: int | None = None) -> tuple[MarketStateDecision, MarketGateDecision]:
        return self.evaluate_market_state_and_gate(
            inputs=self.build_market_state_inputs(date=date, index_series=index_series, max_positions=max_positions),
            existing_positions_count=existing_positions_count,
        )

    def step(
        self,
        snapshot: MarketSnapshot,
        account: AccountState,
        *,
        uptrend_inputs: UptrendConsumerInputs | None = None,
        uptrend_pipeline_inputs: UptrendPipelineInputs | None = None,
    ) -> DailyEngineResult:
        route = self._route(snapshot)
        account_before = account

        if (
            uptrend_inputs is not None
            and uptrend_pipeline_inputs is not None
        ):
            raise ValueError(
                "uptrend_inputs and uptrend_pipeline_inputs "
                "are mutually exclusive"
            )

        if (
            uptrend_inputs is not None
            and route.branch != "UPTREND"
        ):
            raise ValueError(
                "uptrend_inputs supplied for non-UPTREND route: "
                + route.branch
            )

        if (
            uptrend_pipeline_inputs is not None
            and route.branch != "UPTREND"
        ):
            raise ValueError(
                "uptrend_pipeline_inputs supplied for "
                "non-UPTREND route: "
                + route.branch
            )

        if (
            uptrend_inputs is not None
            and uptrend_inputs.date != snapshot.date
        ):
            raise ValueError(
                "uptrend_inputs date does not match snapshot date"
            )

        if uptrend_pipeline_inputs is not None:
            pipeline_errors = (
                uptrend_pipeline_inputs.validate()
            )

            if pipeline_errors:
                raise ValueError(
                    "invalid uptrend_pipeline_inputs: "
                    + "; ".join(pipeline_errors)
                )

            if (
                uptrend_pipeline_inputs.date
                != snapshot.date
            ):
                raise ValueError(
                    "uptrend_pipeline_inputs date does not "
                    "match snapshot date"
                )

        prices = {
            symbol: bar.close
            for symbol, bar in snapshot.prices_by_symbol.items()
            if bar is not None
        }

        account_after = account.mark_to_market(prices=prices, date=snapshot.date)

        if uptrend_pipeline_inputs is not None:
            return self._step_uptrend_pipeline(
                snapshot=snapshot,
                route=route,
                account_before=account_before,
                account_after=account_after,
                pipeline_inputs=uptrend_pipeline_inputs,
            )

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
                "uptrend_decision": {
                    "pre_rank_candidate_rows": (
                        uptrend_result.decision.trace_rows(
                            uptrend_result.decision.pre_rank_candidates
                        )
                    ),
                    "ranked_candidate_rows": (
                        uptrend_result.decision.trace_rows(
                            uptrend_result.decision.ranked_candidates
                        )
                    ),
                    "selected_symbol": (
                        uptrend_result.decision.selected_buy["sym"]
                        if uptrend_result.decision.selected_buy
                        is not None
                        else None
                    ),
                    "selected_entry_type": (
                        uptrend_result.decision.selected_buy[
                            "entry_type"
                        ]
                        if uptrend_result.decision.selected_buy
                        is not None
                        else None
                    ),
                    "selected_target_size_units": (
                        uptrend_result.decision.selected_buy[
                            "target_size_units"
                        ]
                        if uptrend_result.decision.selected_buy
                        is not None
                        else None
                    ),
                    "no_capacity_count": (
                        uptrend_result.decision.no_capacity_count
                    ),
                },
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

    def _step_uptrend_pipeline(
        self,
        *,
        snapshot: MarketSnapshot,
        route: RegimeRoute,
        account_before: AccountState,
        account_after: AccountState,
        pipeline_inputs: UptrendPipelineInputs,
    ) -> DailyEngineResult:
        pipeline_result: (
            UptrendSignalConsumerPipelineResult
        ) = UptrendSignalConsumerPipeline.run(
            date=pipeline_inputs.date,
            symbols=pipeline_inputs.symbols,
            prices_by_symbol=(
                pipeline_inputs.prices_by_symbol
            ),
            market_gate_decision=(
                pipeline_inputs.market_gate_decision
            ),
            account_state=account_after,
            max_positions=self.config.max_positions,
            market_score_default=(
                pipeline_inputs.market_score_default
            ),
            ls60_exit_mode=(
                pipeline_inputs.ls60_exit_mode
            ),
            metadata={
                "engine_entry": "E1RCoreEngine.step",
                **dict(pipeline_inputs.metadata),
            },
        )

        uptrend_result = (
            pipeline_result.consumer_result
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
                "uptrend_pipeline_active": True,
                "uptrend_consumer_active": True,
            },
            candidate_count=(
                uptrend_result.decision.candidate_count
            ),
            selected_symbols=list(
                uptrend_result.metadata[
                    "selected_symbols"
                ]
            ),
            order_intents=order_intents,
            reasons=[
                "uptrend_signal_adapter_pipeline",
                "uptrend_core_consumer",
                route.reason,
                "mark_to_market_only",
                "standard_order_intent_only",
                "no_order_execution",
            ],
            metadata={
                "route": route.__dict__,
                "max_positions": self.config.max_positions,
                "uptrend_pipeline": (
                    pipeline_result.metadata
                ),
                "uptrend_adapter": (
                    pipeline_result
                    .adapter_result
                    .metadata
                ),
                "uptrend_consumer": (
                    uptrend_result.metadata
                ),
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
                "stage": "K2-R24",
                "shell_mode": False,
                "uptrend_pipeline_active": True,
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
