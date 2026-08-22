import json
import os
from pathlib import Path

import pytest

from e1r_engine.universe_versioning.shadow_integration import ShadowIntegrationError, ShadowObserverConfig, UniverseShadowObserver


HEAD = "a3f14b45cf4e2d5746ad67d972fba4dc680904db"


def observe(root: Path, track: str):
    return UniverseShadowObserver(ShadowObserverConfig(root, track, HEAD, "2026-08-10T00:00:00Z")).observe(expected_execution_date="2026-08-11",production_catalogue=("A",),production_eligible=("A",),holdings_symbols=(),data_ready_symbols=("A",),required_indices=("SPX",),date_source="FORWARD_DATE_PLANNER" if track == "forward" else "LIVE_CALENDAR_HARD_GATE")


def test_S319_forward_live_are_distinct_physical_files(tmp_path: Path):
    forward, live = observe(tmp_path,"forward"), observe(tmp_path,"live")
    f = forward.evidence_root / "acceptance_result.json"; l = live.evidence_root / "acceptance_result.json"
    assert f != l and os.stat(f).st_ino != os.stat(l).st_ino
    l.unlink()
    os.link(f, l)
    with pytest.raises(ShadowIntegrationError, match="hardlink"):
        observe(tmp_path,"live")


def test_S320_symlink_cross_track_boundary_holds(tmp_path: Path):
    for case in ("shadow-root", "parent", "cross-track-target"):
        case_root = tmp_path / case
        outside = case_root / "outside"
        outside.mkdir(parents=True)
        universe = case_root / "exports/official/FD-M3180125-SP500-TOP3-engine/forward/universe"
        if case == "parent":
            universe.parent.mkdir(parents=True)
            universe.symlink_to(outside, target_is_directory=True)
        else:
            universe.mkdir(parents=True)
            target = outside
            if case == "cross-track-target":
                target = case_root / "exports/official/FD-M3180125-SP500-TOP3-engine/live/universe/shadow"
                target.mkdir(parents=True)
            (universe / "shadow").symlink_to(target, target_is_directory=True)
        with pytest.raises(ShadowIntegrationError, match="symlink"):
            observe(case_root,"forward")


def test_S321_single_track_failure_does_not_touch_other(tmp_path: Path):
    live = observe(tmp_path,"live")
    before = (live.evidence_root / "acceptance_result.json").read_bytes()
    config = ShadowObserverConfig(tmp_path,"forward",HEAD,"2026-08-10T00:00:00Z")
    with pytest.raises(ShadowIntegrationError):
        UniverseShadowObserver(config).observe(expected_execution_date="bad",production_catalogue=("A",),production_eligible=("A",),holdings_symbols=(),data_ready_symbols=("A",),required_indices=("SPX",),date_source="FORWARD_DATE_PLANNER")
    assert (live.evidence_root / "acceptance_result.json").read_bytes() == before


def test_S322_same_input_is_idempotent(tmp_path: Path):
    first, second = observe(tmp_path,"forward"), observe(tmp_path,"forward")
    assert first.run_id == second.run_id
    assert first.evidence_root == second.evidence_root
    assert len(list(first.evidence_root.iterdir())) == 10
    changed = UniverseShadowObserver(
        ShadowObserverConfig(tmp_path,"forward",HEAD,"2026-08-10T00:00:00Z")
    ).observe(
        expected_execution_date="2026-08-11",
        production_catalogue=("A",),
        production_eligible=("A",),
        holdings_symbols=(),
        data_ready_symbols=("A",),
        required_indices=("SPX",),
        candidate_actions=({"symbol":"A","action":"BUY"},),
        date_source="FORWARD_DATE_PLANNER",
    )
    assert changed.run_id != first.run_id


def test_S323_atomic_publication_leaves_no_temp(tmp_path: Path, monkeypatch):
    import e1r_engine.universe_versioning.shadow_integration as module

    real_replace = module.os.replace
    monkeypatch.setattr(module.os, "replace", lambda *args: (_ for _ in ()).throw(OSError("injected")))
    with pytest.raises(OSError, match="injected"):
        observe(tmp_path,"forward")
    shadow = tmp_path / "exports/official/FD-M3180125-SP500-TOP3-engine/forward/universe/shadow"
    assert not [path for path in shadow.iterdir() if not path.name.startswith(".uv3-")]
    assert not list(shadow.glob(".uv3-*"))

    monkeypatch.setattr(module.os, "replace", real_replace)
    result = observe(tmp_path,"forward")
    assert sorted(path.name for path in result.evidence_root.iterdir()) == sorted(UniverseShadowObserver.EVIDENCE_NAMES)
    assert not list(result.evidence_root.parent.glob(".uv3-*"))


def test_S324_immutable_conflict_is_not_overwritten(tmp_path: Path):
    result = observe(tmp_path,"forward")
    target = result.evidence_root / "acceptance_result.json"
    target.write_text(json.dumps({"tampered":True}))
    with pytest.raises(ShadowIntegrationError, match="immutable evidence conflict"):
        observe(tmp_path,"forward")
    assert json.loads(target.read_text()) == {"tampered":True}
