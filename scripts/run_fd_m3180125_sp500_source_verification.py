#!/usr/bin/env python3
"""Run SA-step-2 read-only Yahoo verification in GitHub Actions."""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from e1r_engine.source_automation.verification import SourceVerifier


def yahoo_probe(symbol):
    import yfinance as yf

    frame = yf.Ticker(symbol).history(period="1mo", interval="1d", auto_adjust=True)
    if frame is None or frame.empty or "Close" not in frame.columns:
        return []
    rows = []
    for index, value in frame["Close"].dropna().items():
        rows.append({"date": str(index)[:10], "close": float(value)})
    return rows


def main():
    result = SourceVerifier(ROOT, yahoo_probe).run_all()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS_SA2_VERIFICATION" else 2


if __name__ == "__main__":
    raise SystemExit(main())
