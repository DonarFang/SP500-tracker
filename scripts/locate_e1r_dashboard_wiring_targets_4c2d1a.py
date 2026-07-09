#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]

BUNDLE = ROOT / "exports/e1r_unified_5y_dashboard_research_bundle.json"

REPORT_JSON = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2D1A_DASHBOARD_WIRING_TARGETS_REPORT.json"
REPORT_MD = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2D1A_DASHBOARD_WIRING_TARGETS_REPORT.md"

SCAN_EXTS = {".html", ".js", ".jsx", ".ts", ".tsx", ".json"}
SKIP_DIRS = {".git", "node_modules", ".next", "dist", "build"}

PATTERNS = [
    "Research & Backtest",
    "Research",
    "Backtest",
    "equity_curve",
    "daily_equity",
    "portfolio_backtest",
    "e1r",
    "E1R",
    "E1_AUDITED_G4_MINHOLD10",
    "e1_unified",
    "fetch(",
    "exports/",
]

def now():
    return datetime.now(timezone.utc).isoformat()

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))

def write_json(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def iter_files():
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        parts = set(p.parts)
        if parts & SKIP_DIRS:
            continue
        if p.suffix.lower() not in SCAN_EXTS:
            continue
        if "docs/research" in str(p):
            continue
        if "exports/e1r_unified_5y_dashboard_research_bundle.json" in str(p):
            continue
        yield p

def scan_file(p: Path):
    try:
        text = p.read_text(errors="replace")
    except Exception:
        return None

    hits = []
    lines = text.splitlines()

    for i, line in enumerate(lines, start=1):
        for pat in PATTERNS:
            if pat in line:
                hits.append({
                    "line": i,
                    "pattern": pat,
                    "text": line.strip()[:260],
                })

    if not hits:
        return None

    score = 0
    joined = "\n".join(h["text"] for h in hits)

    if "Research & Backtest" in joined:
        score += 100
    if "Backtest" in joined:
        score += 40
    if "equity_curve" in joined or "daily_equity" in joined:
        score += 40
    if "E1R" in joined or "e1r" in joined:
        score += 30
    if "fetch(" in joined:
        score += 20
    if "E1_AUDITED_G4_MINHOLD10" in joined:
        score += 20

    return {
        "path": rel(p),
        "score": score,
        "hit_count": len(hits),
        "hits": hits[:80],
    }

def inspect_bundle():
    bundle = json.loads(BUNDLE.read_text())
    rows = bundle.get("curve", {}).get("rows", [])
    metrics = bundle.get("metrics", {})
    return {
        "exists": BUNDLE.exists(),
        "path": rel(BUNDLE),
        "status": bundle.get("status"),
        "metric_source": bundle.get("metric_source"),
        "display_scope": bundle.get("display_scope"),
        "row_count": len(rows),
        "metrics": metrics,
        "warnings": bundle.get("warnings"),
        "do_not_use": bundle.get("do_not_use"),
    }

def main():
    bundle_info = inspect_bundle()

    scan_results = []
    for p in iter_files():
        r = scan_file(p)
        if r:
            scan_results.append(r)

    scan_results.sort(key=lambda x: (-x["score"], x["path"]))

    top = scan_results[:30]

    likely_targets = []
    for r in top:
        path = r["path"].lower()
        joined = " ".join(h["text"] for h in r["hits"]).lower()
        if (
            "research" in joined
            or "backtest" in joined
            or "equity_curve" in joined
            or "portfolio_backtest" in joined
            or "dashboard" in path
            or path.endswith("index.html")
        ):
            likely_targets.append(r)

    report = {
        "generated_at": now(),
        "stage": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2D1A_DASHBOARD_WIRING_TARGETS",
        "status": "DASHBOARD_WIRING_TARGETS_LOCATED_NO_UI_CHANGE",
        "policy": {
            "ui_changed": False,
            "bundle_changed": False,
            "e1_frozen_metrics_changed": False,
            "strategy_logic_changed": False,
        },
        "bundle_info": bundle_info,
        "scan_summary": {
            "files_with_hits": len(scan_results),
            "top_hit_count": len(top),
            "likely_target_count": len(likely_targets),
        },
        "likely_targets": likely_targets[:12],
        "top_scan_results": top,
        "conclusion": "READY_TO_PATCH_DASHBOARD_AFTER_REVIEWING_TARGETS",
        "recommended_next_action": "Proceed to 4C-2D-1B: patch the Research & Backtest tab to load exports/e1r_unified_5y_dashboard_research_bundle.json with explicit account-level-only warnings.",
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R Unified 5Y — 4C-2D-1A Dashboard Wiring Targets")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Bundle")
    md.append("")
    md.append("```json")
    md.append(json.dumps(bundle_info, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Likely Targets")
    md.append("")
    md.append("```json")
    md.append(json.dumps(likely_targets[:12], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{report['conclusion']}`")
    md.append(f"- Recommended: {report['recommended_next_action']}")
    md.append("")
    REPORT_MD.write_text("\n".join(md) + "\n")

    print("E1R_UNIFIED_5Y_4C2D1A_DASHBOARD_WIRING_TARGETS_COMPLETE")
    print("bundle_info:", json.dumps(bundle_info, ensure_ascii=False))
    print("scan_summary:", json.dumps(report["scan_summary"], ensure_ascii=False))
    print("likely_targets:", json.dumps(likely_targets[:8], ensure_ascii=False)[:12000])
    print("conclusion:", report["conclusion"])
    print("recommended_next_action:", report["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
