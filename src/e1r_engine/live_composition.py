"""Formal unactivated Live production composition.

This module only composes existing Live components. It does not implement
market logic, Regime logic, Market State, Market Gate, Router, ranking,
strategy decisions, account rules, or persistence rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import json
from pathlib import Path
from typing import Sequence

from .adapters.live_data import LiveDataAdapter
from .live_account import LiveOpeningState
from .live_daily import LiveDailyProcessor
from .live_data import (
    LiveDataError,
    LiveMarketData,
    LivePriceRepository,
)
from .live_engine_adapter import LiveEngineAdapter
from .live_persistence import LiveRuntimeRepository
from .live_production import LiveProductionRuntime


class LiveCompositionError(ValueError):
    pass


REQUIRED_INDEX_SYMBOLS = frozenset(
    {"SPX", "NDX", "SOX", "VIX"}
)


@dataclass(frozen=True)
class LiveProductionComposition:
    repository: LiveRuntimeRepository
    runtime: LiveProductionRuntime
    market_data: LiveMarketData
    market_date: date
    stock_symbols: tuple[str, ...]
    catalogue_stock_symbols: tuple[str, ...]
    excluded_stock_symbols: tuple[str, ...]


def discover_live_stock_symbols(
    *,
    price_root: Path,
    expected_stock_count: int,
) -> tuple[str, ...]:
    root = Path(price_root)

    if root.name != "live_prices":
        raise LiveCompositionError(
            "Live price root must be named live_prices"
        )

    if expected_stock_count <= 0:
        raise LiveCompositionError(
            "expected_stock_count must be positive"
        )

    symbols = tuple(
        sorted(
            path.stem.strip().upper()
            for path in root.glob("*.json")
            if path.stem.strip().upper()
            not in REQUIRED_INDEX_SYMBOLS
        )
    )

    if len(symbols) != expected_stock_count:
        raise LiveCompositionError(
            "Live stock catalogue count mismatch: "
            f"expected={expected_stock_count}, "
            f"actual={len(symbols)}"
        )

    if len(set(symbols)) != len(symbols):
        raise LiveCompositionError(
            "Live stock catalogue contains duplicates"
        )

    return symbols


def discover_live_eligible_stock_symbols(
    *,
    price_root: Path,
    market_date: date,
    catalogue_stock_symbols: Sequence[str],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Separate catalogue membership from market-date eligibility."""
    repository = LivePriceRepository(Path(price_root))
    eligible: list[str] = []
    excluded: list[str] = []
    for raw_symbol in catalogue_stock_symbols:
        symbol = str(raw_symbol).strip().upper()
        try:
            repository.load_date(market_date, (symbol,))
        except LiveDataError as exc:
            expected = (
                f"{symbol} requires exactly one row for "
                f"{market_date.isoformat()}"
            )
            if str(exc) != expected:
                raise
            excluded.append(symbol)
        else:
            eligible.append(symbol)
    if not eligible:
        raise LiveCompositionError("Live eligible stock universe is empty")
    return tuple(eligible), tuple(excluded)


def validate_current_data_status(
    *,
    status_path: Path,
    market_date: date,
) -> dict[str, object]:
    path = Path(status_path)

    if not path.is_file():
        raise LiveCompositionError(
            "missing Live data update status: "
            + str(path)
        )

    payload = json.loads(
        path.read_text(encoding="utf-8")
    )

    if not isinstance(payload, dict):
        raise LiveCompositionError(
            "Live data update status must be an object"
        )

    if payload.get("data_status") != "CURRENT":
        raise LiveCompositionError(
            "Live data status must be CURRENT"
        )

    if payload.get("latest_market_date") != (
        market_date.isoformat()
    ):
        raise LiveCompositionError(
            "Live data latest_market_date mismatch"
        )

    if payload.get("catalogue_changed") is not False:
        raise LiveCompositionError(
            "Live data catalogue_changed must be false"
        )

    if payload.get("unavailable_symbols") not in ([], ()):
        raise LiveCompositionError(
            "Live data unavailable_symbols must be empty"
        )

    return payload


def compose_unactivated_live_production(
    *,
    price_root: Path,
    live_root: Path,
    data_status_path: Path,
    market_date: date,
    expected_execution_date: date,
    expected_stock_count: int = 498,
    min_bars: int = 120,
) -> LiveProductionComposition:
    """Compose the existing Live path without activating opening state."""

    if expected_execution_date <= market_date:
        raise LiveCompositionError(
            "expected_execution_date must be after market_date"
        )

    if min_bars <= 0:
        raise LiveCompositionError(
            "min_bars must be positive"
        )

    validate_current_data_status(
        status_path=data_status_path,
        market_date=market_date,
    )

    catalogue_stock_symbols = discover_live_stock_symbols(
        price_root=price_root,
        expected_stock_count=expected_stock_count,
    )

    stock_symbols, excluded_stock_symbols = (
        discover_live_eligible_stock_symbols(
            price_root=price_root,
            market_date=market_date,
            catalogue_stock_symbols=catalogue_stock_symbols,
        )
    )

    market_data = LivePriceRepository(
        Path(price_root)
    ).load_date(
        market_date,
        stock_symbols,
    )

    engine_adapter = LiveEngineAdapter(
        data_adapter=LiveDataAdapter(
            Path(price_root)
        ),
        stock_symbols=stock_symbols,
        min_bars=min_bars,
    )

    repository = LiveRuntimeRepository(
        Path(live_root)
    )
    repository.initialize_unactivated()

    runtime = LiveProductionRuntime(
        repository=repository,
        processor=LiveDailyProcessor(
            engine=engine_adapter
        ),
        opening=LiveOpeningState(),
    )

    return LiveProductionComposition(
        repository=repository,
        runtime=runtime,
        market_data=market_data,
        market_date=market_date,
        stock_symbols=stock_symbols,
        catalogue_stock_symbols=catalogue_stock_symbols,
        excluded_stock_symbols=excluded_stock_symbols,
    )


def run_unactivated_live_acceptance(
    *,
    price_root: Path,
    live_root: Path,
    data_status_path: Path,
    market_date: date,
    expected_execution_date: date,
    expected_stock_count: int = 498,
    min_bars: int = 120,
) -> dict[str, object]:
    composition = compose_unactivated_live_production(
        price_root=price_root,
        live_root=live_root,
        data_status_path=data_status_path,
        market_date=market_date,
        expected_execution_date=expected_execution_date,
        expected_stock_count=expected_stock_count,
        min_bars=min_bars,
    )

    result = composition.runtime.dry_run(
        market_date=market_date,
        market_data=composition.market_data,
    )

    acceptance = (
        composition.runtime.commit_unactivated_acceptance(
            result=result,
            expected_execution_date=expected_execution_date,
        )
    )

    if acceptance.get("opening_activated") is not False:
        raise LiveCompositionError(
            "unactivated acceptance changed opening state"
        )

    return {
        **acceptance,
        "stock_symbol_count": len(
            composition.stock_symbols
        ),
        "catalogue_stock_symbol_count": len(
            composition.catalogue_stock_symbols
        ),
        "eligible_stock_symbol_count": len(
            composition.stock_symbols
        ),
        "excluded_stock_symbols": list(
            composition.excluded_stock_symbols
        ),
        "price_root": str(Path(price_root)),
        "live_root": str(Path(live_root)),
        "data_status_path": str(
            Path(data_status_path)
        ),
        "production_composition": (
            "LiveDataAdapter"
            "->LiveEngineAdapter"
            "->LiveDailyProcessor"
            "->LiveProductionRuntime"
            "->LiveRuntimeRepository"
        ),
        "engine_modified": False,
        "workflow_created": False,
    }
