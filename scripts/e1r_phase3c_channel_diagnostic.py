#!/usr/bin/env python3
"""
E1-R Phase 3C Channel Diagnostic

Diagnostic-only script. It does not change trading logic or generated backtest outputs.

Purpose:
1) Decompose E1-R Phase 3B results by channel: Confirmed vs Emerging.
2) Explain why Emerging did not execute in Phase 3B.
3) Summarize SIDEWAYS / DOWNTREND exposure gaps using the existing regime attribution review.

Inputs expected after running `python3 run_backtest.py`:
- exports/backtest.json
- data/research/e1r/e1r_candidate_forward_return_diagnostic.json
- data/research/e1r/e1r_regime_attribution_review.json

Outputs:
- data/research/e1r/e1r_phase3c_channel_diagnostic.json
- data/research/e1r/E1R_PHASE3C_CHANNEL_DIAGNOSTIC_REPORT.md
"""
from __future__ import annotations

import json
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
FWD_PATH = Path("data/research/e1r/e1r_candidate_forward_return_diagnostic.json")
REGIME_REVIEW_PATH = Path("data/research/e1r/e1r_regime_attribution_review.json")
OUT_JSON = Path("data/research/e1r/e1r_phase3c_channel_diagnostic.json")
OUT_MD = Path("data/research/e1r/E1R_PHASE3C_CHANNEL_DIAGNOSTIC_REPORT.md")


def _load_json(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing required input: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _round(x: Any, nd: int = 2) -> Any:
    if isinstance(x, (int, float)):
        return round(float(x), nd)
    return x


def _pct(x: Any) -> str:
    if not isinstance(x, (int, float)):
        return "n/a"
    return f"{x:+.2f}%"


def _candidate_sort_key(c: dict[str, Any]) -> tuple:
    # Mirrors Phase 3B intent: Confirmed first; then better rank / score / acceleration / RS improvement.
    etype = c.get("e1r_entry_type")
    type_priority = 0 if etype == CONFIRMED else 1
    return (
        type_priority,
        int(c.get("leader_rank") or 9999),
        -float(c.get("leader_score") or 0),
        -float(c.get("momentum_acceleration") or 0),
        -float(c.get("rs_20d_improvement") or 0),
        str(c.get("symbol") or ""),
    )


def _trade_return_stats(trades: list[dict[str, Any]]) -> dict[str, Any]:
    rets = [float(t.get("return_pct")) for t in trades if isinstance(t.get("return_pct"), (int, float))]
    wins = [r for r in rets if r > 0]
    losses = [r for r in rets if r < 0]
    sim_end = [t for t in trades if t.get("exit_signal") == "SIM_END" or t.get("sim_end_trade")]
    return {
        "trades": len(trades),
        "closed_trades_ex_sim_end": len(trades) - len(sim_end),
        "sim_end_trades": len(sim_end),
        "avg_return_pct": _round(mean(rets), 2) if rets else 0.0,
        "median_return_pct": _round(median(rets), 2) if rets else 0.0,
        "win_rate_pct": _round(len(wins) / len(rets) * 100, 1) if rets else 0.0,
        "avg_winner_pct": _round(mean(wins), 2) if wins else 0.0,
        "avg_loser_pct": _round(mean(losses), 2) if losses else 0.0,
        "best_trade_pct": _round(max(rets), 2) if rets else 0.0,
        "worst_trade_pct": _round(min(rets), 2) if rets else 0.0,
        "sim_end_symbols": [t.get("symbol") for t in sim_end],
    }


def _safe_variant_results(backtest: dict[str, Any]) -> dict[str, Any]:
    try:
        return backtest["backtest"]["results"]["layer_d"]["variant_results"]
    except KeyError as exc:
        raise KeyError("Cannot locate backtest.results.layer_d.variant_results in exports/backtest.json") from exc


def main() -> None:
    bj = _load_json(BACKTEST_PATH)
    fwd = _load_json(FWD_PATH)
    regime_review = _load_json(REGIME_REVIEW_PATH)
    variants = _safe_variant_results(bj)
    if E1_ID not in variants or E1R_ID not in variants:
        raise KeyError(f"Missing required variants. Found: {list(variants.keys())}")

    e1 = variants[E1_ID]
    e1r = variants[E1R_ID]
    candidates = e1r.get("e1r_candidates", []) or []
    trades = e1r.get("trades", []) or []
    daily_records = e1r.get("daily_equity_records", []) or []
    if not candidates:
        raise RuntimeError("No E1-R candidates found in exports/backtest.json. Run `python3 run_backtest.py` first.")

    candidate_type_counts = Counter(c.get("e1r_entry_type") for c in candidates)
    candidates_by_date: dict[str, list[dict[str, Any]]] = defaultdict(list)
    candidates_by_symbol: Counter[str] = Counter()
    for c in candidates:
        d = c.get("date")
        if d:
            candidates_by_date[d].append(c)
        if c.get("symbol"):
            candidates_by_symbol[c.get("symbol")] += 1

    daily_top1 = []
    daily_mix_counts = Counter()
    top1_type_counts = Counter()
    days_with_confirmed = 0
    days_with_emerging = 0
    days_with_both = 0
    for d, cs in sorted(candidates_by_date.items()):
        types = {c.get("e1r_entry_type") for c in cs}
        if CONFIRMED in types:
            days_with_confirmed += 1
        if EMERGING in types:
            days_with_emerging += 1
        if CONFIRMED in types and EMERGING in types:
            days_with_both += 1
            daily_mix_counts["both"] += 1
        elif CONFIRMED in types:
            daily_mix_counts["confirmed_only"] += 1
        elif EMERGING in types:
            daily_mix_counts["emerging_only"] += 1
        else:
            daily_mix_counts["other"] += 1

        sorted_cs = sorted(cs, key=_candidate_sort_key)
        top = sorted_cs[0]
        top1_type_counts[top.get("e1r_entry_type")] += 1
        daily_top1.append({
            "date": d,
            "symbol": top.get("symbol"),
            "entry_type": top.get("e1r_entry_type"),
            "leader_rank": top.get("leader_rank"),
            "leader_score": top.get("leader_score"),
            "candidate_count": len(cs),
            "confirmed_count": sum(1 for c in cs if c.get("e1r_entry_type") == CONFIRMED),
            "emerging_count": sum(1 for c in cs if c.get("e1r_entry_type") == EMERGING),
        })

    # Approximate execution matching: trade entry_date is T+1 execution; candidate date is usually previous trading day.
    trading_dates = [r.get("date") for r in daily_records if r.get("date")]
    prev_date = {trading_dates[i]: trading_dates[i - 1] for i in range(1, len(trading_dates))}
    candidate_lookup = {(c.get("date"), c.get("symbol")): c for c in candidates}
    executed_matches = []
    unmatched_trades = []
    for t in trades:
        ed = t.get("entry_date")
        sym = t.get("symbol")
        sd = prev_date.get(ed)
        cand = candidate_lookup.get((sd, sym)) if sd else None
        if cand:
            executed_matches.append({
                "symbol": sym,
                "signal_date": sd,
                "entry_date": ed,
                "entry_type": t.get("entry_type") or cand.get("e1r_entry_type"),
                "return_pct": t.get("return_pct"),
                "exit_date": t.get("exit_date"),
                "exit_signal": t.get("exit_signal"),
                "leader_rank": cand.get("leader_rank"),
                "leader_score": cand.get("leader_score"),
            })
        else:
            unmatched_trades.append({
                "symbol": sym,
                "entry_date": ed,
                "entry_type": t.get("entry_type"),
                "return_pct": t.get("return_pct"),
            })

    executed_type_counts = Counter(x.get("entry_type") for x in executed_matches)
    trade_type_counts = Counter(t.get("entry_type") for t in trades)
    executed_by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for t in trades:
        executed_by_type[t.get("entry_type")].append(t)

    # Is Emerging being crowded out by Confirmed priority?
    emerging_top1_days = top1_type_counts.get(EMERGING, 0)
    emerging_candidate_days = days_with_emerging
    emerging_exec = trade_type_counts.get(EMERGING, 0)
    if emerging_exec > 0:
        emerging_non_execution_diagnosis = "EMERGING_EXECUTED_IN_PHASE3B"
    elif emerging_top1_days == 0 and emerging_candidate_days > 0:
        emerging_non_execution_diagnosis = "CROWDED_OUT_BY_CONFIRMED_PRIORITY_AND_DAILY_BUY_CAP"
    elif emerging_top1_days > 0:
        emerging_non_execution_diagnosis = "EMERGING_TOP1_EXISTED_BUT_NOT_EXECUTED_CHECK_CAPACITY_GATE_OR_EXISTING_HOLDINGS"
    else:
        emerging_non_execution_diagnosis = "NO_EMERGING_CANDIDATE_DAYS"

    # SIDEWAYS / DOWNTREND gap from previous fair-regime review.
    comp = regime_review.get("comparison", {})
    regime_gap = {}
    for regime in ["UPTREND", "SIDEWAYS", "DOWNTREND", "UNCLASSIFIED"]:
        x = comp.get(regime, {})
        regime_gap[regime] = {
            "days": x.get("days", x.get("regime_days")),
            "e1_return_pct": x.get("E1_AUDITED_G4_MINHOLD10", {}).get("total_return_pct", x.get("e1_return_pct")),
            "e1r_return_pct": x.get("E1R_REGIME_AWARE_V0_1", {}).get("total_return_pct", x.get("e1r_return_pct")),
            "delta_e1r_minus_e1_pct": x.get("delta_e1r_minus_e1_pct"),
            "spx_return_pct": x.get("spx_return_pct"),
            "e1_exposure_pct": x.get("E1_AUDITED_G4_MINHOLD10", {}).get("avg_exposure_pct", x.get("e1_exposure_pct")),
            "e1r_exposure_pct": x.get("E1R_REGIME_AWARE_V0_1", {}).get("avg_exposure_pct", x.get("e1r_exposure_pct")),
        }

    # Candidate forward-return alpha summary from existing diagnostic.
    fwd_summary = fwd.get("dedup_summary", {})
    channel_forward_alpha = {}
    for typ in [CONFIRMED, EMERGING, "ALL"]:
        node = fwd_summary.get(typ, {})
        channel_forward_alpha[typ] = {
            "candidate_count": node.get("candidate_count"),
            "20d_avg_return_pct": node.get("forward_returns", {}).get("20d", {}).get("avg_return_pct"),
            "20d_avg_excess_pct": node.get("forward_returns", {}).get("20d", {}).get("avg_excess_pct"),
            "30d_avg_return_pct": node.get("forward_returns", {}).get("30d", {}).get("avg_return_pct"),
            "30d_avg_excess_pct": node.get("forward_returns", {}).get("30d", {}).get("avg_excess_pct"),
            "30d_excess_win_rate_pct": node.get("forward_returns", {}).get("30d", {}).get("excess_win_rate_pct"),
            "lead_time_vs_first_e1_entry": node.get("lead_time_vs_first_e1_entry"),
        }

    result = {
        "status": "DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "inputs": {
            "backtest": str(BACKTEST_PATH),
            "candidate_forward_return_diagnostic": str(FWD_PATH),
            "regime_attribution_review": str(REGIME_REVIEW_PATH),
        },
        "fairness_controls": {
            "e1_vs_e1r_comparison_basis": "same_daily_dates_and_same_spx_regime_map",
            "period_a_b_not_primary_evaluation": True,
            "this_script_changes_trading_logic": False,
        },
        "portfolio_summary": {
            E1_ID: {
                "total_return_pct": e1.get("total_return_pct"),
                "max_drawdown_pct": e1.get("max_drawdown_pct"),
                "profit_factor": e1.get("profit_factor"),
                "sharpe_ratio": e1.get("sharpe_ratio"),
                "exposure_pct": e1.get("exposure_pct"),
                "number_of_trades": e1.get("number_of_trades"),
            },
            E1R_ID: {
                "total_return_pct": e1r.get("total_return_pct"),
                "max_drawdown_pct": e1r.get("max_drawdown_pct"),
                "profit_factor": e1r.get("profit_factor"),
                "sharpe_ratio": e1r.get("sharpe_ratio"),
                "exposure_pct": e1r.get("exposure_pct"),
                "number_of_trades": e1r.get("number_of_trades"),
                "research_status": e1r.get("research_status"),
            },
        },
        "candidate_funnel": {
            "raw_candidate_count": len(candidates),
            "candidate_type_counts": dict(candidate_type_counts),
            "candidate_days": len(candidates_by_date),
            "days_with_confirmed": days_with_confirmed,
            "days_with_emerging": days_with_emerging,
            "days_with_both": days_with_both,
            "daily_mix_counts": dict(daily_mix_counts),
            "top1_type_counts_under_phase3b_priority": dict(top1_type_counts),
            "executed_trade_type_counts": dict(trade_type_counts),
            "executed_candidate_match_type_counts": dict(executed_type_counts),
            "emerging_non_execution_diagnosis": emerging_non_execution_diagnosis,
            "top_candidate_symbol_counts": candidates_by_symbol.most_common(20),
            "sample_daily_top1": daily_top1[:20],
            "unmatched_trade_count": len(unmatched_trades),
            "sample_unmatched_trades": unmatched_trades[:20],
        },
        "channel_trade_stats": {
            str(k): _trade_return_stats(v) for k, v in executed_by_type.items()
        },
        "channel_forward_alpha_from_diagnostic": channel_forward_alpha,
        "regime_gap_from_review": regime_gap,
        "interpretation": {
            "phase3b_actual_tested_channel": (
                "CONFIRMED_ONLY" if trade_type_counts.get(CONFIRMED, 0) > 0 and trade_type_counts.get(EMERGING, 0) == 0 else "MIXED_OR_OTHER"
            ),
            "confirmed_channel_status": "EXECUTED_AND_PORTFOLIO_VALIDATED_IN_UPTREND",
            "emerging_channel_status": "HAS_FORWARD_RETURN_ALPHA_BUT_NOT_EXECUTED_IN_PHASE3B" if emerging_exec == 0 else "EXECUTED",
            "sideways_status": "NOT_IMPLEMENTED_OR_NEAR_ZERO_EXPOSURE_IN_PHASE3B",
            "downtrend_status": "NO_SAMPLE_IN_CURRENT_SHARED_WINDOW" if (regime_gap.get("DOWNTREND", {}).get("days") or 0) == 0 else "OBSERVE_ONLY",
            "recommended_next_research_step": "Design separate non-trading diagnostics for Emerging-only capacity and SIDEWAYS low-exposure rules before changing execution logic.",
        },
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    cf = result["candidate_funnel"]
    ps = result["portfolio_summary"]
    # Use the fair regime attribution review's canonical comparison schema.
    # This keeps E1 vs E1-R comparison on the same regime segmentation.
    _canonical_regime_gap = regime_review.get("comparison", {})
    if _canonical_regime_gap:
        result["regime_gap_from_review"] = _canonical_regime_gap

    reg = result["regime_gap_from_review"]
    ch = result["channel_trade_stats"]
    fa = result["channel_forward_alpha_from_diagnostic"]

    md = []
    md.append("# E1-R Phase 3C Channel Diagnostic Report")
    md.append("")
    md.append(f"Generated at: {result['generated_at']}")
    md.append("")
    md.append("Status: **DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE**")
    md.append("")
    md.append("## 1. Fairness Controls")
    md.append("")
    md.append("E1 and E1-R must be compared under the same daily dates and the same SPX regime map. Period A/B is not the primary evaluation dimension for E1-R.")
    md.append("")
    md.append("## 2. Portfolio Summary")
    md.append("")
    md.append("| Strategy | Return | MaxDD | PF | Sharpe | Exposure | Trades |")
    md.append("|---|---:|---:|---:|---:|---:|---:|")
    for sid in [E1_ID, E1R_ID]:
        x = ps[sid]
        md.append(f"| {sid} | {_pct(x.get('total_return_pct'))} | {x.get('max_drawdown_pct')}% | {x.get('profit_factor')} | {x.get('sharpe_ratio')} | {x.get('exposure_pct')}% | {x.get('number_of_trades')} |")
    md.append("")
    md.append("## 3. Candidate Funnel")
    md.append("")
    md.append(f"Raw E1-R candidates: **{cf['raw_candidate_count']}** across **{cf['candidate_days']}** candidate days.")
    md.append("")
    md.append(f"Candidate type counts: `{cf['candidate_type_counts']}`")
    md.append("")
    md.append(f"Daily mix counts: `{cf['daily_mix_counts']}`")
    md.append("")
    md.append(f"Top-1 type counts under Phase 3B priority: `{cf['top1_type_counts_under_phase3b_priority']}`")
    md.append("")
    md.append(f"Executed trade type counts: `{cf['executed_trade_type_counts']}`")
    md.append("")
    md.append(f"Emerging non-execution diagnosis: **{cf['emerging_non_execution_diagnosis']}**")
    md.append("")
    md.append("## 4. Channel Trade Stats")
    md.append("")
    md.append("| Channel | Trades | Closed ex SIM_END | SIM_END | Avg Return | Median | Win Rate | Best | Worst |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for typ, x in ch.items():
        md.append(f"| {typ} | {x['trades']} | {x['closed_trades_ex_sim_end']} | {x['sim_end_trades']} | {_pct(x['avg_return_pct'])} | {_pct(x['median_return_pct'])} | {x['win_rate_pct']}% | {_pct(x['best_trade_pct'])} | {_pct(x['worst_trade_pct'])} |")
    md.append("")
    md.append("## 5. Forward Alpha From Prior Diagnostic")
    md.append("")
    md.append("| Channel | Candidates | 20D Avg | 20D Excess | 30D Avg | 30D Excess | 30D Excess WR |")
    md.append("|---|---:|---:|---:|---:|---:|---:|")
    for typ in [CONFIRMED, EMERGING, "ALL"]:
        x = fa.get(typ, {})
        md.append(f"| {typ} | {x.get('candidate_count')} | {_pct(x.get('20d_avg_return_pct'))} | {_pct(x.get('20d_avg_excess_pct'))} | {_pct(x.get('30d_avg_return_pct'))} | {_pct(x.get('30d_avg_excess_pct'))} | {x.get('30d_excess_win_rate_pct')}% |")
    md.append("")
    md.append("## 6. Regime Gap From Fair Review")
    md.append("")
    md.append("| Regime | Days | E1R-E1 PnL | E1R-E1 Compound | E1R-E1 Excess vs SPX | Exposure Delta | MaxDD Delta |")
    md.append("|---|---:|---:|---:|---:|---:|---:|")
    for regime in ["UPTREND", "SIDEWAYS", "DOWNTREND", "UNCLASSIFIED"]:
        x = reg.get(regime, {})
        md.append(
            f"| {regime} | {x.get('days')} | "
            f"{_pct(x.get('e1r_minus_e1_pnl_pct_initial'))} | "
            f"{_pct(x.get('e1r_minus_e1_compound_pct'))} | "
            f"{_pct(x.get('e1r_minus_e1_excess_vs_spx_pct'))} | "
            f"{_pct(x.get('e1r_minus_e1_avg_exposure_pct'))} | "
            f"{_pct(x.get('e1r_minus_e1_max_dd_within_regime_pct'))} |"
        )
    md.append("")
    md.append("## 7. Frozen Interpretation")
    md.append("")
    md.append("Phase 3B primarily validated the UPTREND Confirmed execution channel. Emerging has positive forward-return alpha in the prior diagnostic, but it did not execute under Phase 3B priority and capacity rules. SIDEWAYS and DOWNTREND remain unimplemented or untested in portfolio execution.")
    md.append("")
    md.append("Recommended next research step: design separate diagnostics for Emerging-only capacity and SIDEWAYS low-exposure rules before changing live execution logic.")
    md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("E1-R PHASE 3C CHANNEL DIAGNOSTIC")
    print("Status: DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE")
    print(f"Candidates: {cf['raw_candidate_count']} across {cf['candidate_days']} days")
    print(f"Candidate type counts: {cf['candidate_type_counts']}")
    print(f"Top-1 type counts: {cf['top1_type_counts_under_phase3b_priority']}")
    print(f"Executed trade type counts: {cf['executed_trade_type_counts']}")
    print(f"Emerging diagnosis: {cf['emerging_non_execution_diagnosis']}")
    print("\nPortfolio:")
    print(f"  E1:   return={ps[E1_ID].get('total_return_pct')} maxDD={ps[E1_ID].get('max_drawdown_pct')} PF={ps[E1_ID].get('profit_factor')} trades={ps[E1_ID].get('number_of_trades')}")
    print(f"  E1-R: return={ps[E1R_ID].get('total_return_pct')} maxDD={ps[E1R_ID].get('max_drawdown_pct')} PF={ps[E1R_ID].get('profit_factor')} trades={ps[E1R_ID].get('number_of_trades')}")
    print("\nRegime review:")
    for regime in ["UPTREND", "SIDEWAYS", "DOWNTREND"]:
        x = reg.get(regime, {})
        print(
            f"  {regime}: days={x.get('days')} "
            f"E1R-E1 pnl={_pct(x.get('e1r_minus_e1_pnl_pct_initial'))} "
            f"compound={_pct(x.get('e1r_minus_e1_compound_pct'))} "
            f"exposure_delta={_pct(x.get('e1r_minus_e1_avg_exposure_pct'))} "
            f"maxDD_delta={_pct(x.get('e1r_minus_e1_max_dd_within_regime_pct'))}"
        )
    print(f"\nOutput: {OUT_JSON}")
    print(f"Report: {OUT_MD}")


if __name__ == "__main__":
    main()
