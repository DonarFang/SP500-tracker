# Stage 3.8E-2F-1B E1R Forward Implementation Plan

Generated At: `2026-07-08T06:41:50.180348+00:00`
HEAD: `4ba7133`

## Status

- Status: `PLAN_COMPLETE_NO_ENGINE_CHANGES`
- Source changed: `False`
- Dashboard changed: `False`
- Exports changed: `False`
- Strategy logic changed: `False`

## Decision

- Reuse E1 accounting primitives: `True`
- Share E1 state file: `False`
- Official E1R runner: `scripts/run_e1r_v0_2_oos.py`
- Dedicated E1R state namespace: `True`
- Dashboard after export: `True`

Reuse E1 OOS accounting/export primitives through an E1R-specific runner and E1R-specific state/export namespace.

## Kickoff Policy

- E1 forward start date: `2026-06-18`
- E1R official kickoff policy: `first trading day after Stage 3.8E-2F implementation is merged and daily update runner succeeds`
- Backfill policy: `allowed only as BACKFILL/SHADOW diagnostics; not counted as official E1R forward test`
- Summary kickoff field: `official_kickoff_date`

## Proposed Files To Add

- `data/oos/e1r_v0_2_portfolio_state.json`
- `data/oos/e1r_v0_2_events.jsonl`
- `data/oos/e1r_v0_2_run_history.jsonl`

## Proposed Files To Modify

- `scripts/run_e1r_v0_2_oos.py` — Make this the official E1R v0.2 forward runner. Generate daily target/actions, update E1R-only state, and write performance exports. Risk: `medium`
- `scripts/run_e1r_v0_2_oos_equity.py` — Either fold into official runner or make it a helper for E1R daily mark-to-market. Avoid duplicate accounting ownership. Risk: `medium`
- `src/oos/portfolio_state.py` — Reuse or lightly generalize portfolio state primitives only if needed. No E1 behavior change. Risk: `medium`
- `src/oos/tracking_engine.py` — Reuse accounting primitives if already parameterizable. Prefer wrapper over changing E1 behavior. Risk: `medium-high`
- `src/oos/exporter.py` — Reuse exporter primitives or add E1R namespace export helpers. Risk: `medium`
- `.github/workflows/update.yml` — After local smoke validation, add E1R forward runner to daily update pipeline. Risk: `medium`
- `dashboard/app.js` — Only after exports contain real forward performance fields, map summary/equity fields to UI. Risk: `low-medium`

## Files Not To Modify During Kickoff

- `src/engine/backtest.py` — Historical E1/E1R backtest rules are frozen. Do not change strategy research logic during forward kickoff.
- `src/engine/e1r_composer.py` — Frozen candidate composition logic should not be tuned. Only call it as a signal/target generator if needed.
- `src/engine/e1r_sidecar_sleeve.py` — Frozen sidecar rule logic should not be changed for kickoff. Only consume output/state.
- `exports/e1r_v0_2_backtest_summary.json` — Historical frozen artifact; must remain a benchmark/reference, not a forward state store.
- `exports/e1r_v0_2_backtest_equity_curve.json` — Historical frozen artifact; do not overwrite with forward data.

## Target Summary Schema

### Status Fields
- `generated_at`
- `generated_at_display`
- `status_date`
- `strategy_id`
- `version`
- `forward_start_date`
- `official_kickoff_date`
- `forward_day_count`
- `tracking_status`
- `research_status`

### Performance Fields
- `portfolio_value`
- `equity`
- `cash`
- `market_value`
- `forward_return_pct`
- `spx_forward_return_pct`
- `alpha_pct`
- `max_drawdown_pct`
- `sharpe_ratio`
- `profit_factor`
- `number_of_trades`
- `executed_orders_count`
- `open_positions_count`

### Exposure Fields
- `gross_exposure`
- `net_exposure`
- `core_exposure`
- `sidecar_exposure`

### Regime Fields
- `market_state`
- `regime`
- `subclass`
- `core_active`
- `sidecar_active`
- `sidecar_selected_count`

## Implementation Phases

### 3.8E-2F-1C — Runner dry-run audit
- Goal: Run existing E1R OOS scripts locally without modification and inspect exact outputs/exit codes.
- Code changes: `False`
- Acceptance: Know which scripts run cleanly.
- Acceptance: Know which outputs are placeholders vs calculated.
- Acceptance: No source/export commit except docs report.

### 3.8E-2F-1D — E1R state namespace implementation
- Goal: Create E1R-only state/event/run-history files and prevent contamination of E1 state.
- Code changes: `True`
- Acceptance: data/oos/portfolio_state.json unchanged by E1R runner.
- Acceptance: data/oos/e1r_v0_2_portfolio_state.json created/updated deterministically.
- Acceptance: Runner is idempotent for same date/prices.

### 3.8E-2F-1E — E1R forward performance accounting
- Goal: Generate E1R summary/equity/positions/orders with real performance fields.
- Code changes: `True`
- Acceptance: summary contains forward_return_pct, portfolio_value, max_drawdown_pct.
- Acceptance: equity curve has at least one official kickoff row.
- Acceptance: positions/orders exist even if empty.
- Acceptance: historical backtest files unchanged.

### 3.8E-2F-1F — Daily pipeline integration
- Goal: Add official E1R forward runner to GitHub Actions daily update pipeline.
- Code changes: `True`
- Acceptance: Daily pipeline updates E1 and E1R independently.
- Acceptance: E1 exports/state remain unchanged except normal daily update.
- Acceptance: E1R exports update daily after market data refresh.

### 3.8E-2F-1G — Dashboard mapping
- Goal: Map E1R forward summary/equity fields into Research & Backtest.
- Code changes: `True`
- Acceptance: E1R Forward latest shows official status_date.
- Acceptance: E1R Forward return is populated from E1R forward summary.
- Acceptance: E1R equity curve uses forward curve, not historical backtest fallback.


## Risk Controls

- Do not modify frozen historical E1R strategy/backtest logic.
- Do not use E1 portfolio_state.json for E1R.
- Do not label backfilled rows as official OOS.
- Do not infer E1R forward performance from historical E1R backtest summary.
- Use smoke tests before GitHub Actions integration.
- Commit docs/audits separately from engine changes.
- Keep E1 and E1R export namespaces separate.

## Acceptance For This Stage

- Implementation route is documented.
- E1/E1R state separation is documented.
- Target export schema is documented.
- Kickoff policy is documented.
- No engine/dashboard/export files are changed.

