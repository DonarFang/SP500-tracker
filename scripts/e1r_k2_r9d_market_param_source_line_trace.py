#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
import re
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

RCA2 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_RCA2_MARKET_PARAM_EVIDENCE_CHAIN_REVIEW.json"
R9C = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9C_115_RETURN_GENERATOR_TRACE.json"
R8 = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R8_MARKET_STATE_PARAMETER_AUDIT.json"
TARGET_ARTIFACT = ROOT / "exports/e1r_v0_2_backtest_summary.json"
GENERATOR_TRACE = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0D_GENERATOR_PATH_TRACE.json"

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9D_MARKET_PARAM_SOURCE_LINE_TRACE.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_K2_R9D_MARKET_PARAM_SOURCE_LINE_TRACE.md"
ARCH_MD = ROOT / "docs/architecture/E1R_4C2C4E_ENGINE_K2_R9D_MARKET_PARAM_SOURCE_LINE_TRACE.md"
AUDIT_JSON = ROOT / "exports/e1r_engine/audit/e1r_k2_r9d_market_param_source_line_trace.json"
EVIDENCE_JSON = ROOT / "exports/e1r_engine/equivalence/e1r_k2_r9d_market_param_source_line_trace_evidence.json"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "src/engine/e1r_composer.py",
]

PRIMARY_SOURCE_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

PREFERRED_ORIGINAL_TRACE_PREFIXES = [
    "docs/research/E1R_V0_2_STAGE3_",
    "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_",
]

POLLUTED_PREFIXES = [
    "docs/research/E1R_4C2C4E_ENGINE_K2_",
    "docs/architecture/E1R_4C2C4E_ENGINE_K2_",
    "exports/e1r_engine/audit/",
    "exports/e1r_engine/equivalence/",
    "scripts/e1r_k2_r9",
    "scripts/e1r_k2_rca",
]

REQUIRED_FIELDS = [
    "market_gate_enabled",
    "risk_off_below_spx_ma50",
    "market_shock_gate_enabled",
    "market_shock_daily_return",
    "market_entry_gate_or_equivalent",
    "e1r_v0_2_core_call_chain",
    "e1r_v0_2_sidecar_call_chain",
]

FIELD_PATTERNS = {
    "market_gate_enabled": [
        r'market_gate_enabled\s*=\s*bool\(a\.get\("market_gate_enabled"',
        r'"market_gate_enabled"\s*:\s*True',
        r'"market_gate_enabled"\s*:\s*true',
    ],
    "risk_off_below_spx_ma50": [
        r'risk_off_below_spx_ma50\s*=\s*bool\(a\.get\("risk_off_below_spx_ma50"',
        r'"risk_off_below_spx_ma50"\s*:\s*True',
        r'"risk_off_below_spx_ma50"\s*:\s*true',
    ],
    "market_shock_gate_enabled": [
        r'market_shock_gate_enabled\s*=\s*bool\(a\.get\("market_shock_gate_enabled"',
        r'"market_shock_gate_enabled"\s*:\s*True',
        r'"market_shock_gate_enabled"\s*:\s*true',
    ],
    "market_shock_daily_return": [
        r'market_shock_daily_return\s*=\s*float\(a\.get\("market_shock_daily_return"',
        r'"market_shock_daily_return"\s*:\s*-0\.02',
        r'market_shock_daily_return.*-0\.02',
    ],
    "market_entry_gate_or_equivalent": [
        r'_gate_state\s*=',
        r'market_entry_allowed\s*=',
        r'entry_capacity\s*>',
        r'blocked_actions',
        r'unaffected_actions',
        r'entry_capacity',
    ],
    "e1r_v0_2_core_call_chain": [
        r'run_stateful_simulation',
        r'core_variant_result',
        r'_core_e1r',
        r'compose_e1r_v0_2_variant',
        r'E1R_REGIME_AWARE_V0_2',
    ],
    "e1r_v0_2_sidecar_call_chain": [
        r'build_e1r_sidecar_sleeve',
        r'sidecar_result',
        r'_sidecar_result',
        r'compose_e1r_v0_2_variant',
        r'MA_CONFLICT',
        r'allowed_subclasses',
        r'gross_exposure',
    ],
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


def safe_text(path: Path, limit: int = 12_000_000) -> str:
    try:
        data = path.read_bytes()
        if len(data) > limit:
            data = data[:limit]
        return data.decode("utf-8", errors="replace")
    except Exception:
        return ""


def compact(v: Any, max_len: int = 2400) -> Any:
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


def is_polluted_path(path_s: str) -> bool:
    return any(path_s.startswith(prefix) for prefix in POLLUTED_PREFIXES)


def is_preferred_original_trace(path_s: str) -> bool:
    return any(path_s.startswith(prefix) for prefix in PREFERRED_ORIGINAL_TRACE_PREFIXES)


def classify_source(path_s: str) -> str:
    if is_polluted_path(path_s):
        return "POLLUTED_GENERATED_AUDIT"
    if path_s in {"src/engine/backtest.py", "src/engine/e1r_composer.py", "src/engine/e1r_sidecar_sleeve.py"}:
        return "PRIMARY_SOURCE_CODE"
    if is_preferred_original_trace(path_s):
        return "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT"
    if path_s.startswith("scripts/") and not path_s.startswith("scripts/e1r_k2_"):
        return "SCRIPT_SOURCE"
    if path_s.startswith("docs/research/"):
        return "RESEARCH_ARTIFACT_UNCLASSIFIED"
    return "OTHER"


def context_lines(path: Path, line_no: int, before: int = 4, after: int = 4) -> list[dict[str, Any]]:
    lines = safe_text(path).splitlines()
    if not lines:
        return []
    start = max(1, line_no - before)
    end = min(len(lines), line_no + after)
    return [
        {"line": i, "text": lines[i - 1][:1600]}
        for i in range(start, end + 1)
    ]


def grep_file_for_patterns(path: Path, field: str, patterns: list[str]) -> list[dict[str, Any]]:
    text = safe_text(path)
    if not text:
        return []

    hits = []
    for i, line in enumerate(text.splitlines(), start=1):
        for pat in patterns:
            if re.search(pat, line):
                path_s = rel(path)
                hits.append({
                    "field": field,
                    "source_path": path_s,
                    "source_class": classify_source(path_s),
                    "line": i,
                    "matched_pattern": pat,
                    "line_text": line[:1600],
                    "context": context_lines(path, i),
                })
                break
    return hits


def collect_primary_source_evidence() -> dict[str, list[dict[str, Any]]]:
    evidence = {field: [] for field in REQUIRED_FIELDS}
    for p in PRIMARY_SOURCE_FILES:
        if not p.exists():
            continue
        for field, patterns in FIELD_PATTERNS.items():
            evidence[field].extend(grep_file_for_patterns(p, field, patterns))
    return evidence


def flatten(obj: Any, prefix: str = "") -> list[dict[str, Any]]:
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else str(k)
            out.append({"path": p, "key": str(k), "value": v})
            out.extend(flatten(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:30000]):
            p = f"{prefix}[{i}]"
            out.append({"path": p, "key": f"[{i}]", "value": v})
            out.extend(flatten(v, p))
    return out


def extract_trace_candidate_paths(trace_obj: Any) -> list[str]:
    paths = []
    for row in flatten(trace_obj):
        v = row["value"]
        if isinstance(v, str):
            texts = [v]
        else:
            try:
                texts = [json.dumps(v, ensure_ascii=False)]
            except Exception:
                texts = [repr(v)]
        for text in texts:
            for m in re.findall(r'(?:docs|scripts|src|exports)/[\w./-]+\.(?:json|md|py)', text):
                if m not in paths and not is_polluted_path(m):
                    paths.append(m)
    return paths


def extract_source_head_rows_from_trace_files(paths: list[str]) -> dict[str, list[dict[str, Any]]]:
    evidence = {field: [] for field in REQUIRED_FIELDS}

    for path_s in paths:
        p = ROOT / path_s
        if not p.exists() or is_polluted_path(path_s):
            continue
        if not (is_preferred_original_trace(path_s) or path_s.startswith("src/") or path_s.startswith("scripts/")):
            continue

        text = safe_text(p)
        if not text:
            continue

        # Direct line/context evidence from trace/source-head files.
        for field, patterns in FIELD_PATTERNS.items():
            direct_hits = grep_file_for_patterns(p, field, patterns)
            for h in direct_hits:
                h["source_class"] = classify_source(path_s)
                evidence[field].append(h)

        # If JSON has explicit source_head / source / text values, search inside them too.
        if p.suffix.lower() == ".json":
            try:
                obj = json.loads(text)
            except Exception:
                continue
            for row in flatten(obj):
                key = row["key"].lower()
                value = row["value"]
                if key not in {"source_head", "source", "text", "source_text", "context"}:
                    continue
                value_s = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
                for field, patterns in FIELD_PATTERNS.items():
                    for pat in patterns:
                        if re.search(pat, value_s):
                            evidence[field].append({
                                "field": field,
                                "source_path": path_s,
                                "source_class": classify_source(path_s),
                                "json_path": row["path"],
                                "matched_pattern": pat,
                                "line_text": compact(value_s),
                                "context": [],
                            })
                            break

    return evidence


def merge_evidence(*parts: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    merged = {field: [] for field in REQUIRED_FIELDS}
    seen = set()
    for part in parts:
        for field, rows in part.items():
            for r in rows:
                key = (
                    field,
                    r.get("source_path"),
                    r.get("line"),
                    r.get("json_path"),
                    r.get("matched_pattern"),
                    r.get("line_text"),
                )
                if key in seen:
                    continue
                seen.add(key)
                merged[field].append(r)
    return merged


def evidence_quality_score(row: dict[str, Any]) -> int:
    cls = row.get("source_class")
    if cls == "PRIMARY_SOURCE_CODE":
        return 100
    if cls == "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT":
        return 75
    if cls == "SCRIPT_SOURCE":
        return 60
    if cls == "RESEARCH_ARTIFACT_UNCLASSIFIED":
        return 30
    if cls == "POLLUTED_GENERATED_AUDIT":
        return 0
    return 10


def build_evidence_matrix(evidence: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    matrix = {}
    for field in REQUIRED_FIELDS:
        rows = evidence.get(field, [])
        clean_rows = [
            r for r in rows
            if r.get("source_class") in {
                "PRIMARY_SOURCE_CODE",
                "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT",
                "SCRIPT_SOURCE",
            }
        ]
        polluted_rows = [
            r for r in rows
            if r.get("source_class") == "POLLUTED_GENERATED_AUDIT"
        ]
        clean_rows_sorted = sorted(clean_rows, key=evidence_quality_score, reverse=True)

        # Field-specific stricter logic.
        primary_count = len([r for r in clean_rows if r.get("source_class") == "PRIMARY_SOURCE_CODE"])
        original_trace_count = len([r for r in clean_rows if r.get("source_class") == "ORIGINAL_TRACE_OR_SOURCE_HEAD_ARTIFACT"])

        if field in {
            "market_gate_enabled",
            "risk_off_below_spx_ma50",
            "market_shock_gate_enabled",
            "market_shock_daily_return",
            "market_entry_gate_or_equivalent",
        }:
            status = "PASS" if primary_count > 0 else ("PARTIAL" if original_trace_count > 0 else "FAIL")
        elif field in {
            "e1r_v0_2_core_call_chain",
            "e1r_v0_2_sidecar_call_chain",
        }:
            status = "PASS" if (primary_count > 0 and original_trace_count > 0) or len(clean_rows) >= 2 else ("PARTIAL" if clean_rows else "FAIL")
        else:
            status = "FAIL"

        matrix[field] = {
            "status": status,
            "clean_evidence_count": len(clean_rows),
            "primary_source_count": primary_count,
            "original_trace_or_source_head_count": original_trace_count,
            "polluted_evidence_count": len(polluted_rows),
            "best_evidence": [compact(r) for r in clean_rows_sorted[:12]],
            "polluted_examples": [compact(r) for r in polluted_rows[:8]],
            "required": {
                "market_gate_enabled": "Assignment/default and call-path into run_stateful_simulation assumptions for E1R v0.2 core.",
                "risk_off_below_spx_ma50": "Assignment/default and usage in market_state / entry_capacity / risk-off logic.",
                "market_shock_gate_enabled": "Assignment/default and usage in _shock_active.",
                "market_shock_daily_return": "Assignment/default value -0.02 and usage in _shock_active.",
                "market_entry_gate_or_equivalent": "Source evidence for gate output or equivalent BUY/ADD blocking and HOLD/REDUCE/EXIT unaffected behavior.",
                "e1r_v0_2_core_call_chain": "run_stateful_simulation -> core_variant_result/_core_e1r -> compose_e1r_v0_2_variant.",
                "e1r_v0_2_sidecar_call_chain": "build_e1r_sidecar_sleeve -> sidecar_result -> compose_e1r_v0_2_variant, MA_CONFLICT 135-row sleeve.",
            }[field],
        }

    return matrix


def inspect_target_artifact() -> dict[str, Any]:
    if not TARGET_ARTIFACT.exists():
        return {"exists": False}
    obj = read_json(TARGET_ARTIFACT)
    wanted = {}
    for row in flatten(obj):
        k = row["key"]
        p = row["path"]
        if k in {
            "strategy_id", "variant", "total_return_pct", "spx_return_pct", "alpha_pct",
            "max_drawdown_pct", "profit_factor", "sharpe_ratio",
            "regime_aware_logic", "sidecar_active_by_regime", "sidecar_active_by_subclass", "source_file",
        } or any(t in p.lower() for t in ["market_gate", "risk_off", "shock"]):
            wanted[p] = compact(row["value"])
    return {
        "exists": True,
        "path": rel(TARGET_ARTIFACT),
        "sha256": sha256(TARGET_ARTIFACT),
        "selected_fields": wanted,
    }


def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    for p in [RCA2, R9C, R8, TARGET_ARTIFACT]:
        if not p.exists():
            raise FileNotFoundError(f"Missing prerequisite: {rel(p)}")

    rca2 = read_json(RCA2)
    if rca2.get("decision", {}).get("next_required_stage") != "4C-2C-4E-ENGINE-K2-R9D-MARKET_PARAM_SOURCE_LINE_TRACE":
        raise RuntimeError("RCA2 did not authorize R9D as next required stage.")

    target = inspect_target_artifact()

    primary_evidence = collect_primary_source_evidence()

    trace_paths: list[str] = []
    generator_trace_exists = GENERATOR_TRACE.exists()
    if generator_trace_exists:
        trace_obj = read_json(GENERATOR_TRACE)
        trace_paths = extract_trace_candidate_paths(trace_obj)
    trace_evidence = extract_source_head_rows_from_trace_files(trace_paths)

    all_evidence = merge_evidence(primary_evidence, trace_evidence)
    matrix = build_evidence_matrix(all_evidence)

    field_status_counts = {}
    for field, row in matrix.items():
        field_status_counts[row["status"]] = field_status_counts.get(row["status"], 0) + 1

    blocking_fields = [
        field for field, row in matrix.items()
        if row["status"] != "PASS"
    ]

    # R9D is source-line audit. It may PASS as audit even if source evidence is incomplete.
    # Replication readiness is separate and stricter.
    source_line_all_fields_pass = len(blocking_fields) == 0

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "market_param_source_line_trace_complete": True,
        "rca2_loaded": True,
        "target_artifact_exists": target.get("exists") is True,
        "generator_trace_exists": generator_trace_exists,
        "primary_source_files_inspected": all(p.exists() for p in PRIMARY_SOURCE_FILES),
        "trace_candidate_paths_extracted": len(trace_paths) > 0,
        "evidence_matrix_built": True,
        "required_fields_count": len(REQUIRED_FIELDS),
        "source_line_all_fields_pass": source_line_all_fields_pass,
        "blocking_fields_count": len(blocking_fields),
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
    }

    decision = {
        "k2_r9d_market_param_source_line_trace_passed": all([
            validations["market_param_source_line_trace_complete"],
            validations["rca2_loaded"],
            validations["target_artifact_exists"],
            validations["primary_source_files_inspected"],
            validations["evidence_matrix_built"],
            validations["strategy_files_unchanged"],
        ]),
        "market_state_115_replication_ready": source_line_all_fields_pass,
        "formula_patch_allowed_now": False,
        "candidate_extraction_allowed_now": False,
        "implementation_may_resume": False,
        "blocking_fields": blocking_fields,
        "next_required_stage_if_ready": "4C-2C-4E-ENGINE-K2-R10-MARKET_GATE_STANDALONE_REPLICATION_PROPOSAL",
        "next_required_stage_if_not_ready": "4C-2C-4E-ENGINE-K2-R9E-MARKET_PARAM_GAP_CLOSURE_PLAN",
        "conclusion": (
            "K2_R9D_PASS_SOURCE_LINE_EVIDENCE_READY_FOR_R10_PROPOSAL"
            if source_line_all_fields_pass
            else "K2_R9D_SOURCE_LINE_TRACE_COMPLETE_EVIDENCE_GAPS_REMAIN"
        ),
        "recommended_next_action": (
            "Proceed to R10 only if every evidence matrix field is PASS. "
            "If any field is PARTIAL/FAIL, prepare a gap-closure plan instead of implementing."
        ),
    }

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-K2-R9D-MARKET_PARAM_SOURCE_LINE_TRACE",
        "status": "MARKET_PARAM_SOURCE_LINE_TRACE_COMPLETE",
        "purpose": "Trace clean source-line/source-head evidence for each required 115% E1R market gate parameter and call-chain field.",
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
            "rca2": {"path": rel(RCA2), "sha256": sha256(RCA2)},
            "r9c": {"path": rel(R9C), "sha256": sha256(R9C)},
            "r8": {"path": rel(R8), "sha256": sha256(R8)},
            "target_artifact": {"path": rel(TARGET_ARTIFACT), "sha256": sha256(TARGET_ARTIFACT)},
            "generator_trace": {"path": rel(GENERATOR_TRACE), "exists": generator_trace_exists, "sha256": sha256(GENERATOR_TRACE)},
            "primary_source_files": [
                {"path": rel(p), "exists": p.exists(), "sha256": sha256(p)}
                for p in PRIMARY_SOURCE_FILES
            ],
        },
        "target_artifact_inspection": target,
        "source_filter": {
            "primary_source_files": [rel(p) for p in PRIMARY_SOURCE_FILES],
            "trace_candidate_paths_count": len(trace_paths),
            "trace_candidate_paths_sample": trace_paths[:50],
            "polluted_prefixes_excluded_as_primary_proof": POLLUTED_PREFIXES,
            "preferred_original_trace_prefixes": PREFERRED_ORIGINAL_TRACE_PREFIXES,
        },
        "evidence_matrix": matrix,
        "field_status_counts": field_status_counts,
        "blocking_fields": blocking_fields,
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)
    write_json(AUDIT_JSON, report)
    write_json(EVIDENCE_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-K2-R9D — Market Parameter Source-Line Trace")
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
    md.append("## Source Filter")
    md.append("```json")
    md.append(json.dumps(report["source_filter"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Evidence Matrix")
    md.append("```json")
    md.append(json.dumps(matrix, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Field Status Counts")
    md.append("```json")
    md.append(json.dumps(field_status_counts, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Blocking Fields")
    md.append("```json")
    md.append(json.dumps(blocking_fields, indent=2, ensure_ascii=False))
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

    print("E1R_4C2C4E_ENGINE_K2_R9D_MARKET_PARAM_SOURCE_LINE_TRACE_COMPLETE")
    print("status:", report["status"])
    print("target_artifact_inspection:", json.dumps(target, ensure_ascii=False))
    print("source_filter:", json.dumps(report["source_filter"], ensure_ascii=False))
    print("evidence_matrix:", json.dumps(matrix, ensure_ascii=False))
    print("field_status_counts:", json.dumps(field_status_counts, ensure_ascii=False))
    print("blocking_fields:", json.dumps(blocking_fields, ensure_ascii=False))
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
