from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from e1r_engine.market_gate import MarketGateDecision
from e1r_engine.state import AccountState, OrderIntent
from e1r_engine.uptrend_core import UptrendBuyDecision, UptrendCore


@dataclass(frozen=True)
class UptrendConsumerInputs:
    date: str
    day_signals: dict[str, dict[str, Any]]
    leader_rank_all: dict[str, int]
    market_gate_decision: MarketGateDecision
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        errors: list[str] = []

        if not self.date:
            errors.append("missing_date")
        if self.market_gate_decision.date != self.date:
            errors.append("market_gate_decision_date_mismatch")
        if not isinstance(self.day_signals, dict):
            errors.append("day_signals_must_be_dict")
        if not isinstance(self.leader_rank_all, dict):
            errors.append("leader_rank_all_must_be_dict")

        return errors


@dataclass(frozen=True)
class UptrendConsumerResult:
    date: str
    decision: UptrendBuyDecision
    order_intents: tuple[OrderIntent, ...]
    account_state_reference: AccountState
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self, *, max_positions: int) -> list[str]:
        errors: list[str] = []

        if not self.date:
            errors.append("missing_date")
        if self.account_state_reference.date != self.date:
            errors.append("account_state_date_mismatch")

        account_validation = self.account_state_reference.validate(
            max_positions=max_positions
        )
        if not account_validation["ok"]:
            errors.extend(
                "account_state:" + error
                for error in account_validation["errors"]
            )

        for order_intent in self.order_intents:
            errors.extend(
                "order_intent:" + error
                for error in order_intent.validate()
            )

        return errors


class UptrendDecisionConsumer:
    @staticmethod
    def consume(
        *,
        inputs: UptrendConsumerInputs,
        account_state: AccountState,
        max_positions: int,
    ) -> UptrendConsumerResult:
        input_errors = inputs.validate()
        if input_errors:
            raise ValueError(
                "invalid uptrend consumer inputs: "
                + "; ".join(input_errors)
            )

        if account_state.date != inputs.date:
            raise ValueError(
                "account_state date does not match "
                "uptrend consumer input date"
            )
        if max_positions < 0:
            raise ValueError("max_positions must be non-negative")

        decision = UptrendCore.decide_uptrend_buy(
            day_signals=inputs.day_signals,
            holdings_symbols=set(account_state.positions.keys()),
            leader_rank_all=inputs.leader_rank_all,
            market_entry_allowed=(
                inputs.market_gate_decision.market_entry_allowed
            ),
            entry_capacity=inputs.market_gate_decision.entry_capacity,
            max_positions=max_positions,
        )

        order_intents: list[OrderIntent] = []

        if decision.selected_buy is not None:
            selected_buy = decision.selected_buy
            symbol = selected_buy["sym"]
            order_intents.append(
                OrderIntent(
                    date=inputs.date,
                    symbol=symbol,
                    intent_type="BUY",
                    side="BUY",
                    target_quantity=None,
                    quantity_delta=None,
                    reason=selected_buy["entry_type"],
                    branch="UPTREND",
                    metadata={
                        "source": "UptrendDecisionConsumer",
                        "strategy_logic_source": "UptrendCore",
                        "e1r_entry_type": selected_buy["entry_type"],
                        "target_size_units": selected_buy[
                            "target_size_units"
                        ],
                        "leader_rank_all": (
                            inputs.leader_rank_all.get(symbol)
                        ),
                        "market_gate_state": (
                            inputs.market_gate_decision.gate_state
                        ),
                        "market_entry_allowed": (
                            inputs
                            .market_gate_decision
                            .market_entry_allowed
                        ),
                        "entry_capacity": (
                            inputs.market_gate_decision.entry_capacity
                        ),
                        "order_executed": False,
                        "account_mutated": False,
                    },
                )
            )

        result = UptrendConsumerResult(
            date=inputs.date,
            decision=decision,
            order_intents=tuple(order_intents),
            account_state_reference=account_state,
            metadata={
                "consumer": "UptrendDecisionConsumer",
                "candidate_count": decision.candidate_count,
                "ranked_candidate_count": len(
                    decision.ranked_candidates
                ),
                "selected_symbols": (
                    [decision.selected_buy["sym"]]
                    if decision.selected_buy is not None
                    else []
                ),
                "no_capacity_count": decision.no_capacity_count,
                "market_gate_state": (
                    inputs.market_gate_decision.gate_state
                ),
                "market_entry_allowed": (
                    inputs
                    .market_gate_decision
                    .market_entry_allowed
                ),
                "entry_capacity": (
                    inputs.market_gate_decision.entry_capacity
                ),
                "legacy_order_payload_constructed": False,
                "market_gate_recomputed": False,
                "order_execution_performed": False,
                "account_mutated": False,
                "legacy_backtest_called": False,
            },
        )

        result_errors = result.validate(max_positions=max_positions)
        if result_errors:
            raise ValueError(
                "invalid uptrend consumer result: "
                + "; ".join(result_errors)
            )

        return result


__all__ = [
    "UptrendConsumerInputs",
    "UptrendConsumerResult",
    "UptrendDecisionConsumer",
]
