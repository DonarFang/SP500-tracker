#!/usr/bin/env python3
"""
Independent canonical Engine Forward daily entrypoint.

This runner is deliberately separate from the legacy GitHub Forward/OOS
system. It writes only:
- data/fw_prices/*
- exports/official/FD-M3180125-SP500-TOP3-engine/forward/*

It never reads or writes legacy Forward/OOS state or the legacy equity curve.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import inspect
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from e1r_engine.core import E1RCoreEngine
from e1r_engine.forward_orchestrator import ForwardStrategyInputBuilder
from e1r_engine.forward_production_composition import (
    build_production_forward_composition,
)

ROOT = Path(__file__).resolve().parents[1]
ENGINE_ID = "FD-M3180125-SP500-TOP3-engine"
FORWARD_ROOT = ROOT / "exports" / "official" / ENGINE_ID / "forward"
SEED_ROOT = FORWARD_ROOT / "seed_2026-06-16"
RUNTIME_ROOT = FORWARD_ROOT / "runtime"
SOURCE_PRICE_ROOT = ROOT / "data" / "prices"
FORWARD_PRICE_ROOT = ROOT / "data" / "fw_prices"
AUTOMATION_ROOT = FORWARD_ROOT / "automation"
STATUS_PATH = AUTOMATION_ROOT / "current_run.json"

INDEX_NAMES = {
    "_GSPC": "SPX",
    "_NDX": "NDX",
    "_SOX": "SOX",
}

EXCLUDED_UNIVERSE = {
    "SPX", "NDX", "SOX", "VIX",
    "_GSPC", "_NDX", "_SOX", "_VIX",
    "GSPC", "^GSPC", "^NDX", "^SOX", "^VIX",
    "QQQ", "SOXX", "VIXY",
}

LEGACY_ROOTS = (
    ROOT / "data" / "oos",
    ROOT / "exports" / "oos",
)
LEGACY_TEXT_TOKENS = (
    "data/oos",
    "exports/oos_",
    "exports/e1r_v0_2_",
)


class ProviderShouldNotBeCalled:
    def __call__(self, *args: Any, **kwargs: Any) -> Mapping[str, str]:
        raise RuntimeError(
            "FORWARD_SIDE_MANAGEMENT_PROVIDER_CALLED:"
            "no policy may be synthesized outside E1RCoreEngine"
        )


def jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {
            field.name: jsonable(getattr(value, field.name))
            for field in dataclasses.fields(value)
        }
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Mapping):
        return {str(key): jsonable(child) for key, child in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [jsonable(child) for child in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if hasattr(value, "__dict__"):
        return {
            str(key): jsonable(child)
            for key, child in vars(value).items()
            if not str(key).startswith("_")
        }
    return str(value)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            jsonable(value),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def legacy_snapshot() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    candidates = [
        ROOT / "data" / "oos",
        ROOT / "exports",
    ]
    for root in candidates:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            relative = str(path.relative_to(ROOT))
            if (
                relative.startswith("data/oos/")
                or relative.startswith("exports/oos_")
                or relative.startswith("exports/e1r_v0_2_")
            ):
                records.append({
                    "path": relative,
                    "sha256": sha256(path),
                    "size_bytes": path.stat().st_size,
                })
    return {"files": records}


def inspect_forward_prices() -> dict[str, Any]:
    if not FORWARD_PRICE_ROOT.is_dir():
        raise RuntimeError(
            f"Missing Engine price root: {FORWARD_PRICE_ROOT}"
        )

    files = sorted(FORWARD_PRICE_ROOT.glob("*.json"))
    if not files:
        raise RuntimeError(
            "No Engine JSON files under data/fw_prices"
        )

    required = {
        "SPX": FORWARD_PRICE_ROOT / "_GSPC.json",
        "NDX": FORWARD_PRICE_ROOT / "_NDX.json",
        "SOX": FORWARD_PRICE_ROOT / "_SOX.json",
    }
    missing = [
        name
        for name, file_path in required.items()
        if not file_path.is_file()
    ]
    if missing:
        raise RuntimeError(
            f"Missing required Engine indices: {missing}"
        )

    latest_dates = {}
    for name, file_path in required.items():
        payload = json.loads(
            file_path.read_text(encoding="utf-8")
        )
        if not isinstance(payload, list) or not payload:
            raise RuntimeError(
                f"Empty Engine index file: {file_path}"
            )
        latest_dates[name] = str(payload[-1]["date"])

    return {
        "mode": "ENGINE_OWNED_FW_PRICES",
        "price_root": "data/fw_prices",
        "legacy_price_root_read": False,
        "legacy_price_root_written": False,
        "source_file_count": len(files),
        "required_index_latest_dates": latest_dates,
        "latest_required_index_date": min(
            latest_dates.values()
        ),
    }

def build_composition(runtime_commit: str, shadow_observer=None):
    price_files: dict[str, Path] = {}
    for path in sorted(FORWARD_PRICE_ROOT.glob("*.json")):
        symbol = path.stem.upper()
        price_files[symbol] = path
        canonical = INDEX_NAMES.get(symbol)
        if canonical is not None:
            price_files[canonical] = path

    for required in ("SPX", "NDX", "SOX"):
        if required not in price_files:
            raise RuntimeError(f"Missing required index {required}")

    universe = tuple(
        sorted(
            symbol
            for symbol in price_files
            if symbol not in EXCLUDED_UNIVERSE
        )
    )

    signature = inspect.signature(ForwardStrategyInputBuilder)
    if "engine" not in signature.parameters:
        raise RuntimeError(
            "ForwardStrategyInputBuilder no longer exposes Engine ownership"
        )

    strategy_builder = ForwardStrategyInputBuilder(
        engine=E1RCoreEngine(),
        management_action_provider=ProviderShouldNotBeCalled(),
    )

    composition = build_production_forward_composition(
        seed_root=SEED_ROOT,
        runtime_root=RUNTIME_ROOT,
        price_files_by_symbol=price_files,
        universe=universe,
        strategy_input_builder=strategy_builder,
        runtime_commit_provider=lambda: runtime_commit,
    )
    composition.runner.shadow_observer = shadow_observer
    from e1r_engine.universe_versioning.production_integration import (
        ProductionUniverseGate,
    )
    production_gate = ProductionUniverseGate(ROOT, "forward")
    if production_gate.mode() == "ENFORCE":
        composition.runner.production_universe_gate = production_gate.resolve
    return composition


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--uv-shadow-probe", action="store_true")
    parser.add_argument(
        "--uv-shadow-activation-time",
        default="2026-08-10T00:00:00Z",
    )
    args = parser.parse_args()

    price_sync = inspect_forward_prices()

    runtime_commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
    ).strip()

    shadow_observer = None
    if args.uv_shadow_probe:
        from e1r_engine.universe_versioning.shadow_integration import (
            ShadowObserverConfig,
            UniverseShadowObserver,
        )

        observer = UniverseShadowObserver(
            ShadowObserverConfig(
                repo_root=ROOT,
                track="forward",
                authority_head=runtime_commit,
                activation_time=args.uv_shadow_activation_time,
            )
        )

        def shadow_observer(**kwargs):
            return observer.observe(
                **kwargs,
                protected_paths=(FORWARD_PRICE_ROOT, RUNTIME_ROOT),
            )

    composition = build_composition(runtime_commit, shadow_observer)
    seed = composition.seed_loader.load()
    current = composition.repository.load()

    if args.uv_shadow_probe:
        reports = list(composition.runner.run_shadow_probe())
        if not reports:
            raise RuntimeError(
                "HOLD_UV_STEP_3_FORWARD_SHADOW: no planned execution dates"
            )
        print(json.dumps({
            "decision": "PASS_UV_STEP_3_FORWARD_SHADOW_PROBE",
            "track": "forward",
            "authority_head": runtime_commit,
            "planned_dates": [row["expected_execution_date"] for row in reports],
            "reports": reports,
            "production_runs_performed": False,
            "production_data_updated": False,
            "production_membership_activated": False,
            "production_side_effect_calls": [],
        }, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    before_legacy = legacy_snapshot()
    dry_run = composition.runner.dry_run()
    planned_dates = list(dry_run.planned_dates)

    common = {
        "engine_id": ENGINE_ID,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "CHECK" if args.check else "OFFICIAL_WRITE",
        "runtime_commit": runtime_commit,
        "price_sync": price_sync,
        "seed_date": seed.seed_date,
        "first_forward_market_date": seed.first_forward_market_date,
        "last_committed_date_before": current.last_committed_date,
        "planned_dates": planned_dates,
        "dry_run_status": dry_run.status,
        "dry_run_repository_initialized": (
            dry_run.repository_initialized
        ),
        "dry_run_commit_day_called": dry_run.commit_day_called,
        "dry_run_forward_state_mutated": (
            dry_run.forward_state_mutated
        ),
        "dry_run_official_artifacts_written": (
            dry_run.official_artifacts_written
        ),
        "legacy_forward_used": False,
        "legacy_equity_curve_used": False,
        "engine_equity_curve": str(
            (RUNTIME_ROOT / "history" / "equity_curve.json").relative_to(ROOT)
        ),
    }

    if args.check:
        if dry_run.status != "PASS_FORWARD_ORCHESTRATOR_DRY_RUN":
            raise RuntimeError(
                f"Unexpected dry-run status: {dry_run.status}"
            )
        if (
            dry_run.repository_initialized
            or dry_run.commit_day_called
            or dry_run.forward_state_mutated
            or dry_run.official_artifacts_written
        ):
            raise RuntimeError("Dry-run violated no-write contract")
        after_legacy = legacy_snapshot()
        if before_legacy != after_legacy:
            raise RuntimeError("Check mode changed legacy Forward artifacts")
        print(json.dumps(common, ensure_ascii=False, indent=2))
        return 0

    results = list(composition.runner.run(allow_official_write=True))
    final_state = composition.repository.load()
    final_state.validate()

    non_committed = [
        jsonable(result)
        for result in results
        if str(getattr(result, "status", "")) != "COMMITTED"
    ]
    if non_committed:
        raise RuntimeError(
            "Engine Forward produced non-COMMITTED results: "
            + json.dumps(non_committed, ensure_ascii=False)
        )

    curve_path = RUNTIME_ROOT / "history" / "equity_curve.json"
    curve = json.loads(curve_path.read_text(encoding="utf-8"))
    if not isinstance(curve, list) or not curve:
        raise RuntimeError("Engine Forward equity curve is empty")
    if curve[-1].get("date") != final_state.last_committed_date:
        raise RuntimeError("Engine equity curve/runtime date mismatch")

    after_legacy = legacy_snapshot()
    if before_legacy != after_legacy:
        raise RuntimeError(
            "Engine Forward run changed legacy Forward/OOS artifacts"
        )

    status = {
        **common,
        "decision": "PASS_INDEPENDENT_ENGINE_FORWARD_DAILY_UPDATE",
        "result_count": len(results),
        "committed_dates": [
            str(getattr(result, "trading_date", ""))
            for result in results
        ],
        "last_committed_date_after": final_state.last_committed_date,
        "final_account_date": final_state.account.date,
        "final_equity": final_state.account.total_equity,
        "engine_equity_curve_point_count": len(curve),
        "engine_equity_curve_last_date": curve[-1].get("date"),
        "legacy_forward_changed": False,
        "legacy_equity_curve_changed": False,
    }
    write_json(STATUS_PATH, status)
    print(json.dumps(status, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        failure = {
            "decision": "FAIL_INDEPENDENT_ENGINE_FORWARD_DAILY_UPDATE",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "error": repr(exc),
            "legacy_forward_used": False,
            "legacy_equity_curve_used": False,
        }
        write_json(STATUS_PATH, failure)
        print(json.dumps(failure, ensure_ascii=False, indent=2))
        raise
