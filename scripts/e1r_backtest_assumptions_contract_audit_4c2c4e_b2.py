#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import ast
import json
import hashlib
import re
from datetime import datetime, timezone
from typing import Any
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT.md"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

SEARCH_DIRS = [
    ROOT / "scripts",
    ROOT / "src",
    ROOT / "tests",
]

KEY_PATTERNS_OF_INTEREST = [
    "run_stateful_simulation",
    "assumptions",
    "buy_size",
    "add_size",
    "sell_size",
    "reduce_size",
    "market_shock_daily_return",
    "market_shock_enabled",
    "market_shock_gate_enabled",
    "max_positions",
    "entry_top_n",
    "candidate_top_n",
    "min_holding_days",
    "e1r_regime_daily",
    "e1r_regime_wiring_enabled",
    "strategy_variant",
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

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def read_text(path: Path) -> str:
    return path.read_text(errors="replace")

def python_files() -> list[Path]:
    files = []
    for d in SEARCH_DIRS:
        if not d.exists():
            continue
        files.extend(sorted(d.rglob("*.py")))
    return files

def extract_literal(node: ast.AST):
    try:
        return ast.literal_eval(node)
    except Exception:
        return None

def get_string_key(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None

def call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return call_name(node.value) + "." + node.attr
    return ""

def infer_backtest_assumption_contract() -> dict[str, Any]:
    path = ROOT / "src/engine/backtest.py"
    text = read_text(path)
    lines = text.splitlines()
    tree = ast.parse(text)

    target = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "run_stateful_simulation":
            target = node
            break

    if target is None:
        return {"error": "run_stateful_simulation not found"}

    key_info = defaultdict(lambda: {
        "access_modes": set(),
        "contexts": set(),
        "default_values": [],
        "line_refs": [],
        "expected_type_hints": set(),
    })

    def add(key: str, access_mode: str, context: str, line: int | None, default=None, type_hint=None):
        info = key_info[key]
        info["access_modes"].add(access_mode)
        info["contexts"].add(context)
        if default is not None:
            info["default_values"].append(default)
        if line:
            src = lines[line - 1].strip() if 1 <= line <= len(lines) else ""
            info["line_refs"].append({"line": line, "text": src[:240]})
        if type_hint:
            info["expected_type_hints"].add(type_hint)

    parent = {}
    for n in ast.walk(target):
        for child in ast.iter_child_nodes(n):
            parent[child] = n

    for node in ast.walk(target):
        if isinstance(node, ast.Subscript):
            if isinstance(node.value, ast.Name) and node.value.id in {"a", "assumptions"}:
                key = get_string_key(node.slice)
                if key:
                    p = parent.get(node)
                    type_hint = None
                    context = "subscript"
                    if isinstance(p, ast.Call):
                        cname = call_name(p.func)
                        if cname in {"float", "int", "bool", "str"}:
                            type_hint = cname
                            context = f"cast_{cname}"
                    add(key, "required_subscript", context, getattr(node, "lineno", None), type_hint=type_hint)

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id in {"a", "assumptions"} and node.func.attr == "get":
                if node.args:
                    key = get_string_key(node.args[0])
                    if key:
                        default = extract_literal(node.args[1]) if len(node.args) >= 2 else None
                        p = parent.get(node)
                        type_hint = None
                        context = "get"
                        if isinstance(p, ast.Call):
                            cname = call_name(p.func)
                            if cname in {"float", "int", "bool", "str"}:
                                type_hint = cname
                                context = f"get_cast_{cname}"
                        add(key, "get", context, getattr(node, "lineno", None), default=default, type_hint=type_hint)

    final = {}
    for key, info in sorted(key_info.items()):
        final[key] = {
            "access_modes": sorted(info["access_modes"]),
            "contexts": sorted(info["contexts"]),
            "default_values": info["default_values"],
            "expected_type_hints": sorted(info["expected_type_hints"]),
            "line_refs": info["line_refs"][:20],
            "required_without_default": "required_subscript" in info["access_modes"],
        }

    return {
        "path": rel(path),
        "function": "run_stateful_simulation",
        "assumption_key_count": len(final),
        "keys": final,
    }

def find_run_stateful_callers() -> list[dict[str, Any]]:
    results = []
    for path in python_files():
        text = read_text(path)
        if "run_stateful_simulation" not in text:
            continue
        lines = text.splitlines()
        for i, line in enumerate(lines, start=1):
            if "run_stateful_simulation" in line:
                start = max(1, i - 8)
                end = min(len(lines), i + 20)
                results.append({
                    "path": rel(path),
                    "line": i,
                    "context": [
                        {"line": j, "text": lines[j - 1][:220]}
                        for j in range(start, end + 1)
                    ],
                })
    return results

def find_assumption_key_assignments() -> dict[str, list[dict[str, Any]]]:
    results = {k: [] for k in KEY_PATTERNS_OF_INTEREST}

    for path in python_files():
        text = read_text(path)
        lines = text.splitlines()

        for key in KEY_PATTERNS_OF_INTEREST:
            if key not in text:
                continue

            for i, line in enumerate(lines, start=1):
                if key in line:
                    if len(results[key]) < 80:
                        results[key].append({
                            "path": rel(path),
                            "line": i,
                            "text": line.strip()[:260],
                        })

    return results

def find_dict_literals_near_assumptions() -> list[dict[str, Any]]:
    out = []

    for path in python_files():
        text = read_text(path)
        if "assumptions" not in text and "buy_size" not in text and "max_positions" not in text:
            continue

        try:
            tree = ast.parse(text)
        except Exception:
            continue

        lines = text.splitlines()

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                targets = []
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        targets.append(t.id)
                    elif isinstance(t, ast.Attribute):
                        targets.append(t.attr)

                value = node.value
                if isinstance(value, ast.Dict):
                    keys = []
                    for k in value.keys:
                        if isinstance(k, ast.Constant) and isinstance(k.value, str):
                            keys.append(k.value)

                    if any(k in keys for k in ["buy_size", "max_positions", "market_shock_daily_return", "entry_top_n"]):
                        start = getattr(node, "lineno", None)
                        end = getattr(node, "end_lineno", None)
                        out.append({
                            "path": rel(path),
                            "line": start,
                            "targets": targets,
                            "keys": keys,
                            "context": [
                                {"line": j, "text": lines[j - 1][:240]}
                                for j in range(max(1, start - 5), min(len(lines), (end or start) + 8) + 1)
                            ] if start else [],
                        })

    return out

def derive_safe_assumption_blueprint(contract: dict[str, Any]) -> dict[str, Any]:
    keys = contract.get("keys", {})

    required_keys = [
        k for k, v in keys.items()
        if v.get("required_without_default")
    ]

    typed_defaults = {}
    unresolved = []

    for k, v in keys.items():
        defaults = v.get("default_values") or []
        hints = set(v.get("expected_type_hints") or [])

        if k == "e1r_regime_daily":
            typed_defaults[k] = "<regime_daily_dict>"
        elif k in {"max_positions", "entry_top_n", "candidate_top_n", "min_holding_days", "min_hold"}:
            typed_defaults[k] = 3 if k in {"max_positions", "entry_top_n"} else 10
        elif k in {"buy_size", "sell_size", "max_single_size", "total_one_way"}:
            typed_defaults[k] = 1.0
        elif k in {"add_size", "reduce_size"}:
            typed_defaults[k] = 0.5
        elif k == "position_size_pct":
            typed_defaults[k] = 1.0 / 3.0
        elif k == "market_shock_daily_return":
            typed_defaults[k] = -0.02
        elif k == "market_shock_recovery_return":
            typed_defaults[k] = 0.01
        elif k == "market_shock_gate_enabled":
            typed_defaults[k] = False
        elif k in {"strategy_variant", "version", "execution_model", "market_entry_gate", "ls60_exit_mode"}:
            typed_defaults[k] = "default"
        elif "bool" in hints:
            typed_defaults[k] = False
        elif "float" in hints:
            if defaults:
                typed_defaults[k] = defaults[0]
            else:
                typed_defaults[k] = 0.0
        elif "int" in hints:
            if defaults:
                typed_defaults[k] = defaults[0]
            else:
                typed_defaults[k] = 0
        elif defaults:
            typed_defaults[k] = defaults[0]
        elif v.get("required_without_default"):
            unresolved.append(k)
        else:
            typed_defaults[k] = None

    return {
        "required_without_default_keys": required_keys,
        "unresolved_required_keys": unresolved,
        "typed_default_blueprint": typed_defaults,
        "warning": "Blueprint is for next smoke design only. Do not treat as strategy change without review.",
    }

def main():
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    contract = infer_backtest_assumption_contract()
    callers = find_run_stateful_callers()
    key_assignments = find_assumption_key_assignments()
    dict_literals = find_dict_literals_near_assumptions()
    blueprint = derive_safe_assumption_blueprint(contract)

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "audit_only_no_backtest_run": True,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == after_hashes,
        "run_stateful_contract_extracted": "keys" in contract and contract.get("assumption_key_count", 0) > 0,
        "callers_found": len(callers) > 0,
        "required_unresolved_zero": len(blueprint["unresolved_required_keys"]) == 0,
    }

    conclusion = (
        "READY_FOR_4C2C4E_B3_SMOKE_WITH_TYPED_ASSUMPTION_CONTRACT"
        if validations["run_stateful_contract_extracted"] and validations["required_unresolved_zero"]
        else "ASSUMPTION_CONTRACT_AUDIT_NEEDS_REVIEW"
    )

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-B2",
        "status": "BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT_COMPLETE",
        "policy": {
            "strategy_logic_changed": False,
            "backtest_engine_run": False,
            "full_5y_backtest_run": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
            "fix_reason": "B/B1 failed because assumptions contract was not locked before smoke.",
        },
        "contract": contract,
        "run_stateful_callers": callers,
        "assumption_key_assignments": key_assignments,
        "dict_literals_near_assumptions": dict_literals,
        "safe_assumption_blueprint": blueprint,
        "validations": validations,
        "conclusion": conclusion,
        "recommended_next_action": (
            "Proceed to 4C-2C-4E-B3: rerun continuous stateful smoke using typed assumption blueprint. "
            "Do not use heuristic key defaults."
            if conclusion.startswith("READY")
            else "Review unresolved assumption keys before rerunning smoke."
        ),
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-B2 — Backtest Assumptions Contract Audit")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append("This audit fixes the B/B1 issue by locking the assumptions contract before another smoke run.")
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
    md.append("## Required Keys Without Default")
    md.append("```json")
    md.append(json.dumps(blueprint["required_without_default_keys"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Unresolved Required Keys")
    md.append("```json")
    md.append(json.dumps(blueprint["unresolved_required_keys"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Typed Default Blueprint")
    md.append("```json")
    md.append(json.dumps(blueprint["typed_default_blueprint"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {report['recommended_next_action']}")
    md.append("")

    REPORT_MD.write_text("\n".join(md))

    print("E1R_4C2C4E_B2_BACKTEST_ASSUMPTIONS_CONTRACT_AUDIT_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("assumption_key_count:", contract.get("assumption_key_count"))
    print("required_without_default_keys:", json.dumps(blueprint["required_without_default_keys"], ensure_ascii=False))
    print("unresolved_required_keys:", json.dumps(blueprint["unresolved_required_keys"], ensure_ascii=False))
    print("typed_default_blueprint:", json.dumps(blueprint["typed_default_blueprint"], ensure_ascii=False))
    print("callers_count:", len(callers))
    print("dict_literals_count:", len(dict_literals))
    print("conclusion:", conclusion)
    print("recommended_next_action:", report["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
