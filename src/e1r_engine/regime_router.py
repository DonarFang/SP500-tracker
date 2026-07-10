from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from e1r_engine.state import EngineBranch


@dataclass(frozen=True)
class RegimeRoute:
    date: str
    branch: EngineBranch
    spx_regime: str | None
    subclass: str | None
    reason: str
    metadata: dict[str, Any]


class RegimeRouter:
    """
    RegimeRouter shell for standalone E1R Engine.

    Responsibility:
    - Convert normalized regime record into an engine branch label.
    - Preserve explicit branch routing trace.

    Must not:
    - Decide BUY/SELL/HOLD/ADD/REDUCE/EXIT.
    - Rank candidates.
    - Size positions.
    - Apply market gates.
    - Execute orders.
    """

    def route(self, date: str, spx_regime: str | None, subclass: str | None) -> RegimeRoute:
        normalized_regime = (spx_regime or "UNKNOWN").upper()
        normalized_subclass = (subclass or "NO_SUBCLASS").upper()

        if normalized_regime == "UPTREND":
            branch: EngineBranch = "UPTREND"
            reason = "route_uptrend"

        elif normalized_regime == "SIDEWAYS" and normalized_subclass == "MA_CONFLICT":
            branch = "SIDEWAYS_MA_CONFLICT"
            reason = "route_sideways_ma_conflict"

        elif normalized_subclass == "DETERIORATION_TRANSITION":
            branch = "DETERIORATION_TRANSITION"
            reason = "route_deterioration_transition"

        elif normalized_subclass == "RECOVERY_TRANSITION":
            branch = "RECOVERY_TRANSITION"
            reason = "route_recovery_transition"

        elif normalized_regime == "DOWNTREND":
            branch = "DOWNTREND"
            reason = "route_downtrend"

        else:
            branch = "CASH_DEFENSIVE"
            reason = "route_default_cash_defensive"

        return RegimeRoute(
            date=date,
            branch=branch,
            spx_regime=normalized_regime,
            subclass=normalized_subclass,
            reason=reason,
            metadata={
                "router_shell_only": True,
                "no_strategy_decision": True,
            },
        )
