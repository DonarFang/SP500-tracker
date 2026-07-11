from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from e1r_engine.market_gate import MarketGateDecision
from e1r_engine.state import AccountState
from e1r_engine.uptrend_consumer import (
    UptrendConsumerResult,
    UptrendDecisionConsumer,
)
from e1r_engine.uptrend_signal_adapter import (
    UptrendSignalAdapter,
    UptrendSignalAdapterResult,
)


@dataclass(frozen=True)
class UptrendSignalConsumerPipelineResult:
    date: str
    adapter_result: UptrendSignalAdapterResult
    consumer_result: UptrendConsumerResult
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        errors: list[str] = []

        if not self.date:
            errors.append("missing_date")

        if self.adapter_result.date != self.date:
            errors.append("adapter_result_date_mismatch")

        if self.consumer_result.date != self.date:
            errors.append("consumer_result_date_mismatch")

        if (
            self.consumer_result.decision.candidate_count
            != self.metadata.get("candidate_count")
        ):
            errors.append("candidate_count_metadata_mismatch")

        return errors


class UptrendSignalConsumerPipeline:
    @staticmethod
    def run(
        *,
        date: str,
        symbols: Sequence[str],
        prices_by_symbol: Mapping[str, Sequence[float]],
        market_gate_decision: MarketGateDecision,
        account_state: AccountState,
        max_positions: int,
        market_score_default: float = 60.0,
        ls60_exit_mode: str = "reduce",
        metadata: dict[str, Any] | None = None,
    ) -> UptrendSignalConsumerPipelineResult:
        if not date:
            raise ValueError("date must be non-empty")

        if market_gate_decision.date != date:
            raise ValueError(
                "market gate date does not match pipeline date"
            )

        if account_state.date != date:
            raise ValueError(
                "account state date does not match pipeline date"
            )

        if max_positions < 0:
            raise ValueError(
                "max_positions must be non-negative"
            )

        adapter_result = UptrendSignalAdapter.build(
            date=date,
            symbols=symbols,
            prices_by_symbol=prices_by_symbol,
            market_score_default=market_score_default,
            ls60_exit_mode=ls60_exit_mode,
        )

        consumer_inputs = adapter_result.to_consumer_inputs(
            market_gate_decision=market_gate_decision,
            metadata={
                "source": "UptrendSignalConsumerPipeline",
                **dict(metadata or {}),
            },
        )

        consumer_result = UptrendDecisionConsumer.consume(
            inputs=consumer_inputs,
            account_state=account_state,
            max_positions=max_positions,
        )

        result = UptrendSignalConsumerPipelineResult(
            date=date,
            adapter_result=adapter_result,
            consumer_result=consumer_result,
            metadata={
                "pipeline": "UptrendSignalConsumerPipeline",
                "adapter": "UptrendSignalAdapter",
                "consumer": "UptrendDecisionConsumer",
                "strategy_core": "UptrendCore",
                "signal_count": len(
                    adapter_result.day_signals
                ),
                "candidate_count": (
                    consumer_result.decision.candidate_count
                ),
                "selected_symbols": list(
                    consumer_result.metadata[
                        "selected_symbols"
                    ]
                ),
                "order_intent_count": len(
                    consumer_result.order_intents
                ),
                "market_gate_recomputed": False,
                "account_mutated": False,
                "order_execution_performed": False,
                "legacy_backtest_called": False,
                "legacy_order_payload_constructed": False,
                **dict(metadata or {}),
            },
        )

        errors = result.validate()

        if errors:
            raise ValueError(
                "invalid uptrend signal-consumer pipeline result: "
                + "; ".join(errors)
            )

        return result


__all__ = [
    "UptrendSignalConsumerPipeline",
    "UptrendSignalConsumerPipelineResult",
]
