#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import tempfile
from pathlib import Path
from typing import Any

ENGINE_ID = "FD-M3180125-SP500-TOP3-engine"
RUN_MODE = "BACKTEST"
VARIANT_ID = "E1R_CAPPED_ATR_A0_V1"
DISPLAY_NAME = "E1R CAPPED-ATR Engine"

VARIANT_JSON_PATH = "$"
DAILY_JSON_PATH = f"{VARIANT_JSON_PATH}.daily_equity_records"
TRADES_JSON_PATH = f"{VARIANT_JSON_PATH}.trades"
FINAL_EQUITY_JSON_PATH = f"{VARIANT_JSON_PATH}.final_equity"
SETTLEMENT_JSON_PATH = (
    f"{VARIANT_JSON_PATH}.sim_end_liquidation_record"
)

EXPECTED_REGULAR_ROW_COUNT = 1259
EXPECTED_TRADE_COUNT = 92
EXPECTED_FIRST_DATE = "2021-06-11"
EXPECTED_LAST_REGULAR_DATE = "2026-06-16"
EXPECTED_SETTLEMENT_DATE = "2026-06-18"
EXPECTED_INITIAL_EQUITY = 100000.0
EXPECTED_LAST_REGULAR_EQUITY = 310000.01
EXPECTED_FINAL_EQUITY = 312687.26
VALUE_TOLERANCE = 0.02


class ExportValidationError(RuntimeError):
    pass


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(1024 * 1024)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def is_finite_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ExportValidationError(message)


def approximately_equal(left: Any, right: float) -> bool:
    return (
        is_finite_number(left)
        and abs(float(left) - right) <= VALUE_TOLERANCE
    )


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = (
        json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
            sort_keys=False,
        )
        + "\n"
    ).encode("utf-8")

    with tempfile.NamedTemporaryFile(
        mode="wb",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as temp:
        temp.write(content)
        temp.flush()
        os.fsync(temp.fileno())
        temp_path = Path(temp.name)

    temp_path.replace(path)


def write_csv_atomic(
    path: Path,
    rows: list[dict[str, Any]],
    fieldnames: list[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as temp:
        writer = csv.DictWriter(
            temp,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
        temp.flush()
        os.fsync(temp.fileno())
        temp_path = Path(temp.name)

    temp_path.replace(path)


def validate_and_extract(
    root: dict[str, Any],
) -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    variant = root
    require(
        variant.get("strategy_variant") == VARIANT_ID,
        "Direct result has the wrong strategy_variant",
    )
    require(
        variant.get("strategy_display_name") == DISPLAY_NAME,
        "Direct result has the wrong strategy_display_name",
    )

    require(isinstance(variant, dict), "Variant must be an object")

    daily = variant.get("daily_equity_records")
    trades = variant.get("trades")
    settlement = variant.get("sim_end_liquidation_record")
    final_equity = variant.get("final_equity")

    require(isinstance(daily, list), "daily_equity_records must be a list")
    require(isinstance(trades, list), "trades must be a list")
    require(isinstance(settlement, dict), "settlement record must be an object")
    require(
        len(variant.get("capped_atr_stop_trace", [])) == 8,
        "Expected exactly 8 CAPPED-ATR trigger trace rows",
    )
    require(
        variant.get("executed_exit_reason_distribution", {}).get(
            "HARD_LOSS_STOP"
        )
        == 3,
        "Expected exactly 3 executed HARD_LOSS_STOP exits",
    )

    require(
        len(daily) == EXPECTED_REGULAR_ROW_COUNT,
        f"Expected {EXPECTED_REGULAR_ROW_COUNT} daily rows, got {len(daily)}",
    )
    require(
        len(trades) == EXPECTED_TRADE_COUNT,
        f"Expected {EXPECTED_TRADE_COUNT} trades, got {len(trades)}",
    )

    required_daily_fields = {
        "date",
        "cash",
        "positions_value",
        "total_equity",
        "daily_return_pct",
        "drawdown_pct",
        "exposure_pct",
        "open_positions_count",
        "pending_orders_count",
        "market_gate_state",
        "spx_regime",
        "spx_close",
        "spx_day_return_pct",
        "event",
    }

    dates: list[str] = []

    for index, row in enumerate(daily):
        require(
            isinstance(row, dict),
            f"daily_equity_records[{index}] must be an object",
        )
        missing = required_daily_fields - set(row)
        require(
            not missing,
            f"daily_equity_records[{index}] missing {sorted(missing)}",
        )

        date = row["date"]
        require(
            isinstance(date, str) and date,
            f"daily_equity_records[{index}] has invalid date",
        )
        dates.append(date)

        require(
            is_finite_number(row["total_equity"]),
            f"daily_equity_records[{index}] invalid total_equity",
        )
        require(
            is_finite_number(row["spx_close"])
            and float(row["spx_close"]) > 0,
            f"daily_equity_records[{index}] invalid spx_close",
        )

    require(dates == sorted(dates), "Daily dates are not ordered")
    require(len(dates) == len(set(dates)), "Daily dates are not unique")

    require(
        dates[0] == EXPECTED_FIRST_DATE,
        f"Unexpected first date: {dates[0]}",
    )
    require(
        dates[-1] == EXPECTED_LAST_REGULAR_DATE,
        f"Unexpected last regular date: {dates[-1]}",
    )
    require(
        approximately_equal(
            daily[0]["total_equity"],
            EXPECTED_INITIAL_EQUITY,
        ),
        f"Unexpected initial equity: {daily[0]['total_equity']}",
    )
    require(
        approximately_equal(
            daily[-1]["total_equity"],
            EXPECTED_LAST_REGULAR_EQUITY,
        ),
        f"Unexpected last regular equity: {daily[-1]['total_equity']}",
    )
    require(
        approximately_equal(final_equity, EXPECTED_FINAL_EQUITY),
        f"Unexpected authoritative final equity: {final_equity}",
    )
    expected_metrics = {
        "total_return_pct": 212.69,
        "cagr_pct": 25.59,
        "max_drawdown_pct": 25.66,
        "sharpe_ratio": 0.76,
        "profit_factor": 2.36,
        "number_of_trades": 92,
        "exposure_pct": 69.2,
    }
    for key, expected in expected_metrics.items():
        require(
            approximately_equal(variant.get(key), expected),
            f"Unexpected {key}: {variant.get(key)}",
        )

    require(
        settlement.get("date") == EXPECTED_SETTLEMENT_DATE,
        f"Unexpected settlement date: {settlement.get('date')}",
    )
    require(
        settlement.get("event") == "SIM_END_LIQUIDATION",
        f"Unexpected settlement event: {settlement.get('event')}",
    )
    require(
        approximately_equal(
            settlement.get("total_equity"),
            EXPECTED_FINAL_EQUITY,
        ),
        "Settlement total_equity does not match final_equity",
    )
    require(
        approximately_equal(
            settlement.get("cash"),
            EXPECTED_FINAL_EQUITY,
        ),
        "Settlement cash does not match final_equity",
    )
    require(
        approximately_equal(settlement.get("positions_value"), 0.0),
        "Settlement positions_value must be zero",
    )

    actual_sim_end_trades = [
        trade
        for trade in trades
        if isinstance(trade, dict)
        and (
            trade.get("is_sim_end") is True
            or trade.get("exit_signal") == "SIM_END"
            or trade.get("exit_type") == "SIM_END"
        )
    ]

    require(
        len(actual_sim_end_trades) == 3,
        f"Expected 3 actual SIM_END trades, got {len(actual_sim_end_trades)}",
    )

    require(
        {trade.get("symbol") for trade in actual_sim_end_trades}
        == {"MRVL", "DELL", "HUM"},
        "Unexpected SIM_END trade symbols",
    )

    return variant, daily, trades, settlement


def build_regular_curve(
    daily: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    initial_spx = float(daily[0]["spx_close"])
    curve: list[dict[str, Any]] = []

    for sequence, row in enumerate(daily, start=1):
        curve.append({
            "sequence": sequence,
            "date": row["date"],
            "point_type": "REGULAR_EOD",
            "event": row["event"],
            "engine_equity": float(row["total_equity"]),
            "cash": float(row["cash"]),
            "positions_value": float(row["positions_value"]),
            "spx_close": float(row["spx_close"]),
            "spx_benchmark_equity": round(
                EXPECTED_INITIAL_EQUITY
                * float(row["spx_close"])
                / initial_spx,
                6,
            ),
            "daily_return_pct": row["daily_return_pct"],
            "spx_day_return_pct": row["spx_day_return_pct"],
            "drawdown_pct": row["drawdown_pct"],
            "exposure_pct": row["exposure_pct"],
            "open_positions_count": row["open_positions_count"],
            "pending_orders_count": row["pending_orders_count"],
            "market_gate_state": row["market_gate_state"],
            "spx_regime": row["spx_regime"],
        })

    return curve


def build_official_curve(
    regular_curve: list[dict[str, Any]],
    settlement: dict[str, Any],
) -> list[dict[str, Any]]:
    official_curve = [dict(row) for row in regular_curve]

    official_curve.append({
        "sequence": len(official_curve) + 1,
        "date": settlement["date"],
        "point_type": "FINAL_SETTLEMENT",
        "event": "SIM_END_LIQUIDATION",
        "engine_equity": float(settlement["total_equity"]),
        "cash": float(settlement["cash"]),
        "positions_value": float(settlement["positions_value"]),
        "spx_close": None,
        "spx_benchmark_equity": None,
        "daily_return_pct": None,
        "spx_day_return_pct": None,
        "drawdown_pct": None,
        "exposure_pct": 0.0,
        "open_positions_count": 0,
        "pending_orders_count": 0,
        "market_gate_state": None,
        "spx_regime": None,
        "settlement_delta_from_last_regular_eod": round(
            EXPECTED_FINAL_EQUITY
            - EXPECTED_LAST_REGULAR_EQUITY,
            6,
        ),
    })

    return official_curve


def scalar_variant_metrics(
    variant: dict[str, Any],
) -> dict[str, Any]:
    result: dict[str, Any] = {}

    for key, value in variant.items():
        if value is None or isinstance(value, (str, int, float, bool)):
            result[key] = value

    return result


def build_manifest(
    output_dir: Path,
    source_path: Path,
    source_sha256: str,
    operational_head: str,
) -> dict[str, Any]:
    artifacts: list[dict[str, Any]] = []

    for path in sorted(output_dir.iterdir()):
        if not path.is_file():
            continue
        if path.name == "current_manifest.json":
            continue

        artifacts.append({
            "filename": path.name,
            "relative_path": path.name,
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        })

    return {
        "schema_version": "1.0.0",
        "manifest_type": "CURRENT_OFFICIAL_ARTIFACT_MANIFEST",
        "engine_id": ENGINE_ID,
        "run_mode": RUN_MODE,
        "artifact_status": "OFFICIAL",
        "formal_variant": VARIANT_ID,
        "canonical_strategy_commit": operational_head,
        "operational_repository_head": operational_head,
        "source": {
            "path_at_export_time": str(source_path),
            "sha256": source_sha256,
        },
        "date_boundaries": {
            "backtest_start": EXPECTED_FIRST_DATE,
            "last_regular_eod": EXPECTED_LAST_REGULAR_DATE,
            "formal_final_settlement": EXPECTED_SETTLEMENT_DATE,
        },
        "artifacts": artifacts,
    }


def export(
    source_path: Path,
    output_dir: Path,
    operational_head: str,
) -> dict[str, Any]:
    source_sha = sha256_file(source_path)

    root = json.loads(source_path.read_text(encoding="utf-8"))
    require(isinstance(root, dict), "Source root must be an object")

    variant, daily, trades, settlement = validate_and_extract(root)

    regular_curve = build_regular_curve(daily)
    official_curve = build_official_curve(regular_curve, settlement)

    actual_sim_end_trades = [
        trade
        for trade in trades
        if isinstance(trade, dict)
        and (
            trade.get("is_sim_end") is True
            or trade.get("exit_signal") == "SIM_END"
            or trade.get("exit_type") == "SIM_END"
        )
    ]

    contract = {
        "schema_version": "1.0.0",
        "contract_name": (
            "FD-M3180125-SP500-TOP3-engine "
            "Official Backtest Artifact Contract"
        ),
        "engine_id": ENGINE_ID,
        "run_mode": RUN_MODE,
        "artifact_status": "OFFICIAL",
        "formal_variant": VARIANT_ID,
        "canonical_strategy_commit": operational_head,
        "source_result_sha256": source_sha,
        "source_json_paths": {
            "variant": VARIANT_JSON_PATH,
            "regular_eod_curve": DAILY_JSON_PATH,
            "trades": TRADES_JSON_PATH,
            "authoritative_final_equity": FINAL_EQUITY_JSON_PATH,
            "final_settlement": SETTLEMENT_JSON_PATH,
        },
        "equity_semantics": {
            "regular_eod_curve": {
                "point_type": "REGULAR_EOD",
                "row_count": EXPECTED_REGULAR_ROW_COUNT,
                "first_date": EXPECTED_FIRST_DATE,
                "last_date": EXPECTED_LAST_REGULAR_DATE,
                "last_equity": EXPECTED_LAST_REGULAR_EQUITY,
                "description": (
                    "Regular end-of-day mark-to-market account states."
                ),
            },
            "formal_final_settlement": {
                "point_type": "FINAL_SETTLEMENT",
                "date": EXPECTED_SETTLEMENT_DATE,
                "event": "SIM_END_LIQUIDATION",
                "final_equity": EXPECTED_FINAL_EQUITY,
                "description": (
                    "Backtest-only terminal liquidation state. "
                    "It must not be used as the Forward seed state."
                ),
            },
            "official_curve_policy": (
                "Preserve all regular EOD points and append one explicitly "
                "typed FINAL_SETTLEMENT point. The settlement point must "
                "never be represented as an ordinary market EOD point."
            ),
        },
        "benchmark_semantics": {
            "source": "regular_eod_curve[].spx_close",
            "normalization_formula": (
                "spx_benchmark_equity = "
                "100000 * current_spx_close / first_spx_close"
            ),
            "settlement_point_policy": (
                "No synthetic SPX value is generated for the "
                "FINAL_SETTLEMENT point."
            ),
        },
        "trade_semantics": {
            "row_count": EXPECTED_TRADE_COUNT,
            "actual_sim_end_trade_count": 3,
            "actual_sim_end_symbols": ["DELL", "HUM", "MRVL"],
            "sim_end_filter": (
                "is_sim_end == true OR exit_signal == SIM_END "
                "OR exit_type == SIM_END"
            ),
        },
        "forward_boundary": {
            "forward_data_start": "2026-06-19",
            "backtest_final_settlement_is_forward_seed": False,
            "forward_seed_requirement": (
                "Use a separately proven pre-liquidation continuous "
                "account snapshot preserving open positions, cost basis, "
                "origins, pending orders, and strategy state."
            ),
        },
        "prohibited_transformations": [
            "Do not rerun the strategy during export",
            "Do not change strategy or execution semantics",
            "Do not infer a Forward seed from the liquidated cash state",
            "Do not classify all trades containing an is_sim_end key as SIM_END",
            "Do not synthesize an SPX close for the final settlement point",
        ],
    }

    metrics = {
        "schema_version": "1.0.0",
        "engine_id": ENGINE_ID,
        "run_mode": RUN_MODE,
        "formal_variant": VARIANT_ID,
        "initial_equity": EXPECTED_INITIAL_EQUITY,
        "last_regular_eod_equity": EXPECTED_LAST_REGULAR_EQUITY,
        "formal_final_equity": EXPECTED_FINAL_EQUITY,
        "formal_total_return_pct": round(
            (
                EXPECTED_FINAL_EQUITY
                / EXPECTED_INITIAL_EQUITY
                - 1.0
            )
            * 100.0,
            6,
        ),
        "last_regular_eod_date": EXPECTED_LAST_REGULAR_DATE,
        "formal_final_settlement_date": EXPECTED_SETTLEMENT_DATE,
        "regular_eod_point_count": len(regular_curve),
        "official_curve_point_count": len(official_curve),
        "trade_count": len(trades),
        "actual_sim_end_trade_count": len(actual_sim_end_trades),
        "settlement_delta_from_last_regular_eod": round(
            EXPECTED_FINAL_EQUITY
            - EXPECTED_LAST_REGULAR_EQUITY,
            6,
        ),
        "spx_first_close": regular_curve[0]["spx_close"],
        "spx_last_regular_close": regular_curve[-1]["spx_close"],
        "spx_total_return_pct": round(
            (
                regular_curve[-1]["spx_close"]
                / regular_curve[0]["spx_close"]
                - 1.0
            )
            * 100.0,
            6,
        ),
        "source_variant_scalar_fields": scalar_variant_metrics(variant),
    }

    provenance = {
        "schema_version": "1.0.0",
        "engine_id": ENGINE_ID,
        "run_mode": RUN_MODE,
        "formal_variant": VARIANT_ID,
        "canonical_strategy_commit": operational_head,
        "operational_repository_head": operational_head,
        "source_result": {
            "path_at_export_time": str(source_path),
            "sha256": source_sha,
        },
        "export_character": {
            "pure_export": True,
            "strategy_executed": False,
            "backtest_rerun": False,
            "strategy_logic_modified": False,
            "account_logic_modified": False,
            "execution_logic_modified": False,
        },
    }

    final_settlement = {
        "schema_version": "1.0.0",
        "engine_id": ENGINE_ID,
        "run_mode": RUN_MODE,
        "formal_variant": VARIANT_ID,
        "point_type": "FINAL_SETTLEMENT",
        "source_json_path": SETTLEMENT_JSON_PATH,
        "authoritative_final_equity_json_path": FINAL_EQUITY_JSON_PATH,
        "record": settlement,
        "settlement_delta_from_last_regular_eod": round(
            EXPECTED_FINAL_EQUITY
            - EXPECTED_LAST_REGULAR_EQUITY,
            6,
        ),
        "forward_seed_eligible": False,
    }

    output_dir.mkdir(parents=True, exist_ok=True)

    write_json_atomic(output_dir / "artifact_contract.json", contract)
    write_json_atomic(
        output_dir / "backtest_equity_curve.json",
        official_curve,
    )
    write_csv_atomic(
        output_dir / "backtest_equity_curve.csv",
        official_curve,
        [
            "sequence",
            "date",
            "point_type",
            "event",
            "engine_equity",
            "cash",
            "positions_value",
            "spx_close",
            "spx_benchmark_equity",
            "daily_return_pct",
            "spx_day_return_pct",
            "drawdown_pct",
            "exposure_pct",
            "open_positions_count",
            "pending_orders_count",
            "market_gate_state",
            "spx_regime",
            "settlement_delta_from_last_regular_eod",
        ],
    )
    write_json_atomic(
        output_dir / "regular_eod_account_records.json",
        daily,
    )
    write_json_atomic(output_dir / "official_trades.json", trades)
    write_json_atomic(
        output_dir / "actual_sim_end_trades.json",
        actual_sim_end_trades,
    )
    write_json_atomic(
        output_dir / "final_settlement.json",
        final_settlement,
    )
    write_json_atomic(output_dir / "official_metrics.json", metrics)
    write_json_atomic(output_dir / "provenance.json", provenance)

    manifest = build_manifest(
        output_dir=output_dir,
        source_path=source_path,
        source_sha256=source_sha,
        operational_head=operational_head,
    )
    write_json_atomic(output_dir / "current_manifest.json", manifest)

    decision = {
        "decision": "PASS_AE_STEP_1_CAPPED_ATR_OFFICIAL_BACKTEST_ARTIFACT_EXPORT",
        "engine_id": ENGINE_ID,
        "run_mode": RUN_MODE,
        "formal_variant": VARIANT_ID,
        "canonical_strategy_commit": operational_head,
        "operational_repository_head": operational_head,
        "source_result_sha256": source_sha,
        "regular_eod_point_count": len(regular_curve),
        "official_curve_point_count": len(official_curve),
        "trade_count": len(trades),
        "actual_sim_end_trade_count": len(actual_sim_end_trades),
        "last_regular_eod_equity": regular_curve[-1]["engine_equity"],
        "formal_final_equity": official_curve[-1]["engine_equity"],
        "output_directory": str(output_dir),
    }

    write_json_atomic(
        output_dir / "STEP1_OFFICIAL_EXPORT_DECISION.json",
        decision,
    )

    manifest = build_manifest(
        output_dir=output_dir,
        source_path=source_path,
        source_sha256=source_sha,
        operational_head=operational_head,
    )
    write_json_atomic(output_dir / "current_manifest.json", manifest)

    return decision


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--operational-head", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    decision = export(
        source_path=args.source,
        output_dir=args.output_dir,
        operational_head=args.operational_head,
    )

    print(json.dumps(decision, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
