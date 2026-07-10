#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone
from typing import Any
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

REPORT_JSON = ROOT / "docs/research/E1R_4C2C4E_ENGINE_C_NO_STRATEGY_DATA_HARNESS_SMOKE.json"
REPORT_MD = ROOT / "docs/research/E1R_4C2C4E_ENGINE_C_NO_STRATEGY_DATA_HARNESS_SMOKE.md"
ARCH_MD = ROOT / "docs/architecture/E1R_HISTORICAL_DATA_HARNESS_SMOKE_CONTRACT.md"
DATABUNDLE_SAMPLE_JSON = ROOT / "exports/e1r_engine/audit/e1r_engine_c_databundle_sample.json"

ENGINE_A_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_A_STANDALONE_ENGINE_ARCHITECTURE_CONTRACT.json"
ENGINE_B_REPORT = ROOT / "docs/research/E1R_4C2C4E_ENGINE_B_R1_NORMALIZED_INPUT_DATA_ADAPTER_CONTRACT_AUDIT.json"

BACKTEST_PATH = ROOT / "src/engine/backtest.py"
SIDECAR_PATH = ROOT / "src/engine/e1r_sidecar_sleeve.py"
COMPOSER_PATH = ROOT / "src/engine/e1r_composer.py"

FROZEN_STRATEGY_FILES = [
    BACKTEST_PATH,
    SIDECAR_PATH,
    COMPOSER_PATH,
]

RESEARCH_STOCK_DIR = ROOT / "data/research/e1_5y/raw/stocks"
RESEARCH_INDEX_DIR = ROOT / "data/research/e1_5y/raw/indices"
REGIME_PATH = ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json"
PROD_PRICE_DIR = ROOT / "data/prices"

INDEX_SYMBOLS = ["SPX", "NDX", "SOX"]
VIX_CANDIDATES = [
    RESEARCH_INDEX_DIR / "VIX.json",
    RESEARCH_INDEX_DIR / "_VIX.json",
    PROD_PRICE_DIR / "_VIX.json",
]

INVALID_ARTIFACTS = [
    "exports/e1r_unified_5y_full_account_v1_result.json",
    "exports/e1r_unified_5y_dashboard_research_bundle.json",
    "exports/e1r_combined_5y_original_max3_result.json",
    "exports/e1r_combined_5y_original_max3_equity_curve.json",
    "exports/e1r_combined_5y_original_max3_summary.json",
]

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except Exception:
        return str(path)

def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def read_json(path: Path) -> Any:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def parse_bar_date(row: dict[str, Any]) -> str | None:
    for key in ["date", "Date", "timestamp", "time"]:
        if key in row and row[key] is not None:
            return str(row[key])[:10]
    return None

def parse_bar_float(row: dict[str, Any], keys: list[str]) -> float | None:
    for key in keys:
        if key in row and row[key] is not None:
            try:
                return float(row[key])
            except Exception:
                return None
    return None

def extract_bars_from_json(path: Path) -> dict[str, Any]:
    raw = read_json(path)

    meta: dict[str, Any] = {
        "path": rel(path),
        "raw_type": type(raw).__name__,
    }

    bars: list[Any] = []

    if isinstance(raw, dict):
        meta["top_level_keys"] = sorted(raw.keys())
        meta["symbol"] = raw.get("symbol") or path.stem
        meta["schema_version"] = raw.get("schema_version")
        meta["data_start"] = raw.get("data_start")
        meta["data_end"] = raw.get("data_end")
        meta["dataset_mode"] = raw.get("dataset_mode")
        meta["source"] = raw.get("source")

        if isinstance(raw.get("bars"), list):
            bars = raw["bars"]
            meta["bar_source"] = "dict.bars"
        else:
            for key in ["data", "prices", "records", "rows", "history", "historical"]:
                if isinstance(raw.get(key), list):
                    bars = raw[key]
                    meta["bar_source"] = f"dict.{key}"
                    break

        if not bars and "dates" in raw and "closes" in raw:
            dates = raw["dates"]
            closes = raw["closes"]
            out = []
            for d, c in zip(dates, closes):
                out.append({
                    "date": str(d)[:10],
                    "close": float(c),
                })
            bars = out
            meta["bar_source"] = "dict.dates_closes"

    elif isinstance(raw, list):
        bars = raw
        meta["symbol"] = path.stem
        meta["bar_source"] = "list"

    parsed = []
    rejected = 0

    for row in bars:
        if not isinstance(row, dict):
            rejected += 1
            continue

        d = parse_bar_date(row)
        close = parse_bar_float(row, ["close", "Close", "adj_close", "Adj Close", "adjClose", "c"])
        if d is None or close is None:
            rejected += 1
            continue

        parsed.append({
            "date": d,
            "open": parse_bar_float(row, ["open", "Open", "o"]),
            "high": parse_bar_float(row, ["high", "High", "h"]),
            "low": parse_bar_float(row, ["low", "Low", "l"]),
            "close": close,
            "volume": parse_bar_float(row, ["volume", "Volume", "v"]),
        })

    parsed.sort(key=lambda x: x["date"])

    meta["raw_bar_count"] = len(bars)
    meta["parsed_bar_count"] = len(parsed)
    meta["rejected_bar_count"] = rejected
    meta["first_date"] = parsed[0]["date"] if parsed else None
    meta["last_date"] = parsed[-1]["date"] if parsed else None
    meta["sample_bar"] = parsed[0] if parsed else None

    return {
        "meta": meta,
        "bars": parsed,
    }

def build_series_from_bars(parsed: dict[str, Any]) -> tuple[list[str], list[float], list[dict[str, Any]]]:
    bars = parsed["bars"]
    dates = [b["date"] for b in bars]
    closes = [float(b["close"]) for b in bars]
    return dates, closes, bars

def load_stock_universe_sample(limit: int | None = None) -> dict[str, Any]:
    if not RESEARCH_STOCK_DIR.exists():
        raise FileNotFoundError(f"missing research stock dir: {rel(RESEARCH_STOCK_DIR)}")

    symbols: list[str] = []
    prices_map: dict[str, list[float]] = {}
    dates_map: dict[str, list[str]] = {}
    ohlc_map: dict[str, list[dict[str, Any]]] = {}
    meta_by_symbol: dict[str, Any] = {}
    skipped: dict[str, str] = {}

    files = sorted(RESEARCH_STOCK_DIR.glob("*.json"))

    for path in files:
        sym = path.stem.replace("_", ".")
        if sym.upper() == "VIXY":
            skipped[sym] = "excluded_vixy"
            continue

        try:
            parsed = extract_bars_from_json(path)
            dates, closes, bars = build_series_from_bars(parsed)
        except Exception as e:
            skipped[sym] = f"parse_error:{type(e).__name__}:{e}"
            continue

        if len(dates) < 120:
            skipped[sym] = f"too_few_bars:{len(dates)}"
            continue

        symbols.append(sym)
        dates_map[sym] = dates
        prices_map[sym] = closes
        ohlc_map[sym] = bars
        meta_by_symbol[sym] = parsed["meta"]

        if limit and len(symbols) >= limit:
            break

    return {
        "symbols": symbols,
        "prices_map": prices_map,
        "dates_map": dates_map,
        "ohlc_map": ohlc_map,
        "meta": {
            "stock_dir": rel(RESEARCH_STOCK_DIR),
            "files_seen": len(files),
            "symbols_loaded": len(symbols),
            "symbols_skipped": len(skipped),
            "skipped_sample": dict(list(skipped.items())[:20]),
            "first_symbols": symbols[:20],
            "meta_sample": {s: meta_by_symbol[s] for s in symbols[:5]},
        },
    }

def load_index_series(symbol: str) -> dict[str, Any]:
    path = RESEARCH_INDEX_DIR / f"{symbol}.json"
    if not path.exists():
        return {
            "symbol": symbol,
            "exists": False,
            "path": rel(path),
        }

    parsed = extract_bars_from_json(path)
    dates, closes, bars = build_series_from_bars(parsed)
    return {
        "symbol": symbol,
        "exists": True,
        "path": rel(path),
        "dates": dates,
        "closes": closes,
        "bars": bars,
        "meta": parsed["meta"],
    }

def load_vix_series() -> dict[str, Any]:
    for path in VIX_CANDIDATES:
        if path.exists():
            parsed = extract_bars_from_json(path)
            dates, closes, bars = build_series_from_bars(parsed)
            return {
                "symbol": "VIX",
                "exists": True,
                "path": rel(path),
                "dates": dates,
                "closes": closes,
                "bars": bars,
                "meta": parsed["meta"],
            }

    return {
        "symbol": "VIX",
        "exists": False,
        "path": None,
    }

def normalize_regime_value(v: Any) -> dict[str, Any]:
    if isinstance(v, dict):
        return {
            "spx_regime": v.get("spx_regime") or v.get("regime") or v.get("state") or v.get("market_regime"),
            "subclass": v.get("subclass") or v.get("sideways_subclass") or v.get("regime_subclass") or v.get("market_subclass"),
            "raw": v,
        }
    if isinstance(v, str):
        return {
            "spx_regime": v,
            "subclass": None,
            "raw": v,
        }
    return {
        "spx_regime": None,
        "subclass": None,
        "raw": v,
    }

def load_regime_daily() -> dict[str, Any]:
    if not REGIME_PATH.exists():
        return {
            "exists": False,
            "path": rel(REGIME_PATH),
            "records": {},
            "meta": {},
        }

    raw = read_json(REGIME_PATH)
    records: dict[str, Any] = {}

    if isinstance(raw, dict):
        date_keys = [
            k for k in raw.keys()
            if isinstance(k, str) and len(k) >= 10 and k[:4].isdigit() and k[4] == "-"
        ]
        if date_keys:
            for k in date_keys:
                records[k[:10]] = normalize_regime_value(raw[k])
        else:
            for key in ["records", "data", "regimes", "daily"]:
                if isinstance(raw.get(key), list):
                    for row in raw[key]:
                        if isinstance(row, dict):
                            d = parse_bar_date(row)
                            if d:
                                records[d] = normalize_regime_value(row)
                    break
    elif isinstance(raw, list):
        for row in raw:
            if isinstance(row, dict):
                d = parse_bar_date(row)
                if d:
                    records[d] = normalize_regime_value(row)

    regime_counts = Counter()
    subclass_counts = Counter()

    for row in records.values():
        regime_counts[str(row.get("spx_regime") or "UNKNOWN")] += 1
        subclass_counts[str(row.get("subclass") or "NO_SUBCLASS")] += 1

    dates = sorted(records.keys())

    return {
        "exists": True,
        "path": rel(REGIME_PATH),
        "records": records,
        "meta": {
            "record_count": len(records),
            "first_date": dates[0] if dates else None,
            "last_date": dates[-1] if dates else None,
            "regime_counts": dict(regime_counts),
            "subclass_counts": dict(subclass_counts),
            "sample": {d: records[d] for d in dates[:5]},
        },
    }

def common_dates_count(date_lists: list[list[str]]) -> dict[str, Any]:
    if not date_lists:
        return {
            "count": 0,
            "first": None,
            "last": None,
        }

    sets = [set(x) for x in date_lists if x]
    if not sets:
        return {
            "count": 0,
            "first": None,
            "last": None,
        }

    common = sorted(set.intersection(*sets))
    return {
        "count": len(common),
        "first": common[0] if common else None,
        "last": common[-1] if common else None,
        "sample": common[:5],
    }

def build_databundle_sample(stock_bundle: dict[str, Any], indices: dict[str, Any], vix: dict[str, Any], regime: dict[str, Any]) -> dict[str, Any]:
    symbols = stock_bundle["symbols"]
    sample_symbols = symbols[:5]

    sample_dates = []
    if "SPX" in indices and indices["SPX"].get("exists"):
        sample_dates = indices["SPX"]["dates"][-5:]

    return {
        "schema": "E1RDataBundleSampleV1",
        "generated_at": now(),
        "mode": "HISTORICAL_SMOKE_ONLY",
        "source": {
            "stocks": rel(RESEARCH_STOCK_DIR),
            "indices": rel(RESEARCH_INDEX_DIR),
            "regime": rel(REGIME_PATH),
        },
        "universe": {
            "count": len(symbols),
            "sample_symbols": sample_symbols,
        },
        "series_summary": {
            "stocks": stock_bundle["meta"],
            "indices": {
                k: {
                    "exists": v.get("exists"),
                    "path": v.get("path"),
                    "count": len(v.get("dates", [])),
                    "first_date": v.get("dates", [None])[0] if v.get("dates") else None,
                    "last_date": v.get("dates", [None])[-1] if v.get("dates") else None,
                    "meta": v.get("meta"),
                }
                for k, v in indices.items()
            },
            "vix": {
                "exists": vix.get("exists"),
                "path": vix.get("path"),
                "count": len(vix.get("dates", [])),
                "first_date": vix.get("dates", [None])[0] if vix.get("dates") else None,
                "last_date": vix.get("dates", [None])[-1] if vix.get("dates") else None,
            },
            "regime": regime["meta"],
        },
        "normalized_shapes": {
            "symbols": "list[str]",
            "prices_map": "dict[str, list[float]]",
            "dates_map": "dict[str, list[str]]",
            "ohlc_map": "dict[str, list[DailyBar]]",
            "indices": "dict[index_symbol, dates/closes/bars]",
            "regime_daily": "dict[date, {spx_regime, subclass, raw}]",
        },
        "sample_payload": {
            "dates": sample_dates,
            "stock_samples": {
                sym: {
                    "dates_tail": stock_bundle["dates_map"][sym][-5:],
                    "closes_tail": stock_bundle["prices_map"][sym][-5:],
                    "ohlc_tail": stock_bundle["ohlc_map"][sym][-2:],
                }
                for sym in sample_symbols
            },
            "index_samples": {
                k: {
                    "dates_tail": v.get("dates", [])[-5:],
                    "closes_tail": v.get("closes", [])[-5:],
                }
                for k, v in indices.items()
            },
            "regime_tail": {
                d: regime["records"].get(d)
                for d in sorted(regime["records"].keys())[-5:]
            } if regime.get("records") else {},
        },
    }

def main() -> None:
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    if not ENGINE_A_REPORT.exists():
        raise FileNotFoundError(f"Missing ENGINE-A report: {rel(ENGINE_A_REPORT)}")
    if not ENGINE_B_REPORT.exists():
        raise FileNotFoundError(f"Missing ENGINE-B-R1 report: {rel(ENGINE_B_REPORT)}")

    stock_bundle = load_stock_universe_sample(limit=None)

    indices = {}
    for sym in INDEX_SYMBOLS:
        indices[sym] = load_index_series(sym)

    vix = load_vix_series()
    regime = load_regime_daily()

    date_alignment = {
        "spx_vs_indices": common_dates_count([
            indices[sym]["dates"]
            for sym in INDEX_SYMBOLS
            if indices.get(sym, {}).get("exists")
        ]),
        "sample_stocks_vs_spx": common_dates_count(
            [indices["SPX"]["dates"]] +
            [stock_bundle["dates_map"][sym] for sym in stock_bundle["symbols"][:20]]
            if indices.get("SPX", {}).get("exists")
            else [stock_bundle["dates_map"][sym] for sym in stock_bundle["symbols"][:20]]
        ),
        "spx_vs_regime": common_dates_count([
            indices["SPX"]["dates"] if indices.get("SPX", {}).get("exists") else [],
            sorted(regime["records"].keys()) if regime.get("records") else [],
        ]),
    }

    databundle_sample = build_databundle_sample(stock_bundle, indices, vix, regime)
    write_json(DATABUNDLE_SAMPLE_JSON, databundle_sample)

    required_index_ok = all(indices[sym].get("exists") and len(indices[sym].get("dates", [])) >= 120 for sym in INDEX_SYMBOLS)

    validations = {
        "no_strategy_data_harness_only": True,
        "strategy_logic_changed": False,
        "backtest_engine_run": False,
        "full_5y_backtest_run": False,
        "forward_runner_run": False,
        "provider_extraction_run": False,
        "adapter_implementation_run": False,
        "official_result_generated": False,
        "dashboard_changed": False,
        "strategy_files_unchanged": before_hashes == {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES},
        "invalid_artifacts_not_used_as_source": True,
        "composer_not_used": True,
        "return_curve_stitching_not_used": True,
        "engine_a_loaded": True,
        "engine_b_loaded": True,
        "research_stock_bars_schema_parsed": stock_bundle["meta"]["symbols_loaded"] > 0,
        "stock_symbols_loaded_ge_500": stock_bundle["meta"]["symbols_loaded"] >= 500,
        "prices_map_built": bool(stock_bundle["prices_map"]),
        "dates_map_built": bool(stock_bundle["dates_map"]),
        "ohlc_map_built": bool(stock_bundle["ohlc_map"]),
        "indices_loaded": required_index_ok,
        "regime_loaded": regime["meta"].get("record_count", 0) > 0,
        "date_alignment_available": date_alignment["sample_stocks_vs_spx"]["count"] > 0,
        "databundle_sample_written": DATABUNDLE_SAMPLE_JSON.exists(),
        "historical_adapter_not_implemented_yet": True,
        "strategy_core_extraction_not_allowed_yet": True,
    }

    decision = {
        "data_harness_smoke_passed": all([
            validations["research_stock_bars_schema_parsed"],
            validations["stock_symbols_loaded_ge_500"],
            validations["prices_map_built"],
            validations["dates_map_built"],
            validations["ohlc_map_built"],
            validations["indices_loaded"],
            validations["regime_loaded"],
            validations["date_alignment_available"],
        ]),
        "selected_loader_basis": {
            "research_bars_parser": "canonical parser should support dict.bars schema found in data/research/e1_5y/raw/stocks and raw/indices",
            "historical_input_fields": [
                "symbols",
                "prices_map",
                "dates_map",
                "ohlc_map",
                "spx_prices/spx_dates",
                "ndx_prices/ndx_dates",
                "sox_prices/sox_dates",
                "vix_prices/vix_dates optional explicit",
                "regime_daily",
            ],
        },
        "historical_adapter_implementation_allowed_next": True,
        "strategy_core_extraction_allowed_now": False,
        "full_5y_backtest_allowed_now": False,
        "forward_runner_allowed_now": False,
        "conclusion": (
            "NO_STRATEGY_DATA_HARNESS_SMOKE_PASS_READY_FOR_HISTORICAL_ADAPTER_SKELETON"
            if all([
                validations["research_stock_bars_schema_parsed"],
                validations["stock_symbols_loaded_ge_500"],
                validations["prices_map_built"],
                validations["dates_map_built"],
                validations["ohlc_map_built"],
                validations["indices_loaded"],
                validations["regime_loaded"],
                validations["date_alignment_available"],
            ])
            else "NO_STRATEGY_DATA_HARNESS_SMOKE_NEEDS_REVIEW"
        ),
        "recommended_next_action": (
            "Proceed to 4C-2C-4E-ENGINE-D: implement HistoricalDataAdapter skeleton and unit smoke only. "
            "Do not implement strategy core yet."
        ),
        "engineering_rule": (
            "HistoricalDataAdapter may normalize data into DataBundle/MarketSnapshot. "
            "It must not decide BUY/SELL, sizing, market gate, regime branch execution, or account state transitions."
        ),
    }

    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "4C-2C-4E-ENGINE-C",
        "status": "NO_STRATEGY_DATA_HARNESS_SMOKE_COMPLETE",
        "purpose": "Verify real 5Y research data can be normalized into the standalone E1R engine input shape without strategy execution.",
        "policy": {
            "strategy_logic_changed": False,
            "no_strategy_data_harness_only": True,
            "backtest_engine_run": False,
            "full_5y_backtest_run": False,
            "forward_runner_run": False,
            "provider_extraction_run": False,
            "adapter_implementation_run": False,
            "official_result_generated": False,
            "dashboard_changed": False,
            "frozen_strategy_files_changed": before_hashes != after_hashes,
            "invalid_artifacts_used_as_source": False,
            "composer_used": False,
            "return_curve_stitching_used": False,
        },
        "stock_universe_summary": stock_bundle["meta"],
        "index_summary": {
            k: {
                "exists": v.get("exists"),
                "path": v.get("path"),
                "count": len(v.get("dates", [])),
                "first_date": v.get("dates", [None])[0] if v.get("dates") else None,
                "last_date": v.get("dates", [None])[-1] if v.get("dates") else None,
                "meta": v.get("meta"),
            }
            for k, v in indices.items()
        },
        "vix_summary": {
            "exists": vix.get("exists"),
            "path": vix.get("path"),
            "count": len(vix.get("dates", [])),
            "first_date": vix.get("dates", [None])[0] if vix.get("dates") else None,
            "last_date": vix.get("dates", [None])[-1] if vix.get("dates") else None,
        },
        "regime_summary": regime["meta"],
        "date_alignment": date_alignment,
        "databundle_sample_path": rel(DATABUNDLE_SAMPLE_JSON),
        "databundle_sample_sha256": sha256(DATABUNDLE_SAMPLE_JSON),
        "validations": validations,
        "decision": decision,
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R 4C-2C-4E-ENGINE-C — No-Strategy Data Harness Smoke")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Purpose")
    md.append("")
    md.append(report["purpose"])
    md.append("")
    md.append("## Policy")
    md.append("```json")
    md.append(json.dumps(report["policy"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Stock Universe Summary")
    md.append("```json")
    md.append(json.dumps(report["stock_universe_summary"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Index Summary")
    md.append("```json")
    md.append(json.dumps(report["index_summary"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Regime Summary")
    md.append("```json")
    md.append(json.dumps(report["regime_summary"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Date Alignment")
    md.append("```json")
    md.append(json.dumps(report["date_alignment"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## DataBundle Sample")
    md.append("")
    md.append(f"- Path: `{report['databundle_sample_path']}`")
    md.append(f"- SHA256: `{report['databundle_sample_sha256']}`")
    md.append("")
    md.append("## Validations")
    md.append("```json")
    md.append(json.dumps(validations, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Decision")
    md.append("```json")
    md.append(json.dumps(decision, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")

    REPORT_MD.write_text("\n".join(md))
    ARCH_MD.write_text("\n".join(md))

    print("E1R_4C2C4E_ENGINE_C_NO_STRATEGY_DATA_HARNESS_SMOKE_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("stock_universe_summary:", json.dumps(report["stock_universe_summary"], ensure_ascii=False))
    print("index_summary:", json.dumps(report["index_summary"], ensure_ascii=False))
    print("vix_summary:", json.dumps(report["vix_summary"], ensure_ascii=False))
    print("regime_summary:", json.dumps(report["regime_summary"], ensure_ascii=False))
    print("date_alignment:", json.dumps(report["date_alignment"], ensure_ascii=False))
    print("databundle_sample:", json.dumps({
        "path": report["databundle_sample_path"],
        "sha256": report["databundle_sample_sha256"],
    }, ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("decision:", json.dumps(decision, ensure_ascii=False))
    print("conclusion:", decision["conclusion"])
    print("recommended_next_action:", decision["recommended_next_action"])
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))
    print("wrote:", rel(ARCH_MD))
    print("wrote:", rel(DATABUNDLE_SAMPLE_JSON))

if __name__ == "__main__":
    main()
