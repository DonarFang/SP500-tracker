"""Live composition around the existing shared FD-M3180125 Engine path."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any, Optional, Protocol, Tuple

from e1r_engine.contracts import HistoricalDataBundle
from e1r_engine.core import E1RCoreEngine
from e1r_engine.live_account import LiveAccountState
from e1r_engine.live_account_adapter import LiveAccountAdapter
from e1r_engine.live_data import LiveMarketData
from e1r_engine.live_recommendation import (
    LiveEngineDecision,
    PositionRecommendation,
    ReferenceCandidate,
)
from e1r_engine.adapters.live_data import LiveDataAdapter


class LiveEngineAdapterError(ValueError):
    pass


@dataclass(frozen=True)
class LivePreparedEngineInputs:
    bundle: HistoricalDataBundle
    stock_symbols: Tuple[str, ...]
    uptrend_inputs: Optional[object] = None
    uptrend_pipeline_inputs: Optional[object] = None
    reference_symbols: Tuple[str, ...] = ()


class LiveFormalInputProvider(Protocol):
    """Provide standard Engine contracts without reimplementing strategy."""

    def prepare(
        self,
        *,
        market_date: str,
        market_data: LiveMarketData,
        live_account: LiveAccountState,
        data_adapter: LiveDataAdapter,
    ) -> LivePreparedEngineInputs:
        ...


def _value(obj: object, name: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


class LiveEngineAdapter:
    """Implement LiveEnginePort through `E1RCoreEngine.step` only."""

    def __init__(
        self,
        *,
        data_adapter: LiveDataAdapter,
        input_provider: LiveFormalInputProvider,
        engine: Optional[E1RCoreEngine] = None,
        account_adapter: Optional[LiveAccountAdapter] = None,
    ) -> None:
        self.data_adapter = data_adapter
        self.input_provider = input_provider
        self.engine = engine or E1RCoreEngine()
        self.account_adapter = account_adapter or LiveAccountAdapter()

    def decide(
        self,
        *,
        market_date: date,
        market_data: LiveMarketData,
        account: LiveAccountState,
    ) -> LiveEngineDecision:
        date_text = market_date.isoformat()
        if market_data.market_date != market_date:
            raise LiveEngineAdapterError("market date mismatch")

        prepared = self.input_provider.prepare(
            market_date=date_text,
            market_data=market_data,
            live_account=account,
            data_adapter=self.data_adapter,
        )

        snapshot = self.data_adapter.build_snapshot(
            bundle=prepared.bundle,
            market_date=date_text,
            universe=prepared.stock_symbols,
        )
        engine_account = self.account_adapter.to_engine_account(
            live_account=account,
            market_date=date_text,
        )

        result = self.engine.step(
            snapshot=snapshot,
            account=engine_account,
            uptrend_inputs=prepared.uptrend_inputs,
            uptrend_pipeline_inputs=prepared.uptrend_pipeline_inputs,
        )

        validation = result.validate(max_positions=3)
        if not isinstance(validation, dict):
            raise LiveEngineAdapterError(
                "DailyEngineResult.validate must return a report dict"
            )
        if not validation.get("ok", False):
            errors = validation.get("errors", [])
            raise LiveEngineAdapterError(
                "invalid DailyEngineResult: "
                + "; ".join(str(item) for item in errors)
            )

        trace = result.decision_trace
        route = _value(trace, "route", None)
        inputs = _value(trace, "inputs", {}) or {}
        outputs = _value(trace, "outputs", {}) or {}
        metadata = _value(result, "metadata", {}) or {}

        regime_record = snapshot.regime
        regime = (
            regime_record.spx_regime
            if regime_record is not None
            else "UNCLASSIFIED"
        )
        subclass = (
            regime_record.subclass
            if regime_record is not None
            else None
        )

        branch = (
            _value(route, "branch", None)
            or _value(trace, "branch", None)
            or regime
        )

        market_state = (
            _value(inputs, "market_state", None)
            or _value(outputs, "market_state", None)
            or _value(trace, "market_state", None)
            or "UNKNOWN"
        )
        gate_state = (
            _value(inputs, "gate_state", None)
            or _value(inputs, "market_gate", None)
            or _value(outputs, "gate_state", None)
            or _value(trace, "gate_state", None)
            or "UNKNOWN"
        )
        entry_capacity = (
            _value(inputs, "entry_capacity", None)
            or _value(outputs, "entry_capacity", None)
            or 0
        )

        ranked = list(prepared.reference_symbols)
        references = tuple(
            ReferenceCandidate(rank=index + 1, symbol=symbol)
            for index, symbol in enumerate(ranked[:3])
        )

        recommendations = []
        for intent in result.order_intents:
            intent_type = str(
                _value(intent, "intent_type", "")
            ).upper()
            if intent_type in {"NOOP", "NO_ACTION"}:
                continue
            if intent_type not in {
                "BUY", "ADD", "HOLD", "REDUCE", "EXIT"
            }:
                raise LiveEngineAdapterError(
                    f"unsupported Engine intent: {intent_type}"
                )
            target = _value(intent, "target_quantity", None)
            recommendations.append(
                PositionRecommendation(
                    symbol=str(_value(intent, "symbol", "")),
                    action=intent_type,
                    reason=str(_value(intent, "reason", "")),
                    target_shares=(
                        Decimal(str(target))
                        if target is not None
                        else None
                    ),
                )
            )

        return LiveEngineDecision(
            market_date=market_date,
            regime=str(regime),
            regime_subclass=(
                str(subclass) if subclass is not None else None
            ),
            market_state=str(market_state),
            market_gate=str(gate_state),
            entry_capacity=int(entry_capacity),
            strategy_branch=str(branch),
            reference_candidates=references,
            position_recommendations=tuple(recommendations),
            evidence={
                "engine_result_metadata": metadata,
                "decision_trace": trace,
                "adapter": "LiveEngineAdapter",
                "engine_entry": "E1RCoreEngine.step",
                "strategy_logic_reimplemented": False,
            },
            engine_version=str(
                metadata.get("stage", "UNKNOWN")
                if isinstance(metadata, dict)
                else "UNKNOWN"
            ),
        )
