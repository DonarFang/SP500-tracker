# K2-R23 Uptrend Signal Adapter Consumer Wiring

## Decision

PASS_UPTREND_SIGNAL_ADAPTER_CONSUMER_WIRING

## Call chain

1. UptrendSignalConsumerPipeline.run
2. UptrendSignalAdapter.build
3. UptrendSignalAdapterResult.to_consumer_inputs
4. UptrendDecisionConsumer.consume
5. UptrendCore.decide_uptrend_buy
6. OrderIntent

## Preserved boundaries

- No legacy backtest import.
- No market-gate recomputation.
- No direct UptrendCore call from the pipeline.
- No order execution or account mutation.
- No protected source modification.

## Validation

{
  "calls_signal_adapter_build": true,
  "calls_to_consumer_inputs": true,
  "calls_decision_consumer": true,
  "imports_backtest": false,
  "calls_market_gate_evaluator": false,
  "calls_uptrend_core_directly": false,
  "calls_order_execution": false
}

## Tests

- R23 wiring tests: 7 PASS
- R22 adapter regressions: 8 PASS
- R21 consumer regressions: 8 PASS
- R20 core regressions: 7 PASS
- Total: 30 PASS

## Next stage

K2-R24-UPTREND-PIPELINE-ENGINE-ENTRY-WIRING
