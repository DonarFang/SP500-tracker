from pathlib import Path
from types import SimpleNamespace

import pytest

from e1r_engine.forward_orchestrator import ForwardContractError, OfficialForwardCatchupRunner
from e1r_engine.universe_versioning.production_integration import ProductionUniverseGate


def runner(gate=None, pending=()):
    class State:
        last_committed_date = "2026-08-21"
        account = SimpleNamespace(positions={})
        pending_orders = pending
        def validate(self): pass
    state = State()
    committer = SimpleNamespace(commit_day=lambda **kwargs: (_ for _ in ()).throw(AssertionError("commit must not be called")))
    return OfficialForwardCatchupRunner(seed_loader=SimpleNamespace(load=lambda: state), repository=SimpleNamespace(exists=lambda: True, load=lambda: state), date_planner=SimpleNamespace(plan=lambda **kwargs: ["2026-08-22"]), market_data_adapter=SimpleNamespace(latest_complete_common_date=lambda **kwargs: "2026-08-22"), snapshot_builder=SimpleNamespace(required_indices=()), strategy_input_builder=None, committer=committer, universe=("A", "B"), series_by_symbol={"A":{"2026-08-22":1},"B":{"2026-08-22":1}}, required_execution_symbols=(), production_universe_gate=gate)


def test_U409_forward_gate_receives_real_planner_date_and_holdings():
    calls = []
    r = runner(lambda **kwargs: calls.append(kwargs) or SimpleNamespace(eligible_buy_universe=("A",), required_data_universe=("A",), blocked_risk_increases=()))
    r._production_universe_decision(execution_date="2026-08-22", account=SimpleNamespace(positions={"B":1}))
    assert calls[0]["expected_execution_date"] == "2026-08-22"
    assert calls[0]["holdings_symbols"] == {"B":1}


def test_U410_forward_pending_ineligible_buy_holds_before_committer():
    order = SimpleNamespace(symbol="B", intent_type="BUY")
    gate = lambda **kwargs: SimpleNamespace(eligible_buy_universe=("A",), required_data_universe=("A",), blocked_risk_increases=({"symbol":"B","action":"BUY"},))
    with pytest.raises(ForwardContractError, match="pending BUY/ADD"):
        runner(gate, (order,)).run(allow_official_write=True)


def test_U411_forward_reduce_exit_are_not_blocked_by_membership(tmp_path: Path):
    gate = ProductionUniverseGate(tmp_path, "forward")
    result = gate.resolve(expected_execution_date="2026-08-22", production_catalogue=("A",), production_eligible=("A",), holdings_symbols=("B",), data_ready_symbols=("A", "B"), required_indices=(), candidate_actions=({"symbol":"B","action":"REDUCE"},{"symbol":"B","action":"EXIT"}))
    assert result.blocked_risk_increases == ()
    assert "B" in result.required_data_universe


def test_U412_forward_off_mode_does_not_inject_gate():
    source = (Path(__file__).resolve().parents[1] / "scripts/run_engine_forward_daily.py").read_text()
    assert 'if production_gate.mode() == "ENFORCE"' in source
    assert "composition.runner.production_universe_gate = production_gate.resolve" in source
