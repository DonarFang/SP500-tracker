from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ENGINE_ID = "FD-M3180125-SP500-TOP3-engine"

CONTRACT_ROOT = (
    ROOT
    / "exports"
    / "official"
    / ENGINE_ID
    / "forward"
    / "shared_runtime_contract"
)

CONTRACT_PATH = (
    CONTRACT_ROOT
    / "official_shared_runtime_contract.json"
)

DECISION_PATH = (
    CONTRACT_ROOT
    / "STEP2_OFFICIAL_SHARED_RUNTIME_CONTRACT_FREEZE_DECISION.json"
)

MANIFEST_PATH = CONTRACT_ROOT / "manifest.json"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_official_shared_runtime_contract() -> None:
    contract = json.loads(
        CONTRACT_PATH.read_text(encoding="utf-8")
    )
    decision = json.loads(
        DECISION_PATH.read_text(encoding="utf-8")
    )
    manifest = json.loads(
        MANIFEST_PATH.read_text(encoding="utf-8")
    )

    assert contract["engine_id"] == ENGINE_ID
    assert contract["contract_status"] == "FROZEN"

    prerequisites = contract["completed_prerequisites"]

    assert prerequisites["engine_development"] == "COMPLETE"
    assert prerequisites["canonical_backtest"] == "PASS"
    assert (
        prerequisites["uptrend_formal_replacement"]
        == "COMPLETE"
    )
    assert (
        prerequisites["sideways_formal_replacement"]
        == "COMPLETE"
    )
    assert (
        prerequisites["reopen_completed_strategy_work"]
        is False
    )

    time_contract = contract["forward_time_contract"]

    assert time_contract["seed_date"] == "2026-06-18"
    assert (
        time_contract["first_forward_market_date"]
        == "2026-06-19"
    )
    assert time_contract["forward_track_end"] == "OPEN_ENDED"
    assert (
        time_contract[
            "automatic_end_of_data_liquidation_allowed"
        ]
        is False
    )

    seed = contract["frozen_seed_boundary"]

    assert seed["required_position_count"] == 3
    assert sorted(seed["required_position_symbols"]) == [
        "DELL",
        "HUM",
        "MRVL",
    ]
    assert seed["actionable_pending_orders"] == []
    assert seed["sim_end_replay_allowed"] is False
    assert (
        seed["post_liquidation_all_cash_seed_allowed"]
        is False
    )

    modules = contract["module_contracts"]

    assert set(modules) == {
        "ForwardSeedLoader",
        "ForwardDatePlanner",
        "ForwardMarketDataAdapter",
        "CanonicalDailyDecisionRouter",
        "PendingOrderLedger",
        "T1ExecutionEngine",
        "ForwardAccountRepository",
        "ForwardDailyCommitter",
        "OfficialForwardArtifactWriter",
    }

    routing = modules[
        "CanonicalDailyDecisionRouter"
    ]["routing"]

    assert (
        routing["UPTREND"]["entry"]
        == "E1RCoreEngine.step"
    )
    assert (
        routing["UPTREND"]["legacy_decision_allowed"]
        is False
    )
    assert (
        routing["SIDEWAYS_MA_CONFLICT"]["ranking"]
        == "SidewaysCore.rank_date"
    )
    assert (
        routing["SIDEWAYS_MA_CONFLICT"]["decision"]
        == "SidewaysExecutionPolicy.build_intents"
    )

    execution = modules["T1ExecutionEngine"]

    assert execution["execution_order"] == [
        "EXIT",
        "REDUCE",
        "REL_REDUCE",
        "TP_REDUCE",
        "ADD",
        "BUY",
    ]
    assert "No SIM_END action" in execution["prohibitions"]
    assert (
        "No automatic data-end liquidation"
        in execution["prohibitions"]
    )

    account_repository = modules[
        "ForwardAccountRepository"
    ]

    assert (
        account_repository["write_contract"][
            "legacy_oos_state_mutation_allowed"
        ]
        is False
    )

    acceptance = contract["acceptance_contract"]

    assert (
        acceptance["contract_freeze_decision"]
        == "PASS_STEP2_OFFICIAL_SHARED_RUNTIME_CONTRACT_FROZEN"
    )
    assert (
        acceptance["forward_execution_allowed_by_this_step"]
        is False
    )
    assert (
        acceptance["canonical_5y_backtest_rerun_required"]
        is False
    )
    assert (
        acceptance["strategy_logic_change_allowed"]
        is False
    )

    assert (
        decision["decision"]
        == "PASS_STEP2_OFFICIAL_SHARED_RUNTIME_CONTRACT_FROZEN"
    )
    assert decision["strategy_logic_changed"] is False
    assert decision["forward_run_performed"] is False
    assert decision["canonical_5y_backtest_rerun"] is False
    assert decision["legacy_oos_state_mutated"] is False

    for filename, record in manifest["artifacts"].items():
        path = CONTRACT_ROOT / filename

        assert path.is_file()
        assert sha256_file(path) == record["sha256"]
