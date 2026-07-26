import ast
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_active_live_workflow_contract():
    workflow=(ROOT/".github/workflows/live-track-daily.yml").read_text()
    runner=(ROOT/"scripts/run_fd_m3180125_live_daily.py").read_text()
    production=(ROOT/"src/e1r_engine/live_production.py").read_text()
    ast.parse(runner); ast.parse(production)
    assert "cron: '30 23 * * 1-5'" in workflow
    assert "workflow_dispatch:" in workflow
    assert "workflow_run:" not in workflow
    assert "commit_active_daily" in production
    assert "ACTIVE_RECOMMENDATION_ONLY" in production
    assert "commit_active_daily" in runner
    assert "PASS_LIVE_ACTIVE_NO_NEW_DATE" in runner
