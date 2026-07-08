# Stage 3.8E-2F-2C-4C-10B Direct Generator Dry-run Audit

Generated At: `2026-07-08T11:59:24.085213+00:00`

## Status

- Status: `DIRECT_GENERATOR_DRY_RUN_COMPLETE_NO_CANONICAL_EXPORTS_WRITTEN`
- Strategy files unchanged: `True`
- Canonical export existence unchanged: `True`

## Diagnosis

- Sidecar build ok: False.
- Sidecar record candidate lists: 0.
- Compose attempts ok: 0.
- Manual extract non-empty attempts: 0.
- Strategy files unchanged: True.
- Canonical export existence unchanged: True.
- No complete portfolio equity preview yet; likely missing 5Y core_daily_equity_records from E1 core backtest.

## Paths

```json
{
  "stock_dir": "data/research/e1_5y/raw/stocks",
  "spx_path": "data/research/e1_5y/raw/indices/SPX.json",
  "regime_path": "data/research/e1_5y/regimes/spx_regime_daily.json",
  "stock_dir_exists": true,
  "stock_file_count": 542,
  "spx_path_exists": true,
  "regime_path_exists": true
}
```

## Config

```json
null
```

## Sidecar Build Summary

```json
null
```

## Core Candidates

```json
null
```

## Compose Attempts

```json
null
```

## Manual Extract Attempts

```json
null
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10C`: Generate or recover 5Y E1 core daily equity records
- Recommended action: If 10B confirms sidecar_records are available but composer cannot create full E1R equity, build the missing 5Y core_daily_equity_records from frozen E1 backtest logic, then compose E1R v0.2.

