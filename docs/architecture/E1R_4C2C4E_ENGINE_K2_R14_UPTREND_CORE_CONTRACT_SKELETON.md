# E1R K2 R14 UptrendCore Contract Skeleton

- Generated UTC: `2026-07-11T09:26:13.998793+00:00`
- Stage: `4C-2C-4E-ENGINE-K2-R14-UPTREND-CORE-CONTRACT-SKELETON`

## Decision boundary

R14 is contract-skeleton only.

It does not:

- rank candidates;
- select candidates;
- generate order intents;
- size positions;
- mutate account state;
- recompute market gate state;
- call legacy backtest code;
- run a full 5Y backtest;
- integrate SIDEWAYS logic.

## Contracts added

- `CandidateSnapshot`
- `GateConsumptionTrace`
- `UptrendCoreInputs`
- `UptrendCoreOutputs`

## Existing shared contracts reused

- `MarketSnapshot`
- `MarketGateDecision`
- `AccountState`
- `OrderIntent`

## Hard constraints

- `max_live_holdings = 3`
- `gate_logic_recomputed = false`
- `strategy_logic_implemented = false`
- `account_state_mutated = false`
- `order_intents = empty`

## Next stage

`4C-2C-4E-ENGINE-K2-R15-UPTREND-CORE-GATE-CONSUMPTION-SMOKE`
