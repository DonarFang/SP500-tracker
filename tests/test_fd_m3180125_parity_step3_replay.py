from datetime import date
import json
from pathlib import Path

from e1r_engine.parity_step3_replay import (
    build_causal_live_projection, causal_rows, compare_contract,
    normalize_forward, normalize_live, protected_hashes, validate_actions,
)


def test_causal_rows_exclude_future_transaction():
    rows = [{"trade_date": "2026-08-13"}, {"trade_date": "2026-08-17"}]
    assert causal_rows(rows, date(2026, 8, 13)) == [rows[0]]


def test_causal_rows_exclude_future_cash_control():
    rows = [{"effective_date": "2026-08-14"}, {"effective_date": "2026-08-15"}]
    assert causal_rows(rows, date(2026, 8, 14)) == [rows[0]]


def test_projection_renumbers_journal_and_preserves_source(tmp_path: Path):
    source, target = tmp_path / "source", tmp_path / "live"
    for rel in ("contracts/live_runtime_contract.json", "runtime/current/runtime_state.json"):
        path = source / rel; path.parent.mkdir(parents=True, exist_ok=True); path.write_text("{}")
    history = source / "runtime/history"; history.mkdir(parents=True)
    tx = [{"trade_date": "2026-08-13"}, {"trade_date": "2026-08-17"}]
    cash = [{"effective_date": "2026-08-14"}]
    journal = [{"sequence": 4, "event": {"trade_date": "2026-08-13"}}, {"sequence": 5, "event": {"trade_date": "2026-08-17"}}]
    for name, rows in (("transactions.jsonl", tx), ("cash_control.jsonl", cash), ("ledger_journal.jsonl", journal)):
        (history / name).write_text("".join(json.dumps(x) + "\n" for x in rows))
    before = protected_hashes(source)
    counts = build_causal_live_projection(source, target, date(2026, 8, 14))
    assert counts == {"transactions": 1, "cash_controls": 1, "journal_events": 1}
    assert json.loads((target / "runtime/history/ledger_journal.jsonl").read_text())["sequence"] == 1
    assert protected_hashes(source) == before


def test_normalizers_compare_account_independent_contract():
    trace = {"market_regime": "UPTREND", "branch": "UPTREND", "inputs": {"market_state": "FULL_ON", "gate_state": "ALLOW", "entry_capacity": 3}, "metadata": {"route": {"subclass": "NO_SUBCLASS"}, "reference_top3": [{"symbol": "A"}]}}
    live = {"regime": "UPTREND", "regime_subclass": "NO_SUBCLASS", "market_state": "FULL_ON", "market_gate": "ALLOW", "entry_capacity": 3, "strategy_branch": "UPTREND", "reference_top3": [{"symbol": "A"}]}
    assert compare_contract(normalize_live(live), normalize_forward(trace))["decision"] == "PASS"


def test_contract_mismatch_fails_closed():
    assert compare_contract({"market_gate": "ALLOW"}, {"market_gate": "RISK_OFF"})["decision"] == "FAIL"


def test_action_contract_accepts_reduce_without_target():
    assert validate_actions({"position_recommendations": [{"symbol": "A", "action": "REDUCE", "target_shares": None}]}) == []


def test_action_contract_rejects_unknown_action():
    assert validate_actions({"position_recommendations": [{"symbol": "A", "action": "SELL_ALL"}]})


def test_action_contract_rejects_reduce_target():
    assert validate_actions({"position_recommendations": [{"symbol": "A", "action": "REDUCE", "target_shares": 1}]})
