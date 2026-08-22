import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from e1r_engine.forward_orchestrator import OfficialForwardCatchupRunner
from e1r_engine.universe_versioning.shadow_integration import (
    ShadowIntegrationError,
    ShadowObserverConfig,
    UniverseShadowObserver,
)


HEAD = "a3f14b45cf4e2d5746ad67d972fba4dc680904db"


def observer(root: Path):
    return UniverseShadowObserver(ShadowObserverConfig(root, "forward", HEAD, "2026-08-10T00:00:00Z"))


def write_event(root: Path, effective="2026-08-12", additions=("NEW",), deletions=("OLD",)):
    path = root / "data/fw_universe/events/E/revision-001.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"event_id":"E","revision":1,"index_id":"SP500","source_type":"SPDJI_INDEX_NEWS","source_url":"u","source_document_hash":"h","announcement_timestamp":"2026-08-11T00:00:00Z","effective_date":effective,"effective_time":"09:30","effective_timezone":"America/New_York","additions":list(additions),"deletions":list(deletions),"event_status":"EFFECTIVE"}))


def test_S307_every_forward_planned_date_is_observed(tmp_path: Path):
    calls = []
    class State:
        last_committed_date = "2026-08-10"
        account = SimpleNamespace(positions={})
        def validate(self): pass
    class Observer:
        def __call__(self, **kwargs):
            calls.append(kwargs)
            return {"expected_execution_date": kwargs["expected_execution_date"]}
    runner = OfficialForwardCatchupRunner(
        seed_loader=SimpleNamespace(load=lambda: State()), repository=SimpleNamespace(exists=lambda: True, load=lambda: State()),
        date_planner=SimpleNamespace(plan=lambda **kwargs: ["2026-08-11","2026-08-12"]),
        market_data_adapter=SimpleNamespace(latest_complete_common_date=lambda **kwargs: "2026-08-12"),
        snapshot_builder=SimpleNamespace(required_indices=("SPX","NDX","SOX")), strategy_input_builder=None,
        committer=None, universe=("A",), series_by_symbol={"A":{"2026-08-11":1,"2026-08-12":1}},
        required_execution_symbols=("A",), shadow_observer=Observer())
    assert len(runner.run_shadow_probe()) == 2
    assert [row["expected_execution_date"] for row in calls] == ["2026-08-11","2026-08-12"]
    assert [row["market_date"] for row in calls] == ["2026-08-11","2026-08-12"]
    assert all(row["date_source"] == "FORWARD_DATE_PLANNER" for row in calls)
    calls.clear()
    replay_runner = OfficialForwardCatchupRunner(
        seed_loader=SimpleNamespace(load=lambda: State()),
        repository=SimpleNamespace(exists=lambda: True, load=lambda: State()),
        date_planner=SimpleNamespace(plan=lambda **kwargs: []),
        market_data_adapter=SimpleNamespace(
            latest_complete_common_date=lambda **kwargs: "2026-08-10"
        ),
        snapshot_builder=SimpleNamespace(required_indices=("SPX","NDX","SOX")),
        strategy_input_builder=None, committer=None, universe=("A",),
        series_by_symbol={"A":{"2026-08-10":1}},
        required_execution_symbols=("A",), shadow_observer=Observer())
    replay = replay_runner.run_shadow_probe()
    assert replay[0]["probe_date_basis"] == "CURRENT_LAST_COMMITTED_FORWARD_DATE_PLANNER_DATE"
    assert calls[0]["expected_execution_date"] == "2026-08-10"


def test_S308_forward_crosses_effective_date_with_distinct_hashes(tmp_path: Path):
    write_event(tmp_path)
    before = observer(tmp_path).observe(expected_execution_date="2026-08-11",production_catalogue=("OLD",),production_eligible=("OLD",),holdings_symbols=(),data_ready_symbols=("OLD","NEW"),required_indices=("SPX",),date_source="FORWARD_DATE_PLANNER")
    after = observer(tmp_path).observe(expected_execution_date="2026-08-12",production_catalogue=("OLD",),production_eligible=("OLD",),holdings_symbols=(),data_ready_symbols=("OLD","NEW"),required_indices=("SPX",),date_source="FORWARD_DATE_PLANNER")
    assert before.shadow_membership_hash != after.shadow_membership_hash


def test_S309_buy_add_diff_is_evidence_only(tmp_path: Path):
    result = observer(tmp_path).observe(expected_execution_date="2026-08-11",production_catalogue=("A",),production_eligible=("A",),holdings_symbols=(),data_ready_symbols=("A",),required_indices=("SPX",),candidate_actions=({"symbol":"A","action":"BUY"},{"symbol":"B","action":"ADD"}),date_source="FORWARD_DATE_PLANNER")
    payload = json.loads((result.evidence_root / "universe_diff.json").read_text())
    assert payload["would_allow_buy_add"] == [{"action":"BUY","symbol":"A"}]
    assert payload["would_block_buy_add"] == [{"action":"ADD","symbol":"B"}]
    report = result.to_dict()
    required = {
        "track", "authority_head", "market_date", "expected_execution_date",
        "production_catalogue_hash", "production_eligible_hash", "holdings_hash",
        "shadow_membership_hash", "shadow_eligible_hash", "shadow_required_data_hash",
        "would_allow_buy_add", "would_block_buy_add", "cross_track_reads_detected",
        "cross_track_writes_detected", "production_side_effect_calls",
        "protected_manifests_unchanged", "decision",
    }
    assert required <= set(report)


def test_S310_deleted_forward_holding_has_no_auto_exit(tmp_path: Path):
    write_event(tmp_path, additions=(), deletions=("OLD",))
    result = observer(tmp_path).observe(expected_execution_date="2026-08-12",production_catalogue=("OLD",),production_eligible=("OLD",),holdings_symbols=("OLD",),data_ready_symbols=("OLD",),required_indices=("SPX",),date_source="FORWARD_DATE_PLANNER")
    payload = json.loads((result.evidence_root / "universe_diff.json").read_text())
    assert payload["holdings_retained_for_management"] == ["OLD"]
    assert payload["automatic_exits_created"] == []


def test_S311_forward_writes_only_forward_shadow(tmp_path: Path):
    result = observer(tmp_path).observe(expected_execution_date="2026-08-11",production_catalogue=("A",),production_eligible=("A",),holdings_symbols=(),data_ready_symbols=("A",),required_indices=("SPX",),date_source="FORWARD_DATE_PLANNER")
    assert "/forward/universe/shadow/" in str(result.evidence_root)
    assert not (tmp_path / "exports/official/FD-M3180125-SP500-TOP3-engine/live/universe/shadow").exists()


def test_S312_forward_production_input_is_unchanged(tmp_path: Path, monkeypatch):
    import e1r_engine.universe_versioning.shadow_integration as module

    protected = tmp_path / "runtime.json"; protected.write_text("unchanged")
    real_manifest = module.manifest_paths
    values = iter(("before", "after"))
    monkeypatch.setattr(module, "manifest_paths", lambda *args, **kwargs: next(values))
    with pytest.raises(ShadowIntegrationError, match="protected production manifest changed"):
        observer(tmp_path).observe(expected_execution_date="2026-08-11",production_catalogue=("A",),production_eligible=("A",),holdings_symbols=(),data_ready_symbols=("A",),required_indices=("SPX",),date_source="FORWARD_DATE_PLANNER",protected_paths=(protected,))
    shadow = tmp_path / "exports/official/FD-M3180125-SP500-TOP3-engine/forward/universe/shadow"
    assert not shadow.exists()

    monkeypatch.setattr(module, "manifest_paths", real_manifest)
    result = observer(tmp_path).observe(expected_execution_date="2026-08-11",production_catalogue=("A",),production_eligible=("A",),holdings_symbols=(),data_ready_symbols=("A",),required_indices=("SPX",),date_source="FORWARD_DATE_PLANNER",protected_paths=(protected,))
    impact = json.loads((result.evidence_root / "production_impact_comparison.json").read_text())
    assert protected.read_text() == "unchanged"
    assert impact["production_impact"] == "ZERO" and impact["production_side_effect_calls"] == []
