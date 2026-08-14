"""Convert actual Live account facts to the shared Engine AccountState."""

from __future__ import annotations

from e1r_engine.live_account import LiveAccountState
from dataclasses import replace

from e1r_engine.capped_atr_stop import VARIANT_ID
from e1r_engine.state import AccountState, PositionState


class LiveAccountAdapterError(ValueError):
    pass


class LiveAccountAdapter:
    """Use actual_cash as the authoritative Engine cash input."""

    def to_engine_account(
        self,
        *,
        live_account: LiveAccountState,
        market_date: str,
    ) -> AccountState:
        engine_positions = {}

        for symbol, position in sorted(live_account.positions.items()):
            mark = getattr(position, "market_price", None)
            if mark is None:
                mark = getattr(position, "last_price", None)
            if mark is None:
                mark = position.average_cost

            transactions = [
                item
                for item in live_account.applied_transactions
                if item.symbol == symbol
            ]
            last_exit = max(
                (
                    index
                    for index, item in enumerate(transactions)
                    if item.action == "EXIT"
                ),
                default=-1,
            )
            cycle = transactions[last_exit + 1 :]
            first_buy = next(
                (item for item in cycle if item.action == "BUY"),
                None,
            )
            entry_date = (
                first_buy.trade_date.isoformat()
                if first_buy is not None
                else market_date
            )
            base = PositionState.create(
                symbol=symbol,
                quantity=float(position.shares),
                avg_cost=float(position.average_cost),
                price=float(mark),
                date=entry_date,
            ).mark_to_market(
                price=float(mark),
                date=market_date,
            )
            engine_positions[symbol] = replace(
                base,
                metadata={
                    "live_cycle_reconstruction_required": True,
                    "first_buy_price": (
                        float(first_buy.price)
                        if first_buy is not None
                        else float(position.average_cost)
                    ),
                    "origin_branch": "UPTREND",
                },
            )

        positions_value = sum(
            position.market_value
            for position in engine_positions.values()
        )
        cash = float(live_account.actual_cash)

        account = AccountState(
            date=market_date,
            cash=cash,
            positions=engine_positions,
            positions_value=float(positions_value),
            total_equity=float(cash + positions_value),
            open_positions_count=len(engine_positions),
            metadata={
                "mode": "LIVE",
                "source": "LiveAccountAdapter",
                "cash_authority": "actual_cash",
                "calculated_cash": str(
                    live_account.calculated_cash
                ),
                "cash_difference": str(
                    live_account.cash_difference
                ),
                "strategy_variant": VARIANT_ID,
            },
        )

        validation = account.validate(max_positions=3)
        if not isinstance(validation, dict):
            raise LiveAccountAdapterError(
                "AccountState.validate must return a report dict"
            )
        if not validation.get("ok", False):
            errors = validation.get("errors", [])
            raise LiveAccountAdapterError(
                "invalid Engine AccountState: "
                + "; ".join(str(item) for item in errors)
            )
        return account
