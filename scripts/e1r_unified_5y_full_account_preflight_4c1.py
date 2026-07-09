#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import hashlib
import importlib.util
import inspect
import sys
from datetime import datetime, timezone
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REPORT_JSON = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C1_PREFLIGHT_REPORT.json"
REPORT_MD = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C1_PREFLIGHT_REPORT.md"
SPEC_JSON = ROOT / "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_SPEC.json"

FROZEN_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

REQUIRED_DATA = {
    "spx_regime_daily": ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json",
    "spx_raw": ROOT / "data/research/e1_5y/raw/indices/SPX.json",
    "e1r_sidecar_records": ROOT / "exports/e1r_v0_2_sidecar_records_5y.json",
}

SOURCE_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
    ROOT / "scripts/export_canonical_5y_equity_curves.py",
]

TARGET_FUNCTION_NAMES = [
    "run_stateful_simulation",
    "run_strategy_variant_comparison",
    "run_backtest",
    "run_portfolio_backtest",
    "run_e1r_backtest",
    "run_e1r_unified_backtest",
    "compose_e1r_v0_2_variant",
    "build_e1r_sidecar_sleeve",
    "extract_core_interval_returns",
    "build_equity_records_from_returns",
]

TARGET_TERMS = [
    "run_stateful_simulation",
    "run_strategy_variant_comparison",
    "selected_variant",
    "variant_results",
    "daily_records",
    "portfolio_value",
    "total_equity",
    "cash",
    "positions_value",
    "open_positions_count",
    "spx_regime",
    "SIDEWAYS",
    "UPTREND",
    "DOWNTREND",
    "MA_CONFLICT",
    "e1r_active_mode",
    "risk_budget",
    "gross_exposure",
    "sidecar",
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

def read_json_if_exists(p: Path) -> Any:
    if not p.exists():
        return None
    return json.loads(p.read_text())

def write_json(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def summarize_json(p: Path) -> dict[str, Any]:
    if not p.exists():
        return {"exists": False}
    out = {
        "exists": True,
        "path": rel(p),
        "size": p.stat().st_size,
        "sha256": sha256(p),
    }
    try:
        obj = read_json_if_exists(p)
        out["json_valid"] = True
        out["type"] = type(obj).__name__
        if isinstance(obj, dict):
            out["top_keys"] = sorted(obj.keys())[:100]
            for key in ["daily_regime", "bars", "rows", "records", "curve"]:
                v = obj.get(key)
                if isinstance(v, list):
                    out[f"{key}_len"] = len(v)
                    if v and isinstance(v[0], dict):
                        out[f"{key}_first_keys"] = sorted(v[0].keys())[:80]
                        out[f"{key}_first"] = v[0]
                        out[f"{key}_last"] = v[-1]
            if "daily_regime" in obj and isinstance(obj["daily_regime"], dict):
                keys = sorted(obj["daily_regime"].keys())
                out["daily_regime_count"] = len(keys)
                out["daily_regime_start"] = keys[0] if keys else None
                out["daily_regime_end"] = keys[-1] if keys else None
        elif isinstance(obj, list):
            out["length"] = len(obj)
            if obj and isinstance(obj[0], dict):
                out["first_keys"] = sorted(obj[0].keys())[:80]
                out["first"] = obj[0]
                out["last"] = obj[-1]
    except Exception as exc:
        out["json_valid"] = False
        out["error"] = type(exc).__name__ + ": " + str(exc)
    return out

def import_module_from_path(name: str, path: Path) -> dict[str, Any]:
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "src"))

    out = {
        "path": rel(path),
        "exists": path.exists(),
        "import_ok": False,
        "errors": [],
        "target_functions": {},
        "public_backtest_like_objects": {},
    }

    if not path.exists():
        return out

    try:
        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise RuntimeError("cannot create import spec")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)

        out["import_ok"] = True

        for fn_name in TARGET_FUNCTION_NAMES:
            if hasattr(mod, fn_name):
                fn = getattr(mod, fn_name)
                item = {
                    "exists": True,
                    "type": type(fn).__name__,
                }
                if callable(fn):
                    try:
                        item["signature"] = str(inspect.signature(fn))
                    except Exception as exc:
                        item["signature_error"] = type(exc).__name__ + ": " + str(exc)
                    try:
                        src, line_no = inspect.getsourcelines(fn)
                        item["source_line"] = line_no
                        item["source_head"] = "".join(src[:80])
                    except Exception as exc:
                        item["source_error"] = type(exc).__name__ + ": " + str(exc)
                out["target_functions"][fn_name] = item

        for name2 in dir(mod):
            if name2.startswith("_"):
                continue
            lower = name2.lower()
            if any(k in lower for k in ["backtest", "simulation", "variant", "portfolio", "e1r", "stateful"]):
                obj = getattr(mod, name2)
                item = {"type": type(obj).__name__}
                if callable(obj):
                    try:
                        item["signature"] = str(inspect.signature(obj))
                    except Exception:
                        pass
                out["public_backtest_like_objects"][name2] = item

    except Exception as exc:
        out["errors"].append(type(exc).__name__ + ": " + str(exc))

    return out

def ast_scan_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": rel(path), "exists": False}

    text = path.read_text(errors="replace")
    result = {
        "path": rel(path),
        "exists": True,
        "grep_hits": [],
        "function_defs": [],
        "calls": [],
    }

    lines = text.splitlines()
    for i, line in enumerate(lines, start=1):
        matched = [t for t in TARGET_TERMS if t in line]
        if matched:
            lo = max(1, i - 3)
            hi = min(len(lines), i + 3)
            result["grep_hits"].append({
                "line": i,
                "matched": matched,
                "context": [
                    {"line": j, "text": lines[j - 1][:900]}
                    for j in range(lo, hi + 1)
                ],
            })

    try:
        tree = ast.parse(text)
    except Exception as exc:
        result["parse_error"] = type(exc).__name__ + ": " + str(exc)
        return result

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name in TARGET_FUNCTION_NAMES or any(k in node.name.lower() for k in ["backtest", "simulation", "variant", "portfolio", "e1r", "stateful"]):
                result["function_defs"].append({
                    "name": node.name,
                    "line": node.lineno,
                    "end_line": getattr(node, "end_lineno", node.lineno),
                    "args": [a.arg for a in node.args.args],
                })

        if isinstance(node, ast.Call):
            call_name = None
            if isinstance(node.func, ast.Name):
                call_name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                call_name = node.func.attr
            if call_name in TARGET_FUNCTION_NAMES:
                result["calls"].append({
                    "line": getattr(node, "lineno", None),
                    "call": call_name,
                })

    return result

def build_spec() -> dict[str, Any]:
    return {
        "strategy_id": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1",
        "purpose": "Run a single continuous 5Y full-account backtest that organically connects UPTREND, SIDEWAYS, and DOWNTREND regimes in one capital account.",
        "window": {
            "target_start": "2021-06-11",
            "target_end": "latest available aligned 5Y date before forward start",
            "expected_min_rows": 1000,
        },
        "capital_account": {
            "initial_capital": 100000.0,
            "single_account": True,
            "daily_mark_to_market": True,
            "fields_required_per_day": [
                "date",
                "cash",
                "market_value",
                "portfolio_value",
                "daily_return",
                "drawdown",
                "n_positions",
                "gross_exposure",
                "regime",
                "subclass",
                "actions",
            ],
        },
        "regime_rules_high_level": {
            "UPTREND": "Use E1R uptrend/core stateful position rules in the same account.",
            "SIDEWAYS_MA_CONFLICT": "Allow sidecar sleeve behavior, e.g. 25% gross exposure, inside the same account.",
            "SIDEWAYS_DETERIORATION_TRANSITION": "Defensive/risk-off or explicitly defined reduced exposure; no untracked external sleeve.",
            "SIDEWAYS_RECOVERY_TRANSITION": "Defensive/recovery transition rule; must be explicit in output attribution.",
            "DOWNTREND": "Cash/risk-off unless a separately approved defensive rule exists.",
        },
        "required_outputs": {
            "official_backtest_curve": "exports/e1r_unified_5y_full_account_v1_equity_curve.json",
            "official_summary": "exports/e1r_unified_5y_full_account_v1_summary.json",
            "comparison_bundle": "exports/e1_e1r_unified_5y_full_account_v1_comparison.json",
            "audit_report": "docs/research/E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C2_RUN_REPORT.json",
        },
        "required_metrics": [
            "total_return_pct",
            "CAGR",
            "max_drawdown_pct",
            "sharpe_ratio",
            "profit_factor",
            "win_rate_pct",
            "number_of_trades",
            "exposure_pct",
            "avg_holding_days",
            "regime_attribution",
            "sidecar_attribution",
            "cash_continuity",
            "market_value_continuity",
        ],
        "acceptance_tests": {
            "one_row_per_date": True,
            "no_symbol_level_rows": True,
            "no_diagnostic_only_rows": True,
            "cash_plus_market_value_equals_portfolio_value": "tolerance <= 0.01%",
            "no_negative_cash_unless_margin_explicitly_enabled": True,
            "regime_coverage_required": ["UPTREND", "SIDEWAYS", "DOWNTREND"],
            "single_account_no_stitching": True,
            "forward_connection_ready": "last backtest equity can seed OOS indexed curve without resetting label ambiguity",
        },
        "non_goals": [
            "Do not stitch separate UPTREND and SIDEWAYS result curves.",
            "Do not reuse frozen E1R +116.74% summary as if it were a daily equity curve.",
            "Do not label any candidate artifact as official unless it passes full account validations.",
        ],
    }

def main() -> int:
    baseline_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}

    spec = build_spec()
    write_json(SPEC_JSON, spec)

    data_summary = {name: summarize_json(path) for name, path in REQUIRED_DATA.items()}

    imports = {
        "backtest": import_module_from_path("backtest_4c1", ROOT / "src/engine/backtest.py"),
        "e1r_composer": import_module_from_path("e1r_composer_4c1", ROOT / "src/engine/e1r_composer.py"),
        "e1r_sidecar_sleeve": import_module_from_path("e1r_sidecar_sleeve_4c1", ROOT / "src/engine/e1r_sidecar_sleeve.py"),
    }

    source_scans = {rel(p): ast_scan_file(p) for p in SOURCE_FILES}

    available_functions = {}
    for module_name, mod in imports.items():
        for fn, info in mod.get("target_functions", {}).items():
            if info.get("exists"):
                available_functions[f"{module_name}.{fn}"] = info.get("signature")

    preflight_checks = {
        "required_data_exists": all(x.get("exists") for x in data_summary.values()),
        "spx_regime_available": data_summary["spx_regime_daily"].get("exists") and data_summary["spx_regime_daily"].get("json_valid"),
        "sidecar_records_available": data_summary["e1r_sidecar_records"].get("exists") and data_summary["e1r_sidecar_records"].get("json_valid"),
        "backtest_import_ok": imports["backtest"].get("import_ok"),
        "composer_import_ok": imports["e1r_composer"].get("import_ok"),
        "sidecar_import_ok": imports["e1r_sidecar_sleeve"].get("import_ok"),
        "stateful_simulation_function_found": any("run_stateful_simulation" in k for k in available_functions),
        "variant_comparison_function_found": any("run_strategy_variant_comparison" in k for k in available_functions),
        "composer_function_found": any("compose_e1r_v0_2_variant" in k for k in available_functions),
    }

    if preflight_checks["stateful_simulation_function_found"] or preflight_checks["variant_comparison_function_found"]:
        conclusion = "UNIFIED_5Y_BACKTEST_ENGINE_ENTRYPOINT_AVAILABLE_FOR_4C2"
        recommended = "Proceed to 4C-2: run controlled full 5Y unified account backtest using the discovered stateful engine entrypoint."
    else:
        conclusion = "UNIFIED_5Y_BACKTEST_ENGINE_ENTRYPOINT_NOT_YET_RESOLVED"
        recommended = "Before full run, add a thin adapter around the existing portfolio/stateful engine entrypoint; do not reconstruct from summary artifacts."

    post_hashes = {rel(p): sha256(p) for p in FROZEN_FILES}

    report = {
        "generated_at": now(),
        "stage": "E1R_UNIFIED_5Y_FULL_ACCOUNT_V1_4C1_PREFLIGHT",
        "status": "E1R_UNIFIED_5Y_FULL_ACCOUNT_PREFLIGHT_COMPLETE",
        "policy": {
            "dashboard_changed": False,
            "strategy_logic_changed": False,
            "full_backtest_run": False,
            "canonical_backtest_written": False,
            "spec_written": True,
        },
        "spec_path": rel(SPEC_JSON),
        "spec": spec,
        "data_summary": data_summary,
        "imports": imports,
        "available_functions": available_functions,
        "source_scans": source_scans,
        "preflight_checks": preflight_checks,
        "conclusion": conclusion,
        "recommended_next_action": recommended,
        "strategy_files_unchanged": baseline_hashes == post_hashes,
        "next_stage": {
            "name": "4C-2",
            "title": "Run E1R Unified 5Y Full Account Backtest",
            "recommended_action": recommended,
        },
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R Unified 5Y Full Account V1 — 4C-1 Preflight")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append("- Status: `E1R_UNIFIED_5Y_FULL_ACCOUNT_PREFLIGHT_COMPLETE`")
    md.append("- Full backtest run: `False`")
    md.append("- Strategy logic changed: `False`")
    md.append("- Canonical backtest written: `False`")
    md.append("- Spec written: `True`")
    md.append("")
    md.append("## Preflight Checks")
    md.append("")
    md.append("```json")
    md.append(json.dumps(preflight_checks, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Available Functions")
    md.append("")
    md.append("```json")
    md.append(json.dumps(available_functions, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Data Summary")
    md.append("")
    md.append("```json")
    md.append(json.dumps(data_summary, indent=2, ensure_ascii=False)[:20000])
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append("")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {recommended}")
    md.append("")
    md.append("## Spec Path")
    md.append("")
    md.append(f"- `{rel(SPEC_JSON)}`")
    md.append("")

    REPORT_MD.write_text("\n".join(md) + "\n")

    print("Stage 4C-1 preflight complete")
    print("status:", report["status"])
    print("strategy_files_unchanged:", report["strategy_files_unchanged"])
    print("spec_path:", rel(SPEC_JSON))
    print("preflight_checks:", json.dumps(preflight_checks, ensure_ascii=False))
    print("available_functions:", json.dumps(available_functions, ensure_ascii=False))
    print("conclusion:", conclusion)
    print("recommended_next_action:", recommended)
    print("next_stage:", report["next_stage"]["name"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
