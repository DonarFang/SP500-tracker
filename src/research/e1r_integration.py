#!/usr/bin/env python3
"""
Reusable helpers for E1-R candidate integration tests.

Purpose:
- Extract baseline E1-R daily equity / daily returns from existing research outputs.
- Merge baseline daily returns with a sidecar daily return stream.
- Produce full 5Y comparison metrics.

This module does not modify the official E1-R engine.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, pstdev
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


DATE_KEYS = ("date", "timestamp", "day")
EQUITY_KEYS = ("equity", "portfolio_value", "value", "nav", "ending_equity")
RETURN_KEYS = (
    "daily_return",
    "return",
    "ret",
    "portfolio_return",
    "daily_ret",
)
RETURN_PCT_KEYS = (
    "daily_return_pct",
    "return_pct",
    "ret_pct",
    "portfolio_return_pct",
    "daily_ret_pct",
)


def safe_float(value: Any) -> Optional[float]:
    try:
        if value is None:
            return None
        x = float(value)
        if math.isnan(x) or math.isinf(x):
            return None
        return x
    except Exception:
        return None


def pct_display(value: Optional[float]) -> Optional[float]:
    return None if value is None else value * 100.0


def compound_return(returns: Iterable[Optional[float]]) -> float:
    value = 1.0
    for r in returns:
        if r is not None:
            value *= 1.0 + r
    return value - 1.0


def max_drawdown_from_returns(
    returns: Sequence[float],
    initial_equity: float = 100000.0,
) -> Tuple[float, List[float]]:
    equity = initial_equity
    curve = [equity]
    peak = equity
    max_dd = 0.0

    for r in returns:
        equity *= 1.0 + r
        curve.append(equity)
        peak = max(peak, equity)
        if peak > 0:
            max_dd = min(max_dd, equity / peak - 1.0)

    return max_dd, curve


def sharpe_ratio(returns: Sequence[float]) -> Optional[float]:
    if len(returns) < 2:
        return None

    sigma = pstdev(returns)
    if sigma == 0:
        return None

    return mean(returns) / sigma * math.sqrt(252)


def profit_factor(returns: Sequence[float]) -> Optional[float]:
    gains = sum(r for r in returns if r > 0)
    losses = -sum(r for r in returns if r < 0)

    if losses == 0:
        if gains == 0:
            return None
        return float("inf")

    return gains / losses


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def _contains_variant_key(obj: Any, variant_name: str) -> bool:
    if isinstance(obj, dict):
        if variant_name in obj:
            return True
        return any(_contains_variant_key(v, variant_name) for v in obj.values())
    if isinstance(obj, list):
        return any(_contains_variant_key(x, variant_name) for x in obj)
    return False


def _find_variant_subtrees(obj: Any, variant_name: str) -> List[Any]:
    """
    Return likely subtrees containing the requested variant.
    Supports both:
    - {"E1R_REGIME_AWARE_V0_1": {...}}
    - [{"variant": "E1R_REGIME_AWARE_V0_1", ...}]
    """
    found: List[Any] = []

    def walk(x: Any) -> None:
        if isinstance(x, dict):
            if variant_name in x:
                found.append(x[variant_name])

            variant_fields = [
                x.get("variant"),
                x.get("variant_name"),
                x.get("name"),
                x.get("strategy"),
                x.get("strategy_name"),
            ]
            if variant_name in variant_fields:
                found.append(x)

            for value in x.values():
                walk(value)

        elif isinstance(x, list):
            for item in x:
                walk(item)

    walk(obj)
    return found


def _looks_like_daily_series(rows: Any) -> bool:
    if not isinstance(rows, list) or len(rows) < 10:
        return False

    dict_rows = [x for x in rows if isinstance(x, dict)]
    if len(dict_rows) < 10:
        return False

    date_hits = 0
    value_hits = 0

    for row in dict_rows[:20]:
        if any(k in row for k in DATE_KEYS):
            date_hits += 1
        if any(k in row for k in EQUITY_KEYS + RETURN_KEYS + RETURN_PCT_KEYS):
            value_hits += 1

    return date_hits >= 5 and value_hits >= 5


def _collect_daily_series(obj: Any) -> List[List[Dict[str, Any]]]:
    series: List[List[Dict[str, Any]]] = []

    def walk(x: Any) -> None:
        if _looks_like_daily_series(x):
            series.append([row for row in x if isinstance(row, dict)])
            return

        if isinstance(x, dict):
            for value in x.values():
                walk(value)
        elif isinstance(x, list):
            for item in x:
                walk(item)

    walk(obj)
    return series


def _get_first(row: Dict[str, Any], keys: Sequence[str]) -> Any:
    for key in keys:
        if key in row:
            return row[key]
    return None


def _standardize_daily_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    records = []

    for row in rows:
        date = _get_first(row, DATE_KEYS)
        if not date:
            continue

        equity = safe_float(_get_first(row, EQUITY_KEYS))
        daily_return = safe_float(_get_first(row, RETURN_KEYS))
        daily_return_pct = safe_float(_get_first(row, RETURN_PCT_KEYS))

        if daily_return is None and daily_return_pct is not None:
            daily_return = daily_return_pct / 100.0

        records.append({
            "date": str(date)[:10],
            "equity": equity,
            "daily_return": daily_return,
            "raw": row,
        })

    records.sort(key=lambda x: x["date"])

    # If returns are missing but equity exists, derive daily returns from equity.
    if records and all(r["daily_return"] is None for r in records):
        prev_equity = None
        for record in records:
            equity = record["equity"]
            if equity is None:
                record["daily_return"] = 0.0
            elif prev_equity is None or prev_equity == 0:
                record["daily_return"] = 0.0
            else:
                record["daily_return"] = equity / prev_equity - 1.0
            prev_equity = equity

    # Drop rows that still cannot be interpreted.
    records = [
        r for r in records
        if r["daily_return"] is not None
    ]

    return records


def extract_variant_daily_returns(
    json_paths: Sequence[Path],
    variant_name: str,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Robust extractor for E1-R baseline daily return series.

    It searches likely JSON outputs and tries to find a daily series
    under the requested variant. If it fails, it returns diagnostics.
    """
    diagnostics: Dict[str, Any] = {
        "variant_name": variant_name,
        "searched_paths": [str(p) for p in json_paths],
        "existing_paths": [],
        "candidate_series": [],
    }

    best_records: List[Dict[str, Any]] = []

    for path in json_paths:
        if not path.exists():
            continue

        diagnostics["existing_paths"].append(str(path))

        try:
            root = load_json(path)
        except Exception as exc:
            diagnostics["candidate_series"].append({
                "path": str(path),
                "error": str(exc),
            })
            continue

        subtrees = _find_variant_subtrees(root, variant_name)
        if not subtrees and _contains_variant_key(root, variant_name):
            subtrees = [root]

        # Fallback: if no explicit variant subtree found, search entire file.
        search_spaces = subtrees if subtrees else [root]

        for idx, subtree in enumerate(search_spaces):
            daily_series = _collect_daily_series(subtree)

            for series_idx, rows in enumerate(daily_series):
                records = _standardize_daily_rows(rows)

                diagnostics["candidate_series"].append({
                    "path": str(path),
                    "subtree_index": idx,
                    "series_index": series_idx,
                    "rows": len(records),
                    "first_date": records[0]["date"] if records else None,
                    "last_date": records[-1]["date"] if records else None,
                    "has_equity": any(r["equity"] is not None for r in records),
                    "has_daily_return": any(r["daily_return"] is not None for r in records),
                })

                if len(records) > len(best_records):
                    best_records = records

    return best_records, diagnostics


def summarize_returns(
    name: str,
    daily_returns: Sequence[float],
    spx_returns: Sequence[float],
    initial_equity: float = 100000.0,
) -> Dict[str, Any]:
    max_dd, equity_curve = max_drawdown_from_returns(
        daily_returns,
        initial_equity=initial_equity,
    )

    total_return = compound_return(daily_returns)
    spx_return = compound_return(spx_returns)

    wins = [r for r in daily_returns if r > 0]
    losses = [r for r in daily_returns if r < 0]

    return {
        "name": name,
        "days": len(daily_returns),
        "return_pct": pct_display(total_return),
        "spx_return_pct": pct_display(spx_return),
        "alpha_vs_spx_pct": pct_display(total_return - spx_return),
        "max_drawdown_pct": pct_display(max_dd),
        "profit_factor": profit_factor(daily_returns),
        "sharpe": sharpe_ratio(daily_returns),
        "win_rate_pct": 100.0 * len(wins) / len(daily_returns) if daily_returns else None,
        "winning_days": len(wins),
        "losing_days": len(losses),
        "equity_start": initial_equity,
        "equity_end": equity_curve[-1] if equity_curve else initial_equity,
    }


def integrate_baseline_and_sidecar(
    baseline_records: Sequence[Dict[str, Any]],
    sidecar_records: Sequence[Dict[str, Any]],
    spx_records: Sequence[Dict[str, Any]],
    regimes: Dict[str, Dict[str, Any]],
    initial_equity: float = 100000.0,
) -> Dict[str, Any]:
    baseline_by_date = {
        r["date"]: r
        for r in baseline_records
    }

    sidecar_by_date = {
        r["date"]: r
        for r in sidecar_records
    }

    spx_by_date = {
        r["date"]: r
        for r in spx_records
    }

    shared_dates = sorted(
        set(baseline_by_date)
        & set(sidecar_by_date)
        & set(spx_by_date)
    )

    daily = []

    for date in shared_dates:
        baseline_return = safe_float(baseline_by_date[date].get("daily_return")) or 0.0
        sidecar_return = safe_float(sidecar_by_date[date].get("portfolio_return")) or 0.0
        spx_return = safe_float(spx_by_date[date].get("spx_return")) or 0.0

        # Conservative clean composition.
        # If baseline and sidecar overlap, this compounds them rather than simply adding.
        combined_return = (1.0 + baseline_return) * (1.0 + sidecar_return) - 1.0

        regime_info = regimes.get(date, {})
        regime = regime_info.get("regime") or "NO_REGIME"
        subclass = regime_info.get("subclass") or "NO_SUBCLASS"

        daily.append({
            "date": date,
            "regime": regime,
            "subclass": subclass,
            "baseline_return": baseline_return,
            "baseline_return_pct": pct_display(baseline_return),
            "sidecar_return": sidecar_return,
            "sidecar_return_pct": pct_display(sidecar_return),
            "combined_return": combined_return,
            "combined_return_pct": pct_display(combined_return),
            "spx_return": spx_return,
            "spx_return_pct": pct_display(spx_return),
            "sidecar_active": bool(sidecar_by_date[date].get("is_active")),
        })

    baseline_returns = [r["baseline_return"] for r in daily]
    sidecar_returns = [r["sidecar_return"] for r in daily]
    combined_returns = [r["combined_return"] for r in daily]
    spx_returns = [r["spx_return"] for r in daily]

    baseline_summary = summarize_returns(
        "E1R_REGIME_AWARE_V0_1_BASELINE",
        baseline_returns,
        spx_returns,
        initial_equity,
    )
    combined_summary = summarize_returns(
        "E1R_V0_2_CANDIDATE_S4",
        combined_returns,
        spx_returns,
        initial_equity,
    )
    sidecar_summary = summarize_returns(
        "S4_MA_CONFLICT_TOP10_QUARTER_SIDECAR_ONLY",
        sidecar_returns,
        spx_returns,
        initial_equity,
    )

    regime_counts = Counter(r["regime"] for r in daily)
    sidecar_active_by_regime = Counter(
        r["regime"] for r in daily if r["sidecar_active"]
    )
    sidecar_active_by_subclass = Counter(
        r["subclass"] for r in daily if r["sidecar_active"]
    )

    contribution_by_regime = defaultdict(float)
    contribution_by_subclass = defaultdict(float)

    for r in daily:
        contribution_by_regime[r["regime"]] += r["sidecar_return"]
        contribution_by_subclass[r["subclass"]] += r["sidecar_return"]

    delta = {
        "return_delta_pct": (
            combined_summary["return_pct"] - baseline_summary["return_pct"]
            if combined_summary["return_pct"] is not None
            and baseline_summary["return_pct"] is not None
            else None
        ),
        "alpha_delta_pct": (
            combined_summary["alpha_vs_spx_pct"] - baseline_summary["alpha_vs_spx_pct"]
            if combined_summary["alpha_vs_spx_pct"] is not None
            and baseline_summary["alpha_vs_spx_pct"] is not None
            else None
        ),
        "maxdd_delta_pct": (
            combined_summary["max_drawdown_pct"] - baseline_summary["max_drawdown_pct"]
            if combined_summary["max_drawdown_pct"] is not None
            and baseline_summary["max_drawdown_pct"] is not None
            else None
        ),
        "pf_delta": (
            combined_summary["profit_factor"] - baseline_summary["profit_factor"]
            if combined_summary["profit_factor"] is not None
            and baseline_summary["profit_factor"] is not None
            and not math.isinf(combined_summary["profit_factor"])
            and not math.isinf(baseline_summary["profit_factor"])
            else None
        ),
        "sharpe_delta": (
            combined_summary["sharpe"] - baseline_summary["sharpe"]
            if combined_summary["sharpe"] is not None
            and baseline_summary["sharpe"] is not None
            else None
        ),
    }

    pass_fail = {
        "return_improvement_ge_5pct": (
            delta["return_delta_pct"] is not None
            and delta["return_delta_pct"] >= 5.0
        ),
        "maxdd_increase_le_2pct": (
            delta["maxdd_delta_pct"] is not None
            and delta["maxdd_delta_pct"] >= -2.0
        ),
        "downdtrend_sidecar_exposure_zero": (
            sidecar_active_by_regime.get("DOWNTREND", 0) == 0
        ),
        "sideways_ma_conflict_only": (
            set(sidecar_active_by_subclass.keys()).issubset({"MA_CONFLICT"})
        ),
        "sideways_sidecar_contribution_positive": (
            contribution_by_regime.get("SIDEWAYS", 0.0) > 0
        ),
    }

    return {
        "shared_days": len(shared_dates),
        "first_date": shared_dates[0] if shared_dates else None,
        "last_date": shared_dates[-1] if shared_dates else None,
        "regime_counts": dict(regime_counts),
        "sidecar_active_by_regime": dict(sidecar_active_by_regime),
        "sidecar_active_by_subclass": dict(sidecar_active_by_subclass),
        "sidecar_simple_contribution_by_regime_pct": {
            k: pct_display(v)
            for k, v in contribution_by_regime.items()
        },
        "sidecar_simple_contribution_by_subclass_pct": {
            k: pct_display(v)
            for k, v in contribution_by_subclass.items()
        },
        "baseline_summary": baseline_summary,
        "sidecar_summary": sidecar_summary,
        "combined_summary": combined_summary,
        "delta_vs_baseline": delta,
        "pass_fail": pass_fail,
        "daily_sample": {
            "first_5": daily[:5],
            "last_5": daily[-5:],
        },
        "daily": daily,
    }


def extract_by_json_path(obj: Any, json_path: str) -> Any:
    """
    Minimal JSON path extractor for dot paths like:
    $.backtest.results.layer_d.variant_results.E1R_REGIME_AWARE_V0_1.daily_equity_records

    Supports dict-only paths, which is enough for our canonical backtest outputs.
    """
    if not json_path.startswith("$."):
        raise ValueError(f"Unsupported json_path: {json_path}")

    cur = obj
    for part in json_path[2:].split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(f"Path segment not found: {part} in {json_path}")
        cur = cur[part]

    return cur


def load_canonical_baseline_daily_equity(
    path: Path,
    json_path: str,
) -> List[Dict[str, Any]]:
    """
    Load the explicitly selected E1-R baseline daily equity records.
    No fuzzy matching.
    """
    obj = load_json(path)
    rows = extract_by_json_path(obj, json_path)

    if not isinstance(rows, list):
        raise TypeError(f"Canonical baseline path does not point to a list: {json_path}")

    records = _standardize_daily_rows([r for r in rows if isinstance(r, dict)])

    if len(records) < 500:
        raise ValueError(
            f"Canonical baseline series too short: rows={len(records)} path={json_path}"
        )

    return records


def align_baseline_returns_to_intervals(
    baseline_records: Sequence[Dict[str, Any]],
    intervals: Sequence[Tuple[str, str]],
) -> List[Dict[str, Any]]:
    """
    Convert baseline daily equity returns into interval-aligned records.

    Baseline daily return dated next_date means:
      previous trading day close -> next_date close

    Sidecar return dated date means:
      date close -> next_date close

    Therefore for interval (date, next_date), use baseline_records[next_date].
    """
    baseline_by_end_date = {
        r["date"]: r
        for r in baseline_records
        if r.get("daily_return") is not None
    }

    aligned = []

    for date, next_date in intervals:
        src = baseline_by_end_date.get(next_date)
        if src is None:
            continue

        aligned.append({
            "date": date,
            "next_date": next_date,
            "baseline_end_date": next_date,
            "daily_return": safe_float(src.get("daily_return")) or 0.0,
            "equity": safe_float(src.get("equity")),
            "raw": src.get("raw", src),
        })

    return aligned


def integrate_aligned_baseline_and_sidecar(
    baseline_interval_records: Sequence[Dict[str, Any]],
    sidecar_records: Sequence[Dict[str, Any]],
    spx_records: Sequence[Dict[str, Any]],
    regimes: Dict[str, Dict[str, Any]],
    initial_equity: float = 100000.0,
) -> Dict[str, Any]:
    """
    Correct integration:
    - baseline records are already interval-aligned by date/next_date.
    - sidecar records use the same date/next_date interval.
    - spx records use the same date/next_date interval.
    """
    baseline_by_interval = {
        (r["date"], r["next_date"]): r
        for r in baseline_interval_records
    }
    sidecar_by_interval = {
        (r["date"], r["next_date"]): r
        for r in sidecar_records
    }
    spx_by_interval = {
        (r["date"], r["next_date"]): r
        for r in spx_records
    }

    shared_keys = sorted(
        set(baseline_by_interval)
        & set(sidecar_by_interval)
        & set(spx_by_interval)
    )

    daily = []

    for date, next_date in shared_keys:
        baseline = baseline_by_interval[(date, next_date)]
        sidecar = sidecar_by_interval[(date, next_date)]
        spx = spx_by_interval[(date, next_date)]

        baseline_return = safe_float(baseline.get("daily_return")) or 0.0
        sidecar_return = safe_float(sidecar.get("portfolio_return")) or 0.0
        spx_return = safe_float(spx.get("spx_return")) or 0.0

        combined_return = (1.0 + baseline_return) * (1.0 + sidecar_return) - 1.0

        regime_info = regimes.get(date, {})
        regime = regime_info.get("regime") or "NO_REGIME"
        subclass = regime_info.get("subclass") or "NO_SUBCLASS"

        daily.append({
            "date": date,
            "next_date": next_date,
            "baseline_end_date": baseline.get("baseline_end_date"),
            "regime": regime,
            "subclass": subclass,
            "baseline_return": baseline_return,
            "baseline_return_pct": pct_display(baseline_return),
            "sidecar_return": sidecar_return,
            "sidecar_return_pct": pct_display(sidecar_return),
            "combined_return": combined_return,
            "combined_return_pct": pct_display(combined_return),
            "spx_return": spx_return,
            "spx_return_pct": pct_display(spx_return),
            "sidecar_active": bool(sidecar.get("is_active")),
        })

    baseline_returns = [r["baseline_return"] for r in daily]
    sidecar_returns = [r["sidecar_return"] for r in daily]
    combined_returns = [r["combined_return"] for r in daily]
    spx_returns = [r["spx_return"] for r in daily]

    baseline_summary = summarize_returns(
        "E1R_REGIME_AWARE_V0_1_BASELINE_INTERVAL_ALIGNED",
        baseline_returns,
        spx_returns,
        initial_equity,
    )
    combined_summary = summarize_returns(
        "E1R_V0_2_CANDIDATE_S4_INTERVAL_ALIGNED",
        combined_returns,
        spx_returns,
        initial_equity,
    )
    sidecar_summary = summarize_returns(
        "S4_MA_CONFLICT_TOP10_QUARTER_SIDECAR_ONLY",
        sidecar_returns,
        spx_returns,
        initial_equity,
    )

    regime_counts = Counter(r["regime"] for r in daily)
    sidecar_active_by_regime = Counter(r["regime"] for r in daily if r["sidecar_active"])
    sidecar_active_by_subclass = Counter(r["subclass"] for r in daily if r["sidecar_active"])

    contribution_by_regime = defaultdict(float)
    contribution_by_subclass = defaultdict(float)

    for r in daily:
        contribution_by_regime[r["regime"]] += r["sidecar_return"]
        contribution_by_subclass[r["subclass"]] += r["sidecar_return"]

    delta = {
        "return_delta_pct": (
            combined_summary["return_pct"] - baseline_summary["return_pct"]
            if combined_summary["return_pct"] is not None
            and baseline_summary["return_pct"] is not None
            else None
        ),
        "alpha_delta_pct": (
            combined_summary["alpha_vs_spx_pct"] - baseline_summary["alpha_vs_spx_pct"]
            if combined_summary["alpha_vs_spx_pct"] is not None
            and baseline_summary["alpha_vs_spx_pct"] is not None
            else None
        ),
        "maxdd_delta_pct": (
            combined_summary["max_drawdown_pct"] - baseline_summary["max_drawdown_pct"]
            if combined_summary["max_drawdown_pct"] is not None
            and baseline_summary["max_drawdown_pct"] is not None
            else None
        ),
        "pf_delta": (
            combined_summary["profit_factor"] - baseline_summary["profit_factor"]
            if combined_summary["profit_factor"] is not None
            and baseline_summary["profit_factor"] is not None
            and not math.isinf(combined_summary["profit_factor"])
            and not math.isinf(baseline_summary["profit_factor"])
            else None
        ),
        "sharpe_delta": (
            combined_summary["sharpe"] - baseline_summary["sharpe"]
            if combined_summary["sharpe"] is not None
            and baseline_summary["sharpe"] is not None
            else None
        ),
    }

    pass_fail = {
        "return_improvement_ge_5pct": (
            delta["return_delta_pct"] is not None
            and delta["return_delta_pct"] >= 5.0
        ),
        "maxdd_increase_le_2pct": (
            delta["maxdd_delta_pct"] is not None
            and delta["maxdd_delta_pct"] >= -2.0
        ),
        "downdtrend_sidecar_exposure_zero": (
            sidecar_active_by_regime.get("DOWNTREND", 0) == 0
        ),
        "sideways_ma_conflict_only": (
            set(sidecar_active_by_subclass.keys()).issubset({"MA_CONFLICT"})
        ),
        "sideways_sidecar_contribution_positive": (
            contribution_by_regime.get("SIDEWAYS", 0.0) > 0
        ),
    }

    return {
        "alignment": "interval_aligned_baseline_by_next_date",
        "shared_intervals": len(shared_keys),
        "first_interval": {
            "date": shared_keys[0][0],
            "next_date": shared_keys[0][1],
        } if shared_keys else None,
        "last_interval": {
            "date": shared_keys[-1][0],
            "next_date": shared_keys[-1][1],
        } if shared_keys else None,
        "regime_counts": dict(regime_counts),
        "sidecar_active_by_regime": dict(sidecar_active_by_regime),
        "sidecar_active_by_subclass": dict(sidecar_active_by_subclass),
        "sidecar_simple_contribution_by_regime_pct": {
            k: pct_display(v)
            for k, v in contribution_by_regime.items()
        },
        "sidecar_simple_contribution_by_subclass_pct": {
            k: pct_display(v)
            for k, v in contribution_by_subclass.items()
        },
        "baseline_summary": baseline_summary,
        "sidecar_summary": sidecar_summary,
        "combined_summary": combined_summary,
        "delta_vs_baseline": delta,
        "pass_fail": pass_fail,
        "daily_sample": {
            "first_5": daily[:5],
            "last_5": daily[-5:],
        },
        "daily": daily,
    }
