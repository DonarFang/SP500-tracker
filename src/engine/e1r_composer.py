"""
E1-R portfolio composer.

Composes:
- E1R_REGIME_AWARE_V0_1 core daily equity records
- E1R sidecar sleeve daily return records

into:
- E1R_REGIME_AWARE_V0_2 formal combined daily equity records

Alignment rule
--------------
Core daily equity record date means:
    previous trading day close -> date close

Sidecar sleeve record date/next_date means:
    date close -> next_date close

Therefore, for sidecar interval (date -> next_date), use core daily return
ending at next_date.
"""

from __future__ import annotations

import copy
import math
from statistics import mean, pstdev
from typing import Any, Optional, Sequence


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


def pct_display(decimal_return: Optional[float]) -> Optional[float]:
    return None if decimal_return is None else decimal_return * 100.0


def compound_return(returns: Sequence[Optional[float]]) -> float:
    value = 1.0
    for r in returns:
        if r is not None:
            value *= 1.0 + r
    return value - 1.0


def max_drawdown(equity_values: Sequence[float]) -> Optional[float]:
    if not equity_values:
        return None

    peak = equity_values[0]
    worst = 0.0

    for value in equity_values:
        peak = max(peak, value)
        if peak > 0:
            worst = min(worst, value / peak - 1.0)

    return worst


def sharpe_ratio(daily_returns: Sequence[float]) -> Optional[float]:
    values = [x for x in daily_returns if x is not None]
    if len(values) < 2:
        return None

    sigma = pstdev(values)
    if sigma == 0:
        return None

    return mean(values) / sigma * math.sqrt(252)


def profit_factor(daily_returns: Sequence[float]) -> Optional[float]:
    gains = sum(x for x in daily_returns if x is not None and x > 0)
    losses = -sum(x for x in daily_returns if x is not None and x < 0)

    if losses == 0:
        if gains == 0:
            return None
        return float("inf")

    return gains / losses


def extract_core_interval_returns(
    core_daily_equity_records: Sequence[dict[str, Any]],
    sidecar_records: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Align core daily returns to sidecar intervals by next_date.

    Returns one record per shared interval:
    {
      date,
      next_date,
      core_return,
      sidecar_return,
      spx_return,
      ...
    }
    """
    core_by_end_date = {}

    for row in core_daily_equity_records:
        date = row.get("date")
        if not date:
            continue

        r = safe_float(row.get("daily_return"))
        if r is None:
            # Some historical outputs may store pct instead of decimal.
            rp = safe_float(row.get("daily_return_pct"))
            r = None if rp is None else rp / 100.0

        if r is None:
            continue

        core_by_end_date[date] = row | {"_normalized_daily_return": r}

    aligned: list[dict[str, Any]] = []

    for sidecar in sidecar_records:
        date = sidecar.get("date")
        next_date = sidecar.get("next_date")

        if not date or not next_date:
            continue

        core = core_by_end_date.get(next_date)
        if core is None:
            continue

        core_return = safe_float(core.get("_normalized_daily_return")) or 0.0
        sidecar_return = safe_float(sidecar.get("portfolio_return")) or 0.0
        spx_return = safe_float(sidecar.get("spx_return")) or 0.0

        combined_return = (1.0 + core_return) * (1.0 + sidecar_return) - 1.0

        aligned.append({
            "date": date,
            "next_date": next_date,
            "core_end_date": next_date,
            "core_return": core_return,
            "core_return_pct": pct_display(core_return),
            "sidecar_return": sidecar_return,
            "sidecar_return_pct": pct_display(sidecar_return),
            "combined_return": combined_return,
            "combined_return_pct": pct_display(combined_return),
            "spx_return": spx_return,
            "spx_return_pct": pct_display(spx_return),
            "regime": sidecar.get("regime"),
            "subclass": sidecar.get("subclass"),
            "sidecar_active": bool(sidecar.get("is_active")),
            "sidecar_selected_count": sidecar.get("selected_count"),
            "sidecar_gross_exposure": sidecar.get("gross_exposure"),
            "sidecar_holdings": sidecar.get("holdings", []),
        })

    return aligned


def build_equity_records_from_returns(
    interval_records: Sequence[dict[str, Any]],
    initial_equity: float,
) -> list[dict[str, Any]]:
    equity = initial_equity
    peak = initial_equity
    records: list[dict[str, Any]] = []

    for row in interval_records:
        r = safe_float(row.get("combined_return")) or 0.0
        equity *= 1.0 + r
        peak = max(peak, equity)

        drawdown = equity / peak - 1.0 if peak > 0 else 0.0

        records.append({
            "date": row["next_date"],
            "interval_start_date": row["date"],
            "interval_end_date": row["next_date"],
            "total_equity": equity,
            "equity": equity,
            "daily_return": r,
            "daily_return_pct": pct_display(r),
            "drawdown": drawdown,
            "drawdown_pct": pct_display(drawdown),

            "core_return": row["core_return"],
            "core_return_pct": row["core_return_pct"],
            "sidecar_return": row["sidecar_return"],
            "sidecar_return_pct": row["sidecar_return_pct"],
            "spx_return": row["spx_return"],
            "spx_return_pct": row["spx_return_pct"],

            "spx_regime": row.get("regime"),
            "sideways_subclass": row.get("subclass"),
            "sidecar_active": row.get("sidecar_active"),
            "sidecar_selected_count": row.get("sidecar_selected_count"),
            "sidecar_gross_exposure": row.get("sidecar_gross_exposure"),
        })

    return records


def summarize_combined_variant(
    interval_records: Sequence[dict[str, Any]],
    equity_records: Sequence[dict[str, Any]],
    initial_equity: float,
) -> dict[str, Any]:
    combined_returns = [safe_float(r.get("combined_return")) or 0.0 for r in interval_records]
    core_returns = [safe_float(r.get("core_return")) or 0.0 for r in interval_records]
    sidecar_returns = [safe_float(r.get("sidecar_return")) or 0.0 for r in interval_records]
    spx_returns = [safe_float(r.get("spx_return")) or 0.0 for r in interval_records]

    equity_curve = [initial_equity] + [
        safe_float(r.get("equity")) or initial_equity for r in equity_records
    ]

    total_return = compound_return(combined_returns)
    core_return = compound_return(core_returns)
    sidecar_return = compound_return(sidecar_returns)
    spx_return = compound_return(spx_returns)

    active_records = [r for r in interval_records if r.get("sidecar_active")]

    active_by_regime: dict[str, int] = {}
    active_by_subclass: dict[str, int] = {}
    contribution_by_regime: dict[str, float] = {}
    contribution_by_subclass: dict[str, float] = {}

    for row in interval_records:
        regime = row.get("regime") or "NO_REGIME"
        subclass = row.get("subclass") or "NO_SUBCLASS"
        sidecar_return_row = safe_float(row.get("sidecar_return")) or 0.0

        contribution_by_regime[regime] = contribution_by_regime.get(regime, 0.0) + sidecar_return_row
        contribution_by_subclass[subclass] = contribution_by_subclass.get(subclass, 0.0) + sidecar_return_row

        if row.get("sidecar_active"):
            active_by_regime[regime] = active_by_regime.get(regime, 0) + 1
            active_by_subclass[subclass] = active_by_subclass.get(subclass, 0) + 1

    return {
        "total_return_pct": pct_display(total_return),
        "core_return_pct": pct_display(core_return),
        "sidecar_return_pct": pct_display(sidecar_return),
        "spx_return_pct": pct_display(spx_return),
        "alpha_pct": pct_display(total_return - spx_return),
        # Match legacy engine convention:
        # max_drawdown_pct is reported as positive magnitude, e.g. 25.90 not -25.90.
        "max_drawdown_pct": abs(pct_display(max_drawdown(equity_curve)) or 0.0),
        "profit_factor": profit_factor(combined_returns),
        "sharpe_ratio": sharpe_ratio(combined_returns),
        "daily_win_rate_pct": (
            100.0 * sum(1 for r in combined_returns if r > 0) / len(combined_returns)
            if combined_returns else None
        ),
        "total_days": len(interval_records),
        "daily_equity_record_count": len(equity_records),
        "sidecar_active_days": len(active_records),
        "sidecar_active_by_regime": active_by_regime,
        "sidecar_active_by_subclass": active_by_subclass,
        "sidecar_simple_contribution_by_regime_pct": {
            k: pct_display(v)
            for k, v in contribution_by_regime.items()
        },
        "sidecar_simple_contribution_by_subclass_pct": {
            k: pct_display(v)
            for k, v in contribution_by_subclass.items()
        },
    }


def compose_e1r_v0_2_variant(
    core_variant_result: dict[str, Any],
    sidecar_result: dict[str, Any],
    initial_equity: float = 100000.0,
) -> dict[str, Any]:
    core_records = core_variant_result.get("daily_equity_records", [])
    sidecar_records = sidecar_result.get("records", [])

    interval_records = extract_core_interval_returns(core_records, sidecar_records)
    equity_records = build_equity_records_from_returns(interval_records, initial_equity)
    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)

    result = copy.deepcopy(core_variant_result)

    sidecar_summary = sidecar_result.get("summary", {}) or {}

    result.update({
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "strategy_variant": "E1R_regime_aware_v0_2_formal_sidecar_sleeve",
        "version": "E1R-v0.2-formal-sidecar-sleeve",
        "research_status": "FORMAL_SIDECAR_SLEEVE_ENGINE",
        "core_total_trades": core_variant_result.get("total_trades"),
        "sidecar_trade_count_approx": sidecar_summary.get("trade_count_approx"),
        "combined_trade_count_note": (
            "total_trades remains inherited from E1R v0.1 core; "
            "sidecar_trade_count_approx counts daily basket holdings and is not "
            "stateful round-trip trade count."
        ),
        "e1r_v0_2_composition": {
            "core_variant": "E1R_REGIME_AWARE_V0_1",
            "sidecar_engine": sidecar_result.get("engine"),
            "sidecar_version": sidecar_result.get("version"),
            "alignment": "core daily return ending at next_date aligned to sidecar date->next_date interval",
            "composition_formula": "(1 + core_return) * (1 + sidecar_return) - 1",
            "sidecar_config": sidecar_result.get("config", {}),
            "sidecar_sample": sidecar_result.get("sample", {}),
            "sidecar_summary": sidecar_result.get("summary", {}),
            "combined_summary": summary,
        },
        "daily_equity_records": equity_records,
        "daily_equity_record_count": len(equity_records),
        "e1r_v0_2_interval_records_sample": {
            "first_5": interval_records[:5],
            "last_5": interval_records[-5:],
        },
    })

    # Override summary-level fields with formal combined values.
    for key in (
        "total_return_pct",
        "spx_return_pct",
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
    ):
        if key in summary:
            result[key] = summary[key]

    result["total_days"] = summary["total_days"]
    result["sidecar_active_days"] = summary["sidecar_active_days"]
    result["sidecar_active_by_regime"] = summary["sidecar_active_by_regime"]
    result["sidecar_active_by_subclass"] = summary["sidecar_active_by_subclass"]
    result["sidecar_simple_contribution_by_regime_pct"] = summary["sidecar_simple_contribution_by_regime_pct"]
    result["sidecar_simple_contribution_by_subclass_pct"] = summary["sidecar_simple_contribution_by_subclass_pct"]

    result.setdefault("strategy_controls", {})
    result["strategy_controls"].update({
        "regime_aware_logic": "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
        "e1r_v0_2_formal_sidecar_sleeve": True,
        "e1r_v0_2_core_variant": "E1R_REGIME_AWARE_V0_1",
        "e1r_v0_2_sidecar_allowed_subclasses": sidecar_result.get("config", {}).get("allowed_subclasses"),
        "e1r_v0_2_sidecar_top_n": sidecar_result.get("config", {}).get("top_n"),
        "e1r_v0_2_sidecar_gross_exposure": sidecar_result.get("config", {}).get("gross_exposure"),
        "e1r_v0_2_excluded_symbols": sidecar_result.get("config", {}).get("excluded_symbols"),
    })

    return result
