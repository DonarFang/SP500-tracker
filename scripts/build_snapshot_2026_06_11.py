"""
scripts/build_snapshot_2026_06_11.py

Build the authoritative S&P 500 constituent snapshot for 2026-06-11.

Method:
  Base:    GitHub datasets/s-and-p-500-companies constituents.csv (2026-05-11)
  Delta:   Apply confirmed S&P changes between 2026-05-11 and 2026-06-11
  Exclude: Changes effective AFTER 2026-06-11 (e.g. MRVL/FLEX on 2026-06-22)

Outputs:
  data/research/e1_5y/constituents/constituents_base_2026-05-11.json
  data/research/e1_5y/constituents/constituent_changes_to_2026-06-11.json
  data/research/e1_5y/constituents/sp500_constituents_2026-06-11.json
"""
import csv, io, json, logging, urllib.request
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)-5s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

SNAPSHOT_DATE = "2026-06-11"
BASE_DATE     = "2026-05-11"
BASE_URL      = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
BASE_COMMIT   = "main"  # pin to commit SHA after download for reproducibility

CONSTITUENTS  = Path("data/research/e1_5y/constituents")
RAW_STOCKS    = Path("data/research/e1_5y/raw/stocks")
HIST_CAND     = Path("data/research/e1_5y/historical_candidates")
AUDIT_FILE    = Path("data/research/e1_5y/data_audit.json")

# ── Confirmed changes: 2026-05-11 → 2026-06-11 ───────────────────────────────
# Only include changes with effective_date <= 2026-06-11
# Source: S&P Dow Jones press releases
CHANGES = [
    {
        "effective_date": "2026-06-02",
        "action":         "ADD",
        "symbol":         "FDXF",
        "replaces":       "EPAM",
        "reason":         "EPAM removed from index",
        "source_url":     "https://press.spglobal.com/",
        "confirmed":      True,
    },
    {
        "effective_date": "2026-06-02",
        "action":         "REMOVE",
        "symbol":         "EPAM",
        "replaced_by":    "FDXF",
        "reason":         "Removed from S&P 500",
        "source_url":     "https://press.spglobal.com/",
        "confirmed":      True,
    },
    # ── Explicitly excluded (effective AFTER 2026-06-11) ──
    # MRVL ADD 2026-06-22  (source: press.spglobal.com/2026-06-05)
    # FLEX ADD 2026-06-22
    # POOL REMOVE 2026-06-22
    # These must NOT be applied to the 2026-06-11 snapshot.
]

ADDS    = {c["symbol"] for c in CHANGES if c["action"] == "ADD"    and c["confirmed"]}
REMOVES = {c["symbol"] for c in CHANGES if c["action"] == "REMOVE" and c["confirmed"]}


def atomic_write(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    tmp.replace(path)


def fetch_base_csv() -> tuple[list[str], str]:
    """Fetch constituents.csv from GitHub. Returns (tickers, raw_csv_text)."""
    logger.info(f"Fetching base CSV from {BASE_URL}")
    req  = urllib.request.Request(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=20)
    raw  = resp.read().decode("utf-8")
    reader  = csv.DictReader(io.StringIO(raw))
    rows    = list(reader)
    col_sym = next((c for c in rows[0] if "symbol" in c.lower() or "ticker" in c.lower()), None)
    if not col_sym:
        raise RuntimeError(f"No symbol column found. Columns: {list(rows[0].keys())}")
    tickers = [r[col_sym].strip().replace(".", "-") for r in rows if r.get(col_sym)]
    logger.info(f"Base CSV: {len(tickers)} symbols (column='{col_sym}')")
    return sorted(set(tickers)), raw


def main():
    # ── 1. Fetch base ─────────────────────────────────────
    base_tickers, base_csv_raw = fetch_base_csv()
    base_set = set(base_tickers)

    # Save base snapshot
    atomic_write(CONSTITUENTS / f"constituents_base_{BASE_DATE}.json", {
        "base_date":      BASE_DATE,
        "source":         "github.com/datasets/s-and-p-500-companies",
        "source_url":     BASE_URL,
        "commit":         BASE_COMMIT,
        "note":           "CSV last updated 2026-05-11. Pin to exact commit SHA for reproducibility.",
        "count":          len(base_tickers),
        "symbols":        base_tickers,
    })
    logger.info(f"Base snapshot saved: {len(base_tickers)} symbols")

    # ── 2. Apply confirmed changes ─────────────────────────
    snapshot_set = (base_set - REMOVES) | ADDS
    snapshot_set.discard("")
    snapshot = sorted(snapshot_set)

    logger.info(f"Applied changes: +{len(ADDS)} -{len(REMOVES)}")
    logger.info(f"Snapshot size: {len(snapshot)}")

    # ── 3. Verify excluded post-cutoff symbols not present ─
    POST_CUTOFF = {"MRVL", "FLEX"}   # effective 2026-06-22
    in_snapshot = POST_CUTOFF & snapshot_set
    if in_snapshot:
        logger.warning(f"⚠️  Post-cutoff symbols in snapshot: {in_snapshot} — removing")
        snapshot_set -= in_snapshot
        snapshot = sorted(snapshot_set)

    # ── 4. Save changes manifest ───────────────────────────
    atomic_write(CONSTITUENTS / "constituent_changes_to_2026-06-11.json", {
        "generated_at":     datetime.now(timezone.utc).isoformat(),
        "base_date":        BASE_DATE,
        "snapshot_date":    SNAPSHOT_DATE,
        "changes_applied":  CHANGES,
        "symbols_added":    sorted(ADDS),
        "symbols_removed":  sorted(REMOVES),
        "explicitly_excluded_post_cutoff": [
            {"symbol": "MRVL", "effective": "2026-06-22",
             "source": "press.spglobal.com/2026-06-05"},
            {"symbol": "FLEX", "effective": "2026-06-22",
             "source": "press.spglobal.com/2026-06-05"},
            {"symbol": "POOL", "effective": "2026-06-22",
             "source": "press.spglobal.com/2026-06-05"},
        ],
    })

    # ── 5. Save final snapshot ─────────────────────────────
    snap_path = CONSTITUENTS / f"sp500_constituents_{SNAPSHOT_DATE}.json"
    atomic_write(snap_path, {
        "snapshot_date":            SNAPSHOT_DATE,
        "dataset_mode":             "CURRENT_CONSTITUENTS_PRELIMINARY",
        "survivorship_bias":        True,
        "formal_pass_fail_allowed": False,
        "generated_at":             datetime.now(timezone.utc).isoformat(),
        "base_source":              BASE_URL,
        "base_date":                BASE_DATE,
        "changes_applied_count":    len(CHANGES),
        "count":                    len(snapshot),
        "symbols":                  snapshot,
        "note": (
            "S&P 500 constituents as of 2026-06-11. "
            "Base: GitHub CSV 2026-05-11 + confirmed S&P changes through 2026-06-11. "
            "Post-cutoff changes (MRVL/FLEX/POOL effective 2026-06-22) explicitly excluded. "
            "Survivorship bias present — not for formal E1 PASS/FAIL."
        ),
    })
    logger.info(f"Final snapshot saved: {snap_path} ({len(snapshot)} symbols)")

    # ── 6. Compare with stale 506 list ────────────────────
    stale_path = Path("data/sp500_constituents.json")
    if stale_path.exists():
        stale     = set(json.load(open(stale_path)))
        new_set   = snapshot_set
        removed_from_stale = sorted(stale - new_set)
        added_to_new       = sorted(new_set - stale)
        logger.info(f"vs stale 506: removed={len(removed_from_stale)} added={len(added_to_new)}")

        # Symbols in stale but not in new snapshot → historical candidates
        HIST_CAND.mkdir(parents=True, exist_ok=True)
        archived = []
        for sym in removed_from_stale:
            src = RAW_STOCKS / f"{sym}.json"
            dst = HIST_CAND / f"{sym}.json"
            if src.exists() and not dst.exists():
                import shutil
                shutil.copy2(src, dst)
                archived.append(sym)
        if archived:
            logger.info(f"Archived {len(archived)} stale symbols → historical_candidates/")

    # ── 7. Data coverage check ────────────────────────────
    has_data   = set(f.stem for f in RAW_STOCKS.glob("*.json"))
    covered    = snapshot_set & has_data
    need_fetch = sorted(snapshot_set - has_data)

    logger.info(f"Data coverage: {len(covered)}/{len(snapshot)} ({len(covered)/len(snapshot):.1%})")
    if need_fetch:
        logger.warning(f"Need to fetch {len(need_fetch)}: {need_fetch}")

    # ── 8. Update audit ───────────────────────────────────
    if AUDIT_FILE.exists():
        audit = json.load(open(AUDIT_FILE))
        audit["universe_snapshot"] = {
            "snapshot_date":     SNAPSHOT_DATE,
            "snapshot_file":     str(snap_path),
            "base_date":         BASE_DATE,
            "base_source":       BASE_URL,
            "count":             len(snapshot),
            "data_coverage":     f"{len(covered)}/{len(snapshot)}",
            "need_fetch":        need_fetch,
            "overall_status": (
                "PRELIMINARY_READY_PENDING_FETCH" if need_fetch
                else "PRELIMINARY_READY"
            ),
        }
        audit["overall_status"] = audit["universe_snapshot"]["overall_status"]
        atomic_write(AUDIT_FILE, audit)

    # ── 9. Summary ────────────────────────────────────────
    logger.info("\n" + "=" * 60)
    logger.info(f"S&P 500 snapshot: {SNAPSHOT_DATE} — {len(snapshot)} symbols")
    logger.info(f"Base ({BASE_DATE}): {len(base_tickers)}")
    logger.info(f"  + Added:   {sorted(ADDS)}")
    logger.info(f"  - Removed: {sorted(REMOVES)}")
    logger.info(f"Data coverage: {len(covered)}/{len(snapshot)}")
    if need_fetch:
        logger.info(f"Still need:    {need_fetch}")
        logger.info("Run: python3 scripts/fetch_e1_5y_data.py --force <SYMBOL>")
    logger.info(f"Status: {'PRELIMINARY_READY_PENDING_FETCH' if need_fetch else 'PRELIMINARY_READY'}")

if __name__ == "__main__":
    main()

