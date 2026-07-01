#!/usr/bin/env python3
"""
E1-R Phase 3E Confirmed Quality Diagnostic

Diagnostic only. No trading logic changes.

Purpose:
- Stress-test E1-R Confirmed execution quality.
- Distinguish healthy trend-winner dependence from fragile top-winner concentration.
- Keep E1 vs E1-R comparisons under the same available backtest output.

Inputs expected in repo root:
- exports/backtest.json generated after E1-R Phase 3B execution
- data/research/e1r/e1r_regime_attribution_review.json (optional but recommended)
- data/research/e1r/e1r_phase3c_channel_diagnostic.json (optional)
- data/sp500_constituents.json (optional, for sector mapping)

Outputs:
- data/research/e1r/e1r_phase3e_confirmed_quality_diagnostic.json
- data/research/e1r/E1R_PHASE3E_CONFIRMED_QUALITY_DIAGNOSTIC_REPORT.md
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median
from typing import Any, Dict, List, Optional

E1_ID = "E1_AUDITED_G4_MINHOLD10"
E1R_ID = "E1R_REGIME_AWARE_V0_1"
CONFIRMED = "E1R_UPTREND_CONFIRMED"

BACKTEST = Path("exports/backtest.json")
REGIME_REVIEW = Path("data/research/e1r/e1r_regime_attribution_review.json")
PHASE3C = Path("data/research/e1r/e1r_phase3c_channel_diagnostic.json")
CONSTITUENTS = Path("data/sp500_constituents.json")

OUT_DIR = Path("data/research/e1r")
OUT_JSON = OUT_DIR / "e1r_phase3e_confirmed_quality_diagnostic.json"
OUT_MD = OUT_DIR / "E1R_PHASE3E_CONFIRMED_QUALITY_DIAGNOSTIC_REPORT.md"


def _load_json(path: Path, required: bool = True) -> Dict[str, Any]:
    if not path.exists():
        if required:
            raise FileNotFoundError(f"Missing required file: {path}")
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _round(x: Any, nd: int = 2) -> Optional[float]:
    if x is None:
        return None
    try:
        if math.isnan(float(x)):
            return None
        return round(float(x), nd)
    except Exception:
        return None


def _pct(x: Any) -> str:
    v = _round(x, 2)
    return "n/a" if v is None else f"{v:+.2f}%"


def _num(x: Any, default: float = 0.0) -> float:
    try:
        if x is None:
            return default
        v = float(x)
        if math.isnan(v):
            return default
        return v
    except Exception:
        return default


def _is_sim_end(t: Dict[str, Any]) -> bool:
    return bool(t.get("is_sim_end")) or t.get("exit_signal") == "SIM_END" or t.get("exit_type") == "SIM_END"


def _trade_stats(trades: List[Dict[str, Any]]) -> Dict[str, Any]:
    rets = [_num(t.get("return_pct")) for t in trades]
    wins = [r for r in rets if r > 0]
    losses = [r for r in rets if r < 0]
    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))
    pf = gross_profit / gross_loss if gross_loss > 0 else (None if gross_profit == 0 else float("inf"))
    return {
        "trades": len(trades),
        "closed_ex_sim_end": len([t for t in trades if not _is_sim_end(t)]),
        "sim_end_trades": len([t for t in trades if _is_sim_end(t)]),
        "sum_return_pct_points": _round(sum(rets)),
        "avg_return_pct": _round(mean(rets)) if rets else None,
        "median_return_pct": _round(median(rets)) if rets else None,
        "win_rate_pct": _round(len(wins) / len(rets) * 100) if rets else None,
        "profit_factor_by_trade_return": _round(pf) if pf not in (None, float("inf")) else pf,
        "gross_profit_pct_points": _round(gross_profit),
        "gross_loss_pct_points": _round(gross_loss),
        "best_trade_pct": _round(max(rets)) if rets else None,
        "worst_trade_pct": _round(min(rets)) if rets else None,
        "avg_holding_days": _round(mean([_num(t.get("holding_days")) for t in trades])) if trades else None,
        "median_holding_days": _round(median([_num(t.get("holding_days")) for t in trades])) if trades else None,
    }


def _exclude_top_winners(trades: List[Dict[str, Any]], n: int, include_sim_end: bool = True) -> List[Dict[str, Any]]:
    pool = list(trades) if include_sim_end else [t for t in trades if not _is_sim_end(t)]
    top = sorted(pool, key=lambda t: _num(t.get("return_pct")), reverse=True)[:n]
    top_ids = {(t.get("symbol"), t.get("entry_date"), t.get("exit_date"), t.get("return_pct")) for t in top}
    return [t for t in pool if (t.get("symbol"), t.get("entry_date"), t.get("exit_date"), t.get("return_pct")) not in top_ids]


def _top_trades(trades: List[Dict[str, Any]], n: int = 10, reverse: bool = True) -> List[Dict[str, Any]]:
    out = []
    for t in sorted(trades, key=lambda x: _num(x.get("return_pct")), reverse=reverse)[:n]:
        out.append({
            "symbol": t.get("symbol"),
            "entry_date": t.get("entry_date"),
            "exit_date": t.get("exit_date"),
            "return_pct": _round(t.get("return_pct")),
            "holding_days": t.get("holding_days"),
            "is_sim_end": _is_sim_end(t),
            "entry_regime": t.get("entry_regime"),
            "dominant_regime": t.get("dominant_regime"),
            "max_gain_pct": _round(t.get("max_gain_pct")),
            "max_drawdown_in_trade": _round(t.get("max_drawdown_in_trade")),
            "leader_score_entry": _round(t.get("leader_score_entry"), 1),
            "entry_type": t.get("entry_type"),
        })
    return out


def _concentration(trades: List[Dict[str, Any]]) -> Dict[str, Any]:
    rets = [_num(t.get("return_pct")) for t in trades]
    wins_sorted = sorted([r for r in rets if r > 0], reverse=True)
    net_sum = sum(rets)
    gross_profit = sum(wins_sorted)
    def share_top(k: int, denom: float) -> Optional[float]:
        if denom == 0:
            return None
        return round(sum(wins_sorted[:k]) / denom * 100, 2)
    return {
        "positive_trade_count": len(wins_sorted),
        "negative_trade_count": len([r for r in rets if r < 0]),
        "top1_share_of_gross_profit_pct": share_top(1, gross_profit),
        "top2_share_of_gross_profit_pct": share_top(2, gross_profit),
        "top3_share_of_gross_profit_pct": share_top(3, gross_profit),
        "top1_share_of_net_sum_pct": share_top(1, net_sum),
        "top2_share_of_net_sum_pct": share_top(2, net_sum),
        "top3_share_of_net_sum_pct": share_top(3, net_sum),
    }


def _symbol_sector_map() -> Dict[str, str]:
    if not CONSTITUENTS.exists():
        return {}
    try:
        obj = json.loads(CONSTITUENTS.read_text(encoding="utf-8"))
    except Exception:
        return {}
    rows = obj if isinstance(obj, list) else obj.get("constituents", []) if isinstance(obj, dict) else []
    m = {}
    for r in rows:
        if not isinstance(r, dict):
            continue
        sym = r.get("symbol") or r.get("ticker") or r.get("Symbol")
        sec = r.get("sector") or r.get("GICS Sector") or r.get("gics_sector") or r.get("Sector")
        if sym and sec:
            m[str(sym)] = str(sec)
    return m


def _counts_by(trades: List[Dict[str, Any]], key_fn) -> Dict[str, int]:
    c = Counter()
    for t in trades:
        k = key_fn(t)
        c[str(k or "UNKNOWN")] += 1
    return dict(c.most_common())


def _month(s: Any) -> str:
    if not s:
        return "UNKNOWN"
    return str(s)[:7]


def _make_stress(trades: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "all_trades": _trade_stats(trades),
        "closed_only_ex_sim_end": _trade_stats([t for t in trades if not _is_sim_end(t)]),
        "sim_end_only": _trade_stats([t for t in trades if _is_sim_end(t)]),
        "exclude_top1_all": _trade_stats(_exclude_top_winners(trades, 1, True)),
        "exclude_top2_all": _trade_stats(_exclude_top_winners(trades, 2, True)),
        "exclude_top3_all": _trade_stats(_exclude_top_winners(trades, 3, True)),
        "exclude_top1_closed_only": _trade_stats(_exclude_top_winners(trades, 1, False)),
        "exclude_top2_closed_only": _trade_stats(_exclude_top_winners(trades, 2, False)),
        "exclude_top3_closed_only": _trade_stats(_exclude_top_winners(trades, 3, False)),
    }


def _grade(e1_stats: Dict[str, Any], e1r_stress: Dict[str, Any]) -> Dict[str, Any]:
    e1_pf = _num(e1_stats.get("all_trades", {}).get("profit_factor_by_trade_return"), 0)
    ex1 = e1r_stress.get("exclude_top1_all", {})
    ex2 = e1r_stress.get("exclude_top2_all", {})
    exsim = e1r_stress.get("closed_only_ex_sim_end", {})

    ex1_pf = _num(ex1.get("profit_factor_by_trade_return"), 0)
    ex2_pf = _num(ex2.get("profit_factor_by_trade_return"), 0)
    exsim_pf = _num(exsim.get("profit_factor_by_trade_return"), 0)
    ex1_sum = _num(ex1.get("sum_return_pct_points"), 0)
    ex2_sum = _num(ex2.get("sum_return_pct_points"), 0)
    exsim_sum = _num(exsim.get("sum_return_pct_points"), 0)

    if ex2_pf >= max(e1_pf, 1.0) and ex2_sum > 0 and exsim_pf >= max(e1_pf, 1.0) and exsim_sum > 0:
        g = "A"
        msg = "Top-winner dependence appears healthy under trade-level stress tests."
    elif ex1_pf >= max(e1_pf, 1.0) and ex1_sum > 0 and ex2_pf >= 1.0 and exsim_sum > 0:
        g = "B"
        msg = "Confirmed channel remains acceptable after removing major winners, but top winners matter."
    elif ex1_sum > 0 and ex1_pf >= 1.0:
        g = "C"
        msg = "Confirmed channel keeps a positive trade-level base after removing Top1, but concentration is meaningful."
    else:
        g = "D"
        msg = "Confirmed channel is highly concentrated; do not promote without more review."
    return {
        "heuristic_grade": g,
        "interpretation": msg,
        "threshold_notes": "Heuristic uses trade-return stress tests, not a recomputed portfolio equity curve.",
        "e1_trade_return_pf_reference": _round(e1_pf),
        "e1r_ex_top1_pf": _round(ex1_pf),
        "e1r_ex_top2_pf": _round(ex2_pf),
        "e1r_ex_sim_end_pf": _round(exsim_pf),
    }


def main() -> None:
    bj = _load_json(BACKTEST, required=True)
    try:
        variants = bj["backtest"]["results"]["layer_d"]["variant_results"]
    except Exception as exc:
        raise KeyError("Could not locate layer_d.variant_results in exports/backtest.json") from exc

    if E1_ID not in variants or E1R_ID not in variants:
        found = list(variants.keys())
        raise SystemExit(
            "Missing required E1/E1-R variants in exports/backtest.json.\n"
            f"Found: {found}\n"
            "Run `python3 run_backtest.py` first, then rerun this diagnostic."
        )

    e1 = variants[E1_ID]
    e1r = variants[E1R_ID]
    e1_trades = e1.get("trades", []) or []
    e1r_trades_all = e1r.get("trades", []) or []
    confirmed = [t for t in e1r_trades_all if t.get("entry_type") == CONFIRMED]

    sector_map = _symbol_sector_map()
    regime_review = _load_json(REGIME_REVIEW, required=False)
    phase3c = _load_json(PHASE3C, required=False)

    e1_stress = _make_stress(e1_trades)
    e1r_stress = _make_stress(confirmed)

    result = {
        "status": "DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "backtest_source": str(BACKTEST),
            "regime_review_source": str(REGIME_REVIEW) if REGIME_REVIEW.exists() else None,
            "phase3c_source": str(PHASE3C) if PHASE3C.exists() else None,
            "constituents_source": str(CONSTITUENTS) if CONSTITUENTS.exists() else None,
        },
        "fairness_controls": {
            "same_backtest_export": True,
            "e1_benchmark_unchanged": True,
            "diagnostic_only_no_trading_logic_change": True,
            "portfolio_adjusted_return_not_recomputed": True,
            "stress_tests_are_trade_return_based": True,
        },
        "portfolio_summary": {
            E1_ID: {k: e1.get(k) for k in ["total_return_pct", "max_drawdown_pct", "profit_factor", "sharpe_ratio", "win_rate_pct", "exposure_pct", "number_of_trades", "total_trades_all"]},
            E1R_ID: {k: e1r.get(k) for k in ["total_return_pct", "max_drawdown_pct", "profit_factor", "sharpe_ratio", "win_rate_pct", "exposure_pct", "number_of_trades", "total_trades_all", "research_status"]},
        },
        "confirmed_trade_count": len(confirmed),
        "entry_type_counts": dict(Counter(t.get("entry_type") for t in e1r_trades_all)),
        "top_winners": _top_trades(confirmed, 10, True),
        "worst_losers": _top_trades(confirmed, 10, False),
        "confirmed_trade_stats": e1r_stress,
        "e1_trade_stats_reference": e1_stress,
        "top_winner_concentration": _concentration(confirmed),
        "symbol_concentration": _counts_by(confirmed, lambda t: t.get("symbol")),
        "sector_concentration": _counts_by(confirmed, lambda t: sector_map.get(str(t.get("symbol")), "UNKNOWN")),
        "entry_month_concentration": _counts_by(confirmed, lambda t: _month(t.get("entry_date"))),
        "sim_end_sensitivity": {
            "sim_end_trades": _top_trades([t for t in confirmed if _is_sim_end(t)], 10, True),
            "closed_only_stats": e1r_stress["closed_only_ex_sim_end"],
            "all_trade_stats": e1r_stress["all_trades"],
        },
        "regime_gap_from_review": regime_review.get("comparison", {}) if isinstance(regime_review, dict) else {},
        "phase3c_reference": {
            "candidate_funnel": phase3c.get("candidate_funnel", {}) if isinstance(phase3c, dict) else {},
            "regime_gap_from_review": phase3c.get("regime_gap_from_review", {}) if isinstance(phase3c, dict) else {},
        },
    }
    result["quality_grade"] = _grade(e1_stress, e1r_stress)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    md: List[str] = []
    md.append("# E1-R Phase 3E Confirmed Quality Diagnostic")
    md.append("")
    md.append(f"Status: **{result['status']}**")
    md.append("")
    md.append("## 1. Purpose")
    md.append("")
    md.append("This diagnostic stress-tests whether E1-R Confirmed winners are a healthy trend-following payoff pattern or an overly fragile concentration. It does not change trading logic.")
    md.append("")
    md.append("## 2. Portfolio Baseline")
    md.append("")
    md.append("| Strategy | Return | MaxDD | PF | Sharpe | Win Rate | Exposure | Trades |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for sid in [E1_ID, E1R_ID]:
        ps = result["portfolio_summary"][sid]
        md.append(f"| {sid} | {_pct(ps.get('total_return_pct'))} | {_pct(ps.get('max_drawdown_pct'))} | {ps.get('profit_factor')} | {ps.get('sharpe_ratio')} | {_pct(ps.get('win_rate_pct'))} | {_pct(ps.get('exposure_pct'))} | {ps.get('number_of_trades')} |")
    md.append("")
    md.append("## 3. Confirmed Trade Stress Tests")
    md.append("")
    md.append("These tests remove the largest winning trades from the trade-return distribution. They are not recomputed portfolio equity curves.")
    md.append("")
    md.append("| Case | Trades | SIM_END | Sum Return Pts | Avg | Median | Win Rate | PF by Trade Return | Best | Worst |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for key in ["all_trades", "closed_only_ex_sim_end", "exclude_top1_all", "exclude_top2_all", "exclude_top3_all", "exclude_top1_closed_only", "exclude_top2_closed_only", "exclude_top3_closed_only"]:
        x = e1r_stress[key]
        md.append(f"| {key} | {x['trades']} | {x['sim_end_trades']} | {_pct(x['sum_return_pct_points'])} | {_pct(x['avg_return_pct'])} | {_pct(x['median_return_pct'])} | {_pct(x['win_rate_pct'])} | {x['profit_factor_by_trade_return']} | {_pct(x['best_trade_pct'])} | {_pct(x['worst_trade_pct'])} |")
    md.append("")
    md.append("## 4. Top Winners and Worst Losers")
    md.append("")
    md.append("### Top Winners")
    md.append("")
    md.append("| Symbol | Entry | Exit | Return | Days | SIM_END | Entry Regime | Max Gain | Max DD in Trade |")
    md.append("|---|---|---|---:|---:|---|---|---:|---:|")
    for t in result["top_winners"][:10]:
        md.append(f"| {t['symbol']} | {t['entry_date']} | {t['exit_date']} | {_pct(t['return_pct'])} | {t['holding_days']} | {t['is_sim_end']} | {t['entry_regime']} | {_pct(t['max_gain_pct'])} | {_pct(t['max_drawdown_in_trade'])} |")
    md.append("")
    md.append("### Worst Losers")
    md.append("")
    md.append("| Symbol | Entry | Exit | Return | Days | SIM_END | Entry Regime | Max Gain | Max DD in Trade |")
    md.append("|---|---|---|---:|---:|---|---|---:|---:|")
    for t in result["worst_losers"][:10]:
        md.append(f"| {t['symbol']} | {t['entry_date']} | {t['exit_date']} | {_pct(t['return_pct'])} | {t['holding_days']} | {t['is_sim_end']} | {t['entry_regime']} | {_pct(t['max_gain_pct'])} | {_pct(t['max_drawdown_in_trade'])} |")
    md.append("")
    md.append("## 5. Concentration")
    md.append("")
    c = result["top_winner_concentration"]
    md.append(f"Top1 share of gross profit: **{_pct(c.get('top1_share_of_gross_profit_pct'))}**")
    md.append(f"Top2 share of gross profit: **{_pct(c.get('top2_share_of_gross_profit_pct'))}**")
    md.append(f"Top3 share of gross profit: **{_pct(c.get('top3_share_of_gross_profit_pct'))}**")
    md.append("")
    md.append(f"Symbol concentration: `{result['symbol_concentration']}`")
    md.append("")
    md.append(f"Sector concentration: `{result['sector_concentration']}`")
    md.append("")
    md.append(f"Entry-month concentration: `{result['entry_month_concentration']}`")
    md.append("")
    md.append("## 6. Regime Delta Reference")
    md.append("")
    md.append("| Regime | Days | E1R-E1 PnL | Compound | Exposure Delta | MaxDD Delta |")
    md.append("|---|---:|---:|---:|---:|---:|")
    for regime in ["UPTREND", "SIDEWAYS", "DOWNTREND", "UNCLASSIFIED"]:
        x = result["regime_gap_from_review"].get(regime, {})
        md.append(f"| {regime} | {x.get('days')} | {_pct(x.get('e1r_minus_e1_pnl_pct_initial'))} | {_pct(x.get('e1r_minus_e1_compound_pct'))} | {_pct(x.get('e1r_minus_e1_avg_exposure_pct'))} | {_pct(x.get('e1r_minus_e1_max_dd_within_regime_pct'))} |")
    md.append("")
    md.append("## 7. Frozen Interpretation")
    md.append("")
    q = result["quality_grade"]
    md.append(f"Heuristic grade: **{q['heuristic_grade']}**")
    md.append("")
    md.append(q["interpretation"])
    md.append("")
    md.append("This is a pressure test, not a penalty test. Trend systems are allowed to rely on major winners; the diagnostic checks whether the Confirmed channel still has a reasonable base after removing the largest winners and SIM_END trades.")
    md.append("")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("E1-R PHASE 3E CONFIRMED QUALITY DIAGNOSTIC")
    print("Status: DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE")
    print(f"Confirmed trades: {len(confirmed)}")
    print(f"Portfolio E1:   return={e1.get('total_return_pct')} maxDD={e1.get('max_drawdown_pct')} PF={e1.get('profit_factor')} trades={e1.get('number_of_trades')}")
    print(f"Portfolio E1-R: return={e1r.get('total_return_pct')} maxDD={e1r.get('max_drawdown_pct')} PF={e1r.get('profit_factor')} trades={e1r.get('number_of_trades')}")
    print("")
    print("Confirmed stress tests by trade return:")
    for key in ["all_trades", "closed_only_ex_sim_end", "exclude_top1_all", "exclude_top2_all", "exclude_top3_all"]:
        x = e1r_stress[key]
        print(f"  {key}: trades={x['trades']} sum={_pct(x['sum_return_pct_points'])} avg={_pct(x['avg_return_pct'])} WR={_pct(x['win_rate_pct'])} PF={x['profit_factor_by_trade_return']}")
    print("")
    print("Top winners:")
    for t in result["top_winners"][:5]:
        print(f"  {t['symbol']} {t['entry_date']}->{t['exit_date']} return={_pct(t['return_pct'])} sim_end={t['is_sim_end']}")
    print("")
    print("Concentration:")
    print(f"  top1_gross_profit_share={_pct(c.get('top1_share_of_gross_profit_pct'))}")
    print(f"  top2_gross_profit_share={_pct(c.get('top2_share_of_gross_profit_pct'))}")
    print(f"  top3_gross_profit_share={_pct(c.get('top3_share_of_gross_profit_pct'))}")
    print("")
    print(f"Quality grade: {q['heuristic_grade']} - {q['interpretation']}")
    print(f"Output: {OUT_JSON}")
    print(f"Report: {OUT_MD}")


if __name__ == "__main__":
    main()
