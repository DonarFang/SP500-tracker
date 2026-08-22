import json
from pathlib import Path

import pytest

from e1r_engine.universe_versioning.production_integration import (
    ProductionUniverseError,
    ProductionUniverseGate,
)


HEAD = "a3f14b45cf4e2d5746ad67d972fba4dc680904db"
CONTRACT_HASH = "1" * 64


def activate(root: Path, track="forward", members=("A", "B")):
    gate = ProductionUniverseGate(root, track)
    gate.activate(expected_execution_date="2026-08-22", baseline_membership=members, authority_head=HEAD, contract_hash=CONTRACT_HASH)
    return gate


def test_U405_missing_mode_is_off_and_preserves_production_eligible(tmp_path: Path):
    result = ProductionUniverseGate(tmp_path, "forward").resolve(expected_execution_date="2026-08-22", production_catalogue=("A", "B"), production_eligible=("B",), holdings_symbols=(), data_ready_symbols=("A", "B"), required_indices=("SPX",))
    assert result.mode == "OFF"
    assert result.eligible_buy_universe == ("B",)


def test_U406_activation_publishes_hash_validated_snapshot_pointer_and_evidence(tmp_path: Path):
    gate = activate(tmp_path)
    result = gate.resolve(expected_execution_date="2026-08-22", production_catalogue=("A", "B"), production_eligible=("A", "B"), holdings_symbols=(), data_ready_symbols=("A", "B"), required_indices=())
    pointer = json.loads((tmp_path / "data/fw_universe/state/current.json").read_text())
    mode = json.loads((tmp_path / "data/fw_universe/production/mode.json").read_text())
    evidence = tmp_path / "exports/official/FD-M3180125-SP500-TOP3-engine/forward/universe/production/mode_changes" / (mode["evidence_hash"] + ".json")
    assert result.mode == "ENFORCE" and pointer["content_hash"] == result.snapshot_hash
    assert evidence.is_file()


def test_U407_event_membership_price_readiness_and_held_deletion(tmp_path: Path):
    event = tmp_path / "data/fw_universe/events/E/revision-001.json"
    event.parent.mkdir(parents=True)
    event.write_text(json.dumps({"event_id":"E","revision":1,"index_id":"SP500","source_type":"SPDJI_INDEX_NEWS","source_url":"u","source_document_hash":"h","announcement_timestamp":"2026-08-21T00:00:00Z","effective_date":"2026-08-22","effective_time":"09:30","effective_timezone":"America/New_York","additions":["C"],"deletions":["A"],"event_status":"EFFECTIVE"}))
    gate = activate(tmp_path, members=("A", "B"))
    result = gate.resolve(expected_execution_date="2026-08-22", production_catalogue=("A", "B", "C"), production_eligible=("A", "B", "C"), holdings_symbols=("A",), data_ready_symbols=("A", "B", "C"), required_indices=("SPX",), candidate_actions=({"symbol":"A","action":"BUY"},{"symbol":"A","action":"EXIT"}))
    assert result.eligible_buy_universe == ("B", "C")
    assert "A" in result.required_data_universe
    assert result.blocked_risk_increases == ({"symbol":"A","action":"BUY"},)


def test_U408_tampered_mode_or_snapshot_holds(tmp_path: Path):
    gate = activate(tmp_path)
    mode_path = tmp_path / "data/fw_universe/production/mode.json"
    payload = json.loads(mode_path.read_text()); payload["mode"] = "OFF"; mode_path.write_text(json.dumps(payload))
    with pytest.raises(ProductionUniverseError, match="content hash mismatch"):
        gate.mode()
