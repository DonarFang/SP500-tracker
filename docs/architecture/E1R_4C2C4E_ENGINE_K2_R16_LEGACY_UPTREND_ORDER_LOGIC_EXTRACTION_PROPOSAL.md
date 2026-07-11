# E1R K2 R16 Legacy UPTREND Order Logic Extraction Proposal

Generated UTC: 2026-07-11T09:43:14.260050+00:00

Decision: PASS_PROPOSAL_READY_FOR_USER_REVIEW_BEFORE_R17

## Scope

R16 is proposal-only and performs no strategy implementation.

It does not modify legacy strategy files, generate orders, size positions, mutate accounts, run a 5Y backtest, or integrate SIDEWAYS.

## Source inventory summary

- candidate_generation: hits=91, files=4, evidence_present=True
- ranking_and_top3_selection: hits=104, files=7, evidence_present=True
- buy_generation: hits=75, files=5, evidence_present=True
- add_generation: hits=53, files=5, evidence_present=True
- hold_behavior: hits=77, files=5, evidence_present=True
- reduce_behavior: hits=86, files=5, evidence_present=True
- exit_behavior: hits=110, files=5, evidence_present=True
- position_sizing: hits=9, files=3, evidence_present=True
- pending_order_boundary: hits=17, files=1, evidence_present=True
- next_day_execution: hits=32, files=1, evidence_present=True
- market_gate_consumption: hits=116, files=3, evidence_present=True
- account_mutation: hits=68, files=3, evidence_present=True
- uptrend_branch: hits=102, files=4, evidence_present=True

## Proposed extraction sequence

1. LegacyUptrendInputBoundary: Identify normalized market, regime, universe, account, holdings, and gate inputs consumed by the legacy UPTREND path.
2. LegacyCandidateSnapshotExtractor: Capture the exact legacy candidate set before ranking or strategy selection.
3. LegacyRankingAndTop3Boundary: Capture exact Leader Score ordering, filters, tie behavior, EntryTopN semantics, and the distinction between entry candidates and holdings.
4. LegacyOrderIntentExtractor: Extract pre-gate BUY, ADD, HOLD, REDUCE, and EXIT intents without executing or mutating the account.
5. MarketGateConsumptionBoundary: Reuse the R15 contract: block BUY and ADD only when market_entry_allowed is false.
6. LegacyPositionSizingBoundary: Extract exact legacy quantity and cash-allocation semantics after intent selection.
7. PendingOrderAndExecutionBoundary: Separate signal-day decisions from T+1 adverse execution, transaction costs, and slippage.
8. AccountMutationBoundary: Keep fills, cash mutation, position mutation, equity updates, and trade closure outside UptrendCore decision generation.

## Strict equivalence contracts

- Candidate eligibility and exclusions
- Leader Score calculation inputs and ordering
- Top3 entry semantics
- Existing holdings are not exited merely for leaving Top3
- BUY and ADD eligibility
- HOLD, REDUCE, and EXIT precedence
- MinHold and exit-block behavior where applicable
- Live holdings count never exceeds 3
- Market gate is consumed, never recomputed
- BUY and ADD only are blocked by closed gate
- Position sizing and minimum-size handling
- Signal day versus execution day alignment
- T+1 adverse price convention
- Transaction cost and slippage convention
- Pending-order ordering and cancellation behavior
- Cash and account mutation identities

## High-risk unknowns

- Exact candidate snapshot boundary: SOURCE_LINES_LOCATED_PROPOSAL_NOT_IMPLEMENTED. Next evidence: Variable-level trace showing the candidate set immediately before ranking and Top3 selection.
- Tie-breaking and sort stability: NOT_YET_PROVEN. Next evidence: Golden rows containing equal or near-equal ranking scores and exact legacy output order.
- Order precedence: NOT_YET_PROVEN. Next evidence: Rows where multiple BUY/ADD/HOLD/REDUCE/EXIT conditions are simultaneously true.
- Sizing versus gate ordering: NOT_YET_PROVEN. Next evidence: Source-line and variable trace proving whether sizing occurs before or after gate consumption.
- Pending-order lifecycle: NOT_YET_PROVEN. Next evidence: Signal-day and execution-day trace including replacement, cancellation, and cash checks.

## Source-line evidence index

### candidate_generation

- src/engine/backtest.py:81 function=MODULE text=# Qualified Candidate Pool（v1.7+）
- src/engine/backtest.py:82 function=MODULE text=# candidate_top_n：Qualified Pool 内最多取 N 个候选（None = 用旧 entry_top_n 逻辑）
- src/engine/backtest.py:84 function=MODULE text=# qualified_entry_enabled：是否启用资格过滤
- src/engine/backtest.py:85 function=MODULE text=# qualified_states：允许的 trend_state
- src/engine/backtest.py:86 function=MODULE text="candidate_top_n":          None,    # None = 沿用旧 entry_top_n=3 逻辑
- src/engine/backtest.py:87 function=MODULE text="qualified_entry_enabled":  False,
- src/engine/backtest.py:88 function=MODULE text="qualified_rs_min":         90.0,
- src/engine/backtest.py:89 function=MODULE text="qualified_momentum_min":   85.0,
- src/engine/backtest.py:90 function=MODULE text="qualified_th_min":         75.0,
- src/engine/backtest.py:91 function=MODULE text="qualified_states":         ["Expansion"],
- src/engine/backtest.py:92 function=MODULE text="qualified_price_above_ma50": True,
- src/engine/backtest.py:93 function=MODULE text="qualified_ma50_slope_min":   0.0,
- src/engine/backtest.py:94 function=MODULE text="fill_only_enabled":          False,  # True = Qualified Pool 只补空仓，不替换持仓
- src/engine/backtest.py:532 function=run_promotion_engine_validation text=candidates = [s for s, v in day_scores.items()
- src/engine/backtest.py:534 function=run_promotion_engine_validation text=for sym in candidates:
- src/engine/backtest.py:851 function=run_stateful_simulation text=# Qualified Candidate Pool 参数
- src/engine/backtest.py:852 function=run_stateful_simulation text=candidate_top_n           = a.get("candidate_top_n", None)   # None = 沿用旧 entry_top_n
- src/engine/backtest.py:853 function=run_stateful_simulation text=qualified_entry_enabled   = bool(a.get("qualified_entry_enabled", False))
- src/engine/backtest.py:854 function=run_stateful_simulation text=qualified_rs_min          = float(a.get("qualified_rs_min", 90.0))
- src/engine/backtest.py:855 function=run_stateful_simulation text=qualified_momentum_min    = float(a.get("qualified_momentum_min", 85.0))
- src/engine/backtest.py:856 function=run_stateful_simulation text=qualified_th_min          = float(a.get("qualified_th_min", 75.0))
- src/engine/backtest.py:857 function=run_stateful_simulation text=qualified_states          = set(a.get("qualified_states", ["Expansion"]))
- src/engine/backtest.py:858 function=run_stateful_simulation text=qualified_price_above_ma50 = bool(a.get("qualified_price_above_ma50", True))
- src/engine/backtest.py:859 function=run_stateful_simulation text=qualified_ma50_slope_min  = float(a.get("qualified_ma50_slope_min", 0.0))
- src/engine/backtest.py:887 function=run_stateful_simulation text=if qualified_entry_enabled:

### ranking_and_top3_selection

- src/engine/backtest.py:24 function=MODULE text=from ..engine.leader_ranking import leader_score as calc_leader_score
- src/engine/backtest.py:35 function=MODULE text="max_positions":      3,
- src/engine/backtest.py:36 function=MODULE text="buy_size":          1.0,    # Top3: 1/3 portfolio full position
- src/engine/backtest.py:37 function=MODULE text="add_size":          0.5,    # Top3: +1/6 portfolio, used only after REDUCE if allowed
- src/engine/backtest.py:38 function=MODULE text="max_single_size":   1.0,    # Top3 strategy: 1/3 max per position
- src/engine/backtest.py:54 function=MODULE text="strategy_variant":  "top3_entry_rs_minhold_relstop",
- src/engine/backtest.py:55 function=MODULE text="entry_top_n":       3,
- src/engine/backtest.py:56 function=MODULE text="rank_based_exit":   False,
- src/engine/backtest.py:78 function=MODULE text="version":           "1.6-top3-rs95-minhold-relstop-comparison",
- src/engine/backtest.py:82 function=MODULE text=# candidate_top_n：Qualified Pool 内最多取 N 个候选（None = 用旧 entry_top_n 逻辑）
- src/engine/backtest.py:83 function=MODULE text=# max_positions：组合最大持仓数
- src/engine/backtest.py:86 function=MODULE text="candidate_top_n":          None,    # None = 沿用旧 entry_top_n=3 逻辑
- src/engine/backtest.py:164 function=_rebuild_leader_score text="leader_score": ls,
- src/engine/backtest.py:222 function=run_leader_engine_validation text=ls = info["leader_score"]
- src/engine/backtest.py:249 function=run_leader_engine_validation text="med_ret":  round(sorted(rets)[len(rets)//2], 3),
- src/engine/backtest.py:274 function=run_leader_engine_validation text=# A2: Full Monotonic Ranking — A>B>C>D>E 严格单调
- src/engine/backtest.py:416 function=stats text=med = sorted(rets)[len(rets)//2]
- src/engine/backtest.py:483 function=run_promotion_engine_validation text=验证 Promotion Score 能否预测未来晋升 Top30。
- src/engine/backtest.py:520 function=run_promotion_engine_validation text=# 用 Leader Score 近似 Promotion Score（历史 RankVelocity 不可用）
- src/engine/backtest.py:522 function=run_promotion_engine_validation text=day_scores[sym] = {"leader_score": ls, "promotion_score": promo_approx}
- src/engine/backtest.py:527 function=run_promotion_engine_validation text=# 当前 Top30
- src/engine/backtest.py:528 function=run_promotion_engine_validation text=top30_now = set(sorted(day_scores, key=lambda s: day_scores[s]["leader_score"], reverse=True)[:30])
- src/engine/backtest.py:533 function=run_promotion_engine_validation text=if v["promotion_score"] >= thresh and s not in top30_now]
- src/engine/backtest.py:536 function=run_promotion_engine_validation text=# 未来某天进入 Top30？
- src/engine/backtest.py:541 function=run_promotion_engine_validation text=# 重算未来 Top30

### buy_generation

- src/engine/backtest.py:42 function=MODULE text="total_round_trip":  0.0020, # buy + sell total
- src/engine/backtest.py:45 function=MODULE text=# BUY/ADD:     next_day_high  × (1 + cost + slippage)  ← worst buy
- src/engine/backtest.py:325 function=run_trade_rule_validation text=对每个 BUY/EXIT 信号，测量信号后的前向收益，
- src/engine/backtest.py:331 function=run_trade_rule_validation text="BUY":  {d: [] for d in forward_days},
- src/engine/backtest.py:340 function=run_trade_rule_validation text=signal_counts = {"BUY": 0, "ADD": 0, "HOLD": 0, "REDUCE": 0, "EXIT": 0}
- src/engine/backtest.py:442 function=run_trade_rule_validation text=buy_avg = summary["BUY"].get(k, {}).get("avg_ret", 0)
- src/engine/backtest.py:449 function=run_trade_rule_validation text=# 有效 BUY 信号数量（去重后）
- src/engine/backtest.py:450 function=run_trade_rule_validation text=buy_n = summary.get("BUY",{}).get("fwd20d",{}).get("n", 0)
- src/engine/backtest.py:610 function=run_action_forward_validation text=- BUY  → 买入后是否有正向期望？
- src/engine/backtest.py:621 function=run_action_forward_validation text=for a in ["BUY","ADD","HOLD","REDUCE","EXIT"]
- src/engine/backtest.py:728 function=run_action_forward_validation text=row = {a: summary[a].get(k,{}).get("avg_ret","—") for a in ["BUY","ADD","HOLD","REDUCE","EXIT"]}
- src/engine/backtest.py:732 function=run_action_forward_validation text=f"BUY={row['BUY']:+.2f}% "
- src/engine/backtest.py:738 function=run_action_forward_validation text=if isinstance(row["BUY"], float) else f"  C2 {d}日: 无数据"
- src/engine/backtest.py:1035 function=run_stateful_simulation text="qualified_candidate_generated":    0,   # qualified: 候选池 BUY 已生成
- src/engine/backtest.py:1046 function=run_stateful_simulation text="action_reason_buy_add_mismatch":  0,   # BUY/ADD 不一致（记录，不中断）
- src/engine/backtest.py:1047 function=run_stateful_simulation text="fill_only_no_empty_slot":         0,   # fill_only 模式：无空仓位，跳过 BUY
- src/engine/backtest.py:1048 function=run_stateful_simulation text="e1r_legacy_buy_blocked":          0,   # E1-R execution: legacy BUY suppressed
- src/engine/backtest.py:1050 function=run_stateful_simulation text="e1r_candidate_buy_generated":     0,   # E1-R execution: candidate BUY generated
- src/engine/backtest.py:1098 function=run_stateful_simulation text="buy_orders_generated": 0,   # qualified_pool BUY 生成数
- src/engine/backtest.py:1128 function=run_stateful_simulation text=if action in ("BUY", "ADD"):
- src/engine/backtest.py:1143 function=run_stateful_simulation text=if action == "BUY":
- src/engine/backtest.py:1172 function=run_stateful_simulation text="entry_signal":          "BUY",
- src/engine/backtest.py:1187 function=run_stateful_simulation text="action_history":        ["BUY"],
- src/engine/backtest.py:1278 function=run_stateful_simulation text="entry_signal":         h["entry_signal"],
- src/engine/backtest.py:1379 function=run_stateful_simulation text=#   Top 3 只限制“新 BUY 候选池”

### add_generation

- src/engine/backtest.py:45 function=MODULE text=# BUY/ADD:     next_day_high  × (1 + cost + slippage)  ← worst buy
- src/engine/backtest.py:332 function=run_trade_rule_validation text="ADD":  {d: [] for d in forward_days},
- src/engine/backtest.py:340 function=run_trade_rule_validation text=signal_counts = {"BUY": 0, "ADD": 0, "HOLD": 0, "REDUCE": 0, "EXIT": 0}
- src/engine/backtest.py:611 function=run_action_forward_validation text=- ADD  → 加仓后是否继续超额？
- src/engine/backtest.py:621 function=run_action_forward_validation text=for a in ["BUY","ADD","HOLD","REDUCE","EXIT"]
- src/engine/backtest.py:728 function=run_action_forward_validation text=row = {a: summary[a].get(k,{}).get("avg_ret","—") for a in ["BUY","ADD","HOLD","REDUCE","EXIT"]}
- src/engine/backtest.py:733 function=run_action_forward_validation text=f"ADD={row['ADD']:+.2f}% "
- src/engine/backtest.py:1046 function=run_stateful_simulation text="action_reason_buy_add_mismatch":  0,   # BUY/ADD 不一致（记录，不中断）
- src/engine/backtest.py:1051 function=run_stateful_simulation text="e1r_emerging_to_confirmed_add":   0,   # E1-R execution: upgrade ADD generated
- src/engine/backtest.py:1056 function=run_stateful_simulation text=portfolio_action_dist = {"HOLD": 0, "ADD": 0, "REDUCE": 0, "REL_REDUCE": 0, "EXIT": 0, "TP_REDUCE": 0}
- src/engine/backtest.py:1128 function=run_stateful_simulation text=if action in ("BUY", "ADD"):
- src/engine/backtest.py:1195 function=run_stateful_simulation text=elif action == "ADD":
- src/engine/backtest.py:1226 function=run_stateful_simulation text=h["action_history"].append("ADD")
- src/engine/backtest.py:1227 function=run_stateful_simulation text=h["ls60_reduce_triggered"] = False  # ADD 后清零 ls60 保护
- src/engine/backtest.py:1614 function=run_stateful_simulation text=# 只限制新开仓 BUY；不限制已有持仓的 HOLD/ADD/REDUCE/EXIT
- src/engine/backtest.py:1781 function=run_stateful_simulation text=#   Position Mgmt → 由 trade_action 决定（HOLD/ADD/REDUCE/EXIT）
- src/engine/backtest.py:1810 function=run_stateful_simulation text=# 已持仓：BUY 信号在 Qualified 模式下转为 ADD，由下方 position mgmt 处理
- src/engine/backtest.py:1812 function=run_stateful_simulation text=action = "ADD"
- src/engine/backtest.py:1893 function=run_stateful_simulation text=# 已持仓股票的管理：ADD / REDUCE / EXIT 与 rank 无关
- src/engine/backtest.py:1894 function=run_stateful_simulation text=if action in ("ADD", "REDUCE", "EXIT"):
- src/engine/backtest.py:1968 function=run_stateful_simulation text=if action == "ADD" and block_add_after_take_profit and holdings[sym].get("take_profit_triggered"):
- src/engine/backtest.py:1971 function=run_stateful_simulation text=if action == "ADD" and not market_entry_allowed:
- src/engine/backtest.py:1983 function=run_stateful_simulation text=# BUY / ADD mismatch     → 仅计数，不中断（进攻类语义相近）
- src/engine/backtest.py:1996 function=run_stateful_simulation text=# CAUTIOUS_ON/CASH_MODE 禁止 ADD（生成层拦截）
- src/engine/backtest.py:1997 function=run_stateful_simulation text=if action == "ADD" and market_gate_enabled and market_state in ("CAUTIOUS_ON", "CASH_MODE"):

### hold_behavior

- src/engine/backtest.py:47 function=MODULE text=# HOLD:        mark-to-market at close, no transaction
- src/engine/backtest.py:58 function=MODULE text=# the impact of RS threshold, minimum holding period, and relative SPX stop.
- src/engine/backtest.py:64 function=MODULE text=# Entry / holding / relative-risk controls tested by v1.6 variants.
- src/engine/backtest.py:66 function=MODULE text="min_holding_days": 0,
- src/engine/backtest.py:67 function=MODULE text="min_hold_allow_broken_exit": True,
- src/engine/backtest.py:334 function=run_trade_rule_validation text="HOLD": {d: [] for d in forward_days},
- src/engine/backtest.py:340 function=run_trade_rule_validation text=signal_counts = {"BUY": 0, "ADD": 0, "HOLD": 0, "REDUCE": 0, "EXIT": 0}
- src/engine/backtest.py:612 function=run_action_forward_validation text=- HOLD → 继续持有是否比卖出更好？
- src/engine/backtest.py:621 function=run_action_forward_validation text=for a in ["BUY","ADD","HOLD","REDUCE","EXIT"]
- src/engine/backtest.py:706 function=run_action_forward_validation text=# 1. HOLD 后收益是否为正（持有有效）
- src/engine/backtest.py:707 function=run_action_forward_validation text=hold_positive = sum(
- src/engine/backtest.py:709 function=run_action_forward_validation text=if summary["HOLD"].get(f"fwd{d}d",{}).get("avg_ret",0) > 0
- src/engine/backtest.py:711 function=run_action_forward_validation text=# 2. REDUCE/EXIT 后收益是否低于 HOLD（减仓/退出有保护作用）
- src/engine/backtest.py:715 function=run_action_forward_validation text=summary["HOLD"].get(f"fwd{d}d",{}).get("avg_ret",0)
- src/engine/backtest.py:720 function=run_action_forward_validation text=summary["HOLD"].get(f"fwd{d}d",{}).get("avg_ret",0)
- src/engine/backtest.py:723 function=run_action_forward_validation text=status = "PASS" if hold_positive >= 3 and (reduce_lower + exit_lower) >= 4 else              "PARTIAL" if hold_positive >= 2 else "FAIL"
- src/engine/backtest.py:728 function=run_action_forward_validation text=row = {a: summary[a].get(k,{}).get("avg_ret","—") for a in ["BUY","ADD","HOLD","REDUCE","EXIT"]}
- src/engine/backtest.py:734 function=run_action_forward_validation text=f"HOLD={row['HOLD']:+.2f}% "
- src/engine/backtest.py:740 function=run_action_forward_validation text=logger.info(f"  Layer C2: {status} (HOLD正收益 {hold_positive}/4, REDUCE低于HOLD {reduce_lower}/4, EXIT低于HOLD {exit_lower}/4)")
- src/engine/backtest.py:746 function=run_action_forward_validation text="hold_positive_count":  hold_positive,
- src/engine/backtest.py:752 function=run_action_forward_validation text="HOLD":   "持有有效" if hold_positive >= 3 else "持有期望偏低，需检查",
- src/engine/backtest.py:903 function=run_stateful_simulation text=min_holding_days = int(a.get("min_holding_days", 0))
- src/engine/backtest.py:906 function=run_stateful_simulation text=min_hold_allow_broken_exit = bool(a.get("min_hold_allow_broken_exit", True))
- src/engine/backtest.py:931 function=run_stateful_simulation text=logger.info(f"  Entry filter: RS >= {entry_rs_min:.1f}; MinHold={min_holding_days}d; "
- src/engine/backtest.py:937 function=run_stateful_simulation text=f"top_n={entry_top_n} minhold={min_holding_days} "

### reduce_behavior

- src/engine/backtest.py:37 function=MODULE text="add_size":          0.5,    # Top3: +1/6 portfolio, used only after REDUCE if allowed
- src/engine/backtest.py:46 function=MODULE text=# REDUCE/EXIT: next_day_low   × (1 - cost - slippage)  ← worst sell
- src/engine/backtest.py:70 function=MODULE text="relative_stop_action": "REL_REDUCE",   # reduce 50%, once per position
- src/engine/backtest.py:79 function=MODULE text="ls60_exit_mode":    "reduce",   # "exit"=旧规则 "reduce"=新规则（默认）
- src/engine/backtest.py:340 function=run_trade_rule_validation text=signal_counts = {"BUY": 0, "ADD": 0, "HOLD": 0, "REDUCE": 0, "EXIT": 0}
- src/engine/backtest.py:613 function=run_action_forward_validation text=- REDUCE → 减仓后股票是否真的走弱？
- src/engine/backtest.py:621 function=run_action_forward_validation text=for a in ["BUY","ADD","HOLD","REDUCE","EXIT"]
- src/engine/backtest.py:711 function=run_action_forward_validation text=# 2. REDUCE/EXIT 后收益是否低于 HOLD（减仓/退出有保护作用）
- src/engine/backtest.py:712 function=run_action_forward_validation text=reduce_lower = sum(
- src/engine/backtest.py:714 function=run_action_forward_validation text=if summary["REDUCE"].get(f"fwd{d}d",{}).get("avg_ret",999) <
- src/engine/backtest.py:723 function=run_action_forward_validation text=status = "PASS" if hold_positive >= 3 and (reduce_lower + exit_lower) >= 4 else              "PARTIAL" if hold_positive >= 2 else "FAIL"
- src/engine/backtest.py:728 function=run_action_forward_validation text=row = {a: summary[a].get(k,{}).get("avg_ret","—") for a in ["BUY","ADD","HOLD","REDUCE","EXIT"]}
- src/engine/backtest.py:735 function=run_action_forward_validation text=f"REDUCE={row['REDUCE']:+.2f}% "
- src/engine/backtest.py:740 function=run_action_forward_validation text=logger.info(f"  Layer C2: {status} (HOLD正收益 {hold_positive}/4, REDUCE低于HOLD {reduce_lower}/4, EXIT低于HOLD {exit_lower}/4)")
- src/engine/backtest.py:747 function=run_action_forward_validation text="reduce_lower_count":   reduce_lower,
- src/engine/backtest.py:753 function=run_action_forward_validation text="REDUCE": f"减仓有保护 ({reduce_lower}/4)" if reduce_lower >= 3 else "减仓保护不足",
- src/engine/backtest.py:798 function=run_stateful_simulation text=add_pct  = a["add_size"]  / max_pos       # Top3: +1/6, only useful after REDUCE
- src/engine/backtest.py:849 function=run_stateful_simulation text=ls60_exit_mode = a.get("ls60_exit_mode", "reduce")  # "exit"=旧规则 "reduce"=新规则
- src/engine/backtest.py:894 function=run_stateful_simulation text=if ls60_exit_mode not in {"exit", "reduce"}:
- src/engine/backtest.py:895 function=run_stateful_simulation text=raise ValueError(f"Invalid ls60_exit_mode={ls60_exit_mode!r}; expected 'exit' or 'reduce'")
- src/engine/backtest.py:935 function=run_stateful_simulation text=f"({'LS<60 → EXIT' if ls60_exit_mode == 'exit' else 'LS<60 → REDUCE'})")
- src/engine/backtest.py:1056 function=run_stateful_simulation text=portfolio_action_dist = {"HOLD": 0, "ADD": 0, "REDUCE": 0, "REL_REDUCE": 0, "EXIT": 0, "TP_REDUCE": 0}
- src/engine/backtest.py:1061 function=run_stateful_simulation text=# 生成过的 EXIT/REDUCE pending signal 原因（含未成交）
- src/engine/backtest.py:1188 function=run_stateful_simulation text="ls60_reduce_triggered": False,  # 方案A：LS<60 REDUCE 一次性保护
- src/engine/backtest.py:1231 function=run_stateful_simulation text=elif action in ("REDUCE", "REL_REDUCE", "TP_REDUCE", "EXIT"):

### exit_behavior

- src/engine/backtest.py:46 function=MODULE text=# REDUCE/EXIT: next_day_low   × (1 - cost - slippage)  ← worst sell
- src/engine/backtest.py:79 function=MODULE text="ls60_exit_mode":    "reduce",   # "exit"=旧规则 "reduce"=新规则（默认）
- src/engine/backtest.py:325 function=run_trade_rule_validation text=对每个 BUY/EXIT 信号，测量信号后的前向收益，
- src/engine/backtest.py:333 function=run_trade_rule_validation text="EXIT": {d: [] for d in forward_days},
- src/engine/backtest.py:340 function=run_trade_rule_validation text=signal_counts = {"BUY": 0, "ADD": 0, "HOLD": 0, "REDUCE": 0, "EXIT": 0}
- src/engine/backtest.py:614 function=run_action_forward_validation text=- EXIT → 退出后是否避免了进一步下跌？
- src/engine/backtest.py:621 function=run_action_forward_validation text=for a in ["BUY","ADD","HOLD","REDUCE","EXIT"]
- src/engine/backtest.py:711 function=run_action_forward_validation text=# 2. REDUCE/EXIT 后收益是否低于 HOLD（减仓/退出有保护作用）
- src/engine/backtest.py:717 function=run_action_forward_validation text=exit_lower = sum(
- src/engine/backtest.py:719 function=run_action_forward_validation text=if summary["EXIT"].get(f"fwd{d}d",{}).get("avg_ret",999) <
- src/engine/backtest.py:723 function=run_action_forward_validation text=status = "PASS" if hold_positive >= 3 and (reduce_lower + exit_lower) >= 4 else              "PARTIAL" if hold_positive >= 2 else "FAIL"
- src/engine/backtest.py:728 function=run_action_forward_validation text=row = {a: summary[a].get(k,{}).get("avg_ret","—") for a in ["BUY","ADD","HOLD","REDUCE","EXIT"]}
- src/engine/backtest.py:736 function=run_action_forward_validation text=f"EXIT={row['EXIT']:+.2f}% "
- src/engine/backtest.py:740 function=run_action_forward_validation text=logger.info(f"  Layer C2: {status} (HOLD正收益 {hold_positive}/4, REDUCE低于HOLD {reduce_lower}/4, EXIT低于HOLD {exit_lower}/4)")
- src/engine/backtest.py:748 function=run_action_forward_validation text="exit_lower_count":     exit_lower,
- src/engine/backtest.py:754 function=run_action_forward_validation text="EXIT":   f"退出有保护 ({exit_lower}/4)" if exit_lower >= 3 else "退出可能过早",
- src/engine/backtest.py:849 function=run_stateful_simulation text=ls60_exit_mode = a.get("ls60_exit_mode", "reduce")  # "exit"=旧规则 "reduce"=新规则
- src/engine/backtest.py:894 function=run_stateful_simulation text=if ls60_exit_mode not in {"exit", "reduce"}:
- src/engine/backtest.py:895 function=run_stateful_simulation text=raise ValueError(f"Invalid ls60_exit_mode={ls60_exit_mode!r}; expected 'exit' or 'reduce'")
- src/engine/backtest.py:904 function=run_stateful_simulation text=# E2 Dynamic Exit parameters
- src/engine/backtest.py:935 function=run_stateful_simulation text=f"({'LS<60 → EXIT' if ls60_exit_mode == 'exit' else 'LS<60 → REDUCE'})")
- src/engine/backtest.py:940 function=run_stateful_simulation text=logger.info(f"  Dynamic Exit v2: ON | Hard=Close<MA50+slope<0 | FULL_ON=needs structure | CAUTIOUS/CASH=LS<60 exits")
- src/engine/backtest.py:1056 function=run_stateful_simulation text=portfolio_action_dist = {"HOLD": 0, "ADD": 0, "REDUCE": 0, "REL_REDUCE": 0, "EXIT": 0, "TP_REDUCE": 0}
- src/engine/backtest.py:1061 function=run_stateful_simulation text=# 生成过的 EXIT/REDUCE pending signal 原因（含未成交）
- src/engine/backtest.py:1231 function=run_stateful_simulation text=elif action in ("REDUCE", "REL_REDUCE", "TP_REDUCE", "EXIT"):

### position_sizing

- src/engine/backtest.py:840 function=_e1r_dominant_regime text=def _e1r_dominant_regime(weights: dict) -> str:
- src/engine/backtest.py:841 function=_e1r_dominant_regime text=if not weights:
- src/engine/backtest.py:843 function=_e1r_dominant_regime text=return max(weights.items(), key=lambda kv: kv[1])[0]
- src/engine/backtest.py:1030 function=run_stateful_simulation text="size_at_minimum":          0,
- src/engine/backtest.py:1317 function=run_stateful_simulation text=skip_reasons["size_at_minimum"] += 1
- src/features/momentum.py:9 function=MODULE text=Weight in Leader Score: 35%
- src/e1r_engine/state.py:152 function=MODULE text=target_quantity: float | None
- src/e1r_engine/state.py:153 function=MODULE text=quantity_delta: float | None
- src/e1r_engine/state.py:166 function=validate text=if self.target_quantity is not None and self.target_quantity < 0:

### pending_order_boundary

- src/engine/backtest.py:1018 function=run_stateful_simulation text=pending_orders: list[dict] = []
- src/engine/backtest.py:1112 function=run_stateful_simulation text=pending_orders = []   # 不生成订单
- src/engine/backtest.py:1120 function=run_stateful_simulation text=for order in pending_orders:
- src/engine/backtest.py:1123 function=run_stateful_simulation text=sig_date  = order["signal_date"]   # 信号日期
- src/engine/backtest.py:1377 function=run_stateful_simulation text=# STEP 3: 生成 T 日信号 → pending_orders for T+1
- src/engine/backtest.py:1524 function=run_stateful_simulation text="pending_orders_count": len(pending_orders),
- src/engine/backtest.py:1792 function=run_stateful_simulation text="signal_date":    date_t,
- src/engine/backtest.py:1839 function=run_stateful_simulation text="signal_date":    date_t,
- src/engine/backtest.py:1882 function=run_stateful_simulation text="signal_date":    date_t,
- src/engine/backtest.py:2016 function=run_stateful_simulation text="signal_date":   date_t,
- src/engine/backtest.py:2051 function=run_stateful_simulation text="signal_date": date_t,
- src/engine/backtest.py:2086 function=run_stateful_simulation text="signal_date": date_t,
- src/engine/backtest.py:2117 function=run_stateful_simulation text="signal_date": date_t,
- src/engine/backtest.py:2134 function=run_stateful_simulation text=pending_orders = management_orders + buy_orders
- src/engine/backtest.py:2154 function=run_stateful_simulation text="pending_orders": len(pending_orders),
- src/engine/backtest.py:2456 function=run_stateful_simulation text="pending_orders_executed":  orders_executed,
- src/engine/backtest.py:2457 function=run_stateful_simulation text="pending_orders_skipped":   sum(skip_reasons.values()),

### next_day_execution

- src/engine/backtest.py:39 function=MODULE text="transaction_cost":  0.0005, # 0.05% one-way
- src/engine/backtest.py:40 function=MODULE text="slippage":          0.0005, # 0.05% one-way
- src/engine/backtest.py:41 function=MODULE text="total_one_way":     0.0010, # cost + slippage per direction
- src/engine/backtest.py:43 function=MODULE text=# Primary Execution Model: Adverse Intraday Execution v1.0
- src/engine/backtest.py:44 function=MODULE text=# Signal Day T → Execute Day T+1
- src/engine/backtest.py:45 function=MODULE text=# BUY/ADD:     next_day_high  × (1 + cost + slippage)  ← worst buy
- src/engine/backtest.py:46 function=MODULE text=# REDUCE/EXIT: next_day_low   × (1 - cost - slippage)  ← worst sell
- src/engine/backtest.py:48 function=MODULE text="execution_model":   "adverse_intraday",
- src/engine/backtest.py:49 function=MODULE text="buy_price_field":   "high",   # T+1 high
- src/engine/backtest.py:50 function=MODULE text="sell_price_field":  "low",    # T+1 low
- src/engine/backtest.py:130 function=_rebuild_leader_score text=p = prices[:t+1]
- src/engine/backtest.py:131 function=_rebuild_leader_score text=spx = spx_prices[:t+1]
- src/engine/backtest.py:138 function=_rebuild_leader_score text=r = period_return(sym_p[:t+1], 60)
- src/engine/backtest.py:358 function=run_trade_rule_validation text=r = period_return(prices_map[sym][:t+1], 60)
- src/engine/backtest.py:365 function=run_trade_rule_validation text=p = prices_map[sym][:t+1]
- src/engine/backtest.py:502 function=run_promotion_engine_validation text=p = prices_map[sym][:t+1]
- src/engine/backtest.py:512 function=run_promotion_engine_validation text=p = prices_map[sym][:t+1]
- src/engine/backtest.py:643 function=run_action_forward_validation text=(period_return(prices_map[s][:t+1], 60) or 0.0)
- src/engine/backtest.py:644 function=run_action_forward_validation text=for s in symbols if s in prices_map and len(prices_map[s]) > t+1
- src/engine/backtest.py:650 function=run_action_forward_validation text=p = prices_map[sym][:t+1]
- src/engine/backtest.py:1104 function=run_stateful_simulation text=date_t1 = master_dates[t+1] if t+1 < len(master_dates) else None
- src/engine/backtest.py:1129 function=run_stateful_simulation text=# Adverse: 执行日最高价买入
- src/engine/backtest.py:1297 function=run_stateful_simulation text="execution_model":      "adverse_intraday_v1.0",
- src/engine/backtest.py:1377 function=run_stateful_simulation text=# STEP 3: 生成 T 日信号 → pending_orders for T+1
- src/engine/backtest.py:1386 function=run_stateful_simulation text=spx_ma50_t = sum(spx_prices[t-49:t+1]) / 50 if t >= 49 else spx_close_t

### market_gate_consumption

- src/engine/backtest.py:59 function=MODULE text="market_gate_enabled": False,
- src/engine/backtest.py:61 function=MODULE text="market_shock_gate_enabled": False,
- src/engine/backtest.py:62 function=MODULE text="market_shock_daily_return": -0.02,
- src/engine/backtest.py:847 function=run_stateful_simulation text=market_gate_enabled = bool(a.get("market_gate_enabled", True))
- src/engine/backtest.py:896 function=run_stateful_simulation text=market_shock_gate_enabled = bool(a.get("market_shock_gate_enabled", True))
- src/engine/backtest.py:897 function=run_stateful_simulation text=market_shock_daily_return = float(a.get("market_shock_daily_return", -0.02))
- src/engine/backtest.py:911 function=run_stateful_simulation text=market_gate_variant = (
- src/engine/backtest.py:912 function=run_stateful_simulation text="D1_NO_MARKET_GATE" if not market_gate_enabled else
- src/engine/backtest.py:913 function=run_stateful_simulation text="D2_RISK_OFF_GATE" if not market_shock_gate_enabled else
- src/engine/backtest.py:927 function=run_stateful_simulation text=logger.info(f"  Market Gate Variant: {market_gate_variant}")
- src/engine/backtest.py:928 function=run_stateful_simulation text=logger.info(f"  Market Gate: enabled={market_gate_enabled} "
- src/engine/backtest.py:930 function=run_stateful_simulation text=f"| Shock<={market_shock_daily_return*100:.1f}%:{market_shock_gate_enabled}")
- src/engine/backtest.py:938 function=run_stateful_simulation text=f"relstop={relative_stop_enabled} gate={market_gate_enabled} ──")
- src/engine/backtest.py:1037 function=run_stateful_simulation text="market_risk_off_block":    0,
- src/engine/backtest.py:1038 function=run_stateful_simulation text="market_shock_block":       0,
- src/engine/backtest.py:1072 function=run_stateful_simulation text=market_gate_days = {
- src/engine/backtest.py:1075 function=run_stateful_simulation text="market_shock": 0,
- src/engine/backtest.py:1393 function=run_stateful_simulation text=if not market_gate_enabled:
- src/engine/backtest.py:1396 function=run_stateful_simulation text=entry_capacity   = max_pos
- src/engine/backtest.py:1397 function=run_stateful_simulation text=market_risk_off  = False
- src/engine/backtest.py:1398 function=run_stateful_simulation text=market_shock     = False
- src/engine/backtest.py:1399 function=run_stateful_simulation text=market_entry_allowed = True
- src/engine/backtest.py:1400 function=run_stateful_simulation text=market_gate_days["entry_allowed"] += 1
- src/engine/backtest.py:1449 function=run_stateful_simulation text=market_shock_gate_enabled
- src/engine/backtest.py:1450 function=run_stateful_simulation text=and spx_day_return <= market_shock_daily_return

### account_mutation

- src/engine/backtest.py:940 function=run_stateful_simulation text=logger.info(f"  Dynamic Exit v2: ON | Hard=Close<MA50+slope<0 | FULL_ON=needs structure | CAUTIOUS/CASH=LS<60 exits")
- src/engine/backtest.py:1016 function=run_stateful_simulation text=cash            = init_cap
- src/engine/backtest.py:1163 function=run_stateful_simulation text=cash  -= shares * exec_price
- src/engine/backtest.py:1228 function=run_stateful_simulation text=cash -= target_add
- src/engine/backtest.py:1264 function=run_stateful_simulation text=cash    += proceeds
- src/engine/backtest.py:1321 function=run_stateful_simulation text=cash            += sell_shares * exec_price
- src/engine/backtest.py:1361 function=run_stateful_simulation text=total_equity = cash + position_value
- src/engine/backtest.py:1365 function=run_stateful_simulation text=logger.warn(f"  {date_t}: negative cash={cash:.2f}")
- src/engine/backtest.py:1366 function=run_stateful_simulation text=cash = 0.0
- src/engine/backtest.py:1367 function=run_stateful_simulation text=if position_value > total_equity * 1.02:
- src/engine/backtest.py:1370 function=run_stateful_simulation text=equity_curve.append(total_equity)
- src/engine/backtest.py:1498 function=run_stateful_simulation text=daily_equity_records[-1]["total_equity"]
- src/engine/backtest.py:1502 function=run_stateful_simulation text=(total_equity / _prev_equity - 1) * 100
- src/engine/backtest.py:1505 function=run_stateful_simulation text=daily_equity_peak = max(daily_equity_peak, total_equity)
- src/engine/backtest.py:1507 function=run_stateful_simulation text=(daily_equity_peak - total_equity) / daily_equity_peak * 100
- src/engine/backtest.py:1518 function=run_stateful_simulation text="positions_value": round(position_value, 2),
- src/engine/backtest.py:1519 function=run_stateful_simulation text="total_equity": round(total_equity, 2),
- src/engine/backtest.py:1522 function=run_stateful_simulation text="exposure_pct": round(position_value / total_equity * 100, 2) if total_equity > 0 else 0.0,
- src/engine/backtest.py:1523 function=run_stateful_simulation text="open_positions_count": len(holdings),
- src/engine/backtest.py:2143 function=run_stateful_simulation text=f"day={spx_day_return*100:+.1f}% cash={cash:.0f} "
- src/engine/backtest.py:2152 function=run_stateful_simulation text="total_equity":   round(total_equity, 2),
- src/engine/backtest.py:2196 function=run_stateful_simulation text=cash    += h["shares"] * exec_price
- src/engine/backtest.py:2239 function=run_stateful_simulation text="positions_value": 0.0,
- src/engine/backtest.py:2240 function=run_stateful_simulation text="total_equity": round(final_equity, 2),
- src/engine/backtest.py:2241 function=run_stateful_simulation text="open_positions_count": 0,

### uptrend_branch

- src/engine/backtest.py:805 function=run_stateful_simulation text=e1r_uptrend_execution_enabled = bool(a.get("e1r_uptrend_execution_enabled", False))
- src/engine/backtest.py:813 function=_e1r_regime_on text=return rec.get("regime") or rec.get("spx_regime") or rec.get("weekly_regime") or "UNCLASSIFIED"
- src/engine/backtest.py:818 function=_e1r_mode_for_regime text=def _e1r_mode_for_regime(regime: str) -> str:
- src/engine/backtest.py:819 function=_e1r_mode_for_regime text=if regime == "UPTREND":
- src/engine/backtest.py:820 function=_e1r_mode_for_regime text=return "UPTREND_EMERGING_CONFIRMED_ENABLED"
- src/engine/backtest.py:821 function=_e1r_mode_for_regime text=if regime == "SIDEWAYS":
- src/engine/backtest.py:823 function=_e1r_mode_for_regime text=if regime == "DOWNTREND":
- src/engine/backtest.py:825 function=_e1r_mode_for_regime text=if regime == "N/A":
- src/engine/backtest.py:829 function=_e1r_risk_budget_for_regime text=def _e1r_risk_budget_for_regime(regime: str) -> dict:
- src/engine/backtest.py:830 function=_e1r_risk_budget_for_regime text=if regime == "UPTREND":
- src/engine/backtest.py:831 function=_e1r_risk_budget_for_regime text=return {"mode": "UPTREND_RISK_ON", "max_positions": 3, "max_total_exposure_pct": 100.0}
- src/engine/backtest.py:832 function=_e1r_risk_budget_for_regime text=if regime == "SIDEWAYS":
- src/engine/backtest.py:834 function=_e1r_risk_budget_for_regime text=if regime == "DOWNTREND":
- src/engine/backtest.py:836 function=_e1r_risk_budget_for_regime text=if regime == "N/A":
- src/engine/backtest.py:1083 function=run_stateful_simulation text=# Read-only telemetry for regime/equity attribution.
- src/engine/backtest.py:1189 function=run_stateful_simulation text=# E1-R Phase 2 regime wiring telemetry. Observer-only.
- src/engine/backtest.py:1191 function=run_stateful_simulation text="entry_type": order.get("e1r_entry_type") or ("E1R_PLACEHOLDER_LEGACY_ENTRY" if e1r_regime_wiring_enabled else None),
- src/engine/backtest.py:1192 function=run_stateful_simulation text="regime_day_weights": {},
- src/engine/backtest.py:1222 function=run_stateful_simulation text=h["size_units"] = min(1.0 if e1r_uptrend_execution_enabled else 1.5, h["size_units"] + _add_size_units)
- src/engine/backtest.py:1225 function=run_stateful_simulation text=h["entry_type"] = order.get("e1r_entry_type")
- src/engine/backtest.py:1304 function=run_stateful_simulation text="dominant_regime":      _e1r_dominant_regime(h.get("regime_day_weights", {})),
- src/engine/backtest.py:1305 function=run_stateful_simulation text="entry_type":           h.get("entry_type"),
- src/engine/backtest.py:1306 function=run_stateful_simulation text="regime_day_weights":   h.get("regime_day_weights", {}),
- src/engine/backtest.py:1358 function=run_stateful_simulation text=_weights = _h.setdefault("regime_day_weights", {})
- src/engine/backtest.py:1608 function=run_stateful_simulation text="e1r_uptrend_emerging_eligible": False,

## Next stage after user approval

4C-2C-4E-ENGINE-K2-R17-LEGACY-UPTREND-INPUT-AND-CANDIDATE-BOUNDARY-GOLDEN-TRACE-PROPOSAL
