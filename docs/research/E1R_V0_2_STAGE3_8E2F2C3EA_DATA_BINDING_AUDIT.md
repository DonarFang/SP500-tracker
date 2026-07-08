# Stage 3.8E-2F-2C-3E-A DATA Binding Audit

Generated At: `2026-07-08T09:17:35.951569+00:00`

## Status

- Status: `AUDIT_COMPLETE_NO_SOURCE_CHANGES`
- Dashboard changed: `False`
- Exports changed: `False`
- State changed: `False`
- Workflow changed: `False`

## Local Data Validation

- orders_rows: `10`
- positions_rows: `10`
- buy_orders: `10`
- symbols: `AXON, DD, DVA, MRNA, HUM, HOOD, FTNT, GEN, SNOW, MOH`

## Static App Audit

- orders_path_present: `True`
- positions_path_present: `True`
- resolver_block_found: `True`
- resolver_mentions_orders_alias: `True`
- resolver_mentions_positions_alias: `True`

## Orders Path Lines

- L1407: `orders: "../exports/oos_e1r_v0_2_orders.json",`

## Positions Path Lines

- L1406: `positions: "../exports/oos_e1r_v0_2_positions.json",`

## Trade Log Calls

- L515: `function e1rForwardTradeLogHtml(ordersRaw, positionsRaw) {`
- L1218: `h+=`<div class="card" style="margin-bottom:1rem"><div class="card-head">${e1rForwardTradeLogHtml(e1rForwardOrdersData(), e1rForwardPositionsData())}`

## DATA Keys Containing E1R

- `e1rConfirmed`
- `e1rFormal`
- `e1rForwardOrders`
- `e1rForwardPositions`
- `e1rRegime`
- `e1rSideways3i`
- `e1rSideways3ir`
- `e1rSideways3k`
- `e1rV02BacktestSummary`
- `e1rV02OosEquityCurve`
- `e1rV02OosOrders`
- `e1rV02OosPositions`
- `e1rV02OosSummary`
- `e1rV02Orders`
- `e1rV02Positions`
- `oosE1rV02Orders`
- `oosE1rV02Positions`
- `oos_e1r_v0_2_orders`
- `oos_e1r_v0_2_positions`

## Diagnosis

- No static diagnosis yet; inspect JSON context.

