"""
scripts/build_weekly_regimes.py

Build weekly SPX market regime classification per
E1_5Y_REGIME_VALIDATION_SPEC_v1.0 §5.

Independence: uses ONLY SPX weekly closes. No E1, no Leader Score,
no future data.

Weekly construction (§5.2):
  - Week = exchange trading week
  - Week close = SPX close on last trading day of week
  - MA10W = SMA of last 10 complete weekly closes
  - MA40W = SMA of last 40 complete weekly closes
  - MA40W_SLOPE_13W = MA40W[t] / MA40W[t-13] - 1
  - State computed at week-end applies to NEXT trading week (1-week lag)

Regimes (§5.3):
  UPTREND   : CloseW > MA40W AND MA10W > MA40W AND SLOPE > 0
  DOWNTREND : CloseW < MA40W AND MA10W < MA40W AND SLOPE < 0
  SIDEWAYS  : all other valid combinations (incl. direction conflicts/transitions)
  UNCLASSIFIED : insufficient history

Outputs:
  data/research/e1_5y/regimes/spx_weekly_regimes.json
  data/research/e1_5y/regimes/spx_regime_episodes.json
  data/research/e1_5y/regimes/spx_regime_daily.json   (daily date -> effective regime)
  data/research/e1_5y/regimes/regime_summary.json
"""
import json, logging
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)-5s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

VALID_START = "2021-06-11"
VALID_END   = "2026-06-11"
SPX_FILE    = Path("data/research/e1_5y/raw/indices/SPX.json")
OUT_DIR     = Path("data/research/e1_5y/regimes")

# ── NYSE holidays (for week-end detection) ───────────────────
NYSE_HOLIDAYS = {
    date(2020,1,1), date(2020,1,20), date(2020,2,17), date(2020,4,10),
    date(2020,5,25), date(2020,7,3), date(2020,9,7), date(2020,11,26), date(2020,12,25),
    date(2021,1,1), date(2021,1,18), date(2021,2,15), date(2021,4,2),
    date(2021,5,31), date(2021,7,5), date(2021,9,6), date(2021,11,25), date(2021,12,24),
    date(2022,1,17), date(2022,2,21), date(2022,4,15),
    date(2022,5,30), date(2022,6,20), date(2022,7,4), date(2022,9,5),
    date(2022,11,24), date(2022,12,26),
    date(2023,1,2), date(2023,1,16), date(2023,2,20), date(2023,4,7),
    date(2023,5,29), date(2023,6,19), date(2023,7,4), date(2023,9,4),
    date(2023,11,23), date(2023,12,25),
    date(2024,1,1), date(2024,1,15), date(2024,2,19), date(2024,3,29),
    date(2024,5,27), date(2024,6,19), date(2024,7,4), date(2024,9,2),
    date(2024,11,28), date(2024,12,25),
    date(2025,1,1), date(2025,1,20), date(2025,2,17), date(2025,4,18),
    date(2025,5,26), date(2025,6,19), date(2025,7,4), date(2025,9,1),
    date(2025,11,27), date(2025,12,25),
    date(2026,1,1), date(2026,1,19), date(2026,2,16), date(2026,4,3),
    date(2026,5,25), date(2026,6,19), date(2026,7,3), date(2026,9,7),
    date(2026,11,26), date(2026,12,25),
}

def is_trading_day(d: date) -> bool:
    return d.weekday() < 5 and d not in NYSE_HOLIDAYS

def sma(values: list, n: int) -> float:
    if len(values) < n:
        return None
    return sum(values[-n:]) / n


def load_spx() -> list:
    if not SPX_FILE.exists():
        logger.error(f"{SPX_FILE} not found — run fetch_e1_5y_data.py first")
        raise SystemExit(1)
    data = json.load(open(SPX_FILE))
    bars = data.get("bars", [])
    return sorted(bars, key=lambda r: r["date"])


def build_weekly_closes(bars: list) -> list:
    """
    Group daily bars into ISO weeks, take last trading day's close per week.
    Returns [{week_end_date, iso_year, iso_week, close}].
    """
    by_week = {}
    for r in bars:
        d = date.fromisoformat(r["date"])
        iso_year, iso_week, _ = d.isocalendar()
        key = (iso_year, iso_week)
        # Keep the latest date in the week
        if key not in by_week or r["date"] > by_week[key]["date"]:
            by_week[key] = r

    weekly = []
    for (iy, iw), r in sorted(by_week.items()):
        weekly.append({
            "week_end_date": r["date"],
            "iso_year":      iy,
            "iso_week":      iw,
            "close":         r["close"],
        })
    return weekly


def classify_regimes(weekly: list) -> list:
    """
    For each week, compute MA10W, MA40W, SLOPE_13W and classify.
    Returns weekly list with regime + indicators added.
    """
    closes = [w["close"] for w in weekly]
    result = []

    for i, w in enumerate(weekly):
        closes_so_far = closes[:i+1]
        ma10  = sma(closes_so_far, 10)
        ma40  = sma(closes_so_far, 40)
        close = w["close"]

        # SLOPE needs MA40W now AND MA40W 13 weeks ago
        slope = None
        if ma40 is not None and i >= 13:
            closes_13ago = closes[:i+1-13]
            ma40_13ago   = sma(closes_13ago, 40)
            if ma40_13ago and ma40_13ago > 0:
                slope = ma40 / ma40_13ago - 1

        # Classify
        if ma10 is None or ma40 is None or slope is None:
            regime   = "UNCLASSIFIED"
            subclass = None
        elif close > ma40 and ma10 > ma40 and slope > 0:
            regime   = "UPTREND"
            subclass = None
        elif close < ma40 and ma10 < ma40 and slope < 0:
            regime   = "DOWNTREND"
            subclass = None
        else:
            regime = "SIDEWAYS"
            # Transition subclass per spec
            if close > ma40 and ma10 > ma40 and slope <= 0:
                subclass = "RECOVERY_TRANSITION"
            elif close < ma40 and ma10 < ma40 and slope >= 0:
                subclass = "DETERIORATION_TRANSITION"
            else:
                subclass = "MA_CONFLICT"

        result.append({
            **w,
            "ma10w":            round(ma10, 4) if ma10 else None,
            "ma40w":            round(ma40, 4) if ma40 else None,
            "ma40w_slope_13w":  round(slope, 6) if slope is not None else None,
            "regime":           regime,
            "subclass":         subclass,
        })

    return result


def build_daily_regime_map(weekly_regimes: list, bars: list) -> dict:
    """
    Map each trading day to its effective regime.
    Day d uses the regime computed from the week ENDING BEFORE d's week.
    """
    # Build week-end → regime lookup
    week_ends = [(date.fromisoformat(w["week_end_date"]), w["regime"], w["subclass"])
                 for w in weekly_regimes]
    week_ends.sort()

    daily = {}
    for r in bars:
        d = date.fromisoformat(r["date"])
        # Find the most recent week-end strictly before this week's start
        # = last week-end that is < Monday of d's week
        monday = d - timedelta(days=d.weekday())
        applicable = None
        for we, regime, subclass in week_ends:
            if we < monday:
                applicable = (regime, subclass)
            else:
                break
        if applicable:
            daily[r["date"]] = {"regime": applicable[0], "subclass": applicable[1]}
        else:
            daily[r["date"]] = {"regime": "UNCLASSIFIED", "subclass": None}

    return daily


def build_episodes(daily: dict, bars: list) -> list:
    """
    Group consecutive same-regime trading days into episodes (§5.4).
    Compute SPX return per episode.
    """
    close_by_date = {r["date"]: r["close"] for r in bars}
    sorted_dates  = sorted(daily.keys())

    episodes = []
    cur_regime  = None
    cur_start   = None
    cur_dates   = []

    def close_episode(regime, dates):
        if not dates:
            return None
        start, end = dates[0], dates[-1]
        c0, c1 = close_by_date.get(start), close_by_date.get(end)
        spx_ret = (c1 / c0 - 1) * 100 if c0 and c1 else None
        return {
            "regime":       regime,
            "start_date":   start,
            "end_date":     end,
            "trading_days": len(dates),
            "spx_return_pct": round(spx_ret, 2) if spx_ret is not None else None,
        }

    for d in sorted_dates:
        regime = daily[d]["regime"]
        if regime != cur_regime:
            if cur_regime is not None:
                ep = close_episode(cur_regime, cur_dates)
                if ep:
                    episodes.append(ep)
            cur_regime = regime
            cur_dates  = [d]
        else:
            cur_dates.append(d)

    if cur_dates:
        ep = close_episode(cur_regime, cur_dates)
        if ep:
            episodes.append(ep)

    return episodes


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    bars = load_spx()
    logger.info(f"SPX bars: {len(bars)} ({bars[0]['date']} → {bars[-1]['date']})")

    # 1. Weekly closes
    weekly = build_weekly_closes(bars)
    logger.info(f"Weekly closes: {len(weekly)} weeks")

    # 2. Classify
    weekly_regimes = classify_regimes(weekly)
    classified = [w for w in weekly_regimes if w["regime"] != "UNCLASSIFIED"]
    logger.info(f"Classified weeks: {len(classified)}/{len(weekly_regimes)}")

    # 3. Daily map (with 1-week lag)
    daily = build_daily_regime_map(weekly_regimes, bars)

    # 4. Coverage stats (within validation window only)
    valid_daily = {d: v for d, v in daily.items()
                   if VALID_START <= d <= VALID_END}

    # 5. Episodes — built from valid_daily so cross-boundary episodes are clipped
    valid_bars = [r for r in bars if VALID_START <= r["date"] <= VALID_END]
    valid_episodes = build_episodes(valid_daily, valid_bars)
    # Also keep full-range episodes for the full output file
    episodes = build_episodes(daily, bars)

    # Episode counts by regime (validation window)
    ep_by_regime = {}
    for e in valid_episodes:
        ep_by_regime[e["regime"]] = ep_by_regime.get(e["regime"], 0) + 1
    regime_days = {}
    subclass_days = {}
    for d, v in valid_daily.items():
        regime_days[v["regime"]] = regime_days.get(v["regime"], 0) + 1
        if v["subclass"]:
            subclass_days[v["subclass"]] = subclass_days.get(v["subclass"], 0) + 1

    total_valid = len(valid_daily)
    regime_pct = {r: round(n/total_valid*100, 1) for r, n in regime_days.items()}

    # ── Save outputs ───────────────────────────────────────
    json.dump({
        "generated_at":   datetime.now(timezone.utc).isoformat(),
        "spec_version":   "E1_5Y_REGIME_VALIDATION_SPEC_v1.0",
        "independence":   "SPX weekly closes only — no E1, no future data",
        "validation_window": {"start": VALID_START, "end": VALID_END},
        "weekly_regimes": weekly_regimes,
    }, open(OUT_DIR / "spx_weekly_regimes.json", "w"), indent=2)

    json.dump({
        "generated_at":   datetime.now(timezone.utc).isoformat(),
        "validation_window": {"start": VALID_START, "end": VALID_END},
        "total_episodes": len(valid_episodes),
        "episodes":       valid_episodes,
    }, open(OUT_DIR / "spx_regime_episodes.json", "w"), indent=2)

    json.dump({
        "generated_at":   datetime.now(timezone.utc).isoformat(),
        "validation_window": {"start": VALID_START, "end": VALID_END},
        "daily_regime":   daily,
    }, open(OUT_DIR / "spx_regime_daily.json", "w"), indent=2)

    # regime_summary.json
    unclassified_days = regime_days.get("UNCLASSIFIED", 0)
    pass_checks = {
        "no_unclassified_in_validation": unclassified_days == 0,
        "has_uptrend":   regime_days.get("UPTREND", 0)   > 0,
        "has_sideways":  regime_days.get("SIDEWAYS", 0)  > 0,
        "has_downtrend": regime_days.get("DOWNTREND", 0) > 0,
    }
    json.dump({
        "generated_at":           datetime.now(timezone.utc).isoformat(),
        "spec_version":           "E1_5Y_REGIME_VALIDATION_SPEC_v1.0",
        "validation_window":      {"start": VALID_START, "end": VALID_END},
        "total_trading_days":     total_valid,
        "regime_days":            regime_days,
        "regime_pct":             regime_pct,
        "subclass_days":          subclass_days,
        "episode_count_by_regime": ep_by_regime,
        "total_episodes":         len(valid_episodes),
        "unclassified_days":      unclassified_days,
        "pass_checks":            pass_checks,
        "note": "Regime classification uses SPX weekly closes only and applies one-week lag.",
    }, open(OUT_DIR / "regime_summary.json", "w"), indent=2)

    # ── Summary ────────────────────────────────────────────
    logger.info("\n" + "=" * 60)
    logger.info("WEEKLY SPX REGIME CLASSIFICATION")
    logger.info("=" * 60)
    logger.info(f"Validation window: {VALID_START} → {VALID_END}")
    logger.info(f"Total trading days: {total_valid}")
    logger.info("")
    logger.info("Regime distribution (validation window):")
    for r in ["UPTREND", "SIDEWAYS", "DOWNTREND", "UNCLASSIFIED"]:
        n = regime_days.get(r, 0)
        pct = regime_pct.get(r, 0)
        logger.info(f"  {r:14s} {n:5d} days  {pct:5.1f}%")
    logger.info("")
    logger.info("SIDEWAYS subclass breakdown:")
    for sc, n in sorted(subclass_days.items()):
        logger.info(f"  {sc:24s} {n:5d} days")
    logger.info("")
    logger.info(f"Episodes (validation window): {len(valid_episodes)}")
    for e in valid_episodes:
        pass  # ep_by_regime already computed above
    for r, n in sorted(ep_by_regime.items()):
        logger.info(f"  {r:14s} {n} episodes")
    logger.info("")
    logger.info("Outputs:")
    logger.info(f"  {OUT_DIR / 'spx_weekly_regimes.json'}")
    logger.info(f"  {OUT_DIR / 'spx_regime_episodes.json'}")
    logger.info(f"  {OUT_DIR / 'spx_regime_daily.json'}")
    logger.info(f"  {OUT_DIR / 'regime_summary.json'}")
    logger.info("")
    logger.info("NOTE: Regime classification only. E1 backtest NOT run.")
    logger.info("      Next: slice E1 trades and equity by regime.")


if __name__ == "__main__":
    main()
