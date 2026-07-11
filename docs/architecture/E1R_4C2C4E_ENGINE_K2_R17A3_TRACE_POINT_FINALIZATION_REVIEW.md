# E1R K2 R17A-3 Final Trace Architecture

Generated UTC: 2026-07-11T12:08:28.020638+00:00

## Signal-day trace

- TP01: pre-rank candidate snapshot
- TP02: post-rank candidate snapshot
- TP03: selected-buy snapshot
- TP04: E1R BUY order-intent snapshot
- TP05: final pending-order handoff

## T+1 execution trace

- TP06: order execution start
- TP07: BUY sizing before account mutation
- TP08: BUY account mutation complete
- TP09: sell execution price finalized
- TP10A: EXIT account mutation complete
- TP10B: REDUCE account mutation complete

## Frozen execution-price contract

- BUY/ADD: T+1 high, fallback close, then multiply by (1 + one_way).
- REDUCE/REL_REDUCE/TP_REDUCE/EXIT: T+1 low, fallback close, then multiply by (1 - one_way).

## Observer boundary

- Trace code may serialize immutable snapshots only.
- Trace code may not mutate candidates, orders, cash, holdings, counters, or control flow.
