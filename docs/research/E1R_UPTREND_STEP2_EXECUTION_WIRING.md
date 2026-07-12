# E1R UPTREND Step 2 — Execution Wiring

## Decision

`PASS_UPTREND_STEP2_EXECUTION_WIRING`

## Fixed plan

- Step 1: Decision equivalence — PASS
- Step 2: Execution wiring — PASS
- Step 3: Formal replacement — pending

## Boundary

A thin adapter translates OrderIntent into the existing legacy pending/T+1 execution path. Existing REDUCE and EXIT payloads are lifted to OrderIntent and restored without changing their frozen semantics.

## Validation

- Adapter disabled vs enabled result equivalence
- Adapter disabled vs enabled JSONL byte equivalence
- Window: 2021-06-01 through 2021-12-31
- BUY executions: 10
- EXIT executions: 7
- REDUCE executions: 11
- No full 5Y run

## Exclusions

- No new execution engine
- No AccountState redesign
- No Market Gate or strategy change
- No ADD or SIDEWAYS work

## Next

UPTREND STEP 3 — FORMAL REPLACEMENT
