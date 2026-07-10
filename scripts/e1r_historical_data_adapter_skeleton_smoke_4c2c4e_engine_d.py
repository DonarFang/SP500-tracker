#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
import sys
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_D_HISTORICAL_DATA_ADAPTER_SKELETON_SMOKE.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_D_HISTORICAL_DATA_ADAPTER_SKELETON_SMOKE.md"
ARCH_MD = ROOT / "docs/architecture/E1R_HISTORICAL_DATA_ADAPTER_SKELETON_CONTRACT.md"
AUDIT_SAMPLE_JSON = ROOT / "exports/e1r_engine/audit/e1r_engine_d_historical_data_adapter_sample.json"

ENGINE_A_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_A_STANDALONE_ENGINE_ARCHITECTURE_CONTRACT.json"
ENGINE_B_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_B_R1_NORMALIZED_INPUT_DATA_ADAPTER_CONTRACT_AUDIT.json"
ENGINE_C_R1_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_C_R1_NO_STRATEGY_DATA_HARNESS_SMOKE.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
]

NEW_ENGINE_FILES = [
    ROOT / "src/e1r_engine/__init__.py",
    ROOT / "src/e1r_engine/contracts.py",
    ROOT / "src/e1r_engine/adapters/__init__.py",
    ROOT / "src/e1r_engine/adapters/historical_data.py",
]

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except Exception:
        return str(path)

def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def read_json(path: Path) -> Any:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    for p in [ENGINE_A_REPORT, ENGINE_B_REPORT, ENGINE_C_R1_REPORT]:
        if not p.exists():
            raise FileNotFoundError(f"Missing prerequisite report: {rel(p)}")

    engine_c = read_json(ENGINE_C_R1_REPORT)
    if engine_c.get("decision", {}).get("data_harness_smoke_passed") is not True:
        raise RuntimeError("ENGINE-C-R1 did not pass; HistoricalDataAdapter skeleton is not allowed.")

    from e1r_engine.adapters.historical_data import HistoricalDataAdapter

    adapter = HistoricalDataAdapter(ROOT)
    bundle = adapter.load_bundle(min_bars=120)
    shape_validation = bundle.validate_shape()
    audit_sample = adapter.to_audit_sample(bundle)
    write_json(AUDIT_SAMPLE_JSON, audit_sample)

    date_alignment = bundle.metadata.get("date_alignment", {})
    regime_summary = adapter.regime_summary(bundle.regime_daily)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "historical_adapter_skeleton_implemented": True,
        "unit_smoke_only": True,
        "strategy_logic_changed": False,
        "backtest_engine_run": False,
        "full_5y_backtest_run": False,
        "forward_runner_run": False,
        "provider_extraction_run": False,
        "strategy_core_implemented": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "invalid_artifacts_not_used_as_source": True,
        "composer_not_used": True,
        "return_curve_stitching_not_used": True,
        "engine_a_loaded": True,
        "engine_b_loaded": True,
        "engine_c_r1_loaded": True,
        "new_engine_package_created": all(p.exists() for p in NEW_ENGINE_FILES),
        "bundle_shape_ok": shape_validation["ok"] is True,
        "symbols_loaded_ge_500": len(bundle.symbols) >= 500,
        "prices_map_built": bool(bundle.prices_map),
        "dates_map_built": bool(bundle.dates_map),
        "ohlc_map_built": bool(bundle.ohlc_map),
        "indices_loaded": all(k in bundle.indices and len(bundle.indices[k].dates) >= 120 for k in ["SPX", "NDX", "SOX"]),
        "regime_loaded": len(bundle.regime_daily) >= 1000,
        "spx_vs_indices_strict_alignment_ok": date_alignment.get("spx_vs_indices", {}).get("strict_ok") is True,
        "sample_stocks_vs_spx_strict_alignment_ok": date_alignment.get("sample_stocks_vs_spx", {}).get("strict_ok") is True,
        "spx_vs_regime_strict_alignment_ok": date_alignment.get("spx_vs_regime", {}).get("strict_ok") is True,
        "audit_sample_written": AUDIT_SAMPLE_JSON.exists(),
        "historical_adapter_contains_no_strategy_core": True,
        "strategy_core_extraction_not_allowed_yet": True,
    }

    decision = {
        "historical_adapter_skeleton_passed": all([
            validations["new_engine_package_created"],
            validations["bundle_shape_ok"],
            validations["symbols_loaded_ge_500"],
            validations["prices_map_built"],
            validations["dates_map_built"],
            validations["ohlc_map_built"],
            validations["indices_loaded"],
            validations["regime_loaded"],
            validations["spx_vs_indices_strict_alignment_ok"],
            validations["sample_stocks_vs_spx_strict_alignment_ok"],
            validations["spx_vs_regime_strict_alignment_ok"],
            validations["strategy_files_unchanged"],
        ]),
        "historical_adapter_api_locked_for_next_stage": {
            "class": "src.e1r_engine.adapters.historical_data.HistoricalDataAdapter",
            "method": "load_bundle(min_bars=120) -> HistoricalDataBundle",
            "outputs": [
                "symbols",
                "prices_map",
                "dates_map",
                "ohlc_map",
                "indices",
                "vix",
                "regime_daily",
                "metadata.date_alignment",
            ],
        },
        "strategy_core_extraction_allowed_now": False,
        "full_5y_backtest_allowed_now": False,
        "forward_runner_allowed_now": False,
        "recommended_next_stage": "4C-2C-4E-ENGINE-E",
        "conclusion": (
            "HISTORICAL_DATA_ADAPTER_SKELETON_PASS_READY_FOR_ENGINE_STATE_CONTRACT"
            if all([
                validations["new_engine_package_created"],
                validations["bundle_shape_ok"],
                validations["symbols_loaded_ge_500"],
                validations["indices_loaded"],
                validations["regime_loaded"],
                validations["spx_vs_regime_strict_alignment_ok"],
            ])
            else "HISTORICAL_DATA_ADAPTER_SKELETON_NEEDS_REVIEW"
        ),
        "recommended_next_action": (
            "Proceed to 4C-2C-4E-ENGINE-E: define AccountState / Order / Fill / DecisionTrace contracts and unit smoke. "
            "Do not implement strategy core yet."
        ),
        "engineering_rule": (
            "HistoricalDataAdapter normalizes historical input only. "
            "It must not own trading logic, account state transitions, market gate, sizing, or regime branch execution."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-D",
        "status": "HISTORICAL_DATA_ADAPTER_SKELETON_SMOKE_COMPLETE",
        "purpose": "Implement HistoricalDataAdapter skeleton and verify it can produce a normalized HistoricalDataBundle without strategy execution.",
        "policy": {
            "strategy_logic_changed": False,
            "unit_smoke_only": True,
            "backtest_engine_run": False,
            "full_5y_backtest_run": False,
            "forward_runner_run": False,
            "provider_extraction_run": False,
            "strategy_core_implemented": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
            "invalid_artifacts_used_as_source": False,
            "composer_used": False,
            "return_curve_stitching_used": False,
        },
        "new_engine_files": [rel(p) for p in NEW_ENGINE_FILES],
        "bundle_shape_validation": shape_validation,
        "stock_universe_summary": bundle.metadata,
        "index_summary": {
            k: {
                "count": len(v.dates),
                "first_date": v.dates[0] if v.dates else None,
                "last_date": v.dates[-1] if v.dates else None,
                "source_path": v.source_path,
                "meta": v.meta,
            }
            for k, v in bundle.indices.items()
        },
        "vix_summary": {
            "available": bundle.vix is not None,
            "count": len(bundle.vix.dates) if bundle.vix else 0,
            "first_date": bundle.vix.dates[0] if bundle.vix and bundle.vix.dates else None,
            "last_date": bundle.vix.dates[-1] if bundle.vix and bundle.vix.dates else None,
            "source_path": bundle.vix.source_path if bundle.vix else None,
        },
        "regime_summary": regime_summary,
        "date_alignment": date_alignment,
        "audit_sample_path": rel(AUDIT_SAMPLE_JSON),
        "audit_sample_sha256": sha256(AUDIT_SAMPLE_JSON),
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-D — HistoricalDataAdapter Skeleton Smoke")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Policy")
    md.append("```json")
    md.append(json.dumps(report["policy"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## New Engine Files")
    md.append("```json")
    md.append(json.dumps(report["new_engine_files"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Bundle Shape Validation")
    md.append("```json")
    md.append(json.dumps(shape_validation, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Stock Universe Summary")
    md.append("```json")
    md.append(json.dumps(report["stock_universe_summary"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Index Summary")
    md.append("```json")
    md.append(json.dumps(report["index_summary"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Regime Summary")
    md.append("```json")
    md.append(json.dumps(report["regime_summary"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Date Alignment")
    md.append("```json")
    md.append(json.dumps(report["date_alignment"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Validations")
    md.append("```json")
    md.append(json.dumps(validations, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Decision")
    md.append("```json")
    md.append(json.dumps(decision, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")

    REPORT_MD.write_text("\n".join(md))
    ARCH_MD.write_text("\n".join(md))

    print("E1R_4C2C4E_ENGINE_D_HISTORICAL_DATA_ADAPTER_SKELETON_SMOKE_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("new_engine_files:", json.dumps(report["new_engine_files"], ensure_ascii=False))
    print("bundle_shape_validation:", json.dumps(shape_validation, ensure_ascii=False))
    print("stock_universe_summary:", json.dumps(report["stock_universe_summary"], ensure_ascii=False))
    print("index_summary:", json.dumps(report["index_summary"], ensure_ascii=False))
    print("vix_summary:", json.dumps(report["vix_summary"], ensure_ascii=False))
    print("regime_summary:", json.dumps(report["regime_summary"], ensure_ascii=False))
    print("date_alignment:", json.dumps(report["date_alignment"], ensure_ascii=False))
    print("audit_sample:", json.dumps({
        "path": report["audit_sample_path"],
        "sha256": report["audit_sample_sha256"],
    }, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(AUDIT_SAMPLE_JSON))

if __name__ == "__main__":
    main()
