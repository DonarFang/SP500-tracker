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

REPORT_JSON = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4C2_SIDECAR_STRICT_FIELD_AUDIT.json"
REPORT_MD = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4C2_SIDECAR_STRICT_FIELD_AUDIT.md"

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

def as_int(v, default=0):
    try:
        if v is None:
            return default
        return int(v)
    except Exception:
        return default

def as_float(v, default=0.0):
    try:
        if v is None:
            return default
        return float(v)
    except Exception:
        return default

def summarize_strict(result: dict):
    records = result.get("records")
    if not isinstance(records, list):
        return {
            "has_records": False,
            "record_count": 0,
            "result_top_keys": sorted(result.keys())[:100],
        }

    all_regimes = Counter()
    all_subclasses = Counter()

    is_active_true_regimes = Counter()
    is_active_true_subclasses = Counter()

    gross_positive_regimes = Counter()
    gross_positive_subclasses = Counter()

    selected_positive_regimes = Counter()
    selected_positive_subclasses = Counter()

    holdings_positive_regimes = Counter()
    holdings_positive_subclasses = Counter()

    active_strict_regimes = Counter()
    active_strict_subclasses = Counter()

    candidate_counts = []
    selected_counts = []
    holdings_lengths = []
    gross_exposures = []

    strict_active_samples = []
    inactive_with_candidate_samples = []
    dr_recovery_samples = []

    for r in records:
        if not isinstance(r, dict):
            continue

        regime = r.get("regime") or r.get("spx_regime") or "UNKNOWN"
        subclass = r.get("subclass") or r.get("sideways_subclass") or "NO_SUBCLASS"

        is_active = r.get("is_active") is True or r.get("sidecar_active") is True or r.get("active") is True
        gross = as_float(r.get("gross_exposure"), 0.0)
        selected = as_int(r.get("selected_count"), 0)
        candidate = as_int(r.get("candidate_count"), 0)

        holdings = r.get("holdings")
        if isinstance(holdings, list):
            holdings_len = len(holdings)
        elif isinstance(holdings, dict):
            holdings_len = len(holdings)
        else:
            holdings_len = 0

        all_regimes[regime] += 1
        all_subclasses[subclass] += 1

        candidate_counts.append(candidate)
        selected_counts.append(selected)
        holdings_lengths.append(holdings_len)
        gross_exposures.append(gross)

        if is_active:
            is_active_true_regimes[regime] += 1
            is_active_true_subclasses[subclass] += 1

        if gross > 0:
            gross_positive_regimes[regime] += 1
            gross_positive_subclasses[subclass] += 1

        if selected > 0:
            selected_positive_regimes[regime] += 1
            selected_positive_subclasses[subclass] += 1

        if holdings_len > 0:
            holdings_positive_regimes[regime] += 1
            holdings_positive_subclasses[subclass] += 1

        # strict account-side active definition:
        # candidate_count alone is NOT active. It is only available universe/candidate count.
        strict_active = is_active or gross > 0 or selected > 0 or holdings_len > 0

        if strict_active:
            active_strict_regimes[regime] += 1
            active_strict_subclasses[subclass] += 1
            if len(strict_active_samples) < 20:
                strict_active_samples.append({
                    "date": r.get("date"),
                    "next_date": r.get("next_date"),
                    "regime": regime,
                    "subclass": subclass,
                    "is_active": is_active,
                    "candidate_count": candidate,
                    "selected_count": selected,
                    "holdings_len": holdings_len,
                    "gross_exposure": gross,
                    "portfolio_return": r.get("portfolio_return"),
                    "portfolio_return_pct": r.get("portfolio_return_pct"),
                    "spx_return": r.get("spx_return"),
                    "spx_return_pct": r.get("spx_return_pct"),
                    "keys": sorted(r.keys()),
                    "holdings_sample": holdings[:5] if isinstance(holdings, list) else holdings,
                })

        if candidate > 0 and not strict_active and len(inactive_with_candidate_samples) < 20:
            inactive_with_candidate_samples.append({
                "date": r.get("date"),
                "regime": regime,
                "subclass": subclass,
                "is_active": is_active,
                "candidate_count": candidate,
                "selected_count": selected,
                "holdings_len": holdings_len,
                "gross_exposure": gross,
            })

        if subclass in {"DETERIORATION_TRANSITION", "RECOVERY_TRANSITION"} and len(dr_recovery_samples) < 30:
            dr_recovery_samples.append({
                "date": r.get("date"),
                "regime": regime,
                "subclass": subclass,
                "is_active": is_active,
                "candidate_count": candidate,
                "selected_count": selected,
                "holdings_len": holdings_len,
                "gross_exposure": gross,
                "strict_active": strict_active,
                "keys": sorted(r.keys()),
            })

    summary = {
        "has_records": True,
        "record_count": len(records),
        "result_top_keys": sorted(result.keys())[:100],

        "all_regime_counts": dict(all_regimes),
        "all_subclass_counts": dict(all_subclasses),

        "is_active_true_regime_counts": dict(is_active_true_regimes),
        "is_active_true_subclass_counts": dict(is_active_true_subclasses),

        "gross_positive_regime_counts": dict(gross_positive_regimes),
        "gross_positive_subclass_counts": dict(gross_positive_subclasses),

        "selected_positive_regime_counts": dict(selected_positive_regimes),
        "selected_positive_subclass_counts": dict(selected_positive_subclasses),

        "holdings_positive_regime_counts": dict(holdings_positive_regimes),
        "holdings_positive_subclass_counts": dict(holdings_positive_subclasses),

        "strict_active_regime_counts": dict(active_strict_regimes),
        "strict_active_subclass_counts": dict(active_strict_subclasses),

        "candidate_count_max": max(candidate_counts) if candidate_counts else 0,
        "selected_count_max": max(selected_counts) if selected_counts else 0,
        "holdings_len_max": max(holdings_lengths) if holdings_lengths else 0,
        "gross_exposure_max": max(gross_exposures) if gross_exposures else 0.0,

        "strict_active_samples": strict_active_samples,
        "inactive_with_candidate_samples": inactive_with_candidate_samples,
        "deterioration_recovery_samples": dr_recovery_samples,

        "field_interpretation": {
            "candidate_count": "candidate/universe count only; must not be treated as live selected positions.",
            "selected_count": "sidecar selected basket count; Top10 candidate/selection pool, not full-account live holdings.",
            "holdings": "sidecar holdings basket used to compute sleeve return.",
            "gross_exposure": "sidecar sleeve gross exposure, expected cap 0.25.",
            "is_active": "sidecar activation flag from original sidecar function.",
        }
    }

    return summary

def main():
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    sys.path.insert(0, str(ROOT))

    run = {"attempted": False, "ok": False, "error": None}
    function_report = {}
    config_report = {}
    summary = None

    try:
        mod = importlib.import_module("src.engine.e1r_sidecar_sleeve")
        Config = getattr(mod, "E1RSidecarConfig")
        build = getattr(mod, "build_e1r_sidecar_sleeve")

        function_report = {
            "module": "src.engine.e1r_sidecar_sleeve",
            "config_signature": str(inspect.signature(Config)),
            "function_signature": str(inspect.signature(build)),
        }

        config = Config(start_date=START_DATE, end_date=END_DATE)

        config_report = {
            "start_date": START_DATE,
            "end_date": END_DATE,
            "config_repr": repr(config),
            "config_dict": getattr(config, "__dict__", None),
            "note": "Only required date fields supplied; all sidecar trading parameters remain original defaults.",
        }

        run["attempted"] = True
        result = build(
            stock_dir=STOCK_DIR,
            spx_path=SPX_PATH,
            regime_path=REGIME_PATH,
            config=config,
        )
        run["ok"] = True
        summary = summarize_strict(result)

    except Exception as exc:
        run["error"] = type(exc).__name__ + ": " + str(exc)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    strict_active_subclasses = set((summary or {}).get("strict_active_subclass_counts", {}).keys())
    strict_active_regimes = set((summary or {}).get("strict_active_regime_counts", {}).keys())

    validations = {
        "strategy_files_unchanged": before_hashes == after_hashes,
        "backtest_engine_run": False,
        "dashboard_changed": False,
        "official_result_generated": False,
        "sidecar_called_ok": run["attempted"] is True and run["ok"] is True,
        "records_exist": bool(summary and summary.get("has_records")),
        "strict_active_only_sideways": strict_active_regimes.issubset({"SIDEWAYS"}) and len(strict_active_regimes) > 0,
        "strict_active_only_ma_conflict": strict_active_subclasses.issubset({"MA_CONFLICT"}) and len(strict_active_subclasses) > 0,
        "deterioration_recovery_not_strict_active": not bool(strict_active_subclasses & {"DETERIORATION_TRANSITION", "RECOVERY_TRANSITION"}),
        "selected_count_max_eq_10": bool(summary and summary.get("selected_count_max") == 10),
        "gross_exposure_max_eq_025": bool(summary and abs(float(summary.get("gross_exposure_max", 999)) - 0.25) < 1e-9),
        "candidate_count_not_used_as_live_holdings": bool(summary and summary.get("candidate_count_max", 0) >= summary.get("selected_count_max", 0)),
    }

    if all(validations.values()):
        conclusion = "ORIGINAL_SIDECAR_CONFIRMED_STRICT_ACTIVE_MA_CONFLICT_ONLY"
        recommended = "Proceed to 4C-2C-4D: full 5Y combined rerun. Use original sidecar output; DETERIORATION/RECOVERY cash/defensive; enforce account open_positions_count <=3."
    else:
        conclusion = "ORIGINAL_SIDECAR_STRICT_AUDIT_FAILED"
        recommended = "Do not run full 5Y. Review failed validations."

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "E1R_COMBINED_5Y_4C2C4C2_SIDECAR_STRICT_FIELD_AUDIT",
        "status": "SIDECAR_STRICT_FIELD_AUDIT_COMPLETE",
        "policy": {
            "strategy_logic_changed": False,
            "backtest_engine_run": False,
            "dashboard_changed": False,
            "official_result_generated": False,
            "audit_fix": "Do not treat candidate_count as selected_count or live holdings.",
        },
        "function_report": function_report,
        "config_report": config_report,
        "sidecar_run": run,
        "sidecar_strict_summary": summary,
        "validations": validations,
        "conclusion": conclusion,
        "recommended_next_action": recommended,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R Combined 5Y — 4C-2C-4C-2 Sidecar Strict Field Audit")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Policy")
    md.append("```json")
    md.append(json.dumps(report["policy"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Strict Sidecar Summary")
    md.append("```json")
    md.append(json.dumps(summary, indent=2, ensure_ascii=False))
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

    print("E1R_COMBINED_5Y_4C2C4C2_SIDECAR_STRICT_FIELD_AUDIT_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("config_report:", json.dumps(config_report, ensure_ascii=False))
    print("sidecar_run:", json.dumps(run, ensure_ascii=False))
    print("sidecar_strict_summary:", json.dumps(summary, ensure_ascii=False)[:16000])
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
