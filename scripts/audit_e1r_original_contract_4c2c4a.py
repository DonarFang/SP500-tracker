#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re
from datetime import datetime, timezone
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

REPORT_JSON = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4A_ORIGINAL_CONTRACT_AUDIT.json"
REPORT_MD = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C4A_ORIGINAL_CONTRACT_AUDIT.md"

SCAN_ROOTS = [
    ROOT / "docs",
    ROOT / "exports",
    ROOT / "src",
    ROOT / "scripts",
]

SCAN_EXTS = {".py", ".json", ".md", ".txt", ".html", ".js", ".ts", ".tsx", ".jsx"}

SKIP_PARTS = {
    ".git",
    "node_modules",
    ".next",
    "dist",
    "build",
}

CONTRACT = {
    "strategy_id": "E1R_COMBINED_5Y_ORIGINAL_CONTRACT",
    "rules": [
        "UPTREND uses the previously validated UPTREND strategy.",
        "SIDEWAYS / MA_CONFLICT uses the previously validated sidecar strategy.",
        "DETERIORATION / RECOVERY participates only if confirmed by original SIDEWAYS definition; otherwise cash/defensive.",
        "DOWNTREND is cash/defensive.",
        "Actual account holdings must always be <= 3 stocks in every regime.",
        "SIDEWAYS Top10 is candidate pool only, not 10 live account holdings.",
        "No trading strategy logic changes are allowed in this audit.",
    ],
}

SEARCH_PATTERNS = {
    "uptrend_confirmed": [
        "E1R_UPTREND_CONFIRMED",
        "UPTREND_CONFIRMED",
        "Confirmed",
        "leader_rank",
        "leader_score",
        "momentum_acceleration",
        "rs_20d_improvement",
    ],
    "uptrend_emerging": [
        "E1R_UPTREND_EMERGING",
        "Emerging",
        "diagnostic_only",
        "emerging",
    ],
    "sideways_sidecar": [
        "sidecar",
        "SIDEWAYS",
        "MA_CONFLICT",
        "gross_exposure",
        "gross_exposure_max",
        "selected_count",
        "selected_count_max",
        "sidecar_active",
    ],
    "deterioration_recovery": [
        "DETERIORATION_TRANSITION",
        "RECOVERY_TRANSITION",
        "Deterioration",
        "Recovery",
    ],
    "downtrend": [
        "DOWNTREND",
        "DOWNTREND_DEFENSIVE",
        "cash",
        "defensive",
    ],
    "position_cap": [
        "max_positions",
        "MaxPos",
        "open_positions_count",
        "MAX_POSITIONS",
        "max_account_positions",
        "position_cap",
    ],
    "top10_candidate_pool": [
        "Top10",
        "top10",
        "candidate_top_n",
        "selected_count_max",
        "candidate pool",
        "candidate_top",
    ],
    "known_invalid_max10": [
        "MaxPos=10",
        "max_positions\": 10",
        "open_positions_count\": 10",
        "final_exposure_pct\": 100.0",
        "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2C_FULL_RUN",
    ],
}

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))

def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def should_scan(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.suffix.lower() not in SCAN_EXTS:
        return False
    if any(part in SKIP_PARTS for part in path.parts):
        return False
    return True

def iter_files():
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if should_scan(p):
                yield p

def scan_file(path: Path):
    try:
        text = path.read_text(errors="replace")
    except Exception:
        return None

    lines = text.splitlines()
    hits_by_group = {}

    for group, patterns in SEARCH_PATTERNS.items():
        hits = []
        for i, line in enumerate(lines, start=1):
            for pat in patterns:
                if pat in line:
                    hits.append({
                        "line": i,
                        "pattern": pat,
                        "text": line.strip()[:300],
                    })
        if hits:
            hits_by_group[group] = hits[:80]

    if not hits_by_group:
        return None

    score = 0
    text_lower = text.lower()

    if "e1r" in text_lower:
        score += 40
    if "uptrend" in text_lower:
        score += 20
    if "sideways" in text_lower:
        score += 20
    if "sidecar" in text_lower:
        score += 30
    if "max_positions" in text_lower or "maxpos" in text_lower:
        score += 20
    if "ma_conflict" in text_lower:
        score += 20
    if "diagnostic" in text_lower:
        score += 5
    if "v0_2" in text_lower or "v0.2" in text_lower:
        score += 20
    if "phase 3b" in text_lower or "phase_3b" in text_lower:
        score += 20
    if "phase 3c" in text_lower or "phase_3c" in text_lower:
        score += 20
    if "phase 3d" in text_lower or "phase_3d" in text_lower:
        score += 10

    return {
        "path": rel(path),
        "score": score,
        "groups": sorted(hits_by_group.keys()),
        "hits_by_group": hits_by_group,
    }

def read_json_if_exists(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except Exception:
        return None

def inspect_known_artifacts():
    candidates = [
        ROOT / "exports/e1r_unified_5y_full_account_v1_result.json",
        ROOT / "exports/e1r_unified_5y_full_account_v1_summary.json",
        ROOT / "exports/e1r_unified_5y_dashboard_research_bundle.json",
        ROOT / "exports/e1r_unified_5y_full_account_v1_row_derived_summary.json",
        ROOT / "exports/e1r_unified_5y_max3_contract_result.json",
        ROOT / "exports/portfolio_backtest.json",
        ROOT / "exports/backtest.json",
        ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json",
    ]

    out = []
    for p in candidates:
        obj = read_json_if_exists(p)
        item = {
            "path": rel(p),
            "exists": p.exists(),
            "json_ok": obj is not None,
        }

        if isinstance(obj, dict):
            item["top_keys"] = sorted(obj.keys())[:80]

            for key in [
                "strategy_variant",
                "version",
                "status",
                "total_return_pct",
                "spx_total_return_pct",
                "alpha_pct",
                "final_equity",
                "max_drawdown_pct",
                "number_of_trades",
                "total_trades_all",
                "e1r_candidate_count",
            ]:
                if key in obj:
                    item[key] = obj[key]

            if "strategy_controls" in obj and isinstance(obj["strategy_controls"], dict):
                sc = obj["strategy_controls"]
                item["strategy_controls_extract"] = {
                    k: sc.get(k)
                    for k in [
                        "max_positions",
                        "entry_top_n",
                        "candidate_top_n",
                        "entry_rs_min",
                        "min_holding_days",
                        "e1r_regime_wiring_enabled",
                        "e1r_regime_source",
                    ]
                    if k in sc
                }

            if "metrics" in obj and isinstance(obj["metrics"], dict):
                m = obj["metrics"]
                item["metrics_extract"] = {
                    k: m.get(k)
                    for k in [
                        "total_return_pct",
                        "spx_total_return_pct",
                        "alpha_pct",
                        "cagr_pct",
                        "max_drawdown_pct",
                        "sharpe_ratio",
                        "row_count",
                        "final_equity",
                    ]
                    if k in m
                }

            if "row_derived_metrics" in obj and isinstance(obj["row_derived_metrics"], dict):
                m = obj["row_derived_metrics"]
                item["row_derived_metrics_extract"] = {
                    k: m.get(k)
                    for k in [
                        "total_return_pct",
                        "spx_total_return_pct",
                        "alpha_pct",
                        "cagr_pct",
                        "max_drawdown_pct",
                        "row_count",
                        "final_exposure_pct",
                    ]
                    if k in m
                }

            if "record_summary" in obj and isinstance(obj["record_summary"], dict):
                rs = obj["record_summary"]
                item["record_summary_extract"] = {
                    k: rs.get(k)
                    for k in [
                        "row_count",
                        "date_start",
                        "date_end",
                        "regime_counts",
                        "active_mode_counts",
                        "risk_budget_mode_counts",
                    ]
                    if k in rs
                }

            if "rows" in obj and isinstance(obj["rows"], list):
                item["rows_count"] = len(obj["rows"])

            if "curve" in obj and isinstance(obj["curve"], dict):
                rows = obj["curve"].get("rows")
                if isinstance(rows, list):
                    item["curve_rows_count"] = len(rows)

        out.append(item)

    return out

def extract_contract_signals(scan_results):
    by_group = {k: [] for k in SEARCH_PATTERNS.keys()}

    for r in scan_results:
        for g in r["groups"]:
            by_group[g].append({
                "path": r["path"],
                "score": r["score"],
                "hits": r["hits_by_group"].get(g, [])[:20],
            })

    for g in by_group:
        by_group[g].sort(key=lambda x: (-x["score"], x["path"]))

    return {g: by_group[g][:10] for g in by_group}

def classify_current_state(contract_signals, artifact_summary):
    findings = []

    findings.append({
        "topic": "UPTREND strategy",
        "current_confidence": "NEEDS_SOURCE_CONFIRMATION",
        "expected_contract": "Use previously validated UPTREND strategy. Do not replace with new logic.",
        "evidence_groups": ["uptrend_confirmed", "uptrend_emerging", "position_cap"],
        "audit_question": "Which file/function is the validated UPTREND execution entrypoint?",
    })

    findings.append({
        "topic": "SIDEWAYS / MA_CONFLICT strategy",
        "current_confidence": "NEEDS_SOURCE_CONFIRMATION",
        "expected_contract": "Use previously validated SIDEWAYS / MA_CONFLICT sidecar strategy. Top10 is candidate pool only.",
        "evidence_groups": ["sideways_sidecar", "top10_candidate_pool", "deterioration_recovery"],
        "audit_question": "Which file/function/artifact is the validated sidecar execution contract?",
    })

    findings.append({
        "topic": "DETERIORATION / RECOVERY",
        "current_confidence": "UNKNOWN_UNTIL_ORIGINAL_SIDEWAYS_CONTRACT_CONFIRMED",
        "expected_contract": "Participate only if original SIDEWAYS strategy explicitly includes them; otherwise cash/defensive.",
        "evidence_groups": ["deterioration_recovery"],
        "audit_question": "Were DETERIORATION_TRANSITION or RECOVERY_TRANSITION included in validated SIDEWAYS execution, or only MA_CONFLICT?",
    })

    findings.append({
        "topic": "DOWNTREND",
        "current_confidence": "NEEDS_SOURCE_CONFIRMATION",
        "expected_contract": "Cash / defensive.",
        "evidence_groups": ["downtrend"],
        "audit_question": "Confirm DOWNTREND has no normal buy execution in combined E1R.",
    })

    findings.append({
        "topic": "Global account position cap",
        "current_confidence": "USER_FROZEN_CONTRACT",
        "expected_contract": "Actual account holdings <= 3 stocks in every regime.",
        "evidence_groups": ["position_cap", "known_invalid_max10"],
        "audit_question": "Confirm current combined backtest call enforces account open_positions_count <= 3, not only candidate count.",
    })

    return findings

def main():
    scan_results = []
    for p in iter_files():
        r = scan_file(p)
        if r:
            scan_results.append(r)

    scan_results.sort(key=lambda x: (-x["score"], x["path"]))

    contract_signals = extract_contract_signals(scan_results)
    artifact_summary = inspect_known_artifacts()
    findings = classify_current_state(contract_signals, artifact_summary)

    report = {
        "generated_at": now(),
        "stage": "E1R_COMBINED_5Y_4C2C4A_ORIGINAL_CONTRACT_RECOVERY_AUDIT",
        "status": "ORIGINAL_CONTRACT_RECOVERY_AUDIT_COMPLETE_NO_STRATEGY_CHANGE_NO_BACKTEST",
        "policy": {
            "strategy_logic_changed": False,
            "backtest_run": False,
            "dashboard_changed": False,
            "exports_modified": False,
            "purpose": "Recover and verify original E1R contract before combined 5Y run.",
        },
        "frozen_user_contract": CONTRACT,
        "scan_summary": {
            "files_with_hits": len(scan_results),
            "top_files": [
                {
                    "path": r["path"],
                    "score": r["score"],
                    "groups": r["groups"],
                    "hit_count": sum(len(v) for v in r["hits_by_group"].values()),
                }
                for r in scan_results[:25]
            ],
        },
        "contract_signals": contract_signals,
        "artifact_summary": artifact_summary,
        "findings": findings,
        "conclusion": "CONTRACT_SOURCES_LOCATED_FOR_REVIEW_BUT_EXECUTABLE_ENTRYPOINTS_NOT_YET_LOCKED",
        "recommended_next_action": "Review the top source hits for UPTREND and SIDEWAYS/MA_CONFLICT, then create a no-strategy-change combined-run adapter that calls only the recovered original entrypoints and enforces global open_positions_count <= 3.",
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R Combined 5Y — 4C-2C-4A Original Contract Recovery Audit")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Policy")
    md.append("")
    md.append("```json")
    md.append(json.dumps(report["policy"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Frozen User Contract")
    md.append("")
    md.append("```json")
    md.append(json.dumps(CONTRACT, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Scan Summary")
    md.append("")
    md.append("```json")
    md.append(json.dumps(report["scan_summary"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Findings")
    md.append("")
    md.append("```json")
    md.append(json.dumps(findings, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Contract Signals")
    md.append("")
    md.append("```json")
    md.append(json.dumps(contract_signals, indent=2, ensure_ascii=False)[:50000])
    md.append("```")
    md.append("")
    md.append("## Artifact Summary")
    md.append("")
    md.append("```json")
    md.append(json.dumps(artifact_summary, indent=2, ensure_ascii=False)[:30000])
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{report['conclusion']}`")
    md.append(f"- Recommended: {report['recommended_next_action']}")
    md.append("")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("E1R_COMBINED_5Y_4C2C4A_ORIGINAL_CONTRACT_AUDIT_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("frozen_user_contract:", json.dumps(CONTRACT, ensure_ascii=False))
    print("scan_summary:", json.dumps(report["scan_summary"], ensure_ascii=False)[:12000])
    print("findings:", json.dumps(findings, ensure_ascii=False))
    print("artifact_summary:", json.dumps(artifact_summary, ensure_ascii=False)[:12000])
    print("conclusion:", report["conclusion"])
    print("recommended_next_action:", report["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
