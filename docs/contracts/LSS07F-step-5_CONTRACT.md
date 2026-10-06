# LSS07F-step-5 — Frozen Engine integration (disabled)

Authorized 2026-10-05. Scope: v13 shared E1RCoreEngine formal raw-history entry.
Market State, Regime, Gate and trade logic remain inside the same Engine.
Forward/Live accounts, inputs and execution remain independent.

## Contract

LSS07-SP500-FROZEN-1.0: score < 60; ordinal rank > 150; six consecutive market
sessions score OLS slope < 0 and rank-fraction OLS slope > 0. Rank fraction is
(rank-1)/(N-1), zero for singleton; stable alphabetical tie order. All score
formulas are reused from the formal UptrendSignalAdapter, including SIDEWAYS
holdings; Sideways reference-list scores are not substituted for Leader Score.
Current track snapshot universe is used for the six historical observations;
this is not a new point-in-time universe reconstruction or a change to BUY ranking.

If adjusted close > previous market-session adjusted close, defer only this
rule for today. Equal close is not a repair. Re-evaluate next day without a
cooldown or waiting budget. Full remaining EXIT can bypass MinHold and does not
require profit. Preserve canonical full EXIT/CAPPED-ATR and same-symbol BUY/ADD.
No portfolio or account mutation; original BUY intents and sizing are retained.
Formal EXIT processing sells then releases capital under the existing execution
contract. Live advice does not constitute a fill.

Default LSS07Config(enabled=False, effective_signal_date=None). Enabling requires
an explicit effective SIGNAL date. Disabled/pre-effective calls return the
original finalized Engine result without calculating LSS07 history.
Legacy frozen 5Y entry is unchanged. No configuration, workflow, ledger, prices,
account state or historical report is rewritten. Existing positions' cost,
quantity and entry date are preserved. Required history may predate activation;
this supplies features and does not create retrospective orders.

Missing six-session inputs suppress only the new LSS07 overlay with explicit
DATA_NOT_READY evidence; they never silently relax the thresholds. Step-6 must
verify readiness before activation. Unexpected programming errors are not
swallowed. Historical score observations are recomputed from dated bars, with
no mutable process cache, no prior invocation requirement and no frozen research
runtime dependency. Future dates are excluded.

## Boundary and tests

Production modifications: core.py's default config and formal-entry hook;
new lss07.py. Tests and frozen fixtures/documentation are the other installed
files. CAPPED-ATR is finalized before the extra EXIT overlay so its EXIT has
priority. Do not patch the old research leader_rank_all bug into unrelated code.

Bounded tests: frozen recorded policy observations; two historical real feature
targets NET/SNDK; strict thresholds/repair/priority/minhold/missing data; disabled
whole-result equivalence against pre-change core; T+1 fractional full EXIT and
stable pending identity; Live recommendation translation and immutable account;
restart determinism. No 5Y or portfolio optimization run.

The Live/Forward adapter tests exercise the existing execution boundaries using
controlled inputs; they do not claim production activation or full-ledger retry
acceptance. Step-6 owns effective-date selection, each track's configuration
wiring, existing pending-order boundary, first production-day evidence and
shutdown procedure. Step-5 does not set an effective date or start either track.

## Installation and recovery

Installer verifies current main/origin/main and exact reviewed source hashes.
A newer data-only commit is allowed if source lock still matches. Source changes,
local edits, unknown file collisions or a failed check stop before overwriting.
Tests run outside the formal repository. Only listed code/test/docs files are
installed, committed and pushed; no force-push, reset, clean or historical replay.

A failed install preserves logs and backups. Never restore an old account snapshot
to roll back code. Before Step-6, reverting the installation commit is sufficient
if needed; once activated, pending advice/orders require explicit handling first.

## V1.1 installer clarification (2026-10-05)

Preserve the exact reviewed pre-existing local changes from the returned V1.0
evidence, including the one modified Forward automation JSON. Capture SHA256,
size, mtime and Git status before installation; verify them unchanged afterward.
Never stage/commit these files. Reject staged changes and any unreviewed local
path. Full-repository cleanliness is not claimed when old files remain.
Completion requires task_scope_clean plus preexisting_local_files_preserved,
commit/push and HEAD=origin/main; working_tree_clean is reported truthfully.
All strategy source, fixtures and tests are byte-identical to V1.0.

## V1.2 — preserved links

Existing allowlisted leaf symlinks are recorded using lstat/readlink; targets are
not read or executed, including dangling virtualenv links. Parent symlinks and
installation-target symlinks remain prohibited. Link target/type changes fail
preservation checks. Twelve installer regression cases passed. Strategy source
and frozen tests unchanged. Previous attempt stopped before tests/installation.

## V1.3 — RCA-led aggregate preflight

Before installation, collect independent repository, identity, source-lock and
local-file blockers into PREFLIGHT_REPORT.json. No production file writes on
preflight failure. Preserve distinct install-target and existing-file policies.
Fifteen focused installer tests passed, including a synthetic replica of all
10,781 evidenced local paths and virtualenv links. No strategy or test-fixture
changes; no production activation. See package RCA.md for facts and unknowns.
