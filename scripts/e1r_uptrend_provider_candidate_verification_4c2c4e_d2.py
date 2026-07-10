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

D1_REPORT = ROOT / "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json"
D_REPORT = ROOT / "docs/research/E1R_4C2C4E_D_CONTINUOUS_STATEFUL_ADAPTER_DESIGN.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_D2_UPTREND_PROVIDER_CANDIDATE_VERIFICATION.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_D2_UPTREND_PROVIDER_CANDIDATE_VERIFICATION.md"

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

INVALID_ARTIFACTS = [
    "exports/e1r_unified_5y_full_account_v1_result.json",
    "exports/e1r_unified_5y_dashboard_research_bundle.json",
    "exports/e1r_combined_5y_original_max3_result.json",
    "exports/e1r_combined_5y_original_max3_equity_curve.json",
    "exports/e1r_combined_5y_original_max3_summary.json",
]

ACTION_TERMS = ["BUY", "ADD", "HOLD", "REDUCE", "EXIT", "TP_REDUCE"]
STATE_TERMS = ["cash", "positions", "total_equity", "positions_value", "open_positions_count"]
CANDIDATE_TERMS = ["candidate", "rank", "leader_score", "entry_top_n", "max_positions", "qualified"]
MARKET_TERMS = ["market_gate", "gate_allowed", "risk_off", "SPX", "MA50", "e1r_regime"]
OUTPUT_TERMS = ["orders", "trades", "daily_records", "daily_equity_records", "actions", "records"]

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
    out = []
    for root in SEARCH_ROOTS:
        if root.exists():
            out.extend(sorted(root.rglob("*.py")))
    return out

def line_window(lines: list[str], line_no: int, before: int = 8, after: int = 12) -> list[dict[str, Any]]:
    start = max(1, line_no - before)
    end = min(len(lines), line_no + after)
    return [{"line": i, "text": lines[i - 1][:300]} for i in range(start, end + 1)]

def load_prior_reports() -> dict[str, Any]:
    out = {
        "d_report_exists": D_REPORT.exists(),
        "d1_report_exists": D1_REPORT.exists(),
        "d_summary": None,
        "d1_summary": None,
    }

    if D_REPORT.exists():
        d = read_json(D_REPORT)
        out["d_summary"] = {
            "status": d.get("status"),
            "decision": d.get("decision"),
            "uptrend_provider_status": d.get("branch_providers", {}).get("UPTREND_signal_provider", {}).get("status"),
        }

    if D1_REPORT.exists():
        d1 = read_json(D1_REPORT)
        out["d1_summary"] = {
            "status": d1.get("status"),
            "decision": d1.get("decision"),
            "direct_standalone_uptrend_provider_count": d1.get("external_provider_candidates", {}).get("direct_standalone_uptrend_provider_count"),
            "internal_uptrend_source_logic_located": d1.get("run_stateful_uptrend_audit", {}).get("internal_uptrend_source_logic_located"),
        }

    return out

def source_for_function(path: Path, name: str, start_line: int | None = None) -> dict[str, Any] | None:
    try:
        text = read_text(path)
        tree = ast.parse(text)
    except Exception:
        return None

    lines = text.splitlines()

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            if start_line is not None and node.lineno != start_line:
                continue

            start = node.lineno
            end = getattr(node, "end_lineno", start)
            source = "\n".join(lines[start - 1:end])
            return {
                "path": rel(path),
                "name": name,
                "start_line": start,
                "end_line": end,
                "line_count": end - start + 1,
                "args": [a.arg for a in node.args.args],
                "source": source,
                "lines": lines,
            }

    return None

def extract_direct_candidates_from_d1() -> list[dict[str, Any]]:
    if not D1_REPORT.exists():
        return []

    d1 = read_json(D1_REPORT)
    direct = d1.get("external_provider_candidates", {}).get("direct_standalone_uptrend_provider_candidates", [])
    if not isinstance(direct, list):
        direct = []

    out = []
    for item in direct:
        if not isinstance(item, dict):
            continue

        path = ROOT / item.get("path", "")
        name = item.get("name")
        start_line = item.get("start_line")

        if path.exists() and name:
            src = source_for_function(path, name, start_line)
        else:
            src = None

        out.append({
            "d1_item": item,
            "source": src,
        })

    return out

def find_additional_direct_candidates() -> list[dict[str, Any]]:
    candidates = []

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

            start = node.lineno
            end = getattr(node, "end_lineno", start)
            source = "\n".join(lines[start - 1:end])
            lower = source.lower()
            name_lower = node.name.lower()

            contains_candidate = "candidate" in lower or "leader_score" in lower or "rank" in lower
            contains_order = any(term in source for term in ACTION_TERMS) or "buy_size" in source or "sell_size" in source
            contains_state = "positions" in source and "cash" in source
            contains_maxpos = "max_positions" in source or "entry_top_n" in source

            if contains_candidate and contains_order and contains_state and contains_maxpos:
                candidates.append({
                    "path": rel(path),
                    "name": node.name,
                    "start_line": start,
                    "end_line": end,
                    "line_count": end - start + 1,
                    "args": [a.arg for a in node.args.args],
                    "contains_candidate": contains_candidate,
                    "contains_order": contains_order,
                    "contains_state": contains_state,
                    "contains_max_positions": contains_maxpos,
                })

    return candidates

def classify_function(src: dict[str, Any] | None) -> dict[str, Any]:
    if src is None:
        return {
            "available": False,
            "classification": "SOURCE_NOT_AVAILABLE",
            "score": 0,
            "reasons": [],
            "risks": ["Cannot inspect source."],
        }

    source = src["source"]
    lower = source.lower()
    args = src.get("args") or []

    features = {
        "has_candidate_logic": any(term in lower for term in ["candidate", "rank", "leader_score", "qualified", "score"]),
        "has_buy_logic": "BUY" in source or "buy_size" in source or "action_buy" in lower,
        "has_add_logic": "ADD" in source or "add_size" in source,
        "has_reduce_logic": "REDUCE" in source or "reduce_size" in source,
        "has_exit_logic": "EXIT" in source or "sell_size" in source or "ls60_exit_mode" in source,
        "has_hold_logic": "HOLD" in source,
        "has_positions_state": "positions" in source,
        "has_cash_state": "cash" in source,
        "has_total_equity": "total_equity" in source or "equity" in source,
        "has_daily_records": "daily_records" in source or "daily_equity_records" in source or "records" in source,
        "has_market_gate": "market_gate" in source or "gate_allowed" in source or "risk_off" in source,
        "has_max_positions": "max_positions" in source or "entry_top_n" in source,
        "has_price_inputs": any(arg in args for arg in ["prices_map", "dates_map", "spx_prices", "spx_dates"]),
        "has_assumptions_arg": "assumptions" in args or "a" in args,
        "imports_or_reads_invalid_artifacts": any(path in source for path in INVALID_ARTIFACTS),
        "calls_run_stateful_simulation": "run_stateful_simulation" in source and src["name"] != "run_stateful_simulation",
        "is_script_main_or_export": "__main__" in source or "write_text" in source or "exports/" in source,
        "contains_sidecar": "sidecar" in lower,
    }

    score = 0
    reasons = []
    risks = []

    positive_weights = {
        "has_candidate_logic": 2,
        "has_buy_logic": 2,
        "has_exit_logic": 2,
        "has_positions_state": 2,
        "has_cash_state": 2,
        "has_market_gate": 1,
        "has_max_positions": 2,
        "has_price_inputs": 1,
        "has_assumptions_arg": 1,
    }

    for k, w in positive_weights.items():
        if features[k]:
            score += w
            reasons.append(k)

    if features["imports_or_reads_invalid_artifacts"]:
        score -= 10
        risks.append("References banned invalid artifacts.")
    if features["is_script_main_or_export"]:
        score -= 2
        risks.append("Looks like script/export helper, not a clean provider.")
    if features["calls_run_stateful_simulation"]:
        score -= 2
        risks.append("Wrapper around run_stateful_simulation, not independent provider.")
    if features["contains_sidecar"]:
        risks.append("Contains sidecar terms; may be mixed-regime helper rather than pure UPTREND provider.")

    if features["has_candidate_logic"] and features["has_buy_logic"] and features["has_exit_logic"] and features["has_positions_state"] and features["has_cash_state"]:
        classification = "STATEFUL_UPTREND_SIMULATOR_OR_PROVIDER_CANDIDATE"
    elif features["has_candidate_logic"] and not (features["has_buy_logic"] or features["has_exit_logic"]):
        classification = "CANDIDATE_GENERATOR_ONLY"
    elif (features["has_buy_logic"] or features["has_exit_logic"]) and not features["has_candidate_logic"]:
        classification = "ORDER_OR_ACTION_HELPER_ONLY"
    elif features["calls_run_stateful_simulation"]:
        classification = "BACKTEST_WRAPPER_NOT_PROVIDER"
    else:
        classification = "DIAGNOSTIC_OR_UNCLEAR_HELPER"

    return {
        "available": True,
        "classification": classification,
        "score": score,
        "reasons": reasons,
        "risks": risks,
        "features": features,
    }

def extract_action_shapes(src: dict[str, Any] | None) -> dict[str, Any]:
    if src is None:
        return {"action_like_dict_count": 0, "literal_action_counts": {}, "samples": []}

    try:
        tree = ast.parse(src["source"])
    except Exception:
        return {"action_like_dict_count": 0, "literal_action_counts": {}, "samples": []}

    actions = []
    start_line = src["start_line"]

    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            keys = []
            literals = {}
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    keys.append(k.value)
                    try:
                        literals[k.value] = ast.literal_eval(v)
                    except Exception:
                        literals[k.value] = None

            keyset = set(keys)
            if keyset.intersection({"action", "symbol", "date", "reason", "shares", "qty", "quantity", "branch"}):
                actions.append({
                    "line": start_line + getattr(node, "lineno", 1) - 1,
                    "keys": keys,
                    "literal_action": literals.get("action"),
                    "literal_reason": literals.get("reason"),
                })

    counts = Counter(str(a["literal_action"]) for a in actions if a.get("literal_action") is not None)

    return {
        "action_like_dict_count": len(actions),
        "literal_action_counts": dict(counts),
        "samples": actions[:80],
    }

def extract_return_shape(src: dict[str, Any] | None) -> dict[str, Any]:
    if src is None:
        return {"return_statements": []}

    try:
        tree = ast.parse(src["source"])
    except Exception:
        return {"return_statements": []}

    returns = []
    start_line = src["start_line"]

    for node in ast.walk(tree):
        if isinstance(node, ast.Return):
            line = start_line + getattr(node, "lineno", 1) - 1
            shape = "unknown"

            if isinstance(node.value, ast.Dict):
                keys = []
                for k in node.value.keys:
                    if isinstance(k, ast.Constant) and isinstance(k.value, str):
                        keys.append(k.value)
                shape = {"type": "dict", "keys": keys}
            elif isinstance(node.value, ast.List):
                shape = {"type": "list"}
            elif isinstance(node.value, ast.Name):
                shape = {"type": "name", "name": node.value.id}
            elif isinstance(node.value, ast.Tuple):
                shape = {"type": "tuple", "len": len(node.value.elts)}

            returns.append({
                "line": line,
                "shape": shape,
            })

    return {"return_statements": returns[:80]}

def inspect_candidate_contexts(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    inspected = []

    for c in candidates:
        src = c.get("source")
        d1_item = c.get("d1_item", {})
        classification = classify_function(src)
        action_shapes = extract_action_shapes(src)
        return_shape = extract_return_shape(src)

        contexts = {}
        if src is not None:
            lines = src["lines"]
            start = src["start_line"]
            source_lines = src["source"].splitlines()

            for term_group, terms in {
                "candidate_terms": CANDIDATE_TERMS,
                "action_terms": ACTION_TERMS,
                "state_terms": STATE_TERMS,
                "market_terms": MARKET_TERMS,
                "output_terms": OUTPUT_TERMS,
            }.items():
                hits = []
                for idx, line in enumerate(source_lines, start=start):
                    if any(term in line for term in terms):
                        hits.append({
                            "line": idx,
                            "text": line.strip()[:300],
                            "context": line_window(lines, idx, 4, 8),
                        })
                contexts[term_group] = hits[:30]

        inspected.append({
            "path": d1_item.get("path") or (src or {}).get("path"),
            "name": d1_item.get("name") or (src or {}).get("name"),
            "start_line": d1_item.get("start_line") or (src or {}).get("start_line"),
            "end_line": d1_item.get("end_line") or (src or {}).get("end_line"),
            "line_count": d1_item.get("line_count") or (src or {}).get("line_count"),
            "args": d1_item.get("args") or (src or {}).get("args"),
            "classification": classification,
            "action_shapes": action_shapes,
            "return_shape": return_shape,
            "contexts": contexts,
        })

    return inspected

def select_best_candidate(inspected: list[dict[str, Any]]) -> dict[str, Any]:
    if not inspected:
        return {
            "selected": None,
            "selection_status": "NO_DIRECT_CANDIDATES",
            "reason": "No direct provider candidates available from D1 report.",
        }

    ranked = sorted(
        inspected,
        key=lambda x: (
            x["classification"]["score"],
            x["action_shapes"]["action_like_dict_count"],
            x.get("line_count") or 0,
        ),
        reverse=True,
    )

    best = ranked[0]
    best_class = best["classification"]["classification"]
    best_score = best["classification"]["score"]

    if best_class == "STATEFUL_UPTREND_SIMULATOR_OR_PROVIDER_CANDIDATE" and best_score >= 8:
        status = "BEST_CANDIDATE_REQUIRES_EQUIVALENCE_SMOKE"
        reason = (
            "A high-scoring candidate exists, but it still must be verified against run_stateful_simulation behavior "
            "before adapter use."
        )
    else:
        status = "NO_VERIFIED_DIRECT_PROVIDER_YET"
        reason = (
            "Candidates exist, but none can be treated as a verified UPTREND provider without equivalence testing "
            "or no-strategy-change extraction."
        )

    return {
        "selected": {
            "path": best["path"],
            "name": best["name"],
            "start_line": best["start_line"],
            "end_line": best["end_line"],
            "line_count": best["line_count"],
            "args": best["args"],
            "classification": best["classification"]["classification"],
            "score": best["classification"]["score"],
            "reasons": best["classification"]["reasons"],
            "risks": best["classification"]["risks"],
            "action_like_dict_count": best["action_shapes"]["action_like_dict_count"],
            "literal_action_counts": best["action_shapes"]["literal_action_counts"],
            "return_shape": best["return_shape"],
        },
        "selection_status": status,
        "reason": reason,
        "ranked_candidates_summary": [
            {
                "rank": i + 1,
                "path": c["path"],
                "name": c["name"],
                "start_line": c["start_line"],
                "classification": c["classification"]["classification"],
                "score": c["classification"]["score"],
                "risks": c["classification"]["risks"],
                "action_like_dict_count": c["action_shapes"]["action_like_dict_count"],
                "literal_action_counts": c["action_shapes"]["literal_action_counts"],
            }
            for i, c in enumerate(ranked[:20])
        ],
    }

def audit_run_stateful_baseline_shape() -> dict[str, Any]:
    src = source_for_function(BACKTEST_PATH, "run_stateful_simulation")
    classification = classify_function(src)
    action_shapes = extract_action_shapes(src)
    return_shape = extract_return_shape(src)

    return {
        "path": "src/engine/backtest.py",
        "name": "run_stateful_simulation",
        "classification": classification,
        "action_shapes": action_shapes,
        "return_shape": return_shape,
        "note": "This is the behavioral baseline, but it is not directly usable as adapter UPTREND provider because it owns a full simulation loop.",
    }

def derive_decision(best: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    selected = best.get("selected")
    status = best.get("selection_status")

    if status == "BEST_CANDIDATE_REQUIRES_EQUIVALENCE_SMOKE" and selected:
        conclusion = "UPTREND_PROVIDER_CANDIDATE_SELECTED_FOR_EQUIVALENCE_SMOKE"
        next_action = (
            "Proceed to 4C-2C-4E-D3: run a short-window UPTREND-only equivalence smoke comparing the selected candidate "
            "against run_stateful_simulation action/order behavior. Do not implement adapter yet."
        )
        provider_locked = False
    else:
        conclusion = "UPTREND_PROVIDER_NOT_LOCKED_EXTRACTION_OR_MANUAL_REVIEW_REQUIRED"
        next_action = (
            "Proceed to 4C-2C-4E-D3: either verify the top candidate by equivalence smoke or design a no-strategy-change "
            "provider extraction from run_stateful_simulation. Do not implement adapter yet."
        )
        provider_locked = False

    return {
        "uptrend_provider_locked": provider_locked,
        "implementation_allowed_now": False,
        "selected_candidate": selected,
        "baseline": {
            "path": baseline["path"],
            "name": baseline["name"],
            "action_like_dict_count": baseline["action_shapes"]["action_like_dict_count"],
            "literal_action_counts": baseline["action_shapes"]["literal_action_counts"],
        },
        "conclusion": conclusion,
        "recommended_next_action": next_action,
        "engineering_rule": (
            "The selected UPTREND provider candidate is not allowed in adapter trading logic until equivalence against "
            "the existing run_stateful_simulation UPTREND behavior is demonstrated."
        ),
    }

def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    prior = load_prior_reports()
    d1_candidates = extract_direct_candidates_from_d1()
    additional_candidates = find_additional_direct_candidates()

    inspected = inspect_candidate_contexts(d1_candidates)
    best = select_best_candidate(inspected)
    baseline = audit_run_stateful_baseline_shape()
    decision = derive_decision(best, baseline)

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
        "d1_report_loaded": prior["d1_report_exists"],
        "d_report_loaded": prior["d_report_exists"],
        "direct_candidates_from_d1_loaded": len(d1_candidates) > 0,
        "direct_candidates_inspected": len(inspected) == len(d1_candidates) and len(inspected) > 0,
        "best_candidate_selected_or_reviewed": best["selection_status"] in {
            "BEST_CANDIDATE_REQUIRES_EQUIVALENCE_SMOKE",
            "NO_VERIFIED_DIRECT_PROVIDER_YET",
            "NO_DIRECT_CANDIDATES",
        },
        "run_stateful_baseline_audited": baseline["path"] == "src/engine/backtest.py",
        "provider_not_locked_yet": decision["uptrend_provider_locked"] is False,
        "implementation_not_allowed_yet": decision["implementation_allowed_now"] is False,
        "decision_generated": bool(decision["conclusion"]),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-D2",
        "status": "UPTREND_PROVIDER_CANDIDATE_VERIFICATION_AUDIT_COMPLETE",
        "purpose": "Classify and verify direct UPTREND provider candidates found by D1 before adapter implementation.",
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
        "prior_reports": prior,
        "d1_direct_candidates_count": len(d1_candidates),
        "additional_direct_candidates_count": len(additional_candidates),
        "additional_direct_candidates_sample": additional_candidates[:40],
        "inspected_candidates": inspected,
        "best_candidate_selection": best,
        "run_stateful_baseline_shape": baseline,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)

    selected = decision.get("selected_candidate") or {}

    md = []
    md.append("# E1R 4C-2C-4E-D2 — UPTREND Provider Candidate Verification Audit")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("Classify and verify direct UPTREND provider candidates found by D1 before adapter implementation.")
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
    md.append("## Candidate Counts")
    md.append("```json")
    md.append(json.dumps({
        "d1_direct_candidates_count": len(d1_candidates),
        "additional_direct_candidates_count": len(additional_candidates),
    }, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Ranked Candidates Summary")
    md.append("```json")
    md.append(json.dumps(best.get("ranked_candidates_summary"), indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Selected Candidate")
    md.append("```json")
    md.append(json.dumps(selected, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Baseline")
    md.append("```json")
    md.append(json.dumps(decision["baseline"], indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_D2_UPTREND_PROVIDER_CANDIDATE_VERIFICATION_AUDIT_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("candidate_counts:", json.dumps({
        "d1_direct_candidates_count": len(d1_candidates),
        "additional_direct_candidates_count": len(additional_candidates),
    }, ensure_ascii=False))
    print("ranked_candidates_summary:", json.dumps(best.get("ranked_candidates_summary"), ensure_ascii=False))
    print("selected_candidate:", json.dumps(selected, ensure_ascii=False))
    print("baseline_summary:", json.dumps(decision["baseline"], ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
