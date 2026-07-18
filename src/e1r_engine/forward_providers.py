from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from e1r_engine.contracts import DailyBar
from e1r_engine.forward_runtime import ForwardContractError
from e1r_engine.market_gate import (
    MarketGateConfig,
    MarketGateDecision,
    MarketGateEvaluator,
    MarketGateInputs,
)
from e1r_engine.state import AccountState
from e1r_engine.uptrend_signal_adapter import (
    UptrendSignalAdapter,
)


SeriesBySymbol = Mapping[
    str,
    Mapping[str, DailyBar],
]


@dataclass(frozen=True)
class MarketStateRecord:
    """
    Explicit upstream Market State input.

    Step 2 wires this contract only. Step 3 is responsible for
    supplying real daily records and validating their source.
    """

    date: str
    market_state: str
    entry_capacity: int
    spx_close: float | None = None
    spx_ma50: float | None = None
    spx_day_return: float | None = None
    source: str = "upstream_explicit_market_state"

    def validate(self) -> None:
        if not self.date:
            raise ForwardContractError(
                "MarketStateRecord requires date"
            )

        if self.market_state not in {
            "FULL_ON",
            "CAUTIOUS_ON",
            "CASH_MODE",
            "UNKNOWN",
        }:
            raise ForwardContractError(
                "unsupported market_state: "
                f"{self.market_state!r}"
            )

        if self.entry_capacity < 0:
            raise ForwardContractError(
                "entry_capacity must be >= 0"
            )

        if self.entry_capacity > 3:
            raise ForwardContractError(
                "entry_capacity exceeds max-3"
            )


@dataclass(frozen=True)
class ExplicitMarketStateProvider:
    """
    Supplies source-equivalent upstream values without recomputing
    Market State policy inside Forward.
    """

    records_by_date: Mapping[
        str,
        MarketStateRecord,
    ]

    def __call__(
        self,
        *,
        date: str,
    ) -> MarketStateRecord:
        record = self.records_by_date.get(date)

        if record is None:
            raise ForwardContractError(
                f"{date}: missing explicit MarketStateRecord"
            )

        record.validate()

        if record.date != date:
            raise ForwardContractError(
                f"{date}: MarketStateRecord date mismatch"
            )

        return record


@dataclass(frozen=True)
class FormalMarketGateProvider:
    """
    Thin adapter:
    ExplicitMarketStateProvider -> MarketGateEvaluator.

    No Market State formula is implemented here.
    """

    market_state_provider: ExplicitMarketStateProvider
    config: MarketGateConfig = MarketGateConfig()

    def __call__(
        self,
        *,
        date: str,
        index_series: SeriesBySymbol,
    ) -> MarketGateDecision:
        record = self.market_state_provider(
            date=date
        )

        decision = MarketGateEvaluator.evaluate(
            self.config,
            MarketGateInputs(
                date=date,
                spx_close=record.spx_close,
                spx_ma50=record.spx_ma50,
                spx_day_return=(
                    record.spx_day_return
                ),
                market_state=record.market_state,
                entry_capacity=(
                    record.entry_capacity
                ),
                existing_positions_count=0,
            ),
        )

        if decision.date != date:
            raise ForwardContractError(
                "Market Gate returned wrong date"
            )

        if decision.entry_capacity > 3:
            raise ForwardContractError(
                "Market Gate exceeded max-3"
            )

        return decision


def _close_history(
    *,
    symbol: str,
    date: str,
    stock_series: SeriesBySymbol,
) -> list[float]:
    if symbol not in stock_series:
        raise ForwardContractError(
            f"{symbol}: missing price series"
        )

    dates = [
        row_date
        for row_date in sorted(
            stock_series[symbol]
        )
        if row_date <= date
    ]

    if not dates or dates[-1] != date:
        raise ForwardContractError(
            f"{symbol}: missing exact T bar for {date}"
        )

    closes: list[float] = []

    for row_date in dates:
        close = stock_series[
            symbol
        ][row_date].close

        if close is None:
            raise ForwardContractError(
                f"{symbol}: null close on {row_date}"
            )

        closes.append(float(close))

    return closes


@dataclass(frozen=True)
class FormalManagementActionProvider:
    """
    Reuses UptrendSignalAdapter, which already calls the formal
    trade_action function and exposes trade_action in day_signals.

    No HOLD/ADD/REDUCE/EXIT rule is implemented here.
    """

    market_score_default: float = 60.0
    ls60_exit_mode: str = "reduce"

    def __call__(
        self,
        *,
        date: str,
        account: AccountState,
        stock_series: SeriesBySymbol,
    ) -> Mapping[str, str]:
        held_symbols = tuple(
            sorted(account.positions)
        )

        if not held_symbols:
            return {}

        prices_by_symbol = {
            symbol: _close_history(
                symbol=symbol,
                date=date,
                stock_series=stock_series,
            )
            for symbol in held_symbols
        }

        result = UptrendSignalAdapter.build(
            date=date,
            symbols=held_symbols,
            prices_by_symbol=prices_by_symbol,
            market_score_default=(
                self.market_score_default
            ),
            ls60_exit_mode=(
                self.ls60_exit_mode
            ),
        )

        actions: dict[str, str] = {}

        for symbol in held_symbols:
            signal = result.day_signals.get(
                symbol
            )

            if signal is None:
                raise ForwardContractError(
                    f"{symbol}: no formal day signal"
                )

            action = signal.get(
                "trade_action"
            )

            if not isinstance(action, str):
                raise ForwardContractError(
                    f"{symbol}: missing trade_action"
                )

            normalized = action.upper()

            if normalized not in {
                "HOLD",
                "ADD",
                "REDUCE",
                "EXIT",
            }:
                raise ForwardContractError(
                    f"{symbol}: invalid trade_action "
                    f"{normalized!r}"
                )

            actions[symbol] = normalized

        return actions


__all__ = [
    "ExplicitMarketStateProvider",
    "FormalManagementActionProvider",
    "FormalMarketGateProvider",
    "MarketStateRecord",
]
