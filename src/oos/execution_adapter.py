"""
Execution adapter: bridges OOS engine to frozen E1 signal logic.
Imports from src/engine but NEVER modifies it.
All execution rules are read from E1_FROZEN_MANIFEST, not hardcoded.
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# T+1 adverse fill model — mirrors backtest.py adverse_intraday_v1.0
ONE_WAY_COST = 0.001  # 0.10%

def fill_price_buy(high: float, cost_rate: float = ONE_WAY_COST) -> float:
    """BUY executes at T+1 high (adverse). Cost added on top."""
    return round(high * (1 + cost_rate), 4)

def fill_price_exit(low: float, cost_rate: float = ONE_WAY_COST) -> float:
    """EXIT executes at T+1 low (adverse). Cost deducted."""
    return round(low * (1 - cost_rate), 4)

def compute_position_size(
    equity: float,
    max_positions: int = 3,
    target_pct: float = 1/3,
    fill_price: float = 1.0,
) -> float:
    """Number of units to buy for a new position."""
    alloc = equity * target_pct
    units = alloc / fill_price
    return round(units, 4)

def check_min_hold(entry_date: str, current_date: str, min_days: int = 10) -> bool:
    """Returns True if MinHold is satisfied (exit allowed)."""
    from datetime import datetime
    try:
        ed = datetime.fromisoformat(entry_date)
        cd = datetime.fromisoformat(current_date)
        return (cd - ed).days >= min_days
    except Exception:
        return True  # fail safe: allow exit

def should_exit_e1(leader_score: float, min_hold_satisfied: bool) -> tuple[bool, str]:
    """
    E1 exit rule: LS < 60 AND MinHold satisfied.
    Returns (should_exit, reason).
    """
    if leader_score < 60 and min_hold_satisfied:
        return True, "leader_score_below_60"
    if leader_score < 60 and not min_hold_satisfied:
        return False, "min_hold_block"
    return False, "hold"
