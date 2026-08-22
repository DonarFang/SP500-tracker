# FD-M3180125 Universe Versioning UV-step-4 Contract v1.0

```text
Frozen: 2026-08-22
Engine: FD-M3180125-SP500-TOP3-engine
Authority HEAD = origin/main = a3f14b45cf4e2d5746ad67d972fba4dc680904db
Required predecessor = UV-step-3 v1.1 COMPLETE / SHADOW ACCEPTED / PRODUCTION INACTIVE
Authorization = IMPLEMENT + VALIDATE + CONTROLLED FORWARD/LIVE ACTIVATION
```

## 1. Purpose and completion target

The sole purpose is to make the accepted, execution-date-effective,
track-local Membership authoritative for production `BUY` and `ADD` risk
increases while preserving management of existing positions.

Completion target:

```text
UV-step-4 = COMPLETE / FORWARD AND LIVE PRODUCTION MEMBERSHIP ENFORCED
```

This status is permitted only after installation, the full acceptance suite,
both independent activation probes, protected-manifest equivalence, and
rollback verification pass on the Mac Authority.

## 2. Frozen production semantics

For track `x` and execution date `t`:

```text
EligibleBuyUniverse[x,t]
  = EffectiveMembership[x,t] ∩ PriceReady[x,t] - Quarantined[x,t]

RequiredDataUniverse[x,t]
  = EligibleBuyUniverse[x,t] ∪ CurrentHoldings[x,t] ∪ RequiredIndices[x]
```

- `BUY`/`ADD` outside `EligibleBuyUniverse` MUST HOLD before execution or
  recommendation publication.
- `HOLD`/`REDUCE`/`EXIT` remain allowed for held deleted members.
- Membership deletion MUST NOT synthesize `EXIT`.
- Missing price data for a held symbol MUST HOLD; it may not be hidden by
  dropping the position from required data.
- Forward uses each actual `ForwardDatePlanner` execution date.
- Live uses only the Calendar Hard Gate `expected_execution_date`.
- Any invalid authority, date, hash, pointer, snapshot, event completeness,
  track isolation, symlink, hardlink, or required-data condition MUST HOLD.
- `OFF` is the default when no mode pointer exists and MUST preserve the exact
  accepted pre-step-4 production path.
- `ENFORCE` has no permissive or static-universe fallback.

The UV activation boundary inherited from UV-step-1 is
`2026-08-10T00:00:00Z`.  Events wholly before that boundary are represented by
the preserved activation baseline; later applicable events must be present in
the current immutable snapshot.

## 3. Track isolation, activation, and rollback

Forward and Live share pure code only.  Each has separate events, snapshots,
current pointer, mode pointer, mode-change evidence, and runtime inputs.

- Forward and Live activation is independent.
- Each mode transition is written as immutable track-local evidence, then the
  hash-validated mode pointer is atomically replaced.
- Installer failure restores source and both pre-install track states.
- Operational rollback changes only the selected track to `OFF`; it never deletes
  events, snapshots, evidence, prices, accounts, ledgers, or history.
- Initial activation baseline is the accepted track's current production
  catalogue.  UV-step-4 does not fetch or infer new S&P events.

## 4. Exact source whitelist

Only these paths may change or be added:

```text
docs/canonical/FD-M3180125_SP500_UNIVERSE_VERSIONING_CONTRACT.md
docs/canonical/FD-M3180125_SP500_UNIVERSE_VERSIONING_UV_STEP_4_CONTRACT_v1.0_FROZEN_2026-08-22.md
src/e1r_engine/universe_versioning/production_integration.py
src/e1r_engine/forward_orchestrator.py
src/e1r_engine/live_composition.py
scripts/run_engine_forward_daily.py
scripts/run_fd_m3180125_live_daily.py
scripts/activate_fd_m3180125_universe_production.py
tests/test_fd_m3180125_universe_production_contract.py
tests/test_fd_m3180125_universe_production_gate.py
tests/test_fd_m3180125_universe_production_forward.py
tests/test_fd_m3180125_universe_production_live.py
tests/test_fd_m3180125_universe_production_isolation.py
tests/test_fd_m3180125_universe_production_zero_impact.py
```

Core Engine, strategy, Adapter logic, account/ledger semantics, price update,
5Y, historical outputs, Workflow, Dashboard, deployment, and broker connectivity
are protected and outside the whitelist.

## 5. Acceptance standard

The frozen suite is:

```text
UV-step-2 regression                 53/53 PASS
Live Calendar Hard Gate             12/12 PASS
UV-step-3 Shadow Integration         30/30 PASS
UV-step-4 Production Integration     24/24 PASS
Total                               119/119 PASS
```

The 24 UV-step-4 gates cover exactly six groups: contract/authority, core
production gate, Forward pre-execution behavior, Live pre-publication behavior,
track isolation/mode control, and zero strategy/history impact.

Mac acceptance additionally requires:

1. precondition `HEAD = origin/main = a3f14b45...` and exact accepted
   UV-step-3 overlay;
2. changed paths equal the 14-path whitelist;
3. stage and installed suites each report `119/119 PASS`;
4. `OFF` proves pre-step-4 output-path equivalence;
5. Forward activation and Live activation each pass independently;
6. an ineligible Forward pending `BUY/ADD` holds before T1 execution;
7. an ineligible Live `BUY/ADD` holds before recommendation commit;
8. a held deleted member remains in required data and can reduce/exit;
9. independent rollback is exercised and both tracks are finally restored to
   `ENFORCE` only after successful verification;
10. protected 5Y, Forward/Live account/ledger/recommendation/runtime history,
    and price manifests are byte-identical before and after;
11. zero production run, zero backtest, zero price update, zero broker call,
    zero commit, and zero push during installation/acceptance.

Any unmet item yields `HOLD_UV_STEP_4` and forbids completion status.

## 6. Explicit non-goals

No automatic event-source acquisition or verification; no Point-in-Time 5Y
rewrite; no strategy optimization; no ranking, sizing, stop, REDUCE, or EXIT
change; no Workflow/Dashboard expansion; no broker execution; and no alteration
of canonical historical evidence.
