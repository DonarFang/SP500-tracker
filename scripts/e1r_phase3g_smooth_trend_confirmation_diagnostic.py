#!/usr/bin/env python3
"""
E1-R Phase 3G Smooth Trend Confirmation Diagnostic

Diagnostic only. Does not modify trading logic, orders, exports/backtest.json,
or any strategy implementation.

Purpose:
A. STC Screen: smooth first, then find strong stocks in SIDEWAYS / DOWNTREND.
   This is the only branch that can later be considered for execution-layer research.
B. Watchlist Funnel: find single-day strong stocks first, then validate whether
   they later pass Smooth Trend Confirmation. This branch is Watchlist / radar only.

Expected inputs after `python3 run_backtest.py`:
- exports/backtest.json, containing E1_AUDITED_G4_MINHOLD10 and E1R_REGIME_AWARE_V0_1
- data/prices/*.json
- data/research/e1r/e1r_regime_attribution_review.json
- data/research/e1r/e1r_phase3f_sideways_rule_diagnostic.json
- data/research/e1_5y/regimes/spx_regime_daily.json

Outputs:
- data/research/e1r/e1r_phase3g_smooth_trend_confirmation_diagnostic.json
- data/research/e1r/E1R_PHASE3G_SMOOTH_TREND_CONFIRMATION_REPORT.md
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
PHASE3F_PATH = Path("data/research/e1r/e1r_phase3f_sideways_rule_diagnostic.json")

OUT_DIR = Path("data/research/e1r")
OUT_JSON = OUT_DIR / "e1r_phase3g_smooth_trend_confirmation_diagnostic.json"
OUT_MD = OUT_DIR / "E1R_PHASE3G_SMOOTH_TREND_CONFIRMATION_REPORT.md"

HORIZONS = [5, 10, 20, 30]
DEDUP_GAP_DAYS = 5
TARGET_REGIMES = ["SIDEWAYS", "DOWNTREND"]
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


def avg(vals: list[Any]) -> float | None:
    xs = [float(v) for v in vals if isinstance(v, (int, float)) and math.isfinite(float(v))]
    return mean(xs) if xs else None


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


def max_drawdown_from_recent_high(values: list[float]) -> float | None:
    if not values:
        return None
    hi = max(values)
    last = values[-1]
    if hi <= 0:
        return None
    return (last / hi - 1.0) * 100.0


def regime_of(d: str, regime_daily: dict[str, Any]) -> str:
    x = regime_daily.get(d)
    if isinstance(x, dict):
        return str(x.get("regime") or x.get("label") or "UNCLASSIFIED")
    if x:
        return str(x)
    return "UNCLASSIFIED"


def load_regime_daily() -> dict[str, Any]:
    obj = load_json(REGIME_PATH)
    daily = obj.get("daily_regime", obj) if isinstance(obj, dict) else {}
    return daily if isinstance(daily, dict) else {}


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


class DailySignalBuilder:
    def __init__(self, price_map: dict[str, tuple[list[str], list[float]]]):
        self.price_map = price_map
        self.date_index_by_symbol = {s: {d: i for i, d in enumerate(dc[0])} for s, dc in price_map.items()}
        self.cache: dict[str, dict[str, dict[str, Any]]] = {}

    def build_for_date(self, d: str) -> dict[str, dict[str, Any]]:
        if d in self.cache:
            return self.cache[d]

        ret60_by_symbol = {}
        for sym, (dates, closes) in self.price_map.items():
            idx = self.date_index_by_symbol[sym].get(d)
            if idx is None or idx < 80:
                continue
            p = closes[: idx + 1]
            r60 = period_return(p, 60)
            if r60 is not None:
                ret60_by_symbol[sym] = r60

        all_ret60 = list(ret60_by_symbol.values())
        rows = []
        if all_ret60:
            for sym, r60 in ret60_by_symbol.items():
                dates, closes = self.price_map[sym]
                idx = self.date_index_by_symbol[sym][d]
                p = closes[: idx + 1]
                rs = rs_percentile(r60, all_ret60)
                mom_d = calc_momentum(p)
                mom = mom_d.get("momentum_score", 0)
                th_d = calc_trend_health(p)
                th = th_d.get("trend_health", 0)
                ls = calc_leader_score(rs, mom, th)
                ma20s = moving_average(p, 20)
                ma50s = moving_average(p, 50)
                ma20 = ma20s[-1] if ma20s else p[-1]
                ma50 = ma50s[-1] if ma50s else p[-1]
                ma20_sl = linreg_slope(ma20s[-10:]) if len(ma20s) >= 10 else 0.0
                ma50_sl = linreg_slope(ma50s[-10:]) if len(ma50s) >= 10 else 0.0
                pullback_20d = max_drawdown_from_recent_high(p[-20:])
                rows.append({
                    "date": d,
                    "symbol": sym,
                    "rs_score": round(rs, 3),
                    "momentum_score": round(mom, 3),
                    "trend_health": round(th, 3),
                    "leader_score": round(ls, 3),
                    "close": round(p[-1], 4),
                    "ma20": round(ma20, 4),
                    "ma50": round(ma50, 4),
                    "ma20_slope": round(ma20_sl, 6),
                    "ma50_slope": round(ma50_sl, 6),
                    "pullback_20d_pct": round_or_none(pullback_20d, 3),
                    "close_gt_ma20": p[-1] > ma20 if ma20 else False,
                    "close_gt_ma50": p[-1] > ma50 if ma50 else False,
                    "ma20_gt_ma50": ma20 > ma50 if ma20 and ma50 else False,
                })

        rows.sort(key=lambda x: x["leader_score"], reverse=True)
        out = {}
        for i, row in enumerate(rows, start=1):
            row["leader_rank"] = i
            out[row["symbol"]] = row
        self.cache[d] = out
        return out

    def signal_history(self, sym: str, d: str, master_dates: list[str], n: int) -> list[dict[str, Any]]:
        idx = {x: i for i, x in enumerate(master_dates)}
        i = idx.get(d)
        if i is None:
            return []
        hist = []
        for dd in master_dates[max(0, i - n + 1): i + 1]:
            row = self.build_for_date(dd).get(sym)
            if row:
                hist.append(row)
        return hist


def stc_score(sym: str, d: str, builder: DailySignalBuilder, master_dates: list[str]) -> dict[str, Any] | None:
    today = builder.build_for_date(d).get(sym)
    if not today:
        return None
    h20 = builder.signal_history(sym, d, master_dates, 20)
    h10 = h20[-10:]
    h5 = h20[-5:]
    if len(h10) < 8 or len(h20) < 15:
        return None

    rs5 = avg([x["rs_score"] for x in h5])
    rs10 = avg([x["rs_score"] for x in h10])
    rs20 = avg([x["rs_score"] for x in h20])
    rank5 = avg([x["leader_rank"] for x in h5])
    rank10 = avg([x["leader_rank"] for x in h10])
    mom5 = avg([x["momentum_score"] for x in h5])
    mom10 = avg([x["momentum_score"] for x in h10])
    rank_le20_days10 = sum(1 for x in h10 if x["leader_rank"] <= 20)
    mom_ge70_days10 = sum(1 for x in h10 if x["momentum_score"] >= 70)
    close_gt_ma20_days5 = sum(1 for x in h5 if x.get("close_gt_ma20"))
    close_gt_ma50_days5 = sum(1 for x in h5 if x.get("close_gt_ma50"))

    score = 0.0

    # RS Smooth, 30 pts.
    score += min(15.0, max(0.0, (num(rs10) - 70.0) / 20.0 * 15.0))
    score += min(10.0, max(0.0, (num(rs20) - 65.0) / 20.0 * 10.0))
    if rs10 is not None and rs20 is not None and rs10 > rs20:
        score += 5.0

    # Rank persistence, 20 pts. Lower rank is better.
    score += min(10.0, max(0.0, (30.0 - num(rank5, 999.0)) / 20.0 * 10.0))
    score += min(7.0, max(0.0, (40.0 - num(rank10, 999.0)) / 25.0 * 7.0))
    score += min(3.0, rank_le20_days10 / 6.0 * 3.0)

    # Momentum smooth, 25 pts.
    score += min(10.0, max(0.0, (num(mom5) - 50.0) / 20.0 * 10.0))
    score += min(8.0, max(0.0, (num(mom10) - 45.0) / 20.0 * 8.0))
    if mom5 is not None and mom10 is not None and mom5 > mom10:
        score += 4.0
    score += min(3.0, mom_ge70_days10 / 6.0 * 3.0)

    # Price structure, 25 pts.
    if today.get("close_gt_ma20"):
        score += 5.0
    if today.get("close_gt_ma50"):
        score += 5.0
    if today.get("ma20_slope", 0) > 0:
        score += 5.0
    if today.get("ma20_gt_ma50") or today.get("ma50_slope", 0) >= 0:
        score += 5.0
    score += min(5.0, close_gt_ma20_days5 / 5.0 * 3.0 + close_gt_ma50_days5 / 5.0 * 2.0)

    out = dict(today)
    out.update({
        "stc_score": round(score, 3),
        "rs_5d_avg": round_or_none(rs5, 3),
        "rs_10d_avg": round_or_none(rs10, 3),
        "rs_20d_avg": round_or_none(rs20, 3),
        "rank_5d_avg": round_or_none(rank5, 3),
        "rank_10d_avg": round_or_none(rank10, 3),
        "momentum_5d_avg": round_or_none(mom5, 3),
        "momentum_10d_avg": round_or_none(mom10, 3),
        "rank_le20_days10": rank_le20_days10,
        "momentum_ge70_days10": mom_ge70_days10,
        "close_gt_ma20_days5": close_gt_ma20_days5,
        "close_gt_ma50_days5": close_gt_ma50_days5,
    })
    return out


def stc_rule_pass(row: dict[str, Any], regime: str, threshold: int) -> bool:
    if not row:
        return False
    if row.get("stc_score", 0) < threshold:
        return False
    # Minimal quality guards: score alone is not enough for execution research.
    if regime == "SIDEWAYS":
        return (
            num(row.get("rs_10d_avg")) >= 85
            and num(row.get("rs_20d_avg")) >= 80
            and num(row.get("rank_10d_avg"), 999) <= 30
            and row.get("close_gt_ma20")
            and row.get("close_gt_ma50")
        )
    if regime == "DOWNTREND":
        return (
            num(row.get("rs_10d_avg")) >= 92
            and num(row.get("rs_20d_avg")) >= 90
            and num(row.get("rank_10d_avg"), 999) <= 15
            and row.get("close_gt_ma50")
            and num(row.get("ma50_slope")) >= 0
        )
    return False


def screen_stc_candidates(builder: DailySignalBuilder, master_dates: list[str], regime_daily: dict[str, Any]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    rules = {
        "SIDEWAYS_STC80": ("SIDEWAYS", 80),
        "SIDEWAYS_STC85": ("SIDEWAYS", 85),
        "SIDEWAYS_STC90": ("SIDEWAYS", 90),
        "DOWNTREND_STC90": ("DOWNTREND", 90),
    }
    candidates: dict[str, list[dict[str, Any]]] = defaultdict(list)
    diag = {
        "regime_day_counts": Counter(),
        "evaluated_symbol_days": 0,
        "stc_computed_symbol_days": 0,
    }

    for d in master_dates:
        reg = regime_of(d, regime_daily)
        if reg not in TARGET_REGIMES:
            continue
        diag["regime_day_counts"][reg] += 1
        daily = builder.build_for_date(d)
        for sym in daily.keys():
            diag["evaluated_symbol_days"] += 1
            row = stc_score(sym, d, builder, master_dates)
            if not row:
                continue
            diag["stc_computed_symbol_days"] += 1
            row["spx_regime"] = reg
            for rule, (rule_regime, threshold) in rules.items():
                if reg == rule_regime and stc_rule_pass(row, reg, threshold):
                    r = dict(row)
                    r["stc_rule"] = rule
                    r["stc_threshold"] = threshold
                    candidates[rule].append(r)

    diag["regime_day_counts"] = dict(diag["regime_day_counts"])
    return candidates, diag


def top1_by_date(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_date: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by_date[r["date"]].append(r)
    out = []
    for d, group in sorted(by_date.items()):
        out.append(sorted(
            group,
            key=lambda x: (-num(x.get("stc_score")), int(x.get("leader_rank") or 9999), -num(x.get("leader_score")), str(x.get("symbol") or "")),
        )[0])
    return out


def build_raw_watchlist_candidates(builder: DailySignalBuilder, master_dates: list[str], regime_daily: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for d in master_dates:
        reg = regime_of(d, regime_daily)
        if reg not in TARGET_REGIMES:
            continue
        for sym, row in builder.build_for_date(d).items():
            # Single-day strong candidate: intentionally looser than STC because this is watchlist/radar only.
            if (
                row["rs_score"] >= 90
                and row["leader_rank"] <= 20
                and row["leader_score"] >= 75
                and row["momentum_score"] >= 70
                and row["trend_health"] >= 65
                and row.get("close_gt_ma20")
            ):
                r = dict(row)
                r["origin_regime"] = reg
                r["watchlist_signal_type"] = f"{reg}_RAW_SINGLE_DAY_STRONG"
                rows.append(r)
    return rows


def find_first_stc_confirmation(raw: dict[str, Any], builder: DailySignalBuilder, master_dates: list[str], regime_daily: dict[str, Any], max_wait: int = 30) -> dict[str, Any] | None:
    idx = {d: i for i, d in enumerate(master_dates)}
    i0 = idx.get(raw["date"])
    if i0 is None:
        return None
    origin_regime = raw.get("origin_regime")
    threshold = 80 if origin_regime == "SIDEWAYS" else 90
    for j in range(i0, min(len(master_dates), i0 + max_wait + 1)):
        d = master_dates[j]
        reg = regime_of(d, regime_daily)
        row = stc_score(raw["symbol"], d, builder, master_dates)
        if row and stc_rule_pass(row, origin_regime, threshold):
            out = dict(row)
            out["origin_date"] = raw["date"]
            out["origin_regime"] = origin_regime
            out["confirmation_date"] = d
            out["date"] = d  # forward return starts at confirmation date, not original discovery date.
            out["confirmation_regime"] = reg
            out["wait_days"] = j - i0
            out["watchlist_confirmation_rule"] = f"{origin_regime}_WATCHLIST_TO_STC{threshold}"
            return out
    return None


def build_watchlist_funnel(builder: DailySignalBuilder, master_dates: list[str], regime_daily: dict[str, Any], price_map: dict[str, tuple[list[str], list[float]]], spx_dates: list[str], spx_closes: list[float]) -> dict[str, Any]:
    raw = build_raw_watchlist_candidates(builder, master_dates, regime_daily)
    dedup_raw = dedup_by_symbol_gap(raw, master_dates, DEDUP_GAP_DAYS)

    confirmations = []
    for r in dedup_raw:
        c = find_first_stc_confirmation(r, builder, master_dates, regime_daily, max_wait=30)
        if c:
            confirmations.append(c)
    enriched_conf = enrich_forward(confirmations, price_map, spx_dates, spx_closes)
    dedup_conf = dedup_by_symbol_gap(enriched_conf, master_dates, DEDUP_GAP_DAYS)

    wait_days = [c["wait_days"] for c in confirmations if isinstance(c.get("wait_days"), int)]
    by_origin = Counter(r.get("origin_regime") for r in dedup_raw)
    by_confirm = Counter(c.get("origin_regime") for c in confirmations)
    by_confirm_regime = Counter(c.get("confirmation_regime") for c in confirmations)

    horizon_rates = {}
    idx = {d: i for i, d in enumerate(master_dates)}
    for h in [5, 10, 20, 30]:
        n = 0
        hit = 0
        for r in dedup_raw:
            i0 = idx.get(r["date"])
            if i0 is None:
                continue
            n += 1
            c = find_first_stc_confirmation(r, builder, master_dates, regime_daily, max_wait=h)
            if c:
                hit += 1
        horizon_rates[f"{h}d_confirmation_rate_pct"] = round(hit / n * 100, 1) if n else None

    return {
        "raw_candidates": len(raw),
        "raw_candidates_dedup": len(dedup_raw),
        "raw_origin_regime_counts_dedup": dict(by_origin),
        "stc_confirmations_30d": len(confirmations),
        "stc_confirmations_30d_dedup": len(dedup_conf),
        "confirmed_origin_regime_counts": dict(by_confirm),
        "confirmation_regime_counts": dict(by_confirm_regime),
        **horizon_rates,
        "avg_wait_days": round(mean(wait_days), 2) if wait_days else None,
        "median_wait_days": round(median(wait_days), 2) if wait_days else None,
        "forward_from_confirmation_date_dedup": summarize_forward(dedup_conf),
        "concentration_confirmations_dedup": concentration(dedup_conf),
        "sample_confirmations": dedup_conf[:10],
    }


def phase3f_baseline() -> dict[str, Any]:
    if not PHASE3F_PATH.exists():
        return {}
    try:
        obj = load_json(PHASE3F_PATH)
        out = {}
        for rule, row in obj.get("sideways_rule_results", {}).items():
            f = row.get("forward_daily_top1_dedup", {})
            out[rule] = {
                "dedup_top1_count": row.get("dedup_top1_count"),
                "20d_avg_excess_pct": f.get("20d", {}).get("avg_excess_pct"),
                "30d_avg_excess_pct": f.get("30d", {}).get("avg_excess_pct"),
                "20d_excess_win_rate_pct": f.get("20d", {}).get("excess_win_rate_pct"),
                "30d_excess_win_rate_pct": f.get("30d", {}).get("excess_win_rate_pct"),
            }
        return out
    except Exception:
        return {}


def decision_from_screen(rule_results: dict[str, Any]) -> dict[str, Any]:
    side80 = rule_results.get("SIDEWAYS_STC80", {})
    f20 = side80.get("forward_daily_top1_dedup", {}).get("20d", {})
    f30 = side80.get("forward_daily_top1_dedup", {}).get("30d", {})
    n20 = f20.get("n", 0) or 0
    ex20 = f20.get("avg_excess_pct")
    ex30 = f30.get("avg_excess_pct")
    wr20 = f20.get("excess_win_rate_pct")
    if n20 >= 20 and ex20 is not None and ex30 is not None and ex20 > 0 and ex30 > 0 and (wr20 or 0) >= 50:
        return {
            "decision": "SIDEWAYS_STC_SCREEN_PROMISING_DIAGNOSTIC_ONLY",
            "reason": "STC Screen produced positive 20D/30D excess with adequate sample. Still diagnostic only; execution requires separate portfolio simulation.",
        }
    if n20 >= 10 and ex20 is not None and ex20 > 0:
        return {
            "decision": "SIDEWAYS_STC_SCREEN_OBSERVATIONAL_ONLY",
            "reason": "STC Screen improved over single-day candidates but evidence is not strong enough for execution-layer approval.",
        }
    return {
        "decision": "SIDEWAYS_DOWNTREND_STC_WATCHLIST_ONLY_FOR_NOW",
        "reason": "Smooth Trend Confirmation does not yet provide sufficient execution-layer evidence. Use as Watchlist/radar only.",
    }


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

    spx_dates, spx_closes = load_price_series("^GSPC")
    if not spx_dates:
        spx_dates, spx_closes = load_price_series("GSPC")
    if not spx_dates:
        raise SystemExit("SPX price series not found under data/prices.")

    regime_daily = load_regime_daily()
    price_map = load_all_price_series()
    builder = DailySignalBuilder(price_map)

    stc_candidates_by_rule, stc_diag = screen_stc_candidates(builder, spx_dates, regime_daily)

    rule_results = {}
    for rule, rows in sorted(stc_candidates_by_rule.items()):
        daily_top1 = top1_by_date(rows)
        enriched_all = enrich_forward(rows, price_map, spx_dates, spx_closes)
        enriched_top1 = enrich_forward(daily_top1, price_map, spx_dates, spx_closes)
        dedup_all = dedup_by_symbol_gap(enriched_all, spx_dates, DEDUP_GAP_DAYS)
        dedup_top1 = dedup_by_symbol_gap(enriched_top1, spx_dates, DEDUP_GAP_DAYS)
        rule_results[rule] = {
            "raw_candidates": len(rows),
            "candidate_days": len({r["date"] for r in rows}),
            "daily_top1_count": len(daily_top1),
            "dedup_all_count": len(dedup_all),
            "dedup_top1_count": len(dedup_top1),
            "forward_all_dedup": summarize_forward(dedup_all),
            "forward_daily_top1_dedup": summarize_forward(dedup_top1),
            "concentration_top1_dedup": concentration(dedup_top1),
            "sample_top1": dedup_top1[:10],
        }

    # Ensure expected rule keys exist even when no candidates.
    for rule in ["SIDEWAYS_STC80", "SIDEWAYS_STC85", "SIDEWAYS_STC90", "DOWNTREND_STC90"]:
        rule_results.setdefault(rule, {
            "raw_candidates": 0,
            "candidate_days": 0,
            "daily_top1_count": 0,
            "dedup_all_count": 0,
            "dedup_top1_count": 0,
            "forward_all_dedup": summarize_forward([]),
            "forward_daily_top1_dedup": summarize_forward([]),
            "concentration_top1_dedup": concentration([]),
            "sample_top1": [],
        })

    watchlist_funnel = build_watchlist_funnel(builder, spx_dates, regime_daily, price_map, spx_dates, spx_closes)
    p3f = phase3f_baseline()
    decision = decision_from_screen(rule_results)

    result = {
        "status": "DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "strategy_id": E1R_ID,
        "inputs": {
            "backtest": str(BACKTEST_PATH),
            "prices_dir": str(PRICES_DIR),
            "regime_source": str(REGIME_PATH),
            "phase3f_sideways_baseline": str(PHASE3F_PATH),
        },
        "fairness_controls": {
            "same_regime_map_as_e1r_review": True,
            "same_backtest_export_window": True,
            "does_not_change_trading_logic": True,
            "stc_screen_uses_only_asof_signal_date_data": True,
            "watchlist_funnel_forward_return_starts_at_confirmation_date": True,
            "execution_decision_uses_stc_screen_not_watchlist_funnel": True,
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
        },
        "stc_definition_v0_1": {
            "score_max": 100,
            "components": {
                "rs_smooth": 30,
                "rank_persistence": 20,
                "momentum_smooth": 25,
                "price_structure": 25,
            },
            "rule_keys": list(rule_results.keys()),
            "note": "Research prior only. Not a frozen trading rule.",
        },
        "stc_screen_smooth_first_then_find_strong": {
            "diagnostics": stc_diag,
            "rule_results": rule_results,
        },
        "watchlist_funnel_find_strong_then_smooth_validate": watchlist_funnel,
        "phase3f_single_day_sideways_baseline": p3f,
        "decision": decision,
        "interpretation": {
            "primary_execution_evidence": "STC Screen only",
            "watchlist_funnel_usage": "Watchlist/radar only; not a buy signal",
            "next_step": "If STC Screen is promising, run a separate portfolio simulation before any execution-layer change.",
        },
    }

    OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    md = []
    md.append("# E1-R Phase 3G Smooth Trend Confirmation Diagnostic")
    md.append("")
    md.append(f"Generated: `{result['generated_at']}`")
    md.append("")
    md.append("Status: **DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE**")
    md.append("")
    md.append("## 1. Question")
    md.append("")
    md.append("Should SIDEWAYS / DOWNTREND strong stocks be evaluated by smoothing first, then selecting persistent leaders, rather than buying single-day strength?")
    md.append("")
    md.append("A. **STC Screen** = smooth first, then find strong stocks. This is the only branch that can later be considered for execution-layer research.")
    md.append("")
    md.append("B. **Watchlist Funnel** = find single-day strong stocks first, then validate whether they later pass STC. This is Watchlist / radar only.")
    md.append("")
    md.append("## 2. STC Screen Results")
    md.append("")
    md.append("| Rule | Raw | Days | Dedup Top1 | 20D Avg | 20D Excess | 20D Excess WR | 30D Avg | 30D Excess | 30D Excess WR |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for rule in ["SIDEWAYS_STC80", "SIDEWAYS_STC85", "SIDEWAYS_STC90", "DOWNTREND_STC90"]:
        rr = rule_results[rule]
        f20 = rr["forward_daily_top1_dedup"]["20d"]
        f30 = rr["forward_daily_top1_dedup"]["30d"]
        md.append(
            f"| {rule} | {rr['raw_candidates']} | {rr['candidate_days']} | {rr['dedup_top1_count']} | "
            f"{pct_str(f20.get('avg_return_pct'))} | {pct_str(f20.get('avg_excess_pct'))} | {f20.get('excess_win_rate_pct')}% | "
            f"{pct_str(f30.get('avg_return_pct'))} | {pct_str(f30.get('avg_excess_pct'))} | {f30.get('excess_win_rate_pct')}% |"
        )
    md.append("")
    md.append("## 3. Watchlist Funnel")
    md.append("")
    md.append(f"Raw single-day watchlist candidates, dedup: **{watchlist_funnel['raw_candidates_dedup']}**")
    md.append("")
    md.append(f"STC confirmations within 30D, dedup: **{watchlist_funnel['stc_confirmations_30d_dedup']}**")
    md.append("")
    md.append(f"Confirmation rates: 10D={watchlist_funnel.get('10d_confirmation_rate_pct')}%, 20D={watchlist_funnel.get('20d_confirmation_rate_pct')}%, 30D={watchlist_funnel.get('30d_confirmation_rate_pct')}%")
    md.append("")
    f20 = watchlist_funnel["forward_from_confirmation_date_dedup"]["20d"]
    f30 = watchlist_funnel["forward_from_confirmation_date_dedup"]["30d"]
    md.append(f"Forward from confirmation date: 20D excess **{pct_str(f20.get('avg_excess_pct'))}**, 30D excess **{pct_str(f30.get('avg_excess_pct'))}**.")
    md.append("")
    md.append("## 4. Phase 3F Single-Day Baseline")
    md.append("")
    md.append("| Phase 3F Rule | Dedup Top1 | 20D Excess | 30D Excess |")
    md.append("|---|---:|---:|---:|")
    for rule, row in p3f.items():
        md.append(f"| {rule} | {row.get('dedup_top1_count')} | {pct_str(row.get('20d_avg_excess_pct'))} | {pct_str(row.get('30d_avg_excess_pct'))} |")
    md.append("")
    md.append("## 5. Decision")
    md.append("")
    md.append(f"Decision: **{decision['decision']}**")
    md.append("")
    md.append(f"Reason: {decision['reason']}")
    md.append("")
    md.append("## 6. Frozen Interpretation")
    md.append("")
    md.append("This diagnostic separates trading evidence from watchlist evidence. Future execution approval can only be based on the STC Screen branch, because it uses smoothed information already available as of the signal date. The Watchlist Funnel is useful for early radar and upgrade observation, but not as a buy signal.")
    md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("E1-R PHASE 3G SMOOTH TREND CONFIRMATION DIAGNOSTIC")
    print("Status: DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE")
    print(f"Symbols loaded: {len(price_map)}")
    print(f"Regime day counts: {stc_diag.get('regime_day_counts')}")
    print("\nSTC Screen: smooth first, then find strong stocks")
    for rule in ["SIDEWAYS_STC80", "SIDEWAYS_STC85", "SIDEWAYS_STC90", "DOWNTREND_STC90"]:
        rr = rule_results[rule]
        f20 = rr["forward_daily_top1_dedup"]["20d"]
        f30 = rr["forward_daily_top1_dedup"]["30d"]
        print(
            f"  {rule}: raw={rr['raw_candidates']} days={rr['candidate_days']} dedup_top1={rr['dedup_top1_count']} "
            f"20D avg={pct_str(f20.get('avg_return_pct'))} excess={pct_str(f20.get('avg_excess_pct'))} excessWR={f20.get('excess_win_rate_pct')}% "
            f"30D avg={pct_str(f30.get('avg_return_pct'))} excess={pct_str(f30.get('avg_excess_pct'))}"
        )

    print("\nWatchlist Funnel: find strong first, then smooth validate")
    print(f"  raw_dedup={watchlist_funnel['raw_candidates_dedup']} confirmations_30d_dedup={watchlist_funnel['stc_confirmations_30d_dedup']}")
    print(
        f"  confirmation rates: 10D={watchlist_funnel.get('10d_confirmation_rate_pct')}% "
        f"20D={watchlist_funnel.get('20d_confirmation_rate_pct')}% "
        f"30D={watchlist_funnel.get('30d_confirmation_rate_pct')}%"
    )
    wf20 = watchlist_funnel["forward_from_confirmation_date_dedup"]["20d"]
    wf30 = watchlist_funnel["forward_from_confirmation_date_dedup"]["30d"]
    print(f"  forward from confirmation: 20D excess={pct_str(wf20.get('avg_excess_pct'))} 30D excess={pct_str(wf30.get('avg_excess_pct'))}")

    print(f"\nDecision: {decision['decision']}")
    print(f"Reason: {decision['reason']}")
    print(f"Output: {OUT_JSON}")
    print(f"Report: {OUT_MD}")


if __name__ == "__main__":
    main()
