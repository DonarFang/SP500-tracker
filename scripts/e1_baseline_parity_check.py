#!/usr/bin/env python3
"""
E1 Baseline Parity Check v1

Purpose:
Verify that the current research worktree can reproduce the frozen audited E1 baseline
from exports/backtest.json without changing strategy logic.

This script is read-only. It does not run a backtest and does not modify E1.
"""

import json
import math
from pathlib import Path

BACKTEST_JSON = Path("exports/backtest.json")
E1_ID = "E1_AUDITED_G4_MINHOLD10"

EXPECTED = {
    "Period A": {
        "total_return_pct": 14.18,
    },
    "Period B": {
        "total_return_pct": 21.80,
    },
    "Full": {
        "total_return_pct": 7.52,
        "profit_factor": 1.25,
        "sharpe_ratio": 0.18,
        "max_drawdown_pct": 38.10,
    },
}

TOL = 0.01


def approx_equal(actual, expected, tol=TOL):
    if actual is None:
        return False
    return abs(float(actual) - float(expected)) <= tol


def find_e1_in_period(period_obj):
    variants = period_obj.get("variants", {})
    if E1_ID in variants:
        return variants[E1_ID]

    # Legacy fallback, only for reading old exports.
    if "E1_GATE_V2_MINHOLD10" in variants:
        return variants["E1_GATE_V2_MINHOLD10"]

    return None


def main():
    if not BACKTEST_JSON.exists():
        raise SystemExit(f"Missing {BACKTEST_JSON}")

    bj = json.load(open(BACKTEST_JSON))
    layer_d = bj["backtest"]["results"]["layer_d"]

    full = layer_d["variant_results"].get(E1_ID)
    if not full:
        raise SystemExit(f"Missing {E1_ID} in layer_d.variant_results")

    period_comparison = layer_d.get("period_comparison", {})

    period_a = None
    period_b = None

    for key, obj in period_comparison.items():
        label = obj.get("label", "")
        if "Period A" in label or key.startswith("A_"):
            period_a = find_e1_in_period(obj)
        if "Period B" in label or key.startswith("B_"):
            period_b = find_e1_in_period(obj)

    checks = []

    def add_check(scope, metric, actual, expected):
        passed = approx_equal(actual, expected)
        checks.append({
            "scope": scope,
            "metric": metric,
            "actual": actual,
            "expected": expected,
            "delta": None if actual is None else round(float(actual) - float(expected), 6),
            "passed": passed,
        })

    if period_a:
        add_check("Period A", "total_return_pct", period_a.get("total_return_pct"), EXPECTED["Period A"]["total_return_pct"])
    else:
        checks.append({
            "scope": "Period A",
            "metric": "total_return_pct",
            "actual": None,
            "expected": EXPECTED["Period A"]["total_return_pct"],
            "delta": None,
            "passed": False,
            "error": "Period A E1 result not found",
        })

    if period_b:
        add_check("Period B", "total_return_pct", period_b.get("total_return_pct"), EXPECTED["Period B"]["total_return_pct"])
    else:
        checks.append({
            "scope": "Period B",
            "metric": "total_return_pct",
            "actual": None,
            "expected": EXPECTED["Period B"]["total_return_pct"],
            "delta": None,
            "passed": False,
            "error": "Period B E1 result not found",
        })

    add_check("Full", "total_return_pct", full.get("total_return_pct"), EXPECTED["Full"]["total_return_pct"])
    add_check("Full", "profit_factor", full.get("profit_factor"), EXPECTED["Full"]["profit_factor"])
    add_check("Full", "sharpe_ratio", full.get("sharpe_ratio"), EXPECTED["Full"]["sharpe_ratio"])
    add_check("Full", "max_drawdown_pct", full.get("max_drawdown_pct"), EXPECTED["Full"]["max_drawdown_pct"])

    passed_all = all(c["passed"] for c in checks)

    out = {
        "check_name": "E1_BASELINE_PARITY_CHECK_V1",
        "status": "PASS" if passed_all else "FAIL",
        "tolerance": TOL,
        "source_file": str(BACKTEST_JSON),
        "strategy_id": E1_ID,
        "checks": checks,
        "note": "Read-only parity check. Does not modify E1 strategy or rerun backtest.",
    }

    out_path = Path("data/research/e1_5y/e1_baseline_parity_check.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")

    print("=" * 72)
    print("E1 BASELINE PARITY CHECK v1")
    print("=" * 72)
    print(f"Status: {out['status']}")
    print(f"Tolerance: ±{TOL}")
    print()
    print(f"{'Scope':<10} {'Metric':<22} {'Actual':>10} {'Expected':>10} {'Delta':>10} {'Pass'}")
    for c in checks:
        print(
            f"{c['scope']:<10} {c['metric']:<22} "
            f"{str(c['actual']):>10} {str(c['expected']):>10} {str(c['delta']):>10} "
            f"{'YES' if c['passed'] else 'NO'}"
        )
    print()
    print("Output:", out_path)

    if not passed_all:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
