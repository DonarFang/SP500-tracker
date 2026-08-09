#!/usr/bin/env python3
"""AE-step 2 isolated Forward/Live replay and atomic promotion."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

from e1r_engine.capped_atr_stop import (
    DISPLAY_NAME,
    POSITION_METADATA_KEY,
    VARIANT_ID,
    build_entry_metadata,
    build_frozen_state,
    compute_entry_atr20,
)
from e1r_engine.core import E1RCoreEngine
from e1r_engine.forward_orchestrator import ForwardStrategyInputBuilder
from e1r_engine.forward_production_composition import (
    build_production_forward_composition,
)
from e1r_engine.forward_runtime import ForwardMarketDataAdapter
from e1r_engine.live_composition import compose_active_live_production


ROOT = Path(__file__).resolve().parents[1]
ENGINE_ID = "FD-M3180125-SP500-TOP3-engine"
OFFICIAL = ROOT / "exports" / "official" / ENGINE_ID
BACKTEST = OFFICIAL / "backtest" / "canonical_5y"
FORWARD = OFFICIAL / "forward"
LIVE = OFFICIAL / "live"
SEED_DATE = "2026-06-16"
FIRST_FORWARD_DATE = "2026-06-17"
LIVE_OPENING_DATE = "2026-07-27"
EXPECTED_RESULT_SHA = (
    "9720084b92ed7e7ae80eaf606a170239312e333f4e5daca7d284835afc6ffcd3"
)
EXCLUDED = {
    "SPX", "NDX", "SOX", "VIX", "_GSPC", "_NDX", "_SOX", "_VIX",
    "GSPC", "^GSPC", "^NDX", "^SOX", "^VIX", "QQQ", "SOXX", "VIXY",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_hash(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(str(item.relative_to(path)).encode())
        digest.update(b"\0")
        digest.update(item.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def parse_series(path: Path) -> dict[str, Any]:
    return ForwardMarketDataAdapter.parse_price_file(path)


def entry_stop(symbol: str, signal_date: str, a0: float) -> dict[str, Any]:
    path = ROOT / "data" / "research" / "e1_5y" / "raw" / "stocks" / f"{symbol}.json"
    series = parse_series(path)
    dates = sorted(series)
    bars = [series[item] for item in dates]
    atr20 = compute_entry_atr20(
        symbol=symbol,
        dates=dates,
        closes=[bar.close for bar in bars],
        ohlc={
            "high": [bar.high for bar in bars],
            "low": [bar.low for bar in bars],
        },
        as_of_date=signal_date,
    )
    if atr20 is None:
        raise RuntimeError(f"{symbol}: cannot derive frozen ATR20 on {signal_date}")
    return build_frozen_state(
        adjusted_first_buy_price=a0,
        entry_metadata=build_entry_metadata(
            atr20=float(atr20), atr_as_of=signal_date
        ),
    ).to_dict()


def build_forward_seed(seed_root: Path, source_head: str) -> dict[str, Any]:
    result_path = ROOT / "exports" / "e1r_unified_5y_full_account_v1_result.json"
    if sha256(result_path) != EXPECTED_RESULT_SHA:
        raise RuntimeError("AE-step 1 result SHA mismatch")
    metrics = load_json(BACKTEST / "official_metrics.json")
    records = load_json(BACKTEST / "regular_eod_account_records.json")
    trades = load_json(BACKTEST / "actual_sim_end_trades.json")
    if metrics.get("formal_variant") != VARIANT_ID:
        raise RuntimeError("Canonical 5Y variant is not CAPPED-ATR")
    last = records[-1]
    if last.get("date") != SEED_DATE or len(trades) != 3:
        raise RuntimeError("Canonical 5Y boundary evidence mismatch")

    positions = []
    for trade in sorted(trades, key=lambda item: item["symbol"]):
        symbol = str(trade["symbol"])
        quantity = float(trade["entry_shares"]) * float(trade["size_units_at_exit"])
        avg_cost = float(trade["entry_execution_price"])
        last_price = float(trade["exit_price"])
        stop_state = entry_stop(
            symbol,
            str(trade["entry_signal_date"]),
            avg_cost,
        )
        positions.append({
            "symbol": symbol,
            "quantity": quantity,
            "avg_cost": avg_cost,
            "last_price": last_price,
            "market_value": quantity * last_price,
            "unrealized_pnl": (last_price - avg_cost) * quantity,
            "entry_date": str(trade["entry_execution_date"]),
            "last_update_date": SEED_DATE,
            "metadata": {
                "carried_position": True,
                "new_forward_buy": False,
                "origin_branch": str(trade["origin_branch"]),
                "remaining_cost_basis": quantity * avg_cost,
                "size_units": float(trade["size_units_at_exit"]),
                "entry_shares": float(trade["entry_shares"]),
                "entry_execution_price": avg_cost,
                POSITION_METADATA_KEY: stop_state,
            },
        })

    positions_value = sum(item["market_value"] for item in positions)
    cash = float(last["cash"])
    if abs(positions_value - float(last["positions_value"])) > 0.02:
        raise RuntimeError("reconstructed seed positions do not reconcile")
    if abs(cash + positions_value - float(last["total_equity"])) > 0.02:
        raise RuntimeError("reconstructed seed equity does not reconcile")

    state = {
        "schema_version": "2.0.0",
        "record_type": "AE_STEP2_CAPPED_ATR_FORWARD_RUNTIME_SEED_STATE",
        "engine_id": ENGINE_ID,
        "formal_variant": VARIANT_ID,
        "seed_boundary": {
            "seed_date": SEED_DATE,
            "first_forward_market_date": FIRST_FORWARD_DATE,
        },
        "seed_semantics": "PRE_SIM_END_CONTINUOUS_ACCOUNT_STATE",
        "sim_end_replayed": False,
        "pending_order_resolution": {
            "historical_pending_order_count_proven": int(last["pending_orders_count"]),
            "exact_payload_proven": False,
            "actionable_pending_orders": [],
            "resolution": "EXPIRED_UNPROVEN_AT_FORWARD_BOUNDARY",
        },
        "account": {
            "date": SEED_DATE,
            "cash": cash,
            "positions": positions,
            "positions_value": positions_value,
            "total_equity": cash + positions_value,
            "open_positions_count": len(positions),
            "metadata": {
                "source": "AE_STEP1_CANONICAL_5Y_NORMAL_EOD",
                "strategy_variant": VARIANT_ID,
                "strategy_display_name": DISPLAY_NAME,
                "sim_end_liquidation_replayed": False,
            },
        },
    }
    contract = {
        "schema_version": "2.0.0",
        "contract_id": f"{ENGINE_ID}/forward-runtime-seed/{SEED_DATE}/ae-step2",
        "contract_status": "ACTIVE_CANONICAL",
        "engine_id": ENGINE_ID,
        "formal_variant": VARIANT_ID,
        "forward_date_contract": {
            "seed_date": SEED_DATE,
            "first_forward_market_date": FIRST_FORWARD_DATE,
            "last_normal_backtest_eod": SEED_DATE,
        },
        "account_economic_contract": {
            "cash": cash,
            "positions_value": positions_value,
            "total_equity": cash + positions_value,
            "required_position_symbols": [item["symbol"] for item in positions],
            "capped_atr_state_required": True,
        },
        "pending_order_contract": state["pending_order_resolution"],
        "runtime_start_semantics": {
            "all_cash_final_settlement_used": False,
            "sim_end_liquidation_replayed": False,
        },
    }
    provenance = {
        "schema_version": "2.0.0",
        "engine_id": ENGINE_ID,
        "artifact_type": "AE_STEP2_CAPPED_ATR_FORWARD_SEED",
        "source_commit": source_head,
        "canonical_result_sha256": EXPECTED_RESULT_SHA,
        "official_metrics_sha256": sha256(BACKTEST / "official_metrics.json"),
        "regular_eod_account_records_sha256": sha256(
            BACKTEST / "regular_eod_account_records.json"
        ),
        "actual_sim_end_trades_sha256": sha256(
            BACKTEST / "actual_sim_end_trades.json"
        ),
        "backtest_rerun_performed": False,
        "sim_end_replayed": False,
    }
    write_json(seed_root / "forward_runtime_seed_state.json", state)
    write_json(seed_root / "forward_runtime_seed_contract.json", contract)
    write_json(seed_root / "forward_runtime_seed_provenance.json", provenance)
    decision = {
        "decision": "PASS_AE_STEP2_CAPPED_ATR_FORWARD_SEED_REBUILT",
        "seed_date": SEED_DATE,
        "first_forward_market_date": FIRST_FORWARD_DATE,
        "seed_equity": cash + positions_value,
        "position_symbols": [item["symbol"] for item in positions],
        "sim_end_replayed": False,
    }
    write_json(seed_root / "STEP2_FORWARD_RUNTIME_SEED_FREEZE_DECISION.json", decision)
    manifest = {
        "schema_version": "2.0.0",
        "engine_id": ENGINE_ID,
        "status": "ACTIVE_CANONICAL",
        "seed_date": SEED_DATE,
        "first_forward_market_date": FIRST_FORWARD_DATE,
        "legacy_oos_is_fact_source": False,
        "sim_end_replayed": False,
        "formal_variant": VARIANT_ID,
        "artifacts": [
            {"path": name, "sha256": sha256(seed_root / name)}
            for name in (
                "forward_runtime_seed_state.json",
                "forward_runtime_seed_contract.json",
                "forward_runtime_seed_provenance.json",
                "STEP2_FORWARD_RUNTIME_SEED_FREEZE_DECISION.json",
            )
        ],
    }
    write_json(seed_root / "current_manifest.json", manifest)
    return decision


class ProviderShouldNotBeCalled:
    def __call__(self, *args: Any, **kwargs: Any) -> Mapping[str, str]:
        raise RuntimeError("no policy may be synthesized outside E1RCoreEngine")


def build_forward_composition(seed_root: Path, runtime_root: Path, source_head: str):
    price_root = ROOT / "data" / "fw_prices"
    price_files: dict[str, Path] = {}
    aliases = {"_GSPC": "SPX", "_NDX": "NDX", "_SOX": "SOX"}
    for path in sorted(price_root.glob("*.json")):
        symbol = path.stem.upper()
        price_files[symbol] = path
        if symbol in aliases:
            price_files[aliases[symbol]] = path
    universe = tuple(sorted(symbol for symbol in price_files if symbol not in EXCLUDED))
    builder = ForwardStrategyInputBuilder(
        engine=E1RCoreEngine(),
        management_action_provider=ProviderShouldNotBeCalled(),
    )
    return build_production_forward_composition(
        seed_root=seed_root,
        runtime_root=runtime_root,
        price_files_by_symbol=price_files,
        universe=universe,
        strategy_input_builder=builder,
        runtime_commit_provider=lambda: source_head,
    )


def replay_forward(seed_root: Path, runtime_root: Path, source_head: str) -> dict[str, Any]:
    composition = build_forward_composition(seed_root, runtime_root, source_head)
    dry = composition.runner.dry_run()
    planned = list(dry.planned_dates)
    if not planned or planned[0] != FIRST_FORWARD_DATE:
        raise RuntimeError("Forward replay does not begin on 2026-06-17")
    results = list(composition.runner.run(allow_official_write=True))
    if [item.trading_date for item in results] != planned:
        raise RuntimeError("Forward replay committed-date mismatch")
    state = composition.repository.load()
    state.validate()
    curve = load_json(runtime_root / "history" / "equity_curve.json")
    if len(curve) != len(planned) or curve[0]["date"] != FIRST_FORWARD_DATE:
        raise RuntimeError("Forward equity curve boundary mismatch")
    for position in state.account.positions.values():
        if POSITION_METADATA_KEY not in position.metadata:
            raise RuntimeError(f"{position.symbol}: missing CAPPED-ATR state")
    return {
        "decision": "PASS_AE_STEP2_FORWARD_REPLAY",
        "first_date": planned[0],
        "last_date": planned[-1],
        "committed_date_count": len(planned),
        "final_equity": state.account.total_equity,
        "open_positions": sorted(state.account.positions),
        "sim_end_replayed": False,
    }


def next_weekday(day: date) -> date:
    result = day + timedelta(days=1)
    while result.weekday() >= 5:
        result += timedelta(days=1)
    return result


def live_market_dates() -> list[str]:
    date_sets = []
    for symbol in ("SPX", "NDX", "SOX"):
        rows = load_json(ROOT / "data" / "live_prices" / f"{symbol}.json")
        date_sets.append({str(row["date"]) for row in rows})
    return sorted(
        item for item in set.intersection(*date_sets)
        if item >= LIVE_OPENING_DATE
    )


def assert_empty_live_ledgers() -> None:
    for name in ("ledger_journal.jsonl", "transactions.jsonl", "cash_control.jsonl"):
        path = LIVE / "runtime" / "history" / name
        if path.exists() and path.read_text(encoding="utf-8").strip():
            raise RuntimeError(
                "AE-step 2 automatic Live replay requires no recorded actual transactions"
            )


def replay_live(staged_live: Path) -> dict[str, Any]:
    assert_empty_live_ledgers()
    shutil.copytree(LIVE / "contracts", staged_live / "contracts")
    shutil.copytree(LIVE / "automation", staged_live / "automation")
    activation = load_json(LIVE / "contracts" / "live_opening_activation.json")
    if (
        activation.get("opening_date") != LIVE_OPENING_DATE
        or str(activation.get("opening_cash")) != "100000.00"
        or activation.get("positions") != {}
        or activation.get("opening_activated") is not True
    ):
        raise RuntimeError("Live Opening contract mismatch")
    initial_state = load_json(
        LIVE / "runtime" / "current" / "runtime_state.json"
    )
    initial_state.update({
        "status": "ACTIVE",
        "opening_date": LIVE_OPENING_DATE,
        "opening_cash": "100000.00",
        "opening_positions": {},
        "opening_activated": True,
        "activation_required": False,
        "last_committed_market_date": None,
        "last_successful_run_at": None,
        "automatic_execution_enabled": False,
        "broker_api_connected": False,
        "workflow_created": True,
    })
    write_json(staged_live / "runtime" / "current" / "runtime_state.json", initial_state)
    market_dates = live_market_dates()
    if not market_dates or market_dates[0] != LIVE_OPENING_DATE:
        raise RuntimeError("Live replay does not begin on Opening date")
    results = []
    status_path = staged_live / "automation" / "current_data_update.json"
    for date_text in market_dates:
        market_date = date.fromisoformat(date_text)
        write_json(status_path, {
            "data_status": "CURRENT",
            "latest_market_date": date_text,
            "catalogue_changed": False,
            "unavailable_symbols": [],
        })
        composition = compose_active_live_production(
            price_root=ROOT / "data" / "live_prices",
            live_root=staged_live,
            data_status_path=status_path,
            market_date=market_date,
            expected_execution_date=next_weekday(market_date),
            expected_stock_count=494,
            min_bars=120,
        )
        result = composition.runtime.dry_run(
            market_date=market_date,
            market_data=composition.market_data,
        )
        results.append(composition.runtime.commit_active_daily(
            result=result,
            expected_execution_date=next_weekday(market_date),
        ))
    source_status = LIVE / "automation" / "current_data_update.json"
    if source_status.exists():
        shutil.copy2(source_status, status_path)
    daily_dates = sorted(
        item.name for item in (staged_live / "runtime" / "daily").iterdir()
        if item.is_dir()
    )
    if daily_dates != market_dates or "2026-07-24" in daily_dates:
        raise RuntimeError("Live replay daily boundary mismatch")
    state = load_json(staged_live / "runtime" / "current" / "runtime_state.json")
    if state.get("last_committed_market_date") != market_dates[-1]:
        raise RuntimeError("Live current state date mismatch")
    report = {
        "decision": "PASS_AE_STEP2_LIVE_OPENING_REPLAY",
        "opening_date": LIVE_OPENING_DATE,
        "opening_cash": "100000.00",
        "opening_positions": {},
        "first_date": market_dates[0],
        "last_date": market_dates[-1],
        "committed_date_count": len(market_dates),
        "actual_trades_recorded": False,
        "automatic_execution_enabled": False,
    }
    write_json(staged_live / "automation" / "ae_step2_replay.json", report)
    return report


def github_workflow_health() -> dict[str, Any]:
    workflows = {}
    for name in ("engine-forward-daily.yml", "live-track-daily.yml", "update.yml"):
        base = f"https://api.github.com/repos/DonarFang/SP500-tracker/actions/workflows/{name}"
        with urllib.request.urlopen(base, timeout=20) as response:
            meta = json.load(response)
        with urllib.request.urlopen(base + "/runs?per_page=20", timeout=20) as response:
            runs = json.load(response)["workflow_runs"]
        scheduled = [item for item in runs if item.get("event") == "schedule"]
        latest = scheduled[0] if scheduled else None
        workflows[name] = {
            "state": meta.get("state"),
            "latest_scheduled_run_id": None if latest is None else latest.get("id"),
            "latest_scheduled_created_at": None if latest is None else latest.get("created_at"),
            "latest_scheduled_conclusion": None if latest is None else latest.get("conclusion"),
        }
        if meta.get("state") != "active" or latest is None or latest.get("conclusion") != "success":
            raise RuntimeError(f"Workflow health failed: {name}")
    return {
        "decision": "PASS_WORKFLOWS_ACTIVE_NOT_STOPPED",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "weekend_no_market_update_is_expected": True,
        "workflows": workflows,
    }


def replace_directory(staged: Path, target: Path, backup_root: Path) -> None:
    backup = backup_root / target.name
    if backup.exists():
        shutil.rmtree(backup)
    if target.exists():
        os.replace(target, backup)
    try:
        os.replace(staged, target)
    except Exception:
        if target.exists():
            shutil.rmtree(target)
        if backup.exists():
            os.replace(backup, target)
        raise


def append_canonical(report: Mapping[str, Any]) -> None:
    path = ROOT / "docs" / "canonical" / "FD-M3180125_ENGINE_CANONICAL_CURRENT_STATE.md"
    begin = "<!-- AE_STEP2_REPLAY_BEGIN -->"
    end = "<!-- AE_STEP2_REPLAY_END -->"
    text = path.read_text(encoding="utf-8")
    block = (
        f"{begin}\n\n## AE-step 2 — Forward / Live replay and Workflow verification\n\n"
        f"- Status: `PASS_AE_STEP2_FINAL_ACCEPTANCE`\n"
        f"- Forward: `{report['forward']['first_date']} → {report['forward']['last_date']}` from the `{SEED_DATE}` normal EOD CAPPED-ATR account state\n"
        f"- Live: `{report['live']['first_date']} → {report['live']['last_date']}` from `{LIVE_OPENING_DATE}` Opening (`USD 100,000`, empty positions)\n"
        f"- Workflows: active; latest scheduled runs successful; weekend no-update is expected\n"
        f"- Backtest rerun or rewrite: `false`\n\n{end}"
    )
    if begin in text and end in text:
        prefix = text.split(begin, 1)[0]
        suffix = text.split(end, 1)[1]
        text = prefix + block + suffix
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8")


def promote(staging: Path, report: dict[str, Any]) -> None:
    backup = staging / "backup"
    backup.mkdir()
    targets = [
        (staging / "seed", FORWARD / "seed_2026-06-16"),
        (staging / "forward_runtime", FORWARD / "runtime"),
        (staging / "live" / "runtime", LIVE / "runtime"),
        (staging / "live" / "automation", LIVE / "automation"),
    ]
    completed: list[tuple[Path, Path]] = []
    try:
        for index, (source, target) in enumerate(targets):
            slot = backup / f"{index}_{target.name}"
            if target.exists():
                os.replace(target, slot)
            os.replace(source, target)
            completed.append((target, slot))
    except Exception:
        for target, slot in reversed(completed):
            if target.exists():
                shutil.rmtree(target)
            if slot.exists():
                os.replace(slot, target)
        raise
    write_json(FORWARD / "current_seed_manifest.json", load_json(
        FORWARD / "seed_2026-06-16" / "current_manifest.json"
    ))
    write_json(FORWARD / "automation" / "ae_step2_replay.json", report["forward"])
    report_json = ROOT / "docs" / "research" / "FD-M3180125_AE_STEP2_REPLAY_REPORT.json"
    write_json(report_json, report)
    md = (
        "# FD-M3180125 — AE-step 2 Replay Report\n\n"
        "```text\nSTATUS: PASS_AE_STEP2_FINAL_ACCEPTANCE\n"
        f"FORWARD: {report['forward']['first_date']} -> {report['forward']['last_date']}\n"
        f"LIVE: {report['live']['first_date']} -> {report['live']['last_date']}\n"
        "WORKFLOWS: ACTIVE / LATEST SCHEDULED RUNS SUCCESS\n"
        "CANONICAL 5Y MODIFIED: FALSE\n```\n"
    )
    (ROOT / "docs" / "research" / "FD-M3180125_AE_STEP2_REPLAY_REPORT.md").write_text(
        md, encoding="utf-8"
    )
    append_canonical(report)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    before_5y = tree_hash(BACKTEST)
    before_result = sha256(ROOT / "exports" / "e1r_unified_5y_full_account_v1_result.json")
    source_head = git_head()
    with tempfile.TemporaryDirectory(prefix=".ae_step2_", dir=ROOT) as name:
        staging = Path(name)
        seed = staging / "seed"
        forward_runtime = staging / "forward_runtime"
        build_forward_seed(seed, source_head)
        forward = replay_forward(seed, forward_runtime, source_head)
        live = replay_live(staging / "live")
        workflow = github_workflow_health()
        report = {
            "decision": "PASS_AE_STEP2_FINAL_ACCEPTANCE",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_commit": source_head,
            "strategy_variant": VARIANT_ID,
            "canonical_result_sha256": EXPECTED_RESULT_SHA,
            "forward": forward,
            "live": live,
            "workflow": workflow,
            "isolation": {
                "canonical_5y_rerun": False,
                "canonical_5y_modified": False,
                "forward_live_shared_runtime_state": False,
                "dashboard_modified": False,
            },
        }
        if tree_hash(BACKTEST) != before_5y or sha256(
            ROOT / "exports" / "e1r_unified_5y_full_account_v1_result.json"
        ) != before_result:
            raise RuntimeError("AE-step 2 changed Canonical 5Y evidence")
        if args.write:
            promote(staging, report)
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
