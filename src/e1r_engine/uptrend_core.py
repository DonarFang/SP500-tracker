from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class UptrendDailyAccountRow:
    date: str
    cash: float
    positions_value: float
    total_equity: float
    open_positions_count: int
    market_gate_state: str | None
    spx_regime: str | None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class UptrendTradeRow:
    symbol: str
    entry_date: str | None
    entry_price: float | None
    exit_date: str | None
    exit_price: float | None
    entry_signal: str | None
    exit_signal: str | None
    entry_regime: str | None
    exit_regime: str | None
    return_pct: float | None
    holding_days: int | float | None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class UptrendCoreResult:
    source: str
    window: dict[str, Any]
    daily_account: list[UptrendDailyAccountRow]
    trades: list[UptrendTradeRow]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_comparable_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "window": self.window,
            "daily_account": [
                {
                    "date": r.date,
                    "cash": r.cash,
                    "positions_value": r.positions_value,
                    "total_equity": r.total_equity,
                    "open_positions_count": r.open_positions_count,
                    "market_gate_state": r.market_gate_state,
                    "spx_regime": r.spx_regime,
                }
                for r in self.daily_account
            ],
            "trades": [
                {
                    "symbol": r.symbol,
                    "entry_date": r.entry_date,
                    "entry_price": r.entry_price,
                    "exit_date": r.exit_date,
                    "exit_price": r.exit_price,
                    "entry_signal": r.entry_signal,
                    "exit_signal": r.exit_signal,
                    "entry_regime": r.entry_regime,
                    "exit_regime": r.exit_regime,
                    "return_pct": r.return_pct,
                    "holding_days": r.holding_days,
                }
                for r in self.trades
            ],
            "metadata": self.metadata,
        }


class UptrendCore:
    """
    ENGINE-J UPTREND extraction skeleton.

    Current scope:
    - Define the stable comparable output shape for future extracted UPTREND logic.
    - Replay/normalize ENGINE-G golden-master output into the new comparable shape.
    - Enable equivalence checker development before moving legacy trading logic.

    This is NOT the final extracted strategy implementation:
    - It does not rank candidates.
    - It does not decide BUY/ADD/REDUCE/EXIT.
    - It does not size positions.
    - It does not apply market gate rules.
    - It does not call run_stateful_simulation.
    """

    def __init__(self, mode: str = "golden_master_replay_skeleton") -> None:
        self.mode = mode

    def from_golden_master(self, golden_master: dict[str, Any]) -> UptrendCoreResult:
        raw = golden_master.get("raw_result", {})
        if not isinstance(raw, dict):
            raise TypeError("golden_master.raw_result must be a dict")

        daily_rows = raw.get("daily_equity_records", [])
        trade_rows = raw.get("trades", [])

        if not isinstance(daily_rows, list):
            raise TypeError("raw_result.daily_equity_records must be a list")
        if not isinstance(trade_rows, list):
            raise TypeError("raw_result.trades must be a list")

        daily_account = [self._normalize_daily_account_row(r) for r in daily_rows if isinstance(r, dict)]
        trades = [self._normalize_trade_row(r) for r in trade_rows if isinstance(r, dict)]

        return UptrendCoreResult(
            source="ENGINE_J_UPTREND_CORE_GOLDEN_MASTER_REPLAY_SKELETON",
            window=golden_master.get("window", {}),
            daily_account=daily_account,
            trades=trades,
            metadata={
                "mode": self.mode,
                "actual_strategy_logic_extracted": False,
                "strategy_decisions_generated": False,
                "purpose": "lock comparable interface and equivalence checker before real extraction",
            },
        )

    def _normalize_daily_account_row(self, row: dict[str, Any]) -> UptrendDailyAccountRow:
        return UptrendDailyAccountRow(
            date=str(row.get("date")),
            cash=float(row.get("cash", 0.0)),
            positions_value=float(row.get("positions_value", row.get("position_value", 0.0))),
            total_equity=float(row.get("total_equity", 0.0)),
            open_positions_count=int(row.get("open_positions_count", row.get("n_holdings", 0))),
            market_gate_state=row.get("market_gate_state"),
            spx_regime=row.get("spx_regime"),
            raw=dict(row),
        )

    def _normalize_trade_row(self, row: dict[str, Any]) -> UptrendTradeRow:
        return UptrendTradeRow(
            symbol=str(row.get("symbol")),
            entry_date=row.get("entry_date"),
            entry_price=self._optional_float(row.get("entry_price")),
            exit_date=row.get("exit_date"),
            exit_price=self._optional_float(row.get("exit_price")),
            entry_signal=row.get("entry_signal"),
            exit_signal=row.get("exit_signal"),
            entry_regime=row.get("entry_regime"),
            exit_regime=row.get("exit_regime"),
            return_pct=self._optional_float(row.get("return_pct")),
            holding_days=row.get("holding_days"),
            raw=dict(row),
        )

    @staticmethod
    def _optional_float(value: Any) -> float | None:
        if value is None:
            return None
        try:
            return float(value)
        except Exception:
            return None
