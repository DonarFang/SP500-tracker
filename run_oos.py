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
from __future__ import annotations

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


def _load_price_from_history(symbol: str, as_of_date: str | None = None) -> dict | None:
    """
    Load latest available OHLC for a symbol from data/prices/{symbol}.json.
    If as_of_date is provided, use the last row with date <= as_of_date.
    This is required for OOS mark-to-market of existing holdings.
    """
    p = Path("data") / "prices" / f"{symbol}.json"
    if not p.exists():
        return None
    try:
        rows = json.loads(p.read_text())
        if not isinstance(rows, list) or not rows:
            return None

        chosen = None
        if as_of_date:
            for r in rows:
                d = r.get("date")
                if d and d <= as_of_date:
                    chosen = r
                elif d and d > as_of_date:
                    break
        if chosen is None:
            chosen = rows[-1]

        close = chosen.get("close")
        if close is None:
            return None
        return {
            "open":  chosen.get("open", close),
            "high":  chosen.get("high", close),
            "low":   chosen.get("low", close),
            "close": close,
            "date":  chosen.get("date"),
            "source": "data/prices",
        }
    except Exception as e:
        logger.warning(f"Cannot load price history for {symbol}: {e}")
        return None


def _current_oos_holding_symbols() -> list[str]:
    """
    Read current OOS holdings so mark-to-market does not depend on leaderboard/trade_actions membership.
    """
    p = Path("data") / "oos" / "portfolio_state.json"
    if not p.exists():
        return []
    try:
        j = json.loads(p.read_text())
        h = j.get("holdings", {}) or {}
        return sorted(h.keys())
    except Exception as e:
        logger.warning(f"Cannot load OOS holdings from portfolio_state.json: {e}")
        return []


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
                "source": "trade_actions",
            }
    except Exception as e:
        logger.warning(f"Cannot load trade_actions.json: {e}")

    # Critical OOS mark-to-market supplement:
    # existing holdings must be priced even when they are no longer in trade_actions.
    for sym in _current_oos_holding_symbols():
        hist_px = _load_price_from_history(sym, data_date)
        if hist_px and hist_px.get("close") is not None:
            prices[sym] = hist_px

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




def cmd_replay_invalidated(date_str: str) -> None:
    """
    Replay an invalidated date.
    Safety checks:
    1. LIVE_FORWARD events must be 0 (only allowed during BACKFILLED_PRELIVE phase)
    2. events.jsonl must exist and be valid
    3. After clearing the date's events, re-run backfill for that date only

    Does NOT delete Git history. Appends corrective events with source=BACKFILLED_PRELIVE.
    The invalidated events file must already exist as audit record.
    """
    import os
    from pathlib import Path
    from src.oos.event_store import load_all_events, EVENTS_FILE, OOS_DIR
    from src.oos.portfolio_state import PortfolioState

    logger.info(f"=== REPLAY INVALIDATED: {date_str} ===")

    # 1. Load all current events
    events = load_all_events()
    live_count = sum(1 for e in events if e.get("source") == "LIVE_FORWARD")

    if live_count > 0:
        logger.error(
            f"REPLAY BLOCKED: {live_count} LIVE_FORWARD events exist. "
            f"Replay is only permitted when LIVE_FORWARD events = 0."
        )
        sys.exit(1)

    # 2. Check invalidated audit file exists
    invalidated_files = list(OOS_DIR.glob("events_INVALIDATED_*.jsonl"))
    if not invalidated_files:
        logger.error("No INVALIDATED audit file found. Run cp first.")
        sys.exit(1)
    logger.info(f"Audit file exists: {[f.name for f in invalidated_files]}")

    # 3. Remove events for the target date only
    remaining = [e for e in events if e.get("date") != date_str]
    removed   = [e for e in events if e.get("date") == date_str]
    logger.info(f"Removing {len(removed)} events for {date_str}, keeping {len(remaining)}")

    # Rewrite events.jsonl without the invalidated date
    import json
    tmp = EVENTS_FILE.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        for ev in remaining:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    tmp.replace(EVENTS_FILE)
    logger.info(f"events.jsonl rewritten: {len(remaining)} events remain")

    # 4. Re-run for the target date as BACKFILLED_PRELIVE
    logger.info(f"Re-running {date_str} as BACKFILLED_PRELIVE ...")
    leaders, prices, mkt_state, data_date = load_market_data()
    from src.oos.tracking_engine import run_oos_day
    result = run_oos_day(
        signal_date=date_str,
        leaders=leaders,
        prices=prices,
        market_state=mkt_state,
        source="BACKFILLED_PRELIVE",
        data_date=data_date,
    )

    # 5. Verify no negative cash
    events_after = load_all_events()
    state = PortfolioState.rebuild_from_events(events_after)
    if state.cash < -0.01:
        logger.error(f"REPLAY FAILED: cash={state.cash:.4f} < 0 after replay!")
        sys.exit(1)

    logger.info(
        f"✅ Replay complete: {date_str} | "
        f"equity={result['equity']} positions={result['n_positions']} cash={state.cash:.2f}"
    )
    print(json.dumps(result, indent=2))

def main():
    parser = argparse.ArgumentParser(description="OOS Tracking Engine v1.1")
    parser.add_argument("--date",     help="Signal date YYYY-MM-DD (must be a trading day)")
    parser.add_argument("--backfill", help="Backfill from YYYY-MM-DD (BACKFILLED_PRELIVE)")
    parser.add_argument("--status",   action="store_true")
    parser.add_argument("--check",    action="store_true", help="Pre-check data freshness")
    parser.add_argument("--replay-invalidated", metavar="DATE",
                        help="Replay invalidated date. Only when LIVE_FORWARD=0.")
    args = parser.parse_args()

    if args.status:
        cmd_status()
        return

    if args.replay_invalidated:
        cmd_replay_invalidated(args.replay_invalidated)
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
