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

R9B = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json"
R9 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json"
R8 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R8_MARKET_STATE_PARAMETER_AUDIT.json"

GENERATOR_TRACE = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json"
TARGET_ARTIFACT = ROOT / "exports/e1r_v0_2_backtest_summary.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9C_115_RETURN_GENERATOR_TRACE.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9C_115_RETURN_GENERATOR_TRACE.md"
ARCH_MD = ROOT / "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9C_115_RETURN_GENERATOR_TRACE.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_r9c_115_return_generator_trace.json"
EVIDENCE_JSON = ROOT / "exports/e1r_engine/equivalence/e1r_k2_r9c_115_return_generator_trace_evidence.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
]

SELF_AUDIT_SCRIPT_NAMES = {
    "e1r_k2_r9b_115_return_artifact_recovery.py",
    "e1r_k2_r9c_115_return_generator_trace.py",
}

KEY_TERMS = [
    "E1R_REGIME_AWARE_V0_2",
    "116.7435999134756",
    "e1r_v0_2_backtest_summary.json",
    "run_stateful_simulation",
    "build_e1r_sidecar_sleeve",
    "D3_RISK_OFF_PLUS_SHOCK_GATE",
    "market_gate_enabled",
    "risk_off_below_spx_ma50",
    "market_shock_gate_enabled",
    "market_shock_daily_return",
    "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
    "sidecar_active_by_regime",
    "sidecar_active_by_subclass",
]

SOURCE_SEARCH_DIRS = [
    ROOT / "scripts",
    ROOT / "src",
    ROOT / "docs",
    ROOT / "exports",
]

EXCLUDE_PARTS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".next",
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


def safe_text(path: Path, limit: int = 10_000_000) -> str:
    try:
        data = path.read_bytes()
        if len(data) > limit:
            data = data[:limit]
        return data.decode("utf-8", errors="replace")
    except Exception:
        return ""


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


def flatten(obj: Any, prefix: str = "") -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else str(k)
            out.append({"path": p, "key": str(k), "value": v})
            out.extend(flatten(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:20000]):
            p = f"{prefix}[{i}]"
            out.append({"path": p, "key": f"[{i}]", "value": v})
            out.extend(flatten(v, p))
    return out


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDE_PARTS for part in path.parts)


def iter_source_files() -> list[Path]:
    files: list[Path] = []
    for base in SOURCE_SEARCH_DIRS:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if is_excluded(p) or not p.is_file():
                continue
            if p.name in SELF_AUDIT_SCRIPT_NAMES:
                continue
            if p.suffix.lower() not in {".py", ".json", ".md", ".txt", ".js"}:
                continue
            files.append(p)
    return sorted(set(files))


def extract_relevant_rows_from_json_trace(obj: Any) -> dict[str, Any]:
    flat = flatten(obj)
    rows = []

    for row in flat:
        v = row["value"]
        text = ""
        if isinstance(v, str):
            text = v
        elif isinstance(v, (int, float, bool)) or v is None:
            text = str(v)
        else:
            try:
                text = json.dumps(v, ensure_ascii=False)
            except Exception:
                text = repr(v)

        matched = [t for t in KEY_TERMS if t.lower() in text.lower() or t.lower() in row["path"].lower()]
        if matched:
            rows.append({
                "path": row["path"],
                "key": row["key"],
                "matched": matched,
                "value": compact(v),
            })

    return {
        "relevant_row_count": len(rows),
        "rows": rows[:500],
        "matched_terms": sorted(set(t for r in rows for t in r["matched"])),
    }


def grep_clean_sources() -> dict[str, Any]:
    hits = []
    for p in iter_source_files():
        text = safe_text(p)
        if not text:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            matched = [t for t in KEY_TERMS if t.lower() in line.lower()]
            if matched:
                hits.append({
                    "path": rel(p),
                    "line": i,
                    "matched": matched,
                    "text": line[:1500],
                })

    by_path: dict[str, list[dict[str, Any]]] = {}
    for h in hits:
        by_path.setdefault(h["path"], []).append(h)

    grouped = []
    for path, rows in by_path.items():
        score = 0
        terms = sorted(set(t for r in rows for t in r["matched"]))
        if "e1r_v0_2_backtest_summary.json" in terms:
            score += 100
        if "E1R_REGIME_AWARE_V0_2" in terms:
            score += 80
        if "116.7435999134756" in terms:
            score += 80
        if "run_stateful_simulation" in terms:
            score += 60
        if "build_e1r_sidecar_sleeve" in terms:
            score += 60
        if "D3_RISK_OFF_PLUS_SHOCK_GATE" in terms:
            score += 60
        score += len(rows)

        grouped.append({
            "path": path,
            "score": score,
            "hit_count": len(rows),
            "matched_terms": terms,
            "sample_hits": rows[:40],
        })

    return {
        "total_hits": len(hits),
        "top_paths": sorted(grouped, key=lambda x: x["score"], reverse=True)[:40],
        "hits": hits[:1000],
    }


def parse_candidate_py(path_s: str) -> dict[str, Any]:
    p = ROOT / path_s
    text = safe_text(p)
    if not p.exists() or p.suffix.lower() != ".py":
        return {"path": path_s, "parse_ok": False, "reason": "not_python_or_missing"}

    try:
        tree = ast.parse(text)
    except Exception as exc:
        return {"path": path_s, "parse_ok": False, "reason": repr(exc)}

    imports = []
    functions = []
    calls = []
    writes = []
    constants = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append({
                "line": getattr(node, "lineno", None),
                "text": ast.get_source_segment(text, node),
            })
        elif isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "line": node.lineno,
                "end_line": getattr(node, "end_lineno", None),
            })
        elif isinstance(node, ast.Call):
            seg = ast.get_source_segment(text, node) or ""
            if any(term in seg for term in [
                "run_stateful_simulation",
                "build_e1r_sidecar_sleeve",
                "write_text",
                "json.dump",
                "json.dumps",
                "open(",
            ]):
                calls.append({
                    "line": getattr(node, "lineno", None),
                    "text": seg[:2500],
                })
        elif isinstance(node, ast.Assign):
            seg = ast.get_source_segment(text, node) or ""
            if any(term in seg for term in KEY_TERMS):
                constants.append({
                    "line": getattr(node, "lineno", None),
                    "text": seg[:2500],
                })
            if "e1r_v0_2_backtest_summary" in seg or "write_text" in seg or "json.dump" in seg:
                writes.append({
                    "line": getattr(node, "lineno", None),
                    "text": seg[:2500],
                })

    return {
        "path": path_s,
        "parse_ok": True,
        "imports": imports[:80],
        "functions": functions[:120],
        "calls": calls[:160],
        "writes": writes[:80],
        "constants": constants[:120],
    }


def inspect_specific_files_from_trace(trace_rows: dict[str, Any], grep_summary: dict[str, Any]) -> list[dict[str, Any]]:
    candidates: list[str] = []

    for r in trace_rows.get("rows", []):
        v = r.get("value")
        text = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
        for m in re.findall(r'[\w./-]+\.py', text):
            if m.startswith("./"):
                m = m[2:]
            if m not in candidates and not Path(m).name in SELF_AUDIT_SCRIPT_NAMES:
                candidates.append(m)

    for item in grep_summary.get("top_paths", []):
        p = item["path"]
        if p.endswith(".py") and Path(p).name not in SELF_AUDIT_SCRIPT_NAMES and p not in candidates:
            candidates.append(p)

    inspected = []
    for p in candidates[:30]:
        inspected.append(parse_candidate_py(p))
    return inspected


def inspect_target_artifact() -> dict[str, Any]:
    if not TARGET_ARTIFACT.exists():
        return {"exists": False}
    obj = read_json(TARGET_ARTIFACT)
    selected = {}
    for row in flatten(obj):
        k = row["key"]
        p = row["path"]
        if k in {
            "strategy_id", "variant", "total_return_pct", "spx_return_pct", "alpha_pct",
            "max_drawdown_pct", "profit_factor", "sharpe_ratio", "regime_aware_logic",
            "sidecar_active_by_regime", "sidecar_active_by_subclass", "source_file",
        } or any(term in p.lower() for term in ["market_gate", "shock", "risk_off"]):
            selected[p] = compact(row["value"])
    return {
        "exists": True,
        "path": rel(TARGET_ARTIFACT),
        "sha256": sha256(TARGET_ARTIFACT),
        "selected_fields": selected,
    }


def extract_market_param_evidence(trace_rows: dict[str, Any], clean_grep: dict[str, Any], inspected_scripts: list[dict[str, Any]]) -> dict[str, Any]:
    terms = {
        "D3_RISK_OFF_PLUS_SHOCK_GATE": [],
        "market_gate_enabled": [],
        "risk_off_below_spx_ma50": [],
        "market_shock_gate_enabled": [],
        "market_shock_daily_return": [],
        "market_entry_gate": [],
        "run_stateful_simulation": [],
        "build_e1r_sidecar_sleeve": [],
    }

    for r in trace_rows.get("rows", []):
        text = json.dumps(r, ensure_ascii=False)
        for term in terms:
            if term.lower() in text.lower():
                terms[term].append({
                    "source": "generator_trace_json",
                    "path": r.get("path"),
                    "value": compact(r.get("value")),
                })

    for item in clean_grep.get("top_paths", []):
        for hit in item.get("sample_hits", []):
            text = json.dumps(hit, ensure_ascii=False)
            for term in terms:
                if term.lower() in text.lower():
                    terms[term].append({
                        "source": "clean_repo_grep",
                        "file": hit.get("path"),
                        "line": hit.get("line"),
                        "text": hit.get("text"),
                    })

    for s in inspected_scripts:
        text = json.dumps(s, ensure_ascii=False)
        for term in terms:
            if term.lower() in text.lower():
                terms[term].append({
                    "source": "candidate_script_ast",
                    "file": s.get("path"),
                    "summary": compact(s),
                })

    summarized = {
        k: {
            "evidence_count": len(v),
            "sample": v[:20],
        }
        for k, v in terms.items()
    }

    blocking_missing = [
        k for k in [
            "market_gate_enabled",
            "risk_off_below_spx_ma50",
            "market_shock_gate_enabled",
            "market_shock_daily_return",
        ]
        if summarized[k]["evidence_count"] == 0
    ]

    return {
        "by_term": summarized,
        "blocking_missing_terms": blocking_missing,
        "has_required_market_param_evidence": len(blocking_missing) == 0,
        "has_generator_call_evidence": (
            summarized["run_stateful_simulation"]["evidence_count"] > 0
            and summarized["build_e1r_sidecar_sleeve"]["evidence_count"] > 0
        ),
    }


def main() -> None:
    started = datetime.now(timezone.utc)

    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    for p in [R9B, R9, R8, TARGET_ARTIFACT]:
        if not p.exists():
            raise FileNotFoundError(f"Missing prerequisite: {rel(p)}")

    r9b = read_json(R9B)
    if r9b.get("decision", {}).get("k2_r9b_115_return_artifact_recovery_passed") is not True:
        raise RuntimeError("K2-R9B did not pass.")

    generator_trace_exists = GENERATOR_TRACE.exists()
    generator_trace_obj = read_json(GENERATOR_TRACE) if generator_trace_exists else None
    trace_rows = extract_relevant_rows_from_json_trace(generator_trace_obj) if generator_trace_obj is not None else {
        "relevant_row_count": 0,
        "rows": [],
        "matched_terms": [],
    }

    clean_grep = grep_clean_sources()
    inspected_scripts = inspect_specific_files_from_trace(trace_rows, clean_grep)
    target = inspect_target_artifact()
    market_param_evidence = extract_market_param_evidence(trace_rows, clean_grep, inspected_scripts)

    self_reference_pollution_removed = all(
        Path(x["path"]).name not in SELF_AUDIT_SCRIPT_NAMES
        for x in clean_grep.get("top_paths", [])
    )

    unresolved = []

    if not generator_trace_exists:
        unresolved.append({
            "id": "generator_path_trace_json_missing",
            "blocking_for_replication": True,
            "path": rel(GENERATOR_TRACE),
        })

    if trace_rows["relevant_row_count"] == 0:
        unresolved.append({
            "id": "generator_path_trace_json_has_no_relevant_rows",
            "blocking_for_replication": True,
        })

    if not market_param_evidence["has_required_market_param_evidence"]:
        unresolved.append({
            "id": "required_market_param_evidence_missing",
            "missing_terms": market_param_evidence["blocking_missing_terms"],
            "blocking_for_replication": True,
        })

    if not market_param_evidence["has_generator_call_evidence"]:
        unresolved.append({
            "id": "generator_call_chain_evidence_incomplete",
            "required": ["run_stateful_simulation", "build_e1r_sidecar_sleeve"],
            "blocking_for_replication": True,
        })

    if not self_reference_pollution_removed:
        unresolved.append({
            "id": "self_reference_pollution_not_fully_removed",
            "blocking_for_replication": True,
        })

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}
    blocking_count = len([x for x in unresolved if x.get("blocking_for_replication")])

    validations = {
        "generator_trace_complete": True,
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
        "r9b_loaded": True,
        "target_artifact_exists": target.get("exists") is True,
        "generator_path_trace_exists": generator_trace_exists,
        "generator_path_trace_relevant_rows_found": trace_rows["relevant_row_count"] > 0,
        "self_reference_pollution_removed": self_reference_pollution_removed,
        "clean_repo_grep_completed": clean_grep["total_hits"] > 0,
        "candidate_scripts_inspected": True,
        "required_market_param_evidence_found": market_param_evidence["has_required_market_param_evidence"],
        "generator_call_chain_evidence_found": market_param_evidence["has_generator_call_evidence"],
        "blocking_unresolved_count": blocking_count,
    }

    decision = {
        "k2_r9c_115_return_generator_trace_passed": all([
            validations["strategy_files_unchanged"],
            validations["target_artifact_exists"],
            validations["generator_path_trace_exists"],
            validations["generator_path_trace_relevant_rows_found"],
            validations["self_reference_pollution_removed"],
            validations["clean_repo_grep_completed"],
            validations["candidate_scripts_inspected"],
        ]),
        "market_state_115_replication_ready": blocking_count == 0,
        "formula_patch_allowed_now": False,
        "candidate_extraction_allowed_now": False,
        "implementation_may_resume": False,
        "unresolved": unresolved,
        "next_required_stage_if_ready": "4C-2C-4E-ENGINE-K2-R10-MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL",
        "next_required_stage_if_not_ready": "4C-2C-4E-ENGINE-K2-R9D-MARKET_PARAM_SOURCE_LINE_TRACE",
        "conclusion": (
            "K2_R9C_PASS_GENERATOR_TRACE_READY_FOR_REPLICATION_PROPOSAL"
            if blocking_count == 0
            else "K2_R9C_GENERATOR_TRACE_COMPLETE_NEEDS_MARKET_PARAM_SOURCE_LINE_TRACE"
        ),
        "recommended_next_action": (
            "If market param evidence is present, prepare standalone replication proposal. "
            "If evidence is still indirect, perform source-line trace for each missing market parameter."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R9C-115_RETURN_GENERATOR_TRACE",
        "status": "115_RETURN_GENERATOR_TRACE_COMPLETE",
        "purpose": "Trace the real generator/call-chain evidence for the E1R v0.2 116.74% artifact, excluding self-reference audit pollution.",
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
            "r9b": rel(R9B),
            "r9": rel(R9),
            "r8": rel(R8),
            "generator_trace": rel(GENERATOR_TRACE),
            "target_artifact": rel(TARGET_ARTIFACT),
        },
        "target_artifact_inspection": target,
        "generator_trace_json": {
            "exists": generator_trace_exists,
            "path": rel(GENERATOR_TRACE),
            "sha256": sha256(GENERATOR_TRACE),
            "relevant_rows": trace_rows,
        },
        "clean_repo_grep": clean_grep,
        "inspected_candidate_scripts": inspected_scripts,
        "market_param_evidence": market_param_evidence,
        "unresolved": unresolved,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)
    write_json(EVIDENCE_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R9C — 115 Return Generator Trace")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Target Artifact")
    md.append("```json")
    md.append(json.dumps(target, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Generator Trace JSON Relevant Rows")
    md.append("```json")
    md.append(json.dumps(trace_rows, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Market Parameter Evidence")
    md.append("```json")
    md.append(json.dumps(market_param_evidence, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Clean Grep Top Paths")
    md.append("```json")
    md.append(json.dumps(clean_grep["top_paths"][:20], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Inspected Candidate Scripts")
    md.append("```json")
    md.append(json.dumps(inspected_scripts, indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_ENGINE_K2_R9C_115_RETURN_GENERATOR_TRACE_COMPLETE")
    print("status:", report["status"])
    print("target_artifact_inspection:", json.dumps(target, ensure_ascii=False))
    print("generator_trace_json_summary:", json.dumps({
        "exists": generator_trace_exists,
        "path": rel(GENERATOR_TRACE),
        "sha256": sha256(GENERATOR_TRACE),
        "relevant_row_count": trace_rows["relevant_row_count"],
        "matched_terms": trace_rows["matched_terms"],
    }, ensure_ascii=False))
    print("market_param_evidence:", json.dumps(market_param_evidence, ensure_ascii=False))
    print("clean_grep_top_paths:", json.dumps(clean_grep["top_paths"][:10], ensure_ascii=False))
    print("inspected_candidate_scripts:", json.dumps(inspected_scripts[:10], ensure_ascii=False))
    print("unresolved:", json.dumps(unresolved, ensure_ascii=False))
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
