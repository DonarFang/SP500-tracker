from __future__ import annotations

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
        price_files_by_symbol: Mapping[str, Path | str],
        universe: Sequence[str],
    ) -> ForwardProductionData:
        normalized_universe = tuple(
            dict.fromkeys(
                str(symbol).strip().upper()
                for symbol in universe
                if str(symbol).strip()
            )
        )

        if not normalized_universe:
            raise ValueError(
                "Forward production universe is empty"
            )

        if len(normalized_universe) != len(tuple(universe)):
            raise ValueError(
                "Forward production universe contains "
                "duplicates or empty symbols"
            )

        normalized_files = {
            str(symbol).strip().upper(): Path(file_path)
            for symbol, file_path
            in price_files_by_symbol.items()
        }

        required_symbols = tuple(
            dict.fromkeys(
                (
                    *self.REQUIRED_INDICES,
                    *normalized_universe,
                )
            )
        )

        missing = [
            symbol
            for symbol in required_symbols
            if symbol not in normalized_files
        ]

        if missing:
            raise ValueError(
                "Missing production price files: "
                + ", ".join(missing)
            )

        nonexistent = [
            symbol
            for symbol in required_symbols
            if not normalized_files[symbol].is_file()
        ]

        if nonexistent:
            raise ValueError(
                "Production price files do not exist: "
                + ", ".join(nonexistent)
            )

        series_by_symbol = {
            symbol: (
                self.market_data_adapter
                .parse_price_file(
                    normalized_files[symbol]
                )
            )
            for symbol in required_symbols
        }

        empty = [
            symbol
            for symbol in required_symbols
            if not series_by_symbol[symbol]
        ]

        if empty:
            raise ValueError(
                "Production price series are empty: "
                + ", ".join(empty)
            )

        latest_complete_common_date = (
            self.market_data_adapter
            .latest_complete_common_date(
                series_by_symbol=series_by_symbol,
                required_symbols=normalized_universe,
            )
        )

        common_dates: set[str] | None = None

        for symbol in required_symbols:
            valid_dates = {
                trading_date
                for trading_date, bar
                in series_by_symbol[symbol].items()
                if (
                    bar is not None
                    and bar.close is not None
                    and float(bar.close) > 0
                )
            }

            common_dates = (
                valid_dates
                if common_dates is None
                else common_dates & valid_dates
            )

        trading_dates = tuple(
            sorted(
                trading_date
                for trading_date
                in (common_dates or set())
                if trading_date
                <= latest_complete_common_date
            )
        )

        if not trading_dates:
            raise ValueError(
                "No complete common Forward trading dates"
            )

        if (
            trading_dates[-1]
            != latest_complete_common_date
        ):
            raise ValueError(
                "Latest complete common date is absent "
                "from the common trading calendar"
            )

        source_hashes = {
            symbol: hashlib.sha256(
                normalized_files[symbol].read_bytes()
            ).hexdigest()
            for symbol in required_symbols
        }

        return ForwardProductionData(
            universe=normalized_universe,
            required_symbols=required_symbols,
            price_files_by_symbol={
                symbol: normalized_files[symbol]
                for symbol in required_symbols
            },
            series_by_symbol=series_by_symbol,
            trading_dates=trading_dates,
            latest_complete_common_date=(
                latest_complete_common_date
            ),
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
        CanonicalDailyDecisionRouter()
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
