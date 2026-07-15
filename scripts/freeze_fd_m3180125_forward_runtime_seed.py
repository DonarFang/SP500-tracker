from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


ENGINE_ID = "FD-M3180125-SP500-TOP3-engine"
FORMAL_VARIANT = "E1R_REGIME_AWARE_V0_2_STATEFUL_MAX3"

CANONICAL_STRATEGY_COMMIT = (
    "d7eb4dc0288433c68332e4607ae261d2f615d371"
)

OFFICIAL_BACKTEST_COMMIT = (
    "abd5aa74d4a3f442cd42b94296adbec6fcf39759"
)

CANONICAL_RESULT_SHA256 = (
    "d8a5ea27ba0d8a7e8f7042bcbd09ffe"
    "67799f3b094a81cb92141a70f3075d593"
)

EXPECTED_SOURCE_DECISION = (
    "PASS_RECONSTRUCTED_ACCOUNT_ECONOMICS_"
    "HOLD_RUNTIME_STATE"
)

FORMAL_DECISION = (
    "PASS_FORWARD_RUNTIME_SEED_CONTRACT_FROZEN"
)

SEED_DATE = "2026-06-18"
FORWARD_START_DATE = "2026-06-19"

EXPECTED_SYMBOLS = {"MRVL", "DELL", "HUM"}
EXPECTED_FINAL_EQUITY = 281711.79

ECONOMIC_TOLERANCE = 0.02
CASH_RECONSTRUCTION_TOLERANCE = 1.00


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        while True:
            block = stream.read(1024 * 1024)

            if not block:
                break

            digest.update(block)

    return digest.hexdigest()


def write_json_atomic(
    path: Path,
    payload: Any,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as stream:
        json.dump(
            payload,
            stream,
            indent=2,
            ensure_ascii=False,
        )
        stream.write("\n")
        temporary_path = Path(stream.name)

    os.replace(temporary_path, path)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def approximately_equal(
    left: float,
    right: float,
    tolerance: float = ECONOMIC_TOLERANCE,
) -> bool:
    return abs(float(left) - float(right)) <= tolerance


def validate_sources(
    state: dict[str, Any],
    decision: dict[str, Any],
) -> None:
    if decision.get("decision") != EXPECTED_SOURCE_DECISION:
        raise ValueError(
            "Unexpected targeted reconciliation decision: "
            f"{decision.get('decision')!r}"
        )

    if state.get("record_type") != (
        "DERIVED_RECONSTRUCTED_PRE_SIM_END_ACCOUNT_STATE"
    ):
        raise ValueError("Unexpected reconstructed record type")

    if state.get("is_original_runtime_record") is not False:
        raise ValueError(
            "Derived record must not be marked as original"
        )

    if state.get(
        "must_not_be_represented_as_original_trace"
    ) is not True:
        raise ValueError(
            "Derived record must preserve its evidence boundary"
        )

    if state.get("date") != SEED_DATE:
        raise ValueError("Unexpected seed date")

    if state.get("engine_id") != ENGINE_ID:
        raise ValueError("Unexpected engine ID")

    if state.get("formal_variant") != FORMAL_VARIANT:
        raise ValueError("Unexpected formal variant")

    positions = state.get("positions")

    if not isinstance(positions, list):
        raise ValueError("positions must be a list")

    if len(positions) != 3:
        raise ValueError("Expected exactly three positions")

    symbols = {
        position.get("symbol")
        for position in positions
        if isinstance(position, dict)
    }

    if symbols != EXPECTED_SYMBOLS:
        raise ValueError(
            f"Unexpected position symbols: {symbols}"
        )

    for position in positions:
        if position.get("reconstruction_complete") is not True:
            raise ValueError(
                f"Incomplete position: {position.get('symbol')}"
            )

        if position.get("origin_branch") != "UPTREND":
            raise ValueError(
                f"Unexpected origin: {position.get('symbol')}"
            )

        if float(position["remaining_shares"]) <= 0:
            raise ValueError(
                f"Invalid remaining shares: "
                f"{position.get('symbol')}"
            )

        if float(
            position[
                "implied_remaining_cost_basis_from_final_leg"
            ]
        ) <= 0:
            raise ValueError(
                f"Invalid cost basis: "
                f"{position.get('symbol')}"
            )

    cash = float(state["cash"])
    positions_value = float(
        state[
            "positions_value_at_liquidation_execution_prices"
        ]
    )
    total_equity = float(
        state[
            "total_equity_at_liquidation_execution_prices"
        ]
    )

    if not approximately_equal(
        cash + positions_value,
        total_equity,
    ):
        raise ValueError(
            "Cash plus positions value does not equal equity"
        )

    if not approximately_equal(
        total_equity,
        EXPECTED_FINAL_EQUITY,
    ):
        raise ValueError(
            "Unexpected reconstructed total equity"
        )

    reconciliation = state.get("reconciliation", {})
    checks = reconciliation.get("checks", {})

    required_checks = {
        "three_sim_end_trades_found",
        "sim_end_symbols_match",
        "position_reconstruction_complete",
        "implied_cash_close_to_last_regular_cash",
        "cash_plus_liquidation_proceeds_equals_final_equity",
        "reconstructed_equity_equals_final_equity",
        "all_origins_are_uptrend",
    }

    missing_checks = sorted(
        required_checks - set(checks)
    )

    failed_checks = sorted(
        key
        for key in required_checks
        if checks.get(key) is not True
    )

    if missing_checks:
        raise ValueError(
            f"Missing reconciliation checks: {missing_checks}"
        )

    if failed_checks:
        raise ValueError(
            f"Failed reconciliation checks: {failed_checks}"
        )

    cash_delta = abs(
        float(
            reconciliation[
                "cash_delta_vs_last_regular_eod"
            ]
        )
    )

    if cash_delta > CASH_RECONSTRUCTION_TOLERANCE:
        raise ValueError(
            "Cash reconstruction exceeds frozen tolerance"
        )

    eligibility = state.get(
        "forward_seed_eligibility",
        {},
    )

    if eligibility.get(
        "eligible_for_account_economic_state"
    ) is not True:
        raise ValueError(
            "Account economic state was not accepted"
        )

    if eligibility.get(
        "eligible_for_full_runtime_continuation"
    ) is not False:
        raise ValueError(
            "Source must not claim original full runtime proof"
        )

    source_result_sha = (
        state.get("sources", {})
        .get("canonical_result_sha256")
    )

    if source_result_sha != CANONICAL_RESULT_SHA256:
        raise ValueError(
            "Canonical result SHA mismatch"
        )


def build_position_state(
    source_position: dict[str, Any],
) -> dict[str, Any]:
    return {
        "symbol": source_position["symbol"],
        "origin_branch": "UPTREND",
        "position_state_source": (
            "DERIVED_FROM_CANONICAL_SIM_END_TRADE"
        ),
        "remaining_shares": float(
            source_position["remaining_shares"]
        ),
        "average_cost": float(
            source_position[
                "implied_avg_cost_from_final_leg"
            ]
        ),
        "remaining_cost_basis": float(
            source_position[
                "implied_remaining_cost_basis_from_final_leg"
            ]
        ),
        "size_units": float(
            source_position["size_units_at_exit"]
        ),
        "entry_shares": float(
            source_position["entry_shares"]
        ),
        "effective_liquidation_price_for_reconciliation_only": (
            float(source_position["effective_exit_price"])
        ),
        "liquidation_proceeds_for_reconciliation_only": (
            float(source_position["liquidation_proceeds"])
        ),
        "source_trade_index": int(
            source_position["source_trade_index"]
        ),
        "source_json_path": (
            source_position["source_json_path"]
        ),
        "forward_policy": {
            "carry_position": True,
            "preserve_origin_branch": True,
            "do_not_replay_sim_end_exit": True,
            "do_not_reenter_as_new_buy": True,
            "apply_normal_uptrend_position_management": True,
        },
    }


def build_seed_state(
    source_state: dict[str, Any],
) -> dict[str, Any]:
    positions = sorted(
        (
            build_position_state(position)
            for position in source_state["positions"]
        ),
        key=lambda item: item["symbol"],
    )

    return {
        "schema_version": "1.0.0",
        "record_type": "FORWARD_RUNTIME_SEED_STATE",
        "engine_id": ENGINE_ID,
        "formal_variant": FORMAL_VARIANT,
        "seed_boundary": {
            "seed_date": SEED_DATE,
            "seed_semantics": (
                "PRE_SIM_END_CONTINUOUS_ACCOUNT_STATE"
            ),
            "first_forward_market_date": (
                FORWARD_START_DATE
            ),
            "sim_end_liquidation_replay_allowed": False,
        },
        "evidence_classification": {
            "is_original_runtime_snapshot": False,
            "account_economics": (
                "MATHEMATICALLY_RECONSTRUCTED_AND_RECONCILED"
            ),
            "runtime_policy": (
                "FORMALLY_FROZEN_GOVERNANCE_DECISION"
            ),
            "must_not_be_represented_as_original_trace": True,
        },
        "account": {
            "cash": float(source_state["cash"]),
            "position_count": 3,
            "positions": positions,
            "positions_value_reference": {
                "value": float(
                    source_state[
                        "positions_value_at_liquidation_execution_prices"
                    ]
                ),
                "valuation_basis": (
                    "SIM_END_EFFECTIVE_EXIT_PRICES_"
                    "FOR_RECONCILIATION_ONLY"
                ),
                "not_forward_opening_market_value": True,
            },
            "total_equity_reference": {
                "value": float(
                    source_state[
                        "total_equity_at_liquidation_execution_prices"
                    ]
                ),
                "valuation_basis": (
                    "PRE_SIM_END_RECONCILIATION_VALUE"
                ),
                "must_be_revalued_on_first_forward_date": True,
            },
        },
        "market_and_risk_state": {
            "spx_regime": source_state["regime"],
            "e1r_active_mode": (
                source_state["e1r_active_mode"]
            ),
            "risk_budget_mode": (
                source_state["risk_budget_mode"]
            ),
            "market_gate_state": (
                source_state["market_gate_state"]
            ),
            "max_positions": 3,
            "max_total_exposure_pct": 100.0,
            "field_source": (
                "LAST_REGULAR_EOD_AND_SIM_END_SETTLEMENT"
            ),
        },
        "pending_order_resolution": {
            "historical_pending_order_count": 1,
            "exact_payload_proven": False,
            "actionable_pending_orders": [],
            "resolution": (
                "EXPIRED_UNPROVEN_AT_FORWARD_BOUNDARY"
            ),
            "policy_source": (
                "USER_APPROVED_RUNTIME_SEED_CONTRACT"
            ),
            "prohibitions": [
                "Do not invent a symbol or action.",
                "Do not execute an unknown historical order.",
                "Do not count the unknown order as actionable.",
            ],
        },
        "runtime_reinitialization": {
            "policy": (
                "REINITIALIZE_UNPROVEN_TRANSIENT_FIELDS_"
                "FROM_FIRST_FORWARD_INPUT"
            ),
            "preserve": [
                "cash",
                "positions",
                "remaining shares",
                "remaining cost basis",
                "average cost",
                "size units",
                "origin branch",
                "known regime/gate/risk mode",
            ],
            "rederive_on_first_forward_date": [
                "ranking cache",
                "candidate cache",
                "market indicators",
                "leader scores",
                "transient decision buffers",
                "non-persistent counters without evidence",
                "daily valuation fields",
            ],
            "reset_to_empty": [
                "actionable pending orders",
                "SIM_END liquidation instructions",
                "temporary execution queue",
            ],
            "prohibited_resets": [
                "position holding identity",
                "position origin branch",
                "remaining shares",
                "remaining cost basis",
                "cash",
            ],
        },
        "first_forward_day_rules": {
            "market_date": FORWARD_START_DATE,
            "opening_actions": [
                "Load seed before processing market data.",
                "Revalue all three positions using forward data.",
                "Recompute transient market and ranking state.",
                "Apply ordinary strategy management.",
            ],
            "prohibited_actions": [
                "Replay SIM_END liquidation.",
                "Start from 281711.79 all-cash settlement.",
                "Execute the unknown historical pending order.",
                "Treat carried positions as new BUY entries.",
                "Backfill invented historical trace records.",
            ],
        },
        "forward_runtime_seed_eligible": True,
        "eligibility_basis": (
            "RECONSTRUCTED_ACCOUNT_ECONOMICS_PLUS_"
            "FROZEN_RUNTIME_BOUNDARY_POLICY"
        ),
    }


def build_contract() -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "contract_id": (
            "FD-M3180125-SP500-TOP3-engine/"
            "forward-runtime-seed/2026-06-18"
        ),
        "engine_id": ENGINE_ID,
        "contract_status": "FROZEN",
        "contract_scope": (
            "FORWARD_RUNTIME_SEED_BOUNDARY_ONLY"
        ),
        "historical_truth_boundary": {
            "original_pre_liquidation_snapshot_found": False,
            "derived_account_record_allowed": True,
            "derived_record_may_be_called_original_trace": False,
            "post_liquidation_cash_state_may_be_used": False,
        },
        "account_economic_contract": {
            "source": (
                "DERIVED_RECONSTRUCTED_PRE_SIM_END_ACCOUNT_STATE"
            ),
            "reconciliation_required": True,
            "closure_delta_required": 0.0,
            "cash_delta_tolerance_vs_last_regular_eod": 1.0,
            "required_position_symbols": [
                "DELL",
                "HUM",
                "MRVL",
            ],
            "required_origin_branch": "UPTREND",
        },
        "pending_order_contract": {
            "historical_count": 1,
            "payload_status": "UNPROVEN",
            "forward_actionability": False,
            "formal_resolution": (
                "EXPIRED_UNPROVEN_AT_FORWARD_BOUNDARY"
            ),
        },
        "runtime_state_contract": {
            "full_historical_runtime_state_proven": False,
            "forward_continuation_authorized_under_policy": True,
            "unproven_transient_fields": (
                "REINITIALIZE_OR_REDERIVE"
            ),
            "persistent_account_fields": "PRESERVE",
            "sim_end_execution_state": "DISCARD",
        },
        "forward_date_contract": {
            "seed_date": SEED_DATE,
            "first_forward_market_date": (
                FORWARD_START_DATE
            ),
            "forward_may_start_before_contract_freeze": False,
            "sim_end_may_be_replayed": False,
        },
        "change_control": {
            "strategy_logic_change_allowed": False,
            "account_economic_values_may_change": False,
            "pending_order_payload_may_be_invented": False,
            "contract_revision_requires_new_evidence_or_approval": True,
        },
    }


def build_provenance(
    source_state_path: Path,
    source_decision_path: Path,
    repository_head: str,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "engine_id": ENGINE_ID,
        "artifact_type": (
            "FORWARD_RUNTIME_SEED_CONTRACT_FREEZE"
        ),
        "repository_head_at_export": repository_head,
        "canonical_strategy_commit": (
            CANONICAL_STRATEGY_COMMIT
        ),
        "official_backtest_artifact_commit": (
            OFFICIAL_BACKTEST_COMMIT
        ),
        "canonical_result_sha256": (
            CANONICAL_RESULT_SHA256
        ),
        "sources": [
            {
                "role": (
                    "RECONSTRUCTED_ACCOUNT_STATE_SOURCE"
                ),
                "path": str(source_state_path),
                "sha256": sha256_file(source_state_path),
            },
            {
                "role": (
                    "TARGETED_RECONCILIATION_DECISION_SOURCE"
                ),
                "path": str(source_decision_path),
                "sha256": sha256_file(
                    source_decision_path
                ),
            },
        ],
        "transformations": [
            (
                "Preserve reconstructed cash, positions, "
                "shares, costs, origins and known market state."
            ),
            (
                "Expire unknown pending order as "
                "non-actionable at the Forward boundary."
            ),
            (
                "Reinitialize unproven transient runtime "
                "state from first Forward input."
            ),
            (
                "Prohibit replay of SIM_END liquidation."
            ),
        ],
        "backtest_rerun_performed": False,
        "forward_run_performed": False,
        "strategy_change_performed": False,
        "account_execution_change_performed": False,
    }


def build_manifest(
    output_dir: Path,
) -> dict[str, Any]:
    artifact_names = [
        "forward_runtime_seed_contract.json",
        "forward_runtime_seed_state.json",
        "forward_runtime_seed_provenance.json",
        "STEP2_FORWARD_RUNTIME_SEED_FREEZE_DECISION.json",
    ]

    artifacts = []

    for name in artifact_names:
        path = output_dir / name

        artifacts.append({
            "filename": name,
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        })

    return {
        "schema_version": "1.0.0",
        "engine_id": ENGINE_ID,
        "artifact_set": (
            "FORWARD_RUNTIME_SEED_2026_06_18"
        ),
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
    }


def freeze(
    source_state_path: Path,
    source_decision_path: Path,
    output_dir: Path,
    repository_head: str,
) -> dict[str, Any]:
    source_state = load_json(source_state_path)
    source_decision = load_json(source_decision_path)

    validate_sources(
        source_state,
        source_decision,
    )

    seed_state = build_seed_state(source_state)
    contract = build_contract()

    provenance = build_provenance(
        source_state_path=source_state_path,
        source_decision_path=source_decision_path,
        repository_head=repository_head,
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    write_json_atomic(
        output_dir / "forward_runtime_seed_contract.json",
        contract,
    )

    write_json_atomic(
        output_dir / "forward_runtime_seed_state.json",
        seed_state,
    )

    write_json_atomic(
        output_dir / "forward_runtime_seed_provenance.json",
        provenance,
    )

    decision = {
        "decision": FORMAL_DECISION,
        "engine_id": ENGINE_ID,
        "formal_variant": FORMAL_VARIANT,
        "seed_date": SEED_DATE,
        "first_forward_market_date": (
            FORWARD_START_DATE
        ),
        "forward_runtime_seed_eligible": True,
        "original_runtime_snapshot_found": False,
        "account_economics_reconstructed": True,
        "runtime_boundary_policy_frozen": True,
        "unknown_pending_order_actionable": False,
        "unknown_pending_order_resolution": (
            "EXPIRED_UNPROVEN_AT_FORWARD_BOUNDARY"
        ),
        "sim_end_liquidation_replay_allowed": False,
        "post_liquidation_cash_seed_allowed": False,
        "position_count": 3,
        "position_symbols": [
            "DELL",
            "HUM",
            "MRVL",
        ],
        "cash": seed_state["account"]["cash"],
        "reference_total_equity": (
            seed_state["account"]
            ["total_equity_reference"]["value"]
        ),
        "canonical_strategy_commit": (
            CANONICAL_STRATEGY_COMMIT
        ),
        "official_backtest_artifact_commit": (
            OFFICIAL_BACKTEST_COMMIT
        ),
        "canonical_result_sha256": (
            CANONICAL_RESULT_SHA256
        ),
        "repository_head_at_freeze": repository_head,
        "source_state_sha256": (
            sha256_file(source_state_path)
        ),
        "source_decision_sha256": (
            sha256_file(source_decision_path)
        ),
    }

    write_json_atomic(
        output_dir
        / "STEP2_FORWARD_RUNTIME_SEED_FREEZE_DECISION.json",
        decision,
    )

    manifest = build_manifest(output_dir)

    write_json_atomic(
        output_dir / "current_manifest.json",
        manifest,
    )

    return decision


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--source-state",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--source-decision",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--repository-head",
        required=True,
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    decision = freeze(
        source_state_path=args.source_state,
        source_decision_path=args.source_decision,
        output_dir=args.output_dir,
        repository_head=args.repository_head,
    )

    print(
        json.dumps(
            decision,
            indent=2,
            ensure_ascii=False,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
