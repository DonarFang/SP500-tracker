# FD-M3180125 — AE-step 1 CAPPED-ATR Migration Record

```text
STATUS: PASS
OFFICIAL_STEP: AE-step 1
ENGINE_ID: FD-M3180125-SP500-TOP3-engine
VARIANT_ID: E1R_CAPPED_ATR_A0_V1
DISPLAY_NAME: E1R CAPPED-ATR Engine
GENERATED_AT: 2026-08-09T08:50:02.021776+00:00
SOURCE_COMMIT: ae3038cd5bf34a38ba0b3ac82f12f8c195082d98
```

## Promoted stop contract

```text
A0 = first BUY cost-adjusted execution price
ATR20 = simple mean of the last 20 complete True Range observations as of first-entry signal day T EOD
distance = clip(3 * ATR20, 12% * A0, 20% * A0)
trigger = A0 - distance
signal = T close <= trigger
execution = T+1 original adverse low fill
A0 / ATR20 / distance / trigger remain frozen for the position cycle
ADD does not update stop state
regime change does not reset stop state
full exit clears stop state
same-symbol re-entry on stop execution day remains allowed
```

## Accepted Canonical 5Y metrics

```json
{
  "final_equity": 312687.26,
  "total_return_pct": 212.69,
  "cagr_pct": 25.59,
  "max_drawdown_pct": 25.66,
  "sharpe_ratio": 0.76,
  "profit_factor": 2.36,
  "number_of_trades": 92,
  "exposure_pct": 69.2
}
```

## Integrity

```text
Canonical result SHA256: 9720084b92ed7e7ae80eaf606a170239312e333f4e5daca7d284835afc6ffcd3
Official manifest SHA256: 3e05ce395ce9d7e99f3728165c48ec8536218c140e39ebdaf70f7853faa437d7
CAPPED-ATR trigger rows: 8
Executed HARD_LOSS_STOP exits: 3
```

## Scope boundary

```text
Forward changed: false
Live changed: false
Workflow changed: false
Dashboard changed: false
Next official step: AE-step 2 (not started by AE-step 1)
```
