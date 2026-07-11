# E1R K2 R16 Legacy UPTREND Extraction Proposal

Compacted legacy-only human review

Generated UTC: 2026-07-11T11:13:56.370541+00:00

Decision:
PASS_COMPACTED_LEGACY_ONLY_EVIDENCE_READY_FOR_R17

## Scope

- One canonical detailed JSON is retained.
- Evidence is restricted to src/engine and src/features.
- src/e1r_engine evidence is excluded.
- No strategy source code was modified.
- No strategy logic was implemented.
- No full 5Y run was performed.
- No SIDEWAYS integration was performed.

## Category coverage

- candidate_generation: legacy_hits=60, retained=12
- ranking_and_top3_selection: legacy_hits=86, retained=12
- buy_generation: legacy_hits=59, retained=12
- add_generation: legacy_hits=42, retained=12
- hold_behavior: legacy_hits=68, retained=12
- reduce_behavior: legacy_hits=77, retained=12
- exit_behavior: legacy_hits=89, retained=12
- position_sizing: legacy_hits=6, retained=6
- pending_order_boundary: legacy_hits=17, retained=12
- next_day_execution: legacy_hits=32, retained=12
- market_gate_consumption: legacy_hits=60, retained=12
- account_mutation: legacy_hits=25, retained=12
- uptrend_branch: legacy_hits=60, retained=12

## Main legacy functions

- src/engine/backtest.py:run_stateful_simulation: 411 hits
- src/engine/backtest.py:MODULE: 52 hits
- src/engine/backtest.py:run_action_forward_validation: 48 hits
- src/engine/trade_decision.py:trade_action_reason: 44 hits
- src/engine/trade_decision.py:trade_action: 35 hits
- src/engine/backtest.py:run_trade_rule_validation: 16 hits
- src/engine/backtest.py:run_promotion_engine_validation: 14 hits
- src/engine/trade_decision.py:MODULE: 13 hits
- src/engine/backtest.py:_e1r_risk_budget_for_regime: 11 hits
- src/engine/backtest.py:_e1r_mode_for_regime: 6 hits
- src/engine/backtest.py:_load_e1r_regime_daily: 5 hits
- src/engine/backtest.py:_rebuild_leader_score: 4 hits
- src/engine/leader_ranking.py:rank_stocks: 4 hits
- src/engine/backtest.py:run_strategy_variant_comparison: 4 hits
- src/engine/backtest.py:run_leader_engine_validation: 3 hits

## High-value evidence samples

### candidate_generation

- src/engine/backtest.py:851 function=run_stateful_simulation source=# Qualified Candidate Pool 参数
- src/engine/backtest.py:852 function=run_stateful_simulation source=candidate_top_n           = a.get("candidate_top_n", None)   # None = 沿用旧 entry_top_n
- src/engine/backtest.py:853 function=run_stateful_simulation source=qualified_entry_enabled   = bool(a.get("qualified_entry_enabled", False))
- src/engine/backtest.py:854 function=run_stateful_simulation source=qualified_rs_min          = float(a.get("qualified_rs_min", 90.0))

### ranking_and_top3_selection

- src/engine/backtest.py:784 function=run_stateful_simulation source=Layer D v1.6: Strict Top3 + RS threshold + MinHold + Relative SPX Stop
- src/engine/backtest.py:792 function=run_stateful_simulation source=logger.info("[Backtest Layer D v1.6] Strict Top3 + RS/MinHold/RelStop Backtest...")
- src/engine/backtest.py:796 function=run_stateful_simulation source=max_pos  = a["max_positions"]
- src/engine/backtest.py:797 function=run_stateful_simulation source=buy_pct  = a["buy_size"]  / max_pos       # Top3: 1/3 per full slot

### buy_generation

- src/engine/backtest.py:1035 function=run_stateful_simulation source="qualified_candidate_generated":    0,   # qualified: 候选池 BUY 已生成
- src/engine/backtest.py:1046 function=run_stateful_simulation source="action_reason_buy_add_mismatch":  0,   # BUY/ADD 不一致（记录，不中断）
- src/engine/backtest.py:1047 function=run_stateful_simulation source="fill_only_no_empty_slot":         0,   # fill_only 模式：无空仓位，跳过 BUY
- src/engine/backtest.py:1048 function=run_stateful_simulation source="e1r_legacy_buy_blocked":          0,   # E1-R execution: legacy BUY suppressed

### add_generation

- src/engine/backtest.py:1046 function=run_stateful_simulation source="action_reason_buy_add_mismatch":  0,   # BUY/ADD 不一致（记录，不中断）
- src/engine/backtest.py:1051 function=run_stateful_simulation source="e1r_emerging_to_confirmed_add":   0,   # E1-R execution: upgrade ADD generated
- src/engine/backtest.py:1056 function=run_stateful_simulation source=portfolio_action_dist = {"HOLD": 0, "ADD": 0, "REDUCE": 0, "REL_REDUCE": 0, "EXIT": 0, "TP_REDUCE": 0}
- src/engine/backtest.py:1128 function=run_stateful_simulation source=if action in ("BUY", "ADD"):

### hold_behavior

- src/engine/backtest.py:903 function=run_stateful_simulation source=min_holding_days = int(a.get("min_holding_days", 0))
- src/engine/backtest.py:906 function=run_stateful_simulation source=min_hold_allow_broken_exit = bool(a.get("min_hold_allow_broken_exit", True))
- src/engine/backtest.py:931 function=run_stateful_simulation source=logger.info(f"  Entry filter: RS >= {entry_rs_min:.1f}; MinHold={min_holding_days}d; "
- src/engine/backtest.py:937 function=run_stateful_simulation source=f"top_n={entry_top_n} minhold={min_holding_days} "

### reduce_behavior

- src/engine/backtest.py:798 function=run_stateful_simulation source=add_pct  = a["add_size"]  / max_pos       # Top3: +1/6, only useful after REDUCE
- src/engine/backtest.py:849 function=run_stateful_simulation source=ls60_exit_mode = a.get("ls60_exit_mode", "reduce")  # "exit"=旧规则 "reduce"=新规则
- src/engine/backtest.py:894 function=run_stateful_simulation source=if ls60_exit_mode not in {"exit", "reduce"}:
- src/engine/backtest.py:895 function=run_stateful_simulation source=raise ValueError(f"Invalid ls60_exit_mode={ls60_exit_mode!r}; expected 'exit' or 'reduce'")

### exit_behavior

- src/engine/backtest.py:849 function=run_stateful_simulation source=ls60_exit_mode = a.get("ls60_exit_mode", "reduce")  # "exit"=旧规则 "reduce"=新规则
- src/engine/backtest.py:894 function=run_stateful_simulation source=if ls60_exit_mode not in {"exit", "reduce"}:
- src/engine/backtest.py:895 function=run_stateful_simulation source=raise ValueError(f"Invalid ls60_exit_mode={ls60_exit_mode!r}; expected 'exit' or 'reduce'")
- src/engine/backtest.py:904 function=run_stateful_simulation source=# E2 Dynamic Exit parameters

### position_sizing

- src/engine/backtest.py:1030 function=run_stateful_simulation source="size_at_minimum":          0,
- src/engine/backtest.py:1317 function=run_stateful_simulation source=skip_reasons["size_at_minimum"] += 1
- src/engine/backtest.py:840 function=_e1r_dominant_regime source=def _e1r_dominant_regime(weights: dict) -> str:
- src/engine/backtest.py:841 function=_e1r_dominant_regime source=if not weights:

### pending_order_boundary

- src/engine/backtest.py:1018 function=run_stateful_simulation source=pending_orders: list[dict] = []
- src/engine/backtest.py:1112 function=run_stateful_simulation source=pending_orders = []   # 不生成订单
- src/engine/backtest.py:1120 function=run_stateful_simulation source=for order in pending_orders:
- src/engine/backtest.py:1123 function=run_stateful_simulation source=sig_date  = order["signal_date"]   # 信号日期

### next_day_execution

- src/engine/backtest.py:1104 function=run_stateful_simulation source=date_t1 = master_dates[t+1] if t+1 < len(master_dates) else None
- src/engine/backtest.py:1129 function=run_stateful_simulation source=# Adverse: 执行日最高价买入
- src/engine/backtest.py:1297 function=run_stateful_simulation source="execution_model":      "adverse_intraday_v1.0",
- src/engine/backtest.py:1377 function=run_stateful_simulation source=# STEP 3: 生成 T 日信号 → pending_orders for T+1

### market_gate_consumption

- src/engine/backtest.py:847 function=run_stateful_simulation source=market_gate_enabled = bool(a.get("market_gate_enabled", True))
- src/engine/backtest.py:896 function=run_stateful_simulation source=market_shock_gate_enabled = bool(a.get("market_shock_gate_enabled", True))
- src/engine/backtest.py:897 function=run_stateful_simulation source=market_shock_daily_return = float(a.get("market_shock_daily_return", -0.02))
- src/engine/backtest.py:911 function=run_stateful_simulation source=market_gate_variant = (

### account_mutation

- src/engine/backtest.py:940 function=run_stateful_simulation source=logger.info(f"  Dynamic Exit v2: ON | Hard=Close<MA50+slope<0 | FULL_ON=needs structure | CAUTIOUS/CASH=LS<60 exits")
- src/engine/backtest.py:1016 function=run_stateful_simulation source=cash            = init_cap
- src/engine/backtest.py:1163 function=run_stateful_simulation source=cash  -= shares * exec_price
- src/engine/backtest.py:1228 function=run_stateful_simulation source=cash -= target_add

### uptrend_branch

- src/engine/backtest.py:805 function=run_stateful_simulation source=e1r_uptrend_execution_enabled = bool(a.get("e1r_uptrend_execution_enabled", False))
- src/engine/backtest.py:1083 function=run_stateful_simulation source=# Read-only telemetry for regime/equity attribution.
- src/engine/backtest.py:1189 function=run_stateful_simulation source=# E1-R Phase 2 regime wiring telemetry. Observer-only.
- src/engine/backtest.py:1191 function=run_stateful_simulation source="entry_type": order.get("e1r_entry_type") or ("E1R_PLACEHOLDER_LEGACY_ENTRY" if e1r_regime_wiring_enabled else None),

## Next stage after user approval

4C-2C-4E-ENGINE-K2-R17-LEGACY-UPTREND-INPUT-AND-CANDIDATE-BOUNDARY-GOLDEN-TRACE-PROPOSAL
