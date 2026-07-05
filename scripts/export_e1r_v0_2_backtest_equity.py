from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def first_present(d: dict[str, Any], keys: list[str], default=None):
    for k in keys:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return default


def normalize_curve(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []

    for r in records:
        if not isinstance(r, dict):
            continue

        date = first_present(r, ["date", "as_of", "data_date"])
        equity = first_present(r, ["equity", "total_equity", "portfolio_value", "value"])
        spx_equity = first_present(r, ["spx_equity", "spx_value", "benchmark_equity"])
        daily_return = first_present(r, ["daily_return", "return", "ret"])
        core_return = first_present(r, ["core_return", "core_daily_return"])
        sidecar_return = first_present(r, ["sidecar_return", "sidecar_daily_return"])
        combined_return = first_present(r, ["combined_return", "combined_daily_return"])

        if date is None or equity is None:
            continue

        row = {
            "date": date,
            "equity": equity,
        }

        if spx_equity is not None:
            row["spx_equity"] = spx_equity
        if daily_return is not None:
            row["daily_return"] = daily_return
        if core_return is not None:
            row["core_return"] = core_return
        if sidecar_return is not None:
            row["sidecar_return"] = sidecar_return
        if combined_return is not None:
            row["combined_return"] = combined_return

        out.append(row)

    return sorted(out, key=lambda x: x["date"])


def extract_variant(variants: dict[str, Any], strategy_id: str) -> dict[str, Any]:
    if strategy_id not in variants:
        available = sorted(variants.keys())
        raise RuntimeError(
            f"Missing variant: {strategy_id}. "
            f"Available variants: {available}. "
            "Run full 5Y backtest with E1R v0.2 engine first."
        )
    return variants[strategy_id]


def main() -> None:
    bt_path = ROOT / "exports/backtest.json"
    if not bt_path.exists():
        raise RuntimeError("Missing exports/backtest.json")

    bt = read_json(bt_path)
    layer_d = bt.get("backtest", {}).get("results", {}).get("layer_d", {})
    variants = layer_d.get("variant_results", {})

    comparison_name = layer_d.get("name")

    v1 = extract_variant(variants, "E1R_REGIME_AWARE_V0_1")
    v2 = extract_variant(variants, "E1R_REGIME_AWARE_V0_2")

    v1_records = v1.get("daily_equity_records") or v1.get("equity_curve") or []
    v2_records = v2.get("daily_equity_records") or v2.get("equity_curve") or []

    v1_curve = normalize_curve(v1_records)
    v2_curve = normalize_curve(v2_records)

    if len(v1_curve) < 1000:
        raise RuntimeError(f"E1R v0.1 curve too short: {len(v1_curve)} rows. Expected 5Y-like curve.")

    if len(v2_curve) < 1000:
        raise RuntimeError(f"E1R v0.2 curve too short: {len(v2_curve)} rows. Expected 5Y-like curve.")

    start_date = v2_curve[0]["date"]
    end_date = v2_curve[-1]["date"]

    if start_date > "2021-06-15":
        raise RuntimeError(f"Start date looks too recent for 5Y export: {start_date}")

    if end_date < "2026-06-15":
        raise RuntimeError(f"End date looks too old for current 5Y export: {end_date}")

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "exports/backtest.json",
        "comparison_name": comparison_name,
        "strategy_id": "E1R_REGIME_AWARE_V0_2",
        "version": v2.get("version"),
        "research_status": v2.get("research_status"),
        "curve_type": "FULL_5Y_BACKTEST_EQUITY",
        "start_date": start_date,
        "end_date": end_date,
        "row_count": len(v2_curve),
        "v0_1": {
            "strategy_id": "E1R_REGIME_AWARE_V0_1",
            "total_return_pct": v1.get("total_return_pct"),
            "spx_return_pct": v1.get("spx_return_pct"),
            "alpha_pct": v1.get("alpha_pct"),
            "max_drawdown_pct": v1.get("max_drawdown_pct"),
            "profit_factor": v1.get("profit_factor"),
            "sharpe_ratio": v1.get("sharpe_ratio"),
            "research_status": v1.get("research_status"),
            "regime_aware_logic": (v1.get("strategy_controls") or {}).get("regime_aware_logic"),
            "row_count": len(v1_curve),
        },
        "v0_2": {
            "strategy_id": "E1R_REGIME_AWARE_V0_2",
            "total_return_pct": v2.get("total_return_pct"),
            "spx_return_pct": v2.get("spx_return_pct"),
            "alpha_pct": v2.get("alpha_pct"),
            "max_drawdown_pct": v2.get("max_drawdown_pct"),
            "profit_factor": v2.get("profit_factor"),
            "sharpe_ratio": v2.get("sharpe_ratio"),
            "research_status": v2.get("research_status"),
            "regime_aware_logic": (v2.get("strategy_controls") or {}).get("regime_aware_logic"),
            "sidecar_active_days": v2.get("sidecar_active_days"),
            "sidecar_active_by_regime": v2.get("sidecar_active_by_regime"),
            "sidecar_active_by_subclass": v2.get("sidecar_active_by_subclass"),
            "composition_exists": bool(v2.get("e1r_v0_2_composition")),
            "row_count": len(v2_curve),
        },
        "notes": [
            "This is the full 5Y E1R v0.2 backtest equity export for Dashboard display.",
            "It is not the live OOS / forward equity curve.",
            "OOS / forward equity will be exported separately in OOS-2B.",
            "Large legacy backtest exports should not be committed with this lightweight export.",
        ],
    }

    equity_export = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "curve_type": "FULL_5Y_BACKTEST_EQUITY",
        "start_date": start_date,
        "end_date": end_date,
        "row_count": len(v2_curve),
        "series": {
            "E1R_REGIME_AWARE_V0_1": v1_curve,
            "E1R_REGIME_AWARE_V0_2": v2_curve,
        },
        "summary": summary,
    }

    write_json(ROOT / "exports/e1r_v0_2_backtest_summary.json", summary)
    write_json(ROOT / "exports/e1r_v0_2_backtest_equity_curve.json", equity_export)

    print("Wrote exports/e1r_v0_2_backtest_summary.json")
    print("Wrote exports/e1r_v0_2_backtest_equity_curve.json")
    print("comparison_name:", comparison_name)
    print("curve_type:", equity_export["curve_type"])
    print("start_date:", start_date)
    print("end_date:", end_date)
    print("row_count:", len(v2_curve))
    print("v0_1 return:", summary["v0_1"]["total_return_pct"])
    print("v0_2 return:", summary["v0_2"]["total_return_pct"])
    print("v0_2 maxDD:", summary["v0_2"]["max_drawdown_pct"])
    print("sidecar_active_days:", summary["v0_2"]["sidecar_active_days"])


if __name__ == "__main__":
    main()
