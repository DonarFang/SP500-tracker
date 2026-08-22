from __future__ import annotations

import ast
from datetime import date
from pathlib import Path
import tempfile
import unittest

from e1r_engine.live_calendar import (
    LiveCalendarError,
    load_live_trading_calendar,
)


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "config/live_calendar/us_equity_calendar_v1.0.json"
RUNNER = ROOT / "scripts/run_fd_m3180125_live_daily.py"


class LiveCalendarContractTests(unittest.TestCase):
    def setUp(self):
        self.calendar = load_live_trading_calendar(ARTIFACT)

    def test_LC01_independence_day_observed(self):
        self.assertEqual(
            self.calendar.next_session(date(2026, 7, 2)),
            date(2026, 7, 6),
        )

    def test_LC02_early_close_is_session(self):
        self.assertEqual(
            self.calendar.next_session(date(2026, 11, 25)),
            date(2026, 11, 27),
        )
        self.assertTrue(self.calendar.is_session(date(2026, 11, 27)))

    def test_LC03_christmas_boundary(self):
        self.assertEqual(
            self.calendar.next_session(date(2026, 12, 24)),
            date(2026, 12, 28),
        )

    def test_LC04_normal_friday_to_monday(self):
        self.assertEqual(
            self.calendar.next_session(date(2026, 8, 7)),
            date(2026, 8, 10),
        )

    def test_LC05_missing_artifact_fails_closed(self):
        with self.assertRaisesRegex(
            LiveCalendarError, "HOLD_LIVE_CALENDAR_MISSING_OR_UNREADABLE"
        ):
            load_live_trading_calendar(Path("does-not-exist.json"))

    def test_LC06_tampered_artifact_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "calendar.json"
            path.write_bytes(ARTIFACT.read_bytes() + b"\n")
            with self.assertRaisesRegex(
                LiveCalendarError, "HOLD_LIVE_CALENDAR_HASH_MISMATCH"
            ):
                load_live_trading_calendar(path)

    def test_LC07_coverage_exhaustion_fails_closed(self):
        with self.assertRaisesRegex(
            LiveCalendarError, "HOLD_LIVE_CALENDAR_COVERAGE_INSUFFICIENT"
        ):
            self.calendar.next_session(date(2028, 12, 29))

    def test_LC08_closed_market_date_rejected(self):
        with self.assertRaisesRegex(
            LiveCalendarError, "HOLD_LIVE_MARKET_DATE_NOT_TRADING_SESSION"
        ):
            self.calendar.next_session(date(2026, 7, 3))

    def test_LC09_runner_has_no_weekday_fallback(self):
        source = RUNNER.read_text(encoding="utf-8")
        self.assertNotIn("next_weekday", source)
        self.assertNotIn("timedelta", source)
        self.assertIn("load_live_trading_calendar", source)
        self.assertIn("live_calendar.next_session(market_date)", source)

    def test_LC10_runner_calendar_call_precedes_composition(self):
        source = RUNNER.read_text(encoding="utf-8")
        tree = ast.parse(source)
        self.assertIsNotNone(tree)
        self.assertLess(
            source.index("load_live_trading_calendar(CALENDAR_PATH)"),
            source.index("compose_active_live_production("),
        )

    def test_LC11_2027_holiday(self):
        self.assertEqual(
            self.calendar.next_session(date(2027, 7, 2)),
            date(2027, 7, 6),
        )

    def test_LC12_2028_early_close_is_session(self):
        self.assertEqual(
            self.calendar.next_session(date(2028, 6, 30)),
            date(2028, 7, 3),
        )
        self.assertTrue(self.calendar.is_session(date(2028, 7, 3)))


if __name__ == "__main__":
    unittest.main()
