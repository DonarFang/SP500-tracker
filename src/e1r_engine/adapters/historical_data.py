from __future__ import annotations

from pathlib import Path
import json
from collections import Counter
from typing import Any

from e1r_engine.contracts import (
    AssetSeries,
    DailyBar,
    HistoricalDataBundle,
    RegimeRecord,
    strict_common_dates,
)


class HistoricalDataAdapter:
    """
    Historical data adapter skeleton for standalone E1R Engine.

    Responsibility:
    - Read 5Y historical stock/index/regime data.
    - Normalize data into HistoricalDataBundle / MarketSnapshot-compatible shape.
    - Provide prices_map / dates_map / ohlc_map for legacy compatibility.

    Must not:
    - Decide BUY/SELL/HOLD/ADD/REDUCE/EXIT.
    - Apply sizing, market gate, regime routing, or account-state transitions.
    - Call run_stateful_simulation.
    - Use stitched or invalid artifacts.
    """

    def __init__(
        self,
        root: Path | str,
        stock_dir: Path | str | None = None,
        index_dir: Path | str | None = None,
        regime_path: Path | str | None = None,
        prod_price_dir: Path | str | None = None,
    ) -> None:
        self.root = Path(root)
        self.stock_dir = Path(stock_dir) if stock_dir else self.root / "data/research/e1_5y/raw/stocks"
        self.index_dir = Path(index_dir) if index_dir else self.root / "data/research/e1_5y/raw/indices"
        self.regime_path = Path(regime_path) if regime_path else self.root / "data/research/e1_5y/regimes/spx_regime_daily.json"
        self.prod_price_dir = Path(prod_price_dir) if prod_price_dir else self.root / "data/prices"

    def load_bundle(self, min_bars: int = 120, exclude_symbols: set[str] | None = None) -> HistoricalDataBundle:
        exclude_symbols = exclude_symbols or {"VIXY"}

        symbols: list[str] = []
        prices_map: dict[str, list[float]] = {}
        dates_map: dict[str, list[str]] = {}
        ohlc_map: dict[str, list[DailyBar]] = {}
        skipped: dict[str, str] = {}
        meta_by_symbol: dict[str, Any] = {}

        stock_files = sorted(self.stock_dir.glob("*.json"))

        for path in stock_files:
            sym = path.stem.replace("_", ".")

            if sym.upper() in exclude_symbols:
                skipped[sym] = "excluded"
                continue

            try:
                series = self.load_asset_series(path, symbol=sym)
            except Exception as exc:
                skipped[sym] = f"parse_error:{type(exc).__name__}:{exc}"
                continue

            if len(series.dates) < min_bars:
                skipped[sym] = f"too_few_bars:{len(series.dates)}"
                continue

            symbols.append(sym)
            prices_map[sym] = series.closes
            dates_map[sym] = series.dates
            ohlc_map[sym] = series.bars
            meta_by_symbol[sym] = series.meta

        indices = {
            symbol: self.load_asset_series(self.index_dir / f"{symbol}.json", symbol=symbol)
            for symbol in ["SPX", "NDX", "SOX"]
        }

        vix = self.load_vix_series()
        regime_daily = self.load_regime_daily()

        metadata = {
            "adapter": "HistoricalDataAdapter",
            "stock_dir": self._rel(self.stock_dir),
            "index_dir": self._rel(self.index_dir),
            "regime_path": self._rel(self.regime_path),
            "prod_price_dir": self._rel(self.prod_price_dir),
            "stock_files_seen": len(stock_files),
            "symbols_loaded": len(symbols),
            "symbols_skipped": len(skipped),
            "skipped_sample": dict(list(skipped.items())[:30]),
            "first_symbols": symbols[:20],
            "symbol_meta_sample": {s: meta_by_symbol[s] for s in symbols[:5]},
            "date_alignment": self.build_alignment_summary(symbols, dates_map, indices, regime_daily),
        }

        return HistoricalDataBundle(
            symbols=symbols,
            prices_map=prices_map,
            dates_map=dates_map,
            ohlc_map=ohlc_map,
            indices=indices,
            regime_daily=regime_daily,
            vix=vix,
            metadata=metadata,
        )

    def load_asset_series(self, path: Path, symbol: str | None = None) -> AssetSeries:
        raw = self._read_json(path)
        resolved_symbol = symbol or path.stem.replace("_", ".")

        meta: dict[str, Any] = {
            "path": self._rel(path),
            "raw_type": type(raw).__name__,
        }

        bars_raw: list[Any] = []

        if isinstance(raw, dict):
            resolved_symbol = str(raw.get("symbol") or resolved_symbol)
            meta.update({
                "top_level_keys": sorted(raw.keys()),
                "symbol": resolved_symbol,
                "schema_version": raw.get("schema_version"),
                "data_start": raw.get("data_start"),
                "data_end": raw.get("data_end"),
                "dataset_mode": raw.get("dataset_mode"),
                "source": raw.get("source"),
            })

            if isinstance(raw.get("bars"), list):
                bars_raw = raw["bars"]
                meta["bar_source"] = "dict.bars"
            else:
                for key in ["data", "prices", "records", "rows", "history", "historical"]:
                    if isinstance(raw.get(key), list):
                        bars_raw = raw[key]
                        meta["bar_source"] = f"dict.{key}"
                        break

            if not bars_raw and "dates" in raw and "closes" in raw:
                bars_raw = [
                    {"date": str(d)[:10], "close": float(c)}
                    for d, c in zip(raw["dates"], raw["closes"])
                ]
                meta["bar_source"] = "dict.dates_closes"

        elif isinstance(raw, list):
            bars_raw = raw
            meta.update({
                "symbol": resolved_symbol,
                "bar_source": "list",
            })

        bars: list[DailyBar] = []
        rejected = 0

        for row in bars_raw:
            if not isinstance(row, dict):
                rejected += 1
                continue

            d = self._parse_date(row)
            close = self._parse_float(row, ["close", "Close", "adj_close", "Adj Close", "adjClose", "c"])

            if d is None or close is None:
                rejected += 1
                continue

            bars.append(DailyBar(
                date=d,
                open=self._parse_float(row, ["open", "Open", "o"]),
                high=self._parse_float(row, ["high", "High", "h"]),
                low=self._parse_float(row, ["low", "Low", "l"]),
                close=close,
                volume=self._parse_float(row, ["volume", "Volume", "v"]),
            ))

        bars.sort(key=lambda x: x.date)

        meta.update({
            "raw_bar_count": len(bars_raw),
            "parsed_bar_count": len(bars),
            "rejected_bar_count": rejected,
            "first_date": bars[0].date if bars else None,
            "last_date": bars[-1].date if bars else None,
            "sample_bar": bars[0].__dict__ if bars else None,
        })

        return AssetSeries(
            symbol=resolved_symbol,
            dates=[b.date for b in bars],
            closes=[b.close for b in bars],
            bars=bars,
            source_path=self._rel(path),
            meta=meta,
        )

    def load_vix_series(self) -> AssetSeries | None:
        candidates = [
            self.index_dir / "VIX.json",
            self.index_dir / "_VIX.json",
            self.prod_price_dir / "_VIX.json",
        ]

        for path in candidates:
            if path.exists():
                return self.load_asset_series(path, symbol="VIX")

        return None

    def load_regime_daily(self) -> dict[str, RegimeRecord]:
        if not self.regime_path.exists():
            return {}

        raw = self._read_json(self.regime_path)
        candidates = self._collect_regime_records(raw)

        records: dict[str, RegimeRecord] = {}

        for row in candidates:
            d = row.get("date")
            regime = row.get("spx_regime")
            subclass = row.get("subclass") or "NO_SUBCLASS"

            if not self._is_date_like(d):
                continue
            if regime not in {"UPTREND", "SIDEWAYS", "DOWNTREND"}:
                continue

            records[str(d)] = RegimeRecord(
                date=str(d),
                spx_regime=regime,
                subclass=str(subclass),
                raw=row.get("raw"),
                source_path=row.get("_source_path"),
            )

        return dict(sorted(records.items()))

    def regime_summary(self, regime_daily: dict[str, RegimeRecord]) -> dict[str, Any]:
        regime_counts = Counter()
        subclass_counts = Counter()

        for row in regime_daily.values():
            regime_counts[row.spx_regime] += 1
            subclass_counts[row.subclass or "NO_SUBCLASS"] += 1

        dates = sorted(regime_daily.keys())

        return {
            "record_count": len(regime_daily),
            "first_date": dates[0] if dates else None,
            "last_date": dates[-1] if dates else None,
            "regime_counts": dict(regime_counts),
            "subclass_counts": dict(subclass_counts),
            "sample": {
                d: {
                    "spx_regime": regime_daily[d].spx_regime,
                    "subclass": regime_daily[d].subclass,
                    "source_path": regime_daily[d].source_path,
                }
                for d in dates[:5]
            },
        }

    def build_alignment_summary(
        self,
        symbols: list[str],
        dates_map: dict[str, list[str]],
        indices: dict[str, AssetSeries],
        regime_daily: dict[str, RegimeRecord],
    ) -> dict[str, Any]:
        return {
            "spx_vs_indices": strict_common_dates({
                sym: series.dates
                for sym, series in indices.items()
            }),
            "sample_stocks_vs_spx": strict_common_dates({
                "SPX": indices["SPX"].dates if "SPX" in indices else [],
                **{sym: dates_map[sym] for sym in symbols[:20]},
            }),
            "spx_vs_regime": strict_common_dates({
                "SPX": indices["SPX"].dates if "SPX" in indices else [],
                "regime": sorted(regime_daily.keys()),
            }),
        }

    def to_audit_sample(self, bundle: HistoricalDataBundle) -> dict[str, Any]:
        sample_symbols = bundle.symbols[:5]

        return {
            "schema": "E1RHistoricalDataBundleAuditSampleV1",
            "adapter": "HistoricalDataAdapter",
            "universe": {
                "count": len(bundle.symbols),
                "sample_symbols": sample_symbols,
            },
            "stocks": bundle.metadata,
            "indices": {
                sym: {
                    "count": len(series.dates),
                    "first_date": series.dates[0] if series.dates else None,
                    "last_date": series.dates[-1] if series.dates else None,
                    "source_path": series.source_path,
                    "meta": series.meta,
                }
                for sym, series in bundle.indices.items()
            },
            "vix": {
                "available": bundle.vix is not None,
                "count": len(bundle.vix.dates) if bundle.vix else 0,
                "first_date": bundle.vix.dates[0] if bundle.vix and bundle.vix.dates else None,
                "last_date": bundle.vix.dates[-1] if bundle.vix and bundle.vix.dates else None,
                "source_path": bundle.vix.source_path if bundle.vix else None,
            },
            "regime": self.regime_summary(bundle.regime_daily),
            "sample_payload": {
                "stock_samples": {
                    sym: {
                        "dates_tail": bundle.dates_map[sym][-5:],
                        "closes_tail": bundle.prices_map[sym][-5:],
                        "ohlc_tail": [bar.__dict__ for bar in bundle.ohlc_map[sym][-2:]],
                    }
                    for sym in sample_symbols
                },
                "index_samples": {
                    sym: {
                        "dates_tail": series.dates[-5:],
                        "closes_tail": series.closes[-5:],
                    }
                    for sym, series in bundle.indices.items()
                },
                "regime_tail": {
                    d: {
                        "spx_regime": bundle.regime_daily[d].spx_regime,
                        "subclass": bundle.regime_daily[d].subclass,
                    }
                    for d in sorted(bundle.regime_daily.keys())[-5:]
                },
            },
        }

    def _collect_regime_records(self, obj: Any, path: str = "$") -> list[dict[str, Any]]:
        found: list[dict[str, Any]] = []

        if isinstance(obj, dict):
            for k, v in obj.items():
                if self._is_date_like(k):
                    row = self._normalize_regime_value(v, str(k)[:10])
                    row["_source_path"] = f"{path}.{k}"
                    found.append(row)

            d = self._parse_date(obj)
            if d is not None:
                row = self._normalize_regime_value(obj, d)
                if row.get("spx_regime") is not None or row.get("subclass") is not None:
                    row["_source_path"] = path
                    found.append(row)

            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    found.extend(self._collect_regime_records(v, f"{path}.{k}"))

        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, (dict, list)):
                    found.extend(self._collect_regime_records(item, f"{path}[{i}]"))

        return found

    def _normalize_regime_value(self, value: Any, date_hint: str | None = None) -> dict[str, Any]:
        if isinstance(value, dict):
            regime = self._find_first_value(value, [
                "spx_regime", "regime", "market_regime", "dominant_regime",
                "state", "market_state", "trend_regime", "label",
            ])
            subclass = self._find_first_value(value, [
                "subclass", "sideways_subclass", "regime_subclass",
                "market_subclass", "spx_subclass", "sub_regime",
            ])

            if regime is None:
                for v in value.values():
                    if isinstance(v, str) and v.upper() in {"UPTREND", "SIDEWAYS", "DOWNTREND"}:
                        regime = v.upper()
                        break

            if subclass is None:
                for v in value.values():
                    if isinstance(v, str) and v.upper() in {
                        "MA_CONFLICT",
                        "DETERIORATION_TRANSITION",
                        "RECOVERY_TRANSITION",
                        "NO_SUBCLASS",
                    }:
                        subclass = v.upper()
                        break

            return {
                "date": date_hint or self._parse_date(value),
                "spx_regime": str(regime).upper() if regime is not None else None,
                "subclass": str(subclass).upper() if subclass is not None else None,
                "raw": value,
            }

        if isinstance(value, str):
            return {
                "date": date_hint,
                "spx_regime": value.upper() if value.upper() in {"UPTREND", "SIDEWAYS", "DOWNTREND"} else value,
                "subclass": None,
                "raw": value,
            }

        return {
            "date": date_hint,
            "spx_regime": None,
            "subclass": None,
            "raw": value,
        }

    @staticmethod
    def _read_json(path: Path) -> Any:
        return json.loads(path.read_text())

    def _rel(self, path: Path) -> str:
        try:
            return str(path.relative_to(self.root))
        except Exception:
            return str(path)

    @staticmethod
    def _is_date_like(value: Any) -> bool:
        return (
            isinstance(value, str)
            and len(value) >= 10
            and value[:4].isdigit()
            and value[4] == "-"
            and value[7] == "-"
        )

    @staticmethod
    def _parse_date(row: dict[str, Any]) -> str | None:
        for key in ["date", "Date", "timestamp", "time", "signal_date", "as_of_date", "trading_date"]:
            if key in row and row[key] is not None:
                value = str(row[key])[:10]
                if HistoricalDataAdapter._is_date_like(value):
                    return value
        return None

    @staticmethod
    def _parse_float(row: dict[str, Any], keys: list[str]) -> float | None:
        for key in keys:
            if key in row and row[key] is not None:
                try:
                    return float(row[key])
                except Exception:
                    return None
        return None

    @staticmethod
    def _find_first_value(row: dict[str, Any], keys: list[str]) -> Any:
        for key in keys:
            if key in row and row[key] not in [None, ""]:
                return row[key]
        return None
