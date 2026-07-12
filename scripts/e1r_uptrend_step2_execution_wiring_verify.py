from __future__ import annotations

import copy
import hashlib
import importlib.util
import inspect
import json
import os
import sys
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
START_DATE = "2021-06-01"
END_DATE = "2021-12-31"
REPORT = ROOT / (
    "exports/e1r_engine/equivalence/"
    "e1r_uptrend_step2_execution_wiring.json"
)
DOC = ROOT / (
    "docs/research/"
    "E1R_UPTREND_STEP2_EXECUTION_WIRING.md"
)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
        default=str,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def import_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def discover_loader() -> tuple[ModuleType, Path]:
    candidates = [
        ROOT / "scripts/export_e1_5y_core_equity.py",
        ROOT / "run_backtest.py",
    ]
    candidates.extend(sorted((ROOT / "scripts").glob("*.py")))
    seen: set[Path] = set()

    for index, path in enumerate(candidates):
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        text = path.read_text(
            encoding="utf-8",
            errors="replace",
        )
        if (
            "def load_stocks" not in text
            or "def load_index" not in text
        ):
            continue
        try:
            module = import_module(
                path,
                f"_step2_loader_{index}",
            )
        except Exception:
            continue
        if callable(getattr(module, "load_stocks", None)) and callable(
            getattr(module, "load_index", None)
        ):
            return module, path

    raise RuntimeError("canonical loader not found")


def load_data(loader: ModuleType) -> dict[str, Any]:
    stocks = loader.load_stocks()
    if not isinstance(stocks, tuple) or len(stocks) < 4:
        raise RuntimeError("unexpected load_stocks contract")

    symbols, prices_map, dates_map, ohlc_map = stocks[:4]
    spx_dates, spx_prices = loader.load_index("SPX")

    def optional(name: str) -> tuple[Any, Any]:
        try:
            return loader.load_index(name)
        except Exception:
            return None, None

    ndx_dates, ndx_prices = optional("NDX")
    sox_dates, sox_prices = optional("SOX")
    vix_dates, vix_prices = optional("VIX")

    return {
        "symbols": list(symbols),
        "prices_map": dict(prices_map),
        "dates_map": dict(dates_map),
        "ohlc_map": ohlc_map,
        "spx_dates": spx_dates,
        "spx_prices": spx_prices,
        "ndx_dates": ndx_dates,
        "ndx_prices": ndx_prices,
        "sox_dates": sox_dates,
        "sox_prices": sox_prices,
        "vix_dates": vix_dates,
        "vix_prices": vix_prices,
    }


def frozen_assumptions() -> dict[str, Any]:
    path = ROOT / (
        "exports/e1r_engine/equivalence/"
        "e1r_k2_r19_runtime_trace_equivalence.json"
    )
    report = json.loads(path.read_text(encoding="utf-8"))
    contract = copy.deepcopy(
        report["assumptions_capture"]["contract"]
    )
    if contract.get("version") != "E1R-uptrend-execution-v0.1":
        raise RuntimeError("unexpected frozen assumptions")
    return contract


def run_case(
    *,
    enabled: bool,
    data: dict[str, Any],
) -> dict[str, Any]:
    from src.engine import backtest

    signature = inspect.signature(
        backtest.run_stateful_simulation
    )
    case_assumptions = frozen_assumptions()
    case_assumptions[
        "e1r_order_intent_execution_adapter_enabled"
    ] = enabled

    kwargs = {
        "symbols": data["symbols"],
        "prices_map": data["prices_map"],
        "dates_map": data["dates_map"],
        "spx_prices": data["spx_prices"],
        "spx_dates": data["spx_dates"],
        "ohlc_map": data["ohlc_map"],
        "assumptions": case_assumptions,
        "step": 1,
        "min_history": 120,
        "market_score_default": 60.0,
        "sim_start_date": START_DATE,
        "sim_end_date": END_DATE,
        "ndx_prices": data["ndx_prices"],
        "ndx_dates": data["ndx_dates"],
        "sox_prices": data["sox_prices"],
        "sox_dates": data["sox_dates"],
        "vix_prices": data["vix_prices"],
        "vix_dates": data["vix_dates"],
    }
    kwargs = {
        key: value
        for key, value in kwargs.items()
        if key in signature.parameters
    }

    with tempfile.TemporaryDirectory(
        prefix="e1r_step2_"
    ) as temp_dir:
        trace_path = Path(temp_dir) / "trace.jsonl"
        old_enabled = os.environ.get("E1R_TRACE_ENABLED")
        old_path = os.environ.get("E1R_TRACE_PATH")
        os.environ["E1R_TRACE_ENABLED"] = "1"
        os.environ["E1R_TRACE_PATH"] = str(trace_path)

        try:
            result = backtest.run_stateful_simulation(**kwargs)
        finally:
            if old_enabled is None:
                os.environ.pop("E1R_TRACE_ENABLED", None)
            else:
                os.environ["E1R_TRACE_ENABLED"] = old_enabled
            if old_path is None:
                os.environ.pop("E1R_TRACE_PATH", None)
            else:
                os.environ["E1R_TRACE_PATH"] = old_path

        trace_bytes = trace_path.read_bytes()
        trace_rows = [
            json.loads(line)
            for line in trace_bytes.decode("utf-8").splitlines()
            if line.strip()
        ]

    counts: dict[str, int] = {}
    for row in trace_rows:
        trace_id = str(row["trace_point_id"])
        counts[trace_id] = counts.get(trace_id, 0) + 1

    return {
        "result": result,
        "result_hash": digest(result),
        "trace_bytes": trace_bytes,
        "trace_hash": hashlib.sha256(trace_bytes).hexdigest(),
        "trace_count": len(trace_rows),
        "trace_counts": counts,
    }


def main() -> int:
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "src"))
    loader, loader_path = discover_loader()
    data = load_data(loader)
    disabled = run_case(enabled=False, data=data)
    enabled = run_case(enabled=True, data=data)

    checks = {
        "result_byte_equivalent": (
            canonical(disabled["result"])
            == canonical(enabled["result"])
        ),
        "trace_byte_equivalent": (
            disabled["trace_bytes"]
            == enabled["trace_bytes"]
        ),
        "result_hash_equal": (
            disabled["result_hash"]
            == enabled["result_hash"]
        ),
        "trace_hash_equal": (
            disabled["trace_hash"]
            == enabled["trace_hash"]
        ),
        "trace_count_equal_832": (
            disabled["trace_count"]
            == enabled["trace_count"]
            == 832
        ),
        "trace_counts_equal": (
            disabled["trace_counts"]
            == enabled["trace_counts"]
        ),
        "buy_execution_count_10": (
            enabled["trace_counts"].get(
                "TP08_BUY_ACCOUNT_MUTATION_COMPLETE"
            )
            == 10
        ),
        "exit_execution_count_7": (
            enabled["trace_counts"].get(
                "TP10A_EXIT_ACCOUNT_MUTATION_COMPLETE"
            )
            == 7
        ),
        "reduce_execution_count_11": (
            enabled["trace_counts"].get(
                "TP10B_REDUCE_ACCOUNT_MUTATION_COMPLETE"
            )
            == 11
        ),
    }

    passed = all(checks.values())
    decision = (
        "PASS_UPTREND_STEP2_EXECUTION_WIRING"
        if passed
        else "FAIL_UPTREND_STEP2_EXECUTION_WIRING"
    )

    report = {
        "schema_version": "1.0",
        "plan_step": 2,
        "plan_total_steps": 3,
        "stage": "UPTREND-STEP2-EXECUTION-WIRING",
        "decision": decision,
        "window": {
            "start": START_DATE,
            "end": END_DATE,
        },
        "loader": str(loader_path.relative_to(ROOT)),
        "checks": checks,
        "disabled": {
            "result_hash": disabled["result_hash"],
            "trace_hash": disabled["trace_hash"],
            "trace_count": disabled["trace_count"],
            "trace_counts": disabled["trace_counts"],
        },
        "enabled": {
            "result_hash": enabled["result_hash"],
            "trace_hash": enabled["trace_hash"],
            "trace_count": enabled["trace_count"],
            "trace_counts": enabled["trace_counts"],
        },
        "scope": {
            "engine_buy_to_legacy_pending_mapping": True,
            "legacy_reduce_exit_lifted_to_order_intent": True,
            "legacy_execution_rules_modified": False,
            "market_gate_modified": False,
            "uptrend_decision_modified": False,
            "account_mutation_rules_modified": False,
            "add_supported": False,
            "full_5y_run": False,
        },
        "next_step": (
            "UPTREND STEP 3 — FORMAL REPLACEMENT"
            if passed
            else None
        ),
    }

    REPORT.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    DOC.write_text(
        "# E1R UPTREND Step 2 — Execution Wiring\n\n"
        f"## Decision\n\n`{decision}`\n\n"
        "## Fixed plan\n\n"
        "- Step 1: Decision equivalence — PASS\n"
        "- Step 2: Execution wiring — "
        + ("PASS" if passed else "FAIL")
        + "\n"
        "- Step 3: Formal replacement — pending\n\n"
        "## Boundary\n\n"
        "A thin adapter translates OrderIntent into the existing "
        "legacy pending/T+1 execution path. Existing REDUCE and EXIT "
        "payloads are lifted to OrderIntent and restored without "
        "changing their frozen semantics.\n\n"
        "## Validation\n\n"
        "- Adapter disabled vs enabled result equivalence\n"
        "- Adapter disabled vs enabled JSONL byte equivalence\n"
        "- Window: 2021-06-01 through 2021-12-31\n"
        "- BUY executions: 10\n"
        "- EXIT executions: 7\n"
        "- REDUCE executions: 11\n"
        "- No full 5Y run\n\n"
        "## Exclusions\n\n"
        "- No new execution engine\n"
        "- No AccountState redesign\n"
        "- No Market Gate or strategy change\n"
        "- No ADD or SIDEWAYS work\n\n"
        "## Next\n\n"
        + str(report["next_step"])
        + "\n",
        encoding="utf-8",
    )

    print("UPTREND STEP 2 VALIDATION RESULT")
    print(
        json.dumps(
            {
                "decision": decision,
                "checks": checks,
                "trace_counts": enabled["trace_counts"],
                "next_step": report["next_step"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
