from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from e1r_engine.contracts import MarketSnapshot
from e1r_engine.market_gate import MarketGateDecision
from e1r_engine.state import AccountState, OrderIntent


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


@dataclass(frozen=True)
class CandidateSnapshot:
    """Opaque placeholder for future candidate extraction.

    R14 does not rank, filter, select, or score candidates.
    """

    date: str
    source: str
    candidates: tuple[dict[str, Any], ...] = ()
    selected_symbols: tuple[str, ...] = ()
    ranking_performed: bool = False
    strategy_selection_performed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def candidate_count(self) -> int:
        return len(self.candidates)

    def validate(self) -> list[str]:
        errors: list[str] = []

        if not self.date:
            errors.append("candidate_snapshot:missing_date")

        if not self.source:
            errors.append("candidate_snapshot:missing_source")

        if self.ranking_performed:
            errors.append(
                "candidate_snapshot:"
                "r14_ranking_must_not_be_performed"
            )

        if self.strategy_selection_performed:
            errors.append(
                "candidate_snapshot:"
                "r14_strategy_selection_must_not_be_performed"
            )

        if any(
            not isinstance(row, dict)
            for row in self.candidates
        ):
            errors.append(
                "candidate_snapshot:"
                "candidates_must_be_dict_records"
            )

        if len(set(self.selected_symbols)) != len(
            self.selected_symbols
        ):
            errors.append(
                "candidate_snapshot:"
                "duplicate_selected_symbols"
            )

        return errors


@dataclass(frozen=True)
class GateConsumptionTrace:
    """Trace-only contract for consuming MarketGateDecision.

    R14 does not generate or filter order intents.
    R15 will test BUY/ADD blocking behavior separately.
    """

    date: str
    gate_state: str
    market_state: str
    entry_capacity: int
    market_entry_allowed: bool
    effective_blocked_actions: tuple[str, ...]
    unaffected_actions: tuple[str, ...]
    source: str = "MarketGateDecision"
    gate_logic_recomputed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        errors: list[str] = []

        if not self.date:
            errors.append("gate_trace:missing_date")

        if self.entry_capacity < 0:
            errors.append(
                "gate_trace:negative_entry_capacity"
            )

        if self.gate_logic_recomputed:
            errors.append(
                "gate_trace:"
                "uptrend_core_must_not_recompute_gate_logic"
            )

        if self.gate_state not in {
            "ALLOW",
            "SHOCK",
            "RISK_OFF",
        }:
            errors.append("gate_trace:invalid_gate_state")

        allowed_actions = {
            "BUY",
            "ADD",
            "HOLD",
            "REDUCE",
            "EXIT",
        }

        if any(
            action not in allowed_actions
            for action in self.effective_blocked_actions
        ):
            errors.append(
                "gate_trace:invalid_blocked_action"
            )

        if any(
            action not in allowed_actions
            for action in self.unaffected_actions
        ):
            errors.append(
                "gate_trace:invalid_unaffected_action"
            )

        return errors


@dataclass(frozen=True)
class UptrendCoreInputs:
    """Stable R14 input contract for future UptrendCore logic."""

    date: str
    market_snapshot: MarketSnapshot
    account_state: AccountState
    market_gate_decision: MarketGateDecision
    candidate_snapshot: CandidateSnapshot
    max_live_holdings: int = 3
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        errors: list[str] = []

        if not self.date:
            errors.append("uptrend_inputs:missing_date")

        if self.max_live_holdings != 3:
            errors.append(
                "uptrend_inputs:"
                "max_live_holdings_contract_must_equal_3"
            )

        if self.market_snapshot.date != self.date:
            errors.append(
                "uptrend_inputs:"
                "market_snapshot_date_mismatch"
            )

        if self.account_state.date != self.date:
            errors.append(
                "uptrend_inputs:"
                "account_state_date_mismatch"
            )

        if self.market_gate_decision.date != self.date:
            errors.append(
                "uptrend_inputs:"
                "market_gate_decision_date_mismatch"
            )

        if self.candidate_snapshot.date != self.date:
            errors.append(
                "uptrend_inputs:"
                "candidate_snapshot_date_mismatch"
            )

        account_validation = self.account_state.validate(
            max_positions=self.max_live_holdings
        )

        if not account_validation["ok"]:
            errors.extend(
                "uptrend_inputs:account_state:" + error
                for error in account_validation["errors"]
            )

        errors.extend(self.candidate_snapshot.validate())

        return errors


@dataclass(frozen=True)
class UptrendCoreOutputs:
    """Stable R14 output contract without strategy implementation."""

    date: str
    account_state_reference: AccountState
    candidate_snapshot: CandidateSnapshot
    gate_consumption_trace: GateConsumptionTrace
    order_intents: tuple[OrderIntent, ...] = ()
    strategy_logic_implemented: bool = False
    account_state_mutated: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(
        self,
        max_live_holdings: int = 3,
    ) -> list[str]:
        errors: list[str] = []

        if not self.date:
            errors.append("uptrend_outputs:missing_date")

        if self.strategy_logic_implemented:
            errors.append(
                "uptrend_outputs:"
                "r14_strategy_logic_must_not_be_implemented"
            )

        if self.account_state_mutated:
            errors.append(
                "uptrend_outputs:"
                "r14_account_state_must_not_be_mutated"
            )

        if self.order_intents:
            errors.append(
                "uptrend_outputs:"
                "r14_order_intents_must_remain_empty"
            )

        if self.account_state_reference.date != self.date:
            errors.append(
                "uptrend_outputs:"
                "account_state_date_mismatch"
            )

        if self.candidate_snapshot.date != self.date:
            errors.append(
                "uptrend_outputs:"
                "candidate_snapshot_date_mismatch"
            )

        if self.gate_consumption_trace.date != self.date:
            errors.append(
                "uptrend_outputs:"
                "gate_trace_date_mismatch"
            )

        account_validation = (
            self.account_state_reference.validate(
                max_positions=max_live_holdings
            )
        )

        if not account_validation["ok"]:
            errors.extend(
                "uptrend_outputs:account_state:" + error
                for error in account_validation["errors"]
            )

        errors.extend(self.candidate_snapshot.validate())
        errors.extend(self.gate_consumption_trace.validate())

        for order_intent in self.order_intents:
            errors.extend(
                "uptrend_outputs:order_intent:" + error
                for error in order_intent.validate()
            )

        return errors


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

    def extract_from_legacy_result(self, legacy_result: dict[str, Any], window: dict[str, Any] | None = None) -> UptrendCoreResult:
        """
        ENGINE-K first real extraction boundary.

        This method extracts comparable UPTREND account/trade outputs from an actual
        run_stateful_simulation result dict. It does not replay a golden-master file,
        and it does not decide trading rules itself.

        Scope:
        - Accept legacy run_stateful_simulation output.
        - Normalize daily_equity_records and trades into stable UptrendCoreResult.
        - Preserve raw rows for future trace tightening.

        Non-scope:
        - No candidate ranking implementation.
        - No BUY/ADD/REDUCE/EXIT rule implementation.
        - No position sizing implementation.
        - No market gate implementation.
        """
        if not isinstance(legacy_result, dict):
            raise TypeError("legacy_result must be a dict")

        daily_rows = legacy_result.get("daily_equity_records", [])
        trade_rows = legacy_result.get("trades", [])

        if not isinstance(daily_rows, list):
            raise TypeError("legacy_result.daily_equity_records must be a list")
        if not isinstance(trade_rows, list):
            raise TypeError("legacy_result.trades must be a list")

        daily_account = [self._normalize_daily_account_row(r) for r in daily_rows if isinstance(r, dict)]
        trades = [self._normalize_trade_row(r) for r in trade_rows if isinstance(r, dict)]

        return UptrendCoreResult(
            source="ENGINE_K_UPTREND_CORE_LEGACY_RESULT_EXTRACTION",
            window=window or {},
            daily_account=daily_account,
            trades=trades,
            metadata={
                "mode": "legacy_result_extraction",
                "actual_strategy_logic_extracted": True,
                "strategy_decisions_generated": False,
                "legacy_result_extraction": True,
                "purpose": "first real extraction boundary from legacy run_stateful_simulation result into new E1R comparable schema",
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
