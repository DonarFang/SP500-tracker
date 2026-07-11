# E1R K2 R15 UptrendCore Gate Consumption Smoke

Generated UTC: 2026-07-11T09:39:23.867738+00:00

Stage:
4C-2C-4E-ENGINE-K2-R15-UPTREND-CORE-GATE-CONSUMPTION-SMOKE

Scope:

- Consume an existing MarketGateDecision.
- Consume existing OrderIntent records.
- Do not generate order intents.
- Do not rank or select candidates.
- Do not size positions.
- Do not mutate account state.
- Do not recompute gate state.
- Do not call legacy backtest code.
- Do not run a full 5Y backtest.
- Do not integrate SIDEWAYS logic.

Approved behavior:

ALLOW:
- BUY preserved
- ADD preserved
- HOLD preserved
- REDUCE preserved
- EXIT preserved

RISK_OFF and SHOCK:
- BUY blocked
- ADD blocked
- HOLD preserved
- REDUCE preserved
- EXIT preserved

Guard row 2021-06-18:

- SPX close below MA50
- market_state CAUTIOUS_ON
- entry_capacity 2
- expected gate_state ALLOW
- BUY and ADD remain allowed

Guard row 2021-05-12:

- SPX daily return at or below minus 2 percent
- market_state CASH_MODE
- entry_capacity 0
- expected gate_state SHOCK
- BUY and ADD blocked
- HOLD, REDUCE, and EXIT preserved

Next stage after approval:

4C-2C-4E-ENGINE-K2-R16-LEGACY-UPTREND-ORDER-LOGIC-EXTRACTION-PROPOSAL
