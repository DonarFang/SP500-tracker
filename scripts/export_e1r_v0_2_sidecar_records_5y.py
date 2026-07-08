#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import sys
import traceback
from datetime import datetime, timezone
from collections import Counter
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

START_DATE = "2021-06-11"
END_DATE = "2026-06-18"

STOCK_DIR = ROOT / "data/research/e1_5y/raw/stocks"
SPX_PATH = ROOT / "data/research/e1_5y/raw/indices/SPX.json"
REGIME_PATH = ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json"

OUT_JSON = ROOT / "exports/e1r_v0_2_sidecar_records_5y.json"
REPORT_JSON = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4A_SIDECAR_RECORDS_EXPORT_REPORT.json"
REPORT_MD = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4A_SIDECAR_RECORDS_EXPORT_REPORT.md"

CANONICAL_E1R_FILES = [
    ROOT / "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
    ROOT / "exports/e1_e1r_5y_equity_comparison.json",
]

EXPECTED = {
    "full_intervals_min": 1000,
    "sidecar_active_expected_approx": 135,
    "ma_conflict_expected_approx": 135,
}

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def normalize_date(x: Any) -> str | None:
    if x is None:
        return None
    s = str(x)
    if len(s) >= 10 and s[4:5] == "-" and s[7:8] == "-":
        return s[:10]
    return None

def as_float(x: Any, default: float = 0.0) -> float:
    try:
        if x is None:
            return default
        return float(x)
    except Exception:
        return default

def object_summary(obj: Any, max_items: int = 3) -> dict[str, Any]:
    if isinstance(obj, dict):
        return {
            "type": "dict",
            "len": len(obj),
            "keys": sorted(list(obj.keys()))[:120],
            "sample": [[k, type(v).__name__] for k, v in list(obj.items())[:max_items]],
        }
    if isinstance(obj, list):
        first = obj[0] if obj else None
        return {
            "type": "list",
            "len": len(obj),
            "first_type": type(first).__name__ if first is not None else None,
            "first_keys": sorted(first.keys()) if isinstance(first, dict) else None,
            "first": obj[:max_items],
            "last": obj[-max_items:] if obj else [],
        }
    return {"type": type(obj).__name__, "repr": repr(obj)[:1000]}

def sidecar_stats(records: list[dict[str, Any]]) -> dict[str, Any]:
    dates = []
    regime_counter = Counter()
    subclass_counter = Counter()
    active_regime_counter = Counter()
    active_subclass_counter = Counter()
    active_count = 0
    nonzero_return_count = 0
    gross_exposure_values = []
    selected_count_values = []

    for r in records:
        d = normalize_date(r.get("date") or r.get("next_date") or r.get("interval_end_date"))
        if d:
            dates.append(d)

        regime = r.get("regime") or r.get("spx_regime") or r.get("market_state")
        subclass = r.get("subclass") or r.get("sideways_subclass")

        if regime:
            regime_counter[str(regime)] += 1
        if subclass:
            subclass_counter[str(subclass)] += 1

        active = bool(r.get("sidecar_active"))
        ret = as_float(r.get("sidecar_return"), 0.0)

        if active:
            active_count += 1
            if regime:
                active_regime_counter[str(regime)] += 1
            if subclass:
                active_subclass_counter[str(subclass)] += 1

        if abs(ret) > 1e-12:
            nonzero_return_count += 1

        if r.get("sidecar_gross_exposure") is not None:
            gross_exposure_values.append(as_float(r.get("sidecar_gross_exposure")))
        if r.get("sidecar_selected_count") is not None:
            selected_count_values.append(as_float(r.get("sidecar_selected_count")))

    dc = Counter(dates)

    return {
        "row_count": len(records),
        "date_start": min(dates) if dates else None,
        "date_end": max(dates) if dates else None,
        "unique_dates": len(dc),
        "max_rows_per_date": max(dc.values()) if dc else None,
        "one_row_per_date": bool(dc) and max(dc.values()) == 1,
        "regime_counts": dict(regime_counter),
        "subclass_counts": dict(subclass_counter),
        "active_count": active_count,
        "nonzero_sidecar_return_count": nonzero_return_count,
        "sidecar_active_by_regime": dict(active_regime_counter),
        "sidecar_active_by_subclass": dict(active_subclass_counter),
        "gross_exposure_min": min(gross_exposure_values) if gross_exposure_values else None,
        "gross_exposure_max": max(gross_exposure_values) if gross_exposure_values else None,
        "selected_count_min": min(selected_count_values) if selected_count_values else None,
        "selected_count_max": max(selected_count_values) if selected_count_values else None,
    }

def interval_stats(intervals: list[Any]) -> dict[str, Any]:
    dates = []
    records = []

    for item in intervals:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            d = normalize_date(item[0])
            nd = normalize_date(item[1])
            if d:
                dates.append(d)
            records.append({"date": d, "next_date": nd})
        elif isinstance(item, dict):
            d = normalize_date(item.get("date"))
            nd = normalize_date(item.get("next_date"))
            if d:
                dates.append(d)
            records.append({"date": d, "next_date": nd})

    dc = Counter(dates)

    return {
        "row_count": len(intervals),
        "date_start": min(dates) if dates else None,
        "date_end": max(dates) if dates else None,
        "unique_dates": len(dc),
        "max_rows_per_date": max(dc.values()) if dc else None,
        "one_row_per_date": bool(dc) and max(dc.values()) == 1,
        "sample_first": records[:3],
        "sample_last": records[-3:] if records else [],
    }

def normalize_sidecar_record(r: dict[str, Any]) -> dict[str, Any]:
    date = normalize_date(r.get("date"))
    next_date = normalize_date(r.get("next_date"))
    return {
        "date": date,
        "next_date": next_date,
        "regime": r.get("regime") or r.get("spx_regime"),
        "subclass": r.get("subclass") or r.get("sideways_subclass"),
        "sidecar_active": bool(r.get("sidecar_active")),
        "sidecar_return": as_float(r.get("sidecar_return"), 0.0),
        "sidecar_return_pct": r.get("sidecar_return_pct"),
        "spx_return": r.get("spx_return"),
        "spx_return_pct": r.get("spx_return_pct"),
        "sidecar_gross_exposure": r.get("sidecar_gross_exposure"),
        "sidecar_selected_count": r.get("sidecar_selected_count"),
        "sidecar_holdings": r.get("sidecar_holdings"),
    }

def main() -> int:
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "src"))

    canonical_e1r_exists_before = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    try:
        from src.engine import e1r_sidecar_sleeve as sidecar

        cfg = sidecar.E1RSidecarConfig(start_date=START_DATE, end_date=END_DATE)

        spx = sidecar.load_asset(SPX_PATH)
        regimes = sidecar.load_regimes(REGIME_PATH)
        stocks, excluded = sidecar.load_stock_universe(STOCK_DIR, cfg)
        intervals = sidecar.build_backtest_intervals(spx, regimes, cfg)
        rankings = sidecar.build_daily_rankings(stocks, spx, regimes, intervals, cfg)
        records_raw = sidecar.run_daily_rebalanced_sidecar(rankings, spx, regimes, intervals, cfg)
        summary = sidecar.summarize_sidecar(records_raw, cfg)

        records = [normalize_sidecar_record(r) for r in records_raw if isinstance(r, dict)]

        istats = interval_stats(intervals)
        sstats = sidecar_stats(records)

        validation = {
            "full_intervals_ge_1000": istats["row_count"] >= EXPECTED["full_intervals_min"],
            "sidecar_records_nonempty": len(records) > 0,
            "sidecar_one_row_per_date": sstats["one_row_per_date"],
            "sidecar_active_count_positive": sstats["active_count"] > 0,
            "sidecar_active_count_reasonable": 80 <= sstats["active_count"] <= 180,
            "ma_conflict_active_present": (
                sstats["sidecar_active_by_subclass"].get("MA_CONFLICT", 0)
                + sstats["sidecar_active_by_subclass"].get("Sideway-MA-Conflict", 0)
                + sstats["sidecar_active_by_subclass"].get("SIDEWAYS_MA_CONFLICT", 0)
            ) > 0,
            "canonical_e1r_files_unchanged": canonical_e1r_exists_before == {rel(p): p.exists() for p in CANONICAL_E1R_FILES},
        }

        write_sidecar = all(validation.values())

        artifact = {
            "artifact_type": "e1r_v0_2_regime_aware_sidecar_records_5y",
            "generated_at": now(),
            "window": {
                "start_date": START_DATE,
                "end_date": END_DATE,
            },
            "source": "src.engine.e1r_sidecar_sleeve.run_daily_rebalanced_sidecar",
            "policy": {
                "e1r_canonical_written": False,
                "portfolio_equity_composed": False,
                "dashboard_changed": False,
                "strategy_logic_changed": False,
            },
            "config": repr(cfg),
            "input_summary": {
                "stock_dir": rel(STOCK_DIR),
                "spx_path": rel(SPX_PATH),
                "regime_path": rel(REGIME_PATH),
                "stocks_loaded": len(stocks) if hasattr(stocks, "__len__") else None,
                "excluded_count": len(excluded) if hasattr(excluded, "__len__") else None,
                "excluded_sample": excluded[:20] if isinstance(excluded, list) else None,
            },
            "interval_stats": istats,
            "sidecar_stats": sstats,
            "sidecar_summary": summary,
            "validation": validation,
            "records": records,
        }

        if write_sidecar:
            write_json(OUT_JSON, artifact)

        status = "E1R_SIDECAR_RECORDS_5Y_WRITTEN" if write_sidecar else "E1R_SIDECAR_RECORDS_5Y_NOT_READY"

        report = {
            "generated_at": now(),
            "stage": "B_STAGE_3_8E2F2C4C10F4A_SIDECAR_RECORDS_EXPORT",
            "status": status,
            "policy": {
                "dashboard_changed": False,
                "workflow_changed": False,
                "strategy_logic_changed": False,
                "e1r_canonical_written": False,
                "portfolio_equity_composed": False,
                "sidecar_records_written": write_sidecar,
            },
            "paths": {
                "sidecar_records_path": rel(OUT_JSON),
                "report_json": rel(REPORT_JSON),
                "report_md": rel(REPORT_MD),
            },
            "input_summary": artifact["input_summary"],
            "interval_stats": istats,
            "sidecar_stats": sstats,
            "sidecar_summary_type": type(summary).__name__,
            "sidecar_summary": summary,
            "validation": validation,
            "canonical_e1r_exists_before": canonical_e1r_exists_before,
            "canonical_e1r_exists_after": {rel(p): p.exists() for p in CANONICAL_E1R_FILES},
            "diagnosis": [
                "Generated regime-aware sidecar records using explicit 5Y window.",
                "Sidecar records are validated separately from full E1/E1R portfolio equity.",
                "No E1R portfolio canonical export was written in this stage.",
            ],
            "next_stage": {
                "name": "Stage 3.8E-2F-2C-4C-10F-4B",
                "title": "Compose continuous E1R portfolio equity from E1 core + sidecar records",
                "recommended_action": "Use exports/e1_5y_backtest_equity_curve.json and exports/e1r_v0_2_sidecar_records_5y.json to compose full-window E1R equity, then validate frozen metrics before writing canonical E1R export.",
            },
        }

        write_json(REPORT_JSON, report)

        md = []
        md.append("# Stage 3.8E-2F-2C-4C-10F-4A Sidecar Records Export Report")
        md.append("")
        md.append(f"Generated At: `{report['generated_at']}`")
        md.append("")
        md.append("## Status")
        md.append("")
        md.append(f"- Status: `{status}`")
        md.append(f"- Sidecar records written: `{write_sidecar}`")
        md.append("- E1R canonical written: `False`")
        md.append("")
        md.append("## Interval Stats")
        md.append("")
        md.append("```json")
        md.append(json.dumps(istats, indent=2, ensure_ascii=False))
        md.append("```")
        md.append("")
        md.append("## Sidecar Stats")
        md.append("")
        md.append("```json")
        md.append(json.dumps(sstats, indent=2, ensure_ascii=False))
        md.append("```")
        md.append("")
        md.append("## Validation")
        md.append("")
        md.append("```json")
        md.append(json.dumps(validation, indent=2, ensure_ascii=False))
        md.append("```")
        md.append("")
        md.append("## Next Stage")
        md.append("")
        md.append(f"- `{report['next_stage']['name']}`: {report['next_stage']['title']}")
        md.append(f"- Recommended action: {report['next_stage']['recommended_action']}")
        md.append("")

        REPORT_MD.write_text("\n".join(md) + "\n")

        print("E1R sidecar 5Y records export complete")
        print("status:", status)
        print("sidecar_records_written:", write_sidecar)
        print("interval_row_count:", istats["row_count"])
        print("interval_window:", istats["date_start"], "->", istats["date_end"])
        print("sidecar_row_count:", sstats["row_count"])
        print("sidecar_unique_dates:", sstats["unique_dates"])
        print("sidecar_active_count:", sstats["active_count"])
        print("sidecar_nonzero_return_count:", sstats["nonzero_sidecar_return_count"])
        print("sidecar_active_by_regime:", json.dumps(sstats["sidecar_active_by_regime"], ensure_ascii=False))
        print("sidecar_active_by_subclass:", json.dumps(sstats["sidecar_active_by_subclass"], ensure_ascii=False))
        print("validation:", json.dumps(validation, ensure_ascii=False))
        print("sidecar_records_path:", rel(OUT_JSON))
        print("report_json:", rel(REPORT_JSON))
        print("report_md:", rel(REPORT_MD))
        print("next_stage:", report["next_stage"]["name"])

        return 0 if write_sidecar else 2

    except Exception as exc:
        report = {
            "generated_at": now(),
            "stage": "B_STAGE_3_8E2F2C4C10F4A_SIDECAR_RECORDS_EXPORT",
            "status": "E1R_SIDECAR_RECORDS_5Y_FAILED",
            "policy": {
                "dashboard_changed": False,
                "workflow_changed": False,
                "strategy_logic_changed": False,
                "e1r_canonical_written": False,
                "portfolio_equity_composed": False,
                "sidecar_records_written": False,
            },
            "error": type(exc).__name__ + ": " + str(exc),
            "traceback_tail": traceback.format_exc()[-10000:],
            "canonical_e1r_exists_before": canonical_e1r_exists_before,
            "canonical_e1r_exists_after": {rel(p): p.exists() for p in CANONICAL_E1R_FILES},
            "diagnosis": [
                "Sidecar generation failed before validated records were written.",
                "No E1R canonical export was written.",
            ],
        }
        write_json(REPORT_JSON, report)
        REPORT_MD.write_text(
            "# Stage 3.8E-2F-2C-4C-10F-4A Sidecar Records Export Report\n\n"
            f"Status: `{report['status']}`\n\n"
            f"Error: `{report['error']}`\n"
        )

        print("E1R sidecar 5Y records export failed")
        print("status:", report["status"])
        print("error:", report["error"])
        print("report_json:", rel(REPORT_JSON))
        print("report_md:", rel(REPORT_MD))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
