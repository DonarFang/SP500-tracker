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

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_J_UPTREND_EXTRACTION_SKELETON.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_J_UPTREND_EXTRACTION_SKELETON.md"
ARCH_MD = ROOT / "docs/architecture/E1R_UPTREND_EXTRACTION_SKELETON_CONTRACT.md"
EQUIV_JSON = ROOT / "exports/e1r_engine/equivalence/e1r_engine_j_uptrend_equivalence_report.json"
PROJECTION_JSON = ROOT / "exports/e1r_engine/audit/e1r_engine_j_uptrend_core_projection.json"

ENGINE_G_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_G_GOLDEN_MASTER_HARNESS.json"
ENGINE_H_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_H_GOLDEN_MASTER_TRACE_SHAPE_AUDIT.json"
ENGINE_I_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_I_UPTREND_EXTRACTION_PLAN.json"
ASSERTIONS_JSON = ROOT / "exports/e1r_engine/audit/e1r_engine_h_equivalence_assertions.json"
GOLDEN_MASTER_JSON = ROOT / "exports/e1r_engine/golden_master/e1r_engine_g_short_window_golden_master.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
]

NEW_ENGINE_FILES = [
    ROOT / "src/e1r_engine/uptrend_core.py",
    ROOT / "src/e1r_engine/equivalence.py",
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


def extract_expected_from_golden_master(golden_master: dict[str, Any]) -> dict[str, Any]:
    raw = golden_master.get("raw_result", {})
    daily = raw.get("daily_equity_records", [])
    trades = raw.get("trades", [])

    comparable_daily = []
    for row in daily:
        comparable_daily.append({
            "date": row.get("date"),
            "cash": row.get("cash"),
            "positions_value": row.get("positions_value", row.get("position_value")),
            "total_equity": row.get("total_equity"),
            "open_positions_count": row.get("open_positions_count", row.get("n_holdings")),
            "market_gate_state": row.get("market_gate_state"),
            "spx_regime": row.get("spx_regime"),
        })

    comparable_trades = []
    for row in trades:
        comparable_trades.append({
            "symbol": row.get("symbol"),
            "entry_date": row.get("entry_date"),
            "entry_price": row.get("entry_price"),
            "exit_date": row.get("exit_date"),
            "exit_price": row.get("exit_price"),
            "entry_signal": row.get("entry_signal"),
            "exit_signal": row.get("exit_signal"),
            "entry_regime": row.get("entry_regime"),
            "exit_regime": row.get("exit_regime"),
            "return_pct": row.get("return_pct"),
            "holding_days": row.get("holding_days"),
        })

    return {
        "source": "ENGINE_G_GOLDEN_MASTER_EXPECTED",
        "window": golden_master.get("window", {}),
        "daily_account": comparable_daily,
        "trades": comparable_trades,
        "metadata": {
            "from": "exports/e1r_engine/golden_master/e1r_engine_g_short_window_golden_master.json",
        },
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    for p in [
        ENGINE_G_REPORT,
        ENGINE_H_REPORT,
        ENGINE_I_REPORT,
        ASSERTIONS_JSON,
        GOLDEN_MASTER_JSON,
    ]:
        if not p.exists():
            raise FileNotFoundError(f"Missing prerequisite file: {rel(p)}")

    engine_g = read_json(ENGINE_G_REPORT)
    engine_h = read_json(ENGINE_H_REPORT)
    engine_i = read_json(ENGINE_I_REPORT)

    if engine_g.get("decision", {}).get("golden_master_harness_passed") is not True:
        raise RuntimeError("ENGINE-G did not pass.")
    if engine_h.get("decision", {}).get("trace_shape_audit_passed") is not True:
        raise RuntimeError("ENGINE-H did not pass.")
    if engine_i.get("decision", {}).get("uptrend_extraction_plan_passed") is not True:
        raise RuntimeError("ENGINE-I did not pass.")

    from e1r_engine.uptrend_core import UptrendCore
    from e1r_engine.equivalence import UptrendEquivalenceChecker

    golden_master = read_json(GOLDEN_MASTER_JSON)

    expected = extract_expected_from_golden_master(golden_master)
    actual_result = UptrendCore().from_golden_master(golden_master)
    actual = actual_result.to_comparable_dict()

    checker = UptrendEquivalenceChecker(money_abs_tol=0.01, pct_abs_tol=0.01)
    equivalence_report = checker.compare(expected=expected, actual=actual).to_dict()

    write_json(PROJECTION_JSON, actual)
    write_json(EQUIV_JSON, equivalence_report)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "uptrend_core_skeleton_defined": True,
        "equivalence_checker_defined": True,
        "golden_master_replay_skeleton_only": True,
        "actual_strategy_logic_extracted": False,
        "strategy_decisions_generated": False,
        "strategy_logic_changed": False,
        "backtest_engine_run": False,
        "full_5y_backtest_run": False,
        "forward_runner_run": False,
        "provider_extraction_run": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "invalid_artifacts_not_used_as_source": True,
        "composer_not_used": True,
        "return_curve_stitching_used": False,
        "engine_g_loaded": True,
        "engine_h_loaded": True,
        "engine_i_loaded": True,
        "new_engine_files_exist": all(p.exists() for p in NEW_ENGINE_FILES),
        "projection_written": PROJECTION_JSON.exists(),
        "equivalence_report_written": EQUIV_JSON.exists(),
        "equivalence_checker_passed_against_replay_projection": equivalence_report["ok"] is True,
        "checked_assertion_count": len(equivalence_report["checked_assertions"]),
        "mismatch_count": equivalence_report["mismatch_count"],
        "daily_rows_compared": equivalence_report["summary"]["expected_daily_rows"],
        "trades_compared": equivalence_report["summary"]["expected_trades"],
        "max_positions_contract_observed": all(
            int(r.get("open_positions_count", 0)) <= 3
            for r in actual.get("daily_account", [])
        ),
    }

    decision = {
        "uptrend_extraction_skeleton_passed": all([
            validations["uptrend_core_skeleton_defined"],
            validations["equivalence_checker_defined"],
            validations["new_engine_files_exist"],
            validations["projection_written"],
            validations["equivalence_report_written"],
            validations["equivalence_checker_passed_against_replay_projection"],
            validations["strategy_files_unchanged"],
            validations["max_positions_contract_observed"],
        ]),
        "actual_strategy_logic_extracted": False,
        "equivalence_checker_ready": equivalence_report["ok"] is True,
        "checked_assertions": equivalence_report["checked_assertions"],
        "strategy_core_extraction_allowed_now": False,
        "uptrend_real_extraction_allowed_after_user_approval": True,
        "sideways_branch_implementation_allowed_now": False,
        "full_5y_backtest_allowed_now": False,
        "forward_runner_allowed_now": False,
        "recommended_next_stage": "4C-2C-4E-ENGINE-K",
        "conclusion": (
            "UPTREND_EXTRACTION_SKELETON_PASS_READY_FOR_REAL_EXTRACTION_STEP"
            if equivalence_report["ok"] is True and before_hashes == after_hashes
            else "UPTREND_EXTRACTION_SKELETON_NEEDS_REVIEW"
        ),
        "recommended_next_action": (
            "Proceed to 4C-2C-4E-ENGINE-K: replace replay skeleton with first real extracted UPTREND implementation, "
            "then compare against ENGINE-G/H assertions. Do not tune or reinterpret trading rules."
        ),
        "engineering_rule": (
            "ENGINE-J locks the output shape and equivalence checker. It intentionally does not claim real strategy extraction yet."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-J",
        "status": "UPTREND_EXTRACTION_SKELETON_COMPLETE",
        "purpose": "Create UPTREND extraction skeleton and equivalence checker against ENGINE-G/H without modifying legacy strategy files.",
        "policy": {
            "strategy_logic_changed": False,
            "golden_master_replay_skeleton_only": True,
            "actual_strategy_logic_extracted": False,
            "backtest_engine_run": False,
            "full_5y_backtest_run": False,
            "forward_runner_run": False,
            "provider_extraction_run": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
            "invalid_artifacts_used_as_source": False,
            "composer_used": False,
            "return_curve_stitching_used": False,
        },
        "new_engine_files": [rel(p) for p in NEW_ENGINE_FILES],
        "projection_path": rel(PROJECTION_JSON),
        "projection_sha256": sha256(PROJECTION_JSON),
        "equivalence_report_path": rel(EQUIV_JSON),
        "equivalence_report_sha256": sha256(EQUIV_JSON),
        "equivalence_report": equivalence_report,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-J — UPTREND Extraction Skeleton")
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
    md.append("## Equivalence Report")
    md.append("```json")
    md.append(json.dumps(equivalence_report, indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_ENGINE_J_UPTREND_EXTRACTION_SKELETON_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("new_engine_files:", json.dumps(report["new_engine_files"], ensure_ascii=False))
    print("equivalence_report:", json.dumps(equivalence_report, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(PROJECTION_JSON))
    print("wrote:", rel(EQUIV_JSON))


if __name__ == "__main__":
    main()
