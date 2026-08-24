"""F01-F08: Forward preservation assertions."""

from pathlib import Path
import hashlib


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "src/e1r_engine/forward_runtime.py").read_text(encoding="utf-8")
RUNNER = (ROOT / "scripts/run_engine_forward_daily.py").read_text(encoding="utf-8")


def test_f01_forward_runtime_remains_present():
    assert "class ForwardRuntimeState" in SOURCE


def test_f02_forward_add_persists_half_unit_step():
    assert 'metadata.get("size_units", 1.0)' in SOURCE
    assert '"add_size_units"' in SOURCE


def test_f03_forward_reduce_has_minimum_half_unit():
    assert 'metadata["size_units"] = max(' in SOURCE
    assert "0.5," in SOURCE


def test_f04_forward_execution_priority_preserved():
    assert '"EXIT": 0' in SOURCE and '"REDUCE": 1' in SOURCE


def test_f05_forward_fractional_execution_preserved():
    assert "requested_units" in SOURCE


def test_f06_forward_runner_not_given_live_price_switch():
    assert "FD_M3180125_LIVE_PRICE_MODE" not in RUNNER


def test_f07_forward_universe_exclusions_preserved():
    assert all(symbol in RUNNER for symbol in ("QQQ", "SOXX", "VIXY"))


def test_f08_forward_history_is_not_a_parity_write_target():
    contract = (ROOT / "docs/contracts/FD-M3180125_PARITY_REPAIR_CONTRACT_v1.0.md").read_text()
    assert "no Forward or Live history rewrite" in contract


def test_i01_no_backtest_path_is_in_repair_contract():
    contract = (ROOT / "docs/contracts/FD-M3180125_PARITY_REPAIR_CONTRACT_v1.0.md").read_text()
    assert "no 5Y execution or rewrite" in contract


def test_i02_live_runner_defaults_to_adjusted_accepted():
    runner = (ROOT / "scripts/run_fd_m3180125_live_daily.py").read_text()
    assert '"ADJUSTED_ACCEPTED").strip().upper()' in runner


def test_i03_adjusted_mode_requires_accepted_evidence():
    runner = (ROOT / "scripts/run_fd_m3180125_live_daily.py").read_text()
    assert 'PRICE_MODE=="ADJUSTED_ACCEPTED"' in runner
    assert 'status.get("production_activation") is not True' in runner


def test_i04_shadow_workflow_skips_active_live_run():
    workflow = (ROOT / ".github/workflows/live-track-daily.yml").read_text()
    assert "github.event_name == 'schedule'" in workflow
    assert "github.event_name == 'push'" in workflow


def test_i05_shadow_workflow_has_no_broker_step():
    workflow = (ROOT / ".github/workflows/live-track-daily.yml").read_text().lower()
    assert "broker" not in workflow


def test_i06_repair_code_has_no_ntap_or_hpe_special_case():
    files = [
        ROOT / "src/e1r_engine/live_cycle_state.py",
        ROOT / "src/e1r_engine/canonical_runtime.py",
        ROOT / "scripts/record_fd_m3180125_live_interaction.py",
    ]
    body = "\n".join(path.read_text() for path in files)
    assert "NTAP" not in body and "HPE" not in body


def test_i07_existing_transaction_ledger_is_byte_preserved():
    path = ROOT / "exports/official/FD-M3180125-SP500-TOP3-engine/live/runtime/history/transactions.jsonl"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == "b935e0dac96a35671f4b0267b48f484256fab5b93a278b858508958b9f5ccc96"


def test_i08_existing_journal_is_byte_preserved():
    path = ROOT / "exports/official/FD-M3180125-SP500-TOP3-engine/live/runtime/history/ledger_journal.jsonl"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == "a00ded3e7628b0743d022754df42e1dc82bd6b13879649d8e709341f0e9a666a"
