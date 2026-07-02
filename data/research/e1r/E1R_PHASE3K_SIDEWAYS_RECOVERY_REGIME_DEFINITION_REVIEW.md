# E1-R Phase 3K — SIDEWAYS Recovery Regime Definition Review

## Status

DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE

This diagnostic does not change E1, E1-R, UPTREND Confirmed, or trading logic.

## Core Question

Is `SIDEWAYS_RECOVERY` a meaningful sub-regime, or did Phase 3I only capture a narrow time-window artifact?

## Rule Summary

| Rule | n | 20D Excess | 30D Excess | Upgrade30 | Fail20 |
|---|---:|---:|---:|---:|---:|
| BASE_STC_COMMON_EQUITY | 43 | -1.39% | -0.91% | 13.95% | 39.53% |
| SIDEWAYS_RECOVERY_COMMON_EQUITY | 16 | +5.36% | +8.95% | n/a | n/a |
| SIDEWAYS_RECOVERY_STC90 | 16 | +5.36% | +8.95% | n/a | n/a |
| SIDEWAYS_RECOVERY_FLOW70 | 20 | +3.69% | +7.27% | n/a | n/a |
| UPGRADE_WATCH_RECOVERY | 20 | +3.90% | +8.10% | 25.00% | 10.00% |

## Time-Window Coverage

| Window | n | 20D Excess | 30D Excess | Upgrade30 | Fail20 |
|---|---:|---:|---:|---:|---:|
| 2025H1 | 20 | +3.90% | +8.10% | n/a | n/a |

## Regime Definition Checks

| Check | Result | Detail |
|---|---:|---|
| recovery_subregime_has_positive_excess | PASS | SIDEWAYS_RECOVERY_COMMON_EQUITY: 20D excess +5.36%, 30D excess +8.95%. |
| target_rule_positive_excess | PASS | UPGRADE_WATCH_RECOVERY: 20D excess +3.90%, 30D excess +8.10%. |
| simple_rule_competitive_with_complex_rule | PASS | Simple recovery 30D excess +8.95% vs target 30D excess +8.10%. |
| time_window_coverage_at_least_two_halves | FAIL | Eligible half-windows: ['2025H1']. |
| positive_30d_in_at_least_two_halves | FAIL | Positive 30D excess half-windows: ['2025H1']. |
| target_fail20_better_than_base | PASS | Target fail20 10.00% vs base fail20 39.53%. |
| target_sample_at_least_20 | PASS | Target dedup_top1_count=20. |

## Decision

**PROMISING_BUT_TIME_CONCENTRATED_DIAGNOSTIC_ONLY**

SIDEWAYS_RECOVERY appears meaningful, but evidence is concentrated in too few half-year windows. Keep as Watchlist/Upgrade Watch only.

## Research Policy

`UPGRADE_WATCH_RECOVERY` remains High Quality Watchlist / Upgrade Watch only. It is not approved for execution. UPTREND Confirmed remains unchanged.
