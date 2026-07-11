# E1R K2 R17 Candidate Boundary Architecture

Generated UTC: 2026-07-11T11:24:28.073133+00:00

## Authoritative report

docs/research/E1R_4C2C4E_ENGINE_K2_R17_LEGACY_UPTREND_INPUT_AND_CANDIDATE_BOUNDARY_GOLDEN_TRACE_PROPOSAL.json

## Boundary sequence

1. SIMULATION_INPUT
2. RAW_UNIVERSE
3. ELIGIBILITY_FILTER
4. PRE_RANK_CANDIDATE_SNAPSHOT
5. RANKED_CANDIDATE_SNAPSHOT
6. TOP3_ENTRY_SELECTION
7. PRE_GATE_INTENT_HANDOFF

## Separation rules

- Candidate tracing must occur before ranking truncation.
- Ranking must remain separate from Top3 entry selection.
- Existing holdings must remain separate from new-entry candidates.
- MarketGateDecision must be consumed after pre-gate intent generation.
- Candidate tracing must not mutate cash or positions.
- Account mutation and execution remain outside UptrendCore decisions.

## Maximum holdings contract

- Maximum live holdings remains 3.

## R17A restriction

- R17A may review instrumentation design.
- R17A may not implement strategy behavior.
- Any future instrumentation must be observational and removable.
