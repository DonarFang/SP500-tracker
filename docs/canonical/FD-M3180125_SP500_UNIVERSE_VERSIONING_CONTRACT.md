# FD-M3180125 S&P 500 Universe Versioning Contract

```text
Contract version: v1.2 UV-step-4 production integration
Original freeze: 2026-08-10
Original Authority HEAD: 43a85815992f1fddefa2da509c2175380c2330da
Aligned implementation Authority: a3f14b45cf4e2d5746ad67d972fba4dc680904db
UV-step-1: COMPLETE / PASS_UV_STEP_1_CONTRACT_FROZEN
UV-step-2: COMPLETE / ISOLATED IMPLEMENTATION
UV-step-3: COMPLETE / SHADOW ACCEPTED / PRODUCTION INACTIVE
UV-step-4: V1.0 FROZEN / IMPLEMENTATION AND CONTROLLED ACTIVATION AUTHORIZED
```

The v1.1 alignment preserves the v1.0 scope, ten-path source whitelist,
default-off shadow semantics, 30 acceptance gates, and production-inactive
boundary.  It changes no strategy contract.  It only rebases the approved
shadow integration onto the canonical single-`Engine.step()` Forward/Live
authority and strengthens symlink isolation, Authority validation, run-id
completeness, and pre-publication protected-manifest verification.

The exact UV-step-3 source whitelist remains:

```text
docs/canonical/FD-M3180125_SP500_UNIVERSE_VERSIONING_CONTRACT.md
scripts/run_engine_forward_daily.py
src/e1r_engine/forward_orchestrator.py
scripts/run_fd_m3180125_live_daily.py
src/e1r_engine/universe_versioning/shadow_integration.py
tests/test_fd_m3180125_universe_shadow_contract.py
tests/test_fd_m3180125_universe_shadow_forward.py
tests/test_fd_m3180125_universe_shadow_live.py
tests/test_fd_m3180125_universe_shadow_isolation.py
tests/test_fd_m3180125_universe_shadow_zero_impact.py
```

This implementation obeys the frozen contract
`FD-M3180125_SP500_UNIVERSE_VERSIONING_UV_STEP_1_CONTRACT_v1.0_FROZEN_2026-08-10.md`.

Hard boundaries:

- Membership resolution consumes a Runtime-supplied `expected_execution_date`; it never calculates the next trading day.
- Forward and Live share only pure code/schema. Their events, registries, snapshots, state, price preparation and Official artifacts are physically separate.
- UV-step-2 cannot modify Engine, Adapter, Runtime, Workflow, Dashboard, accounts, ledgers, orders, fills, daily artifacts, `data/fw_prices`, or `data/live_prices`.
- Existing 5Y, Forward, Live, Legacy and Screening history is immutable.
- New-price preparation remains staged under the corresponding track and is not published to a production price directory.
- Live `next_weekday()` remains rejected and is a hard block before UV-step-3 Live integration.
- The UV-step-2/3 implementation authorizes no production activation, commit,
  push, 5Y run, Forward run, Live run, network request, or price update.
  UV-step-4 separately authorizes only controlled Membership activation; its
  installer still authorizes none of those production runs or updates.

## UV-step-3 — Forward and Live Shadow Integration

UV-step-3 is an explicit, default-off, read-only observation path.  Forward
resolves track-local Membership once for every real
`ForwardDatePlanner` planned execution date.  Live resolves only after the
hash-pinned Live Calendar Hard Gate returns the real
`expected_execution_date`.  Neither result is injected into production
composition, Engine, Adapter, T1 execution, recommendations, orders, fills,
account, ledgers, prices, Membership current state, Workflow, or Dashboard.

When the synchronized Forward runtime has no pending planned date, the
explicit acceptance probe may re-observe only its exact, data-backed
`last_committed_date`.  That date is an already accepted
`ForwardDatePlanner` date, not a newly inferred weekday or fabricated input;
the evidence marks it as
`CURRENT_LAST_COMMITTED_FORWARD_DATE_PLANNER_DATE`.  This rule exists only
to make the read-only acceptance probe possible and does not replay or commit
Forward production.

Forward and Live share only pure code/schema/hash rules.  Their baseline
observations, events, resolved snapshots, price-readiness observations,
run ids, evidence, and acceptance results remain physically separate.
Cross-track read/write, symlink paths, invalid dates, immutable conflicts, or
any protected production-manifest change must fail closed with the applicable
`HOLD_UV_STEP_3_*_SHADOW` decision and no fallback.

The only UV-step-3 mutation is one deterministic, atomically published
evidence directory under the invoking track's approved shadow root.  Shadow
mode requires the explicit `--uv-shadow-probe` entry; ordinary Forward and
Live behavior remains unchanged.  Successful UV-step-3 acceptance means
`SHADOW ACCEPTED / PRODUCTION INACTIVE` only.  Production activation remains
reserved for separately authorized UV-step-4.

## UV-step-4 — Controlled Production Membership Enforcement

UV-step-4 promotes the accepted track-local Membership result into a narrow
production control: only `BUY` and `ADD` may increase risk, and only when the
symbol belongs to the execution-date-effective Membership and is price-ready.
`HOLD`, `REDUCE`, and `EXIT` remain available for an existing position after
Membership deletion; deletion never creates an automatic exit.  Required
market data is therefore the union of eligible-entry symbols, held symbols,
and required indices.

Forward and Live have independent, hash-validated `OFF`/`ENFORCE` pointers.
Absence of a pointer means `OFF` and preserves the pre-UV-step-4 path exactly.
`ENFORCE` never falls back silently: missing/tampered snapshots, omitted
effective events, unavailable held-symbol data, path aliasing, or an ineligible
pending/recommended `BUY`/`ADD` causes a track-specific HOLD before execution
or recommendation publication.  A mode change is atomic, is recorded as
immutable track-local evidence, and may be rolled back per track without
deleting snapshots or history.

UV-step-4 does not acquire Membership events, modify strategy/ranking/sizing/
exit logic, connect Live to a broker, alter prices, rewrite 5Y or historical
artifacts, or add Workflow/Dashboard behavior.  Full frozen authority,
whitelist, installation sequence, failure gates, and acceptance requirements
are defined in
`FD-M3180125_SP500_UNIVERSE_VERSIONING_UV_STEP_4_CONTRACT_v1.0_FROZEN_2026-08-22.md`.
