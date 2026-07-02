#!/usr/bin/env python3
"""
E1-R Phase 3I SIDEWAYS Candidate Quality Decomposition Diagnostic

Diagnostic only. Does not modify trading logic, orders, exports/backtest.json,
or any strategy implementation.

Purpose:
Decompose SIDEWAYS / DOWNTREND STC candidates into more useful watchlist types:
- Upgrade Watch: possible early form of future UPTREND leaders
- Defensive Strength: strong relative performance but likely defensive/risk-off leadership
- Range Rotation: sideways rotation/noise
- Event/Failed-Flow Risk: volume without healthy close/structure confirmation

This script protects the existing UPTREND Confirmed execution path. It only evaluates
non-UPTREND candidates from the Phase 3G STC screen and Phase 3H market-flow metrics.

Expected inputs after `python3 run_backtest.py`:
- exports/backtest.json with E1_AUDITED_G4_MINHOLD10 and E1R_REGIME_AWARE_V0_1
- data/prices/*.json
- scripts/e1r_phase3g_smooth_trend_confirmation_diagnostic.py
- scripts/e1r_phase3h_market_flow_confirmation_diagnostic.py
- data/research/e1_5y/regimes/spx_regime_daily.json
- optional: data/sp500_constituents.json for sector mapping
- optional: exports/e1r_candidates.json for future upgrade-to-confirmed diagnostics

Outputs:
- data/research/e1r/e1r_phase3i_sideways_quality_decomposition_diagnostic.json
- data/research/e1r/E1R_PHASE3I_SIDEWAYS_QUALITY_DECOMPOSITION_REPORT.md
"""
from __future__ import annotations

import importlib.util
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

E1_ID = "E1_AUDITED_G4_MINHOLD10"
E1R_ID = "E1R_REGIME_AWARE_V0_1"

BACKTEST_PATH = Path("exports/backtest.json")
PHASE3G_SCRIPT = Path("scripts/e1r_phase3g_smooth_trend_confirmation_diagnostic.py")
PHASE3H_SCRIPT = Path("scripts/e1r_phase3h_market_flow_confirmation_diagnostic.py")
REGIME_PATH = Path("data/research/e1_5y/regimes/spx_regime_daily.json")
CONSTITUENTS_PATH = Path("data/sp500_constituents.json")
E1R_CANDIDATES_PATH = Path("exports/e1r_candidates.json")

OUT_DIR = Path("data/research/e1r")
OUT_JSON = OUT_DIR / "e1r_phase3i_sideways_quality_decomposition_diagnostic.json"
OUT_MD = OUT_DIR / "E1R_PHASE3I_SIDEWAYS_QUALITY_DECOMPOSITION_REPORT.md"

HORIZONS = [5, 10, 20, 30]
DEDUP_GAP_DAYS = 5
TARGET_BASE_RULES = ["SIDEWAYS_STC80", "DOWNTREND_STC90"]
INDEX_OR_PROXY_SYMBOLS = {"^GSPC", "GSPC", "SPX", "^NDX", "NDX", "^VIX", "VIX", "_VIX", "^SOX", "SOX", "SPY", "QQQ"}
DEFENSIVE_SECTORS = {"Utilities", "Consumer Defensive", "Consumer Staples", "Health Care", "Healthcare", "Real Estate"}


def load_module(path: Path, name: str):
    if not path.exists():
        raise FileNotFoundError(f"Missing required script: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_json(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing required input: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def maybe_load_json(path: Path) -> Any | None:
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def num(x: Any, default: float = 0.0) -> float:
    try:
        if x is None:
            return default
        y = float(x)
        return y if math.isfinite(y) else default
    except Exception:
        return default


def round_or_none(x: Any, nd: int = 3) -> Any:
    try:
        if x is None:
            return None
        y = float(x)
        return round(y, nd) if math.isfinite(y) else None
    except Exception:
        return None


def pct_str(x: Any) -> str:
    try:
        if x is None:
            return "n/a"
        y = float(x)
        if not math.isfinite(y):
            return "n/a"
        return f"{y:+.2f}%"
    except Exception:
        return "n/a"


def avg(xs: list[Any]) -> float | None:
    vals = [float(x) for x in xs if isinstance(x, (int, float)) and math.isfinite(float(x))]
    return statistics.mean(vals) if vals else None


def safe_variant_results(backtest: dict[str, Any]) -> dict[str, Any]:
    try:
        return backtest["backtest"]["results"]["layer_d"]["variant_results"]
    except KeyError as exc:
        raise KeyError("Cannot locate backtest.results.layer_d.variant_results in exports/backtest.json") from exc


def load_sector_map() -> dict[str, str]:
    obj = maybe_load_json(CONSTITUENTS_PATH)
    if obj is None:
        return {}
    rows = obj
    if isinstance(obj, dict):
        for key in ["constituents", "data", "symbols", "sp500", "members"]:
            if isinstance(obj.get(key), list):
                rows = obj[key]
                break
        else:
            rows = list(obj.values())
    out: dict[str, str] = {}
    if isinstance(rows, list):
        for r in rows:
            if not isinstance(r, dict):
                continue
            sym = r.get("symbol") or r.get("ticker") or r.get("Symbol") or r.get("Ticker")
            sector = r.get("sector") or r.get("Sector") or r.get("gics_sector") or r.get("GICS Sector")
            if sym and sector:
                out[str(sym).replace(".", "-")] = str(sector)
                out[str(sym)] = str(sector)
    return out


def pct_return(a: float | None, b: float | None) -> float | None:
    if a is None or b is None or a <= 0 or b <= 0:
        return None
    return (b / a - 1.0) * 100.0


def clv_metrics(row: dict[str, Any], rec: dict[str, list[Any]] | None) -> dict[str, Any]:
    d = row.get("date")
    if not d or not rec:
        return {"clv_available": False}
    dates = rec.get("dates", [])
    try:
        i = {x: j for j, x in enumerate(dates)}.get(str(d))
    except Exception:
        i = None
    if i is None:
        return {"clv_available": False}
    closes = rec.get("close", [])
    highs = rec.get("high", [])
    lows = rec.get("low", [])
    clvs = []
    for k in range(max(0, i - 4), i + 1):
        if k >= len(closes) or k >= len(highs) or k >= len(lows):
            continue
        c, h, l = closes[k], highs[k], lows[k]
        if not isinstance(c, (int, float)) or not isinstance(h, (int, float)) or not isinstance(l, (int, float)):
            continue
        if h > l:
            clvs.append((float(c) - float(l)) / (float(h) - float(l)))
    if not clvs:
        return {"clv_available": False}
    return {
        "clv_available": True,
        "clv_latest": round_or_none(clvs[-1], 4),
        "clv_5d_avg": round_or_none(avg(clvs), 4),
        "close_location_pass": bool((clvs[-1] >= 0.60) or ((avg(clvs) or 0) >= 0.55)),
    }


def spx_context(date: str, spx_dates: list[str], spx_closes: list[float]) -> dict[str, Any]:
    idx = {d: i for i, d in enumerate(spx_dates)}
    i = idx.get(date)
    if i is None or i < 60:
        return {"sideways_subregime": "UNKNOWN"}
    c = spx_closes[i]
    ma20 = avg(spx_closes[i - 19:i + 1])
    ma50 = avg(spx_closes[i - 49:i + 1])
    ma20_prev = avg(spx_closes[i - 24:i - 4]) if i >= 64 else None
    r10 = pct_return(spx_closes[i - 10], c) if i >= 10 else None
    r20 = pct_return(spx_closes[i - 20], c) if i >= 20 else None
    ma20_slope20 = ((ma20 / ma20_prev - 1.0) * 100.0) if ma20 and ma20_prev and ma20_prev > 0 else None

    recovery_score = 0
    deterioration_score = 0
    if r10 is not None and r10 > 1.0: recovery_score += 1
    if r20 is not None and r20 > 2.0: recovery_score += 1
    if ma20_slope20 is not None and ma20_slope20 > 0: recovery_score += 1
    if ma20 is not None and c > ma20: recovery_score += 1
    if ma20 is not None and ma50 is not None and ma20 > ma50: recovery_score += 1
    if r10 is not None and r10 < -1.0: deterioration_score += 1
    if r20 is not None and r20 < -2.0: deterioration_score += 1
    if ma20_slope20 is not None and ma20_slope20 < 0: deterioration_score += 1
    if ma20 is not None and c < ma20: deterioration_score += 1
    if ma20 is not None and ma50 is not None and ma20 < ma50: deterioration_score += 1

    if recovery_score >= 4 and recovery_score > deterioration_score:
        sub = "SIDEWAYS_RECOVERY"
    elif deterioration_score >= 4 and deterioration_score > recovery_score:
        sub = "SIDEWAYS_DETERIORATION"
    else:
        sub = "SIDEWAYS_RANGE"
    return {
        "sideways_subregime": sub,
        "spx_return_10d_pct": round_or_none(r10, 3),
        "spx_return_20d_pct": round_or_none(r20, 3),
        "spx_ma20_slope20_pct": round_or_none(ma20_slope20, 3),
        "spx_close_gt_ma20": bool(ma20 is not None and c > ma20),
        "spx_ma20_gt_ma50": bool(ma20 is not None and ma50 is not None and ma20 > ma50),
        "recovery_score": recovery_score,
        "deterioration_score": deterioration_score,
    }


def sector_confirmation(row: dict[str, Any], sector_map: dict[str, str], price_map: dict[str, tuple[list[str], list[float]]], spx_dates: list[str], spx_closes: list[float]) -> dict[str, Any]:
    sym = str(row.get("symbol") or "")
    sector = sector_map.get(sym)
    if not sector:
        return {"sector": None, "sector_confirmation_available": False, "sector_confirmed": False}
    d = str(row.get("date"))
    spx_idx = {x: i for i, x in enumerate(spx_dates)}
    si = spx_idx.get(d)
    if si is None or si < 20:
        return {"sector": sector, "sector_confirmation_available": False, "sector_confirmed": False}
    spx_20 = pct_return(spx_closes[si - 20], spx_closes[si])
    vals = []
    for s, sec in sector_map.items():
        if sec != sector or s not in price_map:
            continue
        dates, closes = price_map[s]
        idx = {x: j for j, x in enumerate(dates)}.get(d)
        if idx is None or idx < 20:
            continue
        r20 = pct_return(closes[idx - 20], closes[idx])
        if r20 is not None and spx_20 is not None:
            vals.append(r20 - spx_20)
    if len(vals) < 5:
        return {"sector": sector, "sector_confirmation_available": False, "sector_confirmed": False, "sector_sample_n": len(vals)}
    breadth = sum(1 for v in vals if v > 0) / len(vals) * 100.0
    med = statistics.median(vals)
    return {
        "sector": sector,
        "sector_confirmation_available": True,
        "sector_sample_n": len(vals),
        "sector_20d_excess_breadth_pct": round_or_none(breadth, 2),
        "sector_median_20d_excess_pct": round_or_none(med, 3),
        "sector_confirmed": bool(breadth >= 50.0 or med > 0),
        "is_defensive_sector": bool(sector in DEFENSIVE_SECTORS),
    }


def is_proxy(row: dict[str, Any]) -> bool:
    sym = str(row.get("symbol") or "")
    return sym in INDEX_OR_PROXY_SYMBOLS or sym.startswith("^") or sym.startswith("_")


def add_quality_fields(rows: list[dict[str, Any]], phase3h, records_map: dict[str, dict[str, list[Any]]], sector_map: dict[str, str], price_map: dict[str, tuple[list[str], list[float]]], spx_dates: list[str], spx_closes: list[float]) -> list[dict[str, Any]]:
    out = []
    for r in rows:
        rr = dict(r)
        sym = str(rr.get("symbol") or "")
        rr.update(clv_metrics(rr, records_map.get(sym)))
        rr.update(spx_context(str(rr.get("date")), spx_dates, spx_closes))
        rr.update(sector_confirmation(rr, sector_map, price_map, spx_dates, spx_closes))
        rr["proxy_or_index_symbol"] = is_proxy(rr)
        flags = rr.get("flow_flags") or {}
        rr["near_52w_high_confirmed"] = bool(flags.get("near_52w_high_confirmed"))
        rr["healthy_flow70"] = bool(num(rr.get("market_flow_score")) >= 70)
        rr["healthy_flow60"] = bool(num(rr.get("market_flow_score")) >= 60)
        rr["failed_flow_risk"] = bool((flags.get("relative_volume_confirmed") or num(rr.get("rvol_5_20")) >= 1.2) and rr.get("clv_available") and not rr.get("close_location_pass"))
        out.append(rr)
    return out


def pass_quality_rule(row: dict[str, Any], rule: str) -> bool:
    if row.get("proxy_or_index_symbol"):
        return False
    stc = num(row.get("stc_score"))
    flow = num(row.get("market_flow_score"))
    sector_ok = bool(row.get("sector_confirmed"))
    clv_ok = bool(row.get("close_location_pass")) if row.get("clv_available") else True
    near_high = bool(row.get("near_52w_high_confirmed"))
    sub = row.get("sideways_subregime")
    defensive = bool(row.get("is_defensive_sector"))
    if rule == "BASE_STC_COMMON_EQUITY":
        return True
    if rule == "UPGRADE_WATCH_RELAXED":
        return stc >= 90 and flow >= 70 and near_high and clv_ok
    if rule == "UPGRADE_WATCH_RECOVERY":
        return sub == "SIDEWAYS_RECOVERY" and stc >= 90 and flow >= 70 and near_high and clv_ok
    if rule == "UPGRADE_WATCH_SECTOR_CONFIRMED":
        return sub == "SIDEWAYS_RECOVERY" and stc >= 90 and flow >= 70 and near_high and clv_ok and sector_ok
    if rule == "DEFENSIVE_STRENGTH":
        return defensive and stc >= 85 and flow >= 60 and near_high
    if rule == "RANGE_ROTATION_PROXY":
        return sub == "SIDEWAYS_RANGE" and stc >= 80 and (flow < 70 or not sector_ok)
    if rule == "FAILED_FLOW_RISK":
        return bool(row.get("failed_flow_risk"))
    return False


def top1_by_date_stc(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_date: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by_date[str(r.get("date"))].append(r)
    out = []
    for _, group in sorted(by_date.items()):
        out.append(sorted(group, key=lambda x: (-num(x.get("stc_score")), int(x.get("leader_rank") or 9999), -num(x.get("leader_score")), -num(x.get("market_flow_score")), str(x.get("symbol") or "")))[0])
    return out


def load_upgrade_events() -> dict[str, list[tuple[str, str]]]:
    obj = maybe_load_json(E1R_CANDIDATES_PATH)
    events: dict[str, list[tuple[str, str]]] = defaultdict(list)
    if obj is None:
        return events
    rows = obj if isinstance(obj, list) else obj.get("candidates") or obj.get("data") or obj.get("rows") or []
    if not isinstance(rows, list):
        return events
    for r in rows:
        if not isinstance(r, dict):
            continue
        sym = r.get("symbol")
        d = r.get("date")
        # E1-R candidate export uses e1r_entry_type / e1r_uptrend_confirmed_eligible.
        # Keep legacy fallbacks for compatibility with older diagnostics.
        typ = str(
            r.get("e1r_entry_type")
            or r.get("entry_type")
            or r.get("candidate_type")
            or r.get("type")
            or ""
        )
        if sym and d and "CONFIRMED" in typ.upper() and "UPTREND" in typ.upper():
            events[str(sym)].append((str(d)[:10], typ))
    for sym in events:
        events[sym].sort()
    return events


def attach_upgrade_stats(rows: list[dict[str, Any]], upgrade_events: dict[str, list[tuple[str, str]]], spx_dates: list[str]) -> list[dict[str, Any]]:
    idx = {d: i for i, d in enumerate(spx_dates)}
    out = []
    for r in rows:
        rr = dict(r)
        d = str(rr.get("date"))
        sym = str(rr.get("symbol") or "")
        di = idx.get(d)
        upgraded_30 = False
        days_to_upgrade = None
        if di is not None and sym in upgrade_events:
            for ed, _typ in upgrade_events[sym]:
                ei = idx.get(ed)
                if ei is not None and 0 <= ei - di <= 30:
                    upgraded_30 = True
                    days_to_upgrade = ei - di
                    break
        rr["upgraded_to_uptrend_confirmed_30d"] = upgraded_30 if upgrade_events else None
        rr["days_to_uptrend_confirmed"] = days_to_upgrade
        out.append(rr)
    return out


def summarize_rule(rows: list[dict[str, Any]], phase3g, price_map: dict[str, tuple[list[str], list[float]]], spx_dates: list[str], spx_closes: list[float]) -> dict[str, Any]:
    daily_top1 = top1_by_date_stc(rows)
    enriched_all = phase3g.enrich_forward(rows, price_map, spx_dates, spx_closes)
    enriched_top1 = phase3g.enrich_forward(daily_top1, price_map, spx_dates, spx_closes)
    dedup_all = phase3g.dedup_by_symbol_gap(enriched_all, spx_dates, DEDUP_GAP_DAYS)
    dedup_top1 = phase3g.dedup_by_symbol_gap(enriched_top1, spx_dates, DEDUP_GAP_DAYS)
    fwd = phase3g.summarize_forward(dedup_top1)
    fail20 = None
    if dedup_top1:
        vals = [r for r in dedup_top1 if r.get("excess_20d_pct") is not None or r.get("fwd_20d_pct") is not None]
        if vals:
            fail20 = sum(1 for r in vals if num(r.get("excess_20d_pct"), 0) <= -5.0 or num(r.get("fwd_20d_pct"), 0) <= -8.0) / len(vals) * 100.0
    upgrades = [r.get("upgraded_to_uptrend_confirmed_30d") for r in dedup_top1 if r.get("upgraded_to_uptrend_confirmed_30d") is not None]
    return {
        "raw_candidates": len(rows),
        "candidate_days": len({r.get("date") for r in rows}),
        "daily_top1_count": len(daily_top1),
        "dedup_all_count": len(dedup_all),
        "dedup_top1_count": len(dedup_top1),
        "forward_all_dedup": phase3g.summarize_forward(dedup_all),
        "forward_daily_top1_dedup": fwd,
        "failure_rate_20d_pct": round_or_none(fail20, 2),
        "upgrade_to_uptrend_confirmed_30d_rate_pct": round_or_none(sum(1 for x in upgrades if x) / len(upgrades) * 100.0, 2) if upgrades else None,
        "avg_stc_score_top1": round_or_none(avg([num(r.get("stc_score")) for r in dedup_top1]), 3),
        "avg_market_flow_score_top1": round_or_none(avg([num(r.get("market_flow_score")) for r in dedup_top1]), 3),
        "subregime_counts_top1": dict(Counter(str(r.get("sideways_subregime")) for r in dedup_top1)),
        "strength_type_counts_top1": dict(Counter(str(r.get("strength_type")) for r in dedup_top1)),
        "concentration_top1_dedup": phase3g.concentration(dedup_top1),
        "sample_top1": dedup_top1[:10],
    }


def assign_strength_type(row: dict[str, Any]) -> str:
    if row.get("proxy_or_index_symbol"):
        return "EXCLUDED_PROXY_OR_INDEX"
    if row.get("failed_flow_risk"):
        return "EVENT_OR_FAILED_FLOW_RISK"
    if row.get("is_defensive_sector"):
        return "DEFENSIVE_LEADER"
    if row.get("sideways_subregime") == "SIDEWAYS_RECOVERY" and num(row.get("stc_score")) >= 90 and num(row.get("market_flow_score")) >= 70:
        return "RECOVERY_LEADER_CANDIDATE"
    if row.get("sideways_subregime") == "SIDEWAYS_RANGE":
        return "RANGE_ROTATION"
    if row.get("sideways_subregime") == "SIDEWAYS_DETERIORATION":
        return "DETERIORATION_HOLDOUT"
    return "UNCLASSIFIED_STRENGTH"


def decision(rule_results: dict[str, Any]) -> dict[str, Any]:
    candidates = []
    for rule, rr in rule_results.items():
        if rule == "BASE_STC_COMMON_EQUITY":
            continue
        f20 = rr.get("forward_daily_top1_dedup", {}).get("20d", {})
        f30 = rr.get("forward_daily_top1_dedup", {}).get("30d", {})
        n = f20.get("n") or 0
        ex20 = f20.get("avg_excess_pct")
        ex30 = f30.get("avg_excess_pct")
        wr20 = f20.get("excess_win_rate_pct") or 0
        upg = rr.get("upgrade_to_uptrend_confirmed_30d_rate_pct")
        if ex20 is not None and ex30 is not None:
            score = ex20 + ex30 + max(0, wr20 - 50) / 10 + (upg or 0) / 20
            candidates.append((score, rule, n, ex20, ex30, wr20, upg))
    candidates.sort(reverse=True)
    best = candidates[0] if candidates else None
    if best:
        _, rule, n, ex20, ex30, wr20, upg = best
        if n >= 20 and ex20 > 0 and ex30 > 0 and wr20 >= 50:
            return {"decision": "SIDEWAYS_QUALITY_SEGMENT_PROMISING_DIAGNOSTIC_ONLY", "best_rule": rule, "reason": "A SIDEWAYS quality segment met positive 20D/30D excess and sample thresholds. Still diagnostic only; execution would require separate portfolio simulation and UPTREND protection tests."}
        return {"decision": "SIDEWAYS_QUALITY_SEGMENT_WATCHLIST_ONLY", "best_rule": rule, "reason": "Some segments may improve candidate quality, but current evidence is not enough for execution-layer approval. Use for Watchlist/Tier labeling only."}
    return {"decision": "SIDEWAYS_QUALITY_DECOMPOSITION_INSUFFICIENT_SAMPLE", "best_rule": None, "reason": "No valid quality segment had enough evidence for a stronger conclusion."}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    phase3g = load_module(PHASE3G_SCRIPT, "phase3g")
    phase3h = load_module(PHASE3H_SCRIPT, "phase3h")

    bj = load_json(BACKTEST_PATH)
    variants = safe_variant_results(bj)
    if E1_ID not in variants or E1R_ID not in variants:
        print("Missing required E1/E1-R variants in exports/backtest.json.")
        print(f"Found: {list(variants.keys())}")
        print("Run `python3 run_backtest.py` first, then rerun this diagnostic.")
        raise SystemExit(2)

    spx_dates, spx_closes = phase3g.load_price_series("^GSPC")
    if not spx_dates:
        spx_dates, spx_closes = phase3g.load_price_series("GSPC")
    if not spx_dates:
        raise SystemExit("SPX price series not found under data/prices.")
    spx_rec = phase3h.load_records("^GSPC") or phase3h.load_records("GSPC")
    if not spx_rec.get("dates"):
        spx_rec = {"dates": spx_dates, "close": spx_closes, "volume": [], "high": [], "low": []}

    regime_daily = phase3g.load_regime_daily()
    price_map = phase3g.load_all_price_series()
    builder = phase3g.DailySignalBuilder(price_map)
    by_rule, stc_diag = phase3g.screen_stc_candidates(builder, spx_dates, regime_daily)

    base_rows = []
    for rule in TARGET_BASE_RULES:
        for r in by_rule.get(rule, []):
            rr = dict(r)
            rr["base_stc_rule"] = rule
            base_rows.append(rr)

    base_symbols = sorted({r.get("symbol") for r in base_rows if r.get("symbol")})
    records_map = phase3h.load_all_records(base_symbols)
    flow_rows = phase3h.attach_flow(base_rows, records_map, spx_rec)
    flow_rows = [r for r in flow_rows if r.get("has_volume_data")]

    sector_map = load_sector_map()
    quality_rows = add_quality_fields(flow_rows, phase3h, records_map, sector_map, price_map, spx_dates, spx_closes)
    for r in quality_rows:
        r["strength_type"] = assign_strength_type(r)
    quality_rows = attach_upgrade_stats(quality_rows, load_upgrade_events(), spx_dates)

    rules = [
        "BASE_STC_COMMON_EQUITY",
        "UPGRADE_WATCH_RELAXED",
        "UPGRADE_WATCH_RECOVERY",
        "UPGRADE_WATCH_SECTOR_CONFIRMED",
        "DEFENSIVE_STRENGTH",
        "RANGE_ROTATION_PROXY",
        "FAILED_FLOW_RISK",
    ]
    rule_results = {}
    for rule in rules:
        rows = [r for r in quality_rows if pass_quality_rule(r, rule)]
        rule_results[rule] = summarize_rule(rows, phase3g, price_map, spx_dates, spx_closes) if rows else {
            "raw_candidates": 0, "candidate_days": 0, "daily_top1_count": 0, "dedup_all_count": 0, "dedup_top1_count": 0,
            "forward_all_dedup": {}, "forward_daily_top1_dedup": {}, "failure_rate_20d_pct": None,
            "upgrade_to_uptrend_confirmed_30d_rate_pct": None, "sample_top1": []
        }

    by_subregime = {}
    for sub in sorted({str(r.get("sideways_subregime")) for r in quality_rows}):
        rows = [r for r in quality_rows if str(r.get("sideways_subregime")) == sub and not r.get("proxy_or_index_symbol")]
        by_subregime[sub] = summarize_rule(rows, phase3g, price_map, spx_dates, spx_closes) if rows else {}

    by_strength_type = {}
    for typ in sorted({str(r.get("strength_type")) for r in quality_rows}):
        rows = [r for r in quality_rows if str(r.get("strength_type")) == typ and not r.get("proxy_or_index_symbol")]
        by_strength_type[typ] = summarize_rule(rows, phase3g, price_map, spx_dates, spx_closes) if rows else {}

    dec = decision(rule_results)

    result = {
        "status": "DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "strategy_id": E1R_ID,
        "inputs": {
            "backtest": str(BACKTEST_PATH),
            "phase3g_script": str(PHASE3G_SCRIPT),
            "phase3h_script": str(PHASE3H_SCRIPT),
            "regime_source": str(REGIME_PATH),
            "constituents_source": str(CONSTITUENTS_PATH) if CONSTITUENTS_PATH.exists() else None,
            "e1r_candidates_source": str(E1R_CANDIDATES_PATH) if E1R_CANDIDATES_PATH.exists() else None,
        },
        "fairness_controls": {
            "does_not_change_trading_logic": True,
            "protects_existing_uptrend_confirmed_execution": True,
            "evaluates_only_sideways_downtrend_stc_candidates": True,
            "baseline_uses_phase3g_stc_top1_sorting": True,
            "market_flow_uses_phase3h_metrics": True,
            "forward_return_starts_on_signal_date": True,
        },
        "candidate_universe": {
            "base_stc_candidates": len(base_rows),
            "candidates_with_volume_data": len(flow_rows),
            "proxy_or_index_candidates": sum(1 for r in quality_rows if r.get("proxy_or_index_symbol")),
            "sector_map_symbols": len(sector_map),
            "sector_confirmation_available_rows": sum(1 for r in quality_rows if r.get("sector_confirmation_available")),
            "clv_available_rows": sum(1 for r in quality_rows if r.get("clv_available")),
            "subregime_counts": dict(Counter(str(r.get("sideways_subregime")) for r in quality_rows)),
            "strength_type_counts": dict(Counter(str(r.get("strength_type")) for r in quality_rows)),
        },
        "quality_definition_v0_1": {
            "sideways_subregimes": ["SIDEWAYS_RECOVERY", "SIDEWAYS_RANGE", "SIDEWAYS_DETERIORATION"],
            "strength_types": ["RECOVERY_LEADER_CANDIDATE", "DEFENSIVE_LEADER", "RANGE_ROTATION", "EVENT_OR_FAILED_FLOW_RISK", "DETERIORATION_HOLDOUT"],
            "new_factors": ["SPX sideways subregime", "Close Location Value", "Sector confirmation", "Proxy/index exclusion", "Upgrade-to-UPTREND-Confirmed diagnostic when available"],
        },
        "rule_results": rule_results,
        "by_subregime_results": by_subregime,
        "by_strength_type_results": by_strength_type,
        "decision": dec,
        "interpretation": {
            "primary_question": "Can SIDEWAYS STC candidates be decomposed into Upgrade Watch, Defensive Strength, and Rotation/Risk groups with better forward excess or upgrade behavior?",
            "uptrend_policy": "No UPTREND Confirmed execution logic is changed or filtered in Phase 3I.",
            "execution_policy": "Any promising SIDEWAYS segment remains Watchlist/Tier labeling until a separate portfolio simulation proves value without harming UPTREND results.",
        },
    }

    OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    write_report(result)

    print("E1-R PHASE 3I SIDEWAYS QUALITY DECOMPOSITION DIAGNOSTIC")
    print("Status: DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE")
    print(f"Base STC candidates: {len(base_rows)}")
    print(f"Candidates with volume data: {len(flow_rows)}")
    print(f"Proxy/index candidates: {result['candidate_universe']['proxy_or_index_candidates']}")
    print(f"Subregime counts: {result['candidate_universe']['subregime_counts']}")
    print(f"Strength type counts: {result['candidate_universe']['strength_type_counts']}")
    print("\nQuality rule results:")
    for rule, rr in rule_results.items():
        f20 = rr.get("forward_daily_top1_dedup", {}).get("20d", {})
        f30 = rr.get("forward_daily_top1_dedup", {}).get("30d", {})
        print(f"  {rule}: raw={rr.get('raw_candidates')} days={rr.get('candidate_days')} dedup_top1={rr.get('dedup_top1_count')} "
              f"20D avg={pct_str(f20.get('avg_return_pct'))} excess={pct_str(f20.get('avg_excess_pct'))} excessWR={pct_str(f20.get('excess_win_rate_pct'))} "
              f"30D avg={pct_str(f30.get('avg_return_pct'))} excess={pct_str(f30.get('avg_excess_pct'))} "
              f"upgrade30={pct_str(rr.get('upgrade_to_uptrend_confirmed_30d_rate_pct'))} fail20={pct_str(rr.get('failure_rate_20d_pct'))}")
    print(f"\nDecision: {dec['decision']}")
    print(f"Best rule: {dec.get('best_rule')}")
    print(f"Reason: {dec.get('reason')}")
    print(f"Output: {OUT_JSON}")
    print(f"Report: {OUT_MD}")


def write_report(result: dict[str, Any]) -> None:
    md = []
    md.append("# E1-R Phase 3I — SIDEWAYS Candidate Quality Decomposition Diagnostic")
    md.append("")
    md.append(f"Generated: `{result['generated_at']}`")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append("Diagnostic only. No trading logic, UPTREND Confirmed execution, orders, or benchmark rules are changed.")
    md.append("")
    md.append("## Candidate Universe")
    md.append("")
    cu = result["candidate_universe"]
    md.append(f"- Base STC candidates: `{cu['base_stc_candidates']}`")
    md.append(f"- Candidates with volume data: `{cu['candidates_with_volume_data']}`")
    md.append(f"- Proxy/index candidates: `{cu['proxy_or_index_candidates']}`")
    md.append(f"- Sector map symbols: `{cu['sector_map_symbols']}`")
    md.append(f"- CLV available rows: `{cu['clv_available_rows']}`")
    md.append(f"- Subregime counts: `{cu['subregime_counts']}`")
    md.append(f"- Strength type counts: `{cu['strength_type_counts']}`")
    md.append("")
    md.append("## Quality Rule Results")
    md.append("")
    md.append("| Rule | Raw | Days | Dedup Top1 | 20D Avg | 20D Excess | 20D Excess WR | 30D Avg | 30D Excess | Upgrade30 | Fail20 |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for rule, rr in result["rule_results"].items():
        f20 = rr.get("forward_daily_top1_dedup", {}).get("20d", {})
        f30 = rr.get("forward_daily_top1_dedup", {}).get("30d", {})
        md.append(f"| {rule} | {rr.get('raw_candidates')} | {rr.get('candidate_days')} | {rr.get('dedup_top1_count')} | "
                  f"{pct_str(f20.get('avg_return_pct'))} | {pct_str(f20.get('avg_excess_pct'))} | {pct_str(f20.get('excess_win_rate_pct'))} | "
                  f"{pct_str(f30.get('avg_return_pct'))} | {pct_str(f30.get('avg_excess_pct'))} | {pct_str(rr.get('upgrade_to_uptrend_confirmed_30d_rate_pct'))} | {pct_str(rr.get('failure_rate_20d_pct'))} |")
    md.append("")
    md.append("## By SIDEWAYS Subregime")
    md.append("")
    md.append("| Subregime | Dedup Top1 | 20D Excess | 30D Excess | Upgrade30 |")
    md.append("|---|---:|---:|---:|---:|")
    for sub, rr in result.get("by_subregime_results", {}).items():
        f20 = rr.get("forward_daily_top1_dedup", {}).get("20d", {}) if rr else {}
        f30 = rr.get("forward_daily_top1_dedup", {}).get("30d", {}) if rr else {}
        md.append(f"| {sub} | {rr.get('dedup_top1_count') if rr else 0} | {pct_str(f20.get('avg_excess_pct'))} | {pct_str(f30.get('avg_excess_pct'))} | {pct_str(rr.get('upgrade_to_uptrend_confirmed_30d_rate_pct') if rr else None)} |")
    md.append("")
    md.append("## By Strength Type")
    md.append("")
    md.append("| Strength Type | Dedup Top1 | 20D Excess | 30D Excess | Upgrade30 |")
    md.append("|---|---:|---:|---:|---:|")
    for typ, rr in result.get("by_strength_type_results", {}).items():
        f20 = rr.get("forward_daily_top1_dedup", {}).get("20d", {}) if rr else {}
        f30 = rr.get("forward_daily_top1_dedup", {}).get("30d", {}) if rr else {}
        md.append(f"| {typ} | {rr.get('dedup_top1_count') if rr else 0} | {pct_str(f20.get('avg_excess_pct'))} | {pct_str(f30.get('avg_excess_pct'))} | {pct_str(rr.get('upgrade_to_uptrend_confirmed_30d_rate_pct') if rr else None)} |")
    md.append("")
    md.append("## Decision")
    md.append("")
    md.append(f"- Decision: `{result['decision']['decision']}`")
    md.append(f"- Best rule: `{result['decision'].get('best_rule')}`")
    md.append(f"- Reason: {result['decision']['reason']}")
    md.append("")
    md.append("## Interpretation")
    md.append("")
    md.append("Phase 3I is designed for Watchlist/Tier improvement only. A promising segment does not authorize SIDEWAYS execution. Any future execution test must be a separate portfolio simulation and must preserve UPTREND Confirmed results.")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
