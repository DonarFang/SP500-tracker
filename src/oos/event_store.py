"""
Append-only event store backed by data/oos/events.jsonl.
Authority record for all OOS activity. Never edited after write.
"""
import json, os, fcntl, logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

OOS_DIR      = Path(__file__).parent.parent.parent / "data" / "oos"
EVENTS_FILE  = OOS_DIR / "events.jsonl"
RUN_HIST     = OOS_DIR / "run_history.jsonl"

OOS_DIR.mkdir(parents=True, exist_ok=True)

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def make_event_id(date_str: str, event_type: str, symbol: str = "") -> str:
    """Deterministic ID — same run on same day produces same ID."""
    parts = [date_str, event_type]
    if symbol:
        parts.append(symbol)
    return "_".join(parts).upper()

def event_exists(event_id: str) -> bool:
    """Check if event_id already in store (idempotency guard)."""
    if not EVENTS_FILE.exists():
        return False
    with open(EVENTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
                if rec.get("event_id") == event_id:
                    return True
            except json.JSONDecodeError:
                continue
    return False

def append_event(event: dict) -> bool:
    """
    Atomically append one event. Returns False if event_id already exists.
    Uses file lock to prevent concurrent writes.
    """
    event_id = event.get("event_id", "")
    if event_exists(event_id):
        logger.debug(f"Skipping duplicate event: {event_id}")
        return False

    event["_written_at"] = _now_iso()
    line = json.dumps(event, ensure_ascii=False) + "\n"

    with open(EVENTS_FILE, "a", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            f.write(line)
            f.flush()
            os.fsync(f.fileno())
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)

    logger.info(f"Event appended: {event_id}")
    return True

def load_all_events() -> list:
    """Load all events in chronological order."""
    if not EVENTS_FILE.exists():
        return []
    events = []
    with open(EVENTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError as e:
                    logger.error(f"Corrupt event line: {e}")
    return sorted(events, key=lambda e: (e.get("date", ""), e.get("_written_at", "")))

def append_run_record(record: dict) -> None:
    """Log each run attempt to run_history.jsonl."""
    record["_written_at"] = _now_iso()
    with open(RUN_HIST, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def get_last_processed_date() -> Optional[str]:
    """Return the latest signal_date from events, or None."""
    events = load_all_events()
    dates = [e["date"] for e in events if "date" in e]
    return max(dates) if dates else None
