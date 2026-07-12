from pathlib import Path


def test_backtest_contains_frozen_sideways_execution_contract():
    source = Path("src/engine/backtest.py").read_text(encoding="utf-8")
    for token in [
        "e1r_sideways_execution_enabled",
        "def _e1r_subclass_on",
        "_sideways_tradable_cash_base",
        "_sideways_budget_spent",
        "sideways_ma_conflict_deactivated",
        "target_fraction_of_tradable_cash",
        "capital_fraction_of_tradable_cash",
        'action_priority = {"EXIT": 0, "REDUCE": 1',
    ]:
        assert token in source


def test_uptrend_adapter_remains_sideways_free():
    source = Path("src/e1r_engine/uptrend_execution_adapter.py").read_text(encoding="utf-8")
    assert "SIDEWAYS_MA_CONFLICT" not in source
