# FD-M3180125 MG-Step 3

## Market State / Market Gate Evaluator 5Y Validation

Status: `COMPLETE`

Scope:

- MG-Step 3 only
- Market State Evaluator
- Market Gate Evaluator
- Five-year SPX / NDX / SOX historical replay
- Engine public Market State / Gate interface
- Independent MG-Step 1 formula oracle

Explicitly excluded:

- FW-Step 3
- Forward Seed
- Forward Runtime
- Forward dry-run
- Strategy matrix
- Portfolio performance validation

Results:

- Public data adapter: `ForwardMarketDataAdapter.parse_price_file`
- Data value type: `DailyBar`
- One-day `2021-09-28` mismatch count: 0
- Guard rows: PASS
- Short window `2021-09-20` to `2021-10-08` evaluated dates: 15
- Short-window mismatch count: 0
- Five-year evaluated dates: 1503
- First evaluated date: 2020-06-25
- Last evaluated date: 2026-06-18
- Full-history mismatch count: 0
- Market State counts: `{"CASH_MODE": 521, "CAUTIOUS_ON": 154, "FULL_ON": 828}`
- Gate State counts: `{"ALLOW": 982, "RISK_OFF": 474, "SHOCK": 47}`
- FW-Step 3 run: FALSE
- Forward execution run: FALSE
- Protected source changed: FALSE

Decision:

`PASS_MG_STEP3_5Y_EVALUATOR_VALIDATION`
