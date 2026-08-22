# FD-M3180125 S&P 500 Source Automation — SA-step-1 Contract v1.1

```text
Frozen: 2026-08-22
Scope: SA-step-1 ONLY — OFFICIAL SOURCE MONITORING AND CHANGE DETECTION
Predecessor: UV-step-4 COMPLETE / FORWARD AND LIVE ACCEPTED
Production membership impact: NONE
```

## Purpose

Monitor the S&P Global official Press Releases RSS every
calendar day, discover standard S&P 500 membership announcements, preserve the
raw source immutably, and extract candidate ADD/REMOVE facts without creating a
Membership Event or changing any production Universe.

## Frozen source and trust boundary

- Primary source: `https://press.spglobal.com/index.php?s=2429&pagetemplate=rss`.
- Only HTTPS RSS and article documents on S&P Global-controlled hosts are
  accepted: `press.spglobal.com`, or `spglobal.com` / `www.spglobal.com`
  beneath `/spdji/en/`.
- The blocked S&P DJI Media Center page remains an allowed manual/future source,
  but it is not the scheduled acquisition endpoint.
- PR Newswire's S&P Dow Jones Indices issuer channel may be added later as an
  explicitly tested transport fallback. It is not authoritative input in
  SA-step-1 v1.1.
- Wikipedia may be used only for reconciliation alerts; it cannot establish an
  announcement, effective date or Membership Event.
- Yahoo Finance is only the downstream price provider and provider-symbol
  validator. It cannot establish S&P 500 membership or an effective date.
- Standard S&P 500 membership changes are in scope.
- Equal Weight, ESG, Scored & Screened, Capped, consultations, methodology and
  other index products are out of scope.
- Network failure, an empty/changed landing page, missing PDF extraction, or an
  incomplete parse is `SOURCE_HOLD`; it MUST NOT be recorded as no change.

## Frozen output

All runtime writes are isolated under:

```text
data/sp500_source_monitor/
```

Each source document records the canonical URL, raw bytes, SHA-256, UTC fetch
time, title, content type, parser version, candidate facts and failure codes.
The source hash determines `source_id`; repeated identical input is idempotent.

Candidate facts preserve the official symbol exactly as `official_symbol`.
SA-step-1 MUST NOT infer, normalize or test a Yahoo `provider_symbol`.

## Schedule

The independent workflow runs every calendar day at `22:15 UTC`, before the
existing `23:30 UTC` Forward and Live workflows. It may also be dispatched
manually. The initial implementation push triggers the first run;
subsequent source-evidence-only commits do not recursively trigger it. It
commits only the isolated source-monitor evidence path.

GitHub Actions is the authoritative acquisition runtime. Mac installation
validates source contracts and code but does not require S&P network access;
the accepted Mac egress currently receives HTTP 403 / connection reset. A
future application may add a separate Mac provider or transport contract.

This timing does not connect the result to production; that handoff belongs
exclusively to SA-step-3.

## Acceptance

1. Official-domain and path allowlist is enforced.
2. Target membership announcements are selected; derivative products are rejected.
3. Known replacement language yields paired ADD/REMOVE candidates.
4. Official symbols, including punctuation, are preserved.
5. Raw documents and detections are immutable and hash-addressed.
6. Repeat runs are idempotent.
7. All acquisition or parsing uncertainty produces durable HOLD evidence.
8. No Membership Event, Snapshot, Yahoo mapping, price update, Forward, Live,
   5Y, Engine, account, ledger, Dashboard, broker, commit or push occurs during
   installation and acceptance.

Completion status is permitted only after isolated tests and an official-source
read-only probe pass in the authoritative GitHub Actions runtime:

```text
SA-step-1 = COMPLETE / OFFICIAL SOURCE MONITORED /
CHANGES DETECTED / PRODUCTION INACTIVE
```
