# E1-R Phase 3C Channel Diagnostic Report

Generated at: 2026-07-01 18:28:02

Status: **DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE**

## 1. Fairness Controls

E1 and E1-R must be compared under the same daily dates and the same SPX regime map. Period A/B is not the primary evaluation dimension for E1-R.

## 2. Portfolio Summary

| Strategy | Return | MaxDD | PF | Sharpe | Exposure | Trades |
|---|---:|---:|---:|---:|---:|---:|
| E1_AUDITED_G4_MINHOLD10 | +7.52% | 38.1% | 1.25 | 0.18 | 80.1% | 47 |
| E1R_REGIME_AWARE_V0_1 | +65.71% | 32.35% | 1.97 | 0.58 | 74.9% | 39 |

## 3. Candidate Funnel

Raw E1-R candidates: **5564** across **562** candidate days.

Candidate type counts: `{'E1R_UPTREND_EMERGING': 2893, 'E1R_UPTREND_CONFIRMED': 2671}`

Daily mix counts: `{'both': 547, 'confirmed_only': 14, 'emerging_only': 1}`

Top-1 type counts under Phase 3B priority: `{'E1R_UPTREND_CONFIRMED': 561, 'E1R_UPTREND_EMERGING': 1}`

Executed trade type counts: `{'E1R_UPTREND_CONFIRMED': 39}`

Emerging non-execution diagnosis: **EMERGING_TOP1_EXISTED_BUT_NOT_EXECUTED_CHECK_CAPACITY_GATE_OR_EXISTING_HOLDINGS**

## 4. Channel Trade Stats

| Channel | Trades | Closed ex SIM_END | SIM_END | Avg Return | Median | Win Rate | Best | Worst |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| E1R_UPTREND_CONFIRMED | 39 | 37 | 2 | +4.02% | -2.31% | 38.5% | +60.46% | -16.45% |

## 5. Forward Alpha From Prior Diagnostic

| Channel | Candidates | 20D Avg | 20D Excess | 30D Avg | 30D Excess | 30D Excess WR |
|---|---:|---:|---:|---:|---:|---:|
| E1R_UPTREND_CONFIRMED | 1060 | +3.41% | +2.22% | +4.22% | +2.51% | 48.1% |
| E1R_UPTREND_EMERGING | 1409 | +2.20% | +1.14% | +2.57% | +0.90% | 49.2% |
| ALL | 2469 | +2.72% | +1.60% | +3.27% | +1.59% | 48.7% |

## 6. Regime Gap From Fair Review

| Regime | Days | E1R-E1 PnL | E1R-E1 Compound | E1R-E1 Excess vs SPX | Exposure Delta | MaxDD Delta |
|---|---:|---:|---:|---:|---:|---:|
| UPTREND | 565 | +60.29% | +60.30% | +60.30% | +3.21% | -4.91% |
| SIDEWAYS | 86 | -0.03% | -0.04% | -0.04% | -24.34% | -5.13% |
| DOWNTREND | 0 | +0.00% | +0.00% | +0.00% | +0.00% | +0.00% |
| UNCLASSIFIED | 0 | +0.00% | +0.00% | +0.00% | +0.00% | +0.00% |

## 7. Frozen Interpretation

Phase 3B primarily validated the UPTREND Confirmed execution channel. Emerging has positive forward-return alpha in the prior diagnostic, but it did not execute under Phase 3B priority and capacity rules. SIDEWAYS and DOWNTREND remain unimplemented or untested in portfolio execution.

Recommended next research step: design separate diagnostics for Emerging-only capacity and SIDEWAYS low-exposure rules before changing live execution logic.
