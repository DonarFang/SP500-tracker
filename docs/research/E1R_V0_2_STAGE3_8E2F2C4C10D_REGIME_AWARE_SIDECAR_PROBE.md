# Stage 3.8E-2F-2C-4C-10D-R Regime-aware Sidecar Probe

Generated At: `2026-07-08T12:07:23.454135+00:00`

## Principle

- 5Y window includes multiple market regimes.
- Full E1R equity curve should cover the full 5Y interval window.
- Sidecar exposure should only be active in its eligible market regime/subclass.
- Therefore active sidecar count and full interval count must be validated separately.

## Status

- Status: `REGIME_AWARE_SIDECAR_PROBE_COMPLETE_NO_EXPORTS_WRITTEN`
- Strategy files unchanged: `True`
- Canonical existence unchanged: `True`

## Diagnosis

- import_sidecar: True.
- signatures: True.
- make_config: False.
- make_config_error: TypeError: __init__() missing 2 required positional arguments: 'start_date' and 'end_date'.
- load_spx: not_run.
- load_regimes: not_run.
- load_stock_universe: not_run.
- build_backtest_intervals: not_run.
- build_daily_rankings: not_run.
- run_daily_rebalanced_sidecar: not_run.
- summarize_sidecar: not_run.
- build_e1r_sidecar_sleeve: not_run.

## Expected Context

```json
{
  "full_intervals_expected_approx": "about 1258-1261",
  "sideways_expected_approx": 241,
  "ma_conflict_expected_approx": 135,
  "sidecar_active_expected_approx": 135,
  "principle": "Sidecar is regime-aware. It should not be active across all 5Y intervals; full E1R equity is full-window, sidecar exposure is conditional."
}
```

## Steps

```json
{
  "import_sidecar": {
    "name": "import_sidecar",
    "ok": true,
    "value": {
      "module": "<module 'src.engine.e1r_sidecar_sleeve' from '/Users/dongfang/Downloads/sp500-tracker-v13/src/engine/e1r_sidecar_sleeve.py'>",
      "public_names": [
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
      ]
    }
  },
  "signatures": {
    "name": "signatures",
    "ok": true,
    "value": {
      "E1RSidecarConfig": "(start_date: 'str', end_date: 'str', allowed_subclasses: 'tuple[str, ...]' = ('MA_CONFLICT',), top_n: 'int' = 10, gross_exposure: 'float' = 0.25, min_history_days: 'int' = 200, min_price: 'float' = 5.0, initial_equity: 'float' = 100000.0, excluded_symbols: 'tuple[str, ...]' = ('VIXY',)) -> None",
      "load_asset": "(path: 'Path') -> 'dict[str, Any]'",
      "load_regimes": "(path: 'Path') -> 'dict[str, dict[str, Any]]'",
      "load_stock_universe": "(stock_dir: 'Path', config: 'E1RSidecarConfig') -> 'tuple[dict[str, dict[str, Any]], list[str]]'",
      "build_backtest_intervals": "(spx: 'dict[str, Any]', regimes: 'dict[str, dict[str, Any]]', config: 'E1RSidecarConfig') -> 'list[tuple[str, str]]'",
      "build_daily_rankings": "(stocks: 'dict[str, dict[str, Any]]', spx: 'dict[str, Any]', regimes: 'dict[str, dict[str, Any]]', intervals: 'Sequence[tuple[str, str]]', config: 'E1RSidecarConfig') -> 'dict[str, dict[str, Any]]'",
      "run_daily_rebalanced_sidecar": "(rankings: 'dict[str, dict[str, Any]]', spx: 'dict[str, Any]', regimes: 'dict[str, dict[str, Any]]', intervals: 'Sequence[tuple[str, str]]', config: 'E1RSidecarConfig') -> 'list[dict[str, Any]]'",
      "build_e1r_sidecar_sleeve": "(stock_dir: 'Path', spx_path: 'Path', regime_path: 'Path', config: 'E1RSidecarConfig') -> 'dict[str, Any]'"
    }
  },
  "make_config": {
    "name": "make_config",
    "ok": false,
    "error": "TypeError: __init__() missing 2 required positional arguments: 'start_date' and 'end_date'",
    "traceback_tail": "Traceback (most recent call last):\n  File \"/tmp/stage4c10d_regime_aware_sidecar_probe.py\", line 65, in safe_step\n    value = fn()\n  File \"/tmp/stage4c10d_regime_aware_sidecar_probe.py\", line 305, in make_config\n    cfg = s.E1RSidecarConfig()\nTypeError: __init__() missing 2 required positional arguments: 'start_date' and 'end_date'\n"
  }
}
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10E`: Fix first failed sidecar generator step
- Recommended action: Use the first failed granular step error above. Fix wrapper inputs/config only; do not modify frozen sidecar logic.

