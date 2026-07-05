#!/usr/bin/env python3
"""
E1-R baseline series alignment audit.

Purpose:
- Audit all possible E1-R baseline daily equity / return series from existing JSON outputs.
- Identify which series matches run_backtest summary return.
- Identify which series was likely used by integration extractor.
- Do not modify official strategy outputs.

This is read-only.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean, pstdev
from typing import Any, Dict, Iterable, List, Optional, Sequence


ROOT = Path(__file__).resolve().parents[1]

TARGET_VARIANT = "E1R_REGIME_AWARE_V0_1"

EXPECTED_SUMMARY_RETURN_PCT = 105.61
INTEGRATION_EXTRACTED_RETURN_PCT = 110.81369009232222

SEARCH_PATHS = [
    ROOT / "exports/backtest.json",
    ROOT / "exports/portfolio_backtest.json",
    ROOT / "exports/equity_curve.json",
    ROOT / "exports/trade_log.json",
    ROOT / "data/research/e1_5y/backtest.json",
    ROOT / "data/research/e1_5y/portfolio_backtest.json",
    ROOT / "data/research/e1_5y/equity_curve.json",
    ROOT / "data/research/e1_5y/integration_tests/e1r_v0_2_candidate_s4_integration_test.json",
]

DATE_KEYS = ("date", "timestamp", "day")
EQUITY_KEYS = ("equity", "portfolio_value", "value", "nav", "ending_equity", "total_equity")
RETURN_KEYS = ("daily_return", "return", "ret", "portfolio_return", "daily_ret")
RETURN_PCT_KEYS = ("daily_return_pct", "return_pct", "ret_pct", "portfolio_return_pct", "daily_ret_pct")


def safe_float(x: Any) -> Optional[float]:
    try:
        if x is None:
            return None
        v = float(x)
        if math.isnan(v) or math.isinf(v):
            return None
        return v
    except Exception:
        return None


def pct(x: Optional[float]) -> Optional[float]:
    return None if x is None else x * 100.0


def compound_return(returns: Iterable[float]) -> float:
    value = 1.0
    for r in returns:
        value *= 1.0 + r
    return value - 1.0


def max_drawdown_from_returns(returns: Sequence[float]) -> float:
    equity = 1.0
    peak = 1.0
    worst = 0.0

    for r in returns:
        equity *= 1.0 + r
        peak = max(peak, equity)
        worst = min(worst, equity / peak - 1.0)

    return worst


def profit_factor(returns: Sequence[float]) -> Optional[float]:
    gains = sum(r for r in returns if r > 0)
    losses = -sum(r for r in returns if r < 0)

    if losses == 0:
        if gains == 0:
            return None
        return float("inf")

    return gains / losses


def sharpe(returns: Sequence[float]) -> Optional[float]:
    if len(returns) < 2:
        return None
    sd = pstdev(returns)
    if sd == 0:
        return None
    return mean(returns) / sd * math.sqrt(252)


def first_present(row: Dict[str, Any], keys: Sequence[str]) -> Any:
    for k in keys:
        if k in row:
            return row[k]
    return None


def looks_like_daily_series(obj: Any) -> bool:
    if not isinstance(obj, list) or len(obj) < 10:
        return False

    rows = [x for x in obj if isinstance(x, dict)]
    if len(rows) < 10:
        return False

    date_hits = 0
    metric_hits = 0

    for row in rows[:30]:
        if any(k in row for k in DATE_KEYS):
            date_hits += 1
        if any(k in row for k in EQUITY_KEYS + RETURN_KEYS + RETURN_PCT_KEYS):
            metric_hits += 1

    return date_hits >= 5 and metric_hits >= 5


def variant_hint(obj: Any) -> bool:
    if isinstance(obj, dict):
        fields = [
            obj.get("variant"),
            obj.get("variant_name"),
            obj.get("name"),
            obj.get("strategy"),
            obj.get("strategy_name"),
        ]
        if TARGET_VARIANT in fields:
            return True
        return any(variant_hint(v) for v in obj.values())

    if isinstance(obj, list):
        return any(variant_hint(x) for x in obj[:50])

    if isinstance(obj, str):
        return TARGET_VARIANT in obj

    return False


def collect_series(obj: Any, path: str = "$") -> List[Dict[str, Any]]:
    found: List[Dict[str, Any]] = []

    if looks_like_daily_series(obj):
        found.append({
            "json_path": path,
            "rows": obj,
            "contains_variant_hint": variant_hint(obj),
        })
        return found

    if isinstance(obj, dict):
        for k, v in obj.items():
            found.extend(collect_series(v, f"{path}.{k}"))

    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            # Avoid exploding huge lists unless nested row is not already a daily series.
            if i >= 2000:
                break
            found.extend(collect_series(v, f"{path}[{i}]"))

    return found


def standardize_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []

    for row in rows:
        date = first_present(row, DATE_KEYS)
        if not date:
            continue

        equity = safe_float(first_present(row, EQUITY_KEYS))
        daily_return = safe_float(first_present(row, RETURN_KEYS))
        daily_return_pct = safe_float(first_present(row, RETURN_PCT_KEYS))

        if daily_return is None and daily_return_pct is not None:
            daily_return = daily_return_pct / 100.0

        out.append({
            "date": str(date)[:10],
            "equity": equity,
            "daily_return": daily_return,
            "raw_keys": sorted(row.keys()),
        })

    out.sort(key=lambda x: x["date"])

    # If returns missing but equity exists, derive returns from equity.
    if out and all(x["daily_return"] is None for x in out) and any(x["equity"] is not None for x in out):
        prev_equity = None
        for item in out:
            eq = item["equity"]
            if eq is None:
                item["daily_return"] = 0.0
            elif prev_equity is None or prev_equity == 0:
                item["daily_return"] = 0.0
            else:
                item["daily_return"] = eq / prev_equity - 1.0
            prev_equity = eq

    return [x for x in out if x["daily_return"] is not None]


def summarize_series(source_path: Path, json_path: str, rows: List[Dict[str, Any]], contains_variant_hint: bool) -> Dict[str, Any]:
    std = standardize_rows(rows)
    returns = [x["daily_return"] for x in std]

    if not std or not returns:
        return {
            "source_path": str(source_path.relative_to(ROOT)),
            "json_path": json_path,
            "valid": False,
            "reason": "no usable daily return or equity series",
        }

    total_return_pct = pct(compound_return(returns))
    maxdd_pct = pct(max_drawdown_from_returns(returns))
    pf = profit_factor(returns)
    sr = sharpe(returns)

    distance_to_summary = (
        abs(total_return_pct - EXPECTED_SUMMARY_RETURN_PCT)
        if total_return_pct is not None else None
    )
    distance_to_integration = (
        abs(total_return_pct - INTEGRATION_EXTRACTED_RETURN_PCT)
        if total_return_pct is not None else None
    )

    return {
        "source_path": str(source_path.relative_to(ROOT)),
        "json_path": json_path,
        "valid": True,
        "rows": len(std),
        "first_date": std[0]["date"],
        "last_date": std[-1]["date"],
        "return_pct": total_return_pct,
        "max_drawdown_pct": maxdd_pct,
        "profit_factor_daily": pf,
        "sharpe_daily": sr,
        "contains_variant_hint": contains_variant_hint,
        "distance_to_run_backtest_summary_return_pct": distance_to_summary,
        "distance_to_integration_extracted_return_pct": distance_to_integration,
        "first_row_keys": std[0]["raw_keys"],
        "last_row_keys": std[-1]["raw_keys"],
    }


def main() -> None:
    summaries: List[Dict[str, Any]] = []

    print("E1-R BASELINE SERIES ALIGNMENT AUDIT")
    print("=" * 80)
    print(f"Target variant: {TARGET_VARIANT}")
    print(f"Expected run_backtest summary return: {EXPECTED_SUMMARY_RETURN_PCT:.6f}%")
    print(f"Integration extracted return: {INTEGRATION_EXTRACTED_RETURN_PCT:.6f}%")

    for path in SEARCH_PATHS:
        rel = str(path.relative_to(ROOT))
        print(f"\nScanning: {rel}")

        if not path.exists():
            print("  MISSING")
            continue

        try:
            obj = json.loads(path.read_text())
        except Exception as exc:
            print(f"  READ ERROR: {exc}")
            continue

        series = collect_series(obj)
        print(f"  candidate daily series found: {len(series)}")

        for item in series:
            summary = summarize_series(
                source_path=path,
                json_path=item["json_path"],
                rows=item["rows"],
                contains_variant_hint=item["contains_variant_hint"],
            )
            summaries.append(summary)

    valid = [x for x in summaries if x.get("valid")]
    valid.sort(
        key=lambda x: (
            x.get("distance_to_run_backtest_summary_return_pct")
            if x.get("distance_to_run_backtest_summary_return_pct") is not None
            else 999999,
            -x.get("rows", 0),
        )
    )

    print("\n" + "=" * 80)
    print("TOP MATCHES TO run_backtest SUMMARY RETURN")
    print("=" * 80)

    for i, s in enumerate(valid[:20], start=1):
        print(f"\n#{i}")
        print(json.dumps({
            "source_path": s["source_path"],
            "json_path": s["json_path"],
            "rows": s["rows"],
            "first_date": s["first_date"],
            "last_date": s["last_date"],
            "return_pct": s["return_pct"],
            "max_drawdown_pct": s["max_drawdown_pct"],
            "profit_factor_daily": s["profit_factor_daily"],
            "sharpe_daily": s["sharpe_daily"],
            "contains_variant_hint": s["contains_variant_hint"],
            "distance_to_run_backtest_summary_return_pct": s["distance_to_run_backtest_summary_return_pct"],
            "distance_to_integration_extracted_return_pct": s["distance_to_integration_extracted_return_pct"],
            "json_path": s["json_path"],
        }, indent=2, ensure_ascii=False))

    valid_by_integration = sorted(
        valid,
        key=lambda x: (
            x.get("distance_to_integration_extracted_return_pct")
            if x.get("distance_to_integration_extracted_return_pct") is not None
            else 999999,
            -x.get("rows", 0),
        )
    )

    print("\n" + "=" * 80)
    print("TOP MATCHES TO integration EXTRACTED RETURN")
    print("=" * 80)

    for i, s in enumerate(valid_by_integration[:10], start=1):
        print(f"\n#{i}")
        print(json.dumps({
            "source_path": s["source_path"],
            "json_path": s["json_path"],
            "rows": s["rows"],
            "first_date": s["first_date"],
            "last_date": s["last_date"],
            "return_pct": s["return_pct"],
            "max_drawdown_pct": s["max_drawdown_pct"],
            "profit_factor_daily": s["profit_factor_daily"],
            "sharpe_daily": s["sharpe_daily"],
            "contains_variant_hint": s["contains_variant_hint"],
            "distance_to_run_backtest_summary_return_pct": s["distance_to_run_backtest_summary_return_pct"],
            "distance_to_integration_extracted_return_pct": s["distance_to_integration_extracted_return_pct"],
            "json_path": s["json_path"],
        }, indent=2, ensure_ascii=False))

    out_dir = ROOT / "data/research/e1_5y/audits"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "e1r_baseline_series_audit.json"
    out_path.write_text(json.dumps({
        "target_variant": TARGET_VARIANT,
        "expected_run_backtest_summary_return_pct": EXPECTED_SUMMARY_RETURN_PCT,
        "integration_extracted_return_pct": INTEGRATION_EXTRACTED_RETURN_PCT,
        "summaries": summaries,
    }, indent=2, ensure_ascii=False))

    print("\n" + "=" * 80)
    print(f"Wrote audit JSON: {out_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
