# Stage 3.8E-2F-2C-4C-6 Interval Schema Source Audit

Generated At: `2026-07-08T11:37:09.303883+00:00`

## Status

- Status: `INTERVAL_SCHEMA_AUDIT_COMPLETE_NO_EXPORTS_WRITTEN`
- Dashboard changed: `False`
- Exports changed: `False`
- Workflow changed: `False`
- Strategy logic changed: `False`
- Canonical exports written: `False`
- Long backtest run: `False`

## Diagnosis

- Exact toy schema works: extract_core_interval_returns -> build_equity_records_from_returns can generate portfolio-level equity records.
- Required sidecar interval fields include date, next_date, sidecar_return, sidecar_return_pct, spx_return, spx_return_pct, plus regime/subclass metadata.
- Required core daily fields include date and daily_return or daily_return_pct, keyed by the sidecar next_date.
- Found 20 JSON/schema candidates containing interval-related terms. Top candidate: docs/research/E1R_V0_2_STAGE3_8E2F2C4C5_EXPORT_WRAPPER_SMOKE_REPORT.json score=55.
- Next decision: locate real sidecar_records and core_daily_equity_records; if unavailable, export-only wrapper must generate/re-run them using frozen engine/composer code.

## Exact Schema Probe

```json
{
  "extract_ok": true,
  "interval_records": [
    {
      "date": "2021-06-11",
      "next_date": "2021-06-14",
      "core_end_date": "2021-06-14",
      "core_return": 0.01,
      "core_return_pct": 1.0,
      "sidecar_return": 0.0,
      "sidecar_return_pct": 0.0,
      "combined_return": 0.010000000000000009,
      "combined_return_pct": 1.0000000000000009,
      "spx_return": 0.005,
      "spx_return_pct": 0.5,
      "regime": "UPTREND",
      "subclass": null,
      "sidecar_active": false,
      "sidecar_selected_count": null,
      "sidecar_gross_exposure": null,
      "sidecar_holdings": []
    },
    {
      "date": "2021-06-14",
      "next_date": "2021-06-15",
      "core_end_date": "2021-06-15",
      "core_return": -0.005,
      "core_return_pct": -0.5,
      "sidecar_return": 0.0,
      "sidecar_return_pct": 0.0,
      "combined_return": -0.0050000000000000044,
      "combined_return_pct": -0.5000000000000004,
      "spx_return": -0.002,
      "spx_return_pct": -0.2,
      "regime": "SIDEWAYS",
      "subclass": "MA_CONFLICT",
      "sidecar_active": false,
      "sidecar_selected_count": null,
      "sidecar_gross_exposure": null,
      "sidecar_holdings": []
    }
  ],
  "interval_record_keys": [
    "combined_return",
    "combined_return_pct",
    "core_end_date",
    "core_return",
    "core_return_pct",
    "date",
    "next_date",
    "regime",
    "sidecar_active",
    "sidecar_gross_exposure",
    "sidecar_holdings",
    "sidecar_return",
    "sidecar_return_pct",
    "sidecar_selected_count",
    "spx_return",
    "spx_return_pct",
    "subclass"
  ],
  "build_ok": true,
  "equity_records": [
    {
      "date": "2021-06-14",
      "interval_start_date": "2021-06-11",
      "interval_end_date": "2021-06-14",
      "total_equity": 101000.0,
      "equity": 101000.0,
      "daily_return": 0.010000000000000009,
      "daily_return_pct": 1.0000000000000009,
      "drawdown": 0.0,
      "drawdown_pct": 0.0,
      "core_return": 0.01,
      "core_return_pct": 1.0,
      "sidecar_return": 0.0,
      "sidecar_return_pct": 0.0,
      "spx_return": 0.005,
      "spx_return_pct": 0.5,
      "spx_regime": "UPTREND",
      "sideways_subclass": null,
      "sidecar_active": false,
      "sidecar_selected_count": null,
      "sidecar_gross_exposure": null
    },
    {
      "date": "2021-06-15",
      "interval_start_date": "2021-06-14",
      "interval_end_date": "2021-06-15",
      "total_equity": 100495.0,
      "equity": 100495.0,
      "daily_return": -0.0050000000000000044,
      "daily_return_pct": -0.5000000000000004,
      "drawdown": -0.0050000000000000044,
      "drawdown_pct": -0.5000000000000004,
      "core_return": -0.005,
      "core_return_pct": -0.5,
      "sidecar_return": 0.0,
      "sidecar_return_pct": 0.0,
      "spx_return": -0.002,
      "spx_return_pct": -0.2,
      "spx_regime": "SIDEWAYS",
      "sideways_subclass": "MA_CONFLICT",
      "sidecar_active": false,
      "sidecar_selected_count": null,
      "sidecar_gross_exposure": null
    }
  ],
  "equity_record_keys": [
    "core_return",
    "core_return_pct",
    "daily_return",
    "daily_return_pct",
    "date",
    "drawdown",
    "drawdown_pct",
    "equity",
    "interval_end_date",
    "interval_start_date",
    "sidecar_active",
    "sidecar_gross_exposure",
    "sidecar_return",
    "sidecar_return_pct",
    "sidecar_selected_count",
    "sideways_subclass",
    "spx_regime",
    "spx_return",
    "spx_return_pct",
    "total_equity"
  ]
}
```

## Function Sources

### `src/engine/e1r_composer.py::extract_core_interval_returns`

- Lines: `94→168`
```python
def extract_core_interval_returns(
    core_daily_equity_records: Sequence[dict[str, Any]],
    sidecar_records: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Align core daily returns to sidecar intervals by next_date.

    Returns one record per shared interval:
    {
      date,
      next_date,
      core_return,
      sidecar_return,
      spx_return,
      ...
    }
    """
    core_by_end_date = {}

    for row in core_daily_equity_records:
        date = row.get("date")
        if not date:
            continue

        r = safe_float(row.get("daily_return"))
        if r is None:
            # Some historical outputs may store pct instead of decimal.
            rp = safe_float(row.get("daily_return_pct"))
            r = None if rp is None else rp / 100.0

        if r is None:
            continue

        core_by_end_date[date] = row | {"_normalized_daily_return": r}

    aligned: list[dict[str, Any]] = []

    for sidecar in sidecar_records:
        date = sidecar.get("date")
        next_date = sidecar.get("next_date")

        if not date or not next_date:
            continue

        core = core_by_end_date.get(next_date)
        if core is None:
            continue

        core_return = safe_float(core.get("_normalized_daily_return")) or 0.0
        sidecar_return = safe_float(sidecar.get("portfolio_return")) or 0.0
        spx_return = safe_float(sidecar.get("spx_return")) or 0.0

        combined_return = (1.0 + core_return) * (1.0 + sidecar_return) - 1.0

        aligned.append({
            "date": date,
            "next_date": next_date,
            "core_end_date": next_date,
            "core_return": core_return,
            "core_return_pct": pct_display(core_return),
            "sidecar_return": sidecar_return,
            "sidecar_return_pct": pct_display(sidecar_return),
            "combined_return": combined_return,
            "combined_return_pct": pct_display(combined_return),
            "spx_return": spx_return,
            "spx_return_pct": pct_display(spx_return),
            "regime": sidecar.get("regime"),
            "subclass": sidecar.get("subclass"),
            "sidecar_active": bool(sidecar.get("is_active")),
            "sidecar_selected_count": sidecar.get("selected_count"),
            "sidecar_gross_exposure": sidecar.get("gross_exposure"),
            "sidecar_holdings": sidecar.get("holdings", []),
        })

    return aligned
```

### `src/engine/e1r_composer.py::build_equity_records_from_returns`

- Lines: `171→211`
```python
def build_equity_records_from_returns(
    interval_records: Sequence[dict[str, Any]],
    initial_equity: float,
) -> list[dict[str, Any]]:
    equity = initial_equity
    peak = initial_equity
    records: list[dict[str, Any]] = []

    for row in interval_records:
        r = safe_float(row.get("combined_return")) or 0.0
        equity *= 1.0 + r
        peak = max(peak, equity)

        drawdown = equity / peak - 1.0 if peak > 0 else 0.0

        records.append({
            "date": row["next_date"],
            "interval_start_date": row["date"],
            "interval_end_date": row["next_date"],
            "total_equity": equity,
            "equity": equity,
            "daily_return": r,
            "daily_return_pct": pct_display(r),
            "drawdown": drawdown,
            "drawdown_pct": pct_display(drawdown),

            "core_return": row["core_return"],
            "core_return_pct": row["core_return_pct"],
            "sidecar_return": row["sidecar_return"],
            "sidecar_return_pct": row["sidecar_return_pct"],
            "spx_return": row["spx_return"],
            "spx_return_pct": row["spx_return_pct"],

            "spx_regime": row.get("regime"),
            "sideways_subclass": row.get("subclass"),
            "sidecar_active": row.get("sidecar_active"),
            "sidecar_selected_count": row.get("sidecar_selected_count"),
            "sidecar_gross_exposure": row.get("sidecar_gross_exposure"),
        })

    return records
```

## Top Schema Candidates

- score `55` · `docs/research/E1R_V0_2_STAGE3_8E2F2C4C5_EXPORT_WRAPPER_SMOKE_REPORT.json` · hits `extract_core_interval_returns, build_equity_records_from_returns, combined_return, core_return, core_return_pct, sidecar_return, sidecar_return_pct, spx_return, spx_return_pct, next_date, sidecar_records, core_daily_equity_records, sidecar_active, sidecar_selected_count, sidecar_gross_exposure, daily_records, daily_equity, total_equity, portfolio_value, strategy_indexed`
- score `51` · `docs/research/E1R_V0_2_STAGE3_8E2F1E0_TARGET_ACTION_INPUT_AUDIT.json` · hits `extract_core_interval_returns, build_equity_records_from_returns, combined_return, core_return, core_return_pct, sidecar_return, sidecar_return_pct, spx_return, spx_return_pct, next_date, sidecar_records, core_daily_equity_records, sidecar_active, sidecar_selected_count, sidecar_gross_exposure, daily_equity, total_equity, portfolio_value, strategy_indexed`
- score `50` · `docs/research/E1R_V0_2_STAGE3_8E2F1A_FORWARD_SOURCE_AUDIT.json` · hits `extract_core_interval_returns, build_equity_records_from_returns, combined_return, core_return, core_return_pct, sidecar_return, sidecar_return_pct, spx_return, spx_return_pct, next_date, sidecar_records, core_daily_equity_records, sidecar_active, sidecar_selected_count, sidecar_gross_exposure, daily_equity, total_equity, portfolio_value`
- score `48` · `docs/research/E1R_V0_2_STAGE3_8E2F0_FORWARD_KICKOFF_AUDIT.json` · hits `build_equity_records_from_returns, combined_return, core_return, sidecar_return, spx_return, spx_return_pct, next_date, sidecar_records, core_daily_equity_records, sidecar_active, sidecar_selected_count, sidecar_gross_exposure, daily_equity, total_equity, portfolio_value, strategy_indexed`
- score `42` · `docs/research/E1R_V0_2_STAGE3_8E2F2C4C4_GENERATOR_INTERNALS_EXPORT_WRAPPER_PROTOTYPE.json` · hits `extract_core_interval_returns, build_equity_records_from_returns, core_return, sidecar_return, spx_return, spx_return_pct, next_date, sidecar_records, core_daily_equity_records, sidecar_active, sidecar_selected_count, sidecar_gross_exposure, daily_records, daily_equity, total_equity, portfolio_value, strategy_indexed`
- score `35` · `docs/research/E1R_V0_2_STAGE3_8E2F2C4C2_RECOVER_5Y_PORTFOLIO_EQUITY_CANDIDATES.json` · hits `combined_return, spx_return, spx_return_pct, next_date, core_daily_equity_records, sidecar_active, sidecar_selected_count, daily_records, daily_equity, total_equity, portfolio_value, strategy_indexed`
- score `25` · `docs/research/E1R_V0_2_STAGE3_8E2F2C3FB_TREND_REGIME_SOURCE_AUDIT.json` · hits `extract_core_interval_returns, build_equity_records_from_returns, sidecar_return, spx_return, spx_return_pct, next_date, sidecar_active, sidecar_selected_count, portfolio_value`
- score `25` · `docs/research/E1R_V0_2_STAGE3_8E2F2C3FD_MARKET_STATE_GENERATOR_AUDIT.json` · hits `combined_return, next_date, sidecar_active, sidecar_selected_count, strategy_indexed`
- score `20` · `docs/research/E1R_V0_2_STAGE3_8E2A_DATA_SHAPE_AUDIT.json` · hits `spx_return, spx_return_pct, next_date, sidecar_active, sidecar_selected_count, daily_records, total_equity`
- score `17` · `docs/research/E1R_V0_2_STAGE3_8E2F1F0_DAILY_PIPELINE_AUDIT.json` · hits `spx_return, spx_return_pct, next_date, sidecar_active, sidecar_selected_count, total_equity, portfolio_value`
- score `15` · `docs/research/E1R_V0_2_OOS_SUMMARY_FIELD_AUDIT.json` · hits `spx_return, spx_return_pct, next_date, sidecar_active, sidecar_selected_count`
- score `15` · `docs/research/E1R_V0_2_STAGE3_5_MAIN_SMOKE_TEST_REPORT.json` · hits `spx_return, spx_return_pct, next_date, sidecar_active, sidecar_selected_count`
- score `15` · `docs/research/E1R_V0_2_STAGE3_8A_DASHBOARD_REFACTOR_AUDIT.json` · hits `spx_return, spx_return_pct, next_date, sidecar_active, sidecar_selected_count`
- score `15` · `docs/research/E1R_V0_2_STAGE3_8E2F1E1_TARGET_SOURCE_CONTRACT.json` · hits `spx_return, spx_return_pct, next_date, sidecar_active, sidecar_selected_count`
- score `14` · `docs/research/E1R_V0_2_STAGE3_8E2F2C4C3_BACKTEST_GENERATOR_CANONICAL_EXPORT_PLAN.json` · hits `extract_core_interval_returns, build_equity_records_from_returns, spx_return, spx_return_pct, core_daily_equity_records, sidecar_active, daily_records, daily_equity, total_equity, portfolio_value, strategy_indexed`
- score `13` · `docs/research/E1R_V0_2_STAGE3_8E2F1C_RUNNER_DRY_RUN_AUDIT.json` · hits `next_date, sidecar_active, sidecar_selected_count`
- score `12` · `docs/research/E1R_V0_2_STAGE3_8E2F2C3FC_E1R_STATUS_TREND_FIELD_AUDIT.json` · hits `next_date, sidecar_active`
- score `11` · `exports/e1r_v0_2_status.json` · hits `next_date`
- score `11` · `exports/oos_e1r_v0_2_sidecar.json` · hits `next_date`
- score `8` · `docs/research/E1R_V0_2_STAGE3_8E2F2C4C1_5Y_EQUITY_ARTIFACT_AUDIT.json` · hits `spx_return, spx_return_pct, sidecar_active, sidecar_selected_count, daily_equity, total_equity, portfolio_value, strategy_indexed`

## Next Stage

- `Stage 3.8E-2F-2C-4C-7`: Locate or generate real core_daily_equity_records and sidecar_records
- Recommended action: Search exact candidate JSONs and generator scripts for sidecar_records/core_daily_equity_records. If not persisted, implement wrapper inspect mode to call frozen generator path without writing final exports.

