"""
Forward/OOS Tracking Engine v1.0
Main daily loop for E1_AUDITED_G4_MINHOLD10 OOS tracking.
"""
import logging, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.oos.validation      import load_manifest, validate_or_abort
from src.oos.event_store     import (
    load_all_events, append_event, append_run_record,
    get_last_processed_date, make_event_id
)
from src.oos.portfolio_state import PortfolioState, INITIAL_CAPITAL
from src.oos.execution_adapter import (
    fill_price_buy, fill_price_exit,
    allocate_buys, check_min_hold, should_exit_e1
)
from src.oos.exporter import export_all

logger = logging.getLogger(__name__)


def run_oos_day(
    signal_date: str,
    leaders: list,
    prices: dict,
    market_state: dict,
    source: str = "LIVE_FORWARD",
    data_date: str = None,
) -> dict:
    """
    Process one trading day in OOS mode.
    signal_date: T-day (signals generated at close)
    Orders generated today execute T+1 (next trading day).
    source: LIVE_FORWARD or BACKFILLED_PRELIVE
    """
    logger.info(f"=== OOS Day: {signal_date} | source={source} ===")

    # ── 1. Validate manifest ──────────────────────────────
    manifest = load_manifest()
    validate_or_abort(manifest)

    # ── 2. Rebuild state ──────────────────────────────────
    events = load_all_events()
    state  = PortfolioState.rebuild_from_events(events)

    # Init event on first run
    if not events:
        append_event({
            "event_id":        make_event_id(signal_date, "INIT"),
            "event_type":      "INIT",
            "date":            signal_date,
            "initial_capital": INITIAL_CAPITAL,
            "source":          source,
            "strategy_id":     manifest["strategy"]["id"],
        })

    # ── 3. Execute T+1 orders from previous day ───────────
    executed = []

    # ── Split pending orders into exits and buys ─────────
    pending_exits = [o for o in state.pending_orders if o["action"] == "EXIT"]
    pending_buys  = [o for o in state.pending_orders if o["action"] in ("BUY", "ADD")]

    # ── Execute exits first ───────────────────────────────
    for order in pending_exits:
        sym      = order["symbol"]
        t1_px    = prices.get(sym, {})
        sig_prov = order.get("source", "UNKNOWN")
        if not t1_px:
            logger.warning(f"No T+1 price for {sym} — skipping EXIT")
            continue
        exec_event_id = make_event_id(signal_date, "EXIT_EXECUTED", sym)
        fp = fill_price_exit(t1_px["low"])
        appended = append_event({
            "event_id":          exec_event_id,
            "event_type":        "EXIT_EXECUTED",
            "date":              signal_date,
            "symbol":            sym,
            "action":            "EXIT",
            "fill_price":        fp,
            "units":             state.holdings.get(sym, {}).get("units", 0),
            "cost_rate":         0.001,
            "source":            source,
            "signal_provenance": sig_prov,
            "order_ref":         order.get("event_id"),
        })
        if appended:
            executed.append({
                "symbol":               sym,
                "action":               "EXIT",
                "fill_price":           fp,
                "signal_provenance":    sig_prov,
                "execution_provenance": source,
            })

    # Rebuild state after exits (cash may have increased)
    if pending_exits:
        events = load_all_events()
        state  = PortfolioState.rebuild_from_events(events)

    # ── Execute buys with proper batch allocation ─────────
    if pending_buys:
        # Compute fill prices first
        buy_order_list = []
        for order in pending_buys:
            sym   = order["symbol"]
            t1_px = prices.get(sym, {})
            if not t1_px:
                logger.warning(f"No T+1 price for {sym} — skipping BUY")
                continue
            fp = fill_price_buy(t1_px["high"])
            buy_order_list.append({**order, "fill_price": fp})

        # Allocate cash across all buys in one pass — guarantees no negative cash
        allocations = allocate_buys(
            buy_orders=buy_order_list,
            available_cash=state.cash,
            n_existing_positions=len(state.holdings),
        )

        for alloc in allocations:
            sym      = alloc["symbol"]
            order    = next(o for o in buy_order_list if o["symbol"] == sym)
            sig_prov = order.get("source", "UNKNOWN")
            exec_event_id = make_event_id(signal_date, "BUY_EXECUTED", sym)
            appended = append_event({
                "event_id":          exec_event_id,
                "event_type":        "BUY_EXECUTED",
                "date":              signal_date,        # execution date (T+1)
                "signal_date":       order.get("date"),  # original signal date (T)
                "symbol":            sym,
                "action":            order["action"],
                "fill_price":        alloc["fill_price"],
                "units":             alloc["units"],
                "total_cost":        alloc["total_cost"],
                "cost_rate":         alloc["cost_rate"],
                "source":            source,
                "signal_provenance": sig_prov,
                "order_ref":         order.get("event_id"),
            })
            if appended:
                executed.append({
                    "symbol":               sym,
                    "action":               order["action"],
                    "fill_price":           alloc["fill_price"],
                    "units":                alloc["units"],
                    "total_cost":           alloc["total_cost"],
                    "signal_provenance":    sig_prov,
                    "execution_provenance": source,
                })

    # Rebuild after executions
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
        # Exit signals
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
                    "event_id":     order_id,
                    "event_type":   "ORDER_GENERATED",
                    "date":         signal_date,
                    "symbol":       sym,
                    "action":       "EXIT",
                    "signal_reason": reason,
                    "leader_score": ls,
                    "execute_date": "T+1",
                    "source":       source,
                })
                if appended:
                    new_orders.append({"symbol": sym, "action": "EXIT", "reason": reason})

        # Entry signals: Strict Top 3, RS >= 90
        slots = 3 - len(state.holdings)
        if slots > 0:
            candidates = sorted(
                [l for l in leaders
                 if l.get("rs_score", 0) >= 90
                 and l["symbol"] not in state.holdings
                 and l.get("rank", 999) <= 3],
                key=lambda l: l.get("rank", 999)
            )
            for cand in candidates[:slots]:
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

    append_event({
        "event_id":       make_event_id(signal_date, "EOD_SNAPSHOT"),
        "event_type":     "EOD_SNAPSHOT",
        "date":           signal_date,
        "equity":         equity,
        "cash":           round(state.cash, 2),
        "holdings_value": round(hv, 2),
        "n_positions":    len(state.holdings),
        "gate_open":      gate_open,
        "source":         source,
    })

    # ── 6. Save + export ──────────────────────────────────
    state.save_snapshot(cur_prices)
    events = load_all_events()
    state  = PortfolioState.rebuild_from_events(events)
    export_all(state, events, manifest,
               run_date=signal_date,
               data_date=data_date or signal_date)

    summary = {
        "date":        signal_date,
        "source":      source,
        "gate_open":   gate_open,
        "equity":      equity,
        "executed":    executed,
        "new_orders":  new_orders,
        "n_positions": len(state.holdings),
        "status":      "OOS_ACTIVE",
    }
    append_run_record({**summary, "event_count": len(events)})
    logger.info(f"OOS day complete: equity={equity} positions={len(state.holdings)}")
    return summary
