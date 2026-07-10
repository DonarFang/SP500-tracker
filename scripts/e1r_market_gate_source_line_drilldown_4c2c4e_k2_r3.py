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
K2_R2_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R2_MARKET_GATE_SOURCE_TRACE.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R3_MARKET_GATE_SOURCE_LINE_DRILLDOWN.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R3_MARKET_GATE_SOURCE_LINE_DRILLDOWN.md"
ARCH_MD = ROOT / "docs/architecture/E1R_MARKET_GATE_SOURCE_LINE_DRILLDOWN.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_engine_k2_r3_market_gate_source_line_drilldown.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
]

TARGET_LINE_RANGES = [
    (831, 954),
    (1021, 1054),
    (1056, 1091),
    (1370, 1547),
    (1804, 1850),
    (1856, 2013),
    (2121, 2176),
    (2314, 2349),
    (2357, 2430),
]

ASSIGNMENT_PATTERNS = [
    r"\bmarket_gate_state\b",
    r"\bgate_state\b",
    r"\brisk_off\b",
    r"\bshock\b",
    r"\bmarket_gate\b",
    r"\bspx_ma50\b",
    r"\bspx_trend\b",
    r"\bspx_slope\b",
    r"\bmarket_entry_gate\b",
    r"\bD3_RISK_OFF_PLUS_SHOCK_GATE\b",
    r"\bSPX<MA50\b",
]

STRICT_ASSIGNMENT_PATTERNS = [
    r"\bmarket_gate_state\s*=",
    r"\bgate_state\s*=",
    r"\brisk_off\s*=",
    r"\bshock\s*=",
    r"\bmarket_gate\s*=",
    r"\bmarket_entry_gate\s*=",
    r"\bspx_ma50\s*=",
]

CONTROL_PATTERNS = [
    r"\bif\b.*risk_off",
    r"\bif\b.*shock",
    r"\bif\b.*market_gate",
    r"\bif\b.*gate_state",
    r"\belif\b.*risk_off",
    r"\belif\b.*shock",
    r"\belif\b.*market_gate",
    r"\belif\b.*gate_state",
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


def extract_source_rows(lines: list[str], start: int, end: int) -> list[dict[str, Any]]:
    out = []
    for i in range(start, end + 1):
        if i < 1 or i > len(lines):
            continue
        text = lines[i - 1].rstrip()
        matched_any = [p for p in ASSIGNMENT_PATTERNS if re.search(p, text)]
        matched_assign = [p for p in STRICT_ASSIGNMENT_PATTERNS if re.search(p, text)]
        matched_control = [p for p in CONTROL_PATTERNS if re.search(p, text)]
        if matched_any or matched_assign or matched_control:
            out.append({
                "line": i,
                "indent": len(lines[i - 1]) - len(lines[i - 1].lstrip(" ")),
                "text": text,
                "matched_any": matched_any,
                "matched_assign": matched_assign,
                "matched_control": matched_control,
            })
    return out


def extract_context(lines: list[str], center: int, radius: int = 8) -> dict[str, Any]:
    start = max(1, center - radius)
    end = min(len(lines), center + radius)
    return {
        "start": start,
        "end": end,
        "rows": [
            {"line": i, "text": lines[i - 1].rstrip()}
            for i in range(start, end + 1)
        ],
    }


def build_trace_graph(rows: list[dict[str, Any]], lines: list[str]) -> dict[str, Any]:
    assignment_lines = [r for r in rows if r["matched_assign"]]
    control_lines = [r for r in rows if r["matched_control"]]

    important_lines = []
    for r in rows:
        text = r["text"]
        if (
            "market_gate_state" in text
            or "gate_state" in text
            or "risk_off =" in text
            or "shock =" in text
            or "D3_RISK_OFF_PLUS_SHOCK_GATE" in text
            or "SPX<MA50" in text
        ):
            important_lines.append(r["line"])

    contexts = [extract_context(lines, line, radius=10) for line in sorted(set(important_lines))]

    return {
        "assignment_lines": assignment_lines,
        "control_lines": control_lines,
        "important_line_numbers": sorted(set(important_lines)),
        "contexts": contexts,
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    if not BACKTEST.exists():
        raise FileNotFoundError(BACKTEST)
    if not K2_R2_REPORT.exists():
        raise FileNotFoundError(K2_R2_REPORT)

    source = BACKTEST.read_text()
    lines = source.splitlines()
    k2_r2 = read_json(K2_R2_REPORT)

    range_results = []
    all_rows = []

    for start, end in TARGET_LINE_RANGES:
        rows = extract_source_rows(lines, start, end)
        range_results.append({
            "start": start,
            "end": end,
            "line_count": end - start + 1,
            "matched_row_count": len(rows),
            "rows": rows,
        })
        all_rows.extend(rows)

    trace_graph = build_trace_graph(all_rows, lines)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "source_line_drilldown_complete": True,
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
        "k2_r2_loaded": True,
        "target_ranges_scanned": len(TARGET_LINE_RANGES),
        "matched_rows_found": len(all_rows) > 0,
        "assignment_lines_found": len(trace_graph["assignment_lines"]) > 0,
        "important_contexts_found": len(trace_graph["contexts"]) > 0,
    }

    decision = {
        "source_line_drilldown_passed": all([
            validations["strategy_files_unchanged"],
            validations["matched_rows_found"],
            validations["assignment_lines_found"],
            validations["important_contexts_found"],
        ]),
        "matched_row_count": len(all_rows),
        "assignment_line_count": len(trace_graph["assignment_lines"]),
        "important_line_numbers": trace_graph["important_line_numbers"],
        "recommended_next_stage": "4C-2C-4E-ENGINE-K2-R4",
        "conclusion": "MARKET_GATE_SOURCE_LINE_DRILLDOWN_PASS_READY_FOR_FORMULA_RECONSTRUCTION",
        "recommended_next_action": (
            "Use the printed assignment/control contexts to reconstruct the exact legacy market gate formula, "
            "then patch the standalone market gate unit and require daily_market_gate_state mismatch_count=0."
        ),
        "engineering_rule": (
            "Do not use a data-fitted formula. The K2-R4 formula must cite exact assignment/control source lines."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R3",
        "status": "MARKET_GATE_SOURCE_LINE_DRILLDOWN_COMPLETE",
        "purpose": "Extract exact source lines around market gate assignments and controls.",
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
            "k2_r2_report": rel(K2_R2_REPORT),
        },
        "range_results": range_results,
        "trace_graph": trace_graph,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R3 — Market Gate Source Line Drilldown")
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
    md.append("## Trace Graph")
    md.append("```json")
    md.append(json.dumps(trace_graph, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Range Results")
    md.append("```json")
    md.append(json.dumps(range_results, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Decision")
    md.append("```json")
    md.append(json.dumps(decision, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")

    REPORT_MD.write_text("\n".join(md))
    ARCH_MD.write_text("\n".join(md))

    print("E1R_4C2C4E_ENGINE_K2_R3_MARKET_GATE_SOURCE_LINE_DRILLDOWN_COMPLETE")
    print("status:", report["status"])
    print("matched_row_count:", len(all_rows))
    print("assignment_line_count:", len(trace_graph["assignment_lines"]))
    print("important_line_numbers:", json.dumps(trace_graph["important_line_numbers"], ensure_ascii=False))
    print("")
    print("=== ASSIGNMENT LINES ===")
    for row in trace_graph["assignment_lines"]:
        print(f"L{row['line']}: {row['text']}")
    print("")
    print("=== CONTROL LINES ===")
    for row in trace_graph["control_lines"]:
        print(f"L{row['line']}: {row['text']}")
    print("")
    print("=== IMPORTANT CONTEXTS ===")
    for ctx in trace_graph["contexts"]:
        print(f"--- context L{ctx['start']}-L{ctx['end']} ---")
        for row in ctx["rows"]:
            print(f"L{row['line']}: {row['text']}")
    print("")
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(AUDIT_JSON))


if __name__ == "__main__":
    main()
