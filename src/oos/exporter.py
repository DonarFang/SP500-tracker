"""
Export OOS state to Dashboard JSON files under exports/.
Called at end of each successful OOS run.
"""
import json, logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)
EXPORTS = Path(__file__).parent.parent.parent / "exports"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _now_display() -> str:
    try:
        import pytz
        et = pytz.timezone("America/New_York")
        return datetime.now(et).strftime("%Y年%-m月%-d日 %H:%M ET")
    except Exception:
        return _now_iso()

def write_json(name: str, data: dict) -> None:
    EXPORTS.mkdir(parents=True, exist_ok=True)
    path = EXPORTS / name
    tmp  = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    tmp.replace(path)  # atomic rename
    logger.info(f"Exported: {path}")


def export_no_op(run_date: str, reason: str, last_successful: str = None) -> None:
    """
    Write oos_summary.json for NO_OP days (weekend/holiday).
    Does NOT touch events.jsonl or portfolio_state.json.
    """
    from src.oos.calendar import prev_trading_day
    from datetime import date
    expected = prev_trading_day(date.fromisoformat(run_date)).isoformat()
    write_json("oos_summary.json", {
        "generated_at":        _now_iso(),
        "generated_at_display": _now_display(),
        "status":              "NO_OP_MARKET_CLOSED",
        "reason":              reason,
        "run_date":            run_date,
        "last_successful_run": last_successful,
        "last_market_date":    last_successful,
        "expected_market_date": expected,
    })


def export_stale(run_date: str, data_date: str, last_successful: str = None) -> None:
    """Write oos_summary.json for OOS_STALE state."""
    write_json("oos_summary.json", {
        "generated_at":        _now_iso(),
        "generated_at_display": _now_display(),
        "status":              "OOS_STALE",
        "stale_reason":        f"market_data={data_date}, expected={run_date}",
        "run_date":            run_date,
        "last_successful_run": last_successful,
        "last_market_date":    data_date,
        "expected_market_date": run_date,
    })


def export_failed(run_date: str, error: str, last_successful: str = None) -> None:
    """Write oos_summary.json for OOS_FAILED state."""
    write_json("oos_summary.json", {
        "generated_at":        _now_iso(),
        "generated_at_display": _now_display(),
        "status":              "OOS_FAILED",
        "error":               str(error),
        "run_date":            run_date,
        "last_successful_run": last_successful,
        "last_market_date":    None,
        "expected_market_date": run_date,
    })


def export_all(state, events: list, manifest: dict,
               run_date: str, data_date: str) -> None:
    """Full export after a successful OOS run."""
    ts   = _now_iso()
    disp = _now_display()
    strat_id = manifest["strategy"]["id"]
    initial  = manifest["oos_tracking"]["initial_capital"]

    closed   = state.closed_trades
    winners  = [t for t in closed if t["return_pct"] > 0]
    losers   = [t for t in closed if t["return_pct"] <= 0]
    gp = sum(t["pnl"] for t in winners)
    gl = abs(sum(t["pnl"] for t in losers))
    pf = round(gp / gl, 3) if gl > 0 else None
    wr = round(len(winners) / len(closed) * 100, 1) if closed else None

    eq_hist  = state.equity_history
    final_eq = eq_hist[-1]["equity"] if eq_hist else initial
    total_ret = round((final_eq / initial - 1) * 100, 2) if initial else 0

    peak, max_dd = initial, 0.0
    for snap in eq_hist:
        eq = snap["equity"]
        if eq > peak:
            peak = eq
        dd = (peak - eq) / peak * 100
        if dd > max_dd:
            max_dd = dd

    live_count     = sum(1 for e in events if e.get("source") == "LIVE_FORWARD")
    backfill_count = sum(1 for e in events if e.get("source") == "BACKFILLED_PRELIVE")
    last_successful = run_date

    # ── oos_summary.json ──────────────────────────────────
    write_json("oos_summary.json", {
        "generated_at":         ts,
        "generated_at_display": disp,
        "status":               "OOS_ACTIVE",
        "strategy_id":          strat_id,
        "oos_start_date":       manifest["oos_tracking"]["start_date"],
        "run_date":             run_date,
        "last_successful_run":  last_successful,
        "last_market_date":     data_date,
        "expected_market_date": run_date,
        "initial_capital":      initial,
        "final_equity":         round(final_eq, 2),
        "total_return_pct":     total_ret,
        "max_drawdown_pct":     round(max_dd, 2),
        "profit_factor":        pf,
        "win_rate_pct":         wr,
        "total_trades":         len(closed),
        "open_positions":       len(state.holdings),
        "live_event_count":     live_count,
        "backfill_event_count": backfill_count,
        "first_review_criteria": manifest["oos_tracking"]["first_review_criteria"],
        "provenance_note": (
            "BACKFILLED_PRELIVE: events replayed after engine deployment. "
            "LIVE_FORWARD: events generated by automated daily run. "
            "MIXED: signal from BACKFILLED_PRELIVE, execution from LIVE_FORWARD — "
            "not counted in pure LIVE_FORWARD trade statistics."
        ),
        "mixed_provenance_positions": sum(
            1 for h in state.holdings.values()
            if h.get("signal_provenance") != h.get("execution_provenance")
            and h.get("signal_provenance") not in (None, "UNKNOWN")
        ),
    })

    # ── oos_positions.json ────────────────────────────────
    write_json("oos_positions.json", {
        "generated_at": ts, "generated_at_display": disp,
        "strategy_id":  strat_id,
        "as_of":        run_date,
        "positions": [
            {
                "symbol":               sym,
                "entry_date":           h["entry_date"],
                "signal_date":          h.get("signal_date", h["entry_date"]),
                "entry_price":          h["entry_price"],
                "units":                h["units"],
                "cost_basis":           round(h["cost_basis"], 2),
                "signal_provenance":    h.get("signal_provenance", "UNKNOWN"),
                "execution_provenance": h.get("execution_provenance", "UNKNOWN"),
                "mixed_provenance": (
                    h.get("signal_provenance") != h.get("execution_provenance")
                    and h.get("signal_provenance") not in (None, "UNKNOWN")
                    and h.get("execution_provenance") not in (None, "UNKNOWN")
                ),
            }
            for sym, h in state.holdings.items()
        ],
        "pending_orders": [
            {**o, "signal_provenance": o.get("source", "UNKNOWN")}
            for o in state.pending_orders
        ],
        "cash": round(state.cash, 2),
    })

    # ── oos_trades.json ───────────────────────────────────
    write_json("oos_trades.json", {
        "generated_at": ts, "generated_at_display": disp,
        "strategy_id":  strat_id,
        "total_trades": len(closed),
        "trades":       closed,
    })

    # ── oos_equity_curve.json ─────────────────────────────
    write_json("oos_equity_curve.json", {
        "generated_at":    ts,
        "generated_at_display": disp,
        "strategy_id":     strat_id,
        "initial_capital": initial,
        "curve":           eq_hist,
    })

    # ── oos_orders.json ───────────────────────────────────
    order_events = [e for e in events
                    if e.get("event_type") in
                    ("ORDER_GENERATED", "BUY_EXECUTED", "EXIT_EXECUTED")]
    write_json("oos_orders.json", {
        "generated_at": ts, "generated_at_display": disp,
        "strategy_id":  strat_id,
        "orders":       order_events[-100:],
    })

    logger.info("✅ All OOS exports written")
