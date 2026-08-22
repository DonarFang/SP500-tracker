#!/usr/bin/env python3
"""GitHub runtime entrypoint for SA-step-3."""

from datetime import date, timedelta
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def yahoo_history(symbol):
    import yfinance as yf
    frame = yf.download(
        symbol, start="2023-01-01", end=(date.today() + timedelta(days=1)).isoformat(),
        interval="1d", auto_adjust=True, actions=False, progress=False, threads=False,
    )
    if frame is None or frame.empty:
        return []
    rows = []
    for index, source in frame.iterrows():
        def scalar(name):
            value = source[name]
            return value.iloc[0] if hasattr(value, "iloc") else value
        rows.append({
            "date": str(index)[:10], "open": scalar("Open"), "high": scalar("High"),
            "low": scalar("Low"), "close": scalar("Close"), "volume": scalar("Volume"),
        })
    return rows


def main():
    from e1r_engine.source_automation.event_publication import VerifiedEventPublisher
    result = VerifiedEventPublisher(ROOT, yahoo_history).publish()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
