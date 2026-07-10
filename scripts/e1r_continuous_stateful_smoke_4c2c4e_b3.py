#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
import importlib
import inspect
import sys
import traceback
from datetime import datetime, timezone
from collections import Counter
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

B2_REPORT = ROOT / "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_B3_CONTINUOUS_STATEFUL_SMOKE_TYPED_CONTRACT.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_B3_CONTINUOUS_STATEFUL_SMOKE_TYPED_CONTRACT.md"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

INVALID_ARTIFACTS = [
    ROOT / "exports/e1r_unified_5y_full_account_v1_result.json",
    ROOT / "exports/e1r_unified_5y_dashboard_research_bundle.json",
    ROOT / "exports/e1r_combined_5y_original_max3_result.json",
    ROOT / "exports/e1r_combined_5y_original_max3_equity_curve.json",
    ROOT / "exports/e1r_combined_5y_original_max3_summary.json",
]

SMOKE_START = "2022-01-03"
SMOKE_END = "2022-06-30"
INITIAL_EQUITY = 100000.0
MAX_POSITIONS = 3
EXCLUDED_SYMBOLS = {"VIXY"}

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))

def sha256(p: Path) -> str | None:
    if not p.exists():
        return None
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def read_json(path: Path) -> Any:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def fnum(x: Any, default=None):
    try:
        if x is None:
            return default
        return float(x)
    except Exception:
        return default

def extract_bars(obj: Any) -> list[dict[str, Any]]:
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]
    if isinstance(obj, dict):
        for key in ["bars", "prices", "data", "rows"]:
            if isinstance(obj.get(key), list):
                return [x for x in obj[key] if isinstance(x, dict)]
    return []

def normalize_price_file(path: Path):
    obj = read_json(path)
    bars = extract_bars(obj)

    dates, closes = [], []
    ohlc = {"open": [], "high": [], "low": [], "close": [], "volume": []}

    for b in bars:
        d = b.get("date")
        c = fnum(b.get("close"))
        if d is None or c is None:
            continue

        dates.append(str(d)[:10])
        closes.append(c)
        ohlc["open"].append(fnum(b.get("open"), c))
        ohlc["high"].append(fnum(b.get("high"), c))
        ohlc["low"].append(fnum(b.get("low"), c))
        ohlc["close"].append(c)
        ohlc["volume"].append(fnum(b.get("volume"), 0.0))

    return dates, closes, ohlc

def choose_existing_path(candidates: list[Path]) -> Path | None:
    for p in candidates:
        if p.exists():
            return p
    return None

def choose_stock_dir() -> Path:
    candidates = [
        ROOT / "data/research/e1_5y/raw/stocks",
        ROOT / "data/prices",
    ]
    for p in candidates:
        if p.exists() and any(p.glob("*.json")):
            return p
    raise RuntimeError("No stock price directory found.")

def choose_index_path(kind: str) -> Path | None:
    mapping = {
        "SPX": [
            ROOT / "data/research/e1_5y/raw/indices/SPX.json",
            ROOT / "data/prices/_GSPC.json",
            ROOT / "data/prices/SPY.json",
        ],
        "NDX": [
            ROOT / "data/research/e1_5y/raw/indices/NDX.json",
            ROOT / "data/prices/_NDX.json",
        ],
        "SOX": [
            ROOT / "data/research/e1_5y/raw/indices/SOX.json",
            ROOT / "data/prices/_SOX.json",
        ],
        "VIX": [
            ROOT / "data/research/e1_5y/raw/indices/VIX.json",
            ROOT / "data/prices/_VIX.json",
        ],
    }
    return choose_existing_path(mapping[kind])

def choose_regime_path() -> Path:
    candidates = [
        ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json",
        ROOT / "data/regimes/spx_regime_daily.json",
        ROOT / "exports/market_state.json",
    ]
    p = choose_existing_path(candidates)
    if p is None:
        raise RuntimeError("No regime file found.")
    return p

def load_stock_inputs(stock_dir: Path):
    symbols, prices_map, dates_map, ohlc_map, skipped = [], {}, {}, {}, []

    for p in sorted(stock_dir.glob("*.json")):
        sym = p.stem.upper()

        if sym.startswith("_"):
            continue
        if sym in {"SPY", "SPX", "NDX", "SOX", "VIX", "_GSPC", "_NDX", "_SOX", "_VIX"}:
            continue
        if sym in EXCLUDED_SYMBOLS:
            continue

        try:
            dates, closes, ohlc = normalize_price_file(p)
        except Exception as exc:
            skipped.append({"symbol": sym, "path": rel(p), "reason": type(exc).__name__ + ": " + str(exc)})
            continue

        if len(dates) < 260:
            skipped.append({"symbol": sym, "path": rel(p), "reason": f"insufficient_bars:{len(dates)}"})
            continue

        symbols.append(sym)
        prices_map[sym] = closes
        dates_map[sym] = dates
        ohlc_map[sym] = ohlc

    if not symbols:
        raise RuntimeError("No usable stock symbols loaded.")

    return symbols, prices_map, dates_map, ohlc_map, skipped

def load_index(path: Path | None):
    if path is None:
        return [], [], {}
    try:
        return normalize_price_file(path)
    except Exception:
        return [], [], {}

def load_regime_daily(path: Path):
    obj = read_json(path)
    raw = {}

    if isinstance(obj, list):
        raw = {str(r.get("date"))[:10]: r for r in obj if isinstance(r, dict) and r.get("date")}
    elif isinstance(obj, dict):
        if isinstance(obj.get("daily_regime"), dict):
            raw = obj["daily_regime"]
        elif isinstance(obj.get("regimes"), dict):
            raw = obj["regimes"]
        elif isinstance(obj.get("rows"), list):
            raw = {str(r.get("date"))[:10]: r for r in obj["rows"] if isinstance(r, dict) and r.get("date")}
        elif obj.get("date") and (obj.get("regime") or obj.get("spx_regime")):
            raw = {str(obj["date"])[:10]: obj}
        else:
            raw = {str(k)[:10]: v for k, v in obj.items() if isinstance(k, str) and len(k) >= 10}

    out = {}
    for d, v in raw.items():
        if isinstance(v, str):
            out[d] = {
                "date": d,
                "regime": v,
                "spx_regime": v,
                "subclass": "NO_SUBCLASS",
                "sideways_subclass": "NO_SUBCLASS",
            }
        elif isinstance(v, dict):
            regime = (
                v.get("regime")
                or v.get("spx_regime")
                or v.get("market_regime")
                or v.get("state")
                or "UNKNOWN"
            )
            subclass = (
                v.get("subclass")
                or v.get("sideways_subclass")
                or v.get("sideways_type")
                or "NO_SUBCLASS"
            )
            vv = dict(v)
            vv["date"] = d
            vv["regime"] = regime
            vv["spx_regime"] = regime
            vv["subclass"] = subclass
            vv["sideways_subclass"] = subclass
            out[d] = vv

    if not out:
        raise RuntimeError(f"No usable regime daily records from {path}")

    return out

def run_original_sidecar(stock_dir: Path, spx_path: Path, regime_path: Path):
    sys.path.insert(0, str(ROOT))
    mod = importlib.import_module("src.engine.e1r_sidecar_sleeve")
    Config = getattr(mod, "E1RSidecarConfig")
    build = getattr(mod, "build_e1r_sidecar_sleeve")

    config = Config(start_date=SMOKE_START, end_date=SMOKE_END)
    result = build(stock_dir=stock_dir, spx_path=spx_path, regime_path=regime_path, config=config)

    records = result.get("records") if isinstance(result, dict) else []
    if not isinstance(records, list):
        records = []

    by_date = {str(r.get("date"))[:10]: r for r in records if isinstance(r, dict) and r.get("date")}
    active = [r for r in records if isinstance(r, dict) and r.get("is_active") is True]

    summary = {
        "ok": True,
        "record_count": len(records),
        "active_count": len(active),
        "active_regime_counts": dict(Counter(r.get("regime", "UNKNOWN") for r in active)),
        "active_subclass_counts": dict(Counter(r.get("subclass", "NO_SUBCLASS") for r in active)),
        "selected_count_max": max([int(r.get("selected_count") or 0) for r in records], default=0),
        "holdings_len_max": max([
            len(r.get("holdings")) if isinstance(r.get("holdings"), list) else 0
            for r in records
        ], default=0),
        "gross_exposure_max": max([fnum(r.get("gross_exposure"), 0.0) or 0.0 for r in records], default=0.0),
        "strict_active_ma_conflict_count": sum(
            1 for r in records
            if r.get("is_active") is True
            and r.get("regime") == "SIDEWAYS"
            and r.get("subclass") == "MA_CONFLICT"
        ),
    }

    return result, by_date, summary

def build_typed_assumptions_from_b2(regime_daily: dict[str, Any]):
    if not B2_REPORT.exists():
        raise RuntimeError(f"Missing B2 report: {rel(B2_REPORT)}")

    b2 = read_json(B2_REPORT)
    blueprint = b2["safe_assumption_blueprint"]["typed_default_blueprint"]

    assumptions = dict(blueprint)

    assumptions["e1r_regime_daily"] = regime_daily
    assumptions["e1r_regime_source"] = "regime_daily_loaded_by_4C2C4E_B3_smoke"
    assumptions["e1r_regime_wiring_enabled"] = True
    assumptions["e1r_uptrend_execution_enabled"] = True
    assumptions["e1r_shell_mode"] = "continuous_stateful_smoke"

    assumptions["initial_capital"] = INITIAL_EQUITY
    assumptions["max_positions"] = MAX_POSITIONS
    assumptions["entry_top_n"] = MAX_POSITIONS
    assumptions["candidate_top_n"] = 10

    assumptions["buy_size"] = 1.0
    assumptions["add_size"] = 0.5
    assumptions["sell_size"] = 1.0
    assumptions["reduce_size"] = 0.5
    assumptions["position_size_pct"] = 1.0 / MAX_POSITIONS
    assumptions["max_single_size"] = 1.0
    assumptions["total_one_way"] = 1.0

    assumptions["min_holding_days"] = 10
    assumptions["min_hold"] = 10

    assumptions["market_gate_enabled"] = True
    assumptions["gate_use_slope"] = True
    assumptions["gate_use_leadership"] = True
    assumptions["market_entry_gate"] = "slope_leadership"
    assumptions["market_shock_gate_enabled"] = False
    assumptions["market_shock_daily_return"] = -0.02
    assumptions["risk_off_below_spx_ma50"] = False

    assumptions["execution_model"] = "adverse_intraday"
    assumptions["ls60_exit_mode"] = "exit"

    assumptions["strategy_variant"] = "E1R_CONTINUOUS_STATEFUL_SMOKE_4C2C4E_B3"
    assumptions["version"] = "4C-2C-4E-B3-smoke-not-official"

    assumptions["partial_take_profit_enabled"] = False
    assumptions["rank_based_exit"] = False
    assumptions["relative_stop_enabled"] = False
    assumptions["dynamic_exit_enabled"] = False
    assumptions["qualified_entry_enabled"] = False

    contract_keys = sorted(blueprint.keys())
    missing_after_override = [k for k in contract_keys if k not in assumptions]

    override_summary = {
        "source_b2_report": rel(B2_REPORT),
        "contract_key_count": len(contract_keys),
        "missing_after_override": missing_after_override,
        "critical_overrides": {
            "e1r_regime_wiring_enabled": assumptions["e1r_regime_wiring_enabled"],
            "e1r_uptrend_execution_enabled": assumptions["e1r_uptrend_execution_enabled"],
            "e1r_shell_mode": assumptions["e1r_shell_mode"],
            "market_gate_enabled": assumptions["market_gate_enabled"],
            "gate_use_slope": assumptions["gate_use_slope"],
            "gate_use_leadership": assumptions["gate_use_leadership"],
            "execution_model": assumptions["execution_model"],
            "ls60_exit_mode": assumptions["ls60_exit_mode"],
            "market_shock_daily_return": assumptions["market_shock_daily_return"],
            "max_positions": assumptions["max_positions"],
            "entry_top_n": assumptions["entry_top_n"],
            "candidate_top_n": assumptions["candidate_top_n"],
            "buy_size": assumptions["buy_size"],
            "add_size": assumptions["add_size"],
            "sell_size": assumptions["sell_size"],
            "reduce_size": assumptions["reduce_size"],
        },
        "type_checks": {
            "market_shock_daily_return_is_number": isinstance(assumptions["market_shock_daily_return"], (int, float)),
            "buy_size_is_number": isinstance(assumptions["buy_size"], (int, float)),
            "max_positions_is_int": isinstance(assumptions["max_positions"], int),
            "e1r_regime_daily_is_dict": isinstance(assumptions["e1r_regime_daily"], dict),
        },
    }

    return assumptions, override_summary

def call_backtest_engine(stock_dir: Path, regime_daily: dict[str, Any]):
    sys.path.insert(0, str(ROOT))
    mod = importlib.import_module("src.engine.backtest")
    fn = getattr(mod, "run_stateful_simulation")

    symbols, prices_map, dates_map, ohlc_map, skipped = load_stock_inputs(stock_dir)

    spx_path = choose_index_path("SPX")
    ndx_path = choose_index_path("NDX")
    sox_path = choose_index_path("SOX")
    vix_path = choose_index_path("VIX")

    spx_dates, spx_prices, _ = load_index(spx_path)
    ndx_dates, ndx_prices, _ = load_index(ndx_path)
    sox_dates, sox_prices, _ = load_index(sox_path)
    vix_dates, vix_prices, _ = load_index(vix_path)

    assumptions, assumption_summary = build_typed_assumptions_from_b2(regime_daily)

    result = fn(
        symbols=symbols,
        prices_map=prices_map,
        dates_map=dates_map,
        spx_prices=spx_prices,
        spx_dates=spx_dates,
        ohlc_map=ohlc_map,
        assumptions=assumptions,
        step=1,
        min_history=200,
        market_score_default=50,
        sim_start_date=SMOKE_START,
        sim_end_date=SMOKE_END,
        ndx_prices=ndx_prices,
        ndx_dates=ndx_dates,
        sox_prices=sox_prices,
        sox_dates=sox_dates,
        vix_prices=vix_prices,
        vix_dates=vix_dates,
    )

    input_summary = {
        "function_signature": str(inspect.signature(fn)),
        "stock_dir": rel(stock_dir),
        "symbols_loaded": len(symbols),
        "symbols_skipped": len(skipped),
        "spx_path": rel(spx_path) if spx_path else None,
        "ndx_path": rel(ndx_path) if ndx_path else None,
        "sox_path": rel(sox_path) if sox_path else None,
        "vix_path": rel(vix_path) if vix_path else None,
        "assumption_summary": assumption_summary,
    }

    return result, input_summary

def get_daily_records(result: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ["daily_equity_records", "daily_records"]:
        v = result.get(key)
        if isinstance(v, list) and v:
            return [r for r in v if isinstance(r, dict)]
    return []

def summarize_engine_records(records: list[dict[str, Any]], regime_daily: dict[str, Any], sidecar_by_date: dict[str, Any]):
    regime_counts = Counter()
    subclass_counts = Counter()
    branch_counts = Counter()
    open_position_counts = []
    missing_equity = 0
    missing_state_fields = 0
    violations = []
    observed_rows = []

    for r in records:
        d = str(r.get("date") or "")[:10]
        regime_info = regime_daily.get(d, {})
        sidecar = sidecar_by_date.get(d, {})

        regime = (
            r.get("regime")
            or r.get("spx_regime")
            or regime_info.get("regime")
            or regime_info.get("spx_regime")
            or "UNKNOWN"
        )

        subclass = (
            r.get("subclass")
            or r.get("sideways_subclass")
            or regime_info.get("subclass")
            or regime_info.get("sideways_subclass")
            or sidecar.get("subclass")
            or "NO_SUBCLASS"
        )

        if regime == "UPTREND":
            branch_plan = "UPTREND_ENGINE_BRANCH"
        elif regime == "SIDEWAYS" and subclass == "MA_CONFLICT":
            branch_plan = "SIDEWAYS_MA_CONFLICT_SIDECAR_AVAILABLE" if sidecar.get("is_active") is True else "SIDEWAYS_MA_CONFLICT_NO_ACTIVE_SIDECAR"
        else:
            branch_plan = "CASH_DEFENSIVE_EXPECTED"

        open_count = int(r.get("open_positions_count") or 0)
        open_position_counts.append(open_count)

        if open_count > MAX_POSITIONS:
            violations.append({
                "date": d,
                "regime": regime,
                "subclass": subclass,
                "open_positions_count": open_count,
                "branch_plan": branch_plan,
            })

        total_equity = fnum(r.get("total_equity"))
        if total_equity is None:
            total_equity = fnum(r.get("equity"))
        if total_equity is None:
            missing_equity += 1

        has_state = (
            r.get("cash") is not None
            or r.get("positions_value") is not None
            or r.get("market_value") is not None
            or r.get("positions") is not None
        )
        if not has_state:
            missing_state_fields += 1

        regime_counts[regime] += 1
        subclass_counts[subclass] += 1
        branch_counts[branch_plan] += 1

        if len(observed_rows) < 30:
            observed_rows.append({
                "date": d,
                "regime": regime,
                "subclass": subclass,
                "branch_plan": branch_plan,
                "open_positions_count": open_count,
                "cash": r.get("cash"),
                "positions_value": r.get("positions_value"),
                "total_equity": total_equity,
                "sidecar_is_active": sidecar.get("is_active"),
                "sidecar_selected_count": sidecar.get("selected_count"),
                "sidecar_gross_exposure": sidecar.get("gross_exposure"),
            })

    return {
        "record_count": len(records),
        "first_date": str(records[0].get("date"))[:10] if records else None,
        "last_date": str(records[-1].get("date"))[:10] if records else None,
        "regime_counts": dict(regime_counts),
        "subclass_counts": dict(subclass_counts),
        "branch_plan_counts": dict(branch_counts),
        "max_open_positions": max(open_position_counts, default=0),
        "open_position_violations": violations[:30],
        "open_position_violations_count": len(violations),
        "missing_equity_rows": missing_equity,
        "missing_state_field_rows": missing_state_fields,
        "observed_rows_sample": observed_rows,
    }

def write_failure_report(started, before_hashes, error_text: str):
    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}
    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-B3",
        "status": "CONTINUOUS_STATEFUL_SMOKE_FAILED",
        "policy": {
            "strategy_logic_changed": False,
            "backtest_engine_run": True,
            "full_5y_backtest_run": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
            "invalid_artifacts_used_as_source": False,
            "composer_used": False,
            "return_curve_stitching_used": False,
        },
        "error": error_text,
        "conclusion": "4C2C4E_B3_SMOKE_FAILED_REVIEW_BEFORE_CONTINUING",
        "recommended_next_action": "Review failure report before another smoke attempt.",
    }
    write_json(REPORT_JSON, report)
    REPORT_MD.write_text("# E1R 4C-2C-4E-B3 Smoke Failed\n\n```json\n" + json.dumps(report, indent=2, ensure_ascii=False) + "\n```\n")
    return report

def main():
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    try:
        stock_dir = choose_stock_dir()
        regime_path = choose_regime_path()
        spx_path = choose_index_path("SPX")
        if spx_path is None:
            raise RuntimeError("No SPX path found.")

        regime_daily = load_regime_daily(regime_path)

        invalid_artifacts_status = [
            {"path": rel(p), "exists": p.exists(), "used_as_source": False}
            for p in INVALID_ARTIFACTS
        ]

        sidecar_result, sidecar_by_date, sidecar_summary = run_original_sidecar(
            stock_dir=stock_dir,
            spx_path=spx_path,
            regime_path=regime_path,
        )

        engine_result, engine_input_summary = call_backtest_engine(
            stock_dir=stock_dir,
            regime_daily=regime_daily,
        )

        records = get_daily_records(engine_result)
        engine_summary = summarize_engine_records(records, regime_daily, sidecar_by_date)

        after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

        validations = {
            "audit_smoke_only_no_full_5y": True,
            "official_result_generated": False,
            "dashboard_changed": False,
            "strategy_files_unchanged": before_hashes == after_hashes,
            "invalid_artifacts_not_used_as_source": all(not x["used_as_source"] for x in invalid_artifacts_status),
            "no_composer_used": True,
            "no_return_curve_stitching": True,

            "typed_assumption_contract_loaded": engine_input_summary["assumption_summary"]["source_b2_report"].endswith("E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json"),
            "typed_assumption_missing_zero": engine_input_summary["assumption_summary"]["missing_after_override"] == [],
            "critical_type_checks_pass": all(engine_input_summary["assumption_summary"]["type_checks"].values()),

            "engine_run_completed": isinstance(engine_result, dict),
            "engine_daily_records_exist": len(records) > 0,
            "single_account_state_observed": engine_summary["missing_equity_rows"] == 0,
            "state_fields_observed": engine_summary["missing_state_field_rows"] < max(1, len(records)),
            "max_open_positions_le_3": engine_summary["max_open_positions"] <= MAX_POSITIONS,
            "position_violations_zero": engine_summary["open_position_violations_count"] == 0,

            "sidecar_run_completed": isinstance(sidecar_result, dict),
            "sidecar_records_exist": sidecar_summary["record_count"] > 0,
            "sideways_ma_conflict_sidecar_available": sidecar_summary["strict_active_ma_conflict_count"] > 0,
            "sidecar_selected_count_max_10": sidecar_summary["selected_count_max"] == 10,
            "sidecar_gross_exposure_max_025": abs(float(sidecar_summary["gross_exposure_max"]) - 0.25) < 1e-9,

            "uptrend_branch_plan_observed": engine_summary["branch_plan_counts"].get("UPTREND_ENGINE_BRANCH", 0) > 0,
            "sideways_ma_conflict_branch_plan_observed": (
                engine_summary["branch_plan_counts"].get("SIDEWAYS_MA_CONFLICT_SIDECAR_AVAILABLE", 0) > 0
                or engine_summary["branch_plan_counts"].get("SIDEWAYS_MA_CONFLICT_NO_ACTIVE_SIDECAR", 0) > 0
            ),
            "cash_defensive_branch_plan_observed": engine_summary["branch_plan_counts"].get("CASH_DEFENSIVE_EXPECTED", 0) > 0,
        }

        conclusion = (
            "READY_FOR_4C2C4E_C_CONTINUOUS_STATEFUL_IMPLEMENTATION_DESIGN"
            if all(validations.values())
            else "4C2C4E_B3_SMOKE_FAILED_REVIEW_BEFORE_CONTINUING"
        )

        report = {
            "generated_at": now(),
            "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
            "stage": "4C-2C-4E-B3",
            "status": "CONTINUOUS_STATEFUL_SMOKE_COMPLETE",
            "policy": {
                "strategy_logic_changed": False,
                "backtest_engine_run": True,
                "full_5y_backtest_run": False,
                "official_result_generated": False,
                "dashboard_changed": False,
                "frozen_strategy_files_changed": before_hashes != after_hashes,
                "invalid_artifacts_used_as_source": False,
                "composer_used": False,
                "return_curve_stitching_used": False,
                "assumption_source": "B2 typed_default_blueprint plus explicit E1R smoke overrides",
            },
            "inputs": {
                "stock_dir": rel(stock_dir),
                "regime_path": rel(regime_path),
                "spx_path": rel(spx_path),
                "smoke_start": SMOKE_START,
                "smoke_end": SMOKE_END,
            },
            "invalid_artifacts_status": invalid_artifacts_status,
            "engine_input_summary": engine_input_summary,
            "engine_summary": engine_summary,
            "sidecar_summary": sidecar_summary,
            "validations": validations,
            "conclusion": conclusion,
            "recommended_next_action": (
                "Proceed to 4C-2C-4E-C: design the official continuous stateful implementation path. "
                "Do not run full 5Y until 4E-C confirms exact branch execution and transition behavior."
                if conclusion.startswith("READY")
                else "Do not continue. Review failed smoke validations."
            ),
        }

        write_json(REPORT_JSON, report)

        md = []
        md.append("# E1R 4C-2C-4E-B3 — Continuous Stateful Smoke With Typed Assumption Contract")
        md.append("")
        md.append(f"Generated At: `{report['generated_at']}`")
        md.append("")
        md.append("## Purpose")
        md.append("")
        md.append("This is a smoke/prototype only. It is not an official E1R result and does not run the full 5Y backtest.")
        md.append("")
        md.append("## Policy")
        md.append("```json")
        md.append(json.dumps(report["policy"], indent=2, ensure_ascii=False))
        md.append("```")
        md.append("")
        md.append("## Engine Input Summary")
        md.append("```json")
        md.append(json.dumps(engine_input_summary, indent=2, ensure_ascii=False))
        md.append("```")
        md.append("")
        md.append("## Engine Summary")
        md.append("```json")
        md.append(json.dumps(engine_summary, indent=2, ensure_ascii=False))
        md.append("```")
        md.append("")
        md.append("## Sidecar Summary")
        md.append("```json")
        md.append(json.dumps(sidecar_summary, indent=2, ensure_ascii=False))
        md.append("```")
        md.append("")
        md.append("## Validations")
        md.append("```json")
        md.append(json.dumps(validations, indent=2, ensure_ascii=False))
        md.append("```")
        md.append("")
        md.append("## Conclusion")
        md.append(f"- `{conclusion}`")
        md.append(f"- Recommended: {report['recommended_next_action']}")
        md.append("")

        REPORT_MD.write_text("\n".join(md))

        print("E1R_4C2C4E_B3_CONTINUOUS_STATEFUL_SMOKE_COMPLETE")
        print("status:", report["status"])
        print("policy:", json.dumps(report["policy"], ensure_ascii=False))
        print("inputs:", json.dumps(report["inputs"], ensure_ascii=False))
        print("engine_input_summary:", json.dumps(engine_input_summary, ensure_ascii=False))
        print("engine_summary:", json.dumps(engine_summary, ensure_ascii=False))
        print("sidecar_summary:", json.dumps(sidecar_summary, ensure_ascii=False))
        print("validations:", json.dumps(validations, ensure_ascii=False))
        print("conclusion:", conclusion)
        print("recommended_next_action:", report["recommended_next_action"])
        print("wrote:", rel(REPORT_JSON))
        print("wrote:", rel(REPORT_MD))

    except Exception:
        err = traceback.format_exc()
        report = write_failure_report(started, before_hashes, err)
        print("E1R_4C2C4E_B3_FAILED")
        print(err)
        print("wrote:", rel(REPORT_JSON))
        print("wrote:", rel(REPORT_MD))
        raise

if __name__ == "__main__":
    main()
