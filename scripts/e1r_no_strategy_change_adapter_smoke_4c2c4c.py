#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import inspect
import importlib
import hashlib
import sys
from datetime import datetime, timezone
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

REPORT_JSON = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4C_NO_STRATEGY_CHANGE_ADAPTER_SMOKE.json"
REPORT_MD = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4C_NO_STRATEGY_CHANGE_ADAPTER_SMOKE.md"

STOCK_DIR = ROOT / "data/research/e1_5y/raw/stocks"
SPX_PATH = ROOT / "data/research/e1_5y/raw/indices/SPX.json"
REGIME_PATH = ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/backtest.py",
]

CONTRACT = {
    "UPTREND": "Use previously validated UPTREND strategy. Do not replace logic.",
    "SIDEWAYS_MA_CONFLICT": "Use previously validated sidecar strategy.",
    "DETERIORATION_RECOVERY": "Participate only if original sidecar proves participation; otherwise cash/defensive.",
    "DOWNTREND": "Cash/defensive.",
    "GLOBAL_POSITION_CAP": "Actual account live holdings must always be <= 3 stocks.",
    "SIDEWAYS_TOP10": "Candidate pool only, not live 10-stock account holdings.",
    "NO_STRATEGY_CHANGE": True,
}

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))

def sha256(p: Path):
    if not p.exists():
        return None
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def write_json(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def summarize_sidecar_result(result: dict):
    records = None
    for key in ["records", "sidecar_records", "daily_records", "rows"]:
        v = result.get(key)
        if isinstance(v, list):
            records = v
            record_key = key
            break

    summary = {
        "has_records": records is not None,
        "record_key": record_key if records is not None else None,
        "record_count": len(records) if records is not None else 0,
        "top_keys": sorted(result.keys())[:100],
    }

    if records:
        regimes = Counter()
        subclasses = Counter()
        active_regimes = Counter()
        active_subclasses = Counter()
        selected_counts = []
        gross_exposures = []
        sample_active = []

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
                if len(sample_active) < 10:
                    sample_active.append({
                        "date": r.get("date"),
                        "regime": regime,
                        "subclass": subclass,
                        "selected_count": selected_count,
                        "gross_exposure": gross_exposure,
                        "keys": sorted(r.keys())[:40],
                    })

        summary.update({
            "regime_counts": dict(regimes),
            "subclass_counts": dict(subclasses),
            "active_regime_counts": dict(active_regimes),
            "active_subclass_counts": dict(active_subclasses),
            "selected_count_max": max(selected_counts) if selected_counts else 0,
            "gross_exposure_max": max(gross_exposures) if gross_exposures else 0.0,
            "active_samples": sample_active,
        })

        summary["sidecar_active_only_sideways"] = (
            bool(active_regimes)
            and set(active_regimes.keys()).issubset({"SIDEWAYS"})
        )

        summary["sidecar_active_only_ma_conflict"] = (
            bool(active_subclasses)
            and set(active_subclasses.keys()).issubset({"MA_CONFLICT"})
        )

        summary["deterioration_recovery_active"] = any(
            k in active_subclasses
            for k in ["DETERIORATION_TRANSITION", "RECOVERY_TRANSITION"]
        )

        summary["top10_candidate_observed"] = summary["selected_count_max"] >= 10
        summary["top10_is_not_live_holdings_interpretation"] = (
            "selected_count_max is candidate/selection pool from sidecar records; "
            "combined account adapter must still enforce live open_positions_count <= 3."
        )

    return summary

def instantiate_sidecar_config(mod):
    Config = getattr(mod, "E1RSidecarConfig", None)
    if Config is None:
        return None, {"config_class_found": False}

    sig = inspect.signature(Config)
    report = {
        "config_class_found": True,
        "signature": str(sig),
        "parameters": {
            name: {
                "default": None if p.default is inspect._empty else repr(p.default),
                "kind": str(p.kind),
            }
            for name, p in sig.parameters.items()
        },
    }

    try:
        config = Config()
        report["instantiated_with_defaults"] = True
        report["instance_repr"] = repr(config)
        report["instance_dict"] = getattr(config, "__dict__", None)
        return config, report
    except Exception as exc:
        report["instantiated_with_defaults"] = False
        report["error"] = type(exc).__name__ + ": " + str(exc)
        return None, report

def inspect_composer_schema(mod):
    out = {}
    for name in ["compose_e1r_v0_2_variant", "extract_core_interval_returns", "build_equity_records_from_returns"]:
        fn = getattr(mod, name, None)
        out[name] = {
            "exists": fn is not None,
            "signature": str(inspect.signature(fn)) if fn else None,
        }
    return out

def find_existing_core_candidates():
    paths = [
        ROOT / "exports/portfolio_backtest.json",
        ROOT / "exports/e1r_unified_5y_full_account_v1_result.json",
        ROOT / "exports/e1r_unified_5y_dashboard_research_bundle.json",
        ROOT / "exports/e1r_unified_5y_full_account_v1_row_derived_summary.json",
    ]

    out = []
    for p in paths:
        item = {"path": rel(p), "exists": p.exists(), "json_ok": False}
        if p.exists():
            try:
                obj = json.loads(p.read_text())
                item["json_ok"] = True
                item["top_keys"] = sorted(obj.keys())[:100]
                item["strategy_variant"] = obj.get("strategy_variant")
                item["status"] = obj.get("status")
                item["version"] = obj.get("version")
                item["total_return_pct"] = obj.get("total_return_pct")
                item["spx_total_return_pct"] = obj.get("spx_total_return_pct")
                item["daily_records_count"] = len(obj.get("daily_records", [])) if isinstance(obj.get("daily_records"), list) else None
                item["daily_equity_records_count"] = len(obj.get("daily_equity_records", [])) if isinstance(obj.get("daily_equity_records"), list) else None
                if isinstance(obj.get("curve"), dict) and isinstance(obj["curve"].get("rows"), list):
                    item["curve_rows_count"] = len(obj["curve"]["rows"])
            except Exception as exc:
                item["error"] = type(exc).__name__ + ": " + str(exc)
        out.append(item)
    return out

def main():
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    sys.path.insert(0, str(ROOT))

    import_report = {}
    sidecar_run = {
        "attempted": False,
        "ok": False,
        "error": None,
    }
    sidecar_summary = None

    try:
        sidecar_mod = importlib.import_module("src.engine.e1r_sidecar_sleeve")
        composer_mod = importlib.import_module("src.engine.e1r_composer")
        backtest_mod = importlib.import_module("src.engine.backtest")

        import_report["src.engine.e1r_sidecar_sleeve"] = True
        import_report["src.engine.e1r_composer"] = True
        import_report["src.engine.backtest"] = True

        config, config_report = instantiate_sidecar_config(sidecar_mod)
        composer_schema = inspect_composer_schema(composer_mod)

        sidecar_fn = getattr(sidecar_mod, "build_e1r_sidecar_sleeve")

        if config is not None:
            sidecar_run["attempted"] = True
            result = sidecar_fn(
                stock_dir=STOCK_DIR,
                spx_path=SPX_PATH,
                regime_path=REGIME_PATH,
                config=config,
            )
            sidecar_run["ok"] = True
            sidecar_summary = summarize_sidecar_result(result)
        else:
            sidecar_run["error"] = "E1RSidecarConfig could not be instantiated with defaults."

    except Exception as exc:
        import_report["error"] = type(exc).__name__ + ": " + str(exc)
        config_report = locals().get("config_report", None)
        composer_schema = locals().get("composer_schema", None)
        sidecar_run["error"] = type(exc).__name__ + ": " + str(exc)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    core_candidates = find_existing_core_candidates()

    validations = {
        "strategy_files_unchanged": before_hashes == after_hashes,
        "no_backtest_engine_run": True,
        "sidecar_function_called": sidecar_run["attempted"] is True,
        "sidecar_function_ok": sidecar_run["ok"] is True,
        "sidecar_has_records": bool(sidecar_summary and sidecar_summary.get("has_records")),
        "sidecar_active_only_sideways": bool(sidecar_summary and sidecar_summary.get("sidecar_active_only_sideways")),
        "sidecar_active_only_ma_conflict": bool(sidecar_summary and sidecar_summary.get("sidecar_active_only_ma_conflict")),
        "deterioration_recovery_not_active": bool(sidecar_summary and sidecar_summary.get("deterioration_recovery_active") is False),
        "top10_candidate_pool_observed": bool(sidecar_summary and sidecar_summary.get("top10_candidate_observed")),
        "global_live_position_cap_guard_required": True,
    }

    if all(validations.values()):
        conclusion = "SIDECAR_ENTRYPOINT_SMOKE_PASS_MA_CONFLICT_ONLY_TOP10_CANDIDATE_POOL_CONFIRMED"
        recommended = "Proceed to 4C-2C-4D: full 5Y combined rerun using original sidecar entrypoint and original UPTREND/core path, with hard validation that open_positions_count <= 3."
    else:
        conclusion = "SIDECAR_ENTRYPOINT_SMOKE_NEEDS_REVIEW_BEFORE_FULL_RUN"
        recommended = "Do not run full 5Y yet. Review failed validations and source report."

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "E1R_COMBINED_5Y_4C2C4C_NO_STRATEGY_CHANGE_ADAPTER_SMOKE",
        "status": "NO_STRATEGY_CHANGE_ADAPTER_SMOKE_COMPLETE",
        "policy": {
            "strategy_logic_changed": False,
            "backtest_engine_run": False,
            "dashboard_changed": False,
            "official_result_generated": False,
            "purpose": "Smoke original sidecar entrypoint and validate adapter guards before full 5Y rerun.",
        },
        "contract": CONTRACT,
        "paths": {
            "stock_dir": rel(STOCK_DIR),
            "spx_path": rel(SPX_PATH),
            "regime_path": rel(REGIME_PATH),
        },
        "strategy_file_hashes_before": before_hashes,
        "strategy_file_hashes_after": after_hashes,
        "import_report": import_report,
        "sidecar_config": config_report,
        "composer_schema": composer_schema,
        "sidecar_run": sidecar_run,
        "sidecar_summary": sidecar_summary,
        "core_candidates": core_candidates,
        "validations": validations,
        "conclusion": conclusion,
        "recommended_next_action": recommended,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R Combined 5Y — 4C-2C-4C No-Strategy-Change Adapter Smoke")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append(f"Elapsed Seconds: `{report['elapsed_seconds']}`")
    md.append("")
    md.append("## Policy")
    md.append("```json")
    md.append(json.dumps(report["policy"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Contract")
    md.append("```json")
    md.append(json.dumps(CONTRACT, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Sidecar Summary")
    md.append("```json")
    md.append(json.dumps(sidecar_summary, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Core Candidates")
    md.append("```json")
    md.append(json.dumps(core_candidates, indent=2, ensure_ascii=False))
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
    md.append("")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("E1R_COMBINED_5Y_4C2C4C_NO_STRATEGY_CHANGE_ADAPTER_SMOKE_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("sidecar_config:", json.dumps(config_report, ensure_ascii=False))
    print("composer_schema:", json.dumps(composer_schema, ensure_ascii=False))
    print("sidecar_run:", json.dumps(sidecar_run, ensure_ascii=False))
    print("sidecar_summary:", json.dumps(sidecar_summary, ensure_ascii=False)[:12000])
    print("core_candidates:", json.dumps(core_candidates, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
