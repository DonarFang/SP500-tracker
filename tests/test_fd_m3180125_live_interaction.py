from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/record_fd_m3180125_live_interaction.py"


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def live_fixture(tmp_path: Path) -> tuple[Path, Path]:
    live_root = tmp_path / "live"
    price_root = tmp_path / "live_prices"
    price_root.mkdir()
    opening = {
        "opening_activated": True,
        "activation_required": False,
        "opening_date": "2026-07-27",
        "opening_cash": "100000.00",
        "positions": {},
    }
    runtime = {
        **opening,
        "opening_positions": {},
        "status": "ACTIVE",
        "last_committed_market_date": "2026-08-07",
    }
    write_json(live_root / "contracts/live_runtime_contract.json", opening)
    write_json(live_root / "runtime/current/runtime_state.json", runtime)
    write_json(
        price_root / "AAPL.json",
        [{
            "date": "2026-08-07",
            "open": "109",
            "high": "112",
            "low": "108",
            "close": "110",
            "volume": "1000",
        }],
    )
    return live_root, price_root


def run_event(
    tmp_path: Path,
    live_root: Path,
    price_root: Path,
    payload: dict[str, object],
) -> subprocess.CompletedProcess[str]:
    event_path = tmp_path / f"{payload['event_id']}.json"
    write_json(event_path, payload)
    environment = dict(os.environ)
    environment["PYTHONPATH"] = f"{ROOT}:{ROOT / 'src'}"
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--event-file",
            str(event_path),
            "--live-root",
            str(live_root),
            "--price-root",
            str(price_root),
        ],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
        env=environment,
    )


def base_event(**updates: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "contract": "FD_M3180125_LIVE_ACCOUNT_EVENT_V1",
        "user_confirmed": True,
        "event_type": "TRANSACTION",
        "event_id": "TX-20260809-AAPL-BUY-0001",
        "trade_date": "2026-08-09",
        "symbol": "AAPL",
        "action": "BUY",
        "price": "100",
        "shares": "10",
        "notes": "confirmed fill",
    }
    payload.update(updates)
    return payload


def test_confirmed_transaction_updates_two_ledger_projection_and_current_account(
    tmp_path: Path,
) -> None:
    live_root, price_root = live_fixture(tmp_path)
    result = run_event(tmp_path, live_root, price_root, base_event())
    assert "PASS_USER_CONFIRMED_LIVE_INTERACTION" in result.stdout

    transaction = json.loads(
        (live_root / "runtime/history/transactions.jsonl")
        .read_text(encoding="utf-8")
        .strip()
    )
    assert transaction["source"] == "USER_CONFIRMED_EXECUTION"
    assert transaction["gross_cash_effect"] == "-1000"
    assert transaction["cost_basis_after"] == "1000"
    assert transaction["realized_pnl"] == "0"

    account = json.loads(
        (live_root / "runtime/current/account_state.json")
        .read_text(encoding="utf-8")
    )
    assert account["actual_cash"] == "99000.00"
    assert account["total_equity"] == "100000.00"
    assert account["positions"]["AAPL"]["last_price"] == "100"
    assert account["positions"]["AAPL"]["position_source"] == (
        "USER_CONFIRMED_TRANSACTION_LEDGER"
    )


def test_confirmed_cash_control_preserves_trading_pnl(
    tmp_path: Path,
) -> None:
    live_root, price_root = live_fixture(tmp_path)
    result = run_event(
        tmp_path,
        live_root,
        price_root,
        base_event(
            event_type="CASH_CONTROL",
            event_id="CASH-20260809-0001",
            effective_date="2026-08-09",
            actual_cash="100250.00",
            notes="confirmed deposit",
        ),
    )
    assert "PASS_USER_CONFIRMED_LIVE_INTERACTION" in result.stdout
    cash = json.loads(
        (live_root / "runtime/history/cash_control.jsonl")
        .read_text(encoding="utf-8")
        .strip()
    )
    assert cash["cash_before"] == "100000.00"
    assert cash["cash_after"] == "100250.00"
    assert cash["cash_delta"] == "250.00"
    account = json.loads(
        (live_root / "runtime/current/account_state.json")
        .read_text(encoding="utf-8")
    )
    assert account["actual_cash"] == "100250.00"
    assert account["calculated_cash"] == "100000.00"
    assert account["cash_difference"] == "250.00"
    assert account["trading_pnl"] == "0"
