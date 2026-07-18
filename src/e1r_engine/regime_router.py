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
    Sole strategy-branch router for canonical Engine Regime decisions.

    It validates canonical Regime/subclass combinations before routing.
    Invalid, unknown and UNCLASSIFIED inputs remain defensive.
    """

    _VALID_COMBINATIONS = {
        ("UNCLASSIFIED", "NO_SUBCLASS"),
        ("UPTREND", "NO_SUBCLASS"),
        ("DOWNTREND", "NO_SUBCLASS"),
        ("SIDEWAYS", "MA_CONFLICT"),
        ("SIDEWAYS", "DETERIORATION_TRANSITION"),
        ("SIDEWAYS", "RECOVERY_TRANSITION"),
    }

    _KNOWN_REGIMES = {
        "UNCLASSIFIED",
        "UPTREND",
        "SIDEWAYS",
        "DOWNTREND",
    }

    def route(
        self,
        date: str,
        spx_regime: str | None,
        subclass: str | None,
    ) -> RegimeRoute:
        normalized_regime = (
            spx_regime or "UNKNOWN"
        ).upper()

        normalized_subclass = (
            subclass or "NO_SUBCLASS"
        ).upper()

        combination = (
            normalized_regime,
            normalized_subclass,
        )

        if normalized_regime not in self._KNOWN_REGIMES:
            branch: EngineBranch = "CASH_DEFENSIVE"
            reason = "route_unknown_cash_defensive"

        elif combination not in self._VALID_COMBINATIONS:
            branch = "CASH_DEFENSIVE"
            reason = (
                "route_invalid_regime_subclass_combination"
            )

        elif normalized_regime == "UNCLASSIFIED":
            branch = "CASH_DEFENSIVE"
            reason = "route_unclassified_cash_defensive"

        elif normalized_regime == "UPTREND":
            branch = "UPTREND"
            reason = "route_uptrend"

        elif combination == (
            "SIDEWAYS",
            "MA_CONFLICT",
        ):
            branch = "SIDEWAYS_MA_CONFLICT"
            reason = "route_sideways_ma_conflict"

        elif combination == (
            "SIDEWAYS",
            "DETERIORATION_TRANSITION",
        ):
            branch = "DETERIORATION_TRANSITION"
            reason = "route_deterioration_transition"

        elif combination == (
            "SIDEWAYS",
            "RECOVERY_TRANSITION",
        ):
            branch = "RECOVERY_TRANSITION"
            reason = "route_recovery_transition"

        elif normalized_regime == "DOWNTREND":
            branch = "DOWNTREND"
            reason = "route_downtrend"

        else:
            branch = "CASH_DEFENSIVE"
            reason = "route_unreachable_cash_defensive"

        return RegimeRoute(
            date=date,
            branch=branch,
            spx_regime=normalized_regime,
            subclass=normalized_subclass,
            reason=reason,
            metadata={
                "router_shell_only": True,
                "no_strategy_decision": True,
                "combination_valid": (
                    combination
                    in self._VALID_COMBINATIONS
                ),
            },
        )
