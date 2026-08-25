"""Execution-level regression guards added after the Parity audit."""

from e1r_engine.parity_step3_replay import (
    compare_contract,
    validate_forward_execution,
)


def test_step3_rejects_missing_t1_execution_bar():
    payload = {
        "skipped_orders": [
            {
                "symbol": "SNOW",
                "signal_date": "2026-08-04",
                "skip_reason": "MISSING_T1_BAR",
            }
        ]
    }
    assert validate_forward_execution(payload)


def test_step3_accepts_completed_execution():
    assert validate_forward_execution({"skipped_orders": []}) == []


def test_isolated_account_top3_difference_is_diagnostic_only():
    result = compare_contract(
        {"market_gate": "ALLOW", "reference_top3": ["AAA"]},
        {"market_gate": "ALLOW", "reference_top3": ["BBB"]},
    )
    assert result["decision"] == "PASS"
    assert result["reference_top3_diagnostic"]["equal"] is False
    assert result["reference_top3_diagnostic"]["parity_gating"] is False
