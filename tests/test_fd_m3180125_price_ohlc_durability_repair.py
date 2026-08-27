from __future__ import annotations

import importlib.util
import hashlib
import json
from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[1]
UPDATERS = (
    ROOT / "scripts/update_engine_forward_prices.py",
    ROOT / "scripts/update_fd_m3180125_live_adjusted_prices.py",
)


def load_updater(path: Path):
    sys.modules.setdefault("yfinance", types.SimpleNamespace())
    sys.modules.setdefault(
        "pandas",
        types.SimpleNamespace(
            DataFrame=object,
            MultiIndex=object,
            isna=lambda value: value != value,
        ),
    )
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def frame(row: dict[str, object]):
    item = types.SimpleNamespace(**row)
    return types.SimpleNamespace(
        itertuples=lambda index=False: [item]
    )


def test_incomplete_provider_bar_never_overwrites_last_known_good() -> None:
    existing = [{
        "date": "2026-08-26",
        "open": 15.65,
        "high": 15.74,
        "low": 15.21,
        "close": 15.21,
        "volume": 0.0,
    }]
    incomplete = frame({
        "date": "2026-08-26",
        "open": 0.0,
        "high": 0.0,
        "low": 0.0,
        "close": 15.21,
        "volume": 0.0,
    })
    for path in UPDATERS:
        module = load_updater(path)
        assert module.merge_records(existing, incomplete) == existing


def test_incomplete_new_bar_does_not_advance_freshness_date() -> None:
    existing = [{
        "date": "2026-08-25",
        "open": 15.71,
        "high": 16.30,
        "low": 15.13,
        "close": 15.45,
        "volume": 0.0,
    }]
    incomplete = frame({
        "date": "2026-08-26",
        "open": float("nan"),
        "high": float("nan"),
        "low": float("nan"),
        "close": 15.21,
        "volume": 0.0,
    })
    for path in UPDATERS:
        module = load_updater(path)
        merged = module.merge_records(existing, incomplete)
        assert merged[-1]["date"] == "2026-08-25"


def test_valid_overlap_repairs_preexisting_invalid_bar() -> None:
    existing = [{
        "date": "2026-08-26",
        "open": 0.0,
        "high": 0.0,
        "low": 0.0,
        "close": 15.21,
        "volume": 0.0,
    }]
    repaired = frame({
        "date": "2026-08-26",
        "open": 15.65,
        "high": 15.74,
        "low": 15.21,
        "close": 15.21,
        "volume": 0.0,
    })
    for path in UPDATERS:
        module = load_updater(path)
        merged = module.merge_records(existing, repaired)
        assert module.invalid_ohlc_dates(merged) == []
        assert merged[0]["open"] == 15.65


def test_invalid_range_is_rejected_with_rounding_tolerance() -> None:
    invalid = {
        "date": "2026-08-26",
        "open": 15.65,
        "high": 15.50,
        "low": 15.21,
        "close": 15.60,
    }
    rounding_only = {
        "date": "2023-11-24",
        "open": 31.286467886165337,
        "high": 31.382614135742184,
        "low": 31.13263168619579,
        "close": 31.382614135742188,
    }
    for path in UPDATERS:
        module = load_updater(path)
        assert module.valid_ohlc_record(invalid) is False
        assert module.valid_ohlc_record(rounding_only) is True


def test_current_price_roots_contain_only_valid_ohlc() -> None:
    targets = (
        (UPDATERS[0], ROOT / "data/fw_prices"),
        (
            UPDATERS[1],
            ROOT / "data/live_prices_adjusted_v1/live_prices",
        ),
    )
    for updater_path, price_root in targets:
        module = load_updater(updater_path)
        invalid = {}
        for price_path in sorted(price_root.glob("*.json")):
            dates = module.invalid_ohlc_dates(
                module.load_existing(price_path)
            )
            if dates:
                invalid[price_path.name] = dates
        assert invalid == {}


def test_live_status_hash_matches_repaired_vix_file() -> None:
    vix_path = (
        ROOT / "data/live_prices_adjusted_v1/live_prices/VIX.json"
    )
    status_path = (
        ROOT
        / "exports/official/FD-M3180125-SP500-TOP3-engine"
        / "live/automation/parity/current_adjusted_accepted.json"
    )
    status = json.loads(status_path.read_text(encoding="utf-8"))
    assert status["file_hashes"]["VIX"] == hashlib.sha256(
        vix_path.read_bytes()
    ).hexdigest()
