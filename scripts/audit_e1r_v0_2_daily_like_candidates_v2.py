#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
import shutil
import subprocess
import sys
import tempfile
import time
import os
from datetime import datetime, timezone
from collections import Counter
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts/export_canonical_5y_equity_curves.py"

REPORT_JSON = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0F_V2_DAILY_LIKE_CANDIDATE_REJECTION_AUDIT.json"
REPORT_MD = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0F_V2_DAILY_LIKE_CANDIDATE_REJECTION_AUDIT.md"

FROZEN_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

MUTABLE_OUTPUTS = [
    ROOT / "exports/e1r_v0_2_backtest_summary.json",
    ROOT / "exports/e1r_v0_2_backtest_equity_curve.json",
    ROOT / "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
    ROOT / "exports/e1_e1r_5y_equity_comparison.json",
    ROOT / "data/research/e1r/e1r_formal_backtest_v0_1.json",
]

CANONICAL_E1R_FILES = [
    ROOT / "exports/e1r_v0_2_portfolio_backtest_equity_curve.json",
    ROOT / "exports/e1_e1r_5y_equity_comparison.json",
]

INVALID_4B0F_FILES = [
    ROOT / "scripts/extract_e1r_v0_2_daily_equity_candidate.py",
    ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0F_DAILY_EQUITY_CANDIDATE_EXTRACT.json",
    ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0F_DAILY_EQUITY_CANDIDATE_EXTRACT.md",
    ROOT / "exports/e1r_v0_2_daily_equity_candidate_5y_noncanonical.json",
]

TARGETS = {
    "total_return_pct": 116.7435999134756,
    "spx_return_pct": 76.844174428316,
    "alpha_pct": 39.89942548515961,
    "max_drawdown_pct": 25.904809362815108,
    "profit_factor": 1.1919630955509348,
    "sharpe_ratio": 0.7957270568329264,
}

TIMEOUT_SECONDS = 2400

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

def read_json(p: Path) -> Any:
    return json.loads(p.read_text())

def write_json(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def as_float(x: Any, default=None):
    try:
        if x is None:
            return default
        return float(x)
    except Exception:
        return default

def norm_date(x: Any) -> str | None:
    if x is None:
        return None
    s = str(x)
    if len(s) >= 10 and s[4:5] == "-" and s[7:8] == "-":
        return s[:10]
    return None

def backup_outputs(tmpdir: Path) -> dict[str, Any]:
    backup = {}
    for p in MUTABLE_OUTPUTS:
        item = {
            "path": rel(p),
            "existed_before": p.exists(),
            "hash_before": sha256(p),
            "backup_path": None,
        }
        if p.exists():
            bp = tmpdir / rel(p)
            bp.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, bp)
            item["backup_path"] = str(bp)
        backup[rel(p)] = item
    return backup

def restore_outputs(backup: dict[str, Any]) -> dict[str, Any]:
    out = {}
    for relpath, item in backup.items():
        p = ROOT / relpath
        if item["existed_before"]:
            bp = item.get("backup_path")
            if bp and Path(bp).exists():
                p.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(bp, p)
                action = "restored"
            else:
                action = "missing_backup"
        else:
            if p.exists():
                p.unlink()
                action = "deleted_new_file"
            else:
                action = "no_action_absent"

        out[relpath] = {
            "action": action,
            "hash_after_restore": sha256(p),
            "matches_before": sha256(p) == item["hash_before"],
        }
    return out

def run_generator() -> dict[str, Any]:
    env = os.environ.copy()
    env["E1R_DRY_RUN"] = "1"
    env["E1R_NO_WRITE"] = "1"
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")

    started = time.time()
    try:
        proc = subprocess.run(
            [sys.executable, str(GENERATOR)],
            cwd=str(ROOT),
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIMEOUT_SECONDS,
        )
        return {
            "attempted": True,
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "elapsed_seconds": time.time() - started,
            "stdout_tail": proc.stdout[-8000:],
            "stderr_tail": proc.stderr[-8000:],
        }
    except Exception as exc:
        return {
            "attempted": True,
            "ok": False,
            "elapsed_seconds": time.time() - started,
            "error": type(exc).__name__ + ": " + str(exc),
        }

def detect_date(row: dict[str, Any]) -> str | None:
    for k in ["date", "interval_end_date", "next_date", "core_end_date"]:
        d = norm_date(row.get(k))
        if d:
            return d
    return None

def detect_equity(row: dict[str, Any]):
    for k in ["portfolio_value", "total_equity", "equity", "value", "strategy_equity", "strategy_indexed"]:
        v = as_float(row.get(k))
        if v is not None:
            return v, k
    return None, None

def max_drawdown_pct(equities: list[float]) -> float | None:
    if not equities:
        return None
    peak = equities[0]
    worst = 0.0
    for x in equities:
        peak = max(peak, x)
        if peak:
            worst = min(worst, x / peak - 1.0)
    return abs(worst * 100.0)

def row_has_symbol(row: dict[str, Any]) -> bool:
    return "symbol" in row or "ticker" in row

def row_is_diagnostic(row: dict[str, Any]) -> bool:
    return row.get("diagnostic_only") is True

def summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    parsed = []
    symbol_count = 0
    diagnostic_count = 0
    equity_keys = Counter()

    for r in rows:
        if not isinstance(r, dict):
            continue
        if row_has_symbol(r):
            symbol_count += 1
        if row_is_diagnostic(r):
            diagnostic_count += 1

        d = detect_date(r)
        e, ek = detect_equity(r)
        if ek:
            equity_keys[ek] += 1
        if d and e is not None:
            parsed.append((d, e, r))

    dates = [x[0] for x in parsed]
    dc = Counter(dates)
    equities = [x[1] for x in parsed]

    first_eq = equities[0] if equities else None
    last_eq = equities[-1] if equities else None
    total_return = (last_eq / first_eq - 1.0) * 100.0 if first_eq and last_eq else None

    return {
        "row_count": len(rows),
        "parseable_equity_rows": len(parsed),
        "unique_dates": len(set(dates)),
        "date_start": min(dates) if dates else None,
        "date_end": max(dates) if dates else None,
        "max_rows_per_date": max(dc.values()) if dc else None,
        "one_row_per_date": bool(dc) and max(dc.values()) == 1 and len(parsed) == len(set(dates)),
        "symbol_row_count": symbol_count,
        "diagnostic_only_row_count": diagnostic_count,
        "symbol_row_pct": symbol_count / len(rows) if rows else None,
        "diagnostic_only_row_pct": diagnostic_count / len(rows) if rows else None,
        "equity_key_counter": dict(equity_keys),
        "first_equity": first_eq,
        "last_equity": last_eq,
        "total_return_pct_from_rows": total_return,
        "total_return_abs_diff_vs_frozen": abs(total_return - TARGETS["total_return_pct"]) if total_return is not None else None,
        "max_drawdown_pct_from_rows": max_drawdown_pct(equities),
        "maxdd_abs_diff_vs_frozen": (
            abs(max_drawdown_pct(equities) - TARGETS["max_drawdown_pct"])
            if max_drawdown_pct(equities) is not None else None
        ),
        "first_row_keys": sorted(rows[0].keys()) if rows and isinstance(rows[0], dict) else None,
        "first_row_sample": rows[0] if rows else None,
        "last_row_sample": rows[-1] if rows else None,
    }

def validate_portfolio_candidate(stats: dict[str, Any]) -> dict[str, Any]:
    reasons = []

    checks = {
        "row_count_ge_1000": (stats.get("parseable_equity_rows") or 0) >= 1000,
        "one_row_per_date": stats.get("one_row_per_date") is True,
        "not_symbol_level": (stats.get("symbol_row_count") or 0) == 0,
        "not_diagnostic_only": (stats.get("diagnostic_only_row_count") or 0) == 0,
        "max_rows_per_date_eq_1": stats.get("max_rows_per_date") == 1,
        "total_return_close_to_frozen_1pct": (
            stats.get("total_return_abs_diff_vs_frozen") is not None
            and stats["total_return_abs_diff_vs_frozen"] <= 1.0
        ),
        "maxdd_close_to_frozen_1_5pct": (
            stats.get("maxdd_abs_diff_vs_frozen") is not None
            and stats["maxdd_abs_diff_vs_frozen"] <= 1.5
        ),
    }

    for k, ok in checks.items():
        if not ok:
            reasons.append(k)

    return {
        "checks": checks,
        "accepted_as_portfolio_daily_equity": all(checks.values()),
        "rejection_reasons": reasons,
    }

def find_daily_like_lists(obj: Any, source_file: str, path: str = "$", depth: int = 0) -> list[dict[str, Any]]:
    if depth > 10:
        return []

    out = []

    if isinstance(obj, dict):
        for key in ["rows", "records", "daily_equity_records", "daily_records", "equity_curve"]:
            v = obj.get(key)
            if isinstance(v, list) and v and isinstance(v[0], dict):
                stats = summarize_rows(v)
                validation = validate_portfolio_candidate(stats)
                out.append({
                    "source_file": source_file,
                    "json_path": f"{path}.{key}",
                    "list_key": key,
                    "stats": stats,
                    "validation": validation,
                })

        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                out.extend(find_daily_like_lists(v, source_file, f"{path}.{k}", depth + 1))

    elif isinstance(obj, list):
        if obj and isinstance(obj[0], dict):
            stats = summarize_rows(obj)
            if stats["parseable_equity_rows"] > 0:
                validation = validate_portfolio_candidate(stats)
                out.append({
                    "source_file": source_file,
                    "json_path": path,
                    "list_key": None,
                    "stats": stats,
                    "validation": validation,
                })

        for i, v in enumerate(obj[:100]):
            if isinstance(v, (dict, list)):
                out.extend(find_daily_like_lists(v, source_file, f"{path}[{i}]", depth + 1))

    return out

def metric_match_nodes(obj: Any, source_file: str, path: str = "$", depth: int = 0) -> list[dict[str, Any]]:
    if depth > 10:
        return []
    out = []

    if isinstance(obj, dict):
        matched = {}
        diffs = {}
        for k, target in TARGETS.items():
            if k in obj:
                v = as_float(obj.get(k))
                if v is not None:
                    matched[k] = v
                    diffs[k] = abs(v - target)

        if matched:
            out.append({
                "source_file": source_file,
                "json_path": path,
                "matched": matched,
                "diffs": diffs,
                "exact_all_present": len(matched) == len(TARGETS) and all(d <= 0.001 for d in diffs.values()),
                "keys": sorted(obj.keys())[:120],
            })

        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                out.extend(metric_match_nodes(v, source_file, f"{path}.{k}", depth + 1))

    elif isinstance(obj, list):
        for i, v in enumerate(obj[:100]):
            if isinstance(v, (dict, list)):
                out.extend(metric_match_nodes(v, source_file, f"{path}[{i}]", depth + 1))

    return out

def main() -> int:
    baseline_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_before = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}
    invalid_4b0f_before = {rel(p): p.exists() for p in INVALID_4B0F_FILES}

    with tempfile.TemporaryDirectory(prefix="e1r_4b0f_v2_backup_") as td:
        tmpdir = Path(td)
        backup = backup_outputs(tmpdir)
        run_report = run_generator()

        output_items = []
        all_daily_like = []
        all_metric_nodes = []

        for p in MUTABLE_OUTPUTS:
            item = {
                "path": rel(p),
                "exists_after_run": p.exists(),
                "size_after_run": p.stat().st_size if p.exists() else 0,
                "hash_after_run": sha256(p),
            }

            if p.exists() and p.suffix == ".json" and p.stat().st_size <= 20_000_000:
                try:
                    obj = read_json(p)
                    daily = find_daily_like_lists(obj, rel(p))
                    metrics = metric_match_nodes(obj, rel(p))

                    item["daily_like_count"] = len(daily)
                    item["metric_node_count"] = len(metrics)

                    all_daily_like.extend(daily)
                    all_metric_nodes.extend(metrics)
                except Exception as exc:
                    item["inspect_error"] = type(exc).__name__ + ": " + str(exc)

            output_items.append(item)

        restore_report = restore_outputs(backup)

    post_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_after = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}
    invalid_4b0f_after = {rel(p): p.exists() for p in INVALID_4B0F_FILES}

    accepted = [x for x in all_daily_like if x["validation"]["accepted_as_portfolio_daily_equity"]]
    rejected = [x for x in all_daily_like if not x["validation"]["accepted_as_portfolio_daily_equity"]]
    exact_metrics = [x for x in all_metric_nodes if x.get("exact_all_present")]

    # Keep compact report: no full rows, only samples inside stats.
    daily_like_compact = []
    for x in all_daily_like:
        daily_like_compact.append({
            "source_file": x["source_file"],
            "json_path": x["json_path"],
            "list_key": x["list_key"],
            "stats": x["stats"],
            "validation": x["validation"],
        })

    conclusion = "NO_ACCEPTABLE_PORTFOLIO_DAILY_EQUITY_CANDIDATE_FOUND"
    recommended = "Do not promote any daily-like output. Next step should inspect source code around export_canonical_5y_equity_curves.py and composer return values, not persisted diagnostic rows."

    if accepted:
        conclusion = "ACCEPTABLE_PORTFOLIO_DAILY_EQUITY_CANDIDATE_FOUND_BUT_NOT_EXTRACTED"
        recommended = "Run a separate extraction step for the accepted candidate only, still noncanonical first."

    report = {
        "generated_at": now(),
        "stage": "B_STAGE_3_8E2F2C4C10F4B0F_V2_DAILY_LIKE_CANDIDATE_REJECTION_AUDIT",
        "status": "E1R_DAILY_LIKE_CANDIDATE_REJECTION_AUDIT_COMPLETE_NO_CANDIDATE_EXTRACTED",
        "policy": {
            "dashboard_changed": False,
            "workflow_changed": False,
            "strategy_logic_changed": False,
            "e1r_canonical_written": False,
            "portfolio_equity_composed": False,
            "full_backtest_rerun": False,
            "mutable_outputs_restored": True,
            "candidate_extracted": False,
        },
        "hard_filters": [
            "reject if diagnostic_only == true",
            "reject if row contains symbol/ticker",
            "reject if max_rows_per_date > 1",
            "reject if one_row_per_date != true",
            "reject if total_return diff from frozen > 1.0 pct",
            "reject if maxDD diff from frozen > 1.5 pct",
        ],
        "run_report": run_report,
        "output_items": output_items,
        "summary": {
            "daily_like_candidate_count": len(all_daily_like),
            "accepted_candidate_count": len(accepted),
            "rejected_candidate_count": len(rejected),
            "metric_node_count": len(all_metric_nodes),
            "exact_metric_node_count": len(exact_metrics),
        },
        "accepted_candidates": accepted,
        "rejected_candidates": rejected,
        "daily_like_candidates_compact": daily_like_compact,
        "exact_metric_nodes": exact_metrics,
        "metric_nodes_compact": all_metric_nodes[:30],
        "restore_report": restore_report,
        "invalid_4b0f_files_absent_before": all(v is False for v in invalid_4b0f_before.values()),
        "invalid_4b0f_files_absent_after": all(v is False for v in invalid_4b0f_after.values()),
        "invalid_4b0f_file_existence_before": invalid_4b0f_before,
        "invalid_4b0f_file_existence_after": invalid_4b0f_after,
        "conclusion": conclusion,
        "recommended_next_action": recommended,
        "strategy_files_unchanged": baseline_hashes == post_hashes,
        "canonical_existence_unchanged_after_restore": canonical_before == canonical_after,
        "canonical_after_restore": canonical_after,
        "next_stage": {
            "name": "Stage 3.8E-2F-2C-4C-10F-4B-0G",
            "title": "Inspect generator source and composer return contract",
            "recommended_action": recommended,
        },
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# Stage 3.8E-2F-2C-4C-10F-4B-0F-v2 E1R Daily-like Candidate Rejection Audit")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append("- Status: `E1R_DAILY_LIKE_CANDIDATE_REJECTION_AUDIT_COMPLETE_NO_CANDIDATE_EXTRACTED`")
    md.append("- Candidate extracted: `False`")
    md.append("- E1R canonical written: `False`")
    md.append(f"- Strategy files unchanged: `{report['strategy_files_unchanged']}`")
    md.append(f"- Canonical existence unchanged after restore: `{report['canonical_existence_unchanged_after_restore']}`")
    md.append(f"- Invalid 4B-0F files absent after: `{report['invalid_4b0f_files_absent_after']}`")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append("```json")
    md.append(json.dumps(report["summary"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {recommended}")
    md.append("")
    md.append("## Hard Filters")
    md.append("")
    for f in report["hard_filters"]:
        md.append(f"- {f}")
    md.append("")
    md.append("## Rejected Candidates")
    md.append("")
    md.append("```json")
    md.append(json.dumps(rejected[:20], indent=2, ensure_ascii=False)[:30000])
    md.append("```")
    md.append("")
    md.append("## Accepted Candidates")
    md.append("")
    md.append("```json")
    md.append(json.dumps(accepted[:10], indent=2, ensure_ascii=False)[:12000])
    md.append("```")
    md.append("")
    md.append("## Exact Metric Nodes")
    md.append("")
    md.append("```json")
    md.append(json.dumps(exact_metrics[:10], indent=2, ensure_ascii=False)[:12000])
    md.append("```")
    md.append("")
    md.append("## Output Items")
    md.append("")
    md.append("```json")
    md.append(json.dumps(output_items, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Next Stage")
    md.append("")
    md.append(f"- `{report['next_stage']['name']}`: {report['next_stage']['title']}")
    md.append(f"- Recommended action: {report['next_stage']['recommended_action']}")
    md.append("")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("Stage 3.8E-2F-2C-4C-10F-4B-0F-v2 rejection audit complete")
    print("status:", report["status"])
    print("strategy_files_unchanged:", report["strategy_files_unchanged"])
    print("canonical_existence_unchanged_after_restore:", report["canonical_existence_unchanged_after_restore"])
    print("invalid_4b0f_files_absent_after:", report["invalid_4b0f_files_absent_after"])
    print("run_ok:", run_report.get("ok"))
    print("summary:", json.dumps(report["summary"], ensure_ascii=False))
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)

    if rejected:
        r = rejected[0]
        print("top_rejected_source:", r["source_file"])
        print("top_rejected_path:", r["json_path"])
        print("top_rejected_stats:", json.dumps(r["stats"], ensure_ascii=False))
        print("top_rejected_reasons:", json.dumps(r["validation"]["rejection_reasons"], ensure_ascii=False))

    if accepted:
        a = accepted[0]
        print("top_accepted_source:", a["source_file"])
        print("top_accepted_path:", a["json_path"])
        print("top_accepted_stats:", json.dumps(a["stats"], ensure_ascii=False))

    print("next_stage:", report["next_stage"]["name"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
