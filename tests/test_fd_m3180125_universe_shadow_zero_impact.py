import hashlib
import json
from pathlib import Path

from e1r_engine.universe_versioning.shadow_integration import ShadowObserverConfig, UniverseShadowObserver


ROOT = Path(__file__).resolve().parents[1]
HEAD = "a3f14b45cf4e2d5746ad67d972fba4dc680904db"


def digest(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path, track="forward", protected=()):
    observer = UniverseShadowObserver(ShadowObserverConfig(root,track,HEAD,"2026-08-10T00:00:00Z"))
    return observer.observe(expected_execution_date="2026-08-11",production_catalogue=("A",),production_eligible=("A",),holdings_symbols=(),data_ready_symbols=("A",),required_indices=("SPX",),date_source="FORWARD_DATE_PLANNER" if track=="forward" else "LIVE_CALENDAR_HARD_GATE",protected_paths=protected)


def test_S325_shadow_has_no_canonical_5y_dependency(tmp_path: Path):
    source = (ROOT / "src/e1r_engine/universe_versioning/shadow_integration.py").read_text().lower()
    assert "e1_5y" not in source and "five_year" not in source
    result = run(tmp_path)
    assert result.decision == "PASS_UV_STEP_3_FORWARD_SHADOW_PROBE"


def test_S326_historical_forward_artifacts_are_unchanged(tmp_path: Path):
    history = tmp_path / "exports/official/FD-M3180125-SP500-TOP3-engine/forward/runtime/history/equity_curve.json"
    history.parent.mkdir(parents=True); history.write_text("forward-history")
    before = digest(history); run(tmp_path, protected=(history,))
    assert digest(history) == before


def test_S327_historical_live_artifacts_are_unchanged(tmp_path: Path):
    history = tmp_path / "exports/official/FD-M3180125-SP500-TOP3-engine/live/runtime/history/transactions.jsonl"
    history.parent.mkdir(parents=True); history.write_text("live-history")
    before = digest(history); run(tmp_path,"live",(history,))
    assert digest(history) == before


def test_S328_production_price_catalogues_are_unchanged(tmp_path: Path):
    fw = tmp_path / "data/fw_prices/A.json"; live = tmp_path / "data/live_prices/A.json"
    fw.parent.mkdir(parents=True); live.parent.mkdir(parents=True)
    fw.write_text("fw-price"); live.write_text("live-price")
    before = (digest(fw),digest(live)); run(tmp_path,protected=(fw,live))
    assert (digest(fw),digest(live)) == before


def test_S329_no_production_membership_pointer_or_snapshot(tmp_path: Path):
    result = run(tmp_path)
    assert not (tmp_path / "data/fw_universe/state/current.json").exists()
    assert not (tmp_path / "data/fw_universe/snapshots").exists()
    acceptance = json.loads((result.evidence_root / "acceptance_result.json").read_text())
    assert acceptance["production_side_effect_calls"] == []


def test_S330_legacy_screening_and_dashboard_are_unchanged(tmp_path: Path):
    sentinels = []
    for relative in ("data/oos/state.json","screening/result.json","dashboard/app.js"):
        path = tmp_path / relative; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(relative); sentinels.append(path)
    before = [digest(path) for path in sentinels]; result = run(tmp_path,protected=sentinels)
    assert [digest(path) for path in sentinels] == before
    acceptance = json.loads((result.evidence_root / "acceptance_result.json").read_text())
    assert acceptance["protected_manifests_unchanged"] is True
