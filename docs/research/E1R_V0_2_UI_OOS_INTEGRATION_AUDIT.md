# E1R v0.2 UI/OOS Integration Audit Manifest

## 1. Status

Strategy ID: E1R_REGIME_AWARE_V0_2  
Current Phase: UI/OOS Integration  
Branch: feature/e1-5y-data  
Status: INTEGRATED_TO_OOS_2B_2_PAPER_TRACKING  

This audit manifest records the current E1R v0.2 integration state after:

1. Formal backtest implementation
2. Full 5Y validation
3. Dashboard market state integration
4. OOS-1 status/signal export
5. OOS-2A 5Y backtest equity export
6. OOS-2B.1 forward/OOS equity initialization
7. OOS-2B.2 sidecar MTM framework

---

## 2. Completed Layers

### 2.1 Formal Engine

Status: COMPLETE

Implemented files:

- src/engine/e1r_sidecar_sleeve.py
- src/engine/e1r_composer.py
- src/engine/backtest.py

Validated strategy:

E1R_REGIME_AWARE_V0_2  
=  
E1R_REGIME_AWARE_V0_1 core  
+  
SIDEWAYS:MA_CONFLICT Top10 25% daily rebalanced sidecar sleeve

Full 5Y validation:

- Total Return: +116.7435999134756%
- SPX Return: +76.844174428316%
- Alpha: +39.89942548515961%
- Max Drawdown: 25.904809362815108%
- Profit Factor: 1.1919630955509348
- Sharpe Ratio: 0.7957270568329264
- Sidecar Active Days: 135

### 2.2 Documentation

Status: COMPLETE

Documents:

- docs/research/E1R_V0_2_IMPLEMENTATION_MANIFEST.md
- docs/research/E1R_V0_2_OOS_2B_2_SIDECAR_MTM_SPEC.md

### 2.3 Market State UI

Status: COMPLETE

Dashboard now displays current market state and E1R v0.2 core/sidecar activation status.

Data source priority:

- exports/e1r_v0_2_status.json
- fallback: exports/market_state.json

Current state model:

- Mutually exclusive daily market state model

Valid states:

- UPTREND
- DOWNTREND
- SIDEWAYS_MA_CONFLICT
- SIDEWAYS_DETERIORATION
- SIDEWAYS_RECOVERY
- UNKNOWN

Current policy:

UPTREND:

- core active
- sidecar inactive

SIDEWAYS_MA_CONFLICT:

- core inactive/residual
- sidecar active

DOWNTREND / other SIDEWAYS subclasses / UNKNOWN:

- defensive / inactive

### 2.4 OOS-1 Status / Signal Export

Status: COMPLETE

Files:

- scripts/export_e1r_v0_2_status.py
- scripts/run_e1r_v0_2_oos.py
- exports/e1r_v0_2_status.json
- exports/oos_e1r_v0_2_summary.json
- exports/oos_e1r_v0_2_sidecar.json
- exports/oos_e1r_v0_2_positions.json
- exports/oos_e1r_v0_2_orders.json

OOS-1 boundary:

- Status/signal export only
- No real execution
- No broker integration

### 2.5 OOS-2A 5Y Backtest Equity Export

Status: COMPLETE

Files:

- scripts/export_e1r_v0_2_backtest_equity.py
- exports/e1r_v0_2_backtest_summary.json
- exports/e1r_v0_2_backtest_equity_curve.json

Dashboard Research & Backtest now reads:

- exports/e1r_v0_2_backtest_equity_curve.json

Curve type:

- FULL_5Y_BACKTEST_EQUITY

Validation:

- Start Date: 2021-06-14
- End Date: 2026-06-16
- Row Count: 1258

Important distinction:

- This is historical 5Y backtest equity.
- It is not live forward/OOS equity.

### 2.6 OOS-2B.1 Forward/OOS Equity Curve Initialization

Status: COMPLETE

Files:

- scripts/run_e1r_v0_2_oos_equity.py
- exports/oos_e1r_v0_2_equity_curve.json

Forward/OOS fields established:

- core_equity
- sidecar_equity
- combined_equity
- core_daily_return
- sidecar_daily_return
- combined_daily_return

Initial status:

- FORWARD_OOS_EQUITY
- PAPER_TRACKING_NO_REAL_EXECUTION

### 2.7 OOS-2B.2 Sidecar MTM Framework

Status: COMPLETE

Sidecar MTM rule:

- Use previous sidecar positions to calculate current close-to-close return.
- Do not use current-day selected positions to calculate current-day return.

Formula:

sidecar_daily_return(D) = sum(weight_i(D-1) * return_i(D-1 -> D))

Added fields:

- sidecar_positions
- sidecar_mtm_status
- sidecar_mtm_details

Valid MTM statuses:

- CALCULATED_FROM_PREVIOUS_POSITIONS
- NO_PREVIOUS_SIDECAR_POSITIONS
- PREVIOUS_SIDECAR_INACTIVE
- MISSING_PRICE_DATA
- SAME_DATE_NO_NEW_MTM

Current equity status:

- OOS_EQUITY_MTM_TRACKING_SIDECAR_PAPER

Execution status remains:

- PAPER_TRACKING_NO_REAL_EXECUTION

---

## 3. Dashboard Integration

Dashboard files changed:

- dashboard/app.js
- dashboard/styles.css

Dashboard now distinguishes:

1. Current Market State
2. E1R v0.2 Forward / OOS Status
3. E1R v0.2 Forward / OOS Equity Curve
4. E1R v0.2 Full 5Y Backtest Equity Curve

### 3.1 Market Overview

Market Overview displays:

- Current Market State
- E1R v0.2 Forward / OOS
- E1R v0.2 Forward / OOS Equity

Forward/OOS equity source:

- exports/oos_e1r_v0_2_equity_curve.json

### 3.2 Research & Backtest

Research & Backtest displays:

- E1R v0.1 Core
- E1R v0.2 Core + Sidecar

Backtest equity source:

- exports/e1r_v0_2_backtest_equity_curve.json

---

## 4. Workflow Integration

Workflow file:

- .github/workflows/update.yml

OOS runner:

- scripts/run_e1r_v0_2_oos.py

OOS equity runner:

- scripts/run_e1r_v0_2_oos_equity.py

Expected daily refresh chain:

1. Generate E1R v0.2 status
2. Generate OOS-1 summary/sidecar/positions/orders
3. Refresh OOS forward equity curve
4. Dashboard reads updated exports

---

## 5. Current Boundary / Do Not Misinterpret

The current system is not a real execution engine.

Current execution status:

- PAPER_TRACKING_NO_REAL_EXECUTION

Current sidecar status:

- MTM framework exists.
- Sidecar paper MTM is calculated only when previous sidecar positions exist.

Not yet implemented:

1. Real broker execution
2. Real order fills
3. Slippage
4. Transaction costs
5. Stateful sidecar trade lifecycle
6. Production-grade order reconciliation
7. Formal promotion to live strategy

---

## 6. Current Known Limitation

The current sidecar MTM uses previous sidecar positions from the forward/OOS equity record.

This is correct for no-lookahead tracking, but the sidecar position lifecycle is still simplified:

Current:

- previous target positions -> close-to-close MTM

Not yet:

- real order lifecycle
- rebalance turnover
- partial fills
- commission/slippage
- actual portfolio holdings reconciliation

---

## 7. Next Recommended Work

Recommended next phase:

OOS-2B.3 Sidecar simulated lifecycle / turnover tracking

Purpose:

1. Track sidecar target changes day by day.
2. Calculate turnover.
3. Track entered/exited sidecar symbols.
4. Prepare transaction cost analysis.
5. Preserve paper-tracking boundary.

Suggested future outputs:

- exports/oos_e1r_v0_2_sidecar_turnover.json
- exports/oos_e1r_v0_2_sidecar_lifecycle.json

Alternative next work:

- Port feature/e1-5y-data selected changes to sp500-tracker-v13/main

But before porting, recommended:

1. Run one full workflow smoke test.
2. Verify Dashboard loads all new JSON files.
3. Confirm no stale generated_at-only diffs remain.
4. Confirm GitHub Pages branch/source plan.

---

## 8. Important Commits

Key commits in this integration phase:

- b1e152f Add E1R v0.2 formal sidecar sleeve engine
- 2a780f4 Add E1R v0.2 status export for dashboard
- 420b4a8 Add E1R v0.2 OOS status signal export
- 5000882 Show E1R v0.2 OOS status on dashboard
- 47c0daf Export E1R v0.2 5Y backtest equity curve
- 4b725e2 Use E1R v0.2 5Y equity curve on dashboard
- 0bb0fbd Initialize E1R v0.2 OOS forward equity curve
- 2a6071d Show E1R v0.2 OOS equity curve on dashboard
- 17267f7 Clarify E1R v0.2 OOS equity status labels
- ccf6316 Add E1R v0.2 OOS sidecar MTM tracking

---

## 9. Final Integration Statement

E1R v0.2 is now integrated across:

1. Formal 5Y backtest engine
2. Documentation / manifest
3. Lightweight 5Y backtest equity export
4. Dashboard 5Y backtest equity display
5. Market state UI
6. OOS-1 status/signal exports
7. Forward/OOS equity curve initialization
8. Sidecar paper MTM tracking framework

The system is ready for either:

A. OOS-2B.3 sidecar turnover/lifecycle tracking

or

B. controlled port/merge planning into sp500-tracker-v13/main
