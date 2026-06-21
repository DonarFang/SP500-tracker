"""
scripts/fetch_e1_5y_data.py
E1 Five-Year Data Fetch — Current Constituents Preliminary

Usage:
  python3 scripts/fetch_e1_5y_data.py               # fetch all
  python3 scripts/fetch_e1_5y_data.py --retry-failed # retry failed only
  python3 scripts/fetch_e1_5y_data.py --audit-only   # audit existing data
  python3 scripts/fetch_e1_5y_data.py --force AAPL   # force re-fetch one symbol

dataset_mode: CURRENT_CONSTITUENTS_PRELIMINARY
survivorship_bias: true
formal_pass_fail_allowed: false
"""
import argparse, json, time, hashlib, logging, math, os, sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)-5s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────
SCHEMA_VERSION        = "1.0"
DATASET_MODE          = "CURRENT_CONSTITUENTS_PRELIMINARY"
FETCH_START           = "2020-04-01"
VALID_START           = "2021-06-11"
VALID_END             = "2026-06-11"
SOURCE                = "Yahoo Finance"
PRICE_ADJUSTMENT      = "auto_adjust=True (splits and dividends)"

SPX_COVERAGE_MIN      = 0.995
STOCK_COVERAGE_MIN    = 0.980
LATE_LISTING_GRACE    = 0.50   # stocks with < 50% coverage flagged LATE_LISTING
MAX_RETRIES           = 3
RETRY_DELAY_BASE      = 2.0
BATCH_DELAY           = 0.35

# MA40W_SLOPE_13W needs 40+13=53 complete weeks before VALID_START
MA_WEEKS_REQUIRED     = 53

BASE_DIR              = Path("data/research/e1_5y")
RAW_STOCKS_DIR        = BASE_DIR / "raw" / "stocks"
RAW_INDICES_DIR       = BASE_DIR / "raw" / "indices"
CONSTITUENTS_DIR      = BASE_DIR / "constituents"
MANIFEST_FILE         = BASE_DIR / "download_manifest.json"
AUDIT_FILE            = BASE_DIR / "data_audit.json"

INDICES = {
    "SPX": "^GSPC",
    "NDX": "^NDX",
    "SOX": "^SOX",
}

# Ticker mapping: SP500 symbol → Yahoo Finance ticker
TICKER_MAP = {
    "BRK.B": "BRK-B",
    "BF.B":  "BF-B",
    "GOOGL": "GOOGL",
    "GOOG":  "GOOG",
}

def to_yahoo_ticker(symbol: str) -> str:
    return TICKER_MAP.get(symbol, symbol.replace(".", "-"))


# ── Utilities ────────────────────────────────────────────────
def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]

def atomic_write_json(path: Path, data: dict) -> None:
    """Write JSON atomically via temp file → rename."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f)
        tmp.replace(path)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise

def load_spx_trading_days() -> list[str]:
    """Load SPX trading days from raw index file."""
    spx_path = RAW_INDICES_DIR / "SPX.json"
    if not spx_path.exists():
        return []
    data = json.load(open(spx_path))
    return [r["date"] for r in data.get("bars", [])]


# ── NYSE Trading Day Calendar ────────────────────────────────
NYSE_HOLIDAYS = {
    # 2020
    date(2020,1,1), date(2020,1,20), date(2020,2,17), date(2020,4,10),
    date(2020,5,25), date(2020,7,3), date(2020,9,7), date(2020,11,26), date(2020,12,25),
    # 2021
    date(2021,1,1), date(2021,1,18), date(2021,2,15), date(2021,4,2),
    date(2021,5,31), date(2021,7,5), date(2021,9,6), date(2021,11,25), date(2021,12,24),
    # 2022
    date(2022,1,17), date(2022,2,21), date(2022,4,15),
    date(2022,5,30), date(2022,6,20), date(2022,7,4), date(2022,9,5),
    date(2022,11,24), date(2022,12,26),
    # 2023
    date(2023,1,2), date(2023,1,16), date(2023,2,20), date(2023,4,7),
    date(2023,5,29), date(2023,6,19), date(2023,7,4), date(2023,9,4),
    date(2023,11,23), date(2023,12,25),
    # 2024
    date(2024,1,1), date(2024,1,15), date(2024,2,19), date(2024,3,29),
    date(2024,5,27), date(2024,6,19), date(2024,7,4), date(2024,9,2),
    date(2024,11,28), date(2024,12,25),
    # 2025
    date(2025,1,1), date(2025,1,20), date(2025,2,17), date(2025,4,18),
    date(2025,5,26), date(2025,6,19), date(2025,7,4), date(2025,9,1),
    date(2025,11,27), date(2025,12,25),
    # 2026
    date(2026,1,1), date(2026,1,19), date(2026,2,16), date(2026,4,3),
    date(2026,5,25), date(2026,6,19), date(2026,7,3), date(2026,9,7),
    date(2026,11,26), date(2026,12,25),
}

def is_trading_day(d: date) -> bool:
    return d.weekday() < 5 and d not in NYSE_HOLIDAYS

def count_trading_days_range(start: str, end: str) -> int:
    cur = date.fromisoformat(start)
    end_d = date.fromisoformat(end)
    count = 0
    while cur <= end_d:
        if is_trading_day(cur):
            count += 1
        cur += timedelta(days=1)
    return count

def get_week_end_dates(start: str, end: str) -> list[date]:
    """Return the last trading day of each calendar week in range."""
    cur   = date.fromisoformat(start)
    end_d = date.fromisoformat(end)
    weeks = []
    while cur <= end_d:
        # Advance to Friday of this week
        week_end = cur + timedelta(days=(4 - cur.weekday()) % 7)
        # If Friday is holiday, back up to last trading day
        while week_end >= cur and not is_trading_day(week_end):
            week_end -= timedelta(days=1)
        if cur <= week_end <= end_d:
            weeks.append(week_end)
        cur = week_end + timedelta(days=3)  # jump to Monday next week
    return weeks

def compute_first_ma40w_slope_date(spx_bars: list[dict]) -> tuple[Optional[str], Optional[str]]:
    """
    Find the first date where MA40W_SLOPE_13W can be computed.
    Requires 40 weeks for MA40W and 13 additional weeks for slope.
    All weeks must be complete (last trading day of week).
    """
    week_ends = get_week_end_dates(FETCH_START, VALID_END)
    bar_by_date = {r["date"]: r["close"] for r in spx_bars}

    # Find week-end closes
    weekly_closes = []
    for wd in week_ends:
        ds = wd.isoformat()
        if ds in bar_by_date:
            weekly_closes.append((ds, bar_by_date[ds]))

    # Need at least 40+13=53 weeks
    if len(weekly_closes) < 53:
        return None

    # First date where both MA40W[t] and MA40W[t-13] are available
    # MA40W[t] needs weeks[t-39..t], MA40W[t-13] needs weeks[t-52..t-13]
    # So first valid t = index 52 (0-based)
    if len(weekly_closes) < 53:
        return None, None
    first_slope_date = weekly_closes[52][0]

    # Per spec §5.2: state computed at end of week t applies starting NEXT week
    # So first_effective_regime_date = start of week 54 (week after slope computable)
    # = the Monday after weekly_closes[52]
    slope_date_obj = date.fromisoformat(first_slope_date)
    days_to_monday = (7 - slope_date_obj.weekday()) % 7
    if days_to_monday == 0:
        days_to_monday = 7
    effective_date_obj = slope_date_obj + timedelta(days=days_to_monday)
    # Advance to next trading day if Monday is holiday
    while not is_trading_day(effective_date_obj):
        effective_date_obj += timedelta(days=1)

    return first_slope_date, effective_date_obj.isoformat()


# ── OHLCV Validation ─────────────────────────────────────────
def validate_ohlcv(bars: list[dict], symbol: str) -> tuple[int, list[str]]:
    errors = []
    for r in bars:
        o, h, l, c = r.get("open"), r.get("high"), r.get("low"), r.get("close")
        if None in (o, h, l, c):
            errors.append(f"{r['date']}: missing field")
            continue
        if h < l:
            errors.append(f"{r['date']}: high({h}) < low({l})")
        if c <= 0 or o <= 0 or h <= 0 or l <= 0:
            errors.append(f"{r['date']}: non-positive price")
        # Extreme gap: close > 10x high or close < 0.1x low (adjusted data edge case)
        if h > 0 and c > h * 2:
            errors.append(f"{r['date']}: close({c}) > 2x high({h}) — suspicious")
    return len(errors), errors[:10]  # cap reported errors at 10

def check_duplicate_dates(bars: list[dict]) -> list[str]:
    seen, dupes = set(), []
    for r in bars:
        d = r["date"]
        if d in seen:
            dupes.append(d)
        seen.add(d)
    return dupes


# ── Cache Validation ─────────────────────────────────────────
def validate_cache(path: Path, symbol: str) -> tuple[bool, str]:
    """
    Returns (is_valid, reason).
    Valid only if all 6 conditions pass.
    """
    if not path.exists():
        return False, "FILE_NOT_FOUND"
    try:
        data = json.load(open(path))
    except Exception as e:
        return False, f"PARSE_ERROR: {e}"

    if data.get("schema_version") != SCHEMA_VERSION:
        return False, f"SCHEMA_VERSION_MISMATCH: {data.get('schema_version')}"
    if data.get("symbol") != symbol:
        return False, f"SYMBOL_MISMATCH: {data.get('symbol')}"
    if data.get("requested_start") != FETCH_START:
        return False, f"START_MISMATCH: {data.get('requested_start')}"
    bars = data.get("bars", [])
    if not bars:
        return False, "EMPTY_BARS"

    # Must cover frozen validation end date
    last_date = bars[-1]["date"]
    if last_date < VALID_END:
        return False, f"DOES_NOT_COVER_VALID_END: data_end={last_date} < {VALID_END}"

    # Check data is recent (within 10 calendar days of today)
    days_old = (date.today() - date.fromisoformat(last_date)).days
    if days_old > 10:
        return False, f"STALE: last_date={last_date} ({days_old}d ago)"

    # Quick OHLCV check
    invalid_count, _ = validate_ohlcv(bars[:20], symbol)  # spot check first 20
    if invalid_count > 0:
        return False, f"OHLCV_INVALID: {invalid_count} errors in first 20 bars"

    dupes = check_duplicate_dates(bars[:50])
    if dupes:
        return False, f"DUPLICATE_DATES: {dupes[:3]}"

    return True, "OK"


# ── Fetch ─────────────────────────────────────────────────────
def fetch_ticker(yahoo_ticker: str, start: str, end: str) -> tuple[list, dict]:
    """
    Returns (bars, fetch_meta).
    bars: [{date, open, high, low, close, volume}]
    fetch_meta: {attempts, last_attempt_at, error_type, error_message, retryable}
    """
    try:
        import yfinance as yf
    except ImportError:
        raise RuntimeError("yfinance not installed: pip install yfinance")

    meta = {"attempts": 0, "last_attempt_at": None,
            "error_type": None, "error_message": None, "retryable": False}

    for attempt in range(1, MAX_RETRIES + 1):
        meta["attempts"]        = attempt
        meta["last_attempt_at"] = now_iso()
        try:
            tk   = yf.Ticker(yahoo_ticker)
            hist = tk.history(start=start, end=end,
                              auto_adjust=True, actions=True)
            if hist.empty:
                meta["error_type"]    = "EMPTY_RESPONSE"
                meta["error_message"] = "yfinance returned empty DataFrame"
                meta["retryable"]     = True
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY_BASE * attempt)
                    continue
                return [], meta

            bars = []
            for dt, row in hist.iterrows():
                bars.append({
                    "date":   dt.strftime("%Y-%m-%d"),
                    "open":   round(float(row["Open"]),   6),
                    "high":   round(float(row["High"]),   6),
                    "low":    round(float(row["Low"]),    6),
                    "close":  round(float(row["Close"]),  6),
                    "volume": int(row.get("Volume", 0) or 0),
                })
            bars.sort(key=lambda r: r["date"])
            return bars, meta

        except Exception as e:
            meta["error_type"]    = type(e).__name__
            meta["error_message"] = str(e)
            meta["retryable"]     = True
            if attempt < MAX_RETRIES:
                logger.debug(f"Attempt {attempt} failed for {yahoo_ticker}: {e}")
                time.sleep(RETRY_DELAY_BASE * attempt)
            else:
                return [], meta

    return [], meta


# ── Main logic ────────────────────────────────────────────────
def load_constituents(override_path: Optional[str] = None) -> list[str]:
    """
    Load universe from canonical constituents file.
    Falls back to data/prices/ only if no canonical file exists.
    Stocks missing from data/prices/ will still be in the universe
    and recorded as FETCH_FAILED if download fails.
    """
    # Try explicit snapshot first; otherwise use canonical sources.
    if override_path:
        override = Path(override_path)
        if not override.exists():
            raise FileNotFoundError(
                f"Constituents file not found: {override}"
            )
        candidates = [override]
    else:
        candidates = [
            Path("data/sp500_constituents.json"),
            Path("data/members.json"),
            Path("data/constituents.json"),
        ]
    for path in candidates:
        if path.exists():
            try:
                data = json.load(open(path))
                # Handle various formats
                if isinstance(data, list):
                    syms = sorted(str(s) for s in data if s)
                elif isinstance(data, dict):
                    syms = sorted(
                        data.get("symbols") or
                        data.get("tickers") or
                        data.get("constituents") or
                        [k for k in data if not k.startswith("_")]
                    )
                else:
                    continue
                if syms:
                    logger.info(f"Loaded {len(syms)} constituents from {path}")
                    return syms
            except Exception as e:
                logger.warning(f"Could not load {path}: {e}")

    # Fallback: data/prices/ (records data availability bias — warn loudly)
    existing = Path("data/prices")
    if existing.exists():
        syms = sorted(f.stem for f in existing.glob("*.json")
                      if not f.stem.startswith("_"))
        logger.warning(
            f"⚠️  No canonical constituents file found. "
            f"Using data/prices/ ({len(syms)} symbols). "
            f"This may undercount the true universe — "
            f"stocks without price files will be silently excluded."
        )
        return syms

    logger.error("No constituents source found")
    sys.exit(1)

def process_symbol(symbol: str, force: bool = False) -> dict:
    """Fetch, validate and save one stock. Returns result dict."""
    yahoo = to_yahoo_ticker(symbol)
    path  = RAW_STOCKS_DIR / f"{symbol}.json"

    # Cache check (unless forced)
    if not force:
        valid, reason = validate_cache(path, symbol)
        if valid:
            data = json.load(open(path))
            return {
                "status":   "SKIPPED_CACHED",
                "bars":     len(data["bars"]),
                "start":    data["bars"][0]["date"],
                "end":      data["bars"][-1]["date"],
                "yahoo":    yahoo,
            }
        elif path.exists():
            logger.debug(f"{symbol}: cache invalid ({reason}) — re-fetching")

    # Fetch
    bars, fetch_meta = fetch_ticker(yahoo, FETCH_START, date.today().isoformat())

    if not bars:
        return {
            "status":         "FAILED",
            "yahoo":          yahoo,
            "error_type":     fetch_meta.get("error_type"),
            "error_message":  fetch_meta.get("error_message"),
            "attempts":       fetch_meta.get("attempts"),
            "last_attempt_at": fetch_meta.get("last_attempt_at"),
            "retryable":      fetch_meta.get("retryable", True),
        }

    # Validate
    invalid_count, invalid_errors = validate_ohlcv(bars, symbol)
    dupes = check_duplicate_dates(bars)

    # Compute coverage over validation window
    expected = count_trading_days_range(VALID_START, VALID_END)
    in_window = sum(1 for r in bars if VALID_START <= r["date"] <= VALID_END
                    and is_trading_day(date.fromisoformat(r["date"])))
    coverage  = in_window / expected if expected > 0 else 0

    # Classify late listing vs data incomplete
    first_date  = bars[0]["date"]
    # LATE_LISTING_CANDIDATE: first bar is after validation start (truly listed late)
    # DATA_INCOMPLETE: first bar is early but coverage is low (data gaps, not IPO)
    late_listing_candidate = first_date > VALID_START
    data_incomplete        = (not late_listing_candidate
                              and coverage < STOCK_COVERAGE_MIN
                              and first_date <= FETCH_START)
    late_listing = late_listing_candidate  # rename for downstream compat

    data = {
        "schema_version":           SCHEMA_VERSION,
        "dataset_mode":             DATASET_MODE,
        "survivorship_bias":        True,
        "formal_pass_fail_allowed": False,
        "symbol":                   symbol,
        "yahoo_ticker":             yahoo,
        "source":                   SOURCE,
        "price_adjustment":         PRICE_ADJUSTMENT,
        "requested_start":          FETCH_START,
        "requested_end":            date.today().isoformat(),
        "data_start":               bars[0]["date"],
        "data_end":                 bars[-1]["date"],
        "downloaded_at":            now_iso(),
        "bars":                     bars,
    }

    # Atomic write
    status = "OK"
    if invalid_count > 0 or dupes:
        status = "WARN"
    if invalid_count > 5:
        status = "INVALID"

    if status != "INVALID":
        try:
            atomic_write_json(path, data)
        except Exception as e:
            return {"status": "WRITE_FAILED", "error_message": str(e)}

    sha = file_sha256(path) if path.exists() else None

    return {
        "status":          status,
        "yahoo":           yahoo,
        "bars":            len(bars),
        "start":           bars[0]["date"],
        "end":             bars[-1]["date"],
        "in_window":       in_window,
        "coverage":        round(coverage, 4),
        "invalid_ohlc":    invalid_count,
        "invalid_errors":  invalid_errors,
        "duplicate_dates": dupes,
        "late_listing":              late_listing,
        "late_listing_candidate":    late_listing_candidate,
        "data_incomplete":           data_incomplete,
        "sha":             sha,
        "attempts":        fetch_meta.get("attempts"),
    }


def run_audit(constituents: list[str]) -> dict:
    """Compute full audit from saved files."""
    spx_bars_file = RAW_INDICES_DIR / "SPX.json"
    spx_bars      = []
    if spx_bars_file.exists():
        spx_data = json.load(open(spx_bars_file))
        spx_bars = spx_data.get("bars", [])

    spx_dates = [r["date"] for r in spx_bars]
    expected_valid = count_trading_days_range(VALID_START, VALID_END)
    expected_fetch = count_trading_days_range(FETCH_START, date.today().isoformat())

    spx_in_valid = sum(1 for d in spx_dates if VALID_START <= d <= VALID_END)
    spx_coverage = spx_in_valid / expected_valid if expected_valid else 0

    # MA40W slope feasibility
    first_slope_date, first_effective_date = compute_first_ma40w_slope_date(spx_bars)
    warmup_days      = count_trading_days_range(FETCH_START, VALID_START)
    weeks_before     = len(get_week_end_dates(FETCH_START, VALID_START))
    # Feasible only if effective regime date is ON OR BEFORE validation start
    # (state from week ending before VALID_START must already be computable)
    slope_feasible   = (first_effective_date is not None
                        and first_effective_date <= VALID_START)

    # Stock stats — classify each symbol
    coverages_all       = []   # all valid symbols
    coverages_excl_late = []   # excluding LATE_LISTING
    below_98, late_listings, data_incomplete, fetch_failed = [], [], [], []
    invalid_total, dupe_total = 0, 0
    ok_count = fail_count = 0

    for sym in constituents:
        path = RAW_STOCKS_DIR / f"{sym}.json"
        if not path.exists():
            fail_count += 1
            fetch_failed.append(sym)
            continue
        try:
            data = json.load(open(path))
            bars = data.get("bars", [])
            if not bars:
                fail_count += 1
                fetch_failed.append(sym)
                continue
            in_window = sum(1 for r in bars
                            if VALID_START <= r["date"] <= VALID_END
                            and is_trading_day(date.fromisoformat(r["date"])))
            cov = in_window / expected_valid if expected_valid else 0
            first_bar = bars[0]["date"]

            # Classify: LATE_LISTING if first bar is after validation start
            is_late = first_bar > VALID_START
            # DATA_INCOMPLETE: early first bar but low coverage (data gaps)
            is_incomplete = (not is_late
                             and cov < STOCK_COVERAGE_MIN
                             and first_bar <= FETCH_START)

            coverages_all.append(cov)
            if is_late:
                late_listings.append({
                    "symbol":    sym,
                    "coverage":  round(cov, 4),
                    "first_bar": first_bar,
                    "reason":    "LATE_LISTING",
                })
            elif is_incomplete:
                data_incomplete.append({
                    "symbol":   sym,
                    "coverage": round(cov, 4),
                    "first_bar": first_bar,
                    "reason":   "DATA_INCOMPLETE",
                })
                coverages_excl_late.append(cov)
                if cov < STOCK_COVERAGE_MIN:
                    below_98.append({"symbol": sym, "coverage": round(cov, 4),
                                     "classification": "DATA_INCOMPLETE"})
            else:
                coverages_excl_late.append(cov)
                if cov < STOCK_COVERAGE_MIN:
                    below_98.append({"symbol": sym, "coverage": round(cov, 4),
                                     "classification": "LOW_COVERAGE"})

            ic, _ = validate_ohlcv(bars, sym)
            invalid_total += ic
            dc = check_duplicate_dates(bars)
            dupe_total += len(dc)
            ok_count += 1
        except Exception as e:
            fail_count += 1
            fetch_failed.append(sym)

    avg_coverage_all       = sum(coverages_all) / len(coverages_all) if coverages_all else 0
    avg_coverage_excl_late = (sum(coverages_excl_late) / len(coverages_excl_late)
                               if coverages_excl_late else 0)
    # Pass criterion excludes LATE_LISTING (they simply don't have historical data)
    stocks_pass_excl_late  = (avg_coverage_excl_late >= STOCK_COVERAGE_MIN
                               and len([b for b in below_98
                                        if b["classification"] != "LATE_LISTING"]) <= 5)

    universe_size = len(constituents)
    availability_rate = (
        ok_count / universe_size if universe_size else 0
    )
    availability_pass = availability_rate >= STOCK_COVERAGE_MIN
    stocks_pass = availability_pass and stocks_pass_excl_late

    return {
        "generated_at":     now_iso(),
        "dataset_mode":     DATASET_MODE,
        "survivorship_bias": True,
        "formal_pass_fail_allowed": False,
        "fetch_range":      {"start": FETCH_START, "end": date.today().isoformat()},
        "validation_range": {"start": VALID_START, "end": VALID_END},
        "spx": {
            "total_bars":         len(spx_bars),
            "bars_in_valid_window": spx_in_valid,
            "expected_valid_days":  expected_valid,
            "coverage":           round(spx_coverage, 4),
            "pass":               spx_coverage >= SPX_COVERAGE_MIN,
            "PASS_THRESHOLD":     SPX_COVERAGE_MIN,
        },
        "stocks": {
            "universe_size":            len(constituents),
            "ok":                       ok_count,
            "failed":                   fail_count,
            "fetch_failed":             fetch_failed[:20],
            "availability_rate":        round(availability_rate, 4),
            "availability_pass":        availability_pass,
            "avg_coverage_all":         round(avg_coverage_all, 4),
            "avg_coverage_excl_late":   round(avg_coverage_excl_late, 4),
            "late_listings_count":      len(late_listings),
            "late_listings":            late_listings,
            "data_incomplete_count":    len(data_incomplete),
            "data_incomplete":          data_incomplete,
            "below_98pct_count":        len(below_98),
            "below_98pct":              sorted(below_98, key=lambda x: x["coverage"]),
            "coverage_pass_excl_late":  stocks_pass_excl_late,
            "pass":                     stocks_pass,
            "pass_note": (
                "PASS requires universe availability >= 98% and coverage "
                "excluding LATE_LISTING >= 98%. LATE_LISTING means first_bar "
                "after validation start 2021-06-11."
            ),
            "PASS_THRESHOLD":           STOCK_COVERAGE_MIN,
        },
        "data_quality": {
            "invalid_ohlc_total":    invalid_total,
            "duplicate_dates_total": dupe_total,
            "pass":                  invalid_total == 0 and dupe_total == 0,
        },
        "ma40w_slope": {
            "warmup_trading_days":      warmup_days,
            "complete_weeks_in_warmup": weeks_before,
            "required_weeks":           MA_WEEKS_REQUIRED,
            "first_slope_computable_date": first_slope_date,
            "first_effective_regime_date": first_effective_date,
            "effective_before_valid_start": (
                first_effective_date is not None
                and first_effective_date <= VALID_START
            ),
            "feasible":  slope_feasible,
            "note": ("MA40W_SLOPE_13W requires 53 complete weeks to compute. "
                     "Per spec §5.2, state computed at week-end applies from NEXT week. "
                     "first_effective_regime_date must be <= 2021-06-11."),
            "pass":      slope_feasible,
        },
        # overall_pass: ALL sub-checks must pass
        # Excludes LATE_LISTING from coverage calc (see stocks_excl_late below)
        "overall_pass": (
            spx_coverage >= SPX_COVERAGE_MIN
            and stocks_pass
            and invalid_total == 0
            and dupe_total == 0
            and slope_feasible
        ),
        "overall_status": (
            "PRELIMINARY_READY"
            if (spx_coverage >= SPX_COVERAGE_MIN
                and stocks_pass
                and invalid_total == 0
                and dupe_total == 0
                and slope_feasible)
            else "PRELIMINARY_WITH_WARNINGS"
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="E1 5Y Data Fetch")
    parser.add_argument("--retry-failed", action="store_true",
                        help="Retry only previously failed symbols")
    parser.add_argument("--audit-only",   action="store_true",
                        help="Run audit on existing data, no fetching")
    parser.add_argument("--force",        metavar="SYMBOL",
                        help="Force re-fetch one symbol (ignores cache)")
    parser.add_argument(
        "--constituents-file",
        metavar="PATH",
        help="Override constituent universe JSON file",
    )
    args = parser.parse_args()

    for d in [RAW_STOCKS_DIR, RAW_INDICES_DIR, CONSTITUENTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    constituents = load_constituents(args.constituents_file)

    # Save constituents list
    atomic_write_json(CONSTITUENTS_DIR / "current_constituents.json", {
        "dataset_mode":             DATASET_MODE,
        "survivorship_bias":        True,
        "formal_pass_fail_allowed": False,
        "generated_at":             now_iso(),
        "constituents_source":      (
            args.constituents_file or "canonical_auto_detect"
        ),
        "count":                    len(constituents),
        "symbols":                  constituents,
        "ticker_map":               {s: to_yahoo_ticker(s) for s in constituents
                                     if to_yahoo_ticker(s) != s},
        "note": ("Current SP500 members only. "
                 "Point-in-Time Constituents required for formal E1 PASS/FAIL."),
    })

    if args.audit_only:
        logger.info("── Audit only mode ──────────────────────────────")
        audit = run_audit(constituents)
        atomic_write_json(AUDIT_FILE, audit)
        _print_summary(audit, constituents)
        return

    # ── Fetch indices first ───────────────────────────────────
    if not args.retry_failed and not args.force:
        logger.info("── Fetching indices ─────────────────────────────")
        for name, ticker in INDICES.items():
            path = RAW_INDICES_DIR / f"{name}.json"
            valid, reason = validate_cache(path, name) if path.exists() else (False, "")
            if valid:
                logger.info(f"  {name}: cached ✓")
                continue
            logger.info(f"  {name} ({ticker}) ...")
            bars, meta = fetch_ticker(ticker, FETCH_START, date.today().isoformat())
            if not bars:
                logger.error(f"  ❌ {name}: {meta.get('error_message')}")
                continue
            atomic_write_json(path, {
                "schema_version":  SCHEMA_VERSION,
                "dataset_mode":    DATASET_MODE,
                "symbol":          name,
                "yahoo_ticker":    ticker,
                "source":          SOURCE,
                "requested_start": FETCH_START,
                "requested_end":   date.today().isoformat(),
                "data_start":      bars[0]["date"],
                "data_end":        bars[-1]["date"],
                "downloaded_at":   now_iso(),
                "bars":            bars,
            })
            logger.info(f"  ✅ {name}: {len(bars)} bars "
                        f"({bars[0]['date']} → {bars[-1]['date']})")
            time.sleep(BATCH_DELAY)

    # ── Determine symbols to process ──────────────────────────
    if args.force:
        sym = args.force.upper()
        if sym not in constituents:
            logger.error(f"{sym} not in constituents")
            sys.exit(1)
        to_process = [sym]
        force_set  = {sym}
    elif args.retry_failed:
        manifest = json.load(open(MANIFEST_FILE)) if MANIFEST_FILE.exists() else {}
        failed   = [r["symbol"] for r in manifest.get("failed", [])]
        to_process = [s for s in constituents if s in failed]
        force_set  = set(to_process)
        logger.info(f"Retrying {len(to_process)} previously failed symbols")
    else:
        to_process = constituents
        force_set  = set()

    # ── Fetch stocks ──────────────────────────────────────────
    results, failed_list = {}, []
    ok = cached = fail = warn = 0
    total = len(to_process)

    logger.info(f"── Fetching {total} stocks ──────────────────────────")
    for i, sym in enumerate(to_process, 1):
        res = process_symbol(sym, force=(sym in force_set))
        results[sym] = res
        status = res["status"]

        if status == "SKIPPED_CACHED":
            cached += 1
        elif status == "OK":
            ok += 1
            if i % 100 == 0 or i <= 3:
                logger.info(f"  [{i}/{total}] {sym}: {res['bars']} bars "
                            f"cov={res['coverage']:.1%}")
        elif status == "WARN":
            warn += 1
            logger.warning(f"  [{i}/{total}] {sym}: WARN "
                           f"invalid={res['invalid_ohlc']} dupes={res['duplicate_dates']}")
        else:
            fail += 1
            failed_list.append({
                "symbol":        sym,
                "error_type":    res.get("error_type"),
                "error_message": res.get("error_message"),
                "attempts":      res.get("attempts"),
                "last_attempt_at": res.get("last_attempt_at"),
                "retryable":     res.get("retryable", True),
            })
            logger.error(f"  [{i}/{total}] {sym}: FAILED — {res.get('error_message')}")

        time.sleep(BATCH_DELAY)

    # ── Save manifest ─────────────────────────────────────────
    atomic_write_json(MANIFEST_FILE, {
        "generated_at":  now_iso(),
        "dataset_mode":  DATASET_MODE,
        "fetch_range":   {"start": FETCH_START, "end": date.today().isoformat()},
        "counts":        {"ok": ok, "cached": cached, "warn": warn, "failed": fail},
        "results":       results,
        "failed":        failed_list,
    })

    # ── Audit ──────────────────────────────────────────────────
    logger.info("── Running full audit ───────────────────────────")
    audit = run_audit(constituents)
    atomic_write_json(AUDIT_FILE, audit)
    _print_summary(audit, constituents)

    size = sum(f.stat().st_size for f in BASE_DIR.rglob("*.json"))
    logger.info(f"Total size: {size / 1024 / 1024:.1f} MB")
    if failed_list:
        logger.info(f"To retry failures: python3 scripts/fetch_e1_5y_data.py --retry-failed")


def _print_summary(audit: dict, constituents: list) -> None:
    logger.info("\n" + "=" * 60)
    logger.info("DATA AUDIT — CURRENT_CONSTITUENTS_PRELIMINARY")
    logger.info("=" * 60)
    s = audit["spx"]
    logger.info(f"SPX coverage:           {s['coverage']:.1%}  "
                f"({'✅' if s['pass'] else '❌'} threshold={s['PASS_THRESHOLD']:.1%})")
    st = audit["stocks"]
    logger.info(f"Stocks OK:              {st['ok']}/{len(constituents)}")
    logger.info(f"Avg coverage (all):     {st['avg_coverage_all']:.1%}")
    logger.info(f"Avg coverage (ex-late): {st['avg_coverage_excl_late']:.1%}  "
                f"({'✅' if st['pass'] else '❌'})")
    logger.info(f"Below 98% (ex-late):    {st['below_98pct_count']}")
    logger.info(f"Late listings:          {st['late_listings_count']}  "
                f"(excluded from pass criterion)")
    logger.info(f"Data incomplete:        {st['data_incomplete_count']}")
    logger.info(f"Fetch failed:           {len(st['fetch_failed'])}")
    dq = audit["data_quality"]
    logger.info(f"Invalid OHLC:           {dq['invalid_ohlc_total']}  "
                f"({'✅' if dq['pass'] else '❌'})")
    logger.info(f"Duplicate dates:        {dq['duplicate_dates_total']}  "
                f"({'✅' if dq['pass'] else '❌'})")
    ma = audit["ma40w_slope"]
    logger.info(f"Warmup weeks:              {ma['complete_weeks_in_warmup']}  "
                f"(need {ma['required_weeks']})  "
                f"({'✅' if ma['feasible'] else '❌'})")
    logger.info(f"First slope computable:    {ma['first_slope_computable_date']}")
    logger.info(f"First effective regime:    {ma['first_effective_regime_date']}")
    logger.info(f"Effective before {VALID_START}: "
                f"{'✅ YES' if ma.get('effective_before_valid_start') else '❌ NO'}")
    status = audit.get("overall_status", "UNKNOWN")
    icon   = "✅" if audit["overall_pass"] else "⚠️ "
    logger.info(f"\nOverall:  {icon} {status}")
    logger.info(f"Audit file: {AUDIT_FILE}")
    logger.info("NOTE: CURRENT_CONSTITUENTS_PRELIMINARY — survivorship bias present.")
    logger.info("      Do NOT use for formal E1 PASS/FAIL.")


if __name__ == "__main__":
    main()
