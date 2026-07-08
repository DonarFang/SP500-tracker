# Stage 3.8E-2F-1E-1 E1R Target Source Contract

Generated At: `2026-07-08T06:59:01.254448+00:00`
HEAD: `f72f9ac`

## Status

- Status: `CONTRACT_SELECTED_NO_SOURCE_CHANGES`
- Source changed: `False`
- Exports changed: `False`
- State changed: `False`
- Dashboard changed: `False`
- Strategy logic changed: `False`

## Selected Contract

- Core target source: `exports/leaderboard.json`
- Core method: Use current leaderboard rows as core target candidates.
- Sidecar target source: `exports/oos_e1r_v0_2_sidecar.json`
- Sidecar has symbol-level targets in current export: `True`
- Sidecar method: Use exported sidecar selected symbols if present.
- Status source: `exports/e1r_v0_2_status.json`
- Orders rule: orders = diff(previous E1R positions, new symbol-level target weights)
- Implementation decision: `READY_FOR_CORE_AND_SIDECAR_TARGET_EXTRACTION`

## Candidate Summary

- status candidates: `1`
- sidecar candidates: `1`
- leaderboard candidates: `11`
- has leaderboard rows: `True`
- has sidecar symbol targets: `True`
- has status symbol targets: `True`

## Candidate Details

### Status
- path `$.sidecar` symbol_keys=`[]` list_symbol_keys=`['selected']` weight_keys=`['gross_exposure']` row_count=`None` sample_keys=`None`

### Sidecar
- path `$` symbol_keys=`[]` list_symbol_keys=`['selected']` weight_keys=`['gross_exposure']` row_count=`None` sample_keys=`None`

### Leaderboard
- path `$.leaders` symbol_keys=`['symbol']` list_symbol_keys=`None` weight_keys=`[]` row_count=`10` sample_keys=`['trend_state', 'ma50_slope_pct', 'ma50', 'ma20', 'ma50_slope_score', 'name', 'action_description', 'ma50_slope', 'symbol', 'drawdown_score', 'ret20_pct', 'rs_score', 'rank', 'volatility_pct', 'slope20', 'ret60_pct', 'ret20', 'rs_raw', 'above_ma20', 'sector', 'action_color', 'ma200', 'market_score', 'price', 'volatility_score', 'slope5', 'price_structure_score', 'ret60', 'drawdown_pct', 'momentum_score', 'above_ma50', 'action_label', 'above_ma200', 'leader_score', 'trend_health', 'ma20_slope', 'trade_action', 'slope10']`
- path `$.leaders[0]` symbol_keys=`['symbol']` list_symbol_keys=`[]` weight_keys=`[]` row_count=`None` sample_keys=`None`
- path `$.leaders[1]` symbol_keys=`['symbol']` list_symbol_keys=`[]` weight_keys=`[]` row_count=`None` sample_keys=`None`
- path `$.leaders[2]` symbol_keys=`['symbol']` list_symbol_keys=`[]` weight_keys=`[]` row_count=`None` sample_keys=`None`
- path `$.leaders[3]` symbol_keys=`['symbol']` list_symbol_keys=`[]` weight_keys=`[]` row_count=`None` sample_keys=`None`
- path `$.leaders[4]` symbol_keys=`['symbol']` list_symbol_keys=`[]` weight_keys=`[]` row_count=`None` sample_keys=`None`
- path `$.leaders[5]` symbol_keys=`['symbol']` list_symbol_keys=`[]` weight_keys=`[]` row_count=`None` sample_keys=`None`
- path `$.leaders[6]` symbol_keys=`['symbol']` list_symbol_keys=`[]` weight_keys=`[]` row_count=`None` sample_keys=`None`
- path `$.leaders[7]` symbol_keys=`['symbol']` list_symbol_keys=`[]` weight_keys=`[]` row_count=`None` sample_keys=`None`
- path `$.leaders[8]` symbol_keys=`['symbol']` list_symbol_keys=`[]` weight_keys=`[]` row_count=`None` sample_keys=`None`
- path `$.leaders[9]` symbol_keys=`['symbol']` list_symbol_keys=`[]` weight_keys=`[]` row_count=`None` sample_keys=`None`

## Guardrails

- Do not infer symbol-level orders from gross_exposure alone.
- Do not touch E1 state/export.
- Do not modify frozen E1R strategy logic.

## Next

- Stage 3.8E-2F-1E-2: implement target extraction according to this contract.

