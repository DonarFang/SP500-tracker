#!/usr/bin/env python3
"""
E1-R Phase 3F SIDEWAYS Rule Diagnostic

Diagnostic only. Does not modify trading logic, orders, exports/backtest.json,
or any strategy implementation.

Purpose:
- Evaluate whether E1-R should keep SIDEWAYS as cash/near-zero exposure,
  or whether there is enough evidence to test a future low-exposure,
  high-quality SIDEWAYS rule.
- Keep E1 vs E1-R comparisons on the same regime framework.

Expected inputs after `python3 run_backtest.py`:
- exports/backtest.json, containing E1_AUDITED_G4_MINHOLD10 and E1R_REGIME_AWARE_V0_1
- data/prices/*.json
- data/research/e1r/e1r_regime_attribution_review.json
- data/research/e1_5y/regimes/spx_regime_daily.json

Outputs:
- data/research/e1r/e1r_phase3f_sideways_rule_diagnostic.json
- data/research/e1r/E1R_PHASE3F_SIDEWAYS_RULE_DIAGNOSTIC_REPORT.md
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean, median
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.features.rs import period_return, rs_percentile  # noqa: E402
from src.features.momentum import momentum_score as calc_momentum, moving_average, linreg_slope  # noqa: E402
from src.features.trend_health import trend_health_score as calc_trend_health  # noqa: E402
from src.engine.leader_ranking import leader_score as calc_leader_score  # noqa: E402

E1_ID = "E1_AUDITED_G4_MINHOLD10"
E1R_ID = "E1R_REGIME_AWARE_V0_1"

BACKTEST_PATH = Path("exports/backtest.json")
PRICES_DIR = Path("data/prices")
REGIME_PATH = Path("data/research/e1_5y/regimes/spx_regime_daily.json")
REGIME_REVIEW_PATH = Path("data/research/e1r/e1r_regime_attribution_review.json")

OUT_DIR = Path("data/research/e1r")
OUT_JSON = OUT_DIR / "e1r_phase3f_sideways_rule_diagnostic.json"
OUT_MD = OUT_DIR / "E1R_PHASE3F_SIDEWAYS_RULE_DIAGNOSTIC_REPORT.md"

HORIZONS = [5, 10, 20, 30]
DEDUP_GAP_DAYS = 5

INDEX_SYMBOLS = {"^GSPC", "GSPC", "SPX", "^NDX", "NDX", "^VIX", "VIX", "^SOX", "SOX", "SPY", "QQQ"}


def load_json(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing required input: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


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


def round_or_none(x: Any, nd: int = 3) -> Any:
    try:
        if x is None:
            return None
        y = float(x)
        return round(y, nd) if math.isfinite(y) else None
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


def safe_variant_results(backtest: dict[str, Any]) -> dict[str, Any]:
    try:
        return backtest["backtest"]["results"]["layer_d"]["variant_results"]
    except KeyError as exc:
        raise KeyError("Cannot locate backtest.results.layer_d.variant_results in exports/backtest.json") from exc


def series_from_json(obj: Any) -> tuple[list[str], list[float]]:
    if isinstance(obj, list):
        dates, closes = [], []
        for r in obj:
            if not isinstance(r, dict):
                continue
            d = r.get("date") or r.get("Date")
            c = r.get("close") or r.get("Close") or r.get("adj_close") or r.get("Adj Close")
            if d is not None and c is not None:
                dates.append(str(d)[:10])
                closes.append(float(c))
        return dates, closes

    if not isinstance(obj, dict):
        return [], []

    for dk in ["dates", "date", "Date"]:
        for ck in ["close", "closes", "prices", "adj_close", "Adj Close", "Close"]:
            if dk in obj and ck in obj and isinstance(obj[dk], list) and isinstance(obj[ck], list):
                return [str(x)[:10] for x in obj[dk]], [float(x) for x in obj[ck]]

    for key in ["data", "series", "history", "prices"]:
        if key in obj:
            d, c = series_from_json(obj[key])
            if d and c:
                return d, c

    rows = []
    for d, v in obj.items():
        if isinstance(v, dict):
            c = v.get("close") or v.get("Close") or v.get("adj_close") or v.get("Adj Close")
        elif isinstance(v, (int, float)):
            c = v
        else:
            c = None
        if c is not None and isinstance(d, str) and len(d) >= 10 and d[4] == "-":
            rows.append((d[:10], float(c)))
    if rows:
        rows.sort()
        return [r[0] for r in rows], [r[1] for r in rows]
    return [], []


def price_file_candidates(symbol: str) -> list[Path]:
    safe = symbol.replace("/", "-")
    return [
        PRICES_DIR / f"{symbol}.json",
        PRICES_DIR / f"{safe}.json",
        PRICES_DIR / f"{symbol.replace('^','')}.json",
        PRICES_DIR / f"{symbol.replace('^','_')}.json",
    ]


def load_price_series(symbol: str) -> tuple[list[str], list[float]]:
    for path in price_file_candidates(symbol):
        if not path.exists():
            continue
        try:
            dates, closes = series_from_json(load_json(path))
            if dates and closes and len(dates) == len(closes):
                return dates, closes
        except Exception:
            continue
    return [], []


def load_all_price_series() -> dict[str, tuple[list[str], list[float]]]:
    out: dict[str, tuple[list[str], list[float]]] = {}
    for path in sorted(PRICES_DIR.glob("*.json")):
        sym = path.stem
        if sym.startswith("._") or sym in INDEX_SYMBOLS:
            continue
        try:
            dates, closes = series_from_json(load_json(path))
        except Exception:
            continue
        if len(dates) >= 90 and len(dates) == len(closes):
            out[sym] = (dates, closes)
    return out


def pct_return(a: float, b: float) -> float | None:
    if a and b and a > 0 and b > 0:
        return (b / a - 1.0) * 100.0
    return None


def forward_return_for(series_dates: list[str], series_closes: list[float], signal_date: str, horizon: int) -> float | None:
    idx = {d: i for i, d in enumerate(series_dates)}
    i = idx.get(signal_date)
    if i is None:
        future = [j for j, d in enumerate(series_dates) if d >= signal_date]
        if not future:
            return None
        i = future[0]
    j = i + horizon
    if j >= len(series_closes):
        return None
    return pct_return(series_closes[i], series_closes[j])


def summarize(vals: list[Any]) -> dict[str, Any]:
    xs = [float(v) for v in vals if isinstance(v, (int, float)) and math.isfinite(float(v))]
    if not xs:
        return {"n": 0}
    wins = [x for x in xs if x > 0]
    return {
        "n": len(xs),
        "avg_return_pct": round(mean(xs), 3),
        "median_return_pct": round(median(xs), 3),
        "win_rate_pct": round(len(wins) / len(xs) * 100, 1),
        "best_pct": round(max(xs), 3),
        "worst_pct": round(min(xs), 3),
    }


def summarize_forward(rows: list[dict[str, Any]]) -> dict[str, Any]:
    out = {}
    for h in HORIZONS:
        ret_vals = [r.get(f"fwd_{h}d_pct") for r in rows]
        ex_vals = [r.get(f"excess_{h}d_pct") for r in rows]
        ex_clean = [float(v) for v in ex_vals if isinstance(v, (int, float)) and math.isfinite(float(v))]
        ex_wins = [v for v in ex_clean if v > 0]
        out[f"{h}d"] = {
            **summarize(ret_vals),
            "avg_excess_pct": round(mean(ex_clean), 3) if ex_clean else None,
            "median_excess_pct": round(median(ex_clean), 3) if ex_clean else None,
            "excess_win_rate_pct": round(len(ex_wins) / len(ex_clean) * 100, 1) if ex_clean else None,
        }
    return out


def dedup_by_symbol_gap(rows: list[dict[str, Any]], master_dates: list[str], gap: int = DEDUP_GAP_DAYS) -> list[dict[str, Any]]:
    idx = {d: i for i, d in enumerate(master_dates)}
    rows = sorted(rows, key=lambda r: (str(r.get("symbol") or ""), str(r.get("date") or "")))
    last_by_symbol: dict[str, int] = {}
    kept = []
    for r in rows:
        sym = r.get("symbol")
        d = r.get("date")
        i = idx.get(d)
        if not sym or i is None:
            continue
        prev = last_by_symbol.get(sym)
        if prev is None or i - prev >= gap:
            kept.append(r)
            last_by_symbol[sym] = i
    return sorted(kept, key=lambda r: str(r.get("date") or ""))


def enrich_forward(rows: list[dict[str, Any]], price_map: dict[str, tuple[list[str], list[float]]], spx_dates: list[str], spx_closes: list[float]) -> list[dict[str, Any]]:
    enriched = []
    for r0 in rows:
        sym = r0.get("symbol")
        d = r0.get("date")
        if not sym or not d or sym not in price_map:
            continue
        dates, closes = price_map[sym]
        r = dict(r0)
        for h in HORIZONS:
            stock = forward_return_for(dates, closes, d, h)
            spx = forward_return_for(spx_dates, spx_closes, d, h)
            r[f"fwd_{h}d_pct"] = round_or_none(stock, 4)
            r[f"spx_fwd_{h}d_pct"] = round_or_none(spx, 4)
            r[f"excess_{h}d_pct"] = round_or_none(stock - spx, 4) if stock is not None and spx is not None else None
        enriched.append(r)
    return enriched


def avg_abs_return(values: list[float]) -> float | None:
    if len(values) < 2:
        return None
    rets = []
    for i in range(1, len(values)):
        if values[i - 1] > 0:
            rets.append(abs(values[i] / values[i - 1] - 1.0))
    return mean(rets) if rets else None


def max_drawdown_from_recent_high(values: list[float]) -> float | None:
    if not values:
        return None
    hi = max(values)
    last = values[-1]
    if hi <= 0:
        return None
    return (last / hi - 1.0) * 100.0


def candidate_sort_key(c: dict[str, Any]) -> tuple:
    return (
        int(c.get("leader_rank") or 9999),
        -num(c.get("leader_score")),
        -num(c.get("rs_score")),
        -num(c.get("momentum_score")),
        -num(c.get("trend_health")),
        str(c.get("symbol") or ""),
    )


def concentration(rows: list[dict[str, Any]]) -> dict[str, Any]:
    cnt = Counter(r.get("symbol") for r in rows if r.get("symbol"))
    total = sum(cnt.values())
    top10 = cnt.most_common(10)
    return {
        "unique_symbols": len(cnt),
        "total_rows": total,
        "top10_symbol_counts": top10,
        "top10_share_pct": round(sum(v for _, v in top10) / total * 100, 1) if total else 0.0,
    }


def classify_sideways_candidate(sig: dict[str, Any]) -> dict[str, bool]:
    # Spec proxy from E1R_REGIME_AWARE_STRATEGY_SPEC_v0.1:
    # RS>=92, rank<=5, LS>=80, TH>=75, Mom>=75, Close>MA50, MA50 slope>=0,
    # 20d pullback<=8%, Close distance from MA50<=+12%, no volatility expansion.
    base = (
        sig["rs_score"] >= 92
        and sig["leader_rank"] <= 5
        and sig["leader_score"] >= 80
        and sig["trend_health"] >= 75
        and sig["momentum_score"] >= 75
        and sig["close"] > sig["ma50"]
        and sig["ma50_slope"] >= 0
        and sig["pullback_20d_pct"] >= -8.0
        and sig["distance_ma50_pct"] <= 12.0
    )
    no_vol_expansion = sig.get("vol_ratio_10_vs_prev20") is not None and sig["vol_ratio_10_vs_prev20"] <= 1.25
    strict = base and no_vol_expansion
    relaxed_no_vol = base
    ultra_strict = strict and sig["rs_score"] >= 95 and sig["leader_score"] >= 85 and sig["leader_rank"] <= 3
    return {
        "SIDEWAYS_STRICT_SPEC_PROXY": strict,
        "SIDEWAYS_RELAXED_NO_VOL_FILTER": relaxed_no_vol,
        "SIDEWAYS_ULTRA_STRICT_TOP3": ultra_strict,
    }


def build_sideways_candidates(price_map: dict[str, tuple[list[str], list[float]]], spx_dates: list[str], regime_daily: dict[str, Any]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    sideways_dates = [d for d in spx_dates if str((regime_daily.get(d) or {}).get("regime") or regime_daily.get(d)) == "SIDEWAYS"]
    candidates_by_rule: dict[str, list[dict[str, Any]]] = defaultdict(list)
    diagnostics = {
        "sideways_days": len(sideways_dates),
        "symbols_loaded": len(price_map),
        "evaluated_symbol_days": 0,
        "warmup_skipped_symbol_days": 0,
        "candidate_days_by_rule": {},
    }

    date_index_by_symbol = {s: {d: i for i, d in enumerate(dc[0])} for s, dc in price_map.items()}

    for d in sideways_dates:
        ret60_by_symbol = {}
        rows = []
        for sym, (dates, closes) in price_map.items():
            idx = date_index_by_symbol[sym].get(d)
            if idx is None or idx < 80:
                diagnostics["warmup_skipped_symbol_days"] += 1
                continue
            p = closes[: idx + 1]
            r60 = period_return(p, 60)
            if r60 is not None:
                ret60_by_symbol[sym] = r60
        all_ret60 = list(ret60_by_symbol.values())
        if not all_ret60:
            continue

        for sym, r60 in ret60_by_symbol.items():
            dates, closes = price_map[sym]
            idx = date_index_by_symbol[sym][d]
            p = closes[: idx + 1]
            if len(p) < 80:
                continue
            diagnostics["evaluated_symbol_days"] += 1
            rs = rs_percentile(r60, all_ret60)
            mom_d = calc_momentum(p)
            mom = mom_d.get("momentum_score", 0)
            th_d = calc_trend_health(p)
            th = th_d.get("trend_health", 0)
            ls = calc_leader_score(rs, mom, th)
            ma50s = moving_average(p, 50)
            ma50 = ma50s[-1] if ma50s else p[-1]
            ma50_sl = linreg_slope(ma50s[-10:]) if len(ma50s) >= 10 else 0.0
            pullback_20d = max_drawdown_from_recent_high(p[-20:])
            distance_ma50 = (p[-1] / ma50 - 1.0) * 100.0 if ma50 else None
            vol_recent = avg_abs_return(p[-10:])
            vol_prev = avg_abs_return(p[-30:-10]) if len(p) >= 30 else None
            vol_ratio = vol_recent / vol_prev if vol_recent is not None and vol_prev and vol_prev > 0 else None
            rows.append({
                "date": d,
                "symbol": sym,
                "spx_regime": "SIDEWAYS",
                "rs_score": round(rs, 3),
                "momentum_score": round(mom, 3),
                "trend_health": round(th, 3),
                "leader_score": round(ls, 3),
                "close": round(p[-1], 4),
                "ma50": round(ma50, 4),
                "ma50_slope": round(ma50_sl, 6),
                "pullback_20d_pct": round_or_none(pullback_20d, 3),
                "distance_ma50_pct": round_or_none(distance_ma50, 3),
                "vol_ratio_10_vs_prev20": round_or_none(vol_ratio, 3),
            })

        rows.sort(key=lambda x: x["leader_score"], reverse=True)
        for i, row in enumerate(rows, start=1):
            row["leader_rank"] = i
            flags = classify_sideways_candidate(row)
            for rule, ok in flags.items():
                if ok:
                    c = dict(row)
                    c["sideways_rule"] = rule
                    candidates_by_rule[rule].append(c)

    for rule, rows in candidates_by_rule.items():
        diagnostics["candidate_days_by_rule"][rule] = len({r["date"] for r in rows})
    return candidates_by_rule, diagnostics


def load_regime_daily() -> dict[str, Any]:
    obj = load_json(REGIME_PATH)
    daily = obj.get("daily_regime", obj) if isinstance(obj, dict) else {}
    return daily if isinstance(daily, dict) else {}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    bj = load_json(BACKTEST_PATH)
    variants = safe_variant_results(bj)
    if E1_ID not in variants or E1R_ID not in variants:
        print("Missing required E1/E1-R variants in exports/backtest.json.")
        print(f"Found: {list(variants.keys())}")
        print("Run `python3 run_backtest.py` first, then rerun this diagnostic.")
        raise SystemExit(2)

    e1 = variants[E1_ID]
    e1r = variants[E1R_ID]
    regime_review = load_json(REGIME_REVIEW_PATH) if REGIME_REVIEW_PATH.exists() else {}
    regime_comparison = regime_review.get("comparison", {}) if isinstance(regime_review, dict) else {}
    regime_strategies = regime_review.get("strategies", {}) if isinstance(regime_review, dict) else {}

    spx_dates, spx_closes = load_price_series("^GSPC")
    if not spx_dates:
        spx_dates, spx_closes = load_price_series("GSPC")
    if not spx_dates:
        raise SystemExit("SPX price series not found under data/prices.")

    regime_daily = load_regime_daily()
    price_map = load_all_price_series()
    candidates_by_rule, build_diag = build_sideways_candidates(price_map, spx_dates, regime_daily)

    rule_results = {}
    for rule, rows in sorted(candidates_by_rule.items()):
        top1_by_date = []
        for d, group in defaultdict(list, { }).items():
            pass
        by_date: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for r in rows:
            by_date[r["date"]].append(r)
        for d, cs in sorted(by_date.items()):
            top1_by_date.append(sorted(cs, key=candidate_sort_key)[0])
        enriched_all = enrich_forward(rows, price_map, spx_dates, spx_closes)
        enriched_top1 = enrich_forward(top1_by_date, price_map, spx_dates, spx_closes)
        dedup_all = dedup_by_symbol_gap(enriched_all, spx_dates, DEDUP_GAP_DAYS)
        dedup_top1 = dedup_by_symbol_gap(enriched_top1, spx_dates, DEDUP_GAP_DAYS)
        rule_results[rule] = {
            "raw_candidates": len(rows),
            "candidate_days": len(by_date),
            "daily_top1_count": len(top1_by_date),
            "dedup_all_count": len(dedup_all),
            "dedup_top1_count": len(dedup_top1),
            "forward_all_dedup": summarize_forward(dedup_all),
            "forward_daily_top1_dedup": summarize_forward(dedup_top1),
            "concentration_all_dedup": concentration(dedup_all),
            "concentration_top1_dedup": concentration(dedup_top1),
            "sample_top1": top1_by_date[:10],
        }

    sideways_cmp = regime_comparison.get("SIDEWAYS", {})
    sideways_e1 = (regime_strategies.get(E1_ID, {}) or {}).get("by_regime", {}).get("SIDEWAYS", {})
    sideways_e1r = (regime_strategies.get(E1R_ID, {}) or {}).get("by_regime", {}).get("SIDEWAYS", {})

    decision = "KEEP_SIDEWAYS_CASH_FOR_NOW"
    reason = "No strict SIDEWAYS candidate evidence met positive-capacity standard yet."
    strict = rule_results.get("SIDEWAYS_STRICT_SPEC_PROXY", {})
    strict20 = (strict.get("forward_daily_top1_dedup", {}) or {}).get("20d", {})
    strict_count = strict.get("dedup_top1_count", 0) or 0
    strict_excess20 = strict20.get("avg_excess_pct")
    strict_exwr20 = strict20.get("excess_win_rate_pct")
    if strict_count >= 20 and strict_excess20 is not None and strict_excess20 > 0.5 and (strict_exwr20 or 0) >= 50:
        decision = "SIDEWAYS_LOW_EXPOSURE_RESEARCH_CANDIDATE"
        reason = "Strict SIDEWAYS proxy has enough sample and positive 20D excess evidence for a future paper-test design."
    elif strict_count > 0:
        decision = "SIDEWAYS_WATCHLIST_ONLY_FOR_NOW"
        reason = "Strict SIDEWAYS proxy produced candidates, but evidence is not strong enough for execution-layer approval."

    result = {
        "status": "DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "strategy_id": E1R_ID,
        "inputs": {
            "backtest": str(BACKTEST_PATH),
            "prices_dir": str(PRICES_DIR),
            "regime_source": str(REGIME_PATH),
            "regime_review": str(REGIME_REVIEW_PATH),
        },
        "fairness_controls": {
            "same_regime_map_as_e1r_review": True,
            "same_backtest_export_window": True,
            "does_not_change_trading_logic": True,
            "period_slices_not_primary_evaluation": True,
            "sideways_rule_is_candidate_diagnostic_only": True,
        },
        "portfolio_context": {
            "E1": {
                "total_return_pct": e1.get("total_return_pct"),
                "max_drawdown_pct": e1.get("max_drawdown_pct"),
                "profit_factor": e1.get("profit_factor"),
                "number_of_trades": e1.get("number_of_trades"),
            },
            "E1R": {
                "total_return_pct": e1r.get("total_return_pct"),
                "max_drawdown_pct": e1r.get("max_drawdown_pct"),
                "profit_factor": e1r.get("profit_factor"),
                "number_of_trades": e1r.get("number_of_trades"),
            },
            "sideways_regime_review_delta": sideways_cmp,
            "sideways_e1_regime_block": sideways_e1,
            "sideways_e1r_regime_block": sideways_e1r,
        },
        "sideways_candidate_build_diagnostics": build_diag,
        "sideways_rule_results": rule_results,
        "decision": {
            "phase3f_decision": decision,
            "reason": reason,
            "execution_layer_change_approved": False,
            "next_step": "Only consider a future paper-test design if strict SIDEWAYS proxy has sufficient positive excess evidence.",
        },
    }

    OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    md = []
    md.append("# E1-R Phase 3F SIDEWAYS Rule Diagnostic")
    md.append("")
    md.append(f"Status: **{result['status']}**")
    md.append("")
    md.append("## 1. Purpose")
    md.append("")
    md.append("Evaluate whether SIDEWAYS should remain cash/near-zero exposure, or whether a future low-exposure high-quality SIDEWAYS rule deserves paper testing. This diagnostic does not change trading logic.")
    md.append("")
    md.append("## 2. Portfolio Context")
    md.append("")
    md.append("| Strategy | Return | MaxDD | PF | Trades |")
    md.append("|---|---:|---:|---:|---:|")
    md.append(f"| E1 | {pct_str(e1.get('total_return_pct'))} | {pct_str(e1.get('max_drawdown_pct'))} | {e1.get('profit_factor')} | {e1.get('number_of_trades')} |")
    md.append(f"| E1-R | {pct_str(e1r.get('total_return_pct'))} | {pct_str(e1r.get('max_drawdown_pct'))} | {e1r.get('profit_factor')} | {e1r.get('number_of_trades')} |")
    md.append("")
    md.append("## 3. SIDEWAYS Regime Review Delta")
    md.append("")
    md.append("| Days | E1R-E1 PnL | Compound | Exposure Delta | MaxDD Delta |")
    md.append("|---:|---:|---:|---:|---:|")
    md.append(f"| {sideways_cmp.get('days')} | {pct_str(sideways_cmp.get('e1r_minus_e1_pnl_pct_initial'))} | {pct_str(sideways_cmp.get('e1r_minus_e1_compound_pct'))} | {pct_str(sideways_cmp.get('e1r_minus_e1_avg_exposure_pct'))} | {pct_str(sideways_cmp.get('e1r_minus_e1_max_dd_within_regime_pct'))} |")
    md.append("")
    md.append("## 4. SIDEWAYS Candidate Rules")
    md.append("")
    md.append("Strict proxy follows the v0.1 spec: RS>=92, rank<=5, LS>=80, TH>=75, Momentum>=75, close>MA50, MA50 slope>=0, 20D pullback within 8%, MA50 distance <=12%, and no volatility expansion proxy.")
    md.append("")
    md.append("| Rule | Raw | Days | Dedup Top1 | 20D Avg | 20D Excess | 20D Excess WR | 30D Avg | 30D Excess |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for rule, block in rule_results.items():
        f20 = block.get("forward_daily_top1_dedup", {}).get("20d", {})
        f30 = block.get("forward_daily_top1_dedup", {}).get("30d", {})
        md.append(
            f"| {rule} | {block.get('raw_candidates')} | {block.get('candidate_days')} | {block.get('dedup_top1_count')} | "
            f"{pct_str(f20.get('avg_return_pct'))} | {pct_str(f20.get('avg_excess_pct'))} | {f20.get('excess_win_rate_pct')}% | "
            f"{pct_str(f30.get('avg_return_pct'))} | {pct_str(f30.get('avg_excess_pct'))} |"
        )
    md.append("")
    md.append("## 5. Decision")
    md.append("")
    md.append(f"Decision: **{decision}**")
    md.append("")
    md.append(f"Reason: {reason}")
    md.append("")
    md.append("Execution layer change approved: **False**")
    md.append("")
    md.append("## 6. Next Step")
    md.append("")
    md.append("Keep SIDEWAYS as diagnostic-only unless a future paper-test design shows sufficient positive excess return under strict low-exposure rules.")
    md.append("")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("E1-R PHASE 3F SIDEWAYS RULE DIAGNOSTIC")
    print("Status: DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE")
    print(f"SIDEWAYS days: {build_diag.get('sideways_days')} symbols_loaded={build_diag.get('symbols_loaded')}")
    print(f"Portfolio E1:   return={e1.get('total_return_pct')} maxDD={e1.get('max_drawdown_pct')} PF={e1.get('profit_factor')} trades={e1.get('number_of_trades')}")
    print(f"Portfolio E1-R: return={e1r.get('total_return_pct')} maxDD={e1r.get('max_drawdown_pct')} PF={e1r.get('profit_factor')} trades={e1r.get('number_of_trades')}")
    print("\nSIDEWAYS regime delta:")
    print(
        f"  days={sideways_cmp.get('days')} "
        f"E1R-E1 pnl={pct_str(sideways_cmp.get('e1r_minus_e1_pnl_pct_initial'))} "
        f"compound={pct_str(sideways_cmp.get('e1r_minus_e1_compound_pct'))} "
        f"exposure_delta={pct_str(sideways_cmp.get('e1r_minus_e1_avg_exposure_pct'))} "
        f"maxDD_delta={pct_str(sideways_cmp.get('e1r_minus_e1_max_dd_within_regime_pct'))}"
    )
    print("\nSIDEWAYS candidate rule results:")
    if not rule_results:
        print("  No SIDEWAYS candidates found under tested rule proxies.")
    for rule, block in rule_results.items():
        f20 = block.get("forward_daily_top1_dedup", {}).get("20d", {})
        f30 = block.get("forward_daily_top1_dedup", {}).get("30d", {})
        print(
            f"  {rule}: raw={block.get('raw_candidates')} days={block.get('candidate_days')} dedup_top1={block.get('dedup_top1_count')} "
            f"20D avg={pct_str(f20.get('avg_return_pct'))} excess={pct_str(f20.get('avg_excess_pct'))} excessWR={f20.get('excess_win_rate_pct')}% "
            f"30D avg={pct_str(f30.get('avg_return_pct'))} excess={pct_str(f30.get('avg_excess_pct'))}"
        )
    print("\nDecision:", decision)
    print("Reason:", reason)
    print(f"Output: {OUT_JSON}")
    print(f"Report: {OUT_MD}")


if __name__ == "__main__":
    main()
