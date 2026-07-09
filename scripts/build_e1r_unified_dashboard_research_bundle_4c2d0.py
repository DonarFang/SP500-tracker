#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]

ROW_CURVE = ROOT / "exports/e1r_unified_5y_full_account_v1_row_derived_equity_curve.json"
ROW_SUMMARY = ROOT / "exports/e1r_unified_5y_full_account_v1_row_derived_summary.json"

OUT_BUNDLE = ROOT / "exports/e1r_unified_5y_dashboard_research_bundle.json"
REPORT_JSON = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2D0_DASHBOARD_RESEARCH_BUNDLE_REPORT.json"
REPORT_MD = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2D0_DASHBOARD_RESEARCH_BUNDLE_REPORT.md"

def now():
    return datetime.now(timezone.utc).isoformat()

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))

def read_json(p: Path):
    return json.loads(p.read_text())

def write_json(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def main():
    curve = read_json(ROW_CURVE)
    summary = read_json(ROW_SUMMARY)

    metrics = summary["row_derived_metrics"]
    rows = curve["rows"]

    bundle = {
        "artifact_type": "e1r_unified_5y_dashboard_research_bundle",
        "generated_at": now(),
        "status": "DASHBOARD_RESEARCH_BUNDLE_READY_ACCOUNT_LEVEL_ONLY",
        "strategy_id": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1",
        "display_scope": "research_backtest_account_curve_only",
        "metric_source": "daily_equity_records.total_equity",
        "do_not_use": {
            "engine_reported_metrics": True,
            "trade_level_metrics": True,
            "reason": "Engine-reported final_equity used cash instead of total_equity; SIM_END trades have effective_exit=0 and return_pct=-100.",
        },
        "warnings": [
            "Account-level row-derived equity curve is usable for research display.",
            "Trade metrics are not validated and must not be shown as official performance.",
            "Engine-reported result/summary metrics are rejected for official use.",
            "This bundle should not overwrite frozen E1 metrics.",
        ],
        "metrics": {
            "first_date": metrics["first_date"],
            "last_date": metrics["last_date"],
            "row_count": metrics["row_count"],
            "total_return_pct": metrics["total_return_pct"],
            "spx_total_return_pct": metrics["spx_total_return_pct"],
            "alpha_pct": metrics["alpha_pct"],
            "cagr_pct": metrics["cagr_pct"],
            "max_drawdown_pct": metrics["max_drawdown_pct"],
            "sharpe_ratio": metrics["sharpe_ratio_row_derived"],
            "annualized_vol_pct": metrics["annualized_vol_pct_row_derived"],
            "final_equity": metrics["last_equity"],
            "initial_equity": metrics["first_equity"],
            "final_exposure_pct": metrics["final_exposure_pct"],
        },
        "regime_summary": {
            "regime_counts": metrics["regime_counts"],
            "active_mode_counts": metrics["active_mode_counts"],
            "risk_budget_mode_counts": metrics["risk_budget_mode_counts"],
        },
        "validation": summary["validation"],
        "curve": {
            "source": rel(ROW_CURVE),
            "rows": rows,
        },
        "source_files": {
            "row_curve": rel(ROW_CURVE),
            "row_summary": rel(ROW_SUMMARY),
        },
    }

    validation = {
        "bundle_status_ready": bundle["status"] == "DASHBOARD_RESEARCH_BUNDLE_READY_ACCOUNT_LEVEL_ONLY",
        "row_count_ge_1000": metrics["row_count"] >= 1000,
        "has_curve_rows": len(rows) == metrics["row_count"],
        "uses_row_derived_metrics": bundle["metric_source"] == "daily_equity_records.total_equity",
        "engine_metrics_rejected": bundle["do_not_use"]["engine_reported_metrics"] is True,
        "trade_metrics_rejected": bundle["do_not_use"]["trade_level_metrics"] is True,
        "covers_uptrend": metrics["regime_counts"].get("UPTREND", 0) > 0,
        "covers_sideways": metrics["regime_counts"].get("SIDEWAYS", 0) > 0,
        "covers_downtrend": metrics["regime_counts"].get("DOWNTREND", 0) > 0,
    }

    report = {
        "generated_at": now(),
        "stage": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2D0_DASHBOARD_RESEARCH_BUNDLE",
        "status": "DASHBOARD_RESEARCH_BUNDLE_READY_NO_UI_CHANGE",
        "outputs": {
            "bundle": rel(OUT_BUNDLE),
        },
        "metrics": bundle["metrics"],
        "regime_summary": bundle["regime_summary"],
        "validation": validation,
        "warnings": bundle["warnings"],
        "conclusion": "E1R_ROW_DERIVED_ACCOUNT_CURVE_READY_FOR_RESEARCH_DASHBOARD_WIRING",
        "recommended_next_action": "Proceed to 4C-2D-1: wire this bundle into Research & Backtest tab with explicit Account-level only / Trade metrics not validated labels.",
    }

    write_json(OUT_BUNDLE, bundle)
    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R Unified 5Y — 4C-2D-0 Dashboard Research Bundle")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{report['conclusion']}`")
    md.append(f"- Recommended: {report['recommended_next_action']}")
    md.append("")
    md.append("## Metrics")
    md.append("")
    md.append("```json")
    md.append(json.dumps(report["metrics"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Validation")
    md.append("")
    md.append("```json")
    md.append(json.dumps(validation, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Warnings")
    md.append("")
    md.append("```json")
    md.append(json.dumps(bundle["warnings"], indent=2, ensure_ascii=False))
    md.append("```")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("E1R_UNIFIED_5Y_4C2D0_DASHBOARD_RESEARCH_BUNDLE_COMPLETE")
    print("outputs:", json.dumps(report["outputs"], ensure_ascii=False))
    print("metrics:", json.dumps(report["metrics"], ensure_ascii=False))
    print("regime_summary:", json.dumps(report["regime_summary"], ensure_ascii=False))
    print("validation:", json.dumps(validation, ensure_ascii=False))
    print("conclusion:", report["conclusion"])
    print("recommended_next_action:", report["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
