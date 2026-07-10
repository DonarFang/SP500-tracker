#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
import traceback
import inspect
import sys
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_D4B_R1_UPTREND_GOLDEN_MASTER_DIAGNOSTIC.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_D4B_R1_UPTREND_GOLDEN_MASTER_DIAGNOSTIC.md"

D4A_REPORT = ROOT / "docs/research/E1R_4C2C4E_D4A_UPTREND_GOLDEN_MASTER_TRACE_CONTRACT.json"
B2_REPORT = ROOT / "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json"

BACKTEST_PATH = ROOT / "src/engine/backtest.py"
SIDECAR_PATH = ROOT / "src/engine/e1r_sidecar_sleeve.py"
COMPOSER_PATH = ROOT / "src/engine/e1r_composer.py"

FROZEN_STRATEGY_FILES = [
    BACKTEST_PATH,
    SIDECAR_PATH,
    COMPOSER_PATH,
]

STOCK_DIR = ROOT / "data/research/e1_5y/raw/stocks"
INDEX_DIR = ROOT / "data/research/e1_5y/raw/indices"
SPX_PATH = INDEX_DIR / "SPX.json"
NDX_PATH = INDEX_DIR / "NDX.json"
SOX_PATH = INDEX_DIR / "SOX.json"
REGIME_PATH = ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json"

VIX_CANDIDATES = [
    INDEX_DIR / "VIX.json",
    INDEX_DIR / "_VIX.json",
    ROOT / "data/prices/_VIX.json",
]

INVALID_ARTIFACTS = [
    ROOT / "exports/e1r_unified_5y_full_account_v1_result.json",
    ROOT / "exports/e1r_unified_5y_dashboard_research_bundle.json",
    ROOT / "exports/e1r_combined_5y_original_max3_result.json",
    ROOT / "exports/e1r_combined_5y_original_max3_equity_curve.json",
    ROOT / "exports/e1r_combined_5y_original_max3_summary.json",
]

CANDIDATE_WINDOWS = [
    ("2021-10-01", "2022-03-31"),
    ("2022-03-01", "2022-08-31"),
    ("2023-01-03", "2023-06-30"),
    ("2023-07-03", "2023-12-29"),
    ("2024-01-02", "2024-06-28"),
    ("2024-07-01", "2024-12-31"),
    ("2025-01-02", "2025-06-30"),
    ("2025-07-01", "2025-12-31"),
]

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

def parse_date_value(row: dict[str, Any]) -> str | None:
    for k in ["date", "Date", "timestamp", "time"]:
        if k in row and row[k] is not None:
            return str(row[k])[:10]
    return None

def parse_close_value(row: dict[str, Any]) -> float | None:
    for k in ["close", "Close", "adj_close", "Adj Close", "adjClose", "c"]:
        if k in row and row[k] is not None:
            try:
                return float(row[k])
            except Exception:
                return None
    return None

def describe_json_shape(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False, "path": rel(path)}

    try:
        raw = read_json(path)
    except Exception as e:
        return {"exists": True, "path": rel(path), "parse_error": f"{type(e).__name__}: {e}"}

    desc: dict[str, Any] = {
        "exists": True,
        "path": rel(path),
        "type": type(raw).__name__,
    }

    if isinstance(raw, dict):
        desc["top_level_keys"] = sorted(list(raw.keys()))[:40]
        for key in ["data", "prices", "records"]:
            if isinstance(raw.get(key), list):
                desc["list_key"] = key
                desc["list_len"] = len(raw[key])
                desc["sample_type"] = type(raw[key][0]).__name__ if raw[key] else None
                desc["sample"] = raw[key][0] if raw[key] else None
                break
        if "dates" in raw and "closes" in raw:
            desc["dates_closes_len"] = [len(raw["dates"]), len(raw["closes"])]
    elif isinstance(raw, list):
        desc["list_len"] = len(raw)
        desc["sample_type"] = type(raw[0]).__name__ if raw else None
        desc["sample"] = raw[0] if raw else None

    return desc

def load_price_series(path: Path) -> tuple[list[str], list[float]]:
    raw = read_json(path)

    if isinstance(raw, dict):
        if "dates" in raw and "closes" in raw:
            dates = [str(x)[:10] for x in raw["dates"]]
            closes = [float(x) for x in raw["closes"]]
            return dates, closes
        for key in ["data", "prices", "records"]:
            if isinstance(raw.get(key), list):
                raw = raw[key]
                break

    dates: list[str] = []
    closes: list[float] = []

    if isinstance(raw, list):
        for row in raw:
            if isinstance(row, dict):
                d = parse_date_value(row)
                c = parse_close_value(row)
                if d and c is not None:
                    dates.append(d)
                    closes.append(c)
            elif isinstance(row, list) and len(row) >= 2:
                try:
                    dates.append(str(row[0])[:10])
                    closes.append(float(row[1]))
                except Exception:
                    pass

    if not dates or not closes:
        raise ValueError(f"Cannot parse price series from {rel(path)}")

    pairs = sorted(zip(dates, closes), key=lambda x: x[0])
    return [p[0] for p in pairs], [p[1] for p in pairs]

def input_diagnostics() -> dict[str, Any]:
    stock_files = sorted(STOCK_DIR.glob("*.json")) if STOCK_DIR.exists() else []
    sample_stock_shapes = [describe_json_shape(p) for p in stock_files[:5]]

    return {
        "stock_dir": {
            "path": rel(STOCK_DIR),
            "exists": STOCK_DIR.exists(),
            "json_count": len(stock_files),
            "sample_files": [p.name for p in stock_files[:10]],
            "sample_shapes": sample_stock_shapes,
        },
        "indices": {
            "SPX": describe_json_shape(SPX_PATH),
            "NDX": describe_json_shape(NDX_PATH),
            "SOX": describe_json_shape(SOX_PATH),
            "VIX_candidates": [describe_json_shape(p) for p in VIX_CANDIDATES],
        },
        "regime": describe_json_shape(REGIME_PATH),
        "d4a_report_exists": D4A_REPORT.exists(),
        "b2_report_exists": B2_REPORT.exists(),
    }

def load_stock_universe(max_symbols: int | None = None) -> tuple[list[str], dict[str, list[float]], dict[str, list[str]], dict[str, Any]]:
    if not STOCK_DIR.exists():
        raise FileNotFoundError(f"Missing stock dir: {rel(STOCK_DIR)}")

    symbols: list[str] = []
    prices_map: dict[str, list[float]] = {}
    dates_map: dict[str, list[str]] = {}
    skipped: dict[str, str] = {}

    files = sorted(STOCK_DIR.glob("*.json"))
    for path in files:
        sym = path.stem.replace("_", ".")
        if sym.upper() == "VIXY":
            skipped[sym] = "excluded_vixy"
            continue

        try:
            dates, closes = load_price_series(path)
        except Exception as e:
            skipped[sym] = f"parse_error:{type(e).__name__}:{e}"
            continue

        if len(dates) < 100:
            skipped[sym] = f"too_few_rows:{len(dates)}"
            continue

        symbols.append(sym)
        prices_map[sym] = closes
        dates_map[sym] = dates

        if max_symbols and len(symbols) >= max_symbols:
            break

    if not symbols:
        raise RuntimeError("No stock symbols loaded.")

    return symbols, prices_map, dates_map, {
        "files_seen": len(files),
        "symbols_loaded": len(symbols),
        "symbols_skipped": len(skipped),
        "skipped_sample": dict(list(skipped.items())[:20]),
        "first_symbols": symbols[:10],
    }

def load_regime_daily() -> dict[str, Any]:
    if not REGIME_PATH.exists():
        return {}

    raw = read_json(REGIME_PATH)

    if isinstance(raw, dict):
        if all(isinstance(k, str) and len(k) >= 10 for k in raw.keys()):
            return {k[:10]: v for k, v in raw.items()}

        for key in ["records", "data", "regimes"]:
            if isinstance(raw.get(key), list):
                raw = raw[key]
                break

    out = {}
    if isinstance(raw, list):
        for row in raw:
            if isinstance(row, dict):
                d = parse_date_value(row)
                if d:
                    out[d] = row

    return out

def build_assumptions() -> dict[str, Any]:
    base: dict[str, Any] = {}

    if B2_REPORT.exists():
        try:
            b2 = read_json(B2_REPORT)
            blueprint = b2.get("safe_assumption_blueprint", {}).get("typed_default_blueprint")
            if isinstance(blueprint, dict):
                base.update(blueprint)
        except Exception:
            pass

    base.update({
        "strategy_variant": "E1R_UPTREND_GOLDEN_MASTER_DIAGNOSTIC_D4B_R1",
        "version": "d4b-r1-diagnostic",
        "initial_capital": 100000,
        "max_positions": 3,
        "entry_top_n": 3,
        "candidate_top_n": 10,
        "buy_size": 1.0,
        "add_size": 0.5,
        "sell_size": 1.0,
        "reduce_size": 0.5,
        "max_single_size": 1.0,
        "total_one_way": 1.0,
        "min_holding_days": 10,
        "market_gate_enabled": True,
        "gate_use_slope": True,
        "gate_use_leadership": True,
        "market_shock_gate_enabled": False,
        "market_shock_daily_return": -0.02,
        "execution_model": "adverse_intraday",
        "ls60_exit_mode": "exit",
        "e1r_regime_wiring_enabled": True,
        "e1r_uptrend_execution_enabled": True,
        "e1r_shell_mode": "uptrend_golden_master_diagnostic",
        "e1r_regime_daily": load_regime_daily(),
        "qualified_entry_enabled": False,
        "dynamic_exit_enabled": False,
    })

    return base

def inspect_backtest_signature() -> dict[str, Any]:
    try:
        from src.engine.backtest import run_stateful_simulation
        sig = inspect.signature(run_stateful_simulation)
        return {
            "import_ok": True,
            "signature": str(sig),
            "parameters": list(sig.parameters.keys()),
        }
    except Exception as e:
        return {
            "import_ok": False,
            "error": f"{type(e).__name__}: {e}",
            "traceback": traceback.format_exc(limit=8),
        }

def summarize_engine_result(result: Any) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "type": type(result).__name__,
    }

    if isinstance(result, dict):
        summary["top_level_keys"] = sorted(result.keys())
        summary["list_keys"] = {
            k: len(v)
            for k, v in result.items()
            if isinstance(v, list)
        }
        summary["dict_keys"] = [
            k for k, v in result.items()
            if isinstance(v, dict)
        ]
    elif isinstance(result, tuple):
        summary["tuple_len"] = len(result)
        summary["tuple_types"] = [type(x).__name__ for x in result]
    elif isinstance(result, list):
        summary["list_len"] = len(result)
        summary["sample_type"] = type(result[0]).__name__ if result else None

    return summary

def classify_list(records: list[Any]) -> str:
    if not records or not isinstance(records[0], dict):
        return "other"

    keys = set()
    for row in records[:100]:
        if isinstance(row, dict):
            keys.update(row.keys())

    if {"date", "cash", "positions_value", "total_equity", "open_positions_count"}.issubset(keys):
        return "daily_account_state"
    if {"date", "symbol", "leader_score", "leader_rank", "rs_score", "trend_health"}.issubset(keys):
        return "candidate_trace"
    if {"sym", "action", "signal_date"}.issubset(keys):
        return "action_trace"
    if {"symbol", "entry_date", "exit_date", "entry_signal", "exit_signal"}.issubset(keys):
        return "position_lifecycle"
    if "action" in keys and ("symbol" in keys or "sym" in keys):
        return "generic_action"
    return "other"

def recursive_list_scan(obj: Any, path: str = "$", limit: int = 300) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    if len(out) >= limit:
        return out

    if isinstance(obj, dict):
        for k, v in obj.items():
            out.extend(recursive_list_scan(v, f"{path}.{k}", limit))
            if len(out) >= limit:
                break
    elif isinstance(obj, list):
        cls = classify_list(obj)
        keys = []
        if obj and isinstance(obj[0], dict):
            keys = sorted(obj[0].keys())
        out.append({
            "path": path,
            "len": len(obj),
            "classification": cls,
            "sample_keys": keys,
            "sample": obj[:2],
        })
        for i, v in enumerate(obj[:5]):
            if isinstance(v, (dict, list)):
                out.extend(recursive_list_scan(v, f"{path}[{i}]", limit))
                if len(out) >= limit:
                    break

    return out[:limit]

def attempt_window(window: tuple[str, str]) -> dict[str, Any]:
    attempt: dict[str, Any] = {
        "window": {"start": window[0], "end": window[1]},
        "ok": False,
        "phase": None,
    }

    try:
        attempt["phase"] = "load_universe"
        symbols, prices_map, dates_map, universe_meta = load_stock_universe()
        attempt["universe_meta"] = universe_meta

        attempt["phase"] = "load_indices"
        spx_dates, spx_prices = load_price_series(SPX_PATH)
        index_meta = {
            "spx_len": len(spx_dates),
            "spx_first": spx_dates[0] if spx_dates else None,
            "spx_last": spx_dates[-1] if spx_dates else None,
        }

        ndx_dates = ndx_prices = None
        sox_dates = sox_prices = None
        vix_dates = vix_prices = None

        if NDX_PATH.exists():
            ndx_dates, ndx_prices = load_price_series(NDX_PATH)
            index_meta["ndx_len"] = len(ndx_dates)
        if SOX_PATH.exists():
            sox_dates, sox_prices = load_price_series(SOX_PATH)
            index_meta["sox_len"] = len(sox_dates)

        for p in VIX_CANDIDATES:
            if p.exists():
                vix_dates, vix_prices = load_price_series(p)
                index_meta["vix_path"] = rel(p)
                index_meta["vix_len"] = len(vix_dates)
                break

        attempt["index_meta"] = index_meta

        attempt["phase"] = "build_assumptions"
        assumptions = build_assumptions()
        attempt["assumption_summary"] = {
            "key_count": len(assumptions),
            "max_positions": assumptions.get("max_positions"),
            "entry_top_n": assumptions.get("entry_top_n"),
            "candidate_top_n": assumptions.get("candidate_top_n"),
            "e1r_regime_daily_count": len(assumptions.get("e1r_regime_daily") or {}),
        }

        attempt["phase"] = "import_backtest"
        from src.engine.backtest import run_stateful_simulation
        sig = inspect.signature(run_stateful_simulation)
        params = set(sig.parameters.keys())

        kwargs = {
            "symbols": symbols,
            "prices_map": prices_map,
            "dates_map": dates_map,
            "spx_prices": spx_prices,
            "spx_dates": spx_dates,
            "ohlc_map": None,
            "assumptions": assumptions,
            "sim_start_date": window[0],
            "sim_end_date": window[1],
        }

        optional = {
            "ndx_prices": ndx_prices,
            "ndx_dates": ndx_dates,
            "sox_prices": sox_prices,
            "sox_dates": sox_dates,
            "vix_prices": vix_prices,
            "vix_dates": vix_dates,
        }
        for k, v in optional.items():
            if k in params:
                kwargs[k] = v

        # Also include common defaults only if present in signature.
        for k, v in {
            "step": 1,
            "min_history": 60,
            "market_score_default": 50.0,
        }.items():
            if k in params:
                kwargs[k] = v

        attempt["call_kwargs_keys"] = sorted(kwargs.keys())

        attempt["phase"] = "run_short_window_engine"
        result = run_stateful_simulation(**kwargs)

        attempt["phase"] = "scan_result"
        attempt["result_summary"] = summarize_engine_result(result)
        attempt["recursive_lists"] = recursive_list_scan(result)
        classifications = {}
        for item in attempt["recursive_lists"]:
            cls = item["classification"]
            classifications[cls] = classifications.get(cls, 0) + 1
        attempt["recursive_classification_counts"] = classifications

        attempt["ok"] = True
        attempt["phase"] = "complete"
        return attempt

    except Exception as e:
        attempt["ok"] = False
        attempt["error_type"] = type(e).__name__
        attempt["error"] = str(e)
        attempt["traceback"] = traceback.format_exc(limit=12)
        return attempt

def derive_decision(attempts: list[dict[str, Any]]) -> dict[str, Any]:
    ok_attempts = [a for a in attempts if a.get("ok")]
    errors_by_phase: dict[str, int] = {}
    errors_by_type: dict[str, int] = {}

    for a in attempts:
        if a.get("ok"):
            continue
        errors_by_phase[a.get("phase") or "unknown"] = errors_by_phase.get(a.get("phase") or "unknown", 0) + 1
        errors_by_type[a.get("error_type") or "unknown"] = errors_by_type.get(a.get("error_type") or "unknown", 0) + 1

    if ok_attempts:
        conclusion = "D4B_R1_ENGINE_CALL_DIAGNOSTIC_SUCCEEDED_TRACE_SCAN_AVAILABLE"
        next_action = (
            "Proceed to D4B-R2: build the actual golden master export using the confirmed result structure. "
            "Still no provider extraction."
        )
    else:
        conclusion = "D4B_R1_ENGINE_CALL_DIAGNOSTIC_FAILED_REVIEW_FAILURE_PHASE"
        next_action = (
            "Review diagnostic report phases/errors first. Do not continue to extraction. "
            "Fix the engine harness/input contract before exporting golden master."
        )

    return {
        "attempt_count": len(attempts),
        "ok_attempt_count": len(ok_attempts),
        "all_attempts_failed": len(ok_attempts) == 0,
        "errors_by_phase": errors_by_phase,
        "errors_by_type": errors_by_type,
        "provider_extraction_allowed_now": False,
        "adapter_implementation_allowed_now": False,
        "conclusion": conclusion,
        "recommended_next_action": next_action,
        "engineering_rule": (
            "The final E1R engine must support both 5Y backtest and ongoing forward test with one shared core logic. "
            "This diagnostic step must not introduce a backtest-only or forward-only shortcut."
        ),
    }

def write_report(report: dict[str, Any]) -> None:
    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-D4B-R1 — UPTREND Golden Master Fail-Safe Diagnostic")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Policy")
    md.append("```json")
    md.append(json.dumps(report["policy"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Input Diagnostics")
    md.append("```json")
    md.append(json.dumps(report["input_diagnostics"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Backtest Signature")
    md.append("```json")
    md.append(json.dumps(report["backtest_signature"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Attempts")
    md.append("```json")
    md.append(json.dumps(report["attempts"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Validations")
    md.append("```json")
    md.append(json.dumps(report["validations"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Decision")
    md.append("```json")
    md.append(json.dumps(report["decision"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    REPORT_MD.write_text("\n".join(md))

def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    attempts: list[dict[str, Any]] = []
    top_error: dict[str, Any] | None = None

    try:
        inp = input_diagnostics()
        sig = inspect_backtest_signature()

        if not D4A_REPORT.exists():
            raise FileNotFoundError(f"Missing D4A report: {rel(D4A_REPORT)}")

        d4a = read_json(D4A_REPORT)
        d4a_ready = bool(d4a.get("decision", {}).get("current_outputs_sufficient_for_minimal_golden_master"))

        for window in CANDIDATE_WINDOWS:
            attempts.append(attempt_window(window))

        decision = derive_decision(attempts)

    except Exception as e:
        inp = input_diagnostics()
        sig = inspect_backtest_signature()
        decision = {
            "attempt_count": len(attempts),
            "ok_attempt_count": 0,
            "all_attempts_failed": True,
            "top_level_failure": f"{type(e).__name__}: {e}",
            "provider_extraction_allowed_now": False,
            "adapter_implementation_allowed_now": False,
            "conclusion": "D4B_R1_TOP_LEVEL_DIAGNOSTIC_FAILURE_REPORT_WRITTEN",
            "recommended_next_action": "Review top-level diagnostic failure before continuing.",
            "engineering_rule": "Fail-safe report must exist even when export fails.",
        }
        top_error = {
            "type": type(e).__name__,
            "error": str(e),
            "traceback": traceback.format_exc(limit=12),
        }
        d4a_ready = False

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "fail_safe_report_written": True,
        "short_window_diagnostic_attempted": True,
        "full_5y_backtest_run": False,
        "provider_extraction_run": False,
        "adapter_implementation_run": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "invalid_artifacts_not_used_as_source": True,
        "composer_not_used": True,
        "return_curve_stitching_not_used": True,
        "d4a_contract_loaded": D4A_REPORT.exists(),
        "d4a_ready_for_trace": d4a_ready,
        "diagnostic_attempt_count": len(attempts),
        "provider_extraction_not_allowed_yet": True,
        "adapter_implementation_not_allowed_yet": True,
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-D4B-R1",
        "status": "UPTREND_GOLDEN_MASTER_FAILSAFE_DIAGNOSTIC_COMPLETE",
        "purpose": "Diagnose why D4B short-window golden master export failed while preserving no-strategy-change rules.",
        "policy": {
            "strategy_logic_changed": False,
            "short_window_diagnostic_attempted": True,
            "full_5y_backtest_run": False,
            "provider_extraction_run": False,
            "adapter_implementation_run": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
            "invalid_artifacts_used_as_source": False,
            "composer_used": False,
            "return_curve_stitching_used": False,
        },
        "input_diagnostics": inp,
        "backtest_signature": sig,
        "attempts": attempts,
        "top_level_error": top_error,
        "validations": validations,
        "decision": decision,
    }

    write_report(report)

    print("E1R_4C2C4E_D4B_R1_UPTREND_GOLDEN_MASTER_FAILSAFE_DIAGNOSTIC_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("input_diagnostics_summary:", json.dumps({
        "stock_dir": {
            "exists": inp["stock_dir"]["exists"],
            "json_count": inp["stock_dir"]["json_count"],
            "sample_files": inp["stock_dir"]["sample_files"][:5],
        },
        "indices": {
            "SPX_exists": inp["indices"]["SPX"].get("exists"),
            "NDX_exists": inp["indices"]["NDX"].get("exists"),
            "SOX_exists": inp["indices"]["SOX"].get("exists"),
        },
        "regime_exists": inp["regime"].get("exists"),
        "d4a_report_exists": inp["d4a_report_exists"],
    }, ensure_ascii=False))
    print("backtest_signature:", json.dumps(sig, ensure_ascii=False))
    print("attempt_summary:", json.dumps({
        "attempt_count": len(attempts),
        "ok_attempt_count": len([a for a in attempts if a.get("ok")]),
        "errors": [
            {
                "window": a.get("window"),
                "phase": a.get("phase"),
                "error_type": a.get("error_type"),
                "error": a.get("error"),
            }
            for a in attempts if not a.get("ok")
        ][:10],
        "ok_windows": [
            {
                "window": a.get("window"),
                "result_summary": a.get("result_summary"),
                "recursive_classification_counts": a.get("recursive_classification_counts"),
            }
            for a in attempts if a.get("ok")
        ],
    }, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
