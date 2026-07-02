# E1-R Phase 3I-R — SIDEWAYS_RECOVERY Robustness Diagnostic

Diagnostic only. No trading logic changed. UPTREND Confirmed remains protected.

## Target

`UPGRADE_WATCH_RECOVERY` from Phase 3I.

## Full target metrics

- n: 20
- 20D excess: +3.90%
- 30D excess: +8.10%
- upgrade30: +25.00%
- fail20: +20.00%

## Decision

Decision: `PROMISING_BUT_STILL_DIAGNOSTIC_ONLY`
Checks passed: 5 / 7

## Robustness checks

### Year-half splits

| Window | n | 20D excess | 30D excess | upgrade30 | fail20 |
|---|---:|---:|---:|---:|---:|
| 2025H1 | 20 | +3.90% | +8.10% | +25.00% | +20.00% |

### Simple rule comparison

| Rule | raw | n | 20D excess | 30D excess | upgrade30 | fail20 |
|---|---:|---:|---:|---:|---:|---:|
| BASE_STC_COMMON_EQUITY | 959 | 43 | -1.39% | -0.91% | +13.95% | +39.53% |
| SIDEWAYS_RECOVERY_COMMON_EQUITY | 418 | 16 | +5.36% | +8.95% | +31.25% | +18.75% |
| SIDEWAYS_RECOVERY_STC90 | 269 | 16 | +5.36% | +8.95% | +31.25% | +18.75% |
| SIDEWAYS_RECOVERY_FLOW70 | 156 | 20 | +3.69% | +7.27% | +25.00% | +25.00% |
| UPGRADE_WATCH_RECOVERY | 98 | 20 | +3.90% | +8.10% | +25.00% | +20.00% |

## Interpretation

Phase 3I-R is an overfit-defense diagnostic. Passing it does not approve SIDEWAYS execution. It only determines whether Phase 3I deserves a later portfolio-level simulation.
