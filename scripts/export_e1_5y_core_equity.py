#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import sys
from datetime import datetime, timezone
from collections import Counter
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

START_DATE = "2021-06-11"
END_DATE = "2026-06-18"
INITIAL_CAPITAL = 100000.0

STOCK_DIR = ROOT / "data/research/e1_5y/raw/stocks"
INDEX_DIR = ROOT / "data/research/e1_5y/raw/indices"

OUT_JSON = ROOT / "exports/e1_5y_backtest_equity_curve.json"
REPORT_JSON = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3C_E1_CORE_EXPORT_REPORT.json"
REPORT_MD = ROOT / "docs/research/E1R_V0_2_STAGE3_8E2F2C4C10F3C_E1_CORE_EXPORT_REPORT.md"

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))

def read_json(path: Path) -> Any:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def as_float(x: Any) -> float | None:
    if x is None:
        return None
    try:
        return float(x)
    except Exception:
        return None

def normalize_date(x: Any) -> str | None:
    if x is None:
        return None
    s = str(x)
    if len(s) >= 10 and s[4:5] == "-" and s[7:8] == "-":
        return s[:10]
    return None

def extract_records(obj: Any) -> list[dict[str, Any]]:
    if isinstance(obj, list):
        if obj and isinstance(obj[0], dict):
            return obj
        return []

    if isinstance(obj, dict):
        for key in [
            "bars",
            "data",
            "prices",
            "records",
            "rows",
            "history",
            "ohlc",
            "series",
        ]:
            v = obj.get(key)
            if isinstance(v, list) and (not v or isinstance(v[0], dict)):
                return v

        # Some files are keyed by date.
        keyed = []
        for k, v in obj.items():
            if normalize_date(k) and isinstance(v, dict):
                row = dict(v)
                row.setdefault("date", normalize_date(k))
                keyed.append(row)
        if keyed:
            return keyed

    return []

def extract_close(row: dict[str, Any]) -> float | None:
    for key in [
        "close",
        "adj_close",
        "adjClose",
        "Adj Close",
        "Close",
        "price",
        "value",
    ]:
        value = as_float(row.get(key))
        if value is not None:
            return value
    return None

def extract_ohlc(row: dict[str, Any]) -> dict[str, float | None]:
    return {
        "open": as_float(row.get("open", row.get("Open"))),
        "high": as_float(row.get("high", row.get("High"))),
        "low": as_float(row.get("low", row.get("Low"))),
        "close": extract_close(row),
        "volume": as_float(row.get("volume", row.get("Volume"))),
    }

def load_series(path: Path) -> tuple[list[str], list[float], list[dict[str, Any]]]:
    obj = read_json(path)
    records = extract_records(obj)

    rows = []
    for r in records:
        if not isinstance(r, dict):
            continue

        d = normalize_date(
            r.get("date")
            or r.get("Date")
            or r.get("timestamp")
            or r.get("datetime")
        )
        c = extract_close(r)
        if d and c is not None:
            ohlc = extract_ohlc(r)
            ohlc["date"] = d
            rows.append((d, c, ohlc))

    rows = sorted(rows, key=lambda x: x[0])
    dates = [x[0] for x in rows]
    prices = [x[1] for x in rows]
    ohlc_rows = [x[2] for x in rows]
    return dates, prices, ohlc_rows

def load_index(symbol: str) -> tuple[list[str], list[float]]:
    candidates = [
        INDEX_DIR / f"{symbol}.json",
        INDEX_DIR / f"^{symbol}.json",
        ROOT / f"data/prices/{symbol}.json",
        ROOT / f"data/prices/^{symbol}.json",
    ]

    for p in candidates:
        if p.exists():
            dates, prices, _ = load_series(p)
            if dates and prices:
                return dates, prices

    raise FileNotFoundError(f"Cannot load index series for {symbol}. Tried: {[str(x) for x in candidates]}")

def rows_to_ohlc_columns(ohlc_rows: list[dict[str, Any]]) -> dict[str, list[float | None]]:
    return {
        "open": [r.get("open") for r in ohlc_rows],
        "high": [r.get("high") for r in ohlc_rows],
        "low": [r.get("low") for r in ohlc_rows],
        "close": [r.get("close") for r in ohlc_rows],
        "volume": [r.get("volume") for r in ohlc_rows],
    }

def load_stocks() -> tuple[list[str], dict[str, list[float]], dict[str, list[str]], dict[str, dict[str, list[float | None]]], list[dict[str, Any]]]:
    symbols: list[str] = []
    prices_map: dict[str, list[float]] = {}
    dates_map: dict[str, list[str]] = {}
    ohlc_map: dict[str, dict[str, list[float | None]]] = {}
    rejected: list[dict[str, Any]] = []

    for p in sorted(STOCK_DIR.glob("*.json")):
        symbol = p.stem
        if symbol.upper() == "VIXY":
            rejected.append({"symbol": symbol, "reason": "excluded_known_non_sp500_proxy"})
            continue

        try:
            dates, prices, ohlc_rows = load_series(p)
        except Exception as exc:
            rejected.append({"symbol": symbol, "reason": type(exc).__name__ + ": " + str(exc)})
            continue

        if len(dates) < 180:
            rejected.append({"symbol": symbol, "reason": f"too_few_rows:{len(dates)}"})
            continue

        symbols.append(symbol)
        prices_map[symbol] = prices
        dates_map[symbol] = dates
        ohlc_map[symbol] = rows_to_ohlc_columns(ohlc_rows)

    return symbols, prices_map, dates_map, ohlc_map, rejected

def find_lists(obj: Any, prefix: str = "root") -> list[tuple[str, list[Any]]]:
    found = []
    if isinstance(obj, list):
        found.append((prefix, obj))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}"
            if isinstance(v, list):
                found.append((p, v))
            elif isinstance(v, dict):
                found.extend(find_lists(v, p))
    return found

def shape_rows(rows: list[Any], label: str) -> dict[str, Any]:
    keys = set()
    dates = []
    equity_values = []

    for r in rows:
        if not isinstance(r, dict):
            continue
        keys.update(r.keys())

        d = normalize_date(r.get("date") or r.get("interval_end_date") or r.get("next_date"))
        if d:
            dates.append(d)

        eq = as_float(r.get("total_equity", r.get("equity", r.get("portfolio_value"))))
        if eq is not None:
            equity_values.append(eq)

    dc = Counter(dates)
    has_symbol = "symbol" in keys
    has_equity = bool({"total_equity", "equity", "portfolio_value"} & keys)
    one_row_per_date = bool(dc) and max(dc.values()) == 1

    return {
        "label": label,
        "length": len(rows),
        "keys": sorted(keys),
        "date_start": min(dates) if dates else None,
        "date_end": max(dates) if dates else None,
        "unique_dates": len(dc),
        "max_rows_per_date": max(dc.values()) if dc else None,
        "has_symbol_level_rows": has_symbol,
        "has_equity_or_portfolio_value": has_equity,
        "one_row_per_date": one_row_per_date,
        "equity_count": len(equity_values),
        "first_equity": equity_values[0] if equity_values else None,
        "last_equity": equity_values[-1] if equity_values else None,
        "continuity_candidate": (
            len(dc) >= 1000
            and one_row_per_date
            and has_equity
            and not has_symbol
            and (min(dates) <= "2021-07-15" if dates else False)
            and (max(dates) >= "2026-06-01" if dates else False)
        ),
    }

def normalize_equity_rows(result: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any] | None, list[dict[str, Any]]]:
    candidates = []

    for path, rows in find_lists(result):
        if rows and isinstance(rows[0], dict):
            shape = shape_rows(rows, path)
            candidates.append({"path": path, "rows": rows, "shape": shape})

    accepted = [c for c in candidates if c["shape"]["continuity_candidate"]]
    if not accepted:
        return [], None, [c["shape"] for c in candidates]

    best = sorted(
        accepted,
        key=lambda c: (c["shape"]["unique_dates"], c["shape"]["length"]),
        reverse=True,
    )[0]

    clean = []
    rows = sorted(best["rows"], key=lambda r: normalize_date(r.get("date") or r.get("interval_end_date") or r.get("next_date")) or "")

    for r in rows:
        d = normalize_date(r.get("date") or r.get("interval_end_date") or r.get("next_date"))
        eq = as_float(r.get("total_equity", r.get("equity", r.get("portfolio_value"))))
        if not d or eq is None:
            continue

        clean.append({
            "date": d,
            "equity": eq,
            "portfolio_value": eq,
            "strategy_indexed": eq / INITIAL_CAPITAL * 100.0,
            "cash": r.get("cash"),
            "market_value": r.get("market_value", r.get("positions_value", r.get("position_value", r.get("holdings_value")))),
            "n_positions": r.get("n_positions", r.get("open_positions_count", r.get("n_holdings"))),
            "daily_return": r.get("daily_return"),
            "daily_return_pct": r.get("daily_return_pct"),
            "market_state": r.get("market_state", r.get("market_gate_state", r.get("regime"))),
            "source_row_keys": sorted(r.keys()),
        })

    return clean, best["shape"], [c["shape"] for c in candidates]

def main() -> int:
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "src"))

    from src.engine import backtest

    symbols, prices_map, dates_map, ohlc_map, rejected = load_stocks()
    spx_dates, spx_prices = load_index("SPX")

    ndx_dates = ndx_prices = sox_dates = sox_prices = vix_dates = vix_prices = None

    try:
        ndx_dates, ndx_prices = load_index("NDX")
    except Exception:
        pass
    try:
        sox_dates, sox_prices = load_index("SOX")
    except Exception:
        pass
    try:
        vix_dates, vix_prices = load_index("VIX")
    except Exception:
        pass

    assumptions = None
    for name in ["ASSUMPTIONS", "DEFAULT_ASSUMPTIONS"]:
        value = getattr(backtest, name, None)
        if isinstance(value, dict):
            assumptions = dict(value)
            break

    try:
        result = backtest.run_stateful_simulation(
            symbols=symbols,
            prices_map=prices_map,
            dates_map=dates_map,
            spx_prices=spx_prices,
            spx_dates=spx_dates,
            ohlc_map=ohlc_map,
            assumptions=assumptions,
            step=1,
            min_history=120,
            market_score_default=60.0,
            sim_start_date=START_DATE,
            sim_end_date=END_DATE,
            ndx_prices=ndx_prices,
            ndx_dates=ndx_dates,
            sox_prices=sox_prices,
            sox_dates=sox_dates,
            vix_prices=vix_prices,
            vix_dates=vix_dates,
        )
    except Exception as exc:
        report = {
            "generated_at": now(),
            "stage": "B_STAGE_3_8E2F2C4C10F3C_E1_CORE_EXPORT",
            "status": "E1_5Y_CORE_CANONICAL_NOT_READY",
            "policy": {
                "dashboard_changed": False,
                "workflow_changed": False,
                "strategy_logic_changed": False,
                "frozen_strategy_imported_only": True,
                "canonical_e1_written": False,
            },
            "input_summary": {
                "symbols_loaded": len(symbols),
                "symbols_rejected": len(rejected),
                "rejected_sample": rejected[:20],
                "spx_dates": len(spx_dates),
                "spx_start": spx_dates[0] if spx_dates else None,
                "spx_end": spx_dates[-1] if spx_dates else None,
                "ndx_loaded": bool(ndx_dates),
                "sox_loaded": bool(sox_dates),
                "vix_loaded": bool(vix_dates),
                "assumptions_source": "ASSUMPTIONS/DEFAULT_ASSUMPTIONS" if assumptions else "run_stateful_default",
                "ohlc_contract": "dict[symbol] -> dict[open/high/low/close/volume] -> list",
            },
            "error": type(exc).__name__ + ": " + str(exc),
            "diagnosis": [
                "Export-only wrapper called frozen run_stateful_simulation but it raised before producing candidate equity rows.",
                "No canonical E1 export was written.",
            ],
            "canonical_written": False,
        }
        write_json(REPORT_JSON, report)
        REPORT_MD.write_text("# Stage 3.8E-2F-2C-4C-10F-3C E1 Core Export Report\n\nStatus: `E1_5Y_CORE_CANONICAL_NOT_READY`\n\nError: `" + report["error"] + "`\n")
        print("E1 5Y core export wrapper failed before candidate extraction")
        print("status:", report["status"])
        print("error:", report["error"])
        print("symbols_loaded:", len(symbols))
        print("report_json:", rel(REPORT_JSON))
        print("report_md:", rel(REPORT_MD))
        return 2

    rows, chosen_shape, candidate_shapes = normalize_equity_rows(result)

    validation = {
        "row_count": len(rows),
        "unique_dates": len({r["date"] for r in rows}),
        "date_start": rows[0]["date"] if rows else None,
        "date_end": rows[-1]["date"] if rows else None,
        "one_row_per_date": len(rows) == len({r["date"] for r in rows}) if rows else False,
        "full_window": bool(rows) and rows[0]["date"] <= "2021-07-15" and rows[-1]["date"] >= "2026-06-01",
        "capital_continuity_candidate": bool(rows) and len(rows) == len({r["date"] for r in rows}),
        "chosen_shape": chosen_shape,
    }

    write_canonical = (
        validation["row_count"] >= 1000
        and validation["one_row_per_date"]
        and validation["full_window"]
        and validation["capital_continuity_candidate"]
    )

    canonical = None
    if write_canonical:
        canonical = {
            "strategy_id": "E1_AUDITED_G4_MINHOLD10",
            "artifact_type": "canonical_continuous_capital_e1_5y_core_equity_curve",
            "generated_at": now(),
            "capital_model": "continuous_single_account",
            "initial_capital": INITIAL_CAPITAL,
            "simulation_start_date": rows[0]["date"],
            "simulation_end_date": rows[-1]["date"],
            "row_count": len(rows),
            "unique_dates": len({r["date"] for r in rows}),
            "source": "src.engine.backtest.run_stateful_simulation",
            "parameters": {
                "sim_start_date": START_DATE,
                "sim_end_date": END_DATE,
                "step": 1,
                "min_history": 120,
                "market_score_default": 60.0,
                "symbols": len(symbols),
                "stock_dir": rel(STOCK_DIR),
                "index_dir": rel(INDEX_DIR),
            },
            "rows": rows,
        }
        write_json(OUT_JSON, canonical)

    report = {
        "generated_at": now(),
        "stage": "B_STAGE_3_8E2F2C4C10F3C_E1_CORE_EXPORT",
        "status": "E1_5Y_CORE_CANONICAL_WRITTEN" if write_canonical else "E1_5Y_CORE_CANONICAL_NOT_READY",
        "policy": {
            "dashboard_changed": False,
            "workflow_changed": False,
            "strategy_logic_changed": False,
            "frozen_strategy_imported_only": True,
            "canonical_e1_written": write_canonical,
        },
        "input_summary": {
            "symbols_loaded": len(symbols),
            "symbols_rejected": len(rejected),
            "rejected_sample": rejected[:20],
            "spx_dates": len(spx_dates),
            "spx_start": spx_dates[0] if spx_dates else None,
            "spx_end": spx_dates[-1] if spx_dates else None,
            "ndx_loaded": bool(ndx_dates),
            "sox_loaded": bool(sox_dates),
            "vix_loaded": bool(vix_dates),
            "assumptions_source": "ASSUMPTIONS/DEFAULT_ASSUMPTIONS" if assumptions else "run_stateful_default",
        },
        "result_top_keys": sorted(result.keys()) if isinstance(result, dict) else None,
        "candidate_shapes": candidate_shapes[:80],
        "validation": validation,
        "canonical_path": rel(OUT_JSON),
        "canonical_written": write_canonical,
        "diagnosis": [
            "Called frozen run_stateful_simulation through an export-only wrapper.",
            "Used explicit 5Y window and one continuous capital account validation.",
            "Wrote E1 canonical only if row-count, one-row-per-date, full-window and continuity-candidate checks passed.",
        ],
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# Stage 3.8E-2F-2C-4C-10F-3C E1 Core Export Report")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append("")
    md.append("## Status")
    md.append("")
    md.append(f"- Status: `{report['status']}`")
    md.append(f"- Canonical E1 written: `{write_canonical}`")
    md.append(f"- Symbols loaded: `{len(symbols)}`")
    md.append("")
    md.append("## Validation")
    md.append("")
    md.append("```json")
    md.append(json.dumps(validation, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Input Summary")
    md.append("")
    md.append("```json")
    md.append(json.dumps(report["input_summary"], indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Candidate Shapes")
    md.append("")
    md.append("```json")
    md.append(json.dumps(candidate_shapes[:60], indent=2, ensure_ascii=False)[:18000])
    md.append("```")
    REPORT_MD.write_text("\n".join(md) + "\n")

    print("E1 5Y core export wrapper complete")
    print("status:", report["status"])
    print("symbols_loaded:", len(symbols))
    print("symbols_rejected:", len(rejected))
    print("result_top_keys:", report["result_top_keys"])
    print("validation:", json.dumps(validation, ensure_ascii=False))
    print("canonical_written:", write_canonical)
    print("canonical_path:", rel(OUT_JSON))
    print("report_json:", rel(REPORT_JSON))
    print("report_md:", rel(REPORT_MD))

    return 0 if write_canonical else 2

if __name__ == "__main__":
    raise SystemExit(main())
