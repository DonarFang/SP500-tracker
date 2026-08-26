#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ENGINE_ID = "FD-M3180125-SP500-TOP3-engine"
CONTRACT_VERSION = "1.0.0"

ROOT = Path(__file__).resolve().parents[1]

OUTPUT_ROOT = (
    ROOT
    / "exports"
    / "official"
    / ENGINE_ID
    / "forward"
    / "shared_runtime_contract"
)

CONTRACT_JSON = OUTPUT_ROOT / "official_shared_runtime_contract.json"
CONTRACT_MD = OUTPUT_ROOT / "OFFICIAL_SHARED_RUNTIME_CONTRACT.md"
DECISION_JSON = (
    OUTPUT_ROOT
    / "STEP2_OFFICIAL_SHARED_RUNTIME_CONTRACT_FREEZE_DECISION.json"
)
MANIFEST_JSON = OUTPUT_ROOT / "manifest.json"


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        while True:
            block = stream.read(1024 * 1024)

            if not block:
                break

            digest.update(block)

    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_bytes(canonical_json_bytes(value))


def build_contract() -> dict[str, Any]:
    return {
        "schema_version": CONTRACT_VERSION,
        "engine_id": ENGINE_ID,
        "contract_name": "OFFICIAL_SHARED_RUNTIME_CONTRACT",
        "contract_status": "FROZEN",
        "scope": {
            "included": [
                "Forward Seed loading",
                "open-ended trading-date planning",
                "daily market-data normalization",
                "canonical daily decision routing",
                "T+1 pending-order execution",
                "account-state persistence",
                "idempotent daily commit",
                "interruption recovery",
                "official Forward artifact generation",
            ],
            "excluded": [
                "UPTREND strategy changes",
                "SIDEWAYS strategy changes",
                "Engine strategy redevelopment",
                "Canonical 5Y backtest rerun",
                "strategy equivalence revalidation",
                "broker API integration",
                "Dashboard Step 3 integration",
            ],
        },
        "completed_prerequisites": {
            "engine_development": "COMPLETE",
            "canonical_backtest": "PASS",
            "uptrend_formal_replacement": "COMPLETE",
            "sideways_formal_replacement": "COMPLETE",
            "reopen_completed_strategy_work": False,
            "reopen_rule": (
                "Completed Engine and canonical backtest work may be "
                "reopened only when new, reproducible regression evidence exists."
            ),
        },
        "forward_time_contract": {
            "seed_date": "2026-06-16",
            "seed_semantics": "PRE_SIM_END_CONTINUOUS_ACCOUNT_STATE",
            "first_forward_market_date": "2026-06-17",
            "forward_track_end": "OPEN_ENDED",
            "initial_catchup_target": "LATEST_COMPLETE_COMMON_DATA_DATE",
            "subsequent_run_mode": "INCREMENTAL_FROM_LAST_COMMITTED_DATE",
            "processing_order": "STRICT_ASCENDING_TRADING_DATE",
            "fixed_terminal_date_allowed": False,
            "automatic_end_of_data_liquidation_allowed": False,
        },
        "frozen_seed_boundary": {
            "source_root": (
                "exports/official/"
                + ENGINE_ID
                + "/forward/seed_2026-06-16"
            ),
            "required_cash": 70154.33556161943,
            "required_position_symbols": [
                "DELL",
                "HUM",
                "MRVL",
            ],
            "required_position_count": 3,
            "position_origin": "UPTREND",
            "actionable_pending_orders": [],
            "unknown_historical_pending_resolution": (
                "EXPIRED_UNPROVEN_AT_FORWARD_BOUNDARY"
            ),
            "sim_end_replay_allowed": False,
            "post_liquidation_all_cash_seed_allowed": False,
        },
        "module_contracts": {
            "ForwardSeedLoader": {
                "responsibility": (
                    "Load and validate the frozen pre-SIM_END Forward Seed."
                ),
                "inputs": [
                    "forward_runtime_seed_contract.json",
                    "forward_runtime_seed_state.json",
                    "forward_runtime_seed_provenance.json",
                ],
                "outputs": [
                    "ForwardRuntimeState",
                ],
                "must_preserve": [
                    "cash",
                    "symbol",
                    "remaining_shares",
                    "average_cost",
                    "remaining_cost_basis",
                    "size_units",
                    "origin_branch",
                    "entry metadata",
                ],
                "must_reject": [
                    "SIM_END liquidation replay",
                    "post-liquidation all-cash state",
                    "invented pending-order payload",
                ],
            },
            "ForwardDatePlanner": {
                "responsibility": (
                    "Plan all uncommitted trading dates in ascending order."
                ),
                "inputs": [
                    "seed_date",
                    "last_committed_date",
                    "latest_complete_common_data_date",
                    "trading_calendar",
                ],
                "outputs": [
                    "ordered_uncommitted_trading_dates",
                ],
                "rules": [
                    (
                        "First planned date is 2026-06-17 when no Forward "
                        "daily commit exists."
                    ),
                    (
                        "Otherwise first planned date is the first trading "
                        "date after last_committed_date."
                    ),
                    (
                        "No date later than latest_complete_common_data_date "
                        "may be processed."
                    ),
                    (
                        "Empty plan produces NO_OP_DATA_NOT_ADVANCED."
                    ),
                ],
            },
            "ForwardMarketDataAdapter": {
                "responsibility": (
                    "Normalize complete daily inputs without strategy decisions."
                ),
                "inputs": [
                    "stock OHLC history",
                    "SPX history",
                    "NDX history",
                    "SOX history",
                    "daily regime records",
                ],
                "outputs": [
                    "MarketSnapshot",
                    "UPTREND strategy inputs when applicable",
                    "SIDEWAYS ranking inputs when applicable",
                    "latest_complete_common_data_date",
                ],
                "latest_complete_common_date_rule": {
                    "required_indices": [
                        "SPX",
                        "NDX",
                        "SOX",
                    ],
                    "required_symbols": [
                        "current holdings",
                        "pending-order symbols",
                        "symbols required by the active decision branch",
                    ],
                    "missing_required_bar_action": (
                        "STOP_BEFORE_DAILY_COMMIT"
                    ),
                },
                "prohibitions": [
                    "No BUY/ADD/REDUCE/EXIT decision",
                    "No account mutation",
                    "No look-ahead data",
                ],
            },
            "CanonicalDailyDecisionRouter": {
                "responsibility": (
                    "Route one completed trading day to already validated "
                    "canonical decision components."
                ),
                "inputs": [
                    "MarketSnapshot",
                    "AccountState after T+1 execution and T close mark-to-market",
                    "active regime",
                    "branch-specific frozen inputs",
                ],
                "outputs": [
                    "OrderIntent list",
                    "DecisionTrace",
                ],
                "routing": {
                    "UPTREND": {
                        "entry": "E1RCoreEngine.step",
                        "argument": "uptrend_inputs",
                        "legacy_decision_allowed": False,
                    },
                    "SIDEWAYS_MA_CONFLICT": {
                        "ranking": "SidewaysCore.rank_date",
                        "decision": (
                            "SidewaysExecutionPolicy.build_intents"
                        ),
                        "adapter": (
                            "SidewaysExecutionAdapter"
                        ),
                        "strategy_reimplementation_allowed": False,
                    },
                    "OTHER": {
                        "new_risk_expansion": False,
                        "default_output": "HOLD_OR_NOOP",
                        "existing_position_management": (
                            "Use only already frozen applicable management logic."
                        ),
                    },
                },
                "global_rules": [
                    "Maximum open positions across all origins is 3.",
                    (
                        "Regime transitions do not automatically liquidate "
                        "UPTREND-origin positions."
                    ),
                    (
                        "Decision routing must not recompute or alter frozen "
                        "UPTREND or SIDEWAYS strategy definitions."
                    ),
                ],
            },
            "PendingOrderLedger": {
                "responsibility": (
                    "Persist T-day OrderIntents for possible T+1 execution."
                ),
                "inputs": [
                    "OrderIntent list",
                    "signal_date",
                ],
                "outputs": [
                    "deterministic pending-order records",
                ],
                "identity_contract": {
                    "required_fields": [
                        "engine_id",
                        "signal_date",
                        "symbol",
                        "intent_type",
                        "branch",
                        "sequence",
                    ],
                    "identity": "DETERMINISTIC_SHA256",
                    "duplicate_identity_action": "NO_OP_ALREADY_RECORDED",
                },
                "rules": [
                    "HOLD and NOOP do not create executable pending orders.",
                    (
                        "Unknown historical pending orders are never imported "
                        "as actionable orders."
                    ),
                    (
                        "A pending order may transition to FILLED, SKIPPED, "
                        "CANCELLED, or EXPIRED exactly once."
                    ),
                ],
            },
            "T1ExecutionEngine": {
                "responsibility": (
                    "Execute prior-trading-day pending orders and mutate "
                    "AccountState using frozen execution semantics."
                ),
                "execution_order": [
                    "EXIT",
                    "REDUCE",
                    "REL_REDUCE",
                    "TP_REDUCE",
                    "ADD",
                    "BUY",
                ],
                "price_contract": {
                    "BUY": (
                        "T+1 high, fallback to T+1 close, plus one-way cost"
                    ),
                    "ADD": (
                        "T+1 high, fallback to T+1 close, plus one-way cost"
                    ),
                    "EXIT": (
                        "T+1 low, fallback to T+1 close, minus one-way cost"
                    ),
                    "REDUCE": (
                        "T+1 low, fallback to T+1 close, minus one-way cost"
                    ),
                },
                "account_rules": [
                    "EXIT and REDUCE release cash before BUY sizing.",
                    (
                        "Maximum open positions after execution is 3."
                    ),
                    (
                        "SIDEWAYS BUY uses the frozen tradable-cash base: "
                        "10% per symbol and 30% total."
                    ),
                    (
                        "Account cash, quantity, average cost, cost basis, "
                        "size units, realized PnL, and origin branch must remain "
                        "internally consistent."
                    ),
                ],
                "exactly_once_contract": {
                    "fill_identity": (
                        "SHA256(engine_id, order_id, execution_date, action)"
                    ),
                    "duplicate_fill_action": "NO_ACCOUNT_MUTATION",
                    "commit_required_before_next_date": True,
                },
                "prohibitions": [
                    "No SIM_END action",
                    "No automatic data-end liquidation",
                    "No broker-specific behavior",
                ],
            },
            "ForwardAccountRepository": {
                "responsibility": (
                    "Persist the latest committed Forward account and history."
                ),
                "state_fields": [
                    "schema_version",
                    "engine_id",
                    "last_committed_date",
                    "cash",
                    "positions",
                    "pending_orders",
                    "closed_trades",
                    "equity",
                    "decision provenance",
                    "source hashes",
                ],
                "position_fields": [
                    "symbol",
                    "quantity",
                    "average_cost",
                    "remaining_cost_basis",
                    "size_units",
                    "origin_branch",
                    "entry_date",
                    "last_price",
                    "market_value",
                    "realized_pnl",
                    "metadata",
                ],
                "write_contract": {
                    "method": "ATOMIC_TEMP_FILE_REPLACE",
                    "partial_daily_state_allowed": False,
                    "legacy_oos_state_mutation_allowed": False,
                },
            },
            "ForwardDailyCommitter": {
                "responsibility": (
                    "Commit one complete trading day atomically."
                ),
                "daily_sequence": [
                    "load last committed account",
                    "load pending orders from prior trading date",
                    "execute T+1 orders",
                    "mark all holdings to T close",
                    "build canonical daily decision inputs",
                    "generate current-day OrderIntents",
                    "persist new pending orders",
                    "write daily account state",
                    "write orders, fills, trace, and equity row",
                    "update current manifest",
                    "mark trading date committed",
                ],
                "commit_boundary": (
                    "A date is committed only after all required daily "
                    "artifacts and the account state are durable."
                ),
                "recovery": {
                    "uncommitted_partial_date": (
                        "Discard temporary artifacts and rerun the date."
                    ),
                    "committed_date": (
                        "NO_OP_ALREADY_COMMITTED"
                    ),
                    "next_restart_date": (
                        "first trading date after last_committed_date"
                    ),
                },
            },
            "OfficialForwardArtifactWriter": {
                "responsibility": (
                    "Write canonical Forward artifacts for review and Dashboard."
                ),
                "official_root": (
                    "exports/official/"
                    + ENGINE_ID
                    + "/forward/runtime"
                ),
                "required_artifacts": [
                    "current/account_state.json",
                    "current/pending_orders.json",
                    "current/manifest.json",
                    "daily/YYYY-MM-DD/account_state.json",
                    "daily/YYYY-MM-DD/order_intents.json",
                    "daily/YYYY-MM-DD/fills.json",
                    "daily/YYYY-MM-DD/decision_trace.json",
                    "daily/YYYY-MM-DD/equity.json",
                    "history/equity_curve.json",
                    "history/orders.jsonl",
                    "history/fills.jsonl",
                ],
                "manifest_requirements": [
                    "engine_id",
                    "schema_version",
                    "seed_date",
                    "first_forward_market_date",
                    "last_committed_date",
                    "latest_complete_common_data_date",
                    "forward_track_end",
                    "account summary",
                    "artifact SHA256 values",
                    "source-data SHA256 values",
                    "runtime commit",
                ],
            },
        },
        "daily_processing_contract": {
            "order": [
                "PLAN_DATE",
                "LOAD_COMMITTED_STATE",
                "LOAD_T1_MARKET_DATA",
                "EXECUTE_PRIOR_PENDING",
                "MARK_TO_MARKET_AT_CLOSE",
                "BUILD_DAILY_DECISION_INPUTS",
                "ROUTE_CANONICAL_DECISION",
                "CREATE_CURRENT_PENDING",
                "VALIDATE_ACCOUNT_AND_MAX3",
                "WRITE_DAILY_ARTIFACTS",
                "ATOMIC_COMMIT",
                "UPDATE_CURRENT_MANIFEST",
            ],
            "date_atomicity": True,
            "strict_previous_date_dependency": True,
            "parallel_date_processing_allowed": False,
        },
        "idempotency_contract": {
            "date_identity": (
                "SHA256(engine_id, forward_track, trading_date)"
            ),
            "order_identity": (
                "SHA256(engine_id, signal_date, symbol, intent_type, branch, sequence)"
            ),
            "fill_identity": (
                "SHA256(engine_id, order_id, execution_date, action)"
            ),
            "same_date_second_run": "NO_OP_ALREADY_COMMITTED",
            "duplicate_order": "NO_OP_ALREADY_RECORDED",
            "duplicate_fill": "NO_ACCOUNT_MUTATION",
            "commit_manifest_is_source_of_truth": True,
        },
        "validation_contract": {
            "before_daily_commit": [
                "Market date equals planned trading date.",
                "All required market bars are complete.",
                "AccountState validates.",
                "Cash is non-negative within accepted tolerance.",
                "Open positions are at most 3.",
                "All positions have explicit origin_branch.",
                "Every executable pending order has a deterministic order ID.",
                "Every fill references one pending order.",
                "No SIM_END event exists.",
            ],
            "after_daily_commit": [
                "All required daily artifacts exist.",
                "All artifact hashes match the manifest.",
                "last_committed_date equals the processed date.",
                "Current account equals the committed daily account.",
                "The next restart date is deterministic.",
            ],
        },
        "failure_contract": {
            "missing_required_data": "STOP_WITHOUT_DAILY_COMMIT",
            "invalid_seed": "STOP_BEFORE_FIRST_FORWARD_DATE",
            "account_validation_failure": "STOP_WITHOUT_DAILY_COMMIT",
            "duplicate_fill_conflict": "STOP_WITHOUT_ACCOUNT_MUTATION",
            "manifest_hash_failure": "STOP_AND_RETAIN_LAST_GOOD_COMMIT",
            "strategy_input_contract_failure": "STOP_WITHOUT_FALLBACK_TO_LEGACY",
        },
        "acceptance_contract": {
            "contract_freeze_decision": (
                "PASS_STEP2_OFFICIAL_SHARED_RUNTIME_CONTRACT_FROZEN"
            ),
            "implementation_allowed_after_freeze": True,
            "forward_execution_allowed_by_this_step": False,
            "canonical_5y_backtest_rerun_required": False,
            "strategy_logic_change_allowed": False,
            "dashboard_integration_allowed_by_this_step": False,
        },
    }


def build_markdown(contract: dict[str, Any]) -> str:
    modules = contract["module_contracts"]

    lines = [
        "# FD-M3180125-SP500-TOP3-engine",
        "",
        "## Official Shared Runtime Contract",
        "",
        f"- Contract version: `{CONTRACT_VERSION}`",
        "- Status: `FROZEN`",
        "- Forward track: `OPEN_ENDED`",
        "- Seed date: `2026-06-16`",
        "- First Forward market date: `2026-06-17`",
        "",
        "## Frozen premise",
        "",
        "- Engine development is complete.",
        "- Canonical 5Y Backtest has passed.",
        "- UPTREND formal replacement is complete.",
        "- SIDEWAYS formal replacement is complete.",
        (
            "- Completed strategy development and backtest validation must "
            "not be reopened without reproducible regression evidence."
        ),
        "",
        "## Daily runtime order",
        "",
    ]

    for index, step in enumerate(
        contract["daily_processing_contract"]["order"],
        start=1,
    ):
        lines.append(f"{index}. `{step}`")

    lines.extend([
        "",
        "## Canonical decision routing",
        "",
        (
            "- `UPTREND` → `E1RCoreEngine.step` using frozen "
            "`uptrend_inputs`."
        ),
        (
            "- `SIDEWAYS / MA_CONFLICT` → `SidewaysCore.rank_date` "
            "→ `SidewaysExecutionPolicy.build_intents`."
        ),
        "- Other regimes → no new risk expansion; HOLD/NOOP as applicable.",
        "",
        "## T+1 execution",
        "",
        (
            "- Execute prior-day orders before current-day mark-to-market "
            "and decision generation."
        ),
        "- Execution priority: EXIT, REDUCE, REL_REDUCE, TP_REDUCE, ADD, BUY.",
        "- BUY/ADD: T+1 high, fallback close, plus one-way cost.",
        "- EXIT/REDUCE: T+1 low, fallback close, minus one-way cost.",
        "- Global open-position limit: 3.",
        "",
        "## Persistence and recovery",
        "",
        "- One trading date is one atomic commit boundary.",
        "- A committed date is never processed twice.",
        "- Partial temporary artifacts are discarded and the date is rerun.",
        "- Restart begins after `last_committed_date`.",
        "- Legacy OOS state is not mutated.",
        "",
        "## SIM_END separation",
        "",
        "- Forward has no fixed terminal date.",
        "- Data end never triggers liquidation.",
        "- Backtest SIM_END is prohibited in Forward.",
        "- The post-liquidation all-cash state is not a valid Forward Seed.",
        "",
        "## Official modules",
        "",
    ])

    for name, module in modules.items():
        lines.append(f"### `{name}`")
        lines.append("")
        lines.append(module["responsibility"])
        lines.append("")

    lines.extend([
        "## Freeze decision",
        "",
        "```text",
        "PASS_STEP2_OFFICIAL_SHARED_RUNTIME_CONTRACT_FROZEN",
        "```",
        "",
        "This freeze does not run Forward and does not change strategy logic.",
        "",
    ])

    return "\n".join(lines)


def build_decision(
    contract: dict[str, Any],
    contract_sha256: str,
    markdown_sha256: str,
) -> dict[str, Any]:
    return {
        "engine_id": ENGINE_ID,
        "step": "STEP2_OFFICIAL_SHARED_RUNTIME_CONTRACT_FREEZE",
        "decision": (
            "PASS_STEP2_OFFICIAL_SHARED_RUNTIME_CONTRACT_FROZEN"
        ),
        "contract_version": CONTRACT_VERSION,
        "contract_status": "FROZEN",
        "contract_sha256": contract_sha256,
        "markdown_sha256": markdown_sha256,
        "forward_time_contract": (
            contract["forward_time_contract"]
        ),
        "completed_prerequisites": (
            contract["completed_prerequisites"]
        ),
        "module_names": list(
            contract["module_contracts"].keys()
        ),
        "strategy_logic_changed": False,
        "forward_run_performed": False,
        "canonical_5y_backtest_rerun": False,
        "legacy_oos_state_mutated": False,
        "dashboard_step3_started": False,
        "next_action": (
            "Implement the frozen Shared Runtime contract without "
            "changing UPTREND or SIDEWAYS strategy logic."
        ),
    }


def main() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    contract = build_contract()
    write_json(CONTRACT_JSON, contract)

    markdown = build_markdown(contract)
    CONTRACT_MD.write_text(
        markdown,
        encoding="utf-8",
    )

    contract_sha256 = sha256_file(CONTRACT_JSON)
    markdown_sha256 = sha256_file(CONTRACT_MD)

    decision = build_decision(
        contract=contract,
        contract_sha256=contract_sha256,
        markdown_sha256=markdown_sha256,
    )
    write_json(DECISION_JSON, decision)

    manifest = {
        "schema_version": CONTRACT_VERSION,
        "engine_id": ENGINE_ID,
        "artifact_type": (
            "OFFICIAL_SHARED_RUNTIME_CONTRACT_FREEZE"
        ),
        "decision": decision["decision"],
        "artifacts": {
            CONTRACT_JSON.name: {
                "sha256": contract_sha256,
            },
            CONTRACT_MD.name: {
                "sha256": markdown_sha256,
            },
            DECISION_JSON.name: {
                "sha256": sha256_file(DECISION_JSON),
            },
        },
    }
    write_json(MANIFEST_JSON, manifest)

    print(
        json.dumps(
            {
                "decision": decision["decision"],
                "output_root": str(
                    OUTPUT_ROOT.relative_to(ROOT)
                ),
                "contract_sha256": contract_sha256,
                "markdown_sha256": markdown_sha256,
                "decision_sha256": sha256_file(
                    DECISION_JSON
                ),
                "manifest_sha256": sha256_file(
                    MANIFEST_JSON
                ),
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
