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

TARGET_ARTIFACT = ROOT / "exports/e1r_v0_2_backtest_summary.json"
K2_R9 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json"
K2_R8 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R8_MARKET_STATE_PARAMETER_AUDIT.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md"
ARCH_MD = ROOT / "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_r9b_115_return_artifact_recovery.json"
EVIDENCE_JSON = ROOT / "exports/e1r_engine/equivalence/e1r_k2_r9b_115_return_artifact_recovery_evidence.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
]

SEARCH_DIRS = [
    ROOT / "scripts",
    ROOT / "src",
    ROOT / "docs",
    ROOT / "exports",
    ROOT / "data",
]

EXCLUDE_PARTS = {
    ".git",
    "node_modules",
    ".next",
    "__pycache__",
}

TARGET_RETURN = 116.7435999134756

NEEDLES = [
    "e1r_v0_2_backtest_summary",
    "E1R_REGIME_AWARE_V0_2",
    "E1R_REGIME_AWARE_V0_1",
    "UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
    "sidecar_active_by_regime",
    "D3_RISK_OFF_PLUS_SHOCK_GATE",
    "market_entry_gate",
    "market_gate_enabled",
    "risk_off_below_spx_ma50",
    "market_shock_gate_enabled",
    "market_shock_daily_return",
    "run_stateful_simulation",
    "e1r_sidecar",
    "e1r_sidecar_sleeve",
    "e1r_composer",
    "116.7435999134756",
    "116.74",
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


def safe_read_text(path: Path, limit: int = 8_000_000) -> str:
    try:
        data = path.read_bytes()
        if len(data) > limit:
            data = data[:limit]
        return data.decode("utf-8", errors="replace")
    except Exception:
        return ""


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDE_PARTS for part in path.parts)


def iter_files() -> list[Path]:
    out: list[Path] = []
    for base in SEARCH_DIRS:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if is_excluded(p) or not p.is_file():
                continue
            if p.suffix.lower() not in {".py", ".json", ".md", ".txt", ".csv", ".js"}:
                continue
            out.append(p)
    return sorted(set(out))


def grep_needles() -> list[dict[str, Any]]:
    hits = []
    for p in iter_files():
        text = safe_read_text(p)
        if not text:
            continue
        lines = text.splitlines()
        for i, line in enumerate(lines, start=1):
            line_l = line.lower()
            matched = [n for n in NEEDLES if n.lower() in line_l]
            if matched:
                hits.append({
                    "path": rel(p),
                    "line": i,
                    "matched": matched,
                    "text": line[:1200],
                })
    return hits


def score_hit(h: dict[str, Any]) -> int:
    score = 0
    path_l = h["path"].lower()
    text_l = h["text"].lower()
    matched = set(x.lower() for x in h["matched"])

    if "e1r_v0_2_backtest_summary" in matched:
        score += 100
    if "e1r_regime_aware_v0_2" in matched:
        score += 80
    if "116.7435999134756" in matched or "116.74" in matched:
        score += 70
    if "d3_risk_off_plus_shock_gate" in matched:
        score += 60
    if "market_entry_gate" in matched or "market_gate_enabled" in matched:
        score += 50
    if "run_stateful_simulation" in matched:
        score += 40
    if path_l.endswith(".py"):
        score += 30
    if "scripts/" in path_l:
        score += 20
    if "src/" in path_l:
        score += 15
    if "write_text" in text_l or "json.dump" in text_l or "open(" in text_l:
        score += 20

    return score


def group_hits(hits: list[dict[str, Any]]) -> dict[str, Any]:
    by_path: dict[str, list[dict[str, Any]]] = {}
    for h in hits:
        by_path.setdefault(h["path"], []).append(h)

    grouped = []
    for path, rows in by_path.items():
        grouped.append({
            "path": path,
            "score": sum(score_hit(x) for x in rows),
            "hit_count": len(rows),
            "matched_terms": sorted(set(t for r in rows for t in r["matched"])),
            "sample_hits": rows[:30],
        })

    return {
        "by_path": sorted(grouped, key=lambda x: x["score"], reverse=True),
        "all_hits_count": len(hits),
    }


def parse_py_file(path: Path) -> dict[str, Any]:
    text = safe_read_text(path)
    if not text:
        return {"path": rel(path), "parse_ok": False, "error": "empty"}
    try:
        tree = ast.parse(text)
    except Exception as exc:
        return {"path": rel(path), "parse_ok": False, "error": repr(exc)}

    imports = []
    functions = []
    calls = []
    assignments = []

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
            func = node.func
            name = None
            if isinstance(func, ast.Name):
                name = func.id
            elif isinstance(func, ast.Attribute):
                parts = []
                cur = func
                while isinstance(cur, ast.Attribute):
                    parts.append(cur.attr)
                    cur = cur.value
                if isinstance(cur, ast.Name):
                    parts.append(cur.id)
                name = ".".join(reversed(parts))
            if name and any(k in name for k in [
                "run_stateful_simulation",
                "run_sidecar",
                "compose",
                "write_text",
                "dump",
                "dumps",
                "open",
            ]):
                calls.append({
                    "line": getattr(node, "lineno", None),
                    "call": name,
                    "text": ast.get_source_segment(text, node),
                })
        elif isinstance(node, ast.Assign):
            src = ast.get_source_segment(text, node) or ""
            if any(n in src for n in NEEDLES):
                assignments.append({
                    "line": getattr(node, "lineno", None),
                    "text": src[:1500],
                })

    return {
        "path": rel(path),
        "parse_ok": True,
        "imports": imports[:80],
        "functions": functions[:80],
        "calls": calls[:120],
        "assignments": assignments[:80],
    }


def analyze_candidate_scripts(grouped: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = []
    for item in grouped["by_path"][:30]:
        path = ROOT / item["path"]
        if path.suffix.lower() != ".py":
            continue
        parsed = parse_py_file(path)
        candidates.append({
            "path": item["path"],
            "score": item["score"],
            "hit_count": item["hit_count"],
            "matched_terms": item["matched_terms"],
            "sample_hits": item["sample_hits"][:15],
            "ast_summary": parsed,
        })
    return candidates


def compact(v: Any, max_len: int = 1600) -> Any:
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


def flatten_json(obj: Any, prefix: str = "") -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else str(k)
            rows.append({"path": path, "key": str(k), "value": v})
            rows.extend(flatten_json(v, path))
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:5000]):
            path = f"{prefix}[{i}]"
            rows.append({"path": path, "key": f"[{i}]", "value": v})
            rows.extend(flatten_json(v, path))
    return rows


def inspect_target_artifact() -> dict[str, Any]:
    if not TARGET_ARTIFACT.exists():
        return {"exists": False}

    obj = read_json(TARGET_ARTIFACT)
    flat = flatten_json(obj)
    selected = {}

    for row in flat:
        p = row["path"]
        k = row["key"]
        if k in {
            "strategy_id", "variant", "total_return_pct", "spx_return_pct", "alpha_pct",
            "max_drawdown_pct", "profit_factor", "sharpe_ratio", "regime_aware_logic",
            "sidecar_active_by_regime", "sidecar_active_by_subclass", "source_file",
            "simulation_start_date", "simulation_end_date", "simulation_days",
            "trades", "exposure_pct",
        } or any(term in p.lower() for term in ["market_gate", "market_state", "shock", "risk_off", "regime_aware_logic"]):
            selected[p] = compact(row["value"])

    return {
        "exists": True,
        "path": rel(TARGET_ARTIFACT),
        "sha256": sha256(TARGET_ARTIFACT),
        "selected_fields": selected,
    }


def inspect_known_source_files() -> dict[str, Any]:
    known = [
        ROOT / "src/engine/backtest.py",
        ROOT / "src/engine/e1r_composer.py",
        ROOT / "src/engine/e1r_sidecar_sleeve.py",
        ROOT / "run_backtest.py",
    ]

    out = {}
    for p in known:
        if not p.exists():
            out[rel(p)] = {"exists": False}
            continue
        text = safe_read_text(p)
        hits = []
        for i, line in enumerate(text.splitlines(), start=1):
            if any(n.lower() in line.lower() for n in NEEDLES):
                hits.append({
                    "line": i,
                    "matched": [n for n in NEEDLES if n.lower() in line.lower()],
                    "text": line[:1200],
                })
        out[rel(p)] = {
            "exists": True,
            "sha256": sha256(p),
            "hits": hits[:200],
            "hit_count": len(hits),
        }
    return out


def derive_evidence_status(grouped: dict[str, Any], candidate_scripts: list[dict[str, Any]], target: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    unresolved = []

    generator_candidates = [
        c for c in candidate_scripts
        if any("e1r_v0_2_backtest_summary" in t for t in c.get("matched_terms", []))
    ]

    has_generator_script = len(generator_candidates) > 0
    has_target_artifact = bool(target.get("exists"))
    has_return = False
    if has_target_artifact:
        total_ret = target.get("selected_fields", {}).get("total_return_pct")
        try:
            has_return = abs(float(total_ret) - TARGET_RETURN) < 0.01
        except Exception:
            has_return = False

    # Evidence from the artifact itself.
    selected = target.get("selected_fields", {})
    artifact_has_market_gate = any("market_gate" in k.lower() for k in selected)
    artifact_has_regime_logic = "regime_aware_logic" in selected
    artifact_has_sidecar = any("sidecar_active" in k.lower() for k in selected)

    if not has_generator_script:
        unresolved.append({
            "id": "generator_script_for_e1r_v0_2_summary_not_found",
            "blocking_for_replication": True,
        })

    if not artifact_has_market_gate:
        unresolved.append({
            "id": "target_artifact_missing_market_gate_parameters",
            "blocking_for_replication": True,
        })

    if not artifact_has_regime_logic:
        unresolved.append({
            "id": "target_artifact_missing_regime_aware_logic",
            "blocking_for_replication": True,
        })

    status = {
        "target_artifact_exists": has_target_artifact,
        "target_return_verified": has_return,
        "generator_script_candidates_found": has_generator_script,
        "generator_script_candidates": [
            {
                "path": c["path"],
                "score": c["score"],
                "matched_terms": c["matched_terms"],
                "sample_hits": c["sample_hits"][:10],
            }
            for c in generator_candidates[:10]
        ],
        "target_artifact_has_market_gate_parameters": artifact_has_market_gate,
        "target_artifact_has_regime_aware_logic": artifact_has_regime_logic,
        "target_artifact_has_sidecar_evidence": artifact_has_sidecar,
    }

    return status, unresolved


def main() -> None:
    started = datetime.now(timezone.utc)

    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    for p in [K2_R9, K2_R8]:
        if not p.exists():
            raise FileNotFoundError(f"Missing prerequisite: {rel(p)}")

    k2_r9 = read_json(K2_R9)
    if k2_r9.get("decision", {}).get("full_115_artifact_verified") is not True:
        raise RuntimeError("K2-R9 did not verify full 115 artifact.")

    target = inspect_target_artifact()
    hits = grep_needles()
    grouped = group_hits(hits)
    candidate_scripts = analyze_candidate_scripts(grouped)
    known_source_files = inspect_known_source_files()

    evidence_status, unresolved = derive_evidence_status(grouped, candidate_scripts, target)

    # Add unresolved from K2-R9 that remains not solved by recovery.
    prior_unresolved = k2_r9.get("unresolved", [])
    if evidence_status["target_artifact_has_market_gate_parameters"]:
        prior_unresolved_filtered = [
            x for x in prior_unresolved
            if x.get("field") not in {
                "market_entry_gate",
                "market_gate_enabled",
                "risk_off_below_spx_ma50",
                "market_shock_gate_enabled",
                "market_shock_daily_return",
            }
        ]
    else:
        prior_unresolved_filtered = prior_unresolved

    unresolved.extend(prior_unresolved_filtered)

    # Deduplicate.
    seen = set()
    dedup = []
    for x in unresolved:
        key = (x.get("id"), x.get("field"))
        if key in seen:
            continue
        seen.add(key)
        dedup.append(x)
    unresolved = dedup

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    blocking_count = len([x for x in unresolved if x.get("blocking_for_replication")])

    validations = {
        "artifact_recovery_complete": True,
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
        "k2_r9_loaded": True,
        "target_artifact_exists": evidence_status["target_artifact_exists"],
        "target_return_verified": evidence_status["target_return_verified"],
        "repository_grep_completed": len(hits) > 0,
        "candidate_script_analysis_completed": True,
        "known_source_files_inspected": True,
        "generator_script_candidates_found": evidence_status["generator_script_candidates_found"],
        "target_artifact_has_market_gate_parameters": evidence_status["target_artifact_has_market_gate_parameters"],
        "target_artifact_has_regime_aware_logic": evidence_status["target_artifact_has_regime_aware_logic"],
        "target_artifact_has_sidecar_evidence": evidence_status["target_artifact_has_sidecar_evidence"],
        "blocking_unresolved_count": blocking_count,
    }

    decision = {
        "k2_r9b_115_return_artifact_recovery_passed": all([
            validations["strategy_files_unchanged"],
            validations["target_artifact_exists"],
            validations["target_return_verified"],
            validations["repository_grep_completed"],
            validations["candidate_script_analysis_completed"],
            validations["known_source_files_inspected"],
        ]),
        "market_state_115_replication_ready": blocking_count == 0,
        "formula_patch_allowed_now": False,
        "candidate_extraction_allowed_now": False,
        "implementation_may_resume": False,
        "unresolved": unresolved,
        "next_required_stage_if_ready": "4C-2C-4E-ENGINE-K2-R10-MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL",
        "next_required_stage_if_not_ready": "4C-2C-4E-ENGINE-K2-R9C-115_RETURN_GENERATOR_TRACE",
        "conclusion": (
            "K2_R9B_PASS_ARTIFACT_RECOVERY_READY_FOR_REPLICATION_PROPOSAL"
            if blocking_count == 0
            else "K2_R9B_RECOVERY_COMPLETE_NEEDS_GENERATOR_TRACE_OR_PARAM_EVIDENCE"
        ),
        "recommended_next_action": (
            "If blocking unresolved remains, trace the generator script/call chain more narrowly and inspect the source lines "
            "that produced E1R_REGIME_AWARE_V0_2 and regime_aware_logic. Do not patch."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R9B-115_RETURN_ARTIFACT_RECOVERY",
        "status": "115_RETURN_ARTIFACT_RECOVERY_COMPLETE",
        "purpose": "Recover the generation chain and parameter evidence for exports/e1r_v0_2_backtest_summary.json without changing strategy logic.",
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
            "k2_r9": rel(K2_R9),
            "k2_r8": rel(K2_R8),
            "target_artifact": rel(TARGET_ARTIFACT),
            "search_dirs": [rel(x) for x in SEARCH_DIRS],
        },
        "target_artifact_inspection": target,
        "evidence_status": evidence_status,
        "grep_summary": {
            "total_hits": len(hits),
            "top_paths": grouped["by_path"][:20],
        },
        "candidate_scripts": candidate_scripts[:20],
        "known_source_files": known_source_files,
        "unresolved": unresolved,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)
    write_json(EVIDENCE_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R9B — 115 Return Artifact Recovery")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Target Artifact Inspection")
    md.append("```json")
    md.append(json.dumps(target, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Evidence Status")
    md.append("```json")
    md.append(json.dumps(evidence_status, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Top Grep Paths")
    md.append("```json")
    md.append(json.dumps(grouped["by_path"][:20], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Candidate Scripts")
    md.append("```json")
    md.append(json.dumps(candidate_scripts[:20], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Known Source Files")
    md.append("```json")
    md.append(json.dumps(known_source_files, indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_ENGINE_K2_R9B_115_RETURN_ARTIFACT_RECOVERY_COMPLETE")
    print("status:", report["status"])
    print("target_artifact_inspection:", json.dumps(target, ensure_ascii=False))
    print("evidence_status:", json.dumps(evidence_status, ensure_ascii=False))
    print("top_grep_paths:", json.dumps(grouped["by_path"][:10], ensure_ascii=False))
    print("candidate_scripts:", json.dumps(candidate_scripts[:10], ensure_ascii=False))
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
