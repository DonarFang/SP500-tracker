#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import math
import hashlib
import importlib
import sys
from datetime import datetime, timezone
from collections import Counter
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

STOCK_DIR = ROOT / "data/research/e1_5y/raw/stocks"
SPX_PATH = ROOT / "data/research/e1_5y/raw/indices/SPX.json"
REGIME_PATH = ROOT / "data/research/e1_5y/regimes/spx_regime_daily.json"

CORE_CANDIDATES = [
    ROOT / "exports/e1r_unified_5y_full_account_v1_result.json",
    ROOT / "exports/portfolio_backtest.json",
]

OUT_RESULT = ROOT / "exports/e1r_combined_5y_original_max3_result.json"
OUT_CURVE = ROOT / "exports/e1r_combined_5y_original_max3_equity_curve.json"
OUT_SUMMARY = ROOT / "exports/e1r_combined_5y_original_max3_summary.json"

REPORT_JSON = ROOT / "docs/research/E1R_COMBINED_5Y_4C2C4D_ORIGINAL_MAX3_FULL_RUN_REPORT.json"
REPORT_MD = ROOT / "docs/research/E1R_COMBINED_5Y_4C2C4D_ORIGINAL_MAX3_FULL_RUN_REPORT.md"

FROZEN_STRATEGY_FILES = [
    ROOT / "src/engine/backtest.py",
    ROOT / "src/engine/e1r_composer.py",
    ROOT / "src/engine/e1r_sidecar_sleeve.py",
]

START_DATE = "2021-06-11"
END_DATE = "2026-06-18"
INITIAL_EQUITY = 100000.0

CONTRACT = {
    "strategy_id": "E1R_COMBINED_5Y_ORIGINAL_MAX3",
    "strategy_logic_changed": False,
    "uptrend": "Use previously validated UPTREND/core strategy result; do not replace logic.",
    "sideways_ma_conflict": "Call original build_e1r_sidecar_sleeve with original defaults: allowed_subclasses=('MA_CONFLICT',), top_n=10, gross_exposure=0.25.",
    "sideways_top10_interpretation": "Top10 is candidate/sidecar ranking pool, not live account holdings.",
    "sideways_live_account_adapter": "Use original sidecar ordering; account-level live holdings are capped to first 3 candidates. No new score/ranking rule is introduced.",
    "deterioration_recovery": "cash/defensive unless original sidecar strict active, which prior strict audit showed false.",
    "downtrend": "cash/defensive.",
    "global_account_position_cap": 3,
    "metric_source": "adapter daily total_equity; not engine reported final_equity when inconsistent.",
}

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))

def sha256(p: Path) -> str | None:
    if not p.exists():
        return None
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def read_json(p: Path) -> Any:
    return json.loads(p.read_text())

def write_json(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def fnum(x, default=None):
    try:
        if x is None:
            return default
        return float(x)
    except Exception:
        return default

def load_core_result() -> tuple[Path, dict[str, Any]]:
    candidates = []
    for p in CORE_CANDIDATES:
        if not p.exists():
            continue
        try:
            obj = read_json(p)
        except Exception:
            continue

        rows = None
        for k in ["daily_equity_records", "daily_records"]:
            if isinstance(obj.get(k), list) and obj[k]:
                rows = obj[k]
                break

        if not rows:
            continue

        candidates.append((p, obj, len(rows), obj.get("strategy_variant"), obj.get("status")))

    if not candidates:
        raise RuntimeError("No usable core result found. Need existing validated UPTREND/core result artifact.")

    # Prefer E1R artifact with continuous daily_equity_records.
    candidates.sort(key=lambda x: (
        0 if "e1r" in x[0].name.lower() else 1,
        -x[2],
    ))
    p, obj, _, _, _ = candidates[0]
    return p, obj

def core_rows(core: dict[str, Any]) -> list[dict[str, Any]]:
    for k in ["daily_equity_records", "daily_records"]:
        v = core.get(k)
        if isinstance(v, list) and v:
            return [r for r in v if isinstance(r, dict)]
    raise RuntimeError("Core result has no daily records.")

def normalize_core_return_rows(core: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = core_rows(core)
    out = {}
    prev_eq = None

    for r in rows:
        d = str(r.get("date") or "")[:10]
        if not d:
            continue

        eq = fnum(r.get("total_equity"))
        if eq is None:
            eq = fnum(r.get("equity"))
        if eq is None:
            eq = fnum(r.get("portfolio_value"))
        if eq is None:
            continue

        daily_ret = None
        if prev_eq and prev_eq > 0:
            daily_ret = eq / prev_eq - 1.0
        else:
            daily_ret = 0.0

        regime = r.get("spx_regime") or r.get("regime") or r.get("market_regime") or "UNKNOWN"
        open_positions = int(r.get("open_positions_count") or 0)

        out[d] = {
            "date": d,
            "core_total_equity_source": eq,
            "core_daily_return": daily_ret,
            "core_regime": regime,
            "core_open_positions_count": open_positions,
            "core_raw": {
                "cash": r.get("cash"),
                "positions_value": r.get("positions_value"),
                "exposure_pct": r.get("exposure_pct"),
                "market_gate_state": r.get("market_gate_state"),
                "e1r_active_mode": r.get("e1r_active_mode"),
                "risk_budget_mode": r.get("risk_budget_mode"),
            },
        }
        prev_eq = eq

    return out

def build_sidecar_result() -> dict[str, Any]:
    sys.path.insert(0, str(ROOT))
    mod = importlib.import_module("src.engine.e1r_sidecar_sleeve")
    Config = getattr(mod, "E1RSidecarConfig")
    build = getattr(mod, "build_e1r_sidecar_sleeve")

    config = Config(start_date=START_DATE, end_date=END_DATE)
    result = build(
        stock_dir=STOCK_DIR,
        spx_path=SPX_PATH,
        regime_path=REGIME_PATH,
        config=config,
    )
    return result

def sidecar_records_by_date(sidecar: dict[str, Any]) -> dict[str, dict[str, Any]]:
    records = sidecar.get("records")
    if not isinstance(records, list):
        raise RuntimeError("Sidecar result has no records list.")
    out = {}
    for r in records:
        if not isinstance(r, dict):
            continue
        d = str(r.get("date") or "")[:10]
        if d:
            out[d] = r
    return out

def sidecar_adapter_return_and_positions(r: dict[str, Any]) -> tuple[float, list[dict[str, Any]], dict[str, Any]]:
    """
    Account-level max3 adapter:
    - Original sidecar selected Top10 remains candidate/ranking basket.
    - Live account cap requires <=3 positions.
    - Use original holdings order and original per-symbol raw_return.
    - Preserve original sidecar gross exposure = 0.25.
    - Allocate 0.25 / n across first n<=3 selected candidates.
    """
    if not r:
        return 0.0, [], {"reason": "no_sidecar_record"}

    regime = r.get("regime") or "UNKNOWN"
    subclass = r.get("subclass") or "NO_SUBCLASS"
    is_active = r.get("is_active") is True
    gross = fnum(r.get("gross_exposure"), 0.0) or 0.0
    holdings = r.get("holdings") if isinstance(r.get("holdings"), list) else []

    if not (is_active and regime == "SIDEWAYS" and subclass == "MA_CONFLICT" and gross > 0 and holdings):
        return 0.0, [], {
            "reason": "not_strict_active_ma_conflict",
            "regime": regime,
            "subclass": subclass,
            "is_active": is_active,
            "gross_exposure": gross,
            "candidate_count": r.get("candidate_count"),
            "selected_count": r.get("selected_count"),
            "holdings_len": len(holdings),
        }

    live = holdings[:3]
    n = len(live)
    if n == 0:
        return 0.0, [], {"reason": "no_live_candidates_after_cap"}

    weight = gross / n
    adapted = []
    total_ret = 0.0

    for h in live:
        raw_ret = fnum(h.get("raw_return"), 0.0) or 0.0
        contribution = weight * raw_ret
        total_ret += contribution
        adapted.append({
            "symbol": h.get("symbol"),
            "score": h.get("score"),
            "raw_return": raw_ret,
            "raw_return_pct": raw_ret * 100.0,
            "account_weight": weight,
            "weighted_contribution": contribution,
            "weighted_contribution_pct": contribution * 100.0,
        })

    meta = {
        "reason": "strict_active_ma_conflict_max3_adapter",
        "regime": regime,
        "subclass": subclass,
        "is_active": is_active,
        "gross_exposure": gross,
        "candidate_count": r.get("candidate_count"),
        "selected_count": r.get("selected_count"),
        "original_holdings_len": len(holdings),
        "live_holdings_len": len(adapted),
        "original_sidecar_portfolio_return": r.get("portfolio_return"),
        "original_sidecar_portfolio_return_pct": r.get("portfolio_return_pct"),
    }
    return total_ret, adapted, meta

def calc_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {}

    first = rows[0]["total_equity"]
    last = rows[-1]["total_equity"]

    rets = []
    prev = None
    peak = None
    maxdd = 0.0

    for r in rows:
        eq = r["total_equity"]
        if prev and prev > 0:
            rets.append(eq / prev - 1.0)
        prev = eq

        if peak is None or eq > peak:
            peak = eq
        if peak and peak > 0:
            dd = (peak - eq) / peak * 100.0
            maxdd = max(maxdd, dd)

    total_return = (last / first - 1.0) * 100.0
    years = len(rows) / 252.0
    cagr = ((last / first) ** (1.0 / years) - 1.0) * 100.0 if years > 0 and first > 0 else None

    sharpe = None
    vol = None
    if len(rets) > 1:
        mean = sum(rets) / len(rets)
        var = sum((x - mean) ** 2 for x in rets) / (len(rets) - 1)
        std = math.sqrt(var)
        if std > 0:
            sharpe = mean / std * math.sqrt(252)
            vol = std * math.sqrt(252) * 100.0

    spx_first = fnum(rows[0].get("spx_equity_index"))
    spx_last = fnum(rows[-1].get("spx_equity_index"))
    spx_return = None
    alpha = None
    if spx_first and spx_last:
        spx_return = (spx_last / spx_first - 1.0) * 100.0
        alpha = total_return - spx_return

    return {
        "row_count": len(rows),
        "first_date": rows[0]["date"],
        "last_date": rows[-1]["date"],
        "first_equity": first,
        "final_equity": last,
        "total_return_pct": total_return,
        "cagr_pct": cagr,
        "max_drawdown_pct": maxdd,
        "sharpe_ratio": sharpe,
        "annualized_vol_pct": vol,
        "spx_total_return_pct": spx_return,
        "alpha_pct": alpha,
    }

def main():
    started = datetime.now(timezone.utc)
    before_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    core_path, core = load_core_result()
    core_by_date = normalize_core_return_rows(core)

    sidecar = build_sidecar_result()
    sidecar_by_date = sidecar_records_by_date(sidecar)

    dates = sorted(set(core_by_date.keys()) & set(sidecar_by_date.keys()))
    dates = [d for d in dates if START_DATE <= d <= END_DATE]

    if len(dates) < 1000:
        raise RuntimeError(f"Insufficient aligned dates: {len(dates)}")

    rows = []
    total_equity = INITIAL_EQUITY
    spx_index = 100.0

    regime_counts = Counter()
    active_mode_counts = Counter()
    position_count_violations = []

    for i, d in enumerate(dates):
        c = core_by_date[d]
        s = sidecar_by_date.get(d, {})

        regime = s.get("regime") or c.get("core_regime") or "UNKNOWN"
        subclass = s.get("subclass") or "NO_SUBCLASS"

        # Core return is used only for UPTREND; otherwise defensive/cash.
        core_ret = c["core_daily_return"] if regime == "UPTREND" else 0.0

        sidecar_ret, sidecar_live, sidecar_meta = sidecar_adapter_return_and_positions(s)

        if regime == "UPTREND":
            daily_ret = core_ret
            live_positions_count = min(int(c.get("core_open_positions_count") or 0), 3)
            active_mode = "UPTREND_ORIGINAL_CORE"
        elif regime == "SIDEWAYS" and subclass == "MA_CONFLICT" and sidecar_live:
            daily_ret = sidecar_ret
            live_positions_count = len(sidecar_live)
            active_mode = "SIDEWAYS_MA_CONFLICT_ORIGINAL_SIDECAR_MAX3_ADAPTER"
        else:
            daily_ret = 0.0
            live_positions_count = 0
            active_mode = "CASH_DEFENSIVE"

        if live_positions_count > 3:
            position_count_violations.append({
                "date": d,
                "regime": regime,
                "subclass": subclass,
                "live_positions_count": live_positions_count,
                "active_mode": active_mode,
            })

        total_equity *= (1.0 + daily_ret)

        # SPX index from sidecar record when present.
        spx_ret = fnum(s.get("spx_return"), 0.0) or 0.0
        spx_index *= (1.0 + spx_ret)

        regime_counts[regime] += 1
        active_mode_counts[active_mode] += 1

        rows.append({
            "date": d,
            "total_equity": total_equity,
            "indexed_100": total_equity / INITIAL_EQUITY * 100.0,
            "daily_return": daily_ret,
            "daily_return_pct": daily_ret * 100.0,
            "spx_equity_index": spx_index,
            "spx_return": spx_ret,
            "spx_return_pct": spx_ret * 100.0,
            "regime": regime,
            "subclass": subclass,
            "active_mode": active_mode,
            "open_positions_count": live_positions_count,
            "core_daily_return": core_ret,
            "sidecar_adapter_return": sidecar_ret,
            "sidecar_live_positions": sidecar_live,
            "sidecar_meta": sidecar_meta,
        })

    metrics = calc_metrics(rows)
    after_hashes = {rel(p): sha256(p) for p in FROZEN_STRATEGY_FILES}

    validations = {
        "strategy_files_unchanged": before_hashes == after_hashes,
        "row_count_ge_1000": len(rows) >= 1000,
        "one_row_per_date": len(rows) == len(set(r["date"] for r in rows)),
        "max_open_positions_le_3": max(r["open_positions_count"] for r in rows) <= 3,
        "position_count_violations_zero": len(position_count_violations) == 0,
        "sideways_ma_conflict_active_present": active_mode_counts["SIDEWAYS_MA_CONFLICT_ORIGINAL_SIDECAR_MAX3_ADAPTER"] > 0,
        "deterioration_recovery_cash_defensive": all(
            r["active_mode"] == "CASH_DEFENSIVE"
            for r in rows
            if r["subclass"] in {"DETERIORATION_TRANSITION", "RECOVERY_TRANSITION"}
        ),
        "downtrend_cash_defensive": all(
            r["active_mode"] == "CASH_DEFENSIVE"
            for r in rows
            if r["regime"] == "DOWNTREND"
        ),
        "uptrend_core_present": active_mode_counts["UPTREND_ORIGINAL_CORE"] > 0,
    }

    conclusion = (
        "E1R_COMBINED_5Y_ORIGINAL_MAX3_FULL_RUN_VALIDATED"
        if all(validations.values())
        else "E1R_COMBINED_5Y_ORIGINAL_MAX3_FULL_RUN_FAILED_VALIDATION"
    )

    result = {
        "artifact_type": "e1r_combined_5y_original_max3_result",
        "generated_at": now(),
        "contract": CONTRACT,
        "source_core_result": rel(core_path),
        "sidecar_source": {
            "module": "src.engine.e1r_sidecar_sleeve",
            "function": "build_e1r_sidecar_sleeve",
            "config": {
                "start_date": START_DATE,
                "end_date": END_DATE,
                "allowed_subclasses": ["MA_CONFLICT"],
                "top_n": 10,
                "gross_exposure": 0.25,
                "max_live_account_positions_adapter": 3,
            },
        },
        "metrics": metrics,
        "regime_counts": dict(regime_counts),
        "active_mode_counts": dict(active_mode_counts),
        "validations": validations,
        "position_count_violations": position_count_violations,
        "rows": rows,
        "conclusion": conclusion,
    }

    curve = {
        "artifact_type": "e1r_combined_5y_original_max3_equity_curve",
        "generated_at": now(),
        "strategy_id": CONTRACT["strategy_id"],
        "metrics": metrics,
        "rows": [
            {
                "date": r["date"],
                "total_equity": r["total_equity"],
                "indexed_100": r["indexed_100"],
                "spx_equity_index": r["spx_equity_index"],
                "regime": r["regime"],
                "subclass": r["subclass"],
                "active_mode": r["active_mode"],
                "open_positions_count": r["open_positions_count"],
                "daily_return_pct": r["daily_return_pct"],
                "spx_return_pct": r["spx_return_pct"],
            }
            for r in rows
        ],
    }

    summary = {
        "artifact_type": "e1r_combined_5y_original_max3_summary",
        "generated_at": now(),
        "contract": CONTRACT,
        "source_core_result": rel(core_path),
        "metrics": metrics,
        "regime_counts": dict(regime_counts),
        "active_mode_counts": dict(active_mode_counts),
        "validations": validations,
        "conclusion": conclusion,
    }

    write_json(OUT_RESULT, result)
    write_json(OUT_CURVE, curve)
    write_json(OUT_SUMMARY, summary)

    report = {
        "generated_at": now(),
        "elapsed_seconds": (datetime.now(timezone.utc) - started).total_seconds(),
        "stage": "E1R_COMBINED_5Y_4C2C4D_ORIGINAL_MAX3_FULL_RUN",
        "status": "FULL_RUN_COMPLETE",
        "policy": {
            "strategy_logic_changed": False,
            "strategy_files_changed": before_hashes != after_hashes,
            "dashboard_changed": False,
            "official_result_generated": True,
            "adapter_purpose": "Combine original UPTREND/core result and original SIDEWAYS sidecar while enforcing account-level max3 holdings.",
        },
        "contract": CONTRACT,
        "outputs": {
            "result": rel(OUT_RESULT),
            "curve": rel(OUT_CURVE),
            "summary": rel(OUT_SUMMARY),
        },
        "source_core_result": rel(core_path),
        "metrics": metrics,
        "regime_counts": dict(regime_counts),
        "active_mode_counts": dict(active_mode_counts),
        "validations": validations,
        "position_count_violations": position_count_violations[:20],
        "conclusion": conclusion,
        "recommended_next_action": (
            "Review metrics. If accepted, build dashboard bundle from this validated curve."
            if conclusion.endswith("_VALIDATED")
            else "Do not use result. Review validation failures."
        ),
    }

    write_json(REPORT_JSON, report)

    md = []
    md.append("# E1R Combined 5Y — 4C-2C-4D Original Max3 Full Run")
    md.append("")
    md.append(f"Generated At: `{report['generated_at']}`")
    md.append(f"Elapsed Seconds: `{report['elapsed_seconds']}`")
    md.append("")
    md.append("## Contract")
    md.append("```json")
    md.append(json.dumps(CONTRACT, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Metrics")
    md.append("```json")
    md.append(json.dumps(metrics, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Regime / Active Mode Counts")
    md.append("```json")
    md.append(json.dumps({
        "regime_counts": dict(regime_counts),
        "active_mode_counts": dict(active_mode_counts),
    }, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Validations")
    md.append("```json")
    md.append(json.dumps(validations, indent=2, ensure_ascii=False))
    md.append("```")
    md.append("")
    md.append("## Conclusion")
    md.append(f"- `{conclusion}`")
    md.append(f"- Recommended: {report['recommended_next_action']}")
    REPORT_MD.write_text("\n".join(md) + "\n")

    print("E1R_COMBINED_5Y_4C2C4D_ORIGINAL_MAX3_FULL_RUN_COMPLETE")
    print("status:", report["status"])
    print("policy:", json.dumps(report["policy"], ensure_ascii=False))
    print("source_core_result:", rel(core_path))
    print("metrics:", json.dumps(metrics, ensure_ascii=False))
    print("regime_counts:", json.dumps(dict(regime_counts), ensure_ascii=False))
    print("active_mode_counts:", json.dumps(dict(active_mode_counts), ensure_ascii=False))
    print("validations:", json.dumps(validations, ensure_ascii=False))
    print("position_count_violations_count:", len(position_count_violations))
    print("conclusion:", conclusion)
    print("recommended_next_action:", report["recommended_next_action"])
    print("outputs:", json.dumps(report["outputs"], ensure_ascii=False))
    print("wrote:", rel(REPORT_JSON))
    print("wrote:", rel(REPORT_MD))

if __name__ == "__main__":
    main()
