"""
Portfolio state: cash, holdings, pending orders.
Rebuilt from events.jsonl on every run — state.json is just a cache.
Tracks signal_provenance and execution_provenance separately.
"""
import json, logging
from pathlib import Path

logger = logging.getLogger(__name__)

STATE_FILE    = Path(__file__).parent.parent.parent / "data" / "oos" / "portfolio_state.json"
INITIAL_CAPITAL = 100_000.0


class PortfolioState:
    def __init__(self):
        self.cash: float = INITIAL_CAPITAL
        self.holdings: dict = {}
        # holdings[sym] = {units, cost_basis, entry_date, entry_price,
        #                   signal_provenance, execution_provenance}
        self.pending_orders: list = []
        self.equity_history: list = []
        self.closed_trades: list = []

    @classmethod
    def rebuild_from_events(cls, events: list) -> "PortfolioState":
        state = cls()
        # Build a map of order event_id → source for provenance tracking
        order_source_map: dict = {}

        for ev in events:
            t = ev.get("event_type", "")

            if t == "INIT":
                state.cash = ev.get("initial_capital", INITIAL_CAPITAL)

            elif t == "ORDER_GENERATED":
                state.pending_orders.append(ev)
                order_source_map[ev["event_id"]] = ev.get("source", "UNKNOWN")

            elif t == "BUY_EXECUTED":
                sym    = ev["symbol"]
                units  = ev["units"]
                cost   = ev["fill_price"] * units * (1 + ev.get("cost_rate", 0.001))
                state.cash -= cost

                # Provenance: signal came from the ORDER_GENERATED event
                order_ref = ev.get("order_ref", "")
                sig_prov  = order_source_map.get(order_ref, ev.get("source", "UNKNOWN"))
                exec_prov = ev.get("source", "UNKNOWN")

                if sym not in state.holdings:
                    state.holdings[sym] = {
                        "units":                0,
                        "cost_basis":           0,
                        "entry_date":           ev["date"],
                        "entry_price":          ev["fill_price"],
                        "signal_provenance":    sig_prov,
                        "execution_provenance": exec_prov,
                    }
                state.holdings[sym]["units"]      += units
                state.holdings[sym]["cost_basis"] += cost
                state.pending_orders = [
                    o for o in state.pending_orders
                    if not (o["symbol"] == sym and o["action"] in ("BUY", "ADD"))
                ]

            elif t == "EXIT_EXECUTED":
                sym      = ev["symbol"]
                units    = ev.get("units", state.holdings.get(sym, {}).get("units", 0))
                proceeds = ev["fill_price"] * units * (1 - ev.get("cost_rate", 0.001))
                state.cash += proceeds

                if sym in state.holdings:
                    h   = state.holdings.pop(sym)
                    pnl = proceeds - h["cost_basis"]
                    order_ref = ev.get("order_ref", "")
                    sig_prov  = order_source_map.get(order_ref, h.get("signal_provenance", "UNKNOWN"))
                    state.closed_trades.append({
                        "symbol":               sym,
                        "entry_date":           h["entry_date"],
                        "exit_date":            ev["date"],
                        "entry_price":          h["entry_price"],
                        "exit_price":           ev["fill_price"],
                        "units":                units,
                        "pnl":                  round(pnl, 2),
                        "return_pct":           round(pnl / h["cost_basis"] * 100, 2),
                        "signal_provenance":    h.get("signal_provenance", "UNKNOWN"),
                        "execution_provenance": h.get("execution_provenance", "UNKNOWN"),
                        "exit_signal_provenance": sig_prov,
                    })
                state.pending_orders = [
                    o for o in state.pending_orders
                    if not (o["symbol"] == sym and o["action"] == "EXIT")
                ]

            elif t == "EOD_SNAPSHOT":
                state.equity_history.append({
                    "date":           ev["date"],
                    "equity":         ev["equity"],
                    "cash":           ev["cash"],
                    "holdings_value": ev["holdings_value"],
                    "n_positions":    ev["n_positions"],
                    "source":         ev.get("source", "UNKNOWN"),
                })

        return state

    def total_equity(self, prices: dict) -> float:
        hv = sum(
            h["units"] * prices.get(sym, h["entry_price"])
            for sym, h in self.holdings.items()
        )
        return self.cash + hv

    def save_snapshot(self, prices: dict = None) -> None:
        hv = sum(
            h["units"] * (prices or {}).get(sym, h["entry_price"])
            for sym, h in self.holdings.items()
        ) if prices else 0
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "cash":           round(self.cash, 2),
            "holdings":       self.holdings,
            "holdings_value": round(hv, 2),
            "equity":         round(self.cash + hv, 2),
            "n_positions":    len(self.holdings),
            "pending_orders": self.pending_orders,
            "closed_trades":  self.closed_trades[-20:],
        }
        tmp = STATE_FILE.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        tmp.replace(STATE_FILE)
        logger.info(f"Portfolio snapshot saved: {STATE_FILE}")
