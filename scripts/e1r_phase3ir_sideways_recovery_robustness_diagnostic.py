#!/usr/bin/env python3
"""
E1-R Phase 3I-R SIDEWAYS_RECOVERY Robustness / Overfit Defense Diagnostic

Diagnostic only. Does not modify trading logic, orders, exports/backtest.json,
or any strategy implementation.

Purpose:
Stress-test the Phase 3I finding:
    UPGRADE_WATCH_RECOVERY

Main question:
    Is the positive 20D/30D excess from Phase 3I robust enough to remain a
    promising hypothesis, or is it likely an overfit result from a small sample?

Expected run order:
    python3 run_backtest.py        # only if exports/backtest.json lacks E1-R
    python3 scripts/e1r_phase3i_sideways_quality_decomposition_diagnostic.py
    python3 scripts/e1r_phase3ir_sideways_recovery_robustness_diagnostic.py
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
OUT_DIR = ROOT / "data" / "research" / "e1r"
OUT_JSON = OUT_DIR / "e1r_phase3ir_sideways_recovery_robustness_diagnostic.json"
OUT_MD = OUT_DIR / "E1R_PHASE3IR_SIDEWAYS_RECOVERY_ROBUSTNESS_REPORT.md"

PHASE3I_SCRIPT = SCRIPTS_DIR / "e1r_phase3i_sideways_quality_decomposition_diagnostic.py"
BACKTEST_PATH = ROOT / "exports" / "backtest.json"
E1_ID = "E1_AUDITED_G4_MINHOLD10"
E1R_ID = "E1R_REGIME_AWARE_V0_1"
TARGET_RULE = "UPGRADE_WATCH_RECOVERY"
DEDUP_GAP_DAYS = 5


def load_module(path: Path, name: str):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[attr-defined]
    return mod


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def num(x: Any, default: float = 0.0) -> float:
    try:
        if x is None:
            return default
        return float(x)
    except Exception:
        return default


def round_or_none(x: Any, nd: int = 3) -> Any:
    if x is None:
        return None
    try:
        return round(float(x), nd)
    except Exception:
        return None


def pct_str(x: Any) -> str:
    if x is None:
        return "n/a"
    try:
        return f"{float(x):+.2f}%"
    except Exception:
        return "n/a"


def date_year_half(d: str) -> str:
    y = d[:4]
    m = int(d[5:7])
    return f"{y}H1" if m <= 6 else f"{y}H2"


def date_month(d: str) -> str:
    return d[:7]


def safe_variants(backtest: dict[str, Any]) -> dict[str, Any]:
    """
    Resolve variant results from both legacy flat exports and current nested
    exports/backtest.json structure.

    Current structure:
        backtest.results.layer_d.variant_results
    """
    candidate_paths = [
        ("variant_results",),
        ("variants",),
        ("results",),
        ("backtest", "results", "layer_d", "variant_results"),
        ("backtest", "results", "layer_d", "variants"),
    ]

    for path in candidate_paths:
        obj = backtest
        ok = True
        for key in path:
            if isinstance(obj, dict) and isinstance(obj.get(key), dict):
                obj = obj[key]
            else:
                ok = False
                break
        if ok and isinstance(obj, dict):
            return obj

    return {}


def build_phase3i_quality_rows() -> tuple[Any, Any, Any, list[dict[str, Any]], dict[str, Any]]:
    """Rebuild the Phase 3I candidate universe using Phase 3I/3G/3H code."""
    if not PHASE3I_SCRIPT.exists():
        raise SystemExit(f"Missing {PHASE3I_SCRIPT}. Run/copy Phase 3I script first.")

    phase3i = load_module(PHASE3I_SCRIPT, "phase3i")
    phase3g = phase3i.load_module(phase3i.PHASE3G_SCRIPT, "phase3g_for_3ir")
    phase3h = phase3i.load_module(phase3i.PHASE3H_SCRIPT, "phase3h_for_3ir")

    bj = load_json(BACKTEST_PATH)
    variants = safe_variants(bj)
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
    by_rule, _stc_diag = phase3g.screen_stc_candidates(builder, spx_dates, regime_daily)

    base_rows: list[dict[str, Any]] = []
    for rule in phase3i.TARGET_BASE_RULES:
        for r in by_rule.get(rule, []):
            rr = dict(r)
            rr["base_stc_rule"] = rule
            base_rows.append(rr)

    base_symbols = sorted({r.get("symbol") for r in base_rows if r.get("symbol")})
    records_map = phase3h.load_all_records(base_symbols)
    flow_rows = phase3h.attach_flow(base_rows, records_map, spx_rec)
    flow_rows = [r for r in flow_rows if r.get("has_volume_data")]

    sector_map = phase3i.load_sector_map()
    quality_rows = phase3i.add_quality_fields(flow_rows, phase3h, records_map, sector_map, price_map, spx_dates, spx_closes)
    for r in quality_rows:
        r["strength_type"] = phase3i.assign_strength_type(r)
    quality_rows = phase3i.attach_upgrade_stats(quality_rows, phase3i.load_upgrade_events(), spx_dates)

    context = {
        "base_stc_candidates": len(base_rows),
        "candidates_with_volume_data": len(flow_rows),
        "quality_rows": len(quality_rows),
        "sector_map_symbols": len(sector_map),
        "subregime_counts": dict(Counter(str(r.get("sideways_subregime")) for r in quality_rows)),
        "strength_type_counts": dict(Counter(str(r.get("strength_type")) for r in quality_rows)),
    }
    return phase3i, phase3g, phase3h, quality_rows, {"spx_dates": spx_dates, "spx_closes": spx_closes, "price_map": price_map, **context}


def enrich_dedup_top1(rows: list[dict[str, Any]], phase3i, phase3g, ctx: dict[str, Any]) -> list[dict[str, Any]]:
    daily_top1 = phase3i.top1_by_date_stc(rows)
    enriched = phase3g.enrich_forward(daily_top1, ctx["price_map"], ctx["spx_dates"], ctx["spx_closes"])
    return phase3g.dedup_by_symbol_gap(enriched, ctx["spx_dates"], DEDUP_GAP_DAYS)


def forward_summary(rows: list[dict[str, Any]], phase3g) -> dict[str, Any]:
    return phase3g.summarize_forward(rows)


def compact_metrics(rows: list[dict[str, Any]], phase3g) -> dict[str, Any]:
    fs = forward_summary(rows, phase3g)
    upgrades = [r.get("upgraded_to_uptrend_confirmed_30d") for r in rows if r.get("upgraded_to_uptrend_confirmed_30d") is not None]
    fail20_vals = [num(r.get("fwd_20d_pct"), 0.0) for r in rows if r.get("fwd_20d_pct") is not None]
    symbols = Counter(str(r.get("symbol")) for r in rows)
    return {
        "n": len(rows),
        "unique_symbols": len(symbols),
        "top_symbols": symbols.most_common(10),
        "20d_avg_return_pct": round_or_none(fs.get("20d", {}).get("avg_return_pct"), 3),
        "20d_avg_excess_pct": round_or_none(fs.get("20d", {}).get("avg_excess_pct"), 3),
        "20d_excess_win_rate_pct": round_or_none(fs.get("20d", {}).get("excess_win_rate_pct"), 2),
        "30d_avg_return_pct": round_or_none(fs.get("30d", {}).get("avg_return_pct"), 3),
        "30d_avg_excess_pct": round_or_none(fs.get("30d", {}).get("avg_excess_pct"), 3),
        "30d_excess_win_rate_pct": round_or_none(fs.get("30d", {}).get("excess_win_rate_pct"), 2),
        "upgrade30_rate_pct": round_or_none(sum(1 for x in upgrades if x) / len(upgrades) * 100.0, 2) if upgrades else None,
        "fail20_rate_pct": round_or_none(sum(1 for x in fail20_vals if x < 0) / len(fail20_vals) * 100.0, 2) if fail20_vals else None,
    }


def split_diagnostics(target_rows: list[dict[str, Any]], phase3i, phase3g, ctx: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for splitter_name, splitter in [
        ("by_year_half", lambda r: date_year_half(str(r.get("date")))),
        ("by_month", lambda r: date_month(str(r.get("date")))),
    ]:
        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for r in target_rows:
            groups[splitter(r)].append(r)
        res = {}
        for k in sorted(groups):
            dd = enrich_dedup_top1(groups[k], phase3i, phase3g, ctx)
            res[k] = compact_metrics(dd, phase3g)
        out[splitter_name] = res
    return out


def leave_one_symbol_out(dedup_rows: list[dict[str, Any]], phase3g) -> dict[str, Any]:
    symbols = sorted({str(r.get("symbol")) for r in dedup_rows})
    rows = []
    for sym in symbols:
        rem = [r for r in dedup_rows if str(r.get("symbol")) != sym]
        m = compact_metrics(rem, phase3g)
        rows.append({"removed_symbol": sym, **m})
    worst20 = sorted(rows, key=lambda x: num(x.get("20d_avg_excess_pct"), 9999))[:5]
    worst30 = sorted(rows, key=lambda x: num(x.get("30d_avg_excess_pct"), 9999))[:5]
    return {
        "tested_symbols": len(symbols),
        "min_20d_excess_pct": round_or_none(min((num(r.get("20d_avg_excess_pct")) for r in rows), default=None), 3) if rows else None,
        "min_30d_excess_pct": round_or_none(min((num(r.get("30d_avg_excess_pct")) for r in rows), default=None), 3) if rows else None,
        "worst_after_removal_by_20d": worst20,
        "worst_after_removal_by_30d": worst30,
    }


def remove_top_winners(dedup_rows: list[dict[str, Any]], phase3g) -> dict[str, Any]:
    out = {}
    for key in ["excess_20d_pct", "excess_30d_pct", "fwd_30d_pct"]:
        sorted_rows = sorted(dedup_rows, key=lambda r: num(r.get(key), -9999), reverse=True)
        for k in [1, 2, 3]:
            rem = sorted_rows[k:]
            out[f"remove_top{k}_by_{key}"] = compact_metrics(rem, phase3g)
    return out


def leave_one_month_out(dedup_rows: list[dict[str, Any]], phase3g) -> dict[str, Any]:
    months = sorted({date_month(str(r.get("date"))) for r in dedup_rows})
    rows = []
    for m in months:
        rem = [r for r in dedup_rows if date_month(str(r.get("date"))) != m]
        rows.append({"removed_month": m, **compact_metrics(rem, phase3g)})
    return {
        "tested_months": len(months),
        "worst_by_30d_excess": sorted(rows, key=lambda x: num(x.get("30d_avg_excess_pct"), 9999))[:10],
        "all": rows,
    }


def simple_rule_comparison(quality_rows: list[dict[str, Any]], phase3i, phase3g, ctx: dict[str, Any]) -> dict[str, Any]:
    def common(r):
        return not r.get("proxy_or_index_symbol")
    rules = {
        "BASE_STC_COMMON_EQUITY": lambda r: common(r),
        "SIDEWAYS_RECOVERY_COMMON_EQUITY": lambda r: common(r) and r.get("sideways_subregime") == "SIDEWAYS_RECOVERY",
        "SIDEWAYS_RECOVERY_STC90": lambda r: common(r) and r.get("sideways_subregime") == "SIDEWAYS_RECOVERY" and num(r.get("stc_score")) >= 90,
        "SIDEWAYS_RECOVERY_FLOW70": lambda r: common(r) and r.get("sideways_subregime") == "SIDEWAYS_RECOVERY" and num(r.get("market_flow_score")) >= 70,
        "UPGRADE_WATCH_RECOVERY": lambda r: phase3i.pass_quality_rule(r, TARGET_RULE),
    }
    out = {}
    for name, fn in rules.items():
        rr = [r for r in quality_rows if fn(r)]
        dd = enrich_dedup_top1(rr, phase3i, phase3g, ctx) if rr else []
        out[name] = {"raw": len(rr), **compact_metrics(dd, phase3g)}
    return out


def threshold_sensitivity(quality_rows: list[dict[str, Any]], phase3i, phase3g, ctx: dict[str, Any]) -> dict[str, Any]:
    out = {}
    base = [r for r in quality_rows if not r.get("proxy_or_index_symbol") and r.get("sideways_subregime") == "SIDEWAYS_RECOVERY"]
    for stc in [85, 90, 95]:
        for flow in [60, 65, 70, 75]:
            rr = [r for r in base if num(r.get("stc_score")) >= stc and num(r.get("market_flow_score")) >= flow]
            dd = enrich_dedup_top1(rr, phase3i, phase3g, ctx) if rr else []
            out[f"RECOVERY_STC{stc}_FLOW{flow}"] = {"raw": len(rr), **compact_metrics(dd, phase3g)}
    return out


def make_decision(full: dict[str, Any], splits: dict[str, Any], loo: dict[str, Any], toprem: dict[str, Any], sens: dict[str, Any]) -> dict[str, Any]:
    n = int(full.get("n") or 0)
    full20 = num(full.get("20d_avg_excess_pct"))
    full30 = num(full.get("30d_avg_excess_pct"))
    half_results = list(splits.get("by_year_half", {}).values())
    positive_halves_20 = sum(1 for r in half_results if (r.get("n") or 0) >= 3 and num(r.get("20d_avg_excess_pct")) > 0)
    positive_halves_30 = sum(1 for r in half_results if (r.get("n") or 0) >= 3 and num(r.get("30d_avg_excess_pct")) > 0)
    eligible_halves = sum(1 for r in half_results if (r.get("n") or 0) >= 3)
    min_loo30 = loo.get("min_30d_excess_pct")
    remove_top1_30 = toprem.get("remove_top1_by_excess_30d_pct", {}).get("30d_avg_excess_pct")
    stable_sens = [r for r in sens.values() if (r.get("n") or 0) >= 8]
    pos_sens_30 = sum(1 for r in stable_sens if num(r.get("30d_avg_excess_pct")) > 0)

    pass_flags = {
        "full_20d_30d_positive": full20 > 0 and full30 > 0,
        "sample_at_least_20": n >= 20,
        "at_least_two_eligible_half_windows": eligible_halves >= 2,
        "at_least_two_positive_half_windows_30d": positive_halves_30 >= 2,
        "leave_one_symbol_min30_non_negative": min_loo30 is not None and num(min_loo30) >= 0,
        "remove_top1_30d_non_negative": remove_top1_30 is not None and num(remove_top1_30) >= 0,
        "threshold_sensitivity_majority_30d_positive": len(stable_sens) > 0 and pos_sens_30 / len(stable_sens) >= 0.5,
    }
    passed = sum(1 for v in pass_flags.values() if v)
    if pass_flags["full_20d_30d_positive"] and passed >= 5:
        decision = "PROMISING_BUT_STILL_DIAGNOSTIC_ONLY"
    elif pass_flags["full_20d_30d_positive"]:
        decision = "PROMISING_BUT_OVERFIT_RISK_ELEVATED"
    else:
        decision = "NOT_ROBUST_ENOUGH"
    return {
        "decision": decision,
        "passed_checks": passed,
        "total_checks": len(pass_flags),
        "checks": pass_flags,
        "notes": [
            "This is not a trading approval.",
            "UPTREND Confirmed execution remains unchanged.",
            "A later portfolio simulation is required before any execution-layer discussion.",
        ],
    }


def write_report(result: dict[str, Any]) -> None:
    full = result["full_target_metrics"]
    dec = result["decision"]
    md = []
    md.append("# E1-R Phase 3I-R — SIDEWAYS_RECOVERY Robustness Diagnostic")
    md.append("")
    md.append("Diagnostic only. No trading logic changed. UPTREND Confirmed remains protected.")
    md.append("")
    md.append("## Target")
    md.append("")
    md.append("`UPGRADE_WATCH_RECOVERY` from Phase 3I.")
    md.append("")
    md.append("## Full target metrics")
    md.append("")
    md.append(f"- n: {full.get('n')}")
    md.append(f"- 20D excess: {pct_str(full.get('20d_avg_excess_pct'))}")
    md.append(f"- 30D excess: {pct_str(full.get('30d_avg_excess_pct'))}")
    md.append(f"- upgrade30: {pct_str(full.get('upgrade30_rate_pct'))}")
    md.append(f"- fail20: {pct_str(full.get('fail20_rate_pct'))}")
    md.append("")
    md.append("## Decision")
    md.append("")
    md.append(f"Decision: `{dec['decision']}`")
    md.append(f"Checks passed: {dec['passed_checks']} / {dec['total_checks']}")
    md.append("")
    md.append("## Robustness checks")
    md.append("")
    md.append("### Year-half splits")
    md.append("")
    md.append("| Window | n | 20D excess | 30D excess | upgrade30 | fail20 |")
    md.append("|---|---:|---:|---:|---:|---:|")
    for k, r in result["split_diagnostics"]["by_year_half"].items():
        md.append(f"| {k} | {r.get('n')} | {pct_str(r.get('20d_avg_excess_pct'))} | {pct_str(r.get('30d_avg_excess_pct'))} | {pct_str(r.get('upgrade30_rate_pct'))} | {pct_str(r.get('fail20_rate_pct'))} |")
    md.append("")
    md.append("### Simple rule comparison")
    md.append("")
    md.append("| Rule | raw | n | 20D excess | 30D excess | upgrade30 | fail20 |")
    md.append("|---|---:|---:|---:|---:|---:|---:|")
    for k, r in result["simple_rule_comparison"].items():
        md.append(f"| {k} | {r.get('raw')} | {r.get('n')} | {pct_str(r.get('20d_avg_excess_pct'))} | {pct_str(r.get('30d_avg_excess_pct'))} | {pct_str(r.get('upgrade30_rate_pct'))} | {pct_str(r.get('fail20_rate_pct'))} |")
    md.append("")
    md.append("## Interpretation")
    md.append("")
    md.append("Phase 3I-R is an overfit-defense diagnostic. Passing it does not approve SIDEWAYS execution. It only determines whether Phase 3I deserves a later portfolio-level simulation.")
    md.append("")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    phase3i, phase3g, _phase3h, quality_rows, ctx = build_phase3i_quality_rows()

    target_rows = [r for r in quality_rows if phase3i.pass_quality_rule(r, TARGET_RULE)]
    target_dedup = enrich_dedup_top1(target_rows, phase3i, phase3g, ctx)

    full = compact_metrics(target_dedup, phase3g)
    splits = split_diagnostics(target_rows, phase3i, phase3g, ctx)
    loo = leave_one_symbol_out(target_dedup, phase3g)
    toprem = remove_top_winners(target_dedup, phase3g)
    monthloo = leave_one_month_out(target_dedup, phase3g)
    simple = simple_rule_comparison(quality_rows, phase3i, phase3g, ctx)
    sens = threshold_sensitivity(quality_rows, phase3i, phase3g, ctx)
    dec = make_decision(full, splits, loo, toprem, sens)

    result = {
        "status": "DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "strategy_id": E1R_ID,
        "target_rule": TARGET_RULE,
        "fairness_controls": {
            "does_not_change_trading_logic": True,
            "protects_existing_uptrend_confirmed_execution": True,
            "uses_phase3i_candidate_definition": True,
            "uses_same_forward_return_method_as_phase3g_phase3i": True,
            "portfolio_simulation_not_included": True,
        },
        "candidate_universe": {k: v for k, v in ctx.items() if k not in {"spx_dates", "spx_closes", "price_map"}},
        "full_target_metrics": full,
        "target_dedup_sample": target_dedup[:20],
        "split_diagnostics": splits,
        "leave_one_symbol_out": loo,
        "leave_top_winners_out": toprem,
        "leave_one_month_out": monthloo,
        "simple_rule_comparison": simple,
        "threshold_sensitivity": sens,
        "decision": dec,
        "interpretation": {
            "primary_question": "Is Phase 3I UPGRADE_WATCH_RECOVERY robust enough to remain a research hypothesis?",
            "execution_policy": "No SIDEWAYS execution is approved by this diagnostic.",
            "next_step_if_promising": "Phase 3J portfolio-level simulation with strict UPTREND protection constraints.",
        },
    }

    OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    write_report(result)

    print("E1-R PHASE 3I-R SIDEWAYS_RECOVERY ROBUSTNESS DIAGNOSTIC")
    print("Status: DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE")
    print(f"Target: {TARGET_RULE}")
    print(f"Target dedup n: {full.get('n')}, unique_symbols: {full.get('unique_symbols')}")
    print(f"Full: 20D excess={pct_str(full.get('20d_avg_excess_pct'))} 30D excess={pct_str(full.get('30d_avg_excess_pct'))} upgrade30={pct_str(full.get('upgrade30_rate_pct'))} fail20={pct_str(full.get('fail20_rate_pct'))}")
    print("\nYear-half splits:")
    for k, r in splits["by_year_half"].items():
        print(f"  {k}: n={r.get('n')} 20D excess={pct_str(r.get('20d_avg_excess_pct'))} 30D excess={pct_str(r.get('30d_avg_excess_pct'))} upgrade30={pct_str(r.get('upgrade30_rate_pct'))} fail20={pct_str(r.get('fail20_rate_pct'))}")
    print("\nSimple rule comparison:")
    for k, r in simple.items():
        print(f"  {k}: raw={r.get('raw')} n={r.get('n')} 20D excess={pct_str(r.get('20d_avg_excess_pct'))} 30D excess={pct_str(r.get('30d_avg_excess_pct'))} upgrade30={pct_str(r.get('upgrade30_rate_pct'))} fail20={pct_str(r.get('fail20_rate_pct'))}")
    print("\nOverfit-defense decision:")
    print(f"  Decision: {dec['decision']}")
    print(f"  Checks passed: {dec['passed_checks']} / {dec['total_checks']}")
    for k, v in dec["checks"].items():
        print(f"    {k}: {'PASS' if v else 'FAIL'}")
    print(f"\nOutput: {OUT_JSON}")
    print(f"Report: {OUT_MD}")


if __name__ == "__main__":
    main()
