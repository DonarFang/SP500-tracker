#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import hashlib
import re
from datetime import datetime, timezone
from typing import Any
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

D_REPORT = ROOT / "docs/research/E1R_4C2C4E_D_CONTINUOUS_STATEFUL_ADAPTER_DESIGN.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.md"

BACKTEST_PATH = ROOT / "src/engine/backtest.py"
SIDECAR_PATH = ROOT / "src/engine/e1r_sidecar_sleeve.py"
COMPOSER_PATH = ROOT / "src/engine/e1r_composer.py"

FROZEN_STRATEGY_FILES = [
    BACKTEST_PATH,
    SIDECAR_PATH,
    COMPOSER_PATH,
]

SEARCH_ROOTS = [
    ROOT / "src",
    ROOT / "scripts",
    ROOT / "tests",
]

UPTREND_TERMS = [
    "UPTREND",
    "e1r_uptrend_execution_enabled",
    "leader_score",
    "Leader",
    "leader",
    "rank",
    "candidate",
    "BUY",
    "ADD",
    "HOLD",
    "REDUCE",
    "EXIT",
    "max_positions",
    "entry_top_n",
    "buy_size",
    "add_size",
    "reduce_size",
    "sell_size",
    "market_gate",
    "gate_allowed",
    "qualified_entry",
    "relative_stop",
    "min_holding_days",
    "ls60_exit_mode",
]

INVALID_ARTIFACTS = [
    "exports/e1r_unified_5y_full_account_v1_result.json",
    "exports/e1r_unified_5y_dashboard_research_bundle.json",
    "exports/e1r_combined_5y_original_max3_result.json",
    "exports/e1r_combined_5y_original_max3_equity_curve.json",
    "exports/e1r_combined_5y_original_max3_summary.json",
]

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))

def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def read_text(path: Path) -> str:
    return path.read_text(errors="replace")

def read_json(path: Path) -> Any:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def py_files() -> list[Path]:
    files = []
    for root in SEARCH_ROOTS:
        if root.exists():
            files.extend(sorted(root.rglob("*.py")))
    return files

def line_window(lines: list[str], line_no: int, before: int = 8, after: int = 12) -> list[dict[str, Any]]:
    start = max(1, line_no - before)
    end = min(len(lines), line_no + after)
    return [{"line": i, "text": lines[i - 1][:280]} for i in range(start, end + 1)]

def get_function_source(path: Path, function_name: str) -> dict[str, Any]:
    text = read_text(path)
    lines = text.splitlines()
    tree = ast.parse(text)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            start = node.lineno
            end = getattr(node, "end_lineno", start)
            return {
                "path": rel(path),
                "function": function_name,
                "start_line": start,
                "end_line": end,
                "line_count": end - start + 1,
                "source": "\n".join(lines[start - 1:end]),
                "lines": lines,
            }

    raise RuntimeError(f"{function_name} not found in {path}")

def keyword_hits_in_file(path: Path, keywords: list[str], max_hits_each: int = 80) -> dict[str, list[dict[str, Any]]]:
    text = read_text(path)
    lines = text.splitlines()
    out = {}

    for kw in keywords:
        hits = []
        for i, line in enumerate(lines, start=1):
            if kw in line:
                hits.append({
                    "line": i,
                    "text": line.strip()[:280],
                    "context": line_window(lines, i, 4, 8),
                })
        out[kw] = hits[:max_hits_each]

    return out

def keyword_hits_repo(keywords: list[str], max_hits_each: int = 120) -> dict[str, list[dict[str, Any]]]:
    out = {kw: [] for kw in keywords}

    for path in py_files():
        text = read_text(path)
        lines = text.splitlines()

        for kw in keywords:
            if kw not in text:
                continue
            for i, line in enumerate(lines, start=1):
                if kw in line and len(out[kw]) < max_hits_each:
                    out[kw].append({
                        "path": rel(path),
                        "line": i,
                        "text": line.strip()[:280],
                    })

    return out

def call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = call_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""

def literal_str(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None

def audit_run_stateful_uptrend_logic() -> dict[str, Any]:
    fn = get_function_source(BACKTEST_PATH, "run_stateful_simulation")
    source = fn["source"]
    lines = fn["lines"]
    start_line = fn["start_line"]
    function_lines = source.splitlines()

    keyword_hits = []
    for idx, line in enumerate(function_lines, start=start_line):
        if any(term in line for term in UPTREND_TERMS):
            keyword_hits.append({
                "line": idx,
                "text": line.strip()[:300],
                "context": line_window(lines, idx, 5, 12),
            })

    buy_contexts = []
    action_contexts = []
    candidate_contexts = []
    exit_contexts = []
    reduce_contexts = []
    add_contexts = []

    for idx, line in enumerate(function_lines, start=start_line):
        normalized = line.strip()
        upper = normalized.upper()

        if "BUY" in upper or "buy_size" in normalized or "action" in normalized and "BUY" in upper:
            buy_contexts.append({"line": idx, "text": normalized[:300], "context": line_window(lines, idx, 8, 14)})

        if "ADD" in upper or "add_size" in normalized:
            add_contexts.append({"line": idx, "text": normalized[:300], "context": line_window(lines, idx, 8, 14)})

        if "REDUCE" in upper or "reduce_size" in normalized:
            reduce_contexts.append({"line": idx, "text": normalized[:300], "context": line_window(lines, idx, 8, 14)})

        if "EXIT" in upper or "sell_size" in normalized or "ls60_exit_mode" in normalized:
            exit_contexts.append({"line": idx, "text": normalized[:300], "context": line_window(lines, idx, 8, 14)})

        if any(x in normalized for x in ["candidate", "ranked", "leader_score", "score", "entry_top_n", "max_positions"]):
            candidate_contexts.append({"line": idx, "text": normalized[:300], "context": line_window(lines, idx, 6, 10)})

        if any(x in upper for x in ["BUY", "ADD", "REDUCE", "EXIT", "HOLD"]):
            action_contexts.append({"line": idx, "text": normalized[:300], "context": line_window(lines, idx, 6, 10)})

    static_evidence = {
        "contains_UPTREND": "UPTREND" in source,
        "contains_e1r_uptrend_execution_enabled": "e1r_uptrend_execution_enabled" in source,
        "contains_candidate_terms": any(x in source for x in ["candidate", "ranked", "entry_top_n", "leader_score"]),
        "contains_buy_logic": "BUY" in source or "buy_size" in source,
        "contains_add_logic": "ADD" in source or "add_size" in source,
        "contains_reduce_logic": "REDUCE" in source or "reduce_size" in source,
        "contains_exit_logic": "EXIT" in source or "sell_size" in source or "ls60_exit_mode" in source,
        "contains_position_state": "positions" in source and "cash" in source,
        "contains_market_gate": "market_gate" in source or "gate_allowed" in source,
        "contains_max_positions": "max_positions" in source,
    }

    internal_source_located = all([
        static_evidence["contains_candidate_terms"],
        static_evidence["contains_buy_logic"],
        static_evidence["contains_exit_logic"],
        static_evidence["contains_position_state"],
        static_evidence["contains_max_positions"],
    ])

    return {
        "path": fn["path"],
        "function": fn["function"],
        "start_line": fn["start_line"],
        "end_line": fn["end_line"],
        "line_count": fn["line_count"],
        "static_evidence": static_evidence,
        "internal_uptrend_source_logic_located": internal_source_located,
        "keyword_hits_count": len(keyword_hits),
        "keyword_hits_sample": keyword_hits[:80],
        "candidate_contexts_sample": candidate_contexts[:60],
        "buy_contexts_sample": buy_contexts[:40],
        "add_contexts_sample": add_contexts[:30],
        "reduce_contexts_sample": reduce_contexts[:30],
        "exit_contexts_sample": exit_contexts[:40],
        "action_contexts_sample": action_contexts[:80],
    }

def function_index() -> list[dict[str, Any]]:
    out = []

    for path in py_files():
        try:
            text = read_text(path)
            tree = ast.parse(text)
        except Exception:
            continue

        lines = text.splitlines()

        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue

            start = getattr(node, "lineno", None)
            end = getattr(node, "end_lineno", None)
            source = "\n".join(lines[start - 1:end]) if start and end else ""
            name_lower = node.name.lower()

            relevance_score = 0
            score_reasons = []

            rules = [
                ("leader", "leader" in name_lower or "leader_score" in source),
                ("rank", "rank" in name_lower or "rank" in source.lower()),
                ("candidate", "candidate" in name_lower or "candidate" in source.lower()),
                ("buy", "buy" in name_lower or "BUY" in source or "buy_size" in source),
                ("exit", "exit" in name_lower or "EXIT" in source),
                ("reduce", "reduce" in name_lower or "REDUCE" in source),
                ("market_gate", "market_gate" in name_lower or "market_gate" in source or "gate_allowed" in source),
                ("positions", "positions" in source and "cash" in source),
                ("regime", "regime" in name_lower or "regime" in source),
            ]

            for reason, ok in rules:
                if ok:
                    relevance_score += 1
                    score_reasons.append(reason)

            if relevance_score <= 0:
                continue

            out.append({
                "path": rel(path),
                "name": node.name,
                "start_line": start,
                "end_line": end,
                "line_count": end - start + 1 if start and end else None,
                "args": [a.arg for a in node.args.args],
                "relevance_score": relevance_score,
                "score_reasons": score_reasons,
                "contains_buy": "BUY" in source or "buy_size" in source,
                "contains_add": "ADD" in source or "add_size" in source,
                "contains_reduce": "REDUCE" in source or "reduce_size" in source,
                "contains_exit": "EXIT" in source or "sell_size" in source,
                "contains_candidate": "candidate" in source.lower(),
                "contains_leader_score": "leader_score" in source,
                "contains_positions": "positions" in source,
                "contains_cash": "cash" in source,
                "contains_market_gate": "market_gate" in source or "gate_allowed" in source,
                "contains_regime": "regime" in source,
            })

    return sorted(out, key=lambda x: (-x["relevance_score"], x["path"], x["start_line"] or 0))

def locate_external_provider_candidates(functions: list[dict[str, Any]]) -> dict[str, Any]:
    external = [
        f for f in functions
        if not (f["path"] == "src/engine/backtest.py" and f["name"] == "run_stateful_simulation")
    ]

    likely_candidate_providers = [
        f for f in external
        if (
            f["contains_candidate"]
            or f["contains_leader_score"]
            or "rank" in f["score_reasons"]
            or "leader" in f["score_reasons"]
        )
    ]

    likely_order_providers = [
        f for f in external
        if (
            f["contains_buy"]
            or f["contains_add"]
            or f["contains_reduce"]
            or f["contains_exit"]
        )
    ]

    likely_stateful_providers = [
        f for f in external
        if f["contains_positions"] and f["contains_cash"]
    ]

    direct_provider_candidates = [
        f for f in external
        if (
            f["contains_candidate"]
            and f["contains_buy"]
            and f["contains_exit"]
            and f["contains_positions"]
            and f["contains_cash"]
        )
    ]

    return {
        "likely_candidate_provider_functions": likely_candidate_providers[:80],
        "likely_order_provider_functions": likely_order_providers[:80],
        "likely_stateful_provider_functions": likely_stateful_providers[:80],
        "direct_standalone_uptrend_provider_candidates": direct_provider_candidates[:40],
        "direct_standalone_uptrend_provider_count": len(direct_provider_candidates),
    }

def audit_action_dict_shapes() -> dict[str, Any]:
    fn = get_function_source(BACKTEST_PATH, "run_stateful_simulation")
    source = fn["source"]
    start_line = fn["start_line"]

    tree = ast.parse(source)
    actions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            keys = []
            literals = {}
            for k, v in zip(node.keys, node.values):
                key = literal_str(k)
                if key:
                    keys.append(key)
                    try:
                        literals[key] = ast.literal_eval(v)
                    except Exception:
                        literals[key] = None

            key_set = set(keys)
            if key_set.intersection({"action", "symbol", "date", "reason", "shares", "qty", "quantity", "position", "branch"}):
                line_no = start_line + getattr(node, "lineno", 1) - 1
                actions.append({
                    "line": line_no,
                    "keys": keys,
                    "literal_action": literals.get("action"),
                    "literal_reason": literals.get("reason"),
                })

    action_counts = Counter(str(a.get("literal_action")) for a in actions if a.get("literal_action") is not None)

    return {
        "action_like_dict_count": len(actions),
        "literal_action_counts": dict(action_counts),
        "action_like_dicts_sample": actions[:120],
    }

def audit_repo_references() -> dict[str, Any]:
    hits = keyword_hits_repo([
        "run_stateful_simulation",
        "leader_score",
        "BUY",
        "EXIT",
        "REDUCE",
        "ADD",
        "market_gate",
        "entry_top_n",
        "max_positions",
        "e1r_uptrend_execution_enabled",
    ])

    return {
        "keyword_hits": hits,
    }

def load_prior_d() -> dict[str, Any]:
    if not D_REPORT.exists():
        return {
            "exists": False,
            "error": f"Missing {rel(D_REPORT)}",
        }

    d = read_json(D_REPORT)
    return {
        "exists": True,
        "status": d.get("status"),
        "decision": d.get("decision"),
        "branch_provider_status": {
            "uptrend": d.get("branch_providers", {}).get("UPTREND_signal_provider", {}).get("status"),
            "sideways": d.get("branch_providers", {}).get("SIDEWAYS_MA_CONFLICT_provider", {}).get("status"),
            "cash_defensive": d.get("branch_providers", {}).get("CASH_DEFENSIVE_provider", {}).get("status"),
        },
        "entrypoint_status": d.get("entrypoint_inspection", {}).get("entrypoint_status"),
    }

def derive_lock_decision(
    run_audit: dict[str, Any],
    external_candidates: dict[str, Any],
    action_shapes: dict[str, Any],
    prior_d: dict[str, Any],
) -> dict[str, Any]:
    internal_logic_located = run_audit["internal_uptrend_source_logic_located"]
    direct_external_count = external_candidates["direct_standalone_uptrend_provider_count"]

    directly_callable_provider_locked = direct_external_count > 0

    if directly_callable_provider_locked:
        conclusion = "UPTREND_PROVIDER_DIRECT_ENTRYPOINT_CANDIDATE_FOUND_REVIEW_REQUIRED"
        next_action = (
            "Proceed to 4C-2C-4E-D2: verify the direct provider candidate against existing run_stateful_simulation behavior "
            "before adapter implementation."
        )
        implementation_allowed_now = False
        provider_lock_status = "DIRECT_CANDIDATE_FOUND_NOT_VERIFIED"
    elif internal_logic_located:
        conclusion = "UPTREND_LOGIC_LOCATED_INSIDE_RUN_STATEFUL_BUT_PROVIDER_EXTRACTION_REQUIRED"
        next_action = (
            "Proceed to 4C-2C-4E-D2: design a no-strategy-change UPTREND provider extraction plan from run_stateful_simulation. "
            "The provider must reproduce existing candidate/order logic and must be validated by a short-window equivalence smoke."
        )
        implementation_allowed_now = False
        provider_lock_status = "SOURCE_LOGIC_LOCATED_INTERNAL_ONLY"
    else:
        conclusion = "UPTREND_PROVIDER_ENTRYPOINT_NOT_LOCATED_REVIEW_REQUIRED"
        next_action = (
            "Do not implement adapter. Manually review backtest.py and related scripts to locate the validated UPTREND logic."
        )
        implementation_allowed_now = False
        provider_lock_status = "NOT_LOCATED"

    return {
        "prior_d_requires_uptrend_provider_lock": prior_d.get("entrypoint_status", {}).get("uptrend_provider_entrypoint_locked") is False,
        "internal_run_stateful_uptrend_logic_located": internal_logic_located,
        "direct_standalone_provider_candidate_count": direct_external_count,
        "directly_callable_provider_locked": directly_callable_provider_locked,
        "provider_lock_status": provider_lock_status,
        "action_dict_shapes_found": action_shapes["action_like_dict_count"] > 0,
        "implementation_allowed_now": implementation_allowed_now,
        "conclusion": conclusion,
        "recommended_next_action": next_action,
        "engineering_rule": (
            "Do not re-invent UPTREND ranking/order logic. Adapter implementation must either call a verified provider "
            "or extract the existing run_stateful_simulation logic under a no-strategy-change equivalence test."
        ),
    }

def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    prior_d = load_prior_d()
    run_audit = audit_run_stateful_uptrend_logic()
    functions = function_index()
    external_candidates = locate_external_provider_candidates(functions)
    action_shapes = audit_action_dict_shapes()
    repo_refs = audit_repo_references()

    decision = derive_lock_decision(
        run_audit=run_audit,
        external_candidates=external_candidates,
        action_shapes=action_shapes,
        prior_d=prior_d,
    )

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "audit_only_no_backtest_run": True,
        "full_5y_backtest_run": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "invalid_artifacts_not_used_as_source": True,
        "composer_not_used": True,
        "return_curve_stitching_not_used": True,
        "prior_d_loaded": prior_d["exists"] is True,
        "run_stateful_audited": run_audit["path"] == "src/engine/backtest.py",
        "internal_uptrend_logic_located": run_audit["internal_uptrend_source_logic_located"] is True,
        "action_shapes_audited": action_shapes["action_like_dict_count"] >= 0,
        "decision_generated": bool(decision["conclusion"]),
        "implementation_not_allowed_yet": decision["implementation_allowed_now"] is False,
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-D1",
        "status": "UPTREND_PROVIDER_ENTRYPOINT_AUDIT_COMPLETE",
        "purpose": "Locate and lock the validated UPTREND candidate/order source before implementing the continuous-stateful E1R adapter.",
        "policy": {
            "strategy_logic_changed": False,
            "backtest_engine_run": False,
            "full_5y_backtest_run": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
            "invalid_artifacts_used_as_source": False,
            "composer_used": False,
            "return_curve_stitching_used": False,
        },
        "prior_d_evidence": prior_d,
        "run_stateful_uptrend_audit": run_audit,
        "external_provider_candidates": external_candidates,
        "action_dict_shape_audit": action_shapes,
        "repo_reference_audit": repo_refs,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-D1 — UPTREND Provider Entrypoint Audit")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("Locate and lock the validated UPTREND candidate/order source before implementing the continuous-stateful E1R adapter.")
    md.append("")
    md.append("## Policy")
    md.append("```json")
    md.append(json.dumps(report["policy"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Validations")
    md.append("```json")
    md.append(json.dumps(validations, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Prior D Evidence")
    md.append("```json")
    md.append(json.dumps(prior_d, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Run Stateful UPTREND Audit Summary")
    md.append("```json")
    md.append(json.dumps({
        "path": run_audit["path"],
        "function": run_audit["function"],
        "start_line": run_audit["start_line"],
        "end_line": run_audit["end_line"],
        "line_count": run_audit["line_count"],
        "static_evidence": run_audit["static_evidence"],
        "internal_uptrend_source_logic_located": run_audit["internal_uptrend_source_logic_located"],
        "keyword_hits_count": run_audit["keyword_hits_count"],
    }, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## External Provider Candidate Summary")
    md.append("```json")
    md.append(json.dumps({
        "direct_standalone_uptrend_provider_count": external_candidates["direct_standalone_uptrend_provider_count"],
        "likely_candidate_provider_count": len(external_candidates["likely_candidate_provider_functions"]),
        "likely_order_provider_count": len(external_candidates["likely_order_provider_functions"]),
        "likely_stateful_provider_count": len(external_candidates["likely_stateful_provider_functions"]),
    }, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Decision")
    md.append("```json")
    md.append(json.dumps(decision, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Next Action")
    md.append("")
    md.append(decision["recommended_next_action"])
    md.append("")

    REPORT_MD.write_text("\n".join(md))

    print("E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("prior_d_summary:", json.dumps(prior_d, ensure_ascii=False))
    print("run_stateful_uptrend_summary:", json.dumps({
        "path": run_audit["path"],
        "function": run_audit["function"],
        "start_line": run_audit["start_line"],
        "end_line": run_audit["end_line"],
        "line_count": run_audit["line_count"],
        "static_evidence": run_audit["static_evidence"],
        "internal_uptrend_source_logic_located": run_audit["internal_uptrend_source_logic_located"],
        "keyword_hits_count": run_audit["keyword_hits_count"],
    }, ensure_ascii=False))
    print("external_provider_summary:", json.dumps({
        "direct_standalone_uptrend_provider_count": external_candidates["direct_standalone_uptrend_provider_count"],
        "likely_candidate_provider_count": len(external_candidates["likely_candidate_provider_functions"]),
        "likely_order_provider_count": len(external_candidates["likely_order_provider_functions"]),
        "likely_stateful_provider_count": len(external_candidates["likely_stateful_provider_functions"]),
    }, ensure_ascii=False))
    print("action_dict_shape_summary:", json.dumps({
        "action_like_dict_count": action_shapes["action_like_dict_count"],
        "literal_action_counts": action_shapes["literal_action_counts"],
    }, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
