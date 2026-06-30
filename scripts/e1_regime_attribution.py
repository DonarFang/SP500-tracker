"""
scripts/e1_regime_attribution.py

E1 Regime Attribution v1 (trade-level).

Reads:
  exports/backtest.json          (E1 trades, audit window 2023-11 onward)
  data/research/e1_5y/regimes/spx_regime_daily.json  (daily regime map)

Produces trade-level attribution: each E1 trade is tagged with
entry_regime and exit_regime. Cross-regime trades are flagged.

LIMITATION: equity-level regime return / MaxDD requires a continuous
daily equity series, which backtest.json does not currently export
(daily_records is sparse, 22 points). Those metrics are deferred to
the full 5-year backtest run. This script reports trade-level only.

Outputs:
  data/research/e1_5y/regimes/e1_regime_attribution.json
"""
import json, logging
from datetime import date, datetime, timezone
from pathlib import Path
from collections import defaultdict

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)-5s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

BACKTEST_FILE = Path("exports/backtest.json")
REGIME_FILE   = Path("data/research/e1_5y/regimes/spx_regime_daily.json")
OUT_FILE      = Path("data/research/e1_5y/regimes/e1_regime_attribution.json")


def load_e1_trades() -> list:
    bj = json.load(open(BACKTEST_FILE))
    e1 = bj["backtest"]["results"]["layer_d"]["variant_results"]["E1_AUDITED_G4_MINHOLD10"]
    return e1.get("trades", [])


def load_regime_map() -> dict:
    data  = json.load(open(REGIME_FILE))
    daily = data.get("daily_regime", {})
    # {date_str: {regime, subclass}}
    return {d: v["regime"] for d, v in daily.items()}


def regime_on(regime_map: dict, date_str: str) -> str:
    """Return regime for a date, or nearest prior trading day's regime."""
    if date_str in regime_map:
        return regime_map[date_str]
    # Find nearest prior date
    d = date.fromisoformat(date_str)
    for back in range(1, 8):
        prior = (d.fromordinal(d.toordinal() - back)).isoformat()
        if prior in regime_map:
            return regime_map[prior]
    return "UNKNOWN"


def holding_days_weighted_regime(regime_map: dict, entry: str, exit_: str) -> dict:
    """Count trading days in each regime over the holding period."""
    d0 = date.fromisoformat(entry)
    d1 = date.fromisoformat(exit_)
    counts = defaultdict(int)
    cur = d0
    while cur <= d1:
        ds = cur.isoformat()
        if ds in regime_map:
            counts[regime_map[ds]] += 1
        cur = date.fromordinal(cur.toordinal() + 1)
    return dict(counts)


def main():
    trades     = load_e1_trades()
    regime_map = load_regime_map()
    logger.info(f"E1 trades: {len(trades)}")
    logger.info(f"Regime map dates: {len(regime_map)}")

    if not regime_map:
        logger.error("Regime map empty — run build_weekly_regimes.py first")
        raise SystemExit(1)

    regime_dates = sorted(regime_map.keys())
    logger.info(f"Regime coverage: {regime_dates[0]} → {regime_dates[-1]}")

    # Tag each trade
    tagged = []
    cross_regime_count = 0
    for t in trades:
        entry = t["entry_date"]
        exit_ = t["exit_date"]
        entry_regime = regime_on(regime_map, entry)
        exit_regime  = regime_on(regime_map, exit_)
        hd_weighted  = holding_days_weighted_regime(regime_map, entry, exit_)
        dominant     = max(hd_weighted, key=hd_weighted.get) if hd_weighted else "UNKNOWN"
        is_cross     = entry_regime != exit_regime
        if is_cross:
            cross_regime_count += 1

        tagged.append({
            "symbol":            t["symbol"],
            "entry_date":        entry,
            "exit_date":         exit_,
            "return_pct":        t.get("return_pct"),
            "holding_days":      t.get("holding_days"),
            "realized_pnl":      t.get("realized_pnl_before_exit"),
            "is_sim_end":        t.get("is_sim_end", False),
            "exit_reason":       t.get("exit_reason"),
            "entry_regime":      entry_regime,
            "exit_regime":       exit_regime,
            "dominant_regime":   dominant,
            "cross_regime":      is_cross,
            "regime_day_weights": hd_weighted,
        })

    # ── Group by entry_regime ──────────────────────────────
    def group_stats(trade_subset: list) -> dict:
        if not trade_subset:
            return {"trades": 0}
        returns = [x["return_pct"] for x in trade_subset if x["return_pct"] is not None]
        wins    = [r for r in returns if r > 0]
        losses  = [r for r in returns if r <= 0]
        gross_w = sum(x["realized_pnl"] for x in trade_subset
                      if x.get("realized_pnl") and x["return_pct"] and x["return_pct"] > 0)
        gross_l = abs(sum(x["realized_pnl"] for x in trade_subset
                          if x.get("realized_pnl") and x["return_pct"] and x["return_pct"] <= 0))
        return {
            "trades":          len(trade_subset),
            "win_rate_pct":    round(len(wins)/len(returns)*100, 1) if returns else None,
            "avg_return_pct":  round(sum(returns)/len(returns), 2) if returns else None,
            "avg_winner_pct":  round(sum(wins)/len(wins), 2) if wins else None,
            "avg_loser_pct":   round(sum(losses)/len(losses), 2) if losses else None,
            "avg_holding_days": round(sum(x["holding_days"] for x in trade_subset
                                          if x["holding_days"])/len(trade_subset), 1),
            "profit_factor":   round(gross_w/gross_l, 3) if gross_l > 0 else None,
            "sum_realized_pnl": round(sum(x["realized_pnl"] for x in trade_subset
                                          if x.get("realized_pnl")), 2),
            "cross_regime_trades": sum(1 for x in trade_subset if x["cross_regime"]),
        }

    by_entry_regime    = defaultdict(list)
    by_dominant_regime = defaultdict(list)
    for x in tagged:
        by_entry_regime[x["entry_regime"]].append(x)
        by_dominant_regime[x["dominant_regime"]].append(x)

    entry_attribution = {r: group_stats(ts) for r, ts in by_entry_regime.items()}
    dominant_attribution = {r: group_stats(ts) for r, ts in by_dominant_regime.items()}

    result = {
        "generated_at":   datetime.now(timezone.utc).isoformat(),
        "method":         "trade-level attribution v1",
        "dataset_note": (
            "E1 trades from audit window (2023-11 onward). "
            "Regime map covers 2021-06 onward; overlap is audit window. "
            "Equity-level regime return/MaxDD deferred — requires continuous "
            "daily equity series not present in current backtest.json."
        ),
        "trade_count":         len(tagged),
        "cross_regime_count":  cross_regime_count,
        "attribution_by_entry_regime":    entry_attribution,
        "attribution_by_dominant_regime": dominant_attribution,
        "tagged_trades":       tagged,
    }

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT_FILE.with_suffix(".tmp")
    json.dump(result, open(tmp, "w"), indent=2, ensure_ascii=False)
    tmp.replace(OUT_FILE)

    # ── Summary ────────────────────────────────────────────
    logger.info("\n" + "=" * 64)
    logger.info("E1 REGIME ATTRIBUTION v1 (trade-level)")
    logger.info("=" * 64)
    logger.info(f"Total trades: {len(tagged)}  ·  cross-regime: {cross_regime_count}")
    logger.info("")
    logger.info("── By ENTRY regime ──")
    logger.info(f"{'Regime':14s} {'N':>3s} {'Win%':>6s} {'AvgRet':>7s} {'PF':>6s} {'AvgHold':>8s} {'SumPnL':>12s}")
    for r in ["UPTREND", "SIDEWAYS", "DOWNTREND", "UNKNOWN"]:
        s = entry_attribution.get(r)
        if not s or s["trades"] == 0:
            continue
        pf = s['profit_factor'] if s['profit_factor'] is not None else 0
        logger.info(f"{r:14s} {s['trades']:>3d} {s['win_rate_pct'] or 0:>5.1f}% "
                    f"{s['avg_return_pct'] or 0:>6.2f}% {pf:>6.2f} "
                    f"{s['avg_holding_days']:>7.1f}d ${s['sum_realized_pnl']:>11,.0f}")
    logger.info("")
    logger.info("── By DOMINANT regime (holding-days weighted) ──")
    logger.info(f"{'Regime':14s} {'N':>3s} {'Win%':>6s} {'AvgRet':>7s} {'PF':>6s}")
    for r in ["UPTREND", "SIDEWAYS", "DOWNTREND", "UNKNOWN"]:
        s = dominant_attribution.get(r)
        if not s or s["trades"] == 0:
            continue
        pf = s['profit_factor'] if s['profit_factor'] is not None else 0
        logger.info(f"{r:14s} {s['trades']:>3d} {s['win_rate_pct'] or 0:>5.1f}% "
                    f"{s['avg_return_pct'] or 0:>6.2f}% {pf:>6.2f}")
    logger.info("")
    logger.info(f"Output: {OUT_FILE}")
    logger.info("")
    logger.info("Key question: does E1 only work in UPTREND, or also defend in")
    logger.info("SIDEWAYS / DOWNTREND? See win rate and PF per regime above.")
    logger.info("")
    logger.info("NOTE: trade-level only. Equity-level (daily return/MaxDD by")
    logger.info("regime) needs full 5-year backtest with continuous daily equity.")


if __name__ == "__main__":
    main()
