#!/usr/bin/env python3
"""
E1-R Phase 3K: SIDEWAYS Recovery Regime Definition Review

Purpose
-------
Review whether the SIDEWAYS_RECOVERY sub-regime identified in Phase 3I/3I-R
looks like a meaningful regime definition or a narrow time-window artifact.

This diagnostic is intentionally conservative:
- It does NOT change trading logic.
- It does NOT modify E1/E1-R benchmarks.
- It does NOT approve SIDEWAYS execution.
- It only reviews Phase 3I / 3I-R evidence and writes a research report.

Inputs
------
- exports/backtest.json
- data/research/e1r/e1r_phase3i_sideways_quality_decomposition_diagnostic.json
- data/research/e1r/e1r_phase3ir_sideways_recovery_robustness_diagnostic.json

Outputs
-------
- data/research/e1r/e1r_phase3k_sideways_recovery_regime_definition_review.json
- data/research/e1r/E1R_PHASE3K_SIDEWAYS_RECOVERY_REGIME_DEFINITION_REVIEW.md
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BACKTEST_PATH = ROOT / "exports" / "backtest.json"
PHASE3I_PATH = ROOT / "data" / "research" / "e1r" / "e1r_phase3i_sideways_quality_decomposition_diagnostic.json"
PHASE3IR_PATH = ROOT / "data" / "research" / "e1r" / "e1r_phase3ir_sideways_recovery_robustness_diagnostic.json"
OUT_JSON = ROOT / "data" / "research" / "e1r" / "e1r_phase3k_sideways_recovery_regime_definition_review.json"
OUT_MD = ROOT / "data" / "research" / "e1r" / "E1R_PHASE3K_SIDEWAYS_RECOVERY_REGIME_DEFINITION_REVIEW.md"

E1_ID = "E1_AUDITED_G4_MINHOLD10"
E1R_ID = "E1R_REGIME_AWARE_V0_1"
TARGET_RULE = "UPGRADE_WATCH_RECOVERY"
BASE_RULE = "BASE_STC_COMMON_EQUITY"
RECOVERY_SIMPLE_RULE = "SIDEWAYS_RECOVERY_COMMON_EQUITY"
RECOVERY_STC90_RULE = "SIDEWAYS_RECOVERY_STC90"
RECOVERY_FLOW70_RULE = "SIDEWAYS_RECOVERY_FLOW70"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}\nRun prior phase diagnostics first.")
    with path.open("r", encoding="utf-8") as f:
        obj = json.load(f)
    if not isinstance(obj, dict):
        raise SystemExit(f"Expected dict JSON at {path}")
    return obj


def safe_variants(backtest: dict[str, Any]) -> dict[str, Any]:
    candidate_paths = [
        ("variant_results",),
        ("variants",),
        ("results",),
        ("backtest", "results", "layer_d", "variant_results"),
        ("backtest", "results", "layer_d", "variants"),
    ]
    for path in candidate_paths:
        obj: Any = backtest
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


def get_nested(d: dict[str, Any], path: list[str], default: Any = None) -> Any:
    obj: Any = d
    for key in path:
        if isinstance(obj, dict) and key in obj:
            obj = obj[key]
        else:
            return default
    return obj


def find_dict_containing(obj: Any, required_keys: set[str]) -> dict[str, Any] | None:
    """Find first dict whose keys contain required_keys."""
    if isinstance(obj, dict):
        if required_keys.issubset(set(obj.keys())):
            return obj
        for v in obj.values():
            found = find_dict_containing(v, required_keys)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for v in obj:
            found = find_dict_containing(v, required_keys)
            if found is not None:
                return found
    return None


def find_half_splits(obj: Any) -> dict[str, Any]:
    """Find a dict containing year-half split keys such as 2025H1."""
    if isinstance(obj, dict):
        keys = set(obj.keys())
        half_keys = {k for k in keys if isinstance(k, str) and len(k) == 6 and k[:4].isdigit() and k[4] == "H" and k[5] in "12"}
        if half_keys:
            return {k: obj[k] for k in sorted(half_keys)}
        for v in obj.values():
            found = find_half_splits(v)
            if found:
                return found
    elif isinstance(obj, list):
        for v in obj:
            found = find_half_splits(v)
            if found:
                return found
    return {}


def metric(rule: dict[str, Any], horizon: str, field: str) -> float | None:
    # Common layout from Phase 3I/3I-R.
    for key in ("forward_daily_top1_dedup", "forward_top1_dedup", "forward", "forward_summary"):
        sub = rule.get(key)
        if isinstance(sub, dict) and isinstance(sub.get(horizon), dict):
            val = sub[horizon].get(field)
            return to_float(val)
    # Some diagnostics flatten 20D/30D fields.
    flat_keys = [
        f"{horizon}_{field}",
        f"{horizon}_{field.replace('_pct', '')}",
        f"{horizon}_avg_excess_pct" if field == "avg_excess_pct" else "",
        f"{horizon}_avg_return_pct" if field == "avg_return_pct" else "",
    ]
    for k in flat_keys:
        if k and k in rule:
            return to_float(rule.get(k))
    return None


def to_float(v: Any) -> float | None:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = v.strip().replace("%", "")
        if s.lower() in {"n/a", "na", "none", "null", ""}:
            return None
        try:
            return float(s)
        except ValueError:
            return None
    return None


def n_value(rule: dict[str, Any]) -> int | None:
    for k in ("dedup_top1_count", "n", "count", "sample_n"):
        v = rule.get(k)
        if isinstance(v, int):
            return v
        if isinstance(v, float):
            return int(v)
        if isinstance(v, str) and v.isdigit():
            return int(v)
    return None


def get_rule_summary(rule: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(rule, dict):
        return {"available": False}
    return {
        "available": True,
        "raw_candidates": rule.get("raw_candidates"),
        "candidate_days": rule.get("candidate_days"),
        "dedup_top1_count": n_value(rule),
        "20d_avg_return_pct": metric(rule, "20d", "avg_return_pct"),
        "20d_avg_excess_pct": metric(rule, "20d", "avg_excess_pct"),
        "20d_excess_win_rate_pct": metric(rule, "20d", "excess_win_rate_pct"),
        "30d_avg_return_pct": metric(rule, "30d", "avg_return_pct"),
        "30d_avg_excess_pct": metric(rule, "30d", "avg_excess_pct"),
        "30d_excess_win_rate_pct": metric(rule, "30d", "excess_win_rate_pct"),
        "upgrade30_pct": to_float(rule.get("upgrade_to_uptrend_confirmed_30d_rate_pct") or rule.get("upgrade30_pct") or rule.get("upgrade30")),
        "fail20_pct": to_float(rule.get("failure_rate_20d_pct") or rule.get("fail20_pct") or rule.get("fail20")),
    }


def pct(v: Any) -> str:
    x = to_float(v)
    if x is None:
        return "n/a"
    return f"{x:+.2f}%"


def plain_pct(v: Any) -> str:
    x = to_float(v)
    if x is None:
        return "n/a"
    return f"{x:.2f}%"


def main() -> None:
    backtest = load_json(BACKTEST_PATH)
    variants = safe_variants(backtest)
    found_variants = sorted(variants.keys()) if isinstance(variants, dict) else []
    if E1_ID not in found_variants or E1R_ID not in found_variants:
        raise SystemExit(
            "Missing required E1/E1-R variants in exports/backtest.json.\n"
            f"Found: {found_variants}\n"
            "Run `python3 run_backtest.py` first, then rerun this diagnostic."
        )

    p3i = load_json(PHASE3I_PATH)
    p3ir = load_json(PHASE3IR_PATH)

    p3i_rules = p3i.get("rule_results") if isinstance(p3i.get("rule_results"), dict) else {}
    p3ir_simple = find_dict_containing(p3ir, {BASE_RULE, RECOVERY_SIMPLE_RULE}) or {}
    p3ir_target_holder = find_dict_containing(p3ir, {TARGET_RULE}) or {}
    half_splits = find_half_splits(p3ir)

    # Prefer 3I-R simple comparisons for robustness review; fall back to 3I rule results.
    target_rule = p3ir_target_holder.get(TARGET_RULE) or p3i_rules.get(TARGET_RULE)
    base_rule = p3ir_simple.get(BASE_RULE) or p3i_rules.get(BASE_RULE)
    simple_recovery_rule = p3ir_simple.get(RECOVERY_SIMPLE_RULE)
    recovery_stc90_rule = p3ir_simple.get(RECOVERY_STC90_RULE)
    recovery_flow70_rule = p3ir_simple.get(RECOVERY_FLOW70_RULE)

    summaries = {
        BASE_RULE: get_rule_summary(base_rule),
        RECOVERY_SIMPLE_RULE: get_rule_summary(simple_recovery_rule),
        RECOVERY_STC90_RULE: get_rule_summary(recovery_stc90_rule),
        RECOVERY_FLOW70_RULE: get_rule_summary(recovery_flow70_rule),
        TARGET_RULE: get_rule_summary(target_rule),
    }

    # Phase 3I-R simple_rule_comparison has forward/excess metrics but may not carry
    # upgrade30 / fail20 fields. Phase 3I rule_results contains those diagnostic fields.
    # Enrich only missing upgrade/failure fields from Phase 3I to keep 3K reporting complete.
    for rule_name, summary in summaries.items():
        src3i = p3i_rules.get(rule_name)
        if not isinstance(summary, dict) or not isinstance(src3i, dict):
            continue
        src_summary = get_rule_summary(src3i)
        if summary.get("upgrade30_pct") is None and src_summary.get("upgrade30_pct") is not None:
            summary["upgrade30_pct"] = src_summary.get("upgrade30_pct")
        if summary.get("fail20_pct") is None and src_summary.get("fail20_pct") is not None:
            summary["fail20_pct"] = src_summary.get("fail20_pct")

    target = summaries[TARGET_RULE]
    base = summaries[BASE_RULE]
    simple = summaries[RECOVERY_SIMPLE_RULE]

    # Half-window diagnostics.
    eligible_half_windows = []
    positive_30d_half_windows = []
    half_window_summaries: dict[str, Any] = {}
    for hk, hv in half_splits.items():
        hs = get_rule_summary(hv) if isinstance(hv, dict) else {"available": False}
        half_window_summaries[hk] = hs
        if (hs.get("dedup_top1_count") or 0) > 0:
            eligible_half_windows.append(hk)
            if to_float(hs.get("30d_avg_excess_pct")) is not None and to_float(hs.get("30d_avg_excess_pct")) > 0:
                positive_30d_half_windows.append(hk)

    # Regime-definition checks.
    checks: dict[str, dict[str, Any]] = {}

    def add_check(name: str, passed: bool, detail: str, severity: str = "INFO") -> None:
        checks[name] = {"passed": bool(passed), "severity": severity, "detail": detail}

    add_check(
        "recovery_subregime_has_positive_excess",
        (to_float(simple.get("20d_avg_excess_pct")) or -999) > 0 and (to_float(simple.get("30d_avg_excess_pct")) or -999) > 0,
        f"{RECOVERY_SIMPLE_RULE}: 20D excess {pct(simple.get('20d_avg_excess_pct'))}, 30D excess {pct(simple.get('30d_avg_excess_pct'))}.",
        "HIGH",
    )
    add_check(
        "target_rule_positive_excess",
        (to_float(target.get("20d_avg_excess_pct")) or -999) > 0 and (to_float(target.get("30d_avg_excess_pct")) or -999) > 0,
        f"{TARGET_RULE}: 20D excess {pct(target.get('20d_avg_excess_pct'))}, 30D excess {pct(target.get('30d_avg_excess_pct'))}.",
        "HIGH",
    )
    add_check(
        "simple_rule_competitive_with_complex_rule",
        simple.get("available") and target.get("available") and (to_float(simple.get("30d_avg_excess_pct")) or -999) >= (to_float(target.get("30d_avg_excess_pct")) or 999) - 1.0,
        f"Simple recovery 30D excess {pct(simple.get('30d_avg_excess_pct'))} vs target 30D excess {pct(target.get('30d_avg_excess_pct'))}.",
        "MEDIUM",
    )
    add_check(
        "time_window_coverage_at_least_two_halves",
        len(eligible_half_windows) >= 2,
        f"Eligible half-windows: {eligible_half_windows or 'none'}.",
        "HIGH",
    )
    add_check(
        "positive_30d_in_at_least_two_halves",
        len(positive_30d_half_windows) >= 2,
        f"Positive 30D excess half-windows: {positive_30d_half_windows or 'none'}.",
        "HIGH",
    )
    add_check(
        "target_fail20_better_than_base",
        target.get("fail20_pct") is not None and base.get("fail20_pct") is not None and to_float(target.get("fail20_pct")) <= to_float(base.get("fail20_pct")) - 10.0,
        f"Target fail20 {plain_pct(target.get('fail20_pct'))} vs base fail20 {plain_pct(base.get('fail20_pct'))}.",
        "MEDIUM",
    )
    add_check(
        "target_sample_at_least_20",
        (target.get("dedup_top1_count") or 0) >= 20,
        f"Target dedup_top1_count={target.get('dedup_top1_count')}.",
        "MEDIUM",
    )

    high_checks = [v for v in checks.values() if v.get("severity") == "HIGH"]
    high_passed = sum(1 for v in high_checks if v.get("passed"))
    total_passed = sum(1 for v in checks.values() if v.get("passed"))

    if high_passed >= 3 and len(eligible_half_windows) >= 2:
        decision = "SIDEWAYS_RECOVERY_REGIME_DEFINITION_PROVISIONALLY_SUPPORTED"
        reason = "Recovery subregime evidence is positive and has enough time-window coverage for the next portfolio simulation stage."
    elif (to_float(target.get("30d_avg_excess_pct")) or -999) > 0 and (to_float(simple.get("30d_avg_excess_pct")) or -999) > 0:
        decision = "PROMISING_BUT_TIME_CONCENTRATED_DIAGNOSTIC_ONLY"
        reason = "SIDEWAYS_RECOVERY appears meaningful, but evidence is concentrated in too few half-year windows. Keep as Watchlist/Upgrade Watch only."
    else:
        decision = "REGIME_DEFINITION_NOT_SUPPORTED_FOR_EXECUTION"
        reason = "Recovery subregime evidence is not strong enough for portfolio simulation or execution-layer approval."

    result = {
        "status": "DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "strategy_id": E1R_ID,
        "phase": "3K",
        "target": TARGET_RULE,
        "inputs": {
            "backtest": str(BACKTEST_PATH.relative_to(ROOT)),
            "phase3i_json": str(PHASE3I_PATH.relative_to(ROOT)),
            "phase3ir_json": str(PHASE3IR_PATH.relative_to(ROOT)),
        },
        "fairness_controls": {
            "does_not_change_trading_logic": True,
            "protects_existing_uptrend_confirmed_execution": True,
            "does_not_open_sideways_execution_layer": True,
            "uses_phase3i_phase3ir_outputs_only": True,
            "sector_confirmation_status": "DATA_UNAVAILABLE_NOT_EVALUATED",
        },
        "rule_summaries": summaries,
        "half_window_summaries": half_window_summaries,
        "eligible_half_windows": eligible_half_windows,
        "positive_30d_half_windows": positive_30d_half_windows,
        "regime_definition_checks": checks,
        "decision": {
            "decision": decision,
            "reason": reason,
            "checks_passed": total_passed,
            "checks_total": len(checks),
            "high_severity_checks_passed": high_passed,
            "high_severity_checks_total": len(high_checks),
        },
        "interpretation": {
            "primary_finding": "SIDEWAYS_RECOVERY looks more informative than treating SIDEWAYS as one undifferentiated regime.",
            "main_risk": "Evidence is concentrated in a single half-year window unless future/OOS data expands coverage.",
            "research_policy": "Keep UPGRADE_WATCH_RECOVERY as High Quality Watchlist / Upgrade Watch only. Do not execute until portfolio simulation and multi-window/OOS evidence improve.",
            "next_step": "Do not run execution portfolio simulation unless accepting diagnostic-only scope; otherwise wait for more OOS samples or add longer/PIT data.",
        },
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    md = []
    md.append("# E1-R Phase 3K — SIDEWAYS Recovery Regime Definition Review")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append("DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE")
    md.append("")
    md.append("This diagnostic does not change E1, E1-R, UPTREND Confirmed, or trading logic.")
    md.append("")
    md.append("## Core Question")
    md.append("")
    md.append("Is `SIDEWAYS_RECOVERY` a meaningful sub-regime, or did Phase 3I only capture a narrow time-window artifact?")
    md.append("")
    md.append("## Rule Summary")
    md.append("")
    md.append("| Rule | n | 20D Excess | 30D Excess | Upgrade30 | Fail20 |")
    md.append("|---|---:|---:|---:|---:|---:|")
    for rule in [BASE_RULE, RECOVERY_SIMPLE_RULE, RECOVERY_STC90_RULE, RECOVERY_FLOW70_RULE, TARGET_RULE]:
        rr = summaries.get(rule, {})
        md.append(
            f"| {rule} | {rr.get('dedup_top1_count') if rr.get('available') else 'n/a'} | "
            f"{pct(rr.get('20d_avg_excess_pct'))} | {pct(rr.get('30d_avg_excess_pct'))} | "
            f"{plain_pct(rr.get('upgrade30_pct'))} | {plain_pct(rr.get('fail20_pct'))} |"
        )
    md.append("")
    md.append("## Time-Window Coverage")
    md.append("")
    if half_window_summaries:
        md.append("| Window | n | 20D Excess | 30D Excess | Upgrade30 | Fail20 |")
        md.append("|---|---:|---:|---:|---:|---:|")
        for hk, rr in half_window_summaries.items():
            md.append(
                f"| {hk} | {rr.get('dedup_top1_count') if rr.get('available') else 'n/a'} | "
                f"{pct(rr.get('20d_avg_excess_pct'))} | {pct(rr.get('30d_avg_excess_pct'))} | "
                f"{plain_pct(rr.get('upgrade30_pct'))} | {plain_pct(rr.get('fail20_pct'))} |"
            )
    else:
        md.append("No half-window split data found in Phase 3I-R JSON.")
    md.append("")
    md.append("## Regime Definition Checks")
    md.append("")
    md.append("| Check | Result | Detail |")
    md.append("|---|---:|---|")
    for name, ck in checks.items():
        md.append(f"| {name} | {'PASS' if ck.get('passed') else 'FAIL'} | {ck.get('detail')} |")
    md.append("")
    md.append("## Decision")
    md.append("")
    md.append(f"**{decision}**")
    md.append("")
    md.append(reason)
    md.append("")
    md.append("## Research Policy")
    md.append("")
    md.append("`UPGRADE_WATCH_RECOVERY` remains High Quality Watchlist / Upgrade Watch only. It is not approved for execution. UPTREND Confirmed remains unchanged.")
    md.append("")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    print("E1-R PHASE 3K SIDEWAYS_RECOVERY REGIME DEFINITION REVIEW")
    print("Status: DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE")
    print(f"Target: {TARGET_RULE}")
    print("")
    for rule in [BASE_RULE, RECOVERY_SIMPLE_RULE, RECOVERY_STC90_RULE, RECOVERY_FLOW70_RULE, TARGET_RULE]:
        rr = summaries.get(rule, {})
        print(
            f"  {rule}: n={rr.get('dedup_top1_count') if rr.get('available') else 'n/a'} "
            f"20D excess={pct(rr.get('20d_avg_excess_pct'))} "
            f"30D excess={pct(rr.get('30d_avg_excess_pct'))} "
            f"upgrade30={plain_pct(rr.get('upgrade30_pct'))} "
            f"fail20={plain_pct(rr.get('fail20_pct'))}"
        )
    print("")
    print("Half-window coverage:")
    if half_window_summaries:
        for hk, rr in half_window_summaries.items():
            print(
                f"  {hk}: n={rr.get('dedup_top1_count') if rr.get('available') else 'n/a'} "
                f"20D excess={pct(rr.get('20d_avg_excess_pct'))} "
                f"30D excess={pct(rr.get('30d_avg_excess_pct'))}"
            )
    else:
        print("  n/a")
    print("")
    print("Regime-definition checks:")
    print(f"  Checks passed: {total_passed} / {len(checks)}")
    for name, ck in checks.items():
        print(f"    {name}: {'PASS' if ck.get('passed') else 'FAIL'}")
    print("")
    print("Decision:", decision)
    print("Reason:", reason)
    print("Output:", OUT_JSON)
    print("Report:", OUT_MD)


if __name__ == "__main__":
    main()
