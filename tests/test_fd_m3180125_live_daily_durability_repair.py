"""Pure-stdlib contract tests for the Live daily durability repair."""

import ast
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import sys
import types


ROOT = Path(__file__).resolve().parents[1]
UPDATER = (ROOT / "scripts/update_fd_m3180125_live_adjusted_prices.py").read_text()
RUNNER = (ROOT / "scripts/run_fd_m3180125_live_daily.py").read_text()
COMPOSITION = (ROOT / "src/e1r_engine/live_composition.py").read_text()
WORKFLOW = (ROOT / ".github/workflows/live-track-daily.yml").read_text()
SHADOW = (ROOT / "scripts/build_fd_m3180125_live_adjusted_shadow.py").read_text()


def test_d01_repair_sources_parse():
    for source in (UPDATER, RUNNER, COMPOSITION):
        ast.parse(source)


def test_d02_live_adjusted_root_is_the_only_price_root():
    assert '"live_prices_adjusted_v1" / "live_prices"' in UPDATER
    assert '"fw_prices"' not in UPDATER
    assert '"data/live_prices"' not in UPDATER


def test_d03_catalogue_is_frozen_at_491_plus_four_indices():
    assert "EXPECTED_STOCK_COUNT = 491" in UPDATER
    assert "EXPECTED_FILE_COUNT = EXPECTED_STOCK_COUNT + len(INDEX_TICKERS)" in UPDATER


def test_d04_required_indices_are_exact():
    for row in ('"SPX": "^GSPC"', '"NDX": "^NDX"', '"SOX": "^SOX"', '"VIX": "^VIX"'):
        assert row in UPDATER


def test_d05_excluded_etfs_are_rejected():
    assert 'frozenset({"QQQ", "SOXX", "VIXY"})' in UPDATER
    assert "contains excluded ETF symbols" in UPDATER


def test_d06_adjusted_price_semantics_are_explicit():
    assert UPDATER.count("auto_adjust=True") >= 2
    assert '"auto_adjust": True' in UPDATER


def test_d07_overlap_matches_working_forward_contract():
    forward = (ROOT / "scripts/update_engine_forward_prices.py").read_text()
    assert "LOOKBACK_DAYS = 10" in UPDATER
    assert "LOOKBACK_DAYS = 10" in forward


def test_d08_future_provider_rows_are_clipped():
    assert 'frame["date"] <= expected_latest_market_date' in UPDATER


def test_d09_four_index_freshness_is_fail_closed():
    assert "HOLD_LIVE_ADJUSTED_REQUIRED_INDEX_FRESHNESS" in UPDATER
    assert "return 2" in UPDATER


def test_d10_incremental_update_preserves_catalogue_and_publishes(tmp_path):
    pandas = types.ModuleType("pandas")
    pandas.DataFrame = type("DataFrame", (), {})
    pandas.MultiIndex = type("MultiIndex", (), {})
    pandas.isna = lambda value: value is None
    yfinance = types.ModuleType("yfinance")
    previous_pandas = sys.modules.get("pandas")
    previous_yfinance = sys.modules.get("yfinance")
    sys.modules["pandas"] = pandas
    sys.modules["yfinance"] = yfinance
    try:
        spec = importlib.util.spec_from_file_location("live_incremental_under_test", ROOT / "scripts/update_fd_m3180125_live_adjusted_prices.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        if previous_pandas is None:
            sys.modules.pop("pandas", None)
        else:
            sys.modules["pandas"] = previous_pandas
        if previous_yfinance is None:
            sys.modules.pop("yfinance", None)
        else:
            sys.modules["yfinance"] = previous_yfinance

    price_root = tmp_path / "data" / "live_prices_adjusted_v1" / "live_prices"
    price_root.mkdir(parents=True)
    symbols = ["S%03d" % index for index in range(491)] + ["SPX", "NDX", "SOX", "VIX"]
    old = [{"date": "2026-08-24", "open": 10, "high": 11, "low": 9, "close": 10, "volume": 100}]
    for symbol in symbols:
        (price_root / (symbol + ".json")).write_text(json.dumps(old), encoding="utf-8")
    module.PRICE_ROOT = price_root
    module.STATUS_PATH = tmp_path / "accepted.json"
    module.download_bulk = lambda requested, start, end: {symbol: object() for symbol in requested}
    module.download_single = lambda symbol, start, end: None
    module.clip_frame_to_expected_session = lambda frame, expected: frame
    module.merge_records = lambda existing, frame: existing + [{"date": "2026-08-25", "open": 11, "high": 12, "low": 10, "close": 11, "volume": 101}]
    previous_argv = sys.argv
    try:
        sys.argv = ["updater", "--expected-latest-market-date", "2026-08-25"]
        with redirect_stdout(io.StringIO()):
            assert module.main() == 0
    finally:
        sys.argv = previous_argv
    status = json.loads(module.STATUS_PATH.read_text(encoding="utf-8"))
    assert status["decision"] == "PASS_LIVE_ADJUSTED_DAILY_INCREMENTAL_PRICE_UPDATE"
    assert status["stock_symbol_count"] == 491
    assert status["latest_market_date"] == "2026-08-25"
    assert len(list(price_root.glob("*.json"))) == 495


def test_d11_existing_history_is_merged_by_date():
    assert 'rows = {str(row["date"]): dict(row) for row in existing}' in UPDATER
    assert "for key in sorted(rows)" in UPDATER


def test_d12_publish_uses_complete_staging_and_rollback():
    assert "def promote_complete_staging(" in UPDATER
    assert "os.replace(price_root, backup)" in UPDATER
    assert "os.replace(staging_root, price_root)" in UPDATER


def test_d13_daily_workflow_uses_incremental_accepted_updater():
    update_at = WORKFLOW.index("scripts/update_fd_m3180125_live_adjusted_prices.py")
    live_at = WORKFLOW.index("name: Run ACTIVE Personal Live daily")
    assert update_at < live_at


def test_d14_daily_workflow_does_not_update_legacy_raw_prices():
    assert "python scripts/update_fd_m3180125_live_prices.py" not in WORKFLOW
    assert "git add -f data/live_prices/" not in WORKFLOW


def test_d15_shadow_build_cannot_overwrite_active_adjusted_root():
    assert "--shadow-root data/live_prices_adjusted_shadow_v1/live_prices" in WORKFLOW
    assert '("live_prices_adjusted_shadow_v1", "live_prices")' in SHADOW


def test_d16_push_cannot_run_active_live():
    active = WORKFLOW[WORKFLOW.index("name: Run ACTIVE Personal Live daily"):]
    active_condition = active.splitlines()[1]
    assert "schedule" in active_condition and "workflow_dispatch" in active_condition
    assert "push" not in active_condition


def test_d17_runner_resolves_and_processes_all_pending_sessions():
    assert "pending_dates=[]" in RUNNER
    assert "for run_market_date in pending_dates" in RUNNER
    assert '"catchup_market_dates"' in RUNNER


def test_d18_runner_verifies_existing_daily_continuity():
    assert 'LIVE_ROOT/"runtime/daily"/verify_date.isoformat()/"manifest.json"' in RUNNER
    assert "HOLD_LIVE_DAILY_CONTINUITY" in RUNNER


def test_d19_confirmed_live_execution_and_isolation_contracts_remain():
    production = (ROOT / "src/e1r_engine/live_production.py").read_text()
    assert '"automatic_execution_enabled": False' in production
    assert "broker" not in WORKFLOW.lower()
    assert "data/fw_prices/" in WORKFLOW
    assert "fd-m3180125-production-main-writer" in WORKFLOW
