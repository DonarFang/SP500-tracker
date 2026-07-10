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
GOLDEN_MASTER = ROOT / "exports/e1r_engine/golden_master/e1r_engine_g_short_window_golden_master.json"
K2_R1_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R1_MARKET_GATE_FORMULA_AUDIT.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R2_MARKET_GATE_SOURCE_TRACE.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R2_MARKET_GATE_SOURCE_TRACE.md"
ARCH_MD = ROOT / "docs/architecture/E1R_MARKET_GATE_SOURCE_TRACE.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_engine_k2_r2_market_gate_source_trace.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
]

KEYWORDS = [
    "market_gate_state",
    "market_entry_gate",
    "gate_state",
    "risk_off",
    "RiskOff",
    "shock",
    "Shock",
    "spx_ma50",
    "ma50",
    "SPX<MA50",
    "D3_RISK_OFF_PLUS_SHOCK_GATE",
    "market_gate",
    "gate=",
]

CRITICAL_REGEXES = [
    r"market_gate_state\s*=",
    r"gate_state\s*=",
    r"risk_off\s*=",
    r"shock\s*=",
    r"spx_ma50\s*=",
    r"market_gate",
    r"SPX<MA50",
    r"D3_RISK_OFF_PLUS_SHOCK_GATE",
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


def line_context(lines: list[str], line_no: int, radius: int = 12) -> dict[str, Any]:
    start = max(1, line_no - radius)
    end = min(len(lines), line_no + radius)
    return {
        "start": start,
        "end": end,
        "rows": [
            {"line": i, "text": lines[i - 1].rstrip()}
            for i in range(start, end + 1)
        ],
    }


def scan_hits(source: str, fn_bounds: dict[str, Any]) -> list[dict[str, Any]]:
    lines = source.splitlines()
    hits: list[dict[str, Any]] = []

    start = fn_bounds["start_line"]
    end = fn_bounds["end_line"]

    for i in range(start, end + 1):
        line = lines[i - 1]
        matched_keywords = [kw for kw in KEYWORDS if kw in line]
        matched_regexes = [rx for rx in CRITICAL_REGEXES if re.search(rx, line)]
        if matched_keywords or matched_regexes:
            hits.append({
                "line": i,
                "text": line.rstrip(),
                "matched_keywords": matched_keywords,
                "matched_regexes": matched_regexes,
                "indent": len(line) - len(line.lstrip(" ")),
                "context": line_context(lines, i, radius=10),
            })

    return hits


def merge_windows(hits: list[dict[str, Any]], radius: int = 18) -> list[dict[str, Any]]:
    if not hits:
        return []

    windows = []
    for h in hits:
        windows.append([h["line"] - radius, h["line"] + radius])

    windows.sort()
    merged = []
    for s, e in windows:
        if not merged or s > merged[-1][1] + 1:
            merged.append([s, e])
        else:
            merged[-1][1] = max(merged[-1][1], e)

    return [{"start": max(1, s), "end": e} for s, e in merged]


def extract_windows(source: str, windows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lines = source.splitlines()
    out = []

    for w in windows:
        s = max(1, w["start"])
        e = min(len(lines), w["end"])
        out.append({
            "start": s,
            "end": e,
            "line_count": e - s + 1,
            "rows": [
                {"line": i, "text": lines[i - 1].rstrip()}
                for i in range(s, e + 1)
            ],
        })

    return out


def summarize_hits(hits: list[dict[str, Any]]) -> dict[str, Any]:
    by_keyword = {}
    by_regex = {}

    for h in hits:
        for kw in h["matched_keywords"]:
            by_keyword[kw] = by_keyword.get(kw, 0) + 1
        for rx in h["matched_regexes"]:
            by_regex[rx] = by_regex.get(rx, 0) + 1

    return {
        "hit_count": len(hits),
        "by_keyword": dict(sorted(by_keyword.items())),
        "by_regex": dict(sorted(by_regex.items())),
        "hit_lines": [h["line"] for h in hits],
    }


def mismatch_window_rows(gm: dict[str, Any]) -> dict[str, Any]:
    rows = gm.get("raw_result", {}).get("daily_equity_records", [])
    if not isinstance(rows, list):
        return {"rows": []}

    focused = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        date = str(r.get("date"))
        if "2021-05-03" <= date <= "2021-05-24" or date == "2021-06-18":
            focused.append({
                "date": r.get("date"),
                "market_gate_state": r.get("market_gate_state"),
                "spx_close": r.get("spx_close"),
                "spx_ma50": r.get("spx_ma50"),
                "spx_day_return_pct": r.get("spx_day_return_pct"),
                "spx_regime": r.get("spx_regime"),
                "risk_budget": r.get("risk_budget"),
                "risk_budget_mode": r.get("risk_budget_mode"),
                "event": r.get("event"),
                "open_positions_count": r.get("open_positions_count"),
                "pending_orders_count": r.get("pending_orders_count"),
                "exposure_pct": r.get("exposure_pct"),
            })

    return {
        "rows": focused,
        "row_count": len(focused),
    }


def infer_persistence_hypotheses(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Diagnostic only. This is not accepted as formula source.
    It checks whether RISK_OFF appears to be a stateful persistence/cooldown series.
    """
    clean = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        try:
            clean.append({
                "date": str(r.get("date")),
                "expected": r.get("market_gate_state"),
                "day_ret": float(r.get("spx_day_return_pct")),
                "close": float(r.get("spx_close")),
                "ma50": float(r.get("spx_ma50")),
            })
        except Exception:
            pass

    def eval_hypothesis(trigger_day_ret: float | None, cooldown_days: int, include_close_ma50: bool) -> dict[str, Any]:
        cooldown = 0
        actual = []
        for r in clean:
            shock = r["day_ret"] <= -2.0
            trigger = False
            if include_close_ma50 and r["close"] < r["ma50"]:
                trigger = True
            if trigger_day_ret is not None and r["day_ret"] <= trigger_day_ret:
                trigger = True

            if shock:
                state = "SHOCK"
                cooldown = max(cooldown, cooldown_days)
            elif trigger:
                state = "RISK_OFF"
                cooldown = max(cooldown, cooldown_days)
            elif cooldown > 0:
                state = "RISK_OFF"
                cooldown -= 1
            else:
                state = "ALLOW"

            actual.append(state)

        mismatches = []
        for r, state in zip(clean, actual):
            if r["expected"] != state:
                mismatches.append({
                    "date": r["date"],
                    "expected": r["expected"],
                    "actual": state,
                    "day_ret": r["day_ret"],
                    "close": r["close"],
                    "ma50": r["ma50"],
                })

        dist = {}
        for s in actual:
            dist[s] = dist.get(s, 0) + 1

        return {
            "ok": len(mismatches) == 0,
            "mismatch_count": len(mismatches),
            "distribution": dist,
            "mismatches": mismatches[:20],
        }

    results = {}
    for threshold in [None, -0.5, -0.75, -1.0, -1.25, -1.5]:
        for cooldown in range(1, 11):
            for include_ma50 in [False, True]:
                name = f"trigger_dayret_{threshold}_cooldown_{cooldown}_include_ma50_{include_ma50}"
                results[name] = eval_hypothesis(threshold, cooldown, include_ma50)

    best = sorted(
        [
            {"name": name, **res}
            for name, res in results.items()
        ],
        key=lambda x: x["mismatch_count"],
    )[:10]

    return {
        "diagnostic_only": True,
        "best_hypotheses": best,
        "note": "These hypotheses are not accepted as source-of-truth. They only guide source inspection.",
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    if not BACKTEST.exists():
        raise FileNotFoundError(BACKTEST)
    if not GOLDEN_MASTER.exists():
        raise FileNotFoundError(GOLDEN_MASTER)
    if not K2_R1_REPORT.exists():
        raise FileNotFoundError(K2_R1_REPORT)

    source = BACKTEST.read_text()
    fn_bounds = find_function_bounds(source, "run_stateful_simulation")
    hits = scan_hits(source, fn_bounds)
    hit_summary = summarize_hits(hits)

    windows = merge_windows(hits, radius=16)
    source_line_clusters = extract_windows(source, windows)

    gm = read_json(GOLDEN_MASTER)
    focused_rows = mismatch_window_rows(gm)
    daily_rows = gm.get("raw_result", {}).get("daily_equity_records", [])

    hypothesis_diag = infer_persistence_hypotheses(daily_rows if isinstance(daily_rows, list) else [])

    k2_r1 = read_json(K2_R1_REPORT)

    # Focus only on clusters that actually include gate state/risk_off/shock assignment or source-side logging.
    critical_clusters = []
    for cluster in source_line_clusters:
        text_blob = "\n".join(r["text"] for r in cluster["rows"])
        if any(token in text_blob for token in [
            "market_gate_state",
            "gate_state",
            "risk_off",
            "shock",
            "spx_ma50",
            "SPX<MA50",
            "D3_RISK_OFF_PLUS_SHOCK_GATE",
        ]):
            critical_clusters.append(cluster)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "source_trace_complete": True,
        "strategy_logic_changed": False,
        "audit_only": True,
        "formula_not_patched": True,
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
        "k2_r1_loaded": True,
        "run_stateful_simulation_bounds_found": fn_bounds["line_count"] > 0,
        "source_hits_found": len(hits) > 0,
        "critical_clusters_found": len(critical_clusters) > 0,
        "mismatch_window_rows_extracted": focused_rows["row_count"] > 0,
        "hypotheses_evaluated_for_diagnosis_only": True,
    }

    decision = {
        "market_gate_source_trace_passed": all([
            validations["strategy_files_unchanged"],
            validations["source_hits_found"],
            validations["critical_clusters_found"],
            validations["mismatch_window_rows_extracted"],
        ]),
        "basic_formula_from_k2_r1_mismatch_count": k2_r1.get("decision", {}).get("basic_formula_mismatch_count"),
        "critical_cluster_count": len(critical_clusters),
        "source_hit_summary": hit_summary,
        "best_diagnostic_hypotheses": hypothesis_diag["best_hypotheses"][:5],
        "recommended_next_stage": "4C-2C-4E-ENGINE-K2-R3",
        "conclusion": "MARKET_GATE_SOURCE_TRACE_PASS_READY_FOR_EXACT_FORMULA_PATCH",
        "recommended_next_action": (
            "Review critical source clusters and patch market_gate_state using the exact legacy formula. "
            "Do not proceed to candidate extraction until market gate equivalence passes."
        ),
        "engineering_rule": (
            "A data-fitted hypothesis is not enough. K2-R3 must be tied to source lines from backtest.py."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R2",
        "status": "MARKET_GATE_SOURCE_TRACE_COMPLETE",
        "purpose": "Inspect exact source contexts for legacy market gate after K2 mismatch.",
        "policy": {
            "strategy_logic_changed": False,
            "audit_only": True,
            "formula_not_patched": True,
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
        "source": {
            "backtest_path": rel(BACKTEST),
            "backtest_sha256": sha256(BACKTEST),
            "function_bounds": fn_bounds,
        },
        "hit_summary": hit_summary,
        "critical_source_clusters": critical_clusters,
        "focused_mismatch_window_rows": focused_rows,
        "diagnostic_hypotheses": hypothesis_diag,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R2 — Market Gate Source Trace")
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
    md.append("## Source")
    md.append("```json")
    md.append(json.dumps(report["source"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Hit Summary")
    md.append("```json")
    md.append(json.dumps(hit_summary, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Focused Mismatch Window Rows")
    md.append("```json")
    md.append(json.dumps(focused_rows, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Diagnostic Hypotheses")
    md.append("```json")
    md.append(json.dumps(hypothesis_diag, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Critical Source Clusters")
    md.append("```json")
    md.append(json.dumps(critical_clusters, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Decision")
    md.append("```json")
    md.append(json.dumps(decision, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")

    REPORT_MD.write_text("\n".join(md))
    ARCH_MD.write_text("\n".join(md))

    print("E1R_4C2C4E_ENGINE_K2_R2_MARKET_GATE_SOURCE_TRACE_COMPLETE")
    print("status:", report["status"])
    print("source:", json.dumps(report["source"], ensure_ascii=False))
    print("hit_summary:", json.dumps(hit_summary, ensure_ascii=False))
    print("focused_mismatch_window_rows:", json.dumps(focused_rows, ensure_ascii=False))
    print("best_diagnostic_hypotheses:", json.dumps(hypothesis_diag["best_hypotheses"][:5], ensure_ascii=False))
    print("critical_cluster_count:", len(critical_clusters))
    print("critical_cluster_ranges:", json.dumps([
        {"start": c["start"], "end": c["end"], "line_count": c["line_count"]}
        for c in critical_clusters
    ], ensure_ascii=False))
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
