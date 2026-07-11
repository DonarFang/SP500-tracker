# E1R K2 R16 Legacy UPTREND Extraction Architecture

Compacted architecture boundary document

Generated UTC: 2026-07-11T11:13:56.370541+00:00

## Authoritative evidence

Canonical detailed evidence is stored in docs/research/E1R_4C2C4E_ENGINE_K2_R16_LEGACY_UPTREND_ORDER_LOGIC_EXTRACTION_PROPOSAL.json

This architecture document does not duplicate the canonical evidence.

## Source boundary

Included:

- src/engine
- src/features

Excluded as legacy evidence:

- src/e1r_engine

## Required extraction order

1. Legacy UPTREND input boundary
2. Candidate snapshot boundary
3. Ranking and Top3 selection boundary
4. Pre-gate OrderIntent boundary
5. Existing R15 market-gate consumption boundary
6. Position-sizing boundary
7. Pending-order and T+1 execution boundary
8. Account-mutation boundary

## Mandatory equivalence controls

- Preserve candidate eligibility and exclusions.
- Preserve Leader Score inputs and ordering.
- Preserve Top3 entry semantics.
- Do not exit holdings merely because they leave Top3.
- Preserve BUY, ADD, HOLD, REDUCE, and EXIT precedence.
- Preserve maximum live holdings of 3.
- Consume MarketGateDecision without recomputation.
- Preserve pending-order and T+1 execution semantics.
- Keep account mutation outside UptrendCore decision generation.

## R17 boundary

R17 may propose golden traces for inputs and candidate snapshots.
R17 may not implement candidate extraction or strategy behavior.
