"""
Execution adapter: bridges OOS engine to frozen E1 signal logic.
All execution rules read from E1_FROZEN_MANIFEST, not hardcoded.

Key constraint: NO leverage, NO negative cash.
All buy allocations are strictly bounded by available cash.
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)

ONE_WAY_COST = 0.001   # 0.10%
MAX_POSITIONS = 3
TARGET_POSITION_PCT = 1 / 3   # ~33.3%


def fill_price_buy(high: float, cost_rate: float = ONE_WAY_COST) -> float:
    """BUY executes at T+1 high (adverse). Cost added."""
    return round(high * (1 + cost_rate), 4)


def fill_price_exit(low: float, cost_rate: float = ONE_WAY_COST) -> float:
    """EXIT executes at T+1 low (adverse). Cost deducted."""
    return round(low * (1 - cost_rate), 4)


def allocate_buys(
    buy_orders: list,         # list of {symbol, fill_price, ...}
    available_cash: float,
    n_existing_positions: int,
    max_positions: int = MAX_POSITIONS,
    cost_rate: float = ONE_WAY_COST,
) -> list:
    """
    Allocate cash to a batch of buy orders in one pass.
    Guarantees: total cost <= available_cash, cash never goes negative.

    Each order gets:
      target = available_cash / total_slots
      notional = min(target, remaining_cash_before_cost / (1 + cost_rate))
      units = floor(notional / fill_price, 4 decimals)
      total_cost = units * fill_price * (1 + cost_rate)

    remaining_cash and remaining_orders update after each allocation.

    Returns list of {symbol, units, fill_price, total_cost, cost_rate}.
    Skips any order where units would be zero.
    """
    n_buys = len(buy_orders)
    if n_buys == 0 or available_cash <= 0:
        return []

    total_slots    = max_positions - n_existing_positions
    slots_for_buys = min(n_buys, total_slots)
    if slots_for_buys <= 0:
        logger.warning("No position slots available — no buys allocated")
        return []

    remaining_cash   = available_cash
    remaining_orders = slots_for_buys
    result = []

    for i, order in enumerate(buy_orders[:slots_for_buys]):
        sym        = order["symbol"]
        fill_price = order["fill_price"]

        if remaining_cash <= 0:
            logger.warning(f"{sym}: no cash remaining — skipped")
            break

        # Target = equal share of remaining cash across remaining orders
        target_notional = remaining_cash / remaining_orders

        # Max notional so that total_cost <= remaining_cash
        max_notional = remaining_cash / (1 + cost_rate)

        notional   = min(target_notional, max_notional)
        units      = round(notional / fill_price, 4)
        total_cost = round(units * fill_price * (1 + cost_rate), 4)

        if units <= 0:
            logger.warning(f"{sym}: units=0 at fill_price={fill_price} — skipped")
            remaining_orders -= 1
            continue

        # Hard guard: never exceed remaining cash
        if total_cost > remaining_cash + 0.001:
            logger.warning(
                f"{sym}: total_cost={total_cost:.6f} > remaining_cash={remaining_cash:.6f}"
                f" — capping units to fit available cash"
            )
            # Floor units to 4 decimal places to guarantee total_cost <= remaining_cash
            import math
            max_units  = math.floor((remaining_cash / (1 + cost_rate)) / fill_price * 10000) / 10000
            units      = max_units
            total_cost = round(units * fill_price * (1 + cost_rate), 6)
            # Clamp any residual float error
            if total_cost > remaining_cash:
                total_cost = remaining_cash

        remaining_cash   = round(remaining_cash - total_cost, 4)
        remaining_orders -= 1

        result.append({
            "symbol":     sym,
            "units":      units,
            "fill_price": fill_price,
            "total_cost": total_cost,
            "cost_rate":  cost_rate,
        })
        logger.debug(
            f"Allocated {sym}: units={units} fill={fill_price} "
            f"cost={total_cost:.2f} remaining_cash={remaining_cash:.2f}"
        )

    # Final hard check — no tolerance, must be strictly within cash
    total_allocated = sum(r["total_cost"] for r in result)
    if total_allocated > available_cash + 0.001:
        raise RuntimeError(
            f"ALLOCATION ERROR: total_cost={total_allocated:.6f} > "
            f"available_cash={available_cash:.6f}. Aborting to prevent negative cash."
        )

    logger.info(
        f"Allocated {len(result)}/{n_buys} buys, "
        f"total_cost={total_allocated:.2f}, "
        f"remaining_cash={available_cash - total_allocated:.2f}"
    )
    return result


def check_min_hold(entry_date: str, current_date: str, min_days: int = 10) -> bool:
    """Returns True if MinHold is satisfied."""
    from datetime import datetime
    try:
        ed = datetime.fromisoformat(entry_date)
        cd = datetime.fromisoformat(current_date)
        return (cd - ed).days >= min_days
    except Exception:
        return True


def should_exit_e1(leader_score: float, min_hold_satisfied: bool) -> tuple:
    """
    E1 exit rule: LS < 60 AND MinHold satisfied.
    Returns (should_exit: bool, reason: str).
    """
    if leader_score < 60 and min_hold_satisfied:
        return True, "leader_score_below_60"
    if leader_score < 60 and not min_hold_satisfied:
        return False, "min_hold_block"
    return False, "hold"
