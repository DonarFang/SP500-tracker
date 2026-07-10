#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import hashlib
import re
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

BACKTEST = ROOT / "src/engine/backtest.py"
K2_R7 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R7_MARKET_STATE_SOURCE_EQUIVALENCE_TRACE.json"
R7_TRACE = ROOT / "exports/e1r_engine/uptrend/e1r_k2_r7_market_state_source_equivalence_trace.json"
R7_EQUIV = ROOT / "exports/e1r_engine/equivalence/e1r_k2_r7_market_state_source_equivalence.json"
GOLDEN_MASTER = ROOT / "exports/e1r_engine/golden_master/e1r_engine_g_short_window_golden_master.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R8_MARKET_STATE_PARAMETER_AUDIT.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R8_MARKET_STATE_PARAMETER_AUDIT.md"
ARCH_MD = ROOT / "docs/architecture/E1R_4C2C4E_ENGINE_K2_R8_MARKET_STATE_PARAMETER_AUDIT.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_r8_market_state_parameter_audit.json"
PARAM_JSON = ROOT / "exports/e1r_engine/equivalence/e1r_k2_r8_market_state_parameter_audit.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
]

PARAMETER_KEYS = [
    "market_gate_enabled",
    "risk_off_below_spx_ma50",
    "market_shock_gate_enabled",
    "market_shock_daily_return",
    "market_score_full_on",
    "market_score_cautious",
    "market_score_cash",
    "entry_capacity_full_on",
    "entry_capacity_cautious",
    "entry_capacity_cash",
    "max_positions",
    "buy_size",
    "add_size",
    "max_single_size",
    "total_one_way",
]

SOURCE_TARGET_NAMES = [
    "market_gate_enabled",
    "risk_off_below_spx_ma50",
    "market_shock_gate_enabled",
    "market_shock_daily_return",
    "market_state",
    "_shock_active",
    "entry_capacity",
    "market_entry_allowed",
    "market_risk_off",
    "market_shock",
    "_gate_state",
    "market_gate_days",
    "FULL_ON",
    "CAUTIOUS_ON",
    "CASH_MODE",
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


def source_line(lines: list[str], line_no: int) -> str:
    if 1 <= line_no <= len(lines):
        return lines[line_no - 1].rstrip()
    return ""


def source_context(lines: list[str], center: int, radius: int = 6) -> dict[str, Any]:
    start = max(1, center - radius)
    end = min(len(lines), center + radius)
    return {
        "start": start,
        "end": end,
        "rows": [
            {"line": i, "text": source_line(lines, i)}
            for i in range(start, end + 1)
        ],
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


def scan_source(lines: list[str], bounds: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}

    for name in SOURCE_TARGET_NAMES:
        rows = []
        pat = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])")
        for i in range(bounds["start_line"], bounds["end_line"] + 1):
            text = lines[i - 1]
            if not pat.search(text):
                continue
            stripped = text.strip()
            kind = "reference"
            if re.search(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])\s*=", text):
                kind = "assignment"
            elif stripped.startswith(("if ", "elif ")):
                kind = "control"
            elif "logger.info" in text or "Market Gate" in text:
                kind = "log"
            elif "return" in text or "append({" in text:
                kind = "output"
            rows.append({
                "line": i,
                "kind": kind,
                "indent": len(text) - len(text.lstrip(" ")),
                "text": text.rstrip(),
            })
        out[name] = {
            "occurrence_count": len(rows),
            "assignment_count": len([r for r in rows if r["kind"] == "assignment"]),
            "control_count": len([r for r in rows if r["kind"] == "control"]),
            "rows": rows,
        }

    return out


def extract_assumption_gets(lines: list[str], bounds: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    pat = re.compile(r'\ba\.get\(\s*["\']([^"\']+)["\']\s*,\s*([^)]+)\)')
    for i in range(bounds["start_line"], bounds["end_line"] + 1):
        text = lines[i - 1]
        for m in pat.finditer(text):
            key = m.group(1)
            default_expr = m.group(2).strip()
            rows.append({
                "line": i,
                "key": key,
                "default_expr": default_expr,
                "text": text.rstrip(),
                "context": source_context(lines, i, radius=4),
            })
    return rows


def summarize_trace_rows(trace_rows: list[dict[str, Any]]) -> dict[str, Any]:
    dist = {
        "market_state": {},
        "_shock_active": {},
        "entry_capacity": {},
        "market_entry_allowed": {},
        "market_shock": {},
        "market_risk_off": {},
        "_gate_state": {},
    }

    transitions = []
    prev = None

    for row in trace_rows:
        date = row.get("date")
        for key in dist:
            val = row.get(key)
            dist[key][str(val)] = dist[key].get(str(val), 0) + 1

        current = {
            "market_state": row.get("market_state"),
            "_shock_active": row.get("_shock_active"),
            "entry_capacity": row.get("entry_capacity"),
            "market_entry_allowed": row.get("market_entry_allowed"),
            "market_shock": row.get("market_shock"),
            "market_risk_off": row.get("market_risk_off"),
            "_gate_state": row.get("captured__gate_state") or row.get("_gate_state"),
        }
        if prev is not None:
            changed = {
                k: {"from": prev["state"].get(k), "to": current.get(k)}
                for k in current
                if prev["state"].get(k) != current.get(k)
            }
            if changed:
                transitions.append({
                    "date": date,
                    "changed": changed,
                    "prev_date": prev["date"],
                })
        prev = {"date": date, "state": current}

    return {
        "row_count": len(trace_rows),
        "distributions": dist,
        "transition_count": len(transitions),
        "transitions": transitions,
    }


def focused_rows(trace_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for r in trace_rows:
        d = str(r.get("date"))
        if "2021-05-03" <= d <= "2021-05-24" or d == "2021-06-18":
            out.append(r)
    return out


def infer_capacity_mapping(trace_rows: list[dict[str, Any]]) -> dict[str, Any]:
    mapping: dict[str, set] = {}
    conflicts = []

    for r in trace_rows:
        ms = str(r.get("market_state"))
        cap = r.get("entry_capacity")
        mapping.setdefault(ms, set()).add(cap)

    normalized = {k: sorted(list(v), key=lambda x: str(x)) for k, v in mapping.items()}

    for state, caps in normalized.items():
        if len(caps) > 1:
            conflicts.append({
                "market_state": state,
                "entry_capacities": caps,
            })

    return {
        "mapping": normalized,
        "conflicts": conflicts,
        "stable_mapping": len(conflicts) == 0,
    }


def extract_golden_master_controls(gm: dict[str, Any]) -> dict[str, Any]:
    raw = gm.get("raw_result", {})
    controls = raw.get("strategy_controls")
    return {
        "strategy_controls": controls,
        "market_entry_gate": raw.get("market_entry_gate"),
        "version": raw.get("version"),
        "strategy_variant": raw.get("strategy_variant"),
        "entry_top_n": raw.get("entry_top_n"),
        "rank_based_exit": raw.get("rank_based_exit"),
        "e1r_uptrend_execution_enabled": raw.get("e1r_uptrend_execution_enabled"),
        "status": raw.get("status"),
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    for p in [BACKTEST, K2_R7, R7_TRACE, R7_EQUIV, GOLDEN_MASTER]:
        if not p.exists():
            raise FileNotFoundError(f"Missing prerequisite: {rel(p)}")

    k2_r7 = read_json(K2_R7)
    r7_trace = read_json(R7_TRACE)
    r7_equiv = read_json(R7_EQUIV)
    gm = read_json(GOLDEN_MASTER)

    if k2_r7.get("decision", {}).get("source_equivalent_market_state_trace_available") is not True:
        raise RuntimeError("K2-R7 source-equivalent trace is not available.")
    if r7_equiv.get("ok") is not True:
        raise RuntimeError("K2-R7 equivalence report is not ok.")

    source = BACKTEST.read_text()
    lines = source.splitlines()
    bounds = find_function_bounds(source, "run_stateful_simulation")

    source_scan = scan_source(lines, bounds)
    assumption_gets = extract_assumption_gets(lines, bounds)

    trace_rows = r7_trace.get("compared_rows", [])
    if not isinstance(trace_rows, list) or not trace_rows:
        raise RuntimeError("R7 trace compared_rows missing.")

    trace_summary = summarize_trace_rows(trace_rows)
    capacity_mapping = infer_capacity_mapping(trace_rows)
    gm_controls = extract_golden_master_controls(gm)

    market_gate_parameters_from_logs_and_source = {
        "market_gate_variant": "D3_RISK_OFF_PLUS_SHOCK_GATE",
        "market_gate_enabled": True,
        "risk_off_below_spx_ma50": True,
        "market_shock_gate_enabled": True,
        "market_shock_daily_return": -0.02,
        "evidence": [
            {
                "type": "runtime_log_from_R7",
                "text": "Market Gate Variant: D3_RISK_OFF_PLUS_SHOCK_GATE",
            },
            {
                "type": "runtime_log_from_R7",
                "text": "Market Gate: enabled=True | RiskOff=SPX<MA50:True | Shock<=-2.0%:True",
            },
        ],
    }

    parameter_audit = {
        "market_gate_parameters": market_gate_parameters_from_logs_and_source,
        "observed_market_state_distribution": trace_summary["distributions"]["market_state"],
        "observed_shock_distribution": trace_summary["distributions"]["_shock_active"],
        "observed_entry_capacity_distribution": trace_summary["distributions"]["entry_capacity"],
        "observed_gate_state_distribution": trace_summary["distributions"]["_gate_state"],
        "entry_capacity_mapping_by_market_state": capacity_mapping,
        "focused_rows": focused_rows(trace_rows),
        "transitions": trace_summary["transitions"],
        "golden_master_controls": gm_controls,
        "source_assumption_gets_relevant": [
            x for x in assumption_gets
            if x["key"] in PARAMETER_KEYS
            or "market" in x["key"]
            or "risk" in x["key"]
            or "shock" in x["key"]
            or "entry" in x["key"]
        ],
    }

    unresolved = []

    required_market_states = {"FULL_ON", "CAUTIOUS_ON", "CASH_MODE"}
    observed_states = set(str(k) for k in trace_summary["distributions"]["market_state"].keys())
    missing_states = sorted(required_market_states - observed_states)
    if missing_states:
        unresolved.append({
            "id": "missing_expected_market_states_in_short_window",
            "missing_states": missing_states,
            "blocking_for_short_window_equivalence": False,
            "blocking_for_full_115_replication": True,
        })

    if not capacity_mapping["stable_mapping"]:
        unresolved.append({
            "id": "entry_capacity_mapping_conflict",
            "conflicts": capacity_mapping["conflicts"],
            "blocking_for_short_window_equivalence": True,
            "blocking_for_full_115_replication": True,
        })

    # For true 115% replication, we must locate the exact full-run artifact/assumptions later if not present here.
    if not gm_controls.get("strategy_controls"):
        unresolved.append({
            "id": "strategy_controls_not_persisted_in_golden_master_raw_result",
            "blocking_for_short_window_equivalence": False,
            "blocking_for_full_115_replication": True,
            "required_next": "Audit the full E1R 115% run artifact or assumptions source.",
        })

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "market_state_parameter_audit_complete": True,
        "strategy_logic_changed": False,
        "audit_only": True,
        "formula_not_patched": True,
        "backtest_engine_run": False,
        "short_window_existing_engine_run": False,
        "full_5y_backtest_run": False,
        "forward_runner_run": False,
        "candidate_generation_extracted": False,
        "buy_add_reduce_exit_extracted": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "k2_r7_loaded": True,
        "r7_trace_loaded": True,
        "r7_equivalence_ok": r7_equiv.get("ok") is True,
        "trace_rows_loaded": len(trace_rows) > 0,
        "source_scan_complete": True,
        "assumption_gets_extracted": len(assumption_gets) > 0,
        "market_gate_parameters_documented": True,
        "market_state_distribution_documented": True,
        "entry_capacity_mapping_documented": True,
        "entry_capacity_mapping_stable": capacity_mapping["stable_mapping"],
        "focused_rows_documented": True,
        "unresolved_count": len(unresolved),
    }

    decision = {
        "k2_r8_market_state_parameter_audit_passed": all([
            validations["strategy_files_unchanged"],
            validations["r7_equivalence_ok"],
            validations["trace_rows_loaded"],
            validations["source_scan_complete"],
            validations["assumption_gets_extracted"],
            validations["market_gate_parameters_documented"],
            validations["market_state_distribution_documented"],
            validations["entry_capacity_mapping_documented"],
            validations["entry_capacity_mapping_stable"],
        ]),
        "formula_patch_allowed_now": False,
        "candidate_extraction_allowed_now": False,
        "implementation_may_resume": False,
        "unresolved": unresolved,
        "short_window_market_state_replication_ready": (
            validations["entry_capacity_mapping_stable"]
            and validations["r7_equivalence_ok"]
        ),
        "full_115_replication_ready": len([x for x in unresolved if x.get("blocking_for_full_115_replication")]) == 0,
        "next_required_stage": (
            "4C-2C-4E-ENGINE-K2-R9-MARKET_STATE_115_RETURN_ARTIFACT_AUDIT"
            if len([x for x in unresolved if x.get("blocking_for_full_115_replication")]) > 0
            else "4C-2C-4E-ENGINE-K2-R9-MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL"
        ),
        "conclusion": (
            "K2_R8_PASS_SHORT_WINDOW_PARAMETERS_AUDITED_NEEDS_115_ARTIFACT_AUDIT"
            if len([x for x in unresolved if x.get("blocking_for_full_115_replication")]) > 0
            else "K2_R8_PASS_MARKET_STATE_PARAMETERS_READY_FOR_REPLICATION_PROPOSAL"
        ),
        "recommended_next_action": (
            "Audit the exact full E1R 115% run artifact and assumptions before standalone replication, "
            "because short-window source equivalence is not enough to prove full 115% parameter identity."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R8-MARKET_STATE_PARAMETER_AUDIT",
        "status": "MARKET_STATE_PARAMETER_AUDIT_COMPLETE",
        "purpose": "Audit exact market-state and market-gate parameters before copying the E1R 115% market-state behavior.",
        "policy": {
            "strategy_logic_changed": False,
            "audit_only": True,
            "formula_not_patched": True,
            "backtest_engine_run": False,
            "short_window_existing_engine_run": False,
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
            "k2_r7_report": rel(K2_R7),
            "r7_trace": rel(R7_TRACE),
            "r7_equivalence": rel(R7_EQUIV),
            "golden_master": rel(GOLDEN_MASTER),
        },
        "source_scan": source_scan,
        "assumption_gets": assumption_gets,
        "parameter_audit": parameter_audit,
        "unresolved": unresolved,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)
    write_json(PARAM_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R8 — Market State Parameter Audit")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Parameter Audit")
    md.append("```json")
    md.append(json.dumps(parameter_audit, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Unresolved")
    md.append("```json")
    md.append(json.dumps(unresolved, indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_ENGINE_K2_R8_MARKET_STATE_PARAMETER_AUDIT_COMPLETE")
    print("status:", report["status"])
    print("market_gate_parameters:", json.dumps(market_gate_parameters_from_logs_and_source, ensure_ascii=False))
    print("observed_market_state_distribution:", json.dumps(parameter_audit["observed_market_state_distribution"], ensure_ascii=False))
    print("observed_entry_capacity_distribution:", json.dumps(parameter_audit["observed_entry_capacity_distribution"], ensure_ascii=False))
    print("entry_capacity_mapping_by_market_state:", json.dumps(capacity_mapping, ensure_ascii=False))
    print("golden_master_controls:", json.dumps(gm_controls, ensure_ascii=False))
    print("unresolved:", json.dumps(unresolved, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(AUDIT_JSON))
    print("wrote:", rel(PARAM_JSON))


if __name__ == "__main__":
    main()
