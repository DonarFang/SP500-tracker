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

REPORT_JSON = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0F_DAILY_EQUITY_CANDIDATE_EXTRACT.json"
REPORT_MD = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F4B0F_DAILY_EQUITY_CANDIDATE_EXTRACT.md"

OUT_CANDIDATE = ROOT / "exports/e1r_v0_2_daily_equity_candidate_5y_noncanonical.json"

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
            "stdout_tail": proc.stdout[-12000:],
            "stderr_tail": proc.stderr[-12000:],
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
    for k in ["equity", "total_equity", "portfolio_value", "value", "strategy_equity"]:
        v = as_float(row.get(k))
        if v is not None:
            return v
    return None

def detect_spx(row: dict[str, Any]):
    for k in ["spx_indexed", "spx_equity", "spx_value", "spx_close"]:
        v = as_float(row.get(k))
        if v is not None:
            return v
    return None

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

def summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    parsed = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        d = detect_date(r)
        e = detect_equity(r)
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
        "first_equity": first_eq,
        "last_equity": last_eq,
        "total_return_pct_from_rows": total_return,
        "max_drawdown_pct_from_rows": max_drawdown_pct(equities),
        "first_row_keys": sorted(rows[0].keys()) if rows and isinstance(rows[0], dict) else None,
        "first_row": rows[0] if rows else None,
        "last_row": rows[-1] if rows else None,
    }

def metric_match(node: Any) -> dict[str, Any]:
    if not isinstance(node, dict):
        return {"matched": {}, "diffs": {}, "exact": False}

    matched = {}
    diffs = {}
    for k, target in TARGETS.items():
        if k in node:
            v = as_float(node.get(k))
            if v is not None:
                matched[k] = v
                diffs[k] = abs(v - target)

    exact = bool(matched) and all(v <= 0.001 for v in diffs.values())
    return {"matched": matched, "diffs": diffs, "exact": exact}

def find_candidates_in_json(obj: Any, source_path: str, path: str = "$", depth: int = 0) -> list[dict[str, Any]]:
    if depth > 10:
        return []

    out = []

    if isinstance(obj, dict):
        mm = metric_match(obj)

        for key in ["rows", "records", "daily_equity_records", "daily_records", "equity_curve"]:
            v = obj.get(key)
            if isinstance(v, list) and v and isinstance(v[0], dict):
                stats = summarize_rows(v)
                out.append({
                    "source_file": source_path,
                    "json_path": f"{path}.{key}",
                    "list_key": key,
                    "kind": "daily_like_list",
                    "stats": stats,
                    "parent_metric_match": mm,
                    "rows": v,
                })

        if mm["matched"]:
            out.append({
                "source_file": source_path,
                "json_path": path,
                "kind": "metric_node",
                "metric_match": mm,
                "summary_keys": sorted(obj.keys())[:120],
            })

        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                out.extend(find_candidates_in_json(v, source_path, f"{path}.{k}", depth + 1))

    elif isinstance(obj, list):
        if obj and isinstance(obj[0], dict):
            stats = summarize_rows(obj)
            if stats["parseable_equity_rows"] > 0:
                out.append({
                    "source_file": source_path,
                    "json_path": path,
                    "list_key": None,
                    "kind": "daily_like_list",
                    "stats": stats,
                    "parent_metric_match": {"matched": {}, "diffs": {}, "exact": False},
                    "rows": obj,
                })

        for i, v in enumerate(obj[:100]):
            if isinstance(v, (dict, list)):
                out.extend(find_candidates_in_json(v, source_path, f"{path}[{i}]", depth + 1))

    return out

def inspect_outputs_and_extract() -> tuple[dict[str, Any], dict[str, Any] | None]:
    all_candidates = []

    for p in MUTABLE_OUTPUTS:
        item = {
            "path": rel(p),
            "exists": p.exists(),
            "size": p.stat().st_size if p.exists() else 0,
            "hash": sha256(p),
            "candidate_count": 0,
        }

        if p.exists() and p.suffix == ".json" and p.stat().st_size <= 20_000_000:
            try:
                obj = read_json(p)
                candidates = find_candidates_in_json(obj, rel(p))
                item["candidate_count"] = len(candidates)
                item["candidate_summaries"] = [
                    {k: v for k, v in c.items() if k != "rows"}
                    for c in candidates[:20]
                ]
                all_candidates.extend(candidates)
            except Exception as exc:
                item["inspect_error"] = type(exc).__name__ + ": " + str(exc)

        yield item, None

    def score_candidate(c: dict[str, Any]) -> float:
        if c.get("kind") != "daily_like_list":
            return -1e9

        stats = c.get("stats") or {}
        score = 0.0

        rc = stats.get("parseable_equity_rows") or 0
        if rc >= 1000:
            score += 100
        if stats.get("one_row_per_date"):
            score += 100

        tr = stats.get("total_return_pct_from_rows")
        if tr is not None:
            score += max(0, 100 - abs(tr - TARGETS["total_return_pct"]) * 5)

        dd = stats.get("max_drawdown_pct_from_rows")
        if dd is not None:
            score += max(0, 50 - abs(dd - TARGETS["max_drawdown_pct"]) * 5)

        # Penalize symbol-level / diagnostic rows.
        max_rows_per_date = stats.get("max_rows_per_date")
        if max_rows_per_date and max_rows_per_date > 1:
            score -= 200

        return score

    daily = [c for c in all_candidates if c.get("kind") == "daily_like_list"]
    best = sorted(daily, key=score_candidate, reverse=True)[0] if daily else None
    return all_candidates, best

def normalize_candidate_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    first_equity = None

    for r in rows:
        if not isinstance(r, dict):
            continue
        d = detect_date(r)
        e = detect_equity(r)
        if not d or e is None:
            continue

        if first_equity is None:
            first_equity = e

        out.append({
            "date": d,
            "equity": e,
            "portfolio_value": e,
            "strategy_indexed": e / first_equity * 100.0 if first_equity else None,
            "raw_keys": sorted(r.keys()),
            "raw": r,
        })

    return out

def main() -> int:
    baseline_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_before = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    generated_output_items = []
    best_candidate = None
    all_candidate_summaries = []

    with tempfile.TemporaryDirectory(prefix="e1r_4b0f_backup_") as td:
        tmpdir = Path(td)
        backup = backup_outputs(tmpdir)

        run_report = run_generator()

        # Inspect each mutable output.
        all_candidates = []
        for p in MUTABLE_OUTPUTS:
            item = {
                "path": rel(p),
                "exists": p.exists(),
                "size": p.stat().st_size if p.exists() else 0,
                "hash": sha256(p),
            }

            if p.exists() and p.suffix == ".json" and p.stat().st_size <= 20_000_000:
                try:
                    obj = read_json(p)
                    candidates = find_candidates_in_json(obj, rel(p))
                    item["candidate_count"] = len(candidates)
                    item["candidate_summaries"] = [
                        {k: v for k, v in c.items() if k != "rows"}
                        for c in candidates[:20]
                    ]
                    all_candidates.extend(candidates)
                except Exception as exc:
                    item["inspect_error"] = type(exc).__name__ + ": " + str(exc)

            generated_output_items.append(item)

        def score_candidate(c: dict[str, Any]) -> float:
            if c.get("kind") != "daily_like_list":
                return -1e9

            stats = c.get("stats") or {}
            score = 0.0

            rc = stats.get("parseable_equity_rows") or 0
            if rc >= 1000:
                score += 100
            if stats.get("one_row_per_date"):
                score += 100

            tr = stats.get("total_return_pct_from_rows")
            if tr is not None:
                score += max(0, 100 - abs(tr - TARGETS["total_return_pct"]) * 5)

            dd = stats.get("max_drawdown_pct_from_rows")
            if dd is not None:
                score += max(0, 50 - abs(dd - TARGETS["max_drawdown_pct"]) * 5)

            max_rows_per_date = stats.get("max_rows_per_date")
            if max_rows_per_date and max_rows_per_date > 1:
                score -= 200

            return score

        daily = [c for c in all_candidates if c.get("kind") == "daily_like_list"]
        daily_sorted = sorted(daily, key=score_candidate, reverse=True)
        best_candidate = daily_sorted[0] if daily_sorted else None

        all_candidate_summaries = [
            {
                "score": score_candidate(c),
                **{k: v for k, v in c.items() if k != "rows"},
            }
            for c in daily_sorted[:30]
        ]

        candidate_written = False
        candidate_artifact = None

        if best_candidate:
            normalized_rows = normalize_candidate_rows(best_candidate["rows"])
            stats = summarize_rows(best_candidate["rows"])

            validations = {
                "noncanonical_only": True,
                "row_count_ge_1000": stats["parseable_equity_rows"] >= 1000,
                "one_row_per_date": stats["one_row_per_date"],
                "not_symbol_level": (stats["max_rows_per_date"] == 1),
                "total_return_close_to_frozen": (
                    stats["total_return_pct_from_rows"] is not None
                    and abs(stats["total_return_pct_from_rows"] - TARGETS["total_return_pct"]) <= 1.0
                ),
                "maxdd_close_to_frozen": (
                    stats["max_drawdown_pct_from_rows"] is not None
                    and abs(stats["max_drawdown_pct_from_rows"] - TARGETS["max_drawdown_pct"]) <= 1.5
                ),
            }

            candidate_artifact = {
                "artifact_type": "e1r_v0_2_daily_equity_candidate_5y_noncanonical",
                "generated_at": now(),
                "canonical": False,
                "source": {
                    "generator": rel(GENERATOR),
                    "source_file": best_candidate["source_file"],
                    "json_path": best_candidate["json_path"],
                    "list_key": best_candidate["list_key"],
                },
                "targets": TARGETS,
                "stats": stats,
                "validations": validations,
                "rows": normalized_rows,
            }

            write_json(OUT_CANDIDATE, candidate_artifact)
            candidate_written = True

        restore_report = restore_outputs(backup)

    post_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}
    canonical_after = {rel(p): p.exists() for p in CANONICAL_E1R_FILES}

    if best_candidate:
        conclusion = "DAILY_EQUITY_CANDIDATE_EXTRACTED_NONCANONICAL"
        recommended = "Validate the noncanonical candidate against frozen metrics and portfolio-level contract; if it passes, promote via a separate canonical-writing step."
    else:
        conclusion = "NO_DAILY_EQUITY_CANDIDATE_EXTRACTED"
        recommended = "Patch generator wrapper to expose in-memory daily equity rather than relying on persisted outputs."

    report = {
        "generated_at": now(),
        "stage": "B_STAGE_3_8E2F2C4C10F4B0F_DAILY_EQUITY_CANDIDATE_EXTRACT",
        "status": "E1R_DAILY_EQUITY_CANDIDATE_EXTRACT_COMPLETE_NONCANONICAL",
        "policy": {
            "dashboard_changed": False,
            "workflow_changed": False,
            "strategy_logic_changed": False,
            "e1r_canonical_written": False,
            "portfolio_equity_composed": False,
            "full_backtest_rerun": False,
            "mutable_outputs_restored": True,
            "noncanonical_candidate_written": best_candidate is not None,
        },
        "run_report": run_report,
        "generated_output_items": generated_output_items,
        "all_candidate_summaries": all_candidate_summaries,
        "best_candidate_summary": (
            {k: v for k, v in best_candidate.items() if k != "rows"}
            if best_candidate else None
        ),
        "candidate_output_path": rel(OUT_CANDIDATE),
        "candidate_output_exists": OUT_CANDIDATE.exists(),
        "restore_report": restore_report,
        "conclusion": conclusion,
        "recommended_next_action": recommended,
        "strategy_files_unchanged": baseline_hashes == post_hashes,
        "canonical_existence_unchanged_after_restore": canonical_before == canonical_after,
        "canonical_after_restore": canonical_after,
        "next_stage": {
            "name": "Stage 3.8E-2F-2C-4C-10F-4B-0G",
            "title": "Validate E1R noncanonical daily equity candidate",
            "recommended_action": recommended,
        },
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# Stage 3.8E-2F-2C-4C-10F-4B-0F E1R Daily Equity Candidate Extract")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append("- Status: `E1R_DAILY_EQUITY_CANDIDATE_EXTRACT_COMPLETE_NONCANONICAL`")
    md.append(f"- Noncanonical candidate written: `{report['policy']['noncanonical_candidate_written']}`")
    md.append(f"- Strategy files unchanged: `{report['strategy_files_unchanged']}`")
    md.append(f"- Canonical existence unchanged after restore: `{report['canonical_existence_unchanged_after_restore']}`")
    md.append("- E1R canonical written: `False`")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {recommended}")
    md.append("")
    md.append("## Best Candidate")
    md.append("")
    md.append("```json")
    md.append(json.dumps(report["best_candidate_summary"], indent=2, ensure_ascii=False)[:22000])
    md.append("```")
    md.append("")
    md.append("## All Candidate Summaries")
    md.append("")
    md.append("```json")
    md.append(json.dumps(all_candidate_summaries[:20], indent=2, ensure_ascii=False)[:28000])
    md.append("```")
    md.append("")
    md.append("## Generated Output Items")
    md.append("")
    md.append("```json")
    md.append(json.dumps(generated_output_items, indent=2, ensure_ascii=False)[:24000])
    md.append("```")
    md.append("")
    md.append("## Restore Report")
    md.append("")
    md.append("```json")
    md.append(json.dumps(restore_report, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Next Stage")
    md.append("")
    md.append(f"- `{report['next_stage']['name']}`: {report['next_stage']['title']}")
    md.append(f"- Recommended action: {report['next_stage']['recommended_action']}")
    md.append("")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("Stage 3.8E-2F-2C-4C-10F-4B-0F extract complete")
    print("status:", report["status"])
    print("strategy_files_unchanged:", report["strategy_files_unchanged"])
    print("canonical_existence_unchanged_after_restore:", report["canonical_existence_unchanged_after_restore"])
    print("run_ok:", run_report.get("ok"))
    print("candidate_output_exists:", report["candidate_output_exists"])
    print("candidate_output_path:", report["candidate_output_path"])
    print("conclusion:", conclusion)
    if best_candidate:
        print("best_source_file:", best_candidate["source_file"])
        print("best_json_path:", best_candidate["json_path"])
        print("best_stats:", json.dumps(best_candidate["stats"], ensure_ascii=False))
    print("recommended_next_action:", recommended)
    print("next_stage:", report["next_stage"]["name"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
