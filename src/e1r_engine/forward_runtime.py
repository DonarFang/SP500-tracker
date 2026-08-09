from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from e1r_engine.capped_atr_stop import (
    CappedAtrStopPolicy,
    ENTRY_METADATA_KEY,
    POSITION_METADATA_KEY,
    VARIANT_ID,
    annotate_buy_intent,
    build_frozen_state,
)
from e1r_engine.contracts import DailyBar, MarketSnapshot
from e1r_engine.core import E1RCoreEngine
from e1r_engine.state import (
    AccountState,
    DecisionTrace,
    Fill,
    OrderIntent,
    PositionState,
)


ENGINE_ID = "FD-M3180125-SP500-TOP3-engine"
RUNTIME_SCHEMA_VERSION = "1.0.0"

FIRST_FORWARD_MARKET_DATE = "2026-06-17"
SEED_DATE = "2026-06-16"
EXECUTION_PRIORITY = {
    "EXIT": 0,
    "REDUCE": 1,
    "REL_REDUCE": 2,
    "TP_REDUCE": 3,
    "ADD": 4,
    "BUY": 5,
}

EXECUTABLE_INTENT_TYPES = frozenset(
    {
        "BUY",
        "ADD",
        "REDUCE",
        "EXIT",
    }
)


class ForwardRuntimeError(RuntimeError):
    """Base error for the official Shared Runtime."""


class ForwardContractError(ForwardRuntimeError):
    """Raised when frozen runtime contracts are violated."""


class ForwardDataError(ForwardRuntimeError):
    """Raised when required market data is incomplete."""


class ForwardStateError(ForwardRuntimeError):
    """Raised when persisted runtime state is invalid."""


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            default=_json_default,
        )
        + "\n"
    ).encode("utf-8")


def pretty_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
            default=_json_default,
        )
        + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        while True:
            block = stream.read(1024 * 1024)

            if not block:
                break

            digest.update(block)

    return digest.hexdigest()


def deterministic_id(*parts: Any) -> str:
    normalized = "|".join(
        "" if part is None else str(part)
        for part in parts
    )

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()


def _json_default(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)

    if isinstance(value, Path):
        return str(value)

    if isinstance(value, (date, datetime)):
        return value.isoformat()

    raise TypeError(
        f"Object of type {type(value).__name__} "
        "is not JSON serializable"
    )


def _atomic_write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
    )

    temporary_path = Path(temporary_name)

    try:
        with os.fdopen(file_descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())

        os.replace(temporary_path, path)

    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def atomic_write_json(path: Path, value: Any) -> None:
    _atomic_write_bytes(
        path,
        pretty_json_bytes(value),
    )


def load_json(path: Path) -> Any:
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def _coerce_float(
    value: Any,
    *,
    field_name: str,
) -> float:
    try:
        converted = float(value)
    except (TypeError, ValueError) as exc:
        raise ForwardContractError(
            f"{field_name} is not numeric: {value!r}"
        ) from exc

    return converted


def _position_metadata(
    source: Mapping[str, Any],
) -> dict[str, Any]:
    metadata = dict(source.get("metadata") or {})

    for key in (
        "origin_branch",
        "size_units",
        "remaining_cost_basis",
        "entry_shares",
        "entry_execution_price",
        "position_state_source",
        "source_trade_index",
        "source_json_path",
        "forward_policy",
    ):
        if key in source and source[key] is not None:
            metadata[key] = source[key]

    metadata.setdefault(
        "origin_branch",
        source.get("origin_branch") or "UPTREND",
    )

    metadata.setdefault(
        "size_units",
        float(source.get("size_units", 1.0)),
    )

    return metadata


def account_to_dict(account: AccountState) -> dict[str, Any]:
    return {
        "date": account.date,
        "cash": account.cash,
        "positions": {
            symbol: {
                "symbol": position.symbol,
                "quantity": position.quantity,
                "avg_cost": position.avg_cost,
                "last_price": position.last_price,
                "market_value": position.market_value,
                "unrealized_pnl": position.unrealized_pnl,
                "entry_date": position.entry_date,
                "last_update_date": position.last_update_date,
                "metadata": dict(position.metadata),
            }
            for symbol, position
            in sorted(account.positions.items())
        },
        "total_equity": account.total_equity,
        "positions_value": account.positions_value,
        "open_positions_count": account.open_positions_count,
        "metadata": dict(account.metadata),
    }


def account_from_dict(value: Mapping[str, Any]) -> AccountState:
    raw_positions = value.get("positions") or {}

    if isinstance(raw_positions, list):
        raw_positions = {
            row["symbol"]: row
            for row in raw_positions
        }

    positions: dict[str, PositionState] = {}

    for symbol, raw in raw_positions.items():
        resolved_symbol = str(
            raw.get("symbol") or symbol
        )

        quantity = _coerce_float(
            raw.get(
                "quantity",
                raw.get(
                    "remaining_shares",
                    raw.get(
                        "shares",
                        raw.get("units", 0.0),
                    ),
                ),
            ),
            field_name=f"{resolved_symbol}.quantity",
        )

        avg_cost = _coerce_float(
            raw.get(
                "avg_cost",
                raw.get(
                    "average_cost",
                    raw.get(
                        "entry_price",
                        raw.get("entry_execution_price", 0.0),
                    ),
                ),
            ),
            field_name=f"{resolved_symbol}.avg_cost",
        )

        last_price = _coerce_float(
            raw.get(
                "last_price",
                raw.get(
                    "effective_liquidation_price_for_reconciliation_only",
                    avg_cost,
                ),
            ),
            field_name=f"{resolved_symbol}.last_price",
        )

        entry_date = str(
            raw.get("entry_date")
            or raw.get("entry_execution_date")
            or value.get("date")
            or SEED_DATE
        )

        last_update_date = str(
            raw.get("last_update_date")
            or value.get("date")
            or SEED_DATE
        )

        market_value = quantity * last_price
        unrealized_pnl = (
            last_price - avg_cost
        ) * quantity

        positions[resolved_symbol] = PositionState(
            symbol=resolved_symbol,
            quantity=quantity,
            avg_cost=avg_cost,
            last_price=last_price,
            market_value=market_value,
            unrealized_pnl=unrealized_pnl,
            entry_date=entry_date,
            last_update_date=last_update_date,
            metadata=_position_metadata(raw),
        )

    cash = _coerce_float(
        value.get("cash", 0.0),
        field_name="account.cash",
    )

    positions_value = sum(
        position.market_value
        for position in positions.values()
    )

    account = AccountState(
        date=str(value.get("date") or SEED_DATE),
        cash=cash,
        positions=positions,
        total_equity=cash + positions_value,
        positions_value=positions_value,
        open_positions_count=len(positions),
        metadata=dict(value.get("metadata") or {}),
    )

    validation = account.validate(max_positions=3)

    if not validation["ok"]:
        raise ForwardStateError(
            "Invalid AccountState: "
            + "; ".join(validation["errors"])
        )

    for position in account.positions.values():
        if not position.metadata.get("origin_branch"):
            raise ForwardStateError(
                f"{position.symbol}: missing origin_branch"
            )

    return account


def order_intent_to_dict(
    intent: OrderIntent,
) -> dict[str, Any]:
    return {
        "date": intent.date,
        "symbol": intent.symbol,
        "intent_type": intent.intent_type,
        "side": intent.side,
        "target_quantity": intent.target_quantity,
        "quantity_delta": intent.quantity_delta,
        "reason": intent.reason,
        "branch": intent.branch,
        "metadata": dict(intent.metadata),
    }


def order_intent_from_dict(
    value: Mapping[str, Any],
) -> OrderIntent:
    return OrderIntent(
        date=str(value["date"]),
        symbol=str(value.get("symbol") or ""),
        intent_type=value["intent_type"],
        side=value.get("side"),
        target_quantity=(
            None
            if value.get("target_quantity") is None
            else float(value["target_quantity"])
        ),
        quantity_delta=(
            None
            if value.get("quantity_delta") is None
            else float(value["quantity_delta"])
        ),
        reason=str(value.get("reason") or ""),
        branch=value.get("branch") or "NO_TRADE",
        metadata=dict(value.get("metadata") or {}),
    )


def fill_to_dict(fill: Fill) -> dict[str, Any]:
    return {
        "date": fill.date,
        "symbol": fill.symbol,
        "side": fill.side,
        "quantity": fill.quantity,
        "price": fill.price,
        "gross_amount": fill.gross_amount,
        "status": fill.status,
        "reason": fill.reason,
        "metadata": dict(fill.metadata),
    }


@dataclass(frozen=True)
class PendingOrderRecord:
    order_id: str
    signal_date: str
    symbol: str
    intent_type: str
    side: str
    branch: str
    sequence: int
    reason: str
    target_quantity: float | None
    quantity_delta: float | None
    metadata: dict[str, Any] = field(default_factory=dict)
    status: str = "PENDING"

    @staticmethod
    def from_intent(
        intent: OrderIntent,
        *,
        sequence: int,
    ) -> "PendingOrderRecord":
        if intent.intent_type not in EXECUTABLE_INTENT_TYPES:
            raise ForwardContractError(
                "Only executable OrderIntents may enter "
                "the PendingOrderLedger"
            )

        if not intent.symbol:
            raise ForwardContractError(
                "Executable OrderIntent is missing symbol"
            )

        if intent.side is None:
            raise ForwardContractError(
                f"{intent.intent_type}: side is required"
            )

        if (
            intent.intent_type == "SIM_END"
            or str(intent.reason).upper() == "SIM_END"
        ):
            raise ForwardContractError(
                "SIM_END is prohibited in Forward Runtime"
            )

        order_id = deterministic_id(
            ENGINE_ID,
            intent.date,
            intent.symbol,
            intent.intent_type,
            intent.branch,
            sequence,
        )

        return PendingOrderRecord(
            order_id=order_id,
            signal_date=intent.date,
            symbol=intent.symbol,
            intent_type=intent.intent_type,
            side=intent.side,
            branch=intent.branch,
            sequence=sequence,
            reason=intent.reason,
            target_quantity=intent.target_quantity,
            quantity_delta=intent.quantity_delta,
            metadata=dict(intent.metadata),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(
        value: Mapping[str, Any],
    ) -> "PendingOrderRecord":
        return PendingOrderRecord(
            order_id=str(value["order_id"]),
            signal_date=str(value["signal_date"]),
            symbol=str(value["symbol"]),
            intent_type=str(value["intent_type"]),
            side=str(value["side"]),
            branch=str(value["branch"]),
            sequence=int(value["sequence"]),
            reason=str(value.get("reason") or ""),
            target_quantity=(
                None
                if value.get("target_quantity") is None
                else float(value["target_quantity"])
            ),
            quantity_delta=(
                None
                if value.get("quantity_delta") is None
                else float(value["quantity_delta"])
            ),
            metadata=dict(value.get("metadata") or {}),
            status=str(value.get("status") or "PENDING"),
        )


@dataclass
class ForwardRuntimeState:
    schema_version: str
    engine_id: str
    seed_date: str
    first_forward_market_date: str
    last_committed_date: str | None
    account: AccountState
    pending_orders: list[PendingOrderRecord]
    closed_trades: list[dict[str, Any]]
    equity_history: list[dict[str, Any]]
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if self.engine_id != ENGINE_ID:
            raise ForwardStateError(
                f"Unexpected engine_id={self.engine_id!r}"
            )

        if self.seed_date != SEED_DATE:
            raise ForwardStateError(
                f"Unexpected seed_date={self.seed_date!r}"
            )

        if (
            self.first_forward_market_date
            != FIRST_FORWARD_MARKET_DATE
        ):
            raise ForwardStateError(
                "Unexpected first_forward_market_date"
            )

        validation = self.account.validate(max_positions=3)

        if not validation["ok"]:
            raise ForwardStateError(
                "; ".join(validation["errors"])
            )

        seen_order_ids: set[str] = set()

        for order in self.pending_orders:
            if order.order_id in seen_order_ids:
                raise ForwardStateError(
                    f"Duplicate pending order {order.order_id}"
                )

            seen_order_ids.add(order.order_id)

            if order.intent_type == "SIM_END":
                raise ForwardStateError(
                    "SIM_END pending order is prohibited"
                )

        for position in self.account.positions.values():
            if not position.metadata.get("origin_branch"):
                raise ForwardStateError(
                    f"{position.symbol}: origin_branch missing"
                )

    def to_dict(self) -> dict[str, Any]:
        self.validate()

        return {
            "schema_version": self.schema_version,
            "engine_id": self.engine_id,
            "seed_date": self.seed_date,
            "first_forward_market_date": (
                self.first_forward_market_date
            ),
            "last_committed_date": self.last_committed_date,
            "account": account_to_dict(self.account),
            "pending_orders": [
                order.to_dict()
                for order in self.pending_orders
            ],
            "closed_trades": self.closed_trades,
            "equity_history": self.equity_history,
            "metadata": self.metadata,
        }

    @staticmethod
    def from_dict(
        value: Mapping[str, Any],
    ) -> "ForwardRuntimeState":
        state = ForwardRuntimeState(
            schema_version=str(
                value.get(
                    "schema_version",
                    RUNTIME_SCHEMA_VERSION,
                )
            ),
            engine_id=str(value["engine_id"]),
            seed_date=str(value["seed_date"]),
            first_forward_market_date=str(
                value["first_forward_market_date"]
            ),
            last_committed_date=value.get(
                "last_committed_date"
            ),
            account=account_from_dict(value["account"]),
            pending_orders=[
                PendingOrderRecord.from_dict(row)
                for row in value.get("pending_orders", [])
            ],
            closed_trades=[
                dict(row)
                for row in value.get("closed_trades", [])
            ],
            equity_history=[
                dict(row)
                for row in value.get("equity_history", [])
            ],
            metadata=dict(value.get("metadata") or {}),
        )

        state.validate()
        return state


class ForwardSeedLoader:
    def __init__(self, seed_root: Path | str) -> None:
        self.seed_root = Path(seed_root)

    def load(self) -> ForwardRuntimeState:
        state_path = (
            self.seed_root
            / "forward_runtime_seed_state.json"
        )

        contract_path = (
            self.seed_root
            / "forward_runtime_seed_contract.json"
        )

        if not state_path.is_file():
            raise ForwardContractError(
                f"Missing Forward Seed state: {state_path}"
            )

        if not contract_path.is_file():
            raise ForwardContractError(
                f"Missing Forward Seed contract: {contract_path}"
            )

        raw_state = load_json(state_path)
        raw_contract = load_json(contract_path)

        self._validate_boundary(
            raw_state=raw_state,
            raw_contract=raw_contract,
        )

        raw_account = raw_state.get("account")

        if not isinstance(raw_account, Mapping):
            raise ForwardContractError(
                "Forward Seed does not contain account"
            )

        account_payload = dict(raw_account)
        account_payload.setdefault(
            "date",
            SEED_DATE,
        )

        account = account_from_dict(account_payload)

        state = ForwardRuntimeState(
            schema_version=RUNTIME_SCHEMA_VERSION,
            engine_id=ENGINE_ID,
            seed_date=SEED_DATE,
            first_forward_market_date=(
                FIRST_FORWARD_MARKET_DATE
            ),
            last_committed_date=None,
            account=account,
            pending_orders=[],
            closed_trades=[],
            equity_history=[],
            metadata={
                "seed_source": str(state_path),
                "seed_state_sha256": sha256_file(state_path),
                "seed_contract_sha256": sha256_file(
                    contract_path
                ),
                "seed_semantics": (
                    "PRE_SIM_END_CONTINUOUS_ACCOUNT_STATE"
                ),
                "unknown_pending_resolution": (
                    "EXPIRED_UNPROVEN_AT_FORWARD_BOUNDARY"
                ),
                "sim_end_replayed": False,
            },
        )

        state.validate()
        return state

    @staticmethod
    def _validate_boundary(
        *,
        raw_state: Mapping[str, Any],
        raw_contract: Mapping[str, Any],
    ) -> None:
        serialized = json.dumps(
            {
                "state": raw_state,
                "contract": raw_contract,
            },
            ensure_ascii=False,
        ).upper()

        pending_resolution = raw_state.get(
            "pending_order_resolution",
            {},
        )

        if (
            pending_resolution.get(
                "actionable_pending_orders"
            )
            not in ([], None)
        ):
            raise ForwardContractError(
                "Forward Seed contains actionable "
                "historical pending orders"
            )

        resolution = pending_resolution.get(
            "resolution"
        )

        if (
            resolution is not None
            and resolution
            != "EXPIRED_UNPROVEN_AT_FORWARD_BOUNDARY"
        ):
            raise ForwardContractError(
                "Unexpected pending-order boundary resolution"
            )

        if (
            "POST_LIQUIDATION_ALL_CASH" in serialized
            or '"SIM_END_REPLAY_ALLOWED": TRUE'
            in serialized
        ):
            raise ForwardContractError(
                "Invalid post-liquidation or SIM_END seed"
            )


class ForwardDatePlanner:
    def __init__(
        self,
        trading_dates: Iterable[str],
    ) -> None:
        self.trading_dates = tuple(
            sorted(set(str(value) for value in trading_dates))
        )

    def plan(
        self,
        *,
        last_committed_date: str | None,
        latest_complete_common_data_date: str,
    ) -> list[str]:
        if (
            latest_complete_common_data_date
            < FIRST_FORWARD_MARKET_DATE
        ):
            return []

        start_exclusive = (
            last_committed_date
            if last_committed_date is not None
            else SEED_DATE
        )

        return [
            trading_date
            for trading_date in self.trading_dates
            if (
                trading_date > start_exclusive
                and trading_date
                >= FIRST_FORWARD_MARKET_DATE
                and trading_date
                <= latest_complete_common_data_date
            )
        ]


class ForwardMarketDataAdapter:
    """
    Data normalization only.

    This adapter does not make BUY/ADD/REDUCE/EXIT decisions
    and does not mutate AccountState.
    """

    def __init__(
        self,
        *,
        required_indices: Sequence[str] = (
            "SPX",
            "NDX",
            "SOX",
        ),
    ) -> None:
        self.required_indices = tuple(required_indices)

    @staticmethod
    def parse_price_file(
        path: Path | str,
    ) -> dict[str, DailyBar]:
        resolved = Path(path)
        raw = load_json(resolved)

        rows: Any

        if isinstance(raw, list):
            rows = raw

        elif isinstance(raw, Mapping):
            rows = None

            for key in (
                "bars",
                "data",
                "prices",
                "records",
                "rows",
                "history",
                "historical",
            ):
                if isinstance(raw.get(key), list):
                    rows = raw[key]
                    break

            if rows is None:
                dates = raw.get("dates")
                closes = raw.get("closes")

                if (
                    isinstance(dates, list)
                    and isinstance(closes, list)
                ):
                    rows = [
                        {
                            "date": trading_date,
                            "close": close,
                        }
                        for trading_date, close
                        in zip(dates, closes)
                    ]

            if rows is None:
                raise ForwardDataError(
                    f"Unsupported price schema: {resolved}"
                )

        else:
            raise ForwardDataError(
                f"Unsupported price file: {resolved}"
            )

        result: dict[str, DailyBar] = {}

        for row in rows:
            if not isinstance(row, Mapping):
                continue

            trading_date = (
                row.get("date")
                or row.get("Date")
                or row.get("timestamp")
            )

            close = (
                row.get("close")
                if row.get("close") is not None
                else row.get("Close")
            )

            if trading_date is None or close is None:
                continue

            normalized_date = str(trading_date)[:10]
            normalized_close = float(close)

            result[normalized_date] = DailyBar(
                date=normalized_date,
                open=ForwardMarketDataAdapter._optional_float(
                    row.get("open", row.get("Open"))
                ),
                high=ForwardMarketDataAdapter._optional_float(
                    row.get("high", row.get("High"))
                ),
                low=ForwardMarketDataAdapter._optional_float(
                    row.get("low", row.get("Low"))
                ),
                close=normalized_close,
                volume=ForwardMarketDataAdapter._optional_float(
                    row.get("volume", row.get("Volume"))
                ),
            )

        return dict(sorted(result.items()))

    @staticmethod
    def _optional_float(
        value: Any,
    ) -> float | None:
        if value is None:
            return None

        return float(value)

    def latest_complete_common_date(
        self,
        *,
        series_by_symbol: Mapping[
            str,
            Mapping[str, DailyBar],
        ],
        required_symbols: Iterable[str],
    ) -> str:
        required = set(self.required_indices)
        required.update(
            str(symbol)
            for symbol in required_symbols
        )

        if not required:
            raise ForwardDataError(
                "No required symbols were supplied"
            )

        missing_series = sorted(
            symbol
            for symbol in required
            if symbol not in series_by_symbol
        )

        if missing_series:
            raise ForwardDataError(
                "Missing required series: "
                + ", ".join(missing_series)
            )

        common_dates: set[str] | None = None

        for symbol in sorted(required):
            valid_dates = {
                trading_date
                for trading_date, bar
                in series_by_symbol[symbol].items()
                if (
                    bar is not None
                    and bar.close is not None
                    and bar.close > 0
                )
            }

            common_dates = (
                valid_dates
                if common_dates is None
                else common_dates & valid_dates
            )

        if not common_dates:
            raise ForwardDataError(
                "No complete common market date"
            )

        return max(common_dates)

    @staticmethod
    def bars_for_date(
        *,
        series_by_symbol: Mapping[
            str,
            Mapping[str, DailyBar],
        ],
        required_symbols: Iterable[str],
        trading_date: str,
    ) -> dict[str, DailyBar]:
        result: dict[str, DailyBar] = {}

        for symbol in sorted(set(required_symbols)):
            bar = series_by_symbol.get(
                symbol,
                {},
            ).get(trading_date)

            if (
                bar is None
                or bar.close is None
                or bar.close <= 0
            ):
                raise ForwardDataError(
                    f"{symbol}: missing complete bar "
                    f"for {trading_date}"
                )

            result[symbol] = bar

        return result


@dataclass(frozen=True)
class SidewaysDecisionContext:
    stocks: Mapping[str, Any]
    spx: Any
    management_actions: Mapping[str, str]


@dataclass
class CanonicalDecisionResult:
    order_intents: list[OrderIntent]
    decision_trace: DecisionTrace | dict[str, Any]
    metadata: dict[str, Any]


class CanonicalDailyDecisionRouter:
    def __init__(
        self,
        *,
        engine: E1RCoreEngine | None = None,
        sideways_ranker: Any | None = None,
        sideways_policy: Any | None = None,
        entry_atr20_provider: (
            Callable[[str, str], float | None] | None
        ) = None,
    ) -> None:
        self.engine = engine or E1RCoreEngine()
        self.sideways_ranker = sideways_ranker
        self.sideways_policy = sideways_policy
        self.entry_atr20_provider = entry_atr20_provider

    def decide(
        self,
        *,
        snapshot: MarketSnapshot,
        account: AccountState,
        uptrend_inputs: Any | None = None,
        sideways_context: SidewaysDecisionContext
        | None = None,
    ) -> CanonicalDecisionResult:
        route = self.engine.router.route(
            date=snapshot.date,
            spx_regime=(
                None
                if snapshot.regime is None
                else snapshot.regime.spx_regime
            ),
            subclass=(
                None
                if snapshot.regime is None
                else snapshot.regime.subclass
            ),
        )

        if route.branch == "UPTREND":
            if uptrend_inputs is None:
                raise ForwardContractError(
                    "UPTREND requires frozen uptrend_inputs"
                )

            result = self.engine.step(
                snapshot,
                account,
                uptrend_inputs=uptrend_inputs,
                entry_atr20_provider=(
                    self.entry_atr20_provider
                ),
            )

            return CanonicalDecisionResult(
                order_intents=list(
                    result.order_intents
                ),
                decision_trace=result.decision_trace,
                metadata={
                    "decision_source": (
                        "E1RCoreEngine.step"
                    ),
                    "branch": route.branch,
                    "strategy_logic_reimplemented": False,
                },
            )

        is_sideways_ma_conflict = (
            snapshot.regime is not None
            and snapshot.regime.spx_regime == "SIDEWAYS"
            and snapshot.regime.subclass == "MA_CONFLICT"
        )

        if is_sideways_ma_conflict:
            if sideways_context is None:
                raise ForwardContractError(
                    "SIDEWAYS/MA_CONFLICT requires "
                    "SidewaysDecisionContext"
                )

            ranker, policy = self._resolve_sideways_components()

            ranked = ranker.rank_date(
                stocks=sideways_context.stocks,
                spx=sideways_context.spx,
                date=snapshot.date,
                regime="SIDEWAYS",
                subclass="MA_CONFLICT",
            )

            intents = policy.build_intents(
                date=snapshot.date,
                regime="SIDEWAYS",
                subclass="MA_CONFLICT",
                ranked_candidates=ranked,
                account=account,
                management_actions=dict(
                    sideways_context.management_actions
                ),
            )

            trace = {
                    "date": snapshot.date,
                    "branch": "SIDEWAYS_MA_CONFLICT",
                    "ranked_candidate_count": len(ranked),
                    "order_intent_count": len(intents),
                    "decision_source": (
                        "SidewaysCore.rank_date"
                        "->"
                        "SidewaysExecutionPolicy.build_intents"
                    ),
                }
            finalized, stop_rows = self._finalize_runtime_orders(
                date=snapshot.date,
                branch="SIDEWAYS_MA_CONFLICT",
                account=account,
                orders=list(intents),
            )
            trace["capped_atr_stop"] = {
                "variant_id": VARIANT_ID,
                "triggered": stop_rows,
            }
            return CanonicalDecisionResult(
                order_intents=finalized,
                decision_trace=trace,
                metadata={
                    "decision_source": (
                        "SidewaysCore.rank_date"
                        "->"
                        "SidewaysExecutionPolicy.build_intents"
                    ),
                    "branch": "SIDEWAYS_MA_CONFLICT",
                    "strategy_logic_reimplemented": False,
                },
            )

        orders = self._hold_or_noop(
            snapshot=snapshot,
            account=account,
            branch=route.branch,
        )
        orders, stop_rows = self._finalize_runtime_orders(
            date=snapshot.date,
            branch=route.branch,
            account=account,
            orders=orders,
        )

        return CanonicalDecisionResult(
            order_intents=orders,
            decision_trace={
                "date": snapshot.date,
                "branch": route.branch,
                "decision_source": (
                    "SharedRuntime management-only boundary"
                ),
                "new_risk_expansion": False,
                "capped_atr_stop": {
                    "variant_id": VARIANT_ID,
                    "triggered": stop_rows,
                },
            },
            metadata={
                "decision_source": (
                    "SharedRuntime management-only boundary"
                ),
                "branch": route.branch,
                "new_risk_expansion": False,
            },
        )

    def _finalize_runtime_orders(
        self,
        *,
        date: str,
        branch: str,
        account: AccountState,
        orders: Sequence[OrderIntent],
    ) -> tuple[list[OrderIntent], list[dict[str, Any]]]:
        """Use the canonical Engine policy for non-UPTREND runtime routes."""
        strict = account.metadata.get("strategy_variant") == VARIANT_ID
        finalized: list[OrderIntent] = []
        for order in orders:
            if order.intent_type != "BUY" or not strict:
                finalized.append(order)
                continue
            if self.entry_atr20_provider is None:
                raise ForwardContractError(
                    "CAPPED-ATR BUY requires entry_atr20_provider"
                )
            atr20 = self.entry_atr20_provider(order.symbol, order.date)
            if atr20 is None:
                raise ForwardContractError(
                    "missing 20-observation entry ATR for "
                    + order.symbol
                    + " on "
                    + order.date
                )
            finalized.append(
                annotate_buy_intent(
                    order,
                    atr20=float(atr20),
                    atr_as_of=order.date,
                )
            )
        return CappedAtrStopPolicy.apply_engine_orders(
            date=date,
            branch=branch,
            account=account,
            orders=finalized,
            strict=strict,
        )

    def _resolve_sideways_components(
        self,
    ) -> tuple[Any, Any]:
        if (
            self.sideways_ranker is not None
            and self.sideways_policy is not None
        ):
            return (
                self.sideways_ranker,
                self.sideways_policy,
            )

        from e1r_engine.sideways_core import SidewaysCore
        from e1r_engine.sideways_execution import (
            SidewaysExecutionPolicy,
        )

        return (
            SidewaysCore(),
            SidewaysExecutionPolicy(),
        )

    @staticmethod
    def _hold_or_noop(
        *,
        snapshot: MarketSnapshot,
        account: AccountState,
        branch: str,
    ) -> list[OrderIntent]:
        if not account.positions:
            return [
                OrderIntent(
                    date=snapshot.date,
                    symbol="",
                    intent_type="NOOP",
                    side=None,
                    target_quantity=None,
                    quantity_delta=None,
                    reason=(
                        "forward_runtime_no_new_risk_expansion"
                    ),
                    branch=branch,
                    metadata={
                        "new_risk_expansion": False,
                    },
                )
            ]

        return [
            OrderIntent(
                date=snapshot.date,
                symbol=symbol,
                intent_type="HOLD",
                side=None,
                target_quantity=position.quantity,
                quantity_delta=0.0,
                reason=(
                    "forward_runtime_existing_position_hold"
                ),
                branch=branch,
                metadata={
                    "origin_branch": (
                        position.metadata.get(
                            "origin_branch"
                        )
                    ),
                    "new_risk_expansion": False,
                },
            )
            for symbol, position
            in sorted(account.positions.items())
        ]


class PendingOrderLedger:
    @staticmethod
    def create(
        intents: Iterable[OrderIntent],
    ) -> list[PendingOrderRecord]:
        executable = [
            intent
            for intent in intents
            if intent.intent_type
            in EXECUTABLE_INTENT_TYPES
        ]

        executable.sort(
            key=lambda intent: (
                EXECUTION_PRIORITY.get(
                    intent.intent_type,
                    999,
                ),
                intent.symbol,
                intent.reason,
            )
        )

        orders = [
            PendingOrderRecord.from_intent(
                intent,
                sequence=index,
            )
            for index, intent
            in enumerate(executable, start=1)
        ]

        ids = [order.order_id for order in orders]

        if len(ids) != len(set(ids)):
            raise ForwardContractError(
                "PendingOrderLedger produced "
                "duplicate order identities"
            )

        return orders


@dataclass
class ExecutionResult:
    account_after: AccountState
    fills: list[Fill]
    resolved_orders: list[dict[str, Any]]
    closed_trades: list[dict[str, Any]]
    skipped_orders: list[dict[str, Any]]


class T1ExecutionEngine:
    def __init__(
        self,
        *,
        one_way_cost: float = 0.001,
        max_positions: int = 3,
    ) -> None:
        self.one_way_cost = float(one_way_cost)
        self.max_positions = int(max_positions)

    def execute(
        self,
        *,
        execution_date: str,
        account: AccountState,
        pending_orders: Sequence[PendingOrderRecord],
        bars_by_symbol: Mapping[str, DailyBar],
    ) -> ExecutionResult:
        cash = float(account.cash)
        positions = dict(account.positions)

        fills: list[Fill] = []
        resolved: list[dict[str, Any]] = []
        closed_trades: list[dict[str, Any]] = []
        skipped: list[dict[str, Any]] = []

        seen_fill_ids: set[str] = set()

        ordered = sorted(
            pending_orders,
            key=lambda order: (
                EXECUTION_PRIORITY.get(
                    order.intent_type,
                    999,
                ),
                order.sequence,
                order.symbol,
            ),
        )

        tradable_cash_base: float | None = None
        sideways_budget_spent = 0.0

        for order in ordered:
            if order.status != "PENDING":
                continue

            if order.intent_type == "SIM_END":
                raise ForwardContractError(
                    "SIM_END is prohibited in Forward Runtime"
                )

            fill_id = deterministic_id(
                ENGINE_ID,
                order.order_id,
                execution_date,
                order.intent_type,
            )

            if fill_id in seen_fill_ids:
                raise ForwardContractError(
                    f"Duplicate fill identity {fill_id}"
                )

            seen_fill_ids.add(fill_id)

            bar = bars_by_symbol.get(order.symbol)

            if bar is None:
                skipped.append(
                    self._skip(
                        order=order,
                        execution_date=execution_date,
                        reason="MISSING_T1_BAR",
                    )
                )
                continue

            if order.intent_type in {"BUY", "ADD"}:
                raw_price = (
                    bar.high
                    if bar.high is not None
                    and bar.high > 0
                    else bar.close
                )
                price = float(raw_price) * (
                    1.0 + self.one_way_cost
                )
                side = "BUY"

            else:
                raw_price = (
                    bar.low
                    if bar.low is not None
                    and bar.low > 0
                    else bar.close
                )
                price = float(raw_price) * (
                    1.0 - self.one_way_cost
                )
                side = "SELL"

            if price <= 0:
                skipped.append(
                    self._skip(
                        order=order,
                        execution_date=execution_date,
                        reason="INVALID_EXECUTION_PRICE",
                    )
                )
                continue

            if order.intent_type == "BUY":
                if order.symbol in positions:
                    skipped.append(
                        self._skip(
                            order=order,
                            execution_date=execution_date,
                            reason="ALREADY_HOLDING",
                        )
                    )
                    continue

                if len(positions) >= self.max_positions:
                    skipped.append(
                        self._skip(
                            order=order,
                            execution_date=execution_date,
                            reason="MAX_POSITIONS_REACHED",
                        )
                    )
                    continue

                if tradable_cash_base is None:
                    tradable_cash_base = max(0.0, cash)

                target_cash = self._target_buy_cash(
                    order=order,
                    account_cash=cash,
                    account_total_equity=(
                        cash
                        + sum(
                            position.market_value
                            for position
                            in positions.values()
                        )
                    ),
                    tradable_cash_base=tradable_cash_base,
                    sideways_budget_spent=(
                        sideways_budget_spent
                    ),
                )

                target_cash = min(
                    target_cash,
                    max(0.0, cash),
                )

                if target_cash <= 0:
                    skipped.append(
                        self._skip(
                            order=order,
                            execution_date=execution_date,
                            reason="CASH_INSUFFICIENT",
                        )
                    )
                    continue

                quantity = target_cash / price
                gross_amount = quantity * price
                cash -= gross_amount

                metadata = dict(order.metadata)
                metadata.setdefault(
                    "origin_branch",
                    (
                        "SIDEWAYS_MA_CONFLICT"
                        if order.branch
                        == "SIDEWAYS_MA_CONFLICT"
                        else "UPTREND"
                    ),
                )
                metadata.setdefault(
                    "size_units",
                    float(
                        order.metadata.get(
                            "target_size_units",
                            1.0,
                        )
                    ),
                )
                metadata["remaining_cost_basis"] = (
                    gross_amount
                )
                metadata["entry_shares"] = quantity
                metadata["entry_execution_price"] = price
                metadata["order_id"] = order.order_id
                metadata["fill_id"] = fill_id

                if account.metadata.get("strategy_variant") == VARIANT_ID:
                    entry_metadata = metadata.get(ENTRY_METADATA_KEY)
                    if not isinstance(entry_metadata, Mapping):
                        raise ForwardContractError(
                            "CAPPED-ATR BUY fill is missing frozen entry metadata"
                        )
                    metadata[POSITION_METADATA_KEY] = build_frozen_state(
                        adjusted_first_buy_price=price,
                        entry_metadata=entry_metadata,
                    ).to_dict()

                positions[order.symbol] = PositionState(
                    symbol=order.symbol,
                    quantity=quantity,
                    avg_cost=price,
                    last_price=price,
                    market_value=gross_amount,
                    unrealized_pnl=0.0,
                    entry_date=execution_date,
                    last_update_date=execution_date,
                    metadata=metadata,
                )

                if (
                    metadata.get("origin_branch")
                    == "SIDEWAYS_MA_CONFLICT"
                ):
                    sideways_budget_spent += gross_amount

                fill = self._make_fill(
                    fill_id=fill_id,
                    order=order,
                    execution_date=execution_date,
                    side=side,
                    quantity=quantity,
                    price=price,
                    reason="T1_BUY_EXECUTED",
                )

                fills.append(fill)
                resolved.append(
                    self._resolved(
                        order=order,
                        execution_date=execution_date,
                        fill_id=fill_id,
                        status="FILLED",
                    )
                )

            elif order.intent_type == "ADD":
                position = positions.get(order.symbol)

                if position is None:
                    skipped.append(
                        self._skip(
                            order=order,
                            execution_date=execution_date,
                            reason="NOT_HOLDING",
                        )
                    )
                    continue

                quantity = self._quantity_for_add(
                    order=order,
                    position=position,
                    cash=cash,
                    price=price,
                )

                if quantity <= 0:
                    skipped.append(
                        self._skip(
                            order=order,
                            execution_date=execution_date,
                            reason="ADD_SIZE_ZERO",
                        )
                    )
                    continue

                gross_amount = min(
                    cash,
                    quantity * price,
                )

                quantity = gross_amount / price

                if quantity <= 0:
                    skipped.append(
                        self._skip(
                            order=order,
                            execution_date=execution_date,
                            reason="CASH_INSUFFICIENT",
                        )
                    )
                    continue

                new_quantity = (
                    position.quantity + quantity
                )
                new_avg_cost = (
                    (
                        position.quantity
                        * position.avg_cost
                    )
                    + gross_amount
                ) / new_quantity

                cash -= gross_amount

                metadata = dict(position.metadata)
                metadata["size_units"] = min(
                    1.5,
                    float(
                        metadata.get("size_units", 1.0)
                    )
                    + float(
                        order.metadata.get(
                            "add_size_units",
                            0.5,
                        )
                    ),
                )
                metadata["remaining_cost_basis"] = (
                    new_quantity * new_avg_cost
                )
                metadata["last_order_id"] = order.order_id
                metadata["last_fill_id"] = fill_id

                positions[order.symbol] = PositionState(
                    symbol=order.symbol,
                    quantity=new_quantity,
                    avg_cost=new_avg_cost,
                    last_price=price,
                    market_value=new_quantity * price,
                    unrealized_pnl=(
                        price - new_avg_cost
                    ) * new_quantity,
                    entry_date=position.entry_date,
                    last_update_date=execution_date,
                    metadata=metadata,
                )

                fills.append(
                    self._make_fill(
                        fill_id=fill_id,
                        order=order,
                        execution_date=execution_date,
                        side=side,
                        quantity=quantity,
                        price=price,
                        reason="T1_ADD_EXECUTED",
                    )
                )
                resolved.append(
                    self._resolved(
                        order=order,
                        execution_date=execution_date,
                        fill_id=fill_id,
                        status="FILLED",
                    )
                )

            elif order.intent_type in {
                "REDUCE",
                "EXIT",
            }:
                position = positions.get(order.symbol)

                if position is None:
                    skipped.append(
                        self._skip(
                            order=order,
                            execution_date=execution_date,
                            reason="NOT_HOLDING",
                        )
                    )
                    continue

                if order.intent_type == "EXIT":
                    quantity = position.quantity
                else:
                    quantity = self._quantity_for_reduce(
                        order=order,
                        position=position,
                    )

                quantity = min(
                    max(0.0, quantity),
                    position.quantity,
                )

                if quantity <= 0:
                    skipped.append(
                        self._skip(
                            order=order,
                            execution_date=execution_date,
                            reason="SELL_SIZE_ZERO",
                        )
                    )
                    continue

                gross_amount = quantity * price
                cash += gross_amount

                realized_pnl = (
                    price - position.avg_cost
                ) * quantity

                remaining_quantity = (
                    position.quantity - quantity
                )

                if (
                    order.intent_type == "EXIT"
                    or remaining_quantity <= 1e-12
                ):
                    closed_trades.append(
                        {
                            "symbol": order.symbol,
                            "entry_date": (
                                position.entry_date
                            ),
                            "exit_date": execution_date,
                            "quantity": quantity,
                            "average_cost": (
                                position.avg_cost
                            ),
                            "execution_price": price,
                            "realized_pnl": realized_pnl,
                            "origin_branch": (
                                position.metadata.get(
                                    "origin_branch"
                                )
                            ),
                            "exit_reason": order.reason,
                            "order_id": order.order_id,
                            "fill_id": fill_id,
                            "is_sim_end": False,
                        }
                    )

                    positions.pop(order.symbol, None)

                else:
                    metadata = dict(position.metadata)
                    previous_realized = float(
                        metadata.get(
                            "realized_pnl",
                            0.0,
                        )
                    )
                    previous_realized_basis = float(
                        metadata.get(
                            "realized_cost_basis",
                            0.0,
                        )
                    )

                    metadata["realized_pnl"] = (
                        previous_realized
                        + realized_pnl
                    )
                    metadata["realized_cost_basis"] = (
                        previous_realized_basis
                        + quantity * position.avg_cost
                    )
                    metadata["remaining_cost_basis"] = (
                        remaining_quantity
                        * position.avg_cost
                    )
                    metadata["size_units"] = max(
                        0.5,
                        float(
                            metadata.get(
                                "size_units",
                                1.0,
                            )
                        )
                        - float(
                            order.metadata.get(
                                "reduce_size_units",
                                0.5,
                            )
                        ),
                    )
                    metadata["last_order_id"] = (
                        order.order_id
                    )
                    metadata["last_fill_id"] = fill_id

                    positions[order.symbol] = PositionState(
                        symbol=order.symbol,
                        quantity=remaining_quantity,
                        avg_cost=position.avg_cost,
                        last_price=price,
                        market_value=(
                            remaining_quantity * price
                        ),
                        unrealized_pnl=(
                            price - position.avg_cost
                        ) * remaining_quantity,
                        entry_date=position.entry_date,
                        last_update_date=execution_date,
                        metadata=metadata,
                    )

                fills.append(
                    self._make_fill(
                        fill_id=fill_id,
                        order=order,
                        execution_date=execution_date,
                        side=side,
                        quantity=quantity,
                        price=price,
                        reason=(
                            "T1_EXIT_EXECUTED"
                            if order.intent_type == "EXIT"
                            else "T1_REDUCE_EXECUTED"
                        ),
                    )
                )
                resolved.append(
                    self._resolved(
                        order=order,
                        execution_date=execution_date,
                        fill_id=fill_id,
                        status="FILLED",
                    )
                )

            else:
                raise ForwardContractError(
                    "Unsupported pending intent_type="
                    f"{order.intent_type!r}"
                )

        marked_positions = {
            symbol: position.mark_to_market(
                price=(
                    bars_by_symbol[symbol].close
                    if symbol in bars_by_symbol
                    else position.last_price
                ),
                date=execution_date,
            )
            for symbol, position
            in positions.items()
        }

        positions_value = sum(
            position.market_value
            for position in marked_positions.values()
        )

        account_after = AccountState(
            date=execution_date,
            cash=float(cash),
            positions=marked_positions,
            total_equity=float(
                cash + positions_value
            ),
            positions_value=float(positions_value),
            open_positions_count=len(marked_positions),
            metadata={
                **dict(account.metadata),
                "last_execution_date": execution_date,
                "sim_end_performed": False,
            },
        )

        validation = account_after.validate(
            max_positions=self.max_positions
        )

        if not validation["ok"]:
            raise ForwardStateError(
                "T1 execution produced invalid account: "
                + "; ".join(validation["errors"])
            )

        return ExecutionResult(
            account_after=account_after,
            fills=fills,
            resolved_orders=resolved,
            closed_trades=closed_trades,
            skipped_orders=skipped,
        )

    def _target_buy_cash(
        self,
        *,
        order: PendingOrderRecord,
        account_cash: float,
        account_total_equity: float,
        tradable_cash_base: float,
        sideways_budget_spent: float,
    ) -> float:
        origin = (
            order.metadata.get("origin_branch")
            or order.branch
        )

        if origin == "SIDEWAYS_MA_CONFLICT":
            per_fraction = float(
                order.metadata.get(
                    "target_fraction_of_tradable_cash",
                    0.10,
                )
            )
            total_fraction = float(
                order.metadata.get(
                    "capital_fraction_of_tradable_cash",
                    0.30,
                )
            )

            remaining_budget = max(
                0.0,
                (
                    tradable_cash_base
                    * total_fraction
                )
                - sideways_budget_spent,
            )

            return min(
                tradable_cash_base * per_fraction,
                remaining_budget,
                account_cash,
            )

        if order.target_quantity is not None:
            return max(
                0.0,
                order.target_quantity
                * float(
                    order.metadata.get(
                        "reference_price",
                        0.0,
                    )
                ),
            )

        target_fraction = float(
            order.metadata.get(
                "target_fraction_of_equity",
                1.0 / 3.0,
            )
        )

        target_size_units = float(
            order.metadata.get(
                "target_size_units",
                1.0,
            )
        )

        target_size_units = max(
            0.0,
            min(target_size_units, 1.0),
        )

        return min(
            account_cash,
            account_total_equity
            * target_fraction
            * target_size_units,
        )

    @staticmethod
    def _quantity_for_add(
        *,
        order: PendingOrderRecord,
        position: PositionState,
        cash: float,
        price: float,
    ) -> float:
        if order.target_quantity is not None:
            return max(
                0.0,
                order.target_quantity
                - position.quantity,
            )

        if order.quantity_delta is not None:
            return max(
                0.0,
                order.quantity_delta,
            )

        target_cash = min(
            cash,
            float(
                order.metadata.get(
                    "target_add_cash",
                    cash / 3.0,
                )
            ),
        )

        return (
            target_cash / price
            if price > 0
            else 0.0
        )

    @staticmethod
    def _quantity_for_reduce(
        *,
        order: PendingOrderRecord,
        position: PositionState,
    ) -> float:
        if order.target_quantity is not None:
            return max(
                0.0,
                position.quantity
                - order.target_quantity,
            )

        if order.quantity_delta is not None:
            return abs(order.quantity_delta)

        fraction = float(
            order.metadata.get(
                "sell_fraction",
                0.50,
            )
        )

        return position.quantity * fraction

    @staticmethod
    def _make_fill(
        *,
        fill_id: str,
        order: PendingOrderRecord,
        execution_date: str,
        side: str,
        quantity: float,
        price: float,
        reason: str,
    ) -> Fill:
        return Fill(
            date=execution_date,
            symbol=order.symbol,
            side=side,
            quantity=float(quantity),
            price=float(price),
            gross_amount=float(quantity) * float(price),
            status="FILLED",
            reason=reason,
            metadata={
                "engine_id": ENGINE_ID,
                "fill_id": fill_id,
                "order_id": order.order_id,
                "signal_date": order.signal_date,
                "intent_type": order.intent_type,
                "branch": order.branch,
                "sim_end": False,
            },
        )

    @staticmethod
    def _resolved(
        *,
        order: PendingOrderRecord,
        execution_date: str,
        fill_id: str,
        status: str,
    ) -> dict[str, Any]:
        return {
            **order.to_dict(),
            "status": status,
            "execution_date": execution_date,
            "fill_id": fill_id,
        }

    @staticmethod
    def _skip(
        *,
        order: PendingOrderRecord,
        execution_date: str,
        reason: str,
    ) -> dict[str, Any]:
        return {
            **order.to_dict(),
            "status": "SKIPPED",
            "execution_date": execution_date,
            "skip_reason": reason,
        }


class ForwardAccountRepository:
    def __init__(
        self,
        runtime_root: Path | str,
    ) -> None:
        self.runtime_root = Path(runtime_root)
        self.current_root = (
            self.runtime_root / "current"
        )
        self.state_path = (
            self.current_root / "runtime_state.json"
        )

    def exists(self) -> bool:
        return self.state_path.is_file()

    def initialize(
        self,
        state: ForwardRuntimeState,
    ) -> None:
        if self.exists():
            raise ForwardStateError(
                "Forward Runtime is already initialized"
            )

        state.validate()
        atomic_write_json(
            self.state_path,
            state.to_dict(),
        )

    def load(self) -> ForwardRuntimeState:
        if not self.state_path.is_file():
            raise ForwardStateError(
                "Forward Runtime state does not exist"
            )

        return ForwardRuntimeState.from_dict(
            load_json(self.state_path)
        )

    def save(
        self,
        state: ForwardRuntimeState,
    ) -> None:
        state.validate()
        atomic_write_json(
            self.state_path,
            state.to_dict(),
        )


class OfficialForwardArtifactWriter:
    def __init__(
        self,
        runtime_root: Path | str,
    ) -> None:
        self.runtime_root = Path(runtime_root)
        self.current_root = (
            self.runtime_root / "current"
        )
        self.daily_root = (
            self.runtime_root / "daily"
        )
        self.history_root = (
            self.runtime_root / "history"
        )

    def write_daily(
        self,
        *,
        trading_date: str,
        state: ForwardRuntimeState,
        order_intents: Sequence[OrderIntent],
        fills: Sequence[Fill],
        decision_trace: Any,
        execution_result: ExecutionResult,
        source_hashes: Mapping[str, str],
        runtime_commit: str,
    ) -> dict[str, Any]:
        target_directory = (
            self.daily_root / trading_date
        )

        if target_directory.exists():
            raise ForwardStateError(
                f"{trading_date} already has a "
                "daily artifact directory"
            )

        staging_directory = (
            self.daily_root
            / f".{trading_date}.staging"
        )

        if staging_directory.exists():
            shutil.rmtree(staging_directory)

        staging_directory.mkdir(
            parents=True,
            exist_ok=False,
        )

        payloads = {
            "account_state.json": (
                account_to_dict(state.account)
            ),
            "order_intents.json": [
                order_intent_to_dict(intent)
                for intent in order_intents
            ],
            "fills.json": [
                fill_to_dict(fill)
                for fill in fills
            ],
            "decision_trace.json": (
                self._serialize_trace(decision_trace)
            ),
            "equity.json": {
                "date": trading_date,
                "cash": state.account.cash,
                "positions_value": (
                    state.account.positions_value
                ),
                "total_equity": (
                    state.account.total_equity
                ),
                "open_positions_count": (
                    state.account.open_positions_count
                ),
                "event": "EOD_MARK_TO_MARKET",
            },
            "execution.json": {
                "resolved_orders": (
                    execution_result.resolved_orders
                ),
                "skipped_orders": (
                    execution_result.skipped_orders
                ),
                "closed_trades": (
                    execution_result.closed_trades
                ),
                "sim_end_performed": False,
            },
        }

        for filename, payload in payloads.items():
            atomic_write_json(
                staging_directory / filename,
                payload,
            )

        artifacts = {
            filename: {
                "sha256": sha256_file(
                    staging_directory / filename
                )
            }
            for filename in payloads
        }

        manifest = {
            "schema_version": RUNTIME_SCHEMA_VERSION,
            "engine_id": ENGINE_ID,
            "artifact_type": (
                "OFFICIAL_FORWARD_DAILY_COMMIT"
            ),
            "date": trading_date,
            "last_committed_date": trading_date,
            "forward_track_end": "OPEN_ENDED",
            "sim_end_performed": False,
            "runtime_commit": runtime_commit,
            "source_hashes": dict(source_hashes),
            "account_summary": {
                "cash": state.account.cash,
                "positions_value": (
                    state.account.positions_value
                ),
                "total_equity": (
                    state.account.total_equity
                ),
                "open_positions_count": (
                    state.account.open_positions_count
                ),
            },
            "artifacts": artifacts,
        }

        atomic_write_json(
            staging_directory / "manifest.json",
            manifest,
        )

        os.replace(
            staging_directory,
            target_directory,
        )

        return manifest

    def update_current(
        self,
        *,
        state: ForwardRuntimeState,
        daily_manifest: Mapping[str, Any],
    ) -> None:
        self.current_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        atomic_write_json(
            self.current_root / "account_state.json",
            account_to_dict(state.account),
        )

        atomic_write_json(
            self.current_root / "pending_orders.json",
            [
                order.to_dict()
                for order in state.pending_orders
            ],
        )

        current_manifest = {
            **dict(daily_manifest),
            "artifact_type": (
                "OFFICIAL_FORWARD_CURRENT"
            ),
            "current_account_state_sha256": (
                sha256_file(
                    self.current_root
                    / "account_state.json"
                )
            ),
            "current_pending_orders_sha256": (
                sha256_file(
                    self.current_root
                    / "pending_orders.json"
                )
            ),
        }

        atomic_write_json(
            self.current_root / "manifest.json",
            current_manifest,
        )

    def append_history(
        self,
        *,
        trading_date: str,
        state: ForwardRuntimeState,
        order_intents: Sequence[OrderIntent],
        fills: Sequence[Fill],
    ) -> None:
        self.history_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._append_jsonl_unique(
            self.history_root / "orders.jsonl",
            [
                {
                    "record_id": deterministic_id(
                        ENGINE_ID,
                        "ORDER",
                        trading_date,
                        index,
                        intent.symbol,
                        intent.intent_type,
                    ),
                    **order_intent_to_dict(intent),
                }
                for index, intent
                in enumerate(order_intents, start=1)
            ],
        )

        self._append_jsonl_unique(
            self.history_root / "fills.jsonl",
            [
                {
                    "record_id": fill.metadata["fill_id"],
                    **fill_to_dict(fill),
                }
                for fill in fills
            ],
        )

        equity_path = (
            self.history_root / "equity_curve.json"
        )

        history = (
            load_json(equity_path)
            if equity_path.is_file()
            else []
        )

        history_by_date = {
            row["date"]: row
            for row in history
        }

        history_by_date[trading_date] = {
            "date": trading_date,
            "cash": state.account.cash,
            "positions_value": (
                state.account.positions_value
            ),
            "total_equity": (
                state.account.total_equity
            ),
            "open_positions_count": (
                state.account.open_positions_count
            ),
        }

        atomic_write_json(
            equity_path,
            [
                history_by_date[key]
                for key in sorted(history_by_date)
            ],
        )

    @staticmethod
    def _append_jsonl_unique(
        path: Path,
        rows: Sequence[Mapping[str, Any]],
    ) -> None:
        if not rows:
            return

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        existing_ids: set[str] = set()

        if path.is_file():
            for line in path.read_text(
                encoding="utf-8"
            ).splitlines():
                if not line.strip():
                    continue

                existing_ids.add(
                    json.loads(line)["record_id"]
                )

        new_rows = [
            dict(row)
            for row in rows
            if row["record_id"] not in existing_ids
        ]

        if not new_rows:
            return

        with path.open(
            "a",
            encoding="utf-8",
        ) as stream:
            for row in new_rows:
                stream.write(
                    json.dumps(
                        row,
                        ensure_ascii=False,
                        sort_keys=True,
                    )
                    + "\n"
                )

            stream.flush()
            os.fsync(stream.fileno())

    @staticmethod
    def _serialize_trace(
        trace: Any,
    ) -> Any:
        if is_dataclass(trace):
            return asdict(trace)

        if isinstance(trace, Mapping):
            return dict(trace)

        if hasattr(trace, "__dict__"):
            return dict(trace.__dict__)

        return trace


@dataclass
class DailyCommitResult:
    status: str
    trading_date: str
    account: AccountState
    order_intents: list[OrderIntent]
    fills: list[Fill]
    pending_orders: list[PendingOrderRecord]
    manifest: dict[str, Any]


class ForwardDailyCommitter:
    def __init__(
        self,
        *,
        repository: ForwardAccountRepository,
        artifact_writer: OfficialForwardArtifactWriter,
        decision_router: CanonicalDailyDecisionRouter,
        execution_engine: T1ExecutionEngine,
        runtime_commit_provider: Callable[[], str],
    ) -> None:
        self.repository = repository
        self.artifact_writer = artifact_writer
        self.decision_router = decision_router
        self.execution_engine = execution_engine
        self.runtime_commit_provider = (
            runtime_commit_provider
        )

    def commit_day(
        self,
        *,
        trading_date: str,
        snapshot: MarketSnapshot,
        t1_bars_by_symbol: Mapping[str, DailyBar],
        uptrend_inputs: Any | None = None,
        sideways_context: SidewaysDecisionContext
        | None = None,
        source_hashes: Mapping[str, str] | None = None,
    ) -> DailyCommitResult:
        state = self.repository.load()
        state.validate()

        if (
            state.last_committed_date is not None
            and trading_date <= state.last_committed_date
        ):
            return DailyCommitResult(
                status="NO_OP_ALREADY_COMMITTED",
                trading_date=trading_date,
                account=state.account,
                order_intents=[],
                fills=[],
                pending_orders=state.pending_orders,
                manifest={},
            )

        if snapshot.date != trading_date:
            raise ForwardContractError(
                "MarketSnapshot date does not match "
                "planned trading date"
            )

        execution_result = (
            self.execution_engine.execute(
                execution_date=trading_date,
                account=state.account,
                pending_orders=state.pending_orders,
                bars_by_symbol=t1_bars_by_symbol,
            )
        )

        account_after_execution = (
            execution_result.account_after
        )

        close_prices = {
            symbol: bar.close
            for symbol, bar
            in snapshot.prices_by_symbol.items()
            if (
                bar is not None
                and bar.close is not None
            )
        }

        account_at_close = (
            account_after_execution.mark_to_market(
                prices=close_prices,
                date=trading_date,
            )
        )

        for symbol in account_at_close.positions:
            if symbol not in close_prices:
                raise ForwardDataError(
                    f"{symbol}: missing T close price"
                )

        decision = self.decision_router.decide(
            snapshot=snapshot,
            account=account_at_close,
            uptrend_inputs=uptrend_inputs,
            sideways_context=sideways_context,
        )

        new_pending = PendingOrderLedger.create(
            decision.order_intents
        )

        closed_trades = (
            list(state.closed_trades)
            + execution_result.closed_trades
        )

        equity_history = list(
            state.equity_history
        )

        equity_history.append(
            {
                "date": trading_date,
                "cash": account_at_close.cash,
                "positions_value": (
                    account_at_close.positions_value
                ),
                "total_equity": (
                    account_at_close.total_equity
                ),
                "open_positions_count": (
                    account_at_close.open_positions_count
                ),
            }
        )

        new_state = ForwardRuntimeState(
            schema_version=RUNTIME_SCHEMA_VERSION,
            engine_id=ENGINE_ID,
            seed_date=state.seed_date,
            first_forward_market_date=(
                state.first_forward_market_date
            ),
            last_committed_date=trading_date,
            account=account_at_close,
            pending_orders=new_pending,
            closed_trades=closed_trades,
            equity_history=equity_history,
            metadata={
                **dict(state.metadata),
                "last_decision_source": (
                    decision.metadata.get(
                        "decision_source"
                    )
                ),
                "last_commit_date": trading_date,
                "sim_end_performed": False,
            },
        )

        new_state.validate()

        runtime_commit = (
            self.runtime_commit_provider()
        )

        daily_manifest = (
            self.artifact_writer.write_daily(
                trading_date=trading_date,
                state=new_state,
                order_intents=(
                    decision.order_intents
                ),
                fills=execution_result.fills,
                decision_trace=(
                    decision.decision_trace
                ),
                execution_result=execution_result,
                source_hashes=(
                    source_hashes or {}
                ),
                runtime_commit=runtime_commit,
            )
        )

        self.repository.save(new_state)

        self.artifact_writer.update_current(
            state=new_state,
            daily_manifest=daily_manifest,
        )

        self.artifact_writer.append_history(
            trading_date=trading_date,
            state=new_state,
            order_intents=decision.order_intents,
            fills=execution_result.fills,
        )

        return DailyCommitResult(
            status="COMMITTED",
            trading_date=trading_date,
            account=new_state.account,
            order_intents=list(
                decision.order_intents
            ),
            fills=list(execution_result.fills),
            pending_orders=list(new_pending),
            manifest=dict(daily_manifest),
        )
