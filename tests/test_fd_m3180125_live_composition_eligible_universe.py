"""Regression for Live catalogue versus date-eligible universe."""

from datetime import date
from pathlib import Path

from e1r_engine.live_composition import (
    discover_live_eligible_stock_symbols,
    discover_live_stock_symbols,
)


def test_live_catalogue_and_date_eligible_universe_are_separate() -> None:
    root = Path("data/live_prices")
    market_date = date.fromisoformat("2026-07-24")
    catalogue = discover_live_stock_symbols(
        price_root=root, expected_stock_count=494
    )
    eligible, excluded = discover_live_eligible_stock_symbols(
        price_root=root,
        market_date=market_date,
        catalogue_stock_symbols=catalogue,
    )
    assert len(catalogue) == 494
    assert set(eligible).isdisjoint(excluded)
    assert set(eligible) | set(excluded) == set(catalogue)
    assert "CTRA" in excluded
