# Unified 5Y Data / Backtest / Dashboard Migration Specification v0.1

Status: DRAFT_SPECIFICATION  
Purpose: Merge the previous 3Y production line and 5Y research line into one unified data, backtest, export, and dashboard framework.

---

## 1. Objective

The project will no longer maintain two parallel data and strategy systems.

The unified framework will use:

- one primary 5Y data window
- one backtest engine
- one export schema
- one dashboard data contract
- E1 as frozen benchmark
- E1-R as research candidate

---

## 2. Motivation

The previous structure created unnecessary complexity:

- 3Y production exports
- 5Y research exports
- different strategy variants
- different backtest windows
- dashboard using a separate output set
- risk of inconsistent E1 numbers across environments

E1-R is a major strategy upgrade. This is the right time to consolidate the data and reporting architecture.

---

## 3. Target Architecture

Unified strategy IDs:

- E1_AUDITED_G4_MINHOLD10
- E1R_REGIME_AWARE_V0_1

Unified primary data window:

- 5Y default
- SPX master calendar
- Current Constituents preliminary until PIT constituents are available

Unified output destination:

- exports/backtest.json
- exports/trade_log.json
- exports/equity_curve.json
- exports/regime_attribution.json
- exports/e1r_diagnostics.json
- exports/oos_*.json

Research archive remains available but is not the primary dashboard source.

---

## 4. Data Layer Migration

## 4.1 Primary Data

The main price data should support 5Y validation by default.

Primary path:

- data/prices/

Research raw data remains local or archived:

- data/research/e1_5y/raw/

The system should avoid maintaining separate 3Y and 5Y active price universes.

## 4.2 Universe

Initial unified universe:

- Current S&P 500 constituents
- Preliminary only
- Not point-in-time

Future upgrade:

- Point-in-Time constituents
- historical adds/deletes
- survivorship-bias reduction

All reports must clearly mark:

- PRELIMINARY_CURRENT_CONSTITUENTS_NOT_PIT

until PIT support is complete.

## 4.3 Calendar

SPX remains the master calendar.

All stock series align by date, not by array index.

---

## 5. Backtest Migration

## 5.1 E1 Benchmark Protection

E1 remains frozen.

Strategy ID:

- E1_AUDITED_G4_MINHOLD10

Frozen reference metrics:

- Period A total return: +14.18%
- Period B total return: +21.80%
- Full total return: +7.52%
- Profit Factor: 1.25
- Sharpe: 0.18
- MaxDD: 38.10%

Any backtest engine migration must pass E1 baseline parity before E1-R results are trusted.

## 5.2 E1-R Candidate

E1-R is added as a separate strategy variant.

Strategy ID:

- E1R_REGIME_AWARE_V0_1

E1-R must not overwrite E1.

## 5.3 Required Backtest Output

Both E1 and E1-R should output:

- portfolio metrics
- trade log
- daily equity records
- regime attribution
- entry type distribution
- exit reason distribution
- exposure profile
- drawdown profile

---

## 6. Export Schema

## 6.1 exports/backtest.json

The unified schema should contain:

```json
{
  "backtest": {
    "results": {
      "layer_d": {
        "variant_results": {
          "E1_AUDITED_G4_MINHOLD10": {},
          "E1R_REGIME_AWARE_V0_1": {}
        }
      }
    }
  }
}
```

## 6.2 Strategy Result Required Fields

Each strategy result should include:

- strategy_id
- status
- assumptions
- metrics
- sample_validity
- closed_trades
- daily_equity_records
- daily_equity_record_count
- sim_end_liquidation_record
- regime_attribution
- entry_type_distribution
- exit_reason_distribution
- risk_budget_summary

## 6.3 Regime Attribution Export

Unified regime attribution output:

- exports/regime_attribution.json

Required keys:

- strategy_id
- total_return_attribution
- by_regime
- by_entry_type
- equity_level_attribution
- sample_status
- preliminary_status

## 6.4 E1-R Diagnostics Export

Dedicated E1-R diagnostic output:

- exports/e1r_diagnostics.json

Required diagnostics:

- Emerging vs Confirmed entry performance
- SIDEWAYS churn count
- SIDEWAYS failed-breakout losses
- DOWNTREND exception trade count
- UPTREND average holding period
- exit-after-performance diagnostic
- max favorable excursion
- max adverse excursion
- return giveback from peak

---

## 7. Dashboard Migration

## 7.1 Market Overview Tab

Add:

- Current SPX regime
- Regime since date
- E1-R active mode
- Risk budget by current regime
- Max positions allowed
- Max exposure allowed

Example display:

- Current Regime: UPTREND
- E1-R Mode: Emerging + Confirmed Leader Enabled
- Max Positions: 3
- Max Exposure: 100%

## 7.2 Leader Board Tab

Add E1-R fields:

- E1-R action
- E1-R entry type
- E1-R regime
- E1-R eligibility reason
- E1-R risk budget
- Emerging Leader flag
- Confirmed Leader flag
- Sideways Quality Breakout flag
- Downtrend Exception flag

## 7.3 Watchlist Tab

Add:

- E1-R candidate type
- regime-specific setup reason
- invalidation condition
- stop reference
- re-entry cooldown status

## 7.4 Positions & Exit Tab

Add E1-R position management:

- regime at entry
- current regime
- entry type
- current hold rule
- reduce trigger
- exit trigger
- trailing drawdown from highest close
- relative SPX performance since entry
- stop level

## 7.5 Research & Backtest Tab

Add E1 vs E1-R comparison:

- Total Return
- CAGR
- MaxDD
- Sharpe
- Profit Factor
- Win Rate
- Exposure
- Trades
- UPTREND attribution
- SIDEWAYS attribution
- DOWNTREND attribution
- Average holding period
- Average winner
- Average loser

Dashboard should clearly label:

- E1 Frozen Benchmark
- E1-R Research Candidate

---

## 8. OOS / Forward Test Migration

E1 OOS remains separate.

E1-R paper forward test ID:

- E1R_OOS_PAPER

Rules:

- paper only
- append-only events
- separate positions
- separate trades
- separate equity curve
- no mixing with E1 OOS
- no production decision until minimum review window is met

Minimum review window:

- 6 months or 20 closed trades

---

## 9. Migration Phases

## Phase 1: Specification

Create:

- E1R_REGIME_AWARE_STRATEGY_SPEC_v0.1.md
- UNIFIED_5Y_DATA_BACKTEST_DASHBOARD_MIGRATION_SPEC_v0.1.md

No code changes.

## Phase 2: Unified Data Validation

Confirm:

- 5Y data coverage
- SPX master calendar
- constituent count
- price coverage
- warmup sufficiency

## Phase 3: E1 Unified Baseline

Run E1 on unified data.

Confirm:

- E1 strategy exists
- E1 parity check passes or new unified baseline is explicitly frozen
- no accidental strategy drift

## Phase 4: E1-R Implementation

Implement:

- regime-aware risk budget
- UPTREND Emerging / Confirmed logic
- SIDEWAYS quality breakout logic
- DOWNTREND exception protocol
- regime-specific hold / reduce / exit

## Phase 5: Backtest

Run:

- E1
- E1-R v0.1

Compare behavior and risk metrics.

## Phase 6: Dashboard Integration

Update dashboard to display:

- current regime
- E1 vs E1-R comparison
- E1-R candidate labels
- E1-R position management
- E1-R diagnostics

## Phase 7: Forward Test

Start:

- E1R_OOS_PAPER

Maintain separation from E1 OOS.

---

## 10. Deprecated / Archived Items

The following should no longer be treated as active primary framework:

- separate 3Y production-only backtest baseline
- separate 5Y research-only output contract
- dashboard views that only understand E1 but not E1-R
- any E1-R result that overwrites E1 Champion

Legacy data and results may remain archived for audit history.

---

## 11. Acceptance Criteria

Migration is accepted only if:

- E1 Champion remains available
- E1 parity is protected or explicitly re-baselined under unified 5Y rules
- E1-R is clearly labeled as research candidate
- dashboard reads unified exports
- no duplicate conflicting 3Y / 5Y active results remain
- OOS logs remain separate
- generated reports clearly mark Current Constituents / Not PIT status

---

## 12. Non-Goals

This migration does not:

- optimize E1-R parameters
- declare E1-R production-ready
- remove E1 Champion
- solve PIT constituents
- alter live E1 OOS rules
- merge E1-R into production dashboard signals without forward test
