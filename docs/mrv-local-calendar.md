# MRV step 4 — local calendars and annual preparation v1.4

Daily predictions use a local official calendar. CPI, Employment Situation (NFP), and FOMC decision release days alone trigger the existing severe override. LINEAR4, calibration, trading engine, and prediction history remain frozen.

## Automatic timing

The existing MRV Daily Observation workflow performs calendar maintenance. Based on America/New_York time, it checks the current year every 14 days. Starting with the first daily run in November of each year, it also attempts to acquire the next year's official calendar; each year has its own 14-day attempt clock. There is no additional scheduler or account. Failure is not retried on every daily run. An explicit local --force command is available. If the next-year calendar is still missing after January, current-year acquisition continues on the same 14-day cadence.

## Acquisition and activation

BLS: https://www.bls.gov/schedule/{year}/home.htm
Fed: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm

Validate complete annual HTML, year, timezone, unique events and known event types. For a first automatic import, require CPI and NFP dates in all twelve months and eight regular FOMC decisions. These are conservative bootstrap gates, not an assertion that every actual year must contain those counts. Partial publication, cancellations, unusual meetings, or schema changes require manual review; the system never invents a missing date. Existing calendar changes are retained as a diff/candidate for manual approval, with active dates unchanged. Unchanged reviews renew verification. Saved source HTML and hashes allow inspection.

Before a new year is activated, verify frozen artifacts and 199-day golden outputs, probability availability, shared trading-calendar full-year coverage, first-session/previous-session mapping, 70-session feature windows spanning years, no use of target-day prices, and event override behavior. These are engineering and synthetic checks, NOT proof of future predictive performance. Cache compatibility only for the same frozen model manifest, trading-calendar bytes and runtime code hashes; relevant changes invalidate it.

Select the approved calendar by target trading year (not by today's year). The 2026-only hard stop is replaced by validated year coverage and compatibility gates. Existing 2026 active.json/review-state.json are reused; future years use data/mrv/event-calendar/years/{year}/. The packaged seed remains 2026 only. No fabricated or synthetic 2027 calendar is installed.

## Dashboard and failure behavior

Show local verification date/coverage and, from November, next-year preparation status, error and next attempt. exports/mrv/calendar-preparation.json is fetched independently so preparation status remains available when daily prediction is blocked. A failed next-year attempt does not invalidate the current-year forecast. An overdue current-year review warns but retains the approved local dates within coverage (user-approved policy). Unknown target-year coverage blocks a new forecast. Old predictions remain labelled as old records.

BLS 403 is NOT fixed by this update. Use manual import if official network acquisition remains unavailable. The shared Forward/Live trading calendar is unchanged and currently ends 2028-12-31. Preparation for 2029 will report insufficient trading-calendar coverage rather than claiming readiness. Extending that shared artifact needs its own verified update; no trading calendar is fabricated.

## Manual fallback

    cd ~/Downloads/sp500-tracker-v13
    git pull --ff-only
    python3 scripts/mrv/event_calendar.py --year 2027 --force

If blocked, save complete official annual BLS and Fed HTML pages in your browser, then:

    python3 scripts/mrv/event_calendar.py --year 2027 --bls-file /absolute/path/bls.html --fed-file /absolute/path/fed.html

For a changed/atypical candidate, inspect the printed candidate.json and sibling changes.json against official announcements, then approve:

    python3 scripts/mrv/event_calendar.py --year 2027 --approve data/mrv/event-calendar/reviews/REPLACE_WITH_REPORT_FOLDER/candidate.json

The year argument prevents accidental approval of a different year's calendar. Approval also enforces engineering compatibility. Verification dates older than 14 days are not accepted for approval. Recheck sources instead of editing timestamps.

    git add -- data/mrv/event-calendar
    git commit -m 'MRV: verify annual official event calendar'
    GIT_TERMINAL_PROMPT=1 git -c http.version=HTTP/1.1 -c credential.helper= push origin HEAD:main

Then run MRV Daily Observation. Cloud review states are committed by the existing workflow. Daily evidence includes event-calendar-used.json, calendar-health.json and annual-calendar-status.json. Original prediction records are never rewritten.

## Acceptance and scope

Installer syntax, frozen-model checks, synthetic 2026→2027 daily pipeline, failure/partial coverage tests, and install/push/idempotence tests passed in development. User's actual cloud run and eventual real next-year source acquisition remain separate acceptance gates. No paid provider, FRED registration, new Python dependencies, model training or Forward/Live changes.
