# E1R UPTREND Step 3 — Formal Replacement

## Decision

`PASS_UPTREND_STEP3_FORMAL_REPLACEMENT`

## Runtime architecture

The official UPTREND decision source is `E1RCoreEngine.step`.
The Engine emits standard `OrderIntent` objects; a thin boundary
adapter translates them into the existing pending/T+1 contract.
SP500-specific payloads remain outside the Engine core.

This preserves one core contract for backtesting, forward testing
and future live trading, while future data sources connect through
adapters rather than changing strategy logic.

## Short-window evidence

- Window: 2021-06-01 through 2021-12-31
- Result hash: 213a9394f7163f2c8a486f935d7de3401b6b0fc3e72d9c0ff244b07bdcee35c3
- Trace rows: 832
- TP01 / TP02: 150 / 150
- TP03 / TP04 / TP08: 10 / 10 / 10
- TP10A / TP10B: 7 / 11

## Full-history matched RCA evidence

- Window: 2021-06-11 through 2026-06-16
- Legacy: committed Step-2 code at c271dad
- Engine: current Step-3 code
- Result hashes equal
- Recursive result differences: 0
- Trace rows: 4476 / 4476
- Trace hashes equal
- First trace difference: null
- Daily equity records: 1259
- Trades: 60

Matched economic result:

- Total return: +223.43%
- SPX return: +76.84%
- Alpha: +146.59%
- CAGR: +26.48%
- Max drawdown: 23.66%
- Profit factor: 2.54
- Sharpe ratio: 0.78

The Engine replacement did not alter selection, orders, fills,
account state or performance.

## RCA conclusion

The previous failure came from reading nonexistent field
`simulation_days`. The actual schema uses
`daily_equity_record_count` and `daily_equity_records`.

No strategy, Market Gate, execution or account rule changed.

## Fixed three-step plan

1. Decision equivalence — PASS
2. Execution wiring — PASS
3. Formal replacement — PASS

`UPTREND COMPLETE — MOVE TO SIDEWAYS`
