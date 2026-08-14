"""Canonical one-call decision orchestration used by Forward and Live.

This module contains no alternate formulas.  It composes the already
canonical Engine components behind :meth:`E1RCoreEngine.step` so callers pass
raw dated bars and receive the complete daily decision in one call.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping, TYPE_CHECKING

from engine.trade_decision import is_broken_trend

from e1r_engine.canonical_regime import CanonicalRegimeGenerator
from e1r_engine.capped_atr_stop import (
    POSITION_METADATA_KEY,
    VARIANT_ID,
    build_entry_metadata,
    build_frozen_state,
    compute_entry_atr20,
)
from e1r_engine.contracts import AssetSeries, DailyBar, MarketSnapshot
from e1r_engine.sideways_core import SidewaysCore
from e1r_engine.sideways_execution import SidewaysExecutionPolicy
from e1r_engine.state import (
    AccountState,
    DailyEngineResult,
    DecisionTrace,
    OrderIntent,
)
from e1r_engine.uptrend_consumer import UptrendDecisionConsumer
from e1r_engine.uptrend_signal_adapter import UptrendSignalAdapter

if TYPE_CHECKING:
    from e1r_engine.core import E1RCoreEngine


MIN_HOLDING_DAYS = 10
LS60_EXIT_MODE = "exit"


def _through_date(
    series: Mapping[str, DailyBar], date: str
) -> dict[str, DailyBar]:
    return {
        row_date: series[row_date]
        for row_date in sorted(series)
        if row_date <= date
    }


def _asset(symbol: str, series: Mapping[str, DailyBar], date: str) -> AssetSeries:
    rows = _through_date(series, date)
    dates = list(rows)
    bars = [rows[item] for item in dates]
    return AssetSeries(
        symbol=symbol,
        dates=dates,
        closes=[float(bar.close) for bar in bars],
        bars=bars,
        source_path="engine://market_snapshot/history_by_symbol",
    )


def _sideways_asset(
    symbol: str, series: Mapping[str, DailyBar], date: str
) -> dict[str, Any]:
    rows = _through_date(series, date)
    bars = [
        {"date": row_date, "close": float(bar.close)}
        for row_date, bar in rows.items()
    ]
    return {
        "symbol": symbol,
        "bars": bars,
        "dates": [row["date"] for row in bars],
        "by_date": {row["date"]: row for row in bars},
        "date_to_idx": {row["date"]: index for index, row in enumerate(bars)},
    }


class CanonicalRuntime:
    """Build one complete Engine decision from raw, dated market history."""

    @staticmethod
    def decide(
        *, engine: "E1RCoreEngine", snapshot: MarketSnapshot, account: AccountState
    ) -> tuple[DailyEngineResult, Any]:
        history = snapshot.history_by_symbol
        required = set(snapshot.universe) | {"SPX", "NDX", "SOX"}
        missing = sorted(required - set(history))
        if missing:
            raise ValueError(
                "canonical Engine entry missing history: " + ",".join(missing)
            )

        for symbol in required:
            if snapshot.date not in history[symbol]:
                raise ValueError(
                    f"{symbol}: canonical Engine entry missing {snapshot.date} bar"
                )

        spx = _asset("SPX", history["SPX"], snapshot.date)
        regime_record = CanonicalRegimeGenerator.generate(spx).record_for_date(
            snapshot.date
        )
        route = engine.router.route(
            date=snapshot.date,
            spx_regime=regime_record.spx_regime,
            subclass=regime_record.subclass,
        )

        prices = {
            symbol: float(snapshot.prices_by_symbol[symbol].close)
            for symbol in snapshot.prices_by_symbol
        }
        account_after = account.mark_to_market(prices=prices, date=snapshot.date)
        account_after = CanonicalRuntime._hydrate_live_cycles(
            account=account_after,
            history=history,
            universe=snapshot.universe,
        )
        market_state, gate = engine.evaluate_market_state_and_gate_from_series(
            date=snapshot.date,
            index_series={
                symbol: _through_date(history[symbol], snapshot.date)
                for symbol in ("SPX", "NDX", "SOX")
            },
            existing_positions_count=len(account_after.positions),
        )

        close_history = {
            symbol: [
                float(bar.close)
                for bar in _through_date(history[symbol], snapshot.date).values()
            ]
            for symbol in snapshot.universe
        }
        signals = UptrendSignalAdapter.build(
            date=snapshot.date,
            symbols=tuple(snapshot.universe),
            prices_by_symbol=close_history,
            ls60_exit_mode=LS60_EXIT_MODE,
        )
        ranked_symbols = sorted(
            signals.leader_rank_all,
            key=signals.leader_rank_all.__getitem__,
        )
        reference_top3 = [
            {
                "rank": index + 1,
                "symbol": symbol,
                "score": signals.day_signals.get(symbol, {}).get("leader_score"),
                "regime": regime_record.spx_regime,
            }
            for index, symbol in enumerate(ranked_symbols[:3])
        ] if route.branch == "UPTREND" else []

        management = CanonicalRuntime._management_orders(
            date=snapshot.date,
            branch=route.branch,
            account=account_after,
            day_signals=signals.day_signals,
            market_entry_allowed=gate.market_entry_allowed,
            trading_dates=list(_through_date(history["SPX"], snapshot.date)),
        )
        orders = list(management)
        candidate_count = 0
        selected_symbols: list[str] = []

        if route.branch == "UPTREND":
            buy_result = UptrendDecisionConsumer.consume(
                inputs=signals.to_consumer_inputs(
                    market_gate_decision=gate,
                    metadata={
                        "source": "E1RCoreEngine.step/canonical_runtime",
                        "strategy_logic_reimplemented": False,
                    },
                ),
                account_state=account_after,
                max_positions=engine.config.max_positions,
            )
            candidate_count = buy_result.decision.candidate_count
            selected_symbols = list(buy_result.metadata["selected_symbols"])
            orders.extend(buy_result.order_intents)
        elif route.branch == "SIDEWAYS_MA_CONFLICT":
            stocks = {
                symbol: _sideways_asset(symbol, history[symbol], snapshot.date)
                for symbol in snapshot.universe
            }
            ranked = SidewaysCore().rank_date(
                stocks=stocks,
                spx=_sideways_asset("SPX", history["SPX"], snapshot.date),
                date=snapshot.date,
                regime="SIDEWAYS",
                subclass="MA_CONFLICT",
            )
            reference_top3 = [
                {
                    "rank": index + 1,
                    "symbol": row.symbol,
                    "score": row.score,
                    "regime": "SIDEWAYS",
                }
                for index, row in enumerate(ranked[:3])
            ]
            sideways_orders = SidewaysExecutionPolicy().build_intents(
                date=snapshot.date,
                regime="SIDEWAYS",
                subclass="MA_CONFLICT",
                ranked_candidates=ranked,
                account=account_after,
                management_actions={
                    symbol: signal.get("action", "HOLD")
                    for symbol, signal in signals.day_signals.items()
                },
            )
            # The SIDEWAYS policy owns its positions; avoid duplicate management.
            sideways_symbols = {order.symbol for order in sideways_orders}
            orders = [order for order in orders if order.symbol not in sideways_symbols]
            orders.extend(sideways_orders)
            candidate_count = len(ranked)
            selected_symbols = [
                order.symbol for order in sideways_orders if order.intent_type == "BUY"
            ]
        else:
            forced = SidewaysExecutionPolicy().build_intents(
                date=snapshot.date,
                regime=regime_record.spx_regime,
                subclass=regime_record.subclass,
                ranked_candidates=(),
                account=account_after,
            )
            forced_symbols = {order.symbol for order in forced}
            orders = [order for order in orders if order.symbol not in forced_symbols]
            orders.extend(forced)

        if not orders:
            orders = [
                OrderIntent(
                    date=snapshot.date,
                    symbol="",
                    intent_type="NOOP",
                    side=None,
                    target_quantity=None,
                    quantity_delta=None,
                    reason="canonical_engine_no_action",
                    branch=route.branch,
                    metadata={"engine_owned_decision": True},
                )
            ]

        trace = DecisionTrace(
            date=snapshot.date,
            branch=route.branch,
            market_regime=regime_record.spx_regime,
            regime_subclass=regime_record.subclass,
            inputs={
                "market_state": market_state.market_state,
                "gate_state": gate.gate_state,
                "market_entry_allowed": gate.market_entry_allowed,
                "entry_capacity": gate.entry_capacity,
                "canonical_engine_entry": True,
                "external_regime_injected": False,
                "external_strategy_inputs": False,
            },
            candidate_count=candidate_count,
            selected_symbols=selected_symbols,
            order_intents=orders,
            reasons=[
                "canonical_regime_generator",
                "engine_market_state_and_gate",
                "engine_router_and_strategy",
                route.reason,
            ],
            metadata={
                "single_step_decision": True,
                "external_strategy_inputs": False,
                "external_regime_injected": False,
                "route": route.__dict__,
                "reference_top3": reference_top3,
                "ranking_source": (
                    "UptrendSignalAdapter.leader_rank_all"
                    if route.branch == "UPTREND"
                    else "SidewaysCore.rank_date"
                    if route.branch == "SIDEWAYS_MA_CONFLICT"
                    else "NONE"
                ),
                "max_positions": engine.config.max_positions,
                "min_holding_days": MIN_HOLDING_DAYS,
                "ls60_exit_mode": LS60_EXIT_MODE,
            },
        )
        result = DailyEngineResult(
            date=snapshot.date,
            account_before=account,
            account_after=account_after,
            decision_trace=trace,
            order_intents=orders,
            fills=[],
            metadata={
                "engine": "E1RCoreEngine",
                "formal_entry": True,
                "single_step_decision": True,
                "strategy_variant": VARIANT_ID,
            },
        )

        def atr_provider(symbol: str, as_of_date: str) -> float | None:
            rows = _through_date(history.get(symbol, {}), as_of_date)
            dates = list(rows)
            bars = [rows[item] for item in dates]
            return compute_entry_atr20(
                symbol=symbol,
                dates=dates,
                closes=[float(bar.close) for bar in bars],
                ohlc={
                    "high": [bar.high for bar in bars],
                    "low": [bar.low for bar in bars],
                },
                as_of_date=as_of_date,
            )

        return result, atr_provider

    @staticmethod
    def _hydrate_live_cycles(
        *,
        account: AccountState,
        history: Mapping[str, Mapping[str, DailyBar]],
        universe: list[str],
    ) -> AccountState:
        """Deterministically restore Engine state from the manual Live ledger."""
        if account.metadata.get("mode") != "LIVE":
            return account
        positions = dict(account.positions)
        changed = False
        for symbol, position in sorted(positions.items()):
            if POSITION_METADATA_KEY in position.metadata:
                continue
            dates = [item for item in sorted(history.get(symbol, {})) if item < position.entry_date]
            if not dates:
                raise RuntimeError(f"{symbol}: cannot reconstruct Live entry signal date")
            signal_date = dates[-1]
            rows = _through_date(history[symbol], signal_date)
            row_dates = list(rows)
            bars = [rows[item] for item in row_dates]
            atr20 = compute_entry_atr20(
                symbol=symbol,
                dates=row_dates,
                closes=[float(bar.close) for bar in bars],
                ohlc={
                    "high": [bar.high for bar in bars],
                    "low": [bar.low for bar in bars],
                },
                as_of_date=signal_date,
            )
            if atr20 is None:
                raise RuntimeError(f"{symbol}: cannot reconstruct Live entry ATR20")
            metadata = dict(position.metadata)
            metadata[POSITION_METADATA_KEY] = build_frozen_state(
                adjusted_first_buy_price=float(metadata["first_buy_price"]),
                entry_metadata=build_entry_metadata(
                    atr20=float(atr20),
                    atr_as_of=signal_date,
                ),
            ).to_dict()

            past_prices = {
                item: [
                    float(bar.close)
                    for bar in _through_date(history[item], signal_date).values()
                ]
                for item in universe
            }
            entry_signals = UptrendSignalAdapter.build(
                date=signal_date,
                symbols=tuple(universe),
                prices_by_symbol=past_prices,
                ls60_exit_mode=LS60_EXIT_MODE,
            )
            entry_type = entry_signals.day_signals.get(symbol, {}).get(
                "e1r_entry_type"
            )
            metadata["e1r_entry_type"] = entry_type or "UNKNOWN"
            metadata["size_units"] = (
                0.5 if entry_type == "E1R_UPTREND_EMERGING" else 1.0
            )
            metadata["entry_signal_date"] = signal_date
            metadata["live_cycle_reconstruction_required"] = False
            positions[symbol] = replace(position, metadata=metadata)
            changed = True
        return replace(account, positions=positions) if changed else account

    @staticmethod
    def _management_orders(
        *,
        date: str,
        branch: str,
        account: AccountState,
        day_signals: Mapping[str, Mapping[str, Any]],
        market_entry_allowed: bool,
        trading_dates: list[str],
    ) -> list[OrderIntent]:
        orders: list[OrderIntent] = []
        for symbol, position in sorted(account.positions.items()):
            signal = day_signals.get(symbol, {})
            action = str(signal.get("action", "HOLD")).upper()
            origin = str(position.metadata.get("origin_branch", "UPTREND"))
            if origin == "SIDEWAYS_MA_CONFLICT":
                continue
            if action == "BUY":
                action = "HOLD"
            if action == "ADD" and (
                not market_entry_allowed
                or float(position.metadata.get("size_units", 1.0)) >= 1.0
            ):
                action = "HOLD"
            if action in {"REDUCE", "EXIT"}:
                held_days = sum(
                    1
                    for row_date in trading_dates
                    if position.entry_date <= row_date <= date
                )
                if (
                    held_days < MIN_HOLDING_DAYS
                    and not is_broken_trend(str(signal.get("trend_state", "")))
                ):
                    action = "HOLD"

            entry_type = str(position.metadata.get("e1r_entry_type", ""))
            size_units = float(position.metadata.get("size_units", 1.0))
            if (
                action == "HOLD"
                and branch == "UPTREND"
                and entry_type == "E1R_UPTREND_EMERGING"
                and size_units < 1.0
                and signal.get("e1r_uptrend_confirmed_eligible")
                and position.avg_cost > 0
                and position.last_price / position.avg_cost - 1.0 > 0.03
                and position.last_price > float(signal.get("ma20", position.last_price))
                and float(signal.get("momentum_acceleration", 0.0)) >= 0.0
                and market_entry_allowed
            ):
                action = "ADD"

            side = "BUY" if action == "ADD" else "SELL" if action in {"REDUCE", "EXIT"} else None
            orders.append(
                OrderIntent(
                    date=date,
                    symbol=symbol,
                    intent_type=action,
                    side=side,
                    target_quantity=(0.0 if action == "EXIT" else position.quantity if action == "HOLD" else None),
                    quantity_delta=(-position.quantity * 0.5 if action == "REDUCE" else 0.0 if action == "HOLD" else None),
                    reason=(
                        "emerging_upgraded_to_confirmed"
                        if action == "ADD" and entry_type == "E1R_UPTREND_EMERGING"
                        else "canonical_position_" + action.lower()
                    ),
                    branch=branch,
                    metadata={
                        "origin_branch": origin,
                        "leader_score": signal.get("leader_score"),
                        "add_size_units": 0.5,
                        "reduce_fraction": 0.5,
                        "engine_owned_position_management": True,
                    },
                )
            )
        return orders


__all__ = ["CanonicalRuntime", "LS60_EXIT_MODE", "MIN_HOLDING_DAYS"]
