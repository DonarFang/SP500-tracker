#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import math
from datetime import datetime, timezone
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

RESULT = ROOT / "exports/e1r_unified_5y_full_account_v1_result.json"
CURVE_RAW = ROOT / "exports/e1r_unified_5y_full_account_v1_equity_curve.json"
SUMMARY_RAW = ROOT / "exports/e1r_unified_5y_full_account_v1_summary.json"
AUDIT = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C1_METRIC_CONSISTENCY_AUDIT.json"

OUT_CURVE = ROOT / "exports/e1r_unified_5y_full_account_v1_row_derived_equity_curve.json"
OUT_SUMMARY = ROOT / "exports/e1r_unified_5y_full_account_v1_row_derived_summary.json"

REPORT_JSON = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C2_ROW_DERIVED_METRICS_REPORT.json"
REPORT_MD = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C2_ROW_DERIVED_METRICS_REPORT.md"

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))

def read_json(p: Path):
    return json.loads(p.read_text())

def write_json(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def safe_float(x):
    try:
        if x is None:
            return None
        return float(x)
    except Exception:
        return None

def max_drawdown(rows):
    peak = None
    maxdd = 0.0
    for r in rows:
        eq = safe_float(r.get("total_equity"))
        if eq is None:
            continue
        if peak is None or eq > peak:
            peak = eq
        if peak and peak > 0:
            dd = (peak - eq) / peak * 100.0
            maxdd = max(maxdd, dd)
    return maxdd

def daily_returns(rows):
    out = []
    prev = None
    for r in rows:
        eq = safe_float(r.get("total_equity"))
        if eq is None:
            continue
        if prev is not None and prev > 0:
            out.append(eq / prev - 1.0)
        prev = eq
    return out

def sharpe_from_daily(rows):
    rets = daily_returns(rows)
    if len(rets) < 2:
        return None
    mean = sum(rets) / len(rets)
    var = sum((x - mean) ** 2 for x in rets) / (len(rets) - 1)
    std = math.sqrt(var)
    if std == 0:
        return None
    return mean / std * math.sqrt(252)

def cagr(first_eq, last_eq, row_count):
    if not first_eq or not last_eq or row_count <= 1:
        return None
    years = row_count / 252.0
    return ((last_eq / first_eq) ** (1.0 / years) - 1.0) * 100.0

def annualized_vol(rows):
    rets = daily_returns(rows)
    if len(rets) < 2:
        return None
    mean = sum(rets) / len(rets)
    var = sum((x - mean) ** 2 for x in rets) / (len(rets) - 1)
    return math.sqrt(var) * math.sqrt(252) * 100.0

def normalize_rows(result):
    records = result.get("daily_equity_records") or []
    if not records:
        raise RuntimeError("missing daily_equity_records")

    first_eq = safe_float(records[0].get("total_equity"))
    if not first_eq:
        raise RuntimeError("invalid first total_equity")

    rows = []
    prev_eq = None

    for r in records:
        eq = safe_float(r.get("total_equity"))
        cash = safe_float(r.get("cash"))
        pos = safe_float(r.get("positions_value"))
        daily_ret = None
        if prev_eq and eq is not None:
            daily_ret = (eq / prev_eq - 1.0) * 100.0

        rows.append({
            "date": r.get("date"),
            "total_equity": eq,
            "indexed_100": eq / first_eq * 100.0 if eq is not None else None,
            "cash": cash,
            "positions_value": pos,
            "cash_plus_positions": (cash + pos) if cash is not None and pos is not None else None,
            "daily_return_pct_recomputed": daily_ret,
            "drawdown_pct": r.get("drawdown_pct"),
            "exposure_pct": r.get("exposure_pct"),
            "open_positions_count": r.get("open_positions_count"),
            "pending_orders_count": r.get("pending_orders_count"),
            "market_gate_state": r.get("market_gate_state"),
            "spx_regime": r.get("spx_regime"),
            "e1r_active_mode": r.get("e1r_active_mode"),
            "risk_budget_mode": r.get("risk_budget_mode"),
            "risk_budget": r.get("risk_budget"),
            "spx_close": r.get("spx_close"),
            "spx_ma50": r.get("spx_ma50"),
            "spx_day_return_pct": r.get("spx_day_return_pct"),
            "event": r.get("event"),
        })

        prev_eq = eq

    return rows

def summarize_rows(rows, raw_result):
    first = rows[0]
    last = rows[-1]
    first_eq = safe_float(first["total_equity"])
    last_eq = safe_float(last["total_equity"])

    total_return_pct = (last_eq / first_eq - 1.0) * 100.0
    spx_total_return_pct = safe_float(raw_result.get("spx_total_return_pct"))
    alpha_pct = total_return_pct - spx_total_return_pct if spx_total_return_pct is not None else None

    regimes = Counter(r.get("spx_regime") for r in rows)
    modes = Counter(r.get("e1r_active_mode") for r in rows)
    risk_modes = Counter(r.get("risk_budget_mode") for r in rows)

    dates = [r.get("date") for r in rows]
    date_counts = Counter(dates)

    continuity_breaks = []
    for r in rows:
        total = safe_float(r.get("total_equity"))
        cp = safe_float(r.get("cash_plus_positions"))
        if total is None or cp is None:
            continue
        if abs(total - cp) / max(abs(total), 1.0) > 0.0001:
            continuity_breaks.append({
                "date": r.get("date"),
                "total_equity": total,
                "cash_plus_positions": cp,
                "diff": abs(total - cp),
            })

    return {
        "metric_source": "daily_equity_records.total_equity",
        "reported_engine_metrics_status": "REJECTED_FOR_OFFICIAL_USE_METRIC_LAYER_USED_CASH_AS_FINAL_EQUITY",
        "trade_metrics_status": "NOT_VALIDATED_SIM_END_EFFECTIVE_EXIT_ZERO_RETURN_MINUS_100",
        "first_date": first.get("date"),
        "last_date": last.get("date"),
        "row_count": len(rows),
        "unique_dates": len(set(dates)),
        "one_row_per_date": max(date_counts.values()) == 1 if date_counts else False,
        "first_equity": first_eq,
        "last_equity": last_eq,
        "total_return_pct": total_return_pct,
        "spx_total_return_pct": spx_total_return_pct,
        "alpha_pct": alpha_pct,
        "cagr_pct": cagr(first_eq, last_eq, len(rows)),
        "max_drawdown_pct": max_drawdown(rows),
        "sharpe_ratio_row_derived": sharpe_from_daily(rows),
        "annualized_vol_pct_row_derived": annualized_vol(rows),
        "final_cash": last.get("cash"),
        "final_positions_value": last.get("positions_value"),
        "final_cash_plus_positions": last.get("cash_plus_positions"),
        "final_exposure_pct": last.get("exposure_pct"),
        "regime_counts": {str(k): v for k, v in regimes.items()},
        "active_mode_counts": {str(k): v for k, v in modes.items()},
        "risk_budget_mode_counts": {str(k): v for k, v in risk_modes.items()},
        "cash_plus_positions_break_count": len(continuity_breaks),
        "cash_plus_positions_break_samples": continuity_breaks[:10],
    }

def audit_trade_layer(raw_result):
    trades = raw_result.get("trades") or []
    exit_counter = Counter()
    return_counter = Counter()
    effective_exit_counter = Counter()

    suspicious = []

    for t in trades:
        if not isinstance(t, dict):
            continue
        exit_counter[t.get("exit_signal") or t.get("exit_type")] += 1
        return_counter[str(t.get("return_pct"))] += 1
        effective_exit_counter[str(t.get("effective_exit"))] += 1

        if t.get("is_sim_end") is True and safe_float(t.get("effective_exit")) == 0.0:
            suspicious.append({
                "symbol": t.get("symbol"),
                "entry_date": t.get("entry_date"),
                "exit_date": t.get("exit_date"),
                "entry_price": t.get("entry_price"),
                "avg_cost": t.get("avg_cost"),
                "exit_price": t.get("exit_price"),
                "effective_exit": t.get("effective_exit"),
                "return_pct": t.get("return_pct"),
                "is_sim_end": t.get("is_sim_end"),
                "exit_signal": t.get("exit_signal"),
                "exit_type": t.get("exit_type"),
            })

    return {
        "trade_count": len(trades),
        "exit_counter": dict(exit_counter),
        "return_counter": dict(return_counter),
        "effective_exit_counter": dict(effective_exit_counter),
        "sim_end_effective_exit_zero_count": len(suspicious),
        "suspicious_samples": suspicious[:20],
    }

def main():
    raw_result = read_json(RESULT)
    raw_summary = read_json(SUMMARY_RAW)
    audit = read_json(AUDIT)

    rows = normalize_rows(raw_result)
    row_metrics = summarize_rows(rows, raw_result)
    trade_audit = audit_trade_layer(raw_result)

    curve = {
        "artifact_type": "e1r_unified_5y_full_account_v1_row_derived_equity_curve",
        "generated_at": now(),
        "status": "ROW_DERIVED_EQUITY_CURVE_VALIDATED",
        "strategy_id": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1",
        "source_result": rel(RESULT),
        "metric_source": "daily_equity_records.total_equity",
        "warning": "Engine reported metrics are rejected for official use because they used cash as final_equity. Trade metrics are not validated because SIM_END effective_exit is zero.",
        "metrics": row_metrics,
        "rows": rows,
    }

    summary = {
        "artifact_type": "e1r_unified_5y_full_account_v1_row_derived_summary",
        "generated_at": now(),
        "status": "ROW_DERIVED_ACCOUNT_METRICS_VALIDATED_TRADE_METRICS_NOT_VALIDATED",
        "strategy_id": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1",
        "source_result": rel(RESULT),
        "source_raw_summary": rel(SUMMARY_RAW),
        "source_metric_audit": rel(AUDIT),
        "row_derived_metrics": row_metrics,
        "engine_reported_metrics_rejected": audit.get("reported_metrics"),
        "metric_consistency_diagnosis": audit.get("diagnosis"),
        "trade_layer_audit": trade_audit,
        "sample_validity_from_engine": raw_result.get("sample_validity"),
        "validation": {
            "row_count_ge_1000": row_metrics["row_count"] >= 1000,
            "one_row_per_date": row_metrics["one_row_per_date"],
            "cash_plus_positions_continuity_ok": row_metrics["cash_plus_positions_break_count"] == 0,
            "regime_wired": all(v > 0 for k, v in row_metrics["regime_counts"].items() if k != "None"),
            "covers_uptrend": row_metrics["regime_counts"].get("UPTREND", 0) > 0,
            "covers_sideways": row_metrics["regime_counts"].get("SIDEWAYS", 0) > 0,
            "covers_downtrend": row_metrics["regime_counts"].get("DOWNTREND", 0) > 0,
            "reported_engine_metrics_rejected": True,
            "trade_metrics_not_validated": True,
        },
        "next_action": "Use row-derived equity curve for account-level research display only. Do not use engine-reported metrics or trade-level metrics until SIM_END/effective_exit contract is fixed.",
    }

    write_json(OUT_CURVE, curve)
    write_json(OUT_SUMMARY, summary)

    report = {
        "generated_at": now(),
        "stage": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C2_ROW_DERIVED_METRICS",
        "status": "ROW_DERIVED_METRICS_RECOMPUTED_FROM_DAILY_EQUITY",
        "outputs": {
            "curve": rel(OUT_CURVE),
            "summary": rel(OUT_SUMMARY),
        },
        "row_derived_metrics": row_metrics,
        "engine_reported_metrics_rejected": audit.get("reported_metrics"),
        "trade_layer_audit": trade_audit,
        "validation": summary["validation"],
        "conclusion": "ACCOUNT_LEVEL_ROW_DERIVED_CURVE_USABLE_FOR_RESEARCH_DISPLAY_ONLY",
        "recommended_next_action": "Patch dashboard/research labels to use row-derived metrics only; separately fix engine SIM_END/effective_exit trade contract before any trade-level claims.",
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R Unified 5Y Full Account V1 — 4C-2C-2 Row-Derived Metrics")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{report['conclusion']}`")
    md.append(f"- Recommended: {report['recommended_next_action']}")
    md.append("")
    md.append("## Row-Derived Metrics")
    md.append("")
    md.append("```json")
    md.append(json.dumps(row_metrics, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Engine Metrics Rejected")
    md.append("")
    md.append("```json")
    md.append(json.dumps(audit.get("reported_metrics"), indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Trade Layer Audit")
    md.append("")
    md.append("```json")
    md.append(json.dumps(trade_audit, indent=2, ensure_ascii=False)[:20000])
    md.append("```")
    REPORT_MD.write_text("\n".join(md) + "\n")

    print("E1R_UNIFIED_5Y_FULL_ACCOUNT_4C2C2_ROW_DERIVED_COMPLETE")
    print("outputs:", json.dumps(report["outputs"], ensure_ascii=False))
    print("row_derived_metrics:", json.dumps(row_metrics, ensure_ascii=False))
    print("validation:", json.dumps(summary["validation"], ensure_ascii=False))
    print("trade_layer_audit:", json.dumps(trade_audit, ensure_ascii=False)[:8000])
    print("conclusion:", report["conclusion"])
    print("recommended_next_action:", report["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
