# E1R_REGIME_AWARE_V0_2 Implementation Manifest

## Status

Strategy ID: E1R_REGIME_AWARE_V0_2  
Status: FORMAL_ENGINE_PASS  
Branch: feature/e1-5y-data  
Implementation Commit: b1e152f  
Push Status: pushed  

## Strategy Definition

E1R_REGIME_AWARE_V0_2 is:

E1R_REGIME_AWARE_V0_1 core  
+  
SIDEWAYS:MA_CONFLICT Top10 25% daily rebalanced sidecar sleeve

Rules:

- UPTREND: use unchanged E1R_REGIME_AWARE_V0_1 logic.
- SIDEWAYS: sidecar sleeve may be active only when subclass is MA_CONFLICT.
- SIDEWAYS:DETERIORATION_TRANSITION: no sidecar exposure.
- SIDEWAYS:RECOVERY_TRANSITION: no sidecar exposure.
- DOWNTREND: no sidecar exposure.
- Basket: Top 10 candidates.
- Gross exposure: 25%.
- Rebalance: daily close-to-close.
- Excluded symbol: VIXY.

## Candidate Score

The sidecar uses the validated S4 opportunity score:

score =
  2.0 * rs20_vs_spx
+ 1.0 * rs60_vs_spx
+ 0.5 * mom20
+ 0.25 * mom60
+ 3.0 * trend_points
+ 0.2 * drawdown_60d

trend_points is a 0-6 structure score:

- close > MA20
- close > MA50
- close > MA150
- close > MA200
- MA50 > MA150
- MA150 > MA200

## Architecture

New modules:

- src/engine/e1r_sidecar_sleeve.py
- src/engine/e1r_composer.py

Design constraints:

- run_stateful_simulation() is not modified.
- E1R_REGIME_AWARE_V0_1 is not modified.
- E1 / E2 variants are not modified.

Composition formula:

combined_daily_return = (1 + core_return) * (1 + sidecar_return) - 1

Alignment rule:

For sidecar interval date -> next_date, use core daily return ending at next_date.

## Full Backtest Validation

Full 5Y validation passed.

Comparison name: Strategy Variant Comparison  
Sample status: VALID  
Simulation start: 2021-06-11  
Simulation end: 2026-06-18  
Simulation days: 1261  

E1R_REGIME_AWARE_V0_1:

- Total Return: +105.61%
- Max Drawdown: 28.69%
- Research Status: UPTREND_EXECUTION_V0_1
- Regime Logic: UPTREND_EXECUTION_V0_1_ENTRY_ONLY
- Composition Exists: False

E1R_REGIME_AWARE_V0_2:

- Total Return: +116.7435999134756%
- SPX Return: +76.844174428316%
- Alpha: +39.89942548515961%
- Max Drawdown: 25.904809362815108%
- Profit Factor: 1.1919630955509348
- Sharpe Ratio: 0.7957270568329264
- Research Status: FORMAL_SIDECAR_SLEEVE_ENGINE
- Regime Logic: UPTREND_V0_1_CORE_PLUS_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE
- Sidecar Active Days: 135
- Composition Exists: True

Sidecar exposure:

- sidecar_active_by_regime: SIDEWAYS = 135
- sidecar_active_by_subclass: MA_CONFLICT = 135

Sidecar contribution:

- UPTREND: 0.0%
- SIDEWAYS: +6.265828411986754%
- DOWNTREND: 0.0%
- MA_CONFLICT: +6.265828411986754%
- DETERIORATION_TRANSITION: 0.0%
- RECOVERY_TRANSITION: 0.0%

## Invariants

Do not modify without revalidation:

1. Do not modify E1R_REGIME_AWARE_V0_1 behavior.
2. Do not force sidecar logic into run_stateful_simulation().
3. Do not enable sidecar exposure in DOWNTREND.
4. Do not enable sidecar exposure in RECOVERY_TRANSITION.
5. Do not enable sidecar exposure in DETERIORATION_TRANSITION.
6. Do not include VIXY in the sidecar universe.
7. Do not change Top10 selection without revalidation.
8. Do not change 25% gross exposure without revalidation.
9. Do not change daily close-to-close rebalance semantics without revalidation.
10. Do not change the S4 opportunity score without revalidation.
11. Do not change core/sidecar next_date alignment without revalidation.

## Output Conventions

max_drawdown_pct uses positive magnitude.

Example:

25.90 means a 25.90% maximum drawdown.

The comparison block name is:

Strategy Variant Comparison

## Known Limitations

Current sidecar sleeve validation does not yet include explicit transaction costs or slippage.

Before production/OOS promotion, evaluate:

- daily rebalance turnover
- estimated transaction cost
- liquidity constraints
- capacity limits
- spread/slippage assumptions

The sidecar sleeve currently produces daily holdings and contribution records, not traditional stateful round-trip trade records.

## Future Work

Recommended next steps:

1. Output schema review for Dashboard compatibility.
2. Dashboard UI:
   - show E1R_REGIME_AWARE_V0_2
   - show Core / Sidecar / Combined breakdown
   - show current market state:
     Uptrend
     Downtrend
     Sideway-MA-conflict
     Sideway-Deterioration
     Sideway-Recovery
3. OOS integration:
   - daily sidecar sleeve signal
   - sidecar active/inactive status
   - sidecar selected Top10 list
4. Transaction cost / turnover analysis.
5. Optional sidecar trade-log representation.
6. Merge or port selected implementation to sp500-tracker-v13 when ready.

## Final Freeze Statement

E1R_REGIME_AWARE_V0_2 is formally implemented as:

E1R_REGIME_AWARE_V0_1 core  
+  
SIDEWAYS:MA_CONFLICT Top10 25% daily rebalanced sidecar sleeve

Full 5Y validation passed.  
Implementation committed and pushed.  
This version is ready for documentation/schema review and future Dashboard/OOS integration.
