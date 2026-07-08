# Stage 3.8E-2F-2C-4A-1 Sidecar Activation Audit

Generated At: `2026-07-08T13:05:38.265796+00:00`

## Status

- Status: `SIDECAR_ACTIVATION_AUDIT_COMPLETE_NO_EXPORTS_WRITTEN`
- Strategy files unchanged: `True`
- Canonical existence unchanged: `True`

## Last 4A Summary

```json
{
  "status": "E1R_SIDECAR_RECORDS_5Y_NOT_READY",
  "interval_stats": {
    "row_count": 1260,
    "date_start": "2021-06-11",
    "date_end": "2026-06-17",
    "unique_dates": 1260,
    "max_rows_per_date": 1,
    "one_row_per_date": true,
    "sample_first": [
      {
        "date": "2021-06-11",
        "next_date": "2021-06-14"
      },
      {
        "date": "2021-06-14",
        "next_date": "2021-06-15"
      },
      {
        "date": "2021-06-15",
        "next_date": "2021-06-16"
      }
    ],
    "sample_last": [
      {
        "date": "2026-06-15",
        "next_date": "2026-06-16"
      },
      {
        "date": "2026-06-16",
        "next_date": "2026-06-17"
      },
      {
        "date": "2026-06-17",
        "next_date": "2026-06-18"
      }
    ]
  },
  "sidecar_stats": {
    "row_count": 1260,
    "date_start": "2021-06-11",
    "date_end": "2026-06-17",
    "unique_dates": 1260,
    "max_rows_per_date": 1,
    "one_row_per_date": true,
    "regime_counts": {
      "UPTREND": 861,
      "SIDEWAYS": 241,
      "DOWNTREND": 158
    },
    "subclass_counts": {
      "NO_SUBCLASS": 1019,
      "MA_CONFLICT": 135,
      "DETERIORATION_TRANSITION": 63,
      "RECOVERY_TRANSITION": 43
    },
    "active_count": 0,
    "nonzero_sidecar_return_count": 0,
    "sidecar_active_by_regime": {},
    "sidecar_active_by_subclass": {},
    "gross_exposure_min": null,
    "gross_exposure_max": null,
    "selected_count_min": null,
    "selected_count_max": null
  },
  "validation": {
    "full_intervals_ge_1000": true,
    "sidecar_records_nonempty": true,
    "sidecar_one_row_per_date": true,
    "sidecar_active_count_positive": false,
    "sidecar_active_count_reasonable": false,
    "ma_conflict_active_present": false,
    "canonical_e1r_files_unchanged": true
  }
}
```

## Config Probe

```json
{
  "signature": "(start_date: 'str', end_date: 'str', allowed_subclasses: 'tuple[str, ...]' = ('MA_CONFLICT',), top_n: 'int' = 10, gross_exposure: 'float' = 0.25, min_history_days: 'int' = 200, min_price: 'float' = 5.0, initial_equity: 'float' = 100000.0, excluded_symbols: 'tuple[str, ...]' = ('VIXY',)) -> None",
  "repr": "E1RSidecarConfig(start_date='2021-06-11', end_date='2026-06-18', allowed_subclasses=('MA_CONFLICT',), top_n=10, gross_exposure=0.25, min_history_days=200, min_price=5.0, initial_equity=100000.0, excluded_symbols=('VIXY',))",
  "is_dataclass": true,
  "fields": {
    "start_date": "2021-06-11",
    "end_date": "2026-06-18",
    "allowed_subclasses": [
      "MA_CONFLICT"
    ],
    "top_n": 10,
    "gross_exposure": 0.25,
    "min_history_days": 200,
    "min_price": 5.0,
    "initial_equity": 100000.0,
    "excluded_symbols": [
      "VIXY"
    ]
  },
  "function_signatures": {
    "build_daily_rankings": "(stocks: 'dict[str, dict[str, Any]]', spx: 'dict[str, Any]', regimes: 'dict[str, dict[str, Any]]', intervals: 'Sequence[tuple[str, str]]', config: 'E1RSidecarConfig') -> 'dict[str, dict[str, Any]]'",
    "run_daily_rebalanced_sidecar": "(rankings: 'dict[str, dict[str, Any]]', spx: 'dict[str, Any]', regimes: 'dict[str, dict[str, Any]]', intervals: 'Sequence[tuple[str, str]]', config: 'E1RSidecarConfig') -> 'list[dict[str, Any]]'",
    "build_e1r_sidecar_sleeve": "(stock_dir: 'Path', spx_path: 'Path', regime_path: 'Path', config: 'E1RSidecarConfig') -> 'dict[str, Any]'",
    "summarize_sidecar": "(records: 'Sequence[dict[str, Any]]', config: 'E1RSidecarConfig') -> 'dict[str, Any]'"
  }
}
```

## Suspicious Config Fields

```json
{
  "allowed_subclasses": [
    "MA_CONFLICT"
  ],
  "top_n": 10,
  "gross_exposure": 0.25,
  "min_history_days": 200,
  "min_price": 5.0
}
```

## Important Lines

```json
[
  {
    "line": 10,
    "terms": [
      "MA_CONFLICT",
      "SIDEWAYS"
    ],
    "text": "- Active only in SIDEWAYS:MA_CONFLICT."
  },
  {
    "line": 26,
    "terms": [
      "return"
    ],
    "text": "The sidecar sleeve is later composed with the E1R v0.1 core daily returns by"
  },
  {
    "line": 44,
    "terms": [
      "MA_CONFLICT",
      "subclass"
    ],
    "text": "    allowed_subclasses: tuple[str, ...] = (\"MA_CONFLICT\",)"
  },
  {
    "line": 46,
    "terms": [
      "gross_exposure"
    ],
    "text": "    gross_exposure: float = 0.25"
  },
  {
    "line": 56,
    "terms": [
      "return"
    ],
    "text": "            return None"
  },
  {
    "line": 59,
    "terms": [
      "return"
    ],
    "text": "            return None"
  },
  {
    "line": 60,
    "terms": [
      "return"
    ],
    "text": "        return x"
  },
  {
    "line": 62,
    "terms": [
      "return"
    ],
    "text": "        return None"
  },
  {
    "line": 65,
    "terms": [
      "return"
    ],
    "text": "def pct_display(decimal_return: Optional[float]) -> Optional[float]:"
  },
  {
    "line": 66,
    "terms": [
      "return"
    ],
    "text": "    return None if decimal_return is None else decimal_return * 100.0"
  },
  {
    "line": 69,
    "terms": [
      "return"
    ],
    "text": "def compound_return(returns: Iterable[Optional[float]]) -> float:"
  },
  {
    "line": 71,
    "terms": [
      "return"
    ],
    "text": "    for r in returns:"
  },
  {
    "line": 74,
    "terms": [
      "return"
    ],
    "text": "    return value - 1.0"
  },
  {
    "line": 79,
    "terms": [
      "return"
    ],
    "text": "    return mean(xs) if xs else None"
  },
  {
    "line": 84,
    "terms": [
      "return"
    ],
    "text": "    return median(xs) if xs else None"
  },
  {
    "line": 89,
    "terms": [
      "return"
    ],
    "text": "        return None"
  },
  {
    "line": 99,
    "terms": [
      "return"
    ],
    "text": "    return worst"
  },
  {
    "line": 102,
    "terms": [
      "return"
    ],
    "text": "def sharpe_ratio(daily_returns: Sequence[float]) -> Optional[float]:"
  },
  {
    "line": 103,
    "terms": [
      "return"
    ],
    "text": "    values = [x for x in daily_returns if x is not None]"
  },
  {
    "line": 105,
    "terms": [
      "return"
    ],
    "text": "        return None"
  },
  {
    "line": 109,
    "terms": [
      "return"
    ],
    "text": "        return None"
  },
  {
    "line": 111,
    "terms": [
      "return"
    ],
    "text": "    return mean(values) / sigma * math.sqrt(252)"
  },
  {
    "line": 114,
    "terms": [
      "return"
    ],
    "text": "def profit_factor(daily_returns: Sequence[float]) -> Optional[float]:"
  },
  {
    "line": 115,
    "terms": [
      "return"
    ],
    "text": "    gains = sum(x for x in daily_returns if x is not None and x > 0)"
  },
  {
    "line": 116,
    "terms": [
      "return"
    ],
    "text": "    losses = -sum(x for x in daily_returns if x is not None and x < 0)"
  },
  {
    "line": 120,
    "terms": [
      "return"
    ],
    "text": "            return None"
  },
  {
    "line": 121,
    "terms": [
      "return"
    ],
    "text": "        return float(\"inf\")"
  },
  {
    "line": 123,
    "terms": [
      "return"
    ],
    "text": "    return gains / losses"
  },
  {
    "line": 134,
    "terms": [
      "continue"
    ],
    "text": "            continue"
  },
  {
    "line": 147,
    "terms": [
      "return"
    ],
    "text": "    return {"
  },
  {
    "line": 172,
    "terms": [
      "continue"
    ],
    "text": "            continue"
  },
  {
    "line": 175,
    "terms": [
      "continue"
    ],
    "text": "            continue"
  },
  {
    "line": 179,
    "terms": [
      "return"
    ],
    "text": "    return assets, sorted(excluded_found)"
  },
  {
    "line": 185,
    "terms": [
      "return"
    ],
    "text": "    return {"
  },
  {
    "line": 195,
    "terms": [
      "return"
    ],
    "text": "        return None"
  },
  {
    "line": 196,
    "terms": [
      "return"
    ],
    "text": "    return [asset[\"bars\"][i][\"close\"] for i in range(idx - length + 1, idx + 1)]"
  },
  {
    "line": 201,
    "terms": [
      "return"
    ],
    "text": "        return None"
  },
  {
    "line": 204,
    "terms": [
      "return"
    ],
    "text": "        return None"
  },
  {
    "line": 205,
    "terms": [
      "return"
    ],
    "text": "    return sum(window) / length"
  },
  {
    "line": 210,
    "terms": [
      "return"
    ],
    "text": "        return None"
  },
  {
    "line": 216,
    "terms": [
      "return"
    ],
    "text": "        return None"
  },
  {
    "line": 218,
    "terms": [
      "return"
    ],
    "text": "    return (last / first - 1.0) * 100.0"
  },
  {
    "line": 223,
    "terms": [
      "return"
    ],
    "text": "        return None"
  },
  {
    "line": 229,
    "terms": [
      "return"
    ],
    "text": "        return None"
  },
  {
    "line": 231,
    "terms": [
      "return"
    ],
    "text": "    return (last / high - 1.0) * 100.0"
  },
  {
    "line": 234,
    "terms": [
      "return"
    ],
    "text": "def close_to_close_return("
  },
  {
    "line": 243,
    "terms": [
      "return"
    ],
    "text": "        return None"
  },
  {
    "line": 249,
    "terms": [
      "return"
    ],
    "text": "        return None"
  },
  {
    "line": 251,
    "terms": [
      "return"
    ],
    "text": "    return c1 / c0 - 1.0"
  },
  {
    "line": 272,
    "terms": [
      "return"
    ],
    "text": "        return None"
  },
  {
    "line": 276,
    "terms": [
      "return"
    ],
    "text": "        return None"
  },
  {
    "line": 288,
    "terms": [
      "return"
    ],
    "text": "        return None"
  },
  {
    "line": 329,
    "terms": [
      "return"
    ],
    "text": "    return {"
  },
  {
    "line": 353,
    "terms": [
      "return"
    ],
    "text": "    return list(zip(dates[:-1], dates[1:]))"
  },
  {
    "line": 356,
    "terms": [
      "rankings"
    ],
    "text": "def build_daily_rankings("
  },
  {
    "line": 363,
    "terms": [
      "rankings"
    ],
    "text": "    rankings: dict[str, dict[str, Any]] = {}"
  },
  {
    "line": 367,
    "terms": [
      "SIDEWAYS"
    ],
    "text": "        if regime_info.get(\"regime\") != \"SIDEWAYS\":"
  },
  {
    "line": 368,
    "terms": [
      "continue"
    ],
    "text": "            continue"
  },
  {
    "line": 374,
    "terms": [
      "continue"
    ],
    "text": "                continue"
  },
  {
    "line": 378,
    "terms": [
      "continue"
    ],
    "text": "                continue"
  },
  {
    "line": 380,
    "terms": [
      "return"
    ],
    "text": "            one_day_return = close_to_close_return(asset, date, next_date)"
  },
  {
    "line": 381,
    "terms": [
      "return"
    ],
    "text": "            if one_day_return is None:"
  },
  {
    "line": 382,
    "terms": [
      "continue"
    ],
    "text": "                continue"
  },
  {
    "line": 384,
    "terms": [
      "return"
    ],
    "text": "            candidate[\"one_day_return\"] = one_day_return"
  },
  {
    "line": 389,
    "terms": [
      "rankings"
    ],
    "text": "        rankings[date] = {"
  },
  {
    "line": 392,
    "terms": [
      "SIDEWAYS"
    ],
    "text": "            \"regime\": \"SIDEWAYS\","
  },
  {
    "line": 393,
    "terms": [
      "subclass"
    ],
    "text": "            \"subclass\": regime_info.get(\"subclass\") or \"NO_SUBCLASS\","
  },
  {
    "line": 398,
    "terms": [
      "rankings",
      "return"
    ],
    "text": "    return rankings"
  },
  {
    "line": 402,
    "terms": [
      "rankings"
    ],
    "text": "    rankings: dict[str, dict[str, Any]],"
  },
  {
    "line": 408,
    "terms": [
      "subclass"
    ],
    "text": "    allowed_subclasses = set(config.allowed_subclasses)"
  },
  {
    "line": 410,
    "terms": [
      "gross_exposure"
    ],
    "text": "    gross_exposure = float(config.gross_exposure)"
  },
  {
    "line": 417,
    "terms": [
      "subclass"
    ],
    "text": "        subclass = regime_info.get(\"subclass\") or \"NO_SUBCLASS\""
  },
  {
    "line": 419,
    "terms": [
      "return"
    ],
    "text": "        spx_return = close_to_close_return(spx, date, next_date) or 0.0"
  },
  {
    "line": 421,
    "terms": [
      "rankings"
    ],
    "text": "        ranked = rankings.get(date, {})"
  },
  {
    "line": 425,
    "terms": [
      "SIDEWAYS"
    ],
    "text": "            regime == \"SIDEWAYS\""
  },
  {
    "line": 426,
    "terms": [
      "subclass"
    ],
    "text": "            and subclass in allowed_subclasses"
  },
  {
    "line": 428,
    "terms": [
      "gross_exposure"
    ],
    "text": "            and gross_exposure > 0"
  },
  {
    "line": 433,
    "terms": [
      "return"
    ],
    "text": "        portfolio_return = 0.0"
  },
  {
    "line": 436,
    "terms": [
      "selected"
    ],
    "text": "            selected = candidates[:top_n]"
  },
  {
    "line": 437,
    "terms": [
      "gross_exposure",
      "selected"
    ],
    "text": "            weight = gross_exposure / len(selected)"
  },
  {
    "line": 439,
    "terms": [
      "selected"
    ],
    "text": "            for candidate in selected:"
  },
  {
    "line": 440,
    "terms": [
      "return"
    ],
    "text": "                raw_return = candidate[\"one_day_return\"]"
  },
  {
    "line": 441,
    "terms": [
      "return"
    ],
    "text": "                contribution = weight * raw_return"
  },
  {
    "line": 442,
    "terms": [
      "return"
    ],
    "text": "                portfolio_return += contribution"
  },
  {
    "line": 448,
    "terms": [
      "return"
    ],
    "text": "                    \"raw_return\": raw_return,"
  },
  {
    "line": 449,
    "terms": [
      "return"
    ],
    "text": "                    \"raw_return_pct\": pct_display(raw_return),"
  },
  {
    "line": 458,
    "terms": [
      "subclass"
    ],
    "text": "            \"subclass\": subclass,"
  },
  {
    "line": 461,
    "terms": [
      "selected"
    ],
    "text": "            \"selected_count\": len(holdings),"
  },
  {
    "line": 462,
    "terms": [
      "gross_exposure"
    ],
    "text": "            \"gross_exposure\": gross_exposure if is_active else 0.0,"
  },
  {
    "line": 463,
    "terms": [
      "return"
    ],
    "text": "            \"portfolio_return\": portfolio_return,"
  },
  {
    "line": 464,
    "terms": [
      "return"
    ],
    "text": "            \"portfolio_return_pct\": pct_display(portfolio_return),"
  },
  {
    "line": 465,
    "terms": [
      "return"
    ],
    "text": "            \"spx_return\": spx_return,"
  },
  {
    "line": 466,
    "terms": [
      "return"
    ],
    "text": "            \"spx_return_pct\": pct_display(spx_return),"
  },
  {
    "line": 470,
    "terms": [
      "return"
    ],
    "text": "    return records"
  },
  {
    "line": 480,
    "terms": [
      "return"
    ],
    "text": "    daily_returns = [r[\"portfolio_return\"] for r in records]"
  },
  {
    "line": 482,
    "terms": [
      "return"
    ],
    "text": "    active_returns = [r[\"portfolio_return\"] for r in active_records]"
  },
  {
    "line": 483,
    "terms": [
      "return"
    ],
    "text": "    active_spx_returns = [r[\"spx_return\"] for r in active_records]"
  },
  {
    "line": 486,
    "terms": [
      "return"
    ],
    "text": "        equity *= 1.0 + record[\"portfolio_return\"]"
  },
  {
    "line": 489,
    "terms": [
      "return"
    ],
    "text": "    full_strategy_return = equity_curve[-1] / config.initial_equity - 1.0"
  },
  {
    "line": 490,
    "terms": [
      "return"
    ],
    "text": "    full_spx_return = compound_return(r[\"spx_return\"] for r in records)"
  },
  {
    "line": 491,
    "terms": [
      "return"
    ],
    "text": "    active_strategy_return = compound_return(active_returns)"
  },
  {
    "line": 492,
    "terms": [
      "return"
    ],
    "text": "    active_spx_return = compound_return(active_spx_returns)"
  },
  {
    "line": 494,
    "terms": [
      "return"
    ],
    "text": "    wins = [r for r in active_records if r[\"portfolio_return\"] > 0]"
  },
  {
    "line": 495,
    "terms": [
      "return"
    ],
    "text": "    losses = [r for r in active_records if r[\"portfolio_return\"] < 0]"
  },
  {
    "line": 497,
    "terms": [
      "return"
    ],
    "text": "    return {"
  },
  {
    "line": 498,
    "terms": [
      "MA_CONFLICT",
      "SIDEWAYS"
    ],
    "text": "        \"name\": \"E1R_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE\","
  },
  {
    "line": 499,
    "terms": [
      "subclass"
    ],
    "text": "        \"allowed_subclasses\": list(config.allowed_subclasses),"
  },
  {
    "line": 501,
    "terms": [
      "gross_exposure"
    ],
    "text": "        \"gross_exposure\": config.gross_exposure,"
  },
  {
    "line": 511,
    "terms": [
      "return"
    ],
    "text": "        \"full_period_strategy_return_pct\": pct_display(full_strategy_return),"
  },
  {
    "line": 512,
    "terms": [
      "return"
    ],
    "text": "        \"full_period_spx_return_pct\": pct_display(full_spx_return),"
  },
  {
    "line": 513,
    "terms": [
      "return"
    ],
    "text": "        \"full_period_excess_vs_spx_pct\": pct_display(full_strategy_return - full_spx_return),"
  },
  {
    "line": 515,
    "terms": [
      "return"
    ],
    "text": "        \"active_window_strategy_return_pct\": pct_display(active_strategy_return),"
  },
  {
    "line": 516,
    "terms": [
      "return"
    ],
    "text": "        \"active_window_spx_return_pct\": pct_display(active_spx_return),"
  },
  {
    "line": 517,
    "terms": [
      "return"
    ],
    "text": "        \"active_window_excess_vs_spx_pct\": pct_display(active_strategy_return - active_spx_return),"
  },
  {
    "line": 520,
    "terms": [
      "return"
    ],
    "text": "        \"profit_factor\": profit_factor(daily_returns),"
  },
  {
    "line": 521,
    "terms": [
      "return"
    ],
    "text": "        \"sharpe\": sharpe_ratio(daily_returns),"
  },
  {
    "line": 529,
    "terms": [
      "return"
    ],
    "text": "        \"avg_active_day_return_pct\": pct_display(mean_or_none(active_returns)),"
  },
  {
    "line": 530,
    "terms": [
      "return"
    ],
    "text": "        \"median_active_day_return_pct\": pct_display(median_or_none(active_returns)),"
  },
  {
    "line": 549,
    "terms": [
      "rankings"
    ],
    "text": "    rankings = build_daily_rankings(stocks, spx, regimes, intervals, config)"
  },
  {
    "line": 550,
    "terms": [
      "rankings"
    ],
    "text": "    records = run_daily_rebalanced_sidecar(rankings, spx, regimes, intervals, config)"
  },
  {
    "line": 554,
    "terms": [
      "subclass"
    ],
    "text": "    subclass_counts: dict[str, int] = {}"
  },
  {
    "line": 558,
    "terms": [
      "subclass"
    ],
    "text": "        subclass = record[\"subclass\"]"
  },
  {
    "line": 560,
    "terms": [
      "SIDEWAYS"
    ],
    "text": "        if regime == \"SIDEWAYS\":"
  },
  {
    "line": 561,
    "terms": [
      "subclass"
    ],
    "text": "            subclass_counts[subclass] = subclass_counts.get(subclass, 0) + 1"
  },
  {
    "line": 563,
    "terms": [
      "return"
    ],
    "text": "    return {"
  },
  {
    "line": 569,
    "terms": [
      "subclass"
    ],
    "text": "            \"allowed_subclasses\": list(config.allowed_subclasses),"
  },
  {
    "line": 571,
    "terms": [
      "gross_exposure"
    ],
    "text": "            \"gross_exposure\": config.gross_exposure,"
  },
  {
    "line": 590,
    "terms": [
      "subclass"
    ],
    "text": "            \"sideways_subclass_counts\": subclass_counts,"
  }
]
```

## Function Source Heads

### `build_daily_rankings` line `356`

```python
def build_daily_rankings(
    stocks: dict[str, dict[str, Any]],
    spx: dict[str, Any],
    regimes: dict[str, dict[str, Any]],
    intervals: Sequence[tuple[str, str]],
    config: E1RSidecarConfig,
) -> dict[str, dict[str, Any]]:
    rankings: dict[str, dict[str, Any]] = {}

    for date, next_date in intervals:
        regime_info = regimes.get(date, {})
        if regime_info.get("regime") != "SIDEWAYS":
            continue

        candidates: list[dict[str, Any]] = []

        for asset in stocks.values():
            if date not in asset["by_date"] or next_date not in asset["by_date"]:
                continue

            candidate = score_candidate(asset, spx, date, config)
            if candidate is None:
                continue

            one_day_return = close_to_close_return(asset, date, next_date)
            if one_day_return is None:
                continue

            candidate["one_day_return"] = one_day_return
            candidates.append(candidate)

        candidates.sort(key=lambda x: x["score"], reverse=True)

        rankings[date] = {
            "date": date,
            "next_date": next_date,
            "regime": "SIDEWAYS",
            "subclass": regime_info.get("subclass") or "NO_SUBCLASS",
            "candidate_count": len(candidates),
            "candidates": candidates,
        }

    return rankings
```

### `run_daily_rebalanced_sidecar` line `401`

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

### `summarize_sidecar` line `473`

```python
def summarize_sidecar(
    records: Sequence[dict[str, Any]],
    config: E1RSidecarConfig,
) -> dict[str, Any]:
    equity = config.initial_equity
    equity_curve = [equity]

    daily_returns = [r["portfolio_return"] for r in records]
    active_records = [r for r in records if r["is_active"]]
    active_returns = [r["portfolio_return"] for r in active_records]
    active_spx_returns = [r["spx_return"] for r in active_records]

    for record in records:
        equity *= 1.0 + record["portfolio_return"]
        equity_curve.append(equity)

    full_strategy_return = equity_curve[-1] / config.initial_equity - 1.0
    full_spx_return = compound_return(r["spx_return"] for r in records)
    active_strategy_return = compound_return(active_returns)
    active_spx_return = compound_return(active_spx_returns)

    wins = [r for r in active_records if r["portfolio_return"] > 0]
    losses = [r for r in active_records if r["portfolio_return"] < 0]

    return {
        "name": "E1R_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE",
        "allowed_subclasses": list(config.allowed_subclasses),
        "top_n": config.top_n,
        "gross_exposure": config.gross_exposure,
        "excluded_symbols": list(config.excluded_symbols),

        "total_days": len(records),
        "active_days": len(active_records),
        "exposure_pct_full_period": (
            100.0 * len(active_records) / len(records)
            if records else None
        ),

        "full_period_strategy_return_pct": pct_display(full_strategy_return),
        "full_period_spx_return_pct": pct_display(full_spx_return),
        "full_period_excess_vs_spx_pct": pct_display(full_strategy_return - full_spx_return),

        "active_window_strategy_return_pct": pct_display(active_strategy_return),
        "active_window_spx_return_pct": pct_display(active_spx_return),
        "active_window_excess_vs_spx_pct": pct_display(active_strategy_return - active_spx_return),

        "max_drawdown_pct": pct_display(max_drawdown(equity_curve)),
        "profit_factor": profit_factor(daily_returns),
        "sharpe": sharpe_ratio(daily_returns),

        "active_day_win_rate_pct": (
            100.0 * len(wins) / len(active_records)
            if active_records else None
        ),
        "winning_active_days": len(wins),
        "losing_active_days": len(losses),
        "avg_active_day_return_pct": pct_display(mean_or_none(active_returns)),
        "median_active_day_return_pct": pct_display(median_or_none(active_returns)),

        "trade_count_approx": sum(len(r["holdings"]) for r in active_records),
        "equity_start": config.initial_equity,
        "equity_end": equity_curve[-1],
    }
```

### `build_e1r_sidecar_sleeve` line `538`

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

## Diagnosis

- 4A confirmed full intervals and regime/subclass classification are present.
- 4A failed because sidecar_active_count is 0 despite SIDEWAYS=241 and MA_CONFLICT=135.
- This audit inspects config defaults and activation conditions without running another export or writing E1R canonical files.
- Suspicious activation/config fields: {"allowed_subclasses": ["MA_CONFLICT"], "top_n": 10, "gross_exposure": 0.25, "min_history_days": 200, "min_price": 5.0}

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-4A-2`: Run sidecar with explicit activation config if required
- Recommended action: Based on activation audit, set only wrapper-level E1RSidecarConfig parameters needed to activate MA_CONFLICT sidecar, then rerun 4A export validation.

