# FD-M3180125 Engine Market State + Market Gate Integration

## Step 1 — Definition and Contract Freeze

Status: `COMPLETE_PENDING_TEST_AND_COMMIT`

This record freezes the roles, inputs, formulas, outputs, and transaction effects of `MarketStateEvaluator` and `MarketGateEvaluator` before either is integrated into `E1RCoreEngine`.

## Canonical chain

Standard market data → MarketStateEvaluator → MarketStateDecision → MarketGateEvaluator → MarketGateDecision → E1RCoreEngine strategy branch → OrderIntent

## MarketStateEvaluator

Purpose: classify market risk and compute new-risk capacity.

Frozen inputs: date, SPX close, SPX MA50, SPX MA50 ten-trading-day-ago value, SPX one-day return, NDX close/MA50, SOX close/MA50, max_positions.

Frozen formulas:

- `spx_ma50_slope = spx_ma50(t) / spx_ma50(t-10) - 1`
- `leadership_ratio = indices_above_own_ma50 / available_indices`
- `shock_active = shock_enabled AND spx_day_return <= -0.02`
- `CASH_MODE` when shock is active, leadership ratio is below `2/3`, or SPX MA50 slope is negative
- `FULL_ON` when SPX is above MA50, slope is non-negative, leadership ratio is `1.0`, and shock is inactive
- otherwise `CAUTIOUS_ON`
- entry capacity: `FULL_ON=max_positions`, `CAUTIOUS_ON=min(max_positions,2)`, `CASH_MODE=0`

VIX is not part of the canonical Gate.

## MarketGateEvaluator

Purpose: convert the frozen market state and capacity into standardized new-risk permissions.

Frozen formulas:

- `market_shock = shock_enabled AND spx_day_return <= -0.02`
- `market_risk_off = market_state == CASH_MODE AND NOT market_shock`
- `market_entry_allowed = entry_capacity > 0`
- `ALLOW` when entry is allowed
- `SHOCK` when entry is blocked and shock is active
- otherwise `RISK_OFF`

## Transaction effect

Blocked: BUY, ADD, and new-risk expansion above entry capacity.

Unaffected: HOLD, REDUCE, EXIT.

Recovered downstream rule to preserve during integration: `CAUTIOUS_ON` and `CASH_MODE` block ADD.

## Step 1 boundary

Step 1 must not modify `E1RCoreEngine`, `src/engine/backtest.py`, Forward runtime, Live runtime, Regime formulas, ranking, sizing, or strategy logic.

Step 2 is the only authorized step for Engine integration.
