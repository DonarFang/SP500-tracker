# E1-R Phase 3F SIDEWAYS Rule Diagnostic

Status: **DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE**

## 1. Purpose

Evaluate whether SIDEWAYS should remain cash/near-zero exposure, or whether a future low-exposure high-quality SIDEWAYS rule deserves paper testing. This diagnostic does not change trading logic.

## 2. Portfolio Context

| Strategy | Return | MaxDD | PF | Trades |
|---|---:|---:|---:|---:|
| E1 | +7.52% | +38.10% | 1.25 | 47 |
| E1-R | +65.71% | +32.35% | 1.97 | 39 |

## 3. SIDEWAYS Regime Review Delta

| Days | E1R-E1 PnL | Compound | Exposure Delta | MaxDD Delta |
|---:|---:|---:|---:|---:|
| 86 | -0.03% | -0.04% | -24.34% | -5.13% |

## 4. SIDEWAYS Candidate Rules

Strict proxy follows the v0.1 spec: RS>=92, rank<=5, LS>=80, TH>=75, Momentum>=75, close>MA50, MA50 slope>=0, 20D pullback within 8%, MA50 distance <=12%, and no volatility expansion proxy.

| Rule | Raw | Days | Dedup Top1 | 20D Avg | 20D Excess | 20D Excess WR | 30D Avg | 30D Excess |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SIDEWAYS_RELAXED_NO_VOL_FILTER | 130 | 47 | 30 | +0.40% | -4.62% | 20.0% | +0.89% | -7.11% |
| SIDEWAYS_STRICT_SPEC_PROXY | 84 | 34 | 20 | +0.22% | -2.62% | 30.0% | +1.95% | -4.50% |
| SIDEWAYS_ULTRA_STRICT_TOP3 | 44 | 24 | 13 | +0.73% | -0.47% | 38.5% | +2.42% | -1.85% |

## 5. Decision

Decision: **SIDEWAYS_WATCHLIST_ONLY_FOR_NOW**

Reason: Strict SIDEWAYS proxy produced candidates, but evidence is not strong enough for execution-layer approval.

Execution layer change approved: **False**

## 6. Next Step

Keep SIDEWAYS as diagnostic-only unless a future paper-test design shows sufficient positive excess return under strict low-exposure rules.
