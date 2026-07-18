# FD-M3180125 Engine Canonical Regime Contract Freeze

- Date: 2026-07-18
- Status: CONTRACT FROZEN
- Current fixed step: Step 1 — Mechanism Recovery and Contract Freeze
- Development repository: `sp500-tracker-v13`
- Historical evidence repository: `sp500-tracker-5y` — read-only evidence source

## Fixed Three-Step Plan

1. Mechanism Recovery and Contract Freeze
2. Engine Integration
3. Reproduction and Runtime Acceptance

No additional phase, sub-phase, audit framework, or derivative step is introduced.

## Canonical Evidence

Producer: `scripts/build_weekly_regimes.py`

Producer commit: `2c1cc5ffdac5ae89111c11fd1b4b4980b2be4216`

Producer SHA256: `5e98a302be084fd9a19996135381b60ac2ae371d9f3c5ef325a4ebdec7c59115`

Frozen SPX input SHA256: `04e09605b1bee9a900a0f3db4c1926e6bd48f8f4dceebf711b2c9511bd98633e`

The producer and four canonical Regime artifacts originated in the same historical commit.
Artifacts in `sp500-tracker-5y` and `sp500-tracker-v13` were byte-identical during recovery.

## Canonical Generation Chain

SPX daily bars
→ ISO weekly grouping
→ last available SPX trading close in each week
→ MA10W
→ MA40W
→ MA40W 13-week relative slope
→ weekly Regime and subclass
→ mandatory one-week lag
→ daily Regime map

Only SPX closes are inputs. Strategy results, account state, rankings, NDX, SOX,
VIX, breadth and future bars are forbidden inputs.

## Frozen Formulas

- `MA10W[t] = mean(C[t-9] ... C[t])`
- `MA40W[t] = mean(C[t-39] ... C[t])`
- `SLOPE13W[t] = MA40W[t] / MA40W[t-13] - 1`

Classification uses unrounded values. Stored precision is 4 decimals for MA10W
and MA40W, and 6 decimals for SLOPE13W.

## Frozen Classification

- `UNCLASSIFIED`: any required indicator is unavailable.
- `UPTREND`: `CloseW > MA40W AND MA10W > MA40W AND SLOPE13W > 0`.
- `DOWNTREND`: `CloseW < MA40W AND MA10W < MA40W AND SLOPE13W < 0`.
- `SIDEWAYS`: every other valid combination.
- `RECOVERY_TRANSITION`: SIDEWAYS with both CloseW and MA10W above MA40W,
  while SLOPE13W is less than or equal to zero.
- `DETERIORATION_TRANSITION`: SIDEWAYS with both CloseW and MA10W below MA40W,
  while SLOPE13W is greater than or equal to zero.
- `MA_CONFLICT`: every remaining SIDEWAYS combination.

## Mandatory One-Week Lag

For trading day `d`, apply the latest weekly record whose `week_end_date` is
strictly earlier than Monday of the ISO week containing `d`.

A state calculated from week `t` must not be consumed during week `t`.

## Warm-Up Contract

Dates without a prior completed weekly state must be emitted as:

- regime: `UNCLASSIFIED`
- subclass: `null`

The date must not be omitted.

## Engine Boundary

`UNCLASSIFIED` is a valid raw generator state but is not an executable trend branch.
It must produce a not-ready or defensive Engine result. Silent fallback to UPTREND,
SIDEWAYS or DOWNTREND is forbidden.

The legacy `Risk-On / Risk-Off / Neutral` module is not this Canonical Regime Generator.

## Golden Master Result

- Weekly records: 325 reference / 325 generated
- Weekly missing: 0
- Weekly extra: 0
- Weekly mismatches: 0
- Daily records: 1562 reference / 1562 generated
- Daily missing: 0
- Daily extra: 0
- Regime mismatches: 0
- Subclass mismatches: 0
- Full-state mismatches: 0

Decision: `PASS_EXACT_CANONICAL_REGIME_REPRODUCTION`

Acceptance requires zero missing dates, zero extra dates and zero full-state
`(regime, subclass)` mismatches. Aggregate counts alone are insufficient.

## Step Boundary

This file freezes Step 1 only.

It does not implement the Engine-owned generator, modify RegimeRouter, modify
strategy branches, run the 5Y strategy backtest, resume Forward testing, or begin Step 2.
