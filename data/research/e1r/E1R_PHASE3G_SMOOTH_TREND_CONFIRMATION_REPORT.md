# E1-R Phase 3G Smooth Trend Confirmation Diagnostic

Generated: `2026-07-01 20:58:10`

Status: **DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE**

## 1. Question

Should SIDEWAYS / DOWNTREND strong stocks be evaluated by smoothing first, then selecting persistent leaders, rather than buying single-day strength?

A. **STC Screen** = smooth first, then find strong stocks. This is the only branch that can later be considered for execution-layer research.

B. **Watchlist Funnel** = find single-day strong stocks first, then validate whether they later pass STC. This is Watchlist / radar only.

## 2. STC Screen Results

| Rule | Raw | Days | Dedup Top1 | 20D Avg | 20D Excess | 20D Excess WR | 30D Avg | 30D Excess | 30D Excess WR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SIDEWAYS_STC80 | 962 | 96 | 44 | +2.48% | -2.50% | 40.9% | +5.21% | -2.06% | 38.6% |
| SIDEWAYS_STC85 | 782 | 96 | 44 | +2.48% | -2.50% | 40.9% | +5.21% | -2.06% | 38.6% |
| SIDEWAYS_STC90 | 609 | 96 | 44 | +2.48% | -2.50% | 40.9% | +5.21% | -2.06% | 38.6% |
| DOWNTREND_STC90 | 0 | 0 | 0 | n/a | n/a | None% | n/a | n/a | None% |

## 3. Watchlist Funnel

Raw single-day watchlist candidates, dedup: **500**

STC confirmations within 30D, dedup: **230**

Confirmation rates: 10D=65.0%, 20D=70.0%, 30D=72.0%

Forward from confirmation date: 20D excess **-1.81%**, 30D excess **-1.60%**.

## 4. Phase 3F Single-Day Baseline

| Phase 3F Rule | Dedup Top1 | 20D Excess | 30D Excess |
|---|---:|---:|---:|
| SIDEWAYS_RELAXED_NO_VOL_FILTER | 30 | -4.62% | -7.11% |
| SIDEWAYS_STRICT_SPEC_PROXY | 20 | -2.62% | -4.50% |
| SIDEWAYS_ULTRA_STRICT_TOP3 | 13 | -0.47% | -1.85% |

## 5. Decision

Decision: **SIDEWAYS_DOWNTREND_STC_WATCHLIST_ONLY_FOR_NOW**

Reason: Smooth Trend Confirmation does not yet provide sufficient execution-layer evidence. Use as Watchlist/radar only.

## 6. Frozen Interpretation

This diagnostic separates trading evidence from watchlist evidence. Future execution approval can only be based on the STC Screen branch, because it uses smoothed information already available as of the signal date. The Watchlist Funnel is useful for early radar and upgrade observation, but not as a buy signal.
