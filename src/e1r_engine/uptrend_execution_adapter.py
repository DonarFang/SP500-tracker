from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from e1r_engine.state import OrderIntent


SUPPORTED_ACTIONS = frozenset({"BUY", "REDUCE", "EXIT"})


class UptrendExecutionAdapter:
    # Thin translation boundary only. No decision, pricing, fill,
    # sizing, or account mutation is allowed here.

    @staticmethod
    def from_legacy_pending_order(
        payload: Mapping[str, Any],
    ) -> OrderIntent:
        source = deepcopy(dict(payload))
        symbol = str(source.get("sym", "")).strip()
        action = str(source.get("action", "")).upper().strip()
        signal_date = str(source.get("signal_date", "")).strip()

        if not symbol:
            raise ValueError("legacy pending order missing sym")
        if not signal_date:
            raise ValueError(
                "legacy pending order missing signal_date"
            )
        if action not in SUPPORTED_ACTIONS:
            raise ValueError(
                "unsupported UPTREND execution action: "
                + repr(action)
            )

        reason = str(
            source.get(
                "primary_reason",
                source.get(
                    "entry_type",
                    source.get("reason", action),
                ),
            )
        )

        return OrderIntent(
            date=signal_date,
            symbol=symbol,
            intent_type=action,
            side="BUY" if action == "BUY" else "SELL",
            target_quantity=None,
            quantity_delta=None,
            reason=reason,
            branch="UPTREND",
            metadata={
                "source": "UptrendExecutionAdapter",
                "legacy_payload": source,
                "target_size_units": source.get(
                    "target_size_units"
                ),
                "e1r_entry_type": source.get("entry_type"),
                "legacy_action": action,
                "execution_performed": False,
                "account_mutated": False,
            },
        )

    @staticmethod
    def to_legacy_pending_order(
        intent: OrderIntent,
    ) -> dict[str, Any]:
        if intent.branch != "UPTREND":
            raise ValueError(
                "execution adapter accepts UPTREND intents only"
            )

        action = str(intent.intent_type).upper().strip()

        if action not in SUPPORTED_ACTIONS:
            raise ValueError(
                "unsupported UPTREND execution intent: "
                + repr(action)
            )
        if not intent.date:
            raise ValueError("OrderIntent date must be non-empty")
        if not intent.symbol:
            raise ValueError("OrderIntent symbol must be non-empty")

        preserved = intent.metadata.get("legacy_payload")

        if isinstance(preserved, Mapping):
            payload = deepcopy(dict(preserved))
            expected = {
                "sym": intent.symbol,
                "action": action,
                "signal_date": intent.date,
            }

            for key, value in expected.items():
                if payload.get(key) != value:
                    raise ValueError(
                        "preserved legacy payload conflicts with "
                        f"OrderIntent: {key}"
                    )

            return payload

        if action != "BUY":
            raise ValueError(
                "REDUCE/EXIT require preserved legacy payload"
            )

        target_size_units = intent.metadata.get(
            "target_size_units"
        )

        if target_size_units is None:
            raise ValueError(
                "BUY OrderIntent missing target_size_units"
            )

        entry_type = intent.metadata.get(
            "e1r_entry_type",
            intent.reason,
        )

        leader_rank = intent.metadata.get(
            "leader_rank_all"
        )
        leader_score = intent.metadata.get("leader_score")
        close_t = intent.metadata.get("close_t")
        entry_reasons = list(
            intent.metadata.get("entry_reasons", [])
        )

        if leader_score is None:
            raise ValueError(
                "BUY OrderIntent missing leader_score"
            )
        if close_t is None:
            raise ValueError(
                "BUY OrderIntent missing close_t"
            )

        payload: dict[str, Any] = {
            "sym": intent.symbol,
            "action": "BUY",
            "signal_date": intent.date,
            "ls": leader_score,
            "close_t": close_t,
            "entry_rank": leader_rank,
            "strategy": "E1R_UPTREND_EXECUTION_V0_1",
            "entry_mode": "e1r_uptrend_execution_v0_1",
            "primary_reason": entry_type,
            "reasons": entry_reasons,
            "e1r_entry_type": entry_type,
            "target_size_units": float(target_size_units),
        }

        return payload

    @staticmethod
    def normalize_legacy_pending_orders(
        payloads: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        normalized: list[dict[str, Any]] = []

        for payload in payloads:
            action = str(
                payload.get("action", "")
            ).upper().strip()

            if action == "ADD":
                normalized.append(deepcopy(dict(payload)))
                continue

            normalized.append(
                UptrendExecutionAdapter.to_legacy_pending_order(
                    UptrendExecutionAdapter
                    .from_legacy_pending_order(payload)
                )
            )

        return normalized
