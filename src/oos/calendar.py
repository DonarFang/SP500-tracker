"""
Trading calendar utilities for OOS Engine.
Determines valid trading days and prevents execution on weekends/holidays.
"""
from datetime import date, timedelta
from typing import Optional
import logging

logger = logging.getLogger(__name__)

NYSE_HOLIDAYS_2025 = {
    date(2025, 1, 1),
    date(2025, 1, 20),
    date(2025, 2, 17),
    date(2025, 4, 18),
    date(2025, 5, 26),
    date(2025, 6, 19),
    date(2025, 7, 4),
    date(2025, 9, 1),
    date(2025, 11, 27),
    date(2025, 12, 25),
}

NYSE_HOLIDAYS_2026 = {
    date(2026, 1, 1),
    date(2026, 1, 19),
    date(2026, 2, 16),
    date(2026, 4, 3),
    date(2026, 5, 25),
    date(2026, 6, 19),  # Juneteenth
    date(2026, 7, 3),
    date(2026, 9, 7),
    date(2026, 11, 26),
    date(2026, 12, 25),
}

NYSE_HOLIDAYS = NYSE_HOLIDAYS_2025 | NYSE_HOLIDAYS_2026


def is_trading_day(d: date) -> bool:
    if d.weekday() >= 5:
        return False
    return d not in NYSE_HOLIDAYS


def prev_trading_day(d: date) -> date:
    cur = d
    while not is_trading_day(cur):
        cur -= timedelta(days=1)
    return cur


def next_trading_day(d: date) -> date:
    cur = d + timedelta(days=1)
    while not is_trading_day(cur):
        cur += timedelta(days=1)
    return cur


def get_run_status(run_date: Optional[date] = None) -> dict:
    """
    Return run status for a given date.
    status values:
      NO_OP_MARKET_CLOSED  — weekend or holiday
      OOS_ACTIVE           — valid trading day, proceed
    """
    if run_date is None:
        run_date = date.today()

    if not is_trading_day(run_date):
        reason = "weekend" if run_date.weekday() >= 5 else "holiday"
        return {
            "status":          "NO_OP_MARKET_CLOSED",
            "reason":          reason,
            "run_date":        run_date.isoformat(),
            "expected_market_date": prev_trading_day(run_date).isoformat(),
        }

    return {
        "status":               "OOS_ACTIVE",
        "run_date":             run_date.isoformat(),
        "expected_market_date": run_date.isoformat(),
    }
