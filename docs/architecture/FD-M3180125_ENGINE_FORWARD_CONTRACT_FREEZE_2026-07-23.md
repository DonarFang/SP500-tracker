# FD-M3180125 Engine Forward Contract Freeze

**Status:** CANONICAL / ACTIVE
**Effective date:** 2026-07-23
**Scope:** Engine Forward contracts and legacy OOS isolation

## Runtime separation

Legacy GitHub Actions OOS remains an independent legacy track:

```text
data/oos/*
exports/oos_*
exports/e1r_v0_2_*
legacy OOS workflows
```

These paths must not supply Engine Forward market data, Seed, account state,
Regime, Market State, Market Gate, orders, fills, equity, manifests,
validation, or development conclusions.

The Engine Forward track is:

```text
data/fw_prices
→ ProductionForwardDataAdapter
→ completed Engine modules
→ Shared Runtime
→ exports/official/FD-M3180125-SP500-TOP3-engine/forward
```

## Canonical lifecycle

```text
Last normal canonical 5Y EOD: 2026-06-16
Forward Seed/account anchor: 2026-06-16
First Forward market date: 2026-06-17
Initial Forward sequence: 2026-06-17, 2026-06-18, 2026-06-22
2026-06-19: absent
```

`2026-06-22` is the first common date after `2026-06-18`; it is not
the first Forward date.

## Seed authority

```text
seed_2026-06-16 = ACTIVE / CANONICAL
seed_2026-06-18 = SUPERSEDED / AUDIT-ONLY
```

The canonical Seed is derived from canonical 5Y official evidence. It does
not use legacy GitHub OOS files and does not copy account data from the
superseded Seed.

Carried positions are DELL, HUM, and MRVL. They are not new Forward BUYs.
SIM_END liquidation is not replayed. The post-liquidation all-cash state is
not used. Unproven pending orders are not executable.

## Frozen Engine boundary

This contract freeze does not develop or modify completed Engine feature
modules, strategy logic, ranking, sizing, position management, Regime logic,
Market State, Market Gate, router behavior, or T+1 execution semantics.

After Engine Forward passes formal acceptance, it will replace the legacy
GitHub Actions OOS track as the only current Forward state source.
