import os
from pathlib import Path

import pytest

from e1r_engine.universe_versioning.production_integration import ProductionUniverseError, ProductionUniverseGate


HEAD = "a3f14b45cf4e2d5746ad67d972fba4dc680904db"


def test_U417_forward_and_live_state_and_evidence_are_physically_separate(tmp_path: Path):
    fw = ProductionUniverseGate(tmp_path, "forward")
    live = ProductionUniverseGate(tmp_path, "live")
    assert fw.mode_path != live.mode_path
    assert fw.storage.export_root != live.storage.export_root


def test_U418_symlink_and_hardlink_mode_paths_hold(tmp_path: Path):
    outside = tmp_path / "outside"; outside.mkdir()
    link = tmp_path / "data/fw_universe"; link.parent.mkdir(); link.symlink_to(outside, target_is_directory=True)
    with pytest.raises(ProductionUniverseError, match="symlink"):
        ProductionUniverseGate(tmp_path, "forward").mode()
    link.unlink(); mode = tmp_path / "data/fw_universe/production/mode.json"; mode.parent.mkdir(parents=True); mode.write_text("{}")
    alias = tmp_path / "alias"; os.link(mode, alias)
    with pytest.raises(ProductionUniverseError, match="hardlink"):
        ProductionUniverseGate(tmp_path, "forward").mode()


def test_U419_independent_switch_does_not_change_other_track(tmp_path: Path):
    fw = ProductionUniverseGate(tmp_path, "forward"); live = ProductionUniverseGate(tmp_path, "live")
    fw.activate(expected_execution_date="2026-08-22", baseline_membership=("A",), authority_head=HEAD, contract_hash="1"*64)
    assert fw.mode() == "ENFORCE" and live.mode() == "OFF"
    live.activate(expected_execution_date="2026-08-24", baseline_membership=("B",), authority_head=HEAD, contract_hash="1"*64)
    fw.deactivate(authority_head=HEAD, contract_hash="1"*64)
    assert fw.mode() == "OFF" and live.mode() == "ENFORCE"


def test_U420_failed_forward_resolution_does_not_touch_live(tmp_path: Path):
    live = ProductionUniverseGate(tmp_path, "live")
    live.activate(expected_execution_date="2026-08-24", baseline_membership=("B",), authority_head=HEAD, contract_hash="1"*64)
    before = live.mode_path.read_bytes()
    with pytest.raises(ProductionUniverseError):
        ProductionUniverseGate(tmp_path, "forward").resolve(expected_execution_date="bad", production_catalogue=("A",), production_eligible=("A",), holdings_symbols=(), data_ready_symbols=("A",), required_indices=())
    assert live.mode_path.read_bytes() == before
