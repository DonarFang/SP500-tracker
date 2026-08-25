#!/usr/bin/env python3
"""Deterministically rebuild only the canonical Forward runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Mapping

from e1r_engine.core import E1RCoreEngine
from e1r_engine.forward_orchestrator import ForwardStrategyInputBuilder
from e1r_engine.forward_production_composition import (
    build_production_forward_composition,
)
from e1r_engine.forward_runtime import ForwardMarketDataAdapter


ROOT = Path(__file__).resolve().parents[1]
ENGINE_ID = "FD-M3180125-SP500-TOP3-engine"
FORWARD = ROOT / "exports" / "official" / ENGINE_ID / "forward"
SEED = FORWARD / "seed_2026-06-16"
FIRST_FORWARD_DATE = "2026-06-17"
SEED_DATE = "2026-06-16"
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


def tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


class ProviderShouldNotBeCalled:
    def __call__(self, *args: Any, **kwargs: Any) -> Mapping[str, str]:
        del args, kwargs
        raise RuntimeError("policy synthesis outside E1RCoreEngine is prohibited")


def build_composition(runtime_root: Path, runtime_commit: str):
    price_files: dict[str, Path] = {}
    aliases = {"_GSPC": "SPX", "_NDX": "NDX", "_SOX": "SOX"}
    for path in sorted((ROOT / "data" / "fw_prices").glob("*.json")):
        symbol = path.stem.upper()
        price_files[symbol] = path
        if symbol in aliases:
            price_files[aliases[symbol]] = path
    universe = tuple(
        sorted(symbol for symbol in price_files if symbol not in EXCLUDED)
    )
    builder = ForwardStrategyInputBuilder(
        engine=E1RCoreEngine(),
        management_action_provider=ProviderShouldNotBeCalled(),
    )
    composition = build_production_forward_composition(
        seed_root=SEED,
        runtime_root=runtime_root,
        price_files_by_symbol=price_files,
        universe=universe,
        strategy_input_builder=builder,
        runtime_commit_provider=lambda: runtime_commit,
    )
    from e1r_engine.universe_versioning.production_integration import (
        ProductionUniverseGate,
    )
    production_gate = ProductionUniverseGate(ROOT, "forward")
    if production_gate.mode() == "ENFORCE":
        composition.runner.production_universe_gate = production_gate.resolve
    return composition


def validate_seed() -> dict[str, Any]:
    state = load_json(SEED / "forward_runtime_seed_state.json")
    boundary = state.get("seed_boundary") or {}
    if boundary.get("seed_date") != SEED_DATE:
        raise RuntimeError("Forward seed date mismatch")
    if boundary.get("first_forward_market_date") != FIRST_FORWARD_DATE:
        raise RuntimeError("Forward first market date mismatch")
    if state.get("sim_end_replayed") is not False:
        raise RuntimeError("Forward seed must not replay SIM_END")
    positions = state.get("account", {}).get("positions") or []
    symbols = sorted(str(item["symbol"]) for item in positions)
    if symbols != ["DELL", "HUM", "MRVL"]:
        raise RuntimeError(f"Forward seed positions mismatch: {symbols}")
    return {
        "seed_date": SEED_DATE,
        "first_forward_market_date": FIRST_FORWARD_DATE,
        "position_symbols": symbols,
        "seed_state_sha256": sha256(SEED / "forward_runtime_seed_state.json"),
    }


def replay(runtime_root: Path, runtime_commit: str) -> dict[str, Any]:
    if runtime_root.exists() and any(runtime_root.iterdir()):
        raise RuntimeError(f"output root must be absent or empty: {runtime_root}")
    runtime_root.mkdir(parents=True, exist_ok=True)
    seed = validate_seed()
    composition = build_composition(runtime_root, runtime_commit)
    dry_run = composition.runner.dry_run()
    planned_dates = list(dry_run.planned_dates)
    if not planned_dates or planned_dates[0] != FIRST_FORWARD_DATE:
        raise RuntimeError("Forward replay did not begin on 2026-06-17")
    results = list(composition.runner.run(allow_official_write=True))
    committed_dates = [item.trading_date for item in results]
    if committed_dates != planned_dates:
        raise RuntimeError("Forward committed dates do not match dry-run plan")

    state = composition.repository.load()
    state.validate()
    curve = load_json(runtime_root / "history" / "equity_curve.json")
    curve_dates = [str(item["date"]) for item in curve]
    daily_dates = sorted(
        item.name for item in (runtime_root / "daily").iterdir()
        if item.is_dir()
    )
    if curve_dates != planned_dates or daily_dates != planned_dates:
        raise RuntimeError("Forward curve/daily date sequence mismatch")
    if len(set(curve_dates)) != len(curve_dates):
        raise RuntimeError("Forward equity curve contains duplicate dates")
    executable_artifacts = list((runtime_root / "daily").glob("*/fills.json"))
    executable_artifacts += list(
        (runtime_root / "daily").glob("*/order_intents.json")
    )
    executable_artifacts += list(
        (runtime_root / "daily").glob("*/execution.json")
    )
    executable_artifacts.append(runtime_root / "history" / "orders.jsonl")
    if any(
        "SIM_END" in path.read_text(encoding="utf-8")
        for path in executable_artifacts
    ):
        raise RuntimeError("SIM_END is prohibited in Forward replay")

    fills_count = 0
    fill_count_by_month: dict[str, int] = {}
    fills_by_reason: dict[str, int] = {}
    intents_count = 0
    skipped_order_count = 0
    skipped_orders_by_reason: dict[str, int] = {}
    false_missing_t1_bars: list[dict[str, str]] = []
    for day in (runtime_root / "daily").iterdir():
        if not day.is_dir():
            continue
        day_fills = load_json(day / "fills.json")
        fills_count += len(day_fills)
        if day_fills:
            month = day.name[:7]
            fill_count_by_month[month] = (
                fill_count_by_month.get(month, 0) + len(day_fills)
            )
        for fill in day_fills:
            reason = str(fill.get("reason") or "UNKNOWN")
            fills_by_reason[reason] = fills_by_reason.get(reason, 0) + 1
        intents_count += len(load_json(day / "order_intents.json"))
        trace = load_json(day / "decision_trace.json")
        metadata = trace.get("metadata") or {}
        if metadata.get("single_step_decision") is not True:
            raise RuntimeError(f"{day.name}: not a canonical single-step decision")
        if metadata.get("external_strategy_inputs") is not False:
            raise RuntimeError(f"{day.name}: external strategy inputs detected")
        execution = load_json(day / "execution.json")
        for row in execution.get("skipped_orders", []):
            skipped_order_count += 1
            reason = str(row.get("skip_reason") or row.get("reason") or "UNKNOWN")
            skipped_orders_by_reason[reason] = (
                skipped_orders_by_reason.get(reason, 0) + 1
            )
            if reason != "MISSING_T1_BAR":
                continue
            symbol = str(row.get("symbol") or "").strip().upper()
            source_series = composition.runner.series_by_symbol.get(symbol, {})
            if symbol and day.name in source_series:
                false_missing_t1_bars.append(
                    {
                        "execution_date": day.name,
                        "signal_date": str(row.get("signal_date") or ""),
                        "symbol": symbol,
                        "intent_type": str(row.get("intent_type") or ""),
                    }
                )

    if false_missing_t1_bars:
        raise RuntimeError(
            "Forward replay dropped data-backed T+1 orders: "
            + json.dumps(false_missing_t1_bars, sort_keys=True)
        )

    pending = load_json(runtime_root / "current" / "pending_orders.json")
    orders = (runtime_root / "history" / "orders.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()
    report = {
        "status": "PASS_FORWARD_CANONICAL_FULL_INTERVAL_REPLAY",
        "runtime_commit": runtime_commit,
        "seed": seed,
        "first_date": planned_dates[0],
        "last_date": planned_dates[-1],
        "committed_date_count": len(planned_dates),
        "curve_row_count": len(curve),
        "orders_history_count": len(orders),
        "order_intent_count": intents_count,
        "fill_count": fills_count,
        "fill_count_by_month": dict(sorted(fill_count_by_month.items())),
        "fills_by_reason": dict(sorted(fills_by_reason.items())),
        "skipped_order_count": skipped_order_count,
        "skipped_orders_by_reason": dict(sorted(skipped_orders_by_reason.items())),
        "false_missing_t1_bar_count": len(false_missing_t1_bars),
        "final_equity": state.account.total_equity,
        "final_cash": state.account.cash,
        "final_positions": sorted(state.account.positions),
        "pending_order_count": len(pending),
        "sim_end_replayed": False,
        "single_engine_step": True,
        "external_strategy_inputs": False,
        "runtime_tree_sha256": tree_sha256(runtime_root),
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--runtime-commit", required=True)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    if len(args.runtime_commit) != 40 or any(
        char not in "0123456789abcdef" for char in args.runtime_commit.lower()
    ):
        raise RuntimeError("runtime commit must be a 40-character Git SHA")
    if args.runtime_commit != git_head():
        raise RuntimeError("runtime commit must equal the checked-out HEAD")
    output = args.output_root.resolve()
    official_runtime = (FORWARD / "runtime").resolve()
    if output == official_runtime or official_runtime in output.parents:
        raise RuntimeError("direct write to official Forward runtime is prohibited")
    report = replay(output, args.runtime_commit)
    write_json(args.report, report)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
