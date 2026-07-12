"""Thin SIDEWAYS OrderIntent to legacy pending-order adapter."""

from __future__ import annotations

from e1r_engine.sideways_execution import SIDEWAYS_BRANCH
from e1r_engine.state import OrderIntent


class SidewaysExecutionAdapter:
    @staticmethod
    def to_legacy_pending_order(
        intent: OrderIntent,
    ) -> dict[str, object]:
        if intent.branch != SIDEWAYS_BRANCH:
            raise ValueError("adapter accepts SIDEWAYS intents only")
        action = str(intent.intent_type).upper()
        if action not in {"BUY", "REDUCE", "EXIT"}:
            raise ValueError(f"unsupported SIDEWAYS intent: {action}")

        payload: dict[str, object] = {
            "sym": intent.symbol,
            "action": action,
            "signal_date": intent.date,
            "ls": float(intent.metadata.get("sideways_entry_score", 0.0)),
            "close_t": float(intent.metadata.get("close_t", 0.0)),
            "entry_rank": intent.metadata.get("sideways_entry_rank"),
            "strategy": "E1R_SIDEWAYS_MA_CONFLICT_EXECUTION_V0_1",
            "entry_mode": "e1r_sideways_ma_conflict_execution_v0_1",
            "primary_reason": intent.reason,
            "reasons": [intent.reason],
            "origin_branch": SIDEWAYS_BRANCH,
            "entry_regime": "SIDEWAYS",
            "entry_subclass": "MA_CONFLICT",
            "entry_type": "E1R_SIDEWAYS_MA_CONFLICT",
        }
        if action == "BUY":
            payload["target_fraction_of_tradable_cash"] = float(
                intent.metadata["target_fraction_of_tradable_cash"]
            )
            payload["capital_fraction_of_tradable_cash"] = float(
                intent.metadata["capital_fraction_of_tradable_cash"]
            )
            payload["sideways_entry_rank"] = intent.metadata[
                "sideways_entry_rank"
            ]
            payload["sideways_entry_score"] = intent.metadata[
                "sideways_entry_score"
            ]
        if action == "REDUCE":
            payload["reduce_fraction"] = float(
                intent.metadata.get("reduce_fraction", 0.50)
            )
        return payload
