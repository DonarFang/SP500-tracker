# E1R K2 R17A Candidate Boundary Read-Only Trace Design Review

Generated UTC: 2026-07-11T11:33:11.616699+00:00

Decision: BLOCKED_TRACE_POINT_NOT_PROVEN

## Scope

- Design review only.
- No strategy source modified.
- No instrumentation implemented.
- No candidate extractor implemented.
- No full 5Y run performed.
- No SIDEWAYS integration performed.

## Proposed trace points

- RAW_UNIVERSE: line=763, variable=symbols, position=FUNCTION_INPUT
- ELIGIBILITY_FILTER: line=1625, variable=e1r_candidate_records, position=AFTER_EACH_CANDIDATE_RECORD_FINALIZED
- PRE_RANK_CANDIDATE_SNAPSHOT: line=1699, variable=e1r_buy_candidates, position=IMMEDIATELY_BEFORE_FIRST_SORT_OR_TOPN
- RANKED_CANDIDATE_SNAPSHOT: line=1615, variable=e1r_buy_candidates, position=IMMEDIATELY_AFTER_RANK_ORDER_FINALIZED
- TOP3_ENTRY_SELECTION: line=1697, variable=e1r_selected_buy, position=AFTER_E1R_SELECTED_BUY_FINALIZED
- EXISTING_HOLDINGS_SEPARATION: line=1700, variable=holdings, position=BEFORE_NEW_ENTRY_SELECTION
- PRE_GATE_INTENT_HANDOFF: line=1717, variable=e1r_buy_candidates, position=IMMEDIATELY_BEFORE_GATE_CONDITION
- POSITION_SIZING_BOUNDARY: line=None, variable=e1r_selected_buy, position=IMMEDIATELY_BEFORE_FIRST_QUANTITY_CALCULATION
- PENDING_ORDER_BOUNDARY: line=1515, variable=pending_orders, position=IMMEDIATELY_BEFORE_PENDING_ORDER_MUTATION

## Missing boundaries

- POSITION_SIZING_BOUNDARY

## Side-effect review

- RAW_UNIVERSE: passed=True, copy=tuple(symbols)
- ELIGIBILITY_FILTER: passed=True, copy=tuple(dict(record) for record in e1r_candidate_records)
- PRE_RANK_CANDIDATE_SNAPSHOT: passed=True, copy=tuple(dict(record) for record in e1r_buy_candidates)
- RANKED_CANDIDATE_SNAPSHOT: passed=True, copy=tuple(dict(record) for record in e1r_buy_candidates)
- TOP3_ENTRY_SELECTION: passed=True, copy=tuple(dict(record) for record in e1r_selected_buy)
- EXISTING_HOLDINGS_SEPARATION: passed=True, copy=tuple(holdings.keys())
- PRE_GATE_INTENT_HANDOFF: passed=True, copy=tuple(dict(record) for record in e1r_buy_candidates)
- POSITION_SIZING_BOUNDARY: passed=True, copy=tuple(dict(record) for record in e1r_selected_buy)
- PENDING_ORDER_BOUNDARY: passed=True, copy=tuple(dict(order) for order in pending_orders)

## Instrumentation rules

- Instrumentation must be disabled by default.
- Trace collection must be guarded by an explicit read-only callback or trace sink.
- No trace code may sort, append, pop, remove, update, or otherwise mutate strategy collections.
- Trace snapshots must use tuple copies and shallow dict copies only at proven stable boundaries.
- Trace code may not call strategy functions again.
- Trace code may not consume generators or iterators.
- Trace code may not alter logger levels, random state, dates, pending orders, cash, holdings, or signals.
- Trace output must be written after snapshot creation and outside strategy condition expressions.
- A no-trace run and trace-enabled run must produce byte-identical strategy result JSON.

## Single-day smoke acceptance

- No-trace versus trace-enabled result: byte-identical
- Holdings sequence: exact equality
- Pending orders sequence: exact equality
- Candidate record sequence: exact equality
- Cash and equity: exact equality
- Trade count and trade records: exact equality
- Maximum live holdings: <= 3
- Gate decision: exact equality
- Trace payload integrity: SHA256 present and stable

## Next stage

None
