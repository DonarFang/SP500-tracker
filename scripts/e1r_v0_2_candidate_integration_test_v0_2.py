#!/usr/bin/env python3
"""
E1-R v0.2 candidate S4 integration test, v0.2.

Fix vs previous integration test:
- Uses explicit canonical baseline path.
- Aligns baseline daily returns by next_date to sidecar intervals.
- Avoids fuzzy daily-series extraction for the actual comparison.

Candidate:
UPTREND  = unchanged E1R v0.1 baseline
SIDEWAYS = MA_CONFLICT only, top 10, 25% gross exposure
DOWNTREND = cash / no sidecar exposure
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.research.e1r_sideways import (  # noqa: E402
    ResearchConfig,
    build_backtest_intervals,
    build_daily_rankings,
    close_to_close_return,
    load_asset,
    load_regimes,
    load_stock_universe,
    run_daily_rebalanced_sidecar,
)
from src.research.e1r_integration import (  # noqa: E402
    align_baseline_returns_to_intervals,
    integrate_aligned_baseline_and_sidecar,
    load_canonical_baseline_daily_equity,
)


CONFIG = ResearchConfig(
    start_date="2021-06-11",
    end_date="2026-06-16",
    min_history_days=200,
    min_price=5.0,
    initial_equity=100000.0,
    excluded_symbols=("VIXY",),
)

S4_VARIANT = {
    "description": "E1-R v0.2 candidate sidecar: MA_CONFLICT only, top 10, 25% gross exposure.",
    "allowed_subclasses": ["MA_CONFLICT"],
    "top_n": 10,
    "gross_exposure": 0.25,
}

RAW_STOCK_DIR = ROOT / "data/research/e1_5y/raw/stocks"
RAW_INDEX_DIR = ROOT / "data/research/e1_5y/raw/indices"
REGIME_PATH = ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json"

CANONICAL_BASELINE_PATH = ROOT / "exports/backtest.json"
CANONICAL_BASELINE_JSON_PATH = (
    "$.backtest.results.layer_d.variant_results."
    "E1R_REGIME_AWARE_V0_1.daily_equity_records"
)

OUT_DIR = ROOT / "data/research/e1_5y/integration_tests"
OUT_PATH = OUT_DIR / "e1r_v0_2_candidate_s4_integration_test_v0_2.json"


def build_spx_records(spx: dict, intervals: list[tuple[str, str]]) -> list[dict]:
    return [
        {
            "date": date,
            "next_date": next_date,
            "spx_return": close_to_close_return(spx, date, next_date) or 0.0,
        }
        for date, next_date in intervals
    ]


def compact(summary: dict) -> dict:
    keys = [
        "name",
        "days",
        "return_pct",
        "spx_return_pct",
        "alpha_vs_spx_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe",
        "win_rate_pct",
        "equity_start",
        "equity_end",
    ]
    return {k: summary.get(k) for k in keys}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading canonical baseline E1-R daily equity...")
    baseline_daily = load_canonical_baseline_daily_equity(
        CANONICAL_BASELINE_PATH,
        CANONICAL_BASELINE_JSON_PATH,
    )
    print(f"Canonical baseline rows: {len(baseline_daily)}")
    print(f"Canonical baseline first/last: {baseline_daily[0]['date']} -> {baseline_daily[-1]['date']}")

    print("Loading regimes...")
    regimes = load_regimes(REGIME_PATH)

    print("Loading SPX...")
    spx = load_asset(RAW_INDEX_DIR / "SPX.json")

    print("Loading stocks with exclusions...")
    stocks, excluded_found = load_stock_universe(RAW_STOCK_DIR, CONFIG)
    print(f"Stocks loaded after exclusions: {len(stocks)}")
    print(f"Excluded symbols found: {excluded_found}")

    print("Building intervals...")
    intervals = build_backtest_intervals(spx, regimes, CONFIG)
    print(f"Backtest intervals: {len(intervals)}")
    print(f"First interval: {intervals[0][0]} -> {intervals[0][1]}")
    print(f"Last interval: {intervals[-1][0]} -> {intervals[-1][1]}")

    print("Aligning baseline returns to intervals by next_date...")
    baseline_intervals = align_baseline_returns_to_intervals(
        baseline_daily,
        intervals,
    )
    print(f"Aligned baseline intervals: {len(baseline_intervals)}")

    print("Building SIDEWAYS rankings...")
    rankings = build_daily_rankings(stocks, spx, regimes, intervals, CONFIG)
    print(f"SIDEWAYS ranked days: {len(rankings)}")

    print("Running S4 sidecar...")
    sidecar_records = run_daily_rebalanced_sidecar(
        variant=S4_VARIANT,
        rankings=rankings,
        spx=spx,
        regimes=regimes,
        intervals=intervals,
    )

    print("Building SPX interval records...")
    spx_records = build_spx_records(spx, intervals)

    print("Integrating interval-aligned baseline + sidecar...")
    result = integrate_aligned_baseline_and_sidecar(
        baseline_interval_records=baseline_intervals,
        sidecar_records=sidecar_records,
        spx_records=spx_records,
        regimes=regimes,
        initial_equity=CONFIG.initial_equity,
    )

    report = {
        "test_name": "E1R_V0_2_CANDIDATE_S4_INTEGRATION_TEST_V0_2",
        "status": "RESEARCH_ONLY_NOT_OFFICIAL_STRATEGY",
        "baseline_variant": "E1R_REGIME_AWARE_V0_1",
        "candidate_definition": {
            "uptrend": "unchanged E1R_REGIME_AWARE_V0_1 baseline",
            "sideways": "MA_CONFLICT only, top 10, 25% gross exposure",
            "downtrend": "cash / no sidecar exposure",
        },
        "method": {
            "baseline_source_path": str(CANONICAL_BASELINE_PATH.relative_to(ROOT)),
            "baseline_json_path": CANONICAL_BASELINE_JSON_PATH,
            "alignment": "baseline daily return ending at next_date is matched to sidecar interval date->next_date",
            "composition": "daily_combined_return = (1 + baseline_return) * (1 + sidecar_return) - 1",
            "transaction_costs": "not_included",
            "slippage": "not_included",
            "official_strategy_change": False,
            "excluded_symbols": list(CONFIG.excluded_symbols),
            "excluded_symbols_found_in_raw_data": excluded_found,
        },
        "result": result,
    }

    OUT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False))

    print("\nDONE")
    print(f"Wrote: {OUT_PATH}")

    print("\nALIGNMENT SAMPLE")
    print(json.dumps({
        "alignment": result["alignment"],
        "shared_intervals": result["shared_intervals"],
        "first_interval": result["first_interval"],
        "last_interval": result["last_interval"],
        "regime_counts": result["regime_counts"],
        "sidecar_active_by_regime": result["sidecar_active_by_regime"],
        "sidecar_active_by_subclass": result["sidecar_active_by_subclass"],
    }, indent=2, ensure_ascii=False))

    print("\nBASELINE SUMMARY")
    print(json.dumps(compact(result["baseline_summary"]), indent=2, ensure_ascii=False))

    print("\nSIDECAR SUMMARY")
    print(json.dumps(compact(result["sidecar_summary"]), indent=2, ensure_ascii=False))

    print("\nCOMBINED CANDIDATE SUMMARY")
    print(json.dumps(compact(result["combined_summary"]), indent=2, ensure_ascii=False))

    print("\nDELTA VS BASELINE")
    print(json.dumps(result["delta_vs_baseline"], indent=2, ensure_ascii=False))

    print("\nPASS / FAIL")
    print(json.dumps(result["pass_fail"], indent=2, ensure_ascii=False))

    print("\nSIDECAR CONTRIBUTION")
    print(json.dumps({
        "by_regime_pct": result["sidecar_simple_contribution_by_regime_pct"],
        "by_subclass_pct": result["sidecar_simple_contribution_by_subclass_pct"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
