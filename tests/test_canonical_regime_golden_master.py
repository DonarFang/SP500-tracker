from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SPX = ROOT / "data/research/e1_5y/raw/indices/SPX.json"
WEEKLY = ROOT / "data/research/e1_5y/regimes/spx_weekly_regimes.json"
DAILY = ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json"

EXPECTED_HASHES = {
    SPX: "04e09605b1bee9a900a0f3db4c1926e6bd48f8f4dceebf711b2c9511bd98633e",
    WEEKLY: "1bdff14664a65f1d966ac078f130e9ac24ee742d044cede57f05ef00050d74c1",
    DAILY: "3ad4f9308b0b6b77476e4a7d204d3fab71882a5cd6234d872aa5299bf356afc8",
}

EXPECTED_COUNTS = {
    ("UNCLASSIFIED", "NO_SUBCLASS"): 253,
    ("UPTREND", "NO_SUBCLASS"): 910,
    ("SIDEWAYS", "MA_CONFLICT"): 135,
    ("SIDEWAYS", "DETERIORATION_TRANSITION"): 63,
    ("DOWNTREND", "NO_SUBCLASS"): 158,
    ("SIDEWAYS", "RECOVERY_TRANSITION"): 43,
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sma(values: list[float], n: int) -> float | None:
    return sum(values[-n:]) / n if len(values) >= n else None


def load_bars() -> list[dict[str, Any]]:
    raw = json.loads(SPX.read_text())
    return sorted(
        (
            {"date": str(row["date"])[:10], "close": float(row["close"])}
            for row in raw["bars"]
        ),
        key=lambda row: row["date"],
    )


def build_weekly(bars: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_week: dict[tuple[int, int], dict[str, Any]] = {}

    for row in bars:
        d = date.fromisoformat(row["date"])
        iso_year, iso_week, _ = d.isocalendar()
        key = int(iso_year), int(iso_week)

        if key not in by_week or row["date"] > by_week[key]["date"]:
            by_week[key] = row

    weekly = [
        {
            "week_end_date": row["date"],
            "iso_year": iso_year,
            "iso_week": iso_week,
            "close": row["close"],
        }
        for (iso_year, iso_week), row in sorted(by_week.items())
    ]

    closes = [row["close"] for row in weekly]
    result: list[dict[str, Any]] = []

    for i, row in enumerate(weekly):
        current = closes[:i + 1]
        ma10 = sma(current, 10)
        ma40 = sma(current, 40)
        slope = None

        if ma40 is not None and i >= 13:
            old_ma40 = sma(closes[:i + 1 - 13], 40)
            if old_ma40 is not None and old_ma40 > 0:
                slope = ma40 / old_ma40 - 1

        close = row["close"]

        if ma10 is None or ma40 is None or slope is None:
            regime, subclass = "UNCLASSIFIED", None
        elif close > ma40 and ma10 > ma40 and slope > 0:
            regime, subclass = "UPTREND", None
        elif close < ma40 and ma10 < ma40 and slope < 0:
            regime, subclass = "DOWNTREND", None
        elif close > ma40 and ma10 > ma40 and slope <= 0:
            regime, subclass = "SIDEWAYS", "RECOVERY_TRANSITION"
        elif close < ma40 and ma10 < ma40 and slope >= 0:
            regime, subclass = "SIDEWAYS", "DETERIORATION_TRANSITION"
        else:
            regime, subclass = "SIDEWAYS", "MA_CONFLICT"

        result.append({
            **row,
            "ma10w": round(ma10, 4) if ma10 is not None else None,
            "ma40w": round(ma40, 4) if ma40 is not None else None,
            "ma40w_slope_13w": round(slope, 6) if slope is not None else None,
            "regime": regime,
            "subclass": subclass,
        })

    return result


def build_daily(
    bars: list[dict[str, Any]],
    weekly: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    week_ends = sorted(
        (
            date.fromisoformat(row["week_end_date"]),
            row["regime"],
            row["subclass"],
        )
        for row in weekly
    )

    output: dict[str, dict[str, Any]] = {}

    for row in bars:
        d = date.fromisoformat(row["date"])
        monday = d - timedelta(days=d.weekday())
        applicable = None

        for week_end, regime, subclass in week_ends:
            if week_end < monday:
                applicable = regime, subclass
            else:
                break

        if applicable is None:
            output[row["date"]] = {
                "regime": "UNCLASSIFIED",
                "subclass": None,
            }
        else:
            output[row["date"]] = {
                "regime": applicable[0],
                "subclass": applicable[1],
            }

    return output


def test_frozen_hashes() -> None:
    for path, expected in EXPECTED_HASHES.items():
        assert path.exists()
        assert sha256(path) == expected


def test_exact_canonical_reproduction() -> None:
    bars = load_bars()
    generated_weekly = build_weekly(bars)
    generated_daily = build_daily(bars, generated_weekly)

    reference_weekly = json.loads(WEEKLY.read_text())["weekly_regimes"]
    reference_daily = json.loads(DAILY.read_text())["daily_regime"]

    assert len(generated_weekly) == len(reference_weekly) == 325
    assert generated_weekly == reference_weekly

    assert len(generated_daily) == len(reference_daily) == 1562
    assert set(generated_daily) == set(reference_daily)
    assert generated_daily == reference_daily

    counts = Counter(
        (row["regime"], row.get("subclass") or "NO_SUBCLASS")
        for row in generated_daily.values()
    )
    assert dict(counts) == EXPECTED_COUNTS
