# E1R K2 R17A-1 Candidate Flow and Position Sizing Boundary Source Review

Generated UTC: 2026-07-11T11:38:25.905719+00:00

Decision: BLOCKED_POSITION_SIZING_BOUNDARY_NOT_PROVEN

## Scope

- Read-only source review.
- No strategy source modified.
- No instrumentation implemented.
- No strategy behavior implemented.
- No full 5Y run performed.
- No SIDEWAYS integration performed.

## Proven boundaries

- ELIGIBILITY_FINALIZED: line=1671; kind=expression; source=e1r_candidate_records.append({ "date": date_t, "symbol": sym, "spx_regime": "UPTREND", "e1r_entry_type": entry_type, "e1r_uptrend_emerging_eligible": emerging, "e1r_uptrend_confirmed_eligible": confirmed, "leader_rank": rank_all, "leader_score": round(sig["leader_score"], 2),
- PRE_RANK_CANDIDATES_CREATED: line=1699; kind=assignment; source=e1r_buy_candidates = []
- RANK_ORDER_FINALIZED: line=1671; kind=call; source=e1r_candidate_records.append({ "date": date_t, "symbol": sym, "spx_regime": "UPTREND", "e1r_entry_type": entry_type, "e1r_uptrend_emerging_eligible": emerging, "e1r_uptrend_confirmed_eligible": confirmed, "leader_rank": rank_all, "leader_score": round(sig["leader_score"], 2),
- TOP3_SELECTION_FINALIZED: line=1721; kind=assignment; source=e1r_selected_buy = { "sym": _sym, "sig": _sig, "entry_type": _etype, "target_size_units": 1.0 if _etype == "E1R_UPTREND_CONFIRMED" else 0.5, }
- EXISTING_HOLDINGS_SEPARATED: line=1698; kind=branch; source=if e1r_uptrend_execution_enabled and _e1r_regime_on(date_t) == "UPTREND": e1r_buy_candidates = [] for s, v in day_signals.items(): if s in holdings: continue if not v.get("e1r_entry_type"): continue _etype = v.get("e1r_entry_type") _priority = 0 if _etype == "E1R_UPTREND_CONFIRMED" else 1
- PRE_GATE_HANDOFF: line=1717; kind=expression; source=if e1r_buy_candidates and market_entry_allowed:
- POSITION_SIZING_BEGINS: NOT PROVEN
- PENDING_ORDER_MUTATION_BEGINS: NOT PROVEN

## Sequence checks

- ELIGIBILITY_FINALIZED (1671) < PRE_RANK_CANDIDATES_CREATED (1699): True
- PRE_RANK_CANDIDATES_CREATED (1699) < RANK_ORDER_FINALIZED (1671): False
- RANK_ORDER_FINALIZED (1671) < TOP3_SELECTION_FINALIZED (1721): True
- TOP3_SELECTION_FINALIZED (1721) < POSITION_SIZING_BEGINS (None): False
- POSITION_SIZING_BEGINS (None) < PENDING_ORDER_MUTATION_BEGINS (None): False

## Validation

- candidate_sequence_proven: False
- position_sizing_boundary_proven: False
- pending_order_sequence_proven: False
- strict_sequence_proven: False

## Next stage

None
