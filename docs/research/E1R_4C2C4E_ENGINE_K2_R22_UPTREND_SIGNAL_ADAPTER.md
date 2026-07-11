# K2-R22 Uptrend Signal Adapter

## Decision

PASS_UPTREND_SIGNAL_ADAPTER

## Boundary

- Consumes ordered symbols and price histories.
- Reuses existing frozen feature and decision functions.
- Produces day_signals and leader_rank_all.
- Converts the result to UptrendConsumerInputs.

## Non-responsibilities

- Does not import legacy backtest.py.
- Does not recompute market gate state.
- Does not rank UPTREND buy candidates.
- Does not select BUY orders.
- Does not execute trades or mutate accounts.

## Validation

{
  "required_imports_present": true,
  "imports_backtest": false,
  "calls_uptrend_core": false,
  "calls_market_gate_evaluator": false,
  "calls_legacy_order_builder": false,
  "calls_trade_execution": false,
  "builds_consumer_inputs": true
}

## Tests

- R22 adapter tests: 8 PASS
- R21 consumer regression tests: 8 PASS
- R20 core regression tests: 7 PASS
- Total: 23 PASS

## Next stage

K2-R23-UPTREND-SIGNAL-ADAPTER-CONSUMER-WIRING
