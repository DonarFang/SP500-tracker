"""D01-D08: adjusted shadow and stock-universe contract."""

from datetime import date
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_fd_m3180125_live_adjusted_shadow import build_adjusted_shadow
from e1r_engine.live_composition import discover_live_stock_symbols
from update_fd_m3180125_live_prices import YahooDailyProvider


class Provider:
    def __init__(self): self.calls = []
    def fetch(self, **kwargs):
        self.calls.append(kwargs)
        return [{"date": "2026-01-02", "open": 1, "high": 2, "low": 1, "close": 2, "volume": 3}]


def _legacy(tmp_path):
    root = tmp_path / "live_prices"
    root.mkdir()
    row = [{"date": "2026-01-01", "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1}]
    for symbol in ("AAA", "QQQ", "SOXX", "VIXY", "SPX", "NDX", "SOX", "VIX"):
        (root / f"{symbol}.json").write_text(json.dumps(row))
    return root


def test_d01_yahoo_adjusted_provider_is_explicit():
    assert YahooDailyProvider(auto_adjust=True).auto_adjust is True


def test_d02_legacy_provider_default_is_not_silently_changed():
    assert YahooDailyProvider().auto_adjust is False


def test_d03_live_catalogue_excludes_three_etfs(tmp_path):
    root = _legacy(tmp_path)
    assert discover_live_stock_symbols(price_root=root, expected_stock_count=1) == ("AAA",)


def test_d04_adjusted_shadow_has_versioned_root(tmp_path):
    provider = Provider(); legacy = _legacy(tmp_path); shadow = tmp_path / "live_prices_adjusted_v1/live_prices"
    build_adjusted_shadow(legacy_root=legacy, shadow_root=shadow, end_date=date(2026, 1, 2), provider=provider)
    assert shadow.is_dir()


def test_d05_adjusted_shadow_does_not_write_legacy(tmp_path):
    provider = Provider(); legacy = _legacy(tmp_path); before = (legacy / "AAA.json").read_bytes()
    build_adjusted_shadow(legacy_root=legacy, shadow_root=tmp_path / "live_prices_adjusted_v1/live_prices", end_date=date(2026, 1, 2), provider=provider)
    assert (legacy / "AAA.json").read_bytes() == before


def test_d06_adjusted_shadow_excludes_etf_files(tmp_path):
    provider = Provider(); legacy = _legacy(tmp_path); shadow = tmp_path / "live_prices_adjusted_v1/live_prices"
    build_adjusted_shadow(legacy_root=legacy, shadow_root=shadow, end_date=date(2026, 1, 2), provider=provider)
    assert not any((shadow / f"{symbol}.json").exists() for symbol in ("QQQ", "SOXX", "VIXY"))


def test_d07_adjusted_shadow_reports_stock_count(tmp_path):
    result = build_adjusted_shadow(legacy_root=_legacy(tmp_path), shadow_root=tmp_path / "live_prices_adjusted_v1/live_prices", end_date=date(2026, 1, 2), provider=Provider())
    assert result["stock_symbol_count"] == 1


def test_d08_adjusted_shadow_uses_index_provider_symbols(tmp_path):
    provider = Provider()
    build_adjusted_shadow(legacy_root=_legacy(tmp_path), shadow_root=tmp_path / "live_prices_adjusted_v1/live_prices", end_date=date(2026, 1, 2), provider=provider)
    symbols = {call["provider_symbol"] for call in provider.calls}
    assert {"^GSPC", "^NDX", "^SOX", "^VIX"}.issubset(symbols)
