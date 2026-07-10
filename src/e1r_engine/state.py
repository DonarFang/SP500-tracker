from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


OrderSide = Literal["BUY", "SELL"]
OrderIntentType = Literal["BUY", "ADD", "REDUCE", "EXIT", "HOLD", "NOOP"]
FillStatus = Literal["FILLED", "PARTIAL", "REJECTED", "SKIPPED"]
EngineBranch = Literal[
    "UPTREND",
    "SIDEWAYS_MA_CONFLICT",
    "DETERIORATION_TRANSITION",
    "RECOVERY_TRANSITION",
    "DOWNTREND",
    "CASH_DEFENSIVE",
    "UNKNOWN",
]


@dataclass(frozen=True)
class PositionState:
    symbol: str
    quantity: float
    avg_cost: float
    last_price: float
    market_value: float
    unrealized_pnl: float
    entry_date: str
    last_update_date: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def create(symbol: str, quantity: float, avg_cost: float, price: float, date: str) -> "PositionState":
        market_value = quantity * price
        unrealized_pnl = (price - avg_cost) * quantity
        return PositionState(
            symbol=symbol,
            quantity=float(quantity),
            avg_cost=float(avg_cost),
            last_price=float(price),
            market_value=float(market_value),
            unrealized_pnl=float(unrealized_pnl),
            entry_date=date,
            last_update_date=date,
        )

    def mark_to_market(self, price: float, date: str) -> "PositionState":
        market_value = self.quantity * float(price)
        unrealized_pnl = (float(price) - self.avg_cost) * self.quantity
        return PositionState(
            symbol=self.symbol,
            quantity=self.quantity,
            avg_cost=self.avg_cost,
            last_price=float(price),
            market_value=float(market_value),
            unrealized_pnl=float(unrealized_pnl),
            entry_date=self.entry_date,
            last_update_date=date,
            metadata=dict(self.metadata),
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.symbol:
            errors.append("missing_symbol")
        if self.quantity < 0:
            errors.append(f"{self.symbol}:negative_quantity")
        if self.avg_cost < 0:
            errors.append(f"{self.symbol}:negative_avg_cost")
        if self.last_price < 0:
            errors.append(f"{self.symbol}:negative_last_price")
        return errors


@dataclass(frozen=True)
class AccountState:
    date: str
    cash: float
    positions: dict[str, PositionState]
    total_equity: float
    positions_value: float
    open_positions_count: int
    metadata: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def empty(date: str, initial_cash: float = 100000.0) -> "AccountState":
        return AccountState(
            date=date,
            cash=float(initial_cash),
            positions={},
            total_equity=float(initial_cash),
            positions_value=0.0,
            open_positions_count=0,
            metadata={"initial_cash": float(initial_cash)},
        )

    def mark_to_market(self, prices: dict[str, float], date: str) -> "AccountState":
        new_positions: dict[str, PositionState] = {}

        for symbol, position in self.positions.items():
            price = prices.get(symbol, position.last_price)
            new_positions[symbol] = position.mark_to_market(price=price, date=date)

        positions_value = sum(p.market_value for p in new_positions.values())
        total_equity = self.cash + positions_value

        return AccountState(
            date=date,
            cash=float(self.cash),
            positions=new_positions,
            total_equity=float(total_equity),
            positions_value=float(positions_value),
            open_positions_count=len(new_positions),
            metadata=dict(self.metadata),
        )

    def validate(self, max_positions: int = 3) -> dict[str, Any]:
        errors: list[str] = []

        if self.cash < 0:
            errors.append("negative_cash")
        if self.open_positions_count != len(self.positions):
            errors.append("open_positions_count_mismatch")
        if self.open_positions_count > max_positions:
            errors.append("open_positions_count_exceeds_max")
        if abs((self.cash + self.positions_value) - self.total_equity) > 1e-6:
            errors.append("equity_identity_mismatch")

        for position in self.positions.values():
            errors.extend(position.validate())

        return {
            "ok": len(errors) == 0,
            "errors": errors,
            "error_count": len(errors),
            "date": self.date,
            "cash": self.cash,
            "positions_value": self.positions_value,
            "total_equity": self.total_equity,
            "open_positions_count": self.open_positions_count,
            "max_positions": max_positions,
        }


@dataclass(frozen=True)
class OrderIntent:
    date: str
    symbol: str
    intent_type: OrderIntentType
    side: OrderSide | None
    target_quantity: float | None
    quantity_delta: float | None
    reason: str
    branch: EngineBranch
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.date:
            errors.append("missing_date")
        if self.intent_type not in {"HOLD", "NOOP"} and not self.symbol:
            errors.append("missing_symbol")
        if self.intent_type in {"BUY", "ADD", "REDUCE", "EXIT"} and self.side is None:
            errors.append(f"{self.intent_type}:missing_side")
        if self.target_quantity is not None and self.target_quantity < 0:
            errors.append("negative_target_quantity")
        return errors


@dataclass(frozen=True)
class Fill:
    date: str
    symbol: str
    side: OrderSide
    quantity: float
    price: float
    gross_amount: float
    status: FillStatus
    reason: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_order(date: str, symbol: str, side: OrderSide, quantity: float, price: float, status: FillStatus, reason: str) -> "Fill":
        return Fill(
            date=date,
            symbol=symbol,
            side=side,
            quantity=float(quantity),
            price=float(price),
            gross_amount=float(quantity) * float(price),
            status=status,
            reason=reason,
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.date:
            errors.append("missing_date")
        if not self.symbol:
            errors.append("missing_symbol")
        if self.quantity < 0:
            errors.append("negative_quantity")
        if self.price < 0:
            errors.append("negative_price")
        if abs(self.quantity * self.price - self.gross_amount) > 1e-6:
            errors.append("gross_amount_mismatch")
        return errors


@dataclass(frozen=True)
class DecisionTrace:
    date: str
    branch: EngineBranch
    market_regime: str | None
    regime_subclass: str | None
    inputs: dict[str, Any]
    candidate_count: int
    selected_symbols: list[str]
    order_intents: list[OrderIntent]
    reasons: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.date:
            errors.append("missing_date")
        if self.candidate_count < 0:
            errors.append("negative_candidate_count")
        for order in self.order_intents:
            errors.extend(order.validate())
        return errors


@dataclass(frozen=True)
class DailyEngineResult:
    date: str
    account_before: AccountState
    account_after: AccountState
    decision_trace: DecisionTrace
    order_intents: list[OrderIntent]
    fills: list[Fill]
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self, max_positions: int = 3) -> dict[str, Any]:
        errors: list[str] = []

        before = self.account_before.validate(max_positions=max_positions)
        after = self.account_after.validate(max_positions=max_positions)

        if not before["ok"]:
            errors.extend([f"account_before:{e}" for e in before["errors"]])
        if not after["ok"]:
            errors.extend([f"account_after:{e}" for e in after["errors"]])

        errors.extend(self.decision_trace.validate())

        for order in self.order_intents:
            errors.extend(order.validate())

        for fill in self.fills:
            errors.extend(fill.validate())

        if self.account_after.open_positions_count > max_positions:
            errors.append("max_positions_contract_violation")

        return {
            "ok": len(errors) == 0,
            "errors": errors,
            "error_count": len(errors),
            "date": self.date,
            "max_positions": max_positions,
            "account_before": before,
            "account_after": after,
            "order_count": len(self.order_intents),
            "fill_count": len(self.fills),
        }


def apply_fills_contract_only(account: AccountState, fills: list[Fill], date: str) -> AccountState:
    """
    Contract-only fill application used for state smoke tests.

    This is NOT strategy logic:
    - It does not decide orders.
    - It does not size positions.
    - It does not evaluate market gates or regimes.
    - It only verifies that AccountState / Fill accounting identity is coherent.
    """
    cash = account.cash
    positions = dict(account.positions)

    for fill in fills:
        if fill.status != "FILLED":
            continue

        if fill.side == "BUY":
            cash -= fill.gross_amount
            old = positions.get(fill.symbol)
            if old is None:
                positions[fill.symbol] = PositionState.create(
                    symbol=fill.symbol,
                    quantity=fill.quantity,
                    avg_cost=fill.price,
                    price=fill.price,
                    date=date,
                )
            else:
                new_qty = old.quantity + fill.quantity
                new_avg = ((old.quantity * old.avg_cost) + fill.gross_amount) / new_qty if new_qty else 0.0
                positions[fill.symbol] = PositionState.create(
                    symbol=fill.symbol,
                    quantity=new_qty,
                    avg_cost=new_avg,
                    price=fill.price,
                    date=old.entry_date,
                ).mark_to_market(fill.price, date)

        elif fill.side == "SELL":
            cash += fill.gross_amount
            old = positions.get(fill.symbol)
            if old is None:
                continue
            new_qty = max(0.0, old.quantity - fill.quantity)
            if new_qty <= 1e-12:
                positions.pop(fill.symbol, None)
            else:
                positions[fill.symbol] = PositionState.create(
                    symbol=fill.symbol,
                    quantity=new_qty,
                    avg_cost=old.avg_cost,
                    price=fill.price,
                    date=old.entry_date,
                ).mark_to_market(fill.price, date)

    positions_value = sum(p.market_value for p in positions.values())

    return AccountState(
        date=date,
        cash=float(cash),
        positions=positions,
        positions_value=float(positions_value),
        total_equity=float(cash + positions_value),
        open_positions_count=len(positions),
        metadata=dict(account.metadata),
    )
