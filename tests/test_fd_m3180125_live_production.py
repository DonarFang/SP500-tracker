from datetime import date
from pathlib import Path

from e1r_engine.live_account import LiveOpeningState
from e1r_engine.live_daily import LiveDailyProcessor
from e1r_engine.live_data import LiveBar, LiveMarketData
from e1r_engine.live_persistence import LiveRuntimeRepository
from e1r_engine.live_production import LiveProductionRuntime
from e1r_engine.live_recommendation import (
    LiveEngineDecision,
    ReferenceCandidate,
)


class FakeEngine:
    def decide(self, *, market_date, market_data, account):
        return LiveEngineDecision(
            market_date=market_date,
            regime="DOWNTREND",
            regime_subclass=None,
            market_state="CASH_MODE",
            market_gate="RISK_OFF",
            entry_capacity=0,
            strategy_branch="DOWNTREND",
            reference_candidates=(),
            position_recommendations=(),
            engine_version="test",
        )


def test_unactivated_production_dry_run_writes_live_only_artifacts(
    tmp_path: Path,
) -> None:
    repo = LiveRuntimeRepository(tmp_path / "live")
    repo.initialize_unactivated()

    runtime = LiveProductionRuntime(
        repository=repo,
        processor=LiveDailyProcessor(engine=FakeEngine()),
        opening=LiveOpeningState(),
    )
    day = date(2026, 7, 27)
    data = LiveMarketData(
        market_date=day,
        bars={
            "AAPL": LiveBar.from_mapping(
                "AAPL",
                {
                    "date": day.isoformat(),
                    "open": 100,
                    "high": 101,
                    "low": 99,
                    "close": 100,
                    "volume": 1000,
                },
            )
        },
    )

    result = runtime.dry_run(
        market_date=day,
        market_data=data,
    )
    accepted = runtime.commit_unactivated_acceptance(
        result=result,
        expected_execution_date=date(2026, 7, 28),
    )

    assert accepted["opening_activated"] is False
    assert accepted["decision"] == "PASS_LIVE_PRODUCTION_DRY_RUN"
    assert (
        repo.paths.daily
        / day.isoformat()
        / "manifest.json"
    ).is_file()
    assert (
        repo.paths.automation
        / "last_successful_run.json"
    ).is_file()
