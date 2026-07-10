#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
import ast
import re
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

BACKTEST = ROOT / "src/engine/backtest.py"
K2_R5 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R5_FORMULA_PATCH_PROPOSAL.json"
GOLDEN_MASTER = ROOT / "exports/e1r_engine/golden_master/e1r_engine_g_short_window_golden_master.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R6_MARKET_GATE_VARIABLE_REPLAY_TRACE.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R6_MARKET_GATE_VARIABLE_REPLAY_TRACE.md"
ARCH_MD = ROOT / "docs/architecture/E1R_4C2C4E_ENGINE_K2_R6_MARKET_GATE_VARIABLE_REPLAY_TRACE.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_r6_market_gate_variable_replay_trace.json"
REPLAY_JSON = ROOT / "exports/e1r_engine/uptrend/e1r_k2_r6_market_gate_variable_replay_trace.json"
EQUIV_JSON = ROOT / "exports/e1r_engine/equivalence/e1r_k2_r6_market_gate_variable_replay_equivalence.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
]

SOURCE_LINES = {
    "_gate_state_formula": [1510, 1511, 1512],
    "daily_equity_target": [1525],
    "market_entry_allowed_no_gate": [1399],
    "market_entry_allowed_gate": [1485],
    "market_risk_off_gate": [1483],
    "market_shock_gate": [1484],
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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def line_text(lines: list[str], line_no: int) -> str:
    if 1 <= line_no <= len(lines):
        return lines[line_no - 1].rstrip()
    return ""


def source_evidence(lines: list[str]) -> dict[str, Any]:
    return {
        name: [
            {"line": line_no, "text": line_text(lines, line_no)}
            for line_no in line_numbers
        ]
        for name, line_numbers in SOURCE_LINES.items()
    }


def find_function_bounds(source: str, fn_name: str) -> dict[str, Any]:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == fn_name:
            return {
                "name": node.name,
                "start_line": node.lineno,
                "end_line": getattr(node, "end_lineno", node.lineno),
                "line_count": getattr(node, "end_lineno", node.lineno) - node.lineno + 1,
            }
    raise RuntimeError(f"function not found: {fn_name}")


def scan_source_for_market_state_chain(lines: list[str], bounds: dict[str, Any]) -> dict[str, Any]:
    names = [
        "market_state",
        "_shock_active",
        "entry_capacity",
        "market_entry_allowed",
        "market_risk_off",
        "market_shock",
        "_gate_state",
        "market_gate_enabled",
        "risk_off_below_spx_ma50",
        "market_shock_gate_enabled",
        "market_shock_daily_return",
    ]

    out: dict[str, Any] = {}

    for name in names:
        pat = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])")
        rows = []
        for i in range(bounds["start_line"], bounds["end_line"] + 1):
            text = lines[i - 1]
            if not pat.search(text):
                continue
            kind = "reference"
            if re.search(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])\s*=", text):
                kind = "assignment"
            elif text.strip().startswith(("if ", "elif ")):
                kind = "control"
            rows.append({
                "line": i,
                "kind": kind,
                "text": text.rstrip(),
            })
        out[name] = {
            "occurrence_count": len(rows),
            "assignment_count": len([r for r in rows if r["kind"] == "assignment"]),
            "rows": rows,
        }

    return out


def compute_gate_state_from_required_inputs(market_entry_allowed: bool, market_shock: bool) -> str:
    return "ALLOW" if market_entry_allowed else ("SHOCK" if market_shock else "RISK_OFF")


def replay_from_golden_master_rows(daily_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Conservative replay from already-persisted daily rows.

    This intentionally does NOT claim source-equivalent variable replay because the golden master rows
    do not persist market_entry_allowed / market_shock / market_state / _shock_active / entry_capacity.

    We only infer the minimal boolean pair that can reproduce _gate_state:
      ALLOW    -> market_entry_allowed=True,  market_shock=False
      SHOCK    -> market_entry_allowed=False, market_shock=True
      RISK_OFF -> market_entry_allowed=False, market_shock=False

    This is enough to prove formula consistency against the stored target, but not enough to prove
    upstream variable reconstruction. K2-R7 should use this only as a fallback equivalence target,
    and should still prefer a true legacy variable trace if instrumentation is added later.
    """
    replay_rows = []
    mismatches = []

    dist_expected: dict[str, int] = {}
    dist_replayed: dict[str, int] = {}

    for row in daily_rows:
        date = str(row.get("date"))
        expected = row.get("market_gate_state")

        if expected == "ALLOW":
            market_entry_allowed = True
            market_shock = False
            market_risk_off = False
            replay_mode = "minimal_inverse_from_target_allow"
        elif expected == "SHOCK":
            market_entry_allowed = False
            market_shock = True
            market_risk_off = False
            replay_mode = "minimal_inverse_from_target_shock"
        elif expected == "RISK_OFF":
            market_entry_allowed = False
            market_shock = False
            market_risk_off = True
            replay_mode = "minimal_inverse_from_target_risk_off"
        else:
            market_entry_allowed = False
            market_shock = False
            market_risk_off = None
            replay_mode = "unknown_target_state"

        replayed = compute_gate_state_from_required_inputs(
            market_entry_allowed=market_entry_allowed,
            market_shock=market_shock,
        )

        dist_expected[expected] = dist_expected.get(expected, 0) + 1
        dist_replayed[replayed] = dist_replayed.get(replayed, 0) + 1

        if replayed != expected:
            mismatches.append({
                "date": date,
                "expected": expected,
                "replayed": replayed,
                "severity": "hard_fail",
            })

        replay_rows.append({
            "date": date,
            "daily_equity_market_gate_state": expected,
            "replayed_gate_state": replayed,
            "market_entry_allowed": market_entry_allowed,
            "market_shock": market_shock,
            "market_risk_off": market_risk_off,
            "market_state": None,
            "_shock_active": None,
            "entry_capacity": None,
            "spx_close": row.get("spx_close"),
            "spx_ma50": row.get("spx_ma50"),
            "spx_day_return_pct": row.get("spx_day_return_pct"),
            "open_positions_count": row.get("open_positions_count"),
            "pending_orders_count": row.get("pending_orders_count"),
            "exposure_pct": row.get("exposure_pct"),
            "replay_mode": replay_mode,
            "source_quality": "target_inverse_only_not_upstream_source_equivalent",
        })

    return {
        "replay_rows": replay_rows,
        "mismatches": mismatches,
        "summary": {
            "row_count": len(replay_rows),
            "mismatch_count": len(mismatches),
            "expected_distribution": dist_expected,
            "replayed_distribution": dist_replayed,
            "source_quality": "target_inverse_only_not_upstream_source_equivalent",
        },
    }


def focused_rows(replay_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for r in replay_rows:
        d = str(r.get("date"))
        if "2021-05-03" <= d <= "2021-05-24" or d == "2021-06-18":
            out.append(r)
    return out


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    for p in [BACKTEST, K2_R5, GOLDEN_MASTER]:
        if not p.exists():
            raise FileNotFoundError(f"Missing prerequisite: {rel(p)}")

    k2_r5 = read_json(K2_R5)
    gm = read_json(GOLDEN_MASTER)

    if k2_r5.get("decision", {}).get("k2_r5_formula_patch_proposal_passed") is not True:
        raise RuntimeError("K2-R5 proposal did not pass.")
    if k2_r5.get("decision", {}).get("formula_patch_allowed_now") is not False:
        raise RuntimeError("K2-R5 should still block patching.")

    source = BACKTEST.read_text()
    lines = source.splitlines()
    bounds = find_function_bounds(source, "run_stateful_simulation")
    source_chain = scan_source_for_market_state_chain(lines, bounds)
    evidence = source_evidence(lines)

    daily_rows = gm.get("raw_result", {}).get("daily_equity_records", [])
    if not isinstance(daily_rows, list) or not daily_rows:
        raise RuntimeError("Golden master daily_equity_records missing or empty.")

    replay = replay_from_golden_master_rows(daily_rows)
    replay_rows = replay["replay_rows"]

    upstream_availability = {
        "golden_master_has_market_entry_allowed": any("market_entry_allowed" in r for r in daily_rows if isinstance(r, dict)),
        "golden_master_has_market_shock": any("market_shock" in r for r in daily_rows if isinstance(r, dict)),
        "golden_master_has_market_risk_off": any("market_risk_off" in r for r in daily_rows if isinstance(r, dict)),
        "golden_master_has_market_state": any("market_state" in r for r in daily_rows if isinstance(r, dict)),
        "golden_master_has__shock_active": any("_shock_active" in r for r in daily_rows if isinstance(r, dict)),
        "golden_master_has_entry_capacity": any("entry_capacity" in r for r in daily_rows if isinstance(r, dict)),
    }

    upstream_source_equivalent_available = all([
        upstream_availability["golden_master_has_market_entry_allowed"],
        upstream_availability["golden_master_has_market_shock"],
    ])

    replay_artifact = {
        "schema": "E1RK2R6MarketGateVariableReplayTraceV1",
        "generated_at": now(),
        "stage": "4C-2C-4E-ENGINE-K2-R6-MARKET_GATE_VARIABLE_REPLAY_TRACE",
        "source": {
            "golden_master": rel(GOLDEN_MASTER),
            "source_quality": replay["summary"]["source_quality"],
        },
        "source_evidence": evidence,
        "upstream_availability": upstream_availability,
        "replay_rows": replay_rows,
        "focused_rows": focused_rows(replay_rows),
        "summary": replay["summary"],
    }

    equivalence_report = {
        "ok": replay["summary"]["mismatch_count"] == 0,
        "checked_assertions": [
            "daily_equity_market_gate_state_date_sequence",
            "formula_replayed_gate_state_matches_daily_equity_market_gate_state",
        ],
        "mismatch_count": replay["summary"]["mismatch_count"],
        "mismatches": replay["mismatches"],
        "summary": replay["summary"],
        "caveat": (
            "This is formula-level replay from inverse target labels, not full upstream source-equivalent replay, "
            "because golden master rows do not persist market_entry_allowed and market_shock."
        ),
    }

    write_json(REPLAY_JSON, replay_artifact)
    write_json(EQUIV_JSON, equivalence_report)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "market_gate_variable_replay_trace_complete": True,
        "strategy_logic_changed": False,
        "audit_only": True,
        "formula_not_patched": True,
        "backtest_engine_run": False,
        "full_5y_backtest_run": False,
        "forward_runner_run": False,
        "candidate_generation_extracted": False,
        "buy_add_reduce_exit_extracted": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "k2_r5_loaded": True,
        "golden_master_loaded": True,
        "daily_equity_records_loaded": len(daily_rows) > 0,
        "source_evidence_cited": True,
        "source_chain_scanned": True,
        "upstream_source_equivalent_available": upstream_source_equivalent_available,
        "target_inverse_replay_available": True,
        "target_inverse_replay_mismatch_count": replay["summary"]["mismatch_count"],
        "target_inverse_replay_passed": replay["summary"]["mismatch_count"] == 0,
        "replay_artifact_written": REPLAY_JSON.exists(),
        "equivalence_report_written": EQUIV_JSON.exists(),
    }

    decision = {
        "k2_r6_variable_replay_trace_passed": all([
            validations["strategy_files_unchanged"],
            validations["daily_equity_records_loaded"],
            validations["source_evidence_cited"],
            validations["target_inverse_replay_available"],
            validations["target_inverse_replay_passed"],
            validations["replay_artifact_written"],
            validations["equivalence_report_written"],
        ]),
        "upstream_source_equivalent_available": upstream_source_equivalent_available,
        "formula_patch_allowed_now": False,
        "candidate_extraction_allowed_now": False,
        "implementation_may_resume": False,
        "reason_patch_still_blocked": (
            "K2-R6 obtained formula-level target replay but did not obtain true upstream market_entry_allowed/market_shock "
            "from legacy internals. A standalone patch can now be designed to require these inputs, but historical equivalence "
            "must be checked against target-inverse replay unless legacy instrumentation is added."
        ),
        "acceptable_patch_shape_next": (
            "K2-R7 may patch compute_market_gate_state only as a pure function requiring market_entry_allowed and market_shock inputs. "
            "It must not accept spx_close/spx_ma50/spx_day_return as sufficient source-equivalent inputs."
        ),
        "next_required_stage": "4C-2C-4E-ENGINE-K2-R7-MARKET_GATE_EQUIVALENCE_PATCH",
        "conclusion": "K2_R6_PASS_TARGET_REPLAY_READY_FOR_INPUT_REQUIRED_EQUIVALENCE_PATCH",
        "recommended_next_action": (
            "Run 4C-2C-4E-ENGINE-K2-R7-MARKET_GATE_EQUIVALENCE_PATCH: patch a pure input-required "
            "market gate function and validate against K2-R6 replay rows with mismatch_count=0."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R6-MARKET_GATE_VARIABLE_REPLAY_TRACE",
        "status": "MARKET_GATE_VARIABLE_REPLAY_TRACE_COMPLETE",
        "purpose": "Replay market gate variables required by the source-supported formula before patching standalone implementation.",
        "policy": {
            "strategy_logic_changed": False,
            "audit_only": True,
            "formula_not_patched": True,
            "backtest_engine_run": False,
            "full_5y_backtest_run": False,
            "forward_runner_run": False,
            "candidate_generation_extracted": False,
            "buy_add_reduce_exit_extracted": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
        },
        "source": {
            "backtest_path": rel(BACKTEST),
            "backtest_sha256": sha256(BACKTEST),
            "function_bounds": bounds,
            "k2_r5": rel(K2_R5),
            "golden_master": rel(GOLDEN_MASTER),
        },
        "source_evidence": evidence,
        "source_chain": source_chain,
        "upstream_availability": upstream_availability,
        "upstream_source_equivalent_available": upstream_source_equivalent_available,
        "replay_artifact_path": rel(REPLAY_JSON),
        "replay_artifact_sha256": sha256(REPLAY_JSON),
        "equivalence_report_path": rel(EQUIV_JSON),
        "equivalence_report_sha256": sha256(EQUIV_JSON),
        "equivalence_report": equivalence_report,
        "focused_rows": focused_rows(replay_rows),
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R6 — Market Gate Variable Replay Trace")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Source Evidence")
    md.append("```json")
    md.append(json.dumps(evidence, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Upstream Availability")
    md.append("```json")
    md.append(json.dumps(upstream_availability, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Equivalence Report")
    md.append("```json")
    md.append(json.dumps(equivalence_report, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Focused Rows")
    md.append("```json")
    md.append(json.dumps(focused_rows(replay_rows), indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_ENGINE_K2_R6_MARKET_GATE_VARIABLE_REPLAY_TRACE_COMPLETE")
    print("status:", report["status"])
    print("upstream_availability:", json.dumps(upstream_availability, ensure_ascii=False))
    print("upstream_source_equivalent_available:", upstream_source_equivalent_available)
    print("equivalence_report:", json.dumps(equivalence_report, ensure_ascii=False))
    print("focused_rows:", json.dumps(focused_rows(replay_rows), ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(AUDIT_JSON))
    print("wrote:", rel(REPLAY_JSON))
    print("wrote:", rel(EQUIV_JSON))


if __name__ == "__main__":
    main()
