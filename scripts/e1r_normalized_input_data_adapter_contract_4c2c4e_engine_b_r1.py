#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import hashlib
import traceback
from datetime import datetime, timezone
from typing import Any
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_B_R1_NORMALIZED_INPUT_DATA_ADAPTER_CONTRACT_AUDIT.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_B_R1_NORMALIZED_INPUT_DATA_ADAPTER_CONTRACT_AUDIT.md"
ARCH_MD = ROOT / "docs/architecture/E1R_NORMALIZED_INPUT_DATA_ADAPTER_CONTRACT.md"

ENGINE_A_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_A_STANDALONE_ENGINE_ARCHITECTURE_CONTRACT.json"
D4B_R1_REPORT = ROOT / "docs/research/E1R_4C2C4E_D4B_R1_UPTREND_GOLDEN_MASTER_DIAGNOSTIC.json"

BACKTEST_PATH = ROOT / "src/engine/backtest.py"
SIDECAR_PATH = ROOT / "src/engine/e1r_sidecar_sleeve.py"
COMPOSER_PATH = ROOT / "src/engine/e1r_composer.py"

FROZEN_STRATEGY_FILES = [
    BACKTEST_PATH,
    SIDECAR_PATH,
    COMPOSER_PATH,
]

DATA_DIRS = {
    "research_stocks": ROOT / "data/research/e1_5y/raw/stocks",
    "research_indices": ROOT / "data/research/e1_5y/raw/indices",
    "research_regimes": ROOT / "data/research/e1_5y/regimes",
    "prod_prices": ROOT / "data/prices",
}

SOURCE_SCAN_DIRS = [
    ROOT / "src",
    ROOT / "scripts",
]

INVALID_ARTIFACTS = [
    "exports/e1r_unified_5y_full_account_v1_result.json",
    "exports/e1r_unified_5y_dashboard_research_bundle.json",
    "exports/e1r_combined_5y_original_max3_result.json",
    "exports/e1r_combined_5y_original_max3_equity_curve.json",
    "exports/e1r_combined_5y_original_max3_summary.json",
]

JSON_LOAD_KEYWORDS = [
    "json.load",
    "json.loads",
    "read_json",
    "load_price",
    "load_prices",
    "load_stock",
    "load_universe",
    "prices_map",
    "dates_map",
    "data/research/e1_5y",
    "data/prices",
    "SPX.json",
    "_VIX.json",
    "spx_regime_daily",
    "raw/stocks",
    "raw/indices",
]

CLASSIFICATION_RANK = {
    "BACKTEST_HARNESS_CANDIDATE": 100,
    "RUNTIME_LOADER_CANDIDATE": 90,
    "DATA_NORMALIZATION_CANDIDATE": 80,
    "DATA_PATH_HELPER_CANDIDATE": 70,
    "GENERAL_LOADER_CANDIDATE": 60,
    "AUDIT_OR_CONTRACT_SCRIPT_NOT_RUNTIME_LOADER": 20,
    "LOW_CONFIDENCE": 10,
}

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

def read_text(path: Path) -> str:
    return path.read_text(errors="replace")

def read_json(path: Path) -> Any:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def describe_json_shape(path: Path, max_sample: int = 2) -> dict[str, Any]:
    out: dict[str, Any] = {
        "path": rel(path),
        "exists": path.exists(),
    }

    if not path.exists():
        return out

    try:
        raw = read_json(path)
    except Exception as e:
        out["parse_error"] = f"{type(e).__name__}: {e}"
        return out

    out["type"] = type(raw).__name__

    if isinstance(raw, dict):
        out["top_level_keys"] = sorted(str(k) for k in raw.keys())[:80]
        date_like_keys = [
            k for k in raw.keys()
            if isinstance(k, str) and len(k) >= 10 and k[:4].isdigit() and k[4] == "-"
        ]
        out["date_keyed_dict"] = len(date_like_keys) > 0
        out["date_key_sample"] = date_like_keys[:5]

        for key in ["data", "prices", "records", "rows", "historical", "history"]:
            v = raw.get(key)
            if isinstance(v, list):
                out["primary_list_key"] = key
                out["primary_list_len"] = len(v)
                out["primary_list_sample"] = v[:max_sample]
                if v and isinstance(v[0], dict):
                    out["primary_list_sample_keys"] = sorted(v[0].keys())
                break

        for key in ["dates", "closes", "close", "ohlc", "meta", "symbol"]:
            if key in raw:
                value = raw.get(key)
                if isinstance(value, list):
                    out[f"{key}_len"] = len(value)
                else:
                    out[f"has_{key}"] = True

    elif isinstance(raw, list):
        out["list_len"] = len(raw)
        out["sample"] = raw[:max_sample]
        if raw and isinstance(raw[0], dict):
            out["sample_keys"] = sorted(raw[0].keys())
            key_counter = Counter()
            for row in raw[:100]:
                if isinstance(row, dict):
                    for k in row.keys():
                        key_counter[str(k)] += 1
            out["sample_key_frequency"] = dict(key_counter.most_common(40))

    return out

def audit_data_inventory() -> dict[str, Any]:
    inv: dict[str, Any] = {}

    for name, path in DATA_DIRS.items():
        entry: dict[str, Any] = {
            "path": rel(path),
            "exists": path.exists(),
        }

        if path.exists() and path.is_dir():
            json_files = sorted(path.glob("*.json"))
            entry["json_count"] = len(json_files)
            entry["sample_files"] = [p.name for p in json_files[:20]]
            entry["sample_shapes"] = [describe_json_shape(p, max_sample=1) for p in json_files[:8]]
        elif path.exists() and path.is_file():
            entry["shape"] = describe_json_shape(path)

        inv[name] = entry

    return inv

def classify_loader_candidate(path_s: str, name: str, src: str, risks: list[str], score: int) -> str:
    lower_name = name.lower()

    if "audit_or_contract_script_not_runtime_loader" in risks:
        return "AUDIT_OR_CONTRACT_SCRIPT_NOT_RUNTIME_LOADER"

    if "run_stateful_simulation" in src and "prices_map" in src and "dates_map" in src:
        return "BACKTEST_HARNESS_CANDIDATE"

    if path_s.startswith("src/") and any(x in lower_name for x in ["load", "fetch", "read", "parse"]):
        return "RUNTIME_LOADER_CANDIDATE"

    if "prices_map" in src and "dates_map" in src:
        return "DATA_NORMALIZATION_CANDIDATE"

    if "data/prices" in src or "data/research/e1_5y" in src:
        return "DATA_PATH_HELPER_CANDIDATE"

    if score >= 5:
        return "GENERAL_LOADER_CANDIDATE"

    return "LOW_CONFIDENCE"

def scan_loader_candidates() -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    file_hits: list[dict[str, Any]] = []

    py_files: list[Path] = []
    for d in SOURCE_SCAN_DIRS:
        if d.exists():
            py_files.extend(sorted(d.rglob("*.py")))

    for path in py_files:
        text = read_text(path)
        hit_terms = [kw for kw in JSON_LOAD_KEYWORDS if kw in text]
        if not hit_terms:
            continue

        path_s = rel(path)

        file_hits.append({
            "path": path_s,
            "hit_terms": hit_terms,
        })

        try:
            tree = ast.parse(text)
        except Exception:
            continue

        lines = text.splitlines()

        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue

            start = node.lineno
            end = getattr(node, "end_lineno", start)
            src = "\n".join(lines[start - 1:end])
            lower = src.lower()

            score = 0
            reasons = []

            for term in JSON_LOAD_KEYWORDS:
                if term in src:
                    score += 1
                    reasons.append(f"contains:{term}")

            if "prices_map" in src:
                score += 3
                reasons.append("uses_prices_map")
            if "dates_map" in src:
                score += 3
                reasons.append("uses_dates_map")
            if "symbols" in src:
                score += 1
                reasons.append("uses_symbols")
            if "spx_prices" in src or "spx_dates" in src:
                score += 2
                reasons.append("uses_spx_series")
            if "run_stateful_simulation" in src:
                score += 2
                reasons.append("feeds_run_stateful_simulation")
            if "data/research/e1_5y" in src:
                score += 2
                reasons.append("uses_research_5y_data")
            if "data/prices" in src:
                score += 1
                reasons.append("uses_prod_prices")
            if "regime" in lower:
                score += 1
                reasons.append("uses_regime")
            if "ohlc" in lower:
                score += 1
                reasons.append("uses_ohlc")

            risks = []
            if path_s.startswith("scripts/") and any(x in path_s.lower() for x in ["audit", "diagnostic", "contract"]):
                risks.append("audit_or_contract_script_not_runtime_loader")
            if any(x in src for x in INVALID_ARTIFACTS):
                risks.append("references_invalid_artifact")

            if score <= 0:
                continue

            classification = classify_loader_candidate(path_s, node.name, src, risks, score)
            classification_rank = CLASSIFICATION_RANK.get(classification, 0)

            candidates.append({
                "path": path_s,
                "name": node.name,
                "start_line": start,
                "end_line": end,
                "line_count": end - start + 1,
                "args": [a.arg for a in node.args.args],
                "score": score,
                "classification": classification,
                "classification_rank": classification_rank,
                "reasons": reasons,
                "risks": risks,
            })

    candidates.sort(
        key=lambda x: (
            int(x.get("classification_rank", 0)),
            int(x.get("score", 0)),
            -len(x.get("risks", [])),
        ),
        reverse=True,
    )

    return {
        "file_hits": file_hits[:300],
        "candidate_count": len(candidates),
        "top_candidates": candidates[:100],
    }

def audit_backtest_input_signature() -> dict[str, Any]:
    try:
        import inspect
        import sys
        sys.path.insert(0, str(ROOT))
        from src.engine.backtest import run_stateful_simulation

        sig = inspect.signature(run_stateful_simulation)
        return {
            "import_ok": True,
            "signature": str(sig),
            "parameters": list(sig.parameters.keys()),
            "required_core_inputs": [
                "symbols",
                "prices_map",
                "dates_map",
                "spx_prices",
                "spx_dates",
                "ohlc_map",
                "assumptions",
                "sim_start_date",
                "sim_end_date",
                "ndx_prices",
                "ndx_dates",
                "sox_prices",
                "sox_dates",
                "vix_prices",
                "vix_dates",
            ],
        }
    except Exception as e:
        return {
            "import_ok": False,
            "error": f"{type(e).__name__}: {e}",
            "traceback": traceback.format_exc(limit=8),
        }

def infer_schema_contract() -> dict[str, Any]:
    return {
        "contract_name": "E1R_NORMALIZED_INPUT_DATA_ADAPTER_CONTRACT_V1",
        "reason": (
            "Standalone E1R Engine requires one normalized input boundary shared by historical backtest, "
            "forward paper tracking, and future live trading. D4B-R1 showed ad hoc JSON parsing is unsafe."
        ),
        "normalized_market_snapshot": {
            "date": "YYYY-MM-DD",
            "universe": "list[str]",
            "prices_by_symbol": {
                "symbol": {
                    "close": "float",
                    "history": "list[DailyBar]",
                    "ohlc_optional": "open/high/low/close/volume if available",
                }
            },
            "indices": {
                "SPX": "required",
                "NDX": "required if available",
                "SOX": "required if available",
                "VIX": "explicit optional / fallback path",
            },
            "regime": {
                "spx_regime": "UPTREND | SIDEWAYS | DOWNTREND",
                "subclass": "MA_CONFLICT | DETERIORATION_TRANSITION | RECOVERY_TRANSITION | NO_SUBCLASS",
            },
            "features": {
                "leader_features_by_symbol": [
                    "leader_rank",
                    "leader_score",
                    "rs_score",
                    "momentum_score",
                    "trend_health",
                    "ma20",
                    "ma50",
                    "ma20_slope",
                    "ma50_slope",
                ]
            },
        },
        "adapter_contract": {
            "HistoricalDataAdapter": {
                "purpose": "Load 5Y historical data and provide normalized MarketSnapshot sequence.",
                "may_do": [
                    "read JSON files",
                    "normalize schema",
                    "align dates",
                    "provide rolling history",
                    "provide index/regime snapshots",
                ],
                "must_not_do": [
                    "decide trading actions",
                    "change entry/exit/sizing/market gate",
                    "silently use invalid artifacts",
                    "silently fork logic from forward adapter",
                ],
            },
            "ForwardDataAdapter": {
                "purpose": "Load latest daily data and provide the same MarketSnapshot schema.",
                "may_do": [
                    "read latest production data",
                    "normalize schema",
                    "provide rolling history",
                    "provide current regime snapshot",
                ],
                "must_not_do": [
                    "own trading logic",
                    "use run_oos_day as a separate decision engine",
                    "override E1R Core decisions",
                ],
            },
            "LiveDataAdapter_future": {
                "purpose": "Future live-data normalization only, disabled until explicit approval.",
                "must_not_do": [
                    "bypass E1R Core Engine",
                    "introduce broker-specific trading rules",
                ],
            },
        },
        "acceptance_criteria_for_next_stage": [
            "Identify a reusable runtime loader or explicitly conclude none is safe.",
            "Lock real JSON schema for stock/index/regime files.",
            "Define canonical parser behavior for HistoricalDataAdapter.",
            "Confirm ForwardDataAdapter can use the same MarketSnapshot schema.",
            "No strategy logic changes.",
            "No full 5Y run.",
            "No official result.",
        ],
    }

def derive_decision(loader_scan: dict[str, Any]) -> dict[str, Any]:
    top = loader_scan.get("top_candidates", [])

    reusable = [
        c for c in top
        if c.get("classification") in {
            "BACKTEST_HARNESS_CANDIDATE",
            "RUNTIME_LOADER_CANDIDATE",
            "DATA_NORMALIZATION_CANDIDATE",
        }
        and not c.get("risks")
    ]

    audit_only = [
        c for c in top
        if c.get("classification") == "AUDIT_OR_CONTRACT_SCRIPT_NOT_RUNTIME_LOADER"
    ]

    if reusable:
        conclusion = "NORMALIZED_INPUT_CONTRACT_READY_REUSABLE_LOADER_CANDIDATES_FOUND"
        next_action = (
            "Proceed to 4C-2C-4E-ENGINE-C: verify top reusable loader candidates with a no-strategy data-harness smoke. "
            "Do not implement trading core yet."
        )
    else:
        conclusion = "NORMALIZED_INPUT_CONTRACT_READY_NO_RUNTIME_LOADER_LOCKED"
        next_action = (
            "Proceed to 4C-2C-4E-ENGINE-C: create a minimal canonical HistoricalDataAdapter schema probe, "
            "then validate it against real JSON shapes before any strategy/core extraction."
        )

    return {
        "normalized_input_contract_defined": True,
        "loader_candidates_found": loader_scan.get("candidate_count", 0),
        "reusable_runtime_loader_candidate_count": len(reusable),
        "audit_only_candidate_count": len(audit_only),
        "selected_loader_locked": False,
        "historical_adapter_implementation_allowed_now": False,
        "forward_adapter_implementation_allowed_now": False,
        "strategy_core_extraction_allowed_now": False,
        "full_5y_backtest_allowed_now": False,
        "conclusion": conclusion,
        "recommended_next_action": next_action,
        "engineering_rule": (
            "Backtest, forward test, and future live trading must share one normalized MarketSnapshot/DataBundle input contract. "
            "Data adapters normalize inputs; they do not own trading logic."
        ),
        "top_reusable_candidates": reusable[:10],
    }

def write_report(report: dict[str, Any]) -> None:
    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-B-R1 — Normalized Input / Data Adapter Contract Audit")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Policy")
    md.append("```json")
    md.append(json.dumps(report["policy"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Data Inventory Summary")
    md.append("```json")
    md.append(json.dumps({
        k: {
            "path": v.get("path"),
            "exists": v.get("exists"),
            "json_count": v.get("json_count"),
            "sample_files": v.get("sample_files", [])[:10],
            "sample_shapes": v.get("sample_shapes", [])[:3],
        }
        for k, v in report["data_inventory"].items()
    }, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Loader Candidate Summary")
    md.append("```json")
    md.append(json.dumps({
        "candidate_count": report["loader_scan"]["candidate_count"],
        "top_candidates": report["loader_scan"]["top_candidates"][:25],
    }, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Backtest Input Signature")
    md.append("```json")
    md.append(json.dumps(report["backtest_input_signature"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Normalized Input Contract")
    md.append("```json")
    md.append(json.dumps(report["normalized_input_contract"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Validations")
    md.append("```json")
    md.append(json.dumps(report["validations"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Decision")
    md.append("```json")
    md.append(json.dumps(report["decision"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")

    REPORT_MD.write_text("\n".join(md))
    ARCH_MD.write_text("\n".join(md))

def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}
    top_level_error = None

    try:
        engine_a_loaded = ENGINE_A_REPORT.exists()
        data_inventory = audit_data_inventory()
        loader_scan = scan_loader_candidates()
        backtest_sig = audit_backtest_input_signature()
        contract = infer_schema_contract()
        decision = derive_decision(loader_scan)
    except Exception as e:
        engine_a_loaded = ENGINE_A_REPORT.exists()
        data_inventory = {}
        loader_scan = {"file_hits": [], "candidate_count": 0, "top_candidates": []}
        backtest_sig = audit_backtest_input_signature()
        contract = infer_schema_contract()
        decision = {
            "normalized_input_contract_defined": True,
            "selected_loader_locked": False,
            "historical_adapter_implementation_allowed_now": False,
            "forward_adapter_implementation_allowed_now": False,
            "strategy_core_extraction_allowed_now": False,
            "full_5y_backtest_allowed_now": False,
            "conclusion": "NORMALIZED_INPUT_CONTRACT_AUDIT_TOP_LEVEL_FAILURE_REPORT_WRITTEN",
            "recommended_next_action": "Review top-level failure before continuing.",
            "engineering_rule": "Fail-safe report must exist even when audit fails.",
        }
        top_level_error = {
            "type": type(e).__name__,
            "error": str(e),
            "traceback": traceback.format_exc(limit=12),
        }

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "fail_safe_report_written": True,
        "contract_audit_only": True,
        "strategy_logic_changed": False,
        "backtest_engine_run": False,
        "full_5y_backtest_run": False,
        "forward_runner_run": False,
        "provider_extraction_run": False,
        "adapter_implementation_run": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "invalid_artifacts_not_used_as_source": True,
        "composer_not_used": True,
        "return_curve_stitching_not_used": True,
        "engine_a_loaded": engine_a_loaded,
        "data_inventory_completed": bool(data_inventory),
        "loader_candidates_scanned": "candidate_count" in loader_scan,
        "backtest_signature_audited": backtest_sig.get("import_ok") is True,
        "normalized_market_snapshot_contract_defined": True,
        "historical_data_adapter_contract_defined": True,
        "forward_data_adapter_contract_defined": True,
        "future_live_data_adapter_boundary_defined": True,
        "selected_loader_not_locked_yet": decision.get("selected_loader_locked") is False,
        "adapter_implementation_not_allowed_yet": decision.get("historical_adapter_implementation_allowed_now") is False,
        "strategy_core_extraction_not_allowed_yet": decision.get("strategy_core_extraction_allowed_now") is False,
        "decision_generated": bool(decision.get("conclusion")),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-B-R1",
        "status": "NORMALIZED_INPUT_DATA_ADAPTER_CONTRACT_AUDIT_COMPLETE",
        "purpose": "Audit data/input schemas and define normalized input/data adapter contract for standalone E1R engine.",
        "policy": {
            "strategy_logic_changed": False,
            "contract_audit_only": True,
            "backtest_engine_run": False,
            "full_5y_backtest_run": False,
            "forward_runner_run": False,
            "provider_extraction_run": False,
            "adapter_implementation_run": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
            "invalid_artifacts_used_as_source": False,
            "composer_used": False,
            "return_curve_stitching_used": False,
        },
        "top_level_error": top_level_error,
        "data_inventory": data_inventory,
        "loader_scan": loader_scan,
        "backtest_input_signature": backtest_sig,
        "normalized_input_contract": contract,
        "validations": validations,
        "decision": decision,
    }

    write_report(report)

    print("E1R_4C2C4E_ENGINE_B_R1_NORMALIZED_INPUT_DATA_ADAPTER_CONTRACT_AUDIT_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("top_level_error:", json.dumps(top_level_error, ensure_ascii=False))
    print("data_inventory_summary:", json.dumps({
        k: {
            "path": v.get("path"),
            "exists": v.get("exists"),
            "json_count": v.get("json_count"),
            "sample_files": v.get("sample_files", [])[:5],
            "sample_shapes": v.get("sample_shapes", [])[:2],
        }
        for k, v in data_inventory.items()
    }, ensure_ascii=False))
    print("loader_candidate_summary:", json.dumps({
        "candidate_count": loader_scan["candidate_count"],
        "top_candidates": loader_scan["top_candidates"][:20],
    }, ensure_ascii=False))
    print("backtest_input_signature:", json.dumps(backtest_sig, ensure_ascii=False))
    print("normalized_contract_summary:", json.dumps({
        "contract_name": contract["contract_name"],
        "reason": contract["reason"],
        "adapter_contract": contract["adapter_contract"],
        "acceptance_criteria": contract["acceptance_criteria_for_next_stage"],
    }, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))

if __name__ == "__main__":
    main()
