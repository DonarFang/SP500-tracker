"""Frozen LSS07 exit overlay. Pure Engine logic; no files, broker or ledger writes."""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date as iso_date
import math
from typing import Mapping

from e1r_engine.contracts import MarketSnapshot
from e1r_engine.state import DailyEngineResult, OrderIntent
from e1r_engine.uptrend_signal_adapter import UptrendSignalAdapter

VERSION = "LSS07-SP500-FROZEN-1.0"


@dataclass(frozen=True)
class LSS07Config:
    enabled: bool = False
    effective_signal_date: str | None = None

    def __post_init__(self):
        if type(self.enabled) is not bool:
            raise ValueError("LSS07 enabled must be boolean")
        if self.effective_signal_date is not None:
            parsed = iso_date.fromisoformat(self.effective_signal_date)
            if parsed.isoformat() != self.effective_signal_date:
                raise ValueError("LSS07 effective date must be YYYY-MM-DD")
        if self.enabled and self.effective_signal_date is None:
            raise ValueError("LSS07 requires explicit effective signal date")

    def active(self, day: str) -> bool:
        return self.enabled and day >= self.effective_signal_date


def slope(values):
    # Same OLS expression as the frozen research implementation.
    n = len(values)
    xm = (n - 1) / 2
    ym = sum(values) / n
    return sum((i - xm) * (v - ym) for i, v in enumerate(values)) / sum(
        (i - xm) ** 2 for i in range(n)
    )


def evaluate(observation: Mapping[str, object], actions=()):
    """Return a reason; permission/priority comes before the extra EXIT."""
    actions = set(actions)
    if "EXIT" in actions:
        return "CANONICAL_FULL_EXIT_PRIORITY"
    if actions & {"BUY", "ADD"}:
        return "BUY_ADD_UNCHANGED_NO_OVERLAY"
    if not observation.get("ready"):
        return "DATA_NOT_READY"
    extreme = (observation["score"] < 60 and observation["rank"] > 150
               and observation["score_slope"] < 0
               and observation["rank_slope"] > 0)
    if not extreme:
        return "NO_TRIGGER"
    if observation["close"] > observation["previous_close"]:
        return "REPAIR_DEFER_TODAY_ONLY"
    return "EXTREME_EXIT"


def observations(snapshot: MarketSnapshot, held_symbols):
    """Six market sessions, current track universe, causal adjusted history.

    Scores reuse the canonical adapter. Alphabetical ties and (rank-1)/(N-1)
    reproduce the frozen research ranking. This never changes BUY ranking.
    """
    held_symbols = sorted(held_symbols)
    if not held_symbols:
        return {}
    unavailable = lambda reason: {
        s: {"ready": False, "missing_reason": reason} for s in held_symbols
    }
    days = sorted(d for d in snapshot.history_by_symbol.get("SPX", {})
                  if d <= snapshot.date)[-6:]
    if len(days) != 6 or days[-1] != snapshot.date:
        return unavailable("SIX_MARKET_SESSIONS_REQUIRED")
    universe = sorted(snapshot.universe)
    if len(universe) != len(set(universe)):
        raise ValueError("duplicate LSS07 universe symbol")
    if any(s not in snapshot.history_by_symbol for s in universe):
        return unavailable("UNIVERSE_HISTORY_MISSING")
    daily = []
    for day in days:
        prices = {}
        for s in universe:
            rows = snapshot.history_by_symbol[s]
            values = [float(rows[d].close) for d in sorted(rows) if d <= day]
            if any(not math.isfinite(v) or v <= 0 for v in values):
                return unavailable("INVALID_ADJUSTED_CLOSE")
            prices[s] = values
        signals = UptrendSignalAdapter.build(
            date=day, symbols=tuple(universe), prices_by_symbol=prices,
            ls60_exit_mode="exit",
        )
        n = len(signals.leader_rank_all)
        daily.append({s: {
            "score": float(signals.day_signals[s]["leader_score"]),
            "rank": rank, "rank_fraction": (rank - 1) / (n - 1) if n > 1 else 0.,
            "universe_count": n,
        } for s, rank in signals.leader_rank_all.items()})
    output = {}
    for s in held_symbols:
        rows = snapshot.history_by_symbol.get(s, {})
        if any(s not in item or d not in rows for d, item in zip(days, daily)):
            output[s] = {"ready": False, "missing_reason": "HELD_SYMBOL_SIX_SESSION_HISTORY_MISSING"}
            continue
        samples = [dict(item[s], date=d) for d, item in zip(days, daily)]
        output[s] = dict(
            ready=True, score=samples[-1]["score"], rank=samples[-1]["rank"],
            score_slope=slope([x["score"] for x in samples]),
            rank_slope=slope([x["rank_fraction"] for x in samples]),
            close=float(rows[days[-1]].close), previous_close=float(rows[days[-2]].close),
            samples=samples, rank_fraction_definition="(rank-1)/(N-1)",
            tie_order="SYMBOL_ASCENDING", universe_policy="CURRENT_TRACK_SNAPSHOT",
        )
    return output


def apply_lss07(*, snapshot: MarketSnapshot, result: DailyEngineResult,
                config: LSS07Config) -> DailyEngineResult:
    if not config.active(snapshot.date):
        return result
    observed = observations(snapshot, result.account_after.positions)
    orders = list(result.order_intents)
    audit = []
    changed = []
    for symbol, position in sorted(result.account_after.positions.items()):
        own = [o for o in orders if o.symbol == symbol]
        obs = observed[symbol]
        reason = evaluate(obs, [o.intent_type for o in own])
        row = dict(symbol=symbol, reason=reason, observation=obs,
                   signal_date=snapshot.date, entry_date=position.entry_date,
                   remaining_quantity=position.quantity)
        audit.append(row)
        if reason != "EXTREME_EXIT" or position.quantity <= 0:
            continue
        orders = [o for o in orders if o.symbol != symbol and o.intent_type != "NOOP"]
        orders.append(OrderIntent(
            date=snapshot.date, symbol=symbol, intent_type="EXIT", side="SELL",
            target_quantity=0.0, quantity_delta=None, reason="LSS07_EXTREME_EXIT",
            branch=result.decision_trace.branch,
            metadata={"origin_branch": position.metadata.get("origin_branch", "UPTREND"),
                      "engine_owned_position_management": True,
                      "strategy_version": VERSION, "lss07": row,
                      "effective_signal_date": config.effective_signal_date,
                      "signal_date": snapshot.date, "execute_on": "NEXT_TRADING_SESSION",
                      "exit_all_remaining": True, "minhold_override": True},
        ))
        changed.append(symbol)
    summary = dict(version=VERSION, effective_signal_date=config.effective_signal_date,
                   status="EVALUATED", changed_symbols=changed, evaluations=audit)
    trace = replace(result.decision_trace, order_intents=orders,
                    metadata=dict(result.decision_trace.metadata, lss07=summary))
    return replace(result, order_intents=orders, decision_trace=trace,
                   metadata=dict(result.metadata, lss07=summary))
