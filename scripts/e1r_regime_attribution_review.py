#!/usr/bin/env python3
"""
E1 vs E1-R Regime Attribution Review

Diagnostic only. Does not change trading logic.
Compares E1 and E1-R under identical market-regime segmentation using the same
SPX weekly-regime daily map and the same overlapping daily-equity dates.

Outputs:
  data/research/e1r/e1r_regime_attribution_review.json
  data/research/e1r/E1R_REGIME_ATTRIBUTION_REVIEW.md
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

BACKTEST_PATH = Path("exports/backtest.json")
REGIME_PATH = Path("data/research/e1_5y/regimes/spx_regime_daily.json")
OUT_DIR = Path("data/research/e1r")
OUT_JSON = OUT_DIR / "e1r_regime_attribution_review.json"
OUT_MD = OUT_DIR / "E1R_REGIME_ATTRIBUTION_REVIEW.md"

E1_ID = "E1_AUDITED_G4_MINHOLD10"
E1R_ID = "E1R_REGIME_AWARE_V0_1"
REGIME_ORDER = ["UPTREND", "SIDEWAYS", "DOWNTREND", "UNCLASSIFIED"]


def _load_json(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return json.loads(path.read_text())


def _norm_regime_value(v: Any) -> str:
    if isinstance(v, dict):
        v = v.get("regime") or v.get("spx_regime") or v.get("weekly_regime")
    if v is None:
        return "UNCLASSIFIED"
    s = str(v).strip().upper()
    return s if s in set(REGIME_ORDER) else "UNCLASSIFIED"


def _load_regime_daily(path: Path) -> Dict[str, str]:
    obj = _load_json(path)
    raw = obj.get("daily_regime", obj) if isinstance(obj, dict) else {}
    if not isinstance(raw, dict):
        raise ValueError(f"Unexpected regime daily format in {path}")
    return {str(k): _norm_regime_value(v) for k, v in raw.items()}


def _variant_results(backtest_obj: Dict[str, Any]) -> Dict[str, Any]:
    try:
        return backtest_obj["backtest"]["results"]["layer_d"]["variant_results"]
    except KeyError as exc:
        raise KeyError("Cannot find backtest.results.layer_d.variant_results") from exc


def _daily_records(variant: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = variant.get("daily_equity_records") or []
    out = []
    for r in rows:
        d = r.get("date")
        eq = r.get("total_equity")
        if d is None or eq is None:
            continue
        out.append(r)
    out.sort(key=lambda x: x["date"])
    return out


def _safe_float(x: Any, default: float = 0.0) -> float:
    try:
        if x is None:
            return default
        f = float(x)
        if math.isnan(f) or math.isinf(f):
            return default
        return f
    except Exception:
        return default


def _compound_pct(returns_pct: Iterable[float]) -> float:
    v = 1.0
    for r in returns_pct:
        v *= 1.0 + _safe_float(r) / 100.0
    return round((v - 1.0) * 100.0, 4)


def _max_drawdown_from_equity(equities: List[float]) -> float:
    peak = None
    max_dd = 0.0
    for e in equities:
        if e <= 0:
            continue
        if peak is None or e > peak:
            peak = e
        if peak:
            max_dd = max(max_dd, (peak - e) / peak * 100.0)
    return round(max_dd, 4)


def _build_day_map(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {r["date"]: r for r in rows}


def _initial_equity(rows: List[Dict[str, Any]]) -> float:
    if not rows:
        return 100000.0
    # The first daily mark is normally initial capital or very close to it.
    return _safe_float(rows[0].get("total_equity"), 100000.0) or 100000.0


def _attribution_for_strategy(
    strategy_id: str,
    variant: Dict[str, Any],
    shared_dates: List[str],
    regime_daily: Dict[str, str],
) -> Dict[str, Any]:
    rows = _daily_records(variant)
    day_map = _build_day_map(rows)
    init_eq = _initial_equity(rows)

    prev_equity_by_date: Dict[str, float] = {}
    prev = None
    for r in rows:
        d = r["date"]
        eq = _safe_float(r.get("total_equity"), 0.0)
        prev_equity_by_date[d] = prev if prev is not None else eq
        prev = eq

    bucket: Dict[str, Dict[str, Any]] = {}
    all_days: List[Dict[str, Any]] = []
    for regime in REGIME_ORDER:
        bucket[regime] = {
            "regime": regime,
            "days": 0,
            "dates": [],
            "pnl_abs": 0.0,
            "daily_returns_pct": [],
            "spx_daily_returns_pct": [],
            "exposures_pct": [],
            "open_positions_count": [],
            "equities": [],
            "positive_days": 0,
            "negative_days": 0,
        }

    for d in shared_dates:
        r = day_map[d]
        regime = regime_daily.get(d, "UNCLASSIFIED")
        eq = _safe_float(r.get("total_equity"), 0.0)
        prev_eq = prev_equity_by_date.get(d, eq)
        daily_ret = _safe_float(r.get("daily_return_pct"), 0.0)
        pnl = eq - prev_eq
        b = bucket[regime]
        b["days"] += 1
        b["dates"].append(d)
        b["pnl_abs"] += pnl
        b["daily_returns_pct"].append(daily_ret)
        b["spx_daily_returns_pct"].append(_safe_float(r.get("spx_day_return_pct"), 0.0))
        b["exposures_pct"].append(_safe_float(r.get("exposure_pct"), 0.0))
        b["open_positions_count"].append(_safe_float(r.get("open_positions_count"), 0.0))
        b["equities"].append(eq)
        if daily_ret > 0:
            b["positive_days"] += 1
        elif daily_ret < 0:
            b["negative_days"] += 1
        all_days.append({
            "date": d,
            "regime": regime,
            "equity": round(eq, 2),
            "daily_return_pct": round(daily_ret, 4),
            "spx_day_return_pct": round(_safe_float(r.get("spx_day_return_pct"), 0.0), 4),
            "exposure_pct": round(_safe_float(r.get("exposure_pct"), 0.0), 2),
        })

    summarized = {}
    for regime, b in bucket.items():
        days = b["days"]
        avg_exp = sum(b["exposures_pct"]) / days if days else 0.0
        avg_pos = sum(b["open_positions_count"]) / days if days else 0.0
        pnl_pct_initial = b["pnl_abs"] / init_eq * 100.0 if init_eq else 0.0
        positive_rate = b["positive_days"] / days * 100.0 if days else 0.0
        summarized[regime] = {
            "days": days,
            "date_start": b["dates"][0] if days else None,
            "date_end": b["dates"][-1] if days else None,
            "pnl_abs": round(b["pnl_abs"], 2),
            "pnl_pct_initial": round(pnl_pct_initial, 4),
            "compound_return_pct": _compound_pct(b["daily_returns_pct"]),
            "spx_compound_return_pct": _compound_pct(b["spx_daily_returns_pct"]),
            "excess_compound_vs_spx_pct": round(
                _compound_pct(b["daily_returns_pct"]) - _compound_pct(b["spx_daily_returns_pct"]), 4
            ),
            "avg_daily_return_pct": round(sum(b["daily_returns_pct"]) / days, 4) if days else 0.0,
            "positive_day_rate_pct": round(positive_rate, 2),
            "avg_exposure_pct": round(avg_exp, 2),
            "avg_open_positions": round(avg_pos, 2),
            "max_drawdown_within_regime_pct": _max_drawdown_from_equity(b["equities"]),
        }

    total_start = _safe_float(day_map[shared_dates[0]].get("total_equity"), init_eq) if shared_dates else init_eq
    total_end = _safe_float(day_map[shared_dates[-1]].get("total_equity"), init_eq) if shared_dates else init_eq
    return {
        "strategy_id": strategy_id,
        "research_status": variant.get("research_status"),
        "reported_total_return_pct": variant.get("total_return_pct"),
        "reported_max_drawdown_pct": variant.get("max_drawdown_pct"),
        "reported_profit_factor": variant.get("profit_factor"),
        "reported_sharpe_ratio": variant.get("sharpe_ratio"),
        "reported_exposure_pct": variant.get("exposure_pct"),
        "reported_number_of_trades": variant.get("number_of_trades"),
        "shared_window_start": shared_dates[0] if shared_dates else None,
        "shared_window_end": shared_dates[-1] if shared_dates else None,
        "shared_days": len(shared_dates),
        "initial_equity_observed": round(init_eq, 2),
        "shared_window_start_equity": round(total_start, 2),
        "shared_window_end_equity": round(total_end, 2),
        "shared_window_return_pct": round((total_end / total_start - 1.0) * 100.0, 4) if total_start else 0.0,
        "by_regime": summarized,
        "daily_sample": all_days[:3] + ([{"ellipsis": True}] if len(all_days) > 6 else []) + all_days[-3:],
    }


def _trade_dominant_regime(entry_date: str, exit_date: str, sorted_regime_dates: List[str], regime_daily: Dict[str, str]) -> str:
    days = [d for d in sorted_regime_dates if entry_date <= d <= exit_date]
    if not days:
        return regime_daily.get(entry_date, "UNCLASSIFIED")
    c = Counter(regime_daily.get(d, "UNCLASSIFIED") for d in days)
    return c.most_common(1)[0][0]


def _trade_review(strategy_id: str, variant: Dict[str, Any], regime_daily: Dict[str, str]) -> Dict[str, Any]:
    trades = variant.get("trades") or []
    sorted_dates = sorted(regime_daily.keys())
    out = {r: {"trades": 0, "avg_return_pct": 0.0, "win_rate_pct": 0.0, "sim_end_trades": 0} for r in REGIME_ORDER}
    vals = {r: [] for r in REGIME_ORDER}
    sim = {r: 0 for r in REGIME_ORDER}
    entry_types = Counter()
    for t in trades:
        entry = str(t.get("entry_date") or "")
        exitd = str(t.get("exit_date") or entry)
        dom = t.get("dominant_regime") or _trade_dominant_regime(entry, exitd, sorted_dates, regime_daily)
        dom = _norm_regime_value(dom)
        ret = _safe_float(t.get("return_pct"), 0.0)
        vals[dom].append(ret)
        if t.get("exit_signal") == "SIM_END" or t.get("sim_end_trade"):
            sim[dom] += 1
        entry_types[str(t.get("entry_type") or "LEGACY_E1_ENTRY")] += 1
    for r in REGIME_ORDER:
        v = vals[r]
        out[r] = {
            "trades": len(v),
            "avg_return_pct": round(sum(v) / len(v), 4) if v else 0.0,
            "win_rate_pct": round(sum(1 for x in v if x > 0) / len(v) * 100.0, 2) if v else 0.0,
            "sim_end_trades": sim[r],
        }
    return {"strategy_id": strategy_id, "entry_type_counts": dict(entry_types), "by_dominant_regime": out}


def _make_comparison(e1: Dict[str, Any], e1r: Dict[str, Any]) -> Dict[str, Any]:
    comp = {}
    for regime in REGIME_ORDER:
        a = e1["by_regime"][regime]
        b = e1r["by_regime"][regime]
        comp[regime] = {
            "days": a["days"],
            "e1r_minus_e1_pnl_pct_initial": round(b["pnl_pct_initial"] - a["pnl_pct_initial"], 4),
            "e1r_minus_e1_compound_pct": round(b["compound_return_pct"] - a["compound_return_pct"], 4),
            "e1r_minus_e1_excess_vs_spx_pct": round(b["excess_compound_vs_spx_pct"] - a["excess_compound_vs_spx_pct"], 4),
            "e1r_minus_e1_avg_exposure_pct": round(b["avg_exposure_pct"] - a["avg_exposure_pct"], 2),
            "e1r_minus_e1_max_dd_within_regime_pct": round(
                b["max_drawdown_within_regime_pct"] - a["max_drawdown_within_regime_pct"], 4
            ),
        }
    return comp


def _md_table(headers: List[str], rows: List[List[Any]]) -> str:
    def fmt(x: Any) -> str:
        return "" if x is None else str(x)
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    out += ["| " + " | ".join(fmt(x) for x in row) + " |" for row in rows]
    return "\n".join(out)


def _write_report(result: Dict[str, Any]) -> None:
    e1 = result["strategies"][E1_ID]
    e1r = result["strategies"][E1R_ID]
    comp = result["comparison"]

    rows = []
    for regime in REGIME_ORDER:
        a = e1["by_regime"][regime]
        b = e1r["by_regime"][regime]
        c = comp[regime]
        rows.append([
            regime,
            a["days"],
            f"{a['pnl_pct_initial']:+.2f}%",
            f"{b['pnl_pct_initial']:+.2f}%",
            f"{c['e1r_minus_e1_pnl_pct_initial']:+.2f}%",
            f"{a['compound_return_pct']:+.2f}%",
            f"{b['compound_return_pct']:+.2f}%",
            f"{a['avg_exposure_pct']:.1f}%",
            f"{b['avg_exposure_pct']:.1f}%",
            f"{a['spx_compound_return_pct']:+.2f}%",
        ])

    trade_rows = []
    for regime in REGIME_ORDER:
        a = result["trade_review"][E1_ID]["by_dominant_regime"][regime]
        b = result["trade_review"][E1R_ID]["by_dominant_regime"][regime]
        trade_rows.append([
            regime,
            a["trades"], f"{a['avg_return_pct']:+.2f}%", f"{a['win_rate_pct']:.1f}%", a["sim_end_trades"],
            b["trades"], f"{b['avg_return_pct']:+.2f}%", f"{b['win_rate_pct']:.1f}%", b["sim_end_trades"],
        ])

    md = f"""# E1-R Regime Attribution Review

Status: **DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE**  
Generated: {result['generated_at']}  
Regime source: `{result['regime_source']}`  
Shared evaluation window: **{result['shared_window_start']} → {result['shared_window_end']}**  
Shared trading days: **{result['shared_days']}**

## Fairness controls

- E1 and E1-R are compared on the **same daily dates**.
- E1 and E1-R use the **same UPTREND / SIDEWAYS / DOWNTREND regime map**.
- This report does not judge E1-R by unrelated Period A / Period B slices.
- Portfolio-level attribution uses daily equity changes; trade-level attribution is supplementary only.

## Portfolio-level attribution by regime

{_md_table([
    'Regime', 'Days', 'E1 PnL/Initial', 'E1-R PnL/Initial', 'Δ E1-R - E1',
    'E1 Compound', 'E1-R Compound', 'E1 Exp', 'E1-R Exp', 'SPX Compound'
], rows)}

## Trade-level supplementary review

{_md_table([
    'Regime', 'E1 Trades', 'E1 AvgRet', 'E1 WR', 'E1 SimEnd',
    'E1-R Trades', 'E1-R AvgRet', 'E1-R WR', 'E1-R SimEnd'
], trade_rows)}

## Entry type counts

E1: `{result['trade_review'][E1_ID]['entry_type_counts']}`  
E1-R: `{result['trade_review'][E1R_ID]['entry_type_counts']}`

## Interpretation guardrail

This report is designed to answer whether E1-R improves performance under the same market-condition segmentation as E1.  
A valid conclusion should be stated by regime, for example: UPTREND improved / SIDEWAYS reduced damage / DOWNTREND stayed defensive.  
Do not use mismatched time slices as the primary comparison basis.
"""
    OUT_MD.write_text(md)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    backtest = _load_json(BACKTEST_PATH)
    regimes = _load_regime_daily(REGIME_PATH)
    variants = _variant_results(backtest)

    missing = [sid for sid in [E1_ID, E1R_ID] if sid not in variants]
    if missing:
        raise KeyError(f"Missing variant(s) in exports/backtest.json: {missing}")

    e1_rows = _daily_records(variants[E1_ID])
    e1r_rows = _daily_records(variants[E1R_ID])
    e1_dates = set(r["date"] for r in e1_rows)
    e1r_dates = set(r["date"] for r in e1r_rows)
    shared_dates = sorted(d for d in (e1_dates & e1r_dates) if d in regimes)
    if len(shared_dates) < 20:
        raise ValueError(f"Too few shared dates with regime labels: {len(shared_dates)}")

    regime_day_counts = Counter(regimes[d] for d in shared_dates)

    strategy_payload = {
        E1_ID: _attribution_for_strategy(E1_ID, variants[E1_ID], shared_dates, regimes),
        E1R_ID: _attribution_for_strategy(E1R_ID, variants[E1R_ID], shared_dates, regimes),
    }
    trade_payload = {
        E1_ID: _trade_review(E1_ID, variants[E1_ID], regimes),
        E1R_ID: _trade_review(E1R_ID, variants[E1R_ID], regimes),
    }

    result = {
        "status": "DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "regime_source": str(REGIME_PATH),
        "backtest_source": str(BACKTEST_PATH),
        "strategy_ids": [E1_ID, E1R_ID],
        "fairness_controls": {
            "same_daily_dates": True,
            "same_regime_map": True,
            "period_slices_not_primary_evaluation": True,
            "shared_date_count": len(shared_dates),
            "e1_daily_record_count": len(e1_rows),
            "e1r_daily_record_count": len(e1r_rows),
            "excluded_e1_only_dates": sorted(e1_dates - set(shared_dates))[:10],
            "excluded_e1r_only_dates": sorted(e1r_dates - set(shared_dates))[:10],
        },
        "shared_window_start": shared_dates[0],
        "shared_window_end": shared_dates[-1],
        "shared_days": len(shared_dates),
        "shared_regime_day_counts": {r: regime_day_counts.get(r, 0) for r in REGIME_ORDER},
        "strategies": strategy_payload,
        "comparison": _make_comparison(strategy_payload[E1_ID], strategy_payload[E1R_ID]),
        "trade_review": trade_payload,
    }

    OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    _write_report(result)

    print("E1-R REGIME ATTRIBUTION REVIEW")
    print("Status:", result["status"])
    print("Shared window:", result["shared_window_start"], "to", result["shared_window_end"])
    print("Shared days:", result["shared_days"])
    print("Regime days:", result["shared_regime_day_counts"])
    print()
    for regime in REGIME_ORDER:
        c = result["comparison"][regime]
        e1 = result["strategies"][E1_ID]["by_regime"][regime]
        e1r = result["strategies"][E1R_ID]["by_regime"][regime]
        print(
            f"{regime}: days={e1['days']} "
            f"E1={e1['pnl_pct_initial']:+.2f}% "
            f"E1R={e1r['pnl_pct_initial']:+.2f}% "
            f"Delta={c['e1r_minus_e1_pnl_pct_initial']:+.2f}% "
            f"Exp(E1/E1R)={e1['avg_exposure_pct']:.1f}%/{e1r['avg_exposure_pct']:.1f}% "
            f"SPX={e1['spx_compound_return_pct']:+.2f}%"
        )
    print()
    print("Output:", OUT_JSON)
    print("Report:", OUT_MD)


if __name__ == "__main__":
    main()
