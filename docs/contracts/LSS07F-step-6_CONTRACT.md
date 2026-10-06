# LSS07F-step-6 — production opt-in, frozen strategy

Authorized scope: SP500 v13 Forward and Live, shared E1RCoreEngine.
Step-5 accepted at commit 53459d6ea9ae44493a0b6815d309525d861f3e48.
Strategy LSS07-SP500-FROZEN-1.0 remains byte-identical. No changes to Regime,
Market State, Gate, BUY/ADD, canonical exits, MinHold exceptions or execution.

## Configuration and boundary

config/lss07/production_v1.json is the single opt-in record for both formal
compositions. An explicit future US trading SIGNAL date is required. It must
be later than the current New York date, both last-committed market dates and
existing Live transactions/advice. Dates are validated with the existing frozen
US equity calendar. Earliest execution is the following session. Delayed runs
must use a future date, never silently backdate. Both tracks use that same date.

Production composition factories inject E1RCoreEngineConfig(lss07=...) only for
the exact official runtime roots in the same checkout. Core default remains
OFF. Unactivated Live acceptance and research/temporary roots remain OFF.
No workflow is manually dispatched or changed by this installation. Existing
daily workflows will consume the published configuration on their next checkout.

Already existing positions keep cost, quantity, entry date and origin. Existing
pending Forward orders and Live advice/confirmed transactions are unchanged.
An old signal executed after the effective date retains its original identity;
activation does not cancel, replace, reprice or relabel it. New LSS07 signals
begin at or after the effective date and follow existing T+1 execution.

## No historical rewrite

Installer does not call any daily runner, initialize or replay an account,
rebuild equity, download prices, write trade ledgers, or invoke a broker. Existing
5Y, Forward and Live records are protected before and after installation. Normal
future workflow catch-up can still process previously uncommitted sessions;
pre-effective sessions retain baseline decisions. Already committed sessions
remain covered by existing no-repeat/immutable daily contracts.

## Readiness, evidence and scope

Read-only readiness runs frozen six-session feature extraction using latest
Forward prices and accepted adjusted Live prices. It checks current holdings and
pending candidate symbols, with three sample symbols when an account has none.
It reads Live cycle events for symbols only and does not rebuild/rewrite accounts.
Readiness uses current price-eligible universe; the production Universe Gate and
actual snapshot universe policy remain unchanged. Future price availability is
not guaranteed by an installation check. Missing later inputs retain frozen
LSS07 DATA_NOT_READY behavior while canonical risk management continues.

Forward already persists trace.metadata.lss07. New active Live daily advice now
also persists the same frozen summary, version and effective_signal_date.
Before activation its artifact schema remains unchanged. Existing Live advice
is never rewritten to add telemetry. These fields are advice/audit, not fills.

Ten focused deployment tests cover opt-in/disabled modes, official root scope,
configuration validation, composition injection, effective-date/account boundary,
shutdown behavior, Live new-advice audit, old-schema preservation and no repeat
of committed Live dates. Original Step-5 19 tests are reused as accepted evidence;
no portfolio backtest and no parameter search.

Completion is reported separately: PASS_INSTALLED_SCHEDULED requires installation,
commit, push, HEAD==origin/main, task_scope_clean, and protected records unchanged.
PASS_FIRST_PRODUCTION_DAY requires actual effective-date daily artifacts for both
tracks; installation must not claim this future evidence already exists.
verify.sh is a one-time read-only check after normal daily workflows publish the
first active session and those artifacts are present locally. It validates the
activation audit and preserves old daily artifacts, Live ledger byte prefixes and
Forward trade/equity array prefixes. It does not trigger daily runs.

## Shutdown and recovery

run.sh --disable changes only deployment.enabled to false and records disabled_at,
commits and pushes normally. It stops new overlay evaluations after loading the
new config; in-flight processes and previously generated pending orders/advice
are not canceled. Their handling remains explicit under the existing execution
process. Never restore an old account state or delete history to disable LSS07.
Re-enabling an explicitly disabled deployment requires a new reviewed date plan.

Push failure leaves the local commit/config intact and reports its true state.
The same installation command can resume publishing exactly that single verified
commit if origin/main remains its parent; it never force-pushes or auto-merges.
Existing Step-5 allowlisted local materials remain unchanged and uncommitted.
