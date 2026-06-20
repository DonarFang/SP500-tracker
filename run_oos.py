#!/usr/bin/env python3
"""
run_oos.py — Forward/OOS Tracking Engine entry point
Usage:
  python3 run_oos.py                        # run for today
  python3 run_oos.py --date 2026-06-20      # run for specific date
  python3 run_oos.py --backfill 2026-06-16  # backfill from date (BACKFILLED_PRELIVE)
  python3 run_oos.py --status               # show current OOS status
"""
import argparse, json, logging, sys
from pathlib import Path
from datetime import date, datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)-5s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)
sys.path.insert(0, str(Path(__file__).parent))


def load_today_data():
    """Load today's market data from exports/."""
    exports = Path("exports")
    leaders, prices, mkt_state = [], {}, {"gate_open": False}

    try:
        lb = json.loads((exports / "leaderboard.json").read_text())
        leaders = lb.get("leaders", [])
    except Exception as e:
        logger.error(f"Cannot load leaderboard.json: {e}")

    try:
        ms = json.loads((exports / "market_state.json").read_text())
        m  = ms.get("market", {})
        mkt_state = {
            "gate_open":               m.get("leadership_confirmed", False),
            "spx_ma50_slope_positive": m.get("spx_ma50_slope_positive", False),
            "leadership_confirmed":    m.get("leadership_confirmed", False),
        }
    except Exception as e:
        logger.error(f"Cannot load market_state.json: {e}")

    try:
        ta = json.loads((exports / "trade_actions.json").read_text())
        for stock in ta.get("stocks", []):
            sym = stock["symbol"]
            prices[sym] = {
                "open":  stock.get("price"),
                "high":  stock.get("high", stock.get("price")),
                "low":   stock.get("low",  stock.get("price")),
                "close": stock.get("price"),
            }
    except Exception as e:
        logger.warning(f"Cannot load trade_actions.json: {e}")

    return leaders, prices, mkt_state


def cmd_status():
    from src.oos.event_store import load_all_events, get_last_processed_date
    from src.oos.portfolio_state import PortfolioState
    events = load_all_events()
    if not events:
        print("No OOS events yet.")
        return
    state  = PortfolioState.rebuild_from_events(events)
    last   = get_last_processed_date()
    live      = sum(1 for e in events if e.get("source") == "LIVE_FORWARD")
    backfill  = sum(1 for e in events if e.get("source") == "BACKFILLED_PRELIVE")
    print(f"Last processed date : {last}")
    print(f"Total events        : {len(events)}")
    print(f"LIVE_FORWARD events : {live}")
    print(f"BACKFILLED_PRELIVE  : {backfill}")
    print(f"Open positions      : {len(state.holdings)}")
    print(f"Closed trades       : {len(state.closed_trades)}")
    print(f"Cash                : ${state.cash:,.2f}")
    for sym, h in state.holdings.items():
        units = h["units"]
        ep    = h["entry_price"]
        ed    = h["entry_date"]
        print(f"  {sym}: {units} units @ ${ep} (since {ed})")


def main():
    parser = argparse.ArgumentParser(description="OOS Tracking Engine v1.0")
    parser.add_argument("--date",     help="Signal date YYYY-MM-DD (default: today)")
    parser.add_argument("--backfill", help="Backfill from YYYY-MM-DD to yesterday (BACKFILLED_PRELIVE)")
    parser.add_argument("--status",   action="store_true", help="Show current OOS portfolio status")
    args = parser.parse_args()

    if args.status:
        cmd_status()
        return

    from src.oos.tracking_engine import run_oos_day

    if args.backfill:
        start = datetime.fromisoformat(args.backfill).date()
        end   = date.today() - timedelta(days=1)
        cur   = start
        while cur <= end:
            ds = cur.strftime("%Y-%m-%d")
            leaders, prices, mkt_state = load_today_data()
            try:
                result = run_oos_day(
                    signal_date=ds,
                    leaders=leaders,
                    prices=prices,
                    market_state=mkt_state,
                    source="BACKFILLED_PRELIVE",
                )
                eq = result["equity"]
                print(f"✅ {ds} backfilled: equity={eq}")
            except Exception as e:
                logger.error(f"❌ {ds} failed: {e}")
            cur += timedelta(days=1)
    else:
        signal_date = args.date or date.today().strftime("%Y-%m-%d")
        leaders, prices, mkt_state = load_today_data()
        result = run_oos_day(
            signal_date=signal_date,
            leaders=leaders,
            prices=prices,
            market_state=mkt_state,
            source="LIVE_FORWARD",
        )
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
