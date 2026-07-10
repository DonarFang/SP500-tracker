#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
import re
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

K2_R8 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R8_MARKET_STATE_PARAMETER_AUDIT.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md"
ARCH_MD = ROOT / "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_r9_market_state_115_return_artifact_audit.json"
PARAM_COMPARE_JSON = ROOT / "exports/e1r_engine/equivalence/e1r_k2_r9_115_return_market_state_parameter_compare.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
]

SEARCH_DIRS = [
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

TARGET_RETURN = 116.74
RETURN_TOLERANCE = 1.0


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


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDE_PARTS for part in path.parts)


def iter_candidate_files() -> list[Path]:
    files: list[Path] = []
    for base in SEARCH_DIRS:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if is_excluded(p):
                continue
            if not p.is_file():
                continue
            if p.suffix.lower() not in {".json", ".md", ".txt", ".csv"}:
                continue
            path_s = str(p).lower()
            if any(x in path_s for x in ["e1r", "backtest", "research", "engine"]):
                files.append(p)
    return sorted(set(files))


def safe_read_text(path: Path, limit: int = 8_000_000) -> str:
    try:
        data = path.read_bytes()
        if len(data) > limit:
            data = data[:limit]
        return data.decode("utf-8", errors="replace")
    except Exception:
        return ""


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


def value_as_float(v: Any) -> float | None:
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = v.strip().replace("%", "").replace("+", "")
        try:
            return float(s)
        except Exception:
            return None
    return None


def compact_value(v: Any, max_len: int = 1200) -> Any:
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


def extract_json_findings(path: Path, obj: Any) -> dict[str, Any]:
    flat = flatten_json(obj)
    metric_hits = []
    market_hits = []
    return_hits = []
    e1r_hits = []

    for row in flat:
        key_l = row["key"].lower()
        path_l = row["path"].lower()
        v = row["value"]

        if any(term in key_l for term in ["return", "alpha", "cagr", "drawdown", "sharpe", "profit_factor", "win_rate"]):
            metric_hits.append({
                "path": row["path"],
                "key": row["key"],
                "value": compact_value(v),
            })

        f = value_as_float(v)
        if f is not None and (abs(f - TARGET_RETURN) <= RETURN_TOLERANCE or 110 <= f <= 120):
            return_hits.append({
                "path": row["path"],
                "key": row["key"],
                "value": f,
                "distance_to_target_116_74": abs(f - TARGET_RETURN),
            })

        if any(term in path_l for term in ["market_gate", "market_state", "gate", "shock", "risk_off", "entry_capacity", "regime"]):
            market_hits.append({
                "path": row["path"],
                "key": row["key"],
                "value": compact_value(v),
            })

        if "e1r" in path_l or (isinstance(v, str) and "e1r" in v.lower()):
            e1r_hits.append({
                "path": row["path"],
                "key": row["key"],
                "value": compact_value(v),
            })

    top = {}
    if isinstance(obj, dict):
        for k in [
            "name", "version", "strategy_variant", "strategy_name", "strategy",
            "total_return_pct", "spx_total_return_pct", "alpha_pct",
            "cagr_pct", "max_drawdown_pct", "sharpe_ratio", "profit_factor",
            "number_of_trades", "orders", "strategy_controls", "market_entry_gate",
            "e1r_uptrend_execution_enabled", "e1r_regime_wiring_enabled",
            "sample_validity", "status",
        ]:
            if k in obj:
                top[k] = compact_value(obj[k])

    return {
        "path": rel(path),
        "sha256": sha256(path),
        "top_level": top,
        "return_hits": sorted(return_hits, key=lambda x: x["distance_to_target_116_74"])[:20],
        "metric_hits": metric_hits[:100],
        "market_hits": market_hits[:160],
        "e1r_hits": e1r_hits[:100],
        "counts": {
            "return_hits": len(return_hits),
            "metric_hits": len(metric_hits),
            "market_hits": len(market_hits),
            "e1r_hits": len(e1r_hits),
        },
    }


def score_json_finding(f: dict[str, Any]) -> int:
    score = 0
    if f["return_hits"]:
        best = f["return_hits"][0]["distance_to_target_116_74"]
        if best <= 0.01:
            score += 120
        elif best <= 0.25:
            score += 100
        elif best <= 1.0:
            score += 80
        else:
            score += 40

    path_l = f["path"].lower()
    if "e1r" in path_l:
        score += 20
    if "backtest" in path_l:
        score += 10
    if "result" in path_l or "summary" in path_l or "bundle" in path_l:
        score += 10
    if f["counts"]["market_hits"] > 0:
        score += 20
    if f["counts"]["e1r_hits"] > 0:
        score += 20

    top = f.get("top_level", {})
    tr = value_as_float(top.get("total_return_pct"))
    if tr is not None and abs(tr - TARGET_RETURN) <= RETURN_TOLERANCE:
        score += 80

    return score


def extract_text_findings(path: Path, text: str) -> dict[str, Any]:
    lower = text.lower()
    lines = text.splitlines()

    patterns = [
        r"116\.74",
        r"\+116",
        r"115",
        r"total_return",
        r"Total Return",
        r"E1R",
        r"market_gate",
        r"Market Gate",
        r"D3_RISK_OFF_PLUS_SHOCK_GATE",
        r"market_shock",
        r"risk_off",
        r"e1r_regime",
    ]

    hits = []
    for i, line in enumerate(lines, start=1):
        if any(re.search(p, line, flags=re.IGNORECASE) for p in patterns):
            hits.append({"line": i, "text": line[:1000]})
            if len(hits) >= 160:
                break

    score = 0
    if "116.74" in lower:
        score += 70
    if "total_return" in lower or "total return" in lower:
        score += 20
    if "e1r" in lower:
        score += 15
    if "market_gate" in lower or "market gate" in lower:
        score += 15
    if "d3_risk_off_plus_shock_gate".lower() in lower:
        score += 20

    return {
        "path": rel(path),
        "sha256": sha256(path),
        "score": score,
        "hits": hits,
        "counts": {"hits": len(hits)},
    }


def search_artifacts() -> dict[str, Any]:
    files = iter_candidate_files()
    json_findings = []
    text_findings = []

    for p in files:
        text = safe_read_text(p)
        if not text:
            continue

        if p.suffix.lower() == ".json":
            try:
                obj = json.loads(text)
                jf = extract_json_findings(p, obj)
                jf["score"] = score_json_finding(jf)
                if jf["score"] > 0 or jf["counts"]["return_hits"] or jf["counts"]["market_hits"]:
                    json_findings.append(jf)
                continue
            except Exception:
                pass

        tf = extract_text_findings(p, text)
        if tf["score"] > 0 or tf["hits"]:
            text_findings.append(tf)

    return {
        "searched_file_count": len(files),
        "json_findings": sorted(json_findings, key=lambda x: x["score"], reverse=True)[:80],
        "text_findings": sorted(text_findings, key=lambda x: x["score"], reverse=True)[:80],
    }


def load_best_json(path_s: str | None) -> Any | None:
    if not path_s:
        return None
    p = ROOT / path_s
    if not p.exists() or p.suffix.lower() != ".json":
        return None
    try:
        return read_json(p)
    except Exception:
        return None


def extract_metric_snapshot_from_obj(obj: Any) -> dict[str, Any]:
    flat = flatten_json(obj)
    wanted = {}
    for row in flat:
        key = row["key"]
        path = row["path"]
        lk = key.lower()
        lp = path.lower()

        if lk in {
            "total_return_pct", "spx_total_return_pct", "alpha_pct",
            "cagr_pct", "spx_cagr_pct", "max_drawdown_pct",
            "sharpe_ratio", "profit_factor", "win_rate_pct",
            "number_of_trades", "avg_holding_days", "exposure_pct",
            "status", "sample_validity", "strategy_variant", "version",
            "strategy_name", "name",
        }:
            wanted[path] = compact_value(row["value"])

        if "market_entry_gate" in lp or "strategy_controls" in lp or "market_gate" in lp:
            wanted[path] = compact_value(row["value"])

    return wanted


def compare_market_params(best_obj: Any, r8: dict[str, Any]) -> dict[str, Any]:
    r8_params = r8.get("parameter_audit", {}).get("market_gate_parameters", {})
    gm_controls = r8.get("parameter_audit", {}).get("golden_master_controls", {})

    best_flat = flatten_json(best_obj) if best_obj is not None else []

    def find_values_by_key_or_path(term: str) -> list[dict[str, Any]]:
        out = []
        for row in best_flat:
            if row["key"] == term or term.lower() in row["path"].lower():
                out.append({"path": row["path"], "value": compact_value(row["value"])})
        return out[:30]

    best_values = {
        "market_entry_gate": find_values_by_key_or_path("market_entry_gate"),
        "strategy_controls": find_values_by_key_or_path("strategy_controls"),
        "market_gate_enabled": find_values_by_key_or_path("market_gate_enabled"),
        "risk_off_below_spx_ma50": find_values_by_key_or_path("risk_off_below_spx_ma50"),
        "market_shock_gate_enabled": find_values_by_key_or_path("market_shock_gate_enabled"),
        "market_shock_daily_return": find_values_by_key_or_path("market_shock_daily_return"),
        "e1r_regime_wiring_enabled": find_values_by_key_or_path("e1r_regime_wiring_enabled"),
        "e1r_uptrend_execution_enabled": find_values_by_key_or_path("e1r_uptrend_execution_enabled"),
    }

    unresolved = []
    required = {
        "market_entry_gate",
        "market_gate_enabled",
        "risk_off_below_spx_ma50",
        "market_shock_gate_enabled",
        "market_shock_daily_return",
    }

    for key, vals in best_values.items():
        if not vals:
            unresolved.append({
                "id": f"full_115_artifact_missing_{key}",
                "field": key,
                "blocking_for_replication": key in required,
            })

    return {
        "r8_short_window_market_gate_parameters": r8_params,
        "r8_short_window_golden_master_controls": gm_controls,
        "full_115_artifact_values": best_values,
        "unresolved": unresolved,
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    if not K2_R8.exists():
        raise FileNotFoundError(f"Missing prerequisite: {rel(K2_R8)}")

    r8 = read_json(K2_R8)
    if r8.get("decision", {}).get("k2_r8_market_state_parameter_audit_passed") is not True:
        raise RuntimeError("K2-R8 did not pass.")

    search = search_artifacts()
    best_json = search["json_findings"][0] if search["json_findings"] else None
    best_text = search["text_findings"][0] if search["text_findings"] else None

    best_obj = load_best_json(best_json["path"] if best_json else None)
    metric_snapshot = extract_metric_snapshot_from_obj(best_obj) if best_obj is not None else {}
    param_compare = compare_market_params(best_obj, r8) if best_obj is not None else {
        "r8_short_window_market_gate_parameters": r8.get("parameter_audit", {}).get("market_gate_parameters", {}),
        "full_115_artifact_values": {},
        "unresolved": [{"id": "no_parseable_json_115_artifact_found", "blocking_for_replication": True}],
    }

    json_artifact_found = False
    target_return_verified = False
    if best_json:
        for hit in best_json.get("return_hits", []):
            if abs(hit.get("value", 999999) - TARGET_RETURN) <= RETURN_TOLERANCE:
                json_artifact_found = True
                target_return_verified = True
                break

    text_artifact_found = bool(best_text and best_text.get("score", 0) >= 50)

    unresolved = []
    if not json_artifact_found:
        unresolved.append({
            "id": "parseable_json_artifact_for_116_74_not_found",
            "blocking_for_replication": True,
            "best_json": compact_value(best_json),
        })

    if not target_return_verified:
        unresolved.append({
            "id": "target_return_116_74_not_verified_in_parseable_json",
            "target_return": TARGET_RETURN,
            "tolerance": RETURN_TOLERANCE,
            "blocking_for_replication": True,
        })

    unresolved.extend(param_compare.get("unresolved", []))

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

    validations = {
        "market_state_115_return_artifact_audit_complete": True,
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
        "k2_r8_loaded": True,
        "repo_artifacts_searched": search["searched_file_count"] > 0,
        "json_artifact_found": json_artifact_found,
        "text_artifact_found": text_artifact_found,
        "target_return_116_74_verified": target_return_verified,
        "metric_snapshot_extracted": bool(metric_snapshot),
        "market_param_compare_complete": True,
        "unresolved_count": len(unresolved),
    }

    replication_ready = all([
        validations["json_artifact_found"],
        validations["target_return_116_74_verified"],
        len([x for x in unresolved if x.get("blocking_for_replication")]) == 0,
    ])

    decision = {
        "k2_r9_market_state_115_return_artifact_audit_passed": validations["repo_artifacts_searched"],
        "full_115_artifact_verified": validations["json_artifact_found"] and validations["target_return_116_74_verified"],
        "market_state_115_replication_ready": replication_ready,
        "formula_patch_allowed_now": False,
        "candidate_extraction_allowed_now": False,
        "implementation_may_resume": False,
        "unresolved": unresolved,
        "next_required_stage_if_ready": "4C-2C-4E-ENGINE-K2-R10-MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL",
        "next_required_stage_if_not_ready": "4C-2C-4E-ENGINE-K2-R9B-115_RETURN_ARTIFACT_RECOVERY",
        "conclusion": (
            "K2_R9_PASS_115_ARTIFACT_VERIFIED_READY_FOR_REPLICATION_PROPOSAL"
            if replication_ready
            else "K2_R9_AUDIT_COMPLETE_NEEDS_115_ARTIFACT_RECOVERY_OR_PARAM_EVIDENCE"
        ),
        "recommended_next_action": (
            "If the 116.74% JSON artifact and market parameters are verified, proceed to replication proposal. "
            "If not, recover the exact E1R 115% artifact or run only an artifact-producing audit, not optimization."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R9-MARKET_STATE_115_RETURN_ARTIFACT_AUDIT",
        "status": "MARKET_STATE_115_RETURN_ARTIFACT_AUDIT_COMPLETE",
        "purpose": "Find and audit the exact E1R ~116.74% full-run artifact and its market-state/gate assumptions before standalone replication.",
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
            "k2_r8": rel(K2_R8),
            "search_dirs": [rel(p) for p in SEARCH_DIRS],
            "searched_file_count": search["searched_file_count"],
        },
        "artifact_candidates": {
            "best_json": best_json,
            "best_text": best_text,
            "top_json": search["json_findings"][:10],
            "top_text": search["text_findings"][:10],
        },
        "selected_artifact": best_json,
        "selected_artifact_metric_snapshot": metric_snapshot,
        "market_parameter_compare": param_compare,
        "unresolved": unresolved,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)
    write_json(PARAM_COMPARE_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R9 — Market State 115 Return Artifact Audit")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append(report["purpose"])
    md.append("")
    md.append("## Selected Artifact")
    md.append("```json")
    md.append(json.dumps(best_json, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Metric Snapshot")
    md.append("```json")
    md.append(json.dumps(metric_snapshot, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Market Parameter Compare")
    md.append("```json")
    md.append(json.dumps(param_compare, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Top Artifact Candidates")
    md.append("```json")
    md.append(json.dumps(report["artifact_candidates"], indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_ENGINE_K2_R9_MARKET_STATE_115_RETURN_ARTIFACT_AUDIT_COMPLETE")
    print("status:", report["status"])
    print("searched_file_count:", search["searched_file_count"])
    print("selected_artifact:", json.dumps(best_json, ensure_ascii=False))
    print("selected_artifact_metric_snapshot:", json.dumps(metric_snapshot, ensure_ascii=False))
    print("market_parameter_compare:", json.dumps(param_compare, ensure_ascii=False))
    print("unresolved:", json.dumps(unresolved, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(AUDIT_JSON))
    print("wrote:", rel(PARAM_COMPARE_JSON))


if __name__ == "__main__":
    main()
