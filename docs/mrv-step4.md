# MRV step-4 v1.0 — frozen daily observation

## Contract

LINEAR4_T2021_2022 and its strict score > 0.026803055017853218 severe threshold are unchanged. Nonsevere grades inherit M7 light, otherwise moderate. Four inputs: frozen M7 and M6 plus saved annual-2026 I7R/I6V; no fitting, threshold search or calibration runs in production. The saved P2_BETA FINAL maps the LINEAR4 score to three mutually exclusive probabilities. These are observation estimates; limited severe samples prevent claims of certified tail accuracy. Probability failure does not change the grade.

D=max(0,1-SPX target regular-session low / SPX T close). Severe D>=.03, moderate .012<D<.03, light D<=.012. The target is the next session from the existing hash-locked US equity calendar, including holidays. No premarket features. Scheduled CPI, Employment Situation/NFP, and FOMC decision release days alone force final severe; no next-day/minutes/non-trading-day shifts. Calendar override never forces 100% probability. Model and final grades remain separate.

## Frozen artifact lineage

Base M7/M6: reviewed daily step3 models. I7R/I6V: saved annual-2026 models from evidence(20261031-074527).zip. LINEAR4: same step3 package; exact SHA256 0762118c3935fb68b3360cc282683279c8fc2c3f7687c48b6078750ca9ef4cd8. P2_BETA: models/FINAL/P2_BETA.json from evidence(20261031-084427).zip. Model/vendor identities are in config/mrv/manifest.json. Golden fixtures are historical verification data, never live fallbacks.

Annual-2026 bottom models are authorized only for 2026 target dates. The runtime blocks 2027 targets pending a separately reviewed annual artifact; it does not silently refit or extend validity. The existing exchange calendar is not edited.

## Data and timing

Independent Yahoo daily unadjusted SPX/VIX OHLC, CBOE VIX9D/VIX3M daily closes, BLS annual release schedule and Fed annual meeting panel. These EOD proxies are not certified exchange tick feeds. Data-ready gate is 18:00 America/New_York (including early-close days); this is a processing cutoff, not the market closing time. Forecast features use the latest completed session's 70-session history; missing rows cannot be forward-filled. BLS requires all 12 CPI and 12 NFP records; Fed requires eight reviewed two-day scheduled meeting entries. Unexpected schedule structure blocks output for review. Runtime attempts fresh official calendars each run. BLS tries its official ICS subscription first, then the annual HTML page. If both are unavailable, a previously validated official raw snapshot may be reused for at most 72 hours; target opening must be within that validity window. Reuse never renews retrieval time. Dashboard discloses cached status. Expired, missing, corrupt or incomplete calendars block output.

The module reports the original creation timestamp. A forecast first generated after target opening is LATE_RECONSTRUCTION, never prospective evidence. Before-open snapshots are collected at their actual timestamp, not asserted to have existed exactly at T close. Weekend runs retain T and target unless source revisions change the result.

## Paths and interfaces

- scripts/mrv/run.py: stdlib-only daily CLI and offline `--self-test`.
- config/mrv/: immutable model artifacts, vendor lock and golden tests.
- exports/mrv/latest.json: latest valid computation; status.json: independent last-attempt health.
- exports/mrv/predictions/YYYY-MM-DD.json: immutable first record per target.
- exports/mrv/revisions/TARGET/HASH.json: subsequent changed computations; original preserved.
- exports/mrv/actuals/DATE.json: first observed mature actual label, with source and recording time; never overwrite.
- exports/mrv/history.json: first-record history with mature labels; not a performance acceptance report.
- data/mrv/snapshots/PREDICTION_ID/: compressed raw public sources and provenance for each new computation.
- dashboard/mrv-risk.js and .css: independent read-only view below the real overview index-card grid. No app.js, strategy or trading data changes.
- .github/workflows/mrv-daily.yml: 23:15 UTC weekdays, 02:15/06:15 UTC recovery next mornings; shared production-writer concurrency. Explicit MRV paths only. Pages workflow additionally listens for MRV completion.

Default local evidence root: ~/UEIS-MRV/reports/step4/. GitHub Actions writes evidence to runner temporary storage and uploads it as an Actions artifact. Public raw source snapshots remain in the repository. Evidence ZIPs omit unrelated local files and credentials.

## Install and publication

The installer checks main, tracked cleanliness, exact origin and critical interface hashes. Unrelated untracked files are preserved; collisions stop the install. It permits only fast-forward sync, backs up the two modified existing files, writes a declared file set, runs 199 historical score/grade checks, then fetches live inputs and computes a forecast. No pip/system package changes.

By default, only after live computation succeeds does it explicitly stage the MRV file set, commit and push. `--local-only` performs local install/compute without commit/push. A concurrent remote push may cause non-fast-forward rejection; preserve the evidence and review it. There is no force-push, reset, git clean, destructive rollback, automatic rebase or blanket git add. A failure preserves state and evidence and does not claim successful installation/publication. This installer is a one-time integration, not an overwrite/reinstall tool; already-installed or modified source stops for review.

## Daily commands

```
cd ~/Downloads/sp500-tracker-v13
python3 scripts/mrv/run.py --self-test
python3 scripts/mrv/run.py
```

Local daily runs write observations but do not commit/push automatically. GitHub Actions owns routine public updates after installation.

## Acceptance and next action

Developer checks reproduce all 199 step3 2026 four-score/LINEAR4 grade rows, 117 raw-history feature rows (1,638 values), calendar boundaries, no target-price leakage, required-data failures, event independence of probabilities, and immutable archives. See developer-validation.json. This does not certify live provider availability on the user's Mac or GitHub Pages deployment.

Step5 must review the user's installation evidence; confirm the first real T/target, score, grade, probability, calendar sources, exact commit and Pages workflow; inspect the dashboard and at least one scheduled update/retry, stale/missing display and mature actual append. Don't declare step4 online acceptance or trading authority from offline PASS alone. Continue daily observation; do not expand model research or change grades based on probabilities.

## 2026-10-31 v1.1 recovery / RCA

User evidence: evidence(20261031-103518).zip. Local v13 fast-forwarded from eaeb85de3 to b717963e7; 199-day replay passed exactly. 25 integration files were written; daily run failed on repeated BLS HTML HTTP403 before inference/commit/push. The original installer incorrectly assumed its own network success represented user-host access. Root of the server-side 403 (IP policy versus request filtering) is not established. This recovery does not disable TLS, use proxies, bypass sign-in, or scrape challenge pages.

Correction: official BLS ICS adapter, bounded verified calendar snapshot fallback, visible provenance/expiry, exact partial-install hash checks, preserved first predictions and frozen model parameters. Initial official snapshots were retrieved during this repair and are embedded with SHA256 and retrieval time. Daily refreshes replace the local calendar cache only after the full annual event set passes validation. A persistent outage beyond 72h is still BLOCKED, not a claim of no events. Network availability on the user's Mac and GitHub runners remains subject to user-run evidence.

Evidence fix: original outer manifest listed a nested evidence.zip but excluded all files named evidence.zip. Recovery excludes only its own outer ZIP and includes all nested ZIPs; final member hashes are verified after packaging. Previously omitted nested ZIP does not invalidate the 14 other matching outer manifest files or the preserved six-file daily manifest.

Run MRV-step-4-Resume-v1.1.sh once against the partially installed v13. It backs up changed files and records an exact source/output snapshot. It does not re-install or re-fit models. After a successful daily result, default mode commits and pushes only the declared MRV integration. --local-only stops before git add/commit/push. Unexpected edits, unknown MRV files, protected interface changes, conflicting remote commits or expired calendar snapshots stop for review, preserving state.

Completion is still pending the user's run, Pages deployment and step5 end-to-end review. No historical Forward/Live transactions are recalculated or modified.
