# E1R K2 R17 Legacy UPTREND Input and Candidate Boundary Golden Trace Proposal

Generated UTC: 2026-07-11T11:24:28.073133+00:00

Decision: PASS_GOLDEN_TRACE_PROPOSAL_READY_FOR_R17A_READ_ONLY_TRACE_DESIGN_REVIEW

## Scope

- Read-only source analysis.
- No candidate extractor implemented.
- No ranking logic implemented.
- No order generation implemented.
- No position sizing implemented.
- No account mutation implemented.
- No full 5Y run performed.
- No SIDEWAYS integration performed.

## Primary legacy function

- src/engine/backtest.py:run_stateful_simulation lines 763-2486

## Input parameters

- symbols
- prices_map
- dates_map
- spx_prices
- spx_dates
- ohlc_map
- assumptions
- step
- min_history
- market_score_default
- sim_start_date
- sim_end_date
- ndx_prices
- ndx_dates
- sox_prices
- sox_dates
- vix_prices
- vix_dates

## Candidate lifecycle

1. SIMULATION_INPUT: Inputs supplied to run_stateful_simulation before any daily UPTREND decision.
2. RAW_UNIVERSE: Complete symbol set visible to the legacy UPTREND path before eligibility filtering.
3. ELIGIBILITY_FILTER: Per-symbol pass/fail results for history, price, data completeness, exclusions, and other legacy eligibility rules.
4. PRE_RANK_CANDIDATE_SNAPSHOT: Exact complete eligible candidate collection before Leader Score ordering or Top3 selection.
5. RANKED_CANDIDATE_SNAPSHOT: Candidate collection after exact legacy score calculation and ordering, before entry truncation.
6. TOP3_ENTRY_SELECTION: Symbols selected for possible new entry, separate from existing holdings.
7. PRE_GATE_INTENT_HANDOFF: Future boundary where candidate decisions become order intents before R15 gate consumption.

## High-value source evidence

- backtest.py:796 targets=['max_pos'] source=max_pos  = a["max_positions"]
- backtest.py:797 targets=['buy_pct'] source=buy_pct  = a["buy_size"]  / max_pos       # Top3: 1/3 per full slot
- backtest.py:798 targets=['add_pct'] source=add_pct  = a["add_size"]  / max_pos       # Top3: +1/6, only useful after REDUCE
- backtest.py:799 targets=['max_pct'] source=max_pct  = a["max_single_size"] / max_pos # Top3: max 1/3 per position
- backtest.py:802 targets=['strategy_variant'] source=strategy_variant = a.get("strategy_variant", "top3_entry_rs_minhold_relstop")
- backtest.py:845 targets=['entry_top_n'] source=entry_top_n = int(a.get("entry_top_n", 3))
- backtest.py:846 targets=['rank_based_exit'] source=rank_based_exit = bool(a.get("rank_based_exit", False))
- backtest.py:852 targets=['candidate_top_n'] source=candidate_top_n           = a.get("candidate_top_n", None)   # None = 沿用旧 entry_top_n
- backtest.py:1017 targets=['holdings'] source=holdings: dict[str, dict] = {}
- backtest.py:1089 targets=['e1r_candidate_records'] source=e1r_candidate_records: list[dict] = []
- backtest.py:1138 targets=['port_val'] source=port_val = cash + sum(
- backtest.py:1148 targets=['SUBSCRIPT_TARGET'] source=skip_reasons["max_positions_reached"] += 1
- backtest.py:1165 targets=['SUBSCRIPT_TARGET'] source=holdings[sym] = {
- backtest.py:1199 targets=['h'] source=h = holdings[sym]
- backtest.py:1235 targets=['h'] source=h = holdings[sym]
- backtest.py:792 call=logger.info("[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop Backtest...")
- backtest.py:802 call=strategy_variant = a.get("strategy_variant", "top3_entry_rs_minhold_relstop")
- backtest.py:845 call=entry_top_n = int(a.get("entry_top_n", 3))
- backtest.py:845 call=entry_top_n = int(a.get("entry_top_n", 3))
- backtest.py:846 call=rank_based_exit = bool(a.get("rank_based_exit", False))
- backtest.py:846 call=rank_based_exit = bool(a.get("rank_based_exit", False))
- backtest.py:852 call=candidate_top_n           = a.get("candidate_top_n", None)   # None = 沿用旧 entry_top_n
- backtest.py:888 call=logger.info(f"  Qualified Pool: candidate_top_n={candidate_top_n} "
- backtest.py:893 call=logger.info(f"  Entry mode: Strict Top{entry_top_n} (legacy)")
- backtest.py:918 call=logger.info(f"  v{a.get('version','?')} | Strategy={strategy_variant} "

## Golden row classes

- ALLOW_BELOW_MA50_GUARD: date=2021-06-18; purpose=Protect the established market-gate guard: CAUTIOUS_ON with entry capacity 2 remains ALLOW.
- SHOCK_PRECEDENCE_GUARD: date=2021-05-12; purpose=Verify candidate tracing remains observable while SHOCK blocks new BUY and ADD downstream.
- RISK_OFF_ZERO_CAPACITY: date=2022-01-24; purpose=Verify zero-capacity candidate trace and separation between candidate generation and gate blocking.
- TOP3_OVERFLOW: selection_rule=Choose a legacy UPTREND day with at least 5 eligible candidates and at least 3 available slots.; purpose=Prove full pre-rank set, exact ordering, and Top3 truncation.
- TIE_OR_NEAR_TIE: selection_rule=Choose a day where rank positions 3 and 4 have equal or minimally separated Leader Scores.; purpose=Prove deterministic tie-breaking and sort stability.
- EXISTING_HOLDING_OUTSIDE_TOP3: selection_rule=Choose a day with an existing holding that is absent from the new-entry Top3.; purpose=Prove that leaving Top3 alone does not imply EXIT.
- ELIGIBILITY_REJECTION_MATRIX: selection_rule=Choose one or more days containing symbols rejected for insufficient history, minimum price, explicit exclusion, or incomplete indicators.; purpose=Prove each candidate eligibility reason independently.

## Equivalence acceptance criteria

- Same raw universe: metric=symbol set equality; threshold=100 percent
- Same eligibility results: metric=per-symbol eligible flag and reason equality; threshold=100 percent
- Same pre-rank candidate sequence: metric=ordered list equality; threshold=exact
- Same score values: metric=per-symbol Leader Score and components; threshold=exact serialized value or approved numeric tolerance
- Same ranked order: metric=ordered symbol list equality; threshold=exact
- Same Top3 selection: metric=ordered selected symbol list equality; threshold=exact
- Same holdings treatment: metric=existing holdings outside Top3 are not reclassified as EXIT solely by rank; threshold=zero violations
- Position cap preserved: metric=maximum live holdings; threshold=less than or equal to 3
- Gate separation preserved: metric=candidate trace generated independently; R15 alone blocks BUY and ADD; threshold=zero gate recomputations

## Unresolved high-risk unknowns

- Exact variable representing raw universe: SOURCE_CANDIDATES_LOCATED_NOT_YET_TRACED; next=Run one-date read-only variable trace inside the legacy function without changing decisions.
- Exact pre-rank candidate variable: NOT_YET_PROVEN; next=Identify the last assignment before sorting or TopN truncation.
- Tie-breaking order: NOT_YET_PROVEN; next=Capture rank positions around equal scores and inspect sort keys and original order.
- Existing holdings versus new-entry candidates: NOT_YET_PROVEN; next=Trace holdings and candidate lists separately on a day where a holding is outside Top3.
- Candidate trace timing versus position sizing: NOT_YET_PROVEN; next=Establish source-line sequence from Top3 selection through sizing and pending-order creation.

## Next stage after user approval

4C-2C-4E-ENGINE-K2-R17A-LEGACY-UPTREND-CANDIDATE-BOUNDARY-READ-ONLY-TRACE-DESIGN-REVIEW
