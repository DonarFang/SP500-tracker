"""SIDEWAYS/MA_CONFLICT stateful execution decision policy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from e1r_engine.sideways_core import SidewaysCandidate
from e1r_engine.state import AccountState, OrderIntent


SIDEWAYS_BRANCH = "SIDEWAYS_MA_CONFLICT"


@dataclass(frozen=True)
class SidewaysExecutionConfig:
    candidate_top_n: int = 10
    max_positions: int = 3
    capital_fraction_of_tradable_cash: float = 0.30
    per_position_fraction_of_tradable_cash: float = 0.10

    def validate(self) -> None:
        if self.candidate_top_n != 10:
            raise ValueError("candidate_top_n must remain 10")
        if self.max_positions != 3:
            raise ValueError("max_positions must remain 3")
        if self.capital_fraction_of_tradable_cash != 0.30:
            raise ValueError("capital fraction must remain 0.30")
        if self.per_position_fraction_of_tradable_cash != 0.10:
            raise ValueError("per-position fraction must remain 0.10")


def position_origin_branch(metadata: Mapping[str, object]) -> str:
    value = metadata.get("origin_branch")
    return str(value) if value else "UPTREND"


class SidewaysExecutionPolicy:
    def __init__(
        self,
        config: SidewaysExecutionConfig | None = None,
    ) -> None:
        self.config = config or SidewaysExecutionConfig()
        self.config.validate()

    @staticmethod
    def is_active(regime: str, subclass: str) -> bool:
        return regime == "SIDEWAYS" and subclass == "MA_CONFLICT"

    def build_intents(
        self,
        *,
        date: str,
        regime: str,
        subclass: str,
        ranked_candidates: Sequence[SidewaysCandidate],
        account: AccountState,
        management_actions: Mapping[str, str] | None = None,
    ) -> list[OrderIntent]:
        actions = {
            str(symbol): str(action).upper()
            for symbol, action in (management_actions or {}).items()
        }
        sideways_symbols = {
            symbol
            for symbol, position in account.positions.items()
            if position_origin_branch(position.metadata) == SIDEWAYS_BRANCH
        }

        intents: list[OrderIntent] = []

        if not self.is_active(regime, subclass):
            for symbol in sorted(sideways_symbols):
                intents.append(
                    OrderIntent(
                        date=date,
                        symbol=symbol,
                        intent_type="EXIT",
                        side="SELL",
                        target_quantity=0.0,
                        quantity_delta=None,
                        reason="sideways_ma_conflict_deactivated",
                        branch=SIDEWAYS_BRANCH,
                        metadata={
                            "origin_branch": SIDEWAYS_BRANCH,
                            "forced_branch_exit": True,
                        },
                    )
                )
            return intents

        for symbol in sorted(sideways_symbols):
            position = account.positions[symbol]
            action = actions.get(symbol, "HOLD")
            if action == "EXIT":
                intents.append(
                    OrderIntent(
                        date=date,
                        symbol=symbol,
                        intent_type="EXIT",
                        side="SELL",
                        target_quantity=0.0,
                        quantity_delta=None,
                        reason="sideways_stock_rule_exit",
                        branch=SIDEWAYS_BRANCH,
                        metadata={"origin_branch": SIDEWAYS_BRANCH},
                    )
                )
            elif action == "REDUCE":
                intents.append(
                    OrderIntent(
                        date=date,
                        symbol=symbol,
                        intent_type="REDUCE",
                        side="SELL",
                        target_quantity=None,
                        quantity_delta=-(position.quantity * 0.50),
                        reason="sideways_stock_rule_reduce",
                        branch=SIDEWAYS_BRANCH,
                        metadata={
                            "origin_branch": SIDEWAYS_BRANCH,
                            "reduce_fraction": 0.50,
                            "no_auto_restore": True,
                        },
                    )
                )
            else:
                intents.append(
                    OrderIntent(
                        date=date,
                        symbol=symbol,
                        intent_type="HOLD",
                        side=None,
                        target_quantity=position.quantity,
                        quantity_delta=0.0,
                        reason=(
                            "sideways_add_disabled_hold"
                            if action == "ADD"
                            else "sideways_existing_position_hold"
                        ),
                        branch=SIDEWAYS_BRANCH,
                        metadata={
                            "origin_branch": SIDEWAYS_BRANCH,
                            "sideways_add_disabled": action == "ADD",
                        },
                    )
                )

        available_slots = max(
            0,
            self.config.max_positions - account.open_positions_count,
        )
        held = set(account.positions)
        candidates = [
            row
            for row in ranked_candidates[: self.config.candidate_top_n]
            if row.symbol not in held
        ][:available_slots]

        top10 = list(ranked_candidates[: self.config.candidate_top_n])
        ranks = {row.symbol: index + 1 for index, row in enumerate(top10)}

        for candidate in candidates:
            intents.append(
                OrderIntent(
                    date=date,
                    symbol=candidate.symbol,
                    intent_type="BUY",
                    side="BUY",
                    target_quantity=None,
                    quantity_delta=None,
                    reason="sideways_ma_conflict_ranked_entry",
                    branch=SIDEWAYS_BRANCH,
                    metadata={
                        "origin_branch": SIDEWAYS_BRANCH,
                        "entry_regime": "SIDEWAYS",
                        "entry_subclass": "MA_CONFLICT",
                        "entry_type": "E1R_SIDEWAYS_MA_CONFLICT",
                        "sideways_entry_rank": ranks[candidate.symbol],
                        "sideways_entry_score": candidate.score,
                        "candidate_top_n": 10,
                        "capital_fraction_of_tradable_cash": 0.30,
                        "target_fraction_of_tradable_cash": 0.10,
                    },
                )
            )

        return intents
