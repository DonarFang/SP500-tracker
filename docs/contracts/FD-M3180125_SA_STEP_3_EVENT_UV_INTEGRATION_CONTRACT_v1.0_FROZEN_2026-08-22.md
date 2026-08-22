# FD-M3180125 SA-step-3 Event and UV Integration Contract v1.0

Status: FROZEN — 2026-08-22

SA-step-3 consumes only a successful SA-step-2 verification whose official-source,
effective-date, change-pair, identity, and Yahoo mapping semantics are unique.

It creates one deterministic immutable Membership Event and publishes byte-independent
copies to the Forward and Live Event stores. A verified ADD must have at least 252 valid
Yahoo daily rows before either Event is published. Any mapping, identity, price, source,
date, duplicate-semantic, storage-link, or cross-track ambiguity is HOLD and requires
manual intervention.

Forward and Live remain physically isolated. Each track resolves and publishes its own
snapshot for the exact execution date. Before the effective date the old member remains;
on and after the effective date the addition is eligible only when data-ready and the
deletion cannot receive BUY/ADD. Existing holdings remain manageable by HOLD, REDUCE,
or EXIT.

SA-step-3 may write only the added symbol's Forward/Live price files, track-local Events,
track-local snapshots/current pointers, and SA-step-3 audit evidence. It does not run the
Engine, place broker orders, rewrite 5Y, change strategy logic, modify accounts/ledgers,
or rewrite historical Forward/Live results.
