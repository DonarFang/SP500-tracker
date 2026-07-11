# K2-R24 Uptrend Pipeline Engine Entry Wiring

## Decision

PASS_UPTREND_PIPELINE_ENGINE_ENTRY_WIRING

## Engine entry chain

1. E1RCoreEngine.step
2. E1RCoreEngine._step_uptrend_pipeline
3. UptrendSignalConsumerPipeline.run
4. UptrendSignalAdapter.build
5. UptrendSignalAdapterResult.to_consumer_inputs
6. UptrendDecisionConsumer.consume
7. UptrendCore.decide_uptrend_buy
8. OrderIntent

## Preserved boundaries

- Legacy shell behavior remains byte-for-byte unchanged.
- Engine-level NOOP fallback remains intact.
- RegimeRouter remains route-only.
- Market gate is supplied, not recomputed.
- No fills, execution, or account trade mutation occur.
- Legacy backtest.py is not imported.

## Initial test failure review

Two initial tests incorrectly compared strategy-only pipeline orders with engine-level orders. The engine correctly retained its NOOP fallback when the pipeline emitted no strategy order. No implementation change was required; the test contract was corrected.

## Tests

- R24 engine-entry tests: 7 PASS
- R23 wiring regressions: 7 PASS
- R22 adapter regressions: 8 PASS
- R21 consumer regressions: 8 PASS
- R20 core regressions: 7 PASS
- Shell golden cases: 4 byte-equivalent
- Total unit tests: 37 PASS

## Next stage

K2-R25-UPTREND-ENGINE-ENTRY-EQUIVALENCE-SMOKE
