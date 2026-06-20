"""
Forward/OOS Tracking Engine v1.0
Main daily loop for E1_AUDITED_G4_MINHOLD10 OOS tracking.

Flow per trading day:
  1. Validate manifest + config hash
  2. Load events → rebuild portfolio state
  3. Execute T+1 orders from previous day\\\'s signals
  4. Generate today\\\'s signals using frozen E1 rules
  5. Append events atomically
  6. Save state snapshot + export JSONs
"""
import logging, json, os, sys
from datetime import datetime, date
from pathlib import Path
from typing import Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.oos.validation      import load_manifest, validate_or_abort
from src.oos.event_store     import (
    load_all_events, append_event, append_run_record,
    get_last_processed_date, make_event_id
)
from src.oos.portfolio_state import PortfolioState, INITIAL_CAPITAL
from src.oos.execution_adapter import (
    fill_price_buy, fill_price_exit,
    compute_position_size, check_min_hold, should_exit_e1
)
from src.oos.exporter import export_all

logger = logging.getLogger(__name__)

OOS_START_DATE = "2026-06-16"

def run_oos_day(
    signal_date: str,
    leaders: list,          # [{symbol, leader_score, rank, rs_score, ...}]
    prices: dict,           # {symbol: {open, high, low, close, date}}
    market_state: dict,     # {gate_open: bool, spx_ma50_slope_positive: bool, leadership_confirmed: bool}
    source: str = "LIVE_FORWARD",
) -> dict:
    """
    Process one trading day in OOS mode.
    signal_date: T-day (signals generated)
    Execution happens on T+1 (caller passes T+1 prices)

    Returns run summary dict.
    """
    logger.info(f"=== OOS Day: {signal_date} | source={source} ===")

    # ── 1. Validate manifest ──────────────────────────────
    manifest = load_manifest()
    validate_or_abort(manifest)

    # ── 2. Rebuild state from events ─────────────────────
    events  = load_all_events()
    state   = PortfolioState.rebuild_from_events(events)

    # Init event on first run
    if not events:
        append_event({
            "event_id":       make_event_id(signal_date, "INIT"),
            "event_type":     "INIT",
            "date":           signal_date,
            "initial_capital": INITIAL_CAPITAL,
            "source":         source,
            "strategy_id":    manifest["strategy"]["id"],
        })

    # ── 3. Execute pending T+1 orders ────────────────────
    # Pending orders were generated on previous T-day
    executed = []
    for order in list(state.pending_orders):
        sym    = order["symbol"]
        action = order["action"]
        t1_px  = prices.get(sym, {})
        if not t1_px:
            logger.warning(f"No T+1 price for {sym}, skipping {action}")
            continue

        exec_event_id = make_event_id(signal_date, f"{action}_EXECUTED", sym)

        if action in ("BUY", "ADD"):
            fp    = fill_price_buy(t1_px["high"])
            units = compute_position_size(
                equity=state.total_equity(
                    {s: prices.get(s, {}).get("close", h["entry_price"])
                     for s, h in state.holdings.items()}
                ),
                fill_price=fp,
            )
            appended = append_event({
                "event_id":   exec_event_id,
                "event_type": "BUY_EXECUTED",
                "date":       signal_date,
                "symbol":     sym,
                "action":     action,
                "fill_price": fp,
                "units":      units,
                "cost_rate":  0.001,
                "source":     source,
                "order_ref":  order.get("event_id"),
            })
            if appended:
                executed.append({"symbol": sym, "action": action, "fill_price": fp})

        elif action == "EXIT":
            fp = fill_price_exit(t1_px["low"])
            appended = append_event({
                "event_id":   exec_event_id,
                "event_type": "EXIT_EXECUTED",
                "date":       signal_date,
                "symbol":     sym,
                "action":     "EXIT",
                "fill_price": fp,
                "units":      state.holdings.get(sym, {}).get("units", 0),
                "cost_rate":  0.001,
                "source":     source,
                "order_ref":  order.get("event_id"),
            })
            if appended:
                executed.append({"symbol": sym, "action": "EXIT", "fill_price": fp})

    # Rebuild state after executions
    events = load_all_events()
    state  = PortfolioState.rebuild_from_events(events)

    # ── 4. Generate T-day signals (frozen E1 rules) ──────
    gate_open = (
        market_state.get("gate_open", False) or (
            market_state.get("spx_ma50_slope_positive", False) and
            market_state.get("leadership_confirmed", False)
        )
    )

    new_orders = []
    if gate_open:
        # Exit signals for existing holdings
        for sym, h in list(state.holdings.items()):
            ls_data = next((l for l in leaders if l["symbol"] == sym), None)
            if not ls_data:
                continue
            ls = ls_data.get("leader_score", 100)
            min_hold_ok = check_min_hold(h["entry_date"], signal_date)
            should_exit, reason = should_exit_e1(ls, min_hold_ok)
            if should_exit:
                order_id = make_event_id(signal_date, "ORDER_EXIT", sym)
                appended = append_event({
                    "event_id":    order_id,
                    "event_type":  "ORDER_GENERATED",
                    "date":        signal_date,
                    "symbol":      sym,
                    "action":      "EXIT",
                    "signal_reason": reason,
                    "leader_score": ls,
                    "execute_date": "T+1",
                    "source":      source,
                })
                if appended:
                    new_orders.append({"symbol": sym, "action": "EXIT", "reason": reason})

        # Entry signals: Strict Top 3, RS >= 90
        n_positions = len(state.holdings)
        slots_available = 3 - n_positions
        if slots_available > 0:
            candidates = [
                l for l in leaders
                if l.get("rs_score", 0) >= 90
                and l["symbol"] not in state.holdings
                and l.get("rank", 999) <= 3
            ]
            candidates.sort(key=lambda l: l.get("rank", 999))
            for cand in candidates[:slots_available]:
                sym      = cand["symbol"]
                order_id = make_event_id(signal_date, "ORDER_BUY", sym)
                appended = append_event({
                    "event_id":    order_id,
                    "event_type":  "ORDER_GENERATED",
                    "date":        signal_date,
                    "symbol":      sym,
                    "action":      "BUY",
                    "rank":        cand.get("rank"),
                    "leader_score": cand.get("leader_score"),
                    "rs_score":    cand.get("rs_score"),
                    "execute_date": "T+1",
                    "source":      source,
                })
                if appended:
                    new_orders.append({"symbol": sym, "action": "BUY"})
    else:
        logger.info("Gate CLOSED — no new entries")

    # ── 5. EOD snapshot ───────────────────────────────────
    events = load_all_events()
    state  = PortfolioState.rebuild_from_events(events)
    cur_prices = {
        sym: prices.get(sym, {}).get("close", h["entry_price"])
        for sym, h in state.holdings.items()
    }
    hv     = sum(state.holdings[s]["units"] * cur_prices[s] for s in state.holdings)
    equity = round(state.cash + hv, 2)

    snap_id = make_event_id(signal_date, "EOD_SNAPSHOT")
    append_event({
        "event_id":       snap_id,
        "event_type":     "EOD_SNAPSHOT",
        "date":           signal_date,
        "equity":         equity,
        "cash":           round(state.cash, 2),
        "holdings_value": round(hv, 2),
        "n_positions":    len(state.holdings),
        "gate_open":      gate_open,
        "source":         source,
    })

    # ── 6. Save snapshot + export ─────────────────────────
    state.save_snapshot(cur_prices)
    events = load_all_events()
    state  = PortfolioState.rebuild_from_events(events)
    export_all(state, events, manifest)

    summary = {
        "date":        signal_date,
        "source":      source,
        "gate_open":   gate_open,
        "equity":      equity,
        "executed":    executed,
        "new_orders":  new_orders,
        "n_positions": len(state.holdings),
        "status":      "OK",
    }
    append_run_record({**summary, "event_count": len(events)})
    logger.info(f"OOS day complete: equity={equity} positions={len(state.holdings)}")
    return summary
