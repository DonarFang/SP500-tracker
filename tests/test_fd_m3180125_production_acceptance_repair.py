from __future__ import annotations

from datetime import date
from datetime import datetime, timezone
import json
from pathlib import Path

from e1r_engine.source_automation.event_publication import _resolve_track_snapshot
from e1r_engine.universe_versioning.hashing import content_hash
from scripts.resolve_fd_m3180125_latest_completed_session import (
    latest_completed_session,
)


ROOT = Path(__file__).resolve().parents[1]


def test_forward_freshness_gate_covers_all_required_indices():
    source = (ROOT / "scripts/update_engine_forward_prices.py").read_text()
    assert '"_GSPC": "^GSPC"' in source
    assert '"_NDX": "^NDX"' in source
    assert '"_SOX": "^SOX"' in source
    assert '"_VIX": "^VIX"' in source
    assert "HOLD_ENGINE_FORWARD_REQUIRED_INDEX_FRESHNESS" in source
    assert "def clip_frame_to_expected_session(" in source
    assert 'frame["date"] <= expected_latest_market_date' in source
    assert "frame = clip_frame_to_expected_session(" in source


def test_latest_completed_session_does_not_claim_incomplete_day():
    before_close = datetime(2026, 8, 25, 20, 0, tzinfo=timezone.utc)
    after_close = datetime(2026, 8, 25, 23, 0, tzinfo=timezone.utc)
    assert latest_completed_session(before_close) == "2026-08-24"
    assert latest_completed_session(after_close) == "2026-08-25"


def test_live_reconciliation_is_valid_and_track_local():
    path = ROOT / "data/live_universe/pre_activation_reconciliations.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    recorded = payload.pop("content_hash")
    assert payload["track"] == "live"
    assert recorded == content_hash(payload)
    rows = {(row["outgoing"], row["incoming"]) for row in payload["reconciliations"]}
    assert rows == {("CTRA", "VEEV"), ("EA", "FERG")}


def test_live_effective_membership_has_official_replacements():
    snapshot = _resolve_track_snapshot(
        ROOT, "live", date(2026, 8, 24).isoformat()
    )
    members = set(snapshot.effective_membership)
    assert {"VEEV", "FERG"} <= members
    assert not ({"CTRA", "EA"} & members)


def test_forward_and_live_top3_are_not_cross_track_acceptance_gate():
    forward = (ROOT / ".github/workflows/engine-forward-daily.yml").read_text()
    live = (ROOT / ".github/workflows/live-track-daily.yml").read_text()
    combined = forward + "\n" + live
    assert "TOP3_EQUAL" not in combined
    assert "top3 ==" not in combined.lower()
    assert "fd-m3180125-production-main-writer" in forward
    assert "fd-m3180125-production-main-writer" in live
    assert "data/fw_universe/state/ data/fw_universe/snapshots/" in forward
    assert "data/live_universe/state/ data/live_universe/snapshots/" in live
