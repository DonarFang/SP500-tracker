from e1r_engine.sideways_core import SidewaysCandidate
from e1r_engine.sideways_execution import (
    SIDEWAYS_BRANCH,
    SidewaysExecutionPolicy,
)
from e1r_engine.sideways_execution_adapter import SidewaysExecutionAdapter
from e1r_engine.state import AccountState, PositionState


def c(symbol, score):
    return SidewaysCandidate(
        symbol=symbol,
        score=score,
        close=100.0,
        mom20_pct=1.0,
        mom60_pct=1.0,
        rs20_vs_spx_pct=1.0,
        rs60_vs_spx_pct=1.0,
        trend_points_0_to_6=4,
        drawdown_60d_pct=-1.0,
        one_day_return=0.0,
    )


def account(*rows):
    positions = {}
    for symbol, origin in rows:
        p = PositionState.create(
            symbol=symbol,
            quantity=10,
            avg_cost=100,
            price=100,
            date="2026-01-02",
        )
        object.__setattr__(p, "metadata", {"origin_branch": origin})
        positions[symbol] = p
    value = sum(p.market_value for p in positions.values())
    return AccountState(
        date="2026-01-05",
        cash=10000,
        positions=positions,
        total_equity=10000 + value,
        positions_value=value,
        open_positions_count=len(positions),
        metadata={},
    )


def test_empty_account_buys_top_three_with_cash_budget_metadata():
    intents = SidewaysExecutionPolicy().build_intents(
        date="2026-01-05",
        regime="SIDEWAYS",
        subclass="MA_CONFLICT",
        ranked_candidates=[c("A", 3), c("B", 2), c("C", 1), c("D", 0)],
        account=account(),
    )
    buys = [row for row in intents if row.intent_type == "BUY"]
    assert [row.symbol for row in buys] == ["A", "B", "C"]
    assert all(row.metadata["target_fraction_of_tradable_cash"] == 0.10 for row in buys)
    assert all(row.metadata["capital_fraction_of_tradable_cash"] == 0.30 for row in buys)


def test_global_max_three_counts_uptrend_positions():
    intents = SidewaysExecutionPolicy().build_intents(
        date="2026-01-05",
        regime="SIDEWAYS",
        subclass="MA_CONFLICT",
        ranked_candidates=[c("A", 3), c("B", 2)],
        account=account(("U1", "UPTREND"), ("U2", "UPTREND")),
    )
    assert [row.symbol for row in intents if row.intent_type == "BUY"] == ["A"]


def test_no_rank_replacement_and_add_disabled():
    intents = SidewaysExecutionPolicy().build_intents(
        date="2026-01-05",
        regime="SIDEWAYS",
        subclass="MA_CONFLICT",
        ranked_candidates=[c("NEW", 10)],
        account=account(("OLD", SIDEWAYS_BRANCH), ("U1", "UPTREND"), ("U2", "UPTREND")),
        management_actions={"OLD": "ADD"},
    )
    assert not [row for row in intents if row.intent_type == "BUY"]
    hold = next(row for row in intents if row.symbol == "OLD")
    assert hold.intent_type == "HOLD"
    assert hold.metadata["sideways_add_disabled"] is True


def test_reduce_is_half_and_not_restored():
    intent = SidewaysExecutionPolicy().build_intents(
        date="2026-01-05",
        regime="SIDEWAYS",
        subclass="MA_CONFLICT",
        ranked_candidates=[],
        account=account(("S", SIDEWAYS_BRANCH)),
        management_actions={"S": "REDUCE"},
    )[0]
    assert intent.intent_type == "REDUCE"
    assert intent.quantity_delta == -5.0
    assert intent.metadata["reduce_fraction"] == 0.50
    assert intent.metadata["no_auto_restore"] is True


def test_leaving_ma_conflict_exits_only_sideways_origin():
    intents = SidewaysExecutionPolicy().build_intents(
        date="2026-01-05",
        regime="UPTREND",
        subclass="NO_SUBCLASS",
        ranked_candidates=[],
        account=account(("S", SIDEWAYS_BRANCH), ("U", "UPTREND")),
    )
    assert [(row.symbol, row.intent_type) for row in intents] == [("S", "EXIT")]


def test_adapter_carries_tradable_cash_contract():
    intent = SidewaysExecutionPolicy().build_intents(
        date="2026-01-05",
        regime="SIDEWAYS",
        subclass="MA_CONFLICT",
        ranked_candidates=[c("A", 3)],
        account=account(),
    )[0]
    metadata = dict(intent.metadata)
    metadata["close_t"] = 100.0
    intent = type(intent)(
        date=intent.date,
        symbol=intent.symbol,
        intent_type=intent.intent_type,
        side=intent.side,
        target_quantity=intent.target_quantity,
        quantity_delta=intent.quantity_delta,
        reason=intent.reason,
        branch=intent.branch,
        metadata=metadata,
    )
    payload = SidewaysExecutionAdapter.to_legacy_pending_order(intent)
    assert payload["target_fraction_of_tradable_cash"] == 0.10
    assert payload["capital_fraction_of_tradable_cash"] == 0.30
