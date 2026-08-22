import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/canonical/FD-M3180125_SP500_UNIVERSE_VERSIONING_UV_STEP_4_CONTRACT_v1.0_FROZEN_2026-08-22.md"
WHITELIST = (
    "docs/canonical/FD-M3180125_SP500_UNIVERSE_VERSIONING_CONTRACT.md",
    "docs/canonical/FD-M3180125_SP500_UNIVERSE_VERSIONING_UV_STEP_4_CONTRACT_v1.0_FROZEN_2026-08-22.md",
    "src/e1r_engine/universe_versioning/production_integration.py",
    "src/e1r_engine/forward_orchestrator.py",
    "src/e1r_engine/live_composition.py",
    "scripts/run_engine_forward_daily.py",
    "scripts/run_fd_m3180125_live_daily.py",
    "scripts/activate_fd_m3180125_universe_production.py",
    "tests/test_fd_m3180125_universe_production_contract.py",
    "tests/test_fd_m3180125_universe_production_gate.py",
    "tests/test_fd_m3180125_universe_production_forward.py",
    "tests/test_fd_m3180125_universe_production_live.py",
    "tests/test_fd_m3180125_universe_production_isolation.py",
    "tests/test_fd_m3180125_universe_production_zero_impact.py",
)


def test_U401_contract_freezes_authority_and_exact_whitelist():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "a3f14b45cf4e2d5746ad67d972fba4dc680904db" in text
    assert all(path in text for path in WHITELIST)
    assert "119/119 PASS" in text


def test_U402_contract_freezes_buy_add_and_removed_holding_semantics():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "BUY`/`ADD`" in text
    assert "HOLD`/`REDUCE`/`EXIT`" in text
    assert "MUST NOT synthesize `EXIT`" in text
    assert "RequiredDataUniverse" in text


def test_U403_contract_freezes_default_off_independent_rollback_and_no_fallback():
    text = CONTRACT.read_text(encoding="utf-8")
    for token in ("`OFF` is the default", "activation is independent", "no permissive or static-universe fallback", "never deletes"):
        assert token in text


def test_U404_all_uv4_sources_parse():
    for raw in WHITELIST:
        path = ROOT / raw
        if path.suffix == ".py":
            ast.parse(path.read_text(encoding="utf-8"))
