# Stage 3.8E-2F-2C-4C-8 Dry-run Generation Path Audit

Generated At: `2026-07-08T11:44:38.940774+00:00`

## Status

- Status: `DRY_RUN_GENERATION_PATH_AUDIT_COMPLETE_NO_CANONICAL_EXPORTS_WRITTEN`
- Dashboard changed: `False`
- Exports changed: `False`
- Workflow changed: `False`
- Strategy logic changed: `False`
- Canonical exports written: `False`
- Long backtest run: `False`

## Summary

- core_sources_count: `6`
- sidecar_sources_count: `2`
- attempt_count: `0`
- ok_nonempty_attempt_count: `0`
- decision: `PERSISTED_INPUTS_INSUFFICIENT_NEED_FROZEN_GENERATOR_DRY_RUN`

## Frozen Metric Targets

```json
{
  "total_return_pct": 116.7435999134756,
  "spx_return_pct": 76.844174428316,
  "alpha_pct": 39.89942548515961,
  "max_drawdown_pct": 25.904809362815108,
  "profit_factor": 1.1919630955509348,
  "sharpe_ratio": 0.7957270568329264
}
```

## Diagnosis

- Persisted core source candidates found: 6.
- Persisted sidecar source candidates found: 2.
- Non-empty interval generation attempts from persisted inputs: 0.
- Decision: PERSISTED_INPUTS_INSUFFICIENT_NEED_FROZEN_GENERATOR_DRY_RUN.
- If persisted inputs are insufficient, next step should run frozen generator path in controlled dry-run/long-backtest mode and write only new canonical exports after metric validation.

## Next Stage

- `Stage 3.8E-2F-2C-4C-9`: Run controlled frozen generator / long backtest export for canonical 5Y equity curves
- Recommended action: Allow controlled generation because persisted sidecar/interval records are unavailable. Write only new canonical export files and validate against frozen E1R metrics before dashboard patch.

