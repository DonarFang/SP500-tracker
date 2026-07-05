# E1 Regime Attribution v1

Status: PRELIMINARY / TRADE_LEVEL_ONLY  
Dataset: CURRENT_CONSTITUENTS_PRELIMINARY  
Strategy: E1_AUDITED_G4_MINHOLD10  
Regime Classifier: Weekly SPX Regime v1.0  
Generated: 2026-06-30T11:25:14

## Scope

This report summarizes trade-level regime attribution only. It does not evaluate continuous portfolio equity, daily drawdown, cash drag, exposure timing, or concentration impact.

Formal regime PASS/FAIL is not allowed at this stage because:

1. The dataset is CURRENT_CONSTITUENTS_PRELIMINARY and may contain survivorship bias.
2. The attribution is trade-level only.
3. SIDEWAYS and DOWNTREND trade samples are insufficient.

## Sample-status rule

| Trade count | sample_status | conclusion_scope |
|---:|---|---|
| N >= 20 | SAMPLE_OK | FORMAL_EVALUATION_ALLOWED |
| 1 <= N < 20 | INSUFFICIENT_TRADE_SAMPLE | OBSERVATIONAL_ONLY |
| N = 0 | NO_TRADES | OBSERVATIONAL_ONLY |

## By entry regime

| Regime | Trades | sample_status | conclusion_scope |
|---|---:|---|---|
| UPTREND | 43 | SAMPLE_OK | FORMAL_EVALUATION_ALLOWED |
| SIDEWAYS | 4 | INSUFFICIENT_TRADE_SAMPLE | OBSERVATIONAL_ONLY |
| DOWNTREND | 0 | NO_TRADES | OBSERVATIONAL_ONLY |

## By dominant regime

| Regime | Trades | sample_status | conclusion_scope |
|---|---:|---|---|
| UPTREND | 45 | SAMPLE_OK | FORMAL_EVALUATION_ALLOWED |
| SIDEWAYS | 2 | INSUFFICIENT_TRADE_SAMPLE | OBSERVATIONAL_ONLY |
| DOWNTREND | 0 | NO_TRADES | OBSERVATIONAL_ONLY |

## Core findings

1. E1 is effectively an UPTREND-entry model. 43/47 trades, or 91.5%, entered during UPTREND.

2. E1 has zero DOWNTREND entries. Defensive behavior is primarily non-participation, not profitable long-side trading during DOWNTREND.

3. SIDEWAYS results are not statistically usable. Entry-regime SIDEWAYS has only 4 trades, and dominant-regime SIDEWAYS has only 2 trades. Both are marked INSUFFICIENT_TRADE_SAMPLE.

4. Trade-level attribution is insufficient to explain total portfolio performance. Trade-level PF may look stronger than portfolio-level PF/Sharpe because it does not fully capture cash drag, exposure timing, concentration, or daily equity path effects.

## Interpretation boundary

Do not conclude that E1 works in SIDEWAYS or DOWNTREND.

Do not use trade-level PF alone as the final measure of regime capability.

Equity-level attribution with continuous daily equity is required before any formal regime PASS/FAIL.

## Next required step

Run Baseline Parity first, then extend the backtest engine to output continuous daily equity. After that, perform regime equity-level attribution by daily return, drawdown, exposure, and cash allocation.
