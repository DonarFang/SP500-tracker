import json
from pathlib import Path

import pytest

from e1r_engine.universe_versioning.shadow_integration import ShadowIntegrationError, ShadowObserverConfig, UniverseShadowObserver


ROOT = Path(__file__).resolve().parents[1]
HEAD = "a3f14b45cf4e2d5746ad67d972fba4dc680904db"


def observer(root: Path):
    return UniverseShadowObserver(ShadowObserverConfig(root, "live", HEAD, "2026-08-10T00:00:00Z"))


def write_event(root: Path):
    path = root / "data/live_universe/events/E/revision-001.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"event_id":"E","revision":1,"index_id":"SP500","source_type":"SPDJI_INDEX_NEWS","source_url":"u","source_document_hash":"h","announcement_timestamp":"2026-08-11T00:00:00Z","effective_date":"2026-08-12","effective_time":"09:30","effective_timezone":"America/New_York","additions":["NEW"],"deletions":["OLD"],"event_status":"EFFECTIVE"}))


def test_S313_calendar_is_before_shadow_and_composition():
    source = (ROOT / "scripts/run_fd_m3180125_live_daily.py").read_text()
    calendar = source.index("expected_execution_date=live_calendar.next_session")
    shadow = source.index("if args.uv_shadow_probe:")
    composition = source.index("composition=compose_active_live_production")
    assert calendar < shadow < composition
    assert "if not args.uv_shadow_probe and last_raw" in source


def test_S314_live_rejects_non_calendar_date_source(tmp_path: Path):
    with pytest.raises(ShadowIntegrationError, match="Calendar Hard Gate"):
        observer(tmp_path).observe(expected_execution_date="2026-08-11",production_catalogue=("A",),production_eligible=("A",),holdings_symbols=(),data_ready_symbols=("A",),required_indices=("SPX",),date_source="FORWARD_DATE_PLANNER")


def test_S315_live_uses_its_own_baseline_and_events(tmp_path: Path):
    write_event(tmp_path)
    result = observer(tmp_path).observe(expected_execution_date="2026-08-12",production_catalogue=("OLD",),production_eligible=("OLD",),holdings_symbols=(),data_ready_symbols=("NEW",),required_indices=("SPX",),date_source="LIVE_CALENDAR_HARD_GATE")
    baseline = json.loads((result.evidence_root / "baseline_observation.json").read_text())
    membership = json.loads((result.evidence_root / "membership_resolution.json").read_text())
    assert baseline["source"] == "PRODUCTION_EQUIVALENT_CATALOGUE"
    assert membership["snapshot"]["effective_membership"] == ["NEW"]


def test_S316_membership_and_daily_eligible_are_separate(tmp_path: Path):
    result = observer(tmp_path).observe(expected_execution_date="2026-08-11",production_catalogue=("A","B"),production_eligible=("A",),holdings_symbols=(),data_ready_symbols=("A",),required_indices=("SPX",),date_source="LIVE_CALENDAR_HARD_GATE")
    membership = json.loads((result.evidence_root / "membership_resolution.json").read_text())
    assert membership["snapshot"]["effective_membership"] == ["A","B"]
    assert result.shadow_membership_hash != result.shadow_eligible_hash


def test_S317_deleted_live_holding_remains_required_data(tmp_path: Path):
    write_event(tmp_path)
    result = observer(tmp_path).observe(expected_execution_date="2026-08-12",production_catalogue=("OLD",),production_eligible=("OLD",),holdings_symbols=("OLD",),data_ready_symbols=("NEW","OLD"),required_indices=("SPX",),date_source="LIVE_CALENDAR_HARD_GATE")
    diff = json.loads((result.evidence_root / "universe_diff.json").read_text())
    assert diff["holdings_retained_for_management"] == ["OLD"]
    assert diff["automatic_exits_created"] == []


def test_S318_live_recommendation_account_and_ledgers_unchanged(tmp_path: Path):
    files = []
    for name in ("recommendation.json","account.json","transactions.jsonl","cash_control.jsonl","equity.json"):
        path = tmp_path / name; path.write_text(name); files.append(path)
    result = observer(tmp_path).observe(expected_execution_date="2026-08-11",production_catalogue=("A",),production_eligible=("A",),holdings_symbols=(),data_ready_symbols=("A",),required_indices=("SPX",),date_source="LIVE_CALENDAR_HARD_GATE",protected_paths=files)
    assert [path.read_text() for path in files] == [path.name for path in files]
    impact = json.loads((result.evidence_root / "production_impact_comparison.json").read_text())
    assert impact["account_or_ledger_commit_called"] is False
    report = result.to_dict()
    assert report["market_date"] == "2026-08-11"
    assert report["production_side_effect_calls"] == []
