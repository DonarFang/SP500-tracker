from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.engine.e1r_sidecar_sleeve import E1RSidecarConfig, build_e1r_sidecar_sleeve


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def pick(obj: Any, keys: list[str], default: Any = None) -> Any:
    if not isinstance(obj, dict):
        return default
    for k in keys:
        v = obj.get(k)
        if v not in (None, ""):
            return v
    return default


def normalize_e1r_state(regime: str, subclass: str) -> str:
    r = (regime or "UNKNOWN").upper()
    s = (subclass or "").upper()

    if "UP" in r:
        return "UPTREND"
    if "DOWN" in r:
        return "DOWNTREND"
    if "SIDE" in r:
        if "MA_CONFLICT" in s:
            return "SIDEWAYS_MA_CONFLICT"
        if "DETERIOR" in s:
            return "SIDEWAYS_DETERIORATION"
        if "RECOVER" in s:
            return "SIDEWAYS_RECOVERY"
        return "SIDEWAYS"
    return "UNKNOWN"


def extract_latest_regime(regime_json: Any) -> dict[str, Any]:
    daily = regime_json.get("daily_regime") if isinstance(regime_json, dict) else regime_json

    if isinstance(daily, list):
        rows = [r for r in daily if isinstance(r, dict)]
        if not rows:
            raise RuntimeError("daily_regime list is empty")
        rows = sorted(rows, key=lambda r: str(r.get("date", "")))
        return rows[-1]

    if isinstance(daily, dict):
        keys = sorted(daily.keys())
        if not keys:
            raise RuntimeError("daily_regime dict is empty")
        k = keys[-1]
        row = daily[k]
        if not isinstance(row, dict):
            row = {"value": row}
        row = dict(row)
        row.setdefault("date", k)
        return row

    raise RuntimeError("Unsupported spx_regime_daily.json structure")


def extract_legacy_market_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}

    raw = read_json(path)
    market = raw.get("market", raw) if isinstance(raw, dict) else {}

    return {
        "date": pick(market, ["date", "data_date", "as_of"], pick(raw, ["generated_at_display", "generated_at"], None) if isinstance(raw, dict) else None),
        "state": pick(market, ["state", "market_state", "trend_state", "regime"], None),
        "state_zh": pick(market, ["state_zh"], None),
        "market_score": pick(market, ["market_score"], None),
        "leadership_confirmed": pick(market, ["leadership_confirmed"], None),
        "leadership_label": pick(market, ["leadership_label"], None),
    }


def simplify_holding(h: dict[str, Any]) -> dict[str, Any]:
    return {
        "symbol": h.get("symbol"),
        "score": h.get("score"),
        "weight": h.get("weight"),
        "raw_return": h.get("raw_return"),
        "contribution": h.get("contribution"),
    }


def main() -> None:
    regime_path = ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json"
    stock_dir = ROOT / "data/research/e1_5y/raw/stocks"
    spx_path = ROOT / "data/research/e1_5y/raw/indices/SPX.json"
    legacy_market_path = ROOT / "exports/market_state.json"
    out_path = ROOT / "exports/e1r_v0_2_status.json"

    regime_json = read_json(regime_path)
    latest = extract_latest_regime(regime_json)

    date = str(pick(latest, ["date", "as_of", "data_date"], "UNKNOWN"))
    regime = str(pick(latest, ["regime", "market_regime", "state"], "UNKNOWN")).upper()
    subclass = str(pick(latest, ["subclass", "regime_subclass", "market_subclass", "sideways_subclass"], "") or "").upper()
    e1r_market_state = normalize_e1r_state(regime, subclass)

    config = E1RSidecarConfig(
        start_date="2021-06-11",
        end_date=date,
        allowed_subclasses=("MA_CONFLICT",),
        top_n=10,
        gross_exposure=0.25,
        min_history_days=200,
        min_price=5.0,
        initial_equity=100000.0,
        excluded_symbols=("VIXY",),
    )

    sidecar_result = build_e1r_sidecar_sleeve(
        stock_dir=stock_dir,
        spx_path=spx_path,
        regime_path=regime_path,
        config=config,
    )

    records = sidecar_result.get("records", []) or []
    last_record = None

    for r in records:
        if r.get("date") == date or r.get("next_date") == date:
            last_record = r

    if last_record is None and records:
        last_record = records[-1]

    holdings = []
    if isinstance(last_record, dict):
        raw_holdings = (
            last_record.get("holdings")
            or last_record.get("selected")
            or last_record.get("selected_holdings")
            or []
        )
        if isinstance(raw_holdings, list):
            holdings = [simplify_holding(h) for h in raw_holdings if isinstance(h, dict)]

    sidecar_active = e1r_market_state == "SIDEWAYS_MA_CONFLICT" and len(holdings) > 0
    core_active = e1r_market_state == "UPTREND"

    status = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "version": "E1R-v0.2-formal-sidecar-sleeve",
        "research_status": "FORMAL_SIDECAR_SLEEVE_ENGINE",
        "status_date": date,
        "e1r_market_state": e1r_market_state,
        "regime": regime,
        "subclass": subclass or None,
        "mutually_exclusive_state_model": True,
        "core": {
            "strategy_id": "E1R_REGIME_AWARE_V0_1",
            "active": core_active,
            "active_condition": "UPTREND",
        },
        "sidecar": {
            "active": sidecar_active,
            "active_condition": "SIDEWAYS_MA_CONFLICT",
            "gross_exposure": 0.25,
            "top_n": 10,
            "excluded_symbols": ["VIXY"],
            "selected_count": len(holdings),
            "selected": holdings,
            "source_record_date": last_record.get("date") if isinstance(last_record, dict) else None,
            "source_record_next_date": last_record.get("next_date") if isinstance(last_record, dict) else None,
        },
        "legacy_market_state": extract_legacy_market_state(legacy_market_path),
        "source_files": {
            "regime": str(regime_path.relative_to(ROOT)),
            "stocks": str(stock_dir.relative_to(ROOT)),
            "spx": str(spx_path.relative_to(ROOT)),
            "legacy_market_state": str(legacy_market_path.relative_to(ROOT)),
        },
        "notes": [
            "E1R v0.2 uses mutually exclusive daily market states.",
            "Core is active only in UPTREND under the current v0.2 state model.",
            "Sidecar is active only in SIDEWAYS_MA_CONFLICT when holdings are available.",
            "This status export is a lightweight bridge for Dashboard and future OOS integration.",
        ],
    }

    write_json(out_path, status)

    print("Wrote", out_path)
    print("status_date:", status["status_date"])
    print("e1r_market_state:", status["e1r_market_state"])
    print("regime:", status["regime"])
    print("subclass:", status["subclass"])
    print("core.active:", status["core"]["active"])
    print("sidecar.active:", status["sidecar"]["active"])
    print("sidecar.selected_count:", status["sidecar"]["selected_count"])


if __name__ == "__main__":
    main()
