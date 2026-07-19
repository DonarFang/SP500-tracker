"""Standalone E1R market gate contracts and pure evaluator.

This module is intentionally narrow.

It does not:
- rank candidates,
- generate BUY/ADD/REDUCE/EXIT orders,
- mutate account state,
- run a backtest,
- call legacy src.engine.backtest.

Source-equivalent contract from K2-R10:

    market_shock = market_shock_gate_enabled and spx_day_return <= market_shock_daily_return
    market_risk_off = (market_state == "CASH_MODE") and not market_shock
    market_entry_allowed = entry_capacity > 0
    gate_state = "ALLOW" if market_entry_allowed else "SHOCK" if market_shock else "RISK_OFF"

The direct formula "SPX close < SPX MA50 => RISK_OFF" must not be used as gate_state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


MarketState = Literal["FULL_ON", "CAUTIOUS_ON", "CASH_MODE", "UNKNOWN"]
GateState = Literal["ALLOW", "SHOCK", "RISK_OFF"]
BlockedAction = Literal["BUY", "ADD"]
UnaffectedAction = Literal["HOLD", "REDUCE", "EXIT"]


@dataclass(frozen=True)
class MarketGateConfig:
    """Source-proven market gate settings.

    Defaults reflect the formal 5Y D2_RISK_OFF_GATE / Gate G4 No-Shock contract
    recovered from canonical strategy commit d7eb4dc and verified against all 1259 formal dates.
    """

    variant: str = "D2_RISK_OFF_GATE"
    market_gate_enabled: bool = True
    risk_off_below_spx_ma50: bool = False
    market_shock_gate_enabled: bool = False
    market_shock_daily_return: float = -0.02


@dataclass(frozen=True)
class MarketGateInputs:
    """One-day upstream market gate inputs.

    `market_state` and `entry_capacity` are explicit inputs. They are not
    recomputed from SPX close/MA50 inside MarketGateEvaluator because the
    legacy source-equivalent gate chain uses upstream local variables.
    """

    date: str
    spx_close: float | None = None
    spx_ma50: float | None = None
    spx_day_return: float | None = None
    market_state: MarketState = "UNKNOWN"
    entry_capacity: int = 0
    existing_positions_count: int = 0


@dataclass(frozen=True)
class MarketGateDecision:
    """Pure market gate output for downstream branch logic."""

    date: str
    market_state: MarketState
    entry_capacity: int
    market_shock: bool
    market_risk_off: bool
    market_entry_allowed: bool
    gate_state: GateState
    blocked_actions: tuple[BlockedAction, ...] = ("BUY", "ADD")
    unaffected_actions: tuple[UnaffectedAction, ...] = ("HOLD", "REDUCE", "EXIT")
    trace: dict[str, Any] = field(default_factory=dict)


class MarketGateEvaluator:
    """Pure deterministic evaluator for the legacy-equivalent gate chain.

    The evaluator is intentionally side-effect free and does not know about
    portfolios, candidates, order sizing, or regime routing.
    """

    @staticmethod
    def evaluate(config: MarketGateConfig, inputs: MarketGateInputs) -> MarketGateDecision:
        """Evaluate market gate state for one day.

        This mirrors the recovered local-variable chain. It deliberately avoids
        replacing the chain with a simplified direct SPX/MA50 formula.
        """

        if inputs.entry_capacity < 0:
            raise ValueError(f"entry_capacity must be >= 0, got {inputs.entry_capacity!r}")

        if not config.market_gate_enabled:
            market_shock = False
            market_risk_off = False
            market_entry_allowed = True
            gate_state: GateState = "ALLOW"
        else:
            market_shock = (
                bool(config.market_shock_gate_enabled)
                and inputs.spx_day_return is not None
                and float(inputs.spx_day_return) <= float(config.market_shock_daily_return)
            )
            market_risk_off = (inputs.market_state == "CASH_MODE") and not market_shock
            market_entry_allowed = int(inputs.entry_capacity) > 0
            gate_state = "ALLOW" if market_entry_allowed else "SHOCK" if market_shock else "RISK_OFF"

        return MarketGateDecision(
            date=inputs.date,
            market_state=inputs.market_state,
            entry_capacity=int(inputs.entry_capacity),
            market_shock=bool(market_shock),
            market_risk_off=bool(market_risk_off),
            market_entry_allowed=bool(market_entry_allowed),
            gate_state=gate_state,
            trace={
                "variant": config.variant,
                "market_gate_enabled": config.market_gate_enabled,
                "risk_off_below_spx_ma50": config.risk_off_below_spx_ma50,
                "market_shock_gate_enabled": config.market_shock_gate_enabled,
                "market_shock_daily_return": config.market_shock_daily_return,
                "spx_close": inputs.spx_close,
                "spx_ma50": inputs.spx_ma50,
                "spx_day_return": inputs.spx_day_return,
                "source_equivalent_formula": (
                    "ALLOW if entry_capacity > 0 else SHOCK if market_shock else RISK_OFF"
                ),
                "not_used_as_gate_state_formula": "spx_close < spx_ma50",
            },
        )


__all__ = [
    "BlockedAction",
    "GateState",
    "MarketGateConfig",
    "MarketGateDecision",
    "MarketGateEvaluator",
    "MarketGateInputs",
    "MarketState",
    "UnaffectedAction",
]
