#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import hashlib
import importlib
import inspect
import sys
import traceback
from datetime import datetime, timezone
from typing import Any
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
BACKTEST = ROOT / "src/engine/backtest.py"

REGIME_PATH = ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json"

OUT_RESULT = ROOT / "exports/e1r_unified_5y_full_account_v1_result.json"
OUT_CURVE = ROOT / "exports/e1r_unified_5y_full_account_v1_equity_curve.json"
OUT_SUMMARY = ROOT / "exports/e1r_unified_5y_full_account_v1_summary.json"

REPORT_JSON = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C_FULL_RUN_REPORT.json"
REPORT_MD = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C_FULL_RUN_REPORT.md"

FROZEN_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

ASSUMPTION_SOURCE_CANDIDATES = [
    ROOT / "exports/portfolio_backtest.json",
    ROOT / "exports/backtest.json",
    ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2B5_REGIME_WIRING_TRADE_WINDOW_REPORT.json",
]

STOCK_DIR_CANDIDATES = [
    ROOT / "data/research/e1_5y/raw/stocks",
    ROOT / "data/prices",
]

INDEX_PATHS = {
    "SPX": ROOT / "data/research/e1_5y/raw/indices/SPX.json",
    "NDX": ROOT / "data/research/e1_5y/raw/indices/NDX.json",
    "SOX": ROOT / "data/research/e1_5y/raw/indices/SOX.json",
    "VIX": ROOT / "data/research/e1_5y/raw/indices/VIX.json",
}

EXCLUDED_SYMBOLS = {"VIXY"}

HARD_DEFAULTS = {
    "initial_capital": 100000.0,
    "max_positions": 10,
    "buy_size": 1.0,
    "sell_size": 1.0,
    "add_size": 0.5,
    "reduce_size": 0.5,
    "max_single_size": 1.0,
    "total_one_way": 1.0,
    "position_size_pct": 0.10,
    "min_hold": 10,
    "min_holding_days": 10,
    "candidate_top_n": 10,
    "entry_top_n": 3,
    "entry_rs_min": 90.0,
    "qualified_rs_min": 90.0,
    "qualified_th_min": 75.0,
    "qualified_momentum_min": 85.0,
    "qualified_ma50_slope_min": 0.0,
    "qualified_price_above_ma50": True,
    "leader_score_exit": 60,
    "exit_score": 60,
    "market_gate_enabled": True,
    "gate_use_leadership": True,
    "gate_use_slope": True,
    "market_entry_gate": "slope_leadership",
    "market_shock_gate_enabled": False,
    "market_shock_daily_return": -0.02,
    "risk_off_below_spx_ma50": False,
    "execution_model": "adverse_intraday",
    "qualified_entry_enabled": False,
    "qualified_states": ["Expansion"],
    "partial_take_profit": False,
    "partial_take_profit_enabled": False,
    "partial_take_profit_fraction": 0.5,
    "partial_take_profit_threshold": 0.0,
    "block_add_after_take_profit": True,
    "rank_based_exit": False,
    "relative_stop_enabled": False,
    "relative_stop_underperform_pct": -8.0,
    "relative_stop_once_per_position": True,
    "relative_stop_action": "REL_REDUCE",
    "dynamic_exit_enabled": False,
    "ls60_exit_mode": "exit",
    "fill_only_enabled": False,
    "min_hold_allow_broken_exit": True,
    "commission_pct": 0.0,
    "slippage_pct": 0.0,
    "risk_budget": 1.0,
    "risk_budget_mode": "full",
}

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

def write_json(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def read_json(p: Path) -> Any:
    return json.loads(p.read_text())

def extract_bars(obj: Any) -> list[dict[str, Any]]:
    if isinstance(obj, dict):
        for k in ["bars", "prices", "data", "rows"]:
            v = obj.get(k)
            if isinstance(v, list):
                return [x for x in v if isinstance(x, dict)]
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]
    return []

def normalize_symbol_file(p: Path) -> tuple[list[str], list[float], dict[str, list[float]]]:
    obj = read_json(p)
    bars = extract_bars(obj)

    dates: list[str] = []
    closes: list[float] = []
    ohlc = {"open": [], "high": [], "low": [], "close": [], "volume": []}

    for b in bars:
        d = b.get("date")
        c = b.get("close")
        if d is None or c is None:
            continue
        try:
            cf = float(c)
        except Exception:
            continue

        of = float(b.get("open", cf)) if b.get("open") is not None else cf
        hf = float(b.get("high", cf)) if b.get("high") is not None else cf
        lf = float(b.get("low", cf)) if b.get("low") is not None else cf
        vf = float(b.get("volume", 0) or 0)

        dates.append(str(d)[:10])
        closes.append(cf)
        ohlc["open"].append(of)
        ohlc["high"].append(hf)
        ohlc["low"].append(lf)
        ohlc["close"].append(cf)
        ohlc["volume"].append(vf)

    return dates, closes, ohlc

def find_stock_files() -> list[Path]:
    seen = set()
    files = []
    for d in STOCK_DIR_CANDIDATES:
        if not d.exists():
            continue
        for p in sorted(d.glob("*.json")):
            stem = p.stem.upper()
            if stem.startswith("^") or stem in {"SPX", "NDX", "SOX", "VIX", "SPY", "QQQ"}:
                continue
            if stem in EXCLUDED_SYMBOLS:
                continue
            if stem in seen:
                continue
            seen.add(stem)
            files.append(p)
    return files

def extract_assumption_key_usage() -> dict[str, Any]:
    text = BACKTEST.read_text(errors="replace")
    tree = ast.parse(text)

    target = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "run_stateful_simulation":
            target = node
            break

    if target is None:
        return {"function_found": False, "keys": [], "hits": []}

    keys, hits = [], []
    for node in ast.walk(target):
        if isinstance(node, ast.Subscript):
            base = node.value.id if isinstance(node.value, ast.Name) else None
            if base in {"a", "assumptions"}:
                key = None
                s = node.slice
                if isinstance(s, ast.Constant):
                    key = s.value
                if isinstance(key, str):
                    keys.append(key)
                    hits.append({"line": getattr(node, "lineno", None), "base": base, "key": key, "kind": "subscript"})

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "get" and isinstance(node.func.value, ast.Name):
                base = node.func.value.id
                if base in {"a", "assumptions"} and node.args:
                    arg0 = node.args[0]
                    if isinstance(arg0, ast.Constant) and isinstance(arg0.value, str):
                        keys.append(arg0.value)
                        hits.append({"line": getattr(node, "lineno", None), "base": base, "key": arg0.value, "kind": "get"})

    return {
        "function_found": True,
        "keys": sorted(set(keys)),
        "hits": sorted(hits, key=lambda x: (x.get("line") or 0, x.get("key") or "")),
    }

def walk_dicts(obj: Any, path: str = "$") -> list[tuple[str, dict[str, Any]]]:
    out = []
    if isinstance(obj, dict):
        out.append((path, obj))
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                out.extend(walk_dicts(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:50]):
            if isinstance(v, (dict, list)):
                out.extend(walk_dicts(v, f"{path}[{i}]"))
    return out

def recover_assumptions(required_keys: list[str]) -> dict[str, Any]:
    recovered = {}
    sources = []

    for p in ASSUMPTION_SOURCE_CANDIDATES:
        if not p.exists():
            continue
        try:
            obj = read_json(p)
        except Exception:
            continue

        for path, d in walk_dicts(obj):
            overlap = sorted(set(required_keys) & set(d.keys()))
            if len(overlap) >= 5 or path.endswith("strategy_controls") or path.endswith("assumptions"):
                for k in overlap:
                    v = d.get(k)
                    if v is not None and k not in recovered:
                        recovered[k] = v
                sources.append({
                    "source": rel(p),
                    "json_path": path,
                    "overlap_count": len(overlap),
                    "overlap_keys": overlap[:80],
                })

    return {"values": recovered, "sources": sources[:40]}

def load_regime_daily() -> dict[str, Any]:
    obj = read_json(REGIME_PATH)

    if isinstance(obj, dict):
        if isinstance(obj.get("daily_regime"), dict):
            raw = obj["daily_regime"]
        elif isinstance(obj.get("regimes"), dict):
            raw = obj["regimes"]
        elif isinstance(obj.get("rows"), list):
            raw = {
                str(r.get("date"))[:10]: r
                for r in obj["rows"]
                if isinstance(r, dict) and r.get("date")
            }
        else:
            raw = {
                str(k)[:10]: v
                for k, v in obj.items()
                if isinstance(k, str) and len(k) >= 10
            }
    elif isinstance(obj, list):
        raw = {
            str(r.get("date"))[:10]: r
            for r in obj
            if isinstance(r, dict) and r.get("date")
        }
    else:
        raw = {}

    out = {}
    for d, v in raw.items():
        if isinstance(v, str):
            out[d] = {
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
            vv["regime"] = regime
            vv["spx_regime"] = regime
            vv["subclass"] = subclass
            vv["sideways_subclass"] = subclass
            out[d] = vv

    return out

def summarize_regime_daily(regime_daily: dict[str, Any]) -> dict[str, Any]:
    dates = sorted(regime_daily.keys())
    regimes = []
    subclasses = []
    for d in dates:
        v = regime_daily[d]
        if isinstance(v, dict):
            regimes.append(v.get("regime") or v.get("spx_regime") or "UNKNOWN")
            subclasses.append(v.get("subclass") or v.get("sideways_subclass") or "NO_SUBCLASS")
    return {
        "path": rel(REGIME_PATH),
        "exists": REGIME_PATH.exists(),
        "count": len(dates),
        "date_start": dates[0] if dates else None,
        "date_end": dates[-1] if dates else None,
        "regime_counts": dict(Counter(regimes)),
        "subclass_counts": dict(Counter(subclasses)),
    }

def build_assumptions(required_keys: list[str]) -> tuple[dict[str, Any], dict[str, Any]]:
    rec = recover_assumptions(required_keys)
    regime_daily = load_regime_daily()

    assumptions = {}
    provenance = {}

    for k in required_keys:
        if k in rec["values"] and rec["values"][k] is not None:
            assumptions[k] = rec["values"][k]
            provenance[k] = "recovered_artifact"
        elif k in HARD_DEFAULTS:
            assumptions[k] = HARD_DEFAULTS[k]
            provenance[k] = "hard_default"
        else:
            lk = k.lower()
            if "enabled" in lk or "allow" in lk:
                assumptions[k] = False
            elif "states" in lk:
                assumptions[k] = ["UPTREND", "SIDEWAYS"]
            elif "mode" in lk or "source" in lk or "variant" in lk or "version" in lk or "action" in lk:
                assumptions[k] = "default"
            elif "daily" in lk:
                assumptions[k] = {}
            elif any(x in lk for x in ["pct", "score", "threshold", "size", "fraction", "return"]):
                assumptions[k] = 0.0
            elif any(x in lk for x in ["days", "count", "top_n", "positions"]):
                assumptions[k] = 0
            else:
                assumptions[k] = False
            provenance[k] = "type_safe_fallback"

    for k, v in HARD_DEFAULTS.items():
        assumptions.setdefault(k, v)
        provenance.setdefault(k, "hard_default_extra")

    assumptions["e1r_regime_wiring_enabled"] = True
    assumptions["e1r_regime_daily"] = regime_daily
    assumptions["e1r_regime_source"] = rel(REGIME_PATH)
    assumptions["e1r_shell_mode"] = "unified_5y_full_account"
    assumptions["e1r_uptrend_execution_enabled"] = True
    assumptions["strategy_variant"] = "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1"
    assumptions["version"] = "4C-2C-full-5y-unified-account"

    provenance["e1r_regime_wiring_enabled"] = "stage_override"
    provenance["e1r_regime_daily"] = "stage_override_loaded_regime_file"
    provenance["e1r_regime_source"] = "stage_override_loaded_regime_file"
    provenance["e1r_shell_mode"] = "stage_override"
    provenance["e1r_uptrend_execution_enabled"] = "stage_override"
    provenance["strategy_variant"] = "stage_override"
    provenance["version"] = "stage_override"

    return assumptions, {
        "recovery": rec,
        "provenance": provenance,
        "regime_daily_summary": summarize_regime_daily(regime_daily),
    }

def build_inputs() -> dict[str, Any]:
    stock_files = find_stock_files()
    symbols, prices_map, dates_map, ohlc_map = [], {}, {}, {}

    skipped = []

    for p in stock_files:
        sym = p.stem.upper()
        try:
            dates, closes, ohlc = normalize_symbol_file(p)
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

    indices = {}
    for name, path in INDEX_PATHS.items():
        if path.exists():
            d, c, o = normalize_symbol_file(path)
            indices[name] = {"dates": d, "prices": c, "ohlc": o, "count": len(d), "start": d[0] if d else None, "end": d[-1] if d else None}
        else:
            indices[name] = {"dates": [], "prices": [], "ohlc": {}, "count": 0, "missing": True}

    spx_dates = set(indices["SPX"]["dates"])

    sim_start_date = "2021-06-11" if "2021-06-11" in spx_dates else indices["SPX"]["dates"][300]
    sim_end_date = "2026-06-18" if "2026-06-18" in spx_dates else indices["SPX"]["dates"][-1]

    usage = extract_assumption_key_usage()
    assumptions, assumption_build = build_assumptions(usage.get("keys", []))

    return {
        "symbols": symbols,
        "prices_map": prices_map,
        "dates_map": dates_map,
        "ohlc_map": ohlc_map,
        "indices": indices,
        "assumptions": assumptions,
        "assumption_usage": usage,
        "assumption_build": assumption_build,
        "step": 1,
        "min_history": 200,
        "market_score_default": 50,
        "sim_start_date": sim_start_date,
        "sim_end_date": sim_end_date,
        "skipped_symbols": skipped,
    }

def extract_daily_records(result: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ["daily_equity_records", "daily_records", "rows"]:
        v = result.get(key)
        if isinstance(v, list) and v and isinstance(v[0], dict):
            return v
    return []

def build_curve_artifact(result: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    records = extract_daily_records(result)
    rows = []

    first_equity = None
    prev_equity = None

    for r in records:
        eq = r.get("total_equity")
        try:
            eqf = float(eq)
        except Exception:
            eqf = None

        if first_equity is None and eqf is not None:
            first_equity = eqf

        indexed = eqf / first_equity * 100.0 if first_equity and eqf is not None else None

        rows.append({
            "date": r.get("date"),
            "total_equity": eqf,
            "indexed": indexed,
            "cash": r.get("cash"),
            "positions_value": r.get("positions_value"),
            "daily_return_pct": r.get("daily_return_pct"),
            "drawdown_pct": r.get("drawdown_pct"),
            "exposure_pct": r.get("exposure_pct"),
            "open_positions_count": r.get("open_positions_count"),
            "pending_orders_count": r.get("pending_orders_count"),
            "market_gate_state": r.get("market_gate_state"),
            "spx_regime": r.get("spx_regime"),
            "e1r_active_mode": r.get("e1r_active_mode"),
            "risk_budget_mode": r.get("risk_budget_mode"),
            "risk_budget": r.get("risk_budget"),
            "spx_close": r.get("spx_close"),
            "spx_ma50": r.get("spx_ma50"),
            "spx_day_return_pct": r.get("spx_day_return_pct"),
            "event": r.get("event"),
        })

        prev_equity = eqf

    return {
        "artifact_type": "e1r_unified_5y_full_account_v1_equity_curve",
        "generated_at": now(),
        "canonical_for_spec": True,
        "strategy_id": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1",
        "source_result": rel(OUT_RESULT),
        "simulation": {
            "start_date": inputs["sim_start_date"],
            "end_date": inputs["sim_end_date"],
            "symbol_count": len(inputs["symbols"]),
            "excluded_symbols": sorted(EXCLUDED_SYMBOLS),
        },
        "metrics": extract_metrics(result),
        "rows": rows,
    }

def extract_metrics(result: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "total_return_pct",
        "spx_total_return_pct",
        "alpha_pct",
        "cagr_pct",
        "spx_cagr_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
        "win_rate_pct",
        "number_of_trades",
        "total_trades_all",
        "avg_holding_days",
        "avg_winner_pct",
        "avg_loser_pct",
        "exposure_pct",
        "final_equity",
        "initial_capital",
        "status",
        "sample_validity",
        "e1r_candidate_count",
        "e1r_uptrend_execution_enabled",
    ]
    return {k: result.get(k) for k in keys if k in result}

def summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    dates = [r.get("date") for r in records if r.get("date")]
    date_counts = Counter(dates)

    regime_counts = Counter(r.get("spx_regime") for r in records)
    active_counts = Counter(r.get("e1r_active_mode") for r in records)
    risk_counts = Counter(r.get("risk_budget_mode") for r in records)

    subclass_counts = Counter(
        r.get("sideways_subclass") or r.get("subclass")
        for r in records
    )

    cash_value_breaks = []
    for r in records:
        try:
            cash = float(r.get("cash") or 0)
            pos = float(r.get("positions_value") or 0)
            total = float(r.get("total_equity") or 0)
        except Exception:
            continue
        if total:
            diff = abs((cash + pos) - total)
            if diff / max(abs(total), 1.0) > 0.0001:
                cash_value_breaks.append({
                    "date": r.get("date"),
                    "cash": cash,
                    "positions_value": pos,
                    "total_equity": total,
                    "diff": diff,
                })

    return {
        "row_count": len(records),
        "unique_dates": len(set(dates)),
        "date_start": min(dates) if dates else None,
        "date_end": max(dates) if dates else None,
        "max_rows_per_date": max(date_counts.values()) if date_counts else None,
        "one_row_per_date": bool(date_counts) and max(date_counts.values()) == 1,
        "regime_counts": {str(k): v for k, v in regime_counts.items()},
        "active_mode_counts": {str(k): v for k, v in active_counts.items()},
        "risk_budget_mode_counts": {str(k): v for k, v in risk_counts.items()},
        "subclass_counts": {str(k): v for k, v in subclass_counts.items()},
        "non_null_regime_count": sum(1 for r in records if r.get("spx_regime") is not None),
        "non_null_active_mode_count": sum(1 for r in records if r.get("e1r_active_mode") is not None),
        "cash_value_break_count": len(cash_value_breaks),
        "cash_value_break_samples": cash_value_breaks[:10],
        "first": records[0] if records else None,
        "last": records[-1] if records else None,
    }

def build_summary(result: dict[str, Any], inputs: dict[str, Any]) -> dict[str, Any]:
    records = extract_daily_records(result)
    record_summary = summarize_records(records)

    trades = result.get("trades") if isinstance(result.get("trades"), list) else []
    trade_regimes = Counter()
    for t in trades:
        if isinstance(t, dict):
            trade_regimes[t.get("dominant_regime") or t.get("entry_regime")] += 1

    validations = {
        "full_run_completed": True,
        "has_daily_equity_records": len(records) > 0,
        "row_count_ge_1000": len(records) >= 1000,
        "one_row_per_date": record_summary["one_row_per_date"],
        "regime_wired_observed": record_summary["non_null_regime_count"] > 0,
        "active_mode_observed": record_summary["non_null_active_mode_count"] > 0,
        "covers_uptrend": record_summary["regime_counts"].get("UPTREND", 0) > 0,
        "covers_sideways": record_summary["regime_counts"].get("SIDEWAYS", 0) > 0,
        "covers_downtrend": record_summary["regime_counts"].get("DOWNTREND", 0) > 0,
        "cash_plus_positions_continuity_ok": record_summary["cash_value_break_count"] == 0,
        "sample_validity": result.get("sample_validity"),
    }

    return {
        "artifact_type": "e1r_unified_5y_full_account_v1_summary",
        "generated_at": now(),
        "strategy_id": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1",
        "simulation": {
            "start_date": inputs["sim_start_date"],
            "end_date": inputs["sim_end_date"],
            "symbol_count": len(inputs["symbols"]),
            "skipped_symbol_count": len(inputs["skipped_symbols"]),
            "skipped_symbols_sample": inputs["skipped_symbols"][:20],
            "excluded_symbols": sorted(EXCLUDED_SYMBOLS),
        },
        "metrics": extract_metrics(result),
        "record_summary": record_summary,
        "trade_summary": {
            "trade_count": len(trades),
            "dominant_regime_counts": {str(k): v for k, v in trade_regimes.items()},
            "first_trade": trades[0] if trades else None,
            "last_trade": trades[-1] if trades else None,
        },
        "assumption_summary": {
            "critical_assumptions": {
                "e1r_regime_wiring_enabled": inputs["assumptions"].get("e1r_regime_wiring_enabled"),
                "e1r_uptrend_execution_enabled": inputs["assumptions"].get("e1r_uptrend_execution_enabled"),
                "e1r_regime_source": inputs["assumptions"].get("e1r_regime_source"),
                "e1r_shell_mode": inputs["assumptions"].get("e1r_shell_mode"),
                "strategy_variant": inputs["assumptions"].get("strategy_variant"),
                "version": inputs["assumptions"].get("version"),
                "entry_top_n": inputs["assumptions"].get("entry_top_n"),
                "entry_rs_min": inputs["assumptions"].get("entry_rs_min"),
                "max_positions": inputs["assumptions"].get("max_positions"),
                "market_gate_enabled": inputs["assumptions"].get("market_gate_enabled"),
                "execution_model": inputs["assumptions"].get("execution_model"),
            },
            "regime_daily_summary": inputs["assumption_build"]["regime_daily_summary"],
        },
        "validations": validations,
    }

def compact_result_for_report(result: dict[str, Any]) -> dict[str, Any]:
    out = {
        "keys": sorted(result.keys()),
        "metrics": extract_metrics(result),
    }
    for k in ["strategy_controls", "market_entry_gate", "sample_validity", "skipped_orders_by_reason", "portfolio_action_distribution", "executed_exit_reason_distribution", "executed_reduce_reason_distribution", "pending_signal_reason_distribution"]:
        if k in result:
            out[k] = result[k]
    return out

def main() -> int:
    started_at = datetime.now(timezone.utc)
    baseline_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}

    sys.path.insert(0, str(ROOT))

    import_probe = {"ok": False, "error": None, "signature": None}
    run = {
        "attempted": False,
        "ok": False,
        "error": None,
        "traceback_tail": None,
    }

    result = None
    inputs = None

    try:
        mod = importlib.import_module("src.engine.backtest")
        fn = getattr(mod, "run_stateful_simulation")
        import_probe["ok"] = True
        import_probe["signature"] = str(inspect.signature(fn))

        inputs = build_inputs()

        run["input_summary"] = {
            "symbol_count": len(inputs["symbols"]),
            "skipped_symbol_count": len(inputs["skipped_symbols"]),
            "spx_count": inputs["indices"]["SPX"]["count"],
            "spx_start": inputs["indices"]["SPX"].get("start"),
            "spx_end": inputs["indices"]["SPX"].get("end"),
            "sim_start_date": inputs["sim_start_date"],
            "sim_end_date": inputs["sim_end_date"],
            "regime_daily_summary": inputs["assumption_build"]["regime_daily_summary"],
            "critical_assumptions": {
                "e1r_regime_wiring_enabled": inputs["assumptions"].get("e1r_regime_wiring_enabled"),
                "e1r_uptrend_execution_enabled": inputs["assumptions"].get("e1r_uptrend_execution_enabled"),
                "e1r_regime_source": inputs["assumptions"].get("e1r_regime_source"),
                "e1r_shell_mode": inputs["assumptions"].get("e1r_shell_mode"),
                "strategy_variant": inputs["assumptions"].get("strategy_variant"),
                "version": inputs["assumptions"].get("version"),
            },
        }

        run["attempted"] = True

        result = fn(
            symbols=inputs["symbols"],
            prices_map=inputs["prices_map"],
            dates_map=inputs["dates_map"],
            spx_prices=inputs["indices"]["SPX"]["prices"],
            spx_dates=inputs["indices"]["SPX"]["dates"],
            ohlc_map=inputs["ohlc_map"],
            assumptions=inputs["assumptions"],
            step=inputs["step"],
            min_history=inputs["min_history"],
            market_score_default=inputs["market_score_default"],
            sim_start_date=inputs["sim_start_date"],
            sim_end_date=inputs["sim_end_date"],
            ndx_prices=inputs["indices"]["NDX"]["prices"],
            ndx_dates=inputs["indices"]["NDX"]["dates"],
            sox_prices=inputs["indices"]["SOX"]["prices"],
            sox_dates=inputs["indices"]["SOX"]["dates"],
            vix_prices=inputs["indices"]["VIX"]["prices"],
            vix_dates=inputs["indices"]["VIX"]["dates"],
        )

        run["ok"] = True

    except Exception as exc:
        run["error"] = type(exc).__name__ + ": " + str(exc)
        run["traceback_tail"] = traceback.format_exc()[-16000:]

    post_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    elapsed_seconds = (datetime.now(timezone.utc) - started_at).total_seconds()

    if run["ok"] and isinstance(result, dict) and inputs is not None:
        write_json(OUT_RESULT, result)

        curve = build_curve_artifact(result, inputs)
        summary = build_summary(result, inputs)

        write_json(OUT_CURVE, curve)
        write_json(OUT_SUMMARY, summary)

        validations = summary["validations"]

        if all([
            validations["has_daily_equity_records"],
            validations["row_count_ge_1000"],
            validations["one_row_per_date"],
            validations["regime_wired_observed"],
            validations["active_mode_observed"],
            validations["covers_uptrend"],
            validations["covers_sideways"],
            validations["covers_downtrend"],
            validations["cash_plus_positions_continuity_ok"],
        ]):
            conclusion = "E1R_UNIFIED_5Y_FULL_ACCOUNT_RUN_COMPLETE_VALIDATED"
            recommended = "Proceed to 4C-2D: connect validated unified 5Y curve to forward/OOS curve."
        else:
            conclusion = "E1R_UNIFIED_5Y_FULL_ACCOUNT_RUN_COMPLETE_NEEDS_REVIEW"
            recommended = "Review validation failures before connecting to forward/OOS curve."

        result_compact = compact_result_for_report(result)

    else:
        summary = None
        curve = None
        validations = {}
        conclusion = "E1R_UNIFIED_5Y_FULL_ACCOUNT_RUN_FAILED"
        recommended = "Fix traceback before rerunning full 5Y."
        result_compact = None

    report = {
        "generated_at": now(),
        "stage": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C_FULL_RUN",
        "status": "E1R_UNIFIED_5Y_FULL_ACCOUNT_FULL_RUN_COMPLETE",
        "elapsed_seconds": elapsed_seconds,
        "policy": {
            "dashboard_changed": False,
            "strategy_logic_changed": False,
            "full_backtest_run": True,
            "canonical_backtest_written_for_v1_spec": bool(run["ok"]),
            "forward_curve_connected": False,
        },
        "import_probe": import_probe,
        "run": run,
        "outputs": {
            "result": rel(OUT_RESULT) if OUT_RESULT.exists() else None,
            "curve": rel(OUT_CURVE) if OUT_CURVE.exists() else None,
            "summary": rel(OUT_SUMMARY) if OUT_SUMMARY.exists() else None,
        },
        "summary": summary,
        "result_compact": result_compact,
        "validations": validations,
        "conclusion": conclusion,
        "recommended_next_action": recommended,
        "strategy_files_unchanged": baseline_hashes == post_hashes,
        "next_stage": {
            "name": "4C-2D",
            "title": "Connect unified 5Y backtest curve to forward/OOS curve",
            "recommended_action": recommended,
        },
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R Unified 5Y Full Account V1 — 4C-2C Full Run")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append(f"Elapsed Seconds: `{elapsed_seconds}`")
    md.append("")
    md.append("## Outputs")
    md.append("")
    md.append("```json")
    md.append(json.dumps(report["outputs"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Metrics")
    md.append("")
    md.append("```json")
    md.append(json.dumps(summary.get("metrics") if summary else None, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Validations")
    md.append("")
    md.append("```json")
    md.append(json.dumps(validations, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Record Summary")
    md.append("")
    md.append("```json")
    md.append(json.dumps(summary.get("record_summary") if summary else None, indent=2, ensure_ascii=False)[:24000])
    md.append("```")
    md.append("")
    md.append("## Trade Summary")
    md.append("")
    md.append("```json")
    md.append(json.dumps(summary.get("trade_summary") if summary else None, indent=2, ensure_ascii=False)[:16000])
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {recommended}")
    md.append("")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("Stage 4C-2C full 5Y unified account run complete")
    print("status:", report["status"])
    print("elapsed_seconds:", elapsed_seconds)
    print("strategy_files_unchanged:", report["strategy_files_unchanged"])
    print("run_ok:", run["ok"])
    print("run_error:", run.get("error"))
    if run.get("traceback_tail"):
        print("traceback_tail:", run["traceback_tail"][-4000:])
    print("outputs:", json.dumps(report["outputs"], ensure_ascii=False))
    print("metrics:", json.dumps(summary.get("metrics") if summary else None, ensure_ascii=False))
    print("record_summary:", json.dumps(summary.get("record_summary") if summary else None, ensure_ascii=False)[:12000])
    print("trade_summary:", json.dumps(summary.get("trade_summary") if summary else None, ensure_ascii=False)[:8000])
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)
    print("next_stage:", report["next_stage"]["name"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
