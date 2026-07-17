# FD-M3180125-SP500-TOP3-engine

## Official Shared Runtime Contract

- Contract version: `1.0.0`
- Status: `FROZEN`
- Forward track: `OPEN_ENDED`
- Seed date: `2026-06-18`
- First Forward market date: `2026-06-19`

## Frozen premise

- Engine development is complete.
- Canonical 5Y Backtest has passed.
- UPTREND formal replacement is complete.
- SIDEWAYS formal replacement is complete.
- Completed strategy development and backtest validation must not be reopened without reproducible regression evidence.

## Daily runtime order

1. `PLAN_DATE`
2. `LOAD_COMMITTED_STATE`
3. `LOAD_T1_MARKET_DATA`
4. `EXECUTE_PRIOR_PENDING`
5. `MARK_TO_MARKET_AT_CLOSE`
6. `BUILD_DAILY_DECISION_INPUTS`
7. `ROUTE_CANONICAL_DECISION`
8. `CREATE_CURRENT_PENDING`
9. `VALIDATE_ACCOUNT_AND_MAX3`
10. `WRITE_DAILY_ARTIFACTS`
11. `ATOMIC_COMMIT`
12. `UPDATE_CURRENT_MANIFEST`

## Canonical decision routing

- `UPTREND` → `E1RCoreEngine.step` using frozen `uptrend_inputs`.
- `SIDEWAYS / MA_CONFLICT` → `SidewaysCore.rank_date` → `SidewaysExecutionPolicy.build_intents`.
- Other regimes → no new risk expansion; HOLD/NOOP as applicable.

## T+1 execution

- Execute prior-day orders before current-day mark-to-market and decision generation.
- Execution priority: EXIT, REDUCE, REL_REDUCE, TP_REDUCE, ADD, BUY.
- BUY/ADD: T+1 high, fallback close, plus one-way cost.
- EXIT/REDUCE: T+1 low, fallback close, minus one-way cost.
- Global open-position limit: 3.

## Persistence and recovery

- One trading date is one atomic commit boundary.
- A committed date is never processed twice.
- Partial temporary artifacts are discarded and the date is rerun.
- Restart begins after `last_committed_date`.
- Legacy OOS state is not mutated.

## SIM_END separation

- Forward has no fixed terminal date.
- Data end never triggers liquidation.
- Backtest SIM_END is prohibited in Forward.
- The post-liquidation all-cash state is not a valid Forward Seed.

## Official modules

### `ForwardSeedLoader`

Load and validate the frozen pre-SIM_END Forward Seed.

### `ForwardDatePlanner`

Plan all uncommitted trading dates in ascending order.

### `ForwardMarketDataAdapter`

Normalize complete daily inputs without strategy decisions.

### `CanonicalDailyDecisionRouter`

Route one completed trading day to already validated canonical decision components.

### `PendingOrderLedger`

Persist T-day OrderIntents for possible T+1 execution.

### `T1ExecutionEngine`

Execute prior-trading-day pending orders and mutate AccountState using frozen execution semantics.

### `ForwardAccountRepository`

Persist the latest committed Forward account and history.

### `ForwardDailyCommitter`

Commit one complete trading day atomically.

### `OfficialForwardArtifactWriter`

Write canonical Forward artifacts for review and Dashboard.

## Freeze decision

```text
PASS_STEP2_OFFICIAL_SHARED_RUNTIME_CONTRACT_FROZEN
```

This freeze does not run Forward and does not change strategy logic.
