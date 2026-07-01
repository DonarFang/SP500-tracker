# E1-R Phase 3E Confirmed Quality Diagnostic

Status: **DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE**

## 1. Purpose

This diagnostic stress-tests whether E1-R Confirmed winners are a healthy trend-following payoff pattern or an overly fragile concentration. It does not change trading logic.

## 2. Portfolio Baseline

| Strategy | Return | MaxDD | PF | Sharpe | Win Rate | Exposure | Trades |
|---|---:|---:|---:|---:|---:|---:|---:|
| E1_AUDITED_G4_MINHOLD10 | +7.52% | +38.10% | 1.25 | 0.18 | +36.20% | +80.10% | 47 |
| E1R_REGIME_AWARE_V0_1 | +65.71% | +32.35% | 1.97 | 0.58 | +38.50% | +74.90% | 39 |

## 3. Confirmed Trade Stress Tests

These tests remove the largest winning trades from the trade-return distribution. They are not recomputed portfolio equity curves.

| Case | Trades | SIM_END | Sum Return Pts | Avg | Median | Win Rate | PF by Trade Return | Best | Worst |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| all_trades | 39 | 2 | +156.73% | +4.02% | -2.31% | +38.46% | 1.97 | +60.46% | -16.45% |
| closed_only_ex_sim_end | 37 | 0 | +58.70% | +1.59% | -2.47% | +35.14% | 1.36 | +45.59% | -16.45% |
| exclude_top1_all | 38 | 1 | +96.27% | +2.53% | -2.39% | +36.84% | 1.6 | +45.59% | -16.45% |
| exclude_top2_all | 37 | 1 | +50.68% | +1.37% | -2.47% | +35.14% | 1.31 | +39.92% | -16.45% |
| exclude_top3_all | 36 | 1 | +10.76% | +0.30% | -2.74% | +33.33% | 1.07 | +37.57% | -16.45% |
| exclude_top1_closed_only | 36 | 0 | +13.11% | +0.36% | -2.74% | +33.33% | 1.08 | +39.92% | -16.45% |
| exclude_top2_closed_only | 35 | 0 | -26.81% | -0.77% | -3.01% | +31.43% | 0.83 | +30.90% | -16.45% |
| exclude_top3_closed_only | 34 | 0 | -57.71% | -1.70% | -3.17% | +29.41% | 0.64 | +25.97% | -16.45% |

## 4. Top Winners and Worst Losers

### Top Winners

| Symbol | Entry | Exit | Return | Days | SIM_END | Entry Regime | Max Gain | Max DD in Trade |
|---|---|---|---:|---:|---|---|---:|---:|
| MRVL | 2026-04-23 | 2026-06-11 | +60.46% | 35 | True | UPTREND | +88.32% | +0.00% |
| WDC | 2025-08-05 | 2025-10-15 | +45.59% | 51 | False | UPTREND | +67.47% | +43.88% |
| SNDK | 2025-10-16 | 2025-11-21 | +39.92% | 27 | False | UPTREND | +89.70% | +50.49% |
| DELL | 2026-04-24 | 2026-06-11 | +37.57% | 34 | True | UPTREND | +112.55% | +0.00% |
| GEV | 2024-09-20 | 2024-12-19 | +30.90% | 64 | False | UPTREND | +39.17% | +30.04% |
| COIN | 2023-11-24 | 2024-01-05 | +25.97% | 29 | False | UPTREND | +59.20% | +41.38% |
| STX | 2025-07-01 | 2025-10-13 | +20.41% | 73 | False | UPTREND | +67.63% | +44.88% |
| W | 2025-07-03 | 2025-10-10 | +18.27% | 70 | False | UPTREND | +28.97% | +40.81% |
| TPR | 2025-01-07 | 2025-03-07 | +13.53% | 41 | False | UPTREND | +28.99% | +25.17% |
| FICO | 2024-09-13 | 2024-12-10 | +9.08% | 62 | False | UPTREND | +26.18% | +21.84% |

### Worst Losers

| Symbol | Entry | Exit | Return | Days | SIM_END | Entry Regime | Max Gain | Max DD in Trade |
|---|---|---|---:|---:|---|---|---:|---:|
| TSLA | 2024-12-16 | 2025-01-02 | -16.45% | 12 | False | UPTREND | +3.50% | +15.84% |
| ANET | 2025-10-13 | 2025-11-06 | -16.03% | 19 | False | UPTREND | -0.09% | +14.34% |
| ALAB | 2024-12-24 | 2025-01-14 | -13.74% | 13 | False | UPTREND | +1.06% | +12.77% |
| ATI | 2026-02-26 | 2026-03-16 | -13.13% | 13 | False | UPTREND | +1.63% | +14.69% |
| AVGO | 2024-06-18 | 2024-07-18 | -12.52% | 21 | False | UPTREND | -1.19% | +14.45% |
| AMAT | 2026-01-22 | 2026-02-05 | -12.40% | 11 | False | UPTREND | +2.39% | +12.81% |
| TRGP | 2025-01-21 | 2025-02-24 | -9.35% | 24 | False | UPTREND | -0.16% | +9.07% |
| EQT | 2025-01-16 | 2025-02-26 | -8.45% | 28 | False | UPTREND | +0.49% | +10.91% |
| REGN | 2025-11-28 | 2026-01-20 | -8.15% | 35 | False | UPTREND | +2.14% | +14.73% |
| GDDY | 2024-08-16 | 2024-09-05 | -6.24% | 14 | False | UPTREND | +1.82% | +6.05% |

## 5. Concentration

Top1 share of gross profit: **+19.01%**
Top2 share of gross profit: **+33.35%**
Top3 share of gross profit: **+45.90%**

Symbol concentration: `{'GDDY': 2, 'AMAT': 2, 'MELI': 1, 'COIN': 1, 'ALL': 1, 'C': 1, 'GE': 1, 'DAL': 1, 'AVGO': 1, 'GRMN': 1, 'AAPL': 1, 'EXR': 1, 'AXON': 1, 'FICO': 1, 'GEV': 1, 'TSLA': 1, 'BKNG': 1, 'ALAB': 1, 'TRGP': 1, 'EQT': 1, 'TPR': 1, 'RCL': 1, 'W': 1, 'STX': 1, 'WDC': 1, 'ANET': 1, 'BE': 1, 'SNDK': 1, 'BIIB': 1, 'REGN': 1, 'LLY': 1, 'NEM': 1, 'FCX': 1, 'ATI': 1, 'EQIX': 1, 'MRVL': 1, 'DELL': 1}`

Sector concentration: `{'UNKNOWN': 39}`

Entry-month concentration: `{'2023-11': 3, '2025-01': 3, '2025-07': 3, '2025-10': 3, '2025-11': 3, '2026-01': 3, '2026-04': 3, '2024-01': 2, '2024-05': 2, '2024-06': 2, '2024-09': 2, '2024-12': 2, '2024-02': 1, '2024-03': 1, '2024-08': 1, '2024-07': 1, '2024-10': 1, '2024-11': 1, '2025-08': 1, '2026-02': 1}`

## 6. Regime Delta Reference

| Regime | Days | E1R-E1 PnL | Compound | Exposure Delta | MaxDD Delta |
|---|---:|---:|---:|---:|---:|
| UPTREND | 565 | +60.29% | +60.30% | +3.21% | -4.91% |
| SIDEWAYS | 86 | -0.03% | -0.04% | -24.34% | -5.13% |
| DOWNTREND | 0 | +0.00% | +0.00% | +0.00% | +0.00% |
| UNCLASSIFIED | 0 | +0.00% | +0.00% | +0.00% | +0.00% |

## 7. Frozen Interpretation

Heuristic grade: **A**

Top-winner dependence appears healthy under trade-level stress tests.

This is a pressure test, not a penalty test. Trend systems are allowed to rely on major winners; the diagnostic checks whether the Confirmed channel still has a reasonable base after removing the largest winners and SIM_END trades.
