"""Unactivated Live production runtime and dry-run acceptance."""

from __future__ import annotations

from dataclasses import asdict
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Mapping, Optional, Sequence

from .live_account import LiveOpeningState, rebuild_live_account
from .live_daily import LiveDailyProcessor, LiveDailyResult
from .live_data import LiveMarketData
from .live_ledger import LiveLedger, TransactionEvent
from .live_persistence import LiveRuntimeRepository
from .live_reconciliation import reconcile_recommendations


class LiveProductionError(ValueError):
    pass


class LiveProductionRuntime:
    """Compose persisted Live facts with the existing Daily processor."""

    def __init__(
        self,
        *,
        repository: LiveRuntimeRepository,
        processor: LiveDailyProcessor,
        opening: LiveOpeningState,
    ) -> None:
        self.repository = repository
        self.processor = processor
        self.opening = opening

    def dry_run(
        self,
        *,
        market_date: date,
        market_data: LiveMarketData,
    ) -> LiveDailyResult:
        ledger = self.repository.load_ledger()
        result = self.processor.process(
            market_date=market_date,
            market_data=market_data,
            opening=self.opening,
            ledger=ledger,
        )
        return result

    def commit_unactivated_acceptance(
        self,
        *,
        result: LiveDailyResult,
        expected_execution_date: date,
    ) -> dict[str, object]:
        state_path = (
            self.repository.paths.current / "runtime_state.json"
        )
        if not state_path.exists():
            raise LiveProductionError(
                "Live runtime must be initialized first"
            )

        import json
        state = json.loads(state_path.read_text(encoding="utf-8"))
        if state.get("status") != "UNACTIVATED":
            raise LiveProductionError(
                "dry-run acceptance requires UNACTIVATED status"
            )

        ledger = self.repository.load_ledger()
        transactions = list(
            getattr(ledger, "transactions", ())
        )
        reconciliation = reconcile_recommendations(
            signal_date=result.market_date,
            expected_execution_date=expected_execution_date,
            as_of_date=result.market_date,
            recommendations=(
                result.decision.position_recommendations
            ),
            transactions=transactions,
        )

        payload = result.to_payload()
        account = payload["account"]

        artifacts = {
            "market_status": {
                "date": result.market_date.isoformat(),
                "regime": payload["regime"],
                "subclass": payload["regime_subclass"],
                "market_state": payload["market_state"],
                "market_gate": payload["market_gate"],
                "entry_capacity": payload["entry_capacity"],
                "strategy_branch": payload["strategy_branch"],
            },
            "reference_top3": {
                "date": result.market_date.isoformat(),
                "top3": payload["reference_top3"],
                "informational_only": True,
                "account_independent": True,
                "capacity_independent": True,
                "cash_independent": True,
                "not_an_execution_instruction": True,
            },
            "account_state": account,
            "active_positions": {
                "positions": account["positions"],
            },
            "engine_recommendations": {
                "signal_date": result.market_date.isoformat(),
                "expected_execution_date": (
                    expected_execution_date.isoformat()
                ),
                "recommendations": payload[
                    "position_recommendations"
                ],
            },
            "manual_transactions": {
                "transactions": [],
            },
            "reconciliation": {
                "records": [
                    asdict(item) for item in reconciliation
                ],
            },
            "equity": {
                "market_date": result.market_date.isoformat(),
                "actual_cash": account["actual_cash"],
                "positions_value": account["positions_value"],
                "total_equity": account["total_equity"],
                "trading_pnl": account["trading_pnl"],
                "cash_difference": account["cash_difference"],
                "result_hash": result.result_hash,
            },
        }

        hashes = self.repository.commit_daily(
            market_date=result.market_date.isoformat(),
            artifacts=artifacts,
        )

        self.repository.replace_current(
            "account_state.json",
            account,
        )
        self.repository.replace_current(
            "positions.json",
            artifacts["active_positions"],
        )
        self.repository.replace_current(
            "latest_recommendations.json",
            artifacts["engine_recommendations"],
        )
        self.repository.replace_current(
            "latest_reference_top3.json",
            artifacts["reference_top3"],
        )
        self.repository.replace_current(
            "latest_market_status.json",
            artifacts["market_status"],
        )

        run_payload = {
            "run_mode": "DRY_RUN_UNACTIVATED",
            "market_date": result.market_date.isoformat(),
            "result_hash": result.result_hash,
            "validation_status": "PASS",
            "opening_activated": False,
            "completed_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }
        self.repository.update_automation(
            "current_run.json",
            run_payload,
        )
        self.repository.update_automation(
            "last_successful_run.json",
            run_payload,
        )

        return {
            "decision": "PASS_LIVE_PRODUCTION_DRY_RUN",
            "market_date": result.market_date.isoformat(),
            "result_hash": result.result_hash,
            "artifact_hashes": hashes,
            "opening_activated": False,
        }

    def commit_active_daily(
        self,
        *,
        result: LiveDailyResult,
        expected_execution_date: date,
    ) -> dict[str, object]:
        import json
        from datetime import datetime, timezone

        state_path = self.repository.paths.current / "runtime_state.json"
        if not state_path.is_file():
            raise LiveProductionError("ACTIVE Live runtime state is missing")
        state = json.loads(state_path.read_text(encoding="utf-8"))
        if state.get("status") != "ACTIVE":
            raise LiveProductionError("active daily commit requires ACTIVE status")
        if state.get("opening_activated") is not True:
            raise LiveProductionError("active daily commit requires activated opening")
        if state.get("activation_required") is not False:
            raise LiveProductionError("active daily commit requires activation_required=false")

        opening_date = date.fromisoformat(str(state["opening_date"]))
        if result.market_date < opening_date:
            raise LiveProductionError("market_date precedes opening_date")

        last_raw = state.get("last_committed_market_date")
        if last_raw is not None:
            last_date = date.fromisoformat(str(last_raw))
            if result.market_date <= last_date:
                return {
                    "decision": "PASS_LIVE_ACTIVE_NO_NEW_DATE",
                    "market_date": result.market_date.isoformat(),
                    "last_committed_market_date": last_date.isoformat(),
                    "opening_activated": True,
                    "run_mode": "ACTIVE_RECOMMENDATION_ONLY",
                    "actual_trades_recorded": False,
                }

        ledger = self.repository.load_ledger()
        transactions = list(getattr(ledger, "transactions", ()))
        reconciliation = reconcile_recommendations(
            signal_date=result.market_date,
            expected_execution_date=expected_execution_date,
            recommendations=result.decision.position_recommendations,
            transactions=transactions,
        )
        payload = result.to_payload()
        account = payload["account"]
        artifacts = {
            "market_status": {
                "date": result.market_date.isoformat(),
                "regime": payload["regime"],
                "subclass": payload["regime_subclass"],
                "market_state": payload["market_state"],
                "market_gate": payload["market_gate"],
                "entry_capacity": payload["entry_capacity"],
                "strategy_branch": payload["strategy_branch"],
            },
            "reference_top3": {
                "date": result.market_date.isoformat(),
                "top3": payload["reference_top3"],
                "informational_only": True,
                "not_an_execution_instruction": True,
            },
            "account_state": account,
            "active_positions": {"positions": account["positions"]},
            "engine_recommendations": {
                "signal_date": result.market_date.isoformat(),
                "expected_execution_date": expected_execution_date.isoformat(),
                "recommendations": payload["position_recommendations"],
                "recommendation_only": True,
                "automatic_execution": False,
            },
            "manual_transactions": {
                "transactions": [],
                "actual_execution_source": "USER_RECORDED_ONLY",
            },
            "reconciliation": {"records": [asdict(x) for x in reconciliation]},
            "equity": {
                "market_date": result.market_date.isoformat(),
                "actual_cash": account["actual_cash"],
                "positions_value": account["positions_value"],
                "total_equity": account["total_equity"],
                "trading_pnl": account["trading_pnl"],
                "cash_difference": account["cash_difference"],
                "result_hash": result.result_hash,
            },
        }
        hashes = self.repository.commit_daily(
            market_date=result.market_date.isoformat(), artifacts=artifacts
        )
        now = datetime.now(timezone.utc).isoformat()
        self.repository.replace_current("account_state.json", account)
        self.repository.replace_current("positions.json", {"positions": account["positions"]})
        self.repository.replace_current("latest_market_status.json", artifacts["market_status"])
        self.repository.replace_current("latest_reference_top3.json", artifacts["reference_top3"])
        self.repository.replace_current("latest_recommendations.json", artifacts["engine_recommendations"])
        state.update({
            "status": "ACTIVE",
            "opening_activated": True,
            "activation_required": False,
            "last_committed_market_date": result.market_date.isoformat(),
            "last_successful_run_at": now,
        })
        self.repository.replace_current("runtime_state.json", state)
        run_payload = {
            "decision": "PASS_LIVE_ACTIVE_DAILY",
            "run_mode": "ACTIVE_RECOMMENDATION_ONLY",
            "market_date": result.market_date.isoformat(),
            "expected_execution_date": expected_execution_date.isoformat(),
            "opening_activated": True,
            "actual_trades_recorded": False,
            "automatic_execution_enabled": False,
            "artifact_hashes": hashes,
            "result_hash": result.result_hash,
            "completed_at": now,
        }
        self.repository.update_automation("current_run.json", run_payload)
        self.repository.update_automation("last_successful_run.json", run_payload)
        return run_payload
