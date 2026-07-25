"""Deterministic Live-only daily processing core."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
from decimal import Decimal
import hashlib
import json
from typing import Mapping, Sequence

from .live_account import (
    LiveAccountState,
    LiveOpeningState,
    rebuild_live_account,
)
from .live_data import LiveMarketData
from .live_ledger import LiveLedger
from .live_recommendation import LiveEngineDecision, LiveEnginePort
from .live_repository import LiveDailyRepository


class LiveDailyError(ValueError):
    pass


def _canonical_hash(payload: Mapping[str, object]) -> str:
    raw = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class LiveDailyResult:
    market_date: date
    decision: LiveEngineDecision
    account: LiveAccountState
    input_hash: str
    result_hash: str

    def to_payload(self) -> dict[str, object]:
        return {
            "market_date": self.market_date.isoformat(),
            "regime": self.decision.regime,
            "regime_subclass": self.decision.regime_subclass,
            "market_state": self.decision.market_state,
            "market_gate": self.decision.market_gate,
            "entry_capacity": self.decision.entry_capacity,
            "strategy_branch": self.decision.strategy_branch,
            "reference_top3": [
                {"rank": item.rank, "symbol": item.symbol}
                for item in self.decision.reference_candidates
            ],
            "position_recommendations": [
                {
                    "symbol": item.symbol,
                    "action": item.action,
                    "reason": item.reason,
                    "target_shares": item.target_shares,
                }
                for item in self.decision.position_recommendations
            ],
            "account": {
                "actual_cash": self.account.actual_cash,
                "calculated_cash": self.account.calculated_cash,
                "cash_difference": self.account.cash_difference,
                "realized_pnl": self.account.realized_pnl,
                "unrealized_pnl": self.account.unrealized_pnl,
                "trading_pnl": self.account.trading_pnl,
                "positions_value": self.account.positions_value,
                "total_equity": self.account.total_equity,
                "positions": {
                    symbol: {
                        "shares": position.shares,
                        "average_cost": position.average_cost,
                        "cost_basis": position.cost_basis,
                    }
                    for symbol, position in sorted(
                        self.account.positions.items()
                    )
                },
            },
            "engine_id": self.decision.engine_id,
            "engine_version": self.decision.engine_version,
            "evidence": dict(self.decision.evidence),
            "input_hash": self.input_hash,
            "result_hash": self.result_hash,
        }


class LiveDailyProcessor:
    def __init__(
        self,
        *,
        engine: LiveEnginePort,
        repository: LiveDailyRepository | None = None,
    ) -> None:
        self.engine = engine
        self.repository = repository

    def process(
        self,
        *,
        market_date: date,
        market_data: LiveMarketData,
        opening: LiveOpeningState,
        ledger: LiveLedger,
    ) -> LiveDailyResult:
        if market_data.market_date != market_date:
            raise LiveDailyError("market data date mismatch")

        account_symbols = []
        preliminary = rebuild_live_account(
            opening=opening,
            ledger=ledger,
        )
        account_symbols = sorted(preliminary.positions)
        market_data.require_symbols(account_symbols)

        account = rebuild_live_account(
            opening=opening,
            ledger=ledger,
            marks=market_data.close_marks,
        )

        immutable_before = {
            symbol: (
                position.shares,
                position.average_cost,
            )
            for symbol, position in preliminary.positions.items()
        }
        immutable_after = {
            symbol: (
                position.shares,
                position.average_cost,
            )
            for symbol, position in account.positions.items()
        }

        if immutable_before != immutable_after:
            raise LiveDailyError(
                "mark-to-market changed shares or average cost"
            )
        if preliminary.actual_cash != account.actual_cash:
            raise LiveDailyError("mark-to-market changed actual_cash")
        if preliminary.calculated_cash != account.calculated_cash:
            raise LiveDailyError("mark-to-market changed calculated_cash")

        input_payload = {
            "market_date": market_date.isoformat(),
            "bars": {
                symbol: {
                    "open": bar.open,
                    "high": bar.high,
                    "low": bar.low,
                    "close": bar.close,
                    "volume": bar.volume,
                }
                for symbol, bar in sorted(market_data.bars.items())
            },
            "account": {
                "actual_cash": account.actual_cash,
                "calculated_cash": account.calculated_cash,
                "cash_difference": account.cash_difference,
                "positions": {
                    symbol: {
                        "shares": position.shares,
                        "average_cost": position.average_cost,
                    }
                    for symbol, position in sorted(
                        account.positions.items()
                    )
                },
            },
        }
        input_hash = _canonical_hash(input_payload)

        decision = self.engine.decide(
            market_date=market_date,
            market_data=market_data,
            account=account,
        )
        if decision.market_date != market_date:
            raise LiveDailyError("Engine decision date mismatch")

        result_seed = {
            **input_payload,
            "engine_decision": {
                "regime": decision.regime,
                "regime_subclass": decision.regime_subclass,
                "market_state": decision.market_state,
                "market_gate": decision.market_gate,
                "entry_capacity": decision.entry_capacity,
                "strategy_branch": decision.strategy_branch,
                "reference_top3": [
                    (item.rank, item.symbol)
                    for item in decision.reference_candidates
                ],
                "recommendations": [
                    (
                        item.symbol,
                        item.action,
                        item.reason,
                        item.target_shares,
                    )
                    for item in decision.position_recommendations
                ],
                "engine_id": decision.engine_id,
                "engine_version": decision.engine_version,
            },
        }
        result_hash = _canonical_hash(result_seed)

        result = LiveDailyResult(
            market_date=market_date,
            decision=decision,
            account=account,
            input_hash=input_hash,
            result_hash=result_hash,
        )

        if self.repository is not None:
            payload = result.to_payload()
            self.repository.commit(
                market_date=market_date.isoformat(),
                payload=payload,
            )
            self.repository.append_equity_point(
                market_date=market_date.isoformat(),
                payload={
                    "actual_cash": account.actual_cash,
                    "positions_value": account.positions_value,
                    "total_equity": account.total_equity,
                    "trading_pnl": account.trading_pnl,
                    "cash_difference": account.cash_difference,
                    "result_hash": result_hash,
                },
            )

        return result
