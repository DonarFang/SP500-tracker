"""Canonical frozen-entry CAPPED-ATR stop for E1R.

This module owns the only production definition of the promoted stop.  Runtime
adapters may translate their native order/state shapes, but must call this
policy for ATR calculation, cycle-state construction and action resolution.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import math
from typing import Any, Mapping, Sequence

from e1r_engine.state import AccountState, OrderIntent


ENGINE_ID = "FD-M3180125-SP500-TOP3-engine"
VARIANT_ID = "E1R_CAPPED_ATR_A0_V1"
DISPLAY_NAME = "E1R CAPPED-ATR Engine"
HARD_STOP_MODEL = "CAPPED_ATR_FROZEN_ENTRY_A0"
HARD_STOP_REASON = "HARD_LOSS_STOP"
ORIGINAL_EXIT_REASON = "ORIGINAL_ENGINE_EXIT"

ENTRY_METADATA_KEY = "capped_atr_entry"
POSITION_METADATA_KEY = "capped_atr_stop"
BOUNDARY_ABS_TOLERANCE = 1e-12


@dataclass(frozen=True)
class CappedAtrStopConfig:
    atr_lookback: int = 20
    atr_multiplier: float = 3.0
    distance_floor_fraction_of_a0: float = 0.12
    distance_cap_fraction_of_a0: float = 0.20
    block_same_day_reentry_after_hard_stop: bool = False

    def validate(self) -> None:
        if self.atr_lookback != 20:
            raise ValueError("CAPPED-ATR lookback must remain 20")
        if not math.isclose(self.atr_multiplier, 3.0):
            raise ValueError("CAPPED-ATR multiplier must remain 3.0")
        if not math.isclose(self.distance_floor_fraction_of_a0, 0.12):
            raise ValueError("CAPPED-ATR floor must remain 12% of A0")
        if not math.isclose(self.distance_cap_fraction_of_a0, 0.20):
            raise ValueError("CAPPED-ATR cap must remain 20% of A0")
        if self.block_same_day_reentry_after_hard_stop:
            raise ValueError("same-day re-entry after stop execution must remain allowed")


@dataclass(frozen=True)
class CappedAtrStopState:
    a0: float
    atr20: float
    atr_as_of: str
    distance: float
    distance_fraction: float
    trigger_price: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "variant_id": VARIANT_ID,
            "hard_stop_model": HARD_STOP_MODEL,
            "a0": self.a0,
            "atr20": self.atr20,
            "atr_as_of": self.atr_as_of,
            "distance": self.distance,
            "distance_fraction": self.distance_fraction,
            "trigger_price": self.trigger_price,
            "atr_frozen_for_cycle": True,
            "add_updates_stop_anchor": False,
            "block_same_day_reentry_after_hard_stop": False,
        }

    @staticmethod
    def from_mapping(value: Mapping[str, Any]) -> "CappedAtrStopState":
        if value.get("hard_stop_model") != HARD_STOP_MODEL:
            raise ValueError("position has the wrong hard-stop model")
        state = CappedAtrStopState(
            a0=float(value["a0"]),
            atr20=float(value["atr20"]),
            atr_as_of=str(value["atr_as_of"]),
            distance=float(value["distance"]),
            distance_fraction=float(value["distance_fraction"]),
            trigger_price=float(value["trigger_price"]),
        )
        state.validate()
        return state

    def validate(self) -> None:
        values = (
            self.a0,
            self.atr20,
            self.distance,
            self.distance_fraction,
            self.trigger_price,
        )
        if any(not math.isfinite(value) or value <= 0.0 for value in values):
            raise ValueError("CAPPED-ATR state values must be finite and positive")
        if not self.atr_as_of:
            raise ValueError("CAPPED-ATR state is missing atr_as_of")
        expected_trigger = self.a0 - self.distance
        if not math.isclose(
            self.trigger_price,
            expected_trigger,
            rel_tol=0.0,
            abs_tol=BOUNDARY_ABS_TOLERANCE,
        ):
            raise ValueError("CAPPED-ATR trigger is inconsistent with A0-distance")
        if not math.isclose(
            self.distance_fraction,
            self.distance / self.a0,
            rel_tol=0.0,
            abs_tol=BOUNDARY_ABS_TOLERANCE,
        ):
            raise ValueError("CAPPED-ATR distance fraction is inconsistent")


def _finite_positive(value: Any) -> bool:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number) and number > 0.0


def compute_entry_atr20(
    *,
    symbol: str,
    dates: Sequence[str],
    closes: Sequence[float],
    ohlc: Mapping[str, Sequence[float]],
    as_of_date: str,
    config: CappedAtrStopConfig | None = None,
) -> float | None:
    """Simple mean of the last 20 complete True Range observations through T."""
    cfg = config or CappedAtrStopConfig()
    cfg.validate()
    try:
        end_index = list(dates).index(as_of_date)
    except ValueError:
        return None
    highs = ohlc.get("high", ())
    lows = ohlc.get("low", ())
    if end_index < 1:
        return None
    upper = min(
        end_index,
        len(dates) - 1,
        len(closes) - 1,
        len(highs) - 1,
        len(lows) - 1,
    )
    true_ranges: list[float] = []
    for index in range(1, upper + 1):
        previous_close = closes[index - 1]
        high = highs[index]
        low = lows[index]
        if not all(_finite_positive(value) for value in (previous_close, high, low)):
            continue
        previous_close_f = float(previous_close)
        high_f = float(high)
        low_f = float(low)
        true_ranges.append(
            max(
                high_f - low_f,
                abs(high_f - previous_close_f),
                abs(low_f - previous_close_f),
            )
        )
    if len(true_ranges) < cfg.atr_lookback:
        return None
    return sum(true_ranges[-cfg.atr_lookback :]) / cfg.atr_lookback


def build_entry_metadata(*, atr20: float, atr_as_of: str) -> dict[str, Any]:
    if not _finite_positive(atr20) or not atr_as_of:
        raise ValueError("first-entry BUY requires a valid ATR20 and atr_as_of")
    return {
        "variant_id": VARIANT_ID,
        "hard_stop_model": HARD_STOP_MODEL,
        "atr20": float(atr20),
        "atr_as_of": str(atr_as_of),
    }


def build_frozen_state(
    *,
    adjusted_first_buy_price: float,
    entry_metadata: Mapping[str, Any],
    config: CappedAtrStopConfig | None = None,
) -> CappedAtrStopState:
    cfg = config or CappedAtrStopConfig()
    cfg.validate()
    a0 = float(adjusted_first_buy_price)
    atr20 = float(entry_metadata.get("atr20", 0.0))
    atr_as_of = str(entry_metadata.get("atr_as_of", ""))
    if not _finite_positive(a0):
        raise ValueError("A0 must be the positive cost-adjusted first BUY fill price")
    if not _finite_positive(atr20) or not atr_as_of:
        raise ValueError("CAPPED-ATR first BUY is missing valid frozen ATR20 input")
    floor_distance = cfg.distance_floor_fraction_of_a0 * a0
    cap_distance = cfg.distance_cap_fraction_of_a0 * a0
    distance = min(max(cfg.atr_multiplier * atr20, floor_distance), cap_distance)
    state = CappedAtrStopState(
        a0=a0,
        atr20=atr20,
        atr_as_of=atr_as_of,
        distance=distance,
        distance_fraction=distance / a0,
        trigger_price=a0 - distance,
    )
    state.validate()
    return state


def triggered_at_close(*, close: float, state: CappedAtrStopState) -> bool:
    close_f = float(close)
    if not _finite_positive(close_f):
        raise ValueError("CAPPED-ATR evaluation requires a positive finite close")
    return close_f < state.trigger_price or math.isclose(
        close_f,
        state.trigger_price,
        rel_tol=0.0,
        abs_tol=BOUNDARY_ABS_TOLERANCE,
    )


def annotate_buy_intent(
    intent: OrderIntent,
    *,
    atr20: float,
    atr_as_of: str,
) -> OrderIntent:
    if intent.intent_type != "BUY":
        return intent
    metadata = dict(intent.metadata)
    metadata[ENTRY_METADATA_KEY] = build_entry_metadata(
        atr20=atr20,
        atr_as_of=atr_as_of,
    )
    return replace(intent, metadata=metadata)


def annotate_legacy_buy_order(
    order: Mapping[str, Any],
    *,
    atr20: float,
    atr_as_of: str,
) -> dict[str, Any]:
    annotated = dict(order)
    if str(annotated.get("action", "")).upper() == "BUY":
        annotated[ENTRY_METADATA_KEY] = build_entry_metadata(
            atr20=atr20,
            atr_as_of=atr_as_of,
        )
    return annotated


def _canonical_action(action: Any) -> str:
    normalized = str(action or "HOLD").upper()
    if normalized in {"REL_REDUCE", "TP_REDUCE"}:
        return "REDUCE"
    if normalized not in {"EXIT", "REDUCE", "ADD", "HOLD"}:
        raise ValueError("unsupported canonical management action: " + normalized)
    return normalized


def _trace_row(
    *,
    date: str,
    symbol: str,
    close: float,
    state: CappedAtrStopState,
    canonical_action: str,
) -> dict[str, Any]:
    primary = ORIGINAL_EXIT_REASON if canonical_action == "EXIT" else HARD_STOP_REASON
    reasons = [HARD_STOP_REASON]
    if canonical_action == "EXIT":
        reasons.insert(0, ORIGINAL_EXIT_REASON)
    return {
        "decision_date": date,
        "symbol": symbol,
        "variant_id": VARIANT_ID,
        "hard_stop_model": HARD_STOP_MODEL,
        "canonical_action": canonical_action,
        "final_action": "EXIT",
        "primary_reason": primary,
        "triggered_reasons": reasons,
        "current_close": float(close),
        "hard_stop_anchor_price": state.a0,
        "hard_stop_distance_price": state.distance,
        "hard_stop_trigger_price": state.trigger_price,
        "frozen_entry_atr20": state.atr20,
        "frozen_entry_atr_as_of": state.atr_as_of,
        "inclusive_boundary": True,
        "execution_timing": "T_PLUS_1_ADVERSE_LOW",
    }


class CappedAtrStopPolicy:
    """Shared strategy policy used by Core Engine and historical adapters."""

    @staticmethod
    def apply_engine_orders(
        *,
        date: str,
        branch: str,
        account: AccountState,
        orders: Sequence[OrderIntent],
        strict: bool,
    ) -> tuple[list[OrderIntent], list[dict[str, Any]]]:
        output = list(orders)
        traces: list[dict[str, Any]] = []
        for symbol, position in sorted(account.positions.items()):
            raw_state = position.metadata.get(POSITION_METADATA_KEY)
            if raw_state is None:
                if strict:
                    raise RuntimeError("missing frozen A0/ATR stop state for " + symbol)
                continue
            state = CappedAtrStopState.from_mapping(raw_state)
            close = position.last_price
            if not triggered_at_close(close=close, state=state):
                continue
            matches = [order for order in output if order.symbol == symbol]
            if len(matches) > 1:
                raise RuntimeError("multiple Engine management intents for " + symbol)
            canonical_action = _canonical_action(
                matches[0].intent_type if matches else "HOLD"
            )
            traces.append(
                _trace_row(
                    date=date,
                    symbol=symbol,
                    close=close,
                    state=state,
                    canonical_action=canonical_action,
                )
            )
            if canonical_action == "EXIT":
                continue
            output = [order for order in output if order.symbol != symbol]
            output.append(
                OrderIntent(
                    date=date,
                    symbol=symbol,
                    intent_type="EXIT",
                    side="SELL",
                    target_quantity=0.0,
                    quantity_delta=-position.quantity,
                    reason=HARD_STOP_REASON,
                    branch=branch,
                    metadata={
                        "variant_id": VARIANT_ID,
                        "hard_stop_model": HARD_STOP_MODEL,
                        "stop_state": state.to_dict(),
                        "trigger_close": float(close),
                        "signal_timing": "T_EOD",
                        "execution_timing": "T_PLUS_1_ADVERSE_LOW",
                    },
                )
            )
        return output, traces

    @staticmethod
    def apply_legacy_management_orders(
        *,
        date: str,
        holdings: Mapping[str, Mapping[str, Any]],
        canonical_orders: Sequence[Mapping[str, Any]],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        by_symbol: dict[str, Mapping[str, Any]] = {}
        for order in canonical_orders:
            symbol = str(order.get("sym", ""))
            if not symbol:
                raise ValueError("management order missing symbol")
            if symbol in by_symbol:
                raise RuntimeError("multiple canonical management orders for " + symbol)
            by_symbol[symbol] = order

        final_by_symbol: dict[str, dict[str, Any]] = {}
        traces: list[dict[str, Any]] = []
        for symbol in sorted(holdings):
            holding = holdings[symbol]
            raw_state = holding.get(POSITION_METADATA_KEY)
            if raw_state is None:
                raise RuntimeError("missing frozen A0/ATR stop state for " + symbol)
            state = CappedAtrStopState.from_mapping(raw_state)
            close = float(holding.get("current_close", state.a0))
            if not triggered_at_close(close=close, state=state):
                continue
            canonical_order = by_symbol.get(symbol)
            canonical_action = _canonical_action(
                canonical_order.get("action") if canonical_order else "HOLD"
            )
            traces.append(
                _trace_row(
                    date=date,
                    symbol=symbol,
                    close=close,
                    state=state,
                    canonical_action=canonical_action,
                )
            )
            if canonical_action == "EXIT" and canonical_order is not None:
                final_by_symbol[symbol] = dict(canonical_order)
                continue
            final_by_symbol[symbol] = {
                "sym": symbol,
                "action": "EXIT",
                "signal_date": date,
                "ls": float(holding.get("leader_score_entry", 0.0)),
                "close_t": close,
                "entry_rank": None,
                "strategy": VARIANT_ID,
                "primary_reason": HARD_STOP_REASON,
                "reasons": [HARD_STOP_REASON],
                "origin_branch": str(holding.get("origin_branch") or "UPTREND"),
                "hard_stop_model": HARD_STOP_MODEL,
                "hard_stop_trigger_price": state.trigger_price,
                "frozen_entry_atr20": state.atr20,
                "frozen_entry_atr_as_of": state.atr_as_of,
            }

        output: list[dict[str, Any]] = []
        for order in canonical_orders:
            symbol = str(order.get("sym"))
            if symbol in final_by_symbol:
                output.append(final_by_symbol.pop(symbol))
            elif symbol not in holdings:
                output.append(dict(order))
            else:
                output.append(dict(order))
        for symbol in sorted(final_by_symbol):
            output.append(final_by_symbol[symbol])
        return output, traces
