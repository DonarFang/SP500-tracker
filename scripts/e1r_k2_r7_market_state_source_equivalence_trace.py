#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import hashlib
import runpy
import sys
import os
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

BACKTEST = ROOT / "src/engine/backtest.py"
G_SCRIPT = ROOT / "scripts/e1r_golden_master_harness_4c2c4e_engine_g.py"
GOLDEN_MASTER = ROOT / "exports/e1r_engine/golden_master/e1r_engine_g_short_window_golden_master.json"
K2_R6 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R6_MARKET_GATE_VARIABLE_REPLAY_TRACE.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R7_MARKET_STATE_SOURCE_EQUIVALENCE_TRACE.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R7_MARKET_STATE_SOURCE_EQUIVALENCE_TRACE.md"
ARCH_MD = ROOT / "docs/architecture/E1R_4C2C4E_ENGINE_K2_R7_MARKET_STATE_SOURCE_EQUIVALENCE_TRACE.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_r7_market_state_source_equivalence_trace.json"
TRACE_JSON = ROOT / "exports/e1r_engine/uptrend/e1r_k2_r7_market_state_source_equivalence_trace.json"
EQUIV_JSON = ROOT / "exports/e1r_engine/equivalence/e1r_k2_r7_market_state_source_equivalence.json"

# Running the existing golden master script can rewrite timestamped files.
# We back up and restore them so this stage only commits the K2-R7 artifacts.
G_SCRIPT_SIDE_EFFECT_FILES = [
    ROOT / "docs/research/E1R_4C2C4E_ENGINE_G_GOLDEN_MASTER_HARNESS.json",
    ROOT / "docs/research/E1R_4C2C4E_ENGINE_G_GOLDEN_MASTER_HARNESS.md",
    ROOT / "docs/architecture/E1R_GOLDEN_MASTER_HARNESS_CONTRACT.md",
    ROOT / "exports/e1r_engine/golden_master/e1r_engine_g_short_window_golden_master.json",
]

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
]

CAPTURE_NAMES = [
    "date_t",
    "t",
    "market_state",
    "_shock_active",
    "entry_capacity",
    "market_entry_allowed",
    "market_risk_off",
    "market_shock",
    "_gate_state",
    "spx_close_t",
    "spx_ma50_t",
    "spx_day_return",
    "market_gate_enabled",
    "risk_off_below_spx_ma50",
    "market_shock_gate_enabled",
    "market_shock_daily_return",
    "cash",
    "position_value",
    "total_equity",
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


def read_bytes_or_none(path: Path) -> bytes | None:
    return path.read_bytes() if path.exists() else None


def restore_bytes(path: Path, payload: bytes | None) -> None:
    if payload is None:
        if path.exists():
            path.unlink()
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)


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


def find_line_containing(lines: list[str], needle: str) -> int:
    for idx, text in enumerate(lines, start=1):
        if needle in text:
            return idx
    raise RuntimeError(f"cannot find source line containing: {needle}")


def source_context(lines: list[str], start: int, end: int) -> list[dict[str, Any]]:
    return [
        {"line": i, "text": lines[i - 1].rstrip()}
        for i in range(start, end + 1)
        if 1 <= i <= len(lines)
    ]


def safe_value(v: Any) -> Any:
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    if isinstance(v, (list, tuple, set)):
        return [safe_value(x) for x in list(v)[:20]]
    if isinstance(v, dict):
        return {str(k): safe_value(val) for k, val in list(v.items())[:20]}
    try:
        return float(v)
    except Exception:
        return repr(v)


def safe_len(v: Any) -> int | None:
    try:
        return len(v)
    except Exception:
        return None


def compute_gate_state(market_entry_allowed: bool, market_shock: bool) -> str:
    return "ALLOW" if market_entry_allowed else ("SHOCK" if market_shock else "RISK_OFF")


def source_scan(lines: list[str], bounds: dict[str, Any]) -> dict[str, Any]:
    names = [
        "market_state",
        "_shock_active",
        "entry_capacity",
        "market_entry_allowed",
        "market_risk_off",
        "market_shock",
        "_gate_state",
    ]

    out = {}
    for name in names:
        rows = []
        for i in range(bounds["start_line"], bounds["end_line"] + 1):
            text = lines[i - 1]
            if name not in text:
                continue
            stripped = text.strip()
            kind = "reference"
            if f"{name} =" in text or f"{name}  =" in text or f"{name}     =" in text:
                kind = "assignment"
            elif stripped.startswith(("if ", "elif ")):
                kind = "control"
            rows.append({"line": i, "kind": kind, "text": text.rstrip()})
        out[name] = {
            "occurrence_count": len(rows),
            "assignment_count": len([r for r in rows if r["kind"] == "assignment"]),
            "rows": rows,
        }
    return out


def run_legacy_golden_master_with_trace(backtest_path: Path, capture_line: int) -> list[dict[str, Any]]:
    captured: list[dict[str, Any]] = []

    target_file = str(backtest_path.resolve())

    def tracer(frame, event, arg):
        if event != "line":
            return tracer

        if frame.f_code.co_name != "run_stateful_simulation":
            return tracer

        frame_file = str(Path(frame.f_code.co_filename).resolve())
        if frame_file != target_file:
            return tracer

        if frame.f_lineno != capture_line:
            return tracer

        loc = frame.f_locals

        row = {
            "capture_line": capture_line,
            "source_quality": "legacy_sys_trace_locals",
        }

        for name in CAPTURE_NAMES:
            row[name] = safe_value(loc.get(name))

        row["holdings_count"] = safe_len(loc.get("holdings"))
        row["pending_orders_count"] = safe_len(loc.get("pending_orders"))
        row["closed_trades_count"] = safe_len(loc.get("closed_trades"))

        try:
            row["computed_gate_state_from_captured_inputs"] = compute_gate_state(
                bool(loc.get("market_entry_allowed")),
                bool(loc.get("market_shock")),
            )
        except Exception as exc:
            row["computed_gate_state_from_captured_inputs_error"] = repr(exc)

        captured.append(row)
        return tracer

    old_trace = sys.gettrace()
    old_path = list(sys.path)
    old_env_pythonpath = os.environ.get("PYTHONPATH")

    try:
        sys.path.insert(0, str(ROOT))
        sys.path.insert(0, str(ROOT / "src"))
        os.environ["PYTHONPATH"] = f"{ROOT / 'src'}:{ROOT}"

        sys.settrace(tracer)
        runpy.run_path(str(G_SCRIPT), run_name="__main__")
    finally:
        sys.settrace(old_trace)
        sys.path[:] = old_path
        if old_env_pythonpath is None:
            os.environ.pop("PYTHONPATH", None)
        else:
            os.environ["PYTHONPATH"] = old_env_pythonpath

    return captured


def compare_trace_to_golden_master(trace_rows: list[dict[str, Any]], gm_rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_date = {str(r.get("date")): r for r in gm_rows}
    mismatches = []
    compared = []

    for tr in trace_rows:
        date = str(tr.get("date_t"))
        gm = by_date.get(date)

        if gm is None:
            mismatches.append({
                "date": date,
                "field": "date",
                "expected": "present_in_golden_master_daily_equity_records",
                "actual": "missing",
            })
            continue

        expected_gate = gm.get("market_gate_state")
        captured_gate = tr.get("_gate_state")
        computed_gate = tr.get("computed_gate_state_from_captured_inputs")

        row = {
            "date": date,
            "expected_market_gate_state": expected_gate,
            "captured__gate_state": captured_gate,
            "computed_gate_state_from_captured_inputs": computed_gate,
            "market_entry_allowed": tr.get("market_entry_allowed"),
            "market_shock": tr.get("market_shock"),
            "market_risk_off": tr.get("market_risk_off"),
            "market_state": tr.get("market_state"),
            "_shock_active": tr.get("_shock_active"),
            "entry_capacity": tr.get("entry_capacity"),
            "spx_close_t": tr.get("spx_close_t"),
            "spx_ma50_t": tr.get("spx_ma50_t"),
            "spx_day_return": tr.get("spx_day_return"),
            "holdings_count": tr.get("holdings_count"),
            "pending_orders_count": tr.get("pending_orders_count"),
            "source_quality": tr.get("source_quality"),
        }
        compared.append(row)

        if captured_gate != expected_gate:
            mismatches.append({
                "date": date,
                "field": "_gate_state_vs_daily_equity_market_gate_state",
                "expected": expected_gate,
                "actual": captured_gate,
            })

        if computed_gate != expected_gate:
            mismatches.append({
                "date": date,
                "field": "computed_gate_state_from_captured_inputs",
                "expected": expected_gate,
                "actual": computed_gate,
            })

    expected_dates = [str(r.get("date")) for r in gm_rows]
    trace_dates = [str(r.get("date_t")) for r in trace_rows]

    if expected_dates != trace_dates:
        mismatches.append({
            "field": "date_sequence",
            "expected_head_tail_count": {
                "count": len(expected_dates),
                "head": expected_dates[:5],
                "tail": expected_dates[-5:],
            },
            "actual_head_tail_count": {
                "count": len(trace_dates),
                "head": trace_dates[:5],
                "tail": trace_dates[-5:],
            },
        })

    dist_expected: dict[str, int] = {}
    dist_captured: dict[str, int] = {}
    dist_computed: dict[str, int] = {}

    for r in compared:
        dist_expected[r["expected_market_gate_state"]] = dist_expected.get(r["expected_market_gate_state"], 0) + 1
        dist_captured[r["captured__gate_state"]] = dist_captured.get(r["captured__gate_state"], 0) + 1
        dist_computed[r["computed_gate_state_from_captured_inputs"]] = dist_computed.get(r["computed_gate_state_from_captured_inputs"], 0) + 1

    return {
        "ok": len(mismatches) == 0,
        "checked_assertions": [
            "legacy_trace_date_sequence_equals_golden_master_daily_equity_records",
            "captured__gate_state_equals_daily_equity_market_gate_state",
            "computed_gate_state_from_captured_market_entry_allowed_market_shock_equals_daily_equity_market_gate_state",
        ],
        "row_count": len(compared),
        "expected_row_count": len(gm_rows),
        "trace_row_count": len(trace_rows),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "distribution": {
            "expected": dist_expected,
            "captured__gate_state": dist_captured,
            "computed_from_captured_inputs": dist_computed,
        },
        "compared_rows": compared,
    }


def focused_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for r in rows:
        d = str(r.get("date"))
        if "2021-05-03" <= d <= "2021-05-24" or d == "2021-06-18":
            out.append(r)
    return out


def main() -> None:
    started = datetime.now(timezone.utc)

    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}
    side_effect_backups = {p: read_bytes_or_none(p) for p in G_SCRIPT_SIDE_EFFECT_FILES}

    for p in [BACKTEST, G_SCRIPT, GOLDEN_MASTER, K2_R6]:
        if not p.exists():
            raise FileNotFoundError(f"Missing prerequisite: {rel(p)}")

    k2_r6 = read_json(K2_R6)
    if k2_r6.get("decision", {}).get("k2_r6_variable_replay_trace_passed") is not True:
        raise RuntimeError("K2-R6 did not pass.")
    if k2_r6.get("upstream_source_equivalent_available") is not False:
        raise RuntimeError("K2-R6 state unexpected; expected upstream_source_equivalent_available=false.")

    source = BACKTEST.read_text()
    lines = source.splitlines()
    bounds = find_function_bounds(source, "run_stateful_simulation")
    target_line = find_line_containing(lines, '"market_gate_state": _gate_state')

    source_evidence = {
        "function_bounds": bounds,
        "capture_line": target_line,
        "capture_line_text": lines[target_line - 1].rstrip(),
        "_gate_state_formula_context": source_context(lines, 1510, 1512),
        "market_state_chain_static_scan": source_scan(lines, bounds),
    }

    try:
        trace_rows = run_legacy_golden_master_with_trace(BACKTEST, target_line)
    finally:
        # Restore timestamped golden-master outputs from the harness run.
        for path, payload in side_effect_backups.items():
            restore_bytes(path, payload)

    gm = read_json(GOLDEN_MASTER)
    gm_rows = gm.get("raw_result", {}).get("daily_equity_records", [])
    if not isinstance(gm_rows, list) or not gm_rows:
        raise RuntimeError("Golden master daily_equity_records missing after restore.")

    equivalence = compare_trace_to_golden_master(trace_rows, gm_rows)
    compared_rows = equivalence["compared_rows"]

    upstream_values_available = all(
        r.get("market_entry_allowed") is not None
        and r.get("market_shock") is not None
        and r.get("market_risk_off") is not None
        and r.get("market_state") is not None
        and r.get("_shock_active") is not None
        and r.get("entry_capacity") is not None
        for r in compared_rows
    )

    trace_artifact = {
        "schema": "E1RK2R7MarketStateSourceEquivalenceTraceV1",
        "generated_at": now(),
        "stage": "4C-2C-4E-ENGINE-K2-R7-MARKET_STATE_SOURCE_EQUIVALENCE_TRACE",
        "source_quality": "legacy_sys_trace_locals",
        "source": {
            "backtest": rel(BACKTEST),
            "backtest_sha256": sha256(BACKTEST),
            "golden_master_harness": rel(G_SCRIPT),
            "golden_master": rel(GOLDEN_MASTER),
            "capture_line": target_line,
        },
        "source_evidence": source_evidence,
        "trace_rows": trace_rows,
        "compared_rows": compared_rows,
        "focused_rows": focused_rows(compared_rows),
        "equivalence": {
            k: v for k, v in equivalence.items()
            if k != "compared_rows"
        },
    }

    write_json(TRACE_JSON, trace_artifact)

    equivalence_report = {
        k: v for k, v in equivalence.items()
        if k != "compared_rows"
    }
    equivalence_report["focused_rows"] = focused_rows(compared_rows)
    equivalence_report["source_quality"] = "legacy_sys_trace_locals"
    equivalence_report["upstream_values_available"] = upstream_values_available
    write_json(EQUIV_JSON, equivalence_report)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "market_state_source_equivalence_trace_complete": True,
        "strategy_logic_changed": False,
        "audit_only": True,
        "formula_not_patched": True,
        "short_window_existing_engine_run": True,
        "legacy_run_under_sys_trace": True,
        "full_5y_backtest_run": False,
        "forward_runner_run": False,
        "candidate_generation_extracted": False,
        "buy_add_reduce_exit_extracted": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "golden_master_side_effect_files_restored": all(
            read_bytes_or_none(p) == payload for p, payload in side_effect_backups.items()
        ),
        "k2_r6_loaded": True,
        "capture_line_found": target_line > 0,
        "trace_rows_captured": len(trace_rows) > 0,
        "daily_equity_records_loaded": len(gm_rows) > 0,
        "trace_row_count_equals_daily_equity_count": len(trace_rows) == len(gm_rows),
        "equivalence_ok": equivalence["ok"],
        "mismatch_count": equivalence["mismatch_count"],
        "upstream_values_available": upstream_values_available,
        "trace_artifact_written": TRACE_JSON.exists(),
        "equivalence_report_written": EQUIV_JSON.exists(),
    }

    decision = {
        "k2_r7_market_state_source_equivalence_trace_passed": all([
            validations["strategy_files_unchanged"],
            validations["golden_master_side_effect_files_restored"],
            validations["trace_rows_captured"],
            validations["trace_row_count_equals_daily_equity_count"],
            validations["equivalence_ok"],
            validations["mismatch_count"] == 0,
            validations["upstream_values_available"],
            validations["trace_artifact_written"],
            validations["equivalence_report_written"],
        ]),
        "formula_patch_allowed_now": False,
        "candidate_extraction_allowed_now": False,
        "implementation_may_resume": False,
        "source_equivalent_market_state_trace_available": upstream_values_available and equivalence["ok"],
        "next_required_stage_if_pass": "4C-2C-4E-ENGINE-K2-R8-MARKET_STATE_PARAMETER_AUDIT",
        "next_required_stage_if_fail": "4C-2C-4E-ENGINE-K2-R7B-TRACE_CAPTURE_REPAIR",
        "conclusion": (
            "K2_R7_PASS_SOURCE_EQUIVALENT_MARKET_STATE_TRACE_READY_FOR_PARAMETER_AUDIT"
            if upstream_values_available and equivalence["ok"]
            else "K2_R7_NEEDS_TRACE_CAPTURE_REPAIR"
        ),
        "recommended_next_action": (
            "If PASS, audit the exact market-state/gate assumptions and parameters used by the 115% E1R run. "
            "If FAIL, repair trace capture before any patch."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R7-MARKET_STATE_SOURCE_EQUIVALENCE_TRACE",
        "status": "MARKET_STATE_SOURCE_EQUIVALENCE_TRACE_COMPLETE",
        "purpose": "Capture real legacy market-state variables from run_stateful_simulation locals and verify source-equivalent market gate state.",
        "policy": {
            "strategy_logic_changed": False,
            "audit_only": True,
            "formula_not_patched": True,
            "short_window_existing_engine_run": True,
            "legacy_run_under_sys_trace": True,
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
            "golden_master_harness": rel(G_SCRIPT),
            "golden_master": rel(GOLDEN_MASTER),
            "capture_line": target_line,
        },
        "source_evidence": source_evidence,
        "trace_artifact_path": rel(TRACE_JSON),
        "trace_artifact_sha256": sha256(TRACE_JSON),
        "equivalence_report_path": rel(EQUIV_JSON),
        "equivalence_report_sha256": sha256(EQUIV_JSON),
        "equivalence_report": equivalence_report,
        "focused_rows": focused_rows(compared_rows),
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R7 — Market State Source Equivalence Trace")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Source")
    md.append("```json")
    md.append(json.dumps(report["source"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Equivalence Report")
    md.append("```json")
    md.append(json.dumps(equivalence_report, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Focused Rows")
    md.append("```json")
    md.append(json.dumps(focused_rows(compared_rows), indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_ENGINE_K2_R7_MARKET_STATE_SOURCE_EQUIVALENCE_TRACE_COMPLETE")
    print("status:", report["status"])
    print("capture_line:", target_line)
    print("trace_row_count:", len(trace_rows))
    print("daily_equity_row_count:", len(gm_rows))
    print("equivalence_report:", json.dumps(equivalence_report, ensure_ascii=False))
    print("focused_rows:", json.dumps(focused_rows(compared_rows), ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(AUDIT_JSON))
    print("wrote:", rel(TRACE_JSON))
    print("wrote:", rel(EQUIV_JSON))


if __name__ == "__main__":
    main()
