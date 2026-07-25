from datetime import date, timedelta
import json
from pathlib import Path

from e1r_engine.live_composition import (
    run_unactivated_live_acceptance,
)


def write_series(
    root: Path,
    symbol: str,
    *,
    days: int = 500,
    slope: float = 0.1,
) -> str:
    start = date(2025, 1, 1)
    rows = []

    for index in range(days):
        day = start + timedelta(
            days=index
        )
        base = 100.0 + slope * index

        rows.append(
            {
                "date": day.isoformat(),
                "open": base,
                "high": base + 1.0,
                "low": base - 1.0,
                "close": base,
                "volume": 1000,
            }
        )

    (root / f"{symbol}.json").write_text(
        json.dumps(rows),
        encoding="utf-8",
    )

    return rows[-1]["date"]


def test_real_live_production_composition_unactivated_e2e(
    tmp_path: Path,
) -> None:
    price_root = tmp_path / "live_prices"
    price_root.mkdir()

    market_date = write_series(
        price_root,
        "SPX",
        slope=0.20,
    )
    write_series(
        price_root,
        "NDX",
        slope=0.22,
    )
    write_series(
        price_root,
        "SOX",
        slope=0.25,
    )
    write_series(
        price_root,
        "VIX",
        slope=0.01,
    )
    write_series(
        price_root,
        "AAPL",
        slope=0.15,
    )

    day = date.fromisoformat(
        market_date
    )
    expected_execution_date = (
        day + timedelta(days=1)
    )

    live_root = tmp_path / "live"
    status_path = (
        live_root
        / "automation"
        / "current_data_update.json"
    )
    status_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    status_path.write_text(
        json.dumps(
            {
                "data_status": "CURRENT",
                "latest_market_date": (
                    market_date
                ),
                "catalogue_changed": False,
                "unavailable_symbols": [],
            }
        ),
        encoding="utf-8",
    )

    accepted = run_unactivated_live_acceptance(
        price_root=price_root,
        live_root=live_root,
        data_status_path=status_path,
        market_date=day,
        expected_execution_date=(
            expected_execution_date
        ),
        expected_stock_count=1,
        min_bars=120,
    )

    assert (
        accepted["decision"]
        == "PASS_LIVE_PRODUCTION_DRY_RUN"
    )
    assert accepted["opening_activated"] is False
    assert accepted["stock_symbol_count"] == 1
    assert accepted["engine_modified"] is False
    assert accepted["workflow_created"] is False

    daily_root = (
        live_root
        / "runtime"
        / "daily"
        / market_date
    )

    for filename in (
        "market_status.json",
        "reference_top3.json",
        "account_state.json",
        "active_positions.json",
        "engine_recommendations.json",
        "manual_transactions.json",
        "reconciliation.json",
        "equity.json",
        "manifest.json",
    ):
        assert (
            daily_root / filename
        ).is_file()

    runtime_state = json.loads(
        (
            live_root
            / "runtime"
            / "current"
            / "runtime_state.json"
        ).read_text(encoding="utf-8")
    )

    assert (
        runtime_state["status"]
        == "UNACTIVATED"
    )

    last_run = json.loads(
        (
            live_root
            / "automation"
            / "last_successful_run.json"
        ).read_text(encoding="utf-8")
    )

    assert (
        last_run["run_mode"]
        == "DRY_RUN_UNACTIVATED"
    )
    assert last_run["opening_activated"] is False
