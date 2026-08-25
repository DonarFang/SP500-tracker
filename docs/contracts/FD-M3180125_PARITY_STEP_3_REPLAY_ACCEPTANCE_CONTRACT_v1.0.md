# FD-M3180125 Parity-step-3 Read-only Replay Acceptance Contract v1.0

Status: FROZEN FOR PARITY-STEP-3 ONLY

## Scope

Starting at 2026-08-13, replay Personal Live decisions with the Step-2 Yahoo-adjusted shadow store and compare each common trading date with the formal Forward account-independent decision contract.

## Hard boundaries

- 5Y is read-only and is not executed or changed.
- Forward artifacts and strategy are not changed.
- Live history, NTAP/HPE facts, opening contract and current state are not rewritten.
- Active Live, broker APIs and automatic execution are not invoked.
- BUY/ADD manual pause remains; REDUCE remains manual-verification only.
- No ranking, regime, gate, Top3, ATR, priority, sizing or execution rule is reimplemented here.

## Causal replay

Each date uses an isolated temporary Live root. Confirmed transaction events with `trade_date` after that date and cash controls with `effective_date` after that date are excluded. The official append-only files are hash-checked before and after.

## Daily parity

The exact account-independent fields are `regime`, `regime_subclass`, `market_state`, `market_gate`, `entry_capacity`, and `strategy_branch`. Forward and Live are isolated accounts, so different holdings may legitimately produce different ordered `reference_top3`; Top3 equality is recorded as diagnostic evidence and is not a parity gate. Live actions are validated against the shared action vocabulary; account-dependent actions are not required to equal Forward holdings.

Legacy-to-adjusted differences are diagnostic evidence, not automatic failures. Any formal Forward contract mismatch, action-contract error, Forward `MISSING_T1_BAR` execution skip, forbidden ETF in the stock universe, missing adjusted evidence, or protected-file hash change results in `HOLD_PARITY_STEP_3`.

## PASS meaning

`PASS_PARITY_STEP_3_READ_ONLY_REPLAY` means the shadow replay is auditable and activation-eligible for the separately approved next decision. It does not activate adjusted prices, re-enable BUY/ADD, approve REDUCE, or authorize execution.
