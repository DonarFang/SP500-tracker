#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import hashlib
import inspect
import importlib
import sys
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_A_CONTINUOUS_STATEFUL_DESIGN_AUDIT.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_A_CONTINUOUS_STATEFUL_DESIGN_AUDIT.md"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

INVALID_ARTIFACTS = [
    "exports/e1r_unified_5y_full_account_v1_result.json",
    "exports/e1r_unified_5y_dashboard_research_bundle.json",
    "exports/e1r_combined_5y_original_max3_result.json",
    "exports/e1r_combined_5y_original_max3_equity_curve.json",
    "exports/e1r_combined_5y_original_max3_summary.json",
]

CONTRACT = {
    "stage": "4C-2C-4E-A",
    "purpose": "Design audit for official E1R continuous stateful 5Y backtest.",
    "formal_backtest_definition": {
        "model": "single-account continuous stateful backtest",
        "timeline": "one continuous trading-day timeline",
        "state": ["cash", "positions", "total_equity"],
        "daily_logic": [
            "mark existing account state",
            "read daily regime",
            "execute the validated branch for that regime",
            "enforce global live account holdings <= 3",
            "record daily account state"
        ],
    },
    "required_regime_contract": {
        "UPTREND": "validated UPTREND branch",
        "SIDEWAYS_MA_CONFLICT": "validated sidecar branch input; Top10 is candidate/basket only; live account holdings <= 3",
        "DETERIORATION_TRANSITION": "cash/defensive",
        "RECOVERY_TRANSITION": "cash/defensive",
        "DOWNTREND": "cash/defensive",
    },
    "not_allowed": [
        "Do not stitch UPTREND result curve with SIDEWAYS sidecar result curve.",
        "Do not use invalid historical artifacts as core source.",
        "Do not use composer output as formal E1R result if it only composes interval returns.",
        "Do not modify frozen strategy files in this audit.",
        "Do not generate official E1R result in this audit.",
        "Do not run full 5Y backtest in this audit.",
    ],
}

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))

def sha256(p: Path) -> str | None:
    if not p.exists():
        return None
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def read_text(path: Path) -> str:
    return path.read_text(errors="replace")

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def import_signature(module_name: str, object_name: str) -> dict[str, Any]:
    try:
        sys.path.insert(0, str(ROOT))
        mod = importlib.import_module(module_name)
        obj = getattr(mod, object_name)
        return {
            "ok": True,
            "module": module_name,
            "object": object_name,
            "signature": str(inspect.signature(obj)),
            "error": None,
        }
    except Exception as exc:
        return {
            "ok": False,
            "module": module_name,
            "object": object_name,
            "signature": None,
            "error": type(exc).__name__ + ": " + str(exc),
        }

def parse_function_summaries(path: Path) -> dict[str, Any]:
    text = read_text(path)
    tree = ast.parse(text)
    lines = text.splitlines()

    summaries = {}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        start = getattr(node, "lineno", None)
        end = getattr(node, "end_lineno", None)
        source = "\n".join(lines[start - 1:end]) if start and end else ""

        summaries[node.name] = {
            "start_line": start,
            "end_line": end,
            "line_count": end - start + 1 if start and end else None,
            "args": [a.arg for a in node.args.args],
            "contains_cash": "cash" in source,
            "contains_positions": "positions" in source or "open_positions" in source,
            "contains_total_equity": "total_equity" in source or "equity" in source,
            "contains_daily_records": "daily_records" in source or "daily_equity_records" in source,
            "contains_mark_to_market_terms": any(
                x in source for x in ["positions_value", "market_value", "total_equity", "mark"]
            ),
            "contains_max_positions": "max_positions" in source,
            "contains_open_positions_count": "open_positions_count" in source,
            "contains_regime": "regime" in source or "spx_regime" in source,
            "contains_e1r": "e1r" in source.lower(),
            "contains_uptrend": "UPTREND" in source,
            "contains_sideways": "SIDEWAYS" in source,
            "contains_downtrend": "DOWNTREND" in source,
            "contains_ma_conflict": "MA_CONFLICT" in source,
        }

    return summaries

def string_hits(path: Path, patterns: list[str], max_hits_per_pattern: int = 20) -> dict[str, list[dict[str, Any]]]:
    text = read_text(path)
    lines = text.splitlines()
    result = {}

    for pat in patterns:
        hits = []
        for i, line in enumerate(lines, start=1):
            if pat in line:
                hits.append({
                    "line": i,
                    "text": line.strip()[:240],
                })
        result[pat] = hits[:max_hits_per_pattern]

    return result

def audit_backtest_engine() -> dict[str, Any]:
    path = ROOT / "src/engine/backtest.py"
    funcs = parse_function_summaries(path)
    run_info = funcs.get("run_stateful_simulation", {})

    patterns = [
        "run_stateful_simulation",
        "cash",
        "positions",
        "total_equity",
        "positions_value",
        "daily_records",
        "daily_equity_records",
        "open_positions_count",
        "max_positions",
        "e1r",
        "regime",
        "spx_regime",
        "UPTREND",
        "SIDEWAYS",
        "DOWNTREND",
        "MA_CONFLICT",
        "BUY",
        "EXIT",
        "REDUCE",
        "leader_score",
    ]

    requirements = {
        "has_run_stateful_simulation": "run_stateful_simulation" in funcs,
        "state_container_has_cash_and_positions": bool(run_info.get("contains_cash") and run_info.get("contains_positions")),
        "records_daily_account_state": bool(run_info.get("contains_daily_records")),
        "has_mark_to_market_terms": bool(run_info.get("contains_mark_to_market_terms")),
        "has_max_positions_reference": bool(run_info.get("contains_max_positions")),
        "has_open_positions_count_reference": bool(run_info.get("contains_open_positions_count")),
        "has_regime_reference": bool(run_info.get("contains_regime")),
        "has_e1r_reference": bool(run_info.get("contains_e1r")),
        "has_uptrend_reference": bool(run_info.get("contains_uptrend")),
        "has_sideways_reference": bool(run_info.get("contains_sideways")),
        "has_downtrend_reference": bool(run_info.get("contains_downtrend")),
    }

    return {
        "path": rel(path),
        "signature": import_signature("src.engine.backtest", "run_stateful_simulation"),
        "run_stateful_simulation_summary": run_info,
        "requirements": requirements,
        "string_hits": string_hits(path, patterns),
    }

def audit_sidecar() -> dict[str, Any]:
    path = ROOT / "src/engine/e1r_sidecar_sleeve.py"
    funcs = parse_function_summaries(path)
    build_info = funcs.get("build_e1r_sidecar_sleeve", {})

    patterns = [
        "E1RSidecarConfig",
        "build_e1r_sidecar_sleeve",
        "allowed_subclasses",
        "MA_CONFLICT",
        "top_n",
        "gross_exposure",
        "candidate_count",
        "selected_count",
        "holdings",
        "is_active",
        "portfolio_return",
        "raw_return",
        "weighted_contribution",
    ]

    text = read_text(path)

    requirements = {
        "has_sidecar_config": "E1RSidecarConfig" in text,
        "has_sidecar_builder": "build_e1r_sidecar_sleeve" in funcs,
        "has_allowed_subclasses": "allowed_subclasses" in text,
        "has_ma_conflict_reference": "MA_CONFLICT" in text,
        "has_top_n_reference": "top_n" in text,
        "has_gross_exposure_reference": "gross_exposure" in text,
        "has_candidate_count_reference": "candidate_count" in text,
        "has_selected_count_reference": "selected_count" in text,
        "has_holdings_reference": "holdings" in text,
        "has_is_active_reference": "is_active" in text,
        "sidecar_can_provide_branch_candidate_data": all([
            "build_e1r_sidecar_sleeve" in funcs,
            "MA_CONFLICT" in text,
            "holdings" in text,
            "selected_count" in text,
            "gross_exposure" in text,
            "is_active" in text,
        ]),
    }

    return {
        "path": rel(path),
        "signature_config": import_signature("src.engine.e1r_sidecar_sleeve", "E1RSidecarConfig"),
        "signature_builder": import_signature("src.engine.e1r_sidecar_sleeve", "build_e1r_sidecar_sleeve"),
        "build_function_summary": build_info,
        "requirements": requirements,
        "string_hits": string_hits(path, patterns),
    }

def audit_composer() -> dict[str, Any]:
    path = ROOT / "src/engine/e1r_composer.py"
    funcs = parse_function_summaries(path)

    patterns = [
        "compose_e1r_v0_2_variant",
        "extract_core_interval_returns",
        "build_equity_records_from_returns",
        "interval",
        "return",
        "equity",
        "records",
    ]

    policy = {
        "allowed_for_official_continuous_stateful_result": False,
        "reason": (
            "Composer functions appear to compose interval returns/equity records. "
            "Official 4E requires one account with continuous cash/positions, not stitched result curves."
        ),
    }

    wanted = [
        "compose_e1r_v0_2_variant",
        "extract_core_interval_returns",
        "build_equity_records_from_returns",
    ]

    return {
        "path": rel(path),
        "signatures": {
            name: import_signature("src.engine.e1r_composer", name)
            for name in wanted
        },
        "function_summaries": {
            name: funcs.get(name)
            for name in wanted
        },
        "formal_use_policy": policy,
        "string_hits": string_hits(path, patterns),
    }

def audit_invalid_artifacts() -> dict[str, Any]:
    items = []
    for name in INVALID_ARTIFACTS:
        path = ROOT / name
        item = {
            "path": name,
            "exists": path.exists(),
            "must_not_use_as_official_source": True,
            "summary": None,
        }

        if path.exists() and path.suffix == ".json":
            try:
                obj = json.loads(path.read_text())
                if isinstance(obj, dict):
                    item["summary"] = {
                        "top_keys": sorted(obj.keys())[:40],
                        "status": obj.get("status"),
                        "strategy_variant": obj.get("strategy_variant"),
                        "version": obj.get("version"),
                        "conclusion": obj.get("conclusion"),
                    }
            except Exception as exc:
                item["summary"] = {
                    "read_error": type(exc).__name__ + ": " + str(exc)
                }

        items.append(item)

    return {
        "policy": (
            "These artifacts are historical/diagnostic only. "
            "Official 4E continuous stateful backtest must not read them as strategy/core sources."
        ),
        "items": items,
    }

def derive_decision(backtest: dict[str, Any], sidecar: dict[str, Any]) -> dict[str, Any]:
    b = backtest["requirements"]
    s = sidecar["requirements"]

    engine_can_hold_single_account_state = all([
        b["has_run_stateful_simulation"],
        b["state_container_has_cash_and_positions"],
        b["records_daily_account_state"],
        b["has_mark_to_market_terms"],
        b["has_max_positions_reference"],
        b["has_open_positions_count_reference"],
    ])

    engine_has_regime_wiring_terms = all([
        b["has_regime_reference"],
        b["has_e1r_reference"],
        b["has_uptrend_reference"],
        b["has_sideways_reference"],
        b["has_downtrend_reference"],
    ])

    sidecar_can_supply_sideways_branch_data = bool(s["sidecar_can_provide_branch_candidate_data"])

    if engine_can_hold_single_account_state and engine_has_regime_wiring_terms and sidecar_can_supply_sideways_branch_data:
        conclusion = "READY_FOR_4C2C4E_B_CONTINUOUS_STATEFUL_SMOKE"
        next_action = (
            "Create a small continuous-stateful smoke/prototype that owns one account state, "
            "does not read invalid artifacts, does not stitch curves, and validates max open positions <= 3."
        )
    elif engine_can_hold_single_account_state and sidecar_can_supply_sideways_branch_data:
        conclusion = "NEEDS_EXPLICIT_CONTINUOUS_STATEFUL_ADAPTER_DESIGN"
        next_action = (
            "Create a new adapter script/module that owns cash/positions and calls branch logic/signals. "
            "Do not modify frozen strategy files unless explicitly approved."
        )
    else:
        conclusion = "BLOCKED_NEED_ENTRYPOINT_REVIEW"
        next_action = (
            "Do not run full 5Y. First locate exact UPTREND branch entrypoint and state transition mechanism."
        )

    return {
        "engine_can_hold_single_account_state": engine_can_hold_single_account_state,
        "engine_has_regime_wiring_terms": engine_has_regime_wiring_terms,
        "sidecar_can_supply_sideways_branch_data": sidecar_can_supply_sideways_branch_data,
        "composer_allowed_for_formal_result": False,
        "invalid_artifacts_allowed_as_source": False,
        "conclusion": conclusion,
        "recommended_next_action": next_action,
    }

def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    backtest = audit_backtest_engine()
    sidecar = audit_sidecar()
    composer = audit_composer()
    invalid_artifacts = audit_invalid_artifacts()
    decision = derive_decision(backtest, sidecar)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "audit_only_no_full_backtest_run": True,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "invalid_artifacts_not_used_as_source": True,
        "composer_not_allowed_for_formal_result_stitching": True,
        "continuous_stateful_required": True,
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-A",
        "status": "CONTINUOUS_STATEFUL_DESIGN_AUDIT_COMPLETE",
        "contract": CONTRACT,
        "policy": {
            "strategy_logic_changed": False,
            "backtest_engine_run": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
        },
        "validations": validations,
        "audits": {
            "backtest_engine": backtest,
            "sidecar": sidecar,
            "composer": composer,
            "invalid_artifacts": invalid_artifacts,
        },
        "design_decision": decision,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-A — Continuous Stateful 5Y Backtest Design Audit")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("This is a design audit only. It does not run a full 5Y backtest and does not generate an official E1R result.")
    md.append("")
    md.append("## Formal Rule")
    md.append("")
    md.append("Official E1R 5Y backtest must be a **single-account continuous stateful backtest**:")
    md.append("")
    md.append("- one continuous account")
    md.append("- continuous cash")
    md.append("- continuous positions")
    md.append("- daily mark-to-market")
    md.append("- daily regime switch")
    md.append("- global live account holdings <= 3")
    md.append("- no stitched return curves")
    md.append("- no invalid artifacts as source")
    md.append("")
    md.append("## Contract")
    md.append("")
    md.append("```json")
    md.append(json.dumps(CONTRACT, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Validations")
    md.append("")
    md.append("```json")
    md.append(json.dumps(validations, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Backtest Engine Requirements")
    md.append("")
    md.append("```json")
    md.append(json.dumps(backtest["requirements"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Sidecar Requirements")
    md.append("")
    md.append("```json")
    md.append(json.dumps(sidecar["requirements"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Composer Policy")
    md.append("")
    md.append("```json")
    md.append(json.dumps(composer["formal_use_policy"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Invalid Artifact Policy")
    md.append("")
    md.append("```json")
    md.append(json.dumps(invalid_artifacts["policy"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Design Decision")
    md.append("")
    md.append("```json")
    md.append(json.dumps(decision, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Next Action")
    md.append("")
    md.append(decision["recommended_next_action"])
    md.append("")

    REPORT_MD.write_text("\n".join(md))

    print("E1R_4C2C4E_A_CONTINUOUS_STATEFUL_DESIGN_AUDIT_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("backtest_engine_requirements:", json.dumps(backtest["requirements"], ensure_ascii=False))
    print("sidecar_requirements:", json.dumps(sidecar["requirements"], ensure_ascii=False))
    print("design_decision:", json.dumps(decision, ensure_ascii=False))
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
