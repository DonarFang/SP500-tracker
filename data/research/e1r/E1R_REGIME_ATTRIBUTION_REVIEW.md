# E1-R Regime Attribution Review

Status: **DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE**  
Generated: 2026-06-30 19:42:46  
Regime source: `data/research/e1_5y/regimes/spx_regime_daily.json`  
Shared evaluation window: **2023-11-06 → 2026-06-11**  
Shared trading days: **651**

## Fairness controls

- E1 and E1-R are compared on the **same daily dates**.
- E1 and E1-R use the **same UPTREND / SIDEWAYS / DOWNTREND regime map**.
- This report does not judge E1-R by unrelated Period A / Period B slices.
- Portfolio-level attribution uses daily equity changes; trade-level attribution is supplementary only.

## Portfolio-level attribution by regime

| Regime | Days | E1 PnL/Initial | E1-R PnL/Initial | Δ E1-R - E1 | E1 Compound | E1-R Compound | E1 Exp | E1-R Exp | SPX Compound |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UPTREND | 565 | +10.63% | +70.92% | +60.29% | +10.62% | +70.92% | 65.5% | 68.7% | +47.92% |
| SIDEWAYS | 86 | +0.03% | +0.00% | -0.03% | +0.04% | +0.00% | 24.3% | 0.0% | +14.69% |
| DOWNTREND | 0 | +0.00% | +0.00% | +0.00% | +0.00% | +0.00% | 0.0% | 0.0% | +0.00% |
| UNCLASSIFIED | 0 | +0.00% | +0.00% | +0.00% | +0.00% | +0.00% | 0.0% | 0.0% | +0.00% |

## Trade-level supplementary review

| Regime | E1 Trades | E1 AvgRet | E1 WR | E1 SimEnd | E1-R Trades | E1-R AvgRet | E1-R WR | E1-R SimEnd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UPTREND | 0 | +0.00% | 0.0% | 0 | 39 | +4.02% | 38.5% | 2 |
| SIDEWAYS | 0 | +0.00% | 0.0% | 0 | 0 | +0.00% | 0.0% | 0 |
| DOWNTREND | 0 | +0.00% | 0.0% | 0 | 0 | +0.00% | 0.0% | 0 |
| UNCLASSIFIED | 47 | +1.03% | 36.2% | 3 | 0 | +0.00% | 0.0% | 0 |

## Entry type counts

E1: `{'LEGACY_E1_ENTRY': 47}`  
E1-R: `{'E1R_UPTREND_CONFIRMED': 39}`

## Interpretation guardrail

This report is designed to answer whether E1-R improves performance under the same market-condition segmentation as E1.  
A valid conclusion should be stated by regime, for example: UPTREND improved / SIDEWAYS reduced damage / DOWNTREND stayed defensive.  
Do not use mismatched time slices as the primary comparison basis.
