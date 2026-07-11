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
R9D = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9D_MARKET_PARAM_SOURCE_LINE_TRACE.json"
R10 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R10_MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL.json"
R11 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R11_MARKET_GATE_STANDALONE_SKELETON.json"

MARKET_GATE = ROOT / "src/e1r_engine/market_gate.py"
TEST_FILE = ROOT / "tests/e1r_engine/test_market_gate_equivalence.py"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R12_MARKET_GATE_EQUIVALENCE_SMOKE.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R12_MARKET_GATE_EQUIVALENCE_SMOKE.md"
ARCH_MD = ROOT / "docs/architecture/E1R_MARKET_GATE_EQUIVALENCE_SMOKE.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_r12_market_gate_equivalence_smoke.json"
EVIDENCE_JSON = ROOT / "exports/e1r_engine/equivalence/e1r_k2_r12_market_gate_equivalence_smoke_evidence.json"

REVIEW_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_TODAY_REVIEW_AND_NEXT_STEPS.json"
REVIEW_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_TODAY_REVIEW_AND_NEXT_STEPS.md"
REVIEW_ARCH_MD = ROOT / "docs/architecture/E1R_K2_TODAY_REVIEW_AND_NEXT_STEPS.md"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

PROHIBITED_INTEGRATION_PATHS = [
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


def compact(v: Any, max_len: int = 2000) -> Any:
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


def flatten(obj: Any, prefix: str = "") -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else str(k)
            out.append({"path": p, "key": str(k), "value": v})
            out.extend(flatten(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            p = f"{prefix}[{i}]"
            out.append({"path": p, "key": f"[{i}]", "value": v})
            out.extend(flatten(v, p))
    return out


def collect_values_by_key(obj: Any, key_names: set[str]) -> list[tuple[str, Any]]:
    hits = []
    for row in flatten(obj):
        key = row["key"]
        if key in key_names:
            hits.append((row["path"], row["value"]))
    return hits


def first_value(obj: Any, key_names: set[str], prefer_path_terms: list[str] | None = None) -> Any:
    hits = collect_values_by_key(obj, key_names)
    if not hits:
        return None

    prefer_path_terms = prefer_path_terms or []
    for path, value in hits:
        low = path.lower()
        if any(term in low for term in prefer_path_terms):
            return value

    # Avoid computed rows if a non-computed value exists.
    for path, value in hits:
        low = path.lower()
        if "computed" not in low and "standalone" not in low:
            return value

    return hits[0][1]


def to_bool(v: Any) -> bool | None:
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
    return None


def to_float(v: Any) -> float | None:
    if v is None or isinstance(v, bool):
        return None
    try:
        return float(v)
    except Exception:
        return None


def to_int(v: Any) -> int | None:
    if v is None or isinstance(v, bool):
        return None
    try:
        return int(v)
    except Exception:
        return None


def normalize_gate_state(v: Any) -> str | None:
    if v is None:
        return None
    s = str(v).strip().upper()
    if s in {"ALLOW", "SHOCK", "RISK_OFF"}:
        return s
    return None


def normalize_market_state(v: Any) -> str | None:
    if v is None:
        return None
    s = str(v).strip().upper()
    if s in {"FULL_ON", "CAUTIOUS_ON", "CASH_MODE", "UNKNOWN"}:
        return s
    return None


def normalize_row(row: dict[str, Any], source_path: str) -> dict[str, Any] | None:
    prefer = ["captured", "legacy", "locals", "trace"]

    date = first_value(row, {"date", "current_date", "trading_date"}, prefer)
    market_state = normalize_market_state(first_value(row, {"market_state"}, prefer))
    entry_capacity = to_int(first_value(row, {"entry_capacity"}, prefer))

    spx_close = to_float(first_value(row, {"spx_close", "spx_price", "_spx_close"}, prefer))
    spx_ma50 = to_float(first_value(row, {"spx_ma50", "_spx_ma50"}, prefer))
    spx_day_return = to_float(first_value(row, {"spx_day_return", "_spx_day_return", "daily_return"}, prefer))

    market_shock = to_bool(first_value(row, {"market_shock", "_shock_active", "shock_active"}, prefer))
    market_risk_off = to_bool(first_value(row, {"market_risk_off"}, prefer))
    market_entry_allowed = to_bool(first_value(row, {"market_entry_allowed"}, prefer))
    gate_state = normalize_gate_state(first_value(row, {"gate_state", "_gate_state", "market_gate_state"}, prefer))

    if date is None or market_state is None or entry_capacity is None:
        return None
    if market_shock is None or market_risk_off is None or market_entry_allowed is None or gate_state is None:
        return None
    if spx_day_return is None:
        return None

    return {
        "source_path": source_path,
        "date": str(date),
        "market_state": market_state,
        "entry_capacity": entry_capacity,
        "spx_close": spx_close,
        "spx_ma50": spx_ma50,
        "spx_day_return": spx_day_return,
        "expected": {
            "market_shock": market_shock,
            "market_risk_off": market_risk_off,
            "market_entry_allowed": market_entry_allowed,
            "gate_state": gate_state,
        },
        "raw_compact": compact(row, 1600),
    }


def find_candidate_row_lists(obj: Any, source_path: str) -> list[dict[str, Any]]:
    candidates = []

    for item in flatten(obj):
        value = item["value"]
        if isinstance(value, list) and value and all(isinstance(x, dict) for x in value):
            normalized = []
            for row in value:
                nr = normalize_row(row, source_path)
                if nr is not None:
                    normalized.append(nr)
            if normalized:
                candidates.append({
                    "json_path": item["path"],
                    "source_path": source_path,
                    "raw_count": len(value),
                    "normalized_count": len(normalized),
                    "normalized_rows": normalized,
                })

    return sorted(candidates, key=lambda x: (x["normalized_count"], x["raw_count"]), reverse=True)


def extract_golden_rows() -> dict[str, Any]:
    sources = []
    for p in [R7, R8]:
        if p.exists():
            obj = read_json(p)
            candidates = find_candidate_row_lists(obj, rel(p))
            sources.append({
                "path": rel(p),
                "exists": True,
                "sha256": sha256(p),
                "candidate_lists": [
                    {
                        "json_path": c["json_path"],
                        "raw_count": c["raw_count"],
                        "normalized_count": c["normalized_count"],
                    }
                    for c in candidates[:10]
                ],
                "best": candidates[0] if candidates else None,
            })
        else:
            sources.append({"path": rel(p), "exists": False, "candidate_lists": [], "best": None})

    usable = [s for s in sources if s.get("best")]
    if not usable:
        return {
            "sources": sources,
            "selected_source": None,
            "rows": [],
            "error": "No usable golden row list found in R7/R8.",
        }

    # Prefer R7 if it has a useful 62-row trace; otherwise choose largest normalized candidate.
    r7_source = next((s for s in usable if s["path"] == rel(R7) and s["best"]["normalized_count"] >= 10), None)
    selected = r7_source or max(usable, key=lambda s: s["best"]["normalized_count"])

    return {
        "sources": sources,
        "selected_source": {
            "path": selected["path"],
            "json_path": selected["best"]["json_path"],
            "raw_count": selected["best"]["raw_count"],
            "normalized_count": selected["best"]["normalized_count"],
        },
        "rows": selected["best"]["normalized_rows"],
        "error": None,
    }


def run_equivalence(rows: list[dict[str, Any]]) -> dict[str, Any]:
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

    for idx, row in enumerate(rows):
        inputs = MarketGateInputs(
            date=row["date"],
            spx_close=row.get("spx_close"),
            spx_ma50=row.get("spx_ma50"),
            spx_day_return=row.get("spx_day_return"),
            market_state=row["market_state"],
            entry_capacity=row["entry_capacity"],
        )
        decision = MarketGateEvaluator.evaluate(cfg, inputs)
        actual = {
            "market_shock": decision.market_shock,
            "market_risk_off": decision.market_risk_off,
            "market_entry_allowed": decision.market_entry_allowed,
            "gate_state": decision.gate_state,
        }
        expected = row["expected"]
        checks = {
            key: actual.get(key) == expected.get(key)
            for key in expected.keys()
        }
        ok = all(checks.values())

        item = {
            "idx": idx,
            "date": row["date"],
            "inputs": asdict(inputs),
            "expected": expected,
            "actual": actual,
            "checks": checks,
            "ok": ok,
        }
        comparisons.append(item)
        if not ok:
            mismatch = dict(item)
            mismatch["raw_compact"] = row.get("raw_compact")
            mismatches.append(mismatch)

    distribution = {
        "expected_gate_state": {},
        "actual_gate_state": {},
        "expected_market_state": {},
    }
    for c in comparisons:
        eg = c["expected"]["gate_state"]
        ag = c["actual"]["gate_state"]
        ms = c["inputs"]["market_state"]
        distribution["expected_gate_state"][eg] = distribution["expected_gate_state"].get(eg, 0) + 1
        distribution["actual_gate_state"][ag] = distribution["actual_gate_state"].get(ag, 0) + 1
        distribution["expected_market_state"][ms] = distribution["expected_market_state"].get(ms, 0) + 1

    return {
        "row_count": len(comparisons),
        "mismatch_count": len(mismatches),
        "ok": len(comparisons) > 0 and len(mismatches) == 0,
        "distribution": distribution,
        "sample_comparisons": comparisons[:20],
        "mismatches": mismatches[:50],
    }


def write_pytest_file() -> None:
    TEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    TEST_FILE.write_text(
'''"""Smoke tests for standalone E1R market gate evaluator.

Generated by K2-R12. This file intentionally tests only the standalone
MarketGateEvaluator contract; it does not import or execute legacy backtest code.
"""

from e1r_engine.market_gate import MarketGateConfig, MarketGateEvaluator, MarketGateInputs


def test_market_gate_invalid_direct_formula_guard() -> None:
    cfg = MarketGateConfig()
    inputs = MarketGateInputs(
        date="2021-06-18",
        spx_close=4166.45,
        spx_ma50=4181.59,
        spx_day_return=-0.013124,
        market_state="CAUTIOUS_ON",
        entry_capacity=2,
    )

    decision = MarketGateEvaluator.evaluate(cfg, inputs)

    assert decision.gate_state == "ALLOW"
    assert decision.market_entry_allowed is True
    assert decision.market_shock is False
    assert decision.market_risk_off is False


def test_market_gate_shock_precedence() -> None:
    cfg = MarketGateConfig()
    inputs = MarketGateInputs(
        date="2021-05-12",
        spx_day_return=-0.021449,
        market_state="CASH_MODE",
        entry_capacity=0,
    )

    decision = MarketGateEvaluator.evaluate(cfg, inputs)

    assert decision.gate_state == "SHOCK"
    assert decision.market_entry_allowed is False
    assert decision.market_shock is True
    assert decision.market_risk_off is False
''')
    

def run_pytest_smoke() -> dict[str, Any]:
    import subprocess
    import sys

    cmd = [sys.executable, "-m", "pytest", "-q", str(TEST_FILE)]
    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "ok": proc.returncode == 0,
    }


def build_review(r12_decision: dict[str, Any], equivalence: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_at": now(),
        "title": "E1R K2 Review And Next Steps",
        "today_or_current_session_steps": [
            {
                "stage": "K2-R9C",
                "result": "Generator trace completed, but evidence-quality issue remained.",
                "lesson": "Term counts are not source-line provenance.",
            },
            {
                "stage": "K2-RCA2",
                "result": "Three-attempt stop rule was applied.",
                "lesson": "R9/R9B/R9C were all targeting the same evidence-chain objective and had not reached final proof standard.",
            },
            {
                "stage": "K2-R9D",
                "result": "Market parameter source-line trace passed.",
                "lesson": "Clean primary-source evidence is enough to move from evidence recovery to proposal.",
            },
            {
                "stage": "K2-R10",
                "result": "Standalone replication proposal passed.",
                "lesson": "The correct contract is local-variable chain replication, not direct SPX/MA50 formula.",
            },
            {
                "stage": "K2-R11",
                "result": "Standalone market gate skeleton passed.",
                "lesson": "A standalone pure evaluator can be added safely when strategy integration is explicitly prohibited.",
            },
            {
                "stage": "K2-R12",
                "result": "Equivalence smoke completed.",
                "lesson": (
                    "Standalone evaluator is ready for next proposal stage."
                    if r12_decision.get("k2_r12_market_gate_equivalence_smoke_passed")
                    else "Equivalence gaps must be closed before any integration proposal."
                ),
            },
        ],
        "quality_controls_that_helped": [
            "No full 5Y run during evidence and skeleton phases.",
            "No patch before source-line evidence.",
            "No strategy integration before equivalence smoke.",
            "Explicit validation flags for strategy_logic_changed=false and frozen files unchanged.",
            "Three-attempt RCA rule prevented continuing with polluted evidence.",
        ],
        "current_status_after_r12": {
            "equivalence_ok": equivalence.get("ok"),
            "row_count": equivalence.get("row_count"),
            "mismatch_count": equivalence.get("mismatch_count"),
            "market_gate_strategy_integration_allowed_now": False,
            "implementation_may_resume": False,
        },
        "recommended_next_steps": [
            {
                "stage": "4C-2C-4E-ENGINE-K2-R13-UPTREND_CORE_GATE_WIRING_PROPOSAL",
                "type": "proposal only",
                "purpose": "Design how UptrendCore should consume MarketGateDecision without changing entry/exit/sizing logic.",
                "allowed": [
                    "Read standalone market_gate.py and R12 equivalence report.",
                    "Define integration boundary.",
                    "Define test plan for future wiring.",
                ],
                "not_allowed": [
                    "No strategy patch yet.",
                    "No full 5Y run.",
                    "No candidate extraction.",
                ],
            },
            {
                "stage": "Future R14/R15",
                "type": "implementation after approval",
                "purpose": "Only after R13 proposal approval: wire gate decision into standalone UptrendCore skeleton and run local equivalence tests.",
            },
        ],
        "standing_warning": "If three future attempts fail to reach the same objective, stop and perform RCA before continuing.",
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    required = [R7, R8, R9D, R10, R11, MARKET_GATE]
    missing = [rel(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError(f"Missing prerequisites: {missing}")

    r10 = read_json(R10)
    r11 = read_json(R11)
    if r10.get("decision", {}).get("next_stage_after_user_approval") != "4C-2C-4E-ENGINE-K2-R11-MARKET_GATE_STANDALONE_SKELETON":
        raise RuntimeError("R10 state unexpected.")
    if r11.get("decision", {}).get("next_stage_after_user_approval") != "4C-2C-4E-ENGINE-K2-R12-MARKET_GATE_EQUIVALENCE_SMOKE":
        raise RuntimeError("R11 did not authorize R12.")

    golden = extract_golden_rows()
    equivalence = run_equivalence(golden["rows"])

    write_pytest_file()
    pytest_smoke = run_pytest_smoke()

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "market_gate_equivalence_smoke_complete": True,
        "r7_loaded": R7.exists(),
        "r8_loaded": R8.exists(),
        "r9d_loaded": R9D.exists(),
        "r10_loaded": R10.exists(),
        "r11_loaded": R11.exists(),
        "r11_authorized_r12": True,
        "golden_rows_found": len(golden["rows"]) > 0,
        "golden_rows_count": len(golden["rows"]),
        "equivalence_run": True,
        "equivalence_passed": equivalence["ok"],
        "mismatch_count_zero": equivalence["mismatch_count"] == 0,
        "pytest_file_created": TEST_FILE.exists(),
        "pytest_smoke_run": True,
        "pytest_smoke_passed": pytest_smoke["ok"],
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

    decision = {
        "k2_r12_market_gate_equivalence_smoke_passed": all([
            validations["market_gate_equivalence_smoke_complete"],
            validations["golden_rows_found"],
            validations["equivalence_passed"],
            validations["mismatch_count_zero"],
            validations["pytest_smoke_passed"],
            validations["strategy_files_unchanged"],
        ]),
        "market_gate_equivalence_ready": bool(equivalence["ok"]),
        "market_gate_strategy_integration_allowed_now": False,
        "formula_patch_allowed_now": False,
        "candidate_extraction_allowed_now": False,
        "implementation_may_resume": False,
        "requires_user_approval_before_next_stage": True,
        "next_stage_after_user_approval": (
            "4C-2C-4E-ENGINE-K2-R13-UPTREND_CORE_GATE_WIRING_PROPOSAL"
            if equivalence["ok"]
            else "4C-2C-4E-ENGINE-K2-R12B-MARKET_GATE_EQUIVALENCE_GAP_RCA"
        ),
        "conclusion": (
            "K2_R12_PASS_MARKET_GATE_EQUIVALENCE_READY_FOR_R13_WIRING_PROPOSAL"
            if equivalence["ok"]
            else "K2_R12_EQUIVALENCE_GAPS_REMAIN_DO_NOT_INTEGRATE"
        ),
        "recommended_next_action": (
            "Review R12 and session review. If accepted, proceed to R13 wiring proposal only."
            if equivalence["ok"]
            else "Stop and perform R12B RCA/gap closure before any wiring proposal."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R12-MARKET_GATE_EQUIVALENCE_SMOKE",
        "status": "MARKET_GATE_EQUIVALENCE_SMOKE_COMPLETE",
        "purpose": "Compare standalone MarketGateEvaluator against R7/R8 golden rows without strategy integration.",
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
            "r7": {"path": rel(R7), "sha256": sha256(R7)},
            "r8": {"path": rel(R8), "sha256": sha256(R8)},
            "r9d": {"path": rel(R9D), "sha256": sha256(R9D)},
            "r10": {"path": rel(R10), "sha256": sha256(R10)},
            "r11": {"path": rel(R11), "sha256": sha256(R11)},
        },
        "golden_row_extraction": {
            "sources": golden["sources"],
            "selected_source": golden["selected_source"],
            "error": golden["error"],
            "row_count": len(golden["rows"]),
            "sample_rows": golden["rows"][:10],
        },
        "equivalence": equivalence,
        "pytest_smoke": pytest_smoke,
        "created_files": [
            {"path": rel(TEST_FILE), "sha256": sha256(TEST_FILE)},
        ],
        "validations": validations,
        "decision": decision,
    }

    review = build_review(decision, equivalence)

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)
    write_json(EVIDENCE_JSON, report)
    write_json(REVIEW_JSON, review)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R12 — Market Gate Equivalence Smoke")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Golden Row Extraction")
    md.append("```json")
    md.append(json.dumps(report["golden_row_extraction"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Equivalence")
    md.append("```json")
    md.append(json.dumps(equivalence, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Pytest Smoke")
    md.append("```json")
    md.append(json.dumps(pytest_smoke, indent=2, ensure_ascii=False))
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
    review_md.append("# E1R K2 — Today Review And Next Steps")
    review_md.append("")
    review_md.append(f"Generated At: `{review['generated_at']}`")
    review_md.append("")
    review_md.append("## Steps")
    review_md.append("```json")
    review_md.append(json.dumps(review["today_or_current_session_steps"], indent=2, ensure_ascii=False))
    review_md.append("```")
    review_md.append("")
    review_md.append("## Quality Controls")
    review_md.append("```json")
    review_md.append(json.dumps(review["quality_controls_that_helped"], indent=2, ensure_ascii=False))
    review_md.append("```")
    review_md.append("")
    review_md.append("## Current Status")
    review_md.append("```json")
    review_md.append(json.dumps(review["current_status_after_r12"], indent=2, ensure_ascii=False))
    review_md.append("```")
    review_md.append("")
    review_md.append("## Recommended Next Steps")
    review_md.append("```json")
    review_md.append(json.dumps(review["recommended_next_steps"], indent=2, ensure_ascii=False))
    review_md.append("```")
    review_md.append("")
    review_md.append(f"Standing Warning: {review['standing_warning']}")
    review_md.append("")
    REVIEW_MD.write_text("\n".join(review_md))
    REVIEW_ARCH_MD.write_text("\n".join(review_md))

    print("E1R_4C2C4E_ENGINE_K2_R12_MARKET_GATE_EQUIVALENCE_SMOKE_COMPLETE")
    print("status:", report["status"])
    print("golden_row_extraction:", json.dumps(report["golden_row_extraction"], ensure_ascii=False))
    print("equivalence:", json.dumps(equivalence, ensure_ascii=False))
    print("pytest_smoke:", json.dumps(pytest_smoke, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("today_review:", json.dumps(review, ensure_ascii=False))
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
