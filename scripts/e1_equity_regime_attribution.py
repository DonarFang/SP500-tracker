#!/usr/bin/env python3
import json
import math
from pathlib import Path
from collections import defaultdict

BACKTEST = Path("exports/backtest.json")
REGIME_DAILY = Path("data/research/e1_5y/regimes/spx_regime_daily.json")
OUT_JSON = Path("data/research/e1_5y/regimes/e1_equity_regime_attribution.json")
OUT_MD = Path("data/research/e1_5y/regimes/E1_EQUITY_REGIME_ATTRIBUTION_REPORT.md")

STRATEGY_ID = "E1_AUDITED_G4_MINHOLD10"
INIT_CAPITAL = 100_000.0


def load_json(p):
    with open(p) as f:
        return json.load(f)


def normalize_regime_daily(obj):
    if isinstance(obj, dict):
        if "daily_regime" in obj:
            obj = obj["daily_regime"]
        elif "daily_regimes" in obj:
            obj = obj["daily_regimes"]
        elif "records" in obj:
            obj = obj["records"]
        elif "data" in obj:
            obj = obj["data"]

    out = {}
    if isinstance(obj, list):
        for r in obj:
            d = r.get("date")
            regime = (
                r.get("regime")
                or r.get("spx_regime")
                or r.get("weekly_regime")
                or r.get("state")
                or "UNCLASSIFIED"
            )
            if d:
                out[d] = {**r, "regime": regime}
    elif isinstance(obj, dict):
        for d, v in obj.items():
            if isinstance(v, dict):
                regime = (
                    v.get("regime")
                    or v.get("spx_regime")
                    or v.get("weekly_regime")
                    or v.get("state")
                    or "UNCLASSIFIED"
                )
                out[d] = {**v, "regime": regime}
            else:
                out[d] = {"date": d, "regime": str(v)}
    return out


def sample_status(n):
    if n >= 126:
        return "SAMPLE_OK"
    if n >= 20:
        return "SMALL_SAMPLE_OBSERVATIONAL"
    if n > 0:
        return "INSUFFICIENT_SAMPLE_OBSERVATIONAL"
    return "NO_SAMPLE"


def main():
    bj = load_json(BACKTEST)
    regimes = normalize_regime_daily(load_json(REGIME_DAILY))

    e1 = bj["backtest"]["results"]["layer_d"]["variant_results"][STRATEGY_ID]
    records = e1.get("daily_equity_records", [])
    sim_end = e1.get("sim_end_liquidation_record")

    if not records:
        raise SystemExit("daily_equity_records missing. Run python3 run_backtest.py first.")

    rows = []
    prev_equity = INIT_CAPITAL

    for r in records:
        date = r["date"]
        total = float(r["total_equity"])
        pnl = total - prev_equity
        reg = regimes.get(date, {"regime": "UNCLASSIFIED"})
        regime = reg.get("regime", "UNCLASSIFIED")

        rows.append({
            "date": date,
            "regime": regime,
            "daily_return_pct": float(r.get("daily_return_pct", 0.0)),
            "pnl": pnl,
            "total_equity": total,
            "exposure_pct": float(r.get("exposure_pct", 0.0)),
            "open_positions_count": int(r.get("open_positions_count", 0)),
            "event": r.get("event", "EOD_MARK_TO_MARKET"),
        })
        prev_equity = total

    if sim_end:
        last_date = sim_end["date"]
        final_equity = float(sim_end["total_equity"])
        pnl = final_equity - prev_equity
        reg = regimes.get(last_date, {"regime": "UNCLASSIFIED"})
        rows.append({
            "date": last_date,
            "regime": reg.get("regime", "UNCLASSIFIED"),
            "daily_return_pct": (final_equity / prev_equity - 1) * 100 if prev_equity > 0 else 0.0,
            "pnl": pnl,
            "total_equity": final_equity,
            "exposure_pct": 0.0,
            "open_positions_count": 0,
            "event": "SIM_END_LIQUIDATION",
        })

    by_regime = defaultdict(list)
    for r in rows:
        by_regime[r["regime"]].append(r)

    summary = {}
    for regime, rs in sorted(by_regime.items()):
        returns = [x["daily_return_pct"] / 100 for x in rs]
        compound = math.prod([1 + r for r in returns]) - 1
        pnl_sum = sum(x["pnl"] for x in rs)
        avg_ret = sum(returns) / len(returns) if returns else 0.0
        vol = math.sqrt(sum((r - avg_ret) ** 2 for r in returns) / len(returns)) if len(returns) > 1 else 0.0
        ann_vol = vol * math.sqrt(252)
        ann_ret = avg_ret * 252
        sharpe = ann_ret / ann_vol if ann_vol > 0 else 0.0

        summary[regime] = {
            "regime": regime,
            "days": len(rs),
            "sample_status": sample_status(len(rs)),
            "compound_return_pct": round(compound * 100, 2),
            "pnl_contribution_usd": round(pnl_sum, 2),
            "pnl_contribution_pct_of_initial": round(pnl_sum / INIT_CAPITAL * 100, 2),
            "avg_daily_return_pct": round(avg_ret * 100, 4),
            "annualized_vol_pct": round(ann_vol * 100, 2),
            "sharpe_like": round(sharpe, 2),
            "avg_exposure_pct": round(sum(x["exposure_pct"] for x in rs) / len(rs), 2),
            "avg_open_positions": round(sum(x["open_positions_count"] for x in rs) / len(rs), 2),
            "start_date": rs[0]["date"],
            "end_date": rs[-1]["date"],
        }

    total_pnl = sum(x["pnl"] for x in rows)
    result = {
        "strategy_id": STRATEGY_ID,
        "status": "PRELIMINARY_CURRENT_CONSTITUENTS_NOT_PIT",
        "input": {
            "backtest": str(BACKTEST),
            "regime_daily": str(REGIME_DAILY),
        },
        "record_count": len(rows),
        "daily_equity_record_count": len(records),
        "sim_end_liquidation_included": bool(sim_end),
        "total_pnl_usd": round(total_pnl, 2),
        "total_return_pct_of_initial": round(total_pnl / INIT_CAPITAL * 100, 2),
        "by_regime": summary,
    }

    OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False))

    lines = []
    lines.append("# E1 Equity-Level Regime Attribution")
    lines.append("")
    lines.append(f"Strategy: `{STRATEGY_ID}`")
    lines.append(f"Status: `{result['status']}`")
    lines.append(f"Records: {result['record_count']} including SIM_END liquidation: {bool(sim_end)}")
    lines.append(f"Total return attribution: {result['total_return_pct_of_initial']:.2f}%")
    lines.append("")
    lines.append("| Regime | Days | Sample | PnL % Initial | Compound Return | Avg Exposure | Sharpe-like |")
    lines.append("|---|---:|---|---:|---:|---:|---:|")
    for regime, s in summary.items():
        lines.append(
            f"| {regime} | {s['days']} | {s['sample_status']} | "
            f"{s['pnl_contribution_pct_of_initial']:.2f}% | "
            f"{s['compound_return_pct']:.2f}% | "
            f"{s['avg_exposure_pct']:.2f}% | "
            f"{s['sharpe_like']:.2f} |"
        )
    lines.append("")
    lines.append("Interpretation note: regime attribution is equity-level, not trade-entry-level. SIM_END liquidation is included so attribution reconciles to E1 final return.")
    OUT_MD.write_text("\n".join(lines))

    print("=" * 72)
    print("E1 EQUITY REGIME ATTRIBUTION")
    print("=" * 72)
    print(f"Status: {result['status']}")
    print(f"Records: {result['record_count']}")
    print(f"Total attribution return: {result['total_return_pct_of_initial']:.2f}%")
    print("")
    for regime, s in summary.items():
        print(
            f"{regime:12s} days={s['days']:4d} "
            f"pnl%={s['pnl_contribution_pct_of_initial']:7.2f} "
            f"compound%={s['compound_return_pct']:7.2f} "
            f"exposure%={s['avg_exposure_pct']:6.2f} "
            f"sample={s['sample_status']}"
        )
    print("")
    print(f"Output JSON: {OUT_JSON}")
    print(f"Output MD:   {OUT_MD}")


if __name__ == "__main__":
    main()
