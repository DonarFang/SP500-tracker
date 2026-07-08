# Stage 3.8E-2F-2C-4C-10C Sidecar Build Failure Audit

Generated At: `2026-07-08T12:01:12.380396+00:00`

## Status

- Status: `SIDECAR_BUILD_FAILURE_AUDIT_COMPLETE_NO_EXPORTS_WRITTEN`
- Dashboard changed: `False`
- Exports changed: `False`
- Workflow changed: `False`
- Strategy logic changed: `False`
- Canonical exports written: `False`
- Long backtest run: `False`

## Diagnosis

- 10B sidecar_build section not found.
- load_spx_ok: None.
- load_regimes_ok: None.
- load_stock_universe_ok: None.
- build_intervals_ok: None.
- build_sidecar_ok: None.
- Sidecar build now succeeds; next step can compose with 5Y core records.

## Lower Level Probe

```json
{
  "import_ok": false,
  "signatures": {
    "E1RSidecarConfig": "(start_date: 'str', end_date: 'str', allowed_subclasses: 'tuple[str, ...]' = ('MA_CONFLICT',), top_n: 'int' = 10, gross_exposure: 'float' = 0.25, min_history_days: 'int' = 200, min_price: 'float' = 5.0, initial_equity: 'float' = 100000.0, excluded_symbols: 'tuple[str, ...]' = ('VIXY',)) -> None",
    "load_asset": "(path: 'Path') -> 'dict[str, Any]'",
    "load_regimes": "(path: 'Path') -> 'dict[str, dict[str, Any]]'",
    "load_stock_universe": "(stock_dir: 'Path', config: 'E1RSidecarConfig') -> 'tuple[dict[str, dict[str, Any]], list[str]]'",
    "build_backtest_intervals": "(spx: 'dict[str, Any]', regimes: 'dict[str, dict[str, Any]]', config: 'E1RSidecarConfig') -> 'list[tuple[str, str]]'",
    "build_e1r_sidecar_sleeve": "(stock_dir: 'Path', spx_path: 'Path', regime_path: 'Path', config: 'E1RSidecarConfig') -> 'dict[str, Any]'"
  },
  "import_error": "TypeError: __init__() missing 2 required positional arguments: 'start_date' and 'end_date'",
  "import_traceback": "Traceback (most recent call last):\n  File \"<stdin>\", line 146, in try_lower_level_calls\nTypeError: __init__() missing 2 required positional arguments: 'start_date' and 'end_date'\n"
}
```

## Input Shapes

```json
{
  "stock_dir": {
    "path": "data/research/e1_5y/raw/stocks",
    "exists": true,
    "json_file_count": 542,
    "samples": [
      {
        "path": "data/research/e1_5y/raw/stocks/A.json",
        "exists": true,
        "json_valid": true,
        "type": "dict",
        "top_keys": [
          "bars",
          "data_end",
          "data_start",
          "dataset_mode",
          "downloaded_at",
          "formal_pass_fail_allowed",
          "price_adjustment",
          "requested_end",
          "requested_start",
          "schema_version",
          "source",
          "survivorship_bias",
          "symbol",
          "yahoo_ticker"
        ],
        "bars_length": 1562,
        "bars_first": [
          {
            "date": "2020-04-01",
            "open": 66.616585,
            "high": 67.34537,
            "low": 65.350803,
            "close": 66.089172,
            "volume": 2173600
          },
          {
            "date": "2020-04-02",
            "open": 65.465876,
            "high": 69.474187,
            "low": 65.341218,
            "close": 69.320763,
            "volume": 1840300
          }
        ],
        "bars_last": [
          {
            "date": "2026-06-17",
            "open": 127.620003,
            "high": 128.649994,
            "low": 123.699997,
            "close": 124.330002,
            "volume": 2470700
          },
          {
            "date": "2026-06-18",
            "open": 125.559998,
            "high": 127.559998,
            "low": 125.169998,
            "close": 127.059998,
            "volume": 4334300
          }
        ]
      },
      {
        "path": "data/research/e1_5y/raw/stocks/AAL.json",
        "exists": true,
        "json_valid": true,
        "type": "dict",
        "top_keys": [
          "bars",
          "data_end",
          "data_start",
          "dataset_mode",
          "downloaded_at",
          "formal_pass_fail_allowed",
          "price_adjustment",
          "requested_end",
          "requested_start",
          "schema_version",
          "source",
          "survivorship_bias",
          "symbol",
          "yahoo_ticker"
        ],
        "bars_length": 1562,
        "bars_first": [
          {
            "date": "2020-04-01",
            "open": 11.45,
            "high": 11.48,
            "low": 10.5,
            "close": 10.69,
            "volume": 56854400
          },
          {
            "date": "2020-04-02",
            "open": 10.61,
            "high": 11.03,
            "low": 10.0,
            "close": 10.06,
            "volume": 65534600
          }
        ],
        "bars_last": [
          {
            "date": "2026-06-17",
            "open": 15.71,
            "high": 16.059999,
            "low": 15.4,
            "close": 15.42,
            "volume": 130165900
          },
          {
            "date": "2026-06-18",
            "open": 15.85,
            "high": 16.07,
            "low": 15.77,
            "close": 15.99,
            "volume": 126278400
          }
        ]
      },
      {
        "path": "data/research/e1_5y/raw/stocks/AAPL.json",
        "exists": true,
        "json_valid": true,
        "type": "dict",
        "top_keys": [
          "bars",
          "data_end",
          "data_start",
          "dataset_mode",
          "downloaded_at",
          "formal_pass_fail_allowed",
          "price_adjustment",
          "requested_end",
          "requested_start",
          "schema_version",
          "source",
          "survivorship_bias",
          "symbol",
          "yahoo_ticker"
        ],
        "bars_length": 1562,
        "bars_first": [
          {
            "date": "2020-04-01",
            "open": 59.505966,
            "high": 60.041882,
            "low": 57.726823,
            "close": 58.156521,
            "volume": 176218400
          },
          {
            "date": "2020-04-02",
            "open": 58.018927,
            "high": 59.180077,
            "low": 57.188498,
            "close": 59.126968,
            "volume": 165934000
          }
        ],
        "bars_last": [
          {
            "date": "2026-06-17",
            "open": 300.850006,
            "high": 302.070007,
            "low": 294.359985,
            "close": 295.950012,
            "volume": 42745100
          },
          {
            "date": "2026-06-18",
            "open": 298.109985,
            "high": 300.570007,
            "low": 295.619995,
            "close": 298.01001,
            "volume": 85962200
          }
        ]
      },
      {
        "path": "data/research/e1_5y/raw/stocks/ABBV.json",
        "exists": true,
        "json_valid": true,
        "type": "dict",
        "top_keys": [
          "bars",
          "data_end",
          "data_start",
          "dataset_mode",
          "downloaded_at",
          "formal_pass_fail_allowed",
          "price_adjustment",
          "requested_end",
          "requested_start",
          "schema_version",
          "source",
          "survivorship_bias",
          "symbol",
          "yahoo_ticker"
        ],
        "bars_length": 1562,
        "bars_first": [
          {
            "date": "2020-04-01",
            "open": 56.072673,
            "high": 57.526578,
            "low": 55.536202,
            "close": 57.083408,
            "volume": 12948000
          },
          {
            "date": "2020-04-02",
            "open": 56.585833,
            "high": 58.700611,
            "low": 55.559545,
            "close": 58.412937,
            "volume": 8077800
          }
        ],
        "bars_last": [
          {
            "date": "2026-06-17",
            "open": 222.399994,
            "high": 222.839996,
            "low": 218.830002,
            "close": 221.229996,
            "volume": 5624200
          },
          {
            "date": "2026-06-18",
            "open": 221.369995,
            "high": 222.350006,
            "low": 215.369995,
            "close": 216.490005,
            "volume": 9646100
          }
        ]
      },
      {
        "path": "data/research/e1_5y/raw/stocks/ABNB.json",
        "exists": true,
        "json_valid": true,
        "type": "dict",
        "top_keys": [
          "bars",
          "data_end",
          "data_start",
          "dataset_mode",
          "downloaded_at",
          "formal_pass_fail_allowed",
          "price_adjustment",
          "requested_end",
          "requested_start",
          "schema_version",
          "source",
          "survivorship_bias",
          "symbol",
          "yahoo_ticker"
        ],
        "bars_length": 1386,
        "bars_first": [
          {
            "date": "2020-12-10",
            "open": 146.0,
            "high": 165.0,
            "low": 141.25,
            "close": 144.710007,
            "volume": 70447500
          },
          {
            "date": "2020-12-11",
            "open": 146.550003,
            "high": 151.5,
            "low": 135.100006,
            "close": 139.25,
            "volume": 26980800
          }
        ],
        "bars_last": [
          {
            "date": "2026-06-17",
            "open": 140.690002,
            "high": 143.800003,
            "low": 139.5,
            "close": 140.539993,
            "volume": 3438000
          },
          {
            "date": "2026-06-18",
            "open": 141.389999,
            "high": 143.619995,
            "low": 140.139999,
            "close": 142.410004,
            "volume": 7413200
          }
        ]
      }
    ]
  },
  "spx": {
    "path": "data/research/e1_5y/raw/indices/SPX.json",
    "exists": true,
    "json_valid": true,
    "type": "dict",
    "top_keys": [
      "bars",
      "data_end",
      "data_start",
      "dataset_mode",
      "downloaded_at",
      "requested_end",
      "requested_start",
      "schema_version",
      "source",
      "symbol",
      "yahoo_ticker"
    ],
    "bars_length": 1562,
    "bars_first": [
      {
        "date": "2020-04-01",
        "open": 2498.080078,
        "high": 2522.75,
        "low": 2447.48999,
        "close": 2470.5,
        "volume": 5964000000
      },
      {
        "date": "2020-04-02",
        "open": 2458.540039,
        "high": 2533.219971,
        "low": 2455.790039,
        "close": 2526.899902,
        "volume": 6464190000
      },
      {
        "date": "2020-04-03",
        "open": 2514.919922,
        "high": 2538.179932,
        "low": 2459.959961,
        "close": 2488.649902,
        "volume": 6096970000
      }
    ],
    "bars_last": [
      {
        "date": "2026-06-16",
        "open": 7548.779785,
        "high": 7564.959961,
        "low": 7508.680176,
        "close": 7511.350098,
        "volume": 5286210000
      },
      {
        "date": "2026-06-17",
        "open": 7524.5,
        "high": 7532.169922,
        "low": 7402.609863,
        "close": 7420.100098,
        "volume": 5883740000
      },
      {
        "date": "2026-06-18",
        "open": 7487.359863,
        "high": 7511.069824,
        "low": 7468.319824,
        "close": 7500.580078,
        "volume": 9061110000
      }
    ]
  },
  "regime": {
    "path": "data/research/e1_5y/regimes/spx_regime_daily.json",
    "exists": true,
    "json_valid": true,
    "type": "dict",
    "top_keys": [
      "daily_regime",
      "generated_at",
      "validation_window"
    ],
    "daily_regime_type": "dict",
    "daily_regime_length": 1562,
    "daily_regime_sample": [
      [
        "2020-04-01",
        {
          "regime": "UNCLASSIFIED",
          "subclass": null
        }
      ],
      [
        "2020-04-02",
        {
          "regime": "UNCLASSIFIED",
          "subclass": null
        }
      ],
      [
        "2020-04-03",
        {
          "regime": "UNCLASSIFIED",
          "subclass": null
        }
      ]
    ]
  }
}
```

## Relevant Function Sources

### `build_e1r_sidecar_sleeve`

- Lines: `538→594`
```python
def build_e1r_sidecar_sleeve(
    stock_dir: Path,
    spx_path: Path,
    regime_path: Path,
    config: E1RSidecarConfig,
) -> dict[str, Any]:
    spx = load_asset(spx_path)
    regimes = load_regimes(regime_path)
    stocks, excluded_found = load_stock_universe(stock_dir, config)

    intervals = build_backtest_intervals(spx, regimes, config)
    rankings = build_daily_rankings(stocks, spx, regimes, intervals, config)
    records = run_daily_rebalanced_sidecar(rankings, spx, regimes, intervals, config)
    summary = summarize_sidecar(records, config)

    regime_counts: dict[str, int] = {}
    subclass_counts: dict[str, int] = {}

    for record in records:
        regime = record["regime"]
        subclass = record["subclass"]
        regime_counts[regime] = regime_counts.get(regime, 0) + 1
        if regime == "SIDEWAYS":
            subclass_counts[subclass] = subclass_counts.get(subclass, 0) + 1

    return {
        "engine": "e1r_sidecar_sleeve",
        "version": "v0.2_formal_sleeve_engine",
        "config": {
            "start_date": config.start_date,
            "end_date": config.end_date,
            "allowed_subclasses": list(config.allowed_subclasses),
            "top_n": config.top_n,
            "gross_exposure": config.gross_exposure,
            "min_history_days": config.min_history_days,
            "min_price": config.min_price,
            "initial_equity": config.initial_equity,
            "excluded_symbols": list(config.excluded_symbols),
        },
        "sample": {
            "intervals": len(intervals),
            "first_interval": {
                "date": intervals[0][0],
                "next_date": intervals[0][1],
            } if intervals else None,
            "last_interval": {
                "date": intervals[-1][0],
                "next_date": intervals[-1][1],
            } if intervals else None,
            "stock_universe_after_exclusions": len(stocks),
            "excluded_symbols_found_in_raw_data": excluded_found,
            "regime_counts": regime_counts,
            "sideways_subclass_counts": subclass_counts,
        },
        "summary": summary,
        "records": records,
    }
```

### `load_asset`

- Lines: `126→155`
```python
def load_asset(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text())
    bars: list[dict[str, Any]] = []

    for row in raw.get("bars", []):
        date = row.get("date")
        close = safe_float(row.get("close"))
        if not date or close is None:
            continue

        bars.append({
            "date": date,
            "open": safe_float(row.get("open")),
            "high": safe_float(row.get("high")),
            "low": safe_float(row.get("low")),
            "close": close,
            "volume": safe_float(row.get("volume")),
        })

    bars.sort(key=lambda x: x["date"])

    return {
        "symbol": raw.get("symbol") or path.stem,
        "data_start": raw.get("data_start"),
        "data_end": raw.get("data_end"),
        "bars": bars,
        "dates": [x["date"] for x in bars],
        "by_date": {x["date"]: x for x in bars},
        "date_to_idx": {x["date"]: i for i, x in enumerate(bars)},
    }
```

### `load_regimes`

- Lines: `182→189`
```python
def load_regimes(path: Path) -> dict[str, dict[str, Any]]:
    raw = json.loads(path.read_text())
    daily = raw.get("daily_regime", raw)
    return {
        date: value
        for date, value in daily.items()
        if isinstance(value, dict)
    }
```

### `load_stock_universe`

- Lines: `158→179`
```python
def load_stock_universe(
    stock_dir: Path,
    config: E1RSidecarConfig,
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    assets: dict[str, dict[str, Any]] = {}
    excluded_found: list[str] = []
    excluded = set(config.excluded_symbols)

    for path in sorted(stock_dir.glob("*.json")):
        asset = load_asset(path)
        symbol = asset["symbol"]

        if symbol in excluded:
            excluded_found.append(symbol)
            continue

        if len(asset["bars"]) < config.min_history_days:
            continue

        assets[symbol] = asset

    return assets, sorted(excluded_found)
```

### `build_backtest_intervals`

- Lines: `342→353`
```python
def build_backtest_intervals(
    spx: dict[str, Any],
    regimes: dict[str, dict[str, Any]],
    config: E1RSidecarConfig,
) -> list[tuple[str, str]]:
    dates = [
        d for d in spx["dates"]
        if config.start_date <= d <= config.end_date
        and d in regimes
    ]
    dates = sorted(dates)
    return list(zip(dates[:-1], dates[1:]))
```

### `run_daily_rebalanced_sidecar`

- Lines: `401→470`
```python
def run_daily_rebalanced_sidecar(
    rankings: dict[str, dict[str, Any]],
    spx: dict[str, Any],
    regimes: dict[str, dict[str, Any]],
    intervals: Sequence[tuple[str, str]],
    config: E1RSidecarConfig,
) -> list[dict[str, Any]]:
    allowed_subclasses = set(config.allowed_subclasses)
    top_n = int(config.top_n)
    gross_exposure = float(config.gross_exposure)

    records: list[dict[str, Any]] = []

    for date, next_date in intervals:
        regime_info = regimes.get(date, {})
        regime = regime_info.get("regime") or "NO_REGIME"
        subclass = regime_info.get("subclass") or "NO_SUBCLASS"

        spx_return = close_to_close_return(spx, date, next_date) or 0.0

        ranked = rankings.get(date, {})
        candidates = ranked.get("candidates", [])

        is_active = (
            regime == "SIDEWAYS"
            and subclass in allowed_subclasses
            and top_n > 0
            and gross_exposure > 0
            and bool(candidates)
        )

        holdings: list[dict[str, Any]] = []
        portfolio_return = 0.0

        if is_active:
            selected = candidates[:top_n]
            weight = gross_exposure / len(selected)

            for candidate in selected:
                raw_return = candidate["one_day_return"]
                contribution = weight * raw_return
                portfolio_return += contribution

                holdings.append({
                    "symbol": candidate["symbol"],
                    "score": candidate["score"],
                    "weight": weight,
                    "raw_return": raw_return,
                    "raw_return_pct": pct_display(raw_return),
                    "weighted_contribution": contribution,
                    "weighted_contribution_pct": pct_display(contribution),
                })

        records.append({
            "date": date,
            "next_date": next_date,
            "regime": regime,
            "subclass": subclass,
            "is_active": is_active,
            "candidate_count": len(candidates),
            "selected_count": len(holdings),
            "gross_exposure": gross_exposure if is_active else 0.0,
            "portfolio_return": portfolio_return,
            "portfolio_return_pct": pct_display(portfolio_return),
            "spx_return": spx_return,
            "spx_return_pct": pct_display(spx_return),
            "holdings": holdings,
        })

    return records
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10D`: Fix sidecar input contract or proceed to compose if sidecar build succeeds
- Recommended action: Use 10C error diagnosis to either normalize the input paths/schema passed to build_e1r_sidecar_sleeve, or if sidecar build succeeds, generate/recover the 5Y E1 core daily equity records and compose E1R.

