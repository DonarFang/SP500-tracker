# FD-M3180125 Engine Market State + Market Gate Integration

## Step 2 — Engine Integration

Status: `COMPLETE`

Formal path: Standard market data → E1RCoreEngine → MarketStateEvaluator → MarketGateEvaluator → MarketGateDecision → strategy branch.

E1RCoreEngine owns both evaluators. Backtest calls the Engine-owned evaluator chain and compares it with frozen Legacy local values. Forward no longer requires a Market Gate provider. Formal 5Y acceptance remains Step 3.

## Canonical configuration ownership completion

`E1RCoreEngineConfig` now formally owns `MarketStateConfig`,
`MarketGateConfig`, and canonical `max_positions=3`.

`E1RCoreEngine.evaluate_market_state_and_gate()` consumes those
Engine-owned configuration objects directly. It no longer constructs
new default configurations inside the evaluation call.

The canonical default remains D3 Risk-Off plus Shock, Shock enabled at
-2%, and max-three holdings. Historical D2 / Shock-off / max-10 research
runners are not promoted into the canonical Engine contract.

No Forward runtime workflow was activated and no formal 5Y validation
was performed in Step 2.
