# E1-R Regime-Aware Strategy Specification v0.1

Status: DRAFT_SPECIFICATION  
Strategy ID: E1R_REGIME_AWARE_V0_1  
Baseline Benchmark: E1_AUDITED_G4_MINHOLD10  
Purpose: Define an initial audited, non-optimized, regime-aware strategy framework for future backtest and forward test.

---

## 1. Objective

E1-R is not a replacement for E1 Champion.

E1 remains the frozen benchmark. E1-R is a research candidate designed to test whether regime-aware entry, hold, reduce, exit, and risk-budget rules improve portfolio behavior across different market environments.

The key hypothesis is:

> E1 may identify strong stocks, but its current hold / reduce / exit rules are too static across market regimes.

E1-R separates market regimes into:

- UPTREND
- SIDEWAYS
- DOWNTREND

Each regime uses different operating principles.

---

## 2. Regime Source

E1-R v0.1 uses the existing weekly SPX regime classifier.

No new market regime model is introduced in v0.1.

Regime classifier output:

- UPTREND
- SIDEWAYS
- DOWNTREND

The regime classifier is an upstream controller. It determines:

- entry permission
- entry type
- maximum exposure
- position size
- add permission
- hold tolerance
- reduce threshold
- exit threshold
- exception trade protocol

---

## 3. General Design Principles

E1-R v0.1 follows these principles:

1. Do not optimize parameters before first backtest.
2. Do not modify E1 Champion.
3. Separate entry alpha from hold / exit alpha.
4. Do not use one static trend-health threshold across all regimes.
5. UPTREND should identify strong stocks earlier and hold winners longer.
6. SIDEWAYS should reduce noise trading, smooth small fluctuations, and stop failed setups quickly.
7. DOWNTREND should prioritize cash, discipline, and exception-only trading.
8. All trades must carry regime and entry-type labels.

---

# 4. UPTREND Mode

## 4.1 Objective

UPTREND mode is offensive.

The goal is:

- identify emerging leaders earlier
- avoid entering only after late-stage momentum extension
- add only after confirmation
- let winners run
- avoid premature exits caused by short-term LS / TH noise

## 4.2 Entry Types

UPTREND uses two entry types.

### 4.2.1 Emerging Leader Entry

Purpose: Capture strong stocks earlier before they reach the absolute top of the Leader Board.

Initial conditions:

- Regime = UPTREND
- RS >= 80
- RS 20-day improvement >= +10 percentile
- Momentum Score >= 70
- Momentum Acceleration > 0
- Trend Health >= 65
- Close > MA20
- MA20 slope > 0 OR MA20 > MA50
- Leader Rank <= 20
- Market Gate allows risk exposure

Position size:

- 0.5 slot
- approximately 16.7% of portfolio when max_positions = 3

Trade label:

- E1R_UPTREND_EMERGING

### 4.2.2 Confirmed Leader Entry

Purpose: Follow already confirmed market leaders.

Initial conditions:

- Regime = UPTREND
- RS >= 90
- Leader Rank <= 5
- Leader Score >= 75
- Momentum Score >= 75
- Trend Health >= 70
- Close > MA50
- MA50 slope >= 0
- Market Gate allows risk exposure

Position size:

- 1.0 slot
- approximately 33.3% of portfolio

Trade label:

- E1R_UPTREND_CONFIRMED

## 4.3 Add Rules

Add is allowed only in UPTREND. Add is not allowed to average down.

Add conditions:

- Existing position is Emerging Leader
- Position return > +3%
- RS >= 90
- Leader Rank <= 5
- Close > MA20
- Momentum Acceleration >= 0

Add size:

- +0.5 slot

Maximum single position:

- 1.0 slot
- approximately 33.3% of portfolio

## 4.4 Hold Rules

UPTREND hold logic should tolerate normal pullbacks.

Do not exit solely because:

- LS falls below 75
- LS falls below 60
- RS cools from extreme levels
- price retests MA20 or MA50
- momentum decelerates without structural breakdown

## 4.5 Reduce Rules

Reduce 50% if either condition group is met:

Group A:

- LS < 70
- Close < MA20
- RS 10-day decline >= 8 percentile

Group B:

- drawdown from highest close >= 12%
- Close < MA20

## 4.6 Exit Rules

Exit if any condition group is met:

Group A:

- LS < 60
- Close < MA50
- MA50 slope < 0

Group B:

- Relative performance vs SPX since entry <= -8%
- Close < MA50

Group C:

- drawdown from highest close >= 18%

## 4.7 UPTREND Risk Budget

- max_positions = 3
- max_single_position = 33.3%
- Emerging initial size = 16.7%
- Confirmed initial size = 33.3%
- Add allowed = Yes
- MinHold = 10 trading days
- Re-entry cooldown = none by default

---

# 5. SIDEWAYS Mode

## 5.1 Objective

SIDEWAYS mode is selective.

The goal is:

- avoid frequent entry / exit
- avoid being shaken out by small fluctuations
- trade only high-quality setups
- stop failed breakouts quickly
- reduce churn and false signals

## 5.2 Entry Rules

SIDEWAYS does not allow Emerging Leader Entry. Only high-quality confirmed setups are allowed.

Entry conditions:

- Regime = SIDEWAYS
- RS >= 92
- Leader Rank <= 5
- Leader Score >= 80
- Trend Health >= 75
- Momentum Score >= 75
- Close > MA50
- MA50 slope >= 0
- 20-day pullback <= 8%
- Close distance from MA50 <= +12%
- No obvious volatility expansion
- Market Gate allows limited exposure

Position size:

- 0.5 slot
- approximately 16.7% of portfolio

Trade label:

- E1R_SIDEWAYS_QUALITY_BREAKOUT

## 5.3 Hold Rules

SIDEWAYS hold logic should smooth small fluctuations.

Continue holding if:

- Close >= MA50
- RS >= 85
- Drawdown from highest close < 8%
- Price has not clearly fallen back into failed-breakout structure
- Relative performance vs SPX has not materially deteriorated

## 5.4 Reduce Rules

Reduce 50% if either condition group is met:

Group A:

- RS decline from entry >= 10 percentile
- Close < MA20

Group B:

- LS < 70
- Momentum Acceleration < 0

## 5.5 Exit Rules

Exit if any condition is met:

- Close < MA50
- Loss from entry price <= -6%
- Drawdown from highest close >= 10%
- Relative performance vs SPX since entry <= -5%
- Failed breakout confirmed by price falling back below breakout structure

## 5.6 Anti-Churn Rules

To avoid frequent trading:

- Same-symbol re-entry cooldown = 10 trading days after EXIT
- SIDEWAYS new BUY limit = 1 per day
- Add allowed = No

## 5.7 SIDEWAYS Risk Budget

- max_positions = 2
- max_single_position = 16.7%
- max_total_exposure = 33.3%
- Emerging entry = No
- Add allowed = No
- MinHold = 5 trading days
- Stop loss = -6%
- Trailing drawdown stop = -10%
- Re-entry cooldown = 10 trading days

---

# 6. DOWNTREND Mode

## 6.1 Objective

DOWNTREND mode is defensive.

The goal is:

- preserve capital
- avoid trading impulse
- default to cash
- only allow rare exception trades
- avoid forcing the system to trade

## 6.2 Default Rules

In DOWNTREND:

- no normal long entry
- no Emerging Leader Entry
- no normal Confirmed Leader Entry
- no Add
- no forced trading due to high cash
- cash can be 100%

## 6.3 Exception Trade Entry

Exception trades are allowed only if all conditions are met.

Entry conditions:

- Regime = DOWNTREND
- RS >= 97
- Leader Rank <= 3
- Leader Score >= 85
- Trend Health >= 80
- Momentum Score >= 80
- Close > MA50
- MA50 slope >= 0
- Relative SPX 20-day return >= +8%
- 10-day maximum single-day drawdown not worse than -5%
- No SPX shock day
- No VIX / market stress override if available

Position size:

- 0.25 slot
- approximately 8.3% of portfolio

Trade label:

- E1R_DOWNTREND_EXCEPTION

## 6.4 Hold Rules

Continue holding only if:

- RS >= 90
- Close > MA20
- Relative SPX performance has not deteriorated
- Position loss > -4%
- Market is not in active shock

## 6.5 Exit Rules

Exit if any condition is met:

- Close < MA20
- Loss from entry price <= -4%
- Drawdown from highest close >= 7%
- Relative performance vs SPX since entry <= -3%
- SPX daily return <= -2%
- Exception trade no longer qualifies as exceptional

## 6.6 DOWNTREND Risk Budget

- max_positions = 1
- max_total_exposure = 10%
- position size = 8.3%
- Add allowed = No
- MinHold = 0
- Stop loss = -4%
- Trailing drawdown stop = -7%
- Relative SPX stop = -3%

---

# 7. Audit Requirements

E1-R v0.1 must output:

- full return
- Period A return
- Period B return
- CAGR
- MaxDD
- Profit Factor
- Sharpe
- Win Rate
- Avg Winner
- Avg Loser
- Exposure
- Trades by regime
- Entry type distribution
- Exit reason distribution
- Equity attribution by regime
- Entry-Hold-Exit diagnostic

---

# 8. Acceptance Criteria

E1-R v0.1 does not need to immediately beat E1 on total return.

Minimum research acceptance criteria:

- E1 baseline remains unchanged
- MaxDD must be lower than E1's 38.1% to count as safety improvement
- UPTREND should remain the major profit contributor
- SIDEWAYS trade count must not expand excessively
- DOWNTREND trades must remain rare
- DOWNTREND exposure must stay below 10%
- UPTREND average holding period should be longer than E1 if early-exit problem is reduced
- SIDEWAYS average loss should improve versus E1
- E1-R output must be separately labeled and must not replace E1 Champion

---

# 9. Forbidden Actions

Do not:

- modify E1_AUDITED_G4_MINHOLD10
- tune parameters before first full backtest
- merge E1-R into dashboard as production signal before forward test
- use DOWNTREND trades to force market participation
- optimize on SIDEWAYS sample if sample size is insufficient
- reopen E2 Dynamic Exit as part of E1-R v0.1

---

# 10. Forward Test

Forward test ID:

- E1R_OOS_PAPER

Forward test rules:

- paper only
- separate from E1 OOS
- append-only log
- no live decision mixing with E1 Champion
- minimum evaluation window: 6 months or 20 closed trades
