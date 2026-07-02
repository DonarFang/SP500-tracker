# E1-R Phase 3H Market Flow Confirmation Diagnostic

Generated: `2026-07-02 16:59:48`

Status: **DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE**

## 1. Question

For SIDEWAYS / DOWNTREND smooth-trend candidates, does market trading money confirmation improve 20D / 30D excess return versus SPX?

This phase does not touch the existing UPTREND Confirmed execution path.

## 2. Market Flow Score v0.1

| Component | Weight |
|---|---:|
| relative_volume_participation | 25 |
| up_day_volume_confirmation | 25 |
| dollar_volume_liquidity | 15 |
| price_volume_confirmation | 15 |
| setup_quality_dryup_compression_52w_proximity | 20 |

## 3. Rule Results

| Rule | Raw | Days | Dedup Top1 | 20D Avg | 20D Excess | 20D Excess WR | 30D Avg | 30D Excess | 30D Excess WR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| STC_ONLY_WITH_VOLUME_DATA | 962 | 96 | 44 | +2.48% | -2.50% | 40.9% | +5.21% | -2.06% | 38.6% |
| STC_PLUS_RELATIVE_VOLUME | 415 | 96 | 43 | +1.81% | -3.24% | 32.6% | +3.93% | -3.29% | 34.9% |
| STC_PLUS_UP_VOLUME | 691 | 93 | 38 | +2.79% | -2.09% | 42.1% | +5.00% | -2.17% | 42.1% |
| STC_PLUS_DOLLAR_VOLUME_100M | 950 | 96 | 42 | +3.43% | -1.36% | 42.9% | +6.37% | -0.71% | 42.9% |
| STC_PLUS_RVOL_AND_UPVOL | 299 | 92 | 40 | +2.99% | -2.05% | 37.5% | +4.93% | -2.15% | 40.0% |
| STC_PLUS_PRICE_VOLUME | 706 | 94 | 39 | +2.63% | -2.29% | 38.5% | +4.92% | -2.38% | 38.5% |
| STC_PLUS_FLOW_SCORE_60 | 653 | 96 | 38 | +3.17% | -1.62% | 44.7% | +6.20% | -0.94% | 42.1% |
| STC_PLUS_FLOW_SCORE_70 | 315 | 85 | 40 | +3.81% | -0.68% | 37.5% | +6.58% | -0.14% | 42.5% |
| STC_PLUS_FLOW_SCORE_60_AND_LIQUID | 649 | 96 | 37 | +3.13% | -1.57% | 45.9% | +6.15% | -0.85% | 43.2% |

## 4. By-Regime Check

| Regime | Rule | Dedup Top1 | 20D Excess | 30D Excess |
|---|---|---:|---:|---:|
| SIDEWAYS | STC_ONLY_WITH_VOLUME_DATA | 44 | -2.50% | -2.06% |
| SIDEWAYS | STC_PLUS_FLOW_SCORE_60 | 38 | -1.62% | -0.94% |
| SIDEWAYS | STC_PLUS_FLOW_SCORE_70 | 40 | -0.68% | -0.14% |
| SIDEWAYS | STC_PLUS_RVOL_AND_UPVOL | 40 | -2.05% | -2.15% |
| DOWNTREND | STC_ONLY_WITH_VOLUME_DATA | 0 | n/a | n/a |
| DOWNTREND | STC_PLUS_FLOW_SCORE_60 | 0 | n/a | n/a |
| DOWNTREND | STC_PLUS_FLOW_SCORE_70 | 0 | n/a | n/a |
| DOWNTREND | STC_PLUS_RVOL_AND_UPVOL | 0 | n/a | n/a |

## 5. Decision

Decision: **MARKET_FLOW_WATCHLIST_ONLY_FOR_NOW**

Best rule: `STC_PLUS_FLOW_SCORE_70`

Reason: Market-flow filters did not provide sufficient positive 20D/30D excess evidence versus SPX. Keep SIDEWAYS/DOWNTREND candidates as Watchlist/radar only.

## 6. Frozen Interpretation

Market-flow confirmation is evaluated only as a non-UPTREND diagnostic overlay. It must not be applied to UPTREND Confirmed execution without a separate Phase 4 comparison that proves it protects the current UPTREND edge.
