from __future__ import annotations

from e1r_engine.core import E1RCoreEngine

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping, Sequence

from e1r_engine.contracts import DailyBar
from e1r_engine.forward_orchestrator import (
    ForwardMarketSnapshotBuilder,
    ForwardRegimeProvider,
    ForwardStrategyInputBuilder,
    OfficialForwardCatchupRunner,
)
from e1r_engine.forward_runtime import (
    CanonicalDailyDecisionRouter,
    ForwardAccountRepository,
    ForwardDailyCommitter,
    ForwardDatePlanner,
    ForwardMarketDataAdapter,
    ForwardSeedLoader,
    OfficialForwardArtifactWriter,
    T1ExecutionEngine,
)


SeriesBySymbol = Mapping[
    str,
    Mapping[str, DailyBar],
]


@dataclass(frozen=True)
class ForwardProductionData:
    """
    Production Forward market-data boundary.

    Contains normalized price data and provenance only.
    It does not contain Regime labels, ranking decisions,
    Market Gate policy, management policy, orders, or fills.
    """

    universe: tuple[str, ...]
    required_symbols: tuple[str, ...]
    price_files_by_symbol: Mapping[str, Path]
    series_by_symbol: SeriesBySymbol
    trading_dates: tuple[str, ...]
    latest_complete_common_date: str
    source_hashes: Mapping[str, str]


@dataclass(frozen=True)
class ProductionForwardComposition:
    """
    Complete Step-2 runtime object graph.

    Construction is side-effect free:
    no Repository initialization, no commit_day, no Forward run,
    and no Official artifact writes.
    """

    data: ForwardProductionData
    market_data_adapter: ForwardMarketDataAdapter
    regime_provider: ForwardRegimeProvider
    snapshot_builder: ForwardMarketSnapshotBuilder
    strategy_input_builder: ForwardStrategyInputBuilder
    seed_loader: ForwardSeedLoader
    repository: ForwardAccountRepository
    date_planner: ForwardDatePlanner
    decision_router: CanonicalDailyDecisionRouter
    execution_engine: T1ExecutionEngine
    artifact_writer: OfficialForwardArtifactWriter
    committer: ForwardDailyCommitter
    runner: OfficialForwardCatchupRunner

# FD-M3180125 Forward required-runtime-symbols date boundary.
# Forward trading_dates must be based on required runtime symbols, not the all-symbol intersection.
# Required runtime symbols include canonical indices and carried seed positions.
# Tradable universe eligibility is filtered after runtime date boundary is known.
# 5Y historical index files must not be used as Forward runtime fallback.
_FORWARD_INDEX_SYMBOL_ALIASES = {
    "SPX": ("SPX", "^GSPC", "_GSPC", "GSPC"),
    "NDX": ("NDX", "^NDX", "_NDX"),
    "SOX": ("SOX", "^SOX", "_SOX"),
}


def _forward_symbol_lookup_keys(symbol):
    text = str(symbol).strip()
    upper = text.upper()
    no_provider_prefix = text.lstrip("^_")
    no_provider_prefix_upper = no_provider_prefix.upper()
    return tuple(dict.fromkeys((
        text, upper, no_provider_prefix, no_provider_prefix_upper,
        f"^{no_provider_prefix}", f"^{no_provider_prefix_upper}",
        f"_{no_provider_prefix}", f"_{no_provider_prefix_upper}",
    )))


def _canonicalize_forward_price_files_by_symbol(price_files_by_symbol):
    """Normalize Forward Yahoo index filenames into canonical Engine-facing symbols."""
    canonicalized = dict(price_files_by_symbol)
    lookup = {}
    for symbol, path in price_files_by_symbol.items():
        for key in _forward_symbol_lookup_keys(symbol):
            lookup.setdefault(key, path)
    for canonical, aliases in _FORWARD_INDEX_SYMBOL_ALIASES.items():
        if canonical in canonicalized:
            continue
        for alias in aliases:
            for key in _forward_symbol_lookup_keys(alias):
                if key in lookup:
                    canonicalized[canonical] = lookup[key]
                    break
            if canonical in canonicalized:
                break
    return canonicalized


def _forward_date_like(value):
    import re
    if value is None:
        return None
    text = str(value)
    if re.match(r'^\d{4}-\d{2}-\d{2}$', text):
        return text
    if re.match(r'^\d{4}-\d{2}-\d{2}[T ]', text):
        return text[:10]
    return None


def _forward_bar_dates(series):
    dates = set()
    if isinstance(series, dict):
        iterable = list(series.items())
        for key, value in iterable:
            key_date = _forward_date_like(key)
            if key_date is not None:
                dates.add(key_date)
            value_date = _forward_date_like(getattr(value, 'date', None))
            if value_date is not None:
                dates.add(value_date)
            if isinstance(value, dict):
                nested_date = _forward_date_like(value.get('date') or value.get('trading_date'))
                if nested_date is not None:
                    dates.add(nested_date)
        return dates
    for bar in series:
        direct_date = _forward_date_like(getattr(bar, 'date', None))
        if direct_date is not None:
            dates.add(direct_date)
        elif isinstance(bar, dict):
            dict_date = _forward_date_like(bar.get('date') or bar.get('trading_date'))
            if dict_date is not None:
                dates.add(dict_date)
        else:
            fallback_date = _forward_date_like(bar)
            if fallback_date is not None:
                dates.add(fallback_date)
    return dates


def _forward_sha256(path):
    import hashlib
    from pathlib import Path
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _normalize_forward_symbols(symbols):
    return tuple(dict.fromkeys(str(symbol).strip().upper() for symbol in symbols if str(symbol).strip()))


class ProductionForwardDataAdapter:
    """
    Connect production JSON price files to the existing formal
    ForwardMarketDataAdapter contract.

    This class performs normalization and provenance only.
    """

    REQUIRED_INDICES = (
        "SPX",
        "NDX",
        "SOX",
    )

    def __init__(
        self,
        *,
        market_data_adapter: ForwardMarketDataAdapter | None = None,
    ) -> None:
        self.market_data_adapter = (
            market_data_adapter
            or ForwardMarketDataAdapter(
                required_indices=self.REQUIRED_INDICES,
            )
        )

    def load(
        self,
        *,
        price_files_by_symbol,
        universe,
        required_runtime_symbols=None,
    ):
        # FD-M3180125 load uses required runtime symbols for trading_dates.
        from pathlib import Path

        price_files_by_symbol = _canonicalize_forward_price_files_by_symbol(
            price_files_by_symbol
        )
        universe = _normalize_forward_symbols(universe)

        required_indices = tuple(
            getattr(
                self.market_data_adapter,
                'required_indices',
                ('SPX', 'NDX', 'SOX'),
            )
        )
        required_runtime_symbols = _normalize_forward_symbols(
            tuple(required_indices) + tuple(required_runtime_symbols or ())
        )

        missing_required_files = [
            symbol
            for symbol in required_runtime_symbols
            if symbol not in price_files_by_symbol
        ]
        if missing_required_files:
            raise ValueError(
                'Missing production price files: '
                + ', '.join(missing_required_files)
            )

        missing_universe_files = [
            symbol
            for symbol in universe
            if symbol not in required_indices and symbol not in price_files_by_symbol
        ]
        if missing_universe_files:
            raise ValueError(
                'Missing production price files: '
                + ', '.join(missing_universe_files)
            )

        requested_symbols = _normalize_forward_symbols(
            tuple(required_runtime_symbols) + tuple(universe)
        )

        series_by_symbol = {}
        source_hashes = {}
        for symbol in requested_symbols:
            price_file = price_files_by_symbol.get(symbol)
            if price_file is None:
                continue
            path = Path(price_file)
            series = self.market_data_adapter.parse_price_file(path)
            if not series:
                continue
            series_by_symbol[symbol] = series
            source_hashes[symbol] = _forward_sha256(path)

        missing_required_series = [
            symbol
            for symbol in required_runtime_symbols
            if symbol not in series_by_symbol
        ]
        if missing_required_series:
            raise ValueError(
                'Missing production price series: '
                + ', '.join(missing_required_series)
            )

        required_date_sets = [
            _forward_bar_dates(series_by_symbol[symbol])
            for symbol in required_runtime_symbols
        ]
        required_date_counts = {
            symbol: len(_forward_bar_dates(series_by_symbol[symbol]))
            for symbol in required_runtime_symbols
        }
        if any(count == 0 for count in required_date_counts.values()):
            raise ValueError(
                'No parseable dates for required runtime symbols: '
                + ', '.join(
                    f'{symbol}={count}'
                    for symbol, count in required_date_counts.items()
                    if count == 0
                )
            )

        trading_dates = sorted(set.intersection(*required_date_sets))
        if not trading_dates:
            raise ValueError(
                'No common trading dates for required runtime symbols: '
                + ', '.join(required_runtime_symbols)
                + ' | date_counts='
                + str(required_date_counts)
            )

        trading_date_set = set(trading_dates)
        eligible_universe = []
        for symbol in universe:
            if symbol in required_indices:
                continue
            series = series_by_symbol.get(symbol)
            if not series:
                continue
            symbol_dates = _forward_bar_dates(series)
            if trading_date_set.issubset(symbol_dates):
                eligible_universe.append(symbol)

        required_symbols = _normalize_forward_symbols(
            tuple(required_runtime_symbols) + tuple(eligible_universe)
        )
        series_by_symbol = {
            symbol: series_by_symbol[symbol]
            for symbol in required_symbols
            if symbol in series_by_symbol
        }
        source_hashes = {
            symbol: source_hashes[symbol]
            for symbol in required_symbols
            if symbol in source_hashes
        }
        price_files_by_symbol = {
            symbol: price_files_by_symbol[symbol]
            for symbol in required_symbols
            if symbol in price_files_by_symbol
        }

        return ForwardProductionData(
            universe=tuple(eligible_universe),
            required_symbols=tuple(required_symbols),
            price_files_by_symbol=price_files_by_symbol,
            series_by_symbol=series_by_symbol,
            trading_dates=tuple(trading_dates),
            latest_complete_common_date=trading_dates[-1],
            source_hashes=source_hashes,
        )


def build_production_forward_composition(
    *,
    seed_root: Path | str,
    runtime_root: Path | str,
    price_files_by_symbol: Mapping[
        str,
        Path | str,
    ],
    universe: Sequence[str],
    strategy_input_builder: ForwardStrategyInputBuilder,
    runtime_commit_provider: Callable[[], str],
) -> ProductionForwardComposition:
    """
    Wire production Forward data into the existing Canonical
    Regime, Engine Router, strategy-input builder, Shared Runtime,
    T+1 execution, and catch-up runner.

    The already-completed ForwardStrategyInputBuilder is injected
    unchanged. No strategy rule is recreated here.
    """

    if not isinstance(
        strategy_input_builder,
        ForwardStrategyInputBuilder,
    ):
        raise TypeError(
            "strategy_input_builder must be an existing "
            "ForwardStrategyInputBuilder"
        )

    market_data_adapter = ForwardMarketDataAdapter(
        required_indices=(
            "SPX",
            "NDX",
            "SOX",
        )
    )

    data = ProductionForwardDataAdapter(
        market_data_adapter=market_data_adapter
    ).load(
        price_files_by_symbol=price_files_by_symbol,
        universe=universe,
    )

    regime_provider = (
        ForwardRegimeProvider.from_spx_series(
            spx_series=data.series_by_symbol["SPX"]
        )
    )

    snapshot_builder = (
        ForwardMarketSnapshotBuilder(
            regime_provider=regime_provider
        )
    )

    seed_loader = ForwardSeedLoader(seed_root)
    repository = ForwardAccountRepository(runtime_root)

    date_planner = ForwardDatePlanner(
        data.trading_dates
    )

    decision_router = (
        CanonicalDailyDecisionRouter(engine=E1RCoreEngine())
    )

    execution_engine = T1ExecutionEngine(
        one_way_cost=0.001,
        max_positions=3,
    )

    artifact_writer = (
        OfficialForwardArtifactWriter(runtime_root)
    )

    committer = ForwardDailyCommitter(
        repository=repository,
        artifact_writer=artifact_writer,
        decision_router=decision_router,
        execution_engine=execution_engine,
        runtime_commit_provider=(
            runtime_commit_provider
        ),
    )

    def source_hash_provider(
        trading_date: str,
    ) -> Mapping[str, str]:
        del trading_date
        return dict(data.source_hashes)

    runner = OfficialForwardCatchupRunner(
        seed_loader=seed_loader,
        repository=repository,
        date_planner=date_planner,
        market_data_adapter=market_data_adapter,
        snapshot_builder=snapshot_builder,
        strategy_input_builder=(
            strategy_input_builder
        ),
        committer=committer,
        universe=data.universe,
        series_by_symbol=data.series_by_symbol,
        required_execution_symbols=(
            data.required_symbols
        ),
        source_hash_provider=(
            source_hash_provider
        ),
    )

    return ProductionForwardComposition(
        data=data,
        market_data_adapter=market_data_adapter,
        regime_provider=regime_provider,
        snapshot_builder=snapshot_builder,
        strategy_input_builder=(
            strategy_input_builder
        ),
        seed_loader=seed_loader,
        repository=repository,
        date_planner=date_planner,
        decision_router=decision_router,
        execution_engine=execution_engine,
        artifact_writer=artifact_writer,
        committer=committer,
        runner=runner,
    )


__all__ = [
    "ForwardProductionData",
    "ProductionForwardComposition",
    "ProductionForwardDataAdapter",
    "build_production_forward_composition",
]
