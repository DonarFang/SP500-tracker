#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
import importlib.util
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

R7 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R7_MARKET_STATE_SOURCE_EQUIVALENCE_TRACE.json"
R8 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R8_MARKET_STATE_PARAMETER_AUDIT.json"
R11 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R11_MARKET_GATE_STANDALONE_SKELETON.json"
R12 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R12_MARKET_GATE_EQUIVALENCE_SMOKE.json"
R12_REVIEW = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_TODAY_REVIEW_AND_NEXT_STEPS.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R12B_MARKET_GATE_EQUIVALENCE_GAP_RCA.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R12B_MARKET_GATE_EQUIVALENCE_GAP_RCA.md"
ARCH_MD = ROOT / "docs/architecture/E1R_MARKET_GATE_EQUIVALENCE_GAP_RCA.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_r12b_market_gate_equivalence_gap_rca.json"
EVIDENCE_JSON = ROOT / "exports/e1r_engine/equivalence/e1r_k2_r12b_market_gate_equivalence_gap_rca_evidence.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

MARKET_TERMS = [
    "date",
    "market_state",
    "entry_capacity",
    "gate_state",
    "_gate_state",
    "market_gate_state",
    "market_shock",
    "_shock_active",
    "shock_active",
    "market_risk_off",
    "market_entry_allowed",
    "spx_day_return",
    "_spx_day_return",
    "spx_close",
    "spx_ma50",
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


def compact(v: Any, max_len: int = 1200) -> Any:
    if isinstance(v, (str, int, float, bool)) or v is None:
        if isinstance(v, str) and len(v) > max_len:
            return v[:max_len] + "...<truncated>"
        return v
    try:
        s = json.dumps(v, ensure_ascii=False)
        if len(s) > max_len:
            return s[:max_len] + "...<truncated>"
        return json.loads(s)
    except Exception:
        s = repr(v)
        if len(s) > max_len:
            return s[:max_len] + "...<truncated>"
        return s


def flatten(obj: Any, path: str = "") -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if isinstance(obj, dict):
        out.append({
            "path": path or "$",
            "type": "dict",
            "keys": list(obj.keys())[:80],
            "value": obj,
        })
        for k, v in obj.items():
            child = f"{path}.{k}" if path else str(k)
            out.extend(flatten(v, child))
    elif isinstance(obj, list):
        out.append({
            "path": path or "$",
            "type": "list",
            "length": len(obj),
            "value": obj,
        })
        for i, v in enumerate(obj[:5000]):
            child = f"{path}[{i}]"
            out.extend(flatten(v, child))
    else:
        out.append({
            "path": path or "$",
            "type": type(obj).__name__,
            "value": obj,
        })
    return out


def inspect_json_for_market_rows(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": rel(path), "exists": False}

    obj = read_json(path)
    flat = flatten(obj)

    key_frequency: dict[str, int] = {}
    term_hits: list[dict[str, Any]] = []
    row_like_dicts: list[dict[str, Any]] = []
    list_candidates: list[dict[str, Any]] = []

    for item in flat:
        value = item.get("value")

        if isinstance(value, dict):
            keys = list(value.keys())
            for k in keys:
                key_frequency[k] = key_frequency.get(k, 0) + 1

            matched = [k for k in keys if k in MARKET_TERMS or any(term in k for term in MARKET_TERMS)]
            if matched:
                term_hits.append({
                    "path": item["path"],
                    "matched_keys": matched,
                    "key_count": len(keys),
                    "sample": compact(value),
                })
            if len(matched) >= 3:
                row_like_dicts.append({
                    "path": item["path"],
                    "matched_keys": matched,
                    "sample": compact(value),
                })

        if isinstance(value, list) and value:
            dict_items = [x for x in value if isinstance(x, dict)]
            if dict_items:
                all_keys = sorted({k for x in dict_items[:50] for k in x.keys()})
                matched = [k for k in all_keys if k in MARKET_TERMS or any(term in k for term in MARKET_TERMS)]
                if matched:
                    list_candidates.append({
                        "path": item["path"],
                        "length": len(value),
                        "dict_sample_count": len(dict_items),
                        "sample_keys": all_keys[:80],
                        "matched_keys": matched,
                        "sample_first": compact(dict_items[0]),
                    })

    top_keys = sorted(key_frequency.items(), key=lambda kv: kv[1], reverse=True)[:80]

    return {
        "path": rel(path),
        "exists": True,
        "sha256": sha256(path),
        "top_key_frequency": top_keys,
        "term_hit_count": len(term_hits),
        "term_hits_sample": term_hits[:30],
        "row_like_dict_count": len(row_like_dicts),
        "row_like_dicts_sample": row_like_dicts[:30],
        "list_candidate_count": len(list_candidates),
        "list_candidates_sample": list_candidates[:30],
    }


def build_r12_failure_summary() -> dict[str, Any]:
    if not R12.exists():
        return {
            "r12_report_exists": False,
            "summary": "R12 report not found. It likely failed before writing report.",
        }

    r = read_json(R12)
    return {
        "r12_report_exists": True,
        "status": r.get("status"),
        "golden_row_extraction": compact(r.get("golden_row_extraction")),
        "equivalence": compact(r.get("equivalence")),
        "pytest_smoke": compact(r.get("pytest_smoke")),
        "validations": compact(r.get("validations")),
        "decision": compact(r.get("decision")),
    }


def build_corrected_review(r12_failure: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_at": now(),
        "title": "E1R K2 R12B Review And Simplified Next Steps",
        "current_truth": [
            "R12 did not pass.",
            "No strategy integration is allowed.",
            "No R13 wiring proposal is allowed until R12C passes or a better golden-row source is explicitly approved.",
            "The standalone MarketGateEvaluator skeleton from R11 remains intact, but equivalence is not proven.",
        ],
        "r12_failure_causes": [
            {
                "id": "R12B_RC1_GOLDEN_ROW_EXTRACTION_FAILED",
                "evidence": "R12 golden_row_extraction selected_source=null and row_count=0.",
                "meaning": "The extractor assumed the wrong R7/R8 JSON structure.",
            },
            {
                "id": "R12B_RC2_PYTEST_DEPENDENCY_ASSUMED",
                "evidence": "R12 pytest_smoke stderr says No module named pytest.",
                "meaning": "R12 should not require pytest in this local workflow; use pure-Python smoke fallback.",
            },
            {
                "id": "R12B_RC3_REVIEW_NEXT_STEP_CONFLICT",
                "evidence": "R12 decision says R12B, while review still listed R13 as recommended.",
                "meaning": "Review generation must branch on failure and recommend R12C/RCA, not R13.",
            },
        ],
        "simplified_next_step": {
            "stage": "4C-2C-4E-ENGINE-K2-R12C-MARKET_GATE_GOLDEN_ROW_LOCATOR_AND_EQUIVALENCE_RETRY",
            "purpose": "One compact retry: locate real golden rows first, then run pure-Python equivalence only if rows are found.",
            "rules": [
                "Do not use pytest.",
                "Do not integrate strategy.",
                "Do not run full 5Y.",
                "If row_count remains 0, stop and inspect R7/R8 manually instead of adding complexity.",
            ],
        },
        "do_not_do_next": [
            "Do not proceed to R13.",
            "Do not patch market_gate.py based on zero-row equivalence.",
            "Do not install dependencies just to make R12 pass.",
            "Do not treat mismatch_count=0 as success when row_count=0.",
        ],
        "r12_failure_summary": r12_failure,
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    for p in [R7, R8, R11]:
        if not p.exists():
            raise FileNotFoundError(f"Missing prerequisite: {rel(p)}")

    r12_failure = build_r12_failure_summary()
    r7_inspection = inspect_json_for_market_rows(R7)
    r8_inspection = inspect_json_for_market_rows(R8)

    pytest_available = importlib.util.find_spec("pytest") is not None

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "r12b_gap_rca_complete": True,
        "r7_loaded": R7.exists(),
        "r8_loaded": R8.exists(),
        "r11_loaded": R11.exists(),
        "r12_failed_report_loaded": R12.exists(),
        "r7_structure_inspected": r7_inspection.get("exists") is True,
        "r8_structure_inspected": r8_inspection.get("exists") is True,
        "pytest_availability_checked": True,
        "pytest_available": pytest_available,
        "r12_failure_preserved": R12.exists(),
        "strategy_logic_changed": False,
        "strategy_integration_changed": False,
        "legacy_backtest_called": False,
        "backtest_engine_run": False,
        "full_5y_backtest_run": False,
        "candidate_generation_extracted": False,
        "buy_add_reduce_exit_extracted": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
    }

    candidate_paths_found = (
        r7_inspection.get("row_like_dict_count", 0) > 0
        or r8_inspection.get("row_like_dict_count", 0) > 0
        or r7_inspection.get("list_candidate_count", 0) > 0
        or r8_inspection.get("list_candidate_count", 0) > 0
    )

    decision = {
        "k2_r12b_market_gate_equivalence_gap_rca_passed": all([
            validations["r12b_gap_rca_complete"],
            validations["r7_structure_inspected"],
            validations["r8_structure_inspected"],
            validations["strategy_files_unchanged"],
        ]),
        "r12_failure_confirmed": True,
        "market_gate_equivalence_ready": False,
        "market_gate_strategy_integration_allowed_now": False,
        "formula_patch_allowed_now": False,
        "candidate_extraction_allowed_now": False,
        "implementation_may_resume": False,
        "candidate_golden_paths_found_for_next_retry": candidate_paths_found,
        "next_stage_after_user_approval": "4C-2C-4E-ENGINE-K2-R12C-MARKET_GATE_GOLDEN_ROW_LOCATOR_AND_EQUIVALENCE_RETRY",
        "conclusion": "K2_R12B_PASS_GAP_RCA_DONE_DO_NOT_INTEGRATE_READY_FOR_R12C_MINIMAL_RETRY",
        "recommended_next_action": "Run one minimal R12C retry that first locates golden rows and uses pure-Python assertions. Do not proceed to R13.",
    }

    corrected_review = build_corrected_review(r12_failure)

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R12B-MARKET_GATE_EQUIVALENCE_GAP_RCA",
        "status": "MARKET_GATE_EQUIVALENCE_GAP_RCA_COMPLETE",
        "purpose": "Explain R12 failure, inspect R7/R8 structure, preserve failed evidence, and define a minimal retry path.",
        "r12_failure_summary": r12_failure,
        "r7_structure_inspection": r7_inspection,
        "r8_structure_inspection": r8_inspection,
        "pytest": {
            "available": pytest_available,
            "decision": "R12C must not depend on pytest; use pure Python assertions.",
        },
        "corrected_review": corrected_review,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)
    write_json(EVIDENCE_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R12B — Market Gate Equivalence Gap RCA")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## R12 Failure Summary")
    md.append("```json")
    md.append(json.dumps(r12_failure, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## R7 Structure Inspection")
    md.append("```json")
    md.append(json.dumps(r7_inspection, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## R8 Structure Inspection")
    md.append("```json")
    md.append(json.dumps(r8_inspection, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Corrected Review")
    md.append("```json")
    md.append(json.dumps(corrected_review, indent=2, ensure_ascii=False))
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

    # Also overwrite the previous today review with corrected no-R13-before-R12C review.
    write_json(R12_REVIEW, corrected_review)
    review_md = []
    review_md.append("# E1R K2 — Corrected R12 Review And Next Steps")
    review_md.append("")
    review_md.append(f"Generated At: `{corrected_review['generated_at']}`")
    review_md.append("")
    review_md.append("## Current Truth")
    review_md.append("```json")
    review_md.append(json.dumps(corrected_review["current_truth"], indent=2, ensure_ascii=False))
    review_md.append("```")
    review_md.append("")
    review_md.append("## R12 Failure Causes")
    review_md.append("```json")
    review_md.append(json.dumps(corrected_review["r12_failure_causes"], indent=2, ensure_ascii=False))
    review_md.append("```")
    review_md.append("")
    review_md.append("## Simplified Next Step")
    review_md.append("```json")
    review_md.append(json.dumps(corrected_review["simplified_next_step"], indent=2, ensure_ascii=False))
    review_md.append("```")
    review_md.append("")
    review_md.append("## Do Not Do Next")
    review_md.append("```json")
    review_md.append(json.dumps(corrected_review["do_not_do_next"], indent=2, ensure_ascii=False))
    review_md.append("```")
    review_md.append("")
    (ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_TODAY_REVIEW_AND_NEXT_STEPS.md").write_text("\n".join(review_md))
    (ROOT / "docs/architecture/E1R_K2_TODAY_REVIEW_AND_NEXT_STEPS.md").write_text("\n".join(review_md))

    print("E1R_4C2C4E_ENGINE_K2_R12B_MARKET_GATE_EQUIVALENCE_GAP_RCA_COMPLETE")
    print("status:", report["status"])
    print("r12_failure_summary:", json.dumps(r12_failure, ensure_ascii=False))
    print("r7_structure_inspection:", json.dumps(r7_inspection, ensure_ascii=False))
    print("r8_structure_inspection:", json.dumps(r8_inspection, ensure_ascii=False))
    print("pytest:", json.dumps(report["pytest"], ensure_ascii=False))
    print("corrected_review:", json.dumps(corrected_review, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(AUDIT_JSON))
    print("wrote:", rel(EVIDENCE_JSON))
    print("wrote:", rel(R12_REVIEW))


if __name__ == "__main__":
    main()
