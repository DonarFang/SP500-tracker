from __future__ import annotations

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
from e1r_engine.forward_providers import (
    ExplicitMarketStateProvider,
    FormalManagementActionProvider,
    FormalMarketGateProvider,
    MarketStateRecord,
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
class ProductionForwardComposition:
    regime_provider: ForwardRegimeProvider
    market_state_provider: (
        ExplicitMarketStateProvider
    )
    market_gate_provider: (
        FormalMarketGateProvider
    )
    management_action_provider: (
        FormalManagementActionProvider
    )
    snapshot_builder: (
        ForwardMarketSnapshotBuilder
    )
    strategy_input_builder: (
        ForwardStrategyInputBuilder
    )
    seed_loader: ForwardSeedLoader
    repository: ForwardAccountRepository
    date_planner: ForwardDatePlanner
    market_data_adapter: (
        ForwardMarketDataAdapter
    )
    decision_router: (
        CanonicalDailyDecisionRouter
    )
    execution_engine: T1ExecutionEngine
    artifact_writer: (
        OfficialForwardArtifactWriter
    )
    committer: ForwardDailyCommitter
    runner: OfficialForwardCatchupRunner


def build_production_forward_composition(
    *,
    seed_root: Path | str,
    runtime_root: Path | str,
    trading_dates: Sequence[str],
    universe: Sequence[str],
    series_by_symbol: SeriesBySymbol,
    market_state_by_date: Mapping[
        str,
        MarketStateRecord,
    ],
    runtime_commit_provider: Callable[[], str],
    source_hash_provider: (
        Callable[[str], Mapping[str, str]]
        | None
    ) = None,
) -> ProductionForwardComposition:
    if not trading_dates:
        raise ValueError(
            "trading_dates must not be empty"
        )

    if not universe:
        raise ValueError(
            "universe must not be empty"
        )

    if "SPX" not in series_by_symbol:
        raise ValueError(
            "SPX series is required"
        )

    missing_universe = sorted(
        set(universe)
        - set(series_by_symbol)
    )

    if missing_universe:
        raise ValueError(
            "missing universe series: "
            + ",".join(missing_universe)
        )

    regime_provider = (
        ForwardRegimeProvider.from_spx_series(
            spx_series=series_by_symbol["SPX"]
        )
    )

    market_state_provider = (
        ExplicitMarketStateProvider(
            records_by_date=(
                market_state_by_date
            )
        )
    )

    market_gate_provider = (
        FormalMarketGateProvider(
            market_state_provider=(
                market_state_provider
            )
        )
    )

    management_action_provider = (
        FormalManagementActionProvider()
    )

    snapshot_builder = (
        ForwardMarketSnapshotBuilder(
            regime_provider=regime_provider
        )
    )

    strategy_input_builder = (
        ForwardStrategyInputBuilder(
            market_gate_provider=(
                market_gate_provider
            ),
            management_action_provider=(
                management_action_provider
            ),
        )
    )

    seed_loader = ForwardSeedLoader(
        seed_root
    )

    repository = ForwardAccountRepository(
        runtime_root
    )

    date_planner = ForwardDatePlanner(
        trading_dates
    )

    market_data_adapter = (
        ForwardMarketDataAdapter()
    )

    decision_router = (
        CanonicalDailyDecisionRouter()
    )

    execution_engine = T1ExecutionEngine(
        one_way_cost=0.001,
        max_positions=3,
    )

    artifact_writer = (
        OfficialForwardArtifactWriter(
            runtime_root
        )
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

    runner = OfficialForwardCatchupRunner(
        seed_loader=seed_loader,
        repository=repository,
        date_planner=date_planner,
        market_data_adapter=(
            market_data_adapter
        ),
        snapshot_builder=snapshot_builder,
        strategy_input_builder=(
            strategy_input_builder
        ),
        committer=committer,
        universe=tuple(universe),
        series_by_symbol=series_by_symbol,
        required_execution_symbols=tuple(
            sorted(
                set(universe)
                | {"SPX", "NDX", "SOX"}
            )
        ),
        source_hash_provider=(
            source_hash_provider
        ),
    )

    return ProductionForwardComposition(
        regime_provider=regime_provider,
        market_state_provider=(
            market_state_provider
        ),
        market_gate_provider=(
            market_gate_provider
        ),
        management_action_provider=(
            management_action_provider
        ),
        snapshot_builder=snapshot_builder,
        strategy_input_builder=(
            strategy_input_builder
        ),
        seed_loader=seed_loader,
        repository=repository,
        date_planner=date_planner,
        market_data_adapter=(
            market_data_adapter
        ),
        decision_router=decision_router,
        execution_engine=execution_engine,
        artifact_writer=artifact_writer,
        committer=committer,
        runner=runner,
    )


__all__ = [
    "ProductionForwardComposition",
    "build_production_forward_composition",
]
