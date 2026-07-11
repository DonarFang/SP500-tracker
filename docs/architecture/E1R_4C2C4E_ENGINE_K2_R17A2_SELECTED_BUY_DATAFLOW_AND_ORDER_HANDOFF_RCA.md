# E1R K2 R17A-2 Dataflow Architecture

Generated UTC: 2026-07-11T11:43:23.537205+00:00

## Required proven chain

1. Candidate append completion
2. Exact in-place candidate sort
3. Best new-entry selection
4. Selected-buy record finalization
5. Selected-buy consumption
6. Target-size conversion
7. Order creation
8. Pending or T+1 handoff
9. Execution-date consumption

## Corrected semantics

- e1r_buy_candidates = [] is initialization, not pre-rank completion.
- e1r_buy_candidates.sort() is the ranking boundary.
- e1r_buy_candidates[0] is best-entry selection.
- No explicit Top3 truncation is assumed without source evidence.
- max_pos=3 remains the proven portfolio-capacity contract.

## Instrumentation restriction

- No instrumentation may be implemented until the complete selected-buy to T+1 chain is proven.
