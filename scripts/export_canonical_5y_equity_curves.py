#!/usr/bin/env python3
"""
Export-only wrapper for canonical 5Y equity curves.

Stage 3.8E-2F-2C-4C-5:
- inspect mode: inspect available composer/backtest utilities and source artifacts
- smoke mode: run tiny in-memory tests only
- no final exports are written unless a future stage explicitly enables export mode

This script must not modify frozen strategy files.
"""

from __future__ import annotations

import argparse
import inspect
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Sequence


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


REPORT_PATH = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C5_EXPORT_WRAPPER_SMOKE_REPORT.json"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path, default: Any = None) -> Any:
    if default is None:
        default = {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def safe_len(value: Any) -> int | None:
    try:
        return len(value)
    except Exception:
        return None


def summarize_json(path: Path) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "path": str(path.relative_to(ROOT)) if path.exists() else str(path.relative_to(ROOT)),
        "exists": path.exists(),
    }
    if not path.exists():
        return out

    obj = read_json(path, default={"__error__": "json_read_failed"})
    if isinstance(obj, dict) and "__error__" in obj:
        out["json_valid"] = False
        out["error"] = obj["__error__"]
        return out

    out["json_valid"] = True
    out["type"] = type(obj).__name__
    if isinstance(obj, dict):
        out["top_keys"] = sorted(obj.keys())
        lists = {}
        for k, v in obj.items():
            if isinstance(v, list):
                sample = v[-1] if v else None
                lists[k] = {
                    "length": len(v),
                    "last_type": type(sample).__name__ if sample is not None else None,
                    "last_keys": sorted(sample.keys()) if isinstance(sample, dict) else None,
                }
        out["lists"] = lists
        metrics = {}
        for k in [
            "strategy_id",
            "variant",
            "variant_id",
            "total_return_pct",
            "spx_return_pct",
            "alpha_pct",
            "max_drawdown_pct",
            "profit_factor",
            "sharpe",
            "sharpe_ratio",
            "final_equity",
            "initial_capital",
        ]:
            if k in obj:
                metrics[k] = obj[k]
        if isinstance(obj.get("sample_validity"), dict):
            metrics["sample_validity"] = obj["sample_validity"]
        out["metrics"] = metrics
    elif isinstance(obj, list):
        out["length"] = len(obj)
        sample = obj[-1] if obj else None
        out["last_type"] = type(sample).__name__ if sample is not None else None
        out["last_keys"] = sorted(sample.keys()) if isinstance(sample, dict) else None

    return out


def import_composer() -> Dict[str, Any]:
    result: Dict[str, Any] = {"ok": False}
    try:
        from src.engine import e1r_composer as composer  # type: ignore

        result["ok"] = True
        result["module"] = "src.engine.e1r_composer"
        result["functions"] = {}
        for name in [
            "build_equity_records_from_returns",
            "extract_core_interval_returns",
            "compound_return",
            "max_drawdown",
            "sharpe_ratio",
            "profit_factor",
        ]:
            fn = getattr(composer, name, None)
            if fn is None:
                result["functions"][name] = {"exists": False}
                continue
            result["functions"][name] = {
                "exists": True,
                "signature": str(inspect.signature(fn)),
                "source_head": "\n".join(inspect.getsource(fn).splitlines()[:40]),
            }
        result["_module_obj"] = composer
    except Exception as exc:
        result["ok"] = False
        result["error"] = type(exc).__name__ + ": " + str(exc)
    return result


def run_build_equity_smoke(composer: Any) -> Dict[str, Any]:
    fn = getattr(composer, "build_equity_records_from_returns", None)
    if fn is None:
        return {"ok": False, "error": "build_equity_records_from_returns not found"}

    attempts = []

    candidate_sets = [
        {
            "name": "daily_return_pct",
            "records": [
                {"date": "2021-06-11", "daily_return_pct": 0.0},
                {"date": "2021-06-14", "daily_return_pct": 1.0},
                {"date": "2021-06-15", "daily_return_pct": -0.5},
            ],
        },
        {
            "name": "daily_return_decimal",
            "records": [
                {"date": "2021-06-11", "daily_return": 0.0},
                {"date": "2021-06-14", "daily_return": 0.01},
                {"date": "2021-06-15", "daily_return": -0.005},
            ],
        },
        {
            "name": "return_pct",
            "records": [
                {"date": "2021-06-11", "return_pct": 0.0},
                {"date": "2021-06-14", "return_pct": 1.0},
                {"date": "2021-06-15", "return_pct": -0.5},
            ],
        },
        {
            "name": "interval_return",
            "records": [
                {"start_date": "2021-06-11", "end_date": "2021-06-14", "interval_return": 0.01},
                {"start_date": "2021-06-14", "end_date": "2021-06-15", "interval_return": -0.005},
            ],
        },
        {
            "name": "strategy_return",
            "records": [
                {"date": "2021-06-11", "strategy_return": 0.0},
                {"date": "2021-06-14", "strategy_return": 0.01},
                {"date": "2021-06-15", "strategy_return": -0.005},
            ],
        },
    ]

    for candidate in candidate_sets:
        try:
            res = fn(candidate["records"], 100000.0)
            attempts.append({
                "name": candidate["name"],
                "ok": True,
                "type": type(res).__name__,
                "length": safe_len(res),
                "sample": res[:5] if isinstance(res, list) else str(res)[:500],
            })
        except Exception as exc:
            attempts.append({
                "name": candidate["name"],
                "ok": False,
                "error": type(exc).__name__ + ": " + str(exc),
            })

    return {
        "ok": any(a.get("ok") for a in attempts),
        "attempts": attempts,
    }


def inspect_mode() -> Dict[str, Any]:
    composer_result = import_composer()
    composer_clean = {k: v for k, v in composer_result.items() if k != "_module_obj"}

    source_files = [
        ROOT / "data/research/e1r/e1r_formal_backtest_v0_1.json",
        ROOT / "exports/portfolio_backtest.json",
        ROOT / "exports/e1r_v0_2_backtest_summary.json",
        ROOT / "exports/e1r_v0_2_backtest_equity_curve.json",
        ROOT / "exports/oos_e1r_v0_2_equity_curve.json",
        ROOT / "exports/oos_equity_curve.json",
        ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json",
        ROOT / "data/research/e1_5y/raw/indices/SPX.json",
    ]

    return {
        "composer": composer_clean,
        "source_files": [summarize_json(p) for p in source_files],
    }


def smoke_mode() -> Dict[str, Any]:
    composer_result = import_composer()
    composer = composer_result.get("_module_obj")
    if composer is None:
        return {
            "composer_import_ok": False,
            "error": composer_result.get("error", "composer import failed"),
        }

    build_smoke = run_build_equity_smoke(composer)

    # Metric utility smoke tests.
    utility_smoke: Dict[str, Any] = {}
    for name, args in [
        ("compound_return", ([0.01, -0.005, 0.02],)),
        ("max_drawdown", ([100.0, 105.0, 101.0, 110.0],)),
        ("sharpe_ratio", ([0.01, -0.005, 0.02],)),
        ("profit_factor", ([0.01, -0.005, 0.02],)),
    ]:
        fn = getattr(composer, name, None)
        if fn is None:
            utility_smoke[name] = {"ok": False, "error": "missing"}
            continue
        try:
            value = fn(*args)
            utility_smoke[name] = {"ok": True, "value": value}
        except Exception as exc:
            utility_smoke[name] = {
                "ok": False,
                "error": type(exc).__name__ + ": " + str(exc),
            }

    return {
        "composer_import_ok": True,
        "build_equity_records_from_returns": build_smoke,
        "utility_functions": utility_smoke,
    }



def load_existing_5y_generation_inputs() -> Dict[str, Any]:
    """
    Dry-run only.

    This function intentionally does not write canonical exports.
    It inspects whether the current repository has enough persisted inputs
    to generate E1R 5Y interval records:
      core_daily_equity_records + sidecar_records
      -> extract_core_interval_returns(...)
      -> build_equity_records_from_returns(...)
    """
    from src.engine import e1r_composer as composer  # type: ignore

    source_summary: Dict[str, Any] = {
        "core_sources": [],
        "sidecar_sources": [],
        "interval_sources": [],
    }

    def list_shape(label: str, rows: Any) -> Dict[str, Any]:
        if not isinstance(rows, list):
            return {"label": label, "is_list": False}
        keys = set()
        for row in rows[:50]:
            if isinstance(row, dict):
                keys.update(row.keys())
        return {
            "label": label,
            "is_list": True,
            "length": len(rows),
            "keys": sorted(keys),
            "has_core_minimum": (
                "date" in keys and (
                    "daily_return" in keys
                    or "daily_return_pct" in keys
                    or "total_equity" in keys
                    or "equity" in keys
                )
            ),
            "has_sidecar_minimum": (
                "date" in keys
                and "next_date" in keys
                and (
                    "sidecar_return" in keys
                    or "sidecar_return_pct" in keys
                )
            ),
            "has_interval_minimum": (
                "date" in keys
                and "next_date" in keys
                and "combined_return" in keys
            ),
        }

    def append_if_list(bucket: str, label: str, rows: Any) -> None:
        shape = list_shape(label, rows)
        if shape.get("is_list"):
            source_summary[bucket].append(shape)

    portfolio = read_json(ROOT / "exports/portfolio_backtest.json", default={})
    append_if_list("core_sources", "exports/portfolio_backtest.json.daily_records", portfolio.get("daily_records"))
    variant_results = portfolio.get("variant_results") if isinstance(portfolio, dict) else {}
    if isinstance(variant_results, dict):
        for variant, obj in variant_results.items():
            if isinstance(obj, dict):
                append_if_list("core_sources", f"exports/portfolio_backtest.json.variant_results.{variant}.daily_records", obj.get("daily_records"))

    oos_e1 = read_json(ROOT / "exports/oos_equity_curve.json", default={})
    if isinstance(oos_e1, dict):
        append_if_list("core_sources", "exports/oos_equity_curve.json.curve", oos_e1.get("curve"))

    e1r_diag = read_json(ROOT / "exports/e1r_v0_2_backtest_equity_curve.json", default={})
    if isinstance(e1r_diag, dict):
        append_if_list("core_sources", "exports/e1r_v0_2_backtest_equity_curve.json.rows", e1r_diag.get("rows"))
        append_if_list("core_sources", "exports/e1r_v0_2_backtest_equity_curve.json.equity_curve", e1r_diag.get("equity_curve"))

    sidecar = read_json(ROOT / "exports/oos_e1r_v0_2_sidecar.json", default={})
    if isinstance(sidecar, dict):
        for k, v in sidecar.items():
            append_if_list("sidecar_sources", f"exports/oos_e1r_v0_2_sidecar.json.{k}", v)
    elif isinstance(sidecar, list):
        append_if_list("sidecar_sources", "exports/oos_e1r_v0_2_sidecar.json.root", sidecar)

    # Try only persisted candidates. This is expected to fail or produce zero intervals
    # unless real 5Y sidecar records have been persisted.
    attempts: list[dict[str, Any]] = []

    core_candidates = [
        x for x in source_summary["core_sources"]
        if x.get("has_core_minimum")
    ]
    sidecar_candidates = [
        x for x in source_summary["sidecar_sources"]
        if x.get("has_sidecar_minimum")
    ]

    def resolve_rows(label: str) -> Any:
        if label == "exports/portfolio_backtest.json.daily_records":
            return portfolio.get("daily_records")
        if label.startswith("exports/portfolio_backtest.json.variant_results."):
            parts = label.split(".")
            variant = parts[3]
            return variant_results.get(variant, {}).get("daily_records")
        if label == "exports/oos_equity_curve.json.curve":
            return oos_e1.get("curve")
        if label == "exports/e1r_v0_2_backtest_equity_curve.json.rows":
            return e1r_diag.get("rows")
        if label == "exports/e1r_v0_2_backtest_equity_curve.json.equity_curve":
            return e1r_diag.get("equity_curve")
        if label.startswith("exports/oos_e1r_v0_2_sidecar.json."):
            key = label.split(".")[-1]
            return sidecar.get(key) if isinstance(sidecar, dict) else sidecar
        return []

    for core in core_candidates:
        for side in sidecar_candidates:
            core_rows = resolve_rows(core["label"])
            side_rows = resolve_rows(side["label"])
            try:
                interval_records = composer.extract_core_interval_returns(core_rows, side_rows)
                equity_records = composer.build_equity_records_from_returns(interval_records, 100000.0) if interval_records else []
                attempts.append({
                    "core_source": core["label"],
                    "sidecar_source": side["label"],
                    "ok": True,
                    "interval_count": len(interval_records),
                    "equity_count": len(equity_records),
                    "first_interval": interval_records[0] if interval_records else None,
                    "last_interval": interval_records[-1] if interval_records else None,
                    "first_equity": equity_records[0] if equity_records else None,
                    "last_equity": equity_records[-1] if equity_records else None,
                })
            except Exception as exc:
                attempts.append({
                    "core_source": core["label"],
                    "sidecar_source": side["label"],
                    "ok": False,
                    "error": type(exc).__name__ + ": " + str(exc),
                })

    source_summary["attempts"] = attempts
    source_summary["can_generate_from_persisted_inputs"] = any(
        a.get("ok") and a.get("interval_count", 0) > 0 and a.get("equity_count", 0) > 0
        for a in attempts
    )

    frozen_summary = read_json(ROOT / "exports/e1r_v0_2_backtest_summary.json", default={})
    source_summary["frozen_metric_targets"] = {
        "total_return_pct": frozen_summary.get("total_return_pct"),
        "spx_return_pct": frozen_summary.get("spx_return_pct"),
        "alpha_pct": frozen_summary.get("alpha_pct"),
        "max_drawdown_pct": frozen_summary.get("max_drawdown_pct"),
        "profit_factor": frozen_summary.get("profit_factor"),
        "sharpe_ratio": frozen_summary.get("sharpe_ratio"),
    }

    source_summary["decision"] = (
        "PERSISTED_INPUTS_SUFFICIENT"
        if source_summary["can_generate_from_persisted_inputs"]
        else "PERSISTED_INPUTS_INSUFFICIENT_NEED_FROZEN_GENERATOR_DRY_RUN"
    )

    return source_summary


def dry_run_generate_intervals_mode() -> Dict[str, Any]:
    result = load_existing_5y_generation_inputs()

    return {
        "status": "DRY_RUN_GENERATE_INTERVALS_COMPLETE_NO_CANONICAL_EXPORTS_WRITTEN",
        "policy": {
            "dashboard_changed": False,
            "exports_changed": False,
            "workflow_changed": False,
            "strategy_logic_changed": False,
            "canonical_exports_written": False,
            "long_backtest_run": False,
        },
        "result": result,
        "next_stage": {
            "name": "Stage 3.8E-2F-2C-4C-9",
            "title": "Implement frozen generator dry-run or run controlled long backtest export",
            "condition": "If persisted inputs are insufficient, call frozen generator path to produce interval records in dry-run memory first.",
        },
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inspect", action="store_true", help="Inspect composer/functions/source JSONs.")
    parser.add_argument("--smoke", action="store_true", help="Run tiny in-memory smoke tests only.")
    parser.add_argument("--write-report", action="store_true", help="Write smoke report under docs/research.")
    parser.add_argument("--dry-run-generate-intervals", action="store_true", help="Dry-run interval generation from persisted inputs; write no canonical exports.")
    args = parser.parse_args()

    if not args.inspect and not args.smoke and not args.dry_run_generate_intervals:
        args.inspect = True
        args.smoke = True

    report: Dict[str, Any] = {
        "generated_at": utc_now_iso(),
        "stage": "B_STAGE_3_8E2F2C4C5_EXPORT_WRAPPER_SMOKE",
        "status": "SMOKE_COMPLETE_NO_CANONICAL_EXPORTS_WRITTEN",
        "policy": {
            "dashboard_changed": False,
            "exports_changed": False,
            "workflow_changed": False,
            "strategy_logic_changed": False,
            "canonical_exports_written": False,
            "long_backtest_run": False,
        },
        "wrapper": {
            "path": "scripts/export_canonical_5y_equity_curves.py",
            "modes": ["--inspect", "--smoke", "--write-report"],
            "future_canonical_outputs": [
                "exports/e1_5y_backtest_equity_curve.json",
                "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
                "exports/e1_e1r_5y_equity_comparison.json",
            ],
        },
    }

    if args.inspect:
        report["inspect"] = inspect_mode()
    if args.smoke:
        report["smoke"] = smoke_mode()
    if args.dry_run_generate_intervals:
        report["dry_run_generate_intervals"] = dry_run_generate_intervals_mode()

    # Decision summary.
    smoke = report.get("smoke", {})
    build = smoke.get("build_equity_records_from_returns", {}) if isinstance(smoke, dict) else {}
    attempts = build.get("attempts", []) if isinstance(build, dict) else []
    ok_attempts = [a for a in attempts if a.get("ok")]

    dry = report.get("dry_run_generate_intervals", {})
    dry_result = dry.get("result", {}) if isinstance(dry, dict) else {}
    dry_decision = dry_result.get("decision")

    report["diagnosis"] = [
        "Wrapper imports e1r_composer and inspects source JSONs without writing canonical exports.",
        f"build_equity_records_from_returns smoke success attempts: {len(ok_attempts)}.",
        f"dry_run_generate_intervals decision: {dry_decision}.",
        "If persisted inputs are insufficient, next stage should call frozen generator path or controlled long backtest export.",
        "Long backtest remains allowed only after dry-run validates call shape and export schema.",
    ]

    report["next_stage"] = {
        "name": "Stage 3.8E-2F-2C-4C-6",
        "title": "Implement canonical 5Y equity export mode or inspect exact composer field names",
        "condition": "Proceed to export mode only if smoke identifies a valid interval record shape; otherwise inspect composer source lines.",
    }

    if args.write_report:
        write_json(REPORT_PATH, report)

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
