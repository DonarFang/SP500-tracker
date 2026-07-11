# E1R K2 R17A-1 Candidate Trace Boundary Architecture

Generated UTC: 2026-07-11T11:38:25.905719+00:00

## Required semantic order

1. Eligibility record finalized
2. Pre-rank candidate collection created
3. Rank order finalized
4. Top3 selection finalized
5. Position sizing begins
6. Pending-order mutation begins

## Enforcement

- A trace point is not proven merely because a variable is first referenced.
- Initialization assignments such as None or [] do not prove a finalized boundary.
- Position sizing must be located after final candidate selection and before pending-order mutation.
- Pending-order initialization does not count as pending-order mutation.
- All trace instrumentation remains forbidden until every boundary is source-proven.
