# E1R K2 R17A-RCA-1 Execution Price Architecture

Generated UTC: 2026-07-11T12:02:50.998464+00:00

## Execution model

Signal day T:
- Strategy generates an order.
- Order is placed in pending_orders.

Execution day T+1:
- BUY and ADD use execution-day high.
- REDUCE and EXIT use execution-day low.
- Invalid high/low falls back to execution-day close.
- one_way is adverse in both directions.

## Layer contract

- Strategy outputs intent and target_size_units.
- Execution resolves price, shares, cash, and holdings mutation.
