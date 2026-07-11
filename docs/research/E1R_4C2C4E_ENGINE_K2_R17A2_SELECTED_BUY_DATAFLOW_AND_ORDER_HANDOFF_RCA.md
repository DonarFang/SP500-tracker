# E1R K2 R17A-2 Selected-Buy Dataflow and Order-Handoff RCA

Generated UTC: 2026-07-11T11:43:23.537205+00:00

Decision: BLOCKED_ORDER_CREATION_NOT_PROVEN

## Scope

- Directed dataflow RCA only.
- No broad keyword-based boundary inference.
- No strategy source modified.
- No instrumentation implemented.
- No full 5Y run performed.
- No SIDEWAYS integration performed.

## Candidate block source: lines 1695-1740

1695:         # E1-R Phase 3B: UPTREND Execution v0.1 candidate selection.
1696:         # Only entry execution is changed; existing E1 reduce/exit logic remains intact.
1697:         e1r_selected_buy: dict | None = None
1698:         if e1r_uptrend_execution_enabled and _e1r_regime_on(date_t) == "UPTREND":
1699:             e1r_buy_candidates = []
1700:             for s, v in day_signals.items():
1701:                 if s in holdings:
1702:                     continue
1703:                 if not v.get("e1r_entry_type"):
1704:                     continue
1705:                 _etype = v.get("e1r_entry_type")
1706:                 _priority = 0 if _etype == "E1R_UPTREND_CONFIRMED" else 1
1707:                 e1r_buy_candidates.append((
1708:                     _priority,
1709:                     leader_rank_all.get(s, 9999),
1710:                     -v.get("leader_score", 0),
1711:                     -v.get("momentum_acceleration", 0),
1712:                     -v.get("rs_20d_improvement", 0),
1713:                     s,
1714:                     v,
1715:                 ))
1716:             e1r_buy_candidates.sort()
1717:             if e1r_buy_candidates and market_entry_allowed:
1718:                 if len(holdings) < min(max_pos, entry_capacity):
1719:                     _, _, _, _, _, _sym, _sig = e1r_buy_candidates[0]
1720:                     _etype = _sig.get("e1r_entry_type")
1721:                     e1r_selected_buy = {
1722:                         "sym": _sym,
1723:                         "sig": _sig,
1724:                         "entry_type": _etype,
1725:                         "target_size_units": 1.0 if _etype == "E1R_UPTREND_CONFIRMED" else 0.5,
1726:                     }
1727:                 else:
1728:                     skip_reasons["e1r_no_capacity"] += len(e1r_buy_candidates)
1729: 
1730:         if qualified_entry_enabled and candidate_top_n is not None:
1731:             # Qualified Candidate Pool 逻辑：
1732:             # Step 1: 过滤资格条件
1733:             qualified = []
1734:             for s, v in day_signals.items():
1735:                 if v["rs_score"]       < qualified_rs_min:          continue
1736:                 if v["momentum_score"] < qualified_momentum_min:    continue
1737:                 if v["trend_health"]   < qualified_th_min:          continue
1738:                 if v["trend_state"]    not in qualified_states:     continue
1739:                 if qualified_price_above_ma50 and v["close_t"] <= v["ma50"]: continue
1740:                 if v["ma50_slope"]     < qualified_ma50_slope_min:  continue

## Candidate chain

- CANDIDATE_APPEND_COMPLETE (1707) < CANDIDATE_SORT (1716): True
- CANDIDATE_SORT (1716) < BEST_ENTRY_SELECTION (1719): True
- BEST_ENTRY_SELECTION (1719) < SELECTED_BUY_FINALIZED (1721): True

## Selected-buy and order handoff

- candidate_append_complete: line=1707; source=e1r_buy_candidates.append((
- candidate_sort: line=1716; source=e1r_buy_candidates.sort()
- best_entry_selection: line=1719; source=_, _, _, _, _, _sym, _sig = e1r_buy_candidates[0]
- selected_buy_finalized: line=1721; source=e1r_selected_buy = {
- first_selected_buy_consumption: line=1784; source=and e1r_selected_buy
- first_target_size_use: line=1725; source="target_size_units": 1.0 if _etype == "E1R_UPTREND_CONFIRMED" else 0.5,
- first_selected_or_target_order_link: line=1725; source="target_size_units": 1.0 if _etype == "E1R_UPTREND_CONFIRMED" else 0.5,
- order_creation: NOT PROVEN
- pending_handoff: line=2130; source=# 最后一个或倒数第二个 sim 日不生成新 BUY（T+1 执行时会撞上 sim_end_date）
- execution_handoff: line=2130; source=# 最后一个或倒数第二个 sim 日不生成新 BUY（T+1 执行时会撞上 sim_end_date）

## Validation

- candidate_append_count: 1
- candidate_sort_count: 1
- candidate_index_zero_count: 1
- selected_buy_assignment_count: 1
- selected_buy_post_assignment_use_count: 4
- target_size_post_selection_use_count: 2
- order_related_post_selection_count: 22
- selected_or_target_order_link_count: 2
- order_creation_candidate_count: 0
- pending_handoff_candidate_count: 2
- execution_handoff_candidate_count: 1
- candidate_chain_proven: True
- selected_buy_consumption_proven: True
- target_size_dataflow_proven: True
- order_creation_proven: False
- pending_handoff_proven: True
- execution_handoff_proven: True
- source_modified: False
- instrumentation_implemented: False
- strategy_logic_implemented: False
- full_5y_run_performed: False
- sideways_logic_added: False
- frozen_files_unchanged: True

## Next stage

None
