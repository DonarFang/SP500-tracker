# E1-R Phase 3I — SIDEWAYS Candidate Quality Decomposition Diagnostic

Generated: `2026-07-02T17:51:03`

## Status

Diagnostic only. No trading logic, UPTREND Confirmed execution, orders, or benchmark rules are changed.

## Candidate Universe

- Base STC candidates: `962`
- Candidates with volume data: `962`
- Proxy/index candidates: `3`
- Sector map symbols: `0`
- CLV available rows: `962`
- Subregime counts: `{'SIDEWAYS_DETERIORATION': 395, 'SIDEWAYS_RANGE': 149, 'SIDEWAYS_RECOVERY': 418}`
- Strength type counts: `{'DETERIORATION_HOLDOUT': 301, 'EVENT_OR_FAILED_FLOW_RISK': 119, 'EXCLUDED_PROXY_OR_INDEX': 3, 'RANGE_ROTATION': 139, 'UNCLASSIFIED_STRENGTH': 295, 'RECOVERY_LEADER_CANDIDATE': 105}`

## Quality Rule Results

| Rule | Raw | Days | Dedup Top1 | 20D Avg | 20D Excess | 20D Excess WR | 30D Avg | 30D Excess | Upgrade30 | Fail20 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BASE_STC_COMMON_EQUITY | 959 | 96 | 43 | +3.47% | -1.39% | +41.90% | +6.27% | -0.91% | +13.95% | +39.53% |
| UPGRADE_WATCH_RELAXED | 198 | 72 | 37 | +4.34% | -0.54% | +37.80% | +7.21% | +0.05% | +13.51% | +27.03% |
| UPGRADE_WATCH_RECOVERY | 98 | 35 | 20 | +8.01% | +3.90% | +50.00% | +13.87% | +8.10% | +25.00% | +10.00% |
| UPGRADE_WATCH_SECTOR_CONFIRMED | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| DEFENSIVE_STRENGTH | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| RANGE_ROTATION_PROXY | 149 | 18 | 14 | +3.88% | -0.39% | +35.70% | +3.50% | -3.36% | +14.29% | +35.71% |
| FAILED_FLOW_RISK | 119 | 53 | 37 | +1.15% | -5.07% | +29.70% | +2.17% | -6.60% | +10.81% | +59.46% |

## By SIDEWAYS Subregime

| Subregime | Dedup Top1 | 20D Excess | 30D Excess | Upgrade30 |
|---|---:|---:|---:|---:|
| SIDEWAYS_DETERIORATION | 20 | -6.70% | -7.60% | +0.00% |
| SIDEWAYS_RANGE | 14 | -0.39% | -3.36% | +14.29% |
| SIDEWAYS_RECOVERY | 16 | +5.36% | +8.95% | +31.25% |

## By Strength Type

| Strength Type | Dedup Top1 | 20D Excess | 30D Excess | Upgrade30 |
|---|---:|---:|---:|---:|
| DETERIORATION_HOLDOUT | 21 | -6.94% | -8.60% | +0.00% |
| EVENT_OR_FAILED_FLOW_RISK | 37 | -5.07% | -6.60% | +10.81% |
| EXCLUDED_PROXY_OR_INDEX | 0 | n/a | n/a | n/a |
| RANGE_ROTATION | 14 | -0.39% | -3.36% | +14.29% |
| RECOVERY_LEADER_CANDIDATE | 20 | +3.60% | +7.42% | +25.00% |
| UNCLASSIFIED_STRENGTH | 16 | +6.92% | +10.35% | +31.25% |

## Decision

- Decision: `SIDEWAYS_QUALITY_SEGMENT_PROMISING_DIAGNOSTIC_ONLY`
- Best rule: `UPGRADE_WATCH_RECOVERY`
- Reason: A SIDEWAYS quality segment met positive 20D/30D excess and sample thresholds. Still diagnostic only; execution would require separate portfolio simulation and UPTREND protection tests.

## Interpretation

Phase 3I is designed for Watchlist/Tier improvement only. A promising segment does not authorize SIDEWAYS execution. Any future execution test must be a separate portfolio simulation and must preserve UPTREND Confirmed results.
