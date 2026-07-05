from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FEATURE_ROOT = Path("/Users/dongfang/Downloads/sp500-tracker-5y")
MAIN_ROOT = Path("/Users/dongfang/Downloads/sp500-tracker-v13")

REPORT_JSON = FEATURE_ROOT / "reports/e1r_v0_2_port_readiness_audit.json"
REPORT_MD = FEATURE_ROOT / "docs/research/E1R_V0_2_PORT_READINESS_AUDIT.md"

REQUIRED_FILES = [
    "src/engine/e1r_sidecar_sleeve.py",
    "src/engine/e1r_composer.py",
    "src/engine/backtest.py",
    "scripts/export_e1r_v0_2_status.py",
    "scripts/run_e1r_v0_2_oos.py",
    "scripts/run_e1r_v0_2_oos_equity.py",
    "scripts/run_e1r_v0_2_sidecar_lifecycle.py",
    "scripts/export_e1r_v0_2_backtest_equity.py",
    "dashboard/app.js",
    "dashboard/styles.css",
    ".github/workflows/update.yml",
    "docs/research/E1R_V0_2_IMPLEMENTATION_MANIFEST.md",
    "docs/research/E1R_V0_2_OOS_2B_2_SIDECAR_MTM_SPEC.md",
    "docs/research/E1R_V0_2_UI_OOS_INTEGRATION_AUDIT.md",
    "docs/research/E1R_V0_2_PORT_TO_MAIN_PLAN.md",
]

LIGHTWEIGHT_EXPORTS = [
    "exports/e1r_v0_2_status.json",
    "exports/oos_e1r_v0_2_summary.json",
    "exports/oos_e1r_v0_2_sidecar.json",
    "exports/oos_e1r_v0_2_positions.json",
    "exports/oos_e1r_v0_2_orders.json",
    "exports/oos_e1r_v0_2_equity_curve.json",
    "exports/oos_e1r_v0_2_sidecar_lifecycle.json",
    "exports/oos_e1r_v0_2_sidecar_turnover.json",
    "exports/e1r_v0_2_backtest_summary.json",
    "exports/e1r_v0_2_backtest_equity_curve.json",
]

DO_NOT_BLINDLY_COPY = [
    "exports/backtest.json",
    "exports/equity_curve.json",
    "exports/trade_log.json",
    "exports/portfolio_backtest.json",
    "exports/action_forward_returns.json",
]

MANUAL_REVIEW_FILES = [
    "src/engine/backtest.py",
    "dashboard/app.js",
    "dashboard/styles.css",
    ".github/workflows/update.yml",
]


def run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def git_branch(root: Path) -> str:
    code, out, err = run(["git", "branch", "--show-current"], root)
    return out if code == 0 else f"ERROR: {err}"


def git_status(root: Path) -> str:
    code, out, err = run(["git", "status", "--short"], root)
    return out if code == 0 else f"ERROR: {err}"


def git_head(root: Path) -> str:
    code, out, err = run(["git", "rev-parse", "--short", "HEAD"], root)
    return out if code == 0 else f"ERROR: {err}"


def sha256(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_info(rel: str) -> dict[str, Any]:
    fp = FEATURE_ROOT / rel
    mp = MAIN_ROOT / rel
    f_hash = sha256(fp)
    m_hash = sha256(mp)
    return {
        "path": rel,
        "feature_exists": fp.exists(),
        "main_exists": mp.exists(),
        "feature_size": fp.stat().st_size if fp.exists() and fp.is_file() else None,
        "main_size": mp.stat().st_size if mp.exists() and mp.is_file() else None,
        "feature_sha256": f_hash,
        "main_sha256": m_hash,
        "same_content": bool(f_hash and m_hash and f_hash == m_hash),
        "manual_review": rel in MANUAL_REVIEW_FILES,
        "copy_recommendation": (
            "MISSING_IN_FEATURE" if not fp.exists() else
            "COPY_NEW_TO_MAIN" if fp.exists() and not mp.exists() else
            "NO_COPY_NEEDED_SAME_CONTENT" if f_hash and m_hash and f_hash == m_hash else
            "MANUAL_REVIEW_BEFORE_COPY" if rel in MANUAL_REVIEW_FILES else
            "COPY_OR_OVERWRITE_AFTER_REVIEW"
        ),
    }


def json_parse_info(rel: str) -> dict[str, Any]:
    path = FEATURE_ROOT / rel
    info = {
        "path": rel,
        "exists": path.exists(),
        "valid_json": False,
        "top_level_type": None,
        "keys": [],
        "error": None,
    }
    if not path.exists():
        info["error"] = "missing"
        return info
    try:
        obj = json.loads(path.read_text())
        info["valid_json"] = True
        info["top_level_type"] = type(obj).__name__
        if isinstance(obj, dict):
            info["keys"] = sorted(list(obj.keys()))[:30]
    except Exception as e:
        info["error"] = str(e)
    return info


def main() -> None:
    generated_at = datetime.now(timezone.utc).isoformat()

    feature_status = git_status(FEATURE_ROOT)
    main_status = git_status(MAIN_ROOT)

    required = [file_info(x) for x in REQUIRED_FILES]
    lightweight = [file_info(x) for x in LIGHTWEIGHT_EXPORTS]
    heavy = [file_info(x) for x in DO_NOT_BLINDLY_COPY]
    json_checks = [json_parse_info(x) for x in LIGHTWEIGHT_EXPORTS]

    missing_required = [x["path"] for x in required if not x["feature_exists"]]
    missing_main = [x["path"] for x in required if x["feature_exists"] and not x["main_exists"]]
    changed_vs_main = [
        x["path"] for x in required
        if x["feature_exists"] and x["main_exists"] and not x["same_content"]
    ]
    manual_review = [x["path"] for x in required if x["manual_review"] and x["feature_exists"]]

    report = {
        "generated_at": generated_at,
        "feature": {
            "path": str(FEATURE_ROOT),
            "branch": git_branch(FEATURE_ROOT),
            "head": git_head(FEATURE_ROOT),
            "clean": feature_status == "",
            "status_short": feature_status,
        },
        "main": {
            "path": str(MAIN_ROOT),
            "branch": git_branch(MAIN_ROOT),
            "head": git_head(MAIN_ROOT),
            "clean": main_status == "",
            "status_short": main_status,
        },
        "summary": {
            "missing_required_in_feature": missing_required,
            "required_missing_in_main": missing_main,
            "required_changed_vs_main": changed_vs_main,
            "manual_review_required": manual_review,
            "ready_for_copy": feature_status == "" and main_status == "" and not missing_required,
        },
        "required_files": required,
        "lightweight_exports": lightweight,
        "heavy_exports_do_not_blindly_copy": heavy,
        "json_checks": json_checks,
        "recommendation": (
            "READY_FOR_CONTROLLED_COPY_AFTER_MANUAL_REVIEW"
            if feature_status == "" and main_status == "" and not missing_required
            else
            "NOT_READY_REVIEW_STATUS_OR_MISSING_FILES"
        ),
    }

    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")

    lines = []
    lines.append("# E1R v0.2 Port Readiness Audit")
    lines.append("")
    lines.append(f"Generated At: `{generated_at}`")
    lines.append("")
    lines.append("## 1. Worktree Status")
    lines.append("")
    lines.append("| Worktree | Path | Branch | HEAD | Clean |")
    lines.append("|---|---|---:|---:|---:|")
    lines.append(f"| Feature | `{FEATURE_ROOT}` | `{report['feature']['branch']}` | `{report['feature']['head']}` | `{report['feature']['clean']}` |")
    lines.append(f"| Main | `{MAIN_ROOT}` | `{report['main']['branch']}` | `{report['main']['head']}` | `{report['main']['clean']}` |")
    lines.append("")
    lines.append("## 2. Summary")
    lines.append("")
    lines.append(f"- Recommendation: `{report['recommendation']}`")
    lines.append(f"- Ready for controlled copy: `{report['summary']['ready_for_copy']}`")
    lines.append(f"- Missing required files in feature: `{len(missing_required)}`")
    lines.append(f"- Required files missing in main: `{len(missing_main)}`")
    lines.append(f"- Required files changed vs main: `{len(changed_vs_main)}`")
    lines.append(f"- Manual review files: `{len(manual_review)}`")
    lines.append("")
    lines.append("## 3. Required Files")
    lines.append("")
    lines.append("| Path | Feature | Main | Same | Recommendation |")
    lines.append("|---|---:|---:|---:|---|")
    for x in required:
        lines.append(f"| `{x['path']}` | `{x['feature_exists']}` | `{x['main_exists']}` | `{x['same_content']}` | `{x['copy_recommendation']}` |")
    lines.append("")
    lines.append("## 4. Lightweight Exports")
    lines.append("")
    lines.append("| Path | Feature | Main | Same | Recommendation |")
    lines.append("|---|---:|---:|---:|---|")
    for x in lightweight:
        lines.append(f"| `{x['path']}` | `{x['feature_exists']}` | `{x['main_exists']}` | `{x['same_content']}` | `{x['copy_recommendation']}` |")
    lines.append("")
    lines.append("## 5. Heavy / Legacy Exports — Do Not Blindly Copy")
    lines.append("")
    for x in heavy:
        lines.append(f"- `{x['path']}`: feature_exists=`{x['feature_exists']}`, main_exists=`{x['main_exists']}`, same_content=`{x['same_content']}`")
    lines.append("")
    lines.append("## 6. Manual Review Required")
    lines.append("")
    for x in manual_review:
        lines.append(f"- `{x}`")
    lines.append("")
    lines.append("## 7. Next Step")
    lines.append("")
    lines.append("If both worktrees are clean and no required feature files are missing, proceed with a controlled copy into v13/main.")
    lines.append("Do not blindly merge the full feature branch into main.")
    lines.append("")

    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text("\n".join(lines) + "\n")

    print("E1R v0.2 port-readiness audit complete")
    print("feature_branch:", report["feature"]["branch"])
    print("feature_clean:", report["feature"]["clean"])
    print("main_branch:", report["main"]["branch"])
    print("main_clean:", report["main"]["clean"])
    print("missing_required_in_feature:", len(missing_required))
    print("required_missing_in_main:", len(missing_main))
    print("required_changed_vs_main:", len(changed_vs_main))
    print("manual_review_required:", len(manual_review))
    print("recommendation:", report["recommendation"])
    print("wrote:", REPORT_JSON.relative_to(FEATURE_ROOT))
    print("wrote:", REPORT_MD.relative_to(FEATURE_ROOT))


if __name__ == "__main__":
    main()
