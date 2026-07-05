#!/usr/bin/env python3
"""
E1R_SIDEWAYS_FULL_SCAN_V0_1

Purpose:
- Sideways-only research scan for E1-R 5Y dataset.
- Does NOT modify E1-R UPTREND logic.
- Does NOT modify official backtest outputs.
- Reads raw 5Y research data and regime labels.
- Produces a standalone JSON report.

Scope:
- Layer 1: SIDEWAYS subclass / episode distribution.
- Layer 2: candidate forward-return diagnostics by subclass.

Dataset:
- data/research/e1_5y/raw/stocks/*.json
- data/research/e1_5y/raw/indices/SPX.json
- data/research/e1_5y/regimes/spx_regime_daily.json

Important:
This is an opportunity-pool diagnostic, not yet a formal portfolio backtest.
"""

import json
import math
from pathlib import Path
from collections import Counter, defaultdict
from statistics import mean, median

START_DATE = "2021-06-11"
END_DATE = "2026-06-16"

ROOT = Path(".")
RAW_STOCK_DIR = ROOT / "data/research/e1_5y/raw/stocks"
RAW_INDEX_DIR = ROOT / "data/research/e1_5y/raw/indices"
REGIME_PATH = ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json"

OUT_DIR = ROOT / "data/research/e1_5y/sideways_full_scan"
OUT_PATH = OUT_DIR / "e1r_sideways_full_scan_v0_1.json"

FWD_WINDOWS = [5, 10, 20, 30]

# Candidate pool sizes for opportunity scan.
# This is not the official E1 entry rule.
TOP_N_BY_SCORE = 20

# Minimum data requirements.
MIN_HISTORY_DAYS = 200
MIN_PRICE = 5.0


def safe_float(x):
    try:
        if x is None:
            return None
        v = float(x)
        if math.isnan(v) or math.isinf(v):
            return None
        return v
    except Exception:
        return None


def pct(a, b):
    a = safe_float(a)
    b = safe_float(b)
    if a is None or b is None or b == 0:
        return None
    return (a / b - 1.0) * 100.0


def avg(xs):
    xs = [x for x in xs if x is not None]
    return mean(xs) if xs else None


def med(xs):
    xs = [x for x in xs if x is not None]
    return median(xs) if xs else None


def percentile(values, x):
    values = [v for v in values if v is not None]
    if not values or x is None:
        return None
    le = sum(1 for v in values if v <= x)
    return 100.0 * le / len(values)


def max_drawdown_from_high(series):
    """
    Return current drawdown from rolling high within the provided series.
    Input: list of closes.
    Output: negative pct, e.g. -12.5
    """
    vals = [safe_float(x) for x in series]
    vals = [x for x in vals if x is not None]
    if not vals:
        return None
    high = max(vals)
    last = vals[-1]
    if high <= 0:
        return None
    return (last / high - 1.0) * 100.0


def load_bars_json(path):
    j = json.loads(path.read_text())
    bars = j.get("bars", [])
    rows = []
    for b in bars:
        d = b.get("date")
        c = safe_float(b.get("close"))
        h = safe_float(b.get("high"))
        l = safe_float(b.get("low"))
        o = safe_float(b.get("open"))
        v = safe_float(b.get("volume"))
        if d and c is not None:
            rows.append({
                "date": d,
                "open": o,
                "high": h,
                "low": l,
                "close": c,
                "volume": v,
            })
    rows.sort(key=lambda x: x["date"])
    return {
        "symbol": j.get("symbol") or path.stem,
        "data_start": j.get("data_start"),
        "data_end": j.get("data_end"),
        "bars": rows,
        "by_date": {r["date"]: r for r in rows},
        "dates": [r["date"] for r in rows],
        "closes": [r["close"] for r in rows],
    }


def moving_average(vals, n):
    if len(vals) < n:
        return None
    window = vals[-n:]
    if any(v is None for v in window):
        return None
    return sum(window) / n


def slope_pct(vals, n):
    if len(vals) < n + 1:
        return None
    first = vals[-n - 1]
    last = vals[-1]
    if first is None or last is None or first == 0:
        return None
    return (last / first - 1.0) * 100.0


def get_fwd_return(asset, date, n):
    dates = asset["dates"]
    by_date = asset["by_date"]
    if date not in by_date:
        return None
    try:
        i = dates.index(date)
    except ValueError:
        return None
    j = i + n
    if j >= len(dates):
        return None
    c0 = asset["bars"][i]["close"]
    c1 = asset["bars"][j]["close"]
    return pct(c1, c0)


def get_hist_closes(asset, date, n):
    dates = asset["dates"]
    if date not in asset["by_date"]:
        return None
    try:
        i = dates.index(date)
    except ValueError:
        return None
    if i + 1 < n:
        return None
    return [asset["bars"][k]["close"] for k in range(i - n + 1, i + 1)]


def build_sideways_episodes(sideways_dates):
    """
    Group consecutive trading-day SIDEWAYS dates into episodes.
    Since we only have trading dates, adjacency is based on order in shared regime dates.
    """
    episodes = []
    if not sideways_dates:
        return episodes

    cur = [sideways_dates[0]]
    for prev, d in zip(sideways_dates, sideways_dates[1:]):
        # If subclass changes, split episode.
        if d["subclass"] != prev["subclass"]:
            episodes.append(cur)
            cur = [d]
        else:
            cur.append(d)
    episodes.append(cur)

    out = []
    for ep in episodes:
        out.append({
            "start": ep[0]["date"],
            "end": ep[-1]["date"],
            "days": len(ep),
            "subclass": ep[0]["subclass"],
        })
    return out


def summarize_returns(records, prefix):
    """
    Summarize forward return records.
    records contain:
    - fwd{n}
    - spx_fwd{n}
    - excess{n}
    """
    out = {}
    for n in FWD_WINDOWS:
        r_key = f"{prefix}_fwd{n}_pct"
        s_key = f"spx_fwd{n}_pct"
        e_key = f"excess_fwd{n}_pct"

        rs = [r.get(r_key) for r in records if r.get(r_key) is not None]
        ss = [r.get(s_key) for r in records if r.get(s_key) is not None]
        es = [r.get(e_key) for r in records if r.get(e_key) is not None]

        wins_vs_spx = [
            1 for r in records
            if r.get(r_key) is not None
            and r.get(s_key) is not None
            and r.get(r_key) > r.get(s_key)
        ]
        comparable = [
            1 for r in records
            if r.get(r_key) is not None
            and r.get(s_key) is not None
        ]

        out[f"fwd{n}"] = {
            "sample_count": len(rs),
            "avg_return_pct": avg(rs),
            "median_return_pct": med(rs),
            "avg_spx_pct": avg(ss),
            "median_spx_pct": med(ss),
            "avg_excess_pct": avg(es),
            "median_excess_pct": med(es),
            "win_rate_vs_spx_pct": 100.0 * len(wins_vs_spx) / len(comparable) if comparable else None,
        }
    return out


def main():
    if not RAW_STOCK_DIR.exists():
        raise FileNotFoundError(f"Missing stock raw dir: {RAW_STOCK_DIR}")
    if not REGIME_PATH.exists():
        raise FileNotFoundError(f"Missing regime file: {REGIME_PATH}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading regimes...")
    regime_json = json.loads(REGIME_PATH.read_text())
    daily_regime = regime_json.get("daily_regime", {})

    sideways_dates = []
    regime_counts = Counter()
    subclass_counts = Counter()

    for d, v in sorted(daily_regime.items()):
        if not isinstance(v, dict):
            continue
        if not (START_DATE <= d <= END_DATE):
            continue

        reg = v.get("regime") or "NO_REGIME"
        sub = v.get("subclass") or "NO_SUBCLASS"

        regime_counts[reg] += 1

        if reg == "SIDEWAYS":
            subclass_counts[sub] += 1
            sideways_dates.append({
                "date": d,
                "regime": reg,
                "subclass": sub,
            })

    print("Loading SPX...")
    spx = load_bars_json(RAW_INDEX_DIR / "SPX.json")

    print("Loading stocks...")
    stock_assets = {}
    for path in sorted(RAW_STOCK_DIR.glob("*.json")):
        asset = load_bars_json(path)
        sym = asset["symbol"]
        if len(asset["bars"]) >= MIN_HISTORY_DAYS:
            stock_assets[sym] = asset

    print(f"Stocks loaded: {len(stock_assets)}")
    print(f"SIDEWAYS days: {len(sideways_dates)}")
    print(f"SIDEWAYS subclass counts: {dict(subclass_counts)}")

    # Precompute date index for faster lookup.
    for asset in stock_assets.values():
        asset["_date_to_idx"] = {d: i for i, d in enumerate(asset["dates"])}
    spx["_date_to_idx"] = {d: i for i, d in enumerate(spx["dates"])}

    daily_candidate_records = []
    all_candidate_records = []

    for item in sideways_dates:
        d = item["date"]
        subclass = item["subclass"]

        spx_hist_20 = get_hist_closes(spx, d, 20)
        spx_hist_60 = get_hist_closes(spx, d, 60)
        if not spx_hist_20 or not spx_hist_60:
            continue

        spx_mom20 = slope_pct(spx_hist_20, min(19, len(spx_hist_20) - 1))
        spx_mom60 = slope_pct(spx_hist_60, min(59, len(spx_hist_60) - 1))

        candidates_raw = []

        for sym, asset in stock_assets.items():
            if d not in asset["by_date"]:
                continue

            hist_20 = get_hist_closes(asset, d, 20)
            hist_50 = get_hist_closes(asset, d, 50)
            hist_150 = get_hist_closes(asset, d, 150)
            hist_200 = get_hist_closes(asset, d, 200)
            hist_60 = get_hist_closes(asset, d, 60)

            if not hist_20 or not hist_50 or not hist_150 or not hist_200 or not hist_60:
                continue

            close = asset["by_date"][d]["close"]
            if close is None or close < MIN_PRICE:
                continue

            ma20 = moving_average(hist_20, 20)
            ma50 = moving_average(hist_50, 50)
            ma150 = moving_average(hist_150, 150)
            ma200 = moving_average(hist_200, 200)

            mom20 = slope_pct(hist_20, 19)
            mom60 = slope_pct(hist_60, 59)
            dd60 = max_drawdown_from_high(hist_60)

            rs20 = None if spx_mom20 is None or mom20 is None else mom20 - spx_mom20
            rs60 = None if spx_mom60 is None or mom60 is None else mom60 - spx_mom60

            trend_points = 0
            trend_points += 1 if ma20 is not None and close > ma20 else 0
            trend_points += 1 if ma50 is not None and close > ma50 else 0
            trend_points += 1 if ma150 is not None and close > ma150 else 0
            trend_points += 1 if ma200 is not None and close > ma200 else 0
            trend_points += 1 if ma50 is not None and ma150 is not None and ma50 > ma150 else 0
            trend_points += 1 if ma150 is not None and ma200 is not None and ma150 > ma200 else 0

            # Simple opportunity score.
            # Transparent and intentionally separate from official E1 rules.
            score = 0.0
            if rs20 is not None:
                score += 2.0 * rs20
            if rs60 is not None:
                score += 1.0 * rs60
            if mom20 is not None:
                score += 0.5 * mom20
            if mom60 is not None:
                score += 0.25 * mom60
            score += 3.0 * trend_points
            if dd60 is not None:
                score += 0.2 * dd60  # dd60 is negative, penalizes deep drawdown.

            rec = {
                "date": d,
                "subclass": subclass,
                "symbol": sym,
                "close": close,
                "score": score,
                "mom20_pct": mom20,
                "mom60_pct": mom60,
                "rs20_vs_spx_pct": rs20,
                "rs60_vs_spx_pct": rs60,
                "trend_points_0_to_6": trend_points,
                "drawdown_60d_pct": dd60,
            }

            for n in FWD_WINDOWS:
                r = get_fwd_return(asset, d, n)
                s = get_fwd_return(spx, d, n)
                rec[f"candidate_fwd{n}_pct"] = r
                rec[f"spx_fwd{n}_pct"] = s
                rec[f"excess_fwd{n}_pct"] = None if r is None or s is None else r - s

            candidates_raw.append(rec)

        if not candidates_raw:
            continue

        candidates_raw.sort(key=lambda x: x["score"], reverse=True)
        top_candidates = candidates_raw[:TOP_N_BY_SCORE]

        daily_candidate_records.append({
            "date": d,
            "subclass": subclass,
            "available_symbols": len(candidates_raw),
            "selected_candidates": len(top_candidates),
            "top_symbols": [r["symbol"] for r in top_candidates[:10]],
            "top_score": top_candidates[0]["score"] if top_candidates else None,
            "median_score_top_n": med([r["score"] for r in top_candidates]),
        })

        all_candidate_records.extend(top_candidates)

    # Aggregations.
    by_subclass = {}
    for sub in sorted(subclass_counts.keys()):
        recs = [r for r in all_candidate_records if r["subclass"] == sub]
        unique_symbols = sorted(set(r["symbol"] for r in recs))
        sym_counts = Counter(r["symbol"] for r in recs)

        by_subclass[sub] = {
            "sideways_days": subclass_counts[sub],
            "candidate_count": len(recs),
            "deduped_candidate_count": len(set((r["date"], r["symbol"]) for r in recs)),
            "unique_symbols": len(unique_symbols),
            "return_summary": summarize_returns(recs, "candidate"),
            "top_20_symbols_by_candidate_frequency": sym_counts.most_common(20),
            "top_symbol_concentration_pct": (
                100.0 * sym_counts.most_common(1)[0][1] / len(recs)
                if recs and sym_counts else None
            ),
            "top_5_symbol_concentration_pct": (
                100.0 * sum(v for _, v in sym_counts.most_common(5)) / len(recs)
                if recs and sym_counts else None
            ),
        }

    overall_sym_counts = Counter(r["symbol"] for r in all_candidate_records)

    episodes = build_sideways_episodes(sideways_dates)
    episode_by_subclass = defaultdict(list)
    for ep in episodes:
        episode_by_subclass[ep["subclass"]].append(ep["days"])

    layer1 = {
        "regime_counts": dict(regime_counts),
        "sideways_total_days": len(sideways_dates),
        "sideways_subclass_counts": dict(subclass_counts),
        "sideways_subclass_pct": {
            k: 100.0 * v / len(sideways_dates) if sideways_dates else None
            for k, v in subclass_counts.items()
        },
        "sideways_episode_count": len(episodes),
        "sideways_episode_summary_by_subclass": {
            k: {
                "episodes": len(v),
                "avg_days": avg(v),
                "median_days": med(v),
                "max_days": max(v) if v else None,
            }
            for k, v in episode_by_subclass.items()
        },
        "first_20_sideways_dates": sideways_dates[:20],
        "last_20_sideways_dates": sideways_dates[-20:],
    }

    layer2 = {
        "method": {
            "description": "Top-N opportunity-pool scan during SIDEWAYS dates. This is not the official E1 entry rule.",
            "top_n_by_score_per_sideways_day": TOP_N_BY_SCORE,
            "score_inputs": [
                "rs20_vs_spx",
                "rs60_vs_spx",
                "mom20",
                "mom60",
                "trend_points_0_to_6",
                "drawdown_60d",
            ],
            "forward_windows_trading_days": FWD_WINDOWS,
        },
        "overall": {
            "sideways_days_with_candidates": len(daily_candidate_records),
            "candidate_count": len(all_candidate_records),
            "deduped_candidate_count": len(set((r["date"], r["symbol"]) for r in all_candidate_records)),
            "unique_symbols": len(set(r["symbol"] for r in all_candidate_records)),
            "return_summary": summarize_returns(all_candidate_records, "candidate"),
            "top_20_symbols_by_candidate_frequency": overall_sym_counts.most_common(20),
            "top_symbol_concentration_pct": (
                100.0 * overall_sym_counts.most_common(1)[0][1] / len(all_candidate_records)
                if all_candidate_records and overall_sym_counts else None
            ),
            "top_5_symbol_concentration_pct": (
                100.0 * sum(v for _, v in overall_sym_counts.most_common(5)) / len(all_candidate_records)
                if all_candidate_records and overall_sym_counts else None
            ),
        },
        "by_subclass": by_subclass,
    }

    report = {
        "scan_name": "E1R_SIDEWAYS_FULL_SCAN_V0_1",
        "sample_window": {
            "start": START_DATE,
            "end": END_DATE,
        },
        "input_paths": {
            "stocks": str(RAW_STOCK_DIR),
            "indices": str(RAW_INDEX_DIR),
            "regimes": str(REGIME_PATH),
        },
        "output_path": str(OUT_PATH),
        "status": "RESEARCH_ONLY_NOT_OFFICIAL_STRATEGY",
        "frozen_constraints": {
            "do_not_modify_uptrend_e1r_logic": True,
            "do_not_modify_dowtrend_cash_logic": True,
            "sideways_scan_is_sidecar_research_only": True,
        },
        "layer1_sideways_distribution": layer1,
        "layer2_candidate_forward_return_diagnostics": layer2,
        "daily_candidate_sample": {
            "first_5": daily_candidate_records[:5],
            "last_5": daily_candidate_records[-5:],
        },
        "candidate_sample": {
            "first_10": all_candidate_records[:10],
            "last_10": all_candidate_records[-10:],
        },
    }

    OUT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False))

    print("\nDONE")
    print(f"Wrote: {OUT_PATH}")

    print("\nLAYER 1 SUMMARY")
    print(json.dumps(layer1, indent=2, ensure_ascii=False))

    print("\nLAYER 2 OVERALL SUMMARY")
    print(json.dumps(layer2["overall"], indent=2, ensure_ascii=False))

    print("\nLAYER 2 BY SUBCLASS SUMMARY")
    for sub, val in by_subclass.items():
        print(f"\n{sub}")
        print(json.dumps({
            "sideways_days": val["sideways_days"],
            "candidate_count": val["candidate_count"],
            "unique_symbols": val["unique_symbols"],
            "return_summary": val["return_summary"],
            "top_5_symbol_concentration_pct": val["top_5_symbol_concentration_pct"],
            "top_20_symbols_by_candidate_frequency": val["top_20_symbols_by_candidate_frequency"],
        }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
