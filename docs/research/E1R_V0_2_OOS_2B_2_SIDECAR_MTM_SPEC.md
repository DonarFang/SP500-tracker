# E1R v0.2 OOS-2B.2 Sidecar MTM Specification

## Status

Strategy ID: E1R_REGIME_AWARE_V0_2  
Phase: OOS-2B.2  
Purpose: Add sidecar daily mark-to-market tracking to forward/OOS equity curve  
Execution Status: PAPER_TRACKING_NO_REAL_EXECUTION  

## Context

E1R v0.2 has already completed:

1. Formal 5Y backtest engine
2. Implementation manifest
3. Dashboard market state UI
4. OOS-1 status/signal export
5. OOS-2A 5Y backtest equity export
6. OOS-2B.1 forward/OOS equity curve initialization

Before OOS-2B.2, forward/OOS equity has the fields:

- core_equity
- sidecar_equity
- combined_equity
- core_daily_return
- sidecar_daily_return
- combined_daily_return

But sidecar MTM return was not yet connected.

## Core Rule

Sidecar MTM must avoid lookahead.

T close:

- Generate sidecar target positions.

T+1 close:

- Calculate sidecar MTM return using T positions and T -> T+1 close-to-close returns.

Therefore:

sidecar_daily_return(D) = sum(weight_i(D-1) * return_i(D-1 -> D))

The system must not use positions selected on date D to calculate return already earned on date D.

## State Model

E1R v0.2 uses mutually exclusive daily market states:

- UPTREND
- DOWNTREND
- SIDEWAYS_MA_CONFLICT
- SIDEWAYS_DETERIORATION
- SIDEWAYS_RECOVERY
- UNKNOWN

Sidecar is active only when:

market_state == SIDEWAYS_MA_CONFLICT

## Sidecar Position Source

The current day's sidecar target positions come from:

exports/oos_e1r_v0_2_sidecar.json

They are stored into the forward/OOS equity record as:

sidecar_positions

These positions are used for the next trading interval's MTM calculation.

## MTM Status Values

- CALCULATED_FROM_PREVIOUS_POSITIONS
- NO_PREVIOUS_SIDECAR_POSITIONS
- PREVIOUS_SIDECAR_INACTIVE
- MISSING_PRICE_DATA
- SAME_DATE_NO_NEW_MTM

## Execution Boundary

This phase is still paper tracking.

- No real orders are executed.
- No broker integration is used.
- No transaction costs are applied yet.
- No slippage is applied yet.

## Future Work

Next phases:

1. Sidecar simulated position lifecycle
2. Transaction cost / turnover analysis
3. Realistic order generation
4. OOS combined equity audit report
5. Promotion rules for production-like tracking
