import ast
from pathlib import Path

import pytest

from e1r_engine.universe_versioning.shadow_integration import (
    ShadowIntegrationError,
    ShadowObserverConfig,
)


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "src/e1r_engine/universe_versioning/shadow_integration.py"
FORWARD = ROOT / "scripts/run_engine_forward_daily.py"
LIVE = ROOT / "scripts/run_fd_m3180125_live_daily.py"
WHITELIST = (
    "docs/canonical/FD-M3180125_SP500_UNIVERSE_VERSIONING_CONTRACT.md",
    "scripts/run_engine_forward_daily.py",
    "src/e1r_engine/forward_orchestrator.py",
    "scripts/run_fd_m3180125_live_daily.py",
    "src/e1r_engine/universe_versioning/shadow_integration.py",
    "tests/test_fd_m3180125_universe_shadow_contract.py",
    "tests/test_fd_m3180125_universe_shadow_forward.py",
    "tests/test_fd_m3180125_universe_shadow_live.py",
    "tests/test_fd_m3180125_universe_shadow_isolation.py",
    "tests/test_fd_m3180125_universe_shadow_zero_impact.py",
)


def test_S301_exact_source_whitelist_is_frozen():
    contract = (ROOT / "docs/canonical/FD-M3180125_SP500_UNIVERSE_VERSIONING_CONTRACT.md").read_text()
    assert "UV-step-3" in contract
    assert "PRODUCTION INACTIVE" in contract
    assert "a3f14b45cf4e2d5746ad67d972fba4dc680904db" in contract
    assert all(path in contract for path in WHITELIST)


def test_S302_high_risk_components_are_not_imported_by_shadow_module():
    source = MODULE.read_text()
    for token in ("E1RCoreEngine", "LiveEngineAdapter", "T1ExecutionEngine", "live_account_adapter"):
        assert token not in source


def test_S303_shadow_is_default_off():
    forward = FORWARD.read_text()
    live = LIVE.read_text()
    assert 'parser.add_argument("--uv-shadow-probe", action="store_true")' in forward
    assert 'parser.add_argument("--uv-shadow-probe",action="store_true")' in live
    assert "shadow_observer = None" in forward


def test_S304_no_production_consumer_imports_shadow_evidence():
    allowed = {MODULE.resolve(), FORWARD.resolve(), LIVE.resolve()}
    roots = (
        ROOT / "src/e1r_engine",
        ROOT / "scripts",
        ROOT / ".github/workflows",
    )
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.resolve() in allowed:
                continue
            if path.suffix not in {".py", ".yml", ".yaml", ".js", ".html"}:
                continue
            source = path.read_text(encoding="utf-8")
            assert "universe_versioning.shadow_integration" not in source
            assert "dashboard_projection_shadow.json" not in source


def test_S305_no_forbidden_fallback_in_shadow_module():
    source = MODULE.read_text().lower()
    tree = ast.parse(source)
    imported = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    assert not ({"urllib", "requests"} & imported)
    for token in ("data/research/e1_5y", "data/oos", "screening/", "next_weekday"):
        assert token not in source


def test_S306_new_shadow_sources_parse_and_compile():
    for path in (MODULE, FORWARD, LIVE, ROOT / "src/e1r_engine/forward_orchestrator.py"):
        ast.parse(path.read_text())
    with pytest.raises(ShadowIntegrationError, match="Git SHA-1"):
        ShadowObserverConfig(ROOT, "forward", "z" * 40, "2026-08-10T00:00:00Z")
