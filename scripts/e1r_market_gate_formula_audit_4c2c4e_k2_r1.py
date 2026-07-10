#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
import re
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

BACKTEST = ROOT / "src/engine/backtest.py"
GOLDEN_MASTER = ROOT / "exports/e1r_engine/golden_master/e1r_engine_g_short_window_golden_master.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R1_MARKET_GATE_FORMULA_AUDIT.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R1_MARKET_GATE_FORMULA_AUDIT.md"
ARCH_MD = ROOT / "docs/architecture/E1R_MARKET_GATE_FORMULA_AUDIT.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_engine_k2_r1_market_gate_formula_audit.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
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


def line_context(lines: list[str], line_no: int, radius: int = 6) -> dict[str, Any]:
    start = max(1, line_no - radius)
    end = min(len(lines), line_no + radius)
    return {
        "start": start,
        "end": end,
        "rows": [
            {
                "line": i,
                "text": lines[i - 1].rstrip(),
            }
            for i in range(start, end + 1)
        ],
    }


def scan_source_contexts(source: str) -> dict[str, Any]:
    lines = source.splitlines()

    groups = {
        "market_gate_state": ["market_gate_state"],
        "gate_state": ["gate_state"],
        "risk_off": ["risk_off", "RiskOff"],
        "shock": ["shock", "Shock"],
        "spx_ma50": ["spx_ma50", "MA50", "ma50"],
        "market_entry_gate": ["market_entry_gate"],
        "D3_RISK_OFF_PLUS_SHOCK_GATE": ["D3_RISK_OFF_PLUS_SHOCK_GATE"],
        "gate_allowed": ["gate_allowed", "allow_buy", "can_buy"],
    }

    out = {}

    for group, patterns in groups.items():
        hits = []
        for i, line in enumerate(lines, start=1):
            if any(p in line for p in patterns):
                hits.append({
                    "line": i,
                    "text": line.rstrip(),
                    "context": line_context(lines, i, radius=5),
                })
        out[group] = {
            "patterns": patterns,
            "hit_count": len(hits),
            "hits": hits[:30],
        }

    return out


def to_float(x: Any) -> float | None:
    try:
        if x is None:
            return None
        return float(x)
    except Exception:
        return None


def eval_formula_candidates(rows: list[dict[str, Any]]) -> dict[str, Any]:
    expected = [
        {
            "date": r.get("date"),
            "state": r.get("market_gate_state"),
            "spx_close": to_float(r.get("spx_close")),
            "spx_ma50": to_float(r.get("spx_ma50")),
            "spx_day_return_pct": to_float(r.get("spx_day_return_pct")),
        }
        for r in rows
    ]

    def state_basic(r: dict[str, Any]) -> str:
        day = r["spx_day_return_pct"]
        close = r["spx_close"]
        ma50 = r["spx_ma50"]
        if day is not None and day <= -2.0:
            return "SHOCK"
        if close is not None and ma50 is not None and close < ma50:
            return "RISK_OFF"
        return "ALLOW"

    def state_close_lt_ma50_or_day_neg1(r: dict[str, Any]) -> str:
        day = r["spx_day_return_pct"]
        close = r["spx_close"]
        ma50 = r["spx_ma50"]
        if day is not None and day <= -2.0:
            return "SHOCK"
        if close is not None and ma50 is not None and close < ma50:
            return "RISK_OFF"
        if day is not None and day <= -1.0:
            return "RISK_OFF"
        return "ALLOW"

    def state_close_lt_ma50_or_day_neg05(r: dict[str, Any]) -> str:
        day = r["spx_day_return_pct"]
        close = r["spx_close"]
        ma50 = r["spx_ma50"]
        if day is not None and day <= -2.0:
            return "SHOCK"
        if close is not None and ma50 is not None and close < ma50:
            return "RISK_OFF"
        if day is not None and day <= -0.5:
            return "RISK_OFF"
        return "ALLOW"

    formulas = {
        "basic_spx_close_lt_ma50_shock_lte_neg2": state_basic,
        "close_lt_ma50_or_day_lte_neg1": state_close_lt_ma50_or_day_neg1,
        "close_lt_ma50_or_day_lte_neg05": state_close_lt_ma50_or_day_neg05,
    }

    results = {}

    for name, fn in formulas.items():
        mismatches = []
        distribution = {}
        for r in expected:
            actual = fn(r)
            distribution[actual] = distribution.get(actual, 0) + 1
            if actual != r["state"]:
                mismatches.append({
                    "date": r["date"],
                    "expected": r["state"],
                    "actual": actual,
                    "spx_close": r["spx_close"],
                    "spx_ma50": r["spx_ma50"],
                    "spx_day_return_pct": r["spx_day_return_pct"],
                })
        results[name] = {
            "ok": len(mismatches) == 0,
            "mismatch_count": len(mismatches),
            "distribution": distribution,
            "mismatches": mismatches,
        }

    # Try shifted variants to detect whether legacy gate is recorded with t-1 / t+1 alignment.
    basic_states = [state_basic(r) for r in expected]
    expected_states = [r["state"] for r in expected]
    dates = [r["date"] for r in expected]

    for shift in [-2, -1, 1, 2]:
        mismatches = []
        for i, expected_state in enumerate(expected_states):
            j = i + shift
            actual_state = basic_states[j] if 0 <= j < len(basic_states) else None
            if actual_state != expected_state:
                mismatches.append({
                    "date": dates[i],
                    "expected": expected_state,
                    "actual_shifted_basic": actual_state,
                    "shift": shift,
                })
        results[f"basic_formula_shift_{shift}"] = {
            "ok": len(mismatches) == 0,
            "mismatch_count": len(mismatches),
            "mismatches": mismatches[:20],
        }

    return results


def summarize_expected(rows: list[dict[str, Any]]) -> dict[str, Any]:
    dist = {}
    examples = {}
    for r in rows:
        state = r.get("market_gate_state")
        dist[state] = dist.get(state, 0) + 1
        examples.setdefault(state, [])
        if len(examples[state]) < 10:
            examples[state].append({
                "date": r.get("date"),
                "spx_close": r.get("spx_close"),
                "spx_ma50": r.get("spx_ma50"),
                "spx_day_return_pct": r.get("spx_day_return_pct"),
                "market_gate_state": state,
            })

    return {
        "distribution": dist,
        "examples": examples,
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    if not BACKTEST.exists():
        raise FileNotFoundError(BACKTEST)
    if not GOLDEN_MASTER.exists():
        raise FileNotFoundError(GOLDEN_MASTER)

    source = BACKTEST.read_text()
    source_contexts = scan_source_contexts(source)

    gm = read_json(GOLDEN_MASTER)
    daily_rows = gm.get("raw_result", {}).get("daily_equity_records", [])

    if not isinstance(daily_rows, list) or not daily_rows:
        raise RuntimeError("golden master daily_equity_records missing")

    expected_summary = summarize_expected(daily_rows)
    formula_candidate_results = eval_formula_candidates(daily_rows)

    exact_formula_candidates = [
        name
        for name, result in formula_candidate_results.items()
        if result["ok"]
    ]

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "formula_audit_complete": True,
        "strategy_logic_changed": False,
        "audit_only": True,
        "backtest_engine_run": False,
        "full_5y_backtest_run": False,
        "forward_runner_run": False,
        "provider_extraction_run": False,
        "candidate_generation_extracted": False,
        "buy_add_reduce_exit_extracted": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "golden_master_loaded": True,
        "daily_equity_records_loaded": len(daily_rows) > 0,
        "source_contexts_scanned": True,
        "formula_candidates_evaluated": True,
        "basic_formula_known_failed": formula_candidate_results["basic_spx_close_lt_ma50_shock_lte_neg2"]["ok"] is False,
    }

    decision = {
        "market_gate_formula_audit_passed": all([
            validations["strategy_files_unchanged"],
            validations["golden_master_loaded"],
            validations["source_contexts_scanned"],
            validations["formula_candidates_evaluated"],
        ]),
        "exact_formula_candidates": exact_formula_candidates,
        "basic_formula_mismatch_count": formula_candidate_results["basic_spx_close_lt_ma50_shock_lte_neg2"]["mismatch_count"],
        "requires_source_formula_patch": len(exact_formula_candidates) == 0,
        "recommended_next_stage": "4C-2C-4E-ENGINE-K2-R2",
        "conclusion": "MARKET_GATE_FORMULA_AUDIT_PASS_NEEDS_SOURCE_FORMULA_PATCH",
        "recommended_next_action": (
            "Inspect source_contexts for the exact legacy market gate logic, then patch K2 using the real formula. "
            "Do not proceed to candidate extraction until market_gate_state equivalence passes."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R1",
        "status": "MARKET_GATE_FORMULA_AUDIT_COMPLETE",
        "purpose": "Audit actual legacy market gate formula after K2 mismatch.",
        "policy": {
            "strategy_logic_changed": False,
            "audit_only": True,
            "backtest_engine_run": False,
            "full_5y_backtest_run": False,
            "forward_runner_run": False,
            "provider_extraction_run": False,
            "candidate_generation_extracted": False,
            "buy_add_reduce_exit_extracted": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
        },
        "expected_summary": expected_summary,
        "formula_candidate_results": formula_candidate_results,
        "source_contexts": source_contexts,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R1 — Market Gate Formula Audit")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Expected Summary")
    md.append("```json")
    md.append(json.dumps(expected_summary, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Formula Candidate Results")
    md.append("```json")
    md.append(json.dumps(formula_candidate_results, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Source Contexts")
    md.append("```json")
    md.append(json.dumps(source_contexts, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Decision")
    md.append("```json")
    md.append(json.dumps(decision, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")

    REPORT_MD.write_text("\n".join(md))
    ARCH_MD.write_text("\n".join(md))

    print("E1R_4C2C4E_ENGINE_K2_R1_MARKET_GATE_FORMULA_AUDIT_COMPLETE")
    print("status:", report["status"])
    print("expected_summary:", json.dumps(expected_summary, ensure_ascii=False))
    print("formula_candidate_results_summary:", json.dumps({
        k: {
            "ok": v["ok"],
            "mismatch_count": v["mismatch_count"],
            "distribution": v.get("distribution"),
            "first_mismatches": v.get("mismatches", [])[:5],
        }
        for k, v in formula_candidate_results.items()
    }, ensure_ascii=False))
    print("source_context_hit_counts:", json.dumps({
        k: v["hit_count"]
        for k, v in source_contexts.items()
    }, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(AUDIT_JSON))


if __name__ == "__main__":
    main()
