#!/usr/bin/env python3
"""
run_oos.py — Forward/OOS Tracking Engine entry point
Usage:
  python3 run_oos.py                        # run for today (NO_OP on weekends/holidays)
  python3 run_oos.py --date 2026-06-18      # run for specific signal date
  python3 run_oos.py --backfill 2026-06-16  # backfill from date (BACKFILLED_PRELIVE)
  python3 run_oos.py --status               # show current OOS status
  python3 run_oos.py --check                # validate data date before running (for CI)
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


def load_market_data(signal_date: str = None):
    """Load market data from exports/. Returns (leaders, prices, mkt_state, data_date)."""
    exports = Path("exports")
    leaders, prices, mkt_state = [], {}, {"gate_open": False}
    data_date = None

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
        units = h["units"]
        ep    = h["entry_price"]
        ed    = h["entry_date"]
        print(f"  {sym}: {units} units @ ${ep} (since {ed})")


def main():
    parser = argparse.ArgumentParser(description="OOS Tracking Engine v1.0")
    parser.add_argument("--date",     help="Signal date YYYY-MM-DD (must be a trading day)")
    parser.add_argument("--backfill", help="Backfill from YYYY-MM-DD to last trading day (BACKFILLED_PRELIVE)")
    parser.add_argument("--status",   action="store_true", help="Show current OOS portfolio status")
    parser.add_argument("--check",    action="store_true", help="Validate data date only (for CI pre-check)")
    args = parser.parse_args()

    if args.status:
        cmd_status()
        return

    from src.oos.calendar import (
        is_trading_day, prev_trading_day, next_trading_day,
        get_signal_date_for_run, latest_market_data_date
    )
    from src.oos.event_store import get_last_processed_date

    if args.check:
        data_date = latest_market_data_date()
        last_processed = get_last_processed_date()
        print(f"Market data date  : {data_date}")
        print(f"Last OOS date     : {last_processed}")
        if data_date and last_processed and data_date <= last_processed:
            print("⚠️  Data has not advanced — OOS would be NO_OP")
            sys.exit(0)
        print("✅ Data is fresh — OOS can run")
        return

    from src.oos.tracking_engine import run_oos_day

    if args.backfill:
        # Backfill: mark all as BACKFILLED_PRELIVE
        start = datetime.fromisoformat(args.backfill).date()
        end   = prev_trading_day(date.today() - timedelta(days=1))
        cur   = start
        while cur <= end:
            if is_trading_day(cur):
                ds = cur.strftime("%Y-%m-%d")
                leaders, prices, mkt_state, data_date = load_market_data(ds)
                try:
                    result = run_oos_day(
                        signal_date=ds,
                        leaders=leaders,
                        prices=prices,
                        market_state=mkt_state,
                        source="BACKFILLED_PRELIVE",
                    )
                    eq = result["equity"]
                    logger.info(f"✅ {ds} backfilled (BACKFILLED_PRELIVE): equity={eq}")
                except Exception as e:
                    logger.error(f"❌ {ds} failed: {e}")
            else:
                logger.info(f"⏭️  {cur} skipped (non-trading day)")
            cur += timedelta(days=1)

    else:
        # Live daily run
        if args.date:
            run_date = datetime.fromisoformat(args.date).date()
            if not is_trading_day(run_date):
                logger.warning(f"{run_date} is not a trading day — NO_OP")
                sys.exit(0)
            signal_date = args.date
        else:
            # Auto: use today if trading day, else exit NO_OP
            signal_date, is_valid = get_signal_date_for_run(date.today())
            if not is_valid:
                logger.info("Today is not a trading day — NO_OP")
                sys.exit(0)

        # Idempotency: skip if already processed
        last_processed = get_last_processed_date()
        if last_processed and last_processed >= signal_date:
            logger.info(f"Signal date {signal_date} already processed (last={last_processed}) — NO_OP")
            sys.exit(0)

        # Data freshness check
        _, _, _, data_date = load_market_data(signal_date)
        if data_date and data_date < signal_date:
            logger.error(
                f"DATA STALE: market data is from {data_date}, "
                f"signal_date={signal_date}. OOS aborted to prevent stale execution."
            )
            # Write OOS_STALE marker to oos_summary.json for Dashboard
            import json as _json
            from pathlib import Path as _Path
            from datetime import datetime as _dt, timezone as _tz
            _Path("exports/oos_summary.json").write_text(_json.dumps({
                "status": "OOS_STALE",
                "last_successful_date": last_processed,
                "stale_reason": f"market data={data_date}, expected={signal_date}",
                "generated_at": _dt.now(_tz.utc).isoformat(),
            }, indent=2))
            sys.exit(1)

        leaders, prices, mkt_state, _ = load_market_data(signal_date)
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
