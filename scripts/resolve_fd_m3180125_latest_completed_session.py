#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from e1r_engine.live_calendar import load_live_trading_calendar


CALENDAR_PATH = Path("config/live_calendar/us_equity_calendar_v1.0.json")
MARKET_TIMEZONE = ZoneInfo("America/New_York")
COMPLETED_SESSION_CUTOFF = time(18, 0)


def latest_completed_session(as_of_utc: datetime) -> str:
    if as_of_utc.tzinfo is None:
        raise ValueError("as_of_utc must be timezone-aware")
    calendar = load_live_trading_calendar(CALENDAR_PATH)
    local = as_of_utc.astimezone(MARKET_TIMEZONE)
    candidate = local.date()
    if not (
        calendar.is_session(candidate)
        and local.time().replace(tzinfo=None) >= COMPLETED_SESSION_CUTOFF
    ):
        candidate -= timedelta(days=1)
    while not calendar.is_session(candidate):
        candidate -= timedelta(days=1)
    return candidate.isoformat()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of-utc")
    args = parser.parse_args()
    as_of = (
        datetime.fromisoformat(args.as_of_utc.replace("Z", "+00:00"))
        if args.as_of_utc
        else datetime.now(timezone.utc)
    )
    print(latest_completed_session(as_of))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
