"""Live-only contracts around the shared FD-M3180125 Engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Mapping, Protocol, Sequence, Tuple

from .live_account import LiveAccountState
from .live_data import LiveMarketData


class LiveRecommendationError(ValueError):
    pass


@dataclass(frozen=True)
class ReferenceCandidate:
    rank: int
    symbol: str

    def __post_init__(self) -> None:
        if self.rank <= 0:
            raise LiveRecommendationError("rank must be positive")
        symbol = self.symbol.strip().upper()
        if not symbol:
            raise LiveRecommendationError("symbol is required")
        object.__setattr__(self, "symbol", symbol)


@dataclass(frozen=True)
class PositionRecommendation:
    symbol: str
    action: str
    reason: str = ""
    target_shares: Decimal | None = None

    def __post_init__(self) -> None:
        symbol = self.symbol.strip().upper()
        action = self.action.strip().upper()
        if not symbol:
            raise LiveRecommendationError("symbol is required")
        if action not in {"BUY", "ADD", "HOLD", "REDUCE", "EXIT"}:
            raise LiveRecommendationError(f"unsupported action: {action}")
        object.__setattr__(self, "symbol", symbol)
        object.__setattr__(self, "action", action)


@dataclass(frozen=True)
class LiveEngineDecision:
    market_date: date
    regime: str
    regime_subclass: str | None
    market_state: str
    market_gate: str
    entry_capacity: int
    strategy_branch: str
    reference_candidates: Tuple[ReferenceCandidate, ...] = ()
    position_recommendations: Tuple[PositionRecommendation, ...] = ()
    evidence: Mapping[str, object] = field(default_factory=dict)
    engine_id: str = "FD-M3180125-SP500-TOP3-engine"
    engine_version: str = "UNKNOWN"

    def __post_init__(self) -> None:
        if self.entry_capacity < 0:
            raise LiveRecommendationError(
                "entry_capacity must not be negative"
            )
        if len(self.reference_candidates) > 3:
            raise LiveRecommendationError(
                "Daily Reference Top 3 cannot exceed three candidates"
            )
        ranks = [item.rank for item in self.reference_candidates]
        if ranks != list(range(1, len(ranks) + 1)):
            raise LiveRecommendationError(
                "reference candidate ranks must be contiguous from 1"
            )


class LiveEnginePort(Protocol):
    """Port implemented by a composition around the shared Engine code."""

    def decide(
        self,
        *,
        market_date: date,
        market_data: LiveMarketData,
        account: LiveAccountState,
    ) -> LiveEngineDecision:
        ...
