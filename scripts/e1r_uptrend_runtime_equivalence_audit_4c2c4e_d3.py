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

D2B_REPORT = ROOT / "docs/research/E1R_4C2C4E_D2B_REAL_UPTREND_PROVIDER_FILTER_AUDIT.json"
D2_REPORT = ROOT / "docs/research/E1R_4C2C4E_D2_UPTREND_PROVIDER_CANDIDATE_VERIFICATION.json"
D1_REPORT = ROOT / "docs/research/E1R_4C2C4E_D1_UPTREND_PROVIDER_ENTRYPOINT_AUDIT.json"
D_REPORT = ROOT / "docs/research/E1R_4C2C4E_D_CONTINUOUS_STATEFUL_ADAPTER_DESIGN.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_D3_UPTREND_RUNTIME_EQUIVALENCE_AUDIT.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_D3_UPTREND_RUNTIME_EQUIVALENCE_AUDIT.md"

BACKTEST_PATH = ROOT / "src/engine/backtest.py"
TRACKING_ENGINE_PATH = ROOT / "src/oos/tracking_engine.py"
TRADE_DECISION_PATH = ROOT / "src/engine/trade_decision.py"
SIDECAR_PATH = ROOT / "src/engine/e1r_sidecar_sleeve.py"
COMPOSER_PATH = ROOT / "src/engine/e1r_composer.py"

FROZEN_STRATEGY_FILES = [
    BACKTEST_PATH,
    SIDECAR_PATH,
    COMPOSER_PATH,
]

INVALID_ARTIFACTS = [
    "exports/e1r_unified_5y_full_account_v1_result.json",
    "exports/e1r_unified_5y_dashboard_research_bundle.json",
    "exports/e1r_combined_5y_original_max3_result.json",
    "exports/e1r_combined_5y_original_max3_equity_curve.json",
    "exports/e1r_combined_5y_original_max3_summary.json",
]

EQUIVALENCE_DIMENSIONS = [
    "candidate_generation",
    "candidate_ranking",
    "buy_rule",
    "exit_rule",
    "add_rule",
    "reduce_rule",
    "hold_rule",
    "market_gate",
    "max_positions",
    "position_sizing",
    "cash_state",
    "position_state",
    "daily_mark_to_market",
    "order_schema",
    "signal_date_execute_date_convention",
    "historical_replay_compatibility",
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

def line_window(lines: list[str], line_no: int, before: int = 8, after: int = 14) -> list[dict[str, Any]]:
    start = max(1, line_no - before)
    end = min(len(lines), line_no + after)
    return [{"line": i, "text": lines[i - 1][:340]} for i in range(start, end + 1)]

def get_function(path: Path, name: str) -> dict[str, Any] | None:
    if not path.exists():
        return None
    text = read_text(path)
    lines = text.splitlines()
    try:
        tree = ast.parse(text)
    except Exception:
        return None

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
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
        if keyset.intersection({
            "action", "symbol", "date", "reason", "reasons", "shares", "qty",
            "quantity", "branch", "order_type", "signal_date", "execute_date",
            "entry_rank", "leader_score", "rs_score"
        }):
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

def static_features(fn: dict[str, Any] | None) -> dict[str, Any]:
    if fn is None:
        return {"exists": False}

    s = fn["source"]
    lower = s.lower()
    args = fn["args"]

    return {
        "exists": True,
        "path": fn["path"],
        "name": fn["name"],
        "args": args,
        "line_count": fn["line_count"],
        "has_candidate_terms": any(x in lower for x in ["candidate", "leaders", "leader_score", "rank", "qualified", "score"]),
        "takes_precomputed_leaders": "leaders" in args,
        "generates_leaders_from_prices_map": "prices_map" in args and ("leader_score" in lower or "rank" in lower),
        "has_buy_logic": "BUY" in s or "buy_size" in s,
        "has_add_logic": "ADD" in s or "add_size" in s,
        "has_reduce_logic": "REDUCE" in s or "reduce_size" in s,
        "has_exit_logic": "EXIT" in s or "sell_size" in s or "ls60_exit_mode" in s,
        "has_hold_logic": "HOLD" in s,
        "has_market_gate": "market_gate" in s or "gate_allowed" in s or "risk_off" in s,
        "takes_market_state": "market_state" in args,
        "has_max_positions": "max_positions" in s or "entry_top_n" in s or "open_positions_count" in s,
        "has_open_positions_count": "open_positions_count" in s,
        "has_cash_state": "cash" in s,
        "has_positions_state": "positions" in s,
        "has_total_equity": "total_equity" in s or "equity" in s,
        "has_daily_mark_to_market": ("mark" in lower and "market" in lower) or ("holdings_value" in s and "equity" in s),
        "has_signal_execute_dates": "signal_date" in s and "execute_date" in s,
        "references_invalid_artifacts": any(p in s for p in INVALID_ARTIFACTS),
        "calls_run_stateful_simulation": "run_stateful_simulation" in s and fn["name"] != "run_stateful_simulation",
        "writes_files_or_state": any(x in s for x in [".write_text", "open(", "save", "export_all", "append_event", "write_json"]),
        "imports_or_uses_oos_state": any(x in s for x in ["PortfolioState", "rebuild_from_events", "events", "state"]),
        "contains_sidecar": "sidecar" in lower,
    }

def keyword_contexts(fn: dict[str, Any] | None) -> dict[str, list[dict[str, Any]]]:
    if fn is None:
        return {}

    terms = {
        "candidate_generation": ["leaders", "candidate", "leader_score", "rank", "qualified", "score"],
        "buy_logic": ["BUY", "buy_size", "total_cost", "units"],
        "exit_logic": ["EXIT", "sell_size", "ls60_exit_mode", "signal_reason"],
        "add_reduce_hold_logic": ["ADD", "REDUCE", "HOLD", "add_size", "reduce_size"],
        "market_gate": ["market_gate", "gate_allowed", "risk_off", "market_state"],
        "max_positions": ["max_positions", "entry_top_n", "open_positions_count", "n_positions"],
        "state": ["cash", "positions", "equity", "holdings_value", "PortfolioState"],
        "dates": ["signal_date", "execute_date", "data_date"],
    }

    out = {}
    source_lines = fn["source"].splitlines()
    lines = fn["lines"]
    start = fn["start_line"]

    for group, group_terms in terms.items():
        hits = []
        for idx, line in enumerate(source_lines, start=start):
            if any(t in line for t in group_terms):
                hits.append({
                    "line": idx,
                    "text": line.strip()[:360],
                    "context": line_window(lines, idx, 5, 10),
                })
        out[group] = hits[:50]

    return out

def load_prior_reports() -> dict[str, Any]:
    out = {
        "d_exists": D_REPORT.exists(),
        "d1_exists": D1_REPORT.exists(),
        "d2_exists": D2_REPORT.exists(),
        "d2b_exists": D2B_REPORT.exists(),
        "d2b_decision": None,
        "d2b_candidate": None,
    }

    if D2B_REPORT.exists():
        d2b = read_json(D2B_REPORT)
        out["d2b_decision"] = d2b.get("decision")
        out["d2b_candidate"] = d2b.get("decision", {}).get("candidate_for_next_equivalence_audit")
    return out

def compare_equivalence_dimensions(
    baseline_features: dict[str, Any],
    candidate_features: dict[str, Any],
    baseline_actions: dict[str, Any],
    candidate_actions: dict[str, Any],
) -> dict[str, Any]:
    matrix = {}

    def same_bool(key: str) -> bool:
        return bool(baseline_features.get(key)) == bool(candidate_features.get(key))

    matrix["candidate_generation"] = {
        "baseline": {
            "has_candidate_terms": baseline_features.get("has_candidate_terms"),
            "generates_leaders_from_prices_map": baseline_features.get("generates_leaders_from_prices_map"),
            "takes_precomputed_leaders": baseline_features.get("takes_precomputed_leaders"),
        },
        "candidate": {
            "has_candidate_terms": candidate_features.get("has_candidate_terms"),
            "generates_leaders_from_prices_map": candidate_features.get("generates_leaders_from_prices_map"),
            "takes_precomputed_leaders": candidate_features.get("takes_precomputed_leaders"),
        },
        "equivalent": (
            baseline_features.get("generates_leaders_from_prices_map") is True
            and candidate_features.get("takes_precomputed_leaders") is False
        ),
        "risk": "Candidate takes precomputed leaders rather than generating the same historical candidate universe." if candidate_features.get("takes_precomputed_leaders") else None,
    }

    matrix["buy_rule"] = {
        "baseline_has_buy": baseline_features.get("has_buy_logic"),
        "candidate_has_buy": candidate_features.get("has_buy_logic"),
        "baseline_literal_actions": baseline_actions.get("literal_action_counts"),
        "candidate_literal_actions": candidate_actions.get("literal_action_counts"),
        "equivalent": same_bool("has_buy_logic"),
    }

    matrix["exit_rule"] = {
        "baseline_has_exit": baseline_features.get("has_exit_logic"),
        "candidate_has_exit": candidate_features.get("has_exit_logic"),
        "equivalent": same_bool("has_exit_logic"),
    }

    matrix["add_rule"] = {
        "baseline_has_add": baseline_features.get("has_add_logic"),
        "candidate_has_add": candidate_features.get("has_add_logic"),
        "equivalent": same_bool("has_add_logic"),
    }

    matrix["reduce_rule"] = {
        "baseline_has_reduce": baseline_features.get("has_reduce_logic"),
        "candidate_has_reduce": candidate_features.get("has_reduce_logic"),
        "equivalent": same_bool("has_reduce_logic"),
    }

    matrix["hold_rule"] = {
        "baseline_has_hold": baseline_features.get("has_hold_logic"),
        "candidate_has_hold": candidate_features.get("has_hold_logic"),
        "equivalent": same_bool("has_hold_logic"),
    }

    matrix["market_gate"] = {
        "baseline_has_market_gate": baseline_features.get("has_market_gate"),
        "candidate_has_market_gate": candidate_features.get("has_market_gate"),
        "candidate_takes_market_state": candidate_features.get("takes_market_state"),
        "equivalent": baseline_features.get("has_market_gate") == candidate_features.get("has_market_gate"),
        "risk": "Candidate accepts market_state but does not show same market-gate implementation." if candidate_features.get("takes_market_state") and not candidate_features.get("has_market_gate") else None,
    }

    matrix["max_positions"] = {
        "baseline_has_max_positions": baseline_features.get("has_max_positions"),
        "candidate_has_max_positions": candidate_features.get("has_max_positions"),
        "baseline_has_open_positions_count": baseline_features.get("has_open_positions_count"),
        "candidate_has_open_positions_count": candidate_features.get("has_open_positions_count"),
        "equivalent": baseline_features.get("has_max_positions") == candidate_features.get("has_max_positions"),
    }

    matrix["position_sizing"] = {
        "baseline_action_keys_sample": baseline_actions.get("samples", [])[:8],
        "candidate_action_keys_sample": candidate_actions.get("samples", [])[:8],
        "equivalent": False,
        "risk": "Position sizing cannot be assumed equivalent from static schema; requires explicit mapping or replay comparison.",
    }

    matrix["state_ownership"] = {
        "baseline_cash": baseline_features.get("has_cash_state"),
        "baseline_positions": baseline_features.get("has_positions_state"),
        "candidate_cash": candidate_features.get("has_cash_state"),
        "candidate_positions": candidate_features.get("has_positions_state"),
        "candidate_uses_oos_state": candidate_features.get("imports_or_uses_oos_state"),
        "equivalent": (
            baseline_features.get("has_cash_state") == candidate_features.get("has_cash_state")
            and baseline_features.get("has_positions_state") == candidate_features.get("has_positions_state")
        ),
    }

    matrix["historical_replay_compatibility"] = {
        "candidate_writes_files_or_state": candidate_features.get("writes_files_or_state"),
        "candidate_imports_or_uses_oos_state": candidate_features.get("imports_or_uses_oos_state"),
        "candidate_references_invalid_artifacts": candidate_features.get("references_invalid_artifacts"),
        "equivalent": (
            candidate_features.get("references_invalid_artifacts") is False
            and candidate_features.get("writes_files_or_state") is False
            and candidate_features.get("imports_or_uses_oos_state") is False
        ),
        "risk": "OOS candidate may depend on forward event/state model; adapter historical replay should own account state.",
    }

    equivalent_count = sum(1 for v in matrix.values() if v.get("equivalent") is True)
    total_count = len(matrix)
    failed = {k: v for k, v in matrix.items() if v.get("equivalent") is not True}

    return {
        "matrix": matrix,
        "equivalent_count": equivalent_count,
        "total_count": total_count,
        "failed_dimensions": failed,
        "all_equivalent": equivalent_count == total_count,
    }

def audit_trade_decision_helpers() -> dict[str, Any]:
    helpers = []
    for name in ["trade_action", "trade_action_reason"]:
        fn = get_function(TRADE_DECISION_PATH, name)
        helpers.append({
            "name": name,
            "exists": fn is not None,
            "features": static_features(fn),
            "action_shapes": extract_action_shapes(fn),
            "contexts": keyword_contexts(fn),
        })
    return {
        "path": rel(TRADE_DECISION_PATH) if TRADE_DECISION_PATH.exists() else None,
        "helpers": helpers,
        "interpretation": (
            "trade_decision helpers may be reusable as pure rule helpers, but they do not own candidate ranking, "
            "cash, positions, max_positions, or market gate. They are not a full UPTREND provider by themselves."
        ),
    }

def derive_decision(equivalence: dict[str, Any], candidate_features: dict[str, Any]) -> dict[str, Any]:
    hard_fail_reasons = []

    failed = equivalence["failed_dimensions"]

    for dim in [
        "candidate_generation",
        "add_rule",
        "reduce_rule",
        "hold_rule",
        "market_gate",
        "max_positions",
        "position_sizing",
        "historical_replay_compatibility",
    ]:
        if dim in failed:
            hard_fail_reasons.append(dim)

    if candidate_features.get("takes_precomputed_leaders"):
        hard_fail_reasons.append("candidate_requires_precomputed_leaders")
    if not candidate_features.get("has_market_gate"):
        hard_fail_reasons.append("candidate_lacks_same_market_gate")
    if not candidate_features.get("has_max_positions"):
        hard_fail_reasons.append("candidate_lacks_max_positions_guard")
    if not candidate_features.get("has_reduce_logic"):
        hard_fail_reasons.append("candidate_lacks_reduce_logic")
    if not candidate_features.get("has_hold_logic"):
        hard_fail_reasons.append("candidate_lacks_hold_logic")

    if equivalence["all_equivalent"] and not hard_fail_reasons:
        conclusion = "RUN_OOS_DAY_EQUIVALENT_PROVIDER_READY_FOR_CONTROLLED_SMOKE"
        next_action = (
            "Proceed to controlled adapter smoke using run_oos_day as UPTREND provider candidate."
        )
        provider_locked = True
        implementation_allowed_now = False
    else:
        conclusion = "RUN_OOS_DAY_NOT_EQUIVALENT_USE_RUN_STATEFUL_EXTRACTION_PLAN"
        next_action = (
            "Proceed to 4C-2C-4E-D4: no-strategy-change UPTREND provider extraction design from "
            "src/engine/backtest.py::run_stateful_simulation. Do not use run_oos_day as adapter provider."
        )
        provider_locked = False
        implementation_allowed_now = False

    return {
        "uptrend_provider_locked": provider_locked,
        "implementation_allowed_now": implementation_allowed_now,
        "run_oos_day_equivalence_passed": equivalence["all_equivalent"],
        "hard_fail_reasons": sorted(set(hard_fail_reasons)),
        "conclusion": conclusion,
        "recommended_next_action": next_action,
        "engineering_rule": (
            "Correct trading logic has priority over code reuse. A helper that lacks candidate generation, market gate, "
            "max-position guard, sizing equivalence, or historical replay compatibility cannot be used as the official "
            "UPTREND provider."
        ),
    }

def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    prior = load_prior_reports()

    baseline_fn = get_function(BACKTEST_PATH, "run_stateful_simulation")
    candidate_fn = get_function(TRACKING_ENGINE_PATH, "run_oos_day")

    baseline_features = static_features(baseline_fn)
    candidate_features = static_features(candidate_fn)

    baseline_actions = extract_action_shapes(baseline_fn)
    candidate_actions = extract_action_shapes(candidate_fn)

    baseline_contexts = keyword_contexts(baseline_fn)
    candidate_contexts = keyword_contexts(candidate_fn)

    equivalence = compare_equivalence_dimensions(
        baseline_features=baseline_features,
        candidate_features=candidate_features,
        baseline_actions=baseline_actions,
        candidate_actions=candidate_actions,
    )

    trade_decision_helpers = audit_trade_decision_helpers()
    decision = derive_decision(equivalence, candidate_features)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "audit_only_no_full_5y": True,
        "backtest_engine_full_run": False,
        "candidate_runtime_execution_run": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "invalid_artifacts_not_used_as_source": True,
        "composer_not_used": True,
        "return_curve_stitching_not_used": True,
        "d2b_report_loaded": prior["d2b_exists"],
        "baseline_function_loaded": baseline_fn is not None,
        "candidate_function_loaded": candidate_fn is not None,
        "equivalence_matrix_generated": bool(equivalence["matrix"]),
        "trade_decision_helpers_audited": True,
        "provider_not_locked_if_equivalence_failed": (
            decision["uptrend_provider_locked"] is False
            if decision["run_oos_day_equivalence_passed"] is False
            else True
        ),
        "implementation_not_allowed_yet": decision["implementation_allowed_now"] is False,
        "decision_generated": bool(decision["conclusion"]),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-D3",
        "status": "UPTREND_RUNTIME_EQUIVALENCE_AUDIT_COMPLETE",
        "purpose": "Audit whether src/oos/tracking_engine.py::run_oos_day is equivalent to src/engine/backtest.py::run_stateful_simulation for official UPTREND provider use.",
        "policy": {
            "strategy_logic_changed": False,
            "backtest_engine_full_run": False,
            "candidate_runtime_execution_run": False,
            "full_5y_backtest_run": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
            "invalid_artifacts_used_as_source": False,
            "composer_used": False,
            "return_curve_stitching_used": False,
        },
        "prior_reports": prior,
        "baseline": {
            "path": baseline_features.get("path"),
            "name": baseline_features.get("name"),
            "start_line": baseline_fn.get("start_line") if baseline_fn else None,
            "end_line": baseline_fn.get("end_line") if baseline_fn else None,
            "line_count": baseline_features.get("line_count"),
            "features": baseline_features,
            "action_shapes": baseline_actions,
            "contexts": baseline_contexts,
        },
        "candidate": {
            "path": candidate_features.get("path"),
            "name": candidate_features.get("name"),
            "start_line": candidate_fn.get("start_line") if candidate_fn else None,
            "end_line": candidate_fn.get("end_line") if candidate_fn else None,
            "line_count": candidate_features.get("line_count"),
            "features": candidate_features,
            "action_shapes": candidate_actions,
            "contexts": candidate_contexts,
        },
        "equivalence": equivalence,
        "trade_decision_helpers": trade_decision_helpers,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-D3 — UPTREND Runtime Equivalence Audit")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("Audit whether `src/oos/tracking_engine.py::run_oos_day` is equivalent to `src/engine/backtest.py::run_stateful_simulation` for official UPTREND provider use.")
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
    md.append("## Baseline Summary")
    md.append("```json")
    md.append(json.dumps({
        "path": report["baseline"]["path"],
        "name": report["baseline"]["name"],
        "line_count": report["baseline"]["line_count"],
        "features": report["baseline"]["features"],
        "action_shapes": report["baseline"]["action_shapes"],
    }, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Candidate Summary")
    md.append("```json")
    md.append(json.dumps({
        "path": report["candidate"]["path"],
        "name": report["candidate"]["name"],
        "line_count": report["candidate"]["line_count"],
        "features": report["candidate"]["features"],
        "action_shapes": report["candidate"]["action_shapes"],
    }, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Equivalence Matrix")
    md.append("```json")
    md.append(json.dumps(equivalence, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Trade Decision Helpers")
    md.append("```json")
    md.append(json.dumps({
        "path": trade_decision_helpers["path"],
        "interpretation": trade_decision_helpers["interpretation"],
        "helpers": [
            {
                "name": h["name"],
                "exists": h["exists"],
                "features": h["features"],
                "action_shapes": h["action_shapes"],
            }
            for h in trade_decision_helpers["helpers"]
        ],
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

    print("E1R_4C2C4E_D3_UPTREND_RUNTIME_EQUIVALENCE_AUDIT_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("baseline_summary:", json.dumps({
        "path": report["baseline"]["path"],
        "name": report["baseline"]["name"],
        "start_line": report["baseline"]["start_line"],
        "end_line": report["baseline"]["end_line"],
        "line_count": report["baseline"]["line_count"],
        "features": report["baseline"]["features"],
        "action_shapes": report["baseline"]["action_shapes"],
    }, ensure_ascii=False))
    print("candidate_summary:", json.dumps({
        "path": report["candidate"]["path"],
        "name": report["candidate"]["name"],
        "start_line": report["candidate"]["start_line"],
        "end_line": report["candidate"]["end_line"],
        "line_count": report["candidate"]["line_count"],
        "features": report["candidate"]["features"],
        "action_shapes": report["candidate"]["action_shapes"],
    }, ensure_ascii=False))
    print("equivalence_summary:", json.dumps({
        "equivalent_count": equivalence["equivalent_count"],
        "total_count": equivalence["total_count"],
        "all_equivalent": equivalence["all_equivalent"],
        "failed_dimensions": list(equivalence["failed_dimensions"].keys()),
    }, ensure_ascii=False))
    print("trade_decision_helpers_summary:", json.dumps({
        "path": trade_decision_helpers["path"],
        "interpretation": trade_decision_helpers["interpretation"],
        "helpers": [
            {
                "name": h["name"],
                "exists": h["exists"],
                "features": h["features"],
                "action_shapes": h["action_shapes"],
            }
            for h in trade_decision_helpers["helpers"]
        ],
    }, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
