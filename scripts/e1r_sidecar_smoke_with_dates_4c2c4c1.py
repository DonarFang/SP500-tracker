#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import importlib
import inspect
import hashlib
import sys
from datetime import datetime, timezone
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

REPORT_JSON = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4C1_SIDECAR_SMOKE_WITH_DATES.json"
REPORT_MD = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4C1_SIDECAR_SMOKE_WITH_DATES.md"

STOCK_DIR = ROOT / "data/research/e1_5y/raw/stocks"
SPX_PATH = ROOT / "data/research/e1_5y/raw/indices/SPX.json"
REGIME_PATH = ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json"

START_DATE = "2021-06-11"
END_DATE = "2026-06-18"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/backtest.py",
]

def now():
    return datetime.now(timezone.utc).isoformat()

def rel(p: Path):
    return str(p.relative_to(ROOT))

def sha256(p: Path):
    if not p.exists():
        return None
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def write_json(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def summarize_sidecar(result: dict):
    records = None
    record_key = None

    for key in ["records", "sidecar_records", "daily_records", "rows"]:
        v = result.get(key)
        if isinstance(v, list):
            records = v
            record_key = key
            break

    summary = {
        "result_top_keys": sorted(result.keys())[:100],
        "has_records": records is not None,
        "record_key": record_key,
        "record_count": len(records) if records else 0,
    }

    if not records:
        return summary

    regimes = Counter()
    subclasses = Counter()
    active_regimes = Counter()
    active_subclasses = Counter()
    selected_counts = []
    gross_exposures = []
    active_samples = []

    for r in records:
        if not isinstance(r, dict):
            continue

        regime = (
            r.get("regime")
            or r.get("spx_regime")
            or r.get("market_regime")
            or r.get("state")
            or "UNKNOWN"
        )
        subclass = (
            r.get("sideways_subclass")
            or r.get("subclass")
            or r.get("sideways_type")
            or "NO_SUBCLASS"
        )

        selected_count = (
            r.get("selected_count")
            or r.get("selection_count")
            or r.get("candidate_count")
            or 0
        )
        gross_exposure = (
            r.get("gross_exposure")
            or r.get("gross_exposure_pct")
            or r.get("sidecar_gross_exposure")
            or 0
        )

        try:
            selected_count = int(selected_count)
        except Exception:
            selected_count = 0

        try:
            gross_exposure = float(gross_exposure)
        except Exception:
            gross_exposure = 0.0

        active = False
        for k in ["active", "sidecar_active", "is_active"]:
            if r.get(k) is True:
                active = True

        if selected_count > 0 or gross_exposure > 0:
            active = True

        regimes[regime] += 1
        subclasses[subclass] += 1
        selected_counts.append(selected_count)
        gross_exposures.append(gross_exposure)

        if active:
            active_regimes[regime] += 1
            active_subclasses[subclass] += 1
            if len(active_samples) < 12:
                active_samples.append({
                    "date": r.get("date"),
                    "regime": regime,
                    "subclass": subclass,
                    "selected_count": selected_count,
                    "gross_exposure": gross_exposure,
                    "keys": sorted(r.keys())[:50],
                })

    summary.update({
        "regime_counts": dict(regimes),
        "subclass_counts": dict(subclasses),
        "active_regime_counts": dict(active_regimes),
        "active_subclass_counts": dict(active_subclasses),
        "selected_count_max": max(selected_counts) if selected_counts else 0,
        "gross_exposure_max": max(gross_exposures) if gross_exposures else 0.0,
        "active_samples": active_samples,
        "sidecar_active_only_sideways": bool(active_regimes) and set(active_regimes).issubset({"SIDEWAYS"}),
        "sidecar_active_only_ma_conflict": bool(active_subclasses) and set(active_subclasses).issubset({"MA_CONFLICT"}),
        "deterioration_recovery_active": any(k in active_subclasses for k in ["DETERIORATION_TRANSITION", "RECOVERY_TRANSITION"]),
        "top10_candidate_pool_observed": max(selected_counts) >= 10 if selected_counts else False,
        "interpretation": "selected_count/top_n is sidecar candidate/selection pool; combined account live holdings must still be capped at <=3.",
    })

    return summary

def main():
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    sys.path.insert(0, str(ROOT))

    sidecar_run = {
        "attempted": False,
        "ok": False,
        "error": None,
    }
    sidecar_summary = None
    config_report = None
    function_report = None

    try:
        mod = importlib.import_module("src.engine.e1r_sidecar_sleeve")
        Config = getattr(mod, "E1RSidecarConfig")
        build = getattr(mod, "build_e1r_sidecar_sleeve")

        function_report = {
            "module": "src.engine.e1r_sidecar_sleeve",
            "config_signature": str(inspect.signature(Config)),
            "function_signature": str(inspect.signature(build)),
        }

        config = Config(
            start_date=START_DATE,
            end_date=END_DATE,
        )

        config_report = {
            "start_date": START_DATE,
            "end_date": END_DATE,
            "config_repr": repr(config),
            "config_dict": getattr(config, "__dict__", None),
            "note": "Only required date fields are supplied; all other sidecar parameters stay at original defaults.",
        }

        sidecar_run["attempted"] = True
        result = build(
            stock_dir=STOCK_DIR,
            spx_path=SPX_PATH,
            regime_path=REGIME_PATH,
            config=config,
        )
        sidecar_run["ok"] = True
        sidecar_summary = summarize_sidecar(result)

    except Exception as exc:
        sidecar_run["error"] = type(exc).__name__ + ": " + str(exc)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "strategy_files_unchanged": before_hashes == after_hashes,
        "backtest_engine_run": False,
        "dashboard_changed": False,
        "official_result_generated": False,
        "sidecar_function_called": sidecar_run["attempted"] is True,
        "sidecar_function_ok": sidecar_run["ok"] is True,
        "sidecar_has_records": bool(sidecar_summary and sidecar_summary.get("has_records")),
        "sidecar_active_only_sideways": bool(sidecar_summary and sidecar_summary.get("sidecar_active_only_sideways")),
        "sidecar_active_only_ma_conflict": bool(sidecar_summary and sidecar_summary.get("sidecar_active_only_ma_conflict")),
        "deterioration_recovery_not_active": bool(sidecar_summary and sidecar_summary.get("deterioration_recovery_active") is False),
        "top10_candidate_pool_observed": bool(sidecar_summary and sidecar_summary.get("top10_candidate_pool_observed")),
        "gross_exposure_cap_25pct": bool(sidecar_summary and abs(float(sidecar_summary.get("gross_exposure_max", 999)) - 0.25) < 1e-9),
    }

    if all(validations.values()):
        conclusion = "ORIGINAL_SIDECAR_ENTRYPOINT_CONFIRMED_MA_CONFLICT_ONLY_TOP10_CANDIDATE_POOL"
        recommended = "Proceed to 4C-2C-4D full 5Y combined rerun using original UPTREND/core path plus original sidecar, with hard validation open_positions_count <=3."
    else:
        conclusion = "ORIGINAL_SIDECAR_ENTRYPOINT_NOT_CONFIRMED"
        recommended = "Do not run full 5Y. Review failed validations."

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "E1R_COMBINED_5Y_4C2C4C1_SIDECAR_SMOKE_WITH_DATES",
        "status": "SIDECAR_SMOKE_WITH_DATES_COMPLETE",
        "policy": {
            "strategy_logic_changed": False,
            "backtest_engine_run": False,
            "dashboard_changed": False,
            "official_result_generated": False,
            "parameter_change": "Only required start_date/end_date supplied to instantiate original sidecar config.",
        },
        "paths": {
            "stock_dir": rel(STOCK_DIR),
            "spx_path": rel(SPX_PATH),
            "regime_path": rel(REGIME_PATH),
        },
        "function_report": function_report,
        "config_report": config_report,
        "sidecar_run": sidecar_run,
        "sidecar_summary": sidecar_summary,
        "validations": validations,
        "conclusion": conclusion,
        "recommended_next_action": recommended,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R Combined 5Y — 4C-2C-4C-1 Sidecar Smoke With Dates")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Policy")
    md.append("```json")
    md.append(json.dumps(report["policy"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Sidecar Summary")
    md.append("```json")
    md.append(json.dumps(sidecar_summary, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Validations")
    md.append("```json")
    md.append(json.dumps(validations, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {recommended}")
    REPORT_MD.write_text("\n".join(md) + "\n")

    print("E1R_COMBINED_5Y_4C2C4C1_SIDECAR_SMOKE_WITH_DATES_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("function_report:", json.dumps(function_report, ensure_ascii=False))
    print("config_report:", json.dumps(config_report, ensure_ascii=False))
    print("sidecar_run:", json.dumps(sidecar_run, ensure_ascii=False))
    print("sidecar_summary:", json.dumps(sidecar_summary, ensure_ascii=False)[:14000])
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
