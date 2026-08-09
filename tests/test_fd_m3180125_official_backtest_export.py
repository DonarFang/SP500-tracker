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
    / "export_fd_m3180125_official_backtest.py"
)


def load_exporter():
    spec = importlib.util.spec_from_file_location(
        "fd_m3180125_official_exporter",
        EXPORTER_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load official exporter")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_fixture(module) -> dict:
    daily = []

    for index in range(module.EXPECTED_REGULAR_ROW_COUNT):
        date = f"2021-06-11#{index:04d}"
        equity = module.EXPECTED_INITIAL_EQUITY + index

        daily.append({
            "date": date,
            "cash": equity,
            "positions_value": 0.0,
            "total_equity": equity,
            "daily_return_pct": 0.0,
            "drawdown_pct": 0.0,
            "exposure_pct": 0.0,
            "open_positions_count": 0,
            "pending_orders_count": 0,
            "market_gate_state": "ALLOW",
            "spx_regime": "UPTREND",
            "spx_close": 4000.0 + index,
            "spx_day_return_pct": 0.0,
            "event": "EOD_MARK_TO_MARKET",
        })

    daily[0]["date"] = module.EXPECTED_FIRST_DATE
    daily[0]["total_equity"] = module.EXPECTED_INITIAL_EQUITY
    daily[0]["cash"] = module.EXPECTED_INITIAL_EQUITY

    daily[-1]["date"] = module.EXPECTED_LAST_REGULAR_DATE
    daily[-1]["total_equity"] = (
        module.EXPECTED_LAST_REGULAR_EQUITY
    )
    daily[-1]["cash"] = module.EXPECTED_LAST_REGULAR_EQUITY

    trades = []

    for index in range(module.EXPECTED_TRADE_COUNT):
        trades.append({
            "symbol": f"T{index:03d}",
            "is_sim_end": False,
            "exit_signal": "EXIT",
            "exit_type": "NORMAL_EXIT",
        })

    for index, symbol in zip(
        (89, 90, 91),
        ("MRVL", "DELL", "HUM"),
    ):
        trades[index] = {
            "symbol": symbol,
            "is_sim_end": True,
            "exit_signal": "SIM_END",
            "exit_type": "SIM_END",
        }

    return {
        "engine_id": module.ENGINE_ID,
        "strategy_variant": module.VARIANT_ID,
        "strategy_display_name": module.DISPLAY_NAME,
        "daily_equity_records": daily,
        "trades": trades,
        "final_equity": module.EXPECTED_FINAL_EQUITY,
        "total_return_pct": 212.69,
        "cagr_pct": 25.59,
        "max_drawdown_pct": 25.66,
        "sharpe_ratio": 0.76,
        "profit_factor": 2.36,
        "number_of_trades": 92,
        "exposure_pct": 69.2,
        "capped_atr_stop_trace": [
            {"symbol": f"S{index}"} for index in range(8)
        ],
        "executed_exit_reason_distribution": {"HARD_LOSS_STOP": 3},
        "sim_end_liquidation_record": {
            "date": module.EXPECTED_SETTLEMENT_DATE,
            "event": "SIM_END_LIQUIDATION",
            "cash": module.EXPECTED_FINAL_EQUITY,
            "positions_value": 0.0,
            "total_equity": module.EXPECTED_FINAL_EQUITY,
        },
    }


class OfficialBacktestExporterTests(unittest.TestCase):
    def test_actual_sim_end_filter_does_not_match_false_key(self):
        trades = [
            {
                "symbol": "A",
                "is_sim_end": False,
                "exit_signal": "EXIT",
                "exit_type": "NORMAL_EXIT",
            },
            {
                "symbol": "B",
                "is_sim_end": True,
                "exit_signal": "SIM_END",
                "exit_type": "SIM_END",
            },
        ]

        actual = [
            trade
            for trade in trades
            if (
                trade.get("is_sim_end") is True
                or trade.get("exit_signal") == "SIM_END"
                or trade.get("exit_type") == "SIM_END"
            )
        ]

        self.assertEqual(
            [trade["symbol"] for trade in actual],
            ["B"],
        )

    def test_official_curve_appends_typed_settlement_point(self):
        module = load_exporter()

        daily = [{
            "date": module.EXPECTED_FIRST_DATE,
            "cash": 100000.0,
            "positions_value": 0.0,
            "total_equity": 100000.0,
            "daily_return_pct": 0.0,
            "drawdown_pct": 0.0,
            "exposure_pct": 0.0,
            "open_positions_count": 0,
            "pending_orders_count": 0,
            "market_gate_state": "ALLOW",
            "spx_regime": "UPTREND",
            "spx_close": 4000.0,
            "spx_day_return_pct": 0.0,
            "event": "EOD_MARK_TO_MARKET",
        }]

        settlement = {
            "date": module.EXPECTED_SETTLEMENT_DATE,
            "event": "SIM_END_LIQUIDATION",
            "cash": module.EXPECTED_FINAL_EQUITY,
            "positions_value": 0.0,
            "total_equity": module.EXPECTED_FINAL_EQUITY,
        }

        regular = module.build_regular_curve(daily)
        official = module.build_official_curve(
            regular,
            settlement,
        )

        self.assertEqual(len(official), 2)
        self.assertEqual(
            official[0]["point_type"],
            "REGULAR_EOD",
        )
        self.assertEqual(
            official[-1]["point_type"],
            "FINAL_SETTLEMENT",
        )
        self.assertEqual(
            official[-1]["event"],
            "SIM_END_LIQUIDATION",
        )
        self.assertIsNone(official[-1]["spx_close"])
        self.assertAlmostEqual(
            official[-1]["engine_equity"],
            module.EXPECTED_FINAL_EQUITY,
            places=2,
        )

    def test_contract_prohibits_liquidated_forward_seed(self):
        module = load_exporter()

        with tempfile.TemporaryDirectory() as directory:
            temp_root = Path(directory)
            source = temp_root / "source.json"
            output = temp_root / "official"

            source.write_text(
                json.dumps(build_fixture(module)),
                encoding="utf-8",
            )

            decision = module.export(
                source_path=source,
                output_dir=output,
                operational_head="test-head",
            )

            contract = json.loads(
                (output / "artifact_contract.json").read_text(
                    encoding="utf-8"
                )
            )
            settlement = json.loads(
                (output / "final_settlement.json").read_text(
                    encoding="utf-8"
                )
            )
            manifest = json.loads(
                (output / "current_manifest.json").read_text(
                    encoding="utf-8"
                )
            )

            self.assertEqual(
                decision["decision"],
                "PASS_AE_STEP_1_CAPPED_ATR_OFFICIAL_BACKTEST_ARTIFACT_EXPORT",
            )
            self.assertFalse(
                contract["forward_boundary"]
                ["backtest_final_settlement_is_forward_seed"]
            )
            self.assertFalse(
                settlement["forward_seed_eligible"]
            )

            manifest_names = {
                item["filename"]
                for item in manifest["artifacts"]
            }

            self.assertIn(
                "STEP1_OFFICIAL_EXPORT_DECISION.json",
                manifest_names,
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
