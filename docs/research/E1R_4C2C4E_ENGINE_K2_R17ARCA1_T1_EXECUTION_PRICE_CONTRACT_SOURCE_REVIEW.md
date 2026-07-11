# E1R K2 R17A-RCA-1 T+1 Execution Price Contract Review

Generated UTC: 2026-07-11T12:02:50.998464+00:00

Decision: PASS_T1_HIGH_BUY_LOW_SELL_EXECUTION_CONTRACT_PROVEN

## Contract

- BUY / ADD: T+1 high; fallback close; exec_price = raw * (1 + one_way).
- REDUCE / EXIT: T+1 low; fallback close; exec_price = raw * (1 - one_way).
- signal_date comes from the pending order; exec_date is the current loop date.

## Validation

- pending_execution_loop_count: 1
- buy_add_branch_count: 1
- sell_branch_count: 1
- buy_high_call_count: 1
- buy_close_call_count: 2
- sell_low_call_count: 1
- sell_close_call_count: 1
- buy_exec_price_assignment_count: 2
- sell_exec_price_assignment_count: 1
- buy_high_proven: True
- buy_close_fallback_proven: True
- buy_positive_one_way_cost_proven: True
- sell_low_proven: True
- sell_close_fallback_proven: True
- sell_negative_one_way_cost_proven: True
- signal_to_execution_date_proven: True
- buy_cash_and_holdings_proven: True
- sell_cash_and_holdings_proven: True
- full_execution_price_contract_proven: True
- source_modified: False
- instrumentation_implemented: False
- strategy_logic_implemented: False
- full_5y_run_performed: False
- sideways_logic_added: False
- frozen_files_unchanged: True

## Next stage

4C-2C-4E-ENGINE-K2-R17A-3-TRACE-POINT-FINALIZATION-REVIEW
