#!/usr/bin/env python3
"""
run_oos.py — Forward/OOS Tracking Engine entry point v1.1
Usage:
  python3 run_oos.py                        # run for today (NO_OP on weekends/holidays)
  python3 run_oos.py --date 2026-06-18      # run for specific signal date
  python3 run_oos.py --backfill 2026-06-16  # backfill (BACKFILLED_PRELIVE)
  python3 run_oos.py --status               # show current OOS status
  python3 run_oos.py --check                # pre-check data freshness
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


def load_market_data():
    exports = Path("exports")
    leaders, prices, mkt_state, data_date = [], {}, {"gate_open": False}, None

    try:
        lb = json.loads((exports / "leaderboard.json").read_text())
        leaders = lb.get("leaders", [])
    except Exception as e:
        logger.error(f"Cannot load leaderboard.json: {e}")

    try:
        ms = json.loads((exports / "market_state.json").read_text())
        m  = ms.get("market", {})
        data_date = m.get("data_date") or ms.get("generated_at", "")[:10]
        mkt_state = {
            "gate_open":               m.get("leadership_confirmed", False),
            "spx_ma50_slope_positive": m.get("spx_ma50_slope_positive", False),
            "leadership_confirmed":    m.get("leadership_confirmed", False),
            "data_date":               data_date,
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

    return leaders, prices, mkt_state, data_date


def cmd_status():
    from src.oos.event_store import load_all_events, get_last_processed_date
    from src.oos.portfolio_state import PortfolioState
    events = load_all_events()
    if not events:
        print("No OOS events yet.")
        return
    state    = PortfolioState.rebuild_from_events(events)
    last     = get_last_processed_date()
    live     = sum(1 for e in events if e.get("source") == "LIVE_FORWARD")
    backfill = sum(1 for e in events if e.get("source") == "BACKFILLED_PRELIVE")
    print(f"Last processed date : {last}")
    print(f"Total events        : {len(events)}")
    print(f"LIVE_FORWARD events : {live}")
    print(f"BACKFILLED_PRELIVE  : {backfill}")
    print(f"Open positions      : {len(state.holdings)}")
    print(f"Closed trades       : {len(state.closed_trades)}")
    print(f"Cash                : ${state.cash:,.2f}")
    for sym, h in state.holdings.items():
        sp = h.get("signal_provenance", "?")
        ep = h.get("execution_provenance", "?")
        print(f"  {sym}: {h['units']} units @ ${h['entry_price']} "
              f"(since {h['entry_date']}) sig={sp} exec={ep}")


def main():
    parser = argparse.ArgumentParser(description="OOS Tracking Engine v1.1")
    parser.add_argument("--date",     help="Signal date YYYY-MM-DD (must be a trading day)")
    parser.add_argument("--backfill", help="Backfill from YYYY-MM-DD (BACKFILLED_PRELIVE)")
    parser.add_argument("--status",   action="store_true")
    parser.add_argument("--check",    action="store_true", help="Pre-check data freshness")
    args = parser.parse_args()

    if args.status:
        cmd_status()
        return

    from src.oos.calendar import (
        is_trading_day, prev_trading_day, get_run_status
    )
    from src.oos.event_store import get_last_processed_date
    from src.oos.exporter import export_no_op, export_stale, export_failed

    today = date.today()

    if args.check:
        _, _, _, data_date = load_market_data()
        last_processed = get_last_processed_date()
        run_st = get_run_status(today)
        print(f"Run date          : {today}")
        print(f"Market data date  : {data_date}")
        print(f"Last OOS date     : {last_processed}")
        print(f"Calendar status   : {run_st['status']}")
        if run_st["status"] == "NO_OP_MARKET_CLOSED":
            print("NO_OP — market closed today")
            sys.exit(0)
        if data_date and last_processed and data_date <= last_processed:
            print("⚠️  Data has not advanced — OOS would be NO_OP")
            sys.exit(0)
        print("✅ Data is fresh — OOS can run")
        return

    from src.oos.tracking_engine import run_oos_day

    if args.backfill:
        start = datetime.fromisoformat(args.backfill).date()
        end   = prev_trading_day(today - timedelta(days=1))
        cur   = start
        while cur <= end:
            if is_trading_day(cur):
                ds = cur.strftime("%Y-%m-%d")
                leaders, prices, mkt_state, data_date = load_market_data()
                try:
                    result = run_oos_day(
                        signal_date=ds,
                        leaders=leaders,
                        prices=prices,
                        market_state=mkt_state,
                        source="BACKFILLED_PRELIVE",
                        data_date=data_date,
                    )
                    eq = result["equity"]
                    logger.info(f"✅ {ds} BACKFILLED_PRELIVE: equity={eq}")
                except Exception as e:
                    logger.error(f"❌ {ds} failed: {e}")
            else:
                logger.info(f"⏭  {cur} skipped (non-trading day)")
            cur += timedelta(days=1)

    else:
        # Live daily run
        if args.date:
            run_date = datetime.fromisoformat(args.date).date()
        else:
            run_date = today

        run_st = get_run_status(run_date)

        if run_st["status"] == "NO_OP_MARKET_CLOSED":
            logger.info(f"NO_OP_MARKET_CLOSED: {run_date} ({run_st['reason']})")
            last = get_last_processed_date()
            export_no_op(run_date.isoformat(), run_st["reason"], last)
            sys.exit(0)

        signal_date = run_date.strftime("%Y-%m-%d")

        # Idempotency
        last_processed = get_last_processed_date()
        if last_processed and last_processed >= signal_date:
            logger.info(f"Already processed {signal_date} — NO_OP")
            sys.exit(0)

        leaders, prices, mkt_state, data_date = load_market_data()

        # Data freshness check (only fail on trading days)
        if data_date and data_date < signal_date:
            logger.error(f"OOS_STALE: market data={data_date}, expected={signal_date}")
            export_stale(signal_date, data_date, last_processed)
            sys.exit(1)

        try:
            source = "LIVE_FORWARD"
            result = run_oos_day(
                signal_date=signal_date,
                leaders=leaders,
                prices=prices,
                market_state=mkt_state,
                source=source,
                data_date=data_date,
            )
            print(json.dumps(result, indent=2))
        except Exception as e:
            logger.error(f"OOS_FAILED: {e}")
            export_failed(signal_date, str(e), last_processed)
            sys.exit(1)


if __name__ == "__main__":
    main()
