from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EquivalenceMismatch:
    assertion: str
    index: int | None
    field: str
    expected: Any
    actual: Any
    tolerance: str
    severity: str


@dataclass(frozen=True)
class EquivalenceReport:
    ok: bool
    checked_assertions: list[str]
    mismatch_count: int
    mismatches: list[EquivalenceMismatch]
    summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "checked_assertions": self.checked_assertions,
            "mismatch_count": self.mismatch_count,
            "mismatches": [m.__dict__ for m in self.mismatches],
            "summary": self.summary,
        }


class UptrendEquivalenceChecker:
    """
    ENGINE-J equivalence checker for UPTREND extraction.

    It implements the ENGINE-H T0/T1 minimum assertions:
    - daily date sequence
    - daily cash / positions_value / total_equity
    - daily open_positions_count
    - daily market_gate_state
    - daily spx_regime
    - trade lifecycle symbol/date/price
    - trade signals and regimes
    """

    def __init__(self, money_abs_tol: float = 0.01, pct_abs_tol: float = 0.01) -> None:
        self.money_abs_tol = float(money_abs_tol)
        self.pct_abs_tol = float(pct_abs_tol)

    def compare(self, expected: dict[str, Any], actual: dict[str, Any]) -> EquivalenceReport:
        mismatches: list[EquivalenceMismatch] = []
        checked: list[str] = []

        expected_daily = expected.get("daily_account", [])
        actual_daily = actual.get("daily_account", [])
        expected_trades = expected.get("trades", [])
        actual_trades = actual.get("trades", [])

        checked.append("daily_account_date_sequence")
        self._compare_daily_date_sequence(expected_daily, actual_daily, mismatches)

        checked.append("daily_total_equity_cash_positions")
        self._compare_daily_money(expected_daily, actual_daily, mismatches)

        checked.append("daily_open_positions_count")
        self._compare_daily_exact(
            expected_daily,
            actual_daily,
            field="open_positions_count",
            assertion="daily_open_positions_count",
            mismatches=mismatches,
        )

        checked.append("daily_market_gate_state")
        self._compare_daily_exact(
            expected_daily,
            actual_daily,
            field="market_gate_state",
            assertion="daily_market_gate_state",
            mismatches=mismatches,
        )

        checked.append("daily_spx_regime")
        self._compare_daily_exact(
            expected_daily,
            actual_daily,
            field="spx_regime",
            assertion="daily_spx_regime",
            mismatches=mismatches,
        )

        checked.append("trade_lifecycle_symbol_dates")
        self._compare_trade_lifecycle(expected_trades, actual_trades, mismatches)

        checked.append("trade_signals_and_reasons")
        self._compare_trade_signals(expected_trades, actual_trades, mismatches)

        return EquivalenceReport(
            ok=len(mismatches) == 0,
            checked_assertions=checked,
            mismatch_count=len(mismatches),
            mismatches=mismatches,
            summary={
                "expected_daily_rows": len(expected_daily),
                "actual_daily_rows": len(actual_daily),
                "expected_trades": len(expected_trades),
                "actual_trades": len(actual_trades),
                "money_abs_tol": self.money_abs_tol,
                "pct_abs_tol": self.pct_abs_tol,
            },
        )

    def _compare_daily_date_sequence(self, expected_rows: list[dict[str, Any]], actual_rows: list[dict[str, Any]], mismatches: list[EquivalenceMismatch]) -> None:
        expected_dates = [r.get("date") for r in expected_rows]
        actual_dates = [r.get("date") for r in actual_rows]

        if expected_dates != actual_dates:
            mismatches.append(EquivalenceMismatch(
                assertion="daily_account_date_sequence",
                index=None,
                field="date_sequence",
                expected=expected_dates,
                actual=actual_dates,
                tolerance="exact",
                severity="hard_fail",
            ))

    def _compare_daily_money(self, expected_rows: list[dict[str, Any]], actual_rows: list[dict[str, Any]], mismatches: list[EquivalenceMismatch]) -> None:
        for i, (e, a) in enumerate(zip(expected_rows, actual_rows)):
            for field in ["cash", "positions_value", "total_equity"]:
                ev = self._to_float(e.get(field))
                av = self._to_float(a.get(field))
                if ev is None or av is None or abs(ev - av) > self.money_abs_tol:
                    mismatches.append(EquivalenceMismatch(
                        assertion="daily_total_equity_cash_positions",
                        index=i,
                        field=field,
                        expected=e.get(field),
                        actual=a.get(field),
                        tolerance=f"abs <= {self.money_abs_tol}",
                        severity="hard_fail",
                    ))

    def _compare_daily_exact(self, expected_rows: list[dict[str, Any]], actual_rows: list[dict[str, Any]], field: str, assertion: str, mismatches: list[EquivalenceMismatch]) -> None:
        for i, (e, a) in enumerate(zip(expected_rows, actual_rows)):
            if e.get(field) != a.get(field):
                mismatches.append(EquivalenceMismatch(
                    assertion=assertion,
                    index=i,
                    field=field,
                    expected=e.get(field),
                    actual=a.get(field),
                    tolerance="exact",
                    severity="hard_fail",
                ))

        if len(expected_rows) != len(actual_rows):
            mismatches.append(EquivalenceMismatch(
                assertion=assertion,
                index=None,
                field="row_count",
                expected=len(expected_rows),
                actual=len(actual_rows),
                tolerance="exact",
                severity="hard_fail",
            ))

    def _compare_trade_lifecycle(self, expected_trades: list[dict[str, Any]], actual_trades: list[dict[str, Any]], mismatches: list[EquivalenceMismatch]) -> None:
        if len(expected_trades) != len(actual_trades):
            mismatches.append(EquivalenceMismatch(
                assertion="trade_lifecycle_symbol_dates",
                index=None,
                field="trade_count",
                expected=len(expected_trades),
                actual=len(actual_trades),
                tolerance="exact",
                severity="hard_fail",
            ))

        for i, (e, a) in enumerate(zip(expected_trades, actual_trades)):
            for field in ["symbol", "entry_date", "exit_date"]:
                if e.get(field) != a.get(field):
                    mismatches.append(EquivalenceMismatch(
                        assertion="trade_lifecycle_symbol_dates",
                        index=i,
                        field=field,
                        expected=e.get(field),
                        actual=a.get(field),
                        tolerance="exact",
                        severity="hard_fail",
                    ))

            for field in ["entry_price", "exit_price", "return_pct"]:
                ev = self._to_float(e.get(field))
                av = self._to_float(a.get(field))
                tol = self.money_abs_tol if field != "return_pct" else self.pct_abs_tol
                if ev is None or av is None or abs(ev - av) > tol:
                    mismatches.append(EquivalenceMismatch(
                        assertion="trade_lifecycle_symbol_dates",
                        index=i,
                        field=field,
                        expected=e.get(field),
                        actual=a.get(field),
                        tolerance=f"abs <= {tol}",
                        severity="hard_fail",
                    ))

    def _compare_trade_signals(self, expected_trades: list[dict[str, Any]], actual_trades: list[dict[str, Any]], mismatches: list[EquivalenceMismatch]) -> None:
        for i, (e, a) in enumerate(zip(expected_trades, actual_trades)):
            for field in ["entry_signal", "exit_signal", "entry_regime", "exit_regime"]:
                if e.get(field) != a.get(field):
                    mismatches.append(EquivalenceMismatch(
                        assertion="trade_signals_and_reasons",
                        index=i,
                        field=field,
                        expected=e.get(field),
                        actual=a.get(field),
                        tolerance="exact",
                        severity="hard_fail",
                    ))

    @staticmethod
    def _to_float(value: Any) -> float | None:
        if value is None:
            return None
        try:
            return float(value)
        except Exception:
            return None
