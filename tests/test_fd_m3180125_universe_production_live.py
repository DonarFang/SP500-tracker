from pathlib import Path

from e1r_engine.universe_versioning.production_integration import ProductionUniverseGate


ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "scripts/run_fd_m3180125_live_daily.py"
COMPOSITION = ROOT / "src/e1r_engine/live_composition.py"


def test_U413_live_uses_eligible_symbols_for_engine_and_required_symbols_for_data():
    source = COMPOSITION.read_text()
    assert "stock_symbols=stock_symbols" in source
    assert ".load_date(\n        market_date,\n        required_data_symbols," in source


def test_U414_live_uses_calendar_date_before_production_gate():
    source = LIVE.read_text()
    calendar = source.index("expected_execution_date=live_calendar.next_session(market_date)")
    gate = source.index('production_gate=ProductionUniverseGate(Path.cwd(),"live")')
    assert calendar < gate


def test_U415_live_rechecks_engine_actions_before_recommendation_commit():
    source = LIVE.read_text()
    actions = source.index("actions=tuple")
    final_gate = source.index("final_decision=production_gate.resolve")
    commit = source.index("committed=composition.runtime.commit_active_daily")
    assert actions < final_gate < commit


def test_U416_live_deleted_holding_can_exit_without_membership_block(tmp_path: Path):
    result = ProductionUniverseGate(tmp_path, "live").resolve(expected_execution_date="2026-08-24", production_catalogue=("A",), production_eligible=("A",), holdings_symbols=("OLD",), data_ready_symbols=("A", "OLD"), required_indices=("SPX",), candidate_actions=({"symbol":"OLD","action":"EXIT"},))
    assert result.blocked_risk_increases == ()
    assert "OLD" in result.required_data_universe
