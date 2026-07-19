# FD-M3180125 Engine Market State + Market Gate Integration

## Step 2 — Engine Integration

Status: `COMPLETE_PENDING_TEST_AND_COMMIT`

Formal path: Standard market data → E1RCoreEngine → MarketStateEvaluator → MarketGateEvaluator → MarketGateDecision → strategy branch.

E1RCoreEngine owns both evaluators. Backtest calls the Engine-owned evaluator chain and compares it with frozen Legacy local values. Forward no longer requires a Market Gate provider. Formal 5Y acceptance remains Step 3.
