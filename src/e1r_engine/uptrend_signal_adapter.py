from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from engine.leader_ranking import leader_score
from engine.trade_decision import trade_action
from features.momentum import (
    linreg_slope,
    momentum_acceleration,
    momentum_score,
    moving_average,
)
from features.rs import period_return, rs_percentile
from features.trend_health import (
    trend_health_score,
    trend_lifecycle,
)

from e1r_engine.market_gate import MarketGateDecision
from e1r_engine.uptrend_consumer import UptrendConsumerInputs


@dataclass(frozen=True)
class UptrendSignalAdapterResult:
    date: str
    day_signals: dict[str, dict[str, Any]]
    leader_rank_all: dict[str, int]
    symbol_order: tuple[str, ...]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_consumer_inputs(
        self,
        *,
        market_gate_decision: MarketGateDecision,
        metadata: dict[str, Any] | None = None,
    ) -> UptrendConsumerInputs:
        if market_gate_decision.date != self.date:
            raise ValueError(
                "market gate date does not match adapter result date"
            )

        return UptrendConsumerInputs(
            date=self.date,
            day_signals={
                symbol: dict(signal)
                for symbol, signal in self.day_signals.items()
            },
            leader_rank_all=dict(self.leader_rank_all),
            market_gate_decision=market_gate_decision,
            metadata=dict(metadata or {}),
        )


class UptrendSignalAdapter:
    @staticmethod
    def build(
        *,
        date: str,
        symbols: Sequence[str],
        prices_by_symbol: Mapping[str, Sequence[float]],
        market_score_default: float = 60.0,
        ls60_exit_mode: str = "reduce",
    ) -> UptrendSignalAdapterResult:
        if not date:
            raise ValueError("date must be non-empty")

        symbol_order = tuple(symbols)

        if len(set(symbol_order)) != len(symbol_order):
            raise ValueError("symbols must not contain duplicates")

        prices_copy: dict[str, list[float]] = {}

        for symbol in symbol_order:
            if symbol not in prices_by_symbol:
                raise ValueError(
                    f"missing price history for symbol: {symbol}"
                )

            prices_copy[symbol] = list(
                prices_by_symbol[symbol]
            )

        all_ret60: list[float] = []
        all_ret60_prev20: list[float] = []

        for symbol in symbol_order:
            prices = prices_copy[symbol]

            if len(prices) > 60:
                current_return = period_return(prices, 60)

                if current_return is not None:
                    all_ret60.append(current_return)

            if len(prices) > 80:
                previous_return = period_return(
                    prices[:-20],
                    60,
                )

                if previous_return is not None:
                    all_ret60_prev20.append(
                        previous_return
                    )

        day_signals: dict[str, dict[str, Any]] = {}

        for symbol in symbol_order:
            prices = prices_copy[symbol]

            if len(prices) < 60:
                continue

            close_t = prices[-1]
            ret60 = period_return(prices, 60) or 0.0
            rs = rs_percentile(ret60, all_ret60)

            momentum_data = momentum_score(prices)
            momentum = momentum_data["momentum_score"]

            trend_health_data = trend_health_score(prices)
            trend_health = trend_health_data["trend_health"]

            score = leader_score(
                rs,
                momentum,
                trend_health,
            )

            state = trend_lifecycle(
                trend_health,
                momentum,
                rs,
            )

            ma20_series = moving_average(prices, 20)
            ma20_value = (
                ma20_series[-1]
                if ma20_series
                else close_t
            )
            ma20_slope = (
                linreg_slope(ma20_series[-10:])
                if len(ma20_series) >= 10
                else 0
            )

            ma50_series = moving_average(prices, 50)
            ma50_value = (
                ma50_series[-1]
                if ma50_series
                else close_t
            )
            ma50_slope = (
                linreg_slope(ma50_series[-10:])
                if len(ma50_series) >= 10
                else 0
            )

            rs_prev20 = 50.0
            rs_20d_improvement = 0.0

            if (
                len(prices) > 80
                and all_ret60_prev20
            ):
                ret60_prev20 = period_return(
                    prices[:-20],
                    60,
                )
                rs_prev20 = rs_percentile(
                    ret60_prev20,
                    all_ret60_prev20,
                )
                rs_20d_improvement = round(
                    rs - rs_prev20,
                    2,
                )

            momentum_acc = momentum_acceleration(
                prices
            )

            action = trade_action(
                state,
                momentum,
                rs,
                close_t,
                ma50_value,
                ma50_slope,
                score,
                trend_health,
                market_score_default,
                ls60_exit_mode=ls60_exit_mode,
            )

            day_signals[symbol] = {
                "symbol": symbol,
                "action": action,
                "trend_state": state,
                "momentum_score": momentum,
                "rs_score": rs,
                "leader_score": score,
                "trend_health": trend_health,
                "close_t": close_t,
                "ma20": ma20_value,
                "ma20_slope": ma20_slope,
                "ma50": ma50_value,
                "ma50_slope": ma50_slope,
                "rs_prev20": rs_prev20,
                "rs_20d_improvement": (
                    rs_20d_improvement
                ),
                "momentum_acceleration": momentum_acc,
                "e1r_entry_type": None,
                "e1r_uptrend_emerging_eligible": False,
                "e1r_uptrend_confirmed_eligible": False,
                "e1r_entry_reason": [],
            }

        tagged_signals, leader_rank_all = (
            UptrendSignalAdapter.tag_uptrend_candidates(
                day_signals=day_signals,
                symbol_order=symbol_order,
            )
        )

        return UptrendSignalAdapterResult(
            date=date,
            day_signals=tagged_signals,
            leader_rank_all=leader_rank_all,
            symbol_order=symbol_order,
            metadata={
                "adapter": "UptrendSignalAdapter",
                "strategy_source": (
                    "legacy_backtest_signal_production"
                ),
                "symbol_count": len(symbol_order),
                "signal_count": len(tagged_signals),
                "all_ret60_count": len(all_ret60),
                "all_ret60_prev20_count": (
                    len(all_ret60_prev20)
                ),
                "market_score_default": (
                    market_score_default
                ),
                "ls60_exit_mode": ls60_exit_mode,
                "e1r_shell_mode_equivalent": True,
                "market_gate_recomputed": False,
                "candidate_selection_performed": False,
                "buy_selection_performed": False,
            },
        )

    @staticmethod
    def tag_uptrend_candidates(
        *,
        day_signals: Mapping[
            str,
            Mapping[str, Any],
        ],
        symbol_order: Sequence[str],
    ) -> tuple[
        dict[str, dict[str, Any]],
        dict[str, int],
    ]:
        ordered_symbols = tuple(symbol_order)

        if len(set(ordered_symbols)) != len(
            ordered_symbols
        ):
            raise ValueError(
                "symbol_order must not contain duplicates"
            )

        missing = [
            symbol
            for symbol in day_signals
            if symbol not in set(ordered_symbols)
        ]

        if missing:
            raise ValueError(
                "day_signals contains symbols absent from "
                f"symbol_order: {missing}"
            )

        tagged = {
            symbol: {
                **dict(day_signals[symbol]),
                "e1r_entry_reason": list(
                    day_signals[symbol].get(
                        "e1r_entry_reason",
                        [],
                    )
                ),
            }
            for symbol in ordered_symbols
            if symbol in day_signals
        }

        top_ranked = sorted(
            (
                (
                    symbol,
                    signal["leader_score"],
                )
                for symbol, signal in tagged.items()
            ),
            key=lambda row: row[1],
            reverse=True,
        )

        leader_rank_all = {
            symbol: index + 1
            for index, (symbol, _) in enumerate(
                top_ranked
            )
        }

        for symbol, signal in tagged.items():
            rank_all = leader_rank_all.get(
                symbol,
                9999,
            )

            emerging_reasons: list[str] = []

            if signal["rs_score"] >= 80:
                emerging_reasons.append("rs_above_80")
            if (
                signal.get(
                    "rs_20d_improvement",
                    0,
                )
                >= 10
            ):
                emerging_reasons.append(
                    "rs_20d_improvement_above_10"
                )
            if signal["momentum_score"] >= 70:
                emerging_reasons.append(
                    "momentum_above_70"
                )
            if (
                signal.get(
                    "momentum_acceleration",
                    0,
                )
                > 0
            ):
                emerging_reasons.append(
                    "momentum_acceleration_positive"
                )
            if signal["trend_health"] >= 65:
                emerging_reasons.append(
                    "trend_health_above_65"
                )
            if signal["close_t"] > signal.get(
                "ma20",
                signal["close_t"],
            ):
                emerging_reasons.append(
                    "close_above_ma20"
                )
            if (
                signal.get("ma20_slope", 0) > 0
                or signal.get("ma20", 0)
                > signal.get("ma50", 0)
            ):
                emerging_reasons.append(
                    "ma20_structure_positive"
                )
            if rank_all <= 20:
                emerging_reasons.append(
                    "leader_rank_top20"
                )

            emerging = (
                signal["rs_score"] >= 80
                and signal.get(
                    "rs_20d_improvement",
                    0,
                )
                >= 10
                and signal["momentum_score"] >= 70
                and signal.get(
                    "momentum_acceleration",
                    0,
                )
                > 0
                and signal["trend_health"] >= 65
                and signal["close_t"]
                > signal.get(
                    "ma20",
                    signal["close_t"],
                )
                and (
                    signal.get("ma20_slope", 0) > 0
                    or signal.get("ma20", 0)
                    > signal.get("ma50", 0)
                )
                and rank_all <= 20
            )

            confirmed_reasons: list[str] = []

            if signal["rs_score"] >= 90:
                confirmed_reasons.append(
                    "rs_above_90"
                )
            if rank_all <= 5:
                confirmed_reasons.append(
                    "leader_rank_top5"
                )
            if signal["leader_score"] >= 75:
                confirmed_reasons.append(
                    "leader_score_above_75"
                )
            if signal["momentum_score"] >= 75:
                confirmed_reasons.append(
                    "momentum_above_75"
                )
            if signal["trend_health"] >= 70:
                confirmed_reasons.append(
                    "trend_health_above_70"
                )
            if signal["close_t"] > signal.get(
                "ma50",
                signal["close_t"],
            ):
                confirmed_reasons.append(
                    "close_above_ma50"
                )
            if signal.get("ma50_slope", 0) >= 0:
                confirmed_reasons.append(
                    "ma50_slope_non_negative"
                )

            confirmed = (
                signal["rs_score"] >= 90
                and rank_all <= 5
                and signal["leader_score"] >= 75
                and signal["momentum_score"] >= 75
                and signal["trend_health"] >= 70
                and signal["close_t"]
                > signal.get(
                    "ma50",
                    signal["close_t"],
                )
                and signal.get("ma50_slope", 0) >= 0
            )

            if emerging or confirmed:
                entry_type = (
                    "E1R_UPTREND_CONFIRMED"
                    if confirmed
                    else "E1R_UPTREND_EMERGING"
                )
                reasons = (
                    confirmed_reasons
                    if confirmed
                    else emerging_reasons
                )

                signal["e1r_entry_type"] = entry_type
                signal[
                    "e1r_uptrend_emerging_eligible"
                ] = emerging
                signal[
                    "e1r_uptrend_confirmed_eligible"
                ] = confirmed
                signal["e1r_entry_reason"] = reasons

        return tagged, leader_rank_all


__all__ = [
    "UptrendSignalAdapter",
    "UptrendSignalAdapterResult",
]
