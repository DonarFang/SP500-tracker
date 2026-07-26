from datetime import date
from decimal import Decimal
import json
from pathlib import Path

from e1r_engine.live_composition import load_official_live_opening


def test_load_official_live_opening(tmp_path: Path) -> None:
    root = tmp_path / "live"
    contract = root / "contracts/live_runtime_contract.json"
    runtime = root / "runtime/current/runtime_state.json"
    contract.parent.mkdir(parents=True)
    runtime.parent.mkdir(parents=True)
    contract.write_text(json.dumps({
        "opening_date": "2026-07-27",
        "opening_cash": "100000.00",
        "positions": {},
        "opening_activated": True,
        "activation_required": False,
    }))
    runtime.write_text(json.dumps({
        "opening_date": "2026-07-27",
        "opening_cash": "100000.00",
        "opening_positions": {},
        "opening_activated": True,
        "activation_required": False,
    }))
    opening = load_official_live_opening(root)
    assert opening.opening_date == date(2026, 7, 27)
    assert opening.opening_cash == Decimal("100000.00")
    assert opening.positions == {}
