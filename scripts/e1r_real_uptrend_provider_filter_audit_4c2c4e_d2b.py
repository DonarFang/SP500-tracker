#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import hashlib
from datetime import datetime, timezone
from typing import Any
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

D2_REPORT = ROOT / "docs/research/E1R_4C2C4E_D2_UPTREND_PROVIDER_CANDIDATE_VERIFICATION.json"
D1_REPORT = ROOT / "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json"
D_REPORT = ROOT / "docs/research/E1R_4C2C4E_D_CONTINUOUS_STATEFUL_ADAPTER_DESIGN.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_D2B_REAL_UPTREND_PROVIDER_FILTER_AUDIT.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_D2B_REAL_UPTREND_PROVIDER_FILTER_AUDIT.md"

BACKTEST_PATH = ROOT / "src/engine/backtest.py"
TRACKING_ENGINE_PATH = ROOT / "src/oos/tracking_engine.py"
SIDECAR_PATH = ROOT / "src/engine/e1r_sidecar_sleeve.py"
COMPOSER_PATH = ROOT / "src/engine/e1r_composer.py"

FROZEN_STRATEGY_FILES = [
    BACKTEST_PATH,
    SIDECAR_PATH,
    COMPOSER_PATH,
]

SEARCH_ROOTS = [
    ROOT / "src",
    ROOT / "tests",
]

BANNED_PROVIDER_PATH_PREFIXES = [
    "scripts/",
    "docs/",
]

BANNED_PROVIDER_NAME_TERMS = [
    "audit",
    "design",
    "inspect",
    "verify",
    "validation",
    "report",
    "summary",
    "index",
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
CANDIDATE_TERMS = ["candidate", "rank", "leader_score", "entry_top_n", "max_positions", "qualified", "score"]
MARKET_TERMS = ["market_gate", "gate_allowed", "risk_off", "SPX", "MA50", "market_state"]
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

def line_window(lines: list[str], line_no: int, before: int = 8, after: int = 14) -> list[dict[str, Any]]:
    start = max(1, line_no - before)
    end = min(len(lines), line_no + after)
    return [{"line": i, "text": lines[i - 1][:320]} for i in range(start, end + 1)]

def function_source(path: Path, name: str, start_line: int | None = None) -> dict[str, Any] | None:
    if not path.exists():
        return None

    try:
        text = read_text(path)
        tree = ast.parse(text)
    except Exception:
        return None

    lines = text.splitlines()

    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        if node.name != name:
            continue
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

def iter_functions() -> list[dict[str, Any]]:
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

            start = node.lineno
            end = getattr(node, "end_lineno", start)
            source = "\n".join(lines[start - 1:end])
            out.append({
                "path": rel(path),
                "name": node.name,
                "start_line": start,
                "end_line": end,
                "line_count": end - start + 1,
                "args": [a.arg for a in node.args.args],
                "source": source,
                "lines": lines,
            })

    return out

def load_prior() -> dict[str, Any]:
    out = {
        "d_exists": D_REPORT.exists(),
        "d1_exists": D1_REPORT.exists(),
        "d2_exists": D2_REPORT.exists(),
        "d2_selected_candidate": None,
        "d2_ranked_candidates": None,
        "d2_decision": None,
    }

    if D2_REPORT.exists():
        d2 = read_json(D2_REPORT)
        out["d2_selected_candidate"] = d2.get("decision", {}).get("selected_candidate")
        out["d2_ranked_candidates"] = d2.get("best_candidate_selection", {}).get("ranked_candidates_summary")
        out["d2_decision"] = d2.get("decision")

    return out

def is_banned_false_positive(path: str, name: str) -> tuple[bool, list[str]]:
    reasons = []

    if any(path.startswith(prefix) for prefix in BANNED_PROVIDER_PATH_PREFIXES):
        reasons.append("path_is_script_or_docs_not_runtime_provider")

    lower_name = name.lower()
    for term in BANNED_PROVIDER_NAME_TERMS:
        if term in lower_name:
            reasons.append(f"name_contains_{term}")

    if "4c2c4e" in path.lower():
        reasons.append("path_is_stage_audit_script")

    if reasons:
        return True, reasons

    return False, []

def classify_runtime_function(fn: dict[str, Any]) -> dict[str, Any]:
    source = fn["source"]
    lower = source.lower()
    path = fn["path"]
    name = fn["name"]

    banned, banned_reasons = is_banned_false_positive(path, name)

    features = {
        "runtime_src_path": path.startswith("src/"),
        "oos_path": path.startswith("src/oos/"),
        "engine_path": path.startswith("src/engine/"),
        "has_candidate_logic": any(t in lower for t in ["candidate", "leader_score", "rank", "qualified", "score"]),
        "has_buy_logic": "BUY" in source or "buy_size" in source,
        "has_add_logic": "ADD" in source or "add_size" in source,
        "has_reduce_logic": "REDUCE" in source or "reduce_size" in source,
        "has_exit_logic": "EXIT" in source or "sell_size" in source or "ls60_exit_mode" in source,
        "has_hold_logic": "HOLD" in source,
        "has_positions_state": "positions" in source,
        "has_cash_state": "cash" in source,
        "has_total_equity": "total_equity" in source or "equity" in source,
        "has_open_positions_count": "open_positions_count" in source or "len(positions)" in source,
        "has_market_gate": "market_gate" in source or "gate_allowed" in source or "risk_off" in source,
        "has_max_positions": "max_positions" in source or "entry_top_n" in source,
        "has_orders_or_trades": "orders" in source or "trades" in source or "actions" in source,
        "has_daily_loop": "for " in source and ("date" in source or "dates" in source),
        "references_invalid_artifacts": any(p in source for p in INVALID_ARTIFACTS),
        "calls_run_stateful_simulation": "run_stateful_simulation" in source and name != "run_stateful_simulation",
        "contains_sidecar": "sidecar" in lower,
    }

    score = 0
    if features["runtime_src_path"]:
        score += 5
    if features["has_candidate_logic"]:
        score += 2
    if features["has_buy_logic"]:
        score += 2
    if features["has_exit_logic"]:
        score += 2
    if features["has_positions_state"]:
        score += 2
    if features["has_cash_state"]:
        score += 2
    if features["has_market_gate"]:
        score += 1
    if features["has_max_positions"]:
        score += 2
    if features["has_orders_or_trades"]:
        score += 1

    risks = []
    if banned:
        score -= 20
        risks.extend(banned_reasons)
    if features["references_invalid_artifacts"]:
        score -= 20
        risks.append("references_invalid_artifacts")
    if features["calls_run_stateful_simulation"]:
        score -= 3
        risks.append("wrapper_around_run_stateful_simulation")
    if features["contains_sidecar"]:
        risks.append("contains_sidecar_terms_may_not_be_pure_uptrend")

    if banned:
        classification = "FALSE_POSITIVE_AUDIT_OR_DESIGN_HELPER"
    elif features["runtime_src_path"] and features["has_candidate_logic"] and features["has_buy_logic"] and features["has_exit_logic"] and features["has_positions_state"] and features["has_cash_state"]:
        classification = "REAL_RUNTIME_PROVIDER_CANDIDATE"
    elif features["runtime_src_path"] and features["has_candidate_logic"] and not (features["has_buy_logic"] or features["has_exit_logic"]):
        classification = "RUNTIME_CANDIDATE_GENERATOR_ONLY"
    elif features["runtime_src_path"] and (features["has_buy_logic"] or features["has_exit_logic"]):
        classification = "RUNTIME_ORDER_OR_TRACKING_HELPER"
    else:
        classification = "NOT_A_PROVIDER"

    return {
        "path": path,
        "name": name,
        "start_line": fn["start_line"],
        "end_line": fn["end_line"],
        "line_count": fn["line_count"],
        "args": fn["args"],
        "classification": classification,
        "score": score,
        "features": features,
        "risks": risks,
    }

def extract_action_shapes(fn: dict[str, Any] | None) -> dict[str, Any]:
    if fn is None:
        return {"action_like_dict_count": 0, "literal_action_counts": {}, "samples": []}

    try:
        tree = ast.parse(fn["source"])
    except Exception:
        return {"action_like_dict_count": 0, "literal_action_counts": {}, "samples": []}

    actions = []
    start_line = fn["start_line"]

    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue

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
        if keyset.intersection({"action", "symbol", "date", "reason", "shares", "qty", "quantity", "branch", "order_type"}):
            actions.append({
                "line": start_line + getattr(node, "lineno", 1) - 1,
                "keys": keys,
                "literal_action": literals.get("action"),
                "literal_reason": literals.get("reason"),
                "literal_order_type": literals.get("order_type"),
            })

    counts = Counter(str(a["literal_action"]) for a in actions if a.get("literal_action") is not None)

    return {
        "action_like_dict_count": len(actions),
        "literal_action_counts": dict(counts),
        "samples": actions[:120],
    }

def inspect_contexts(fn: dict[str, Any] | None) -> dict[str, Any]:
    if fn is None:
        return {}

    contexts = {}
    source_lines = fn["source"].splitlines()
    lines = fn["lines"]
    start = fn["start_line"]

    groups = {
        "candidate_terms": CANDIDATE_TERMS,
        "action_terms": ACTION_TERMS,
        "state_terms": STATE_TERMS,
        "market_terms": MARKET_TERMS,
        "output_terms": OUTPUT_TERMS,
    }

    for name, terms in groups.items():
        hits = []
        for idx, line in enumerate(source_lines, start=start):
            if any(term in line for term in terms):
                hits.append({
                    "line": idx,
                    "text": line.strip()[:340],
                    "context": line_window(lines, idx, 5, 10),
                })
        contexts[name] = hits[:50]

    return contexts

def audit_run_oos_day() -> dict[str, Any]:
    fn = function_source(TRACKING_ENGINE_PATH, "run_oos_day")
    if fn is None:
        return {
            "exists": False,
            "path": rel(TRACKING_ENGINE_PATH),
            "name": "run_oos_day",
        }

    classification = classify_runtime_function(fn)
    action_shapes = extract_action_shapes(fn)
    contexts = inspect_contexts(fn)

    can_be_direct_adapter_provider = False
    direct_blockers = []

    if not classification["features"]["has_candidate_logic"]:
        direct_blockers.append("no_candidate_generation_evidence")
    if not classification["features"]["has_buy_logic"]:
        direct_blockers.append("no_buy_generation_evidence")
    if not classification["features"]["has_exit_logic"]:
        direct_blockers.append("no_exit_generation_evidence")
    if not classification["features"]["has_positions_state"]:
        direct_blockers.append("no_positions_state_evidence")
    if classification["features"]["references_invalid_artifacts"]:
        direct_blockers.append("references_invalid_artifacts")
    if classification["features"]["calls_run_stateful_simulation"]:
        direct_blockers.append("wrapper_not_provider")

    if not direct_blockers and classification["classification"] == "REAL_RUNTIME_PROVIDER_CANDIDATE":
        can_be_direct_adapter_provider = True

    return {
        "exists": True,
        "path": fn["path"],
        "name": fn["name"],
        "start_line": fn["start_line"],
        "end_line": fn["end_line"],
        "line_count": fn["line_count"],
        "args": fn["args"],
        "classification": classification,
        "action_shapes": action_shapes,
        "contexts": contexts,
        "direct_adapter_provider_assessment": {
            "can_be_direct_adapter_provider_without_equivalence": False,
            "can_be_direct_adapter_provider_after_equivalence": can_be_direct_adapter_provider,
            "blockers_or_required_checks": direct_blockers + [
                "must_verify_same_UPTREND_rules_as_run_stateful_simulation",
                "must_verify_same_BUY_EXIT_dates_and_symbols_in_short_window",
                "must_verify_same_position_sizing_or explicitly map to adapter sizing",
                "must verify OOS assumptions do not depend on forward-only state unavailable in historical adapter",
            ],
        },
    }

def rank_real_runtime_candidates() -> dict[str, Any]:
    classified = []
    for fn in iter_functions():
        c = classify_runtime_function(fn)
        if c["classification"] in {
            "REAL_RUNTIME_PROVIDER_CANDIDATE",
            "RUNTIME_CANDIDATE_GENERATOR_ONLY",
            "RUNTIME_ORDER_OR_TRACKING_HELPER",
        }:
            action_shapes = extract_action_shapes(fn)
            classified.append({
                **{k: c[k] for k in ["path", "name", "start_line", "end_line", "line_count", "args", "classification", "score", "features", "risks"]},
                "action_like_dict_count": action_shapes["action_like_dict_count"],
                "literal_action_counts": action_shapes["literal_action_counts"],
            })

    ranked = sorted(
        classified,
        key=lambda x: (
            x["classification"] == "REAL_RUNTIME_PROVIDER_CANDIDATE",
            x["score"],
            x["action_like_dict_count"],
        ),
        reverse=True,
    )

    return {
        "real_runtime_candidate_count": len(ranked),
        "ranked_real_runtime_candidates": ranked[:80],
    }

def audit_d2_false_positive() -> dict[str, Any]:
    prior = load_prior()
    selected = prior.get("d2_selected_candidate") or {}

    path = selected.get("path")
    name = selected.get("name")

    if not path or not name:
        return {
            "d2_selected_exists": False,
            "false_positive_confirmed": None,
            "reason": "No selected candidate found in D2 report.",
        }

    banned, reasons = is_banned_false_positive(path, name)

    no_actions = (selected.get("action_like_dict_count") or 0) == 0
    risk_wrapper = any("Wrapper" in r or "wrapper" in r for r in selected.get("risks") or [])

    false_positive = bool(banned or no_actions or risk_wrapper)

    return {
        "d2_selected_exists": True,
        "d2_selected_candidate": selected,
        "false_positive_confirmed": false_positive,
        "false_positive_reasons": reasons + (
            ["no_action_like_dicts"] if no_actions else []
        ) + (
            ["wrapper_or_static_audit_risk"] if risk_wrapper else []
        ),
        "corrective_rule": "Exclude scripts/docs/audit/design functions from provider candidate set.",
    }

def audit_baseline_run_stateful() -> dict[str, Any]:
    fn = function_source(BACKTEST_PATH, "run_stateful_simulation")
    if fn is None:
        return {"exists": False}

    classification = classify_runtime_function(fn)
    action_shapes = extract_action_shapes(fn)

    return {
        "exists": True,
        "path": fn["path"],
        "name": fn["name"],
        "start_line": fn["start_line"],
        "end_line": fn["end_line"],
        "line_count": fn["line_count"],
        "classification": classification,
        "action_shapes": action_shapes,
        "baseline_role": "behavioral_reference_only_not_direct_provider",
    }

def derive_decision(
    false_positive_audit: dict[str, Any],
    run_oos: dict[str, Any],
    runtime_candidates: dict[str, Any],
    baseline: dict[str, Any],
) -> dict[str, Any]:
    run_oos_candidate = (
        run_oos.get("exists") is True
        and run_oos.get("classification", {}).get("classification") == "REAL_RUNTIME_PROVIDER_CANDIDATE"
    )

    run_oos_direct_without_equivalence = False

    if false_positive_audit.get("false_positive_confirmed") and run_oos_candidate:
        conclusion = "D2_FALSE_POSITIVE_FILTERED_RUN_OOS_DAY_REQUIRES_EQUIVALENCE_AUDIT"
        next_action = (
            "Proceed to 4C-2C-4E-D3: UPTREND runtime equivalence audit focused on "
            "src/oos/tracking_engine.py::run_oos_day versus src/engine/backtest.py::run_stateful_simulation. "
            "Do not implement adapter trading logic yet."
        )
    elif false_positive_audit.get("false_positive_confirmed") and not run_oos_candidate:
        conclusion = "D2_FALSE_POSITIVE_FILTERED_NO_RUNTIME_PROVIDER_LOCKED"
        next_action = (
            "Proceed to D3 extraction design from run_stateful_simulation. run_oos_day is not a sufficient runtime provider candidate."
        )
    else:
        conclusion = "D2B_REVIEW_REQUIRED"
        next_action = "Review provider filtering results manually before continuing."

    return {
        "d2_false_positive_confirmed": false_positive_audit.get("false_positive_confirmed"),
        "run_oos_day_is_runtime_candidate": run_oos_candidate,
        "run_oos_day_allowed_directly_without_equivalence": run_oos_direct_without_equivalence,
        "uptrend_provider_locked": False,
        "implementation_allowed_now": False,
        "baseline_reference": {
            "path": baseline.get("path"),
            "name": baseline.get("name"),
            "action_like_dict_count": baseline.get("action_shapes", {}).get("action_like_dict_count"),
            "literal_action_counts": baseline.get("action_shapes", {}).get("literal_action_counts"),
        },
        "candidate_for_next_equivalence_audit": {
            "path": "src/oos/tracking_engine.py",
            "name": "run_oos_day",
            "reason": "Best real runtime candidate after filtering out scripts/docs/audit/design false positives.",
        } if run_oos_candidate else None,
        "conclusion": conclusion,
        "recommended_next_action": next_action,
        "engineering_rule": (
            "Trading logic is not correct until proven equivalent or explicitly approved. "
            "Do not use audit scripts as providers. Do not use run_oos_day in adapter until equivalence with "
            "run_stateful_simulation UPTREND behavior is verified."
        ),
    }

def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    prior = load_prior()
    false_positive_audit = audit_d2_false_positive()
    run_oos = audit_run_oos_day()
    runtime_candidates = rank_real_runtime_candidates()
    baseline = audit_baseline_run_stateful()

    decision = derive_decision(false_positive_audit, run_oos, runtime_candidates, baseline)

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
        "d2_report_loaded": prior["d2_exists"],
        "d2_false_positive_confirmed": false_positive_audit.get("false_positive_confirmed") is True,
        "scripts_docs_filtered_from_provider_candidates": True,
        "run_oos_day_audited": run_oos.get("exists") is True,
        "runtime_candidates_ranked": runtime_candidates["real_runtime_candidate_count"] > 0,
        "baseline_run_stateful_audited": baseline.get("exists") is True,
        "provider_not_locked_yet": decision["uptrend_provider_locked"] is False,
        "implementation_not_allowed_yet": decision["implementation_allowed_now"] is False,
        "decision_generated": bool(decision["conclusion"]),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-D2B",
        "status": "REAL_UPTREND_PROVIDER_FILTER_AUDIT_COMPLETE",
        "purpose": "Filter false-positive provider candidates and inspect real runtime candidate src/oos/tracking_engine.py::run_oos_day.",
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
        "false_positive_audit": false_positive_audit,
        "run_oos_day_audit": run_oos,
        "runtime_candidate_ranking": runtime_candidates,
        "baseline_run_stateful_audit": baseline,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-D2B — Real UPTREND Provider Filter Audit")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("Filter false-positive provider candidates and inspect the real runtime candidate `src/oos/tracking_engine.py::run_oos_day`.")
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
    md.append("## False Positive Audit")
    md.append("```json")
    md.append(json.dumps(false_positive_audit, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## run_oos_day Summary")
    md.append("```json")
    md.append(json.dumps({
        "exists": run_oos.get("exists"),
        "path": run_oos.get("path"),
        "name": run_oos.get("name"),
        "start_line": run_oos.get("start_line"),
        "end_line": run_oos.get("end_line"),
        "line_count": run_oos.get("line_count"),
        "args": run_oos.get("args"),
        "classification": run_oos.get("classification"),
        "action_shapes": run_oos.get("action_shapes"),
        "direct_adapter_provider_assessment": run_oos.get("direct_adapter_provider_assessment"),
    }, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Runtime Candidate Ranking")
    md.append("```json")
    md.append(json.dumps(runtime_candidates["ranked_real_runtime_candidates"][:20], indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_D2B_REAL_UPTREND_PROVIDER_FILTER_AUDIT_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("false_positive_audit:", json.dumps(false_positive_audit, ensure_ascii=False))
    print("run_oos_day_summary:", json.dumps({
        "exists": run_oos.get("exists"),
        "path": run_oos.get("path"),
        "name": run_oos.get("name"),
        "start_line": run_oos.get("start_line"),
        "end_line": run_oos.get("end_line"),
        "line_count": run_oos.get("line_count"),
        "args": run_oos.get("args"),
        "classification": run_oos.get("classification"),
        "action_shapes": run_oos.get("action_shapes"),
        "direct_adapter_provider_assessment": run_oos.get("direct_adapter_provider_assessment"),
    }, ensure_ascii=False))
    print("runtime_candidate_ranking_summary:", json.dumps({
        "real_runtime_candidate_count": runtime_candidates["real_runtime_candidate_count"],
        "top_candidates": runtime_candidates["ranked_real_runtime_candidates"][:10],
    }, ensure_ascii=False))
    print("baseline_summary:", json.dumps({
        "exists": baseline.get("exists"),
        "path": baseline.get("path"),
        "name": baseline.get("name"),
        "action_shapes": baseline.get("action_shapes"),
        "baseline_role": baseline.get("baseline_role"),
    }, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
