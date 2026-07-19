from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

MarketState = Literal["FULL_ON", "CAUTIOUS_ON", "CASH_MODE"]


@dataclass(frozen=True)
class MarketStateConfig:
    market_gate_enabled: bool = True
    market_shock_gate_enabled: bool = False
    market_shock_daily_return: float = -0.02
    use_ma50_slope: bool = True
    use_index_leadership: bool = True
    cash_leadership_threshold: float = 2.0 / 3.0
    full_on_leadership_threshold: float = 1.0


@dataclass(frozen=True)
class MarketStateInputs:
    date: str
    spx_close: float
    spx_ma50: float
    spx_ma50_10d_ago: float
    spx_day_return: float
    ndx_close: float | None = None
    ndx_ma50: float | None = None
    sox_close: float | None = None
    sox_ma50: float | None = None
    max_positions: int = 3


@dataclass(frozen=True)
class MarketStateDecision:
    date: str
    market_state: MarketState
    entry_capacity: int
    spx_close: float
    spx_ma50: float
    spx_ma50_slope: float
    spx_day_return: float
    spx_above_ma50: bool
    ndx_above_ma50: bool | None
    sox_above_ma50: bool | None
    leadership_count: int
    leadership_denominator: int
    leadership_ratio: float
    shock_active: bool
    trace: dict[str, Any] = field(default_factory=dict)


class MarketStateEvaluator:
    @staticmethod
    def _optional_above_ma50(
        close: float | None,
        ma50: float | None,
    ) -> bool | None:
        if close is None and ma50 is None:
            return None
        if close is None or ma50 is None:
            raise ValueError(
                "index close and MA50 must either both be present or both be absent"
            )
        return float(close) > float(ma50)

    @staticmethod
    def evaluate(
        config: MarketStateConfig,
        inputs: MarketStateInputs,
    ) -> MarketStateDecision:
        if not inputs.date:
            raise ValueError("date must be non-empty")
        if inputs.max_positions <= 0:
            raise ValueError("max_positions must be positive")
        if inputs.spx_ma50 <= 0:
            raise ValueError("spx_ma50 must be positive")

        spx_ma50_slope = (
            float(inputs.spx_ma50) / float(inputs.spx_ma50_10d_ago) - 1.0
            if inputs.spx_ma50_10d_ago > 0
            else 0.0
        )

        spx_above = float(inputs.spx_close) > float(inputs.spx_ma50)
        ndx_above = MarketStateEvaluator._optional_above_ma50(
            inputs.ndx_close, inputs.ndx_ma50
        )
        sox_above = MarketStateEvaluator._optional_above_ma50(
            inputs.sox_close, inputs.sox_ma50
        )

        leadership_values = [spx_above]
        if ndx_above is not None:
            leadership_values.append(ndx_above)
        if sox_above is not None:
            leadership_values.append(sox_above)

        leadership_count = sum(value is True for value in leadership_values)
        leadership_denominator = len(leadership_values)
        leadership_ratio = leadership_count / leadership_denominator

        shock_active = (
            config.market_shock_gate_enabled
            and float(inputs.spx_day_return) <= config.market_shock_daily_return
        )

        if not config.market_gate_enabled:
            market_state: MarketState = "FULL_ON"
            entry_capacity = inputs.max_positions
        else:
            cash_mode = (
                shock_active
                or (
                    config.use_index_leadership
                    and leadership_ratio < config.cash_leadership_threshold
                )
                or (
                    config.use_ma50_slope
                    and spx_ma50_slope < 0
                )
            )

            slope_ok = spx_ma50_slope >= 0 if config.use_ma50_slope else True
            leadership_strong = (
                leadership_ratio >= config.full_on_leadership_threshold
                if config.use_index_leadership
                else True
            )

            if cash_mode:
                market_state = "CASH_MODE"
                entry_capacity = 0
            elif spx_above and slope_ok and leadership_strong and not shock_active:
                market_state = "FULL_ON"
                entry_capacity = inputs.max_positions
            else:
                market_state = "CAUTIOUS_ON"
                entry_capacity = min(inputs.max_positions, 2)

        return MarketStateDecision(
            date=inputs.date,
            market_state=market_state,
            entry_capacity=int(entry_capacity),
            spx_close=float(inputs.spx_close),
            spx_ma50=float(inputs.spx_ma50),
            spx_ma50_slope=float(spx_ma50_slope),
            spx_day_return=float(inputs.spx_day_return),
            spx_above_ma50=spx_above,
            ndx_above_ma50=ndx_above,
            sox_above_ma50=sox_above,
            leadership_count=int(leadership_count),
            leadership_denominator=int(leadership_denominator),
            leadership_ratio=float(leadership_ratio),
            shock_active=bool(shock_active),
            trace={
                "source_contract": "formal 5Y Gate G4 source-equivalent chain",
                "vix_used": False,
                "cash_mode_formula": (
                    "shock_active OR leadership_ratio < 2/3 OR spx_ma50_slope < 0"
                ),
                "full_on_formula": (
                    "spx_close > spx_ma50 AND spx_ma50_slope >= 0 "
                    "AND leadership_ratio >= 1.0 AND NOT shock_active"
                ),
                "entry_capacity_mapping": {
                    "FULL_ON": inputs.max_positions,
                    "CAUTIOUS_ON": min(inputs.max_positions, 2),
                    "CASH_MODE": 0,
                },
            },
        )


__all__ = [
    "MarketState",
    "MarketStateConfig",
    "MarketStateDecision",
    "MarketStateEvaluator",
    "MarketStateInputs",
]
