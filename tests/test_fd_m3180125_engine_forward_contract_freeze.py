from __future__ import annotations

import ast
import json
from pathlib import Path

from e1r_engine.forward_runtime import (
    FIRST_FORWARD_MARKET_DATE,
    SEED_DATE,
    ForwardSeedLoader,
)

ROOT = Path(__file__).resolve().parents[1]
FORWARD = (
    ROOT
    / "exports"
    / "official"
    / "FD-M3180125-SP500-TOP3-engine"
    / "forward"
)
ENGINE_SOURCE = ROOT / "src" / "e1r_engine"


def test_canonical_seed_loads() -> None:
    assert SEED_DATE == "2026-06-16"
    assert FIRST_FORWARD_MARKET_DATE == "2026-06-17"

    state = ForwardSeedLoader(FORWARD / "seed_2026-06-16").load()

    assert state.seed_date == "2026-06-16"
    assert state.first_forward_market_date == "2026-06-17"
    assert state.account.date == "2026-06-16"
    assert abs(state.account.cash - 77867.71) < 1e-8
    assert abs(state.account.positions_value - 232132.29618824524) < 0.02
    assert abs(state.account.total_equity - 310000.00618824525) < 0.02
    assert set(state.account.positions) == {"DELL", "HUM", "MRVL"}
    assert state.account.metadata["strategy_variant"] == "E1R_CAPPED_ATR_A0_V1"
    for position in state.account.positions.values():
        assert "capped_atr_stop" in position.metadata
    assert state.pending_orders == []


def test_current_manifest_and_superseded_guard() -> None:
    current = json.loads(
        (FORWARD / "current_seed_manifest.json").read_text(encoding="utf-8")
    )
    marker = json.loads(
        (
            FORWARD
            / "seed_2026-06-18"
            / "SUPERSEDED_BY_ENGINE_FORWARD_CONTRACT.json"
        ).read_text(encoding="utf-8")
    )

    assert current["seed_date"] == "2026-06-16"
    assert current["first_forward_market_date"] == "2026-06-17"
    assert current["legacy_oos_is_fact_source"] is False
    assert marker["status"] == "SUPERSEDED_AUDIT_ONLY"
    assert marker["must_not_be_loaded_as_current_seed"] is True


def test_engine_source_has_no_legacy_oos_dependency() -> None:
    forbidden = ("data/oos", "exports/oos_", "exports/e1r_v0_2_")
    hits: list[str] = []

    for path in sorted(ENGINE_SOURCE.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        ast.parse(text)
        for token in forbidden:
            if token in text:
                hits.append(f"{path.relative_to(ROOT)}:{token}")

    assert hits == []
