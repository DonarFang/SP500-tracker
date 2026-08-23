"""Replay confirmed Live transactions into deterministic Engine cycle state.

Recommendations never mutate this state.  Only append-only transaction events
that have actually been recorded by the owner are consumed.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import hashlib
import json
from pathlib import Path
from typing import Iterable

from .capped_atr_stop import VARIANT_ID
from .live_ledger import ManualAction, TransactionEvent


class LiveCycleStateError(ValueError):
    pass


@dataclass(frozen=True)
class LiveCycleState:
    symbol: str
    cycle_id: str
    first_buy_price: float
    size_units: float
    add_count: int
    reduce_count: int
    origin_branch: str
    entry_signal_date: str | None
    expected_execution_date: str | None
    entry_recommendation_id: str | None
    last_event_id: str
    strategy_variant: str

    def to_metadata(self) -> dict[str, object]:
        return {
            "live_cycle_id": self.cycle_id,
            "first_buy_price": self.first_buy_price,
            "size_units": self.size_units,
            "add_count": self.add_count,
            "reduce_count": self.reduce_count,
            "origin_branch": self.origin_branch,
            "entry_signal_date": self.entry_signal_date,
            "expected_execution_date": self.expected_execution_date,
            "entry_recommendation_id": self.entry_recommendation_id,
            "last_confirmed_event_id": self.last_event_id,
            "strategy_variant": self.strategy_variant,
            "cycle_state_source": "CONFIRMED_TRANSACTION_REPLAY",
        }


def stable_recommendation_id(
    *, signal_date: str, expected_execution_date: str, symbol: str, action: str
) -> str:
    raw = "|".join(
        (
            signal_date,
            expected_execution_date,
            symbol.strip().upper(),
            action.strip().upper(),
        )
    ).encode("utf-8")
    return "REC-" + hashlib.sha256(raw).hexdigest()[:24].upper()


def _cycle_id(symbol: str, event_id: str) -> str:
    raw = f"{symbol}|{event_id}".encode("utf-8")
    return "CYCLE-" + hashlib.sha256(raw).hexdigest()[:20].upper()


def replay_live_cycles(
    events: Iterable[TransactionEvent],
) -> dict[str, LiveCycleState]:
    states: dict[str, LiveCycleState] = {}
    seen: set[str] = set()
    for event in events:
        if event.event_id in seen:
            continue
        seen.add(event.event_id)
        symbol = event.symbol
        previous = states.get(symbol)
        if event.action is ManualAction.BUY:
            if previous is not None:
                raise LiveCycleStateError(f"{symbol}: BUY inside active cycle")
            units = float(event.target_size_units or 1.0)
            states[symbol] = LiveCycleState(
                symbol=symbol,
                cycle_id=_cycle_id(symbol, event.event_id),
                first_buy_price=float(event.price),
                size_units=units,
                add_count=0,
                reduce_count=0,
                origin_branch=event.origin_branch or "UPTREND",
                entry_signal_date=(
                    event.signal_date.isoformat() if event.signal_date else None
                ),
                expected_execution_date=(
                    event.expected_execution_date.isoformat()
                    if event.expected_execution_date
                    else None
                ),
                entry_recommendation_id=event.recommendation_id,
                last_event_id=event.event_id,
                strategy_variant=event.strategy_variant or VARIANT_ID,
            )
            continue
        if previous is None:
            raise LiveCycleStateError(
                f"{symbol}: {event.action.value} without active cycle"
            )
        if event.action is ManualAction.ADD:
            units = min(1.0, previous.size_units + 0.5)
            states[symbol] = LiveCycleState(
                **{
                    **previous.__dict__,
                    "size_units": units,
                    "add_count": previous.add_count + 1,
                    "last_event_id": event.event_id,
                }
            )
        elif event.action is ManualAction.REDUCE:
            units = max(0.5, previous.size_units - 0.5)
            states[symbol] = LiveCycleState(
                **{
                    **previous.__dict__,
                    "size_units": units,
                    "reduce_count": previous.reduce_count + 1,
                    "last_event_id": event.event_id,
                }
            )
        elif event.action is ManualAction.EXIT:
            del states[symbol]
    return states


def load_transaction_events(live_root: Path) -> tuple[TransactionEvent, ...]:
    journal = Path(live_root) / "runtime/history/ledger_journal.jsonl"
    if not journal.is_file():
        return ()
    events: list[TransactionEvent] = []
    for line_number, raw in enumerate(
        journal.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not raw.strip():
            continue
        row = json.loads(raw)
        payload = row.get("event")
        if row.get("ledger") != "TRANSACTION":
            continue
        if not isinstance(payload, dict):
            raise LiveCycleStateError(
                f"journal line {line_number}: event must be object"
            )
        clean = {key: value for key, value in payload.items() if key != "event_type"}
        clean["trade_date"] = date.fromisoformat(str(clean["trade_date"]))
        for field in ("signal_date", "expected_execution_date"):
            if clean.get(field) is not None:
                clean[field] = date.fromisoformat(str(clean[field]))
        events.append(TransactionEvent(**clean))
    return tuple(events)


__all__ = [
    "LiveCycleState",
    "LiveCycleStateError",
    "load_transaction_events",
    "replay_live_cycles",
    "stable_recommendation_id",
]
