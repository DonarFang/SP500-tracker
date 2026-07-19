# FD-M3180125 MG Formal 5Y Correction

## Decision

`PASS_MG_STEP123_FORMAL_5Y_EQUIVALENCE`

## MG-Step 1

Corrected the canonical Engine default contract to the formal five-year
configuration:

- `D2_RISK_OFF_GATE`
- Shock disabled
- direct SPX-below-MA50 risk-off flag disabled
- MA50 ten-session slope enabled
- SPX/NDX/SOX leadership enabled

Optional D3 Shock capability remains available only through explicit opt-in.

## MG-Step 2

`E1RCoreEngine` owns and consumes the corrected Market State and Market
Gate defaults. The locked contract and integration test set passes.

## MG-Step 3

- Formal dates: 1259
- Date range: 2021-06-11 to 2026-06-16
- Gate mismatch count: 0
- Base-field mismatch count: 0
- Market State counts: {'FULL_ON': 660, 'CAUTIOUS_ON': 134, 'CASH_MODE': 465}
- Gate State counts: {'ALLOW': 794, 'RISK_OFF': 465}

The formal artifact does not persist the three-state Market State field.
Market State is reconstructed from the canonical formula and configuration,
and its resulting Gate matches all 1259 formal dates.

## Boundaries

- `src/engine/backtest.py` unchanged.
- No FW-Step 3 execution.
- No scope outside MG-Step 1/2/3.
