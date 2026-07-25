"""Convert actual Live account facts to the shared Engine AccountState."""

from __future__ import annotations

from e1r_engine.live_account import LiveAccountState
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

            engine_positions[symbol] = PositionState.create(
                symbol=symbol,
                quantity=float(position.shares),
                avg_cost=float(position.average_cost),
                price=float(mark),
                date=market_date,
            ).mark_to_market(
                price=float(mark),
                date=market_date,
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
