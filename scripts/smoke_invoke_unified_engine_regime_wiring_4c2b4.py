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

REPORT_JSON = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2B4_REGIME_WIRING_SMOKE_REPORT.json"
REPORT_MD = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2B4_REGIME_WIRING_SMOKE_REPORT.md"

REGIME_PATH = ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json"

FROZEN_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

ASSUMPTION_SOURCE_CANDIDATES = [
    ROOT / "exports/portfolio_backtest.json",
    ROOT / "exports/backtest.json",
    ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2B3_SMOKE_OHLC_CONTRACT_REPORT.json",
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

def find_stock_files(limit: int = 20) -> list[Path]:
    files = []
    for d in STOCK_DIR_CANDIDATES:
        if not d.exists():
            continue
        for p in sorted(d.glob("*.json")):
            stem = p.stem.upper()
            if stem.startswith("^") or stem in {"SPX", "NDX", "SOX", "VIX", "SPY", "QQQ"}:
                continue
            files.append(p)
    return files[:limit]

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

    # Critical overrides for this stage: verify regime wiring, not legacy-only run.
    assumptions["e1r_regime_wiring_enabled"] = True
    assumptions["e1r_regime_daily"] = regime_daily
    assumptions["e1r_regime_source"] = rel(REGIME_PATH)
    assumptions["e1r_shell_mode"] = "regime_wiring_smoke"
    assumptions["e1r_uptrend_execution_enabled"] = True
    assumptions["strategy_variant"] = "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_REGIME_WIRING_SMOKE"
    assumptions["version"] = "4C-2B-4-regime-wiring-smoke"

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
        "sample_first": regime_daily[dates[0]] if dates else None,
        "sample_last": regime_daily[dates[-1]] if dates else None,
    }

def build_inputs(smoke_symbols_limit: int = 12) -> dict[str, Any]:
    stock_files = find_stock_files(smoke_symbols_limit)
    symbols, prices_map, dates_map, ohlc_map = [], {}, {}, {}

    for p in stock_files:
        sym = p.stem.upper()
        dates, closes, ohlc = normalize_symbol_file(p)
        if len(dates) < 260:
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

    spx_dates = indices["SPX"]["dates"]

    # Choose a window that is likely to include UPTREND and maybe non-UPTREND.
    # This remains a smoke test, not full 5Y.
    sim_start_date = "2022-01-03" if "2022-01-03" in set(spx_dates) else (spx_dates[420] if len(spx_dates) > 500 else None)
    sim_end_date = "2022-04-29" if "2022-04-29" in set(spx_dates) else (spx_dates[min(500, len(spx_dates)-1)] if len(spx_dates) > 500 else None)

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
    }

def summarize_result(result: Any) -> dict[str, Any]:
    out = {"type": type(result).__name__}
    if isinstance(result, dict):
        out["keys"] = sorted(result.keys())
        metrics = {}
        for k in [
            "total_return_pct", "spx_total_return_pct", "spx_return_pct",
            "alpha_pct", "max_drawdown_pct", "profit_factor", "sharpe_ratio",
            "number_of_trades", "total_trades_all", "final_equity",
            "initial_capital", "exposure_pct", "status", "sample_validity",
            "e1r_candidate_count", "e1r_uptrend_execution_enabled",
        ]:
            if k in result:
                metrics[k] = result.get(k)
        out["metric_like_values"] = metrics

        lists = {}
        for k, v in result.items():
            if isinstance(v, list):
                item = {"length": len(v), "first_type": type(v[0]).__name__ if v else None}
                if v and isinstance(v[0], dict):
                    item["first_keys"] = sorted(v[0].keys())[:120]
                    item["first"] = v[0]
                    item["last"] = v[-1]
                lists[k] = item
        out["lists"] = lists

        dicts = {}
        for k, v in result.items():
            if isinstance(v, dict):
                dicts[k] = {"keys": sorted(v.keys())[:120], "len": len(v)}
        out["dicts"] = dicts
    else:
        out["repr"] = repr(result)[:2000]
    return out

def summarize_daily_regime_output(result_summary: dict[str, Any]) -> dict[str, Any]:
    daily_info = result_summary.get("lists", {}).get("daily_equity_records", {})
    first = daily_info.get("first")
    last = daily_info.get("last")
    # Full list is not in summary, so this gives only smoke-level proof points.
    return {
        "daily_equity_records_length": daily_info.get("length"),
        "first_spx_regime": first.get("spx_regime") if isinstance(first, dict) else None,
        "first_e1r_active_mode": first.get("e1r_active_mode") if isinstance(first, dict) else None,
        "last_spx_regime": last.get("spx_regime") if isinstance(last, dict) else None,
        "last_e1r_active_mode": last.get("e1r_active_mode") if isinstance(last, dict) else None,
        "first": first,
        "last": last,
    }

def main() -> int:
    baseline_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    sys.path.insert(0, str(ROOT))

    import_probe = {"ok": False, "error": None, "signature": None}
    smoke = {
        "attempted": False,
        "ok": False,
        "error": None,
        "traceback_tail": None,
        "input_summary": {},
        "result_summary": {},
        "daily_regime_output_summary": {},
    }

    try:
        mod = importlib.import_module("src.engine.backtest")
        fn = getattr(mod, "run_stateful_simulation")
        import_probe["ok"] = True
        import_probe["signature"] = str(inspect.signature(fn))

        inputs = build_inputs()

        provenance = inputs["assumption_build"]["provenance"]
        provenance_counts = {}
        for v in provenance.values():
            provenance_counts[v] = provenance_counts.get(v, 0) + 1

        ohlc_contract_sample = {}
        for s in inputs["symbols"][:3]:
            o = inputs["ohlc_map"].get(s, {})
            ohlc_contract_sample[s] = {
                "type": type(o).__name__,
                "keys": sorted(o.keys()) if isinstance(o, dict) else None,
                "lengths": {k: len(v) for k, v in o.items()} if isinstance(o, dict) else None,
            }

        smoke["input_summary"] = {
            "symbol_count": len(inputs["symbols"]),
            "symbols": inputs["symbols"],
            "spx_count": inputs["indices"]["SPX"]["count"],
            "spx_start": inputs["indices"]["SPX"].get("start"),
            "spx_end": inputs["indices"]["SPX"].get("end"),
            "sim_start_date": inputs["sim_start_date"],
            "sim_end_date": inputs["sim_end_date"],
            "required_assumption_keys_count": len(inputs["assumption_usage"].get("keys", [])),
            "assumption_provenance_counts": provenance_counts,
            "assumption_recovery_sources": inputs["assumption_build"]["recovery"]["sources"][:10],
            "regime_daily_summary": inputs["assumption_build"]["regime_daily_summary"],
            "ohlc_contract_sample": ohlc_contract_sample,
            "critical_assumptions": {
                "e1r_regime_wiring_enabled": inputs["assumptions"].get("e1r_regime_wiring_enabled"),
                "e1r_uptrend_execution_enabled": inputs["assumptions"].get("e1r_uptrend_execution_enabled"),
                "e1r_regime_source": inputs["assumptions"].get("e1r_regime_source"),
                "e1r_shell_mode": inputs["assumptions"].get("e1r_shell_mode"),
                "strategy_variant": inputs["assumptions"].get("strategy_variant"),
                "version": inputs["assumptions"].get("version"),
            },
        }

        smoke["attempted"] = True

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

        smoke["ok"] = True
        smoke["result_summary"] = summarize_result(result)
        smoke["daily_regime_output_summary"] = summarize_daily_regime_output(smoke["result_summary"])

    except Exception as exc:
        if not import_probe["ok"]:
            import_probe["error"] = type(exc).__name__ + ": " + str(exc)
        smoke["error"] = type(exc).__name__ + ": " + str(exc)
        smoke["traceback_tail"] = traceback.format_exc()[-12000:]

    post_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}

    result_lists = smoke.get("result_summary", {}).get("lists", {}) or {}
    has_daily_records = any(k in result_lists for k in ["daily_records", "daily_equity_records", "rows", "equity_curve", "curve"])

    daily_out = smoke.get("daily_regime_output_summary", {})
    regime_wired_observed = (
        daily_out.get("first_spx_regime") is not None
        or daily_out.get("last_spx_regime") is not None
        or daily_out.get("first_e1r_active_mode") is not None
        or daily_out.get("last_e1r_active_mode") is not None
    )

    if import_probe["ok"] and smoke["ok"] and has_daily_records and regime_wired_observed:
        conclusion = "STATEFUL_ENGINE_REGIME_WIRING_SMOKE_OK_READY_FOR_FULL_5Y_UNIFIED_RUN"
        recommended = "Proceed to 4C-2C: run full 5Y unified full-account backtest with regime wiring enabled."
    elif import_probe["ok"] and smoke["ok"] and has_daily_records:
        conclusion = "STATEFUL_ENGINE_SMOKE_OK_BUT_REGIME_OUTPUT_NOT_OBSERVED"
        recommended = "Inspect backtest.py regime field contract; regime_daily may need alternate key shape before full E1R run."
    elif import_probe["ok"] and smoke["ok"]:
        conclusion = "STATEFUL_ENGINE_REGIME_SMOKE_OK_BUT_OUTPUT_CONTRACT_NEEDS_MAPPING"
        recommended = "Map returned object fields to daily equity contract before full 5Y."
    elif import_probe["ok"]:
        conclusion = "PACKAGE_IMPORT_OK_REGIME_SMOKE_FAILED"
        recommended = "Use traceback to fix regime wiring input contract, then retry."
    else:
        conclusion = "PACKAGE_IMPORT_FAILED"
        recommended = "Fix package import first."

    report = {
        "generated_at": now(),
        "stage": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2B4_REGIME_WIRING_SMOKE",
        "status": "E1R_UNIFIED_ENGINE_REGIME_WIRING_SMOKE_COMPLETE_NO_FULL_BACKTEST",
        "policy": {
            "dashboard_changed": False,
            "strategy_logic_changed": False,
            "full_backtest_run": False,
            "canonical_backtest_written": False,
            "smoke_invoke_only": True,
        },
        "import_probe": import_probe,
        "smoke": smoke,
        "has_daily_records_like_output": has_daily_records,
        "regime_wired_observed": regime_wired_observed,
        "conclusion": conclusion,
        "recommended_next_action": recommended,
        "strategy_files_unchanged": baseline_hashes == post_hashes,
        "next_stage": {
            "name": "4C-2C",
            "title": "Run full 5Y unified full-account backtest with regime wiring",
            "recommended_action": recommended,
        },
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R Unified 5Y Full Account V1 — 4C-2B-4 Regime Wiring Smoke")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append("- Status: `E1R_UNIFIED_ENGINE_REGIME_WIRING_SMOKE_COMPLETE_NO_FULL_BACKTEST`")
    md.append("- Full backtest run: `False`")
    md.append("- Strategy logic changed: `False`")
    md.append("")
    md.append("## Key Checks")
    md.append("")
    md.append("```json")
    md.append(json.dumps({
        "package_import_ok": import_probe.get("ok"),
        "smoke_ok": smoke.get("ok"),
        "has_daily_records_like_output": has_daily_records,
        "regime_wired_observed": regime_wired_observed,
        "critical_assumptions": smoke.get("input_summary", {}).get("critical_assumptions"),
        "daily_regime_output_summary": smoke.get("daily_regime_output_summary"),
    }, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Smoke Summary")
    md.append("")
    md.append("```json")
    md.append(json.dumps(smoke, indent=2, ensure_ascii=False)[:38000])
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {recommended}")
    md.append("")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("Stage 4C-2B-4 regime wiring smoke complete")
    print("status:", report["status"])
    print("strategy_files_unchanged:", report["strategy_files_unchanged"])
    print("package_import_ok:", import_probe["ok"])
    print("smoke_attempted:", smoke["attempted"])
    print("smoke_ok:", smoke["ok"])
    print("smoke_error:", smoke.get("error"))
    if smoke.get("traceback_tail"):
        print("smoke_traceback_tail:", smoke["traceback_tail"][-3000:])
    print("input_summary:", json.dumps(smoke.get("input_summary"), ensure_ascii=False)[:12000])
    print("daily_regime_output_summary:", json.dumps(smoke.get("daily_regime_output_summary"), ensure_ascii=False)[:8000])
    print("result_summary:", json.dumps(smoke.get("result_summary"), ensure_ascii=False)[:12000])
    print("has_daily_records_like_output:", has_daily_records)
    print("regime_wired_observed:", regime_wired_observed)
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)
    print("next_stage:", report["next_stage"]["name"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
