# E1R K2 R17A-RCA Selected-Buy to Buy-Orders Control-Flow Review

Generated UTC: 2026-07-11T11:51:28.413347+00:00

Decision: PASS_SELECTED_BUY_TO_BUY_ORDERS_CONTROL_FLOW_PROVEN

## Formal RCA scope

- Read-only AST control-flow review.
- No instrumentation implemented.
- No strategy source modified.
- No order logic implemented.
- No full 5Y run performed.
- No SIDEWAYS integration performed.

## Proven boundary nodes

- selected_buy_finalized: line=1721; end_line=1726; source=e1r_selected_buy = {                         "sym": _sym,                         "sig": _sig,                         "entry_type": _etype,                         "target_size_units": 1.0 if _etype == "E1R_UPTREND_CONFIRMED" else 0.5,                     }
- selected_buy_consumed: line=1782; end_line=1804; source=if (                 e1r_uptrend_execution_enabled                 and e1r_selected_buy                 and sym == e1r_selected_buy["sym"]                 and sym not in holdings             ):                 _etype = e1r_selected_buy["entry_type"]                 buy_orders.append({                     "sym":            sym,                     "action":         "BUY",                     "signal_date":    date_t,                     "ls":             ls,                     "close_t":        close_t,                     "entry_rank":     top_entry_rank.get(sym) or leader_rank_all.get(sym),                     "strategy":       "E1R_UPTREND_EXECUTION_V0_1",                     "entry_mode":     "e1r_uptrend_execution_v0_1",                     "primary_reason": _etype,                     "reasons":        sig.get("e1r_entry_reason", []),                     "e1r_entry_type": _etype,                     "target_size_units": e1r_selected_buy["target_size_units"],                 })                 skip_reasons["e1r_candidate_buy_generated"] += 1                 continue
- target_size_conversion: line=1789; end_line=1802; source=buy_orders.append({                     "sym":            sym,                     "action":         "BUY",                     "signal_date":    date_t,                     "ls":             ls,                     "close_t":        close_t,                     "entry_rank":     top_entry_rank.get(sym) or leader_rank_all.get(sym),                     "strategy":       "E1R_UPTREND_EXECUTION_V0_1",                     "entry_mode":     "e1r_uptrend_execution_v0_1",                     "primary_reason": _etype,                     "reasons":        sig.get("e1r_entry_reason", []),                     "e1r_entry_type": _etype,                     "target_size_units": e1r_selected_buy["target_size_units"],                 })
- buy_order_creation: line=1789; end_line=1802; source=buy_orders.append({                     "sym":            sym,                     "action":         "BUY",                     "signal_date":    date_t,                     "ls":             ls,                     "close_t":        close_t,                     "entry_rank":     top_entry_rank.get(sym) or leader_rank_all.get(sym),                     "strategy":       "E1R_UPTREND_EXECUTION_V0_1",                     "entry_mode":     "e1r_uptrend_execution_v0_1",                     "primary_reason": _etype,                     "reasons":        sig.get("e1r_entry_reason", []),                     "e1r_entry_type": _etype,                     "target_size_units": e1r_selected_buy["target_size_units"],                 })
- pending_orders_handoff: line=2134; end_line=2134; source=pending_orders = management_orders + buy_orders
- pending_orders_execution_loop: line=1102; end_line=2162; source=for t in range(min_history, n_days - 2):         date_t  = master_dates[t]   if t   < len(master_dates) else None         date_t1 = master_dates[t+1] if t+1 < len(master_dates) else None         if not date_t or not date_t1:             continue          # ── 交易执行区间过滤 ────────────────────────────         # master_dates 保持完整（指标计算不受影响）；         # 只有在 [_trade_start, _trade_end] 区间内才执行交易和统计         if _trade_start and date_t < _trade_start:             pending_orders = []   # 不生成订单             continue         if _trade_end and date_t > _trade_end:             break          # ════════════════════════════════════════════════         # STEP 1: 执行前一日 pending orders（T-1信号 → T日执行）         # ════════════════════════════════════════════════         for order in pending_orders:             sym       = order["sym"]             action    = order["action"]             sig_date  = order["signal_date"]   # 信号日期             exec_date = date_t                 # 执行日期 = 今天             ls        = order["ls"]             close_ref = order["close_t"]       # 信号日收盘（参考价）              if action in ("BUY", "ADD"):                 # Adverse: 执行日最高价买入                 raw = get_price_by_date(sym, exec_date, "high")                 if raw <= 0:                     raw = get_price_by_date(sym, exec_date, "close")                 if raw <= 0:                     skip_reasons["no_t1_price"] += 1                     continue                 exec_price = raw * (1 + one_way)                  port_val = cash + sum(                     h["shares"] * h.get("current_close", h["avg_cost"])                     for h in holdings.values()                 )                  if action == "BUY":                     if sym in holdings:                         skip_reasons["already_holding"] += 1                         continue                     if len(holdings) >= max_pos:                         skip_reasons["max_positions_reached"] += 1                         continue                     _order_size_units = float(order.get("target_size_units", 1.0))                     _order_size_units = max(0.0, min(_order_size_units, 1.0))                     target = port_val * buy_pct * _order_size_units                     if port_val > 0 and target / port_val > max_pct:                         target = port_val * max_pct                         skip_reasons["max_single_size_reached"] += 1                     if target > cash:                         if cash * 0.99 < 10:                             skip_reasons["cash_insufficient"] += 1                             continue                         target = cash * 0.99                      shares = target / exec_price                     cash  -= shares * exec_price                     orders_executed += 1                     holdings[sym] = {                         "shares":                shares,                         "avg_cost":              exec_price,                         "size_units":            _order_size_units,                         "entry_close_ref":       close_ref,                         "entry_date":            exec_date,                         "entry_sig_date":        sig_date,                         "entry_signal":          "BUY",                         "e1r_entry_type":       order.get("e1r_entry_type"),                         "highest_close":         close_ref,                         "min_close_since_entry": close_ref,                         "current_close":         close_ref,                         "leader_score_entry":    ls,                         "entry_spx":             spx_prices[master_dates.index(exec_date)] if exec_date in master_dates else spx_close_t,                         "relative_stop_triggered": False,                         "relative_stop_signal_date": None,                         "relative_stop_exec_date": None,                         "take_profit_triggered": False,                         "take_profit_signal_date": None,                         "take_profit_exec_date": None, ...TRUNCATED...
- holdings_buy_mutation: line=1165; end_line=1193; source=holdings[sym] = {                         "shares":                shares,                         "avg_cost":              exec_price,                         "size_units":            _order_size_units,                         "entry_close_ref":       close_ref,                         "entry_date":            exec_date,                         "entry_sig_date":        sig_date,                         "entry_signal":          "BUY",                         "e1r_entry_type":       order.get("e1r_entry_type"),                         "highest_close":         close_ref,                         "min_close_since_entry": close_ref,                         "current_close":         close_ref,                         "leader_score_entry":    ls,                         "entry_spx":             spx_prices[master_dates.index(exec_date)] if exec_date in master_dates else spx_close_t,                         "relative_stop_triggered": False,                         "relative_stop_signal_date": None,                         "relative_stop_exec_date": None,                         "take_profit_triggered": False,                         "take_profit_signal_date": None,                         "take_profit_exec_date": None,                         "realized_pnl":          0.0,                         "realized_cost_basis":   0.0,                         "action_history":        ["BUY"],                         "ls60_reduce_triggered": False,  # 方案A：LS<60 REDUCE 一次性保护                         # E1-R Phase 2 regime wiring telemetry. Observer-only.                         "entry_regime": _e1r_regime_on(exec_date),                         "entry_type": order.get("e1r_entry_type") or ("E1R_PLACEHOLDER_LEGACY_ENTRY" if e1r_regime_wiring_enabled else None),                         "regime_day_weights": {},                     }

## Control-flow checks

- candidate_sort (1716) < best_entry_selection (1719): True
- best_entry_selection (1719) < selected_buy_finalized (1721): True
- selected_buy_finalized (1721) < selected_buy_consumed (1782): True
- selected_buy_consumed (1782) <= buy_order_creation (1789): True
- buy_order_creation (1789) < pending_orders_handoff (2134): True

## Validation

- selected_buy_finalized_count: 1
- selected_buy_consuming_if_count: 1
- target_size_node_count: 7
- target_size_conversion_candidate_count: 1
- buy_action_node_count: 10
- buy_orders_assignment_count: 1
- buy_orders_append_count: 3
- buy_orders_extend_count: 0
- order_dict_candidate_count: 7
- pending_orders_assignment_count: 3
- pending_execution_loop_candidate_count: 2
- holdings_mutation_count: 1
- buy_holdings_mutation_count: 1
- candidate_selection_chain_proven: True
- selected_buy_to_order_proven: True
- target_size_conversion_proven: True
- buy_order_payload_proven: True
- buy_orders_to_pending_proven: True
- pending_to_execution_proven: True
- execution_to_holdings_proven: True
- full_chain_proven: True
- source_modified: False
- instrumentation_implemented: False
- strategy_logic_implemented: False
- full_5y_run_performed: False
- sideways_logic_added: False
- frozen_files_unchanged: True

## Root cause

- Earlier reviews relied on broad textual matches and did not inspect complete order AST nodes.
- This review directly inspects buy_orders mutations, payloads, pending handoff, execution loop, and holdings mutation.

## Next stage

4C-2C-4E-ENGINE-K2-R17A-3-TRACE-POINT-FINALIZATION-REVIEW
