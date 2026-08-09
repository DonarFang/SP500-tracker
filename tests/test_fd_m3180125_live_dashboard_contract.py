from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIVE_ROOT = (
    ROOT
    / "exports/official/FD-M3180125-SP500-TOP3-engine/live"
)
D2_BLOCK_SHA256 = (
    "d22893819734c7e7fafba2de048ae38b6d66a7157683cd9deffd709c040aa9e6"
)


def test_live_tab_order_and_legacy_tabs_are_preserved() -> None:
    app = (ROOT / "dashboard/app.js").read_text(encoding="utf-8")
    index = (ROOT / "dashboard/index.html").read_text(encoding="utf-8")
    load_all = app[app.index("async function loadAll()") :]
    assert load_all.index("installStep3D1Tab()") < load_all.index(
        "installStep3D2Tab()"
    ) < load_all.index("installStep3D3Tab()")
    for label in ("Leader Board", "Watchlist", "Positions &amp; Exit"):
        assert label in index
    assert "Live Trade Display" in app


def test_forward_validation_block_is_byte_preserved() -> None:
    app = (ROOT / "dashboard/app.js").read_text(encoding="utf-8")
    start = app.index("/* STEP3_D2_FORWARD_TEST_VALIDATION */")
    end = app.index("function installStep3D1Tab()")
    assert hashlib.sha256(app[start:end].encode()).hexdigest() == D2_BLOCK_SHA256
    assert "E1R_CAPPED_ATR_A0_V1" in app[start:end]


def test_dashboard_interaction_is_owner_confirmed_and_has_no_browser_secret() -> None:
    app = (ROOT / "dashboard/app.js").read_text(encoding="utf-8")
    workflow = (
        ROOT / ".github/workflows/live-account-interaction.yml"
    ).read_text(encoding="utf-8")
    for required in (
        "runtime/history/transactions.jsonl",
        "runtime/history/cash_control.jsonl",
        "user_confirmed: true",
        "Submit new issue",
        "automatic execution: `false`",
    ):
        assert required.lower() in app.lower()
    assert "github.actor == 'DonarFang'" in workflow
    assert "issues:" in workflow
    assert "types: [opened]" in workflow
    assert "personal-live-track-daily" in workflow
    assert "contents: write" in workflow
    assert "password" not in app.lower()
    assert "github_pat_" not in app.lower()


def test_interaction_runner_is_live_only_and_compiles() -> None:
    runner = (
        ROOT / "scripts/record_fd_m3180125_live_interaction.py"
    ).read_text(encoding="utf-8")
    ast.parse(runner)
    assert "LiveRuntimeRepository" in runner
    assert "load_official_live_opening" in runner
    assert "USER_CONFIRMED_EXECUTION" in runner
    assert "future transactions cannot be recorded" in runner
    assert "automatic_execution\": False" in runner
    assert "broker_api_connected\": False" in runner
    assert "data/fw_prices" not in runner
    assert "/forward/" not in runner
    assert "/backtest/" not in runner


def test_current_official_live_artifacts_are_consistent() -> None:
    runtime = json.loads(
        (LIVE_ROOT / "runtime/current/runtime_state.json").read_text()
    )
    market = json.loads(
        (LIVE_ROOT / "runtime/current/latest_market_status.json").read_text()
    )
    recommendations = json.loads(
        (LIVE_ROOT / "runtime/current/latest_recommendations.json").read_text()
    )
    account = json.loads(
        (LIVE_ROOT / "runtime/current/account_state.json").read_text()
    )
    assert runtime["status"] == "ACTIVE"
    assert runtime["opening_date"] == "2026-07-27"
    assert runtime["opening_cash"] == "100000.00"
    assert runtime["automatic_execution_enabled"] is False
    assert runtime["broker_api_connected"] is False
    assert runtime["last_committed_market_date"] == market["date"]
    assert recommendations["signal_date"] == market["date"]
    assert recommendations["recommendation_only"] is True
    assert recommendations["automatic_execution"] is False
    for field in (
        "actual_cash",
        "calculated_cash",
        "cash_difference",
        "positions_value",
        "total_equity",
        "trading_pnl",
    ):
        assert field in account
