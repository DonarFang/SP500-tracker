#!/usr/bin/env python3
"""
E1R_SIDEWAYS_PAPER_PORTFOLIO_V0_2

Clean-architecture research script.

What changed vs v0.1:
- Reusable logic moved to src/research/e1r_sideways.py.
- VIXY is explicitly excluded.
- Benchmark reporting is fixed:
  1. full_period_strategy_return
  2. full_period_spx_return
  3. active_window_strategy_return
  4. active_window_spx_return
  5. sideways_all_days_spx_return
  6. allowed_sideways_spx_return

This script remains research-only and does not modify official E1-R.
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
    load_asset,
    load_regimes,
    load_stock_universe,
    run_daily_rebalanced_sidecar,
    summarize_sample_counts,
    summarize_sidecar,
)


CONFIG = ResearchConfig(
    start_date="2021-06-11",
    end_date="2026-06-16",
    min_history_days=200,
    min_price=5.0,
    initial_equity=100000.0,
    excluded_symbols=("VIXY",),
)


RAW_STOCK_DIR = ROOT / "data/research/e1_5y/raw/stocks"
RAW_INDEX_DIR = ROOT / "data/research/e1_5y/raw/indices"
REGIME_PATH = ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json"

OUT_DIR = ROOT / "data/research/e1_5y/sideways_full_scan"
OUT_PATH = OUT_DIR / "e1r_sideways_paper_portfolio_v0_2.json"


VARIANTS = {
    "S0_CURRENT_CASH": {
        "description": "Baseline: current E1-R behavior during SIDEWAYS, no active SIDEWAYS execution.",
        "allowed_subclasses": [],
        "top_n": 0,
        "gross_exposure": 0.0,
    },
    "S1_MA_CONFLICT_TOP20_HALF": {
        "description": "MA_CONFLICT only, top 20 ranked candidates, 50% gross exposure.",
        "allowed_subclasses": ["MA_CONFLICT"],
        "top_n": 20,
        "gross_exposure": 0.50,
    },
    "S2_MA_CONFLICT_TOP10_HALF": {
        "description": "MA_CONFLICT only, top 10 ranked candidates, 50% gross exposure.",
        "allowed_subclasses": ["MA_CONFLICT"],
        "top_n": 10,
        "gross_exposure": 0.50,
    },
    "S3_MA_CONFLICT_TOP5_HALF": {
        "description": "MA_CONFLICT only, top 5 ranked candidates, 50% gross exposure.",
        "allowed_subclasses": ["MA_CONFLICT"],
        "top_n": 5,
        "gross_exposure": 0.50,
    },
    "S4_MA_CONFLICT_TOP10_QUARTER": {
        "description": "MA_CONFLICT only, top 10 ranked candidates, 25% gross exposure.",
        "allowed_subclasses": ["MA_CONFLICT"],
        "top_n": 10,
        "gross_exposure": 0.25,
    },
    "S5_DETERIORATION_TOP10_QUARTER": {
        "description": "DETERIORATION_TRANSITION only, top 10 ranked candidates, 25% gross exposure. Diagnostic only.",
        "allowed_subclasses": ["DETERIORATION_TRANSITION"],
        "top_n": 10,
        "gross_exposure": 0.25,
    },
    "S6_RECOVERY_TOP10_HALF_DIAGNOSTIC": {
        "description": "RECOVERY_TRANSITION only, top 10 ranked candidates, 50% gross exposure. Negative-control diagnostic.",
        "allowed_subclasses": ["RECOVERY_TRANSITION"],
        "top_n": 10,
        "gross_exposure": 0.50,
    },
}


def compact_summary(summary: dict) -> dict:
    keys = [
        "full_period_strategy_return_pct",
        "full_period_spx_return_pct",
        "full_period_excess_vs_spx_pct",
        "active_window_strategy_return_pct",
        "active_window_spx_return_pct",
        "active_window_excess_vs_spx_pct",
        "sideways_all_days_spx_return_pct",
        "allowed_sideways_spx_return_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe",
        "active_days",
        "sideways_days",
        "allowed_sideways_days",
        "exposure_pct_full_period",
        "exposure_pct_sideways_only",
        "active_day_win_rate_pct",
        "avg_active_day_return_pct",
        "trade_count_approx",
        "unique_symbols",
        "top_3_symbols_contribution_pct_of_total_abs",
        "top_3_trades_contribution_pct_of_total_abs",
        "top_3_symbols_by_contribution",
    ]
    return {k: summary.get(k) for k in keys}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading regimes...")
    regimes = load_regimes(REGIME_PATH)

    print("Loading SPX...")
    spx = load_asset(RAW_INDEX_DIR / "SPX.json")

    print("Loading stocks...")
    stocks, excluded_found = load_stock_universe(RAW_STOCK_DIR, CONFIG)

    print(f"Stocks loaded after exclusions: {len(stocks)}")
    print(f"Excluded symbols found: {excluded_found}")

    print("Building intervals...")
    intervals = build_backtest_intervals(spx, regimes, CONFIG)
    print(f"Backtest intervals: {len(intervals)}")

    print("Building daily rankings...")
    rankings = build_daily_rankings(stocks, spx, regimes, intervals, CONFIG)
    print(f"SIDEWAYS ranked days: {len(rankings)}")

    variant_records = {}
    variant_summaries = {}

    for name, variant in VARIANTS.items():
        records = run_daily_rebalanced_sidecar(
            variant=variant,
            rankings=rankings,
            spx=spx,
            regimes=regimes,
            intervals=intervals,
        )
        variant_records[name] = records
        variant_summaries[name] = summarize_sidecar(
            name=name,
            variant=variant,
            records=records,
            initial_equity=CONFIG.initial_equity,
        )

    sample_counts = summarize_sample_counts(
        records=next(iter(variant_records.values())),
        stock_count=len(stocks),
        excluded_found=excluded_found,
    )

    report = {
        "scan_name": "E1R_SIDEWAYS_PAPER_PORTFOLIO_V0_2",
        "status": "RESEARCH_ONLY_NOT_OFFICIAL_STRATEGY",
        "sample_window": {
            "start": CONFIG.start_date,
            "end": CONFIG.end_date,
        },
        "method": {
            "architecture": "thin_script_plus_reusable_research_module",
            "portfolio_type": "daily_close_to_next_close_rebalanced_sidecar",
            "initial_equity": CONFIG.initial_equity,
            "excluded_symbols": list(CONFIG.excluded_symbols),
            "excluded_symbols_found_in_raw_data": excluded_found,
            "transaction_costs": "not_included",
            "slippage": "not_included",
            "official_strategy_change": False,
            "benchmark_fix": {
                "full_period_spx_return": "SPX compounded over all backtest intervals.",
                "active_window_spx_return": "SPX compounded only on days when this variant is active.",
                "sideways_all_days_spx_return": "SPX compounded over all SIDEWAYS days.",
                "allowed_sideways_spx_return": "SPX compounded over SIDEWAYS subclass days allowed by the variant.",
            },
        },
        "frozen_constraints": {
            "do_not_modify_uptrend_e1r_logic": True,
            "do_not_modify_dowtrend_cash_logic": True,
            "sideways_scan_is_sidecar_research_only": True,
        },
        "sample_counts": sample_counts,
        "variant_summaries": variant_summaries,
        "variant_daily_samples": {
            name: {
                "first_3": records[:3],
                "last_3": records[-3:],
            }
            for name, records in variant_records.items()
        },
    }

    OUT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False))

    print("\nDONE")
    print(f"Wrote: {OUT_PATH}")

    print("\nMETHOD")
    print(json.dumps(report["method"], indent=2, ensure_ascii=False))

    print("\nSAMPLE COUNTS")
    print(json.dumps(sample_counts, indent=2, ensure_ascii=False))

    print("\nVARIANT SUMMARIES")
    for name, summary in variant_summaries.items():
        print(f"\n{name}")
        print(json.dumps(compact_summary(summary), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
