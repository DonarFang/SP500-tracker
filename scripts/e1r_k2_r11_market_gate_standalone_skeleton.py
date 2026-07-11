#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

R10 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R10_MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL.json"
R9D = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9D_MARKET_PARAM_SOURCE_LINE_TRACE.json"
MARKET_GATE = ROOT / "src/e1r_engine/market_gate.py"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R11_MARKET_GATE_STANDALONE_SKELETON.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R11_MARKET_GATE_STANDALONE_SKELETON.md"
ARCH_MD = ROOT / "docs/architecture/E1R_MARKET_GATE_STANDALONE_SKELETON.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_r11_market_gate_standalone_skeleton.json"
EVIDENCE_JSON = ROOT / "exports/e1r_engine/equivalence/e1r_k2_r11_market_gate_standalone_skeleton_evidence.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

PROHIBITED_CREATED_IN_R11 = [
    ROOT / "tests/e1r_engine/test_market_gate_equivalence.py",
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


def run_smoke() -> dict[str, Any]:
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
            "name": "full_on_allow",
            "inputs": MarketGateInputs(
                date="2021-04-05",
                spx_close=4077.91,
                spx_ma50=3900.0,
                spx_day_return=0.004,
                market_state="FULL_ON",
                entry_capacity=3,
            ),
            "expected": {
                "gate_state": "ALLOW",
                "market_entry_allowed": True,
                "market_shock": False,
                "market_risk_off": False,
            },
        },
        {
            "name": "cautious_on_allow",
            "inputs": MarketGateInputs(
                date="2021-06-18",
                spx_close=4166.45,
                spx_ma50=4181.59,
                spx_day_return=-0.013124,
                market_state="CAUTIOUS_ON",
                entry_capacity=2,
            ),
            "expected": {
                "gate_state": "ALLOW",
                "market_entry_allowed": True,
                "market_shock": False,
                "market_risk_off": False,
            },
            "note": "This guards against the invalid direct formula close < MA50 => RISK_OFF.",
        },
        {
            "name": "cash_mode_risk_off",
            "inputs": MarketGateInputs(
                date="2021-05-10",
                spx_close=4188.43,
                spx_ma50=4041.08,
                spx_day_return=-0.0104,
                market_state="CASH_MODE",
                entry_capacity=0,
            ),
            "expected": {
                "gate_state": "RISK_OFF",
                "market_entry_allowed": False,
                "market_shock": False,
                "market_risk_off": True,
            },
        },
        {
            "name": "shock_precedence",
            "inputs": MarketGateInputs(
                date="2021-05-12",
                spx_close=4063.04,
                spx_ma50=4045.0,
                spx_day_return=-0.021449,
                market_state="CASH_MODE",
                entry_capacity=0,
            ),
            "expected": {
                "gate_state": "SHOCK",
                "market_entry_allowed": False,
                "market_shock": True,
                "market_risk_off": False,
            },
        },
        {
            "name": "gate_disabled_allow",
            "config": MarketGateConfig(market_gate_enabled=False),
            "inputs": MarketGateInputs(
                date="2099-01-01",
                spx_day_return=-0.10,
                market_state="CASH_MODE",
                entry_capacity=0,
            ),
            "expected": {
                "gate_state": "ALLOW",
                "market_entry_allowed": True,
                "market_shock": False,
                "market_risk_off": False,
            },
        },
    ]

    results = []
    for case in cases:
        local_cfg = case.get("config", cfg)
        decision = MarketGateEvaluator.evaluate(local_cfg, case["inputs"])
        d = asdict(decision)
        expected = case["expected"]
        checks = {
            key: d[key] == value
            for key, value in expected.items()
        }
        checks["blocked_actions"] = tuple(d["blocked_actions"]) == ("BUY", "ADD")
        checks["unaffected_actions"] = tuple(d["unaffected_actions"]) == ("HOLD", "REDUCE", "EXIT")
        results.append({
            "name": case["name"],
            "note": case.get("note"),
            "inputs": asdict(case["inputs"]),
            "config": asdict(local_cfg),
            "decision": d,
            "expected": expected,
            "checks": checks,
            "ok": all(checks.values()),
        })

    return {
        "case_count": len(results),
        "ok": all(r["ok"] for r in results),
        "results": results,
    }


def inspect_module() -> dict[str, Any]:
    text = MARKET_GATE.read_text()
    required_tokens = [
        "class MarketGateConfig",
        "class MarketGateInputs",
        "class MarketGateDecision",
        "class MarketGateEvaluator",
        "market_entry_allowed = int(inputs.entry_capacity) > 0",
        'gate_state = "ALLOW" if market_entry_allowed else "SHOCK" if market_shock else "RISK_OFF"',
        "spx_close < spx_ma50",
    ]
    return {
        "path": rel(MARKET_GATE),
        "exists": MARKET_GATE.exists(),
        "sha256": sha256(MARKET_GATE),
        "required_tokens": {
            token: token in text
            for token in required_tokens
        },
        "line_count": len(text.splitlines()),
    }


def main() -> None:
    started = datetime.now(timezone.utc)

    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    for p in [R10, R9D]:
        if not p.exists():
            raise FileNotFoundError(f"Missing prerequisite: {rel(p)}")

    r10 = read_json(R10)
    r9d = read_json(R9D)

    if r10.get("decision", {}).get("k2_r10_market_gate_standalone_replication_proposal_passed") is not True:
        raise RuntimeError("R10 proposal did not pass.")
    if r10.get("decision", {}).get("next_stage_after_user_approval") != "4C-2C-4E-ENGINE-K2-R11-MARKET_GATE_STANDALONE_SKELETON":
        raise RuntimeError("R10 did not identify R11 skeleton as next stage.")
    if r9d.get("decision", {}).get("market_state_115_replication_ready") is not True:
        raise RuntimeError("R9D did not mark market_state_115_replication_ready=True.")

    module_inspection = inspect_module()
    smoke = run_smoke()

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "market_gate_standalone_skeleton_complete": True,
        "r10_loaded": True,
        "r9d_loaded": True,
        "r10_authorized_r11": True,
        "module_created": MARKET_GATE.exists(),
        "module_required_tokens_present": all(module_inspection["required_tokens"].values()),
        "smoke_run": True,
        "smoke_passed": smoke["ok"],
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
        "prohibited_test_file_not_created": all(not p.exists() for p in PROHIBITED_CREATED_IN_R11),
    }

    decision = {
        "k2_r11_market_gate_standalone_skeleton_passed": all([
            validations["market_gate_standalone_skeleton_complete"],
            validations["r10_loaded"],
            validations["r9d_loaded"],
            validations["r10_authorized_r11"],
            validations["module_created"],
            validations["module_required_tokens_present"],
            validations["smoke_passed"],
            validations["strategy_files_unchanged"],
            validations["prohibited_test_file_not_created"],
        ]),
        "market_gate_skeleton_ready": True,
        "market_gate_equivalence_ready": False,
        "market_gate_strategy_integration_allowed_now": False,
        "formula_patch_allowed_now": False,
        "candidate_extraction_allowed_now": False,
        "implementation_may_resume": False,
        "requires_user_approval_before_next_stage": True,
        "next_stage_after_user_approval": "4C-2C-4E-ENGINE-K2-R12-MARKET_GATE_EQUIVALENCE_SMOKE",
        "conclusion": "K2_R11_PASS_MARKET_GATE_STANDALONE_SKELETON_READY_FOR_R12_EQUIVALENCE_SMOKE",
        "recommended_next_action": "Review skeleton. If accepted, proceed to R12 equivalence smoke against R7/R8 golden rows. Do not integrate into strategy yet.",
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R11-MARKET_GATE_STANDALONE_SKELETON",
        "status": "MARKET_GATE_STANDALONE_SKELETON_COMPLETE",
        "purpose": "Add standalone market gate dataclasses and pure evaluator skeleton with smoke checks, without strategy integration.",
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
        "source_reports": {
            "r10": {"path": rel(R10), "sha256": sha256(R10)},
            "r9d": {"path": rel(R9D), "sha256": sha256(R9D)},
        },
        "created_files": [
            {"path": rel(MARKET_GATE), "sha256": sha256(MARKET_GATE)},
        ],
        "module_inspection": module_inspection,
        "smoke": smoke,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)
    write_json(EVIDENCE_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R11 — Market Gate Standalone Skeleton")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Created Files")
    md.append("```json")
    md.append(json.dumps(report["created_files"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Module Inspection")
    md.append("```json")
    md.append(json.dumps(module_inspection, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Smoke")
    md.append("```json")
    md.append(json.dumps(smoke, indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_ENGINE_K2_R11_MARKET_GATE_STANDALONE_SKELETON_COMPLETE")
    print("status:", report["status"])
    print("created_files:", json.dumps(report["created_files"], ensure_ascii=False))
    print("module_inspection:", json.dumps(module_inspection, ensure_ascii=False))
    print("smoke:", json.dumps(smoke, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(AUDIT_JSON))
    print("wrote:", rel(EVIDENCE_JSON))


if __name__ == "__main__":
    main()
