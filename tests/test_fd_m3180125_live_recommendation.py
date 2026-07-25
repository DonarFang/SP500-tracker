from datetime import date

import pytest

from e1r_engine.live_recommendation import (
    LiveEngineDecision,
    LiveRecommendationError,
    ReferenceCandidate,
)


def test_reference_top3_is_rank_and_symbol_only() -> None:
    decision = LiveEngineDecision(
        market_date=date(2026, 7, 27),
        regime="UPTREND",
        regime_subclass=None,
        market_state="RISK_ON",
        market_gate="ALLOW",
        entry_capacity=0,
        strategy_branch="UPTREND",
        reference_candidates=(
            ReferenceCandidate(1, "AAPL"),
            ReferenceCandidate(2, "MSFT"),
            ReferenceCandidate(3, "NVDA"),
        ),
    )
    assert [item.symbol for item in decision.reference_candidates] == [
        "AAPL",
        "MSFT",
        "NVDA",
    ]
    assert decision.entry_capacity == 0


def test_reference_top3_rejects_more_than_three() -> None:
    with pytest.raises(LiveRecommendationError):
        LiveEngineDecision(
            market_date=date(2026, 7, 27),
            regime="UPTREND",
            regime_subclass=None,
            market_state="RISK_ON",
            market_gate="ALLOW",
            entry_capacity=3,
            strategy_branch="UPTREND",
            reference_candidates=tuple(
                ReferenceCandidate(i, f"S{i}")
                for i in range(1, 5)
            ),
        )
