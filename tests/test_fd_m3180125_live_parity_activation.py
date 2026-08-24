import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_live_defaults_to_adjusted_accepted_and_preserves_rollback():
    source = (ROOT / "scripts/run_fd_m3180125_live_daily.py").read_text()
    ast.parse(source)
    assert '"ADJUSTED_ACCEPTED").strip().upper()' in source
    assert '{"ADJUSTED_ACCEPTED", "LEGACY_HOLD"}' in source
    assert 'current_adjusted_accepted.json' in source
    assert 'Path("data/live_prices_adjusted_v1/live_prices")' in source


def test_active_workflow_rebuilds_adjusted_prices_before_live():
    workflow = (ROOT / ".github/workflows/live-track-daily.yml").read_text()
    build_at = workflow.index("Build accepted adjusted Personal Live prices")
    live_at = workflow.index("Run ACTIVE Personal Live daily")
    assert build_at < live_at
    assert "--accepted-production" in workflow
    assert "PASS_LIVE_ADJUSTED_PRICE_LIBRARY_BUILT" in workflow
    assert "FD_M3180125_LIVE_PRICE_MODE: ADJUSTED_ACCEPTED" in workflow
    assert "Activate Forward and Live adjusted price and REDUCE parity" in workflow


def test_accepted_builder_keeps_shadow_default_for_isolated_checks():
    source = (
        ROOT / "scripts/build_fd_m3180125_live_adjusted_shadow.py"
    ).read_text()
    ast.parse(source)
    assert '"--accepted-production"' in source
    assert '"PASS_LIVE_ADJUSTED_PRICE_LIBRARY_BUILT"' in source
    assert '"ADJUSTED_SHADOW_NOT_ACTIVE"' in source


def test_forward_and_live_share_half_unit_reduce_contract():
    canonical = (ROOT / "src/e1r_engine/canonical_runtime.py").read_text()
    forward = (ROOT / "src/e1r_engine/forward_runtime.py").read_text()
    live_cycle = (ROOT / "src/e1r_engine/live_cycle_state.py").read_text()
    assert 'if action == "REDUCE" and size_units <= 0.5' in canonical
    assert 'metadata["size_units"] = max(' in forward and "0.5," in forward
    assert "units = max(0.5, previous.size_units - 0.5)" in live_cycle


def test_activation_does_not_add_broker_or_execution_channel():
    workflow = (ROOT / ".github/workflows/live-track-daily.yml").read_text().lower()
    assert "broker" not in workflow
    assert "commit_active_daily" not in workflow
