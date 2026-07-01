# E1-R Phase 3D Emerging Channel Diagnostic

Generated: `2026-07-01 19:04:38`

Status: **DIAGNOSTIC_ONLY_NO_TRADING_LOGIC_CHANGE**

## 1. Purpose

Evaluate whether Emerging deserves a future separate 0.5-slot channel if it does not have to compete with Confirmed under the current Phase 3B Top-1 priority rule.

## 2. Phase 3C Baseline

Candidate type counts: `{'E1R_UPTREND_EMERGING': 2893, 'E1R_UPTREND_CONFIRMED': 2671}`

Top-1 type counts under Phase 3B priority: `{'E1R_UPTREND_CONFIRMED': 561, 'E1R_UPTREND_EMERGING': 1}`

Executed trade type counts: `{'E1R_UPTREND_CONFIRMED': 39}`

## 3. Emerging Funnel

Raw Emerging candidates: **2893**
Emerging candidate days: **548**
Emerging-only daily Top1 days: **548**
Emerging-only Top1 dedup count: **402**
Capacity proxy days: **155**
Capacity proxy dedup count: **123**

Proxy block reasons: `{'confirmed_exists_same_day': 547, 'phase3b_top1_is_confirmed': 547, 'no_capacity_proxy': 393, 'already_holding_symbol_proxy': 4}`

## 4. Forward Return Summary

### Emerging All Dedup

Count: **1409**

| Horizon | Avg | Excess | Win Rate | Excess WR | N |
|---|---:|---:|---:|---:|---:|
| 5D | +0.71% | +0.49% | 53.8% | 51.0% | 1409 |
| 10D | +1.09% | +0.57% | 55.4% | 50.8% | 1398 |
| 20D | +2.20% | +1.14% | 55.6% | 50.3% | 1375 |
| 30D | +2.57% | +0.90% | 58.4% | 49.2% | 1350 |

Unique symbols: **409**; Top-10 share: **7.2%**
Top symbols: `[('DDOG', 11), ('C', 11), ('AVGO', 10), ('DASH', 10), ('EXPE', 10), ('MPWR', 10), ('ISRG', 10), ('LLY', 10), ('KLAC', 10), ('DAL', 10)]`

### Emerging-only Daily Top1 Dedup

Count: **402**

| Horizon | Avg | Excess | Win Rate | Excess WR | N |
|---|---:|---:|---:|---:|---:|
| 5D | +0.85% | +0.55% | 55.2% | 52.2% | 402 |
| 10D | +1.33% | +0.78% | 53.9% | 48.1% | 397 |
| 20D | +2.05% | +1.04% | 52.6% | 49.2% | 392 |
| 30D | +1.90% | +0.36% | 56.1% | 46.0% | 385 |

Unique symbols: **234**; Top-10 share: **10.9%**
Top symbols: `[('DASH', 5), ('MPWR', 5), ('MRVL', 5), ('DDOG', 5), ('DECK', 4), ('CCI', 4), ('ETSY', 4), ('DHI', 4), ('BAX', 4), ('ISRG', 4)]`

### Emerging Capacity Proxy Dedup

Count: **123**

| Horizon | Avg | Excess | Win Rate | Excess WR | N |
|---|---:|---:|---:|---:|---:|
| 5D | +0.84% | +0.41% | 54.5% | 53.7% | 123 |
| 10D | +1.31% | +0.46% | 62.8% | 45.5% | 121 |
| 20D | +1.23% | -0.25% | 52.9% | 47.9% | 121 |
| 30D | +2.22% | +0.36% | 57.9% | 50.4% | 121 |

Unique symbols: **103**; Top-10 share: **18.7%**
Top symbols: `[('CCI', 3), ('WELL', 3), ('BAX', 3), ('MELI', 2), ('CAH', 2), ('CEG', 2), ('DAL', 2), ('BSX', 2), ('MAA', 2), ('FOXA', 2)]`

## 5. Upgrade Path

| Sample | 5D Upgrade | 10D Upgrade | 20D Upgrade | 30D Upgrade | Avg Gap | Median Gap |
|---|---:|---:|---:|---:|---:|---:|
| emerging_all_dedup | 26.5% | 31.6% | 37.0% | 41.6% | 4.61 | 3 |
| emerging_only_daily_top1_dedup | 42.8% | 47.0% | 53.0% | 56.7% | 3.42 | 1.0 |

## 6. Interpretation Guardrails

- This is not an execution backtest.
- Capacity proxy is approximate and does not replay cash, fills, partial sizing, or same-day order priority.
- A future Phase 3E execution test should be allowed only if Emerging Top1 shows positive excess return with reasonable concentration and upgrade behavior.
