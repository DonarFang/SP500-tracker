from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

EXPORTER_PATH = (
    REPO_ROOT
    / "scripts"
    / "freeze_fd_m3180125_forward_runtime_seed.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "forward_seed_freezer",
        EXPORTER_PATH,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load freezer")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def build_position(
    symbol: str,
    shares: float,
    average_cost: float,
    trade_index: int,
) -> dict:
    cost_basis = shares * average_cost
    exit_price = average_cost + 10.0
    proceeds = shares * exit_price
    final_leg_pnl = proceeds - cost_basis

    return {
        "symbol": symbol,
        "origin_branch": "UPTREND",
        "entry_shares": shares * 2,
        "size_units_at_exit": 0.5,
        "remaining_shares": shares,
        "avg_cost_reported": average_cost,
        "effective_exit_price": exit_price,
        "liquidation_proceeds": proceeds,
        "implied_remaining_cost_basis_from_final_leg": (
            cost_basis
        ),
        "implied_avg_cost_from_final_leg": (
            average_cost
        ),
        "reconstruction_complete": True,
        "source_trade_index": trade_index,
        "source_json_path": (
            f"$.trades[{trade_index}]"
        ),
        "final_leg_realized_pnl": final_leg_pnl,
    }


def build_state(module) -> dict:
    positions = [
        build_position("MRVL", 100.0, 100.0, 89),
        build_position("DELL", 100.0, 200.0, 90),
        build_position("HUM", 100.0, 300.0, 91),
    ]

    cash = 221711.79
    positions_value = 60000.0

    return {
        "record_type": (
            "DERIVED_RECONSTRUCTED_PRE_SIM_END_ACCOUNT_STATE"
        ),
        "is_original_runtime_record": False,
        "must_not_be_represented_as_original_trace": True,
        "engine_id": module.ENGINE_ID,
        "formal_variant": module.FORMAL_VARIANT,
        "date": "2026-06-18",
        "cash": cash,
        "positions_value_at_liquidation_execution_prices": (
            positions_value
        ),
        "total_equity_at_liquidation_execution_prices": (
            281711.79
        ),
        "positions": positions,
        "regime": "UPTREND",
        "e1r_active_mode": (
            "UPTREND_EMERGING_CONFIRMED_ENABLED"
        ),
        "risk_budget_mode": "UPTREND_RISK_ON",
        "market_gate_state": "ALLOW",
        "reconciliation": {
            "cash_delta_vs_last_regular_eod": 0.25,
            "checks": {
                "three_sim_end_trades_found": True,
                "sim_end_symbols_match": True,
                "position_reconstruction_complete": True,
                "implied_cash_close_to_last_regular_cash": True,
                (
                    "cash_plus_liquidation_proceeds_"
                    "equals_final_equity"
                ): True,
                (
                    "reconstructed_equity_"
                    "equals_final_equity"
                ): True,
                "all_origins_are_uptrend": True,
            },
        },
        "forward_seed_eligibility": {
            "eligible_for_account_economic_state": True,
            "eligible_for_full_runtime_continuation": False,
        },
        "sources": {
            "canonical_result_sha256": (
                module.CANONICAL_RESULT_SHA256
            ),
        },
    }


class ForwardRuntimeSeedFreezeTests(unittest.TestCase):
    def test_contract_expires_unknown_pending_order(self):
        module = load_module()
        contract = module.build_contract()

        pending = contract["pending_order_contract"]

        self.assertEqual(
            pending["historical_count"],
            1,
        )
        self.assertFalse(
            pending["forward_actionability"]
        )
        self.assertEqual(
            pending["formal_resolution"],
            "EXPIRED_UNPROVEN_AT_FORWARD_BOUNDARY",
        )

    def test_seed_prohibits_sim_end_replay(self):
        module = load_module()
        seed = module.build_seed_state(
            build_state(module)
        )

        self.assertFalse(
            seed["seed_boundary"]
            ["sim_end_liquidation_replay_allowed"]
        )

        self.assertTrue(
            seed["forward_runtime_seed_eligible"]
        )

        self.assertEqual(
            seed["pending_order_resolution"]
            ["actionable_pending_orders"],
            [],
        )

    def test_freeze_writes_machine_readable_artifacts(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_state = root / "state.json"
            source_decision = root / "decision.json"
            output = root / "output"

            source_state.write_text(
                json.dumps(build_state(module)),
                encoding="utf-8",
            )

            source_decision.write_text(
                json.dumps({
                    "decision": (
                        module.EXPECTED_SOURCE_DECISION
                    )
                }),
                encoding="utf-8",
            )

            decision = module.freeze(
                source_state_path=source_state,
                source_decision_path=source_decision,
                output_dir=output,
                repository_head="test-head",
            )

            self.assertEqual(
                decision["decision"],
                module.FORMAL_DECISION,
            )

            seed = json.loads(
                (
                    output
                    / "forward_runtime_seed_state.json"
                ).read_text(encoding="utf-8")
            )

            manifest = json.loads(
                (
                    output
                    / "current_manifest.json"
                ).read_text(encoding="utf-8")
            )

            self.assertEqual(
                seed["account"]["position_count"],
                3,
            )

            self.assertEqual(
                manifest["artifact_count"],
                4,
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
