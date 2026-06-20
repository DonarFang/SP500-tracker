"""
Portfolio state: cash, holdings, pending orders.
Rebuilt from events.jsonl on every run — state.json is just a cache.
"""
import json, logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

STATE_FILE = Path(__file__).parent.parent.parent / "data" / "oos" / "portfolio_state.json"
INITIAL_CAPITAL = 100_000.0

class PortfolioState:
    def __init__(self):
        self.cash: float = INITIAL_CAPITAL
        self.holdings: dict = {}   # symbol -> {units, cost_basis, entry_date, entry_price}
        self.pending_orders: list = []  # orders generated T-day, executed T+1
        self.equity_history: list = []  # [{date, equity, cash, holdings_value}]
        self.closed_trades: list = []

    @classmethod
    def rebuild_from_events(cls, events: list) -> "PortfolioState":
        """Replay all events to reconstruct current state."""
        state = cls()
        for ev in events:
            t = ev.get("event_type", "")
            if t == "INIT":
                state.cash = ev.get("initial_capital", INITIAL_CAPITAL)
            elif t == "ORDER_GENERATED":
                # Pending order: will be executed next day
                state.pending_orders.append(ev)
            elif t == "BUY_EXECUTED":
                sym   = ev["symbol"]
                units = ev["units"]
                cost  = ev["fill_price"] * units * (1 + ev.get("cost_rate", 0.001))
                state.cash -= cost
                if sym not in state.holdings:
                    state.holdings[sym] = {
                        "units": 0, "cost_basis": 0,
                        "entry_date": ev["date"], "entry_price": ev["fill_price"]
                    }
                state.holdings[sym]["units"]      += units
                state.holdings[sym]["cost_basis"] += cost
                # Remove matched pending order
                state.pending_orders = [
                    o for o in state.pending_orders
                    if not (o["symbol"] == sym and o["action"] in ("BUY", "ADD"))
                ]
            elif t == "EXIT_EXECUTED":
                sym   = ev["symbol"]
                units = ev.get("units", state.holdings.get(sym, {}).get("units", 0))
                proceeds = ev["fill_price"] * units * (1 - ev.get("cost_rate", 0.001))
                state.cash += proceeds
                if sym in state.holdings:
                    h = state.holdings.pop(sym)
                    pnl = proceeds - h["cost_basis"]
                    state.closed_trades.append({
                        "symbol":     sym,
                        "entry_date": h["entry_date"],
                        "exit_date":  ev["date"],
                        "entry_price": h["entry_price"],
                        "exit_price": ev["fill_price"],
                        "units":      units,
                        "pnl":        round(pnl, 2),
                        "return_pct": round(pnl / h["cost_basis"] * 100, 2),
                        "source":     ev.get("source", "LIVE_FORWARD"),
                    })
                state.pending_orders = [
                    o for o in state.pending_orders
                    if not (o["symbol"] == sym and o["action"] == "EXIT")
                ]
            elif t == "EOD_SNAPSHOT":
                state.equity_history.append({
                    "date":            ev["date"],
                    "equity":          ev["equity"],
                    "cash":            ev["cash"],
                    "holdings_value":  ev["holdings_value"],
                    "n_positions":     ev["n_positions"],
                    "source":          ev.get("source", "LIVE_FORWARD"),
                })
        return state

    def total_equity(self, prices: dict) -> float:
        holdings_val = sum(
            h["units"] * prices.get(sym, h["entry_price"])
            for sym, h in self.holdings.items()
        )
        return self.cash + holdings_val

    def to_dict(self, prices: dict = None) -> dict:
        hv = sum(
            h["units"] * (prices or {}).get(sym, h["entry_price"])
            for sym, h in self.holdings.items()
        ) if prices else 0
        return {
            "cash":           round(self.cash, 2),
            "holdings":       self.holdings,
            "holdings_value": round(hv, 2),
            "equity":         round(self.cash + hv, 2),
            "n_positions":    len(self.holdings),
            "pending_orders": self.pending_orders,
            "closed_trades":  self.closed_trades[-20:],  # last 20 for snapshot
        }

    def save_snapshot(self, prices: dict = None) -> None:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(prices), f, indent=2, ensure_ascii=False)
        logger.info(f"Portfolio snapshot saved: {STATE_FILE}")
