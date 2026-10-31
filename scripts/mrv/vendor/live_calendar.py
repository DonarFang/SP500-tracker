from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
from typing import Any, FrozenSet


CALENDAR_ID = "FD-M3180125_US_EQUITY_LIVE_CALENDAR_V1"
SCHEMA_VERSION = "1.0"
MARKET_TIMEZONE = "America/New_York"
PRIMARY_SOURCE = "https://www.nyse.com/trade/hours-calendars"
CROSS_CHECK_SOURCE = "https://www.nasdaqtrader.com/trader.aspx?id=calendar"
EXPECTED_ARTIFACT_SHA256 = "3831e643f82f35802b3a43cd19252832374a56b584c7287f0cdd47638a6e3044"


class LiveCalendarError(RuntimeError):
    """Fail-closed Live calendar contract violation."""


def _parse_iso_date(value: Any, field: str) -> date:
    if not isinstance(value, str):
        raise LiveCalendarError("HOLD_LIVE_CALENDAR_INVALID_%s" % field.upper())
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise LiveCalendarError(
            "HOLD_LIVE_CALENDAR_INVALID_%s" % field.upper()
        ) from error
    if parsed.isoformat() != value:
        raise LiveCalendarError("HOLD_LIVE_CALENDAR_INVALID_%s" % field.upper())
    return parsed


def _parse_date_set(value: Any, field: str) -> FrozenSet[date]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise LiveCalendarError("HOLD_LIVE_CALENDAR_INVALID_%s" % field.upper())
    if value != sorted(set(value)):
        raise LiveCalendarError("HOLD_LIVE_CALENDAR_NONCANONICAL_%s" % field.upper())
    return frozenset(_parse_iso_date(item, field) for item in value)


@dataclass(frozen=True)
class LiveTradingCalendar:
    coverage_start: date
    coverage_end: date
    full_day_closures: FrozenSet[date]
    early_close_sessions: FrozenSet[date]
    extraordinary_full_day_closures: FrozenSet[date]

    def _require_covered(self, day: date) -> None:
        if day < self.coverage_start or day > self.coverage_end:
            raise LiveCalendarError("HOLD_LIVE_CALENDAR_COVERAGE_INSUFFICIENT")

    def is_session(self, day: date) -> bool:
        self._require_covered(day)
        closures = self.full_day_closures | self.extraordinary_full_day_closures
        return day.weekday() < 5 and day not in closures

    def next_session(self, market_date: date) -> date:
        self._require_covered(market_date)
        if not self.is_session(market_date):
            raise LiveCalendarError("HOLD_LIVE_MARKET_DATE_NOT_TRADING_SESSION")
        candidate = market_date + timedelta(days=1)
        while True:
            self._require_covered(candidate)
            if self.is_session(candidate):
                return candidate
            candidate += timedelta(days=1)


def load_live_trading_calendar(path: Path) -> LiveTradingCalendar:
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise LiveCalendarError("HOLD_LIVE_CALENDAR_MISSING_OR_UNREADABLE") from error
    if hashlib.sha256(raw).hexdigest() != EXPECTED_ARTIFACT_SHA256:
        raise LiveCalendarError("HOLD_LIVE_CALENDAR_HASH_MISMATCH")
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise LiveCalendarError("HOLD_LIVE_CALENDAR_INVALID_JSON") from error
    if not isinstance(payload, dict):
        raise LiveCalendarError("HOLD_LIVE_CALENDAR_INVALID_ROOT")
    expected_identity = {
        "calendar_id": CALENDAR_ID,
        "schema_version": SCHEMA_VERSION,
        "market_timezone": MARKET_TIMEZONE,
        "primary_source": PRIMARY_SOURCE,
        "cross_check_source": CROSS_CHECK_SOURCE,
    }
    for field, expected in expected_identity.items():
        if payload.get(field) != expected:
            raise LiveCalendarError("HOLD_LIVE_CALENDAR_IDENTITY_MISMATCH_%s" % field.upper())
    coverage_start = _parse_iso_date(payload.get("coverage_start"), "coverage_start")
    coverage_end = _parse_iso_date(payload.get("coverage_end"), "coverage_end")
    if coverage_start >= coverage_end:
        raise LiveCalendarError("HOLD_LIVE_CALENDAR_INVALID_COVERAGE")
    full_day_closures = _parse_date_set(
        payload.get("full_day_closures"), "full_day_closures"
    )
    early_close_sessions = _parse_date_set(
        payload.get("early_close_sessions"), "early_close_sessions"
    )
    extraordinary = _parse_date_set(
        payload.get("extraordinary_full_day_closures"),
        "extraordinary_full_day_closures",
    )
    all_listed = full_day_closures | early_close_sessions | extraordinary
    if any(day < coverage_start or day > coverage_end for day in all_listed):
        raise LiveCalendarError("HOLD_LIVE_CALENDAR_DATE_OUTSIDE_COVERAGE")
    if full_day_closures & early_close_sessions:
        raise LiveCalendarError("HOLD_LIVE_CALENDAR_CLOSE_CONFLICT")
    if extraordinary & early_close_sessions:
        raise LiveCalendarError("HOLD_LIVE_CALENDAR_OVERRIDE_CONFLICT")
    calendar = LiveTradingCalendar(
        coverage_start=coverage_start,
        coverage_end=coverage_end,
        full_day_closures=full_day_closures,
        early_close_sessions=early_close_sessions,
        extraordinary_full_day_closures=extraordinary,
    )
    if any(not calendar.is_session(day) for day in early_close_sessions):
        raise LiveCalendarError("HOLD_LIVE_CALENDAR_INVALID_EARLY_CLOSE")
    return calendar
