#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

R7 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R7_MARKET_STATE_SOURCE_EQUIVALENCE_TRACE.json"
R8 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R8_MARKET_STATE_PARAMETER_AUDIT.json"
R11 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R11_MARKET_GATE_STANDALONE_SKELETON.json"
R12 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R12_MARKET_GATE_EQUIVALENCE_SMOKE.json"
R12B = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R12B_MARKET_GATE_EQUIVALENCE_GAP_RCA.json"

MARKET_GATE = ROOT / "src/e1r_engine/market_gate.py"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R12C_MARKET_GATE_GOLDEN_ROW_LOCATOR_AND_EQUIVALENCE_RETRY.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R12C_MARKET_GATE_GOLDEN_ROW_LOCATOR_AND_EQUIVALENCE_RETRY.md"
ARCH_MD = ROOT / "docs/architecture/E1R_MARKET_GATE_GOLDEN_ROW_LOCATOR_AND_EQUIVALENCE_RETRY.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_r12c_market_gate_golden_row_locator_and_equivalence_retry.json"
EVIDENCE_JSON = ROOT / "exports/e1r_engine/equivalence/e1r_k2_r12c_market_gate_golden_row_locator_and_equivalence_retry_evidence.json"

REVIEW_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_TODAY_REVIEW_AND_NEXT_STEPS.json"
REVIEW_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_TODAY_REVIEW_AND_NEXT_STEPS.md"
REVIEW_ARCH_MD = ROOT / "docs/architecture/E1R_K2_TODAY_REVIEW_AND_NEXT_STEPS.md"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
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


def compact(v: Any, max_len: int = 1800) -> Any:
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


def get_path(obj: Any, dotted: str) -> Any:
    cur = obj
    if not dotted:
        return cur
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def bool_value(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return bool(v)
    if isinstance(v, str):
        s = v.strip().lower()
        if s in {"true", "1", "yes"}:
            return True
        if s in {"false", "0", "no"}:
            return False
    raise ValueError(f"Cannot normalize bool value: {v!r}")


def normalize_gate_state(v: Any) -> str:
    s = str(v).strip().upper()
    if s not in {"ALLOW", "SHOCK", "RISK_OFF"}:
        raise ValueError(f"Invalid gate_state: {v!r}")
    return s


def normalize_market_state(v: Any) -> str:
    s = str(v).strip().upper()
    if s not in {"FULL_ON", "CAUTIOUS_ON", "CASH_MODE", "UNKNOWN"}:
        raise ValueError(f"Invalid market_state: {v!r}")
    return s


def locate_r7_golden_rows(r7: dict[str, Any]) -> dict[str, Any]:
    candidate_paths = [
        "equivalence_report.focused_rows",
        "focused_rows",
    ]

    candidates = []
    for path in candidate_paths:
        rows = get_path(r7, path)
        if isinstance(rows, list) and rows and all(isinstance(x, dict) for x in rows):
            candidates.append({
                "path": path,
                "row_count": len(rows),
                "sample": compact(rows[:3]),
                "rows": rows,
            })

    if not candidates:
        return {
            "selected_path": None,
            "row_count": 0,
            "rows": [],
            "candidates": [],
            "error": "No focused_rows found at equivalence_report.focused_rows or focused_rows.",
        }

    # Prefer equivalence_report.focused_rows because it is the explicit R7 equivalence target.
    selected = next((c for c in candidates if c["path"] == "equivalence_report.focused_rows"), candidates[0])

    return {
        "selected_path": selected["path"],
        "row_count": selected["row_count"],
        "rows": selected["rows"],
        "candidates": [
            {
                "path": c["path"],
                "row_count": c["row_count"],
                "sample": c["sample"],
            }
            for c in candidates
        ],
        "error": None,
    }


def normalize_golden_row(row: dict[str, Any], idx: int) -> dict[str, Any]:
    return {
        "idx": idx,
        "date": str(row["date"]),
        "market_state": normalize_market_state(row["market_state"]),
        "entry_capacity": int(row["entry_capacity"]),
        "spx_close": float(row["spx_close_t"]) if row.get("spx_close_t") is not None else None,
        "spx_ma50": float(row["spx_ma50_t"]) if row.get("spx_ma50_t") is not None else None,
        "spx_day_return": float(row["spx_day_return"]) if row.get("spx_day_return") is not None else None,
        "expected": {
            "gate_state": normalize_gate_state(
                row.get("captured__gate_state")
                or row.get("expected_market_gate_state")
                or row.get("computed_gate_state_from_captured_inputs")
            ),
            "market_entry_allowed": bool_value(row["market_entry_allowed"]),
            "market_shock": bool_value(row["market_shock"]),
            "market_risk_off": bool_value(row["market_risk_off"]),
        },
        "source_quality": row.get("source_quality"),
        "raw": compact(row),
    }


def run_equivalence(normalized_rows: list[dict[str, Any]]) -> dict[str, Any]:
    import sys

    src = str(ROOT / "src")
    if src not in sys.path:
        sys.path.insert(0, src)

    from e1r_engine.market_gate import (
        MarketGateConfig,
        MarketGateEvaluator,
        MarketGateInputs,
    )

    cfg = MarketGateConfig()

    comparisons = []
    mismatches = []

    for row in normalized_rows:
        inputs = MarketGateInputs(
            date=row["date"],
            spx_close=row["spx_close"],
            spx_ma50=row["spx_ma50"],
            spx_day_return=row["spx_day_return"],
            market_state=row["market_state"],
            entry_capacity=row["entry_capacity"],
        )

        decision = MarketGateEvaluator.evaluate(cfg, inputs)

        actual = {
            "gate_state": decision.gate_state,
            "market_entry_allowed": decision.market_entry_allowed,
            "market_shock": decision.market_shock,
            "market_risk_off": decision.market_risk_off,
        }

        expected = row["expected"]
        checks = {
            k: actual[k] == expected[k]
            for k in expected.keys()
        }
        ok = all(checks.values())

        item = {
            "idx": row["idx"],
            "date": row["date"],
            "source_quality": row.get("source_quality"),
            "inputs": asdict(inputs),
            "expected": expected,
            "actual": actual,
            "checks": checks,
            "ok": ok,
        }

        comparisons.append(item)
        if not ok:
            mismatch = dict(item)
            mismatch["raw"] = row["raw"]
            mismatches.append(mismatch)

    distribution = {
        "expected_gate_state": {},
        "actual_gate_state": {},
        "market_state": {},
        "source_quality": {},
    }

    for item in comparisons:
        eg = item["expected"]["gate_state"]
        ag = item["actual"]["gate_state"]
        ms = item["inputs"]["market_state"]
        sq = item.get("source_quality") or "UNKNOWN"

        distribution["expected_gate_state"][eg] = distribution["expected_gate_state"].get(eg, 0) + 1
        distribution["actual_gate_state"][ag] = distribution["actual_gate_state"].get(ag, 0) + 1
        distribution["market_state"][ms] = distribution["market_state"].get(ms, 0) + 1
        distribution["source_quality"][sq] = distribution["source_quality"].get(sq, 0) + 1

    return {
        "row_count": len(comparisons),
        "mismatch_count": len(mismatches),
        "ok": len(comparisons) > 0 and len(mismatches) == 0,
        "distribution": distribution,
        "sample_comparisons": comparisons[:25],
        "mismatches": mismatches[:50],
    }


def pure_python_regression_smoke() -> dict[str, Any]:
    import sys

    src = str(ROOT / "src")
    if src not in sys.path:
        sys.path.insert(0, src)

    from e1r_engine.market_gate import (
        MarketGateConfig,
        MarketGateEvaluator,
        MarketGateInputs,
    )

    cfg = MarketGateConfig()

    cases = [
        {
            "name": "invalid_direct_formula_guard_2021_06_18",
            "inputs": MarketGateInputs(
                date="2021-06-18",
                spx_close=4166.450195,
                spx_ma50=4181.589023459999,
                spx_day_return=-0.01312446878817667,
                market_state="CAUTIOUS_ON",
                entry_capacity=2,
            ),
            "expected_gate_state": "ALLOW",
        },
        {
            "name": "shock_precedence_2021_05_12",
            "inputs": MarketGateInputs(
                date="2021-05-12",
                spx_close=4063.040039,
                spx_ma50=4049.93962408,
                spx_day_return=-0.02144940076056902,
                market_state="CASH_MODE",
                entry_capacity=0,
            ),
            "expected_gate_state": "SHOCK",
        },
    ]

    results = []
    for case in cases:
        decision = MarketGateEvaluator.evaluate(cfg, case["inputs"])
        ok = decision.gate_state == case["expected_gate_state"]
        results.append({
            "name": case["name"],
            "inputs": asdict(case["inputs"]),
            "expected_gate_state": case["expected_gate_state"],
            "actual_gate_state": decision.gate_state,
            "ok": ok,
        })

    return {
        "case_count": len(results),
        "ok": all(r["ok"] for r in results),
        "results": results,
    }


def build_final_review(equivalence: dict[str, Any], locator: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_at": now(),
        "title": "E1R K2 Review After R12C",
        "today_or_current_session_steps": [
            {
                "stage": "K2-R9D",
                "result": "PASS",
                "summary": "Clean source-line evidence established for market gate parameters and E1R v0.2 call chain.",
            },
            {
                "stage": "K2-R10",
                "result": "PASS",
                "summary": "Standalone replication proposal accepted as design-only.",
            },
            {
                "stage": "K2-R11",
                "result": "PASS",
                "summary": "Standalone MarketGateEvaluator skeleton created without strategy integration.",
            },
            {
                "stage": "K2-R12",
                "result": "FAIL",
                "summary": "Initial equivalence smoke failed because golden rows were not found and pytest was unavailable.",
            },
            {
                "stage": "K2-R12B",
                "result": "PASS",
                "summary": "RCA located real R7 golden rows and corrected next-step policy.",
            },
            {
                "stage": "K2-R12C",
                "result": "PASS" if equivalence.get("ok") else "FAIL",
                "summary": (
                    f"Pure-Python equivalence used {locator.get('selected_path')} with "
                    f"{equivalence.get('row_count')} rows and {equivalence.get('mismatch_count')} mismatches."
                ),
            },
        ],
        "current_truth": {
            "market_gate_skeleton_ready": True,
            "market_gate_equivalence_ready": equivalence.get("ok"),
            "row_count": equivalence.get("row_count"),
            "mismatch_count": equivalence.get("mismatch_count"),
            "selected_golden_path": locator.get("selected_path"),
            "market_gate_strategy_integration_allowed_now": False,
            "implementation_may_resume": False,
        },
        "lessons": [
            "R12C proves the correct simplified workflow: locate explicit golden rows first, then compare.",
            "No pytest dependency should be required for this project’s smoke validation path.",
            "Do not proceed from zero-row equivalence; row_count must be positive.",
            "The invalid direct formula close < MA50 => RISK_OFF remains blocked by the 2021-06-18 guard row.",
        ],
        "recommended_next_step": {
            "stage": decision.get("next_stage_after_user_approval"),
            "type": "proposal only",
            "purpose": "Design how standalone UptrendCore should consume MarketGateDecision without changing entry/exit/sizing logic.",
            "allowed": [
                "Read market_gate.py and R12C report.",
                "Define wiring boundary.",
                "Define future implementation test gates.",
            ],
            "not_allowed": [
                "No direct strategy patch yet.",
                "No full 5Y run yet.",
                "No candidate extraction yet.",
                "No live-holding behavior changes.",
            ],
        },
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    required = [R7, R8, R11, R12B, MARKET_GATE]
    missing = [rel(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError(f"Missing prerequisites: {missing}")

    r7 = read_json(R7)
    r11 = read_json(R11)
    r12b = read_json(R12B)

    if r11.get("decision", {}).get("next_stage_after_user_approval") != "4C-2C-4E-ENGINE-K2-R12-MARKET_GATE_EQUIVALENCE_SMOKE":
        raise RuntimeError("R11 state unexpected.")
    if r12b.get("decision", {}).get("next_stage_after_user_approval") != "4C-2C-4E-ENGINE-K2-R12C-MARKET_GATE_GOLDEN_ROW_LOCATOR_AND_EQUIVALENCE_RETRY":
        raise RuntimeError("R12B did not authorize R12C.")

    locator = locate_r7_golden_rows(r7)
    if locator["row_count"] <= 0:
        raise RuntimeError("R12C stopped: R7 focused_rows still not found. Do manual inspection before adding complexity.")

    normalized_rows = [
        normalize_golden_row(row, idx)
        for idx, row in enumerate(locator["rows"])
    ]

    equivalence = run_equivalence(normalized_rows)
    regression_smoke = pure_python_regression_smoke()

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "r12c_equivalence_retry_complete": True,
        "r7_loaded": R7.exists(),
        "r8_loaded": R8.exists(),
        "r11_loaded": R11.exists(),
        "r12b_loaded": R12B.exists(),
        "r12b_authorized_r12c": True,
        "golden_rows_found": locator["row_count"] > 0,
        "golden_rows_count": locator["row_count"],
        "selected_golden_path": locator["selected_path"],
        "equivalence_run": True,
        "equivalence_passed": equivalence["ok"],
        "mismatch_count_zero": equivalence["mismatch_count"] == 0,
        "pure_python_regression_smoke_run": True,
        "pure_python_regression_smoke_passed": regression_smoke["ok"],
        "pytest_required": False,
        "strategy_logic_changed": False,
        "standalone_module_only": True,
        "strategy_integration_changed": False,
        "legacy_backtest_called": False,
        "backtest_engine_run": False,
        "short_window_existing_engine_run": False,
        "full_5y_backtest_run": False,
        "forward_runner_run": False,
        "candidate_generation_extracted": False,
        "buy_add_reduce_exit_extracted": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "formula_not_patched_in_legacy": True,
        "strategy_files_unchanged": before_hashes == after_hashes,
    }

    passed = all([
        validations["r12c_equivalence_retry_complete"],
        validations["golden_rows_found"],
        validations["equivalence_passed"],
        validations["mismatch_count_zero"],
        validations["pure_python_regression_smoke_passed"],
        validations["strategy_files_unchanged"],
    ])

    decision = {
        "k2_r12c_market_gate_equivalence_retry_passed": passed,
        "market_gate_equivalence_ready": passed,
        "market_gate_strategy_integration_allowed_now": False,
        "formula_patch_allowed_now": False,
        "candidate_extraction_allowed_now": False,
        "implementation_may_resume": False,
        "requires_user_approval_before_next_stage": True,
        "next_stage_after_user_approval": (
            "4C-2C-4E-ENGINE-K2-R13-UPTREND_CORE_GATE_WIRING_PROPOSAL"
            if passed
            else "4C-2C-4E-ENGINE-K2-R12D-MARKET_GATE_EQUIVALENCE_MANUAL_INSPECTION"
        ),
        "conclusion": (
            "K2_R12C_PASS_MARKET_GATE_EQUIVALENCE_READY_FOR_R13_WIRING_PROPOSAL"
            if passed
            else "K2_R12C_EQUIVALENCE_RETRY_FAILED_DO_NOT_INTEGRATE"
        ),
        "recommended_next_action": (
            "Review R12C and final session review. If accepted, proceed to R13 proposal only."
            if passed
            else "Stop and inspect equivalence mismatches manually before continuing."
        ),
    }

    final_review = build_final_review(equivalence, locator, decision)

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R12C-MARKET_GATE_GOLDEN_ROW_LOCATOR_AND_EQUIVALENCE_RETRY",
        "status": "MARKET_GATE_GOLDEN_ROW_LOCATOR_AND_EQUIVALENCE_RETRY_COMPLETE",
        "purpose": "Use the explicitly located R7 focused_rows golden data and pure Python assertions to retry standalone MarketGateEvaluator equivalence.",
        "source_reports": {
            "r7": {"path": rel(R7), "sha256": sha256(R7)},
            "r8": {"path": rel(R8), "sha256": sha256(R8)},
            "r11": {"path": rel(R11), "sha256": sha256(R11)},
            "r12": {"path": rel(R12), "exists": R12.exists(), "sha256": sha256(R12)},
            "r12b": {"path": rel(R12B), "sha256": sha256(R12B)},
            "market_gate": {"path": rel(MARKET_GATE), "sha256": sha256(MARKET_GATE)},
        },
        "golden_row_locator": {
            "selected_path": locator["selected_path"],
            "row_count": locator["row_count"],
            "candidates": locator["candidates"],
            "error": locator["error"],
            "sample_normalized_rows": normalized_rows[:10],
        },
        "equivalence": equivalence,
        "pure_python_regression_smoke": regression_smoke,
        "policy": {
            "strategy_logic_changed": False,
            "standalone_module_only": True,
            "strategy_integration_changed": False,
            "legacy_backtest_called": False,
            "backtest_engine_run": False,
            "short_window_existing_engine_run": False,
            "full_5y_backtest_run": False,
            "forward_runner_run": False,
            "candidate_generation_extracted": False,
            "buy_add_reduce_exit_extracted": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "formula_not_patched_in_legacy": True,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
        },
        "validations": validations,
        "decision": decision,
        "final_review": final_review,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)
    write_json(EVIDENCE_JSON, report)
    write_json(REVIEW_JSON, final_review)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R12C — Golden Row Locator And Equivalence Retry")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Golden Row Locator")
    md.append("```json")
    md.append(json.dumps(report["golden_row_locator"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Equivalence")
    md.append("```json")
    md.append(json.dumps(equivalence, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Pure Python Regression Smoke")
    md.append("```json")
    md.append(json.dumps(regression_smoke, indent=2, ensure_ascii=False))
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

    review_md = []
    review_md.append("# E1R K2 — Review After R12C")
    review_md.append("")
    review_md.append(f"Generated At: `{final_review['generated_at']}`")
    review_md.append("")
    review_md.append("## Steps")
    review_md.append("```json")
    review_md.append(json.dumps(final_review["today_or_current_session_steps"], indent=2, ensure_ascii=False))
    review_md.append("```")
    review_md.append("")
    review_md.append("## Current Truth")
    review_md.append("```json")
    review_md.append(json.dumps(final_review["current_truth"], indent=2, ensure_ascii=False))
    review_md.append("```")
    review_md.append("")
    review_md.append("## Lessons")
    review_md.append("```json")
    review_md.append(json.dumps(final_review["lessons"], indent=2, ensure_ascii=False))
    review_md.append("```")
    review_md.append("")
    review_md.append("## Recommended Next Step")
    review_md.append("```json")
    review_md.append(json.dumps(final_review["recommended_next_step"], indent=2, ensure_ascii=False))
    review_md.append("```")
    review_md.append("")
    REVIEW_MD.write_text("\n".join(review_md))
    REVIEW_ARCH_MD.write_text("\n".join(review_md))

    print("E1R_4C2C4E_ENGINE_K2_R12C_MARKET_GATE_GOLDEN_ROW_LOCATOR_AND_EQUIVALENCE_RETRY_COMPLETE")
    print("status:", report["status"])
    print("golden_row_locator:", json.dumps(report["golden_row_locator"], ensure_ascii=False))
    print("equivalence:", json.dumps(equivalence, ensure_ascii=False))
    print("pure_python_regression_smoke:", json.dumps(regression_smoke, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("final_review:", json.dumps(final_review, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(AUDIT_JSON))
    print("wrote:", rel(EVIDENCE_JSON))
    print("wrote:", rel(REVIEW_JSON))
    print("wrote:", rel(REVIEW_MD))
    print("wrote:", rel(REVIEW_ARCH_MD))


if __name__ == "__main__":
    main()
