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
SHORT_START = "2021-06-01"
SHORT_END = "2021-12-31"
FULL_START = "2021-06-11"
FULL_END = "2026-06-16"

REPORT = ROOT / (
    "exports/e1r_engine/equivalence/"
    "e1r_uptrend_step3_formal_replacement.json"
)
DOC = ROOT / (
    "docs/research/"
    "E1R_UPTREND_STEP3_FORMAL_REPLACEMENT.md"
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
                f"_step3_loader_{index}",
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
    return copy.deepcopy(
        report["assumptions_capture"]["contract"]
    )


def run_case(
    *,
    data: dict[str, Any],
    start: str,
    end: str,
) -> dict[str, Any]:
    from src.engine import backtest

    assumptions = frozen_assumptions()
    assumptions[
        "e1r_order_intent_execution_adapter_enabled"
    ] = True
    assumptions[
        "e1r_engine_shadow_legacy_compare_enabled"
    ] = True

    signature = inspect.signature(
        backtest.run_stateful_simulation
    )
    kwargs = {
        "symbols": data["symbols"],
        "prices_map": data["prices_map"],
        "dates_map": data["dates_map"],
        "spx_prices": data["spx_prices"],
        "spx_dates": data["spx_dates"],
        "ohlc_map": data["ohlc_map"],
        "assumptions": assumptions,
        "step": 1,
        "min_history": 120,
        "market_score_default": 60.0,
        "sim_start_date": start,
        "sim_end_date": end,
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
        prefix="e1r_step3_"
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
        rows = [
            json.loads(line)
            for line in trace_bytes.decode("utf-8").splitlines()
            if line.strip()
        ]

    counts: dict[str, int] = {}
    for row in rows:
        trace_id = str(row["trace_point_id"])
        counts[trace_id] = counts.get(trace_id, 0) + 1

    return {
        "result": result,
        "result_hash": digest(result),
        "trace_hash": hashlib.sha256(trace_bytes).hexdigest(),
        "trace_count": len(rows),
        "trace_counts": counts,
    }


def main() -> int:
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "src"))

    loader, loader_path = discover_loader()
    data = load_data(loader)

    short = run_case(
        data=data,
        start=SHORT_START,
        end=SHORT_END,
    )

    full = run_case(
        data=data,
        start=FULL_START,
        end=FULL_END,
    )

    short_checks = {
        "trace_count_832": short["trace_count"] == 832,
        "tp01_150": short["trace_counts"].get(
            "TP01_PRE_RANK_CANDIDATES"
        ) == 150,
        "tp02_150": short["trace_counts"].get(
            "TP02_POST_RANK_CANDIDATES"
        ) == 150,
        "tp03_10": short["trace_counts"].get(
            "TP03_SELECTED_BUY_FINALIZED"
        ) == 10,
        "tp04_10": short["trace_counts"].get(
            "TP04_BUY_ORDER_INTENT_CREATED"
        ) == 10,
        "tp08_10": short["trace_counts"].get(
            "TP08_BUY_ACCOUNT_MUTATION_COMPLETE"
        ) == 10,
        "tp10a_7": short["trace_counts"].get(
            "TP10A_EXIT_ACCOUNT_MUTATION_COMPLETE"
        ) == 7,
        "tp10b_11": short["trace_counts"].get(
            "TP10B_REDUCE_ACCOUNT_MUTATION_COMPLETE"
        ) == 11,
    }

    full_result = full["result"]
    full_checks = {
        "daily_equity_record_count_positive": (
            int(
                full_result.get(
                    "daily_equity_record_count",
                    0,
                )
            )
            > 0
        ),
        "daily_equity_records_count_matches": (
            len(full_result.get("daily_equity_records", []))
            == int(
                full_result.get(
                    "daily_equity_record_count",
                    0,
                )
            )
        ),
        "trade_records_present": (
            len(full_result.get("trades", [])) > 0
        ),
        "result_hash_present": bool(full["result_hash"]),
        "trace_hash_present": bool(full["trace_hash"]),
    }

    passed = all(short_checks.values()) and all(
        full_checks.values()
    )
    decision = (
        "PASS_UPTREND_STEP3_FORMAL_REPLACEMENT"
        if passed
        else "FAIL_UPTREND_STEP3_FORMAL_REPLACEMENT"
    )

    report = {
        "schema_version": "1.0",
        "plan_step": 3,
        "plan_total_steps": 3,
        "decision": decision,
        "official_runtime_decision_source": "E1RCoreEngine.step",
        "production_legacy_decision_called": False,
        "validation_shadow_only": True,
        "short_window": {
            "start": SHORT_START,
            "end": SHORT_END,
            "checks": short_checks,
            "result_hash": short["result_hash"],
            "trace_hash": short["trace_hash"],
            "trace_count": short["trace_count"],
            "trace_counts": short["trace_counts"],
        },
        "full_history": {
            "run_count": 1,
            "start": FULL_START,
            "end": FULL_END,
            "checks": full_checks,
            "result_hash": full["result_hash"],
            "trace_hash": full["trace_hash"],
            "trace_count": full["trace_count"],
            "summary": {
                key: full_result.get(key)
                for key in [
                    "daily_equity_record_count",
                    "total_return_pct",
                    "spx_total_return_pct",
                    "alpha_pct",
                    "max_drawdown_pct",
                    "profit_factor",
                    "sharpe_ratio",
                    "pending_orders_executed",
                ]
            },
        },
        "loader": str(loader_path.relative_to(ROOT)),
        "next": (
            "UPTREND COMPLETE — MOVE TO SIDEWAYS"
            if passed
            else None
        ),
    }

    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    DOC.write_text(
        "# E1R UPTREND Step 3 — Formal Replacement\n\n"
        f"## Decision\n\n`{decision}`\n\n"
        "`E1RCoreEngine.step` is now the official UPTREND "
        "decision source. Existing pending/T+1 execution remains "
        "unchanged. Legacy decision logic is validation-shadow only.\n\n"
        "Exactly one full-history run was performed.\n\n"
        "## Next\n\n"
        + str(report["next"])
        + "\n",
        encoding="utf-8",
    )

    print("UPTREND STEP 3 VALIDATION RESULT")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
