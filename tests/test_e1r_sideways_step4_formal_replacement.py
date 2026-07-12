from pathlib import Path


def test_formal_stateful_variant_is_registered_and_selected():
    source = Path("src/engine/backtest.py").read_text(encoding="utf-8")
    assert '"E1R_REGIME_AWARE_V0_2_STATEFUL_MAX3"' in source
    assert '"e1r_sideways_execution_enabled": True' in source
    assert '_formal_stateful_id = "E1R_REGIME_AWARE_V0_2_STATEFUL_MAX3"' in source


def test_legacy_sidecar_is_reference_only():
    source = Path("src/engine/backtest.py").read_text(encoding="utf-8")
    assert "E1R_REGIME_AWARE_V0_2_LEGACY_SIDECAR_REFERENCE" in source
    assert "LEGACY_VIRTUAL_SIDECAR_REFERENCE_NOT_FORMAL" in source
    assert '"formal_selection_eligible"] = False' in source


def test_acceptance_telemetry_is_present():
    source = Path("src/engine/backtest.py").read_text(encoding="utf-8")
    for token in (
        '"origin_branch":        h.get("origin_branch") or "UPTREND"',
        '"entry_tradable_cash_base"',
        '"entry_sideways_total_budget"',
        '"entry_target_cash"',
        '"total_cost_basis"',
        '"total_realized_pnl"',
        '"uptrend_positions_count"',
        '"sideways_positions_count"',
        '"position_origin_counts"',
        '"sideways_positions_value"',
        '"e1r_sideways_execution_enabled": e1r_sideways_execution_enabled',
        '"entry_signal_date"',
        '"entry_signal_regime"',
        '"entry_signal_subclass"',
        '"entry_execution_date"',
        '"resolved_assumptions"',
    ):
        assert token in source
