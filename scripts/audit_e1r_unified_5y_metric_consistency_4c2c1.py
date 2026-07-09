#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
from collections import Counter
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]

RESULT = ROOT / "exports/e1r_unified_5y_full_account_v1_result.json"
CURVE = ROOT / "exports/e1r_unified_5y_full_account_v1_equity_curve.json"
SUMMARY = ROOT / "exports/e1r_unified_5y_full_account_v1_summary.json"

REPORT_JSON = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C1_METRIC_CONSISTENCY_AUDIT.json"
REPORT_MD = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C1_METRIC_CONSISTENCY_AUDIT.md"

def now():
    return datetime.now(timezone.utc).isoformat()

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))

def read_json(p: Path):
    return json.loads(p.read_text())

def write_json(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def pct(a, b):
    if b in (0, None):
        return None
    return (a / b - 1.0) * 100.0

def max_drawdown_from_rows(rows):
    peak = None
    maxdd = 0.0
    for r in rows:
        eq = r.get("total_equity")
        if eq is None:
            continue
        eq = float(eq)
        if peak is None or eq > peak:
            peak = eq
        if peak and peak > 0:
            dd = (peak - eq) / peak * 100.0
            maxdd = max(maxdd, dd)
    return maxdd

def audit():
    result = read_json(RESULT)
    curve = read_json(CURVE)
    summary = read_json(SUMMARY)

    daily = result.get("daily_equity_records") or []
    curve_rows = curve.get("rows") or []
    trades = result.get("trades") or []

    first_daily = daily[0] if daily else None
    last_daily = daily[-1] if daily else None
    first_curve = curve_rows[0] if curve_rows else None
    last_curve = curve_rows[-1] if curve_rows else None

    first_eq = float(first_daily["total_equity"]) if first_daily else None
    last_eq = float(last_daily["total_equity"]) if last_daily else None
    last_cash = float(last_daily["cash"]) if last_daily and last_daily.get("cash") is not None else None
    last_pos = float(last_daily["positions_value"]) if last_daily and last_daily.get("positions_value") is not None else None

    row_return_pct = pct(last_eq, first_eq) if first_eq and last_eq else None
    row_maxdd_pct = max_drawdown_from_rows(daily)

    reported_metrics = {
        "result_total_return_pct": result.get("total_return_pct"),
        "result_final_equity": result.get("final_equity"),
        "result_max_drawdown_pct": result.get("max_drawdown_pct"),
        "summary_total_return_pct": summary.get("metrics", {}).get("total_return_pct"),
        "summary_final_equity": summary.get("metrics", {}).get("final_equity"),
        "summary_max_drawdown_pct": summary.get("metrics", {}).get("max_drawdown_pct"),
    }

    trade_exit_counter = Counter()
    trade_return_counter = Counter()
    trade_regime_counter = Counter()
    suspicious_trades = []

    for t in trades:
        if not isinstance(t, dict):
            continue
        trade_exit_counter[t.get("exit_signal") or t.get("exit_type")] += 1
        trade_return_counter[str(t.get("return_pct"))] += 1
        trade_regime_counter[t.get("dominant_regime") or t.get("entry_regime")] += 1

        if t.get("return_pct") == -100.0 or t.get("effective_exit") == 0.0:
            suspicious_trades.append({
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
                "dominant_regime": t.get("dominant_regime"),
                "size_units_at_exit": t.get("size_units_at_exit"),
            })

    consistency_checks = {
        "result_exists": RESULT.exists(),
        "curve_exists": CURVE.exists(),
        "summary_exists": SUMMARY.exists(),
        "daily_records_count": len(daily),
        "curve_rows_count": len(curve_rows),
        "first_daily_equity": first_eq,
        "last_daily_equity": last_eq,
        "last_daily_cash": last_cash,
        "last_daily_positions_value": last_pos,
        "last_cash_plus_positions": (last_cash + last_pos) if last_cash is not None and last_pos is not None else None,
        "row_derived_total_return_pct": row_return_pct,
        "row_derived_max_drawdown_pct": row_maxdd_pct,
        "reported_result_final_equity_equals_last_total_equity": abs(float(result.get("final_equity", 0)) - last_eq) < 0.01 if last_eq is not None else False,
        "reported_result_final_equity_equals_last_cash": abs(float(result.get("final_equity", 0)) - last_cash) < 0.01 if last_cash is not None else False,
        "reported_return_matches_row_return": abs(float(result.get("total_return_pct", 0)) - row_return_pct) < 0.05 if row_return_pct is not None else False,
        "reported_maxdd_matches_row_maxdd": abs(float(result.get("max_drawdown_pct", 0)) - row_maxdd_pct) < 0.05 if row_maxdd_pct is not None else False,
    }

    if consistency_checks["reported_result_final_equity_equals_last_cash"] and not consistency_checks["reported_result_final_equity_equals_last_total_equity"]:
        diagnosis = "METRIC_LAYER_APPEARS_TO_USE_CASH_AS_FINAL_EQUITY"
        recommended = "Do not use reported result metrics. Recompute official metrics from daily_equity_records total_equity, then patch exporter/report labels."
    elif not consistency_checks["reported_return_matches_row_return"]:
        diagnosis = "REPORTED_METRICS_DO_NOT_MATCH_DAILY_EQUITY_ROWS"
        recommended = "Do not connect to OOS. Recompute metrics from rows and inspect SIM_END liquidation logic."
    elif suspicious_trades:
        diagnosis = "TRADE_LIQUIDATION_OR_RETURN_CONTRACT_SUSPICIOUS"
        recommended = "Inspect SIM_END effective_exit and trade return calculation before official promotion."
    else:
        diagnosis = "METRICS_APPEAR_CONSISTENT"
        recommended = "Proceed only after confirming sample_validity policy."

    report = {
        "generated_at": now(),
        "stage": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C1_METRIC_CONSISTENCY_AUDIT",
        "inputs": {
            "result": rel(RESULT),
            "curve": rel(CURVE),
            "summary": rel(SUMMARY),
        },
        "reported_metrics": reported_metrics,
        "row_derived_metrics": {
            "first_equity": first_eq,
            "last_equity": last_eq,
            "total_return_pct": row_return_pct,
            "max_drawdown_pct": row_maxdd_pct,
        },
        "consistency_checks": consistency_checks,
        "trade_audit": {
            "trade_count": len(trades),
            "exit_counter": dict(trade_exit_counter),
            "return_counter": dict(trade_return_counter),
            "dominant_regime_counter": {str(k): v for k, v in trade_regime_counter.items()},
            "suspicious_trade_count": len(suspicious_trades),
            "suspicious_trade_samples": suspicious_trades[:20],
        },
        "sample_validity": result.get("sample_validity"),
        "diagnosis": diagnosis,
        "recommended_next_action": recommended,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R Unified 5Y Full Account V1 — 4C-2C-1 Metric Consistency Audit")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Diagnosis")
    md.append("")
    md.append(f"- `{diagnosis}`")
    md.append(f"- Recommended: {recommended}")
    md.append("")
    md.append("## Reported vs Row-Derived Metrics")
    md.append("")
    md.append("```json")
    md.append(json.dumps({
        "reported_metrics": reported_metrics,
        "row_derived_metrics": report["row_derived_metrics"],
        "consistency_checks": consistency_checks,
    }, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Trade Audit")
    md.append("")
    md.append("```json")
    md.append(json.dumps(report["trade_audit"], indent=2, ensure_ascii=False)[:24000])
    md.append("```")
    REPORT_MD.write_text("\n".join(md) + "\n")

    print("E1R_UNIFIED_5Y_FULL_ACCOUNT_4C2C1_AUDIT_COMPLETE")
    print("reported_metrics:", json.dumps(reported_metrics, ensure_ascii=False))
    print("row_derived_metrics:", json.dumps(report["row_derived_metrics"], ensure_ascii=False))
    print("consistency_checks:", json.dumps(consistency_checks, ensure_ascii=False))
    print("trade_audit:", json.dumps(report["trade_audit"], ensure_ascii=False)[:8000])
    print("sample_validity:", json.dumps(report["sample_validity"], ensure_ascii=False))
    print("diagnosis:", diagnosis)
    print("recommended_next_action:", recommended)
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    audit()
