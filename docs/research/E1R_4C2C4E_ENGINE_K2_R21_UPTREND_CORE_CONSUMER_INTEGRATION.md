# K2-R21 Uptrend Core Consumer Integration

## Decision

PASS_UPTREND_CORE_CONSUMER_INTEGRATION

## Preserved contracts

- Original shell path is byte-for-byte equivalent across four golden cases.
- RegimeRouter source is unchanged.
- UptrendCore source is unchanged.
- No legacy order payload is constructed.
- No top_entry_rank is fabricated.
- No market gate is recomputed.
- No fills or order execution occur.
- No legacy backtest function is called.

## Validation

{
  "core_calls_consumer": true,
  "consumer_calls_decide_uptrend_buy": true,
  "consumer_calls_build_legacy_order": false,
  "router_calls_uptrend_components": false,
  "consumer_calls_legacy": false,
  "core_calls_legacy": false,
  "consumer_imports_market_gate_evaluator": false,
  "consumer_constructs_fill": false,
  "consumer_calls_fill_application": false
}

## Tests

- R21 consumer tests: 8 PASS
- R20 regression tests: 7 PASS
- Original shell golden cases: 4 equivalent

## Next stage

K2-R22-UPTREND-SIGNAL-ADAPTER
