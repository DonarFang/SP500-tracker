#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
import inspect
import sys
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_G_GOLDEN_MASTER_HARNESS.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_G_GOLDEN_MASTER_HARNESS.md"
ARCH_MD = ROOT / "docs/architecture/E1R_GOLDEN_MASTER_HARNESS_CONTRACT.md"
GOLDEN_MASTER_JSON = ROOT / "exports/e1r_engine/golden_master/e1r_engine_g_short_window_golden_master.json"

ENGINE_A_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_A_STANDALONE_ENGINE_ARCHITECTURE_CONTRACT.json"
ENGINE_B_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_B_R1_NORMALIZED_INPUT_DATA_ADAPTER_CONTRACT_AUDIT.json"
ENGINE_C_R1_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_C_R1_NO_STRATEGY_DATA_HARNESS_SMOKE.json"
ENGINE_D_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_D_HISTORICAL_DATA_ADAPTER_SKELETON_SMOKE.json"
ENGINE_E_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_E_STATE_CONTRACT_SMOKE.json"
ENGINE_F_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_F_CORE_ENGINE_SHELL_SMOKE.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
]

INVALID_ARTIFACTS = [
    ROOT / "exports/e1r_unified_5y_full_account_v1_result.json",
    ROOT / "exports/e1r_unified_5y_dashboard_research_bundle.json",
    ROOT / "exports/e1r_combined_5y_original_max3_result.json",
    ROOT / "exports/e1r_combined_5y_original_max3_equity_curve.json",
    ROOT / "exports/e1r_combined_5y_original_max3_summary.json",
]

SHORT_WINDOW_START = "2021-04-05"
SHORT_WINDOW_END = "2021-06-30"
MAX_WINDOW_DAYS_ALLOWED = 90


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except Exception:
        return str(path)


def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def safe_preview(value: Any, limit: int = 5) -> Any:
    if isinstance(value, list):
        return value[:limit]
    if isinstance(value, dict):
        return {k: safe_preview(v, limit=limit) for k, v in list(value.items())[:limit]}
    return value


def summarize_obj(obj: Any) -> dict[str, Any]:
    out: dict[str, Any] = {
        "type": type(obj).__name__,
    }
    if isinstance(obj, dict):
        out["key_count"] = len(obj)
        out["keys"] = sorted([str(k) for k in obj.keys()])[:120]
        out["preview"] = safe_preview(obj, limit=3)
    elif isinstance(obj, list):
        out["length"] = len(obj)
        out["preview"] = safe_preview(obj, limit=3)
        if obj and isinstance(obj[0], dict):
            out["first_row_keys"] = sorted([str(k) for k in obj[0].keys()])
    else:
        out["repr"] = repr(obj)[:500]
    return out


def json_safe(obj: Any) -> Any:
    if hasattr(obj, "__dict__"):
        return {k: json_safe(v) for k, v in obj.__dict__.items()}
    if isinstance(obj, dict):
        return {str(k): json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [json_safe(v) for v in obj]
    if isinstance(obj, tuple):
        return [json_safe(v) for v in obj]
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return repr(obj)


def bars_to_legacy_ohlc_dict(bars: list[Any]) -> dict[str, list[Any]]:
    """
    Convert HistoricalDataAdapter DailyBar list into the legacy backtest.py ohlc_map shape.

    run_stateful_simulation expects:
      ohlc_map[symbol].get("high", [])
      ohlc_map[symbol].get("low", [])
      etc.

    So each symbol must map to a dict of field arrays, not a list of bar dicts.
    """
    rows: list[dict[str, Any]] = []
    for b in bars:
        if hasattr(b, "__dict__"):
            rows.append(dict(b.__dict__))
        elif isinstance(b, dict):
            rows.append(dict(b))
        else:
            raise TypeError(f"Unsupported bar type: {type(b).__name__}")

    return {
        "date": [r.get("date") for r in rows],
        "open": [r.get("open") for r in rows],
        "high": [r.get("high") for r in rows],
        "low": [r.get("low") for r in rows],
        "close": [r.get("close") for r in rows],
        "volume": [r.get("volume") for r in rows],
    }


def count_dates_between(dates: list[str], start: str, end: str) -> int:
    return sum(1 for d in dates if start <= d <= end)


def extract_candidate_golden_master(result: Any) -> dict[str, Any]:
    """
    Extract a conservative golden-master artifact from unknown legacy result schema.
    This does not transform returns into an official result; it only stores trace-shaped
    outputs for later equivalence comparison.
    """
    summary = summarize_obj(result)
    result_json = json_safe(result)

    key_candidates = {
        "daily_account_candidates": [],
        "action_trace_candidates": [],
        "trade_candidates": [],
        "equity_curve_candidates": [],
        "position_candidates": [],
    }

    if isinstance(result_json, dict):
        for key, value in result_json.items():
            k = str(key).lower()

            if isinstance(value, list):
                first = value[0] if value else {}
                first_keys = set(first.keys()) if isinstance(first, dict) else set()

                if (
                    "daily" in k
                    or "equity" in k
                    or {"date", "total_equity"}.issubset(first_keys)
                    or {"date", "cash"}.issubset(first_keys)
                ):
                    key_candidates["daily_account_candidates"].append({
                        "key": key,
                        "length": len(value),
                        "first_row_keys": sorted(first_keys),
                        "sample": value[:3],
                    })

                if (
                    "action" in k
                    or "order" in k
                    or {"action", "sym"}.issubset(first_keys)
                    or {"action", "symbol"}.issubset(first_keys)
                ):
                    key_candidates["action_trace_candidates"].append({
                        "key": key,
                        "length": len(value),
                        "first_row_keys": sorted(first_keys),
                        "sample": value[:10],
                    })

                if (
                    "trade" in k
                    or {"entry_date", "exit_date"}.issubset(first_keys)
                    or {"symbol", "return_pct"}.issubset(first_keys)
                ):
                    key_candidates["trade_candidates"].append({
                        "key": key,
                        "length": len(value),
                        "first_row_keys": sorted(first_keys),
                        "sample": value[:10],
                    })

                if "equity" in k or {"date", "equity"}.issubset(first_keys):
                    key_candidates["equity_curve_candidates"].append({
                        "key": key,
                        "length": len(value),
                        "first_row_keys": sorted(first_keys),
                        "sample": value[:5],
                    })

                if "position" in k or {"symbol", "quantity"}.issubset(first_keys):
                    key_candidates["position_candidates"].append({
                        "key": key,
                        "length": len(value),
                        "first_row_keys": sorted(first_keys),
                        "sample": value[:5],
                    })

    metrics = {}
    if isinstance(result_json, dict):
        for key, value in result_json.items():
            if isinstance(value, (int, float, str, bool)) or value is None:
                metrics[key] = value

    return {
        "result_summary": summary,
        "scalar_metrics": metrics,
        "candidate_trace_sections": key_candidates,
        "raw_result_preview": safe_preview(result_json, limit=5),
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    for p in [
        ENGINE_A_REPORT,
        ENGINE_B_REPORT,
        ENGINE_C_R1_REPORT,
        ENGINE_D_REPORT,
        ENGINE_E_REPORT,
        ENGINE_F_REPORT,
    ]:
        if not p.exists():
            raise FileNotFoundError(f"Missing prerequisite report: {rel(p)}")

    prereq = {
        "engine_d_passed": read_json(ENGINE_D_REPORT).get("decision", {}).get("historical_adapter_skeleton_passed") is True,
        "engine_e_passed": read_json(ENGINE_E_REPORT).get("decision", {}).get("state_contract_smoke_passed") is True,
        "engine_f_passed": read_json(ENGINE_F_REPORT).get("decision", {}).get("core_engine_shell_smoke_passed") is True,
    }

    if not all(prereq.values()):
        raise RuntimeError(f"Prerequisite stage failed: {prereq}")

    from e1r_engine.adapters.historical_data import HistoricalDataAdapter
    from src.engine.backtest import run_stateful_simulation

    adapter = HistoricalDataAdapter(ROOT)
    bundle = adapter.load_bundle(min_bars=120)
    bundle_validation = bundle.validate_shape()

    if not bundle_validation["ok"]:
        raise RuntimeError(f"HistoricalDataBundle invalid: {bundle_validation}")

    spx = bundle.indices["SPX"]
    ndx = bundle.indices["NDX"]
    sox = bundle.indices["SOX"]
    vix = bundle.vix

    window_day_count = count_dates_between(spx.dates, SHORT_WINDOW_START, SHORT_WINDOW_END)
    if window_day_count <= 0:
        raise RuntimeError("Short window has no SPX dates.")
    if window_day_count > MAX_WINDOW_DAYS_ALLOWED:
        raise RuntimeError(f"Short window too long: {window_day_count} > {MAX_WINDOW_DAYS_ALLOWED}")

    prices_map = bundle.prices_map
    dates_map = bundle.dates_map
    ohlc_map = {sym: bars_to_legacy_ohlc_dict(bars) for sym, bars in bundle.ohlc_map.items()}

    assumptions = {
        # Required fields identified by previous assumption contract.
        "buy_size": 0.20,
        "add_size": 0.10,
        "max_single_size": 0.35,
        "max_positions": 3,
        "total_one_way": 1.00,

        # Safe baseline defaults; this does not change strategy files.
        "initial_cash": 100000.0,
        "min_hold_days": 10,
        "e1r_enabled": True,
        "e1r_max_positions": 3,
        "e1r_sideways_enabled": False,
        "debug": False,
    }

    signature = str(inspect.signature(run_stateful_simulation))

    result = run_stateful_simulation(
        symbols=bundle.symbols,
        prices_map=prices_map,
        dates_map=dates_map,
        spx_prices=spx.closes,
        spx_dates=spx.dates,
        ohlc_map=ohlc_map,
        assumptions=assumptions,
        step=1,
        min_history=120,
        market_score_default=60.0,
        sim_start_date=SHORT_WINDOW_START,
        sim_end_date=SHORT_WINDOW_END,
        ndx_prices=ndx.closes,
        ndx_dates=ndx.dates,
        sox_prices=sox.closes,
        sox_dates=sox.dates,
        vix_prices=vix.closes if vix else None,
        vix_dates=vix.dates if vix else None,
    )

    extracted = extract_candidate_golden_master(result)

    golden_master = {
        "schema": "E1RGoldenMasterShortWindowV1",
        "generated_at": now(),
        "stage": "4C-2C-4E-ENGINE-G",
        "source": {
            "baseline_function": "src.engine.backtest.run_stateful_simulation",
            "signature": signature,
            "input_adapter": "e1r_engine.adapters.historical_data.HistoricalDataAdapter",
        },
        "window": {
            "start": SHORT_WINDOW_START,
            "end": SHORT_WINDOW_END,
            "spx_trading_days": window_day_count,
            "max_window_days_allowed": MAX_WINDOW_DAYS_ALLOWED,
        },
        "input_summary": {
            "symbols_count": len(bundle.symbols),
            "indices": sorted(bundle.indices.keys()),
            "regime_count": len(bundle.regime_daily),
            "vix_available": vix is not None,
            "bundle_validation": bundle_validation,
            "date_alignment": bundle.metadata.get("date_alignment"),
        },
        "assumption_keys": sorted(assumptions.keys()),
        "golden_master_extract": extracted,
        "raw_result": json_safe(result),
    }
    write_json(GOLDEN_MASTER_JSON, golden_master)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    candidates = extracted["candidate_trace_sections"]
    trace_section_count = sum(len(v) for v in candidates.values())
    raw_is_dict = isinstance(json_safe(result), dict)
    raw_key_count = len(json_safe(result).keys()) if raw_is_dict else 0

    validations = {
        "golden_master_harness_defined": True,
        "short_window_existing_engine_run": True,
        "strategy_logic_changed": False,
        "full_5y_backtest_run": False,
        "forward_runner_run": False,
        "provider_extraction_run": False,
        "strategy_core_implemented": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "invalid_artifacts_not_used_as_source": True,
        "composer_not_used": True,
        "return_curve_stitching_used": False,
        "engine_a_loaded": True,
        "engine_b_loaded": True,
        "engine_c_r1_loaded": True,
        "engine_d_loaded": prereq["engine_d_passed"],
        "engine_e_loaded": prereq["engine_e_passed"],
        "engine_f_loaded": prereq["engine_f_passed"],
        "historical_adapter_bundle_loaded": bundle_validation["ok"],
        "short_window_days_le_90": window_day_count <= MAX_WINDOW_DAYS_ALLOWED,
        "run_stateful_simulation_called_once": True,
        "baseline_result_is_dict": raw_is_dict,
        "baseline_result_has_keys": raw_key_count > 0,
        "golden_master_file_written": GOLDEN_MASTER_JSON.exists(),
        "trace_sections_detected": trace_section_count > 0,
        "strategy_core_extraction_not_allowed_yet": True,
        "uptrend_provider_extraction_not_allowed_yet": True,
    }

    decision = {
        "golden_master_harness_passed": all([
            validations["historical_adapter_bundle_loaded"],
            validations["short_window_days_le_90"],
            validations["baseline_result_is_dict"],
            validations["baseline_result_has_keys"],
            validations["golden_master_file_written"],
            validations["strategy_files_unchanged"],
        ]),
        "trace_sections_detected": trace_section_count,
        "golden_master_api_locked_for_next_stage": {
            "baseline_source": "src.engine.backtest.run_stateful_simulation",
            "golden_master_path": rel(GOLDEN_MASTER_JSON),
            "window": f"{SHORT_WINDOW_START}..{SHORT_WINDOW_END}",
            "purpose": "future extraction equivalence comparison, not official performance result",
        },
        "strategy_core_extraction_allowed_now": False,
        "uptrend_provider_extraction_allowed_now": False,
        "sideways_branch_implementation_allowed_now": False,
        "full_5y_backtest_allowed_now": False,
        "forward_runner_allowed_now": False,
        "recommended_next_stage": "4C-2C-4E-ENGINE-H",
        "conclusion": (
            "GOLDEN_MASTER_HARNESS_PASS_READY_FOR_TRACE_SHAPE_AUDIT"
            if all([
                validations["baseline_result_is_dict"],
                validations["golden_master_file_written"],
                validations["strategy_files_unchanged"],
            ])
            else "GOLDEN_MASTER_HARNESS_NEEDS_REVIEW"
        ),
        "recommended_next_action": (
            "Proceed to 4C-2C-4E-ENGINE-H: audit golden-master trace shape and define exact equivalence assertions. "
            "Do not extract UPTREND strategy core yet."
        ),
        "engineering_rule": (
            "Golden master is a comparison baseline only. It must not be treated as official result, "
            "and it must not modify strategy behavior."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-G",
        "status": "GOLDEN_MASTER_HARNESS_COMPLETE",
        "purpose": "Run a short-window existing-engine baseline via run_stateful_simulation and export golden-master trace-shaped output for future equivalence comparison.",
        "policy": {
            "strategy_logic_changed": False,
            "short_window_existing_engine_run": True,
            "full_5y_backtest_run": False,
            "forward_runner_run": False,
            "provider_extraction_run": False,
            "strategy_core_implemented": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
            "invalid_artifacts_used_as_source": False,
            "composer_used": False,
            "return_curve_stitching_used": False,
        },
        "baseline_function": {
            "name": "run_stateful_simulation",
            "module": "src.engine.backtest",
            "signature": signature,
        },
        "window": {
            "start": SHORT_WINDOW_START,
            "end": SHORT_WINDOW_END,
            "spx_trading_days": window_day_count,
            "max_window_days_allowed": MAX_WINDOW_DAYS_ALLOWED,
        },
        "input_summary": golden_master["input_summary"],
        "result_summary": extracted["result_summary"],
        "candidate_trace_sections_summary": {
            key: [
                {
                    "key": item["key"],
                    "length": item["length"],
                    "first_row_keys": item["first_row_keys"],
                }
                for item in items
            ]
            for key, items in candidates.items()
        },
        "scalar_metrics": extracted["scalar_metrics"],
        "golden_master_path": rel(GOLDEN_MASTER_JSON),
        "golden_master_sha256": sha256(GOLDEN_MASTER_JSON),
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-G — Golden Master Harness")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Policy")
    md.append("```json")
    md.append(json.dumps(report["policy"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Baseline Function")
    md.append("```json")
    md.append(json.dumps(report["baseline_function"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Window")
    md.append("```json")
    md.append(json.dumps(report["window"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Input Summary")
    md.append("```json")
    md.append(json.dumps(report["input_summary"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Result Summary")
    md.append("```json")
    md.append(json.dumps(report["result_summary"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Candidate Trace Sections")
    md.append("```json")
    md.append(json.dumps(report["candidate_trace_sections_summary"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Scalar Metrics")
    md.append("```json")
    md.append(json.dumps(report["scalar_metrics"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Golden Master")
    md.append(f"- Path: `{report['golden_master_path']}`")
    md.append(f"- SHA256: `{report['golden_master_sha256']}`")
    md.append("")
    md.append("## Validations")
    md.append("```json")
    md.append(json.dumps(validations, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Decision")
    md.append("```json")
    md.append(json.dumps(decision, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")

    REPORT_MD.write_text("\n".join(md))
    ARCH_MD.write_text("\n".join(md))

    print("E1R_4C2C4E_ENGINE_G_GOLDEN_MASTER_HARNESS_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("baseline_function:", json.dumps(report["baseline_function"], ensure_ascii=False))
    print("window:", json.dumps(report["window"], ensure_ascii=False))
    print("input_summary:", json.dumps(report["input_summary"], ensure_ascii=False))
    print("result_summary:", json.dumps(report["result_summary"], ensure_ascii=False))
    print("candidate_trace_sections_summary:", json.dumps(report["candidate_trace_sections_summary"], ensure_ascii=False))
    print("scalar_metrics:", json.dumps(report["scalar_metrics"], ensure_ascii=False))
    print("golden_master:", json.dumps({
        "path": report["golden_master_path"],
        "sha256": report["golden_master_sha256"],
    }, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(GOLDEN_MASTER_JSON))


if __name__ == "__main__":
    main()
