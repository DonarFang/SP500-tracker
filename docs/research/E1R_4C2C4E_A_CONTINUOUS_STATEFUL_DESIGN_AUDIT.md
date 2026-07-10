# E1R 4C-2C-4E-A — Continuous Stateful 5Y Backtest Design Audit

Generated At: `2026-07-10T02:14:31.433688+00:00`

## Purpose

This is a design audit only. It does not run a full 5Y backtest and does not generate an official E1R result.

## Formal Rule

Official E1R 5Y backtest must be a **single-account continuous stateful backtest**:

- one continuous account
- continuous cash
- continuous positions
- daily mark-to-market
- daily regime switch
- global live account holdings <= 3
- no stitched return curves
- no invalid artifacts as source

## Contract

```json
{
  "stage": "4C-2C-4E-A",
  "purpose": "Design audit for official E1R continuous stateful 5Y backtest.",
  "formal_backtest_definition": {
    "model": "single-account continuous stateful backtest",
    "timeline": "one continuous trading-day timeline",
    "state": [
      "cash",
      "positions",
      "total_equity"
    ],
    "daily_logic": [
      "mark existing account state",
      "read daily regime",
      "execute the validated branch for that regime",
      "enforce global live account holdings <= 3",
      "record daily account state"
    ]
  },
  "required_regime_contract": {
    "UPTREND": "validated UPTREND branch",
    "SIDEWAYS_MA_CONFLICT": "validated sidecar branch input; Top10 is candidate/basket only; live account holdings <= 3",
    "DETERIORATION_TRANSITION": "cash/defensive",
    "RECOVERY_TRANSITION": "cash/defensive",
    "DOWNTREND": "cash/defensive"
  },
  "not_allowed": [
    "Do not stitch UPTREND result curve with SIDEWAYS sidecar result curve.",
    "Do not use invalid historical artifacts as core source.",
    "Do not use composer output as formal E1R result if it only composes interval returns.",
    "Do not modify frozen strategy files in this audit.",
    "Do not generate official E1R result in this audit.",
    "Do not run full 5Y backtest in this audit."
  ]
}
```

## Validations

```json
{
  "audit_only_no_full_backtest_run": true,
  "official_result_generated": false,
  "dashboard_changed": false,
  "strategy_files_unchanged": true,
  "invalid_artifacts_not_used_as_source": true,
  "composer_not_allowed_for_formal_result_stitching": true,
  "continuous_stateful_required": true
}
```

## Backtest Engine Requirements

```json
{
  "has_run_stateful_simulation": true,
  "state_container_has_cash_and_positions": true,
  "records_daily_account_state": true,
  "has_mark_to_market_terms": true,
  "has_max_positions_reference": true,
  "has_open_positions_count_reference": true,
  "has_regime_reference": true,
  "has_e1r_reference": true,
  "has_uptrend_reference": true,
  "has_sideways_reference": true,
  "has_downtrend_reference": true
}
```

## Sidecar Requirements

```json
{
  "has_sidecar_config": true,
  "has_sidecar_builder": true,
  "has_allowed_subclasses": true,
  "has_ma_conflict_reference": true,
  "has_top_n_reference": true,
  "has_gross_exposure_reference": true,
  "has_candidate_count_reference": true,
  "has_selected_count_reference": true,
  "has_holdings_reference": true,
  "has_is_active_reference": true,
  "sidecar_can_provide_branch_candidate_data": true
}
```

## Composer Policy

```json
{
  "allowed_for_official_continuous_stateful_result": false,
  "reason": "Composer functions appear to compose interval returns/equity records. Official 4E requires one account with continuous cash/positions, not stitched result curves."
}
```

## Invalid Artifact Policy

```json
"These artifacts are historical/diagnostic only. Official 4E continuous stateful backtest must not read them as strategy/core sources."
```

## Design Decision

```json
{
  "engine_can_hold_single_account_state": true,
  "engine_has_regime_wiring_terms": true,
  "sidecar_can_supply_sideways_branch_data": true,
  "composer_allowed_for_formal_result": false,
  "invalid_artifacts_allowed_as_source": false,
  "conclusion": "READY_FOR_4C2C4E_B_CONTINUOUS_STATEFUL_SMOKE",
  "recommended_next_action": "Create a small continuous-stateful smoke/prototype that owns one account state, does not read invalid artifacts, does not stitch curves, and validates max open positions <= 3."
}
```

## Next Action

Create a small continuous-stateful smoke/prototype that owns one account state, does not read invalid artifacts, does not stitch curves, and validates max open positions <= 3.
