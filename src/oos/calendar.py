"""
Trading calendar utilities for OOS Engine.
Determines valid trading days and prevents execution on weekends/holidays.
"""
from datetime import date, timedelta
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# NYSE holidays 2026 (from NYSE official calendar)
NYSE_HOLIDAYS_2026 = {
    date(2026, 1, 1),   # New Year's Day
    date(2026, 1, 19),  # MLK Day
    date(2026, 2, 16),  # Presidents Day
    date(2026, 4, 3),   # Good Friday
    date(2026, 5, 25),  # Memorial Day
    date(2026, 6, 19),  # Juneteenth
    date(2026, 7, 3),   # Independence Day (observed)
    date(2026, 9, 7),   # Labor Day
    date(2026, 11, 26), # Thanksgiving
    date(2026, 11, 27), # Day after Thanksgiving (early close — treat as full holiday for safety)
    date(2026, 12, 25), # Christmas
}

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

NYSE_HOLIDAYS = NYSE_HOLIDAYS_2025 | NYSE_HOLIDAYS_2026


def is_trading_day(d: date) -> bool:
    """Return True if d is a valid NYSE trading day."""
    if d.weekday() >= 5:  # Saturday=5, Sunday=6
        return False
    if d in NYSE_HOLIDAYS:
        return False
    return True


def prev_trading_day(d: date) -> date:
    """Return the most recent trading day on or before d."""
    cur = d
    while not is_trading_day(cur):
        cur -= timedelta(days=1)
    return cur


def next_trading_day(d: date) -> date:
    """Return the next trading day strictly after d."""
    cur = d + timedelta(days=1)
    while not is_trading_day(cur):
        cur += timedelta(days=1)
    return cur


def get_signal_date_for_run(run_date: Optional[date] = None) -> tuple[str, bool]:
    """
    Determine signal_date for an OOS run on run_date.
    Returns (signal_date_str, is_valid_run_day).

    If run_date is not a trading day, returns (None, False) — caller should NO_OP.
    Signal date = run_date itself (signals generated at T-day close,
    run happens after close on T-day).
    """
    if run_date is None:
        run_date = date.today()

    if not is_trading_day(run_date):
        logger.info(f"{run_date} is not a trading day (weekend or holiday) — NO_OP")
        return ("", False)

    return (run_date.strftime("%Y-%m-%d"), True)


def latest_market_data_date(exports_path: str = "exports") -> Optional[str]:
    """
    Read the data date from market_state.json to confirm data has advanced.
    Returns date string or None.
    """
    import json
    from pathlib import Path
    try:
        ms = json.loads((Path(exports_path) / "market_state.json").read_text())
        return ms.get("market", {}).get("data_date") or ms.get("generated_at", "")[:10]
    except Exception:
        return None
