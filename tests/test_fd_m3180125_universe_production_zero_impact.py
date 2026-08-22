from pathlib import Path

from e1r_engine.universe_versioning.production_integration import ProductionUniverseGate


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/canonical/FD-M3180125_SP500_UNIVERSE_VERSIONING_UV_STEP_4_CONTRACT_v1.0_FROZEN_2026-08-22.md"


def test_U421_whitelist_excludes_engine_strategy_history_dashboard_and_workflow():
    text = CONTRACT.read_text()
    block = text.split("## 4. Exact source whitelist", 1)[1].split("## 5.", 1)[0]
    for token in ("src/e1r_engine/core.py", "src/e1r_engine/capped_atr_stop.py", "data/research", ".github/workflows", "dashboard"):
        assert token not in block


def test_U422_production_module_has_no_network_strategy_or_broker_dependency():
    source = (ROOT / "src/e1r_engine/universe_versioning/production_integration.py").read_text()
    for token in ("requests", "urllib", "E1RCoreEngine", "LiveEngineAdapter", "broker", "yfinance"):
        assert token not in source


def test_U423_deactivation_retains_immutable_snapshot_and_mode_evidence(tmp_path: Path):
    gate = ProductionUniverseGate(tmp_path, "forward")
    gate.activate(expected_execution_date="2026-08-22", baseline_membership=("A",), authority_head="a"*40, contract_hash="1"*64)
    snapshot = tuple((tmp_path / "data/fw_universe/snapshots").glob("*.json"))
    gate.deactivate(authority_head="a"*40, contract_hash="1"*64)
    assert snapshot and all(path.is_file() for path in snapshot)
    assert len(tuple((gate.storage.export_root / "production/mode_changes").glob("*.json"))) == 2


def test_U424_uv4_does_not_run_or_rewrite_production_during_activation():
    source = (ROOT / "scripts/activate_fd_m3180125_universe_production.py").read_text()
    assert "production_run_performed\": False" in source
    assert "price_update_performed\": False" in source
    for token in ("commit_day(", "engine.step(", "update_fd_m3180125", "backtest"):
        assert token not in source
