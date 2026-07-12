# K2-R25 UPTREND Engine Entry Equivalence Smoke

## Decision

`PASS_UPTREND_ENGINE_ENTRY_EQUIVALENCE_SMOKE`

## Window

- 2021-06-01 to 2021-12-31
- Compared days: 150
- Legacy selected BUY days: 10
- Legacy BUY order-intent days: 10
- Gate-blocked days: 19
- Mismatches: 0

## Boundary

Legacy TP01-TP04 decision records were replayed through `E1RCoreEngine.step(uptrend_inputs=...)`. The comparison covers candidate counts/symbols, selected symbol, entry type, target size units, gate state, and BUY OrderIntent semantics.

R22-R24 separately prove adapter-to-consumer pipeline wiring, so R25 does not duplicate those tests.

## Backtest scope

- One frozen 2021_H2 short-window legacy run
- No full 5Y backtest
- No strategy or engine source modification

## Next stage

K2-R26-SIDEWAYS-LEGACY-CONTRACT-CAPTURE
