# Stage 3.8E-2F-2C-4C-10A Direct Generator Function Audit

Generated At: `2026-07-08T11:53:29.173693+00:00`

## Status

- Status: `DIRECT_GENERATOR_FUNCTION_AUDIT_COMPLETE_NO_EXPORTS_WRITTEN`
- Dashboard changed: `False`
- Exports changed: `False`
- Workflow changed: `False`
- Strategy logic changed: `False`
- Canonical exports written: `False`
- Long backtest run: `False`

## Diagnosis

- e1r_sidecar_sleeve.py imports successfully.
- e1r_composer.py imports successfully.
- Top sidecar function candidate: run_daily_rebalanced_sidecar in src/engine/e1r_sidecar_sleeve.py line 401 score=15.
- Top composer function candidate: extract_core_interval_returns in src/engine/e1r_composer.py line 94 score=47.
- Next stage should inspect the full source of top sidecar candidates and build a dry-run call with real 5Y data, allowing long runtime if needed.

## Sidecar Function Candidates

- score `15` · `src/engine/e1r_sidecar_sleeve.py::run_daily_rebalanced_sidecar` line `401` args `rankings, spx, regimes, intervals, config` returns `list[dict[str, Any]]`
  - terms: `spx_return, spx_return_pct, next_date, date, portfolio, E1RSidecarConfig, SIDEWAYS`
- score `13` · `src/engine/e1r_sidecar_sleeve.py::build_e1r_sidecar_sleeve` line `538` args `stock_dir, spx_path, regime_path, config` returns `dict[str, Any]`
  - terms: `next_date, date, equity, E1RSidecarConfig, SIDEWAYS`
- score `12` · `src/engine/e1r_sidecar_sleeve.py::build_daily_rankings` line `356` args `stocks, spx, regimes, intervals, config` returns `dict[str, dict[str, Any]]`
  - terms: `next_date, date, E1RSidecarConfig, SIDEWAYS`
- score `10` · `src/engine/e1r_sidecar_sleeve.py::close_to_close_return` line `234` args `asset, date, next_date` returns `Optional[float]`
  - terms: `next_date, date`
- score `8` · `src/engine/e1r_sidecar_sleeve.py::summarize_sidecar` line `473` args `records, config` returns `dict[str, Any]`
  - terms: `spx_return, spx_return_pct, daily_return, portfolio, equity, E1RSidecarConfig, MA_CONFLICT, SIDEWAYS`
- score `2` · `src/engine/e1r_sidecar_sleeve.py::score_candidate` line `254` args `asset, spx, date, config` returns `Optional[dict[str, Any]]`
  - terms: `date, E1RSidecarConfig`
- score `2` · `src/engine/e1r_sidecar_sleeve.py::build_backtest_intervals` line `342` args `spx, regimes, config` returns `list[tuple[str, str]]`
  - terms: `date, E1RSidecarConfig`
- score `1` · `src/engine/e1r_sidecar_sleeve.py::max_drawdown` line `87` args `equity_values` returns `Optional[float]`
  - terms: `equity`
- score `1` · `src/engine/e1r_sidecar_sleeve.py::sharpe_ratio` line `102` args `daily_returns` returns `Optional[float]`
  - terms: `daily_return`
- score `1` · `src/engine/e1r_sidecar_sleeve.py::profit_factor` line `114` args `daily_returns` returns `Optional[float]`
  - terms: `daily_return`
- score `1` · `src/engine/e1r_sidecar_sleeve.py::load_asset` line `126` args `path` returns `dict[str, Any]`
  - terms: `date`
- score `1` · `src/engine/e1r_sidecar_sleeve.py::load_stock_universe` line `158` args `stock_dir, config` returns `tuple[dict[str, dict[str, Any]], list[str]]`
  - terms: `E1RSidecarConfig`
- score `1` · `src/engine/e1r_sidecar_sleeve.py::load_regimes` line `182` args `path` returns `dict[str, dict[str, Any]]`
  - terms: `date`
- score `1` · `src/engine/e1r_sidecar_sleeve.py::history_closes` line `192` args `asset, date, length` returns `Optional[list[float]]`
  - terms: `date`
- score `0` · `src/engine/e1r_sidecar_sleeve.py::safe_float` line `53` args `value` returns `Optional[float]`
  - terms: ``
- score `0` · `src/engine/e1r_sidecar_sleeve.py::pct_display` line `65` args `decimal_return` returns `Optional[float]`
  - terms: ``
- score `0` · `src/engine/e1r_sidecar_sleeve.py::compound_return` line `69` args `returns` returns `float`
  - terms: ``
- score `0` · `src/engine/e1r_sidecar_sleeve.py::mean_or_none` line `77` args `values` returns `Optional[float]`
  - terms: ``
- score `0` · `src/engine/e1r_sidecar_sleeve.py::median_or_none` line `82` args `values` returns `Optional[float]`
  - terms: ``
- score `0` · `src/engine/e1r_sidecar_sleeve.py::moving_average` line `199` args `values, length` returns `Optional[float]`
  - terms: ``

## Composer Function Candidates

- score `47` · `src/engine/e1r_composer.py::extract_core_interval_returns` line `94` args `core_daily_equity_records, sidecar_records` returns `list[dict[str, Any]]`
  - terms: `sidecar_records, sidecar_return, sidecar_return_pct, sidecar_holdings, sidecar_active, sidecar_selected_count, sidecar_gross_exposure, combined_return, core_return, core_return_pct, spx_return, spx_return_pct, next_date, date, daily_return, daily_return_pct, portfolio, equity, extract_core_interval_returns`
- score `45` · `src/engine/e1r_composer.py::build_equity_records_from_returns` line `171` args `interval_records, initial_equity` returns `list[dict[str, Any]]`
  - terms: `sidecar_return, sidecar_return_pct, sidecar_active, sidecar_selected_count, sidecar_gross_exposure, combined_return, core_return, core_return_pct, spx_return, spx_return_pct, next_date, date, daily_return, daily_return_pct, equity, total_equity, build_equity_records_from_returns`
- score `33` · `src/engine/e1r_composer.py::compose_e1r_v0_2_variant` line `283` args `core_variant_result, sidecar_result, initial_equity` returns `dict[str, Any]`
  - terms: `sidecar_records, sidecar_return, sidecar_active, sidecar_gross_exposure, core_return, spx_return, spx_return_pct, next_date, date, equity, build_equity_records_from_returns, extract_core_interval_returns, MA_CONFLICT, UPTREND, SIDEWAYS`
- score `29` · `src/engine/e1r_composer.py::summarize_combined_variant` line `214` args `interval_records, equity_records, initial_equity` returns `dict[str, Any]`
  - terms: `sidecar_return, sidecar_return_pct, sidecar_active, combined_return, core_return, core_return_pct, spx_return, spx_return_pct, equity`
- score `1` · `src/engine/e1r_composer.py::max_drawdown` line `55` args `equity_values` returns `Optional[float]`
  - terms: `equity`
- score `1` · `src/engine/e1r_composer.py::sharpe_ratio` line `70` args `daily_returns` returns `Optional[float]`
  - terms: `daily_return`
- score `1` · `src/engine/e1r_composer.py::profit_factor` line `82` args `daily_returns` returns `Optional[float]`
  - terms: `daily_return`
- score `0` · `src/engine/e1r_composer.py::safe_float` line `31` args `value` returns `Optional[float]`
  - terms: ``
- score `0` · `src/engine/e1r_composer.py::pct_display` line `43` args `decimal_return` returns `Optional[float]`
  - terms: ``
- score `0` · `src/engine/e1r_composer.py::compound_return` line `47` args `returns` returns `float`
  - terms: ``

## Import Probe

```json
{
  "sidecar_import_ok": true,
  "sidecar_public_names": [
    "Any",
    "E1RSidecarConfig",
    "Iterable",
    "Optional",
    "Path",
    "Sequence",
    "annotations",
    "build_backtest_intervals",
    "build_daily_rankings",
    "build_e1r_sidecar_sleeve",
    "close_to_close_return",
    "compound_return",
    "dataclass",
    "drawdown_from_high_pct",
    "history_closes",
    "json",
    "load_asset",
    "load_regimes",
    "load_stock_universe",
    "math",
    "max_drawdown",
    "mean",
    "mean_or_none",
    "median",
    "median_or_none",
    "moving_average",
    "pct_display",
    "profit_factor",
    "pstdev",
    "run_daily_rebalanced_sidecar",
    "safe_float",
    "score_candidate",
    "sharpe_ratio",
    "slope_pct",
    "summarize_sidecar"
  ],
  "sidecar_functions": {
    "Any": {
      "type": "_SpecialForm",
      "signature": "(*args, **kwds)"
    },
    "E1RSidecarConfig": {
      "type": "type",
      "signature": "(start_date: 'str', end_date: 'str', allowed_subclasses: 'tuple[str, ...]' = ('MA_CONFLICT',), top_n: 'int' = 10, gross_exposure: 'float' = 0.25, min_history_days: 'int' = 200, min_price: 'float' = 5.0, initial_equity: 'float' = 100000.0, excluded_symbols: 'tuple[str, ...]' = ('VIXY',)) -> None"
    },
    "Iterable": {
      "type": "_SpecialGenericAlias",
      "signature": "(*args, **kwargs)"
    },
    "Optional": {
      "type": "_SpecialForm",
      "signature": "(*args, **kwds)"
    },
    "Path": {
      "type": "type",
      "signature": "(*args, **kwargs)"
    },
    "Sequence": {
      "type": "_SpecialGenericAlias",
      "signature": "(*args, **kwargs)"
    },
    "build_backtest_intervals": {
      "type": "function",
      "signature": "(spx: 'dict[str, Any]', regimes: 'dict[str, dict[str, Any]]', config: 'E1RSidecarConfig') -> 'list[tuple[str, str]]'"
    },
    "build_daily_rankings": {
      "type": "function",
      "signature": "(stocks: 'dict[str, dict[str, Any]]', spx: 'dict[str, Any]', regimes: 'dict[str, dict[str, Any]]', intervals: 'Sequence[tuple[str, str]]', config: 'E1RSidecarConfig') -> 'dict[str, dict[str, Any]]'"
    },
    "build_e1r_sidecar_sleeve": {
      "type": "function",
      "signature": "(stock_dir: 'Path', spx_path: 'Path', regime_path: 'Path', config: 'E1RSidecarConfig') -> 'dict[str, Any]'"
    },
    "close_to_close_return": {
      "type": "function",
      "signature": "(asset: 'dict[str, Any]', date: 'str', next_date: 'str') -> 'Optional[float]'"
    },
    "compound_return": {
      "type": "function",
      "signature": "(returns: 'Iterable[Optional[float]]') -> 'float'"
    },
    "dataclass": {
      "type": "function",
      "signature": "(cls=None, /, *, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)"
    },
    "drawdown_from_high_pct": {
      "type": "function",
      "signature": "(values: 'Optional[Sequence[float]]') -> 'Optional[float]'"
    },
    "history_closes": {
      "type": "function",
      "signature": "(asset: 'dict[str, Any]', date: 'str', length: 'int') -> 'Optional[list[float]]'"
    },
    "load_asset": {
      "type": "function",
      "signature": "(path: 'Path') -> 'dict[str, Any]'"
    },
    "load_regimes": {
      "type": "function",
      "signature": "(path: 'Path') -> 'dict[str, dict[str, Any]]'"
    },
    "load_stock_universe": {
      "type": "function",
      "signature": "(stock_dir: 'Path', config: 'E1RSidecarConfig') -> 'tuple[dict[str, dict[str, Any]], list[str]]'"
    },
    "max_drawdown": {
      "type": "function",
      "signature": "(equity_values: 'Sequence[float]') -> 'Optional[float]'"
    },
    "mean": {
      "type": "function",
      "signature": "(data)"
    },
    "mean_or_none": {
      "type": "function",
      "signature": "(values: 'Iterable[Optional[float]]') -> 'Optional[float]'"
    },
    "median": {
      "type": "function",
      "signature": "(data)"
    },
    "median_or_none": {
      "type": "function",
      "signature": "(values: 'Iterable[Optional[float]]') -> 'Optional[float]'"
    },
    "moving_average": {
      "type": "function",
      "signature": "(values: 'Optional[Sequence[float]]', length: 'int') -> 'Optional[float]'"
    },
    "pct_display": {
      "type": "function",
      "signature": "(decimal_return: 'Optional[float]') -> 'Optional[float]'"
    },
    "profit_factor": {
      "type": "function",
      "signature": "(daily_returns: 'Sequence[float]') -> 'Optional[float]'"
    },
    "pstdev": {
      "type": "function",
      "signature": "(data, mu=None)"
    },
    "run_daily_rebalanced_sidecar": {
      "type": "function",
      "signature": "(rankings: 'dict[str, dict[str, Any]]', spx: 'dict[str, Any]', regimes: 'dict[str, dict[str, Any]]', intervals: 'Sequence[tuple[str, str]]', config: 'E1RSidecarConfig') -> 'list[dict[str, Any]]'"
    },
    "safe_float": {
      "type": "function",
      "signature": "(value: 'Any') -> 'Optional[float]'"
    },
    "score_candidate": {
      "type": "function",
      "signature": "(asset: 'dict[str, Any]', spx: 'dict[str, Any]', date: 'str', config: 'E1RSidecarConfig') -> 'Optional[dict[str, Any]]'"
    },
    "sharpe_ratio": {
      "type": "function",
      "signature": "(daily_returns: 'Sequence[float]') -> 'Optional[float]'"
    },
    "slope_pct": {
      "type": "function",
      "signature": "(values: 'Optional[Sequence[float]]', periods: 'int') -> 'Optional[float]'"
    },
    "summarize_sidecar": {
      "type": "function",
      "signature": "(records: 'Sequence[dict[str, Any]]', config: 'E1RSidecarConfig') -> 'dict[str, Any]'"
    }
  },
  "composer_import_ok": true,
  "composer_public_names": [
    "Any",
    "Optional",
    "Sequence",
    "annotations",
    "build_equity_records_from_returns",
    "compose_e1r_v0_2_variant",
    "compound_return",
    "copy",
    "extract_core_interval_returns",
    "math",
    "max_drawdown",
    "mean",
    "pct_display",
    "profit_factor",
    "pstdev",
    "safe_float",
    "sharpe_ratio",
    "summarize_combined_variant"
  ],
  "composer_functions": {
    "Any": {
      "type": "_SpecialForm",
      "signature": "(*args, **kwds)"
    },
    "Optional": {
      "type": "_SpecialForm",
      "signature": "(*args, **kwds)"
    },
    "Sequence": {
      "type": "_SpecialGenericAlias",
      "signature": "(*args, **kwargs)"
    },
    "build_equity_records_from_returns": {
      "type": "function",
      "signature": "(interval_records: 'Sequence[dict[str, Any]]', initial_equity: 'float') -> 'list[dict[str, Any]]'"
    },
    "compose_e1r_v0_2_variant": {
      "type": "function",
      "signature": "(core_variant_result: 'dict[str, Any]', sidecar_result: 'dict[str, Any]', initial_equity: 'float' = 100000.0) -> 'dict[str, Any]'"
    },
    "compound_return": {
      "type": "function",
      "signature": "(returns: 'Sequence[Optional[float]]') -> 'float'"
    },
    "extract_core_interval_returns": {
      "type": "function",
      "signature": "(core_daily_equity_records: 'Sequence[dict[str, Any]]', sidecar_records: 'Sequence[dict[str, Any]]') -> 'list[dict[str, Any]]'"
    },
    "max_drawdown": {
      "type": "function",
      "signature": "(equity_values: 'Sequence[float]') -> 'Optional[float]'"
    },
    "mean": {
      "type": "function",
      "signature": "(data)"
    },
    "pct_display": {
      "type": "function",
      "signature": "(decimal_return: 'Optional[float]') -> 'Optional[float]'"
    },
    "profit_factor": {
      "type": "function",
      "signature": "(daily_returns: 'Sequence[float]') -> 'Optional[float]'"
    },
    "pstdev": {
      "type": "function",
      "signature": "(data, mu=None)"
    },
    "safe_float": {
      "type": "function",
      "signature": "(value: 'Any') -> 'Optional[float]'"
    },
    "sharpe_ratio": {
      "type": "function",
      "signature": "(daily_returns: 'Sequence[float]') -> 'Optional[float]'"
    },
    "summarize_combined_variant": {
      "type": "function",
      "signature": "(in
```

## Top Function Source Heads

### `src/engine/e1r_sidecar_sleeve.py`

#### `run_daily_rebalanced_sidecar` line `401` score `15`
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

#### `build_e1r_sidecar_sleeve` line `538` score `13`
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

#### `build_daily_rankings` line `356` score `12`
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

#### `close_to_close_return` line `234` score `10`
```python
def close_to_close_return(
    asset: dict[str, Any],
    date: str,
    next_date: str,
) -> Optional[float]:
    left = asset["by_date"].get(date)
    right = asset["by_date"].get(next_date)

    if not left or not right:
        return None

    c0 = safe_float(left.get("close"))
    c1 = safe_float(right.get("close"))

    if c0 is None or c1 is None or c0 == 0:
        return None

    return c1 / c0 - 1.0
```

#### `summarize_sidecar` line `473` score `8`
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

### `src/engine/e1r_composer.py`

#### `extract_core_interval_returns` line `94` score `47`
```python
def extract_core_interval_returns(
    core_daily_equity_records: Sequence[dict[str, Any]],
    sidecar_records: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Align core daily returns to sidecar intervals by next_date.

    Returns one record per shared interval:
    {
      date,
      next_date,
      core_return,
      sidecar_return,
      spx_return,
      ...
    }
    """
    core_by_end_date = {}

    for row in core_daily_equity_records:
        date = row.get("date")
        if not date:
            continue

        r = safe_float(row.get("daily_return"))
        if r is None:
            # Some historical outputs may store pct instead of decimal.
            rp = safe_float(row.get("daily_return_pct"))
            r = None if rp is None else rp / 100.0

        if r is None:
            continue

        core_by_end_date[date] = row | {"_normalized_daily_return": r}

    aligned: list[dict[str, Any]] = []

    for sidecar in sidecar_records:
        date = sidecar.get("date")
        next_date = sidecar.get("next_date")

        if not date or not next_date:
            continue

        core = core_by_end_date.get(next_date)
        if core is None:
            continue

        core_return = safe_float(core.get("_normalized_daily_return")) or 0.0
        sidecar_return = safe_float(sidecar.get("portfolio_return")) or 0.0
        spx_return = safe_float(sidecar.get("spx_return")) or 0.0

        combined_return = (1.0 + core_return) * (1.0 + sidecar_return) - 1.0

        aligned.append({
            "date": date,
            "next_date": next_date,
            "core_end_date": next_date,
            "core_return": core_return,
            "core_return_pct": pct_display(core_return),
            "sidecar_return": sidecar_return,
            "sidecar_return_pct": pct_display(sidecar_return),
            "combined_return": combined_return,
            "combined_return_pct": pct_display(combined_return),
            "spx_return": spx_return,
            "spx_return_pct": pct_display(spx_return),
            "regime": sidecar.get("regime"),
            "subclass": sidecar.get("subclass"),
            "sidecar_active": bool(sidecar.get("is_active")),
            "sidecar_selected_count": sidecar.get("selected_count"),
            "sidecar_gross_exposure": sidecar.get("gross_exposure"),
            "sidecar_holdings": sidecar.get("holdings", []),
        })

    return aligned
```

#### `build_equity_records_from_returns` line `171` score `45`
```python
def build_equity_records_from_returns(
    interval_records: Sequence[dict[str, Any]],
    initial_equity: float,
) -> list[dict[str, Any]]:
    equity = initial_equity
    peak = initial_equity
    records: list[dict[str, Any]] = []

    for row in interval_records:
        r = safe_float(row.get("combined_return")) or 0.0
        equity *= 1.0 + r
        peak = max(peak, equity)

        drawdown = equity / peak - 1.0 if peak > 0 else 0.0

        records.append({
            "date": row["next_date"],
            "interval_start_date": row["date"],
            "interval_end_date": row["next_date"],
            "total_equity": equity,
            "equity": equity,
            "daily_return": r,
            "daily_return_pct": pct_display(r),
            "drawdown": drawdown,
            "drawdown_pct": pct_display(drawdown),

            "core_return": row["core_return"],
            "core_return_pct": row["core_return_pct"],
            "sidecar_return": row["sidecar_return"],
            "sidecar_return_pct": row["sidecar_return_pct"],
            "spx_return": row["spx_return"],
            "spx_return_pct": row["spx_return_pct"],

            "spx_regime": row.get("regime"),
            "sideways_subclass": row.get("subclass"),
            "sidecar_active": row.get("sidecar_active"),
            "sidecar_selected_count": row.get("sidecar_selected_count"),
            "sidecar_gross_exposure": row.get("sidecar_gross_exposure"),
        })

    return records
```

#### `compose_e1r_v0_2_variant` line `283` score `33`
```python
def compose_e1r_v0_2_variant(
    core_variant_result: dict[str, Any],
    sidecar_result: dict[str, Any],
    initial_equity: float = 100000.0,
) -> dict[str, Any]:
    core_records = core_variant_result.get("daily_equity_records", [])
    sidecar_records = sidecar_result.get("records", [])

    interval_records = extract_core_interval_returns(core_records, sidecar_records)
    equity_records = build_equity_records_from_returns(interval_records, initial_equity)
    summary = summarize_combined_variant(interval_records, equity_records, initial_equity)

    result = copy.deepcopy(core_variant_result)

    sidecar_summary = sidecar_result.get("summary", {}) or {}

    result.update({
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "strategy_variant": "E1R_regime_aware_v0_2_formal_sidecar_sleeve",
        "version": "E1R-v0.2-formal-sidecar-sleeve",
        "research_status": "FORMAL_SIDECAR_SLEEVE_ENGINE",
        "core_total_trades": core_variant_result.get("total_trades"),
        "sidecar_trade_count_approx": sidecar_summary.get("trade_count_approx"),
        "combined_trade_count_note": (
            "total_trades remains inherited from E1R v0.1 core; "
            "sidecar_trade_count_approx counts daily basket holdings and is not "
            "stateful round-trip trade count."
        ),
        "e1r_v0_2_composition": {
            "core_variant": "E1R_REGIME_AWARE_V0_1",
            "sidecar_engine": sidecar_result.get("engine"),
            "sidecar_version": sidecar_result.get("version"),
            "alignment": "core daily return ending at next_date aligned to sidecar date->next_date interval",
            "composition_formula": "(1 + core_return) * (1 + sidecar_return) - 1",
            "sidecar_config": sidecar_result.get("config", {}),
            "sidecar_sample": sidecar_result.get("sample", {}),
            "sidecar_summary": sidecar_result.get("summary", {}),
            "combined_summary": summary,
        },
        "daily_equity_records": equity_records,
        "daily_equity_record_count": len(equity_records),
        "e1r_v0_2_interval_records_sample": {
            "first_5": interval_records[:5],
            "last_5": interval_records[-5:],
        },
    })

    # Override summary-level fields with formal combined values.
    for key in (
        "total_return_pct",
        "spx_return_pct",
        "alpha_pct",
        "max_drawdown_pct",
        "profit_factor",
        "sharpe_ratio",
    ):
        if key in summary:
            result[key] = summary[key]

    result["total_days"] = summary["total_days"]
    result["sidecar_active_days"] = summary["sidecar_active_days"]
    result["sidecar_active_by_regime"] = summary["sidecar_active_by_regime"]
    result["sidecar_active_by_subclass"] = summary["sidecar_active_by_subclass"]
    result["sidecar_simple_contribution_by_regime_pct"] = summary["sidecar_simple_contribution_by_regime_pct"]
    result["sidecar_simple_contribution_by_subclass_pct"] = summary["sidecar
```

#### `summarize_combined_variant` line `214` score `29`
```python
def summarize_combined_variant(
    interval_records: Sequence[dict[str, Any]],
    equity_records: Sequence[dict[str, Any]],
    initial_equity: float,
) -> dict[str, Any]:
    combined_returns = [safe_float(r.get("combined_return")) or 0.0 for r in interval_records]
    core_returns = [safe_float(r.get("core_return")) or 0.0 for r in interval_records]
    sidecar_returns = [safe_float(r.get("sidecar_return")) or 0.0 for r in interval_records]
    spx_returns = [safe_float(r.get("spx_return")) or 0.0 for r in interval_records]

    equity_curve = [initial_equity] + [
        safe_float(r.get("equity")) or initial_equity for r in equity_records
    ]

    total_return = compound_return(combined_returns)
    core_return = compound_return(core_returns)
    sidecar_return = compound_return(sidecar_returns)
    spx_return = compound_return(spx_returns)

    active_records = [r for r in interval_records if r.get("sidecar_active")]

    active_by_regime: dict[str, int] = {}
    active_by_subclass: dict[str, int] = {}
    contribution_by_regime: dict[str, float] = {}
    contribution_by_subclass: dict[str, float] = {}

    for row in interval_records:
        regime = row.get("regime") or "NO_REGIME"
        subclass = row.get("subclass") or "NO_SUBCLASS"
        sidecar_return_row = safe_float(row.get("sidecar_return")) or 0.0

        contribution_by_regime[regime] = contribution_by_regime.get(regime, 0.0) + sidecar_return_row
        contribution_by_subclass[subclass] = contribution_by_subclass.get(subclass, 0.0) + sidecar_return_row

        if row.get("sidecar_active"):
            active_by_regime[regime] = active_by_regime.get(regime, 0) + 1
            active_by_subclass[subclass] = active_by_subclass.get(subclass, 0) + 1

    return {
        "total_return_pct": pct_display(total_return),
        "core_return_pct": pct_display(core_return),
        "sidecar_return_pct": pct_display(sidecar_return),
        "spx_return_pct": pct_display(spx_return),
        "alpha_pct": pct_display(total_return - spx_return),
        # Match legacy engine convention:
        # max_drawdown_pct is reported as positive magnitude, e.g. 25.90 not -25.90.
        "max_drawdown_pct": abs(pct_display(max_drawdown(equity_curve)) or 0.0),
        "profit_factor": profit_factor(combined_returns),
        "sharpe_ratio": sharpe_ratio(combined_returns),
        "daily_win_rate_pct": (
            100.0 * sum(1 for r in combined_returns if r > 0) / len(combined_returns)
            if combined_returns else None
        ),
        "total_days": len(interval_records),
        "daily_equity_record_count": len(equity_records),
        "sidecar_active_days": len(active_records),
        "sidecar_active_by_regime": active_by_regime,
        "sidecar_active_by_subclass": active_by_subclass,
        "sidecar_simple_contribution_by_regime_pct": {
            k: pct_display(v)
            for k, v in contribution_by_regime.items()
        },
        "sidecar_simple_contribution_by_sub
```

#### `max_drawdown` line `55` score `1`
```python
def max_drawdown(equity_values: Sequence[float]) -> Optional[float]:
    if not equity_values:
        return None

    peak = equity_values[0]
    worst = 0.0

    for value in equity_values:
        peak = max(peak, value)
        if peak > 0:
            worst = min(worst, value / peak - 1.0)

    return worst
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10B`: Prototype direct sidecar/composer dry-run call
- Recommended action: Use the top sidecar function signatures from this audit to call the frozen sidecar generator with data/research/e1_5y raw prices and regimes. First run dry-run summary only; then export canonical E1R portfolio equity only if metrics match frozen summary.

