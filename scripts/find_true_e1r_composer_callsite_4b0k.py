#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import hashlib
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REPORT_JSON = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.json"
REPORT_MD = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE.md"

FROZEN_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

CANONICAL_E1R_FILES = [
    ROOT / "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
    ROOT / "exports/e1_e1r_5y_equity_comparison.json",
]

# Exclude scripts created during 4B recovery/audit process, because 4B-0J showed
# they can become false-positive "callsites".
EXCLUDE_NAME_FRAGMENTS = [
    "audit_e1r_",
    "probe_e1r_",
    "instrument_e1r_",
    "resolve_e1r_",
    "dry_run_e1r_",
    "find_true_e1r_composer_callsite_4b0k",
]

TARGET_TERMS = [
    "compose_e1r_v0_2_variant",
    "core_variant_result",
    "sidecar_result",
    "build_equity_records_from_returns",
    "extract_core_interval_returns",
    "run_strategy_variant_comparison",
    "run_stateful_simulation",
    "E1R_REGIME_AWARE_V0_2",
    "e1r_v0_2_backtest_summary.json",
    "e1r_v0_2_backtest_equity_curve.json",
]

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))

def sha256(p: Path) -> str | None:
    if not p.exists():
        return None
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def write_json(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def should_exclude(p: Path) -> bool:
    name = p.name
    if any(fragment in name for fragment in EXCLUDE_NAME_FRAGMENTS):
        return True
    if p.parts[-2:] and "docs" in p.parts:
        return True
    return False

def grep_context(p: Path) -> dict[str, Any] | None:
    text = p.read_text(errors="replace")
    if not any(t in text for t in TARGET_TERMS):
        return None

    lines = text.splitlines()
    hits = []
    score = 0

    for i, line in enumerate(lines, start=1):
        matched = [t for t in TARGET_TERMS if t in line]
        if not matched:
            continue

        score += len(matched)
        if "compose_e1r_v0_2_variant" in matched:
            score += 100
        if "core_variant_result" in matched:
            score += 40
        if "sidecar_result" in matched:
            score += 40
        if "run_strategy_variant_comparison" in matched:
            score += 20
        if "run_stateful_simulation" in matched:
            score += 20
        if "E1R_REGIME_AWARE_V0_2" in matched:
            score += 20

        lo = max(1, i - 5)
        hi = min(len(lines), i + 5)
        hits.append({
            "line": i,
            "matched": matched,
            "context": [
                {"line": j, "text": lines[j - 1][:1000]}
                for j in range(lo, hi + 1)
            ],
        })

    return {
        "path": rel(p),
        "score": score,
        "hit_count": len(hits),
        "hits": hits[:100],
    }

def ast_call_scan(p: Path) -> dict[str, Any]:
    text = p.read_text(errors="replace")
    try:
        tree = ast.parse(text)
    except Exception as exc:
        return {"path": rel(p), "parse_error": type(exc).__name__ + ": " + str(exc), "calls": []}

    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = None
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr

            if name and name in [
                "compose_e1r_v0_2_variant",
                "run_strategy_variant_comparison",
                "run_stateful_simulation",
                "build_equity_records_from_returns",
                "extract_core_interval_returns",
            ]:
                calls.append({
                    "line": getattr(node, "lineno", None),
                    "call": name,
                })

    return {"path": rel(p), "calls": calls}

def collect_source_files() -> list[Path]:
    files = []
    for base in [ROOT / "scripts", ROOT / "src"]:
        if not base.exists():
            continue
        for p in base.rglob("*.py"):
            if not p.is_file():
                continue
            if should_exclude(p):
                continue
            files.append(p)
    return sorted(files)

def main() -> int:
    baseline_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_before = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    files = collect_source_files()
    grep_hits = []
    ast_hits = []

    for p in files:
        g = grep_context(p)
        if g:
            grep_hits.append(g)

        a = ast_call_scan(p)
        if a.get("calls"):
            ast_hits.append(a)

    grep_hits = sorted(grep_hits, key=lambda x: (-x["score"], x["path"]))

    direct_compose_files = [
        g for g in grep_hits
        if any("compose_e1r_v0_2_variant" in h["matched"] for h in g["hits"])
    ]

    core_builder_files = [
        g for g in grep_hits
        if any(
            ("core_variant_result" in h["matched"] or "run_strategy_variant_comparison" in h["matched"] or "run_stateful_simulation" in h["matched"])
            for h in g["hits"]
        )
    ]

    composer_related_files = [
        g for g in grep_hits
        if any(
            ("build_equity_records_from_returns" in h["matched"] or "extract_core_interval_returns" in h["matched"])
            for h in g["hits"]
        )
    ]

    post_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_after = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    if direct_compose_files:
        conclusion = "TRUE_DIRECT_COMPOSER_CALLSITE_FOUND"
        recommended = "Instrument the top true direct composer callsite in no-write mode."
    elif core_builder_files:
        conclusion = "NO_DIRECT_COMPOSER_CALLSITE_BUT_CORE_BUILDER_PATHS_FOUND"
        recommended = "Instrument the top core builder path to capture core_variant_result before composer invocation."
    elif composer_related_files:
        conclusion = "NO_TRUE_CALLSITE_FOUND_ONLY_COMPOSER_HELPERS_REFERENCED"
        recommended = "Recover the generator by following helper usage and archived wrapper reports."
    else:
        conclusion = "NO_TRUE_HISTORICAL_COMPOSER_CALLSITE_FOUND_IN_CURRENT_SOURCE"
        recommended = "Proceed by reconstructing inputs from validated E1 core + validated sidecar records, but keep output noncanonical until metrics match frozen E1R."

    report = {
        "generated_at": now(),
        "stage": "B_STAGE_3_8E2F2C4C10F4B0K_TRUE_COMPOSER_CALLSITE_TRACE",
        "status": "E1R_TRUE_COMPOSER_CALLSITE_TRACE_COMPLETE_NO_EXECUTION",
        "policy": {
            "dashboard_changed": False,
            "workflow_changed": False,
            "strategy_logic_changed": False,
            "e1r_canonical_written": False,
            "portfolio_equity_composed": False,
            "full_backtest_rerun": False,
            "source_only": True,
        },
        "search_summary": {
            "source_files_scanned": len(files),
            "grep_hit_file_count": len(grep_hits),
            "ast_call_hit_file_count": len(ast_hits),
            "direct_compose_file_count": len(direct_compose_files),
            "core_builder_file_count": len(core_builder_files),
            "composer_related_file_count": len(composer_related_files),
        },
        "direct_compose_files": direct_compose_files[:20],
        "core_builder_files": core_builder_files[:20],
        "composer_related_files": composer_related_files[:20],
        "top_grep_hits": grep_hits[:30],
        "ast_hits": ast_hits[:30],
        "excluded_name_fragments": EXCLUDE_NAME_FRAGMENTS,
        "conclusion": conclusion,
        "recommended_next_action": recommended,
        "strategy_files_unchanged": baseline_hashes == post_hashes,
        "canonical_existence_unchanged": canonical_before == canonical_after,
        "canonical_after": canonical_after,
        "next_stage": {
            "name": "Stage 3.8E-2F-2C-4C-10F-4B-0L",
            "title": "Instrument true source path or reconstruct noncanonical E1R composition",
            "recommended_action": recommended,
        },
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# Stage 3.8E-2F-2C-4C-10F-4B-0K True Composer Callsite Trace")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append("- Status: `E1R_TRUE_COMPOSER_CALLSITE_TRACE_COMPLETE_NO_EXECUTION`")
    md.append("- Source only: `True`")
    md.append("- E1R canonical written: `False`")
    md.append(f"- Strategy files unchanged: `{report['strategy_files_unchanged']}`")
    md.append(f"- Canonical existence unchanged: `{report['canonical_existence_unchanged']}`")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append("```json")
    md.append(json.dumps(report["search_summary"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {recommended}")
    md.append("")
    md.append("## Direct Compose Files")
    md.append("")
    md.append("```json")
    md.append(json.dumps(direct_compose_files[:10], indent=2, ensure_ascii=False)[:24000])
    md.append("```")
    md.append("")
    md.append("## Core Builder Files")
    md.append("")
    md.append("```json")
    md.append(json.dumps(core_builder_files[:10], indent=2, ensure_ascii=False)[:24000])
    md.append("```")
    md.append("")
    md.append("## Top Grep Hits")
    md.append("")
    md.append("```json")
    md.append(json.dumps(grep_hits[:12], indent=2, ensure_ascii=False)[:28000])
    md.append("```")
    md.append("")
    md.append("## Next Stage")
    md.append("")
    md.append(f"- `{report['next_stage']['name']}`: {report['next_stage']['title']}")
    md.append(f"- Recommended action: {report['next_stage']['recommended_action']}")
    md.append("")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("Stage 3.8E-2F-2C-4C-10F-4B-0K true callsite trace complete")
    print("status:", report["status"])
    print("strategy_files_unchanged:", report["strategy_files_unchanged"])
    print("canonical_existence_unchanged:", report["canonical_existence_unchanged"])
    print("summary:", json.dumps(report["search_summary"], ensure_ascii=False))
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)

    if direct_compose_files:
        top = direct_compose_files[0]
        print("top_direct_compose_source:", top["path"])
        print("top_direct_compose_score:", top["score"])
    if core_builder_files:
        top = core_builder_files[0]
        print("top_core_builder_source:", top["path"])
        print("top_core_builder_score:", top["score"])
    if grep_hits:
        top = grep_hits[0]
        print("top_source_hit:", top["path"])
        print("top_source_score:", top["score"])

    print("next_stage:", report["next_stage"]["name"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
