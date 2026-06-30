#!/usr/bin/env python3
"""
E1-R Candidate Forward Return Diagnostic v0.1

Purpose:
- Validate whether E1-R UPTREND candidate tags have forward-return edge.
- Diagnostic only. Does not modify backtest, strategy, orders, or exports/backtest.json.

Inputs:
- exports/e1r_candidates.json
- exports/backtest.json
- data/prices/*.json

Outputs:
- data/research/e1r/e1r_candidate_forward_return_diagnostic.json
- data/research/e1r/E1R_CANDIDATE_FORWARD_RETURN_REPORT.md
"""

from __future__ import annotations

import json
import math
from collections import defaultdict, Counter
from pathlib import Path
from statistics import mean, median

CANDIDATES_PATH = Path("exports/e1r_candidates.json")
BACKTEST_PATH = Path("exports/backtest.json")
PRICES_DIR = Path("data/prices")
OUT_DIR = Path("data/research/e1r")
OUT_JSON = OUT_DIR / "e1r_candidate_forward_return_diagnostic.json"
OUT_MD = OUT_DIR / "E1R_CANDIDATE_FORWARD_RETURN_REPORT.md"

STRATEGY_ID = "E1R_REGIME_AWARE_V0_1"
BENCHMARK_ID = "E1_AUDITED_G4_MINHOLD10"
HORIZONS = [5, 10, 20, 30]
DEDUP_GAP_DAYS = 5


def load_json(path: Path):
    with path.open() as f:
        return json.load(f)


def _series_from_json(obj):
    """Return (dates, closes) from several known/likely price JSON formats."""
    if isinstance(obj, list):
        dates, closes = [], []
        for r in obj:
            if not isinstance(r, dict):
                continue
            d = r.get("date") or r.get("Date")
            c = r.get("close") or r.get("Close") or r.get("adj_close") or r.get("Adj Close")
            if d is not None and c is not None:
                dates.append(str(d))
                closes.append(float(c))
        return dates, closes

    if not isinstance(obj, dict):
        return [], []

    # Common direct format: {dates: [...], close: [...]}
    date_keys = ["dates", "date", "Date"]
    close_keys = ["close", "closes", "prices", "adj_close", "Adj Close", "Close"]
    for dk in date_keys:
        for ck in close_keys:
            if dk in obj and ck in obj and isinstance(obj[dk], list) and isinstance(obj[ck], list):
                return [str(x) for x in obj[dk]], [float(x) for x in obj[ck]]

    # Nested wrappers: {data: ...}, {series: ...}, {history: ...}
    for key in ["data", "series", "history", "prices"]:
        if key in obj:
            d, c = _series_from_json(obj[key])
            if d and c:
                return d, c

    # Mapping by date: {"2024-01-01": {close: ...}}
    if obj and all(isinstance(k, str) for k in obj.keys()):
        rows = []
        for d, v in obj.items():
            if isinstance(v, dict):
                c = v.get("close") or v.get("Close") or v.get("adj_close") or v.get("Adj Close")
            else:
                c = v if isinstance(v, (int, float)) else None
            if c is not None and len(d) >= 10 and d[4:5] == "-":
                rows.append((d, float(c)))
        if rows:
            rows.sort()
            return [r[0] for r in rows], [r[1] for r in rows]

    return [], []


def price_file_candidates(symbol: str):
    safe = symbol.replace("/", "-")
    return [
        PRICES_DIR / f"{symbol}.json",
        PRICES_DIR / f"{safe}.json",
        PRICES_DIR / f"{symbol.replace('^','')}.json",
        PRICES_DIR / f"{symbol.replace('^','_')}.json",
    ]


def load_price_series(symbol: str):
    for path in price_file_candidates(symbol):
        if path.exists():
            try:
                dates, closes = _series_from_json(load_json(path))
                if dates and closes and len(dates) == len(closes):
                    return dates, closes
            except Exception:
                continue
    return [], []


def pct(a: float, b: float):
    return (b / a - 1.0) * 100.0 if a and a > 0 and b and b > 0 else None


def forward_return_for(series_dates, series_closes, signal_date: str, horizon: int):
    idx = {d: i for i, d in enumerate(series_dates)}
    i = idx.get(signal_date)
    if i is None:
        # Use nearest future trading date if signal date is absent for the stock.
        future = [j for j, d in enumerate(series_dates) if d >= signal_date]
        if not future:
            return None
        i = future[0]
    j = i + horizon
    if j >= len(series_closes):
        return None
    return pct(series_closes[i], series_closes[j])


def summarize(rows):
    vals = [r for r in rows if r is not None and math.isfinite(r)]
    if not vals:
        return {"n": 0}
    wins = [v for v in vals if v > 0]
    return {
        "n": len(vals),
        "avg_return_pct": round(mean(vals), 3),
        "median_return_pct": round(median(vals), 3),
        "win_rate_pct": round(len(wins) / len(vals) * 100, 1),
        "best_pct": round(max(vals), 3),
        "worst_pct": round(min(vals), 3),
    }


def summarize_excess(items, h):
    vals = []
    wins = 0
    for r in items:
        stock = r.get(f"fwd_{h}d_pct")
        spx = r.get(f"spx_fwd_{h}d_pct")
        if stock is None or spx is None:
            continue
        ex = stock - spx
        vals.append(ex)
        if ex > 0:
            wins += 1
    if not vals:
        return {"n": 0}
    return {
        "n": len(vals),
        "avg_excess_pct": round(mean(vals), 3),
        "median_excess_pct": round(median(vals), 3),
        "excess_win_rate_pct": round(wins / len(vals) * 100, 1),
    }


def trading_day_gap(date_a: str, date_b: str, master_dates: list[str]):
    idx = {d: i for i, d in enumerate(master_dates)}
    if date_a not in idx or date_b not in idx:
        return None
    return idx[date_b] - idx[date_a]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    candidates_obj = load_json(CANDIDATES_PATH)
    candidates = candidates_obj.get("candidates", candidates_obj if isinstance(candidates_obj, list) else [])
    backtest = load_json(BACKTEST_PATH)
    variants = backtest["backtest"]["results"]["layer_d"]["variant_results"]
    e1 = variants.get(BENCHMARK_ID, {})
    e1_trades = e1.get("trades", [])

    spx_dates, spx_closes = load_price_series("^GSPC")
    if not spx_dates:
        spx_dates, spx_closes = load_price_series("GSPC")
    if not spx_dates:
        raise SystemExit("SPX price series not found under data/prices. Expected ^GSPC.json or GSPC.json compatible file.")

    # First E1 entry date by symbol, used for lead-time diagnostic.
    first_e1_entry = {}
    for t in e1_trades:
        sym = t.get("symbol")
        ed = t.get("entry_date")
        if sym and ed and (sym not in first_e1_entry or ed < first_e1_entry[sym]):
            first_e1_entry[sym] = ed

    price_cache = {"^GSPC": (spx_dates, spx_closes)}
    enriched = []
    missing_price_symbols = Counter()

    for c in candidates:
        sym = c.get("symbol")
        date = c.get("date")
        if not sym or not date:
            continue
        if sym not in price_cache:
            price_cache[sym] = load_price_series(sym)
        dates, closes = price_cache[sym]
        if not dates:
            missing_price_symbols[sym] += 1
            continue

        r = dict(c)
        for h in HORIZONS:
            r[f"fwd_{h}d_pct"] = forward_return_for(dates, closes, date, h)
            r[f"spx_fwd_{h}d_pct"] = forward_return_for(spx_dates, spx_closes, date, h)
            if r[f"fwd_{h}d_pct"] is not None and r[f"spx_fwd_{h}d_pct"] is not None:
                r[f"excess_{h}d_pct"] = round(r[f"fwd_{h}d_pct"] - r[f"spx_fwd_{h}d_pct"], 4)
            else:
                r[f"excess_{h}d_pct"] = None

        e1_entry = first_e1_entry.get(sym)
        r["first_e1_entry_date"] = e1_entry
        r["lead_days_vs_first_e1_entry"] = trading_day_gap(date, e1_entry, spx_dates) if e1_entry else None
        enriched.append(r)

    # 5-trading-day de-dup by symbol + entry type to reduce repeated daily signals.
    enriched.sort(key=lambda x: (x.get("symbol", ""), x.get("e1r_entry_type", ""), x.get("date", "")))
    last_kept = {}
    dedup = []
    spx_idx = {d: i for i, d in enumerate(spx_dates)}
    for r in enriched:
        key = (r.get("symbol"), r.get("e1r_entry_type"))
        d = r.get("date")
        i = spx_idx.get(d)
        if i is None:
            continue
        prev = last_kept.get(key)
        if prev is None or i - prev >= DEDUP_GAP_DAYS:
            dedup.append(r)
            last_kept[key] = i

    def grouped_summary(items):
        out = {}
        groups = defaultdict(list)
        for r in items:
            groups[r.get("e1r_entry_type", "UNKNOWN")].append(r)
        groups["ALL"] = list(items)
        for name, rs in groups.items():
            hsum = {}
            for h in HORIZONS:
                hsum[f"{h}d"] = {
                    **summarize([r.get(f"fwd_{h}d_pct") for r in rs]),
                    **summarize_excess(rs, h),
                }
            lead_vals = [r.get("lead_days_vs_first_e1_entry") for r in rs if r.get("lead_days_vs_first_e1_entry") is not None]
            out[name] = {
                "candidate_count": len(rs),
                "forward_returns": hsum,
                "lead_time_vs_first_e1_entry": {
                    "n": len(lead_vals),
                    "avg_trading_days": round(mean(lead_vals), 2) if lead_vals else None,
                    "median_trading_days": round(median(lead_vals), 2) if lead_vals else None,
                    "pct_before_or_same_e1_entry": round(sum(1 for x in lead_vals if x >= 0) / len(lead_vals) * 100, 1) if lead_vals else None,
                },
            }
        return out

    by_date = Counter(r.get("date") for r in enriched)
    result = {
        "strategy_id": STRATEGY_ID,
        "benchmark_strategy_id": BENCHMARK_ID,
        "status": "DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE",
        "input": {
            "candidates": str(CANDIDATES_PATH),
            "backtest": str(BACKTEST_PATH),
            "prices_dir": str(PRICES_DIR),
        },
        "raw_candidate_count": len(candidates),
        "enriched_candidate_count": len(enriched),
        "dedup_gap_trading_days": DEDUP_GAP_DAYS,
        "dedup_candidate_count": len(dedup),
        "missing_price_symbol_count": len(missing_price_symbols),
        "missing_price_top_symbols": missing_price_symbols.most_common(20),
        "raw_summary": grouped_summary(enriched),
        "dedup_summary": grouped_summary(dedup),
        "candidate_count_by_date": dict(sorted(by_date.items())),
        "sample_enriched_candidates": enriched[:20],
    }

    OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False))

    lines = []
    lines.append("# E1-R Candidate Forward Return Diagnostic")
    lines.append("")
    lines.append(f"Status: `{result['status']}`")
    lines.append(f"Raw candidates: {result['raw_candidate_count']}")
    lines.append(f"Enriched candidates: {result['enriched_candidate_count']}")
    lines.append(f"Dedup candidates ({DEDUP_GAP_DAYS} trading-day gap): {result['dedup_candidate_count']}")
    lines.append("")
    lines.append("## Dedup Forward Return Summary")
    lines.append("")
    lines.append("| Entry Type | Count | 5D Avg | 5D Excess | 10D Avg | 10D Excess | 20D Avg | 20D Excess | 30D Avg | 30D Excess |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for name, s in result["dedup_summary"].items():
        fr = s["forward_returns"]
        def cell(h, k):
            v = fr[f"{h}d"].get(k)
            return "n/a" if v is None else f"{v:.3f}%"
        lines.append(
            f"| {name} | {s['candidate_count']} | "
            f"{cell(5, 'avg_return_pct')} | {cell(5, 'avg_excess_pct')} | "
            f"{cell(10, 'avg_return_pct')} | {cell(10, 'avg_excess_pct')} | "
            f"{cell(20, 'avg_return_pct')} | {cell(20, 'avg_excess_pct')} | "
            f"{cell(30, 'avg_return_pct')} | {cell(30, 'avg_excess_pct')} |"
        )
    lines.append("")
    lines.append("## Lead Time vs First E1 Entry")
    lines.append("")
    lines.append("Positive lead days means the E1-R candidate appeared before or on the first E1 trade entry date for the same symbol.")
    lines.append("")
    lines.append("| Entry Type | N | Avg Trading Days | Median Trading Days | % Before/Same E1 Entry |")
    lines.append("|---|---:|---:|---:|---:|")
    for name, s in result["dedup_summary"].items():
        lt = s["lead_time_vs_first_e1_entry"]
        lines.append(
            f"| {name} | {lt['n']} | {lt['avg_trading_days']} | {lt['median_trading_days']} | {lt['pct_before_or_same_e1_entry']}% |"
        )
    lines.append("")
    lines.append("Interpretation: this report validates candidate alpha only. It does not authorize E1-R execution logic.")
    OUT_MD.write_text("\n".join(lines))

    print("=" * 72)
    print("E1-R CANDIDATE FORWARD RETURN DIAGNOSTIC")
    print("=" * 72)
    print(f"Status: {result['status']}")
    print(f"Raw candidates: {result['raw_candidate_count']}")
    print(f"Enriched candidates: {result['enriched_candidate_count']}")
    print(f"Dedup candidates: {result['dedup_candidate_count']}")
    print("")
    for name, s in result["dedup_summary"].items():
        fr = s["forward_returns"]
        print(f"{name}: count={s['candidate_count']}")
        for h in HORIZONS:
            x = fr[f"{h}d"]
            print(
                f"  {h:2d}D avg={x.get('avg_return_pct')}% "
                f"excess={x.get('avg_excess_pct')}% "
                f"WR={x.get('win_rate_pct')}% "
                f"excessWR={x.get('excess_win_rate_pct')}% n={x.get('n')}"
            )
    print("")
    print(f"Output JSON: {OUT_JSON}")
    print(f"Output MD:   {OUT_MD}")


if __name__ == "__main__":
    main()
