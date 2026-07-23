# FD-M3180125 Independent Engine Forward GitHub Daily

**Status:** ACTIVE / PARALLEL-ISOLATED
**Effective date:** 2026-07-23

## Decision

The existing legacy GitHub Forward workflow remains unchanged and continues
to own its existing Forward outputs and equity curve.

A separate workflow is added:

```text
.github/workflows/engine-forward-daily.yml
```

It runs only the independent Engine Forward path:

```text
data/prices
→ data/fw_prices
→ ProductionForwardDataAdapter
→ Shared Runtime / Engine
→ exports/official/FD-M3180125-SP500-TOP3-engine/forward
```

## Hard separation

Engine Forward must not:

- execute or replace `run_oos.py`;
- write `data/oos/*`;
- write `exports/oos_*`;
- write `exports/e1r_v0_2_*`;
- overwrite, supply, splice, or extend the legacy equity curve;
- supply data to the current legacy Dashboard.

Legacy Forward must not supply Engine Seed, account, decisions, orders, fills,
equity, manifests, validation, or development evidence.

## Independent Engine outputs

```text
forward/runtime/current/*
forward/runtime/daily/*
forward/runtime/history/orders.jsonl
forward/runtime/history/equity_curve.json
forward/automation/current_run.json
```

The Engine equity curve remains independent until a later explicit cutover.
At that later cutover, the legacy Forward system and legacy equity curve will
be removed, and the complete Engine Forward system will become the official
replacement. That cutover is not performed here.
