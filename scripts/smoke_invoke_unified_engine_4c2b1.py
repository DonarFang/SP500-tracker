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

ROOT = Path(__file__).resolve().parents[1]
BACKTEST = ROOT / "src/engine/backtest.py"

REPORT_JSON = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2B1_SMOKE_RETRY_REPORT.json"
REPORT_MD = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2B1_SMOKE_RETRY_REPORT.md"

FROZEN_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
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

BASE_ASSUMPTIONS = {
    "initial_capital": 100000.0,
    "max_positions": 10,
    "buy_size": 1.0,
    "sell_size": 1.0,
    "add_size": 0.5,
    "reduce_size": 0.5,
    "position_size_pct": 0.10,
    "min_holding_days": 10,
    "candidate_top_n": 10,
    "entry_top_n": 10,
    "entry_rs_min": 60,
    "leader_score_exit": 60,
    "market_gate_enabled": True,
    "market_entry_gate": "slope_leadership",
    "execution_model": "next_close",
    "qualified_entry_enabled": True,
    "qualified_states": ["UPTREND", "SIDEWAYS"],
    "partial_take_profit": False,
    "rank_based_exit": True,
    "relative_stop_enabled": False,
    "relative_stop_underperform_pct": -8.0,
    "e1r_unified_smoke": True,
}

FALLBACK_DEFAULTS = {
    "buy_size": 1.0,
    "sell_size": 1.0,
    "add_size": 0.5,
    "reduce_size": 0.5,
    "max_positions": 10,
    "min_hold": 10,
    "min_holding_days": 10,
    "candidate_top_n": 10,
    "entry_top_n": 10,
    "entry_rs_min": 60,
    "leader_score_exit": 60,
    "exit_score": 60,
    "risk_budget": 1.0,
    "risk_budget_mode": "full",
    "initial_capital": 100000.0,
    "commission_pct": 0.0,
    "slippage_pct": 0.0,
    "market_gate_enabled": True,
    "partial_take_profit": False,
    "rank_based_exit": True,
    "qualified_entry_enabled": True,
    "relative_stop_enabled": False,
    "relative_stop_underperform_pct": -8.0,
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

def normalize_symbol_file(p: Path) -> tuple[list[str], list[float], list[dict[str, Any]]]:
    obj = read_json(p)
    bars = extract_bars(obj)
    rows = []
    dates = []
    closes = []
    for b in bars:
        d = b.get("date")
        c = b.get("close")
        if d is None or c is None:
            continue
        try:
            cf = float(c)
        except Exception:
            continue
        dates.append(str(d)[:10])
        closes.append(cf)
        rows.append({
            "date": str(d)[:10],
            "open": float(b.get("open", cf)) if b.get("open") is not None else cf,
            "high": float(b.get("high", cf)) if b.get("high") is not None else cf,
            "low": float(b.get("low", cf)) if b.get("low") is not None else cf,
            "close": cf,
            "volume": float(b.get("volume", 0) or 0),
        })
    return dates, closes, rows

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
        return {"function_found": False, "keys": [], "subscript_hits": []}

    keys = []
    hits = []

    for node in ast.walk(target):
        # a["key"] or assumptions["key"]
        if isinstance(node, ast.Subscript):
            base = None
            if isinstance(node.value, ast.Name):
                base = node.value.id
            if base in {"a", "assumptions"}:
                key = None
                s = node.slice
                if isinstance(s, ast.Constant):
                    key = s.value
                elif hasattr(ast, "Index") and isinstance(s, ast.Index) and isinstance(s.value, ast.Constant):
                    key = s.value.value
                if isinstance(key, str):
                    keys.append(key)
                    hits.append({"line": getattr(node, "lineno", None), "base": base, "key": key})

        # a.get("key") or assumptions.get("key")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "get" and isinstance(node.func.value, ast.Name):
                base = node.func.value.id
                if base in {"a", "assumptions"} and node.args:
                    arg0 = node.args[0]
                    if isinstance(arg0, ast.Constant) and isinstance(arg0.value, str):
                        keys.append(arg0.value)
                        hits.append({"line": getattr(node, "lineno", None), "base": base, "key": arg0.value, "method": "get"})

    return {
        "function_found": True,
        "keys": sorted(set(keys)),
        "subscript_hits": sorted(hits, key=lambda x: (x.get("line") or 0, x.get("key") or "")),
    }

def build_assumptions(required_keys: list[str]) -> dict[str, Any]:
    a = dict(BASE_ASSUMPTIONS)
    missing_filled = {}

    for k in required_keys:
        if k not in a:
            if k in FALLBACK_DEFAULTS:
                a[k] = FALLBACK_DEFAULTS[k]
                missing_filled[k] = FALLBACK_DEFAULTS[k]
            else:
                # Conservative generic defaults by key name.
                lk = k.lower()
                if "enabled" in lk:
                    a[k] = False
                elif "states" in lk:
                    a[k] = ["UPTREND", "SIDEWAYS"]
                elif "mode" in lk:
                    a[k] = "default"
                elif "pct" in lk or "score" in lk or "threshold" in lk:
                    a[k] = 0.0
                elif "days" in lk or "count" in lk or "top_n" in lk:
                    a[k] = 0
                else:
                    a[k] = None
                missing_filled[k] = a[k]

    return a, missing_filled

def build_inputs(smoke_symbols_limit: int = 12) -> dict[str, Any]:
    stock_files = find_stock_files(smoke_symbols_limit)
    symbols = []
    prices_map = {}
    dates_map = {}
    ohlc_map = {}

    for p in stock_files:
        sym = p.stem.upper()
        dates, closes, rows = normalize_symbol_file(p)
        if len(dates) < 260:
            continue
        symbols.append(sym)
        prices_map[sym] = closes
        dates_map[sym] = dates
        ohlc_map[sym] = rows

    indices = {}
    for name, path in INDEX_PATHS.items():
        if path.exists():
            d, c, r = normalize_symbol_file(path)
            indices[name] = {"dates": d, "prices": c, "rows": r, "count": len(d), "start": d[0] if d else None, "end": d[-1] if d else None}
        else:
            indices[name] = {"dates": [], "prices": [], "rows": [], "count": 0, "missing": True}

    spx_dates = indices["SPX"]["dates"]
    sim_start_date = spx_dates[260] if len(spx_dates) > 360 else None
    sim_end_date = spx_dates[min(320, len(spx_dates)-1)] if len(spx_dates) > 360 else None

    assumption_usage = extract_assumption_key_usage()
    assumptions, missing_filled = build_assumptions(assumption_usage.get("keys", []))

    return {
        "symbols": symbols,
        "prices_map": prices_map,
        "dates_map": dates_map,
        "ohlc_map": ohlc_map,
        "indices": indices,
        "assumptions": assumptions,
        "assumption_usage": assumption_usage,
        "missing_filled": missing_filled,
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
        ]:
            if k in result:
                metrics[k] = result.get(k)
        out["metric_like_values"] = metrics

        lists = {}
        for k, v in result.items():
            if isinstance(v, list):
                item = {"length": len(v), "first_type": type(v[0]).__name__ if v else None}
                if v and isinstance(v[0], dict):
                    item["first_keys"] = sorted(v[0].keys())[:100]
                    item["first"] = v[0]
                    item["last"] = v[-1]
                lists[k] = item
        out["lists"] = lists

        dicts = {}
        for k, v in result.items():
            if isinstance(v, dict):
                dicts[k] = {"keys": sorted(v.keys())[:100], "len": len(v)}
        out["dicts"] = dicts
    else:
        out["repr"] = repr(result)[:2000]
    return out

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
    }

    try:
        mod = importlib.import_module("src.engine.backtest")
        fn = getattr(mod, "run_stateful_simulation")
        import_probe["ok"] = True
        import_probe["signature"] = str(inspect.signature(fn))

        inputs = build_inputs()

        smoke["input_summary"] = {
            "symbol_count": len(inputs["symbols"]),
            "symbols": inputs["symbols"],
            "spx_count": inputs["indices"]["SPX"]["count"],
            "spx_start": inputs["indices"]["SPX"].get("start"),
            "spx_end": inputs["indices"]["SPX"].get("end"),
            "sim_start_date": inputs["sim_start_date"],
            "sim_end_date": inputs["sim_end_date"],
            "required_assumption_keys_count": len(inputs["assumption_usage"].get("keys", [])),
            "required_assumption_keys": inputs["assumption_usage"].get("keys", []),
            "missing_filled": inputs["missing_filled"],
            "final_assumption_keys": sorted(inputs["assumptions"].keys()),
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

    except Exception as exc:
        if not import_probe["ok"]:
            import_probe["error"] = type(exc).__name__ + ": " + str(exc)
        smoke["error"] = type(exc).__name__ + ": " + str(exc)
        smoke["traceback_tail"] = traceback.format_exc()[-10000:]

    post_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}

    result_lists = smoke.get("result_summary", {}).get("lists", {}) or {}
    has_daily_records = any(k in result_lists for k in ["daily_records", "rows", "equity_curve", "curve"])

    if import_probe["ok"] and smoke["ok"] and has_daily_records:
        conclusion = "STATEFUL_ENGINE_SMOKE_OK_READY_FOR_FULL_5Y_RUN"
        recommended = "Proceed to 4C-2C: run full 5Y unified account backtest with all symbols and full aligned 5Y date window."
    elif import_probe["ok"] and smoke["ok"]:
        conclusion = "STATEFUL_ENGINE_SMOKE_OK_BUT_OUTPUT_CONTRACT_NEEDS_MAPPING"
        recommended = "Map returned object fields to daily equity contract, then run full 5Y."
    elif import_probe["ok"]:
        conclusion = "PACKAGE_IMPORT_OK_SMOKE_RETRY_FAILED"
        recommended = "Use traceback to add remaining missing assumptions or adjust input contract, then retry."
    else:
        conclusion = "PACKAGE_IMPORT_FAILED"
        recommended = "Fix package import first."

    report = {
        "generated_at": now(),
        "stage": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2B1_SMOKE_RETRY",
        "status": "E1R_UNIFIED_ENGINE_SMOKE_RETRY_COMPLETE_NO_FULL_BACKTEST",
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
        "conclusion": conclusion,
        "recommended_next_action": recommended,
        "strategy_files_unchanged": baseline_hashes == post_hashes,
        "next_stage": {
            "name": "4C-2C",
            "title": "Run full 5Y unified account backtest",
            "recommended_action": recommended,
        },
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R Unified 5Y Full Account V1 — 4C-2B-1 Smoke Retry")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append("- Status: `E1R_UNIFIED_ENGINE_SMOKE_RETRY_COMPLETE_NO_FULL_BACKTEST`")
    md.append("- Full backtest run: `False`")
    md.append("- Strategy logic changed: `False`")
    md.append("")
    md.append("## Import Probe")
    md.append("")
    md.append("```json")
    md.append(json.dumps(import_probe, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Smoke")
    md.append("")
    md.append("```json")
    md.append(json.dumps(smoke, indent=2, ensure_ascii=False)[:32000])
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {recommended}")
    md.append("")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("Stage 4C-2B-1 smoke retry complete")
    print("status:", report["status"])
    print("strategy_files_unchanged:", report["strategy_files_unchanged"])
    print("package_import_ok:", import_probe["ok"])
    print("import_signature:", import_probe.get("signature"))
    print("smoke_attempted:", smoke["attempted"])
    print("smoke_ok:", smoke["ok"])
    print("smoke_error:", smoke.get("error"))
    if smoke.get("traceback_tail"):
        print("smoke_traceback_tail:", smoke["traceback_tail"][-3000:])
    print("input_summary:", json.dumps(smoke.get("input_summary"), ensure_ascii=False))
    print("result_summary:", json.dumps(smoke.get("result_summary"), ensure_ascii=False)[:8000])
    print("has_daily_records_like_output:", has_daily_records)
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)
    print("next_stage:", report["next_stage"]["name"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
