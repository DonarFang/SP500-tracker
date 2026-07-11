# K2-R19 Runtime Trace Equivalence

## Decision

`PASS_RUNTIME_TRACE_EQUIVALENCE`

## Stage status

- K2-R17 — Legacy execution contract proof: PASS
- K2-R18 — Read-only trace instrumentation: PASS_STATIC
- K2-R19 — Runtime trace equivalence: PASS

No subordinate stage numbering is used.

## Assumptions contract

- Captured simulation calls: 9
- E1R candidates: 3
- Unique contracts: 1
- Contract proven: true
- Contract hash: `7a9fef9291fad51b8285ea9fc4d0bfa0ad2bb91404c6267fff621fb2cf2ad6da`

The comparison function later raised a formatting error while
processing the synthetic capture result. This occurred after the
unique E1R assumptions contract had been captured and therefore does
not invalidate the contract proof.

## Golden runtime window

- Window: 2021-06-01 through 2021-12-31
- Simulation days: 150
- Closed trades: 10

### BUY path

- Symbol: AVGO
- Signal date: 2021-12-22
- Execution date: 2021-12-23
- Entry type: E1R_UPTREND_CONFIRMED
- Chain: TP04 → TP06 → TP07 → TP08

### REDUCE path

- Symbol: CPT
- Signal date: 2021-08-09
- Execution date: 2021-08-10
- Chain: TP09 → TP10B

### EXIT path

- Symbol: HD
- Signal date: 2021-12-21
- Execution date: 2021-12-22
- Chain: TP09 → TP10A

## Runtime equivalence

- Disabled result hash:
  `213a9394f7163f2c8a486f935d7de3401b6b0fc3e72d9c0ff244b07bdcee35c3`
- Enabled result hash:
  `213a9394f7163f2c8a486f935d7de3401b6b0fc3e72d9c0ff244b07bdcee35c3`
- Recursive result differences: 0
- Trace records: 832
- Valid record hashes: 832
- Invalid record hashes: 0
- Unknown trace IDs: 0
- T-to-T+1 ordering: PASS
- Protected source changes: 0

## Nonblocking coverage gaps

- Emerging-entry branch: NOT_OBSERVED
- Capacity-block semantic observability: NOT_COVERED

Neither gap blocks the R19 objective, which is to establish that
read-only tracing does not alter strategy or account results across
the BUY, REDUCE and EXIT side-effect paths.

## Next stage

`K2-R20-UPTREND-CORE-EXTRACTION`
