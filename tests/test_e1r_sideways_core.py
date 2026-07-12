from __future__ import annotations

from copy import deepcopy

import pytest

from e1r_engine.sideways_core import (
    SidewaysConfig,
    SidewaysCore,
    drawdown_from_high_pct,
    slope_pct,
)


def _asset(symbol: str, closes: list[float]) -> dict:
    dates = [f"2025-01-{i + 1:02d}" for i in range(len(closes))]
    bars = [
        {"date": date, "close": close}
        for date, close in zip(dates, closes)
    ]
    return {
        "symbol": symbol,
        "bars": bars,
        "dates": dates,
        "date_to_idx": {
            date: index for index, date in enumerate(dates)
        },
        "by_date": {
            row["date"]: row for row in bars
        },
    }


def _inputs() -> tuple[dict, dict, str, str]:
    spx = _asset("SPX", [100.0 + i * 0.2 for i in range(202)])
    stocks = {
        "AAA": _asset("AAA", [100.0 + i * 0.5 for i in range(202)]),
        "BBB": _asset("BBB", [100.0 + i * 0.3 for i in range(202)]),
        "CCC": _asset("CCC", [100.0 + i * 0.1 for i in range(202)]),
        "VIXY": _asset("VIXY", [100.0 + i * 2.0 for i in range(202)]),
    }
    return stocks, spx, spx["dates"][-2], spx["dates"][-1]


def test_frozen_math_contract() -> None:
    assert slope_pct([100.0] + [100.0] * 18 + [110.0], 19) == pytest.approx(10.0)
    assert drawdown_from_high_pct([100.0, 120.0, 108.0]) == pytest.approx(-10.0)


def test_activation_and_allocation_contract() -> None:
    stocks, spx, date, next_date = _inputs()
    core = SidewaysCore(
        SidewaysConfig(
            top_n=10,
            gross_exposure=0.25,
            min_history_days=200,
        )
    )
    plan = core.decide_interval(
        stocks=stocks,
        spx=spx,
        date=date,
        next_date=next_date,
        regime="SIDEWAYS",
        subclass="MA_CONFLICT",
    )

    assert plan.is_active is True
    assert plan.candidate_count == 3
    assert plan.selected_count == 3
    assert [holding.symbol for holding in plan.holdings] == [
        "AAA", "BBB", "CCC"
    ]
    assert [holding.weight for holding in plan.holdings] == pytest.approx(
        [0.25 / 3.0] * 3
    )
    assert "VIXY" not in plan.trace.selected_symbols
    assert sum(
        holding.weight for holding in plan.holdings
    ) == pytest.approx(0.25)
    assert sum(
        holding.weighted_contribution for holding in plan.holdings
    ) == pytest.approx(plan.portfolio_return)


@pytest.mark.parametrize(
    ("regime", "subclass"),
    [
        ("UPTREND", "NO_SUBCLASS"),
        ("DOWNTREND", "NO_SUBCLASS"),
        ("SIDEWAYS", "DETERIORATION"),
        ("SIDEWAYS", "RECOVERY"),
    ],
)
def test_inactive_branches_have_zero_allocation(
    regime: str,
    subclass: str,
) -> None:
    stocks, spx, date, next_date = _inputs()
    plan = SidewaysCore().decide_interval(
        stocks=stocks,
        spx=spx,
        date=date,
        next_date=next_date,
        regime=regime,
        subclass=subclass,
    )
    assert plan.is_active is False
    assert plan.selected_count == 0
    assert plan.gross_exposure == 0.0
    assert plan.portfolio_return == 0.0


def test_top_n_truncation_and_stable_tie_order() -> None:
    stocks, spx, date, next_date = _inputs()
    # AAA and AAB have identical price paths and therefore identical scores.
    stocks = {
        "AAA": stocks["AAA"],
        "AAB": _asset(
            "AAB",
            [100.0 + i * 0.5 for i in range(202)],
        ),
        **stocks,
    }
    plan = SidewaysCore(
        SidewaysConfig(top_n=2, gross_exposure=0.25)
    ).decide_interval(
        stocks=stocks,
        spx=spx,
        date=date,
        next_date=next_date,
        regime="SIDEWAYS",
        subclass="MA_CONFLICT",
    )
    assert [holding.symbol for holding in plan.holdings] == ["AAA", "AAB"]


def test_no_input_mutation() -> None:
    stocks, spx, date, next_date = _inputs()
    stocks_before = deepcopy(stocks)
    spx_before = deepcopy(spx)
    SidewaysCore().decide_interval(
        stocks=stocks,
        spx=spx,
        date=date,
        next_date=next_date,
        regime="SIDEWAYS",
        subclass="MA_CONFLICT",
    )
    assert stocks == stocks_before
    assert spx == spx_before
