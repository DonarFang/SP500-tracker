#!/usr/bin/env python3
"""
E1-R Phase 3D Emerging Channel Diagnostic

Diagnostic only. Does not modify trading logic, orders, exports/backtest.json,
or any strategy implementation.

Purpose:
- Evaluate whether the Emerging channel has enough independent quality to justify
  a future separate 0.5-slot execution channel.
- Keep E1 vs E1-R comparisons on the same market/regime framework.
- Diagnose Emerging signal quality without allowing it to compete unfairly with
  Confirmed under the current Phase 3B Top-1 priority rule.

Expected inputs after `python3 run_backtest.py`:
- exports/backtest.json
- exports/e1r_candidates.json                         optional fallback
- data/prices/*.json
- data/research/e1r/e1r_candidate_forward_return_diagnostic.json
- data/research/e1r/e1r_phase3c_channel_diagnostic.json
- data/research/e1_5y/regimes/spx_regime_daily.json

Outputs:
- data/research/e1r/e1r_phase3d_emerging_channel_diagnostic.json
- data/research/e1r/E1R_PHASE3D_EMERGING_CHANNEL_DIAGNOSTIC_REPORT.md
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean, median
from typing import Any

E1_ID = "E1_AUDITED_G4_MINHOLD10"
E1R_ID = "E1R_REGIME_AWARE_V0_1"
CONFIRMED = "E1R_UPTREND_CONFIRMED"
EMERGING = "E1R_UPTREND_EMERGING"

BACKTEST_PATH = Path("exports/backtest.json")
CANDIDATES_EXPORT_PATH = Path("exports/e1r_candidates.json")
PRICES_DIR = Path("data/prices")
FWD_DIAG_PATH = Path("data/research/e1r/e1r_candidate_forward_return_diagnostic.json")
PHASE3C_PATH = Path("data/research/e1r/e1r_phase3c_channel_diagnostic.json")
REGIME_PATH = Path("data/research/e1_5y/regimes/spx_regime_daily.json")

OUT_DIR = Path("data/research/e1r")
OUT_JSON = OUT_DIR / "e1r_phase3d_emerging_channel_diagnostic.json"
OUT_MD = OUT_DIR / "E1R_PHASE3D_EMERGING_CHANNEL_DIAGNOSTIC_REPORT.md"

HORIZONS = [5, 10, 20, 30]
DEDUP_GAP_DAYS = 5
MAX_POSITIONS_PROXY = 3


def load_json(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing required input: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def pct_str(x: Any) -> str:
    if isinstance(x, (int, float)) and math.isfinite(float(x)):
        return f"{float(x):+.2f}%"
    return "n/a"


def num(x: Any, default: float = 0.0) -> float:
    try:
        if x is None:
            return default
        y = float(x)
        return y if math.isfinite(y) else default
    except Exception:
        return default


def round_or_none(x: Any, nd: int = 3) -> Any:
    if isinstance(x, (int, float)) and math.isfinite(float(x)):
        return round(float(x), nd)
    return None


def safe_variant_results(backtest: dict[str, Any]) -> dict[str, Any]:
    try:
        return backtest["backtest"]["results"]["layer_d"]["variant_results"]
    except KeyError as exc:
        raise KeyError("Cannot locate backtest.results.layer_d.variant_results in exports/backtest.json") from exc


def load_candidates(e1r_result: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = e1r_result.get("e1r_candidates", []) or []
    if candidates:
        return candidates

    if CANDIDATES_EXPORT_PATH.exists():
        obj = load_json(CANDIDATES_EXPORT_PATH)
        if isinstance(obj, list):
            return obj
        if isinstance(obj, dict):
            return obj.get("candidates", []) or []

    raise RuntimeError(
        "No E1-R candidates found. Run `python3 run_backtest.py` first so E1-R candidates are available."
    )


def candidate_sort_key(c: dict[str, Any]) -> tuple:
    # Emerging-only ranking: do not give Confirmed any priority because this diagnostic
    # evaluates Emerging as an independent channel.
    return (
        int(c.get("leader_rank") or 9999),
        -num(c.get("leader_score")),
        -num(c.get("momentum_score")),
        -num(c.get("momentum_acceleration")),
        -num(c.get("rs_20d_improvement")),
        -num(c.get("rs_score")),
        str(c.get("symbol") or ""),
    )


def phase3b_sort_key(c: dict[str, Any]) -> tuple:
    # Mirrors Phase 3B: Confirmed first, then rank/score/acceleration.
    typ = c.get("e1r_entry_type")
    typ_pri = 0 if typ == CONFIRMED else 1
    return (
        typ_pri,
        int(c.get("leader_rank") or 9999),
        -num(c.get("leader_score")),
        -num(c.get("momentum_score")),
        -num(c.get("momentum_acceleration")),
        -num(c.get("rs_20d_improvement")),
        str(c.get("symbol") or ""),
    )


def series_from_json(obj: Any) -> tuple[list[str], list[float]]:
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

    for dk in ["dates", "date", "Date"]:
        for ck in ["close", "closes", "prices", "adj_close", "Adj Close", "Close"]:
            if dk in obj and ck in obj and isinstance(obj[dk], list) and isinstance(obj[ck], list):
                return [str(x) for x in obj[dk]], [float(x) for x in obj[ck]]

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
            rows.append((d, float(c)))
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


def pct(a: float, b: float) -> float | None:
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
    return pct(series_closes[i], series_closes[j])


def summarize(vals: list[float | None]) -> dict[str, Any]:
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


def enrich_forward(rows: list[dict[str, Any]], spx_dates: list[str], spx_closes: list[float]) -> tuple[list[dict[str, Any]], Counter]:
    price_cache: dict[str, tuple[list[str], list[float]]] = {"^GSPC": (spx_dates, spx_closes)}
    missing = Counter()
    enriched = []
    for r0 in rows:
        sym = r0.get("symbol")
        d = r0.get("date")
        if not sym or not d:
            continue
        if sym not in price_cache:
            price_cache[sym] = load_price_series(sym)
        dates, closes = price_cache[sym]
        if not dates:
            missing[sym] += 1
            continue
        r = dict(r0)
        for h in HORIZONS:
            stock = forward_return_for(dates, closes, d, h)
            spx = forward_return_for(spx_dates, spx_closes, d, h)
            r[f"fwd_{h}d_pct"] = round_or_none(stock, 4)
            r[f"spx_fwd_{h}d_pct"] = round_or_none(spx, 4)
            r[f"excess_{h}d_pct"] = round_or_none(stock - spx, 4) if stock is not None and spx is not None else None
        enriched.append(r)
    return enriched, missing


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


def active_positions_from_trades(trades: list[dict[str, Any]], date: str) -> set[str]:
    active = set()
    for t in trades:
        sym = t.get("symbol")
        ed = t.get("entry_date")
        xd = t.get("exit_date")
        if not sym or not ed:
            continue
        if ed <= date and (not xd or date < xd):
            active.add(sym)
    return active


def upgrade_stats(emerging_rows: list[dict[str, Any]], all_candidates_by_symbol: dict[str, list[dict[str, Any]]], master_dates: list[str]) -> dict[str, Any]:
    idx = {d: i for i, d in enumerate(master_dates)}
    horizons = [5, 10, 20, 30]
    result = {}
    upgrade_day_gaps = []

    for h in horizons:
        n = 0
        upgraded = 0
        for r in emerging_rows:
            sym = r.get("symbol")
            d = r.get("date")
            if not sym or d not in idx:
                continue
            n += 1
            i0 = idx[d]
            found_gap = None
            for c in all_candidates_by_symbol.get(sym, []):
                if c.get("e1r_entry_type") != CONFIRMED:
                    continue
                cd = c.get("date")
                if cd not in idx:
                    continue
                gap = idx[cd] - i0
                if 0 < gap <= h:
                    found_gap = gap
                    break
            if found_gap is not None:
                upgraded += 1
                upgrade_day_gaps.append(found_gap)
        result[f"within_{h}d"] = {
            "n": n,
            "upgraded": upgraded,
            "upgrade_rate_pct": round(upgraded / n * 100, 1) if n else 0.0,
        }

    result["avg_upgrade_gap_days"] = round(mean(upgrade_day_gaps), 2) if upgrade_day_gaps else None
    result["median_upgrade_gap_days"] = round(median(upgrade_day_gaps), 2) if upgrade_day_gaps else None
    return result


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


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    bj = load_json(BACKTEST_PATH)
    variants = safe_variant_results(bj)
    if E1_ID not in variants or E1R_ID not in variants:
        raise KeyError(f"Missing required variants. Found: {list(variants.keys())}")

    e1r = variants[E1R_ID]
    e1r_trades = e1r.get("trades", []) or []
    all_candidates = load_candidates(e1r)

    spx_dates, spx_closes = load_price_series("^GSPC")
    if not spx_dates:
        spx_dates, spx_closes = load_price_series("GSPC")
    if not spx_dates:
        raise SystemExit("SPX price series not found under data/prices.")

    phase3c = load_json(PHASE3C_PATH) if PHASE3C_PATH.exists() else {}
    fwd_diag = load_json(FWD_DIAG_PATH) if FWD_DIAG_PATH.exists() else {}

    by_date: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_symbol: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for c in all_candidates:
        d = c.get("date")
        sym = c.get("symbol")
        if d:
            by_date[d].append(c)
        if sym:
            by_symbol[sym].append(c)
    for sym in by_symbol:
        by_symbol[sym].sort(key=lambda x: x.get("date", ""))

    emerging_all = [c for c in all_candidates if c.get("e1r_entry_type") == EMERGING]

    emerging_top1 = []
    phase3b_top1 = []
    daily_block_reasons = Counter()
    capacity_rows = []
    for d, cs in sorted(by_date.items()):
        emerging = [c for c in cs if c.get("e1r_entry_type") == EMERGING]
        confirmed = [c for c in cs if c.get("e1r_entry_type") == CONFIRMED]
        if not emerging:
            continue

        e_top = sorted(emerging, key=candidate_sort_key)[0]
        emerging_top1.append(e_top)

        p3b_top = sorted(cs, key=phase3b_sort_key)[0]
        phase3b_top1.append(p3b_top)

        active = active_positions_from_trades(e1r_trades, d)
        capacity_available = len(active) < MAX_POSITIONS_PROXY
        already_holding = e_top.get("symbol") in active

        if confirmed:
            daily_block_reasons["confirmed_exists_same_day"] += 1
        if p3b_top.get("e1r_entry_type") == CONFIRMED:
            daily_block_reasons["phase3b_top1_is_confirmed"] += 1
        if not capacity_available:
            daily_block_reasons["no_capacity_proxy"] += 1
        if already_holding:
            daily_block_reasons["already_holding_symbol_proxy"] += 1

        if capacity_available and not already_holding:
            capacity_rows.append(e_top)

    emerging_top1_enriched, missing_top1 = enrich_forward(emerging_top1, spx_dates, spx_closes)
    emerging_top1_dedup = dedup_by_symbol_gap(emerging_top1_enriched, spx_dates, DEDUP_GAP_DAYS)

    emerging_all_enriched, missing_all = enrich_forward(emerging_all, spx_dates, spx_closes)
    emerging_all_dedup = dedup_by_symbol_gap(emerging_all_enriched, spx_dates, DEDUP_GAP_DAYS)

    capacity_enriched, missing_capacity = enrich_forward(capacity_rows, spx_dates, spx_closes)
    capacity_dedup = dedup_by_symbol_gap(capacity_enriched, spx_dates, DEDUP_GAP_DAYS)

    upgrade_all = upgrade_stats(emerging_all_dedup, by_symbol, spx_dates)
    upgrade_top1 = upgrade_stats(emerging_top1_dedup, by_symbol, spx_dates)

    phase3c_funnel = phase3c.get("candidate_funnel", {})
    prior_dedup_summary = fwd_diag.get("dedup_summary", {})
    prior_emerging = prior_dedup_summary.get(EMERGING, {})

    result = {
        "status": "DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "strategy_id": E1R_ID,
        "inputs": {
            "backtest": str(BACKTEST_PATH),
            "candidate_export_fallback": str(CANDIDATES_EXPORT_PATH),
            "phase3c": str(PHASE3C_PATH),
            "candidate_forward_return_diagnostic": str(FWD_DIAG_PATH),
            "prices_dir": str(PRICES_DIR),
        },
        "fairness_controls": {
            "does_not_change_trading_logic": True,
            "emerging_evaluated_independently_from_confirmed_top1_priority": True,
            "same_price_data_and_spx_forward_benchmark": True,
            "dedup_gap_trading_days": DEDUP_GAP_DAYS,
        },
        "phase3c_baseline": {
            "candidate_type_counts": phase3c_funnel.get("candidate_type_counts"),
            "top1_type_counts_under_phase3b_priority": phase3c_funnel.get("top1_type_counts_under_phase3b_priority"),
            "executed_trade_type_counts": phase3c_funnel.get("executed_trade_type_counts"),
        },
        "emerging_funnel": {
            "raw_emerging_candidates": len(emerging_all),
            "emerging_candidate_days": len({c.get("date") for c in emerging_all if c.get("date")}),
            "emerging_top1_days": len(emerging_top1),
            "emerging_top1_dedup_count": len(emerging_top1_dedup),
            "emerging_capacity_proxy_days": len(capacity_rows),
            "emerging_capacity_proxy_dedup_count": len(capacity_dedup),
            "daily_block_reasons_proxy": dict(daily_block_reasons),
            "missing_price_symbols_top1": missing_top1.most_common(10),
            "missing_price_symbols_all": missing_all.most_common(10),
        },
        "forward_return_summary": {
            "emerging_all_dedup": {
                "count": len(emerging_all_dedup),
                "summary": summarize_forward(emerging_all_dedup),
                "concentration": concentration(emerging_all_dedup),
            },
            "emerging_only_daily_top1_dedup": {
                "count": len(emerging_top1_dedup),
                "summary": summarize_forward(emerging_top1_dedup),
                "concentration": concentration(emerging_top1_dedup),
            },
            "emerging_capacity_proxy_dedup": {
                "count": len(capacity_dedup),
                "summary": summarize_forward(capacity_dedup),
                "concentration": concentration(capacity_dedup),
            },
            "prior_emerging_pool_diagnostic": prior_emerging,
        },
        "upgrade_path": {
            "emerging_all_dedup": upgrade_all,
            "emerging_only_daily_top1_dedup": upgrade_top1,
        },
        "interpretation": {
            "phase3d_question": "If Emerging does not compete with Confirmed Top-1, does it justify a future 0.5-slot channel?",
            "preliminary_rule": "Diagnostic only. A future execution test requires positive excess return, controlled concentration, and acceptable capacity/upgrade path.",
            "notes": [
                "Emerging Top-1 evaluates the best Emerging candidate each day regardless of Confirmed priority.",
                "Capacity proxy is approximate because it does not replay order execution; it only uses Phase 3B E1-R trade intervals.",
                "Upgrade path measures whether an Emerging candidate later becomes Confirmed for the same symbol.",
            ],
        },
    }

    OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    def md_forward_block(title: str, block: dict[str, Any]) -> list[str]:
        rows = [f"### {title}", ""]
        rows.append(f"Count: **{block.get('count')}**")
        rows.append("")
        rows.append("| Horizon | Avg | Excess | Win Rate | Excess WR | N |")
        rows.append("|---|---:|---:|---:|---:|---:|")
        for h in HORIZONS:
            x = block.get("summary", {}).get(f"{h}d", {})
            rows.append(
                f"| {h}D | {pct_str(x.get('avg_return_pct'))} | {pct_str(x.get('avg_excess_pct'))} | "
                f"{x.get('win_rate_pct', 'n/a')}% | {x.get('excess_win_rate_pct', 'n/a')}% | {x.get('n', 0)} |"
            )
        conc = block.get("concentration", {})
        rows.append("")
        rows.append(f"Unique symbols: **{conc.get('unique_symbols')}**; Top-10 share: **{conc.get('top10_share_pct')}%**")
        rows.append(f"Top symbols: `{conc.get('top10_symbol_counts')}`")
        rows.append("")
        return rows

    md = []
    md.append("# E1-R Phase 3D Emerging Channel Diagnostic")
    md.append("")
    md.append(f"Generated: `{result['generated_at']}`")
    md.append("")
    md.append("Status: **DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE**")
    md.append("")
    md.append("## 1. Purpose")
    md.append("")
    md.append("Evaluate whether Emerging deserves a future separate 0.5-slot channel if it does not have to compete with Confirmed under the current Phase 3B Top-1 priority rule.")
    md.append("")
    md.append("## 2. Phase 3C Baseline")
    md.append("")
    md.append(f"Candidate type counts: `{result['phase3c_baseline']['candidate_type_counts']}`")
    md.append("")
    md.append(f"Top-1 type counts under Phase 3B priority: `{result['phase3c_baseline']['top1_type_counts_under_phase3b_priority']}`")
    md.append("")
    md.append(f"Executed trade type counts: `{result['phase3c_baseline']['executed_trade_type_counts']}`")
    md.append("")
    md.append("## 3. Emerging Funnel")
    md.append("")
    ef = result["emerging_funnel"]
    md.append(f"Raw Emerging candidates: **{ef['raw_emerging_candidates']}**")
    md.append(f"Emerging candidate days: **{ef['emerging_candidate_days']}**")
    md.append(f"Emerging-only daily Top1 days: **{ef['emerging_top1_days']}**")
    md.append(f"Emerging-only Top1 dedup count: **{ef['emerging_top1_dedup_count']}**")
    md.append(f"Capacity proxy days: **{ef['emerging_capacity_proxy_days']}**")
    md.append(f"Capacity proxy dedup count: **{ef['emerging_capacity_proxy_dedup_count']}**")
    md.append("")
    md.append(f"Proxy block reasons: `{ef['daily_block_reasons_proxy']}`")
    md.append("")
    md.append("## 4. Forward Return Summary")
    md.append("")
    fs = result["forward_return_summary"]
    md.extend(md_forward_block("Emerging All Dedup", fs["emerging_all_dedup"]))
    md.extend(md_forward_block("Emerging-only Daily Top1 Dedup", fs["emerging_only_daily_top1_dedup"]))
    md.extend(md_forward_block("Emerging Capacity Proxy Dedup", fs["emerging_capacity_proxy_dedup"]))
    md.append("## 5. Upgrade Path")
    md.append("")
    md.append("| Sample | 5D Upgrade | 10D Upgrade | 20D Upgrade | 30D Upgrade | Avg Gap | Median Gap |")
    md.append("|---|---:|---:|---:|---:|---:|---:|")
    for name, x in result["upgrade_path"].items():
        md.append(
            f"| {name} | "
            f"{x.get('within_5d', {}).get('upgrade_rate_pct')}% | "
            f"{x.get('within_10d', {}).get('upgrade_rate_pct')}% | "
            f"{x.get('within_20d', {}).get('upgrade_rate_pct')}% | "
            f"{x.get('within_30d', {}).get('upgrade_rate_pct')}% | "
            f"{x.get('avg_upgrade_gap_days')} | {x.get('median_upgrade_gap_days')} |"
        )
    md.append("")
    md.append("## 6. Interpretation Guardrails")
    md.append("")
    md.append("- This is not an execution backtest.")
    md.append("- Capacity proxy is approximate and does not replay cash, fills, partial sizing, or same-day order priority.")
    md.append("- A future Phase 3E execution test should be allowed only if Emerging Top1 shows positive excess return with reasonable concentration and upgrade behavior.")
    md.append("")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    top1_20 = result["forward_return_summary"]["emerging_only_daily_top1_dedup"]["summary"].get("20d", {})
    top1_30 = result["forward_return_summary"]["emerging_only_daily_top1_dedup"]["summary"].get("30d", {})
    cap_20 = result["forward_return_summary"]["emerging_capacity_proxy_dedup"]["summary"].get("20d", {})
    up = result["upgrade_path"]["emerging_only_daily_top1_dedup"]

    print("E1-R PHASE 3D EMERGING CHANNEL DIAGNOSTIC")
    print("Status: DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE")
    print(f"Raw Emerging candidates: {ef['raw_emerging_candidates']} across {ef['emerging_candidate_days']} days")
    print(f"Emerging-only Top1 days: {ef['emerging_top1_days']} dedup={ef['emerging_top1_dedup_count']}")
    print(f"Capacity proxy days: {ef['emerging_capacity_proxy_days']} dedup={ef['emerging_capacity_proxy_dedup_count']}")
    print(f"Proxy block reasons: {ef['daily_block_reasons_proxy']}")
    print("")
    print("Emerging-only Top1 forward returns:")
    print(f"  20D avg={pct_str(top1_20.get('avg_return_pct'))} excess={pct_str(top1_20.get('avg_excess_pct'))} WR={top1_20.get('win_rate_pct')}% excessWR={top1_20.get('excess_win_rate_pct')}% n={top1_20.get('n')}")
    print(f"  30D avg={pct_str(top1_30.get('avg_return_pct'))} excess={pct_str(top1_30.get('avg_excess_pct'))} WR={top1_30.get('win_rate_pct')}% excessWR={top1_30.get('excess_win_rate_pct')}% n={top1_30.get('n')}")
    print("")
    print("Emerging capacity proxy forward returns:")
    print(f"  20D avg={pct_str(cap_20.get('avg_return_pct'))} excess={pct_str(cap_20.get('avg_excess_pct'))} WR={cap_20.get('win_rate_pct')}% excessWR={cap_20.get('excess_win_rate_pct')}% n={cap_20.get('n')}")
    print("")
    print("Emerging Top1 upgrade path:")
    print(f"  10D upgrade={up.get('within_10d', {}).get('upgrade_rate_pct')}%")
    print(f"  20D upgrade={up.get('within_20d', {}).get('upgrade_rate_pct')}%")
    print(f"  30D upgrade={up.get('within_30d', {}).get('upgrade_rate_pct')}%")
    print(f"  avg_gap={up.get('avg_upgrade_gap_days')} median_gap={up.get('median_upgrade_gap_days')}")
    print("")
    print(f"Output: {OUT_JSON}")
    print(f"Report: {OUT_MD}")


if __name__ == "__main__":
    main()
