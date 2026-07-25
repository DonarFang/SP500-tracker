"""Live entry adapter into the shared FD-M3180125 Engine.

Market data enters only through LiveDataAdapter. The existing Engine-owned
CanonicalRegimeGenerator creates Regime. E1RCoreEngine.step remains unchanged
and owns Market State, Market Gate, Router, strategy branch, ranking, sizing,
and OrderIntent behavior.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any, Optional, Sequence

from e1r_engine.adapters.live_data import (
    LiveDataAdapter,
)
from e1r_engine.canonical_regime import (
    CanonicalRegimeGenerator,
)
from e1r_engine.contracts import (
    AssetSeries,
    HistoricalDataBundle,
    MarketSnapshot,
)
from e1r_engine.core import E1RCoreEngine
from e1r_engine.live_account import (
    LiveAccountState,
)
from e1r_engine.live_account_adapter import (
    LiveAccountAdapter,
)
from e1r_engine.live_data import LiveMarketData
from e1r_engine.live_recommendation import (
    LiveEngineDecision,
    PositionRecommendation,
    ReferenceCandidate,
)


class LiveEngineAdapterError(ValueError):
    pass


def _value(
    obj: object,
    name: str,
    default: Any = None,
) -> Any:
    if isinstance(obj, dict):
        return obj.get(name, default)

    return getattr(obj, name, default)


def _bar_for_date(
    series: AssetSeries,
    market_date: str,
):
    try:
        index = series.dates.index(
            market_date
        )
    except ValueError as exc:
        raise LiveEngineAdapterError(
            f"{series.symbol}: missing bar for "
            f"{market_date}"
        ) from exc

    return series.bars[index]


def _snapshot_from_bundle(
    *,
    bundle: HistoricalDataBundle,
    market_date: str,
    universe: Sequence[str],
    regime,
) -> MarketSnapshot:
    prices_by_symbol = {}

    for symbol in universe:
        dates = bundle.dates_map.get(
            symbol,
            [],
        )

        try:
            index = dates.index(
                market_date
            )
        except ValueError as exc:
            raise LiveEngineAdapterError(
                f"{symbol}: missing Live stock bar "
                f"for {market_date}"
            ) from exc

        prices_by_symbol[symbol] = (
            bundle.ohlc_map[symbol][index]
        )

    indices = {
        symbol: _bar_for_date(
            series,
            market_date,
        )
        for symbol, series in bundle.indices.items()
    }

    if bundle.vix is not None:
        indices["VIX"] = _bar_for_date(
            bundle.vix,
            market_date,
        )

    snapshot = MarketSnapshot(
        date=market_date,
        universe=list(universe),
        prices_by_symbol=prices_by_symbol,
        indices=indices,
        regime=regime,
        metadata={
            "mode": "LIVE",
            "market_data_source": (
                "LiveDataAdapter"
            ),
            "regime_source": (
                "engine://canonical_regime"
            ),
            "external_regime_injected": False,
            "provider_abstraction_used": False,
        },
    )

    return snapshot


def _reference_candidates(
    result,
) -> tuple[ReferenceCandidate, ...]:
    selected = list(
        _value(
            result.decision_trace,
            "selected_symbols",
            [],
        )
        or []
    )

    normalized = []

    for item in selected:
        symbol = str(item).strip().upper()

        if symbol and symbol not in normalized:
            normalized.append(symbol)

    return tuple(
        ReferenceCandidate(
            rank=index + 1,
            symbol=symbol,
        )
        for index, symbol in enumerate(
            normalized[:3]
        )
    )


class LiveEngineAdapter:
    """Load Live market data, enter the existing Engine, map its output."""

    def __init__(
        self,
        *,
        data_adapter: LiveDataAdapter,
        stock_symbols: Sequence[str],
        min_bars: int = 120,
        engine: Optional[E1RCoreEngine] = None,
        account_adapter: Optional[
            LiveAccountAdapter
        ] = None,
    ) -> None:
        normalized_symbols = tuple(
            str(symbol).strip().upper()
            for symbol in stock_symbols
        )

        if not normalized_symbols:
            raise LiveEngineAdapterError(
                "stock_symbols must not be empty"
            )

        if len(set(normalized_symbols)) != len(
            normalized_symbols
        ):
            raise LiveEngineAdapterError(
                "stock_symbols must be unique"
            )

        if min_bars <= 0:
            raise LiveEngineAdapterError(
                "min_bars must be positive"
            )

        self.data_adapter = data_adapter
        self.stock_symbols = normalized_symbols
        self.min_bars = int(min_bars)
        self.engine = engine or E1RCoreEngine()
        self.account_adapter = (
            account_adapter
            or LiveAccountAdapter()
        )

    def decide(
        self,
        *,
        market_date: date,
        market_data: LiveMarketData,
        account: LiveAccountState,
    ) -> LiveEngineDecision:
        date_text = market_date.isoformat()

        if market_data.market_date != market_date:
            raise LiveEngineAdapterError(
                "market date mismatch"
            )

        bundle = self.data_adapter.load_bundle(
            stock_symbols=self.stock_symbols,
            min_bars=self.min_bars,
        )

        canonical_timeline = (
            CanonicalRegimeGenerator().generate(
                bundle.indices["SPX"]
            )
        )
        regime_record = (
            canonical_timeline.record_for_date(
                date_text
            )
        )

        snapshot = _snapshot_from_bundle(
            bundle=bundle,
            market_date=date_text,
            universe=self.stock_symbols,
            regime=regime_record,
        )

        engine_account = (
            self.account_adapter.to_engine_account(
                live_account=account,
                market_date=date_text,
            )
        )

        result = self.engine.step(
            snapshot=snapshot,
            account=engine_account,
        )

        validation = result.validate(
            max_positions=3
        )

        if not isinstance(validation, dict):
            raise LiveEngineAdapterError(
                "DailyEngineResult.validate must "
                "return a report dict"
            )

        if not validation.get("ok", False):
            raise LiveEngineAdapterError(
                "invalid DailyEngineResult: "
                + "; ".join(
                    str(item)
                    for item in validation.get(
                        "errors",
                        [],
                    )
                )
            )

        trace = result.decision_trace
        trace_inputs = _value(
            trace,
            "inputs",
            {},
        ) or {}
        trace_metadata = _value(
            trace,
            "metadata",
            {},
        ) or {}
        result_metadata = _value(
            result,
            "metadata",
            {},
        ) or {}

        market_state = (
            trace_inputs.get("market_state")
            or trace_metadata.get("market_state")
            or "UNKNOWN"
        )
        market_gate = (
            trace_inputs.get("gate_state")
            or trace_inputs.get("market_gate")
            or trace_metadata.get("gate_state")
            or "UNKNOWN"
        )
        entry_capacity = (
            trace_inputs.get("entry_capacity")
            or trace_metadata.get(
                "entry_capacity"
            )
            or 0
        )

        recommendations = []

        for intent in result.order_intents:
            action = str(
                _value(
                    intent,
                    "intent_type",
                    "",
                )
            ).upper()

            if action in {
                "NOOP",
                "NO_ACTION",
            }:
                continue

            if action not in {
                "BUY",
                "ADD",
                "HOLD",
                "REDUCE",
                "EXIT",
            }:
                raise LiveEngineAdapterError(
                    "unsupported Engine intent: "
                    + action
                )

            target = _value(
                intent,
                "target_quantity",
                None,
            )

            recommendations.append(
                PositionRecommendation(
                    symbol=str(
                        _value(
                            intent,
                            "symbol",
                            "",
                        )
                    ),
                    action=action,
                    reason=str(
                        _value(
                            intent,
                            "reason",
                            "",
                        )
                    ),
                    target_shares=(
                        Decimal(str(target))
                        if target is not None
                        else None
                    ),
                )
            )

        return LiveEngineDecision(
            market_date=market_date,
            regime=str(
                _value(
                    trace,
                    "market_regime",
                    regime_record.spx_regime,
                )
            ),
            regime_subclass=(
                None
                if _value(
                    trace,
                    "regime_subclass",
                    regime_record.subclass,
                )
                is None
                else str(
                    _value(
                        trace,
                        "regime_subclass",
                        regime_record.subclass,
                    )
                )
            ),
            market_state=str(
                market_state
            ),
            market_gate=str(
                market_gate
            ),
            entry_capacity=int(
                entry_capacity
            ),
            strategy_branch=str(
                _value(
                    trace,
                    "branch",
                    regime_record.spx_regime,
                )
            ),
            reference_candidates=(
                _reference_candidates(result)
            ),
            position_recommendations=tuple(
                recommendations
            ),
            evidence={
                "engine_result_metadata": (
                    result_metadata
                ),
                "decision_trace": trace,
                "adapter": "LiveEngineAdapter",
                "engine_entry": (
                    "E1RCoreEngine.step"
                ),
                "regime_source": (
                    "engine://canonical_regime"
                ),
                "external_regime_injected": False,
                "provider_abstraction_used": False,
                "strategy_logic_reimplemented": False,
            },
            engine_version=str(
                result_metadata.get(
                    "stage",
                    "UNKNOWN",
                )
            ),
        )
