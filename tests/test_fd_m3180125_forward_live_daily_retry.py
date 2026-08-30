from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORWARD_WORKFLOW = (ROOT / ".github/workflows/engine-forward-daily.yml").read_text()
LIVE_WORKFLOW = (ROOT / ".github/workflows/live-track-daily.yml").read_text()
FORWARD_UPDATER = (ROOT / "scripts/update_engine_forward_prices.py").read_text()
LIVE_UPDATER = (ROOT / "scripts/update_fd_m3180125_live_adjusted_prices.py").read_text()
COMPLETION_GATE = (ROOT / "scripts/check_fd_m3180125_track_session_complete.py").read_text()


def test_primary_and_same_session_retry_slots_are_frozen():
    assert "cron: '30 23 * * 1-5'" in FORWARD_WORKFLOW
    assert "cron: '30 1,3,7 * * 2-6'" in FORWARD_WORKFLOW
    assert "cron: '30 0,2,4,8 * * 2-6'" in LIVE_WORKFLOW


def test_successful_track_skips_later_downloads_and_strategy_runs():
    assert "check_fd_m3180125_track_session_complete.py" in FORWARD_WORKFLOW
    assert "check_fd_m3180125_track_session_complete.py" in LIVE_WORKFLOW
    assert "- 'scripts/check_fd_m3180125_track_session_complete.py'" in LIVE_WORKFLOW
    assert FORWARD_WORKFLOW.count("steps.completion.outputs.complete != 'true'") == 2
    assert LIVE_WORKFLOW.count("steps.completion.outputs.complete != 'true'") == 2


def test_shared_writer_lock_preserves_download_mutual_exclusion():
    lock = "group: fd-m3180125-production-main-writer"
    assert lock in FORWARD_WORKFLOW
    assert lock in LIVE_WORKFLOW
    assert "cancel-in-progress: false" in FORWARD_WORKFLOW
    assert "cancel-in-progress: false" in LIVE_WORKFLOW


def test_required_index_direct_fetch_has_bounded_retries():
    for source in (FORWARD_UPDATER, LIVE_UPDATER):
        ast.parse(source)
        assert "REQUIRED_INDEX_DIRECT_ATTEMPTS = 3" in source
        assert "REQUIRED_INDEX_DIRECT_RETRY_SECONDS = (20.0, 60.0)" in source
        assert "def download_required_indices(" in source
        assert "downloaded.update(" in source


def test_completion_gate_is_read_only_and_track_local():
    ast.parse(COMPLETION_GATE)
    assert "write_text" not in COMPLETION_GATE
    assert "data/fw_prices" not in COMPLETION_GATE
    assert "data/live_prices" not in COMPLETION_GATE
    assert 'choices=("forward", "live")' in COMPLETION_GATE
