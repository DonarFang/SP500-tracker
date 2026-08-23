#!/usr/bin/env python3
"""Record one owner-confirmed Live account interaction.

The script writes only the independent Personal Live ledgers/current account
projection.  It never creates an Engine recommendation, an automatic fill, or
an order, and it never reads Forward or 5Y account state.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
from decimal import Decimal
import json
import os
from pathlib import Path
import re
from typing import Any, Mapping

from e1r_engine.live_account import LiveOpeningState, rebuild_live_account
from e1r_engine.live_composition import load_official_live_opening
from e1r_engine.live_data import LivePriceRepository
from e1r_engine.live_ledger import CashControlEvent, TransactionEvent
from e1r_engine.live_cycle_state import stable_recommendation_id
from e1r_engine.capped_atr_stop import VARIANT_ID
from e1r_engine.live_persistence import LiveRuntimeRepository


ENGINE = "FD-M3180125-SP500-TOP3-engine"
LIVE_ROOT = Path("exports/official") / ENGINE / "live"
PRICE_ROOT = Path("data/live_prices")
ISSUE_MARKER = "FD_M3180125_LIVE_ACCOUNT_EVENT_V1"
ALLOWED_OWNER = "DonarFang"


class LiveInteractionError(ValueError):
    pass


def load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise LiveInteractionError(f"expected JSON object: {path}")
    return payload


def load_optional_object(path: Path) -> dict[str, Any]:
    return load_object(path) if path.is_file() else {}


def extract_issue_payload(path: Path) -> dict[str, Any]:
    event = load_object(path)
    issue = event.get("issue")
    if not isinstance(issue, dict):
        raise LiveInteractionError("GitHub event does not contain an issue")
    login = str((issue.get("user") or {}).get("login") or "")
    owner = str((event.get("repository") or {}).get("owner", {}).get("login") or "")
    if login != ALLOWED_OWNER or owner != ALLOWED_OWNER:
        raise LiveInteractionError("only the repository owner may confirm Live events")
    body = str(issue.get("body") or "")
    if f"<!-- {ISSUE_MARKER} -->" not in body:
        raise LiveInteractionError("Live event marker is missing")
    match = re.search(r"```json\s*(\{.*?\})\s*```", body, re.DOTALL)
    if not match:
        raise LiveInteractionError("Live event JSON block is missing")
    payload = json.loads(match.group(1))
    if not isinstance(payload, dict):
        raise LiveInteractionError("Live event payload must be an object")
    return payload


def validate_common(payload: Mapping[str, Any]) -> None:
    if payload.get("contract") != ISSUE_MARKER:
        raise LiveInteractionError("Live event contract mismatch")
    if payload.get("user_confirmed") is not True:
        raise LiveInteractionError("user_confirmed must be true")
    event_id = str(payload.get("event_id") or "").strip()
    if not re.fullmatch(r"[A-Z0-9][A-Z0-9_.-]{7,79}", event_id):
        raise LiveInteractionError("event_id format is invalid")


def load_marks(
    *,
    price_root: Path,
    market_date: date,
    symbols: set[str],
    fill_symbol: str | None,
    fill_price: Decimal | None,
) -> dict[str, Decimal]:
    marks: dict[str, Decimal] = {}
    repository = LivePriceRepository(price_root)
    historical = set(symbols)
    if fill_symbol:
        historical.discard(fill_symbol)
    if historical:
        marks.update(repository.load_date(market_date, sorted(historical)).close_marks)
    if fill_symbol and fill_price is not None:
        marks[fill_symbol] = fill_price
    return marks


def position_cost_basis(account: object, symbol: str) -> Decimal:
    position = getattr(account, "positions", {}).get(symbol)
    return Decimal("0") if position is None else position.cost_basis


def recommendation_link(
    *, live_root: Path, symbol: str, action: str, trade_date: date
) -> dict[str, object]:
    current = load_optional_object(
        live_root / "runtime/current/latest_recommendations.json"
    )
    candidates = [
        current,
        *(
            load_optional_object(path)
            for path in sorted(
                (live_root / "runtime/daily").glob("*/engine_recommendations.json")
            )
        ),
    ]
    matches: list[dict[str, object]] = []
    for payload in candidates:
        signal_date = str(payload.get("signal_date") or "")
        expected = str(payload.get("expected_execution_date") or "")
        rows = payload.get("recommendations", [])
        if not signal_date or expected != trade_date.isoformat() or not isinstance(rows, list):
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            if str(row.get("symbol", "")).upper() == symbol.upper() and str(
                row.get("action", "")
            ).upper() == action.upper():
                matches.append(
                    {
                        "signal_date": signal_date,
                        "expected_execution_date": expected,
                        "recommendation_id": stable_recommendation_id(
                            signal_date=signal_date,
                            expected_execution_date=expected,
                            symbol=symbol,
                            action=action,
                        ),
                        "target_size_units": (
                            row.get("target_size_units")
                            or (
                                "0.5"
                                if "EMERGING" in str(row.get("reason", "")).upper()
                                else "1.0"
                                if action.upper() == "BUY"
                                else None
                            )
                        ),
                    }
                )
    unique = {str(item["recommendation_id"]): item for item in matches}
    if len(unique) > 1:
        raise LiveInteractionError("multiple recommendation links match transaction")
    return next(iter(unique.values()), {})


def validate_live_reduce_shares(*, current_shares: Decimal, reduce_shares: Decimal) -> None:
    if current_shares < 2:
        raise LiveInteractionError("HOLD_LIVE_REDUCE_MANUAL: fewer than two shares")
    half = current_shares / Decimal("2")
    allowed = {half.to_integral_value(rounding="ROUND_FLOOR"), half.to_integral_value(rounding="ROUND_CEILING")}
    if reduce_shares not in allowed or reduce_shares >= current_shares:
        raise LiveInteractionError("HOLD_LIVE_CYCLE_RECONCILIATION_REQUIRED")


def account_payload(account: object, marks: Mapping[str, Decimal]) -> dict[str, Any]:
    positions = {}
    for symbol, position in sorted(account.positions.items()):
        mark = marks.get(symbol, position.average_cost)
        positions[symbol] = {
            "shares": position.shares,
            "average_cost": position.average_cost,
            "cost_basis": position.cost_basis,
            "last_price": mark,
            "market_value": position.shares * mark,
            "unrealized_pnl": position.shares * (mark - position.average_cost),
            "position_source": "USER_CONFIRMED_TRANSACTION_LEDGER",
        }
    return {
        "actual_cash": account.actual_cash,
        "calculated_cash": account.calculated_cash,
        "cash_difference": account.cash_difference,
        "positions": positions,
        "positions_value": account.positions_value,
        "realized_pnl": account.realized_pnl,
        "total_equity": account.total_equity,
        "trading_pnl": account.trading_pnl,
        "unrealized_pnl": account.unrealized_pnl,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event-file", type=Path)
    parser.add_argument("--github-event", type=Path)
    parser.add_argument("--live-root", type=Path, default=LIVE_ROOT)
    parser.add_argument("--price-root", type=Path, default=PRICE_ROOT)
    args = parser.parse_args()
    if bool(args.event_file) == bool(args.github_event):
        raise LiveInteractionError("provide exactly one event source")
    payload = (
        load_object(args.event_file)
        if args.event_file
        else extract_issue_payload(args.github_event)
    )
    validate_common(payload)

    live_root = args.live_root
    price_root = args.price_root
    runtime_state = load_object(live_root / "runtime/current/runtime_state.json")
    if runtime_state.get("status") != "ACTIVE":
        raise LiveInteractionError("Live runtime is not ACTIVE")
    market_date = date.fromisoformat(str(runtime_state["last_committed_market_date"]))
    opening: LiveOpeningState = load_official_live_opening(live_root)
    repository = LiveRuntimeRepository(live_root)
    ledger = repository.load_ledger()
    before = rebuild_live_account(opening=opening, ledger=ledger)
    event_type = str(payload.get("event_type") or "").upper()
    now = datetime.now(timezone.utc)
    latest_market = load_optional_object(
        live_root / "runtime/current/latest_market_status.json"
    )

    if event_type == "TRANSACTION":
        transaction_symbol = str(payload["symbol"]).strip().upper()
        transaction_action = str(payload["action"]).strip().upper()
        transaction_date = date.fromisoformat(str(payload["trade_date"]))
        link = recommendation_link(
            live_root=live_root,
            symbol=transaction_symbol,
            action=transaction_action,
            trade_date=transaction_date,
        )
        if transaction_action == "REDUCE":
            position = before.positions.get(transaction_symbol)
            if position is None:
                raise LiveInteractionError("REDUCE requires an active position")
            validate_live_reduce_shares(
                current_shares=position.shares,
                reduce_shares=Decimal(str(payload.get("shares"))),
            )
        event = TransactionEvent(
            event_id=str(payload["event_id"]),
            trade_date=date.fromisoformat(str(payload["trade_date"])),
            symbol=str(payload["symbol"]),
            action=str(payload["action"]),
            price=str(payload["price"]),
            shares=payload.get("shares"),
            notes=str(payload.get("notes") or ""),
            recommendation_id=str(payload.get("recommendation_id") or link.get("recommendation_id") or "") or None,
            signal_date=(
                date.fromisoformat(str(payload.get("signal_date") or link.get("signal_date")))
                if payload.get("signal_date") or link.get("signal_date")
                else None
            ),
            expected_execution_date=(
                date.fromisoformat(str(payload.get("expected_execution_date") or link.get("expected_execution_date")))
                if payload.get("expected_execution_date") or link.get("expected_execution_date")
                else None
            ),
            origin_branch=str(payload.get("origin_branch") or latest_market.get("strategy_branch") or "UPTREND"),
            strategy_variant=str(payload.get("strategy_variant") or VARIANT_ID),
            target_size_units=payload.get("target_size_units") or link.get("target_size_units"),
        )
        if opening.opening_date and event.trade_date < opening.opening_date:
            raise LiveInteractionError("trade_date precedes Live opening_date")
        if event.trade_date > now.date():
            raise LiveInteractionError("future transactions cannot be recorded")
        ledger.append_transaction(event)
        preliminary = rebuild_live_account(opening=opening, ledger=ledger)
        marks = load_marks(
            price_root=price_root,
            market_date=market_date,
            symbols=set(preliminary.positions),
            fill_symbol=event.symbol if event.symbol in preliminary.positions else None,
            fill_price=event.price if event.symbol in preliminary.positions else None,
        )
        after = rebuild_live_account(opening=opening, ledger=ledger, marks=marks)
        applied = after.applied_transactions[-1]
        audit = {
            **event.canonical_payload(),
            "created_at": now,
            "source": "USER_CONFIRMED_EXECUTION",
            "origin_regime": latest_market.get("regime") or "UNKNOWN",
            "origin_subclass": latest_market.get("subclass") or "UNKNOWN",
            "effective_shares": applied.effective_shares,
            "gross_cash_effect": applied.gross_cash_effect,
            "actual_cash_before": before.actual_cash,
            "actual_cash_after": after.actual_cash,
            "calculated_cash_before": before.calculated_cash,
            "calculated_cash_after": after.calculated_cash,
            "cost_basis_before": position_cost_basis(before, event.symbol),
            "cost_basis_after": position_cost_basis(after, event.symbol),
            "realized_pnl": applied.realized_pnl,
        }
        repository.append_transaction(event, audit_payload=audit)
    elif event_type == "CASH_CONTROL":
        event = CashControlEvent(
            event_id=str(payload["event_id"]),
            effective_date=date.fromisoformat(str(payload["effective_date"])),
            actual_cash=str(payload["actual_cash"]),
            notes=str(payload.get("notes") or ""),
        )
        if opening.opening_date and event.effective_date < opening.opening_date:
            raise LiveInteractionError("effective_date precedes Live opening_date")
        if event.effective_date > now.date():
            raise LiveInteractionError("future cash controls cannot be recorded")
        ledger.append_cash_control(event)
        preliminary = rebuild_live_account(opening=opening, ledger=ledger)
        marks = load_marks(
            price_root=price_root,
            market_date=market_date,
            symbols=set(preliminary.positions),
            fill_symbol=None,
            fill_price=None,
        )
        after = rebuild_live_account(opening=opening, ledger=ledger, marks=marks)
        repository.append_cash_control(
            event,
            cash_before=before.actual_cash,
            created_at=now,
        )
    else:
        raise LiveInteractionError("event_type must be TRANSACTION or CASH_CONTROL")

    current = account_payload(after, marks)
    repository.replace_current("account_state.json", current)
    repository.replace_current("positions.json", {"positions": current["positions"]})
    interaction = {
        "decision": "PASS_USER_CONFIRMED_LIVE_INTERACTION",
        "event_id": str(payload["event_id"]),
        "event_type": event_type,
        "recorded_at": now,
        "market_data_date": market_date,
        "account_state": {
            "actual_cash": after.actual_cash,
            "calculated_cash": after.calculated_cash,
            "cash_difference": after.cash_difference,
            "total_equity": after.total_equity,
        },
        "automatic_execution": False,
        "broker_api_connected": False,
    }
    repository.update_automation("latest_user_interaction.json", interaction)
    print(json.dumps(interaction, ensure_ascii=False, indent=2, default=str))
    print("PASS_USER_CONFIRMED_LIVE_INTERACTION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
