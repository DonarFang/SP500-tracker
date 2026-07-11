# E1R K2 R17A-RCA Control-Flow Architecture

Generated UTC: 2026-07-11T11:51:28.413347+00:00

## Required chain

1. Candidate sort
2. Best-entry selection
3. Selected-buy finalization
4. Selected-buy consumption
5. Target-size conversion
6. BUY-order payload creation
7. buy_orders mutation
8. pending_orders handoff
9. pending-orders T+1 execution
10. holdings BUY mutation

## Evidence rule

- Comments, empty-list initialization, and variable-name occurrence do not prove boundaries.
- A boundary requires an executable AST node, complete source segment, line range, and variable linkage.

## Instrumentation restriction

- No instrumentation may be implemented unless full_chain_proven is true.
