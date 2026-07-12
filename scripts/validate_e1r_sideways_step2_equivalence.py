#!/usr/bin/env python3
"""Validate standalone SIDEWAYS decision equivalence against frozen golden data."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

from e1r_engine.sideways_core import (
    SidewaysConfig,
    SidewaysCore,
    build_intervals,
)
from engine.e1r_sidecar_sleeve import (
    load_asset,
    load_regimes,
    load_stock_universe,
)


def _walk_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from _walk_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_strings(child)


def _resolve_sources(
    artifact: dict[str, Any],
    repo: Path,
) -> tuple[Path, Path, Path]:
    strings = list(_walk_strings(artifact.get("source", {})))
    strings += list(_walk_strings(artifact.get("input_summary", {})))

    existing = []
    for raw in strings:
        path = Path(raw).expanduser()
        if not path.is_absolute():
            path = repo / path
        if path.exists():
            existing.append(path.resolve())

    stock_dirs = [
        path for path in existing
        if path.is_dir() and len(list(path.glob("*.json"))) >= 100
    ]
    json_files = [path for path in existing if path.is_file()]

    spx_files = [
        path for path in json_files
        if "spx" in path.name.lower()
    ]
    regime_files = [
        path for path in json_files
        if "regime" in path.name.lower()
        or "market_state" in path.name.lower()
    ]

    if not stock_dirs:
        for path in repo.rglob("*"):
            if (
                path.is_dir()
                and "stock" in path.name.lower()
                and len(list(path.glob("*.json"))) >= 100
            ):
                stock_dirs.append(path.resolve())

    if not spx_files:
        spx_files = [
            path.resolve()
            for path in repo.rglob("*.json")
            if "spx" in path.name.lower()
            and path.stat().st_size > 10000
        ]

    if not regime_files:
        regime_files = [
            path.resolve()
            for path in repo.rglob("*.json")
            if (
                "regime" in path.name.lower()
                or "market_state" in path.name.lower()
            )
            and path.stat().st_size > 10000
        ]

    if not stock_dirs or not spx_files or not regime_files:
        raise RuntimeError(
            "Unable to resolve stock_dir/SPX/regime inputs from artifact "
            "metadata or repository paths."
        )

    return stock_dirs[0], spx_files[0], regime_files[0]


def _close(a: float, b: float, tol: float = 1e-12) -> bool:
    return abs(float(a) - float(b)) <= tol


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--artifact",
        default="exports/e1r_v0_2_sidecar_records_5y.json",
    )
    parser.add_argument(
        "--out",
        default="/tmp/e1r_sideways_step2_equivalence.json",
    )
    args = parser.parse_args()

    repo = Path.cwd()
    artifact_path = Path(args.artifact)
    raw = json.loads(artifact_path.read_text(encoding="utf-8"))
    golden = raw["records"]

    stock_dir, spx_path, regime_path = _resolve_sources(raw, repo)

    raw_config = raw.get("config")
    window = raw.get("window", {})
    summary = raw.get("sidecar_summary", {})
    input_summary = raw.get("input_summary", {})

    if not isinstance(window, dict):
        raise RuntimeError("golden artifact window must be a dict")
    if not isinstance(summary, dict):
        raise RuntimeError("golden artifact sidecar_summary must be a dict")
    if not isinstance(input_summary, dict):
        raise RuntimeError("golden artifact input_summary must be a dict")
    if not isinstance(raw_config, str):
        raise RuntimeError(
            "golden artifact config must be the frozen dataclass repr string"
        )

    start_date = window.get("start_date") or golden[0]["date"]
    end_date = window.get("end_date") or golden[-1]["next_date"]

    # The artifact stores ``config`` as a repr string.  Parse only the frozen
    # primitive fields needed for validation; do not eval the string.
    config_patterns = {
        "min_history_days": r"min_history_days=(\d+)",
        "min_price": r"min_price=([0-9.]+)",
        "initial_equity": r"initial_equity=([0-9.]+)",
    }
    parsed_config = {}
    for field, pattern in config_patterns.items():
        match = re.search(pattern, raw_config)
        if match is None:
            raise RuntimeError(
                f"missing {field} in frozen config repr: {raw_config}"
            )
        parsed_config[field] = match.group(1)

    legacy_cfg = type(
        "LegacyConfig",
        (),
        {
            "start_date": start_date,
            "end_date": end_date,
            "allowed_subclasses": tuple(
                summary.get("allowed_subclasses", ["MA_CONFLICT"])
            ),
            "top_n": int(summary.get("top_n", 10)),
            "gross_exposure": float(
                summary.get("gross_exposure", 0.25)
            ),
            "min_history_days": int(
                parsed_config["min_history_days"]
            ),
            "min_price": float(parsed_config["min_price"]),
            "initial_equity": float(
                parsed_config["initial_equity"]
            ),
            "excluded_symbols": tuple(
                summary.get("excluded_symbols")
                or input_summary.get("excluded_sample")
                or ["VIXY"]
            ),
        },
    )()

    spx = load_asset(spx_path)
    regimes = load_regimes(regime_path)
    stocks, _ = load_stock_universe(stock_dir, legacy_cfg)
    intervals = build_intervals(
        spx,
        regimes,
        start_date,
        end_date,
    )

    core = SidewaysCore(
        SidewaysConfig(
            allowed_subclasses=legacy_cfg.allowed_subclasses,
            top_n=legacy_cfg.top_n,
            gross_exposure=legacy_cfg.gross_exposure,
            min_history_days=legacy_cfg.min_history_days,
            min_price=legacy_cfg.min_price,
            excluded_symbols=legacy_cfg.excluded_symbols,
        )
    )
    plans = core.decide_many(
        stocks=stocks,
        spx=spx,
        regimes=regimes,
        intervals=intervals,
    )

    mismatches = []
    if len(plans) != len(golden):
        mismatches.append({
            "field": "record_count",
            "expected": len(golden),
            "actual": len(plans),
        })

    for index, (plan, expected) in enumerate(zip(plans, golden)):
        expected_active = bool(expected["sidecar_active"])
        scalar_pairs = {
            "date": (plan.date, expected["date"]),
            "next_date": (plan.next_date, expected["next_date"]),
            "regime": (plan.regime, expected["regime"]),
            "subclass": (plan.subclass, expected["subclass"]),
            "is_active": (plan.is_active, expected_active),
            "candidate_count": (
                plan.candidate_count,
                expected["candidate_count"],
            ),
            "selected_count": (
                plan.selected_count,
                expected["sidecar_selected_count"],
            ),
        }
        for field, (actual, target) in scalar_pairs.items():
            if actual != target:
                mismatches.append({
                    "index": index,
                    "date": expected["date"],
                    "field": field,
                    "expected": target,
                    "actual": actual,
                })

        float_pairs = {
            "gross_exposure": (
                plan.gross_exposure,
                expected["sidecar_gross_exposure"],
            ),
            "portfolio_return": (
                plan.portfolio_return,
                expected["sidecar_return"],
            ),
            "spx_return": (
                plan.spx_return,
                expected["spx_return"],
            ),
        }
        for field, (actual, target) in float_pairs.items():
            if not _close(actual, target):
                mismatches.append({
                    "index": index,
                    "date": expected["date"],
                    "field": field,
                    "expected": target,
                    "actual": actual,
                })

        expected_holdings = expected["sidecar_holdings"]
        if len(plan.holdings) != len(expected_holdings):
            mismatches.append({
                "index": index,
                "date": expected["date"],
                "field": "holdings_length",
                "expected": len(expected_holdings),
                "actual": len(plan.holdings),
            })
        for h_index, (actual, target) in enumerate(
            zip(plan.holdings, expected_holdings)
        ):
            if actual.symbol != target["symbol"]:
                mismatches.append({
                    "index": index,
                    "holding_index": h_index,
                    "date": expected["date"],
                    "field": "symbol",
                    "expected": target["symbol"],
                    "actual": actual.symbol,
                })
            for field, actual_value, expected_value in (
                ("score", actual.score, target["score"]),
                ("weight", actual.weight, target["weight"]),
                ("raw_return", actual.raw_return, target["raw_return"]),
                (
                    "weighted_contribution",
                    actual.weighted_contribution,
                    target["weighted_contribution"],
                ),
            ):
                if not _close(actual_value, expected_value):
                    mismatches.append({
                        "index": index,
                        "holding_index": h_index,
                        "date": expected["date"],
                        "field": field,
                        "expected": expected_value,
                        "actual": actual_value,
                    })

        if len(mismatches) >= 100:
            break

    active_count = sum(plan.is_active for plan in plans)
    canonical = [
        {
            "date": plan.date,
            "next_date": plan.next_date,
            "regime": plan.regime,
            "subclass": plan.subclass,
            "is_active": plan.is_active,
            "candidate_count": plan.candidate_count,
            "selected_count": plan.selected_count,
            "gross_exposure": plan.gross_exposure,
            "portfolio_return": plan.portfolio_return,
            "spx_return": plan.spx_return,
            "holdings": [
                {
                    "symbol": holding.symbol,
                    "score": holding.score,
                    "weight": holding.weight,
                    "raw_return": holding.raw_return,
                    "weighted_contribution": (
                        holding.weighted_contribution
                    ),
                }
                for holding in plan.holdings
            ],
        }
        for plan in plans
    ]
    encoded = json.dumps(
        canonical,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    report = {
        "decision": (
            "PASS_SIDEWAYS_STEP2_DECISION_EQUIVALENCE"
            if not mismatches
            and len(plans) == 1260
            and active_count == 135
            else "FAIL_SIDEWAYS_STEP2_DECISION_EQUIVALENCE"
        ),
        "inputs": {
            "stock_dir": str(stock_dir),
            "spx_path": str(spx_path),
            "regime_path": str(regime_path),
        },
        "record_count": len(plans),
        "active_count": active_count,
        "mismatch_count": len(mismatches),
        "first_mismatches": mismatches[:20],
        "canonical_result_sha256": hashlib.sha256(encoded).hexdigest(),
    }

    Path(args.out).write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["decision"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
