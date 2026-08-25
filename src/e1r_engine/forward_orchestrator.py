from __future__ import annotations

from e1r_engine.core import E1RCoreEngine

from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Iterable,
    Mapping,
    Optional,
    Protocol,
    Sequence,
)

from e1r_engine.canonical_regime import (
    CanonicalRegimeGenerator,
    CanonicalRegimeTimeline,
)
from e1r_engine.contracts import (
    DailyBar,
    MarketSnapshot,
)
from e1r_engine.forward_runtime import (
    DailyCommitResult,
    ForwardAccountRepository,
    ForwardContractError,
    ForwardDailyCommitter,
    ForwardDatePlanner,
    ForwardMarketDataAdapter,
    ForwardRuntimeState,
    ForwardSeedLoader,
    SidewaysDecisionContext,
)
from e1r_engine.market_gate import MarketGateDecision
from e1r_engine.state import AccountState
from e1r_engine.uptrend_consumer import (
    UptrendConsumerInputs,
)
from e1r_engine.uptrend_signal_adapter import (
    UptrendSignalAdapter,
)


SeriesBySymbol = Mapping[
    str,
    Mapping[str, DailyBar],
]


class MarketGateProvider(Protocol):
    """
    Existing formal Market Gate dependency.

    This orchestrator deliberately does not implement or recompute
    Market Gate policy.
    """

    def __call__(
        self,
        *,
        date: str,
        index_series: SeriesBySymbol,
    ) -> MarketGateDecision:
        ...


class ManagementActionProvider(Protocol):
    """
    Existing stock-management dependency.

    This orchestrator deliberately does not implement trade_action,
    EXIT, REDUCE, ADD, or HOLD policy.
    """

    def __call__(
        self,
        *,
        date: str,
        account: AccountState,
        stock_series: SeriesBySymbol,
    ) -> Mapping[str, str]:
        ...


@dataclass(frozen=True)
class ForwardRegimeProvider:
    """
    Thin Forward wrapper around the canonical Regime generator.

    It creates no alternate Regime formula and reads no historical
    Regime artifact.
    """

    timeline: CanonicalRegimeTimeline
    source_symbol: str = "SPX"

    @classmethod
    def from_spx_series(
        cls,
        *,
        spx_series: Mapping[str, DailyBar],
    ) -> "ForwardRegimeProvider":
        ordered_bars = [
            spx_series[date]
            for date in sorted(spx_series)
        ]

        if not ordered_bars:
            raise ForwardContractError(
                "Forward Regime requires non-empty SPX series"
            )

        timeline = CanonicalRegimeGenerator.generate(
            ordered_bars
        )

        return cls(timeline=timeline)

    def record_for_date(self, date: str) -> Any:
        return self.timeline.record_for_date(date)

    def decision_for_date(self, date: str) -> Any:
        return self.timeline.decision_for_date(date)


@dataclass(frozen=True)
class ForwardMarketSnapshotBuilder:
    """
    Formal Forward MarketSnapshot construction boundary.

    It only assembles existing contract objects.
    """

    regime_provider: ForwardRegimeProvider | None = None
    required_indices: tuple[str, ...] = (
        "SPX",
        "NDX",
        "SOX",
    )

    def build(
        self,
        *,
        date: str,
        universe: Sequence[str],
        series_by_symbol: SeriesBySymbol,
        required_data_symbols: Sequence[str] = (),
    ) -> MarketSnapshot:
        symbol_order = tuple(universe)
        required_data_order = tuple(required_data_symbols)

        if len(set(symbol_order)) != len(symbol_order):
            raise ForwardContractError(
                "Forward universe contains duplicate symbols"
            )

        missing_indices = [
            symbol
            for symbol in self.required_indices
            if symbol not in series_by_symbol
            or date not in series_by_symbol[symbol]
        ]

        if missing_indices:
            raise ForwardContractError(
                "Forward snapshot missing index bars: "
                + ",".join(missing_indices)
            )

        snapshot_symbols = tuple(
            sorted(set(symbol_order) | set(required_data_order))
        )
        missing_stocks = [
            symbol
            for symbol in snapshot_symbols
            if symbol not in series_by_symbol
            or date not in series_by_symbol[symbol]
        ]

        if missing_stocks:
            raise ForwardContractError(
                "Forward snapshot missing stock bars: "
                + ",".join(missing_stocks)
            )

        prices_by_symbol = {
            symbol: series_by_symbol[symbol][date]
            for symbol in snapshot_symbols
        }

        indices = {
            symbol: series_by_symbol[symbol][date]
            for symbol in self.required_indices
        }

        return MarketSnapshot(
            date=date,
            universe=list(symbol_order),
            prices_by_symbol=prices_by_symbol,
            indices=indices,
            regime=None,
            metadata={
                "source":
                    "ForwardMarketSnapshotBuilder",
                "regime_source":
                    "E1RCoreEngine.step",
                "external_regime_injected":
                    False,
                "strategy_logic_reimplemented":
                    False,
            },
            history_by_symbol={
                symbol: {
                    row_date: bar
                    for row_date, bar in series_by_symbol[symbol].items()
                    if row_date <= date
                }
                for symbol in set(snapshot_symbols) | set(self.required_indices)
            },
        )


@dataclass(frozen=True)
class ForwardStrategyInputs:
    uptrend_inputs: UptrendConsumerInputs | None
    sideways_context: SidewaysDecisionContext | None
    branch: str
    regime: str | None
    subclass: str | None
    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(frozen=True)
class ForwardStrategyInputBuilder:
    """
    Strategy-input wiring only.

    UPTREND:
      Reuses UptrendSignalAdapter and an injected formal Market Gate.

    SIDEWAYS/MA_CONFLICT:
      Builds the existing SidewaysDecisionContext structure and uses
      an injected formal stock-management provider.

    No strategy formula is implemented here.
    """

    management_action_provider: (
        ManagementActionProvider
    )
    engine: E1RCoreEngine
    min_uptrend_history: int = 61

    @staticmethod
    def _close_history(
        *,
        symbol: str,
        date: str,
        series_by_symbol: SeriesBySymbol,
    ) -> list[float]:
        if symbol not in series_by_symbol:
            raise ForwardContractError(
                f"{symbol}: missing Forward price series"
            )

        values = []

        for row_date in sorted(
            series_by_symbol[symbol]
        ):
            if row_date > date:
                break

            bar = series_by_symbol[symbol][row_date]

            if bar.close is None:
                continue

            values.append(float(bar.close))

        return values

    @staticmethod
    def _sideways_asset(
        *,
        symbol: str,
        date: str,
        series_by_symbol: SeriesBySymbol,
    ) -> dict[str, Any]:
        if symbol not in series_by_symbol:
            raise ForwardContractError(
                f"{symbol}: missing SIDEWAYS series"
            )

        bars = []

        for row_date in sorted(
            series_by_symbol[symbol]
        ):
            if row_date > date:
                break

            bar = series_by_symbol[symbol][row_date]

            if bar.close is None:
                continue

            bars.append({
                "date": row_date,
                "close": float(bar.close),
            })

        if not bars:
            raise ForwardContractError(
                f"{symbol}: empty SIDEWAYS history"
            )

        return {
            "symbol": symbol,
            "bars": bars,
            "dates": [
                row["date"]
                for row in bars
            ],
            "by_date": {
                row["date"]: row
                for row in bars
            },
            "date_to_idx": {
                row["date"]: index
                for index, row in enumerate(bars)
            },
        }

    def build(
        self,
        *,
        snapshot: MarketSnapshot,
        account: AccountState,
        universe: Sequence[str],
        series_by_symbol: SeriesBySymbol,
    ) -> ForwardStrategyInputs:
        regime = (
            None
            if snapshot.regime is None
            else snapshot.regime.spx_regime
        )

        subclass = (
            None
            if snapshot.regime is None
            else snapshot.regime.subclass
        )

        if regime == "UPTREND":
            market_state_decision, gate = self.engine.evaluate_market_state_and_gate_from_series(
                date=snapshot.date,
                index_series={symbol: series_by_symbol[symbol] for symbol in ("SPX", "NDX", "SOX")},
                existing_positions_count=len(account.positions),
            )

            if gate.date != snapshot.date:
                raise ForwardContractError(
                    "Engine Market Gate date does not match Forward snapshot date"
                )

            symbol_order = tuple(universe)
            histories = {
                symbol: self._close_history(
                    symbol=symbol,
                    date=snapshot.date,
                    series_by_symbol=series_by_symbol,
                )
                for symbol in symbol_order
            }

            insufficient = [
                symbol
                for symbol, values in histories.items()
                if len(values)
                < self.min_uptrend_history
            ]

            if insufficient:
                raise ForwardContractError(
                    "UPTREND history is insufficient: "
                    + ",".join(insufficient)
                )

            adapter_result = (
                UptrendSignalAdapter.build(
                    date=snapshot.date,
                    symbols=symbol_order,
                    prices_by_symbol=histories,
                )
            )

            uptrend_inputs = (
                adapter_result.to_consumer_inputs(
                    market_gate_decision=gate,
                    metadata={
                        "source":
                            "ForwardStrategyInputBuilder",
                        "strategy_logic_reimplemented":
                            False,
                    },
                )
            )

            return ForwardStrategyInputs(
                uptrend_inputs=uptrend_inputs,
                sideways_context=None,
                branch="UPTREND",
                regime=regime,
                subclass=subclass,
                metadata={
                    "uptrend_adapter":
                        "UptrendSignalAdapter",
                    "market_state_source": "E1RCoreEngine.MarketStateEvaluator",
                    "market_gate_source": "E1RCoreEngine.MarketGateEvaluator",
                    "market_state": market_state_decision.market_state,
                    "entry_capacity": market_state_decision.entry_capacity,
                },
            )

        if (
            regime == "SIDEWAYS"
            and subclass == "MA_CONFLICT"
        ):
            stocks = {
                symbol: self._sideways_asset(
                    symbol=symbol,
                    date=snapshot.date,
                    series_by_symbol=series_by_symbol,
                )
                for symbol in universe
            }

            spx = self._sideways_asset(
                symbol="SPX",
                date=snapshot.date,
                series_by_symbol=series_by_symbol,
            )

            management_actions = dict(
                self.management_action_provider(
                    date=snapshot.date,
                    account=account,
                    stock_series={
                        symbol:
                            series_by_symbol[symbol]
                        for symbol in universe
                    },
                )
            )

            unknown_actions = sorted(
                {
                    action.upper()
                    for action
                    in management_actions.values()
                }
                - {
                    "HOLD",
                    "ADD",
                    "REDUCE",
                    "EXIT",
                }
            )

            if unknown_actions:
                raise ForwardContractError(
                    "SIDEWAYS management provider "
                    "returned unsupported actions: "
                    + ",".join(unknown_actions)
                )

            context = SidewaysDecisionContext(
                stocks=stocks,
                spx=spx,
                management_actions=management_actions,
            )

            return ForwardStrategyInputs(
                uptrend_inputs=None,
                sideways_context=context,
                branch="SIDEWAYS_MA_CONFLICT",
                regime=regime,
                subclass=subclass,
                metadata={
                    "sideways_ranker":
                        "SidewaysCore",
                    "sideways_policy":
                        "SidewaysExecutionPolicy",
                    "management_action_source":
                        type(
                            self.management_action_provider
                        ).__name__,
                    "strategy_logic_reimplemented":
                        False,
                },
            )

        return ForwardStrategyInputs(
            uptrend_inputs=None,
            sideways_context=None,
            branch=regime or "UNCLASSIFIED",
            regime=regime,
            subclass=subclass,
            metadata={
                "management_only": True,
                "new_risk_expansion": False,
            },
        )


@dataclass(frozen=True)
class ForwardDryRunDay:
    date: str
    branch: str
    regime: str | None
    subclass: str | None
    universe_count: int
    execution_bar_count: int
    uptrend_inputs_present: bool
    sideways_context_present: bool


@dataclass(frozen=True)
class ForwardDryRunResult:
    status: str
    planned_dates: tuple[str, ...]
    days: tuple[ForwardDryRunDay, ...]
    repository_initialized: bool
    commit_day_called: bool
    forward_state_mutated: bool
    official_artifacts_written: bool
    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class OfficialForwardCatchupRunner:
    """
    Formal orchestration boundary.

    dry_run():
      Validates the complete daily construction path without touching
      Forward repository state or official artifacts.

    run():
      Performs initialization and commit_day only when the caller
      explicitly passes allow_official_write=True.
    """

    seed_loader: ForwardSeedLoader
    repository: ForwardAccountRepository
    date_planner: ForwardDatePlanner
    market_data_adapter: ForwardMarketDataAdapter
    snapshot_builder: ForwardMarketSnapshotBuilder
    strategy_input_builder: ForwardStrategyInputBuilder
    committer: ForwardDailyCommitter
    universe: tuple[str, ...]
    series_by_symbol: SeriesBySymbol
    required_execution_symbols: tuple[str, ...]
    source_hash_provider: (
        Callable[[str], Mapping[str, str]]
        | None
    ) = None
    shadow_observer: Optional[Callable[..., Any]] = None
    production_universe_gate: Optional[Callable[..., Any]] = None

    def _latest_complete_date(self) -> str:
        return (
            self.market_data_adapter
            .latest_complete_common_date(
                series_by_symbol=self.series_by_symbol,
                required_symbols=(
                    self.required_execution_symbols
                ),
            )
        )

    def _planned_dates(
        self,
        *,
        last_committed_date: str | None,
    ) -> list[str]:
        return self.date_planner.plan(
            last_committed_date=last_committed_date,
            latest_complete_common_data_date=(
                self._latest_complete_date()
            ),
        )

    def _required_symbols_for_account(
        self,
        account: AccountState,
        pending_orders: Sequence[Any] = (),
    ) -> tuple[str, ...]:
        """Return every symbol whose T+1 bar can affect execution.

        New BUY orders are not positions yet.  Excluding pending-order symbols
        therefore turns an available T+1 bar into a false ``MISSING_T1_BAR``
        skip.  Keep the stable index/holding set, and add every pending order.
        """
        return tuple(
            sorted(
                set(self.required_execution_symbols)
                | set(account.positions)
                | {
                    str(order.symbol).strip().upper()
                    for order in pending_orders
                    if getattr(order, "symbol", None)
                }
            )
        )

    def _production_universe_decision(
        self,
        *,
        execution_date: str,
        account: AccountState,
        candidate_actions: Sequence[Mapping[str, Any]] = (),
    ) -> Any | None:
        if self.production_universe_gate is None:
            return None
        data_ready = tuple(
            sorted(
                symbol for symbol in self.universe
                if symbol in self.series_by_symbol
                and execution_date in self.series_by_symbol[symbol]
            )
        )
        return self.production_universe_gate(
            expected_execution_date=execution_date,
            production_catalogue=self.universe,
            production_eligible=self.universe,
            holdings_symbols=account.positions,
            data_ready_symbols=data_ready,
            required_indices=self.snapshot_builder.required_indices,
            candidate_actions=candidate_actions,
        )

    def _daily_data_ready_universe(
        self,
        execution_date: str,
    ) -> tuple[str, ...]:
        return tuple(
            sorted(
                symbol
                for symbol in self.universe
                if symbol in self.series_by_symbol
                and execution_date in self.series_by_symbol[symbol]
            )
        )

    def run_shadow_probe(self) -> tuple[Mapping[str, Any], ...]:
        """Observe planned dates and stop before Engine, T1, or commit.

        This is the explicit UV-step-3 acceptance boundary.  It loads only
        the seed/current Forward state and the already composed market-data
        catalogue.  It does not build a strategy snapshot, call Engine.step,
        execute T1, initialize/save the repository, or publish production
        artifacts.
        """
        if self.shadow_observer is None:
            raise ForwardContractError(
                "Forward shadow observer is disabled; explicit injection is required"
            )

        seed_state = self.seed_loader.load()
        seed_state.validate()
        if self.repository.exists():
            current_state = self.repository.load()
            current_state.validate()
        else:
            current_state = seed_state

        planned_dates = self._planned_dates(
            last_committed_date=current_state.last_committed_date
        )
        probe_date_basis = "PENDING_FORWARD_DATE_PLANNER_DATE"
        if not planned_dates:
            anchor = current_state.last_committed_date
            if not anchor or not any(
                symbol in self.series_by_symbol
                and anchor in self.series_by_symbol[symbol]
                for symbol in self.required_execution_symbols
            ):
                raise ForwardContractError(
                    "Forward shadow probe has neither a pending planned date "
                    "nor a data-backed last committed planner date"
                )
            planned_dates = (anchor,)
            probe_date_basis = (
                "CURRENT_LAST_COMMITTED_FORWARD_DATE_PLANNER_DATE"
            )
        reports = []
        holdings = tuple(sorted(current_state.account.positions))
        required_indices = tuple(self.snapshot_builder.required_indices)
        for planned_date in planned_dates:
            data_ready = tuple(
                sorted(
                    symbol
                    for symbol in self.universe
                    if symbol in self.series_by_symbol
                    and planned_date in self.series_by_symbol[symbol]
                )
            )
            result = self.shadow_observer(
                market_date=planned_date,
                expected_execution_date=planned_date,
                production_catalogue=self.universe,
                production_eligible=self.universe,
                holdings_symbols=holdings,
                data_ready_symbols=data_ready,
                required_indices=required_indices,
                candidate_actions=(),
                date_source="FORWARD_DATE_PLANNER",
            )
            report = (
                result.to_dict()
                if hasattr(result, "to_dict")
                else dict(result)
            )
            reports.append(
                dict(report, probe_date_basis=probe_date_basis)
            )
        return tuple(reports)

    def dry_run(self) -> ForwardDryRunResult:
        seed_state = self.seed_loader.load()
        seed_state.validate()

        if self.repository.exists():
            current_state = self.repository.load()
            current_state.validate()
        else:
            current_state = seed_state

        planned_dates = self._planned_dates(
            last_committed_date=(
                current_state.last_committed_date
            )
        )

        days = []

        for date in planned_dates:
            universe_decision = self._production_universe_decision(
                execution_date=date,
                account=current_state.account,
            )
            eligible_universe = (
                self._daily_data_ready_universe(date)
                if universe_decision is None
                else universe_decision.eligible_buy_universe
            )
            required_data = (
                () if universe_decision is None
                else tuple(
                    symbol
                    for symbol in universe_decision.required_data_universe
                    if symbol not in self.snapshot_builder.required_indices
                )
            )
            snapshot = self.snapshot_builder.build(
                date=date,
                universe=eligible_universe,
                series_by_symbol=self.series_by_symbol,
                required_data_symbols=required_data,
            )

            engine_result = (
                self.committer.decision_router.engine.step(
                    snapshot,
                    current_state.account.mark_to_market(
                        prices={
                            symbol: bar.close
                            for symbol, bar in snapshot.prices_by_symbol.items()
                        },
                        date=date,
                    ),
                )
            )

            execution_symbols = (
                self._required_symbols_for_account(
                    current_state.account,
                    current_state.pending_orders,
                )
            )

            bars = (
                ForwardMarketDataAdapter
                .bars_for_date(
                    series_by_symbol=(
                        self.series_by_symbol
                    ),
                    required_symbols=execution_symbols,
                    trading_date=date,
                )
            )

            if set(bars) != set(execution_symbols):
                raise ForwardContractError(
                    "dry-run execution-bar contract mismatch"
                )

            days.append(
                ForwardDryRunDay(
                    date=date,
                    branch=engine_result.decision_trace.branch,
                    regime=engine_result.decision_trace.market_regime,
                    subclass=engine_result.decision_trace.regime_subclass,
                    universe_count=len(
                        snapshot.universe
                    ),
                    execution_bar_count=len(bars),
                    uptrend_inputs_present=(
                        engine_result.decision_trace.branch
                        == "UPTREND"
                    ),
                    sideways_context_present=(
                        engine_result.decision_trace.branch
                        == "SIDEWAYS_MA_CONFLICT"
                    ),
                )
            )

        return ForwardDryRunResult(
            status="PASS_FORWARD_ORCHESTRATOR_DRY_RUN",
            planned_dates=tuple(planned_dates),
            days=tuple(days),
            repository_initialized=False,
            commit_day_called=False,
            forward_state_mutated=False,
            official_artifacts_written=False,
            metadata={
                "strategy_logic_reimplemented": False,
                "canonical_regime_source":
                    "CanonicalRegimeGenerator",
                "uptrend_source":
                    "UptrendSignalAdapter",
                "sideways_source":
                    "SidewaysCore/"
                    "SidewaysExecutionPolicy",
            },
        )

    def run(
        self,
        *,
        allow_official_write: bool = False,
    ) -> list[DailyCommitResult]:
        if not allow_official_write:
            raise ForwardContractError(
                "Official Forward write is not authorized; "
                "pass allow_official_write=True only after "
                "explicit runtime authorization"
            )

        if not self.repository.exists():
            seed_state = self.seed_loader.load()
            seed_state.validate()
            self.repository.initialize(seed_state)

        results = []

        while True:
            state = self.repository.load()
            state.validate()

            planned_dates = self._planned_dates(
                last_committed_date=(
                    state.last_committed_date
                )
            )

            if not planned_dates:
                break

            date = planned_dates[0]

            pending_actions = tuple(
                {
                    "symbol": order.symbol,
                    "action": order.intent_type,
                }
                for order in state.pending_orders
            )
            universe_decision = self._production_universe_decision(
                execution_date=date,
                account=state.account,
                candidate_actions=pending_actions,
            )
            if (
                universe_decision is not None
                and universe_decision.blocked_risk_increases
            ):
                raise ForwardContractError(
                    "HOLD_UV_STEP_4_FORWARD_PRODUCTION: "
                    "pending BUY/ADD failed pre-execution Universe gate"
                )
            eligible_universe = (
                self._daily_data_ready_universe(date)
                if universe_decision is None
                else universe_decision.eligible_buy_universe
            )
            required_data = (
                () if universe_decision is None
                else tuple(
                    symbol
                    for symbol in universe_decision.required_data_universe
                    if symbol not in self.snapshot_builder.required_indices
                )
            )

            snapshot = self.snapshot_builder.build(
                date=date,
                universe=eligible_universe,
                series_by_symbol=self.series_by_symbol,
                required_data_symbols=required_data,
            )

            execution_symbols = (
                self._required_symbols_for_account(
                    state.account,
                    state.pending_orders,
                )
            )

            bars = (
                ForwardMarketDataAdapter
                .bars_for_date(
                    series_by_symbol=(
                        self.series_by_symbol
                    ),
                    required_symbols=execution_symbols,
                    trading_date=date,
                )
            )

            source_hashes = (
                {}
                if self.source_hash_provider is None
                else dict(
                    self.source_hash_provider(date)
                )
            )

            result = self.committer.commit_day(
                trading_date=date,
                snapshot=snapshot,
                t1_bars_by_symbol=bars,
                uptrend_inputs=None,
                sideways_context=None,
                source_hashes=source_hashes,
            )

            results.append(result)

            if result.status != "COMMITTED":
                break

        return results


__all__ = [
    "ForwardDryRunDay",
    "ForwardDryRunResult",
    "ForwardMarketSnapshotBuilder",
    "ForwardRegimeProvider",
    "ForwardStrategyInputBuilder",
    "ForwardStrategyInputs",
    "ManagementActionProvider",
    "MarketGateProvider",
    "OfficialForwardCatchupRunner",
]
