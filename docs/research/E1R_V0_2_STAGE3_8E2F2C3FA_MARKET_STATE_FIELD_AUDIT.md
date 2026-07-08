# Stage 3.8E-2F-2C-3F-A Market State Field Audit

Generated At: `2026-07-08T09:48:52.285481+00:00`

## Status

- Status: `AUDIT_COMPLETE_NO_SOURCE_CHANGES`
- Dashboard changed: `False`
- Exports changed: `False`
- State changed: `False`
- Workflow changed: `False`

## Field Candidates

- Trend State: `None = None`
- Risk Mode: `state = Risk-On`
- Data Date: `date = 2026-07-07`
- Market Score: `market_score = 60.0`
- Leadership: `None = None`
- Subclass: `None = None`

## Diagnosis

- Current displayed State likely maps to risk mode, not trend regime.
- No obvious trend regime field found directly in market object; inspect generator/source hits.
- Risk mode field candidate found: state=Risk-On

## Market Keys

- `advance_count`
- `advance_decline`
- `date`
- `decline_count`
- `indices`
- `leadership_confirmed`
- `leadership_label`
- `market_score`
- `ndx_score`
- `notes`
- `pct_above_ma50`
- `score_breakdown`
- `sox_score`
- `spx_close`
- `spx_ma200`
- `spx_ma50`
- `spx_score`
- `spx_slope20`
- `state`
- `state_color`
- `state_icon`
- `state_zh`
- `vix_color`
- `vix_score`
- `vix_state`

## Recommended UI

- `Trend State: UPTREND / SIDEWAYS / DOWNTREND`
- `Risk Mode: Risk-On / Cautious / Risk-Off`
- `Data date`
- `Market score`
- `Leadership`

